# Session DSH — relecture

- identifiant : `session-b3e96cb1-fb3b-4593-a2a6-b034ae644413`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-16 03:01:09
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche V3 (clôture) : la clôture de la nuit — le rapport `reports/rapport-bilan-exploitable-2.md` + JSON (les 9 tâches T/U/V, les chiffres, les négatifs), la mise à jour de `docs/pilotage/en-cours.md` et de la roadmap, le **tag annoté** `exploitable-2026-11-16` sur le dernier commit vert, et le relevé des portes (`work/portes/`, sans relancer la passe).

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

- **bash** `{"command": "pwd && git status --short && git log --oneline -20", "description": "Inspect repository status and recent log"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
ae3c24f2 V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
2e617034 EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)
1d4eb49e JOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4
c77ed4b6 U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE
04894aea U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4)
75a56c05 U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)
d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/4 LUE, 86E PORTE VERTE
9a291
… [1402 caractères tronqués]
  ```

- **bash** `{"command": "ls -la && ls -la work 2>/dev/null && ls -la work/portes 2>/dev/null && ls -la reports | tail -30", "description": "List workspace, work/portes and reports"}`

  ```
total 212
drwxr-xr-x. 1 stephane stephane   760 16 nov 02:01 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    42 16 nov 02:01 build
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane    56 16 nov 00:38 dist
drwxr-xr-x. 1 stephane stephane   138 15 nov 22:25 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   136 16 nov 02:01 drave.egg-info
drwxr-xr-x. 1 stephane stephane   220 16 nov 03:01 .git
-rw-r--r--. 1 stephane stephane   653 15 nov 22:25 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane  1012 16 nov 00:22 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-------. 1 stephane stephane  1272 16 nov 01:44 pyproject.toml
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-boot
… [11108 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports | grep -iE 'exploitable|bilan|T[0-9]|U[0-9]|V[0-9]' | tail -60", "description": "List exploitable/bilan reports"}`

  ```
-rw-------. 1 stephane stephane   21608 15 nov 23:37 rapport-bilan-exploitable.md
-rw-r--r--. 1 stephane stephane    3803 15 nov 14:10 rapport-bilan-jour-1115.md
-rw-r--r--. 1 stephane stephane    3041 15 nov 04:32 rapport-bilan-nuit.md
-rw-r--r--. 1 stephane stephane    5196 15 nov 06:23 rapport-bilan-semaine.md
-rw-------. 1 stephane stephane   15713 15 nov 04:01 rapport-cic-v2.md
-rw-r--r--. 1 stephane stephane   28110 15 nov 12:34 rapport-coherence-fiches-v7.md
-rw-------. 1 stephane stephane   45633  5 nov 22:51 rapport-coherence-fiches-v8.md
-rw-------. 1 stephane stephane   11559 15 nov 02:12 rapport-coordination-n2-v2.json
-rw-------. 1 stephane stephane   15412 15 nov 02:12 rapport-coordination-n2-v2.md
-rw-r--r--. 1 stephane stephane   22126 15 nov 02:30 rapport-coordination-s-v2.json
-rw-------. 1 stephane stephane   23828 15 nov 02:30 rapport-coordination-s-v2.md
-rw-r--r--. 1 stephane stephane    2467 28 oct 09:17 rapport-couche-int8-canal.md
-rw-r--r--. 1 stephane stephane    1885 28 oct 09:17 rapport-couche-int8.md
-rw-------. 1 stephane stephane   10481 28 oct 09:17 rapport-decoupage-v41.md
-rw-r--r--. 1 stephane stephane   34830 15 nov 12:34 rapport-dev-test-v10.md
… [3506 caractères tronqués]
  ```

- **bash** `{"command": "ls -la work/portes/roue-1116 && find work/portes/roue-1116 -maxdepth 2 -type f | head -50", "description": "Inspect latest door pass directory"}`

  ```
total 400
drwxr-xr-x. 1 stephane stephane  3590 16 nov 02:50 .
drwxr-xr-x. 1 stephane stephane   602 16 nov 00:45 ..
drwxr-xr-x. 1 stephane stephane    64 16 nov 01:01 deepseek-porte
-rw-r--r--. 1 stephane stephane 26243 16 nov 01:57 jeux-mesures.json
-rw-r--r--. 1 stephane stephane  9218 16 nov 01:57 langues-mesures.json
-rw-r--r--. 1 stephane stephane  3310 16 nov 01:58 maitres-mesures.json
-rw-r--r--. 1 stephane stephane   580 16 nov 00:46 porte-adaptateur-sortie.log
-rw-r--r--. 1 stephane stephane  1407 16 nov 00:49 porte-audit-drapeaux.log
-rw-r--r--. 1 stephane stephane   398 16 nov 00:49 porte-b1110-hybride.log
-rw-r--r--. 1 stephane stephane   413 16 nov 00:49 porte-balayage.log
-rw-r--r--. 1 stephane stephane   264 16 nov 00:49 porte-banc-performance.log
-rw-r--r--. 1 stephane stephane   866 16 nov 00:49 porte-bloc-code.log
-rw-r--r--. 1 stephane stephane  1101 16 nov 00:50 porte-bloc-linguistique.log
-rw-r--r--. 1 stephane stephane   877 16 nov 00:50 porte-bloc-maths.log
-rw-r--r--. 1 stephane stephane  1035 16 nov 00:50 porte-bloc-tableaux.log
-rw-r--r--. 1 stephane stephane  2083 16 nov 00:51 porte-budget.log
-rw-r--r--. 1 stephane stephane   868 16 nov 00:52 porte-bus.
… [7557 caractères tronqués]
  ```

- **bash** `{"command": "git tag -l | tail -20 && echo '---' && git log --oneline --decorate -3", "description": "List tags and decorated recent commits"}`

  ```
chantier-2026-11-14
semaine-2-2026-11-20
semaine-2026-11-14
---
ae3c24f2 (HEAD -> s/v7) V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
2e617034 (origin/s/v7, origin/master, origin/HEAD, master) EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)
1d4eb49e JOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4
  ```

- **bash** `{"command": "git branch -a --contains HEAD && echo '---' && git log --oneline --all --decorate -30", "description": "Check branches and full recent log"}`

  ```
* s/v7
---
ae3c24f2 (HEAD -> s/v7) V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
2e617034 (origin/s/v7, origin/master, origin/HEAD, master) EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)
1d4eb49e JOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4
c77ed4b6 U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE
04894aea U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4)
75a56c05 U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)
d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/
… [3057 caractères tronqués]
  ```

- **bash** `{"command": "grep -rilE 'exploitable|T[0-9]|U[0-9]|V[0-9]' docs/pilotage | head -40", "description": "Find planning docs mentioning tasks"}`

  ```
docs/pilotage/manques.md
docs/pilotage/backlog/R04-tete-survol.md
docs/pilotage/backlog/R05-tete-balayage.md
docs/pilotage/backlog/R06-tete-relecture.md
docs/pilotage/backlog/R13-tokenisation-bpe.md
docs/pilotage/backlog/N2-distillation.md
docs/pilotage/backlog/A8.3-defaut.md
docs/pilotage/programme-r.md
docs/pilotage/README.md
docs/pilotage/chantiers.md
docs/pilotage/plan-travail.md
docs/pilotage/semaine-autonome.md
docs/pilotage/references-non-regression.md
docs/pilotage/semaine-2.md
docs/pilotage/roadmap.md
docs/pilotage/en-cours.md
  ```

