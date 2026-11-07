# Session DSH — relecture

- identifiant : `session-932afd57-1363-4133-b6f1-64f7d937f38d`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-07 14:59:21
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J2.2 : le corpus commun — choisir un échantillon (10-50 textes) présent des deux côtés (Panini/NIPADA et Drave), le normaliser (UTF-8, une phrase par ligne, métadonnées langue/époque), l'écrire dans `work/corpus-commun/` (non versionné) + une fiche `reports/rapport-corpus-commun.md` + JSON. Lire les corpus Panini sans les modifier.

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

- **bash** `{"command": "pwd && ls -la && git status --short | head -50", "description": "Inspect workspace root and git status"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   180  7 nov 14:59 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   932  7 nov 00:00 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 74108  7 nov 14:54 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [1352 caractères tronqués]
  ```

- **bash** `{"command": "ls -la docs/pilotage/ 2>/dev/null | head -40; echo ---; ls -la work/ 2>/dev/null | head -40; echo ---; ls -la reports/ 2>/dev/null | head -40", "description": "List pilotage, work, reports"}`

  ```
total 220
drwxr-xr-x. 1 stephane stephane   298  7 nov 14:55 .
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 ..
drwxr-xr-x. 1 stephane stephane  1686  4 nov 11:53 backlog
-rw-r--r--. 1 stephane stephane 26125  7 nov 00:50 chantiers.md
-rw-r--r--. 1 stephane stephane 11637  7 nov 14:55 en-cours.md
-rw-r--r--. 1 stephane stephane 12411 28 oct 09:17 manques.md
-rw-r--r--. 1 stephane stephane 34739  7 nov 00:50 plan-travail.md
-rw-r--r--. 1 stephane stephane 22138  1 nov 13:46 programme-r.md
-rw-r--r--. 1 stephane stephane  4380  2 nov 20:20 README.md
-rw-r--r--. 1 stephane stephane 14292  6 nov 20:00 references-non-regression.md
-rw-r--r--. 1 stephane stephane 49874  7 nov 14:38 roadmap.md
-rw-r--r--. 1 stephane stephane 10053  7 nov 14:38 semaine-autonome.md
-rw-r--r--. 1 stephane stephane 14336 28 oct 09:17 utilisation.md
---
total 220
drwxr-xr-x. 1 stephane stephane  1616  7 nov 12:58 .
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 ..
-rwxr-xr-x. 1 stephane stephane  2133  2 nov 16:46 attente_portes.sh
drwxr-xr-x. 1 stephane stephane    60  7 nov 12:18 chantier
-rw-r--r--. 1 stephane stephane  6879  1 nov 12:49 corpus-wiki-langues.log
-rw-r--r--. 1 stephane stephane  1004
… [5011 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"J2.2\\|corpus-commun\\|corpus commun\" --include=\"*.md\" --include=\"*.json\" . 2>/dev/null | grep -v \".git/\" | head -60", "description": "Search task references"}`

  ```
./reports/rapport-inventaire-panini.md:376:**Formats de référence pour un corpus commun.**
./reports/pensee-inventaire-panini.json:811:      "action": "corpus commun : aligner udhr_corpus.json (532) et Qtrinet/data/udhr/langues.jsonl (456), produire la table iso3 et l'echantillon de 20 langues",
./reports/rapport-atomes-niveaux.md:90:> décrivent le dispositif à construire en J2.2, pas un résultat.
./reports/rapport-atomes-niveaux.md:209:## 6. Protocole de mesure — ce qu'il faudra faire en J2.2
./reports/rapport-atomes-niveaux.md:211:### 6.1 Le corpus commun
./reports/rapport-atomes-niveaux.md:289:## 8. La suite — J2.2
./reports/rapport-atomes-niveaux.md:291:1. **Construire le corpus commun** : 20 textes, mêmes identifiants, mêmes métadonnées, signatures Panini et
./reports/rapport-atomes-niveaux.md:299:Le lien avec le reste de la semaine : cette table est le préalable de J2.2 (corpus commun), J3.1 (retrieval à
./reports/atomes-niveaux.json:733: "prochaine_etape": "J2.2 : construire le corpus commun (20 textes, mêmes identifiants), pré-enregistrer les 14 paires atome -> variable principale, exécuter le protocole (CLR, permutations, partielles, BH, split-half, corpus négatif), publie
… [5966 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/ | head -80; echo ---; cat .gitignore", "description": "List data and gitignore"}`

  ```
total 961812
drwxr-xr-x. 1 stephane stephane      2664  2 nov 18:33 .
drwxr-xr-x. 1 stephane stephane       686  6 nov 09:52 ..
drwxr-xr-x. 1 stephane stephane       220 22 oct 22:05 adaptateurs
drwxr-xr-x. 1 stephane stephane        32 19 oct 14:30 alignement
-rw-r--r--. 1 stephane stephane  59784525 21 oct 01:02 composition-etats.npz
-rw-r--r--. 1 stephane stephane  30539912 21 oct 03:44 composition-verne-14b-etats.npz
-rw-r--r--. 1 stephane stephane  21144969 21 oct 01:38 composition-verne-7b-etats.npz
-rw-r--r--. 1 stephane stephane  12037642 21 oct 01:30 composition-verne-etats.npz
-rw-r--r--. 1 stephane stephane 151064111 21 oct 23:31 composition-verne-large-etats.npz
-rw-r--r--. 1 stephane stephane 147255554 21 oct 23:47 composition-verne-plan-etats.npz
-rw-r--r--. 1 stephane stephane     97900 29 oct 14:19 consignes_train.jsonl
-rw-r--r--. 1 stephane stephane      1931 29 oct 14:19 consignes_val.jsonl
-rw-r--r--. 1 stephane stephane 100276153  8 oct 09:42 corpus_en.txt
-rw-r--r--. 1 stephane stephane   2032162  8 oct 09:42 corpus_en_val.txt
-rw-r--r--. 1 stephane stephane  17031747 17 oct 18:26 corpus_fr_litterature.txt
-rw-r--r--. 1 stephane stephane   4402195 28 oct 12:45
… [5125 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '90,140p' tools/chantier/plan.json", "description": "Read plan J2.2"}`

  ```
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
  },
  {
   "id": "J2.2",
   "jour": 2,
   "titre": "Panini I — le corpus commun",
   "mandat": "Tâche J2.2 : le corpus commun — choisir un échantillon (10-50 textes) présent des deux côtés (Panini/NIPADA et Drave), le normaliser (UTF-8, une phrase par ligne, métadonnées langue/époque), l'écrire dans `work/corpus-commun/` (non versionné) + une fiche `reports/rapport-corpus-commun.md` + JSON. Lire les corpus Panini sans les modifier.",
   "budget_min": 90,
   "acceptation
… [1421 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' reports/rapport-inventaire-panini.md", "description": "Read Panini inventory report start"}`

  ```
# Inventaire Panini — état daté du 7 novembre 2026

> **Mission.** Inventaire complet et daté des 14 dépôts de l'écosystème Panini pour préparer le
> chantier autonome d'une semaine d'intégration avec Drave (`../Qtrinet/`, 7 → 14/11/2026).
> **Lecture seule** : aucun commit, aucun fichier de code, de doc ou de configuration modifié,
> `git status` lancé avec `--no-optional-locks`. Un seul effet de bord, documenté au §5.7 : un
> `sqlite3` de lecture a checkpointé le WAL d'une base de corpus. Les deux seuls fichiers écrits sont ce rapport et son JSON.
>
> **Méthode.** `git log` / `status` / `submodule status`, lecture des README, docs et journaux de
> bord, comptages (`find`, `du`, `wc`), lecture directe des artefacts JSON. **Aucune suite de tests
> n'a été exécutée** : les leurs coûtent de 45 min à 3 h 30. Les chiffres cités sont ceux que
> Panini **publie**, avec leur date et leur chemin — ils sont repris, pas re-mesurés.

---

## 0. Ce qu'il faut retenir

1. **Un seul dépôt est vivant au sens fort : `Panini/research`** (= `Panini-Research`, qui est un
   lien symbolique vers lui). 1 622 commits, dernier le **25/10/2026**, 182 194 lignes de Python,
   50 124 lignes de noyau formel.
… [8639 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '200,330p' reports/rapport-atomes-niveaux.md", "description": "Read protocol section"}`

  ```
Une ACP sur les parts CLR donne **4 composantes de valeur propre > 1** ; les trois premières expliquent
**80,7 %** de la variance (6,967 · 2,845 · 1,491 · 1,260 · …). Autrement dit, dans ce corpus, les 14 atomes
n'occupent que **quatre dimensions effectives**. Une table qui traiterait les 14 atomes comme 14 mesures
indépendantes surestimerait massivement l'information disponible.

**Ce que cette calibration n'est pas** : un test de la table. Elle ne contrôle ni la date, ni la langue, ni le
genre ; elle ne dit pas si un atome « porte » un niveau. Elle dit que le corpus de départ est **petit, colinéaire
et déséquilibré**, et que le protocole doit en tenir compte.

## 6. Protocole de mesure — ce qu'il faudra faire en J2.2

### 6.1 Le corpus commun

- **20 textes** au minimum, avec le même identifiant des deux côtés, le même découpage (premiers 10 000 mots,
  comme `analytic_sigs_v1.json`), et les mêmes métadonnées : date, langue, famille, genre.
- **Au moins 5 genres** et **3 familles** ; sinon, l'époque et le genre expliqueront tout.
- Les signatures Panini (14 parts) et les annotations Drave (9 niveaux, dont 8 retenus) sont produites sur le
  **même texte**, pas sur deux traductions
… [5963 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '300,430p' reports/rapport-inventaire-panini.md", "description": "Read Panini corpus formats section"}`

  ```
| 1 | **ÊTRE** | ∃ | 2 | existence, substrat | témoin : retrait **catastrophique** |
| 2 | **DIFFÉRENCE** | ∆ | 3 | gradient entre états | témoin : casse |
| 3 | **RAPPORT** | ∼ | 5 | relation | témoin : casse |
| 4 | **ORIENTATION** | ↗ | 7 | direction du flux | témoin : dégrade (lien H₀) |
| 5 | **SUJET** | ⊙ | 11 | agent, expérienceur | porteur modéré |
| 6 | **TEMPS** | ⧖ | 13 | durée, séquence | porteur modéré |
| 7 | **MODALITÉ** | ◇ | 17 | possible / nécessaire (Ł3) | spéculatif |
| 8 | **NOMBRE** | № | 19 | quantité, cardinalité | faible (candidat au retrait) |
| 9 | **ESPACE** | ⊕ | 23 | localisation, métaphore | porteur modéré |
| 10 | **OPÉRATION** | ⊗ | 29 | action, acte (les dhātus ACT) | témoin : casse |
| 11 | **FONCTION** | λ | 31 | finalité, usage | spéculatif |
| 12 | **STRUCTURE** | ⊞ | 37 | organisation, agencement | porteur modéré |
| 13 | **SYMÉTRIE** | ≍ | 41 | symétrie, équilibre | **meilleur candidat au retrait** |
| 14 | **ÉQUATION** | ≡ | 43 | égalité, équivalence | faible en philo, fort en technique |

**Sont-ils utilisables par Drave ? Oui, à trois conditions.**

1. **En lecture directe** : `analytic_sigs_v1.json` est un `{texte: {14 flottants}}` pur, s
… [9299 caractères tronqués]
  ```

- **bash** `{"command": "ls -d ../Panini* 2>/dev/null; echo ---; ls -la ../Panini/research/data/ 2>/dev/null | head -40; echo ---; ls -la ../Panini/research/nipada/falsification/ 2>/dev/null | head -40", "description": "Locate Panini repositories and corpus files"}`

  ```
../Panini
../Panini-AttributionRegistry
../Panini-AutonomousMissions
../Panini-CloudOrchestrator
../Panini-CoLabController
../Panini-CopilotageShared
../Panini-DatasetsIngestion
../Panini-ExecutionOrchestrator
../Panini-FS
../Panini-PublicationEngine
../Panini-Research
../Panini-SemanticCore
../Panini-SpecKit-Shared
../Panini-UltraReactive
---
total 104828
drwxr-xr-x. 1 stephane stephane     8154  5 aoû 14:37 .
drwxr-xr-x. 1 stephane stephane     2112 21 oct 08:37 ..
-rw-r--r--. 1 stephane stephane      225 27 jan  2026 acceleration_config.json
-rw-r--r--. 1 stephane stephane    16117 27 jan  2026 analyse_20250922_085336_en.json
-rw-r--r--. 1 stephane stephane    12390 27 jan  2026 analyse_20250922_085336_fr.json
-rw-r--r--. 1 stephane stephane     2737 27 jan  2026 ANALYSE_DETAILLEE_CONCEPTS_20250922.json
-rw-r--r--. 1 stephane stephane     3218 27 jan  2026 ANALYSE_FONCTIONS_LEXICALES_DHATU_20250922.json
-rw-r--r--. 1 stephane stephane     8339 27 jan  2026 analyse_litterature_pertinente.json
-rw-r--r--. 1 stephane stephane    17387 27 jan  2026 analyse_molecules_semantiques_conte.json
-rw-r--r--. 1 stephane stephane     3893 27 jan  2026 analyse_onomastique_20250922_090407_en.js
… [5433 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/udhr/ | head -50; echo ---; head -c 800 data/udhr/langues.jsonl; echo; echo ---; head -c 600 data/udhr/genealogie.json", "description": "Inspect Drave UDHR data"}`

  ```
total 19588
drwxr-xr-x. 1 stephane stephane     502 25 oct 00:01 .
drwxr-xr-x. 1 stephane stephane    2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane 7661342 17 oct 23:14 articles.jsonl
-rw-r--r--. 1 stephane stephane 6481755 17 oct 23:14 articles_propres.jsonl
-rw-r--r--. 1 stephane stephane    8286 17 oct 23:49 _eng.txt
drwxr-xr-x. 1 stephane stephane    1206 27 oct 22:33 familles
-rw-r--r--. 1 stephane stephane    9734 17 oct 23:49 _fra.txt
-rw-r--r--. 1 stephane stephane   90808 18 oct 10:30 genealogie.json
-rw-r--r--. 1 stephane stephane  126982 17 oct 23:14 langues.jsonl
-rw-r--r--. 1 stephane stephane   57191 17 oct 23:14 meta.json
-rw-r--r--. 1 stephane stephane   70498 18 oct 01:19 udhr_10_train.txt
-rw-r--r--. 1 stephane stephane   29232 18 oct 01:19 udhr_10_val.txt
-rw-r--r--. 1 stephane stephane    6834 18 oct 01:31 udhr_1_train.txt
-rw-r--r--. 1 stephane stephane    2239 18 oct 01:31 udhr_1_val.txt
-rw-r--r--. 1 stephane stephane  459299 18 oct 01:19 udhr_50_train.txt
-rw-r--r--. 1 stephane stephane  180892 18 oct 01:19 udhr_50_val.txt
-rw-r--r--. 1 stephane stephane    8818 18 oct 00:20 udhr_fra_train.txt
-rw-r--r--. 1 stephane stephane    5490 18 oct 00:28 udhr_
… [1545 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='../Panini/research/data/udhr_corpus.json'\nd=json.load(open(p))\nprint(type(d), len(d))\nif isinstance(d, dict):\n    for k in list(d)[:3]:\n        print('KEY', repr(k), type(d[k]))\n        print(json.dumps(d[k], ensure_ascii=False)[:800])\nelif isin … [153 caractères tronqués]`

  ```
<class 'dict'> 6
KEY 'format' <class 'str'>
"udhr-v2.0-xml"
KEY 'source' <class 'str'>
"eric-muller/udhr (GitHub) — Unicode UDHR XML Project"
KEY 'article' <class 'str'>
"Article 1"
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['../Panini/research/nipada/falsification/analytic_sigs_v1.json','../Panini/research/nipada/falsification/modern_sigs_v1.json','../Panini/research/nipada/falsification/modern_corpus_sigs_v2.json']:\n    d=json.load(open(p))\n    print('\\n===',p, … [138 caractères tronqués]`

  ```
=== ../Panini/research/nipada/falsification/analytic_sigs_v1.json <class 'dict'> 44
['2_esdras', 'aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'curry_1930', 'daniel_book', 'dn1_brahmajala', 'ezekiel_book', 'hosea_book', 'isaiah_book']

=== ../Panini/research/nipada/falsification/modern_sigs_v1.json <class 'dict'> 35
['2_esdras', 'aristotle_categories', 'aristotle_nicomachean_ethics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'daniel_book', 'dn1_brahmajala', 'ezekiel_book', 'hosea_book', 'isaiah_book', 'jeremiah_book', 'mikolov_2013', 'miller_evidence_prophecy', 'mn2_sabbasava']

=== ../Panini/research/nipada/falsification/modern_corpus_sigs_v2.json <class 'dict'> 39
['2_esdras', 'aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'daniel_book', 'dn1_brahmajala', 'ezekiel_book', 'hosea_book', 'isaiah_book', 'jeremiah_book']
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/research/data/udhr_corpus.json'))\nprint(list(d.keys()))\nfor k,v in d.items():\n    print(k, type(v), (len(v) if hasattr(v,'__len__') else ''))\nlangs=d.get('languages') or d.get('langs') or d.get('data')\nprint(type(langs))\n … [271 caractères tronqués]`

  ```
['format', 'source', 'article', 'total_languages', 'families', 'languages']
format <class 'str'> 13
source <class 'str'> 52
article <class 'str'> 9
total_languages <class 'int'> 
families <class 'dict'> 10
languages <class 'dict'> 532
<class 'dict'>
007 {"name": "Sãotomense", "iso": "007", "script": "Latn", "dir": "ltr", "text": "Tudu nguê di mundu ca nancê livli e igual ni dignidade e ni dirêtu. Punda nen ca pensá e nen tê cunxensa, selá nen fé tudu cuá cu tençón de lumón.", "family": "Other", "branch": "Unknown", "tradition": "other"}
008 {"name": "Crioulo, Upper Guinea (008)", "iso": "008", "script": "Latn", "dir": "ltr", "text": "Tudu pecadur padidu livre, ninguin ca más ninguin, tudu djusta, tudu tem mesmu diritu. Tudu quin qui padidu, tem si roçon, cu si manera di pensa. Na metadi di utrus I díbidi fassi cussas cu ermondadi.", "family": "Other", "branch": "Unknown", "tradition": "other"}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['data/udhr/articles_propres.jsonl','data/udhr/articles.jsonl']:\n    with open(p) as f:\n        line=f.readline()\n    d=json.loads(line)\n    print('===',p, list(d.keys()))\n    print(json.dumps(d,ensure_ascii=False)[:1200])\nEOF", "descriptio … [41 caractères tronqués]`

  ```
=== data/udhr/articles_propres.jsonl ['fichier', 'iso3', 'nom', 'script', 'art', 'texte', 'variante']
{"fichier": "udhr_007.xml", "iso3": "cri", "nom": "Sãotomense", "script": "Latn", "art": 1, "texte": "Tudu nguê di mundu ca nancê livli e igual ni dignidade e ni dirêtu. Punda nen ca pensá e nen tê cunxensa, selá nen fé tudu cuá cu tençón de lumón.", "variante": "007"}
=== data/udhr/articles.jsonl ['fichier', 'iso3', 'nom', 'script', 'art', 'titre', 'texte']
{"fichier": "udhr_007.xml", "iso3": "cri", "nom": "Sãotomense", "script": "Latn", "art": 0, "titre": "Préambule", "texte": "Punda dignidade di tudo nguê di mundu e dirêtu d'inem igual e andeji cu a na pô bêndê fa sá stê di liberdade, di justiça e di paz ni mundu; Punda fata di conheximentu e displêzu di dirêtu di hómé plovocá atu di malvadez cu ca revoltá cunxença di tudu hómé di mundu e punda ua mundu cu tudu nguê ca pô sa livli, pê pô flá e pê pô quêlê ni cuá cuê mêssê, sê mendu e sê miséria, fô ploclamadu cuma cuá maxi importanti cu hómé inventá; Punda ploteçón di dirêtu di hómé baseado ni ua ligime di dirêtu sá importante lumadu, pa hómé na sá obligado utilizá, cuma ultimu recurso, livolta contla tirania e opressón; Punda ê
… [462 caractères tronqués]
  ```

- **bash** `{"command": "ls ../Panini/research/nipada/corpus/_cache/sources/ 2>/dev/null | head -30; echo ---; ls ../Panini/research/nipada/corpus/_cache/sources/ 2>/dev/null | wc -l; echo ---; python3 - <<'EOF'\nimport json,os\np='../Panini/research/nipada/falsification/analytic_sigs_v1.json'\nd=json.load(open … [239 caractères tronqués]`

  ```
2_esdras.txt
apastamba_grhya_sutra.txt
aristotle_categories.txt
aristotle_de_caelo.txt
aristotle_nicomachean_ethics.txt
aristotle_parts_of_animals.txt
aristotle_posterior_analytics.txt
aristotle_prior_analytics.txt
asvalayana_grhya_sutra.txt
baudhayana_dharmasutra.txt
bengio_2003.txt
book_of_enoch.txt
brihadaranyaka_upanishad.txt
burnet_early_greek_philosophy.txt
chandogya_upanishad.txt
curry_1930.txt
daniel_book.txt
daodejing.txt
daxue.txt
dn11_kevatta.txt
dn14_mahapadana.txt
dn15_mahanidana.txt
dn16_mahaparinibbana.txt
dn1_brahmajala.txt
dn21_sakkapanha.txt
dn22_mahasatipatthana.txt
dn26_cakkavatti.txt
dn29_pasadika.txt
dn2_samannaphala.txt
dn33_sangiti.txt
---
102
---
2_esdras -> ['2_esdras.txt']
aristotle_categories -> ['aristotle_categories.txt']
aristotle_de_caelo -> ['aristotle_de_caelo.txt']
aristotle_nicomachean_ethics -> ['aristotle_nicomachean_ethics.txt']
aristotle_parts_of_animals -> ['aristotle_parts_of_animals.txt']
aristotle_posterior_analytics -> ['aristotle_posterior_analytics.txt']
aristotle_prior_analytics -> ['aristotle_prior_analytics.txt']
bengio_2003 -> ['bengio_2003.txt']
book_of_enoch -> ['book_of_enoch.txt']
curry_1930 -> ['curry_1930.txt']
daniel_book ->
… [1476 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIl \"aristotle\\|bengio\\|book_of_enoch\\|brahmajala\" data/ 2>/dev/null | head -20; echo ---; find data -maxdepth 2 -iname \"*gutenberg*\" -o -iname \"*sacred*\" -o -iname \"*corpus*\" | head -40", "description": "Search Drave data for Panini works"}`

  ```
[still running after 60000ms; moved to background job bash-16]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "find data -maxdepth 2 -type d | sort | sed -n '1,200p'", "description": "List Drave data directories"}`

  ```
data
data/adaptateurs
data/adaptateurs/bilingue-1600
data/adaptateurs/plan-bilingue-800
data/adaptateurs/plan-contraste-800
data/adaptateurs/plan-contraste-plein-800
data/adaptateurs/plan-multi-tache-800
data/adaptateurs/plan-recurrent-800
data/alignement
data/corpus_litt_propre
data/corpus_nonambigu
data/corpus_ocr
data/corpus_ocr_cegep
data/corpus_ocr_cegep_avant_micro
data/corpus_ocr_cegep_micro
data/corpus_ocr_cegep_pilote-2pages
data/corpus_pdf
data/corpus_pdf_documents
data/corpus_propre
data/corpus_repo_propre
data/corpus_wiki_ar
data/corpus_wiki_ar_texte
data/corpus_wiki_de
data/corpus_wiki_de_texte
data/corpus_wiki_en
data/corpus_wiki_en_texte
data/corpus_wiki_es
data/corpus_wiki_es_texte
data/corpus_wiki_fr
data/corpus_wiki_fr_texte
data/corpus_wiki_it
data/corpus_wiki_it_texte
data/corpus_wiki_ja
data/corpus_wiki_ja_texte
data/corpus_wiki_pt
data/corpus_wiki_pt_texte
data/corpus_wiki_ru
data/corpus_wiki_ru_texte
data/corpus_wiki_zh
data/corpus_wiki_zh_texte
data/daccord
data/deepseek
data/deepseek/cache
data/deepseek/distillation
data/deepseek/distillation-300
data/deepseek/distillation-300-controle
data/deepseek/distillation-600
data/deepseek/distillation-600-controle
d
… [678 caractères tronqués]
  ```

- **bash** `{"command": "ls data/corpus_litt_propre data/corpus_propre data/corpus_repo_propre data/structures 2>/dev/null | head -60; echo ---; du -sh data/corpus_litt_propre data/corpus_propre data/corpus_repo_propre data/structures 2>/dev/null", "description": "Inspect corpus directories"}`

  ```
data/corpus_litt_propre:
test.txt
train.txt
val.txt

data/corpus_propre:
dev.txt
test.canal
test.txt
train.canal
train.txt
val.canal
val.txt

data/corpus_repo_propre:
dev.txt
test.txt
train.txt
val.txt

data/structures:
banque.jsonl
banque-manifest.json
banque-reference.jsonl
banque-reference-manifest.json
banque-validee.jsonl
banque-validee-manifest.json
---
17M	data/corpus_litt_propre
7,2M	data/corpus_propre
5,6M	data/corpus_repo_propre
136K	data/structures
  ```

- **bash** `{"command": "ls -la tools/structures | head; echo ---; cat .gitmodules; echo ---; ls tools/structures 2>/dev/null | head -20", "description": "Inspect structures submodule"}`

  ```
total 160
drwxr-xr-x. 1 stephane stephane   438  3 nov 16:22 .
drwxr-xr-x. 1 stephane stephane 17398  7 nov 14:44 ..
-rw-r--r--. 1 stephane stephane  7469  3 nov 17:08 arbre_svg.py
-rw-------. 1 stephane stephane  4388  2 nov 20:04 candidats_corpus.py
-rw-r--r--. 1 stephane stephane  7035  2 nov 02:10 construire_donnees.py
drwxr-xr-x. 1 stephane stephane   414  3 nov 16:49 donnees
-rw-r--r--. 1 stephane stephane 11442  2 nov 16:27 exporter_corpus.py
-rw-r--r--. 1 stephane stephane 30580  4 nov 11:41 generateur.py
-rw-r--r--. 1 stephane stephane    44  1 nov 10:50 .git
---
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
---
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
__pycache__
README.md
serveur.py
static
tests
verifier_corpus.py
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, os\n# Compare UDHR sets\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\ndrave=set()\nfor line in open('data/udhr/langues.jsonl'):\n    d=json.loads(line); drave.add(d['fichier'])\nprint('Panini langs', len(pan), 'Drave files … [569 caractères tronqués]`

  ```
Panini langs 532 Drave files 456
intersection 453
pan only sample ['udhr_021.xml', 'udhr_022.xml', 'udhr_023.xml', 'udhr_025.xml', 'udhr_026.xml']
drave only sample ['udhr_012.xml', 'udhr_kwi.xml', 'udhr_prq.xml']
drave iso3 389 with article1 389
  ```

