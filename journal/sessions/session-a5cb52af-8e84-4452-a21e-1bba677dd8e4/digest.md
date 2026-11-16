# Session DSH — relecture

- identifiant : `session-a5cb52af-8e84-4452-a21e-1bba677dd8e4`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-16 02:29:04
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche V2 (exploitable) : les **exemples de la doc** — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (**les candidats objets, les rôles normalisés, la durée**) et corrige les sorties qui ont bougé ; vérifie le `demarrage.md` (les 3 commandes) ; le **contrôle négatif** : aucune sortie de la doc ne doit différer du code (un script de vérification `tools/verifie_exemples.py` si possible). Fiche `reports/rapport-exemples-v2.md` + JSON, commit.

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

- **bash** `{"command": "pwd && ls && git status --short | head -50 && git log --oneline -5", "description": "Inspect workspace root and git state"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
AGENTS.md
bench
build
colab
data
dist
docs
drave-core
drave.egg-info
journal
models
__pycache__
pyproject.toml
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
run_real_clusters.py
run_sparsity.py
run_value_encoding.py
sprints
src
tools
work
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
 M tools/chantier/
… [1221 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/produit/ && wc -l docs/produit/exemples.md docs/produit/demarrage.md 2>/dev/null", "description": "List product docs"}`

  ```
demarrage.md
exemples.md
README.md
 1013 docs/produit/exemples.md
  287 docs/produit/demarrage.md
 1300 total
  ```

