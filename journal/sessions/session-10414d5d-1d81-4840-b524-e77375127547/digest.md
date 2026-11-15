# Session DSH — relecture

- identifiant : `session-10414d5d-1d81-4840-b524-e77375127547`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 03:06:40
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche B2 : les 14 atomes comme prédicteurs des 8 niveaux Drave — sur les 44 œuvres × 14 flottants (JSON plat, lecture seule chez Panini), mesure la prédiction d'un niveau (POS, syntagmes, attachement) par les atomes, avec le contrôle de permutation des colonnes et le contrôle de date ; fiche `reports/rapport-atomes-prediction.md` + JSON.

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

- **bash** `{"command": "pwd && ls && git log --oneline -5", "description": "List repo root and recent commits"}`

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
c37fed06 B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE
f926b5bc C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PROFONDEUR, 41 VERDICTS À RE-JUGER ; PORT 8765 PRIS, PARE-FEU ACTIF ; LES 11 VERDICTS COMMITTÉS (389b99f)
292c70b5 C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09
5891ef8a ÉTAT — T0 TENU : LA LIGNE FAIT RACCOURCIE
6560a0a5 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612)
  ```

- **bash** `{"command": "ls reports/ | head -50; echo ---; ls journal/ | tail -20", "description": "List reports and journal directories"}`

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
alignement-verne.md
analyse-litteraire.json
archive
atomes-niveaux.json
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeur-mots.json
b10-mots-contraste.json
b10-mots-jw.json
---
2026-10-25
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
2026-11-
… [69 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/atomes-niveaux.json && python3 -c \"\nimport json\nd=json.load(open('reports/atomes-niveaux.json'))\nprint(type(d))\nprint(json.dumps(d,indent=1,ensure_ascii=False)[:3000])\n\"", "description": "Inspect existing atomes-niveaux.json"}`

  ```
-rw-r--r--. 1 stephane stephane 22066  7 nov 14:54 reports/atomes-niveaux.json
<class 'dict'>
{
 "fiche": "reports/rapport-atomes-niveaux.md",
 "version": "1.0",
 "date": "2026-11-07",
 "titre": "Table de correspondance — 14 atomes V14 de Panini et 8 niveaux Drave",
 "statut": "hypothese_de_lecture_et_protocole_non_mesure",
 "sources": {
  "atomes": {
   "depot": "../../Panini/research",
   "head": "e10d695",
   "head_date": "2026-10-25",
   "fichiers": [
    "../../Panini/README.md",
    "../../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md",
    "../../Panini/research/philosophy-theory/GRILLE_ABLATION_V14_v0.1.md",
    "../../Panini/research/nipada/falsification/analytic_sigs_v1.json"
   ],
   "note": "V14 de Research uniquement ; les 34 atomes de Panini-FS et les 9 dhatus de l'ancien docs/ de l'hote ne sont pas utilises."
  },
  "niveaux": {
   "fichiers": [
    "../docs/theorie/contrat-bloc-langue.md",
    "../docs/theorie/pre-traitement-linguistique.md",
    "rapport-bloc-linguistique.md"
   ],
   "note": "Le contrat compte 9 niveaux avec morphème ; le mandat J2.1 en liste 8. Le morphème reste un ancrage possible pour ∆ et λ, pas un porteur."
  }
 },
 "niveaux":
… [1894 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"B2\" docs/pilotage/roadmap.md | head -30; echo ---; grep -rn \"atome\" docs/pilotage/roadmap.md | head -30", "description": "Find B2 in roadmap"}`

  ```
268:| **B2** | représentation et raisonnement : RSN, composition, XNLI, 32 B | ✅ | aucune — l'échelle et la profondeur sont tracées |
444:- **clos** : B2.6 (le plan multi-tâches), B3 (le plan résiste), B4 (les opérateurs), B5/B6 (les jeux), B7/B8
---
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 
… [1768 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"14 flottants\\|44 œuvres\\|44 oeuvres\\|flottants\" docs/ reports/ --include=*.md | head -40", "description": "Search for 14 floats references"}`

  ```
docs/pilotage/semaine-autonome.md:70:| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |
docs/pilotage/semaine-autonome.md:271:coordination (S, A, N2, R). Puis Panini (le corpus à date contrôlée, les 44 œuvres).
docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domin
… [9440 caractères tronqués]
  ```

- **bash** `{"command": "ls ../Panini/research 2>/dev/null | head; echo ---; ls ../Panini | head -20; echo ---; ls ../Panini/research/nipada 2>/dev/null | head", "description": "Inspect Panini repo"}`

  ```
AGENTS.md
archives
archives_scripts_v1
autonomous-agents
colab_results
config
conftest.py
copilotage
data
deployments
---
config
CONTEXTE-IA.md
copilotage
corpus
data
Dockerfile.template
docs
experiments
experiments.json
legacy
modules
notebooks
outputs
Panini-AttributionRegistry
Panini.code-workspace
PHILOSOPHIE.md
pyproject.toml
README.md
research
scripts
---
api
closure
corpus
encyclopedia
falsification
fpga
modal
molecules
NAC_ROADMAP_v1.0.md
NIPADA_SEMANTIC_PIPELINE.md
  ```

- **bash** `{"command": "sed -n '55,90p' docs/pilotage/semaine-autonome.md; echo ===; sed -n '395,420p' reports/rapport-inventaire-panini.md", "description": "Read B2 task description and inventory excerpt"}`

  ```
- Les **14 atomes V14** (source canonique `research/src/nipada/core/hardware_mapping.py` ;
  ∃ ÊTRE, ∆ DIFFÉRENCE, ∼ RAPPORT, ↗ ORIENTATION, ⊙ SUJET, ⧖ TEMPS, ◇ MODALITÉ, № NOMBRE,
  ⊕ ESPACE, ⊗ OPÉRATION, λ FONCTION, ⊞ STRUCTURE, ≍ SYMÉTRIE, ≡ ÉQUATION) et les **9 dhātus**.
  Utilisables par Drave **en JSON plat, sans dépendance**.
- **La généalogie** : `src/nipada/signing/language_genealogy.py` (29 langues) et l'**UDHR 532
  langues** — la **même source XML** que Drave (456 langues avec glottocodes).
- Leur **avertissement** (à ne jamais oublier) : β **époque +0,138** vs **filiation +0,049**
  (R² 0,30) — la surface capte l'époque ; tout test de style contrôle la date, tout test de famille
  contrôle la surface.

**Les trois intégrations les plus mûres** (inventaire du 07/11) :

| # | intégration | livrable | contrôle négatif | risque |
|---|---|---|---|---|
| 1 | **UDHR + généalogie** (même source XML des deux côtés) | table iso3/famille/branche + échantillon 20 langues | familles différentes = retrieval faible ; sœurs = fort | codes ISO (007/008 vs iso3) |
| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes d
… [3301 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-atomes-niveaux.md", "description": "Read existing atomes-niveaux report"}`

  ```
# Table de correspondance — 14 atomes de Panini et 8 niveaux de Drave

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.1 · **Date** : 2026-11-07
> **Verdict** : ✅ **la table est complète** — 14 atomes, 8 niveaux, 14 lignes, un ancrage et un porteur par
> atome, une mesure possible et son contrôle négatif. ⚠️ **aucune correspondance atome ↔ niveau n'est mesurée à
> ce stade** : c'est une **hypothèse de lecture** et un **protocole**, pas une corrélation. La calibration des
> 44 œuvres de Panini montre **33 paires d'atomes à |r| ≥ 0,5** (brut), **4 composantes > 1** et **80,7 %** de
> la variance sur les trois premières (ACP sur CLR) : la colinéarité est le premier confondant, avant même
> l'époque.
> **Dispositif** : lecture seule de `../../Panini/research` (HEAD `e10d695`, 2026-10-25) ; signatures
> `../../Panini/research/nipada/falsification/analytic_sigs_v1.json` (44 œuvres, 2026-10-18) ; contrat des
> niveaux `../docs/theorie/contrat-bloc-langue.md` ; JSON [`atomes-niveaux.json`](atomes-niveaux.json).
> **Aucune écriture dans Panini** : les seuls fichiers produits sont cette fiche et son JSON.

## 1. La question, et ce que la table n'est pas

Un
… [8684 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"B2\\b\\|B2 —\\|B2 :\" docs/ reports/ journal/ REPRISE.md --include=*.md --include=*.json | head -40", "description": "Search B2 references everywhere"}`

  ```
docs/archive/roadmap-detail-2026-10-29.md:162:### B2 — La représentation et le raisonnement (étage 2)
docs/archive/roadmap-detail-2026-10-29.md:166:| B2.1 | **La RSN** : une représentation partagée, mais non alignée | ✅ | pont 28-69 %, cos 0,78-0,92, insensible à la taille |
docs/archive/roadmap-detail-2026-10-29.md:167:| B2.2 | **La composition** | ✅ | 0,61 / 0,84 → **0,76 / 0,865** au 7 B |
docs/archive/roadmap-detail-2026-10-29.md:168:| B2.3 | **Le raisonnement synthétique** : dans l'état, aligné par un pont linéaire | ✅ | 1,00 → 0,51 ; pont 0,46-1,00 ; quatre langues, douze personnes, trois échelles |
docs/archive/roadmap-detail-2026-10-29.md:169:| B2.4 | **L'alignement appris** : bilingue, contraste, saturation | ✅ | 0,656 → 0,742 → **0,753** ; le prix (in-langue 98,7 → 77,6) |
docs/archive/roadmap-detail-2026-10-29.md:170:| B2.5 | **Le raisonnement naturel** (XNLI) | ✅ | 0,50-0,59 ; pont 0,59 → **0,77** (fine-tuning) ; le domaine compte plus que le volume |
docs/archive/roadmap-detail-2026-10-29.md:171:| B2.6 | **Le plan multi-tâches** : entraîner le plan **et** le raisonnement ensemble | ✅ mesuré — **0,364** | l'EN→FR reste au chiffre de la tâche seule (0,364) ; l'in-langue 
… [7012 caractères tronqués]
  ```

- **bash** `{"command": "cat REPRISE.md | head -120", "description": "Read REPRISE.md"}`

  ```
# Reprise — démarrer une session de travail

> **Check-list, pas un état.** L'état vit dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; le plan
> dans [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) ; l'ancien index par module est archivé
> ([`docs/archive/etat-modules-2026-10-10.md`](docs/archive/etat-modules-2026-10-10.md)). Ce fichier ne dit que : quoi lire, quoi vérifier,
> quels pièges éviter, et où écrire. Le détail mesuré est dans [`reports/`](reports/) — **une fiche
> par expérience**. Version longue d'avant le 2026-10-10 :
> [`journal/2026-10-10/reprise-historique.md`](journal/2026-10-10/reprise-historique.md).

## 1. Les cinq premières minutes

```bash
date                                   # HAE (EDT, UTC−4) : on LIT l'horloge, on ne la suppose pas
git log --oneline -5                   # ce qui vient d'être fait
ls journal/ | tail -5                  # la journée en cours, par thème
```

Puis, dans l'ordre : [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) (l'état, **d'abord**) → **un**
document de tâche (`docs/methode/...`) → la fiche `reports/` du chantier. Le journal du jour ne se lit
que si l'on a besoin du **récit** ; la roadmap se lit
… [8063 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"atome\\|B2\\|Panini\\|J2\" docs/pilotage/en-cours.md | head -40", "description": "Search state for atomes/B2"}`

  ```
92:- **Panini J2.1–J3.2** : table **14 atomes** ; UDHR **418/438** ; J3.1 script domine, date non significative ; J3.2 : **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, **V14 3/21** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-faces.md).
93:- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../../reports/rapport-retrieval-familles.md).
94:- **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1 inter-traditions à ±10 ans,
98:- **Panini J12.1–J12.2 — §334 et CIC** : §334 — 655 lignes = 495 paires uniques ; [§334](../../reports/rapport-panini-334.md). CIC — **42/42** verdicts, **42/42** empreintes, **36/36** preuves altérées rejetées, **1 020/1 020** mutations de `eq(2,2)` rejetées ; [CIC](../../reports/rapport-cic-verificateur.md).
  ```

- **bash** `{"command": "sed -n '1,80p' docs/pilotage/en-cours.md", "description": "Read current state header"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 02 h 32 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**

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
> le h
… [4673 caractères tronqués]
  ```

- **bash** `{"command": "ls -la ../Panini/research/nipada/falsification/ | head -40; echo ===; python3 - <<'EOF'\nimport json\np='../Panini/research/nipada/falsification/analytic_sigs_v1.json'\nd=json.load(open(p))\nprint(len(d))\nfor k in list(d)[:5]: print(k, d[k])\nEOF", "description": "Inspect Panini falsif … [28 caractères tronqués]`

  ```
total 212144
drwxr-xr-x. 1 stephane stephane   21326 18 oct 10:03 .
drwxr-xr-x. 1 stephane stephane     650  4 jun 11:29 ..
-rw-r--r--. 1 stephane stephane   22381 18 oct 10:03 analytic_sigs_v1.json
-rw-r--r--. 1 stephane stephane    7048 18 oct 10:03 axeA_p1_subset_v1.json
-rw-r--r--. 1 stephane stephane    1644 18 oct 10:03 benchmark_generatif_analytique_v1.json
-rw-r--r--. 1 stephane stephane    4228 18 oct 10:03 benchmark_generatif_clean_v1.json
-rw-r--r--. 1 stephane stephane    9358  8 sep 15:34 benchmark_generatif_contenu_v1.json
-rw-r--r--. 1 stephane stephane    6059 18 oct 10:03 benchmark_generatif_corpus_v1.json
-rw-r--r--. 1 stephane stephane    2200 18 oct 10:03 benchmark_generatif_v1.json
-rw-r--r--. 1 stephane stephane   25410 30 avr  2026 circular_translation_test.json
-rw-r--r--. 1 stephane stephane    1738 18 oct 10:03 container_profiles_v1.json
-rw-r--r--. 1 stephane stephane    7948 28 jun 19:53 context_q1_embedding.json
-rw-r--r--. 1 stephane stephane    3849 28 jun 19:48 context_q1_normalized.json
-rw-r--r--. 1 stephane stephane   11481 28 jun 19:32 context_q1_translation_drift.json
-rw-r--r--. 1 stephane stephane     773 28 jun 19:32 context_q3_channel_stabil
… [4357 caractères tronqués]
  ```

- **bash** `{"command": "ls ../Panini/research/nipada/falsification/*.json | head; echo ===; ls ../Panini/research/nipada/corpus/ 2>/dev/null | head; echo ===; ls ../Panini/research/nipada/corpus/_cache/sources 2>/dev/null | head", "description": "List Panini corpus files"}`

  ```
../Panini/research/nipada/falsification/analytic_sigs_v1.json
../Panini/research/nipada/falsification/axeA_p1_subset_v1.json
../Panini/research/nipada/falsification/benchmark_generatif_analytique_v1.json
../Panini/research/nipada/falsification/benchmark_generatif_clean_v1.json
../Panini/research/nipada/falsification/benchmark_generatif_contenu_v1.json
../Panini/research/nipada/falsification/benchmark_generatif_corpus_v1.json
../Panini/research/nipada/falsification/benchmark_generatif_v1.json
../Panini/research/nipada/falsification/circular_translation_test.json
../Panini/research/nipada/falsification/container_profiles_v1.json
../Panini/research/nipada/falsification/context_q1_embedding.json
===
478c_url_validation_plan.json
ambiguity_annotations.json
ANALYSE_REFERENCES_V272_20260508.md
ANALYSE_REFERENCES_V272_CLEAN.md
archive_org_cache.json
archive_org_metadata_cache.json
_cache
catalog_african_colonial_v206x.json
catalog_buddhist_axial_v205.json
catalog_buddhist_late_antique_v206d.json
===
2_esdras.txt
apastamba_grhya_sutra.txt
aristotle_categories.txt
aristotle_de_caelo.txt
aristotle_nicomachean_ethics.txt
aristotle_parts_of_animals.txt
aristotle_posterior_analytics.txt
aristotl
… [113 caractères tronqués]
  ```

- **bash** `{"command": "ls ../Panini/research/nipada/corpus/ | grep -i \"334\\|manifest\\|source\\|meta\\|date\"; echo ===; find ../Panini/research -name \"*334*\" -maxdepth 4 | head -20", "description": "Find 334 metadata files"}`

  ```
archive_org_metadata_cache.json
signed_corpus_v309_manifest_de.json
signed_corpus_v310_manifest_en.json
===
../Panini/research/data/mass_ingestion/full_texts/pg22334_en.txt
../Panini/research/data/mass_ingestion/full_texts/pg23334_en.txt
../Panini/research/data/mass_ingestion/full_texts/pg23340_en.txt
../Panini/research/data/mass_ingestion/full_texts/pg23349_en.txt
../Panini/research/data/mass_ingestion/full_texts/pg25334_en.txt
../Panini/research/data/mass_ingestion/full_texts/pg26334_en.txt
../Panini/research/nipada/falsification/nipada_v334_graph_v35.json
../Panini/research/nipada/falsification/nipada_v334_graph_v35_gps.json
../Panini/research/nipada/falsification/nipada_v334_revalidation_v35.json
../Panini/research/nipada/falsification/pairs334_axes_v1.json
../Panini/research/nipada/fpga/sim/graph_sub334_dst.mem
../Panini/research/nipada/fpga/sim/graph_sub334_meta.json
../Panini/research/nipada/fpga/sim/graph_sub334_src.mem
../Panini/research/nipada/fpga/sim/graph_sub334_wgt.mem
../Panini/research/philosophy-theory/PREDICTION_V16_CORPUS_334_v0.1.md
../Panini/research/scripts/fetch_missing_334.py
../Panini/research/scripts/fetch_sources_334.py
  ```

- **bash** `{"command": "grep -rn \"pairs334\\|sources_manifest\\|year\\|date\" reports/rapport-panini-334.md | head -50", "description": "Find date sources in 334 report"}`

  ```
10:> **1 189** (**136** à ≤ 100 ans). Le contraste de filiation à **date fixe** est fort dans la tranche
18:> coefficient de date est **négatif** (**−0,006**) et non significatif. L'avertissement de Panini n'est
21:> **Dispositif** : les artefacts §334 de Panini/Nipada, lus en **lecture seule** — `pairs334_axes_v1.json`
23:> `nipada_v334_graph_v35.json` (1 753 nœuds) pour les dates, les traditions et les langues,
24:> `analytic_sigs_v1.json` (**44 œuvres × 14 atomes**), `sources_coverage.json` / `sources_manifest.json`
26:> pour la comparaison. Deux niveaux : **paire** (H0, date, filiation, contrôles) et **œuvre**
34:> **traductions anglaises** alors que la date est celle de la **composition** ; `d_topo` est une distance
35:> de **transmission**, corrélée à la date (ρ ≈ 0,61) ; les **44 signatures ne sont pas** les vecteurs qui
43:([`panini-nipada.md`](../docs/methode/panini-nipada.md)). Leur remède est de **contrôler la date** dans
59:composition — de tradition, de date et de **source/traduction**.
124:- **date contrôlée** : étiquettes de tradition permutées **dans chaque tranche de 250 ans** ;
131:Quatre tests sont déclarés **principaux** avant lecture : retrieval de filiation (d
… [3851 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/ | grep -i \"pos\\|tag\\|syntag\\|chunk\\|attach\\|langue\\|lingu\\|atome\\|panini\" | head -40", "description": "Find linguistic tools"}`

  ```
adaptateur_langue.py
bloc_linguistique.py
cancellation_langue.py
carte_langues.py
census_routage.py
code_partage.py
composition_latente.py
composition_multilingue.py
composition_verne.py
decomposition.py
decoupe_langues.py
domaine_ou_langue.py
etats_sans_langue.py
extraire_evals_langues.py
generer_par_langue.py
langue_dans_etat.py
langue_dans_etat_v1_fautif.py
mesure_langues.py
ou_entre_la_langue.py
panini_334.py
pensee_multilingue.py
penser_sans_langue.py
plan_entrainement_bilingue.py
plateau_multilingue.py
porte-bloc-linguistique.sh
porte-n3-composition.sh
porte-n3-positions.sh
position_multilingue.py
position_seule.py
profil_langues.py
  ```

