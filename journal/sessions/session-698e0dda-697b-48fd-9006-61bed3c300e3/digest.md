# Session DSH — relecture

- identifiant : `session-698e0dda-697b-48fd-9006-61bed3c300e3`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 22:16:36
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche T3 (exploitable, 3/5) : **le quickstart** — écris `docs/produit/demarrage.md` (le clone, l'install T1, les 3 commandes, la sortie attendue, le JSON, le tagger optionnel, les 3 erreurs courantes et leur code) ; vérifie **chaque commande** en la rejouant (le texte et la sortie réels) ; ajoute le lien dans `docs/produit/README.md` et `docs/README.md` ; le **contrôle négatif** : un débutant sans le dépôt doit pouvoir suivre les 5 minutes. Fiche `reports/rapport-quickstart.md` + JSON, commit.

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

- **bash** `{"command": "pwd && ls && echo \"---\" && ls docs/produit/ 2>/dev/null && echo \"---\" && ls reports/ | head -30", "description": "List repository root and docs/produit"}`

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
---
exemples.md
README.md
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
[stderr]
ls: write error: Broken pipe
  ```

- **bash** `{"command": "cat docs/produit/README.md 2>/dev/null; echo \"===DOCS README===\"; cat docs/README.md 2>/dev/null | head -100", "description": "Read product and docs READMEs"}`

  ```
attachement 238/239), le
**gelé 602** (0,7882, 234/239) et le **réel 452** (`--reel` : POS **0,8891**, F1 **0,7906**,
attachement 99,46 %). Les chiffres de la fiche v12 (0,6511/0,6482, 235/236) sont **datés** : ils
mesuraient le bloc avant la semaine du 07/11. Toujours lire la base avec le chiffre.

## 3. Comment l'utiliser — cinq exemples réels

Tout se lance **depuis la racine du dépôt**. Les commandes ci-dessous sont celles d'aujourd'hui ;
elles n'utilisent ni modèle, ni GPU, ni réseau. Les JSON complets et commentés sont dans
[`exemples.md`](exemples.md).

### 3.1 Analyser une phrase

```bash
python3 tools/drave.py analyser "Le chat dort."
```
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
            phrase=0.85 · discours=0.50 · pragmati
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"T3\\|T1\\|quickstart\\|démarrage\\|demarrage\" docs/pilotage/ docs/produit/ reports/ 2>/dev/null | head -60", "description": "Find T1/T3 task references"}`

  ```
docs/pilotage/chantiers.md:90:| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **porte** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **professeur** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + **votante** + **trois looks** + **bayésien** + **bayésien 2** + **vraisemblance** + **dérive** + **adaptative** + **glisse** + **rupture** + **alternance** + **chaotique** + **fréquent** + **rapide** + **limite** + **hasard 2** + **intra** + **asym** + **rare** + **très rare** + **ultra-rare** + **un look** + **look tardif** + **oubli** + **oubli fort** + **oubli total** + **seuil** + **seuil fin*
… [20392 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' docs/pilotage/en-cours.md", "description": "Read current state"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 22 h 03 HNE (T2 : l'API du JSON)**

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
> le hook pre-commit refuse un fait s
… [11217 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"T1\\b\" journal/sessions/ work/ docs/ 2>/dev/null | grep -i \"install\\|produit\\|quick\\|doc\\|paquet\\|demarr\" | head -40", "description": "Find T1 install task context"}`

  ```
journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/rapport.md:128:- **T1** Inspect exact bytes of the doc line
journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/rapport.md:129:- **T1** Fix the bpe doc comment
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:10981:- **T1** : a8f2635f8 docs: record which models this box is good at, and why src/llama-hparams.cpp:8:void llama_hparams::set_swa_pattern(uint32_t n_pattern, bool dense_first) { src/llama-hparams.h:308:    void se
journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:92:- **T1** Cherche références aux traces dans la doc
journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:118:- **T1** `docs/convertisseur.md:20:| mémoire crête (fichier 353 Mo) | ~700 Mo | **413 Mo** |`
journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:119:- **T1** `docs/format-flux.md:33:actif**, et 505 ko par jeton sur une exécution dense (deux listes par couche).`
journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:120:- **T1** `docs/format-flux.md:97:| la taille suit l'activité | densité ÷2,3 → trace ÷2,5 (132 Mo → 53 Mo) |`
journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rappo
… [6443 caractères tronqués]
  ```

- **bash** `{"command": "ls -lt journal/sessions/ | head -10; echo ---; ls -lt work/ | head -20; echo ---; git log --oneline -15", "description": "Recent sessions and commits"}`

  ```
total 24
-rw-r--r--. 1 stephane stephane 16589 15 nov 22:13 MANIFEST.md
drwxr-xr-x. 1 stephane stephane    80 15 nov 21:56 session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f
drwxr-xr-x. 1 stephane stephane    80 15 nov 21:56 session-8217267f-fd89-462c-8112-cba3ba9877b3
drwxr-xr-x. 1 stephane stephane    80 15 nov 14:18 session-ed9b8942-25a3-48ee-9f86-f6821e56df9d
drwxr-xr-x. 1 stephane stephane    94 15 nov 13:18 e181ce02-cd50-488a-a6be-e84b79d40dcc
drwxr-xr-x. 1 stephane stephane    80 15 nov 13:05 session-c6d0e659-7d2e-4d23-a2b4-d50387bb6f61
drwxr-xr-x. 1 stephane stephane    80 15 nov 13:05 session-7fc0675a-4f7b-470d-8dd7-bedcaf3bcd6e
drwxr-xr-x. 1 stephane stephane    80 15 nov 12:37 session-e3fa8f1c-e304-4a0b-922a-79e5a1a580e5
drwxr-xr-x. 1 stephane stephane    80 15 nov 12:34 session-f71c99b5-4cd1-41cd-81b4-87e7e7c8bfeb
---
total 240
drwxr-xr-x. 1 stephane stephane   290 15 nov 21:37 chantier
drwxr-xr-x. 1 stephane stephane   178 15 nov 13:34 tagger-lot
drwxr-xr-x. 1 stephane stephane  3538 15 nov 13:18 portes-w5
drwxr-xr-x. 1 stephane stephane    20 15 nov 12:35 page-s-mesure
drwxr-xr-x. 1 stephane stephane   584 15 nov 12:23 portes
-rw-r--r--. 1 stephane stephane  1790 15 nov 12:
… [2828 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat 7f1519f7 | head -50; echo ===; git show --stat 71fdf72c | head -40", "description": "Inspect T1-T2 and plan commits"}`

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
… [2818 caractères tronqués]
  ```

- **bash** `{"command": "git show 71fdf72c --name-only | head -40; echo ===; grep -rln \"51 tâches\\|51 taches\\|T3 \" journal/ docs/ work/ 2>/dev/null | head -20", "description": "Find plan file"}`

  ```
commit 71fdf72c895fdf5298c7aa91d52b6058b9c154ff
Author: Stéphane <stephane@localhost>
Date:   Sun Nov 15 15:05:10 2026 -0500

    CLÔTURE — LE PLAN (51 TÂCHES) ET LE PROTOCOLE OR-ROLES (X2) COMMITTÉS ; L'ÉTAT HORODATÉ

docs/pilotage/en-cours.md
journal/2026-11-15/README.md
journal/2026-11-15/distribue.md
journal/2026-11-15/docs.md
journal/2026-11-15/memoire.md
journal/2026-11-15/mesures.md
journal/2026-11-15/modele.md
journal/2026-11-15/outils.md
journal/2026-11-15/portes.md
journal/README.md
journal/sessions/MANIFEST.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
tools/chantier/plan.json
tools/protocole_or_roles.py
===
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/session.jsonl.zstd
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
journal/sessions/c25f97d1-9a4d-41da-b983-004f793afe43/rapport.md
journal/sessions/c25f97d1-9a4d-41da-b983-004f793afe43/digest.md
journal/sessions/c776b71f-525a-4bad-b83c-eff1c2d204ff/session.jsonl.zstd
journal/sessions/5c1bbea7-1d14-47b6-a48c-fea15f2b857e/session.jsonl.zstd
journal/sessions/8734fc13-aeb8-4cdf-b005-c182f77be0dc/digest.md
journal/ses
… [878 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(type(p))\nprint(json.dumps(p, ensure_ascii=False, indent=1)[:4000])\nEOF", "description": "Read plan JSON"}`

  ```
<class 'dict'>
{
 "nom": "Semaine 07/11 → 14/11 — le produit et l'intégration Panini",
 "principe": "Une tâche n'est finie que si son acceptation passe ; l'agent commite, le superviseur vérifie.",
 "taches": [
  {
   "id": "J0",
   "jour": 0,
   "titre": "Le contrôle du superviseur",
   "mandat": "Réponds exactement le mot OK, sans autre texte. C'est un test de liaison du superviseur.",
   "budget_min": 2,
   "acceptation": [
    {
     "commande": "python3 -c \"print('LIAISON-OK')\"",
     "attendu": "LIAISON-OK"
    }
   ]
  },
  {
   "id": "J1.1",
   "jour": 1,
   "titre": "r035 : la relative zéro",
   "mandat": "Tâche J1.1 du chantier : la relative zéro (r035, « The film she talks about is out. »). Reproduis, explique, propose UNE règle générale mesurée sur dev/test ; si elle tient (attachement 236→237, POS/F1 stables), intègre-la et commite avec une fiche `reports/rapport-r035.md` + `reports/pensee-r035.json`. Sinon, écris la fiche du rejet (chiffres, raison) et commite-la. Règles : ne touche pas S/D/N2 ; 183/183 portes ; en-cours à jour.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-r035.md && echo FICHE-OK",
     "attendu": "FICHE
… [2815 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"T3\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md journal/sessions/*/digest.md 2>/dev/null | grep -i \"quick\\|start\\|produit\\|install\\|doc\" | tail -20; echo ===; grep -rn \"3/5\\|T1–T5\\|T1-T5\\|T1 —\\|T2 —\\|T3 —\" journal/ docs/ reports/ 2>/dev/null  … [60 caractères tronqués]`

  ```
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:12121:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib,re\np=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text()\nt=re.sub(r\"\\(T0 canonique, T1 rejeu,\\n  T2 stratégies, T3 anytime, T4 justification\\)\", \"\", t)\nt=t.replace(\"6 bis) ~~opérateu … [677 caractères tronqués]`
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:66193:| **T3** le démarrage | `docs/produit/demarrage.md` en 5 minutes, chaque commande rejouée | un débutant suit sans le dépôt |
journal/sessions/206a4022-ab3c-497d-a5fa-0194931c7fa0/digest.md:1106:01_DOC chars 210 octets 219 debut 'D 23/7\n\n“T3 |\n| Ÿ x | ¥\n"4\nx x\ny\nVA\na x\n4\n| (Va |\n' fin 'paogé clou\n\nMSe ant Metric te pew Lo Tales\nthe CORONA Ww. fe'
journal/sessions/206a4022-ab3c-497d-a5fa-0194931c7fa0/digest.md:1108:03_DOC chars 210 octets 219 debut 'D 23/7\n\n“T3 |\n| Ÿ x | ¥\n"4\nx x\ny\nVA\na x\n4\n| (Va |\n' fin 'paogé clou\n\nMSe ant Metric te pew Lo Tales\nthe CORONA Ww. fe'
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:4181:**Diagnostic définitif** : cette tour n'a que deux
… [13513 caractères tronqués]
  ```

- **bash** `{"command": "git log --all --oneline --grep=\"T3\" | head -20; echo ===; git status --short | head -40", "description": "Search git log and status"}`

  ```
a20de579 PENSÉE v0 — LE STATE STORE EXISTE ET TIENT SES SIX PORTES
481083ee PENSÉE v0 — LE STATE STORE EXISTE ET TIENT SES SIX PORTES
53b03dae B4.6 — LE LORA CALCULE EN FLOAT32 : en float16 la perte partait en NaN (sous-debordement du produit x@A.T). A et B sont en float32, le forward fait x.float() et rend le resultat au dtype d'entree. Le modele reste en float16, le LoRA calcule en float32
===
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
  ```

- **bash** `{"command": "sed -n '66150,66230p' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md", "description": "Read T1-T5 plan table in digest"}`

  ```
| **l'empaquetage** | pas de `pip install`, pas de commande `drave` dans le `PATH` ; tout part de la racine du dépôt |
| **le neuronal local** | la cascade 7B (0,9415) exige un serveur local interdit par la règle 11 ; le tagger **API** est en option, le 7B local n'est 
| **la restitution sémantique** | `restituer` est un **codec de surface** (graphème) ; il ne restitue pas le sens, ne traduit pas, ne génère pas |

**Ce qui est déjà tenu** : `--version`, `--aide`, les **quatre** sous-commandes, le JSON
déterministe, l
… [1150 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path('tools/chantier/plan.json'); d=json.loads(p.read_text())\ndef t(id, jour, titre, mandat, checks, budget=90):\n    return {\"id\": id, \"jour\": jour, \"titre\": titre, \"mandat\" … [5863 caractères tronqués]`

  ```
plan : 57 tâches
phase exploitable
PID 1028271
2026-11-15 21:37:27 · ▶ T1 — L'empaquetage — pip install et la commande drave (timeout 3600 s)
dim 15 nov 2026 21:37:46 EST
  ```

### 🤖 Assistant

⏵ La nuit « exploitable » est lancée (T1 : l'empaquetage). Voici le résumé du reste à faire

## 
… [4921 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if str(t['id']).startswith('T'):\n        print(json.dumps(t, ensure_ascii=False, indent=2))\nEOF", "description": "Show T tasks with acceptance"}`

  ```
{
  "id": "T1",
  "jour": 19,
  "titre": "L'empaquetage — pip install et la commande drave",
  "mandat": "Tâche T1 (exploitable, 1/5) : **l'empaquetage** — écris un **`pyproject.toml`** minimal (le nom `drave`, la version 0.1.0, le `requires-python >= 3.10`, **aucune dépendance**, le `console_scripts` `drave = tools.drave:main` ou un module d'entrée propre), vérifie `python3 -m pip install -e .` dans un **venv temporaire** (`/tmp/venv-drave`), puis `drave --version` et `drave analyser \"Le chat dort.\"` depuis un **autre répertoire** (pas la racine du dépôt) ; le contrôle négatif : sans install, `drave` doit échouer proprement. Fiche `reports/rapport-empaquetage.md` + JSON, un test dans `tools/tests/` (ou une note), et la doc `docs/produit/README.md` § 8.10 mise à jour (l'install). **Ne casse pas** `python3 tools/drave.py` (le chemin historique).",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f pyproject.toml && echo PYPROJECT-OK",
      "attendu": "PYPROJECT-OK"
    },
    {
      "commande": "test -f reports/rapport-empaquetage.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    }
  ]
}
{
  "id": "T2",
  "jour": 19,
  "titre": "Le contrat — les candidat
… [4267 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-empaquetage.md; echo ===JSON===; cat reports/empaquetage.json | head -80", "description": "Read T1 report and JSON"}`

  ```
# T1 — l'empaquetage : `pip install -e .`, `drave` hors du dépôt, chemin historique intact

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T1** (exploitable, 1/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **empaquetage minimal livré**.
>
> **Le chiffre.** `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,
> **0** dépendance d'exécution, script console `drave = tools.drave:main`.
> `python3 -m pip install -e .` dans **`/tmp/venv-drave`** (Python **3.13.16**, pip **26.2.1**)
> rend **0** et `Successfully installed drave-0.1.0` ; `drave --version` rend **`drave 0.1.0`**
> et `drave analyser "Le chat dort."` rend **0** depuis **`/tmp`**. Le **contrôle négatif** —
> le même nom sans installation — échoue **proprement** : code **127**, `command not found`,
> **aucune** trace Python. Le chemin historique `python3 tools/drave.py` reste **vert**.
>
> **Dispositif** : [`pyproject.toml`](../pyproject.toml),
> [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py),
> [`reports/empaquetage.json`](empaquetage.json),
> [`docs/produit/README.md`](../docs/produit/README.md) § 8.10.

## 1. Ce qui est livré

Le paquet est **minimal** et sans
… [7266 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' docs/methode/resultats.md", "description": "Read result method"}`

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

- **bash** `{"command": "sed -n '120,240p' reports/rapport-empaquetage.md; echo ===; sed -n '1,60p' docs/produit/README.md", "description": "Read T1 negative control and product intro"}`

  ```
Le contrôle négatif est le **même nom de commande, sans l'installation**. On vide le `PATH` et
on retire `PYTHONPATH` / `VIRTUAL_ENV`, puis on lance depuis `/tmp` :

```bash
env -i PATH=/usr/bin:/bin HOME=/tmp bash -c 'drave --version'
# code 127
# stdout : (vide)
# stderr : bash: line 1: drave: command not found
```

**Lecture.** L'échec est **propre** : c'est un échec de **résolution** (127), pas une trace
Python, pas un import partiel, pas un code 0 trompeur. Si `drave` restait résolu sans
installation, le test positif ne prouverait rien ; ici, le contraste est net.

## 5. Le test

```bash
python3 tools/tests/test_empaquetage.py
# Ran 8 tests in 0.5 s
# OK
```

Le test fige **huit** points :

1. `pyproject.toml` existe ;
2. nom `drave`, version `0.1.0`, `requires-python >= 3.10` ;
3. aucune dépendance d'exécution, backend `setuptools.build_meta` ;
4. script console `drave = tools.drave:main` ;
5. `python3 tools/drave.py --version` → `drave 0.1.0` ;
6. `python3 tools/drave.py analyser "Le chat dort."` → `0`, avec `GN` et `Le chat` ;
7. `from tools.drave import main` depuis un **autre** répertoire ;
8. sans installation, `drave` échoue **proprement** (127, `command not found`, pas
… [5731 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"8.10\\|Comment l'installer\\|Où aller ensuite\\|^## \\|^### \" docs/produit/README.md | tail -40", "description": "Find product README sections"}`

  ```
29:## Sommaire
39:- [9. Où aller ensuite](#9-où-aller-ensuite)
41:## 1. À qui s'adresse le produit
57:## 2. Ce que le produit fait
95:## 3. Comment l'utiliser — cinq exemples réels
101:### 3.1 Analyser une phrase
124:### 3.2 Analyser en JSON et lire l'attachement
161:### 3.3 Mesurer sur le gold
217:### 3.3 quater Traiter un corpus
227:### 3.3 bis La vue des syntagmes qui se chevauchent — les champs du schéma v2
342:### 3.3 ter Le contexte (mémoire de discours)
351:### 3.4 Rejouer et vérifier le déterminisme
368:### 3.5 Le refus, et la langue inconnue
386:### 3.6 Restituer la surface (v0)
421:### 3.6 bis La base honnête — `--reel`
431:### 3.7 Le tagger en option — `--tagger`
559:## 4. Ce que le produit ne fait pas encore
643:## 5. Performance
665:## 6. Garanties
701:## 7. Le CLI livré — contrat et manques
791:## 8. FAQ — dix questions
801:### 8.1 Quelles langues le produit reconnaît-il ?
811:### 8.2 Est-ce que ça marche hors ligne ?
818:### 8.3 Combien ça coûte ?
827:### 8.4 Qu'est-ce que `--tagger` change ?
838:### 8.5 Quel est le format de sortie, et est-il stable ?
850:### 8.6 Que veut dire « attachement », et à quel point est-il fiable ?
863:### 8.7 Pourquoi reste-t-il un span i
… [228 caractères tronqués]
  ```

- **bash** `{"command": "python3 --version; cat pyproject.toml; echo ===; python3 tools/drave.py --version; echo \"exit=$?\"; echo ===; python3 tools/drave.py --aide | head -80", "description": "Check version and CLI help"}`

  ```
Python 3.13.16
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
packages = ["tools"]
===
drave 0.1.0
exit=0
===
usage: drave [-h] [-V] {analyser,evaluer,rejouer,restituer} ...

Point d'entrée produit du bloc linguistique (analyse et restitution).

arguments:
  {analyser,evaluer,rejouer,restituer}
    analyser            étiqueter un texte (POS, syntagmes, pragmatique)
    evaluer             mesurer l'heuristique sur le gold
    rejouer             analyser deux fois et vérifier le déterminisme
    restituer           reconstruire la surface depuis l'annotation et mesurer le miroir

options:
  -h, --help, --aide    afficher cette aide et quitter
  -V, --version         afficher la version et quitter

Commandes : analyser, evaluer, rejouer, restituer.
Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) ·
4 clé/tagger indisponible (absente ou refusée, seulement avec --tagger explicite) · 1 erreur.
Options : --json
… [822 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"exit\\|code\\|return [0-9]\\|SystemExit\\|refus\\|fichier\" tools/drave.py | head -80", "description": "Find exit code handling"}`

  ```
22:agent/prédicat/lieu lisibles). La restitution est un **codec de surface** : elle reconstruit
23:depuis le niveau `graphème`, pas un décodeur neuronal.
28:changer le code de sortie** (0 dans les deux cas, 3 pour un refus) ; `stderr` dit lequel a servi,
35:Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible
36:(absente ou refusée) · 1 erreur.
51:# déduits du fichier pour que la commande marche aussi depuis un autre répertoire. Aucun paquet
82:    return s.encode("utf-8", "replace").decode("utf-8", "replace")
103:    """L'API refuse la clé (HTTP 401/403) : ce n'est pas un refus de phrase, c'est un arrêt.
105:    Une clé absente et une clé refusée sont la même dépendance manquante du point de vue du
106:    produit : le code 4, un message qui nomme les trois sources de la clé, et rien sur `stdout`.
109:    def __init__(self, code: int) -> None:
110:        self.code = int(code)
112:            f"clé DeepSeek refusée (HTTP {self.code}) : vérifiez DEEPSEEK_KEY_FILE, "
178:    - **aucun code 4** : une clé refusée (401/403) ou un réseau coupé n'arrête pas le run ;
179:      l'analyse est rendue par l'heuristique, code 0, avec la cause dans `refus` ;
182:
… [3996 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '480,640p' tools/drave.py; echo ===MAIN===; sed -n '880,1040p' tools/drave.py", "description": "Read analyser and main"}`

  ```
lignes.append("PRAGMATIQUE —")

    couverture = a.couverture()
    if couverture:
        ordre = [n for n in bl.NIVEAUX if n in couverture]
        ordre += sorted(n for n in couverture if n not in bl.NIVEAUX)
        lignes.extend(_envelopper(
            "COUVERTURE  ",
            "(confiance max par niveau)  "
            + " · ".join(f"{n}={couverture[n]:.2f}" for n in ordre),
        ))
    if tagger and a.refus:
        lignes.extend(_envelopper("REFUS TAGGER  ", a.refus))
    if stats is not None:
        lignes.extend(_envelopper("TAGGER API  ", _ligne_tagger(stats)))
    return "\n".join(lignes)


# --------------------------------------------------------------------------- commandes


def _lire_entree(args: argparse.Namespace) -> str:
    """Le texte : l'argument, ou le **fichier** (`--fichier`)."""
    if getattr(args, "fichier", None):
        return pathlib.Path(args.fichier).read_text(encoding="utf-8", errors="replace")
    return args.texte or ""


def _analyser_jsonl(texte: str, args: argparse.Namespace, h: bl.Heuristique, bloc,
                    stats: dict | None = None, auto: _TaggerAuto | None = None) -> int:
    """Une **ligne JSON par phrase** (traitement
… [12876 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1040,1220p' tools/drave.py", "description": "Read main function"}`

  ```
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
        if jeton == "--tagger" and i + 1 < len(argv) and argv[i + 1] in ("auto", "api", "explicite"):
            valeur = argv[i + 1]
            sortie.append("--tagger-auto" if valeur == "auto" else "--tagger")
            i += 2
            continue
        if jeton.startswith("--tagger="):
            valeur = jeton.split("=", 1)[1]
            if valeur == "auto":
                sortie.append("--tagger-auto")
            elif valeur in ("api", "explicite"):
                sortie.append("--tagger")
            else:
                sortie.append(jeton)
        else:
            sortie.append(jeton)
        i += 1
    return sortie


def co
… [10052 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1220,1340p' tools/drave.py", "description": "Read end of main"}`

  ```
help="sortie JSON (restitution, miroir, contrôle négatif ; "
                                "rôles avec --roles)")
    restituer.set_defaults(fonction=cmd_restituer)
    return parseur


def main(argv: list[str] | None = None) -> int:
    # un stdout non-UTF-8 ne doit pas faire planter l'en-tête (« — ») : on tolère les remplacements
    try:
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
    except CleTaggerRefusee as exc:
        # même dépendance manquante qu'une clé absente : code 4, message clair, rien sur stdout
        print(f"{NOM}: dépendance absente :
… [290 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"quickstart\\|les 3 commandes\\|3 commandes\\|demarrage.md\\|démarrage\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | tail -20", "description": "Search plan details for quickstart"}`

  ```
51796:**Performance** (Xeon E5-2687W v3, Python 3.13.16) : heuristique **1,08 / 4,60 / 19,43 ms** à 10/50/200 mots (923/218/51,5 phrases/s), 0,09–0,11 ms/mot. Parallèle 1,51/6,18/27,22 ms ; cascade 1,51/6,25/29,64 ms (avec le mock). Mémoire : pic 540,6 Kio pour 200 mots / 1 061 étiquettes ; RSS 30,7 Mio, delta 0 après 100 analyses ; démarrage à froid 99–113 ms / 27,4 Mio. Au-delà de 200 mots, coût superlinéaire : 0,394 ms/mot à 4 000 (1,57 s), exposant ≈1,45 (`_cible_proche` : 199 302 appels à `_est_adverbe_seul`). Déterminisme : mêmes JSON sur même instance, instances fraîches et graines 0/1/42 ; `duree_s` exclue par défaut.
51950:- Mémoire : pic **540,6 Kio** pour 200 mots ; RSS **30,7 Mio**, **delta 0** après 100 analyses ; démarrage à froid **99–113 ms**.
52243:- **Temps CLI** : 136,8–226,6 ms, médiane **152,7 ms** (démarrage ~146 ms) ; **interne** : 0,2–45,1 ms, médiane **1,0 ms** ; f50 45,1 ms. **10 k** : 590–765 ms CLI, 331,6 ms interne, 2,76 Mo JSON ; **50 k** : 5,44 s, 11,5 Mo. `evaluer` 530–543 ms (vivant), 577–600 ms (`--gold`) ; `rejouer` 146–149 ms.
52266:**Ce qu'il confirme** : 50 phrases, **0 plantage sur le banc**, 50/50 déterminisme, spans valides, 11 clés racine s
… [3064 caractères tronqués]
  ```

- **bash** `{"command": "git remote -v; echo ===; ls -la ~/.config/drave/deepseek.key 2>/dev/null || echo \"pas de clé fichier\"; env | grep -i \"deepseek\\|DSH_KEY\" || echo \"pas de clé env\"", "description": "Check remote URL and key presence"}`

  ```
origin	git@github.com:stephanedenis/drave.git (fetch)
origin	git@github.com:stephanedenis/drave.git (push)
===
-rw-------. 1 stephane stephane 36  3 nov 11:15 /home/stephane/.config/drave/deepseek.key
pas de clé env
  ```

- **bash** `{"command": "timeout 20 git ls-remote https://github.com/stephanedenis/drave.git HEAD 2>&1 | head -5; echo \"https_exit=${PIPESTATUS[0]}\"", "description": "Check public HTTPS clone"}`

  ```
7f1519f749ab0939ad24b642abe785e7ab0aa87a	HEAD
https_exit=0
  ```

- **bash** `{"command": "git branch --show-current; git rev-parse HEAD; git status --short | wc -l; ls -d /tmp/venv-drave 2>/dev/null && /tmp/venv-drave/bin/drave --version 2>&1 | head -2", "description": "Check branch and existing venv"}`

  ```
s/v7
7f1519f749ab0939ad24b642abe785e7ab0aa87a
15
/tmp/venv-drave
drave 0.1.0
  ```

- **bash** `{"command": "git status -sb | head -5; git log --oneline origin/s/v7 -3 2>/dev/null; git log --oneline origin/master -3 2>/dev/null; git branch -r | head", "description": "Check remote branch state"}`

  ```
## s/v7
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f/digest.md
 M reports/pensee-coherence-fiches-v7.json
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
71fdf72c CLÔTURE — LE PLAN (51 TÂCHES) ET LE PROTOCOLE OR-ROLES (X2) COMMITTÉS ; L'ÉTAT HORODATÉ
c9067a39 INDEX — RÉGÉNÉRÉ APRÈS LA SEMAINE 2 (W1-W6, X1-X3, Y1)
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
71fdf72c CLÔTURE — LE PLAN (51 TÂCHES) ET LE PROTOCOLE OR-ROLES (X2) COMMITTÉS ; L'ÉTAT HORODATÉ
c9067a39 INDEX — RÉGÉNÉRÉ APRÈS LA SEMAINE 2 (W1-W6, X1-X3, Y1)
  origin/HEAD -> origin/master
  origin/master
  origin/s/close
  origin/s/v7
  ```

- **todo_write** `{"todos": [{"content": "Rejouer le parcours complet dans un clone propre (clone, venv, install, 3 commandes, JSON, tagger, erreurs)", "status": "in_progress"}, {"content": "Écrire docs/produit/demarrage.md avec les sorties réelles", "status": "pending"}, {"content": "Ajouter les liens dans docs/prod … [274 caractères tronqués]`

  ```
Updated todo list: 4 pending, 1 in progress, 0 completed.
  ```

- **bash** `{"command": "set -e\nrm -rf /tmp/qs-drave /tmp/qs-home\nmkdir -p /tmp/qs-home\ncd /tmp\ngit clone --depth 1 https://github.com/stephanedenis/drave.git /tmp/qs-drave > /tmp/qs-clone.log 2>&1\ncd /tmp/qs-drave\ngit rev-parse --short HEAD\npython3 -m venv .venv\n. .venv/bin/activate\nHOME=/tmp/qs-home  … [238 caractères tronqués]`

  ```
7f1519f
3.13.16

[notice] A new release of pip is available: 26.2.1 -> 26.3
[notice] To update, run: pip install --upgrade pip
INSTALL_EXIT=0
  ```

- **bash** `{"command": "cd /tmp/qs-drave && . .venv/bin/activate\nexport HOME=/tmp/qs-home\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\nrun() { echo \"### CMD: $*\"; \"$@\" > /tmp/qs-out.txt 2> /tmp/qs-err.txt; c=$?; echo \"### EXIT: $c\"; echo \"### STDOUT:\"; cat /tmp/qs-out.txt; echo  … [227 caractères tronqués]`

  ```
### CMD: drave --version
### EXIT: 0
### STDOUT:
drave 0.1.0
### STDERR:
### END
### CMD: drave analyser Le chat dort.
### EXIT: 0
### STDOUT:
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
### STDERR:
### END
### CMD: drave evaluer
### EXIT: 0
### STDOUT:
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
SYNTAGMES   F1 81.88 %  (P 86.64 % / R 77.62 %)
  tête      F1 90.83 %  (P 96.11 % / R 86.10 %)
  vue linéaire (partition filtrer) F1 81.88 %  · attachement 93.72 % de couverture
BASE RÉELLE (hand + reel, 452 phras
… [396 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Le chat dort.\"; echo \"exit=$?\"; echo ===; git diff 7f1519f7^ 7f1519f7 -- tools/bloc_linguistique.py | head -120", "description": "Check local analyzer output and T2 diff"}`

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
exit=0
===
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index edb29e19..c397ac4e 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -49,8 +49,10 @@ from typing import Protocol, Sequence
 RACINE = pathlib.Path(__file__).resolve().parent.parent
 try:  # paquet : `tools.bloc_linguistique`
     from . import roles_gp as _roles_gp
+    from .roles_vocabulaire import normaliser_role as _normaliser_role
 except ImportError:  # script : `python3 tools/bloc_linguistique.py`
     import roles_gp as _roles_gp
+    from roles_vocabulaire import normaliser_role as _normaliser_role
 NIVEAUX = 
… [4762 caractères tronqués]
  ```

- **bash** `{"command": "diff -u /tmp/qs-drave/tools/bloc_linguistique.py /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py | head -40; echo \"DIFF_EXIT=${PIPESTATUS[0]}\"; echo ===; diff -u /tmp/qs-drave/tools/drave.py /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py | he … [96 caractères tronqués]`

  ```
DIFF_EXIT=0
===
DIFF2_EXIT=0
  ```

- **bash** `{"command": "cd /tmp && . /tmp/qs-drave/.venv/bin/activate\npython -c 'import tools, tools.drave; print(tools.__file__); print(tools.drave.__file__)'\npython -m pip show drave | sed -n '1,12p'\nhead -20 /tmp/qs-drave/.venv/bin/drave\nls /tmp/qs-drave/.venv/lib/python3.13/site-packages/ | grep -i dra … [59 caractères tronqués]`

  ```
None
/tmp/qs-drave/tools/drave.py
Name: drave
Version: 0.1.0
Summary: Le point d'entrée produit du bloc linguistique de Drave.
Home-page: 
Author: 
Author-email: 
License: 
Location: /tmp/qs-drave/.venv/lib64/python3.13/site-packages
Editable project location: /tmp/qs-drave
Requires: 
Required-by: 
#!/tmp/qs-drave/.venv/bin/python3
import sys
from tools.drave import main
if __name__ == '__main__':
    sys.argv[0] = sys.argv[0].removesuffix('.exe')
    sys.exit(main())
drave-0.1.0.dist-info
__editable___drave_0_1_0_finder.py
__editable__.drave-0.1.0.pth
  ```

- **bash** `{"command": "cd /tmp/qs-drave\necho \"== direct, HOME qs ==\"; HOME=/tmp/qs-home python3 tools/drave.py analyser \"Le chat dort.\"\necho \"== direct, HOME real ==\"; HOME=/home/stephane python3 tools/drave.py analyser \"Le chat dort.\"\necho \"== installed, HOME real ==\"; HOME=/home/stephane /tmp/q … [99 caractères tronqués]`

  ```
== direct, HOME qs ==
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
== direct, HOME real ==
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
== installed, HOME real ==
dra
… [558 caractères tronqués]
  ```

- **bash** `{"command": "diff -qr /tmp/qs-drave /home/stephane/Data13TB/stephane/GitHub/Qtrinet -x .git -x .venv 2>/dev/null | head -40", "description": "Diff whole trees"}`

  ```
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet: data
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs: agent
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas: decision.puml.svg
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas: pipeline.mmd.svg
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core: target
Only in /tmp/qs-drave: drave.egg-info
Files /tmp/qs-drave/journal/README.md and /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/README.md differ
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/00221850-90de-4287-90ee-324a35e504cd: session.v4.jsonl.zstd
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/04ed1834-b0f8-42a1-aa21-75a75c19647e: session.jsonl.zstd
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c: session.v4.jsonl.zstd
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880: session.v4.jsonl.zstd
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2: session.v4.jsonl.zstd
Only 
… [3688 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/ | head -30; echo ===; diff -qr /tmp/qs-drave/tools /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools -x __pycache__ | head -30", "description": "Diff tools directory"}`

  ```
M tools/chantier/plan.json
?? tools/tests/linguistique/gold_reel_50.py
===
Files /tmp/qs-drave/tools/chantier/plan.json and /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/chantier/plan.json differ
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: CHANGELOG.md
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: CONTRIBUTING.md
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: .git
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: .github
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: .gitignore
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: LICENSE
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: Makefile
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: pyproject.toml
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: .pytest_cache
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: README.md
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: .ruff_cache
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch: SECURITY.md
… [1494 caractères tronqués]
  ```

- **bash** `{"command": "diff -qr /tmp/qs-drave/tools/tests /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests -x __pycache__ | head -40; echo ===; ls /tmp/qs-drave/tools/tests/linguistique | head; echo ===; ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique | head", "descripti … [33 caractères tronqués]`

  ```
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique: gold_reel_50.py
===
anaphore.py
classement_cible.py
classer_gv.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel.json
gold_reel.py
gold_restitution_v2.json
===
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

- **bash** `{"command": "cd /tmp && echo \"local script from /tmp:\"; python3 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py analyser \"Le chat dort.\" | sed -n '1,10p'; echo \"clone script from local root:\"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/qs-drave/tools/drav … [94 caractères tronqués]`

  ```
local script from /tmp:
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
clone script from local root:
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
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"== local with fresh pycache prefix ==\"; PYTHONPYCACHEPREFIX=/tmp/pycache-fresh python3 tools/drave.py analyser \"Le chat dort.\" | sed -n '5,9p'\necho \"== clone with fresh pycache prefix ==\"; cd /tmp/qs-drave && PYTHONPYCACHE … [368 caractères tronqués]`

  ```
== local with fresh pycache prefix ==
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
== clone with fresh pycache prefix ==
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·
== local pyc ==
-rw-r--r--. 1 stephane stephane 195029 15 nov 22:08 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/__pycache__/bloc_linguistique.cpython-313.pyc
-rw-------. 1 stephane stephane 76432 15 nov 22:02 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/__pycache__/drave.cpython-313.pyc
  ```

- **bash** `{"command": "ls -l /tmp/qs-drave/tools/roles_vocabulaire.py /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_vocabulaire.py; cmp /tmp/qs-drave/tools/roles_vocabulaire.py /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_vocabulaire.py && echo SAME; echo ===; diff -qr /tmp/qs-dra … [216 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane 4575 15 nov 21:54 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_vocabulaire.py
-rw-r--r--. 1 stephane stephane 4575 15 nov 22:18 /tmp/qs-drave/tools/roles_vocabulaire.py
SAME
===
Only in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique: gold_reel_50.py
  ```

- **bash** `{"command": "env | grep -i \"^DRAVE\\|^PYTHON\" || echo none", "description": "Check DRAVE and Python env vars"}`

  ```
PYTHONSTARTUP=/etc/pythonstart
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"data\\|RACINE\\|lexique\\|json\" tools/bloc_linguistique.py | head -80", "description": "Find data dependencies in analyzer"}`

  ```
24:    python3 tools/bloc_linguistique.py --mode parallele --fichier page.txt --json
25:    python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl
37:import json
44:import unicodedata
46:from dataclasses import dataclass, field
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
64:@dataclass(frozen=True)
69:    def json(self) -> dict:
73:@dataclass
87:    def json(self) -> dict:
93:            "script": self.script, "meta": _meta_json(self.meta),
102:def _meta_json(meta: dict) -> dict:
124:@dataclass
149:    def json(self, avec_duree: bool = False) -> dict:
158:            "etiquettes": [e.json() for e in self.etiquettes],
159:            "unites_semantiques": [u.json() for u in self.unites_semantiques],
180:    return unicodedata.normalize("NFC", texte).casefold()
205:        d = json.loads(ligne)
269:        nom = unicodedata.name(ch)
305:# --------------------------------------------------------------------------- lexiques
423:# Un lexique verbal minimal, bilingue, pour arbitrer les classes ouvertes : le POS de surface
641:    r"(?<![\w])(?:[\w.-]+)\.(?:py|pyi|md|rst|txt|json|jsonl|csv|tsv|ya?ml|toml|ini|cfg|sh|bash|zsh|html?|css|js|ts|jsx|tsx|svg|
… [2654 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1000,1070p' tools/bloc_linguistique.py; echo ===; ls tools/structures | head; git ls-files tools/structures | head; echo ===; grep -rn \"roles_gp\\|structures\" tools/bloc_linguistique.py | head -30", "description": "Inspect  … [23 caractères tronqués]`

  ```
# un nom propre sujet : un seul mot, majuscule, pas un mot fermé ; la
                # forme inversée « Peux-tu » est un verbe + enclitique, pas un sujet.
                nom_propre = ("-" not in mots[0][2] and mots[0][2][:1].isupper()
                              and not _est_verbe(mots[0][2])
                              and self._pos(langue, mots[0][2])[0] != "VERB"
                              and n0 not in lex.get("DET", set())
                              and n0 not in lex.get("PREP", set())
                              and n0 not in lex.get("CONJ", set())
                              and n0 not in lex.get("PRON", set()))
                if (n0e in _suj or nom_propre) and sv:
                    fin_sujet = mots[0][1]
                    if fin_sujet < f:
                        gn = dict(s)
                        gn.update({"type": "GN", "role": "agent", "niveau": 0,
                                   "fin": fin_sujet,
                                   "texte": texte[d:fin_sujet], "parent": None})
                        gv = dict(s)
                        debut_gv = mots[1][0]
                        gv.update({"debut": debut_gv, "texte": texte[debut_gv:f]})
     
… [2800 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat .gitmodules 2>/dev/null || echo \"no .gitmodules\"; git submodule status 2>&1 | head; git ls-tree HEAD tools/structures; git ls-tree HEAD tools/docwatch 2>/dev/null; git config --get-regexp '^submodule\\.' 2>/dev/null | head", "d … [39 caractères tronqués]`

  ```
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
 d256888934b017ac024de2a8eed22ecf81e6c799 tools/docwatch (v0.4.1-3-gd256888)
 389b99f8383eb47c0cc008f5d3211c9d65d895fc tools/structures (heads/master)
160000 commit 389b99f8383eb47c0cc008f5d3211c9d65d895fc	tools/structures
160000 commit d256888934b017ac024de2a8eed22ecf81e6c799	tools/docwatch
submodule.tools/docwatch.url https://github.com/stephanedenis/docwatch.git
submodule.tools/docwatch.active true
submodule.tools/structures.url /home/stephane/Data13TB/stephane/GitHub/drave-structures
submodule.tools/structures.active true
  ```

- **bash** `{"command": "timeout 20 git ls-remote https://github.com/stephanedenis/drave-structures.git HEAD 2>&1 | head -3; echo \"exit=${PIPESTATUS[0]}\"; timeout 20 git ls-remote https://github.com/stephanedenis/docwatch.git HEAD 2>&1 | head -3; echo \"exit2=${PIPESTATUS[0]}\"", "description": "Check structu … [34 caractères tronqués]`

  ```
ERROR: Repository not found.
fatal: Could not read from remote repository.

exit=128
95e94c47007672e4a64e6a4952944e071f92ef94	HEAD
exit2=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"segmenter_s\" tools/bloc_linguistique.py | head -30; echo ===; grep -n \"def __init__\" tools/bloc_linguistique.py | head -10; sed -n '400,470p' tools/bloc_linguistique.py", "description": "Find segmenter_s usage"}`

  ```
840:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
844:        self.segmenter_s = segmenter_s
1026:        if not self.segmenter_s:
1043:        if not self.segmenter_s:
1965:        h = Heuristique(segmenter_s=False)
===
840:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
1953:    def __init__(self, profils: dict[str, dict] | None = None):
2009:    def __init__(self, modele: str | pathlib.Path, llama_cli: str = "llama-cli",
2098:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18081",
2227:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
2357:    def __init__(self, pos: BlocLinguistique, chunks: BlocLinguistique,
2407:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
2757:    def __init__(self, blocs: Sequence[BlocLinguistique],
2782:    def __init__(self, heuristique: BlocLinguistique, neuronal: BlocLinguistique,
2822:    def __init__(self, cout_par_octet: float = 1.0):
}

RELATIFS = {"qui", "que", "qu", "dont", "où", "which", "that", "who", "whom", "whose",
            "where"
… [5109 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '835,930p' tools/bloc_linguistique.py; echo ===; grep -n \"def analyser\" tools/bloc_linguistique.py | head -5; sed -n '1730,1810p' tools/bloc_linguistique.py", "description": "Read Heuristique init and analyser"}`

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
… [9773 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qs-drave && for p in alternative filtrer filtrer_union brut; do echo \"== $p ==\"; python3 tools/drave.py analyser \"Le chat dort.\" --partition $p | sed -n '5,8p'; done", "description": "Test partitions without submodule"}`

  ```
== alternative ==
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
== filtrer ==
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
== filtrer_union ==
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
== brut ==
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
  ```

- **bash** `{"command": "du -sh /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures; find /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures -maxdepth 1 -type f | wc -l; du -sh /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/* 2>/dev/null | sort -h | tail -10", "descr … [32 caractères tronqués]`

  ```
1,1M	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures
14
12K	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_corpus.py
12K	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/mesure_analyseur.py
12K	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/mesure_corpus.py
16K	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/serveur.py
24K	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/README.md
32K	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py
32K	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/static
124K	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests
172K	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/__pycache__
636K	/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '\"role\"\\|role.*=\\|_role' tools/bloc_linguistique.py | sed -n '1,80p'", "description": "Find role assignment logic"}`

  ```
51:    from . import roles_gp as _roles_gp
52:    from .roles_vocabulaire import normaliser_role as _normaliser_role
54:    import roles_gp as _roles_gp
55:    from roles_vocabulaire import normaliser_role as _normaliser_role
97:def normaliser_role(role: str, strict: bool = True) -> str:
99:    return _normaliser_role(role, strict=strict)
105:    Le rôle brut reste dans l'objet Python (`e.meta["role"]`) : les règles internes et
110:    if "role" in sortie:
111:        sortie["role"] = normaliser_role(sortie.get("role", ""))
113:        if isinstance(alternative, dict) and "role" in alternative:
114:            alternative["role"] = normaliser_role(alternative.get("role", ""))
565:def _role_gp(prep: str, suivant: str = "", precedent: str = "",
576:        return _roles_gp.role_gp(prep, suivant=suivant, precedent=precedent,
1013:                        gn.update({"type": "GN", "role": "agent", "niveau": 0,
1451:                                     "role": "complément" if stype == "SUB" else "qualité",
1472:                role = "groupe nominal"
1477:                    role = "patient"
1478:                segments.append({"type": "GN", "role": role, "niveau": 0,
1486:              
… [1523 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1420,1560p' tools/bloc_linguistique.py", "description": "Read fallback chunker roles"}`

  ```
j = i + 1
                    verbes_vus = 0
                    prec_aux = False      # le mot précédent est un auxiliaire (même groupe)
                    predicat_vu = False   # un prédicat a déjà été vu dans la clause
                    while j < len(mots) and mots[j][3] == "mot":
                        m = mots[j][2]
                        aux = _normaliser(m) in AUXILIAIRES
                        if aux:
                            if predicat_vu and not prec_aux:
                                break      # un AUX après un prédicat ouvre la principale
                            prec_aux = True
                            j += 1
                            continue
                        if est_verbe(mots[j][0], m):
                            if prec_aux:
                                # verbe plein collé à son auxiliaire : même groupe verbal
                                predicat_vu = True
                                prec_aux = False
                                j += 1
                                continue
                            verbes_vus += 1
                            if predicat_vu or verbes_vus == 2:
                                break  # se
… [7597 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp\nfor s in \"Le chat dort.\" \"Il dort.\" \"Le chat mange.\" \"Marie lit.\" \"Le chien court.\" \"Elle travaille.\" \"Le chat est sur le toit.\" \"Le livre est intéressant.\" \"The cat sleeps.\"; do\n  a=$(cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave. … [325 caractères tronqués]`

  ```
DIFF: Le chat dort.
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
--
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
DIFF: Il dort.
  GN   [0:2]  Il    rôle=agent     → dort
  GV   [3:7]  dort  rôle=predicat  → —
PRAGMATIQUE
--
  GN   [0:2]  Il    rôle=agent     → dort
  GV   [3:7]  dort  rôle=predicat  → —
PRAGMATIQUE
DIFF: Le chat mange.
  GN   [0:7]   Le chat  rôle=agent     → mange
  GV   [8:13]  mange    rôle=predicat  → chat
PRAGMATIQUE
--
  GN   [0:7]   Le chat  rôle=objet     → mange
  GV   [8:13]  mange    rôle=predicat  → —
PRAGMATIQUE
SAME: Marie lit.
DIFF: Le chien court.
  GN   [0:8]   Le chien  rôle=agent     → court
  GV   [9:14]  court     rôle=predicat  → chien
PRAGMATIQUE
--
  GN   [0:8]   Le chien  rôle=objet     → court
  GV   [9:14]  court     rôle=predicat  → —
PRAGMATIQUE
DIFF: Elle travaille.
  GN   [0:4]   Elle       rôle=agent     → travaille
  GV   [5:14]  travaille  rôle=predicat  → —
PRAGMATIQUE
--
  GN   [0:4]   Elle       rôle=agent     → travaille
  GV   [5:14]  travaille  rôle=predicat  → —
PRAGMATIQUE
DIFF: Le chat est sur le toit.
  GN   
… [603 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qs-drave && python3 tools/drave.py analyser \"Marie lit.\"; echo exit=$?; echo ===; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Marie lit.\"", "description": "Check stable sample full output"}`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=und script=Latn source=heuristique · 16 étiquettes · unités sémantiques=2 (80.0% du texte)
POS  Marie/NOUN lit/VERB ./PONCT
SYNTAGMES
  GN   [0:5]  Marie  rôle=agent     → lit
  GV   [6:9]  lit    rôle=predicat  → —
PRAGMATIQUE
  phrase [0:10] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
exit=0
===
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=und script=Latn source=heuristique · 16 étiquettes · unités sémantiques=2 (80.0% du texte)
POS  Marie/NOUN lit/VERB ./PONCT
SYNTAGMES
  GN   [0:5]  Marie  rôle=agent     → lit
  GV   [6:9]  lit    rôle=predicat  → —
PRAGMATIQUE
  phrase [0:10] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
  ```

- **bash** `{"command": "cd /tmp\nfor s in \"Marie lit un livre.\" \"Marie mange une pomme.\" \"Le chat dort sur le toit.\" \"Paris est une ville.\" \"Marie lit le livre.\" \"Le chat de Marie dort.\" \"Le chat noir dort.\" \"Le petit chat dort.\"; do\n  a=$(cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet &&  … [308 caractères tronqués]`

  ```
DIFF: Marie lit un livre.
DIFF: Marie mange une pomme.
DIFF: Le chat dort sur le toit.
DIFF: Paris est une ville.
DIFF: Marie lit le livre.
DIFF: Le chat de Marie dort.
DIFF: Le chat noir dort.
DIFF: Le petit chat dort.
  ```

- **bash** `{"command": "cd /tmp\nfor s in \"Marie lit.\" \"Il dort.\" \"Le chat dort.\"; do\n  a=$(cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"$s\" --langue fr 2>/dev/null)\n  b=$(cd /tmp/qs-drave && python3 tools/drave.py analyser \"$s\" --langue fr 2>/dev/null)\n   … [181 caractères tronqués]`

  ```
DIFF --langue fr: Marie lit.
DIFF --langue fr: Il dort.
DIFF --langue fr: Le chat dort.
  ```

- **bash** `{"command": "cd /tmp/qs-drave && python3 tools/drave.py analyser \"The cat sleeps.\"; echo ===; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"The cat sleeps.\"", "description": "Check English sample output"}`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=en script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (60.0% du texte)
POS  The/DET cat/NOUN sleeps/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   The cat  rôle=objet     → sleeps
  GV   [8:14]  sleeps   rôle=predicat  → —
PRAGMATIQUE
  phrase [0:15] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
===
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=en script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (60.0% du texte)
POS  The/DET cat/NOUN sleeps/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   The cat  rôle=objet     → sleeps
  GV   [8:14]  sleeps   rôle=predicat  → —
PRAGMATIQUE
  phrase [0:15] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1800,1905p' tools/bloc_linguistique.py", "description": "Read segment publication and target logic"}`

  ```
cible = None  # « a » / « est » ne sont pas des cibles
                    if not cible:
                        gns_s = [x for x in c.get("segments", []) if x.get("type") == "GN"]
                        cible = (self._repli_cible_gp(texte, s, gns_s)
                                 or self._cible_proche(texte, s, gvs, verbes, cache_gv))
                    cible = self._cible_hors_span(texte, s, gvs, cible)
                    cible = self._repli_verbe_propre(texte, s, cible)
                    candidats = list(noms) + self._verbes_proches(
                        texte, s, gvs, verbes=verbes, cache=cache_gv)
                    # la **tête** de chaque candidat S (« « … » → Le livre » → livre ; « … → Les
                    # fleurs poussent » → poussent) : mesuré +45 segments au top-k strict.
                    for nom in noms:
                        if "→" in nom:
                            tete = self._tete_texte(nom.split("→", 1)[1])
                            if tete and tete not in candidats:
                                candidats.append(tete)
                    meta = {"role": s.get("role", ""), "niveau": s.get("niveau", 0)}
                    if cible:
         
… [5320 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _repli_cible_gp\\|def _cible_proche\\|def _candidats_precedent\\|def _verbes_proches\\|def _cible_hors_span\" tools/bloc_linguistique.py; sed -n '1070,1230p' tools/bloc_linguistique.py", "description": "Read target help … [14 caractères tronqués]`

  ```
1156:    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:
1176:    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict]) -> str | None:
1198:    def _cible_hors_span(texte: str, segment: dict, gvs: list[dict], cible: str | None):
1274:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
1309:    def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
        Le gold : « elle qui commence nage » → REL « qui commence » a pour cible `elle`,
        sujet du GV `nage`. La règle ne s'applique qu'aux REL sans antécédent dans le
        chemin courant (union S/chunker) et exige un GV à droite **et** un GN à gauche.
        La règle littérale « REL après un GV » ne s'applique à aucun segment du gold.
        """
        if segment.get("type") != "REL":
            return None
        droites = [x for x in tous if x.get("type") == "GV"
                   and x.get("debut", 0) >= segment.get("fin", 0)]
        if not droites:
            return None
        gauches = [x for x in tous if x.get("type") == "GN"
                   and x.get("fin", 0) <= segment.get("debut", 0)]
        if not gauches:
            return None
… [6888 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1270,1355p' tools/bloc_linguistique.py", "description": "Read cible_proche and verbes_proches"}`

  ```
cache[cle] = v
        return v

    @staticmethod
    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
                      verbes: list[tuple[int, int, str]] | None = None,
                      cache: dict | None = None) -> str | None:
        """La cible d'un segment : le **verbe du GV le plus proche** (règle de proximité).

        Rend `None` si le segment est lui-même un GV ou s'il n'y a pas de GV. Le verbe est le
        dernier token du GV (`a vu` → `vu`, `est mangé` → `mangé`).
        """
        gvs = [g for g in gvs if not _est_adverbe_seul(g)]
        if segment.get("type") == "GV" or not gvs:
            return None
        if segment.get("type") == "GP":
            # un GP n'est pas gouverné par un mot de son propre span (« est prêt à manger »)
            dehors = [g for g in gvs
                      if not (g["debut"] >= segment["debut"] and g["fin"] <= segment["fin"])]
            if dehors:
                gvs = dehors
        # le plus proche, tous côtés mêlés : la variante « GV de gauche d'abord » a été
        # mesurée (2026-11-05) et donne **le même** exact — elle n'est pas retenue.
        def ecart(g: dict) -> int:
            if g["fin"] 
… [2909 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'EOF'\nimport generateur, json\nprint(json.dumps(generateur.analyser(\"Le chat dort.\"), ensure_ascii=False, indent=1)[:3000])\nEOF", "description": "Inspect S generator output"}`

  ```
[
 {
  "nom": "structure la plus proche",
  "lecture": "chaque segment se rattache à la cible la plus proche.",
  "attachement": null,
  "segments": [
   {
    "debut": 0,
    "fin": 7,
    "texte": "Le chat",
    "type": "GN",
    "role": "agent",
    "niveau": 1,
    "parent": 1,
    "profondeur": 1
   },
   {
    "debut": 8,
    "fin": 12,
    "texte": "dort",
    "type": "GV",
    "role": "predicat",
    "niveau": 0,
    "parent": null,
    "profondeur": 0
   }
  ]
 }
]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Le chat dort.\" --json | python3 -c 'import json,sys; a=json.load(sys.stdin); [print(json.dumps(e,ensure_ascii=False,indent=1)) for e in a[\"etiquettes\"] if e[\"niveau\"]==\"syntagme\"]'", "descript … [36 caractères tronqués]`

  ```
{
 "niveau": "syntagme",
 "type": "GN",
 "valeur": "Le chat",
 "debut": 0,
 "fin": 7,
 "source": "heuristique",
 "confiance": 0.55,
 "candidats": [
  "structure la plus proche",
  "dort"
 ],
 "langue": "fr",
 "script": "Latn",
 "meta": {
  "role": "agent",
  "niveau": 1,
  "attachement": {
   "segment": "Le chat",
   "cible": "dort",
   "candidats": [
    {
     "span": {
      "debut": 8,
      "fin": 12
     },
     "cible": "dort",
     "source": "heuristique"
    }
   ]
  }
 }
}
{
 "niveau": "syntagme",
 "type": "GV",
 "valeur": "dort",
 "debut": 8,
 "fin": 12,
 "source": "heuristique",
 "confiance": 0.55,
 "candidats": [
  "structure la plus proche"
 ],
 "langue": "fr",
 "script": "Latn",
 "meta": {
  "role": "predicat",
  "niveau": 0,
  "attachement": {
   "segment": "dort",
   "cible": "chat",
   "candidats": [
    {
     "span": {
      "debut": 3,
      "fin": 7
     },
     "cible": "chat",
     "source": "heuristique"
    }
   ]
  }
 }
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"attachement\\|cible\" tools/bloc_linguistique.py | sed -n '60,140p'", "description": "Find attachment post-processing"}`

  ```
1804:                                 or self._cible_proche(texte, s, gvs, verbes, cache_gv))
1805:                    cible = self._cible_hors_span(texte, s, gvs, cible)
1806:                    cible = self._repli_verbe_propre(texte, s, cible)
1817:                    if cible:
1818:                        meta["attachement"] = self._attachement(
1819:                            texte, s, cible, candidats, self.nom)
1832:                cible = (self._cible_precedent(texte, s, prec, verbes)
1833:                         or self._repli_cible_gp(texte, s, [x for x in simples if x["type"] == "GN"])
1834:                         or self._cible_proche(texte, s, gvs_s, verbes, cache_gv))
1835:                cible = self._cible_hors_span(texte, s, gvs_s, cible)
1836:                cible = self._repli_verbe_propre(texte, s, cible)
1841:                if cible:
1842:                    meta["attachement"] = self._attachement(
1843:                        texte, s, cible, candidats, self.nom)
1861:                cible = (self._cible_precedent(texte, s, prec, verbes)
1862:                         or self._cible_rel_sujet(
1865:                         or self._repli_cible_gp(texte, s, [
… [759 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _verbe_dans\" -A30 tools/bloc_linguistique.py", "description": "Read _verbe_dans"}`

  ```
1243:    def _verbe_dans(texte: str, debut: int, fin: int,
1244-                    verbes: list[tuple[int, int, str]] | None = None,
1245-                    strict: bool = False) -> str | None:
1246-        """Le **verbe** du span : le lexique d'abord, puis le POS `VERB`, sinon le dernier mot."""
1247-        mots = [(m.start() + debut, m.group()) for m in re.finditer(r"[\wÀ-ÿ'-]+", texte[debut:fin])]
1248-        mots = [(d, _sans_enclitique(m)) for d, m in mots]
1249-        # le verbe **plein** d'abord : « J'ai vu » donne `vu`, pas `ai`
1250-        for _, m in mots:
1251-            if _est_verbe(m) and _normaliser(m) not in AUXILIAIRES:
1252-                return m
1253-        for _, m in mots:
1254-            if _est_verbe(m) and _normaliser(m) not in AUXILIAIRES:
1255-                return m
1256-        if verbes:
1257-            for d, f, v in verbes:
1258-                if d >= debut and f <= fin:
1259-                    return v
1260-        return None if strict else (mots[-1][1] if mots else None)
1261-
1262-    @staticmethod
1263-    def _verbe_gv(texte: str, g: dict, verbes, cache: dict | None = None):
1264-        """`_verbe_dans` mémoïsé par span de GV : l
… [367 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"sous-module\\|submodule\\|structures\" docs/ README.md | head -30", "description": "Search submodule documentation"}`

  ```
docs/archive/architecture-cerveau-et-drave.md:105:  structures décrites ici n'a été simulée ici.
docs/archive/hebbien-differentiel-et-biologie.md:119:### Écart 3 — nos structures sont saturées, donc la croissance ne veut rien dire
docs/archive/note-un-pont-par-professeur.md:79:se demander s'il émerge des structures communes. **C'est un projet pour l'initiative
docs/schemas/chantiers-vision.svg:3:<desc>D (données) alimente L (bloc langue), N (natif), S (structures) et R (lecteur) ; L alimente S, B et N ; S alimente B et renvoie ses validations à L ; A (moteur) exécute N et B ; N porte R1–R3 ; B10.3 attend R5 ; B13 (pensée) consomme R, L et N. Trait plein : alimente ou débloque ; pointillé : attend ou plafonne.</desc>
docs/schemas/chantiers-vision.svg:10:<rect x="620" y="96" width="200" height="86" rx="8" fill="#e0f2f1" stroke="#00695c" stroke-width="2"/><text x="720.0" y="130" text-anchor="middle" font-size="16" font-weight="bold" fill="#00695c">S — les structures</text><text x="720.0" y="154" text-anchor="middle" font-size="11" fill="#444">candidats · validation humaine</text>
docs/methode/modularisation.md:7:> **Résumé —** Faut-il diviser le dépôt en submodules et paralléliser ? L
… [4366 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '80,120p' docs/pilotage/utilisation.md", "description": "Read submodule usage doc"}`

  ```
`docs/schemas/README.md` référence ✓. Les blocs Markdown `mermaid` / `puml` sont aussi rendus, via le cache
et la route `/diagram/<hash>.<affixe>.svg` ✓. Un outil absent laisse le bloc intact ✓.

Outils installés localement : `~/.local/bin/plantuml` (JAR) et `~/.local/bin/mmdc`
(`@mermaid-js/mermaid-cli`, Chrome système) ✓. Les chemins sont dans `[diagrams]` ✓.

**Le 27/10, l'ancien `serveur-doc.py` (port 8787, `drave-doc.service`) a été retiré** ✓ : il faisait double
emploi avec docwatch et n'était pas versionnable indépendamment. La page « où en est » se lit désormais
directement dans [`docs/pilotage/en-cours.md`](en-cours.md) ✓ — c'est le document épinglé à ouvrir dans docwatch ✓.
Le code reste dans l'historique Git et une sauvegarde hors dépôt ✓.

**Ce qui change pour la suite** : toute évolution de la présentation (arbre, rendu, épingles, routes) va dans
le dépôt public — il est épinglé dans **`tools/docwatch/`** comme sous-module ✓. Drave ne garde **aucun**
serveur de documentation ✓.

### Le code est un sous-module de Drave

Après un clone :

```bash
git submodule update --init --recursive
```

Pour faire évoluer une fonctionnalité :

```bash
cd tools/docwatch
pytest && ruff
… [497 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qs-drave && . .venv/bin/activate && export HOME=/tmp/qs-home\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\ncd /tmp\necho \"=== JSON raw (first 25 lines) ===\"\ndrave analyser \"Le chat dort.\" --json > /tmp/qs-annotation.json; echo \"exit=$?\"; wc -c /tmp/q … [605 caractères tronqués]`

  ```
=== JSON raw (first 25 lines) ===
exit=0
5899 /tmp/qs-annotation.json
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
  {
   "niveau": "mot",
   "type": "mot",
=== JSON consumer ===
schema= drave.annotation version= 2 langue= fr etiquettes= 20
syntagmes= [('GN', 'Le chat'), ('GV', 'dort')]
roles= [('GN', 'objet'), ('GV', 'predicat')]
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Le chat dort.\" --json | wc -c; python3 tools/drave.py evaluer --json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(list(d)[:20]); print(d.get(\"version\"), d.get(\"gold\"))' 2>/dev/nu … [53 caractères tronqués]`

  ```
6179
['version', 'gold', 'heuristique', 'reel', 'syntagmes_lineaire', 'attachement_lineaire', 'controle_negatif']
0.1.0 {'nom': 'vivant (hand + reel + synthétique)', 'gele': False, 'phrases': 612, 'tokens': 3179, 'cibles_attachement': 239}
  ```

- **bash** `{"command": "cd /tmp/qs-drave && . .venv/bin/activate\nrun() { echo \"### CMD: $*\"; \"$@\" > /tmp/qs-out.txt 2> /tmp/qs-err.txt; c=$?; echo \"### EXIT: $c\"; echo \"### STDOUT:\"; cat /tmp/qs-out.txt; echo \"### STDERR:\"; cat /tmp/qs-err.txt; echo \"### END\"; }\nexport HOME=/tmp/qs-home\nunset DE … [230 caractères tronqués]`

  ```
### CMD: drave analyser Le chat dort. --tagger
### EXIT: 4
### STDOUT:
### STDERR:
drave: dépendance absente : clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans ~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.
### END
### CMD: drave analyser Le chat dort. --tagger auto
### EXIT: 0
### STDOUT:
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
### STDERR:
drave: tagger auto · heuristique (clé absente)
### END
  ```

- **bash** `{"command": "cd /tmp/qs-drave && . .venv/bin/activate\nexport HOME=/home/stephane\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\ncd /tmp\ntimeout 60 drave analyser \"Le chat dort.\" --tagger > /tmp/qs-tagger-out.txt 2> /tmp/qs-tagger-err.txt; c=$?\necho \"EXIT=$c\"; echo \"=== S … [153 caractères tronqués]`

  ```
EXIT=0
=== STDOUT ===
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.3 s
=== STDERR ===
  ```

- **bash** `{"command": "cd /tmp/qs-drave && . .venv/bin/activate\nexport HOME=/home/stephane\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\ncd /tmp\ntimeout 30 drave analyser \"Le chat dort.\" --tagger > /tmp/qs-tagger2-out.txt 2> /tmp/qs-tagger2-err.txt; c=$?\necho \"EXIT=$c\"; tail -2 /t … [119 caractères tronqués]`

  ```
EXIT=0
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=0 · cache=1 · tokens=0 · latence=0.0 s
  ```

- **bash** `{"command": "cd /tmp/qs-drave && . .venv/bin/activate\nexport HOME=/tmp/qs-home\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\ncd /tmp\nrun() { echo \"### CMD: $*\"; \"$@\" > /tmp/qs-out.txt 2> /tmp/qs-err.txt; c=$?; echo \"### EXIT: $c\"; echo \"### STDOUT:\"; cat /tmp/qs-out.t … [337 caractères tronqués]`

  ```
### CMD: drave analyser 
### EXIT: 3
### STDOUT:
### STDERR:
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
### END
### CMD: drave analyser  --json
### EXIT: 3
### STDOUT:
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
### STDERR:
### END
### CMD: drave analyser --fichier /tmp/absent-xyz.txt
### EXIT: 1
### STDOUT:
### STDERR:
drave: erreur : FileNotFoundError : [Errno 2] No such file or directory: '/tmp/absent-xyz.txt'
### END
### CMD: drave analyser --fichier /tmp
### EXIT: 1
### STDOUT:
### STDERR:
drave: erreur : IsADirectoryError : [Errno 21] Is a directory: '/tmp'
### END
### CMD: drave analyser Le chat dort. --langue de
### EXIT: 2
### STDOUT:
### STDERR:
usage: drave analyser [-h] [--partition {brut,alternative,filtrer_union,filtrer}] [--fichier CHEMIN]
                      [--jsonl] [--contexte CONTEXTE] [--langue {fr,en}] [--tagger] [--json]
          
… [537 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qs-drave && . .venv/bin/activate\nexport HOME=/tmp/qs-home\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\ncd /tmp\necho \"=== REJOUER ===\"; drave rejouer \"Le chat dort.\"; echo \"exit=$?\"\necho \"=== RESTITUER ===\"; drave restituer \"Le chat dort.\"; ech … [63 caractères tronqués]`

  ```
=== REJOUER ===
rejeu identique : oui
  texte      : 'Le chat dort.'
  langue     : fr
  étiquettes : 20
  JSON       : 4217 octets · sha256 2577786670e5752c…
exit=0
=== RESTITUER ===
restitution (annotation → surface)
source      : 'Le chat dort.'
surface     : 'Le chat dort.'
fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%
mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%
pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%
miroir      : 0.0000 (non exact) — minimum des fidélités binaires de la surface (graphème), des mots et des POS ; une sortie n'est fidèle que si elle reproduit exactement la source
contrôle négatif : mélange exacte 0.0000 (caractères 0.3077) · troncature exacte 0.0000 (caractères 0.9231)
exit=0
  ```

- **bash** `{"command": "cd /tmp\nfor s in \"Il pleut.\" \"Dors.\" \"Le chat et le chien dorment.\" \"Le chat, le chien et la souris dorment.\" \"Hier, il a plu.\" \"Le chat dort et le chien mange.\" \"Bonjour.\" \"Le chat.\" \"Chat.\" \"Le chat dort-il ?\"; do\n  a=$(cd /home/stephane/Data13TB/stephane/GitHub/ … [307 caractères tronqués]`

  ```
DIFF: Il pleut.
SAME: Dors.
langue=und script=Latn source=heuristique · 11 étiquettes · unités sémantiques=1 (80.0% du texte)
POS  Dors/NOUN ./PONCT
SYNTAGMES
  GV   [0:4]  Dors  rôle=predicat  → —
PRAGMATIQUE
  phrase [0:5] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·

DIFF: Le chat et le chien dorment.
DIFF: Le chat, le chien et la souris dorment.
DIFF: Hier, il a plu.
DIFF: Le chat dort et le chien mange.
SAME: Bonjour.
langue=und script=Latn source=heuristique · 10 étiquettes · unités sémantiques=1 (87.5% du texte)
POS  Bonjour/NOUN ./PONCT
SYNTAGMES —
PRAGMATIQUE
  phrase [0:8] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · phrase=0.85 ·
            discours=0.50 · pragmatique=0.45 · document=0.70

DIFF: Le chat.
SAME: Chat.
langue=und script=Latn source=heuristique · 10 étiquettes · unités sémantiques=1 (80.0% du texte)
POS  Chat/NOUN ./PONCT
SYNTAGMES —
PRAGMATIQUE
  phrase [0:5] déclarative · acte=assertion · négation=non · modalité=non · doubl
… [188 caractères tronqués]
  ```

- **bash** `{"command": "set -e\nrm -rf /tmp/qs-drave2 /tmp/qs-home2\nmkdir -p /tmp/qs-home2\ncd /tmp\nT0=$(date +%s%N)\ngit clone --depth 1 https://github.com/stephanedenis/drave.git /tmp/qs-drave2 >/tmp/qs2-clone.log 2>&1\nT1=$(date +%s%N)\ncd /tmp/qs-drave2\npython3 -m venv .venv\nT2=$(date +%s%N)\n. .venv/b … [469 caractères tronqués]`

  ```
clone 5.41 s
venv 3.73 s
install 3.42 s
total 12.56 s
Installing collected packages: drave
Successfully installed drave-0.1.0

[notice] A new release of pip is available: 26.2.1 -> 26.3
[notice] To update, run: pip install --upgrade pip
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat .gitignore | head -40; grep -n \"venv\" .gitignore", "description": "Check venv gitignore"}`

  ```
__pycache__/
*.pyc
*.egg-info/
/build/
/dist/
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
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py evaluer | sed -n '1,20p'", "description": "Capture local full evaluer output", "timeoutMs": 120000}`

  ```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)
  tête      F1 90.29 %  (P 92.61 % / R 88.08 %)
  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture
BASE RÉELLE (hand + reel, 452 phrases)  POS 88.91 % · F1 79.06 % · attachement 99.46 %
ATTACHEMENT exact 99.58 % · couverture 99.58 % · exact sur span 100.00 % · top-k 98.74 %
  tête      couverture 100.00 % · top-k 99.16 %
PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %
FRACTION SÉMANTIQUE 54.76 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
  ```

- **bash** `{"command": "cd /tmp/qs-drave2 && . .venv/bin/activate && export HOME=/tmp/qs-home2\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\ncd /tmp\ndrave analyser \"Le chat dort.\" --json > annotation.json; echo \"save_exit=$?\"\npython3 -m json.tool annotation.json | sed -n '1,24p'\nec … [415 caractères tronqués]`

  ```
save_exit=0
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
--- consumer ---
drave.annotation 2 fr 20 étiquettes
[('GN', 'Le chat', 'objet'), ('GV', 'dort', 'predicat')]
consumer_exit=0
5899 annotation.json
  ```

- **bash** `{"command": "cd /tmp && sed -n '1,24p' annotation.json", "description": "Show raw JSON head"}`

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
  {
   "niveau": "mot",
  ```

- **bash** `{"command": "sed -n '1,80p' docs/produit/exemples.md; echo ===; sed -n '1,120p' tools/revue_documentation.py", "description": "Read example doc and review tool"}`

  ```
# Dix exemples d'analyse, commentés

> **Ce que ce document est.** Dix exécutions **réelles** du produit, avec leur JSON commenté. Il
> complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
> *comment lire* ce qui sort. Les **cinq premiers blocs** ont été produits le **2026-11-06** sur
> la branche `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et
> sans réseau ; ils ont été **rejoués le 2026-11-14** sur le code courant — F1 **0,7902**,
> attachement **238/238 labels** (238/239 cibles), schéma **v2**. Le format v2 ajoute
> `version: 2` et, sur un syntagme qui chevauche un autre, `meta.partition`/`meta.alternative` ;
> v1 reste lue ([schéma v2](../../tools/schemas/drave-annotation-v2.json)).
>
> **Les cinq blocs du 15/11.** Trois exécutions avec `--tagger` (§ 6) et deux avec `--reel`
> (§ 7), produites le **2026-11-15** avec la **clé DeepSeek** et un **cache disque neuf** : le
> coût affiché est donc réel (`réseau=1`, tokens non nuls). Le tagger ne change que le **POS** ;
> les syntagmes, rôles et attachements restent à l'heuristique. La base `--reel` est la **base
> honnête** : 452 phrases réelles (main + corpus),
… [8622 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff 7f1519f7^ 7f1519f7 -- docs/pilotage/en-cours.md | head -120", "description": "See T1-T2 en-cours update"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 85803db9..aef31600 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 15 h 05 HNE (clôture : le plan et le protocole or-roles committés)**
+**Mis à jour : 2026-11-15, 22 h 03 HNE (T2 : l'API du JSON)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -86,9 +86,9 @@
 
 - **S — les structures** : 61/61 types, 144/144 rôles ; **19/19 verdicts `389b99f`** ; [v2](../../reports/rapport-coordination-s-v2.md).
 - **N2 — en pause** : commande **`eval_longueurs.py --rope --val <dir>`** (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
-- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.
… [2641 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff 7f1519f7^ 7f1519f7 -- journal/2026-11-15/docs.md journal/2026-11-15/README.md | head -120; echo ===; tail -20 journal/2026-11-15/docs.md", "description": "See journal updates for T1-T2"}`

  ```
diff --git a/journal/2026-11-15/README.md b/journal/2026-11-15/README.md
index 56c740f8..bb1d9cda 100644
--- a/journal/2026-11-15/README.md
+++ b/journal/2026-11-15/README.md
@@ -5,13 +5,13 @@
 > le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
 > [l'index des sessions](../README.md#sessions).
 
-**46 commits** · **1 session(s)** · **7 thème(s)**
+**47 commits** · **1 session(s)** · **7 thème(s)**
 
 ## Thèmes du jour
 
 | thème | commits | fichier |
 |---|---|---|
-| distribue | 7 | [distribue.md](distribue.md) |
+| distribue | 8 | [distribue.md](distribue.md) |
 | docs | 13 | [docs.md](docs.md) |
 | memoire | 3 | [memoire.md](memoire.md) |
 | mesures | 17 | [mesures.md](mesures.md) |
@@ -23,7 +23,7 @@
 
 | session | titre | début | durée | liens |
 |---|---|---|---|---|
-| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 358.4 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |
+| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 
… [4352 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"INDEX\\|README\" tools/revue_documentation.py | head -20; ls reports/INDEX.md reports/README.md 2>/dev/null; head -30 reports/INDEX.md 2>/dev/null", "description": "Check reports index requirements"}`

  ```
68:            if "archive" not in p.parts and p.name != "README.md" and not est_carte(p)]
82:            + [RACINE / "docs/README.md", RACINE / "README.md",
89:            + [RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])
97:               RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])
169:    if not (RACINE / "reports/README.md").exists():
170:        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")
264:        idx_cartes = RACINE / "docs/theorie/glossaire/README.md"
266:            alertes.append("glossaire : docs/theorie/glossaire/README.md manque")
271:                    alertes.append(f"glossaire : {c.name} n'est pas listé dans glossaire/README.md")
reports/INDEX.md
reports/README.md
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **756 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [
… [2726 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' tools/verifie_etat_a_jour.py", "description": "Read state freshness hook"}`

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
… [5141 caractères tronqués]
  ```

- **bash** `{"command": "cat /tmp/qs2-clone.log; echo \"---\"; cat /tmp/qs-clone.log; echo \"---install head---\"; sed -n '1,20p' /tmp/qs2-install.log", "description": "Read clone and install logs"}`

  ```
Cloning into '/tmp/qs-drave2'...
---
Cloning into '/tmp/qs-drave'...
---install head---
Obtaining file:///tmp/qs-drave2
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
  Created wheel for drave: filename=drave-0.1.0-0.editable-py3-none-any.whl size=2895 sha256=b43c7e56add472503d7110cb5269a7768df816c8f36e93a9828c78b15c7c3b63
  Stored in directory: /tmp/pip-ephem-wheel-cache-k6rywzaw/wheels/9a/20/5e/d29a437c59cc2e5f19389285b9e71e4c0b3d098181931948e8
Successfully built drave
Installing collected packages: drave
Successfully installed drave-0.1.0

[notice] A new release o
… [85 caractères tronqués]
  ```

- **bash** `{"command": "set -e\nrm -rf /tmp/qs-doc /tmp/qs-doc-home\nmkdir -p /tmp/qs-doc /tmp/qs-doc-home\ncd /tmp/qs-doc\nT0=$(date +%s%N)\ngit clone https://github.com/stephanedenis/drave.git > /tmp/qs-doc-clone.log 2>&1\ncd drave\nT1=$(date +%s%N)\npython3 -m venv .venv\nT2=$(date +%s%N)\nsource .venv/bin/ … [567 caractères tronqués]`

  ```
clone 6.71 s
venv 3.58 s
install 3.35 s
total 13.64 s
7f1519f749ab0939ad24b642abe785e7ab0aa87a

[notice] A new release of pip is available: 26.2.1 -> 26.3
[notice] To update, run: pip install --upgrade pip
  ```

- **bash** `{"command": "cd /tmp/qs-doc/drave && source .venv/bin/activate && export HOME=/tmp/qs-doc-home\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\nrun() { echo \"### CMD: $*\"; \"$@\" > /tmp/qs-doc-out.txt 2> /tmp/qs-doc-err.txt; c=$?; echo \"### EXIT: $c\"; echo \"### STDOUT:\"; cat … [245 caractères tronqués]`

  ```
### CMD: drave --version
### EXIT: 0
### STDOUT:
drave 0.1.0
### STDERR:
### END
### CMD: drave analyser Le chat dort.
### EXIT: 0
### STDOUT:
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
### STDERR:
### END
### CMD: drave evaluer
### EXIT: 0
### STDOUT:
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
SYNTAGMES   F1 81.88 %  (P 86.64 % / R 77.62 %)
  tête      F1 90.83 %  (P 96.11 % / R 86.10 %)
  vue linéaire (partition filtrer) F1 81.88 %  · attachement 93.72 % de couverture
BASE RÉELLE (hand + reel, 452 phras
… [396 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qs-doc/drave && source .venv/bin/activate && export HOME=/tmp/qs-doc-home\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\nset +e\ndrave analyser \"Le chat dort.\" --json > annotation.json; echo \"save_exit=$?\"\nsed -n '1,24p' annotation.json\necho \"--- cons … [410 caractères tronqués]`

  ```
save_exit=0
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
  {
   "niveau": "mot",
--- consumer ---
drave.annotation 2 fr 20 étiquettes
[('GN', 'Le chat', 'objet'), ('GV', 'dort', 'predicat')]
consumer_exit=0
5899 annotation.json
  ```

- **bash** `{"command": "cd /tmp/qs-doc/drave && source .venv/bin/activate && export HOME=/tmp/qs-doc-home\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\nrun() { echo \"### CMD: $*\"; \"$@\" > /tmp/qs-doc-out.txt 2> /tmp/qs-doc-err.txt; c=$?; echo \"### EXIT: $c\"; echo \"### STDOUT:\"; cat … [266 caractères tronqués]`

  ```
### CMD: drave analyser Le chat dort. --tagger
### EXIT: 4
### STDOUT:
### STDERR:
drave: dépendance absente : clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans ~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.
### END
### CMD: drave analyser Le chat dort. --tagger auto
### EXIT: 0
### STDOUT:
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
### STDERR:
drave: tagger auto · heuristique (clé absente)
### END
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"cache\" tools/llm/deepseek.py tools/drave.py | grep -i \"path\\|dir\\|fichier\\|~\" | head -20; find /home/stephane/.cache -maxdepth 2 -iname '*drave*' -o -iname '*deepseek*' 2>/dev/null | head", "description": "Find tagge … [18 caractères tronqués]`

  ```
tools/llm/deepseek.py:128:                 modele: str | None = None, cache_dir: str | pathlib.Path | None = None,
tools/llm/deepseek.py:137:        self.cache_dir = pathlib.Path(cache_dir or os.environ.get("DEEPSEEK_CACHE")
tools/llm/deepseek.py:152:        chemin = self.cache_dir / f"{cle}.json"
tools/llm/deepseek.py:168:            self.cache_dir.mkdir(parents=True, exist_ok=True)
tools/llm/deepseek.py:169:            (self.cache_dir / f"{cle}.json").write_text(json.dumps({
  ```

- **bash** `{"command": "sed -n '130,145p' /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/llm/deepseek.py", "description": "Read cache dir default"}`

  ```
essais: int = 3) -> None:
        self.cle = cle if cle is not None else _cle_env()
        self.base_url = (base_url or os.environ.get("DEEPSEEK_BASE_URL")
                         or os.environ.get("DSH_BASE_URL")
                         or BASE_DEFAUT).rstrip("/")
        self.modele = (modele or os.environ.get("DEEPSEEK_MODEL")
                       or os.environ.get("DSH_MODEL") or MODELE_DEFAUT)
        self.cache_dir = pathlib.Path(cache_dir or os.environ.get("DEEPSEEK_CACHE")
                                      or CACHE_DEFAUT)
        self.transport = transport or _http
        self.sleep = sleep
        self.timeout = timeout
        self.essais = max(1, essais)

    # ------------------------------------------------------------------
    def disponible(self) -> bool:
  ```

- **bash** `{"command": "grep -n \"CACHE_DEFAUT\" /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/llm/deepseek.py", "description": "Find cache default path"}`

  ```
44:CACHE_DEFAUT = RACINE / "data" / "deepseek" / "cache"
138:                                      or CACHE_DEFAUT)
  ```

- **bash** `{"command": "cd /tmp/qs-doc/drave && source .venv/bin/activate\nexport HOME=/home/stephane\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\ntimeout 60 drave analyser \"Le chat dort.\" --tagger > /tmp/qs-doc-tagger-out.txt 2> /tmp/qs-doc-tagger-err.txt; c=$?\necho \"EXIT=$c\"; echo … [179 caractères tronqués]`

  ```
EXIT=0
=== STDOUT ===
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=0.9 s
=== STDERR ===
  ```

- **bash** `{"command": "cd /tmp/qs-doc/drave && source .venv/bin/activate\nexport HOME=/home/stephane\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\ntimeout 30 drave analyser \"Le chat dort.\" --tagger > /tmp/qs-doc-tagger2-out.txt 2>&1; c=$?\necho \"EXIT=$c\"; tail -2 /tmp/qs-doc-tagger2- … [69 caractères tronqués]`

  ```
EXIT=0
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=0 · cache=1 · tokens=0 · latence=0.0 s
  ```

- **bash** `{"command": "cd /tmp/qs-doc/drave && source .venv/bin/activate && export HOME=/tmp/qs-doc-home\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\nrun() { echo \"### CMD: $*\"; \"$@\" > /tmp/qs-doc-out.txt 2> /tmp/qs-doc-err.txt; c=$?; echo \"### EXIT: $c\"; echo \"### STDOUT:\"; cat … [262 caractères tronqués]`

  ```
### CMD: drave analyser 
### EXIT: 3
### STDOUT:
### STDERR:
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
### END
### CMD: drave analyser --fichier absent.txt
### EXIT: 1
### STDOUT:
### STDERR:
drave: erreur : FileNotFoundError : [Errno 2] No such file or directory: 'absent.txt'
### END
### CMD: drave analyser Le chat dort. --langue de
### EXIT: 2
### STDOUT:
### STDERR:
usage: drave analyser [-h] [--partition {brut,alternative,filtrer_union,filtrer}] [--fichier CHEMIN]
                      [--jsonl] [--contexte CONTEXTE] [--langue {fr,en}] [--tagger] [--json]
                      [TEXTE]
drave analyser: erreur d'usage : argument --langue: invalid choice: 'de' (choose from 'fr', 'en')
### END
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py rejouer \"Le chat dort.\"; echo ===; cd /tmp/qs-doc/drave && source .venv/bin/activate && HOME=/tmp/qs-doc-home drave rejouer \"Le chat dort.\"", "description": "Compare rejouer local vs clone"}`

  ```
rejeu identique : oui
  texte      : 'Le chat dort.'
  langue     : fr
  étiquettes : 20
  JSON       : 4390 octets · sha256 f6355d8175a75854…
===
rejeu identique : oui
  texte      : 'Le chat dort.'
  langue     : fr
  étiquettes : 20
  JSON       : 4217 octets · sha256 2577786670e5752c…
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,140p' tools/taille_documents.py", "description": "Read document size budget"}`

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
… [4863 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re,pathlib\nfor p in ['docs/README.md','docs/produit/README.md','docs/pilotage/en-cours.md']:\n    t=pathlib.Path(p).read_text()\n    print(p, len(re.findall(r'\\S+',t)))\nEOF", "description": "Check current … [14 caractères tronqués]`

  ```
docs/README.md 995
docs/produit/README.md 9211
docs/pilotage/en-cours.md 1629
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Produit\\|produit/README\\|produit/exemples\" docs/README.md; sed -n '105,125p' docs/README.md", "description": "Inspect product table in docs README"}`

  ```
92:## Produit — ce qui s'utilise aujourd'hui
96:| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte avec Drave |
97:| [`produit/README.md` § 8](produit/README.md#8-faq--dix-questions) | la **FAQ** : dix questions vérifiées contre le code |
98:| [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels (entrée → sortie), dont un cas d'échec connu |
| [`archive/README.md`](archive/README.md) | les plans, notes et études de 2026-09/10, hors chargement |

## La règle de rangement

`docs/` = **méthode, pilotage, théorie, implantation** ; `reports/` = **résultats** ; `journal/` = **récit daté** ;
`data/` = **[corpus](theorie/glossaire/entrees/corpus.md)**. Une page de `docs/` qui se remplit de tableaux de mesures déménage dans `reports/`.
Les **plans et notes datés** vivent dans [`archive/`](archive/README.md), **facultatifs** ; la feuille de route est
[`pilotage/roadmap.md`](pilotage/roadmap.md).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '140,360p' tools/revue_documentation.py", "description": "Read review checks in detail"}`

  ```
m = re.search(r"Mis à jour : (\d{4}-\d\d-\d\d)", t)
    if not m:
        alertes.append("fraîcheur : en-cours.md n'a pas de date « Mis à jour : AAAA-MM-JJ »")
    else:
        page, dernier = m.group(1), date_dernier_commit()
        if dernier and page != dernier:
            alertes.append(
                f"fraîcheur : en-cours.md dit {page}, le dernier commit date du {dernier}"
            )
    retard = retards(RACINE)
    if retard and not etat_modifie(RACINE):
        etat, _fait, lignes = retard
        if etat == "absent":
            alertes.append("fraîcheur : en-cours.md n'a jamais été commité")
        else:
            alertes.append(
                f"fraîcheur : {len(lignes)} fait(s) commité(s) après le dernier état "
                f"({etat[1]}) — mettre en-cours.md à jour"
            )

    # 1. classement : aucune donnée de résultat dans docs/
    for f in (RACINE / "docs").rglob("*"):
        if f.suffix in (".json", ".csv", ".npz", ".jsonl") and f.is_file():
            if f.name == "index.json" and f.parent.name == "glossaire":
                continue
            alertes.append(f"classement : donnée de résultat dans docs/ → {f.relative_to(RACINE)}")
    f
… [9172 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys,pathlib\nsys.path.insert(0,'tools')\nimport revue_documentation as r\nprint('docs',r.compte_docs())\nprint('fiches',r.compte_fiches())\nprint('json',r.compte_json())\nprint('portes',r.compte_portes())\nE … [47 caractères tronqués]`

  ```
docs 124
fiches 761
json 855
portes 85
  ```

- **todo_write** `{"todos": [{"content": "Rejouer le parcours complet dans un clone propre (clone, venv, install, 3 commandes, JSON, tagger, erreurs)", "status": "completed"}, {"content": "Écrire docs/produit/demarrage.md avec les sorties réelles", "status": "in_progress"}, {"content": "Ajouter les liens dans docs/pr … [276 caractères tronqués]`

  ```
Updated todo list: 3 pending, 1 in progress, 1 completed.
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md", "content": "# Démarrage en 5 minutes\n\n> **Ce que ce document est.** Le parcours le plus court pour installer **drave** et lancer\n> trois commandes. Il part d'un **clone public** et ne suppose aucun fichier  … [10368 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cat /tmp/qs-doc-clone.log; echo \"---\"; grep -n \"Successfully installed\" /tmp/qs-doc-install.log", "description": "Check exact clone and install output"}`

  ```
Cloning into 'drave'...
---
17:Successfully installed drave-0.1.0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '20,42p' docs/produit/README.md; echo ===; sed -n '920,950p' docs/produit/README.md; echo ===; sed -n '92,100p' docs/README.md; echo ===; sed -n '1,20p' .gitignore", "description": "Read insertion contexts"}`

  ```
> **06/11**, et l'`evaluer` du § 3.3 a été relancé le **14/11** (gold vivant 612, `--par-langue
> fr/en`). Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
> La **FAQ** (§ 8) est vérifiée à part le **2026-11-15** par
> [`tools/verifier_faq.py`](../../tools/verifier_faq.py) : **10/10** réponses.
>
> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
> candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.

## Sommaire

- [1. À qui s'adresse le produit](#1-à-qui-sadresse-le-produit)
- [2. Ce que le produit fait](#2-ce-que-le-produit-fait)
- [3. Comment l'utiliser — cinq exemples réels](#3-comment-lutiliser--cinq-exemples-réels)
- [4. Ce que le produit ne fait pas encore](#4-ce-que-le-produit-ne-fait-pas-encore)
- [5. Performance](#5-performance)
- [6. Garanties](#6-garanties)
- [7. Le CLI livré — contrat et manques](#7-le-cli-livré--contrat-et-manques)
- [**8. FAQ — dix questions**](#8-faq--dix-questions)
- [9. Où aller ensuite](#9-où-aller-ensuite)

## 1. À qui s'adresse le produ
… [3400 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,\n> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses\n> cand … [568 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "| si vous voulez… | allez à |\n|---|---|\n| **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |", "new_string": "| si vous voulez… | allez à |\n|---|---|\n| **installer et lancer en 5 min … [108 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "old_string": "| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte avec Drave |\n| [`produit/README.md` § 8](produit/README.md#8-faq--dix-questions) | la **FAQ** : dix questions vérifi … [553 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore", "old_string": "__pycache__/\n*.pyc\n*.egg-info/", "new_string": "__pycache__/\n*.pyc\n.venv/\n*.egg-info/"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 40}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "offset": 88, "limit": 18}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore", "limit": 12}`

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
8: > **Vérifié le 2026-11-14** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
9: > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
10: > existent, et la
11: > porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
12: > § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le
13: > **prototype `--tagger auto`** (complété le **2026-11-15**, § 3.7) choisit l'API si une clé
14: > existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
15: > Le format
16: > est **version 2** (`schema: "drave.annotation"`,
17: > `version: 2`) : le schéma v2 ajoute `met
… [1572 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md</path>
<type>file</type>
<content>
88: | [`implantation/llm-externe.md`](implantation/llm-externe.md) | le [banc externe](theorie/glossaire/entrees/banc-externe.md), le [professeur](theorie/glossaire/entrees/professeur.md) et l'[élève](theorie/glossaire/entrees/eleve.md) |
89: | [`implantation/numa-segregation.md`](implantation/numa-segregation.md) | la ségrégation [NUMA](theorie/glossaire/entrees/numa.md) mesurée |
90: | [`implantation/configuration-nvme-raid-amd.md`](implantation/configuration-nvme-raid-amd.md) | l'array [NVMe](theorie/glossaire/entrees/nvme-ssd-odirect-pread.md) et le pari AMD |
91: 
92: ## Produit — ce qui s'utilise aujourd'hui
93: 
94: | document | pour quoi |
95: |---|---|
96: | [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte avec Drave |
97: | [`produit/README.md` § 8](produit/README.md#8-faq--dix-questions) | la **FAQ** : dix questions vérifiées contre le code |
98: | [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels (entrée → sortie), dont un cas d'échec connu |
99: 
100: ## Transversal et archive
101: 
102: | document | pour quoi |
1
… [287 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore</path>
<type>file</type>
<content>
1: __pycache__/
2: *.pyc
3: *.egg-info/
4: /build/
5: /dist/
6: reports/*.tmp
7: models/
8: data/
9: qtrinet-core/target/
10: 
11: # Traces de session : la copie brute reste sur disque (volumineuse, binaire),
12: # le digest markdown est versionné.

(Showing lines 1-12 of 26. Use offset=13 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,\n> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses\n> cand … [568 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| si vous voulez… | allez à |\n|---|---|\n| **installer et lancer en 5 minutes** | [`demarrage.md`](demarrage.md) |\n| **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |", "old_string":  … [108 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "new_string": "| [`produit/demarrage.md`](produit/demarrage.md) | le **quickstart** : cinq minutes, trois commandes |\n| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte |\n| [`produi … [553 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore", "new_string": "__pycache__/\n*.pyc\n.venv/\n*.egg-info/", "old_string": "__pycache__/\n*.pyc\n*.egg-info/"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re,pathlib\nt=pathlib.Path('docs/README.md').read_text()\nprint(len(re.findall(r'\\S+',t)))\nEOF\ngrep -n \"demarrage\" docs/README.md docs/produit/README.md", "description": "Check docs README word count an … [9 caractères tronqués]`

  ```
997
docs/README.md:96:| [`produit/demarrage.md`](produit/demarrage.md) | le **quickstart** : cinq minutes, trois commandes |
docs/produit/README.md:30:> JSON, tagger optionnel et erreurs — est dans [`demarrage.md`](demarrage.md).
docs/produit/README.md:929:| **installer et lancer en 5 minutes** | [`demarrage.md`](demarrage.md) |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re,pathlib\nt=pathlib.Path('docs/produit/demarrage.md').read_text()\nprint('mots',len(re.findall(r'\\S+',t)),'lignes',t.count(chr(10))+1)\nEOF", "description": "Count quickstart words"}`

  ```
mots 1539 lignes 282
  ```

- **write** `{"content": "# Démarrage en 5 minutes\n\n> **Ce que ce document est.** Le parcours le plus court pour installer **drave** et lancer\n> trois commandes. Il part d'un **clone public** et ne suppose aucun fichier du dépôt de\n> développement. Chaque commande et chaque sortie ont été **rejouées le 2026- … [8867 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re,pathlib\nt=pathlib.Path('docs/produit/demarrage.md').read_text()\nprint('mots',len(re.findall(r'\\S+',t)),'lignes',t.count(chr(10))+1)\nEOF", "description": "Count trimmed quickstart"}`

  ```
mots 1300 lignes 245
  ```

- **bash** `{"command": "cd /tmp/qs-doc/drave && source .venv/bin/activate && HOME=/tmp/qs-doc-home drave analyser \"Le chat dort.\" --json > /tmp/ann.json && sed -n '1,22p' /tmp/ann.json | nl -ba | tail -5", "description": "Verify 22-line JSON excerpt"}`

  ```
18	   "candidats": [],
    19	   "langue": "fr",
    20	   "script": "Latn",
    21	   "meta": {}
    22	  },
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md", "new_string": "**Texte vide → code 3.**\n\n```bash\ndrave analyser \"\"\n```\n\n```text\ndrave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)\n```\n\nUn refus est une **répo … [1537 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md has been updated successfully.
  ```

- **bash** `{"command": "cd /tmp/qs-doc/drave && git submodule update --init tools/structures > /tmp/qs-sub-out.txt 2> /tmp/qs-sub-err.txt; c=$?; echo \"EXIT=$c\"; echo \"OUT:\"; cat /tmp/qs-sub-out.txt; echo \"ERR:\"; cat /tmp/qs-sub-err.txt; echo \"--- .gitmodules ---\"; cat .gitmodules", "description": "Test … [41 caractères tronqués]`

  ```
EXIT=1
OUT:
ERR:
Submodule 'tools/structures' (/home/stephane/Data13TB/stephane/GitHub/drave-structures) registered for path 'tools/structures'
Cloning into '/tmp/qs-doc/drave/tools/structures'...
fatal: transport 'file' not allowed
fatal: clone of '/home/stephane/Data13TB/stephane/GitHub/drave-structures' into submodule path '/tmp/qs-doc/drave/tools/structures' failed
Failed to clone 'tools/structures'. Retry scheduled
Cloning into '/tmp/qs-doc/drave/tools/structures'...
fatal: transport 'file' not allowed
fatal: clone of '/home/stephane/Data13TB/stephane/GitHub/drave-structures' into submodule path '/tmp/qs-doc/drave/tools/structures' failed
Failed to clone 'tools/structures' a second time, aborting
--- .gitmodules ---
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
  ```

- **bash** `{"command": "git --version; cd /tmp/qs-doc/drave && . .venv/bin/activate && python --version && python -m pip --version", "description": "Get tool versions"}`

  ```
git version 2.56.0
Python 3.13.16
pip 26.2.1 from /tmp/qs-doc/drave/.venv/lib64/python3.13/site-packages/pip (python 3.13)
  ```

- **write** `{"content": "# T3 — le démarrage en 5 minutes : clone public, installation, trois commandes, JSON, tagger, erreurs\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T3** (exploitable, 3/5) ·\n> **Date** : 2026-11-15 · **Verdict** : ✅ **quickstart livré et rejoué** ; ⚠️ le **clone\n> publ … [12893 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-quickstart.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\n\nanalyser = \"\"\"drave 0.1.0 — analyse heuristique (CPU, hors ligne)\nlangue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN d … [9255 caractères tronqués]`

  ```
reports/quickstart.json 8311
JSON-OK
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Current date and time"}`

  ```
2026-11-15 22:26 EST
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 12}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 84, "limit": 22}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 22 h 03 HNE (T2 : l'API du JSON)**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
11: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
12: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.

(Showing lines 1-12 of 145. Use offset=13 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
84: 
85: ## Ce qui est en cours
86: 
87: - **S — les structures** : 61/61 types, 144/144 rôles ; **19/19 verdicts `389b99f`** ; [v2](../../reports/rapport-coordination-s-v2.md).
88: - **N2 — en pause** : commande **`eval_longueurs.py --rope --val <dir>`** (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
89: - **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md). **T2** : **2 139** objets ; rôles **21 → 8** ; [fiche](../../reports/rapport-contrat-json.md), [JSON](../../reports/contrat-json.json).
90: - **L — le bloc langue** : contrat ; frontière script 1,0 / langue 0,137/0,9687 ; fusion réparée **0,9309/0,8226/0,8784/0,9954**.
91: - **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,684
… [1616 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"T1\\|T2\\|T3\" docs/pilotage/en-cours.md", "description": "Find T1/T2/T3 in state"}`

  ```
3:**Mis à jour : 2026-11-15, 22 h 03 HNE (T2 : l'API du JSON)**
67:- **Prochaine action** : **J4 — l'or de rôles** (seconds cadres, rôles hors cadre) ; T132/T133, gold de pensée.
89:- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md). **T2** : **2 139** objets ; rôles **21 → 8** ; [fiche](../../reports/rapport-contrat-json.md), [JSON](../../reports/contrat-json.json).
117:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit (J11)** | **`g017` tranché** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
127:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold de pensée, **J4 — or de rôles** (seconds cadres) ; **S** — page `/` : décision et recette (106/41), référents ; **Panini** — les 26 signatures V14, puis le test à date contrôlée ; **R0.7** — `auto` prototype livré 
… [108 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport revue_documentation as r\nprint(r.compte_docs(), r.compte_fiches(), r.compte_json())\nEOF", "description": "Check counters after adding files"}`

  ```
125 762 856
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 10, "offset": 101}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
101: | invariant | valeur | contrôle |
102: |---|---|---|
103: | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
104: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
105: | fichiers / JSON de résultats | **761** / **855** | `reports/*.md` / `reports/*.json` |
106: | documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
107: | dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |
108: 
109: ## Les chantiers et leurs bloquants
110: 

(Showing lines 101-110 of 145. Use offset=111 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 22 h 26 HNE (T3 : le démarrage en 5 minutes)**", "old_string": "**Mis à jour : 2026-11-15, 22 h 03 HNE (T2 : l'API du JSON)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), … [1086 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **762** / **856** | `reports/*.md` / `reports/*.json` |\n| documents de `docs/` | **125** (hors archive et README) | `docs/**/*.md` |", "old_string": "| fichiers … [158 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -30; echo ===; tail -8 journal/2026-11-15/docs.md; echo ===; grep -n \"T1/T2\" journal/2026-11-15/docs.md journal/2026-11-15/README.md", "description": "Inspect journal status and end"}`

  ```
M .gitignore
 M docs/README.md
 M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f/digest.md
 M journal/sessions/session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? docs/produit/demarrage.md
?? journal/sessions/session-698e0dda-697b-48fd-9006-61bed3c300e3/
?? reports/quickstart.json
?? reports/rapport-quickstart.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
===

### W5 — l'état et la roadmap après la restitution v3

`docs/pilotage/en-cours.md` passe à **753** fichiers / **846** JSON, la session Pensée reçoit
W5 (gold v2 **20/46**, F1 **0,5406** ; gold S **144/144**, cinq rô
… [334 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md", "limit": 35, "offset": 160}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md</path>
<type>file</type>
<content>
160: (**0,064315 $** en pointe), à comparer aux **0,065359 $** de la référence `0,04 $/612` — la
161: référence était à deux appels par phrase, le câblage actuel en fait un. À chaud : **0 réseau,
162: 0 token, 0 $**, **2,635 s**, **22 770 items/min**, **1 000/1 000 hashes identiques**. `--jsonl`
163: rend **1 003 lignes** (3 phrases du gold contiennent deux phrases) ; le second passage chaud est
164: **0 réseau / 0 token**.
165: [`fiche`](../../reports/rapport-tagger-lot.md) · [`JSON`](../../reports/rapport-tagger-lot.json).
166: 
167: ### T1/T2 — le produit exploitable : l'empaquetage, puis l'API du JSON
168: 
169: **T1** rend le produit installable : `pyproject.toml` (nom `drave`, version **0.1.0**, zéro
170: dépendance d'exécution, script `drave = tools.drave:main`) ; `pip install -e .` dans
171: `/tmp/venv-drave` rend **0**, `drave --version` et `drave analyser "Le chat dort."` passent
172: depuis `/tmp`, et sans installation la commande échoue proprement (**127**). **8 tests.**
173: 
174: **T2** ouvre l'API du JSON. Les candidats d'attachement deviennent des **
… [873 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md", "new_string": "[`fiche T1`](../../reports/rapport-empaquetage.md) · [`fiche T2`](../../reports/rapport-contrat-json.md) ·\n[`JSON T2`](../../reports/contrat-json.json).\n\n### T3 — le démarrage en 5 minutes … [1053 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py > /tmp/revue-t3.txt 2>&1; c=$?; echo \"EXIT=$c\"; cat /tmp/revue-t3.txt", "description": "Run documentation review", "timeoutMs": 120000}`

  ```
EXIT=0
  revue de documentation · 762 fiche(s) · 856 JSON · 125 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py > /tmp/taille-t3.txt 2>&1; c=$?; echo \"TAILLE_EXIT=$c\"; tail -20 /tmp/taille-t3.txt; echo ===; python3 tools/verifie_en_cours.py > /tmp/encours-t3.txt 2>&1; c=$?; echo \"ENCOURS_EXIT=$c\"; cat /tmp … [224 caractères tronqués]`

  ```
TAILLE_EXIT=1
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2733    231   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4041 mots (budget 4 000)

  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md
… [419 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -30 /tmp/taille-t3.txt", "description": "Read size report head"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    9000    493   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2733    231   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [519 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '140,240p' tools/taille_documents.py", "description": "Read T0 budget calculation"}`

  ```
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
    lignes.sort(reverse=True)
    print("  budget de contexte · documents chargeables")
    print(f"  {'mots':>6} {'lignes':>6} {'cat':>4} {'budget':>6}  document")
    for n, l, rel, cat, budget in lignes[:18]:
        print(f"  {n:6d} {l:6d} 
… [524 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), … [1214 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).", "old_string": "> **État courant, pas histoire** : une sous-section par **sessi … [68 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.\n- **Prochaine action** : **suivi docs**, puis la **passe**.\n- **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée  … [292 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py > /tmp/taille-t3b.txt 2>&1; c=$?; echo \"TAILLE_EXIT=$c\"; tail -8 /tmp/taille-t3b.txt; echo ===; python3 tools/verifie_en_cours.py | tail -3", "description": "Re-run size and state checks", "timeout … [12 caractères tronqués]`

  ```
TAILLE_EXIT=1
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4001 mots (budget 4 000)

  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4001 mots (AGENTS + en-cours + une tâche) > budget 4 000
===
  en-cours · 1631 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T3** : quickstart 5 min, 3/3 ; [fiche](../../reports/rapport-quickstart.md), [JSON](../../reports/quickstart.json).", "old_string": "**T3** : quickstart 5 min, 3/3 commandes ; [fiche](../../re … [70 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py > /tmp/taille-t3c.txt 2>&1; c=$?; echo \"TAILLE_EXIT=$c\"; tail -5 /tmp/taille-t3c.txt", "description": "Confirm size budget", "timeoutMs": 120000}`

  ```
TAILLE_EXIT=0

  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py > /tmp/revue-t3b.txt 2>&1; c=$?; echo \"REVUE_EXIT=$c\"; cat /tmp/revue-t3b.txt; echo ===; bash tools/porte-tableaux.sh > /tmp/tableaux-t3.txt 2>&1; c=$?; echo \"TABLEAUX_EXIT=$c\"; tail -12 /tmp/ … [85 caractères tronqués]`

  ```
REVUE_EXIT=0
  revue de documentation · 762 fiche(s) · 856 JSON · 125 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
===
TABLEAUX_EXIT=0
  ✅ 1839 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4652 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schemas.py > /tmp/schemas-t3.txt 2>&1; c=$?; echo \"SCHEMAS_EXIT=$c\"; tail -10 /tmp/schemas-t3.txt", "description": "Verify schemas", "timeoutMs": 120000}`

  ```
SCHEMAS_EXIT=0
  schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-produit.sh tools/tests/test_produit.py tools/tests/test_empaquetage.py 2>/dev/null; python3 tools/tests/test_produit.py 2>&1 | tail -3; echo \"PRODUIT_EXIT=${PIPESTATUS[0]}\"; python3 tools/tests/test_empaquetage.py 2> … [121 caractères tronqués]`

  ```
tools/porte-produit.sh
tools/tests/test_empaquetage.py
tools/tests/test_produit.py
Ran 24 tests in 13.717s

OK
PRODUIT_EXIT=0
Ran 8 tests in 0.527s

OK
EMP_EXIT=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh > /tmp/porte-produit-t3.txt 2>&1; c=$?; echo \"PORTE_PRODUIT_EXIT=$c\"; tail -20 /tmp/porte-produit-t3.txt; echo ===; python3 tools/verifier_schema_produit.py --gold 20 > /tmp/schema-produit-t3.txt 2>&1; c … [151 caractères tronqués]`

  ```
PORTE_PRODUIT_EXIT=0
  ✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f6355d8175a75854 deux fois
  ✅ smoke test : Ran 24 tests
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
===
SCHEMA_PRODUIT_EXIT=0
  ✅ gold:g018 (v2)
  ✅ gold:g019 (v2)
  ✅ gold:g020 (v2)
  ✅ rétro-compatibilité : annotation v1 lue par le schéma v1
  ✅ contrôle négatif : le schéma v2 refuse une annotation v1
  ✅ contrôle négatif : le schéma v2 refuse un rôle hors vocabulaire
  ✅ contrôle négatif : le schéma v2 refuse un candidat chaîne
  ✅ validateur JSON Schema · 26 cas
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/toutes-les-portes.sh; echo ===; cat docs/pilotage/references-non-regression.md | head -60", "description": "Read all-gates script and known reds"}`

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
… [6399 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qs-doc/drave && source .venv/bin/activate && export HOME=/tmp/qs-doc-home\nunset DEEPSEEK_API_KEY DEEPSEEK_KEY_FILE DSH_API_KEY DSH_KEY_FILE\ndrave analyser \"\" --json > /tmp/empty-final.json 2>/tmp/empty-final.err; echo \"EXIT=$?\"; cat /tmp/empty-final.err; python3 - <<'PY'\n … [206 caractères tronqués]`

  ```
EXIT=3
drave.annotation 2 vide 0 0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md</path>
<type>file</type>
<content>
1: # Démarrage en 5 minutes
2: 
3: > **Ce que ce document est.** Le parcours le plus court pour installer **drave** et lancer
4: > trois commandes. Il part d'un **clone public** et ne suppose aucun fichier du dépôt de
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
26: restent absen
… [3869 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md", "limit": 140, "offset": 121}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md</path>
<type>file</type>
<content>
121: ```
122: 
123: ```json
124: {
125:  "schema": "drave.annotation",
126:  "version": 2,
127:  "texte": "Le chat dort.",
128:  "langue": "fr",
129:  "script": "Latn",
130:  "source": "heuristique",
131:  "refus": "",
132:  "etiquettes": [
133:   {
134:    "niveau": "graphème",
135:    "type": "lettres",
136:    "valeur": "Le",
137:    "debut": 0,
138:    "fin": 2,
139:    "source": "heuristique",
140:    "confiance": 0.99,
141:    "candidats": [],
142:    "langue": "fr",
143:    "script": "Latn",
144:    "meta": {}
145:   },
146: ```
147: 
148: Le JSON complet fait **5 899 octets**. Pour le consommer sans dépendance :
149: 
150: ```bash
151: python3 -c 'import json; a=json.load(open("annotation.json")); print(a["schema"], a["version"], a["langue"], len(a["etiquettes"]), "étiquettes"); print([(e["type"], e["valeur"], e["meta"].get("role")) for e in a["etiquettes"] if e["niveau"]=="syntagme"])'
152: ```
153: 
154: ```text
155: drave.annotation 2 fr 20 étiquettes
156: [('GN', 'Le chat', 'objet'), ('GV', 'dort', 'predicat')]
157: ```
158: 
159: Le contrat est **versionné
… [3958 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit add .gitignore docs/README.md docs/pilotage/en-cours.md docs/produit/README.md docs/produit/demarrage.md journal/2026-11-15/README.md reports/quickstart.json reports/rapport-quickstart.md\ngit diff --cached --check; echo \"CHECK_EX … [95 caractères tronqués]`

  ```
CHECK_EXIT=0
 .gitignore                    |   1 +
 docs/README.md                |   7 +-
 docs/pilotage/en-cours.md     |  17 ++-
 docs/produit/README.md        |   4 +
 docs/produit/demarrage.md     | 250 ++++++++++++++++++++++++++++++++++++++++++
 journal/2026-11-15/README.md  |  12 ++
 reports/quickstart.json       | 212 +++++++++++++++++++++++++++++++++++
 reports/rapport-quickstart.md | 236 +++++++++++++++++++++++++++++++++++++++
 8 files changed, 727 insertions(+), 12 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --cached -- docs/pilotage/en-cours.md docs/README.md docs/produit/README.md .gitignore | head -160", "description": "Review staged state and link diffs"}`

  ```
diff --git a/.gitignore b/.gitignore
index 7937dc3f..c03530af 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,5 +1,6 @@
 __pycache__/
 *.pyc
+.venv/
 *.egg-info/
 /build/
 /dist/
diff --git a/docs/README.md b/docs/README.md
index 81e94db9..e55d50ba 100644
--- a/docs/README.md
+++ b/docs/README.md
@@ -93,9 +93,10 @@
 
 | document | pour quoi |
 |---|---|
-| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte avec Drave |
-| [`produit/README.md` § 8](produit/README.md#8-faq--dix-questions) | la **FAQ** : dix questions vérifiées contre le code |
-| [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels (entrée → sortie), dont un cas d'échec connu |
+| [`produit/demarrage.md`](produit/demarrage.md) | le **quickstart** : cinq minutes, trois commandes |
+| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte |
+| [`produit/README.md` § 8](produit/README.md#8-faq--dix-questions) | la **FAQ** : dix questions vérifiées |
+| [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels, dont un échec connu |
 
 ## Transversal et archive
 
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index
… [5714 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 22 h 26 HNE (T3 : le démarrage)**", "old_string": "**Mis à jour : 2026-11-15, 22 h 26 HNE (T3 : le démarrage en 5 minutes)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T3** : quickstart 3/3, clone public dégradé ; [fiche](../../reports/rapport-quickstart.md), [JSON](../../reports/quickstart.json).", "old_string": "**T3** : quickstart 5 min, 3/3 ; [fiche](../ … [75 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py > /tmp/taille-t3d.txt 2>&1; c=$?; echo \"TAILLE_EXIT=$c\"; tail -4 /tmp/taille-t3d.txt; echo ===; python3 tools/revue_documentation.py > /tmp/revue-t3c.txt 2>&1; c=$?; echo \"REVUE_EXIT=$c\"; cat /tm … [83 caractères tronqués]`

  ```
TAILLE_EXIT=0
  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
===
REVUE_EXIT=0
  revue de documentation · 762 fiche(s) · 856 JSON · 125 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md && git diff --cached --check; echo \"CHECK_EXIT=$?\"; git diff --cached --stat", "description": "Restage en-cours and check"}`

  ```
CHECK_EXIT=0
 .gitignore                    |   1 +
 docs/README.md                |   7 +-
 docs/pilotage/en-cours.md     |  17 ++-
 docs/produit/README.md        |   4 +
 docs/produit/demarrage.md     | 250 ++++++++++++++++++++++++++++++++++++++++++
 journal/2026-11-15/README.md  |  12 ++
 reports/quickstart.json       | 212 +++++++++++++++++++++++++++++++++++
 reports/rapport-quickstart.md | 236 +++++++++++++++++++++++++++++++++++++++
 8 files changed, 727 insertions(+), 12 deletions(-)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-quickstart.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-quickstart.md</path>
<type>file</type>
<content>
1: # T3 — le démarrage en 5 minutes : clone public, installation, trois commandes, JSON, tagger, erreurs
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T3** (exploitable, 3/5) ·
4: > **Date** : 2026-11-15 · **Verdict** : ✅ **quickstart livré et rejoué** ; ⚠️ le **clone
5: > public** n'a pas le sous-module `tools/structures`, donc la sortie d'un débutant est
6: > **dégradée** par rapport au dépôt de développement. Le document le dit, mesure l'écart et
7: > donne les deux sorties.
8: >
9: > **Le chiffre.** Sur un clone public neuf (commit **7f1519f**, Python **3.13.16**, pip
10: > **26.2.1**, sans clé) : **3/3 commandes** sortent **0**, le JSON fait **5 899 octets** en
11: > schéma **v2**, `--tagger` sans clé sort **4**, `--tagger auto` sort **0**, et les **3
12: > erreurs** rejouées sortent **3 / 4 / 1**. Clone + venv + installation : **13,64 s** de
13: > machine. Le contrôle négatif « un débutant sans le dépôt » passe pour les commandes, mais
14: > découvre l'écart du sous-module : `analyser` rend `rôle=objet` / `GV → —` au lieu de
15: > `agent` 
… [4996 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-quickstart.md", "limit": 125, "offset": 119}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-quickstart.md</path>
<type>file</type>
<content>
119: ### 3.5 Le tagger optionnel
120: 
121: | cas | commande | code | `stdout` | `stderr` |
122: |---|---|---:|---|---|
123: | **sans clé, explicite** | `drave analyser "Le chat dort." --tagger` | **4** | vide | `drave: dépendance absente : clé DeepSeek absente …` |
124: | **sans clé, auto** | `drave analyser "Le chat dort." --tagger auto` | **0** | identique au § 3.2 | `drave: tagger auto · heuristique (clé absente)` |
125: | **avec clé, explicite** | `drave analyser "Le chat dort." --tagger` | **0** | `source=cascade`, `TAGGER API … réseau=1 · cache=0 · tokens=130 · latence=0.9 s` | vide |
126: | **avec clé, cache chaud** | le même, seconde fois | **0** | `réseau=0 · cache=1 · tokens=0 · latence=0.0 s` | vide |
127: 
128: La clé n'apparaît ni dans `stdout`, ni dans `stderr`, ni dans le JSON. Le mode `auto` ne change
129: jamais le code de sortie (0 dans les deux cas) ; le 4 reste réservé à `--tagger` explicite.
130: 
131: ### 3.6 Les trois erreurs
132: 
133: | cas | commande | code | `stdout` | `stderr` (extrait) |
134: |---|---|---:|---|---|
135: | texte vide | 
… [6893 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-quickstart.md", "new_string": "| clone | `https://github.com/stephanedenis/drave.git`, clone complet (sans `--depth`), **commit 7f1519f** |", "old_string": "| clone | `https://github.com/stephanedenis/drave.git`, `--depth … [36 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-quickstart.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-quickstart.md && git diff --cached --check; echo \"CHECK_EXIT=$?\"; git status --short | sed -n '1,30p'", "description": "Restage report and check status"}`

  ```
CHECK_EXIT=0
M  .gitignore
M  docs/README.md
M  docs/pilotage/en-cours.md
M  docs/produit/README.md
A  docs/produit/demarrage.md
M  journal/2026-11-15/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f/digest.md
 M journal/sessions/session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
A  reports/quickstart.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
A  reports/rapport-quickstart.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? journal/sessions/session-698e0dda-697b-48fd-9006-61bed3c300e3/
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test -f docs/produit/demarrage.md && echo QUICKSTART-OK; python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?; python3 tools/taille_documents.py >/dev/null 2>&1; echo TAILLE-$?; python3 tools/verifie_en_cours.py >/dev/ … [92 caractères tronqués]`

  ```
QUICKSTART-OK
REVUE-0
TAILLE-0
ENCOURS-0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"T3 — LE DÉMARRAGE EN 5 MINUTES : 3/3 COMMANDES REJOUÉES, JSON V2 5 899 OCTETS, TAGGER 4/0, ERREURS 3/4/1 ; LE CLONE PUBLIC SANS tools/structures EST DÉGRADÉ, DOCUMENTÉ\" -m \"Clone public neuf (7f1519f, Python 3.13.16 … [782 caractères tronqués]`

  ```
✅ index : aucun fait stagé sans état
[s/v7 7d114559] T3 — LE DÉMARRAGE EN 5 MINUTES : 3/3 COMMANDES REJOUÉES, JSON V2 5 899 OCTETS, TAGGER 4/0, ERREURS 3/4/1 ; LE CLONE PUBLIC SANS tools/structures EST DÉGRADÉ, DOCUMENTÉ
 23 files changed, 4770 insertions(+), 40 deletions(-)
 create mode 100644 docs/produit/demarrage.md
 create mode 100644 journal/sessions/session-698e0dda-697b-48fd-9006-61bed3c300e3/digest.md
 create mode 100644 journal/sessions/session-698e0dda-697b-48fd-9006-61bed3c300e3/rapport.md
 create mode 100644 reports/quickstart.json
 create mode 100644 reports/rapport-quickstart.md
COMMIT_EXIT=0
7d114559 T3 — LE DÉMARRAGE EN 5 MINUTES : 3/3 COMMANDES REJOUÉES, JSON V2 5 899 OCTETS, TAGGER 4/0, ERREURS 3/4/1 ; LE CLONE PUBLIC SANS tools/structures EST DÉGRADÉ, DOCUMENTÉ
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline 7d114559 | head -40; echo ===; git status --short | head -30", "description": "Inspect commit contents"}`

  ```
7d114559 T3 — LE DÉMARRAGE EN 5 MINUTES : 3/3 COMMANDES REJOUÉES, JSON V2 5 899 OCTETS, TAGGER 4/0, ERREURS 3/4/1 ; LE CLONE PUBLIC SANS tools/structures EST DÉGRADÉ, DOCUMENTÉ
 .gitignore                                         |    1 +
 docs/README.md                                     |    7 +-
 docs/pilotage/en-cours.md                          |   17 +-
 docs/produit/README.md                             |    4 +
 docs/produit/demarrage.md                          |  250 ++
 journal/2026-11-15/README.md                       |   19 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/memoire.md                      |    2 +-
 journal/2026-11-15/mesures.md                      |    2 +-
 journal/2026-11-15/modele.md                       |    2 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    9 +-
 journal/README.md                                  |    5 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   36 +
 .../rapport.md                   
… [875 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py > /tmp/revue-post.txt 2>&1; c=$?; echo \"REVUE_EXIT=$c\"; cat /tmp/revue-post.txt; echo ===; python3 tools/taille_documents.py > /tmp/taille-post.txt 2>&1; c=$?; echo \"TAILLE_EXIT=$c\"; tail -4 / … [348 caractères tronqués]`

  ```
REVUE_EXIT=0
  revue de documentation · 762 fiche(s) · 856 JSON · 125 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
===
TAILLE_EXIT=0
  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
===
ENCOURS_EXIT=0
  en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
===
JOURNAL_EXIT=0
  journal · 47 jour(s) · 219 session(s) · 2668 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD:journal/2026-11-15/README.md | grep -n -A12 \"T3 —\" | head -20", "description": "Verify journal T3 note in commit"}`

  ```
186:### T3 — le démarrage en 5 minutes : rejoué sur un clone public
187-
188-Le quickstart [`docs/produit/demarrage.md`](../../docs/produit/demarrage.md) part d'un clone
189-public neuf, installe dans `.venv` et lance trois commandes ; **3/3** sortent **0**, le JSON
190-fait **5 899 octets** en schéma **v2**, `--tagger` sans clé sort **4**, `auto` sort **0**, et
191-les trois erreurs sortent **3 / 4 / 1**. Le contrôle négatif « débutant sans le dépôt » passe,
192-mais découvre que `tools/structures` (URL locale dans `.gitmodules`) manque à un clone public :
193-`analyser` rend `objet` / `—` au lieu de `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %**
194-au lieu de **79,02 %** / **99,58 %**. Le document affiche la sortie réelle du clone et nomme
195-l'écart ; la correction du sous-module reste à faire.
196-[`fiche`](../../reports/rapport-quickstart.md) · [`JSON`](../../reports/quickstart.json).
197-<!-- /notes -->
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline HEAD | head -30; echo ===; git status --short | head -15", "description": "Final commit and status"}`

  ```
7d114559 T3 — LE DÉMARRAGE EN 5 MINUTES : 3/3 COMMANDES REJOUÉES, JSON V2 5 899 OCTETS, TAGGER 4/0, ERREURS 3/4/1 ; LE CLONE PUBLIC SANS tools/structures EST DÉGRADÉ, DOCUMENTÉ
 .gitignore                                         |    1 +
 docs/README.md                                     |    7 +-
 docs/pilotage/en-cours.md                          |   17 +-
 docs/produit/README.md                             |    4 +
 docs/produit/demarrage.md                          |  250 ++
 journal/2026-11-15/README.md                       |   19 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/memoire.md                      |    2 +-
 journal/2026-11-15/mesures.md                      |    2 +-
 journal/2026-11-15/modele.md                       |    2 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    9 +-
 journal/README.md                                  |    5 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   36 +
 .../rapport.md                   
… [875 caractères tronqués]
  ```

### 🤖 Assistant

**T3 livré et committé** — `7d114559`.

## Ce qui est écrit

- [`docs/produit/demarrage.md`](docs/produit/demarrage.md) : clone public, installation T1, les **trois commandes** (`--version`, `analyser`, `evaluer`), le **JSON** v2 avec consommateur Python, le **tagger optionnel** (`--tagger`, `--tagger auto`), les **trois erreurs courantes** (3 / 4 / 1), le tableau des codes 0–4.
- Liens ajoutés dans [`docs/produit/README.md`](docs/produit/README.md) (en tête + § 9) et [`docs/README.md`](docs/README.md) (table Produit).
- `.venv/` ajouté au [`.gitignore`](.gitignore).
- Fiche [`reports/rapport-quickstart.md`](reports/rapport-quickstart.md) + [`reports/quickstart.json`](reports/quickstart.json).

## Chaque commande rejouée

Clone public neuf (`7f1519f`, Python 3.13.16, pip 26.2.1, sans clé) : clone + venv + install = **13,64 s**. Résultats : `--version` **0**, `analyser` **0**, `evaluer` **0** ; JSON **5 899 octets**, 20 étiquettes, schéma **v2** ; `--tagger` sans clé **4**, `--tagger auto` **0**, avec clé **0** (130 tokens, cache chaud 0) ; erreurs texte vide **3**, fichier absent **1**, `--langue de` **2**.

## Contrôle négatif — et ce qu'il a trouvé

Un débutant sans le dépôt suit bien les 5 minutes : **3/3 commandes passent**, le JSON se consomme, les erreurs sont conformes. Mais le clone public n'a pas `tools/structures` : son URL dans `.gitmodules` est un **chemin local**, et `git submodule update` échoue (`transport 'file' not allowed`). Conséquence mesurée : `analyser` rend `objet` / `—` au lieu de `agent` / `chat`, et `evaluer` **81,88 % / 88,70 %** au lieu de **79,02 % / 99,58 %**. Le quickstart affiche la sortie **réelle du clone** et nomme l'écart ; la correction du sous-module reste à faire (hors T3).

## Vérifications

`QUICKSTART-OK`, `REVUE-0`, `TAILLE-0`, `ENCOURS-0`, `JOURNAL-0`, `porte-produit` verte, `test_produit` 24/24, `test_empaquetage` 8/8, schéma 26 cas OK.

