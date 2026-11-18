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