- **read** `{"file_path": "docs/produit/exemples.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md</path>
<type>file</type>
<content>
1: # Dix exemples d'analyse, commentés
2: 
3: > **Ce que ce document est.** Dix exécutions **réelles** du produit, avec leur JSON commenté. Il
4: > complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
5: > *comment lire* ce qui sort. Les **cinq premiers blocs** ont été produits le **2026-11-06** sur
6: > la branche `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et
7: > sans réseau ; ils ont été **rejoués le 2026-11-14** sur le code courant — F1 **0,7902**,
8: > attachement **238/238 labels** (238/239 cibles), schéma **v2**. Le format v2 ajoute
9: > `version: 2` et, sur un syntagme qui chevauche un autre, `meta.partition`/`meta.alternative` ;
10: > v1 reste lue ([schéma v2](../../tools/schemas/drave-annotation-v2.json)).
11: >
12: > **Les cinq blocs du 15/11.** Trois exécutions avec `--tagger` (§ 6) et deux avec `--reel`
13: > (§ 7), produites le **2026-11-15** avec la **clé DeepSeek** et un **cache disque neuf** : le
14: > coût affiché est donc réel (`réseau=1`, tokens non nuls). Le tagger ne change q
… [41524 caractères tronqués]
  ```

- **read** `{"file_path": "docs/produit/demarrage.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md</path>
<type>file</type>
<content>
1: # Démarrage en 5 minutes
2: 
3: > **Ce que ce document est.** Le parcours le plus court pour installer **drave** et lancer
4: > les commandes. Il part d'un **clone public** et ne suppose aucun fichier du dépôt de
5: > développement. Chaque commande et chaque sortie ont été **rejouées le 2026-11-15** sur un
6: > clone neuf (commit **7f1519f**, Python **3.13.16**, pip **26.2.1**), sans clé DeepSeek.
7: > Le relevé complet, les temps et le contrôle négatif sont dans
8: > [`reports/rapport-quickstart.md`](../../reports/rapport-quickstart.md) et
9: > [`reports/quickstart.json`](../../reports/quickstart.json).
10: 
11: **Prérequis** : Python **3.10+**, `git`, un terminal. Aucun GPU, aucun modèle, aucune clé pour
12: le chemin par défaut : le produit est **CPU, hors ligne et déterministe**.
13: 
14: ## 1. Cloner
15: 
16: ```bash
17: git clone https://github.com/stephanedenis/drave.git
18: cd drave
19: ```
20: 
21: ```text
22: Cloning into 'drave'...
23: ```
24: 
25: Le clone ne télécharge **pas** les sous-modules : `tools/docwatch` et `tools/structures`
26: restent absents
… [10806 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py --version; python3 tools/drave.py analyser \"Le chat dort.\"; echo \"exit=$?\"", "description": "Run current CLI basic example"}`

  ```
drave 0.1.0
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
exit=0
  ```

- **bash** `{"command": "git diff --stat && git diff docs/produit/demarrage.md | head -100", "description": "Inspect working diff"}`

  ```
docs/implantation/bloc-linguistique.md             |  13 +
 docs/pilotage/en-cours.md                          |  14 +-
 docs/pilotage/roadmap.md                           |  21 +-
 docs/produit/README.md                             | 165 ++++-
 docs/produit/demarrage.md                          |  38 +-
 journal/README.md                                  |   3 +-
 journal/sessions/MANIFEST.md                       |   5 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  28 +
 .../rapport.md                                     |  14 +-
 pyproject.toml                                     |   9 +-
 reports/INDEX.md                                   |   4 +-
 reports/README.md                                  |   4 +-
 reports/pensee-coherence-fiches-v7.json            |  19 +
 reports/pensee-dev-test-v10.json                   |   2 +-
 reports/pensee-quatre-modes.json                   | 734 ++++++++++++---------
 reports/rapport-audit-v7.md                        |   6 +-
 reports/rapport-bloc-linguistique.md               |   7 +
 reports/rapport-coherence-fiches-v7.md             |  17 +-
 reports/rapport-dev-test-v10.md                    |   2 +-
 reports/rapport-pensee-
… [3901 caractères tronqués]
  ```

- **bash** `{"command": "git diff tools/drave.py | head -250", "description": "Read working diff of CLI"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index e5469d2f..cc07e9e5 100644
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
… [11032 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"duree\\|role_normalise\\|normalis\\|candidats\" tools/drave.py | head -80", "description": "Search new fields in CLI"}`

  ```
450:    """Une valeur de syntagme sur une ligne (les blancs sont normalisés pour l'affichage)."""
498:        roles = [bl.normaliser_role(e.meta.get("role", "")) or "—" for e in syntagmes]
594:        sys.stdout.write(_sur(json.dumps(a.json(avec_duree=args.duree), ensure_ascii=False)) + "\n")
629:    `confiance`, `sous_seuil`, `source` et les candidats.
667:    duree = bool(getattr(args, "duree", False))
711:                    sys.stdout.write(_dumps(annotation.json(avec_duree=duree)))
728:                sys.stdout.write(_dumps(annotation.json(avec_duree=duree)))
735:        sys.stdout.write(_dumps(annotation.json(avec_duree=duree)))
1374:def _normaliser_tagger(argv: list[str]) -> list[str]:
1410:        "Options : --json, --jsonl, --duree, --fichier CHEMIN, --langue fr|en,\n"
1476:                          help="sortie JSON complète (annotation, sans durée sauf avec --duree)")
1477:    analyser.add_argument("--duree", action="store_true",
1478:                          help="ajouter la durée de l'analyse (cout.duree_s) au JSON "
1524:                    "du bloc prend le relais (champ `source`). `--json` publie les candidats.",
1540:                              "candidats)")
16
… [71 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json | python3 -c \"import json,sys; a=json.load(sys.stdin); print(json.dumps({k:a.get(k) for k in ('schema','version','langue','script','refus')},ensure_ascii=False)); print('root keys:',list(a)); [print(e['niveau'],e['type'],e['valeu … [168 caractères tronqués]`

  ```
{"schema": "drave.annotation", "version": 2, "langue": "fr", "script": "Latn", "refus": ""}
root keys: ['schema', 'version', 'texte', 'langue', 'script', 'source', 'refus', 'etiquettes', 'unites_semantiques', 'fraction_semantique', 'trace', 'cout', 'contexte']
pos DET Le {"ouvert": false}
syntagme GN Le chat {"role": "agent", "niveau": 1, "attachement": {"segment": "Le chat", "cible": "dort", "candidats": [{"span": {"debut": 8, "fin": 12}, "cible": "dort", "source": "heuristique"}]}}
pos NOUN chat {"ouvert": true}
pos VERB dort {"ouvert": true}
syntagme GV dort {"role": "predicat", "niveau": 0, "attachement": {"segment": "dort", "cible": "chat", "candidats": [{"span": {"debut": 3, "fin": 7}, "cible": "chat", "source": "heuristique"}]}}
pos PONCT . {"ouvert": false}
  ```

- **bash** `{"command": "grep -rn \"normaliser_role\\|duree_s\\|avec_duree\\|role_normalise\\|role=\" tools/bloc_linguistique.py src 2>/dev/null | head -60", "description": "Find role normalization and duration"}`

  ```
tools/bloc_linguistique.py:54:    from .roles_vocabulaire import normaliser_role as _normaliser_role
tools/bloc_linguistique.py:57:    from roles_vocabulaire import normaliser_role as _normaliser_role
tools/bloc_linguistique.py:99:def normaliser_role(role: str, strict: bool = True) -> str:
tools/bloc_linguistique.py:101:    return _normaliser_role(role, strict=strict)
tools/bloc_linguistique.py:113:        sortie["role"] = normaliser_role(sortie.get("role", ""))
tools/bloc_linguistique.py:116:            alternative["role"] = normaliser_role(alternative.get("role", ""))
tools/bloc_linguistique.py:151:    def json(self, avec_duree: bool = False) -> dict:
tools/bloc_linguistique.py:153:        if not avec_duree:
tools/bloc_linguistique.py:154:            cout.pop("duree_s", None)
tools/bloc_linguistique.py:1757:                              cout={"octets": 0, "duree_s": round(time.perf_counter() - t0, 6)})
tools/bloc_linguistique.py:1763:                              cout={"octets": len(texte.encode("utf-8", "replace")), "duree_s": round(time.perf_counter() - t0, 6)})
tools/bloc_linguistique.py:2119:                                "etiquettes": len(etiquettes), "duree_s": round(time.
… [1544 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json | python3 -m json.tool | head -120", "description": "Full annotation g001"}`

  ```
{
    "schema": "drave.annotation",
    "version": 2,
    "texte": "Le chat dort.",
    "langue": "fr",
    "script": "Latn",
    "source": "heuristique",
    "refus": "",
    "etiquettes": [
        {
            "niveau": "graph\u00e8me",
            "type": "lettres",
            "valeur": "Le",
            "debut": 0,
            "fin": 2,
            "source": "heuristique",
            "confiance": 0.99,
            "candidats": [],
            "langue": "fr",
            "script": "Latn",
            "meta": {}
        },
        {
            "niveau": "mot",
            "type": "mot",
            "valeur": "Le",
            "debut": 0,
            "fin": 2,
            "source": "heuristique",
            "confiance": 0.98,
            "candidats": [],
            "langue": "fr",
            "script": "Latn",
            "meta": {}
        },
        {
            "niveau": "pos",
            "type": "DET",
            "valeur": "Le",
            "debut": 0,
            "fin": 2,
            "source": "heuristique",
            "confiance": 0.92,
            "candidats": [],
            "langue": "fr",
            "script": "Latn",
            "meta": {
                "ou
… [2003 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,190p' tools/bloc_linguistique.py", "description": "Read bloc annotation json method"}`

  ```
#!/usr/bin/env python3
"""bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.

Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :

  - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
  - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
    substitution et le parallèle sans GPU ;
  - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
    même type d'annotation ;
  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
  - `Parallele` et `Cascade` : les deux modes de composition. Le parallèle fusionne les
    étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
    que l'heuristique ne couvre pas.

La sortie est une **annotation typée** — pas le corps de la RSN : chaque étiquette porte son
`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script`
… [6049 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json \\\n  | jq '{langue, script, refus,\n         pos: [.etiquettes[] | select(.niveau==\"pos\")\n           | {valeur, type, debut, fin, confiance, ouvert:.meta.ouvert}],\n         syntagmes: [.etiquettes[] | select(.niveau==\"syntag … [369 caractères tronqués]`

  ```
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "pos": [
    {
      "valeur": "Le",
      "type": "DET",
      "debut": 0,
      "fin": 2,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "chat",
      "type": "NOUN",
      "debut": 3,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "dort",
      "type": "VERB",
      "debut": 8,
      "fin": 12,
      "confiance": 0.72,
      "ouvert": true
    },
    {
      "valeur": ".",
      "type": "PONCT",
      "debut": 12,
      "fin": 13,
      "confiance": 0.95,
      "ouvert": false
    }
  ],
  "syntagmes": [
    {
      "valeur": "Le chat",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confiance": 0.55,
      "role": "agent",
      "cible": "dort",
      "union": null,
      "candidats": [
        "structure la plus proche",
        "dort"
      ]
    },
    {
      "valeur": "dort",
      "type": "GV",
      "debut": 8,
      "fin": 12,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "chat",
      "union": null,
      "candidats": [
        "structure la plus proche"
      ]
    }
  ],
  "phrase": [
    {
      "type": "ty
… [132 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" --json \\\n  | jq '{langue, script, refus,\n         syntagmes: [.etiquettes[] | select(.niveau==\"syntagme\")\n           | {valeur, type, debut, fin, confiance, role:.meta.role,\n              cible:.meta.attach … [261 caractères tronqués]`

  ```
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "syntagmes": [
    {
      "valeur": "Le livre",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.55,
      "role": "agent",
      "cible": "intéressant",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ]
    },
    {
      "valeur": "que j'ai lu",
      "type": "REL",
      "debut": 9,
      "fin": 20,
      "confiance": 0.55,
      "role": "qualite",
      "cible": "livre",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ]
    },
    {
      "valeur": "que j'ai lu est intéressant",
      "type": "REL",
      "debut": 9,
      "fin": 36,
      "confiance": 0.3,
      "role": "qualite",
      "cible": "livre",
      "union": true,
      "candidats": [
        "REL",
        "livre",
        "intéressant"
      ]
    },
    {
      "valeur": "est intéressant",
      "type": "GV",
      "debut": 21,
      "fin": 36,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "livre",
      "union": null,
      "candidats": [
        "« que j'ai 
… [291 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"The day when we left was beautiful.\" --langue en --json \\\n  | jq '{langue, script, refus,\n         pos: [.etiquettes[] | select(.niveau==\"pos\")\n           | {valeur, type, debut, fin, confiance, ouvert:.meta.ouvert}],\n         syntagmes: [.etiqu … [229 caractères tronqués]`

  ```
{
  "langue": "en",
  "script": "Latn",
  "refus": "",
  "pos": [
    {
      "valeur": "The",
      "type": "DET",
      "debut": 0,
      "fin": 3,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "day",
      "type": "NOUN",
      "debut": 4,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "when",
      "type": "CONJ",
      "debut": 8,
      "fin": 12,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "we",
      "type": "PRON",
      "debut": 13,
      "fin": 15,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "left",
      "type": "VERB",
      "debut": 16,
      "fin": 20,
      "confiance": 0.85,
      "ouvert": true
    },
    {
      "valeur": "was",
      "type": "AUX",
      "debut": 21,
      "fin": 24,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "beautiful",
      "type": "ADJ",
      "debut": 25,
      "fin": 34,
      "confiance": 0.68,
      "ouvert": true
    },
    {
      "valeur": ".",
      "type": "PONCT",
      "debut": 34,
      "fin": 35,
      "confiance": 0.95,
      "ouvert": false
    }
  ],
  "synta
… [777 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"The film she talks about is out.\" --json \\\n  | jq '{langue, script, refus,\n         syntagmes: [.etiquettes[] | select(.niveau==\"syntagme\")\n           | {valeur, type, debut, fin, confiance, role:.meta.role,\n              cible:.meta.attachement … [256 caractères tronqués]`

  ```
{
  "langue": "en",
  "script": "Latn",
  "refus": "",
  "syntagmes": [
    {
      "valeur": "The film",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.35,
      "role": "objet",
      "cible": "out",
      "union": null,
      "candidats": [
        "GN",
        "out"
      ]
    },
    {
      "valeur": "she talks about",
      "type": "REL",
      "debut": 9,
      "fin": 24,
      "confiance": 0.35,
      "role": "qualite",
      "cible": "film",
      "union": null,
      "candidats": [
        "REL",
        "film",
        "out"
      ]
    },
    {
      "valeur": "is out",
      "type": "GV",
      "debut": 25,
      "fin": 31,
      "confiance": 0.35,
      "role": "predicat",
      "cible": null,
      "union": null,
      "candidats": [
        "GV"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type",
      "valeur": "déclarative"
    }
  ],
  "pragmatique": [
    {
      "type": "acte",
      "valeur": "assertion"
    }
  ]
}
  ```

- **bash** `{"command": "sed -n '1,220p' tools/roles_vocabulaire.py", "description": "Read role vocabulary"}`

  ```
"""roles_vocabulaire.py — le vocabulaire **fermé** des rôles de l'annotation.

Le produit publie un rôle par syntagme (`meta.role`). Les règles internes en produisent
plusieurs orthographes et plusieurs granularités : `prédicat`/`predicat`, `qualité`/
`qualite`, `patient`/`complément`/`groupe nominal` pour un GN, `possession` pour le
possesseur, etc. Un consommateur qui filtre `role == "predicat"` ne doit pas dépendre de
la règle qui a produit le segment.

Ce module est la **seule** table de passage. Il est pur (aucun import du bloc) pour que
les tests puissent le charger seul et pour que le schéma JSON puisse publier la même
liste (`tools/schemas/drave-annotation-v2.json`).

    from tools.roles_vocabulaire import ROLES, normaliser_role
    normaliser_role("prédicat")        # "predicat"
    normaliser_role("groupe nominal")  # "objet"
    normaliser_role("inventé")         # lève RoleHorsVocabulaire

Le vocabulaire est volontairement **petit** : huit rôles. Ce n'est pas une annotation
sémantique plus fine ; c'est une **normalisation** de ce que les règles publient déjà.
La table est exhaustive pour les rôles produits par `bloc_linguistique.py` et le
générateur S ; un rôle inconnu
… [3301 caractères tronqués]
  ```

- **bash** `{"command": "git diff docs/implantation/bloc-linguistique.md | head -80; git diff tools/tests/test_produit.py tools/tests/test_empaquetage.py | head -120", "description": "Read related docs/tests diffs"}`

  ```
diff --git a/docs/implantation/bloc-linguistique.md b/docs/implantation/bloc-linguistique.md
index cd9f8728..36ea8a61 100644
--- a/docs/implantation/bloc-linguistique.md
+++ b/docs/implantation/bloc-linguistique.md
@@ -265,6 +265,19 @@ banc est classé `sco` (ou `und` sous le seuil) par l'heuristique ; le profil UD
 **parallèle et propre**, ce n'est pas 398 langues de déploiement. Le bloc est honnête : il dit
 `und` sous le seuil, il ne force pas une langue.
 
+**L'exposition produit — `drave profils`.** Les profils ne restent pas dans le banc :
+`drave profils --texte` rend la **langue probable**, le **script** et la **confiance** depuis
+l'artefact embarqué (398 langues, `tools/tests/linguistique/profils_udhr.json`), et
+`analyser --profils` emploie le même détecteur pour l'annotation. La décision est `und` sous
+le seuil **0,12** ; la langue probable et la confiance restent publiées. Sur un texte court,
+le prior des mots-outils des sept langues du bloc peut trancher (`source: lexique`) ; sur un
+texte long, les 398 profils (`source: profils`). Mesure : **20/20** langues et **20/20**
+scripts sur les 20 langues stratifiées de l'échantillon UDHR (article 15), **313/320 =
+0,9781**
… [2960 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -30", "description": "Recent commits"}`

  ```
2e617034 EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)
1d4eb49e JOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4
c77ed4b6 U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE
04894aea U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4)
75a56c05 U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)
d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/4 LUE, 86E PORTE VERTE
9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS
7e195ee6 T4 — CORRECTION DE LA FICHE : LE POINT 4 000 MOTS A PL
… [2888 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline --all -- tools/roles_vocabulaire.py | head -10; git log --oneline --all -S 'avec_duree' -- tools/bloc_linguistique.py | head -10; git log --oneline --all -S 'candidats' -- tools/bloc_linguistique.py | head -10", "description": "Find feature commits"}`

  ```
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
651bfc90 BLOC LINGUISTIQUE — NEUF NIVEAUX, HEURISTIQUE ET NEURONAL, 398 LANGUES À 0,9687
d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
efbae885 B13 — LE NOM PROPRE SUJET EST UN GN : F1 0,7438 → 0,7535, TÊTE 0,865, ATTACHEMENT 236/237 ; 183/183
c78a53bd B13 — LE PRONOM SUJET EST UN GN : F1 0,6519 → 0,7013 (+4,9), TÊTE 0,7709 → 0,8141, ATTACHEMENT PRÉSERVÉ (236/237, 0,9916) ; 183/183
c43dd5cc B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183
6b976cb1 B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 
… [381 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat 7f1519f7 | head -60; git show --stat 9a291c8b | head -40; git show --stat 7d114559 | head -40", "description": "Inspect feature commits stats"}`

  ```
commit 7f1519f749ab0939ad24b642abe785e7ab0aa87a
Author: Stéphane <stephane@localhost>
Date:   Sun Nov 15 22:12:42 2026 -0500

    T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)

 .gitignore                                         |    3 +
 docs/pilotage/en-cours.md                          |    8 +-
 docs/produit/README.md                             |  131 +-
 docs/produit/exemples.md                           |    8 +-
 journal/2026-11-15/README.md                       |   25 +-
 journal/2026-11-15/distribue.md                    |    5 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/memoire.md                      |    2 +-
 journal/2026-11-15/mesures.md                      |    2 +-
 journal/2026-11-15/modele.md                       |    2 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    4 +-
 journal/sessions/MANIFEST.md                       |    6 +-
 .../e181ce02-cd50-488a-a6be-e84b
… [6414 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i 'exemple\\|quickstart'; ls tools/ | grep -i 'exemple\\|verifie'", "description": "Existing reports and verifiers"}`

  ```
quickstart.json
rapport-exemples-rejoues.json
rapport-exemples-rejoues.md
rapport-exemples-tagger.json
rapport-exemples-tagger.md
rapport-quickstart.md
verifie_backlog.py
verifie_contamination.py
verifie_en_cours.py
verifie_etat_a_jour.py
verifie_journal.py
verifier_bilan.py
verifier_chaine_etat.py
verifier_faq.py
verifier_formats.py
verifier_liens_faq.py
verifier_liens.py
verifier_parite_native.py
verifier_performance_fix.py
verifier_schema_produit.py
verifier_schemas.py
verifier_table_types.sh
verifier_v41_engram.py
verifier_v41_mhc.py
  ```

- **bash** `{"command": "git show 7f1519f7 -- docs/produit/exemples.md", "description": "See doc changes from T1-T2"}`

  ```
commit 7f1519f749ab0939ad24b642abe785e7ab0aa87a
Author: Stéphane <stephane@localhost>
Date:   Sun Nov 15 22:12:42 2026 -0500

    T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)

diff --git a/docs/produit/exemples.md b/docs/produit/exemples.md
index b4b8cf6a..493cd772 100644
--- a/docs/produit/exemples.md
+++ b/docs/produit/exemples.md
@@ -48,12 +48,16 @@
 - `--reel` : ce n'est pas une annotation, c'est une **évaluation**. Le JSON porte
   `gold.nom: "réel (hand + reel, sans synthétique)"`, `gold.phrases: 452`,
   `gold.cibles_attachement: 184` et `reel: null` (la base mesurée **est** déjà la base réelle).
-- `meta.attachement` : `{segment, cible}` ; `cible` est une **chaîne**, pas un span.
+- `meta.attachement` : `{segment, cible, candidats}` ; `cible` est une **chaîne**, et
+  `candidats` (v2) est une liste d'objets `{span, cible, source}` — `span` donne la position
+  exacte de la cible dans `texte`. Un candidat dont la cible n'est pas retrouvée est écarté.
 - `meta.partition` : `{groupe, rang, membres, vue}` — présent sur un syntagme d'un groupe de
   chevauc
… [879 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"candidat\\|role\\|rôle\\|durée\\|duree\" docs/produit/README.md | head -80", "description": "Search README for features"}`

  ```
27:> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
28:> candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.
49:| **linguiste, enseignant, curieux** | une analyse immédiate : POS, syntagmes, rôles, attachement, acte de parole | c'est une **annotation**, pas une traduction ni une correction |
50:| **développeur NLP** | un JSON déterministe, des spans, une confiance, des candidats | le format est **versionné** (schéma v2) ; v1 reste lue (§ 7) |
66:documentent les syntagmes qui se chevauchent, `meta.attachement.candidats` publie les
67:candidats en **objets** `{span, cible, source}`, et `meta.role` appartient à un
68:**vocabulaire fermé** de huit rôles.
75:| **attachement** | par syntagme : `role`, `cible`, `candidats` (objets v2, chaînes d'affichage en lecture) | **238/239** exacts ; couverture **0,9958** ; exact sur span **1,0000** ; **2 139** candidats objets, **0** span faux |
77:| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |
82:**candidats**. C'est une lecture, avec sa confiance ; ce n'est pas un arbre syntaxique complet.
89:1
… [6301 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"verifie_exemples\\|exemples.md\" tools tests 2>/dev/null | head -40; grep -rn \"exemples.md\" --include='*.py' --include='*.sh' . | head -40", "description": "Find existing checks referencing examples"}`

  ```
tools/chantier/plan.json:314:   "mandat": "Tâche J11.1 : rejoue les 5 blocs de `docs/produit/exemples.md`, corrige les sorties, fiche `reports/rapport-exemples-rejoues.md`, commit.",
tools/chantier/plan.json:504:   "mandat": "Tâche D1 : les exemples de `docs/produit/exemples.md` — ajoute 3 exemples avec `--tagger` (la sortie réelle avec la clé, le coût affiché) et 2 avec `--reel` (la base honnête), et vérifie que les sorties collent au code courant (F1 0,7902, 238/239, schéma v2). Fiche `reports/rapport-exemples-tagger.md` + JSON, commit.",
tools/chantier/plan.json:898:   "mandat": "Tâche V2 (exploitable) : les **exemples de la doc** — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (**les candidats objets, les rôles normalisés, la durée**) et corrige les sorties qui ont bougé ; vérifie le `demarrage.md` (les 3 commandes) ; le **contrôle négatif** : aucune sortie de la doc ne doit différer du code (un script de vérification `tools/verifie_exemples.py` si possible). Fiche `reports/rapport-exemples-v2.md` + JSON, commit.",
  ```

- **bash** `{"command": "sed -n '55,175p' docs/produit/README.md; sed -n '300,360p' docs/produit/README.md; sed -n '660,690p' docs/produit/README.md; sed -n '855,870p' docs/produit/README.md", "description": "Read README key sections"}`

  ```
quatre gold sont versionnés dans `tools/tests/linguistique/` ; le corpus UDHR, lui, ne l'est pas
(voir § 4).

**Ce que ce n'est pas** : un produit grand public, un traducteur, un générateur, un correcteur,
un serveur. Le produit **lit** et **étiquette** ; il n'écrit pas de texte.

## 2. Ce que le produit fait

Une seule opération : `analyser(texte, langue)` → une **annotation**. Elle porte neuf niveaux ;
le produit en expose cinq, plus le coût et la trace. Le JSON est estampillé `schema`
(`"drave.annotation"`) et `version` (`2`) ; en v2, `meta.partition` et `meta.alternative`
documentent les syntagmes qui se chevauchent, `meta.attachement.candidats` publie les
candidats en **objets** `{span, cible, source}`, et `meta.role` appartient à un
**vocabulaire fermé** de huit rôles.

| ce que vous demandez | ce que vous obtenez | mesure du 15/11 |
|---|---|---|
| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; `drave profils` les expose, `--langue` reste un indice `fr`/`en`) |
| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 4
… [12307 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"\"; echo \"exit=$?\"; echo '---'; python3 tools/drave.py analyser \"\" --json; echo \"exit=$?\"; echo '---'; python3 tools/bloc_linguistique.py --texte \"\" --json | jq '{langue, script, refus, etiquettes: (.etiquettes|length)}'; echo \"exit=$?\"", "des … [36 caractères tronqués]`

  ```
exit=3
---
{
 "schema": "drave.annotation",
 "version": 2,
 "texte": "",
 "langue": "und",
 "script": "Zyyy",
 "source": "heuristique",
 "refus": "vide",
 "etiquettes": [],
 "unites_semantiques": [],
 "fraction_semantique": 0.0,
 "trace": [
  {
   "etape": "refus",
   "raison": "vide"
  }
 ],
 "cout": {
  "octets": 0
 },
 "contexte": ""
}
exit=3
---
{
  "langue": "und",
  "script": "Zyyy",
  "refus": "vide",
  "etiquettes": 0
}
exit=0
[stderr]
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --reel; echo \"exit=$?\"", "description": "Replay reel evaluation"}`

  ```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold réel (hand + reel, sans synthétique) · 452 phrases · 2480 tokens · 184 cibles d'attachement

POS         exactitude 88.91 %  (fermé 92.94 %, ouvert 84.66 %)
SYNTAGMES   F1 79.06 %  (P 81.28 % / R 76.95 %)
  tête      F1 89.90 %  (P 93.84 % / R 86.28 %)
  vue linéaire (partition filtrer) F1 79.53 %  · attachement 91.85 % de couverture
BASE RÉELLE — (déjà la base, ou gold gelé)
ATTACHEMENT exact 99.46 % · couverture 99.46 % · exact sur span 100.00 % · top-k 98.91 %
  tête      couverture 100.00 % · top-k 99.45 %
PRAGMATIQUE acte 99.56 % · négation 96.90 % · modalité 98.45 % · double sens 96.46 %
FRACTION SÉMANTIQUE 50.82 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 0.00 % (graine 0, 184 cibles)
exit=0
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"\" 2>/tmp/err.txt 1>/tmp/out.txt; echo \"exit=$?\"; echo \"stdout=[$(cat /tmp/out.txt)]\"; echo \"stderr=[$(cat /tmp/err.txt)]\"", "description": "Separate refusal streams"}`

  ```
exit=3
stdout=[]
stderr=[drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)]
  ```

- **bash** `{"command": "test -f ~/.config/drave/deepseek.key && echo \"cle fichier presente\" || echo \"pas de cle fichier\"; test -n \"$DEEPSEEK_API_KEY\" && echo \"env presente\" || echo \"pas d'env\"; test -n \"$DEEPSEEK_KEY_FILE\" && echo \"key_file present\" || true", "description": "Check DeepSeek key av … [12 caractères tronqués]`

  ```
cle fichier presente
pas d'env
  ```

- **bash** `{"command": "sed -n '1,240p' reports/rapport-exemples-rejoues.md 2>/dev/null | head -120; cat reports/rapport-exemples-rejoues.json 2>/dev/null | head -60", "description": "Read prior examples replay report"}`

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
… [6327 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\n# print nearby tasks around mandate V2\nfor i,t in enumerate(p.get('taches',p if isinstance(p,list) else [])):\n    pass\nprint(type(p), list(p)[:10] if isinstance(p,dict) else len(p))\nPY\ngrep -n -B5 -A5 'V2 … [83 caractères tronqués]`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
893-  },
894-  {
895-   "id": "V2",
896-   "jour": 21,
897-   "titre": "Les exemples — le JSON de la v2",
898:   "mandat": "Tâche V2 (exploitable) : les **exemples de la doc** — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (**les candidats objets, les rôles normalisés, la durée**) et corrige les sorties qui ont bougé ; vérifie le `demarrage.md` (les 3 commandes) ; le **contrôle négatif** : aucune sortie de la doc ne doit différer du code (un script de vérification `tools/verifie_exemples.py` si possible). Fiche `reports/rapport-exemples-v2.md` + JSON, commit.",
899-   "budget_min": 90,
900-   "acceptation": [
901-    {
902-     "commande": "test -f reports/rapport-exemples-v2.md && echo FICHE-OK",
903-     "attendu": "FICHE-OK"
  ```

- **bash** `{"command": "grep -rn \"V2\\|exemples\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -40", "description": "Search state/roadmap for V2"}`

  ```
docs/pilotage/roadmap.md:59:**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
docs/pilotage/roadmap.md:65:[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. **D1** ajoute **3** exemples
docs/pilotage/roadmap.md:66:`--tagger` et **2** `--reel` à [`exemples.md`](../produit/exemples.md)
docs/pilotage/roadmap.md:67:([`fiche`](../../reports/rapport-exemples-tagger.md)).
docs/pilotage/roadmap.md:144:schéma v2, restitution v1, 50 textes, 5 exemples, fr/en), tagger (**0,9475, +8,49**), Panini
  ```

- **bash** `{"command": "sed -n '890,940p' tools/chantier/plan.json", "description": "Read V2 acceptance criteria"}`

  ```
"attendu": "STRICT-0"
    }
   ]
  },
  {
   "id": "V2",
   "jour": 21,
   "titre": "Les exemples — le JSON de la v2",
   "mandat": "Tâche V2 (exploitable) : les **exemples de la doc** — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (**les candidats objets, les rôles normalisés, la durée**) et corrige les sorties qui ont bougé ; vérifie le `demarrage.md` (les 3 commandes) ; le **contrôle négatif** : aucune sortie de la doc ne doit différer du code (un script de vérification `tools/verifie_exemples.py` si possible). Fiche `reports/rapport-exemples-v2.md` + JSON, commit.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-exemples-v2.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
    {
     "commande": "bash tools/porte-produit.sh 2>&1 | tail -1",
     "attendu": "verte"
    }
   ]
  },
  {
   "id": "V3",
   "jour": 21,
   "titre": "La clôture — le tag exploitable",
   "mandat": "Tâche V3 (clôture) : la clôture de la nuit — le rapport `reports/rapport-bilan-exploitable-2.md` + JSON (les 9 tâches T/U/V, les chiffres, les négatifs), la mise à jour de `docs/pilotage/en-cours.md` et de la roadmap, le **tag annoté** `
… [407 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/porte-produit.sh", "description": "Read product gate"}`

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
… [5067 caractères tronqués]
  ```

- **bash** `{"command": "git diff tools/porte-produit.sh", "description": "Diff product gate"}`

  ```
diff --git a/tools/porte-produit.sh b/tools/porte-produit.sh
index a638d075..a1ce87dd 100755
--- a/tools/porte-produit.sh
+++ b/tools/porte-produit.sh
@@ -31,6 +31,21 @@ assert any(e['niveau'] == 'pos' for e in d['etiquettes'])
   fi
 done
 
+if sortie=$(python3 tools/drave.py profils --texte "Le chat dort." --json 2>&1) \
+   && printf '%s' "$sortie" | python3 -c "
+import json, sys
+d = json.load(sys.stdin)
+assert d['schema'] == 'drave.profils', d.get('schema')
+assert d['langue'] == 'fra', d.get('langue')
+assert d['script'] == 'Latn', d.get('script')
+assert d['profils']['langues'] == 398, d.get('profils')
+assert 0.0 < d['confiance'] <= 1.0, d.get('confiance')
+" 2>/dev/null; then
+  dit ✅ "profils : langue, script, confiance, 398 profils"
+else
+  dit ❌ "profils : sortie inattendue : $sortie"; ko=1
+fi
+
 a=$(python3 tools/drave.py rejouer "Le chat dort." 2>&1 | grep -o 'sha256 [0-9a-f]*' | head -1)
 b=$(python3 tools/drave.py rejouer "Le chat dort." 2>&1 | grep -o 'sha256 [0-9a-f]*' | head -1)
 if [ -n "$a" ] && [ "$a" = "$b" ]; then dit ✅ "rejeu : $a deux fois"; else dit ❌ "rejeu instable : '$a' vs '$b'"; ko=1; fi
@@ -41,6 +56,12 @@ else
   dit ❌ "smoke test en échec (voir
… [499 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat 2e617034 | head -50; git show --stat 1d4eb49e | head -30; git log -1 --format='%H %ci %s'", "description": "Inspect U3 commit"}`

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
commit 1d4eb49e0435a05127437c2baf477b043a019460
Author: Stéphane <stephane@
… [1150 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -5 -- tools/drave.py; git log --oneline -5 -- tools/bloc_linguistique.py; git log --oneline -5 -- pyproject.toml; git log --oneline -5 -- docs/produit/demarrage.md", "description": "Last commits per file"}`

  ```
c77ed4b6 U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE
9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
519b729f J5 — Y1 : LE MODE AUTO DU TAGGER (CLÉ 0/130 TOKENS, INVALIDE 0, SANS CLÉ 0 IDENTIQUE AU DÉFAUT, RÉSEAU 0 APRÈS 3 ESSAIS) ; 30/30 TESTS
9960b37f SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE GOLD v2 NE GAGNE QU'UN CADRE (20/46, F1 0,5406, LIEU 0,60) ; --roles-v3 OPT-IN
d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
9960b37f SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE
… [1021 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/structures 2>/dev/null | head; git submodule status 2>/dev/null; cat .gitmodules 2>/dev/null", "description": "Check structures submodule"}`

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
 d256888934b017ac024de2a8eed22ecf81e6c799 tools/docwatch (v0.4.1-3-gd256888)
 648adce3ea18ef4d142778fd67d42413aae5ae64 tools/structures (heads/master)
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
  ```

- **bash** `{"command": "grep -n \"rôle=objet\\|rôle=agent\\|79.02\\|81.88\\|88.70\\|99.58\" reports/rapport-quickstart.md | head -30; sed -n '1,80p' reports/rapport-quickstart.md", "description": "Read quickstart report"}`

  ```
14:> découvre l'écart du sous-module : `analyser` rend `rôle=objet` / `GV → —` au lieu de
15:> `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %** au lieu de **79,02 %** / **99,58 %**.
83:| `drave analyser "Le chat dort."` | `/tmp/qs-doc/drave` | **0** | `langue=fr`, `GN [0:7] Le chat rôle=objet → dort`, `GV [8:12] dort rôle=predicat → —` |
93:| `drave evaluer` | `/tmp/qs-doc/drave` | **0** | **86,25 %** | **81,88 %** | **88,70 %** |
178:| `evaluer` — F1 | **81,88 %** | **79,02 %** |
179:| `evaluer` — attachement exact | **88,70 %** | **99,58 %** |
186:clone public (81,88 contre 79,02) **n'est pas un gain** : il s'accompagne de 10,88 points
204:sous-module), rendent `agent` / `chat` et **79,02 % / 99,58 %**. C'est ce contraste qui prouve
# T3 — le démarrage en 5 minutes : clone public, installation, trois commandes, JSON, tagger, erreurs

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T3** (exploitable, 3/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **quickstart livré et rejoué** ; ⚠️ le **clone
> public** n'a pas le sous-module `tools/structures`, donc la sortie d'un débutant est
> **dégradée** par rapport au dépôt de développement. Le document le dit, mesure l'
… [3572 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"structures\" tools/drave.py tools/bloc_linguistique.py tools/produit* 2>/dev/null | head -40", "description": "Find structures usage"}`

  ```
tools/bloc_linguistique.py:1222:            if str(RACINE / "tools/structures") not in sys.path:
tools/bloc_linguistique.py:1223:                sys.path.insert(0, str(RACINE / "tools/structures"))
  ```

- **bash** `{"command": "grep -rn \"rôle=objet\\|groupe nominal\\|generateur\" tools/bloc_linguistique.py | head -40", "description": "Find role generation logic"}`

  ```
1224:            import generateur  # le générateur S, importé en lecture seule
1225:            return generateur.analyser(texte)
1239:            import generateur
1240:            base = generateur._segmente(texte, generateur._tokens(texte))
1660:                role = "groupe nominal"
2443:                  "Étiquettes : O (hors syntagme), B-GN/I-GN (groupe nominal), B-GV/I-GV (groupe "
  ```

- **bash** `{"command": "rm -rf /tmp/qs-check && mkdir -p /tmp/qs-check && git archive HEAD | tar -x -C /tmp/qs-check && ls /tmp/qs-check/tools | head && (cd /tmp/qs-check && python3 tools/drave.py --version && python3 tools/drave.py analyser \"Le chat dort.\" && python3 tools/drave.py evaluer) 2>&1 | head -50" … [73 caractères tronqués]`

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
drave 0.1.0
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
SYNTAGMES   F1 81.88 %  (P 86.64 % / R 77.62 %)
  tête      F1 90.83 %  (P 96.11 % / R 86.10 %)
  vue linéaire (partition filtrer) F1 81.88 %  · attachement 93.72 % de couverture
BASE RÉELLE (hand + reel, 452 phrases)  P
… [408 caractères tronqués]
  ```

- **bash** `{"command": "du -sh /tmp/qs-check; git ls-files | wc -l; du -sh .git", "description": "Check archive size"}`

  ```
134M	/tmp/qs-check
4147
404M	.git
  ```

- **bash** `{"command": "du -sh tools tools/tests/linguistique 2>/dev/null; find tools -maxdepth 1 -type d | head -30", "description": "Sizes of tools"}`

  ```
114M	tools
tools
tools/tokenizer_kimi
tools/__pycache__
tools/jeux
tools/llm
tools/semantique
tools/cerveau
tools/docwatch
tools/tests
tools/hooks
tools/pensee
tools/structures
tools/schemas
tools/chantier
  ```

- **bash** `{"command": "du -sh tools/structures tools/docwatch tools/tests/linguistique tools/llm 2>/dev/null; du -sh * | sort -h | tail -10", "description": "Subdir sizes"}`

  ```
1,1M	tools/structures
88M	tools/docwatch
2,9M	tools/tests/linguistique
552K	tools/llm
2,0M	dist
4,6M	docs
7,1M	build
32M	reports
114M	tools
332M	drave-core
442M	journal
2,5G	models
18G	work
127G	data
  ```

- **bash** `{"command": "rm -rf /tmp/qs2 && mkdir -p /tmp/qs2 && cp -a tools /tmp/qs2/tools && rm -rf /tmp/qs2/tools/structures /tmp/qs2/tools/docwatch && (cd /tmp/qs2 && python3 tools/drave.py analyser \"Le chat dort.\" | head -5 && python3 tools/drave.py evaluer | tail -4)", "description": "Test minimal no-st … [15 caractères tronqués]`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=objet     → dort
  tête      couverture 100.00 % · top-k 95.54 %
PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %
FRACTION SÉMANTIQUE 54.76 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
  ```

- **bash** `{"command": "python3 tools/drave.py profils --texte \"Le chat dort.\"; echo \"exit=$?\"; python3 tools/drave.py profils --texte \"Привет мир\" --json | head -40; echo \"exit=$?\"; python3 tools/drave.py analyser \"Le chat dort.\" --profils | head -8", "description": "Replay demarrage profils outputs … [2 caractères tronqués]`

  ```
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue=fra script=Latn confiance=0.3333 source=lexique
langue      : fra (French)
script      : Latn
confiance   : 0.3333 (marge 0.0000, seuil 0.12)
source      : lexique
prior       : fra (mots-outils 0.3333)
candidats   : hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
exit=0
{
 "schema": "drave.profils",
 "version": 1,
 "texte": "Привет мир",
 "langue": "rus",
 "langue_probable": "rus",
 "nom": "Russian",
 "script": "Cyrl",
 "confiance": 0.22,
 "marge": 0.125,
 "source": "profils",
 "seuil": 0.12,
 "sous_seuil": false,
 "refus": "",
 "prior": null,
 "candidats": [
  {
   "langue": "rus",
   "nom": "Russian",
   "score": 0.25
  },
  {
   "langue": "bos",
   "nom": "Bosnian (Cyrillic)",
   "score": 0.125
  },
  {
   "langue": "bul",
   "nom": "Bulgarian",
   "score": 0.125
  },
  {
   "langue": "evn",
   "nom": "Evenki",
   "score": 0.125
  },
  {
   "langue": "gld",
   "nom": "Nanai",
   "score": 0.125
exit=0
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fra script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS
… [240 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json > /tmp/annotation.json; wc -c /tmp/annotation.json; sed -n '1,22p' /tmp/annotation.json; python3 -c 'import json; a=json.load(open(\"/tmp/annotation.json\")); print(a[\"schema\"], a[\"version\"], a[\"langue\"], len(a[\"etiquettes\ … [193 caractères tronqués]`

  ```
6179 /tmp/annotation.json
{
 "schema": "drave.annotation",
 "version": 2,
 "texte": "Le chat dort.",
 "langue": "fr",
 "script": "Latn",
 "source": "heuristique",
 "refus": "",
 "etiquettes": [
  {
   "niveau": "graphème",
   "type": "lettres",
   "valeur": "Le",
   "debut": 0,
   "fin": 2,
   "source": "heuristique",
   "confiance": 0.99,
   "candidats": [],
   "langue": "fr",
   "script": "Latn",
   "meta": {}
  },
drave.annotation 2 fr 20 étiquettes
[('GN', 'Le chat', 'agent'), ('GV', 'dort', 'predicat')]
  ```

- **bash** `{"command": "(cd /tmp/qs2 && python3 tools/drave.py analyser \"Le chat dort.\" --json > /tmp/annotation-no-structures.json); wc -c /tmp/annotation-no-structures.json; python3 -c 'import json; a=json.load(open(\"/tmp/annotation-no-structures.json\")); print([(e[\"type\"], e[\"valeur\"], e[\"meta\"].g … [116 caractères tronqués]`

  ```
5899 /tmp/annotation-no-structures.json
[('GN', 'Le chat', 'objet'), ('GV', 'dort', 'predicat')]
  ```

- **bash** `{"command": "jq --version; python3 --version; git --version", "description": "Check tool versions"}`

  ```
jq-1.8.2
Python 3.13.16
git version 2.56.0
  ```

- **bash** `{"command": "sed -n '1,160p' docs/pilotage/en-cours.md", "description": "Read current state"}`

  ```
# En ce moment

**Mis à jour : 2026-11-16 (`evaluer --strict`)**

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
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 
… [11167 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' docs/pilotage/roadmap.md", "description": "Read roadmap"}`

  ```
# La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers

> **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
> L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
> contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
>
> **Détail et histoire** : l'ancien plan [A/B](../theorie/glossaire/entrees/a-b.md) est archivé dans
> [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
> [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
> dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
> [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).

## Comment lire cette roadmap

- **Les états** : ✅ mesuré et écrit · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
- **Le carpe diem** : pas d'échéance. Un chantier est **[fait](../theorie/glossaire/entrees
… [23688 caractères tronqués]
  ```

- **bash** `{"command": "ls journal/2026-11-16/; sed -n '1,120p' journal/2026-11-16/README.md", "description": "Read day journal"}`

  ```
docs.md
memoire.md
mesures.md
README.md
# 2026-11-16

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-16/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**5 commits** · **1 session(s)** · **3 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 1 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 3 | [mesures.md](mesures.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 369.5 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (D
… [1749 caractères tronqués]
  ```

- **bash** `{"command": "git status --short journal/2026-11-16 docs/pilotage/roadmap.md docs/pilotage/en-cours.md", "description": "Status of journal/state"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json --duree | jq '{duree_s: .cout.duree_s, octets: .cout.octets}'; python3 tools/drave.py analyser \"Le chat dort.\" --json | jq '.cout'", "description": "Measure duration field"}`

  ```
{
  "duree_s": 0.004758,
  "octets": 13
}
{
  "octets": 13,
  "caracteres": 13,
  "etiquettes": 20
}
  ```

### 🤖 Assistant

I'll start by building the verification harness around the current code, then update the docs to match it exactly.

- **bash** `{"command": "python3 - <<'PY'\nimport re, pathlib\np = pathlib.Path('docs/produit/exemples.md')\nt = p.read_text()\n# section headings and fenced block positions\nfor m in re.finditer(r'^(#{2,3}) (.+)$', t, re.M):\n    print(m.start(), m.group(0))\nPY", "description": "List section offsets"}`

  ```
2414 ## 0. Comment lire les JSON
5735 ## 1. Une déclarative simple — `g001`
9360 ## 2. Un attachement de REL — `g011`
13275 ## 3. L'anglais et le marqueur ambigu — `r241`
17280 ## 4. Le refus — texte vide
18784 ## 5. L'échec autrefois connu — `r035`, désormais prédit
22478 ## 6. Le tagger en option — trois exécutions avec la clé
23128 ### 6.1 `g001` — le cas neutre
24472 ### 6.2 `g011` — `lu` redevient un verbe
27646 ### 6.3 `r241` — `when` redevient un pronom
29241 ### 6.4 Ce que les trois exemples mesurent — et ne mesurent pas
30529 ## 7. La base honnête — deux exécutions avec `--reel`
30829 ### 7.1 `evaluer --reel` — la sortie lisible
32747 ### 7.2 `evaluer --reel --json` — le contrat de la mesure
34456 ## 8. Ce que ces exemples ne montrent pas
36159 ## 9. Où aller ensuite
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "> **Ce que ce document est.** Dix exécutions **réelles** du produit, avec leur JSON commenté. Il\n> complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit\n> *comment lire* ce qui sort. Les **cinq premiers bl … [4612 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "- `confiance` : **déclarée**, pas calibrée. 0,3 pour un NOUN ouvert, 0,92 pour un DET. Avec\n  `--tagger`, les POS neuronaux portent **0,60** : c'est le **seuil de la cascade**, pas une\n  probabilité par token ; ils ont `source: \"neuronal\"` … [1511 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "  syntagmes: [.etiquettes[] | select(.niveau==\"syntagme\")\n        | {valeur, type, debut, fin, confiance, role:.meta.role,\n           cible:.meta.attachement.cible, union:.meta.union,\n           partition:.meta.partition, alternative:.met … [375 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "Puis : `python3 tools/drave.py analyser \"…\" --json | jq \"$FILTRE\"`.", "new_string": "Puis : `python3 tools/drave.py analyser \"…\" --json | jq \"$FILTRE\"`.\n\n`candidats` est la liste **historique** de chaînes ; `candidats_objets` est la  … [265 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"union:.meta.union, candidats\" docs/produit/exemples.md", "description": "Count filter occurrences"}`

  ```
143:              cible:.meta.attachement.cible, union:.meta.union, candidats}],
258:              cible:.meta.attachement.cible, union:.meta.union, candidats}],
387:              cible:.meta.attachement.cible, union:.meta.union, candidats}]}'
609:              cible:.meta.attachement.cible, union:.meta.union, candidats}],
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "              cible:.meta.attachement.cible, union:.meta.union, candidats}],", "new_string": "              cible:.meta.attachement.cible, union:.meta.union, candidats,\n              candidats_objets:.meta.attachement.candidats}],", "replace_ … [11 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated. All occurrences were successfully replaced.
  ```

- **bash** `{"command": "sed -n '378,392p' docs/produit/exemples.md; grep -n \"union:.meta.union, candidats\" docs/produit/exemples.md", "description": "Check §3 filter"}`

  ```
