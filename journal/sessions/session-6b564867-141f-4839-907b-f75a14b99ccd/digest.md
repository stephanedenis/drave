# Session DSH — relecture

- identifiant : `session-6b564867-141f-4839-907b-f75a14b99ccd`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 02:03:36
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche C1 : la coordination N2, suite de J4.1 — écris `reports/rapport-coordination-n2-v2.md` + JSON : la commande **validée** `python3 work/n2ac/eval_longueurs.py --rope --canal-dir <dir>` (le correctif mesuré 2,79), la commande à ne PAS utiliser (`--rope` seul : 40,07), le test de non-régression proposé (`porte-n2.sh` : la porte à 3,09 doit rester à 3,09), et la mise à jour de la ligne N2 de `docs/pilotage/en-cours.md`. **Ne modifie rien dans `tools/n2/` ni `work/n2ac/`.**

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

### 🤖 Assistant

I'll start by understanding the task context. Let me read the relevant files.

- **bash** `{"command": "ls -la && echo \"---\" && ls reports/ | head -50 && echo \"---\" && ls work/n2ac/ 2>/dev/null && echo \"---\" && ls tools/n2/ 2>/dev/null", "description": "List repo structure and relevant dirs"}`

  ```
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198 15 nov 02:03 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 76454 15 nov 01:31 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run
… [7487 caractères tronqués]
  ```

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --short | head -40 && echo \"---BRANCH---\" && git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet log --oneline -10", "description": "Check git status and recent log"}`

  ```