- **bash** `{"command": "grep -rln \"POS\\|pos\" tools/*.py | head -30; echo ===; ls reports/ | grep -i \"pos\\|tagger\\|syntag\\|attach\\|langue\" | head -30", "description": "Find POS scripts and reports"}`

  ```
tools/adaptateur_langue.py
tools/aiguille.py
tools/aligneur_litteraire.py
tools/amplification.py
tools/analyse_empreinte.py
tools/analyse_engram.py
tools/analyse_flux.py
tools/analyse_hc.py
tools/analyse_litteraire.py
tools/analyse_octets_par_jeton.py
tools/ancre_professeur.py
tools/applique_pont.py
tools/approximabilite_bloc.py
tools/audit_drapeaux_harnais.py
tools/banc_durci.py
tools/banc-experts.py
tools/banc_lecteur.py
tools/blanchiment_entree.py
tools/bloc_code.py
tools/bloc_linguistique.py
tools/bloc_maths.py
tools/bloc_tableaux.py
tools/boucle_directe.py
tools/c8_entrainer_tete.py
tools/c8_sonde_lineaire.py
tools/cache_pont.py
tools/calibre_modes.py
tools/campagne_synthese.py
tools/canal_structure.py
tools/cancellation_langue.py
===
carte-24langues-3b.json
carte-24langues.json
composition-latente-14b.json
composition-latente-3b.json
composition-latente-7b.json
composition-multilingue.json
composition-penalite-3b.json
composition-penalite-7b.json
composition-verne-14b.json
composition-verne-7b.json
composition-verne.json
composition-verne-large.json
composition-verne-plan.json
evaluer-langue.json
jeux-langues-mesures.json
n3.4a-composition.json
n3.5f-positions.json
pensee-att
… [394 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/panini_334.py tools/bloc_linguistique.py; echo ===; grep -n \"def \\|POS\\|syntag\\|attach\\|analytic\" tools/panini_334.py | head -80", "description": "Inspect panini_334 tool"}`

  ```
1500 tools/panini_334.py
  2906 tools/bloc_linguistique.py
  4406 total
===
44:CE QUE LE DISPOSITIF NE PEUT PAS DIRE.
45:  - La date attachée à une œuvre est sa date de **composition** (ou son
81:SIGNATURES = PANINI / "nipada" / "falsification" / "analytic_sigs_v1.json"
139:def sha256(chemin: pathlib.Path) -> str:
147:def lire_json(chemin: pathlib.Path):
151:def commit_git(chemin: pathlib.Path) -> str | None:
160:def moyenne(valeurs) -> float:
164:def ecart_type(valeurs) -> float:
168:def ic95(valeurs) -> list[float] | None:
174:def p_unilateral(null, observe, sens="superieur") -> float:
182:def p_bilateral(null, observe) -> float:
188:def standardise(v: np.ndarray) -> np.ndarray:
194:def ols(y, X, poids=None):
214:def r2_partiel(r2_joint: float, r2_sans: float) -> float:
218:def auc(y, score) -> float:
230:def logit(y, X, max_iter=100):
250:def bin_date(annee: float) -> int:
254:def tradition_large(etiquette: str | None) -> str:
259:def auteur_canonique(auteur: str | None) -> str:
268:def charger():
335:def analyser_paires(paires, textes, ids_paires, n_perm=2000, n_boot=1000, graine=0):
641:    def contraste(masque):
751:def construire_matrice(textes, ids_signes):
758:def ordre_ca
… [491 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def \\|POS\\|syntag\\|attach\\|chunk\\|NIVEAU\\|niveau\" tools/bloc_linguistique.py | head -80", "description": "Inspect bloc_linguistique tool"}`

  ```
12:  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
13:    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
15:    étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
50:NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
63:    def json(self) -> dict:
69:    niveau: str
81:    def json(self) -> dict:
83:            "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
92:# v2 : ajoute `meta.partition` et `meta.alternative` (partition des syntagmes qui se
111:    def par_niveau(self) -> dict[str, list[Etiquette]]:
114:            sortie[e.niveau].append(e)
117:    def couverture(self) -> dict[str, float]:
118:        """La confiance maximale par niveau — la couverture *déclarée*, pas une précision."""
120:                for n, es in self.par_niveau().items()}
122:    def json(self, avec_duree: bool = False) -> dict:
141:    def analyser(self, texte: str, langue: str | None = None,
152:def _normaliser(texte: str) -> str:
156:def _
… [4283 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '795,870p' tools/bloc_linguistique.py; echo ===; sed -n '1380,1480p' tools/bloc_linguistique.py", "description": "Read Analyzer API"}`

  ```
class Heuristique:
    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""

    nom = "heuristique"

    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
                 union: bool = True, partition: str = "alternative"):
        self.profils = profils
        self.segmenter_s = segmenter_s
        self.seuil_ouvert = seuil_ouvert
        self.seuil_langue = seuil_langue
        self.union = union
        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
        # "filtrer_union" : on retire le S qui **contient** un segment chunker (le filtre
        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
        # Dans les deux filtres, le segment retiré reste dans `meta.alternative` (`retire`).
        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
            raise ValueError("partition attend 'brut', 'alternative', 'filtrer_union' ou 'filtrer'")
        self.partition =
… [9060 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '268,340p' tools/panini_334.py", "description": "Read loader for works and dates"}`

  ```
def charger():
    paires = lire_json(PAIRES)
    graphe = lire_json(GRAPHE)
    signatures = lire_json(SIGNATURES)
    revalidation = lire_json(REVALIDATION)
    couverture = {x["id"]: x for x in lire_json(COUVERTURE)}
    manifeste = {x["id"]: x for x in lire_json(MANIFESTE)}
    noeuds = graphe["nodes"]

    ids_paires = sorted({p["a"] for p in paires["pairs"]} | {p["b"] for p in paires["pairs"]})
    ids_signes = sorted(signatures)

    textes = {}
    for tid in ids_paires:
        n = noeuds.get(tid, {})
        m = manifeste.get(tid, {})
        c = couverture.get(tid, {})
        textes[tid] = {
            "id": tid,
            "annee": n.get("year"),
            "tradition_fine": n.get("tradition_label") or "",
            "tradition_large": tradition_large(n.get("tradition_label")),
            "tradition_micro": n.get("tradition_micro") or "",
            "auteur": auteur_canonique(n.get("author")),
            "auteur_brut": n.get("author") or "",
            "langue_origine": n.get("language_original") or n.get("lang") or "",
            "langue_source": (m.get("lang") or "").strip(),
            "url_source": (m.get("url") or "").strip(),
            "source_ok": bo
… [2447 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,140p' tools/panini_334.py", "description": "Read paths and constants"}`

  ```
Usage :
  python3 tools/panini_334.py
  python3 tools/panini_334.py --rapide
  python3 tools/panini_334.py --sortie /tmp/panini-334.json
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib
import subprocess

import numpy as np
from scipy import stats

RACINE = pathlib.Path(__file__).resolve().parent.parent
PANINI = RACINE.parent / "Panini" / "research"
PAIRES = PANINI / "nipada" / "falsification" / "pairs334_axes_v1.json"
GRAPHE = PANINI / "nipada" / "falsification" / "nipada_v334_graph_v35.json"
SIGNATURES = PANINI / "nipada" / "falsification" / "analytic_sigs_v1.json"
REVALIDATION = PANINI / "nipada" / "falsification" / "nipada_v334_revalidation_v35.json"
COUVERTURE = PANINI / "nipada" / "corpus" / "_cache" / "sources_coverage.json"
MANIFESTE = PANINI / "nipada" / "corpus" / "_cache" / "sources_manifest.json"
V150 = PANINI / "nipada" / "falsification" / "nipada_v150_validation.json"
SORTIE_DEFAUT = RACINE / "reports" / "panini-334.json"

ATOMES = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS", "MODALITÉ",
    "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION", "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

… [1970 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport panini_334 as p\npaires, graphe, sigs, reval, textes, ids_paires, ids_signes, audit = p.charger()\nprint('ATOMES', p.ATOMES)\nfor t in audit['textes'][:3]:\n    print(t)\nprint('...')\nprint('44', len(ids_signes))\nimport … [285 caractères tronqués]`

  ```
ATOMES ['ÊTRE', 'DIFFÉRENCE', 'RAPPORT', 'ORIENTATION', 'SUJET', 'TEMPS', 'MODALITÉ', 'NOMBRE', 'ESPACE', 'OPÉRATION', 'FONCTION', 'STRUCTURE', 'SYMÉTRIE', 'ÉQUATION']
{'id': '2_esdras', 'annee': 100, 'tradition_fine': 'JUDEAN_APOCALYPTIC_LATE', 'tradition_large': 'ABRAHAMIC', 'tradition_micro': 'JEWISH_APOCALYPTIC', 'auteur': 'anonymous (Ezra apocalypse tradition)', 'auteur_brut': 'anonymous (Ezra apocalypse tradition)', 'langue_origine': 'eng', 'langue_source': 'eng', 'url_source': 'https://www.sacred-texts.com/bib/poly/es2.htm', 'source_ok': True, 'mots_source': 3733, 'titre': '2 Esdras / 4 Ezra (Polyglot Bible)', 'kind': 'apocalyptic_text', 'signe': True, 'signature': [0.07446500282604852, 0.013816044014481109, 0.10099345547363615, 0.005331763602619648, 0.14124697298283334, 0.05189835957545314, 0.02705634807902917, 0.14932406971800052, 0.04847053574653187, 0.06701372487945408, 0.12163933372805281, 0.14742169250272855, 0.0006717195879862289, 0.050650977283144785]}
{'id': 'an7_64_kodhana', 'annee': -410, 'tradition_fine': 'BUDDHIST_AXIAL', 'tradition_large': 'BUDDHIST', 'tradition_micro': 'BUDDHISM_THERAVADA', 'auteur': 'anonymous_sangha', 'auteur_brut': 'anonymous_sangha', 'lang
… [961 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='../Panini/research/nipada/corpus/_cache/sources_manifest.json'\nd=json.load(open(p))\nprint(type(d), len(d))\nif isinstance(d,dict):\n    for k in list(d)[:3]: print(k, json.dumps(d[k],ensure_ascii=False)[:500])\nelse:\n    print(d[0])\nEOF", "descript … [33 caractères tronqués]`

  ```
<class 'list'> 107
{'id': 'dn1_brahmajala', 'lang': 'eng', 'url': 'https://suttacentral.net/dn1/en/sujato', 'title': 'dn1_brahmajala'}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, pathlib, json\nsys.path.insert(0,'tools')\nimport panini_334 as p\npaires, graphe, sigs, reval, textes, ids_paires, ids_signes, audit = p.charger()\nman=json.load(open(p.MANIFESTE))\ncouv=json.load(open(p.COUVERTURE))\nfor k in list(man)[:2]:\n    print(js … [203 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 8, in <module>
TypeError: list indices must be integers or slices, not dict
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\nbase=pathlib.Path('../Panini/research/nipada')\nfor name in ['corpus/_cache/sources_coverage.json','corpus/_cache/sources_manifest.json']:\n    d=json.load(open(base/name))\n    print(name, type(d), len(d))\n    for x in d[:2]: print(json.dumps(x … [164 caractères tronqués]`

  ```
corpus/_cache/sources_coverage.json <class 'list'> 107
{"id": "dn1_brahmajala", "ok": true, "words": 12773}
{"id": "dn2_samannaphala", "ok": true, "words": 12082}
corpus/_cache/sources_manifest.json <class 'list'> 107
{"id": "dn1_brahmajala", "lang": "eng", "url": "https://suttacentral.net/dn1/en/sujato", "title": "dn1_brahmajala"}
{"id": "dn2_samannaphala", "lang": "eng", "url": "https://suttacentral.net/dn2/en/sujato", "title": "dn2_samannaphala"}
===
102
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, pathlib, hashlib\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\nmiss=[]\nfor t in ids_signes:\n    f=base/(t+'.txt')\n    if not f.exists(): miss.append(t) … [310 caractères tronqués]`

  ```
missing []
n 44 min 1210 max 1419392 sum 6205139
median 64191.0
  ```