**Entrée.** `The day when we left was beautiful.` (phrase `reel` du gold, `r241`).

**Commande.**

```bash
python3 tools/drave.py analyser "The day when we left was beautiful." --langue en --json \
  | jq '{langue, script, refus,
         pos: [.etiquettes[] | select(.niveau=="pos")
           | {valeur, type, debut, fin, confiance, ouvert:.meta.ouvert}],
         syntagmes: [.etiquettes[] | select(.niveau=="syntagme")
           | {valeur, type, debut, fin, confiance, role:.meta.role,
              cible:.meta.attachement.cible, union:.meta.union, candidats}]}'
```

**Sortie (réelle).**
143:              cible:.meta.attachement.cible, union:.meta.union, candidats,
259:              cible:.meta.attachement.cible, union:.meta.union, candidats,
389:              cible:.meta.attachement.cible, union:.meta.union, candidats}]}'
611:              cible:.meta.attachement.cible, union:.meta.union, candidats,
  ```

- **bash** `{"command": "sed -n '138,148p' docs/produit/exemples.md; sed -n '384,392p' docs/produit/exemples.md", "description": "Verify filter edits"}`

  ```
| jq '{langue, script, refus,
         pos: [.etiquettes[] | select(.niveau=="pos")
           | {valeur, type, debut, fin, confiance, ouvert:.meta.ouvert}],
         syntagmes: [.etiquettes[] | select(.niveau=="syntagme")
           | {valeur, type, debut, fin, confiance, role:.meta.role,
              cible:.meta.attachement.cible, union:.meta.union, candidats,
              candidats_objets:.meta.attachement.candidats}],
         phrase: [.etiquettes[] | select(.niveau=="phrase") | {type, valeur}],
         pragmatique: [.etiquettes[] | select(.niveau=="pragmatique") | {type, valeur}]}'