MM journal/2026-11-14/README.md
MM journal/2026-11-14/distribue.md
MM journal/2026-11-14/docs.md
MM journal/2026-11-14/memoire.md
MM journal/2026-11-14/mesures.md
MM journal/2026-11-14/moteur.md
MM journal/2026-11-14/portes.md
D  journal/2026-11-15/README.md
D  journal/2026-11-15/mesures.md
D  journal/2026-11-15/portes.md
MM journal/README.md
MM journal/THEMES.md
D  journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/digest.md
D  journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/rapport.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
MM journal/sessions/session-a68c9aaf-bd76-458b-8501-5a29431b2e10/digest.md
MM journal/sessions/session-a68c9aaf-bd76-458b-8501-5a29431b2e10/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? journal/2026-11-15/
?? journal/sessions/24e34ad3-f423-4394
… [1311 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i -E 'n2|coordination|longueur' ; echo \"---TOOLS---\" ; ls tools/n2/ 2>/dev/null ; echo \"---N2AC---\" ; ls work/n2ac/ | grep -i -E 'longueur|n2|porte' ; echo \"---PORTE---\" ; find . -name 'porte-n2*' -not -path … [83 caractères tronqués]`

  ```
n2-200k.json
n2-budget.json
n2-capacite-fenetre.json
n2-distillation.json
n2-distillation-native.json
n2-fenetre.json
n2-hierarchie.json
n2-porte-propre.json
n2-production-fenetre.json
n2-propre.json
n2-r11.json
n2-r12-2048.json
pensee-etat-n2.json
pensee-quatre-modes-432-run2.json
pensee-quatre-modes-run2.json
pont-longueur2-3b.json
rapport-coordination-a.json
rapport-coordination-a.md
rapport-coordination-n2.json
rapport-coordination-n2.md
rapport-coordination-r.json
rapport-coordination-r.md
rapport-coordination-s.json
rapport-coordination-s.md
rapport-etat-n2.md
rapport-n2-200k.md
rapport-n2-34m-distille.md
rapport-n2-anglais-34m.md
rapport-n2-anglais-distille.md
rapport-n2-anglais.md
rapport-n2-budget.md
rapport-n2-canal-34m.md
rapport-n2-canal-distille.md
rapport-n2-canal-kd-34m.md
rapport-n2-canal.md
rapport-n2-capacite-34m.md
rapport-n2-capacite.md
rapport-n2-capacite-reelle.md
rapport-n2-combine.md
rapport-n2-corpus-1go.md
rapport-n2-corpus-elargi.md
rapport-n2-corpus-reel.md
rapport-n2-distillation.md
rapport-n2-distillation-native.md
rapport-n2-distillation-reelle.md
rapport-n2-diversite.md
rapport-n2-echantillon.md
rapport-n2-fenetre.md
rapport-n2-fenetre-r1.md
rapport-
… [578 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -i -E 'N2|J4\\.1|J4' docs/pilotage/en-cours.md | head -40", "description": "Find N2 line in en-cours"}`

  ```
12:- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
36:- **Ce que font les autres** : **N2**, **S**, **Pensée**.
51:- **Ce que font les autres** : **hub**, **N2**, **Pensée**.
65:- **Ce que font les autres** : **N2**, **S**, **hub**.
72:### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*
75:- **Rôle** : **N2** — la production et la capacité.
80:- **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondération) ; `kd2` et `rope2048` **arrêtés** ; **paire propre** : **3,1500** → **3,1119** (−0,06 ; −0,19 anglais) ; **repondération : −0,05** ; **2 048** ne bat pas 1 024 ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [production](../../reports/rapport-n2-production-fenetre.md), [erratum](../../reports/rapport-n2-distillation-native.md), [porte](../../reports/rapport-n2-porte-propre.md).
89:- **N2 — en pause** : **1 024** = recette ; **2 048 fini** ; distillation mesurée ; prochaine : **porte propre (0,29)** ; **GPUs libres**.
119:| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522
… [741 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md</path>
<type>file</type>
<content>
1: # N2 — la coordination du mètre : `--rope` ne suffit pas, il faut le canal
2: 
3: > **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-13 · **HEAD mesuré** :
4: > `ced21933` · **Verdict** : `tools/eval_n2_propre.py` lit les checkpoints RoPE comme des positions
5: > absolues et rend **8,0225** sur `propre512-8k` à 128 octets, là où le mètre RoPE rend **2,9726**
6: > à 128 et **2,7856** à 1 024. Le correctif `--rope` est **nécessaire mais non suffisant** : le
7: > checkpoint de la porte a été entraîné **avec le canal**, et `--rope` seul rend **40,0658** à 128.
8: > Le correctif validé est **`--rope --canal-dir`** ; la commande qui donne 2,79 aujourd'hui est le
9: > mètre existant `work/n2ac/eval_longueurs.py --rope`. **Aucun fichier de N2 modifié**
10: > (`native_model.py`, `entrainer_native.py`, `work/` intacts).
11: 
12: **En trois lignes.** (1) `charge()` construit `NativeModel` absolu et `ppl_protocole()` oublie le
13: canal : **deux** causes, pas une. (2) `--rope` seul rend **40,07** ; `--rope --canal-dir` rend
14: **2,9726** à 128 e
… [20830 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn -i -E 'J4\\.1|J4|2,79|2\\.79|40,07|40\\.07|3,09|3\\.09' journal/ docs/pilotage/ reports/rapport-coordination-n2.md 2>/dev/null | head -50", "description": "Search for J4.1 and key figures"}`

  ```
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:2174:**Attention** : l'hypothèse « relecture du cache KV » a été **réfutée** par la mesure (chemin groupé par tête KV : 3,20 → 3,27 ms). L'instrumentation des trois phases a montré que les scores coûtaient 2,10 des 3,09 ms, en calcul scalaire déjà à 3,3 opérations/cycle. En AVX2+FMA : **3,09 → 1,57 ms**.
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:6461:non structuré         1    5.0%  59.08% |    1.05    2.64    2.79   2.00 |     0.29    20.15
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:7911:  E[|v|]                : 42.79
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:8072:  E[|v|] sur non-nuls      :  42.79  → mode UNAIRE
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:10543:- Qwen2.5-0.5B measures: real Q8_0 494 M weights, density 99.2%, E[|v|]=42.79, E[popcount]=3.13; Q4_0 E[|v|]=3.02, E[popcount]=1.39, 27.2% of non-zeros are ±1.
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:10881:threads=8      100.0%       4303745  fusion   3.09 G (1.3949 ms) | 2-listes   3.23 G (1.3307 ms)
journal/sessions/22bcae27-254b-47b2-acda-87467dab
… [10739 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2ac/eval_longueurs.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2ac/eval_longueurs.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """eval_longueurs.py — la courbe de longueur d'un point de contrôle (absolu ou RoPE).
3: 
4: Le mètre est celui de N2 (`work/n2j/evalue_canal.py`) : canal fourni, fenêtres Van der Corput
5: dans des chunks de 8192 octets, 8 lots × 16 fenêtres. On peut demander n'importe quelle
6: longueur, y compris **1 000 octets** (la porte R1.1).
7: 
8: Usage :
9:   PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/eval_longueurs.py <point.pt> \
10:       --longueurs 128,256,512,1000 [--rope] [--val data/wiki_fr/propre]
11: """
12: from __future__ import annotations
13: 
14: import argparse
15: import json
16: import pathlib
17: import sys
18: 
19: sys.path.insert(0, ".")
20: sys.path.insert(0, "work/n2j")
21: 
22: import torch  # noqa: E402
23: 
24: from tools.eval_n2_propre import charge, charger_bytes  # noqa: E402
25: import evalue_canal as ec  # noqa: E402
26: 
27: 
28: def main() -> None:
29:     ap = argparse.ArgumentParser()
30:     ap.add_argument("point")
31:     ap.add_argument("--longueurs", default="128,256,512")
32:     ap.add_argument("--rope"
… [1111 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn -i 'porte-n2\\|porte n2' --include='*.md' --include='*.sh' --include='*.json' . 2>/dev/null | grep -v '.git/' | head -30 ; echo \"---J41---\" ; grep -rn 'J4.1' journal/ docs/ reports/ 2>/dev/null | head -20", "description":  … [42 caractères tronqués]`

  ```
./reports/rapport-native-distillation.md:35:**N2.3 — première passe : atteint.** La distillation fonctionne et le gain est mesuré. La porte N2
./reports/rapport-native-distillation-tetes.md:36:une meilleure langue. La porte N2 (**PPL < 2,5**) n'est pas atteinte.
./reports/rapport-native-distillation-multi.md:33:- La porte N2 (**< 2,5**) reste **non atteinte** ; elle était définie sur le français.
./reports/rapport-native-capacite-egal.md:46:d'entraînement domine** (+26 % pour le 11,47 M entraîné). La porte N2 (**PPL < 2,5**) reste hors de portée à 5 000 pas.
./reports/r02-banc-lecture.json:827:   "question": "Quelle porte N2 doit-elle franchir ?",
./reports/r03-lecteur-modele.json:320:   "question": "Quelle porte N2 doit-elle franchir ?",
./reports/r03-lecteur-modele.json:327:    "reponse": "Pour déterminer la porte N2 que N2 doit franchir, nous devons suivre les étapes suiv"
./reports/r03-lecteur-modele.json:334:    "reponse": "Pour identifier la porte N2 qui doit être franchie, nous devons suivre les étapes suivantes :\n\n1"
./reports/r03-lecteur-modele.json:341:    "reponse": "Pour répondre à cette question, nous devons identifier les informations fournies pour déterminer la por
… [8411 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-n2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-n2.md</path>
<type>file</type>
<content>
1: # N2 — l'état du chantier et de sa porte : inventaire, vérification, proposition
2: 
3: > **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-06 · **Verdict** :
4: > N2 n'a **pas** de porte unique dans la passe : sa rouge est une **mesure** — **2,7856** de PPL
5: > sur le corpus propre à 1 024 octets contre la porte **< 2,5**, soit **0,29** en validation
6: > (**0,36** en test). Le mètre est **reproductible** (2,7856 / 2,8566 à l'identique, contrôle
7: > permuté **1 692,39**, deux exécutions égales) et tient en **12 s** de GPU. `tools/eval_n2_propre.py`
8: > **tourne** sur le checkpoint le plus récent mais **ne le mesure pas** : il charge l'architecture à
9: > positions **absolues** et rend **12,91** (pire que l'uniforme, 5,55) là où le mètre RoPE rend
10: > **4,63** ; sur le checkpoint de la porte, **8,02** contre **2,97** à 128 octets. Une
11: > `tools/porte-n2.sh` est **proposable** : non-régression **≤ 2,80** par défaut, seuil **2,5** en
12: > mode chantier, **~30–40 s** de GPU, dépendante de `work/` et `data/` **non suivis**.
13: 
14: ## La
… [19372 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\ns=json.dumps(p,ensure_ascii=False,indent=1)\nfor key in ['\"C1\"','C1','coordination N2','n2ac','3,09','3.09']:\n    i=s.find(key)\n    print('KEY',key,'a … [120 caractères tronqués]`

  ```
KEY "C1" at 17081
ports/rapport-tableau-mesures.md`, commit.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-tableau-mesures.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    }
   ]
  },
  {
   "id": "J14.1",
   "jour": 14,
   "titre": "La clôture — la passe et le tag",
   "mandat": "Tâche J14.1 : la clôture — **sans relancer la passe complète** (elle a été faite le 14/11 00 h : `work/portes/passe-1311-23h15.log`, 84 portes, 81 vertes, 3 rouges nommées). Vérifie « porte-indice », « porte-melange », « porte-sessions » ; mets à jour `docs/pilotage/references-non-regression.md` si nécessaire ; crée le **tag annoté** `chantier-2026-11-14` sur le dernier commit vert ; écris le rapport de clôture `reports/rapport-cloture-chantier.md` + JSON ; commit.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "git tag -l 'chantier-2026-11-14'",
     "attendu": "chantier-2026-11-14"
    },
    {
     "commande": "test -f reports/rapport-cloture-chantier.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
    {
     "commande": "python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?",
     "attendu": "REVUE-0"
    }
   ]

