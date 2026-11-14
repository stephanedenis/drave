# Session DSH — relecture

- identifiant : `session-6b997dd9-9a2e-4d72-b31a-5a6d40609d56`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 04:43:42
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J11.3 : re-mesurer les 50 textes libres avec le code de la semaine (F1 0,7902, le schéma v2, la restitution) : plantages, chevauchements (les deux vues), les 8 champs, le temps. Fiche `reports/rapport-robustesse-semaine.md` + JSON, comparaison avec l'audit A26.

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

- **bash** `{"command": "ls -la && echo \"---\" && ls reports/ | head -50 && echo \"---\" && ls docs/pilotage/", "description": "List workspace root and reports"}`

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
drwxr-xr-x. 1 stephane stephane   180 14 nov 04:43 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   972 14 nov 00:51 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 75656 14 nov 04:37 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run
… [2141 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"0,7902\\|0.7902\\|J11.3\\|A26\" --include=\"*.md\" --include=\"*.json\" --include=\"*.py\" . | head -60", "description": "Search for task identifiers"}`

  ```
./reports/kfold-pidgin-7.json:112:   "chrf": 48.465090579028505,
./reports/kfold-asp-0066.json:17:   "chrf": 48.465090579028505,
./reports/semantique-mesures.json:130:    "contrastif": 0.8844119310379028,
./reports/cerveau-mesures-corrigees.json:67382:        "moyenne": 0.037902954430324036,
./reports/m7-frequence.json:8328:     -0.0879027306248892
./reports/rapport-composition-sans-perte.md:8:> **Le défaut de composition** (audit A26 : « la fusion dégrade le POS de 1,16 pt et perd 14 spans
./reports/rapport-re-test-produit.md:4:> **Ce que le produit fait sur les 50 textes de l'audit A26**, rejoués sur le code du 06/11 21 h :
./reports/rapport-re-test-produit.md:49:- [`rapport-fiabilite-produit.md`](rapport-fiabilite-produit.md) — l'audit A26.
./reports/rapport-etat-a.md:123:  (comme A23, A24, A26, A29). Il ne doit pas figurer dans l'inventaire A.
./reports/rapport-etat-a.md:146:- **Collision d'identifiants** : `rapport-re-test-produit.md` appelle l'audit CLI « **A26** » —
./reports/rapport-etat-a.md:147:  homonyme de la ligne **A2.6**. Les audits A17/A23/A24/A26/A29 ne sont pas des lignes de roadmap.
./reports/rapport-etat-a.md:219:  les fiches A24/A26 sont des instantanés et le c
… [6434 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"J11\" reports/*.md reports/*.json docs/ journal/ 2>/dev/null | head -40", "description": "Find J11 task references"}`

  ```
reports/INDEX.md
reports/rapport-bilan-chantier.md
reports/rapport-evaluer-langue.md
reports/rapport-exemples-rejoues.md
reports/evaluer-langue.json
reports/rapport-bilan-chantier.json
reports/rapport-exemples-rejoues.json
docs/pilotage/semaine-autonome.md
docs/pilotage/roadmap.md
docs/pilotage/en-cours.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/session.jsonl.zstd
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/session.jsonl.zstd
journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/session.jsonl.zstd
journal/sessions/8734fc13-aeb8-4cdf-b005-c182f77be0dc/session.jsonl.zstd
journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/session.jsonl.zstd
journal/sessions/482522d1-31f1-43eb-ae9c-a681336404f7/session.jsonl.zstd
journal/sessions/49721012-99c1-4d9c-967a-eee41f25ff2e/session.v4.jsonl.zstd
journal/sessions/4a342d0f-bf6c-433f-bac9-c5a960b89a7f/session.v4.jsonl.zstd
journal/sessions/54621513-76ae-401e-87df-a5084cacb359/session.v4.jsonl.zstd
journal/sessions/d629d7d7-e122-4596-8757-f4264a2b15cf/session.v4.jsonl.zstd
journal/sessions/f0969e87-af0c-43b1-93cf-f278d9c90846/session.v4.jsonl.zstd
journal/sessions/fc167f70-be8b-4c63-be5e-3c0d3c0ba1c3/session.v4.jsonl.zst
… [1239 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-re-test-produit.md", "description": "Read product retest report"}`

  ```
# B13 — re-test produit : 50 textes libres, la vue linéaire supprime les chevauchements

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Ce que le produit fait sur les 50 textes de l'audit A26**, rejoués sur le code du 06/11 21 h :
> en vue **`alternative`** (défaut), 405 segments et **145 chevauchements** ; en vue **`filtrer`**,
> 297 segments et **0 chevauchement**. Les **5 textes sans syntagme** sont l'emoji, le texte vide,
> les espaces, `...` et un nombre nu — des entrées **non linguistiques**, pas des échecs.
>
> **Dispositif** : `tools/bloc_linguistique.py` (`Heuristique(partition=...)`), les 50 textes de
> [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json) ; JSON
> [`pensee-re-test-produit.json`](pensee-re-test-produit.json).

## 1. Les chiffres

| vue | segments | chevauchements | textes sans syntagme |
|---|---:|---:|---:|
| **`alternative`** (défaut) | 405 | **145** | 5 |
| **`filtrer`** (linéaire) | 297 | **0** | 5 |

**Ce que ça dit** :

- **La vue linéaire fait exactement ce qu'elle promet** : 0 chevauchement sur les textes libres.
- **Les 5 sans syntagme sont légitimes** : 🚀, `""`, `"   "`, `"..."`, `"1234567890"
… [1159 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"J11\" docs/pilotage/semaine-autonome.md | head -40; echo \"===\"; grep -n \"J11\" docs/pilotage/roadmap.md | head -40; echo \"===\"; grep -n \"J11\" docs/pilotage/en-cours.md | head -40", "description": "Locate J11 sections"}`

  ```
179:**A6.2**, la **passe générique d'honnêteté**, puis **J11–J13** (produit, Panini §334/CIC, table des
251:**La suite.** **J11.1–J11.4** (produit : exemples, par-langue, robustesse, schéma documenté) ;
===
66:**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
72:[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**
73:(`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
75:**J11.2 — la mesure par langue.** `evaluer --par-langue` expose le détail **fr/en** (POS,
83:JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
===
63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.2** (produit : [exemples](..
… [996 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-restitution-v1.md", "description": "Read restitution v1 report head"}`

  ```
# B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : J8.1 · **Date** : 2026-11-14 ·
> **Verdict** : ✅
>
> **La question.** Au-delà de la surface exacte (46/46), produire une **forme canonique**
> depuis l'annotation — **segments + rôles + cibles** — et la mesurer : le **miroir strict**
> (0,1087) doit-il monter ?
>
> **La réponse.** **Non — et il ne doit pas.** Le miroir strict compare une sortie à la
> **surface brute** ; la forme canonique replie la casse, retire la ponctuation et réduit
> les espaces. Contre la source canonisée, elle est exacte **46/46 = 1,0000** ; contre la
> source brute, elle tombe à **1/46 = 0,0217** (seul `f18`, `1234567890`, n'a ni casse ni
> ponctuation). Le **miroir strict reste 5/46 = 0,1087** : la v1 ne fabrique pas de
> surface, elle mesure autre chose. Le chiffre utile de la v1 est **1,0000 canonique**,
> pas 0,1087 strict.
>
> **Le chiffre.** 46 annotations, **46/46 formes canoniques exactes** contre la source
> canonisée ; **395 segments**, **395 rôles**, **315 cibles**, **315/315 cibles résolues**
> dans la source, **313/315** portées par un autre segment 
… [4781 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '55,100p' docs/pilotage/roadmap.md", "description": "Read roadmap J11 section"}`

  ```
**J10.1 — le bilan du chantier.** **20 tâches sur 21** passent l'acceptation ; **5 timeouts**
(J1.2, J2.2, J3.1, J5.2, J8.1), dont **4 récupérés** par une acceptation verte ou le commit de la
tâche suivante, et **1 vrai échec** (J5.2, le tag absent). Le produit gagne **2 attachements**
(236 → 238 labels) et **+0,0369 de F1** (0,7533 → 0,7902), la POS ne bouge pas ; Panini est
**mesuré et borné** (table 14/14, corpus 418/438, retrieval J3.1, généalogie J3.2, familles
J7.1) ; la coordination N2/S/R/A est **datée**. La **clôture formelle** reste à faire : **J14.1**
doit refaire la passe et poser le tag `chantier-2026-11-14`. Le détail — chiffres, décisions
D1–D20, rejets R1–R30, échecs, reste — est dans
[`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON.

**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
avec le code courant ; **4 sont corrigés** : la ponctuation finale entre dans le POS (`g001`,
`r241`), le refus sort en **3** et `r035` — l'ancien échec connu — rend exactement le gold
(`REL [9:24] « she talks about » → film`). Le seul bloc identique est `g011`. F1 **0,7902**,
attachement **238/238 labels** (238/
… [2853 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '235,290p' docs/pilotage/semaine-autonome.md; echo \"=== en-cours ===\"; sed -n '1,140p' docs/pilotage/en-cours.md", "description": "Read semaine-autonome and en-cours"}`

  ```
| F1 syntagmes | 0,7533 | **0,7902** (+0,0369) | [convention](../../reports/rapport-convention-gv.md) |
| attachement | 236/237 labels (236/239 cibles, 0,9916) | **238/238 labels** (238/239 cibles, 0,9958) | [s065](../../reports/rapport-s065.md) |
| produit | schéma v1 ; restitution v0 46/46, miroir 0,1087 | schéma **v2** (26/0) ; restitution **v1** canonique 46/46, strict 0,1087, **395/395/315/313** | [v1](../../reports/rapport-restitution-v1.md) |
| tagger | 0,8625 | **0,9475** (+8,49) ; réel 432 **+4,67** | [R](../../reports/rapport-coordination-r.md) |
| Panini | 0 mesure | table **14/14** ; corpus **418/438** ; retrieval **script +0,609** ; généalogie **154/154** ; familles **0,619 contre 0,0445** | [familles](../../reports/rapport-retrieval-familles.md) |
| portes / tag | 84 portes | **84, 81 vertes, 3 rouges tolérées** ; **tag absent** | [références](references-non-regression.md) |

**Les décisions.** **D1–D20** : le produit (relative zéro, convention GV, schéma v2, restitution,
`g017` rejeté, `s065` intégré, forme canonique), Panini (table, corpus, retrieval, généalogie,
séparation sœur/famille), la coordination (N2, S, R, A) et la méthode (encart qui pointe,
acceptation d'
… [12934 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"8 champs\\|huit champs\\|8 fields\\|les 8\\|schéma v2\\|schema v2\" --include=\"*.md\" --include=\"*.py\" --include=\"*.json\" docs reports tools | head -40", "description": "Search for the 8 fields and schema v2"}`

  ```
docs/archive/architecture-kimi-k3.md:188:7 168) : `ffn_routed_down` (7168→3584), les 896 experts (`gate/up/down`, 3 072 de
docs/archive/etat-emulation-professeur.md:148:langue**. Ajuster les 896 dimensions densément revient à ajuster massivement du
docs/archive/etat-emulation-professeur.md:349:qu'on choisit en lui. En visant le sous-ensemble actif plutôt que les 896 canaux
docs/archive/etat-emulation-professeur.md:424:   **seulement à la dernière position**. Sur l'ensemble du texte, **les 896 canaux
docs/archive/note-cancellation-evenementielle.md:104:recherche aléatoire, sur les 8 sorties les plus énergétiques :
docs/archive/note-chemin-court-n4.md:75:| **B** | **adaptateurs par couche** (LoRA sur les 8 premières) | rang faible sur q/k/v/o | moyen (rétropropagation à travers 8 couches) | les couches basses peuvent-elles apprendre à rendre leur état lisible ? |
docs/archive/plan-deepseek41-complet.md:452:> formats. Il n'est pas un signe de défaut de calcul — les 88,9 % de top-1
docs/archive/plan-mla-vision.md:181:`n_wa_pattern = 8` confirme le point délicat annoncé : **toutes les 8 couches,
docs/pilotage/plan-travail.md:41:| **D/R/A — terminé (02/11)** | les corpus (texte intégral,
… [5166 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/ | grep -i \"produit\\|libre\\|restitution\\|schema\\|bloc\" ; echo ---; ls tools/tests/ | grep -i \"produit\\|libre\\|restitution\\|schema\"", "description": "Find relevant tools and tests"}`

  ```
approximabilite_bloc.py
bloc_code.py
bloc_linguistique.py
bloc_maths.py
bloc_tableaux.py
calibre_modes.py
calibrer.py
essai_blocs.py
hebbien_produits.py
iterer_bloc.py
mesurer_restitution_v0.py
mesurer_restitution_v1.py
porte-bloc-code.sh
porte-bloc-linguistique.sh
porte-bloc-maths.sh
porte-bloc-tableaux.sh
porte-miroir-blocs.sh
porte-produit.sh
ref_ggml_bloc.c
restitution.py
restitution_udhr.py
schemas
v41_attention_blocs.py
verifier_schema_produit.py
verifier_schemas.py
vision_bloc_ref.py
---
test_produit_libre.py
test_produit.py
test_restitution.py
test_schema_produit.py
  ```

- **bash** `{"command": "sed -n '1,200p' reports/rapport-schema-v2.md", "description": "Read schema v2 report"}`

  ```
# B13 — le schéma v2 : `meta.partition` et `meta.alternative` typés, version 2, v1 toujours lue

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.3 · **Date** : 2026-11-07 ·
> **Verdict** : ✅
> **Ce qui change pour un client** : l'annotation porte `schema: "drave.annotation"` et
> `version: 2`. Le schéma v2 publie les deux champs qui documentent les syntagmes qui se
> chevauchent : `meta.partition` (`{groupe, rang, membres, vue}`) et `meta.alternative` (la liste
> des autres segments du groupe, avec `relation`, `union`, `rang`, `retire`, `role`,
> `attachement`). Les champs sont **additifs** : un client qui ne lit pas `meta` continue de lire
> l'annotation. **La version 1 reste lue** : `verifier_schema_produit.py` choisit le schéma
> d'après `version`, et un **contrôle négatif** vérifie que le schéma v2 refuse bien une
> annotation v1.
>
> **Dispositif** : [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json),
> [`drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json) (inchangé),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`VERSION_ANNOTATION = 2`),
> [`verifier_schema_produit.py`](../tools/verifier_schema_produit.
… [4868 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nd=json.load(open('tools/schemas/drave-annotation-v2.json'))\nprint(json.dumps(d,indent=1,ensure_ascii=False)[:4000])\n\"", "description": "Print schema v2 JSON"}`

  ```
{
 "$schema": "https://json-schema.org/draft/2020-12/schema",
 "$id": "https://drave.local/schema/annotation-v2.json",
 "title": "drave.annotation v2",
 "description": "L'annotation du bloc linguistique heuristique, version 2 : identique à la v1 et documente, dans `meta`, la partition des syntagmes qui se chevauchent (`meta.partition`) et les segments alternatifs du groupe (`meta.alternative`). Les deux champs sont additifs et optionnels : v1 reste lue.",
 "type": "object",
 "required": [
  "schema",
  "version",
  "texte",
  "langue",
  "script",
  "refus",
  "etiquettes",
  "unites_semantiques"
 ],
 "properties": {
  "schema": {
   "const": "drave.annotation"
  },
  "version": {
   "const": 2
  },
  "texte": {
   "type": "string"
  },
  "langue": {
   "type": "string",
   "pattern": "^[a-z]{2,3}$|^und$"
  },
  "script": {
   "type": "string"
  },
  "source": {
   "type": "string"
  },
  "refus": {
   "type": "string",
   "enum": [
    "",
    "vide",
    "non_texte",
    "trop_long",
    "neuronal"
   ]
  },
  "etiquettes": {
   "type": "array",
   "items": {
    "type": "object",
    "required": [
     "niveau",
     "type",
     "valeur",
     "debut",
     "fin",
     "source"
… [2787 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nfor f in ['reports/pensee-re-test-produit.json','reports/pensee-fiabilite-produit.json']:\n    d=json.load(open(f))\n    print('==',f,'type',type(d).__name__)\n    print(list(d)[:20] if isinstance(d,dict) else len(d))\n\"", "description": "Inspect retest and  … [12 caractères tronqués]`

  ```
== reports/pensee-re-test-produit.json type dict
['date', 'ligne', 'banc', 'alternative', 'filtrer', 'sans_syntagme', 'temps_s', 'limites']
== reports/pensee-fiabilite-produit.json type dict
['rapport', 'ligne', 'branche', 'commit_mesure', 'commit_module', 'date', 'objet', 'verdict', 'snapshot', 'dispositif', 'banc_50', 'robustesse', 'contrat', 'schema_propose', 'test_non_regression', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
  ```

- **bash** `{"command": "sed -n '1,160p' tools/tests/test_produit_libre.py", "description": "Read 50-text test"}`

  ```
#!/usr/bin/env python3
"""test_produit_libre.py — non-régression sur les **50 textes libres** de l'audit A26.

Ce que le test fige :
- la vue **`filtrer`** ne produit **aucun** chevauchement de syntagmes (0/50) ;
- la vue **`alternative`** (défaut) documente les chevauchements dans `meta.alternative` ;
- les **5 textes non linguistiques** (emoji, vide, espaces, ponctuation, nombre nu) n'ont
  **aucun** syntagme ;
- l'analyse est **déterministe** (deux passes identiques).
"""
from __future__ import annotations

import json
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
NON_LINGUISTIQUES = {"f14", "f15", "f16", "f17", "f18"}


def _textes() -> list[tuple[str, str]]:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    return [(item["id"], item["texte"]) for item in donnees["banc_50"]["resultats"]]


def _segments(annotation) -> list:
    return [e for e in annotation.etiquettes if e.niveau == "syntagme"]


def _chevauchements(segments: list) -> int:
    return sum(1 for i, a in enumerate(segments) for b in segments[i + 1:]
           
… [1439 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' reports/rapport-fiabilite-produit.md", "description": "Read audit A26 report"}`

  ```
# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 23/46 textes à chevauchement de syntagmes

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `56eb43af` (module `c1a08588`, `tools/drave.py` `59a06f3e`) ·
> **Date** : 2026-11-06 · **Verdict** : ⚠️ **la surface est fiable ; le contrat ne l'est pas encore.**
> **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
> [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json).
>
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) (CLI : `analyser`, `evaluer`, `rejouer`,
> `--version`) et [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) ;
> **50 phrases libres** écrites pour l'audit (textes dans le JSON) ; harnais local non committé
> dans `/tmp` ; machine **Xeon E5-2687W v3**, Python **3.13.16**.
>
> **Snapshot.** HEAD a bougé pendant l'audit (`6ef2a3f5` → `56eb43af`). Le module a reçu à
> **11 h 34** le correctif « non-str / surrogate » (`c1a08588`) ; le banc a tourné à **11 h 40**,
> après ce correctif, et `drave.py` n'a pas changé. Les chiffres portent sur ce couple de hash ;
> un audit futur doit repa
… [9685 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nd=json.load(open('reports/pensee-re-test-produit.json'))\nprint(json.dumps(d,indent=1,ensure_ascii=False))\n\"", "description": "Print product retest JSON"}`

  ```
{
 "date": "2026-11-06",
 "ligne": "B13",
 "banc": "50 textes de pensee-fiabilite-produit.json",
 "alternative": {
  "segments": 405,
  "chevauchements": 145,
  "sans_syntagme": 5
 },
 "filtrer": {
  "segments": 297,
  "chevauchements": 0,
  "sans_syntagme": 5
 },
 "sans_syntagme": [
  "🚀",
  "",
  "   ",
  "...",
  "1234567890"
 ],
 "temps_s": 0.13,
 "limites": [
  "justesse non mesurée",
  "définition du chevauchement",
  "comparaison audit non à définition constante"
 ]
}
  ```

- **bash** `{"command": "sed -n '1,240p' tools/mesurer_restitution_v1.py", "description": "Read restitution v1 measurement script"}`

  ```
#!/usr/bin/env python3
"""mesurer_restitution_v1.py — produit le JSON de la fiche J8.1.

Mesure la **forme canonique v1** sur les **50 textes libres** de
`reports/pensee-fiabilite-produit.json` (le banc de l'audit A26) et écrit
`reports/pensee-restitution-v1.json`. La fiche `reports/rapport-restitution-v1.md`
cite ce JSON.

La v1 ne remplace pas la v0 : elle ajoute une lecture **structurelle** (segments +
rôles + cibles) et un **miroir canonique** comparé à une source canonisée. Le miroir
strict (surface brute) reste mesuré, pour que la réponse à « doit-il monter ? » soit
vérifiable.

    python3 tools/mesurer_restitution_v1.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import tools.restitution as restitution  # noqa: E402

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
SORTIE = RACINE / "reports" / "pensee-restitution-v1.json"

LIMITES = [
    "Le miroir canonique vaut 1,0000 **par construction** : les jetons viennent des "
    "spans `mot`/`pos`, qui sont des sous-chaînes de la 
… [3239 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Heuristique\\|def analyser\\|VERSION_ANNOTATION\\|partition\" tools/bloc_linguistique.py | head -40; echo ---; grep -n \"def restituer\\|def forme_canonique\\|def miroir_canonique\\|def mesurer_banc_v1\" tools/restitution.py", "description": "Locate key functions"}`

  ```
92:# v2 : ajoute `meta.partition` et `meta.alternative` (partition des syntagmes qui se
94:VERSION_ANNOTATION = 2
128:            "schema": SCHEMA_ANNOTATION, "version": VERSION_ANNOTATION,
141:    def analyser(self, texte: str, langue: str | None = None,
796:class Heuristique:
803:                 union: bool = True, partition: str = "alternative"):
812:        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
814:        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
815:            raise ValueError("partition attend 'brut', 'alternative', 'filtrer_union' ou 'filtrer'")
816:        self.partition = partition
1455:    def analyser(self, texte: str, langue: str | None = None,
1805:        if self.partition != "brut":
1806:            _expliciter_partition(etiquettes, filtrer=(
1807:                "" if self.partition == "alternative"
1808:                else "union" if self.partition == "filtrer_union" else "strict"))
1845:    def analyser(self, texte: str, langue: str | None = None,
1916:    def analyser(self, texte: str, langue: str | None = None,
2026:    def analyser(self, texte: str, langue: str | None = None,
2160:    d
… [1224 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -15; echo ---; git status --short | head -20; echo ---; git rev-parse HEAD; python3 --version", "description": "Check git state and recent commits"}`

  ```
09e54143 J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ
84e393bb J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238
a6808c5e CHANTIER — LE PLAN EST RELU À CHAQUE TOUR (LA BOUCLE VOYAIT UNE FILE VIDE APRÈS UN AJOUT DE TÂCHES) ; ÉTAT HORODATÉ
03ecee41 J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ
81fc9ecf JOURNAL — 2026-11-14 : J9.1 AU RÉCIT (19 FICHES « INSTANTANÉ HISTORIQUE »)
ecef7250 J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT
229098ec J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
d31e8788 J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE
e4288023 J6.2 — PORTE PRODUIT VERTE (183/183) : FIXTURES D'ATTACHEMENT À 238/238, FICHE ET JSON À JOUR
2d6f5bff PORTES — LA PASSE DU 14/11 : 84 PORTES, 81 VERTES, 3 ROUGES (INDICE, MELANGE, SESSIONS DU HUB) ; MANDAT E1
… [1196 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '780,900p' tools/restitution.py", "description": "Read restitution bench functions"}`

  ```
"squelette_identique": sum(
                1 for r in annotes if r["stabilite"]["squelette_identique"]),
            "jetons_identiques": sum(
                1 for r in annotes if r["stabilite"]["jetons_identiques"]),
            "fidelite": round(
                sum(1 for r in annotes if r["stabilite"]["squelette_identique"]) / max(1, n), 4),
        },
        "controle_negatif_canonique": {
            "melange_exacts": sum(
                1 for r in annotes if r["controle_negatif_canonique"]["melange"]["exact"]),
            "melange_fidelite_caractere": moyenne(
                [r["controle_negatif_canonique"]["melange"]["fidelite_caractere"]
                 for r in annotes]),
            "tronque_exacts": sum(
                1 for r in annotes if r["controle_negatif_canonique"]["tronque"]["exact"]),
            "tronque_fidelite_caractere": moyenne(
                [r["controle_negatif_canonique"]["tronque"]["fidelite_caractere"]
                 for r in annotes]),
            "detectes": sum(
                1 for r in annotes if r["controle_negatif_canonique"]["detecte"]),
        },
        "controle_negatif_structure": {
            "eligibles": sum(
             
… [4262 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nb=d['banc_50']\nprint(list(b))\nprint(list(b['resultats'][0]))\nfor r in b['resultats'][:3]:\n    print({k:r[k] for k in r if k!='texte'})\nprint('n=',len(b['resultats']))\nprint('ids=',[r['id'] for  … [76 caractères tronqués]`

  ```
['synthese', 'resultats']
['id', 'categorie', 'attendu', 'texte', 'caracteres', 'octets_utf8', 'rc', 'temps_cli_ms', 'temps_api_ms', 'deterministe', 'json_octets', 'json_valide', 'langue', 'script', 'labels', 'mots', 'pos', 'syntagmes', 'attaches', 'sans_attachement', 'chevauchements_syntagme', 'chevauchements_phrase_type', 'syntagmes_union', 'conflits_apres_filtre_union', 'cibles_fermees', 'cibles_absentes', 'phrases', 'phrases_espaces_initiaux', 'documents', 'doc_tronquees', 'doc_titres', 'unites_semantiques', 'fraction_semantique', 'trous_pos', 'sans_syntagme', 'sans_pos']
{'id': 'f01', 'categorie': 'fr', 'attendu': 'fr', 'caracteres': 13, 'octets_utf8': 13, 'rc': 0, 'temps_cli_ms': 150.79, 'temps_api_ms': 0.796, 'deterministe': True, 'json_octets': 5561, 'json_valide': True, 'langue': 'fr', 'script': 'Latn', 'labels': 19, 'mots': 4, 'pos': 3, 'syntagmes': 2, 'attaches': 2, 'sans_attachement': 0, 'chevauchements_syntagme': 0, 'chevauchements_phrase_type': 0, 'syntagmes_union': 0, 'conflits_apres_filtre_union': 0, 'cibles_fermees': 0, 'cibles_absentes': 0, 'phrases': 1, 'phrases_espaces_initiaux': 0, 'documents': 1, 'doc_tronquees': 0, 'doc_titres': [], 'unites_semantiques': 2, '
… [2104 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def cmd_analyser\\|def _analyser\\|analyser\" tools/drave.py | head -30; echo ---; grep -n \"def items_banc\\|def mesurer_annotation_v1\\|DEFINITION_MIROIR\\|VERSION_CANONIQUE\\|SCHEMA_CANONIQUE\" tools/restitution.py | head", "description": "Locate CLI analyser and restitutio … [8 caractères tronqués]`

  ```
6:    python3 tools/drave.py analyser "Le chat dort."
7:    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
15:Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
171:def _analyser_jsonl(texte: str, args: argparse.Namespace) -> int:
179:        a = h.analyser(phrase, args.langue, args.contexte)
188:def cmd_analyser(args: argparse.Namespace) -> int:
191:        return _analyser_jsonl(texte, args)
192:    annotation = bl.Heuristique(partition=args.partition).analyser(texte, args.langue,
350:    premiere = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
351:    seconde = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
414:    annotation = bl.Heuristique().analyser(texte, args.langue, args.contexte)
463:        "Commandes : analyser, evaluer, rejouer, restituer.\n"
470:        "  python3 tools/drave.py analyser \"Le chat dort.\"\n"
484:                                  metavar="{analyser,evaluer,rejouer,restituer}",
487:    analyser = sous.add_parser(
488:        "analyser",
491:        epilog="Exemple : python3 tools/drave.py analyser \"Le chat dort.\" --j
… [1300 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '165,240p' tools/drave.py; echo \"=== Annotation ===\"; sed -n '100,200p' tools/bloc_linguistique.py; echo \"=== items_banc ===\"; sed -n '250,300p' tools/restitution.py", "description": "Read analyser CLI and Annotation"}`

  ```
"""Le texte : l'argument, ou le **fichier** (`--fichier`)."""
    if getattr(args, "fichier", None):
        return pathlib.Path(args.fichier).read_text(encoding="utf-8", errors="replace")
    return args.texte or ""


def _analyser_jsonl(texte: str, args: argparse.Namespace) -> int:
    """Une **ligne JSON par phrase** (traitement de corpus : `--jsonl`)."""
    h = bl.Heuristique(partition=args.partition)
    n = 0
    for debut, fin, _typ, _ in h._phrases(texte):
        phrase = texte[debut:fin]
        if not phrase.strip():
            continue
        a = h.analyser(phrase, args.langue, args.contexte)
        sys.stdout.write(_sur(json.dumps(a.json(), ensure_ascii=False)) + "\n")
        n += 1
    if n == 0:
        print(f"{NOM}: refus d'analyse : vide", file=sys.stderr)
        return 3
    return 0


def cmd_analyser(args: argparse.Namespace) -> int:
    texte = _lire_entree(args)
    if args.jsonl:
        return _analyser_jsonl(texte, args)
    annotation = bl.Heuristique(partition=args.partition).analyser(texte, args.langue,
                                                                   args.contexte)
    if annotation.refus:
        # un refus est une **réponse** 
… [7919 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"pensee-re-test-produit\\|re-test-produit\\|banc_50\" tools reports/*.md docs | head -30", "description": "Find retest harness references"}`

  ```
tools/__pycache__/restitution.cpython-313.pyc
tools/tests/__pycache__/test_restitution.cpython-313.pyc
tools/tests/test_produit_libre.py
tools/tests/test_restitution.py
tools/restitution.py
reports/INDEX.md
reports/rapport-etat-a.md
reports/rapport-fiabilite-produit.md
reports/rapport-produit-bloc-l.md
reports/rapport-re-test-produit.md
reports/README.md
  ```

- **bash** `{"command": "ls tools/*.py | sed 's#tools/##' | sort | head -100", "description": "List tools python files"}`

  ```
adaptateur_langue.py
aiguille.py
aligneur_litteraire.py
amplification.py
analyse_alignement.py
analyse_empreinte.py
analyse_engram.py
analyse_experts_statique.py
analyse_flux.py
analyse_hc.py
analyse_litteraire.py
analyse_octets_par_jeton.py
analyse_reutilisation_experts.py
analyse_union_experts.py
ancre_professeur.py
applique_pont.py
approximabilite_bloc.py
archive_sessions.py
audit_drapeaux_harnais.py
banc_complet.py
banc_durci.py
banc-experts.py
banc_lecteur.py
banc_lecture.py
banc-prelire.py
blanchiment_entree.py
bloc_code.py
bloc_linguistique.py
bloc_maths.py
bloc_tableaux.py
boucle_directe.py
bruit_entree.py
budget_execution_locale.py
c8_entrainer_tete.py
c8_sonde_lineaire.py
cache_pont.py
calibre_modes.py
calibrer.py
campagne_synthese.py
canal_structure.py
cancellation_langue.py
carte_chantiers.py
carte_decisions.py
carte_langues.py
catalogue_corpus.py
cca_raisonnement.py
census_routage.py
chat.py
clusters_moe.py
code_partage.py
compare_etats.py
compare_genres.py
compare_logits.py
compare_professeurs.py
comparer_noyaux.py
composition_latente.py
composition_multilingue.py
composition_verne.py
construire-niah.py
contenu_par_couche.py
contrastif_hors_echantillon.py
controle_cap
… [737 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/verifier_schema_produit.py", "description": "Read schema verifier"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/drave.py evaluer --json 2>/dev/null | head -c 1200; echo; echo \"rc=$?\"", "description": "Check evaluer JSON output"}`

  ```
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
     "NOUN": 1,
     "VERB": 1
    },
    "CONJ": {
     "PRON": 15,
     "CONJ": 68,
     "?": 13,
     "PREP": 2
    },
    "DET": {
     "DET": 586,
     "?": 2
    },
    "NOUN": {
     "NOUN": 657,
     "ADJ": 17,
     "VERB": 7,
     "?": 1
    },
    "NUM": {
     "NUM": 2
    },
    "PONCT": {
     "PONCT": 25
    },
    "PREP": {
     "PREP": 114
    },
    "PRON": {
     "PRON": 429,
     "?": 30,
     "CONJ": 2,
     "DET": 14
    },
    "VERB": {
     "VERB": 546,
     "NOUN": 218,
     "PREP": 2,
     "ADJ": 2,
     "?": 16,
     "AUX": 7,
     "ADV": 1
    }
   }
  },
  "syntagme": {
   "pre

… [4 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py evaluer --json 2>/dev/null > /tmp/eval.json && python3 -c \"\nimport json\nd=json.load(open('/tmp/eval.json'))\nh=d['heuristique']\nprint(json.dumps({k:h[k] for k in h if k not in ('pos','syntagme')},indent=1)[ … [119 caractères tronqués]`

  ```
{
 "bloc": "heuristique",
 "phrases": 612,
 "pragmatique": {
  "acte": 0.9967,
  "negation": 0.9771,
  "modalite": 0.9886,
  "double_sens": 0.9444
 },
 "fraction_semantique": 0.5476,
 "attachement": {
  "cibles": 239,
  "labels": 238,
  "top1": 238,
  "topk": 236,
  "exact": 238,
  "top1_taux": 0.9958,
  "topk_taux": 0.9874,
  "exact_taux": 0.9958,
  "exact_any": 238,
  "exact_any_taux_span": 1.0,
  "top1_taux_span": 1.0,
  "topk_taux_span": 0.9916,
  "topk_exact": 236,
  "topk_exact_taux": 0.9874,
  "topk_exact_taux_span": 0.9916,
  "exact_taux_span": 1.0,
  "verbe": {
   "cibles": 158,
   "justes": 158,
   "taux": 1.0
  },
  "nom": {
   "cibles": 80,
   "justes": 80,
   "taux": 1.0
  },
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
 "attachement_tete": {
  "cibles": 238,
  "labels": 238,
  "top1": 238,
  "topk": 236,
  "top1_taux": 1.0,
  "topk_taux": 0.9916,
  "couverture": 1.0
 }
}
SYNT {
 "precision": 0.786,
 "rappel": 0.7944,
 "f1": 0.7902,
 "tp":
… [144 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nb=json.load(open('reports/pensee-fiabilite-produit.json'))\nitems=b['banc_50']['resultats']\nfor vue in ('alternative','filtrer','filt … [762 caractères tronqués]`

  ```
alternative segments 411 ov 127 textes_ov 27 sans 5
 refus [('f14', 'vide'), ('f15', 'vide'), ('f16', 'vide'), ('f17', 'vide')]
 sans ['f14', 'f15', 'f16', 'f17', 'f18']
filtrer segments 323 ov 0 textes_ov 0 sans 5
filtrer_union segments 363 ov 41 textes_ov 12 sans 5
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys,time\nsys.path.insert(0,'.')\nimport tools.restitution as r\nb=json.load(open('reports/pensee-fiabilite-produit.json'))\nitems=r.items_banc(b)\nt=time.perf_counter()\nm=r.mesurer_banc_v1(items)\npri … [158 caractères tronqués]`

  ```
duree 12.087022027932107
{
 "n": 50,
 "annotations": 46,
 "refus": 4,
 "refus_ids": [
  "f14",
  "f15",
  "f16",
  "f17"
 ],
 "strict": {
  "exacts": 5,
  "fidelite": 0.1087
 },
 "canonique": {
  "exacts": 46,
  "fidelite": 1.0,
  "fidelite_caractere": 1.0
 },
 "strict_sur_canonique": {
  "exacts": 1,
  "fidelite": 0.0217,
  "fidelite_caractere": 0.8566
 },
 "structure": {
  "segments": 395,
  "segments_avec_role": 395,
  "attachements": 315,
  "cibles_resolues": 315,
  "cibles_dans_un_segment": 313,
  "couverture_caracteres": 0.7519,
  "couverture_jetons": 0.6584,
  "taux_roles": 1.0,
  "taux_cibles_resolues": 1.0,
  "taux_cibles_dans_un_segment": 0.9937
 },
 "stabilite": {
  "squelette_identique": 18,
  "jetons_identiques": 46,
  "fidelite": 0.3913
 },
 "controle_negatif_canonique": {
  "melange_exacts": 0,
  "melange_fidelite_caractere": 0.3865,
  "tronque_exacts": 0,
  "tronque_fidelite_caractere": 0.7998,
  "detectes": 46
 },
 "controle_negatif_structure": {
  "eligibles": 43,
  "detectes": 43,
  "cle_changee": 43,
  "roles_retires": 395,
  "cibles_retirees": 315
 }
}
  ```

- **bash** `{"command": "sed -n '690,780p' tools/restitution.py; echo ===; sed -n '455,540p' tools/restitution.py", "description": "Read mesure annotation v1 detail"}`

  ```
def mesurer_annotation_v1(a: bl.Annotation, source: str, graine: int = 0,
                          analyseur: bl.Heuristique | None = None) -> dict:
    """La restitution v1 d'une annotation : strict (v0) + canonique + structure."""
    base = mesurer_annotation(a, source, graine)
    if a.refus:
        return {
            "langue": a.langue,
            "refus": a.refus,
            "source_caracteres": len(source),
            "source_octets": len(source.encode("utf-8")),
            "etiquettes": len(a.etiquettes),
            "strict": base["miroir"],
            "surface_stricte": base["surface"],
            "canonique": None,
            "forme": None,
            "structure": None,
            "stabilite": None,
            "strict_sur_canonique": None,
            "controle_negatif_canonique": None,
            "controle_negatif_structure": None,
        }
    forme = forme_canonique(a)
    return {
        "langue": a.langue,
        "refus": "",
        "source_caracteres": len(source),
        "source_octets": len(source.encode("utf-8")),
        "etiquettes": len(a.etiquettes),
        "strict": base["miroir"],
        "surface_stricte": base["surface"],
        "ca
… [6503 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nb=json.load(open('reports/pensee-fiabilite-produit.json'))\nitems=b['banc_50']['resultats']\nfor vue in ('alternative','filtrer','filt … [755 caractères tronqués]`

  ```
alternative segments 395 ov 115 textes_ov 21 sans 7
 sans ['f14', 'f15', 'f16', 'f17', 'f18', 'f27', 'f37']
 ov counts {'f02': 2, 'f05': 1, 'f06': 2, 'f10': 1, 'f11': 1, 'f20': 3, 'f21': 2, 'f22': 2, 'f23': 2, 'f24': 5, 'f31': 2, 'f32': 1, 'f34': 2, 'f38': 1, 'f39': 2, 'f41': 3, 'f43': 10, 'f44': 2, 'f45': 4, 'f46': 4, 'f50': 63}
filtrer segments 313 ov 0 textes_ov 0 sans 7
filtrer_union segments 352 ov 40 textes_ov 11 sans 7
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nb=json.load(open('reports/pensee-fiabilite-produit.json'))\nfor it in b['banc_50']['resultats']:\n    if it['id'] in ('f13','f14','f15','f16','f17','f18','f27','f37','f33',' … [505 caractères tronqués]`

  ```
f13 "J'ai trouvé ça génial 😍🔥" attendu fr
f14 '🚀' attendu refus
f15 '' attendu refus
f16 '   ' attendu refus
f17 '...' attendu refus
f18 '1234567890' attendu fr
f27 'Élodie sourit.' attendu fr
f33 'Si tu viens, apporte le dessert.' attendu fr
f37 'Email: alice@example.org, phone: +33 6 12 34 56 78.' attendu fr
f50 "# Notes de terrain\nLe chat de la voisine qui dort sur le toit se réveille dès que le jour se lève ; il descend alors d attendu fr
f13 refus= '' langue= und seg= 2 labels= 30
f14 refus= 'vide' langue= und seg= 0 labels= 0
f15 refus= 'vide' langue= und seg= 0 labels= 0
f16 refus= 'vide' langue= und seg= 0 labels= 0
f17 refus= 'vide' langue= und seg= 0 labels= 0
f18 refus= '' langue= und seg= 0 labels= 7
f27 refus= '' langue= und seg= 0 labels= 14
f37 refus= '' langue= und seg= 0 labels= 66
  ```

- **bash** `{"command": "grep -n \"def _dumps\\|def _sur\" tools/drave.py; sed -n '100,165p' tools/drave.py", "description": "Check CLI JSON serialization"}`

  ```
55:def _sur(s: str) -> str:
60:def _dumps(objet) -> str:
        f"langue={a.langue} script={a.script} source={a.source} · {len(a.etiquettes)} étiquettes "
        f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"
    )

    pos = [e for e in a.etiquettes if e.niveau == "pos"]
    if pos:
        lignes.extend(_envelopper("POS  ", " ".join(f"{e.valeur}/{e.type}" for e in pos)))
    else:
        lignes.append("POS  —")

    syntagmes = [e for e in a.etiquettes if e.niveau == "syntagme"]
    if syntagmes:
        valeurs = [_valeur_affichee(e.valeur, 46) for e in syntagmes]
        roles = [str(e.meta.get("role") or "—") for e in syntagmes]
        cibles = [str((e.meta.get("attachement") or {}).get("cible") or "—") for e in syntagmes]
        spans = [f"[{e.debut}:{e.fin}]" for e in syntagmes]
        lt = max(3, max(len(e.type) for e in syntagmes))
        lsp = max(len(s) for s in spans)
        lv = max(len(v) for v in valeurs)
        lr = max(len(r) for r in roles)
        lignes.append("SYNTAGMES")
        for e, valeur, role, cible, span in zip(syntagmes, valeurs, roles, cibles, spans):
            lignes.append(
                f"  {
… [1766 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '48,70p' tools/drave.py", "description": "Read dumps function"}`

  ```
VERSION = "0.1.0"
LARGEUR = 100


# --------------------------------------------------------------------------- sorties JSON


def _sur(s: str) -> str:
    """Une chaîne toujours **écrivable** : un surrogate isolé devient U+FFFD (jamais d'exception)."""
    return s.encode("utf-8", "replace").decode("utf-8", "replace")


def _dumps(objet) -> str:
    """JSON stable (pas d'horodatage, pas de durée) et lisible."""
    return _sur(json.dumps(objet, ensure_ascii=False, indent=1)) + "\n"


def _canonique(a: bl.Annotation) -> str:
    """La forme comparée par `rejouer` : clés triées, durée exclue, sans espaces inutiles."""
    return _sur(json.dumps(a.json(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))


# --------------------------------------------------------------------------- rendu lisible
  ```

- **bash** `{"command": "sed -n '180,340p' reports/rapport-fiabilite-produit.md", "description": "Read audit A26 rest"}`

  ```
| cas | code attendu | code observé | stdout | constat |
|---|---:|---:|---:|---|
| `--version`, `--aide` | 0 | **0** | oui | conforme |
| aucune commande, commande inconnue, texte manquant | 2 | **2** | 0 | conforme |
| `--langue de`, `--langue FR`, option inconnue | 2 | **2** | 0 | conforme (choix `fr\|en`) |
| texte commençant par `--` (`--bonjour`) | 0 | **2** | 0 | **anomalie** : pris pour une option |
| même texte avec `--` séparateur | 0 | **0** | oui | conforme |
| texte `-3 degrés` | 0 | **0** | oui | conforme (argparse accepte) |
| un mot (`Bonjour`), un caractère (`a`) | 0 | **0** | oui | conforme ; 7 et 8 étiquettes (0 et 1 syntagme) |
| caractères spéciaux (f40 : `@ # $ % & * ( ) [ ] { } < > ~ ^`, barre verticale et antislash) | 0 | **0** | oui | 76 étiquettes, 0 plantage ; la barre et l'antislash sont des tokens de ponctuation |
| texte vide / espace / tabs | 1 | **1** | **0** | conforme, refus |
| ponctuation seule / emoji / espace invisible | 1 | **1** | **0** | refus correct, **raison `vide` fausse** |
| `--json` avant le texte | 0 | **0** | oui | conforme |
| nouvelle ligne, tabulation, CRLF | 0 | **0** | oui | conforme |

Les codes **0 / 1 / 2** existent ; les co
… [8036 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '340,470p' reports/rapport-fiabilite-produit.md", "description": "Read A26 control negative and conclusion"}`

  ```
"type": "object",
      "required": ["niveau", "type", "valeur", "debut", "fin", "source",
                   "confiance", "candidats", "langue", "script", "meta"],
      "properties": {
        "niveau": {"enum": ["graphème", "morphème", "mot", "pos", "syntagme",
                            "phrase", "discours", "pragmatique", "document"]},
        "type": {"type": "string", "minLength": 1},
        "valeur": {"type": "string"},
        "debut": {"type": "integer", "minimum": 0},
        "fin": {"type": "integer", "minimum": 0},
        "source": {"enum": ["heuristique", "neuronal", "humain"]},
        "confiance": {"type": "number", "minimum": 0, "maximum": 1},
        "candidats": {"type": "array", "items": {"type": "string"}},
        "langue": {"type": "string"},
        "script": {"type": "string"},
        "meta": {"type": "object"}
      },
      "additionalProperties": true
    }
  }
}
```

**Politique de version.** MAJOR pour toute suppression, renommage ou changement de type/sémantique
d'un des 8 champs ; MINOR pour un champ optionnel, une valeur de `type` ou un code de `refus`.
`schema` et `version` sont présents **sur succès et sur refus** ; le refus est un code **3** 
… [5029 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/tests/test_schema_produit.py", "description": "Read current schema tests"}`

  ```
#!/usr/bin/env python3
"""test_schema_produit.py — le **contrat** du produit : schéma v2, v1 lue, refus, entrées hostiles.

Ce que le test fige (et qu'un client peut supposer) :
- 8 champs **obligatoires** à la racine : `schema`, `version`, `texte`, `langue`, `script`,
  `refus`, `etiquettes`, `unites_semantiques` ;
- `schema == "drave.annotation"` et `version == 2` ;
- `meta.partition` et `meta.alternative` sont déclarés dans le schéma v2 ;
- une annotation **v1 reste lue** par le vérificateur (schéma v1), et le schéma v2 la refuse ;
- un refus est une **réponse** : JSON valide avec `refus`, code de sortie 3 ;
- un surrogate isolé et une entrée non textuelle ne font pas planter.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_V1 = RACINE / "tools" / "schemas" / "drave-annotation-v1.json"
SCHEMA_V2 = RACINE / "tools" / "schemas" / "drave-annotation-v2.json"
VERIFICATEUR = RACINE / "tools" / "verifier_schema_produit.py"
OBLIGATOIRES = ("schema", "version", "texte", "langue", "script", "refus",
                "etiquettes", "unites_semantiques")


def _cli(*arg
… [3967 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nb=json.load(open('reports/pensee-fiabilite-produit.json'))\na26={r['id']:r for r in b['banc_50']['resultats']}\nprint('A26 total pairs',sum(r['chevauchements_syntagme'] for  … [769 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
  File "<stdin>", line 5, in <genexpr>
KeyError: 'chevauchements_syntagme'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nb=json.load(open('reports/pensee-fiabilite-produit.json'))\nrs=b['banc_50']['resultats']\nprint(len(rs))\nfor r in rs[:2]: print(sorted(r))\nmissing=[r['id'] for r in rs if 'chevauchements_syntagme' no … [85 caractères tronqués]`

  ```
50
['attaches', 'attendu', 'caracteres', 'categorie', 'chevauchements_phrase_type', 'chevauchements_syntagme', 'cibles_absentes', 'cibles_fermees', 'conflits_apres_filtre_union', 'deterministe', 'doc_titres', 'doc_tronquees', 'documents', 'fraction_semantique', 'id', 'json_octets', 'json_valide', 'labels', 'langue', 'mots', 'octets_utf8', 'phrases', 'phrases_espaces_initiaux', 'pos', 'rc', 'sans_attachement', 'sans_pos', 'sans_syntagme', 'script', 'syntagmes', 'syntagmes_union', 'temps_api_ms', 'temps_cli_ms', 'texte', 'trous_pos', 'unites_semantiques']
['attaches', 'attendu', 'caracteres', 'categorie', 'chevauchements_phrase_type', 'chevauchements_syntagme', 'cibles_absentes', 'cibles_fermees', 'conflits_apres_filtre_union', 'deterministe', 'doc_titres', 'doc_tronquees', 'documents', 'fraction_semantique', 'id', 'json_octets', 'json_valide', 'labels', 'langue', 'mots', 'octets_utf8', 'phrases', 'phrases_espaces_initiaux', 'pos', 'rc', 'sans_attachement', 'sans_pos', 'sans_syntagme', 'script', 'syntagmes', 'syntagmes_union', 'temps_api_ms', 'temps_cli_ms', 'texte', 'trous_pos', 'unites_semantiques']
missing ['f14', 'f15', 'f16', 'f17']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nb=json.load(open('reports/pensee-fiabilite-produit.json'))\na26={r['id']:r for r in b['banc_50']['resultats']}\nprint('A26 total pairs',sum(r.get('chevauchements_syntagme',0 … [791 caractères tronqués]`

  ```
A26 total pairs 107
A26 texts with pairs 23
{'f02': 2, 'f05': 1, 'f06': 4, 'f10': 1, 'f11': 1, 'f20': 2, 'f21': 3, 'f22': 2, 'f23': 2, 'f24': 5, 'f26': 1, 'f29': 2, 'f31': 1, 'f32': 1, 'f34': 3, 'f38': 1, 'f39': 2, 'f41': 3, 'f43': 10, 'f44': 2, 'f45': 4, 'f46': 4, 'f50': 50}
CUR total 115 texts 21
{'f02': (2, 2), 'f05': (1, 1), 'f06': (4, 2), 'f10': (1, 1), 'f11': (1, 1), 'f20': (2, 3), 'f21': (3, 2), 'f22': (2, 2), 'f23': (2, 2), 'f24': (5, 5), 'f26': (1, 0), 'f29': (2, 0), 'f31': (1, 2), 'f32': (1, 1), 'f34': (3, 2), 'f38': (1, 1), 'f39': (2, 2), 'f41': (3, 3), 'f43': (10, 10), 'f44': (2, 2), 'f45': (4, 4), 'f46': (4, 4), 'f50': (50, 63)}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nb=json.load(open('reports/pensee-fiabilite-produit.json'))\na26={r['id']:r for r in b['banc_50']['resultats']}\nimport tools.bloc_linguistique as bl\nh=bl.Heuristique()\nfor … [436 caractères tronqués]`

  ```
f06 A26 syn 6 cur 7
f20 A26 syn 7 cur 8
f21 A26 syn 5 cur 5
f26 A26 syn 4 cur 4
  [('REL', 0, 21, 'Où sont les toilettes'), ('GN', 24, 26, 'Je'), ('GV', 27, 34, 'cherche'), ('GP', 35, 53, 'depuis dix minutes')]
f29 A26 syn 5 cur 4
  [('GN', 0, 2, 'Il'), ('GV', 3, 8, 'a dit'), ('GV', 13, 19, 'Rentre'), ('GP', 20, 32, 'avant minuit')]
f31 A26 syn 2 cur 3
f34 A26 syn 6 cur 6
f50 A26 syn 171 cur 193
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"import fastjsonschema; print(fastjsonschema.__version__)\" 2>&1; date -I; git log -1 --format=%H", "description": "Check validator and date"}`

  ```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import fastjsonschema; print(fastjsonschema.__version__)
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'fastjsonschema' has no attribute '__version__'
2026-11-14
09e541435fd9d05e912039905c8a880e8d9ac5c7
  ```

- **bash** `{"command": "sed -n '790,825p' tools/bloc_linguistique.py; sed -n '1455,1485p' tools/bloc_linguistique.py", "description": "Check Heuristique defaults"}`

  ```
ajouter(_absorber_fermants(texte, j), _type_phrase(texte[i:j]))
        i = j
    ajouter(n, "déclarative")
    return sortie


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
        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"
… [2441 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py", "content": "#!/usr/bin/env python3\n\"\"\"mesurer_robustesse_semaine.py — le banc J11.3 sur les **50 textes libres** de l'audit A26.\n\nCe que le banc mesure, avec le code de la semaine (F1 0,7902, s … [25852 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py", "old_string": "        inv = _anneau_vide(a_alt, texte)\n        cli_champs = champs_8\n        api_alt_ok, api_alt_err = _valider_annotation(a_alt.json(), valideurs[2])\n        api_fil_ok, api_fil_ … [526 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py", "new_string": "            \"api_alternative_schema_v2\": api_alt_ok,\n            \"api_filtrer_schema_v2\": api_fil_ok,\n            \"api_alternative_champs_8\": api_alt_champs,\n            \"api … [162 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py", "new_string": "            \"champs_8\": {\n                \"cli_alternative\": sum(1 for r in resultats if r[\"champs_8\"]),\n                \"api_alternative\": sum(1 for r in resultats if r[\"ap … [476 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py", "new_string": "        \"restitution_melange_detecte\": s_v1[\"controle_negatif_canonique\"][\"detectes\"],\n        \"restitution_troncature_detecte\": s_v1[\"controle_negatif_canonique\"][\"detecte … [415 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/mesurer_robustesse_semaine.py", "description": "Run J11.3 measurement", "timeoutMs": 300000}`

  ```
J11.3 — les 50 textes libres re-mesurés
  code : HEAD 09e54143 · F1 0.7902 · POS 0.8625 · attachement 238/239
  plantages 0/50 · refus 4/50 · JSON valide 50/50 · 8 champs 50/50 · schéma v2 50/50
  alternative : 395 segments · 115 chevauchements · 21/46 textes
  filtrer     : 313 segments · 0 chevauchement · 7 textes sans syntagme
  temps CLI   : médiane 155.2 ms (134.4–239.9) · API médiane 2.9 ms
  restitution : canonique 46/46 · strict 5/46 · segments 395
  écrit : reports/pensee-robustesse-semaine.json
[stderr]

real	0m30,007s
user	0m27,778s
sys	0m2,258s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,statistics\nd=json.load(open('reports/pensee-robustesse-semaine.json'))\nts=[r['temps_api_ms'] for r in d['resultats']]\nprint(sorted(ts))\nprint(d['synthese']['temps'])\nprint('top',sorted((r['temps_ap … [262 caractères tronqués]`

  ```
[0.0, 0.0, 0.1, 0.1, 0.6, 0.8, 1.0, 1.3, 1.5, 1.5, 1.7, 1.8, 1.9, 1.9, 2.2, 2.4, 2.4, 2.5, 2.5, 2.6, 2.6, 2.8, 2.8, 2.8, 2.9, 2.9, 2.9, 2.9, 3.0, 3.2, 3.3, 3.5, 3.5, 3.5, 3.6, 3.9, 3.9, 3.9, 4.0, 4.2, 4.2, 4.4, 4.4, 4.8, 5.4, 5.9, 8.9, 11.5, 18.6, 70.0]
{'cli_ms': {'n': 50, 'min': 134.4, 'mediane': 155.2, 'moyenne': 156.9, 'p95': 168.1, 'max': 239.9, 'total': 7842.8}, 'api_ms': {'n': 50, 'min': 0.0, 'mediane': 2.9, 'moyenne': 4.7, 'p95': 11.5, 'max': 70.0, 'total': 232.9}, 'api_filtrer_ms': {'n': 50, 'min': 0.0, 'mediane': 2.5, 'moyenne': 3.9, 'p95': 5.9, 'max': 59.0, 'total': 193.0}, 'restitution_s': 12.03}
top [(4.4, 'f45'), (4.8, 'f41'), (5.4, 'f20'), (5.9, 'f38'), (8.9, 'f02'), (11.5, 'f01'), (18.6, 'f43'), (70.0, 'f50')]
CLI [(134.4, 'f17'), (138.6, 'f16'), (138.9, 'f24'), (142.1, 'f42'), (144.0, 'f25')] [(167.5, 'f22'), (167.7, 'f47'), (168.1, 'f35'), (168.3, 'f05'), (239.9, 'f50')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-robustesse-semaine.json'))\ns=d['synthese']\nfor k in ('plantages','codes','stderr_succes','json_valide','champs_8','schema_v2','determinisme','alternative','filtrer',' … [303 caractères tronqués]`

  ```
plantages 0
codes {"0": 46, "3": 4}
stderr_succes 0
json_valide 50
champs_8 {"cli_alternative": 50, "api_alternative": 50, "api_filtrer": 50}
schema_v2 {"cli_alternative": 50, "api_alternative": 50, "api_filtrer": 50}
determinisme 50
alternative {"segments": 395, "chevauchements": 115, "textes_avec_chevauchement": 21, "textes_sans_syntagme": 7, "textes_avec_syntagme": 43}
filtrer {"segments": 313, "chevauchements": 0, "textes_avec_chevauchement": 0, "textes_sans_syntagme": 7, "textes_avec_syntagme": 43}
filtrer_union {"segments": 352, "chevauchements": 40, "textes_avec_chevauchement": 11}
sans_syntagme {"total": 7, "ids": ["f14", "f15", "f16", "f17", "f18", "f27", "f37"], "annotations": 3, "ids_annotations": ["f18", "f27", "f37"]}
invariants {"spans_hors_texte": 0, "spans_vides": 0, "cibles_absentes": 0, "etiquettes": 4827}
controles_negatifs {"schema_v1_lue": {"attendu": true, "observe": true}, "schema_v2_refuse_v1": {"attendu": true, "observe": false}, "schema_v2_refuse_champ_manquant": {"attendu": true, "observe": false}, "chevauchement_injecte": {"attendu": 1, "observe": 1, "temoin_sans_chevauchement": 0}, "filtrer_non_vide": {"attendu": "> 0", "observe": 313}, "restitution_mel
… [354 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.verifier_schema_produit import SCHEMAS\nimport fastjsonschema\ns=json.load(open(SCHEMAS[2]))\nprint('version prop',s['proper … [711 caractères tronqués]`

  ```
version prop {'const': 2}
v2 PASS
v1 FAIL JsonSchemaValueException data.version must be same as const definition: 2
missing refus FAIL JsonSchemaValueException data must contain ['refus'] properties
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.verifier_schema_produit import SCHEMAS, OBLIGATOIRES\nimport fastjsonschema\nschemas = {v: json.loads(p.read_text(encoding=' … [847 caractères tronqués]`

  ```
{1: <function validate_https___drave_local_schema_annotation_v1_json at 0x7f82696bb9c0>, 2: <function validate_https___drave_local_schema_annotation_v2_json at 0x7f82696e0fe0>} {1: PosixPath('/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v1.json'), 2: PosixPath('/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v2.json')}
v1 field 1 v1_lue (True, '')
v2_refuse_v1 (False, 'data.version must be same as const definition: 2')
v2_refuse_champ (False, "data must contain ['refus'] properties")
  ```

- **bash** `{"command": "grep -n \"v2_refuse\\|_valider_annotation\\|temoin\\|sans_champ\\|v1_lue\" tools/mesurer_robustesse_semaine.py", "description": "Inspect control block"}`

  ```
135:def _valider_annotation(annotation: dict, valideur) -> tuple[bool, str]:
238:                schema_ok, schema_erreur = _valider_annotation(annotation_cli, valideur)
266:        api_alt_ok, api_alt_err = _valider_annotation(api_alt_json, valideurs[2])
267:        api_fil_ok, api_fil_err = _valider_annotation(api_fil_json, valideurs[2])
336:    temoin = h_alt.analyser("Le chat dort.")
337:    temoin_json = temoin.json()
338:    v1 = json.loads(json.dumps(temoin_json))
345:    v1_lue, _ = _valider_annotation(v1, valideurs[1])
346:    v2_refuse_v1, _ = _valider_annotation(v1, valideurs[2])
347:    sans_champ = json.loads(json.dumps(temoin_json))
348:    sans_champ.pop("refus", None)
349:    v2_refuse_champ_manquant, _ = _valider_annotation(sans_champ, valideurs[2])
351:    seg_temoin = _segments(temoin)
352:    injecte = seg_temoin + seg_temoin[:1]  # duplique un segment : une paire qui se chevauche
354:    base_sans = len(_chevauchements(seg_temoin))
359:        "schema_v1_lue": {"attendu": True, "observe": v1_lue},
360:        "schema_v2_refuse_v1": {"attendu": True, "observe": v2_refuse_v1},
361:        "schema_v2_refuse_champ_manquant": {"attendu": True, "observe": v2_refuse_c
… [71 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py", "new_string": "    # Chauffe : on ne veut pas attribuer au premier texte le coût d'import du module ni\n    # la compilation des expressions régulières du bloc.\n    _cli(\"Le chat dort.\")\n    h_al … [240 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py", "new_string": "    v1_lue, _ = _valider_annotation(v1, valideurs[1])\n    v2_accepte_v1, _ = _valider_annotation(v1, valideurs[2])\n    v2_refuse_v1 = not v2_accepte_v1\n    sans_champ = json.loads(j … [510 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/mesurer_robustesse_semaine.py", "description": "Rerun J11.3 measurement", "timeoutMs": 300000}`

  ```
J11.3 — les 50 textes libres re-mesurés
  code : HEAD 09e54143 · F1 0.7902 · POS 0.8625 · attachement 238/239
  plantages 0/50 · refus 4/50 · JSON valide 50/50 · 8 champs 50/50 · schéma v2 50/50
  alternative : 395 segments · 115 chevauchements · 21/46 textes
  filtrer     : 313 segments · 0 chevauchement · 7 textes sans syntagme
  temps CLI   : médiane 159.2 ms (142.3–257.7) · API médiane 2.7 ms
  restitution : canonique 46/46 · strict 5/46 · segments 395
  écrit : reports/pensee-robustesse-semaine.json
[stderr]

real	0m30,250s
user	0m27,896s
sys	0m2,380s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-robustesse-semaine.json'))\nprint(json.dumps(d['synthese']['controles_negatifs'],indent=1,ensure_ascii=False))\nprint(json.dumps(d['synthese']['temps'],indent=1))\nprin … [205 caractères tronqués]`

  ```
{
 "schema_v1_lue": {
  "attendu": true,
  "observe": true
 },
 "schema_v2_refuse_v1": {
  "attendu": true,
  "observe": true
 },
 "schema_v2_refuse_champ_manquant": {
  "attendu": true,
  "observe": true
 },
 "chevauchement_injecte": {
  "attendu": 1,
  "observe": 1,
  "temoin_sans_chevauchement": 0
 },
 "filtrer_non_vide": {
  "attendu": "> 0",
  "observe": 313
 },
 "restitution_melange_detecte": 46,
 "restitution_troncature_detecte": 46,
 "restitution_melange_exacts": 0,
 "restitution_troncature_exacts": 0,
 "restitution_roles_retires": 395,
 "restitution_cibles_retirees": 315
}
{
 "cli_ms": {
  "n": 50,
  "min": 142.3,
  "mediane": 159.2,
  "moyenne": 160.4,
  "p95": 175.4,
  "max": 257.7,
  "total": 8017.8
 },
 "api_ms": {
  "n": 50,
  "min": 0.0,
  "mediane": 2.7,
  "moyenne": 4.4,
  "p95": 6.4,
  "max": 74.0,
  "total": 220.8
 },
 "api_filtrer_ms": {
  "n": 50,
  "min": 0.0,
  "mediane": 2.5,
  "moyenne": 3.9,
  "p95": 6.7,
  "max": 61.4,
  "total": 194.5
 },
 "restitution_s": 12.04
}
{
 "head": "09e541435fd9d05e912039905c8a880e8d9ac5c7",
 "drave": "0.1.0",
 "schema_annotation": 2,
 "sha256_schemas": {
  "1": "87d0bdb8527869cb1c92f0aa0318677c9beeade679682080ca222685c86cf04a"
… [1456 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nb=json.load(open('reports/pensee-fiabilite-produit.json'))\na26={r['id']:r.get('chevauchements_syntagme',0) for r in b['banc_50']['resultats']}\nd=json.load(open('reports/pensee-robustesse-semaine.json … [456 caractères tronqués]`

  ```
f06: 4 -> 2
f20: 2 -> 3
f21: 3 -> 2
f26: 1 -> 0
f29: 2 -> 0
f31: 1 -> 2
f34: 3 -> 2
f50: 50 -> 63
sum a26 107 sum cur 115
texts a26 23 texts cur 21
top cur [(63, 'f50'), (10, 'f43'), (5, 'f24'), (4, 'f46'), (4, 'f45'), (3, 'f41')]
  ```

- **bash** `{"command": "grep -n \"J11.1\\|J11.2\\|restitution-v1\\|schema-v2\\|rapport-re-test-produit\\|robustesse\" reports/INDEX.md | head -20; echo ---; sed -n '70,95p' reports/INDEX.md; echo ---; sed -n '110,130p' reports/INDEX.md", "description": "Inspect reports index"}`

  ```
173:| [rapport-exemples-rejoues.md](rapport-exemples-rejoues.md) | J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec |
486:| [rapport-pensee-graines.md](rapport-pensee-graines.md) | B13 — la robustesse sur 5 graines : le curriculum `open` tient |
671:| [rapport-re-test-produit.md](rapport-re-test-produit.md) | B13 — re-test produit : 50 textes libres, la vue linéaire supprime les chevauchements |
675:| [rapport-restitution-v1.md](rapport-restitution-v1.md) | B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087 |
680:| [rapport-robustesse-produit.md](rapport-robustesse-produit.md) | B13 — la robustesse du produit : un surrogate ne plante plus, une entrée non-str est refusée |
696:| [rapport-schema-v2.md](rapport-schema-v2.md) | B13 — le schéma v2 : `meta.partition` et `meta.alternative` typés, version 2, v1 toujours lue |
---
| [rapport-b10-mots-jw.md](rapport-b10-mots-jw.md) | B10 — le décodeur mot sur JW : 26,7 contre un plancher de 17,1 (+9,5), mais le `z` ne porte que 1,9 point |
| [rapport-b102bis-capacite.md](rapport-b102bis-capacite.md) | B10.2bis — la capacité : 31,77 M contre 9,29 M, le décodeur ne bouge
… [6447 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"INDEX.md\" tools/*.py | head -20; echo ---; sed -n '1,40p' reports/INDEX.md; echo ---; sed -n '670,700p' reports/INDEX.md", "description": "Inspect index generation and section"}`

  ```
tools/index_reports.py:2:"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.
tools/index_reports.py:5:avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
tools/index_reports.py:10:    python3 tools/index_reports.py              # réécrit reports/INDEX.md
tools/index_reports.py:32:        if p.name not in ("README.md", "INDEX.md") and not p.name.startswith("historique-")
tools/index_reports.py:42:        "> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;",
tools/index_reports.py:53:    ap = argparse.ArgumentParser(description="Génère reports/INDEX.md (déterministe).")
tools/index_reports.py:61:    sortie = RACINE / "reports/INDEX.md"
tools/index_reports.py:67:    print(f"  {len(fiches())} fiches → reports/INDEX.md")
tools/surveille_sessions.py:33:            "docs/pilotage/README.md", "AGENTS.md", "reports/INDEX.md",
tools/taille_documents.py:128:        if p.name in ("README.md", "INDEX.md") or p.name.startswith("historique-"):
---
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **722 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `histor
… [8651 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- reports/INDEX.md | head -60; echo ---; git diff --stat | head -20", "description": "Check existing index diff"}`

  ```
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 5506faf4..23f34a66 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **718 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **722 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -78,6 +78,7 @@
 | [rapport-b13-porte-134.md](rapport-b13-porte-134.md) | B13 — la porte est à 134/140 : le 140/140 de 702b368c ne se rejoue pas ; quatre rouges viennent du sous-module S |
 | [rapport-b13-porte-138.md](rapport-b13-porte-138.md) | B13 — la porte est à 138/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 restent |
 | [rapport-b13-porte-140.md](rapport-b13-porte-140.md) | B13 — la porte est à 140/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 alignés sur 2/5 (distracteurs r428–r432) |
+| [rapport-bilan-chantier.md](rapport-bilan-chantier.md) | J10.1 — le bilan du chantier : F1 0,7533 → 0,7902, attachement 236 → 238, Panini mesuré et borné |
 | [rapport-b
… [5331 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal/2026-11-14/ && echo --- && sed -n '1,120p' journal/2026-11-14/README.md && echo --- && sed -n '1,80p' journal/2026-11-14/mesures.md", "description": "Read journal entry structure"}`

  ```
docs.md
memoire.md
mesures.md
portes.md
README.md
---
# 2026-11-14

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**12 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 3 | [docs.md](docs.md) |
| memoire | 2 | [memoire.md](memoire.md) |
| mesures | 5 | [mesures.md](mesures.md) |
| portes | 2 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 324.0 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:52 | `64d9dd23` | J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PER
… [8645 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nb=json.load(open('reports/pensee-fiabilite-produit.json'))\nh=bl.Heuristique()\nn=c=0\nfor r in b['banc_50']['resultats']:\n    a=h.ana … [395 caractères tronqués]`

  ```
labels 4827 cibles 315
labels measured 4827
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfor t in ['Élodie sourit.','Email: alice@example.org, phone: +33 6 12 34 56 78.','1234567890']:\n    for lg in (None,'fr'):\n        a=bl.He … [244 caractères tronqués]`

  ```
'Élodie sourit.' langue None -> und seg 0 []
'Élodie sourit.' langue fr -> und seg 1 [('GV', 'Élodie sourit')]
'Email: alice@example.org,' langue None -> und seg 0 []
'Email: alice@example.org,' langue fr -> und seg 4 [('GV', 'Email'), ('GV', 'alice@example'), ('GV', 'org'), ('GV', 'phone')]
'1234567890' langue None -> und seg 0 []
'1234567890' langue fr -> und seg 0 []
  ```

- **write** `{"content": "# J11.3 — les 50 textes libres : 0 plantage, 50/50 au schéma v2, 115 chevauchements en `alternative`, 0 en `filtrer`\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **J11.3** · **Date** : 2026-11-14 ·\n> **Verdict** : ✅\n>\n> **Commit mesuré** : `09e54143` — **F1 0,7902**, * … [13747 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-robustesse-semaine.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-robustesse-semaine.json'))\ns=d['synthese']\nprint(json.dumps(s['temps'],ensure_ascii=False))\nprint(json.dumps(s['alternative'],ensure_ascii=False))\nprint(json.dumps( … [619 caractères tronqués]`

  ```
{"cli_ms": {"n": 50, "min": 142.3, "mediane": 159.2, "moyenne": 160.4, "p95": 175.4, "max": 257.7, "total": 8017.8}, "api_ms": {"n": 50, "min": 0.0, "mediane": 2.7, "moyenne": 4.4, "p95": 6.4, "max": 74.0, "total": 220.8}, "api_filtrer_ms": {"n": 50, "min": 0.0, "mediane": 2.5, "moyenne": 3.9, "p95": 6.7, "max": 61.4, "total": 194.5}, "restitution_s": 12.04}
{"segments": 395, "chevauchements": 115, "textes_avec_chevauchement": 21, "textes_sans_syntagme": 7, "textes_avec_syntagme": 43}
{"segments": 313, "chevauchements": 0, "textes_avec_chevauchement": 0, "textes_sans_syntagme": 7, "textes_avec_syntagme": 43}
{"segments": 352, "chevauchements": 40, "textes_avec_chevauchement": 11}
f13 {'segments': 2, 'chevauchements': 0, 'sans_syntagme': False}
f27 {'segments': 0, 'chevauchements': 0, 'sans_syntagme': True}
f37 {'segments': 0, 'chevauchements': 0, 'sans_syntagme': True}
f43 10
f50 63
invariants {'spans_hors_texte': 0, 'spans_vides': 0, 'cibles_absentes': 0, 'etiquettes': 4827}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py && git diff --stat -- reports/INDEX.md && grep -n \"rapport-robustesse-semaine\" reports/INDEX.md", "description": "Regenerate reports index"}`

  ```
724 fiches → reports/INDEX.md
 reports/INDEX.md | 9 ++++++++-
 1 file changed, 8 insertions(+), 1 deletion(-)
682:| [rapport-robustesse-semaine.md](rapport-robustesse-semaine.md) | J11.3 — les 50 textes libres : 0 plantage, 50/50 au schéma v2, 115 chevauchements en `alternative`, 0 en `filtrer` |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"J11.2\\|J11.3\\|J11.4\" docs/pilotage/roadmap.md docs/pilotage/en-cours.md docs/pilotage/semaine-autonome.md", "description": "Locate J11 mentions"}`

  ```
docs/pilotage/roadmap.md:72:[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**
docs/pilotage/roadmap.md:73:(`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
docs/pilotage/roadmap.md:75:**J11.2 — la mesure par langue.** `evaluer --par-langue` expose le détail **fr/en** (POS,
docs/pilotage/roadmap.md:83:JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
docs/pilotage/en-cours.md:63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.2** (produit : [exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md)) ; **contrat v1**, **`drave` v0**.
docs/pilotage/en-cours.md:94:- **J11.1/J11.2** : 5/5 
… [1023 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"La suite\" docs/pilotage/roadmap.md | head; grep -n \"J11\" docs/pilotage/roadmap.md", "description": "Check roadmap suite lines"}`

  ```
72:[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**
83:JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
66:**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
72:[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**
73:(`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
75:**J11.2 — la mesure par langue.** `evaluer --par-langue` expose le détail **fr/en** (POS,
83:JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '75,86p' docs/pilotage/roadmap.md", "description": "Read roadmap J11.2 paragraph"}`

  ```
**J11.2 — la mesure par langue.** `evaluer --par-langue` expose le détail **fr/en** (POS,
syntagmes, attachement, pragmatique, contrôle négatif recalculé par langue) sans changer le
global. **fr** : 402 phrases, POS **0,8159**, F1 **0,7475**, attachement **151/151** ; **en** :
210 phrases, POS **0,9451**, F1 **0,8656**, attachement **87/88** (span 87/87). L'anglais est
devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le
réel seul, l'écart tient (POS 0,9451 contre 0,8408 ; F1 0,8656 contre 0,7258) — il reste
**confondu avec la source**. Le test vérifie la non-régression (`--par-langue` ne change pas
`heuristique`) et la cohérence des comptes. [`fiche`](../../reports/rapport-evaluer-langue.md) +
JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).

**La vue d'ensemble des chantiers** — huit chantiers (A, B, N, R, **S**, **L**, **D**, B13), leurs relations, leurs chemins critiques et les tensions à trancher — est dans [`chantiers.md`](chantiers.md) ; la carte est [`chantiers-vision.svg`](../schemas/chantiers-vision.svg) ; le **plan de travail multi-sessions** (qui fait quoi, où, à quelle cadence) est dan
… [103 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qrineç/tools/..", "old_string": "JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).\n\n**La vue d'ensemble des chantiers**", "new_string": "JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** … [935 caractères tronqués]`

  ```
Error: cannot resolve "/home/stephane/Data13TB/stephane/GitHub/Qrineç/tools/..": parent traversal crosses a missing directory
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).\n\n**J11.3 — les 50 textes libres.** Les **50 phrases de l'audit A26** sont rejouées avec le\ncode du 14/ … [952 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 60, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
60: **mesuré et borné** (table 14/14, corpus 418/438, retrieval J3.1, généalogie J3.2, familles
61: J7.1) ; la coordination N2/S/R/A est **datée**. La **clôture formelle** reste à faire : **J14.1**
62: doit refaire la passe et poser le tag `chantier-2026-11-14`. Le détail — chiffres, décisions
63: D1–D20, rejets R1–R30, échecs, reste — est dans
64: [`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON.
65: 
66: **J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
67: avec le code courant ; **4 sont corrigés** : la ponctuation finale entre dans le POS (`g001`,
68: `r241`), le refus sort en **3** et `r035` — l'ancien échec connu — rend exactement le gold
69: (`REL [9:24] « she talks about » → film`). Le seul bloc identique est `g011`. F1 **0,7902**,
70: attachement **238/238 labels** (238/239 cibles, 0,9958) ; le mandat 237/238 est l'état d'avant
71: `s065`. Le contrôle négatif (mutation d'un token dans une copie de la doc) est détecté 4/5.
72: [`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. L
… [1699 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).\n\n**J11.3 — les 50 textes libres.** Les **50 phrases de l'audit A26** sont rejouées avec le\ncode du 14/ … [952 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 80, "offset": 55}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
55: ### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif ; heartbeat à rafraîchir)*
56: 
57: - **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
58: - **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
59: - **Plan** : B13, bloc linguistique.
60: - **Stratégie** : v0 mesuré.
61: - **Ambition** : un runtime cognitif tracé.
62: - **Objectif final** : un moteur de pensée v0.
63: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.2** (produit : [exemples](../../reports/rapport-exemples-r
… [7746 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo md_root $(ls reports/*.md | wc -l) md_all $(find reports -name '*.md' | wc -l) json_root $(ls reports/*.json | wc -l) json_all $(find reports -name '*.json' | wc -l)", "description": "Count report files"}`

  ```
md_root 727 md_all 897 json_root 821 json_all 821
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fichiers\\|JSON de résultats\\|reports.*md\\|glob\" tools/revue_documentation.py | head -40", "description": "Check revue counter logic"}`

  ```
67:    return [p for p in (RACINE / "docs").rglob("*.md")
72:    return list((RACINE / "docs").rglob("*.md"))
76:    return list((RACINE / "reports").glob("*.md"))
80:    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins)."""
93:    """Les fichiers dont les liens doivent résoudre (docs, fiches courantes, racine)."""
95:            + [RACINE / "reports/07-mesures-couche-commune.md",
96:               RACINE / "reports/fiche-nuit-17-10.md",
101:    return len(list((RACINE / "tools").glob("porte-*.sh")))
105:    return len(list((RACINE / "docs/theorie/synthese").glob("0*.md")))
113:    return len(list((RACINE / "reports").glob("*.json")))
161:    for f in (RACINE / "docs").rglob("*"):
169:    if not (RACINE / "reports/README.md").exists():
170:        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")
176:    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
187:        alertes.append("compteurs : la ligne « fichiers / JSON » manque dans en-cours.md")
190:            (int(fiches.group(1)), compte_fiches(), "fichiers"),
262:    cartes = sorted((RACINE / "docs/theorie/glossaire/entree
… [330 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](.. … [1252 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée* … [1126 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J11.1–J11.3** : 5/5 blocs rejoués, `r035` prédit ; `--par-langue` fr/en ; 50 textes libres **0 plantage**, **50/50 schéma v2**, **115/0** chevauchements, CLI **159,2 ms** ; F1 **0,7902**, at … [405 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **727** / **821** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **726** / **820** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (ca … [586 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — 11 verdicts + pointeur ; **R0.7** — split  … [399 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 20, "offset": 129}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
129: ## Les questions ouvertes
130: 
131: - **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
132: - **N2** : **< 2,5** ? → **oui par la fenêtre** : 2,4759 / 2,4373 au grand corpus (1 024, 30 k pas) ; la porte **propre** reste à 2,7856.
133: - **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.
134: - **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).
135: - **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche ; la
136:   **restitution v1** : le miroir strict **ne monte pas** (0,1087), la forme canonique vaut
137:   **46/46** ; le gold de forme canonique reste à faire.
138: 
139: ## La carte
140: 
141: - Méthode : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·
142:   [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · plan : [roadmap](roadmap.md) ·
143:   [backlog](backlog/index.md) · preuves : [reports/](../../reports/) · [journal
… [63 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche ; la\n  **restitution v1** : le miroir strict **ne monte pas** (0,1087), la forme canonique vaut\n  **46/46** ; le g … [464 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '150,215p' docs/pilotage/semaine-autonome.md", "description": "Read week plan task table"}`

  ```
Le superviseur a lancé **21 tâches** (budget **22 032 s** au 14/11 03 h 46, hors J10.1). **20
passent l'acceptation** ; **1 échoue** (J5.2, le tag). **5 timeouts** : J1.2, J2.2, J3.1, J5.2,
J8.1 — quatre sont récupérés par une acceptation verte ou par le commit de la tâche suivante ;
J5.2 reste un **échec rouge**. La règle du 13/11 (`ced21933`) tient : **l'acceptation d'abord, le
timeout n'est pas un verdict** (voir le bilan § 4).

| tâche | verdict | livrable | commit |
|---|---|---|---|
| J0 (contrôle) | ✅ fait | la liaison superviseur ↔ dsh | — |
| J1.1 `r035` | ✅ fait | exact **237/238**, couverture **0,9958** | `25a6c0ff` |
| J1.2 convention GV | ✅ livré (timeout) | F1 **0,7549 → 0,7902** | `92652984` |
| J1.3 schéma v2 | ✅ fait | `meta.partition`/`meta.alternative`, 26 cas | `9a259953` |
| J1.4 restitution v0 | ✅ fait | 46/46 surfaces exactes | `8eb0cc49` |
| J2.1 atomes ↔ niveaux | ✅ fait | 14/14 lignes | `9c7f71dc` |
| J2.2 + J3.1 corpus/retrieval | ✅ livré (timeout) | 418/438 paires exactes | `c3467170` (par J3.2) |
| J3.2 généalogie | ✅ fait | 154/154 paires hors script | `c2e629b3` |
| J4 N2/S/R/A | ✅ fait (13/11) | 4 fiches + 4 JSON ; D1–D8 | `commit J5.1` |
| J5.1 rapp
… [5685 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -60", "description": "Run documentation review", "timeoutMs": 180000}`

  ```
revue de documentation · 727 fiche(s) · 821 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py; echo \"rc=$?\"", "description": "Verify en-cours"}`

  ```
en-cours · 1713 mots · 7 sections · 4 session(s) · 9 puces · 6 questions
  ❌ 2 anomalie(s) :
     · 6 questions ouvertes > 5
     · question sans ce qui la débloque (`→`) : **Produit** : le défaut `alternative` (**115** chevauchement
rc=1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py; echo \"rc=$?\"", "description": "Verify journal"}`

  ```
journal · 46 jour(s) · 187 session(s) · 2475 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -20; echo \"rc=$?\"", "description": "Check document budget"}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2746    203   T1   2800  reports/README.md
    2450    166   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4083 mots (budget 4 000)

  avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [116 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schemas.py 2>&1 | tail -20; echo \"rc=$?\"", "description": "Verify schemas"}`

  ```
schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,180p' tools/taille_documents.py", "description": "Understand T0 budget"}`

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

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche ; la\n  **restitution v1** : le miroir strict **ne monte pas** (0,1087), la forme canonique vaut\n  **46/46** ; le g … [464 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|T0 :\" ; python3 tools/verifie_en_cours.py 2>&1 | tail -5", "description": "Recheck budgets and en-cours"}`

  ```
T0 max : 4057 mots (budget 4 000)
  ❌ 1 violation(s) :
     · T0 : 4057 mots (AGENTS + en-cours + une tâche) > budget 4 000
  en-cours · 1687 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 5, "offset": 62}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
62: - **Objectif final** : un moteur de pensée v0.
63: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.2** (produit : [exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md)) ; **J11.3** (50 textes libres : 0 plantage, 50/50 schéma v2, 115/0 chevauchements ; [fiche](../../reports/rapport-robustesse-semaine.md)) ; **contrat v1**, **`drave` v0**.
64: - **Ce qu'elle fait** : l'API rejoue le gold (mêmes verdicts).
65: - **Ce que font les autres** : **N2**, **S**, **hub**.
66: - **Prochaine action** : **trancher la convention d'adverbe (`g017`)** ; puis T132/T133, gold 200+.

(Showing lines 6
… [51 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](.. … [1252 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 3, "offset": 89}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
89: - **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée** (test −0,0028 ; g017 à trancher) ; **schéma v2** (v1 lue) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.3** (50 textes libres : 0 plantage, 50/50 schéma v2, **115** chevauchements `alternative` / **0** `filtrer`, CLI **159,2 ms** ; [fiche](../../reports/rapport-robustesse-semaine.md)) ; **J9.1** passe d'honnêteté (**19** fiches ; [fiche](../../reports/rapport-passe-honnetete.md)) ; [restitution v0](../../reports/rapport-restitution-v0.md), [g017](../../reports/rapport-g017.md).
90: - **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
91: - **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significative ; **J3.2** : `lang_distance` couvre **5/21** langues (Glottolo
… [393 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée* … [1239 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 2, "offset": 94}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
94: - **J11.1–J11.3** : 5/5 blocs rejoués, `r035` prédit ; `--par-langue` fr/en ; 50 textes libres **0 plantage**, **50/50 schéma v2**, **115/0** chevauchements, CLI **159,2 ms** ; F1 **0,7902**, att. **238/239** ; [J11.1](../../reports/rapport-exemples-rejoues.md), [J11.2](../../reports/rapport-evaluer-langue.md), [J11.3](../../reports/rapport-robustesse-semaine.md).
95: - **Coordination J4** : N2 **2,9726/2,7856** ; S **7/4** ; R **0,9475 (+8,49)** ; A6.2 **libre** ; [N2](../../reports/rapport-coordination-n2.md), [S](../../reports/rapport-coordination-s.md), [R](../../reports/rapport-coordination-r.md), [A](../../reports/rapport-coordination-a.md).

(Showing lines 94-95 of 143. Use offset=96 to continue.)
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|T0 :\"", "description": "Check T0 after trims"}`

  ```
T0 max : 4030 mots (budget 4 000)
     · T0 : 4030 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée* … [1049 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J11.1–J11.3** : 5/5 blocs rejoués, `r035` prédit ; `--par-langue` fr/en ; **J11.3** 50 textes libres, **115/0** chevauchements ; F1 **0,7902**, att. **238/239** ; [J11.1](../../reports/rappo … [514 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 2, "offset": 117}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
117: | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1–J11.3 (produit : 50 textes libres, 50/50 schéma v2, 115/0 chevauchements)** | **J11.4** (schéma v2 documenté) ; **trancher `g017`** ; puis T132/T133, gold 200+ ; **B10.3 bloquée** |
118: | **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 (manque **0,2856** val / **0,3566** test) ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |

(Showing lines 117-118 of 143. Use offset=119 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (ca … [592 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|T0 :\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3", "description": "Recheck T0 and en-cours"}`

  ```
T0 max : 4004 mots (budget 4 000)
     · T0 : 4004 mots (AGENTS + en-cours + une tâche) > budget 4 000
  en-cours · 1634 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J11.1–J11.3** : `--par-langue` fr/en ; **J11.3** 50 textes libres, **115/0** chevauchements ; F1 **0,7902**, att. **238/239** ; [J11.1](../../reports/rapport-exemples-rejoues.md), [J11.2](.. … [435 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|T0 :|violation\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3", "description": "Final budget check"}`

  ```
T0 max : 3998 mots (budget 4 000)
  en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md", "limit": 30, "offset": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md</path>
<type>file</type>
<content>
80: [`reports/rapport-retrieval-familles.md`](../../reports/rapport-retrieval-familles.md), JSON
81: [`reports/retrieval-familles.json`](../../reports/retrieval-familles.json), outil
82: [`tools/retrieval_familles.py`](../../tools/retrieval_familles.py).
83: **J8.1 — la restitution v1 : le miroir strict ne monte pas, la forme canonique vaut 1,0000.**
84: La v0 restitue la surface **46/46** mais le miroir strict tombe à **5/46 = 0,1087** parce que
85: `rendre_mots`/`rendre_pos` séparent la ponctuation (`dort .`). La v1 construit une **forme
86: canonique** depuis les **segments + rôles + cibles** : **46/46 formes exactes** contre une
87: source canonisée (casse repliée, ponctuation retirée), mais **1/46 = 0,0217** contre la source
88: brute — et le **miroir strict reste 0,1087**. C'est la réponse : le strict ne doit pas monter,
89: il mesure la surface ; la forme canonique mesure autre chose. La structure tient : **395
90: segments**, **395 rôles**, **315 cibles**, **315/315 résolues**, **313/315** portées par un
91: autre segment ; couverture **65,84 % des jetons**,
… [650 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md", "new_string": "[`reports/pensee-restitution-v1.json`](../../reports/pensee-restitution-v1.json), outil\n[`tools/mesurer_restitution_v1.py`](../../tools/mesurer_restitution_v1.py).\n**J11.3 — les 50 textes l … [1352 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-produit.sh tools/porte-*.sh | grep -i \"produit\\|schema\\|restitution\\|libre\\|docs\\|journal\\|en-cours\"", "description": "Find relevant gate scripts"}`

  ```
tools/porte-produit.sh
tools/porte-produit.sh
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh 2>&1 | tail -30; echo \"rc=${PIPESTATUS[0]}\"", "description": "Run product gate", "timeoutMs": 180000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 18 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m unittest tools.tests.test_produit_libre tools.tests.test_schema_produit tools.tests.test_restitution 2>&1 | tail -20", "description": "Run relevant unit tests", "timeoutMs": 180000}`

  ```
..................................
----------------------------------------------------------------------
Ran 34 tests in 15.015s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schema_produit.py --gold 20 2>&1 | tail -8; echo \"rc=${PIPESTATUS[0]}\"", "description": "Run schema verifier", "timeoutMs": 120000}`

  ```
✅ gold:g016 (v2)
  ✅ gold:g017 (v2)
  ✅ gold:g018 (v2)
  ✅ gold:g019 (v2)
  ✅ gold:g020 (v2)
  ✅ rétro-compatibilité : annotation v1 lue par le schéma v1
  ✅ contrôle négatif : le schéma v2 refuse une annotation v1
  ✅ validateur JSON Schema · 26 cas
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -10; echo \"rc=${PIPESTATUS[0]}\"", "description": "Rerun documentation review", "timeoutMs": 180000}`

  ```
revue de documentation · 727 fiche(s) · 821 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py 2>&1 | tail -4; echo \"rc=${PIPESTATUS[0]}\"", "description": "Rerun journal check"}`

  ```
journal · 46 jour(s) · 187 session(s) · 2478 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -8; echo \"rc=${PIPESTATUS[0]}\"", "description": "Rerun budget check"}`

  ```
1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3998 mots (budget 4 000)

  avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -8; echo \"rc=${PIPESTATUS[0]}\"", "description": "Run tables gate", "timeoutMs": 120000}`

  ```
✅ 1792 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4140 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short; echo ---; git diff --stat -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/INDEX.md journal/2026-11-14/README.md", "description": "Inspect working tree changes"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-14/README.md
 M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? reports/pensee-robustesse-semaine.json
?? reports/rapport-robustesse-semaine.md
?? reports/rapport-s-paragraphes.md
?? tools/mesurer_robustesse_semaine.py
---
 docs/pilotage/en-cours.md    |  8 ++++----
 docs/pilotage/roadmap.md     | 11 +++++++++++
 journal/2026-11-14/README.md | 13 +++++++++++++
 reports/INDEX.md             |  9 ++++++++-
 4 files changed, 36 insertions(+), 5 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '160,210p' tools/revue_documentation.py; grep -n \"INDEX\\|orphelin\\|index\" tools/revue_documentation.py | head -30", "description": "Check index coverage rules"}`

  ```
# 1. classement : aucune donnée de résultat dans docs/
    for f in (RACINE / "docs").rglob("*"):
        if f.suffix in (".json", ".csv", ".npz", ".jsonl") and f.is_file():
            if f.name == "index.json" and f.parent.name == "glossaire":
                continue
            alertes.append(f"classement : donnée de résultat dans docs/ → {f.relative_to(RACINE)}")
    for nom in ("07-mesures-couche-commune.md", "fiche-nuit-17-10.md"):
        if not (RACINE / "reports" / nom).exists():
            alertes.append(f"classement : la fiche courante reports/{nom} manque")
    if not (RACINE / "reports/README.md").exists():
        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")

    # 5. compteurs : la page d'état est la source unique, et elle dit le disque
    portes = extrait_entier(t, r"\|\s*portes\s*\|\s*\*\*(\d+)\*\*")
    chapitres = extrait_entier(t, r"\|\s*chapitres de la synthèse\s*\|\s*\*\*(\d+)\*\*")
    documents = extrait_entier(t, r"\|\s*documents de[^|]*\|\s*\*\*(\d+)\*\*")
    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
    for nom, valeur, disque in (
        ("portes", portes, comp
… [2645 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline 84e393bb | head -20; echo ---; git show --stat --oneline 229098ec | head -20; echo ---; git show --stat --oneline 03ecee41 | head -20", "description": "Check prior commit file sets"}`

  ```
84e393bb J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238
 docs/pilotage/en-cours.md                          |   15 +-
 docs/pilotage/roadmap.md                           |    9 +
 docs/produit/exemples.md                           |  151 +-
 journal/2026-11-14/README.md                       |    7 +-
 journal/2026-11-14/docs.md                         |    2 +-
 journal/2026-11-14/memoire.md                      |    5 +-
 journal/2026-11-14/mesures.md                      |    2 +-
 journal/2026-11-14/portes.md                       |    2 +-
 journal/README.md                                  |    4 +-
 journal/sessions/MANIFEST.md                       |    6 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   26 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 2096 ++++++++++++++++++++
 .../rapport.md                                     |   54 +-
 reports/rapport-exemples-rejoues.json              |  500 +++++
 reports/rapport-exemples-rejoues.md                |  171 ++
 16 files changed, 2970 insertions(+), 94 deletions(-)
---
229098ec 
… [2641 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-14/README.md | sed -n '1,220p'", "description": "Review state and journal diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index bf9a9e5f..1159fac1 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -91,7 +91,7 @@
 - **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significative ; **J3.2** : `lang_distance` couvre **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, la famille vit dans **2-3 paires**, **V14 : 3/21** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-faces.md).
 - **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002), échantillon 20 nul ; J3.1 reproduit ; [fiche](../../reports/rapport-retrieval-familles.md).
 - **J5.1 / J10.1 — les bilans** : semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets** ; [rapport](../../reports/rapport-semaine.md)) ; chantier (**20/21**, attachement **2
… [7351 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/pensee-robustesse-semaine.json > /dev/null && echo \"json ok\"; git diff --check -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-14/README.md || true", "description": "Validate JSON  … [16 caractères tronqués]`

  ```
json ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-14/README.md reports/pensee-robustesse-semaine.json reports/rapport-robustesse-semaine.md tools/mesurer_robustesse_semaine.py && git status --short | head -20 … [78 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-14/README.md
 M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
A  reports/pensee-robustesse-semaine.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
A  reports/rapport-robustesse-semaine.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
A  tools/mesurer_robustesse_semaine.py
 m tools/structures
?? reports/rapport-s-paragraphes.md
---
 docs/pilotage/en-cours.md              |    8 +-
 docs/pilotage/roadmap.md               |   11 +
 journal/2026-11-14/README.md           |   13 +
 reports/pensee-robustesse-semaine.json | 3040 ++++++++++++++++++++++++++++++++
 reports/rapport-robustesse-semaine.md  |  238 +++
 tools/mesurer_robustesse_semaine.py    |  565 ++++++
 6 files changed, 3871 insertions(+), 4 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 SCHÉMA V2, 115 CHEVAUCHEMENTS ALTERNATIVE / 0 FILTRER ; RESTITUTION 46/46, STRICT 0,1087 (F1 0,7902)\"", "description": "Commit J11.3 result"}`

  ```
[stderr]
  ✅ index : aucun fait stagé sans état
[still running after 60000ms; moved to background job bash-92]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-92", "wait": true, "timeout_ms": 120000}`

  ```
[s/v7 55bde5c5] J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 SCHÉMA V2, 115 CHEVAUCHEMENTS ALTERNATIVE / 0 FILTRER ; RESTITUTION 46/46, STRICT 0,1087 (F1 0,7902)
 19 files changed, 6724 insertions(+), 33 deletions(-)
 create mode 100644 journal/sessions/session-6b997dd9-9a2e-4d72-b31a-5a6d40609d56/digest.md
 create mode 100644 journal/sessions/session-6b997dd9-9a2e-4d72-b31a-5a6d40609d56/rapport.md
 create mode 100644 reports/pensee-robustesse-semaine.json
 create mode 100644 reports/rapport-robustesse-semaine.md
 create mode 100644 tools/mesurer_robustesse_semaine.py
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline HEAD | head -40; echo ---; git status --short | head -30", "description": "Inspect commit contents"}`

  ```
55bde5c5 J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 SCHÉMA V2, 115 CHEVAUCHEMENTS ALTERNATIVE / 0 FILTRER ; RESTITUTION 46/46, STRICT 0,1087 (F1 0,7902)
 docs/pilotage/en-cours.md                          |    8 +-
 docs/pilotage/roadmap.md                           |   11 +
 journal/2026-11-14/README.md                       |   20 +-
 journal/2026-11-14/docs.md                         |    2 +-
 journal/2026-11-14/memoire.md                      |    2 +-
 journal/2026-11-14/mesures.md                      |    8 +-
 journal/2026-11-14/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/THEMES.md                                  |    2 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |    9 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 2490 ++++++++++++++++
 .../rapport.md                                     |  181 ++
 .../digest.md                                      |  106 +
 .../rapport.md                                     |   47 +-
 reports/pensee-robustesse-semaine.jso
… [622 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -6; echo \"rc=${PIPESTATUS[0]}\"", "description": "Post-commit doc review", "timeoutMs": 180000}`

  ```
revue de documentation · 727 fiche(s) · 821 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py 2>&1 | tail -3; echo \"rc=${PIPESTATUS[0]}\"", "description": "Post-commit journal check"}`

  ```
journal · 46 jour(s) · 188 session(s) · 2482 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|✅\"; echo \"rc=${PIPESTATUS[0]}\"", "description": "Post-commit budget check"}`

  ```
T0 max : 3998 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo \"rc=${PIPESTATUS[0]}\"", "description": "Post-commit en-cours check"}`

  ```
en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format='%h %s' && echo --- && git show HEAD:journal/2026-11-14/README.md | grep -n \"J11.3\" | head; echo ---; git status --short | head -20", "description": "Verify commit and journal"}`

  ```
55bde5c5 J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 SCHÉMA V2, 115 CHEVAUCHEMENTS ALTERNATIVE / 0 FILTRER ; RESTITUTION 46/46, STRICT 0,1087 (F1 0,7902)
---
99:**J11.3 — les 50 textes libres : le contrat tient, la vue linéaire ne chevauche pas.** Les
---
 M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-robustesse-semaine.json'))\nprint(list(d))\nprint(json.dumps(d['resultats'][0],ensure_ascii=False,indent=1)[:1200])\nprint('refus f14:',json.dumps(d['resultats'][13],en … [178 caractères tronqués]`

  ```
['schema', 'version', 'date', 'ligne', 'tache', 'titre', 'banc', 'banc_sha256', 'commande', 'code', 'dispositif', 'synthese', 'comparaison_a26', 'resultats', 'limites']
{
 "id": "f01",
 "categorie": "fr",
 "attendu": "fr",
 "caracteres": 13,
 "rc": 0,
 "rc_2": 0,
 "plantage": false,
 "traceback": false,
 "stderr_succes": false,
 "deterministe": true,
 "json_valide": true,
 "erreur_json": "",
 "champs_8": true,
 "schema_v2": true,
 "schema_erreur": "",
 "version": 2,
 "refus": "",
 "langue": "fr",
 "script": "Latn",
 "temps_cli_ms": 158.8,
 "temps_cli_2_ms": 161.8,
 "temps_api_ms": 1.9,
 "temps_api_filtrer_ms": 1.5,
 "api_alternative_schema_v2": true,
 "api_filtrer_schema_v2": true,
 "api_alternative_champs_8": true,
 "api_filtrer_champs_8": true,
 "alternative": {
  "segments": 2,
  "chevauchements": 0,
  "sans_syntagme": false
 },
 "filtrer": {
  "segments": 2,
  "chevauchements": 0,
  "sans_syntagme": false
 },
 "filtrer_union": {
  "segments": 2,
  "chevauchements": 0,
  "sans_syntagme": false
 },
 "invariants": {
  "etiquettes": 20,
  "spans_hors_texte": 0,
  "spans_vides": 0,
  "cibles_absentes": 0
 },
 "erreurs_api": {
  "alternative": "",
  "filtrer": ""
 }
}
refus f14: {
 "
… [2010 caractères tronqués]
  ```

### 🤖 Assistant

**J11.3 fait.** Fiche `reports/rapport-robustesse-semaine.md`, JSON `reports/pensee-robustesse-semaine.json`, outil reproductible `tools/mesurer_robustesse_semaine.py`. Commit **`55bde5c5`** ; mesure sur le code **`09e54143`** (F1 **0,7902**, POS **0,8625**, attachement **238/238 labels — 238/239 cibles, 0,9958**, schéma v2, restitution v1).

| mesure | audit A26 (06/11) | **J11.3 (14/11)** |
|---|---:|---:|
| plantages | 0/50 | **0/50** |
| JSON valide | 0/46 invalide + 4 refus vides | **50/50** |
| refus | 4/50, code 1, stdout 0 o | **4/50, code 3, JSON** |
| 8 champs obligatoires | 0/46 | **50/50** |
| schéma v2 | absent | **50/50** (CLI + API, deux vues) |
| chevauchements `alternative` | 107 paires / 23/46 | **115 paires / 21/46** |
| chevauchements `filtrer` | 0 après filtre `meta.union` | **0/50**, vue publiée |
| sans syntagme (annotés) | 4/46 | **3/46** (`f18`, `f27`, `f37` ; `f13` segmenté) |
| temps CLI médian | 152,7 ms | **159,2 ms** |
| temps API médian | 1,0 ms | **2,7 ms** |

**Les deux vues.** `alternative` : **395 segments, 115 chevauchements** ; `filtrer` : **313 segments, 0 chevauchement**. `filtrer_union` (contrôle) : 352 segments, 40 chevauchements. Le zéro de `filtrer` n'est pas un artefact : 313 segments, et le compteur détecte bien un chevauchement injecté (1/1).

**Le contrat.** 50/50 CLI portent les 8 champs et passent JSON Schema v2 ; 50/50 en API `alternative` et 50/50 en API `filtrer`. Les 4 refus sont des réponses JSON valides. Déterminisme **50/50** ; **0 span hors texte**, **0 span vide**, **0 cible absente** sur 4 827 étiquettes et 315 cibles.

**La restitution.** Identique à la v1 : **46/46 canonique**, **strict 5/46 = 0,1087**, **395 segments / 395 rôles / 315 cibles / 313 dans un autre segment**, stabilité **18/46**. Contrôles : mélange/troncature **46/46 détectés, 0/46 exacts** ; rôles/cibles retirés **43/43**.

**La comparaison A26.** L'écart 107 → 115 est un effet du **code**, pas du compteur : mêmes paires strictes, mais `f50` passe de 50 à 63, `f26` et `f29` tombent à 0, `f06` de 4 à 2. Le nombre de textes touchés baisse de 23 à 21 malgré la hausse du total. Les 8 champs passent de 0/46 à 50/50 et les refus de « code 1 sans JSON » à « code 3 avec JSON ».

**Vérifications.** `porte-produit` verte (183/183), 34 tests produit/schéma/restitution OK, `verifier_schema_produit --gold 20` OK, revue de documentation OK (727 fiches / 821 JSON), journal OK, budget T0 **3 998/4 000** mots, tableaux et schémas OK.

**Limites nommées dans la fiche** : banc écrit à la main, définition stricte du chevauchement, comparaison à code non constant, 4 refus exclus de la structure, temps dominé par le démarrage CLI, restitution canonique vraie par construction.