```

  | jq '{langue, script, refus,
         pos: [.etiquettes[] | select(.niveau=="pos")
           | {valeur, type, debut, fin, confiance, ouvert:.meta.ouvert}],
         syntagmes: [.etiquettes[] | select(.niveau=="syntagme")
           | {valeur, type, debut, fin, confiance, role:.meta.role,
              cible:.meta.attachement.cible, union:.meta.union, candidats}]}'
```

**Sortie (réelle).**
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "              cible:.meta.attachement.cible, union:.meta.union, candidats}]}'", "new_string": "              cible:.meta.attachement.cible, union:.meta.union, candidats,\n              candidats_objets:.meta.attachement.candidats}]}'"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '195,235p' docs/produit/exemples.md", "description": "Locate §1 output end"}`

  ```
"fin": 7,
      "confiance": 0.55,
      "role": "agent",
      "cible": "dort",
      "union": null,
      "candidats": [
        "structure la plus proche",
        "dort"
      ]
    },
    {
      "valeur": "dort",
      "type": "GV",
      "debut": 8,
      "fin": 12,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "chat",
      "union": null,
      "candidats": [
        "structure la plus proche"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type",
      "valeur": "déclarative"
    }
  ],
  "pragmatique": [
    {
      "type": "acte",
      "valeur": "assertion"
    }
  ]
}
```

**Lecture.**
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "  \"pragmatique\": [\n    {\n      \"type\": \"acte\",\n      \"valeur\": \"assertion\"\n    }\n  ]\n}\n```\n\n**Lecture.**\n\n- `langue: fr`, `script: Latn`, `refus: \"\"` : le texte est accepté.", "new_string": "  \"pragmatique\": [\n    {\n … [629 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "- Deux syntagmes : `GN « Le chat » [0:7] → dort` et `GV « dort » [8:12] → chat`. Le gold `g001`\n  attend exactement ces deux spans et `assertion` ; c'est le cas de base réussi.\n- L'extrait omet `fraction_semantique`, `unites_semantiques`, `t … [905 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '370,410p' docs/produit/exemples.md", "description": "Read §2 lecture"}`

  ```
}
  ]
}
```

**Lecture.**

- `REL « que j'ai lu » [9:20] → livre` : c'est l'attachement attendu par le gold
  (`cible: livre`). C'est le cas `g011` réussi.
- `REL « que j'ai lu est intéressant » [9:36] → livre` avec **`union: true`** : c'est la **seconde
  lecture d'union**, un **doublon REL** qui chevauche la première. La sortie lisible du CLI ne
  montre pas `union` : elle affiche deux REL, et il faut **ignorer la plus longue** pour une
  lecture unique (ou filtrer les segments qui en contiennent un autre). Ce n'est pas une erreur
  d'attachement : c'est une hypothèse concurrente publiée telle quelle.
- En **v2**, le JSON complet porte en plus `meta.partition` sur les trois segments du groupe 0
  (`membres: 3` ; rang 1 = REL longue, rang 2 = GV, rang 3 = REL courte) et `meta.alternative`
  avec les deux autres. Le filtre ci-dessus ne les sélectionne pas ; pour les voir, ajouter
  `partition:.meta.partition, alternative:.meta.alternative` (voir le `FILTRE` du § 0).
- `GN « Le livre » → intéressant` : le GN est rattaché au GV, pas à la REL. Le gold annote ce GN
  `patient`, le bloc `agent` : **les rôles ne sont pas mesurés** par le banc ; seul
  l'attachement l'est. Ne pas lire `ro
… [1027 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "- En **v2**, le JSON complet porte en plus `meta.partition` sur les trois segments du groupe 0\n  (`membres: 3` ; rang 1 = REL longue, rang 2 = GV, rang 3 = REL courte) et `meta.alternative`\n  avec les deux autres. Le filtre ci-dessus ne les  … [2344 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" --json | jq '[.etiquettes[] | select(.niveau==\"syntagme\") | {valeur, c:.meta.attachement.candidats}]'", "description": "Check g011 candidate spans"}`

  ```
[
  {
    "valeur": "Le livre",
    "c": [
      {
        "span": {
          "debut": 25,
          "fin": 36
        },
        "cible": "intéressant",
        "source": "heuristique"
      },
      {
        "span": {
          "debut": 0,
          "fin": 8
        },
        "cible": "Le livre",
        "source": "heuristique"
      },
      {
        "span": {
          "debut": 3,
          "fin": 8
        },
        "cible": "livre",
        "source": "heuristique"
      }
    ]
  },
  {
    "valeur": "que j'ai lu",
    "c": [
      {
        "span": {
          "debut": 3,
          "fin": 8
        },
        "cible": "livre",
        "source": "heuristique"
      },
      {
        "span": {
          "debut": 0,
          "fin": 8
        },
        "cible": "Le livre",
        "source": "heuristique"
      },
      {
        "span": {
          "debut": 25,
          "fin": 36
        },
        "cible": "intéressant",
        "source": "heuristique"
      }
    ]
  },
  {
    "valeur": "que j'ai lu est intéressant",
    "c": [
      {
        "span": {
          "debut": 3,
          "fin": 8
        },
        "cible": "livre",
        "source": "heuristique"
     
… [518 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "- Les deux REL portent `role: qualite` : la forme accentuée `qualité` est **normalisée**, comme\n  `prédicat` en `predicat`. Les `candidats_objets` publient `livre[10:15]` et `intéressant[21:32]`\n  avec leur source, sans changer l'attachement … [263 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '490,540p' docs/produit/exemples.md", "description": "Read §3 lecture"}`

  ```
}
  ],
  "syntagmes": [
    {
      "valeur": "The day",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confiance": 0.35,
      "role": "groupe nominal",
      "cible": "beautiful",
      "union": null,
      "candidats": [
        "GN",
        "beautiful"
      ]
    },
    {
      "valeur": "when we left",
      "type": "REL",
      "debut": 8,
      "fin": 20,
      "confiance": 0.35,
      "role": "qualité",
      "cible": "day",
      "union": null,
      "candidats": [
        "REL",
        "day",
        "beautiful"
      ]
    },
    {
      "valeur": "was beautiful",
      "type": "GV",
      "debut": 21,
      "fin": 34,
      "confiance": 0.35,
      "role": "prédicat",
      "cible": null,
      "union": null,
      "candidats": [
        "GV"
      ]
    }
  ]
}
```

**Lecture.**
  ```

- **bash** `{"command": "sed -n '540,580p' docs/produit/exemples.md", "description": "Read §3 lecture bullets"}`

  ```
- `when` est tagué **CONJ** par le POS, mais il déclenche une **REL** `[8:20] « when we left »`
  → `day` : c'est la correction `AMBIGUES_REL` de la v12 (« when » après un GN = relative ;
  ailleurs, subordonnée). Sans elle, la REL était une SUB et le span était perdu.
- `left` est désormais **VERB** (0,85) et `was` **AUX** ; le POS anglais n'est pas parfait pour
  autant (POS global **0,8625**, ouvert **0,7918**). L'attachement juste et le POS imparfait
  continuent de coexister dans la même sortie.
- `beautiful` est **ADJ**, `The day` **GN**, `was beautiful` **GV** : la segmentation est
  complète. La ponctuation finale sort en **PONCT** depuis le correctif de ponctuation.
- L'attachement `REL → day` est celui du gold ; c'est le **87/87 labels** anglais (88 cibles ;
  `g017` est la seule cible sans span prédit).
- `GV « was beautiful »` a `cible: null` : le bloc ne publie pas d'attachement pour ce GV. `null`
  veut dire « pas de cible publiée », pas « pas de relation ».

**Ce qu'il faut en conclure.** Le produit n'est pas monolingue : il analyse l'anglais et publie
les mêmes champs. Mais une réussite d'attachement peut coexister avec des erreurs de POS ; les
deux mesures sont sép
… [763 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "- `beautiful` est **ADJ**, `The day` **GN**, `was beautiful` **GV** : la segmentation est\n  complète. La ponctuation finale sort en **PONCT** depuis le correctif de ponctuation.\n- L'attachement `REL → day` est celui du gold ; c'est le **87/8 … [609 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '690,740p' docs/produit/exemples.md", "description": "Read §5 lecture"}`

  ```
"role": "prédicat",
      "cible": null,
      "union": null,
      "candidats": [
        "GV"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type",
      "valeur": "déclarative"
    }
  ],
  "pragmatique": [
    {
      "type": "acte",
      "valeur": "assertion"
    }
  ]
}
```

**Lecture.**

- Le bloc prédit exactement les trois spans du gold : `GN « The film » [0:8]`, `REL « she talks
  about » [9:24] → film` et `GV « is out » [25:31]`. **La REL est là**, avec la cible attendue.
- La relative est **sans marqueur** (« the film **she talks about** » : le pronom relatif est
  absent). La règle **relative zéro** (`relative_zero`, J1.1) la retrouve : GN antécédent, pronom
  sujet, verbe, préposition orpheline. C'était l'un des « 17 spans inatteignables » de la v12 ;
  ce n'est plus le cas.
- L'exactitude d'attachement est **238/238 labels = 1,0000**, mais elle reste **conditionnelle
  aux spans prédits** ; la couverture est **238/239 = 0,9958**. Les deux chiffres doivent être lus
  ensemble.
- Le seul span du gold encore manquant qui porte une cible est `g017` : `SUB [9:28] « that she
  would come »`, que le bloc étend à `[9:38]` en absorbant `yesterday`. C'est l'échec coura
… [1004 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"The film she talks about is out.\" --json | jq '[.etiquettes[] | select(.niveau==\"syntagme\") | {valeur, c:.meta.attachement.candidats}]'", "description": "Check r035 candidate spans"}`

  ```
[
  {
    "valeur": "The film",
    "c": [
      {
        "span": {
          "debut": 21,
          "fin": 24
        },
        "cible": "out",
        "source": "heuristique"
      }
    ]
  },
  {
    "valeur": "she talks about",
    "c": [
      {
        "span": {
          "debut": 4,
          "fin": 8
        },
        "cible": "film",
        "source": "heuristique"
      },
      {
        "span": {
          "debut": 21,
          "fin": 24
        },
        "cible": "out",
        "source": "heuristique"
      }
    ]
  },
  {
    "valeur": "is out",
    "c": null
  }
]
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "- Le bloc prédit exactement les trois spans du gold : `GN « The film » [0:8]`, `REL « she talks\n  about » [9:24] → film` et `GV « is out » [25:31]`. **La REL est là**, avec la cible attendue.\n- La relative est **sans marqueur** (« the film * … [629 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"rôle=qualité\\|rôle=prédicat\\|rôle=groupe nominal\\|rôle=qualite\\|rôle=predicat\\|rôle=objet\\|rôle=agent\" docs/produit/exemples.md", "description": "Find readable role lines"}`

  ```
126:  GN   [0:7]   Le chat  rôle=agent     → dort
127:  GV   [8:12]  dort     rôle=predicat  → chat
766:  GN   [0:7]   Le chat  rôle=agent     → dort
767:  GV   [8:12]  dort     rôle=predicat  → chat
799:  GN   [0:8]    Le livre                     rôle=agent     → intéressant
800:  REL  [9:20]   que j'ai lu                  rôle=qualite   → livre
801:  REL  [9:36]   que j'ai lu est intéressant  rôle=qualité   → livre
802:  GV   [21:36]  est intéressant              rôle=predicat  → livre
890:  GN   [0:7]    The day        rôle=groupe nominal  → beautiful
891:  REL  [8:20]   when we left   rôle=qualité         → day
892:  GV   [21:34]  was beautiful  rôle=prédicat        → —
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "  REL  [9:36]   que j'ai lu est intéressant  rôle=qualité   → livre", "new_string": "  REL  [9:36]   que j'ai lu est intéressant  rôle=qualite   → livre"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "  GN   [0:7]    The day        rôle=groupe nominal  → beautiful\n  REL  [8:20]   when we left   rôle=qualité         → day\n  GV   [21:34]  was beautiful  rôle=prédicat        → —", "new_string": "  GN   [0:7]    The day        rôle=objet      … [135 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '990,1035p' docs/produit/exemples.md", "description": "Read §8"}`

  ```
```json
{
  "version": "0.1.0",
  "gold": {
    "nom": "réel (hand + reel, sans synthétique)",
    "gele": false,
    "phrases": 452,
    "tokens": 2480,
    "cibles_attachement": 184
  },
  "reel": null,
  "pos": {
    "exactitude": 0.8891,
    "exactitude_ferme": 0.9294,
    "exactitude_ouvert": 0.8466,
    "tokens": 2480
  },
  "f1": {
    "f1": 0.7906,
    "precision": 0.8128,
    "rappel": 0.7695
  },
  "attachement": {
    "cibles": 184,
    "labels": 183,
    "exact": 183,
    "exact_taux": 0.9946,
    "couverture": 0.9946
  },
  "controle_negatif": {
    "nom": "cible exacte tirée au hasard dans le gold",
    "graine": 0,
    "cibles": 184,
    "exact_taux": 0.0
  }
}
```

**Lecture.** `gold.nom` **nomme la base** mesurée, `gold.phrases: 452` et
`gold.cibles_attachement: 184` la bornent. `reel: null` est **attendu** : la base mesurée est
déjà la base réelle ; sans `--reel`, ce champ porte un objet (452 phrases, POS, F1,
attachement) calculé à côté du global. Les nombres sont **les mêmes** que dans la sortie
lisible : 0,8891, 0,7906, 0,9946. Attention : ce JSON est un **rapport d'évaluation**
(`version: "0.1.0"` est celle du CLI), pas une **annotation** : le schéma `drave.an
… [35 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1040,1085p' docs/produit/exemples.md", "description": "Read §8 bullets"}`

  ```
2. **Pas de neuronal local** : le défaut reste `Heuristique` (CPU, hors ligne) ; `MockNeuronal`
   est un contrat, pas un tagger. Le CLI expose en **option** le tagger POS de l'**API DeepSeek**
   (`--tagger`, § 6), pas un modèle local : la cascade 7B locale (0,9415) n'est pas un chemin
   livré.
3. **Pas de couverture complète** : sur les **239 cibles d'attachement** du gold vivant, **238**
   ont un span prédit (**0,9958**) ; la seule qui manque est `g017` (`SUB [9:28]`). Sur la base
   réelle 452, **183/184** cibles ont un span (0,9946). `r035`, autrefois manqué, est désormais
   prédit (§ 5).
4. **Pas de lecture unique garantie** : le **doublon REL de l'union** (`union: true`) est publié ;
   il faut le filtrer si l'on veut un seul segment par span.
5. **Pas de valeurs normalisées** : `candidats` sont des chaînes et `role` n'est pas normalisé
   (`predicat`/`prédicat`). Le **format** est versionné (v2 ; v1 reste lue), mais le vocabulaire
   des valeurs, lui, n'a pas de schéma. Avec `--tagger`, `confiance` vaut **0,60** (le seuil de
   la cascade), `source` vaut `neuronal` et `meta.ouvert` est **absent** : ne pas lire ces champs
   comme une probabilité.

Pour mesurer sur votre 
… [1719 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "5. **Pas de valeurs normalisées** : `candidats` sont des chaînes et `role` n'est pas normalisé\n   (`predicat`/`prédicat`). Le **format** est versionné (v2 ; v1 reste lue), mais le vocabulaire\n   des valeurs, lui, n'a pas de schéma. Avec `--t … [838 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "| **le contrat du bloc** | [`docs/implantation/bloc-linguistique.md`](../implantation/bloc-linguistique.md) |\n| **le rejeu des cinq blocs du 14/11** | [`reports/rapport-exemples-rejoues.md`](../../reports/rapport-exemples-rejoues.md) |", "new … [408 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re, subprocess, pathlib, json, shutil\np = pathlib.Path('docs/produit/exemples.md')\nt = p.read_text()\nshutil.copy(p, '/tmp/exemples.before.json')\n# section boundaries\nheads = [(m.start(), m.group(0)) for m in re.finditer(r'^## .+$', t, re.M)]\nsections = []\ … [2469 caractères tronqués]`

  ```
remplacements: 5
## 1. Une déclarative simple — `g001` main
## 1. Une déclarative simple — `g001` duree
## 2. Un attachement de REL — `g011` main
## 3. L'anglais et le marqueur ambigu — `r241` main
## 5. L'échec autrefois connu — `r035`, désormais prédit main
  ```

- **bash** `{"command": "sed -n '160,300p' docs/produit/exemples.md", "description": "Inspect §1 updated output"}`

  ```
"debut": 0,
      "fin": 2,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "chat",
      "type": "NOUN",
      "debut": 3,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "dort",
      "type": "VERB",
      "debut": 8,
      "fin": 12,
      "confiance": 0.72,
      "ouvert": true
    },
    {
      "valeur": ".",
      "type": "PONCT",
      "debut": 12,
      "fin": 13,
      "confiance": 0.95,
      "ouvert": false
    }
  ],
  "syntagmes": [
    {
      "valeur": "Le chat",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confiance": 0.55,
      "role": "agent",
      "cible": "dort",
      "union": null,
      "candidats": [
        "structure la plus proche",
        "dort"
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 8,
            "fin": 12
          },
          "cible": "dort",
          "source": "heuristique"
        }
      ]
    },
    {
      "valeur": "dort",
      "type": "GV",
      "debut": 8,
      "fin": 12,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "chat",
      "union": null,
      "candidats": [
        "struct
… [2400 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '300,380p' docs/produit/exemples.md; sed -n '470,540p' docs/produit/exemples.md", "description": "Inspect §2 and §3 blocks"}`

  ```
syntagmes: [.etiquettes[] | select(.niveau=="syntagme")
           | {valeur, type, debut, fin, confiance, role:.meta.role,
              cible:.meta.attachement.cible, union:.meta.union, candidats,
              candidats_objets:.meta.attachement.candidats}],
         phrase: [.etiquettes[] | select(.niveau=="phrase") | {type, valeur}],
         pragmatique: [.etiquettes[] | select(.niveau=="pragmatique") | {type, valeur}]}'
```

**Sortie (réelle).**

```json
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "syntagmes": [
    {
      "valeur": "Le livre",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.55,
      "role": "agent",
      "cible": "intéressant",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 25,
            "fin": 36
          },
          "cible": "intéressant",
          "source": "heuristique"
        },
        {
          "span": {
            "debut": 0,
            "fin": 8
          },
          "cible": "Le livre",
          "source": "heuristique"
        },
        
… [3700 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '790,820p' docs/produit/exemples.md; sed -n '880,905p' docs/produit/exemples.md", "description": "Inspect §6 readable outputs"}`

  ```
"refus": "",
  "syntagmes": [
    {
      "valeur": "The film",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.35,
      "role": "objet",
      "cible": "out",
      "union": null,
      "candidats": [
        "GN",
        "out"
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 21,
            "fin": 24
          },
          "cible": "out",
          "source": "heuristique"
        }
      ]
    },
    {
      "valeur": "she talks about",
      "type": "REL",
      "debut": 9,
      "fin": 24,

- Le bloc prédit exactement les trois spans du gold : `GN « The film » [0:8]`, `REL « she talks
  about » [9:24] → film` et `GV « is out » [25:31]`. **La REL est là**, avec la cible attendue.
- Rôles **normalisés** : `The film` est `objet` (brut `groupe nominal`), `she talks about`
  `qualite` (brut `qualité`), `is out` `predicat`. Les candidats objets publient `out[21:24]`
  pour le GN et `film[4:8]`, `out[21:24]` pour la REL ; le GV n'en publie aucun (`null`).
- La relative est **sans marqueur** (« the film **she talks about** » : le pronom relatif est
  absent). La règle **relative zéro** (`relative_zero`, J1.1) la retrou
… [1255 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"rôle=\" docs/produit/exemples.md", "description": "All readable role lines after edits"}`

  ```
126:  GN   [0:7]   Le chat  rôle=agent     → dort
127:  GV   [8:12]  dort     rôle=predicat  → chat
932:  GN   [0:7]   Le chat  rôle=agent     → dort
933:  GV   [8:12]  dort     rôle=predicat  → chat
965:  GN   [0:8]    Le livre                     rôle=agent     → intéressant
966:  REL  [9:20]   que j'ai lu                  rôle=qualite   → livre
967:  REL  [9:36]   que j'ai lu est intéressant  rôle=qualite   → livre
968:  GV   [21:36]  est intéressant              rôle=predicat  → livre
1056:  GN   [0:7]    The day        rôle=objet           → beautiful
1057:  REL  [8:20]   when we left   rôle=qualite         → day
1058:  GV   [21:34]  was beautiful  rôle=predicat        → —
  ```

- **write** `{"file_path": "tools/verifie_exemples.py", "content": "#!/usr/bin/env python3\n\"\"\"verifie_exemples.py — le contrôle négatif des exemples de la doc produit.\n\nCe script rejoue les sorties publiées dans `docs/produit/exemples.md` et\n`docs/produit/demarrage.md` avec le code courant, puis compare : … [21380 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py", "description": "Run examples verifier", "timeoutMs": 300000}`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 496, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 439, in main
    cas = cas_exemples(texte_exemples)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 172, in cas_exemples
    bloc_lang(s, "text").corps, "texte"))
    ~~~~~~~~~^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 102, in bloc_lang
    raise LookupError(f"bloc {lang!r} #{rang} introuvable dans {s.titre!r}")
