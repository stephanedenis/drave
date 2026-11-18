# Session DSH — relecture

- identifiant : `8c024745-95cb-4885-9d0b-865142606b6d`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-18 08:58:22
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français). La machine est dédiée : 2 GPU Quadro RTX 5000 libres, 40 threads.

TÂCHE : mesurer la GRAMMATICALITÉ du modèle natif de 100 M (work/n2ac/mix1024-100m.pt) avec le banc existant, et comparer au 34 M déjà mesuré.

Étapes :
1. Lis reports/rapport-grammaticalite*.md (ou le rapport qui porte le banc de grammaticalité) et tools/banc_grammaticalite.py pour retrouver le protocole exact (les prompts, les réglages, les métriques GV/ciment, le contrôle négatif).
2. Regarde le JSON de référence (reports/banc-grammaticalite*.json) et les commandes qui l'ont produit.
3. Lance le banc sur work/n2ac/mix1024-100m.pt avec le MÊME protocole. Si le script n'a pas d'option --device et que le CPU est trop lent, ajoute --device (comme tools/banc_generation.py l'a fait : charger(chemin, device="cpu"), modèle .to(device), tenseurs sur le device) — c'est la seule modification de code autorisée, et elle doit rester compatible avec l'usage existant.
4. Écris reports/banc-grammaticalite-100m.json (le JSON du banc) et reports/rapport-grammaticalite-100m.md : le tableau 34 M vs 100 M, le contrôle (aléatoire si le protocole le prévoit), les limites (prompts, longueur, une graine).

CONTRAINTES STRICTES :
- ne touche pas à docs/pilotage/en-cours.md, docs/pilotage/roadmap.md, AGENTS.md ;
- ne committe pas ;
- n'écris que reports/banc-grammaticalite-100m.json, reports/rapport-grammaticalite-100m.md et (si nécessaire) tools/banc_grammaticalite.py ;
- utilise /home/stephane/gpu-env/bin/python (torch+cu130) ;
- GPU : utilise cuda:0 ; si un autre processus occupe, prends cuda:1.

Rends à la fin : les chiffres clés (GV et ciment pour le 100 M, et le 34 M de référence), les commandes exactes, et les chemins des fichiers.
Your parent agent id is "d67a9bb1-090e-4f69-baf2-a831c00aa275". Before you finish, send your result to that agent with send_message({ agent_id: "d67a9bb1-090e-4f69-baf2-a831c00aa275", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

12. **La tarification de l'API a deux fenêtres** : **remisé** pendant **UTC 16:30 → 00:30**
    (la Chine 00:30 → 08:30), soit au Canada **11:30 → 19:30** ; **plein tarif** le reste.
    **L'API en remisée** (le tagger, la distillation), **le local en pleine** (l'entraînement, les
    tests, les docs) ; **deux files** par chantier. → [`plans-tarif.md`](docs/pilotage/plans-tarif.md)

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

⏵ Exploration du dépôt pour retrouver le banc de grammaticalité et le protocole

- **bash** `{"command": "ls reports/ | grep -i gramm; echo \"---\"; ls tools/ | grep -i gramm; echo \"---\"; ls -la work/n2ac/ 2>/dev/null | head -30", "description": "Liste les fichiers de grammaticalité"}`

  ```
banc-grammaticalite-echelle.json
banc-grammaticalite.json
rapport-programme-evolutif.md
---
banc_grammaticalite.py
---
total 8605900
drwxr-xr-x. 1 stephane stephane     10516 17 nov 09:57 .
drwxr-xr-x. 1 stephane stephane      2854 17 nov 15:33 ..
-rw-r--r--. 1 stephane stephane 137224476  2 nov 17:31 absolu-pos1152.drvm
-rw-r--r--. 1 stephane stephane     21807  2 nov 17:31 absolu-pos1152.log
-rw-r--r--. 1 stephane stephane 137248740  2 nov 17:30 absolu-pos1152.pt
-rw-r--r--. 1 stephane stephane       561  2 nov 17:31 absolu-pos1152.pt.json
-rw-------. 1 stephane stephane      2763  2 nov 21:05 agrege_fenetre.py
-rw-r--r--. 1 stephane stephane      1680  2 nov 23:31 agrege_production.py
-rw-------. 1 stephane stephane      3151  2 nov 18:50 agrege_r11.py
-rw-r--r--. 1 stephane stephane  47283932  3 nov 04:04 cap-1147m-128.drvm
-rw-r--r--. 1 stephane stephane     35105  3 nov 04:04 cap-1147m-128.log
-rw-r--r--. 1 stephane stephane  47308063  3 nov 04:04 cap-1147m-128.pt
-rw-r--r--. 1 stephane stephane       505  3 nov 04:04 cap-1147m-128.pt.json
-rw-r--r--. 1 stephane stephane  47283932  3 nov 03:33 cap-1147m-512.drvm
-rw-r--r--. 1 stephane stephane      9444  3 nov 03:33 cap-1147m
… [1023 caractères tronqués]
  ```

- **glob** `{"pattern": "**/banc*grammaticalite*"}`

  ```
tools/banc_grammaticalite.py
reports/banc-grammaticalite.json
reports/banc-grammaticalite-echelle.json
  ```

### 🤖 Assistant

⏵ Lecture du banc et des JSON de référence

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_grammaticalite.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_grammaticalite.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """banc_grammaticalite.py — le natif jugé par le bloc linguistique de Drave.
3: 
4: POURQUOI. Le banc de génération dit que le natif produit des mots mais pas des
5: phrases. Ce banc le mesure **avec notre propre analyseur** : sur les générations
6: du natif (et le contrôle aléatoire), il compte les **GV** (un texte sans verbe
7: n'est pas une phrase), les **GN**, la part des **classes fermées** (le ciment :
8: DET, PREP, CONJ, PRON), et les **attachements** réussis.
9: 
10: LA MESURE. Pour chaque génération : `gv`, `gn`, `mots`, `ciment` (la fraction
11: des mots en classe fermée), `attaches` (les segments avec une cible / les
12: segments). Le **contrôle** : les générations du modèle aléatoire, traitées
13: par le même analyseur. Si le natif a une syntaxe, il doit avoir **plus de GV**
14: et **plus d'attachements** que le hasard ; sinon, le banc dit qu'il n'en a pas.
15: 
16: Usage :
17:   python3 tools/banc_grammaticalite.py --entree reports/banc-generation.json \
18:       --controle reports/banc-generation-aleatoire.json --sortie re
… [3089 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la reports/*grammaticalite* reports/*grammatical* 2>/dev/null; echo \"=== recherche rapport ===\"; grep -ril \"grammaticalit\" reports/ journal/ 2>/dev/null | head -30", "description": "Cherche les rapports de grammaticalité"}`

  ```
-rw-r--r--. 1 stephane stephane 1038 16 nov 15:04 reports/banc-grammaticalite-echelle.json
-rw-r--r--. 1 stephane stephane 1038 16 nov 15:04 reports/banc-grammaticalite-echelle.json
-rw-r--r--. 1 stephane stephane 1041 16 nov 10:53 reports/banc-grammaticalite.json
-rw-r--r--. 1 stephane stephane 1041 16 nov 10:53 reports/banc-grammaticalite.json
=== recherche rapport ===
reports/rapport-gold-anglais.md
reports/rapport-banc-generation.md
reports/rapport-natif-exploitable.md
reports/fiche-modele-natif.md
reports/rapport-bilan-natif.md
reports/rapport-banc-generation-100m.md
journal/sessions/d629d7d7-e122-4596-8757-f4264a2b15cf/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/digest.md
journal/2026-11-16/README.md
journal/2026-11-16/modele.md
  ```

### 🤖 Assistant

⏵ Recherche du rapport et du protocole de génération

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat reports/banc-grammaticalite.json; echo \"=== ECHELLE ===\"; cat reports/banc-grammaticalite-echelle.json; echo \"=== GEN 100M ===\"; cat reports/rapport-banc-generation-100m.md", "description": "Lit les JSON de grammaticalité et  … [17 caractères tronqués]`

  ```
{
 "natif": {
  "greedy": {
   "textes": 20,
   "gv_moyen": 6.9,
   "gn_moyen": 2.85,
   "mots_moyen": 44.8,
   "ciment": 0.3346,
   "attaches": 0.7368,
   "sans_verbe": 0.15
  },
  "top40_0.8": {
   "textes": 20,
   "gv_moyen": 6.35,
   "gn_moyen": 3.15,
   "mots_moyen": 35.2,
   "ciment": 0.3769,
   "attaches": 0.887,
   "sans_verbe": 0.0
  },
  "top20_0.5": {
   "textes": 20,
   "gv_moyen": 5.85,
   "gn_moyen": 3.15,
   "mots_moyen": 38.5,
   "ciment": 0.3098,
   "attaches": 0.7892,
   "sans_verbe": 0.0
  }
 },
 "aleatoire": {
  "greedy": {
   "textes": 20,
   "gv_moyen": 2.3,
   "gn_moyen": 1.8,
   "mots_moyen": 62.5,
   "ciment": 0.7912,
   "attaches": 0.7466,
   "sans_verbe": 0.0
  },
  "top40_0.8": {
   "textes": 20,
   "gv_moyen": 3.35,
   "gn_moyen": 2.8,
   "mots_moyen": 87.8,
   "ciment": 0.8008,
   "attaches": 0.6503,
   "sans_verbe": 0.1
  },
  "top20_0.5": {
   "textes": 20,
   "gv_moyen": 4.0,
   "gn_moyen": 2.35,
   "mots_moyen": 89.6,
   "ciment": 0.7959,
   "attaches": 0.6701,
   "sans_verbe": 0.05
  }
 }
}
=== ECHELLE ===
{
 "natif": {
  "greedy": {
   "textes": 20,
   "gv_moyen": 1.9,
   "gn_moyen": 1.6,
   "mots_moyen": 12.8,
   "ciment": 0.1369,
   "attaches":
… [4729 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la tools/banc_generation.py reports/banc-generation*.json 2>/dev/null; echo \"=== grep grammaticalité dans rapports ===\"; grep -n -i \"grammaticalit\\|GV\\|ciment\" reports/rapport-banc-generation.md reports/rapport-banc-generat … [88 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 19805 17 nov 14:37 reports/banc-generation-100m.json
-rw-r--r--. 1 stephane stephane 23390 16 nov 11:51 reports/banc-generation-11m.json
-rw-r--r--. 1 stephane stephane 23993 16 nov 11:51 reports/banc-generation-21m.json
-rw-r--r--. 1 stephane stephane 19530 18 nov 08:52 reports/banc-generation-34m-64o.json
-rw-r--r--. 1 stephane stephane 24433 18 nov 08:52 reports/banc-generation-alea-64o.json
-rw-r--r--. 1 stephane stephane 30819 16 nov 10:43 reports/banc-generation-aleatoire.json
-rw-r--r--. 1 stephane stephane 24369 16 nov 10:33 reports/banc-generation.json
-rw-r--r--. 1 stephane stephane  8065 17 nov 14:35 tools/banc_generation.py
=== grep grammaticalité dans rapports ===
reports/rapport-banc-generation.md:52:## 3 bis. Le natif jugé par notre analyseur (le banc de grammaticalité)
reports/rapport-banc-generation.md:54:[`tools/banc_grammaticalite.py`](../tools/banc_grammaticalite.py) passe les **136 générations**
reports/rapport-banc-generation.md:57:| source | GV moyens | GN moyens | ciment (classes fermées) | attachements |
reports/rapport-banc-generation.md:64:**Lecture.** Le natif a **trois fois plus de GV** que le hasard (6,9 contre 2,3) : il
… [995 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du rapport de référence et du code de génération

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-banc-generation.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_generation.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-banc-generation.md</path>
<type>file</type>
<content>
1: # Le banc de génération du natif — le modèle a appris les mots, pas la phrase
2: 
3: > **Ligne de roadmap** : **N4** (l'usage du natif) · **Date** : 2026-11-16 · **Modèle mesuré** :
4: > `work/n2ac/mix1024-60k.pt` (**34,3 M** paramètres, RoPE, seq 1 024, PPL **2,40**, corpus
5: > `wiki_mix/propre`) · **Verdict** : ❌ **le natif n'est pas un générateur de texte** — il a
6: > appris le **vocabulaire** (87 % de mots réels), pas la **composition** (un trigramme répété
7: > **15 fois** en greedy, des pseudo-mots en échantillonnage).
8: >
9: > **Le chiffre, en une ligne.** Sur **20 prompts** fixes et **128 octets** par prompt, trois
10: > réglages : **greedy** 0,870 de mots valides mais une **répétition de 15** ; **top-40/0,8**
11: > 0,490 de mots valides et une diversité de 1,000 ; **top-20/0,5** 0,735 et 0,981. Le
12: > **contrôle aléatoire** (même architecture, poids au hasard) : **0,336** de mots valides et
13: > **1** de répétition — le banc discrimine le modèle du bruit.
14: 
15: ## 1. Le dispositif
16: 
17: [`tools/banc_generation.py`](../tools/banc_generat
… [6392 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_generation.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """banc_generation.py — le banc de génération du modèle natif (diagnostic, pas un produit).
3: 
4: POURQUOI. Le modèle natif (`drave-n0`, 34 M) a une PPL de 2,40 mais l'archive dit
5: « cohérent 12 octets puis dérive ». Ce banc mesure ce que la PPL ne dit pas : sur
6: 20 prompts fixes et trois réglages, la **qualité du texte produit** (mots réels,
7: diversité, répétition), la **vitesse** et la **mémoire**, avec un **contrôle
8: aléatoire** (la même architecture, poids au hasard) — sans lui, aucun chiffre ne
9: se lit.
10: 
11: CE QU'IL MESURE, PAR RÉGLAGE.
12:   - `octets` / `secondes` / `octets_s` : le débit de génération (byte-level) ;
13:   - `mots` : les mots décodés (UTF-8 avec remplacement) ;
14:   - `mots_valides` : la fraction des mots présents dans le vocabulaire du corpus
15:     (`data/wiki_mix/propre/train.txt`, les 50 000 formes les plus fréquentes) —
16:     le proxy de « ce sont des mots français » ;
17:   - `distinct_2` : la diversité (les bigrammes de mots distincts / total) ;
18:   - `repetition` : le plus grand nombre d'o
… [7846 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification GPU, modèles et JSON de contrôle

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv; echo \"=== torch ===\"; /home/stephane/gpu-env/bin/python -c \"import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.devi … [205 caractères tronqués]`

  ```
index, name, memory.used [MiB], memory.total [MiB], utilization.gpu [%]
0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %
1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %
=== torch ===
2.11.0+cu130 True 2
=== modeles ===
-rw-r--r--. 1 stephane stephane 293509850 17 nov 09:57 work/n2ac/mix1024-100m.pt
-rw-r--r--. 1 stephane stephane 137248341  3 nov 17:22 work/n2ac/mix1024-60k.pt
{
 "modele": "drave-n0",
 "parametres": 73366568,
 "corpus": "data/wiki_mix/propre/train.txt",
 "octets": 1017487092,
 "pas": 3000,
 "seq": 1024,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "perte_finale": 1.4668956995010376,
 "ppl_val": 4.01394552944023,
 "jetons_val": 65536,
 "tetes": false,
 "precision_main": 0.591796875,
 "precision_early": [
  0.000518798828125,
  0.00372314453125,
  0.002532958984375
 ],
 "drvm": "work/n2ac/mix1024-100m.drvm",
 "sha256_drvm": "1011c1af0f3e311c6fbb8022d4b4bebbf821cd25de9ea9073f99c330ac65c178",
 "duree_s": 879.9492771625519
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfor p in [\"reports/banc-generation.json\",\"reports/banc-generation-aleatoire.json\",\"reports/banc-generation-100m.json\",\"reports/banc-generation-34m-64o.json\",\"reports/ … [410 caractères tronqués]`

  ```
reports/banc-generation.json modele= work/n2ac/mix1024-60k.pt aleatoire= False n= 128 vocab= 50000 reglages= ['greedy', 'top40_0.8', 'top20_0.5'] prompts= 20 lignes0= 20
reports/banc-generation-aleatoire.json modele= work/n2ac/mix1024-60k.pt aleatoire= True n= 128 vocab= 50000 reglages= ['greedy', 'top40_0.8', 'top20_0.5'] prompts= 20 lignes0= 20
reports/banc-generation-100m.json modele= work/n2ac/mix1024-100m.pt aleatoire= False n= 64 vocab= 50000 reglages= ['greedy', 'top40_0.8', 'top20_0.5'] prompts= 20 lignes0= 20
reports/banc-generation-34m-64o.json modele= work/n2ac/mix1024-60k.pt aleatoire= False n= 64 vocab= 50000 reglages= ['greedy', 'top40_0.8', 'top20_0.5'] prompts= 20 lignes0= 20
reports/banc-generation-alea-64o.json modele= work/n2ac/mix1024-60k.pt aleatoire= True n= 64 vocab= 50000 reglages= ['greedy', 'top40_0.8', 'top20_0.5'] prompts= 20 lignes0= 20
  ```

### 🤖 Assistant

⏵ Vérification du nombre réel de paramètres du « 100 M »

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport torch, sys\nsys.path.insert(0,'.')\nfrom tools.native_model import NativeConfig, NativeModel\nfor p in [\"work/n2ac/mix1024-100m.pt\",\"work/n2ac/mix1024-60k.pt\"]:\n    ck=torch.lo … [387 caractères tronqués]`

  ```
work/n2ac/mix1024-100m.pt
  config: {'vocab': 256, 'd_model': 640, 'n_blocks': 6, 'n_heads': 4, 'expert_hidden': 640, 'n_experts': 8, 'top_k': 2, 'kwta': 0.25, 'window': 256, 'max_pos': 2048, 'thought_steps': 2, 'early_blocks': (1, 3, 5), 'rsn_dim': 120}
  params: 73366568 clés: ['config', 'state']
work/n2ac/mix1024-60k.pt
  config: {'vocab': 256, 'd_model': 384, 'n_blocks': 6, 'n_heads': 4, 'expert_hidden': 512, 'n_experts': 8, 'top_k': 2, 'kwta': 0.25, 'window': 1024, 'max_pos': 2048, 'thought_steps': 2, 'early_blocks': (1, 3, 5), 'rsn_dim': 120}
  params: 34301224 clés: ['config', 'state']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"mix1024-100m\\|100 M\" docs/pilotage/en-cours.md docs/pilotage/natif-plan.md 2>/dev/null | head -30; echo \"=== git ===\"; git status --porcelain | head -20; echo \"=== branche ===\"; git branch --show-current", "descripti … [49 caractères tronqués]`

  ```
docs/pilotage/en-cours.md:3:**Mis à jour : 2026-11-18, 00 h 10 HNE (la passe 90 portes, 87/3, aucune nouvelle · le 100 M mesuré : répétition 9 → 6, la composition ne vient pas)**
docs/pilotage/en-cours.md:84:- **N2 — 100 M mesuré** (17/11) : banc apparié (64 o, GPU) — greedy **0,882** vs **0,884** (34 M), répétition **6** vs **9**, top-40 **+0,069**, top-20 **−0,088** ; aléatoire **0,37** ; [fiche](../../reports/rapport-banc-generation-100m.md) ; porte `eval_longueurs.py --rope --val` (**2,7856**) ensuite.
=== git ===
?? reports/corpus-epingle.json
?? tools/epingle_corpus.py
=== branche ===
s/v7
  ```

### 🤖 Assistant

⏵ Inspection de la fenêtre du modèle et du bloc linguistique

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"window\\|max_pos\" tools/native_model.py | head -30; echo \"=== bloc ===\"; ls -la tools/bloc_linguistique.py; grep -n \"class Heuristique\" -A5 tools/bloc_linguistique.py | head -20", "description": "Vérifie la fenêtre et  … [13 caractères tronqués]`

  ```
34:    window: int = 256
35:    max_pos: int = 2048
89:        masque = (i[:, None] >= i[None, :]) & ((i[:, None] - i[None, :]) < self.cfg.window)
101:        self.pos = nn.Embedding(self.cfg.max_pos, self.cfg.d_model)
205:                                   "kwta": cfg.kwta, "window": cfg.window,
213:                      "cache": {"kind": "kv", "max": cfg.window},
=== bloc ===
-rw-r--r--. 1 stephane stephane 167604 16 nov 00:01 tools/bloc_linguistique.py
1012:class Heuristique:
1013-    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
1014-
1015-    nom = "heuristique"
1016-
1017-    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nd=json.load(open(\"reports/banc-generation.json\"))\nfor n,r in d[\"reglages\"].items():\n    print(n, \"n_lignes\", len(r[\"lignes\"]), \"octets\", r[\"octets\"])\n    print( … [168 caractères tronqués]`

  ```
greedy n_lignes 20 octets 2560
  ex: La France est un pays | La France est un pays don d d da d 20 n dese de 1 20 20 aba dele  1  la  1 20 20 201 1  19
top40_0.8 n_lignes 20 octets 2560
  ex: La France est un pays | La France est un pays esovors de destode dene f. 20 Trat Bra s? 1 15 A. l. mb e. Aust Mete
top20_0.5 n_lignes 20 octets 2560
  ex: La France est un pays | La France est un pays 2010 sene don d ousi le e 20 ste 2019 de 20 1 se confolemenatéce Som
  ```

### 🤖 Assistant

⏵ Lancement du banc de génération 100 M sur cuda:0 (128 octets, protocole 34 M)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 --sortie /tmp/banc-generation-100m-128o.json 2>&1 | tail -20", "description": "Génère 100M, 20 prompts, 128 oc … [63 caractères tronqués]`

  ```
started background job bash-277
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' journal/2026-11-16/modele.md", "description": "Lit le récit du 16 novembre sur le modèle"}`

  ```
# 2026-11-16 — Modèles, entraînement, parcimonie, biologie

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (14)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 03:12 | `3c10e3ee` | V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON | `en-cours.md`, `references-non-regression.md`, `roadmap.md` (+18) |
| 07:57 | `6f5e0f0c` | SOUS-MODULES — LE DOCWATCH REPINÉ SUR 95e94c4 (LE PIN d256888 N'EXISTE PAS SUR LE REMOTE) ; LE CLONE --recurse-submodules PASSE | `en-cours.md`, `README.md`, `docs.md` (+10) |
| 10:44 | `cf3f9bc7` | NATIF — LE BANC DE GÉNÉRATION (20 PROMPTS, 3 RÉGLAGES, LE CONTRÔLE ALÉATOIRE) : LE MODÈLE A APPRIS LES MOTS (0,87 CONTRE 0,34) PAS LA PHRASE (RÉPÉTITION 15 EN GREEDY) | `en-cours.md`, `README.md`, `docs.md` (+15) |
| 10:53 | `b2dfc1cc` | NATIF — LE BANC DE GRAMMATICALITÉ : NOTRE ANALYSEUR JUGE 
… [3532 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-277", "timeout_ms": 120000}`

  ```
(no new output)
[status: running]
  ```

### 🤖 Assistant

⏵ Pendant la génération, examen des échantillons et du contexte

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nd=json.load(open(\"reports/banc-generation-100m.json\"))\nfor n,r in d[\"reglages\"].items():\n    print(\"==\",n,\"mots_valides\",r[\"mots_valides\"],\"repetition\",r[\"repet … [194 caractères tronqués]`

  ```
== greedy mots_valides 0.8824 repetition 6
   La France est un pays | La France est un pays de de de des de de de de lande lande s de lande s de de lande l
   Dans les années 1950 | Dans les années 1950isale s ses es de s se mise de de lans des le de s de de s de la
   Il était une fois | Il était une fois de de la pré de ére le de la de s ére de ére land s de stio
== top40_0.8 mots_valides 0.5869 repetition 1
   La France est un pays | La France est un pays de son dest de Sonans dge : landes salante dent alaux régiathu
   Dans les années 1950 | Dans les années 1950ismalesatres avie lese de ales Janse, ses auletin agist dales de
   Il était une fois | Il était une fois s ée é dis aut erill aist dé es enditale drans d polatis de 
== top20_0.5 mots_valides 0.6529 repetition 2
   La France est un pays | La France est un pays de ale des de mionse de de pos de des ansemisé lant de enantit
   Dans les années 1950 | Dans les années 1950ales s ponemife desont emmese e nale mble ess mandons at es dans
   Il était une fois | Il était une fois auré demioien llans s porétales t de ce quronales ande ps é
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '70,100p' docs/pilotage/en-cours.md", "description": "Lit la ligne N de l'état courant"}`

  ```
- **Rôle** : **N2** — la production et la capacité.
- **Plan** : fenêtre.
- **Ambition** : la longueur et la capacité.
- **Stratégie** : budgets contrôlés, mêmes bancs.
- **Objectif final** : la production qui tient.
- **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte ; `kd2` et `rope2048` **arrêtés** ; **paire propre** : **3,1500** → **3,1119**
- **Ce que font les autres** : **hub**, **S**, **Pensée**.
- **Prochaine action** : la **porte propre (0,29)** ; le **2 048** est fini.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles ; **19/19 verdicts `389b99f`** ; [v2](../../reports/rapport-coordination-s-v2.md).
- **N2 — 100 M mesuré · corpus épinglé** : banc apparié — greedy **0,882** vs **0,884** (34 M), répétition **6** vs **9** ; [fiche](../../reports/rapport-banc-generation-100m.md) ; **corpus épinglé** (train `0876b608…`, val `fbddef91…`, manifeste `fae5bb73…`, `--verifie` 6,5 s) — [fiche](../../reports/rapport-corpus-epingle.md).
- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** 
… [1953 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-277", "timeout_ms": 300000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "nvidia-smi --query-compute-apps=pid,used_memory,gpu_uuid --format=csv; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv; ps -o pid,etime,pcpu,pmem,cmd -C python | tail -5", "description": "Vérifie l'activité GPU et CPU du job"}`

  ```
pid, used_gpu_memory [MiB], gpu_uuid
index, memory.used [MiB], utilization.gpu [%]
0, 1 MiB, 0 %
1, 1 MiB, 0 %
    PID     ELAPSED %CPU %MEM CMD
 313960       00:21  114  0.5 /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 --sortie /tmp/banc-generation-100m-128o.json
  ```

- **bash** `{"command": "ls -la /tmp/banc-generation-100m-128o.json 2>/dev/null; ps -o pid,lstart,etime,pcpu,cmd -p 313960; cat /proc/313960/status 2>/dev/null | grep -E \"State|VmRSS|Threads\"; echo \"=== jobs ===\"; ", "description": "Vérifie l'état détaillé du processus"}`

  ```
PID                  STARTED     ELAPSED %CPU CMD
 313960 mer nov 18 09:00:31 2026       00:30  110 /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 --sortie /tmp/banc-generation-100m-128o.json
State:	R (running)
VmRSS:	  869968 kB
Threads:	40
=== jobs ===
  ```

- **job_list** `{}`

  ```
bash-277 [bash] running — cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 --sortie /tmp/banc-generation-100m-128o.json 2>&1 | tail -20
  ```

- **bash** `{"command": "date; ls -la /tmp/banc-generation-100m-128o.json 2>/dev/null || echo \"pas encore de sortie\"; ps -o pid,etime,pcpu,cmd -p 313960", "description": "Compare l'heure et l'âge du processus"}`

  ```
mer 18 nov 2026 09:01:06 EST
pas encore de sortie
    PID     ELAPSED %CPU CMD
 313960       00:34  108 /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 --sortie /tmp/banc-generation-100m-128o.json
  ```

### 🤖 Assistant

⏵ Attente de la génération (lecture du corpus de 1 Go en cours)

- **job_output** `{"job_id": "bash-277", "timeout_ms": 420000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "date; ps -o pid,etime,pcpu,pmem,cmd -p 313960; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader; ls -la /tmp/banc-generation-100m-128o.json 2>/dev/null || echo \"pas de sortie\"", "description": "Contrôle l'avancement du job"}`

  ```
mer 18 nov 2026 09:01:20 EST
    PID     ELAPSED %CPU %MEM CMD
 313960       00:48  106  0.7 /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 --sortie /tmp/banc-generation-100m-128o.json
0, 1 MiB, 0 %
1, 1 MiB, 0 %
pas de sortie
  ```

### 🤖 Assistant

⏵ Test à blanc du pipeline de grammaticalité sur les JSON 64 octets existants

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time /home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py --entree reports/banc-generation-100m.json --controle reports/banc-generation-alea-64o.json --sortie /tmp/banc-grammaticalite-100m-64o.json", "description": "Teste l … [73 caractères tronqués]`

  ```
natif     greedy     gv=1.10 gn=1.30 mots=19.9 ciment=0.693 attaches=0.870 sans_verbe=0.45
natif     top40_0.8  gv=2.15 gn=1.95 mots=15.1 ciment=0.375 attaches=0.814 sans_verbe=0.00
natif     top20_0.5  gv=1.60 gn=1.80 mots=17.4 ciment=0.471 attaches=0.837 sans_verbe=0.10
aleatoire greedy     gv=1.50 gn=1.75 mots=47.5 ciment=0.790 attaches=0.775 sans_verbe=0.05
aleatoire top40_0.8  gv=2.05 gn=2.10 mots=48.6 ciment=0.795 attaches=0.739 sans_verbe=0.05
aleatoire top20_0.5  gv=2.15 gn=2.00 mots=51.6 ciment=0.819 attaches=0.685 sans_verbe=0.00
[stderr]

real	0m0,361s
user	0m0,342s
sys	0m0,019s
  ```

- **bash** `{"command": "sleep 45; date; ps -o pid,etime,pcpu,cmd -p 313960; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader; ls -la /tmp/banc-generation-100m-128o.json 2>/dev/null || echo \"pas de sortie\"", "description": "Attend et vérifie le job de génération", "timeoutMs": 12 … [5 caractères tronqués]`

  ```
mer 18 nov 2026 09:02:26 EST
    PID     ELAPSED %CPU CMD
 313960       01:54  103 /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 --sortie /tmp/banc-generation-100m-128o.json
0, 502 MiB, 57 %
1, 4 MiB, 0 %
pas de sortie
  ```

- **bash** `{"command": "sleep 60; date; ps -o pid,etime,pcpu -p 313960; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader; ls -la /tmp/banc-generation-100m-128o.json 2>/dev/null || echo \"pas de sortie\"", "description": "Attend la fin de la génération", "timeoutMs": 120000}`

  ```
mer 18 nov 2026 09:03:37 EST
    PID     ELAPSED %CPU
0, 1 MiB, 0 %
1, 1 MiB, 0 %
-rw-r--r--. 1 stephane stephane 24231 18 nov 09:02 /tmp/banc-generation-100m-128o.json
  ```

### 👤 Utilisateur

background job bash-277 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 --sortie /tmp/banc-generation-100m-128o.json 2>&1 | tail -20) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Génération terminée, lecture des sorties et vérification de cohérence

- **job_output** `{"job_id": "bash-277"}`

  ```
écrit : /tmp/banc-generation-100m-128o.json
greedy       mots_valides=0.878 distinct_2=0.652 repetition=6 echo=0.02 octets/s=121.9
top40_0.8    mots_valides=0.551 distinct_2=1.000 repetition=1 echo=0.02 octets/s=118.4
top20_0.5    mots_valides=0.673 distinct_2=0.960 repetition=2 echo=0.02 octets/s=117.9
[stderr]

real	1m59,390s
user	2m1,050s
sys	0m2,176s
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/banc-generation-100m-128o.json\"))\nprint(\"modele\",d[\"modele\"],\"n\",d[\"n\"],\"aleatoire\",d[\"aleatoire\"],\"vocab\",d[\"vocabulaire\"])\nfor n,r … [409 caractères tronqués]`

  ```
modele work/n2ac/mix1024-100m.pt n 128 aleatoire False vocab 50000
greedy mots_valides 0.8784 distinct2 0.6523 rep 6 echo 0.0151 octets/s 121.9 temps 21.0
    La France est un pays | La France est un pays de de de des de de de de lande lande s de lande s de de lande landes de de lande land des lande lande lande 
    Dans les années 1950 | Dans les années 1950isale s ses es de s se mise de de lans des le de s de de s de lande s de de lande s de des de lans des de le d
    Il était une fois | Il était une fois de de la pré de ére le de la de s ére de ére land s de stion de de de de lande lande s chatie de lage me de lans
top40_0.8 mots_valides 0.5511 distinct2 1.0 rep 1 echo 0.0158 octets/s 118.4 temps 20.73
    La France est un pays | La France est un pays 6a de , daicuis ables s dales de  coné de mic an. n e de lorgislie), s elosa pagéranie e don, durebans doion
    Dans les années 1950 | Dans les années 1950iveansalles d . ponce mion . elalale  blandes dre matifin  e ssion de sth ie ville tise mmpois des de ponde  l
    Il était une fois | Il était une fois don cs e andes onn unai  és é étale chie ers ations de émin e latistrionle t de San miraiste  éstale mes de pori
top20_0.5 mo
… [549 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Calcul de la grammaticalité 100 M et vérification de la référence 34 M

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py --entree /tmp/banc-generation-100m-128o.json --controle reports/banc-generation-aleatoire.json --sortie reports/banc-grammaticalite-100m.json && echo \"=== JSON écrit === … [127 caractères tronqués]`

  ```
natif     greedy     gv=1.45 gn=1.55 mots=35.2 ciment=0.661 attaches=0.905 sans_verbe=0.40
natif     top40_0.8  gv=4.00 gn=1.85 mots=27.7 ciment=0.375 attaches=0.771 sans_verbe=0.00
natif     top20_0.5  gv=2.65 gn=1.90 mots=32.0 ciment=0.461 attaches=0.871 sans_verbe=0.00
aleatoire greedy     gv=2.30 gn=1.80 mots=62.5 ciment=0.791 attaches=0.747 sans_verbe=0.00
aleatoire top40_0.8  gv=3.35 gn=2.80 mots=87.8 ciment=0.801 attaches=0.650 sans_verbe=0.10
aleatoire top20_0.5  gv=4.00 gn=2.35 mots=89.6 ciment=0.796 attaches=0.670 sans_verbe=0.05
=== JSON écrit ===
{
 "natif": {
  "greedy": {
   "textes": 20,
   "gv_moyen": 1.45,
   "gn_moyen": 1.55,
   "mots_moyen": 35.2,
   "ciment": 0.6611,
   "attaches": 0.9052,
   "sans_verbe": 0.4
  },
  "top40_0.8": {
   "textes": 20,
   "gv_moyen": 4.0,
   "gn_moyen": 1.85,
   "mots_moyen": 27.7,
   "ciment": 0.3748,
   "attaches": 0.7708,
   "sans_verbe": 0.0
  },
  "top20_0.5": {
   "textes": 20,
   "gv_moyen": 2.65,
   "gn_moyen": 1.9,
   "mots_moyen": 32.0,
   "ciment": 0.4605,
   "attaches": 0.8707,
   "sans_verbe": 0.0
  }
 },
 "aleatoire": {
  "greedy": {
   "textes": 20,
   "gv_moyen": 2.3,
   "gn_moyen": 1.8,
   "mots_moyen": 62.5,
   "ci
… [404 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py --entree reports/banc-generation.json --controle reports/banc-generation-aleatoire.json --sortie /tmp/banc-grammaticalite-34m-128o.json >/dev/null && diff <(cat /tmp/banc … [200 caractères tronqués]`

  ```
RÉFÉRENCE 34M REPRODUITE À L'IDENTIQUE
  ```

### 🤖 Assistant

⏵ Lancement du contrôle aléatoire 100 M (même graine 1234) en arrière-plan

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --aleatoire --n 128 --sortie /tmp/banc-generation-alea-100m-128o.json 2>&1 | tail -20", "description": "Génère le contrôle aléatoire 1 … [66 caractères tronqués]`

  ```
started background job bash-326
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json, collections, re\nSTOP = set(\"de la le les des du un une et en à a l d que qui dans pour par sur au aux se s est sont était être avec ne pas plus il elle on nous vous ils elle … [827 caractères tronqués]`

  ```
===== 34M
greedy     mots_gen= 832 de= 54 (0.06) top5=[('1', 153), ('e', 110), ('a', 98), ('d', 62), ('de', 54)] types=149
top40_0.8  mots_gen= 465 de=  7 (0.02) top5=[('1', 15), ('d', 12), ('a', 11), ('e', 8), ('de', 7)] types=345
top20_0.5  mots_gen= 652 de= 15 (0.02) top5=[('20', 49), ('e', 43), ('1', 38), ('a', 38), ('d', 20)] types=261
===== 100M
greedy     mots_gen= 661 de=304 (0.46) top5=[('de', 304), ('lande', 86), ('s', 50), ('des', 35), ('le', 18)] types=74
top40_0.8  mots_gen= 476 de= 45 (0.09) top5=[('de', 45), ('e', 32), ('s', 24), ('le', 12), ('des', 11)] types=289
top20_0.5  mots_gen= 587 de=143 (0.24) top5=[('de', 143), ('e', 39), ('s', 33), ('le', 26), ('des', 23)] types=248
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat work/n2ac/mix1024-60k.pt.json 2>/dev/null; echo \"=== log 100m ===\"; ls work/n2ac/mix1024-100m.log 2>/dev/null && tail -20 work/n2ac/mix1024-100m.log", "description": "Lit les métadonnées du 34M et le log du 100M"}`

  ```
{
 "modele": "drave-n0-rope",
 "parametres": 34301224,
 "corpus": "data/wiki_mix/propre/train.txt",
 "octets": 1017487092,
 "pas": 30000,
 "seq": 1024,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "window": 1024,
 "positions": "rope",
 "init": "work/n2ac/mix1024-30k.pt",
 "perte_finale": 1.0251544713974,
 "ppl_val": 2.4038261088297856,
 "jetons_val": 65536,
 "tetes": true,
 "drvm": "work/n2ac/mix1024-60k.drvm",
 "sha256_drvm": "72e740e06d93e7d43ac09b324ff209620b48d9abd19914064e45ca7644068af5",
 "duree_s": 13331.16178894043
}
=== log 100m ===
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nref=json.load(open(\"reports/banc-grammaticalite.json\"))\nnew=json.load(open(\"reports/banc-grammaticalite-100m.json\"))\nfor reg in [\"greedy\",\"top40_0.8\",\"top20_0.5\"]: … [548 caractères tronqués]`

  ```
greedy     34M gv=6.90 ciment=0.3346 gv100=15.4 | 100M gv=1.45 ciment=0.6611 gv100=4.1 | dGV=-5.45
top40_0.8  34M gv=6.35 ciment=0.3769 gv100=18.0 | 100M gv=4.00 ciment=0.3748 gv100=14.4 | dGV=-2.35
top20_0.5  34M gv=5.85 ciment=0.3098 gv100=15.2 | 100M gv=2.65 ciment=0.4605 gv100=8.3 | dGV=-3.20

controle 34M greedy gv=2.30 ciment=0.7912 gv100=3.7
  ```

### 🤖 Assistant

⏵ Contrôle aléatoire en cours ; analyse de la concentration du ciment

- **bash** `{"command": "sleep 60; date; ps -o pid,etime,pcpu,cmd -C python | tail -3; ls -la /tmp/banc-generation-alea-100m-128o.json 2>/dev/null || echo \"pas de sortie\"", "description": "Vérifie l'avancement du contrôle aléatoire", "timeoutMs": 120000}`

  ```
mer 18 nov 2026 09:06:26 EST
    PID     ELAPSED %CPU CMD
 318290       01:35  103 /home/stephane/gpu-env/bin/python -m tools.entrainer_native --corpus data/wiki_mix/propre/train.txt --val data/wiki_mix/propre/val.txt --pas 50 --seq 1024 --lot 8 --lr 1e-4 --dim 640 --expert-hidden 640 --no-tetes --amp --device cuda:0 --graine 1 --init work/n2ac/mix1024-100m.pt --sortie /tmp/essai-50pas.pt --drvm /tmp/essai-50pas.drvm
 318459       01:22  826 /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --aleatoire --n 128 --sortie /tmp/banc-generation-alea-100m-128o.json
pas de sortie
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '20,50p' tools/native_model.py", "description": "Lit la configuration par défaut du modèle natif"}`

  ```
from tools.drvm import TensorSpec, write_drvm


@dataclass
class NativeConfig:
    vocab: int = 256
    d_model: int = 224
    n_blocks: int = 6
    n_heads: int = 4
    expert_hidden: int = 288
    n_experts: int = 8
    top_k: int = 2
    kwta: float = 0.25
    window: int = 256
    max_pos: int = 2048
    thought_steps: int = 2
    early_blocks: tuple[int, ...] = (1, 3, 5)  # 0-based : après 2, 4, 6
    rsn_dim: int = 120


class SparseFFN(nn.Module):
    def __init__(self, cfg: NativeConfig):
        super().__init__()
        self.cfg = cfg
        self.router = nn.Linear(cfg.d_model, cfg.n_experts)
        self.gate = nn.Linear(cfg.d_model, cfg.n_experts * cfg.expert_hidden)
        self.up = nn.Linear(cfg.d_model, cfg.n_experts * cfg.expert_hidden)
        self.down = nn.Linear(cfg.n_experts * cfg.expert_hidden, cfg.d_model)

    def forward(self, x):
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/banc-generation-100m-128o.json\"))\nfor reg in [\"greedy\",\"top40_0.8\",\"top20_0.5\"]:\n    r=d[\"reglages\"][reg]\n    print(reg, \"textes sans verb … [1161 caractères tronqués]`

  ```
greedy textes sans verbe (brut):
top40_0.8 textes sans verbe (brut):
top20_0.5 textes sans verbe (brut):
== 34M
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 23, in <module>
  File "<stdin>", line 23, in <genexpr>
AttributeError: 'Etiquette' object has no attribute 'surface'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Etiquette\" -A15 tools/bloc_linguistique.py | head -25", "description": "Inspecte la classe Etiquette"}`

  ```
76:class Etiquette:
77-    niveau: str
78-    type: str
79-    valeur: str
80-    debut: int
81-    fin: int
82-    source: str = "heuristique"
83-    confiance: float = 0.5
84-    candidats: list[str] = field(default_factory=list)
85-    langue: str = "und"
86-    script: str = SCRIPT_NEUTRE
87-    meta: dict = field(default_factory=dict)
88-
89-    def json(self) -> dict:
90-        return {
91-            "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json, sys\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\na=bl.Heuristique()\nFER={\"DET\",\"PREP\",\"CONJ\",\"PRON\",\"AUX\",\"PONCT\"}\nfor nom,p in [(\"34M\", … [957 caractères tronqués]`

  ```
== 34M
  greedy     sans_verbe=3/20 de_parmi_fermes=54/308 (0.175) types_fermes=25 pos=895
  top40_0.8  sans_verbe=0/20 de_parmi_fermes=7/277 (0.025) types_fermes=42 pos=705
  top20_0.5  sans_verbe=0/20 de_parmi_fermes=15/241 (0.062) types_fermes=37 pos=770
== 100M
  greedy     sans_verbe=8/20 de_parmi_fermes=304/467 (0.651) types_fermes=22 pos=705
  top40_0.8  sans_verbe=0/20 de_parmi_fermes=45/203 (0.222) types_fermes=40 pos=554
  top20_0.5  sans_verbe=0/20 de_parmi_fermes=143/298 (0.480) types_fermes=27 pos=641
  ```

- **bash** `{"command": "sleep 90; date; ps -o pid,etime,pcpu -p 318459; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader; ls -la /tmp/banc-generation-alea-100m-128o.json 2>/dev/null || echo \"pas de sortie\"", "description": "Attend le contrôle aléatoire 100M", "timeoutMs": 180000 … [1 caractères tronqués]`

  ```
mer 18 nov 2026 09:09:00 EST
    PID     ELAPSED %CPU
 318459       03:56 1590
0, 4 MiB, 0 %
1, 124 MiB, 0 %
pas de sortie
  ```

### 🤖 Assistant

⏵ Vérification de la cohérence greedy 64 → 128 octets

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\na=json.load(open(\"reports/banc-generation-100m.json\"))[\"reglages\"][\"greedy\"][\"lignes\"]\nb=json.load(open(\"/tmp/banc-generation-100m-128o.json\"))[\"reglages\"][\"gree … [346 caractères tronqués]`

  ```
prefixes identiques: 20/20
  ```

- **job_output** `{"job_id": "bash-326", "timeout_ms": 180000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sleep 60; date; ps -o pid,etime,pcpu -p 318459; ls -la /tmp/banc-generation-alea-100m-128o.json 2>/dev/null || echo \"pas de sortie\"", "description": "Vérifie la fin du contrôle aléatoire", "timeoutMs": 120000}`

  ```
mer 18 nov 2026 09:10:44 EST
    PID     ELAPSED %CPU
-rw-r--r--. 1 stephane stephane 32910 18 nov 09:10 /tmp/banc-generation-alea-100m-128o.json
  ```

### 👤 Utilisateur

background job bash-326 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time /home/stephane/gpu-env/bin/python tools/banc_generation.py --modele work/n2ac/mix1024-100m.pt --aleatoire --n 128 --sortie /tmp/banc-generation-alea-100m-128o.json 2>&1 | tail -20) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Contrôle aléatoire 100 M terminé, calcul de sa grammaticalité

- **job_output** `{"job_id": "bash-326"}`

  ```
écrit : /tmp/banc-generation-alea-100m-128o.json
greedy       mots_valides=0.315 distinct_2=1.000 repetition=1 echo=0.00 octets/s=28.6
top40_0.8    mots_valides=0.263 distinct_2=1.000 repetition=1 echo=0.00 octets/s=26.9
top20_0.5    mots_valides=0.297 distinct_2=1.000 repetition=1 echo=0.00 octets/s=16.6
[stderr]

real	5m37,226s
user	87m2,369s
sys	0m7,685s
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py --entree /tmp/banc-generation-100m-128o.json --controle /tmp/banc-generation-alea-100m-128o.json --sortie /tmp/banc-grammaticalite-100m-controle-100m.json && echo \"=== m … [483 caractères tronqués]`

  ```
natif     greedy     gv=1.45 gn=1.55 mots=35.2 ciment=0.661 attaches=0.905 sans_verbe=0.40
natif     top40_0.8  gv=4.00 gn=1.85 mots=27.7 ciment=0.375 attaches=0.771 sans_verbe=0.00
natif     top20_0.5  gv=2.65 gn=1.90 mots=32.0 ciment=0.461 attaches=0.871 sans_verbe=0.00
aleatoire greedy     gv=4.75 gn=3.15 mots=90.4 ciment=0.763 attaches=0.558 sans_verbe=0.00
aleatoire top40_0.8  gv=5.25 gn=3.45 mots=105.1 ciment=0.816 attaches=0.757 sans_verbe=0.05
aleatoire top20_0.5  gv=3.85 gn=2.05 mots=87.4 ciment=0.795 attaches=0.672 sans_verbe=0.00
=== métriques génération aléatoire 100M ===
aleatoire True n 128
greedy mots_valides 0.3154 rep 1 distinct2 1.0 octets/s 28.6
top40_0.8 mots_valides 0.2634 rep 1 distinct2 1.0 octets/s 26.9
top20_0.5 mots_valides 0.2969 rep 1 distinct2 1.0 octets/s 16.6
  ```

### 🤖 Assistant

⏵ Vérification CPU/GPU du greedy 34 M et composition du contrôle aléatoire

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json, collections\na=json.load(open(\"reports/banc-generation.json\"))[\"reglages\"][\"greedy\"][\"lignes\"]\nb=json.load(open(\"reports/banc-generation-34m-64o.json\"))[\"reglages\ … [686 caractères tronqués]`

  ```
34M greedy : prefixes 64 o identiques au 128 o (CPU vs GPU) : 0/20
greedy mots 67 top5 [('���*ŭ�un�[��', 5), ('\x14', 5), ('g��\x08!ӭ��l�*�', 3), ('\x07����a\x19}g�r\x137i\x02�\x02�e�\\�\x12�\x14�\x00', 2), ('���*�f2g�ˏ[��', 2)]
top40_0.8 mots 101 top5 [('�', 2), ("�f&����7�+��*\x1b?]c�e����l�(zsu'i�\x00z:\x02ư�v߰��$l\x00wvw܋��g���ռ�f\x0el'#�g", 1), ('�\x11>h�˫/r�', 1), ('n*�ji*�', 1), ('l��3��\x12���(�y+ca\x05,c~ga"pdk�\x04%o�\x11-����', 1)]
top20_0.5 mots 89 top5 [('�', 2), ('x[!m>�=t�sm', 1), ('e�/�r��g���d��h6ܔ�', 1), ('yp}���\x128�\x12��\x01ʹp-z�b�e\x07�g��6��k��va3���r���nԯw�u\x19\x10j', 1), ('f���^�����a�3�[qsx�j�\x14\x14��w�u�\x0fa̺�zi\x02e�gl�', 1)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\na=json.load(open(\"reports/banc-generation.json\"))[\"reglages\"][\"greedy\"][\"lignes\"]\nb=json.load(open(\"reports/banc-generation-34m-64o.json\"))[\"reglages\"][\"greedy\" … [243 caractères tronqués]`

  ```
PROMPT La France est un pays
  128: 'La France est un pays don d d da d 20 n dese de 1 20 20 aba dele  1  la  1 20 20 201 1  19 1 190 20 '
   64: 'La France est un pays don d d da d 20 n dese de 1 20 20 aba dele  1  la  1 20 20 201 '
PROMPT Dans les années 1950
  128: 'Dans les années 1950 le por le de la da la le e e de de e ena 20 1 esa la en ena da da es  da da es '
   64: 'Dans les années 1950 le por le de la da la le e e de de e ena 20 1 esa la en ena da '
PROMPT Il était une fois
  128: 'Il était une fois de de pre dile de de de e de d ese e esinanoré e e ene e es ece es e 1 e e e e e e'
   64: 'Il était une fois de de pre dile de de de e de d ese e esinanoré e e ene e es ec'
PROMPT Le chat
  128: 'Le chatin de en 1 1 de a 1 la da 1 1 1  1 19 1 1 19 1 19 li 19 19 1 19 1 1 19 19 19 A 1 19 1 199 191'
   64: 'Le chatin de en 1 1 de a 1 la da 1 1 1  1 19 1 1 19 1 19 li 19 19 1 19 '
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\na=json.load(open(\"reports/banc-generation.json\"))[\"reglages\"][\"greedy\"][\"lignes\"]  # 128, CPU\nb=json.load(open(\"reports/banc-generation-34m-64o.json\"))[\"reglages\" … [267 caractères tronqués]`

  ```
34M greedy : prefixes 64 o identiques au 128 o (CPU vs GPU) : 20/20
  ```

### 🤖 Assistant

⏵ Adoption du contrôle apparié 100 M et calcul du tableau final

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py --entree /tmp/banc-generation-100m-128o.json --controle /tmp/banc-generation-alea-100m-128o.json --sortie reports/banc-grammaticalite-100m.json && echo \"=== JSON final = … [134 caractères tronqués]`

  ```
natif     greedy     gv=1.45 gn=1.55 mots=35.2 ciment=0.661 attaches=0.905 sans_verbe=0.40
natif     top40_0.8  gv=4.00 gn=1.85 mots=27.7 ciment=0.375 attaches=0.771 sans_verbe=0.00
natif     top20_0.5  gv=2.65 gn=1.90 mots=32.0 ciment=0.461 attaches=0.871 sans_verbe=0.00
aleatoire greedy     gv=4.75 gn=3.15 mots=90.4 ciment=0.763 attaches=0.558 sans_verbe=0.00
aleatoire top40_0.8  gv=5.25 gn=3.45 mots=105.1 ciment=0.816 attaches=0.757 sans_verbe=0.05
aleatoire top20_0.5  gv=3.85 gn=2.05 mots=87.4 ciment=0.795 attaches=0.672 sans_verbe=0.00
=== JSON final ===
{
 "natif": {
  "greedy": {
   "textes": 20,
   "gv_moyen": 1.45,
   "gn_moyen": 1.55,
   "mots_moyen": 35.2,
   "ciment": 0.6611,
   "attaches": 0.9052,
   "sans_verbe": 0.4
  },
  "top40_0.8": {
   "textes": 20,
   "gv_moyen": 4.0,
   "gn_moyen": 1.85,
   "mots_moyen": 27.7,
   "ciment": 0.3748,
   "attaches": 0.7708,
   "sans_verbe": 0.0
  },
  "top20_0.5": {
   "textes": 20,
   "gv_moyen": 2.65,
   "gn_moyen": 1.9,
   "mots_moyen": 32.0,
   "ciment": 0.4605,
   "attaches": 0.8707,
   "sans_verbe": 0.0
  }
 },
 "aleatoire": {
  "greedy": {
   "textes": 20,
   "gv_moyen": 4.75,
   "gn_moyen": 3.15,
   "mots_moyen": 90.4,
   
… [409 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nref=json.load(open(\"reports/banc-grammaticalite.json\"))\nnew=json.load(open(\"/tmp/banc-grammaticalite-100m-controle-100m.json\"))\ngen34=json.load(open(\"reports/banc-gener … [1405 caractères tronqués]`

  ```
| source | réglage | GV | GN | mots | ciment | attaches | sans verbe | GV/100 mots |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **34 M** | greedy | 6.90 | 2.85 | 44.8 | 0.3346 | 0.7368 | 0.15 | 15.4 |
| **34 M** | top40_0.8 | 6.35 | 3.15 | 35.2 | 0.3769 | 0.8870 | 0.00 | 18.0 |
| **34 M** | top20_0.5 | 5.85 | 3.15 | 38.5 | 0.3098 | 0.7892 | 0.00 | 15.2 |
| **100 M** | greedy | 1.45 | 1.55 | 35.2 | 0.6611 | 0.9052 | 0.40 | 4.1 |
| **100 M** | top40_0.8 | 4.00 | 1.85 | 27.7 | 0.3748 | 0.7708 | 0.00 | 14.4 |
| **100 M** | top20_0.5 | 2.65 | 1.90 | 32.0 | 0.4605 | 0.8707 | 0.00 | 8.3 |

| 34 M aléatoire | greedy | 2.30 | 1.80 | 62.5 | 0.7912 | 0.7466 | 0.00 | 3.7 |
| 34 M aléatoire | top40_0.8 | 3.35 | 2.80 | 87.8 | 0.8008 | 0.6503 | 0.10 | 3.8 |
| 34 M aléatoire | top20_0.5 | 4.00 | 2.35 | 89.6 | 0.7959 | 0.6701 | 0.05 | 4.5 |
| 100 M aléatoire | greedy | 4.75 | 3.15 | 90.4 | 0.7627 | 0.5580 | 0.00 | 5.3 |
| 100 M aléatoire | top40_0.8 | 5.25 | 3.45 | 105.1 | 0.8157 | 0.7575 | 0.05 | 5.0 |
| 100 M aléatoire | top20_0.5 | 3.85 | 2.05 | 87.4 | 0.7954 | 0.6722 | 0.00 | 4.4 |

| modèle | réglage | mots valides | distinct-2 | répétition |
|---|---|---:|---:|---:|
| 34 M | greedy | 0.87
… [233 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des GV détectés : verbes réels ou artefacts de boucle ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json, sys, collections\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\na=bl.Heuristique()\nfor nom,p in [(\"34M\",\"reports/banc-generation.json\"),(\"100M\",\"/ … [603 caractères tronqués]`

  ```
===== 34M greedy
  ex GV: ['est', 'est un pays don']
  top GV: [('a', 58), ('de', 6), ('d', 5), ('A', 3), ('A Ba', 3), ('a a', 3), ('est', 2), ('a da', 2), ('a e e', 2), ('e', 2), ('est un pays don', 1), ('en ena da da es  da da es', 1), ('en e lala lana e dese', 1), ('était', 1), ('était une fois', 1)]
===== 100M greedy
  ex GV: ['est', 'est un pays', 'landes']
  top GV: [('est', 3), ('ss', 3), ('mise', 2), ('est un pays', 1), ('landes', 1), ('es', 1), ('se mise', 1), ('était', 1), ('était une fois', 1), ('jouent', 1), ('lantis', 1), ('a décidé late', 1), ('este', 1), ('alis es ale', 1), ('es ale', 1)]
  ```

### 🤖 Assistant

⏵ Recherche des contextes de « a » qui gonflent les GV du 34 M

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json, sys, collections\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\na=bl.Heuristique()\nd=json.load(open(\"reports/banc-generation.json\"))\nbest=[]\nfor l in … [413 caractères tronqués]`

  ```
--- 39 GV | La science
La science a a d A destome de de  a d e f   a d a   d frine a d ana  da lan 1 an a a de a a a a a a a  1 a  a de a a a a a a a a a a a  a 
GV: ['a', 'a a', 'a', 'd', 'A destome', 'a', 'a', 'd', 'a', 'a', 'an', 'a', 'a a', 'a', 'de', 'a', 'a a a a a a a  1 a  a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'de', 'a', 'a a a a a a a a a a a  a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
--- 37 GV | La mer
La meri a  a a a a a a a a popra ux a d du  a da d a asa a a de a da la a do e 1 a de a esa a da lla d a A  a de a a a a pr a de pre d
GV: ['a', 'a  a a a a a a a a popra ux a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a popra ux', 'a', 'a da', 'd', 'a asa', 'a asa a a', 'a', 'a', 'de', 'a da', 'a do e', 'a do e 1 a', 'a', 'de', 'a esa', 'a esa a da lla', 'a da lla', 'd', 'a', 'a A  a', 'a', 'de', 'a', 'a a a a pr a', 'a', 'a', 'a pr', 'a']
--- 11 GV | La musique
La musique d  de A de etris d da  fata  A  A A A A A Ba  a A A si A  A A A A Ba Ala A Ba A Ba A A A A Ana An Am Aba Ana A Ana A An A A Ala
GV: ['A', 'A  A A A A A Ba  a A A', 'A Ba', 'a', 'A', 'A Ba', 'A Ba', 'A Ana An Am Aba Ana', 'A Ana', 'A An', 'A Ala']
  ```

### 🤖 Assistant

⏵ Analyse des verbes produits : types et concentration

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json, sys, collections\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\na=bl.Heuristique()\nfor nom,p in [(\"34M\",\"reports/banc-generation.json\"),(\"100M\",\"/ … [591 caractères tronqués]`

  ```
===== 34M
  greedy     verbes= 17 types= 8 top=[('es', 7), ('est', 4), ('était', 1), ('espenes', 1), ('jouent', 1), ('esed', 1)]
  top40_0.8  verbes= 11 types= 9 top=[('est', 3), ('esovors', 1), ('es', 1), ('était', 1), ('ponecunovons', 1), ('jouent', 1)]
  top20_0.5  verbes= 15 types= 7 top=[('es', 7), ('est', 3), ('était', 1), ('desespes', 1), ('jouent', 1), ('pis', 1)]
===== 100M
  greedy     verbes= 19 types=10 top=[('es', 5), ('est', 3), ('ss', 3), ('landes', 2), ('était', 1), ('jouent', 1)]
  top40_0.8  verbes= 41 types=38 top=[('és', 3), ('lus', 2), ('est', 1), ('ables', 1), ('blandes', 1), ('mmpois', 1)]
  top20_0.5  verbes= 37 types=31 top=[('es', 3), ('est', 2), ('ales', 2), ('demis', 2), ('ans', 2), ('attes', 1)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json, sys\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\na=bl.Heuristique()\nd=json.load(open(\"reports/banc-generation.json\"))\nt=[l for l in d[\"reglages\"][ … [406 caractères tronqués]`

  ```
La science a a d A destome de de  a d e f   a d a   d frine a d ana  da lan 1 an a a de a a a a a a a  1 a  a de a a a a a a a a a a a  a 
POS: [('La', 'DET'), ('science', 'NOUN'), ('a', 'PREP'), ('a', 'PREP'), ('d', 'PREP'), ('A', 'PREP'), ('destome', 'NOUN'), ('de', 'PREP'), ('de', 'PREP'), ('a', 'PREP'), ('d', 'PREP'), ('e', 'NOUN'), ('f', 'NOUN'), ('a', 'PREP'), ('d', 'PREP'), ('a', 'PREP'), ('d', 'PREP'), ('frine', 'NOUN'), ('a', 'PREP'), ('d', 'PREP'), ('ana', 'NOUN'), ('da', 'NOUN'), ('lan', 'NOUN'), ('1', 'NUM'), ('an', 'NOUN'), ('a', 'PREP'), ('a', 'PREP'), ('de', 'PREP'), ('a', 'PREP'), ('a', 'PREP'), ('a', 'PREP'), ('a', 'PREP'), ('a', 'PREP'), ('a', 'PREP'), ('a', 'PREP'), ('1', 'NUM'), ('a', 'PREP'), ('a', 'PREP'), ('de', 'PREP'), ('a', 'PREP')]
SYNT: [('La science', 'GN', {'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'La science', 'cible': 'd', 'candidats': [{'span': {'debut': 15, 'fin': 16}, 'cible': 'd', 'source': 'heuristique'}, {'span': {'debut': 54, 'fin': 59}, 'cible': 'frine', 'source': 'heuristique'}, {'span': {'debut': 0, 'fin': 10}, 'cible': 'La science', 'source': 'heuristique'}, {'span': {'debut': 1, 'fin': 2}, 'cible': 'a', 'source': 'heuristi
… [5376 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test d'un GV « à appui verbal » : le banc compte-t-il vraiment des verbes ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json, sys\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\na=bl.Heuristique()\nfor nom,p in [(\"34M\",\"reports/banc-generation.json\"),(\"100M\",\"/tmp/banc-gene … [1065 caractères tronqués]`

  ```
===== 34M
  greedy     GV=138 GV_appui_verbal=16 GV_tete_verbale=13 tokens_VERB/AUX= 17 par_texte=[2, 1, 4, 0, 0, 1, 1, 3, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0]
  top40_0.8  GV=127 GV_appui_verbal=16 GV_tete_verbale=12 tokens_VERB/AUX= 11 par_texte=[3, 1, 5, 0, 0, 1, 0, 1, 0, 0, 2, 2, 0, 0, 0, 0, 1, 0, 0, 0]
  top20_0.5  GV=117 GV_appui_verbal=19 GV_tete_verbale=14 tokens_VERB/AUX= 15 par_texte=[2, 2, 5, 0, 0, 4, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 0]
===== 100M
  greedy     GV= 29 GV_appui_verbal=20 GV_tete_verbale=19 tokens_VERB/AUX= 19 par_texte=[3, 1, 2, 1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 1, 0, 0, 0, 3, 0, 3]
  top40_0.8  GV= 80 GV_appui_verbal=43 GV_tete_verbale=34 tokens_VERB/AUX= 41 par_texte=[4, 3, 4, 1, 1, 4, 1, 1, 1, 1, 3, 2, 0, 4, 3, 2, 1, 3, 2, 2]
  top20_0.5  GV= 53 GV_appui_verbal=37 GV_tete_verbale=35 tokens_VERB/AUX= 37 par_texte=[6, 2, 3, 0, 2, 4, 0, 1, 2, 0, 2, 3, 1, 0, 2, 3, 0, 1, 3, 2]
  ```

### 🤖 Assistant

⏵ Envoi d'un point d'étape au parent (taille réelle, budget d'entraînement, confound)

- **send_message** `{"agent_id": "d67a9bb1-090e-4f69-baf2-a831c00aa275", "message": "Point d'étape — banc de grammaticalité 100 M (mesure terminée, rapport en cours d'écriture).\n\n1) Le fichier work/n2ac/mix1024-100m.pt ne fait pas 100 M : 73 366 568 paramètres (vérifié dans le checkpoint et le .pt.json), et il n'a qu … [1719 caractères tronqués]`

  ```
message delivered to agent d67a9bb1-090e-4f69-baf2-a831c00aa275
  ```

### 🤖 Assistant

⏵ Vérification des positions (RoPE vs absolues) avant d'écrire le rapport

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport torch\nfor p in [\"work/n2ac/mix1024-60k.pt\",\"work/n2ac/mix1024-100m.pt\"]:\n    ck=torch.load(p,map_location=\"cpu\",weights_only=False)\n    ks=[k for k in ck[\"state\"] if (\"r … [296 caractères tronqués]`

  ```
work/n2ac/mix1024-60k.pt clés rope/pos: ['pos.weight']
  config: {'vocab': 256, 'd_model': 384, 'n_blocks': 6, 'n_heads': 4, 'expert_hidden': 512, 'n_experts': 8, 'top_k': 2, 'kwta': 0.25, 'window': 1024, 'max_pos': 2048, 'thought_steps': 2, 'early_blocks': (1, 3, 5), 'rsn_dim': 120}
work/n2ac/mix1024-100m.pt clés rope/pos: ['pos.weight']
  config: {'vocab': 256, 'd_model': 640, 'n_blocks': 6, 'n_heads': 4, 'expert_hidden': 640, 'n_experts': 8, 'top_k': 2, 'kwta': 0.25, 'window': 256, 'max_pos': 2048, 'thought_steps': 2, 'early_blocks': (1, 3, 5), 'rsn_dim': 120}
=== code rope ===
  ```

### 👤 Utilisateur

Agent d67a9bb1-090e-4f69-baf2-a831c00aa275 sent a message: 
Important : ton JSON `banc-grammaticalite-100m.json` compare le 100 M (généré à **n=64**) au contrôle `reports/banc-generation-aleatoire.json` (généré à **n=128**) — les textes n'ont pas la même longueur (le contrôle a 90 mots, le natif 35), donc gv_moyen et ciment ne sont pas comparables et le contrôle paraît « meilleur » (ciment 0,76 contre 0,66).

J'ai créé le contrôle APPARIÉ : `reports/banc-generation-alea-64o.json` (poids au hasard, n=64, même graine). Refais la passe `banc_grammaticalite.py` avec `--controle reports/banc-generation-alea-64o.json`, réécris `banc-grammaticalite-100m.json`, et dans la fiche : (1) compare au 34 M en gardant la réserve que son JSON de référence est en n=128 ; (2) note que le GV baisse de 6,9 (34 M) à 1,45 (100 M) — est-ce la longueur, le modèle, ou l'analyseur ? (3) le contrôle apparié. Donne les deux chiffres (n=128 historique, n=64 apparié) plutôt que de mélanger.

### 👤 Utilisateur

Agent d67a9bb1-090e-4f69-baf2-a831c00aa275 sent a message: 
Excellent point d'étape, et tes deux réserves sont les bonnes : (1) le « 100 M » fait 73,4 M et n'a que 3 000 pas (contre 30 000 pour le 34 M) — la comparaison confond échelle et entraînement ; (2) GV et ciment mesurent surtout le token de boucle (« a » vs « de ») et il faut le GV/100 mots. Garde tout ça dans la fiche, avec les deux chiffres bruts ET normalisés.

De mon côté, la confusion « 3 000 pas » est en cours de traitement : j'entraîne le 73 M (init = ce checkpoint, lr 1e-4, AMP, seq 1024, lot 8, val épinglée) pour 10 000 pas — il sera à 13 000 pas vers 10 h 05. Si tu veux, prépare ton rapport pour accueillir ce point : je te donnerai le banc de génération du checkpoint r1 (mêmes 20 prompts, n=128) et tu pourras dire si la répétition et le token de boucle bougent avec l'entraînement. Termine d'abord la fiche actuelle (73 M à 3 000 pas) avec ses réserves ; on fera une seconde fiche pour r1.

### 🤖 Assistant

⏵ Correction du malentendu n=64/n=128 et calcul des deux passes appariées n=64

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 100M n=64 vs controle 34M alea n=64 ===\" && /home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py --entree reports/banc-generation-100m.json --controle reports/banc-generation-alea-64o.json --sortie /tmp/banc-gra … [368 caractères tronqués]`

  ```
=== 100M n=64 vs controle 34M alea n=64 ===
natif     greedy     gv=1.10 gn=1.30 mots=19.9 ciment=0.693 attaches=0.870 sans_verbe=0.45
natif     top40_0.8  gv=2.15 gn=1.95 mots=15.1 ciment=0.375 attaches=0.814 sans_verbe=0.00
natif     top20_0.5  gv=1.60 gn=1.80 mots=17.4 ciment=0.471 attaches=0.837 sans_verbe=0.10
aleatoire greedy     gv=1.50 gn=1.75 mots=47.5 ciment=0.790 attaches=0.775 sans_verbe=0.05
aleatoire top40_0.8  gv=2.05 gn=2.10 mots=48.6 ciment=0.795 attaches=0.739 sans_verbe=0.05
aleatoire top20_0.5  gv=2.15 gn=2.00 mots=51.6 ciment=0.819 attaches=0.685 sans_verbe=0.00
=== 34M n=64 vs controle 34M alea n=64 ===
natif     greedy     gv=3.35 gn=2.25 mots=24.6 ciment=0.427 attaches=0.765 sans_verbe=0.20
natif     top40_0.8  gv=3.10 gn=2.40 mots=15.8 ciment=0.343 attaches=0.773 sans_verbe=0.05
natif     top20_0.5  gv=3.40 gn=2.30 mots=20.3 ciment=0.342 attaches=0.668 sans_verbe=0.05
aleatoire greedy     gv=1.50 gn=1.75 mots=47.5 ciment=0.790 attaches=0.775 sans_verbe=0.05
aleatoire top40_0.8  gv=2.05 gn=2.10 mots=48.6 ciment=0.795 attaches=0.739 sans_verbe=0.05
aleatoire top20_0.5  gv=2.15 gn=2.00 mots=51.6 ciment=0.819 attaches=0.685 sans_verbe=0.00
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfor p in [\"reports/banc-generation-100m.json\",\"reports/banc-generation-34m-64o.json\",\"reports/banc-generation-alea-64o.json\",\"/tmp/banc-generation-100m-128o.json\",\"/t … [214 caractères tronqués]`

  ```
reports/banc-generation-100m.json n= 64 aleatoire= False modele= work/n2ac/mix1024-100m.pt
reports/banc-generation-34m-64o.json n= 64 aleatoire= False modele= work/n2ac/mix1024-60k.pt
reports/banc-generation-alea-64o.json n= 64 aleatoire= True modele= work/n2ac/mix1024-60k.pt
/tmp/banc-generation-100m-128o.json n= 128 aleatoire= False modele= work/n2ac/mix1024-100m.pt
/tmp/banc-generation-alea-100m-128o.json n= 128 aleatoire= True modele= work/n2ac/mix1024-100m.pt
  ```

### 🤖 Assistant

⏵ Calcul du tableau complet n=128 et n=64, avec ratios au hasard

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\n# n=128\nr34_128=json.load(open(\"reports/banc-grammaticalite.json\"))\nr100_128=json.load(open(\"/tmp/banc-grammaticalite-100m-controle-100m.json\"))  # 100M natif + 100M ale … [2243 caractères tronqués]`

  ```
### n=128
34M        greedy     GV=6.90 GN=2.85 mots=44.8 ciment=0.3346 attaches=0.7368 sans=0.15 GV100=15.4
34M        top40_0.8  GV=6.35 GN=3.15 mots=35.2 ciment=0.3769 attaches=0.8870 sans=0.00 GV100=18.0
34M        top20_0.5  GV=5.85 GN=3.15 mots=38.5 ciment=0.3098 attaches=0.7892 sans=0.00 GV100=15.2
100M       greedy     GV=1.45 GN=1.55 mots=35.2 ciment=0.6611 attaches=0.9052 sans=0.40 GV100=4.1
100M       top40_0.8  GV=4.00 GN=1.85 mots=27.7 ciment=0.3748 attaches=0.7708 sans=0.00 GV100=14.4
100M       top20_0.5  GV=2.65 GN=1.90 mots=32.0 ciment=0.4605 attaches=0.8707 sans=0.00 GV100=8.3
34M alea   greedy     GV=2.30 GN=1.80 mots=62.5 ciment=0.7912 attaches=0.7466 sans=0.00 GV100=3.7
34M alea   top40_0.8  GV=3.35 GN=2.80 mots=87.8 ciment=0.8008 attaches=0.6503 sans=0.10 GV100=3.8
34M alea   top20_0.5  GV=4.00 GN=2.35 mots=89.6 ciment=0.7959 attaches=0.6701 sans=0.05 GV100=4.5
100M alea  greedy     GV=4.75 GN=3.15 mots=90.4 ciment=0.7627 attaches=0.5580 sans=0.00 GV100=5.3
100M alea  top40_0.8  GV=5.25 GN=3.45 mots=105.1 ciment=0.8157 attaches=0.7575 sans=0.05 GV100=5.0
100M alea  top20_0.5  GV=3.85 GN=2.05 mots=87.4 ciment=0.7954 attaches=0.6722 sans=0.00 GV100=4.4

### n=64
… [1194 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Passe n=128 avec le contrôle 34 M (référence), puis assemblage du JSON à deux sections

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py --entree /tmp/banc-generation-100m-128o.json --controle reports/banc-generation-aleatoire.json --sortie /tmp/banc-grammaticalite-100m-128o-controle34.json && echo \"=== a … [1083 caractères tronqués]`

  ```
natif     greedy     gv=1.45 gn=1.55 mots=35.2 ciment=0.661 attaches=0.905 sans_verbe=0.40
natif     top40_0.8  gv=4.00 gn=1.85 mots=27.7 ciment=0.375 attaches=0.771 sans_verbe=0.00
natif     top20_0.5  gv=2.65 gn=1.90 mots=32.0 ciment=0.461 attaches=0.871 sans_verbe=0.00
aleatoire greedy     gv=2.30 gn=1.80 mots=62.5 ciment=0.791 attaches=0.747 sans_verbe=0.00
aleatoire top40_0.8  gv=3.35 gn=2.80 mots=87.8 ciment=0.801 attaches=0.650 sans_verbe=0.10
aleatoire top20_0.5  gv=4.00 gn=2.35 mots=89.6 ciment=0.796 attaches=0.670 sans_verbe=0.05
=== assemblage ===
{
 "note": "n128 : 100 M natif, 128 octets, controle 34 M aleatoire n128 (reports/banc-generation-aleatoire.json). n64 : 100 M natif, 64 octets, controle 34 M aleatoire n64 (reports/banc-generation-alea-64o.json). controle_100m_n128 : controle scale-matched 100 M aleatoire n128 (poids au hasard, graine 1234).",
 "n128": {
  "natif": {
   "greedy": {
    "textes": 20,
    "gv_moyen": 1.45,
    "gn_moyen": 1.55,
    "mots_moyen": 35.2,
    "ciment": 0.6611,
    "attaches": 0.9052,
    "sans_verbe": 0.4
   },
   "top40_0.8": {
    "textes": 20,
    "gv_moyen": 4.0,
    "gn_moyen": 1.85,
    "mots_moyen": 27.7,
    "ciment": 0.3748
… [2428 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Envoi de la correction n=64/n=128 et des chiffres appariés au parent

- **send_message** `{"agent_id": "d67a9bb1-090e-4f69-baf2-a831c00aa275", "message": "Correction sur le n : mon JSON n'était pas n=64. Le 100 M a été généré à n=128 (/tmp/banc-generation-100m-128o.json) et le contrôle scale-matched aussi (/tmp/banc-generation-alea-100m-128o.json). Les 35 mots du natif et les 90 du contr … [1679 caractères tronqués]`

  ```
message delivered to agent d67a9bb1-090e-4f69-baf2-a831c00aa275
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche `rapport-grammaticalite-100m.md` avec les deux longueurs et les réserves

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "content": "# N4 — la grammaticalité du « 100 M » : moins de GV, plus de ciment, un banc piégé par la boucle\n\n> **Ligne de roadmap** : **N4** (l'usage du natif) · **Date** : 2026-11-18 · **Modèl … [19370 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Vérification du JSON, des liens et de l'état git

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python -m json.tool reports/banc-grammaticalite-100m.json >/dev/null && echo \"JSON valide\" && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport re, pathlib\np=pathlib.Path(\"reports/rapport-grammaticali … [399 caractères tronqués]`

  ```
JSON valide
liens: 15
OK   ../tools/banc_generation.py
OK   ../tools/banc_grammaticalite.py
OK   banc-grammaticalite-100m.json
OK   ../tools/banc_generation.py
OK   ../tools/banc_grammaticalite.py
OK   rapport-banc-generation.md
OK   rapport-banc-generation-100m.md
OK   banc-grammaticalite-100m.json
OK   banc-grammaticalite.json
OK   banc-generation.json
OK   banc-generation-aleatoire.json
OK   banc-generation-100m.json
OK   banc-generation-alea-64o.json
OK   banc-generation-34m-64o.json
OK   ../docs/pilotage/natif-plan.md
mots: 3516
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain; echo \"=== fichiers créés ===\"; ls -la reports/banc-grammaticalite-100m.json reports/rapport-grammaticalite-100m.md; echo \"=== diff outils ===\"; git diff --stat tools/banc_grammaticalite.py", "description": … [47 caractères tronqués]`

  ```
M journal/README.md
 M journal/sessions/8c024745-95cb-4885-9d0b-865142606b6d/digest.md
 M journal/sessions/8c024745-95cb-4885-9d0b-865142606b6d/rapport.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/c7e46dba-11cb-456b-a3b6-715428927f99/digest.md
 M journal/sessions/c7e46dba-11cb-456b-a3b6-715428927f99/rapport.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/digest.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/rapport.md
?? bench/checkpoint_bench.sh
?? journal/sessions/174fd5ef-1163-4983-85b5-9101752ad711/
?? journal/sessions/da0f2984-32d0-459d-a761-d3faf6a10b8a/
?? reports/banc-grammaticalite-100m.json
?? reports/rapport-a2.6-reconnaissance.md
?? reports/rapport-grammaticalite-100m.md
=== fichiers créés ===
-rw-r--r--. 1 stephane stephane  3064 18 nov 09:21 reports/banc-grammaticalite-100m.json
-rw-------. 1 stephane stephane 19839 18 nov 09:23 reports/rapport-grammaticalite-100m.md
=== diff outils ===
  ```

### 🤖 Assistant

⏵ Corrections de précision dans la fiche (greedy explicite, contrôle n=64, budget r1)

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "old_string": "> **Verdict** : à 128 octets (protocole du 34 M), le 100 M **perd les GV** (1,45 contre 6,90) et\n> **monte le ciment** (0,661 contre 0,335) ; à 64 octets (contrôle de longueur), le … [334 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "old_string": "- **Le modèle** : le 100 M produit moins de mots par texte (19,9 contre 24,6 à 64 octets) et\n  les concentre sur un token, « de ». Le 34 M boucle sur « a ». La classe du token de b … [342 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "new_string": "Le 34 M à 64 octets a été mesuré de la même façon :\n\n```bash\n/home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py \\\n    --entree reports/banc-generation-34m-64o.json  … [287 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "new_string": "| contrôle 34 M aléatoire | top-20 | 2,15 | 2,00 | 51,6 | 0,819 | 4,2 | 1,0 |\n\n*Le hasard est le 34 M aléatoire (seul contrôle n=64 disponible) ; le 100 M aléatoire n'a été\nmesur … [160 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "new_string": "Le banc lexical dit que le 100 M est **comparable ou meilleur** en greedy et top-40 (et qu'il\nrépète moins : 6 contre 15), tandis que le banc de grammaticalité dit qu'il a **près d … [270 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "new_string": "2. **La prochaine action est l'entraînement à parité**, pas le 300 M : amener le 73 M à un budget\n   comparable (**13 000 pas pour r1**, **30 000 pas pour la parité stricte** avec  … [418 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Clarification des contrôles utilisés dans les ratios (propre hasard vs 34 M)

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "new_string": "| 64 octets | 100 M | **1,8×** | 3,4× | 2,2× |\n\n*Lecture des contrôles : à 128 octets, chaque modèle est comparé à son propre aléatoire (34 M\npour le 34 M, 100 M pour le 100 M) ; … [731 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Relecture complète de la fiche

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md</path>
<type>file</type>
<content>
1: # N4 — la grammaticalité du « 100 M » : moins de GV, plus de ciment, un banc piégé par la boucle
2: 
3: > **Ligne de roadmap** : **N4** (l'usage du natif) · **Date** : 2026-11-18 · **Modèle mesuré** :
4: > `work/n2ac/mix1024-100m.pt` (**73,37 M** paramètres réels, 3 000 pas, PPL val **4,014**) ·
5: > **Référence** : `work/n2ac/mix1024-60k.pt` (**34,30 M**, 30 000 pas, PPL **2,404**) ·
6: > **Verdict** : en greedy, à 128 octets (protocole du 34 M), le 100 M **perd les GV** (1,45
7: > contre 6,90) et **monte le ciment** (0,661 contre 0,335) ; à 64 octets (contrôle de longueur),
8: > le même écart tient (1,10 contre 3,35 ; 0,693 contre 0,427). Mais **42 %** des GV du 34 M sont le seul token
9: > « a » et **46 %** des mots du 100 M sont « de » : GV et ciment mesurent surtout la **classe du
10: > token de boucle**. Le 100 M est **plus répétitif et moins divers** ; il n'est pas démontré
11: > « moins grammatical ». Le fichier fait **73,37 M** et **3 000 pas** (10× moins que le 34 M) :
12: > la comparaison d'échelle est confondue avec l'entraînement.
13: 
14: 
… [20427 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernières précisions de formulation (verbe « a », saturation lexicale, lecture r1)

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "new_string": "« a a » (3), « est » (2), « a da » (2), « a e e » (2). Les GV du 34 M sont donc massivement des\n**runs de « a »**, le plus souvent le verbe avoir sans accent, que l'analyseur étiqu … [513 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "new_string": "moins de GV** (6,90 / 1,45 = 4,76). Les deux axes ne mesurent pas la même chose : en greedy, les\nmots valides sont saturés dès 34 M, la structure non. C'est exactement la raison d' … [396 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "new_string": "répétition (6) et les mots valides (0,878). Si la part de « de » reste haute et que le GV/100 ne\nmonte pas vers 10–15 à 13 000 pas, le budget seul ne suffira probablement pas ; si  … [345 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérification des outils de documentation (périmètre reports) et du compte de mots

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"reports\\|RACINE\\|docs\" tools/taille_documents.py | head -20; echo \"=== revue ===\"; grep -n \"reports\\|glob\\|docs\" tools/revue_documentation.py | head -25; echo \"=== mots ===\"; wc -w reports/rapport-grammaticalite- … [66 caractères tronqués]`

  ```
11:Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
23:RACINE = pathlib.Path(__file__).resolve().parent.parent
28:    ("T0", "docs/pilotage/en-cours.md", 2000),
29:    ("T1", "docs/methode/organisation-du-depot.md", 1800),
30:    ("T1", "docs/methode/modularisation.md", 1600),
31:    ("T1", "docs/methode/relations-humaines.md", 1400),
32:    ("T0", "docs/methode/*.md", 1200),
33:    ("T1", "docs/README.md", 1000),
34:    ("T1", "docs/theorie/carte.md", 1100),
35:    ("T1", "docs/theorie/synthese/index.md", 2000),
36:    ("T1", "docs/theorie/synthese/0*.md", 2000),
37:    ("T1", "docs/pilotage/roadmap.md", 9000),
38:    ("T1", "docs/theorie/glossaire.md", 1500),
39:    ("T1", "docs/theorie/glossaire/0*.md", 5000),
40:    ("T1", "docs/theorie/glossaire/1*.md", 5000),
41:    ("T1", "docs/theorie/glossaire/README.md", 2000),
42:    ("T1", "docs/schemas/README.md", 1500),
43:    ("CARTE", "docs/theorie/glossaire/entrees/*.md", 150),
44:    ("T1", "reports/README.md", 2800),
47:    ("T1", "docs/pilotage/utilisation.md", 2500),
=== revue ===
5:  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
7:  3. annotat
… [1370 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Passe de revue documentaire ciblée sur la nouvelle fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 /home/stephane/gpu-env/bin/python tools/revue_documentation.py > /tmp/revue.txt 2>&1; code=$?; echo \"exit=$code\"; echo \"=== lignes concernant la fiche ===\"; grep -n -i \"grammaticalite-100m\\|rapport-grammaticalite\"  … [171 caractères tronqués]`

  ```
exit=1
=== lignes concernant la fiche ===
aucune
=== fin ===
  revue de documentation · 794 fiche(s) · 885 JSON · 128 doc(s) · 90 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · compteurs : en-cours.md dit 792 fichiers, le disque en a 794
  ```

### 🤖 Assistant

⏵ Vérification des tableaux Markdown de la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,40p' tools/porte-tableaux.sh 2>/dev/null; echo \"=== run ===\"; timeout 120 bash tools/porte-tableaux.sh > /tmp/tableaux.txt 2>&1; code=$?; echo \"exit=$code\"; tail -20 /tmp/tableaux.txt", "description": "Lance la porte de … [33 caractères tronqués]`

  ```
#!/bin/bash
# porte-tableaux.sh — un tableau Markdown qui ne rend pas est un tableau qui n'existe PAS.
#
# POURQUOI CETTE PORTE EXISTE. Le 13/10, le premier tableau de `docs/etat-cerveau.md` s'affichait
# comme du TEXTE dans docwatch : une seule ligne (`| **C2 (cycle 2 régions)** | … |`) avait
# **4 cellules pour 5 colonnes** — un lien qui avait glissé d'une colonne. Le rendu (mistune,
# puis markdown_it, puis markdown) refuse alors le tableau ENTIER, sans rien dire : les 13 lignes
# disparaissent de la page et personne ne le voit, parce que le texte est toujours là, en gris.
#
# CE QU'ELLE VÉRIFIE (trois conditions, toutes nécessaires au rendu) :
#   1. l'en-tête et le séparateur d'un tableau ont le MÊME nombre de cellules ;
#   2. chaque ligne du corps a ce nombre de cellules ;
#   3. aucun `\|` ne subsiste : mistune ne le déséchappe NI dans un espace de code NI dans la
#      prose (il s'affiche alors littéralement). Pour une barre de valeur absolue dans du code,
#      on écrit `∣` (U+2223), qui rend partout et ne casse pas la lecture.
# Les tableaux DANS une citation (`> | … |`) sont valides et vérifiés aussi.
#
# CE QU'ELLE NE VÉRIFIE PAS : les tableaux « écrasés » sur une se
… [1141 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle final des fichiers et de l'absence de modification de code

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 644 reports/rapport-grammaticalite-100m.md && ls -la reports/banc-grammaticalite-100m.json reports/rapport-grammaticalite-100m.md && echo \"=== git diff code ===\" && git diff --stat -- tools/banc_grammaticalite.py tools/banc_g … [255 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane  3064 18 nov 09:21 reports/banc-grammaticalite-100m.json
-rw-r--r--. 1 stephane stephane 20618 18 nov 09:27 reports/rapport-grammaticalite-100m.md
=== git diff code ===
(vide = aucune modification)
=== mes fichiers ===
?? reports/banc-grammaticalite-100m.json
?? reports/rapport-grammaticalite-100m.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nd=json.load(open(\"reports/banc-grammaticalite-100m.json\"))\nprint(\"clés:\", list(d))\nfor section in [\"n128\",\"n64\"]:\n    print(section, \"natif greedy:\", d[section][\ … [295 caractères tronqués]`

  ```
clés: ['note', 'n128', 'n64', 'controle_100m_n128']
n128 natif greedy: {'textes': 20, 'gv_moyen': 1.45, 'gn_moyen': 1.55, 'mots_moyen': 35.2, 'ciment': 0.6611, 'attaches': 0.9052, 'sans_verbe': 0.4} | controle greedy: 2.3 0.7912
n64 natif greedy: {'textes': 20, 'gv_moyen': 1.1, 'gn_moyen': 1.3, 'mots_moyen': 19.9, 'ciment': 0.6927, 'attaches': 0.8698, 'sans_verbe': 0.45} | controle greedy: 1.5 0.7904
controle_100m_n128 greedy: {'textes': 20, 'gv_moyen': 4.75, 'gn_moyen': 3.15, 'mots_moyen': 90.4, 'ciment': 0.7627, 'attaches': 0.558, 'sans_verbe': 0.0}
  ```

### 🤖 Assistant

⏵ Ajout de la traçabilité des sources de contrôle dans la fiche

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "new_string": "*Lecture des contrôles : à 128 octets, chaque modèle est comparé à son propre aléatoire (34 M\npour le 34 M, 100 M pour le 100 M) ; à 64 octets, les deux sont comparés au 34 M aléat … [399 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md": file changed since it was read — re-read the file, then retry
  ```

### 🤖 Assistant

⏵ Le fichier a changé : relecture de la section concernée avant édition

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && stat -c '%y %s' reports/rapport-grammaticalite-100m.md; grep -n \"Lecture des contrôles\" -A4 -B2 reports/rapport-grammaticalite-100m.md", "description": "Vérifie la modification et le passage concerné"}`

  ```
2026-11-18 09:27:14.622776469 -0500 20618
180-| 64 octets | 100 M | **1,8×** | 3,4× | 2,2× |
181-
182:*Lecture des contrôles : à 128 octets, chaque modèle est comparé à son propre aléatoire (34 M
183-pour le 34 M, 100 M pour le 100 M) ; à 64 octets, les deux sont comparés au 34 M aléatoire,
184-seul contrôle n=64 disponible.*
185-
186-**Ce que le contrôle dit.** Le 34 M est **3,4 à 4,7× au-dessus de son bruit**, stable d'une
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "offset": 175, "limit": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md</path>
<type>file</type>
<content>
175: | longueur | modèle | greedy | top-40 | top-20 |
176: |---|---|---:|---:|---:|
177: | 128 octets | 34 M | **4,2×** | **4,7×** | **3,4×** |
178: | 128 octets | 100 M | **0,8×** | 2,9× | 1,9× |
179: | 64 octets | 34 M | **4,3×** | **4,7×** | **4,0×** |
180: | 64 octets | 100 M | **1,8×** | 3,4× | 2,2× |
181: 
182: *Lecture des contrôles : à 128 octets, chaque modèle est comparé à son propre aléatoire (34 M
183: pour le 34 M, 100 M pour le 100 M) ; à 64 octets, les deux sont comparés au 34 M aléatoire,
184: seul contrôle n=64 disponible.*
185: 
186: **Ce que le contrôle dit.** Le 34 M est **3,4 à 4,7× au-dessus de son bruit**, stable d'une
187: longueur à l'autre. Le 100 M greedy est **au plancher** (0,8× de son propre hasard à 128 octets ;
188: 1,8× du hasard 34 M à 64 octets : selon la longueur et le contrôle, il passe juste sous ou juste
189: au-dessus du hasard). En top-40 et top-20, il
190: garde un signal (1,9–3,4×), mais plus faible que le 34 M. Le 100 M n'est donc pas du bruit pur
191: en échantillonnage ; en greedy, il n'est pas distinguable du 
… [279 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md", "new_string": "*Lecture des contrôles : à 128 octets, chaque modèle est comparé à son propre aléatoire (34 M\npour le 34 M, 100 M pour le 100 M) ; à 64 octets, les deux sont comparés au 34 M aléat … [399 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Dernière passe tableaux/liens après l'ajout de la note

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 bash tools/porte-tableaux.sh 2>&1 | tail -5; echo \"exit=${PIPESTATUS[0]}\"", "description": "Revérifie les tableaux et liens", "timeoutMs": 180000}`

  ```
✅ 1893 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4973 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-18)
exit=0
  ```

### 🤖 Assistant

⏵ Envoi du résultat final consolidé au parent

- **send_message** `{"agent_id": "d67a9bb1-090e-4f69-baf2-a831c00aa275", "message": "RÉSULTAT FINAL — banc de grammaticalité du « 100 M » (73,37 M réels, 3 000 pas) vs 34 M (30 000 pas).\n\nFICHIERS\n- reports/banc-grammaticalite-100m.json (clés `n128`, `n64`, `controle_100m_n128`)\n- reports/rapport-grammaticalite-100 … [3242 caractères tronqués]`

  ```
message delivered to agent d67a9bb1-090e-4f69-baf2-a831c00aa275
  ```

### 🤖 Assistant

⏵ Récapitulatif final

## Livrables

- `reports/banc-grammaticalite-100m.json` — clés `n128`, `n64`, `controle_100m_n128`
- `reports/rapport-grammaticalite-100m.md` — fiche complète (protocole, tableaux, contrôles, limites, protocole r1)
- Aucun code modifié : `banc_grammaticalite.py` ne charge pas de modèle et `banc_generation.py` avait déjà `--device`. Aucun commit, aucun fichier interdit touché.

## Chiffres clés

**n=128 (protocole exact du 34 M, 20 prompts, 3 réglages, même analyseur) :**

| modèle | réglage | GV | ciment | GV/100 mots |
|---|---|---:|---:|---:|
| 34 M | greedy | **6,90** | **0,335** | 15,4 |
| 34 M | top-40/0,8 | 6,35 | 0,377 | 18,0 |
| 34 M | top-20/0,5 | 5,85 | 0,310 | 15,2 |
| **100 M** | greedy | **1,45** | **0,661** | 4,1 |
| **100 M** | top-40/0,8 | 4,00 | 0,375 | 14,4 |
| **100 M** | top-20/0,5 | 2,65 | 0,461 | 8,3 |

En greedy, 8/20 textes du 100 M n'ont aucun GV (3/20 pour le 34 M).

**n=64 (contrôle de longueur) :** 34 M greedy **3,35 GV / 0,427** ; 100 M greedy **1,10 / 0,693** ; contrôle 34 M aléatoire n=64 **1,50 / 0,790**. Le contrôle 100 M aléatoire n=128 donne **4,75 GV / 0,763**.

**Ratios GV/100 au hasard :** 34 M **3,4–4,7×** (stable à 64 et 128 octets) ; 100 M greedy **0,8×** (n=128, son propre hasard) et **1,8×** (n=64) — au plancher ; top-40/top-20 **1,9–3,4×**.

## Deux réserves majeures

1. **Le « 100 M » fait 73 366 568 paramètres** (×2,14, pas ×3) et **3 000 pas** contre 30 000 pour le 34 M (PPL val **4,014** contre **2,404**) : la comparaison confond échelle et entraînement. Ne pas conclure « l'échelle n'achète pas la grammaire ».
2. **GV et ciment mesurent surtout la classe du token de boucle** : 42 % des GV du 34 M sont le seul « a » (58/138) ; 46 % des mots du 100 M sont « de » (304/661). Le 100 M est plus répétitif (46 % vs 18 % de mot dominant) et moins divers (74 vs 149 types), mais le banc ne prouve pas qu'il est « moins grammatical ».

## Commandes

```bash
# génération 100 M, n=128, GPU
/home/stephane/gpu-env/bin/python tools/banc_generation.py \
  --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 \
  --sortie /tmp/banc-generation-100m-128o.json

# grammaticalité n=128, contrôle 34 M aléatoire n=128
/home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py \
  --entree /tmp/banc-generation-100m-128o.json \
  --controle reports/banc-generation-aleatoire.json \
  --sortie /tmp/banc-grammaticalite-100m-128o-controle34.json

# grammaticalité n=64, contrôle 34 M aléatoire n=64
/home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py \
  --entree reports/banc-generation-100m.json \
  --controle reports/banc-generation-alea-64o.json \
  --sortie /tmp/banc-grammaticalite-100m-64o.json
```

Les deux autres passes (contrôle 100 M aléatoire n=128 et 34 M n=64) sont dans la fiche §1. `porte-tableaux.sh` est vert ; `revue_documentation.py` ne signale que le compteur d'`en-cours` (792 vs 794, +2 fiches), à mettre à jour dans `docs/pilotage/en-cours.md` — fichier que je ne pouvais pas toucher.

