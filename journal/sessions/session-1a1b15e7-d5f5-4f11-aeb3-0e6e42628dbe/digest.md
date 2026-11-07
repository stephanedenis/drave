# Session DSH — relecture

- identifiant : `session-1a1b15e7-d5f5-4f11-aeb3-0e6e42628dbe`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-07 16:29:22
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J3.1 : le retrieval inter-langues **à époque contrôlée** (l'avertissement de Panini : l'époque domine). Sur le lexique B7 (71 langues) et/ou le corpus commun, mesure le retrieval avec un contrôle de date (couples contemporains vs décalés) et la surface (écriture, famille). Fiche `reports/rapport-retrieval-epoque.md` + JSON, contrôle négatif.

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

- **bash** `{"command": "pwd; ls; echo '---'; ls docs/pilotage/; echo '---'; ls reports/ | head -60", "description": "Explore repository layout"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
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
run_real_clusters.py
run_sparsity.py
run_value_encoding.py
sprints
src
tools
work
---
backlog
chantiers.md
en-cours.md
manques.md
plan-travail.md
programme-r.md
README.md
references-non-regression.md
roadmap.md
semaine-autonome.md
utilisation.md
---
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

… [587 caractères tronqués]
  ```

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --short | head -30; echo '---'; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet log --oneline -8", "description": "Check git status and recent commits"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/references-non-regression.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-07/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89/digest.md
 M journal/sessions/session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89/rapport.md
 M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/superviseur.py
 m tools/structures
?? journal/sessions/session-932afd57-1363-4133-b6f1-64f7d937f38d/
?? reports/corpus-commun.json
?? reports/rapport-corpus-commun.md
?? reports/rapport-s-paragraphes.md
?? tools/corpus_commun.py
---
9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE
8eb0cc49 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTE
… [709 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"J3\" docs/ journal/ reports/ --include=*.md | head -30", "description": "Find J3 references"}`

  ```
docs/pilotage/semaine-autonome.md:91:| **J3 · 09/11** | matin | **Panini II** : le **retrieval à époque contrôlée** | une mesure (double contrôle) |
docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) | la **pragmatique neuronale** ; le **refus r353** ; **J3.1** (retrieval à époque contrôlée) |
docs/pilotage/roadmap.md:253:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitutio
… [8070 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"retrieval\" docs/ reports/ tools/ src/ | head -40; echo '---'; grep -rln \"B7\" docs/ reports/ tools/ src/ | head -40", "description": "Find retrieval and B7 references"}`

  ```
docs/schemas/programme-r-phases.svg
docs/methode/panini-nipada.md
docs/pilotage/backlog/R05-tete-balayage.md
docs/pilotage/backlog/R22-memoire-episodique.md
docs/pilotage/backlog/R51-lecture-croisee.md
docs/pilotage/programme-r.md
docs/pilotage/semaine-autonome.md
docs/pilotage/roadmap.md
docs/theorie/glossaire/README.md
docs/theorie/glossaire/index.json
docs/theorie/synthese/05-la-pensee-sans-verbaliser.md
docs/theorie/synthese/07-modeles-alternatifs-entree-sortie.md
docs/theorie/lecture-rapide.md
reports/archive/rapport-campagne-benefices.md
reports/campagne-benefices/032-29-la-memoire-qui-sert-retrieval-injection.md
reports/pensee-multilingue.json
reports/alignement-3b.json
reports/alignement-7b.json
reports/composition-multilingue.json
reports/composition-verne.json
reports/composition-verne-7b.json
reports/pas-de-pensee.json
reports/pas-de-pensee-7b.json
reports/pas-de-pensee-contracte-3b.json
reports/pas-de-pensee-contracte-7b.json
reports/pas-de-pensee-mlp-18.json
reports/pas-de-pensee-mlp-6.json
reports/composition-verne-14b.json
reports/pas-de-pensee-14b.json
reports/pas-de-pensee-recurrent.json
reports/composition-latente-3b.json
reports/composition-latente-7b.json
report
… [1789 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' docs/methode/panini-nipada.md", "description": "Read Panini-Nipada method doc"}`

  ```
# Étudier Panini et Nipada, régulièrement

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **à chaque cycle**, avant de conclure sur
> la généalogie, les styles ou les familles de langues.

## Pourquoi

Les projets **`../Panini/`** et **`../Panini-Research/`** poursuivent le **même objectif par une approche
complémentaire** : Panini décompose le texte en **14 atomes sémantiques**, Nipada le fait tourner comme un tissu
computationnel — *algébrique, là où Drave est statistique*. Ils tiennent le **système linguistique** et généralisent
une **généalogie des langues, dialectes et styles**.

## La règle

À chaque cycle, **lire ce qui a bougé chez eux** (docs, publications, journaux de bord, `git log`) et **confronter
leurs résultats aux nôtres**. Ce qui en sort va dans [`docs/theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md)
(la théorie) — **jamais les chiffres** (ils vont dans `reports/`).

## Leur avertissement, à ne pas oublier ✗✓

Leur signature lexicale capte **l'époque** (β **+0,138**) bien plus que la **filiation** (β **+0,049**) — *la
surface transmet les signifiants, pas la généalogie*.

Conséquences pour nos tests :