LookupError: bloc 'text' #0 introuvable dans '## 1. Une déclarative simple — `g001`'
[exit code: 1]
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "        blocs = [\n            Bloc(m.group(1), m.start(), m.end(), m.group(2))\n            for m in re.finditer(r\"^```(\\w*)\\n(.*?)\\n```$\", texte[debut:fin], re.M | re.S)\n        ]", "new_string": "        blocs = [\n            Bloc(m … [164 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py", "description": "Run examples verifier again", "timeoutMs": 300000}`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 496, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 439, in main
    cas = cas_exemples(texte_exemples)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 220, in cas_exemples
    sec = section(sections, prefixe)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 82, in section
    raise LookupError(f"section introuvable : {prefixe!r}")
LookupError: section introuvable : '### 6.1'
[exit code: 1]
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "    tetes = [(m.start(), m.group(0)) for m in re.finditer(r\"^## .+$\", texte, re.M)]", "new_string": "    tetes = [(m.start(), m.group(0)) for m in re.finditer(r\"^#{2,3} .+$\", texte, re.M)]"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py", "description": "Run examples verifier third time", "timeoutMs": 300000}`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 496, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 439, in main
    cas = cas_exemples(texte_exemples)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 234, in cas_exemples
    cmd = bloc_bash(s, "evaluer --reel --json")
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 89, in bloc_bash
    raise LookupError(f"commande {contient!r} introuvable dans {s.titre!r}")
LookupError: commande 'evaluer --reel --json' introuvable dans '### 7.1 `evaluer --reel` — la sortie lisible'
[exit code: 1]
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "    # § 7.2 — le JSON de --reel\n    cmd = bloc_bash(s, \"evaluer --reel --json\")\n    cas.append(Cas(\"exemples §7.2 --reel JSON\", \"exemples.md\", cmd.corps,\n                   bloc_apres(s, cmd, \"json\").corps, \"json\"))", "new_string … [274 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py", "description": "Run examples verifier fourth time", "timeoutMs": 300000}`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 497, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 448, in main
    cas_dem, note = cas_demarrage(texte_demarrage, cwd)
                    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 295, in cas_demarrage
    attendu = bloc_lang(s, "text", 1).corps
              ~~~~~~~~~^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 102, in bloc_lang
    raise LookupError(f"bloc {lang!r} #{rang} introuvable dans {s.titre!r}")
LookupError: bloc 'text' #1 introuvable dans '### 3.4 Le JSON — la même analyse, en machine'
[exit code: 1]
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "    cmd = bloc_bash(s, \"python3 -c\")\n    attendu = bloc_lang(s, \"text\", 1).corps", "new_string": "    cmd = bloc_bash(s, \"python3 -c\")\n    attendu = bloc_lang(s, \"text\").corps"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py", "description": "Run examples verifier fifth time", "timeoutMs": 300000}`

  ```
✅ exemples §1 lisible — 10 ligne(s)
  ✅ exemples §1 JSON — JSON exact
  ✅ exemples §1 durée — duree_s=0.004704 (variable), octets exacts
  ✅ exemples §2 JSON — JSON exact
  ✅ exemples §3 JSON — JSON exact
  ✅ exemples §4 refus CLI — code 3, stderr exact
  ✅ exemples §4 refus API — JSON exact
  ✅ exemples §5 JSON — JSON exact
  ✅ exemples §6.1 syntagmes — 2 ligne(s) de syntagmes
  ✅ exemples §6.2 syntagmes — 4 ligne(s) de syntagmes
  ❌ exemples §6.3 syntagmes — conforme
      SYNTAGMES:
attendu:
GN   [0:7]    The day        rôle=objet           → beautiful
  REL  [8:20]   when we left   rôle=qualite         → day
  GV   [21:34]  was beautiful  rôle=predicat        → —
obtenu:
GN   [0:7]    The day        rôle=objet     → beautiful
  REL  [8:20]   when we left   rôle=qualite   → day
  GV   [21:34]  was beautiful  rôle=predicat  → —
  ✅ exemples §7.1 --reel — 13 ligne(s)
  ✅ exemples §7.2 --reel JSON — JSON exact
  ✅ demarrage §3.1 --version — 1 ligne(s)
  ✅ demarrage §3.2 analyser — 10 ligne(s)
  ✅ demarrage §3.3 evaluer — 13 ligne(s)
  ✅ demarrage §3.4 JSON — 22 lignes
  ✅ demarrage §3.4 consommateur — 2 ligne(s)
  ❌ demarrage §3.5 profils — conforme
      code 127: /bin/bash: line 
… [548 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"The day when we left was beautiful.\" --langue en | sed -n '/SYNTAGMES/,/PRAGMATIQUE/p'; python3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" | sed -n '/SYNTAGMES/,/PRAGMATIQUE/p'", "description": "Check readable syntagme alignment" … [1 caractères tronqués]`

  ```
SYNTAGMES
  GN   [0:7]    The day        rôle=objet     → beautiful
  REL  [8:20]   when we left   rôle=qualite   → day
  GV   [21:34]  was beautiful  rôle=predicat  → —
PRAGMATIQUE
SYNTAGMES
  GN   [0:8]    Le livre                     rôle=agent     → intéressant
  REL  [9:20]   que j'ai lu                  rôle=qualite   → livre
  REL  [9:36]   que j'ai lu est intéressant  rôle=qualite   → livre
  GV   [21:36]  est intéressant              rôle=predicat  → livre
PRAGMATIQUE
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "  GN   [0:7]    The day        rôle=objet           → beautiful\n  REL  [8:20]   when we left   rôle=qualite         → day\n  GV   [21:34]  was beautiful  rôle=predicat        → —", "new_string": "  GN   [0:7]    The day        rôle=objet      … [117 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md": file changed since it was read — re-read the file, then retry
  ```

- **bash** `{"command": "sed -n '1052,1060p' docs/produit/exemples.md", "description": "Re-read §6.3 lines"}`

  ```
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=en script=Latn source=cascade · 38 étiquettes · unités sémantiques=3 (45.7% du texte)
POS  The/DET day/NOUN when/PRON we/PRON left/VERB was/AUX beautiful/ADJ ./PONCT
SYNTAGMES
  GN   [0:7]    The day        rôle=objet           → beautiful
  REL  [8:20]   when we left   rôle=qualite         → day
  GV   [21:34]  was beautiful  rôle=predicat        → —
PRAGMATIQUE
  phrase [0:35] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
  ```