- **bash** `{"command": "grep -n \"attachement\\|attacher\\|cible\\|niveau.*syntagme\" tools/bloc_linguistique.py | head -40; echo ===; sed -n '110,150p' tools/bloc_linguistique.py", "description": "Find attachment output fields"}`

  ```
997:    def _cibles_s(self, texte: str) -> dict:
998:        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
1001:        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
1009:            return {(s.debut, s.fin, s.type): (s.cible_gp or s.cible_nom or s.cible_verbe)
1015:    def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
1028:    def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict]) -> str | None:
1031:        Le gold : « elle qui commence nage » → REL « qui commence » a pour cible `elle`,
1070:    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict]) -> str | None:
1085:    def _repli_verbe_propre(texte: str, segment: dict, cible: str | None):
1087:        if cible or segment.get("type") not in ("SUB", "REL"):
1088:            return cible
1089:        return Heuristique._verbe_dans(texte, segment["debut"], segment["fin"]) or cible
1092:    def _cible_hors_span(texte: str, segment: dict, gvs: list[dict], cible: str | None):
1098:        if not cible or segment.get("type") not in ("GP", "SUB"):
1099:            return cible
1101:        if _normali
… [3736 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"attachement\" reports/rapport-bloc-linguistique.md | head -20; echo ===; sed -n '1,60p' reports/rapport-bloc-linguistique.md", "description": "Read language block report header"}`

  ```
75:| syntagme | 0,40 | 0,78 | GN/GV/GP/REL/SUB, rôles, attachements candidats |
===
# Le bloc linguistique — 398 langues au niveau langue, un contrat pour l'heuristique et le neuronal

> **Ligne de roadmap** : **R0.7** (proposition — la couche linguistique de surface) · **Date** :
> 2026-11-01 · **Verdict** : ✅ **le contrat tient** : neuf niveaux, deux implémentations
> substituables, un parallèle et une cascade, une activation sémantique à **51–76 %** ; la
> **langue** est mesurée à **0,9687** sur **398 langues** (script **1,0000**, profils permutés
> **0,0022**). ⚠️ **les niveaux profonds n'ont pas de gold** et le **modèle neuronal réel n'est
> pas qualifié** (le `llama-cli` local a expiré) : la couverture est **déclarée**, pas prouvée.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`porte-bloc-linguistique.sh`](../tools/porte-bloc-linguistique.sh),
> [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py),
> JSON [`bloc-linguistique.json`](bloc-linguistique.json). Contrat :
> [`bloc-linguistique.md`](../docs/implantation/bloc-linguistique.md).

## 1. La question

Peut-on avoir **un seul bloc** qui étiquette du **grap
… [2296 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, pathlib, json, time\nsys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique, charger_profils_udhr\nh=Heuristique(profils=None)\nt0=time.time()\ntxt=open('../Panini/research/nipada/corpus/ … [564 caractères tronqués]`

  ```
time 0.6350014209747314 lang en 
etiquettes 18124
{'niveau': 'graphème', 'type': 'lettres', 'valeur': 'The', 'debut': 0, 'fin': 3, 'source': 'heuristique', 'confiance': 0.99, 'candidats': [], 'langue': 'en', 'script': 'Latn', 'meta': {}}
{'niveau': 'mot', 'type': 'mot', 'valeur': 'The', 'debut': 0, 'fin': 3, 'source': 'heuristique', 'confiance': 0.98, 'candidats': [], 'langue': 'en', 'script': 'Latn', 'meta': {}}
{'niveau': 'pos', 'type': 'DET', 'valeur': 'The', 'debut': 0, 'fin': 3, 'source': 'heuristique', 'confiance': 0.92, 'candidats': [], 'langue': 'en', 'script': 'Latn', 'meta': {'ouvert': False}}
{'niveau': 'syntagme', 'type': 'GN', 'valeur': 'The Project Gutenberg eBook', 'debut': 0, 'fin': 27, 'source': 'heuristique', 'confiance': 0.35, 'candidats': ['GN', 'parts', 'restrictions', 'it'], 'langue': 'en', 'script': 'Latn', 'meta': {'role': 'groupe nominal', 'niveau': 0, 'attachement': {'segment': 'The Project Gutenberg eBook', 'cible': 'parts'}}}
{'niveau': 'discours', 'type': 'connecteur', 'valeur': 'in', 'debut': 0, 'fin': 200, 'source': 'heuristique', 'confiance': 0.55, 'candidats': ['but'], 'langue': 'en', 'script': 'Latn', 'meta': {}}
{'niveau': 'phrase', 'type': 'type'
… [4790 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"sources\\|\\.txt\\|Gutenberg\\|nettoy\\|clean\" tools/panini_334.py | head -40; echo ===; grep -rn \"def charger_texte\\|def lire_texte\\|Gutenberg\" tools/*.py | head -20", "description": "Find text cleaning code"}`

  ```
7:paires finies, 102 sources acquises) et les signatures V14 de 44 œuvres (14 parts
39:      (24 sources `eng`, 1 `fra`, 19 langue inconnue). On refait le modèle de
57:Aucune écriture dans Panini : les sources sont lues en lecture seule, avec
83:COUVERTURE = PANINI / "nipada" / "corpus" / "_cache" / "sources_coverage.json"
84:MANIFESTE = PANINI / "nipada" / "corpus" / "_cache" / "sources_manifest.json"
318:        "sources_manifeste": len(manifeste),
319:        "sources_ok": sum(1 for x in couverture.values() if x.get("ok")),
320:        "sources_ok_parmi_48": sum(1 for tid in ids_paires if textes[tid]["source_ok"]),
321:        "sources_ok_parmi_44": sum(1 for tid in ids_signes if textes[tid]["source_ok"]),
1376:            "sources_ok": audit["sources_ok"],
1377:            "sources_manifeste": audit["sources_manifeste"],
1378:            "sources_ok_parmi_44": audit["sources_ok_parmi_44"],
1451:        "sources": {
1469:            "la date est la date de composition (ou son estimation), pas la date de traduction ; 24/44 sources sont anglaises, 1 française, 19 de langue inconnue",
===
tools/aligneur_litteraire.py:347:    """Lit un texte Gutenberg, retire le BOM, les CRLF et l'a
… [1254 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '330,380p' tools/aligneur_litteraire.py", "description": "Read Gutenberg cleaner"}`

  ```
def romain_vers_entier(romain: str) -> int:
    total = 0
    precedent = 0
    for caractere in reversed(romain.upper()):
        valeur = _VALEURS_ROMAINES[caractere]
        total += -valeur if valeur < precedent else valeur
        precedent = max(precedent, valeur)
    return total


DEBUT_GUTENBERG = re.compile(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG[^\n]*\*\*\*")
FIN_GUTENBERG = re.compile(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG[^\n]*\*\*\*")


def lire_gutenberg(chemin: Path) -> str:
    """Lit un texte Gutenberg, retire le BOM, les CRLF et l'appareil Gutenberg."""
    brut = chemin.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    debut = DEBUT_GUTENBERG.search(brut)
    fin = FIN_GUTENBERG.search(brut)
    if debut and fin and fin.start() > debut.end():
        brut = brut[debut.end() : fin.start()]
    return brut.strip("\n")


def _bloc_titre(lignes: list[str], i: int) -> tuple[int, str]:
    """Après l'en-tête ligne `i`, retourne (début du corps, titre).

    Le titre est un bloc de lignes majoritairement en majuscules ; s'il n'y en a pas, on ne consomme rien.
    """
    n = len(lignes)
    j = i + 1
    while j < n and 
… [613 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, pathlib, re\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\nfor t in ids_signes:\n    s=open(base/(t+'.txt'),encoding='utf-8',errors='replace').read()\n     … [259 caractères tronqués]`

  ```
2_esdras 102937 False '// Apply the local archive-bar preference before shared HTML can paint. try { document.doc'
aristotle_categories 100859 True 'The Project Gutenberg eBook of The Categories This eBook is for the use of anyone anywhere'
aristotle_de_caelo 75423 False '{{header | title = On the Heavens | author = Aristotle | translator = John Leofric Stocks '
aristotle_parts_of_animals 43441 False "{{header | title = [[../]] | author = Aristotle | translator = William Ogle | section = ''"
aristotle_posterior_analytics 6751 False '{{header | title = Posterior Analytics | author = Aristotle | translator = E. S. Bouchier '
aristotle_prior_analytics 5110 False '<HTML> <HEAD> <!--The Internet Classics Archive by Daniel C. Stevenson, Web Atomics. World'
bengio_2003 63198 False '%PDF-1.1 % 2 0 obj < < /Length 5589 /Filter /LZWDecode >> stream \x10y\x18l \x18 `P\\9\x1b\x06\x11!\x04: A eR_BT'
book_of_enoch 5246 False 'Title The Book of Enoch Author Unknown author Translated by R.H. Charles Details 115 chapt'
curry_1930 129182 False "Stanford Encyclopedia of Philosophy Menu Browse Table of Contents What's New Random Entry "
daniel_book 1695 False 'Daniel Back to book Daniel The archive, o
… [3269 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, pathlib\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\nsizes=sorted(((base/(t+'.txt')).stat().st_size,t) for t in ids_signes)\nprint(sizes[-5:])\nEOF\nwhic … [78 caractères tronqués]`

  ```
[(388414, 'plato_theaetetus_jowett'), (498777, 'russell_parousia_1878'), (656863, 'aristotle_nicomachean_ethics'), (1338923, 'plato_laws'), (1419392, 'plato_republic_jowett')]
/usr/bin/pdftotext
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 - <<'EOF'\nimport sys, time\nsys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique\nfrom aligneur_litteraire import lire_gutenberg\nfrom pathlib import Path\nh=Heuristique()\np=Path('../Panini/rese … [315 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-36]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-36"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, pathlib\nfrom collections import Counter\nsys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique\nfrom aligneur_litteraire import lire_gutenberg\nh=Heuristique()\ntxt=lire_gutenberg(pathl … [719 caractères tronqués]`

  ```
POS Counter({'NOUN': 2776, 'PONCT': 1613, 'PREP': 1185, 'DET': 1025, 'AUX': 927, 'VERB': 732, 'CONJ': 605, 'PRON': 552, 'ADJ': 545, 'ADV': 308, 'NUM': 100})
SYN Counter({'GV': 1028, 'GP': 823, 'GN': 673, 'SUB': 197, 'REL': 147})
SYN roles Counter({'prédicat': 1028, 'groupe nominal': 483, 'theme': 271, 'agent': 237, 'but': 231, 'complément': 223, 'lieu': 206, 'qualité': 147, 'moyen': 39, 'temps': 3})
PRAG Counter({'acte': 357, 'double_sens': 6})
DISC Counter({'connecteur': 304, 'paragraphe': 1})
PHRASE Counter({'type': 357, 'négation': 143, 'modalité': 81})
  ```

- **job_output** `{"job_id": "bash-36"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps aux | grep -E \"python3 -|bloc_ling\" | grep -v grep | head", "description": "Check running analysis process"}`

  ```
stephane 2954023  0.1  0.0   7700  4188 ?        Ss   03:08   0:00 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 - <<'EOF' import sys, time sys.path.insert(0,'tools') from bloc_linguistique import Heuristique from aligneur_litteraire import lire_gutenberg from pathlib import Path h=Heuristique() p=Path('../Panini/research/nipada/corpus/_cache/sources/plato_republic_jowett.txt') t=time.time(); txt=lire_gutenberg(p); print('read',len(txt),time.time()-t) t=time.time(); a=h.analyser(txt,'en'); print('analyse',time.time()-t,'etiquettes',len(a.etiquettes),'lang',a.langue) EOF
stephane 2954030  0.0  0.0   5848  2508 ?        S    03:08   0:00 timeout 300 python3 -
stephane 2954031  100  0.5 729224 713992 ?       R    03:08   1:29 python3 -
  ```

- **job_kill** `{"job_id": "bash-36", "reason": "Full-text analysis too slow; switching to fixed-size samples"}`

  ```
requested cancellation of job bash-36
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\ncouv={x['id']:x for x in json.load(open(p.COUVERTURE))}\nws=sorted((couv[t].get('words') or 0,t) for t in ids_signes)\nprint(ws[:12])\nprint('>=1000',sum(1 … [158 caractères tronqués]`

  ```
[(304, 'mengzi'), (328, 'hosea_book'), (342, 'zechariah_book'), (422, 'aristotle_prior_analytics'), (451, 'lukasiewicz_1920'), (483, 'daniel_book'), (555, 'mn35_culasaccaka'), (600, 'mikolov_2013'), (788, 'qiwulun'), (827, 'book_of_enoch'), (941, 'aristotle_posterior_analytics'), (1129, 'kleene_1936')]
>=1000 33 >=2000 28 >=5000 26
  ```

- **bash** `{"command": "grep -rn \"analytic_sigs_v1\\|analytic_sigs\" ../Panini/research --include=*.py --include=*.md | head -20", "description": "Find signature computation code"}`

  ```
../Panini/research/scripts/loi_analytique.py:21:CACHE = OUT / "analytic_sigs_v1.json"
  ```

- **bash** `{"command": "grep -rn \"def.*sign\\|def.*analytic\\|Gutenberg\\|clean\" ../Panini/research/nipada/signing/*.py 2>/dev/null | head -40; ls ../Panini/research/nipada/signing 2>/dev/null", "description": "Inspect signing module"}`

  ```
(no output)
[exit code: 2]
  ```

- **bash** `{"command": "sed -n '1,120p' ../Panini/research/scripts/loi_analytique.py", "description": "Read signature computation script"}`

  ```
#!/usr/bin/env python3
"""Loi H₀′ avec la projection ANALYTIQUE (sign_analytic) — round 18.

Même protocole que la re-fondation (paires §334 officielles couvertes par les textes
ré-acquis, split hors hold-out v1), mais d_lex calculé sur les signatures analytiques
dynamiques (WordNet→supersense→E-V14→V14), au lieu du signeur lexical saturant.
Usage : PYTHONPATH=src python3 scripts/loi_analytique.py
"""
from __future__ import annotations
import json
from multiprocessing import Pool
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "nipada" / "corpus" / "_cache" / "sources"
OUT = ROOT / "nipada" / "falsification"
W = 10000
V14 = ["ÊTRE","DIFFÉRENCE","RAPPORT","ORIENTATION","SUJET","TEMPS","MODALITÉ",
       "NOMBRE","ESPACE","OPÉRATION","FONCTION","STRUCTURE","SYMÉTRIE","ÉQUATION"]
CACHE = OUT / "analytic_sigs_v1.json"


def sign_one(nid):
    p = SRC / f"{nid}.txt"
    if not p.exists(): return (nid, None)
    words = p.read_text(encoding="utf-8").split()
    if len(words) < 300: return (nid, None)
    try:
        from nipada.signing.analytical_projection import sign_analytic
        return (nid, sign_analytic(" ".join(words[:W])
… [1705 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\ncounts=[]\nfor t in ids_signes:\n    w=(base/(t+'.txt')).read_text(encoding='utf-8',errors='replace').split() … [313 caractères tronqués]`

  ```
[(304, 'mengzi'), (328, 'hosea_book'), (342, 'zechariah_book'), (422, 'aristotle_prior_analytics'), (451, 'lukasiewicz_1920'), (483, 'daniel_book'), (555, 'mn35_culasaccaka'), (600, 'mikolov_2013'), (788, 'qiwulun'), (827, 'book_of_enoch')]
>=10k 23 >=20k 7 >=30k 6
[(10668, 'plato_charmides'), (11008, 'nostradamus_centuries'), (11411, 'quillian_1968'), (11451, 'plato_sophist'), (11553, 'schank_1972'), (11803, 'plato_philebus_jowett'), (12462, 'plato_gorgias'), (12462, 'plato_gorgias_jowett'), (12772, 'plato_meno'), (12772, 'plato_meno_jowett'), (12773, 'dn1_brahmajala'), (13271, 'plato_phaedo'), (13559, 'aristotle_de_caelo'), (17525, 'aristotle_categories'), (18585, 'curry_1930'), (19077, 'plato_symposium_jowett')]
  ```

- **bash** `{"command": "git status --short | head -30; echo ===; git branch --show-current; date", "description": "Check git status and date"}`

  ```
M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-gold-reel-50.json
?? reports/rapport-gold-reel-50.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
===
s/v7
dim 15 nov 2026 03:11:21 EST
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, sys, pathlib, subprocess\nfrom html.parser import HTMLParser\nsys.path.insert(0,'tools')\nimport panini_334 as p\n\nclass _Strip(HTMLParser):\n    def __init__(self):\n        super().__init__(); self.ou … [1984 caractères tronqués]`

  ```
2_esdras raw 102937 clean 47866 alpha% 73.4 '// Apply the local archive-bar preference before shared HTML can paint. try catch (e) // Pre-paint theme: mirror mode-wa'
bengio_2003 raw 0 clean 0 alpha% 0.0 ''
plato_republic_jowett raw 1419135 clean 1415223 alpha% 76.5 'The Project Gutenberg eBook of The Republic of Plato This eBook is for the use of anyone anywhere in the United States a'
mengzi raw 1664 clean 1492 alpha% 78.2 "Mencius went to see king Hûi of Liang. The king said, 'Venerable sir, since you have not counted it far to come here, a "
qiwulun raw 4472 clean 4472 alpha% 74.6 'T T O T P Title The Texts of Taoism, Part I of II Author Unknown author Translated by James Legge Details 139 chapters E'
aristotle_de_caelo raw 75423 clean 75234 alpha% 79.3 '==Part 1== The science which has to do with nature clearly concerns itself for the most part with bodies and magnitudes '
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, pathlib, subprocess\nsys.path.insert(0,'tools')\nimport panini_334 as p\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\nfor t in ['2_esdras','bengio_2003','plato_republic_jowett']:\n    raw=(base/( … [464 caractères tronqués]`

  ```
==== 2_esdras 103170 b'// Apply the local archive-bar preference before shared HTML'
*** START -1
***START -1
Project Gutenberg -1
<script -1
<body -1
Chapter 52125
CHAPTER -1
==== bengio_2003 66060 b'%PDF-1.1 % 2 0 obj < < /Length 5589 /Filter /LZWDecode >> st'
*** START -1
***START -1
Project Gutenberg -1
<script -1
<body -1
Chapter -1
CHAPTER -1
==== plato_republic_jowett 1419392 b'The Project Gutenberg eBook of The Republic of Plato This eB'
*** START 759
***START -1
Project Gutenberg 4
<script -1
<body -1
Chapter -1
CHAPTER -1
===
../Panini/research/nipada/corpus/_cache/sources/bengio_2003.txt: PDF document, version 1.1, 10 page(s)
Syntax Error (22): Illegal character <3c> in hex string
Syntax Error (24): Illegal character <2f> in hex string
Syntax Error (25): Illegal character <4c> in hex string
Syntax Error (27): Illegal character <6e> in hex string
Syntax Error (28): Illegal character <67> in hex string
  ```

- **bash** `{"command": "python3 - <<'EOF'\ns=open('../Panini/research/nipada/corpus/_cache/sources/plato_republic_jowett.txt',encoding='utf-8',errors='replace').read()\nprint(repr(s[700:1100]))\nprint('END',s.upper().rfind('END OF'))\nEOF", "description": "Inspect Gutenberg markers"}`

  ```
'gutenberg.org/ebooks/55201 Credits: Produced by Ed Brandon *** START OF THE PROJECT GUTENBERG EBOOK THE REPUBLIC OF PLATO *** THE REPUBLIC OF PLATO _JOWETT_ London HENRY FROWDE OXFORD UNIVERSITY PRESS WAREHOUSE AMEN CORNER, E. C. THE REPUBLIC OF PLATO TRANSLATED INTO ENGLISH WITH _INTRODUCTION, ANALYSIS MARGINAL ANALYSIS, AND INDEX_ BY B. JOWETT, M.A. MASTER OF BALLIOL COLLEGE REGIUS PROFESSOR OF '
END 1400978
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\ns=open('../Panini/research/nipada/corpus/_cache/sources/plato_republic_jowett.txt',encoding='utf-8',errors='replace').read()\npat=re.compile(r'\\*\\*\\*\\s*START OF (?:THE|THIS) PROJECT GUTENBERG[^\\n]*\\*\\*\\*',re.I)\nprint(pat.search(s))\nprint(repr(s[74 … [50 caractères tronqués]`

  ```
<re.Match object; span=(759, 1401038), match='*** START OF THE PROJECT GUTENBERG EBOOK THE REPU>
'uced by Ed Brandon *** START OF THE PROJECT GUTENBERG EBOOK THE REPUBLIC OF PLATO *** THE REPUBLIC OF PLATO _JOWETT_ Lon'
  ```

- **bash** `{"command": "python3 - <<'EOF'\ns=open('../Panini/research/nipada/corpus/_cache/sources/2_esdras.txt',encoding='utf-8',errors='replace').read()\nprint(repr(s[49000:51000]))\nprint('---')\nprint(repr(s[51500:52800]))\nEOF", "description": "Inspect 2_esdras junk region"}`

  ```
'-foreground h-8 text-sm" data-slot="tooltip-trigger" data-sidebar="menu-button" data-size="default" id="bits-s110" data-state="closed" data-delay-duration="0" data-tooltip-trigger="" tabindex="0" type="button"> Unicode span:last-child]:truncate hover:bg-sidebar-accent hover:text-sidebar-accent-foreground h-8 text-sm" data-slot="tooltip-trigger" data-sidebar="menu-button" data-size="default" id="bits-s111" data-state="closed" data-delay-duration="0" data-tooltip-trigger="" tabindex="0" type="button"> Volunteer span:last-child]:truncate hover:bg-sidebar-accent hover:text-sidebar-accent-foreground h-8 text-sm" data-slot="tooltip-trigger" data-sidebar="menu-button" data-size="default" id="bits-s112" data-state="closed" data-delay-duration="0" data-tooltip-trigger="" tabindex="0" type="button"> Wishlist span:last-child]:truncate hover:bg-sidebar-accent hover:text-sidebar-accent-foreground h-8 text-sm" data-slot="tooltip-trigger" data-sidebar="menu-button" data-size="default" id="bits-s113" data-state="closed" data-delay-duration="0" data-tooltip-trigger="" tabindex="0" type="button"> Community Guidelines span:last-child]:truncate hover:bg-sidebar-accent hover:text-sidebar-accent-foregr
… [2109 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for opt in \"\" \"-raw\" \"-layout\"; do echo \"== $opt\"; pdftotext $opt ../Panini/research/nipada/corpus/_cache/sources/bengio_2003.txt - 2>/dev/null | head -c 200; echo; done", "description": "Try pdftotext modes on bengio_2003"}`

  ```
== 

== -raw

== -layout
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, re, pathlib\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\nSTOP=set('the of and to in a is that it fo … [1024 caractères tronqués]`

  ```
stop 0.007 mark 0.087 alpha 0.495 n  6607 bengio_2003
stop 0.012 mark 0.000 alpha 0.328 n  1609 jeremiah_book
stop 0.012 mark 0.000 alpha 0.364 n  1579 isaiah_book
stop 0.013 mark 0.000 alpha 0.321 n  1506 ezekiel_book
stop 0.039 mark 0.000 alpha 0.452 n   483 daniel_book
stop 0.056 mark 0.000 alpha 0.634 n   342 zechariah_book
stop 0.058 mark 0.000 alpha 0.622 n   328 hosea_book
stop 0.059 mark 0.356 alpha 0.735 n  3733 2_esdras
stop 0.112 mark 0.144 alpha 0.795 n   555 mn35_culasaccaka
stop 0.114 mark 0.220 alpha 0.748 n   422 aristotle_prior_analytics
stop 0.208 mark 0.000 alpha 0.926 n   827 book_of_enoch
stop 0.234 mark 0.000 alpha 0.905 n   788 qiwulun
stop 0.235 mark 0.010 alpha 0.909 n   600 mikolov_2013
stop 0.285 mark 0.000 alpha 0.937 n  1151 sibylline_oracles
stop 0.298 mark 0.003 alpha 0.891 n  1129 kleene_1936
--- best
stop 0.513 mark 0.002 alpha 0.965 n 10000 plato_phaedrus_jowett
stop 0.524 mark 0.002 alpha 0.953 n 10000 plato_gorgias
stop 0.524 mark 0.002 alpha 0.953 n 10000 plato_gorgias_jowett
stop 0.528 mark 0.005 alpha 0.964 n 10000 plato_phaedo
stop 0.538 mark 0.003 alpha 0.959 n 10000 plato_charmides
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport panini_334 as p\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\nfor t in ['jeremiah_book','isaiah_book','2_esdras','mn35_culasaccaka']:\n    s=(base/(t+'.txt')).r … [222 caractères tronqués]`

  ```
==== jeremiah_book
Jeremiah Back to book Jeremiah The archive, offline Own the Wisdom of the Ages Every text in the library on a single USB drive. Read offline, cite freely, keep forever. No subscription required. Get the drive $127.00 Jeremiah King James Version: Jeremiah Polyglot Sep | Tan | Vul Jeremiah Chapter 1 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 Jeremiah Chapter 2 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 Jeremiah Chapter 3 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 Jeremiah Chapter 4 1 2 3 4 5 6 7 8 9 10 11 12 1
...
 5 6 7 8 9 10 11 12 13 14 Jeremiah Chapter 22 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 Jeremiah Chapter 23 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 Jeremiah Chapter 24 1 2 3 4 5 6 7 8 9 10 Jeremiah Chapter 25 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 Jeremiah Chapter 26 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 Jeremiah Chapter 27 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 2
… [3695 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, re\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\nSTOP=set('the of and to in a is that it for as with … [1101 caractères tronqués]`

  ```
ok 28 of 44
OK  stop 0.285 mark 0.000 alpha 0.937 n  1151 sibylline_oracles
OK  stop 0.298 mark 0.003 alpha 0.891 n  1129 kleene_1936
OK  stop 0.336 mark 0.002 alpha 0.897 n 10000 schank_1972
OK  stop 0.366 mark 0.002 alpha 0.947 n 10000 quillian_1968
OK  stop 0.370 mark 0.002 alpha 0.914 n 10000 miller_evidence_prophecy
OK  stop 0.376 mark 0.001 alpha 0.913 n  8562 voluspa
OK  stop 0.399 mark 0.003 alpha 0.863 n 10000 curry_1930
OK  stop 0.412 mark 0.002 alpha 0.955 n 10000 russell_parousia_1878
OK  stop 0.432 mark 0.003 alpha 0.956 n 10000 nostradamus_centuries
OK  stop 0.433 mark 0.003 alpha 0.949 n 10000 dn1_brahmajala
OK  stop 0.461 mark 0.002 alpha 0.949 n 10000 aristotle_nicomachean_ethics
OK  stop 0.472 mark 0.001 alpha 0.955 n  2055 mn2_sabbasava
OK  stop 0.475 mark 0.004 alpha 0.964 n 10000 plato_laws
OK  stop 0.477 mark 0.004 alpha 0.952 n 10000 plato_republic_jowett
OK  stop 0.490 mark 0.008 alpha 0.969 n  7548 aristotle_parts_of_animals
OK  stop 0.493 mark 0.005 alpha 0.954 n 10000 plato_sophist
OK  stop 0.498 mark 0.013 alpha 0.967 n 10000 aristotle_de_caelo
OK  stop 0.498 mark 0.009 alpha 0.956 n 10000 plato_philebus_jowett
OK  stop 0.501 mark 0.004 alpha 0.961 n 100
… [1565 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\ns=open('../Panini/research/nipada/corpus/_cache/sources/plato_republic_jowett.txt','rb').read()\nprint('CR',s.count(b'\\r'),'LF',s.count(b'\\n'))\nprint(repr(s[1000:1200]))\nEOF", "description": "Check line endings"}`

  ```
CR 0 LF 0
b'YSIS MARGINAL ANALYSIS, AND INDEX_ BY B. JOWETT, M.A. MASTER OF BALLIOL COLLEGE REGIUS PROFESSOR OF GREEK IN THE UNIVERSITY OF OXFORD DOCTOR IN THEOLOGY OF THE UNIVERSITY OF LEYDEN THE THIRD EDITION _'
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\nrows=[]\nfor t in ids_signes:\n    s=(base/(t+'.txt')).read_bytes()\n    rows.append((s.count(b'\\n'),len(s), … [150 caractères tronqués]`

  ```
[(0, 1210, 'hosea_book'), (0, 1320, 'zechariah_book'), (0, 1666, 'mengzi'), (0, 1698, 'daniel_book'), (0, 3269, 'lukasiewicz_1920'), (0, 3784, 'mikolov_2013'), (0, 4487, 'qiwulun'), (0, 4811, 'ezekiel_book'), (0, 4989, 'isaiah_book'), (0, 5110, 'aristotle_prior_analytics'), (0, 5185, 'jeremiah_book'), (0, 5246, 'book_of_enoch'), (0, 6802, 'aristotle_posterior_analytics'), (0, 6817, 'kleene_1936'), (0, 7064, 'sibylline_oracles')]
zero LF 44 of 44
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport numpy as np, time\nrng=np.random.default_rng(0)\nn,p=44,14\nX=rng.normal(size=(n,p)); y=X[:,0]*0.5+rng.normal(size=n)\nlambdas=np.logspace(-2,3,20)\n\ndef cv_ridge(X,y,lambdas):\n    n=len(y); preds=np.empty … [801 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 23, in <module>
  File "<stdin>", line 18, in cv_ridge
ValueError: operands could not be broadcast together with shapes (1,43) (20,) 
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport numpy as np, time\nrng=np.random.default_rng(0)\nn,p=44,14\nX=rng.normal(size=(n,p)); y=X[:,0]*0.5+rng.normal(size=n)\nlambdas=np.logspace(-2,3,20)\n\ndef cv_ridge(X,y,lambdas):\n    n=len(y); preds=np.empty … [848 caractères tronqués]`

  ```
one 0.014381885528564453 -0.041989007847852644
100 1.2552950382232666
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\nprint('no year', [t for t in ids_signes if textes[t]['annee'] is None])\nprint('traditions', __import__('co … [186 caractères tronqués]`

  ```
no year []
traditions Counter({'GRECO': 19, 'ABRAHAMIC': 8, 'COGNITIVE_SCIENCE': 4, 'FORMAL_LOGIC': 3, 'BUDDHIST': 3, 'CHINESE': 2, 'MILLENARIAN': 2, 'RENAISSANCE_OCCULT': 1, 'CLASSICAL_ORACULAR': 1, 'NORSE_EDDIC': 1})
years [-750, -700, -600, -590, -520, -440, -430, -430, -390, -385, -385, -385, -385, -380, -380, -380, -370, -369, -360, -360, -350, -340, -340, -340, -340, -330, -330, -300, -300, -200, -200, -165, 100, 1000, 1555, 1836, 1878, 1920, 1930, 1936, 1968, 1972, 2003, 2013]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, hashlib, collections\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,sigs,_,textes,_,ids_signes,_=p.charger()\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\nh=collections.defaultdict(list … [414 caractères tronqués]`

  ```
dup text ['plato_gorgias', 'plato_gorgias_jowett']
dup text ['plato_meno', 'plato_meno_jowett']
dup sig ['plato_gorgias', 'plato_gorgias_jowett']
dup sig ['plato_meno', 'plato_meno_jowett']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, sys, html, subprocess, pathlib\nsys.path.insert(0,'tools')\nimport panini_334 as p\nfrom html.parser import HTMLParser\nclass _Strip(HTMLParser):\n    def __init__(self): super().__init__(); self.out=[]; … [2698 caractères tronqués]`

  ```
plato_republic_jowett        raw 1419135 clean 1396235 prose 1305827 words 235628 stop 0.94
    'THE REPUBLIC OF PLATO _JOWETT_ London HENRY FROWDE OXFORD UNIVERSITY PRESS WAREHOUSE AMEN CORNER, E.'
2_esdras                     raw  102937 clean   48128 prose    5149 words   759 stop 0.11
    "// Apply the local archive-bar preference before shared HTML can paint. mirror mode-watcher's setIni"
jeremiah_book                raw    5182 clean    5182 prose     302 words    50 stop 0.06
    'Jeremiah Back to book Jeremiah The archive, offline Own the Wisdom of the Ages Every text in the lib'
bengio_2003                  raw   63198 clean   38431 prose      21 words     7 stop 0.0
    'g a vcS 7EX 4ZQ ݱK G.'
aristotle_categories         raw  100859 clean   81865 prose   81422 words 14427 stop 0.99
    'HTML version by Al Haines. The Categories By Aristotle Translated by E. Edghill Section 1 Part 1 Thi'
mengzi                       raw    1664 clean    1492 prose    1492 words   270 stop 1.0
    "Mencius went to see king Hûi of Liang. The king said, 'Venerable sir, since you have not counted it "
qiwulun                      raw    4472 clean    4472 prose    3685 words   562 stop 0.82
 
… [105 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\nfor t in ids_signes:\n    if textes[t]['langue_source']=='fra': print(t)\nEOF", "description": "Find French … [9 caractères tronqués]`

  ```
nostradamus_centuries
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/tests/ | head; ls tools/tests/linguistique/ 2>/dev/null | head", "description": "Check tests layout"}`

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
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p work && cat > tools/atomes_prediction.py <<'PYEOF'\n#!/usr/bin/env python3\n\"\"\"B2 — les 14 atomes de Panini prédisent-ils les niveaux de Drave ?\n\nCe que le dispositif mesure\n---------------------------\n44 œuvres du §3 … [33134 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re\np='tools/atomes_prediction.py'\ns=open(p).read()\ns=s.replace('''    n_mots = 0\n    n_lettres = 0\n    n_ponct = 0\n    n_alpha_num = 0\n''','''    n_mots = 0\n    n_lettres = 0\n    n_ponct = 0\n    n_ … [1886 caractères tronqués]`

  ```
OK
277:    n_lettres = 0
351:                n_lettres += sum(1 for c in v if c.isalpha())
361:                n_lettres += 1
386:        "graph_lettres": n_lettres / max(1, n_lettres + n_ponct),
390:        "mot_longueur": n_lettres / n_mots_total,
418:        "att_part_gp": att_types.get("GP", 0) / total_att,
639:    "ATTACHEMENT": ["att_taux", "att_distance", "att_distance_mediane", "att_part_gp"],
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\ns=s.replace('''    n_mots = 0\n    n_lettres = 0\n    n_ponct = 0''','''    n_mots = 0\n    n_lettres_mots = 0\n    n_lettres_chars = 0\n    n_ponct = 0''')\ns=s.re … [801 caractères tronqués]`

  ```
OK
277:    n_lettres_mots = 0
278:    n_lettres_chars = 0
352:                n_lettres_mots += sum(1 for c in v if c.isalpha())
362:                n_lettres_chars += 1
387:        "graph_lettres": n_lettres_chars / max(1, n_lettres_chars + n_ponct),
391:        "mot_longueur": n_lettres_mots / n_mots_total,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, time, json\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nimport panini_334 as p\n_,_,_,_,textes,_,ids_signes,_=p.charger()\nbase=p.PANINI/'nipada'/'corpus'/'_cache'/'sources'\nfor t in [' … [477 caractères tronqués]`

  ```
aristotle_categories raw 81865 prose 81422 q {'n_jetons': 10000, 'stopwords': 0.5021, 'balises': 0.0036, 'lettres': 0.9613, 'propre': True} dt 1.91
{'n_fenetres': 6, 'n_mots': 10599, 'n_phrases': 411, 'n_syntagmes': 3469, 'n_attachements': 2202, 'n_attachements_cible': 2190, 'graph_lettres': 0.96, 'graph_ponctuation': 0.04, 'graph_entropie': 4.098, 'mot_longueur': 4.469, 'mot_ttr': 0.104, 'mot_hapax': 0.04, 'pos_entropie': 2.933, 'pos_part_nom': 0.311, 'pos_part_verbe': 0.191, 'pos_part_adj': 0.057, 'pos_part_adv': 0.032, 'pos_part_pron': 0.06, 'pos_part_det': 0.123, 'pos_part_prep': 0.141, 'pos_part_conj': 0.073, 'pos_part_num': 0.013, 'pos_ponct': 0.156, 'syn_par_phrase': 8.44, 'syn_longueur': 2.748, 'syn_part_gn': 0.227, 'syn_part_gv': 0.365, 'syn_part_gp': 0.287, 'syn_part_rel': 0.056, 'syn_part_sub': 0.065, 'syn_profondeur': 0.407, 'att_taux': 0.995, 'att_distance': 3.935, 'att_distance_mediane': 2.0, 'att_part_gp': 0.451, 'att_introuvable': 0.0, 'att_self': 0.005, 'phrase_longueur': 25.788, 'phrase_negation': 0.382, 'phrase_modalite': 0.243, 'phrase_interrogative': 0.0, 'pragma_assertion': 0.998, 'pragma_entropie': 0.025, 'disc_connecteurs_1000': 33.682, 'doc_paragraphes_1000
… [2401 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/atomes_prediction.py --mesurer --forcer 2>&1 | tail -50", "description": "Measure all 44 works", "timeoutMs": 600000}`

  ```
[ 7/44] aristotle_prior_analytics        mots=    57 propre=True syn=    0 (  7.9s)
  [ 8/44] bengio_2003                      mots=     0 propre=False syn=    0 (  7.9s)
  [ 9/44] book_of_enoch                    mots=   619 propre=True syn=  138 (  8.0s)
  [10/44] curry_1930                       mots= 18394 propre=True syn= 2736 (  9.5s)
  [11/44] daniel_book                      mots=   105 propre=False syn=    0 (  9.5s)
  [12/44] dn1_brahmajala                   mots= 12645 propre=True syn= 3141 ( 11.3s)
  [13/44] ezekiel_book                     mots=   174 propre=False syn=    0 ( 11.3s)
  [14/44] hosea_book                       mots=   106 propre=False syn=    0 ( 11.3s)
  [15/44] isaiah_book                      mots=   210 propre=False syn=   17 ( 11.3s)
  [16/44] jeremiah_book                    mots=   182 propre=False syn=    0 ( 11.3s)
  [17/44] kleene_1936                      mots=   807 propre=True syn=  219 ( 11.4s)
  [18/44] lukasiewicz_1920                 mots=   414 propre=True syn=   90 ( 11.4s)
  [19/44] mengzi                           mots=   269 propre=True syn=   96 ( 11.5s)
  [20/44] mikolov_2013                     mots=   484 propre=True syn=  138 (
… [3021 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\ns=s.replace('''        chemin = sources / f\"{tid}.txt\"\n        brut, meta = lire_source(chemin)\n        signature_q = qualite_fenetre_signature(brut)\n        p … [1714 caractères tronqués]`

  ```
OK
461:        signature_q["utilisable"] = bool(signature_q["propre"] and signature_q["assez_long"])
467:            mesures["n_mots_mesures"] = mesures.get("n_mots", 0)
490:        "source": str(panini.SIGNATURES),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/atomes_prediction.py --mesurer --forcer 2>&1 | tail -12", "description": "Rerun measurement with fixes", "timeoutMs": 300000}`

  ```
[34/44] plato_republic_jowett            mots=235643 propre=True syn= 3173 ( 49.0s)
  [35/44] plato_sophist                    mots= 10507 propre=True syn= 2322 ( 53.3s)
  [36/44] plato_symposium_jowett           mots= 19038 propre=True syn= 3637 ( 55.5s)
  [37/44] plato_theaetetus_jowett          mots= 64065 propre=True syn= 3358 ( 57.6s)
  [38/44] qiwulun                          mots=   553 propre=True syn=  117 ( 57.6s)
  [39/44] quillian_1968                    mots=  9999 propre=True syn= 2864 ( 59.3s)
  [40/44] russell_parousia_1878            mots= 83248 propre=True syn= 3180 ( 61.3s)
  [41/44] schank_1972                      mots=  9542 propre=True syn= 2265 ( 62.6s)
  [42/44] sibylline_oracles                mots=   934 propre=True syn=  270 ( 62.7s)
  [43/44] voluspa                          mots=  7341 propre=True syn= 1420 ( 64.8s)
  [44/44] zechariah_book                   mots=   106 propre=False syn=    0 ( 64.8s)
mesures : 44 œuvres → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/atomes-prediction-mesures.json
[stderr]

real	1m5,953s
user	1m8,830s
sys	0m0,344s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=d['oeuvres']\nprint('n',len(o))\nprint('mesurables',sum(1 for x in o if x['mesures']))\nprint('utilisable',sum(1 for x in o if x['qualite_ … [396 caractères tronqués]`

  ```
n 44
mesurables 36
utilisable 28
propre 34
2_esdras                         n= 3733 stop=0.059 bal=0.356 prop=False util=False mes=True mots=   769 an=100
aristotle_categories             n=10000 stop=0.501 bal=0.004 prop=True util=True mes=True mots= 14427 an=-340
aristotle_de_caelo               n=10000 stop=0.498 bal=0.013 prop=True util=True mes=True mots= 13485 an=-330
aristotle_nicomachean_ethics     n=10000 stop=0.461 bal=0.002 prop=True util=True mes=True mots=112419 an=-340
aristotle_parts_of_animals       n= 7548 stop=0.490 bal=0.008 prop=True util=True mes=True mots=  7544 an=-330
aristotle_posterior_analytics    n=  941 stop=0.319 bal=0.007 prop=True util=False mes=True mots=   639 an=-340
aristotle_prior_analytics        n=  422 stop=0.114 bal=0.220 prop=False util=False mes=False mots=    57 an=-340
bengio_2003                      n= 6607 stop=0.007 bal=0.087 prop=False util=False mes=False mots=     0 an=2003
book_of_enoch                    n=  827 stop=0.208 bal=0.000 prop=True util=False mes=True mots=   619 an=-200
curry_1930                       n=10000 stop=0.399 bal=0.003 prop=True util=True mes=True mots= 18394 an=1930
daniel_book                      n=  4
… [3759 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/atomes_prediction.py --analyser --rapide 2>&1 | tail -40", "description": "Run quick analysis on 36 works", "timeoutMs": 600000}`

  ```
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/atomes_prediction.py", line 807, in <module>
    main()
    ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/atomes_prediction.py", line 786, in main
    res = analyser(data, n_perm_col=n_col, n_perm_date=n_date)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/atomes_prediction.py", line 667, in analyser
    Y = np.array([[o["mesures"].get(k, np.nan) for k in noms] for o in sous], float)
ValueError: setting an array element with a sequence. The requested array has an inhomogeneous shape after 2 dimensions. The detected shape was (36, 48) + inhomogeneous part.
[stderr]

real	0m1,180s
user	0m4,214s
sys	0m0,121s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\ns=s.replace('''FAMILLES = {''','''METRIQUES = [\n    \"graph_lettres\", \"graph_ponctuation\", \"graph_entropie\",\n    \"mot_longueur\", \"mot_ttr\", \"mot_hapax\" … [1030 caractères tronqués]`

  ```
OK
680:    noms = [k for k in METRIQUES if all(k in o["mesures"] for o in sous)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/atomes_prediction.py --analyser --rapide", "description": "Run quick analysis (500 perms)", "timeoutMs": 900000, "run_in_background": true}`

  ```
started background job bash-73
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=d['oeuvres']\nfor label,cond in [\n ('mesurable',lambda x: bool(x['mesures'])),\n ('utilisable',lambda x: x['qualite_source']['utilisable' … [427 caractères tronqués]`

  ```
mesurable 36
   ['2_esdras', 'aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'book_of_enoch', 'curry_1930', 'dn1_brahmajala', 'isaiah_book', 'kleene_1936', 'lukasiewicz_1920', 'mengzi', 'mikolov_2013', 'miller_evidence_prophecy', 'mn2_sabbasava', 'nostradamus_centuries', 'plato_charmides', 'plato_gorgias', 'plato_gorgias_jowett', 'plato_laws', 'plato_meno', 'plato_meno_jowett', 'plato_phaedo', 'plato_phaedrus_jowett', 'plato_philebus_jowett', 'plato_republic_jowett', 'plato_sophist', 'plato_symposium_jowett', 'plato_theaetetus_jowett', 'qiwulun', 'quillian_1968', 'russell_parousia_1878', 'schank_1972', 'sibylline_oracles', 'voluspa']
utilisable 28
   ['aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'curry_1930', 'dn1_brahmajala', 'kleene_1936', 'miller_evidence_prophecy', 'mn2_sabbasava', 'nostradamus_centuries', 'plato_charmides', 'plato_gorgias', 'plato_gorgias_jowett', 'plato_laws', 'plato_meno', 'plato_meno_jowett', 'plato_phaedo', 'plato_phaedrus_jowett', 'plato_philebus_jowett', 'plato_republic_jowett', 'plato_sophist', 'plat
… [1244 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-73 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/atomes_prediction.py --analyser --rapide) finished [status: completed, exit code: 1]. Read its output with job_output.

- **job_output** `{"job_id": "bash-73"}`

  ```
CV atomes…
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/atomes_prediction.py", line 821, in <module>
    main()
    ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/atomes_prediction.py", line 800, in main
    res = analyser(data, n_perm_col=n_col, n_perm_date=n_date)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/atomes_prediction.py", line 696, in analyser
    _, r2_atomes, lam_atomes = cv_ridge_multi(X, Y, lambdas, groupes=groupes)
                               ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/atomes_prediction.py", line 587, in cv_ridge_multi
    F = f[:, None, :] * (U.T @ Yc)[None, :, :]
        ~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~
ValueError: operands could not be broadcast together with shapes (30,1,14) (1,14,38) 
[status: completed, exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\ns=s.replace('''        F = f[:, None, :] * (U.T @ Yc)[None, :, :]''','''        F = f[:, :, None] * (U.T @ Yc)[None, :, :]''')\nopen(p,'w').write(s)\nEOF\npython3 - … [97 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, numpy as np\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nrng=np.random.default_rng(0)\nn,p=30,6\nX=rng.normal(size=(n,p)); Y=np.column_stack([X[:,0]+rng.normal(size=n), X[:,1]*0.5+rng.no … [951 caractères tronqués]`

  ```
multi [ 0.38524918 -0.06312111] [ 4.2813324  26.36650899  4.2813324  14.38449888  4.2813324 ]
single 0 -0.03520590239231769
single 1 -0.06263149639334031
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, numpy as np\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nrng=np.random.default_rng(0)\nn,p=30,6\nX=rng.normal(size=(n,p)); y=X[:,0]+rng.normal(size=n)\nlambdas=np.logspace(-2,3,20)\npred … [759 caractères tronqués]`

  ```
multi [0.38524918]
loop -0.03520590239231769
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport numpy as np\nrng=np.random.default_rng(0)\nn,p=30,6\nX=rng.normal(size=(n,p)); y=X[:,0]+rng.normal(size=n)\nlambdas=np.logspace(-2,3,20)\ni=0\ntr=np.ones(n,bool); tr[i]=False\nXtr,ytr=X[tr],y[tr]\nmx=Xtr.mea … [791 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 16, in <module>
ValueError: operands could not be broadcast together with shapes (580,29) (20,29) 
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport numpy as np\nrng=np.random.default_rng(0)\nn,p=30,6\nX=rng.normal(size=(n,p)); y=X[:,0]+rng.normal(size=n)\nlambdas=np.logspace(-2,3,20)\ni=0\ntr=np.ones(n,bool); tr[i]=False\nXtr,ytr=X[tr],y[tr]\nmx=Xtr.mea … [675 caractères tronqués]`

  ```
multi lam 4.281332398719392 34.50384193556685
loop same lam 80.06031209979419
max diff yhat 1.9318436335360007
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport numpy as np\nrng=np.random.default_rng(0)\nn,p=30,6\nX=rng.normal(size=(n,p)); y=X[:,0]+rng.normal(size=n)\nlambdas=np.logspace(-2,3,20)\ni=0; tr=np.ones(n,bool); tr[i]=False\nXtr,ytr=X[tr],y[tr]\nmx=Xtr.mea … [597 caractères tronqués]`

  ```
0 0.0 [ 1.48365389 -2.24132048  0.7298496 ] [ 1.48365389 -2.24132048  0.7298496 ]
5 0.0 [ 1.47333296 -2.22540784  0.71914954] [ 1.47333296 -2.22540784  0.71914954]
19 0.0 [ 0.04467742 -0.07454342  0.00465978] [ 0.04467742 -0.07454342  0.00465978]
actual diff 0.0
F2 shape (20, 6, 1) yhat shape (20, 29)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport numpy as np\nrng=np.random.default_rng(0)\nn,p=30,6\nX=rng.normal(size=(n,p)); y=X[:,0]+rng.normal(size=n)\nlambdas=np.logspace(-2,3,20)\ni=0; tr=np.ones(n,bool); tr[i]=False\nXtr,ytr=X[tr],y[tr]\nmx=Xtr.mea … [898 caractères tronqués]`

  ```
la 4.281332398719392 h diff 0.0
argmin 10 4.281332398719392
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/atomes_prediction.py --analyser --rapide", "description": "Run quick analysis again", "timeoutMs": 900000, "run_in_background": true}`

  ```
started background job bash-82
  ```

- **bash** `{"command": "sleep 30; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l reports/atomes-prediction.json 2>/dev/null; ps aux | grep atomes_prediction | grep -v grep | head", "description": "Check analysis progress"}`

  ```
stephane 2959272  109  0.0 5760008 108704 ?      Rsl  03:18   0:37 python3 tools/atomes_prediction.py --analyser --rapide
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, numpy as np\nfrom scipy import stats\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if x['mesures']]\nprint('n',len(o))\nmetrics=['pos_entropie','syn_par_phras … [537 caractères tronqués]`

  ```
n 36
pos_entropie             mean 2.4970 sd 0.6588 min 0.7001 max 3.0065
syn_par_phrase           mean 6.7412 sd 2.0315 min 2.8333 max 11.3536
att_distance             mean 3.8460 sd 1.0454 min 2.5577 max 7.2723
att_taux                 mean 0.9949 sd 0.0058 min 0.9721 max 1.0000
mot_ttr                  mean 0.2289 sd 0.1044 min 0.1038 max 0.4951
phrase_longueur          mean 24.0257 sd 5.8128 min 11.1579 max 38.1321
disc_connecteurs_1000    mean 28.5234 sd 7.6541 min 4.7847 max 44.6097
year corr
pos_entropie             rho -0.484 p 0.0028
syn_par_phrase           rho -0.310 p 0.0656
att_distance             rho +0.073 p 0.6705
att_taux                 rho +0.241 p 0.1570
mot_ttr                  rho +0.610 p 0.0001
phrase_longueur          rho -0.322 p 0.0557
disc_connecteurs_1000    rho +0.055 p 0.7496
  ```

- **bash** `{"command": "sleep 60; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep atomes_prediction | grep -v grep | head; ls -l reports/atomes-prediction.json 2>/dev/null", "description": "Check analysis progress again"}`

  ```
[still running after 60000ms; moved to background job bash-85]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

### 👤 Utilisateur

background job bash-82 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/atomes_prediction.py --analyser --rapide) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-82"}`

  ```
CV atomes…
  CV date…
  CV joint…
  permutations colonnes (500)…
    200/500 ( 12.1s)
    400/500 ( 24.3s)
    date 200/500 ( 45.6s)
    date 400/500 ( 60.6s)
résultats → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/atomes-prediction.json
  POS          R²_atomes=+0.0687 p_col=0.0020 (Holm 0.0060) R²_date=-0.1794 Δ=+0.1633
  SYNTAGMES    R²_atomes=-0.0366 p_col=0.0180 (Holm 0.0359) R²_date=-0.1564 Δ=-0.1208
  ATTACHEMENT  R²_atomes=-0.2194 p_col=0.9661 (Holm 0.9661) R²_date=-0.1455 Δ=-0.5549
[stderr]
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/atomes_prediction.py:600: RuntimeWarning: invalid value encountered in divide
  r2 = 1 - ((Y - preds) ** 2).sum(0) / ((Y - Y.mean(0)) ** 2).sum(0)
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-85 (bash: sleep 60; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep atomes_prediction | grep -v grep | head; ls -l reports/atomes-prediction.json 2>/dev/null) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-prediction.json'))\nm=d['metriques']\nrows=sorted(m.items(), key=lambda kv: kv[1]['p_col'])\nfor k,v in rows:\n    print(f\"{k:<26} {v['famille']:<12} r2A {v['r2_atomes … [268 caractères tronqués]`

  ```
pos_part_verbe             POS          r2A +0.7029 pC 0.0020 bh 0.0253 r2D -0.2740 dJD +0.9505 pJD 0.0838
pos_part_num               POS          r2A +0.1866 pC 0.0020 bh 0.0253 r2D -0.4002 dJD +0.5395 pJD 0.0918
att_introuvable            autre        r2A +nan pC 0.0020 bh 0.0253 r2D +nan dJD +nan pJD 0.0020
pos_part_pron              POS          r2A +0.2100 pC 0.0040 bh 0.0303 r2D -0.0434 dJD +0.2567 pJD 0.5170
phrase_negation            autre        r2A +0.4063 pC 0.0040 bh 0.0303 r2D +0.1959 dJD +0.2285 pJD 0.9920
phrase_modalite            autre        r2A +0.2570 pC 0.0060 bh 0.0379 r2D -0.1604 dJD +0.2039 pJD 0.8942
pos_part_adv               POS          r2A +0.1976 pC 0.0100 bh 0.0506 r2D -0.1855 dJD +0.2118 pJD 0.7246
mot_longueur               autre        r2A +0.1443 pC 0.0120 bh 0.0506 r2D -0.1301 dJD +0.5780 pJD 0.0259
syn_part_gn                SYNTAGMES    r2A +0.1134 pC 0.0120 bh 0.0506 r2D -0.2438 dJD +0.0007 pJD 0.7345
graph_ponctuation          autre        r2A +0.0290 pC 0.0160 bh 0.0552 r2D +0.0201 dJD -0.5832 pJD 0.9980
syn_part_rel               SYNTAGMES    r2A +0.0976 pC 0.0160 bh 0.0552 r2D -0.1284 dJD +0.4804 pJD 0.0160
syn_part_sub               SYNTA
… [4007 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, numpy as np\nfrom scipy import stats\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if x['mesures']]\natomes=d['atomes']\ny=np.array([x['mesures']['pos_part_ve … [602 caractères tronqués]`

  ```
year rho SignificanceResult(statistic=np.float64(-0.5596163452831248), pvalue=np.float64(0.0003873631856702078))
ÊTRE         rho +0.847 p 0.0000
DIFFÉRENCE   rho +0.754 p 0.0000
RAPPORT      rho -0.686 p 0.0000
ORIENTATION  rho +0.413 p 0.0122
SUJET        rho +0.087 p 0.6127
TEMPS        rho -0.041 p 0.8115
MODALITÉ     rho +0.411 p 0.0128
NOMBRE       rho -0.084 p 0.6275
ESPACE       rho +0.604 p 0.0001
OPÉRATION    rho -0.061 p 0.7259
FONCTION     rho -0.487 p 0.0026
STRUCTURE    rho -0.627 p 0.0000
SYMÉTRIE     rho +0.577 p 0.0002
ÉQUATION     rho -0.065 p 0.7058
top verb works
plato_gorgias 0.206 -385 True
plato_gorgias_jowett 0.206 -380 True
plato_phaedo 0.207 -380 True
mengzi 0.212 -300 True
plato_meno 0.212 -385 True
plato_meno_jowett 0.212 -385 True
mn2_sabbasava 0.216 -430 True
plato_charmides 0.22 -390 True
bottom
isaiah_book 0.006 -700 False
qiwulun 0.062 -300 True
book_of_enoch 0.083 -200 True
2_esdras 0.093 100 False
kleene_1936 0.122 1936 True
schank_1972 0.123 1972 True
mikolov_2013 0.123 2013 True
lukasiewicz_1920 0.124 1920 True
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, numpy as np\nfrom scipy import stats\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if x['mesures']]\natomes=d['atomes']\ndef rank(a): return stats.rankdata(a) … [911 caractères tronqués]`

  ```
=== cohort 36 36
ÊTRE         rho +0.847 p 0.0000 | partiel +0.718 p 0.0000
DIFFÉRENCE   rho +0.754 p 0.0000 | partiel +0.589 p 0.0002
RAPPORT      rho -0.686 p 0.0000 | partiel -0.526 p 0.0010
STRUCTURE    rho -0.627 p 0.0000 | partiel -0.239 p 0.1603
ESPACE       rho +0.604 p 0.0001 | partiel +0.681 p 0.0000
SYMÉTRIE     rho +0.577 p 0.0002 | partiel +0.458 p 0.0050
=== cohort 28 28
ÊTRE         rho +0.710 p 0.0000 | partiel +0.480 p 0.0098
DIFFÉRENCE   rho +0.596 p 0.0008 | partiel +0.311 p 0.1076
RAPPORT      rho -0.494 p 0.0075 | partiel -0.211 p 0.2810
STRUCTURE    rho -0.552 p 0.0023 | partiel +0.049 p 0.8044
ESPACE       rho +0.286 p 0.1403 | partiel +0.422 p 0.0254
SYMÉTRIE     rho +0.409 p 0.0306 | partiel +0.317 p 0.1006
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, numpy as np\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if x['mesures']]\ny=np.array([[x['m … [400 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
TypeError: _design_date() takes 1 positional argument but 2 were given
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\ns=s.replace('''def _design_date(annees: np.ndarray) -> np.ndarray:\n    z = (annees - np.nanmean(annees)) / (np.nanstd(annees) or 1)\n    return np.column_stack([np … [452 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, numpy as np\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if x['mesures']]\nks=['pos_entropie … [423 caractères tronqués]`

  ```
deg 1 {'pos_entropie': np.float64(-0.1018), 'syn_par_phrase': np.float64(-0.0478), 'att_distance': np.float64(-0.1584), 'pos_part_verbe': np.float64(-0.0468), 'mot_ttr': np.float64(0.1363)}
deg 2 {'pos_entropie': np.float64(-0.3803), 'syn_par_phrase': np.float64(-0.2381), 'att_distance': np.float64(-0.2842), 'pos_part_verbe': np.float64(-0.2652), 'mot_ttr': np.float64(-0.0005)}
deg 3 {'pos_entropie': np.float64(-0.1902), 'syn_par_phrase': np.float64(-0.9075), 'att_distance': np.float64(-1.0412), 'pos_part_verbe': np.float64(-1.6057), 'mot_ttr': np.float64(-0.5537)}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, numpy as np\nfrom scipy import stats\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if x['mesu … [919 caractères tronqués]`

  ```
year {'pos_entropie': np.float64(-0.1018), 'syn_par_phrase': np.float64(-0.0478), 'att_distance': np.float64(-0.1584), 'pos_part_verbe': np.float64(-0.0468), 'mot_ttr': np.float64(0.1363)}
rank {'pos_entropie': np.float64(-0.1114), 'syn_par_phrase': np.float64(-0.0328), 'att_distance': np.float64(-0.1707), 'pos_part_verbe': np.float64(-0.0355), 'mot_ttr': np.float64(0.235)}
ancien {'pos_entropie': np.float64(-0.751), 'syn_par_phrase': np.float64(-0.0451), 'att_distance': np.float64(-0.2518), 'pos_part_verbe': np.float64(-0.2233), 'mot_ttr': np.float64(-0.1542)}
rank2 {'pos_entropie': np.float64(-0.2516), 'syn_par_phrase': np.float64(-0.0824), 'att_distance': np.float64(-0.2546), 'pos_part_verbe': np.float64(-0.1444), 'mot_ttr': np.float64(0.1825)}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^def analyser\\|^def main\\|^FAMILLES\\|^PRIMAIRES\\|^METRIQUES\" tools/atomes_prediction.py", "description": "Locate analyser function bounds"}`

  ```
648:METRIQUES = [
662:FAMILLES = {
670:PRIMAIRES = list(FAMILLES)
673:def analyser(data: dict, n_perm_col: int = 2000, n_perm_date: int = 1000) -> dict:
788:def main(argv=None):
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '673,790p' tools/atomes_prediction.py", "description": "Read current analyser for replacement"}`

  ```
def analyser(data: dict, n_perm_col: int = 2000, n_perm_date: int = 1000) -> dict:
    oeuvres = data["oeuvres"]
    # garde les œuvres mesurables (au moins 200 mots de prose et des mesures)
    idx = [i for i, o in enumerate(oeuvres) if o.get("mesures")
           and np.isfinite(o["mesures"].get("pos_entropie", np.nan))]
    sous = [oeuvres[i] for i in idx]
    n = len(sous)
    X = clr(np.array([o["signature"] for o in sous], float))
    annees = np.array([o["annee"] for o in sous], float)
    D = _design_date(annees)
    noms = [k for k in METRIQUES if all(k in o["mesures"] for o in sous)]
    Y = np.array([[o["mesures"].get(k, np.nan) for k in noms] for o in sous], float)
    # remplace les NaN par la moyenne de la colonne (peu de cas) et note-le
    nan_par_metrique = {k: int(np.sum(~np.isfinite(Y[:, j]))) for j, k in enumerate(noms)}
    for j in range(Y.shape[1]):
        col = Y[:, j]
        if np.any(~np.isfinite(col)):
            col[~np.isfinite(col)] = np.nanmean(col)
            Y[:, j] = col

    groupes = _groupes(sous)
    lambdas = np.logspace(-2, 3, 30)
    rng = np.random.default_rng(GRAINE)

    # observé
    print("  CV atomes…", flush=True)
    _, r2_atomes
… [4209 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\nstart=s.index('def analyser(data: dict')\nend=s.index('def main(argv=None):')\nnew='''def _filtre_cohorte(o: dict, cohorte: str) -> bool:\n    \"\"\"Cohortes pré-dé … [9385 caractères tronqués]`

  ```
OK
705:def cv_residuel(X, Y, D, lambdas, groupes):
719:def analyser(data: dict, cohorte: str = "mesurable", n_perm_col: int = 2000,
865:def main(argv=None):
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '865,940p' tools/atomes_prediction.py", "description": "Read main"}`

  ```
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mesurer", action="store_true")
    ap.add_argument("--analyser", action="store_true")
    ap.add_argument("--tout", action="store_true")
    ap.add_argument("--forcer", action="store_true")
    ap.add_argument("--rapide", action="store_true", help="500 permutations")
    args = ap.parse_args(argv)
    if args.tout or args.mesurer:
        data = charger_donnees(forcer=args.forcer)
        print(f"mesures : {len(data['oeuvres'])} œuvres → {SORTIE_MESURES}")
    if args.tout or args.analyser:
        data = charger_donnees()
        n_col = 500 if args.rapide else 2000
        n_date = 500 if args.rapide else 1000
        res = analyser(data, n_perm_col=n_col, n_perm_date=n_date)
        res.update({
            "fiche": "reports/rapport-atomes-prediction.md",
            "version": "1.0",
            "date": "2026-11-15",
            "titre": "Les 14 atomes de Panini prédisent-ils les niveaux de Drave ?",
            "statut": "mesure",
            "source": data["source"],
            "atomes": data["atomes"],
            "oeuvres": data["oeuvres"],
        })
        SORTIE.write_text
… [438 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\nstart=s.index('def main(argv=None):')\nnew='''def main(argv=None):\n    ap = argparse.ArgumentParser(description=__doc__)\n    ap.add_argument(\"--mesurer\", action … [3521 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/atomes_prediction.py --analyser --rapide --cohorte utilisable 2>&1 | tail -20", "description": "Quick analysis on clean 28", "timeoutMs": 600000}`

  ```
=== cohorte utilisable (colonnes=500, date=500, degré date=1)
  [utilisable] n=28 : CV atomes…
  [utilisable] : date in-sample + atomes sur résidus…
  [utilisable] permutations colonnes (500)…
    200/500 ( 13.4s)
    400/500 ( 26.5s)
  [utilisable] permutations date (500)…
    date 200/500 ( 46.4s)
    date 400/500 ( 60.0s)
résultats → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/atomes-prediction.json
-- utilisable_d1 (n=28)
  POS          R²A=-0.1491 pC=0.2954 rhoA=-0.0313 pR=0.0479 R²date=+0.1630 R²res=-0.5516 pRes=1.0000
  SYNTAGMES    R²A=-0.2133 pC=0.7146 rhoA=-0.3952 pR=0.3413 R²date=+0.0579 R²res=-0.4659 pRes=0.9940
  ATTACHEMENT  R²A=-0.1851 pC=0.6547 rhoA=-0.3191 pR=0.2655 R²date=+0.0487 R²res=-0.2940 pRes=0.8982
[stderr]

real	1m8,002s
user	1m11,105s
sys	0m0,116s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-prediction.json'))\nm=d['metriques']\nrows=sorted(m.items(), key=lambda kv: kv[1]['p_col'])\nfor k,v in rows:\n    print(f\"{k:<26} {v['famille']:<12} r2A {v['r2_atomes … [219 caractères tronqués]`

  ```
graph_entropie             autre        r2A +0.7809 pC 0.0020 rho +0.787 pRho 0.0020 r2date +0.2164 r2res +0.7715 pRes 0.8703
mot_longueur               autre        r2A +0.6042 pC 0.0020 rho +0.696 pRho 0.0020 r2date +0.3925 r2res +0.0559 pRes 1.0000
phrase_negation            autre        r2A +0.4990 pC 0.0020 rho +0.758 pRho 0.0020 r2date +0.5380 r2res +0.5977 pRes 0.4351
pos_part_verbe             POS          r2A +0.3885 pC 0.0040 rho +0.532 pRho 0.0080 r2date +0.3693 r2res -0.0399 pRes 0.9960
pragma_entropie            autre        r2A +0.3150 pC 0.0060 rho +0.506 pRho 0.0120 r2date +0.1590 r2res +0.1205 pRes 0.8862
pos_part_pron              POS          r2A +0.1416 pC 0.0140 rho +0.464 pRho 0.0120 r2date +0.2207 r2res -0.0076 pRes 0.9681
mot_ttr                    autre        r2A +0.1581 pC 0.0160 rho +0.463 pRho 0.0120 r2date +0.5354 r2res -0.4145 pRes 0.9960
phrase_interrogative       autre        r2A +0.1964 pC 0.0160 rho +0.455 pRho 0.0140 r2date +0.2584 r2res -0.0742 pRes 1.0000
pragma_assertion           autre        r2A +0.1356 pC 0.0259 rho +0.443 pRho 0.0200 r2date +0.1907 r2res -0.0379 pRes 0.9760
pos_part_adj               POS          r2A -0.0807 pC 0.0838 rho 
… [3461 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, numpy as np\nd=json.load(open('reports/atomes-prediction.json'))\nnoms=d['noms']\nfor k in ['graph_entropie','mot_longueur','pos_part_verbe','phrase_negation']:\n    j=noms.index(k)\n    print(k)\n     … [446 caractères tronqués]`

  ```
graph_entropie
 obs r2A 0.7809 null col mean -0.2037 p95 -0.0253
 obs r2res 0.7715 null res mean 0.8022 p95 0.8579
 obs date 0.2164 null date mean 0.0387 p95 0.1423
mot_longueur
 obs r2A 0.6042 null col mean -0.199 p95 0.0033
 obs r2res 0.0559 null res mean 0.6247 p95 0.695
 obs date 0.3925 null date mean 0.0397 p95 0.1409
pos_part_verbe
 obs r2A 0.3885 null col mean -0.2026 p95 -0.0509
 obs r2res -0.0399 null res mean 0.3877 p95 0.46
 obs date 0.3693 null date mean 0.0384 p95 0.1486
phrase_negation
 obs r2A 0.499 null col mean -0.2074 p95 -0.0266
 obs r2res 0.5977 null res mean 0.5865 p95 0.7236
 obs date 0.538 null date mean 0.0376 p95 0.1331
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, numpy as np\nfrom scipy import stats\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if x['mesu … [966 caractères tronqués]`

  ```
n 28
POS          PC1 var 0.56 r2 -0.171 rho +0.016 r2res -0.649
  loadings {'pos_entropie': np.float64(0.4), 'pos_part_nom': np.float64(-0.4), 'pos_part_verbe': np.float64(0.11), 'pos_part_adj': np.float64(0.21), 'pos_part_adv': np.float64(0.34), 'pos_part_pron': np.float64(0.32), 'pos_part_det': np.float64(0.36), 'pos_part_prep': np.float64(0.36), 'pos_part_conj': np.float64(0.38), 'pos_part_num': np.float64(0.06), 'pos_ponct': np.float64(-0.05)}
SYNTAGMES    PC1 var 0.64 r2 -0.137 rho -0.571 r2res -0.722
  loadings {'syn_par_phrase': np.float64(0.24), 'syn_longueur': np.float64(-0.36), 'syn_part_gn': np.float64(0.36), 'syn_part_gv': np.float64(-0.43), 'syn_part_gp': np.float64(0.43), 'syn_part_rel': np.float64(0.35), 'syn_part_sub': np.float64(-0.35), 'syn_profondeur': np.float64(0.27)}
ATTACHEMENT  PC1 var 0.41 r2 -0.072 rho +0.120 r2res -0.083
  loadings {'att_taux': np.float64(0.53), 'att_distance': np.float64(0.54), 'att_distance_mediane': np.float64(0.22), 'att_part_gp': np.float64(0.62)}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/atomes_cohortes.py <<'EOF'\nimport sys, json, numpy as np\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nd=json.load(open('reports/atomes-prediction-mesures.json'))\n# ajoute une cohorte \"propre\" au filtre\ … [1012 caractères tronqués]`

  ```
started background job bash-102
  ```

- **bash** `{"command": "sleep 60; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep atomes_cohortes | grep -v grep | head", "description": "Check cohort job progress"}`

  ```
[still running after 60000ms; moved to background job bash-103]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l work/atomes_cohortes.py; ps aux | grep atomes_cohortes | grep -v grep | head", "description": "Check cohort job still running"}`

  ```
-rw-r--r--. 1 stephane stephane 1040 15 nov 03:23 work/atomes_cohortes.py
stephane 2961177  104  0.0 5757908 107516 ?      Rsl  03:23   1:17 python3 work/atomes_cohortes.py
  ```

### 👤 Utilisateur

background job bash-103 (bash: sleep 60; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep atomes_cohortes | grep -v grep | head) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-102"}`

  ```
[mesurable] n=36 : CV atomes…
  [mesurable] : date in-sample + atomes sur résidus…
  [mesurable] permutations colonnes (300)…
    200/300 ( 17.2s)
  [mesurable] permutations date (300)…
    date 200/300 ( 42.1s)
### mesurable n=36
  POS          R2A=+0.069 pC=0.003 rho=+0.174 pRho=0.007 date=+0.065 R2res=+0.110 pRes=0.419
  SYNTAGMES    R2A=-0.037 pC=0.010 rho=+0.203 pRho=0.003 date=+0.035 R2res=+0.023 pRes=0.090
  ATTACHEMENT  R2A=-0.219 pC=0.960 rho=+0.098 pRho=0.010 date=+0.026 R2res=-0.423 pRes=0.997
  [propre] n=34 : CV atomes…
  [propre] : date in-sample + atomes sur résidus…
  [propre] permutations colonnes (300)…
    200/300 ( 15.6s)
  [propre] permutations date (300)…
[status: running]
  ```

- **bash** `{"command": "sleep 90; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep atomes_cohortes | grep -v grep | head", "description": "Wait for cohort job"}`

  ```
[still running after 60000ms; moved to background job bash-105]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-102"}`

  ```
date 200/300 ( 39.2s)
### propre n=34
  POS          R2A=-0.023 pC=0.017 rho=+0.042 pRho=0.013 date=+0.103 R2res=-0.108 pRes=0.993
  SYNTAGMES    R2A=-0.015 pC=0.013 rho=+0.095 pRho=0.007 date=+0.053 R2res=-0.074 pRes=0.877
  ATTACHEMENT  R2A=-0.098 pC=0.362 rho=+0.020 pRho=0.023 date=+0.030 R2res=-0.164 pRes=0.970
  [propre_500] n=31 : CV atomes…
  [propre_500] : date in-sample + atomes sur résidus…
  [propre_500] permutations colonnes (300)…
    200/300 ( 14.2s)
  [propre_500] permutations date (300)…
    date 200/300 ( 35.6s)
### propre_500 n=31
  POS          R2A=-0.028 pC=0.017 rho=+0.020 pRho=0.020 date=+0.095 R2res=-0.122 pRes=0.973
  SYNTAGMES    R2A=-0.139 pC=0.502 rho=-0.020 pRho=0.027 date=+0.032 R2res=-0.139 pRes=0.502
  ATTACHEMENT  R2A=-0.180 pC=0.834 rho=+0.110 pRho=0.010 date=+0.036 R2res=-0.057 pRes=0.023
  [utilisable] n=28 : CV atomes…
  [utilisable] : date in-sample + atomes sur résidus…
  [utilisable] permutations colonnes (300)…
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, numpy as np\nfrom scipy import stats\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if x['mesu … [673 caractères tronqués]`

  ```
null rho mean -0.47212429910250464 sd 0.5045129287020147 min -0.9635916046784696 max 0.7656720790584317
obs rho 0.5323110624315445
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, numpy as np\nfrom scipy import stats\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if x['mesu … [549 caractères tronqués]`

  ```
random r2 -0.21196036723190526 rho -0.8787298440391726
pred first [0.17746015 0.17707716 0.1790962  0.17880895 0.17928673] y first [0.1913109  0.19482567 0.16073425 0.16897655 0.14175754]
atoms r2 0.3885256128876109 rho 0.5323110624315445
pred first [0.18785325 0.18083803 0.18425858 0.18413585 0.14723397] y first [0.1913109  0.19482567 0.16073425 0.16897655 0.14175754]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\ns=s.replace('''            Xtr_s, Xte_s, mx, sx = _standardiser(Xtr_r, Xte_r)\n            my = Ytr_r.mean(0)\n            Yc = Ytr_r - my\n        else:\n          … [1800 caractères tronqués]`

  ```
OK
random r2 -0.11596820685919518 rho -0.11880646489501585
pred sd 0.0030657291171899566 pred first [0.17795318 0.17770036 0.17845676 0.17847478 0.17794444]
atoms r2 0.43101091848977724 rho 0.599671412924425
pred sd 0.017990965430495373 pred first [0.18834628 0.18146124 0.18361914 0.18380168 0.14589168]
null rho mean -0.09716397845584547 sd 0.2597500655780299
  ```

### 👤 Utilisateur

background job bash-105 (bash: sleep 90; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep atomes_cohortes | grep -v grep | head) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\ns=s.replace('''    if cohorte == \"utilisable\":\n        return bool(q.get(\"utilisable\"))\n    if cohorte == \"strict\":''','''    if cohorte == \"utilisable\":\ … [2951 caractères tronqués]`

  ```
OK
201:                "propre": False}
211:        "propre": bool(stop >= 0.15 and balises <= 0.05 and lettres >= 0.75),
461:        signature_q["utilisable"] = bool(signature_q["propre"] and signature_q["assez_long"])
484:              f"propre={signature_q['propre']} syn={mesures.get('n_syntagmes', 0):5d} "
688:    if cohorte == "propre":
689:        return bool(q.get("propre"))
690:    if cohorte == "propre_500":
691:        return bool(q.get("propre")) and o["mesures"].get("n_mots_mesures", 0) >= 500
804:            "r2_exces": round(float(r2_atomes[j] - np.nanmean(null_col[:, j])), 4),
806:            "rho_exces": round(float(rho_atomes[j] - np.nanmean(null_col_rho[:, j])), 4),
844:            "r2_exces_moyen": round(obs - float(np.nanmean(null)), 4),
847:            "rho_exces_moyen": round(obs_rho - float(np.nanmean(null_rho)), 4),
899:                    ("propre", max(300, n_col // 4), max(300, n_date // 4), 1),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/atomes_prediction.py --analyser --cohorte utilisable --rapide 2>&1 | tail -12", "description": "Quick primary on clean 28 after centering fix", "timeoutMs": 600000}`

  ```
[utilisable] : date in-sample + atomes sur résidus…
  [utilisable] permutations colonnes (500)…
    200/500 ( 13.4s)
    400/500 ( 26.7s)
  [utilisable] permutations date (500)…
    date 200/500 ( 46.7s)
    date 400/500 ( 60.2s)
résultats → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/atomes-prediction.json
-- utilisable_d1 (n=28)
  POS          R²A=-0.0729 pC=0.3373 rhoA=+0.1782 pR=0.0379 R²date=+0.1630 R²res=-0.4650 pRes=1.0000
  SYNTAGMES    R²A=-0.1387 pC=0.7305 rhoA=+0.0005 pR=0.2575 R²date=+0.0579 R²res=-0.3840 pRes=0.9920
  ATTACHEMENT  R²A=-0.1049 pC=0.6467 rhoA=-0.0744 pR=0.4291 R²date=+0.0487 R²res=-0.2151 pRes=0.9182
  ```

### 👤 Utilisateur

background job bash-102 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/atomes_cohortes.py <<'EOF'
import sys, json, numpy as np
sys.path.insert(0,'tools')
import atomes_prediction as ap
d=json.load(open('reports/atomes-prediction-mesures.json'))
# ajoute une cohorte "propre" au filtre
orig=ap._filtre_cohorte
def filtre(o,c):
    if c=='propre':
        return bool(o.get('mesures')) and bool(o['qualite_source'].get('propre')) and np.isfinite(o['mesures'].get('pos_entropie',np.nan))
    if c=='propre_500':
        return filtre(o,'propre') and o['mesures'].get('n_mots_mesures',0)>=500
    return orig(o,c)
ap._filtre_cohorte=filtre
for c in ['mesurable','propre','propre_500','utilisable','strict','strict_plus']:
    r=ap.analyser(d,cohorte=c,n_perm_col=300,n_perm_date=300)
    print(f"### {c} n={r['n']}")
    for f in ap.PRIMAIRES:
        if f not in r['familles']: continue
        x=r['familles'][f]
        print(f"  {f:<12} R2A={x['r2_atomes_moyen']:+.3f} pC={x['p_col']:.3f} rho={x['rho_cv_moyen']:+.3f} pRho={x['p_rho_col']:.3f} date={x['r2_date_in_moyen']:+.3f} R2res={x['r2_resid_moyen']:+.3f} pRes={x['p_resid']:.3f}")
EOF
python3 work/atomes_cohortes.py) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-prediction.json'))\nm=d['metriques']\nrows=sorted(m.items(), key=lambda kv: kv[1]['p_col'])\nfor k,v in rows[:18]:\n    print(f\"{k:<26} {v['famille']:<12} r2A {v['r2_a … [456 caractères tronqués]`

  ```
graph_entropie             autre        r2A +0.7913 pC 0.0020 exc +0.915 rho +0.809 pRho 0.0020 date +0.216 pRes 0.8982
mot_longueur               autre        r2A +0.6543 pC 0.0020 exc +0.759 rho +0.726 pRho 0.0020 date +0.393 pRes 1.0000
phrase_negation            autre        r2A +0.5319 pC 0.0020 exc +0.647 rho +0.782 pRho 0.0020 date +0.538 pRes 0.3932
pos_part_verbe             POS          r2A +0.4310 pC 0.0040 exc +0.539 rho +0.600 pRho 0.0040 date +0.369 pRes 0.9960
pragma_entropie            autre        r2A +0.3600 pC 0.0060 exc +0.464 rho +0.551 pRho 0.0120 date +0.159 pRes 0.9202
pos_part_pron              POS          r2A +0.2320 pC 0.0080 exc +0.338 rho +0.516 pRho 0.0120 date +0.221 pRes 0.9621
mot_ttr                    autre        r2A +0.2132 pC 0.0160 exc +0.322 rho +0.508 pRho 0.0160 date +0.535 pRes 0.9960
phrase_interrogative       autre        r2A +0.2659 pC 0.0160 exc +0.367 rho +0.518 pRho 0.0100 date +0.258 pRes 1.0000
pragma_assertion           autre        r2A +0.2113 pC 0.0220 exc +0.312 rho +0.507 pRho 0.0180 date +0.191 pRes 0.9940
phrase_modalite            autre        r2A +0.0241 pC 0.0838 exc +0.122 rho +0.358 pRho 0.0798 date +0.515 pRes 1.0000

… [1847 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\ns=s.replace('''    return {\n        \"cohorte\": cohorte,\n        \"n\": n,\n        \"metriques\": metriques,''','''    # descriptif des atomes : date, colinéari … [883 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/atomes_prediction.py --analyser", "description": "Run final full analysis (primary 28, 2000 perms)", "timeoutMs": 1800000, "run_in_background": true}`

  ```
started background job bash-113
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, numpy as np\nfrom scipy import stats\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=d['oeuvres']; A=d['atomes']\nan=np.array([x['annee'] for x in o],float)\nprint('n',len(o),'years',an … [458 caractères tronqués]`

  ```
n 44 years -750.0 2013.0 median -340.0
pre-1000 33 post-1500 10
traditions {'ABRAHAMIC': 8, 'BUDDHIST': 3, 'CHINESE': 2, 'CLASSICAL_ORACULAR': 1, 'COGNITIVE_SCIENCE': 4, 'FORMAL_LOGIC': 3, 'GRECO': 19, 'MILLENARIAN': 2, 'NORSE_EDDIC': 1, 'RENAISSANCE_OCCULT': 1}
ÊTRE         rho_date -0.089 p 0.5666
DIFFÉRENCE   rho_date -0.097 p 0.5321
RAPPORT      rho_date +0.012 p 0.9364
ORIENTATION  rho_date +0.243 p 0.1125
SUJET        rho_date -0.447 p 0.0023
TEMPS        rho_date -0.348 p 0.0205
MODALITÉ     rho_date -0.017 p 0.9115
NOMBRE       rho_date +0.067 p 0.6667
ESPACE       rho_date +0.266 p 0.0810
OPÉRATION    rho_date +0.315 p 0.0376
FONCTION     rho_date -0.021 p 0.8935
STRUCTURE    rho_date +0.201 p 0.1915
SYMÉTRIE     rho_date -0.171 p 0.2683
ÉQUATION     rho_date +0.332 p 0.0276
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, numpy as np\nfrom scipy import stats\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if x['mesures'] and x['qualite_source']['utilisable']]\nA=d['atomes']; an=n … [346 caractères tronqués]`

  ```
n 28 unique texts 26
ÊTRE         rho_date -0.633 p 0.0003
DIFFÉRENCE   rho_date -0.545 p 0.0027
RAPPORT      rho_date +0.504 p 0.0063
ORIENTATION  rho_date +0.127 p 0.5190
SUJET        rho_date -0.256 p 0.1893
TEMPS        rho_date -0.234 p 0.2309
MODALITÉ     rho_date -0.311 p 0.1075
NOMBRE       rho_date -0.228 p 0.2435
ESPACE       rho_date +0.019 p 0.9255
OPÉRATION    rho_date +0.228 p 0.2441
FONCTION     rho_date +0.447 p 0.0172
STRUCTURE    rho_date +0.728 p 0.0000
SYMÉTRIE     rho_date -0.343 p 0.0743
ÉQUATION     rho_date -0.045 p 0.8207
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; ls -l reports/atomes-prediction.json", "description": "Check final analysis progress"}`

  ```
stephane 2963235  116  0.0 5760984 110404 ?      Rsl  03:27   0:22 python3 tools/atomes_prediction.py --analyser
-rw-r--r--. 1 stephane stephane 164327 15 nov 03:27 reports/atomes-prediction.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"gold\\|POS\\|attachement\\|syntagme\\|F1\" reports/rapport-bloc-linguistique.md | head -40", "description": "Find heuristic accuracy figures"}`

  ```
7:> **0,0022**). ⚠️ **les niveaux profonds n'ont pas de gold** et le **modèle neuronal réel n'est
28:- **neuf niveaux** : graphème, morphème, mot, pos, syntagme, phrase, discours, pragmatique,
37:- **les compositions** : `Parallele` (fusion par niveau/span/source, syntagme heuristique
75:| syntagme | 0,40 | 0,78 | GN/GV/GP/REL/SUB, rôles, attachements candidats |
82:confiances basses sont **assumées** : le morphème, le syntagme et la pragmatique sont des
92:  **sauf le syntagme**, où la segmentation heuristique (le générateur de la coloration) est
94:- **cascade** : l'heuristique d'abord ; si `morphème`, `pos`, `syntagme`, `discours` ou
99:syntagmes du générateur S (GN « Le chat », GP « de la voisine », REL « qui dort sur le toit »,
130:  ou un LLM sur un gold.
151:- **les niveaux profonds n'ont pas de gold** : les confiances 0,32–0,78 sont **déclarées**, pas
161:1. **Un gold** de POS/syntagme/pragmatique sur 100–200 phrases pour transformer les confiances en
163:2. **Un modèle neuronal qualifié** (tagger ou LLM) sur ce gold ; l'adaptateur est branché.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"238/239\\|0,9958\\|86,25\" reports/*.md | head; echo ===; grep -rn \"238/239\\|0,9958\\|86,25\" reports/*.md | head", "description": "Find B13 gold figures"}`

  ```
reports/rapport-base-reelle.md
reports/rapport-bilan-chantier.md
reports/rapport-cloture-chantier.md
reports/rapport-convention-gv.md
reports/rapport-coordination-r.md
reports/rapport-evaluer-langue.md
reports/rapport-exemples-rejoues.md
reports/rapport-g017.md
reports/rapport-passe-honnetete.md
reports/rapport-pont-generatif.md
===
reports/rapport-base-reelle.md:7:> 86,25 %) et la **F1 est la même** (79,06 % contre 79,02 %) — le synthétique n'aidait donc **pas**
reports/rapport-base-reelle.md:18:| POS | 86,25 % | **88,91 %** (fermé 92,94 / ouvert 84,66) |
reports/rapport-bilan-chantier.md:53:| exact / cibles | 236/239 | **238/239** | **+2** | le dénominateur reste 239 (`g017` sans label) | [s065](rapport-s065.md) |
reports/rapport-bilan-chantier.md:54:| couverture (labels / 239) | 0,9916 | **0,9958** | **+0,0042** | — | [r035](rapport-r035.md) |
reports/rapport-bilan-chantier.md:55:| exactitude sur les spans | 0,9958 | **1,0** | **+0,0042** | 238 labels sur le bon span ; `g017` n'a pas de label | [s065](rapport-s065.md) |
reports/rapport-bilan-chantier.md:69:- **Le dénominateur compte.** 238/238 est le taux sur les **labels** ; 238/239 (0,9958) est le
reports/rapport-bilan-chantie
… [806 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; stat -c '%y %s' reports/atomes-prediction.json", "description": "Check final job and JSON timestamp"}`

  ```
stephane 2963235  109  0.0 5760984 110404 ?      Rsl  03:27   0:36 python3 tools/atomes_prediction.py --analyser
2026-11-15 03:27:35.790756256 -0500 164327
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' reports/rapport-panini-334.md", "description": "Read a model report header"}`

  ```
# J12.1 — Le §334 et les 44 œuvres : le retrieval et la prédiction de l'époque vs la filiation

> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, J12.1 · **Date** : 2026-11-14
> **Verdict** : ✅ **le §334 est une géométrie de filiation, pas d'époque — et le corpus ne permet pas
> de séparer les deux.** La loi H0 de Panini se reproduit (**R² = 0,909139** sur les **655 lignes** de
> paires ; **0,906307** sur les **488 paires uniques non auto**), et l'époque seule explique **0,258**
> de la distance lexicale ; mais elle n'ajoute que **0,0089** de R² **après** la topologie
> (p = 0,86 ; β standardisé **−0,035**). Le plan est **colinéaire** : **180** paires de même tradition
> ont **28,7 ans** d'écart en moyenne (max **230**), les **308** paires inter-traditions en ont
> **1 189** (**136** à ≤ 100 ans). Le contraste de filiation à **date fixe** est fort dans la tranche
> axiale (**Δ = −0,166**, p = 0,0005), mais **disparaît à surface contrôlée** (même langue source
> anglaise : **Δ = −0,135** contre un null de **−0,129**, p = 0,34).
> Sur les **44 signatures** (14 parts flottantes), le retrieval brut donne **61,4 %** de même tradition
> (hasard 22,4 %) et **56,8
… [3790 caractères tronqués]
  ```

- **bash** `{"command": "sleep 120; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; stat -c '%y %s' reports/atomes-prediction.json", "description": "Wait for final analysis", "timeoutMs": 180000}`

  ```
stephane 2963235  102  0.0 5761880 111304 ?      Rsl  03:27   2:41 python3 tools/atomes_prediction.py --analyser
2026-11-15 03:27:35.790756256 -0500 164327
  ```

- **job_output** `{"job_id": "bash-113"}`

  ```
=== cohorte utilisable (colonnes=2000, date=1000, degré date=1)
  [utilisable] n=28 : CV atomes…
  [utilisable] : date in-sample + atomes sur résidus…
  [utilisable] permutations colonnes (2000)…
    200/2000 ( 13.5s)
    400/2000 ( 26.9s)
    600/2000 ( 40.3s)
    800/2000 ( 53.5s)
    1000/2000 ( 66.7s)
    1200/2000 ( 80.2s)
    1400/2000 ( 93.3s)
    1600/2000 (106.5s)
    1800/2000 (119.6s)
    2000/2000 (132.7s)
  [utilisable] permutations date (1000)…
    date 200/1000 (145.9s)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=d['oeuvres']\nprint('NON MESURABLES')\nfor x in o:\n    if not x['mesures']:\n        print(f\"- {x['id']}: {x['n_mots_prose']} mots de pr … [729 caractères tronqués]`

  ```
NON MESURABLES
- aristotle_prior_analytics: 57 mots de prose, format=texte, propre=False
- bengio_2003: 0 mots de prose, format=pdf, propre=False
- daniel_book: 105 mots de prose, format=texte, propre=False
- ezekiel_book: 174 mots de prose, format=texte, propre=False
- hosea_book: 106 mots de prose, format=texte, propre=False
- jeremiah_book: 182 mots de prose, format=texte, propre=False
- mn35_culasaccaka: 37 mots de prose, format=texte, propre=False
- zechariah_book: 106 mots de prose, format=texte, propre=False
MESURABLES MAIS SIGNATURE NON PROPRE
- 2_esdras: n_jetons=3733, stop=0.0592, balises=0.3563, mots_prose=769
- isaiah_book: n_jetons=1579, stop=0.012, balises=0.0, mots_prose=210
PROPRE MAIS COURT (<1000 jetons)
- aristotle_posterior_analytics: n_jetons=941, mots_mesures=636
- book_of_enoch: n_jetons=827, mots_mesures=613
- lukasiewicz_1920: n_jetons=451, mots_mesures=425
- mengzi: n_jetons=304, mots_mesures=269
- mikolov_2013: n_jetons=600, mots_mesures=478
- qiwulun: n_jetons=788, mots_mesures=541
  ```

- **bash** `{"command": "sleep 90; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; stat -c '%y %s' reports/atomes-prediction.json", "description": "Check final job progress", "timeoutMs": 150000}`

  ```
stephane 2963235  101  0.0 5760844 110668 ?      Rsl  03:27   4:21 python3 tools/atomes_prediction.py --analyser
2026-11-15 03:27:35.790756256 -0500 164327
  ```

- **job_output** `{"job_id": "bash-113"}`

  ```
date 400/1000 (159.2s)
    date 600/1000 (172.5s)
    date 800/1000 (185.7s)
    date 1000/1000 (198.8s)
=== cohorte mesurable (colonnes=500, date=300, degré date=1)
  [mesurable] n=36 : CV atomes…
  [mesurable] : date in-sample + atomes sur résidus…
  [mesurable] permutations colonnes (500)…
    200/500 ( 17.0s)
    400/500 ( 34.0s)
  [mesurable] permutations date (300)…
    date 200/300 ( 59.5s)
[status: running]
  ```

- **bash** `{"command": "sleep 120; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; stat -c '%y %s' reports/atomes-prediction.json", "description": "Wait for final analysis completion", "timeoutMs": 180000}`

  ```
stephane 2963235  100  0.0 5760136 110308 ?      Rsl  03:27   6:27 python3 tools/atomes_prediction.py --analyser
2026-11-15 03:27:35.790756256 -0500 164327
  ```

- **job_output** `{"job_id": "bash-113"}`

  ```
=== cohorte propre (colonnes=500, date=300, degré date=1)
  [propre] n=34 : CV atomes…
  [propre] : date in-sample + atomes sur résidus…
  [propre] permutations colonnes (500)…
    200/500 ( 16.1s)
    400/500 ( 32.0s)
  [propre] permutations date (300)…
    date 200/300 ( 56.3s)
=== cohorte strict (colonnes=500, date=300, degré date=1)
  [strict] n=26 : CV atomes…
  [strict] : date in-sample + atomes sur résidus…
  [strict] permutations colonnes (500)…
    200/500 ( 12.4s)
    400/500 ( 24.6s)
  [strict] permutations date (300)…
    date 200/300 ( 43.0s)
=== cohorte utilisable (colonnes=500, date=300, degré date=2)
  [utilisable] n=28 : CV atomes…
  [utilisable] : date in-sample + atomes sur résidus…
  [utilisable] permutations colonnes (500)…
[status: running]
  ```

- **bash** `{"command": "sleep 75; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; stat -c '%y %s' reports/atomes-prediction.json", "description": "Wait for last cohort", "timeoutMs": 120000}`

  ```
2026-11-15 03:35:08.460804185 -0500 301918
  ```

### 👤 Utilisateur

background job bash-113 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/atomes_prediction.py --analyser) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-113"}`

  ```
200/500 ( 13.2s)
    400/500 ( 26.3s)
  [utilisable] permutations date (300)…
    date 200/300 ( 45.9s)
résultats → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/atomes-prediction.json
-- utilisable_d1 (n=28)
  POS          R²A=-0.0729 pC=0.3583 rhoA=+0.1782 pR=0.0295 R²date=+0.1630 R²res=-0.4650 pRes=1.0000
  SYNTAGMES    R²A=-0.1387 pC=0.7456 rhoA=+0.0005 pR=0.2439 R²date=+0.0579 R²res=-0.3840 pRes=0.9860
  ATTACHEMENT  R²A=-0.1049 pC=0.6812 rhoA=-0.0744 pR=0.4278 R²date=+0.0487 R²res=-0.2151 pRes=0.9171
-- mesurable_d1 (n=36)
  POS          R²A=+0.1092 pC=0.0020 rhoA=+0.3041 pR=0.0020 R²date=+0.0651 R²res=+0.1108 pRes=0.7973
  SYNTAGMES    R²A=+0.0207 pC=0.0180 rhoA=+0.3196 pR=0.0020 R²date=+0.0355 R²res=+0.0731 pRes=0.1063
  ATTACHEMENT  R²A=-0.1641 pC=0.9721 rhoA=+0.2123 pR=0.0120 R²date=+0.0256 R²res=-0.3716 pRes=0.9967
-- propre_d1 (n=34)
  POS          R²A=+0.0356 pC=0.0140 rhoA=+0.2373 pR=0.0080 R²date=+0.1028 R²res=-0.0517 pRes=0.9867
  SYNTAGMES    R²A=+0.0416 pC=0.0100 rhoA=+0.2573 pR=0.0020 R²date=+0.0526 R²res=-0.0204 pRes=0.8937
  ATTACHEMENT  R²A=-0.0352 pC=0.3273 rhoA=+0.1765 pR=0.0220 R²date=+0.0303 R²res=-0.1088 pRes=0.9668
-- strict_d1 (n=26)
  POS    
… [654 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-prediction.json'))\nprint('keys',list(d.keys()))\nprint('primary',d['cohorte_primaire'],'n',d['n'])\nprint('perm',d['permutations'])\nprint('ecartees',d['metriques_ecar … [921 caractères tronqués]`

  ```
keys ['fiche', 'version', 'date', 'titre', 'statut', 'source', 'atomes', 'cohorte_primaire', 'n', 'familles', 'metriques', 'metriques_ecartees', 'permutations', 'null_col', 'null_resid', 'null_date_in', 'noms', 'cohortes', 'oeuvres']
primary utilisable n 28
perm {'colonnes': 2000, 'date': 1000, 'graine': 20261115, 'degre_date': 1}
ecartees ['att_introuvable']
--- primary families
POS {'r2_atomes_moyen': -0.0729, 'p_col': 0.3583208395802099, 'p_col_holm': 1.0, 'r2_exces_moyen': 0.0332, 'rho_cv_moyen': 0.1782, 'p_rho_col': 0.02948525737131434, 'rho_exces_moyen': 0.2674, 'r2_date_in_moyen': 0.163, 'p_date_in': 0.008991008991008992, 'r2_resid_moyen': -0.465, 'p_resid': 1.0, 'p_resid_holm': 1.0}
SYNTAGMES {'r2_atomes_moyen': -0.1387, 'p_col': 0.7456271864067966, 'p_col_holm': 1.0, 'r2_exces_moyen': -0.0338, 'rho_cv_moyen': 0.0005, 'p_rho_col': 0.24387806096951525, 'rho_exces_moyen': 0.0846, 'r2_date_in_moyen': 0.0579, 'p_date_in': 0.1958041958041958, 'r2_resid_moyen': -0.384, 'p_resid': 0.986013986013986, 'p_resid_holm': 1.0}
ATTACHEMENT {'r2_atomes_moyen': -0.1049, 'p_col': 0.6811594202898551, 'p_col_holm': 1.0, 'r2_exces_moyen': -0.0136, 'rho_cv_moyen': -0.0744, 'p_rho_col': 0.4277861
… [1995 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-prediction.json'))\nfor k in ['syn_par_phrase','att_distance','pos_entropie','pos_part_nom','phrase_longueur','disc_connecteurs_1000']:\n    v=d['metriques'][k]\n    pr … [704 caractères tronqués]`

  ```
syn_par_phrase {'r2_atomes': -0.0507, 'p_col': 0.44427786106946526, 'rho_cv': -0.2037, 'p_rho_col': 0.6796601699150425, 'r2_date_in': 0.1146, 'p_date_in': 0.07692307692307693, 'r2_resid': -0.0091, 'p_resid': 0.02097902097902098}
att_distance {'r2_atomes': -0.0892, 'p_col': 0.751624187906047, 'rho_cv': 0.2103, 'p_rho_col': 0.1054472763618191, 'r2_date_in': 0.1754, 'p_date_in': 0.02197802197802198, 'r2_resid': -0.2017, 'p_resid': 0.9010989010989011}
pos_entropie {'r2_atomes': -0.0718, 'p_col': 0.5287356321839081, 'rho_cv': 0.0821, 'p_rho_col': 0.239880059970015, 'r2_date_in': 0.0209, 'p_date_in': 0.4145854145854146, 'r2_resid': -0.55, 'p_resid': 0.989010989010989}
pos_part_nom {'r2_atomes': -0.0688, 'p_col': 0.5157421289355323, 'rho_cv': 0.3045, 'p_rho_col': 0.07246376811594203, 'r2_date_in': 0.063, 'p_date_in': 0.23076923076923078, 'r2_resid': -0.5834, 'p_resid': 0.993006993006993}
phrase_longueur {'r2_atomes': -0.0273, 'p_col': 0.3498250874562719, 'rho_cv': -0.2913, 'p_rho_col': 0.824087956021989, 'r2_date_in': 0.1398, 'p_date_in': 0.04495504495504495, 'r2_resid': -0.0852, 'p_resid': 0.8311688311688312}
disc_connecteurs_1000 {'r2_atomes': -0.0089, 'p_col': 0.11694152923538231, 'rho
… [2189 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, numpy as np\nfrom scipy import stats\nsys.path.insert(0,'tools')\nimport atomes_prediction as ap\nd=json.load(open('reports/atomes-prediction-mesures.json'))\no=[x for x in d['oeuvres'] if ap._fil … [668 caractères tronqués]`

  ```
14 mean r2 -0.0728647207995806 per [-0.072 -0.069  0.431 -0.019 -0.148  0.232 -0.015 -0.057  0.001 -0.317
 -0.768]
  kaiser 5 ev [4.76 3.18 1.95 1.66 1.26 0.7  0.48 0.22 0.14 0.09 0.04 0.02 0.01 0.  ] cond 678375040980928.1
13 mean r2 -0.09248381934246774 per [-0.076 -0.116  0.429  0.025 -0.204  0.155 -0.013 -0.043 -0.011 -0.357
 -0.806]
  kaiser 5 ev [4.56 2.9  1.71 1.45 1.23 0.69 0.48 0.22 0.14 0.08 0.02 0.01 0.01] cond 27.947977376631663
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/atomes_prediction.py'\ns=open(p).read()\ns=s.replace('''    X = clr(np.array([o[\"signature\"] for o in sous], float))\n    annees = np.array([o[\"annee\"] for o in sous], float)''','''    Xfull = clr(np.a … [2182 caractères tronqués]`

  ```
OK
733:    Xfull = clr(np.array([o["signature"] for o in sous], float))
736:    X = Xfull[:, :-1]
867:        rho, p = stats.spearmanr(Xfull[:, j], annees)
878:        "base_clr": f"{X.shape[1]} colonnes (CLR de rang {X.shape[1]})",
883:                "nb_composantes_kaiser": int(np.sum(ev > 1))},
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/atomes_prediction.py --analyser", "description": "Rerun final analysis with 13-column CLR", "timeoutMs": 1800000, "run_in_background": true}`

  ```
started background job bash-130
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/tableaux_atomes.py <<'PY'\nimport json, sys\nD=json.load(open('reports/atomes-prediction.json'))\nP=[c for c in D['cohortes'] if c['cle']==D['cohorte_primaire']+'_d1'][0]\ndef f(x): return f\"{x:+.3f}\".replace('+','+') if … [3517 caractères tronqués]`

  ```
## Table familles (primaire)
| famille | R² atomes | p_col | Holm | ρ CV | p_ρ | R² date | p_date | R² résidu | p_resid |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **POS** | -0.073 | 0.3583 | 1.0000 | +0.178 | 0.0295 | +0.163 | 0.0090 | -0.465 | 1.0000 |
| **SYNTAGMES** | -0.139 | 0.7456 | 1.0000 | +0.001 | 0.2439 | +0.058 | 0.1958 | -0.384 | 0.9860 |
| **ATTACHEMENT** | -0.105 | 0.6812 | 1.0000 | -0.074 | 0.4278 | +0.049 | 0.2577 | -0.215 | 0.9171 |

## Table niveaux (meilleure métrique / métrique pré-déclarée)
| niveau | métrique | R² atomes | p_col | BH | ρ CV | R² date | p_date | p_resid | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| graphème | `graph_entropie` | +0.791 | 0.0005 | 0.0062 | +0.809 | +0.216 | 0.0130 | 0.9171 | brut, absorbé date |
| mot | `mot_longueur` | +0.654 | 0.0005 | 0.0062 | +0.726 | +0.393 | 0.0020 | 1.0000 | brut, absorbé date |
| pos | `pos_part_verbe` | +0.431 | 0.0025 | 0.0231 | +0.600 | +0.369 | 0.0020 | 1.0000 | brut, absorbé date |
| syntagme | `syn_par_phrase` | -0.051 | 0.4443 | 0.8892 | -0.204 | +0.115 | 0.0769 | 0.0210 | non |
| phrase | `phrase_negation` | +0.532 | 0.0005 | 0.0062 | +0.782 | +0.538 | 0.0010 | 0.4146 
… [3963 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; stat -c '%y %s' reports/atomes-prediction.json", "description": "Check rerun progress"}`

  ```
stephane 2965986  123  0.0 5761084 110300 ?      Rsl  03:36   0:17 python3 tools/atomes_prediction.py --analyser
2026-11-15 03:35:08.460804185 -0500 301918
  ```

- **bash** `{"command": "sleep 120; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; stat -c '%y %s' reports/atomes-prediction.json", "description": "Wait for rerun", "timeoutMs": 180000}`

  ```
stephane 2965986  102  0.0 5761656 111012 ?      Rsl  03:36   2:28 python3 tools/atomes_prediction.py --analyser
2026-11-15 03:35:08.460804185 -0500 301918
  ```

- **bash** `{"command": "sleep 150; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; stat -c '%y %s' reports/atomes-prediction.json", "description": "Wait for rerun completion", "timeoutMs": 200000}`

  ```
stephane 2965986  101  0.0 5760332 110348 ?      Rsl  03:36   5:05 python3 tools/atomes_prediction.py --analyser
2026-11-15 03:35:08.460804185 -0500 301918
  ```

- **job_output** `{"job_id": "bash-130"}`

  ```
=== cohorte utilisable (colonnes=2000, date=1000, degré date=1)
  [utilisable] n=28 : CV atomes…
  [utilisable] : date in-sample + atomes sur résidus…
  [utilisable] permutations colonnes (2000)…
    200/2000 ( 13.8s)
    400/2000 ( 27.6s)
    600/2000 ( 41.2s)
    800/2000 ( 54.9s)
    1000/2000 ( 68.2s)
    1200/2000 ( 81.5s)
    1400/2000 ( 94.8s)
    1600/2000 (108.1s)
    1800/2000 (121.5s)
    2000/2000 (134.8s)
  [utilisable] permutations date (1000)…
    date 200/1000 (148.4s)
    date 400/1000 (161.8s)
    date 600/1000 (175.2s)
    date 800/1000 (188.7s)
    date 1000/1000 (202.3s)
=== cohorte mesurable (colonnes=500, date=300, degré date=1)
  [mesurable] n=36 : CV atomes…
  [mesurable] : date in-sample + atomes sur résidus…
  [mesurable] permutations colonnes (500)…
    200/500 ( 17.2s)
    400/500 ( 34.4s)
  [mesurable] permutations date (300)…
    date 200/300 ( 60.1s)
=== cohorte propre (colonnes=500, date=300, degré date=1)
  [propre] n=34 : CV atomes…
  [propre] : date in-sample + atomes sur résidus…
  [propre] permutations colonnes (500)…
    200/500 ( 16.3s)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal/2026-11-15/ 2>/dev/null | head; echo ===; ls journal/2026-11-14/ 2>/dev/null | head; echo ===; sed -n '1,60p' journal/2026-11-14/*.md 2>/dev/null | head -60", "description": "Inspect journal conventions"}`

  ```
distribue.md
docs.md
mesures.md
portes.md
README.md
===
distribue.md
docs.md
memoire.md
mesures.md
moteur.md
portes.md
README.md
===
# 2026-11-14 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (3)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 05:37 | `bb68b820` | J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0089 APRÈS TOPO (p=0,86) ; FILIATION 61,4 % vs 50,0 % (HOLM 0,128), ÉPOQUE 56,8 % vs 53,8 % (p=0,373), ANNÉE INTRA-TRADITION R²=0,042 (HOLM 0,034) ; V150 β DATE −0,006 ≠ +0,138 | `en-cours.md`, `roadmap.md`, `genealogie-des-langues.md` (+17) |
| 07:24 | `5928e75a` | DOCS — LES 9 FICHES DU CHANTIER INDEXÉES, LE README DANS LE BUDGET (T1) ; CLÔTURE AU TAG chantier-2026-11-14 | `en-cours.md`, `README.md`, `distribue.md` (+13) |
|
… [3491 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat journal/2026-11-15/README.md 2>/dev/null | head -40; echo ===; ls -la journal/2026-11-15/", "description": "Inspect today's journal index"}`

  ```
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**6 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 1 | [distribue.md](distribue.md) |
| docs | 1 | [docs.md](docs.md) |
| mesures | 3 | [mesures.md](mesures.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 346.3 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE
… [1237 caractères tronqués]
  ```

- **bash** `{"command": "sleep 90; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; stat -c '%y %s' reports/atomes-prediction.json", "description": "Wait for rerun final cohorts", "timeoutMs": 120000}`

  ```
stephane 2965986  100  0.0 5760524 110644 ?      Rsl  03:36   6:46 python3 tools/atomes_prediction.py --analyser
2026-11-15 03:35:08.460804185 -0500 301918
  ```

- **job_output** `{"job_id": "bash-130"}`

  ```
400/500 ( 32.4s)
  [propre] permutations date (300)…
    date 200/300 ( 56.8s)
=== cohorte strict (colonnes=500, date=300, degré date=1)
  [strict] n=26 : CV atomes…
  [strict] : date in-sample + atomes sur résidus…
  [strict] permutations colonnes (500)…
    200/500 ( 12.6s)
    400/500 ( 25.3s)
  [strict] permutations date (300)…
    date 200/300 ( 44.2s)
=== cohorte utilisable (colonnes=500, date=300, degré date=2)
  [utilisable] n=28 : CV atomes…
  [utilisable] : date in-sample + atomes sur résidus…
  [utilisable] permutations colonnes (500)…
    200/500 ( 13.5s)
[status: running]
  ```

- **bash** `{"command": "sleep 80; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep \"atomes_prediction.py --analyser\" | grep -v grep | head; stat -c '%y %s' reports/atomes-prediction.json", "description": "Wait for last cohort completion", "timeoutMs": 120000}`

  ```
2026-11-15 03:43:36.702945619 -0500 301777
  ```

### 👤 Utilisateur

background job bash-130 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/atomes_prediction.py --analyser) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-130"}`

  ```
400/500 ( 27.1s)
  [utilisable] permutations date (300)…
    date 200/300 ( 47.5s)
résultats → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/atomes-prediction.json
-- utilisable_d1 (n=28)
  POS          R²A=-0.0925 pC=0.5552 rhoA=+0.1762 pR=0.0290 R²date=+0.1630 R²res=-0.5672 pRes=1.0000
  SYNTAGMES    R²A=-0.1604 pC=0.8506 rhoA=-0.0127 pR=0.2579 R²date=+0.0579 R²res=-0.4003 pRes=0.9830
  ATTACHEMENT  R²A=-0.0916 pC=0.6652 rhoA=-0.0473 pR=0.3513 R²date=+0.0487 R²res=-0.2187 pRes=0.9500
-- mesurable_d1 (n=36)
  POS          R²A=+0.1022 pC=0.0040 rhoA=+0.2796 pR=0.0060 R²date=+0.0651 R²res=+0.1047 pRes=0.7674
  SYNTAGMES    R²A=+0.0596 pC=0.0060 rhoA=+0.3350 pR=0.0020 R²date=+0.0355 R²res=+0.0728 pRes=0.1362
  ATTACHEMENT  R²A=-0.1525 pC=0.9780 rhoA=+0.2473 pR=0.0100 R²date=+0.0256 R²res=-0.3495 pRes=0.9967
-- propre_d1 (n=34)
  POS          R²A=+0.0100 pC=0.0359 rhoA=+0.2343 pR=0.0040 R²date=+0.1028 R²res=-0.0597 pRes=1.0000
  SYNTAGMES    R²A=+0.0143 pC=0.0220 rhoA=+0.2273 pR=0.0060 R²date=+0.0526 R²res=-0.0265 pRes=0.7508
  ATTACHEMENT  R²A=-0.0448 pC=0.4870 rhoA=+0.1857 pR=0.0220 R²date=+0.0303 R²res=-0.1572 pRes=0.9635
-- strict_d1 (n=26)
  POS          R²A=-0.0796 pC=
… [633 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='work/tableaux_atomes.py'\ns=open(p).read()\ns=s.replace(\"print('ACP',P['acp'],'cond',P['condition'],P['base_clr'])\",\"print('ACP',P.get('acp'),'cond',P.get('condition'),P.get('base_clr'))\")\nopen(p,'w').write … [83 caractères tronqués]`

  ```
## Table familles (primaire)
| famille | R² atomes | p_col | Holm | ρ CV | p_ρ | R² date | p_date | R² résidu | p_resid |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **POS** | -0.092 | 0.5552 | 1.0000 | +0.176 | 0.0290 | +0.163 | 0.0140 | -0.567 | 1.0000 |
| **SYNTAGMES** | -0.160 | 0.8506 | 1.0000 | -0.013 | 0.2579 | +0.058 | 0.1928 | -0.400 | 0.9830 |
| **ATTACHEMENT** | -0.092 | 0.6652 | 1.0000 | -0.047 | 0.3513 | +0.049 | 0.2328 | -0.219 | 0.9500 |

## Table niveaux (meilleure métrique / métrique pré-déclarée)
| niveau | métrique | R² atomes | p_col | BH | ρ CV | R² date | p_date | p_resid | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| graphème | `graph_entropie` | +0.811 | 0.0005 | 0.0092 | +0.825 | +0.216 | 0.0130 | 0.9271 | brut, absorbé date |
| mot | `mot_longueur` | +0.657 | 0.0005 | 0.0092 | +0.744 | +0.393 | 0.0030 | 1.0000 | brut, absorbé date |
| pos | `pos_part_verbe` | +0.429 | 0.0025 | 0.0277 | +0.593 | +0.369 | 0.0020 | 0.9990 | brut, absorbé date |
| syntagme | `syn_par_phrase` | -0.056 | 0.4538 | 0.8395 | -0.211 | +0.115 | 0.0859 | 0.0120 | non |
| phrase | `phrase_negation` | +0.440 | 0.0040 | 0.0277 | +0.789 | +0.538 | 0.0010 | 0.7592 
… [4243 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, numpy as np, collections\nD=json.load(open('reports/atomes-prediction.json'))\nP=[c for c in D['cohortes'] if c['cle']=='utilisable_d1'][0]\nids={o['id'] for o in D['oeuvres']}\n# reconstruct primary i … [677 caractères tronqués]`

  ```
n 28 unique 26
years -440 1972 median -355.0 pre1000 20 post1500 7
Counter({'GRECO': 17, 'FORMAL_LOGIC': 2, 'BUDDHIST': 2, 'MILLENARIAN': 2, 'COGNITIVE_SCIENCE': 2, 'RENAISSANCE_OCCULT': 1, 'CLASSICAL_ORACULAR': 1, 'NORSE_EDDIC': 1})
ids ['aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'curry_1930', 'dn1_brahmajala', 'kleene_1936', 'miller_evidence_prophecy', 'mn2_sabbasava', 'nostradamus_centuries', 'plato_charmides', 'plato_gorgias', 'plato_gorgias_jowett', 'plato_laws', 'plato_meno', 'plato_meno_jowett', 'plato_phaedo', 'plato_phaedrus_jowett', 'plato_philebus_jowett', 'plato_republic_jowett', 'plato_sophist', 'plato_symposium_jowett', 'plato_theaetetus_jowett', 'quillian_1968', 'russell_parousia_1878', 'schank_1972', 'sibylline_oracles', 'voluspa']
n_mots min max median 797 11517 10468.5
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > reports/rapport-atomes-prediction.md <<'MDEOF'\n# B2 — Les 14 atomes prédisent-ils les niveaux de Drave ? Le style de surface, oui ; POS, syntagmes et attachement, non\n\n> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **C … [26641 caractères tronqués]`

  ```
391 reports/rapport-atomes-prediction.md
63
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nD=json.load(open('reports/atomes-prediction.json'))\nfor f,v in D['familles'].items():\n    print(f,'rho',v['rho_cv_moyen'],'exces',v['rho_exces_moyen'],'p',v['p_rho_col'])\nEOF", "description": "Check … [20 caractères tronqués]`

  ```
POS rho 0.1762 exces 0.2686 p 0.028985507246376812
SYNTAGMES rho -0.0127 exces 0.0744 p 0.25787106446776614
ATTACHEMENT rho -0.0473 exces 0.0399 p 0.35132433783108447
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-atomes-prediction.md'\ns=open(p).read()\ns=s.replace('**Holm 0,087**','**Holm 0,088**')\ns=s.replace('ce p devient **0,087** après Holm','ce p devient **0,088** après Holm')\ns=s.replace(\"Le ρ d … [984 caractères tronqués]`

  ```
5:> 14 atomes ne prédisent pas les trois niveaux du mandat : POS **R²_CV = −0,092** (p_col = 0,56),
6:> syntagmes **−0,160** (p = 0,85), attachement **−0,092** (p = 0,67). Le seul signal nominal (POS,
7:> **ρ = +0,176**, p = 0,029, **Holm 0,088**) ne survit pas au contrôle de date (**p_resid = 1,0**).
183:| **POS** | **−0,092** | 0,5552 | 1,0000 | **+0,176** | 0,0290 | +0,163 | 0,0140 | −0,567 | **1,0000** |
185:| **ATTACHEMENT** | **−0,092** | 0,6652 | 1,0000 | −0,047 | 0,3513 | +0,049 | 0,2328 | −0,219 | **0,9500** |
189:ce p devient **0,088** après Holm sur les trois familles, et le contrôle de date le retire
224:| POS | −0,092 | −0,096 | +0,051 | 0,5552 | +0,176 | 0,0290 |
226:| ATTACHEMENT | −0,092 | −0,079 | +0,020 | 0,6652 | −0,047 | 0,3513 |
263:| **utilisable** | **28** | POS | **−0,092** | 0,5552 | +0,176 | 0,0290 | +0,163 | 1,0000 |
265:| utilisable | 28 | ATTACHEMENT | **−0,092** | 0,6652 | −0,047 | 0,3513 | +0,049 | 0,9500 |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '186,196p' reports/rapport-atomes-prediction.md", "description": "Check edited paragraph"}`

  ```
**Lecture.** Aucune des trois familles n'a de R² positif : le modèle ridge fait **moins bien** que la
moyenne des œuvres. La permutation des colonnes ne sauve que le ρ de POS (**+0,176**, p = 0,029), mais
ce p devient **0,088** après Holm sur les trois familles, et le contrôle de date le retire
(**p_resid = 1,0**). Les syntagmes et l'attachement sont au hasard, et le restent après date.

Le ρ de POS est un artefact de la LOOCV : le null de ρ n'est pas centré sur 0 (la moyenne d'entraînement
est retirée, ce qui anti-corrèle légèrement la prédiction et la valeur tenue à l'écart) ; c'est pourquoi
le p de ρ est plus petit que le p de R². L'excès de ρ (observé − null) est de **+0,267**, mais il ne
correspond qu'à un classement faible, et il disparaît après date.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-atomes-prediction.md'\ns=open(p).read()\nold=\"\"\"Le ρ de POS est un artefact de la LOOCV : le null de ρ n'est pas centré sur 0 (la moyenne d'entraînement\nest retirée, ce qui anti-corrèle légèr … [865 caractères tronqués]`

  ```
(**p_resid = 1,0**). Les syntagmes et l'attachement sont au hasard, et le restent après date.

Le ρ de POS est un artefact de la LOOCV : le null de ρ n'est pas centré sur 0 (la CV avec 13 prédicteurs
sur 28 observations produit des prédictions très resserrées et une légère anticorrélation résiduelle ; la
moyenne du null est **≈ −0,092**) ; c'est pourquoi le p de ρ est plus petit que le p de R². L'excès de ρ
(observé − null) est de **+0,269**, mais il ne correspond qu'à un classement faible, et il disparaît après
date.

### 4.2 Les huit niveaux
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nfor p in ['reports/atomes-prediction.json','reports/atomes-prediction-mesures.json']:\n    d=json.load(open(p))\n    print(p,'ok',len(json.dumps(d)))\nprint('JSON keys',list(json.load(open('reports/ato … [76 caractères tronqués]`

  ```
reports/atomes-prediction.json ok 248833
reports/atomes-prediction-mesures.json ok 88915
JSON keys ['fiche', 'version', 'date', 'titre', 'statut', 'source', 'atomes', 'cohorte_primaire', 'n', 'familles', 'metriques', 'metriques_ecartees', 'permutations', 'null_col', 'null_resid', 'null_date_in', 'noms', 'cohortes', 'oeuvres']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' tools/tests/linguistique/test_bloc_linguistique.py 2>/dev/null | head -60; ls tools/tests/linguistique/", "description": "Inspect test style"}`

  ```
"""Tests du bloc linguistique — contrat, substitution, parallèle, cascade, activation."""
import json
import pathlib
import stat
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl

TEXTE = "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat !"


class TestBlocLinguistique(unittest.TestCase):
    def setUp(self):
        self.h = bl.Heuristique(segmenter_s=False)
        self.n = bl.MockNeuronal()

    def test_niveaux_et_spans(self):
        a = self.h.analyser(TEXTE, "fr")
        niveaux = {e.niveau for e in a.etiquettes}
        self.assertEqual(set(bl.NIVEAUX) - niveaux, set(), f"niveaux manquants : {set(bl.NIVEAUX)-niveaux}")
        for e in a.etiquettes:
            self.assertGreaterEqual(e.debut, 0)
            self.assertLessEqual(e.fin, len(TEXTE))
            self.assertLessEqual(e.debut, e.fin)

    def test_relative_zero(self):
        """Relative zéro : [GN] [pronom sujet] [verbe] [préposition orpheline] → REL.

        La règle est **structurelle** : elle ne dépend ni du nom, ni du pronom, ni du verbe,
        ni de la prépositi
… [1995 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > tools/tests/linguistique/test_atomes_prediction.py <<'PY'\n\"\"\"Tests de l'outil B2 — CLR, fenêtres, qualité, CV ridge groupée, permutations.\"\"\"\nimport pathlib\nimport sys\nimport unittest\n\nimport numpy as np\n\nRACINE = … [3496 caractères tronqués]`

  ```
test_clr_somme_nulle (tools.tests.linguistique.test_atomes_prediction.TestAtomesPrediction.test_clr_somme_nulle) ... ok
test_cv_ridge_retrouve_une_relation (tools.tests.linguistique.test_atomes_prediction.TestAtomesPrediction.test_cv_ridge_retrouve_une_relation) ... ok
test_design_date (tools.tests.linguistique.test_atomes_prediction.TestAtomesPrediction.test_design_date) ... ERROR
test_fenetres_non_chevauchantes (tools.tests.linguistique.test_atomes_prediction.TestAtomesPrediction.test_fenetres_non_chevauchantes) ... ok
test_filtrer_prose_retire_le_js (tools.tests.linguistique.test_atomes_prediction.TestAtomesPrediction.test_filtrer_prose_retire_le_js) ... ok
test_groupes_doublons (tools.tests.linguistique.test_atomes_prediction.TestAtomesPrediction.test_groupes_doublons) ... ok
test_holm_et_bh (tools.tests.linguistique.test_atomes_prediction.TestAtomesPrediction.test_holm_et_bh) ... ok
test_p_perm (tools.tests.linguistique.test_atomes_prediction.TestAtomesPrediction.test_p_perm) ... ok
test_permutation_colonnes_detruit (tools.tests.linguistique.test_atomes_prediction.TestAtomesPrediction.test_permutation_colonnes_detruit) ... ok
test_r2_et_rho (tools.tests.linguistique.test_atome
… [768 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/tests/linguistique/test_atomes_prediction.py'\ns=open(p).read().replace('self.assertTrue(np.all(D[:, 1] < D[1:, 1]))','self.assertTrue(np.all(D[:-1, 1] < D[1:, 1]))')\nopen(p,'w').write(s)\nEOF\npython3 -m … [115 caractères tronqués]`

  ```
test_r2_et_rho (tools.tests.linguistique.test_atomes_prediction.TestAtomesPrediction.test_r2_et_rho) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.043s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,12p' docs/pilotage/en-cours.md; echo ===; sed -n '86,102p' docs/pilotage/en-cours.md", "description": "Read state sections to update"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 02 h 32 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.
===
## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
- **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
- **Pensée — B13 (actif)** : **183/183**, gold 432 ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017
… [2618 caractères tronqués]
  ```

- **bash** `{"command": "date \"+%Y-%m-%d %H:%M %Z\"", "description": "Current time"}`

  ```
2026-11-15 03:46 EST
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\ns=s.replace('**Mis à jour : 2026-11-15, 02 h 32 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**','**Mis à jour : 2026-11-15, 03 h 46 HNE (B2 : atomes → niv … [726 caractères tronqués]`

  ```
3:**Mis à jour : 2026-11-15, 03 h 46 HNE (B2 : atomes → niveaux, négatif contrôlé)**
93:- **Panini B2 — atomes prédicteurs des niveaux** : sur **28 œuvres propres** (44 signatures, 36 mesurables), POS **R² −0,092** (p 0,56), syntagmes **−0,160** (p 0,85), attachement **−0,092** (p 0,67) ; le style de surface est prédit (graphème **+0,811**, mot **+0,657**, négation **+0,440**, verbes **+0,429**) mais **absorbé par la date** (p_resid 0,76–1,0) ; [fiche](../../reports/rapport-atomes-prediction.md), [JSON](../../reports/atomes-prediction.json).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"R0.7\" docs/pilotage/roadmap.md | head; echo ===; sed -n '348,360p' docs/pilotage/roadmap.md", "description": "Find R0.7 roadmap row"}`

  ```
33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; la suite : **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; R2/R3 attendent N5/N4 |
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **
… [8917 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"J2.1\\|J2\\b\\|Panini\" docs/pilotage/roadmap.md | head -20", "description": "Find Panini section in roadmap"}`

  ```
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 vs 0,427)** ([fiche](../../reports/rapport-retrieval-epoque.md)) ; **J3.2 généalogie à deux faces : Panini couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au hasard exact, le signal de famille vit dans 
… [5254 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '110,132p' docs/pilotage/roadmap.md", "description": "Read roadmap narrative around J12"}`

  ```
contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même
tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à
**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction
d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150
n'est pas reproduit (**−0,006**, p=0,093). L'avertissement de Panini est **indexé à son corpus**.
[`fiche`](../../reports/rapport-panini-334.md) + [`JSON`](../../reports/panini-334.json).

**J12.2 — le corpus d'or CIC rejoué hors de Panini.** Le corpus portable de Panini
(**3** defs, **21** consts, **42** entrées : **36** `accepte`, **6** `rejette`) est rejoué par un
noyau **CIC-lite réécrit côté Drave**, sans importer le vérificateur de Panini : **42/42** verdicts,
**42/42** empreintes `sha256(preuve || type)`, **42/42** sérialisations canoniques. Le contrôle
négatif est net : altérer le dernier octet des **36** preuves acceptées les fait **36/36** rejeter,
et les **1 020** mutations d'un octet de `eq(2,2)` sont **1 020/1 020** rejetées ; un noyau
« accepte tout » et un noyau « rejette tou
… [823 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/roadmap.md'\ns=open(p).read()\nold='([`fiche`](../../reports/rapport-cic-verificateur.md)) + [`JSON`](../../reports/cic-verificateur.json).\\n\\n**J13.1'\nnew='''([`fiche`](../../reports/rapport-ci … [1515 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 16, in <module>
AssertionError
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '124,132p' docs/pilotage/roadmap.md | cat -A | head -20", "description": "Inspect exact J12.2 ending"}`

  ```
La copie `tools/tests/cic/corpus_dor_cic_v1.json` est **byte-identique** M-CM-  la source$
(`3018f6f4M-bM-^@M-&aaec`) ; la porte `tools/porte-cic.sh` et **21** tests rejouent le tout. C'est un$
**verrou de portabilitM-CM-)** : M-BM-+ nos deux systM-CM-(mes vM-CM-)rifient les mM-CM-*mes preuves M-BM-;, pas une preuve de$
correction du noyau Panini (le corpus n'exerce que **20** des **39** M-CM-)tiquettes du format).$
[`fiche`](../../reports/rapport-cic-verificateur.md) + [`JSON`](../../reports/cic-verificateur.json).$
$
**J13.1 M-bM-^@M-^T la table des mesures.** Le chantier est **consolidM-CM-)** en une table unique : **26 tM-CM-"ches**$
de J1.1 M-CM-  J12.2, **25 acceptations vertes**, **1 M-CM-)chec** (J5.2, le tag), **5 timeouts** dont **4$
rM-CM-)cupM-CM-)rM-CM-)s**. Chaque ligne porte sa **base** (612/602), son **avant**, son **aprM-CM-(s**, son **M-NM-^T**, un$
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/roadmap.md'\ns=open(p).read()\nold='[`fiche`](../../reports/rapport-cic-verificateur.md) + [`JSON`](../../reports/cic-verificateur.json).\\n\\n**J13.1'\nnew='''[`fiche`](../../reports/rapport-cic-v … [1045 caractères tronqués]`

  ```
130:**B2 — les atomes ne prédisent pas les niveaux.** Sur les **28 œuvres propres** (44 signatures,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"B13 neuronal\" docs/pilotage/roadmap.md | head; python3 - <<'EOF'\ns=open('docs/pilotage/roadmap.md').read()\ni=s.find('J12.2 corpus d')\nprint(repr(s[i-100:i+400]))\nEOF", "description": "Find exact R0.7 row ending"}`

  ```
363:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 langues** à **0,9687** ; **gold 360** : POS **0,765**, syntagmes exacts **0,190**/**tête 0,510**, **attachement tête 1,0/0,966/0,932** (59 ambiguës), pragmatique **1,0/1,0/0,994/0,889** ; le neuronal réel est **qualifié** (tagger 7B, POS **0,9440** ; **syntagmes 0,7606** ; **cascade complète 0,9415/0,7539/1,0**) ; **corpus commun UDHR** (21 textes, 418/438 paires exactes, 8/8 contrôles) ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine, l'époque ne pèse pas à écriture contrôlée** ([fiche](../../reports/rapport-retrieval-epoque.md)) ; **J3.2 généalogie à deux faces : Panini 3/655 paires inter-langues, 5/21 langues ; Glottolog 21/21 ; 154/154 paires hors script au hasard, famille dans 2-3 paires** ([fiche](../../reports/rapport-genealogie-deux-faces.md)) ; **J7.1 retrieval par famille : 66,1 % famille / 26,1 % sœur (hasard 10,3 / 2,5), hors écriture au hasard ; sœurs 0,619 vs 0,0445 sur LANG_TREE 25 (13,9×, +0,448, p=0,002), nul sur l
… [1396 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/roadmap.md'\ns=open(p).read()\nold='([fiche](../../reports/rapport-cic-verificateur.md)) | — (livré ; B13 neuronal'\nnew='([fiche](../../reports/rapport-cic-verificateur.md)) ; **B2 atomes → niveau … [395 caractères tronqués]`

  ```
1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"atomes\" reports/README.md | head; wc -l reports/README.md", "description": "Check reports index"}`

  ```
36:| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |
214 reports/README.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '30,42p' reports/README.md", "description": "Read reports index around atomes"}`

  ```
| [`rapport-coordination-n2.md`](rapport-coordination-n2.md) | **N2** — le mètre RoPE : 8,0225 → |
| [`rapport-coordination-n2-v2.md`](rapport-coordination-n2-v2.md) | **N2** — la commande validée : `--rope --val` **2,7856**, `--rope` seul **40,0658**, témoin **3,09** |
| [`rapport-coordination-s.md`](rapport-coordination-s.md) | **S** — les 11 verdicts non committés |
| [`rapport-coordination-s-v2.md`](rapport-coordination-s-v2.md) | **S** — la page `/` ne sert pas la v7 : **369** stockés, **0** `profondeur`, **41** verdicts à re-juger |
| [`rapport-coordination-r.md`](rapport-coordination-r.md) | **R** — tagger POS 612 : **0,9475 (+8,49)** |
| [`rapport-tagger-option.md`](rapport-tagger-option.md) | **R0.7 / 1A** — le tagger POS en option : **+8,57** sur 20 phrases, **+8,49** sur 612, défaut hors ligne |
| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |
| [`rapport-corpus-commun.md`](rapport-corpus-commun.md) | **Panini** — le corpus commun UDHR |
| [`rapport-retrieval-epoque.md`](rapport-retrieval-epoque.md) | **Panini** — le retrieval contrôlé |
| [`rapport-retrieval-familles.md`](rapport-retrieval-familles.md) | **Panini** — le 
… [347 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/README.md'\ns=open(p).read()\nold='| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |\\n'\nnew=old+'| [`rapport-atomes-prediction.md`](rapport-atomes-predi … [309 caractères tronqués]`

  ```
37:| [`rapport-atomes-prediction.md`](rapport-atomes-prediction.md) | **Panini B2** — les atomes ne prédisent pas POS/syntagmes/attachement sur 28 œuvres propres ; le style est prédit, la date l'absorbe |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, pathlib\np=pathlib.Path('reports/rapport-atomes-prediction.md')\ns=p.read_text()\nbad=[]\nfor m in re.finditer(r'\\[[^\\]]*\\]\\(([^)]+)\\)',s):\n    u=m.group(1).split('#')[0]\n    if not u or u.startsw … [231 caractères tronqués]`

  ```
links 11 bad []
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 740 fiche(s) · 834 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 739 fichiers, le disque en a 740
     · compteurs : en-cours.md dit 832 JSON, le disque en a 834
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -30", "description": "Run table gate", "timeoutMs": 300000}`

  ```
✅ 1812 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4350 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"739\\|832\" docs/pilotage/en-cours.md | head", "description": "Find counters in en-cours"}`

  ```
111:| fichiers / JSON de résultats | **739** / **832** | `reports/*.md` / `reports/*.json` |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/en-cours.md'\ns=open(p).read().replace('| fichiers / JSON de résultats | **739** / **832** |','| fichiers / JSON de résultats | **740** / **834** |')\nopen(p,'w').write(s)\nEOF\npython3 tools/revue … [107 caractères tronqués]`

  ```
revue de documentation · 740 fiche(s) · 834 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -40", "description": "Check git status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-72a370ef-2ad7-4a59-8418-d88c38545f6e/digest.md
 M journal/sessions/session-72a370ef-2ad7-4a59-8418-d88c38545f6e/rapport.md
 M reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? journal/sessions/session-10414d5d-1d81-4840-b524-e77375127547/
?? reports/atomes-prediction-mesures.json
?? reports/atomes-prediction.json
?? reports/rapport-atomes-prediction.md
?? reports/rapport-gold-reel-50.json
?? reports/rapport-gold-reel-50.md
?? reports/rapport-s-paragraphes.md
?? tools/atomes_prediction.py
?? tools/tests/linguistique/gold_reel_50.py
?? tools/tests/linguistique/test_atomes_prediction.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo ===; python3 tools/taille_documents.py 2>&1 | tail -15; echo ===; python3 tools/verifie_journal.py 2>&1 | tail -15; echo ===; python3 tools/verifier_schemas.py 2>&1 | tail -10", … [75 caractères tronqués]`

  ```
en-cours · 1725 mots · 7 sections · 4 session(s) · 11 puces · 5 questions
  ❌ 1 anomalie(s) :
     · 11 puces dans « Ce qui est en cours » > 10
===
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4095 mots (budget 4 000)

  avertissements :
     · 55 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9113 mots > budget 9000 (T1)
     · T0 : 4095 mots (AGENTS + en-cours + une tâche) > budget 4 000
===
  journal · 47 jour(s) · 199 session(s) · 2561 lien(s)
  ✅ un dossier p
… [217 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re\ns=open('docs/pilotage/en-cours.md').read()\nstart=s.index('## Ce qui est en cours')\nend=s.index('## Les chiffres de l\\'état')\nfor line in s[start:end].split('\\n'):\n    if line.startswith('- **'):\n  … [108 caractères tronqués]`

  ```
29 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; 
32 - **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>
55 - **Pensée — B13 (actif)** : **183/183**, gold 432 ; `r035` (238/238), conventio
26 - **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ;
62 - **Panini J2.1–J3.2** : table **14 atomes** ; UDHR **418/438** ; J3.1 script do
72 - **Panini B2 — atomes prédicteurs des niveaux** : sur **28 œuvres propres** (44
39 - **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **6
15 - **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1 inter-tradit
48 - **Panini J12.1–J12.2 — §334 et CIC** : §334 — 655 lignes = 495 paires uniques 
79 - **J5.1 / J10.1 / J13.1 / J14.1 — les bilans et la clôture** : semaine (F1 **0,
58 - **J11.1–J11.4** : par-langue fr/en ; J11.3 50 textes, 115/0 chevauchements ; J
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\n# 1. merge B2 into J2.1\nold_j21='- **Panini J2.1–J3.2** : table **14 atomes** ; UDHR **418/438** ; J3.1 script domine, date non significative ; J3.2 : **5/21** lang … [3329 caractères tronqués]`

  ```
29 - **S — les structures** : 61/61 types, 144/144 rôles, 56 te
32 - **N2 — en pause** : **commande validée** `eval_longueurs.p
55 - **Pensée — B13 (actif)** : **183/183**, gold 432 ; `r035` 
26 - **L — le bloc langue** : contrat ; frontière script 1,0, l
93 - **Panini J2.1–J3.2 + B2** : table **14 atomes** ; UDHR **4
39 - **Panini J7.1** : 532 textes (445 langues) ; hors script, 
15 - **Panini B1 — protocole à date contrôlée** : **60 paires**
48 - **Panini J12.1–J12.2 — §334 et CIC** : §334 — 655 lignes =
65 - **J5.1 / J10.1 / J13.1 / J14.1 — bilans et clôture** : sem
47 - **J11.1–J11.4** : par-langue fr/en, 50 textes, schéma v2 (
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\ns=s.replace('**B2 : atomes → niveaux négatif** (POS −0,092, syntagmes −0,160, attachement −0,092 sur 28 œuvres propres ; style prédit mais absorbé par la date)','**B … [612 caractères tronqués]`

  ```
T0 max : 4029 mots (budget 4 000)

  avertissements :
     · 55 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9113 mots > budget 9000 (T1)
     · T0 : 4029 mots (AGENTS + en-cours + une tâche) > budget 4 000
===
  en-cours · 1659 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\n# J2.1 remove J3.1 clause\ns=s.replace(' ; J3.1 script domine, date non significative ; J3.2 :',' ; J3.2 :')\n# J5.1 shorten\ns=s.replace('semaine F1 **0,7533 → 0,79 … [1117 caractères tronqués]`

  ```
T0 max : 4003 mots (budget 4 000)
  ❌ 2 violation(s) :
     · T0 : 4003 mots (AGENTS + en-cours + une tâche) > budget 4 000
  en-cours · 1633 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\ns=s.replace('table **14 atomes**','**14 atomes**')\ns=s.replace('par-langue fr/en, 50 textes','fr/en, 50 textes')\ns=s.replace('semaine F1 **0,7902**','F1 **0,7902** … [292 caractères tronqués]`

  ```
T0 max : 3999 mots (budget 4 000)
  ❌ 1 violation(s) :
  en-cours · 1629 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re\ns=open('docs/pilotage/roadmap.md').read()\ni=s.index('**B2 — les atomes'); j=s.index('**J13.1',i)\npara=s[i:j]\nprint('B2 para words',len(re.findall(r'\\w+',para)))\nprint(para)\n# detail clause\nk=s.ind … [158 caractères tronqués]`

  ```
B2 para words 145
**B2 — les atomes ne prédisent pas les niveaux.** Sur les **28 œuvres propres** (44 signatures,
36 mesurables), les 14 atomes V14 ne prédisent pas POS (**R²_CV −0,092**, p=0,56), syntagmes
(**−0,160**, p=0,85) ni attachement (**−0,092**, p=0,67) ; le seul ρ nominal (POS +0,176, p=0,029,
Holm 0,088) ne survit pas à la date (p_resid=1,0). Le dispositif est sensible au style (entropie des
graphèmes +0,811, longueur des mots +0,657, négation +0,440, verbes +0,429), mais la date absorbe tout
(p_resid 0,76–1,0). Le signal des 36 mesurables (+0,102 / +0,060) tombe à +0,010 / +0,014 sur 34 et
−0,080 / −0,204 sur 26 : il est porté par les sources courtes et deux signatures non-propres.
[`fiche`](../../reports/rapport-atomes-prediction.md) + [`JSON`](../../reports/atomes-prediction.json).


detail words 33
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -o \"J3.1 retrieval à époque contrôlée : l'écriture domine, l'époque ne pèse pas à écriture contrôlée\" docs/pilotage/roadmap.md | wc -l", "description": "Count J3.1 clause occurrences"}`

  ```
1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/roadmap.md'\ns=open(p).read()\n# 1. shorten B2 paragraph\ni=s.index('**B2 — les atomes'); j=s.index('**J13.1',i)\nnew='''**B2 — atomes et niveaux : négatif contrôlé.** Sur **28 œuvres propres**, PO … [1335 caractères tronqués]`

  ```
9033    490   T1   9000  docs/pilotage/roadmap.md
  T0 max : 3999 mots (budget 4 000)
  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9033 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/roadmap.md'\ns=open(p).read()\n# shorten B2 paragraph\ni=s.index('**B2 — atomes'); j=s.index('**J13.1',i)\nnew='''**B2 — atomes et niveaux : négatif contrôlé.** Sur **28 œuvres propres**, POS **R²_ … [834 caractères tronqués]`

  ```
9006    489   T1   9000  docs/pilotage/roadmap.md
  T0 max : 3999 mots (budget 4 000)
  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9006 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/roadmap.md'\ns=open(p).read()\ns=s.replace('**B2 — atomes et niveaux : négatif contrôlé.** Sur **28 œuvres propres**, POS','**B2 — atomes et niveaux : négatif.** **28 œuvres propres**, POS')\ns=s.r … [260 caractères tronqués]`

  ```
9002    489   T1   9000  docs/pilotage/roadmap.md
  T0 max : 3999 mots (budget 4 000)
  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9002 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='docs/pilotage/roadmap.md'\ns=open(p).read()\ns=s.replace('**28 œuvres propres**, POS','**28 œuvres**, POS')\ns=s.replace('; le ρ POS (+0,176','; ρ POS (+0,176')\nopen(p,'w').write(s)\nEOF\npython3 tools/taille_d … [112 caractères tronqués]`

  ```
9000    489   T1   9000  docs/pilotage/roadmap.md
  T0 max : 3999 mots (budget 4 000)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -6", "description": "Check budget output"}`

  ```
T0 max : 3999 mots (budget 4 000)

  avertissements :
     · 55 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -6; echo ===; python3 tools/verifie_en_cours.py 2>&1 | tail -4; echo ===; python3 tools/verifie_journal.py 2>&1 | tail -3; echo ===; bash tools/porte-tableaux.sh 2>&1 | tail -5", "desc … [60 caractères tronqués]`

  ```
revue de documentation · 740 fiche(s) · 834 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
===
  en-cours · 1629 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
===
  journal · 47 jour(s) · 199 session(s) · 2561 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
===
  ✅ 1812 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4350 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m unittest tools.tests.linguistique.test_atomes_prediction tools.tests.linguistique.test_bloc_linguistique 2>&1 | tail -8", "description": "Run relevant unit tests", "timeoutMs": 300000}`

  ```
..............................
----------------------------------------------------------------------
Ran 30 tests in 0.113s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/journal_auto.py --help 2>&1 | head -30", "description": "Check journal_auto usage"}`

  ```
usage: journal_auto.py [-h] [--jour JOUR] [--depuis DEPUIS] [--lister]
                       [--dry-run] [--quiet]

options:
  -h, --help       show this help message and exit
  --jour JOUR      AAAA-MM-JJ (défaut : aujourd'hui)
  --depuis DEPUIS  générer chaque jour depuis cette date
  --lister         montrer les thèmes et leurs mots-clés
  --dry-run
  --quiet
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md; echo ===; git diff -- docs/pilotage/roadmap.md | head -80", "description": "Inspect our diffs"}`

  ```
docs/pilotage/en-cours.md | 14 +++++++-------
 docs/pilotage/roadmap.md  |  7 ++++++-
 reports/README.md         |  1 +
 3 files changed, 14 insertions(+), 8 deletions(-)
===
diff --git a/docs/pilotage/roadmap.md b/docs/pilotage/roadmap.md
index edd202a3..29962de9 100644
--- a/docs/pilotage/roadmap.md
+++ b/docs/pilotage/roadmap.md
@@ -127,6 +127,11 @@ La copie `tools/tests/cic/corpus_dor_cic_v1.json` est **byte-identique** à la s
 correction du noyau Panini (le corpus n'exerce que **20** des **39** étiquettes du format).
 [`fiche`](../../reports/rapport-cic-verificateur.md) + [`JSON`](../../reports/cic-verificateur.json).
 
+**B2 — atomes et niveaux : négatif.** **28 œuvres**, POS **R²_CV −0,092**,
+syntagmes **−0,160**, attachement **−0,092** ; ρ POS (+0,176, p=0,029, Holm 0,088) ne survit pas à la
+date (p_resid=1,0). Le style est absorbé par la date (graphèmes +0,811, mots +0,657, négation
++0,440, verbes +0,429). [`fiche`](../../reports/rapport-atomes-prediction.md) + [`JSON`](../../reports/atomes-prediction.json).
+
 **J13.1 — la table des mesures.** Le chantier est **consolidé** en une table unique : **26 tâches**
 de J1.1 à J12.2, **25 acceptations vertes**, **1 échec** (J5
… [6553 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/pilotage/en-cours.md | head -80", "description": "Inspect en-cours diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index f6b3be80..69e07d57 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 02 h 32 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**
+**Mis à jour : 2026-11-15, 03 h 46 HNE (B2 : atomes → niveaux, négatif contrôlé)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -87,17 +87,17 @@
 
 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
 - **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
-- **Pensée — B13 (actif)** : **183/183**, gold 432 ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, restitution v1 (46/46, strict 0,1087), **J9.1** (19 fiches) ; [s065](../../re
… [5014 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --check -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md; echo \"diff-check=$?\"; python3 -m json.tool reports/atomes-prediction.json > /dev/null && echo json-ok", "description": "Check whitespace and  … [6 caractères tronqués]`

  ```
diff-check=0
json-ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/atomes_prediction.py tools/tests/linguistique/test_atomes_prediction.py reports/rapport-atomes-prediction.md reports/atomes-prediction.json reports/atomes-prediction-mesures.json reports/README.md docs/pilotage/en-cours … [392 caractères tronqués]`