- tout test
… [623 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,120p' docs/pilotage/semaine-autonome.md", "description": "Read J3 week plan"}`

  ```
| # | intégration | livrable | contrôle négatif | risque |
|---|---|---|---|---|
| 1 | **UDHR + généalogie** (même source XML des deux côtés) | table iso3/famille/branche + échantillon 20 langues | familles différentes = retrieval faible ; sœurs = fort | codes ISO (007/008 vs iso3) |
| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |
| 3 | **corpus d'or CIC** (42 verdicts, preuve + sha256) | vérificateur indépendant, 42/42 | altérer un octet doit être rejeté | aucun (le plus vérifiable) |

**Trop immature pour la semaine** : le produit NIPADA, le noyau comme service, les 11 modules,
Panini-FS, l'API REST.

### 2.4 La surface d'intégration

| Panini / NIPADA apporte | Drave apporte | premier livrable commun |
|---|---|---|
| les **14 atomes**, les universaux | nos **niveaux** (POS, syntagmes, pragmatique) et leurs mesures | une **table de correspondance** atomes ↔ niveaux, sur un corpus commun |
| les **corpus** (Gutenberg, UDHR) et leur découpage | le **retrieval** inter-langues (mesures 49) | une mesure de retrieval **à époque contrôlée** |
| la 
… [3064 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"B7\\|71\\|retrieval\\|époque\\|date\" docs/theorie/jeux-symboliques.md | head -40; echo '==='; wc -l docs/theorie/jeux-symboliques.md reports/rapport-langues-maitres.md reports/rapport-multilingue.md reports/rapport-corpus-commun.md", "description": "Search B7 in jeu symboliqu … [7 caractères tronqués]`

  ```
69:| **2** | lexique | synonymes et langues (FR/EN, puis **71 langues** pour les mots-clés) | `Cf3`, « cavalier de g1 vers f3 », « as de cœur », `конь g1 f3`, `馬 g1 f3` |
129:## Les langues et les maîtres (B7/B8)
131:Le **lexique multilingue** (35 concepts, 71 langues, construit depuis Wikidata CC0) et le **corpus de 449
148:  71 langues couvrent les **mots-clés**, pas la grammaire. Cinq langues n'ont aucun item naturel ; la notation
168:| [`tools/jeux/lexique_multilingue.py`](../../tools/jeux/lexique_multilingue.py) | le lexique 71 langues (Wikidata) et sa recherche |
177:| [`tools/jeux/mesure_langues.py`](../../tools/jeux/mesure_langues.py) | la couverture et les contrôles des 71 langues |
===
  182 docs/theorie/jeux-symboliques.md
  226 reports/rapport-langues-maitres.md
   63 reports/rapport-multilingue.md
  330 reports/rapport-corpus-commun.md
  801 total
  ```

- **bash** `{"command": "sed -n '1,160p' reports/rapport-corpus-commun.md", "description": "Read corpus commun report"}`

  ```
# Corpus commun Panini/NIPADA ↔ Drave — UDHR, article 1

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.2 · **Date** : 2026-11-07
> **Verdict** : ✅ **le corpus est construit et vérifié** — **21 textes** (20 langues stratifiées + le
> français pivot), **5 familles**, **10 écritures**, **42 phrases**, **3 603 caractères**. Les **21**
> paires Panini ↔ Drave sont **identiques après normalisation** ; **418 paires exactes** sur **438**
> appariables (**95,4 %**). **20 écarts de surface** sont **exclus, pas corrigés**. Les **8 contrôles**
> (**6 rejets** attendus + **2 témoins** d'acceptation) sont **conformes** (8/8).
> **Dispositif** : lecture seule de `../Panini/research/data/udhr_corpus.json` (HEAD du dépôt
> `e10d695`, 2026-10-25 ; fichier **non suivi par git**, SHA-256 `531bc75c…`, vérifié avant et
> après) ; `data/udhr/articles_propres.jsonl`, `langues.jsonl`, `genealogie.json` (HEAD
> `9c7f71dc`, 2026-11-07) ; outil `../tools/corpus_commun.py` ;
> JSON [`corpus-commun.json`](corpus-commun.json). Le corpus lui-même vit dans
> `work/corpus-commun/`, **non versionné** (`.gitignore` : `work/`).
> **Aucune écriture dans Panini** : le script vérifie 
… [8885 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,182p' docs/theorie/jeux-symboliques.md; echo '==='; ls tools/jeux/; echo '==='; ls data/ | head -40", "description": "Read B7 section and tools"}`

  ```
- **perturbation** : changer un champ sémantique doit changer l'empreinte après rendu/relu ;
- **permutation du lexique** : permuter les concepts doit faire **chuter** la couverture des phrases — sinon
  le lexique n'était pas utilisé ;
- **étiquettes mélangées** : mélanger les attendus doit faire tomber la couverture au hasard ;
- **règles** : perft des échecs (six positions), perft des dames (1→6), captures, suicide, ko, score ;
- **pensée** : le morpion exact ne perd pas contre le hasard, les mats en un sont trouvés, la recherche des
  dames gagne contre le joueur sans recherche, la politique des cartes bat le hasard, et les cinq jeux
  donnent la **même décision** sur des surfaces différentes.

## Les langues et les maîtres (B7/B8)

Le **lexique multilingue** (35 concepts, 71 langues, construit depuis Wikidata CC0) et le **corpus de 449
surfaces** sont mesurés : lecture au niveau 4, paires inter-langues invariantes, notation indépendante de la
langue, noms de jeux détectés. Les **maîtres** (17 principes, 9 sources du domaine public, 3 parties) changent
l'ouverture des échecs, tiennent le livre, gagnent au go 9×9 et ne perdent pas aux dames ; l'accord avec le coup
du maître ne b
… [4943 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-langues-maitres.md", "description": "Read languages report"}`

  ```
# B7/B8 — 71 langues pour les jeux, et les livres des maîtres mesurés

> Mesure du **26/10/2026**, sur `Hauru` (Python 3.13, sans GPU), `tools/jeux/` et
> `tools/porte-jeux.sh`. Deux extensions de B5/B6 : un **lexique multilingue** de 35 concepts dans
> **71 langues** (Wikidata, CC0) et une **base de 17 principes** tirés de neuf sources (sept ouvrages du
> domaine public, les proverbes traditionnels du go, le morpion résolu), avec leurs évaluations, leur livre,
> leurs parties et leurs politiques. JSON bruts :
> [`jeux-langues-mesures.json`](jeux-langues-mesures.json) et
> [`jeux-maitres-mesures.json`](jeux-maitres-mesures.json). Concept :
> [`docs/theorie/jeux-symboliques.md`](../docs/theorie/jeux-symboliques.md). Durées : **3,1 s** (langues), **468,8 s**
> (maîtres), **188,7 s** (jeux, régénéré avec le lexique Unicode).

## Ce qui est mesuré

1. **Les langues** — le même sens (pièce + cases, rang + enseigne, nom du jeu + coordonnée) dans 71 langues ;
   couverture du corpus au niveau 4, invariance inter-langues, contrôle par permutation des libellés,
   notation indépendante de la langue, détection des noms de jeux.
2. **Les maîtres** — 17 principes encodés dans la pensée, et ce 
… [5148 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='tools/jeux/lexique_multilingue.json'\nd=json.load(open(p))\nprint(type(d), list(d)[:10] if isinstance(d,dict) else len(d))\nprint(json.dumps(d, ensure_ascii=False)[:1500])\nEOF", "description": "Inspect lexicon JSON structure"}`

  ```
<class 'dict'> ['version', 'source', 'date', 'langues', 'variantes', 'concepts', 'manuel']
{"version": 1, "source": "Wikidata (CC0), wbgetentities props=labels ; pageprops Wikipédia pour les QID ; libellés normalisés (NFKC, casse pliée, accents retirés, parenthèses retirées)", "date": "2026-10-26", "langues": ["ar", "bn", "ca", "cs", "da", "de", "el", "en", "eo", "es", "et", "eu", "fa", "fi", "fr", "gl", "he", "hi", "hr", "hu", "id", "is", "it", "ja", "ka", "kk", "ko", "lt", "lv", "mk", "ms", "mt", "nb", "nl", "nn", "pl", "pt", "ro", "ru", "sk", "sl", "sq", "sr", "sv", "sw", "ta", "th", "tr", "uk", "ur", "vi", "zh", "af", "am", "az", "be", "bs", "cy", "ga", "hy", "km", "ky", "lo", "mn", "ne", "pa", "si", "so", "uz", "yo", "zu"], "variantes": {"zh": ["zh-hans", "zh-cn", "zh-sg", "zh-hant"], "pt": ["pt-br"], "sr": ["sr-ec", "sr-el"]}, "concepts": {"jeu.morpion": {"qid": "Q210339", "qids": ["Q210339"], "labels": {"ar": ["لعبة اكس-او"], "ca": ["tres en ratlla"], "cs": ["piskvorky"], "da": ["kryds og bolle"], "de": ["tic-tac-toe"], "en": ["tic-tac-toe"], "eo": ["tiktakto"], "es": ["tres en raya"], "et": ["trips-traps-trull"], "eu": ["hiruko artzain-joko"], "fa": ["ایکس او"], "fi": ["ris
… [391 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/jeux/lexique_multilingue.py", "description": "Read lexicon module"}`

  ```
#!/usr/bin/env python3
"""lexique_multilingue.py — les libellés des jeux, en 53 langues.

Le fichier `lexique_multilingue.json` (construit par
`construire_lexique_multilingue.py`) porte les libellés **normalisés** de
35 concepts : noms des cinq jeux, pièces des échecs, rangs et enseignes des
cartes, couleurs, notions de maîtres. Ce module les charge et les rend
cherchables par **domaine** :

    MULTI.cherche("echecs.piece", "король g1 f3")
    MULTI.cherche("cartes.couleur", "ملك القلوب")

La recherche est **multi-formes** : n-grammes de 1 à 4 unités pour les langues à
espaces, et sous-chaîne pour les écritures qui n'en mettent pas (CJK, thaï). Le
libellé est comparé sous sa forme normalisée (`normalise_forme`), la même que
celle du constructeur : NFKC, casse pliée, diacritiques optionnels retirés,
parenthèses de désambiguïsation ôtées.

Ce module ne **devine** pas la langue d'un texte : il compte les libellés
reconnus et rend la langue la plus probable (`detecte_langue`). C'est une
mesure, pas une certitude ; la fiche donne le taux.
"""
from __future__ import annotations

import json
import pathlib
from collections import Counter, defaultdict
from dataclasses import dataclass

fr
… [3679 caractères tronqués]
  ```

- **bash** `{"command": "ls ..; echo '==='; ls ../Panini 2>/dev/null | head; echo '==='; ls ../Panini-Research 2>/dev/null | head; echo '==='; find ../Panini ../Panini-Research -maxdepth 3 -iname '*corpus*' 2>/dev/null | head -30", "description": "Inspect Panini sibling repos"}`

  ```
915-SPO (1).com
915-SPO.com
915-SPO.com-2
Ai_Docs
arduino-i2c-scanner
Arduino-IRremote
ArduinoNunchuk
Biblio
Biblio-2
blue-pill-quickstart
bohemian-lab
consolider_panini_research.sh
contcal
copilotage
copilotage-shared
DeDRM_tools
drave-structures
emails
equipement-kindle
equipment-cam-IP-PTZ
equipment-dvr-coax
equipment-hauru
equipment-kamaji
equipment-mystery
equipment-ponyo
equipment-radio
equipment-remarkable
equipment-router
equipment-totoro
ESP32-CAM-Experiments
ESP-Experiments
financemeteo
FPGA-Stratix-V
GitHub-Centralized
gods-eye-view
hauru-top
jtag-mpsse-blaster
jtag-quartus-ft232h
linux_signing_key.pub
llama.cpp
llama.cpp-k3
MyKindleContent
nipada-public
OntoWave
Panini
Panini-AttributionRegistry
Panini-AutonomousMissions
Panini-CloudOrchestrator
Panini-CoLabController
Panini-CopilotageShared
Panini-DatasetsIngestion
Panini-ExecutionOrchestrator
Panini-FS
Panini-PublicationEngine
Panini-Research
Panini-SemanticCore
Panini-SpecKit-Shared
Panini-UltraReactive
Pensine
Pensine-GouvQc
Pensine-Personnel
pensine-plugin-calendar
pensine-plugin-inbox
pensine-plugin-journal
pensine-plugin-reflection
pensine-plus
Pensine-StephaneDenis
pensine-web
pp-sp-reference-design
Qtrinet
rm-a
… [1874 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"époque\\|epoque\\|date\\|siècle\\|siecle\" docs/theorie/genealogie-des-langues.md | head -40; echo '==='; sed -n '1,80p' docs/theorie/genealogie-des-langues.md", "description": "Read genealogy doc for epoch"}`

  ```
23:| **style / époque** | baroque, classique, technique, traduit | le registre, la syntaxe, le vocabulaire |
39:| **époque** (années) | **+0,138** | **dominant** |
43:*Leur conclusion : **la signature de surface capte l'époque, pas la filiation*** ✗✓ — « l'héritage transmet les
45:les atomes, pour supprimer le confondant langue/époque.
49:1. **contrôler l'époque** ✗✓ : un « style » mesuré sur deux traductions d'âges différents peut être de l'**époque**,
50:   pas du traducteur. Tout test de style doit apparier les dates, ou les déclarer.
55:   l'époque.
70:  l'alignement et l'époque* ✗✓.
73:de référence — et **organiser les tests par niveau**, en contrôlant l'époque. C'est ce qui manque pour dire que la
===
# La généalogie des langues, des dialectes et des styles

> **Ce que cette page est.** La **théorie** de la structure généalogique qui doit organiser l'**étage entrée-sortie** (nom historique : « couche commune »)
> entrée-sortie de Drave, et ce que les projets complémentaires **Panini** et **Nipada** ont établi sur elle. Les
> mesures de Drave sont dans [`reports/07-mesures-couche-commune.md`](../../reports/07-mesures-couche-commune.md).
> *À relire et à mettre à jour à chaque 
… [4350 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"retrieval\\|retrouv\\|mesure 49\\|49 \" reports/07-mesures-couche-commune.md | head -30; echo '==='; grep -rln \"retrieval\" tools/ src/ drave-core/ | head -20", "description": "Find retrieval measure implementation"}`

  ```
29:| [**3**](07/p3.md) | « Trente-et-unième mesure (17/10, 20 h 15) : l'hypothèse « récit contr… » | « Mesure 49 — l'alignement suit la GÉNÉALOGIE des langues… » | 23 | 586 |
35:| [**9**](07/p9.md) | « Mesure 131 — LE PONT EST **LANGUE-GÉNÉRAL** (4 LANGUES) : FR/DE donn… » | « Mesure 149 — LE CONTRÔLE DU CONTRASTE : avec des paires **mélangées*… » | 19 | 602 |
===
tools/__pycache__/retrieval_parallele.cpython-313.pyc
tools/__pycache__/udhr_commun.cpython-313.pyc
tools/__pycache__/style_traducteur.cpython-313.pyc
tools/__pycache__/retrieval_udhr.cpython-313.pyc
tools/__pycache__/pensee_multilingue.cpython-313.pyc
tools/__pycache__/composition_multilingue.cpython-313.pyc
tools/__pycache__/traduire_bench.cpython-313.pyc
tools/__pycache__/composition_latente.cpython-313.pyc
tools/__pycache__/composition_verne.cpython-313.pyc
tools/__pycache__/pas_de_pensee.cpython-313.pyc
tools/__pycache__/pas_de_pensee_mlp.cpython-313.pyc
tools/__pycache__/pas_de_pensee_contracte.cpython-313.pyc
tools/__pycache__/pas_de_pensee_recurrent.cpython-313.pyc
tools/__pycache__/pas_de_pensee_non_lineaire.cpython-313.pyc
tools/__pycache__/pas_de_pensee_corrige.cpython-313.pyc
tools/__pycache__/etat_de_plan.cpy
… [212 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"def .*retriev\\|retrieval\\|retrouve\" tools/ src/ drave-core/ --include=*.py | head -30", "description": "Search retrieval code"}`

  ```
tools/mla_synthetique.py:8:indépendante en numpy — c'est elle que le moteur devra retrouver.
tools/energie_du_contenu.py:2:"""energie_du_contenu.py — peut-on retrouver l'ÉNERGIE de contenu, pas seulement son rapport ?
tools/peripherie_memoire.py:4:LA QUESTION, ET ELLE EST PRÉCISE. La lecture LINÉAIRE de l'état de sortie ne retrouve pas le
tools/audit_drapeaux_harnais.py:13:drapeau dont l'effet ne se retrouve pas dans le fichier est un drapeau qui ne s'applique pas — et
tools/audit_drapeaux_harnais.py:162:        print("Un drapeau dont l'effet ne se retrouve pas dans le fichier ne s'applique pas — ou ne")
tools/memoire_travail.py:6:non linéaire — retrouve le signal **courant** (R² **+0,992**) mais **pas** celui d'il y a 8 pas
tools/memoire_travail.py:24:  * **contrôle** : cibles de la mémoire **mélangées** — une sonde qui « retrouve » un signal
tools/releve_parametre.py:15:Si le rang-1 retrouve l'essentiel de l'écart ✓✓ → **la langue est un paramètre de rang 1** ✓✓, et le « relevé
tools/retrieval_parallele.py:2:"""retrieval_parallele.py — LE MÊME SENS DANS DEUX LANGUES : les états se RESSEMBLENT-ILS ?
tools/retrieval_parallele.py:8:LE DISPOSITIF (retrieval croisé ✓). On prend un liv
… [2184 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' tools/style_traducteur.py", "description": "Read style/translator retrieval tool"}`

  ```
#!/usr/bin/env python3
"""style_traducteur.py — LE STYLE DU TRADUCTEUR EST-IL LISIBLE ? ET LE SENS SURVIT-IL AU STYLE ?

LA TROISIÈME DISTINCTION DE LA SÉRIE ✓✓, après les langues (448 ✓) et les variantes (7 ✓) : **le style** ✗✓.
Deux **traductions anglaises de la MÊME œuvre** (L'Odyssée : Samuel Butler ✓ et Alexander Pope ✓) partagent la
langue et le contenu ✓ — elles ne diffèrent que par le **style du traducteur** ✓✓. C'est le dispositif le plus
propre pour cette question ✓.

TROIS MESURES DANS LE MÊME OUTIL ✗ :
  · **le style est-il lisible ?** ✓ : un classifieur binaire (traducteur A contre B), entraîné sur la moitié des
    segments, testé sur l'autre moitié ✓✓ — hasard 50 % ✓ ;
  · **le sens survit-il au style ?** ✓✓ : le segment *i* de A se retrouve-t-il dans B ? ✓ (retrieval, hasard
    1/N ✓) — c'est la **traduction** au sens de « même contenu, autre surface » ✓ ;
  · **le contrôle négatif** ✓✓ : étiquettes mélangées (le style doit retomber à 50 %) et segments mélangés (le
    retrieval doit retomber au hasard ✓).

⚠️ CE QU'IL NE DIT PAS ✗ : la découpe est **proportionnelle** ✓✗ (comme pour Verne le 17/10 ✓) — deux éditions
peuvent dériver ✓ ; on le verra au retrieval ✓. E
… [4584 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/retrieval_udhr.py", "description": "Read UDHR retrieval tool"}`

  ```
#!/usr/bin/env python3
"""retrieval_udhr.py — LA TRADUCTION : LE MÊME ARTICLE SE RETROUVE-T-IL D'UNE LANGUE À L'AUTRE ?

LA MESURE DE « TRADUCTION » DE CETTE SÉRIE ✓✓. Les 30 articles de la Déclaration sont **alignés** ✓ : l'article 7
dit la même chose dans toutes les langues ✓✓. On demande donc au modèle : *pour l'état de l'article 7 en français,
quel article de la liste anglaise est le plus proche ?* ✓ Si c'est **l'article 7** ✓✓, l'état porte le **sens**
d'une langue à l'autre ✓ — c'est exactement la couche commune en traduction ✓.

TROIS DISPOSITIFS DANS LE MÊME OUTIL ✗ :
  · `--mode paires`    : un jeu de paires représentatives (même famille, familles différentes, écritures
    différentes ✓) — la question « le sens traverse-t-il la frontière des langues ? » ✓ ;
  · `--mode variantes` : les variantes d'une **même** langue ✗✓ (occitan 7, romanche 7, houndé 3, roumain 3 ✓) —
    c'est le test « **dialectes et styles** » ✓✓ : le même sens, deux traductions, la même langue ✓ ;
  · `--mode temoin`    : le **contrôle négatif** ✓✓ — on mélange les articles d'une langue et on refait la mesure ✓ ;
    il **doit** retomber au hasard ✓ (3,3 %) ✗ — sinon, c'est que la mesure ne mesure rie
… [5361 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"0.138\\|0,138\\|signature lexicale\\|signature_lexicale\" ../Panini ../Panini-Research 2>/dev/null | head -20", "description": "Find Panini signature analysis"}`

  ```
../Panini/.git/COMMIT_EDITMSG
../Panini/.git/modules/research/index
../Panini/data/gutenberg_multilingual_verified/multilingual_dhatu_cycle_results.json
../Panini/data/monitoring_data_realtime.json
../Panini/data/panini_high_performance_report_20250920_154356.json
../Panini/data/panini_high_performance_report_20250920_173923.json
../Panini/data/panini_high_performance_report_20250921_004756.json
../Panini/data/panini_high_performance_report_20250921_005325.json
../Panini/docs/panini/publications/exports/corpus_dhatu_complet_universel.pdf
../Panini/docs/panini/references/cache/DN06011FU1.pdf
../Panini/docs/panini/references/cache/brown_2020_gpt3_language_models_few_shot.pdf
../Panini/docs/panini/references/cache/deletang_2024_language_modeling_is_compression.pdf
../Panini/docs/panini/references/cache/entropy_semantic_compression_2509.00503.pdf
../Panini/docs/panini/references/cache/gpt_compression_kolmogorov_2308.06942.pdf
../Panini/docs/panini/references/cache/mikolov_2013_word2vec_efficient_estimation.pdf
../Panini/docs/panini/references/cache/quantum_semantic_framework_2506.10077.pdf
../Panini/docs/panini/references/cache/semantic_token_2508.15190.pdf
../Panini/docs/panini/refere
… [421 caractères tronqués]
  ```

- **bash** `{"command": "find ../Panini ../Panini-Research -maxdepth 4 -type f \\( -name '*.json' -o -name '*.jsonl' -o -name '*.csv' \\) 2>/dev/null | grep -iE 'philo|hist|corpus|text|era|date' | head -40", "description": "Find dated corpora in Panini"}`

  ```
../Panini/data/acceleration_config.json
../Panini/data/analyse_litterature_pertinente.json
../Panini/data/audit_corpus_planification_extension.json
../Panini/data/contraintes_operateurs_naires.json
../Panini/data/gutenberg_corpus/collection_metadata.json
../Panini/data/gutenberg_direct_corpus/direct_collection_metadata.json
../Panini/data/gutenberg_massive_corpus/direct_collection_metadata.json
../Panini/data/gutenberg_multilingual_corpus/multilingual_metadata.json
../Panini/data/gutenberg_smart_corpus/smart_collection_metadata.json
../Panini/data/incremental_corpus/collection_stats_20250922_225818.json
../Panini/data/incremental_corpus/collection_stats_20250922_231427.json
../Panini/data/incremental_corpus/collector_optimization.json
../Panini/data/incremental_corpus/fast_batch_20250922_231522.json
../Panini/data/incremental_corpus/fast_batch_20250922_231530.json
../Panini/data/incremental_corpus/fast_batch_20250922_231538.json
../Panini/data/incremental_corpus/fast_batch_20250922_231547.json
../Panini/data/incremental_corpus/fast_batch_20250922_231555.json
../Panini/data/incremental_corpus/fast_batch_20250922_231710.json
../Panini/data/incremental_corpus/fast_batch_20250922_23171
… [1485 caractères tronqués]
  ```

- **bash** `{"command": "ls data/alignement | head; echo '==='; ls work/ | head -30; echo '==='; ls work/corpus-commun 2>/dev/null | head; echo '==='; find . -maxdepth 3 -iname '*odys*' -o -iname '*butler*' -o -iname '*pope*' 2>/dev/null | head", "description": "Inspect alignment and work dirs"}`

  ```
verne_fr_en.json
===
attente_portes.sh
chantier
corpus-commun
corpus-wiki-langues.log
corpus-wiki.log
corpus-wiki-reste.log
dr
entete-references.txt
finaliser_ocr.py
hub-nuit.md
maj_references2.py
maj_references3.py
maj_references.py
maj_table_seule.py
msg-1335.txt
msg-80-2.txt
msg-backlog-n2.txt
msg-bilan.txt
msg-claims.txt
msg-cle2.txt
msg-cle3.txt
msg-cle.txt
msg-cpt.txt
msg-etat.txt
msg-homeo2.txt
msg-homeo.txt
msg-j2.txt
msg-jour.txt
msg-n2-sed.txt
msg-n2-sous25.txt
===
controle-negatif.json
corpus.jsonl
index.json
metadata.tsv
README.md
sources.sha256
textes
===
  ```

- **bash** `{"command": "find data -maxdepth 2 -type d | head -40; echo '==='; ls data/udhr | head", "description": "List data directories"}`

  ```
data
data/udhr
data/udhr/familles
data/glottolog
data/eurlex
data/eurlex/xhtml
data/alignement
data/presse
data/presse/api
data/onu
data/onu/pdf
data/onu/docx
data/jw
data/jw/html
data/pidgin.old
data/pidgin.old/html
data/raisonnement
data/ted2020
data/wikimatrix
data/opensubtitles
data/adaptateurs
data/adaptateurs/bilingue-1600
data/adaptateurs/plan-bilingue-800
data/adaptateurs/plan-contraste-800
data/adaptateurs/plan-contraste-plein-800
data/adaptateurs/plan-recurrent-800
data/adaptateurs/plan-multi-tache-800
data/jrc
data/xnli
data/xnli/XNLI-1.0
data/xnli/__MACOSX
data/xnli/XNLI-MT-1.0
data/multiun
data/diabla
data/diabla/raw
data/daccord
data/deepseek
data/deepseek/cache
data/deepseek/distillation
data/deepseek/distillation-controle
===
articles.jsonl
articles_propres.jsonl
_eng.txt
familles
_fra.txt
genealogie.json
langues.jsonl
meta.json
udhr_10_train.txt
udhr_10_val.txt
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,os\nfor p in ['../Panini/data/gutenberg_multilingual_corpus/multilingual_metadata.json','../Panini/data/gutenberg_corpus/collection_metadata.json']:\n    try:\n        d=json.load(open(p))\n        print('==',p,type(d))\n        if isinstance(d,dict):\n    … [273 caractères tronqués]`

  ```
== ../Panini/data/gutenberg_multilingual_corpus/multilingual_metadata.json <class 'dict'>
['alice_wonderland', 'around_world_80_days', 'frankenstein', 'dracula', 'pride_prejudice', 'metamorphosis']
{"alice_wonderland": {"title": "Alice's Adventures in Wonderland", "author": "Lewis Carroll", "original_lang": "en", "versions": {"en": {"gutenberg_id": "11", "url": "https://www.gutenberg.org/files/11/11-0.txt", "file_path": "data/gutenberg_multilingual_corpus/alice_wonderland/alice_wonderland_en.txt", "content_length": 144696, "download_success": true}, "fr": {"gutenberg_id": "55456", "url": "https://www.gutenberg.org/files/55456/55456-0.txt", "file_path": "data/gutenberg_multilingual_corpus/alice_wonderland/alice_wonderland_fr.txt", "content_length": 160824, "download_success": true}, "de": {"gutenberg_id": "19778", "url": "https://www.gutenberg.org/files/19778/19778-0.txt", "download_success": false, "error": "404 Client Error: Not Found for url: https://www.gutenberg.org/files/19778/19778-0.txt"}, "es": {"gutenberg_id": "28885", "url": "https://www.gutenberg.org/files/28885/28885-0.txt", "download_success": false, "error": "404 Client Error: Not Found for url: https://www.gutenberg.
… [1563 caractères tronqués]
  ```

- **bash** `{"command": "ls ../Panini/data/gutenberg_multilingual_corpus | head -20; echo '==='; du -sh ../Panini/data/gutenberg_multilingual_corpus 2>/dev/null; echo '==='; ls data/eurlex | head; echo '==='; ls data/multiun | head", "description": "Inspect multilingual corpus dirs"}`

  ```
alice_wonderland
around_world_80_days
dracula
frankenstein
metamorphosis
multilingual_metadata.json
pride_prejudice
===
4,3M	../Panini/data/gutenberg_multilingual_corpus
===
32025R1106-24.json
32025R1106-8.json
32025R1106.json
32025R2509.json
xhtml
===
en-fr.tmx.gz
multiun_tech_fr_en.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/data/gutenberg_multilingual_corpus/multilingual_metadata.json'))\nfor k,v in d.items():\n    print('##',k,v['title'],v.get('author'),v.get('original_lang'))\n    for lang,ver in v['versions'].items():\n        print('  ',lang,v … [163 caractères tronqués]`

  ```
## alice_wonderland Alice's Adventures in Wonderland Lewis Carroll en
   en 11 True 144696 data/gutenberg_multilingual_corpus/alice_wonderland/alice_wonderland_en.txt
   fr 55456 True 160824 data/gutenberg_multilingual_corpus/alice_wonderland/alice_wonderland_fr.txt
   de 19778 False None 
   es 28885 False None 
   it 28371 False None 
## around_world_80_days Around the World in Eighty Days Jules Verne en
   en 103 True 377221 data/gutenberg_multilingual_corpus/around_world_80_days/around_world_80_days_en.txt
   fr 800 False None 
   de 37761 False None 
   es 103 True 396770 data/gutenberg_multilingual_corpus/around_world_80_days/around_world_80_days_es.txt
## frankenstein Frankenstein Mary Shelley en
   en 84 True 419434 data/gutenberg_multilingual_corpus/frankenstein/frankenstein_en.txt
   fr 17989 False None 
   de 46762 True 340532 data/gutenberg_multilingual_corpus/frankenstein/frankenstein_de.txt
   es 21295 False None 
## dracula Dracula Bram Stoker en
   en 345 True 861499 data/gutenberg_multilingual_corpus/dracula/dracula_en.txt
   fr 31311 True 87695 data/gutenberg_multilingual_corpus/dracula/dracula_fr.txt
   de 31284 False None 
## pride_prejudice Pride and Prejudice 
… [416 caractères tronqués]
  ```

- **bash** `{"command": "ls data/jw | head; echo '==='; find data/jw -maxdepth 2 -type f | head -20; echo '==='; ls data/presse | head; echo '==='; ls data/ted2020 | head; echo '==='; ls data/opensubtitles | head", "description": "Inspect JW and other corpora"}`

  ```
html
jw_2026.json
===
data/jw/html/https_www_jw_org_en_library_magazines_watchtower_study_august_2026_An_Appeal_on_the_Basis_of_Love_.html
data/jw/html/B0_E0_A4_95_E0_A5_80_E0_A4_97_E0_A4_AF_E0_A5_80_E0_A4_97_E0_A5_81_E0_A4_9C_E0_A4_BC_E0_A4_BE_E0_A4_B0_E0_A4_BF_E0_A4_B6_.html
data/jw/html/B0_E0_A6_A3_E0_A7_87_E0_A6_95_E0_A6_B0_E0_A6_BE_E0_A6_8F_E0_A6_95_E0_A6_85_E0_A6_A8_E0_A7_81_E0_A6_B0_E0_A7_8B_E0_A6_A7_.html
data/jw/html/https_www_jw_org_id_perpustakaan_majalah_menara_pengawal_pelajaran_agustus_2026_Permohonan_atas_Dasar_Kasih_.html
data/jw/html/D8_A8_D8_AA_DA_A9_DB_8C_D8_A8_D9_90_D9_86_D8_A7_D9_BE_D8_B1_D8_A7_DB_8C_DA_A9_D8_AF_D8_B1_D8_AE_D9_88_D8_A7_D8_B3_D8_AA_.html
data/jw/html/A9_B6_E7_94_A8_2026_E5_B9_B48_E6_9C_88_E6_84_9B_E3_81_AB_E5_9F_BA_E3_81_A5_E3_81_84_E3_81_9F_E3_81_8A_E9_A1_98_E3_81_84_.html
data/jw/html/B5_E0_A4_B0_E0_A4_95_E0_A5_87_E0_A4_B2_E0_A5_87_E0_A4_B2_E0_A5_80_E0_A4_B5_E0_A4_BF_E0_A4_A8_E0_A4_82_E0_A4_A4_E0_A5_80_.html
data/jw/html/9A_E0_B1_87_E0_B0_B8_E0_B0_BF_E0_B0_A8_E0_B0_92_E0_B0_95_E0_B0_B5_E0_B0_BF_E0_B0_A8_E0_B1_8D_E0_B0_A8_E0_B0_AA_E0_B0_82_.html
data/jw/html/ap_chi_thap_canh_hoc_hoi_thang8_2026_L_E1_BB_9Di_n_C3_A0i_xin_d_E1_BB_B1a_tr_C3_AAn_t_C
… [1646 caractères tronqués]
  ```

- **bash** `{"command": "ls data/xnli; echo '==='; ls data/wikimatrix | head; echo '==='; ls data/glottolog; echo '==='; python3 - <<'EOF'\nimport json\nd=json.load(open('data/udhr/genealogie.json'))\nk=list(d)[:2]\nprint(k)\nfor kk in k: print(kk, json.dumps(d[kk],ensure_ascii=False)[:500])\nEOF", "description … [41 caractères tronqués]`

  ```
__MACOSX
XNLI-1.0
XNLI-1.0.zip
XNLI-MT-1.0
XNLI-MT-1.0.zip
===
en-fr.tmx.gz
wikimatrix_fr_en.json
===
languages.csv
values.csv
===
['udhr_007.xml', 'udhr_008.xml']
udhr_007.xml {"iso3": "cri", "nom": "Sãotomense", "script": "Latn", "famille": "Indo-European", "branche": "indo1319/clas1257/ital1284/lati1262/lati1263/impe1234/roma1334/ital1285/west2813/shif1234/sout3183/west2838/gali1263/macr1272/lowe1440/bant1299/saot1242", "niveau": "language"}
udhr_008.xml {"iso3": "pov", "nom": "Crioulo, Upper Guinea (008)", "script": "Latn", "famille": "Indo-European", "branche": "indo1319/clas1257/ital1284/lati1262/lati1263/impe1234/roma1334/ital1285/west2813/shif1234/sout3183/west2838/gali1263/macr1272/uppe1458", "niveau": "language"}
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-multilingue.md", "description": "Read multilingual report"}`

  ```
# B15 — M1 sur 66 langues : invariance et exactitude

> **Objet.** Mesurer le codec M1 sur le corpus multilingue existant, par langue et par jeu, avec
> une baseline de surface et un contrôle de surface permutée. **Couche lexicale** : les surfaces
> B7 sont « libellé + coordonnée » ; la réussite mesure la reconnaissance lexicale, pas la
> compréhension d'une phrase libre.

## Corpus

| source | coups | langues | paires |
|---|---:|---:|---:|
| B5 | 79 | 2 (en, fr) + notation | 19 |
| B7 | 449 | 66 | 11 |
| total | **528** | **66** | **30** |

- **71 langues** au lexique, **66** présentes dans le corpus ; absentes : **ky, lo, mt, si, yo**.
- **26 paires multi-variantes**, **15 paires interlangues**.
- 5 langues à **n=1** (am, km, pa, so, zu) : un taux de 0 ou 100 % sur un seul item n'est pas une estimation.

## Résultats globaux

| mesure | valeur |
|---|---:|
| exact avec contexte | **528 / 528 = 100 %** |
| exact sans contexte | **374 / 528 = 70,8 %** |
| canonique | **528 / 528 = 100 %** |
| invariance toutes variantes (contexte) | **26 / 26 = 100 %** |
| invariance interlangues (contexte) | **15 / 15 = 100 %** |
| invariance toutes variantes (sans contexte) | **21 / 26 = 80,8 %*
… [1615 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,100p' reports/rapport-pensee-multilingue.md 2>/dev/null || ls reports | grep -i multiling", "description": "Read thought multilingual report"}`

  ```
composition-multilingue.json
multilingue.json
pensee-multilingue.json
position-multilingue.json
raisonnement-multilingue-3b.json
rapport-multilingue.md
rapport-n2-multilingue-34m-distille.md
rapport-n2-multilingue-34m.md
rapport-n2-multilingue-capacite.md
rapport-n2-multilingue-distille.md
rapport-n2-multilingue.md
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,os\nfor p in ['data/jw/jw_2026.json','data/presse/presse_2026.json','data/eurlex/32025R1106-24.json','data/multiun/multiun_tech_fr_en.json','data/wikimatrix/wikimatrix_fr_en.json']:\n    try:\n        d=json.load(open(p))\n        print('==',p,type(d), len … [195 caractères tronqués]`

  ```
== data/jw/jw_2026.json <class 'dict'> 4
{"source": "jw.org, La Tour de garde (étude) août 2026", "langues": ["arz", "ben", "eng", "hau", "hin", "ind", "jpn", "mar", "swh", "tel", "urd", "vie"], "documents": [{"article": "An-Appeal-on-the-Basis-of-Love", "n": 37, "langues": ["arz", "ben", "eng", "hau", "hin", "ind", "jpn", "mar", "swh", "tel", "urd", "vie"]}, {"article": "did-you-know", "n": 7, "langues": ["arz", "ben", "eng", "hau", "hin", "ind", "jpn", "mar", "swh", "tel", "urd", "vie"]}, {"article": "Resist-Satans-Tactics-Trust-In-Jehovah-and-In-Jesus", "n": 24, "langues": ["arz", "ben", "eng", "hau", "hin", "ind", "jpn", "mar", "
== data/presse/presse_2026.json <class 'dict'> 5
{"source": "Commission européenne, presse, 2026", "references": ["IP/26/1633", "IP/26/1654", "IP/26/1661", "IP/26/1710", "IP/26/1738", "IP/26/1829", "IP/26/1871", "IP/26/1920", "IP/26/1934", "IP/26/1941", "IP/26/1983", "IP/26/1990", "IP/26/2018", "IP/26/2039", "IP/26/2137"], "documents": [{"ref": "IP/26/1633", "date": "2026-07-16", "n": 13, "titre_en": "Commission welcomes political agreement on the Programme for agile and rapid defence innovation"}, {"ref": "IP/26/1654", "date": "2026-07-20", "n": 14, "
… [2065 caractères tronqués]
  ```

- **bash** `{"command": "find data -maxdepth 2 -type f | sed 's|.*/||' | sort | head -60; echo '==='; du -sh data/* 2>/dev/null | sort -h | tail -20", "description": "List data files and sizes"}`

  ```
32025R1106-24.json
32025R1106-8.json
32025R1106.json
32025R2509.json
articles.jsonl
articles_propres.jsonl
articles.txt
articles.txt
ar_train.txt
ar_val.txt
asp_raw.json
banque.jsonl
banque-manifest.json
banque-reference.jsonl
banque-reference-manifest.json
banque-validee.jsonl
banque-validee-manifest.json
bible.json
bible_narratif.json
bible_web.json
brut.txt
composition-etats.npz
composition-verne-14b-etats.npz
composition-verne-7b-etats.npz
composition-verne-etats.npz
composition-verne-large-etats.npz
composition-verne-plan-etats.npz
consignes_train.jsonl
consignes_val.jsonl
corpus_en.txt
corpus_en_val.txt
corpus_fr_litterature.txt
corpus_fr_train.txt
corpus_fr.txt
corpus_fr_val.txt
corpus_mixte_dev.txt
corpus_mixte_litt2.txt
corpus_mixte_litt.txt
corpus_mixte_propre.txt
corpus_mixte.txt
corpus_multi_train.txt
corpus_multi.txt
corpus_multi_val.txt
corpus_repo.txt
daccord.tsv
de_train.txt
de_val.txt
dev.txt
dev.txt
diabla_fr_en.json
diabla_refs_fr_en.json
en-fr.tmx.gz
en-fr.tmx.gz
en-fr.tmx.gz
en-fr.tmx.gz
en-fr.tmx.gz
eng_kjv_usfm.zip
_eng.txt
eng_web_usfm.zip
en_index_doublons.json
===
2,0G	data/wiki_mix
2,2G	data/corpus_wiki_it
2,3G	data/xnli
2,5G	data/corpus_wiki_zh_texte
2,7
… [441 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['data/bible.json','data/bible_narratif.json','data/bible_web.json']:\n    try:\n        d=json.load(open(p))\n        print('==',p,type(d), len(d) if hasattr(d,'__len__') else '')\n        s=json.dumps(d,ensure_ascii=False)\n        print(s[:120 … [89 caractères tronqués]`

  ```
data/bible.json [Errno 2] No such file or directory: 'data/bible.json'
data/bible_narratif.json [Errno 2] No such file or directory: 'data/bible_narratif.json'
data/bible_web.json [Errno 2] No such file or directory: 'data/bible_web.json'
  ```

- **bash** `{"command": "ls -la data/bible* 2>/dev/null; echo '==='; grep -rln \"bible\" tools/ --include=*.py | head", "description": "Bible files and tools"}`

  ```
===
tools/kfold_pidgin.py
tools/corpus_pidgin_bible.py
  ```

- **bash** `{"command": "find data -maxdepth 3 -name 'bible*' -o -name '*.usfm*' | head -20; echo '==='; python3 - <<'EOF'\nimport subprocess\nEOF\ngrep -rn \"bible\" tools/corpus_pidgin_bible.py | head", "description": "Locate Bible data"}`

  ```
data/pidgin.old/bible.json
data/pidgin.old/bible_web.json
data/pidgin.old/bible_narratif.json
===
2:"""corpus_pidgin_bible.py — LA BIBLE PIDGIN : des milliers de paires narratives, verset par verset.
50:    ap.add_argument("--sortie", default="data/pidgin/bible.json")
54:    pcm_zip = telecharge("https://ebible.org/Scriptures/pcm_usfm.zip", cache / "pcm_usfm.zip")
55:    en_zip = telecharge("https://ebible.org/Scriptures/eng-kjv_usfm.zip", cache / "eng_kjv_usfm.zip")
  ```

- **bash** `{"command": "ls data/*.json 2>/dev/null | sed 's|data/||' | head -80; echo '==='; ls data/*.jsonl 2>/dev/null | sed 's|data/||' | head -30", "description": "List top-level JSON data files"}`

  ```
wt2.json
===
consignes_train.jsonl
consignes_val.jsonl
instructions_fr.jsonl
  ```

- **bash** `{"command": "ls data/pidgin.old/; echo '==='; python3 - <<'EOF'\nimport json\nd=json.load(open('data/pidgin.old/bible.json'))\nprint(type(d),len(d)); print(json.dumps(d,ensure_ascii=False)[:800])\nEOF", "description": "Inspect pidgin bible"}`

  ```
asp_raw.json
bible.json
bible_narratif.json
bible_web.json
eng_kjv_usfm.zip
eng_web_usfm.zip
en_index_doublons.json
en_index.tsv
en_titles.tsv
html
mono_bbc_clean.json
mono_bbc.json
mono.json
pcm_usfm.zip
pcmwiki-latest-langlinks.sql.gz
pcmwiki-latest-pages-articles.xml
pcmwiki-latest-pages-articles.xml.bz2
pidgin.json
translatewiki_en.txt
translatewiki_pcm.txt
wiki.json
wiki_local.json
===
<class 'list'> 30950
[{"en": "Adam , Sheth , Enosh ,", "pcm": "Na Adam born Seth, Seth born Enosh, Enosh born Kenan"}, {"en": "Kenan , Mahalaleel , Jered ,", "pcm": "and na Kenan born Mahalalel. Na Mahalalel bi Jared papa."}, {"en": "Henoch , Methuselah , Lamech ,", "pcm": "Jared born Enoch, Enoch born Metuselah, Metuselah kon born Lamek."}, {"en": "Noah , Shem , Ham , and Japheth .", "pcm": "Lamek born Noah,"}, {"en": "¶ The sons of Japheth ; Gomer , and Magog , and Madai , and Javan , and Tubal , and Meshech , and Tiras .", "pcm": "Jafet shidren na:"}, {"en": "And the sons of Gomer ; Ashchenaz , and Riphath , and Togarmah . + 1.6 Riphath: or, Diphath as it is in some copies", "pcm": "Gomer shidren na:"}, {"en": "And the sons of Javan ; Elishah , and Tarshish , Kittim , and Dodanim . + 1.7 Doda
… [15 caractères tronqués]
  ```

- **bash** `{"command": "find ../Panini-Research ../Panini -maxdepth 5 -type f 2>/dev/null | grep -iE 'signature|atome|philosoph|greek|latin|sanskrit|aristote|platon' | grep -v '\\.git/' | head -40", "description": "Find Panini philosophy signature files"}`

  ```
../Panini/docs/panini/discoveries/dhatu_universals/DHATU_ATOMES_CONCEPTUELS_REVISION.md
../Panini/docs/ouvrage/_staging/fiches/S16-philosophie-et-filiation.md
../Panini/modules/core/filesystem/reports/wikipedia_sanskrit_test.json
../Panini/research/archives/scripts_v2/nipada_s423_v14_signatures.py
../Panini/research/nipada/corpus/references_v272/WIERZBICKA-Rightwrongphilosophy-2002.pdf
../Panini/research/nipada/corpus/catalog_greco_latin_axial_v206k.json
../Panini/research/nipada/corpus/catalog_greco_latin_late_antique_v206l.json
../Panini/research/nipada/corpus/catalog_greco_latin_medieval_v206m.json
../Panini/research/nipada/corpus/nipada_v224_greco_latin_catalog.json
../Panini/research/nipada/corpus/signed_corpus_v225_greco_latin.json
../Panini/research/nipada/corpus/signed_corpus_v225b_greco_latin.json
../Panini/research/nipada/corpus/signed_corpus_v225c_greco_latin_curated.json
../Panini/research/nipada/corpus/signed_corpus_v225d_greco_latin.json
../Panini/research/nipada/corpus/signed_corpus_v225e_greco_latin_curated.json
../Panini/research/nipada/corpus/signed_corpus_v312_platon.json
../Panini/research/nipada/falsification/nipada_v151_dense_signatures.json
../Panini/research
… [1805 caractères tronqués]
  ```

- **bash** `{"command": "find ../Panini-Research -maxdepth 4 -type d 2>/dev/null | grep -v '\\.git' | head -50", "description": "List Panini-Research dirs"}`

  ```
(no output)
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,os\nbase='../Panini/research/nipada/corpus/'\nfor f in ['signed_corpus_v225e_greco_latin_curated.json','catalog_greco_latin_axial_v206k.json','nipada_v224_greco_latin_catalog.json','signed_corpus_v312_platon.json']:\n    p=base+f\n    try:\n        d=json. … [244 caractères tronqués]`

  ```
== signed_corpus_v225e_greco_latin_curated.json <class 'dict'> 7
{"version": "v225e", "description": "§225e GL curated: v225d minus top-5 noisy (§232d analysis). 6 texts retained.", "pruned_from": "v225d", "removed": ["cicero_de_natura_deorum", "cicero_de_officiis", "epictetus_enchiridion", "marcus_aurelius_meditations", "plotinus_enneads"], "retained_count": 6, "created": "2026-05-03", "signed": [{"local_id": "epictetus_discourses", "graph_node_id": "epictetus_discourses", "catalog": "greco_latin_v225b", "tradition_label": "GRECO_LATIN_STOIC", "lang": "eng", "n_chars": 115796, "n_words": 23100, "n_segments": 33, "v14_signature": {"ÊTRE": 0.1557478368355995, "DIFFÉRENCE": 0.11124845488257108, "RAPPORT": 0.11124845488257108, "ORIENTATION": 0.042027194066749075, "SUJET": 0.05067985166872682, "TEMPS": 0.048207663782447466, "MODALITÉ": 0.0407911001236094, "NOMBRE": 0.09023485784919653, "ESPACE": 0.05067985166872682, "OPÉRATION": 0.15945611866501855, "FONC
== catalog_greco_latin_axial_v206k.json <class 'dict'> 10
{"version": "v206k_greco_latin_axial", "generated": "2026-04-29", "macro_culture": "GRECO_LATIN", "epoch": "axial", "n_works": 70, "target": 70, "primary_sources": ["Perseus Di
… [2634 caractères tronqués]
  ```

- **bash** `{"command": "timeout 20 curl -sI https://ebible.org/Scriptures/eng_kjv_usfm.zip | head -5; echo EXIT:$?", "description": "Test network to ebible"}`

  ```
HTTP/2 404 
date: Sat, 07 Nov 2026 21:32:09 GMT
content-type: text/html
server: cloudflare
nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
EXIT:0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('data/udhr/meta.json'))\nprint(type(d), len(d)); print(json.dumps(d,ensure_ascii=False)[:600])\nEOF\nls data/udhr/familles | head", "description": "Inspect UDHR metadata"}`

  ```
<class 'dict'> 441
{"udhr_007.xml": {"iso3": "cri", "nom": "Sãotomense", "script": "Latn", "sens": "ltr", "variante": "007", "nb_articles": 30}, "udhr_008.xml": {"iso3": "pov", "nom": "Crioulo, Upper Guinea (008)", "script": "Latn", "sens": "ltr", "variante": "008", "nb_articles": 30}, "udhr_009.xml": {"iso3": "kmb", "nom": "Mbundu (009)", "script": "Latn", "sens": "ltr", "variante": "009", "nb_articles": 30}, "udhr_010.xml": {"iso3": "tdt", "nom": "Tetun Dili", "script": "Latn", "sens": "ltr", "variante": "010", "nb_articles": 30}, "udhr_011.xml": {"iso3": "umb", "nom": "Umbundu (011)", "script": "Latn", "sens"
abkhaz-adyge.jsonl
ac_benue.jsonl
afro-asiatic.jsonl
afro_ouest.jsonl
arawakan.jsonl
artificial-language.jsonl
atlantic-congo.jsonl
austroasiatic.jsonl
austro_est.jsonl
austronesian.jsonl
  ```

- **bash** `{"command": "find . -maxdepth 4 -iname '*usfm*' -o -iname '*bible*' 2>/dev/null | grep -v '\\.git' | head -30", "description": "Find local Bible resources"}`

  ```
./reports/kfold-pidgin-bible.json
./reports/kfold-bible-narratif-0210.json
./data/jw/html/https_www_jw_org_en_library_magazines_watchtower_study_august_2026_Bible_Fact_E2_80_8B_The_Tree_That_Wakes_Up_Early_.html
./data/pidgin.old/pcm_usfm.zip
./data/pidgin.old/eng_kjv_usfm.zip
./data/pidgin.old/bible.json
./data/pidgin.old/eng_web_usfm.zip
./data/pidgin.old/bible_web.json
./data/pidgin.old/bible_narratif.json
./tools/corpus_pidgin_bible.py
  ```

- **bash** `{"command": "unzip -l data/pidgin.old/eng_kjv_usfm.zip 2>/dev/null | head -20; echo '==='; unzip -l data/pidgin.old/pcm_usfm.zip 2>/dev/null | head -10", "description": "Inspect local USFM zips"}`

  ```
Archive:  data/pidgin.old/eng_kjv_usfm.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
    66465  2026-10-20 20:37   00-FRTeng-kjv.usfm
   557290  2026-10-20 20:37   02-GENeng-kjv.usfm
   459146  2026-10-20 20:37   03-EXOeng-kjv.usfm
   326245  2026-10-20 20:37   04-LEVeng-kjv.usfm
   471838  2026-10-20 20:37   05-NUMeng-kjv.usfm
   382856  2026-10-20 20:37   06-DEUeng-kjv.usfm
   270104  2026-10-20 20:37   07-JOSeng-kjv.usfm
   271465  2026-10-20 20:37   08-JDGeng-kjv.usfm
    35063  2026-10-20 20:37   09-RUTeng-kjv.usfm
   361143  2026-10-20 20:37   10-1SAeng-kjv.usfm
   301450  2026-10-20 20:37   11-2SAeng-kjv.usfm
   358288  2026-10-20 20:37   12-1KIeng-kjv.usfm
   336812  2026-10-20 20:37   13-2KIeng-kjv.usfm
   326040  2026-10-20 20:37   14-1CHeng-kjv.usfm
   386113  2026-10-20 20:37   15-2CHeng-kjv.usfm
   118095  2026-10-20 20:37   16-EZReng-kjv.usfm
   157595  2026-10-20 20:37   17-NEHeng-kjv.usfm
===
Archive:  data/pidgin.old/pcm_usfm.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
   192429  2026-10-20 19:34   02-GENpcm.usfm
   155820  2026-10-20 19:34   03-EXOpcm.usfm
   107508  2026-10-20 19:34   04-LEVpcm.usfm
   150
… [173 caractères tronqués]
  ```

- **bash** `{"command": "ls models/ | head -40; echo '==='; du -sh models/* 2>/dev/null | sort -h | tail -15", "description": "List local models"}`

  ```
Qwen2.5-0.5B-Q4_0.gguf
Qwen2.5-0.5B-Q8_0.gguf
vision
===
337M	models/Qwen2.5-0.5B-Q4_0.gguf
507M	models/Qwen2.5-0.5B-Q8_0.gguf
1,6G	models/vision
  ```

- **bash** `{"command": "ls /tmp | grep -iE 'hf|model|jouet|qwen|labse|e5' | head -20; echo '==='; find /home/stephane -maxdepth 3 -type d -iname '*labse*' -o -iname '*e5*' -o -iname '*qwen*' 2>/dev/null | head", "description": "Find cached HF models"}`

  ```
hf
porte-sauvegarde-modele
sddm-auth-f2d3e75e-2f52-4d65-bbe3-8e4ee538e2ad
tmppiz00lhf
===
/home/stephane/.ServiceHub/277e49e548
/home/stephane/.ServiceHub/8916328e78/304540E567
/home/stephane/.ServiceHub/logs/108DCF4A-Microsoft.VisualStudio.ProjectSystem.ProjectInitializationStatusService-384064-qsj3e5tq-1.log
/home/stephane/.ServiceHub/logs/1D0E0880-Microsoft.VisualStudio.CsDKSourceBasedTestDiscovery.Service-784435-xpe5ntoy-1.log
/home/stephane/.ServiceHub/logs/2B339AD3-Microsoft.VisualStudio.TestWindow.VSCode.ProjectSystemProvider.Service-370745-jte50fe4-1.log
/home/stephane/.ServiceHub/logs/350EB055-VsHubClient-570673-2e5mo3v5-1.log
/home/stephane/.ServiceHub/logs/4254DE50-AssemblyLoadContext-Microsoft.VisualStudio.Code.ServiceHost-11E7E7-291865-r2bvo5gn-1.log
/home/stephane/.ServiceHub/logs/4254DE50-AssemblyLoadContext-Microsoft.VisualStudio.Code.ServiceHost-376842-291855-ukmiscyo-1.log
/home/stephane/.ServiceHub/logs/4254DE50-AssemblyLoadContext-Microsoft.VisualStudio.Code.ServiceHost-7319CC-291855-ekg5rpdm-1.log
/home/stephane/.ServiceHub/logs/4254DE50-AssemblyLoadContext-Microsoft.VisualStudio.Code.ServiceHost-92B392-291865-boqp1e1z-1.log
  ```

- **bash** `{"command": "ls /tmp/hf | head -30; echo '==='; du -sh /tmp/hf/* 2>/dev/null | sort -h | tail -15", "description": "Inspect /tmp/hf"}`

  ```
/tmp/hf
===
  ```

- **bash** `{"command": "python3 -c \"import sentence_transformers, transformers, torch; print(sentence_transformers.__version__, transformers.__version__, torch.__version__)\" 2>&1 | head -5; echo '==='; find ~/.cache/huggingface -maxdepth 3 -type d 2>/dev/null | head -30", "description": "Check ML libraries a … [13 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import sentence_transformers, transformers, torch; print(sentence_transformers.__version__, transformers.__version__, torch.__version__)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'sentence_transformers'
===
  ```

- **bash** `{"command": "file /tmp/hf; ls -la /tmp/hf; echo '==='; python3 -c \"import torch, transformers; print(torch.__version__, transformers.__version__)\" 2>&1 | tail -3; echo '==='; ls ~/.cache/huggingface/hub 2>/dev/null | head", "description": "Check /tmp/hf and libs"}`

  ```
/tmp/hf: DTSZ compressed data, version 98
-rw-r--r--. 1 stephane stephane 12367  4 nov 14:01 /tmp/hf
===
    import torch, transformers; print(torch.__version__, transformers.__version__)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'torch'
===
blobs
CACHEDIR.TAG
datasets--maximoss--daccord-contradictions
datasets--maximoss--gqnli-fr
datasets--rbawden--DiaBLa
models--ggml-org--gemma-3-1b-it-GGUF
models--Qwen--Qwen2.5-0.5B
models--Qwen--Qwen2.5-0.5B-Instruct
models--Qwen--Qwen2.5-14B-Instruct
models--Qwen--Qwen2.5-1.5B-Instruct
  ```

- **bash** `{"command": "sed -n '1,120p' tools/udhr_commun.py", "description": "Read UDHR common loader"}`

  ```
#!/usr/bin/env python3
"""udhr_commun.py — LE SOCLE DES MESURES UDHR : charger, encoder, moyenner.

POURQUOI UN MODULE À PART. Les expériences de cette série (sonde de langue, retrieval croisé, restitution) ont
toutes le **même** premier étage ✓✓ : charger un modèle, encoder un article, garder les états par couche et les
**moyenner** ✓. Si cet étage est écrit trois fois, il divergera trois fois ✗✓ — et c'est exactement le genre
d'écart qu'on ne voit pas ✓✓.

TROIS CHOIX QUI DOIVENT ÊTRE DITS ✗ :
  · **la moyenne des positions** ✓ : elle détruit l'ordre des mots ✓✗. Pour identifier une **langue** c'est sans
    gravité (la langue est dans le vocabulaire et l'orthographe ✓) ; pour la **traduction**, c'est une hypothèse
    forte ✓ — un état moyen n'est pas une phrase ✓.
  · **la normalisation du modèle** (`model.norm` ✓) : on lit l'état tel que le modèle l'utiliserait pour sortir ✓✓,
    pas l'état brut de la couche ✓ — c'est le choix du chapitre 7 ✓.
  · **la troncature** à `--longueur` octets/jetons ✓ : les articles longs (l'article 2 fait 1 500 caractères ✓)
    sont coupés ✗✓ ; la moyenne porte donc sur le **début** de l'article ✓.

CE QU'IL NE FAIT PAS ✗ : il ne vérifie pas que 
… [3871 caractères tronqués]
  ```

- **bash** `{"command": "which -a python3 python; echo '==='; ls .venv venv 2>/dev/null; echo '==='; find /home/stephane -maxdepth 4 -name 'torch' -type d 2>/dev/null | head; echo '==='; python3 -m pip list 2>/dev/null | grep -iE 'torch|transformers|numpy|scikit|scipy'", "description": "Locate Python env with t … [6 caractères tronqués]`

  ```
/usr/bin/python3
/bin/python3
===
===
===
numpy                                          2.5.3
scipy                                          1.18.1
[stderr]
which: no python in (/home/stephane/IA/outils:/usr/local/cuda-13/bin:/home/stephane/.lmstudio/bin:/home/stephane/IA/outils:/home/stephane/.local/share/../bin:/home/stephane/.cargo/bin:/usr/local/cuda-13/bin:/home/stephane/.lmstudio/bin:/home/stephane/.local/bin:/usr/local/bin:/usr/bin:/bin:/home/stephane/.dotnet/tools:/home/stephane/.lmstudio/bin:/home/stephane/.lmstudio/bin:/home/stephane/.lmstudio/bin)
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/jeux/lexique_multilingue.json'))\nfor c in list(d['concepts'])[:3]:\n    print('==',c)\n    print(json.dumps(d['concepts'][c],ensure_ascii=False)[:800])\nEOF", "description": "Inspect concept fields"}`

  ```
== jeu.morpion
{"qid": "Q210339", "qids": ["Q210339"], "labels": {"ar": ["لعبة اكس-او"], "ca": ["tres en ratlla"], "cs": ["piskvorky"], "da": ["kryds og bolle"], "de": ["tic-tac-toe"], "en": ["tic-tac-toe"], "eo": ["tiktakto"], "es": ["tres en raya"], "et": ["trips-traps-trull"], "eu": ["hiruko artzain-joko"], "fa": ["ایکس او"], "fi": ["ristinolla"], "fr": ["tic-tac-toe"], "gl": ["pai fillo nai"], "he": ["איקס עיגול"], "hr": ["kruzic i krizic"], "hu": ["amoba"], "id": ["silang-bulat-silang"], "it": ["tris"], "ja": ["三目並べ"], "ko": ["틱택토"], "lt": ["kryziukai-nuliukai"], "lv": ["krustini un nulites"], "ms": ["tic-tac-toe"], "nb": ["tripp-trapp-tresko"], "nl": ["boter-kaas-en-eieren"], "pl": ["kołko i krzyzyk"], "pt": ["jogo do galo", "jogo da velha"], "ro": ["x si 0"], "ru": ["крестики-нолики"], "sk": ["pis
== jeu.echecs
{"qid": "Q718", "qids": ["Q718"], "labels": {"ar": ["الشطرنج"], "bn": ["দাবা"], "ca": ["escacs"], "cs": ["sachy"], "da": ["skak"], "de": ["schach"], "el": ["σκακι"], "en": ["chess"], "eo": ["sako"], "es": ["ajedrez"], "et": ["male"], "eu": ["xake"], "fa": ["شطرنج"], "fi": ["shakki"], "fr": ["echecs"], "gl": ["xadrez"], "he": ["שחמט"], "hi": ["शतरंज"], "hr": ["sah"], "
… [1243 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/jeux/construire_lexique_multilingue.py", "description": "Read lexicon builder"}`

  ```
#!/usr/bin/env python3
"""construire_lexique_multilingue.py — le lexique des jeux, en 53 langues.

CE QUE CE SCRIPT FAIT, ET POURQUOI IL EST SÉPARÉ. Le lexique multilingue est une
**donnée** (des libellés) et non une règle : on le construit une fois depuis
Wikidata, on le versionne, et la porte n'a plus besoin du réseau. Le script est
donc un **outil de construction**, pas un outil de mesure : il écrit
`tools/jeux/lexique_multilingue.json`, que `lexique_multilingue.py` charge.

LA SOURCE. Les libellés viennent de **Wikidata** (`wbgetentities`,
`props=labels`), donc de la licence **CC0** ; les identifiants sont ceux des
articles Wikipédia anglais, lus par `pageprops`. Les concepts sont volontairement
**peu nombreux et stables** (pièces, rangs, couleurs, enseignes, noms de jeux,
notions de maîtres) : un libellé faux serait pire qu'un libellé absent, et la
couverture est mesurée, pas supposée.

CE QUI EST MANUEL. Les verbes (« joue », « prend », « passe ») ne sont pas des
entités Wikidata : le lexique multilingue ne les invente pas. Les surfaces
multilingues sont donc des **mots-clés** (pièce + cases, rang + enseigne), et la
grammaire reste FR/EN. C'est un choix du contrat, écrit dans
… [4835 caractères tronqués]
  ```

- **bash** `{"command": "head -3 data/glottolog/languages.csv; echo '==='; head -3 data/glottolog/values.csv; echo '==='; wc -l data/glottolog/*.csv", "description": "Inspect Glottolog tables"}`

  ```
ID,Name,Macroarea,Latitude,Longitude,Glottocode,ISO639P3code,Level,Countries,Family_ID,Language_ID,Closest_ISO369P3code,First_Year_Of_Documentation,Last_Year_Of_Documentation,Is_Isolate
abkh1242,Abkhaz-Adyge,Eurasia,43.692403000000006,40.8701525,abkh1242,,family,,,,,,,
surm1244,Surmic,Africa,6.8819987708333334,34.97338345833333,surm1244,,family,,,,,,,
===
ID,Language_ID,Parameter_ID,Value,Code_ID,Comment,Source,codeReference
abkh1242-level,abkh1242,level,family,level-family,,,
abkh1242-category,abkh1242,category,Family,category-Family,,,
===
   27178 data/glottolog/languages.csv
  145199 data/glottolog/values.csv
  172377 total
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport csv\nfor p in ['data/glottolog/languages.csv','data/glottolog/values.csv']:\n    with open(p,newline='',encoding='utf-8') as f:\n        r=csv.reader(f); h=next(r)\n        print('==',p,len(h)); print(h)\nEOF", "description": "Print Glottolog headers"}`

  ```
== data/glottolog/languages.csv 15
['ID', 'Name', 'Macroarea', 'Latitude', 'Longitude', 'Glottocode', 'ISO639P3code', 'Level', 'Countries', 'Family_ID', 'Language_ID', 'Closest_ISO369P3code', 'First_Year_Of_Documentation', 'Last_Year_Of_Documentation', 'Is_Isolate']
== data/glottolog/values.csv 8
['ID', 'Language_ID', 'Parameter_ID', 'Value', 'Code_ID', 'Comment', 'Source', 'codeReference']
  ```

- **bash** `{"command": "head -2 data/udhr/langues.jsonl; echo '==='; python3 - <<'EOF'\nimport json\nd=[json.loads(l) for l in open('data/udhr/langues.jsonl')][:3]\nfor x in d: print(json.dumps(x,ensure_ascii=False)[:800])\nEOF", "description": "Inspect UDHR languages metadata"}`

  ```
{"fichier": "udhr_007.xml", "iso3": "cri", "nom": "Sãotomense", "script": "Latn", "sens": "ltr", "titre": "Declaraçón Universal di Dirêtu di Hómé", "nb_articles": 30, "preambule_car": 1593, "attrs": "iso639-3=cri key=007 n=Sãotomense dir=ltr iso15924=Latn"}
{"fichier": "udhr_008.xml", "iso3": "pov", "nom": "Crioulo, Upper Guinea (008)", "script": "Latn", "sens": "ltr", "titre": "DECLARAÇON UNIVERSAL DI DIRITU DI OMIS", "nb_articles": 30, "preambule_car": 1875, "attrs": "iso639-3=pov key=008 n=Crioulo, Upper Guinea (008) dir=ltr iso15924=Latn"}
===
{"fichier": "udhr_007.xml", "iso3": "cri", "nom": "Sãotomense", "script": "Latn", "sens": "ltr", "titre": "Declaraçón Universal di Dirêtu di Hómé", "nb_articles": 30, "preambule_car": 1593, "attrs": "iso639-3=cri key=007 n=Sãotomense dir=ltr iso15924=Latn"}
{"fichier": "udhr_008.xml", "iso3": "pov", "nom": "Crioulo, Upper Guinea (008)", "script": "Latn", "sens": "ltr", "titre": "DECLARAÇON UNIVERSAL DI DIRITU DI OMIS", "nb_articles": 30, "preambule_car": 1875, "attrs": "iso639-3=pov key=008 n=Crioulo, Upper Guinea (008) dir=ltr iso15924=Latn"}
{"fichier": "udhr_009.xml", "iso3": "kmb", "nom": "Mbundu (009)", "script": "Latn", "sens": "ltr
… [128 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' tools/corpus_pidgin_bible.py", "description": "Read pidgin Bible builder"}`

  ```
#!/usr/bin/env python3
"""corpus_pidgin_bible.py — LA BIBLE PIDGIN : des milliers de paires narratives, verset par verset.

POURQUOI ✓✓. Les paires translatewiki sont **courtes et techniques** (mesure 95) ✗✗ ; il faut des paires
**narratives**. La **Bible en pidgin nigérian** (PCMWBT, 2019, Wycliffe) existe sur eBible en **USFM**, avec les
mêmes numéros de versets que la Bible anglaise (KJV) ✓✓ — l'alignement est **structurel** (livre, chapitre, verset)
✓✓. On construit les paires et on les ajoute à l'entraînement ✓✓.

⚠️ CE QUE CELA NE DIT PAS ✗ : la Bible est **ancienne** (contamination possible de l'anglais) et son registre est
**religieux** ✓✗ ; l'évaluation reste sur les **contes** tenus à part ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib, re, urllib.request, zipfile

UA = {"User-Agent": "Mozilla/5.0 (corpus Drave)"}


def telecharge(url: str, dest: pathlib.Path) -> pathlib.Path:
    if dest.exists() and dest.stat().st_size > 100_000:
        return dest
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())
    return dest


def parse_usfm(texte: str) -> dict[tup
… [1995 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['data/pidgin.old/bible.json','data/pidgin.old/bible_web.json','data/pidgin.old/bible_narratif.json']:\n    d=json.load(open(p))\n    print('==',p,len(d), list(d[0]) if isinstance(d,list) and d else type(d))\n    if isinstance(d,list):\n        f … [109 caractères tronqués]`

  ```
== data/pidgin.old/bible.json 30950 ['en', 'pcm']
{"en": "Adam , Sheth , Enosh ,", "pcm": "Na Adam born Seth, Seth born Enosh, Enosh born Kenan"}
{"en": "Kenan , Mahalaleel , Jered ,", "pcm": "and na Kenan born Mahalalel. Na Mahalalel bi Jared papa."}
== data/pidgin.old/bible_web.json 30934 ['en', 'pcm']
{"en": "Adam, Seth , Enosh,", "pcm": "Na Adam born Seth, Seth born Enosh, Enosh born Kenan"}
{"en": "Kenan , Mahalalel , Jared ,", "pcm": "and na Kenan born Mahalalel. Na Mahalalel bi Jared papa."}
== data/pidgin.old/bible_narratif.json 7526 ['en', 'pcm', 'cle']
{"en": "The first book I wrote, Theophilus , concerned all that Jesus began both to do and to teach ,", "pcm": "My friend Teofilus, for di book wey I first rite give yu, I tok about all di tins wey Jesus Christ start to dey do and tish,", "cle": "ACT.1.1"}
{"en": "until the day in which he was received up, after he had given commandment through the Holy Spirit to the apostles whom he had chosen .", "pcm": "until di day wen God kon karry am go heaven, afta e give orda to di apostles, wey e choose with di Holy Spirit.", "cle": "ACT.1.2"}
  ```

- **bash** `{"command": "find . -maxdepth 5 -type f \\( -iname '*_usfm.zip' -o -iname '*usfm*' \\) 2>/dev/null | head -20; echo '==='; grep -rn \"ebible\" tools/ | head", "description": "Find other USFM zips"}`

  ```
./data/pidgin.old/pcm_usfm.zip
./data/pidgin.old/eng_kjv_usfm.zip
./data/pidgin.old/eng_web_usfm.zip
===
tools/corpus_pidgin_bible.py:54:    pcm_zip = telecharge("https://ebible.org/Scriptures/pcm_usfm.zip", cache / "pcm_usfm.zip")
tools/corpus_pidgin_bible.py:55:    en_zip = telecharge("https://ebible.org/Scriptures/eng-kjv_usfm.zip", cache / "eng_kjv_usfm.zip")
  ```

- **bash** `{"command": "timeout 30 curl -s 'https://ebible.org/Scriptures/' | head -40", "description": "List eBible Scriptures page"}`

  ```
<!DOCTYPE html>
<html><head>
  <meta content="text/html; charset=utf-8" http-equiv="content-type">
  <link rel="stylesheet" href="vu.css" type="text/css">
  <title>Bible List</title>
</head><body style="color: rgb(0, 0, 64); background-color: rgb(255, 255, 255);">
<div id="container">
<div id="top">
<table align='center'><tr><td><a href="http://eBible.org"><img src="eBible.orgLogo100.png" alt="eBible.org"/></td><td><a href="index.php"><img src="BibleShelf100.png" alt="Translations"/></a></td><td><a href="country.php"><img src="BlueMarble100.png" alt="Countries/Territories"/></a></td></tr><tr><td><a href="http://eBible.org">eBible.org</td><td><a href="index.php">Translations</a></td><td><a href="country.php">Territories</a></td></tr></table><p>&nbsp;</p><h1>Bible Translations</h1><p>Select a translation for a list of available downloads. Select a heading to sort by that column.</p></div><table border="1" padding="2"><tr><td><b>Territory</b></td><td><a href="index.php?sort=l">Language</a></td><td><a href="index.php?sort=e">Language (English)</a></td><td><a href="index.php?sort=v">Vernacular Title</a></td><td><a href="index.php?sort=t">English Title</a></td></tr><tr class='redist'><td
… [15576 caractères tronqués]
  ```

- **bash** `{"command": "ls tools | grep -iE 'align|retriev|lexiq|traduc|bible|udhr' ; echo '==='; ls tools/alignement 2>/dev/null | head; echo '==='; grep -rln \"cosine\\|tfidf\\|Tfidf\\|n-gram\" tools/*.py | head -20", "description": "Find existing CPU retrieval/alignment tools"}`

  ```
aligneur_litteraire.py
analyse_alignement.py
corpus_pidgin_bible.py
extrait_udhr.py
genealogie_udhr.py
importer_udhr.py
preparer_udhr.py
restitution_udhr.py
retrieval_parallele.py
retrieval_udhr.py
sonder_udhr.py
style_traducteur.py
test_contamination_udhr.py
udhr_commun.py
===
===
tools/engram_reference.py
tools/entrainer_moteur.py
tools/traduire_bench.py
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('data/pidgin.old/bible_narratif.json'))\nprint(len(d))\nfrom collections import Counter\nprint(Counter(x['cle'].split('.')[0] for x in d).most_common(10))\nprint(d[0]['cle'])\nEOF", "description": "Inspect narrative Bible alignment keys"}`

  ```
7526
[('GEN', 1531), ('EXO', 1213), ('LUK', 1149), ('MAT', 1071), ('ACT', 1006), ('JHN', 879), ('MRK', 677)]
ACT.1.1
  ```

- **bash** `{"command": "python3 - <<'EOF'\ntry:\n import pycountry; print('pycountry', pycountry.__version__ if hasattr(pycountry,'__version__') else 'ok')\nexcept Exception as e: print('no pycountry',e)\ntry:\n import babel; print('babel ok')\nexcept Exception as e: print('no babel',e)\nEOF", "description": " … [26 caractères tronqués]`

  ```
no pycountry No module named 'pycountry'
babel ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport csv\nrows=list(csv.DictReader(open('data/glottolog/languages.csv',encoding='utf-8')))\nprint(len(rows))\n# show some with first year\nn=0\nfor r in rows:\n    if r['First_Year_Of_Documentation'] and r['Level']=='language':\n        print(r['Name'],r['ISO639P3co … [287 caractères tronqués]`

  ```
27177
Puelche pue 1829 1956
Betoi-Jirara  1741 1787
Mochica omc 1644 1920
Atakapa aqp 1721 1934
Sechuran  1792 1918
Lule ule 1732 1825
Coahuilteco xcw 1732 1760
Kariri  1698 1867
Takelma tkm 1857 1934
Tallán  1792 1850
Timucua tjm 1612 1767
Jirajaran  1886 1916
Puquina puq 1607 1750
Comecrudan xcm 1829 1886
Andaqui ana 1787 1975
langs with first year 212
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport csv\nrows=list(csv.DictReader(open('data/glottolog/languages.csv',encoding='utf-8')))\nwant={'eng','fra','deu','spa','rus','cmn','jpn','ara','hin','swh','yor','zul','tur','pol','vie','tha','kor','heb','ell','lat'}\nfor r in rows:\n    if r['ISO639P3code'] in wa … [190 caractères tronqués]`

  ```
Korean kor   language
Vietnamese vie   language
Japanese jpn   language
Turkish tur   language
Russian rus   language
Mandarin Chinese cmn   language
Latin lat -100 100 language
Polish pol   language
Modern Hebrew heb   language
Modern Greek ell   language
Thai tha   language
Yoruba yor   language
Hindi hin   language
German deu   language
English eng   language
Swahili swh   language
Spanish spa   language
Zulu zul   language
French fra   language
  ```

- **bash** `{"command": "find data/udhr -maxdepth 2 -type f | head -20; echo '==='; grep -o 'date=\"[^\"]*\"' data/udhr/*.xml 2>/dev/null | head; echo '==='; find data/udhr -maxdepth 2 -type f | wc -l", "description": "Check UDHR raw XML dates"}`

  ```
data/udhr/langues.jsonl
data/udhr/articles.jsonl
data/udhr/udhr_train.txt
data/udhr/meta.json
data/udhr/articles_propres.jsonl
data/udhr/udhr_val.txt
data/udhr/_fra.txt
data/udhr/_eng.txt
data/udhr/udhr_fra_train.txt
data/udhr/udhr_fra_val.txt
data/udhr/udhr_10_train.txt
data/udhr/udhr_10_val.txt
data/udhr/udhr_50_train.txt
data/udhr/udhr_50_val.txt
data/udhr/udhr_1_train.txt
data/udhr/udhr_1_val.txt
data/udhr/genealogie.json
data/udhr/familles/indo-european.jsonl
data/udhr/familles/atlantic-congo.jsonl
data/udhr/familles/austronesian.jsonl
===
===
55
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport urllib.request, json\nurl='https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q1860&props=claims&format=json'\ntry:\n    req=urllib.request.Request(url,headers={'User-Agent':'Drave/1.0'})\n    d=json.load(urllib.request.urlopen(req,timeout=20))\n    cl … [277 caractères tronqués]`

  ```
claims 180
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport urllib.request, json\nids=['Q36510','Q397','Q35355','Q1860','Q150','Q652','Q5146','Q9610']\nfor qid in ids:\n    url=f'https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims&format=json'\n    try:\n        req=urllib.request.Request(url, … [620 caractères tronqués]`

  ```
Q36510 []
Q397 [('P580', '-0800-00-00T00:00:00Z')]
Q35355 [('P571', '-5500-00-00T00:00:00Z')]
Q1860 []
Q150 []
Q652 []
Q5146 []
Q9610 []
  ```

- **bash** `{"command": "python3 -c \"import sklearn; print(sklearn.__version__)\" 2>&1; python3 -c \"import numpy, scipy; print(numpy.__version__, scipy.__version__)\"", "description": "Check sklearn availability"}`

  ```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import sklearn; print(sklearn.__version__)
    ^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'sklearn'
2.5.3 1.18.1
  ```

- **bash** `{"command": "cat > /tmp/proto_b7.py <<'EOF'\nimport json, unicodedata, re, math, itertools\nfrom collections import defaultdict\nD=json.load(open('tools/jeux/lexique_multilingue.json'))\nlangs=D['langues']; concepts=D['concepts']\ndef norm(s):\n    s=unicodedata.normalize('NFKC',s).casefold()\n    s … [1313 caractères tronqués]`

  ```
langs 71 concepts 35
coverage min/max 1 35 median 19
fr en 12 35 0.34285714285714286
en de 10 34 0.29411764705882354
ru uk 20 32 0.625
hi ur 1 14 0.07142857142857142
ar fa 6 23 0.2608695652173913
zh ja 1 30 0.03333333333333333
en zh 1 32 0.03125
fr ru 1 34 0.029411764705882353
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nD=json.load(open('tools/jeux/lexique_multilingue.json'))\nmeta=json.load(open('data/udhr/meta.json'))\niso3s={m['iso3'] for m in meta.values()}\nscripts={}\nfor m in meta.values(): scripts.setdefault(m['iso3'],m['script'])\nlangs=D['langues']\nprint(len(l … [1041 caractères tronqués]`

  ```
71 ['ar', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'gl', 'he', 'hi', 'hr', 'hu', 'id', 'is', 'it', 'ja', 'ka', 'kk', 'ko', 'lt', 'lv', 'mk', 'ms', 'mt', 'nb', 'nl', 'nn', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'sw', 'ta', 'th', 'tr', 'uk', 'ur', 'vi', 'zh', 'af', 'am', 'az', 'be', 'bs', 'cy', 'ga', 'hy', 'km', 'ky', 'lo', 'mn', 'ne', 'pa', 'si', 'so', 'uz', 'yo', 'zu']
missing iso3 in udhr [('ar', 'ara'), ('et', 'est'), ('fa', 'fas'), ('lv', 'lav'), ('ms', 'msa'), ('sq', 'sqi'), ('sw', 'swa'), ('az', 'aze'), ('mn', 'mon'), ('ne', 'nep'), ('uz', 'uzb')]
scripts sample [('ar', None), ('bn', 'Beng'), ('ca', 'Latn'), ('cs', 'Latn'), ('da', 'Latn'), ('de', 'Latn'), ('el', 'Grek'), ('en', 'Latn'), ('eo', 'Latn'), ('es', 'Latn')]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nmeta=json.load(open('data/udhr/meta.json'))\nfor f,m in meta.items():\n    if m['nom'].lower().startswith(('arab','est','pers','latv','malay','alban','swah','azer','mong','nepal','uzbek')):\n        print(f,m['iso3'],m['nom'],m['script'])\nEOF", "descript … [31 caractères tronqués]`

  ```
udhr_als.xml als Albanian, Tosk Latn
udhr_arb.xml arb Arabic, Standard Arab
udhr_arl.xml arl Arabela Latn
udhr_azj_cyrl.xml azj Azerbaijani, North (Cyrillic) Cyrl
udhr_azj_latn.xml azj Azerbaijani, North (Latin) Latn
udhr_est.xml ekk Estonian Latn
udhr_khk.xml khk Mongolian, Halh (Cyrillic) Cyrl
udhr_lav.xml lvs Latvian Latn
udhr_mal.xml mal Malayalam Mlym
udhr_mly_arab.xml zlm Malay (Arabic) Arab
udhr_mly_latn.xml zlm Malay (Latin) Latn
udhr_nep.xml npi Nepali Deva
udhr_swh.xml swh Swahili Latn
udhr_uzn_cyrl.xml uzn Uzbek, Northern (Cyrillic) Cyrl
udhr_uzn_latn.xml uzn Uzbek, Northern (Latin) Latn
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport csv, json\nrows=list(csv.DictReader(open('data/glottolog/languages.csv',encoding='utf-8')))\nby={}\nfor r in rows:\n    if r['Level']=='language' and r['ISO639P3code'] and r['ISO639P3code'] not in by:\n        by[r['ISO639P3code']]=r\nM={'ar':'ara','bn':'ben',' … [1138 caractères tronqués]`

  ```
missing [('ar', 'ara'), ('et', 'est'), ('fa', 'fas'), ('hr', 'hrv'), ('ms', 'msa'), ('nb', 'nob'), ('nn', 'nno'), ('sq', 'sqi'), ('sr', 'srp'), ('sw', 'swa'), ('az', 'aze'), ('bs', 'bos'), ('mn', 'mon'), ('ne', 'nep'), ('uz', 'uzb')]
en ('indo1319', 'English', 'Africa;Eurasia;South America')
fr ('indo1319', 'French', 'Eurasia')
de ('indo1319', 'German', 'Eurasia')
ru ('indo1319', 'Russian', 'Eurasia')
uk ('indo1319', 'Ukrainian', 'Eurasia')
hi ('indo1319', 'Hindi', 'Eurasia')
ur ('indo1319', 'Urdu', 'Eurasia')
ar None
fa None
zh ('sino1245', 'Mandarin Chinese', 'Eurasia')
ja ('japo1237', 'Japanese', 'Eurasia')
sw None
yo ('atla1278', 'Yoruba', 'Africa')
zu ('atla1278', 'Zulu', 'Africa')
tr ('turk1311', 'Turkish', 'Eurasia')
fi ('ural1272', 'Finnish', 'Eurasia')
eu ('', 'Basque', 'Eurasia')
ka ('kart1248', 'Georgian', 'Eurasia')
ko ('kore1284', 'Korean', 'Eurasia')
th ('taik1256', 'Thai', 'Eurasia')
vi ('aust1305', 'Vietnamese', 'Eurasia')
  ```

- **bash** `{"command": "cat > /tmp/proto_bible.py <<'EOF'\nimport zipfile,re,json,unicodedata,math,random\nfrom collections import Counter\nimport numpy as np\n\ndef parse_usfm(texte):\n    out={}; livre=None; chapitre=None\n    for ligne in texte.splitlines():\n        m=re.match(r\"\\\\id\\s+([A-Z0-9]{3})\", … [3944 caractères tronqués]`

  ```
verses 36822 38052 31069
common 31065
narr 7532
filtered 4359
dedup 4315
sample 800
KJV-WEB top1 0.9925 mrr 0.9379 med 1 ctrl 0.0025
WEB-PCM top1 0.6475 mrr 0.0444 med 1 ctrl 0.0000
KJV-PCM top1 0.5925 mrr 0.0301 med 1 ctrl 0.0013
  ```

- **bash** `{"command": "for id in hin arb cmn zho fra deu spa por rus; do code=$(timeout 15 curl -s -o /dev/null -w '%{http_code}' \"https://ebible.org/Scriptures/${id}_usfm.zip\"); echo \"$id $code\"; done", "description": "Probe eBible USFM availability"}`

  ```
hin 404
arb 404
cmn 404
zho 404
fra 404
deu 404
spa 404
por 404
rus 404
  ```

- **bash** `{"command": "for id in hin Usfm arb Usfm cmn Usfm fra Usfm deu Usfm spa Usfm; do :; done; timeout 20 curl -s 'https://ebible.org/Scriptures/index.php?sort=l' | grep -oE \"details.php\\?id=(hin|arb|cmn|fra|deu|spa|por|rus)[^']*\" | head", "description": "Find eBible translation IDs"}`

  ```
details.php?id=deuelo
details.php?id=deuelo
details.php?id=deuelo
details.php?id=deuelo
details.php?id=deu1951
details.php?id=deu1951
details.php?id=deu1951
details.php?id=deu1951
details.php?id=deuelbbk
details.php?id=deuelbbk
[stderr]
grep: write error: Broken pipe
  ```

- **bash** `{"command": "timeout 30 curl -s 'https://ebible.org/Scriptures/index.php?sort=l' -o /tmp/ebible.html; grep -oE \"details.php\\?id=[^']+'[^>]*>[^<]*Hindi[^<]*\" /tmp/ebible.html | head -10; echo '---'; grep -oE \"details.php\\?id=[^']+'[^>]*>[^<]*Arabic[^<]*\" /tmp/ebible.html | head -5", "descriptio … [35 caractères tronqués]`

  ```
details.php?id=urdgvh' target='_blank'>Urdu Geo Bible, Hindi Script
details.php?id=hin2017' target='_blank' class='freeserif redist'>Hindi
details.php?id=hin2017' target='_blank'>Hindi Indian Revised Version Bible
details.php?id=hin2010' target='_blank' class='akshar_unicode restricted'>Hindi
details.php?id=hin2010' target='_blank'>Hindi Easy Reading Version
details.php?id=hincv' target='_blank' class='freeserif redist'>Hindi
details.php?id=hincv' target='_blank'>Hindi Contemporary Version Bible
---
details.php?id=arq' target='_blank' class='amiri restricted'>Arabic, Algerian Spoken
details.php?id=arq' target='_blank' class='amiri restricted'>Arabic, Algerian Spoken
details.php?id=arq' target='_blank'>Arabic, Algerian Spoken: Arabe Algerian NT
details.php?id=aeu' target='_blank' class='dejavu_serif redist'>Arabic, Tunisian Spoken
details.php?id=pga' target='_blank' class='liberation_sans redist'>Sudanese Creole Arabic
  ```

- **bash** `{"command": "grep -oE \"details.php\\?id=[^']+'[^>]*>[^<]*Arabic[^<]*\" /tmp/ebible.html | grep -i 'standard\\|modern' | head -10; echo '---'; grep -oE \"details.php\\?id=[^']+'[^>]*>[^<]*(Chinese|Mandarin)[^<]*\" /tmp/ebible.html | head -8", "description": "Find Standard Arabic and Chinese IDs"}`

  ```
details.php?id=arbnav' target='_blank' class='amiri redist'>Arabic, Standard
---
details.php?id=cmnswcb' target='_blank' class='bitstream_cyberbit redist'>Chinese, Mandarin
details.php?id=cmnswcb' target='_blank'>World Chinese Bible
details.php?id=cmn2006' target='_blank' class='bitstream_cyberbit restricted'>Chinese
details.php?id=cmn2006' target='_blank'>Chinese (simplified) Easy Reading Version
details.php?id=cmn-cu89s' target='_blank' class='bitstream_cyberbit redist'>Chinese
details.php?id=cmn-cu89s' target='_blank'>Chinese Union Version (simplified)
details.php?id=cmn-ncvs' target='_blank' class='bitstream_cyberbit restricted'>Chinese
details.php?id=cmn-ncvs' target='_blank'>Chinese New Version (simplified)
  ```

- **bash** `{"command": "for id in hin2017 arbnav cmn-cu89s; do timeout 60 curl -sL -o /tmp/${id}.zip \"https://ebible.org/Scriptures/${id}_usfm.zip\"; echo \"$id $(stat -c%s /tmp/${id}.zip) $(file -b /tmp/${id}.zip | cut -c1-40)\"; done", "description": "Download multilingual USFM zips"}`

  ```
hin2017 2243258 Zip archive data, made by v3.0 UNIX, ext
arbnav 1977649 Zip archive data, made by v3.0 UNIX, ext
cmn-cu89s 1429725 Zip archive data, made by v3.0 UNIX, ext
  ```

- **bash** `{"command": "grep -oE \"details.php\\?id=[^']+'[^>]*>[^<]*French[^<]*\" /tmp/ebible.html | head -8", "description": "Find French eBible ID"}`

  ```
details.php?id=frajnd' target='_blank' class='gentium_plus redist'>French
details.php?id=frajnd' target='_blank'>French: Bible J.N. Darby
details.php?id=fra_fob' target='_blank' class='gentium redist'>French
details.php?id=fra_fob' target='_blank'>French Ostervald Bible
details.php?id=fraLSG' target='_blank' class='gentium redist'>French
details.php?id=fraLSG' target='_blank'>French Louis Segond 1910 Bible
details.php?id=frasbl' target='_blank' class='dejavu_serif redist'>French
details.php?id=frasbl' target='_blank'>French Free Holy Bible for the World
  ```

- **bash** `{"command": "for id in hin2017 arbnav cmn-cu89s fraLSG fra_fob eng-kjv eng-web pcm; do echo \"=== $id\"; timeout 20 curl -s \"https://ebible.org/Scriptures/details.php?id=$id\" | sed -e 's/<[^>]*>/ /g' | tr -s ' \\n' ' \\n' | grep -iE 'date|copyright|public domain|license|year|translation' | head -8 … [60 caractères tronqués]`

  ```
=== hin2017
 इंडियन रिवाइज्ड वर्जन (IRV) हिंदी - 2019 eBible.org Translations Territories &nbsp; इंडियन रिवाइज्ड वर्जन (IRV) हिंदी - 2019 Hindi Indian Revised Version Bible Language: [hin] मानक हिन्दी‎ Hindi Title: इंडियन रिवाइज्ड वर्जन (IRV) हिंदी - 2019 Hindi Indian Revised Version Bible Abbreviation: IRVHin ID: HINIRV or hin2017 Copyright © 2017, 2018, 2019 Bridge Connectivity Solutions Format Link Browser Bible Study online with Browser Bible MP3 Audio Stream or download MP3 audio Mobile HTML Read Mobile HTML online Zipped mobile HTML hin2017_html.zip ePub 3 and Kindle hin2017.epub PDF PDF file list Crosswire Sword module hin2017eb.zip Plain text canon only chapter files hin2017_readaloud.zip BibleWorks import (VPL) + SQL hin2017_vpl.zip Browser Bible module hin2017_browserBible.zip USFX hin2017_usfx.zip USFM hin2017_usfm.zip XeTeX hin2017_xetex.zip The Indian Revised Version Holy Bible in the Hindi language of India आदि में परमेश्वर ने आकाश और पृथ्वी की सृष्टि की। (इब्रा. 1:10, इब्रा. 11:3) —Genesis 1:1 दाऊद का भजन यहोवा मेरा चरवाहा है, मुझे कुछ घटी न होगी। (यशा. 40:11) —Psalm 23:1 इसलिए पहले तुम परमेश्वर के राज्य और धार्मिकता की खोज करो तो ये सब वस्तुएँ तुम्हें मिल जाएँगी। (ल
… [13735 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('work/corpus-commun/index.json'))\nprint(type(d), list(d)[:10] if isinstance(d,dict) else len(d))\nprint(json.dumps(d,ensure_ascii=False)[:1200])\nEOF", "description": "Inspect corpus commun index"}`

  ```
<class 'dict'> ['controles', 'date', 'fichiers', 'intersection', 'limites', 'normalisation', 'prochaine_etape', 'selection', 'sources', 'statistiques']
{"controles": {"controle_negatif": {"n": 8, "n_ok": 8, "verdict": "PASS"}, "egalite_exacte": {"attendu": 21, "n": 21, "verdict": "PASS"}, "familles": {"attendu": 5, "n": 5, "verdict": "PASS"}}, "date": "2026-11-07", "fichiers": {"controle_negatif": "work/corpus-commun/controle-negatif.json", "corpus_jsonl": "work/corpus-commun/corpus.jsonl", "index": "work/corpus-commun/index.json", "metadata_tsv": "work/corpus-commun/metadata.tsv", "sources_sha256": "work/corpus-commun/sources.sha256", "textes": "work/corpus-commun/textes/ (21 fichiers)"}, "intersection": {"appariables_article1": 438, "article1_drave": 440, "drave_article1_hors_panini": 2, "drave_langues": 456, "ecarts_surface": 20, "exacts": 418, "familles_exactes": {"(inconnue)": 10, "Abkhaz-Adyge": 2, "Afro-Asiatic": 12, "Algic": 1, "Araucanian": 1, "Arawakan": 7, "Artificial Language": 3, "Athabaskan-Eyak-Tlingit": 1, "Atlantic-Congo": 81, "Austroasiatic": 3, "Austronesian": 37, "Aymaran": 1, "Barbacoan": 1, "Cahuapanan": 1, "Chicham": 4, "Dravidian": 5, "Eskimo-Aleut": 1, "Gua
… [152 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\narts={}\nfor l in open('data/udhr/articles_propres.jsonl'):\n    x=json.loads(l); arts.setdefault(x['fichier'],set()).add(int(x['art']))\nidx=json.load(open('work/corpus-commun/index.json'))\nprint(type(idx))\nif isinstance(idx,dict):\n    for k,v in list … [89 caractères tronqués]`

  ```
<class 'dict'>
controles {'controle_negatif': {'n': 8, 'n_ok': 8, 'verdict': 'PASS'}, 'egalite_exacte': {'attendu': 21, 'n': 21, 'verdict': 'PASS'}, 'familles': {'attendu': 5, 'n': 5, 'verdict': 'PASS'}}
date 2026-11-07
fichiers {'controle_negatif': 'work/corpus-commun/controle-negatif.json', 'corpus_jsonl': 'work/corpus-commun/corpus.jsonl', 'index': 'work/corpus-commun/index.json', 'metadata_tsv': 'work/corpus-commun/metadata.tsv', 'sources_sha256': 'work/corpus-commun/sources.sha256', 'textes': 'work/corpus-commun/textes
  ```

- **bash** `{"command": "head -3 work/corpus-commun/metadata.tsv; echo '==='; head -2 work/corpus-commun/corpus.jsonl; echo '==='; wc -l work/corpus-commun/corpus.jsonl", "description": "Inspect corpus commun files"}`

  ```
id	iso3	langue	script	famille	branche_feuille	genre	epoque	role	nb_phrases	nb_mots_ws	nb_caracteres	sha256_fichier
udhr_eng	eng	English	Latn	Indo-European	macr1271	declaration	1948	strate	2	30	170	95b7af97d4eca78cf41422a4366078d5ba4f981d24357e039f7d56bf9cb3c1c1
udhr_hin	hin	Hindi	Deva	Indo-European	hind1270	declaration	1948	strate	2	35	189	def1dbc3332c84f1efd47b1f04ed8addcb1f70c73e9d69c959194cbb48554087
===
{"branche_feuille": "macr1271", "epoque": 1948, "famille": "Indo-European", "genre": "declaration", "id": "udhr_eng", "iso3": "eng", "langue": "English", "phrase": "All human beings are born free and equal in dignity and rights.", "phrase_index": 0, "role": "strate", "script": "Latn", "sha256_phrase": "73df4f2492ac4b38c118185076b6f8f06747865d916d6c760540b69444c92249"}
{"branche_feuille": "macr1271", "epoque": 1948, "famille": "Indo-European", "genre": "declaration", "id": "udhr_eng", "iso3": "eng", "langue": "English", "phrase": "They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.", "phrase_index": 1, "role": "strate", "script": "Latn", "sha256_phrase": "a00c0b1b8b2dc70b6a99c58db016134b9223aa4f3905d47e25ab037780c586ad"}
===

… [34 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nidx=json.load(open('work/corpus-commun/index.json'))\nprint(json.dumps(idx['statistiques'],ensure_ascii=False,indent=1)[:1500])\nprint('selection keys', idx['selection'].keys() if isinstance(idx['selection'],dict) else type(idx['selection']))\nEOF", "desc … [33 caractères tronqués]`

  ```
{
 "familles": {
  "Afro-Asiatic": 4,
  "Atlantic-Congo": 4,
  "Austronesian": 4,
  "Indo-European": 5,
  "Sino-Tibetan": 4
 },
 "langues_par_famille": {
  "Afro-Asiatic": [
   "udhr_amh",
   "udhr_arb",
   "udhr_hau_NE",
   "udhr_heb"
  ],
  "Atlantic-Congo": [
   "udhr_ewe",
   "udhr_fuf_adlm",
   "udhr_ibo",
   "udhr_kin"
  ],
  "Austronesian": [
   "udhr_ind",
   "udhr_jav",
   "udhr_mly_arab",
   "udhr_tgl"
  ],
  "Indo-European": [
   "udhr_bel",
   "udhr_ell_monotonic",
   "udhr_eng",
   "udhr_fra",
   "udhr_hin"
  ],
  "Sino-Tibetan": [
   "udhr_cmn_hant",
   "udhr_cnh",
   "udhr_ctd",
   "udhr_mya"
  ]
 },
 "n_caracteres": 3603,
 "n_familles": 5,
 "n_mots_ws": 566,
 "n_phrases": 42,
 "n_pivots": 1,
 "n_scripts": 10,
 "n_strates": 20,
 "n_textes": 21,
 "scripts": {
  "Adlm": 1,
  "Arab": 2,
  "Cyrl": 1,
  "Deva": 1,
  "Ethi": 1,
  "Grek": 1,
  "Hant": 1,
  "Hebr": 1,
  "Latn": 11,
  "Mymr": 1
 }
}
selection keys dict_keys(['criteres', 'familles_attendues', 'n_pivots', 'n_strates', 'pivot', 'principe'])
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nidx=json.load(open('work/corpus-commun/index.json'))\nsel=idx['selection']\nprint(json.dumps(sel,ensure_ascii=False)[:800])\nids=set()\nfor f in ['udhr_eng','udhr_hin','udhr_bel','udhr_ell_monotonic','udhr_kin','udhr_ewe','udhr_ibo','udhr_fuf_adlm','udhr_ … [501 caractères tronqués]`

  ```
{"criteres": ["présent des deux côtés (même fichier udhr_<clé>.xml)", "article 1 identique après NFC et espaces collapsés", "5 familles parmi les six plus représentées, choisies pour la diversité des écritures (Turkic, 17 paires, écarté : ses écritures sont déjà couvertes)", "4 langues par famille, écritures distinctes quand c'est possible", "français ajouté hors strate comme pivot de Drave"], "familles_attendues": ["Afro-Asiatic", "Atlantic-Congo", "Austronesian", "Indo-European", "Sino-Tibetan"], "n_pivots": 1, "n_strates": 20, "pivot": "fra", "principe": "20 langues stratifiées (5 familles glottolog × 4) + le français, pivot de Drave ; toutes les paires sont exactes après normalisation."}
files 21
udhr_amh.xml 30 1 30
udhr_arb.xml 30 1 30
udhr_bel.xml 30 1 30
udhr_cmn_hant.xml 30 1 30
udhr_cnh.xml 30 1 30
udhr_ctd.xml 30 1 30
udhr_ell_monotonic.xml 30 1 30
udhr_eng.xml 30 1 30
udhr_ewe.xml 30 1 30
udhr_fra.xml 30 1 30
udhr_fuf_adlm.xml 30 1 30
udhr_hau_NE.xml 30 1 30
udhr_heb.xml 30 1 30
udhr_hin.xml 30 1 30
udhr_ibo.xml 30 1 30
udhr_ind.xml 30 1 30
udhr_jav.xml 30 1 30
udhr_kin.xml 30 1 30
udhr_mly_arab.xml 30 1 30
udhr_mya.xml 30 1 30
udhr_tgl.xml 30 1 30
  ```

- **bash** `{"command": "cat > /tmp/proto_multi.py <<'EOF'\nimport zipfile,re\nfrom collections import Counter\ndef parse_usfm(texte):\n    out={}; livre=None; chapitre=None\n    for ligne in texte.splitlines():\n        m=re.match(r\"\\\\id\\s+([A-Z0-9]{3})\",ligne)\n        if m: livre=m.group(1); continue\n  … [1242 caractères tronqués]`

  ```
KJV 36822
WEB 38052
PCM 31069
HIN 31104
ARB 31102
CUV 30951
common 30934
books [('PSA', 2444), ('GEN', 1531), ('JER', 1358), ('ISA', 1288), ('EZK', 1267), ('NUM', 1245), ('EXO', 1211), ('LUK', 1143), ('MAT', 1069), ('JOB', 1064)]
narr 7504
  ```

- **bash** `{"command": "for id in fraLSG fra_fob; do timeout 60 curl -sL -o /tmp/${id}.zip \"https://ebible.org/Scriptures/${id}_usfm.zip\"; echo \"$id $(stat -c%s /tmp/${id}.zip) $(file -b /tmp/${id}.zip | cut -c1-30)\"; done", "description": "Download French Bibles"}`

  ```
fraLSG 3474538 Zip archive data, made by v3.0
fra_fob 2998440 Zip archive data, made by v3.0
  ```

- **bash** `{"command": "timeout 30 curl -s \"https://ebible.org/Scriptures/details.php?id=deu1951\" | sed -e 's/<[^>]*>/ /g' | tr -s ' \\n' ' \\n' | grep -iE 'copyright|public domain|updated|Luther|Language' | head -6; echo '==='; timeout 30 curl -s \"https://ebible.org/Scriptures/details.php?id=spaRV1909\" |  … [164 caractères tronqués]`

  ```
Die Schlachter-Bibel 1951 eBible.org Translations Territories &nbsp; Die Schlachter-Bibel 1951 German Schlachter Bible 1951 Language: [deu] Deutsch German, Standard Title: Die Schlachter-Bibel 1951 German Schlachter Bible 1951 Abbreviation: SCH1951 ID: DEUSCH or deu1951 Copyright © 1951 Genfer Bibelgeschellschaft (Geneva Bible Society) Format Link Browser Bible Study online with Browser Bible Mobile HTML Read Mobile HTML online Zipped mobile HTML deu1951_html.zip ePub 3 and Kindle deu1951.epub PDF PDF file list Crosswire Sword module deu1951eb.zip Plain text canon only chapter files deu1951_readaloud.zip BibleWorks import (VPL) + SQL deu1951_vpl.zip Browser Bible module deu1951_browserBible.zip USFX deu1951_usfx.zip USFM deu1951_usfm.zip XeTeX deu1951_xetex.zip The Holy Bible in German, Schlachter 1951 version Im Anfang schuf Gott den Himmel und die Erde. —Genesis 1:1 Ein Psalm Davids. Der HERR ist mein Hirte; mir wird nichts mangeln. —Psalm 23:1 Trachtet aber zuerst nach dem Reiche Gottes und nach seiner Gerechtigkeit, so wird euch solches alles hinzugelegt werden. —Matthew 6:33 Denn Gott hat die Welt so geliebt, daß er seinen eingeborenen Sohn gab, damit jeder, der an ihn glaubt,
… [2036 caractères tronqués]
  ```

- **bash** `{"command": "timeout 60 curl -sL -o /tmp/spaRV1909.zip \"https://ebible.org/Scriptures/spaRV1909_usfm.zip\"; echo \"$(stat -c%s /tmp/spaRV1909.zip)\"", "description": "Download Spanish Bible"}`

  ```
2384901
  ```

- **bash** `{"command": "cat > /tmp/proto_multi2.py <<'EOF'\nimport zipfile,re\nfrom collections import Counter\ndef parse_usfm(texte):\n    out={}; livre=None; chapitre=None\n    for ligne in texte.splitlines():\n        m=re.match(r\"\\\\id\\s+([A-Z0-9]{3})\",ligne)\n        if m: livre=m.group(1); continue\n … [1235 caractères tronqués]`

  ```
KJV 36822
WEB 38052
PCM 31069
HIN 31104
ARB 31102
CUV 30951
LSG 31170
OST 31107
SPA 31084
common 30880
narr 7499
  ```

- **bash** `{"command": "grep -oE \"details.php\\?id=[^']+'[^>]*>[^<]*Russian[^<]*\" /tmp/ebible.html | head -8; echo '---'; grep -oE \"details.php\\?id=[^']+'[^>]*>[^<]*Portuguese[^<]*\" /tmp/ebible.html | head -6; echo '---'; grep -oE \"details.php\\?id=[^']+'[^>]*>[^<]*German[^<]*\" /tmp/ebible.html | head - … [56 caractères tronqués]`

  ```
details.php?id=rusfb' target='_blank' class='liberation_sans redist'>Russian
details.php?id=rusfb' target='_blank'>Russian Freedom Bible
details.php?id=russyn' target='_blank' class='gentium_plus redist'>Russian
details.php?id=russyn' target='_blank'>Russian Synodal Bible
---
details.php?id=portft' target='_blank' class='dejavu_serif redist'>Portuguese
details.php?id=portft' target='_blank'>Portuguese Translation for Translators
details.php?id=porbr2018' target='_blank' class='dejavu_serif redist'>Portuguese
details.php?id=porbr2018' target='_blank'>Portuguese Bíblia Livre
details.php?id=porblt' target='_blank'>Portuguese Free Bible for All
details.php?id=porbrbsl' target='_blank' class='dejavu_serif redist'>Portuguese
---
details.php?id=deuelo' target='_blank' class='dejavu_serif redist'>German, Standard
details.php?id=deuelo' target='_blank'>German Unrevised Elberfelder Bible
details.php?id=deu1951' target='_blank' class='dejavu_serif redist'>German, Standard
details.php?id=deu1951' target='_blank'>German Schlachter Bible 1951
details.php?id=deuelbbk' target='_blank' class='dejavu_serif redist'>German
details.php?id=deuelbbk' target='_blank'>German ELBBK Bible
details.php?id=deu1
… [125 caractères tronqués]
  ```

- **bash** `{"command": "for id in deu1912 russyn porbr2018; do timeout 90 curl -sL -o /tmp/${id}.zip \"https://ebible.org/Scriptures/${id}_usfm.zip\"; echo \"$id $(stat -c%s /tmp/${id}.zip) $(file -b /tmp/${id}.zip | cut -c1-25)\"; done", "description": "Download German/Russian/Portuguese Bibles"}`

  ```
deu1912 2499701 Zip archive data, made by
russyn 1639834 Zip archive data, made by
porbr2018 1452896 Zip archive data, made by
  ```

- **bash** `{"command": "timeout 30 curl -s \"https://ebible.org/Scriptures/details.php?id=deu1912\" | sed -e 's/<[^>]*>/ /g' | tr -s ' \\n' ' \\n' | grep -iE 'public domain|copyright|updated' | head -4; echo '==='; timeout 30 curl -s \"https://ebible.org/Scriptures/details.php?id=russyn\" | sed -e 's/<[^>]*>/  … [137 caractères tronqués]`

  ```
Lutherbibel 1912 eBible.org Translations Territories &nbsp; Lutherbibel 1912 German Luther Bible 1912 Language: [deu] Deutsch German, Standard Title: Lutherbibel 1912 German Luther Bible 1912 Abbreviation: L1912 ID: GERL12 or deu1912 public domain Format Link Browser Bible Study online with Browser Bible Mobile HTML Read Mobile HTML online Zipped mobile HTML deu1912_html.zip ePub 3 and Kindle deu1912.epub PDF PDF file list Crosswire Sword module deu1912eb.zip Plain text canon only chapter files deu1912_readaloud.zip BibleWorks import (VPL) + SQL deu1912_vpl.zip Browser Bible module deu1912_browserBible.zip USFX deu1912_usfx.zip USFM deu1912_usfm.zip XeTeX deu1912_xetex.zip The Holy Bible in German, Luther 1912 Am Anfang schuf Gott Himmel und Erde. —Genesis 1:1 Ein Psalm Davids. Der HERR ist mein Hirte; mir wird nichts mangeln. —Psalm 23:1 Trachtet am ersten nach dem Reich Gottes und nach seiner Gerechtigkeit, so wird euch solches alles zufallen. —Matthew 6:33 Also hat Gott die Welt geliebt, daß er seinen eingeborenen Sohn gab, auf daß alle, die an ihn glauben, nicht verloren werden, sondern das ewige Leben haben. —John 3:16 Wir wissen aber, daß denen, die Gott lieben, alle Dinge zu
… [1431 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-19 (bash: grep -rln "0.138\|0,138\|signature lexicale\|signature_lexicale" ../Panini ../Panini-Research 2>/dev/null | head -20) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-19"}`

  ```
(no new output)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cat > /tmp/proto_multi3.py <<'EOF'\nimport zipfile,re\nfrom collections import Counter\ndef parse_usfm(texte):\n    out={}; livre=None; chapitre=None\n    for ligne in texte.splitlines():\n        m=re.match(r\"\\\\id\\s+([A-Z0-9]{3})\",ligne)\n        if m: livre=m.group(1); continue\n … [1312 caractères tronqués]`

  ```
KJV 36822
WEB 38052
PCM 31069
HIN 31104
ARB 31102
CUV 30951
LSG 31170
OST 31107
SPA 31084
LUT 31102
RUS 31169
POR 31102
common 30117
narr 7499
  ```

- **bash** `{"command": "cat > /tmp/proto_matrix.py <<'EOF'\nimport zipfile,re,unicodedata,math,random\nfrom collections import Counter\nimport numpy as np\ndef parse_usfm(texte):\n    out={}; livre=None; chapitre=None\n    for ligne in texte.splitlines():\n        m=re.match(r\"\\\\id\\s+([A-Z0-9]{3})\",ligne) … [3325 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-95]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-95", "wait": true, "timeout_ms": 120000}`

  ```
filtered 286
dedup 286
sample 286
       KJV    WEB    PCM    HIN    ARB    CUV    LSG    OST    SPA    LUT    RUS    POR
 KJV   nan   0.99   0.81   0.03   0.00   0.05   0.97   0.97   1.00   1.00   0.00   0.64
 WEB  0.99    nan   0.87   0.02   0.00   0.04   0.99   0.99   0.95   0.94   0.00   0.63
 PCM  0.82   0.88    nan   0.00   0.00   0.00   0.51   0.49   0.47   0.51   0.00   0.50
 HIN  0.03   0.02   0.00    nan   0.00   0.03   0.03   0.00   0.00   0.00   0.00   0.01
 ARB  0.00   0.00   0.00   0.00    nan   0.00   0.00   0.00   0.00   0.00   0.00   0.00
 CUV  0.05   0.04   0.00   0.03   0.00    nan   0.05   0.00   0.00   0.00   0.00   0.01
 LSG  0.95   0.99   0.42   0.03   0.00   0.05    nan   1.00   0.96   0.94   0.00   0.73
 OST  0.95   0.98   0.42   0.00   0.00   0.00   1.00    nan   0.96   0.93   0.00   0.78
 SPA  1.00   0.94   0.44   0.00   0.00   0.01   0.95   0.96    nan   0.99   0.00   0.99
 LUT  1.00   0.96   0.47   0.00   0.00   0.00   0.95   0.95   1.00    nan   0.00   0.45
 RUS  0.00   0.00   0.00   0.00   0.00   0.00   0.00   0.00   0.00   0.00    nan   0.00
 POR  0.60   0.58   0.50   0.01   0.00   0.02   0.67   0.73   0.99   0.42   0.00    nan
[status: completed, ex
… [11 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/count_verses.py <<'EOF'\nimport zipfile,re,unicodedata\nfrom collections import Counter\ndef parse_usfm(texte):\n    out={}; livre=None; chapitre=None\n    for ligne in texte.splitlines():\n        m=re.match(r\"\\\\id\\s+([A-Z0-9]{3})\",ligne)\n        if m: livre=m.group(1) … [2039 caractères tronqués]`

  ```
20 600 all 3732
  KJV dup keys 6
  WEB dup keys 14
  PCM dup keys 4
  HIN dup keys 8
  ARB dup keys 12
  CUV dup keys 26
  LSG dup keys 6
  OST dup keys 12
  SPA dup keys 2
  LUT dup keys 6
  RUS dup keys 14
  POR dup keys 4
  ```

- **bash** `{"command": "sed -n '1,180p' docs/methode/resultats.md", "description": "Read result conventions"}`

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

- **bash** `{"command": "grep -n \"J3.1\\|J3\\|Panini II\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/chantiers.md | head -30", "description": "Find J3.1 state entries"}`

  ```
docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) | la **pragmatique neuronale** ; le **refus r353** ; **J3.1** (retrieval à époque contrôlée) |
docs/pilotage/roadmap.md:253:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 langues** à **0,9687** ; **gold 360** : POS **0,765**, syntagmes exacts **0,190**/**tête
… [438 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"Panini\\|J2\\|J3\\|retrieval\\|corpus commun\" docs/pilotage/en-cours.md | head -40; echo '==='; sed -n '1,80p' docs/pilotage/en-cours.md", "description": "Read en-cours state"}`

  ```
92:- **Panini J2.1/J2.2** : table **14 atomes** ; corpus UDHR **418/438 exactes** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).
===
# En ce moment

**Mis à jour : 2026-11-07, 15 h 05 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.
… [5015 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '80,120p' docs/pilotage/en-cours.md; echo '==='; grep -n \"## \\|### \" docs/pilotage/en-cours.md | head -40", "description": "Read en-cours structure"}`

  ```
- **Ce que font les autres** : **hub**, **S**, **Pensée**.
- **Prochaine action** : la **porte propre (0,29)** ; le **2 048** est fini.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
- **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
- **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; la fusion garde l'heuristique ; **`r035` réglé** (237/238, 0,9958) ; **convention des GV réglée** (F1 **0,7902**, sujet hors du GV + adverbe final, 0 perte d'attachement) ; 
… [3157 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p work/retrieval-epoque/bibles reports\ncp -n data/pidgin.old/eng_kjv_usfm.zip work/retrieval-epoque/bibles/eng-kjv_usfm.zip\ncp -n data/pidgin.old/eng_web_usfm.zip work/retrieval-epoque/bibles/eng-web_usfm.zip\ncp -n data/pidgin.old/pcm_usfm.zip work/retrieval-epoque/bibles/pcm_ … [314 caractères tronqués]`

  ```
total 26848
drwxr-xr-x. 1 stephane stephane     382  7 nov 16:40 .
drwxr-xr-x. 1 stephane stephane      12  7 nov 16:40 ..
-rw-r--r--. 1 stephane stephane 1977649  7 nov 16:40 arbnav_usfm.zip
-rw-r--r--. 1 stephane stephane 1429725  7 nov 16:40 cmn-cu89s_usfm.zip
-rw-r--r--. 1 stephane stephane 2499701  7 nov 16:40 deu1912_usfm.zip
-rw-r--r--. 1 stephane stephane 2771083  7 nov 16:40 eng-kjv_usfm.zip
-rw-r--r--. 1 stephane stephane 3250185  7 nov 16:40 eng-web_usfm.zip
-rw-r--r--. 1 stephane stephane 2998440  7 nov 16:40 fra_fob_usfm.zip
-rw-r--r--. 1 stephane stephane 3474538  7 nov 16:40 fraLSG_usfm.zip
-rw-r--r--. 1 stephane stephane 2243258  7 nov 16:40 hin2017_usfm.zip
-rw-r--r--. 1 stephane stephane 1341437  7 nov 16:40 pcm_usfm.zip
-rw-r--r--. 1 stephane stephane 1452896  7 nov 16:40 porbr2018_usfm.zip
-rw-r--r--. 1 stephane stephane 1639834  7 nov 16:40 russyn_usfm.zip
-rw-r--r--. 1 stephane stephane 2384901  7 nov 16:40 spaRV1909_usfm.zip
===
0fcb07ae4adeeb44925838a0fec22c82dd85b01024feee72164824d680be9490  work/retrieval-epoque/bibles/arbnav_usfm.zip
496f17f4daa62ab125968e9e55118bd3a9c5086a6835a2846da4dc529d470ba0  work/retrieval-epoque/bibles/cmn-cu89s_usfm.zip
76fb83f10
… [1108 caractères tronqués]
  ```

- **bash** `{"command": "cat > tools/retrieval_epoque.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"retrieval_epoque.py — J3.1 : le retrieval inter-langues à ÉPOQUE CONTRÔLÉE.\n\nLA QUESTION. Panini avertit : leur signature lexicale capte l'époque (β +0,138) bien plus que la filiation\n(β +0,049). Un retrieval inter … [38439 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re,pathlib\np=pathlib.Path('tools/retrieval_epoque.py')\ns=p.read_text()\nold='''            # contrôle 1 : permuter les libellés entre concepts dans B\n            perm = list(range(len(cb)))\n            rng.shuffle(perm)\n            Bp = XB[perm]\n           … [2045 caractères tronqués]`

  ```
patched
OK
  ```

- **bash** `{"command": "time python3 tools/retrieval_epoque.py --rapide --n-versets 300 --sortie /tmp/retrieval-epoque-rapide.json 2>&1 | tail -30", "description": "Run quick retrieval test", "timeoutMs": 300000}`

  ```
B7 — lexique des 71 langues…
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_epoque.py", line 766, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_epoque.py", line 731, in main
    b7 = b7_mesure(charge_b7(), graine=a.graine)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_epoque.py", line 262, in b7_mesure
    perm = rng.permutation(len(communs))
           ^^^^^^^^^^^^^^^
AttributeError: 'Random' object has no attribute 'permutation'
[stderr]

real	0m1,057s
user	0m0,976s
sys	0m0,058s
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/retrieval_epoque.py')\ns=p.read_text()\ns=s.replace('perm = rng.permutation(len(communs))','perm = rng.sample(range(len(communs)), len(communs))')\ns=s.replace('perm = rng.permutation(A.shape[0])','perm = rng.sample(range(A.shape[0 … [296 caractères tronqués]`

  ```
ok
B7 — lexique des 71 langues…
  71 langues, 4004 paires ordonnées
UDHR — corpus commun, 21 langues, 30 articles…
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_epoque.py", line 766, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_epoque.py", line 735, in main
    udhr = udhr_mesure(charge_udhr(), graine=a.graine)
                       ~~~~~~~~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_epoque.py", line 356, in charge_udhr
    m = meta[f]
        ~~~~^^^
KeyError: 'udhr_amh'
[stderr]

real	0m11,575s
user	0m11,309s
sys	0m0,262s
  ```

- **bash** `{"command": "head -1 data/udhr/articles_propres.jsonl; python3 - <<'EOF'\nimport json\nf=set()\nfor l in open('data/udhr/articles_propres.jsonl'):\n    f.add(json.loads(l)['fichier'])\nfor x in sorted(f)[:5]: print(x)\nprint('udhr_amh' in f, 'udhr_amh.xml' in f)\nEOF", "description": "Check UDHR fil … [8 caractères tronqués]`

  ```
{"fichier": "udhr_007.xml", "iso3": "cri", "nom": "Sãotomense", "script": "Latn", "art": 1, "texte": "Tudu nguê di mundu ca nancê livli e igual ni dignidade e ni dirêtu. Punda nen ca pensá e nen tê cunxensa, selá nen fé tudu cuá cu tençón de lumón.", "variante": "007"}
udhr_007.xml
udhr_008.xml
udhr_009.xml
udhr_010.xml
udhr_011.xml
False True
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/retrieval_epoque.py')\ns=p.read_text()\nold='''def charge_udhr() -> dict:\n    articles: dict[str, dict[int, str]] = {}\n    for ligne in (RACINE / \"data\" / \"udhr\" / \"articles_propres.jsonl\").read_text(encoding=\"utf-8\").spl … [1996 caractères tronqués]`

  ```
ok
B7 — lexique des 71 langues…
  71 langues, 4004 paires ordonnées
UDHR — corpus commun, 21 langues, 30 articles…
  21 langues, 420 paires
BIBLE — 12 traductions datées…
  300 versets, 132 paires
→ /tmp/retrieval-epoque-rapide.json
[stderr]

real	0m24,792s
user	0m27,125s
sys	0m0,524s
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/retrieval-epoque-rapide.json'))\nfor arm in ['b7','udhr','bible']:\n    x=d[arm]\n    print('====',arm)\n    print(json.dumps({k:x[k] for k in x if k not in ('paires','meta_langues','matrice_top1','traductions')},ensure_ascii=False, … [64 caractères tronqués]`

  ```
==== b7
{
 "n_langues": 71,
 "n_concepts": 35,
 "n_langues_avec_libelle": 71,
 "agregats": {
  "toutes": {
   "n_paires": 4004,
   "top1_moyen": 0.13811021897113393,
   "top1_median": 0.1,
   "ic_bas": 0.034482758620689655,
   "ic_haut": 0.42105263157894735
  },
  "script_meme": {
   "n_paires": 1686,
   "top1_moyen": 0.2157931078334983,
   "top1_median": 0.1875,
   "ic_bas": 0.043478260869565216,
   "ic_haut": 0.5454545454545454
  },
  "script_different": {
   "n_paires": 2318,
   "top1_moyen": 0.08160747927227875,
   "top1_median": 0.07142857142857142,
   "ic_bas": 0.03333333333333333,
   "ic_haut": 0.2
  },
  "famille_meme": {
   "n_paires": 1504,
   "top1_moyen": 0.1685876818378344,
   "top1_median": 0.12,
   "ic_bas": 0.03333333333333333,
   "ic_haut": 0.5526988636363629
  },
  "famille_differente": {
   "n_paires": 2500,
   "top1_moyen": 0.11977497731052693,
   "top1_median": 0.09090909090909091,
   "ic_bas": 0.034482758620689655,
   "ic_haut": 0.3333333333333333
  },
  "script_meme_famille_meme": {
   "n_paires": 690,
   "top1_moyen": 0.2659844556503593,
   "top1_median": 0.23333333333333334,
   "ic_bas": 0.08333333333333333,
   "ic_haut": 0.6990217391304346
  },
  "script_m
… [5223 caractères tronqués]
  ```

- **bash** `{"command": "time python3 tools/retrieval_epoque.py --n-versets 1000 2>&1 | tail -20", "description": "Run full retrieval measurement", "timeoutMs": 600000}`

  ```
B7 — lexique des 71 langues…
  71 langues, 4004 paires ordonnées
UDHR — corpus commun, 21 langues, 30 articles…
  21 langues, 420 paires
BIBLE — 12 traductions datées…
  1000 versets, 132 paires
→ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/retrieval-epoque.json
[stderr]

real	0m36,726s
user	0m38,747s
sys	0m0,531s
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nfor arm in ['b7','udhr','bible']:\n    x=d[arm]\n    print('====',arm)\n    if arm=='bible':\n        print(json.dumps({k:x[k] for k in ['n_traductions','n_langues','n_versets_communs','n_versets_retenus … [561 caractères tronqués]`

  ```
==== b7
{
 "n_langues": 71,
 "n_concepts": 35,
 "agregats": {
  "toutes": {
   "n_paires": 4004,
   "top1_moyen": 0.13811021897113393,
   "top1_median": 0.1,
   "ic_bas": 0.034482758620689655,
   "ic_haut": 0.42105263157894735
  },
  "script_meme": {
   "n_paires": 1686,
   "top1_moyen": 0.2157931078334983,
   "top1_median": 0.1875,
   "ic_bas": 0.043478260869565216,
   "ic_haut": 0.5454545454545454
  },
  "script_different": {
   "n_paires": 2318,
   "top1_moyen": 0.08160747927227875,
   "top1_median": 0.07142857142857142,
   "ic_bas": 0.03333333333333333,
   "ic_haut": 0.2
  },
  "famille_meme": {
   "n_paires": 1504,
   "top1_moyen": 0.1685876818378344,
   "top1_median": 0.12,
   "ic_bas": 0.03333333333333333,
   "ic_haut": 0.5526988636363629
  },
  "famille_differente": {
   "n_paires": 2500,
   "top1_moyen": 0.11977497731052693,
   "top1_median": 0.09090909090909091,
   "ic_bas": 0.034482758620689655,
   "ic_haut": 0.3333333333333333
  },
  "script_meme_famille_meme": {
   "n_paires": 690,
   "top1_moyen": 0.2659844556503593,
   "top1_median": 0.23333333333333334,
   "ic_bas": 0.08333333333333333,
   "ic_haut": 0.6990217391304346
  },
  "script_meme_famille_differente": {
   "
… [911 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nx=d['udhr']\nprint(json.dumps({k:x[k] for k in ['n_langues','n_articles','epoque','agregats','controles']},ensure_ascii=False,indent=1))\nx=d['bible']\nprint('==== bible')\nprint(json.dumps({k:x[k] for k … [488 caractères tronqués]`

  ```
{
 "n_langues": 21,
 "n_articles": 30,
 "epoque": 1948,
 "agregats": {
  "toutes": {
   "n_paires": 420,
   "top1_moyen": 0.049444444444444444,
   "top1_median": 0.03333333333333333,
   "ic_bas": 0.0,
   "ic_haut": 0.18416666666666592
  },
  "script_meme": {
   "n_paires": 112,
   "top1_moyen": 0.09375,
   "top1_median": 0.05,
   "ic_bas": 0.0,
   "ic_haut": 0.8483333333333329
  },
  "script_different": {
   "n_paires": 308,
   "top1_moyen": 0.03333333333333333,
   "top1_median": 0.03333333333333333,
   "ic_bas": 0.03333333333333333,
   "ic_haut": 0.03333333333333333
  },
  "famille_meme": {
   "n_paires": 68,
   "top1_moyen": 0.09411764705882353,
   "top1_median": 0.03333333333333333,
   "ic_bas": 0.03333333333333333,
   "ic_haut": 0.9108333333333335
  },
  "famille_differente": {
   "n_paires": 352,
   "top1_moyen": 0.040814393939393935,
   "top1_median": 0.03333333333333333,
   "ic_bas": 0.0,
   "ic_haut": 0.16666666666666666
  },
  "script_meme_famille_meme": {
   "n_paires": 16,
   "top1_moyen": 0.2916666666666667,
   "top1_median": 0.1,
   "ic_bas": 0.0125,
   "ic_haut": 0.9333333333333333
  },
  "script_meme_famille_differente": {
   "n_paires": 96,
   "top1_moyen": 0.060763
… [5064 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, numpy as np\nd=json.load(open('reports/retrieval-epoque.json'))\n# B7 top pairs with n>=10\nb=d['b7']['paires']\nb2=[p for p in b if p['n_concepts']>=10]\nprint('B7 top 15')\nfor p in sorted(b2,key=lambda x:-x['top1'])[:15]:\n    print(f\"{p['a']}-{p['b'] … [917 caractères tronqués]`

  ```
B7 top 15
nb-nn 0.875 n=16 Latn/Indo-European vs Latn/Indo-European
bs-hr 0.857 n=14 Latn/Indo-European vs Latn/Indo-European
cs-sk 0.826 n=23 Latn/Indo-European vs Latn/Indo-European
nn-nb 0.812 n=16 Latn/Indo-European vs Latn/Indo-European
mk-sr 0.800 n=15 Cyrl/Indo-European vs Cyrl/Indo-European
sr-mk 0.800 n=15 Cyrl/Indo-European vs Cyrl/Indo-European
hr-bs 0.786 n=14 Latn/Indo-European vs Latn/Indo-European
sk-cs 0.783 n=23 Latn/Indo-European vs Latn/Indo-European
sl-bs 0.765 n=17 Latn/Indo-European vs Latn/Indo-European
bs-sl 0.765 n=17 Latn/Indo-European vs Latn/Indo-European
gl-es 0.750 n=16 Latn/Indo-European vs Latn/Indo-European
nl-af 0.750 n=20 Latn/Indo-European vs Latn/Indo-European
ca-es 0.733 n=30 Latn/Indo-European vs Latn/Indo-European
da-nn 0.733 n=15 Latn/Indo-European vs Latn/Indo-European
nn-da 0.733 n=15 Latn/Indo-European vs Latn/Indo-European
B7 bottom 10
fi-sw 0.000 n=11 Latn/Uralic vs Latn/Atlantic-Congo
fr-uz 0.000 n=13 Latn/Indo-European vs Latn/Turkic
gl-sw 0.000 n=10 Latn/Indo-European vs Latn/Atlantic-Congo
is-sw 0.000 n=11 Latn/Inconnue vs Latn/Atlantic-Congo
pt-sw 0.000 n=11 Latn/Indo-European vs Latn/Atlantic-Congo
sq-en 0.000 n=21 Latn/Indo-Europ
… [2020 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nfor l,m in d['b7']['meta_langues'].items():\n    if m['famille']=='Inconnue' or m['script']=='Inconnu':\n        print(l,m)\nEOF", "description": "Check missing B7 metadata"}`

  ```
is {'famille': 'Inconnue', 'script': 'Latn', 'n_concepts': 14}
lo {'famille': 'Inconnue', 'script': 'Laoo', 'n_concepts': 1}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/retrieval_epoque.py')\ns=p.read_text()\ns=s.replace('\"ka\": \"Kartvelian\", \"eo\": \"Constructed\", \"af\": \"Indo-European\",',\n            '\"ka\": \"Kartvelian\", \"eo\": \"Constructed\", \"af\": \"Indo-European\", \"is\": \" … [268 caractères tronqués]`

  ```
ok
B7 — lexique des 71 langues…
  71 langues, 4004 paires ordonnées
UDHR — corpus commun, 21 langues, 30 articles…
  21 langues, 420 paires
BIBLE — 12 traductions datées…
  1000 versets, 132 paires
→ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/retrieval-epoque.json
[stderr]

real	0m39,496s
user	0m40,710s
sys	0m0,538s
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/retrieval_epoque.py')\ns=p.read_text()\n# add helper after bootstrap_proportion\nold='''def bootstrap_proportion(hits: np.ndarray, B: int = 1000, graine: int = 0) -> tuple[float, float]:\n    \"\"\"IC 95 % par bootstrap sur les req … [1674 caractères tronqués]`

  ```
ok
B7 — lexique des 71 langues…
  71 langues, 4004 paires ordonnées
UDHR — corpus commun, 21 langues, 30 articles…
  21 langues, 420 paires
BIBLE — 12 traductions datées…
  1000 versets, 132 paires
→ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/retrieval-epoque.json
[stderr]

real	0m39,918s
user	0m41,108s
sys	0m0,541s
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nfor arm in ['b7','udhr','bible']:\n    print(arm, json.dumps(d[arm]['controles'],ensure_ascii=False))\nprint('b7', json.dumps(d['b7']['agregats'],ensure_ascii=False,indent=0)[:1600])\nprint('bible reg',  … [356 caractères tronqués]`

  ```
b7 {"permutation_libelles_top1_moyen": 0.07009296218989107, "permutation_libelles_chance_moyenne": 0.05533861190370844, "appariement_autre_langue_top1_moyen": 0.15368769523220174, "appariement_autre_langue_n": 187}
udhr {"permutation_articles_top1_moyen": 0.0323015873015873, "chance_moyenne": 0.033333333333333326, "epoques_distinctes": [1948]}
bible {"permutation_versets_top1_moyen": 0.0007045454545454546, "chance_moyenne": 0.001, "n_versets": 1000}
b7 {
"toutes": {
"n_paires": 4004,
"top1_moyen": 0.13811021897113393,
"top1_median": 0.1,
"ic_bas": 0.034482758620689655,
"ic_haut": 0.42105263157894735
},
"script_meme": {
"n_paires": 1686,
"top1_moyen": 0.2157931078334983,
"top1_median": 0.1875,
"ic_bas": 0.043478260869565216,
"ic_haut": 0.5454545454545454
},
"script_different": {
"n_paires": 2318,
"top1_moyen": 0.08160747927227875,
"top1_median": 0.07142857142857142,
"ic_bas": 0.03333333333333333,
"ic_haut": 0.2
},
"famille_meme": {
"n_paires": 1582,
"top1_moyen": 0.17064185036892338,
"top1_median": 0.13333333333333333,
"ic_bas": 0.03333333333333333,
"ic_haut": 0.5535511363636348
},
"famille_differente": {
"n_paires": 2422,
"top1_moyen": 0.11686123430090153,
"top1_median": 0.09090909
… [2726 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/retrieval_epoque.py')\ns=p.read_text()\n# insert helper before B7 section\nmarker='''# ---------------------------------------------------------------------------\n# 1. B7 — le lexique des 71 langues\n# ---------------------------- … [3004 caractères tronqués]`

  ```
ok
B7 — lexique des 71 langues…
  71 langues, 4004 paires ordonnées
UDHR — corpus commun, 21 langues, 30 articles…
  21 langues, 420 paires
BIBLE — 12 traductions datées…
  1000 versets, 132 paires
→ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/retrieval-epoque.json
[stderr]

real	0m40,078s
user	0m42,315s
sys	0m0,538s
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nfor arm in ['b7','udhr']:\n    print('==',arm)\n    print(json.dumps(d[arm]['regression'],ensure_ascii=False,indent=1))\nEOF", "description": "Inspect surface regressions"}`

  ```
== b7
{
 "n_paires": 4004,
 "variables": [
  "script_match",
  "famille_match",
  "chance"
 ],
 "coef": {
  "constante": 0.044874156727354717,
  "script_match": 0.13202811097591444,
  "famille_match": 0.045551580022617916,
  "chance": 0.3549809942727636
 },
 "ic95": {
  "constante": [
   0.0402424105108902,
   0.049713749354300035
  ],
  "script_match": [
   0.1260199164442826,
   0.1373736592361705
  ],
  "famille_match": [
   0.039840497631147345,
   0.051299710128318236
  ],
  "chance": [
   0.2796521140196921,
   0.42392327264439855
  ]
 },
 "r2": 0.40023665765489547
}
== udhr
{
 "n_paires": 420,
 "variables": [
  "script_match",
  "famille_match",
  "chance"
 ],
 "coef": {
  "constante": 0.0239165525733774,
  "script_match": 0.061861313868612655,
  "famille_match": 0.05561891727493886,
  "chance": 0.000797218419112569
 },
 "ic95": {
  "constante": [
   0.015529924683828005,
   0.030826145981691526
  ],
  "script_match": [
   0.03442632498142905,
   0.09444748218213007
  ],
  "famille_match": [
   0.014449192654597364,
   0.11076554853992496
  ],
  "chance": [
   0.0005176641561276178,
   0.0010275381993897124
  ]
 },
 "r2": 0.13957348684925897
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, numpy as np\nd=json.load(open('reports/retrieval-epoque.json'))\np=d['bible']['paires']\nfor lab,f in [('contemporain<=50',lambda x:x['delta_annees']<=50),('decalé>=150',lambda x:x['delta_annees']>=150)]:\n    q=[x for x in p if f(x)]\n    ss=[x for x in  … [1015 caractères tronqués]`

  ```
contemporain<=50 n 42 same script 14 0.7100000000000001 diff script 28 0.002107142857142857
decalé>=150 n 30 same script 18 0.7096111111111111 diff script 12 0.0029999999999999996

same script by delta
0 25 12 0.6696666666666667
25 75 2 0.952
75 150 24 0.6594166666666667
150 300 18 0.7096111111111111

pivot KJV mean delta 0.003300000000000003 n 10
  positives [('OST', 0.005), ('POR', 0.027), ('PCM', 0.087)]
  negatives [('SPA', -0.036), ('LUT', -0.049)]

pivot OST mean delta 0.005699999999999997 n 10
  positives [('KJV', 0.021), ('LUT', 0.026), ('CUV', 0.012), ('WEB', 0.016), ('HIN', 0.014)]
  negatives [('POR', -0.032)]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, numpy as np\nd=json.load(open('reports/retrieval-epoque.json'))\ncs=d['bible']['contrastes']\nsame_script={'OST':'Latn','KJV':'Latn','SPA':'Latn','LSG':'Latn','LUT':'Latn','WEB':'Latn','POR':'Latn','PCM':'Latn'}\nfor piv in ['KJV','OST']:\n    z=[c for c  … [908 caractères tronqués]`

  ```
KJV all mean 0.003300000000000003 same-script mean 0.005166666666666671 n 6
   [('OST', 0.005), ('SPA', -0.036), ('LSG', -0.003), ('LUT', -0.049), ('POR', 0.027), ('PCM', 0.087)]
   IC targets [-0.02883333  0.04283333]
OST all mean 0.005699999999999997 same-script mean 0.005166666666666662 n 6
   [('KJV', 0.021), ('SPA', -0.001), ('LUT', 0.026), ('WEB', 0.016), ('POR', -0.032), ('PCM', 0.001)]
   IC targets [-0.01166667  0.0185    ]
bin 0 25 n 12 mean 0.67
bin 25 75 n 2 mean 0.952
bin 75 150 n 24 mean 0.659
bin 150 300 n 18 mean 0.71
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nfor c,m in d['bible']['traductions'].items():\n    print(f\"| `{c}` | {m['nom']} | {m['langue']} | {m['script']} | {m['famille']} | {m['annee']} | {m['licence']} | `{m['sha256'][:12]}…` |\")\nprint('\\nc … [136 caractères tronqués]`

  ```
| `OST` | Ostervald | français | Latn | Indo-European | 1744 | domaine public | `4631037b5b9e…` |
| `KJV` | King James (texte standard 1769) | anglais | Latn | Indo-European | 1769 | domaine public | `67561758cf58…` |
| `RUS` | Synodal | russe | Cyrl | Indo-European | 1876 | domaine public | `9af20fe73fff…` |
| `SPA` | Reina-Valera 1909 | espagnol | Latn | Indo-European | 1909 | domaine public | `56937c2be9ad…` |
| `LSG` | Louis Segond 1910 | français | Latn | Indo-European | 1910 | domaine public | `64c4fe2a84d9…` |
| `LUT` | Luther 1912 | allemand | Latn | Indo-European | 1912 | domaine public | `76fb83f108dd…` |
| `CUV` | Chinese Union Version | chinois | Hani | Sino-Tibetan | 1919 | domaine public | `496f17f4daa6…` |
| `WEB` | World English Bible | anglais | Latn | Indo-European | 2000 | domaine public | `37aac697f5d9…` |
| `ARB` | New Arabic Version | arabe | Arab | Afro-Asiatic | 2012 | CC BY-SA 4.0 | `0fcb07ae4ade…` |
| `HIN` | Indian Revised Version | hindi | Deva | Indo-European | 2017 | CC BY-SA 4.0 | `7fe5d5b089c4…` |
| `POR` | Bíblia Livre | portugais | Latn | Indo-European | 2018 | CC BY-SA 3.0 | `7ca6742fc1a3…` |
| `PCM` | Nigerian Pidgin | pidgin nigérian | Latn | Cr
… [95 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"INDEX.md\" tools/*.py tools/*.sh | head; echo '==='; grep -n \"INDEX\" tools/revue_documentation.py | head", "description": "Find report index tool"}`

  ```
tools/index_reports.py
tools/surveille_sessions.py
tools/taille_documents.py
===
  ```

- **bash** `{"command": "sed -n '1,80p' tools/revue_documentation.py", "description": "Read doc review tool"}`

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
… [1781 caractères tronqués]
  ```

- **bash** `{"command": "cat > reports/rapport-retrieval-epoque.md <<'MD'\n# J3.1 — Le retrieval inter-langues à époque contrôlée\n\n> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J3.1 · **Date** : 2026-11-07\n> **Verdict** : ✅ **la mesure est faite, et elle renverse l'avertisse … [19288 caractères tronqués]`

  ```
293 reports/rapport-retrieval-epoque.md
  ```

- **bash** `{"command": "sed -n '1,60p' tools/index_reports.py; echo '==='; python3 tools/index_reports.py --help 2>&1 | head -20", "description": "Inspect report index tool"}`

  ```
#!/usr/bin/env python3
"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.

L'index est **exhaustif** et **déterministe** : une ligne par fiche, triée par nom,
avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
et `historique-*`) sont exclus du tableau ; les compteurs de `docs/pilotage/en-cours.md`
comptent, eux, tous les `.md` de `reports/`.

Usage :
    python3 tools/index_reports.py              # réécrit reports/INDEX.md
    python3 tools/index_reports.py --verifier   # ne réécrit rien, sort 1 si périmé
    python3 tools/index_reports.py --aide       # affiche l'aide (ne touche à rien)
"""
from __future__ import annotations

import argparse
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent


def titre(p: pathlib.Path) -> str:
    for ligne in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if ligne.startswith("# "):
            return ligne[2:].strip().replace("|", "—")
    return p.stem.replace("-", " ")


def fiches() -> list[pathlib.Path]:
    return sorted(
        p for p in (RACINE / "reports").glob("*.md")
        if p.name not in ("README.md", "INDEX.md") and not p.n
… [1290 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' journal/2026-11-07/README.md; echo '==='; tail -40 journal/2026-11-07/README.md", "description": "Read journal entry structure"}`

  ```
# 2026-11-07

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-07/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**28 commits** · **5 session(s)** · **6 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 3 | [distribue.md](distribue.md) |
| docs | 12 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 7 | [mesures.md](mesures.md) |
| modele | 1 | [modele.md](modele.md) |
| portes | 4 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `77d26bc7-1657-4c96-83c9-bba7c25dd828` | Tu travailles dans /home/stephane/Data13 | 2026-11-07 00:49 | 1.4 h | [rapport](../sessions/77d26bc7-1657-4c96-83c9-bba7c25dd828/rapport.md) · [digest](../sessions/77d26bc7-1657-4c96-83c9-bba7c25dd828/digest.md) |
| `7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0` | Tu travailles dans /home/stephane/Data13 | 2026-11-07 02:09 | 0.1 h | [rapport](../sessions/7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0/rap
… [8896 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '25,45p' docs/pilotage/roadmap.md; echo '==='; sed -n '245,258p' docs/pilotage/roadmap.md", "description": "Read roadmap lines to update"}`

  ```
## En un coup d'œil

| chantier | ce qu'il couvre | état | prochaine action |
|---|---|---|---|
| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule**
… [11720 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace('**Mis à jour : 2026-11-07, 15 h 05 HNE (heure locale, EST).**',\n            '**Mis à jour : 2026-11-07, 17 h 05 HNE (heure locale, EST).**')\nold='- **Panini J2.1/J2.2** : table … [2344 caractères tronqués]`

  ```
en-cours ok
roadmap ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('journal/2026-11-07/README.md')\ns=p.read_text()\nold='''suivi par git). [Fiche](../../reports/rapport-corpus-commun.md).\n<!-- /notes -->'''\nnew='''suivi par git). [Fiche](../../reports/rapport-corpus-commun.md).\n\n**L'après-midi du 07 … [1056 caractères tronqués]`

  ```
journal ok
  709 fiches → reports/INDEX.md
INDEX_OK
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -80", "description": "Run documentation review"}`

  ```
revue de documentation · 712 fiche(s) · 805 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 711 fichiers, le disque en a 712
     · compteurs : en-cours.md dit 804 JSON, le disque en a 805
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace('| fichiers / JSON de résultats | **711** / **804** |','| fichiers / JSON de résultats | **712** / **805** |')\np.write_text(s)\nprint('ok')\nPY\npython3 tools/revue_documentation … [72 caractères tronqués]`

  ```
ok
  revue de documentation · 712 fiche(s) · 805 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "bash tools/toutes-les-portes.sh > /tmp/portes.out 2>&1; echo EXIT:$?; tail -30 /tmp/portes.out", "description": "Run all gates", "run_in_background": true}`

  ```
started background job bash-132
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -10; echo '---'; python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo '---'; python3 tools/verifie_journal.py 2>&1 | tail -10", "description": "Run auxiliary checks"}`

  ```
schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
---
  en-cours · 1673 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
---
  journal · 44 jour(s) · 171 session(s) · 2366 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nfor a,b in [('en','sw'),('fr','tr'),('en','id'),('fr','vi')]:\n    z=[p for p in d['b7']['paires'] if p['a']==a and p['b']==b]\n    print(a,b,[(p['top1'],p['n_concepts']) for p in z])\nEOF", "description … [26 caractères tronqués]`

  ```
en sw [(0.09090909090909091, 11)]
fr tr [(0.25925925925925924, 27)]
en id [(0.10526315789473684, 19)]
fr vi [(0.07692307692307693, 26)]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, numpy as np\nd=json.load(open('reports/retrieval-epoque.json'))\np=d['bible']['paires']\nq=[x for x in p if x['script_match'] and x['famille_match']]\nprint('same script+family',len(q),'mean',np.mean([x['top1'] for x in q]),'min',min(x['top1'] for x in q) … [189 caractères tronqués]`

  ```
same script+family 42 mean 0.8161428571428571 min 0.136 max 0.998
POR LUT 0.136
LUT POR 0.14
POR KJV 0.278
KJV POR 0.297
POR WEB 0.304
WEB POR 0.324
POR LSG 0.427
LSG POR 0.445
POR OST 0.455
OST POR 0.477
OST LUT 0.901
LSG LUT 0.927
OST KJV 0.933
LUT LSG 0.937
WEB LUT 0.948
POR SPA 0.948
SPA POR 0.953
LSG KJV 0.954
SPA LSG 0.957
LUT OST 0.959
OST WEB 0.96
WEB SPA 0.96
LUT WEB 0.962
LSG SPA 0.963
OST SPA 0.964
WEB LSG 0.967
SPA WEB 0.968
KJV LSG 0.97
KJV OST 0.971
LSG WEB 0.976
WEB OST 0.976
SPA OST 0.98
SPA LUT 0.992
KJV SPA 0.996
KJV WEB 0.996
SPA KJV 0.996
LUT SPA 0.996
WEB KJV 0.996
OST LSG 0.997
KJV LUT 0.997
LUT KJV 0.997
LSG OST 0.998
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\np=[x for x in d['udhr']['paires'] if not x['script_match']]\nprint('n',len(p),'max',max(x['top1'] for x in p),'min',min(x['top1'] for x in p))\nprint([(x['a'],x['b'],x['top1']) for x in p if x['top1']>0. … [68 caractères tronqués]`

  ```
n 308 max 0.03333333333333333 min 0.03333333333333333
[]
  ```

- **bash** `{"command": "timeout 20 curl -s \"https://ebible.org/Scriptures/details.php?id=porbr2018\" | sed -e 's/<[^>]*>/ /g' | tr -s ' \\n' ' \\n' | grep -iE 'creative commons|public domain|copyright' | head -4", "description": "Verify Portuguese license"}`

  ```
Bíblia Livre eBible.org Translations Territories &nbsp; Bíblia Livre Portuguese Bíblia Livre Language: [por] Português Portuguese Dialect: Brasil &nbsp; Title: Bíblia Livre Portuguese Bíblia Livre Abbreviation: BL ID: PORBLJ or porbr2018 Copyright © 2018 Diego Santos, Mario Sérgio, e Marco Teles Format Link Browser Bible Study online with Browser Bible Mobile HTML Read Mobile HTML online Zipped mobile HTML porbr2018_html.zip ePub 3 and Kindle porbr2018.epub PDF PDF file list Crosswire Sword module porbr2018eb.zip Plain text canon only chapter files porbr2018_readaloud.zip BibleWorks import (VPL) + SQL porbr2018_vpl.zip Browser Bible module porbr2018_browserBible.zip USFX porbr2018_usfx.zip USFM porbr2018_usfm.zip XeTeX porbr2018_xetex.zip The Holy Bible in Brazilian Portuguese, updated from from the 1819 translation by João Ferreira de Almeida, Textus Receptus edition A Bíblia Sagrada em português do Brasil, atualizada a partir da tradução de 1819 de João Ferreira de Almeida, edição Textus Receptus No princípio criou Deus os céus e a terra. —Genesis 1:1 Salmo de Davi: O SENHOR é meu pastor, nada me faltará. —Psalm 23:1 Mas buscai primeiramente o Reino de Deus e a sua justiça, e tod
… [1374 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/retrieval_epoque.py')\ns=p.read_text()\ns=s.replace('\"https://ebible.org/Scriptures/porbr2018_usfm.zip\", \"porbr2018_usfm.zip\"),',\n            '\"https://ebible.org/Scriptures/porbr2018_usfm.zip\", \"porbr2018_usfm.zip\"),')\ns … [3059 caractères tronqués]`

  ```
script ok
report ok
208:années** donne **p = 0,19** (500 permutations). Le coefficient d'écriture (0,609) vaut **18 fois** celui des dates par siècle (0,034) ; la famille
224:l'écart d'années n'a **aucun effet détectable** à écriture contrôlée (−0,034 par siècle, IC incluant 0).
  ```

- **bash** `{"command": "python3 tools/retrieval_epoque.py --n-versets 1000 2>&1 | tail -5; python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nprint(d['bible']['traductions']['POR']['licence'])\nEOF", "description": "Rerun with license fix", "timeoutMs": 300000}`

  ```
UDHR — corpus commun, 21 langues, 30 articles…
  21 langues, 420 paires
BIBLE — 12 traductions datées…
  1000 versets, 132 paires
→ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/retrieval-epoque.json
CC BY 4.0
  ```

- **bash** `{"command": "sed -n '1,30p' reports/rapport-retrieval-epoque.md; echo '...'; sed -n '100,150p' reports/rapport-retrieval-epoque.md; echo '...'; sed -n '190,235p' reports/rapport-retrieval-epoque.md", "description": "Review report sections"}`

  ```
# J3.1 — Le retrieval inter-langues à époque contrôlée

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J3.1 · **Date** : 2026-11-07
> **Verdict** : ✅ **la mesure est faite ; elle borne l'avertissement** —
> dans ce retrieval de **surface**, **l'écriture domine** (+0,609 ; IC 95 % [0,529 ; 0,702]), la **famille**
> compte ensuite (+0,181 [0,106 ; 0,253]), et **l'écart d'années ne pèse pas** (−0,034 par siècle
> [−0,075 ; +0,009], p = 0,19 par permutation). À écriture contrôlée, les couples **contemporains** et
> **décalés** sont au **même niveau** : **0,710 vs 0,710**. Le renversement brut (0,238 vs 0,427) est un
> **effet de composition** : les couples décalés contiennent **60 %** de paires de même écriture, les
> contemporains **33 %**. **L'époque ne domine pas ici ; elle n'est pas nulle pour autant : sans contrôle,
> elle fausse la comparaison.**
> **Dispositif** : trois corpus, un même retrieval de surface (n-grammes de caractères, TF-IDF, cosinus,
> top-1) ; **B7** (71 langues, 35 concepts, libellés Wikidata 2026), **UDHR** (21 langues du corpus commun,
> 30 articles, 1948), **BIBLE** (12 traductions datées de 1744 à 2019, 1 000 versets narratif
… [6970 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-epoque.md')\ns=p.read_text()\ns=s.replace(\"**L'époque ne domine pas ici ; elle n'est pas nulle pour autant : sans contrôle,\\n> elle fausse la comparaison.**\",\n            \"**L'époque ne domine pas ici ; le  … [369 caractères tronqués]`

  ```
ok
> dans ce retrieval de **surface**, **l'écriture domine** (+0,609 ; IC 95 % [0,529 ; 0,702]), la **famille**
> compte ensuite (+0,181 [0,106 ; 0,253]), et **l'écart d'années ne pèse pas** (−0,034 par siècle
> [−0,075 ; +0,009], p = 0,19 par permutation). À écriture contrôlée, les couples **contemporains** et
> **décalés** sont au **même niveau** : **0,710 vs 0,710**. Le renversement brut (0,238 vs 0,427) est un
> **effet de composition** : les couples décalés contiennent **60 %** de paires de même écriture, les
> contemporains **33 %**. **L'époque ne domine pas ici ; le confondant de composition, lui, n'est pas nul : sans
> contrôle, il fausse la comparaison.**
> **Dispositif** : trois corpus, un même retrieval de surface (n-grammes de caractères, TF-IDF, cosinus,
> top-1) ; **B7** (71 langues, 35 concepts, libellés Wikidata 2026), **UDHR** (21 langues du corpus commun,
> 30 articles, 1948), **BIBLE** (12 traductions datées de 1744 à 2019, 1 000 versets narratifs alignés).
> **Contrôles négatifs** : cibles mélangées (permutation sans point fixe) pour les trois bras ; années
  ```

- **job_output** `{"job_id": "bash-132", "wait": true, "timeout_ms": 300000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ls -lh reports/retrieval-epoque.json reports/rapport-retrieval-epoque.md; python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nprint('top keys',list(d))\nprint('b7 pairs',len(d['b7']['paires']),'udhr',len(d['udhr']['paires']),'bible',len(d['bible']['paires … [179 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane  20K  7 nov 16:49 reports/rapport-retrieval-epoque.md
-rw-r--r--. 1 stephane stephane 2,1M  7 nov 16:49 reports/retrieval-epoque.json
top keys ['tache', 'titre', 'date', 'methode', 'b7', 'udhr', 'bible']
b7 pairs 4004 udhr 420 bible 132
b7 meta all True
  ```

- **job_output** `{"job_id": "bash-132", "wait": true, "timeout_ms": 300000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -20; echo '---'; python3 tools/taille_documents.py 2>&1 | tail -15", "description": "Run doc review and size check"}`

  ```
revue de documentation · 712 fiche(s) · 805 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---
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
     · 40 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4043 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 tools/verifie_etat_a_jour.py 2>&1 | tail -20; echo '---'; python3 tools/index_reports.py --verifier && echo INDEX_OK", "description": "Check state freshness and index"}`

  ```
état · dernier fait 9c7f71dc · dernier état 9c7f71dc
  ✅ aucun fait commité après le dernier état
---
INDEX_OK
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | head -30", "description": "See T0 breakdown"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    7209    383   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2783    190   T1   2800  reports/README.md
    2404    162   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [519 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\nold='''- **Panini J2.1/J2.2/J3.1** : table **14 atomes** ; corpus UDHR **418/438 exactes** ; **J3.1 retrieval à époque contrôlée** : **l'écriture domine** (+0,609), l'**époque ne pèse pas** à … [916 caractères tronqués]`

  ```
ok
  T0 max : 4024 mots (budget 4 000)
  ❌ 1 violation(s) :
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | head -5; echo '---'; python3 - <<'EOF'\nimport pathlib,re\nfor p in ['AGENTS.md','docs/pilotage/en-cours.md','docs/methode/resultats.md','docs/methode/panini-nipada.md']:\n    t=pathlib.Path(p).read_text()\n    print(p,len(re.findall(r\"\\S+\",t) … [50 caractères tronqués]`

  ```
en-cours · 1654 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
---
AGENTS.md 1196
docs/pilotage/en-cours.md 1654
docs/methode/resultats.md 524
docs/methode/panini-nipada.md 262
  ```

- **bash** `{"command": "grep -n \"T0\\|AGENTS\\|tâche\" tools/taille_documents.py | head -30; sed -n '1,80p' tools/taille_documents.py", "description": "Read T0 budget definition"}`

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
154:        violations.append(f"T0 : {t0} mots (AGENTS + en-cours + une tâche) > budget 4 000")
163:    print(f"  T0 max : {t0} mots (budget 4 000)")
#!/usr/bin/env python3
"""taille_documents.py — le budget de contexte et la cohésion des documents.

Ce que l'outil vérifie :
  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
  2. la cohésion minimale : un titre, un résumé 
… [3262 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace('**J3.1 : l\\'écriture domine, l\\'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19) ; le brut (0,238 vs 0,427) est un effet de composition**',\n            '**J3.1  … [700 caractères tronqués]`

  ```
ok
  T0 max : 4008 mots (budget 4 000)
  ❌ 1 violation(s) :
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace('**2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ;', '**2 048 fini** ;')\np.write_text(s)\nprint('ok')\nPY\npython3 tools/taille_documents.py 2>&1 | grep -E \"T0 max| … [46 caractères tronqués]`

  ```
ok
  T0 max : 4000 mots (budget 4 000)
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; python3 tools/verifie_en_cours.py 2>&1 | head -3", "description": "Verify budget and state"}`

  ```
1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 40 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  en-cours · 1630 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -10; echo '---'; python3 tools/verifie_etat_a_jour.py 2>&1 | tail -5; echo '---'; python3 tools/index_reports.py --verifier && echo INDEX_OK", "description": "Rerun doc checks after trims"}`

  ```
revue de documentation · 712 fiche(s) · 805 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---
  état · dernier fait 9c7f71dc · dernier état 9c7f71dc
  ✅ aucun fait commité après le dernier état
---
INDEX_OK
  ```

- **job_output** `{"job_id": "bash-132", "wait": true, "timeout_ms": 300000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps aux | grep -E \"toutes-les-portes|porte-|pytest|python3\" | grep -v grep | head -15; echo '==='; tail -20 /tmp/portes.out", "description": "Check gate progress"}`

  ```
root        2062  0.0  0.0 145716 53608 ?        Ssl  nov03   0:01 /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
root        2233  0.1  0.0 436152 32680 ?        Ssl  nov03  10:01 /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
stephane    3002  0.1  0.0 283252 32588 ?        Ssl  nov03   7:23 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
stephane  216359  0.0  0.0   5848  2508 ?        S    12:18   0:00 timeout 25200 python3 tools/chantier/superviseur.py boucle --budget 21600 --timeout 5400
stephane  216362  0.1  0.0  26656 23592 ?        S    12:18   0:21 python3 tools/chantier/superviseur.py boucle --budget 21600 --timeout 5400
stephane  820703  0.0  0.0   7832  4240 ?        Ss   15:11   0:00 bash tools/toutes-les-portes.sh
stephane 1208651  0.0  0.0   7700  4140 ?        Ss   16:48   0:00 bash -c bash tools/toutes-les-portes.sh > /tmp/portes.out 2>&1; echo EXIT:$?; tail -30 /tmp/portes.out
stephane 1208666  0.0  0.0   7832  4272 ?        S    16:48   0:00 bash tools/toutes-les-portes.sh
stephane 1377995  0.0  0.0   5848  2504 ?        S    17:04   0:00 timeout 1800 bash tools/porte-cycle-c2.sh
stephane 1377996  0.0  0.0   7832  4300 ?  
… [3547 caractères tronqués]
  ```

- **bash** `{"command": "git status --short; echo '==='; git diff --stat", "description": "Review git status and diff stat"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/references-non-regression.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-07/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89/digest.md
 M journal/sessions/session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89/rapport.md
 M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/superviseur.py
 m tools/structures
?? journal/sessions/session-932afd57-1363-4133-b6f1-64f7d937f38d/
?? reports/corpus-commun.json
?? reports/rapport-corpus-commun.md
?? reports/rapport-retrieval-epoque.md
?? reports/rapport-s-paragraphes.md
?? reports/retrieval-epoque.json
?? tools/corpus_commun.py
?? tools/retrieval_epoque.py
===
 docs/pilotage/en-cours.md                          |  10 +-
 d
… [1291 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-07/README.md reports/INDEX.md | sed -n '1,220p'", "description": "Inspect diffs of shared files"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index d923018f..5a197a0a 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-07, 17 h 05 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -85,11 +85,11 @@
 ## Ce qui est en cours
 
 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
-- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
+- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
 - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-i
… [17499 caractères tronqués]
  ```

- **bash** `{"command": "tail -40 /tmp/portes.out; echo '==='; ps aux | grep -E \"toutes-les-portes|porte-\" | grep -v grep | wc -l", "description": "Check gates progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-1107-16h48
  porte-adaptateur-sortie ✅                          76 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         183 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          17 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          22 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          71 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                         192 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅ 
… [694 caractères tronqués]
  ```

- **bash** `{"command": "ps -eo pid,etime,pcpu,cmd | grep -E \"porte-|drave-core|python\" | grep -v grep | head -20", "description": "Check running gate commands"}`

  ```
2062  3-21:31:51  0.0 /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
   2233  3-21:31:49  0.1 /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
   3002  3-21:31:45  0.1 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
   3291  3-21:31:39  2.0 /home/stephane/.local/share/pipx/venvs/docwatch/bin/python -E /home/stephane/.local/bin/docwatch --config /home/stephane/.config/docwatch/config.toml --no-browser
 216359    04:47:04  0.0 timeout 25200 python3 tools/chantier/superviseur.py boucle --budget 21600 --timeout 5400
 216362    04:47:04  0.1 python3 tools/chantier/superviseur.py boucle --budget 21600 --timeout 5400
1377995       01:18  0.0 timeout 1800 bash tools/porte-cycle-c2.sh
1377996       01:18  0.0 bash tools/porte-cycle-c2.sh
1390213       00:18  1.2 python3 tools/derouler.py --topologie /tmp/porte-cycle-c2/cycle.json --pas-temps 4 --morceau /tmp/porte-cycle-c2/morceau.txt --limite 128 --sortie /tmp/porte-cycle-c2/cycle2 --moteur ./drave-core/target/release/drave --modele models/Qwen2.5-0.5B-Q8_0.gguf --travail /tmp/porte-cycle-c2/travail-cycle2
1392502       00:07  0.0 timeout 1800 bash tools/porte-reflexe.sh
1392503       00:07  0.0 bash to
… [1219 caractères tronqués]
  ```

- **bash** `{"command": "/home/stephane/gpu-env/bin/python -c \"import torch, transformers, sentence_transformers; print(torch.__version__, transformers.__version__, sentence_transformers.__version__)\" 2>&1 | head -5", "description": "Check GPU env ML libraries"}`

  ```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import torch, transformers, sentence_transformers; print(torch.__version__, transformers.__version__, sentence_transformers.__version__)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'sentence_transformers'
  ```

- **bash** `{"command": "/home/stephane/gpu-env/bin/python -c \"import torch, transformers; print(torch.__version__, transformers.__version__); print(torch.cuda.is_available())\" 2>&1 | head -5", "description": "Check torch in GPU env"}`

  ```
2.11.0+cu130 5.15.0
True
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, math\nd=json.load(open('reports/retrieval-epoque.json'))\nfor arm in ['b7','udhr','bible']:\n    ps=d[arm]['paires']\n    assert all(0<=p['top1']<=1 for p in ps), arm\n    assert all(0<=p['controle_permutation']<=1 for p in ps), arm\n    assert all(math.i … [441 caractères tronqués]`

  ```
b7 4004 ok
udhr 420 ok
bible 132 ok
B7 langs in pairs 64
diag [None, None, None, None, None, None, None, None, None, None, None, None]
contrasts 20
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nallL=set(d['b7']['meta_langues'])\ninp=set()\nfor p in d['b7']['paires']: inp.add(p['a']); inp.add(p['b'])\nprint('missing',sorted(allL-inp))\nfor l in sorted(allL-inp): print(l,d['b7']['meta_langues'][l … [65 caractères tronqués]`

  ```
missing ['am', 'km', 'ky', 'lo', 'mt', 'si', 'yo']
am {'famille': 'Afro-Asiatic', 'script': 'Ethi', 'n_concepts': 4}
km {'famille': 'Austroasiatic', 'script': 'Khmr', 'n_concepts': 3}
ky {'famille': 'Turkic', 'script': 'Cyrl', 'n_concepts': 2}
lo {'famille': 'Tai-Kadai', 'script': 'Laoo', 'n_concepts': 1}
mt {'famille': 'Afro-Asiatic', 'script': 'Latn', 'n_concepts': 4}
si {'famille': 'Indo-European', 'script': 'Sinh', 'n_concepts': 4}
yo {'famille': 'Atlantic-Congo', 'script': 'Latn', 'n_concepts': 3}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/retrieval_epoque.py')\ns=p.read_text()\nold='''    return {\n        \"n_langues\": len(langues), \"n_concepts\": len(b7[\"concepts\"]),\n        \"n_langues_avec_libelle\": len(matrices),\n        \"meta_langues\": meta,'''\nnew=' … [1312 caractères tronqués]`

  ```
ok
UDHR — corpus commun, 21 langues, 30 articles…
  21 langues, 420 paires
BIBLE — 12 traductions datées…
  1000 versets, 132 paires
→ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/retrieval-epoque.json
[stderr]
  File "<stdin>", line 5
    new='**4 004 paires ordonnées**, 71 langues au lexique, 35 concepts. Le top-1 moyen est **0,138** ; le hasard moyen\nest **0,055** (1/k, k variable). **64 langues** ont au moins 5 concepts communs avec une autre et entrent dans\nles paires ; les **7** autres (`am`, `km`, `ky`, `lo`, `mt`, `si`, `yo`) n'ont que 1 à 4 concepts et sortent de\nla mesure appariée. Les 2×2 :'
                                                                                                                                                                                                                                                                                                                    ^^^
SyntaxError: invalid syntax
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-epoque.md')\ns=p.read_text()\nold=\"\"\"**4 004 paires ordonnées**, 71 langues, 35 concepts. Le top-1 moyen est **0,138** ; le hasard moyen est\n**0,055** (1/k, k variable). Les 2×2 :\"\"\"\nnew=\"\"\"**4 004 pa … [640 caractères tronqués]`

  ```
ok
64 ['am', 'km', 'ky', 'lo', 'mt', 'si', 'yo']
  ```

- **bash** `{"command": "git ls-files reports/rapport-atomes-niveaux.md reports/rapport-corpus-commun.md reports/corpus-commun.json tools/corpus_commun.py; echo '==='; git log --oneline -1 -- reports/rapport-atomes-niveaux.md; echo '==='; git status --short reports/rapport-atomes-niveaux.md", "description": "Ch … [32 caractères tronqués]`

  ```
reports/rapport-atomes-niveaux.md
===
9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE
===
  ```

- **bash** `{"command": "tail -25 /tmp/portes.out; echo '==='; ps -eo pid,etime,pcpu,cmd | grep -E \"porte-\" | grep -v grep | head", "description": "Check gates progress again"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-1107-16h48
  porte-adaptateur-sortie ✅                          76 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         183 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          17 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          22 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          71 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                         192 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅ 
… [1651 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, numpy as np\nd=json.load(open('reports/retrieval-epoque.json'))\np=d['b7']['paires']\nX=np.array([[1,x['script_match'],x['famille_match'],np.log(x['n_concepts']),x['chance']] for x in p],float)\ny=np.array([x['top1'] for x in p])\nc,*_=np.linalg.lstsq(X,y … [264 caractères tronqués]`

  ```
coef [ 0.14676638  0.13368463  0.04805022 -0.03238741  0.0702812 ]
weighted [ 0.1046608   0.15005505  0.05167496 -0.02107675  0.10757041]
  ```

- **bash** `{"command": "git diff --check -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-07/README.md reports/rapport-retrieval-epoque.md tools/retrieval_epoque.py; echo EXIT:$?", "description": "Check whitespace errors"}`

  ```
EXIT:0
  ```

- **bash** `{"command": "python3 -m py_compile tools/retrieval_epoque.py && python3 tools/retrieval_epoque.py --rapide --n-versets 200 --sortie /tmp/retrieval-check.json >/tmp/retrieval-check.log 2>&1; echo EXIT:$?; tail -5 /tmp/retrieval-check.log", "description": "Smoke test quick mode", "timeoutMs": 300000}`

  ```
EXIT:0
UDHR — corpus commun, 21 langues, 30 articles…
  21 langues, 420 paires
BIBLE — 12 traductions datées…
  300 versets, 132 paires
→ /tmp/retrieval-check.json
  ```

- **bash** `{"command": "tail -20 /tmp/portes.out; echo '==='; ps -eo pid,etime,pcpu,cmd | grep -E \"porte-\" | grep -v grep | head -5", "description": "Check gates progress"}`

  ```
porte-adaptateur-sortie ✅                          76 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         183 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          17 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          22 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          71 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                         192 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅                         119 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard   
… [1546 caractères tronqués]
  ```

- **bash** `{"command": "git add tools/retrieval_epoque.py reports/rapport-retrieval-epoque.md reports/retrieval-epoque.json reports/rapport-corpus-commun.md reports/corpus-commun.json tools/corpus_commun.py docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-07/README.md reports/INDEX.md\ngit di … [64 caractères tronqués]`

  ```
docs/pilotage/en-cours.md           |    10 +-
 docs/pilotage/roadmap.md            |     4 +-
 journal/2026-11-07/README.md        |    19 +
 reports/INDEX.md                    |     5 +-
 reports/corpus-commun.json          |  1501 +
 reports/rapport-corpus-commun.md    |   330 +
 reports/rapport-retrieval-epoque.md |   295 +
 reports/retrieval-epoque.json       | 88655 ++++++++++++++++++++++++++++++++++
 tools/corpus_commun.py              |  1154 +
 tools/retrieval_epoque.py           |   815 +
 10 files changed, 92780 insertions(+), 8 deletions(-)
  ```

- **bash** `{"command": "git diff --cached --check; echo EXIT:$?; echo '==='; git diff --cached -- docs/pilotage/en-cours.md | head -40", "description": "Check staged diff"}`

  ```
EXIT:0
===
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index d923018f..5a197a0a 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-07, 17 h 05 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -85,11 +85,11 @@
 ## Ce qui est en cours
 
 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
-- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
+- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
 - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (
… [2261 caractères tronqués]
  ```

- **bash** `{"command": "tail -15 /tmp/portes.out; echo '==='; ps -eo pid,etime,pcpu,cmd | grep -E \"porte-\" | grep -v grep | head -5", "description": "Check gates progress"}`

  ```
porte-bloc-linguistique ✅                          22 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          71 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                         192 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅                         119 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard        ✅                          38 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne
  porte-cerveau          ✅                          10 s    ✅ porte tenue (quatre facultés composent, chacune reste active, le tout est déterministe)
  porte-consolidation    ✅                          81 s    ✅ porte tenue (fusion exacte : nulle ⇒ identique, réelle ⇒ visible, lecteur ⇒ hors fichier)
  porte-coupe            ✅                         162 s    ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % 
… [1003 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-epoque.md')\ns=p.read_text()\nold=\"\"\"**0,90 à 1,00**, sauf le portugais 2018 (0,14–0,48) ; les paires avec le pidgin vont de 0,17 à 0,66. **La date n'ordonne pas ces valeurs ; l'écriture et la\ntradition de t … [526 caractères tronqués]`

  ```
ok
EXIT:0
  ```

- **bash** `{"command": "tail -10 /tmp/portes.out; echo '==='; ps -eo pid,etime,pcpu,cmd | grep -E \"porte-\" | grep -v grep | head -3", "description": "Check gates progress"}`

  ```
porte-bus-socket       ✅                         119 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard        ✅                          38 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne
  porte-cerveau          ✅                          10 s    ✅ porte tenue (quatre facultés composent, chacune reste active, le tout est déterministe)
  porte-consolidation    ✅                          81 s    ✅ porte tenue (fusion exacte : nulle ⇒ identique, réelle ⇒ visible, lecteur ⇒ hors fichier)
  porte-coupe            ✅                         162 s    ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit
  porte-cycle-c2         ✅                         142 s    ✅ porte tenue (chaîne exacte · pas 1 exact · borné · coût dit · trajectoire déterministe ·
  porte-deepseek         ✅                           1 s    ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
  porte-delais           ✅                          25 s    ✅ le temps, lui, augmente : 9.64 s → 11.94 s (+2.3 s ≈ 50 ms × 64 pas)
  porte-diff-couche      ✅                          22 s    ✅ 
… [357 caractères tronqués]
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,cmd | grep -E \"1392502|1392503|1414834|1414835|reflexe|echange\" | grep -v grep; echo '==='; ls -lt work/portes-1107-16h48 2>/dev/null | head", "description": "Inspect stuck gate processes"}`

  ```
1392502  820703       02:48  0.0 timeout 1800 bash tools/porte-reflexe.sh
1392503 1392502       02:48  0.0 bash tools/porte-reflexe.sh
1414834 1208666       00:43  0.0 timeout 1800 bash tools/porte-echange-experts.sh
1414835 1414834       00:43  0.0 bash tools/porte-echange-experts.sh
1433998 1414835       00:11  0.0 bash tools/porte-echange-experts.sh
1434000 1433998       00:11  0.0 bash tools/porte-echange-experts.sh
1436075 1392503       00:05  156 /home/stephane/gpu-env/bin/python tools/n4_dessin_b.py --objectif tronque --train 1 --val 2 --test 3 --epoques 1 --graine 0 --rang 4 --alpha 8 --bras lora+adaptateur --lots 1 --accord --json /tmp/tmp.vFDG0PcMMy/assemblage/accord.json --sans-portes
===
total 88
-rw-r--r--. 1 stephane stephane  165  7 nov 17:08 porte-echange-experts.log
-rw-r--r--. 1 stephane stephane  434  7 nov 17:07 registre.txt
-rw-r--r--. 1 stephane stephane 1175  7 nov 17:07 porte-document.log
-rw-r--r--. 1 stephane stephane  452  7 nov 17:07 porte-diff-couche.log
-rw-r--r--. 1 stephane stephane  577  7 nov 17:07 porte-delais.log
-rw-r--r--. 1 stephane stephane  678  7 nov 17:06 porte-deepseek.log
-rw-r--r--. 1 stephane stephane 1340  7 nov 17:06 porte-cycle-c2.l
… [142 caractères tronqués]
  ```

- **bash** `{"command": "cat work/portes-1107-16h48/registre.txt", "description": "Read gate register"}`

  ```
porte-adaptateur-sortie 0 76
porte-audit-drapeaux 0 183
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 17
porte-bloc-linguistique 0 22
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 71
porte-bus 0 192
porte-bus-socket 0 119
porte-c4-retard 0 38
porte-cerveau 0 10
porte-consolidation 0 81
porte-coupe 0 162
porte-cycle-c2 0 142
porte-deepseek 0 1
porte-delais 0 25
porte-diff-couche 0 22
porte-document 0 6
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -5; echo '---'; python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation\"; echo '---'; python3 tools/verifie_en_cours.py 2>&1 | head -3", "description": "Final doc checks before commit"}`

  ```
revue de documentation · 712 fiche(s) · 805 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---
  T0 max : 4000 mots (budget 4 000)
---
  en-cours · 1630 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "sleep 60; wc -l work/portes-1107-16h48/registre.txt; tail -10 work/portes-1107-16h48/registre.txt; echo '==='; tail -5 /tmp/portes.out", "description": "Wait and check gate register", "timeoutMs": 90000}`

  ```
21 work/portes-1107-16h48/registre.txt
porte-c4-retard 0 38
porte-cerveau 0 10
porte-consolidation 0 81
porte-coupe 0 162
porte-cycle-c2 0 142
porte-deepseek 0 1
porte-delais 0 25
porte-diff-couche 0 22
porte-document 0 6
porte-echange-experts 0 63
===
  porte-deepseek         ✅                           1 s    ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
  porte-delais           ✅                          25 s    ✅ le temps, lui, augmente : 9.64 s → 11.94 s (+2.3 s ≈ 50 ms × 64 pas)
  porte-diff-couche      ✅                          22 s    ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé
  porte-document         ✅                           6 s  ✅ porte document verte
  porte-echange-experts  ✅                          63 s    PORTE TENUE
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,cmd | grep -E \"n4_dessin|reflexe|entrainer\" | grep -v grep | head -5; echo '==='; tail -10 work/portes-1107-16h48/porte-reflexe.log 2>/dev/null", "description": "Check reflexe gate"}`

  ```
1475692 1475356       00:14  0.0 timeout 1800 /home/stephane/gpu-env/bin/python -u tools/entrainer_moteur.py --famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 --lot 32 --lr 3e-4 --graine 1 --pas 200 --eval-tous 200 --poids-lognormaux --verifier-sauvegarde --sortie /tmp/porte-sauvegarde-modele/lognormal
1475693 1475692       00:14  129 /home/stephane/gpu-env/bin/python -u tools/entrainer_moteur.py --famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 --lot 32 --lr 3e-4 --graine 1 --pas 200 --eval-tous 200 --poids-lognormaux --verifier-sauvegarde --sortie /tmp/porte-sauvegarde-modele/lognormal
===
[exit code: 1]
  ```

- **bash** `{"command": "cat work/portes-1107-16h48/porte-reflexe.log 2>/dev/null | tail -30; echo '==='; ls -la work/portes-1107-16h48/porte-reflexe*", "description": "Read reflexe log"}`

  ```
===
[stderr]
ls: cannot access 'work/portes-1107-16h48/porte-reflexe*': No such file or directory
[exit code: 2]
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1208666 || $1==1208666 || $2==1208651 {print}' | head -20; echo '==='; ps -eo pid,ppid,etime,pcpu,cmd | grep \"toutes-les-portes\" | grep -v grep", "description": "Inspect our gate process tree"}`

  ```
1208666 1208651       21:33  0.0 bash tools/toutes-les-portes.sh
1449907 1208666       00:59  0.0 timeout 1800 bash tools/porte-episodique.sh
===
 820703    2886    01:58:39  0.0 bash tools/toutes-les-portes.sh
1208651 1169498       21:33  0.0 bash -c bash tools/toutes-les-portes.sh > /tmp/portes.out 2>&1; echo EXIT:$?; tail -30 /tmp/portes.out
1208666 1208651       21:33  0.0 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "sleep 120; wc -l work/portes-1107-16h48/registre.txt; tail -8 work/portes-1107-16h48/registre.txt; echo '==='; tail -5 /tmp/portes.out", "description": "Wait and check gates", "timeoutMs": 150000}`

  ```
21 work/portes-1107-16h48/registre.txt
porte-consolidation 0 81
porte-coupe 0 162
porte-cycle-c2 0 142
porte-deepseek 0 1
porte-delais 0 25
porte-diff-couche 0 22
porte-document 0 6
porte-echange-experts 0 63
===
  porte-deepseek         ✅                           1 s    ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
  porte-delais           ✅                          25 s    ✅ le temps, lui, augmente : 9.64 s → 11.94 s (+2.3 s ≈ 50 ms × 64 pas)
  porte-diff-couche      ✅                          22 s    ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé
  porte-document         ✅                           6 s  ✅ porte document verte
  porte-echange-experts  ✅                          63 s    PORTE TENUE
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1208666 || $1==1208666 {print}' | head; echo '==='; ls -lt work/portes-1107-16h48 | head -5", "description": "Check current gate child"}`

  ```
1208666 1208651       23:40  0.0 bash tools/toutes-les-portes.sh
1449907 1208666       03:06  0.0 timeout 1800 bash tools/porte-episodique.sh
===
total 96
-rw-r--r--. 1 stephane stephane 5238  7 nov 17:11 porte-episodique.log
-rw-r--r--. 1 stephane stephane  461  7 nov 17:08 registre.txt
-rw-r--r--. 1 stephane stephane  343  7 nov 17:08 porte-echange-experts.log
-rw-r--r--. 1 stephane stephane 1175  7 nov 17:07 porte-document.log
  ```

- **bash** `{"command": "tail -20 work/portes-1107-16h48/porte-episodique.log", "description": "Read episodic gate log"}`

  ```
round-trip        : 219/300 épisodes relus AU BIT PRÈS avec leur propre clé
    échecs expliqués  : 81 par COLLISION de clés (deux états indiscernables), 0 par ÉGALITÉ de recouvrement (clés distinctes, même nombre de canaux partagés — départagées par l'identifiant le plus petit)
  ✅ 81 échecs, tous expliqués : 81 collisions, 0 égalités de recouvrement
=== 6. expansion + égalisation : l'index doit ÉLUDER pour de vrai ===
  [modele] 24 couches chargées en 7.705347076s — listes 0.71 Go , 8 threads
    expansion         : 896 → 16384 canaux de clé (8 entrées par canal, signes par hachage) ; les VALEURS restent les états exacts de dimension 896
    égalisation       : chaque canal de clé centré et réduit sur le magasin — un canal systématiquement grand n'entre plus dans toutes les clés
    coût de l'expansion : 131072 additions par lecture (fixe) · le balayage évité coûte N × 64 comparaisons · l'expansion est donc rentable au-delà de N ≈ 2048 épisodes — EN DESSOUS, le balayage complet est MOINS cher
    clé               : 64 canaux sur 16384 (densité 0.39 %), valeurs de dimension 896
    round-trip        : 300/300 épisodes relus AU BIT PRÈS avec leur propre clé
    séparation        :
… [873 caractères tronqués]
  ```

- **bash** `{"command": "sleep 90; wc -l work/portes-1107-16h48/registre.txt; tail -5 work/portes-1107-16h48/registre.txt; echo '==='; tail -5 /tmp/portes.out", "description": "Wait for episodic gate", "timeoutMs": 120000}`

  ```
25 work/portes-1107-16h48/registre.txt
porte-echange-experts 0 63
porte-episodique 0 212
porte-etat 0 0
porte-flux 0 33
porte-fusion 0 10
===
  porte-echange-experts  ✅                          63 s    PORTE TENUE
  porte-episodique       ✅                         212 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          33 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/retrieval_epoque.py')\ns=p.read_text()\nold='''    sortie = pathlib.Path(a.sortie)\n    sortie.parent.mkdir(parents=True, exist_ok=True)\n    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1), encoding=\"utf-8\") … [719 caractères tronqués]`

  ```
ok
EXIT:0
  ```

- **bash** `{"command": "rm -f work/retrieval-epoque-rapide.json; python3 tools/retrieval_epoque.py --rapide --n-versets 200 >/tmp/rapide.log 2>&1; echo EXIT:$?; tail -3 /tmp/rapide.log; ls -l work/retrieval-epoque-rapide.json | cut -c1-60", "description": "Test rapid guard", "timeoutMs": 300000}`

  ```
EXIT:0
BIBLE — 12 traductions datées…
  300 versets, 132 paires
→ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/retrieval-epoque-rapide.json
-rw-r--r--. 1 stephane stephane 2138260  7 nov 17:14 work/re
  ```

- **bash** `{"command": "rm -f work/retrieval-epoque-rapide.json; git status --short | head -5", "description": "Remove rapid artifact"}`

  ```
M  docs/pilotage/en-cours.md
 M docs/pilotage/references-non-regression.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-07/README.md
 M journal/README.md
  ```

- **bash** `{"command": "wc -l work/portes-1107-16h48/registre.txt; tail -5 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 /tmp/portes.out", "description": "Check gate progress"}`

  ```
25 work/portes-1107-16h48/registre.txt
porte-echange-experts 0 63
porte-episodique 0 212
porte-etat 0 0
porte-flux 0 33
porte-fusion 0 10
===
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          33 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1208666 || $1==1208666 {print}'; echo '==='; ls -lt work/portes-1107-16h48 | head -4", "description": "Check current gate"}`

  ```
1208666 1208651       26:01  0.0 bash tools/toutes-les-portes.sh
1493585 1208666       01:14  0.0 timeout 1800 bash tools/porte-gain.sh
===
total 112
-rw-r--r--. 1 stephane stephane  589  7 nov 17:14 porte-gain.log
-rw-r--r--. 1 stephane stephane  533  7 nov 17:13 registre.txt
-rw-r--r--. 1 stephane stephane 1844  7 nov 17:13 porte-fusion.log
  ```

- **bash** `{"command": "grep -n \"home/stephane\\|/tmp\\|RACINE\" tools/corpus_commun.py | head -10; echo '==='; grep -n \"home/stephane\" reports/corpus-commun.json | head -3", "description": "Check J2.2 portability"}`

  ```
34:RACINE = Path(__file__).resolve().parents[1]
35:PANINI_RESEARCH = RACINE.parent / "Panini" / "research"
37:DRAVE_UDHR = RACINE / "data" / "udhr"
41:OUTIL = RACINE / "tools" / "corpus_commun.py"
42:SORTIE = RACINE / "work" / "corpus-commun"
43:RAPPORT_JSON = RACINE / "reports" / "corpus-commun.json"
154:        "depot": str(depot.relative_to(RACINE.parent))
155:        if depot.is_relative_to(RACINE.parent)
754:                **git_info(RACINE),
1073:        chemin = (RACINE / relatif).resolve()
===
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -20; echo EXIT:${PIPESTATUS[0]}", "description": "Check table gate"}`

  ```
❌ 1 tableau(x) ne rendront pas (mistune refuse le tableau ENTIER) :
     reports/rapport-retrieval-epoque.md:203 — 5 cellules ≠ 3 attendues
  1768 fichier(s) examiné(s)
EXIT:1
  ```

- **bash** `{"command": "sed -n '198,210p' reports/rapport-retrieval-epoque.md", "description": "Inspect broken table"}`

  ```
**La régression des 132 paires.** `top1 ~ |Δ années|/siècle + script_match + famille_match + langue_match` :

| variable | coefficient | IC 95 % |
|---|---:|---:|
| **|Δ années| par siècle** | **−0,034** | **[−0,075 ; +0,009]** |
| écriture même | **+0,609** | [0,529 ; 0,702] |
| famille même | **+0,181** | [0,106 ; 0,253] |
| langue même | **+0,311** | [0,209 ; 0,402] |
| constante | −0,037 | [−0,091 ; +0,013] |

**R² = 0,763.** Le coefficient de dates n'est **pas significatif** ; le contrôle par **permutation des
années** donne **p = 0,19** (500 permutations). Le coefficient d'écriture (0,609) vaut **18 fois** celui des dates par siècle (0,034) ; la famille
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-epoque.md')\ns=p.read_text().replace('| **|Δ années| par siècle** | **−0,034** | **[−0,075 ; +0,009]** |',\n                        '| **Δ années par siècle** | **−0,034** | **[−0,075 ; +0,009]** |')\np.write_te … [135 caractères tronqués]`

  ```
ok
  ✅ 1768 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3830 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
EXIT:0
  ```

- **bash** `{"command": "git add reports/rapport-retrieval-epoque.md; git diff --cached --check; echo EXIT:$?", "description": "Restage report"}`

  ```
EXIT:0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -3; python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation\"", "description": "Final checks"}`

  ```
revue de documentation · 712 fiche(s) · 805 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  T0 max : 4000 mots (budget 4 000)
  ```

- **bash** `{"command": "wc -l work/portes-1107-16h48/registre.txt; tail -5 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 /tmp/portes.out", "description": "Check gates"}`

  ```
25 work/portes-1107-16h48/registre.txt
porte-echange-experts 0 63
porte-episodique 0 212
porte-etat 0 0
porte-flux 0 33
porte-fusion 0 10
===
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          33 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  ```

- **bash** `{"command": "tail -10 work/portes-1107-16h48/porte-gain.log; echo '==='; ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1208666 || $1==1208666 {print}'", "description": "Check gain gate"}`

  ```
gain -0.5   : 17.1200
  gain -1.0   : 19.4791
  ✅ toute inhibition dégrade, et de plus en plus : l'optimum intérieur est réfuté de ce côté
=== 3. optimum INTÉRIEUR (couche 0) : 0,75 doit battre 0,5 ET 1,5 ===
  gain 0,5 : 14.1057 · 0,75 : 12.9635 · 1,5 : 15.4298
  ✅ PPL gain 0.5 épinglée : 14.1057
  ✅ PPL gain 0.75 épinglée : 12.9635
  ✅ PPL gain 1.5 épinglée : 15.4298
  ✅ optimum intérieur : 12.9635 contre 14.1057, 15.4298 et 14.6496 sans réglage (11.5 % de mieux)
=== 4. la FALAISE : 0,25 à la couche 0 casse le modèle ===
===
1208666 1208651       26:25  0.0 bash tools/toutes-les-portes.sh
1493585 1208666       01:37  0.0 timeout 1800 bash tools/porte-gain.sh
  ```

- **bash** `{"command": "sleep 90; wc -l work/portes-1107-16h48/registre.txt; tail -3 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 /tmp/portes.out", "description": "Wait for gain gate", "timeoutMs": 120000}`

  ```
25 work/portes-1107-16h48/registre.txt
porte-etat 0 0
porte-flux 0 33
porte-fusion 0 10
===
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          33 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  ```

- **bash** `{"command": "tail -8 work/portes-1107-16h48/porte-gain.log; ps -eo pid,etime,pcpu,cmd | grep -E \"porte-gain|drave-core\" | grep -v grep | head -5", "description": "Check gain gate progress"}`

  ```
✅ le bénéfice est à l'ENTRÉE : couches 0 et 1 à 12.9635 et 13.9844 (mieux que 14.6496), couche 5 à 14.7526 (pas mieux)
=== 6. un PROFIL ne compose PAS : il défait le meilleur réglage seul ===
  0:0.75 seul : 12.9635 · +1:0.5 : 13.7679 · +1:0.5+2:1.0 : 13.7679
  ✅ la composition DÉGRADE (12.9635 → 13.7679), et un gain 1,0 y est exactement neutre (13.7679 = 13.7679)
=== 7. l'effet DIMINUE avec la fenêtre d'évaluation (et il tient) ===
  128 jetons : 12.9635 (réf 14.6496) · 256 jetons : 17.1915 (réf 17.4315)
  ✅ la direction tient aux deux fenêtres, la MAGNITUDE décroît : 11.5 % à 128 jetons, 1.4 % à 256 — une condition, pas une propriété
=== 8. le drapeau AGIT AUSSI dans le chemin RÉPARTI ===
1493585       03:15  0.0 timeout 1800 bash tools/porte-gain.sh
1493586       03:15  0.0 bash tools/porte-gain.sh
1504733       02:23  0.0 timeout 2400 env DRAVE_VISION_POIDS=all DRAVE_VISION_COUCHES=32 DRAVE_VISION_FUSION=1 ./drave-core/target/release/drave models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf --banc-vision /tmp/porte-vision/tour.bin
1504734       02:23  100 ./drave-core/target/release/drave models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf --banc-vision /tmp/porte-vision/tour.b
… [134 caractères tronqués]
  ```

- **bash** `{"command": "sleep 120; wc -l work/portes-1107-16h48/registre.txt; tail -3 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 /tmp/portes.out", "description": "Wait for gain gate completion", "timeoutMs": 150000}`

  ```
26 work/portes-1107-16h48/registre.txt
porte-flux 0 33
porte-fusion 0 10
porte-gain 0 251
===
  porte-flux             ✅                          33 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         251 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1208666 || $1==1208666 {print}' | head", "description": "Check next gate"}`

  ```
1208666 1208651       30:07  0.0 bash tools/toutes-les-portes.sh
1532194 1208666       01:08  0.0 timeout 1800 bash tools/porte-greffe.sh
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-epoque.md')\ns=p.read_text()\nold=\"\"\"**R² = 0,400.** L'écriture pèse **près de trois fois** la famille. Les meilleures paires sont des langues\"\"\"\nnew=\"\"\"**R² = 0,400.** L'écriture pèse **près de trois  … [428 caractères tronqués]`

  ```
ok
  ✅ 1768 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3830 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
  ```

- **bash** `{"command": "sleep 150; wc -l work/portes-1107-16h48/registre.txt; tail -4 work/portes-1107-16h48/registre.txt; echo '==='; tail -4 /tmp/portes.out", "description": "Wait and check gates", "timeoutMs": 180000}`

  ```
26 work/portes-1107-16h48/registre.txt
porte-etat 0 0
porte-flux 0 33
porte-fusion 0 10
porte-gain 0 251
===
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          33 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         251 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  ```

- **bash** `{"command": "tail -8 work/portes-1107-16h48/porte-greffe.log; echo '==='; ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1208666 || $1==1208666 {print}'", "description": "Check greffe gate"}`

  ```
=== 0. construire A (avec aiguille) et B (sans), et vérifier qu'elles diffèrent ===
  A (avec aiguille) : [1863, 48, 12, 19, 19, 22, 16, 15843]
  B (sans aiguille) : [220, 16, 17, 18, 19, 20, 21, 22]
=== 1. prélever l'état de la dernière position DE L'INFÉRENCE (--etat-fin) ===
    capture d'état    : position(s) [1470] (depuis la fin d'une invite de 1471 jetons) écrite(s) dans /tmp/tmp.yRKDOTegi7/etatA
=== 2. témoin de non-effet : poids 0 ⇒ aucune différence ===
===
1208666 1208651       32:48  0.0 bash tools/toutes-les-portes.sh
1532194 1208666       03:49  0.0 timeout 1800 bash tools/porte-greffe.sh
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-retrieval-epoque.md", "description": "Read report first half"}`

  ```
# J3.1 — Le retrieval inter-langues à époque contrôlée

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J3.1 · **Date** : 2026-11-07
> **Verdict** : ✅ **la mesure est faite ; elle borne l'avertissement** —
> dans ce retrieval de **surface**, **l'écriture domine** (+0,609 ; IC 95 % [0,529 ; 0,702]), la **famille**
> compte ensuite (+0,181 [0,106 ; 0,253]), et **l'écart d'années ne pèse pas** (−0,034 par siècle
> [−0,075 ; +0,009], p = 0,19 par permutation). À écriture contrôlée, les couples **contemporains** et
> **décalés** sont au **même niveau** : **0,710 vs 0,710**. Le renversement brut (0,238 vs 0,427) est un
> **effet de composition** : les couples décalés contiennent **60 %** de paires de même écriture, les
> contemporains **33 %**. **L'époque ne domine pas ici ; le confondant de composition, lui, n'est pas nul : sans
> contrôle, il fausse la comparaison.**
> **Dispositif** : trois corpus, un même retrieval de surface (n-grammes de caractères, TF-IDF, cosinus,
> top-1) ; **B7** (71 langues, 35 concepts, libellés Wikidata 2026), **UDHR** (21 langues du corpus commun,
> 30 articles, 1948), **BIBLE** (12 traductions datées de 1744 à 2019, 1 000 ve
… [7441 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,300p' reports/rapport-retrieval-epoque.md", "description": "Read report second half"}`

  ```
|---|---:|---:|
| **écriture même** | **0,266** (742 paires) | **0,176** (944 paires) |
| **écriture différente** | **0,086** (840 paires) | **0,079** (1 478 paires) |

La régression `top1 ~ script_match + famille_match + chance` donne :

| variable | coefficient | IC 95 % |
|---|---:|---:|
| écriture même | **+0,132** | [0,126 ; 0,137] |
| famille même | **+0,046** | [0,040 ; 0,051] |
| chance (1/k) | +0,355 | [0,280 ; 0,424] |
| constante | +0,045 | [0,040 ; 0,050] |

**R² = 0,400.** L'écriture pèse **près de trois fois** la famille. Les coefficients ne se comparent pas
d'un bras à l'autre (le hasard B7 est 1/k, celui de la Bible 1/1 000) ; seule la **hiérarchie** se compare.
Les meilleures paires sont des langues
sœurs de même écriture : `nb–nn` 0,875, `bs–hr` 0,857, `cs–sk` 0,826, `mk–sr` 0,800. Les paires de même
écriture mais de familles différentes restent au-dessus du hasard (`fr–tr` 0,259, `en–id` 0,105…), mais loin des sœurs.
**Contrôle négatif** : cibles permutées **0,070** contre un hasard de **0,055** — proche du hasard ; le
léger excès est attendu, des libellés de concepts différents peuvent se ressembler (roi/dame, blanc/noir).
**Contrôle de langue** : apparier A à u
… [9884 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-epoque.md')\ns=p.read_text()\nold=\"\"\"coefficient observé doit sortir de la distribution permutée. Les IC sont des **bootstrap** sur les requêtes\n(1 000 rééchantillonnages) ou sur les paires (1 000) selon le  … [893 caractères tronqués]`

  ```
ok
  ✅ 1768 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3830 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
  ```

- **bash** `{"command": "wc -l work/portes-1107-16h48/registre.txt; tail -4 work/portes-1107-16h48/registre.txt; echo '==='; tail -4 /tmp/portes.out", "description": "Check gates"}`

  ```
26 work/portes-1107-16h48/registre.txt
porte-etat 0 0
porte-flux 0 33
porte-fusion 0 10
porte-gain 0 251
===
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          33 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         251 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  ```

- **bash** `{"command": "tail -6 work/portes-1107-16h48/porte-greffe.log; echo '==='; ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1208666 || $1==1208666 {print}'", "description": "Check greffe gate"}`

  ```
=== 0. construire A (avec aiguille) et B (sans), et vérifier qu'elles diffèrent ===
  A (avec aiguille) : [1863, 48, 12, 19, 19, 22, 16, 15843]
  B (sans aiguille) : [220, 16, 17, 18, 19, 20, 21, 22]
=== 1. prélever l'état de la dernière position DE L'INFÉRENCE (--etat-fin) ===
    capture d'état    : position(s) [1470] (depuis la fin d'une invite de 1471 jetons) écrite(s) dans /tmp/tmp.yRKDOTegi7/etatA
=== 2. témoin de non-effet : poids 0 ⇒ aucune différence ===
===
1208666 1208651       33:06  0.0 bash tools/toutes-les-portes.sh
1532194 1208666       04:07  0.0 timeout 1800 bash tools/porte-greffe.sh
  ```

- **bash** `{"command": "ls -d work/portes-* 2>/dev/null; echo '==='; ps -eo pid,ppid,etime,cmd | grep \"superviseur\\|toutes-les-portes\" | grep -v grep", "description": "Check other gate runs"}`

  ```
work/portes-1106-01h03
work/portes-1106-01h28
work/portes-1107-01h43
work/portes-1107-02h09
work/portes-1107-15h11
work/portes-1107-16h48
work/portes-j12-1107-12h58
work/portes-n3-cloture
===
 216359    2886    05:02:41 timeout 25200 python3 tools/chantier/superviseur.py boucle --budget 21600 --timeout 5400
 216362  216359    05:02:41 python3 tools/chantier/superviseur.py boucle --budget 21600 --timeout 5400
 820703    2886    02:10:16 bash tools/toutes-les-portes.sh
1208651 1169498       33:10 bash -c bash tools/toutes-les-portes.sh > /tmp/portes.out 2>&1; echo EXIT:$?; tail -30 /tmp/portes.out
1208666 1208651       33:10 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "wc -l work/portes-1107-15h11/registre.txt 2>/dev/null; tail -3 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check other gate progress"}`

  ```
83 work/portes-1107-15h11/registre.txt
porte-tokenizer-kimi 0 6
porte-topologie 0 123
porte-trace 0 32
  ```

- **bash** `{"command": "sleep 60; wc -l work/portes-1107-15h11/registre.txt; wc -l work/portes-1107-16h48/registre.txt; ps -eo pid,etime,cmd | grep \"toutes-les-portes\" | grep -v grep", "description": "Wait for other gate run", "timeoutMs": 90000}`

  ```
83 work/portes-1107-15h11/registre.txt
26 work/portes-1107-16h48/registre.txt
 820703    02:11:20 bash tools/toutes-les-portes.sh
1208651       34:14 bash -c bash tools/toutes-les-portes.sh > /tmp/portes.out 2>&1; echo EXIT:$?; tail -30 /tmp/portes.out
1208666       34:14 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1532194 || $2==1532195 || $1==1532194 || $1==1532195 {print}'; echo '==='; ps -eo pid,etime,pcpu,cmd | grep \"drave-core\" | grep -v grep | head -3", "description": "Check greffe child"}`

  ```
1532194 1208666       05:18  0.0 timeout 1800 bash tools/porte-greffe.sh
1532195 1532194       05:18  0.0 bash tools/porte-greffe.sh
1535204 1532195       00:46  0.0 bash tools/porte-greffe.sh
===
1504733       08:38  0.0 timeout 2400 env DRAVE_VISION_POIDS=all DRAVE_VISION_COUCHES=32 DRAVE_VISION_FUSION=1 ./drave-core/target/release/drave models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf --banc-vision /tmp/porte-vision/tour.bin
1504734       08:38 99.9 ./drave-core/target/release/drave models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf --banc-vision /tmp/porte-vision/tour.bin
1535205       00:46  879 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --prompt  Division . On August 1 , the 23rd Regiment was in a new sector of which it had only a limited knowledge . It took over a 16 @,@ 000 yards ( 15 @,@ 000 m ) Naktong River front without its 3rd Battalion which had been attached to the US 1st Cavalry Division to the north . Colonel Paul L. Freeman , the regimental commander , deployed the 1st Battalion on the high ground along the river with the three companies abreast . The 1st Battalion , under US Lieutenant Colonel Claire E. Hutchin , Jr . , outposted 
… [5784 caractères tronqués]
  ```

- **bash** `{"command": "sleep 120; wc -l work/portes-1107-15h11/registre.txt work/portes-1107-16h48/registre.txt; ps -eo pid,etime,cmd | grep \"toutes-les-portes\" | grep -v grep", "description": "Wait for gates", "timeoutMs": 150000}`

  ```
83 work/portes-1107-15h11/registre.txt
  26 work/portes-1107-16h48/registre.txt
 109 total
 820703    02:13:27 bash tools/toutes-les-portes.sh
1208651       36:21 bash -c bash tools/toutes-les-portes.sh > /tmp/portes.out 2>&1; echo EXIT:$?; tail -30 /tmp/portes.out
1208666       36:20 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "python3 tools/retrieval_epoque.py --n-versets 1000 --sortie /tmp/retrieval-2.json >/tmp/retrieval-2.log 2>&1; echo EXIT:$?; python3 - <<'EOF'\nimport json\na=json.load(open('reports/retrieval-epoque.json')); b=json.load(open('/tmp/retrieval-2.json'))\nfor arm in ['b7','udhr','bible']:\n … [308 caractères tronqués]`

  ```
EXIT:0
b7 0.13811021897113393 0.13811021897113393
udhr 0.049444444444444444 0.049444444444444444
bible 0.29343181818181824 0.29343181818181824
bible reg -0.033809822582852256 -0.033809822582852256
  ```

- **bash** `{"command": "rm -f /tmp/retrieval-2.json; wc -l work/portes-1107-15h11/registre.txt work/portes-1107-16h48/registre.txt; tail -3 /tmp/portes.out", "description": "Check gates"}`

  ```
85 work/portes-1107-15h11/registre.txt
  26 work/portes-1107-16h48/registre.txt
 111 total
  porte-flux             ✅                          33 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         251 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  ```

- **bash** `{"command": "ps -eo pid,etime,cmd | grep \"toutes-les-portes\" | grep -v grep; echo '==='; tail -5 work/portes-1107-15h11/registre.txt; echo '==='; tail -5 work/portes-1107-16h48/porte-greffe.log", "description": "Check other run completion"}`

  ```
1208651       37:09 bash -c bash tools/toutes-les-portes.sh > /tmp/portes.out 2>&1; echo EXIT:$?; tail -30 /tmp/portes.out
1208666       37:09 bash tools/toutes-les-portes.sh
===
porte-tokenizer-kimi 0 6
porte-topologie 0 123
porte-trace 0 32
porte-vision 0 646
--- 79 vertes, 5 rouges ---
===
  A + son état (poids 100) : [1863, 48, 12, 19, 19, 22, 16, 15843]
  ✅ l'état injecté porte bien la direction du contenu de A
=== 4. CORRIGÉ : l'état de A dans C (sans aucun code) DONNE le code ===
  poids 1    : [220, 16, 17, 18, 19, 20, 21, 22]
  poids 2    : [1863, 48, 41, 43, 198, 16141, 374, 25]
  ```

- **bash** `{"command": "awk '$2 != 0' work/portes-1107-15h11/registre.txt", "description": "List other run reds"}`

  ```
porte-indice 1 1060
porte-melange 1 127
porte-occupation-moteur 1 62
porte-sessions 1 0
porte-tableaux 1 1
--- 79 vertes, 5 rouges ---
  ```

- **bash** `{"command": "grep -n \"indice\\|melange\\|occupation\\|sessions\\|tableaux\" docs/pilotage/references-non-regression.md | head -20", "description": "Check tolerated reds"}`

  ```
7:> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
8:> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
10:> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
16:> (`indice` 821 s, `melange` 102 s), 1 h 48, GPU libres.
19:> `porte-sessions` (coordination, rejouée verte à 08 h 10 après la pause de N2/S).
28:> (journaux `/tmp/portes-1101-n2h`). Mêmes rouges que la passe du 31/10 : `porte-indice` (921 s),
29:> `porte-melange` (112 s), `porte-homeostasie` (environnementale) et `porte-reparti-moteur`.
53:> documentés) : le récit et les tableaux sont dans
63:| `porte-audit-drapeaux.sh` | 167 s | ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun |
69:| `porte-bloc-tableaux.sh` | 1 s | ✅ porte bloc tableaux verte |
92:| `porte-indice.sh` | 821 s | ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, question qui  |
98:| `porte-melange.sh` | 102 s | ❌ l'état de A ne rend pas le code de A dans une |
120:| `porte-occupation-elagage.sh` | 60 s | ✅ porte occupation × élagage :
… [526 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,35p' docs/pilotage/references-non-regression.md", "description": "Read tolerated reds list"}`

  ```
# Références de non-régression

> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
> échouait sur une ancre du banc pilote (« < 2,5 ») que la réécriture de la roadmap du 04/11
> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
> signale les heartbeats périmés du hub et de `e181ce02` au moment de la passe — le hub l'a rafraîchi
> à 01 h 55, **`e181ce02` reste à rafraîchir par sa session**. Longues vertes : `greffe` **840 s**,
> `homeostasie` **755 s**, `profondeur-routee` **700 s**, `vision` **670 s**, `ocr-scans` **529 s**.

> **Passe précédente — 2026-11-03 11 h 30 :** 82 portes, 80 vertes, 2 rouges structurelles
> (`indice` 821 s, `melange` 102 s), 1 h 48, GPU libres.
>
> **Passe précédente — 2026-11-03
… [1017 caractères tronqués]
  ```

- **bash** `{"command": "sleep 120; wc -l work/portes-1107-16h48/registre.txt; tail -3 work/portes-1107-16h48/registre.txt; echo '==='; tail -4 work/portes-1107-16h48/porte-greffe.log", "description": "Wait for greffe", "timeoutMs": 150000}`

  ```
26 work/portes-1107-16h48/registre.txt
porte-flux 0 33
porte-fusion 0 10
porte-gain 0 251
===
  poids 1    : [220, 16, 17, 18, 19, 20, 21, 22]
  poids 2    : [1863, 48, 41, 43, 198, 16141, 374, 25]
  poids 4    : [1863, 48, 41, 43, 198, 16141, 374, 25]
  poids 10   : [1863, 48, 41, 43, 198, 16141, 374, 25]
  ```

- **bash** `{"command": "sleep 90; wc -l work/portes-1107-16h48/registre.txt; tail -3 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 /tmp/portes.out", "description": "Wait for greffe completion", "timeoutMs": 120000}`

  ```
26 work/portes-1107-16h48/registre.txt
porte-flux 0 33
porte-fusion 0 10
porte-gain 0 251
===
  porte-flux             ✅                          33 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         251 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  ```

- **bash** `{"command": "tail -15 work/portes-1107-16h48/porte-greffe.log; echo '==='; ps -eo pid,ppid,etime,pcpu,cmd | awk '$1==1535205 || $2==1532195 {print}' | head", "description": "Check greffe status"}`

  ```
capture d'état    : position(s) [1470] (depuis la fin d'une invite de 1471 jetons) écrite(s) dans /tmp/tmp.yRKDOTegi7/etatA
=== 2. témoin de non-effet : poids 0 ⇒ aucune différence ===
  ✅ poids 0 : [220, 16, 17, 18, 19, 20, 21, 22] (identique à B sans greffe)
=== 3. le mécanisme fonctionne : A + son propre état reste sur le code ===
  A + son état (poids 100) : [1863, 48, 12, 19, 19, 22, 16, 15843]
  ✅ l'état injecté porte bien la direction du contenu de A
=== 4. CORRIGÉ : l'état de A dans C (sans aucun code) DONNE le code ===
  poids 1    : [220, 16, 17, 18, 19, 20, 21, 22]
  poids 2    : [1863, 48, 41, 43, 198, 16141, 374, 25]
  poids 4    : [1863, 48, 41, 43, 198, 16141, 374, 25]
  poids 10   : [1863, 48, 41, 43, 198, 16141, 374, 25]
  poids 100  : [1863, 48, 41, 43, 198, 16141, 374, 25]
  ✅ l'état de A, prélevé LÀ OÙ LE CALCUL SE FAIT, porte bien son contenu
     (l'ancienne conclusion négative était un décalage d'un jeton, pas une propriété
=== 5. la greffe porte TOUT le contenu, pas seulement le premier jeton ===
===
1539139 1532195       00:48  0.0 bash tools/porte-greffe.sh
  ```

- **bash** `{"command": "sleep 120; wc -l work/portes-1107-16h48/registre.txt; tail -3 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 /tmp/portes.out", "description": "Wait for greffe section 5", "timeoutMs": 150000}`

  ```
27 work/portes-1107-16h48/registre.txt
porte-fusion 0 10
porte-gain 0 251
porte-greffe 0 739
===
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         251 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  porte-greffe           ✅                         739 s    ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1208666 || $1==1208666 {print}'; echo '==='; tail -3 work/portes-1107-16h48/registre.txt", "description": "Check next gate"}`

  ```
1208666 1208651       43:06  0.0 bash tools/toutes-les-portes.sh
1539851 1208666       01:47  0.0 timeout 1800 bash tools/porte-harnais-invariants.sh
===
porte-fusion 0 10
porte-gain 0 251
porte-greffe 0 739
  ```

- **bash** `{"command": "sleep 120; wc -l work/portes-1107-16h48/registre.txt; tail -5 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 /tmp/portes.out", "description": "Wait for harnais gate", "timeoutMs": 150000}`

  ```
28 work/portes-1107-16h48/registre.txt
porte-flux 0 33
porte-fusion 0 10
porte-gain 0 251
porte-greffe 0 739
porte-harnais-invariants 0 120
===
  porte-gain             ✅                         251 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  porte-greffe           ✅                         739 s    ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE
  porte-harnais-invariants ✅                         120 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1208666 || $1==1208666 {print}'", "description": "Check next gate"}`

  ```
1208666 1208651       45:11  0.0 bash tools/toutes-les-portes.sh
1541406 1208666       01:53  0.0 timeout 1800 bash tools/porte-homeostasie.sh
  ```

- **bash** `{"command": "git status --short tools/retrieval_epoque.py tools/corpus_commun.py reports/rapport-retrieval-epoque.md reports/retrieval-epoque.json reports/rapport-corpus-commun.md reports/corpus-commun.json docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-07/README.md reports/INDEX … [49 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-07/README.md
M  reports/INDEX.md
A  reports/corpus-commun.json
A  reports/rapport-corpus-commun.md
A  reports/rapport-retrieval-epoque.md
A  reports/retrieval-epoque.json
A  tools/corpus_commun.py
A  tools/retrieval_epoque.py
  ```

- **bash** `{"command": "ls .git/hooks | grep -v sample; echo '==='; sed -n '1,80p' .git/hooks/pre-commit 2>/dev/null", "description": "Inspect git hooks"}`

  ```
pre-commit
===
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
# Le journal du jour, par thème (sources : git + journal/sessions). L'i
… [249 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/verifie_etat_a_jour.py", "description": "Read state hook"}`

  ```
#!/usr/bin/env python3
"""verifie_etat_a_jour.py — aucun fait commité sans sa ligne d'état.

POURQUOI CET OUTIL EXISTE. `en-cours` est la seule source de l'état, et le contrat
disait « seul le principal écrit ». Ce n'est pas une garantie : l'identité se déduit
d'une variable d'environnement absente — un « pair » est autodéclaré — et si la
principale s'arrête, l'état se fige. Surtout, rien ne comparait les commits : la
revue ne regardait que la DATE, donc deux commits du même jour passaient. Le 29/10,
A8.0 (15 h 51) a été commité après le dernier état (15 h 34) sans aucune alerte.

La garantie est au commit, pas dans la discipline d'un écrivain :
  --index  (hook pre-commit) : un commit qui prépare un fait (reports/, roadmap,
           backlog) sans toucher `en-cours` est REFUSÉ ;
  --head   : si un fait a été commité après le dernier commit d'`en-cours`, l'état
           est en retard — la session qui le voit le corrige, sans attendre.

Le journal est du récit dérivé (le hook l'archive) : il n'exige pas de ligne d'état.

Usage :
  python3 tools/verifie_etat_a_jour.py             # --head
  python3 tools/verifie_etat_a_jour.py --index     # pour le hook
  python3 tools/verifie_eta
… [3540 caractères tronqués]
  ```

- **bash** `{"command": "tail -3 work/portes-1107-16h48/porte-homeostasie.log 2>/dev/null; ps -eo pid,etime,pcpu,cmd | grep -E \"homeostasie\" | grep -v grep | head -3", "description": "Check homeostasie gate"}`

  ```
variantes écrites : ×0, ×0,6, ×1,0 (depuis /tmp/n4/rang4-lora.pt)
porte de l'homéostasie (E9) — LoRA rang 4, amplitudes ×0 / ×0,6 / ×1,0
1541406       02:05  0.0 timeout 1800 bash tools/porte-homeostasie.sh
1541407       02:05  0.0 bash tools/porte-homeostasie.sh
1550292       00:37  0.0 bash tools/porte-homeostasie.sh
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-epoque.md')\ns=p.read_text()\ns=s.replace(\"et **l'écart d'années ne pèse pas** (−0,034 par siècle\", \"et **l'écart d'années ne pèse pas en moyenne** (−0,034 par siècle\")\ns=s.replace(\"l'écart d'années n'a ** … [801 caractères tronqués]`

  ```
ok
  ✅ 1768 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3830 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
  ```

- **bash** `{"command": "sleep 180; wc -l work/portes-1107-16h48/registre.txt; tail -3 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 /tmp/portes.out", "description": "Wait for homeostasie", "timeoutMs": 210000}`

  ```
28 work/portes-1107-16h48/registre.txt
porte-gain 0 251
porte-greffe 0 739
porte-harnais-invariants 0 120
===
  porte-gain             ✅                         251 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  porte-greffe           ✅                         739 s    ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE
  porte-harnais-invariants ✅                         120 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
  ```

- **bash** `{"command": "cat > /tmp/commit-msg.txt <<'MSG'\nJ3.1 — RETRIEVAL À ÉPOQUE CONTRÔLÉE : L'ÉCRITURE DOMINE (+0,609) ; L'ÉPOQUE NE PÈSE PAS À ÉCRITURE CONTRÔLÉE (−0,034/SIÈCLE, p=0,19) ; LE BRUT EST UN EFFET DE COMPOSITION (0,238 vs 0,427)\n\nDispositif : B7 (71 langues, 35 concepts, libellés Wikidata 2 … [1165 caractères tronqués]`

  ```
9 /tmp/commit-msg.txt
  ```

- **bash** `{"command": "sleep 180; wc -l work/portes-1107-16h48/registre.txt; tail -4 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 /tmp/portes.out", "description": "Wait for homeostasie completion", "timeoutMs": 210000}`

  ```
28 work/portes-1107-16h48/registre.txt
porte-fusion 0 10
porte-gain 0 251
porte-greffe 0 739
porte-harnais-invariants 0 120
===
  porte-gain             ✅                         251 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  porte-greffe           ✅                         739 s    ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE
  porte-harnais-invariants ✅                         120 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
  ```

- **bash** `{"command": "tail -8 work/portes-1107-16h48/porte-homeostasie.log; ps -eo pid,etime,pcpu,cmd | grep \"homeostasie\" | grep -v grep | head -3", "description": "Check homeostasie progress"}`

  ```
variantes écrites : ×0, ×0,6, ×1,0 (depuis /tmp/n4/rang4-lora.pt)
porte de l'homéostasie (E9) — LoRA rang 4, amplitudes ×0 / ×0,6 / ×1,0
  (×0 : GGUF réécrit — l'export re-quantifie, la comparaison porte sur la mesure)
  ✅ 1. ×0 rend le modèle de départ (norme 72.1293 contre 72.1312, écart 2.6e-05 = la re-quantification de l'export)
  ✅ 2. l'activité croît avec l'amplitude : 72.1312 ≤ 73.1445 ≤ 73.1923
1541406       08:23  0.0 timeout 1800 bash tools/porte-homeostasie.sh
1541407       08:23  0.0 bash tools/porte-homeostasie.sh
1610296       00:35  0.0 bash tools/porte-homeostasie.sh
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-epoque.md')\ns=p.read_text()\nold=\"\"\"8. **Familles B7 grossières.** La table `FAMILLE_B7` est au niveau **macro** (Glottolog), pas à la feuille ;\n   deux langues « même famille » peuvent être très éloignées  … [913 caractères tronqués]`

  ```
ok
  ✅ 1768 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3830 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
  ```

- **bash** `{"command": "sleep 180; wc -l work/portes-1107-16h48/registre.txt; tail -4 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 /tmp/portes.out", "description": "Wait for homeostasie", "timeoutMs": 210000}`

  ```
30 work/portes-1107-16h48/registre.txt
porte-greffe 0 739
porte-harnais-invariants 0 120
porte-homeostasie 0 575
porte-horloge 0 29
===
  porte-harnais-invariants ✅                         120 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
  porte-homeostasie      ✅                         575 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,cmd | awk '$2==1208666 || $1==1208666 {print}'", "description": "Check next gate"}`

  ```
1208666 1208651       54:53  0.0 bash tools/toutes-les-portes.sh
1630445 1208666       01:31  0.0 timeout 1800 bash tools/porte-indice.sh
  ```

- **bash** `{"command": "sleep 240; wc -l work/portes-1107-16h48/registre.txt; tail -3 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 work/portes-1107-16h48/porte-indice.log", "description": "Wait for indice gate", "timeoutMs": 270000}`

  ```
30 work/portes-1107-16h48/registre.txt
porte-harnais-invariants 0 120
porte-homeostasie 0 575
porte-horloge 0 29
===
    capture d'état    : position(s) [1439] écrite(s) dans /tmp/tmp.yZCHGCivcF/etatB.*
    capture d'état    : position(s) [1469] écrite(s) dans /tmp/tmp.yZCHGCivcF/etatA.*
=== 3. la mémoire interroge A, avec puis sans l'indice extérieur ===
  ```

- **bash** `{"command": "sleep 300; wc -l work/portes-1107-16h48/registre.txt; tail -3 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 work/portes-1107-16h48/porte-indice.log", "description": "Wait for indice gate", "timeoutMs": 330000}`

  ```
30 work/portes-1107-16h48/registre.txt
porte-harnais-invariants 0 120
porte-homeostasie 0 575
porte-horloge 0 29
===
    capture d'état    : position(s) [1439] écrite(s) dans /tmp/tmp.yZCHGCivcF/etatB.*
    capture d'état    : position(s) [1469] écrite(s) dans /tmp/tmp.yZCHGCivcF/etatA.*
=== 3. la mémoire interroge A, avec puis sans l'indice extérieur ===
  ```

- **bash** `{"command": "sleep 300; wc -l work/portes-1107-16h48/registre.txt; tail -3 work/portes-1107-16h48/registre.txt; echo '==='; tail -3 work/portes-1107-16h48/porte-indice.log", "description": "Wait for indice gate", "timeoutMs": 330000}`

  ```
30 work/portes-1107-16h48/registre.txt
porte-harnais-invariants 0 120
porte-homeostasie 0 575
porte-horloge 0 29
===
    capture d'état    : position(s) [1469] écrite(s) dans /tmp/tmp.yZCHGCivcF/etatA.*
=== 3. la mémoire interroge A, avec puis sans l'indice extérieur ===
  témoin   capture d'état    : position(s) [1440] écrite(s) dans /tmp/tmp.yZCHGCivcF/etatC.*
  ```

- **bash** `{"command": "sleep 300; wc -l work/portes-1107-16h48/registre.txt; tail -3 work/portes-1107-16h48/registre.txt; echo '==='; tail -4 work/portes-1107-16h48/porte-indice.log", "description": "Wait for indice gate", "timeoutMs": 330000}`
