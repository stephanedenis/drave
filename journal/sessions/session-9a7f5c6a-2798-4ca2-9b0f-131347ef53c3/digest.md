# Session DSH — relecture

- identifiant : `session-9a7f5c6a-2798-4ca2-9b0f-131347ef53c3`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 08:57:01
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche W1 (semaine 2, J1 matin, la part du pilote) : le gold réel 452 — **ne modifie pas le gold** (S/D). Écris `reports/rapport-gold-452.md` + JSON : (1) la composition exacte des 452 (20 hand + 432 corpus, par langue, par source) ; (2) le **split 402 / H50** proposé (50 phrases mises à l'écart, la règle déterministe du tirage, la graine) ; (3) le **sha256 avant** du gold ; (4) la **liste des 10 GP/SUB candidats à annoter** (les spans non attachés, avec leur phrase et leur cible) pour S ; (5) la constante « gold 200+ » retirée des docs. Ne touche pas `tools/tests/linguistique/gold_*.json`.

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

- **bash** `{"command": "pwd && ls -la && git status --short | head -50 && git log --oneline -5", "description": "Inspect repo root and git state"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 06:29 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198 15 nov 08:57 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 77688 15 nov 06:59 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [1968 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/tests/linguistique/ 2>/dev/null | head -40; echo '---'; ls -la reports/ | head -40", "description": "List gold dir and reports dir"}`

  ```
total 1540
drwxr-xr-x. 1 stephane stephane    964 15 nov 04:59 .
drwxr-xr-x. 1 stephane stephane   1018 15 nov 06:38 ..
-rw-r--r--. 1 stephane stephane  16090  2 nov 09:26 anaphore.py
-rw-r--r--. 1 stephane stephane  35148  5 nov 14:25 classement_cible.py
-rw-r--r--. 1 stephane stephane   6231  7 nov 13:02 classer_gv.py
-rw-r--r--. 1 stephane stephane  15762  6 nov 19:50 evaluer_gold.py
-rw-r--r--. 1 stephane stephane 450905  2 nov 13:27 gold_gele.json
-rw-r--r--. 1 stephane stephane  20009 15 nov 07:40 gold.json
-rw-r--r--. 1 stephane stephane   7813  2 nov 12:03 gold.py
-rw-r--r--. 1 stephane stephane  29924 15 nov 02:45 gold_reel_50.py
-rw-r--r--. 1 stephane stephane 470149  2 nov 14:39 gold_reel.json
-rw-r--r--. 1 stephane stephane 132934  5 nov 14:04 gold_reel.py
-rw-r--r--. 1 stephane stephane  14631 15 nov 04:59 gold_restitution_v2.json
-rw-r--r--. 1 stephane stephane   1939  5 nov 17:52 gold_split.py
-rw-r--r--. 1 stephane stephane 149211  6 nov 18:56 gold_synthetique.json
-rw-r--r--. 1 stephane stephane  10222  6 nov 18:55 gold_synthetique.py
-rw-r--r--. 1 stephane stephane   2953  2 nov 12:17 juge.py
-rw-r--r--. 1 stephane stephane  22366  3 nov 14:05 miroir.py
drwxr-xr-x
… [3762 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"452\" docs/pilotage/ docs/methode/ tools/chantier/plan.json 2>/dev/null | head -60", "description": "Search plan for 452 references"}`

  ```
docs/pilotage/semaine-autonome.md:281:| C3 **R** | ✅ | le « gold 200+ » **défini** (452 phrases), 50 ratées sélectionnées |
docs/pilotage/semaine-2.md:26:| **gold réel** | **452** phrases (402 + H50), 184 cibles ; le nom « 200+ » est **obsolète** | H50 n'est pas encore un **test** ; **10 GP/SUB** à annoter (dont 4 dans H50) ; le dénominateur passe à **194** | [C3](../../reports/rapport-gold-reel-50.md) |
docs/pilotage/semaine-2.md:30:| **tagger** | **+8,49** pts sur 612, **+6,1** sur 452 ; 4 cas d'erreur caractérisés | la question du **défaut** : coût, latence, clé absente, hors-ligne | [D1](../../reports/rapport-exemples-tagger.md) · [E2](../../reports/rapport-tagger-erreurs.md) |
docs/pilotage/semaine-2.md:32:**Le gold n'est pas à recompter.** 452 est le **nombre** ; H50 est le **statut de test** ; les
docs/pilotage/semaine-2.md:48:| **J1 · 16/11** | matin | **Le gold réel 452, nommé et tenu à l'écart** : retirer « gold 200+ » ; figer le split **402 / H50** ; annoter les **10 GP/SUB** (4 dans H50) ; sha256 du gold avant/après. | S + pilote | fiche gold 452 + JSON ; 402 vs H50 ; **184 → 194** cibles ; double codage **4/10**. | C3 ; le gold est à S |
docs/pilotage/semaine-2.md:56:|
… [2904 caractères tronqués]
  ```

- **bash** `{"command": "head -80 tools/tests/linguistique/gold_reel_50.py; echo '==='; head -60 tools/tests/linguistique/gold_split.py", "description": "Inspect gold_reel_50 and gold_split"}`

  ```
#!/usr/bin/env python3
"""gold_reel_50.py — les 50 phrases réelles que l'heuristique rate (proposition C3/R).

POURQUOI. Le gold réel (`gold.json` 20 hand + `gold_reel.json` 432 reel) mesure le bloc
linguistique depuis B13. Ses erreurs ne sont plus réparties : le POS porte 275 erreurs de
tokens, la segmentation 346 segments manquants (dont 74 ADJ/ADV/PONCT que l'heuristique ne
produit pas), l'attachement **une seule** (g017, SUB). Le « gold 200+ » des fiches R n'est
donc pas un problème de **nombre** (452 > 200) : c'est un problème de **discrimination**.
Ce banc sélectionne 50 phrases réelles que l'heuristique rate, mesure ce qu'elles ajoutent,
et liste les **candidats à annoter** — sans modifier le gold (territoire S/D).

RÈGLE DE SÉLECTION (déterministe, aucune graine).
  1. score = 3 × (cible d'attachement absente ou fausse)
           + 2 × (token POS faux)
           + 1 × (segment gold absent au même span) ;
  2. quota 25 français + 25 anglais ;
  3. au plus 2 phrases par **signature d'erreur** (POS confondus, types de segments absents,
     types d'attachement) : une construction ne peut pas prendre tout le lot (les 11 négations
     « Ne …-t-il pas ? » sont plafonnées) ;
  
… [3916 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ | grep -i gold; echo '==='; ls -la reports/ | grep -i \"reel-50\\|452\"; echo '==='; sed -n '570,620p' tools/chantier/plan.json", "description": "Find existing gold reports and W1 task"}`

  ```
-rw-r--r--. 1 stephane stephane     381  2 nov 03:58 pensee-gold-200.json
-rw-r--r--. 1 stephane stephane     530  2 nov 09:18 pensee-gold-342.json
-rw-r--r--. 1 stephane stephane   23145  5 nov 16:00 pensee-gold-anglais.json
-rw-r--r--. 1 stephane stephane   32798  2 nov 23:21 pensee-gold-cascade-200.json
-rw-r--r--. 1 stephane stephane   32777  2 nov 18:20 pensee-gold-cascade.json
-rw-r--r--. 1 stephane stephane     427  2 nov 04:53 pensee-gold-complexes100.json
-rw-r--r--. 1 stephane stephane     419  2 nov 04:37 pensee-gold-complexes20.json
-rw-r--r--. 1 stephane stephane     418  2 nov 04:45 pensee-gold-complexes50.json
-rw-r--r--. 1 stephane stephane     415  2 nov 04:23 pensee-gold-complexes.json
-rw-r--r--. 1 stephane stephane     413  2 nov 05:01 pensee-gold-discours.json
-rw-r--r--. 1 stephane stephane     241  2 nov 13:32 pensee-gold-gele.json
-rw-r--r--. 1 stephane stephane     639  6 nov 19:02 pensee-gold-gp-corrige.json
-rw-r--r--. 1 stephane stephane   31377  1 nov 20:16 pensee-gold-linguistique.json
-rw-r--r--. 1 stephane stephane   20947  2 nov 16:53 pensee-gold-neuronal.json
-rw-r--r--. 1 stephane stephane    4558  2 nov 19:06 pensee-gold-pragmatique.json
-rw-r--r
… [5031 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,130p' docs/pilotage/semaine-2.md", "description": "Read semaine-2 plan"}`

  ```
# La semaine 2 — cinq jours, deux vagues, quatre chantiers et une décision

> **Ce que ce document est.** Le plan du **16 au 22 novembre 2026** : ce qui se fait, dans quel
> ordre, avec quelles dépendances, quels contrôles et quels livrables. Il **succède** à
> [`semaine-autonome.md`](semaine-autonome.md), qui reste l'**archive** de la semaine 1 et n'est
> **pas modifié**. L'état courant est dans [`en-cours.md`](en-cours.md) ; les chiffres sont dans
> les fiches citées, jamais recopiés ici.
>
> **Sources.** Le [bilan de la semaine](../../reports/rapport-bilan-semaine.md) et les fiches des
> tâches C/B/D/E : [C1](../../reports/rapport-coordination-n2-v2.md), [C2](../../reports/rapport-coordination-s-v2.md),
> [C3](../../reports/rapport-gold-reel-50.md), [B1](../../reports/rapport-protocole-date.md),
> [B2](../../reports/rapport-atomes-prediction.md), [B3](../../reports/rapport-cic-v2.md),
> [D1](../../reports/rapport-exemples-tagger.md), [D2](../../reports/rapport-restitution-v2.md),
> [D3](../../reports/rapport-faq.md), [E1](../../reports/rapport-faq-sommaire.md),
> [E2](../../reports/rapport-tagger-erreurs.md). Le plan ne promet aucun chiffre : il nomme la
> mesure, son **contrôle
… [10659 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' reports/rapport-gold-reel-50.md", "description": "Read existing C3 report part 1"}`

  ```
# R0.7 / B13 — le gold réel étendu : 50 phrases que l'heuristique rate, et ce qu'elles disent

> **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **B13** · **Tâche** : C3 (coordination R) ·
> **Date** : 2026-11-15 · **HEAD mesuré** : `f926b5bc` · **Verdict** : ✅ **le gold réel n'est pas un
> problème de nombre** (452 phrases, déjà > 200) : c'est un problème de **discrimination**. Les
> **50 phrases réelles dures** (2 hand + 48 reel ; 25 fr + 25 en ; les plus coûteuses, à
> diversité plafonnée) portent **37,1 %** des erreurs POS et **25,1 %** des segments absents pour
> **11,1 %** des phrases ; l'heuristique y fait **68,42 %** de POS (étiquettes seules **75,68 %**)
> contre **91,98 %** sur le reste. L'attachement, lui, est **saturé** : **183/184** (une seule
> erreur, `g017`). L'extension utile est donc **un lot dur tenu à l'écart** + **10 cibles GP/SUB à
> annoter** (dont 4 dans le lot), **pas 50 phrases de plus**.

**En trois lignes.** (1) Le « gold 200+ » est **défini** : c'est le gold **linguistique** hand + reel
(452 phrases, 2 480 tokens, 184 cibles d'attachement), pas le gold de pensée ; le libellé « 200+ »
est **obsolète** et ambigu (T15). (2) On sélectionne **50 phr
… [10374 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"gold 200+\\|gold 200 +\\|200+\\|200 +\" docs/ --include='*.md' | head -80", "description": "Search docs for gold 200+ mentions"}`

  ```
docs/pilotage/plan-travail.md:39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **166/166** (6 S fixés ; T132/T133 2/5), gold **432**, 116 liens ; **gold neuronal** (POS **0,9415** / syntagmes **0,7539** / acte **1,0**) ; **DRVM/native** règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusion par sous-type : le double sens 0,9884 (+0,0208) ; variance du sous-type : 0,9838 ; tirages : 0,9838 ×3 (déterministe sur ces invites) ; attachement : top1 0,3431, exact 0,0042 ; cibles : 1863 segments, 1624 sans cible (87,2 %), couverture réelle 0,1283 ; cibles 500 : 294 GN / 206 GV ; relation GN → GV : 221/637 ; rôles par position : 301/322, relation 0,8195 (522/637) surévaluée ; correctif `par` → agent (partiel : le générateur S garde `moyen`) ; sans `par` : le chunker 3/3, le générateur S ignore ; cible par proximité : exact 0,0042 → 0,0544 ; candidats verbes : top-k 0,4686, tête 0,7655 ; échecs qualifiés : 127 = 94 span + 33 cible** (négation/modalité sous l'heuristiq
… [13687 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"H50\" docs/ reports/ journal/ work/ tools/chantier/plan.json 2>/dev/null | head -80", "description": "Search H50 references"}`

  ```
QlaErYTMvvpsFuJWrjlKAsu7/Xs3Qy93zHJ9w3e+Ml4qOCI76UxmHmy+e8dMf2rC+ptejYyv4XfhSvnfPvajGbn/rY+IR85dXePWyu4f/lh2Uv7v1gdx0LOGMucXtqO01VVZ1GT61b4vPUdZqrkusSOAeHSrC1tWTLtFSXS4R3vnK5Y8m0VAUlkt8yQI7Az82HVgXULRLnjg8ceLBB56NsCUPX4yTehdDpnBk14sCqK2YyrV/IUbj6el1Sv6Sz+3RooaolS6oCLXbRV386AHcv8Qu70sO+8lgeN03Z97j4RAcOeTq7e3q6nTxSIBSQ0LAD4MBSqZQqljZwDsycMTPAkMuZ5r51GHhQTZANu7fiPVbZTnSnq+/yrE289gN/7Mvf/t/k+V0zUIrD7P9SfKFr2ro/sJdr/Qc414Yv0xfoP3909tDhW6B8ABfLxBMYRDUs2b59iUGc3bcP5CAkSPEjUa0HAkkGIdt04lVT88TmjXO1JMTjwkbAugEiJnVzgdwGXPr/Ve0bwFJoqkvKXOMO+dkNf6OVpJM/T0ilfyERnSyZb7GI3WrRTZD1oOrTCjkeUErv3/hku3jkll+u/I5WpjL3DI+oA7oQN1HbpjZsTOl81N6HAQg7WwBf1QHga9Zt83KN8f1LoiI9g415cU44hs1906ZO8xH9a6d4+jSQaDzDvmEyr4Hvpviwj/bh3KXVyJ1XrJXX2RdFw1OmBMr/J46F+/5ISjjD9Q5jnWOOfkvRt0AdzrkM9dY5xmVF73yAfTDB5jIwa2pWQ99BziqEYOOVWx74u/zIcBwk8Q8RNlsnDwfL8upg/emPhzZrh8YMPXMO1T0blLci9ebnw+G7nerD2tYueaSiWc49dKgpiEI4hkPUwUaO5pErhvROftwuXNUzMt0MHzhI/dy1KwGeaA1T9Zs5DBGcRtthat+2G1gvuMP0qBDT367BbQr5kEPcfLNmqsD23INa+cpgXuA37521y60FQZxJUB1P+bSeuJiUCOh3npgqXjTvus7hTXRro7rHGMnXyzggKSIo1dRnDICFxv+oD2/Pcd3c6CBmLeDmzk5ssptu9ooPJamJmzgHR5LI5Z3Z47xrgrTXMzg45JUGpe7kp6tqYslElQVn//WUBcHnEQObw54exVm2g+vjqrspcSq31Krzre5b+rNBk4og9vYOm6pKSXDbb8DU/OUiox
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"graine\" reports/rapport-gold-reel-50.md tools/tests/linguistique/gold_reel_50.py docs/pilotage/semaine-2.md | head -40", "description": "Search seed mentions in gold 50"}`

  ```
reports/rapport-gold-reel-50.md:69:**Score par phrase** (déterministe, aucune graine) :
reports/rapport-gold-reel-50.md:214:| mesure | global 452 | **lot dur 50** | reste 402 | hasard stratifié (8 graines) |
reports/rapport-gold-reel-50.md:236:| uniforme (12 classes, graine 0) | **8,36 %** (lot) · 9,56 % (global) | — | — |
reports/rapport-gold-reel-50.md:237:| 50 au hasard, 8 graines | 85,00–91,01 % | 76,22–83,85 % | 100 % |
reports/rapport-gold-reel-50.md:238:| 50 stratifiées, 8 graines | 87,24–90,77 % | 73,68–83,63 % | 95,0–100 % |
reports/rapport-gold-reel-50.md:242:la plage stratifiée (une graine tire `g017`). L'heuristique reste **3,1×** au-dessus du majoritaire
reports/rapport-gold-reel-50.md:398:- **Le hasard.** Les contrôles sont à **8 graines**, pas exhaustifs : une autre graine peut sortir
reports/rapport-gold-reel-50.md:431:  — lecture seule, `--sortie`, aucune graine pour la sélection.
tools/tests/linguistique/gold_reel_50.py:12:RÈGLE DE SÉLECTION (déterministe, aucune graine).
tools/tests/linguistique/gold_reel_50.py:22:CONTRÔLES. 50 tirées au hasard (8 graines), 50 stratifiées (25 fr + 25 en, 1 hand par langue),
tools/tests/linguistique/gold_reel_50.py:302:    for gra
… [1182 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '220,470p' reports/rapport-gold-reel-50.md", "description": "Read C3 report part 2"}`

  ```
| phrases | 452 | 50 | 402 | 50 |
| tokens | 2 480 | 323 | 2 157 | 260–296 |

**Part des erreurs** : le lot fait **11,1 %** des phrases et **13,0 %** des tokens, mais il porte
**37,1 %** des erreurs POS (102/275), **25,1 %** des segments absents (87/346) et **100 %** de
l'erreur d'attachement (1/1). C'est un **stress test**, pas un échantillon.

**Écart mesuré, pas projeté** : le lot dur est **23,56 points** sous le reste pour le POS,
**23,54** sous le reste pour la F1, **4,55** sous le reste pour l'attachement (mais ce dernier
n'est que `g017`).

**Contrôles négatifs.**

| contrôle | POS | F1 | attachement |
|---|---:|---:|---:|
| majoritaire (classe la plus fréquente) | **21,98 %** (PRON, lot) · 23,47 % (global) | — | — |
| uniforme (12 classes, graine 0) | **8,36 %** (lot) · 9,56 % (global) | — | — |
| 50 au hasard, 8 graines | 85,00–91,01 % | 76,22–83,85 % | 100 % |
| 50 stratifiées, 8 graines | 87,24–90,77 % | 73,68–83,63 % | 95,0–100 % |
| **lot dur 50** | **68,42 %** | **58,36 %** | **95,45 %** |

Le lot dur est **sous les deux plages** pour le POS et la F1 ; pour l'attachement, il est **dans**
la plage stratifiée (une graine tire `g017`). L'heuristique reste **3,1×** au-des
… [12829 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/rapport-gold-reel-50.json'\nd=json.load(open(p))\nprint(type(d), list(d.keys())[:40])\nfor k,v in d.items():\n    if isinstance(v,(dict,list)):\n        print(k, type(v).__name__, len(v))\n    else:\n        print(k, repr(v)[:120])\nPY", "descri … [46 caractères tronqués]`

  ```
<class 'dict'> ['date', 'ligne', 'tache', 'commit_mesure', 'objet', 'heuristique', 'selection', 'mesure', 'erreurs_hard_50', 'candidats_a_annoter', 'controles_negatifs', 'gold_intact', 'limites', 'ce_qui_ferait_faux', 'fichiers']
date '2026-11-15 02:46 EST'
ligne 'R0.7 / B13'
tache 'C3 — coordination R, le gold réel étendu'
commit_mesure 'f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888'
objet dict 8
heuristique dict 4
selection dict 4
mesure dict 11
erreurs_hard_50 dict 5
candidats_a_annoter dict 4
controles_negatifs dict 5
gold_intact dict 3
limites list 7
ce_qui_ferait_faux list 5
fichiers dict 4
  ```

- **bash** `{"command": "grep -n \"def \\|SIGNATURE\\|signature\\|selection\\|score\\|tri\\|sorted\" tools/tests/linguistique/gold_reel_50.py | head -80", "description": "Locate selection function in gold_reel_50.py"}`

  ```
13:  1. score = 3 × (cible d'attachement absente ou fausse)
17:  3. au plus 2 phrases par **signature d'erreur** (POS confondus, types de segments absents,
59:def sha256(chemin: pathlib.Path) -> str:
63:def charger() -> list[dict]:
74:def commit() -> str:
77:                              text=True, timeout=10).stdout.strip() or "inconnu"
85:def _span(texte: str, d: int, f: int) -> str:
89:def analyser(h, p: dict) -> dict:
117:    fn = sorted(gold_seg - pred_seg)
118:    fp = sorted(pred_seg - gold_seg)
119:    tp = sorted(gold_seg & pred_seg)
142:    signature = (
144:        tuple(sorted((x["gold"], x["predit"]) for x in pos_erreurs)),
145:        tuple(sorted(x[0] for x in fn)),
146:        tuple(sorted((x["type"], x["erreur"]) for x in att_erreurs)),
162:        "signature": signature,
163:        "score": 3 * len(att_erreurs) + 2 * len(pos_erreurs) + len(fn),
170:def _rangs(rows: list[dict], wa: int, wp: int, wf: int) -> list[dict]:
172:        r["score"] = wa * len(r["attachement"]["erreurs"]) + wp * len(r["pos"]["erreurs"]) \
174:    return sorted(rows, key=lambda r: (-r["score"], r["id"]))
177:def selectionner(rows: list[dict], wa: int = 3, wp: int = 2, wf: int = 1,
179:    
… [2342 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '80,340p' tools/tests/linguistique/gold_reel_50.py", "description": "Read gold_reel_50 selection logic"}`

  ```
# --------------------------------------------------------------------------- analyse


def _span(texte: str, d: int, f: int) -> str:
    return texte[d:f]


def analyser(h, p: dict) -> dict:
    """Une phrase : POS, segments, attachement, et la liste de ses erreurs."""
    texte = p["texte"]
    a = h.analyser(texte, p.get("langue") or "fr")
    pos = {(e.debut, e.fin): e.type for e in a.etiquettes if e.niveau == "pos"}

    pos_erreurs, pos_n = [], len(p["mots"])
    ok = ok_ferme = ok_ouvert = n_ferme = n_ouvert = 0
    for m in p["mots"]:
        pred = pos.get((m["debut"], m["fin"]), "?")
        juste = pred == m["pos"]
        ok += juste
        if m["pos"] in FERME:
            n_ferme += 1
            ok_ferme += juste
        else:
            n_ouvert += 1
            ok_ouvert += juste
        if not juste:
            pos_erreurs.append({"token": m["texte"], "gold": m["pos"], "predit": pred,
                                "debut": m["debut"], "fin": m["fin"],
                                "classe": "fermé" if m["pos"] in FERME else "ouvert",
                                # « ? » = aucun token prédit à ce span : c'est la
                                # tokenisat
… [10781 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pprint\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nfor k in ['objet','selection','mesure','candidats_a_annoter','gold_intact','fichiers']:\n    print('='*20,k)\n    pprint.pp(d[k], width=160, sort_dicts=False)\nPY", "description": "Dump C3 JSO … [18 caractères tronqués]`

  ```
, 'fp': 0, 'fn': 0, 'precision': 1.0, 'rappel': 1.0, 'f1': 1.0},
                                                                'REL': {'tp': 5, 'fp': 1, 'fn': 0, 'precision': 0.8333, 'rappel': 1.0, 'f1': 0.9091},
                                                                'SUB': {'tp': 4, 'fp': 0, 'fn': 0, 'precision': 1.0, 'rappel': 1.0, 'f1': 1.0},
                                                                'ADJ': {'tp': 0, 'fp': 0, 'fn': 3, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0},
                                                                'ADV': {'tp': 0, 'fp': 0, 'fn': 2, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0},
                                                                'PONCT': {'tp': 0, 'fp': 0, 'fn': 2, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0}},
                                      'attachement': {'cibles': 20,
                                                      'justes': 20,
                                                      'erreurs': 0,
                                                      'exactitude': 1.0,
                                                      'par_type': {'GP': {'cibles': 11, 'justes': 11, 'erreurs': 0, 'exactitude':
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nfor f in ['gold.json','gold_reel.json']:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    print('='*10,f, list(d.keys()))\n    ph=d['phrases']\n    print('n phrases', len(ph))\n    print('keys sample', list(ph[0].keys()))\n    print( … [352 caractères tronqués]`

  ```
========== gold.json ['version', 'phrases', 'note']
n phrases 20
keys sample ['id', 'langue', 'texte', 'mots', 'segments', 'pragma']
ex0 {"id": "g001", "langue": "fr", "texte": "Le chat dort.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chat", "pos": "NOUN", "debut": 3, "fin": 7}, {"texte": "dort", "pos": "VERB", "debut": 8, "fin": 12}], "segments": [{"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}, {"type": "GV", "texte": "dort", "role": "prédicat", "debut": 8, "fin": 12}], "pragma": {"acte": "assertion"}}
langues Counter({'fr': 14, 'en': 6})
sources Counter({None: 20})
ids first ['g001', 'g002', 'g003', 'g004', 'g005', 'g006', 'g007', 'g008', 'g009', 'g010'] last ['g016', 'g017', 'g018', 'g019', 'g020']
========== gold_reel.json ['version', 'source', 'note', 'phrases']
n phrases 432
keys sample ['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source']
ex0 {"id": "r001", "langue": "fr", "texte": "Le chien mange une pomme.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chien", "pos": "NOUN", "debut": 3, "fin": 8}, {"texte": "mange", "pos": "VERB", "debut": 9, "fin": 14}, {"texte": "une", "pos
… [601 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nprint('selection keys', list(d['selection'].keys()))\nfor k,v in d['selection'].items():\n    if isinstance(v,list):\n        print(k,'list',len(v))\n        if v: print('  sample', json. … [733 caractères tronqués]`

  ```
selection keys ['regle', 'phrases', 'ids', 'composition']
regle "score = 3×att + 2×POS + 1×segment absent ; 25 fr + 25 en ; au plus 2 phrases par signature d'erreur ; départage par id."
phrases list 50
  sample {"id": "g017", "source": "hand", "langue": "en", "texte": "She said that she would come yesterday.", "score": 4, "pos_erreurs": 0, "segments_fn": 1, "segments_fp": 1, "att_erreurs": 1}
ids list 50
  sample "g017"
composition {"sources": {"hand": 2, "reel": 48}, "langues": {"en": 25, "fr": 25}, "signatures_distinctes": 42, "score_min": 3, "score_max": 10, "tokens": 323, "segments": 190, "cibles_attachement": 22}
mesure keys ['global_452', 'hard_50', 'reste_402', 'hand_20', 'reel_432', 'fr_242', 'en_210', 'part_des_erreurs', 'controles', 'sensibilite_poids', 'projection_502']
  global_452 {'phrases': 452, 'tokens': 2480, 'pos': {'exactitude': 0.8891, 'ferme': 0.9294, 'ouvert': 0.8466, 'justes': 2205, 'erreurs': 275, 'tokenisation': 66, 'etiquette_exactitude': 0.9134, 'note': '`exactitude` compte la tokenisation ; `etiquette_exactitude` retire les tokens gold sans token prédit (« ? »).'}, 'segmentation': {'tp': 1155, 'fp': 266, 'fn': 346, 'precision': 0.8128, 'rappel': 0.7695, 
… [26426 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nfor c in d['candidats_a_annoter']['priorite_1_attachement']['candidats']:\n    print(json.dumps(c, ensure_ascii=False))\nPY", "description": "Print 10 candidate spans"}`

  ```
{"id": "r267", "type": "GP", "segment": "à moi", "debut": 34, "fin": 39, "phrase": "Le livre qui est sur la table est à moi.", "dans_hard_50": false}
{"id": "r324", "type": "GP", "segment": "sur la table", "debut": 13, "fin": 25, "phrase": "Le livre est sur la table ; il est rouge.", "dans_hard_50": true}
{"id": "r328", "type": "GP", "segment": "on the table", "debut": 12, "fin": 24, "phrase": "The book is on the table; it is red.", "dans_hard_50": true}
{"id": "r336", "type": "GP", "segment": "to her", "debut": 27, "fin": 33, "phrase": "Paul sees Marie; he speaks to her.", "dans_hard_50": false}
{"id": "r342", "type": "GP", "segment": "to her", "debut": 27, "fin": 33, "phrase": "Paul sees Marie; he speaks to her; she listens.", "dans_hard_50": false}
{"id": "r349", "type": "GP", "segment": "sur la table", "debut": 13, "fin": 25, "phrase": "Le livre est sur la table ; je le lis.", "dans_hard_50": true}
{"id": "r358", "type": "GP", "segment": "to her", "debut": 27, "fin": 33, "phrase": "Paul sees Marie; he speaks to her.", "dans_hard_50": false}
{"id": "r363", "type": "GP", "segment": "on the table", "debut": 12, "fin": 24, "phrase": "The book is on the table; I read it.", "dans_har
… [311 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -- reports/rapport-gold-reel-50.md reports/rapport-gold-reel-50.json tools/tests/linguistique/gold_reel_50.py | head -10; echo '---'; git ls-files tools/tests/linguistique/gold_reel_50.py reports/rapport-gold-reel-50.md; echo '---status'; git status --short tools/tests … [110 caractères tronqués]`

  ```
4d6cffc4 PHASE 4 — D1-D3 (LES EXEMPLES DU TAGGER, LA RESTITUTION v2, LA FAQ 10/10) ; L'INDEX, LA FICHE C3 ORPHELINE (GOLD RÉEL 50) ET LE PLAN COMMITTÉS
---
reports/rapport-gold-reel-50.md
---status
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "sed -n '400,470p' tools/tests/linguistique/gold_reel_50.py", "description": "Read main setup of gold_reel_50"}`

  ```
for r in choisies
        ],
    }


# --------------------------------------------------------------------------- sortie


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sortie", default=str(RACINE / "reports" / "rapport-gold-reel-50.json"))
    args = ap.parse_args()

    avant = {str(p): sha256(p) for p in (GOLD, REEL)}
    phrases = charger()
    h = bl.Heuristique()
    rows = [analyser(h, p) for p in phrases]
    for r, p in zip(rows, phrases):
        r["_tokens"] = [m["pos"] for m in p["mots"]]
        r["_segments"] = p["segments"]

    choisies = selectionner(rows)
    if len(choisies) != 50:
        raise SystemExit(f"la sélection doit faire 50 phrases, elle en fait {len(choisies)}")
    hard_ids = {r["id"] for r in choisies}
    reste = [r for r in rows if r["id"] not in hard_ids]

    mesures = {"global_452": metriques(rows), "hard_50": metriques(choisies),
               "reste_402": metriques(reste)}
    for nom, rs in (("hand_20", [r for r in rows if r["source"] == "hand"]),
                    ("reel_432", [r for r in rows if r["source"] == "reel"]),
                    ("fr_242", [r for r in rows if r["langue"] == "
… [1760 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nprint(json.dumps(d['selection']['phrases'][:3], ensure_ascii=False, indent=1))\nprint('--- ids by lang')\nfor lg in ('fr','en'):\n    ids=[p['id'] for p in d['selection']['phrases'] if p['langue']==lg … [83 caractères tronqués]`

  ```
[
 {
  "id": "g017",
  "source": "hand",
  "langue": "en",
  "texte": "She said that she would come yesterday.",
  "score": 4,
  "pos_erreurs": 0,
  "segments_fn": 1,
  "segments_fp": 1,
  "att_erreurs": 1
 },
 {
  "id": "r034",
  "source": "reel",
  "langue": "en",
  "texte": "The book that I read is exciting.",
  "score": 4,
  "pos_erreurs": 2,
  "segments_fn": 0,
  "segments_fp": 0,
  "att_erreurs": 0
 },
 {
  "id": "r071",
  "source": "reel",
  "langue": "en",
  "texte": "The car drives fast.",
  "score": 3,
  "pos_erreurs": 1,
  "segments_fn": 1,
  "segments_fp": 1,
  "att_erreurs": 0
 }
]
--- ids by lang
fr 25 ['g004', 'r091', 'r203', 'r210', 'r225', 'r227', 'r255', 'r260', 'r261', 'r262', 'r266', 'r272', 'r304', 'r309', 'r324', 'r331', 'r339', 'r343', 'r346', 'r347', 'r349', 'r357', 'r408', 'r409', 'r410']
en 25 ['g017', 'r034', 'r071', 'r076', 'r102', 'r104', 'r106', 'r119', 'r159', 'r163', 'r179', 'r217', 'r241', 'r246', 'r285', 'r287', 'r291', 'r293', 'r328', 'r362', 'r363', 'r366', 'r368', 'r370', 'r422']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json, collections, hashlib, time\nsys.path.insert(0, 'tools')\nsys.path.insert(0, 'tools/tests/linguistique')\nimport gold_reel_50 as g\nimport bloc_linguistique as bl\nt=time.time()\nphrases=g.charger(); h=bl.Heuristique()\nrows=[g.analyser(h,p) for p in p … [1531 caractères tronqués]`

  ```
analysed 452 in 0.3 s
baseline match C3 True len 50 diff set()
0 50 match False diff 18 ['g004', 'r071', 'r076', 'r227', 'r272', 'r277', 'r304', 'r314', 'r324', 'r347']
1 50 match False diff 16 ['r071', 'r225', 'r227', 'r287', 'r297', 'r304', 'r335', 'r343', 'r347', 'r374']
2 50 match False diff 18 ['r076', 'r210', 'r227', 'r260', 'r277', 'r287', 'r297', 'r304', 'r343', 'r347']
42 50 match False diff 16 ['g004', 'r071', 'r246', 'r260', 'r262', 'r266', 'r272', 'r297', 'r304', 'r320']
2026 50 match False diff 14 ['r076', 'r225', 'r227', 'r260', 'r262', 'r277', 'r287', 'r297', 'r374', 'r376']
20261116 50 match False diff 14 ['g004', 'r071', 'r210', 'r266', 'r272', 'r304', 'r320', 'r347', 'r374', 'r376']
20261115 50 match False diff 14 ['r076', 'r210', 'r227', 'r266', 'r272', 'r304', 'r320', 'r374', 'r376', 'r379']
20261117 50 match False diff 16 ['r071', 'r076', 'r260', 'r266', 'r272', 'r277', 'r287', 'r297', 'r304', 'r320']
12345 50 match False diff 18 ['g004', 'r071', 'r076', 'r210', 'r227', 'r266', 'r295', 'r304', 'r335', 'r347']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections, hashlib, pathlib\nbase=pathlib.Path('tools/tests/linguistique')\ng=json.load(open(base/'gold.json'))['phrases']\nr=json.load(open(base/'gold_reel.json'))['phrases']\nprint('hand n',len(g),'unique ids',len({p['id'] for p in g}))\nprint('reel n' … [865 caractères tronqués]`

  ```
hand n 20 unique ids 20
reel n 432 unique ids 432
reel id min/max r001 r432
dups []
first [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] last [423, 424, 425, 426, 427, 428, 429, 430, 431, 432]
missing count 0 first []
all source values Counter({None: 20}) Counter({'reel': 432})
gold.json 20009 3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a
gold_reel.json 470149 05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11
concat sha256 cff6b6d703546ad5992c5ada4fc99e1bdaa8e76e9cd089bd3e3b88bd71e90ac5
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib, re\nroot=pathlib.Path('docs')\nfor p in sorted(root.rglob('*.md')):\n    try:\n        txt=p.read_text(encoding='utf-8')\n    except Exception as e:\n        print('ERR',p,e); continue\n    for i,l in enumerate(txt.splitlines(),1):\n        if '200+' in … [105 caractères tronqués]`

  ```
docs/pilotage/chantiers.md:88: | **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter que le résidu ? | ✅ **contrat + bloc v0** : 9 niveaux, **398 langues à 0,9687**, **gold 432 réels + 160 synthétiques** (POS 0,7544 à 320 phrase
docs/pilotage/chantiers.md:90: | **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **po
docs/pilotage/chantiers.md:181: | 5 | **gold 200+** et **porte B13** | B13 | la pragmatique neuronale est mesurée (négatif) ; la cascade et la politique LLM sont livrées |
docs/pilotage/en-cours.md:67: - **Prochaine action** : **qualité des rôles** ; T132/T133, gold 200+.
docs/pilotage/en-cours.md:69: - **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**.
docs/pilotage/en-cours.md:131: **N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+, **qualité des rôles** ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — migration `/` v7 (106/41) ; référents ; **R0.7** — split réel ; *
docs/pilotage
… [2554 caractères tronqués]
  ```

- **bash** `{"command": "date -Iseconds; git rev-parse HEAD; git log -1 --format='%h %ad %s' --date=iso", "description": "Check current date and HEAD"}`

  ```
2026-11-15T08:59:00-05:00
6b2208ee1579739a188086f957c0d508e8a04726
6b2208ee 2026-11-15 08:08:51 -0500 PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE, RESTITUTION v3, LE TAGGER PAR DÉFAUT ? ; LA FILE DU CHANTIER À 41 TÂCHES
  ```

- **bash** `{"command": "sed -n '1,80p' docs/methode/resultats.md; echo '===='; sed -n '1,80p' docs/methode/rangement.md", "description": "Read result/report conventions"}`

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
… [7710 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfor f in ['docs/pilotage/chantiers.md','docs/pilotage/en-cours.md','docs/pilotage/plan-travail.md','docs/pilotage/roadmap.md','docs/pilotage/semaine-2.md','docs/pilotage/semaine-autonome.md','docs/produit/README.md']:\n    txt=pathlib.Path(f).read_text( … [334 caractères tronqués]`

  ```
==================== docs/pilotage/chantiers.md
L88: ...**sans `par` : chunker 3/3, S ignore** ; **cible par proximité : exact ×13** ; **candidats verbes : top-k 0,4686** ; **échecs : 94 spans (48 REL/33 SUB/13 GP), 8 cibles** | **gold 200+** ; **porte B13** (183/183) ; la cascade mesurée | D (corpus), S (banque), N2 (entraînement) | R (prétraitement), B...
L90: ...ité : exact ×13** ; **candidats verbes : top-k 0,4686** ; **échecs : 94 spans (48 REL/33 SUB/13 GP), 8 cibles** (négation/modalité sous l'heuristique, la fusion la garde) ; **gold 200+** ; **porte 183/183** | L (états), R (documents), N (opérateurs) | B, R, L |...
L181: ...| 5 | **gold 200+** et **porte B13** | B13 | la pragmatique neuronale est mesurée (négatif) ; la cascade et la politique LLM sont liv...

==================== docs/pilotage/en-cours.md
L67: ...- **Prochaine action** : **qualité des rôles** ; T132/T133, gold 200+....
L69: ...- **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**....
L131: ...**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+, **qualité des rôles** ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — migration `/` v...

========
… [2498 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '145,168p' docs/pilotage/roadmap.md; echo '==== produit'; sed -n '525,545p' docs/produit/README.md; echo '==== chantiers 175-185'; sed -n '175,185p' docs/pilotage/chantiers.md", "description": "Read contexts for roadmap/product/chantiers"}`

  ```
(table **14/14**, corpus **418/438**, retrieval, généalogie **154/154**, familles **0,619 vs
0,0445**, §334, CIC **42/42**), portes (**183/183**, passe **81/84**). La **base 612/602** est
re-mesurée au HEAD `b20a4c31` : **0,7902 / 0,7882** (F1), **238/239 / 234/239** (attachement).
[`tableau`](../../reports/rapport-tableau-mesures.md) + [`JSON`](../../reports/tableau-mesures.json).

**J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag `chantier-2026-11-14`.** La
passe du **14/11 00 h 30** (`work/portes/passe-1311-23h15.log`) n'est **pas refaite** : les trois
rouges sont **revérifiées**. `porte-sessions` passe **verte** après la mise en pause du hub
`1e7ef596` et le rafraîchissement du heartbeat `e181ce02` ; `porte-indice` et `porte-melange`
restent **rouges structurelles** (mêmes causes : écart au témoin nul pour l'indice ; état de A qui
ne rend pas son code pour le mélange). Le tag annoté `chantier-2026-11-14` est posé sur le dernier
commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +
[`JSON`](../../reports/rapport-cloture-chantier.json)
… [3227 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '55,75p' docs/pilotage/en-cours.md; echo '==== 125-135'; sed -n '125,135p' docs/pilotage/en-cours.md", "description": "Read en-cours contexts"}`

  ```
### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)*

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13.
- **Stratégie** : v0 mesuré.
- **Ambition** : un runtime cognitif tracé.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)) ; **D2** ([v2](../../reports/rapport-restitution-v2.md)) ; **D3** ([FAQ](../../reports/rapport-faq.md), 10/10) ; **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; **E2** ([cas d'erreur](../../reports/rapport-tagger-erreurs.md)).
- **Ce que font les autres** : **N2**, **S**, **
… [1267 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr={p['id']:p for p in json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']}\nids=['r267','r324','r328','r336','r342','r349','r358','r363','r367','r429']\nfor i in ids:\n    p=r[i]\n    print('='*10,i,p['langue'],p['texte'])\n    print('mot … [283 caractères tronqués]`

  ```
========== r267 fr Le livre qui est sur la table est à moi.
mots: [('Le', 0, 2, 'DET'), ('livre', 3, 8, 'NOUN'), ('qui', 9, 12, 'PRON'), ('est', 13, 16, 'VERB'), ('sur', 17, 20, 'PREP'), ('la', 21, 23, 'DET'), ('table', 24, 29, 'NOUN'), ('est', 30, 33, 'AUX'), ('à', 34, 35, 'PREP'), ('moi', 36, 39, 'PRON')]
 seg GN 'Le livre' 0 8 cible None cibles None
 seg REL 'qui est sur la table' 9 29 cible livre cibles ['livre']
 seg GV 'est' 30 33 cible None cibles None
 seg GP 'à moi' 34 39 cible None cibles None
========== r324 fr Le livre est sur la table ; il est rouge.
mots: [('Le', 0, 2, 'DET'), ('livre', 3, 8, 'NOUN'), ('est', 9, 12, 'VERB'), ('sur', 13, 16, 'PREP'), ('la', 17, 19, 'DET'), ('table', 20, 25, 'NOUN'), ('il', 28, 30, 'PRON'), ('est', 31, 34, 'AUX'), ('rouge', 35, 40, 'ADJ')]
 seg GN 'Le livre' 0 8 cible None cibles None
 seg GV 'est' 9 12 cible None cibles None
 seg GP 'sur la table' 13 25 cible None cibles None
 seg GN 'il' 28 30 cible None cibles None
 seg GV 'est' 31 34 cible None cibles None
 seg ADJ 'rouge' 35 40 cible None cibles None
========== r328 en The book is on the table; it is red.
mots: [('The', 0, 3, 'DET'), ('book', 4, 8, 'NOUN'), ('is', 9, 11, 'VERB'), (
… [3954 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nG=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nR=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nph=[dict(p, _source='hand', _fichier='gold.json') for p in G]+[dict(p, _source='corpus', _fichier='gol … [898 caractères tronqués]`

  ```
hand fr {'phrases': 14, 'tokens': 74, 'segments': 40, 'cibles': 10, 'seg_types': {'GN': 16, 'GV': 14, 'GP': 8, 'SUB': 1, 'REL': 1}, 'target_types': {'GP': 8, 'SUB': 1, 'REL': 1}}
hand en {'phrases': 6, 'tokens': 31, 'segments': 16, 'cibles': 3, 'seg_types': {'GN': 7, 'GV': 6, 'GP': 2, 'SUB': 1}, 'target_types': {'GP': 2, 'SUB': 1}}
hand TOTAL {'phrases': 20, 'tokens': 105, 'segments': 56, 'cibles': 13, 'seg_types': {'GN': 23, 'GV': 20, 'GP': 10, 'SUB': 2, 'REL': 1}, 'target_types': {'GP': 10, 'SUB': 2, 'REL': 1}}
corpus fr {'phrases': 228, 'tokens': 1258, 'segments': 759, 'cibles': 86, 'seg_types': {'GN': 344, 'GV': 279, 'GP': 33, 'REL': 29, 'SUB': 28, 'ADJ': 17, 'ADV': 22, 'PONCT': 7}, 'target_types': {'GP': 30, 'REL': 29, 'SUB': 27}}
corpus en {'phrases': 204, 'tokens': 1117, 'segments': 686, 'cibles': 85, 'seg_types': {'GN': 314, 'GV': 253, 'GP': 38, 'REL': 28, 'SUB': 25, 'ADJ': 18, 'ADV': 8, 'PONCT': 2}, 'target_types': {'GP': 32, 'REL': 28, 'SUB': 25}}
corpus TOTAL {'phrases': 432, 'tokens': 2375, 'segments': 1445, 'cibles': 171, 'seg_types': {'GN': 658, 'GV': 532, 'GP': 71, 'REL': 57, 'SUB': 53, 'ADJ': 35, 'ADV': 30, 'PONCT': 9}, 'target_types': {'GP': 62, 'REL': 57, 'SUB': 5
… [241 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json, collections, hashlib, random, pathlib\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport gold_reel_50 as g\nimport bloc_linguistique as bl\n\nG=pathlib.Path('tools/tests/linguistique/gold.json'); R=pathlib.Path('tools/t … [2292 caractères tronqués]`

  ```
H50 match C3: True n 50 50
H50 ids: ['g004', 'g017', 'r034', 'r071', 'r076', 'r091', 'r102', 'r104', 'r106', 'r119', 'r159', 'r163', 'r179', 'r203', 'r210', 'r217', 'r225', 'r227', 'r241', 'r246', 'r255', 'r260', 'r261', 'r262', 'r266', 'r272', 'r285', 'r287', 'r291', 'r293', 'r304', 'r309', 'r324', 'r328', 'r331', 'r339', 'r343', 'r346', 'r347', 'r349', 'r357', 'r362', 'r363', 'r366', 'r368', 'r370', 'r408', 'r409', 'r410', 'r422']
H50 scores match C3: True
manifest 1615c17a97bb998451de66585dadcea0643ba1d7f8d962ccbdf28a13b575d970
H50 {"phrases": 50, "sources": {"hand": 2, "reel": 48}, "langues": {"en": 25, "fr": 25}, "source_langue": {"hand/fr": 1, "hand/en": 1, "reel/fr": 24, "reel/en": 24}, "tokens": 323, "segments": 190, "cibles": 22}
  mesure {"phrases": 50, "tokens": 323, "pos": {"exactitude": 0.6842, "ferme": 0.7542, "ouvert": 0.5972, "justes": 221, "erreurs": 102, "tokenisation": 31, "etiquette_exactitude": 0.7568, "note": "`exactitude` compte la tokenisation ; `etiquette_exactitude` retire les tokens gold sans token prédit (« ? »)."}, "segmentation": {"tp": 103, "fp": 60, "fn": 87, "precision": 0.6319, "rappel": 0.5421, "f1": 0.5836}, "attachement": {"cibles": 22, "justes"
… [2034 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib, json, collections\nfiles=['docs/pilotage/chantiers.md','docs/pilotage/en-cours.md','docs/pilotage/plan-travail.md','docs/pilotage/roadmap.md','docs/pilotage/semaine-2.md','docs/pilotage/semaine-autonome.md','docs/produit/README.md']\nout={}\nfor f in fi … [626 caractères tronqués]`

  ```
{
 "docs/pilotage/chantiers.md": {
  "gold_200_plus": 3,
  "lignes": [
   {
    "ligne": 88,
    "contexte": "es : top-k 0,4686** ; **échecs : 94 spans (48 REL/33 SUB/13 GP), 8 cibles** | **gold 200+** ; **porte B13** (183/183) ; la cascade mesurée | D (corpus), S (banque), N2 (entraînement) | R (prétraitemen"
   },
   {
    "ligne": 90,
    "contexte": " GP), 8 cibles** (négation/modalité sous l'heuristique, la fusion la garde) ; **gold 200+** ; **porte 183/183** | L (états), R (documents), N (opérateurs) | B, R, L |"
   },
   {
    "ligne": 181,
    "contexte": "| 5 | **gold 200+** et **porte B13** | B13 | la pragmatique neuronale est mesurée (négatif) ; la cascade et la politique LLM son"
   }
  ],
  "toutes_200_plus": 3
 },
 "docs/pilotage/en-cours.md": {
  "gold_200_plus": 3,
  "lignes": [
   {
    "ligne": 67,
    "contexte": "- **Prochaine action** : **qualité des rôles** ; T132/T133, gold 200+."
   },
   {
    "ligne": 69,
    "contexte": "- **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**."
   },
   {
    "ligne": 131,
    "contexte": "**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+, **qualité des rôles** ; **J3.2** — V14 des 21 l
… [2657 caractères tronqués]
  ```

- **bash** `{"command": "git check-ignore -v reports/rapport-gold-reel-50.json reports/rapport-gold-452.json 2>/dev/null || true; echo '---'; cat .gitignore", "description": "Check gitignore for report JSON"}`

  ```
---
__pycache__/
*.pyc
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
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md", "offset": 86, "limit": 8}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 64, "limit": 8}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 533, "limit": 8}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md</path>
<type>file</type>
<content>
86: | **R — le lecteur** | un document, une question, un budget : réponse sourcée ou refus motivé ? | ✅ R0.1–R0.3 ; R0.4/R0.5 négatifs ; R4.1–R4.4 mesurés (R4.4 : 4/5 familles ≥ 90 %) | **R1.1/R1.2** (contexte natif) ; R2/R3 attendent N ; R5 attend B10.3 | R03 (banc), N, B10.3, D (docs) | la preuve d'usage pour tous |
87: | **S — les structures** | quelles structures d'interprétation candidates, et lesquelles un humain valide ? | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests**, gold **60**, corpus **60**, banque **84/67**, page **`/paragraphes`** ; **h050/h053** et le fait divers **fermés** | **poursuivre la validation sur `/paragraphes`** (a001–a003 faits) ; rétro-traduction API | L (annotations), D (corpus), B (sens) | L (banque), B (pragmatique), D (corpus) |
88: | **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter que le résidu ? | ✅ **contrat + bloc v0** : 9 niveaux, **398 langues à 0,9687**, **gold 432 réels + 160 synthétiques** (POS 0,7544 à 320 phrases, réel 0,7657, exact 0,194, tête 0,510), **attachement
… [3757 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
64: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)) ; **D2** ([v2](../../reports/rapport-restitution-v2.md)) ; **D3** ([FAQ](../../reports/rapport-faq.md), 10/10) ; **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; **E2** ([cas d'erreur](../../reports/rapport-tagger-erreurs.md)).
65: - **Ce que font les autres** : **N2**, **S**, **hub**.
66: - **Ce qu'elle fait** : chantier.
67: - **Prochaine action** : **qualité des rôles** ; T132/T133, gold 200+.
68: - **Clôture** : **J14.1 faite** (84/81/3 ; `sessions` verte, `indice` et `melange` structurelles ; tag `chantier-2026-11-14`).
69: - **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**.
70: - **Journal
… [154 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
533: sémantique est un **compteur d'unités**, pas une représentation.
534: 
535: **8. Pas de classement appris ni de gold 200+.** L'attachement est une **heuristique de
536: proximité** avec candidats ; il n'y a pas de modèle de classement. Le gold fait 612 phrases, dont
537: 160 synthétiques ; le gold 200+ réel reste à faire.
538: 
539: **9. Pas de calibration des confiances.** `confiance` est **déclarée** (0,3 pour un NOUN ouvert,
540: 0,92 pour un DET), pas mesurée comme une probabilité. Elle sert à trier, pas à seuiller une

(Showing lines 533-540 of 829. Use offset=541 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md", "limit": 3, "offset": 38}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md", "limit": 3, "offset": 194}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md", "limit": 3, "offset": 337}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md", "limit": 3, "offset": 365}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 2, "offset": 30}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 3, "offset": 159}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 2, "offset": 287}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "limit": 3, "offset": 25}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "limit": 3, "offset": 47}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "limit": 3, "offset": 111}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md</path>
<type>file</type>
<content>
38: | **N2 — le natif (session `0733c5bb`)** | entraîner et évaluer le modèle natif sur les corpus D, mesurer longueur, capacité, diversité | N2, N4, le mètre honnête | **GPU** (1 des 2), 8–16 cœurs | **N2.ac** (1 Go, 60 k pas) : **3,49 / 6,03** — production ; **200 k pas** : val_fr **3,16**, littérature **5,61**, anglais **7,28**, wikitext2 **8,00** (**< 2,5 non atteinte**) ; **R1.1/R1.2 mesurées** ; **2 048 fini** (2×10 000 pas) ; prochaine : la **porte propre (0,29)**. |
39: | **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **166/166** (6 S fixés ; T132/T133 2/5), gold **432**, 116 liens ; **gold neuronal** (POS **0,9415** / syntagmes **0,7539** / acte **1,0**) ; **DRVM/native** règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusion par sous-type : le double sens 0,9884 (+0,0208) ; variance du sous-type : 0,9838 ; tirages : 0,9838 ×3 (détermi
… [1058 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "limit": 3, "offset": 280}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md</path>
<type>file</type>
<content>
194: 3. **L/B13 — la langue et la pensée (CPU).** **Session `e181ce02` ouverte.** **166/166** (6 S fixés ; T132/T133 2/5), gold **432**, 116 liens ; **gold neuronal** qualifié (POS **0,9415**, syntagmes
195:    **0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusion par sous-type : le double sens 0,9884 (+0,0208) ; variance du sous-type : 0,9838 ; tirages : 0,9838 ×3 (déterministe sur ces invites) ; attachement : top1 0,3431, exact 0,0042 ; cibles : 1863 segments, 1624 sans cible (87,2 %), couverture réelle 0,1283 ; cibles 500 : 294 GN / 206 GV ; relation GN → GV : 221/637 ; rôles par position : 301/322, relation 0,8195 (522/637) surévaluée ; correctif `par` → agent (partiel : le générateur S garde `moyen`) ; sans `par` : le chunker 3/3, le générateur S ignore ; cible par proximité : exact 0,0042 → 0,0544 ; candidats verbes : top-k 0,4686, tête 0,7655 ; échecs qualifiés : 127 = 94 span + 33 cible** (négation/modalité sous l'
… [228 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md</path>
<type>file</type>
<content>
337: | S `29ad180d` | `cpu1` 4, `ram` 8 | homographes/lexique, h033, gold |
338: | Pensée `e181ce02` | `cpu1` 4, `ram` 16 | gold 200+, porte mobile |
339: | D/R/A `fe3c05f0` | close | place `cpu1` 2 libre si on la rouvre |

(Showing lines 337-339 of 456. Use offset=340 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md</path>
<type>file</type>
<content>
365: | **S** `29ad180d` | `tools/structures/`, `docs/schemas/arbre-referents.svg`, `reports/s-*` | **v6** (h050, h053, « si fort que » fermés, gold 60) ; la **validation des paragraphes** sur `/paragraphes` ; la **rétro-traduction** API | `cpu1` 4, `ram` 8 | fiches + tests verts + commit | validation faite ou report nommé |
366: | **L/B13** `e181ce02` | `tools/pensee/`, `reports/pensee-*`, `docs/theorie/pensee-*` | **porte stochastique/fenêtre** (test faible), **gold 200+**, **T132/T133** ; professeurs par l'**API** | `cpu1` 4, `ram` 16 | fiches + commit | porte franchie ou négatif nommé |
367: | **hub** `536cd5d6` | `docs/pilotage/`, `journal/` (hors sessions), `reports/README.md`, `reports/INDEX.md`, ``tools/sessions.py`, `tools/ressources.py`, `tools/index_reports.py`, `tools/surveille_sessions.py`` | tenir l'**état** (un écrivain à la fois), intégrer chaque fait, surveiller heartbeats et claims ; **passe complète** quand les GPU sont libres ; **bilan 08 h** | `cpu1` 1, `ram` 1 | état/roadmap/journal à jour ; verdict de passe | bilan de 08 h écrit et committé |

… [71 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
30: | **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
31: | **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise*
… [1464 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
159: **Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le
160: gold 200+ ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).
161: 

(Showing lines 159-161 of 492. Use offset=162 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
287: | **B12** | les modules cerveau-langage M1–M9 | ⚠️ / ❌ | **B12.10 close** (négatif : [oracle](../theorie/glossaire/entrees/oracle.md) = M8, M4 seul = 0) ; seul M1 est solide |
288: | **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **porte** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **professeur** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + **votante** + **trois looks** + **bayésien** + **bayésien 2** + **vraisemblance** + **dérive** + **adaptative** + **glisse** + **ru
… [1206 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md</path>
<type>file</type>
<content>
25: |---|---|---|---|
26: | **gold réel** | **452** phrases (402 + H50), 184 cibles ; le nom « 200+ » est **obsolète** | H50 n'est pas encore un **test** ; **10 GP/SUB** à annoter (dont 4 dans H50) ; le dénominateur passe à **194** | [C3](../../reports/rapport-gold-reel-50.md) |
27: | **page `/` de S** | **369** candidats stockés, **0** profondeur ; la v7 donne **359** dont **99 à ≥3** ; **56** tests | décider garder/régénérer ; **106 conservés**, **41 à re-juger** ; référents **9/16** faux | [C2](../../reports/rapport-coordination-s-v2.md) |

(Showing lines 25-27 of 113. Use offset=28 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md</path>
<type>file</type>
<content>
47: |---|---|---|---|---|---|
48: | **J1 · 16/11** | matin | **Le gold réel 452, nommé et tenu à l'écart** : retirer « gold 200+ » ; figer le split **402 / H50** ; annoter les **10 GP/SUB** (4 dans H50) ; sha256 du gold avant/après. | S + pilote | fiche gold 452 + JSON ; 402 vs H50 ; **184 → 194** cibles ; double codage **4/10**. | C3 ; le gold est à S |
49: | | après-midi | **La page `/` de S, décidée** : garder l'ancien banc ou régénérer ; si régénération, signature + **106 conservés** + **41 en quarantaine** ; mesurer `/` (369/0) contre la v7 (359/99). | S (écrit) + pilote (mesure) | fiche de décision + JSON ; la liste des 41 ; **0** écriture du pilote dans `tools/structures/`. | C2 ; S doit trancher |

(Showing lines 47-49 of 113. Use offset=50 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md</path>
<type>file</type>
<content>
111:   reste le chemin sûr tant que la décision n'est pas mesurée.
112: - **Pas de « gold 200+ »** : le libellé disparaît au profit de **gold réel 452**, **lot dur H50**
113:   et **cibles 184 → 194**.

(End of file - total 113 lines)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md</path>
<type>file</type>
<content>
280: | C2 **S** | ✅ | la page `/` **ne sert pas la v7** ; les 11 verdicts committés (`389b99f`) |
281: | C3 **R** | ✅ | le « gold 200+ » **défini** (452 phrases), 50 ratées sélectionnées |
282: | B1 **Panini** | ✅ | le protocole à **date contrôlée** (60 paires, 3 strates) — le §334 ne fournit qu'**une** paire contemporaine |

(Showing lines 280-282 of 288. Use offset=283 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md", "old_string": "| **gold 200+** ; **porte B13** (183/183) ; la cascade mesurée |", "new_string": "| **gold réel 452** ; **porte B13** (183/183) ; la cascade mesurée |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md", "old_string": "(négation/modalité sous l'heuristique, la fusion la garde) ; **gold 200+** ; **porte 183/183** |", "new_string": "(négation/modalité sous l'heuristique, la fusion la garde) ; **gold de pensée ( … [30 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md", "old_string": "| 5 | **gold 200+** et **porte B13** | B13 |", "new_string": "| 5 | **gold de pensée (B13)** et **porte B13** | B13 |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Prochaine action** : **qualité des rôles** ; T132/T133, gold 200+.", "new_string": "- **Prochaine action** : **qualité des rôles** ; T132/T133, gold de pensée."}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**.", "new_string": "- **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**."}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "T132/T133, gold 200+, **qualité des rôles**", "new_string": "T132/T133, gold de pensée, **qualité des rôles**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md", "old_string": "Prochaine : **T132/T133**, **gold 200+**. |", "new_string": "Prochaine : **T132/T133**, **gold de pensée**. |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md", "old_string": "Prochaine action : **T132/T133**, **gold 200+**.", "new_string": "Prochaine action : **T132/T133**, **gold de pensée**."}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md", "old_string": "| Pensée `e181ce02` | `cpu1` 4, `ram` 16 | gold 200+, porte mobile |", "new_string": "| Pensée `e181ce02` | `cpu1` 4, `ram` 16 | gold de pensée, porte mobile |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md", "old_string": "**porte stochastique/fenêtre** (test faible), **gold 200+**, **T132/T133**", "new_string": "**porte stochastique/fenêtre** (test faible), **gold de pensée**, **T132/T133**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "**T132/T133** ; **gold 200+** ; **porte 183/183**", "new_string": "**T132/T133** ; **gold de pensée** ; **porte 183/183**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "T132/T133 et le\ngold 200+ ; **E2**", "new_string": "T132/T133 et le\ngold de pensée ; **E2**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "+ 8 cibles** ; **gold 200+** ; **porte 183/183**", "new_string": "+ 8 cibles** ; **gold de pensée** ; **porte 183/183**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "old_string": "le nom « 200+ » est **obsolète**", "new_string": "l'ancien nom est **obsolète**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "old_string": "retirer « gold 200+ » ; figer le split", "new_string": "retirer l'ancien nom ; figer le split"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "old_string": "- **Pas de « gold 200+ »** : le libellé disparaît au profit de **gold réel 452**, **lot dur H50**", "new_string": "- **L'ancien libellé est retiré** : il disparaît au profit de **gold réel 452* … [20 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "old_string": "le « gold 200+ » **défini** (452 phrases)", "new_string": "le gold réel 452 **défini** (452 phrases)"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "**8. Pas de classement appris ni de gold 200+.** L'attachement est une **heuristique de\nproximité** avec candidats ; il n'y a pas de modèle de classement. Le gold fait 612 phrases, dont\n160 synth … [384 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nhits=[]\nfor p in pathlib.Path('docs').rglob('*.md'):\n    txt=p.read_text(encoding='utf-8',errors='replace')\n    for i,l in enumerate(txt.splitlines(),1):\n        if '200+' in l:\n            hits.append((str(p),i,l[:200]))\nprint('hits',len(hits))\n … [78 caractères tronqués]`

  ```
hits 0
  ```

- **bash** `{"command": "git diff --stat; echo '---'; git diff -- docs/pilotage/chantiers.md docs/pilotage/en-cours.md docs/pilotage/plan-travail.md docs/pilotage/roadmap.md docs/pilotage/semaine-2.md docs/pilotage/semaine-autonome.md docs/produit/README.md | sed -n '1,220p'", "description": "Review doc diff"}`

  ```
docs/pilotage/chantiers.md                         |   6 +-
 docs/pilotage/en-cours.md                          |   6 +-
 docs/pilotage/plan-travail.md                      |   8 +-
 docs/pilotage/roadmap.md                           |   6 +-
 docs/pilotage/semaine-2.md                         |   6 +-
 docs/pilotage/semaine-autonome.md                  |   2 +-
 docs/produit/README.md                             |   5 +-
 journal/README.md                                  |   2 +-
 journal/sessions/MANIFEST.md                       |   2 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  65 ++
 .../rapport.md                                     |  48 +-
 reports/pensee-coherence-fiches-v7.json            |  19 +
 reports/pensee-dev-test-v10.json                   |   2 +-
 reports/pensee-quatre-modes.json                   | 734 ++++++++++++---------
 reports/rapport-audit-v7.md                        |   6 +-
 reports/rapport-coherence-fiches-v7.md             |  17 +-
 reports/rapport-dev-test-v10.md                    |   2 +-
 reports/rapport-pensee-v12.md                      |   4 +-
 reports/rapport-spans-chunker.md                   |  13 +-
 tools/chantier/plan.jso
… [45758 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/gen_w1.py <<'PY'\nfrom __future__ import annotations\nimport sys, json, collections, hashlib, random, pathlib, datetime\nsys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/tests/linguistique')\nimport gold_reel_50 as g\nimport bloc_linguistique as bl\n\nROOT = pathlib.Pat … [18591 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/gen_w1.py", line 67, in <module>
    rows = [g.analyser(h, p) for p in phrases]
            ~~~~~~~~~~^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", line 149, in analyser
    "id": p["id"], "source": p["source"], "langue": p.get("langue") or "fr",
                             ~^^^^^^^^^^
KeyError: 'source'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/gen_w1.py'\ns=open(p).read()\ns=s.replace(\"phrases = [dict(p, _source='hand', _fichier='gold.json') for p in G] + \\\\\\n          [dict(p, _source='corpus', _fichier='gold_reel.json') for p in R]\",\n\"phrases = [dict(p, source='hand', _source='hand', _fichie … [1142 caractères tronqués]`

  ```
patched
JSON écrit: reports/rapport-gold-452.json 43771 octets
H50 50 reste 402 manifeste 1615c17a97bb998451de66585dadcea0643ba1d7f8d962ccbdf28a13b575d970
métriques {'phrases': 452, 'tokens': 2480, 'pos_exactitude': 0.8891, 'pos_etiquette_exactitude': 0.9134, 'pos_justes': 2205, 'pos_erreurs': 275, 'pos_tokenisation': 66, 'f1': 0.7906, 'seg_tp': 1155, 'seg_fp': 266, 'seg_fn': 346, 'attachement_exactitude': 0.9946, 'attachement_cibles': 184, 'attachement_justes': 183, 'attachement_erreurs': 1} {'phrases': 50, 'tokens': 323, 'pos_exactitude': 0.6842, 'pos_etiquette_exactitude': 0.7568, 'pos_justes': 221, 'pos_erreurs': 102, 'pos_tokenisation': 31, 'f1': 0.5836, 'seg_tp': 103, 'seg_fp': 60, 'seg_fn': 87, 'attachement_exactitude': 0.9545, 'attachement_cibles': 22, 'attachement_justes': 21, 'attachement_erreurs': 1} {'phrases': 402, 'tokens': 2157, 'pos_exactitude': 0.9198, 'pos_etiquette_exactitude': 0.935, 'pos_justes': 1984, 'pos_erreurs': 173, 'pos_tokenisation': 35, 'f1': 0.819, 'seg_tp': 1052, 'seg_fp': 206, 'seg_fn': 259, 'attachement_exactitude': 1.0, 'attachement_cibles': 162, 'attachement_justes': 162, 'attachement_erreurs': 0} {'phrases': 50, 'tokens': 278, 'pos_exactitude': 
… [271 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-452.json'))\nprint('keys',list(d))\nprint('\\nCOMPOSITION')\nfor k,v in d['composition']['par_source_et_langue'].items():\n    print(k,v)\nprint('total',d['composition']['total'])\nprint('\\nSPLIT')\nfor k in ('h50_id … [486 caractères tronqués]`

  ```
keys ['date', 'date_cible', 'ligne', 'tache', 'commit_mesure', 'commit_c3', 'objet', 'composition', 'sha256', 'split', 'candidats_a_annoter', 'retrait_gold_200_plus', 'controles_negatifs', 'gold_intact', 'limites', 'ce_qui_ferait_faux', 'fichiers']

COMPOSITION
hand/fr {'phrases': 14, 'tokens': 74, 'segments': 40, 'cibles': 10, 'segments_par_type': {'GN': 16, 'GV': 14, 'GP': 8, 'REL': 1, 'SUB': 1, 'ADJ': 0, 'ADV': 0, 'PONCT': 0}, 'cibles_par_type': {'GP': 8, 'REL': 1, 'SUB': 1}}
hand/en {'phrases': 6, 'tokens': 31, 'segments': 16, 'cibles': 3, 'segments_par_type': {'GN': 7, 'GV': 6, 'GP': 2, 'REL': 0, 'SUB': 1, 'ADJ': 0, 'ADV': 0, 'PONCT': 0}, 'cibles_par_type': {'GP': 2, 'REL': 0, 'SUB': 1}}
corpus/fr {'phrases': 228, 'tokens': 1258, 'segments': 759, 'cibles': 86, 'segments_par_type': {'GN': 344, 'GV': 279, 'GP': 33, 'REL': 29, 'SUB': 28, 'ADJ': 17, 'ADV': 22, 'PONCT': 7}, 'cibles_par_type': {'GP': 30, 'REL': 29, 'SUB': 27}}
corpus/en {'phrases': 204, 'tokens': 1117, 'segments': 686, 'cibles': 85, 'segments_par_type': {'GN': 314, 'GV': 253, 'GP': 38, 'REL': 28, 'SUB': 25, 'ADJ': 18, 'ADV': 8, 'PONCT': 2}, 'cibles_par_type': {'GP': 32, 'REL': 28, 'SUB': 25}}
total {'phrases': 452, 
… [4040 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-452.json'))\nprint(json.dumps(d['split']['part_des_erreurs'],ensure_ascii=False,indent=1))\nprint(json.dumps(d['controles_negatifs'],ensure_ascii=False,indent=1))\nprint(json.dumps(d['retrait_gold_200_plus'],ensure_as … [79 caractères tronqués]`

  ```
{
 "pos": {
  "lot": 102,
  "total": 275,
  "part": 0.3709
 },
 "fn": {
  "lot": 87,
  "total": 346,
  "part": 0.2514
 },
 "att": {
  "lot": 1,
  "total": 1,
  "part": 1.0
 }
}
{
 "partition": "H50 ∩ 402 = 0 ; H50 ∪ 402 = 452 ; aucun id dupliqué.",
 "reproduction": "recalcul au HEAD 6b2208ee : 50/50 ids identiques à C3 ; 50/50 scores identiques ; Jaccard 1,0.",
 "hash": "sha256 avant = après ; git diff des deux gold vide.",
 "tirage_aleatoire": "graine 20261116 : POS 88,13 %, F1 78,69 %, attachement 100 % ; H50 : 68,42 %, 58,36 %, 95,45 %.",
 "candidats": "10 segments GP/SUB sans cible = 184 - 174 ? non : 10 spans, 0 cible ; 4 dans H50, 6 dans 402.",
 "docs": "aucun « 200+ » restant dans docs/ (0 ligne)."
}
{
 "fait": true,
 "occurrences_avant": 18,
 "lignes_avant": 19,
 "occurrences_apres": 0,
 "fichiers": [
  {
   "fichier": "docs/pilotage/chantiers.md",
   "avant": 3,
   "apres": 0,
   "remplacement": "gold réel 452 (L) ; gold de pensée (B13)"
  },
  {
   "fichier": "docs/pilotage/en-cours.md",
   "avant": 3,
   "apres": 0,
   "remplacement": "gold de pensée (B13)"
  },
  {
   "fichier": "docs/pilotage/plan-travail.md",
   "avant": 4,
   "apres": 0,
   "remplacement": "gold de p
… [804 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/gen_w1.py'\ns=open(p).read()\ns=s.replace('''            'score': \"3 × |cibles d'attachement absentes ou fausses| + 2 × |tokens POS faux| + 1 × |segments gold absents|\",''',\n'''            'score': \"3 × |cibles d'attachement évaluées absentes ou fausses (le … [999 caractères tronqués]`

  ```
patched
JSON écrit: reports/rapport-gold-452.json 43968 octets
H50 50 reste 402 manifeste 1615c17a97bb998451de66585dadcea0643ba1d7f8d962ccbdf28a13b575d970
métriques {'phrases': 452, 'tokens': 2480, 'pos_exactitude': 0.8891, 'pos_etiquette_exactitude': 0.9134, 'pos_justes': 2205, 'pos_erreurs': 275, 'pos_tokenisation': 66, 'f1': 0.7906, 'seg_tp': 1155, 'seg_fp': 266, 'seg_fn': 346, 'attachement_exactitude': 0.9946, 'attachement_cibles': 184, 'attachement_justes': 183, 'attachement_erreurs': 1} {'phrases': 50, 'tokens': 323, 'pos_exactitude': 0.6842, 'pos_etiquette_exactitude': 0.7568, 'pos_justes': 221, 'pos_erreurs': 102, 'pos_tokenisation': 31, 'f1': 0.5836, 'seg_tp': 103, 'seg_fp': 60, 'seg_fn': 87, 'attachement_exactitude': 0.9545, 'attachement_cibles': 22, 'attachement_justes': 21, 'attachement_erreurs': 1} {'phrases': 402, 'tokens': 2157, 'pos_exactitude': 0.9198, 'pos_etiquette_exactitude': 0.935, 'pos_justes': 1984, 'pos_erreurs': 173, 'pos_tokenisation': 35, 'f1': 0.819, 'seg_tp': 1052, 'seg_fp': 206, 'seg_fn': 259, 'attachement_exactitude': 1.0, 'attachement_cibles': 162, 'attachement_justes': 162, 'attachement_erreurs': 0} {'phrases': 50, 'tokens': 278, 'pos_exactitude': 
… [271 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/gen_w1_md.py <<'PY'\nfrom __future__ import annotations\nimport json, pathlib\n\nD = json.load(open('reports/rapport-gold-452.json', encoding='utf-8'))\nC = D['composition']\nS = D['split']\nCAND = D['candidats_a_annoter']['priorite_1']\nSHA = D['sha256']\n\ndef pct(x):\n     … [18280 caractères tronqués]`

  ```
MD écrit 20384 octets 240 lignes
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md", "limit": 260}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md</path>
<type>file</type>
<content>
1: # W1 — le gold réel 452 : composition, split 402 / H50, sha256 et 10 candidats GP/SUB
2: 
3: > **Ligne de roadmap** : **R0.7** (bloc linguistique) / **B13** · **Tâche** : W1 (semaine 2, J1 matin, la part du pilote) ·
4: > **Date** : 2026-11-15 (J1 · 16/11) · **HEAD mesuré** : `6b2208ee` · **Verdict** : ✅ **le gold réel 452 est
5: > nommé et composé ; le split 402/H50 est figé ; le gold est intact ; les 10 GP/SUB sont listés pour S.**
6: 
7: **En trois lignes.** (1) Le gold réel fait **452** phrases = **20 hand** (`gold.json`) + **432 corpus**
8: (`gold_reel.json`) ; **242 fr + 210 en** ; **2 480 tokens**, **1 501 segments**, **184 cibles** d'attachement.
9: (2) Le split proposé est **402 / H50** : H50 = les **50 phrases dures** de C3 (2 hand + 48 corpus ; 25 fr + 25 en),
10: sélectionnées par score d'erreur, **sans aléa** ; la **graine 20261116** ne sert qu'au contrôle aléatoire et au
11: manifeste. (3) **10 GP/SUB** sans cible sont proposés à S (9 GP + 1 SUB ; **4 dans H50**) : le dénominateur
12: d'attachement passe de **184 à 194**. Le **sha256** du gold est id
… [15279 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md", "offset": 261, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md</path>
<type>file</type>
<content>
261: - `r358` (GP, en) — « Paul sees Marie; he speaks to her. » : `to her` → **speaks** (20–26, GV). GP datif ; cible = le verbe `speaks`.
262: - `r363` (GP, en) — « The book is on the table; I read it. » : `on the table` → **is** (9–11, GV). Famille « on the table » ; cible = le verbe `is`.
263: - `r367` (GP, en) — « The teacher speaks; the students listen to him. » : `to him` → **listen** (33–39, GV). GP datif ; cible = le verbe `listen`.
264: - `r429` (SUB, fr) — « On dit que c'est vrai. » : `que c'est vrai` → **dit** (3–6, GV). SUB complétive ; cible = le verbe `dit`.
265: 
266: ## 5. Le retrait de « gold 200+ » des docs
267: 
268: Le libellé **« gold 200+ »** est retiré des docs ; il recouvrait deux objets différents, désormais nommés :
269: 
270: | objet | nom retenu | occurrences |
271: |---|---|---:|
272: | gold linguistique réel | **gold réel 452** (20 hand + 432 corpus) | 5 |
273: | gold de pensée de B13 | **gold de pensée (B13)** | 11 |
274: | archive de la semaine 1 | **gold réel 452** (corrigé sans réécrire l'histoire) | 1 |
275: | mentions de la consign
… [4312 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md", "old_string": "| gold linguistique réel | **gold réel 452** (20 hand + 432 corpus) | 5 |\n| gold de pensée de B13 | **gold de pensée (B13)** | 11 |\n| archive de la semaine 1 | **gold réel 452** (corrigé san … [486 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nd=json.load(open('reports/rapport-gold-452.json'))\np=d['split']['phrases_h50']\nprint(collections.Counter(x['source'] for x in p))\nprint(p[0]); print(p[-1])\nprint('score rule:', d['split']['regle']['score'])\nprint('candidats ctrl:', d['con … [151 caractères tronqués]`

  ```
Counter({'corpus': 48, 'hand': 2})
{'id': 'g017', 'source': 'hand', 'langue': 'en', 'texte': 'She said that she would come yesterday.', 'score': 4, 'pos_erreurs': 0, 'segments_fn': 1, 'segments_fp': 1, 'att_erreurs': 1}
{'id': 'r410', 'source': 'corpus', 'langue': 'fr', 'texte': 'Ne dort-elle pas ?', 'score': 7, 'pos_erreurs': 2, 'segments_fn': 3, 'segments_fp': 1, 'att_erreurs': 0}
score rule: 3 × |cibles d'attachement évaluées absentes ou fausses (les segments sans cible gold ne comptent pas)| + 2 × |tokens POS faux| + 1 × |segments gold absents|
candidats ctrl: 10 segments GP/SUB sans cible (9 GP + 1 SUB) ; 0 cible ; 4 dans H50, 6 dans 402.
verif docs: scan de docs/**/*.md : 0 ligne contenant « 200+ » (18 occurrences « gold 200+ » avant, 0 après).
  ```

- **bash** `{"command": "grep -n \"rapport-gold-reel-50\\|rapport-gold-452\" reports/INDEX.md reports/README.md 2>/dev/null | head -20; echo '---'; head -40 tools/index_reports.py", "description": "Check index for gold reports"}`

  ```
reports/INDEX.md:201:| [rapport-gold-reel-50.md](rapport-gold-reel-50.md) | R0.7 / B13 — le gold réel étendu : 50 phrases que l'heuristique rate, et ce qu'elles disent |
reports/README.md:20:| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
---
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
    for ligne in p.read_text(encoding="utf-8", erro
… [469 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"rapport-gold-452\\|rapport-gold-reel-50\" docs/pilotage/en-cours.md docs/pilotage/semaine-2.md docs/pilotage/roadmap.md | head -20", "description": "Check docs links to gold reports"}`

  ```
docs/pilotage/semaine-2.md:11:> [C3](../../reports/rapport-gold-reel-50.md), [B1](../../reports/rapport-protocole-date.md),
docs/pilotage/semaine-2.md:26:| **gold réel** | **452** phrases (402 + H50), 184 cibles ; l'ancien nom est **obsolète** | H50 n'est pas encore un **test** ; **10 GP/SUB** à annoter (dont 4 dans H50) ; le dénominateur passe à **194** | [C3](../../reports/rapport-gold-reel-50.md) |
  ```

- **bash** `{"command": "sed -n '1,60p' docs/pilotage/en-cours.md; echo '===='; sed -n '100,148p' docs/pilotage/en-cours.md", "description": "Read en-cours structure"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 08 h 10 HNE (le plan de la semaine 2 est écrit)**

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
> le hook pre-commit r
… [6045 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,40p' reports/README.md; echo '---'; sed -n '195,205p' reports/INDEX.md", "description": "Read reports README/index around gold"}`

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
| [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) | **Bilan** — la semaine 07 → 15/11 : le produit, Panini, la coordination, le harnais |
| [`rapport-bilan-nuit.md`](rapport-bilan-nuit.md) | **Bilan** — la nuit du 14 au 15/11 : le tagger, la base honnête, la phase C/B |
| [`rapport-gold-reel-50.md`](r
… [3948 caractères tronqués]
  ```

- **bash** `{"command": "echo -n 'reports md: '; ls reports/*.md | wc -l; echo -n 'reports json: '; ls reports/*.json | wc -l; echo -n 'docs md: '; find docs -name '*.md' ! -path 'docs/archive/*' ! -name README.md | wc -l; echo -n 'mots en-cours: '; python3 -c \"import re,pathlib; t=pathlib.Path('docs/pilotage/ … [114 caractères tronqués]`

  ```
reports md: 749
reports json: 842
docs md: 459
mots en-cours: 1632
  ```

- **bash** `{"command": "python3 tools/index_reports.py --verifier; echo \"INDEX-VERIF-$?\"", "description": "Check if reports index is stale"}`

  ```
INDEX-VERIF-1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "old_string": "fiche gold 452 + JSON ; 402 vs H50 ;", "new_string": "[fiche gold 452](../../reports/rapport-gold-452.md) + JSON ; 402 vs H50 ;"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "old_string": "| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |", "new_string": "| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md)  … [217 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 08 h 10 HNE (le plan de la semaine 2 est écrit)**", "new_string": "**Mis à jour : 2026-11-15, 09 h 10 HNE (W1 : le gold 452 et le split 402/H50 sont figés)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit (J11)** | **`g017` tranché** ; T132/T133, gold 45 … [301 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1)** ; R2/R3 attendent N5/N4 | **route API LIVRÉE** (`--tagger`, 0bbdbbb3) ; **split réel tenu à l'é … [255 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **748** / **841** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **749** / **842** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "## Ce qui reste\n\n**N2** — porte (0,2856/0,3566) ;", "new_string": "## Ce qui reste\n\n**W1 (J1)** — gold réel **452** (20 hand + 432 corpus ; 242 fr + 210 en) ; split **402/H50** figé ; **10 G … [130 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 6, "offset": 17}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
17: |---|---|
18: | [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) | **Bilan** — la semaine 07 → 15/11 : le produit, Panini, la coordination, le harnais |
19: | [`rapport-bilan-nuit.md`](rapport-bilan-nuit.md) | **Bilan** — la nuit du 14 au 15/11 : le tagger, la base honnête, la phase C/B |
20: | [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
21: | [`rapport-protocole-date.md`](rapport-protocole-date.md) | **Panini** — le protocole à date contrôlée : 60 paires, trois strates |
22: | [`rapport-cic-v2.md`](rapport-cic-v2.md) | **Panini** — le CIC v2 : 42/42, les types clos, le sha256 sans hashlib |

(Showing lines 17-22 of 222. Use offset=23 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "old_string": "| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |", "new_string": "| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md)  … [217 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/index_reports.py && python3 tools/index_reports.py --verifier; echo \"INDEX-VERIF-$?\"; grep -n \"rapport-gold-452\" reports/INDEX.md", "description": "Regenerate and verify reports index"}`

  ```
746 fiches → reports/INDEX.md
INDEX-VERIF-0
199:| [rapport-gold-452.md](rapport-gold-452.md) | W1 — le gold réel 452 : composition, split 402 / H50, sha256 et 10 candidats GP/SUB |
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -80; echo \"REVUE-${PIPESTATUS[0]}\"", "description": "Run documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 749 fiche(s) · 842 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE-0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -40; echo \"PORTE-TABLEAUX-${PIPESTATUS[0]}\"", "description": "Run table/link gate", "timeoutMs": 300000}`

  ```
✅ 1824 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4469 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
PORTE-TABLEAUX-0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -30; echo \"EN-COURS-$?\"; python3 tools/taille_documents.py 2>&1 | tail -30; echo \"TAILLE-$?\"", "description": "Check state and document sizes", "timeoutMs": 300000}`

  ```
en-cours · 1665 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN-COURS-0
  budget de contexte · documents chargeables
    mots lignes  cat budget  document
    9002    493   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2513    224   T1   2800  reports/README.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    
… [732 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, hashlib, pathlib\nd=json.load(open('reports/rapport-gold-452.json'))\nh=set(d['split']['h50_ids']); r=set(d['split']['reste_402_ids'])\nassert len(h)==50 and len(r)==402 and not (h&r) and len(h|r)==452\nassert d['sha256']['avant']==d['sha256']['apres']\nas … [768 caractères tronqués]`

  ```
JSON-OK 50 402 3663be6cea2f 05d4f6dfae67
JSON-0
GOLD-DIFF-0
 M docs/pilotage/chantiers.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/roadmap.md
 M docs/pilotage/semaine-2.md
 M docs/pilotage/semaine-autonome.md
 M docs/produit/README.md
 M reports/INDEX.md
 M reports/README.md
?? reports/rapport-gold-452.json
?? reports/rapport-gold-452.md
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 09 h 10 HNE (W1 : le gold 452 et le split 402/H50 sont figés)**", "new_string": "**Mis à jour : 2026-11-15, 09 h 10 HNE (W1 : gold 452)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**W1 (J1)** — gold réel **452** (20 hand + 432 corpus ; 242 fr + 210 en) ; split **402/H50** figé ; **10 GP/SUB** candidats (4 dans H50) ; sha256 intact ; [fiche](../../reports/rapport-gold-452. … [92 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "**T132/T133** ; **gold de pensée** ; **porte 183/183**", "new_string": "**T132/T133** ; **gold B13** ; **porte 183/183**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "gold de pensée ; **E2**", "new_string": "gold B13 ; **E2**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "+ 8 cibles** ; **gold de pensée** ; **porte 183/183**", "new_string": "+ 8 cibles** ; **gold B13** ; **porte 183/183**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py >/tmp/taille.out 2>&1; rc=$?; tail -25 /tmp/taille.out; echo \"TAILLE-EXIT-$rc\"", "description": "Check document budgets with exit code", "timeoutMs": 120000}`

  ```
mots lignes  cat budget  document
    8999    493   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2513    224   T1   2800  reports/README.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/th
… [471 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/gen_w1.py'\ns=open(p).read()\ns=s.replace(\"'remplacement': 'gold de pensée (B13)'},\\n            {'fichier': 'docs/pilotage/roadmap.md'\", \"'remplacement': 'gold B13 (pensée)'},\\n            {'fichier': 'docs/pilotage/roadmap.md'\")\n# The above may be too  … [1011 caractères tronqués]`

  ```
patched generator
JSON écrit: reports/rapport-gold-452.json 44001 octets
H50 50 reste 402 manifeste 1615c17a97bb998451de66585dadcea0643ba1d7f8d962ccbdf28a13b575d970
métriques {'phrases': 452, 'tokens': 2480, 'pos_exactitude': 0.8891, 'pos_etiquette_exactitude': 0.9134, 'pos_justes': 2205, 'pos_erreurs': 275, 'pos_tokenisation': 66, 'f1': 0.7906, 'seg_tp': 1155, 'seg_fp': 266, 'seg_fn': 346, 'attachement_exactitude': 0.9946, 'attachement_cibles': 184, 'attachement_justes': 183, 'attachement_erreurs': 1} {'phrases': 50, 'tokens': 323, 'pos_exactitude': 0.6842, 'pos_etiquette_exactitude': 0.7568, 'pos_justes': 221, 'pos_erreurs': 102, 'pos_tokenisation': 31, 'f1': 0.5836, 'seg_tp': 103, 'seg_fp': 60, 'seg_fn': 87, 'attachement_exactitude': 0.9545, 'attachement_cibles': 22, 'attachement_justes': 21, 'attachement_erreurs': 1} {'phrases': 402, 'tokens': 2157, 'pos_exactitude': 0.9198, 'pos_etiquette_exactitude': 0.935, 'pos_justes': 1984, 'pos_erreurs': 173, 'pos_tokenisation': 35, 'f1': 0.819, 'seg_tp': 1052, 'seg_fp': 206, 'seg_fn': 259, 'attachement_exactitude': 1.0, 'attachement_cibles': 162, 'attachement_justes': 162, 'attachement_erreurs': 0} {'phrases': 50, 'tokens': 278, 'pos_exa
… [287 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-452.json'))\nfor f in d['retrait_gold_200_plus']['fichiers']:\n    print(f)\nprint(d['retrait_gold_200_plus']['regle'])\nPY", "description": "Check retrait entries after regeneration"}`

  ```
{'fichier': 'docs/pilotage/chantiers.md', 'avant': 3, 'apres': 0, 'remplacement': 'gold réel 452 (L) ; gold de pensée (B13)'}
{'fichier': 'docs/pilotage/en-cours.md', 'avant': 3, 'apres': 0, 'remplacement': 'gold de pensée (B13)'}
{'fichier': 'docs/pilotage/plan-travail.md', 'avant': 4, 'apres': 0, 'remplacement': 'gold B13 (pensée)'}
{'fichier': 'docs/pilotage/roadmap.md', 'avant': 3, 'apres': 0, 'remplacement': 'gold B13 (pensée)'}
{'fichier': 'docs/pilotage/semaine-2.md', 'avant': 2, 'apres': 0, 'remplacement': "l'ancien nom ; l'ancien libellé"}
{'fichier': 'docs/pilotage/semaine-autonome.md', 'avant': 1, 'apres': 0, 'remplacement': 'gold réel 452 (archive corrigée)'}
{'fichier': 'docs/produit/README.md', 'avant': 2, 'apres': 0, 'remplacement': 'gold réel 452'}
les occurrences B13 (pensée) deviennent « gold de pensée » (noté « gold B13 » dans la roadmap) ; les occurrences linguistiques deviennent « gold réel 452 » ; l'archive de la semaine 1 est corrigée sans réécrire l'histoire.
  ```

- **bash** `{"command": "grep -n \"plan-travail\\|roadmap.md\" /tmp/gen_w1.py | head -10", "description": "Locate retrait entries in generator"}`

  ```
301:            {'fichier': 'docs/pilotage/plan-travail.md', 'avant': 4, 'apres': 0, 'remplacement': 'gold B13 (pensée)'},
302:            {'fichier': 'docs/pilotage/roadmap.md', 'avant': 3, 'apres': 0, 'remplacement': 'gold B13 (pensée)'},
348:            'docs/pilotage/plan-travail.md', 'docs/pilotage/roadmap.md',
  ```

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/gen_w1.py'\ns=open(p).read()\ns=s.replace(\"{'fichier': 'docs/pilotage/plan-travail.md', 'avant': 4, 'apres': 0, 'remplacement': 'gold B13 (pensée)'}\",\n            \"{'fichier': 'docs/pilotage/plan-travail.md', 'avant': 4, 'apres': 0, 'remplacement': 'gold de … [376 caractères tronqués]`

  ```
ok
GEN-0
docs/pilotage/chantiers.md -> gold réel 452 (L) ; gold de pensée (B13)
docs/pilotage/en-cours.md -> gold de pensée (B13)
docs/pilotage/plan-travail.md -> gold de pensée (B13)
docs/pilotage/roadmap.md -> gold B13 (pensée)
docs/pilotage/semaine-2.md -> l'ancien nom ; l'ancien libellé
docs/pilotage/semaine-autonome.md -> gold réel 452 (archive corrigée)
docs/produit/README.md -> gold réel 452
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md", "old_string": "| gold de pensée de B13 | **gold de pensée (B13)** | 12 |", "new_string": "| gold de pensée de B13 | **gold de pensée (B13)** (noté `gold B13` dans la roadmap) | 12 |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md", "old_string": "| `docs/pilotage/roadmap.md` | 3 | 0 | gold de pensée (B13) |", "new_string": "| `docs/pilotage/roadmap.md` | 3 | 0 | gold B13 (pensée) |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -20; echo \"REVUE-${PIPESTATUS[0]}\"", "description": "Re-run documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 749 fiche(s) · 842 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE-0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -20; echo \"PORTE-TABLEAUX-${PIPESTATUS[0]}\"", "description": "Re-run table/link gate", "timeoutMs": 300000}`

  ```
✅ 1824 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4469 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
PORTE-TABLEAUX-0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py >/tmp/taille2.out 2>&1; rc=$?; tail -8 /tmp/taille2.out; echo \"TAILLE-EXIT-$rc\"; python3 tools/verifie_en_cours.py 2>&1 | tail -5; echo \"EN-COURS-${PIPESTATUS[0]}\"; python3 tools/index_reports.py --verifier; echo \"INDEX-$?\"", "description": "Re-ch … [48 caractères tronqués]`

  ```
1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3995 mots (budget 4 000)

  avertissements :
     · 57 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
TAILLE-EXIT-0
  en-cours · 1625 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN-COURS-0
INDEX-0
  ```

- **bash** `{"command": "git diff --check; echo \"DIFF-CHECK-$?\"; python3 -m json.tool reports/rapport-gold-452.json >/dev/null; echo \"JSON-TOOL-$?\"", "description": "Check whitespace and JSON syntax"}`

  ```
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:64925: new blank line at EOF.
DIFF-CHECK-2
JSON-TOOL-0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib, hashlib, json\nhits=[]\nfor p in pathlib.Path('docs').rglob('*.md'):\n    txt=p.read_text(encoding='utf-8',errors='replace')\n    for i,l in enumerate(txt.splitlines(),1):\n        if '200+' in l:\n            hits.append((str(p),i,l[:120]))\nprint('200 … [619 caractères tronqués]`

  ```
200+ docs hits: 0
tools/tests/linguistique/gold.json 20009 3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a
tools/tests/linguistique/gold_reel.json 470149 05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11
JSON sha avant==apres True
H50/reste 50 402
candidats 10 4
  ```

- **bash** `{"command": "git diff --check -- docs/pilotage/chantiers.md docs/pilotage/en-cours.md docs/pilotage/plan-travail.md docs/pilotage/roadmap.md docs/pilotage/semaine-2.md docs/pilotage/semaine-autonome.md docs/produit/README.md reports/README.md reports/INDEX.md; echo \"TARGETED-DIFF-CHECK-$?\"", "desc … [50 caractères tronqués]`

  ```
TARGETED-DIFF-CHECK-0
  ```

- **bash** `{"command": "python3 - <<'PY'\nfor f in ['reports/rapport-gold-452.md','reports/rapport-gold-452.json']:\n    txt=open(f,encoding='utf-8').read()\n    bad=[i for i,l in enumerate(txt.splitlines(),1) if l.rstrip()!=l]\n    print(f,'trailing whitespace lines',bad[:10], 'count',len(bad), 'ends newline' … [72 caractères tronqués]`

  ```
reports/rapport-gold-452.md trailing whitespace lines [] count 0 ends newline True
reports/rapport-gold-452.json trailing whitespace lines [] count 0 ends newline True
  ```

- **bash** `{"command": "git status --short -- docs reports/README.md reports/INDEX.md reports/rapport-gold-452.md reports/rapport-gold-452.json tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json; echo '---'; git diff --stat -- docs reports/README.md reports/INDEX.md; echo '---'; wc -l r … [109 caractères tronqués]`

  ```
M docs/pilotage/chantiers.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/roadmap.md
 M docs/pilotage/semaine-2.md
 M docs/pilotage/semaine-autonome.md
 M docs/produit/README.md
 M reports/INDEX.md
 M reports/README.md
?? reports/rapport-gold-452.json
?? reports/rapport-gold-452.md
---
 docs/pilotage/chantiers.md        |  6 +++---
 docs/pilotage/en-cours.md         | 14 +++++++-------
 docs/pilotage/plan-travail.md     |  8 ++++----
 docs/pilotage/roadmap.md          |  6 +++---
 docs/pilotage/semaine-2.md        |  6 +++---
 docs/pilotage/semaine-autonome.md |  2 +-
 docs/produit/README.md            |  5 +++--
 reports/INDEX.md                  |  3 ++-
 reports/README.md                 |  1 +
 9 files changed, 27 insertions(+), 24 deletions(-)
---
  353 reports/rapport-gold-452.md
 1855 reports/rapport-gold-452.json
 2208 total
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-452.json'))\n# Print compact composition and split for final verification\nprint('total', d['composition']['total'])\nprint('hand', d['composition']['par_source']['hand'])\nprint('corpus', d['composition']['par_source … [380 caractères tronqués]`

  ```
total {'phrases': 452, 'tokens': 2480, 'segments': 1501, 'cibles': 184, 'segments_par_type': {'GN': 681, 'GV': 552, 'GP': 81, 'REL': 58, 'SUB': 55, 'ADJ': 35, 'ADV': 30, 'PONCT': 9}, 'cibles_par_type': {'GP': 72, 'REL': 58, 'SUB': 54}}
hand {'phrases': 20, 'tokens': 105, 'segments': 56, 'cibles': 13, 'segments_par_type': {'GN': 23, 'GV': 20, 'GP': 10, 'REL': 1, 'SUB': 2, 'ADJ': 0, 'ADV': 0, 'PONCT': 0}, 'cibles_par_type': {'GP': 10, 'REL': 1, 'SUB': 2}}
corpus {'phrases': 432, 'tokens': 2375, 'segments': 1445, 'cibles': 171, 'segments_par_type': {'GN': 658, 'GV': 532, 'GP': 71, 'REL': 57, 'SUB': 53, 'ADJ': 35, 'ADV': 30, 'PONCT': 9}, 'cibles_par_type': {'GP': 62, 'REL': 57, 'SUB': 52}}
h50 {'phrases': 50, 'sources': {'hand': 2, 'corpus': 48}, 'langues': {'en': 25, 'fr': 25}, 'source_langue': {'hand/fr': 1, 'hand/en': 1, 'corpus/fr': 24, 'corpus/en': 24}, 'tokens': 323, 'segments': 190, 'cibles': 22}
reste {'phrases': 402, 'sources': {'hand': 18, 'corpus': 384}, 'langues': {'fr': 217, 'en': 185}, 'source_langue': {'hand/fr': 13, 'hand/en': 5, 'corpus/fr': 204, 'corpus/en': 180}, 'tokens': 2157, 'segments': 1311, 'cibles': 162}
manifest 1615c17a97bb998451de66585dadcea0643ba1d7f8d962c
… [216 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- reports/INDEX.md reports/README.md docs/pilotage/en-cours.md | sed -n '1,160p'", "description": "Review index/readme/en-cours diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 8726729b..0ffda7dc 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 08 h 10 HNE (le plan de la semaine 2 est écrit)**
+**Mis à jour : 2026-11-15, 09 h 10 HNE (W1 : gold 452)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -64,9 +64,9 @@
 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)) ; **D2** ([v2](../../reports/rapport-restitution-v2.md)) ; **D3** ([FAQ](../../reports/rapport-faq.md), 10/10) ; **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; **E2** ([cas d'erreur](../../reports/rapport-tagger-erreurs.md)).
 - **Ce que font les aut
… [6276 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**R0.7** — split réel ;", "new_string": "**R0.7** — tagger 402/H50 ;"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py >/tmp/taille3.out 2>&1; rc=$?; tail -4 /tmp/taille3.out; echo \"TAILLE-$rc\"; python3 tools/verifie_en_cours.py >/tmp/ec.out 2>&1; rc=$?; tail -3 /tmp/ec.out; echo \"EN-COURS-$rc\"", "description": "Re-check budgets after state tweak", "timeoutMs": 1200 … [3 caractères tronqués]`

  ```
avertissements :
     · 57 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
TAILLE-0
  en-cours · 1625 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN-COURS-0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py >/tmp/revue.out 2>&1; rc=$?; tail -3 /tmp/revue.out; echo \"REVUE-$rc\"; bash tools/porte-tableaux.sh >/tmp/tableaux.out 2>&1; rc=$?; tail -3 /tmp/tableaux.out; echo \"TABLEAUX-$rc\"", "description": "Re-check review and links", "timeoutMs": 300000}`

  ```
revue de documentation · 749 fiche(s) · 842 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE-0
  ✅ 1824 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4469 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
TABLEAUX-0
  ```

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/gen_w1.py'\ns=open(p).read()\ns=s.replace(\"\"\"            'sans_cible': '10 GP/SUB sans cible (9 GP + 1 SUB) = les 10 candidats du § 4',\"\"\",\n\"\"\"            'sans_cible': '10 GP/SUB sans cible (9 GP + 1 SUB) = les 10 candidats du § 4',\n            'sou … [272 caractères tronqués]`

  ```
ok
GEN-0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md", "old_string": "Le corpus pèse **2 375 tokens** (95,8 % du gold) et **171 cibles** ; le hand pèse **105 tokens** et **13 cibles**.", "new_string": "Le corpus pèse **2 375 tokens** (95,8 % du gold) et **171 ci … [141 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-452.md has been updated successfully.
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-gold-452.json >/dev/null && echo JSON-TOOL-OK\npython3 - <<'PY'\nimport json, pathlib, hashlib\nd=json.load(open('reports/rapport-gold-452.json'))\nh=set(d['split']['h50_ids']); r=set(d['split']['reste_402_ids'])\nassert len(h)==50 and len(r)==402 an … [796 caractères tronqués]`

  ```
JSON-TOOL-OK
JSON-OK
DOCS-200+ 0
SHA tools/tests/linguistique/gold.json 3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a
SHA tools/tests/linguistique/gold_reel.json 05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py >/tmp/revue2.out 2>&1; rc=$?; tail -3 /tmp/revue2.out; echo \"REVUE-$rc\"; python3 tools/index_reports.py --verifier; echo \"INDEX-$?\"; git diff --check -- docs/pilotage docs/produit/README.md reports/README.md reports/INDEX.md; echo \"DIFF-CHECK-$? … [82 caractères tronqués]`

  ```
revue de documentation · 749 fiche(s) · 842 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE-0
INDEX-0
DIFF-CHECK-0
  ```

- **bash** `{"command": "sed -n '1,90p' reports/rapport-gold-452.json", "description": "Read JSON header/composition"}`

  ```
{
  "date": "2026-11-15",
  "date_cible": "2026-11-16 (J1 · matin)",
  "ligne": "R0.7 / B13",
  "tache": "W1 — le gold réel 452 : composition, split 402/H50, sha256 et 10 candidats GP/SUB",
  "commit_mesure": "6b2208ee1579739a188086f957c0d508e8a04726",
  "commit_c3": "f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888",
  "objet": {
    "gold": "gold réel 452 = 20 hand + 432 corpus",
    "fichiers": {
      "hand": "tools/tests/linguistique/gold.json",
      "corpus": "tools/tests/linguistique/gold_reel.json"
    },
    "unites": {
      "phrase": "un item du gold",
      "token": "mot gold (mots[])",
      "segment": "syntagme gold (segments[])",
      "cible": "attachement d'un GP/REL/SUB à son gouverneur"
    },
    "note": "lecture seule ; aucun fichier gold n'est modifié"
  },
  "composition": {
    "total": {
      "phrases": 452,
      "tokens": 2480,
      "segments": 1501,
      "cibles": 184,
      "segments_par_type": {
        "GN": 681,
        "GV": 552,
        "GP": 81,
        "REL": 58,
        "SUB": 55,
        "ADJ": 35,
        "ADV": 30,
        "PONCT": 9
      },
      "cibles_par_type": {
        "GP": 72,
        "REL": 58,
        "SUB": 54
      }
    },
    "par
… [926 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-452.json'))\nprint(json.dumps({k:d[k] for k in ('date','date_cible','ligne','tache','commit_mesure','commit_c3')},ensure_ascii=False,indent=1))\nprint(json.dumps(d['candidats_a_annoter']['priorite_1']['effet'],ensure_ … [158 caractères tronqués]`

  ```
{
 "date": "2026-11-15",
 "date_cible": "2026-11-16 (J1 · matin)",
 "ligne": "R0.7 / B13",
 "tache": "W1 — le gold réel 452 : composition, split 402/H50, sha256 et 10 candidats GP/SUB",
 "commit_mesure": "6b2208ee1579739a188086f957c0d508e8a04726",
 "commit_c3": "f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888"
}
{
 "cibles_avant": 184,
 "cibles_apres": 194,
 "delta": 10,
 "avant_par_type": {
  "GP": 72,
  "REL": 58,
  "SUB": 54
 },
 "apres_par_type": {
  "GP": 81,
  "REL": 58,
  "SUB": 55
 },
 "par_base": {
  "h50": {
   "avant": 22,
   "candidats": 4,
   "apres": 26
  },
  "reste_402": {
   "avant": 162,
   "candidats": 6,
   "apres": 168
  },
  "total": {
   "avant": 184,
   "candidats": 10,
   "apres": 194
  }
 }
}
{
 "partition": "H50 ∩ 402 = 0 ; H50 ∪ 402 = 452 ; aucun id dupliqué.",
 "reproduction": "recalcul au HEAD 6b2208ee : 50/50 ids identiques à C3 ; 50/50 scores identiques ; Jaccard 1,0.",
 "hash": "sha256 avant = après ; git diff des deux gold vide.",
 "tirage_aleatoire": "graine 20261116 : POS 88,13 %, F1 78,69 %, attachement 100 % ; H50 : 68,42 %, 58,36 %, 95,45 %.",
 "candidats": "10 segments GP/SUB sans cible (9 GP + 1 SUB) ; 0 cible ; 4 dans H50, 6 dans 402.",
 "docs": "
… [47 caractères tronqués]
  ```

### 🤖 Assistant

## Livrables

- Fiche : [`reports/rapport-gold-452.md`](reports/rapport-gold-452.md)
- JSON : [`reports/rapport-gold-452.json`](reports/rapport-gold-452.json)

## Ce que la fiche établit

**1. Composition exacte des 452**
- **20 hand** (`gold.json`) : 14 fr + 6 en.
- **432 corpus** (`gold_reel.json`, source brute `reel`) : 228 fr + 204 en.
- Total : **242 fr + 210 en**, **2 480 tokens**, **1 501 segments**, **184 cibles** (GP 72, REL 58, SUB 54).
- Il reste **10 GP/SUB sans cible** : 9 GP + 1 SUB.

**2. Split 402 / H50**
- H50 = les **50 phrases dures de C3** : **2 hand + 48 corpus**, **25 fr + 25 en**, **323 tokens**, **190 segments**, **22 cibles**.
- 402 = **18 hand + 384 corpus**, **217 fr + 185 en**, **2 157 tokens**, **1 311 segments**, **162 cibles**.
- Règle déterministe : score `3×att + 2×POS + 1×segment absent`, tri `(-score, id)`, au plus 2 phrases par signature d'erreur, quota 25/25. **Aucun aléa.**
- **Graine `20261116`** : elle ne sert **pas** à tirer H50 (lot dur C3) ; elle fixe le **contrôle négatif** et le **manifeste** (`1615c17a…`). Le tirage aléatoire de cette graine est fourni dans le JSON, non retenu.
- Manifeste : `1615c17a97bb998451de66585dadcea0643ba1d7f8d962ccbdf28a13b575d970`.

**3. sha256 avant du gold** — identique après :
- `gold.json` : `3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a`
- `gold_reel.json` : `05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11`
- Concaténation ordonnée : `cff6b6d703546ad5992c5ada4fc99e1bdaa8e76e9cd089bd3e3b88bd71e90ac5`

**4. 10 GP/SUB candidats pour S** (cible proposée = verbe gouverneur) :

| id | span | cible |
|---|---|---|
| `r267` | `à moi` | `est` (30–33) |
| `r324` | `sur la table` | `est` (9–12) |
| `r328` | `on the table` | `is` (9–11) |
| `r336` | `to her` | `speaks` (20–26) |
| `r342` | `to her` | `speaks` (20–26) |
| `r349` | `sur la table` | `est` (9–12) |
| `r358` | `to her` | `speaks` (20–26) |
| `r363` | `on the table` | `is` (9–11) |
| `r367` | `to him` | `listen` (33–39) |
| `r429` | `que c'est vrai` (SUB) | `dit` (3–6) |

**4 dans H50** (`r324`, `r328`, `r349`, `r363`) ; double codage proposé sur ces 4. Si S accepte les 10 : **184 → 194** cibles (GP 72→81, SUB 54→55 ; H50 22→26, 402 162→168).

**5. « gold 200+ » retiré des docs**
- **18 occurrences** exactes supprimées, **0 ligne `200+`** restante dans `docs/**/*.md`.
- Les occurrences **B13** deviennent **« gold de pensée (B13) »** (noté `gold B13` dans la roadmap) ; les occurrences **linguistiques** deviennent **« gold réel 452 »**.
- Fichiers touchés : `chantiers.md`, `en-cours.md`, `plan-travail.md`, `roadmap.md`, `semaine-2.md`, `semaine-autonome.md`, `produit/README.md`.

## Contrôles passés

- `python3 tools/revue_documentation.py` → **0**
- `bash tools/porte-tableaux.sh` → **0**
- `python3 tools/taille_documents.py` → **0** (T0 3 995 / 4 000)
- `python3 tools/verifie_en_cours.py` → **0**
- `python3 tools/index_reports.py --verifier` → **0**
- `git diff -- tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json` → **vide**
- Aucun fichier `tools/tests/linguistique/gold_*.json` modifié.

Le gold est intact ; les fichiers sont **non committés** (à la session principale de committer).