- **bash** `{"command": "ls -la docs/pilotage/ && grep -n 'V3\\|exploitable\\|nuit' docs/pilotage/en-cours.md | head -40", "description": "List pilotage docs and search en-cours"}`

  ```
total 264
drwxr-xr-x. 1 stephane stephane   322 16 nov 02:54 .
drwxr-xr-x. 1 stephane stephane   138 15 nov 22:25 ..
drwxr-xr-x. 1 stephane stephane  1686  4 nov 11:53 backlog
-rw-r--r--. 1 stephane stephane 26157 15 nov 09:00 chantiers.md
-rw-r--r--. 1 stephane stephane 12517 16 nov 02:54 en-cours.md
-rw-r--r--. 1 stephane stephane 12411 28 oct 09:17 manques.md
-rw-r--r--. 1 stephane stephane 34763 15 nov 09:00 plan-travail.md
-rw-r--r--. 1 stephane stephane 22138  1 nov 13:46 programme-r.md
-rw-r--r--. 1 stephane stephane  4380  2 nov 20:20 README.md
-rw-r--r--. 1 stephane stephane 14391 15 nov 12:34 references-non-regression.md
-rw-r--r--. 1 stephane stephane 64551 16 nov 02:40 roadmap.md
-rw-r--r--. 1 stephane stephane 14966 15 nov 12:34 semaine-2.md
-rw-r--r--. 1 stephane stephane 22973 15 nov 09:00 semaine-autonome.md
-rw-r--r--. 1 stephane stephane 14336 28 oct 09:17 utilisation.md
19:> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
123:**T1–T6** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s) ; **U2 — la roue** (1 727 201 o, sans gold → 4) ; **U3** profils 20/20 ; **V2** **27/27** ; [bilan](../../reports/rapport-bilan-exploitable.
… [267 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-16 (V2)**
4: 
5: > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
6: 
7: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
8: 
9: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
10: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
11: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
12: - **Prochaine action** : **suivi docs**, puis la **passe**.
13: - **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
14: - **Bloquants** : aucun.
15: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
16: 
17: ## Sessions en cours
18: 
19: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
20: > [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
21: > `plan.md` (`python3 tools/sess
… [11803 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal | tail -20 && find journal -iname '*1116*' -o -iname '*2026-11-16*' | head -40", "description": "Find journal entries for 2026-11-16"}`

  ```
drwxr-xr-x. 1 stephane stephane   228 28 oct 14:06 2026-10-26
drwxr-xr-x. 1 stephane stephane   290 28 oct 14:11 2026-10-27
drwxr-xr-x. 1 stephane stephane   216 28 oct 14:06 2026-10-28
drwxr-xr-x. 1 stephane stephane   208 29 oct 17:08 2026-10-29
drwxr-xr-x. 1 stephane stephane   150 31 oct 11:22 2026-10-30
drwxr-xr-x. 1 stephane stephane   182 31 oct 23:28 2026-10-31
drwxr-xr-x. 1 stephane stephane   244  1 nov 22:30 2026-11-01
drwxr-xr-x. 1 stephane stephane   224  2 nov 20:13 2026-11-02
drwxr-xr-x. 1 stephane stephane   224  3 nov 16:48 2026-11-03
drwxr-xr-x. 1 stephane stephane   180  4 nov 23:37 2026-11-04
drwxr-xr-x. 1 stephane stephane   174  5 nov 10:24 2026-11-05
drwxr-xr-x. 1 stephane stephane   168  6 nov 22:24 2026-11-06
drwxr-xr-x. 1 stephane stephane   132  7 nov 15:13 2026-11-07
drwxr-xr-x. 1 stephane stephane    76 13 nov 23:10 2026-11-13
drwxr-xr-x. 1 stephane stephane   132 14 nov 06:59 2026-11-14
drwxr-xr-x. 1 stephane stephane   150 15 nov 23:37 2026-11-15
drwxr-xr-x. 1 stephane stephane    90 16 nov 02:50 2026-11-16
-rw-r--r--. 1 stephane stephane 55638 16 nov 02:57 README.md
drwxr-xr-x. 1 stephane stephane 17400 16 nov 02:48 sessions
-rw-r--r--. 1 stephane st
… [54 caractères tronqués]
  ```

- **bash** `{"command": "grep -nE '^\\|? ?(T[1-6]|U[1-3]|V[1-3])\\b|T1|T2|T3|T4|T5|T6|U1|U2|U3|V1|V2|V3' docs/pilotage/plan-travail.md | head -80", "description": "Search task plan for T/U/V tasks"}`

  ```
39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **166/166** (6 S fixés ; T132/T133 2/5), gold **432**, 116 liens ; **gold neuronal** (POS **0,9415** / syntagmes **0,7539** / acte **1,0**) ; **DRVM/native** règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusion par sous-type : le double sens 0,9884 (+0,0208) ; variance du sous-type : 0,9838 ; tirages : 0,9838 ×3 (déterministe sur ces invites) ; attachement : top1 0,3431, exact 0,0042 ; cibles : 1863 segments, 1624 sans cible (87,2 %), couverture réelle 0,1283 ; cibles 500 : 294 GN / 206 GV ; relation GN → GV : 221/637 ; rôles par position : 301/322, relation 0,8195 (522/637) surévaluée ; correctif `par` → agent (partiel : le générateur S garde `moyen`) ; sans `par` : le chunker 3/3, le générateur S ignore ; cible par proximité : exact 0,0042 → 0,0544 ; candidats verbes : top-k 0,4686, tête 0,7655 ; échecs qualifiés : 127 = 94 span + 33 cible** (négation/modalité sous l'heuristique). Prochaine : **T132/T133**
… [1445 caractères tronqués]
  ```

- **bash** `{"command": "grep -rilE '\\bT6\\b|\\bU3\\b|\\bV3\\b' docs journal reports 2>/dev/null | head -40", "description": "Find files mentioning T6/U3/V3"}`

  ```
docs/archive/note-cancellation-evenementielle.md
docs/archive/note-corpus-panini.md
docs/archive/note-ingestion-corpus.md
docs/archive/plan-cerveau-complet.md
docs/archive/plan-deepseek41-complet.md
docs/archive/plan-mla-vision.md
docs/archive/plan-prefill-reparti.md
docs/archive/roadmap-detail-2026-10-29.md
docs/schemas/pipeline.mmd.svg
docs/pilotage/backlog/R04-tete-survol.md
docs/pilotage/backlog/R06-tete-relecture.md
docs/pilotage/semaine-2.md
docs/pilotage/roadmap.md
docs/pilotage/en-cours.md
docs/theorie/glossaire/02-modeles-et-architectures.md
docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
docs/theorie/glossaire/05-flux-protocole-et-transport.md
docs/theorie/glossaire/06-repartition-materiel-et-energie.md
docs/theorie/glossaire/07-mesure-qualite-et-methode-experimentale.md
docs/theorie/glossaire/09-sources-externes-citees.md
docs/theorie/glossaire/README.md
docs/theorie/glossaire/entrees/ecart-relatif-rms-ecart-max.md
docs/theorie/glossaire/entrees/trace-de-flux-versions-1-a-3.md
docs/theorie/glossaire/entrees/xeon-e5-2687w-v3-cpu.md
docs/theorie/glossaire/index.json
docs/implantation/format-flux.md
docs/implantation/configuration-nvme-raid-amd.md
docs
… [848 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/2026-11-16 && for f in journal/2026-11-16/*; do echo \"=== $f\"; head -40 \"$f\"; done", "description": "Read 2026-11-16 journal entries"}`

  ```
total 24
drwxr-xr-x. 1 stephane stephane   90 16 nov 02:50 .
drwxr-xr-x. 1 stephane stephane 1012 16 nov 00:22 ..
-rw-r--r--. 1 stephane stephane 2120 16 nov 02:57 docs.md
-rw-r--r--. 1 stephane stephane 1076 16 nov 02:57 memoire.md
-rw-r--r--. 1 stephane stephane 1879 16 nov 02:57 mesures.md
-rw-r--r--. 1 stephane stephane 1001 16 nov 02:57 moteur.md
-rw-r--r--. 1 stephane stephane 4450 16 nov 02:57 README.md
=== journal/2026-11-16/docs.md
# 2026-11-16 — Documentation, état, conventions

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (2)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:48 | `1d4eb49e` | JOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4 | `README.md`, `mesures.md`, `README.md` (+3) |
| 02:47 | `1a5a6548` | V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE | `bloc
… [7498 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'U1\\|U2\\|U3\\|T1\\|T6\\|V1\\|V2\\|exploitable' docs/pilotage/roadmap.md | head -80", "description": "Locate T/U/V in roadmap"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [11837 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/*bilan* && echo '--- JSON ---' && ls -la reports/*bilan*.json 2>/dev/null; grep -n 'T1\\|T2\\|T3\\|T4\\|T5\\|T6\\|U1\\|U2\\|U3' reports/rapport-bilan-exploitable.md | head -40", "description": "Inspect existing bilan exploitable"}`

  ```
-rw-r--r--. 1 stephane stephane   907 29 oct 16:25 reports/a26-bilan.json
-rw-r--r--. 1 stephane stephane  3861 27 oct 09:33 reports/bilan-b11.md
-rw-------. 1 stephane stephane  9416  2 oct 15:32 reports/bilan-multi-materiel.md
-rw-r--r--. 1 stephane stephane   378  2 nov 07:32 reports/pensee-anaphore-bilan.json
-rw-r--r--. 1 stephane stephane   871 15 nov 04:32 reports/pensee-bilan-nuit.json
-rw-r--r--. 1 stephane stephane  2298 29 oct 16:25 reports/rapport-a26-bilan.md
-rw-r--r--. 1 stephane stephane 39210 14 nov 03:52 reports/rapport-bilan-chantier.json
-rw-------. 1 stephane stephane 38158 14 nov 03:52 reports/rapport-bilan-chantier.md
-rw-------. 1 stephane stephane 17845 15 nov 23:36 reports/rapport-bilan-exploitable.json
-rw-------. 1 stephane stephane 21608 15 nov 23:37 reports/rapport-bilan-exploitable.md
-rw-r--r--. 1 stephane stephane  3803 15 nov 14:10 reports/rapport-bilan-jour-1115.md
-rw-r--r--. 1 stephane stephane  3041 15 nov 04:32 reports/rapport-bilan-nuit.md
-rw-r--r--. 1 stephane stephane  5196 15 nov 06:23 reports/rapport-bilan-semaine.md
-rw-r--r--. 1 stephane stephane  3174  2 nov 07:32 reports/rapport-pensee-anaphore-bilan.md
--- JSON ---
-rw-r--r--. 1 ste
… [2091 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 140, "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
140: de J1.1 à J12.2, **25 acceptations vertes**, **1 échec** (J5.2, le tag), **5 timeouts** dont **4
141: récupérés**. Chaque ligne porte sa **base** (612/602), son **avant**, son **après**, son **Δ**, un
142: **contrôle négatif**, son **commit** et sa **fiche** : produit (**F1 0,7533 → 0,7902**,
143: attachement **236/237 → 238/238 labels**, couverture **0,9916 → 0,9958**, spans **2 → 1**,
144: schéma v2, restitution v1, 50 textes, 5 exemples, fr/en), tagger (**0,9475, +8,49**), Panini
145: (table **14/14**, corpus **418/438**, retrieval, généalogie **154/154**, familles **0,619 vs
146: 0,0445**, §334, CIC **42/42**), portes (**183/183**, passe **81/84**). La **base 612/602** est
147: re-mesurée au HEAD `b20a4c31` : **0,7902 / 0,7882** (F1), **238/239 / 234/239** (attachement).
148: [`tableau`](../../reports/rapport-tableau-mesures.md) + [`JSON`](../../reports/tableau-mesures.json).
149: 
150: **J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag `chantier-2026-11-14`.** La
151: passe du **14/11 00 h 30** (`work/portes/passe-1311-23h15.log`) n'est **pa
… [5897 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/ && grep -n 'V1\\|V2\\|V3\\|T1\\|T6\\|U1\\|U3\\|nuit\\|exploitable' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md | head -60", "description": "Search session plan for V tasks"}`

  ```
total 25580
drwxr-xr-x. 1 stephane stephane       94 16 nov 00:40 .
drwxr-xr-x. 1 stephane stephane    17400 16 nov 02:48 ..
-rw-r--r--. 1 stephane stephane  4235473 16 nov 02:54 digest.md
-rw-r--r--. 1 stephane stephane     7254 16 nov 00:40 plan.md
-rw-r--r--. 1 stephane stephane   775011 16 nov 02:56 rapport.md
-rw-------. 1 stephane stephane 21166361 16 nov 02:49 session.v4.jsonl.zstd
19:- **Prochaine action** : **U3 — `--profils`** ; **U1** (α **1,08**, 10 000 mots **0,82 s**, sorties identiques ; [fiche](../../../reports/rapport-performance-fix.md)) et **U2** (roue autonome, gold dedans, roue sans gold → 4 ; [fiche](../../../reports/rapport-roue.md)) sont livrés.
28:  regret, justification, rejeu) et intégration DRVM/DRVF ; 9) ~~bloc linguistique~~ (R0.7, 398 langues) ; 10) ~~coréférence et absences~~ (140/140, gold 432) ; 11) ~~gold neuronal~~ (tagger 7B local, cascade POS 0,9440) ; 12) ~~syntagmes~~ (BIO 7B, exact 0,6173, tête 0,7606) ; 13) ~~cascade complète~~ (POS 0,9415, syntagmes 0,7539, acte 1,0) ; 14) ~~DRVM/native~~ (cadenas 3 nœuds avec règle, minimal 0 ; porte 27 nœuds avec règle) ; 15) ~~porte DRVM~~ (27 nœuds, 4 sonde) ; 16) ~~pragmatique neuronale~~ (négatif : d
… [1101 caractères tronqués]
  ```

- **bash** `{"command": "find . -path ./.git -prune -o -iname '*exploitable*' -print 2>/dev/null | head -30 && echo '---' && grep -ril 'rapport-bilan-exploitable-2' . --exclude-dir=.git 2>/dev/null | head", "description": "Find exploitable files and references to bilan 2"}`

  ```
./reports/rapport-bilan-exploitable.json
./reports/rapport-bilan-exploitable.md
---
[still running after 60000ms; moved to background job bash-16]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md</path>
<type>file</type>
<content>
1: # Plan de session — Pensée, la RSN plurielle et le moteur N3
2: 
3: > **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
4: > [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
5: > synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
6: > Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
7: 
8: - **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
9: - **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
10: - **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
11: - **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
12:   `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
13:   `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`,
14:   `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`,
15:   `tools/porte-bloc-linguistique.
… [6345 caractères tronqués]
  ```

- **bash** `{"command": "cat work/portes/roue-1116/registre.txt", "description": "Read latest doors registry"}`

  ```
porte-adaptateur-sortie 0 74
porte-audit-drapeaux 0 182
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-banc-performance 0 17
porte-bloc-code 0 17
porte-bloc-linguistique 0 18
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 53
porte-bus 0 86
porte-bus-socket 0 102
porte-c4-retard 0 35
porte-cerveau 0 9
porte-cic 0 13
porte-consolidation 0 82
porte-coupe 0 155
porte-cycle-c2 0 142
porte-deepseek 0 1
porte-delais 0 24
porte-diff-couche 0 22
porte-document 0 6
porte-echange-experts 0 62
porte-episodique 0 205
porte-etat 0 0
porte-flux 0 28
porte-fusion 0 9
porte-gain 0 253
porte-greffe 0 791
porte-harnais-invariants 0 127
porte-homeostasie 0 614
porte-horloge 0 29
porte-indice 1 1127
porte-jeux 0 131
porte-jumeaux 0 33
porte-lecteur 0 1
porte-lecture 0 2
porte-m5-brouillon 0 1
porte-melange 1 149
porte-memoire 0 12
porte-miroir-blocs 0 12
porte-mistral 0 10
porte-n3-cache 0 7
porte-n3-composition 0 7
porte-n3-deux-processus 0 6
porte-n3-deux-regions 0 5
porte-n3-generation 0 10
porte-n3-inventaire 0 0
porte-n3-placement 0 5
porte-n3-pont 0 6
porte-n3-positions 0 6
porte-n3-profondeur 0 7
porte-n3-refus 0 6
porte-n3-reseau 0 5
porte-n3-routes 0 6
porte-n3-service-briques 0
… [698 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/toutes-les-portes.sh", "description": "Read doors runner script"}`

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

- **bash** `{"command": "ls -la work/portes/roue-1116 | tail -20 && find work/portes/roue-1116 -maxdepth 1 -type f -printf '%f\\n' | sort | tail -30", "description": "Inspect door pass directory contents"}`

  ```
-rw-r--r--. 1 stephane stephane  2100 16 nov 02:24 porte-pont.log
-rw-r--r--. 1 stephane stephane  1549 16 nov 02:27 porte-prechargement.log
-rw-r--r--. 1 stephane stephane   870 16 nov 02:30 porte-produit.log
-rw-r--r--. 1 stephane stephane  3392 16 nov 02:41 porte-profondeur-routee.log
-rw-r--r--. 1 stephane stephane   496 16 nov 02:41 porte-push-paresseux.log
-rw-r--r--. 1 stephane stephane   487 16 nov 02:42 porte-r13-bpe.log
-rw-r--r--. 1 stephane stephane   859 16 nov 02:42 porte-recurrence.log
-rw-r--r--. 1 stephane stephane  3147 16 nov 02:45 porte-reflexe.log
-rw-r--r--. 1 stephane stephane   453 16 nov 02:45 porte-registre.log
-rw-r--r--. 1 stephane stephane   296 16 nov 02:45 porte-reparti-moteur.log
-rw-r--r--. 1 stephane stephane   539 16 nov 02:45 porte-ressources.log
-rw-r--r--. 1 stephane stephane  1396 16 nov 02:46 porte-sauvegarde-modele.log
-rw-r--r--. 1 stephane stephane   286 16 nov 02:46 porte-sessions.log
-rw-r--r--. 1 stephane stephane   703 16 nov 02:48 porte-speculatif.log
-rw-r--r--. 1 stephane stephane   279 16 nov 02:48 porte-tableaux.log
-rw-r--r--. 1 stephane stephane   127 16 nov 02:48 porte-tokenizer-kimi.log
-rw-r--r--. 1 stephane stephane  1257 16
… [860 caractères tronqués]
  ```

- **bash** `{"command": "wc -l work/portes/roue-1116/registre.txt && awk 'NF==3{n++} $2!=0{r++} END{print \"entrées=\"n, \"rouges=\"r}' work/portes/roue-1116/registre.txt && stat -c '%y %n' work/portes/roue-1116/registre.txt && ls tools/porte-*.sh | wc -l", "description": "Count registry entries and gates"}`

  ```
87 work/portes/roue-1116/registre.txt
entrées=86 rouges=5
2026-11-16 03:01:46.706529849 -0500 work/portes/roue-1116/registre.txt
86
  ```

- **bash** `{"command": "grep -nE 'indice|melange|produit|sessions|prechargement' docs/pilotage/references-non-regression.md | head -40", "description": "Check tolerated red gates"}`

  ```
3:> **Passe — 2026-11-15 09 h 53 → 12 h 15 :** **85 portes, 81 vertes, 4 rouges** — `indice` et
4:> `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prechargement`
9:> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
10:> `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
11:> `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
14:> **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
15:> heartbeat `e181ce02` rafraîchi) ; `porte-indice` et `porte-melange` restent **rouges
16:> structurelles** (indice 482 contre témoin 459 ; état de A sans son code). Journaux
21:> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
22:> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
24:> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
92:| `porte-homeostasie.sh` | 495 s | ✅ porte tenue (×0 exact · activité monotone · dominance reproduite) |
94:| `porte-indice.sh` | 913 s | ❌ l'indice extérieur
… [345 caractères tronqués]
  ```

- **bash** `{"command": "for n in porte-indice porte-melange porte-produit porte-sessions; do echo \"=== $n\"; tail -12 work/portes/roue-1116/$n.log; done", "description": "Read tails of the four red gates"}`

  ```
=== porte-indice
  écho     indice SÉMANTIQUE : l'état de la question, position 1469, aiguille en 669 :
  écho       épisode rendu : 1469 · recouvrement 64/64 · distance à l'aiguille : 800 jetons
  écho       hasard        : 370 jetons en moyenne sur 1470 épisodes
  écho       ⇒ la mémoire n'a PAS retrouvé l'aiguille : un indice qui ne ressemble pas au contenu cherché ne le retrouve pas. C'est une limite du rappel par le contenu — il n'est pas sémantique —, et elle est mesurée, pas supposée.
  écho   
  extérieur   indice SÉMANTIQUE : EXTÉRIEUR (/tmp/tmp.3sI30HizL0/etatB.1439, 896 valeurs) — il n'est PAS dans le magasin, aiguille en 669 :
  extérieur     épisode rendu : 187 · recouvrement 4/64 · distance à l'aiguille : 482 jetons
  extérieur     hasard        : 370 jetons en moyenne sur 1470 épisodes
  extérieur     ⇒ la mémoire n'a PAS retrouvé l'aiguille : un indice qui ne ressemble pas au contenu cherché ne le retrouve pas. C'est une limite du rappel par le contenu — il n'est pas sémantique —, et elle est mesurée, pas supposée.
  extérieur 
  ✅ indice interne : écho (64/64) — la mesure ne prouve RIEN, et c'est pourquoi la porte exige un indice extérieur
  ❌ l'indice extérieur to
… [1721 caractères tronqués]
  ```

- **bash** `{"command": "awk 'NF==3 && $2!=0 {print}' work/portes/roue-1116/registre.txt && echo '--- duplicates ---' && awk 'NF==3 {print $1}' work/portes/roue-1116/registre.txt | sort | uniq -d", "description": "List red entries and duplicates"}`

  ```
porte-indice 1 1127
porte-melange 1 149
porte-produit 1 187
porte-sessions 1 0
--- duplicates ---
  ```

- **bash** `{"command": "grep -nE '^porte-(indice|melange|produit|sessions|vision)' work/portes/roue-1116/registre.txt", "description": "Check specific gate entries"}`

  ```
33:porte-indice 1 1127
39:porte-melange 1 149
70:porte-produit 1 187
80:porte-sessions 1 0
86:porte-vision 0 661
  ```

- **bash** `{"command": "sed -n '1,220p' tools/porte-produit.sh", "description": "Read produit gate script"}`

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
… [5330 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /tmp/porte-produit-strict.log 2>/dev/null && cat /tmp/porte-produit-strict.log 2>/dev/null | tail -60", "description": "Read produit strict failure log"}`

  ```
-rw-r--r--. 1 stephane stephane 104 16 nov 02:58 /tmp/porte-produit-strict.log
.....
----------------------------------------------------------------------
Ran 5 tests in 10.864s

OK
  ```

- **bash** `{"command": "sed -n '1,80p' docs/methode/portes.md && echo '--- refs ---' && sed -n '1,60p' docs/pilotage/references-non-regression.md", "description": "Read doors method and tolerated red references"}`

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
… [7372 caractères tronqués]
  ```

- **bash** `{"command": "git log --date=iso --pretty='%h %ad %s' -20", "description": "Show commit dates"}`

  ```
ae3c24f2 2026-11-16 02:47:28 -0500 V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
2e617034 2026-11-16 02:10:08 -0500 EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)
1d4eb49e 2026-11-16 00:48:36 -0500 JOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4
c77ed4b6 2026-11-16 00:45:22 -0500 U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE
04894aea 2026-11-16 00:28:00 -0500 U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4)
75a56c05 2026-11-16 00:24:30 -0500 U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)
d19f0fc7 2026-11-16 00:19:47 -0500 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO
83adaa2b 2026-11-15 23:40:39 -0500 T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, Q
… [1874 caractères tronqués]
  ```

- **bash** `{"command": "git log --all --oneline --grep='V1\\|strict' | head -20 && echo '---' && git status --porcelain=v1 | head", "description": "Find V1 commit and working tree status"}`

  ```
ae3c24f2 V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
c37fed06 B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE
cb6ccab4 J14.1 — LA CLÔTURE : 84 PORTES, 81 VERTES, 3 ROUGES NOMMÉES (SESSIONS RÉPARÉE, INDICE ET MELANGE STRUCTURELLES) ; TAGS chantier-2026-11-14 ET semaine-2026-11-14 SUR 0e75f101 ; 28/28 ACCEPTATIONS ; RAPPORT + JSON
bb68b820 J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0089 APRÈS TOPO (p=0,86) ; FILIATION 61,4 % vs 50,0 % (HOLM 0,128), ÉPOQUE 56,8 % vs 53,8 % (p=0,373), ANNÉE INTRA-TRADITION R²=0,042 (HOLM 0,034) ; V150 β DATE −0,006 ≠ +0,138
03ecee41 J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ
229098ec J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COL
… [1629 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'evaluer\\|strict\\|Ran 5' /tmp/porte-produit-strict.log /tmp/porte-produit-tests.log 2>/dev/null | tail -20; stat -c '%y %n' /tmp/porte-produit-*.log 2>/dev/null", "description": "Check strict test logs timestamps"}`

  ```
/tmp/porte-produit-strict.log:3:Ran 5 tests in 10.864s
2026-11-16 03:01:07.813407092 -0500 /tmp/porte-produit-autotest.log
2026-11-15 04:44:37.562331054 -0500 /tmp/porte-produit-d1.log
2026-11-16 02:58:54.836987383 -0500 /tmp/porte-produit-exemples.log
2026-11-16 02:58:24.068890271 -0500 /tmp/porte-produit-libre.log
2026-11-07 12:33:49.751640355 -0500 /tmp/porte-produit-r035.log
2026-11-16 02:58:40.833943186 -0500 /tmp/porte-produit-restitution.log
2026-11-16 02:58:42.423948204 -0500 /tmp/porte-produit-restitution-v2.log
2026-11-16 02:58:44.027953267 -0500 /tmp/porte-produit-schema.log
2026-11-07 14:20:57.262275252 -0500 /tmp/porte-produit-schema-v2.log
2026-11-16 02:58:23.235887642 -0500 /tmp/porte-produit-strict.log
2026-11-16 02:58:12.188852774 -0500 /tmp/porte-produit-tests.log
2026-11-16 02:47:20.116786765 -0500 /tmp/porte-produit-v2b.log
2026-11-16 02:43:33.443065184 -0500 /tmp/porte-produit-v2.log
2026-11-16 02:58:23.579888727 -0500 /tmp/porte-produit-valide.log
  ```

- **bash** `{"command": "sed -n '1,200p' reports/rapport-cloture-chantier.md", "description": "Read previous closure report"}`

  ```
# J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag `chantier-2026-11-14`

> **Ligne de roadmap** : **B13** (le produit), **Panini**, **N2**, **S**, **R**, **A** · **Tâche** :
> J14.1 · **Date** : 2026-11-14 · **Verdict** : ✅
>
> **Ce que ce rapport est.** La **clôture** du chantier, **sans relancer la passe complète** : la
> passe de référence est celle du **14/11 00 h 30** (`work/portes/passe-1311-23h15.log`) —
> **84 portes, 81 vertes, 3 rouges nommées**. J14.1 **rejoue les trois rouges** (`indice`,
> `melange`, `sessions`), met à jour [`references-non-regression.md`](../docs/pilotage/references-non-regression.md),
> pose le **tag annoté** `chantier-2026-11-14` sur le dernier commit vert, et écrit cette fiche.
> Il **ne refait pas** les 81 vertes : ce serait une seconde passe, et le mandat l'interdit.
>
> **Le chiffre.** **84 / 81 / 3** reste le relevé. Après vérification ciblée : `porte-sessions`
> passe **verte** (20 s), `porte-indice` et `porte-melange` restent **rouges structurelles**. Le tag
> `chantier-2026-11-14` est posé sur **`0e75f101`** (J13.1), avec le tag de semaine
> `semaine-2026-11-14` que J5.2 n'avait pas posé : l'échec est **réparé**, pas effa
… [12770 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/rapport-cloture-chantier.json'\nd=json.load(open(p))\nprint(json.dumps(d, indent=1, ensure_ascii=False)[:6000])\nPY", "description": "Inspect previous closure JSON structure"}`

  ```
{
 "schema": "drave.cloture-chantier",
 "version": 1,
 "titre": "J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag chantier-2026-11-14",
 "sous_titre": "Sans relancer la passe complète : vérification ciblée des trois rouges, références, tags annotés, bilan de clôture",
 "date": "2026-11-14",
 "tache": "J14.1",
 "statut": "cloture",
 "head": "0e75f101",
 "lignes_roadmap": [
  "B13",
  "Panini",
  "N2",
  "S",
  "R",
  "A"
 ],
 "principe": "La passe de référence du 14/11 00 h 30 (84/81/3) n'est pas refaite ; seules les trois rouges sont rejouées. Les chiffres de produit, de tagger et de Panini sont ceux de J13.1 et de leurs fiches, pas de nouvelles mesures.",
 "passe": {
  "lancee": "2026-11-13 23:15 HNE",
  "fin": "2026-11-14 00:30 HNE",
  "portes": 84,
  "vertes": 81,
  "rouges": 3,
  "refaite": false,
  "log": "work/portes/passe-1311-23h15.log",
  "journaux": "work/portes/passe-1311-23h15",
  "rouges_detail": [
   {
    "porte": "indice",
    "code": 1,
    "duree_s": 875,
    "cause": "indice extérieur à 482 jetons de l'aiguille, témoin à 459, hasard 370 : écart nul ou négatif"
   },
   {
    "porte": "melange",
    "code": 1,
    "duree_s": 111,
    "cause": "l
… [4800 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable.md</path>
<type>file</type>
<content>
1: # T6 — le bilan exploitable : installable, rejouable, mesuré, mais pas encore général
2: 
3: > **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **T6** (clôture de la nuit
4: > exploitable) · **Date** : 2026-11-15 · **Verdict** : ✅ **les cinq briques T1–T5 tiennent
5: > ensemble** ; ❌ **trois limites restent nommées et bornées** (clone public dégradé, croissance
6: > O(k²), or de rôles humain absent).
7: >
8: > **Le chiffre, en une ligne.** Un débutant installe **`drave 0.1.0`** en **13,64 s** de machine
9: > (`pip install -e .`), lance **3/3** commandes, obtient un JSON **v2** de **5 899 octets** avec
10: > **2 139** candidats objets et **8** rôles normalisés ; **10 000 mots** passent en **4,01 s**
11: > (**2 493 mots/s**, **126 Mio**, **14,8 Mo** de JSON) ; la CLI rend **20/20** cas et **cinq
12: > codes** (0/3/4/5/1). Le **contrôle de linéarité échoue** (α = **1,55**), le **clone public**
13: > perd le sous-module S (attachement **88,70 %** au lieu de **99,58 %**), et le **gold de S**
14: > n'est pas un or humain indépendant. La passe complète 
… [21640 caractères tronqués]
  ```

- **bash** `{"command": "for f in rapport-performance-fix rapport-roue rapport-profils rapport-evaluer-strict rapport-exemples-v2; do echo \"===== $f.md =====\"; sed -n '1,60p' reports/$f.md; done", "description": "Read headers of U/V fiches"}`

  ```
===== rapport-performance-fix.md =====
# U1 — les deux O(k²) sont bornés : 10 000 mots de **4,0 s à 0,82 s** (×4,9), α de **1,53 à 1,08**, sorties **identiques au bit près**

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **U1** (exploitable, suite de T4) ·
> **Date** : 2026-11-16 · **Verdict** : ✅ **le contrôle de linéarité passe** — α = **1,076**
> (objectif ≤ 1,15), le terme quadratique n'ajoute que **+0,00077 de R²** (contre +0,041
> avant), et **les sorties sont identiques** : 612 phrases du gold, 452 réelles, 10 000 mots,
> sept blocs contrôlés, **diff vide**. Le temps de la fonction sur 10 000 mots passe de
> **3,991 s à 0,816 s** (×4,9) ; la mémoire reste au même niveau (**127,4 Mio** contre
> **126,9 Mio**), le JSON est **octet pour octet** le même (14 795 890 octets).
>
> **Les deux points de T4.** `_groupes_partition` comparait **toutes les paires** de
> syntagmes (O(k²)) ; il balaie maintenant les intervalles triés par début (O(k log k)).
> `_cible_proche` filtrait puis **triait tous les GV** pour chaque segment ; un **index**
> rend les GV par distance croissante en O(log m + candidats examinés). Le profil a ensuite
> nommé trois autres boucles quadratiques, 
… [16809 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,160p' reports/rapport-performance-fix.md", "description": "Read U1 10k and controls"}`

  ```
## 2. Les 10 000 mots

Sur le préfixe exact de 10 000 mots de `data/corpus_fr_litterature.txt` (sha256
`0069b20e…e08871`), même texte, même JSON :

| mesure | avant | après | écart |
|---|---:|---:|---:|
| fonction `Heuristique.analyser` | **3,991 s** | **0,816 s** | **×4,89** |
| débit (fonction) | 2 506 mots/s | **12 259 mots/s** | ×4,89 |
| CLI `--json` | 5,011 s | **1,668 s** | ×3,00 |
| sérialisation JSON seule | 0,628 s | 0,628 s | ×1,00 |
| pic RSS (fonction) | 129 936 Ko (126,9 Mio) | 130 452 Ko (**127,4 Mio**) | +0,5 Mio |
| pic RSS (CLI) | 171 316 Ko (167,3 Mio) | 171 864 Ko (167,8 Mio) | +0,5 Mio |
| JSON indenté | 14 795 890 octets | **14 795 890 octets** | **identique** |
| étiquettes / syntagmes | 54 522 / 2 726 | 54 522 / 2 726 | identique |

Le CLI ne gagne « que » ×3 parce que les **0,63 s de `json.dumps`** et le démarrage ne
baissent pas ; c'est la fonction qui porte le gain. La mémoire ne baisse pas : les index
ajoutent environ **0,5 Mio** (trois listes triées + un arbre de segments par liste de GV),
soit **+0,4 %** — le prix du temps linéaire.

## 3. Le gold 612 / 452 — mêmes chiffres, au bit près

Les annotations canoniques (JSON trié, sans durée) des **612** p
… [5799 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '55,200p' reports/rapport-roue.md", "description": "Read U2 controls and negatives"}`

  ```
```

- **Python** 3.13.16 ; pip du venv **26.2.1** (pip système 26.2.2) ; **setuptools** 84.0.0.
- **`--no-build-isolation`** : le build utilise le setuptools déjà installé ; avec l'isolation,
  pip doit installer `setuptools>=61`, donc réseau ou cache.
- **`--no-index --no-deps --no-cache-dir`** : l'installation ne peut venir que du fichier, et
  aucune dépendance n'est résolue (le projet n'en a aucune).
- **`HOME=/tmp/drave-home`** et variables `*_API_KEY` / `*_KEY_FILE` retirées : le tagger sans
  clé est reproductible.
- **`cd /tmp`** pour tous les contrôles : la commande installée ne dépend pas du répertoire.

## 3. Ce que la roue contient

| famille | contenu | preuve |
|---|---|---|
| le CLI | `tools/drave.py` + les modules racine de `tools/` | `drave --version` → `drave 0.1.0` |
| la mesure | `tools/tests/linguistique/{evaluer_gold,miroir}.py` | `drave evaluer --json` → 0 |
| les **gold** | `gold.json`, `gold_gele.json`, `gold_reel.json`, `gold_restitution_v2.json`, `gold_synthetique.json` | gold 612 / gelé 602 / réel 452 |
| le générateur S | `tools/structures/generateur.py` (sous-module **648adce3**) | `rôle=agent` sur « Le chat dort. », comme le dépôt |
| le tagger (opti
… [6752 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,190p' reports/rapport-profils.md", "description": "Read U3 measure and negatives"}`

  ```
un effacement.

**Deux chemins, et `source` le dit.** Sur un texte **long** (> 80 caractères), les 398 profils
de trigrammes. Sur un texte **court**, les profils se recouvrent (398 langues, quelques
trigrammes) : le **prior des mots-outils** des sept langues du bloc peut trancher
(`source: lexique`, `prior: {langue, score}`), et les `candidats` restent les profils — le
désaccord est visible, pas masqué. Un texte de **moins de cinq mots** qui passe par les profils est pénalisé
(confiance × mots / 5) pour qu'un mot isolé ne devienne pas une langue.

**Codes de sortie.** `0` succès, `3` refus (texte vide ou sans lettre/chiffre), `4` artefact
de profils absent ou illisible, `5` usage (`TEXTE` et `--texte` ensemble, seuil hors `[0,1]`,
fichier répertoire). Sans l'artefact, `stdout` reste vide, le message nomme le fichier et les
deux issues (réinstaller la roue, ou lancer le constructeur).

## 3. La mesure — les 20 langues de l'échantillon UDHR

L'échantillon est celui de [`rapport-corpus-commun.md`](rapport-corpus-commun.md) § 3 : **20
langues stratifiées** (5 familles × 4, 10 écritures), choisies pour l'égalité exacte de
l'article 1 des deux côtés. On garde le **fichier** exact (`udhr_
… [6746 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,200p' reports/rapport-evaluer-strict.md", "description": "Read V1 real gold and negative control"}`

  ```
### 3.2 Gold réel 452

| mode | POS | ΔPOS | syntagmes F1 | ΔF1 | tête F1 | Δtête | acte | attachement exact |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **heuristique** | **0,8891** | — | **0,7906** | — | **0,8990** | — | 0,9956 | 0,9946 |
| neuronal (`MockNeuronal`) | 0,7621 | −12,70 pts | 0,7448 | −4,58 pts | 0,8697 | −2,93 pts | 0,9956 | 0,0000 |
| parallèle | 0,8891 | +0,00 pt | 0,7906 | +0,00 pt | 0,8990 | +0,00 pt | 0,9956 | 0,9946 |
| **cascade** | **0,8891** | **+0,00 pt** | **0,7906** | **+0,00 pt** | **0,8990** | **+0,00 pt** | 0,9956 | 0,9946 |

Les 452 appels neuronaux ne changent pas les labels : la cascade réelle est **l'heuristique
avec un appel neuronal dominé**. C'est le fait que le mode strict publie, pas un gain caché.

## 4. Le plancher et le code de sortie

| gold | cascade POS | plancher | marge | verdict |
|---|---:|---:|---:|---|
| **vivant 612** | **0,8625** | 0,70 | **+16,25 pts** | ✅ |
| **réel 452** | **0,8891** | 0,70 | **+18,91 pts** | ✅ |

La commande sort **0** parce que les deux mesures passent. Le plancher n'est pas un
affichage : c'est la condition du code de retour, et le test vérifie qu'un verdict faux rend
**1** (injection d'un rapport `o
… [2754 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '55,220p' reports/rapport-exemples-v2.md", "description": "Read V2 details and limits"}`

  ```
```diff
-      "role": "groupe nominal",
+      "role": "objet",
...
-      "role": "qualité",
+      "role": "qualite",
...
-      "role": "prédicat",
+      "role": "predicat",
```

### 2.3 `r035` — mêmes rôles, même relative zéro

La REL `she talks about [9:24] → film` est toujours prédite ; le gold à trois spans est toujours
exact. Les trois rôles passent par la même table que `r241` (`groupe nominal` → `objet`,
`qualité` → `qualite`, `prédicat` → `predicat`). Aucun span, aucune cible ne bouge.

## 3. Les candidats objets et les rôles

Le champ historique `candidats` reste une liste de **chaînes** ; `meta.attachement.candidats`
publie les mêmes candidats en **objets** `{span, cible, source}`. Sur les quatre textes des blocs
JSON (`g001`, `g011`, `r241`, `r035`) :

| invariant | valeur | contrôle |
|---|---:|---|
| candidats objets | **18** | `tools/verifie_exemples.py` |
| spans exacts (`texte[debut:fin] == cible`) | **18/18** | le script, sur chaque objet |
| candidats non objets | **0** | le script refuse une chaîne |
| rôles publiés | **4** (`agent`, `predicat`, `objet`, `qualite`) | tous dans les **8** du vocabulaire |
| rôles hors vocabulaire | **0** | `roles_vocabulaire.R
… [4163 caractères tronqués]
  ```

- **bash** `{"command": "grep -nE '\\bV3\\b|9 tâches|neuf tâches|T/U/V|bilan exploitable 2|exploitable-2|exploitable-2026' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | tail -30", "description": "Search session digest for V3 plan"}`

  ```
42063:CORRECTIF PROPOSÉ (pseudo-code précis dans la fiche, non appliqué) : dans `Heuristique.analyser` (section 5, lignes 853–941) hoister `simples = self._syntagmes_simple(texte, lg)` et `gvs_simple` une seule fois ; créer `cache_gv = {}` local à l'analyse ; ajouter `_verbe_gv(texte, g, verbes, cache_gv)` et le passer à `_cible_proche`/`_verbes_proches` (remplacer les appels 681/685/701) ; remplacer les sites 861/914/916/919/928/929-930 et passer `cache_gv` aux appels 887/895/899/916/922/935/940. Effet attendu : 1+2S → 1 chunking, S·G appels de verbe → ≤G, sortie identique. Limite : le tri par segment reste ; V3 (index+bisect) et V4 (tri fusionné) testés sur l'instantané antérieur, plus lents et V3 1 divergence/612, non retenus.
42091:- **Limite** : le `sorted(gvs, key=ecart)` par segment reste ; le cache ne rend pas la courbe strictement linéaire. V3 (index+bisect) et V4 (tri fusionné) testés, plus lents, non retenus ; V3 avait 1 divergence/612.
42759:dcf7bc91 B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS 29/29 = 1,0 ; R2/R3/R4 DE A9 ; 181/181
43109:- CONCURRENCE IMPORTANTE : après les mesures, le dépôt est passé à la V3 (dcf7bc91, 15:18) : exact 141/145, top1 143, noms 29
… [4864 caractères tronqués]
  ```

- **bash** `{"command": "grep -nE '\\bV3\\b|9 tâches|neuf tâches|T/U/V|exploitable-2|exploitable-2026' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md | tail -30", "description": "Search session report for V3 plan"}`

  ```
9725:- **A23** : **29 tâches** inventoriées (8 autonomes, 11 en coordination, 10 bloquées), **18 périmées** signalées, **6 doublons**.
9801:**29 tâches** : **8 autonomes** (exécutées en grande partie), **11 en coordination**, **10 bloquées** ; **18 mentions périmées** corrigées dans les documents. L'audit de fiabilité (A24) a mesuré **50 phrases libres** : **0 plantage**, mais **132 paires de syntagmes qui se chevauchent** (51,9 % des étiquettes, dues au générateur S + l'union) et **18 correctifs**
11395:- B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS 29/29 = 1,0 ; R2/R3/R4 DE A9 ; 181/181" -- tools/bloc_linguistique.py tools/pensee/autotest.py reports/rapp
11402:- B13 — L'ANGLAIS EST LE TROU (60/94 SPANS, S NE SEGMENTE PAS L'ANGLAIS) ; TABLEAU V3 RÉPARÉ ; 182/182" -- reports/rapport-gold-anglais.md reports/rapport-pensee-
  ```

- **bash** `{"command": "sed -n '66600,66820p' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md", "description": "Read session digest around V2/V3 orchestration"}`

  ```
- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git branch -f master s/v7 && timeout 280 git push origin s/v7 2>&1 | tail -1; timeout 280 git push origin master 2>&1 | tail -1; sleep 900; date; tail -2 work/chantier/journal.log; ls reports/rapport-roue.md 2>/dev/null", "descriptio … [49 caractères tronqués]`

  ```
04894aea..1d4eb49e  s/v7 -> s/v7
   04894aea..1d4eb49e  master -> master
[still running after 600000ms; moved to background job bash-5231]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-5231", "timeout_ms": 600000, "wait": true}`

  ```
lun 16 nov 2026 01:30:38 EST
2026-11-16 00:31:30 · ✔ U1 en 2852.4 s (code 0) — ✅ test -f reports/rapport-performance-fix.md && echo FICHE-OK; ✅ python3 tools/tests/test_produit.py 2>&1 | tail -1
2026-11-16 00:31:30 · ▶ U2 — L'empaquetage — la roue et le README (timeout 3600 s)
reports/rapport-roue.md
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 600; date; tail -2 work/chantier/journal.log; git 
… [7353 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'V3 —\\|V3 -\\|rapport-bilan-exploitable-2\\|bilan exploitable 2\\|LA CLÔTURE DE LA NUIT\\|clôture de la nuit' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | tail -40", "description": "Find V3 plan lines in digest"}`

  ```
48753:3ab768f7 B13 — LA CLÔTURE DE LA NUIT : EXACT 221/221, COUVERTURE 0,9247, DEV 152/152, TEST 69/69 ; 18 SPANS DONT 17 INATTEIGNABLES
66503:> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **T6** (clôture de la nuit
66746:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 1800; date; tail -3 work/chantier/journal.log; git rev-list --count origin/master..s/v7; ls reports/rapport-exemples-v2.md reports/rapport-bilan-exploitable-2.md 2>/dev/null", "description": "Suivre V2/V3", "timeoutMs": 1900000 … [1 caractères tronqués]`
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nprint(type(d), d.keys() if isinstance(d,dict) else len(d))\nif isinstance(d,dict):\n    for k,v in d.items():\n        print(k, type(v), len(v) if hasattr(v,'__len__') else '')\nPY", "description": "Inspect ch … [18 caractères tronqués]`

  ```
<class 'dict'> dict_keys(['nom', 'principe', 'taches'])
nom <class 'str'> 58
principe <class 'str'> 93
taches <class 'list'> 63
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d['taches']:\n    print(t.get('id'), '|', t.get('jour'), '|', t.get('titre'))\nPY", "description": "List all planned tasks"}`

  ```
J0 | 0 | Le contrôle du superviseur
J1.1 | 1 | r035 : la relative zéro
J1.2 | 1 | La convention des GV
J1.3 | 1 | Le schéma v2
J1.4 | 1 | La restitution v0
J2.1 | 2 | Panini I — la table atomes ↔ niveaux
J2.2 | 2 | Panini I — le corpus commun
J3.1 | 3 | Panini II — le retrieval à époque contrôlée
J3.2 | 3 | Panini II — la généalogie à deux faces
J4.1 | 4 | Coordination N2 — le mètre RoPE
J4.2 | 4 | Coordination S — les 11 verdicts
J4.3 | 4 | Coordination R — le tagger sur 612
J4.4 | 4 | Coordination A — A6.2 et A8.3b2
J5.1 | 5 | Le rapport de semaine
J5.2 | 5 | La passe complète et le tag
J6.1 | 6 | Le dernier span g017
J6.2 | 6 | La cible s065
J7.1 | 7 | Panini — le retrieval approfondi
J8.1 | 8 | La restitution v1
J9.1 | 9 | La passe d'honnêteté des fiches
J10.1 | 10 | Le bilan de la semaine
J11.1 | 11 | Le produit — les exemples rejoués
J11.2 | 11 | Le produit — la mesure par langue
J11.3 | 11 | Le produit — la robustesse des 50 textes
J11.4 | 11 | Le contrat — le schéma v2 documenté
J12.1 | 12 | Panini — le §334 et les 44 œuvres
J12.2 | 12 | Panini — le corpus d'or CIC
J13.1 | 13 | Les bilans — la table des mesures
J14.1 | 14 | La clôture — la passe et le tag
C1 | 15 | Coordina
… [1565 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d['taches']:\n    if t.get('id') in ('T1','T2','T3','T4','T5','T6','U1','U2','U3','V1','V2','V3'):\n        print('='*70)\n        print(json.dumps(t, ensure_ascii=False, indent=1))\nPY", "description … [33 caractères tronqués]`

  ```
======================================================================
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
=======================
… [9835 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S %Z' && sed -n '1,160p' tools/porte-sessions.sh", "description": "Check time and sessions gate logic"}`

  ```
2026-11-16 03:03:54 EST
#!/bin/bash
# porte-sessions.sh — les plans de session sont lisibles et le linter refuse un doublon.
set -u
cd "$(dirname "$0")/.."
python3 tools/sessions.py --autotest || exit 1
python3 tools/sessions.py --check --strict || exit 1
echo "PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict"
  ```

- **bash** `{"command": "grep -n 'heartbeat\\|périmé\\|122' tools/sessions.py | head -40 && grep -n 'Heartbeat\\|heartbeat' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "description": "Inspect sessions heartbeat logic"}`

  ```
5:périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
8:et les heartbeats périmés (le `--check` seul les signale). Les **fichiers
16:l'état, son heartbeat n'est plus exigé, et la reprise la remet `actif`.
18:`work/ressources.json` : le heartbeat n'est pas exigé ; le registre distingue le
34:CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
71:    hb = champs.get("heartbeat", "")
72:    heartbeat = None
77:            heartbeat = datetime.fromisoformat(brut)
79:            heartbeat = datetime.strptime(brut, "%Y-%m-%d %H:%M")
80:        age = (datetime.now() - heartbeat).total_seconds() / 60.0
84:            "fichiers": fic, "heartbeat": heartbeat, "age": age,
113:    heartbeat = f"{m.group(1)} {int(m.group(2)):02d}:{m.group(3)} HAE" if m else ""
124:                    "heartbeat": heartbeat})
136:        heartbeat = s["heartbeat"] or datetime.now().strftime("%Y-%m-%d %H:%M HAE")
143:> session : le heartbeat est celui de l'état, pas une preuve de vie.
149:- **Heartbeat** : {heartbeat}
187:            erreurs.append(f"{p['chemin']} : heartbeat illisible")
195:                    f"mandat long ({a['age']:.0f} min) : {a['id']} — claim 
… [732 caractères tronqués]
  ```

- **bash** `{"command": "git status --porcelain=v1 | head -30 && echo '--- work tracked? ---' && git ls-files work/portes/roue-1116 | head", "description": "Check working tree and tracked door logs"}`

  ```
--- work tracked? ---
  ```

- **bash** `{"command": "python3 tools/sessions.py --status 2>&1 | tail -40; echo '--- check ---'; python3 tools/sessions.py --check --strict; echo CODE-$?", "description": "Check session status and strict check"}`

  ```
sessions · plans de mandat
    0733c5bb-f90b-4f58 · terminé  · 15402 min · N2 (200 000 pas sur le mélange, PPL domaine/littérature/anglais/wikitext2, courbe de longueur), R1.1/R1.2 mesurés depuis N2
      → **surveiller les runs relancés à 09 h 30** — `kd2` (gpu0, chargement du corpus) et `rope2048` (gpu1, en cours) ; puis mesurer et committer ; ensuite la **porte propre (0,29)**.
    0b0a6a0d-05f5-4308 · terminé  · 21269 min · N2.h — corpus propre, porte honnête, généralité, verrou de longueur
      → close — N2.i (3,13 / 12,93 / 33,83) et Pensée v0 (6/6 portes) sont committés.
    0b69f616-5c75-4c34 · terminé  · 23343 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
    1e7ef596-93e6-45f1 · en pause · 15909 min · docs/pilotage/` (en-cours, roadmap, chantiers, plan-travail, références), journal/` (hors `sessions/<id>/`), reports/README.md, reports/INDEX.md, tools/sessions.py, tools/ressources.py, tools/index_reports.py, tools/surveille_sessions.py, l'index git.
      → **suivi docs** (N3 intégré, état au 04/11), puis la **passe** après les runs.
    22e518ee-81b8-4081 · terminé  · 22514 min · a
… [2881 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '160,215p' tools/sessions.py && grep -n 'SEUIL\\|180\\|120\\|age' tools/sessions.py | head -20", "description": "Read mandatory heartbeat threshold"}`

  ```
chemin = racine / "work/ressources.json"
    if not chemin.exists():
        return set()
    try:
        data = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return {str(c.get("session", "")) for c in data.get("claims", []) if c.get("session")}


def verifier(racine: Path, strict: bool = False) -> tuple[list[str], list[str]]:
    erreurs: list[str] = []
    avertissements: list[str] = []
    plans = decouvrir(racine)
    actifs = [p for p in plans if p["etat"] in ACTIFS]
    claims = sessions_avec_claim(racine)
    vus: dict[str, str] = {}
    for p in plans:
        manquants = [c for c in CHAMPS if c not in p["champs"]]
        if manquants:
            erreurs.append(f"{p['chemin']} : champ(s) manquant(s) — {', '.join(manquants)}")
        if p["etat"] not in ETATS_CONNUS:
            erreurs.append(f"{p['chemin']} : état inconnu {p['etat']!r}")
        if p["etat"] in A_CONFIRMER:
            (erreurs if strict else avertissements).append(
                f"plan à confirmer : {p['id']} — la session doit le compléter")
        if p["age"] is None:
            erreurs.append(f"{p['chemin']} : heartbeat illisi
… [2399 caractères tronqués]
  ```

- **bash** `{"command": "ps -ef | grep -E 'chantier|supervise|plan.json|drave' | grep -v grep | head -20; echo '---'; tail -8 work/chantier/journal.log 2>/dev/null; echo '---'; ls -la work/chantier | head", "description": "Check for running supervisor and chantier log"}`

  ```
stephane 1504202    2886  0 02:13 ?        00:00:00 timeout 18000 python3 tools/chantier/superviseur.py boucle --budget 36000 --timeout 3000
stephane 1504204 1504202  0 02:13 ?        00:00:04 python3 tools/chantier/superviseur.py boucle --budget 36000 --timeout 3000
stephane 1638979  264909  0 02:38 ?        00:00:00 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 1800; date; tail -3 work/chantier/journal.log; git rev-list --count origin/master..s/v7; ls reports/rapport-exemples-v2.md reports/rapport-bilan-exploitable-2.md 2>/dev/null
---
2026-11-16 01:31:30 · ✔ U2 en 3600.1 s (code 124) — ✅ test -f reports/rapport-roue.md && echo FICHE-OK
2026-11-16 01:31:31 · ▶ U3 — La CLI — les profils de langue (timeout 3600 s)
2026-11-16 02:02:54 · ✔ U3 en 1883.2 s (code 0) — ✅ test -f reports/rapport-profils.md && echo FICHE-OK
2026-11-16 02:13:25 · ▶ V1 — Le banc — evaluer --strict (timeout 3000 s)
2026-11-16 02:29:02 · ✔ V1 en 932.3 s (code 0) — ✅ test -f reports/rapport-evaluer-strict.md && echo FICHE-OK; ✅ python3 tools/drave.py evaluer --strict >/dev/null 2>&1; echo STRICT-$?
2026-11-16 02:29:02 · ▶ V2 — Les exemples — le JSON de la v2 (timeout 3000 s)
2026-11-16 03:
… [788 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat --oneline HEAD | head -40 && echo '---' && git show --stat --oneline HEAD~1 | head -20", "description": "Inspect V2 and U3 commit stats"}`

  ```
ae3c24f2 V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
 docs/implantation/bloc-linguistique.md             |   13 +
 docs/pilotage/en-cours.md                          |   14 +-
 docs/pilotage/roadmap.md                           |   25 +-
 docs/produit/README.md                             |  165 +-
 docs/produit/demarrage.md                          |   38 +-
 docs/produit/exemples.md                           |  299 +-
 journal/2026-11-16/README.md                       |   25 +-
 journal/2026-11-16/docs.md                         |   21 +-
 journal/2026-11-16/memoire.md                      |    2 +-
 journal/2026-11-16/mesures.md                      |    2 +-
 journal/2026-11-16/moteur.md                       |   19 +
 journal/README.md                                  |    6 +-
 journal/THEMES.md                                  |    1 +
 journal/sessions/MANIFEST.md                       |    6 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   59 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 32
… [2411 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/chantier/superviseur.py", "description": "Inspect supervisor behavior"}`

  ```
#!/usr/bin/env python3
"""superviseur.py — le méta-harnais du chantier autonome : file de tâches, exécution, vérification.

**Le problème.** DSH donne l'**agent** : des rounds, une session reprenable (`--session-id`), la
compaction du contexte, des sous-agents. Il **ne donne pas** la couche de contrôle d'un chantier de
plusieurs jours : file de tâches persistante, vérification d'acceptation **indépendante** de
l'agent, budget, reprise après crash, escalade, journal d'audit. Ce superviseur est cette couche.

**Les trois garanties.**
1. **Une tâche n'est finie que si son acceptation passe** — une commande, un attendu, exécutés par
   le superviseur, pas par l'agent.
2. **Rien n'est perdu** : l'état (`work/chantier/etat.json`) et le journal (`work/chantier/journal.log`)
   sont écrits après **chaque** étape ; une relance reprend la première tâche non finie.
3. **On s'arrête proprement** : le fichier `work/chantier/STOP` (ou le budget, ou le nombre de
   tâches) arrête la boucle ; l'agent n'est jamais tué au milieu d'un commit.

**Usage.**
    python3 tools/chantier/superviseur.py etat          # où en est-on ?
    python3 tools/chantier/superviseur.py prochaine     # la prochaine tâch
… [7350 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '200,360p' tools/chantier/superviseur.py", "description": "Read supervisor loop and commit checks"}`

  ```
plan, etat = charger_plan(), charger_etat()
    if STOP.exists():
        print("STOP présent : on ne lance rien.")
        return 3
    avant = git_avant()
    if avant["modifies"]:
        print(f"note : {len(avant['modifies'])} fichier(s) déjà modifié(s) (autres sessions) — on continue.")
    file = taches_en_file(plan, etat)
    if not file:
        print("file vide.")
        return 0
    if args.id:
        choisie = [x for x in file if x["id"] == args.id]
        if not choisie:
            print(f"{args.id} n'est pas en file (fait, bloquée ou absente) — « reprendre {args.id} » pour la remettre.")
            return 5
        t = choisie[0]
    else:
        t = file[0]
    resultat = executer_tache(t, etat, args.timeout)
    apres = subprocess.run(["git", "rev-parse", "HEAD"], cwd=RACINE,
                           capture_output=True, text=True).stdout.strip()
    resultat["head_avant"] = avant["head"][:10]
    resultat["head_apres"] = apres[:10]
    resultat["commit_produit"] = apres != avant["head"]
    etat["taches"][t["id"]] = {"titre": t["titre"], **resultat}
    etat["budget_s"] = etat.get("budget_s", 0) + resultat["duree_s"]
    etat["lancements"] = etat.get("lancem
… [3703 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/revue_documentation.py", "description": "Inspect documentation review checks"}`

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
… [7540 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/verifie_en_cours.py && echo '---' && sed -n '1,120p' tools/taille_documents.py", "description": "Inspect state length checks"}`

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
… [9945 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/README.md && echo '--- INDEX head ---' && sed -n '1,40p' reports/INDEX.md", "description": "Read reports index format"}`

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
| [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) | **Bilan** — la semaine 07 → 15/11 : le produit, Panini, la coordination, le harnais |
| [`rapport-bilan-nuit.md`](r
… [12192 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,100p' tools/index_reports.py", "description": "Inspect report index generator"}`

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
… [1392 caractères tronqués]
  ```

- **todo_write** `{"todos": [{"content": "Rassembler les chiffres T1–T6, U1–U3, V1–V2 et le relevé des portes", "status": "in_progress"}, {"content": "Vérifier les deux rouges non structurelles (produit, sessions) sans relancer la passe", "status": "pending"}, {"content": "Écrire reports/rapport-bilan-exploitable-2.m … [422 caractères tronqués]`

  ```
Updated todo list: 6 pending, 1 in progress, 0 completed.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "old_string": "- **Heartbeat** : 2026-11-16 00:45 EST\n- **Prochaine action** : **U3 — `--profils`** ; **U1** (α **1,08**, 10 000 mots **0,82 s**, sorties identiques ; [fich … [662 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md has been updated successfully.
  ```

- **bash** `{"command": "mkdir -p work/portes/verif-cloture-1116 && { time bash tools/porte-sessions.sh; } > work/portes/verif-cloture-1116/porte-sessions.log 2>&1; code=$?; echo \"porte-sessions $code\" >> work/portes/verif-cloture-1116/registre.txt; echo \"CODE=$code\"; tail -8 work/portes/verif-cloture-1116/ … [80 caractères tronqués]`

  ```
CODE=0
autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé, mandat long avec claim accepté, reservation imbriquée avertie sans refus
  ✅ plans cohérents
PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict

real	0m0,202s
user	0m0,163s
sys	0m0,033s
  ```

- **bash** `{"command": "mkdir -p work/portes/verif-cloture-1116 && { time bash tools/porte-produit.sh; } > work/portes/verif-cloture-1116/porte-produit.log 2>&1; code=$?; echo \"porte-produit $code\" >> work/portes/verif-cloture-1116/registre.txt; echo \"CODE=$code\"; tail -20 work/portes/verif-cloture-1116/po … [91 caractères tronqués]`

  ```
started background job bash-60
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nr=pathlib.Path('.')\nprint('portes', len(list((r/'tools').glob('porte-*.sh'))))\nprint('chapitres', len(list((r/'docs/theorie/synthese').glob('0*.md'))))\ndef est_carte(p): return p.parent.name=='entrees' and p.parent.parent.name=='glossaire'\ndocs=[p f … [311 caractères tronqués]`

  ```
portes 86
chapitres 8
docs 125
reports md 770
reports json 865
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['reports/rapport-bilan-exploitable.json','reports/performance-fix.json','reports/roue.json','reports/profils.json','reports/evaluer-strict.json','reports/rapport-exemples-v2.json']:\n    try:\n        d=json.load(open(f))\n        print(f, '=>',  … [171 caractères tronqués]`

  ```
reports/rapport-bilan-exploitable.json => drave.bilan-exploitable 1 | T6 — le bilan exploitable : installable, rejouable, mesuré, mais pas encore géné
reports/performance-fix.json => drave.performance.fix 1 | 
reports/roue.json => drave.roue.verification 1 | 
reports/profils.json => drave.profils.mesure 1 | 
reports/evaluer-strict.json => None 0.1.0 | 
reports/rapport-exemples-v2.json => None None | Les exemples de la doc — rejeu v2
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-bilan-exploitable.json'))\nprint(list(d.keys()))\nfor k,v in d.items():\n    print('---',k, type(v).__name__)\n    if isinstance(v,(dict,list)):\n        print(json.dumps(v, ensure_ascii=False, indent=1)[:1500])\n    else: … [75 caractères tronqués]`

  ```
['schema', 'version', 'titre', 'date', 'tache', 'statut', 'lignes_roadmap', 'principe', 'sources', 'installable', 'quickstart', 'api_json', 'performance', 'codes_sortie', 'portes', 'negatifs', 'reste', 'suite', 'limites', 'fichiers', 'verdict']
--- schema str
'drave.bilan-exploitable'
--- version int
1
--- titre str
'T6 — le bilan exploitable : installable, rejouable, mesuré, mais pas encore général'
--- date str
'2026-11-15'
--- tache str
'T6'
--- statut str
'cloture'
--- lignes_roadmap list
[
 "B13",
 "R0.7",
 "S",
 "Panini"
]
--- principe str
"Aucune mesure nouvelle : ce bilan relit les fiches T1-T5, leurs JSON et les registres de portes. La passe complète n'est pas relancée."
--- sources list
[
 {
  "tache": "T1",
  "titre": "l'empaquetage",
  "fiche": "reports/rapport-empaquetage.md",
  "json": "reports/empaquetage.json",
  "commit": "7f1519f7"
 },
 {
  "tache": "T2",
  "titre": "l'API du JSON",
  "fiche": "reports/rapport-contrat-json.md",
  "json": "reports/contrat-json.json",
  "commit": "7f1519f7"
 },
 {
  "tache": "T3",
  "titre": "le quickstart",
  "fiche": "reports/rapport-quickstart.md",
  "json": "reports/quickstart.json",
  "commit": "7d114559"
 },
 {
  "tache": "T4"
… [13882 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-60", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sed -n '1,70p' docs/pilotage/roadmap.md && echo '--- 120-190 ---' && sed -n '120,190p' docs/pilotage/roadmap.md", "description": "Read roadmap structure around exploitable"}`

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
… [20026 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-60", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sleep 30; tail -4 work/portes/verif-cloture-1116/porte-produit.log 2>/dev/null; cat work/portes/verif-cloture-1116/registre.txt 2>/dev/null", "description": "Check targeted produit gate progress"}`

  ```
✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
porte-sessions 0
  ```

- **bash** `{"command": "sed -n '1,30p' docs/pilotage/references-non-regression.md", "description": "Read references top lines"}`

  ```
# Références de non-régression

> **Passe — 2026-11-15 09 h 53 → 12 h 15 :** **85 portes, 81 vertes, 4 rouges** — `indice` et
> `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prechargement`
> **environnementale** (deux passes en parallèle ; PPL identique 799,8557 ; verte le 14/11).
> Journaux `work/portes-1115-09h53/`. **Pas de passe complète pour W6** ; ciblage
> `work/portes/w6-ciblage` (8/9), `w6-ciblage2` (2/2) puis `w6-final` (9/9).

> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
> `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
> `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
> `work/portes/passe-1311-23h15.log`.
>
> **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
> heartbeat `e181ce02` rafraîchi) ; `porte-indice` et `porte-melange` restent **rouges
> structurelles** (indice 482 contre témoin 459 ; état de A sans son code). Journaux
> `work/portes/verif-cloture/`.

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durabl
… [944 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '80,145p' docs/pilotage/references-non-regression.md", "description": "Read references gate table area"}`

  ```
| `porte-deepseek.sh` | 0 s | ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation. |
| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.77 s → 9.67 s (+2.9 s ≈ 50 ms × 64 pas) |
| `porte-diff-couche.sh` | 17 s | ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé |
| `porte-document.sh` | 6 s | ✅ porte document verte |
| `porte-echange-experts.sh` | 52 s | PORTE TENUE |
| `porte-episodique.sh` | 165 s | ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un |
| `porte-etat.sh` | 0 s | ✅ porte état verte : aucun fait commité après le dernier état |
| `porte-flux.sh` | 24 s | mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427) |
| `porte-fusion.sh` | 7 s | ✅ v1 refusée (code 2), trace seule refusée (code 2) |
| `porte-gain.sh` | 205 s | ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), sans fenê |
| `porte-greffe.sh` | 626 s | ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE |
| `porte-harnais-invariants.sh` | 109 s | ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, 
… [6038 caractères tronqués]
  ```

- **bash** `{"command": "sleep 20; tail -8 work/portes/verif-cloture-1116/porte-produit.log; echo '---'; cat work/portes/verif-cloture-1116/registre.txt", "description": "Check targeted produit gate result"}`

  ```
✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
---
porte-sessions 0
  ```

- **bash** `{"command": "sleep 30; tail -5 work/portes/verif-cloture-1116/porte-produit.log; echo '---'; cat work/portes/verif-cloture-1116/registre.txt; echo '--- code check ---'", "description": "Check produit gate final result"}`

  ```
✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
---
porte-sessions 0
--- code check ---
  ```

- **bash** `{"command": "ps -ef | grep -E 'porte-produit|autotest' | grep -v grep | head -10; tail -1 /tmp/porte-produit-autotest.log 2>/dev/null", "description": "Check autotest progress"}`

  ```
stephane 1725951 1723939  0 03:04 ?        00:00:00 bash -c mkdir -p work/portes/verif-cloture-1116 && { time bash tools/porte-produit.sh; } > work/portes/verif-cloture-1116/porte-produit.log 2>&1; code=$?; echo "porte-produit $code" >> work/portes/verif-cloture-1116/registre.txt; echo "CODE=$code"; tail -20 work/portes/verif-cloture-1116/porte-produit.log
stephane 1725960 1725951  0 03:04 ?        00:00:00 bash tools/porte-produit.sh
stephane 1726514 1725960  0 03:05 ?        00:00:00 timeout 600 python3 -m tools.pensee.autotest
stephane 1726515 1726514  0 03:05 ?        00:00:00 python3 -m tools.pensee.autotest
stephane 1726516 1726515 99 03:05 ?        00:00:56 python3 -m tools.pensee.autotest
stephane 1726517 1726515 16 03:05 ?        00:00:09 python3 -m tools.pensee.autotest
stephane 1726518 1726515 14 03:05 ?        00:00:08 python3 -m tools.pensee.autotest
stephane 1726519 1726515 15 03:05 ?        00:00:08 python3 -m tools.pensee.autotest
stephane 1726520 1726515 16 03:05 ?        00:00:09 python3 -m tools.pensee.autotest
stephane 1726521 1726515 16 03:05 ?        00:00:09 python3 -m tools.pensee.autotest
  ```

- **bash** `{"command": "git log --oneline -8 -- tools/drave.py tools/profils_udhr.py tools/tests/test_evaluer_strict.py tools/verifie_exemples.py pyproject.toml && echo '--- V2 code? ---' && git show --name-only --format='' HEAD | grep -E '^(tools|pyproject|docs/produit)' | head -30", "description": "Check whi … [29 caractères tronqués]`

  ```
ae3c24f2 V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
c77ed4b6 U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE
9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
519b729f J5 — Y1 : LE MODE AUTO DU TAGGER (CLÉ 0/130 TOKENS, INVALIDE 0, SANS CLÉ 0 IDENTIQUE AU DÉFAUT, RÉSEAU 0 APRÈS 3 ESSAIS) ; 30/30 TESTS
9960b37f SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE GOLD v2 NE GAGNE QU'UN CADRE (20/46, F1 0,5406, LIEU 0,60) ; --roles-v3 OPT-IN
840e613e TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES
5b2d07fc D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 
… [615 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat --oneline 2e617034 | grep -E 'tools/|pyproject|docs/produit|reports/' | head -40", "description": "Inspect U3 commit code files"}`

  ```
(no output)
  ```

- **bash** `{"command": "sleep 45; tail -4 work/portes/verif-cloture-1116/porte-produit.log; echo '---'; cat work/portes/verif-cloture-1116/registre.txt", "description": "Wait for produit gate completion"}`

  ```
✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
---
porte-sessions 0
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable-2.md", "content": "# V3 — la clôture de la nuit exploitable : les neuf tâches T1–T6 · U1–U3, deux vérifications, 86 portes, le tag `exploitable-2026-11-16`\n\n> **Ligne de roadmap** : **B13** (le produit … [18917 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable-2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

background job bash-60 (bash: mkdir -p work/portes/verif-cloture-1116 && { time bash tools/porte-produit.sh; } > work/portes/verif-cloture-1116/porte-produit.log 2>&1; code=$?; echo "porte-produit $code" >> work/portes/verif-cloture-1116/registre.txt; echo "CODE=$code"; tail -20 work/portes/verif-cloture-1116/porte-produit.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-60"}`

  ```
CODE=0
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
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte

real	3m19,281s
user	6m35,762s
sys	0m3,881s
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cat work/portes/verif-cloture-1116/registre.txt && echo '---' && tail -3 work/portes/verif-cloture-1116/porte-produit.log", "description": "Confirm targeted gate registry"}`

  ```
porte-sessions 0
porte-produit 0
---
real	3m19,281s
user	6m35,762s
sys	0m3,881s
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\n\nd = {\n \"schema\": \"drave.bilan-exploitable-2\",\n \"version\": 1,\n \"titre\": \"V3 — la clôture de la nuit exploitable : les neuf tâches T1–T6 · U1–U3, deux vérifications, 86 portes, le tag exploitable-2026-11-16\",\n \"sous_titre\": \"Bilan … [15360 caractères tronqués]`

  ```
écrit reports/rapport-bilan-exploitable-2.json 15351 octets
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-16 (V2)**", "new_string": "**Mis à jour : 2026-11-16 (V3)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**, v2 **20/46**) ; **U1** 4,0 → 0,82 s (α 1,08) ; **U2** roue 1 727 201 o, sans gold → 4 ; **U3** profils 20/20, `und` ; **V1** `--strict` 0,8 … [649 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **770** / **865** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **772** / **866** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W … [426 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**U1 — les deux O(k²) bornés** (α **1,08**, 10 000 mots **0,82 s**, sorties identiques, [fiche](../../reports/rapport-performance-fix.md)) ; **U2–U3 · V1–V2** ; **V3 la clôture** : **86/82/4** l … [290 caractères tronqués]`

  ```
Error: old_string was not found in "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T1–T6 — produit exploitable : installable, quickstart, JSON v2, performance, CLI 20/20** ([bilan](../../reports/rapport-bilan-exploitable.md)) ; **U1–U3, V1–V2, V3 — la clôture et le tag** ([b … [222 caractères tronqués]`

  ```
Error: old_string was not found in "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**V3 — la clôture** : **T1–T6**, **U1–U3**, **V1–V2** sont liées ; le relevé **86/82/4** est daté, **84/2** après vérification ciblée des deux rouges de circonstance ; tag `exploitable-2026-11-1 … [697 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n 'T1–T6 produit exploitable\\|T1–T6 — produit exploitable\\|U1 — les deux' docs/pilotage/en-cours.md", "description": "Locate exact B/R row text"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "sed -n '108,120p' docs/pilotage/en-cours.md", "description": "Read current B/R rows"}`

  ```
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : roue 1 727 201 o, mêmes JSON, sans gold → evaluer 4 ; U3 : profils 398 langues, 20/20, ambigu und ; V2 : exemples 27/27, 3 blocs corrigés** | **`g017` tranché** ; **J4** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N4** | N2 : **1 024 — 2,3911 / 2,3522** ; porte 2,7856 ; **[v2](../../reports/rapport-coordination-n2-v2.md)** ; N3 couvert ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |
| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 0,9575, réel 452 0,9500 ; W2 : 402 0,9643, H50 0,8607 ; W3 : défaut hors ligne, clé invalide 4, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; X3 : lot 
… [1043 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": " ; **V2 : exemples 27/27, 3 blocs corrigés ; V1 : `--strict` 0,8625/0,8891 ; V3 : clôture 86/82/4 → 84/2, tag `exploitable-2026-11-16`** |", "old_string": " ; **V2 : exemples 27/27, 3 blocs corr … [10 caractères tronqués]`

  ```
Error: old_string was not found in "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "réseau coupé 0 après 3 essais ; défaut inchangé) ; **V3 : clôture, tag `exploitable-2026-11-16` sur `ae3c24f2`** ; R2/R3 attendent N5/N4 |", "old_string": "réseau coupé 0 après 3 essais ; défaut … [40 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n 'V2 : exemples 27/27' docs/pilotage/en-cours.md", "description": "Find B row V2 substring"}`

  ```
113:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : roue 1 727 201 o, mêmes JSON, sans gold → evaluer 4 ; U3 : profils 398 langues, 20/20, ambigu und ; V2 : exemples 27/27, 3 blocs corrigés** | **`g017` tranché** ; **J4** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "V2 : exemples 27/27, 3 blocs corrigés ; V1 : --strict 0,8625/0,8891 ; V3 : clôture 86/82/4 → 84/2, tag exploitable-2026-11-16**", "old_string": "V2 : exemples 27/27, 3 blocs corrigés**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md')\nt=p.read_text()\nold='**U1 — les deux O(k²) bornés** (α **1,08**, 10 000 mots **0,82 s**, sorties identiques, [fiche](../../reports/rapport-performance-fix.md)) |'\nnew='**U1 — les deux O(k²) bornés** (α **1 … [918 caractères tronqués]`

  ```
ok
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**V2 — exemples.** 3 corrigés par les rôles normalisés ; 18 candidats objets, 0 faux ;\n`tools/verifie_exemples.py` 27/27 ; démarrage 3/3. [Fiche](../../reports/rapport-exemples-v2.md) ·\n[JSON]( … [735 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md": file changed since it was read — re-read the file, then retry
  ```

- **bash** `{"command": "sed -n '174,190p' docs/pilotage/roadmap.md", "description": "Re-read roadmap V2 area"}`

  ```
**V1 — `evaluer --strict` (16/11).** Quatre modes, cascade **0,8625** / **0,8891**, plancher
**0,70** ; négatif **0,0000** → **1**. [Fiche](../../reports/rapport-evaluer-strict.md) ·
[JSON](../../reports/evaluer-strict.json).

**V2 — exemples.** 3 corrigés par les rôles normalisés ; 18 candidats objets, 0 faux ;
`tools/verifie_exemples.py` 27/27 ; démarrage 3/3. [Fiche](../../reports/rapport-exemples-v2.md) ·
[JSON](../../reports/rapport-exemples-v2.json).

**T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques ; trois limites (clone public,
O(k²), or de S). [Fiche](../../reports/rapport-bilan-exploitable.md) ·
[JSON](../../reports/rapport-bilan-exploitable.json).

**La vue d'ensemble** est dans [`chantiers.md`](chantiers.md) ; carte,
[`chantiers-vision.svg`](../schemas/chantiers-vision.svg) ; plan,
[`plan-travail.md`](plan-travail.md).
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**V2 — exemples.** 3 corrigés par les rôles normalisés ; 18 candidats objets, 0 faux ;\n`tools/verifie_exemples.py` 27/27 ; démarrage 3/3. [Fiche](../../reports/rapport-exemples-v2.md) ·\n[JSON]( … [735 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 170, "limit": 25}`

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
179: **V2 — exemples.** 3 corrigés par les rôles normalisés ; 18 candidats objets, 0 faux ;
180: `tools/verifie_exemples.py` 27/27 ; démarrage 3/3. [Fiche](../../reports/rapport-exemples-v2.md) ·
181: [JSON](../../reports/rapport-exemples-v2.json).
182: 
183: **T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques ; trois limites (clone public,
184: O(k²), or de S). [Fiche](../../reports/rapport-bilan-exploitable.md) ·
185: [JSON](../../reports/rapport-bilan-exploitable.json).
186: 
187: **La vue d'ensemble** est dans [`chantiers.md`](chantiers.md) ; carte,
188: [`chantiers-vision.svg`](../schemas/chantiers-vision.svg) ; plan,
189: [`plan
… [260 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**V2 — exemples.** 3 corrigés par les rôles normalisés ; 18 candidats objets, 0 faux ;\n`tools/verifie_exemples.py` 27/27 ; démarrage 3/3. [Fiche](../../reports/rapport-exemples-v2.md) ·\n[JSON]( … [735 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n 'porte-produit.sh\\|porte-sessions.sh\\|porte-prechargement.sh' docs/pilotage/references-non-regression.md", "description": "Locate gate lines in references"}`

  ```
130:| `porte-prechargement.sh` | 181 s | PORTE TENUE |
140:| `porte-sessions.sh` | 20 s | ✅ PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md", "limit": 12}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md</path>
<type>file</type>
<content>
1: # Références de non-régression
2: 
3: > **Passe — 2026-11-15 09 h 53 → 12 h 15 :** **85 portes, 81 vertes, 4 rouges** — `indice` et
4: > `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prechargement`
5: > **environnementale** (deux passes en parallèle ; PPL identique 799,8557 ; verte le 14/11).
6: > Journaux `work/portes-1115-09h53/`. **Pas de passe complète pour W6** ; ciblage
7: > `work/portes/w6-ciblage` (8/9), `w6-ciblage2` (2/2) puis `w6-final` (9/9).
8: 
9: > **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
10: > `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
11: > `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
12: > `work/portes/passe-1311-23h15.log`.

(Showing lines 1-12 of 163. Use offset=13 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md", "new_string": "# Références de non-régression\n\n> **Passe — 2026-11-16 00 h 45 → 03 h 01 :** **86 portes, 82 vertes, 4 rouges** — `indice` et\n> `melange` structurelles ; `produit` (V1 n'avai … [1396 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n 'rapport-performance-fix\\|rapport-roue\\|rapport-bilan-exploitable-2\\|rapport-profils\\|rapport-evaluer-strict' reports/README.md", "description": "Check current report index rows"}`

  ```
44:| [`rapport-profils.md`](rapport-profils.md) | **U3/B13** — `drave profils` : les **398 profils UDHR** exposés, **20/20** sur l'échantillon, ambigu **`und`**, artefact de 802 110 o dans la roue |
45:| [`rapport-evaluer-strict.md`](rapport-evaluer-strict.md) | **V1** — `--strict` : cascade **0,8625/0,8891**, plancher **0,70** |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 14, "offset": 38}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
38: | [`rapport-cloture-chantier.md`](rapport-cloture-chantier.md) | **J14.1** — la clôture : **84/81/3**, trois rouges |
39: | [`rapport-tableau-mesures.md`](rapport-tableau-mesures.md) | **J13.1** — la table des mesures : POS |
40: | [`rapport-bilan-chantier.md`](rapport-bilan-chantier.md) | **J10.1** — le bilan du chantier : F1 |
41: | [`rapport-semaine.md`](rapport-semaine.md) | **J5.1** — le rapport de semaine : produit |
42: | [`rapport-semaine-2.md`](rapport-semaine-2.md) | **W6** — la semaine 2 : W1-W5, le tagger, Panini bloqué, la restitution v3 |
43: | [`rapport-bilan-exploitable.md`](rapport-bilan-exploitable.md) | **T6/B13** — installable, quickstart **3/3**, JSON v2 (**2 139** objets, **8** rôles), 10 000 mots **4,01 s**, CLI **20/20** ; trois limites, passe **85/81/4** |
44: | [`rapport-profils.md`](rapport-profils.md) | **U3/B13** — `drave profils` : les **398 profils UDHR** exposés, **20/20** sur l'échantillon, ambigu **`und`**, artefact de 802 110 o dans la roue |
45: | [`rapport-evaluer-strict.md`](rapport-evaluer-strict.md) | **V1** — `--strict` : cascade **
… [894 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-bilan-exploitable.md`](rapport-bilan-exploitable.md) | **T6/B13** — installable, quickstart **3/3**, JSON v2 (**2 139** objets, **8** rôles), 10 000 mots **4,01 s**, CLI **20/20** ; trois li … [1449 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/index_reports.py", "description": "Regenerate reports index"}`

  ```
768 fiches → reports/INDEX.md
  ```

- **bash** `{"command": "python3 tools/journal_auto.py --aide 2>&1 | head -40 || sed -n '1,60p' tools/journal_auto.py", "description": "Inspect journal generator usage"}`

  ```
usage: journal_auto.py [-h] [--jour JOUR] [--depuis DEPUIS] [--lister]
                       [--dry-run] [--quiet]
journal_auto.py: error: unrecognized arguments: --aide
  ```

- **bash** `{"command": "sed -n '1,90p' tools/journal_auto.py", "description": "Read journal auto tool"}`

  ```
#!/usr/bin/env python3
"""journal_auto.py — le journal quotidien, ÉCRIT PAR JOUR (UN DOSSIER) ET PAR THÈME, à partir de git et des sessions.

POURQUOI. Le journal doit consigner les **événements datés** (voir
`docs/organisation-du-depot.md`), et une journée de ce dépôt est trop riche pour un seul
fichier : un jour touche le moteur, les protocoles, les mesures, les portes et la
documentation. D'où le découpage **`<AAAA-MM-JJ>_<thème>.md`** : on lit la journée d'un thème,
et on suit un thème **d'un jour à l'autre** (le nom commence par la date, le thème suit —
`ls journal/2026-10-1*/attention.md`).

SOURCES, et rien d'autre :
  1. **git** — les commits du jour (heure d'auteur, en heure locale de la machine) et les
     fichiers touchés ; c'est la chronologie **fiable** (les horodatages écrits à la main
     s'étaient retrouvés dans le futur) ;
  2. **journal/sessions/** — les rapports de session dont la fenêtre de temps couvre le jour
     (début et durée lus dans l'index `journal/README.md`, régénéré par
     `tools/session_report.py`) : on en extrait les **titres de tour** classés par thème, avec
     le lien vers le rapport complet.

CE QUI EST PRÉSERVÉ. Tout ce que l'humain (ou l
… [3484 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'notes\\|U2 —\\|V2' journal/2026-11-16/README.md | tail -20 && tail -40 journal/2026-11-16/README.md", "description": "Inspect journal day notes"}`

  ```
5:> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
32:| 00:45 | `c77ed4b6` | U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE |
35:| 02:47 | `1a5a6548` | V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE |
39:<!-- notes -->
40:### U2 — la roue autonome, et la roue sans gold qui refuse de mesurer
57:### V2 — les exemples de la doc rejoués, et le contrôle qui les tient
72:<!-- /notes -->
| 00:48 | `1d4eb49e` | JOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4 |
| 02:10 | `2e617034` | EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF) |
| 02:47 | `1a5a6548` | V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE |

## Le récit de la journée (écrit à la main)

<!-- notes -->
### U2 — la roue autonome, et la roue sans gold qui refuse de mesurer

`python3 -m pip wheel . --no-deps --no-build-isolation
… [2084 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md", "new_string": "[Fiche](../../reports/rapport-exemples-v2.md) · [JSON](../../reports/rapport-exemples-v2.json).\n\n### V3 — la clôture de la nuit exploitable, et le tag sur le dernier commit vert\n\nLes **ne … [1319 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md", "limit": 6, "offset": 67}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md</path>
<type>file</type>
<content>
67: syntagmes du tagger à l'heuristique. **27/27 cas conformes, 0 écart** ; une mutation
68: `qualite` → `qualité` est détectée. Les **3 commandes** du démarrage sont **3/3** dans une copie
69: sans `tools/structures` (JSON **5 899 octets**).
70: 
71: [Fiche](../../reports/rapport-exemples-v2.md) · [JSON](../../reports/rapport-exemples-v2.json).
72: <!-- /notes -->

(End of file - total 72 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md", "new_string": "[Fiche](../../reports/rapport-exemples-v2.md) · [JSON](../../reports/rapport-exemples-v2.json).\n\n### V3 — la clôture de la nuit exploitable, et le tag sur le dernier commit vert\n\nLes **ne … [1319 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '1,180p' tools/verifie_etat_a_jour.py", "description": "Inspect state freshness hook logic"}`

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
… [6062 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -30; echo CODE-${PIPESTATUS[0]}", "description": "Run documentation review"}`

  ```
revue de documentation · 771 fiche(s) · 866 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · compteurs : en-cours.md dit 772 fichiers, le disque en a 771
CODE-1
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py; echo CODE-$?; python3 tools/taille_documents.py 2>&1 | tail -15; echo TAILLE-${PIPESTATUS[0]}", "description": "Check state length and structure"}`

  ```
en-cours · 1660 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
CODE-0
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4030 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 4 violation(s) :
     · docs/pilotage/roadmap.md : 9080 mots > budget 9000 (T1)
     · reports/README.md : 2860 mots > budget 2800 (T1)
     · docs/pilotage/references-non-regression.md : 2520 mots > budget 2500 (T1)
     · T0 : 4030 mots (AGENTS + en-cours + une tâche) > budget 4 000
TAILLE-1
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -20; echo CODE-${PIPESTATUS[0]}", "description": "Check journal consistency"}`

  ```
journal · 48 jour(s) · 227 session(s) · 2731 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
CODE-0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -10; echo CODE-${PIPESTATUS[0]}; python3 tools/verifier_schemas.py 2>&1 | tail -10; echo SCHEMAS-${PIPESTATUS[0]}", "description": "Run tables and schemas gates"}`

  ```
✅ 1853 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4837 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
CODE-0
  schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
SCHEMAS-0
  ```

- **bash** `{"command": "grep -rn '772' reports/rapport-bilan-exploitable-2.md reports/rapport-bilan-exploitable-2.json docs/pilotage/en-cours.md journal/2026-11-16/README.md 2>/dev/null", "description": "Find wrong 772 counter"}`

  ```
reports/rapport-bilan-exploitable-2.md:127:| 12 | **Les compteurs bougent** | **772** fiches / **866** JSON après ce rapport ; `en-cours` est la source | une fiche ajoutée après ce commit rend le chiffre faux sans calcul |
reports/rapport-bilan-exploitable-2.md:177:| C6 | les compteurs sont ceux du disque | `reports/*.md`, `reports/*.json`, `docs/**/*.md`, `tools/porte-*.sh` | **772 / 866 / 125 / 86** |
reports/rapport-bilan-exploitable-2.md:193:5. **Les compteurs bougent.** **772** fiches / **866** JSON après ce rapport ; `en-cours` est la
reports/rapport-bilan-exploitable-2.json:265:   "preuve": "772 fiches / 866 JSON après ce rapport ; en-cours est la source",
reports/rapport-bilan-exploitable-2.json:339:   "resultat": "772 / 866 / 125 / 86"
reports/rapport-bilan-exploitable-2.json:353:  "Les compteurs (772 fiches / 866 JSON) sont ceux du disque après ce rapport."
docs/pilotage/en-cours.md:101:| fichiers / JSON de résultats | **772** / **866** | `reports/*.md` / `reports/*.json` |
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re, pathlib\nfor f in ['docs/pilotage/roadmap.md','reports/README.md','docs/pilotage/references-non-regression.md','docs/pilotage/en-cours.md']:\n    t=pathlib.Path(f).read_text()\n    print(f, len(re.findall(r'\\S+',t)))\nPY", "description": "Count words in aff … [12 caractères tronqués]`

  ```
docs/pilotage/roadmap.md 9406
reports/README.md 2860
docs/pilotage/references-non-regression.md 2520
docs/pilotage/en-cours.md 1660
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\nfor f in ['reports/rapport-bilan-exploitable-2.md','reports/rapport-bilan-exploitable-2.json','docs/pilotage/en-cours.md']:\n    p=Path(f); t=p.read_text(); n=t.count('772'); t=t.replace('772','771'); p.write_text(t); print(f, n)\nPY", "descri … [36 caractères tronqués]`

  ```
reports/rapport-bilan-exploitable-2.md 3
reports/rapport-bilan-exploitable-2.json 3
docs/pilotage/en-cours.md 1
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/README.md'); t=p.read_text()\nlines=t.splitlines()\nout=[]\nfor l in lines:\n    if l.startswith('| [`rapport-performance-fix.md`]') or l.startswith('| [`rapport-roue.md`]'):\n        continue\n    if l.startswith('| [`rapport- … [488 caractères tronqués]`

  ```
lignes 235
README mots 2808
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/README.md'); t=p.read_text()\nt=t.replace('| [`rapport-bilan-exploitable-2.md`](rapport-bilan-exploitable-2.md) | **V3/B13** — la clôture : **86/82/4** → **84/2**, tag `exploitable-2026-11-16` |',\n            '| [`rapport-bila … [323 caractères tronqués]`

  ```
README mots 2804
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/README.md'); t=p.read_text()\nt=t.replace('| **V3** — clôture **86/82/4** → **84/2**, tag `exploitable-2026-11-16` |','| **V3** — **86/82/4** → **84/2**, tag `exploitable-2026-11-16` |')\np.write_text(t)\nimport re\nprint('READ … [80 caractères tronqués]`

  ```
README mots 2803
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/README.md'); t=p.read_text()\nt=t.replace('| **V3** — **86/82/4** → **84/2**, tag `exploitable-2026-11-16` |','| **V3** — **86/82/4** → **84/2** |')\nt=t.replace('artefact de 802 110 o dans la roue','artefact 802 110 o dans la  … [131 caractères tronqués]`

  ```
README mots 2800
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/README.md'); t=p.read_text().replace('artefact 802 110 o dans la roue','artefact 802 110 o')\np.write_text(t)\nimport re\nprint('README mots', len(re.findall(r'\\S+', t)))\nPY", "description": "README margin"}`

  ```
README mots 2797
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/references-non-regression.md'); t=p.read_text()\nold='''> **Passe — 2026-11-16 00 h 45 → 03 h 01 :** **86 portes, 82 vertes, 4 rouges** — `indice` et\n> `melange` structurelles ; `produit` (V1 n'avait pas fini) et `sessio … [1078 caractères tronqués]`

  ```
references mots 2497
  ```

- **bash** `{"command": "grep -n 'V3' docs/pilotage/en-cours.md | cut -c1-260", "description": "Locate V3 mentions in en-cours"}`

  ```
3:**Mis à jour : 2026-11-16 (V3)**
62:- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**, v2 **20/46**) ; **U1** 4,0 → 0,82 s (α 1,08) ; **U2** roue 1 727 201 o, sans gold → 4 ; **U3** profils 20/20, `und` ; **V1** `--strict` 0,8625/0,8891 ; **V2** exemples **27/27** ; **V3** la clôture — [b
113:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : roue 1 727 201 o, mêmes JSON, sans gold → evaluer 4 ; U3 : profi
115:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 0,9575, réel 452 0,9500 ; W2 : 402 0,9643, H50 0,8607 ; W3 : défaut hors ligne, clé invalide 4, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; X3 : lot 1 000, 672 appels, 99 971 tokens, 0,02177 
123:**V3 — la clôture** : **T1–T6**, **U1–U3**, **V1–V2** sont liées ; le relevé **86/82/4** est daté, **84/2** après vérification ciblée des deux rouges de circonstance ; tag `exploitable-2026-11-16` sur `ae3c24f2` ; [bilan 2](../../reports/rapport-bilan-expl
  ```

- **bash** `{"command": "sed -n '62p;113p;115p;123p' docs/pilotage/en-cours.md", "description": "Print exact en-cours lines"}`

  ```
- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**, v2 **20/46**) ; **U1** 4,0 → 0,82 s (α 1,08) ; **U2** roue 1 727 201 o, sans gold → 4 ; **U3** profils 20/20, `und` ; **V1** `--strict` 0,8625/0,8891 ; **V2** exemples **27/27** ; **V3** la clôture — [bilan 2](../../reports/rapport-bilan-exploitable-2.md), **86/82/4** lu, **84/2** après vérification ciblée, tag `exploitable-2026-11-16` sur `ae3c24f2`.
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : roue 1 727 201 o, mêmes JSON, sans gold → evaluer 4 ; U3 : profils 398 langues, 20/20, ambigu und ; V2 : exemples 27/27, 3 blocs corrigés ; V1 : --strict 0,8625/0,8891 ; V3 : clôture 86/82/4 → 84/2, tag exploitable-2026-11-16** | **`g017` tranché** ; **J4** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 0,9575, réel 452 0,9500 ; W2 : 402 0,9643, H50 0,8607 ; W3 : défaut hors ligne, clé invalide 4, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; X3 : lot 1 000, 672 appels, 99 971 tokens, 0,02177 
… [1283 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md'); t=p.read_text()\nt=t.replace('**V3** la clôture — [bilan 2](../../reports/rapport-bilan-exploitable-2.md), **86/82/4** lu, **84/2** après vérification ciblée, tag `exploitable-2026-11-16` sur `ae3c24f2`.',\ … [981 caractères tronqués]`

  ```
en-cours mots 1638
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md'); t=p.read_text()\nt=t.replace('\\n**C1** · **C2** · **C3** · **C4** · **C5** · **C6** · **C7** — hors graphe.\\n','\\n**C1–C7** — hors graphe.\\n')\np.write_text(t)\nimport re\nprint('en-cours mots', len(re. … [74 caractères tronqués]`

  ```
en-cours mots 1626
  ```

- **bash** `{"command": "grep -n 'État au 15/11\\|Passe\\*\\* : 84 portes' docs/pilotage/roadmap.md | head", "description": "Locate outdated roadmap state sentence"}`

  ```
38:**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902**, attachement **238/239** (0,9958), **1 span (`g017`)** ; **183/183** ; contrat **v2** (v1 lue) ; restitution **v3** (gold S **144/144**) ; **T5 CLI : 20/20, codes 0/3/4/5** ; **84 portes, 81/3** (`indice`, `melange`, `sessions`) ; `master` = `s/v7` ; [fiche `s065`](../../reports/rapport-s065.md).
44:CEGEP **91 scans uniques**, 1 982 p). **Passe** : 84 portes, **81/3**, 1 h 30 (00 h 30) ; les rouges tolérées sont `indice` et `melange` (structurelles), `sessions` est revérifiée verte ; compteurs **745 fiches / 839 JSON**.
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md'); t=p.read_text()\n# shorten V3 paragraph\nold='''**V3 — la clôture (16/11).** Les neuf tâches **T1–T6 · U1–U3** et les deux vérifications\n**V1–V2** sont liées ; relevé **86 / 82 / 4** (`work/portes/roue-1116 … [2134 caractères tronqués]`

  ```
roadmap mots 9334
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md'); t=p.read_text()\nfor s in ['**T5 CLI : 20/20, codes 0/3/4/5** ; ', '`master` = `s/v7` ; ']:\n    assert s in t, s\n    t=t.replace(s,'',1)\np.write_text(t)\nimport re\nprint('roadmap mots', len(re.findall(r' … [67 caractères tronqués]`

  ```
roadmap mots 9323
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -12; echo CODE-${PIPESTATUS[0]}", "description": "Re-check context budgets"}`

  ```
2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3996 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
CODE-0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -10; echo CODE-${PIPESTATUS[0]}", "description": "Re-run documentation review"}`

  ```
revue de documentation · 771 fiche(s) · 866 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · structure : 0 chantiers sur 7 dans en-cours.md ([])
CODE-1
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py; echo CODE-$?", "description": "Re-check state"}`

  ```
en-cours · 1626 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
CODE-0
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md'); t=p.read_text()\nold='| **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |'\nnew='| **C1** **C2** **C3** **C4** **C5** **C6** **C7** | hors graphe (transférés au journal) | aucun (hor … [274 caractères tronqués]`

  ```
en-cours mots 1628
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8; echo CODE-${PIPESTATUS[0]}", "description": "Re-run documentation review"}`

  ```
revue de documentation · 771 fiche(s) · 866 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
CODE-0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -4; echo CODE-${PIPESTATUS[0]}; python3 tools/verifie_en_cours.py; echo ENCOURS-$?", "description": "Re-check budgets and state"}`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
CODE-0
  en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
ENCOURS-0
  ```

- **bash** `{"command": "git tag -a exploitable-2026-11-16 -m \"Exploitable 2026-11-16 : 86 portes (82 vertes, 4 rouges au relevé ; 84/2 après vérification ciblée, indice et melange structurelles) ; T1-T6, U1-U3, V1-V2 ; V3\" ae3c24f2 && git cat-file -t exploitable-2026-11-16 && git rev-parse exploitable-2026-1 … [100 caractères tronqués]`

  ```
tag
ae3c24f2d8bb36311bc1d05e349b032c429a732c
exploitable-2026-11-16 Exploitable 2026-11-16 : 86 portes (82 vertes, 4 rouges au relevé ; 84/2 après vérification ciblée, indice et melange structurelles) ; T1-T6, U1-U3, V1-V2 ; V3
  ```

- **bash** `{"command": "git status --short && echo '--- diff stat ---' && git diff --stat", "description": "Review working tree changes"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/references-non-regression.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-16/README.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
 M reports/INDEX.md
 M reports/README.md
?? reports/rapport-bilan-exploitable-2.json
?? reports/rapport-bilan-exploitable-2.md
--- diff stat ---
 docs/pilotage/en-cours.md                               | 17 ++++++++---------
 docs/pilotage/references-non-regression.md              |  6 ++++++
 docs/pilotage/roadmap.md                                | 17 ++++++++++-------
 journal/2026-11-16/README.md                            | 17 +++++++++++++++++
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md        |  4 ++--
 reports/INDEX.md                                        |  3 ++-
 reports/README.md                                       |  5 +++--
 7 files changed, 48 insertions(+), 21 deletions(-)
  ```

- **bash** `{"command": "git diff --check; echo CHECK-$?; python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-bilan-exploitable-2.json'))\nprint('JSON OK', d['tache'], d['head'], d['portes']['relevé']['portes'], d['tag']['nom'])\nPY", "description": "Check whitespace and JSON validity"}`

  ```
CHECK-0
JSON OK V3 ae3c24f2 86 exploitable-2026-11-16
  ```

- **bash** `{"command": "git diff -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/references-non-regression.md reports/README.md | sed -n '1,220p'", "description": "Review state and roadmap diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index f46bcd9c..48408f6e 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-16 (V2)**
+**Mis à jour : 2026-11-16 (V3)**
 
 > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
 
@@ -59,7 +59,7 @@
 - **Plan** : B13 · **Stratégie** : v0 · **Ambition** : tracé · **Objectif final** : moteur v0.
 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.
 - **Ce que font les autres** : N2.
-- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**, v2 **20/46**) ; **U1** 4,0 → 0,82 s (α 1,08) ; **U2** roue 1 727 201 o, sans gold → 4 ; **U3** profils 20/20, `und` ; **V1** `--strict` 0,8625/0,8891 ; **V2** exemples **27/27** ([fiche](../../reports/rapport-exemples-v2.md)).
+- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**, v2 **20/46**) ; **U1** 4,0 → 0,82 s (α 1,08) ; **U2** roue 1 727 201 o, sans gold → 4 ; **U3** profils 20/20, `und` ; **V1** `--strict` 0,8625/0,8891 ; **V2** exemples **27/27** ; **V3** la clôture — **86/82/4** → **84/2**, tag `exploitable-2026-11-16` ([bilan 2](.
… [26904 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md'); t=p.read_text()\nt=t.replace('1 982 p)..','1 982 p).')\nv3='''**V3 — la clôture (16/11).** **T1–T6 · U1–U3 · V1–V2** ; **86 / 82 / 4** → **84 / 2**\n(`work/portes/`) ; tag `exploitable-2026-11-16` sur **`ae3 … [503 caractères tronqués]`

  ```
roadmap mots 9323
  ```

- **bash** `{"command": "grep -n '03 h 04\\|03:04\\|03 h 10\\|03:10\\|03 h 06\\|03:06' reports/rapport-bilan-exploitable-2.md reports/rapport-bilan-exploitable-2.json docs/pilotage/references-non-regression.md", "description": "Check targeted verification times"}`

  ```
reports/rapport-bilan-exploitable-2.md:102:| `porte-sessions` | **0** | ✅ verte après heartbeat à **03:06** ; autotest + `--check --strict` passent | `work/portes/verif-cloture-1116/porte-sessions.log` |
reports/rapport-bilan-exploitable-2.md:150:`porte-produit` rouge à 02:30) ; la vérification ciblée du **16/11 03:04–03:10** la rejoue verte
reports/rapport-bilan-exploitable-2.json:181:     "cause": "heartbeat à 03:06 ; autotest et --check --strict passent"
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-bilan-exploitable-2.md'); t=p.read_text().replace('16/11 03:04–03:10','16/11 03:04–03:08')\np.write_text(t)\nprint('ok')\nPY", "description": "Fix targeted verification time"}`

  ```
ok
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -3; echo REVUE-${PIPESTATUS[0]}; python3 tools/taille_documents.py 2>&1 | tail -2; echo TAILLE-${PIPESTATUS[0]}", "description": "Final doc review and budget check"}`

  ```
revue de documentation · 771 fiche(s) · 866 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE-0

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
TAILLE-0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -4; echo TABLEAUX-${PIPESTATUS[0]}", "description": "Final table gate"}`

  ```
✅ 1853 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4835 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
TABLEAUX-0
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -3; echo JOURNAL-${PIPESTATUS[0]}", "description": "Final journal check"}`

  ```
journal · 48 jour(s) · 227 session(s) · 2731 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
JOURNAL-0
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/references-non-regression.md reports/rapport-bilan-exploitable-2.md reports/rapport-bilan-exploitable-2.json reports/README.md reports/INDEX.md journal/2026-11-16/README.md journal/sessions/e181ce02-cd50-488a-a6be- … [186 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/references-non-regression.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-16/README.md
M  journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
M  reports/INDEX.md
M  reports/README.md
A  reports/rapport-bilan-exploitable-2.json
A  reports/rapport-bilan-exploitable-2.md
--- hook ---
  ✅ index : aucun fait stagé sans état
HOOK-0
  ```

- **bash** `{"command": "git commit -m \"V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON\" 2>&1 | tail -20; echo COMMIT-${PIPESTATUS[0]}", "description": "Commit V3 closure"}`

  ```
[still running after 60000ms; moved to background job bash-125]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-125", "timeout_ms": 60000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -ef | grep -E 'pre-commit|committing|git commit|porte-|revue_doc|journal' | grep -v grep | head -20", "description": "See what commit hook is running"}`

  ```
root        1408       1  0 nov03 ?        00:06:29 /usr/lib/systemd/systemd-journald
stephane 1727662  264909  0 03:09 ?        00:00:00 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 900; date; tail -2 work/chantier/journal.log; git tag -l "exploitable-*"; git rev-list --count origin/master..s/v7
stephane 1729337 1723939  0 03:12 ?        00:00:00 bash -c git commit -m "V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON" 2>&1 | tail -20; echo COMMIT-${PIPESTATUS[0]}
stephane 1729344 1729337  0 03:12 ?        00:00:00 git commit -m V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON
stephane 1729362 1729344  0 03:12 ?        00:00:00 /bin/sh .git/hooks/pre-commit
  ```

- **bash** `{"command": "cat .git/hooks/pre-commit 2>/dev/null | head -80; echo '--- child ---'; ps --ppid 1729362 -o pid,etime,cmd", "description": "Inspect pre-commit hook"}`

  ```
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
# Le journal du jour, par thème (sources : git + journal/sessions). L'index README est
… [332 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-125", "timeout_ms": 120000, "wait": true}`

  ```
✅ index : aucun fait stagé sans état
[s/v7 3c10e3ee] V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON
 21 files changed, 3550 insertions(+), 48 deletions(-)
 create mode 100644 journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/digest.md
 create mode 100644 journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/rapport.md
 create mode 100644 reports/rapport-bilan-exploitable-2.json
 create mode 100644 reports/rapport-bilan-exploitable-2.md
COMMIT-0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "git status --short; echo '---'; git log --oneline --decorate -3; echo '--- tag ---'; git cat-file -t exploitable-2026-11-16; git rev-parse exploitable-2026-11-16^{}; echo '--- branches ---'; git branch -vv | head", "description": "Verify commit, tag and branches"}`

  ```
---
3c10e3ee (HEAD -> s/v7) V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON
ae3c24f2 (tag: exploitable-2026-11-16) V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
2e617034 (origin/s/v7, origin/master, origin/HEAD, master) EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)
--- tag ---
tag
ae3c24f2d8bb36311bc1d05e349b032c429a732c
--- branches ---
  backup/pre-scrub-20261101-133055 5d5c1ee9 DONNÉES — LES DIX LANGUES SONT LÀ : 21,6 M ARTICLES, 31,4 G CARACTÈRES, 38,8 GO, 0 FUITE
  master                           2e617034 [origin/master] EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)
  s/close                          1d2cd6af ÉTAT — HEURE 16 H 33 ; B13 165/165 (CANDIDATS VERBES), D RESTAURÉ 62, 2 048 À 3 950 PAS
* s/v7                             3c10e3ee V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG
… [53 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -3; echo REVUE-${PIPESTATUS[0]}; python3 tools/verifie_en_cours.py | tail -2; echo ENCOURS-${PIPESTATUS[0]}; python3 tools/taille_documents.py 2>&1 | tail -1; echo TAILLE-${PIPESTATUS[0]}", "description": "Post-commit documentation checks … [2 caractères tronqués]`

  ```
revue de documentation · 771 fiche(s) · 866 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE-0
  en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
ENCOURS-0
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
TAILLE-0
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -2; echo JOURNAL-${PIPESTATUS[0]}; python3 tools/verifier_schemas.py 2>&1 | tail -2; echo SCHEMAS-${PIPESTATUS[0]}; bash tools/porte-tableaux.sh 2>&1 | tail -3; echo TABLEAUX-${PIPESTATUS[0]}", "description": "Post-commit journal, schema and  … [14 caractères tronqués]`

  ```
journal · 48 jour(s) · 228 session(s) · 2735 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
JOURNAL-0
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
SCHEMAS-0
  ✅ 1853 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4835 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
TABLEAUX-0
  ```

- **bash** `{"command": "git remote -v; git status -sb | head -3", "description": "Check remote and ahead status"}`

  ```
origin	git@github.com:stephanedenis/drave.git (fetch)
origin	git@github.com:stephanedenis/drave.git (push)
## s/v7
  ```

- **bash** `{"command": "git branch -f master s/v7 && timeout 120 git push origin s/v7 2>&1 | tail -3; echo PUSH_SV7-${PIPESTATUS[0]}; timeout 120 git push origin master 2>&1 | tail -3; echo PUSH_MASTER-${PIPESTATUS[0]}; timeout 120 git push origin exploitable-2026-11-16 2>&1 | tail -3; echo PUSH_TAG-${PIPESTAT … [56 caractères tronqués]`

  ```
To github.com:stephanedenis/drave.git
   2e617034..3c10e3ee  s/v7 -> s/v7
PUSH_SV7-0
To github.com:stephanedenis/drave.git
   2e617034..3c10e3ee  master -> master
PUSH_MASTER-0
To github.com:stephanedenis/drave.git
 * [new tag]           exploitable-2026-11-16 -> exploitable-2026-11-16
PUSH_TAG-0
  ```

- **bash** `{"command": "grep -n 'V3 — la clôture\\|7 commits\\|Tous les commits' journal/2026-11-16/README.md | head; tail -25 journal/2026-11-16/README.md", "description": "Verify journal note committed"}`

  ```
8:**7 commits** · **1 session(s)** · **4 thème(s)**
25:## Tous les commits (heure réelle)
73:### V3 — la clôture de la nuit exploitable, et le tag sur le dernier commit vert
Le contrôle n'est plus une relecture : `tools/verifie_exemples.py` lit les deux documents,
exécute chaque commande et compare le **JSON parsé**, le texte exact, le code du refus et les
syntagmes du tagger à l'heuristique. **27/27 cas conformes, 0 écart** ; une mutation
`qualite` → `qualité` est détectée. Les **3 commandes** du démarrage sont **3/3** dans une copie
sans `tools/structures` (JSON **5 899 octets**).

[Fiche](../../reports/rapport-exemples-v2.md) · [JSON](../../reports/rapport-exemples-v2.json).

### V3 — la clôture de la nuit exploitable, et le tag sur le dernier commit vert

Les **neuf tâches** du lot exploitable (**T1–T6**, **U1–U3**) et les deux vérifications
(**V1–V2**) sont liées dans un second bilan : [rapport-bilan-exploitable-2.md](../../reports/rapport-bilan-exploitable-2.md)
+ [JSON](../../reports/rapport-bilan-exploitable-2.json). Le chiffre de la nuit : le produit
s'installe, **10 000 mots** passent en **0,82 s** (α **1,076**, sorties identiques), la roue est
autonome (**1 727 201 o**, 
… [751 caractères tronqués]
  ```

- **job_list** `{}`

  ```
bash-16 [bash] running — find . -path ./.git -prune -o -iname '*exploitable*' -print 2>/dev/null | head -30 && echo '---' && grep -ril 'rapport-bilan-exploitable-2' . --exclude-dir=.git 2>/dev/null | head
bash-60 [bash] completed — mkdir -p work/portes/verif-cloture-1116 && { time bash tools/porte-produit.sh; } > work/portes/verif-cloture-1116/porte-produit.log 2>&1; code=$?; echo "porte-produit $code" >> work/portes/verif-cloture-1116/registre.txt; echo "CODE=$code"; tail -20 work/portes/verif-cloture-1116/porte-produit.log
bash-125 [bash] completed — git commit -m "V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON" 2>&1 | tail -20; echo COMMIT-${PIPESTATUS[0]}
  ```

- **job_kill** `{"job_id": "bash-16", "reason": "Recherche large devenue inutile ; le rapport est écrit et committé."}`

  ```
requested cancellation of job bash-16
  ```

- **todo_write** `{"todos": [{"content": "Rassembler les chiffres T1–T6, U1–U3, V1–V2 et le relevé des portes", "status": "completed"}, {"content": "Vérifier les deux rouges non structurelles (produit, sessions) sans relancer la passe", "status": "completed"}, {"content": "Écrire reports/rapport-bilan-exploitable-2.m … [432 caractères tronqués]`

  ```
Updated todo list: 0 pending, 0 in progress, 7 completed.
  ```

- **bash** `{"command": "git status --short; echo '--- head ---'; git log --oneline --decorate -2; echo '--- files in head ---'; git show --name-only --format='' HEAD | grep 'rapport-bilan-exploitable-2'; echo '--- remote tag ---'; timeout 60 git ls-remote --tags origin 'exploitable-2026-11-16' 2>&1 | head", "d … [59 caractères tronqués]`

  ```
--- head ---
3c10e3ee (HEAD -> s/v7, origin/s/v7, origin/master, origin/HEAD, master) V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON
ae3c24f2 (tag: exploitable-2026-11-16) V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
--- files in head ---
reports/rapport-bilan-exploitable-2.json
reports/rapport-bilan-exploitable-2.md
--- remote tag ---
fba7b1d93b46b06ea6661beaaf284ac961926c94	refs/tags/exploitable-2026-11-16
  ```

- **bash** `{"command": "grep -n 'rapport-bilan-exploitable-2' reports/INDEX.md reports/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -10", "description": "Verify new report linked from indexes and state"}`

  ```
reports/INDEX.md:85:| [rapport-bilan-exploitable-2.md](rapport-bilan-exploitable-2.md) | V3 — la clôture de la nuit exploitable : les neuf tâches T1–T6 · U1–U3, deux vérifications, 86 portes, le tag `exploitable-2026-11-16` |
reports/README.md:46:| [`rapport-bilan-exploitable-2.md`](rapport-bilan-exploitable-2.md) | **V3** — **86/82/4** → **84/2** |
docs/pilotage/en-cours.md:62:- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**, v2 **20/46**) ; **U1** 4,0 → 0,82 s (α 1,08) ; **U2** roue 1 727 201 o, sans gold → 4 ; **U3** profils 20/20, `und` ; **V1** `--strict` 0,8625/0,8891 ; **V2** exemples **27/27** ; **V3** la clôture — **86/82/4** → **84/2**, tag `exploitable-2026-11-16` ([bilan 2](../../reports/rapport-bilan-exploitable-2.md)).
docs/pilotage/en-cours.md:122:**V3 — la clôture** : **T1–T6**, **U1–U3**, **V1–V2** ; **86/82/4** → **84/2** après vérification ciblée ; tag `exploitable-2026-11-16` sur `ae3c24f2` ; [bilan 2](../../reports/rapport-bilan-exploitable-2.md), [U1](../../reports/rapport-performance-fix.md), [U2](../../reports/rapport-roue.md), [U3](../../reports/rapport-profils.md), [V1](../../reports/rapport-evaluer-strict.md), [V2](../../reports/rapport-exemples-v2.m
… [4794 caractères tronqués]
  ```

- **bash** `{"command": "printf 'porte-sessions 0 1\\nporte-produit 0 199\\n' > work/portes/verif-cloture-1116/registre.txt && cat work/portes/verif-cloture-1116/registre.txt && awk '$2 != 0' work/portes/verif-cloture-1116/registre.txt; echo AWK-${PIPESTATUS[0]}", "description": "Normalize targeted gate registr … [10 caractères tronqués]`

  ```
porte-sessions 0 1
porte-produit 0 199
AWK-0
  ```

- **job_list** `{}`

  ```
bash-16 [bash] killed — find . -path ./.git -prune -o -iname '*exploitable*' -print 2>/dev/null | head -30 && echo '---' && grep -ril 'rapport-bilan-exploitable-2' . --exclude-dir=.git 2>/dev/null | head
bash-60 [bash] completed — mkdir -p work/portes/verif-cloture-1116 && { time bash tools/porte-produit.sh; } > work/portes/verif-cloture-1116/porte-produit.log 2>&1; code=$?; echo "porte-produit $code" >> work/portes/verif-cloture-1116/registre.txt; echo "CODE=$code"; tail -20 work/portes/verif-cloture-1116/porte-produit.log
bash-125 [bash] completed — git commit -m "V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON" 2>&1 | tail -20; echo COMMIT-${PIPESTATUS[0]}
  ```

### 🤖 Assistant

**V3 — clôture faite.** Le bilan de la nuit est écrit et committé.

- **Rapport** : `reports/rapport-bilan-exploitable-2.md` + `reports/rapport-bilan-exploitable-2.json`.
  Il couvre les **9 tâches mesurées T1–T6 · U1–U3**, les **deux vérifications V1–V2** et cette clôture :
  produit installable, JSON **2 139** objets / **8** rôles, **10 000 mots 0,82 s** (α **1,076**, diff vide),
  roue **1 727 201 o** (sans gold → **4**), profils **20/20** (ambigu **`und`**), `--strict` **0,8625/0,8891**,
  exemples **27/27** — avec **12 négatifs** nommés (clone public, or de S, mock neuronal, confiance non calibrée, etc.).
- **Portes** : relevé `work/portes/roue-1116/` lu **sans relancer la passe** → **86 portes, 82 vertes, 4 rouges**
  (`indice`, `melange` structurelles ; `produit` et `sessions` de circonstance).
  Vérification ciblée dans `work/portes/verif-cloture-1116/` : `sessions` **0**, `produit` **0**
  (`--strict` 5 tests, exemples 27/27, autotest 183/183) → **84 vertes, 2 rouges structurelles**.
- **État et roadmap** : `docs/pilotage/en-cours.md` et `docs/pilotage/roadmap.md` mis à jour
  (compteurs **771/866**, passe du 16/11, V3, tag) ; `references-non-regression.md` et journal du 16/11 complétés.
- **Tag annoté** : `exploitable-2026-11-16` sur le dernier commit vert **`ae3c24f2`** (V2).
  Contrôles : `git cat-file -t` → `tag` ; `git rev-parse exploitable-2026-11-16^{}` → `ae3c24f2`.
- **Commit** : `3c10e3ee` — *V3 — la clôture…* ; poussé sur `origin/s/v7`, `origin/master` et le tag.
- **Vérifications finales** : `revue_documentation.py` ✅, `verifie_en_cours.py` ✅, `taille_documents.py` ✅,
  `verifie_journal.py` ✅, `porte-tableaux.sh` ✅, `verifier_schemas.py` ✅.

Prochaine mesure désignée : **J4 — l’or de rôles** ; Panini attend ses 26 signatures et la décision `auto` reste humaine.