… [12947 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -ld tools/n2 2>&1; ls -la tools/n2 2>&1 | head; echo \"---\"; find tools -maxdepth 2 -iname '*n2*' 2>/dev/null; echo \"---git log file---\"; git log --oneline -- work/n2ac/eval_longueurs.py | head; echo \"---canal-dir grep---\"; g … [174 caractères tronqués]`

  ```
ls: cannot access 'tools/n2': No such file or directory
ls: cannot access 'tools/n2': No such file or directory
---
tools/__pycache__/eval_n2.cpython-313.pyc
tools/__pycache__/eval_n2_propre.cpython-313.pyc
tools/eval_n2.py
tools/eval_n2_budget.py
tools/eval_n2_propre.py
---git log file---
---canal-dir grep---
[still running after 60000ms; moved to background job bash-8]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,200p' reports/rapport-coordination-n2.json", "description": "Read existing v1 JSON"}`

  ```
{
  "date": "2026-11-13",
  "head": "ced21933",
  "ligne": "N2",
  "objet": "coordination du mètre eval_n2_propre.py pour les checkpoints RoPE",
  "fiche": "reports/rapport-coordination-n2.md",
  "verdict": "eval_n2_propre.py lit les checkpoints RoPE comme des positions absolues et rend 8,0225 sur propre512-8k à 128 octets, contre 2,9726 à 128 et 2,7856 à 1024 au mètre RoPE. --rope est nécessaire mais non suffisant : le checkpoint de la porte a été entraîné avec le canal, et --rope seul rend 40,0658. Le correctif validé est --rope --canal-dir.",
  "aucune_modification_n2": [
    "tools/native_model.py",
    "tools/entrainer_native.py",
    "work/"
  ],
  "bug": {
    "fichier": "tools/eval_n2_propre.py",
    "symptome": "val 8,0225 au lieu de 2,9726 à 128 et 2,7856 à 1024 sur work/n2ac/propre512-8k.pt",
    "causes": [
      {
        "rang": 1,
        "nom": "architecture",
        "detail": "charge() construit NativeModel (table de positions apprise absolue) au lieu de NativeModelRoPE ; les checkpoints N2 depuis le 02/11 sont des NativeModelRoPE, avec les mêmes noms de tenseurs et self.pos inutilisé.",
        "silence": "load_state_dict(strict=False) : 127 clés, 0 manquante, 0 
… [8470 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln 'coordination-n2-v2\\|la porte à 3,09\\|3,09 doit rester' journal/ reports/ docs/ 2>/dev/null | head -20", "description": "Search prior work on v2"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline --all -- reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json | head; echo '--- en-cours N2 lines context ---'; sed -n '60,145p' docs/pilotage/en-cours.md", "description": "Read en-cours N2 sectio … [3 caractères tronqués]`

  ```
34e3e4ab J5.1 — LE RAPPORT DE SEMAINE : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 237, TAGGER 0,9475 (+8,49, INTÉGRER), INTÉGRATION BORNÉE (TABLE 14/14, CORPUS 418/438), 13 DÉCISIONS, 21 REJETS
--- en-cours N2 lines context ---
- **Plan** : B13.
- **Stratégie** : v0 mesuré.
- **Ambition** : un runtime cognitif tracé.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Ce qu'elle fait** : chantier.
- **Prochaine action** : **trancher la convention d'adverbe (`g017`)** ; puis T132/T133, gold 200+.
- **Clôture** : **J14.1 faite** (84/81/3 ; `sessions` verte, `indice` et `melange` structurelles ; tag `chantier-2026-11-14`).
- **Bloquants
… [7469 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -E 'rope|canal|longueurs|def charge|add_argument' tools/eval_n2_propre.py | head -60", "description": "Check eval_n2_propre current options"}`

  ```
16:  longueurs         : PPL à 129, 192, 256, 384, 512 octets — le verrou de longueur, mesuré
21:      [--longueurs] [--decomposition] [--sortie work/n2h/eval.json]
40:def charger_bytes(chemin) -> torch.Tensor:
44:def charge(chemin, device="cuda"):
111:    ap.add_argument("point")
112:    ap.add_argument("--chunk", type=int, default=8192)
113:    ap.add_argument("--corpus-dir", default="data/corpus_propre",
115:    ap.add_argument("--longueurs", action="store_true")
116:    ap.add_argument("--decomposition", action="store_true")
117:    ap.add_argument("--sortie", default=None)
118:    ap.add_argument("--device", default="cuda")
144:    if a.longueurs:
145:        r["longueurs"] = {str(L): round(ppl_protocole(m, val, L, 16, a.chunk, device=a.device), 4)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l tools/eval_n2_propre.py work/n2ac/eval_longueurs.py reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json; echo '--- git status N2 ---'; git status --short tools/eval_n2_propre.py work/n2ac/eval_longueurs.py r … [186 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 11915 13 nov 21:52 reports/rapport-coordination-n2.json
-rw-r--r--. 1 stephane stephane 20149 13 nov 21:52 reports/rapport-coordination-n2.md
-rw-------. 1 stephane stephane  6787  1 nov 07:17 tools/eval_n2_propre.py
-rw-------. 1 stephane stephane  1940  2 nov 16:22 work/n2ac/eval_longueurs.py
--- git status N2 ---
--- grep canal in work ---
[still running after 60000ms; moved to background job bash-13]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader 2>&1 | head -8); echo '--- gpu-env ---'; ls -l ~/gpu-env/bin/python 2>&1; echo '--- eval_longueurs help ---'; PYTHONPATH=. ~/gpu-env/bi … [112 caractères tronqués]`

  ```
0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %
1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %
--- gpu-env ---
lrwxrwxrwx. 1 stephane stephane 7 31 jui 08:53 /home/stephane/gpu-env/bin/python -> python3
--- eval_longueurs help ---
usage: eval_longueurs.py [-h] [--longueurs LONGUEURS] [--rope] [--val VAL]
                         [--sortie SORTIE]
                         point

positional arguments:
  point

options:
  -h, --help            show this help message and exit
  --longueurs LONGUEURS
  --rope
  --val VAL
  --sortie SORTIE
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,58p' docs/pilotage/en-cours.md", "description": "Read en-cours header"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 01 h 50 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **État** : **en pause** depuis le 05/11 (dernier heartbeat) ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'
… [2580 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l work/n2ac/propre512-8k.pt work/n2h/A-propre-g1.pt data/corpus_propre/{val,test}.{txt,canal} 2>&1", "description": "Verify artifacts exist"}`

  ```
-rw-r--r--. 1 stephane stephane    180224  3 nov 02:03 data/corpus_propre/test.canal
-rw-r--r--. 1 stephane stephane    180224 31 oct 22:20 data/corpus_propre/test.txt
-rw-r--r--. 1 stephane stephane    180224  2 nov 23:07 data/corpus_propre/val.canal
-rw-r--r--. 1 stephane stephane    180224 31 oct 22:20 data/corpus_propre/val.txt
-rw-r--r--. 1 stephane stephane 137248474  3 nov 02:01 work/n2ac/propre512-8k.pt
-rw-r--r--. 1 stephane stephane  47302035 31 oct 23:12 work/n2h/A-propre-g1.pt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/propre512-8k.pt --rope --canal-dir data/corpus_propre --longueurs 128 2>&1 | tail -3; echo \"EXIT=$?\"", "description": "Test whether --canal-dir is accepted"}`

  ```
[--sortie SORTIE]
                         point
eval_longueurs.py: error: unrecognized arguments: --canal-dir data/corpus_propre
EXIT=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/propre512-8k.pt --rope --longueurs 128,256,512,1024 --val data/corpus_propre 2>&1 | tail -8", "description": "Re … [60 caractères tronqués]`

  ```
L128 : 2.9726
  L256 : 2.8988
  L512 : 2.8443
  L1024 : 2.7856
{"fichier": "propre512-8k.pt", "val": "data/corpus_propre", "positions": "rope", "L128": 2.9726, "L256": 2.8988, "L512": 2.8443, "L1024": 2.7856}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/A-propre-g1.pt --longueurs 2>&1 | tail -12", "description": "Replay 3.09 absolute control", "timeoutMs": 300000}`

  ```
{"fichier": "A-propre-g1.pt", "params": 11816136, "val": 3.0971, "test": 3.2098, "litterature": 15.9854, "litterature_propre": 17.0838, "anglais": 60.6957, "wikitext2": 59.729, "permute": 1356.6433, "longueurs": {"129": 3.1334, "192": 8.7137, "256": 14.4554, "384": 24.8061, "512": 34.0535}}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf /tmp/c1-propre-test && mkdir -p /tmp/c1-propre-test && cp data/corpus_propre/test.txt /tmp/c1-propre-test/val.txt && cp data/corpus_propre/test.canal /tmp/c1-propre-test/val.canal && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA … [242 caractères tronqués]`

  ```
L128 : 3.0649
  L512 : 2.8875
  L1024 : 2.8566
{"fichier": "propre512-8k.pt", "val": "/tmp/c1-propre-test", "positions": "rope", "L128": 3.0649, "L512": 2.8875, "L1024": 2.8566}
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """eval_n2_propre.py — la porte honnête : PPL sur un corpus dédupliqué, et hors domaine.
3: 
4: Le corpus de `data/corpus_propre/` est construit par `tools/corpus_propre.py` : passages
5: répétés retirés, split par chunks contigus, **zéro fenêtre de validation dans
6: l'entraînement** (vérifié). Ce script évalue un point de contrôle :
7: 
8:   val / test        : in-domain, fenêtres tirées **dans** un chunk (jamais à cheval sur le
9:                       collage de deux chunks, qui est un artefact du split) ;
10:   litterature       : `data/corpus_fr_litterature.txt` (Verne, public domain) — jamais vu ;
11:   anglais           : `data/corpus_en.txt` (Wikipédia) — jamais vu ;
12:   wikitext2         : `data/wikitext2_test.txt` — jamais vu ;
13:   permute           : contrôle négatif, mêmes octets de validation, ordre détruit ;
14:   decomposition     : PPL des têtes précoces (après 2, 4, 6 blocs) et sans la boucle de
15:                       pensée — ce que chaque pièce porte, et ce que l'arrêt précoce coûte ;
16:   longueurs         : PPL à
… [6366 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' work/n2ac/rope_model.py", "description": "Inspect charge_rope signature"}`

  ```
#!/usr/bin/env python3
"""rope_model.py — la variante **positions relatives** du modèle natif (R1.1/R1.2).

Le modèle de `tools/native_model.py` ajoute une **position apprise absolue** (`self.pos`) et
compte sur les positions aléatoires à l'entraînement (N2.j2) : le gain à 512 octets est réel
(÷2,1 à ÷2,4) mais c'est une **astuce d'entraînement**, pas une propriété de l'architecture.
Ce module remplace la position absolue par un **RoPE** (rotation des q/k, aucune position
apprise) : le score d'attention ne dépend plus que de l'**écart** entre positions, donc
l'extrapolation en longueur est acquise par construction.

Rien n'est modifié dans `tools/` : les blocs réutilisent les **mêmes noms de paramètres**
(`ln1`, `qkv`, `out`, `ln2`, `ffn`), ce qui permet de charger un point de contrôle absolu
comme initialisation (`strict=False`, `pos` reste inutilisé).

Usage :
  PYTHONPATH=. python3 -c "from work.n2ac.rope_model import charge_rope; ..."
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from tools.native_model import Block, NativeConfig, NativeModel, exporter_drvm


def rope(x: torch.Tensor, base: float = 10_00
… [2213 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '80,180p' work/n2ac/rope_model.py | grep -n 'def charge_rope' -A12", "description": "Find charge_rope definition"}`

  ```
11:def charge_rope(chemin: str, device: str = "cuda", window: int | None = None):
12-    ck = torch.load(chemin, map_location="cpu", weights_only=False)
13-    cfg = NativeConfig(**{k: v for k, v in ck["config"].items()
14-                          if k in NativeConfig.__annotations__})
15-    if window is not None:
16-        cfg.window = window
17-    m = NativeModelRoPE(cfg).to(device)
18-    m.load_state_dict(ck["state"], strict=False)
19-    m.eval()
20-    return m
21-
22-
23-def exporter(m, chemin: str) -> str:
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python - <<'EOF' 2>&1 | tail -6\nimport tools.eval_n2_propre as e\nfrom work.n2ac.rope_model import charge_rope\nval = e.charger_bytes('data/corpus_propre/va … [266 caractères tronqués]`

  ```
L128 sans canal : 40.0658
L256 sans canal : 49.5308
L512 sans canal : 59.8126
L1024 sans canal : 65.7898
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run documentation review baseline", "timeoutMs": 120000}`

  ```
revue de documentation · 735 fiche(s) · 828 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -60 reports/README.md; echo '---INDEX HEAD---'; head -40 reports/INDEX.md", "description": "Inspect reports README/INDEX"}`

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
| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |
| [`note-panini-334.md`](note-panini-334.md) | **Panini** — la note à envoyer : H0 reproduite, β époque non, la collinéarité |
| [`rapport-panini-334.md`](rapport-panini-334.md)
… [8726 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,240p' tools/revue_documentation.py", "description": "Read documentation review checks"}`

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
… [8301 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '240,420p' tools/revue_documentation.py", "description": "Rest of documentation review"}`

  ```
if not (RACINE / p).exists():
                ligne = texte[: m.start()].count("\n") + 1
                alertes.append(f"chemin mort : {f.relative_to(RACINE)}:{ligne} → {p}")

    # 7b. orphelins : tout document vivant doit avoir au moins un lien entrant
    entrants: set[pathlib.Path] = set()
    for f in sources_nav():
        try:
            texte = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for cible in liens(texte):
            if cible.startswith(("http://", "https://", "mailto:")):
                continue
            p = (f.parent / cible).resolve()
            if p.suffix == ".md":
                entrants.add(p)
    for p in docs_vivants():
        if p.resolve() not in entrants:
            alertes.append(f"navigation : {p.relative_to(RACINE)} n'a aucun lien entrant")

    # 7b bis. les fiches glossaire sont toutes listées dans l'index du dossier
    cartes = sorted((RACINE / "docs/theorie/glossaire/entrees").glob("*.md"))
    if cartes:
        idx_cartes = RACINE / "docs/theorie/glossaire/README.md"
        if not idx_cartes.exists():
            alertes.append("glossaire : docs/theorie/glossaire/README.md manq
… [5453 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -E '3,09|3\\.09|3,196|3\\.196|3,0904' reports/rapport-n2-porte-propre.md reports/n2-porte-propre.json | head -20", "description": "Find 3.09 in gate report"}`

  ```
reports/rapport-n2-porte-propre.md:10:> Les deux bras battent la chaîne honnête de N2.h (val **3,0904**, test **3,1960**). Et la
reports/rapport-n2-porte-propre.md:18:corpus dédupliqué, split par chunks, **0 % de fuite**). La chaîne honnête y valait **3,0904** avec
reports/rapport-n2-porte-propre.md:34:  canal fourni), et le protocole N2.h pour la comparaison à 3,0904.
reports/rapport-n2-porte-propre.md:45:| N2.h, chaîne honnête (référence) | 3,0904 | — | — | — | 3,1960 | — | — |
reports/rapport-n2-porte-propre.md:84:4. **Les deux bras battent la chaîne honnête de N2.h** (3,0904 val / 3,1960 test) : à 2,9027 et
reports/rapport-n2-porte-propre.md:97:  la comparaison à 3,0904 est **indicative**, la comparaison entre les deux bras est contrôlée.
reports/n2-porte-propre.json:85:  "temoin": "N2.h : val 3,0904, test 3,1960",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py --help 2>&1 | head -20; echo '---'; sed -n '1,80p' tools/index_reports.py", "description": "Inspect index generator"}`

  ```
usage: index_reports.py [-h] [--verifier] [--aide]

Génère reports/INDEX.md (déterministe).

options:
  -h, --help  show this help message and exit
  --verifier  ne réécrit rien : compare l'index au disque, sort 1 s'il est
              périmé
  --aide      affiche l'aide et sort
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
    for ligne in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if li
… [1677 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py --verifier; echo \"INDEX_VERIF=$?\"; ls reports/*.md | wc -l; ls reports/*.json | wc -l", "description": "Check index freshness and counts"}`

  ```
INDEX_VERIF=0
735
828
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/propre512-8k.pt --rope --canal-dir data/corpus_propre --longueurs 128 >/tmp/c1_argparse.out 2>&1; echo \"EXIT=$?\"; tail -2 /tmp/c1_argparse.out; echo '---tmp co … [107 caractères tronqués]`

  ```
EXIT=2
                         point
eval_longueurs.py: error: unrecognized arguments: --canal-dir data/corpus_propre
---tmp copy---
-rw-------. 1 stephane stephane 7710 13 nov 21:44 /tmp/eval_n2_propre_rope.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,30p' reports/rapport-n2-porte-propre.md; echo '---N2H refs---'; grep -n -E 'N2\\.h|3,0904|3,1960' reports/rapport-n2-porte-propre.md | head", "description": "Read gate report header"}`

  ```
# N2 — La porte < 2,5 sur le corpus propre, attaquée avec la fenêtre

> **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-03 · **Verdict** :
> la porte **< 2,5 n'est pas atteinte** : le meilleur point est **2,7856** en
> validation et **2,8566** en test (fenêtre 512, contexte 1 024) — il manque **0,29**. Mais la
> fenêtre est le **seul bras dont la courbe descend avec la longueur** : à octets égaux (33 Mo),
> la fenêtre 512 fait **2,9726 → 2,8443 → 2,7856** de 128 à 1 024 octets, quand la fenêtre 128
> fait **2,9027 → 3,0464 → 3,1107** : elle gagne à courte longueur, puis elle est **0,33
> derrière** à 1 024.
> Les deux bras battent la chaîne honnête de N2.h (val **3,0904**, test **3,1960**). Et la
> **capacité ne ferme pas la porte** : à fenêtre 512, init aléatoire et 33 Mo vus, 11,47 M donne
> 2,8960 à 1 024 octets, 21,65 M 2,8688, 34,3 M **2,8662** — elle **sature** à 21,65 M et laisse
> encore **0,37**.

## La question

La porte de N2 est **PPL < 2,5 sur le corpus propre**, tenu à l'écart par construction (N2.h :
corpus dédupliqué, split par chunks, **0 % de fuite**). La chaîne honnête y valait **3,0904** avec
la recette à fenêtre 128 ; la porte était à **
… [1632 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -E 'canal-dir|--rope|add_argument|def charge' /tmp/eval_n2_propre_rope.py | head -30", "description": "Inspect patched /tmp tool options"}`

  ```
2:"""Copie de travail /tmp : eval_n2_propre.py + --rope + --canal-dir + --longueurs liste.
24:def charger_bytes(chemin) -> torch.Tensor:
28:def charger_canal(chemin) -> torch.Tensor:
32:def charge(chemin, device="cuda", rope=False):
119:    ap.add_argument("point")
120:    ap.add_argument("--chunk", type=int, default=8192)
121:    ap.add_argument("--corpus-dir", default="data/corpus_propre",
123:    ap.add_argument("--longueurs", nargs="?", const="129,192,256,384,512,1024",
126:    ap.add_argument("--decomposition", action="store_true")
127:    ap.add_argument("--sortie", default=None)
128:    ap.add_argument("--device", default="cuda")
129:    ap.add_argument("--rope", action="store_true",
131:    ap.add_argument("--canal-dir", default=None,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python /tmp/eval_n2_propre_rope.py work/n2ac/propre512-8k.pt --rope --canal-dir data/corpus_propre --longueurs 128,256,512,1024 2>&1 | tail -4", "description … [66 caractères tronqués]`

  ```
{"fichier": "propre512-8k.pt", "params": 34301224, "val": 2.9726, "test": 3.0807, "litterature": 52.2935, "litterature_propre": 53.7013, "anglais": 117.4252, "wikitext2": 117.7308, "permute": 1673.4162, "longueurs": {"128": 2.9726, "256": 2.8988, "512": 2.8443, "1024": 2.7856}}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%Y-%m-%d %H:%M %Z'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/propre512-8k.pt --rope --longueurs 1024 --val data/corpus_propre 2>&1 | tail -2", "de … [63 caractères tronqués]`

  ```
2026-11-15 02:09 EST
  L1024 : 2.7856
{"fichier": "propre512-8k.pt", "val": "data/corpus_propre", "positions": "rope", "L1024": 2.7856}
  ```

### 👤 Utilisateur

background job bash-13 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l tools/eval_n2_propre.py work/n2ac/eval_longueurs.py reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json; echo '--- git status N2 ---'; git status --short tools/eval_n2_propre.py work/n2ac/eval_longueurs.py reports/rapport-coordination-n2.md; echo '--- grep canal in work ---'; grep -rn 'canal-dir' work/ tools/ 2>/dev/null | head -10) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_list** `{}`

  ```
bash-8 [bash] running — cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -ld tools/n2 2>&1; ls -la tools/n2 2>&1 | head; echo "---"; find tools -maxdepth 2 -iname '*n2*' 2>/dev/null; echo "---git log file---"; git log --oneline -- work/n2ac/eval_longueurs.py | head; echo "---canal-dir grep---"; grep -rn -- '--canal-dir' --include='*.py' --include='*.sh' --include='*.md' . 2>/dev/null | grep -v '.git/' | head -20
bash-13 [bash] completed — cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l tools/eval_n2_propre.py work/n2ac/eval_longueurs.py reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json; echo '--- git status N2 ---'; git status --short tools/eval_n2_propre.py work/n2ac/eval_longueurs.py reports/rapport-coordination-n2.md; echo '--- grep canal in work ---'; grep -rn 'canal-dir' work/ tools/ 2>/dev/null | head -10
  ```

- **job_kill** `{"job_id": "bash-8", "reason": "Recherche large devenue inutile ; les faits sont vérifiés."}`

  ```
requested cancellation of job bash-8
  ```

### 🤖 Assistant

All key figures are re-verified at current HEAD. Now writing the v2 report.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md", "content": "# N2 — la commande validée : le canal avec RoPE, et le témoin 3,09 qui ne doit pas bouger\n\n> **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-15 · **HEAD mesuré … [15205 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "{\n  \"version\": 2,\n  \"date\": \"2026-11-15\",\n  \"head\": \"5891ef8a\",\n  \"ligne\": \"N2\",\n  \"objet\": \"coordination N2, suite de J4.1 : la commande validée, la commande interdite, le test de non-régression\",\n  \"fiche\": \"reports/rapport-coordination-n2-v2.md\",\n  \"v1\" … [12057 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'N2 — en pause\\|N — le natif\\|fichiers / JSON\\|Mis à jour' docs/pilotage/en-cours.md", "description": "Locate lines to edit in en-cours"}`

  ```
3:**Mis à jour : 2026-11-15, 01 h 50 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**
89:- **N2 — en pause** : **1 024** = recette ; **2 048 fini** ; distillation mesurée ; prochaine : **porte propre (0,29)** ; **GPUs libres**.
106:| fichiers / JSON de résultats | **735** / **828** | `reports/*.md` / `reports/*.json` |
119:| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 (manque **0,2856** val / **0,3566** test) ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 01 h 50 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**", "new_string": "**Mis à jour : 2026-11-15, 02 h 15 HNE (tagger : 95,75 % sur 612, 95,00 % sur le rée … [42 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 150}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 01 h 50 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
11: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
12: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
13: - **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
14: - **État** : **en pause** depuis le 05/11 (dernier heartbeat) ; la clôture J14.1 est portée par `e181ce02`.
15: - **Bloquants** : aucun.
16: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
17: 
18: ## Sessions en cours
19: 
20: > Contrat : [`continuite.md`](../methode/continuite.md) · s
… [11881 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 01 h 50 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**", "new_string": "**Mis à jour : 2026-11-15, 02 h 15 HNE (tagger : 95,75 % sur 612, 95,00 % sur le rée … [42 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **N2 — en pause** : **1 024** = recette ; **2 048 fini** ; distillation mesurée ; prochaine : **porte propre (0,29)** ; **GPUs libres**.", "new_string": "- **N2 — en pause** : **1 024** = rece … [412 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **735** / **828** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **736** / **829** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 (manque **0,2856** val / **0,3566** test) ; **N3 couvert** (17 portes, … [561 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 55}`

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
18: | [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |
19: | [
… [4109 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-coordination-n2.md`](rapport-coordination-n2.md) | **N2** — le mètre RoPE : 8,0225 → |\n| [`rapport-coordination-n2-v2.md`](rapport-coordination-n2-v2.md) | **N2** — la commande validée : `- … [187 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py && python3 -m json.tool reports/rapport-coordination-n2-v2.json >/dev/null && echo JSON-OK && python3 tools/index_reports.py --verifier && echo INDEX-OK", "description": "Regenerate index and validate J … [5 caractères tronqués]`

  ```
733 fiches → reports/INDEX.md
JSON-OK
INDEX-OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -20; echo \"REVUE=${PIPESTATUS[0]}\"", "description": "Run documentation review after edits", "timeoutMs": 120000}`

  ```
revue de documentation · 736 fiche(s) · 829 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo \"EN_COURS=${PIPESTATUS[0]}\"", "description": "Validate en-cours state", "timeoutMs": 120000}`

  ```
en-cours · 1683 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN_COURS=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -20; echo \"TAILLE=${PIPESTATUS[0]}\"", "description": "Check document size budget", "timeoutMs": 120000}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2323    214   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4053 mots (budget 4 000)

  avertissements :
     · 51 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [120 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, re\nf = pathlib.Path('reports/rapport-coordination-n2-v2.md')\nt = f.read_text()\nmissing=[]\nfor c in re.findall(r'\\]\\(([^)#]+?)\\)', t):\n    if c.startswith(('http://','https://','mailto:')): c … [204 caractères tronqués]`

  ```
LIENS_MANQUANTS []
MOTS 2211
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,180p' tools/taille_documents.py", "description": "Inspect size budget tool"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, re, subprocess\ndef mots(t): return len(re.findall(r'\\S+', t))\ncur = pathlib.Path('docs/pilotage/en-cours.md').read_text()\nbase = subprocess.check_output(['git','show','HEAD:docs/pilotage/en-cour … [714 caractères tronqués]`

  ```
cur en-cours 1683 base en-cours 1625 delta 58
AGENTS 1196
max method (1174, 'continuite.md')
T0 cur 4053
T0 base 3995
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/pilotage/en-cours.md | head -80", "description": "Show en-cours diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index bf2d714b..c30bb1cd 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 01 h 50 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**
+**Mis à jour : 2026-11-15, 02 h 15 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452 ; N2 : commande validée, 2,7856)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -86,7 +86,7 @@
 ## Ce qui est en cours
 
 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
-- **N2 — en pause** : **1 024** = recette ; **2 048 fini** ; distillation mesurée ; prochaine : **porte propre (0,29)** ; **GPUs libres**.
+- **N2 — en pause** : **1 024** = recette ; **2 048 fini** ; distillation mesurée ; **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856** à 1 024 ; test 2,8566) ; **ne pas utiliser `--rope` sans canal** (**40,0658**) ; `porte-n2.sh` **proposée** : le témoin absolu N2.h **3,09** (3,0971) doit rester **3,09** ; [coor
… [3382 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 02 h 15 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**", "old_string": "**Mis à jour : 2026-11-15, 02 h 15 HNE (tagger : 95,75 % sur 612, 95,00 % sur le rée … [42 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **N2 — en pause** : **2 048 fini** ; **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2](../../reports/rapport-coordination … [517 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 (manque **0,2856** val / **0,3566** test) ; **[v2 : 3,09 tenu](../../r … [629 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, re\ndef mots(t): return len(re.findall(r'\\S+', t))\ncur=pathlib.Path('docs/pilotage/en-cours.md').read_text()\na=mots(pathlib.Path('AGENTS.md').read_text())\nspecifiques={\"organisation-du-depot.md … [383 caractères tronqués]`

  ```
en-cours 1634 T0 4004
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4004 mots (budget 4 000)

  avertissements :
     · 51 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4004 mots (AGENTS + en-cours + une tâche) > budget 4 000
TAILLE=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2](../../reports/rapport-coordination-n2-v2.md) ; proc … [295 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.", "old_string": "- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux)."}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep -E 'T0 max|violation|✅|❌'; echo \"TAILLE=${PIPESTATUS[0]}\"", "description": "Recheck T0 after trims", "timeoutMs": 120000}`

  ```
T0 max : 3997 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
TAILLE=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md", "new_string": "La ligne **N2 — en pause** de [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md) est\nmise à jour avec : la commande validée (`--rope --val <dir>`, 2,7856), l'interdiction d … [719 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json", "new_string": "    \"changement\": \"ligne N2 : commande validée eval_longueurs.py --rope --val <dir> (2,7856), --rope seul sans canal = 40,0658, lien v2, prochaine porte propre ; ligne N : lien  … [458 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-coordination-n2-v2.json >/dev/null && echo JSON-OK && python3 tools/revue_documentation.py 2>&1 | tail -5; echo \"REVUE=${PIPESTATUS[0]}\"", "description": "Validate JSON and rerun review", "timeo … [14 caractères tronqués]`

  ```
JSON-OK
  revue de documentation · 736 fiche(s) · 829 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -5; echo \"EN_COURS=${PIPESTATUS[0]}\"; python3 tools/taille_documents.py 2>&1 | grep -E 'T0 max|✅|❌'; echo \"TAILLE=${PIPESTATUS[0]}\"; python3 tools/index_reports.py --verifier; echo \" … [83 caractères tronqués]`

  ```
en-cours · 1627 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN_COURS=0
  T0 max : 3997 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
TAILLE=0
INDEX=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && stat -c '%y %n' work/n2ac/eval_longueurs.py work/n2ac/rope_model.py tools/eval_n2_propre.py tools/native_model.py 2>&1; echo '--- tracked changes (ours) ---'; git status --short reports/rapport-coordination-n2-v2.md reports/rapport-c … [253 caractères tronqués]`

  ```
2026-11-02 16:22:40.367604569 -0500 work/n2ac/eval_longueurs.py
2026-11-02 16:21:33.673694726 -0500 work/n2ac/rope_model.py
2026-11-01 07:17:12.146387511 -0500 tools/eval_n2_propre.py
2026-11-01 18:32:09.381528369 -0500 tools/native_model.py
--- tracked changes (ours) ---
 M docs/pilotage/en-cours.md
 M reports/INDEX.md
 M reports/README.md
?? reports/rapport-coordination-n2-v2.json
?? reports/rapport-coordination-n2-v2.md
--- diffstat ---
 docs/pilotage/en-cours.md | 10 +++++-----
 reports/INDEX.md          |  3 ++-
 reports/README.md         |  1 +
 3 files changed, 8 insertions(+), 6 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/hooks/ | grep -v sample; echo '---'; sed -n '1,180p' tools/verifie_etat_a_jour.py", "description": "Inspect commit hook requirements"}`

  ```
pre-commit
---
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
  python3 to
… [6077 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat .git/hooks/pre-commit", "description": "Read pre-commit hook"}`

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
… [234 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md", "new_string": "C'est le piège : `--rope` corrige l'**architecture**, pas l'**entrée manquante**. Le checkpoint de la\nporte a été entraîné avec `--canal data/corpus_propre/train.canal`\n(`work/n2ac … [900 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md", "new_string": "**3,0971** est dans la classe de la chaîne honnête N2.h publiée (**3,0904** val / **3,1960** test,\n[`rapport-n2-porte-propre.md`](rapport-n2-porte-propre.md)) : c'est le **3,09** à  … [622 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json", "new_string": "      \"pourquoi\": \"--rope corrige l'architecture, pas l'entrée manquante : le checkpoint de la porte a été entraîné avec --canal data/corpus_propre/train.canal. Sans canal, la P … [516 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json", "new_string": "        \"note\": \"Architecture absolue : la courbe monte aussi (8 → 38,5). Les deux modes faux sont au-dessus de 2,79.\"", "old_string": "        \"note\": \"Architecture absolue … [76 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json", "new_string": "      \"verdict\": \"3,0971 est dans la classe de 3,0904 / 3,1960 : c'est le 3,09 à ne pas casser. Avec canal, ce checkpoint rend 10,99 (v1) : le canal ne s'ajoute pas à un modèle  … [310 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v … [283 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 (manque **0,2856** val / **0,3566** test) ; **[v2](../../reports/rappo … [548 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md", "new_string": "La ligne **N2 — en pause** de [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md) est\nmise à jour avec : la commande validée (`--rope --val <dir>`, 2,7856), l'interdiction d … [724 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json", "new_string": "    \"changement\": \"ligne N2 : commande validée eval_longueurs.py --rope --val <dir> (2,7856), --rope seul sans canal = 40,0658, invariant « v2 : 3,09 tenu », lien v2, puis porte … [427 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-coordination-n2-v2.json >/dev/null && echo JSON-OK; python3 tools/taille_documents.py 2>&1 | grep -E 'T0 max|✅|❌'; echo \"TAILLE=${PIPESTATUS[0]}\"", "description": "Check JSON and T0 after reword … [26 caractères tronqués]`

  ```
JSON-OK
  T0 max : 3996 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
TAILLE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -4; echo \"REVUE=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo \"EN_COURS=${PIPESTATUS[0]}\"", "description": "Rerun review and state checks", "timeoutMs": … [8 caractères tronqués]`

  ```
revue de documentation · 736 fiche(s) · 829 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  en-cours · 1626 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN_COURS=0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md</path>
<type>file</type>
<content>
1: # N2 — la commande validée : le canal avec RoPE, et le témoin 3,09 qui ne doit pas bouger
2: 
3: > **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-15 · **HEAD mesuré** :
4: > `5891ef8a` · **Verdict** : la mesure **2,79** est celle du couple **RoPE + canal**, rejouée
5: > **2,9726 / 2,8988 / 2,8443 / 2,7856** de 128 à 1 024 octets. **`--rope` sans canal rend
6: > 40,0658** à 128 et **65,7898** à 1 024 : c'est la commande à ne pas utiliser. La commande du
7: > mandat, `eval_longueurs.py --rope --canal-dir <dir>`, **n'existe pas telle quelle** :
8: > `--canal-dir` est le drapeau du correctif `eval_n2_propre.py` (validé en copie `/tmp`), et
9: > `eval_longueurs.py` fournit le canal par `--val <dir>`. Le test `porte-n2.sh` proposé doit tenir
10: > **deux** invariants : la porte RoPE + canal à **2,7856**, et le témoin absolu N2.h à **3,09**
11: > (mesuré **3,0971** en validation, **3,2098** en test). **Aucun fichier de `tools/n2/` ni de
12: > `work/n2ac/` n'a été modifié.**
13: 
14: **En trois lignes.** (1) La commande validée, exécutab
… [15424 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md", "new_string": "**Le point clé** : ici `--val data/corpus_propre` **est** le canal. `eval_longueurs.py` lit\ntoujours `val.canal` (ligne 44 du script) ; il n'y a pas de mode « sans canal ». C'est po … [599 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md", "new_string": "| `eval_n2_propre.py --rope` seul (copie `/tmp`) | **non** | 40,0658 | 49,5308 | 59,8126 | 65,7898 |", "old_string": "| `eval_n2_propre.py --rope` seul | **non** | 40,0658 | 49,5308  … [23 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --check -- docs/pilotage/en-cours.md reports/README.md reports/INDEX.md && echo DIFF-CHECK-OK; python3 -m json.tool reports/rapport-coordination-n2-v2.json >/dev/null && echo JSON-OK", "description": "Check whitespace and JS … [4 caractères tronqués]`

  ```
DIFF-CHECK-OK
JSON-OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && if [ -x tools/porte-tableaux.sh ]; then bash tools/porte-tableaux.sh 2>&1 | tail -15; echo \"TABLEAUX=${PIPESTATUS[0]}\"; else echo 'pas de porte-tableaux'; fi", "description": "Run table gate", "timeoutMs": 180000}`

  ```
✅ 1806 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4310 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
TABLEAUX=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schemas.py 2>&1 | tail -8; echo \"SCHEMAS=${PIPESTATUS[0]}\"", "description": "Verify schemas unaffected", "timeoutMs": 120000}`

  ```
schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
SCHEMAS=0
  ```

### 🤖 Assistant

All checks pass. I'll commit only the five C1 files (explicit paths), then re-verify the state.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-coordination-n2-v2.md reports/rapport-coordination-n2-v2.json reports/README.md reports/INDEX.md docs/pilotage/en-cours.md && python3 tools/verifie_etat_a_jour.py --index; echo \"HOOK_PRE=${PIPESTATUS[0]}\"",  … [53 caractères tronqués]`

  ```
✅ index : aucun fait stagé sans état
HOOK_PRE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09\" -- reports/rapport-coordination-n2-v2.md reports/rapport-coordination-n2-v2.json reports/README.md reports/INDEX.md do … [154 caractères tronqués]`
