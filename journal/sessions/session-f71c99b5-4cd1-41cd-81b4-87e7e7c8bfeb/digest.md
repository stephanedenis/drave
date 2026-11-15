# Session DSH — relecture

- identifiant : `session-f71c99b5-4cd1-41cd-81b4-87e7e7c8bfeb`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 12:05:10
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche W6 (J5 après-midi) : la clôture de la semaine 2 — le rapport `reports/rapport-semaine-2.md` + JSON (les chiffres avant/après de chaque vague W1-W5, les négatifs, les décisions), la mise à jour de `docs/pilotage/en-cours.md` et `semaine-2.md` (l'état par jour), le **tag annoté** `semaine-2-2026-11-20` sur le dernier commit vert, et le relevé des portes. Ne relance pas la passe complète : lis `work/portes/`.

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

- **bash** `{"command": "pwd && git log --oneline -15 && git status --short | head -50", "description": "Inspect repo state and recent commits"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
93e046f7 SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
be3f41ad SEMAINE 2 — W3 : LA MATRICE DU TAGGER (DÉFAUT HORS LIGNE CODE 0, CLÉ INVALIDE 4, RÉSEAU COUPÉ 0 APRÈS 3 ESSAIS, 1 000 PHRASES = 143 870 TOKENS) ; 4 TESTS DE PLUS
3439cb0c ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte
1683c2b4 W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
4dbeff45 SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S
6b2208ee PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE, RESTITUTION v3, LE TAGGER PAR DÉFAUT ? ; LA FILE DU CHANTIER À 41 TÂCHES
8cb0a926 PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE CONTRÔLÉE, RESTITUTION V3, TAGGER PAR DÉFAUT ?
49011807 ÉTAT — T0 VERT (LA LIGNE FAIT NETTOYÉE, COQUILLE CORRIGÉE)
2b7e520b ÉTAT — T0 VERT
c
… [2077 caractères tronqués]
  ```

- **bash** `{"command": "ls -la && echo '---DOCS---' && ls docs/pilotage/ && echo '---REPORTS---' && ls reports/ | tail -40 && echo '---WORK---' && ls work/ 2>/dev/null", "description": "List repo structure and key directories"}`

  ```
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 06:29 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198 15 nov 12:05 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 78154 15 nov 11:17 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run
… [3269 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md</path>
<type>file</type>
<content>
1: # La semaine 2 — cinq jours, deux vagues, quatre chantiers et une décision
2: 
3: > **Ce que ce document est.** Le plan du **16 au 22 novembre 2026** : ce qui se fait, dans quel
4: > ordre, avec quelles dépendances, quels contrôles et quels livrables. Il **succède** à
5: > [`semaine-autonome.md`](semaine-autonome.md), qui reste l'**archive** de la semaine 1 et n'est
6: > **pas modifié**. L'état courant est dans [`en-cours.md`](en-cours.md) ; les chiffres sont dans
7: > les fiches citées, jamais recopiés ici.
8: >
9: > **Sources.** Le [bilan de la semaine](../../reports/rapport-bilan-semaine.md) et les fiches des
10: > tâches C/B/D/E : [C1](../../reports/rapport-coordination-n2-v2.md), [C2](../../reports/rapport-coordination-s-v2.md),
11: > [C3](../../reports/rapport-gold-reel-50.md), [B1](../../reports/rapport-protocole-date.md),
12: > [B2](../../reports/rapport-atomes-prediction.md), [B3](../../reports/rapport-cic-v2.md),
13: > [D1](../../reports/rapport-exemples-tagger.md), [D2](../../reports/rapport-restitution-v2.md),
14: > [D3](../../reports/rapport-faq.md), [
… [11308 caractères tronqués]
  ```

- **bash** `{"command": "ls -la work/portes/ work/portes-w5/ 2>/dev/null; echo '---'; for d in work/portes work/portes-w5; do echo \"== $d\"; find \"$d\" -maxdepth 2 -type f | head -40; done", "description": "List portes directories"}`

  ```
work/portes/:
total 40
drwxr-xr-x. 1 stephane stephane   526 15 nov 03:03 .
drwxr-xr-x. 1 stephane stephane  2218 15 nov 11:21 ..
drwxr-xr-x. 1 stephane stephane   178 15 nov 03:03 b1-protocole-03h03
drwxr-xr-x. 1 stephane stephane  3432  3 nov 05:42 passe-0303-04h10
drwxr-xr-x. 1 stephane stephane  3432  3 nov 13:07 passe-0303-11h30
drwxr-xr-x. 1 stephane stephane  3392  2 nov 21:13 passe-1102-19h32
drwxr-xr-x. 1 stephane stephane    22  2 nov 16:45 passe-1102-apres-n2
drwxr-xr-x. 1 stephane stephane  1080  4 nov 08:31 passe-1104-08h00
drwxr-xr-x. 1 stephane stephane  3512 14 nov 01:00 passe-1311-23h15
-rw-r--r--. 1 stephane stephane 13611 14 nov 01:10 passe-1311-23h15.log
drwxr-xr-x. 1 stephane stephane  3512 14 nov 03:48 passe-1402-02h00
drwxr-xr-x. 1 stephane stephane  3478  5 nov 01:54 passe-2404-23h45
-rw-r--r--. 1 stephane stephane    17  4 nov 23:42 passe-2404-23h45.debut
-rw-r--r--. 1 stephane stephane 13701  5 nov 02:05 passe-2404-23h45.log
drwxr-xr-x. 1 stephane stephane   316  2 nov 16:35 sous-passe-1102-16h35
-rw-r--r--. 1 stephane stephane   322  2 nov 21:57 tableaux-rejeu.log
drwxr-xr-x. 1 stephane stephane   190 14 nov 07:12 verif-cloture

work/portes-w5/:
total 132
… [5606 caractères tronqués]
  ```

- **bash** `{"command": "git log -1 --format='%H %ci %s'; echo '---all---'; git log --all --oneline -20; echo '---branches---'; git branch -a --verbose; echo '---status---'; git status --short --branch | head -5; echo '---reflog---'; git reflog -12", "description": "Inspect branches, dates, reflog"}`

  ```
93e046f720fbe4d8cff4a105f6a03c8be134b657 2026-11-15 11:04:52 -0500 SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
---all---
93e046f7 SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
be3f41ad SEMAINE 2 — W3 : LA MATRICE DU TAGGER (DÉFAUT HORS LIGNE CODE 0, CLÉ INVALIDE 4, RÉSEAU COUPÉ 0 APRÈS 3 ESSAIS, 1 000 PHRASES = 143 870 TOKENS) ; 4 TESTS DE PLUS
3439cb0c ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte
1683c2b4 W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
4dbeff45 SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S
6b2208ee PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE, RESTITUTION v3, LE TAGGER PAR DÉFAUT ? ; LA FILE DU CHANTIER À 41 TÂCHES
8cb0a926 PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 45
… [4707 caractères tronqués]
  ```

- **bash** `{"command": "cat work/portes-w5/registre.txt; echo '=== last registre in portes ==='; cat work/portes/passe-1402-02h00/registre.txt 2>/dev/null | head -60", "description": "Read latest gates registry"}`

  ```
porte-adaptateur-sortie 0 91
porte-audit-drapeaux 0 177
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 17
porte-bloc-linguistique 0 18
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 55
porte-bus 0 92
porte-bus-socket 0 198
porte-c4-retard 0 41
porte-cerveau 0 11
porte-cic 0 13
porte-consolidation 0 89
porte-coupe 0 175
porte-cycle-c2 0 138
porte-deepseek 0 1
porte-delais 0 24
porte-diff-couche 0 23
porte-document 0 8
porte-echange-experts 0 81
porte-episodique 0 274
porte-etat 0 1
porte-flux 0 30
porte-fusion 0 10
porte-gain 0 281
porte-greffe 124 600
porte-harnais-invariants 0 128
=== last registre in portes ===
porte-adaptateur-sortie 0 81
porte-audit-drapeaux 0 175
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 12
porte-bloc-linguistique 0 14
porte-bloc-maths 0 0
porte-bloc-tableaux 0 2
porte-budget 0 46
porte-bus 0 81
porte-bus-socket 0 97
porte-c4-retard 0 31
porte-cerveau 0 9
porte-consolidation 0 102
porte-coupe 0 135
porte-cycle-c2 0 129
porte-deepseek 0 1
porte-delais 0 21
porte-diff-couche 0 19
porte-document 0 6
porte-echange-experts 0 56
porte-episodique 0 173
porte-etat 0 0
porte-flux 0 26
porte-fusion 0 8
porte-gain 0 218
porte
… [753 caractères tronqués]
  ```

- **bash** `{"command": "find work/portes -name registre.txt -printf '%TY-%Tm-%Td %TH:%TM %p\\n' | sort; echo '=== reports recent ==='; find reports -maxdepth 1 -type f -newermt '2026-11-15 10:00' -printf '%TH:%TM %f\\n' | sort; echo '=== journal recent ==='; find journal -newermt '2026-11-15 10:00' -type f -pr … [101 caractères tronqués]`

  ```
2026-11-02 16:35 work/portes/sous-passe-1102-16h35/registre.txt
2026-11-02 21:23 work/portes/passe-1102-19h32/registre.txt
2026-11-03 05:51 work/portes/passe-0303-04h10/registre.txt
2026-11-03 13:16 work/portes/passe-0303-11h30/registre.txt
2026-11-04 08:31 work/portes/passe-1104-08h00/registre.txt
2026-11-05 02:05 work/portes/passe-2404-23h45/registre.txt
2026-11-14 01:10 work/portes/passe-1311-23h15/registre.txt
2026-11-14 03:58 work/portes/passe-1402-02h00/registre.txt
2026-11-15 03:03 work/portes/b1-protocole-03h03/registre.txt
=== reports recent ===
10:30 rapport-tagger-defaut.json
10:30 rapport-tagger-defaut.md
10:58 panini-manifeste.json
11:02 rapport-panini-manifeste.md
11:17 README.md
11:18 INDEX.md
11:53 pensee-restitution-v3.json
12:03 rapport-restitution-v3.md
=== journal recent ===
11:18 journal/sessions/session-72a370ef-2ad7-4a59-8418-d88c38545f6e/rapport.md
11:18 journal/sessions/session-78f03aed-fb9d-4009-8625-e1186078059c/rapport.md
11:18 journal/sessions/session-932afd57-1363-4133-b6f1-64f7d937f38d/rapport.md
11:18 journal/sessions/session-9a7f5c6a-2798-4ca2-9b0f-131347ef53c3/rapport.md
11:18 journal/sessions/session-9cb32ff9-6fb5-489f-a41e-0e2df9aeb32f/rapport.md
… [1798 caractères tronqués]
  ```

- **bash** `{"command": "grep -ril \"W5\" docs reports journal work 2>/dev/null | head -40; echo '=== semaine-2 mentions W5 ==='; grep -rn \"W5\" docs/pilotage/*.md reports/*.md 2>/dev/null | head -40", "description": "Search for W5 references"}`

  ```
docs/schemas/pipeline.mmd.svg
docs/pilotage/en-cours.md
docs/pilotage/roadmap.md
reports/rapport-panini-manifeste.md
reports/pensee-restitution-v3.json
reports/rapport-restitution-v3.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/session.jsonl.zstd
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md
journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/session.jsonl.zstd
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/session.jsonl.zstd
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
journal/sessions/e7dfe34f-d596-4f98-93c2-cad5a92d3b1e/session.jsonl.zstd
journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/session.jsonl.zstd
journal/sessions/7d0d2578-0048-4998-8494-7d2daef56769/session.jsonl.zstd
journal/sessions/c25f97d1-9a4d-41da-b983-004f793afe43/session.jsonl.zstd
journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/session.jsonl.zstd
journal/sessions/bcfe0b97-1795-4610-8e8b-b598ca1ba6cb/session.jsonl.zstd
journal/sessions/7c876089-605c-4836-930e-925a66028509/session.jsonl.zstd
journal/sessions/7c876089-605c-4836-930e-925a66028509/digest.md
journal/sessions/aa5f9fc5-9
… [4181 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 11 h 40 HNE (W5 : la restitution v3 — les rôles des GP)**
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
21: > [`journ
… [11861 caractères tronqués]
  ```

- **bash** `{"command": "git diff --stat; echo '=== staged ==='; git diff --cached --stat; echo '=== W5 reports ==='; sed -n '1,80p' reports/rapport-restitution-v3.md; echo '=== registre w5 full ==='; cat work/portes-w5/registre.txt; echo '=== greffe log tail ==='; tail -40 work/portes-w5/porte-greffe.log", "de … [53 caractères tronqués]`

  ```
docs/produit/README.md                             |  25 +-
 journal/README.md                                  |   5 +-
 journal/sessions/MANIFEST.md                       |   7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  41 ++
 .../rapport.md                                     |  14 +-
 .../digest.md                                      | 115 ++++
 .../rapport.md                                     |  51 +-
 reports/pensee-coherence-fiches-v7.json            |  19 +
 reports/pensee-dev-test-v10.json                   |   2 +-
 reports/pensee-quatre-modes.json                   | 734 ++++++++++++---------
 reports/rapport-audit-v7.md                        |   6 +-
 reports/rapport-coherence-fiches-v7.md             |  17 +-
 reports/rapport-dev-test-v10.md                    |   2 +-
 reports/rapport-pensee-v12.md                      |   4 +-
 reports/rapport-spans-chunker.md                   |  13 +-
 tools/chantier/plan.json                           | 129 ++++
 tools/drave.py                                     |  26 +
 17 files changed, 848 insertions(+), 362 deletions(-)
=== staged ===
 docs/pilotage/en-cours.md          |    29 +-
 docs/pilotage/roadmap.md 
… [6230 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md</path>
<type>file</type>
<content>
1: # Références de non-régression
2: 
3: > **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
4: > `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
5: > `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
6: > `work/portes/passe-1311-23h15.log`.
7: >
8: > **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
9: > heartbeat `e181ce02` rafraîchi) ; `porte-indice` et `porte-melange` restent **rouges
10: > structurelles** (indice 482 contre témoin 459 ; état de A sans son code). Journaux
11: > `work/portes/verif-cloture/`.
12: > **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).
13: 
14: > **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
15: > 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
16: > (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-ind
… [13972 caractères tronqués]
  ```

- **bash** `{"command": "cat work/portes-w5/porte-greffe.log; echo '=== previous greffe ==='; cat work/portes/passe-1402-02h00/porte-greffe.log; echo '=== pass log tail ==='; ls -la work/portes-w5 | tail -5", "description": "Read greffe gate logs and tolerated reds"}`

  ```
=== 0. construire A (avec aiguille) et B (sans), et vérifier qu'elles diffèrent ===
  A (avec aiguille) : [1863, 48, 12, 19, 19, 22, 16, 15843]
  B (sans aiguille) : [220, 16, 17, 18, 19, 20, 21, 22]
=== 1. prélever l'état de la dernière position DE L'INFÉRENCE (--etat-fin) ===
    capture d'état    : position(s) [1470] (depuis la fin d'une invite de 1471 jetons) écrite(s) dans /tmp/tmp.0mY9AjWhkm/etatA
=== 2. témoin de non-effet : poids 0 ⇒ aucune différence ===
  ✅ poids 0 : [220, 16, 17, 18, 19, 20, 21, 22] (identique à B sans greffe)
=== 3. le mécanisme fonctionne : A + son propre état reste sur le code ===
  A + son état (poids 100) : [1863, 48, 12, 19, 19, 22, 16, 15843]
  ✅ l'état injecté porte bien la direction du contenu de A
=== 4. CORRIGÉ : l'état de A dans C (sans aucun code) DONNE le code ===
  poids 1    : [220, 16, 17, 18, 19, 20, 21, 22]
  poids 2    : [1863, 48, 41, 43, 198, 16141, 374, 25]
=== previous greffe ===
=== 0. construire A (avec aiguille) et B (sans), et vérifier qu'elles diffèrent ===
  A (avec aiguille) : [1863, 48, 12, 19, 19, 22, 16, 15843]
  B (sans aiguille) : [220, 16, 17, 18, 19, 20, 21, 22]
=== 1. prélever l'état de la dernière position DE L'INF
… [2113 caractères tronqués]
  ```

- **bash** `{"command": "ps aux | grep -E 'porte-|toutes-les-portes' | grep -v grep | head -20; echo '---'; cat work/portes-w5/porte-homeostasie.log; echo '---'; cat work/portes-w5/porte-harnais-invariants.log", "description": "Check for running gate processes"}`

  ```
stephane   91839  0.0  0.0   7832  4280 ?        Ss   11:21   0:00 bash tools/toutes-les-portes.sh
stephane  451917  0.0  0.0   5848  2504 ?        S    12:02   0:00 timeout 1800 bash tools/porte-vision.sh
stephane  451918  0.0  0.0   7832  4220 ?        S    12:02   0:00 bash tools/porte-vision.sh
stephane  451924  0.0  0.0   5848  2504 ?        S    12:02   0:00 timeout 2400 env DRAVE_VISION_POIDS=all DRAVE_VISION_COUCHES=32 DRAVE_VISION_FUSION=1 ./drave-core/target/release/drave models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf --banc-vision /tmp/porte-vision/tour.bin
stephane  451925 99.8  0.3 1094440 492620 ?      R    12:02   2:57 ./drave-core/target/release/drave models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf --banc-vision /tmp/porte-vision/tour.bin
stephane  453065  0.0  0.0   5848  2508 ?        S    12:04   0:00 timeout 600 bash tools/porte-homeostasie.sh
stephane  453066  0.0  0.0   7832  4288 ?        S    12:04   0:00 bash tools/porte-homeostasie.sh
stephane  453515  0.0  0.0   7832  2108 ?        S    12:04   0:00 bash tools/porte-homeostasie.sh
stephane  453516  953  0.5 10710220 677208 ?     Rl   12:04   7:31 ./drave-core/target/release/drave /tmp/porte-homeo
… [1699 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"semaine 2\\|semaine-2\\|W1\\|W2\\|W3\\|W4\\|W5\" journal/2026-11-15/README.md | head -40; echo '=== journal day files ==='; ls journal/2026-11-1* 2>/dev/null; ls journal | tail -12", "description": "Check journal for week 2 narrative"}`

  ```
59:| 09:18 | `4dbeff45` | SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S |
60:| 09:24 | `1683c2b4` | W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3 |
61:| 09:41 | `3439cb0c` | ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte |
62:| 10:47 | `be3f41ad` | SEMAINE 2 — W3 : LA MATRICE DU TAGGER (DÉFAUT HORS LIGNE CODE 0, CLÉ INVALIDE 4, RÉSEAU COUPÉ 0 APRÈS 3 ESSAIS, 1 000 PHRASES = 143 870 TOKENS) ; 4 TESTS DE PLUS |
63:| 10:59 | `e283d09a` | SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE |
104:### W2 — le tagger sur 402/H50 : il gagne sur les deux, le fermé du 402 paie
106:Le split de W1 (**402 / H50**) reçoit sa mesure : le tagger POS de l'API gagne **+4,45 pts** sur les
113:+19,40) ; H50, lui, gagne **aussi** le fermé. La suite (W3) doit décider du défaut et, si possible,
117:### W5 — la restitution v3 : les ci
… [456 caractères tronqués]
  ```

- **bash** `{"command": "for p in 3923655 91839; do echo \"== $p\"; tr '\\0' ' ' < /proc/$p/cmdline; echo; readlink /proc/$p/cwd; ls -l /proc/$p/fd 2>/dev/null | grep -E 'log|registre|txt' | head; done", "description": "Identify running gate pass outputs"}`

  ```
== 3923655
bash tools/toutes-les-portes.sh 
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
== 91839
bash tools/toutes-les-portes.sh 
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
  ```

- **bash** `{"command": "sed -n '1,140p' tools/toutes-les-portes.sh", "description": "Read gate runner script"}`

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

- **bash** `{"command": "ls -ld work/portes-* | tail -10; echo '---'; ls work/portes-1115-09h53 2>/dev/null | tail; echo '--- registre 09h53 ---'; tail -5 work/portes-1115-09h53/registre.txt 2>/dev/null; echo '--- pstree ---'; ps -o pid,ppid,etime,cmd -p 3923655,91839; ps -o pid,ppid,etime,cmd --ppid 3923655; p … [89 caractères tronqués]`

  ```
drwxr-xr-x. 1 stephane stephane   58 14 nov 05:42 work/portes-1114-05h40
drwxr-xr-x. 1 stephane stephane 1078 14 nov 06:16 work/portes-1114-05h52
drwxr-xr-x. 1 stephane stephane   50 15 nov 04:03 work/portes-1115-04h03
drwxr-xr-x. 1 stephane stephane 3396 15 nov 06:56 work/portes-1115-05h08
drwxr-xr-x. 1 stephane stephane 1078 15 nov 07:09 work/portes-1115-06h45
drwxr-xr-x. 1 stephane stephane  930 15 nov 09:39 work/portes-1115-09h22
drwxr-xr-x. 1 stephane stephane 3396 15 nov 12:02 work/portes-1115-09h53
drwxr-xr-x. 1 stephane stephane 3512  7 nov 14:58 work/portes-j12-1107-12h58
drwxr-xr-x. 1 stephane stephane  768  4 nov 11:32 work/portes-n3-cloture
drwxr-xr-x. 1 stephane stephane 1204 15 nov 12:04 work/portes-w5
---
porte-ressources.log
porte-sauvegarde-modele.log
porte-sessions.log
porte-speculatif.log
porte-tableaux.log
porte-tokenizer-kimi.log
porte-topologie.log
porte-trace.log
porte-vision.log
registre.txt
--- registre 09h53 ---
porte-speculatif 0 81
porte-tableaux 0 1
porte-tokenizer-kimi 0 7
porte-topologie 0 135
porte-trace 0 32
--- pstree ---
    PID    PPID     ELAPSED CMD
3923655    2886    02:12:29 bash tools/toutes-les-portes.sh
  91839    2886       44:29 bash too
… [227 caractères tronqués]
  ```

- **bash** `{"command": "for p in 3923655 91839; do echo \"== $p\"; tr '\\0' '\\n' < /proc/$p/environ | grep -E '^(DELAI|JOURNAUX|PORTES)='; done; echo '=== 09h53 registre complete ==='; cat work/portes-1115-09h53/registre.txt; echo '=== count ==='; awk '$2!=0' work/portes-1115-09h53/registre.txt", "description … [39 caractères tronqués]`

  ```
== 3923655
== 91839
JOURNAUX=work/portes-w5
DELAI=600
=== 09h53 registre complete ===
porte-adaptateur-sortie 0 76
porte-audit-drapeaux 0 177
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 16
porte-bloc-linguistique 0 16
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 50
porte-bus 0 83
porte-bus-socket 0 104
porte-c4-retard 0 35
porte-cerveau 0 10
porte-cic 0 13
porte-consolidation 0 91
porte-coupe 0 156
porte-cycle-c2 0 147
porte-deepseek 0 0
porte-delais 0 25
porte-diff-couche 0 21
porte-document 0 6
porte-echange-experts 0 61
porte-episodique 0 204
porte-etat 0 1
porte-flux 0 28
porte-fusion 0 9
porte-gain 0 249
porte-greffe 0 780
porte-harnais-invariants 0 121
porte-homeostasie 0 579
porte-horloge 0 29
porte-indice 1 1149
porte-jeux 0 123
porte-jumeaux 0 32
porte-lecteur 0 1
porte-lecture 0 2
porte-m5-brouillon 0 0
porte-melange 1 137
porte-memoire 0 12
porte-miroir-blocs 0 10
porte-mistral 0 11
porte-n3-cache 0 6
porte-n3-composition 0 7
porte-n3-deux-processus 0 5
porte-n3-deux-regions 0 5
porte-n3-generation 0 9
porte-n3-inventaire 0 0
porte-n3-placement 0 5
porte-n3-pont 0 5
porte-n3-positions 0 6
porte-n3-profondeur 0 6
porte-n3-refus 0 5
porte-n3
… [809 caractères tronqués]
  ```

- **bash** `{"command": "echo '=== prechargement ==='; cat work/portes-1115-09h53/porte-prechargement.log; echo '=== sessions ==='; cat work/portes-1115-09h53/porte-sessions.log; echo '=== indice tail ==='; tail -15 work/portes-1115-09h53/porte-indice.log; echo '=== melange tail ==='; tail -15 work/portes-1115- … [82 caractères tronqués]`

  ```
=== prechargement ===
porte du préchargement — qwen3-30b-a3b-Q4_K_M.gguf, 8 jetons, ctx 512, 3 répétition(s)
bras       rép       octets lus      mural chargement     calcul  perplexité
demande    1             9.53 Go    0:16.01 8.94259278      6.5 s  799.8557
demande    2             9.53 Go    0:17.24 9.262159116      7.4 s  799.8557
demande    3             9.52 Go    0:16.40 8.747005011      7.1 s  799.8557
madvise    1             6.20 Go    0:21.55 9.375999711     11.6 s  799.8557
madvise    2             5.64 Go    0:22.88 9.258575503     13.1 s  799.8557
madvise    3             6.13 Go    0:31.07 9.467716609     21.1 s  799.8557
fils       1            10.93 Go    0:19.78 9.606944216      9.7 s  799.8557
fils       2            10.91 Go    0:24.21 9.650762778     14.0 s  799.8557
fils       3            10.94 Go    0:20.50 10.661156059      9.2 s  799.8557
tampons    1             6.20 Go    0:18.50 9.614501373      8.5 s  799.8557
tampons    2             6.20 Go    0:20.22 9.348037957     10.4 s  799.8557
tampons    3             6.20 Go    0:21.05 10.046644786     10.6 s  799.8557

  ✅ perplexité identique dans les trois bras : 799.8557
     demande  :   9.53 Go lus · 
… [3095 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' reports/rapport-bilan-semaine.md", "description": "Read week 1 closure report template"}`

  ```
# Le bilan de la semaine (07 → 15/11) — le produit gagne 3,7 points, Panini est borné, le harnais tient

> **Ce que ce bilan est.** La **synthèse de la semaine** : le produit, Panini, la coordination, le
> méta-harnais. **Aucune mesure nouvelle** : chaque chiffre renvoie à sa fiche. Il est écrit pour
> être lu en 5 minutes, pas pour remplacer les fiches.

## 1. Le produit — les chiffres, avec leur base

| mesure | avant (07/11) | **après (15/11)** | base |
|---|---:|---:|---|
| **F1 syntagmes** | 0,7533 | **0,7902** (+3,69) | vivant 612 |
| F1 syntagmes (réel) | — | **0,7906** | réel 452 |
| **POS** | 0,8625 | 0,8625 | vivant 612 |
| POS (réel) | — | **0,8891** | réel 452 |
| POS avec `--tagger` | — | **0,9575** (612) · **0,9500** (réel) | API |
| **attachement exact** | 236/237 | **238/239** (0,9958) | vivant 612 |
| attachement (réel) | — | **99,46 %** | réel 452 |
| exact sur span | 1,0000 | **1,0000** | vivant 612 |
| spans perdus | 2 | **1** (`g017`, inatteignable) | vivant 612 |

**Les trois bases** : le **vivant 612** (20 main + 432 corpus + 160 synthétiques), le **gelé 602**
(la référence figée) et le **réel 452** (`--reel`, hand + reel, sans synthétique). Les chiffres
glob
… [3810 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-semaine.md; echo '=== INDEX tail ==='; tail -30 reports/INDEX.md", "description": "Read weekly report and index conventions"}`

  ```
# J5.1 — le rapport de semaine : le produit gagne 3,69 points de F1, l'intégration est bornée

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (le moteur de pensée), **R0.7** (le bloc langue), **N2**, **S**,
> **R**, **A**, **Panini** · **Tâche** : J5.1 · **Date** : 2026-11-13 · **Verdict** : ✅
>
> **Ce que ce rapport est.** La **relecture consolidée** des fiches des jours 1 à 4 : les chiffres
> avant/après, les décisions, les rejets et ce qui reste. **Aucune mesure nouvelle** : chaque
> chiffre est celui de sa fiche, avec sa base, son contrôle négatif et sa limite.
>
> **Base.** Gold vivant **612 phrases / 239 cibles / 3 179 jetons** ; POS heuristique **0,8625** ;
> F1 **0,7533** au départ de la semaine ; commits J1–J3 `25a6c0ff` → `c2e629b3` ; fiches J4 du
> **13/11** (HEAD `dc78f223`). Les fiches J4 de N2, S et A ne sont pas encore committées au moment
> de la rédaction : **J5.1 les emporte avec ce rapport**.
>
> **Le verdict en une phrase.** L
… [12166 caractères tronqués]
  ```

- **bash** `{"command": "date; echo '---'; ls reports/ | grep -E 'semaine|bilan' ; echo '--- json semaine ---'; ls reports/*semaine* 2>/dev/null", "description": "Check system date and weekly report files"}`

  ```
dim 15 nov 2026 12:06:15 EST
---
a26-bilan.json
bilan-b11.md
bilan-multi-materiel.md
pensee-anaphore-bilan.json
pensee-bilan-nuit.json
pensee-robustesse-semaine.json
rapport-a26-bilan.md
rapport-bilan-chantier.json
rapport-bilan-chantier.md
rapport-bilan-nuit.md
rapport-bilan-semaine.md
rapport-pensee-anaphore-bilan.md
rapport-robustesse-semaine.md
rapport-semaine.json
rapport-semaine.md
--- json semaine ---
reports/pensee-robustesse-semaine.json
reports/rapport-bilan-semaine.md
reports/rapport-robustesse-semaine.md
reports/rapport-semaine.json
reports/rapport-semaine.md
  ```

- **bash** `{"command": "sed -n '1,120p' docs/methode/resultats.md", "description": "Read results method requirements"}`

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

- **bash** `{"command": "cat reports/rapport-semaine.json | head -120; echo '...'; python3 -c \"import json;d=json.load(open('reports/rapport-semaine.json'));print(list(d.keys()))\"", "description": "Inspect weekly report JSON structure"}`

  ```
{
  "titre": "J5.1 — le rapport de semaine : le produit gagne 3,69 points de F1, l'intégration est bornée",
  "version": 1,
  "date": "2026-11-13",
  "tache": "J5.1",
  "lignes_roadmap": ["B13", "R0.7", "N2", "S", "R", "A", "Panini"],
  "statut": "consolide",
  "base": {
    "gold_phrases": 612,
    "gold_cibles": 239,
    "pos_jetons": 3179,
    "pos_heuristique": 0.8625,
    "f1_depart": 0.7533,
    "commits_j1_j3": ["25a6c0ff", "92652984", "9a259953", "8eb0cc49", "9c7f71dc", "c3467170", "c2e629b3"],
    "head_j4": "dc78f223",
    "note": "Aucune mesure nouvelle : ce rapport relit les fiches des jours 1 à 4."
  },
  "chiffres": {
    "produit": {
      "pos": {
        "production_avant": 0.8625,
        "production_apres": 0.8625,
        "delta": 0.0,
        "jetons": 3179,
        "jetons_changes": 0,
        "lecture": "J1.1 et J1.2 sont des regles de syntagmes ; la POS ne bouge pas."
      },
      "f1": {
        "avant": {"all": 0.7533, "dev": 0.7476, "test": 0.7663, "lineaire": 0.8120},
        "apres": {"all": 0.7902, "dev": 0.7875, "test": 0.7962, "lineaire": 0.8144},
        "delta": {"all": 0.0369, "dev": 0.0399, "test": 0.0299, "lineaire": 0.0024},
        "controle
… [4128 caractères tronqués]
  ```

- **bash** `{"command": "for f in reports/rapport-gold-452.md reports/rapport-tagger-h50.md reports/rapport-tagger-defaut.md reports/rapport-panini-manifeste.md; do echo \"===== $f\"; sed -n '1,45p' \"$f\"; done", "description": "Read W1-W4 report headers"}`

  ```
===== reports/rapport-gold-452.md
# W1 — le gold réel 452 : composition, split 402 / H50, sha256 et 10 candidats GP/SUB

> **Ligne de roadmap** : **R0.7** (bloc linguistique) / **B13** · **Tâche** : W1 (semaine 2, J1 matin, la part du pilote) ·
> **Date** : 2026-11-15 (J1 · 16/11) · **HEAD mesuré** : `6b2208ee` · **Verdict** : ✅ **le gold réel 452 est
> nommé et composé ; le split 402/H50 est figé ; le gold est intact ; les 10 GP/SUB sont listés pour S.**

**En trois lignes.** (1) Le gold réel fait **452** phrases = **20 hand** (`gold.json`) + **432 corpus**
(`gold_reel.json`) ; **242 fr + 210 en** ; **2 480 tokens**, **1 501 segments**, **184 cibles** d'attachement.
(2) Le split proposé est **402 / H50** : H50 = les **50 phrases dures** de C3 (2 hand + 48 corpus ; 25 fr + 25 en),
sélectionnées par score d'erreur, **sans aléa** ; la **graine 20261116** ne sert qu'au contrôle aléatoire et au
manifeste. (3) **10 GP/SUB** sans cible sont proposés à S (9 GP + 1 SUB ; **4 dans H50**) : le dénominateur
d'attachement passe de **184 à 194**. Le **sha256** du gold est identique avant/après ; aucun fichier gold n'est modifié.

**Ce que cette fiche est, et n'est pas.**

- **Est** : la composi
… [11422 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -E 'gold-452|tagger-h50|tagger-defaut|panini-manifeste|restitution-v3'", "description": "Find W1-W5 JSON files"}`

  ```
panini-manifeste.json
pensee-restitution-v3.json
rapport-gold-452.json
rapport-gold-452.md
rapport-panini-manifeste.md
rapport-restitution-v3.md
rapport-tagger-defaut.json
rapport-tagger-defaut.md
rapport-tagger-h50.json
rapport-tagger-h50.md
  ```

- **bash** `{"command": "sed -n '45,200p' reports/rapport-gold-452.md", "description": "Read rest of gold 452 report"}`

  ```
| type de segment | hand | corpus | total |
|---|---|---|---|
| GN | 23 | 658 | 681 |
| GV | 20 | 532 | 552 |
| GP | 10 | 71 | 81 |
| REL | 1 | 57 | 58 |
| SUB | 2 | 53 | 55 |
| ADJ | 0 | 35 | 35 |
| ADV | 0 | 30 | 30 |
| PONCT | 0 | 9 | 9 |
| **total** | **56** | **1445** | **1501** |

| type de cible | hand | corpus | total |
|---|---|---|---|
| GP | 10 | 62 | 72 |
| REL | 1 | 57 | 58 |
| SUB | 2 | 52 | 54 |
| **total** | **13** | **171** | **184** |

**Les cibles sont saturées sur GP/REL/SUB, pas sur GN/GV.** 184 cibles = **GP 72 + REL 58 + SUB 54**.
Il reste **10 segments GP/SUB sans cible** (9 GP + 1 SUB) : ce sont exactement les 10 candidats du § 4.
Les **1 233 GN/GV** n'ont pas de cible ; les annoter est une deuxième vague facultative, pas ce lot.

## 2. Le split 402 / H50

### 2.1 La règle déterministe

Le split n'est **pas** un tirage au hasard : H50 est le **lot dur** de C3, sélectionné sur les erreurs de
l'heuristique. La règle est déterministe et reproductible :

```text
score(p) = 3 × |cibles d'attachement évaluées absentes ou fausses|
         + 2 × |tokens POS faux|
         + 1 × |segments gold absents|
```

1. Calculer le score sur les **452** phrases, au HEAD `6b2
… [6636 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['reports/rapport-gold-452.json','reports/rapport-tagger-h50.json','reports/rapport-tagger-defaut.json','reports/panini-manifeste.json','reports/pensee-restitution-v3.json']:\n    d=json.load(open(f))\n    print('==',f)\n    def walk(x,p=''):\n    … [371 caractères tronqués]`

  ```
== reports/rapport-gold-452.json
date str 2026-11-15
date_cible str 2026-11-16 (J1 · matin)
ligne str R0.7 / B13
tache str W1 — le gold réel 452 : composition, split 402/H50, sha256 et 10 candidats GP/SUB
commit_mesure str 6b2208ee1579739a188086f957c0d508e8a04726
commit_c3 str f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888
objet dict 
objet.gold str gold réel 452 = 20 hand + 432 corpus
objet.fichiers dict 
objet.unites dict 
objet.note str lecture seule ; aucun fichier gold n'est modifié
composition dict 
composition.total dict 
composition.par_source dict 
composition.par_langue dict 
composition.par_source_et_langue dict 
composition.lecture dict 
sha256 dict 
sha256.gold.json str 3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a
sha256.gold_reel.json str 05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11
sha256.concat_ordonnee str cff6b6d703546ad5992c5ada4fc99e1bdaa8e76e9cd089bd3e3b88bd71e90ac5
sha256.avant dict 
sha256.apres dict 
sha256.identique bool True
sha256.commande str sha256sum tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json
split dict 
split.nom str 402 / H50
split.statut str proposé ; S valide ou corrige, le pilote ne
… [13718 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfrom pprint import pprint\nd=json.load(open('reports/rapport-gold-452.json'))\nprint('W1 composition'); pprint(d['composition']); print('split partition'); pprint(d['split']['partition']); print('mesure'); pprint(d['split']['mesure']); print('part erreurs' … [413 caractères tronqués]`

  ```
W1 composition
{'lecture': {'cibles': '184 = GP 72 + REL 58 + SUB 54',
             'phrases': '242 fr + 210 en = 452 ; 20 hand + 432 corpus',
             'sans_cible': '10 GP/SUB sans cible (9 GP + 1 SUB) = les 10 '
                           'candidats du § 4',
             'source': 'le champ source de gold_reel.json vaut `reel` ; la '
                       "fiche et le split l'appellent `corpus`."},
 'par_langue': {'en': {'cibles': 88,
                       'cibles_par_type': {'GP': 34, 'REL': 28, 'SUB': 26},
                       'phrases': 210,
                       'segments': 702,
                       'segments_par_type': {'ADJ': 18,
                                             'ADV': 8,
                                             'GN': 321,
                                             'GP': 40,
                                             'GV': 259,
                                             'PONCT': 2,
                                             'REL': 28,
                                             'SUB': 26},
                       'tokens': 1148},
                'fr': {'cibles': 96,
                       'cibles_par_type': {'GP': 38, 'REL': 30, 'SUB': 28}
… [17486 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfrom pprint import pprint\nd=json.load(open('reports/rapport-tagger-h50.json'))\nfor k in ['split','passes','regle_decision','scores_api_452','cout_api_452']:\n    print('==',k); pprint(d[k])\nPY", "description": "Extract W2 figures"}`

  ```
'r136',
                                                                       'r137',
                                                                       'r138',
                                                                       'r139',
                                                                       'r140',
                                                                       'r141',
                                                                       'r142',
                                                                       'r143',
                                                                       'r144',
                                                                       'r145',
                                                                       'r146',
                                                                       'r147',
                                                                       'r148',
                                                                       'r149',
                                                                       'r150',
                                                                       'r151',
       
… [48692 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfrom pprint import pprint\nd=json.load(open('reports/rapport-tagger-defaut.json'))\nprint('matrice:'); \nfor m in d['matrice']: print({k:m.get(k) for k in ['cas','code','stdout','stderr','test','resultat'] if k in m})\nprint('cout:'); pprint(d['cout_1000_p … [106 caractères tronqués]`

  ```
matrice:
{'cas': 'defaut_sans_cle_analyser', 'code': 0, 'stderr': '', 'test': 'TestMatriceW3.test_defaut_sans_cle_code_0'}
{'cas': 'defaut_sans_cle_evaluer', 'code': 0, 'stderr': '', 'test': 'TestMatriceW3.test_defaut_sans_cle_code_0'}
{'cas': 'defaut_zero_socket', 'code': 0, 'stderr': '', 'test': 'TestMatriceW3.test_defaut_n_ouvre_aucune_socket'}
{'cas': 'avec_cle', 'code': 0, 'stderr': 'drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.2 s', 'test': 'TestCliAvecTransportFactice.test_analyser_tagger_json'}
{'cas': 'cle_invalide', 'code': 4, 'stderr': "drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.", 'test': 'TestErreursTagger.test_cle_invalide_code_4'}
{'cas': 'reseau_coupe', 'code': 0, 'stderr': 'drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused\ndrave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s', 'test': 'TestErreursTagger.test_reseau_coupe_repli_heuristique'}
{'cas': 'refus_modele_no
… [5163 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfrom pprint import pprint\nd=json.load(open('reports/panini-manifeste.json'))\nprint('manifeste reduction'); pprint(d['manifeste']['reduction_effective'])\nprint('sources courtes'); pprint(d['manifeste']['sources_courtes'])\nprint('doublons'); pprint(d['ma … [289 caractères tronqués]`

  ```
epublic_jowett': {'cos': 0.998659,
                                                     'l2': 0.017292,
                                                     'mots': 255752,
                                                     'ok': True},
                           'plato_sophist': {'cos': 0.996164,
                                             'l2': 0.028704,
                                             'mots': 11451,
                                             'ok': True},
                           'plato_symposium_jowett': {'cos': 0.996378,
                                                      'l2': 0.028071,
                                                      'mots': 19077,
                                                      'ok': True},
                           'plato_theaetetus_jowett': {'cos': 0.998118,
                                                       'l2': 0.020641,
                                                       'mots': 68786,
                                                       'ok': True},
                           'qiwulun': {'cos': 0.999693,
                                       'l2': 0.008663,
                                       'mots': 788,
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/panini-manifeste.json'))\nprint('sources courtes:')\nfor s in d['manifeste']['sources_courtes']: print(s)\nprint('\\ndoublons:')\nfor s in d['manifeste']['doublons_sources']: print(s)\nprint('\\nreduction:', json.dumps(d['manifest … [398 caractères tronqués]`

  ```
sources courtes:
epicurus_letters
sextus_pyrrho
zadeh_1965

doublons:
{'sha256': 'f7443b99845c0bd7643d648fcc3323f51deed449166e869f2b627f3defdc4f8e', 'ids': ['apastamba_grhya_sutra', 'hiranyakesi_grhya_sutra'], 'signes': [], 'a_signer': ['apastamba_grhya_sutra', 'hiranyakesi_grhya_sutra'], 'mots': 770}
{'sha256': '62a07681bbbc311e807d2e488883557601bd7f48210fd9d1b6b092ddf65a4fcd', 'ids': ['baudhayana_dharmasutra', 'vasistha_dharmasutra'], 'signes': [], 'a_signer': ['baudhayana_dharmasutra', 'vasistha_dharmasutra'], 'mots': 626}
{'sha256': '18f4886716914654f550e11cbd892504abdc993055aac8e4206bba5583109d72', 'ids': ['chandogya_upanishad', 'isa_upanishad'], 'signes': [], 'a_signer': ['chandogya_upanishad', 'isa_upanishad'], 'mots': 890}
{'sha256': '0d877881c8a644a3fb1ae4e635ffb508c79830281963652a9af07f005a110407', 'ids': ['daodejing', 'qiwulun', 'zhuangzi'], 'signes': ['qiwulun'], 'a_signer': ['daodejing', 'zhuangzi'], 'mots': 788}
{'sha256': 'e0bcd4dd8d3e8276d0747dcd5cb7470f05cb5f8420d25b83c6f078606eb5e71e', 'ids': ['paraskara_grhya_sutra', 'sankhayana_grhya_sutra'], 'signes': [], 'a_signer': ['paraskara_grhya_sutra', 'sankhayana_grhya_sutra'], 'mots': 848}
{'sha256': '068ad6cb618964cff
… [1492 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-restitution-v3.json'))\nprint('synthese:'); print(json.dumps({k:d['synthese'][k] for k in ['n','annotations','refus','or','cadre','roles','couverture','controles']},ensure_ascii=False,indent=1)[:4000])\nprint('\\ngold_s bas … [849 caractères tronqués]`

  ```
synthese:
{
 "n": 50,
 "annotations": 46,
 "refus": 4,
 "or": {
  "textes": 46,
  "variantes": 65,
  "roles_attendus": 77
 },
 "cadre": {
  "exacts": 20,
  "taux": 0.4348,
  "exacts_non_vides": 17,
  "exacts_vides": 3,
  "partiels": 43,
  "partiels_taux": 0.9348,
  "exacts_stricts": 17,
  "taux_strict": 0.3696,
  "roles_exacts_moyens": 2.0217
 },
 "roles": {
  "exacts": 93,
  "total": 138,
  "taux": 0.6739,
  "cadres_exacts": 20,
  "cadres_exacts_taux": 0.4348,
  "cadres_partiels": 43,
  "justes": 40,
  "attendus": 77,
  "predits": 71,
  "precision": 0.5634,
  "rappel": 0.5195,
  "f1": 0.5406,
  "faux_positifs": 31,
  "faux_negatifs": 37,
  "vrais_negatifs": 53,
  "par_role": {
   "agent": {
    "exacts": 29,
    "attendus": 32,
    "predits": 28,
    "justes": 18,
    "faux_positifs": 10,
    "faux_negatifs": 14,
    "vrais_negatifs": 11,
    "taux_exact": 0.6304,
    "precision": 0.6429,
    "rappel": 0.5625,
    "f1": 0.6
   },
   "predicat": {
    "exacts": 22,
    "attendus": 39,
    "predits": 39,
    "justes": 19,
    "faux_positifs": 20,
    "faux_negatifs": 20,
    "vrais_negatifs": 3,
    "taux_exact": 0.4783,
    "precision": 0.4872,
    "rappel": 0.4872,
    "f1": 0.487
… [12043 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"W6\\|semaine-2-2026\\|semaine-2026-11-22\" docs reports journal tools work 2>/dev/null | head -30", "description": "Search for W6 and tag references"}`

  ```
81pJ9Nv6Rx9Ea4w6jDLjxZxbFY06Xzm+uwuoU0wcr43+FAfSy0sc+lbMaZWT1m4FK53qQoMxga6schjKTbz3I5nD3HpZK38yeOVjWquOCGu+CFP+5wXhjMksvghSnNWaiyIy6pQTSBA3s5LetRRY0ZA3iFlrovMH8xjm/74Fe232PPC8nDezNJpUkUD18Yeae2XkMNvgHK1ZXPyWTePSDVBy4ezDFXflU0/PYV07VMNpPeBVqeOYhGyYF955uACjj8yRqk3OggqJTFmVAWMWZn1Yyay3/0n+XNtU73Bkz1qhHtrn/liyg+MHb1XY4r/7DSAuEVoy89RSXX8q9+S6VEB5ZsydlJ8xljtDNmemlJu0nlr+G8s0ubfRQknoOsMe69CwOE9TEyg5+HID0e4QJWw1uekElWnZGA6qVsMahWtHs0NXExPpEmvb783fNDmIVAc4Lm9MTm5w7ZbJbv4JLtRf3Ct/tL+KiWFIWje99dL0l2NPNamX/xHDT6dpO0q7prkpoTVFHK7LBIYCckbJwwgXYG64tlR7DExpX0/28qZ5S5J2/cvkQwLCuH4+NW0H781Fccep3Fz5T6CM5p9tX+JTysFdQ91IsDOw8LCydbpo7iya5MNxLKeKCWYlS/q2gSRzFEle24F27Ds3816Bvj1YAkyYpM3JFyxDqrRi4eH7aQd/uB79sKUykJiXO6bhW2aP7qMkMzLKtH7W5vMGnRD1i88fhbdZg2p6qknRnWBLdt7hL1YqFQZ1TLsUwXMJdSDTAXnySwiQqzU1GxglLCWa1PMsbIM5sBAdB5gjoBzlSWxLcNYFW876wUlgv8wFS9sretnDaK7cumjcPrBlfy4DmVe9BJWxnJfIR9nj42FQca2tms619r4FqFalgl6qt8Pb4AFn6kdDwatU3i0DfE7qF4+qZ5xkzn49s7Mx8PaFpwu6tyumgc38/uoiI4JawP7NvnN8+WzGuydvPhfZ/X5QrlGggniRaADnAfeIEESoS4746IS1NH9NsmLK391L/qsUth5rpConan/Ai2XWB9PwEE6jbRRun/fvHlwhURz+NgPXK565/cnn1iErt59F62EoLTIAPzyE4lAP2TRDRO15Ux/7JgRl1/7uRrsWnS52z1Po/H578ykDAs6/YGnVb71jX0dIEcRJvjOWWULkmKV6TncHqsRtMnS8w7C3hcZ8xhLV
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/roadmap.md", "description": "Read roadmap state"}`

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
… [19809 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nprint(type(d), list(d)[:20] if isinstance(d,dict) else len(d))\ntaches = d['taches'] if isinstance(d,dict) and 'taches' in d else d\nfor t in taches:\n    if t.get('id') in ('W1','W2','W3','W4','W5','W6'):\n   … [110 caractères tronqués]`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
{
  "id": "W1",
  "jour": 17,
  "titre": "J1 — le gold réel 452 : le split 402/H50",
  "mandat": "Tâche W1 (semaine 2, J1 matin, la part du pilote) : le gold réel 452 — **ne modifie pas le gold** (S/D). Écris `reports/rapport-gold-452.md` + JSON : (1) la composition exacte des 452 (20 hand + 432 corpus, par langue, par source) ; (2) le **split 402 / H50** proposé (50 phrases mises à l'écart, la règle déterministe du tirage, la graine) ; (3) le **sha256 avant** du gold ; (4) la **liste des 10 GP/SUB candidats à annoter** (les spans non attachés, avec leur phrase et leur cible) pour S ; (5) la constante « gold 200+ » retirée des docs. Ne touche pas `tools/tests/linguistique/gold_*.json`.",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f reports/rapport-gold-452.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    }
  ]
}
{
  "id": "W2",
  "jour": 17,
  "titre": "J2 — le tagger sur 402 et H50",
  "mandat": "Tâche W2 (J2 matin) : le tagger sur le split — mesure `evaluer --tagger` sur les 402 (l'entraînement) et sur les 50 H50 (la tenue à l'écart), avec le cache chaud puis l'API ; le POS de l'heuristique et du tagger 
… [3465 caractères tronqués]
  ```

- **bash** `{"command": "ls journal/sessions/session-bfc6d60f-dbfd-473c-a769-05fde9b1e428/; echo '--- plan ---'; cat journal/sessions/session-bfc6d60f-dbfd-473c-a769-05fde9b1e428/plan.md 2>/dev/null; echo '--- digest head ---'; sed -n '1200,1320p' journal/sessions/session-bfc6d60f-dbfd-473c-a769-05fde9b1e428/di … [72 caractères tronqués]`

  ```
digest.md
rapport.md
session.v4.jsonl.zstd
--- plan ---
--- digest head ---
  GN  patient        'moi'

 Il pense à son projet.
  GN  agent          'Il'
  GV  predicat       'pense'
  GP  destinataire   'à son projet'

 Le chat dort sur le canapé.
  GN  agent          'Le chat'
  GV  predicat       'dort'
  GP  lieu           'sur le canapé'

 Il part vers 9 h.
  GN  agent          'Il'
  GV  predicat       'part'
  GP  lieu           'vers'
  GP  lieu           'vers 9 h'

 Il court vers la gare.
  GN  agent          'Il'
  GV  predicat       'court'
  GP  lieu           'vers la 
… [1476 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nprint(type(d), list(d.keys())[:10] if isinstance(d,dict) else len(d))\ns=json.dumps(d,ensure_ascii=False)\nimport re\nfor m in re.finditer(r'.{200}W5.{400}', s):\n    print(m.group(0)); print('---')\nEOF", "d … [47 caractères tronqués]`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
nifeste.md` + JSON. **Ne modifie rien chez Panini.**", "budget_min": 90, "acceptation": [{"commande": "test -f reports/rapport-panini-manifeste.md && echo FICHE-OK", "attendu": "FIC
… [5877 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' journal/sessions/session-bfc6d60f-dbfd-473c-a769-05fde9b1e428/digest.md; echo '=== TAIL ==='; tail -80 journal/sessions/session-bfc6d60f-dbfd-473c-a769-05fde9b1e428/digest.md", "description": "Read current session digest head and tail"}`

  ```
# Session DSH — relecture

- identifiant : `session-bfc6d60f-dbfd-473c-a769-05fde9b1e428`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 11:05:10
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche W5 (J3 après-midi) : la restitution v3 — `_role_gp` distingue **lieu / temps / destinataire / possession / complément** (des prépositions : `à` + lieu/temps/destinataire, `de` + possession, `avec` + moyen...) ; mesure la **précision et le rappel par rôle** sur le gold v2 (46) et le gold S (61/144 existants), avec le **contrôle négatif** (permuter les rôles doit tuer la mesure). Fiche `reports/rapport-restitution-v3.md` + JSON, tests. Si les rôles ne se séparent pas, écris le négatif.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Compteurs vivants.** Dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; ne pas les recopier ici.

> **Porte d'entrée.** L
… [14340 caractères tronqués]
  ```

- **bash** `{"command": "git tag -l | tail -20; echo '---'; for t in $(git tag -l | tail -6); do echo \"== $t\"; git cat-file -t \"$t\"; git tag -n5 \"$t\" | head -8; git log -1 --format='%h %ci %s' \"$t\"; done", "description": "Inspect existing tags and annotations"}`

  ```
chantier-2026-11-14
semaine-2026-11-14
---
== chantier-2026-11-14
tag
chantier-2026-11-14 Chantier 2026-11-14 : 84 portes, 81 vertes, 3 rouges nommées (indice, melange, sessions) ; 28/28 acceptations ; J14.1
0e75f101 2026-11-14 06:32:00 -0500 J13.1 — LA TABLE DES MESURES : F1 0,7533 → 0,7902, ATTACHEMENT 236/237 → 238/238, BASE 612/602, 26 TÂCHES (25 VERTES, 1 ÉCHEC), 18 CONTRÔLES ; J14.1 RESTE (PASSE + TAG)
== semaine-2026-11-14
tag
semaine-2026-11-14 Semaine 2026-11-14 : tag de J5.2, posé à la clôture J14.1 sur le dernier commit vert 0e75f101
0e75f101 2026-11-14 06:32:00 -0500 J13.1 — LA TABLE DES MESURES : F1 0,7533 → 0,7902, ATTACHEMENT 236/237 → 238/238, BASE 612/602, 26 TÂCHES (25 VERTES, 1 ÉCHEC), 18 CONTRÔLES ; J14.1 RESTE (PASSE + TAG)
  ```

- **bash** `{"command": "grep -rn \"semaine-2026-11-14\\|chantier-2026-11-14\" docs reports journal | head -20", "description": "Find previous tag closure narrative"}`

  ```
docs/pilotage/semaine-autonome.md:176:**Reste** : la **clôture** (J14.1 : passe complète + tag `chantier-2026-11-14`), `g017` (la
docs/pilotage/semaine-autonome.md:203:| **J5** | après-midi : passe, tag, release | ❌ **échec** (timeout, tag absent) | passe **84/81/3** faite ailleurs (`2d6f5bff`) ; **pas de tag** | — | J14.1 : passe + tag `chantier-2026-11-14` |
docs/pilotage/semaine-autonome.md:253:(clôture : passe + tag `chantier-2026-11-14`). Avant, les lignes bloquées restent nommées :
docs/pilotage/roadmap.md:55:J7.1) ; la coordination N2/S/R/A est **datée**. La **clôture formelle** est faite en **J14.1** : sans refaire la passe, les trois rouges sont revérifiées et le tag `chantier-2026-11-14` est posé sur le dernier commit vert. Le détail — chiffres, décisions
docs/pilotage/roadmap.md:150:**J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag `chantier-2026-11-14`.** La
docs/pilotage/roadmap.md:155:ne rend pas son code pour le mélange). Le tag annoté `chantier-2026-11-14` est posé sur le dernier
docs/pilotage/roadmap.md:156:commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
reports/rapport-bilan-chantier.json:995: 
… [2094 caractères tronqués]
  ```

- **bash** `{"command": "date; echo '=== 09h53 registre tail ==='; tail -8 work/portes-1115-09h53/registre.txt; echo '=== w5 registre tail ==='; tail -8 work/portes-w5/registre.txt; echo '=== ps ==='; ps -o pid,etime,cmd -p 3923655,91839 2>/dev/null", "description": "Check gate pass progress"}`

  ```
dim 15 nov 2026 12:07:05 EST
=== 09h53 registre tail ===
porte-ressources 0 1
porte-sauvegarde-modele 0 58
porte-sessions 1 0
porte-speculatif 0 81
porte-tableaux 0 1
porte-tokenizer-kimi 0 7
porte-topologie 0 135
porte-trace 0 32
=== w5 registre tail ===
porte-echange-experts 0 81
porte-episodique 0 274
porte-etat 0 1
porte-flux 0 30
porte-fusion 0 10
porte-gain 0 281
porte-greffe 124 600
porte-harnais-invariants 0 128
=== ps ===
    PID     ELAPSED CMD
3923655    02:13:45 bash tools/toutes-les-portes.sh
  91839       45:45 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "git diff --cached -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-15/README.md journal/2026-11-15/mesures.md | sed -n '1,220p'", "description": "Review staged W5 docs changes"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index e8d05f9b..9746c69b 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 11 h 10 HNE (W4 : le manifeste Panini et le rejeu disponible)**
+**Mis à jour : 2026-11-15, 11 h 40 HNE (W5 : la restitution v3 — les rôles des GP)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -46,7 +46,7 @@
 - **Ambition** : rôles.
 - **Stratégie** : contrôles.
 - **Objectif final** : gold 60.
-- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
+- **Fait** : types **61/61**, rôles **144/144** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../repo
… [27684 caractères tronqués]
  ```

- **bash** `{"command": "python3 -m unittest tools.tests.test_restitution_v3 2>&1 | tail -5; echo '=== tagger ==='; python3 tools/tests/test_tagger_api.py 2>&1 | tail -3; echo '=== v2 ==='; python3 -m unittest tools.tests.test_restitution_v2 2>&1 | tail -3", "description": "Run W5 and tagger tests"}`

  ```
.............................
----------------------------------------------------------------------
Ran 29 tests in 2.600s

OK
=== tagger ===
Ran 21 tests in 6.280s

OK
=== v2 ===
Ran 17 tests in 1.352s

OK
  ```

- **bash** `{"command": "grep -n \"SEMAINE 2 — W5\\|W5 :\" journal/sessions/session-bfc6d60f-dbfd-473c-a769-05fde9b1e428/digest.md | tail -10; echo '---'; grep -rn \"W5 —\" journal/2026-11-15/README.md | head", "description": "Look for prepared W5 commit message"}`

  ```
---
117:### W5 — la restitution v3 : les cinq rôles se séparent, le cadre ne suit pas
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -30", "description": "Run documentation review"}`

  ```
revue de documentation · 753 fiche(s) · 846 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "sed -n '1,160p' docs/methode/portes.md", "description": "Read gates method"}`

  ```
# Les portes : lancer, lire le verdict, ne pas se tromper de rouge

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.

## La commande

```bash
bash tools/toutes-les-portes.sh
```

Elle lance **toutes** les `tools/porte-*.sh`, séquentiellement, **sans s'arrêter à la première rouge** (on veut le
[tableau](../theorie/glossaire/entrees/tableau.md), pas la première tuile), et borne **chaque** [porte](../theorie/glossaire/entrees/porte.md) à `DELAI=1800` s. Durée observée d'une passe complète :
**1 h 30 – 2 h** sur Hauru (**83 portes** ; certaines entraînent de petits modèles, d'autres utilisent les [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md) ;
`porte-deepseek` est **hors réseau** et rapide). La dernière passe complète à **82 portes** (03/11 11 h 30, **machine au repos**, **1 h 48**) a donné
**80 vertes, 2 rouges** (les 2 connues : `indice`, `melange`) ;
`porte-reparti-moteur` (ré-étalonnée à 8,7434) et `porte-homeostasie` (auto-générée) sont **vertes** ;
la liste et le diagnostic sont dans
[`references-non-regression.md`](../pilotage/references-non-regression.md). `porte-deepseek` est **
… [3931 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/porte-tableaux.sh; echo '=== document ==='; sed -n '1,100p' tools/porte-document.sh; echo '=== etat ==='; sed -n '1,80p' tools/porte-etat.sh", "description": "Inspect targeted gate scripts"}`

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
… [6909 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- tools/drave.py | head -120; echo '=== staged drave ==='; git diff --cached -- tools/drave.py | head -160", "description": "Compare staged and unstaged drave.py changes"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index b4b767d2..ec45a311 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -246,6 +246,30 @@ def _cout_tagger(stats: dict) -> dict:
             "modeles_renvoyes": dict(stats["modeles"])}
 
 
+def _cout_pour_phrases(cout: dict, mesurees: int, cible: int) -> dict:
+    """Le coût d'un lot de `cible` phrases, au prorata du lot **mesuré**.
+
+    Le tagger fait **un appel par phrase** : le coût est linéaire en nombre de phrases. On ne
+    modélise pas la longueur des phrases (le prompt la porte), donc ce chiffre vaut pour un lot
+    de même longueur moyenne que le lot mesuré. `mesurees` est le nombre de phrases réellement
+    passées au tagger ; il ne doit pas être confondu avec le nombre d'appels (le cache mémoire
+    peut en servir plusieurs).
+    """
+    mesurees = max(1, int(mesurees))
+    cible = max(0, int(cible))
+    ratio = cible / mesurees
+    return {
+        "phrases": cible,
+        "phrases_mesurees": mesurees,
+        "modele": cout.get("modele", MODELE_TAGGER),
+        "appels": int(round(cout.get("appels", 0) * ratio)),
+        "requetes": int(round(cout.get("requetes", 0) * ratio)),
+        "cache": int(ro
… [7582 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat be3f41ad | head -40; echo '=== HEAD drave has cost? ==='; git show HEAD:tools/drave.py | grep -n \"cout_pour_1000\\|_cout_pour_phrases\" | head; echo '=== index drave has cost? ==='; git show :tools/drave.py | grep -n \"cout_pour_1000\\|_cout_pour_phrases\" | head; echo  … [150 caractères tronqués]`

  ```
commit be3f41adc89b7f7bda103a54262ecf0c358c4339
Author: Stéphane <stephane@localhost>
Date:   Sun Nov 15 10:47:30 2026 -0500

    SEMAINE 2 — W3 : LA MATRICE DU TAGGER (DÉFAUT HORS LIGNE CODE 0, CLÉ INVALIDE 4, RÉSEAU COUPÉ 0 APRÈS 3 ESSAIS, 1 000 PHRASES = 143 870 TOKENS) ; 4 TESTS DE PLUS

 docs/pilotage/en-cours.md                          |   28 +-
 journal/2026-11-15/README.md                       |    7 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/mesures.md                      |   15 +-
 journal/2026-11-15/modele.md                       |    5 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    6 +-
 journal/sessions/MANIFEST.md                       |    8 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  137 ++
 .../rapport.md                                     |   17 +-
 .../digest.md                                      |  121 +
 .../rapport.md                                     |   47 +-
 .../digest.md                          
… [849 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"cout_pour_1000\\|_cout_pour_phrases\" tools/tests/test_tagger_api.py | head -20; git show HEAD:tools/tests/test_tagger_api.py | grep -n \"cout_pour_1000\\|_cout_pour_phrases\" | head -20", "description": "Check W3 test dependency on cost function"}`

  ```
493:    def test_cout_pour_1000_phrases(self) -> None:
520:        cout = donnees["tagger"]["cout_pour_1000_phrases"]
493:    def test_cout_pour_1000_phrases(self) -> None:
520:        cout = donnees["tagger"]["cout_pour_1000_phrases"]
  ```

- **todo_write** `{"todos": [{"content": "Vérifier l'état W5 (tests, revue, fichiers stagés) et committer W5 + le champ de coût W3 manquant", "status": "in_progress"}, {"content": "Lire les portes (dernière passe complète + passes du 15/11) et consigner le relevé", "status": "pending"}, {"content": "Écrire reports/ra … [478 caractères tronqués]`

  ```
Updated todo list: 6 pending, 1 in progress, 0 completed.
  ```

- **bash** `{"command": "ls work/msg-* | tail -20; grep -l \"W5\\|restitution v3\" work/msg-* 2>/dev/null", "description": "Look for a prepared W5 commit message"}`

  ```
work/msg-backlog-n2.txt
work/msg-bilan.txt
work/msg-claims.txt
work/msg-cle2.txt
work/msg-cle3.txt
work/msg-cle.txt
work/msg-cpt.txt
work/msg-etat.txt
work/msg-homeo2.txt
work/msg-homeo.txt
work/msg-j2.txt
work/msg-jour.txt
work/msg-n2-sed.txt
work/msg-n2-sous25.txt
work/msg-nuit.txt
work/msg-p3.txt
work/msg-passe82.txt
work/msg-pin.txt
work/msg-r11.txt
work/msg-refs.txt
[exit code: 1]
  ```

- **bash** `{"command": "python3 tools/drave.py restituer \"Le train part à 14 h.\" --roles-v3 | head -30; echo '=== banc ==='; python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --roles-v3 --json 2>/dev/null | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['synthese'][ … [105 caractères tronqués]`

  ```
restitution v3 (rôles de GP)
source          : 'Le train part à 14 h.'
cadre principal :
  agent         : Le train
  prédicat      : part
  lieu          : —
segments de rôle: 2 (1 agents, 1 prédicats, 0 lieux)

rôles (agent, prédicat, lieu)
  agent     : Le train
  prédicat  : part
  lieu      : —
  autres    : temps: à 14 h
segments de rôle : 2
   1. GN/agent [0:8] « Le train » → part
   2. GV/predicat [9:13] « part » → train

rôles de GP (v3) : temps: 1

restitution du rendu : exacte (relire_roles(rendre_roles(a)))
contrôle négatif      : retrait détecté · permutation détectée · détecté True
=== banc ===
17 0.5406
  ```

- **bash** `{"command": "git diff --cached -- reports/INDEX.md reports/README.md journal/2026-11-15/outils.md | head -80", "description": "Check staged index/readme entries"}`

  ```
diff --git a/journal/2026-11-15/outils.md b/journal/2026-11-15/outils.md
index 011b80b5..8c52c5a4 100644
--- a/journal/2026-11-15/outils.md
+++ b/journal/2026-11-15/outils.md
@@ -28,4 +28,14 @@
 
 <!-- notes -->
 
+
+### W5 — la règle de rôle et son banc
+
+Nouveau module pur [`tools/roles_gp.py`](../../tools/roles_gp.py) (règle + 24 cas), mesure
+[`tools/restitution_v3.py`](../../tools/restitution_v3.py) (préparation, appariement v2/v3,
+`mesurer_banc_v3`, `mesurer_gold_analyseur_v3`, contrôles), script
+[`tools/mesurer_restitution_v3.py`](../../tools/mesurer_restitution_v3.py) et **29** tests
+[`tools/tests/test_restitution_v3.py`](../../tools/tests/test_restitution_v3.py). Le CLI gagne
+`restituer --roles-v3` (opt-in) ; `--roles` v2 est inchangé et la suite v2 (17 tests) passe.
+
 <!-- /notes -->
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 03a54867..7e3867ec 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **748 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **750 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) so
… [2974 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached --name-only; echo '--- unstaged names ---'; git diff --name-only", "description": "List staged and unstaged files"}`

  ```
docs/pilotage/en-cours.md
docs/pilotage/roadmap.md
journal/2026-11-15/README.md
journal/2026-11-15/docs.md
journal/2026-11-15/mesures.md
journal/2026-11-15/outils.md
reports/INDEX.md
reports/README.md
reports/pensee-restitution-v3.json
reports/rapport-restitution-v3.md
tools/bloc_linguistique.py
tools/drave.py
tools/mesurer_restitution_v3.py
tools/restitution_v3.py
tools/roles_gp.py
tools/tests/test_restitution_v3.py
--- unstaged names ---
docs/produit/README.md
journal/README.md
journal/sessions/MANIFEST.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
journal/sessions/session-5d421585-1af2-4f07-ac86-e4879cc23d4f/digest.md
journal/sessions/session-5d421585-1af2-4f07-ac86-e4879cc23d4f/rapport.md
reports/pensee-coherence-fiches-v7.json
reports/pensee-dev-test-v10.json
reports/pensee-quatre-modes.json
reports/rapport-audit-v7.md
reports/rapport-coherence-fiches-v7.md
reports/rapport-dev-test-v10.md
reports/rapport-pensee-v12.md
reports/rapport-spans-chunker.md
tools/chantier/plan.json
tools/drave.py
  ```

- **bash** `{"command": "cat > work/msg-w5.txt <<'EOF'\nSEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE GOLD v2 NE GAGNE QU'UN CADRE (20/46, F1 0,5406, LIEU 0,60) ; --roles-v3 OPT-IN\n\nLa règle tools/roles_gp.py quitte la préposition seule pour le context … [1200 caractères tronqués]`

  ```
[stderr]
  ✅ index : aucun fait stagé sans état
[still running after 60000ms; moved to background job bash-53]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-53", "wait": true, "timeout_ms": 120000}`