- **bash** `{"command": "grep -rn \"corpus-commun\\|corpus commun\" journal/ 2>/dev/null | tail -40", "description": "Search journal for corpus commun work"}`

  ```
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:59543:- **La surface d'intégration** : une table **atomes ↔ niveaux**, un **corpus commun**, le **retrieval à époque contrôlée**, la **généalogie à deux faces** (leur théorie + notre alignement Glottolog), un **schéma JSON** validé des deux côtés.
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:59547:- **J2** : Panini I (la table atomes ↔ niveaux, le corpus commun) ;
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:59702:  [a_faire ] J2.2   j2 — Panini I — le corpus commun
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:60494:  [a_faire ] J2.2   j2 — Panini I — le corpus commun
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md:10295:- **La surface d'intégration** : une table **atomes ↔ niveaux**, un **corpus commun**, le **retrieval à époque contrôlée**, la **généalogie à deux faces** (leur théorie + notre alignement Glottolog), un **schéma JSON** validé des deux côtés.
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md:10299:- **J2** : Panini I (la table atomes ↔ niveaux, le corpus commun) ;
journal/sessions/session-a25a85ea-061e-49bd-bb61-64e
… [769 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"udhr\" reports/rapport-*.md 2>/dev/null | head -30; echo ---; ls reports/ | grep -i \"udhr\\|corpus\" | head -30", "description": "Search reports for UDHR work"}`

  ```
reports/rapport-b102bis-capacite.md:60:gpu-env/bin/python3 tools/semantique/entrainer.py --corpus udhr \
reports/rapport-cycle-rapide.md:35:**Ce que `tools/extrait_article1.py` produit** (`udhr_xml/`, 456 fichiers) :
reports/rapport-etat-s.md:27:| UDHR | **456** langues, **13 996** articles | `data/udhr/` |
reports/rapport-etat-s.md:91:raccourci faux. L'UDHR a **456 langues** (`data/udhr/langues.jsonl`), **13 996** lignes d'articles
reports/rapport-etat-s.md:496:  `data/udhr/` (456).
reports/rapport-ie-sous-familles.md:4:> `data/udhr/genealogie.json` porte la **branche glottolog** : on découpe l'IE en **sous-familles**
reports/rapport-ie-sous-familles.md:47:- Données : `data/udhr/familles/ie_{italique,indo_iranien,germanique,baltique,celtique}.jsonl`.
reports/rapport-inventaire-panini.md:294:| **Format d'échange** | `research/data/udhr_demo.nipada` (v0.3.0) | texte auto-portant : `§1: ∃ {iso:[eng:BEING, fra:ÊTRE]}…` |
reports/rapport-inventaire-panini.md:339:| **Étiquettes de corpus** | `research/data/udhr_corpus.json` (532 langues) | `family`, `branch`, `tradition` par langue | 532 |
reports/rapport-inventaire-panini.md:340:| **Généalogie réelle (Drave)** | `Qtrinet/data/udhr/gene
… [3639 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '430,470p' reports/rapport-inventaire-panini.md; echo ---; sed -n '520,545p' reports/rapport-inventaire-panini.md", "description": "Read inventory integration section"}`

  ```
## 4. Les trois intégrations les plus mûres

### 4.1 Le corpus UDHR et la généalogie — **la plus mûre, à faire en J2**

**Pourquoi.** Même source XML des deux côtés, données déjà présentes, format texte + JSON, aucune
dépendance. Panini apporte 532 langues étiquetées (famille/branche/tradition) et sa décomposition
V14 ; Drave apporte 456 langues × 30 articles et Glottolog.

**Premier livrable.** Un `data/udhr/` commun : table `iso3 → fichier → famille → branche →
tradition`, échantillon de 20 langues (5 familles × 4), et une mesure de recouvrement des codes.
**Mesure** : nombre de langues appariées, taux d'accord des familles, langues orphelines.
**Contrôle négatif** : deux langues de **familles différentes** doivent donner un retrieval faible,
deux langues **sœurs** un retrieval fort ; si les deux se valent, la mesure ne mesure rien.
**Risque** : les codes ISO ne sont pas les mêmes (Panini utilise des variantes `007`, `008`… ;
Drave a normalisé en `iso3`) — c'est le vrai travail.

### 4.2 Les signatures 14 atomes — **la plus utile pour la table atomes ↔ niveaux**

**Pourquoi.** `analytic_sigs_v1.json` est un JSON plat, sans dépendance ; les 14 atomes ont un
ordre canonique, un sym
… [2487 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/research/data/udhr_corpus.json'))\nprint('families', json.dumps(d['families'], ensure_ascii=False)[:2000])\n# count family labels\nfrom collections import Counter\nc=Counter(v.get('family') for v in d['languages'].values())\npr … [141 caractères tronqués]`

  ```
families {"Other": {"count": 503, "branches": ["Unknown"]}, "Indo-European": {"count": 17, "branches": ["Germanic", "Indo-Iranian", "Italic", "Romance", "Slavic"]}, "Afro-Asiatic": {"count": 2, "branches": ["Semitic"]}, "Uralic": {"count": 2, "branches": ["Finnic", "Ugric"]}, "Austronesian": {"count": 2, "branches": ["Malayo-Polynesian"]}, "Dravidian": {"count": 2, "branches": ["Southern"]}, "Japonic": {"count": 1, "branches": ["Japanese"]}, "Koreanic": {"count": 1, "branches": ["Korean"]}, "Turkic": {"count": 1, "branches": ["Oghuz"]}, "Niger-Congo": {"count": 1, "branches": ["Bantu"]}}
Counter({'Other': 421, 'Indo-European': 53, 'Sino-Tibetan': 11, 'Niger-Congo': 9, 'Afro-Asiatic': 8, 'Austronesian': 7, 'Dravidian': 6, 'Uralic': 3, 'Japonic': 3, 'Turkic': 3, 'Austroasiatic': 3, 'Tai-Kadai': 2, 'Isolate': 1, 'Kartvelian': 1, 'Koreanic': 1})
Counter({'other': 422, 'western_modern': 49, 'african': 16, 'indian': 13, 'confucean': 10, 'buddhist': 8, 'southeast_asian': 8, 'western_classical': 4, 'islamic': 2})
  ```

- **bash** `{"command": "for f in data/corpus_litt_propre/train.txt data/corpus_propre/train.txt data/corpus_repo_propre/train.txt; do echo \"=== $f\"; head -c 300 \"$f\"; echo; done", "description": "Peek Drave text corpora"}`

  ```
=== data/corpus_litt_propre/train.txt
Au lecteur

  Cette version électronique reproduit dans son intégralité
  la version originale.

  La ponctuation n'a pas été modifiée hormis quelques corrections
  mineures.

  L'orthographe a été conservée. Seuls quelques mots ont été modifiés.
  La liste des modifications se trouve à
=== data/corpus_propre/train.txt
L'architecture du cerveau — et ce qui manque à Drave pour la porter
9 octobre 2026. docs/biologie-pour-drave.md traitait de la brique (le
neurone, la synapse, l'énergie). Ce document traite de l'édifice : les régions,
les fibres, les noyaux, les organes — et fait l'inventaire de ce que Drave
=== data/corpus_repo_propre/train.txt
# La documentation de Drave — quatre familles

> **`docs/` dit ce qui reste vrai** : la méthode, l'état, la théorie, l'implantation. Les **chiffres** et les
> séries vivent dans [`reports/`](../reports/) ; le **récit daté** dans [`journal/`](../journal/). Une page de
> `docs/` qui se remplit
  ```

- **bash** `{"command": "grep -l -i \"aristotle\\|bengio\\|brahmajala\\|book of enoch\" data/corpus_*.txt data/*.txt 2>/dev/null | head; echo done", "description": "Search text corpora for Panini works"}`

  ```
data/corpus_en.txt
data/corpus_en_val.txt
data/corpus_mixte_litt2.txt
data/corpus_mixte_litt.txt
data/corpus_mixte.txt
data/corpus_multi_train.txt
data/corpus_multi.txt
data/corpus_repo.txt
data/corpus_en.txt
data/corpus_en_val.txt
done
  ```

- **bash** `{"command": "grep -n -i -m 5 \"aristotle\" data/corpus_en.txt; echo ---; grep -n -i -m 5 \"bengio\" data/corpus_en.txt; echo ---; grep -n -i -m 5 \"brahmajala\" data/corpus_en.txt", "description": "Check matches in English corpus"}`

  ```
2993:Aristotle }} ( ; }} 384–322&nbsp;BC) was an ancient Greek philosopher and polymath. His writings cover a broad range of subjects spanning the natural sciences, philosophy, linguistics, economics, politics, psychology, and the arts. As the founder of the Peripatetic school of philosophy in the Lyceum in Athens, he began the wider Aristotelian tradition that followed, which set the groundwork for the development of modern science.
2995:Little is known about Aristotle's life. He was born in the city of Stagira in northern Greece during the Classical period. His father, Nicomachus, died when Aristotle was a child, and he was brought up by a guardian. At around eighteen years old, he joined Plato's Academy in Athens and remained there until the age of thirty seven ( ). Shortly after Plato died, Aristotle left Athens and, at the request of Philip II of Macedon, tutored his son Alexander the Great beginning in 343 BC. He established a library in the Lyceum, which helped him to produce many of his hundreds of books on papyrus scrolls.
2997:Though Aristotle wrote many treatises and dialogues for publication, only around a third of his original output has survived, none of it intended f
… [3561 caractères tronqués]
  ```

- **bash** `{"command": "wc -l data/corpus_en.txt; head -c 400 data/corpus_en.txt", "description": "Inspect English corpus"}`

  ```
1196326 data/corpus_en.txt
Anarchism is a political philosophy and movement that seeks to abolish all institutions that perpetuate authority, coercion, or hierarchy, primarily targeting the state and capitalism. Anarchism advocates for the replacement of the state with stateless societies and voluntary free associations.

Although traces of anarchist ideas are found all throughout history, modern anarchism emerged from the
  ```

- **bash** `{"command": "for f in data/corpus_multi.txt data/corpus_multi_train.txt data/corpus_fr_litterature.txt data/corpus_mixte_litt2.txt; do echo \"=== $f\"; head -c 300 \"$f\"; echo; done", "description": "Inspect multi corpora"}`

  ```
=== data/corpus_multi.txt
Tudu nguê di mundu ca nancê livli e igual ni dignidade e ni dirêtu. Punda nen ca pensá e nen tê cunxensa, selá nen fé tudu cuá cu tençón de lumón.
Tudu nguê ca pô flá ni dirêtu cu liberdade cu sa ploclamadu ni Declaraçón sé, sê distinçón, mó fala di laça, di côlô, di sexo, d
=== data/corpus_multi_train.txt
Tudu nguê di mundu ca nancê livli e igual ni dignidade e ni dirêtu. Punda nen ca pensá e nen tê cunxensa, selá nen fé tudu cuá cu tençón de lumón.
Tudu nguê ca pô flá ni dirêtu cu liberdade cu sa ploclamadu ni Declaraçón sé, sê distinçón, mó fala di laça, di côlô, di sexo, d
=== data/corpus_fr_litterature.txt
Au lecteur

  Cette version électronique reproduit dans son intégralité
  la version originale.

  La ponctuation n'a pas été modifiée hormis quelques corrections
  mineures.

  L'orthographe a été conservée. Seuls quelques mots ont été modifiés.
  La liste des modifications se trouve à
=== data/corpus_mixte_litt2.txt
« « « ENGLISH « « «
Anarchism is a political philosophy and movement that seeks to abolish all institutions that perpetuate authority, coercion, or hierarchy, primarily targeting the state and capitalism. Anarchism advocates for the re
… [59 caractères tronqués]
  ```

- **bash** `{"command": "find data -maxdepth 3 -type f \\( -iname \"*aristo*\" -o -iname \"*platon*\" -o -iname \"*plato*\" -o -iname \"*enoch*\" -o -iname \"*upanishad*\" -o -iname \"*bengio*\" \\) 2>/dev/null | head -30; echo done", "description": "Find named works in Drave data"}`

  ```
done
  ```

- **bash** `{"command": "ls -la ../Panini/research/data/ | grep -i udhr; echo ---; python3 - <<'EOF'\nimport json,os\nfor p in ['../Panini/research/data/udhr_decomposed_v14.json','../Panini/research/data/udhr_convergence_v14.json']:\n    if os.path.exists(p):\n        d=json.load(open(p))\n        print('===',p … [272 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane   932627  3 aoû 16:46 udhr_article1_en.json
-rw-r--r--. 1 stephane stephane  1058726  3 aoû 16:46 udhr_article1_fr.json
-rw-r--r--. 1 stephane stephane     4705  5 aoû 14:04 udhr_convergence_graph.json
-rw-r--r--. 1 stephane stephane     6045  5 aoû 14:03 udhr_convergence_v14.json
-rw-r--r--. 1 stephane stephane   235085  4 aoû 10:26 udhr_corpus.json
-rw-r--r--. 1 stephane stephane     2409  5 aoû 14:03 udhr_decomposed_v14.json
-rw-r--r--. 1 stephane stephane    12632  3 aoû 14:52 udhr_demo.nipada
-rw-r--r--. 1 stephane stephane     1521  5 aoû 14:10 udhr_omw_coverage.json
-rw-r--r--. 1 stephane stephane      533  5 aoû 14:13 udhr_reconstruction_full.json
-rw-r--r--. 1 stephane stephane      368  5 aoû 14:09 udhr_reconstruction_report.json
-rw-r--r--. 1 stephane stephane    12508  5 aoû 14:05 udhr_universal_graph.json
---
=== ../Panini/research/data/udhr_decomposed_v14.json <class 'dict'> 2
total_languages_processed 11
results {"bul": {"name": "Bulgarian", "family": "Indo-European", "branch": "Slavic", "tradition": "western_modern", "tokens": 29, "found": 1, "coverage": 0.034482758620689655}, "cat": {"name": "Catalan", "family": "Indo-European", "bra
… [1839 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='data/udhr/meta.json'\nd=json.load(open(p))\nprint(type(d), len(d))\nif isinstance(d,dict):\n    print(list(d)[:10])\n    for k in list(d)[:2]: print(k, json.dumps(d[k],ensure_ascii=False)[:600])\nelif isinstance(d,list):\n    print(json.dumps(d[:2],ens … [72 caractères tronqués]`

  ```
<class 'dict'> 441
['udhr_007.xml', 'udhr_008.xml', 'udhr_009.xml', 'udhr_010.xml', 'udhr_011.xml', 'udhr_012.xml', 'udhr_013.xml', 'udhr_014.xml', 'udhr_016.xml', 'udhr_017.xml']
udhr_007.xml {"iso3": "cri", "nom": "Sãotomense", "script": "Latn", "sens": "ltr", "variante": "007", "nb_articles": 30}
udhr_008.xml {"iso3": "pov", "nom": "Crioulo, Upper Guinea (008)", "script": "Latn", "sens": "ltr", "variante": "008", "nb_articles": 30}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['../Panini/research/data/udhr_article1_en.json','../Panini/research/data/udhr_article1_fr.json']:\n    d=json.load(open(p))\n    print('===',p,type(d),len(d))\n    if isinstance(d,dict):\n        print(list(d)[:8])\n        k=list(d)[0]\n        … [203 caractères tronqués]`

  ```
=== ../Panini/research/data/udhr_article1_en.json <class 'dict'> 14
['format', 'lang', 'source_text', 'nipada_source', 'principle', 'step1_tokenization', 'step2_morphology', 'step3_syntax']
format "nipada-dtp-v12"
=== ../Panini/research/data/udhr_article1_fr.json <class 'dict'> 14
['format', 'lang', 'source_text', 'nipada_source', 'principle', 'step1_tokenization', 'step2_morphology', 'step3_syntax']
format "nipada-dtp-v12"
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\n# list available language keys and names\nfor k in list(d)[:10]:\n    v=d[k]; print(k, v['name'], v['families'] if 'families' in v else v.get('family'), v['iso'])\nEOF", "descript … [37 caractères tronqués]`

  ```
007 Sãotomense Other 007
008 Crioulo, Upper Guinea (008) Other 008
009 Mbundu (009) Other 009
010 Tetun Dili Other 010
011 Umbundu (011) Other 011
013 (Mijisa) Other 013
014 (Maiunan) Other 014
016 (Minjiang, spoken) Other 016
017 (Minjiang, written) Other 017
020 Drung Other 020
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nks=list(pan)\nprint(len(ks))\nprint([k for k in ks if not k.isdigit()][:30])\nprint('all numeric?', all(k.isdigit() for k in ks))\nEOF", "description": "Check Panini UDHR key fo … [7 caractères tronqués]`

  ```
532
['aar', 'abk', 'ace', 'acu', 'acu_1', 'ada', 'ady', 'afr', 'agr', 'aii', 'ajg', 'aka_akuapem', 'aka_asante', 'aka_fante', 'als', 'alt', 'amc', 'ame', 'amh', 'ami', 'amr', 'arb', 'arl', 'arn', 'ast', 'auc', 'auv', 'ayo', 'ayr', 'azj_cyrl']
all numeric? False
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, unicodedata, hashlib\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\n# drave article1 map by variant/file/iso\nart={}\nfor line in open('data/udhr/articles_propres.jsonl'):\n    d=json.loads(line)\n    if d['art']==1:\n      … [592 caractères tronqués]`

  ```
drave art1 440
match 418 diff 20 missing 94
('ady', 'Adyghe', 'Цӏыф пстэури шъхьэфитэу, ялъытэныгъэрэ яфэшъуашэхэмрэкӏэ зэф', 'ЦIыф пстэури шъхьэфитэу, ялъытэныгъэрэ яфэшъуашэхэмрэкIэ зэф')
('bfa', 'Bari', 'Ŋutu liŋ a yuŋwe kana, jojo i to’diri ko ’dekesi ko ti se to', 'Ŋutu liŋ a yuŋwe kana, jojo i toďiri ko ďekesi ko ti se toki')
('boa', 'Bora', 'Pámeere ííñújɨri meíjcyame tsá múhójɨ́sɨ́ pañé ɨ́cubáhrádú m', 'Pámeere ííñújɨri meíjcyame tsá múhójɨ́sɨ́ pañé ɨ́cubáhrádú m')
('bos_cyrl', 'Bosnian (Cyrillic)', 'Сва људска бића раћају се слободна и једнака у достојанству ', 'Сва људска биђа рађају се слободна и једнака у достојанству ')
('cbi', 'Chachi', "Naaju chachilla bain mu' chachilla bain na kayatu tichiba bu", "Naaju chachilla bain mu' chachilla bain na kayatu tichiba bu")
('cmn_hans', 'Chinese, Mandarin (Simplified)', '人人生而自由，在尊严和权利上一律平等。他们赋有理性和良心，并应以兄弟关系的精神相对待。', '人人生而自由,在尊严和权利上一律平等。他们赋有理性和良心,并应以兄弟关系的精神相对待。')
('csa', 'Chinantec, Chiltepec', "Lejɨ̈ ni sou tsa lisia̱ ija̱a sia ikou' ne kojo̱ jï ne juso̱", "Lej†̎ ni sou tsa lisia̱ ija̱a sia ikou' ne kojo̱ jï ne juso̱")
('dyu', 'Jula', 'Wólo’ lá, hádamaden’ bɛɛ ye hɔrɔn ye, bɛɛ ká kán lànbe ní há', 'Wólo’ lá, hádamaden’ bɛɛ ye hɔr
… [423 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nfor k in ['aar','ady','afr','cmn_hans','eng','fra','007']:\n    if k in pan:\n        v=pan[k]; print(k, 'iso=',v['iso'],'name=',v['name'],'script=',v['script'])\n# map iso dupl … [205 caractères tronqués]`

  ```
aar iso= aar name= Afar script= Latn
ady iso= ady name= Adyghe script= Cyrl
afr iso= afr name= Afrikaans script= Latn
cmn_hans iso= cmn_hans name= Chinese, Mandarin (Simplified) script= Hans
eng iso= eng name= English script= Latn
fra iso= fra name= French script= Latn
007 iso= 007 name= Sãotomense script= Latn
dup iso [] unique 532
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\n# drave file->iso and iso->files\nfiles={}\nfor line in open('data/udhr/langues.jsonl'):\n    d=json.loads(line); files[d['fichier']]=d\nfrom collections import Counter\nc=Counter(d['iso3'] for d in files.values())\nprint('files',len(files),'iso',len(c),' … [199 caractères tronqués]`

  ```
files 456 iso 400 dups [('pov', 2), ('kmb', 2), ('umb', 2), ('und', 5), ('acu', 2), ('twi', 2), ('oci', 7), ('azj', 2), ('bos', 2), ('chr', 2)]
udhr_007.xml {'fichier': 'udhr_007.xml', 'iso3': 'cri', 'nom': 'Sãotomense', 'script': 'Latn', 'sens': 'ltr', 'titre': 'Declaraçón Universal di Dirêtu di Hómé', 'nb_articles': 30, 'preambule_car': 1593, 'attrs': 'iso639-3=cri key=007 n=Sãotomense dir=ltr iso15924=Latn'}
udhr_aar.xml None
udhr_kwi.xml {'fichier': 'udhr_kwi.xml', 'iso3': 'kwi', 'nom': 'Awa-Cuaiquer', 'script': 'Latn', 'sens': 'ltr', 'titre': 'MINMURUS WANTAAWARUSPA', 'nb_articles': 30, 'preambule_car': 1523, 'attrs': 'iso639-3=kwi key=kwi n=Awa-Cuaiquer dir=ltr iso15924=Latn'}
udhr_eng.xml {'fichier': 'udhr_eng.xml', 'iso3': 'eng', 'nom': 'English', 'script': 'Latn', 'sens': 'ltr', 'titre': 'Universal Declaration of Human Rights', 'nb_articles': 30, 'preambule_car': 1992, 'attrs': 'iso639-3=eng key=eng n=English dir=ltr iso15924=Latn'}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, unicodedata\nfrom collections import Counter, defaultdict\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\ngene=json.load(open('data/udhr/genealogie.json'))\nfiles={}\nfor line in open('data/udhr/langues.jsonl'):\n    d=json. … [969 caractères tronqués]`

  ```
nofile 79 noart 15 diff 20 exact 418
families exact Counter({'Indo-European': 120, 'Atlantic-Congo': 81, 'Austronesian': 37, 'Sino-Tibetan': 17, 'Turkic': 17, 'Afro-Asiatic': 12, 'Mayan': 11, 'Quechuan': 11, '(inconnue)': 10, 'Uralic': 8, 'Arawakan': 7, 'Mande': 7, 'Tai-Kadai': 7, 'Otomanguean': 7, 'Pano-Tacanan': 5, 'Dravidian': 5, 'Chicham': 4, 'Nilotic': 4, 'Tungusic': 4, 'Hmong-Mien': 3, 'Artificial Language': 3, 'Austroasiatic': 3, 'Abkhaz-Adyge': 2, 'Zaparoan': 2, 'Iroquoian': 2, 'Tupian': 2, 'Uto-Aztecan': 2, 'Tucanoan': 2, 'Harakmbut': 1, 'Araucanian': 1, 'Aymaran': 1, 'Cahuapanan': 1, 'Muskogean': 1, 'Barbacoan': 1, 'Songhay': 1, 'Yanomamic': 1, 'Huitotoan': 1, 'Japonic': 1, 'Eskimo-Aleut': 1, 'Mongolic-Khitan': 1, 'Saharan': 1, 'Koreanic': 1, 'Algic': 1, 'Misumalpan': 1, 'Mixe-Zoque': 1, 'Athabaskan-Eyak-Tlingit': 1, 'Ticuna-Yuri': 1, 'Guaicuruan': 1, 'Totonacan': 1, 'Tarascan': 1, 'Peba-Yagua': 1})
scripts exact [('Latn', 329), ('Cyrl', 26), ('Arab', 10), ('Deva', 7), ('Hans', 5), ('Mymr', 3), ('Ethi', 2), ('Tibt', 2), ('Cher', 2), ('Grek', 2), ('Hebr', 2), ('Taml', 2), ('Thai', 2), ('Hani', 2), ('Syrc', 1)]
diff [('ady', 'udhr_ady.xml', 'Adyghe'), ('bfa', 'udhr_bfa.xml'
… [765 caractères tronqués]
  ```

- **bash** `{"command": "find data/jw -maxdepth 3 -type f | head -30; echo ---; du -sh data/jw; echo ---; find data/jw -type f | wc -l", "description": "Inspect JW data"}`

  ```
data/jw/html/https_www_jw_org_en_library_magazines_watchtower_study_august_2026_An_Appeal_on_the_Basis_of_Love_.html
data/jw/html/B0_E0_A4_95_E0_A5_80_E0_A4_97_E0_A4_AF_E0_A5_80_E0_A4_97_E0_A5_81_E0_A4_9C_E0_A4_BC_E0_A4_BE_E0_A4_B0_E0_A4_BF_E0_A4_B6_.html
data/jw/html/B0_E0_A6_A3_E0_A7_87_E0_A6_95_E0_A6_B0_E0_A6_BE_E0_A6_8F_E0_A6_95_E0_A6_85_E0_A6_A8_E0_A7_81_E0_A6_B0_E0_A7_8B_E0_A6_A7_.html
data/jw/html/https_www_jw_org_id_perpustakaan_majalah_menara_pengawal_pelajaran_agustus_2026_Permohonan_atas_Dasar_Kasih_.html
data/jw/html/D8_A8_D8_AA_DA_A9_DB_8C_D8_A8_D9_90_D9_86_D8_A7_D9_BE_D8_B1_D8_A7_DB_8C_DA_A9_D8_AF_D8_B1_D8_AE_D9_88_D8_A7_D8_B3_D8_AA_.html
data/jw/html/A9_B6_E7_94_A8_2026_E5_B9_B48_E6_9C_88_E6_84_9B_E3_81_AB_E5_9F_BA_E3_81_A5_E3_81_84_E3_81_9F_E3_81_8A_E9_A1_98_E3_81_84_.html
data/jw/html/B5_E0_A4_B0_E0_A4_95_E0_A5_87_E0_A4_B2_E0_A5_87_E0_A4_B2_E0_A5_80_E0_A4_B5_E0_A4_BF_E0_A4_A8_E0_A4_82_E0_A4_A4_E0_A5_80_.html
data/jw/html/9A_E0_B1_87_E0_B0_B8_E0_B0_BF_E0_B0_A8_E0_B0_92_E0_B0_95_E0_B0_B5_E0_B0_BF_E0_B0_A8_E0_B1_8D_E0_B0_A8_E0_B0_AA_E0_B0_82_.html
data/jw/html/ap_chi_thap_canh_hoc_hoi_thang8_2026_L_E1_BB_9Di_n_C3_A0i_xin_d_E1_BB_B1a_tr_C3_AAn_t_C3_ACnh_y_C3_AAu_th_C6_
… [2874 caractères tronqués]
  ```

- **bash** `{"command": "find data -maxdepth 3 -type f | grep -iE \"bible|ezekiel|daniel|isaiah|jeremiah|enoch|esdras\" | head -30; echo done", "description": "Search Bible books in Drave data"}`

  ```
data/jw/html/https_www_jw_org_en_library_magazines_watchtower_study_august_2026_Bible_Fact_E2_80_8B_The_Tree_That_Wakes_Up_Early_.html
data/pidgin.old/bible.json
data/pidgin.old/bible_web.json
data/pidgin.old/bible_narratif.json
done
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,os\nfor p in ['data/pidgin.old/bible.json','data/pidgin.old/bible_web.json','data/pidgin.old/bible_narratif.json']:\n    print('===',p,os.path.getsize(p))\n    d=json.load(open(p))\n    print(type(d), len(d))\n    if isinstance(d,dict):\n        print(list … [232 caractères tronqués]`

  ```
=== data/pidgin.old/bible.json 8422901
<class 'list'> 30950
[{"en": "Adam , Sheth , Enosh ,", "pcm": "Na Adam born Seth, Seth born Enosh, Enosh born Kenan"}, {"en": "Kenan , Mahalaleel , Jered ,", "pcm": "and na Kenan born Mahalalel. Na Mahalalel bi Jared papa."}]
=== data/pidgin.old/bible_web.json 7568957
<class 'list'> 30934
[{"en": "Adam, Seth , Enosh,", "pcm": "Na Adam born Seth, Seth born Enosh, Enosh born Kenan"}, {"en": "Kenan , Mahalalel , Jared ,", "pcm": "and na Kenan born Mahalalel. Na Mahalalel bi Jared papa."}]
=== data/pidgin.old/bible_narratif.json 2236969
<class 'list'> 7526
[{"en": "The first book I wrote, Theophilus , concerned all that Jesus began both to do and to teach ,", "pcm": "My friend Teofilus, for di book wey I first rite give yu, I tok about all di tins wey Jesus Christ start to dey do and tish,", "cle": "ACT.1.1"}, {"en": "until the day in which he was received up, after he had given commandment through the Holy Spirit to the apostles whom he had chosen .", "pcm": "until di day wen God kon karry am go heaven, afta e give orda to di apostles, wey e choose with di Holy Spirit.", "cle": "ACT.1.2"}]
  ```

- **bash** `{"command": "ls -la data/pidgin.old | head -40; du -sh data/pidgin.old", "description": "List pidgin.old"}`

  ```
total 319848
drwxr-xr-x. 1 stephane stephane       736 21 oct 14:30 .
drwxr-xr-x. 1 stephane stephane      2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane     35592 21 oct 14:30 asp_raw.json
-rw-r--r--. 1 stephane stephane   8422901 21 oct 06:10 bible.json
-rw-r--r--. 1 stephane stephane   2236969 21 oct 09:10 bible_narratif.json
-rw-r--r--. 1 stephane stephane   7568957 21 oct 06:21 bible_web.json
-rw-r--r--. 1 stephane stephane   2771083 21 oct 06:10 eng_kjv_usfm.zip
-rw-r--r--. 1 stephane stephane   3250185 21 oct 06:21 eng_web_usfm.zip
-rw-r--r--. 1 stephane stephane        55 21 oct 13:38 en_index_doublons.json
-rw-r--r--. 1 stephane stephane  40583572 21 oct 13:28 en_index.tsv
-rw-r--r--. 1 stephane stephane 226353342 21 oct 13:38 en_titles.tsv
drwxr-xr-x. 1 stephane stephane      6540 21 oct 02:13 html
-rw-r--r--. 1 stephane stephane   9901216 21 oct 04:55 mono_bbc_clean.json
-rw-r--r--. 1 stephane stephane  10272510 21 oct 04:54 mono_bbc.json
-rw-r--r--. 1 stephane stephane    158878 21 oct 04:19 mono.json
-rw-r--r--. 1 stephane stephane   1341437 21 oct 06:10 pcm_usfm.zip
-rw-r--r--. 1 stephane stephane    789511 21 oct 13:25 pcmwiki-latest-langlinks.sql.gz
-rw-r--r--
… [548 caractères tronqués]
  ```

- **bash** `{"command": "for f in daniel_book ezekiel_book isaiah_book jeremiah_book hosea_book zechariah_book 2_esdras book_of_enoch; do echo \"=== $f\"; head -c 400 \"../Panini/research/nipada/corpus/_cache/sources/$f.txt\"; echo; done", "description": "Inspect Panini Bible source headers"}`

  ```
=== daniel_book
Daniel Back to book Daniel The archive, offline Own the Wisdom of the Ages Every text in the library on a single USB drive. Read offline, cite freely, keep forever. No subscription required. Get the drive $127.00 Daniel King James Version: Daniel Sep:DaT Polyglot Sep:Dan | Tan | Vul Daniel Chapter 1 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 Daniel Chapter 2 1 2 3 4 5 6 7 8 9 10 11 12 1
=== ezekiel_book
Ezekiel Back to book Ezekiel The archive, offline Own the Wisdom of the Ages Every text in the library on a single USB drive. Read offline, cite freely, keep forever. No subscription required. Get the drive $127.00 Ezekiel King James Version: Ezekiel Polyglot Sep | Tan | Vul Ezekiel Chapter 1 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 Ezekiel Chapter 2 1 2 3 4 5 6 7
=== isaiah_book
Isaiah Back to book Isaiah The archive, offline Own the Wisdom of the Ages Every text in the library on a single USB drive. Read offline, cite freely, keep forever. No subscription required. Get the drive $127.00 Isaiah King James Version: Isaiah Polyglot Sep | Tan | Vul Isaiah Chapter 1 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 
… [2139 caractères tronqués]
  ```

- **bash** `{"command": "unzip -l data/pidgin.old/eng_kjv_usfm.zip | head -30; echo ---; unzip -l data/pidgin.old/eng_web_usfm.zip | head -10", "description": "List KJV/WEB USFM archive"}`

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
    84967  2026-10-20 20:37   18-ESTeng-kjv.usfm
   262508  2026-10-20 20:37   19-JOBeng-kjv.usfm
   661997  2026-10-20 20:37   20-PSAeng-kjv.usfm
   235046  2026-10-20 20:37   21-PROeng-kjv.usfm
    79896  2026-10-20 20:37   22-ECCeng-kjv.usfm
    39584
… [695 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,150p' docs/pilotage/semaine-autonome.md", "description": "Read week plan day 2"}`

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
… [4501 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"J2.2\\|corpus commun\\|20 textes\\|UDHR\" docs/pilotage/roadmap.md docs/pilotage/en-cours.md docs/pilotage/chantiers.md docs/pilotage/plan-travail.md | head -40", "description": "Search planning docs for J2.2"}`

  ```
docs/pilotage/roadmap.md:175:| **B10** | le protocole sémantique : encodeur `z`, décodeur, raisonnement | ✅ / ❌ / ⏳ | **B10.3 bloqué** ; 5 leviers : l'**objectif mot** lève le décodeur (**32,5** UDHR, **26,7** JW > plancher 17,1) mais le `z` ne porte que **1,5–2,6** points ; le **contrastif** ne le fait pas lire — le verrou est l'encodeur |
docs/pilotage/roadmap.md:356:| S — la banque validée | **`/paragraphes` fini** : 9/9 paragraphes, 19/19 candidats, 11 acceptés, 8 exclus, **11 verdicts non committés** ; **banque 150 verdicts / 74 des 207 phrases** (35,7 %), mais la page sert les **369 candidats du 02/11** sans `profondeur` ; **rétro-traduction absente** ; **71 langues = lexique B7**, pas l'UDHR, **0/71 testée** | committer les 11 verdicts (session S), servir la v7 (359 candidats, 99 à profondeur ≥ 3), décider la rétro-traduction |
  ```

- **bash** `{"command": "head -c 2000 ../Panini/research/data/udhr_demo.nipada; echo; echo ---; grep -o \"Article [0-9]*\" ../Panini/research/data/udhr_demo.nipada | sort -u | head -20", "description": "Inspect NIPADA demo format"}`

  ```
# ═══════════════════════════════════════════════════════════════════════════
# FORMAT .NIPADA v0.3.0 — UDHR Article 1 Demo Data
# ═══════════════════════════════════════════════════════════════════════════
# Auto-portant : toutes les données de la démo sont dans ce fichier.
# Aucun dictionnaire Python, aucune donnée externe.
# Le code ne fait que lire ce fichier et appliquer les règles.
# ═══════════════════════════════════════════════════════════════════════════

nipada: 0.3.0


# ═══════════════════════════════════════════════════════════════════════════
# §1 — 14 ∃ (atomes)  ·  1 codepoint Unicode  ·  catégorie Sm
# ═══════════════════════════════════════════════════════════════════════════
§1:
  ∃:  {iso: [eng:BEING,         fra:ÊTRE]}
  ∆:  {iso: [eng:DIFFERENCE,    fra:DIFFÉRENCE]}
  ∼:  {iso: [eng:RELATION,      fra:RAPPORT]}
  ↗:  {iso: [eng:ORIENTATION,   fra:ORIENTATION]}
  ⊙:  {iso: [eng:SUBJECT,       fra:SUJET]}
  ⧖:  {iso: [eng:TIME,          fra:TEMPS]}
  ◇:  {iso: [eng:MODALITY,      fra:MODALITÉ]}
  №:  {iso: [eng:NUMBER,        fra:NOMBRE]}
  ⊕:  {iso: [eng:SPACE,         fra:ESPACE]}
  ⊗:  {iso: [eng:OPERATION,     fra:OPÉRATION]}
  λ:  {iso: [eng:FUNCTION,     
… [24 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('data/udhr/articles.jsonl')) if False else None\n# count articles per language\nfrom collections import Counter\nc=Counter()\nfor line in open('data/udhr/articles.jsonl'):\n    o=json.loads(line); c[o['fichier']]+=1\nprint('langs',len(c), … [96 caractères tronqués]`

  ```
langs 456 article counts Counter({31: 445, 30: 4, 1: 4, 24: 2, 29: 1})
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, unicodedata\nfrom collections import defaultdict\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\ngene=json.load(open('data/udhr/genealogie.json'))\nfiles={}\nfor line in open('data/udhr/langues.jsonl'):\n    d=json.loads(lin … [1149 caractères tronqués]`

  ```
### Indo-European 120
007            cri      Latn  Sãotomense                          w= 31 c= 146 br=saot1242
008            pov      Latn  Crioulo, Upper Guinea (008)         w= 36 c= 200 br=uppe1458
afr            afr      Latn  Afrikaans                           w= 28 c= 162 br=afri1273
als            als      Latn  Albanian, Tosk                      w= 30 c= 171 br=alba1268
ast            ast      Latn  Asturian                            w= 29 c= 164 br=astu1244
auv            oci      Latn  Occitan (Auvergnat)                 w= 28 c= 157 br=occi1240
bel            bel      Cyrl  Belarusan                           w= 25 c= 154 br=east1426
ben            ben      Beng  Bengali                             w= 26 c= 168 br=gaud1238
bho            bho      Deva  Bhojpuri                            w= 34 c= 184 br=bhoj1246
bis            bis      Latn  Bislama                             w= 31 c= 148 br=earl1243
bos_latn       bos      Latn  Bosnian (Latin)                     w= 28 c= 164 br=east2821
bre            bre      Latn  Breton                              w= 33 c= 164 br=bret1245
bul            bul      Cyrl  Bulgarian                           w= 29 c= 147 br=mace
… [17002 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,240p' docs/methode/resultats.md", "description": "Read results method"}`

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

- **bash** `{"command": "sed -n '1,160p' docs/methode/rangement.md", "description": "Read filing method"}`

  ```
# Le rangement, et la revue de documentation

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). La règle la plus souvent violée du dépôt : à lire
> **avant de classer un fichier** ou de clore un sous-chantier.

## Les quatre dossiers (règle stricte)

| dossier | ce qu'il contient | ce qu'il ne contient **jamais** |
|---|---|---|
| **`docs/`** | quatre familles : **méthode**, **pilotage**, **théorie**, **implantation** — ce qui reste vrai quand les chiffres changent | des **résultats** de mesure, des tableaux de chiffres, des comptes rendus de round |
| **`reports/`** | les **résultats mesurés** : fiches, séries de mesures, tableaux, erratums, récits de round, JSON de résultats | la documentation de référence |
| **`journal/`** | le **récit daté** : ce qui a été fait, quand, et ce qu'on en a appris | les chiffres seuls (ils vont dans `reports/`) |
| **`data/`** | les corpus et leur généalogie (`data/udhr/`, `data/corpus_*.txt`, `data/eurlex/`) | du code |

Dans `docs/`, les quatre familles sont **séparées** : `methode/` (comment on travaille), `pilotage/` (où l'on en
est), `theorie/` (ce qui reste vrai), `implantation/` (comment c'est construit). Une page de `docs/`
… [4004 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,90p' reports/rapport-atomes-niveaux.md", "description": "Read atomes report style"}`

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
… [4506 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-niveaux.json'))\nprint(list(d.keys()))\nprint(json.dumps(d, ensure_ascii=False, indent=1)[:1500])\nEOF", "description": "Inspect atomes JSON structure"}`

  ```
['fiche', 'version', 'date', 'titre', 'statut', 'sources', 'niveaux', 'niveaux_du_contrat', 'principe', 'atomes', 'calibration_44_oeuvres', 'protocole', 'limites', 'prochaine_etape', 'fichiers']
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
   "note": "Le contrat compte 9 niveaux avec morphème ; le mandat J2.
… [494 caractères tronqués]
  ```

- **bash** `{"command": "date -u +%Y-%m-%dT%H:%M:%SZ; git log -1 --format='%H %ad %s' --date=short; git -C ../Panini/research log -1 --format='%H %ad %s' --date=short", "description": "Get current date and commits"}`

  ```
2026-11-07T20:03:03Z
9c7f71dc94986f50bdf4fcc58c728eea1e2d3b7a 2026-11-07 PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE
e10d695e65f52031222819cb1bdbb290d08f8e57 2026-10-25 docs(incident): la classe vue depuis les KITS — un False rapide est un kit incomplet, pas une preuve cassee ; diagnostic en une commande
  ```

- **bash** `{"command": "git status --short -- data/udhr ../Panini/research/data/udhr_corpus.json 2>/dev/null; sha256sum ../Panini/research/data/udhr_corpus.json data/udhr/articles_propres.jsonl data/udhr/langues.jsonl data/udhr/genealogie.json", "description": "Check source status and hashes"}`

  ```
531bc75c4d926cabc477165a6c7cd1ea70869ee0aa82d203053f30676d9cf190  ../Panini/research/data/udhr_corpus.json
7ccac9c3c641a72ac3aaa726c743ada8369d2419fbcb334c1da0a4833d2d7a6d  data/udhr/articles_propres.jsonl
12eee36241c1fc9ceb947a36406dcd357db523e87b50ebfa330b61a626a58dea  data/udhr/langues.jsonl
3d907676892fb16ee18a522998ef63e6403951f0e6ac5853f486342e1e54a30d  data/udhr/genealogie.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, re, unicodedata\nsel=['eng','hin','bel','ell_monotonic','kin','ewe','ibo','fuf_adlm','ind','tgl','mly_arab','jav','mya','bod','cmn_hant','cnh','arb','amh','heb','hau_NE']\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\n# sen … [872 caractères tronqués]`

  ```
### eng English | sents 2
  > All human beings are born free and equal in dignity and rights.
  > They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.
### hin Hindi | sents 1
  > सभी मनुष्यों को गौरव और अधिकारों के मामले में जन्मजात स्वतन्त्रता और समानता प्राप्त है । उन्हें बुद्धि और अन्तरात्मा की देन प्राप्त है और परस्पर उन्हें भाईचारे के भाव से बर्ताव करना चाहिए ।
### bel Belarusan | sents 2
  > Усе людзі нараджаюцца свабоднымі і роўнымі ў сваёй годнасці і правах.
  > Яны надзелены розумам і сумленнем і павінны ставіцца адзін да аднаго ў духу брацтва.
### ell_monotonic Greek (monotonic) | sents 2
  > Όλοι οι άνθρωποι γεννιούνται ελεύθεροι και ίσοι στην αξιοπρέπεια και τα δικαιώματα.
  > Είναι προικισμένοι με λογική και συνείδηση, και οφείλουν να συμπεριφέρονται μεταξύ τους με πνεύμα αδελφοσύνης.
### kin Rwanda | sents 2
  > Abantu bose bavuka aliko bakwiye agaciro no kwubahwa kimwe.
  > Bose bavukana ubwenge n'umutima, bagomba kugilirana kivandimwe.
### ewe Éwé | sents 2
  > Wodzi amegbetɔwo katã ablɔɖeviwoe eye wodzena bubu kple gomekpɔkpɔ sɔsɔe.
  > Susu kple dzitsinya le wo dometɔ ɖesiaɖe si eyata wodze be woanɔ anyi le ɖek
… [3063 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nmods=['sentencex','pysbd','nltk','spacy','stanza','icu','blingfire','syntok','segtok',' razdel']\nfor m in mods:\n    m=m.strip()\n    try:\n        __import__(m); print(m,'OK')\n    except Exception as e: print(m,'NO',type(e).__name__)\nEOF", "description": "Check se … [27 caractères tronqués]`

  ```
sentencex NO ModuleNotFoundError
pysbd NO ModuleNotFoundError
nltk NO ModuleNotFoundError
spacy NO ModuleNotFoundError
stanza NO ModuleNotFoundError
icu NO ModuleNotFoundError
blingfire NO ModuleNotFoundError
syntok NO ModuleNotFoundError
segtok NO ModuleNotFoundError
razdel NO ModuleNotFoundError
  ```

- **bash** `{"command": "which python3; python3 -V; pip list 2>/dev/null | grep -iE \"sentence|nltk|spacy|stanza|icu|bling|syntok|segtok|razdel\" | head", "description": "Check Python packages"}`

  ```
/usr/bin/python3
Python 3.13.16
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, re, unicodedata\nsel=['eng','hin','bel','ell_monotonic','kin','ewe','ibo','fuf_adlm','ind','tgl','mly_arab','jav','mya','cmn_hant','cnh','ctd','arb','amh','heb','hau_NE']\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\ndef n … [883 caractères tronqués]`

  ```
eng            n=2 :: All human beings are born free and equal in dignity and || They are endowed with reason and conscience and should 
hin            n=2 :: सभी मनुष्यों को गौरव और अधिकारों के मामले में जन्मजात स || उन्हें बुद्धि और अन्तरात्मा की देन प्राप्त है और परस्पर
bel            n=2 :: Усе людзі нараджаюцца свабоднымі і роўнымі ў сваёй годн || Яны надзелены розумам і сумленнем і павінны ставіцца ад
ell_monotonic  n=2 :: Όλοι οι άνθρωποι γεννιούνται ελεύθεροι και ίσοι στην αξ || Είναι προικισμένοι με λογική και συνείδηση, και οφείλου
kin            n=2 :: Abantu bose bavuka aliko bakwiye agaciro no kwubahwa ki || Bose bavukana ubwenge n'umutima, bagomba kugilirana kiv
ewe            n=2 :: Wodzi amegbetɔwo katã ablɔɖeviwoe eye wodzena bubu kple || Susu kple dzitsinya le wo dometɔ ɖesiaɖe si eyata wodze
ibo            n=2 :: A mụrụ mmadụ nile n'ohere nakwa nha anya ugwu na ikike. || E nyere ha uche na mmụọ ime ihe ziri ezi nke na ha kwes
fuf_adlm       n=2 :: 𞤋𞤲𞥆𞤢𞤥𞤢 𞤢𞥄𞤣𞤫𞥅𞤶𞤭 𞤬𞤮𞤬 𞤨𞤮𞤼𞤭، 𞤲'𞤣𞤭𞤥𞤯𞤭𞤣𞤭 𞤫 𞤶𞤭𞤦𞤭𞤲𞤢𞤲𞥆𞤣𞤫 𞤼𞤮 𞤦𞤢𞤲𞥆 || 𞤉𞤩𞤫 𞤲'𞤺𞤮𞥅𞤣𞤭 𞤥𞤭𞥅𞤶𞤮 𞤫 𞤸𞤢𞤳𞥆𞤭𞤤𞤢𞤲𞤼𞤢𞥄𞤺𞤢𞤤 𞤫𞤼𞤫 𞤫𞤩𞤫 𞤨𞤮𞤼𞤭 𞤸𞤵𞥅𞤬𞤮 𞤲
ind            n=2 :: Semua orang dilahirkan merdeka dan mempunyai martabat d || Mereka dikaruniai akal 
… [1406 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\ns='የሰው፡ልጅ፡ሁሉ፡ሲወለድ፡ነጻና፡በክብርና፡በመብትም፡እኩልነት፡ያለው፡ነው።፡የተፈጥሮ፡ማስተዋልና፡ሕሊና፡ስላለው፡አንዱ፡ሌላውን፡በወንድማማችነት፡መንፈስ፡መመልከት፡ይገባዋል።'\nfor i,ch in enumerate(s):\n    if ch in '።፡':\n        print(i, hex(ord(ch)), repr(ch), repr(s[max(0,i-10):i+10]))\nEOF", "description": "Inspect Amharic punct … [19 caractères tronqués]`

  ```
3 0x1361 '፡' 'የሰው፡ልጅ፡ሁሉ፡ሲወለ'
6 0x1361 '፡' 'የሰው፡ልጅ፡ሁሉ፡ሲወለድ፡ነ'
9 0x1361 '፡' 'የሰው፡ልጅ፡ሁሉ፡ሲወለድ፡ነጻና፡'
14 0x1361 '፡' 'ልጅ፡ሁሉ፡ሲወለድ፡ነጻና፡በክብርና'
18 0x1361 '፡' 'ሉ፡ሲወለድ፡ነጻና፡በክብርና፡በመብ'
24 0x1361 '፡' '፡ነጻና፡በክብርና፡በመብትም፡እኩል'
30 0x1361 '፡' 'ክብርና፡በመብትም፡እኩልነት፡ያለው'
36 0x1361 '፡' 'መብትም፡እኩልነት፡ያለው፡ነው።፡የ'
40 0x1361 '፡' '፡እኩልነት፡ያለው፡ነው።፡የተፈጥሮ'
43 0x1362 '።' 'ልነት፡ያለው፡ነው።፡የተፈጥሮ፡ማስ'
44 0x1361 '፡' 'ነት፡ያለው፡ነው።፡የተፈጥሮ፡ማስተ'
50 0x1361 '፡' '፡ነው።፡የተፈጥሮ፡ማስተዋልና፡ሕሊ'
57 0x1361 '፡' 'ፈጥሮ፡ማስተዋልና፡ሕሊና፡ስላለው፡'
61 0x1361 '፡' 'ማስተዋልና፡ሕሊና፡ስላለው፡አንዱ፡'
66 0x1361 '፡' 'ና፡ሕሊና፡ስላለው፡አንዱ፡ሌላውን፡'
70 0x1361 '፡' 'ና፡ስላለው፡አንዱ፡ሌላውን፡በወንድ'
75 0x1361 '፡' 'ው፡አንዱ፡ሌላውን፡በወንድማማችነት'
85 0x1361 '፡' '፡በወንድማማችነት፡መንፈስ፡መመልከ'
90 0x1361 '፡' 'ማማችነት፡መንፈስ፡መመልከት፡ይገባ'
96 0x1361 '፡' 'መንፈስ፡መመልከት፡ይገባዋል።'
102 0x1362 '።' 'መልከት፡ይገባዋል።'
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, re, unicodedata\nsel=['eng','hin','bel','ell_monotonic','kin','ewe','ibo','fuf_adlm','ind','tgl','mly_arab','jav','mya','cmn_hant','cnh','ctd','arb','amh','heb','hau_NE']\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\ndef n … [718 caractères tronqués]`

  ```
eng            Latn  n=2 words=12 chars=169
hin            Deva  n=2 words=16 chars=188
bel            Cyrl  n=2 words=11 chars=153
ell_monotonic  Grek  n=2 words=12 chars=193
kin            Latn  n=2 words=9 chars=122
ewe            Latn  n=2 words=10 chars=164
ibo            Latn  n=2 words=11 chars=156
fuf_adlm       Adlm  n=2 words=10 chars=153
ind            Latn  n=2 words=11 chars=180
tgl            Latn  n=2 words=14 chars=191
mly_arab       Arab  n=2 words=11 chars=160
jav            Latn  n=2 words=12 chars=191
mya            Mymr  n=2 words=10 chars=261
cmn_hant       Hant  n=2 words=1 chars=43
cnh            Latn  n=2 words=25 chars=291
ctd            Latn  n=2 words=16 chars=220
arb            Arab  n=2 words=8 chars=115
amh            Ethi  n=2 words=1 chars=102
heb            Hebr  n=2 words=9 chars=125
hau_NE         Latn  n=2 words=19 chars=221
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, unicodedata\nfrom collections import Counter\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nfiles={}\nfor line in open('data/udhr/langues.jsonl'):\n    d=json.loads(line); files[d['fichier']]=d\nart={}\nfor line in open('da … [1412 caractères tronqués]`

  ```
exact 418 diff 20 noart 15 nofile 79
noart: ['bin', 'csw', 'iii', 'ike', 'kha', 'khk_mong', 'lia', 'lus', 'nym', 'ojb', 'qxu', 'taj', 'tgl_tglg', 'tzm_tfng', 'umb']
diff: ['ady', 'bfa', 'boa', 'bos_cyrl', 'cbi', 'cmn_hans', 'csa', 'dyu', 'hau_NG', 'hrv', 'kat', 'khm', 'kjh', 'oaa', 'pcd', 'piu', 'shp', 'sme', 'ykg', 'yor']
drave art1 not panini 2 ['udhr_012.xml', 'udhr_prq.xml']
selected
eng            Latn  Indo-European        macr1271   [Indo-European/Germanic/western_modern] English
fra            Latn  Indo-European        glob1239   [Indo-European/Romance/western_modern] French
hin            Deva  Indo-European        hind1270   [Indo-European/Indo-Iranian/indian] Hindi
bel            Cyrl  Indo-European        east1426   [Indo-European/Slavic/western_modern] Belarusan
ell_monotonic  Grek  Indo-European        nucl1783   [Indo-European/Hellenic/western_classical] Greek (monotonic)
kin            Latn  Atlantic-Congo       rwan1241   [Niger-Congo/Bantu/african] Rwanda
ewe            Latn  Atlantic-Congo       ewei1234   [Other/Unknown/other] Éwé
ibo            Latn  Atlantic-Congo       cent2417   [Niger-Congo/Volta-Niger/african] Igbo
fuf_adlm       Adlm  Atlantic-Congo     
… [1249 caractères tronqués]
  ```

- **todo_write** `{"todos": [{"content": "Inspect Panini/Drave UDHR sources and fix the 20+1 sample", "status": "in_progress"}, {"content": "Write tools/corpus_commun.py (build, verify, negative control)", "status": "pending"}, {"content": "Build work/corpus-commun/ and inspect normalized output", "status": "pending" … [289 caractères tronqués]`

  ```
Updated todo list: 5 pending, 1 in progress, 0 completed.
  ```

- **bash** `{"command": "sed -n '1,220p' docs/pilotage/en-cours.md", "description": "Read current state"}`

  ```
# En ce moment

**Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**

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
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 11** : serveurs loca
… [10132 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"J2\\.1\\|J2\\.2\\|Panini I\\|semaine Panini\" docs/pilotage/roadmap.md | head -20; echo ---; sed -n '1,80p' docs/pilotage/roadmap.md", "description": "Inspect roadmap header and J2 lines"}`

  ```
---
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
- **Le carpe diem** : pas d'échéance. Un chantier est **[fait](../theorie/glossaire/ent
… [13854 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p work/corpus-commun reports && ls -ld work/corpus-commun", "description": "Create output directory"}`

  ```
drwxr-xr-x. 1 stephane stephane 0  7 nov 15:05 work/corpus-commun
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nc=collections.Counter()\nfor line in open('data/udhr/articles_propres.jsonl'):\n    d=json.loads(line)\n    if d['art']==1: c[d['fichier']]+=1\nprint('dups',[x for x in c.items() if x[1]>1][:10])\nEOF", "description": "Check duplicate article … [12 caractères tronqués]`

  ```
dups []
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py", "content": "#!/usr/bin/env python3\n\"\"\"Corpus commun Panini/NIPADA ↔ Drave — UDHR article 1 (tâche J2.2).\n\nLe corpus est écrit dans ``work/corpus-commun/`` (non versionné) ; la fiche\n``reports/rapport-corpu … [43070 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/corpus_commun.py --tout", "description": "Build and verify common corpus"}`

  ```
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "find work/corpus-commun -maxdepth 2 -type f | sort | sed -n '1,50p'; echo ---; wc -l work/corpus-commun/corpus.jsonl work/corpus-commun/metadata.tsv; echo ---; sed -n '1,25p' work/corpus-commun/metadata.tsv", "description": "Inspect corpus output files"}`

  ```
work/corpus-commun/controle-negatif.json
work/corpus-commun/corpus.jsonl
work/corpus-commun/index.json
work/corpus-commun/metadata.tsv
work/corpus-commun/README.md
work/corpus-commun/sources.sha256
work/corpus-commun/textes/udhr_amh.txt
work/corpus-commun/textes/udhr_arb.txt
work/corpus-commun/textes/udhr_bel.txt
work/corpus-commun/textes/udhr_cmn_hant.txt
work/corpus-commun/textes/udhr_cnh.txt
work/corpus-commun/textes/udhr_ctd.txt
work/corpus-commun/textes/udhr_ell_monotonic.txt
work/corpus-commun/textes/udhr_eng.txt
work/corpus-commun/textes/udhr_ewe.txt
work/corpus-commun/textes/udhr_fra.txt
work/corpus-commun/textes/udhr_fuf_adlm.txt
work/corpus-commun/textes/udhr_hau_NE.txt
work/corpus-commun/textes/udhr_heb.txt
work/corpus-commun/textes/udhr_hin.txt
work/corpus-commun/textes/udhr_ibo.txt
work/corpus-commun/textes/udhr_ind.txt
work/corpus-commun/textes/udhr_jav.txt
work/corpus-commun/textes/udhr_kin.txt
work/corpus-commun/textes/udhr_mly_arab.txt
work/corpus-commun/textes/udhr_mya.txt
work/corpus-commun/textes/udhr_tgl.txt
---
   42 work/corpus-commun/corpus.jsonl
   22 work/corpus-commun/metadata.tsv
   64 total
---
id	iso3	langue	script	famille	branche_feuille	genre	epoque	
… [3232 caractères tronqués]
  ```

- **bash** `{"command": "for f in eng hin mya cmn_hant amh; do echo \"=== $f\"; cat work/corpus-commun/textes/udhr_$f.txt; done", "description": "Inspect sample text files"}`

  ```
=== eng
All human beings are born free and equal in dignity and rights.
They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.
=== hin
सभी मनुष्यों को गौरव और अधिकारों के मामले में जन्मजात स्वतन्त्रता और समानता प्राप्त है ।
उन्हें बुद्धि और अन्तरात्मा की देन प्राप्त है और परस्पर उन्हें भाईचारे के भाव से बर्ताव करना चाहिए ।
=== mya
လူတိုင်းသည် တူညီ လွတ်လပ်သော ဂုဏ်သိက္ခာဖြင့် လည်းကောင်း၊ တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့် လည်းကောင်း၊ မွေးဖွားလာသူများ ဖြစ်သည်။
ထိုသူတို့၌ ပိုင်းခြား ဝေဖန်တတ်သော ဉာဏ်နှင့် ကျင့်ဝတ် သိတတ်သော စိတ်တို့ရှိကြ၍ ထိုသူတို့သည် အချင်းချင်း မေတ္တာထား၍ ဆက်ဆံကျင့်သုံးသင့်၏။
=== cmn_hant
人人生而自由，在尊嚴和權利上一律平等。
他們賦有理性和良心，並應以兄弟關係的精神相對待。
=== amh
የሰው፡ልጅ፡ሁሉ፡ሲወለድ፡ነጻና፡በክብርና፡በመብትም፡እኩልነት፡ያለው፡ነው።
የተፈጥሮ፡ማስተዋልና፡ሕሊና፡ስላለው፡አንዱ፡ሌላውን፡በወንድማማችነት፡መንፈስ፡መመልከት፡ይገባዋል።
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nidx=json.load(open('work/corpus-commun/index.json'))\nprint('keys', list(idx))\nprint('stats', json.dumps(idx['statistiques'], ensure_ascii=False, indent=1))\nprint('intersection', json.dumps({k:v for k,v in idx['intersection'].items() if k!='listes'}, en … [235 caractères tronqués]`

  ```
keys ['controles', 'date', 'fichiers', 'limites', 'normalisation', 'prochaine_etape', 'selection', 'sources', 'statistiques', 'textes', 'titre', 'version']
stats {
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
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
KeyError: 'intersection'
[exit code: 
… [2 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nc=json.load(open('work/corpus-commun/controle-negatif.json'))\nprint(json.dumps(c, ensure_ascii=False, indent=1))\nprint('---- corpus.jsonl first 2')\nfor i,line in enumerate(open('work/corpus-commun/corpus.jsonl')):\n    print(line.strip())\n    if i>=1: … [67 caractères tronqués]`

  ```
{
 "date": "2026-11-07",
 "n_ok": 8,
 "n_tests": 8,
 "tests": [
  {
   "attendu": "acceptation",
   "detail": "udhr_eng : Panini == Drave après normalisation",
   "nom": "temoin_paire_correcte",
   "obtenu": "acceptation",
   "ok": true
  },
  {
   "attendu": "rejet",
   "detail": "un caractère changé dans le texte Panini doit casser l'égalité",
   "nom": "panini_altere",
   "obtenu": "rejet",
   "ok": true
  },
  {
   "attendu": "rejet",
   "detail": "un caractère changé dans le texte Drave doit casser l'égalité",
   "nom": "drave_altere",
   "obtenu": "rejet",
   "ok": true
  },
  {
   "attendu": "rejet",
   "detail": "deux langues différentes ne doivent pas être appariables",
   "nom": "appariement_croise",
   "obtenu": "rejet",
   "ok": true
  },
  {
   "attendu": "rejet",
   "detail": "nb_phrases 1 != 2; caractères perdus ou ajoutés (hors espaces)",
   "nom": "phrase_supprimee",
   "obtenu": "rejet",
   "ok": true
  },
  {
   "attendu": "rejet",
   "detail": "nb_phrases 3 != 2; ligne vide",
   "nom": "ligne_vide",
   "obtenu": "rejet",
   "ok": true
  },
  {
   "attendu": "rejet",
   "detail": "une empreinte différente doit être refusée",
   "nom": "empreinte_fausse",
   "obte
… [1061 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\nprint('keys', list(r))\nprint('stats', json.dumps(r['statistiques'], ensure_ascii=False, indent=1))\nprint('intersection', json.dumps({k:v for k,v in r['intersection'].items() if k!='listes'}, ensure_ascii= … [260 caractères tronqués]`

  ```
keys ['controle_negatif', 'controles', 'date', 'fiche', 'fichiers', 'intersection', 'ligne_roadmap', 'limites', 'normalisation', 'prochaine_etape', 'selection', 'sources', 'statistiques', 'statut', 'textes', 'titre', 'version']
stats {
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
intersection {
 "appariables_article1": 438,
 "
… [1576 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' work/corpus-commun/README.md", "description": "Inspect generated README"}`

  ```
# Corpus commun Panini/NIPADA ↔ Drave — UDHR article 1

> **Corpus local, non versionné.** `work/` est ignoré par git. La fiche versionnée est
> `reports/rapport-corpus-commun.md` ; le JSON versionné est `reports/corpus-commun.json`.
> Date : 2026-11-07 · outil : `tools/corpus_commun.py` · version : 1.0.

## Ce que c'est

L'intersection **exacte** de l'article 1 de la Déclaration universelle des droits de l'homme
(DUDH, 1948) entre :

- Panini/NIPADA : `../Panini/research/data/udhr_corpus.json` (532 langues) ;
- Drave : `data/udhr/articles_propres.jsonl` (456 langues, article 1).

21 textes (20 stratifiés + 1 pivot),
5 familles, 10 écritures, 42 phrases.

## Contenu

| fichier | contenu |
|---|---|
| `textes/<id>.txt` | le texte normalisé, **une phrase par ligne**, UTF-8, LF, sans ligne vide |
| `corpus.jsonl` | une phrase par ligne + métadonnées (id, langue, famille, époque, rôle) |
| `metadata.tsv` | une ligne par texte, colonnes fixes |
| `index.json` | manifeste complet (sources, sélection, contrôles, textes) |
| `sources.sha256` | empreintes des sources et de l'outil |
| `controle-negatif.json` | tests de rejet (altération, phrase supprimée, ligne vide, etc.) |

## Reproductio
… [1296 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nidx=json.load(open('work/corpus-commun/index.json'))\nprint(json.dumps(idx['sources'], ensure_ascii=False, indent=1))\nEOF", "description": "Check source info"}`

  ```
{
 "commune": {
  "note": "même source XML des deux côtés ; Drave normalise les codes en iso3.",
  "source": "eric-muller/udhr (Unicode UDHR XML Project)",
  "url": "https://github.com/eric-muller/udhr"
 },
 "drave": {
  "date": "2026-11-07",
  "depot": "Qtrinet",
  "fichiers": {
   "data/udhr/articles_propres.jsonl": "7ccac9c3c641a72ac3aaa726c743ada8369d2419fbcb334c1da0a4833d2d7a6d",
   "data/udhr/genealogie.json": "3d907676892fb16ee18a522998ef63e6403951f0e6ac5853f486342e1e54a30d",
   "data/udhr/langues.jsonl": "12eee36241c1fc9ceb947a36406dcd357db523e87b50ebfa330b61a626a58dea"
  },
  "head": "9c7f71dc94986f50bdf4fcc58c728eea1e2d3b7a"
 },
 "panini": {
  "article": "Article 1",
  "date": "2026-10-25",
  "depot": "Panini/research",
  "fichier": "../Panini/research/data/udhr_corpus.json",
  "fichier_modifie_avant": false,
  "format": "udhr-v2.0-xml",
  "head": "e10d695e65f52031222819cb1bdbb290d08f8e57",
  "lecture_seule": true,
  "sha256": "531bc75c4d926cabc477165a6c7cd1ea70869ee0aa82d203053f30676d9cf190",
  "source_declaree": "eric-muller/udhr (GitHub) — Unicode UDHR XML Project",
  "total_languages": 532
 }
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\nfor x in r['textes']:\n    print(f\"| `{x['id']}` | {x['langue']} | {x['script']} | {x['famille']} | `{x['branche_feuille']}` | {x['role']} | {x['nb_phrases']} | {x['nb_caracteres']} |\")\nprint('\\n--- eca … [430 caractères tronqués]`

  ```
| `udhr_eng` | English | Latn | Indo-European | `macr1271` | strate | 2 | 170 |
| `udhr_hin` | Hindi | Deva | Indo-European | `hind1270` | strate | 2 | 189 |
| `udhr_bel` | Belarusan | Cyrl | Indo-European | `east1426` | strate | 2 | 154 |
| `udhr_ell_monotonic` | Greek (monotonic) | Grek | Indo-European | `nucl1783` | strate | 2 | 194 |
| `udhr_kin` | Rwanda | Latn | Atlantic-Congo | `rwan1241` | strate | 2 | 123 |
| `udhr_ewe` | Éwé | Latn | Atlantic-Congo | `ewei1234` | strate | 2 | 165 |
| `udhr_ibo` | Igbo | Latn | Atlantic-Congo | `cent2417` | strate | 2 | 157 |
| `udhr_fuf_adlm` | Pular (Adlam) | Adlm | Atlantic-Congo | `fula1264` | strate | 2 | 154 |
| `udhr_ind` | Indonesian | Latn | Austronesian | `stan1327` | strate | 2 | 181 |
| `udhr_tgl` | Tagalog | Latn | Austronesian | `taga1269` | strate | 2 | 192 |
| `udhr_mly_arab` | Malay (Arabic) | Arab | Austronesian | `sing1270` | strate | 2 | 161 |
| `udhr_jav` | Javanese (Latin) | Latn | Austronesian | `glob1245` | strate | 2 | 192 |
| `udhr_mya` | Burmese | Mymr | Sino-Tibetan | `nucl1811` | strate | 2 | 262 |
| `udhr_cmn_hant` | Chinese, Mandarin (Traditional) | Hant | Sino-Tibetan | `mand1471` | strate | 2 | 43 |
| `udhr
… [1469 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nprint([k for k in p if k.startswith('012') or k=='prq'])\nprint('012' in p, 'prq' in p)\nEOF", "description": "Check Panini keys 012/prq"}`

  ```
[]
False False
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, unicodedata\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nart={}\nfor line in open('data/udhr/articles_propres.jsonl'):\n    d=json.loads(line)\n    if d['art']==1: art[d['fichier']]=d\ndef norm(s):\n    s=unicodedata.norm … [456 caractères tronqués]`

  ```
### ady len 162 162 first diff 1
P: 'Цӏыф пстэури шъхьэфитэу, я'
D: 'ЦIыф пстэури шъхьэфитэу, я'
### cmn_hans len 43 43 first diff 6
P: '人人生而自由，在尊严和权利上一律平等。他们赋有理性和良心，并应'
D: '人人生而自由,在尊严和权利上一律平等。他们赋有理性和良心,并应'
### hrv len 164 164 first diff 19
P: 'Sva ljudska bića rađaju se slobodna i jednak'
D: 'Sva ljudska bića raćaju se slobodna i jednak'
### hau_NG len 225 225 first diff 7
P: 'Su dai ’yan-adam, ana haifuwarsu'
D: 'Su dai ‘yan-adam, ana haifuwarsu'
### yor len 166 172 first diff 42
P: 'a bí ní òmìnira; iyì àti ẹ̀tọ́ kọ̀ọ̀kan sì dọ́gba.'
D: 'a bí ní òmìnira; iyì àti è̩tó̩ kò̩ò̩kan sì dó̩gba.'
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py", "old_string": "- **Comptage des mots** : `nb_mots_ws` est un comptage sur les espaces ; il vaut 1 pour le chinois\n  et l'amharique, qui ne séparent pas les mots par des espaces. Ce n'est pas une tokenisation.",  … [225 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py", "old_string": "    index[\"fichiers\"] = {\n        \"index\": \"work/corpus-commun/index.json\",", "new_string": "    index[\"intersection\"] = {\n        k: v for k, v in intersection.items() if k != \"listes\" … [93 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py", "old_string": "    if ecrire_rapport:\n        rapport = fabriquer_rapport(index, records, intersection, controle)\n        RAPPORT_JSON.parent.mkdir(parents=True, exist_ok=True)\n        RAPPORT_JSON.write_text( … [1179 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py", "old_string": "    with tempfile.TemporaryDirectory(dir=sortie.parent, prefix=\".verif-corpus-\") as tmp:\n        tmp_path = Path(tmp)\n        construire(tmp_path, ecrire_rapport=False)\n        erreurs.extend( … [847 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py", "old_string": "    if any(not t.get(\"ok\") for t in controle_attendu.get(\"tests\", [])):\n        erreurs.append(\"controle-negatif.json: un test a échoué\")\n\n    return erreurs", "new_string": "    if any(no … [620 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py", "old_string": "            \"egalite_exacte\": {\n                \"n\": len(records),\n                \"attendu\": len(records),\n                \"verdict\": \"PASS\",\n            },", "new_string": "         … [357 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/corpus_commun.py --tout", "description": "Rebuild and verify after edits"}`

  ```
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nidx=json.load(open('work/corpus-commun/index.json'))\nprint('keys', list(idx))\nprint('intersection', json.dumps(idx['intersection'], ensure_ascii=False, indent=1))\nprint('controles', json.dumps(idx['controles'], ensure_ascii=False, indent=1))\nEOF", "de … [53 caractères tronqués]`

  ```
keys ['controles', 'date', 'fichiers', 'intersection', 'limites', 'normalisation', 'prochaine_etape', 'selection', 'sources', 'statistiques', 'textes', 'titre', 'version']
intersection {
 "appariables_article1": 438,
 "article1_drave": 440,
 "drave_article1_hors_panini": 2,
 "drave_langues": 456,
 "ecarts_surface": 20,
 "exacts": 418,
 "familles_exactes": {
  "(inconnue)": 10,
  "Abkhaz-Adyge": 2,
  "Afro-Asiatic": 12,
  "Algic": 1,
  "Araucanian": 1,
  "Arawakan": 7,
  "Artificial Language": 3,
  "Athabaskan-Eyak-Tlingit": 1,
  "Atlantic-Congo": 81,
  "Austroasiatic": 3,
  "Austronesian": 37,
  "Aymaran": 1,
  "Barbacoan": 1,
  "Cahuapanan": 1,
  "Chicham": 4,
  "Dravidian": 5,
  "Eskimo-Aleut": 1,
  "Guaicuruan": 1,
  "Harakmbut": 1,
  "Hmong-Mien": 3,
  "Huitotoan": 1,
  "Indo-European": 120,
  "Iroquoian": 2,
  "Japonic": 1,
  "Koreanic": 1,
  "Mande": 7,
  "Mayan": 11,
  "Misumalpan": 1,
  "Mixe-Zoque": 1,
  "Mongolic-Khitan": 1,
  "Muskogean": 1,
  "Nilotic": 4,
  "Otomanguean": 7,
  "Pano-Tacanan": 5,
  "Peba-Yagua": 1,
  "Quechuan": 11,
  "Saharan": 1,
  "Sino-Tibetan": 17,
  "Songhay": 1,
  "Tai-Kadai": 7,
  "Tarascan": 1,
  "Ticuna-Yuri": 1,
  "Totonacan": 1,
  "Tucanoan"
… [451 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\ni=r['intersection']\nprint('453/456', round(453/456*100,1))\nprint('453/532', round(453/532*100,1))\nprint('418/438', round(418/438*100,1))\nprint('418/440', round(418/440*100,1))\nprint('418/532', round(41 … [335 caractères tronqués]`

  ```
453/456 99.3
453/532 85.2
418/438 95.4
418/440 95.0
418/532 78.6
20/438 4.6
top families
| (inconnue) | 10 | 2.4 % |
| Abkhaz-Adyge | 2 | 0.5 % |
| Afro-Asiatic | 12 | 2.9 % |
| Algic | 1 | 0.2 % |
| Araucanian | 1 | 0.2 % |
| Arawakan | 7 | 1.7 % |
| Artificial Language | 3 | 0.7 % |
| Athabaskan-Eyak-Tlingit | 1 | 0.2 % |
| Atlantic-Congo | 81 | 19.4 % |
| Austroasiatic | 3 | 0.7 % |
| Austronesian | 37 | 8.9 % |
| Aymaran | 1 | 0.2 % |
selected share
Afro-Asiatic 4 19.0
Atlantic-Congo 4 19.0
Austronesian 4 19.0
Indo-European 5 23.8
Sino-Tibetan 4 19.0
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "content": "# Corpus commun Panini/NIPADA ↔ Drave — UDHR, article 1\n\n> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.2 · **Date** : 2026-11-07\n> **Verdict** : ✅ **l … [19245 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\nl=r['intersection']['listes']['sans_fichier_drave']\nprint(len(l))\nprint(l)\nEOF", "description": "Inspect 79 missing Drave files"}`

  ```
79
['udhr_021.xml', 'udhr_022.xml', 'udhr_023.xml', 'udhr_025.xml', 'udhr_026.xml', 'udhr_027.xml', 'udhr_028.xml', 'udhr_029.xml', 'udhr_030.xml', 'udhr_032.xml', 'udhr_041.xml', 'udhr_042.xml', 'udhr_043.xml', 'udhr_044.xml', 'udhr_045.xml', 'udhr_046.xml', 'udhr_047.xml', 'udhr_048.xml', 'udhr_049.xml', 'udhr_050.xml', 'udhr_052.xml', 'udhr_053.xml', 'udhr_054.xml', 'udhr_055.xml', 'udhr_056.xml', 'udhr_057.xml', 'udhr_058.xml', 'udhr_059.xml', 'udhr_060.xml', 'udhr_061.xml', 'udhr_062.xml', 'udhr_063.xml', 'udhr_064.xml', 'udhr_065.xml', 'udhr_066.xml', 'udhr_067.xml', 'udhr_068.xml', 'udhr_069.xml', 'udhr_071.xml', 'udhr_072.xml', 'udhr_aar.xml', 'udhr_ayo.xml', 'udhr_bvi.xml', 'udhr_cas.xml', 'udhr_chv.xml', 'udhr_cmn_hans_beijing.xml', 'udhr_cmn_hans_guiyang.xml', 'udhr_cmn_hans_harbin.xml', 'udhr_cmn_hans_nanjing.xml', 'udhr_cmn_hans_tianjin.xml', 'udhr_cnr.xml', 'udhr_crh.xml', 'udhr_ese.xml', 'udhr_fuv2.xml', 'udhr_fvr.xml', 'udhr_gnw.xml', 'udhr_gsw1.xml', 'udhr_hau_3.xml', 'udhr_hsn.xml', 'udhr_idu.xml', 'udhr_ijs.xml', 'udhr_jpn_osaka.xml', 'udhr_jpn_tokyo.xml', 'udhr_kaa.xml', 'udhr_kqs.xml', 'udhr_mal_chillus.xml', 'udhr_mor.xml', 'udhr_mtp.xml', 'udhr_niv.xml', 'udh
… [156 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "`nym`, `ojb`, `qxu`, `taj`, `tgl_tglg`, `tzm_tfng`, `umb`. **Les 2 Drave hors Panini** :\n`udhr_012.xml`, `udhr_prq.xml`. **Les 79 sans fichier Drave** sont surtout des variantes\nnumériq … [456 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/corpus_commun.py --verifier; echo \"exit=$?\"; python3 tools/corpus_commun.py --controle-negatif | tail -5", "description": "Run verifier and negative control"}`

  ```
VERIFIER: PASS
exit=0
      "ok": true
    }
  ],
  "verdict": "PASS"
}
  ```

- **bash** `{"command": "set -e\nn=0\nfor f in work/corpus-commun/textes/*.txt; do\n  iconv -f UTF-8 -t UTF-8 \"$f\" >/dev/null\n  lines=$(wc -l < \"$f\")\n  empty=$(grep -c '^$' \"$f\" || true)\n  [ \"$lines\" -eq 2 ] || { echo \"BAD LINES $f $lines\"; exit 1; }\n  [ \"$empty\" -eq 0 ] || { echo \"EMPTY $f $em … [230 caractères tronqués]`

  ```
UTF8+LINES OK: 21 fichiers
.gitignore:23:work/	work/corpus-commun/index.json
531bc75c4d926cabc477165a6c7cd1ea70869ee0aa82d203053f30676d9cf190  ../Panini/research/data/udhr_corpus.json
  ```

- **bash** `{"command": "wc -l -w reports/rapport-corpus-commun.md reports/corpus-commun.json tools/corpus_commun.py; echo ---; grep -n \"TODO\\|FIXME\\|XXX\" reports/rapport-corpus-commun.md tools/corpus_commun.py || true", "description": "Check report size and TODOs"}`

  ```
309   3146 reports/rapport-corpus-commun.md
  1406   2784 reports/corpus-commun.json
  1081   3817 tools/corpus_commun.py
  2796   9747 total
---
  ```

- **bash** `{"command": "python3 -m py_compile tools/corpus_commun.py && echo PYCOMPILE-OK; python3 - <<'EOF'\nimport json\nfor p in ['reports/corpus-commun.json','work/corpus-commun/index.json','work/corpus-commun/controle-negatif.json']:\n    json.load(open(p)); print('JSON OK', p)\nEOF", "description": "Comp … [23 caractères tronqués]`

  ```
PYCOMPILE-OK
JSON OK reports/corpus-commun.json
JSON OK work/corpus-commun/index.json
JSON OK work/corpus-commun/controle-negatif.json
  ```

- **bash** `{"command": "git -C ../Panini/research diff --quiet -- data/udhr_corpus.json; echo \"diff=$?\"; git -C ../Panini/research diff --cached --quiet -- data/udhr_corpus.json; echo \"cached=$?\"; git -C ../Panini/research status --porcelain -- data/udhr_corpus.json; echo \"status_done\"", "description": " … [32 caractères tronqués]`

  ```
diff=0
cached=0
?? data/udhr_corpus.json
status_done
  ```

- **bash** `{"command": "git status --short -- data/udhr reports/corpus-commun.json reports/rapport-corpus-commun.md tools/corpus_commun.py docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal | sed -n '1,80p'", "description": "Check git status of our paths"}`

  ```
?? reports/corpus-commun.json
?? reports/rapport-corpus-commun.md
?? tools/corpus_commun.py
  ```

- **bash** `{"command": "git -C ../Panini/research ls-files --error-unmatch data/udhr_corpus.json >/dev/null 2>&1; echo \"ls-files=$?\"; git -C ../Panini/research check-ignore -v data/udhr_corpus.json; echo \"check-ignore=$?\"; git -C ../Panini/research status --porcelain --untracked-files=no -- data/udhr_corpu … [73 caractères tronqués]`

  ```
ls-files=1
check-ignore=1
done
  ```

- **bash** `{"command": "grep -n \"def fichier_suivi_modifie\\|fichier_modifie_avant\\|def git_info\" -A18 -B2 tools/corpus_commun.py", "description": "Locate source status code"}`

  ```
133-
134-
135:def git_info(depot: Path) -> dict[str, Any]:
136-    """HEAD et date, en lecture seule. Ne lève jamais."""
137-    def run(*args: str) -> subprocess.CompletedProcess[str] | None:
138-        try:
139-            return subprocess.run(
140-                ["git", "-C", str(depot), *args],
141-                capture_output=True,
142-                text=True,
143-                timeout=10,
144-                check=False,
145-            )
146-        except (OSError, subprocess.TimeoutExpired):
147-            return None
148-
149-    head = run("log", "-1", "--format=%H")
150-    date = run("log", "-1", "--format=%ad", "--date=short")
151-    return {
152-        "depot": str(depot.relative_to(RACINE.parent))
153-        if depot.is_relative_to(RACINE.parent)
--
158-
159-
160:def fichier_suivi_modifie(depot: Path, relatif: str) -> bool | None:
161-    """True si le fichier suivi a une différence (index ou travail). None si git échoue."""
162-    def run(*args: str) -> subprocess.CompletedProcess[str] | None:
163-        try:
164-            return subprocess.run(
165-                ["git", "-C", str(depot), *args],
166-                capture_output=True,
167-     
… [1523 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '160,190p' tools/corpus_commun.py", "description": "Read function tail"}`

  ```
def fichier_suivi_modifie(depot: Path, relatif: str) -> bool | None:
    """True si le fichier suivi a une différence (index ou travail). None si git échoue."""
    def run(*args: str) -> subprocess.CompletedProcess[str] | None:
        try:
            return subprocess.run(
                ["git", "-C", str(depot), *args],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return None

    travail = run("diff", "--quiet", "--", relatif)
    index = run("diff", "--cached", "--quiet", "--", relatif)
    if travail is None or index is None:
        return None
    if travail.returncode not in (0, 1) or index.returncode not in (0, 1):
        return None
    return travail.returncode == 1 or index.returncode == 1


# ---------------------------------------------------------------------------
# Normalisation et segmentation
# ---------------------------------------------------------------------------

def normaliser_texte(texte: str) -> str:
    """NFC, LF, espaces collapsés, frontière éthiopienne U+1362 U+1361.

    On ne change ni la ca
… [50 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py", "old_string": "def git_info(depot: Path) -> dict[str, Any]:\n    \"\"\"HEAD et date, en lecture seule. Ne lève jamais.\"\"\"\n    def run(*args: str) -> subprocess.CompletedProcess[str] | None:\n        try:\n    … [3860 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py", "old_string": "                \"fichier_modifie_avant\": fichier_suivi_modifie(\n                    PANINI_RESEARCH, \"data/udhr_corpus.json\"\n                ),\n                \"lecture_seule\": True,", "ne … [356 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "> **Dispositif** : lecture seule de `../Panini/research/data/udhr_corpus.json` (HEAD `e10d695`,\n> 2026-10-25, SHA-256 `531bc75c…`) ; `data/udhr/articles_propres.jsonl`, `langues.jsonl`,\ … [451 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "| Panini/NIPADA | `../Panini/research/data/udhr_corpus.json` | JSON `udhr-v2.0-xml` | **532** | `e10d695` | 2026-10-25 | `531bc75c…` |", "new_string": "| Panini/NIPADA | `../Panini/resear … [121 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

### 👤 Utilisateur

background job bash-16 (bash: grep -rIl "aristotle\|bengio\|book_of_enoch\|brahmajala" data/ 2>/dev/null | head -20; echo ---; find data -maxdepth 2 -iname "*gutenberg*" -o -iname "*sacred*" -o -iname "*corpus*" | head -40) finished [status: completed, exit code: 0]. Read its output with job_output.

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "La source déclarée est la même des deux côtés (`eric-muller/udhr`). Elle **n'est pourtant pas\nbyte-identique** : après NFC et compression des espaces, **20 langues** gardent un écart de  … [941 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/corpus_commun.py --tout && python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\nprint(json.dumps(r['sources']['panini'], ensure_ascii=False, indent=1))\nEOF", "description": "Rebuild and check Panini source status"}`

  ```
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
{
 "article": "Article 1",
 "date": "2026-10-25",
 "depot": "Panini/research",
 "fichier": "../Panini/research/data/udhr_corpus.json",
 "fichier_modifie_avant": null,
 "fichier_suivi_par_git": false,
 "format": "udhr-v2.0-xml",
 "head": "e10d695e65f52031222819cb1bdbb290d08f8e57",
 "lecture_seule": true,
 "sha256": "531bc75c4d926cabc477165a6c7cd1ea70869ee0aa82d203053f30676d9cf190",
 "source_declaree": "eric-muller/udhr (GitHub) — Unicode UDHR XML Project",
 "total_languages": 532
}
  ```

- **bash** `{"command": "sed -n '1,200p' tools/verifie_en_cours.py", "description": "Read en-cours validator"}`

  ```
#!/usr/bin/env python3
"""verifie_en_cours.py — l'état doit rester court, structuré, reprenable et multi-session.

Le fichier `docs/pilotage/en-cours.md` est la seule source de l'état. Ce contrôle vérifie :
  1. un budget de **2 000 mots** ;
  2. les **sept sections** du template ;
  3. « Sessions en cours » : une sous-section `### Session ...` par session active, avec
     **Id**, **Rôle**, **Plan**, **Ambition**, **Stratégie**, **Objectif final**,
     **Ce qu'elle fait**, **Ce que font les autres**, **Prochaine action**, **Bloquants** et
     **Journal** ;
  4. **10 puces au plus** dans « Ce qui est en cours », sans doublon et sans puce de plus de 80 mots ;
  5. « Les chantiers et leurs bloquants » : une ligne **A**, **B**, **N**, **R** avec un bloquant
     **non vide** (le mot « aucun » est une information, une cellule vide est un oubli) ;
  6. **5 questions ouvertes au plus**, chacune avec ce qui la débloque (`→`) ;
  7. une **prochaine action nommée** dans « Ce qui reste » (A/B/C/N/R) ;
  8. aucune ligne de journal A7.x dans l'état (les mesures vont dans `reports/`).

Usage : python3 tools/verifie_en_cours.py   (code 0 = l'état est reprenable)
"""
from __future__ import anno
… [4812 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"Panini\\|J2\" docs/pilotage/roadmap.md | tail -20", "description": "Find roadmap Panini lines"}`

  ```
(no output)
  ```

- **bash** `{"command": "grep -n \"R0\\.7\" docs/pilotage/roadmap.md | head -20; echo ---; grep -n \"R0\\.7\" docs/pilotage/en-cours.md docs/pilotage/chantiers.md | head -20", "description": "Find R0.7 roadmap lines"}`

  ```
33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; la suite : **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; R2/R3 attendent N5/N4 |
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **
… [1763 caractères tronqués]
  ```

- **bash** `{"command": "printf 'reports md: '; ls reports/*.md 2>/dev/null | wc -l; printf 'reports json: '; ls reports/*.json 2>/dev/null | wc -l; printf 'docs md (hors archive/README): '; find docs -name '*.md' ! -path 'docs/archive/*' ! -name README.md | wc -l; printf 'portes: '; ls tools/porte-*.sh 2>/dev/ … [57 caractères tronqués]`

  ```
reports md: 711
reports json: 804
docs md (hors archive/README): 458
portes: 84
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run doc review"}`

  ```
revue de documentation · 711 fiche(s) · 804 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 710 fichiers, le disque en a 711
     · compteurs : en-cours.md dit 803 JSON, le disque en a 804
exit=1
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\nt=open('docs/pilotage/en-cours.md').read()\nm=re.search(r'## Ce qui est en cours\\n(.*?)\\n## ', t, re.S)\nbullets=[l for l in m.group(1).splitlines() if l.startswith('- ')]\nprint(len(bullets))\nfor b in bullets: print(len(re.findall(r'\\S+',b)), b[:80])\n … [46 caractères tronqués]`

  ```
6
21 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8
44 - **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 0
36 - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventai
67 - **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 
20 - **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ;
12 - **Panini J2.1** : table **14 atomes × 8 niveaux** ; [fiche](../../reports/rapp
  ```

- **bash** `{"command": "sed -n '245,258p' docs/pilotage/roadmap.md", "description": "Read R0.7 roadmap row context"}`

  ```
établir la cible avant de la porter dans le natif.

| # | fonctionnalité | état | porte |
|---|---|---|---|
| **R0.1** | **graphe de document** : régions typées (titre, section, paragraphe, [tableau](../theorie/glossaire/entrees/tableau.md), code, maths, figure), offsets, provenance ; parseurs PDF/HTML/DOCX/Markdown ; sans modèle | ✅ **51 pages**, fidélité **1,000** | 50 pages découpées, provenance exacte, rejeu identique |
| **R0.2** | **[contrôleur de lecture](../theorie/glossaire/entrees/controleur-de-lecture.md)** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, titres, premières/dernières phrases, BM25/regex) | ✅ **1,000** à 30 % sur **5 types** | à 30 % du budget, **≥ 90 %** de la réponse de la lecture intégrale sur **3 types** |
| **R0.3** | **[banc de lecture rapide](../theorie/glossaire/entrees/banc-de-lecture-rapide.md)** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles [closed-book](../theorie/glossaire/entrees/closed-book.md), régions aléatoires, sections mélangées | ✅ **249 questions** : extractif **1,000** à 30 % ; modèle **0,231** contre début **0,042**. **Durci*
… [2249 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**", "new_string": "**Mis à jour : 2026-11-07, 15 h 05 HNE (heure locale, EST).**"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Panini J2.1** : table **14 atomes × 8 niveaux** ; [fiche](../../reports/rapport-atomes-niveaux.md).", "new_string": "- **Panini J2.1** : table **14 atomes × 8 niveaux** ; [fiche](../../repor … [257 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **710** / **803** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **711** / **804** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 10}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 85, "limit": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).

(Showing lines 1-10 of 140. Use offset=11 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
85: ## Ce qui est en cours
86: 
87: - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
88: - **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
89: - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
90: - **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; la fusion garde l'heuristique ; **`r035` réglé** (237/238, 0,9958) ; **convention des GV réglée** (F1 **0,7902**, sujet hors du GV + adverbe final, 0 perte d'attachement) ; **schéma v2** publié (26 cas, 0 échec ; `meta.partition`/`meta.alternative`, v1 lue) ; **restitution v0** : **46/46
… [3284 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**", "new_string": "**Mis à jour : 2026-11-07, 15 h 05 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Panini J2.1** : table **14 atomes × 8 niveaux** ; [fiche](../../reports/rapport-atomes-niveaux.md).", "new_string": "- **Panini J2.1** : table **14 atomes × 8 niveaux** ; [fiche](../../repor … [257 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **710** / **803** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **711** / **804** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Panini J2.2** : corpus commun UDHR **21 textes / 42 phrases / 5 familles / 10 écritures** ; **418/438 paires exactes (95,4 %)**, **20 écarts exclus**, **8/8 contrôles** ; [fiche](../../repor … [320 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 33, "limit": 4}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 253, "limit": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
33: | **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; la suite : **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; R2/R3 attendent N5/N4 |
34: | **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête le verbe) ; [fiche](../../reports/rapport-s-fait-divers.md). **v6** : h050, h053 et « si fort que » **fermés**, gold **60** (vague 5) ; **60/60** types, **142/142** rôles, **50/50** complém
… [1917 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
253: | **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 langues** à **0,9687** ; **gold 360** : POS **0,765**, syntagmes exacts **0,190**/**tête 0,510**, **attachement tête 1,0/0,966/0,932** (59 ambiguës), pragmatique **1,0/1,0/0,994/0,889** ; le neuronal réel est **qualifié** (tagger 7B, POS **0,9440** ; **syntagmes 0,7606** ; **cascade complète 0,9415/0,7539/1,0**) | — (livré ; B13 neuronal : POS, syntagmes, cascade complète) |

(Showing lines 253-253 of 382. Use offset=254 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script … [1369 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lan … [1112 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "ls -la journal/ | tail -30; echo ---; find journal -maxdepth 2 -type f -name \"*.md\" | tail -20", "description": "Inspect journal structure"}`

  ```
drwxr-xr-x. 1 stephane stephane   150 28 oct 14:12 2026-10-12
drwxr-xr-x. 1 stephane stephane   192 28 oct 14:06 2026-10-13
drwxr-xr-x. 1 stephane stephane   206 28 oct 14:06 2026-10-14
drwxr-xr-x. 1 stephane stephane   224 28 oct 14:06 2026-10-15
drwxr-xr-x. 1 stephane stephane   224 28 oct 14:06 2026-10-16
drwxr-xr-x. 1 stephane stephane   192 28 oct 14:11 2026-10-17
drwxr-xr-x. 1 stephane stephane   108 28 oct 14:06 2026-10-18
drwxr-xr-x. 1 stephane stephane   114 28 oct 14:11 2026-10-19
drwxr-xr-x. 1 stephane stephane   104 28 oct 14:11 2026-10-20
drwxr-xr-x. 1 stephane stephane   168 28 oct 14:11 2026-10-21
drwxr-xr-x. 1 stephane stephane   136 28 oct 14:06 2026-10-22
drwxr-xr-x. 1 stephane stephane    42 28 oct 14:11 2026-10-23
drwxr-xr-x. 1 stephane stephane   206 28 oct 14:06 2026-10-24
drwxr-xr-x. 1 stephane stephane   150 28 oct 14:11 2026-10-25
drwxr-xr-x. 1 stephane stephane   228 28 oct 14:06 2026-10-26
drwxr-xr-x. 1 stephane stephane   290 28 oct 14:11 2026-10-27
drwxr-xr-x. 1 stephane stephane   216 28 oct 14:06 2026-10-28
drwxr-xr-x. 1 stephane stephane   208 29 oct 17:08 2026-10-29
drwxr-xr-x. 1 stephane stephane   150 31 oct 11:22 2026-10-30
drwxr-xr-x. 1 stephane
… [1249 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/sessions/ | tail -20; echo ---; sed -n '1,80p' tools/verifie_journal.py", "description": "Inspect journal sessions and validator"}`

  ```
drwxr-xr-x. 1 stephane stephane    80  5 nov 10:18 fbdbd6fb-1ebc-4348-a6cc-f10faf76520b
drwxr-xr-x. 1 stephane stephane    80 31 oct 11:19 fc167f70-be8b-4c63-be5e-3c0d3c0ba1c3
drwxr-xr-x. 1 stephane stephane    80 31 oct 11:19 fd4b8df1-abc9-4dd6-94df-fcf484cc9017
drwxr-xr-x. 1 stephane stephane   114  2 nov 18:36 fe3c05f0-834b-44f2-8739-501865d652c1
drwxr-xr-x. 1 stephane stephane    74 28 oct 09:17 ff364db0-d28f-47eb-973e-f13bdafd35a2
drwxr-xr-x. 1 stephane stephane    80  5 nov 13:13 ff7e786c-3ece-4eae-864e-19dddfead93c
drwxr-xr-x. 1 stephane stephane    80  5 nov 21:14 fff7ca81-5684-4c2e-b7c5-a8f3c012cc49
-rw-r--r--. 1 stephane stephane 12965  7 nov 14:56 MANIFEST.md
drwxr-xr-x. 1 stephane stephane    14 30 oct 11:04 _modele
drwxr-xr-x. 1 stephane stephane    34 31 oct 11:21 N2-GPU
-rw-r--r--. 1 stephane stephane  1471 31 oct 11:23 README.md
drwxr-xr-x. 1 stephane stephane    80  7 nov 14:18 session-614644be-9315-4734-9b97-236a792f4dc5
drwxr-xr-x. 1 stephane stephane    80  7 nov 10:51 session-6af74924-89c1-4b96-aa02-b70bd77ab178
drwxr-xr-x. 1 stephane stephane    80  7 nov 10:51 session-78f03aed-fb9d-4009-8625-e1186078059c
drwxr-xr-x. 1 stephane stephane    80  7 nov 14:57 sess
… [3798 caractères tronqués]
  ```

- **bash** `{"command": "env | grep -E '^DSH_|SESSION|JOURNAUX' | sort | sed -n '1,80p'", "description": "Inspect DSH env vars"}`

  ```
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
DESKTOP_SESSION=plasma6
DSH_HOME=/home/stephane/.dsh
DSH_PROFILE_DIR=/home/stephane/.dsh/profiles/headless
DSH_PROFILE=headless
DSH_SESSION_ID=session-932afd57-1363-4133-b6f1-64f7d937f38d
DSH_SHELL=1
KDE_FULL_SESSION=true
KDE_SESSION_UID=1000
KDE_SESSION_VERSION=6
KONSOLE_DBUS_SESSION=/Sessions/5
SESSION_MANAGER=local/Hauru:@/tmp/.ICE-unix/64061,unix/Hauru:/tmp/.ICE-unix/64061
SHELL_SESSION_ID=9ccf95734de74d019d86e8774384d6fe
XDG_SESSION_CLASS=user
XDG_SESSION_DESKTOP=KDE
XDG_SESSION_ID=4
XDG_SESSION_PATH=/org/freedesktop/DisplayManager/Session1
XDG_SESSION_TYPE=x11
XSESSION_IS_UP=yes
  ```

- **bash** `{"command": "ls -la journal/sessions/session-932afd57-1363-4133-b6f1-64f7d937f38d 2>/dev/null; echo ---; sed -n '1,120p' journal/2026-11-07/README.md", "description": "Check current session journal and day README"}`

  ```
---
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
| `7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0` | Tu travailles dans /home/stephane/Data13 | 2026-11-07 02:09 | 0.1 h | [rapport](../sessions/7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0
… [5901 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/README.md", "offset": 55, "limit": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/README.md</path>
<type>file</type>
<content>
55: | 10:58 | `f93ddc60` | DOCS — README T1 : DEUX LIGNES RACCOURCIES, BUDGET TENU |
56: | 11:09 | `fffbbe5d` | PANINI — L'INVENTAIRE INTÉGRÉ AU PLAN : 14 DÉPÔTS, 7 AXES, 14 ATOMES, 9 CORPUS, TROIS INTÉGRATIONS MÛRES (UDHR+GÉNÉALOGIE, ATOMES↔NIVEAUX, CORPUS CIC) AVEC LEURS CONTRÔLES NÉGATIFS |
57: | 11:12 | `34fdd4ef` | DOCS — README T1 TENU (DEUX LIGNES LONGUES RACCOURCIES) |
58: | 11:16 | `d7469b5c` | INDEX — RÉGÉNÉRÉ APRÈS L'INVENTAIRE PANINI (702 FICHES) ; ÉTAT HORODATÉ |
59: | 12:40 | `25a6c0ff` | B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183 |
60: | 13:44 | `92652984` | B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183 |
61: | 14:23 | `9a259953` | B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE |
62: | 14:45 | `8eb0cc49` | B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE |
63: 
64: ## Le récit de la journée (écrit à la main)
65: 
66: <!-- notes -->
67: **La nuit du 
… [736 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/README.md", "offset": 74, "limit": 15}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/README.md</path>
<type>file</type>
<content>
74: **L'après-midi du 07/11 (J1.3 → J1.4).** Le **schéma v2** publie `meta.partition` et
75: `meta.alternative` (26 cas, 0 échec ; v1 toujours lue). La **restitution v0** ajoute
76: `python3 tools/drave.py restituer TEXTE` : la surface est reconstruite depuis le niveau
77: `graphème`, **sans lire `Annotation.texte`**, puis comparée à la source. Sur les **50 textes
78: libres**, **46 annotations** (4 refus) et **46/46 surfaces exactes** ; le **miroir strict**
79: (minimum surface/mots/POS) vaut **0,1087** — la ponctuation séparée des mots fait tomber mots et
80: POS, alors que la fidélité de caractères reste à 0,9506. Le miroir a trouvé un vrai trou : `f50`
81: perdait ses **10 sauts de ligne** (45/46, 0,9783) ; le correctif `C` les annote et la surface
82: revient à 46/46. Le contrôle négatif (mélange, troncature) casse **46/46**. C'est un **codec de
83: surface**, pas un décodeur : la fidélité sémantique reste à mesurer.
84: [Fiche](../../reports/rapport-restitution-v0.md).
85: <!-- /notes -->

(End of file - total 85 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/README.md", "old_string": "[Fiche](../../reports/rapport-restitution-v0.md).\n<!-- /notes -->", "new_string": "[Fiche](../../reports/rapport-restitution-v0.md).\n\n**L'après-midi du 07/11 (J2.2).** Le **corpus commun P … [802 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py; echo \"en-cours=$?\"; python3 tools/verifie_journal.py; echo \"journal=$?\"", "description": "Validate state and journal"}`

  ```
en-cours · 1664 mots · 7 sections · 4 session(s) · 7 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
en-cours=0
  journal · 44 jour(s) · 170 session(s) · 2361 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
journal=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -30; echo \"revue=${PIPESTATUS[0]}\"", "description": "Run doc review"}`

  ```
revue de documentation · 711 fiche(s) · 804 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -40; echo \"taille=${PIPESTATUS[0]}\"", "description": "Check document budgets"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    7161    383   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2783    190   T1   2800  reports/README.md
    2434    162   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [528 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -30; echo \"tableaux=${PIPESTATUS[0]}\"", "description": "Run table gate"}`

  ```
✅ 1767 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3816 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
tableaux=0
  ```

- **bash** `{"command": "sed -n '1,220p' tools/taille_documents.py", "description": "Read document budget tool"}`

  ```
#!/usr/bin/env python3
"""taille_documents.py — le budget de contexte et la cohésion des documents.

Ce que l'outil vérifie :
  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
  2. la cohésion minimale : un titre, un résumé en tête, et pour les documents datés un
     « Résumé » + « ne pas charger par défaut » ;
  3. les fiches de résultats trop longues pour être lues d'un bloc (avertissement, pas échec) ;
  4. le classement des plus gros documents, pour voir où le contexte part.

Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
ils ne sont pas chargés automatiquement. Le budget est en **mots** ; l'estimation de tokens
est donnée à titre indicatif (≈ caractères / 4).

Les **sources de diagrammes** (` ```plantuml `, ` ```mermaid `) sont **rendues, pas lues** :
elles ne comptent pas dans le budget ; le document les porte, la page montre le SVG.
"""
from __future__ import annotations
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent

# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
BUDGETS: list[tuple[str, str, int
… [6542 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\nlines=open('docs/pilotage/en-cours.md').read().splitlines()\nfor l in lines:\n    if l.startswith('- **Panini'):\n        print(len(re.findall(r'\\S+',l)), l)\nEOF", "description": "Count Panini bullet words"}`

  ```
12 - **Panini J2.1** : table **14 atomes × 8 niveaux** ; [fiche](../../reports/rapport-atomes-niveaux.md).
38 - **Panini J2.2** : corpus commun UDHR **21 textes / 42 phrases / 5 familles / 10 écritures** ; **418/438 paires exactes (95,4 %)**, **20 écarts exclus**, **8/8 contrôles** ; [fiche](../../reports/rapport-corpus-commun.md) ; suite **J3.1** (retrieval à époque contrôlée).
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\ncands=[\n\"- **Panini J2.1/J2.2** : table **14 atomes × 8 niveaux** ; corpus UDHR **21 textes**, **418/438 paires exactes (95,4 %)** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).\",\n\"- **Panini J2.1 … [346 caractères tronqués]`

  ```
23 - **Panini J2.1/J2.2** : table **14 atomes × 8 niveaux** ; corpus UDHR **21 textes**, **418/438 paires exactes (95,4 %)** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).
25 - **Panini J2.1/J2.2** : table **14 atomes × 8 niveaux** ; corpus UDHR **21 textes**, **418/438 paires exactes (95,4 %)**, **8/8 contrôles** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\ncands=[\n\"- **Panini J2.1/J2.2** : table **14 atomes × 8 niveaux** ; corpus UDHR **418/438 paires exactes (95,4 %)** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).\",\n\"- **Panini J2.1/J2.2** : table … [525 caractères tronqués]`

  ```
21 - **Panini J2.1/J2.2** : table **14 atomes × 8 niveaux** ; corpus UDHR **418/438 paires exactes (95,4 %)** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).
23 - **Panini J2.1/J2.2** : table **14 atomes × 8 niveaux** ; corpus UDHR **21 textes**, **418/438 paires exactes (95,4 %)** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).
20 - **Panini J2.1/J2.2** : table **14 atomes × 8 niveaux** ; corpus UDHR **21 textes**, **418/438 exactes** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\nc=\"- **Panini J2.1/J2.2** : table **14 atomes** ; corpus UDHR **418/438 exactes** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).\"\nprint(len(re.findall(r'\\S+',c)))\nc2=\"- **Panini J2.1/J2.2** : tab … [253 caractères tronqués]`

  ```
15
16
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\nfor c in [\n\"- **Panini J2.1/J2.2** : table **14 atomes × 8 niveaux** ; corpus UDHR **418/438 exactes** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).\",\n\"- **Panini J2.1/J2.2** : table **14 atomes* … [241 caractères tronqués]`

  ```
18 - **Panini J2.1/J2.2** : table **14 atomes × 8 niveaux** ; corpus UDHR **418/438 exactes** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).
17 - **Panini J2.1/J2.2** : table **14 atomes** ; corpus UDHR **21 textes**, **418/438 exactes** ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md).
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Panini J2.1** : table **14 atomes × 8 niveaux** ; [fiche](../../reports/rapport-atomes-niveaux.md).\n- **Panini J2.2** : corpus commun UDHR **21 textes / 42 phrases / 5 familles / 10 écritur … [383 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -12; echo \"taille=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py", "description": "Recheck budgets and state"}`

  ```
2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3999 mots (budget 4 000)

  avertissements :
     · 40 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
taille=0
  en-cours · 1629 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 tools/index_reports.py 2>&1 | tail -20; echo \"index=${PIPESTATUS[0]}\"; git status --short -- reports/INDEX.md | cat", "description": "Regenerate reports index"}`

  ```
708 fiches → reports/INDEX.md
index=0
 M reports/INDEX.md
  ```

- **bash** `{"command": "git diff --stat -- reports/INDEX.md; git diff -- reports/INDEX.md | head -40", "description": "Inspect index diff"}`

  ```
reports/INDEX.md | 4 +++-
 1 file changed, 3 insertions(+), 1 deletion(-)
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 6b7b52bd..7c161df1 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **706 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **708 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -56,6 +56,7 @@
 | [rapport-analyse-flux.md](rapport-analyse-flux.md) | Analyse du flux, couche par couche |
 | [rapport-annotation-independante.md](rapport-annotation-independante.md) | Contrôle indépendant de la convention d'attachement — 20 segments annotés à la main |
 | [rapport-architecture-memoire.md](rapport-architecture-memoire.md) | Rapport — architecture mémoire : ce qui va en VRAM, en RAM, et sur le disque |
+| [rapport-atomes-niveaux.md](rapport-atomes-niveaux.md) | Table de correspondance — 14 atomes de Panini et 8 niveaux de Drave |
 | [rapport-attention-creuse.md](rapport-attention-creuse.md) | Attention creuse — le trou se 
… [1213 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/corpus_commun.py --verifier && python3 tools/corpus_commun.py --controle-negatif >/tmp/controle.json && python3 - <<'EOF'\nimport json\nc=json.load(open('/tmp/controle.json'))\nprint(c['verdict'], c['n_ok'], '/', c['n_tests'])\nEOF", "description": "Re-verify corpus and co … [7 caractères tronqués]`

  ```
VERIFIER: PASS
PASS 8 / 8
  ```

- **bash** `{"command": "git diff --stat -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-07/README.md reports/INDEX.md; echo ---; git status --short -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-07/README.md reports/INDEX.md", "description": "Check modified state fi … [5 caractères tronqués]`

  ```
docs/pilotage/en-cours.md    |  6 +++---
 docs/pilotage/roadmap.md     |  4 ++--
 journal/2026-11-07/README.md | 10 ++++++++++
 reports/INDEX.md             |  4 +++-
 4 files changed, 18 insertions(+), 6 deletions(-)
---
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-07/README.md
 M reports/INDEX.md
  ```

- **bash** `{"command": "sed -n '1,160p' tools/toutes-les-portes.sh", "description": "Inspect gate runner"}`

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
… [3112 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/toutes-les-portes.sh", "description": "Run full gates suite", "run_in_background": true}`

  ```
started background job bash-120
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py", "old_string": "                \"5 familles les plus représentées parmi les paires exactes\",\n                \"4 langues par famille, écritures distinctes quand c'est possible\",", "new_string": "               … [244 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_commun.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "Le pool exact de **418** paires couvre **51 étiquettes de famille** (dont **10 `(inconnue)`**).\nLes cinq familles retenues sont les cinq plus représentées :\n\n| famille | paires exactes … [2125 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/corpus_commun.py --tout", "description": "Rebuild after criteria fix"}`

  ```
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\nprint(json.dumps(r['selection'], ensure_ascii=False, indent=1))\nEOF", "description": "Check selection criteria JSON"}`

  ```
{
 "criteres": [
  "présent des deux côtés (même fichier udhr_<clé>.xml)",
  "article 1 identique après NFC et espaces collapsés",
  "5 familles parmi les six plus représentées, choisies pour la diversité des écritures (Turkic, 17 paires, écarté : ses écritures sont déjà couvertes)",
  "4 langues par famille, écritures distinctes quand c'est possible",
  "français ajouté hors strate comme pivot de Drave"
 ],
 "familles_attendues": [
  "Afro-Asiatic",
  "Atlantic-Congo",
  "Austronesian",
  "Indo-European",
  "Sino-Tibetan"
 ],
 "n_pivots": 1,
 "n_strates": 20,
 "pivot": "fra",
 "principe": "20 langues stratifiées (5 familles glottolog × 4) + le français, pivot de Drave ; toutes les paires sont exactes après normalisation."
}
  ```

- **bash** `{"command": "grep -n \"Turkic\\|46 autres\\|45 autres\\|cinq plus\\|six plus\" reports/rapport-corpus-commun.md", "description": "Check report family wording"}`

  ```
106:Les cinq familles retenues sont **parmi les six plus représentées** ; le **turcique** (17 paires)
116:| Turkic | 17 | 4,1 % | 0 (écarté : écritures déjà couvertes) |
118:| 45 autres étiquettes | 134 | 32,1 % | 0 |
122:4,1 %) et les **45 autres** étiquettes (**134**, 32,1 %, dont les 10 `(inconnue)`) ne sont pas
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,re\nr=json.load(open('reports/corpus-commun.json'))\nl=r['intersection']['listes']['sans_fichier_drave']\nnum=[x for x in l if re.search(r'udhr_\\d+\\.xml$',x)]\ncode=[x for x in l if x not in num]\nprint(len(l), len(num), len(code))\nprint(num[-1], code[: … [51 caractères tronqués]`

  ```
79 40 39
udhr_072.xml ['udhr_aar.xml', 'udhr_ayo.xml', 'udhr_bvi.xml', 'udhr_cas.xml', 'udhr_chv.xml']
  ```

- **bash** `{"command": "grep -n \"96,1\\|96.1\" reports/rapport-corpus-commun.md", "description": "Locate incorrect rate"}`

  ```
75:| appariables article 1 | **438** | 96,1 % de l'intersection | 15 communs sans article 1, 2 Drave hors Panini |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "| appariables article 1 | **438** | 96,1 % de l'intersection | 15 communs sans article 1, 2 Drave hors Panini |", "new_string": "| appariables article 1 | **438** | 96,7 % de l'intersecti … [55 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"%\" reports/rapport-corpus-commun.md | sed -n '1,80p'", "description": "Review all percentages"}`

  ```
7:> appariables (**95,4 %**). **20 écarts de surface** sont **exclus, pas corrigés**. Les **8 contrôles
73:| fichiers communs | **453** | **99,3 %** de Drave ; **85,2 %** de Panini | l'intersection des identifiants de fichier |
74:| article 1 côté Drave | 440 | 96,5 % de Drave | 16 fichiers Drave n'ont pas d'article 1 |
75:| appariables article 1 | **438** | 96,7 % de l'intersection | 15 communs sans article 1, 2 Drave hors Panini |
76:| **paires exactes** | **418** | **95,4 %** des appariables ; **78,6 %** de Panini | le corpus disponible |
77:| écarts de surface | 20 | 4,6 % des appariables | exclus, pas corrigés |
112:| Indo-European | 120 | 28,7 % | 5 |
113:| Atlantic-Congo | 81 | 19,4 % | 4 |
114:| Austronesian | 37 | 8,9 % | 4 |
115:| Sino-Tibetan | 17 | 4,1 % | 4 |
116:| Turkic | 17 | 4,1 % | 0 (écarté : écritures déjà couvertes) |
117:| Afro-Asiatic | 12 | 2,9 % | 4 |
118:| 45 autres étiquettes | 134 | 32,1 % | 0 |
119:| **total** | **418** | **100 %** | **21** |
121:Les cinq familles retenues couvrent **267/418 = 63,9 %** du pool exact ; le turcique (**17**,
122:4,1 %) et les **45 autres** étiquettes (**134**, 32,1 %, dont les 10 `(inconnue)`) ne sont pas
124:**sur-représe
… [171 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "représentés. Ce n'est donc **pas** un échantillon proportionnel : les petites familles sont\n**sur-représentées** dans l'échantillon (19,0 % chacune contre 2,9 à 8,9 % du pool) et\nl'indo … [598 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "> **Aucune écriture dans Panini** : le script vérifie l'empreinte de la source avant et après ;\n> les seuls fichiers versionnés produits sont cette fiche, son JSON et l'outil.", "new_str … [253 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **bash** `{"command": "wc -l -w reports/rapport-corpus-commun.md; python3 tools/taille_documents.py 2>&1 | grep -n \"corpus-commun\\|T0 max\"", "description": "Check report length and budget"}`

  ```
322  3315 reports/rapport-corpus-commun.md
21:  T0 max : 3999 mots (budget 4 000)
  ```

- **bash** `{"command": "job_list", "description": "List background jobs"}`

  ```
[stderr]
bash: line 1: job_list: command not found
[exit code: 127]
  ```

- **job_list** `{}`

  ```
bash-16 [bash] completed — grep -rIl "aristotle\|bengio\|book_of_enoch\|brahmajala" data/ 2>/dev/null | head -20; echo ---; find data -maxdepth 2 -iname "*gutenberg*" -o -iname "*sacred*" -o -iname "*corpus*" | head -40
bash-120 [bash] running — bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport ast\nsrc=open('tools/corpus_commun.py').read()\ntree=ast.parse(src)\nprint('functions', len([n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]))\nprint('lines', src.count('\\n')+1)\nEOF\nruff check tools/corpus_commun.py 2>/dev/null  … [45 caractères tronqués]`

  ```
functions 28
lines 1093
  ```

- **bash** `{"command": "grep -n \"def \\|SELECTION\\|FAMILLES_ATTENDUES\" tools/corpus_commun.py | sed -n '1,80p'", "description": "List tool functions"}`

  ```
55:SELECTION: list[tuple[str, str]] = [
85:FAMILLES_ATTENDUES = {
105:def sha256_bytes(donnees: bytes) -> str:
109:def sha256_texte(texte: str) -> str:
113:def sha256_fichier(chemin: Path) -> str:
121:def lire_jsonl(chemin: Path) -> list[dict[str, Any]]:
135:def git_run(depot: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
149:def git_info(depot: Path) -> dict[str, Any]:
162:def fichier_suivi_par_git(depot: Path, relatif: str) -> bool | None:
174:def fichier_suivi_modifie(depot: Path, relatif: str) -> bool | None:
195:def normaliser_texte(texte: str) -> str:
209:def decouper_phrases(texte: str) -> list[str]:
229:def texte_fichier(phrases: list[str]) -> str:
233:def sans_espaces(texte: str) -> str:
237:def valider_phrases(
259:def egalite_normee(a: str, b: str) -> bool:
267:def lire_sources() -> dict[str, Any]:
291:def statistiques_intersection(sources: dict[str, Any]) -> dict[str, Any]:
346:def construire_records(sources: dict[str, Any]) -> list[dict[str, Any]]:
354:    for cle, role in SELECTION:
416:    if len(records) != len(SELECTION):
421:def statistiques_echantillon(records: list[dict[str, Any]]) -> dict[str, Any]:
442:def construire_corpus_jsonl(records: list[
… [991 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '927,1042p' tools/corpus_commun.py", "description": "Read verifier function"}`

  ```
def verifier(sortie: Path) -> list[str]:
    erreurs: list[str] = []
    index_path = sortie / "index.json"
    if not index_path.is_file():
        return [f"index absent : {index_path}"]
    index = json.loads(index_path.read_text(encoding="utf-8"))
    records = index.get("textes", [])
    if not records:
        return ["index sans textes"]

    # 1. Reconstruire dans un dossier temporaire et comparer octet par octet.
    with tempfile.TemporaryDirectory(dir=sortie.parent, prefix=".verif-corpus-") as tmp:
        tmp_path = Path(tmp)
        construire(tmp_path, ecrire_rapport=False)
        erreurs.extend(comparer_arbres(sortie, tmp_path))
        if (sortie / "index.json").read_text(encoding="utf-8") != (
            tmp_path / "index.json"
        ).read_text(encoding="utf-8"):
            erreurs.append("index.json diffère de la reconstruction")

    # 2. Contrôles sémantiques sur les fichiers écrits.
    corpus_jsonl = sortie / "corpus.jsonl"
    if not corpus_jsonl.is_file():
        return erreurs + ["corpus.jsonl absent"]
    lignes = lire_jsonl(corpus_jsonl)
    par_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ligne in lignes:
        par_id[ligne["i
… [3788 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\nold='''    par_id: dict[str, list[dict[str, Any]]] = defaultdict(list)\n    for ligne in lignes:\n        par_id[ligne[\"id\"]].append(ligne)\n\n    for r in records:\n'''\nnew='''    par_id: … [2100 caractères tronqués]`

  ```
ok
compile-ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "git diff -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-07/README.md reports/INDEX.md | sed -n '1,220p'", "description": "Review state diffs"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index d923018f..92494392 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-07, 15 h 05 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -89,7 +89,7 @@
 - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
 - **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; la fusion garde l'heuristique ; **`r035` réglé** (237/238, 0,9958) ; **convention des GV réglée** (F1 **0,7902**, sujet hors du GV + adverbe final, 0 perte d'attachement) ; **schéma v2** publié (26 cas, 0 échec ; `meta.partition`/`meta.alternative`, v1 lue) ; **restitution v0** : **46/46 surfaces**, miroir **0,1087** ; [fiche](../../reports/rapport-restit
… [14088 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-120", "wait": false}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-1107-15h11
  porte-adaptateur-sortie ✅                          73 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
[status: running]
  ```

- **bash** `{"command": "chmod +x tools/corpus_commun.py; ls -l tools/corpus_commun.py; head -1 tools/corpus_commun.py", "description": "Make tool executable"}`

  ```
-rwx--x--x. 1 stephane stephane 43268  7 nov 15:12 tools/corpus_commun.py
#!/usr/bin/env python3
  ```

- **bash** `{"command": "chmod 755 tools/corpus_commun.py; ls -l tools/corpus_commun.py", "description": "Set tool permissions"}`

  ```
-rwxr-xr-x. 1 stephane stephane 43268  7 nov 15:12 tools/corpus_commun.py
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -12; echo \"revue=${PIPESTATUS[0]}\"; bash tools/porte-tableaux.sh 2>&1 | tail -5; echo \"tableaux=${PIPESTATUS[0]}\"", "description": "Re-run doc review and table gate"}`

  ```
revue de documentation · 711 fiche(s) · 804 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  ✅ 1767 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3818 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
tableaux=0
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py; python3 tools/verifie_en_cours.py; python3 tools/taille_documents.py 2>&1 | tail -4", "description": "Re-run state/journal/budget checks"}`

  ```
journal · 44 jour(s) · 170 session(s) · 2361 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  en-cours · 1629 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  avertissements :
     · 40 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -10; echo \"schemas=${PIPESTATUS[0]}\"", "description": "Verify schemas"}`

  ```
schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
schemas=0
  ```

- **bash** `{"command": "grep -n \"8/8\\|contrôle négatif\\|contrôles négatifs\\|rejets attendus\" reports/rapport-corpus-commun.md journal/2026-11-07/README.md work/corpus-commun/README.md tools/corpus_commun.py | sed -n '1,80p'", "description": "Locate control wording"}`

  ```
reports/rapport-corpus-commun.md:8:> négatifs** sont des **rejets attendus** (8/8).
reports/rapport-corpus-commun.md:229:| contrôle négatif | 8/8 rejets attendus | **8/8** |
reports/rapport-corpus-commun.md:231:### 5.1 Le contrôle négatif, test par test
reports/rapport-corpus-commun.md:244:Le contrôle négatif n'est donc pas un simple « relancer le script » : il **altère** le texte, **croise**
reports/rapport-corpus-commun.md:314:  contrôle négatif ;
journal/2026-11-07/README.md:82:revient à 46/46. Le contrôle négatif (mélange, troncature) casse **46/46**. C'est un **codec de
journal/2026-11-07/README.md:93:**8/8 rejets attendus**, source Panini **SHA-256 `531bc75c…` inchangée** avant/après (fichier non
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "offset": 1, "limit": 15}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "offset": 220, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md</path>
<type>file</type>
<content>
1: # Corpus commun Panini/NIPADA ↔ Drave — UDHR, article 1
2: 
3: > **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.2 · **Date** : 2026-11-07
4: > **Verdict** : ✅ **le corpus est construit et vérifié** — **21 textes** (20 langues stratifiées + le
5: > français pivot), **5 familles**, **10 écritures**, **42 phrases**, **3 603 caractères**. Les **21**
6: > paires Panini ↔ Drave sont **identiques après normalisation** ; **418 paires exactes** sur **438**
7: > appariables (**95,4 %**). **20 écarts de surface** sont **exclus, pas corrigés**. Les **8 contrôles
8: > négatifs** sont des **rejets attendus** (8/8).
9: > **Dispositif** : lecture seule de `../Panini/research/data/udhr_corpus.json` (HEAD du dépôt
10: > `e10d695`, 2026-10-25 ; fichier **non suivi par git**, SHA-256 `531bc75c…`, vérifié avant et
11: > après) ; `data/udhr/articles_propres.jsonl`, `langues.jsonl`, `genealogie.json` (HEAD
12: > `9c7f71dc`, 2026-11-07) ; outil `../tools/corpus_commun.py` ;
13: > JSON [`corpus-commun.json`](corpus-commun.json). Le corpus lui-même vi
… [246 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md</path>
<type>file</type>
<content>
220: | contrôle | attendu | obtenu |
221: |---|---|---|
222: | égalité exacte Panini ↔ Drave, 21 textes | 21/21 | **21/21** |
223: | familles attendues (5) | 5/5 | **5/5** |
224: | UTF-8 strict, sans BOM, LF | 21/21 | **21/21** |
225: | une phrase par ligne, aucune ligne vide | 21/21 | **21/21** |
226: | reconstruction `textes/*.txt` == `corpus.jsonl` | 21/21 | **21/21** |
227: | déterminisme (`--verifier`, reconstruction octet par octet) | identique | **identique** |
228: | source Panini inchangée (SHA-256 avant/après) | `531bc75c…` | **`531bc75c…`** |
229: | contrôle négatif | 8/8 rejets attendus | **8/8** |
230: 
231: ### 5.1 Le contrôle négatif, test par test
232: 
233: | test | attendu | obtenu | ce qu'il vérifie |
234: |---|---|---|---|
235: | `temoin_paire_correcte` | acceptation | ✅ acceptation | la paire correcte passe |
236: | `panini_altere` | rejet | ✅ rejet | un caractère changé côté Panini casse l'égalité |
237: | `drave_altere` | rejet | ✅ rejet | un caractère changé côté Drave casse l'égalité |
238: | `appariement_croise` | rejet | ✅ rejet | l'an
… [826 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "> appariables (**95,4 %**). **20 écarts de surface** sont **exclus, pas corrigés**. Les **8 contrôles\n> négatifs** sont des **rejets attendus** (8/8).", "new_string": "> appariables (**9 … [170 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "| contrôle négatif | 8/8 rejets attendus | **8/8** |\n\n### 5.1 Le contrôle négatif, test par test", "new_string": "| contrôles (6 rejets + 2 témoins) | 8/8 conformes | **8/8** |\n\n### 5 … [33 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "Le contrôle négatif n'est donc pas un simple « relancer le script » : il **altère** le texte, **croise**\nles langues, **supprime** une phrase, **vide** une ligne et **falsifie** une empr … [466 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"contrôle négatif\\|contrôles négatifs\\|rejets attendus\" reports/rapport-corpus-commun.md journal/2026-11-07/README.md tools/corpus_commun.py", "description": "Find remaining control wording"}`

  ```
reports/rapport-corpus-commun.md:315:  contrôle négatif ;
journal/2026-11-07/README.md:82:revient à 46/46. Le contrôle négatif (mélange, troncature) casse **46/46**. C'est un **codec de
journal/2026-11-07/README.md:93:**8/8 rejets attendus**, source Panini **SHA-256 `531bc75c…` inchangée** avant/après (fichier non
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/README.md", "old_string": "**8/8 rejets attendus**, source Panini **SHA-256 `531bc75c…` inchangée** avant/après (fichier non", "new_string": "**8/8 tests conformes** (6 rejets, 2 témoins), source Panini **SHA-256 `531b … [45 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/README.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"tests de rejet\\|controle-negatif\" tools/corpus_commun.py | head", "description": "Find README control text"}`

  ```
16:    python3 tools/corpus_commun.py --controle-negatif
647:| `controle-negatif.json` | tests de rejet (altération, phrase supprimée, ligne vide, etc.) |
656:`--controle-negatif` rejoue les tests de rejet. Le script ne modifie jamais Panini : il vérifie
855:    (sortie / "controle-negatif.json").write_text(
870:        "controle_negatif": "work/corpus-commun/controle-negatif.json",
1041:        (sortie / "controle-negatif.json").read_text(encoding="utf-8")
1044:        erreurs.append("controle-negatif.json: verdict != PASS")
1046:        erreurs.append("controle-negatif.json: un test a échoué")
1071:        "--controle-negatif", action="store_true", help="rejouer les tests de rejet"
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\ns=s.replace('| `controle-negatif.json` | tests de rejet (altération, phrase supprimée, ligne vide, etc.) |','| `controle-negatif.json` | tests de contrôle (altération, phrase supprimée, ligne … [451 caractères tronqués]`

  ```
ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\nold='''            \"commune\": {\n                \"source\": \"eric-muller/udhr (Unicode UDHR XML Project)\",\n                \"url\": \"https://github.com/eric-muller/udhr\",\n            … [902 caractères tronqués]`

  ```
ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
{
 "fichier": "tools/corpus_commun.py",
 "sha256": "7753ac90454c891486c1f4b12e290c7198f9ede7223e37b6c20b1cf6d92f1815"
}
  ```

- **job_output** `{"job_id": "bash-120", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\nold='''        return subprocess.run(\n            [\"git\", \"-C\", str(depot), *args],\n            capture_output=True,\n            text=True,\n            timeout=10,\n            check= … [434 caractères tronqués]`

  ```
ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "sha256sum ../Panini/research/data/udhr_corpus.json; git -C ../Panini/research --no-optional-locks status --porcelain --untracked-files=no -- data/udhr_corpus.json; echo \"status_exit=$?\"", "description": "Verify Panini source hash"}`

  ```
531bc75c4d926cabc477165a6c7cd1ea70869ee0aa82d203053f30676d9cf190  ../Panini/research/data/udhr_corpus.json
status_exit=0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\nold='''        for cle in (\"textes\", \"controles\", \"statistiques\"):\n            if rapport.get(cle) != index.get(cle):\n                erreurs.append(f\"reports/corpus-commun.json: {cl … [422 caractères tronqués]`

  ```
ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\ns=r['statistiques']\nprint(s['n_textes'], s['n_phrases'], s['n_familles'], s['n_scripts'], s['n_caracteres'], s['n_mots_ws'])\nprint(r['controles'])\nprint(r['sources']['outil'])\nEOF", "description": "Veri … [29 caractères tronqués]`

  ```
21 42 5 10 3603 566
{'controle_negatif': {'n': 8, 'n_ok': 8, 'verdict': 'PASS'}, 'egalite_exacte': {'attendu': 21, 'n': 21, 'verdict': 'PASS'}, 'familles': {'attendu': 5, 'n': 5, 'verdict': 'PASS'}}
{'fichier': 'tools/corpus_commun.py', 'sha256': 'a32618c2132100d36e487e822ec1fe29428a1995421d69796f33baadc2f68b85'}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\nold='''    return {\n        \"date\": DATE,\n        \"n_tests\": len(tests),\n        \"n_ok\": sum(1 for t in tests if t[\"ok\"]),\n        \"verdict\": \"PASS\" if all(t[\"ok\"] for t in  … [805 caractères tronqués]`

  ```
ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
{'date': '2026-11-07', 'n_ok': 8, 'n_rejets_attendus': 6, 'n_temoins_attendus': 2, 'n_tests': 8, 'verdict': 'PASS'}
  ```

- **job_output** `{"job_id": "bash-120", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "offset": 1, "limit": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md</path>
<type>file</type>
<content>
1: # Corpus commun Panini/NIPADA ↔ Drave — UDHR, article 1
2: 
3: > **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.2 · **Date** : 2026-11-07
4: > **Verdict** : ✅ **le corpus est construit et vérifié** — **21 textes** (20 langues stratifiées + le
5: > français pivot), **5 familles**, **10 écritures**, **42 phrases**, **3 603 caractères**. Les **21**
6: > paires Panini ↔ Drave sont **identiques après normalisation** ; **418 paires exactes** sur **438**
7: > appariables (**95,4 %**). **20 écarts de surface** sont **exclus, pas corrigés**. Les **8 contrôles**
8: > (**6 rejets** attendus + **2 témoins** d'acceptation) sont **conformes** (8/8).
9: > **Dispositif** : lecture seule de `../Panini/research/data/udhr_corpus.json` (HEAD du dépôt
10: > `e10d695`, 2026-10-25 ; fichier **non suivi par git**, SHA-256 `531bc75c…`, vérifié avant et
11: > après) ; `data/udhr/articles_propres.jsonl`, `langues.jsonl`, `genealogie.json` (HEAD
12: > `9c7f71dc`, 2026-11-07) ; outil `../tools/corpus_commun.py` ;
13: > JSON [`corpus-commun.json`](corpus-
… [8146 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "- Panini/NIPADA : `research/data/udhr_corpus.json`, format `udhr-v2.0-xml`, **532 langues**,", "new_string": "- Panini/NIPADA : `../Panini/research/data/udhr_corpus.json`, format `udhr-v2 … [27 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "old_string": "3. **5 familles** glottolog × **4 langues**, les cinq familles les plus représentées du pool exact ;", "new_string": "3. **5 familles** glottolog × **4 langues**, parmi les six plus repré … [115 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "offset": 140, "limit": 100}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md</path>
<type>file</type>
<content>
140: 5. le **français** ajouté **hors strate** comme pivot de Drave (la langue de référence du dépôt).
141: 
142: | id | langue | écriture | famille | branche (feuille) | rôle | phrases | caractères |
143: |---|---|---|---|---:|---|---:|---:|
144: | `udhr_eng` | English | Latn | Indo-European | `macr1271` | strate | 2 | 170 |
145: | `udhr_hin` | Hindi | Deva | Indo-European | `hind1270` | strate | 2 | 189 |
146: | `udhr_bel` | Belarusan | Cyrl | Indo-European | `east1426` | strate | 2 | 154 |
147: | `udhr_ell_monotonic` | Greek (monotonic) | Grek | Indo-European | `nucl1783` | strate | 2 | 194 |
148: | `udhr_kin` | Rwanda | Latn | Atlantic-Congo | `rwan1241` | strate | 2 | 123 |
149: | `udhr_ewe` | Éwé | Latn | Atlantic-Congo | `ewei1234` | strate | 2 | 165 |
150: | `udhr_ibo` | Igbo | Latn | Atlantic-Congo | `cent2417` | strate | 2 | 157 |
151: | `udhr_fuf_adlm` | Pular (Adlam) | Adlm | Atlantic-Congo | `fula1264` | strate | 2 | 154 |
152: | `udhr_ind` | Indonesian | Latn | Austronesian | `stan1327` | strate | 2 | 181 |
153: | `udhr_tgl` | Tagalog | Latn | Aust
… [5250 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-corpus-commun.md')\ns=p.read_text()\ns=s.replace('| `controle-negatif.json` | les huit tests de rejet |','| `controle-negatif.json` | les huit tests de contrôle (6 rejets + 2 témoins) |')\np.write_text(s)\nprint('ok')\ … [53 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"controle-negatif\\|tests de\" work/corpus-commun/README.md | head", "description": "Check generated README wording"}`

  ```
27:| `controle-negatif.json` | tests de contrôle (altération, phrase supprimée, ligne vide, etc.) |
36:`--controle-negatif` rejoue les tests de contrôle. Le script ne modifie jamais Panini : il vérifie
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md", "offset": 240, "limit": 90}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md</path>
<type>file</type>
<content>
240: | `phrase_supprimee` | rejet | ✅ rejet | 1 phrase au lieu de 2 : refus |
241: | `ligne_vide` | rejet | ✅ rejet | 3 lignes dont une vide : refus |
242: | `empreinte_fausse` | rejet | ✅ rejet | une empreinte qui n'est pas celle du fichier est refusée |
243: | `pivot_francais_coherent` | acceptation | ✅ acceptation | le pivot est bien `Indo-European` et `pivot_fr` |
244: 
245: Le dispositif n'est donc pas un simple « relancer le script » : il **altère** le texte, **croise**
246: les langues, **supprime** une phrase, **vide** une ligne et **falsifie** une empreinte — six rejets
247: attendus — plus deux témoins qui doivent **accepter** (la paire correcte et la cohérence du pivot).
248: Les huit tests sont dans `work/corpus-commun/controle-negatif.json`.
249: 
250: ### 5.2 Ce qui pourrait rendre ce corpus faux
251: 
252: - **Le filtre d'égalité exacte** exclut 20 langues qui diffèrent par une apostrophe, une cédille ou
253:   une virgule. Si ces variantes sont systématiques dans une famille ou une écriture, l'échantillon
254:   est biaisé vers les orthographes «
… [5547 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-corpus-commun.md')\ns=p.read_text()\ns=s.replace('''- **Le filtre d'égalité exacte** exclut 20 langues qui diffèrent par une apostrophe, une cédille ou\n  une virgule. Si ces variantes sont systématiques dans une famil … [1166 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"tolér\\|rouge\\|indice\\|melange\\|sessions\" docs/pilotage/references-non-regression.md | head -40", "description": "Check tolerated gate reds"}`

  ```
3:> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).
6:> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
7:> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
8:> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
10:> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
15:> **Passe précédente — 2026-11-03 11 h 30 :** 82 portes, 80 vertes, 2 rouges structurelles
16:> (`indice` 821 s, `melange` 102 s), 1 h 48, GPU libres.
18:> **Passe précédente — 2026-11-03 à 04 h 10 :** 82 portes, 77 vertes, 5 rouges, 1 h 40 — 4 connues +
19:> `porte-sessions` (coordination, rejouée verte à 08 h 10 après la pause de N2/S).
22:> (17/17, 92 s, 0 rouge, `work/portes-n3-cloture/registre.txt`) ; elle est entrée **verte** dans la
28:> (journaux `/tmp/portes-1101-n2h`). Mêmes rouges que la passe du 31/10 : `porte-indice` (921 s),
29:> `porte-melange` (112 s), `porte-homeostasie` (environnementale) et `porte-reparti-moteur`.
32:> **Passe précédente — 2026-10-31 à 19 h 42 :*
… [826 caractères tronqués]
  ```

- **bash** `{"command": "ls -la work/portes-1107-15h11/ 2>/dev/null | tail -20; echo ---; tail -5 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check gate progress"}`

  ```
total 8
drwxr-xr-x. 1 stephane stephane  126  7 nov 15:12 .
drwxr-xr-x. 1 stephane stephane 1676  7 nov 15:13 ..
-rw-r--r--. 1 stephane stephane  580  7 nov 15:12 porte-adaptateur-sortie.log
-rw-r--r--. 1 stephane stephane    0  7 nov 15:12 porte-audit-drapeaux.log
-rw-r--r--. 1 stephane stephane   29  7 nov 15:12 registre.txt
---
porte-adaptateur-sortie 0 73
  ```

- **bash** `{"command": "date -u '+%H:%M:%S UTC'; date '+%H:%M:%S local'; ps -o pid,etime,cmd -C bash | grep -E \"porte-|toutes\" | head -10", "description": "Check gate elapsed time"}`

  ```
20:14:24 UTC
15:14:24 local
 820703       03:11 bash tools/toutes-les-portes.sh
 833976       01:59 bash tools/porte-audit-drapeaux.sh
 836007       00:00 bash -c date -u '+%H:%M:%S UTC'; date '+%H:%M:%S local'; ps -o pid,etime,cmd -C bash | grep -E "porte-|toutes" | head -10
  ```

- **bash** `{"command": "python3 tools/corpus_commun.py --verifier && echo \"OK\"", "description": "Final corpus verification"}`

  ```
VERIFIER: PASS
OK
  ```

- **bash** `{"command": "grep -R \"/home/\\|/tmp/\" reports/corpus-commun.json work/corpus-commun/index.json work/corpus-commun/README.md 2>/dev/null | head; echo done", "description": "Check for absolute paths"}`

  ```
done
  ```

- **bash** `{"command": "grep -R \"TODO\\|FIXME\\|XXX\" reports/rapport-corpus-commun.md reports/corpus-commun.json tools/corpus_commun.py work/corpus-commun/README.md | head; echo done", "description": "Check for TODOs"}`

  ```
done
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\nold='''        if relatif.endswith(\"#avant\"):\n            continue\n        chemin = (RACINE / relatif).resolve()\n'''\nnew='''        if relatif.endswith(\"#avant\"):\n            if sha2 … [422 caractères tronqués]`

  ```
ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "sha256sum tools/corpus_commun.py; python3 -c \"import json;print(json.load(open('reports/corpus-commun.json'))['sources']['outil']['sha256'])\"", "description": "Verify tool hash consistency"}`

  ```
57dbc0ff21c232db3d74899fe870e1b0f3a54826c7a98970359a970e96242e1a  tools/corpus_commun.py
57dbc0ff21c232db3d74899fe870e1b0f3a54826c7a98970359a970e96242e1a
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, unicodedata\nfrom pathlib import Path\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nart={}\nfor line in open('data/udhr/articles_propres.jsonl'):\n    d=json.loads(line)\n    if d['art']==1: art[d['fichier']]=d\ndef norm(s … [587 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 19, in <module>
AssertionError: cmn_hant
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, unicodedata, re\npan=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nart={}\nfor line in open('data/udhr/articles_propres.jsonl'):\n    d=json.loads(line)\n    if d['art']==1: art[d['fichier']]=d\ndef norm(s):\n    s=unicodedata. … [661 caractères tronqués]`

  ```
independent exact check: 21 texts
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-corpus-commun.md')\ns=p.read_text()\ns=s.replace('''- pas de **casse** (pas de `lower()`), pas de suppression des **diacritiques**, pas de\n  translittération, pas de normalisation de la ponctuation ;''','''- pas de ** … [269 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\nold='''            \"segmentation par ponctuation forte, sans modèle ; le tibétain a été écarté\",\n        ],\n'''\nnew='''            \"segmentation par ponctuation forte, sans modèle ; le  … [326 caractères tronqués]`

  ```
ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -5 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gate progress"}`

  ```
15:15:06 local
porte-adaptateur-sortie 0 73
2
  ```

- **bash** `{"command": "sed -n '1,80p' tools/porte-audit-drapeaux.sh", "description": "Inspect slow gate"}`

  ```
#!/bin/bash
# porte-audit-drapeaux.sh — chaque drapeau du harnais laisse-t-il dans le FICHIER sa trace ?
#
# POURQUOI CETTE PORTE. Le dépôt a un audit des drapeaux du MOTEUR (« huit drapeaux analysés mais
# jamais appliqués »). Le harnais vient de coûter **trois résultats faux publiés** pour la même
# raison, et le 11/10 l'audit en a trouvé **deux de plus** :
#
#   · `--masque 0.25` ne masquait que les `nn.Linear` (5,8 % des poids) : l'occupation du fichier
#     valait **83,9 %** là où le drapeau annonçait 26 %. Les chiffres d'E1 et d'E2 décrivaient
#     l'attention seule, sans le dire ;
#   · `--croissance` héritait du même défaut, et son gradient était lu sur `mod.weight.grad` — qui
#     vaut `None` quand le poids est reparamétré, donc la croissance ne voyait **aucun** gradient.
#
# CE QU'ELLE VÉRIFIE : pour chaque drapeau, une propriété **lisible dans le fichier exporté**
# (occupation, ratio de signes), comparée à ce que le drapeau promet — et **comparative** quand un
# seuil absolu jugerait la théorie plutôt que le drapeau (la croissance se juge contre le même
# masque statique, pas contre un pourcentage deviné).
#
# CE QU'ELLE NE VÉRIFIE PAS : les drapeaux sans trace atten
… [1020 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"s-paragraphes\\|atomes-niveaux\\|corpus-commun\" reports/INDEX.md", "description": "Check index entries"}`

  ```
59:| [rapport-atomes-niveaux.md](rapport-atomes-niveaux.md) | Table de correspondance — 14 atomes de Panini et 8 niveaux de Drave |
120:| [rapport-corpus-commun.md](rapport-corpus-commun.md) | Corpus commun Panini/NIPADA ↔ Drave — UDHR, article 1 |
679:| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -8 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l; ps -o pid,etime,cmd -C bash | grep -E \"porte-|toutes\" | head -5", "description": "Check gates progress"}`

  ```
15:15:22 local
porte-adaptateur-sortie 0 73
2
 820703       04:09 bash tools/toutes-les-portes.sh
 833976       02:56 bash tools/porte-audit-drapeaux.sh
 836877       00:00 bash -c date '+%H:%M:%S local'; tail -8 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l; ps -o pid,etime,cmd -C bash | grep -E "porte-|toutes" | head -5
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\nprint('top keys:', sorted(r))\nprint('sources keys:', sorted(r['sources']))\nprint('selection keys:', sorted(r['selection']))\nprint('stats keys:', sorted(r['statistiques']))\nprint('text keys:', sorted(r[' … [212 caractères tronqués]`

  ```
top keys: ['controle_negatif', 'controles', 'date', 'fiche', 'fichiers', 'intersection', 'ligne_roadmap', 'limites', 'normalisation', 'prochaine_etape', 'selection', 'sources', 'statistiques', 'statut', 'textes', 'titre', 'version']
sources keys: ['commune', 'drave', 'outil', 'panini']
selection keys: ['criteres', 'familles_attendues', 'n_pivots', 'n_strates', 'pivot', 'principe']
stats keys: ['familles', 'langues_par_famille', 'n_caracteres', 'n_familles', 'n_mots_ws', 'n_phrases', 'n_pivots', 'n_scripts', 'n_strates', 'n_textes', 'scripts']
text keys: ['branche', 'branche_feuille', 'branche_panini', 'drave_fichier', 'epoque', 'epoque_label', 'epoque_note', 'famille', 'famille_panini', 'genre', 'id', 'iso3', 'langue', 'nb_caracteres', 'nb_mots_ws', 'nb_phrases', 'niveau_glottolog', 'panini_cle', 'role', 'script', 'sens', 'sha256_fichier', 'sha256_source_drave', 'sha256_source_panini', 'tradition_panini']
textes ids: ['udhr_eng', 'udhr_hin', 'udhr_bel', 'udhr_ell_monotonic', 'udhr_kin', 'udhr_ewe', 'udhr_ibo', 'udhr_fuf_adlm', 'udhr_ind', 'udhr_tgl', 'udhr_mly_arab', 'udhr_jav', 'udhr_mya', 'udhr_cmn_hant', 'udhr_cnh', 'udhr_ctd', 'udhr_arb', 'udhr_amh', 'udhr_heb', 'udhr_hau_NE', 
… [126 caractères tronqués]
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -8 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:15:29 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
5
  ```

- **bash** `{"command": "git status --short -- data/udhr reports/corpus-commun.json reports/rapport-corpus-commun.md tools/corpus_commun.py docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-07/README.md reports/INDEX.md; echo ---; git diff --numstat -- docs/pilotage/en-cours.md docs/pilotage/ro … [106 caractères tronqués]`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-07/README.md
 M reports/INDEX.md
?? reports/corpus-commun.json
?? reports/rapport-corpus-commun.md
?? tools/corpus_commun.py
---
3	3	docs/pilotage/en-cours.md
2	2	docs/pilotage/roadmap.md
10	0	journal/2026-11-07/README.md
3	1	reports/INDEX.md
  ```

- **bash** `{"command": "git diff --check -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-07/README.md reports/INDEX.md; echo \"diffcheck=$?\"; git diff --no-index --check /dev/null reports/rapport-corpus-commun.md 2>/dev/null | head; echo done", "description": "Check whitespace errors"}`

  ```
diffcheck=0
done
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -10 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:15:42 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
6
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-corpus-commun.md')\ns=p.read_text()\ns=s.replace('''données de `Panini/research` est dans le même cas (le dépôt porte des centaines de milliers de\nfichiers non suivis). Le HEAD `e10d695` est donc celui du **dépôt**, p … [398 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\ng=json.load(open('data/udhr/genealogie.json'))\nprint('genealogie entries', len(g))\nl=[json.loads(x) for x in open('data/udhr/langues.jsonl')]\nprint('langues entries', len(l))\nEOF", "description": "Check genealogie count"}`

  ```
genealogie entries 441
langues entries 456
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\nold='''            \"drave\": {\n                **git_info(RACINE),\n                \"fichiers\": {\n                    \"data/udhr/langues.jsonl\": drave_hashes[\"langues\"],\n            … [934 caractères tronqués]`

  ```
ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-corpus-commun.md')\ns=p.read_text()\ns=s.replace('| Drave | `data/udhr/genealogie.json` | JSON | 456 | `9c7f71dc` | 2026-11-07 | `3d907676…` |','| Drave | `data/udhr/genealogie.json` | JSON | 441 | `9c7f71dc` | 2026-11 … [367 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sed -n '50,68p' reports/rapport-corpus-commun.md", "description": "Check source table"}`

  ```
| côté | fichier | format | langues | HEAD | date | SHA-256 |
|---|---|---|---|---|---|---|
| Panini/NIPADA | `../Panini/research/data/udhr_corpus.json` | JSON `udhr-v2.0-xml` | **532** | `e10d695` | 2026-10-25 | `531bc75c…` (fichier non suivi) |
| Drave | `data/udhr/articles_propres.jsonl` | JSONL | **456** | `9c7f71dc` | 2026-11-07 | `7ccac9c3…` |
| Drave | `data/udhr/langues.jsonl` | JSONL | 456 | `9c7f71dc` | 2026-11-07 | `12eee362…` |
| Drave | `data/udhr/genealogie.json` | JSON | 441 | `9c7f71dc` | 2026-11-07 | `3d907676…` |

Les **441** entrées de `genealogie.json` couvrent 441 des 456 fichiers Drave ; les **21** textes
retenus ont tous une branche Glottolog.

**Le fichier Panini n'est pas suivi par git.** `git ls-files` le refuse, et une grande partie des
données de `Panini/research` est dans le même cas (le dépôt porte des centaines de milliers de
fichiers non suivis ; voir [`rapport-inventaire-panini.md`](rapport-inventaire-panini.md) § 1.2).
Le HEAD `e10d695` est donc celui du **dépôt**, pas une version du fichier :
le contrôle de non-modification est l'**empreinte SHA-256 avant/après** (`531bc75c…`), pas un
`git diff`. C'est le contrôle qui fait foi ici.

La source décl
… [180 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\ng=set(json.load(open('data/udhr/genealogie.json')))\nf={json.loads(x)['fichier'] for x in open('data/udhr/langues.jsonl')}\nprint(len(g), len(f), len(g&f), len(g-f), len(f-g))\nprint(list(g-f)[:5], list(f-g)[:5])\nEOF", "description": "Check genealogy cov … [7 caractères tronqués]`

  ```
441 456 441 0 15
[] ['udhr_ike.xml', 'udhr_taj.xml', 'udhr_khk_mong.xml', 'udhr_iii.xml', 'udhr_umb.xml']
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\ng=set(json.load(open('data/udhr/genealogie.json')))\nf={json.loads(x)['fichier'] for x in open('data/udhr/langues.jsonl')}\nnoart=set(json.load(open('reports/corpus-commun.json'))['intersection']['listes']['sans_article1'])\nprint(sorted((f-g)))\nprint(so … [96 caractères tronqués]`

  ```
['udhr_bin.xml', 'udhr_csw.xml', 'udhr_iii.xml', 'udhr_ike.xml', 'udhr_kha.xml', 'udhr_khk_mong.xml', 'udhr_lia.xml', 'udhr_lus.xml', 'udhr_nym.xml', 'udhr_ojb.xml', 'udhr_qxu.xml', 'udhr_taj.xml', 'udhr_tgl_tglg.xml', 'udhr_tzm_tfng.xml', 'udhr_umb.xml']
['udhr_bin.xml', 'udhr_csw.xml', 'udhr_iii.xml', 'udhr_ike.xml', 'udhr_kha.xml', 'udhr_khk_mong.xml', 'udhr_lia.xml', 'udhr_lus.xml', 'udhr_nym.xml', 'udhr_ojb.xml', 'udhr_qxu.xml', 'udhr_taj.xml', 'udhr_tgl_tglg.xml', 'udhr_tzm_tfng.xml', 'udhr_umb.xml']
True
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-corpus-commun.md')\ns=p.read_text()\ns=s.replace('''Les **441** entrées de `genealogie.json` couvrent 441 des 456 fichiers Drave ; les **21** textes\nretenus ont tous une branche Glottolog.''','''Les **441** entrées de … [297 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 -c \"import json;print(json.dumps(json.load(open('reports/corpus-commun.json'))['sources']['drave'],ensure_ascii=False,indent=1))\"", "description": "Check Drave source counts"}`

  ```
{
 "date": "2026-11-07",
 "depot": "Qtrinet",
 "fichiers": {
  "data/udhr/articles_propres.jsonl": "7ccac9c3c641a72ac3aaa726c743ada8369d2419fbcb334c1da0a4833d2d7a6d",
  "data/udhr/genealogie.json": "3d907676892fb16ee18a522998ef63e6403951f0e6ac5853f486342e1e54a30d",
  "data/udhr/langues.jsonl": "12eee36241c1fc9ceb947a36406dcd357db523e87b50ebfa330b61a626a58dea"
 },
 "head": "9c7f71dc94986f50bdf4fcc58c728eea1e2d3b7a",
 "n_article1": 440,
 "n_genealogie": 441,
 "n_langues": 456
}
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -12 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:16:14 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
9
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-corpus-commun.md')\ns=p.read_text()\ns=s.replace('''  **famille Panini** ; la confrontation des deux représentations est possible sur ces 21 lignes,\n  avec la limite que les 21 textes ne couvrent que 5 familles (267/4 … [308 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cat work/corpus-commun/sources.sha256", "description": "Inspect source hashes"}`

  ```
531bc75c4d926cabc477165a6c7cd1ea70869ee0aa82d203053f30676d9cf190  ../Panini/research/data/udhr_corpus.json
12eee36241c1fc9ceb947a36406dcd357db523e87b50ebfa330b61a626a58dea  data/udhr/langues.jsonl
7ccac9c3c641a72ac3aaa726c743ada8369d2419fbcb334c1da0a4833d2d7a6d  data/udhr/articles_propres.jsonl
3d907676892fb16ee18a522998ef63e6403951f0e6ac5853f486342e1e54a30d  data/udhr/genealogie.json
df89ee6c551f0711ea077aa95baa3008c0e9f44a086a9f1bcb339ccfa9cc7fc6  tools/corpus_commun.py
531bc75c4d926cabc477165a6c7cd1ea70869ee0aa82d203053f30676d9cf190  ../Panini/research/data/udhr_corpus.json#avant
  ```

- **bash** `{"command": "sha256sum tools/corpus_commun.py; python3 -c \"import json;print(json.load(open('reports/corpus-commun.json'))['sources']['outil']['sha256'])\"", "description": "Check current tool hash"}`

  ```
df89ee6c551f0711ea077aa95baa3008c0e9f44a086a9f1bcb339ccfa9cc7fc6  tools/corpus_commun.py
df89ee6c551f0711ea077aa95baa3008c0e9f44a086a9f1bcb339ccfa9cc7fc6
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -12 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:16:29 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
9
  ```

- **bash** `{"command": "sed -n '1,160p' tools/porte-sessions.sh", "description": "Inspect sessions gate"}`

  ```
#!/bin/bash
# porte-sessions.sh — les plans de session sont lisibles et le linter refuse un doublon.
set -u
cd "$(dirname "$0")/.."
python3 tools/sessions.py --autotest || exit 1
python3 tools/sessions.py --check --strict || exit 1
echo "PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict"
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -15 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:16:46 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
9
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -15 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:16:52 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
10
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -16 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:16:57 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
10
  ```

- **bash** `{"command": "grep -n \"706\\|708\\|711\" reports/README.md reports/INDEX.md docs/pilotage/en-cours.md | head", "description": "Check counter mentions"}`

  ```
reports/README.md:152:| [`rapport-native-plafond.md`](rapport-native-plafond.md) | **N2 synthèse** — plafond **2,708**, six essais, porte 2,5 non atteinte |
reports/README.md:155:| [`rapport-native-prof20k-5.md`](rapport-native-prof20k-5.md) | **N2.19** — 30 000 pas : PPL **2,708**, précision **72,80 %** |
reports/INDEX.md:3:> **Généré** par `tools/index_reports.py` — **708 fiches**. Les fichiers
reports/INDEX.md:28:| [rapport-a80-porte-bus-socket.md](rapport-a80-porte-bus-socket.md) | A8.0 — `porte-bus-socket` épingle la référence et les trois régimes : 113,0068 / 148,7080 / 42,3176 / 148,9144 |
reports/INDEX.md:312:| [rapport-native-8b-warm.md](rapport-native-8b-warm.md) | N2.29 — 8 blocs réchauffés : 2,866, toujours derrière 2,708 |
reports/INDEX.md:341:| [rapport-native-plafond.md](rapport-native-plafond.md) | N2 — synthèse : le plafond de 2,708 |
reports/INDEX.md:351:| [rapport-native-prof20k-5.md](rapport-native-prof20k-5.md) | N2.19 — 30 000 pas de plus : PPL 2,708 |
docs/pilotage/en-cours.md:102:| fichiers / JSON de résultats | **711** / **804** | `reports/*.md` / `reports/*.json` |
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -18 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:17:03 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
10
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C bash | grep -E \"porte-|toutes\" | head -5; ls -lt work/portes-1107-15h11/*.log | head -5", "description": "See current gate"}`

  ```
820703       05:52 bash tools/toutes-les-portes.sh
 842477       00:13 bash tools/porte-bus.sh
 843805       00:01 bash tools/porte-bus.sh
 843817       00:00 bash -c ps -o pid,etime,cmd -C bash | grep -E "porte-|toutes" | head -5; ls -lt work/portes-1107-15h11/*.log | head -5
-rw-r--r--. 1 stephane stephane   68  7 nov 15:16 work/portes-1107-15h11/porte-bus.log
-rw-r--r--. 1 stephane stephane 2083  7 nov 15:16 work/portes-1107-15h11/porte-budget.log
-rw-r--r--. 1 stephane stephane 1035  7 nov 15:16 work/portes-1107-15h11/porte-bloc-tableaux.log
-rw-r--r--. 1 stephane stephane  877  7 nov 15:15 work/portes-1107-15h11/porte-bloc-maths.log
-rw-r--r--. 1 stephane stephane 1095  7 nov 15:15 work/portes-1107-15h11/porte-bloc-linguistique.log
  ```

- **bash** `{"command": "sed -n '927,960p' tools/corpus_commun.py", "description": "Read verifier temp block"}`

  ```
for rel in sorted(chemins_a - chemins_b):
        erreurs.append(f"fichier manquant : {rel}")
    for rel in sorted(chemins_b - chemins_a):
        erreurs.append(f"fichier en trop : {rel}")
    for rel in sorted(chemins_a & chemins_b):
        if sha256_fichier(a / rel) != sha256_fichier(b / rel):
            erreurs.append(f"contenu différent : {rel}")
    return erreurs


def verifier(sortie: Path) -> list[str]:
    erreurs: list[str] = []
    index_path = sortie / "index.json"
    if not index_path.is_file():
        return [f"index absent : {index_path}"]
    index = json.loads(index_path.read_text(encoding="utf-8"))
    records = index.get("textes", [])
    if not records:
        return ["index sans textes"]

    # 1. Reconstruire dans un dossier temporaire et comparer octet par octet.
    with tempfile.TemporaryDirectory(dir=sortie.parent, prefix=".verif-corpus-") as tmp:
        tmp_path = Path(tmp)
        construire(tmp_path, ecrire_rapport=False)
        erreurs.extend(comparer_arbres(sortie, tmp_path))
        if (sortie / "index.json").read_text(encoding="utf-8") != (
            tmp_path / "index.json"
        ).read_text(encoding="utf-8"):
            erreurs.append
… [227 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\nold='''    # 1. Reconstruire dans un dossier temporaire et comparer octet par octet.\n    with tempfile.TemporaryDirectory(dir=sortie.parent, prefix=\".verif-corpus-\") as tmp:\n        tmp_p … [2459 caractères tronqués]`

  ```
ok
compile-ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -20 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:17:39 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
10
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C bash | grep -E \"porte-|toutes\" | head -5", "description": "See current gate"}`

  ```
820703       06:28 bash tools/toutes-les-portes.sh
 842477       00:49 bash tools/porte-bus.sh
 847854       00:00 bash tools/porte-bus.sh
 847858       00:00 bash -c ps -o pid,etime,cmd -C bash | grep -E "porte-|toutes" | head -5
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -22 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:17:46 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
10
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\nf=r['intersection']['familles_exactes']\nprint('families labels',len(f),'sum',sum(f.values()))\nprint('unknown',f.get('(inconnue)'))\nEOF", "description": "Verify family labels count"}`

  ```
families labels 51 sum 418
unknown 10
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -24 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:17:53 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
10
  ```

- **bash** `{"command": "tail -20 work/portes-1107-15h11/porte-bus.log 2>/dev/null; echo ---; ps -o pid,etime,cmd -C bash | grep -E \"porte-bus|toutes\"", "description": "Inspect bus gate"}`

  ```
=== 1. bus NEUTRE : la sortie doit être identique AU BIT PRÈS ===
  sans bus : 59.0790 · bus neutre : 59.0790
  ✅ perplexité ET empreintes identiques (126 croisements, horodatage exclu)
=== 2. bus NON NEUTRE : le bus doit être BRANCHÉ ===
  gain=1.5 : 64.1160
  ✅ PPL bus épinglée : 64.116
  ✅ la sortie change : le bus agit
  ✅ les empreintes changent aussi
=== 3. le bus sur un nœud RELAIS (région du MILIEU) ===
  relais sans bus : 59.0790 · relais avec bus gain=1.5 : 66.0379
  ✅ PPL relais épinglées : 59,0790 / 66,0379
  ✅ le bus traverse les instances et agit sur la région du milieu
=== 4. bus diffusé par FICHIER DE CONTRÔLE, sur un nœud RELAIS (C5bis) ===
---
 820703       06:42 bash tools/toutes-les-portes.sh
 842477       01:03 bash tools/porte-bus.sh
 849070       00:05 bash tools/porte-bus.sh
 849265       00:00 bash tools/porte-bus.sh
 849287       00:00 bash -c tail -20 work/portes-1107-15h11/porte-bus.log 2>/dev/null; echo ---; ps -o pid,etime,cmd -C bash | grep -E "porte-bus|toutes"
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -26 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:17:59 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
10
  ```

- **bash** `{"command": "grep -c \"=== \" tools/porte-bus.sh; tail -5 tools/porte-bus.sh", "description": "Estimate bus gate steps"}`

  ```
4
print("  ✅ PPL fichier épinglées : 59,0790 / 66,0379")
PPLBUSF
[ -n "$R1" ] && [ "$R1" != "$R0" ] && echo "  ✅ le canal diffusé par fichier change la région du milieu" \
    || { echo "  ❌ le fichier de contrôle est sans effet"; exit 1; }
rm -rf "$T"
  ```

- **bash** `{"command": "find work/corpus-commun -maxdepth 1 -type d -name '.verif-*' -o -name '.corpus-*'; echo done; du -sh work/corpus-commun", "description": "Check temp dirs"}`

  ```
done
152K	work/corpus-commun
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -28 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:18:07 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
10
  ```

- **bash** `{"command": "sed -n '104,132p' reports/rapport-corpus-commun.md; echo ---; sed -n '250,275p' reports/rapport-corpus-commun.md", "description": "Read edited report sections"}`

  ```
`nym`, `ojb`, `qxu`, `taj`, `tgl_tglg`, `tzm_tfng`, `umb`. **Les 2 Drave hors Panini** :
`udhr_012.xml`, `udhr_prq.xml`. **Les 79 sans fichier Drave** se répartissent en **40 variantes
numériques** (`udhr_021.xml` … `udhr_072.xml`) et **39 codes absents** (`udhr_aar.xml`,
`udhr_ayo.xml`, `udhr_cmn_hans_beijing.xml`, …) ; la liste complète est dans le JSON.

### 2.3 Les familles du pool exact

Le pool exact de **418** paires couvre **51 étiquettes de famille** (dont **10 `(inconnue)`**).
Les cinq familles retenues sont **parmi les six plus représentées** ; le **turcique** (17 paires)
est écarté malgré un compte supérieur à l'**afro-asiatique** (12), parce qu'il n'ajoute aucune
écriture nouvelle (cyrillique, arabe et latin sont déjà couverts) :

| famille | paires exactes | part du pool | textes retenus |
|---|---:|---:|---:|
| Indo-European | 120 | 28,7 % | 5 |
| Atlantic-Congo | 81 | 19,4 % | 4 |
| Austronesian | 37 | 8,9 % | 4 |
| Sino-Tibetan | 17 | 4,1 % | 4 |
| Turkic | 17 | 4,1 % | 0 (écarté : écritures déjà couvertes) |
| Afro-Asiatic | 12 | 2,9 % | 4 |
| 45 autres étiquettes | 134 | 32,1 % | 0 |
| **total** | **418** | **100 %** | **21** |

Les cinq familles retenues couvren
… [2522 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\nprint('scripts pool?', r['statistiques']['scripts'])\nEOF", "description": "Check script count"}`

  ```
scripts pool? {'Adlm': 1, 'Arab': 2, 'Cyrl': 1, 'Deva': 1, 'Ethi': 1, 'Grek': 1, 'Hant': 1, 'Hebr': 1, 'Latn': 11, 'Mymr': 1}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\n# use exact files list, map to Panini key -> script\np=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nscripts=set()\nfor f in r['intersection']['listes']['exacts']:\n    k=f[5:-4] … [124 caractères tronqués]`

  ```
36 ['Adlm', 'Arab', 'Armn', 'Beng', 'Cakm', 'Cher', 'Cyrl', 'Deva', 'Ethi', 'Gran', 'Grek', 'Gujr', 'Guru', 'Hang', 'Hani', 'Hans', 'Hant', 'Hebr', 'Java', 'Jpan', 'Knda', 'Lana', 'Laoo', 'Latn', 'Mlym', 'Mymr', 'Sinh', 'Syrc', 'Taml', 'Tavt', 'Telu', 'Tfng', 'Thaa', 'Thai', 'Tibt', 'Vaii']
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -30 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:18:18 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -32 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:18:23 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C bash | grep -E \"porte-|toutes\" | head -5", "description": "See current gate"}`

  ```
820703       07:12 bash tools/toutes-les-portes.sh
 851855       00:08 bash tools/porte-bus-socket.sh
 851950       00:04 bash tools/porte-bus-socket.sh
 852410       00:00 bash -c ps -o pid,etime,cmd -C bash | grep -E "porte-|toutes" | head -5
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -34 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:18:30 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -36 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:18:33 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "tail -20 work/portes-1107-15h11/porte-bus-socket.log 2>/dev/null; echo ---; ps -o pid,etime,cmd -C bash | grep -E \"bus-socket|toutes\"", "description": "Inspect bus-socket gate"}`

  ```
=== 1. référence : aucun bus ===
  perplexité de référence : 113.0068
  ✅ PPL référence épinglée : 113.0068
=== 2. bus STATIQUE sur le nœud (--bus gain=2.0) ===
---
 820703       07:23 bash tools/toutes-les-portes.sh
 851855       00:18 bash tools/porte-bus-socket.sh
 853011       00:03 bash tools/porte-bus-socket.sh
 853378       00:00 bash -c tail -20 work/portes-1107-15h11/porte-bus-socket.log 2>/dev/null; echo ---; ps -o pid,etime,cmd -C bash | grep -E "bus-socket|toutes"
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -38 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:18:39 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -40 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:18:43 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "for f in fuf_adlm mly_arab arb heb mya; do echo \"=== $f\"; sed -n '1,3p' work/corpus-commun/textes/udhr_$f.txt; done", "description": "Inspect RTL and non-Latin texts"}`

  ```
=== fuf_adlm
𞤋𞤲𞥆𞤢𞤥𞤢 𞤢𞥄𞤣𞤫𞥅𞤶𞤭 𞤬𞤮𞤬 𞤨𞤮𞤼𞤭، 𞤲'𞤣𞤭𞤥𞤯𞤭𞤣𞤭 𞤫 𞤶𞤭𞤦𞤭𞤲𞤢𞤲𞥆𞤣𞤫 𞤼𞤮 𞤦𞤢𞤲𞥆𞤺𞤫 𞤸𞤢𞤳𞥆𞤫𞥅𞤶𞤭.
𞤉𞤩𞤫 𞤲'𞤺𞤮𞥅𞤣𞤭 𞤥𞤭𞥅𞤶𞤮 𞤫 𞤸𞤢𞤳𞥆𞤭𞤤𞤢𞤲𞤼𞤢𞥄𞤺𞤢𞤤 𞤫𞤼𞤫 𞤫𞤩𞤫 𞤨𞤮𞤼𞤭 𞤸𞤵𞥅𞤬𞤮 𞤲'𞤣𞤭𞤪𞤣𞤫 𞤫 𞤲'𞤣𞤫𞤪 𞤩 𞤭𞤴𞤲𞤺𞤵𞤴𞤵𞤥𞥆𞤢𞥄𞤺𞤵.
=== mly_arab
سموا مأنسي دلاهيركن بيبس دان سامرات دري سڬي كموليأن دان حق٢.
مريك ممڤوڽاي ڤميكيرن دان ڤراسأن هاتي دان هندقله برتيندق د انتارا ساتو سام لائن دڠن سماڠت ڤرساودارأن.
=== arb
يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق.
وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء.
=== heb
כל בני אדם נולדו בני חורין ושווים בערכם ובזכויותיהם.
כולם חוננו בתבונה ובמצפון, לפיכך חובה עליהם לנהוג איש ברעהו ברוח של אחוה.
=== mya
လူတိုင်းသည် တူညီ လွတ်လပ်သော ဂုဏ်သိက္ခာဖြင့် လည်းကောင်း၊ တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့် လည်းကောင်း၊ မွေးဖွားလာသူများ ဖြစ်သည်။
ထိုသူတို့၌ ပိုင်းခြား ဝေဖန်တတ်သော ဉာဏ်နှင့် ကျင့်ဝတ် သိတတ်သော စိတ်တို့ရှိကြ၍ ထိုသူတို့သည် အချင်းချင်း မေတ္တာထား၍ ဆက်ဆံကျင့်သုံးသင့်၏။
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -42 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:18:51 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "grep -n \"sleep\\|timeout\\|attendre\\|wait\" tools/porte-bus-socket.sh | head -20; tail -10 work/portes-1107-15h11/porte-bus-socket.log", "description": "Check bus-socket gate progress"}`

  ```
12:# qu'après. L'ordre est alors garanti par la porte elle-même, pas par un `sleep`
58:s = socket.create_connection(("127.0.0.1", port), timeout=5)
74:  sleep 2
79:  sleep 2
82:            for p in "${PIDS[@]}"; do wait "$p" 2>/dev/null; done; PIDS=(); }
161:sleep 3
163:wait $PID 2>/dev/null
193:sleep 1.2
195:wait $PID 2>/dev/null
212:sleep 1.2
214:wait $PID 2>/dev/null
=== 2. bus STATIQUE sur le nœud (--bus gain=2.0) ===
  [bus] canaux actifs sur ce nœud : gain=2
  perplexité avec gain statique : 148.7080
  ✅ PPL gain statique épinglée : 148.708
=== 3. bus par SOCKET, ligne envoyée avant la connexion du pilote ===
  bus : OK gain 2
  perplexité par socket : 148.7080
  écart socket / statique : 0.000000e+00
  ✅ identique au bit près (0,00e0)
=== 4. ligne NEUTRE par socket : rien ne doit changer ===
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -44 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:18:59 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "tail -8 work/portes-1107-15h11/porte-bus-socket.log; ps -o pid,etime,cmd -C bash | grep -E \"bus-socket|toutes\"", "description": "Check bus-socket completion"}`

  ```
perplexité par socket : 148.7080
  écart socket / statique : 0.000000e+00
  ✅ identique au bit près (0,00e0)
=== 4. ligne NEUTRE par socket : rien ne doit changer ===
  bus : OK gain 1
  écart neutre / référence : 0.000000e+00
  ✅ identique au bit près (0,00e0)
=== 5. ligne envoyée EN PLEIN VOL ===
 820703       07:48 bash tools/toutes-les-portes.sh
 851855       00:43 bash tools/porte-bus-socket.sh
 855891       00:00 bash -c tail -8 work/portes-1107-15h11/porte-bus-socket.log; ps -o pid,etime,cmd -C bash | grep -E "bus-socket|toutes"
  ```

- **bash** `{"command": "ls tools/porte-*journal* tools/porte-*doc* 2>/dev/null; echo done", "description": "Find doc/journal gates"}`

  ```
tools/porte-document.sh
done
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -46 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:19:08 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "tail -12 work/portes-1107-15h11/porte-bus-socket.log; ps -o pid,etime,cmd -C bash | grep -E \"bus-socket|toutes\"", "description": "Check bus-socket final"}`

  ```
✅ PPL gain statique épinglée : 148.708
=== 3. bus par SOCKET, ligne envoyée avant la connexion du pilote ===
  bus : OK gain 2
  perplexité par socket : 148.7080
  écart socket / statique : 0.000000e+00
  ✅ identique au bit près (0,00e0)
=== 4. ligne NEUTRE par socket : rien ne doit changer ===
  bus : OK gain 1
  écart neutre / référence : 0.000000e+00
  ✅ identique au bit près (0,00e0)
=== 5. ligne envoyée EN PLEIN VOL ===
  bus : OK gain 2 (pendant que le pilote calcule)
 820703       07:57 bash tools/toutes-les-portes.sh
 851855       00:52 bash tools/porte-bus-socket.sh
 856632       00:00 bash -c tail -12 work/portes-1107-15h11/porte-bus-socket.log; ps -o pid,etime,cmd -C bash | grep -E "bus-socket|toutes"
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -48 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:19:15 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -50 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:19:18 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "tail -15 work/portes-1107-15h11/porte-bus-socket.log; ps -o pid,etime,cmd -C bash | grep -E \"bus-socket|toutes\"", "description": "Check bus-socket final"}`

  ```
=== 2. bus STATIQUE sur le nœud (--bus gain=2.0) ===
  [bus] canaux actifs sur ce nœud : gain=2
  perplexité avec gain statique : 148.7080
  ✅ PPL gain statique épinglée : 148.708
=== 3. bus par SOCKET, ligne envoyée avant la connexion du pilote ===
  bus : OK gain 2
  perplexité par socket : 148.7080
  écart socket / statique : 0.000000e+00
  ✅ identique au bit près (0,00e0)
=== 4. ligne NEUTRE par socket : rien ne doit changer ===
  bus : OK gain 1
  écart neutre / référence : 0.000000e+00
  ✅ identique au bit près (0,00e0)
=== 5. ligne envoyée EN PLEIN VOL ===
  bus : OK gain 2 (pendant que le pilote calcule)
 820703       08:08 bash tools/toutes-les-portes.sh
 851855       01:03 bash tools/porte-bus-socket.sh
 858190       00:00 bash -c tail -15 work/portes-1107-15h11/porte-bus-socket.log; ps -o pid,etime,cmd -C bash | grep -E "bus-socket|toutes"
  ```

- **bash** `{"command": "sed -n '1,80p' tools/porte-document.sh", "description": "Inspect doc gate"}`

  ```
#!/bin/bash
# porte-document.sh — R0.1 : le document est un graphe, et le graphe se vérifie.
#
# POURQUOI CETTE PORTE EXISTE. Une découpe de document qui « a l'air bonne » n'est pas une
# découpe : sans partition exacte, un offset faux ne se voit pas ; sans extraction
# indépendante, un extracteur qui invente des mots ne se voit pas non plus. Cette porte
# exige donc les trois choses ensemble — partition, fidélité, rejeu — plus trois contrôles
# négatifs qui doivent ÉCHOUER (texte plat, deux colonnes, notes hors corps).
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ==="
python3 tools/graphe_document.py --porte
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte document verte" || echo "❌ porte document ROUGE (code $CODE)"
exit "$CODE"
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -52 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:19:26 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "ps -eo pid,etime,pcpu,pmem,cmd | grep -E \"bus-socket|python3.*bus|toutes-les\" | grep -v grep | head -10", "description": "Check bus-socket process CPU"}`

  ```
820703       08:16  0.0  0.0 bash tools/toutes-les-portes.sh
 851854       01:11  0.0  0.0 timeout 1800 bash tools/porte-bus-socket.sh
 851855       01:11  0.0  0.0 bash tools/porte-bus-socket.sh
  ```

- **bash** `{"command": "ps --ppid 851855 -o pid,etime,pcpu,cmd; ps --ppid 851854 -o pid,etime,pcpu,cmd", "description": "Check gate children"}`

  ```
PID     ELAPSED %CPU CMD
 855877       00:29  780 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 53384 --topologie /tmp/tmp.TtOPwu9oZ7/topo.json --region n2 --ctx 256 --threads 8
 855956       00:27  775 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 53383 --topologie /tmp/tmp.TtOPwu9oZ7/topo.json --region n1 --ctx 256 --threads 8 --bus-serveur 54243
 856001       00:25  899 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:53383 --topologie /tmp/tmp.TtOPwu9oZ7/topo.json --ids-file /tmp/campagne24/ids_0.5B-Q8.txt --limit 256 --ctx 256 --threads 8 --flux f32
    PID     ELAPSED %CPU CMD
 851855       01:13  0.0 bash tools/porte-bus-socket.sh
  ```

- **bash** `{"command": "for p in reports/rapport-corpus-commun.md reports/corpus-commun.json tools/corpus_commun.py work/corpus-commun/index.json work/corpus-commun/corpus.jsonl work/corpus-commun/metadata.tsv ../Panini/research/data/udhr_corpus.json data/udhr/articles_propres.jsonl data/udhr/langues.jsonl dat … [141 caractères tronqués]`

  ```
OK reports/rapport-corpus-commun.md
OK reports/corpus-commun.json
OK tools/corpus_commun.py
OK work/corpus-commun/index.json
OK work/corpus-commun/corpus.jsonl
OK work/corpus-commun/metadata.tsv
OK ../Panini/research/data/udhr_corpus.json
OK data/udhr/articles_propres.jsonl
OK data/udhr/langues.jsonl
OK data/udhr/genealogie.json
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -54 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:19:36 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -56 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:19:42 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "cat work/portes-1107-15h11/porte-bloc-code.log", "description": "Inspect code gate log"}`

  ```
=== PORTE R4.2 — LE BLOC CODE ===
=== PORTE R4.2 — LE BLOC CODE ===
1. parseur     : 345/345 fichiers acceptés, 577948 nœuds, 2282 fonctions, 97 classes
2. exécution   : 24/24 snippets exacts
3. portée      : x module=module / x fonction=fonction ; y=2 ; noms libres flux=1, portée=0
4. contrôle    : texte faux 3/3, exécution juste 3/3
     2**10 + 24       exécute   1048 · texte      2
     sum(range(10))   exécute     45 · texte     10
     (3 + 4) * 2      exécute     14 · texte      3
5. refus       : 7/7 nommés (syntaxe, import, attribut, division_zero, nom_inconnu, boucle, appel_interdit)
6. coût        : ×4.35 de temps pour ×4 nœuds (0.30 ms / 50 additions)
7. miroir      : 345/345 fichiers rendus puis relus à l'identique ; contrôle aplati perdu
8. rejeu       : identique
✅ porte bloc code verte
✅ porte bloc code verte
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -58 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:19:47 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "sed -n '1,30p' docs/pilotage/references-non-regression.md", "description": "Read reference pass header"}`

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
… [753 caractères tronqués]
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -60 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:19:55 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
11
  ```

- **bash** `{"command": "tail -6 work/portes-1107-15h11/porte-bus-socket.log; ps -o pid,etime,cmd -C bash | grep -E \"bus-socket|toutes\"", "description": "Check bus-socket log"}`

  ```
=== 6. le bus du PILOTE : neutre par socket, inerte AU BIT PRÈS ===
  bus du pilote : OK gain 1
  neutre côté pilote / référence : 0.000000e+00
  ✅ identique au bit près (0,00e0)
=== 7. le bus du PILOTE branché : une ligne non neutre change le résultat ===
  bus du pilote : OK gain 2
 820703       08:44 bash tools/toutes-les-portes.sh
 851855       01:39 bash tools/porte-bus-socket.sh
 862154       00:00 bash -c tail -6 work/portes-1107-15h11/porte-bus-socket.log; ps -o pid,etime,cmd -C bash | grep -E "bus-socket|toutes"
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -62 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:20:01 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
porte-bus-socket 0 102
12
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -64 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:20:06 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
porte-bus-socket 0 102
12
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -66 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:20:10 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
porte-bus-socket 0 102
12
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C bash | grep -E \"porte-|toutes\" | head -5", "description": "See current gate"}`

  ```
820703       08:59 bash tools/toutes-les-portes.sh
 862501       00:12 bash tools/porte-c4-retard.sh
 863610       00:07 bash tools/porte-c4-retard.sh
 864639       00:00 bash -c ps -o pid,etime,cmd -C bash | grep -E "porte-|toutes" | head -5
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -68 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:20:15 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
porte-bus-socket 0 102
12
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -70 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:20:19 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
porte-bus-socket 0 102
12
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nc=json.load(open('work/corpus-commun/controle-negatif.json'))\nfor t in c['tests']:\n    print(t['nom'], t['attendu'], t['obtenu'], t['ok'])\nprint(c['n_tests'], c['n_ok'], c['n_rejets_attendus'], c['n_temoins_attendus'], c['verdict'])\nEOF", "description … [35 caractères tronqués]`

  ```
temoin_paire_correcte acceptation acceptation True
panini_altere rejet rejet True
drave_altere rejet rejet True
appariement_croise rejet rejet True
phrase_supprimee rejet rejet True
ligne_vide rejet rejet True
empreinte_fausse rejet rejet True
pivot_francais_coherent acceptation acceptation True
8 8 6 2 PASS
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -72 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:20:26 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
porte-bus-socket 0 102
12
  ```

- **bash** `{"command": "tail -5 work/portes-1107-15h11/porte-c4-retard.log 2>/dev/null; ps -o pid,etime,cmd -C bash | grep -E \"c4-retard|toutes\"", "description": "Check c4 gate"}`

  ```
✅ PPL du retard épinglées : 14,6496 / 14,6496 / 9 277,9771 / 151 517,0001
  ✅ retard 0 = modèle entier (14.6496 = 14.6496) : la coupe est exacte
  ✅ un pas de retard coûte ×633 : la POSITION d'un état est son identité
  ✅ la dégradation sature (retard 8 : ×10343, pas moins que le retard 1)
=== 5. politique : un état MANQUANT coûte moins qu'un état PÉRIMÉ (on ne réutilise jamais) ===
 820703       09:17 bash tools/toutes-les-portes.sh
 862501       00:30 bash tools/porte-c4-retard.sh
 868035       00:01 bash tools/porte-c4-retard.sh
 868049       00:00 bash -c tail -5 work/portes-1107-15h11/porte-c4-retard.log 2>/dev/null; ps -o pid,etime,cmd -C bash | grep -E "c4-retard|toutes"
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; tail -74 work/portes-1107-15h11/registre.txt 2>/dev/null; ls work/portes-1107-15h11/*.log 2>/dev/null | wc -l", "description": "Check gates progress"}`

  ```
15:20:33 local
porte-adaptateur-sortie 0 73
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 85
porte-bus-socket 0 102
12
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 300000}`

  ```
porte-audit-drapeaux   ✅                         182 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          13 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          17 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          52 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          85 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅                         102 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard        ✅                          34 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynch
… [485 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 300000}`

  ```
porte-cycle-c2         ✅                         141 s    ✅ porte tenue (chaîne exacte · pas 1 exact · borné · coût dit · trajectoire déterministe ·
  porte-deepseek         ✅                           0 s    ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
  porte-delais           ✅                          24 s    ✅ le temps, lui, augmente : 8.01 s → 11.55 s (+3.5 s ≈ 50 ms × 64 pas)
  porte-diff-couche      ✅                          21 s    ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé
  porte-document         ✅                           6 s  ✅ porte document verte
  porte-echange-experts  ✅                          59 s    PORTE TENUE
[status: running]
  ```

- **bash** `{"command": "awk '$2 != 0 {print}' work/portes-1107-15h11/registre.txt 2>/dev/null; echo \"rouges=$(awk '$2 != 0' work/portes-1107-15h11/registre.txt 2>/dev/null | wc -l)\"", "description": "Check reds so far"}`

  ```
rouges=0
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 300000}`

  ```
porte-episodique       ✅                         195 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           1 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          27 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                           8 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
[status: running]
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 300000}`

  ```
porte-gain             ✅                         241 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
[status: running]
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 300000}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

You are repeating the exact same tool call with identical arguments. Carefully analyze the previous result before calling again: if the task is not complete, try a different approach or different arguments instead of repeating the call.

- **bash** `{"command": "python3 - <<'EOF'\nimport csv, json\nrows=list(csv.DictReader(open('work/corpus-commun/metadata.tsv',encoding='utf-8'),delimiter='\\t'))\nprint('rows',len(rows))\nprint('ids unique',len({r['id'] for r in rows}))\nprint('epochs',sorted({r['epoque'] for r in rows}))\nprint('genres',sorted … [306 caractères tronqués]`

  ```
rows 21
ids unique 21
epochs ['1948']
genres ['declaration']
familles ['Afro-Asiatic', 'Atlantic-Congo', 'Austronesian', 'Indo-European', 'Sino-Tibetan']
roles ['pivot_fr', 'strate']
phrases sum 42
chars sum 3603
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nlines=[json.loads(l) for l in open('work/corpus-commun/corpus.jsonl',encoding='utf-8')]\nprint('lines',len(lines))\nprint('ids',len({l['id'] for l in lines}))\nprint('phrases per id', {i:sum(1 for l in lines if l['id']==i) for i in sorted({l['id'] for l i … [109 caractères tronqués]`

  ```
lines 42
ids 21
phrases per id {'udhr_amh': 2, 'udhr_arb': 2, 'udhr_bel': 2, 'udhr_cmn_hant': 2, 'udhr_cnh': 2, 'udhr_ctd': 2, 'udhr_ell_monotonic': 2, 'udhr_eng': 2, 'udhr_ewe': 2, 'udhr_fra': 2, 'udhr_fuf_adlm': 2, 'udhr_hau_NE': 2, 'udhr_heb': 2, 'udhr_hin': 2, 'udhr_ibo': 2, 'udhr_ind': 2, 'udhr_jav': 2, 'udhr_kin': 2, 'udhr_mly_arab': 2, 'udhr_mya': 2, 'udhr_tgl': 2}
epochs [1948]
  ```

- **bash** `{"command": "git diff --stat -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-07/README.md reports/INDEX.md; echo ---; wc -l reports/rapport-corpus-commun.md reports/corpus-commun.json tools/corpus_commun.py; echo ---; git status --short -- docs/pilotage/en-cours.md docs/pilotag … [178 caractères tronqués]`

  ```
docs/pilotage/en-cours.md    |  6 +++---
 docs/pilotage/roadmap.md     |  4 ++--
 journal/2026-11-07/README.md | 10 ++++++++++
 reports/INDEX.md             |  4 +++-
 4 files changed, 18 insertions(+), 6 deletions(-)
---
   330 reports/rapport-corpus-commun.md
  1417 reports/corpus-commun.json
  1153 tools/corpus_commun.py
  2900 total
---
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-07/README.md
 M reports/INDEX.md
?? reports/corpus-commun.json
?? reports/rapport-corpus-commun.md
?? tools/corpus_commun.py
  ```

- **bash** `{"command": "grep -n \"chinois\\|amharique\\|tibétain\\|20 langues\" work/corpus-commun/README.md", "description": "Check README limits wording"}`

  ```
45:- **Sélection non aléatoire** : 20 langues stratifiées (5 familles × 4) + le français, choisis pour
46:  la diversité des écritures et parce que le texte est identique des deux côtés. Les 20 langues
49:  le chinois et l'amharique, qui ne séparent pas les mots par des espaces. Ce n'est pas une
52:  abréviations. Le tibétain a été écarté de l'échantillon pour cette raison.
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; awk '{print $2}' work/portes-1107-15h11/registre.txt 2>/dev/null | sort | uniq -c; tail -5 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check gate counts and latest"}`

  ```
15:46:08 local
     26 0
porte-episodique 0 195
porte-etat 0 1
porte-flux 0 27
porte-fusion 0 8
porte-gain 0 241
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/corpus_commun.py')\ns=p.read_text()\nold='''            \"nb_phrases\": len(phrases),\n            \"nb_mots_ws\": sum(len(p.split()) for p in phrases),\n            \"nb_caracteres\": len(source_panini),\n'''\nnew='''           … [366 caractères tronqués]`

  ```
ok
CONSTRUIRE: 21 textes, 42 phrases, 5 familles, 10 écritures
VERIFIER: PASS
  ```

- **bash** `{"command": "ls -lh reports/corpus-commun.json work/corpus-commun/index.json; python3 - <<'EOF'\nimport json\nr=json.load(open('reports/corpus-commun.json'))\nprint(r['textes'][0]['id'], r['textes'][0]['phrases'])\nprint(len(r['textes']), sum(len(x['phrases']) for x in r['textes']))\nEOF", "descript … [34 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 52K  7 nov 15:46 reports/corpus-commun.json
-rw-r--r--. 1 stephane stephane 37K  7 nov 15:46 work/corpus-commun/index.json
udhr_eng ['All human beings are born free and equal in dignity and rights.', 'They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.']
21 42
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; awk '{print $2}' work/portes-1107-15h11/registre.txt 2>/dev/null | sort | uniq -c; tail -3 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check gate counts"}`

  ```
15:46:29 local
     26 0
porte-flux 0 27
porte-fusion 0 8
porte-gain 0 241
  ```

- **job_list** `{}`

  ```
bash-16 [bash] completed — grep -rIl "aristotle\|bengio\|book_of_enoch\|brahmajala" data/ 2>/dev/null | head -20; echo ---; find data -maxdepth 2 -iname "*gutenberg*" -o -iname "*sacred*" -o -iname "*corpus*" | head -40
bash-120 [bash] running — bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "ls -lt work/portes-1107-15h11/*.log | head -3; tail -5 work/portes-1107-15h11/porte-greffe.log 2>/dev/null", "description": "Check current gate log"}`

  ```
-rw-r--r--. 1 stephane stephane 1000  7 nov 15:45 work/portes-1107-15h11/porte-greffe.log
-rw-r--r--. 1 stephane stephane 4655  7 nov 15:36 work/portes-1107-15h11/porte-gain.log
-rw-r--r--. 1 stephane stephane 1844  7 nov 15:32 work/portes-1107-15h11/porte-fusion.log
  ✅ l'état injecté porte bien la direction du contenu de A
=== 4. CORRIGÉ : l'état de A dans C (sans aucun code) DONNE le code ===
  poids 1    : [220, 16, 17, 18, 19, 20, 21, 22]
  poids 2    : [1863, 48, 41, 43, 198, 16141, 374, 25]
  poids 4    : [1863, 48, 41, 43, 198, 16141, 374, 25]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport hashlib, json\nr=json.load(open('reports/corpus-commun.json'))\nfor x in r['textes']:\n    content='\\n'.join(x['phrases'])+'\\n'\n    h=hashlib.sha256(content.encode()).hexdigest()\n    assert h==x['sha256_fichier'], x['id']\nprint('phrases/hash OK for', len(r … [68 caractères tronqués]`

  ```
phrases/hash OK for 21
  ```

- **bash** `{"command": "sed -n '85,105p' docs/pilotage/en-cours.md", "description": "Read en-cours final section"}`

  ```
## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
- **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
- **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; la fusion garde l'heuristique ; **`r035` réglé** (237/238, 0,9958) ; **convention des GV réglée** (F1 **0,7902**, sujet hors du GV + adverbe final, 0 perte d'attachement) ; **schéma v2** publié (26 cas, 0 échec ; `meta.partition`/`meta.alternative`, v1 lue) ; **restitution v0** : **46/46 surfaces**, miroir **0,1087** ; [fiche](../../reports/rapport-restitution-v0.md).
- **L — le bloc langue** : contrat ; frontière script 1,
… [822 caractères tronqués]
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; awk '{print $2}' work/portes-1107-15h11/registre.txt 2>/dev/null | sort | uniq -c; tail -2 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check gate counts"}`

  ```
15:46:45 local
     26 0
porte-fusion 0 8
porte-gain 0 241
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; awk '{print $2}' work/portes-1107-15h11/registre.txt 2>/dev/null | sort | uniq -c; tail -2 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check gate counts"}`

  ```
15:46:51 local
     26 0
porte-fusion 0 8
porte-gain 0 241
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport unicodedata, pathlib\nbad=[]\nfor p in sorted(pathlib.Path('work/corpus-commun/textes').glob('*.txt')):\n    t=p.read_text(encoding='utf-8')\n    if '\\t' in t: bad.append((p.name,'tab'))\n    for ch in t:\n        if unicodedata.category(ch)=='Cc' and ch not i … [233 caractères tronqués]`

  ```
control chars: []
files: 21
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\nbad=[]\nfor p in sorted(pathlib.Path('work/corpus-commun/textes').glob('*.txt')):\n    for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):\n        if line!=line.strip(): bad.append((p.name,i,repr(line[-10:])))\nprint('leading/traili … [85 caractères tronqués]`

  ```
leading/trailing spaces: [] count 0
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; awk '{print $2}' work/portes-1107-15h11/registre.txt 2>/dev/null | sort | uniq -c; tail -2 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check gate counts"}`

  ```
15:47:06 local
     26 0
porte-fusion 0 8
porte-gain 0 241
  ```

- **bash** `{"command": "tail -3 work/portes-1107-15h11/porte-greffe.log 2>/dev/null; ps -o pid,etime,cmd -C bash | grep -E \"greffe|toutes\"", "description": "Check greffe gate progress"}`

  ```
poids 2    : [1863, 48, 41, 43, 198, 16141, 374, 25]
  poids 4    : [1863, 48, 41, 43, 198, 16141, 374, 25]
  poids 10   : [1863, 48, 41, 43, 198, 16141, 374, 25]
 820703       35:55 bash tools/toutes-les-portes.sh
 985518       10:29 bash tools/porte-greffe.sh
 990873       00:24 bash tools/porte-greffe.sh
 991104       00:00 bash -c tail -3 work/portes-1107-15h11/porte-greffe.log 2>/dev/null; ps -o pid,etime,cmd -C bash | grep -E "greffe|toutes"
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; awk '{print $2}' work/portes-1107-15h11/registre.txt 2>/dev/null | sort | uniq -c; tail -2 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check gate counts"}`

  ```
15:47:13 local
     26 0
porte-fusion 0 8
porte-gain 0 241
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 600000}`

  ```
porte-greffe           ✅                         736 s    ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE
  porte-harnais-invariants ✅                         118 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
[status: running]
  ```

- **bash** `{"command": "ls -lt work/portes-1107-15h11/*.log | head -3; tail -3 work/portes-1107-15h11/porte-homeostasie.log 2>/dev/null; ps -o pid,etime,cmd -C bash | grep -E \"homeostasie|toutes\"", "description": "Check homeostasie gate"}`

  ```
-rw-r--r--. 1 stephane stephane  437  7 nov 15:55 work/portes-1107-15h11/porte-homeostasie.log
-rw-r--r--. 1 stephane stephane 1374  7 nov 15:50 work/portes-1107-15h11/porte-harnais-invariants.log
-rw-r--r--. 1 stephane stephane 2073  7 nov 15:48 work/portes-1107-15h11/porte-greffe.log
  (×0 : GGUF réécrit — l'export re-quantifie, la comparaison porte sur la mesure)
  ✅ 1. ×0 rend le modèle de départ (norme 72.1293 contre 72.1312, écart 2.6e-05 = la re-quantification de l'export)
  ✅ 2. l'activité croît avec l'amplitude : 72.1312 ≤ 73.1445 ≤ 73.1923
 820703       46:06 bash tools/toutes-les-portes.sh
 993528       06:25 bash tools/porte-homeostasie.sh
1045167       00:09 bash tools/porte-homeostasie.sh
1046659       00:00 bash -c ls -lt work/portes-1107-15h11/*.log | head -3; tail -3 work/portes-1107-15h11/porte-homeostasie.log 2>/dev/null; ps -o pid,etime,cmd -C bash | grep -E "homeostasie|toutes"
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8; echo \"revue=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py | tail -2; python3 tools/verifie_journal.py | tail -2", "description": "Re-run doc checks"}`

  ```
revue de documentation · 711 fiche(s) · 804 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  en-cours · 1629 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  journal · 44 jour(s) · 171 session(s) · 2365 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "ls -lt journal/sessions | head -5; find journal/sessions -maxdepth 2 -type f -newermt '2026-11-07 15:00' | head -10", "description": "Check new session files"}`

  ```
total 20
drwxr-xr-x. 1 stephane stephane    80  7 nov 15:18 session-932afd57-1363-4133-b6f1-64f7d937f38d
-rw-r--r--. 1 stephane stephane 13042  7 nov 15:17 MANIFEST.md
drwxr-xr-x. 1 stephane stephane    80  7 nov 14:57 session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89
drwxr-xr-x. 1 stephane stephane    80  7 nov 14:57 session-9cb32ff9-6fb5-489f-a41e-0e2df9aeb32f
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md
journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/rapport.md
journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/digest.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
journal/sessions/e7dfe34f-d596-4f98-93c2-cad5a92d3b1e/rapport.md
journal/sessions/e7dfe34f-d596-4f98-93c2-cad5a92d3b1e/digest.md
journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/digest.md
journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md
[stderr]
ls: write error: Broken pipe
find: ‘standard output’: Broken pipe
find: write error
  ```

- **bash** `{"command": "ls -la journal/sessions/session-932afd57-1363-4133-b6f1-64f7d937f38d; echo ---; sed -n '1,60p' journal/sessions/session-932afd57-1363-4133-b6f1-64f7d937f38d/rapport.md 2>/dev/null", "description": "Inspect current session journal"}`

  ```
total 1180
drwxr-xr-x. 1 stephane stephane     80  7 nov 15:18 .
drwxr-xr-x. 1 stephane stephane  12488  7 nov 15:17 ..
-rw-r--r--. 1 stephane stephane 222394  7 nov 15:17 digest.md
-rw-r--r--. 1 stephane stephane  21584  7 nov 15:18 rapport.md
-rw-------. 1 stephane stephane 957354  7 nov 15:17 session.v4.jsonl.zstd
---
# Session session- — Corpus commun J2.2 : échantillon normalisé

> **Journaux :** [le jour](../../2026-11-07/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-932afd57-1363-4133-b6f1-64f7d937f38d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-07 14:59 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 211 |
| Appels d'outils | 266 |
| Fichiers touchés | 5 |
| Commandes | 214 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J2.2 : le corpus commun — choisir un échantillon (10-50 textes) présent des deux côtés (Panini/NIPADA et Drave), le normaliser (UTF-8, une phrase par ligne, métadonnées langue/époque), l'écrire dans `work/corpus-commun/` (non versionné) + une fi
… [1537 caractères tronqués]
  ```

- **bash** `{"command": "git status --short -- journal/sessions/session-932afd57-1363-4133-b6f1-64f7d937f38d journal/sessions/MANIFEST.md | head", "description": "Check session journal tracking"}`

  ```
M journal/sessions/MANIFEST.md
?? journal/sessions/session-932afd57-1363-4133-b6f1-64f7d937f38d/
  ```

- **bash** `{"command": "sed -n '1,80p' journal/sessions/README.md; echo ---; git diff --stat -- journal/sessions/MANIFEST.md; git diff -- journal/sessions/MANIFEST.md | head -40", "description": "Inspect sessions README and manifest diff"}`

  ```
# Sessions — plans vivants et archives

Deux choses différentes vivent ici :

- **`<id>/plan.md`** — le **mandat vivant** d'une session active : périmètre, fichiers réservés,
  heartbeat, prochaine action, état. Il s'écrit **avant** de modifier `docs/pilotage/en-cours.md`
  et se consulte avec `python3 tools/sessions.py --status`.
- **`<id>/rapport.md`** et **`<id>/digest.md`** — l'**archive** d'une session terminée, générée
  par `tools/session_report.py` / `tools/archive_sessions.py` ; les deux outils lisent
  `session.jsonl.zstd` **et** `session.v4.jsonl.zstd` (les traces récentes).
- **`<id>/cloture.md`** — la **clôture écrite à la main** quand le rapport automatique ne dit pas
  ce qui est livré et ce qui reste (`c3d0f0bd`, `f0969e87`) ; `N2-GPU` n'a pas de trace DSH et son
  rapport est écrit à la main.

Un plan n'est pas un état : `en-cours` reste la seule source de l'état. Un plan périmé (heartbeat
> 45 min) est signalé ; une session qui reprend un périmètre périmé le rafraîchit d'abord.

Modèle : [`_modele/plan.md`](_modele/plan.md). Vérification : `python3 tools/sessions.py --check`.

Migration douce : `python3 tools/sessions.py --depuis-en-cours` crée, pour chaque sessio
… [2208 caractères tronqués]
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; awk '{print $2}' work/portes-1107-15h11/registre.txt 2>/dev/null | sort | uniq -c; tail -2 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check gate counts"}`

  ```
15:57:41 local
     28 0
porte-greffe 0 736
porte-harnais-invariants 0 118
  ```

- **bash** `{"command": "tail -4 work/portes-1107-15h11/porte-homeostasie.log 2>/dev/null; ps -o pid,etime,cmd -C bash | grep -E \"homeostasie|toutes\"", "description": "Check homeostasie progress"}`

  ```
porte de l'homéostasie (E9) — LoRA rang 4, amplitudes ×0 / ×0,6 / ×1,0
  (×0 : GGUF réécrit — l'export re-quantifie, la comparaison porte sur la mesure)
  ✅ 1. ×0 rend le modèle de départ (norme 72.1293 contre 72.1312, écart 2.6e-05 = la re-quantification de l'export)
  ✅ 2. l'activité croît avec l'amplitude : 72.1312 ≤ 73.1445 ≤ 73.1923
 820703       46:32 bash tools/toutes-les-portes.sh
 993528       06:51 bash tools/porte-homeostasie.sh
1045167       00:35 bash tools/porte-homeostasie.sh
1050843       00:00 bash -c tail -4 work/portes-1107-15h11/porte-homeostasie.log 2>/dev/null; ps -o pid,etime,cmd -C bash | grep -E "homeostasie|toutes"
  ```

- **bash** `{"command": "sed -n '44,54p' docs/pilotage/references-non-regression.md", "description": "Read reference table row"}`

  ```
## 1. Ce qui se vérifie en une commande

| quoi | commande | attendu |
|---|---|---|
| tests unitaires | `cargo test --release` (dans `drave-core/`) | **138 tests** (le compte est dans la sortie) |
| toutes les portes | `tools/toutes-les-portes.sh` | **83 portes** ; dernière passe **79 vertes, 4 rouges** (04/11 23 h 43 → 05/11 02 h 12, machine au repos) : 2 connues (`indice`, `melange`), 1 **corrigée** (`lecteur`, ancre du banc), 1 de **coordination** (`sessions`, heartbeat de `e181ce02`) · ⚠ **ne jamais lire une porte à travers un `tail`** |
| une porte | `tools/porte-<nom>.sh` | la dernière ligne dit ce qu'elle verrouille |

> **16/10 — l'audit des 46 portes** (deux vrais défauts corrigés, des faux positifs
> documentés) : le récit et les tableaux sont dans
> [`historique-passes-portes.md`](../../reports/historique-passes-portes.md).
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md", "offset": 48, "limit": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md</path>
<type>file</type>
<content>
48: | tests unitaires | `cargo test --release` (dans `drave-core/`) | **138 tests** (le compte est dans la sortie) |

(Showing lines 48-48 of 161. Use offset=49 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md", "offset": 49, "limit": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md</path>
<type>file</type>
<content>
49: | toutes les portes | `tools/toutes-les-portes.sh` | **83 portes** ; dernière passe **79 vertes, 4 rouges** (04/11 23 h 43 → 05/11 02 h 12, machine au repos) : 2 connues (`indice`, `melange`), 1 **corrigée** (`lecteur`, ancre du banc), 1 de **coordination** (`sessions`, heartbeat de `e181ce02`) · ⚠ **ne jamais lire une porte à travers un `tail`** |

(Showing lines 49-49 of 161. Use offset=50 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md", "old_string": "| toutes les portes | `tools/toutes-les-portes.sh` | **83 portes** ; dernière passe **79 vertes, 4 rouges** (04/11 23 h 43 → 05/11 02 h 12, machine au repos) : 2 connues (`indic … [353 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md has been updated successfully.
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; awk '{print $2}' work/portes-1107-15h11/registre.txt 2>/dev/null | sort | uniq -c; tail -2 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check gate counts"}`

  ```
15:57:59 local
     28 0
porte-greffe 0 736
porte-harnais-invariants 0 118
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"references-non-regression|T0 max|violation\"; echo done", "description": "Check reference budget"}`

  ```
2404    162   T1   2500  docs/pilotage/references-non-regression.md
  T0 max : 3999 mots (budget 4 000)
done
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 300000}`

  ```
porte-homeostasie      ✅                         591 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          28 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
[status: running]
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 600000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ls -lt work/portes-1107-15h11/*.log | head -3; tail -3 work/portes-1107-15h11/porte-indice.log 2>/dev/null; ps -o pid,etime,cmd -C bash | grep -E \"indice|toutes\"", "description": "Check indice gate progress"}`

  ```
-rw-r--r--. 1 stephane stephane  594  7 nov 16:05 work/portes-1107-15h11/porte-indice.log
-rw-r--r--. 1 stephane stephane  769  7 nov 16:01 work/portes-1107-15h11/porte-horloge.log
-rw-r--r--. 1 stephane stephane  599  7 nov 16:00 work/portes-1107-15h11/porte-homeostasie.log
    capture d'état    : position(s) [1439] écrite(s) dans /tmp/tmp.bvhjutrCeK/etatB.*
    capture d'état    : position(s) [1469] écrite(s) dans /tmp/tmp.bvhjutrCeK/etatA.*
=== 3. la mémoire interroge A, avec puis sans l'indice extérieur ===
 820703    01:01:59 bash tools/toutes-les-portes.sh
1082547       11:59 bash tools/porte-indice.sh
1121985       00:00 bash -c ls -lt work/portes-1107-15h11/*.log | head -3; tail -3 work/portes-1107-15h11/porte-indice.log 2>/dev/null; ps -o pid,etime,cmd -C bash | grep -E "indice|toutes"
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 600000}`

  ```
porte-indice           ❌ code 1                 1060 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
  porte-jeux             ✅                         123 s    ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision,
  porte-jumeaux          ✅                          31 s  PORTE TENUE : l'échange est exact, il ne crée pas de gain entre jumeaux identiques, il
  porte-lecteur          ✅                           1 s  ✅ porte lecteur verte
  porte-lecture          ✅                           1 s  ✅ porte lecture verte
  porte-m5-brouillon     ✅                           0 s    ✅ brouillon déclaré (cibles [37,38,39]) et porté : 75 tenseurs, 41 263 M poids
[status: running]
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 300000}`

  ```
porte-melange          ❌ code 1                  127 s    ❌ l'état de A ne rend pas le code de A dans une
  porte-memoire          ✅                          10 s  PORTE TENUE : la mémoire retient les K derniers signaux HORS du réseau, exactement, sans
  porte-miroir-blocs     ✅                           9 s  ✅ porte miroir verte
  porte-mistral          ✅                          10 s      ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= p
  porte-n3-cache         ✅                           7 s  PORTE TENUE : saut de calcul mesuré · sortie changée · condition K/V nommée
  porte-n3-composition   ✅                           7 s  PORTE TENUE : service + profondeur + routage + comptage composés sur les mêmes modèles
  porte-n3-deux-processus ✅                           5 s  PORTE TENUE : deux processus · fichier de frontière · logits identiques au pas plein
  porte-n3-deux-regions  ✅                           5 s  PORTE TENUE : découpage 0..k / k..n bit-exact · pont des deux côtés · prompt différent
  porte-n3-generation    ✅                           9 s  PORTE TENUE : génération répartie · deux caches · sortie bit-identique
  porte-n3-inven
… [2112 caractères tronqués]
  ```

- **bash** `{"command": "tail -40 work/portes-1107-15h11/porte-occupation-moteur.log; echo ---; sed -n '1,120p' tools/porte-occupation-moteur.sh", "description": "Inspect occupation gate failure"}`

  ```
frame #4: c10::ApproximateClockToUnixTimeConverter::measurePairs() + 0x27 (0x7f6eb796a327 in /home/stephane/gpu-env/lib64/python3.13/site-packages/torch/lib/libc10.so)
frame #5: c10::ApproximateClockToUnixTimeConverter::ApproximateClockToUnixTimeConverter() + 0xc (0x7f6eb796a34c in /home/stephane/gpu-env/lib64/python3.13/site-packages/torch/lib/libc10.so)
frame #6: <unknown function> + 0x2b9df (0x7f6eb9e6b9df in /home/stephane/gpu-env/lib64/python3.13/site-packages/torch/lib/libc10_cuda.so)
frame #7: <unknown function> + 0xd940 (0x7f6eb9e4d940 in /home/stephane/gpu-env/lib64/python3.13/site-packages/torch/lib/libc10_cuda.so)
frame #8: <unknown function> + 0x655e (0x7f6f2189355e in /lib64/ld-linux-x86-64.so.2)
frame #9: <unknown function> + 0x666c (0x7f6f2189366c in /lib64/ld-linux-x86-64.so.2)
frame #10: _dl_catch_exception + 0x11b (0x7f6f2188f5f9 in /lib64/ld-linux-x86-64.so.2)
frame #11: <unknown function> + 0xda20 (0x7f6f2189aa20 in /lib64/ld-linux-x86-64.so.2)
frame #12: _dl_catch_exception + 0x89 (0x7f6f2188f567 in /lib64/ld-linux-x86-64.so.2)
frame #13: <unknown function> + 0xdf34 (0x7f6f2189af34 in /lib64/ld-linux-x86-64.so.2)
frame #14: <unknown function> + 0x9a66c (0x7f6f2
… [7153 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"occupation\" docs/pilotage/references-non-regression.md | head -20; echo ---; grep -n \"occupation-moteur\" docs/pilotage/references-non-regression.md reports/*.md 2>/dev/null | head -20", "description": "Check occupation gate in references"}`

  ```
63:| `porte-audit-drapeaux.sh` | 167 s | ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun |
120:| `porte-occupation-elagage.sh` | 60 s | ✅ porte occupation × élagage : la cible annoncée est VÉRIFIÉE dans le fichier exporté |
121:| `porte-occupation-moteur.sh` | 53 s | ✅ porte occupation du moteur : la ligne « occupation des poids » est annoncée, elle COLLE à |
---
docs/pilotage/references-non-regression.md:121:| `porte-occupation-moteur.sh` | 53 s | ✅ porte occupation du moteur : la ligne « occupation des poids » est annoncée, elle COLLE à |
reports/historique-passes-portes.md:273:> `porte-harnais-invariants`, `porte-audit-drapeaux`, `porte-occupation-moteur`,
reports/rapport-a80-audit-final.md:24:| sans PPL | `diff-couche`, `echange-experts`, `harnais-invariants`, `jumeaux`, `mistral`, `occupation-moteur`, `prechargement`, `push-paresseux` | aucune PPL à épingler |
  ```

- **bash** `{"command": "head -40 work/portes-1107-15h11/porte-occupation-moteur.log", "description": "Inspect occupation gate start"}`

  ```
terminate called after throwing an instance of 'c10::Error'
  what():  fast_1 >= fast_0 INTERNAL ASSERT FAILED at "/pytorch/c10/util/ApproximateClock.cpp":17, please report a bug to PyTorch. getCount is non-monotonic.
Exception raised from measurePair at /pytorch/c10/util/ApproximateClock.cpp:17 (most recent call first):
frame #0: c10::Error::Error(c10::SourceLocation, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >) + 0x9d (0x7f6eb797305d in /home/stephane/gpu-env/lib64/python3.13/site-packages/torch/lib/libc10.so)
frame #1: c10::detail::torchCheckFail(char const*, char const*, unsigned int, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) + 0xc3 (0x7f6eb79076fd in /home/stephane/gpu-env/lib64/python3.13/site-packages/torch/lib/libc10.so)
frame #2: c10::detail::torchInternalAssertFail(char const*, char const*, unsigned int, char const*, char const*) + 0x42 (0x7f6eb796f6a2 in /home/stephane/gpu-env/lib64/python3.13/site-packages/torch/lib/libc10.so)
frame #3: <unknown function> + 0x952fe (0x7f6eb796a2fe in /home/stephane/gpu-env/lib64/python3.13/site-packages/torch/lib/libc10.so)
frame #4: c10::ApproximateClockT
… [2286 caractères tronqués]
  ```

- **bash** `{"command": "date '+%H:%M:%S local'; awk '{print $2}' work/portes-1107-15h11/registre.txt 2>/dev/null | sort | uniq -c; tail -3 work/portes-1107-15h11/registre.txt 2>/dev/null", "description": "Check gate counts"}`

  ```
16:28:34 local
     57 0
      3 1
porte-n3-sparsite 0 5
porte-occupation-elagage 0 62
porte-occupation-moteur 1 62
  ```

- **job_output** `{"job_id": "bash-120", "wait": true, "timeout_ms": 600000}`