- **read** `{"file_path": "docs/produit/exemples.md", "offset": 1054, "limit": 8}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md</path>
<type>file</type>
<content>
1054: POS  The/DET day/NOUN when/PRON we/PRON left/VERB was/AUX beautiful/ADJ ./PONCT
1055: SYNTAGMES
1056:   GN   [0:7]    The day        rôle=objet           → beautiful
1057:   REL  [8:20]   when we left   rôle=qualite         → day
1058:   GV   [21:34]  was beautiful  rôle=predicat        → —
1059: PRAGMATIQUE
1060:   phrase [0:35] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
1061: COUVERTURE  (confiance max par niveau)  graphème=0.99 · morphème=0.32 · mot=0.98 · pos=0.95 ·

(Showing lines 1054-1061 of 1243. Use offset=1062 to continue.)
</content>
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "  GN   [0:7]    The day        rôle=objet           → beautiful\n  REL  [8:20]   when we left   rôle=qualite         → day\n  GV   [21:34]  was beautiful  rôle=predicat        → —", "new_string": "  GN   [0:7]    The day        rôle=objet      … [117 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "    cmd = bloc_bash(s, \"profils --texte\")\n    attendu = bloc_lang(s, \"text\").corps\n    commande = cmd.corps.replace(\"drave \", \"python3 tools/drave.py \", 1)", "new_string": "    cmd = bloc_bash(s, \"profils --texte\")\n    attendu =  … [219 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "        ok = proc.returncode == 0 and note[cle] in proc.stdout\n        resultats.append({\"id\": f\"note dev {cle}\", \"ok\": ok,\n                          \"detail\": note[cle] if ok else f\"absent de: {proc.stdout[:200]}\"})\n    proc = e … [942 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py", "description": "Run verifier after fixes", "timeoutMs": 300000}`

  ```
✅ exemples §1 lisible — 10 ligne(s)
  ✅ exemples §1 JSON — JSON exact
  ✅ exemples §1 durée — duree_s=0.004057 (variable), octets exacts
  ✅ exemples §2 JSON — JSON exact
  ✅ exemples §3 JSON — JSON exact
  ✅ exemples §4 refus CLI — code 3, stderr exact
  ✅ exemples §4 refus API — JSON exact
  ✅ exemples §5 JSON — JSON exact
  ✅ exemples §6.1 syntagmes — 2 ligne(s) de syntagmes
  ✅ exemples §6.2 syntagmes — 4 ligne(s) de syntagmes
  ✅ exemples §6.3 syntagmes — 3 ligne(s) de syntagmes
  ✅ exemples §7.1 --reel — 13 ligne(s)
  ✅ exemples §7.2 --reel JSON — JSON exact
  ✅ demarrage §3.1 --version — 1 ligne(s)
  ✅ demarrage §3.2 analyser — 10 ligne(s)
  ✅ demarrage §3.3 evaluer — 13 ligne(s)
  ✅ demarrage §3.4 JSON — 22 lignes
  ✅ demarrage §3.4 consommateur — 2 ligne(s)
  ✅ demarrage §3.5 profils — 9 ligne(s)
  ✅ note dev analyser — rôle=agent
  ✅ note dev cible — → chat
  ✅ note dev f1 — F1 79.02 %
  ❌ note dev attachement — absent de: drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ou

22/23 cas conformes — ❌ 1 écart(s)
[exit code: 1]
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "        \"attachement\": \"attachement exact 99.58 %\",", "new_string": "        \"attachement\": \"ATTACHEMENT exact 99.58 %\","}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py", "description": "Run verifier final", "timeoutMs": 300000}`

  ```
✅ exemples §1 lisible — 10 ligne(s)
  ✅ exemples §1 JSON — JSON exact
  ✅ exemples §1 durée — duree_s=0.004332 (variable), octets exacts
  ✅ exemples §2 JSON — JSON exact
  ✅ exemples §3 JSON — JSON exact
  ✅ exemples §4 refus CLI — code 3, stderr exact
  ✅ exemples §4 refus API — JSON exact
  ✅ exemples §5 JSON — JSON exact
  ✅ exemples §6.1 syntagmes — 2 ligne(s) de syntagmes
  ✅ exemples §6.2 syntagmes — 4 ligne(s) de syntagmes
  ✅ exemples §6.3 syntagmes — 3 ligne(s) de syntagmes
  ✅ exemples §7.1 --reel — 13 ligne(s)
  ✅ exemples §7.2 --reel JSON — JSON exact
  ✅ demarrage §3.1 --version — 1 ligne(s)
  ✅ demarrage §3.2 analyser — 10 ligne(s)
  ✅ demarrage §3.3 evaluer — 13 ligne(s)
  ✅ demarrage §3.4 JSON — 22 lignes
  ✅ demarrage §3.4 consommateur — 2 ligne(s)
  ✅ demarrage §3.5 profils — 9 ligne(s)
  ✅ note dev analyser — rôle=agent
  ✅ note dev cible — → chat
  ✅ note dev f1 — F1 79.02 %
  ✅ note dev attachement — ATTACHEMENT exact 99.58 %

23/23 cas conformes — ✅ aucun écart
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py --mutation; echo \"exit=$?\"", "description": "Run negative control mutation", "timeoutMs": 300000}`

  ```
✅ exemples §1 lisible — 10 ligne(s)
  ✅ exemples §1 JSON — JSON exact
  ✅ exemples §1 durée — duree_s=0.004324 (variable), octets exacts
  ❌ exemples §2 JSON — JSON exact
      .syntagmes[1].role: 'qualité' attendu, 'qualite' reçu
  ✅ exemples §3 JSON — JSON exact
  ✅ exemples §4 refus CLI — code 3, stderr exact
  ✅ exemples §4 refus API — JSON exact
  ✅ exemples §5 JSON — JSON exact
  ✅ exemples §6.1 syntagmes — 2 ligne(s) de syntagmes
  ✅ exemples §6.2 syntagmes — 4 ligne(s) de syntagmes
  ✅ exemples §6.3 syntagmes — 3 ligne(s) de syntagmes
  ✅ exemples §7.1 --reel — 13 ligne(s)
  ✅ exemples §7.2 --reel JSON — JSON exact
  ✅ demarrage §3.1 --version — 1 ligne(s)
  ✅ demarrage §3.2 analyser — 10 ligne(s)
  ✅ demarrage §3.3 evaluer — 13 ligne(s)
  ✅ demarrage §3.4 JSON — 22 lignes
  ✅ demarrage §3.4 consommateur — 2 ligne(s)
  ✅ demarrage §3.5 profils — 9 ligne(s)
  ✅ note dev analyser — rôle=agent
  ✅ note dev cible — → chat
  ✅ note dev f1 — F1 79.02 %
  ✅ note dev attachement — ATTACHEMENT exact 99.58 %

✅ mutation détectée : 1 cas en écart (attendu > 0)

22/23 cas conformes — ❌ 1 écart(s)
exit=0
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py --json > /tmp/exemples-v2.json; jq '{head, comptes, mutation, ok, resultats: [.resultats[] | {id, ok, detail}]}' /tmp/exemples-v2.json", "description": "Generate JSON report", "timeoutMs": 300000}`

  ```
{
  "head": "2e617034",
  "comptes": {
    "cas": 23,
    "ok": 23,
    "echecs": 0
  },
  "mutation": false,
  "ok": true,
  "resultats": [
    {
      "id": "exemples §1 lisible",
      "ok": true,
      "detail": "10 ligne(s)"
    },
    {
      "id": "exemples §1 JSON",
      "ok": true,
      "detail": "JSON exact"
    },
    {
      "id": "exemples §1 durée",
      "ok": true,
      "detail": "duree_s=0.004359 (variable), octets exacts"
    },
    {
      "id": "exemples §2 JSON",
      "ok": true,
      "detail": "JSON exact"
    },
    {
      "id": "exemples §3 JSON",
      "ok": true,
      "detail": "JSON exact"
    },
    {
      "id": "exemples §4 refus CLI",
      "ok": true,
      "detail": "code 3, stderr exact"
    },
    {
      "id": "exemples §4 refus API",
      "ok": true,
      "detail": "JSON exact"
    },
    {
      "id": "exemples §5 JSON",
      "ok": true,
      "detail": "JSON exact"
    },
    {
      "id": "exemples §6.1 syntagmes",
      "ok": true,
      "detail": "2 ligne(s) de syntagmes"
    },
    {
      "id": "exemples §6.2 syntagmes",
      "ok": true,
      "detail": "4 ligne(s) de syntagmes"
    },
    {
      "id": "exemples §6.3 syntagmes
… [1243 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "RACINE = pathlib.Path(__file__).resolve().parent.parent\nDOCS = RACINE / \"docs\" / \"produit\"\nEXEMPLES = DOCS / \"exemples.md\"\nDEMARRAGE = DOCS / \"demarrage.md\"", "new_string": "RACINE = pathlib.Path(__file__).resolve().parent.parent\n … [320 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "# --------------------------------------------------------------------------- principal", "new_string": "def verifier_invariants() -> list[dict]:\n    \"\"\"Les invariants v2 : candidats objets, spans exacts, rôles dans le vocabulaire, durée. … [3300 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "        if note and not args.sans_demarrage:\n            resultats.extend(verifier_note_demarrage(note))\n    finally:", "new_string": "        if note and not args.sans_demarrage:\n            resultats.extend(verifier_note_demarrage(note)) … [65 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py", "description": "Run verifier with invariants", "timeoutMs": 300000}`

  ```
✅ exemples §1 lisible — 10 ligne(s)
  ✅ exemples §1 JSON — JSON exact
  ✅ exemples §1 durée — duree_s=0.004041 (variable), octets exacts
  ✅ exemples §2 JSON — JSON exact
  ✅ exemples §3 JSON — JSON exact
  ✅ exemples §4 refus CLI — code 3, stderr exact
  ✅ exemples §4 refus API — JSON exact
  ✅ exemples §5 JSON — JSON exact
  ✅ exemples §6.1 syntagmes — 2 ligne(s) de syntagmes
  ✅ exemples §6.2 syntagmes — 4 ligne(s) de syntagmes
  ✅ exemples §6.3 syntagmes — 3 ligne(s) de syntagmes
  ✅ exemples §7.1 --reel — 13 ligne(s)
  ✅ exemples §7.2 --reel JSON — JSON exact
  ✅ demarrage §3.1 --version — 1 ligne(s)
  ✅ demarrage §3.2 analyser — 10 ligne(s)
  ✅ demarrage §3.3 evaluer — 13 ligne(s)
  ✅ demarrage §3.4 JSON — 22 lignes
  ✅ demarrage §3.4 consommateur — 2 ligne(s)
  ✅ demarrage §3.5 profils — 9 ligne(s)
  ✅ note dev analyser — rôle=agent
  ✅ note dev cible — → chat
  ✅ note dev f1 — F1 79.02 %
  ✅ note dev attachement — ATTACHEMENT exact 99.58 %
  ✅ invariants candidats objets — 18 candidats objets, 0 span faux
  ✅ invariants rôles normalisés — 4 rôle(s), tous dans les 8 du vocabulaire
  ✅ invariants durée — absente sans --duree, numérique avec

26/26 cas conformes — ✅ aucun écar
… [1 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py --mutation >/tmp/mutation.txt 2>&1; code=$?; tail -4 /tmp/mutation.txt; echo \"exit=$code\"", "description": "Test mutation control again", "timeoutMs": 300000}`

  ```
✅ mutation détectée : 1 cas en écart (attendu > 0)

25/26 cas conformes — ❌ 1 écart(s)
exit=0
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "    cmd = bloc_bash(s, \"--json\")\n    commande = (cmd.corps.replace(\"drave \", \"python3 tools/drave.py \", 1)\n                .replace(\"> annotation.json\", \"> annotation.json\"))\n    attendu = bloc_lang(s, \"json\").corps\n    cas.ap … [674 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/verifie_exemples.py", "old_string": "    if c.genre == \"json_lignes\":", "new_string": "    if c.genre == \"octets\":\n        if proc.returncode != 0:\n            return False, [f\"code {proc.returncode}: {proc.stderr.strip()[:300]}\"], \"\"\n        fichier = c.cwd / \"annot … [373 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py | tail -8", "description": "Run verifier with byte-size check", "timeoutMs": 300000}`

  ```
✅ note dev cible — → chat
  ✅ note dev f1 — F1 79.02 %
  ✅ note dev attachement — ATTACHEMENT exact 99.58 %
  ✅ invariants candidats objets — 18 candidats objets, 0 span faux
  ✅ invariants rôles normalisés — 4 rôle(s), tous dans les 8 du vocabulaire
  ✅ invariants durée — absente sans --duree, numérique avec

27/27 cas conformes — ✅ aucun écart
  ```

- **bash** `{"command": "python3 -m py_compile tools/verifie_exemples.py && echo OK; python3 tools/verifie_exemples.py --json | jq '{ok, comptes, head}'", "description": "Compile and JSON check", "timeoutMs": 300000}`

  ```
OK
{
  "ok": true,
  "comptes": {
    "cas": 27,
    "ok": 27,
    "echecs": 0
  },
  "head": "2e617034"
}
  ```

- **bash** `{"command": "grep -n \"qualité\\|prédicat\\|groupe nominal\" docs/produit/exemples.md", "description": "Search stale role spellings"}`

  ```
15:> rôles** : `qualité` → `qualite`, `prédicat` → `predicat`, `groupe nominal` → `objet`.
59:  (`prédicat` → `predicat`, `qualité` → `qualite`, `groupe nominal`/`patient`/`complément` →
496:- Les deux REL portent `role: qualite` : la forme accentuée `qualité` est **normalisée**, comme
497:  `prédicat` en `predicat`. Les `candidats_objets` publient `livre[3:8]` et
686:- Les rôles sont **normalisés** : `The day` est `objet` (le brut `groupe nominal` tombe sur
883:- Rôles **normalisés** : `The film` est `objet` (brut `groupe nominal`), `she talks about`
884:  `qualite` (brut `qualité`), `is out` `predicat`. Les candidats objets publient `out[21:24]`
1070:étiquette ici l'anglais correctement ; ce n'est pas une preuve de qualité par langue (la
1137:la qualité réelle. La F1, elle, est quasi identique (79,06 contre 79,02). Publier le seul
1217:   huit valeurs (`predicat` sans accent, `groupe nominal` → `objet`), pas raffinés. Le champ
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "> **Le rejeu du 2026-11-16.** **3 blocs sur 5** ont bougé, tous par la **normalisation des\n> rôles** : `qualité` → `qualite`, `prédicat` → `predicat`, `groupe nominal` → `objet`.\n> `g001` et le refus sont identiques champ pour champ. Les **c … [792 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"exemples.md\" docs/produit/README.md docs/produit/demarrage.md docs/README.md reports/README.md | head -20", "description": "Find references to examples doc"}`

  ```
docs/produit/README.md:103:[`exemples.md`](exemples.md).
docs/produit/README.md:143:`union: true`, à filtrer pour une lecture unique (voir [`exemples.md`](exemples.md) § 2).
docs/produit/README.md:504:[`exemples.md`](exemples.md) § 6).
docs/produit/README.md:578:[`exemples.md`](exemples.md) § 6 totalisent **3 appels**, **441 tokens** et **3,7 s**.
docs/produit/README.md:937:gratuite (**0 réseau, 0 token**). Les trois exemples de [`exemples.md`](exemples.md) totalisent
docs/produit/README.md:1055:| **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |
docs/produit/demarrage.md:286:| cinq JSON commentés et un cas d'échec connu | [`exemples.md`](exemples.md) |
docs/README.md:99:| [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels, dont un échec connu |
  ```

- **write** `{"file_path": "reports/rapport-exemples-v2.md", "content": "# V2 — les cinq exemples rejoués : 3 blocs corrigés par les rôles normalisés, 27/27 cas conformes\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **V2** (exploitable, 21/21) ·\n> **Date** : 2026-11-16 · **Verdict** : ✅\n> **Cinq … [8481 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-v2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" | head -2; python3 tools/drave.py analyser \"The film she talks about is out.\" | head -2", "description": "Check tag counts"}`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 43 étiquettes · unités sémantiques=3 (48.6% du texte)
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=en script=Latn source=heuristique · 37 étiquettes · unités sémantiques=2 (28.1% du texte)
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py --json > /tmp/exemples-v2.json && python3 - <<'PY'\nimport json, pathlib, subprocess\nbase = json.load(open('/tmp/exemples-v2.json'))\nhead = subprocess.run(['git','rev-parse','--short=8','HEAD'], text=True, capture_output=True).stdout.strip()\nrapport  … [4312 caractères tronqués]`

  ```
reports/rapport-exemples-v2.json 7237
{
  "tache": "V2",
  "head": "2e617034",
  "exemples": 3,
  "controle_negatif": {
    "script": "tools/verifie_exemples.py",
    "cas": 27,
    "conformes": 27,
    "echecs": 0,
    "mutation": {
      "motif": "\"role\": \"qualite\" -> \"role\": \"qualité\"",
      "detectee": true,
      "cas_en_ecart": 1
    }
  },
  "comptes": {
    "cas": 27,
    "conformes": 27
  }
}
  ```

- **bash** `{"command": "grep -n \"Mis à jour\\|U3\\|V1\\|Ce qui est en cours\\|Ce qui reste\\|Prochaine action\" docs/pilotage/en-cours.md | head -30", "description": "Locate state lines"}`

  ```
