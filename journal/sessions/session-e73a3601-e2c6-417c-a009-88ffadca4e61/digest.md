# Session DSH — relecture

- identifiant : `session-e73a3601-e2c6-417c-a009-88ffadca4e61`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 04:35:55
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche D1 : les exemples de `docs/produit/exemples.md` — ajoute 3 exemples avec `--tagger` (la sortie réelle avec la clé, le coût affiché) et 2 avec `--reel` (la base honnête), et vérifie que les sorties collent au code courant (F1 0,7902, 238/239, schéma v2). Fiche `reports/rapport-exemples-tagger.md` + JSON, commit.

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

- **bash** `{"command": "pwd && ls", "description": "List repository root"}`

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
  ```

- **bash** `{"command": "git status --short && git log --oneline -5", "description": "Show git status and recent commits"}`

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
ee04ea91 BILAN DE LA NUIT — LE TAGGER (95,75), LA BASE HONNÊTE (452), LA PHASE C/B (N2, S, R, PANINI) ET LES NÉGATIFS DITS
c24253ee DOC PRODUIT — LA PASSE D'HONNÊTETÉ : LES TROIS BASES (612, 602, RÉEL 452), L'ATTACHEMENT 238/239, LE TAGGER 95,75, LES CHIFFRES DATÉS ANNOTÉS
f1c6b506 PHASE 3 (C PUIS B) — N2 (--rope --canal-dir), S (page / et 11 VERDICTS), R (GOLD RÉEL 452), PANINI (PROTOCOLE À DATE CONTRÔLÉE, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX, CIC 42/42) ; 6 FICHES, SEPT. 9 DU PLAN
2067a6f0 B3 — LE CORPUS D'OR CIC V2 : 42/42 TYPES DE BRUJIN BIEN FORMÉS, 42/42 SHA256 PAR DEUX IMPLÉMENTATIONS, 36/36 PREUVES ET 42/42 TYPES ALTÉRÉS REJETÉS
01b6db6e JOURNAL — 2026-11-15 : B2, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX (NÉGA
… [48 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/produit/ && wc -l docs/produit/exemples.md", "description": "List product docs and line count"}`

  ```
exemples.md
README.md
682 docs/produit/exemples.md
  ```

- **bash** `{"command": "grep -rn -- \"--tagger\\|--reel\" --include=*.py --include=*.md . | head -80", "description": "Find tagger and reel options"}`

  ```
./reports/rapport-pensee-gold-linguistique.md:90:`--reel` essaie `NeuronalLLM` avec `Qwen2.5-0.5B-Q4_0` et 10 s : **`RefusNeuronal`**. Le mock est
./reports/pensee-tagger-option.json:7:  "drapeau": "--tagger",
./reports/pensee-tagger-option.json:154:   "le défaut (sans --tagger) est exactement l'heuristique",
./reports/pensee-tagger-option.json:157:   "evaluer --tagger publie le delta et le coût"
./reports/rapport-tagger-option.md:4:> 2026-11-14 · **Verdict** : ✅ **option livrée** — `--tagger` sur `analyser` et `evaluer` ; POS
./reports/rapport-tagger-option.md:19:**Sur la base réelle 452** (`--tagger --reel`) : **0,9500** contre **0,8891** — **+6,1 points** ;
./reports/rapport-tagger-option.md:27:python3 tools/drave.py analyser "Le chat dort." --tagger          # POS par l'API, syntagmes heuristiques
./reports/rapport-tagger-option.md:28:python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
./reports/rapport-tagger-option.md:29:python3 tools/drave.py evaluer --tagger                            # heuristique + cascade API + Δ
./reports/rapport-tagger-option.md:30:python3 tools/drave.py evaluer --tagger --par-langue --json
./reports/rapport-tagger-option.md:63:| mesu
… [3139 caractères tronqués]
  ```

- **job_kill** `{"job_id": "bash-4", "reason": "Malformed grep command, stopping scan"}`

  ```
requested cancellation of job bash-4
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md</path>
<type>file</type>
<content>
1: # Cinq exemples d'analyse, commentés
2: 
3: > **Ce que ce document est.** Cinq exécutions **réelles** du produit, avec leur JSON commenté. Il
4: > complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
5: > *comment lire* ce qui sort. Les sorties ont été produites le **2026-11-06** sur la branche
6: > `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et sans réseau ;
7: > elles ont été **rejouées le 2026-11-14** sur le code courant — F1 **0,7902**, attachement
8: > **238/238 labels** (238/239 cibles), schéma **v2**. Le format v2 ajoute `version: 2` et, sur un
9: > syntagme qui chevauche un autre, `meta.partition`/`meta.alternative` ; v1 reste lue
10: > ([schéma v2](../../tools/schemas/drave-annotation-v2.json)).
11: >
12: > **Le rejeu du 14/11.** **4 blocs sur 5** ont bougé : la ponctuation finale entre dans le POS
13: > (20 étiquettes et non 19), le refus sort en **3**, le POS anglais de `r241` s'améliore et
14: > `r035`, l'ancien échec connu, est désormais **prédit**. Seul le bloc `g011` est identique
… [24849 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-option.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-base-reelle.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-option.md</path>
<type>file</type>
<content>
1: # R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne
2: 
3: > **Ligne de roadmap** : **R0.7** (le lecteur) · **Décision** : **1A** du 14/11 · **Date** :
4: > 2026-11-14 · **Verdict** : ✅ **option livrée** — `--tagger` sur `analyser` et `evaluer` ; POS
5: > **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre
6: > 0,8625** du gold 612 (**+8,49**) ; **40 appels**, **11 868 tokens** (cache neuf), **0 refus** ;
7: > le **défaut** reste l'**heuristique**, CPU, hors ligne, déterministe. Le gain est **+4,67** sur
8: > le seul gold réel 432 : lire le chiffre avec sa source.
9: 
10: ## 1 bis. Les deux défauts corrigés (15/11)
11: 
12: | défaut | avant | **après** |
13: |---|---|---|
14: | **2 appels par phrase** (le tagger de syntagmes était appelé sans être utilisé) | 2 appels | **1 appel** |
15: | **`PONCT` perdu** (le tagger ne reçoit que mots et nombres) | 0 ponctuation étiquetée | **25/25** (restituée depuis l'heuristique) |
16: 
17: **La mesure sur le gold 61
… [10319 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-base-reelle.md</path>
<type>file</type>
<content>
1: # B13 — la base honnête : `evaluer --reel`, 452 phrases réelles, et ce que le synthétique cachait
2: 
3: > **Ligne de roadmap** : **B13** (le produit) · **Décision** : 6A · **Date** : 2026-11-15 ·
4: > **Verdict** : ✅ **la CLI sait maintenant mesurer le réel** (`evaluer --reel`) et **publie la
5: > base réelle à côté du global** dans la sortie par défaut. Ce que ça révèle : sur les **452
6: > phrases réelles** (main + corpus, sans les 160 synthétiques), le **POS monte** (88,91 % contre
7: > 86,25 %) et la **F1 est la même** (79,06 % contre 79,02 %) — le synthétique n'aidait donc **pas**
8: > le POS, contrairement à ce qu'on pouvait craindre, mais il **tirait la moyenne vers le bas**.
9: >
10: > **Dispositif** : [`drave.py`](../tools/drave.py) (`--reel`, la ligne `BASE RÉELLE`),
11: > [`test_produit.py`](../tools/tests/test_produit.py) (2 tests) ; JSON
12: > [`pensee-base-reelle.json`](pensee-base-reelle.json).
13: 
14: ## 1. Les deux bases
15: 
16: | mesure | vivant 612 | **réel 452** |
17: |---|---:|---:|
18: | POS | 86,25 % | **88,91 %** (fermé 92,94 / ouvert
… [2485 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/drave.py && grep -n \"tagger\\|reel\\|cout\\|coût\\|BASE RÉELLE\\|BASE REELLE\" tools/drave.py | head -100", "description": "Inspect drave CLI flags"}`

  ```
901 tools/drave.py
8:    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
11:    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
21:En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
24:**Sans `--tagger`, le défaut ne change pas** : heuristique, CPU, hors ligne, déterministe.
28:Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger absent · 1 erreur.
57:# Le tagger est une **option** : sans `--tagger`, rien de ce bloc n'est importé ni exécuté.
60:# La fusion de l'option : le POS vient du tagger, tout le reste de l'heuristique. On ne force
85:# --------------------------------------------------------------------------- le tagger (option)
89:    """Aucune clé : le tagger est une option, jamais un prérequis du produit."""
99:def _cle_tagger() -> str:
117:        "Sans --tagger, le défaut reste l'heuristique hors ligne."
121:def _client_tagger():
124:    return DeepSeek(cle=_cle_tagger())
127:def _transport_tagger(client, stats: dict):
128:    """Le transport attendu par les taggers : invite → contenu, avec le coût mesuré."""
150:    ""
… [6093 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 230}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """drave.py — le point d'entrée produit du bloc linguistique.
3: 
4: Une seule commande, quatre gestes, hors ligne et déterministe :
5: 
6:     python3 tools/drave.py analyser "Le chat dort."
7:     python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
8:     python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
9:     python3 tools/drave.py evaluer
10:     python3 tools/drave.py evaluer --gold --json
11:     python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
12:     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
13:     python3 tools/drave.py restituer "Le chat dort."
14:     python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
15:     python3 tools/drave.py --version
16: 
17: Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
18: avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et l
… [10240 caractères tronqués]
  ```

- **bash** `{"command": "git branch --show-current; ls ~/.config/drave/ 2>/dev/null; [ -n \"$DEEPSEEK_KEY_FILE\" ] && echo \"KEYFILE=$DEEPSEEK_KEY_FILE\"; [ -n \"$DEEPSEEK_API_KEY\" ] && echo \"APIKEY set\"; [ -n \"$DSH_KEY_FILE\" ] && echo \"DSHKEYFILE=$DSH_KEY_FILE\"", "description": "Check branch and API key … [15 caractères tronqués]`

  ```
s/v7
deepseek.key
[exit code: 1]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 245, "limit": 400}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
245: def formater_annotation(a: bl.Annotation, tagger: bool = False,
246:                         stats: dict | None = None) -> str:
247:     """La sortie lisible : POS compact, syntagmes (rôle + cible), pragmatique, couverture.
248: 
249:     Avec `--tagger`, l'en-tête le dit, le coût de l'API est affiché et un refus du tagger est
250:     nommé — le JSON d'annotation, lui, garde exactement le même contrat.
251:     """
252:     titre = (f"{NOM} {VERSION} — analyse cascade POS (tagger API DeepSeek, réseau)"
253:              if tagger else f"{NOM} {VERSION} — analyse heuristique (CPU, hors ligne)")
254:     lignes = [titre]
255:     lignes.append(
256:         f"langue={a.langue} script={a.script} source={a.source} · {len(a.etiquettes)} étiquettes "
257:         f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"
258:     )
259: 
260:     pos = [e for e in a.etiquettes if e.niveau == "pos"]
261:     if pos:
262:         lignes.extend(_envelopper("POS  ", " ".join(f"{e.valeur}/{e.type}" for e in pos)))
263:     else:
264:         lignes.appe
… [20329 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --json > /tmp/eval.json 2>/tmp/eval.err; echo exit=$?; head -c 600 /tmp/eval.json; echo; cat /tmp/eval.err", "description": "Run offline evaluation JSON", "timeoutMs": 300000}`

  ```
exit=0
{
 "version": "0.1.0",
 "gold": {
  "nom": "vivant (hand + reel + synthétique)",
  "gele": false,
  "phrases": 612,
  "tokens": 3179,
  "cibles_attachement": 239
 },
 "heuristique": {
  "bloc": "heuristique",
  "phrases": 612,
  "pos": {
   "exactitude": 0.8625,
   "exactitude_ferme": 0.9373,
   "exactitude_ouvert": 0.7918,
   "tokens": 3179,
   "confusions": {
    "ADJ": {
     "ADJ": 65,
     "NOUN": 65,
     "VERB": 4
    },
    "ADV": {
     "ADV": 131,
     "NOUN": 7,
     "PREP": 1,
     "ADJ": 1,
     "?": 1
    },
    "AUX": {
     "PREP": 4,
     "AUX": 119,
     "?": 3,
     "NOUN":
  ```

- **bash** `{"command": "grep -n \"cache\\|class DeepSeek\\|def demande\\|DEEPSEEK\\|url\\|environ\" tools/llm/deepseek.py | head -60", "description": "Inspect DeepSeek client cache"}`

  ```
14:dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
15:paquet externe : `urllib` suffit.
18:- `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
19:- `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
20:- `DEEPSEEK_MODEL` (ou `DSH_MODEL`) : `deepseek-chat` par défaut ;
21:- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages
27:    DEEPSEEK_API_KEY=... python3 tools/llm/deepseek.py --prompt ... --json
39:import urllib.error
40:import urllib.request
44:CACHE_DEFAUT = RACINE / "data" / "deepseek" / "cache"
66:    cache: bool = False
74:    """La clé, sans jamais l'écrire : variable d'environnement ou fichier 0600.
76:    `DEEPSEEK_API_KEY` / `DSH_API_KEY` d'abord ; sinon `DEEPSEEK_KEY_FILE` /
80:    for var in ("DEEPSEEK_API_KEY", "DSH_API_KEY"):
81:        v = os.environ.get(var)
84:    for var in ("DEEPSEEK_KEY_FILE", "DSH_KEY_FILE"):
85:        chemin = os.environ.get(var)
96:def _cache_cle(modele: str, messages: list[dict], temperature: float,
104:def _http(url: str, entetes: dict[str, str], corps: bytes, timeout: float) -> dict:
105:    requete = urllib.request.Requ
… [2332 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr=json.load(open('/tmp/eval.json'))\nh=r['heuristique']\nprint('phrases',r['gold']['phrases'],'cibles',r['gold']['cibles_attachement'])\nprint('POS',h['pos']['exactitude'])\nprint('F1',h['syntagme']['f1'],'P',h['syntagme']['precision'],'R',h['syntagme']['r … [377 caractères tronqués]`

  ```
phrases 612 cibles 239
POS 0.8625
F1 0.7902 P 0.786 R 0.7944
tete 0.9029
att exact 0.9958 couverture 0.9958 labels 238 cibles 239
reel {'phrases': 452, 'pos': 0.8891, 'f1': 0.7906, 'attachement': 183, 'couverture': 0.9946}
lineaire 0.8144 {'exact': 224, 'labels': 224, 'couverture': 0.9372}
  ```

- **bash** `{"command": "timeout 90 python3 tools/drave.py analyser \"Le chat dort.\" --tagger; echo \"exit=$?\"", "description": "Test tagger with live API call", "timeoutMs": 120000}`

  ```
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=0 · cache=1 · tokens=0 · latence=0.0 s
exit=0
  ```

- **bash** `{"command": "ls reports/ | grep -i \"exemple\\|rejou\" ; echo ---; ls data/deepseek/cache | wc -l; du -sh data/deepseek/cache 2>/dev/null", "description": "Find example reports and cache size"}`

  ```
pensee-parite-drvm-native-rejoue.json
rapport-exemples-rejoues.json
rapport-exemples-rejoues.md
rapport-pensee-parite-drvm-native-rejoue.md
---
3759
15M	data/deepseek/cache
  ```

- **bash** `{"command": "ls reports/*exemple* reports/*rejou* 2>/dev/null; echo ---; grep -n \"exemples\\|exemple\" reports/INDEX.md reports/README.md | head -30", "description": "Search report indexes for examples"}`

  ```
reports/pensee-parite-drvm-native-rejoue.json
reports/rapport-exemples-rejoues.json
reports/rapport-exemples-rejoues.json
reports/rapport-exemples-rejoues.md
reports/rapport-exemples-rejoues.md
reports/rapport-pensee-parite-drvm-native-rejoue.md
---
reports/INDEX.md:183:| [rapport-exemples-rejoues.md](rapport-exemples-rejoues.md) | J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec |
reports/README.md:25:| [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md) | **B13** — les 5 exemples de la doc |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-rejoues.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-rejoues.md</path>
<type>file</type>
<content>
1: # J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : **J11.1** · **Date** : 2026-11-14 ·
4: > **Verdict** : ✅
5: > **Cinq blocs rejoués** avec le code courant, **4 corrigés**, **1 identique** : la ponctuation
6: > finale entre dans le POS (`g001`, `r241`), le refus sort en **3**, et **`r035` est désormais
7: > prédit** — span `REL [9:24] « she talks about »` et cible `film`, exactement le gold.
8: > **Le chiffre.** F1 syntagmes **0,7902** ; POS **0,8625** (fermé 0,9373, ouvert 0,7918) ;
9: > attachement **238/238 labels** (238/239 cibles, **0,9958**). Le mandat porte encore **237/238** :
10: > c'est l'état d'avant `s065` (J6.2), qui a ajouté un label **sans toucher un span** — F1 inchangé.
11: > **Dispositif** : [`docs/produit/exemples.md`](../docs/produit/exemples.md) (les 5 blocs),
12: > [`tools/drave.py`](../tools/drave.py) 0.1.0, [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
13: > `jq` ; mesure par `python3 tools/drave.py evaluer --j
… [8841 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr=json.load(open('reports/rapport-exemples-rejoues.json'))\nprint(json.dumps(r,ensure_ascii=False,indent=1)[:3000])\nPY", "description": "Inspect existing replay report JSON"}`

  ```
{
 "tache": "J11.1",
 "titre": "Les cinq exemples de la doc produit rejoués",
 "date": "2026-11-14",
 "head": "a6808c5edf741ea59d45602fdfeee0916488beaf",
 "code": {
  "cli": "drave 0.1.0",
  "schema": 2,
  "commande": "python3 tools/drave.py"
 },
 "gold": {
  "nom": "vivant (hand + reel + synthétique)",
  "gele": false,
  "phrases": 612,
  "tokens": 3179,
  "cibles_attachement": 239
 },
 "mesure": {
  "pos": {
   "exactitude": 0.8625,
   "ferme": 0.9373,
   "ouvert": 0.7918,
   "tokens": 3179
  },
  "syntagmes": {
   "f1": 0.7902,
   "precision": 0.786,
   "rappel": 0.7944,
   "tp": 1480,
   "fp": 403,
   "fn": 383,
   "tete_f1": 0.9029
  },
  "attachement": {
   "labels": 238,
   "cibles": 239,
   "exact": 238,
   "exact_taux": 0.9958,
   "couverture": 0.9958,
   "par_langue": {
    "fr": {
     "cibles": 151,
     "labels": 151,
     "exact": 151,
     "topk": 149,
     "exact_taux_span": 1.0
    },
    "en": {
     "cibles": 88,
     "labels": 87,
     "exact": 87,
     "topk": 87,
     "exact_taux_span": 1.0
    }
   }
  },
  "note": "Le mandat porte 237/238 ; l'etat courant est 238/238 labels depuis la regle s065 (J6.2). 238/239 cibles."
 },
 "blocs": [
  {
   "id": "1",
   "c
… [1800 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"tagger\\|reel\\|exemple\" docs/produit/README.md | head -40; echo ---; wc -l docs/produit/README.md", "description": "Search product notice for tagger and reel sections"}`

  ```
11:> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
33:aucun accès réseau **par défaut** (le tagger en option, lui, appelle l'API DeepSeek, § 3.7). Les
50:| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger` |
72:**gelé 602** (0,7882, 234/239) et le **réel 452** (`--reel` : POS **0,8891**, F1 **0,7906**,
76:## 3. Comment l'utiliser — cinq exemples réels
80:[`exemples.md`](exemples.md).
120:`union: true`, à filtrer pour une lecture unique (voir [`exemples.md`](exemples.md) § 2).
129:gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement
173:gold réel (`hand` + `reel`) donne encore l'anglais devant (POS 94,51 contre 84,08 ; F1 86,56
362:### 3.6 bis La base honnête — `--reel`
365:python3 tools/drave.py evaluer --reel
368:`--reel` mesure les **452 phrases réelles** (main + corpus), sans les 160 synthétiques : POS
372:### 3.7 Le tagger en option — `--tagger`
375:python3 tools/drave.py analyser "Le chat dort." --tagger
376:python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
377
… [2470 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"D1\\|exemples\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -40", "description": "Find task D1 in state and roadmap"}`

  ```
docs/pilotage/en-cours.md:64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)).
docs/pilotage/roadmap.md:56:D1–D20, rejets R1–R30, échecs, reste — est dans
docs/pilotage/roadmap.md:59:**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
docs/pilotage/roadmap.md:65:[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**
docs/pilotage/roadmap.md:143:schéma v2, restitution v1, 50 textes, 5 exemples, fr/en), tagger (**0,9475, +8,49**), Panini
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 180}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
1: # La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers
2: 
3: > **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
4: > L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
5: > contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
6: >
7: > **Détail et histoire** : l'ancien plan [A/B](../theorie/glossaire/entrees/a-b.md) est archivé dans
8: > [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
9: > [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
10: > dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
11: > [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).
12: 
13: ## Comment lire cette roadmap
14: 
15: - **Les états** : ✅ m
… [24519 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 04 h 50 HNE (bilan de la nuit écrit)**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
11: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
12: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.
13: - **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
14: - **État** : **en pause** depuis le 05/11 (dernier heartbeat) ; la clôture J14.1 est portée par `e181ce02`.
15: - **Bloquants** : aucun.
16: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
17: 
18: ## Sessions en cours
19: 
20: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
21: > [`journal/sessions/`](../.
… [9524 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"D1\\b\\|D1 \\|exemples\\|tagger\\|reel\" tools/chantier/plan.json | head -60", "description": "Search current work plan for D1"}`

  ```
171:   "titre": "Coordination R — le tagger sur 612",
172:   "mandat": "Tâche J4.3 : la coordination R — décider le tagger POS sur le gold 612 via l'API DeepSeek (clé absente). Fiche `reports/rapport-coordination-r.md` + JSON : le coût (~1 200 appels, ~360 k tokens, ~20 min), la décision (mesure < +2 pts → négatif nommé ; ≥ +5 → intégrer), la commande exacte avec la clé.",
313:   "titre": "Le produit — les exemples rejoués",
314:   "mandat": "Tâche J11.1 : rejoue les 5 blocs de `docs/produit/exemples.md`, corrige les sorties, fiche `reports/rapport-exemples-rejoues.md`, commit.",
318:     "commande": "test -f reports/rapport-exemples-rejoues.md && echo FICHE-OK",
452:   "mandat": "Tâche C3 : la coordination R — propose et mesure l'extension du gold réel (le « gold 200+ » des fiches R) : prends 50 phrases **réelles** (hand + reel) que l'heuristique rate, écris la fiche `reports/rapport-gold-reel-50.md` + JSON (les erreurs d'attachement par type, les candidats à annoter), sans modifier le gold (S/D territory : le gold est à S).",
456:     "commande": "test -f reports/rapport-gold-reel-50.md && echo FICHE-OK",
501:   "id": "D1",
503:   "titre": "Les exemples avec le tagger et la base 
… [819 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-nuit.md", "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-nuit.md</path>
<type>file</type>
<content>
1: # Le bilan de la nuit du 14 au 15/11 — le tagger, la base honnête, la phase C/B
2: 
3: > **Ce que ce bilan est.** La synthèse de la nuit (23 h 30 → 04 h 45) : les décisions exécutées
4: > (1A → 6A), les mesures, les négatifs, et l'état du dépôt. **Aucune mesure nouvelle** n'est
5: > revendiquée : chaque chiffre renvoie à sa fiche.
6: 
7: ## 1. Le produit (6A)
8: 
9: | chantier | résultat | fiche |
10: |---|---|---|
11: | **le tagger en option** (`--tagger`) | POS **95,75 %** sur 612 (+9,5), **95,00 %** sur le réel 452 (+6,1) ; **1 appel**/phrase ; `PONCT` restitué ; ~0,02 $ | [`rapport-tagger-option.md`](rapport-tagger-option.md) |
12: | **la base honnête** (`--reel`) | 452 phrases : POS **88,91 %**, F1 **79,06 %**, attachement **99,46 %** ; publiée à côté du global | [`rapport-base-reelle.md`](rapport-base-reelle.md) |
13: | **les tests** | 14 tests tagger (0 réseau) + 20 tests produit ; porte produit **verte** | — |
14: 
15: ## 2. La coordination (C)
16: 
17: | tâche | résultat | fiche |
18: |---|---|---|
19: | **N2** | la commande **validée** : `--rope --cana
… [2093 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\n# find structure\nprint(type(p), p.keys() if isinstance(p,dict) else len(p))\nPY", "description": "Inspect plan JSON structure"}`

  ```
<class 'dict'> dict_keys(['nom', 'principe', 'taches'])
  ```

- **bash** `{"command": "sed -n '495,540p' tools/chantier/plan.json", "description": "Read D1 plan block"}`

  ```
"commande": "test -f reports/rapport-cic-v2.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    }
   ]
  },
  {
   "id": "D1",
   "jour": 15,
   "titre": "Les exemples avec le tagger et la base réelle",
   "mandat": "Tâche D1 : les exemples de `docs/produit/exemples.md` — ajoute 3 exemples avec `--tagger` (la sortie réelle avec la clé, le coût affiché) et 2 avec `--reel` (la base honnête), et vérifie que les sorties collent au code courant (F1 0,7902, 238/239, schéma v2). Fiche `reports/rapport-exemples-tagger.md` + JSON, commit.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-exemples-tagger.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
    {
     "commande": "bash tools/porte-produit.sh 2>&1 | tail -1",
     "attendu": "verte"
    }
   ]
  },
  {
   "id": "D2",
   "jour": 15,
   "titre": "La restitution v2 — les rôles",
   "mandat": "Tâche D2 : la restitution v2 — au-delà de la surface exacte (v0) et de la forme canonique (v1), restitue les **rôles** (agent, prédicat, lieu) dans une forme lisible et mesure la fidélité des rôles sur les 46 textes de la v0 ; fiche `reports/rapport-restitution-v2.md` + JSON, tests, commit. Si les
… [816 caractères tronqués]
  ```

- **bash** `{"command": "rm -rf /tmp/drave-exemples-tagger-cache && mkdir -p /tmp/drave-exemples-tagger-cache\nDEEPSEEK_CACHE=/tmp/drave-exemples-tagger-cache timeout 120 python3 tools/drave.py analyser \"Le chat dort.\" --tagger > /tmp/tag1.out 2> /tmp/tag1.err; echo \"exit=$?\"; cat /tmp/tag1.out; cat /tmp/ta … [74 caractères tronqués]`

  ```
exit=0
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.1 s
  ```

- **bash** `{"command": "DEEPSEEK_CACHE=/tmp/drave-exemples-tagger-cache timeout 120 python3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" --tagger > /tmp/tag2.out 2> /tmp/tag2.err; echo \"exit=$?\"; cat /tmp/tag2.out; cat /tmp/tag2.err", "description": "Fresh-cache tagger on g011", "timeout … [12 caractères tronqués]`

  ```
exit=0
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 43 étiquettes · unités sémantiques=3 (48.6% du texte)
POS  Le/DET livre/NOUN que/PRON j'ai/PRON lu/VERB est/AUX intéressant/ADJ ./PONCT
SYNTAGMES
  GN   [0:8]    Le livre                     rôle=agent     → intéressant
  REL  [9:20]   que j'ai lu                  rôle=qualite   → livre
  REL  [9:36]   que j'ai lu est intéressant  rôle=qualité   → livre
  GV   [21:36]  est intéressant              rôle=predicat  → livre
PRAGMATIQUE
  phrase [0:37] déclarative · acte=assertion · négation=non · modalité=non · double sens=oui
COUVERTURE  (confiance max par niveau)  graphème=0.99 · morphème=0.32 · mot=0.98 · pos=0.95 ·
            syntagme=0.55 · phrase=0.85 · discours=0.55 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=157 · latence=1.5 s
  ```

- **bash** `{"command": "sleep 3; DEEPSEEK_CACHE=/tmp/drave-exemples-tagger-cache timeout 120 python3 tools/drave.py analyser \"The day when we left was beautiful.\" --langue en --tagger > /tmp/tag3.out 2> /tmp/tag3.err; echo \"exit=$?\"; cat /tmp/tag3.out; cat /tmp/tag3.err", "description": "Fresh-cache tagger … [31 caractères tronqués]`

  ```
exit=0
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=en script=Latn source=cascade · 38 étiquettes · unités sémantiques=3 (45.7% du texte)
POS  The/DET day/NOUN when/PRON we/PRON left/VERB was/AUX beautiful/ADJ ./PONCT
SYNTAGMES
  GN   [0:7]    The day        rôle=groupe nominal  → beautiful
  REL  [8:20]   when we left   rôle=qualité         → day
  GV   [21:34]  was beautiful  rôle=prédicat        → —
PRAGMATIQUE
  phrase [0:35] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · morphème=0.32 · mot=0.98 · pos=0.95 ·
            syntagme=0.35 · phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=154 · latence=1.1 s
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\ng=json.load(open('tools/tests/linguistique/gold.json'))\nprint(type(g), (g.keys() if isinstance(g,dict) else len(g)))\nPY", "description": "Inspect gold JSON structure"}`

  ```
<class 'dict'> dict_keys(['version', 'phrases', 'note'])
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\ng=json.load(open('tools/tests/linguistique/gold.json'))\nidx={p['id']:p for p in g['phrases']}\nfor i in ('g001','g011','r241','g017','r035'):\n    p=idx.get(i)\n    print('=====',i)\n    print(json.dumps(p,ensure_ascii=False,indent=1))\nPY", "description" … [42 caractères tronqués]`

  ```
===== g001
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
===== g011
{
 "id": "g011",
 "langue": "fr",
 "texte": "Le livre que j'ai lu est intéressant.",
 "mots": [
  {
   "texte": "Le",
   "pos": "DET",
   "debut": 0,
   "fin": 2
  },
  {
   "texte": "livre",
   "pos": "NOUN",
   "debut": 3,
   "fin": 8
  },
  {
   "texte": "que",
   "pos": "CONJ",
   "debut": 9,
   "fin": 12
  },
  {
   "texte": "j'ai",
   "pos": "PRON",
   "debut": 13,
   "fin": 17
  },
  {
   "texte": "lu",
   "pos": "VERB",
   "debut": 18,
   "fin": 20
  },
  {
   "texte": "est",
   "pos": "AUX",
   "debut": 21,
   "fin": 24
  },
  {
   "texte": "intéressant",
   "pos": "ADJ",
   "debut": 25,
   "fin": 36
  }
 ],
 "segme
… [1519 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor fn in ('tools/tests/linguistique/gold_reel.json','tools/tests/linguistique/gold.json'):\n    g=json.load(open(fn))\n    print(fn, list(g.keys()) if isinstance(g,dict) else type(g))\n    phrases = g.get('phrases', g) if isinstance(g,dict) else g\n    id … [230 caractères tronqués]`

  ```
tools/tests/linguistique/gold_reel.json ['version', 'source', 'note', 'phrases']
===== r241
{
 "id": "r241",
 "langue": "en",
 "texte": "The day when we left was beautiful.",
 "mots": [
  {
   "texte": "The",
   "pos": "DET",
   "debut": 0,
   "fin": 3
  },
  {
   "texte": "day",
   "pos": "NOUN",
   "debut": 4,
   "fin": 7
  },
  {
   "texte": "when",
   "pos": "PRON",
   "debut": 8,
   "fin": 12
  },
  {
   "texte": "we",
   "pos": "PRON",
   "debut": 13,
   "fin": 15
  },
  {
   "texte": "left",
   "pos": "VERB",
   "debut": 16,
   "fin": 20
  },
  {
   "texte": "was",
   "pos": "AUX",
   "debut": 21,
   "fin": 24
  },
  {
   "texte": "beautiful",
   "pos": "ADJ",
   "debut": 25,
   "fin": 34
  }
 ],
 "segments": [
  {
   "type": "GN",
   "texte": "The day",
   "role": "patient",
   "debut": 0,
   "fin": 7
  },
  {
   "type": "REL",
   "texte": "when we left",
   "role": "temps",
   "debut": 8,
   "fin": 20,
   "cibles": [
    "day"
   ],
   "cible": "day"
  },
  {
   "type": "GV",
   "texte": "was",
   "role": "prédicat",
   "debut": 21,
   "fin": 24
  },
  {
   "type": "ADJ",
   "texte": "beautiful",
   "role": "attribut",
   "debut": 25,
   "fin": 34
  }
 ],
 "pragma": {
  "a
… [1169 caractères tronqués]
  ```

- **bash** `{"command": "for t in \"Le chat dort.|fr\" \"Le livre que j'ai lu est intéressant.|fr\" \"The day when we left was beautiful.|en\"; do IFS='|' read -r texte langue <<< \"$t\"; echo \"=== $texte\"; python3 tools/drave.py analyser \"$texte\" --langue \"$langue\" --json | python3 -c 'import json,sys; a … [206 caractères tronqués]`

  ```
=== Le chat dort.
=== Le livre que j'ai lu est intéressant.
=== The day when we left was beautiful.
[stderr]
  File "<string>", line 1
    import json,sys; a=json.load(sys.stdin); print(" ".join(f"{e[\"valeur\"]}/{e[\"type\"]}" for e in a["etiquettes"] if e["niveau"]=="pos"))
                                                                  ^
SyntaxError: unexpected character after line continuation character
  File "<string>", line 1
    import json,sys; a=json.load(sys.stdin); print(" ".join(f"{e[\"valeur\"]}/{e[\"type\"]}" for e in a["etiquettes"] if e["niveau"]=="pos"))
                                                                  ^
SyntaxError: unexpected character after line continuation character
  File "<string>", line 1
    import json,sys; a=json.load(sys.stdin); print(" ".join(f"{e[\"valeur\"]}/{e[\"type\"]}" for e in a["etiquettes"] if e["niveau"]=="pos"))
                                                                  ^
SyntaxError: unexpected character after line continuation character
[exit code: 1]
  ```

- **bash** `{"command": "for f in /tmp/tag1 /tmp/tag2 /tmp/tag3; do echo \"=== $f\"; done; ls -l data/deepseek/cache | head -3", "description": "Placeholder check outputs"}`

  ```
=== /tmp/tag1
=== /tmp/tag2
=== /tmp/tag3
total 15100
-rw-r--r--. 1 stephane stephane 1106  4 nov 13:19 001218f9ae808eb41920978467eec88209b2ebdeb43cf98679fbf257f6a9272a.json
-rw-r--r--. 1 stephane stephane  998  4 nov 12:45 00155c45c77a76284ad6df1774ad674f9e8287450a065cb0701cace428db6165.json
[stderr]
ls: write error: Broken pipe
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json > /tmp/h1.json\npython3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" --json > /tmp/h2.json\npython3 tools/drave.py analyser \"The day when we left was beautiful.\" --langue en --json > /tmp/h3.json\npython3 -  … [280 caractères tronqués]`

  ```
1 version 2 POS Le/DET chat/NOUN dort/VERB ./PONCT
2 version 2 POS Le/DET livre/NOUN que/PRON j'ai/PRON lu/NOUN est/AUX intéressant/ADJ ./PONCT
3 version 2 POS The/DET day/NOUN when/CONJ we/PRON left/VERB was/AUX beautiful/ADJ ./PONCT
  ```

- **bash** `{"command": "timeout 300 python3 tools/drave.py evaluer --reel > /tmp/reel1.out 2> /tmp/reel1.err; echo \"exit=$?\"; cat /tmp/reel1.out; cat /tmp/reel1.err", "description": "Run evaluer --reel text output", "timeoutMs": 330000}`

  ```
exit=0
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
  ```

- **bash** `{"command": "timeout 300 python3 tools/drave.py evaluer --reel --json > /tmp/reel1.json 2> /tmp/reel1j.err; echo \"exit=$?\"; python3 - <<'PY'\nimport json\nr=json.load(open('/tmp/reel1.json'))\nprint(json.dumps({\n 'version':r['version'],\n 'gold':r['gold'],\n 'reel':r['reel'],\n 'heuristique': {\n … [518 caractères tronqués]`

  ```
exit=0
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
 "heuristique": {
  "pos": {
   "exactitude": 0.8891,
   "exactitude_ferme": 0.9294,
   "exactitude_ouvert": 0.8466,
   "tokens": 2480
  },
  "syntagme": {
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
}
  ```

- **bash** `{"command": "DEEPSEEK_CACHE=/tmp/drave-exemples-tagger-cache python3 tools/drave.py analyser \"Le chat dort.\" --tagger --json > /tmp/tag1.json 2>/tmp/tag1j.err; echo exit=$?; cat /tmp/tag1j.err\nDEEPSEEK_CACHE=/tmp/drave-exemples-tagger-cache python3 tools/drave.py analyser \"Le livre que j'ai lu e … [678 caractères tronqués]`

  ```
exit=0
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=1 · tokens=0 · latence=0.0 s
exit=0
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=1 · tokens=0 · latence=0.0 s
exit=0
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=1 · tokens=0 · latence=0.0 s
1 drave.annotation 2 cascade POS: Le/DET chat/NOUN dort/VERB ./PONCT
   cout: {'octets': 13, 'etiquettes': 19}
2 drave.annotation 2 cascade POS: Le/DET livre/NOUN que/PRON j'ai/PRON lu/VERB est/AUX intéressant/ADJ ./PONCT
   cout: {'octets': 38, 'etiquettes': 42}
3 drave.annotation 2 cascade POS: The/DET day/NOUN when/PRON we/PRON left/VERB was/AUX beautiful/ADJ ./PONCT
   cout: {'octets': 35, 'etiquettes': 37}
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 120, "offset": 350}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
350: `--banc reports/pensee-fiabilite-produit.json` rejoue les **50 textes libres** : **46/46
351: surfaces exactes**, miroir strict **0,1087**, contrôle négatif **46/46**. C'est un **codec de
352: surface**, pas un décodeur neuronal : il ne prouve pas la fidélité sémantique. La fiche est
353: [`rapport-restitution-v0.md`](../../reports/rapport-restitution-v0.md).
354: 
355: `--canonique` ajoute la **forme canonique v1** (segments + rôles + cibles) : **46/46** contre
356: la source **canonisée**, mais le **miroir strict reste 0,1087** — la forme n'est pas la
357: surface, et elle tombe à **1/46** si on la compare à la source brute. Les **395 segments**
358: portent **395 rôles** et **315 cibles** (315 résolues, 313 dans un autre segment) ; la
359: stabilité structurelle est **18/46**. Fiche
360: [`rapport-restitution-v1.md`](../../reports/rapport-restitution-v1.md).
361: 
362: ### 3.6 bis La base honnête — `--reel`
363: 
364: ```bash
365: python3 tools/drave.py evaluer --reel
366: ```
367: 
368: `--reel` mesure les **452 phrases réelles** (main + corpus), sans les 160 syn
… [6952 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md</path>
<type>file</type>
<content>
1: # Ce qu'un résultat doit porter
2: 
3: > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
4: > résultats, ou un message de commit.
5: 
6: ## Les cinq pièces d'un résultat
7: 
8: 1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
9:    [porte](../theorie/glossaire/entrees/porte.md)) ;
10: 2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
11:    mesure pas ;
12: 3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
13:    quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
14:    grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire co
… [2865 caractères tronqués]
  ```

- **bash** `{"command": "ls journal/ | tail -20; echo ---; ls journal/2026-11-15 2>/dev/null || true; echo ---; find journal -maxdepth 2 -type f -newermt '2026-11-14' | head -30", "description": "Inspect journal layout"}`

  ```
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
2026-11-15
README.md
sessions
THEMES.md
---
distribue.md
docs.md
mesures.md
portes.md
README.md
---
journal/sessions/MANIFEST.md
journal/README.md
journal/THEMES.md
journal/2026-11-14/docs.md
journal/2026-11-14/memoire.md
journal/2026-11-14/portes.md
journal/2026-11-14/README.md
journal/2026-11-14/distribue.md
journal/2026-11-14/moteur.md
journal/2026-11-14/mesures.md
journal/2026-11-15/portes.md
journal/2026-11-15/mesures.md
journal/2026-11-15/docs.md
journal/2026-11-15/distribue.md
journal/2026-11-15/README.md
  ```

- **bash** `{"command": "sed -n '1,120p' reports/README.md; echo ====; sed -n '1,40p' reports/INDEX.md; echo ====; sed -n '170,195p' reports/INDEX.md", "description": "Read reports indexes"}`

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
| [`rapport-bilan-nuit.md`](rapport-bilan-nuit.md) | **Bilan** — la nuit du 14 au 15/11 : le tagger, la base honnête, la phase C/B |
| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
| [`rapport-protocole-date.md`](rapport-protoc
… [19088 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' journal/2026-11-15/README.md; echo ====; sed -n '1,80p' journal/2026-11-15/mesures.md; echo ====; sed -n '1,60p' journal/2026-11-15/docs.md", "description": "Read today's journal entries"}`

  ```
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**12 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 3 | [distribue.md](distribue.md) |
| docs | 3 | [docs.md](docs.md) |
| mesures | 5 | [mesures.md](mesures.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 347.9 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTI
… [8652 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/index_reports.py --help 2>&1 | head -30; echo ---; python3 tools/journal_auto.py --help 2>&1 | head -30", "description": "Check index and journal tool usage"}`

  ```
usage: index_reports.py [-h] [--verifier] [--aide]

Génère reports/INDEX.md (déterministe).

options:
  -h, --help  show this help message and exit
  --verifier  ne réécrit rien : compare l'index au disque, sort 1 s'il est
              périmé
  --aide      affiche l'aide et sort
---
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

- **bash** `{"command": "date; git log -1 --format='%H %ad %cd' --date=iso", "description": "Check system and commit dates"}`

  ```
dim 15 nov 2026 04:38:55 EST
ee04ea9134d8f9fab62c8728fd1ab7857ded4dd3 2026-11-15 04:33:07 -0500 2026-11-15 04:33:07 -0500
  ```

- **bash** `{"command": "git diff --stat; echo ---; git status --short", "description": "Inspect uncommitted change scope"}`

  ```
reports/pensee-coherence-fiches-v7.json |  19 +
 reports/pensee-dev-test-v10.json        |   2 +-
 reports/pensee-quatre-modes.json        | 734 ++++++++++++++++++--------------
 reports/rapport-audit-v7.md             |   6 +-
 reports/rapport-coherence-fiches-v7.md  |  17 +-
 reports/rapport-dev-test-v10.md         |   2 +-
 reports/rapport-pensee-v12.md           |   4 +-
 reports/rapport-spans-chunker.md        |  13 +-
 tools/chantier/plan.json                | 121 ++++++
 9 files changed, 581 insertions(+), 337 deletions(-)
---
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
  ```

- **bash** `{"command": "sed -n '1,200p' tools/revue_documentation.py", "description": "Inspect documentation review checks"}`

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
… [6605 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nr=pathlib.Path('reports')\nprint('md',len(list(r.glob('*.md'))),'json',len(list(r.glob('*.json'))))\nprint('docs',len([p for p in pathlib.Path('docs').rglob('*.md') if 'archive' not in p.parts and p.name!='README.md' and not (p.parent.name=='entrees' an … [240 caractères tronqués]`

  ```
md 742 json 836
docs 123
portes 85
chapitres 8
  ```

- **bash** `{"command": "sed -n '1,160p' tools/porte-produit.sh", "description": "Inspect product gate script"}`

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
… [3266 caractères tronqués]
  ```

- **bash** `{"command": "jq '{version, gold, reel,\n     pos: (.heuristique.pos | {exactitude, exactitude_ferme, exactitude_ouvert, tokens}),\n     f1: (.heuristique.syntagme | {f1, precision, rappel}),\n     attachement: (.heuristique.attachement | {cibles, labels, exact, exact_taux, couverture}),\n     contro … [88 caractères tronqués]`

  ```
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

- **bash** `{"command": "jq '{schema, version, langue, script, refus,\n     pos: [.etiquettes[] | select(.niveau==\"pos\") | {valeur, type, debut, fin, confiance, ouvert:.meta.ouvert}]}' /tmp/tag2.json", "description": "Produce exact tagger JSON POS extract"}`

  ```
{
  "schema": "drave.annotation",
  "version": 2,
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "pos": [
    {
      "valeur": "Le",
      "type": "DET",
      "debut": 0,
      "fin": 2,
      "confiance": 0.6,
      "ouvert": null
    },
    {
      "valeur": "livre",
      "type": "NOUN",
      "debut": 3,
      "fin": 8,
      "confiance": 0.6,
      "ouvert": null
    },
    {
      "valeur": "que",
      "type": "PRON",
      "debut": 9,
      "fin": 12,
      "confiance": 0.6,
      "ouvert": null
    },
    {
      "valeur": "j'ai",
      "type": "PRON",
      "debut": 13,
      "fin": 17,
      "confiance": 0.6,
      "ouvert": null
    },
    {
      "valeur": "lu",
      "type": "VERB",
      "debut": 18,
      "fin": 20,
      "confiance": 0.6,
      "ouvert": null
    },
    {
      "valeur": "est",
      "type": "AUX",
      "debut": 21,
      "fin": 24,
      "confiance": 0.6,
      "ouvert": null
    },
    {
      "valeur": "intéressant",
      "type": "ADJ",
      "debut": 25,
      "fin": 36,
      "confiance": 0.6,
      "ouvert": null
    },
    {
      "valeur": ".",
      "type": "PONCT",
      "debut": 36,
      "fin": 37,
      "confiance": 0.95,
 
… [32 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"§\" docs/produit/exemples.md", "description": "Find section cross-references"}`

  ```
194:(voir § 5).
311:  `partition:.meta.partition, alternative:.meta.alternative` (voir le `FILTRE` du § 0).
660:   est désormais prédit (§ 5).
668:n'est pas publié comme schéma — c'est un des manques du CLI (notice § 7). Le schéma de
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --help 2>&1 | head -40", "description": "Check schema verifier usage"}`

  ```
usage: verifier_schema_produit.py [-h] [--json] [--gold N] [--aide]

Valide drave.annotation contre le schéma de sa version.

options:
  -h, --help  show this help message and exit
  --json      détail JSON des cas
  --gold N    valide aussi les N premières phrases du gold (0 = aucune)
  --aide      affiche cette aide et sort
  ```

- **bash** `{"command": "sed -n '1,180p' tools/verifier_schema_produit.py", "description": "Inspect schema verifier implementation"}`

  ```
#!/usr/bin/env python3
"""verifier_schema_produit.py — valide une annotation `drave.annotation` contre le schéma de sa version.

Deux schémas sont publiés (Draft 2020-12) :

- `tools/schemas/drave-annotation-v1.json` — le contrat d'origine (version 1) ;
- `tools/schemas/drave-annotation-v2.json` — le contrat courant (version 2) : il ajoute
  `meta.partition` et `meta.alternative`, les deux champs qui documentent les syntagmes qui se
  chevauchent.

Le vérificateur lit `version` dans l'annotation et choisit le schéma correspondant : une
annotation v1 reste donc **lue** et validée par le schéma v1. Il compile les schémas une fois,
puis valide les annotations de cas choisis : français, anglais, refus (texte vide), entrée non
textuelle, texte très long, plus une annotation v1 de rétro-compatibilité. Il ne dépend que de
`fastjsonschema` (sinon il se rabat sur une validation minimale des champs obligatoires et de la
version). Un **contrôle négatif** vérifie que le schéma v2 refuse bien une annotation v1.

Usage :
    python3 tools/verifier_schema_produit.py              # 5 cas v2 + 1 cas v1, sortie 0/1
    python3 tools/verifier_schema_produit.py --json       # le détail des cas
    pyt
… [5948 caractères tronqués]
  ```

- **bash** `{"command": "timeout 300 python3 tools/drave.py evaluer --par-langue --json > /tmp/eval_lang.json 2>/tmp/eval_lang.err; echo exit=$?; python3 - <<'PY'\nimport json\nr=json.load(open('/tmp/eval_lang.json'))\nfor lang,m in r.get('par_langue',{}).items():\n    print(lang, m['phrases'], 'POS', m['pos'][ … [254 caractères tronqués]`

  ```
exit=0
en 210 POS 0.9451 F1 0.8656 att 87 / 88 0.9886
fr 402 POS 0.8159 F1 0.7475 att 151 / 151 1.0
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"The film she talks about is out.\" --json > /tmp/r035.json; python3 tools/drave.py analyser \"\" --json > /tmp/vide.json; echo \"vide exit=$?\"; python3 - <<'PY'\nimport json\na=json.load(open('/tmp/r035.json'))\nprint('r035 version', a['version'], 'REL … [290 caractères tronqués]`

  ```
vide exit=3
r035 version 2 REL [('The film', 'out'), ('she talks about', 'film'), ('is out', None)]
vide drave.annotation 2 vide 0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor fn in ('reports/tagger-612.json','reports/pensee-tagger-option.json'):\n    try:\n        d=json.load(open(fn))\n        print('===',fn, list(d.keys())[:20])\n        for k in ('cout','cost','prix','tokens','modele'):\n            if k in d: print(k, j … [131 caractères tronqués]`

  ```
=== reports/tagger-612.json ['date', 'gold', 'modeles_renvoyes', 'modes', 'pos_par_source', 'seuils', 'refus', 'refus_detail', 'appels', 'api', 'latence_s', 'duree_totale_s', 'limites']
=== reports/pensee-tagger-option.json ['date', 'branche', 'decision', 'ligne_roadmap', 'option', 'mesure_20', 'mesure_612_reference', 'tests', 'limites', 'apres_15_11', 'base_reelle_452']
  ```

- **bash** `{"command": "grep -n \"0,0[0-9]\\|\\\\$ \\|dollar\\|prix\\|coût\" reports/rapport-coordination-r.md reports/tagger-612.json reports/pensee-tagger-option.json 2>/dev/null | head -40", "description": "Find dollar cost statements"}`

  ```
reports/rapport-coordination-r.md:10:> manque. Coût mesuré : **1 218 appels, 358 962 tokens, 21 min**, **~0,04 $** hors pointe.
reports/rapport-coordination-r.md:104:| **uniforme** | tirage uniforme sur les 12 classes | **0,0833** |
reports/rapport-coordination-r.md:111:## 3. Le protocole et le coût
reports/rapport-coordination-r.md:145:### 3.3 Le coût facturé
reports/rapport-coordination-r.md:148:0,003 / 0,006 $ par M, entrée **cache miss** 0,15 / 0,30 $ par M, sortie 0,60 / 1,20 $ par M
reports/rapport-coordination-r.md:155:| **hors pointe** (run à 03:00 UTC, samedi) | 0,0005 $ | 0,0262 $ | 0,0164 $ | **~0,043 $** |
reports/rapport-coordination-r.md:156:| **pointe** | 0,0009 $ | 0,0524 $ | 0,0328 $ | **~0,086 $** |
reports/rapport-coordination-r.md:158:Le run a eu lieu un **samedi 03:00 UTC** : **hors pointe**, donc **~0,04 $**. Pour **1 000
reports/rapport-coordination-r.md:159:phrases** : **~1 990 appels**, **~587 k tokens**, **~34 min** séquentielles, **~0,07 $** hors
reports/rapport-coordination-r.md:160:pointe (**~0,14 $** en pointe). Le POS seul coûterait **la moitié** (~609 appels, ~180 k tokens,
reports/rapport-coordination-r.md:260:4. **Coût** : ~0,07 $ et ~34 min par 1 
… [473 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '140,165p' reports/rapport-coordination-r.md; echo ====; python3 - <<'PY'\nimport json\nd=json.load(open('reports/tagger-612.json'))\nfor k in ('appels','api','latence_s','duree_totale_s'):\n    print(k, json.dumps(d[k],ensure_ascii=False)[:800])\nPY", "description": "Read cost d … [25 caractères tronqués]`

  ```
Le run 432 de référence (`pensee-quatre-modes-432-run2.json`) : **858 appels**, **254 454
tokens**, **807,6 s**, soit **1,986 appel/phrase**, **296,6 tokens/appel**, **0,941 s/appel**.
Le passage à 612 donne **1 218 appels**, **358 962 tokens**, **1 259,2 s** : la consigne était
juste à quelques pour cent.

### 3.3 Le coût facturé

Tarif public `deepseek-flash` au 2026-11-13 (hors pointe / pointe) : entrée **cache hit**
0,003 / 0,006 $ par M, entrée **cache miss** 0,15 / 0,30 $ par M, sortie 0,60 / 1,20 $ par M
([tarifs](https://api-docs.deepseek.com/quick_start/pricing)). Le run a consommé, d'après les
`usage` du cache : **155 136 tokens d'entrée en cache hit**, **174 822 en cache miss**,
**27 326 tokens de sortie** (totaux à ±0,5 % près, six prompts dupliqués).

| tarif | entrée hit | entrée miss | sortie | **total** |
|---|---:|---:|---:|---:|
| **hors pointe** (run à 03:00 UTC, samedi) | 0,0005 $ | 0,0262 $ | 0,0164 $ | **~0,043 $** |
| **pointe** | 0,0009 $ | 0,0524 $ | 0,0328 $ | **~0,086 $** |

Le run a eu lieu un **samedi 03:00 UTC** : **hors pointe**, donc **~0,04 $**. Pour **1 000
phrases** : **~1 990 appels**, **~587 k tokens**, **~34 min** séquentielles, **~0,07 $** hor
… [430 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-tagger-option.json'))\nprint(json.dumps(d.get('apres_15_11'),ensure_ascii=False,indent=1))\nprint(json.dumps(d.get('base_reelle_452'),ensure_ascii=False,indent=1))\nPY", "description": "Read updated tagger cost figures"}`

  ```
{
 "appels_par_phrase": 1,
 "ponct": "25/25",
 "pos_612": 0.9575,
 "delta": 0.095,
 "cout": {
  "appels": 609,
  "tokens": 22299,
  "latence_s": 155.636,
  "requetes": 159
 }
}
{
 "pos_heuristique": 0.8891,
 "pos_tagger": 0.95,
 "delta": 0.0609,
 "appels": 449,
 "cache": 449,
 "reseau": 0
}
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "old_string": "# Cinq exemples d'analyse, commentés\n\n> **Ce que ce document est.** Cinq exécutions **réelles** du produit, avec leur JSON commenté. Il\n> complète la notice [`README.md`](README.md) : la notic … [3706 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "old_string": "- `confiance` : **déclarée**, pas calibrée. 0,3 pour un NOUN ouvert, 0,92 pour un DET.\n- `meta.attachement` : `{segment, cible}` ; `cible` est une **chaîne**, pas un span.", "new_string": "- `co … [974 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "old_string": "## 6. Ce que ces exemples ne montrent pas", "new_string": "## 6. Le tagger en option — trois exécutions avec la clé\n\n> **Le dispositif.** Les trois commandes ci-dessous ont été lancées le **202 … [12012 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "offset": 930}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md</path>
<type>file</type>
<content>
930:     "tokens": 2480
931:   },
932:   "f1": {
933:     "f1": 0.7906,
934:     "precision": 0.8128,
935:     "rappel": 0.7695
936:   },
937:   "attachement": {
938:     "cibles": 184,
939:     "labels": 183,
940:     "exact": 183,
941:     "exact_taux": 0.9946,
942:     "couverture": 0.9946
943:   },
944:   "controle_negatif": {
945:     "nom": "cible exacte tirée au hasard dans le gold",
946:     "graine": 0,
947:     "cibles": 184,
948:     "exact_taux": 0.0
949:   }
950: }
951: ```
952: 
953: **Lecture.** `gold.nom` **nomme la base** mesurée, `gold.phrases: 452` et
954: `gold.cibles_attachement: 184` la bornent. `reel: null` est **attendu** : la base mesurée est
955: déjà la base réelle ; sans `--reel`, ce champ porte un objet (452 phrases, POS, F1,
956: attachement) calculé à côté du global. Les nombres sont **les mêmes** que dans la sortie
957: lisible : 0,8891, 0,7906, 0,9946. Attention : ce JSON est un **rapport d'évaluation**
958: (`version: "0.1.0"` est celle du CLI), pas une **annotation** : le schéma `drave.annotation`
959: v2 ne s'applique pas ici.
960: 
9
… [2520 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "old_string": "2. **Pas de neuronal** : tout vient de `Heuristique` (CPU) ; `MockNeuronal` est un contrat, pas un\n   tagger, et le CLI ne l'expose pas. La cascade 7B (0,9415) n'est pas un chemin livré.\n3. **P … [1790 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "old_string": "## 7. Où aller ensuite\n\n| si vous voulez… | allez à |\n|---|---|\n| **la notice d'usage** | [`README.md`](README.md) |\n| **le schéma du JSON (v2, v1)** | [`drave-annotation-v2.json`](../../too … [1700 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"^## \\|^### \" docs/produit/exemples.md", "description": "List section headings"}`

  ```
34:## 0. Comment lire les JSON
79:## 1. Une déclarative simple — `g001`
217:## 2. Un attachement de REL — `g011`
344:## 3. L'anglais et le marqueur ambigu — `r241`
500:## 4. Le refus — texte vide
552:## 5. L'échec autrefois connu — `r035`, désormais prédit
673:## 6. Le tagger en option — trois exécutions avec la clé
683:### 6.1 `g001` — le cas neutre
716:### 6.2 `g011` — `lu` redevient un verbe
798:### 6.3 `r241` — `when` redevient un pronom
832:### 6.4 Ce que les trois exemples mesurent — et ne mesurent pas
854:## 7. La base honnête — deux exécutions avec `--reel`
860:### 7.1 `evaluer --reel` — la sortie lisible
900:### 7.2 `evaluer --reel --json` — le contrat de la mesure
961:## 8. Ce que ces exemples ne montrent pas
984:## 9. Où aller ensuite
  ```

- **write** `{"file_path": "/tmp/verifier_d1.py", "content": "#!/usr/bin/env python3\n\"\"\"Vérifie les cinq nouveaux blocs de docs/produit/exemples.md contre le CLI courant.\"\"\"\nimport json\nimport pathlib\nimport re\nimport subprocess\nimport sys\n\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/G … [4601 caractères tronqués]`

  ```
<path>/tmp/verifier_d1.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "timeout 400 python3 /tmp/verifier_d1.py; echo \"exit=$?\"", "description": "Verify new doc blocks against current CLI", "timeoutMs": 430000}`

  ```
exit=1
[stderr]
Traceback (most recent call last):
  File "/tmp/verifier_d1.py", line 119, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/verifier_d1.py", line 81, in main
    raise RuntimeError(p.stderr)
RuntimeError: /bin/sh: -c: line 1: unexpected EOF while looking for matching `''
  ```

- **edit** `{"file_path": "/tmp/verifier_d1.py", "old_string": "        # le bloc JSON de 6.2\n        if titre == \"6.2\":\n            attendu_json = json.loads(sortie(doc, titre, \"**Sortie (réelle, extrait).**\"))\n            commande = (\n                f\"{sys.executable} tools/drave.py analyser {json.d … [1932 caractères tronqués]`

  ```
The file /tmp/verifier_d1.py has been updated successfully.
  ```

- **edit** `{"file_path": "/tmp/verifier_d1.py", "old_string": "    # --- le bloc --reel JSON\n    attendu = json.loads(sortie(doc, \"7.2\", \"**Sortie (réelle).**\"))\n    commande = (\n        f\"{sys.executable} tools/drave.py evaluer --reel --json | \"\n        \"jq '{version, gold, reel, \"\n        \"pos: … [1615 caractères tronqués]`

  ```
The file /tmp/verifier_d1.py has been updated successfully.
  ```

- **bash** `{"command": "timeout 400 python3 /tmp/verifier_d1.py; echo \"exit=$?\"", "description": "Re-run doc block verification", "timeoutMs": 430000}`

  ```
4/5 blocs reproduits
6.2: JSON différent
exit=1
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\na=json.load(open('/tmp/tag2.json'))\nfor v in ('lu','.'):\n    e=next(e for e in a['etiquettes'] if e['niveau']=='pos' and e['valeur']==v)\n    print(json.dumps(e,ensure_ascii=False,indent=1))\nPY", "description": "Show full POS objects including source"}`

  ```
{
 "niveau": "pos",
 "type": "VERB",
 "valeur": "lu",
 "debut": 18,
 "fin": 20,
 "source": "neuronal",
 "confiance": 0.6,
 "candidats": [],
 "langue": "und",
 "script": "Latn",
 "meta": {
  "modele": true
 }
}
{
 "niveau": "pos",
 "type": "PONCT",
 "valeur": ".",
 "debut": 36,
 "fin": 37,
 "source": "heuristique",
 "confiance": 0.95,
 "candidats": [],
 "langue": "fr",
 "script": "Latn",
 "meta": {
  "ouvert": false
 }
}
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "old_string": "  \"lu\": {\n    \"niveau\": \"pos\",\n    \"type\": \"VERB\",\n    \"valeur\": \"lu\",\n    \"debut\": 18,\n    \"fin\": 20,\n    \"confiance\": 0.6,\n    \"meta\": {\n      \"ouvert\": null\n   … [1863 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "old_string": "- `confiance` : **déclarée**, pas calibrée. 0,3 pour un NOUN ouvert, 0,92 pour un DET. Avec\n  `--tagger`, les POS neuronaux portent **0,60** : c'est le **seuil de la cascade**, pas une\n  probab … [612 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "old_string": "   des valeurs, lui, n'a pas de schéma. Avec `--tagger`, `confiance` vaut **0,60** (le seuil de\n   la cascade) et `meta.ouvert` est `null` : ne pas lire ces champs comme une probabilité.", "new_ … [233 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "timeout 400 python3 /tmp/verifier_d1.py; echo \"exit=$?\"", "description": "Re-run doc block verification after JSON fix", "timeoutMs": 430000}`

  ```
5/5 blocs reproduits
exit=0
  ```

- **bash** `{"command": "python3 - <<'PY'\ntry:\n    import fastjsonschema\n    print('fastjsonschema', fastjsonschema.__version__ if hasattr(fastjsonschema,'__version__') else 'ok')\nexcept Exception as e:\n    print('absent', e)\nPY", "description": "Check fastjsonschema availability"}`

  ```
fastjsonschema ok
  ```

- **edit** `{"file_path": "/tmp/verifier_d1.py", "old_string": "DOC = RACINE / \"docs/produit/exemples.md\"", "new_string": "DOC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else RACINE / \"docs/produit/exemples.md\""}`

  ```
The file /tmp/verifier_d1.py has been updated successfully.
  ```

- **bash** `{"command": "cp docs/produit/exemples.md /tmp/exemples-mute.md\npython3 - <<'PY'\nfrom pathlib import Path\np=Path('/tmp/exemples-mute.md')\ns=p.read_text()\nold='POS  Le/DET livre/NOUN que/PRON j\\'ai/PRON lu/VERB est/AUX intéressant/ADJ ./PONCT'\nnew='POS  Le/DET livre/NOUN que/PRON j\\'ai/PRON lu … [302 caractères tronqués]`

  ```
mutation appliquée
3/5 blocs reproduits
6.2: annotation différente
  doc: "POS  Le/DET livre/NOUN que/PRON j'ai/PRON lu/NOUN est/AUX intéressant/ADJ ./PONCT"
  cli: "POS  Le/DET livre/NOUN que/PRON j'ai/PRON lu/VERB est/AUX intéressant/ADJ ./PONCT"
exit=1
  ```

- **edit** `{"file_path": "/tmp/verifier_d1.py", "old_string": "    # --- compte\n    total = len(EXEMPLES) + 2\n    if echecs:\n        print(f\"{total - len(echecs)}/{total} blocs reproduits\")\n        print(\"\\n\".join(echecs))\n        return 1\n    print(f\"{total}/{total} blocs reproduits\")\n    return … [353 caractères tronqués]`

  ```
The file /tmp/verifier_d1.py has been updated successfully.
  ```

- **bash** `{"command": "timeout 400 python3 /tmp/verifier_d1.py /tmp/exemples-mute.md; echo \"exit=$?\"", "description": "Re-run mutation control with correct count", "timeoutMs": 430000}`

  ```
4/5 blocs reproduits
6.2: annotation différente
  doc: "POS  Le/DET livre/NOUN que/PRON j'ai/PRON lu/NOUN est/AUX intéressant/ADJ ./PONCT"
  cli: "POS  Le/DET livre/NOUN que/PRON j'ai/PRON lu/VERB est/AUX intéressant/ADJ ./PONCT"
exit=1
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport copy, json, pathlib\nimport fastjsonschema\nschema=json.load(open('tools/schemas/drave-annotation-v2.json'))\nvalide=fastjsonschema.compile(schema)\nok=0\nfor n in (1,2,3):\n    a=json.load(open(f'/tmp/tag{n}.json'))\n    assert a['schema']=='drave.annotation' a … [638 caractères tronqués]`

  ```
annotations tagger valides v2: 3 /3
version 3 refusée: data.version must be same as const definition: 2
sans refus refusé: data must contain ['refus'] properties
  ```

- **bash** `{"command": "bash tools/porte-produit.sh > /tmp/porte-produit-d1.log 2>&1; echo \"exit=$?\" >> /tmp/porte-produit-d1.log; tail -30 /tmp/porte-produit-d1.log", "description": "Run product gate for D1 acceptance", "run_in_background": true}`

  ```
started background job bash-60
  ```

- **bash** `{"command": "git rev-parse HEAD; git rev-parse --short HEAD; cat /tmp/tag1.out; echo @@@; cat /tmp/tag2.out; echo @@@; cat /tmp/tag3.out", "description": "Capture HEAD and tagger outputs"}`

  ```
ee04ea9134d8f9fab62c8728fd1ab7857ded4dd3
ee04ea91
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.1 s
@@@
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 43 étiquettes · unités sémantiques=3 (48.6% du texte)
POS  Le/DET livre/NOUN que/PRON j'ai/PRON lu/VERB est/AUX intéressant/ADJ ./PONCT
SYNTAGMES
  GN   [0:8]    Le livre                     rôle=agent     → intéressant
  REL  [9:20]   que j'ai lu                  rôle=qualite   → livre
  REL  [9:36]   que j'ai lu est intéressant  rôle=qualité   → livre
  GV   [21:36]  est 
… [1244 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-60"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cat > /tmp/gen_rapport_d1.py <<'PY'\nimport json, pathlib, subprocess, re\n\nR = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nhead = subprocess.check_output(['git','rev-parse','HEAD'], cwd=R, text=True).strip()\n\ndef lire(p): return pathlib.Path(p).read_text(encodin … [8721 caractères tronqués]`

  ```
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-tagger.json 10542 octets
justes: [('g001', {'heuristique': 3, 'tagger': 3, 'total': 3}), ('g011', {'heuristique': 5, 'tagger': 6, 'total': 7}), ('r241', {'heuristique': 6, 'tagger': 7, 'total': 7})]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-tagger.md", "content": "# D1 — les exemples `--tagger` et `--reel` : le coût affiché, la base honnête, cinq blocs rejoués\n\n> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **D1** · **Date** : 2026-11 … [9965 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-tagger.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **job_output** `{"job_id": "bash-60"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ls tools/tests/ | grep -i tagger; grep -rn \"20 phrases\\|tagger_20\\|qualifier_tagger\" tools reports | head -20", "description": "Find tagger 20-phrase harness"}`

  ```
test_tagger_api.py
tools/tests/linguistique/gold.py:3:20 phrases (14 françaises, 6 anglaises), **écrites à la main** après le bloc : elles ne sont pas
tools/tests/linguistique/qualifier_neuronal.py:277:                "20 phrases réelles (hand) ont servi au choix du modèle et du prompt ; les 160 "
tools/tests/linguistique/gold_synthetique.py:3:Les 20 phrases de `gold.py` sont **réelles** (écrites à la main) ; celles-ci sont **synthétiques** :
tools/tests/linguistique/qualifier_tagger_612.py:2:"""qualifier_tagger_612.py — le tagger POS API sur le gold 612 (hand 20 + reel 432 + synth 160).
tools/tests/linguistique/qualifier_tagger_612.py:16:    PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
tools/pensee/autotest.py:1384:    """Les 20 phrases complexes : POS 0,6829, syntagme 0,2963."""
tools/verifier_schema_produit.py:21:    python3 tools/verifier_schema_produit.py --gold 20    # + 20 phrases du gold
tools/porte-produit.sh:45:  dit ✅ "schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)"
reports/07/p8.md:76:**Le dispositif** ✓✓ : **630 séries** Verne (2 520 phrases FR, 3 B, `composition_verne.py --series 640`) ✓ ;
reports/rapport-pensee-gold-linguistiqu
… [1571 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/tests/linguistique/qualifier_tagger_612.py; grep -n \"argparse\\|add_argument\\|limit\\|source\" tools/tests/linguistique/qualifier_tagger_612.py | head -40", "description": "Inspect tagger qualification harness options"}`

  ```
#!/usr/bin/env python3
"""qualifier_tagger_612.py — le tagger POS API sur le gold 612 (hand 20 + reel 432 + synth 160).

POURQUOI. Le banc `qualifier_quatre_modes.py` ne charge que `gold_reel.json` (432 phrases) ; le
gold courant en compte 612, et le tagger n'y a jamais été mesuré. Ce banc ajoute la ventilation
hand / reel / synth, la latence réelle des appels et le modèle effectivement renvoyé par l'API.
Il ne modifie aucun autre fichier et n'écrit que le JSON demandé.

COÛT. Deux appels par phrase (POS + syntagmes), partagés par les six modes grâce au cache des
tagger : ~1 214 appels, ~360 k tokens, ~20 min pour 612 phrases.

USAGE.
    DEEPSEEK_KEY_FILE=$HOME/.config/drave/deepseek.key \
    DEEPSEEK_CACHE=$(mktemp -d /tmp/j43-cache.XXXX) \
    DEEPSEEK_MODEL=deepseek-chat \
    PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
      --sortie /tmp/tagger-612.json

La clé n'est jamais lue en dur : `tools/llm/deepseek.py` lit `DEEPSEEK_API_KEY` ou le fichier
`DEEPSEEK_KEY_FILE` (0600). Le cache doit être neuf : le cache par défaut contient les réponses
du 2026-11-04 et rejouerait l'ancien modèle au lieu de mesurer celui d'aujourd'hui.
"""
from __future__ impo
… [3464 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-60"}`

  ```
(no new output)
[status: running]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "```\ndrave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)\nlangue=fr script=Latn source=cascade · 19 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VERB\n … [1533 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "**Ce que l'option change — et ce qu'elle ne change pas.** Le **POS** vient du tagger\n(`source=cascade`, confiance déclarée **0,60**) ; les **syntagmes**, leurs **rôles**, leurs\n**cibles d'attache … [2620 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"appels 40\\|cache 40\\|1 218\\|358 962\\|21 min\\|0,04\\|94,75\\|+8,49\\|réel 432\" docs/produit/README.md", "description": "Find remaining stale tagger figures in README"}`

  ```
195:dit lequel est préféré — **aucune perte**), `filtrer` (vue linéaire : **F1 +0,047** mais **18
323:honnête : « Élodie sourit. » rend `langue=und` (confiance 0,04 < seuil 0,12), même avec
429:  COÛT        appels 40 · réseau 0 · cache 40 · tokens 0 · modèle deepseek-chat
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "  COÛT        appels 40 · réseau 0 · cache 40 · tokens 0 · modèle deepseek-chat", "new_string": "  COÛT        appels 20 · réseau 0 · cache 20 · tokens 0 · modèle deepseek-chat"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '45,55p' docs/produit/README.md; echo ---; sed -n '455,475p' docs/produit/README.md", "description": "Check other README tagger mentions"}`

  ```
documentent les syntagmes qui se chevauchent.

| ce que vous demandez | ce que vous obtenez | mesure du 15/11 |
|---|---|---|
| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; le CLI n'expose que `fr`/`en` comme indice) |
| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger` |
| **syntagmes** | GN, GV, GP, REL, SUB, avec leur span | F1 **0,7902** ; tête **0,9029** (vivant 612) ; **0,7906** sur le réel 452 |
| **attachement** | par syntagme : `role`, `cible`, `candidats` | **238/239** exacts ; couverture **0,9958** ; exact sur span **1,0000** |
| **pragmatique** | acte (assertion, question, exclamation), négation, modalité, double sens | acte **0,9967**, négation **0,9771**, modalité **0,9886**, double sens **0,9444** |
| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |
| **coût et trace** | octets, caractères, étiquettes, étapes | local, sans réseau |
---
`meta.union: true`. C'est une **lecture concurrente** publiée par l'union,
… [1454 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "`evaluer --tagger` mesure en plus la cascade **API** (**0,9475** sur 612, § 3.7), sans changer le\ndéfaut.", "new_string": "`evaluer --tagger` mesure en plus la cascade **API** (**0,9575** sur 612, … [35 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "grep -rn \"0,9475\\|0.9475\\|94,75\\|8,49\\|358 962\\|1 218 appel\\|deux appels\\|2 appels\" docs/produit reports/README.md | head -30", "description": "Find remaining stale tagger figures in product docs"}`

  ```
reports/README.md:38:| [`rapport-coordination-r.md`](rapport-coordination-r.md) | **R** — tagger POS 612 : **0,9475 (+8,49)** |
reports/README.md:39:| [`rapport-tagger-option.md`](rapport-tagger-option.md) | **R0.7 / 1A** — le tagger POS en option : **+8,57** sur 20 phrases, **+8,49** sur 612, défaut hors ligne |
  ```

- **job_output** `{"job_id": "bash-60"}`

  ```
(no new output)
[status: running]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "old_string": "| [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md) | **B13** — les 5 exemples de la doc |", "new_string": "| [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md) | **B13** — les 5 ex … [169 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
1: # Les rapports — données intermédiaires et références
2: 
3: > **Ce dossier porte les résultats et les données de nos travaux**, jamais la documentation de référence
4: > (elle est dans [`docs/`](../docs/)). Les fiches courantes sont citées depuis le tableau de bord
5: > [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md).
6: 
7: > **Navigation** : [la carte des sujets](../docs/theorie/carte.md) · [l'état du moment](../docs/pilotage/en-cours.md) ·
8: > [l'inventaire des docs](../docs/README.md) · [le journal](../journal/README.md).
9: >
10: > **Contexte** : la fiche [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) est un **hub** de
11: > **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par
12: > partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).
13: 
14: ## Les fiches courantes
15: 
16: | fichier | ce qu'il porte |
17: |---|---|
18: | [`rapport-bilan-nuit.md`](rapport-bilan-nuit.md) | **Bilan** — la nuit du 14 au 15/11 : le tagger, la base honnête, la phase C/B |
19: | 
… [3917 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "old_string": "| [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md) | **B13** — les 5 exemples de la doc |", "new_string": "| [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md) | **B13** — les 5 ex … [169 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "old_string": "| [`rapport-tagger-option.md`](rapport-tagger-option.md) | **R0.7 / 1A** — le tagger POS en option : **+8,57** sur 20 phrases, **+8,49** sur 612, défaut hors ligne |", "new_string": "| [`rapport-tagger- … [147 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/index_reports.py; echo exit=$?; git diff --stat reports/INDEX.md", "description": "Regenerate reports index"}`

  ```
740 fiches → reports/INDEX.md
exit=0
 reports/INDEX.md | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
120: | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
121: | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1–J11.4 (produit)** | **trancher `g017`** ; puis T132/T133, gold 200+ ; **B10.3 bloquée** |
122: | **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 (manque **0,2856** val / **0,3566** test) ; **[v2](../../reports/rapport-coordination-n2-v2.md)** ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |
123: | **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9475 (+8,49), intégrer** ; R2/R3 attendent N5/N4 | **route API LIVRÉE** (`--tagger`, 0bbdbbb3) ; **split réel tenu à l'écart** |
124: | **C1–C7** | hor
… [1695 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-60"}`

  ```
(no new output)
[status: running]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 04 h 50 HNE (bilan de la nuit écrit)**", "new_string": "**Mis à jour : 2026-11-15, 05 h 00 HNE (D1 : les exemples du tagger et de la base réelle)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 c … [989 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, restitution v1 (46/46, strict 0,1087), **J9.1 … [629 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **742** / **836** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **743** / **837** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9475 (+8,49), intégrer** ; R2/R3 attendent N5/N4 | **route API LIVRÉE** (`--tagger`, 0bbdbbb3) ; **split réel tenu à l'écart** |", "new_ … [249 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "**J12.1 — le §334 et les 44 signatures.**", "new_string": "**D1 — les exemples du tagger et de la base réelle.** `docs/produit/exemples.md` passe de **5**\nà **10** blocs : **3** avec `--tagger`  … [730 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-11-14 07 h 10**.", "new_string": "L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour … [33 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **job_output** `{"job_id": "bash-60"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -20 /tmp/porte-produit-d1.log; echo ---; ps -o pid,etime,cmd -C python3 | tail -10", "description": "Inspect gate progress log"}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 20 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
---
    PID     ELAPSED CMD
   3002 11-09:10:30 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
2725542    12:30:59 python3 src/app.py --no-browser
2997720       08:44 python3 tools/chantier/superviseur.py boucle --budget 14400 --timeout 3600
3000536       01:52 python3 -m tools.pensee.autotest
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-tagger.md", "old_string": "- [`docs/produit/exemples.md`](../docs/produit/exemples.md) — les **cinq nouveaux blocs** (§ 6 et\n  § 7), l'en-tête « dix exemples », les deux bullets `TAGGER API`/`--reel` du § 0, et  … [631 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-tagger.md has been updated successfully.
  ```

### 👤 Utilisateur

background job bash-60 (bash: bash tools/porte-produit.sh > /tmp/porte-produit-d1.log 2>&1; echo "exit=$?" >> /tmp/porte-produit-d1.log; tail -30 /tmp/porte-produit-d1.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-60"}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 20 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
exit=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "timeout 400 python3 /tmp/verifier_d1.py; echo \"verif_exemples_exit=$?\"", "description": "Final real doc block verification", "timeoutMs": 430000}`

  ```
5/5 blocs reproduits
verif_exemples_exit=0
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --gold 20; echo \"schema_exit=$?\"; python3 tools/verifier_schemas.py; echo \"schemas_exit=$?\"", "description": "Run schema checks", "timeoutMs": 180000}`

  ```
✅ fr (v2)
  ✅ en (v2)
  ✅ vide (v2)
  ✅ ponctuation (v2)
  ✅ long (v2)
  ✅ v1 (v1)
  ✅ gold:g001 (v2)
  ✅ gold:g002 (v2)
  ✅ gold:g003 (v2)
  ✅ gold:g004 (v2)
  ✅ gold:g005 (v2)
  ✅ gold:g006 (v2)
  ✅ gold:g007 (v2)
  ✅ gold:g008 (v2)
  ✅ gold:g009 (v2)
  ✅ gold:g010 (v2)
  ✅ gold:g011 (v2)
  ✅ gold:g012 (v2)
  ✅ gold:g013 (v2)
  ✅ gold:g014 (v2)
  ✅ gold:g015 (v2)
  ✅ gold:g016 (v2)
  ✅ gold:g017 (v2)
  ✅ gold:g018 (v2)
  ✅ gold:g019 (v2)
  ✅ gold:g020 (v2)
  ✅ rétro-compatibilité : annotation v1 lue par le schéma v1
  ✅ contrôle négatif : le schéma v2 refuse une annotation v1
  ✅ validateur JSON Schema · 26 cas
schema_exit=0
  schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
schemas_exit=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py; echo \"taille_exit=$?\"; python3 tools/verifie_en_cours.py; echo \"encours_exit=$?\"; python3 tools/index_reports.py --verifier; echo \"index_exit=$?\"", "description": "Run doc size, state and index checks", "timeoutMs": 120000}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    9122    502   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2463    221   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [754 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\ns=open('docs/pilotage/roadmap.md').read()\ni=s.index('**D1 —')\nj=s.index('**J12.1', i)\np=s[i:j]\nprint('words paragraph', len(p.split()))\nprint(p[:400])\nPY", "description": "Count D1 roadmap paragraph words"}`

  ```
words paragraph 122
**D1 — les exemples du tagger et de la base réelle.** `docs/produit/exemples.md` passe de **5**
à **10** blocs : **3** avec `--tagger` (la clé, le réseau, le **coût affiché** ; `g001` neutre,
`g011` `lu` NOUN → VERB, `r241` `when` CONJ → PRON ; **14/17 → 16/17** sur 17 tokens, **3
appels / 441 tokens / 3,7 s**) et **2** avec `--reel` (452 phrases : POS **0,8891**, F1
**0,7906**, attachement **183/
  ```

- **bash** `{"command": "grep -n \"def .*mots\\|split\\|budget\" tools/taille_documents.py | head -40; sed -n '1,80p' tools/taille_documents.py", "description": "Inspect word count implementation"}`

  ```
2:"""taille_documents.py — le budget de contexte et la cohésion des documents.
5:  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
11:Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
12:ils ne sont pas chargés automatiquement. Le budget est en **mots** ; l'estimation de tokens
16:elles ne comptent pas dans le budget ; le document les porte, la page montre le SVG.
25:# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
72:def mots(texte: str) -> int:
77:#: pas dans le budget de contexte. Le rendu (docwatch) est ce que voit le lecteur ;
85:def mots_hors_diagrammes(texte: str) -> int:
90:    for cat, motif, budget in BUDGETS:
92:            return cat, budget
101:    for cat, motif, budget in BUDGETS:
110:            lignes.append((n, t.count("\n") + 1, rel, cat, budget))
111:            tete = "\n".join(t.splitlines()[:20])
122:            if budget and n > budget:
123:                violations.append(f"{rel} : {n} mots > budget {budget} ({cat})")
147:    # propre budget. Les compter ici faisait payer 1 579 mots au T0 (organisation-du-depot.md)
148:    # au l
… [4118 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\ns=open('docs/pilotage/roadmap.md').read()\ni=s.index('**D1 —')\nj=s.index('**J12.1', i)\nprint('old block words', len(s[i:j].split()))\nk=s.index(\"La suite produit est **J11.2**\", i)\nprint('suite sentence', s[k:s.index('\\n',k)])\nPY", "description": "Mea … [32 caractères tronqués]`

  ```
old block words 122
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
ValueError: substring not found
[exit code: 1]
  ```

- **bash** `{"command": "sed -n '59,70p' docs/pilotage/roadmap.md", "description": "Read J11.1 paragraph"}`

  ```
**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
avec le code courant ; **4 sont corrigés** : la ponctuation finale entre dans le POS (`g001`,
`r241`), le refus sort en **3** et `r035` — l'ancien échec connu — rend exactement le gold
(`REL [9:24] « she talks about » → film`). Le seul bloc identique est `g011`. F1 **0,7902**,
attachement **238/238 labels** (238/239 cibles, 0,9958) ; le mandat 237/238 est l'état d'avant
`s065`. Le contrôle négatif (mutation d'un token dans une copie de la doc) est détecté 4/5.
[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**
(`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).

**J11.2 — la mesure par langue.** `evaluer --par-langue` expose le détail **fr/en** (POS,
syntagmes, attachement, pragmatique, contrôle négatif recalculé par langue) sans changer le
global. **fr** : 402 phrases, POS **0,8159**, F1 **0,7475**, attachement **151/151** ; **en** :
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**\n(`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).", "new_string … [223 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md')\ns=p.read_text()\ni=s.index('**D1 — les exemples du tagger et de la base réelle.**')\nj=s.index('**J12.1', i)\nassert s[i:j].endswith('\\n\\n')\np.write_text(s[:i]+s[j:])\nprint('removed', len(s[i:j].split()) … [167 caractères tronqués]`

  ```
removed 122 words
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2463    221   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4027 mots (budget 4 000)

  avertissements :
     · 55 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagme
… [140 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 05 h 00 HNE (D1 : les exemples du tagger et de la base réelle)**", "new_string": "**Mis à jour : 2026-11-15, 05 h 00 HNE (D1)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**D1** : **3 exemples `--tagger` + 2 `--reel`** dans [`exemples.md`](../produit/exemples.md) ([fiche](../../reports/rapport-exemples-tagger.md)).", "new_string": "**D1** ([fiche](../../reports/r … [30 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, restitution v1 (46/46, strict 0,1087), **J9.1 … [637 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) après les correctifs du 15/11 ; 0,9500 sur le réel 452 (+6,1)** ; R2/R3 attendent N5/N4 | **route API LIVRÉE** (`--tagger`,  … [265 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py; echo \"encours_exit=$?\"", "description": "Recheck context budget and state"}`

  ```
1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3996 mots (budget 4 000)

  avertissements :
     · 55 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
exit=0
  en-cours · 1626 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
encours_exit=0
  ```

- **bash** `{"command": "timeout 300 python3 tools/revue_documentation.py > /tmp/revue-d1.log 2>&1; echo \"exit=$?\"; tail -40 /tmp/revue-d1.log", "description": "Run documentation review", "timeoutMs": 330000}`

  ```
exit=0
  revue de documentation · 743 fiche(s) · 837 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh > /tmp/porte-tableaux-d1.log 2>&1; echo \"exit=$?\"; tail -20 /tmp/porte-tableaux-d1.log", "description": "Run table gate", "timeoutMs": 180000}`

  ```
exit=0
  ✅ 1815 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4390 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "git diff --check; echo \"diff_check_exit=$?\"; python3 -m json.tool reports/rapport-exemples-tagger.json > /dev/null; echo \"json_exit=$?\"", "description": "Check whitespace and JSON validity"}`

  ```
diff_check_exit=0
json_exit=0
  ```

- **bash** `{"command": "git status --short; echo ---; git diff --stat", "description": "Review working tree before commit"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M docs/produit/exemples.md
 M reports/INDEX.md
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
?? reports/rapport-exemples-tagger.json
?? reports/rapport-exemples-tagger.md
?? reports/rapport-gold-reel-50.json
?? reports/rapport-gold-reel-50.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
---
 docs/pilotage/en-cours.md               |  10 +-
 docs/pilotage/roadmap.md                |   7 +-
 docs/produit/README.md                  |  38 +-
 docs/produit/exemples.md                | 365 +++++++++++++++-
 reports/INDEX.md                        |   3 +-
 reports/README.md                       |   3 +-
 reports/pensee-coherence-fiches-v7.json |  19 +
 reports/pensee-dev-test-v10.json        |   2 +-
 reports/pensee-quatre-modes.json        | 734 ++++++++++++++++++--------------
 r
… [356 caractères tronqués]
  ```

- **bash** `{"command": "git show HEAD:reports/README.md | grep -n \"gold-reel-50\\|rapport-s-paragraphes\" || echo \"pas dans HEAD\"; git show HEAD:reports/INDEX.md | grep -n \"gold-reel-50\" || echo \"pas dans INDEX HEAD\"", "description": "Check if prior untracked reports are linked in HEAD"}`

  ```
19:| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
197:| [rapport-gold-reel-50.md](rapport-gold-reel-50.md) | R0.7 / B13 — le gold réel étendu : 50 phrases que l'heuristique rate, et ce qu'elles disent |
  ```

- **bash** `{"command": "git ls-files reports/rapport-gold-reel-50.md reports/rapport-s-paragraphes.md tools/tests/linguistique/gold_reel_50.py; git log --oneline -3 -- reports/rapport-gold-reel-50.md", "description": "Check tracked status of prior reports"}`

  ```
(no output)
  ```

- **bash** `{"command": "git show HEAD:reports/INDEX.md | grep -n \"s-paragraphes\" || echo \"pas dans INDEX HEAD\"; git diff reports/INDEX.md", "description": "Inspect INDEX diff for untracked entries"}`

  ```
705:| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
diff --git a/reports/INDEX.md b/reports/INDEX.md
index dae26e0d..666d75bb 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **739 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **740 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -181,6 +181,7 @@
 | [rapport-evaluer-langue.md](rapport-evaluer-langue.md) | J11.2 — la mesure par langue : l'anglais devant, mais le gold n'est pas le même |
 | [rapport-execution-v41.md](rapport-execution-v41.md) | Rapport — test d'exécution locale de DeepSeek-V4.1-Flash, avec toutes les optimisations |
 | [rapport-exemples-rejoues.md](rapport-exemples-rejoues.md) | J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec |
+| [rapport-exemples-tagger.md](rapport-exemples-tagger.md) | D1 — les exemples `--tagger` et `--reel`
… [501 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/verifie_etat_a_jour.py; ls .git/hooks/ | head; [ -f .git/hooks/pre-commit ] && sed -n '1,80p' .git/hooks/pre-commit", "description": "Inspect pre-commit hook requirements"}`

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
… [5177 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat --oneline ee04ea91 | head -30", "description": "Check if prior commit includes journal"}`

  ```
ee04ea91 BILAN DE LA NUIT — LE TAGGER (95,75), LA BASE HONNÊTE (452), LA PHASE C/B (N2, S, R, PANINI) ET LES NÉGATIFS DITS
 docs/pilotage/en-cours.md                          |  4 +-
 journal/2026-11-15/README.md                       |  7 ++--
 journal/2026-11-15/distribue.md                    |  2 +-
 journal/2026-11-15/docs.md                         |  5 ++-
 journal/2026-11-15/mesures.md                      |  2 +-
 journal/2026-11-15/portes.md                       |  2 +-
 journal/README.md                                  |  2 +-
 journal/sessions/MANIFEST.md                       |  2 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 20 +++++++++
 .../rapport.md                                     | 17 ++++----
 reports/INDEX.md                                   |  3 +-
 reports/README.md                                  |  1 +
 reports/pensee-bilan-nuit.json                     | 36 +++++++++++++++++
 reports/rapport-bilan-nuit.md                      | 47 ++++++++++++++++++++++
 14 files changed, 129 insertions(+), 21 deletions(-)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md", "offset": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md</path>
<type>file</type>
<content>
20: 
21: <!-- /notes -->

(End of file - total 21 lines)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md</path>
<type>file</type>
<content>
1: # 2026-11-15 — Documentation, état, conventions
2: 
3: > **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
4: > Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
5: > Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.
6: 
7: ## Commits du jour (3)
8: 
9: | heure | commit | fait | fichiers |
10: |---|---|---|---|
11: | 02:00 | `5891ef8a` | ÉTAT — T0 TENU : LA LIGNE FAIT RACCOURCIE | `en-cours.md`, `README.md`, `mesures.md` (+6) |
12: | 03:51 | `01b6db6e` | JOURNAL — 2026-11-15 : B2, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX (NÉGATIF CONTRÔLÉ ; LE STYLE EST ABSORBÉ PAR LA DATE) | `README.md`, `mesures.md`, `README.md` (+4) |
13: | 04:30 | `c24253ee` | DOC PRODUIT — LA PASSE D'HONNÊTETÉ : LES TROIS BASES (612, 602, RÉEL 452), L'ATTACHEMENT 238/239, LE TAGGER 95,75, LES CHIFFRES DATÉS ANNOTÉS | `en-cours.md`, `README.md`, `README.md` (+5) |
14: 
15: ## Sessions actives ce jour
16: 
17: - `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Doc
… [320 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md", "old_string": "<!-- notes -->\n\n<!-- /notes -->", "new_string": "<!-- notes -->\n\n### D1 — les exemples du tagger et de la base réelle\n\n`docs/produit/exemples.md` passe à **dix** blocs. **Trois** exécutio … [710 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md has been updated successfully.
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/produit/README.md docs/produit/exemples.md reports/INDEX.md reports/README.md reports/rapport-exemples-tagger.md reports/rapport-exemples-tagger.json journal/2026-11-15/docs.md\ngit diff --cached --stat", "description": "St … [37 caractères tronqués]`

  ```
docs/pilotage/en-cours.md            |  10 +-
 docs/pilotage/roadmap.md             |   7 +-
 docs/produit/README.md               |  38 ++--
 docs/produit/exemples.md             | 365 +++++++++++++++++++++++++++++++++--
 journal/2026-11-15/docs.md           |  11 ++
 reports/INDEX.md                     |   3 +-
 reports/README.md                    |   3 +-
 reports/rapport-exemples-tagger.json | 270 ++++++++++++++++++++++++++
 reports/rapport-exemples-tagger.md   | 161 +++++++++++++++
 9 files changed, 822 insertions(+), 46 deletions(-)
  ```

- **bash** `{"command": "git commit -F - <<'MSG'\nD1 — LES EXEMPLES DU TAGGER ET DE LA BASE RÉELLE : 3 BLOCS --tagger (441 TOKENS, 3,7 S), 2 BLOCS --reel (452 PHRASES, POS 88,91, F1 79,06), 5/5 REJOUÉS, MUTATION 4/5\n\nLes exemples de docs/produit/exemples.md passent de 5 à 10 blocs :\n- 3 avec --tagger (clé +  … [551 caractères tronqués]`