3:**Mis à jour : 2026-11-16 (`evaluer --strict`)**
12:- **Prochaine action** : **suivi docs**, puis la **passe**.
36:- **Prochaine action** : reprise par le hub `1e7ef596` ; l'état du 04/11 est la source.
51:- **Prochaine action** : **migration `/` v7** (106/41) ; référents ; rétro-traduction.
62:- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** la roue : **1 727 201 o**, mêmes JSON hors dépôt, sans gold → **4** ([fiche](../../reports/rapport-roue.md)) ; **U3** profils **20/20**, ambigu **`und`** ([fiche](../../reports/rapport-profils.md)) ; **V1** `--strict` : **0,8625** / **0,8891** ([fiche](../../reports/rapport-evaluer-strict.md)).
63:- **Prochaine action** : **J4** ; T132/T133 ; la décision `auto`.
77:- **Prochaine action** : la **porte propre (0,29)** ; le **2 048** est fini.
81:## Ce qui est en cours
85:- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → 4) ; **U3** profils 20/20 ; [v2](../..
… [1521 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-16 (`evaluer --strict`)**", "new_string": "**Mis à jour : 2026-11-16 (V2, les exemples de la doc)**"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "offset": 1, "limit": 10}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-16 (`evaluer --strict`)**
4: 
5: > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
6: 
7: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
8: 
9: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
10: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.

(Showing lines 1-10 of 143. Use offset=11 to continue.)
</content>
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-16 (`evaluer --strict`)**", "new_string": "**Mis à jour : 2026-11-16 (V2, les exemples de la doc)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** la roue : **1 727 201 o**, mêmes JSON hors dépô … [883 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → 4) ; **U3** profils 20/20 ; [v2](../../reports/ … [660 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s) ; **U2 — la roue** (1 727 201 o, sans gold → 4) ; **U3** profils 20/20 ; [bilan](../../reports/rapport-bilan-exploitable.md), [U1](../../reports/rapport-performan … [514 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "**B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : roue 1 727 201 o, mêmes JSON, sans gold → evaluer 4 ; U3 : profils 398 langues, 20/20, ambigu und** | **`g017` tranché** ; **J4* … [474 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"V1 —\\|U3\\|T6 — le bilan exploitable\" docs/pilotage/roadmap.md | tail -10", "description": "Locate roadmap V1"}`

  ```
172:**U3** : **398 profils UDHR** ; **20/20**, **433/447** ; ambigu **`und`**
175:**V1 — `evaluer --strict` (16/11).** Quatre modes, cascade **0,8625** / **0,8891**, plancher
179:**T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques ; trois limites (clone public,
  ```

- **read** `{"file_path": "docs/pilotage/roadmap.md", "offset": 170, "limit": 14}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
170: ([fiche](../../reports/rapport-roue.md)).
171: 
172: **U3** : **398 profils UDHR** ; **20/20**, **433/447** ; ambigu **`und`**
173: ([fiche](../../reports/rapport-profils.md)).
174: 
175: **V1 — `evaluer --strict` (16/11).** Quatre modes, cascade **0,8625** / **0,8891**, plancher
176: **0,70** ; négatif **0,0000** → **1**. [Fiche](../../reports/rapport-evaluer-strict.md) ·
177: [JSON](../../reports/evaluer-strict.json).
178: 
179: **T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques ; trois limites (clone public,
180: O(k²), or de S). [Fiche](../../reports/rapport-bilan-exploitable.md) ·
181: [JSON](../../reports/rapport-bilan-exploitable.json). Restent **J4**, **Panini**, `auto`.
182: 
183: **La vue d'ensemble** est dans [`chantiers.md`](chantiers.md) ; carte,

(Showing lines 170-183 of 515. Use offset=184 to continue.)
</content>
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "old_string": "**V1 — `evaluer --strict` (16/11).** Quatre modes, cascade **0,8625** / **0,8891**, plancher\n**0,70** ; négatif **0,0000** → **1**. [Fiche](../../reports/rapport-evaluer-strict.md) ·\n[JSON](../../reports/evaluer-strict.json).\n\n**T6 — le bi … [945 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "journal/2026-11-16/README.md", "offset": 1, "limit": 10}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md</path>
<type>file</type>
<content>
1: # 2026-11-16
2: 
3: > **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
4: > [`journal/2026-11-16/`](README.md). Le récit écrit à la main est conservé plus bas, dans
5: > le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
6: > [l'index des sessions](../README.md#sessions).
7: 
8: **5 commits** · **1 session(s)** · **3 thème(s)**
9: 
10: ## Thèmes du jour

(Showing lines 1-10 of 53. Use offset=11 to continue.)
</content>
  ```

- **read** `{"file_path": "journal/2026-11-16/README.md", "offset": 38, "limit": 16}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md</path>
<type>file</type>
<content>
38: 
39: `python3 -m pip wheel . --no-deps --no-build-isolation -w dist` a rendu
40: **`drave-0.1.0-py3-none-any.whl`** (1 727 201 o, 422 entrées, sha256 `d980c470…a99dbce`).
41: Installée dans un venv propre **depuis le fichier**, elle rend depuis `/tmp` `drave 0.1.0`,
42: `drave analyser "Le chat dort."` (`rôle=agent`) et `drave evaluer --json` (gold 612, POS 0,8625,
43: F1 0,7902, exact 0,9958). Les JSON sont **identiques au bit près** à ceux du dépôt.
44: 
45: La décision : les cinq **gold** sont des `package-data`, avec `tools.tests.linguistique`,
46: `tools.structures` et `tools.llm`. Une roue **amputée** des gold installe et analyse encore,
47: mais `drave evaluer` sort en **4**, `stdout` vide, et nomme les fichiers manquants ; `--gold`
48: sélectionne le gelé et ne remplace pas un gold absent. C'est le contrôle négatif qui manquait
49: à T1, où le wheel échouait avant même d'analyser. Le point S (sans `generateur`, `rôle=objet`
50: au lieu d'`agent`) a été trouvé et corrigé par l'embarquement de `tools.structures`.
51: 
52: [Fiche](../../reports/rapport-roue
… [115 caractères tronqués]
  ```

- **edit** `{"file_path": "journal/2026-11-16/README.md", "old_string": "[Fiche](../../reports/rapport-roue.md) · [JSON](../../reports/roue.json) · doc § 8.10.\n<!-- /notes -->", "new_string": "[Fiche](../../reports/rapport-roue.md) · [JSON](../../reports/roue.json) · doc § 8.10.\n\n### V2 — les exemples de la  … [1052 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md has been updated successfully.
  ```

- **bash** `{"command": "git diff --stat -- docs/produit/exemples.md reports/rapport-exemples-v2.md reports/rapport-exemples-v2.json tools/verifie_exemples.py docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-16/README.md", "description": "Diff stat of V2 files"}`

  ```
docs/pilotage/en-cours.md    |  14 +-
 docs/pilotage/roadmap.md     |  29 +++--
 docs/produit/exemples.md     | 299 ++++++++++++++++++++++++++++++++++++++-----
 journal/2026-11-16/README.md |  16 +++
 4 files changed, 309 insertions(+), 49 deletions(-)
  ```

- **bash** `{"command": "git diff -- docs/produit/exemples.md | head -200", "description": "Review examples diff"}`

  ```
diff --git a/docs/produit/exemples.md b/docs/produit/exemples.md
index 493cd772..8c88a51c 100644
--- a/docs/produit/exemples.md
+++ b/docs/produit/exemples.md
@@ -4,10 +4,22 @@
 > complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
 > *comment lire* ce qui sort. Les **cinq premiers blocs** ont été produits le **2026-11-06** sur
 > la branche `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et
-> sans réseau ; ils ont été **rejoués le 2026-11-14** sur le code courant — F1 **0,7902**,
+> sans réseau ; ils ont été **rejoués le 2026-11-16** sur le code courant — F1 **0,7902**,
 > attachement **238/238 labels** (238/239 cibles), schéma **v2**. Le format v2 ajoute
-> `version: 2` et, sur un syntagme qui chevauche un autre, `meta.partition`/`meta.alternative` ;
-> v1 reste lue ([schéma v2](../../tools/schemas/drave-annotation-v2.json)).
+> `version: 2`, `meta.attachement.candidats` en **objets** `{span, cible, source}`, un
+> `meta.role` **normalisé** (huit valeurs) et, sur un syntagme qui chevauche un autre,
+> `meta.partition`/`meta.alternative` ; v1 reste lue
+> ([schéma v2](../../tools/schemas/drave-annotation-v2.jso
… [9238 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -80", "description": "Documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 770 fiche(s) · 865 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 769 fichiers, le disque en a 770
     · compteurs : en-cours.md dit 864 JSON, le disque en a 865
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -40", "description": "Table gate", "timeoutMs": 300000}`

  ```
✅ 1851 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4783 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
  ```

- **bash** `{"command": "grep -n \"769\\|864\" docs/pilotage/en-cours.md", "description": "Find counter line"}`

  ```
101:| fichiers / JSON de résultats | **769** / **864** | `reports/*.md` / `reports/*.json` |
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "offset": 99, "limit": 4}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
99: | portes | **86** (dont `porte-banc-performance` le 15/11) | `tools/porte-*.sh` |
100: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
101: | fichiers / JSON de résultats | **769** / **864** | `reports/*.md` / `reports/*.json` |
102: | documents de `docs/` | **125** (hors archive et README) | `docs/**/*.md` |

(Showing lines 99-102 of 143. Use offset=103 to continue.)
</content>
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **769** / **864** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **770** / **865** | `reports/*.md` / `reports/*.json` |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -20", "description": "Rerun documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 770 fiche(s) · 865 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo \"---\"; python3 tools/verifie_journal.py 2>&1 | tail -30", "description": "State and journal checks", "timeoutMs": 300000}`

  ```
en-cours · 1668 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
---
  journal · 48 jour(s) · 226 session(s) · 2722 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -20; echo \"---\"; python3 tools/taille_documents.py 2>&1 | tail -20", "description": "Schemas and size checks", "timeoutMs": 300000}`

  ```
schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
---
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2800    234   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4038 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-visio
… [280 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "old_string": "**V2 — les exemples de la doc (16/11).** Les **5 blocs** rejoués : **3 corrigés** par les\n**rôles normalisés** (`qualité` → `qualite`, `prédicat` → `predicat`, `groupe nominal` →\n`objet`), **2 identiques** hors enrichissement ; **18 candidat … [774 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** la roue : **1 727 201 o**, mêmes JSON hors dépô … [674 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20", "description": "Rerun size budget", "timeoutMs": 300000}`

  ```
2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2800    234   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4010 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/
… [110 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "old_string": "**V2 — les exemples de la doc (16/11).** **5 blocs** rejoués, **3 corrigés** par les rôles\nnormalisés, **2 identiques** ; **18 candidats objets**, **0 span faux** ; `--duree` documentée.\n`tools/verifie_exemples.py` : **27/27**, mutation **1/ … [466 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → 4) ; **U3** profils 20/20 ; **V2** les exemples … [660 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8", "description": "Rerun size budget again", "timeoutMs": 300000}`

  ```
T0 max : 4004 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9013 mots > budget 9000 (T1)
     · T0 : 4004 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "old_string": "**V2 — les exemples (16/11).** 5 blocs, 3 corrigés par les rôles normalisés ; 18 candidats\nobjets, 0 span faux ; `tools/verifie_exemples.py` 27/27, mutation 1/1 ; démarrage 3/3 sans\n`tools/structures`. [Fiche](../../reports/rapport-exemples- … [320 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "old_string": "O(k²), or de S). [Fiche](../../reports/rapport-bilan-exploitable.md) ·\n[JSON](../../reports/rapport-bilan-exploitable.json). Restent **J4**, **Panini**, `auto`.", "new_string": "O(k²), or de S). [Fiche](../../reports/rapport-bilan-exploitable … [63 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s) ; **U2 — la roue** (1 727 201 o, sans gold → 4) ; **U3** profils 20/20 ; **V2** les exemples **27/27** ; [bilan](../../reports/rapport-bilan-exploitable.md), [U1] … [569 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -6", "description": "Rerun size budget", "timeoutMs": 300000}`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9001 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8", "description": "Rerun doc review", "timeoutMs": 300000}`

  ```
revue de documentation · 770 fiche(s) · 865 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "old_string": "**V2 — exemples (16/11).** 3 corrigés par les rôles normalisés ; 18 candidats objets, 0 faux ;", "new_string": "**V2 — exemples.** 3 corrigés par les rôles normalisés ; 18 candidats objets, 0 faux ;"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -4", "description": "Check size budget final", "timeoutMs": 300000}`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "bash tools/porte-produit.sh > /tmp/porte-produit-v2.log 2>&1; echo $? > /tmp/porte-produit-v2.code", "description": "Run product gate", "run_in_background": true}`

  ```
started background job bash-108
  ```

- **bash** `{"command": "grep -n \"exemples\" reports/INDEX.md reports/README.md | head -20", "description": "Check report index"}`

  ```
reports/INDEX.md:190:| [rapport-exemples-rejoues.md](rapport-exemples-rejoues.md) | J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec |
reports/INDEX.md:191:| [rapport-exemples-tagger.md](rapport-exemples-tagger.md) | D1 — les exemples `--tagger` et `--reel` : le coût affiché, la base honnête, cinq blocs rejoués |
reports/README.md:32:| [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md) | **B13** — les 5 exemples de la doc |
reports/README.md:33:| [`rapport-exemples-tagger.md`](rapport-exemples-tagger.md) | **D1** — les 3 exemples `--tagger` (coût affiché) et les 2 `--reel` (base honnête) |
  ```

- **bash** `{"command": "git status --short | head -60", "description": "Working tree status"}`

  ```
M docs/implantation/bloc-linguistique.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M docs/produit/demarrage.md
 M docs/produit/exemples.md
 M journal/2026-11-16/README.md
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
?? reports/rapport-exemp
… [388 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,20p' reports/INDEX.md; sed -n '180,200p' reports/INDEX.md", "description": "Read report index header"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **766 fiches**. Les fichiers
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
… [3500 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '20,45p' reports/README.md", "description": "Read report README table"}`

  ```
| [`rapport-bilan-nuit.md`](rapport-bilan-nuit.md) | **Bilan** — la nuit du 14 au 15/11 : le tagger, la base honnête, la phase C/B |
| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
| [`rapport-gold-452.md`](rapport-gold-452.md) | **W1/R0.7** — le gold réel 452 : composition, split 402/H50, sha256, 10 candidats GP/SUB |
| [`rapport-tagger-h50.md`](rapport-tagger-h50.md) | **W2/R0.7** — le tagger sur le split : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/attachement 402 inchangés, fermé 402 **−1,55** ; la règle ne le rejette pas |
| [`rapport-tagger-defaut.md`](rapport-tagger-defaut.md) | **W3/R0.7** — la matrice du tagger : défaut hors ligne **code 0** / `--tagger` **code 4** sans clé ; réseau coupé = repli **code 0** ; coût **1 000 phrases** = 143 870 tokens, ~0,031 $ hors pointe ; recommandation : défaut hors ligne, opt-in, pas de `auto` |
| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (677 textes), **672 appels réseau**, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,8 Mo**, **0,02177 $** ; cache chaud **
… [2660 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/index_reports.py --help 2>&1 | head -30", "description": "Check index_reports usage"}`

  ```
usage: index_reports.py [-h] [--verifier] [--aide]

Génère reports/INDEX.md (déterministe).

options:
  -h, --help  show this help message and exit
  --verifier  ne réécrit rien : compare l'index au disque, sort 1 s'il est
              périmé
  --aide      affiche l'aide et sort
  ```

- **bash** `{"command": "python3 tools/index_reports.py && head -5 reports/INDEX.md && grep -n \"rapport-exemples-v2\\|rapport-profils\\|rapport-evaluer-strict\" reports/INDEX.md", "description": "Regenerate report index", "timeoutMs": 300000}`

  ```
767 fiches → reports/INDEX.md
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **767 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.
188:| [rapport-evaluer-strict.md](rapport-evaluer-strict.md) | V1 — `evaluer --strict` : les quatre modes locaux, la cascade à 86,25 % / 88,91 %, le plancher 0,70 qui mord |
192:| [rapport-exemples-v2.md](rapport-exemples-v2.md) | V2 — les cinq exemples rejoués : 3 blocs corrigés par les rôles normalisés, 27/27 cas conformes |
666:| [rapport-profils.md](rapport-profils.md) | U3 — `drave profils` : la détection de langue des 398 profils UDHR, exposée |
  ```

- **read** `{"file_path": "reports/README.md", "offset": 30, "limit": 6}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
30: | [`note-panini-334.md`](note-panini-334.md) | **Panini** — la note à envoyer : H0 reproduite, β époque non, la collinéarité |
31: | [`rapport-panini-334.md`](rapport-panini-334.md) | **Panini** — le §334 : H0 0,909/0,906, la |
32: | [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md) | **B13** — les 5 exemples de la doc |
33: | [`rapport-exemples-tagger.md`](rapport-exemples-tagger.md) | **D1** — les 3 exemples `--tagger` (coût affiché) et les 2 `--reel` (base honnête) |
34: | [`rapport-evaluer-langue.md`](rapport-evaluer-langue.md) | **B13** — `evaluer --par-langue` : fr 0,8159 / |
35: | [`rapport-robustesse-semaine.md`](rapport-robustesse-semaine.md) | **B13** — les 50 textes libres après le |

(Showing lines 30-35 of 233. Use offset=36 to continue.)
</content>
  ```

- **edit** `{"file_path": "reports/README.md", "old_string": "| [`rapport-exemples-tagger.md`](rapport-exemples-tagger.md) | **D1** — les 3 exemples `--tagger` (coût affiché) et les 2 `--reel` (base honnête) |", "new_string": "| [`rapport-exemples-tagger.md`](rapport-exemples-tagger.md) | **D1** — les 3 exemple … [210 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8", "description": "Doc review after index update", "timeoutMs": 300000}`

  ```
revue de documentation · 770 fiche(s) · 865 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **job_output** `{"job_id": "bash-108", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "git diff -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -160", "description": "Review state/roadmap diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 36ca8023..e933ea41 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-16, 00 h 45 HNE (U2 : la roue, les gold dedans, la roue sans gold échoue)**
+**Mis à jour : 2026-11-16 (V2, les exemples de la doc)**
 
 > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
 
@@ -59,8 +59,8 @@
 - **Plan** : B13 · **Stratégie** : v0 · **Ambition** : tracé · **Objectif final** : moteur v0.
 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.
 - **Ce que font les autres** : N2.
-- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** la roue : **1 727 201 o**, mêmes JSON hors dépôt, sans gold → `evaluer` **4** ([fiche](../../reports/rapport-roue.md)).
-- **Prochaine action** : **U3 — `--profils`** ; **J4** ; T132/T133.
+- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**, v2 **20/46**) ; **U1** 4,0 → 0,82 s (α 1,08) ; **U2** roue 1 727 201 o, s
… [9414 caractères tronqués]
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-exemples-v2.json >/dev/null && echo JSON-OK; wc -l reports/rapport-exemples-v2.md tools/verifie_exemples.py; grep -n \"27/27\\|18 candidats\\|5 899\\|3/3\" reports/rapport-exemples-v2.md", "description": "Check report consistency"}`

  ```
JSON-OK
  167 reports/rapport-exemples-v2.md
  585 tools/verifie_exemples.py
  752 total
1:# V2 — les cinq exemples rejoués : 3 blocs corrigés par les rôles normalisés, 27/27 cas conformes
9:> documentée (`--duree`). Les **3 commandes** du démarrage sont rejouées **3/3** dans une copie
10:> **sans** `tools/structures` (JSON **5 899 octets**).
119:Le § 3.4 est vérifié aussi : le JSON complet fait **5 899 octets**, l'extrait de 22 lignes et le
141:Résultat : **27/27 cas conformes, 0 écart**. Le contrôle du contrôle : le mode `--mutation`
  ```

- **bash** `{"command": "sed -n '1,80p' tools/profils_udhr.py; sed -n '1,40p' tools/drave.py | tail -10", "description": "Check profils import dependencies"}`

  ```
#!/usr/bin/env python3
"""profils_udhr.py — les profils de langue UDHR, chargés et exposés par le CLI.

Le bloc linguistique sait déjà détecter la langue par **recouvrement de trigrammes** sur les
profils construits depuis l'UDHR (`bloc_linguistique.charger_profils_udhr`). Ce module rend
cette détection **utilisable** : il charge l'artefact de profils (un JSON versionné, embarqué
dans la roue), expose la langue probable, le script et la confiance, et garde le seuil du
produit (`0,12`) explicite.

    python3 tools/drave.py profils --texte "Le chat dort."
    python3 tools/drave.py profils --texte "Le chat the cat dort sleeps." --json

Le profil est une **donnée**, pas un prompt : il se versionne, se rejoue et se vérifie par son
empreinte. Il est construit par `tools/construire_profils_udhr.py` à partir des articles 0–14
de `data/udhr/articles.jsonl` ; l'article 15 reste tenu à l'écart pour la mesure.

Ce que la confiance est : la marge du premier profil sur le second, mélangée au recouvrement
(`(meilleur - second) / meilleur + 0,2 × meilleur`). Ce n'est **pas** une probabilité calibrée.
Sous le seuil `0,12`, la **décision** du produit est `und` ; la langue probable reste exposée.
"
… [3154 caractères tronqués]
  ```

- **bash** `{"command": "git log --all --oneline -- tools/profils_udhr.py | head; git branch -a | head; git status --porcelain=v1 | wc -l", "description": "Check if profils code committed elsewhere"}`

  ```
backup/pre-scrub-20261101-133055
  master
  s/close
* s/v7
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/s/close
  remotes/origin/s/v7
47
  ```

- **job_output** `{"job_id": "bash-108", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -30 /tmp/porte-produit-v2.log 2>/dev/null; echo '---'; ps -o pid,etime,cmd -C python3 | tail -10", "description": "Check gate progress"}`

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
---
1650795       00:01 python3 -m tools.pensee.autotest
1650796       00:01 python3 -m tools.pensee.autotest
1650797       00:01 python3 -m tools.pensee.autotest
1650798       00:01 python3 -m tools.pensee.autotest
1650799       00:01 python3 -m tools.pensee.autotest
1650800       00:01 python3 -m tools.pensee.autotest
1650801       00:01 python3 -m tools.pensee.autotest
1650802       00:01 python3 -m tools.pensee.autotest
1650803       00:01 python3 -m tools.pensee.autotest

… [51 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"pensee-quatre-modes\\|profils.json\\|evaluer-strict.json\" reports/rapport-evaluer-strict.md reports/rapport-profils.md | head -20; ls -lh tools/tests/linguistique/profils_udhr.json reports/rapport-exemples-v2.json", "description": "Check report dependencies"}`

  ```
reports/rapport-evaluer-strict.md:17:> (5 tests) · [`reports/evaluer-strict.json`](evaluer-strict.json) · `tools/drave.py`
reports/rapport-evaluer-strict.md:124:- [`reports/evaluer-strict.json`](evaluer-strict.json) — le rapport complet (modes 612 et 452,
reports/rapport-profils.md:20:> [`reports/profils.json`](profils.json), [`tools/drave.py`](../tools/drave.py),
reports/rapport-profils.md:200:| `reports/profils.json` | la mesure reproductible |
-rw-r--r--. 1 stephane stephane 7,1K 16 nov 02:38 reports/rapport-exemples-v2.json
-rw-r--r--. 1 stephane stephane 784K 16 nov 01:39 tools/tests/linguistique/profils_udhr.json
  ```

- **bash** `{"command": "git diff --stat | tail -5; git status --short | awk '{print $1}' | sort | uniq -c", "description": "Summarize working changes"}`

  ```
tools/porte-produit.sh                             |  21 +
 tools/tests/test_empaquetage.py                    |  10 +-
 tools/tests/test_produit.py                        |   6 +-
 tools/verifier_faq.py                              |   6 +-
 31 files changed, 1568 insertions(+), 458 deletions(-)
     16 ??
     31 M
  ```

- **bash** `{"command": "find journal/sessions/session-9e0eeeb8-7572-4a68-a74e-7405d06e3757 -maxdepth 1 -type f -printf '%f %s\\n' 2>/dev/null; head -20 journal/sessions/session-9e0eeeb8-7572-4a68-a74e-7405d06e3757/*.md 2>/dev/null | head -40", "description": "Inspect new session dir"}`

  ```
session.v4.jsonl.zstd 309143
digest.md 96643
rapport.md 14991
==> journal/sessions/session-9e0eeeb8-7572-4a68-a74e-7405d06e3757/digest.md <==
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
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct 
… [663 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"gold_reel_50\\|rapport-s-paragraphes\" tools reports docs journal 2>/dev/null | head -20", "description": "Check unrelated untracked files"}`

  ```
tools/tests/linguistique/qualifier_tagger_h50.py:73:    import gold_reel_50 as c3
tools/tests/linguistique/gold_reel_50.py:2:"""gold_reel_50.py — les 50 phrases réelles que l'heuristique rate (proposition C3/R).
tools/tests/linguistique/gold_reel_50.py:27:    python3 tools/tests/linguistique/gold_reel_50.py \
tools/tests/linguistique/gold_reel_50.py:593:            "script": "tools/tests/linguistique/gold_reel_50.py",
reports/rapport-file-taches.md:22:**Sources lues** : `docs/pilotage/roadmap.md` (382 l.), `en-cours.md` (145 l., version 10 h 20), `plan-travail.md` § 9 et § 12 (deux sections 9 : l. 163 et 403), `backlog/index.md` (37 fiches), `backlog/dependances.md` (43 arêtes, 3 plafonds), `references-non-regression.md` (84 portes), les 12 fiches `reports/rapport-*.md` les plus récentes, les fiches produit (`rapport-produit-v0.md`, `rapport-autotest-parallele.md`) et les fiches de blocage (`rapport-a26-bilan.md`, `rapport-a26-lot-disque.md`, `rapport-n2-r12-2048.md`, `rapport-s-paragraphes.md`).
reports/rapport-file-taches.md:26:**État de l'arbre** : `s/v7`, HEAD `7679a2d4` à 10 h 20. L'arbre est **sale avant** l'inventaire (journal, sept `reports/` modifiés, `tools/structures` mo
… [2003 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-108", "wait": true, "timeout_ms": 300000}`

  ```
(no new output)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "tail -5 /tmp/porte-produit-v2.log; cat /tmp/porte-produit-v2.code", "description": "Read gate result"}`

  ```
✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
0
  ```

- **edit** `{"file_path": "tools/porte-produit.sh", "old_string": "if AUTOTEST_JOBS=8 timeout 600 python3 -m tools.pensee.autotest >/tmp/porte-produit-autotest.log 2>&1; then", "new_string": "if python3 tools/verifie_exemples.py >/tmp/porte-produit-exemples.log 2>&1; then\n  dit ✅ \"exemples de la doc : $(tail  … [262 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "tools/porte-produit.sh", "offset": 135, "limit": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh</path>
<type>file</type>
<content>
135:   dit ❌ "refus : code $code, JSON non conforme"; ko=1
136: fi
137: 
138: if AUTOTEST_JOBS=8 timeout 600 python3 -m tools.pensee.autotest >/tmp/porte-produit-autotest.log 2>&1; then
139:   dit ✅ "autotest parallèle : $(grep -oE '[0-9]+/[0-9]+ portes tenues' /tmp/porte-produit-autotest.log | tail -1)"
140: else
141:   dit ❌ "autotest en échec (voir /tmp/porte-produit-autotest.log)"; ko=1
142: fi
143: 
144: [ "$ko" -eq 0 ] && { echo "✅ porte produit verte"; exit 0; } || { echo "❌ porte produit rouge"; exit 1; }

(End of file - total 144 lines)
</content>
  ```

- **edit** `{"file_path": "tools/porte-produit.sh", "old_string": "if AUTOTEST_JOBS=8 timeout 600 python3 -m tools.pensee.autotest >/tmp/porte-produit-autotest.log 2>&1; then", "new_string": "if python3 tools/verifie_exemples.py >/tmp/porte-produit-exemples.log 2>&1; then\n  dit ✅ \"exemples de la doc : $(tail  … [262 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py >/tmp/porte-produit-exemples.log 2>&1; echo \"code=$?\"; tail -1 /tmp/porte-produit-exemples.log | sed 's/^ *//'", "description": "Test gate example line", "timeoutMs": 300000}`

  ```
code=0
27/27 cas conformes — ✅ aucun écart
  ```

- **bash** `{"command": "bash tools/porte-produit.sh > /tmp/porte-produit-v2b.log 2>&1; echo $? > /tmp/porte-produit-v2b.code", "description": "Run product gate again", "run_in_background": true}`

  ```
started background job bash-127
  ```

- **bash** `{"command": "git status --porcelain", "description": "Full status for staging"}`

  ```
M docs/implantation/bloc-linguistique.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M docs/produit/demarrage.md
 M docs/produit/exemples.md
 M journal/2026-11-16/README.md
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
?? reports/rapport-exemp
… [388 caractères tronqués]
  ```

- **bash** `{"command": "git diff --check; echo \"diff-check=$?\"; python3 -m py_compile tools/drave.py tools/profils_udhr.py tools/verifie_exemples.py tools/tests/test_profils.py tools/tests/test_evaluer_strict.py && echo COMPILE-OK", "description": "Whitespace and compile check"}`

  ```
diff-check=0
COMPILE-OK
  ```

- **bash** `{"command": "grep -rIn \"sk-[A-Za-z0-9]\\{20,\\}\\|DEEPSEEK_API_KEY=.*[A-Za-z0-9]\" tools reports docs journal/2026-11-16 2>/dev/null | head -5; echo \"secret-scan-done\"", "description": "Scan for secrets in changed areas"}`

  ```
tools/llm/deepseek.py:27:    DEEPSEEK_API_KEY=... python3 tools/llm/deepseek.py --prompt ... --json
tools/llm/enseignant.py:17:    DEEPSEEK_API_KEY=... python3 tools/llm/enseignant.py \
tools/porte-deepseek.sh:12:# La mesure **live** est opt-in : `DEEPSEEK_API_KEY=... DEEPSEEK_LIVE=1
tools/structures/README.md:288:export DEEPSEEK_API_KEY=sk-…
reports/pensee-etat-s.json:343:   "commande": "DEEPSEEK_CACHE=\"$PWD/work/deepseek-cache\" DEEPSEEK_API_KEY=... python3 tools/llm/enseignant.py --prompts work/retro-traduction/prompts-fr-en.jsonl --sortie work/retro-traduction/fr-en.jsonl ; puis mesure.py --entree ... --json ...",
secret-scan-done
  ```

- **job_output** `{"job_id": "bash-127", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "paths=$(git status --porcelain | sed 's/^...//' | sed 's/^\"//;s/\"$//'); git add -- $paths; git status --short | head -60; echo '---'; git diff --cached --stat | tail -8", "description": "Stage all current work"}`

  ```
M  docs/implantation/bloc-linguistique.md
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/produit/README.md
M  docs/produit/demarrage.md
M  docs/produit/exemples.md
M  journal/2026-11-16/README.md
M  journal/README.md
M  journal/sessions/MANIFEST.md
M  journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
M  journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
A  journal/sessions/session-9e0eeeb8-7572-4a68-a74e-7405d06e3757/digest.md
A  journal/sessions/session-9e0eeeb8-7572-4a68-a74e-7405d06e3757/rapport.md
M  pyproject.toml
M  reports/INDEX.md
M  reports/README.md
A  reports/evaluer-strict.json
M  reports/pensee-coherence-fiches-v7.json
M  reports/pensee-dev-test-v10.json
M  reports/pensee-quatre-modes.json
A  reports/profils.json
M  reports/rapport-audit-v7.md
M  reports/rapport-bloc-linguistique.md
M  reports/rapport-coherence-fiches-v7.md
M  reports/rapport-dev-test-v10.md
A  reports/rapport-evaluer-strict.md
A  reports/rapport-exemples-v2.json
A  reports/rapport-exemples-v2.md
M  reports/rapport-pensee-v12.md
A  reports/rapport-profils.md
M  reports/rapport-roue.md
A  reports/rapport-s-paragraphes.md
M  reports/rapport-spans-chunker.md
M
… [973 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-127", "wait": true, "timeout_ms": 300000}`

  ```
(no new output)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "tail -6 /tmp/porte-produit-v2b.log; cat /tmp/porte-produit-v2b.code", "description": "Read second gate result"}`

  ```
✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
0
  ```

- **bash** `{"command": "git commit -m \"V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE\n\nLes cinq blocs de docs/produit/exemples.md sont rejoués sur le code courant : 3 corrigés\n(qualité → qualite, prédicat →  … [697 caractères tronqués]`

  ```
[s/v7 f0708433] V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
 55 files changed, 14837 insertions(+), 463 deletions(-)
 create mode 100644 journal/2026-11-16/moteur.md
 create mode 100644 journal/sessions/session-9e0eeeb8-7572-4a68-a74e-7405d06e3757/digest.md
 create mode 100644 journal/sessions/session-9e0eeeb8-7572-4a68-a74e-7405d06e3757/rapport.md
 create mode 100644 journal/sessions/session-a5cb52af-8e84-4452-a21e-1bba677dd8e4/digest.md
 create mode 100644 journal/sessions/session-a5cb52af-8e84-4452-a21e-1bba677dd8e4/rapport.md
 create mode 100644 reports/evaluer-strict.json
 create mode 100644 reports/profils.json
 create mode 100644 reports/rapport-evaluer-strict.md
 create mode 100644 reports/rapport-exemples-v2.json
 create mode 100644 reports/rapport-exemples-v2.md
 create mode 100644 reports/rapport-profils.md
 create mode 100644 reports/rapport-s-paragraphes.md
 create mode 100644 tools/construire_profils_udhr.py
 create mode 100644 tools/mesurer_profils.py
 create mode 100644 tools/profils_udhr.py
 create mode 100644 tools/tests/linguistique/gold_reel_50.py
 create mode 
… [402 caractères tronqués]
  ```

- **bash** `{"command": "git status --short | head -40; echo '---'; git log -1 --format='%H %s'", "description": "Check post-commit status"}`

  ```
---
f0708433820f5e43e71004572a909a3830042662 V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py | tail -4; python3 tools/revue_documentation.py 2>&1 | tail -3; python3 tools/taille_documents.py 2>&1 | tail -2", "description": "Post-commit verification", "timeoutMs": 300000}`

  ```
✅ invariants rôles normalisés — 4 rôle(s), tous dans les 8 du vocabulaire
  ✅ invariants durée — absente sans --duree, numérique avec

27/27 cas conformes — ✅ aucun écart
  revue de documentation · 770 fiche(s) · 865 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ❌ 1 violation(s) :
     · reports/README.md : 2817 mots > budget 2800 (T1)
  ```

- **bash** `{"command": "sed -n '1,18p' reports/README.md; wc -w reports/README.md", "description": "Read reports README header"}`

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
2817 reports/README.md
  ```

- **bash** `{"command": "grep -n \"rapport-tagger-lot\" reports/README.md; grep -n \"rapport-exemples-v2\" reports/README.md", "description": "Find long rows"}`

  ```
25:| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (677 textes), **672 appels réseau**, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,8 Mo**, **0,02177 $** ; cache chaud **0 réseau / 0 token / 0 $**, **1 000/1 000 hashes identiques** ; `--jsonl` 1 003 lignes |
34:| [`rapport-exemples-v2.md`](rapport-exemples-v2.md) | **V2/B13** — les 5 exemples rejoués : rôles normalisés, candidats objets, **27/27** cas |
  ```

- **edit** `{"file_path": "reports/README.md", "old_string": "| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (677 textes), **672 appels réseau**, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,8 Mo**, **0,02177 $** ; cache chaud **0 réseau / 0 … [331 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/README.md", "old_string": "| [`rapport-exemples-v2.md`](rapport-exemples-v2.md) | **V2/B13** — les 5 exemples rejoués : rôles normalisés, candidats objets, **27/27** cas |", "new_string": "| [`rapport-exemples-v2.md`](rapport-exemples-v2.md) | **V2/B13** — 5 exemples rejoués,  … [31 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -3", "description": "Check size after trimming", "timeoutMs": 300000}`

  ```
· 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "git add -- reports/README.md && git commit --amend --no-edit && git log -1 --oneline | head -1", "description": "Amend commit with README budget fix", "timeoutMs": 300000}`

  ```
[stderr]
  ❌ commit refusé : 1 fait(s) stagé(s) sans docs/pilotage/en-cours.md
     · reports/README.md
     → mettre l'état à jour, puis `git add docs/pilotage/en-cours.md`
  ⛔ commit refusé : un fait sans ligne d'état.
     mets docs/pilotage/en-cours.md à jour, puis :
     git add docs/pilotage/en-cours.md
[exit code: 1]
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "offset": 1, "limit": 4}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-16 (V2, les exemples de la doc)**
4: 

(Showing lines 1-4 of 143. Use offset=5 to continue.)
</content>
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-16 (V2, les exemples de la doc)**", "new_string": "**Mis à jour : 2026-11-16 (V2, les exemples de la doc ; README des rapports dans le budget)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "git add -- reports/README.md docs/pilotage/en-cours.md && git commit --amend --no-edit && git log -1 --oneline | head -1 && git status --short", "description": "Amend with state line", "timeoutMs": 300000}`

  ```
[s/v7 1a5a6548] V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
 Date: Mon Nov 16 02:47:28 2026 -0500
 55 files changed, 15001 insertions(+), 467 deletions(-)
 create mode 100644 journal/2026-11-16/moteur.md
 create mode 100644 journal/sessions/session-9e0eeeb8-7572-4a68-a74e-7405d06e3757/digest.md
 create mode 100644 journal/sessions/session-9e0eeeb8-7572-4a68-a74e-7405d06e3757/rapport.md
 create mode 100644 journal/sessions/session-a5cb52af-8e84-4452-a21e-1bba677dd8e4/digest.md
 create mode 100644 journal/sessions/session-a5cb52af-8e84-4452-a21e-1bba677dd8e4/rapport.md
 create mode 100644 reports/evaluer-strict.json
 create mode 100644 reports/profils.json
 create mode 100644 reports/rapport-evaluer-strict.md
 create mode 100644 reports/rapport-exemples-v2.json
 create mode 100644 reports/rapport-exemples-v2.md
 create mode 100644 reports/rapport-profils.md
 create mode 100644 reports/rapport-s-paragraphes.md
 create mode 100644 tools/construire_profils_udhr.py
 create mode 100644 tools/mesurer_profils.py
 create mode 100644 tools/profils_udhr.py
 create mode 100644 tools/tests/ling
… [440 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_exemples.py | tail -3; echo '---'; python3 tools/revue_documentation.py 2>&1 | tail -3; echo '---'; python3 tools/taille_documents.py 2>&1 | tail -2; echo '---'; python3 tools/verifie_en_cours.py 2>&1 | tail -2; python3 tools/verifie_journal.py 2>&1 | tail -2", "de … [60 caractères tronqués]`

  ```
✅ invariants durée — absente sans --duree, numérique avec

27/27 cas conformes — ✅ aucun écart
---
  revue de documentation · 770 fiche(s) · 865 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---
  ❌ 1 violation(s) :
     · T0 : 4007 mots (AGENTS + en-cours + une tâche) > budget 4 000
---
  en-cours · 1637 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
  journal · 48 jour(s) · 227 session(s) · 2729 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-16 (V2, les exemples de la doc ; README des rapports dans le budget)**", "new_string": "**Mis à jour : 2026-11-16 (V2)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -2", "description": "Check T0 after shortening", "timeoutMs": 300000}`

  ```
✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "git add -- docs/pilotage/en-cours.md && git commit --amend --no-edit >/tmp/amend.log 2>&1; code=$?; tail -4 /tmp/amend.log; echo \"code=$code\"; git log -1 --oneline | head -1; git status --short", "description": "Amend state line", "timeoutMs": 300000}`
