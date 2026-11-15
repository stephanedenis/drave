# Session DSH — relecture

- identifiant : `session-72a370ef-2ad7-4a59-8418-d88c38545f6e`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 02:46:22
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche B1 : le protocole Panini à date contrôlée (la suite de la note 4A) — construis `reports/rapport-protocole-date.md` + JSON : 60 paires en trois groupes (20 contemporaines de traditions différentes ±10 ans, 20 de même tradition à ±200 ans, 20 de même langue source à dates décalées), tirées des artefacts §334 en lecture seule ; le protocole (H0, les contrôles, les 14 atomes), le pré-enregistrement, et la commande que Panini peut rejouer. **Ne modifie rien chez Panini.**

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

- **bash** `{"command": "pwd && ls -la && echo \"---\" && ls reports/ | head -50", "description": "List repo root and reports"}`

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
drwxr-xr-x. 1 stephane stephane   198 15 nov 02:46 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 76786 15 nov 02:45 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [2025 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -15 && echo \"---\" && git status --short | head -30", "description": "Show recent commits and status"}`

  ```
f926b5bc C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PROFONDEUR, 41 VERDICTS À RE-JUGER ; PORT 8765 PRIS, PARE-FEU ACTIF ; LES 11 VERDICTS COMMITTÉS (389b99f)
292c70b5 C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09
5891ef8a ÉTAT — T0 TENU : LA LIGNE FAIT RACCOURCIE
6560a0a5 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612)
2d7a7f2b 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5)
ce7241d5 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS
34c0fb0b INDEX — RÉGÉNÉRÉ APRÈS LE TAGGER (LA FICHE 20/612, LE COÛT, LES TESTS) ; ÉTAT HORODATÉ
5b03a0dd DOC PRODUIT — LE TAGGER EN OPTION DOCUMENTÉ (CACHE CHAUD, COÛT, LIEN DE LA FICHE) ; § 3.7 COMPLET
d6e66080 ÉTAT — LA LIGNE R REQUALIFIÉE : LE TAGGER EST LIVRÉ (--tagger, 0bbdbbb3), LA PROCHAINE ACTION PASSE AU SPLIT RÉEL ET AU GOLD 200+
29b3dd13 ÉTAT — T0 TENU APRÈS L'INSCRIPTION DE
… [1150 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i -E \"panini|nipada|4a|date|protocole\" ; echo \"---\"; grep -rl \"4A\" docs/ reports/ journal/ --include=*.md | head -30", "description": "Find Panini/4A related files"}`

  ```
n3.4a-composition.json
note-panini-334.md
panini-334.json
pensee-inventaire-panini.json
rapport-inventaire-panini.md
rapport-n3.4a-composition.md
rapport-panini-334.md
---
docs/pilotage/semaine-autonome.md
reports/note-panini-334.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
journal/sessions/f2de810a-b765-444d-b3cc-d8fce1ba2105/digest.md
journal/sessions/0b69f616-5c75-4c34-b97a-ae05564812af/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/digest.md
journal/sessions/599e9c0e-4252-43ca-a89a-3886d723c379/digest.md
journal/sessions/session-1a1b15e7-d5f5-4f11-aeb3-0e6e42628dbe/digest.md
journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/digest.md
journal/sessions/session-e0896820-1b14-4849-a926-cc56f678b88d/digest.md
journal/2026-11-14/docs.md
journal/2026-11-14/README.md
journal/2026-11-14/mesures.md
  ```

- **bash** `{"command": "ls docs/methode/ && echo \"---\" && sed -n '1,80p' docs/methode/panini-nipada.md", "description": "Read Panini-Nipada method doc"}`

  ```
chantier-autonome.md
contexte.md
continuite.md
echantillonnage-vdc.md
illustrations.md
miroir.md
mission.md
modularisation.md
organisation-du-depot.md
panini-nipada.md
portes.md
rangement.md
relations-humaines.md
ressources.md
resultats.md
---
# Étudier Panini et Nipada, régulièrement

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **à chaque cycle**, avant de conclure sur
> la généalogie, les styles ou les familles de langues.

## Pourquoi

Les projets **`../Panini/`** et **`../Panini-Research/`** poursuivent le **même objectif par une approche
complémentaire** : Panini décompose le texte en **14 atomes sémantiques**, Nipada le fait tourner comme un tissu
computationnel — *algébrique, là où Drave est statistique*. Ils tiennent le **système linguistique** et généralisent
une **généalogie des langues, dialectes et styles**.

## La règle

À chaque cycle, **lire ce qui a bougé chez eux** (docs, publications, journaux de bord, `git log`) et **confronter
leurs résultats aux nôtres**. Ce qui en sort va dans [`docs/theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md)
(la théorie) — **jamais les chiffres** (ils vont dans `reports/`).

## Leur
… [867 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/note-panini-334.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/note-panini-334.md</path>
<type>file</type>
<content>
1: # Note pour Panini/NIPADA — le §334 : votre loi reproduite, votre β époque non, et pourquoi
2: 
3: > **Ce que cette note est.** Le **message prêt à envoyer** à l'équipe Panini/NIPADA (décision 4A
4: > du 14/11), avec la fiche technique en dessous. Elle porte sur **leur** résultat du §334
5: > (l'époque β +0,138 vs la filiation +0,049) et sur notre rejeu indépendant.
6: > **Ce qu'elle n'est pas** : une réfutation. C'est une **mesure de plus**, avec ses limites.
7: 
8: ## 1. Le message (à envoyer tel quel)
9: 
10: > Bonjour,
11: >
12: > Nous avons rejoué votre §334 (655 paires, 374 avec date, les 44 signatures V14) avec nos outils
13: > et un contrôle supplémentaire : la **topologie** du graphe (la distance dans l'arbre), pour
14: > séparer ce que l'époque explique de ce que la filiation explique.
15: >
16: > **Ce qui se reproduit** : votre loi H0 tient (**R² = 0,909139** sur les 655 lignes ;
17: > **0,906307** sur les 488 paires uniques non auto). Le retrieval brut donne **61,4 %** de même
18: > tradition (hasard 22,4 %).
19: >
20: > **Ce qui ne se reproduit pas** :
… [3562 caractères tronqués]
  ```

- **bash** `{"command": "wc -l reports/panini-334.json reports/rapport-panini-334.md reports/rapport-inventaire-panini.md reports/pensee-inventaire-panini.json 2>/dev/null; echo \"---\"; head -c 3000 reports/note-panini-334.md", "description": "Inspect 334 artifacts sizes"}`

  ```
9723 reports/panini-334.json
   384 reports/rapport-panini-334.md
   548 reports/rapport-inventaire-panini.md
   852 reports/pensee-inventaire-panini.json
 11507 total
---
# Note pour Panini/NIPADA — le §334 : votre loi reproduite, votre β époque non, et pourquoi

> **Ce que cette note est.** Le **message prêt à envoyer** à l'équipe Panini/NIPADA (décision 4A
> du 14/11), avec la fiche technique en dessous. Elle porte sur **leur** résultat du §334
> (l'époque β +0,138 vs la filiation +0,049) et sur notre rejeu indépendant.
> **Ce qu'elle n'est pas** : une réfutation. C'est une **mesure de plus**, avec ses limites.

## 1. Le message (à envoyer tel quel)

> Bonjour,
>
> Nous avons rejoué votre §334 (655 paires, 374 avec date, les 44 signatures V14) avec nos outils
> et un contrôle supplémentaire : la **topologie** du graphe (la distance dans l'arbre), pour
> séparer ce que l'époque explique de ce que la filiation explique.
>
> **Ce qui se reproduit** : votre loi H0 tient (**R² = 0,909139** sur les 655 lignes ;
> **0,906307** sur les 488 paires uniques non auto). Le retrieval brut donne **61,4 %** de même
> tradition (hasard 22,4 %).
>
> **Ce qui ne se reproduit pas** : le coefficient
… [1859 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/panini-334.json'))\nprint(type(d))\nif isinstance(d,dict):\n    for k,v in d.items():\n        print(k, type(v), (len(v) if hasattr(v,'__len__') else ''))\n        if isinstance(v,list) and v:\n            print('  first:', json. … [175 caractères tronqués]`

  ```
<class 'dict'>
tache <class 'str'> 5
titre <class 'str'> 105
date <class 'str'> 10
graine <class 'int'> 
sources <class 'dict'> 9
  keys: ['paires', 'graphe', 'signatures', 'revalidation', 'couverture', 'manifeste', 'v150', 'commit_panini', 'commit_drave']
audit <class 'dict'> 17
  keys: ['corpus_actif_officiel', 'corpus_actif_tradition', 'corpus_actif_references', 'paires', 'sections', 'textes_distincts_paires', 'textes_absents_des_paires', 'oeuvres_signees', 'textes_paires_sans_signature', 'sources_manifeste', 'sources_ok', 'sources_ok_parmi_48', 'sources_ok_parmi_44', 'urls_non_vides', 'urls_uniques_non_vides', 'langues_source_44', 'textes']
paires <class 'dict'> 17
  keys: ['n_paires', 'n_paires_officielles', 'n_paires_uniques', 'n_auto_paires', 'n_doublons_lignes', 'n_textes', 'contraste_date_surface', 'modeles', 'positivite', 'bins_date', 'delta_pondere_bins', 'permutations', 'bootstrap', 'surface_meme_langue', 'doublons_exacts', 'correlations', 'paires']
oeuvres <class 'dict'> 12
  keys: ['n', 'v150', 'retrieval', 'retrieval_nulls', 'bins_retrieval', 'modele_cos', 'prediction', 'surface_eng', 'sans_doublons', 'bootstrap', 'signatures_permutees', 'oeuvres']
synthese <class 'd
… [257 caractères tronqués]
  ```

- **bash** `{"command": "ls -d ../Panini* 2>/dev/null; echo \"---\"; ls ../Panini 2>/dev/null | head -40; echo \"---gitmodules---\"; cat .gitmodules", "description": "Locate Panini repo"}`

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
config
CONTEXTE-IA.md
copilotage
corpus
data
Dockerfile.template
docs
experiments
experiments.json
legacy
modules
notebooks
outputs
Panini-AttributionRegistry
Panini.code-workspace
PHILOSOPHIE.md
pyproject.toml
README.md
research
scripts
signwriting-bloc-complet.png
signwriting-mains.png
signwriting-unicode-inventory.txt
src
tech
tests
tools
utils
---gitmodules---
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
  ```

- **bash** `{"command": "cd ../Panini && grep -rli \"§334\\|section 334\\|#334\\|334\" --include=*.md --include=*.json --include=*.py --include=*.txt . 2>/dev/null | head -40", "description": "Search Panini repo for 334 artifacts"}`

  ```
./data/gutenberg_corpus/1342/1342.txt
./data/gutenberg_corpus_large/1342/1342.txt
./data/gutenberg_direct_corpus/1342/1342.txt
./data/gutenberg_massive_corpus/1342/1342.txt
./data/gutenberg_multilingual_corpus/pride_prejudice/pride_prejudice_en.txt
./data/gutenberg_multilingual_verified/pride_prejudice/pride_prejudice_en.txt
./data/incremental_corpus/intelligent_batch_003_20250922_231124.json
./data/incremental_corpus/turbo_batch_20250922_232622.json
./data/incremental_corpus/turbo_batch_20250922_235017.json
./data/incremental_corpus/turbo_batch_20250922_235539.json
./data/incremental_corpus/turbo_batch_20250922_235632.json
./data/incremental_corpus/turbo_batch_20250922_235648.json
./data/incremental_corpus/turbo_batch_20250922_235900.json
./data/incremental_corpus/turbo_batch_20250922_235905.json
./data/incremental_corpus/turbo_batch_20250922_235937.json
./data/incremental_corpus/turbo_batch_20250922_235958.json
./data/incremental_corpus/turbo_batch_20250923_000133.json
./data/incremental_corpus/turbo_batch_20250923_000226.json
./data/incremental_corpus/turbo_batch_20250923_000407.json
./data/monitoring_data_realtime.json
./data/panini_high_performance_report_20250920_154356.json

… [1291 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/panini-334.json'))\nprint(json.dumps(d['sources'], ensure_ascii=False, indent=1)[:3000])\nprint('---PAIRES keys---')\np=d['paires']['paires']\nprint(type(p), len(p))\nprint(json.dumps(p[0], ensure_ascii=False, indent=1)[:1500])\n … [56 caractères tronqués]`

  ```
{
 "paires": {
  "chemin": "Panini/research/nipada/falsification/pairs334_axes_v1.json",
  "sha256": "8de7a6797d5316293bd29c3e5ac070d2ef5582acdeb96b286397237540528777"
 },
 "graphe": {
  "chemin": "Panini/research/nipada/falsification/nipada_v334_graph_v35.json",
  "sha256": "9ddf050aa1699a3c345c6b9e8ad973b8096d6003219b069dd6a6f51489793cfe"
 },
 "signatures": {
  "chemin": "Panini/research/nipada/falsification/analytic_sigs_v1.json",
  "sha256": "8aa9c1d50d89e4dc13a8b9bdbf0ae77d4e5a6da4bed00ecd126284f0f7a5519e"
 },
 "revalidation": {
  "chemin": "Panini/research/nipada/falsification/nipada_v334_revalidation_v35.json",
  "sha256": "b2be71436a017b7881fee7f93d26bedd948a7c342166236c8314d1f278abb546"
 },
 "couverture": {
  "chemin": "Panini/research/nipada/corpus/_cache/sources_coverage.json",
  "sha256": "5d06443de6aed73370ba209faacc25a48859b07741fdbe680f0db5914d23f5dd"
 },
 "manifeste": {
  "chemin": "Panini/research/nipada/corpus/_cache/sources_manifest.json",
  "sha256": "5eda052cadf361a94d0089ea2644c468f9ba62cc70eb81dfa61a74846adb1a1e"
 },
 "v150": {
  "chemin": "Panini/research/nipada/falsification/nipada_v150_validation.json",
  "sha256": "353168c2fd3846c9238168628ecf9c2956ef519b
… [428 caractères tronqués]
  ```

- **job_kill** `{"job_id": "bash-8", "reason": "grep trop large, inutile"}`

  ```
requested cancellation of job bash-8
  ```

- **bash** `{"command": "cd ../Panini && ls -la research/nipada/falsification/ | head -60", "description": "List Panini falsification artifacts"}`

  ```
total 212144
drwxr-xr-x. 1 stephane stephane   21326 18 oct 10:03 .
drwxr-xr-x. 1 stephane stephane     650  4 jun 11:29 ..
-rw-r--r--. 1 stephane stephane   22381 18 oct 10:03 analytic_sigs_v1.json
-rw-r--r--. 1 stephane stephane    7048 18 oct 10:03 axeA_p1_subset_v1.json
-rw-r--r--. 1 stephane stephane    1644 18 oct 10:03 benchmark_generatif_analytique_v1.json
-rw-r--r--. 1 stephane stephane    4228 18 oct 10:03 benchmark_generatif_clean_v1.json
-rw-r--r--. 1 stephane stephane    9358  8 sep 15:34 benchmark_generatif_contenu_v1.json
-rw-r--r--. 1 stephane stephane    6059 18 oct 10:03 benchmark_generatif_corpus_v1.json
-rw-r--r--. 1 stephane stephane    2200 18 oct 10:03 benchmark_generatif_v1.json
-rw-r--r--. 1 stephane stephane   25410 30 avr  2026 circular_translation_test.json
-rw-r--r--. 1 stephane stephane    1738 18 oct 10:03 container_profiles_v1.json
-rw-r--r--. 1 stephane stephane    7948 28 jun 19:53 context_q1_embedding.json
-rw-r--r--. 1 stephane stephane    3849 28 jun 19:48 context_q1_normalized.json
-rw-r--r--. 1 stephane stephane   11481 28 jun 19:32 context_q1_translation_drift.json
-rw-r--r--. 1 stephane stephane     773 28 jun 19:32 context_q3_channel_stabil
… [3645 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\np=json.load(open('research/nipada/falsification/pairs334_axes_v1.json'))\nprint(type(p))\nif isinstance(p,dict):\n    print(list(p)[:20])\n    for k,v in p.items():\n        print(k, type(v), len(v) if hasattr(v,'__len__') els … [415 caractères tronqués]`

  ```
<class 'dict'>
['version', 'created', 'method', 'n_pairs', 'r2_L2', 'alpha', 'vopt', 'pairs']
version <class 'str'> 2
created <class 'str'> 10
method <class 'str'> 35
n_pairs <class 'int'> 
r2_L2 <class 'dict'> 4
alpha <class 'float'> 
vopt <class 'dict'> 4
pairs <class 'list'> 655
 first: {"section": "a", "a": "dn1_brahmajala", "b": "mn2_sabbasava", "d_topo": 3.6, "d_lex": 0.33870554623886845, "d_H": 0.6076717359284258, "cos": 0.7492899129132787, "trad_a": "BUDDHIST_AXIAL", "trad_b": "BUDDHIST_AXIAL", "lang_a": "eng", "lang_b": "eng", "same_comp": true}
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\nfor f in ['research/nipada/falsification/analytic_sigs_v1.json','research/nipada/falsification/nipada_v334_revalidation_v35.json','research/nipada/falsification/nipada_v334_graph_v35.json']:\n    print('==',f)\n    d=json.load(open(f))\n   … [431 caractères tronqués]`

  ```
== research/nipada/falsification/analytic_sigs_v1.json
<class 'dict'> ['2_esdras', 'aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'curry_1930', 'daniel_book', 'dn1_brahmajala', 'ezekiel_book', 'hosea_book', 'isaiah_book', 'jeremiah_book', 'kleene_1936', 'lukasiewicz_1920', 'mengzi', 'mikolov_2013']
  2_esdras <class 'dict'> 14
    {"ÊTRE": 0.07446500282604852, "DIFFÉRENCE": 0.013816044014481109, "RAPPORT": 0.10099345547363615, "ORIENTATION": 0.005331763602619648, "SUJET": 0.14124697298283334, "TEMPS": 0.05189835957545314, "MODALITÉ": 0.02705634807902917, "NOMBRE": 0.14932406971800052, "ESPACE": 0.04847053574653187, "OPÉRATION": 0.06701372487945408, "FONCTION": 0.12163933372805281, "STRUCTURE": 0.14742169250272855, "SYMÉTRIE
  aristotle_categories <class 'dict'> 14
    {"ÊTRE": 0.14598002759025833, "DIFFÉRENCE": 0.03854854561582201, "RAPPORT": 0.0765354958116522, "ORIENTATION": 0.005632418801409541, "SUJET": 0.17885306226299458, "TEMPS": 0.05455181280253287, "MODALITÉ": 0.0543486933929131, "NOMBRE": 0.0919066931460675, "ESPACE": 0
… [20605 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))\nnodes=g['nodes']\nsig=[(k,v) for k,v in nodes.items() if v.get('v14_signature')]\nprint('signed nodes', len(sig))\nfor k,v in sorted(sig, key=lambd … [253 caractères tronqués]`

  ```
signed nodes 57
-600 lzh DAOISM | tao_te_ching_legge_en | Laozi (Legge) | corpus_work
-400 None CHINESE_RATIONALIST | mozi_selections | mozi | proto_atheist_work
-400 lzh CONFUCIAN_AXIAL | great_learning_legge_en | Zengzi/Legge | corpus_work
-399 grc GRECO_PLATONIC | plato_euthyphro_jowett | Platon (Jowett) | corpus_work
-399 grc GRECO_PLATONIC | plato_crito_jowett | Platon (Jowett) | corpus_work
-385 grc GRECO_PLATONIC | plato_symposium_jowett | Platon (Jowett) | corpus_work
-385 grc GRECO_PLATONIC | plato_meno_jowett | Platon (Jowett) | corpus_work
-380 grc GRECO_PLATONIC | plato_republic_jowett | Platon (Jowett) | corpus_work
-380 grc GRECO_PLATONIC | plato_gorgias_jowett | Platon (Jowett) | corpus_work
-380 grc GRECO_PLATONIC | plato_republic_fr | Platon (Cousin) | corpus_work
-370 grc GRECO_PLATONIC | plato_phaedrus_jowett | Platon (Jowett) | corpus_work
-369 grc GRECO_PLATONIC | plato_theaetetus_jowett | Platon (Jowett) | corpus_work
-360 grc GRECO_PLATONIC | plato_philebus_jowett | Platon (Jowett) | corpus_work
-300 grc GRECO_LAT_MATERIAL | epicurus_letters | Épicure | proto_atheist_work
-300 san INDIAN_MATERIAL | carvaka_fragments | Cārvāka / Lokāyata (école) | proto_atheis
… [3418 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\np=json.load(open('research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nprint('n',len(p))\nprint('sections', collections.Counter(x['section'] for x in p))\nfor s in ['a','b','c']:\n    xs=[x for x in p if x['section … [507 caractères tronqués]`

  ```
n 655
sections Counter({'a': 459, 'b': 180, 'c': 16})
--- section a 459
keys ['section', 'a', 'b', 'd_topo', 'd_lex', 'd_H', 'cos', 'trad_a', 'trad_b', 'lang_a', 'lang_b', 'same_comp']
  trad_a [('', 199), ('BUDDHIST_AXIAL', 107), ('GRECO_PLATONIC', 56), ('INDIAN_AXIAL', 26), ('CHINESE_AXIAL', 25), ('CONFUCIAN_AXIAL', 24), ('ABRAHAMIC_PROPHETIC_AXIAL', 12), ('JUDEAN_APOCALYPTIC_LATE', 4), ('NORSE_EDDIC_MEDIEVAL', 3), ('RENAISSANCE_OCCULT_EARLY_MODERN', 2), ('MILLENARIAN_MODERN_PROTESTANT', 1)]
  trad_b [('', 269), ('GRECO_PLATONIC', 147), ('ABRAHAMIC_PROPHETIC_AXIAL', 11), ('BUDDHIST_AXIAL', 9), ('CONFUCIAN_AXIAL', 5), ('MILLENARIAN_MODERN_PROTESTANT', 5), ('CHINESE_AXIAL', 4), ('INDIAN_AXIAL', 3), ('CLASSICAL_ORACULAR', 3), ('JUDEAN_APOCALYPTIC_LATE', 2), ('RENAISSANCE_OCCULT_EARLY_MODERN', 1)]
  lang_a [('', 245), ('eng', 212), ('fra', 2)]
  lang_b [('', 279), ('eng', 179), ('fra', 1)]
  same_comp [('True', 459)]
--- section b 180
keys ['section', 'a', 'b', 'd_topo', 'd_lex', 'd_H', 'cos', 'trad_a', 'trad_b', 'lang_a', 'lang_b', 'same_comp']
  trad_a [('FUZZY_LOGIC', 30), ('MANY_VALUED_LOGIC', 30), ('RECURSIVE_FUNCTIONS', 30), ('COMBINATORY_LOGIC', 30), ('SEMANTIC_NETWORKS', 30),
… [801 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && ls research/nipada/ && echo \"---falsification count---\" && ls research/nipada/falsification | wc -l && echo \"---corpus cache---\" && ls research/nipada/corpus/_cache/ | head -40", "description": "List nipada dirs and corpus cache"}`

  ```
api
closure
corpus
encyclopedia
falsification
fpga
modal
molecules
NAC_ROADMAP_v1.0.md
NIPADA_SEMANTIC_PIPELINE.md
ONTOWAVE_DESIGN_v1.0.md
originals_cache
publication
PUBLICATION_PLAN_v1.0.md
RAPPORT_FALSIFICATION_NIPADA_v1.0.md
schema
scripts
semantic
src
SYNTHESE_v0.2.0.md
SYNTHESE_v0.3.0.md
SYNTHESE_v0.4.0-alpha.md
taxonomies
v7
validation_repo
---falsification count---
345
---corpus cache---
dhammapada_muller_en_pg2017.txt
feuerbach_essence_en_pg69432.txt
gutenberg_curated
hobbes_leviathan_en_pg3207.txt
holbach_system_nature_en_pg8909.txt
hume_dialogues_en_pg4583.txt
manifest_de_wikisource.txt
manifest_en_pg61.txt
missing48.json
mit_aristotle_categories_idx.txt
mit_aristotle_categories_s001.txt
mit_aristotle_categories_s002.txt
mit_aristotle_categories_s003.txt
mit_aristotle_de_anima_idx.txt
mit_aristotle_de_anima_s001.txt
mit_aristotle_de_anima_s002.txt
mit_aristotle_de_anima_s003.txt
mit_aristotle_de_caelo_idx.txt
mit_aristotle_de_caelo_s001.txt
mit_aristotle_de_caelo_s002.txt
mit_aristotle_de_caelo_s003.txt
mit_aristotle_de_caelo_s004.txt
mit_aristotle_de_interpretatione_idx.txt
mit_aristotle_de_interpretatione_s001.txt
mit_aristotle_de_interpretatione_s002.txt
mit_aristotle
… [548 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\ns=json.load(open('research/nipada/falsification/analytic_sigs_v1.json'))\nprint('sig keys',len(s))\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nsig_nodes={k for k,v in g.items() if v … [341 caractères tronqués]`

  ```
sig keys 44
sig_nodes 57 sig keys in graph 11 sig keys missing {'mengzi', 'schank_1972', 'aristotle_de_caelo', 'plato_gorgias', 'mn35_culasaccaka', 'voluspa', 'qiwulun', 'dn1_brahmajala', 'plato_phaedo', 'aristotle_prior_analytics', 'jeremiah_book', 'quillian_1968', 'sibylline_oracles', 'book_of_enoch', 'hosea_book', 'aristotle_posterior_analytics', 'plato_laws', 'plato_meno', 'zechariah_book', 'aristotle_categories', 'plato_charmides', 'ezekiel_book', '2_esdras', 'nostradamus_centuries', 'daniel_book', 'plato_sophist', 'mn2_sabbasava', 'curry_1930', 'aristotle_nicomachean_ethics', 'isaiah_book', 'miller_evidence_prophecy', 'russell_parousia_1878', 'aristotle_parts_of_animals'}
2_esdras | 100 | None | JUDEAN_APOCALYPTIC_LATE
aristotle_categories | -340 | grc | GRECO_LATIN_AXIAL
aristotle_de_caelo | -330 | grc | GRECO_LATIN_AXIAL
aristotle_nicomachean_ethics | -340 | grc | GRECO_LATIN_AXIAL
aristotle_parts_of_animals | -330 | grc | GRECO_LATIN_AXIAL
aristotle_posterior_analytics | -340 | grc | GRECO_LATIN_AXIAL
aristotle_prior_analytics | -340 | grc | GRECO_LATIN_AXIAL
bengio_2003 | 2003 | eng | NEURAL_LANGUAGE_MODELS
book_of_enoch | -200 | None | JUDEAN_APOCALYPTIC_LATE
curry_1930 
… [1762 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\ns=json.load(open('research/nipada/falsification/analytic_sigs_v1.json'))\nprint(len(s)); print(sorted(s))\nEOF", "description": "List signature keys"}`

  ```
44
['2_esdras', 'aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'curry_1930', 'daniel_book', 'dn1_brahmajala', 'ezekiel_book', 'hosea_book', 'isaiah_book', 'jeremiah_book', 'kleene_1936', 'lukasiewicz_1920', 'mengzi', 'mikolov_2013', 'miller_evidence_prophecy', 'mn2_sabbasava', 'mn35_culasaccaka', 'nostradamus_centuries', 'plato_charmides', 'plato_gorgias', 'plato_gorgias_jowett', 'plato_laws', 'plato_meno', 'plato_meno_jowett', 'plato_phaedo', 'plato_phaedrus_jowett', 'plato_philebus_jowett', 'plato_republic_jowett', 'plato_sophist', 'plato_symposium_jowett', 'plato_theaetetus_jowett', 'qiwulun', 'quillian_1968', 'russell_parousia_1878', 'schank_1972', 'sibylline_oracles', 'voluspa', 'zechariah_book']
  ```

- **bash** `{"command": "cd ../Panini && grep -rn \"334\" research/nipada/falsification/*.md docs/rapports/*2025-11-13* 2>/dev/null | head -40", "description": "Find §334 write-up"}`

  ```
docs/rapports/SESSION_FINALE_COMPLETE_2025-11-13.md:45:3. **VISUALISATION_EVOLUTION_2025-11-13.md** (334 lignes)
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\ns=json.load(open('research/nipada/falsification/analytic_sigs_v1.json'))\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nsig_nodes={k for k,v in g.items() if v.get('v14_signature')}\nprint(len(s),le … [177 caractères tronqués]`

  ```
44 57 11
missing ['2_esdras', 'aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'aristotle_prior_analytics', 'book_of_enoch', 'curry_1930', 'daniel_book', 'dn1_brahmajala', 'ezekiel_book', 'hosea_book', 'isaiah_book', 'jeremiah_book', 'mengzi', 'miller_evidence_prophecy', 'mn2_sabbasava', 'mn35_culasaccaka', 'nostradamus_centuries', 'plato_charmides', 'plato_gorgias', 'plato_laws', 'plato_meno', 'plato_phaedo', 'plato_sophist', 'qiwulun', 'quillian_1968', 'russell_parousia_1878', 'schank_1972', 'sibylline_oracles', 'voluspa', 'zechariah_book']
extra ['bhagavad_gita_arnold_en', 'carus_gospel_buddha_en', 'carvaka_fragments', 'confucius_analects_en', 'darwin_origin_de', 'darwin_origin_en', 'dhammapada_muller_en', 'epicurus_letters', 'feuerbach_christianity_en', 'feuerbach_wesen', 'great_learning_legge_en', 'han_feizi_selections', 'hobbes_leviathan_complete', 'holbach_systeme', 'holbach_systeme_en', 'hume_dialogues', 'hume_dialogues_nhr', 'ibn_rawandi_fragments', 'ingersoll_works', 'khayyam_rubaiyat_fitzgerald_en', 'koran_rodwell_en', 'lucretius_drn', 'lucretius_drn_en', 'marcus_aurelius_meditati
… [522 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\np=json.load(open('research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nnodes=set()\nfor x in p: nodes.add(x['a']); nodes.add(x['b'])\nprint('nodes in pairs',len(nodes)); print(sorted(nodes))\ns=json.load(open('rese … [498 caractères tronqués]`

  ```
nodes in pairs 48
['2_esdras', 'an7_64_kodhana', 'aristotle_categories', 'aristotle_de_anima', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'brahma_sutra_badarayana', 'curry_1930', 'daniel_book', 'dn1_brahmajala', 'ezekiel_book', 'hosea_book', 'isaiah_book', 'jeremiah_book', 'kleene_1936', 'lukasiewicz_1920', 'mengzi', 'mikolov_2013', 'miller_evidence_prophecy', 'mn2_sabbasava', 'mn35_culasaccaka', 'nostradamus_centuries', 'plato_charmides', 'plato_gorgias', 'plato_gorgias_jowett', 'plato_laws', 'plato_meno', 'plato_meno_jowett', 'plato_phaedo', 'plato_phaedrus_jowett', 'plato_philebus_jowett', 'plato_republic_jowett', 'plato_sophist', 'plato_symposium_jowett', 'plato_theaetetus_jowett', 'qiwulun', 'quillian_1968', 'russell_parousia_1878', 'schank_1972', 'sibylline_oracles', 'voluspa', 'zadeh_1965', 'zechariah_book']
pair nodes with sig 44 without ['an7_64_kodhana', 'aristotle_de_anima', 'brahma_sutra_badarayana', 'zadeh_1965']
no sig but graph sig ['an7_64_kodhana', 'aristotle_de_anima', 'brahma_sutra_badarayana', 'zadeh_1965']
2_esdras | y 100 | lan
… [3548 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nfor k in ['aristotle_categories','plato_gorgias','plato_gorgias_jowett','mengzi','qiwulun','dn1_brahmajala','isaiah_book','2_esdras','nostradamus_centu … [174 caractères tronqués]`

  ```
== aristotle_categories
{
 "kind": "canon_work",
 "author": "aristotle",
 "year": -340,
 "language_original": "grc",
 "tradition_label": "GRECO_LATIN_AXIAL",
 "tradition_micro": "GREEK_ARISTOTELIAN",
 "title_original": "Katēgoriai",
 "title_en": "Categories",
 "tags": [
  "aristotelian",
  "logic"
 ],
 "ingestion_status": "catalog_only",
 "v14_signature": null
}
== plato_gorgias
{
 "kind": "canon_work",
 "author": "plato",
 "year": -385,
 "language_original": "grc",
 "tradition_label": "GRECO_LATIN_AXIAL",
 "tradition_micro": "GREEK_PLATONIC",
 "title_original": "Gorgias (dialogue)",
 "title_en": "Gorgias",
 "tags": [
  "platonic"
 ],
 "ingestion_status": "catalog_only",
 "v14_signature": null
}
== plato_gorgias_jowett
{
 "kind": "corpus_work",
 "author": "Platon (Jowett)",
 "year": -380,
 "language_original": "grc",
 "language_version": "eng",
 "tradition_label": "GRECO_PLATONIC",
 "title_original": "Γοργίας",
 "title_en": "Gorgias",
 "ingestion_status": "signed_v295",
 "v14_signature": {
  "ÊTRE": 0.17973629,
  "DIFFÉRENCE": 0.14226232,
  "RAPPORT": 0.03435115,
  "ORIENTATION": 0.04337266,
  "SUJET": 0.09576683,
  "TEMPS": 0.05031228,
  "MODALITÉ": 0.06904927,
  "NOMBRE": 0.05170
… [5685 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, itertools, collections\np=json.load(open('research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nnodes=set()\nfor x in p: nodes.add(x['a']);  … [1466 caractères tronqués]`

  ```
G1 candidates exact trad 30
11 ('GRECO_LATIN_AXIAL', 'GRECO_PLATONIC')
10 ('GRECO_PLATONIC', 'GRECO_LATIN_AXIAL')
2 ('INDIAN_AXIAL', 'CHINESE_AXIAL')
1 ('CLASSICAL_ORACULAR', 'JUDEAN_APOCALYPTIC_LATE')
1 ('MANY_VALUED_LOGIC', 'COMBINATORY_LOGIC')
1 ('COMBINATORY_LOGIC', 'RECURSIVE_FUNCTIONS')
1 ('FUZZY_LOGIC', 'SEMANTIC_NETWORKS')
1 ('FUZZY_LOGIC', 'CONCEPTUAL_DEPENDENCY')
1 ('SEMANTIC_NETWORKS', 'CONCEPTUAL_DEPENDENCY')
1 ('NEURAL_LANGUAGE_MODELS', 'DISTRIBUTIONAL_SEMANTICS')
--- coarse diff
3 5
2 ('INDIAN', 'CHINESE')
2 ('LOGIC', 'AI')
1 ('CLASSICAL_ORACULAR', 'ABRAHAM')
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nd=json.load(open('reports/panini-334.json'))\nps=d['paires']['paires']\nprint(len(ps)); print(json.dumps(ps[0],ensure_ascii=False,indent=1))\nprint('--- fields')\nfor k in ps[0]: print(k, collections.Counter(str(x.get(k)) for x in ps).most_co … [242 caractères tronqués]`

  ```
488
{
 "a": "dn1_brahmajala",
 "b": "mn2_sabbasava",
 "section": "a",
 "d_topo": 3.6,
 "d_lex": 0.33870554623886845,
 "cos": 0.7492899129132787,
 "dy": 10.0,
 "meme_tradition_large": true,
 "meme_tradition_fine": true,
 "meme_auteur": true
}
--- fields
a [('zadeh_1965', 30), ('lukasiewicz_1920', 29), ('kleene_1936', 28), ('curry_1930', 27), ('quillian_1968', 26), ('schank_1972', 25)]
b [('plato_philebus_jowett', 30), ('plato_theaetetus_jowett', 29), ('plato_gorgias_jowett', 28), ('plato_meno_jowett', 27), ('plato_phaedrus_jowett', 26), ('plato_symposium_jowett', 25)]
section [('a', 322), ('b', 150), ('c', 16)]
d_topo [('0.01', 48), ('1.0', 48), ('1.01', 44), ('1.03', 25), ('9.459999999999999', 24), ('0.02', 20)]
d_lex [('0.33870554623886845', 1), ('0.25142955342124895', 1), ('0.1759746945506818', 1), ('0.19678634403070785', 1), ('0.2191822399503319', 1), ('0.28569203665297943', 1)]
cos [('0.7492899129132787', 1), ('0.8085855379994222', 1), ('0.8748775343155926', 1), ('0.8395924924926331', 1), ('0.7961964231191426', 1), ('0.8244204847568499', 1)]
dy [('10.0', 24), ('40.0', 24), ('30.0', 22), ('50.0', 22), ('45.0', 21), ('0.0', 19)]
meme_tradition_large [('False', 308), ('True', 180)
… [128 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && ls research/nipada/falsification | grep -i -E \"334|date|pair|v150|graph\" ; echo \"---\"; python3 - <<'EOF'\nimport json\nd=json.load(open('research/nipada/falsification/nipada_v150_validation.json'))\nprint(type(d), list(d)[:30] if isinstance(d,dict) else len(d))\nif i … [300 caractères tronqués]`

  ```
nipada_v148_inheritance_graph.json
nipada_v150_validation.json
nipada_v159_inheritance_graph_v2.json
nipada_v160_validation_graph_v2.json
nipada_v168_inheritance_graph_v3.json
nipada_v172_graph_v4.json
nipada_v176_graph_v5.json
nipada_v178_graph_v6.json
nipada_v179_graph_v7.json
nipada_v182_graph_v8.json
nipada_v189_graph_v9.json
nipada_v199_graph_v10.json
nipada_v207_graph_v10.json
nipada_v208_graph_v11.json
nipada_v210a_graph_v12.json
nipada_v219_graph_v13.json
nipada_v243c_graph_v14c.json
nipada_v243_graph_v14.json
nipada_v244_graph_v15b.json
nipada_v244_graph_v15c.json
nipada_v244_graph_v15d.json
nipada_v244_graph_v15e.json
nipada_v244_graph_v15.json
nipada_v245_graph_v15f.json
nipada_v246_graph_v15g.json
nipada_v247_graph_v15h.json
nipada_v248_graph_v15i.json
nipada_v249_graph_v15j.json
nipada_v250_graph_v15k.json
nipada_v251_graph_v15l.json
nipada_v252_graph_v15m.json
nipada_v253_graph_v15n.json
nipada_v254_graph_v15o.json
nipada_v255_graph_v15p.json
nipada_v256_graph_v15q.json
nipada_v257_graph_v15r.json
nipada_v258_graph_v15s.json
nipada_v264_graph_patch_report.json
nipada_v264_graph_v16p.json
nipada_v265_graph_patch_report.json
nipada_v265_graph_v17p.json
nipada_v266_graph
… [3392 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, itertools, collections\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nnodes=[(k,v) for k,v in g.items() if v.get('v14_signature') and v.get('year') is not None]\nprint('dated signed',len(nodes))\nr … [1109 caractères tronqués]`

  ```
dated signed 49
('tao_te_ching_legge_en', -600, 'lzh', 'DAOISM', None, 'Laozi (Legge)')
('mozi_selections', -400, 'lzh', 'CHINESE_RATIONALIST', None, 'mozi')
('great_learning_legge_en', -400, 'lzh', 'CONFUCIAN_AXIAL', None, 'Zengzi/Legge')
('plato_euthyphro_jowett', -399, 'grc', 'GRECO_PLATONIC', None, 'Platon (Jowett)')
('plato_crito_jowett', -399, 'grc', 'GRECO_PLATONIC', None, 'Platon (Jowett)')
('plato_symposium_jowett', -385, 'grc', 'GRECO_PLATONIC', None, 'Platon (Jowett)')
('plato_meno_jowett', -385, 'grc', 'GRECO_PLATONIC', None, 'Platon (Jowett)')
('plato_republic_jowett', -380, 'grc', 'GRECO_PLATONIC', None, 'Platon (Jowett)')
('plato_gorgias_jowett', -380, 'grc', 'GRECO_PLATONIC', None, 'Platon (Jowett)')
('plato_republic_fr', -380, 'grc', 'GRECO_PLATONIC', None, 'Platon (Cousin)')
('plato_phaedrus_jowett', -370, 'grc', 'GRECO_PLATONIC', None, 'Platon (Jowett)')
('plato_theaetetus_jowett', -369, 'grc', 'GRECO_PLATONIC', None, 'Platon (Jowett)')
('plato_philebus_jowett', -360, 'grc', 'GRECO_PLATONIC', None, 'Platon (Jowett)')
('epicurus_letters', -300, 'grc', 'GRECO_LAT_MATERIAL', None, 'Épicure')
('carvaka_fragments', -300, 'san', 'INDIAN_MATERIAL', None, 'Cārvāka / Lokā
… [3048 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, itertools\nfrom collections import Counter\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nrows=[(k,v.get('year'),v.get('language_original') or v.get('lang'),v.get('tradition_label'),v.get('traditio … [1434 caractères tronqués]`

  ```
G1 exact label diff <=10: 28
  3 ('AMERICAN_FREETHINKER', 'EUR_ANTI_CHRISTIAN')
  2 ('CHINESE_RATIONALIST', 'GRECO_PLATONIC')
  2 ('CONFUCIAN_AXIAL', 'GRECO_PLATONIC')
  2 ('EUR_PESSIMIST_CRITIC', 'EVOLUTION_NATURELLE')
  2 ('MATERIALIST_MODERN', 'EVOLUTION_NATURELLE')
  1 ('CHINESE_RATIONALIST', 'CONFUCIAN_AXIAL')
  1 ('GRECO_LAT_MATERIAL', 'INDIAN_MATERIAL')
  1 ('STOIC_ROMAN', 'SCEPT')
  1 ('MODERN_WESTERN', 'EUR_MATERIALIST_ATHEIST')
  1 ('MODERN_WESTERN', 'FRENCH_ENLIGHTENMENT')
  1 ('MODERN_WESTERN', 'EUR_SCEPTICAL_EMPIRICIST')
  1 ('EUR_MATERIALIST_ATHEIST', 'FRENCH_ENLIGHTENMENT')
  1 ('EUR_MATERIALIST_ATHEIST', 'EUR_SCEPTICAL_EMPIRICIST')
  1 ('FRENCH_ENLIGHTENMENT', 'EUR_SCEPTICAL_EMPIRICIST')
  1 ('MODERN_WESTERN', 'EUR_RATIONALIST_CRITIC')
  1 ('MODERN_WESTERN', 'EUR_PESSIMIST_CRITIC')
  1 ('EUR_RATIONALIST_CRITIC', 'EUR_PESSIMIST_CRITIC')
  1 ('EUR_PESSIMIST_CRITIC', 'MATERIALIST_MODERN')
  1 ('COGNITIVE_LIMITS', 'FUZZY_LOGIC')
  1 ('NEURAL_LANGUAGE_MODELS', 'DISTRIBUTIONAL_SEMANTICS')
  1 ('NEURAL_LANGUAGE_MODELS', 'NEUROSEMIOTICS')
  1 ('DISTRIBUTIONAL_SEMANTICS', 'NEUROSEMIOTICS')
G1 micro diff <=10: 4
  1 ('WORKING_MEMORY_CAPACITY', 'MEMBERSHIP_FUNCTIONS')
  1 ('DI
… [1432 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, itertools\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nrows=[(k,v.get('year'),v.get('language_original') or v.get('lang'),v.get('tradition_label'),v.get('author')) for k,v in g.items() if v.get(' … [434 caractères tronqués]`

  ```
0  epicurus_letters                          -300 GRECO_LAT_MATERIAL       | carvaka_fragments                         -300 INDIAN_MATERIAL          | sameauth=False
  0  feuerbach_wesen                           1841 MODERN_WESTERN           | feuerbach_christianity_en                 1841 EUR_RATIONALIST_CRITIC   | sameauth=False
  0  holbach_systeme                           1770 MODERN_WESTERN           | holbach_systeme_en                        1770 EUR_MATERIALIST_ATHEIST  | sameauth=False
  0  holbach_systeme                           1770 MODERN_WESTERN           | voltaire_oeuvres_33_fr                    1770 FRENCH_ENLIGHTENMENT     | sameauth=False
  0  holbach_systeme_en                        1770 EUR_MATERIALIST_ATHEIST  | voltaire_oeuvres_33_fr                    1770 FRENCH_ENLIGHTENMENT     | sameauth=False
  0  marx_critique_political_economy_en        1859 MATERIALIST_MODERN       | darwin_origin_en                          1859 EVOLUTION_NATURELLE      | sameauth=False
  0  mikolov_2013                              2013 DISTRIBUTIONAL_SEMANTICS | pulvermuller_2013                         2013 NEUROSEMIOTICS           | sameauth=False
  0  mozi_selections      
… [3510 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"B1\\|protocole.*date\\|date contrôlée\\|date control\" docs/ journal/ reports/ --include=*.md --include=*.json 2>/dev/null | head -40", "description": "Search for B1 task description"}`

  ```
docs/archive/etat-modules-2026-10-10.md:5:> corrigés (`docs/archive/`), B10–B12 réintégrés dans les cartes. **Les règles d'`AGENTS.md`
docs/archive/roadmap-detail-2026-10-29.md:10:> base. Le format **DRVM** et le modèle **`drave-n0`** deviennent la **ligne principale** ; B9/B10/B11 passent
docs/archive/roadmap-detail-2026-10-29.md:29:| **B — l'intelligence** | B1–B12 : la langue, la pensée, les jeux, les maîtres, le banc externe, la sémantique | B1.5 (corpus), B10.3 (décodeur), B12.10 (modules) |
docs/archive/roadmap-detail-2026-10-29.md:149:### B1 — L'entrée-sortie linguistique (étage 1)
docs/archive/roadmap-detail-2026-10-29.md:153:| B1.1 | **Le juge post-cutoff** : un texte neuf, jamais vu à l'entraînement | ✅ | le règlement 2025 (139 unités) ; l'UDHR contaminée (le 7 B récite) ; toutes les mesures refaites |
docs/archive/roadmap-detail-2026-10-29.md:154:| B1.2 | **La qualité de traducteur** : chrF + plancher + marge + intervalle | ✅ | **55-76**, marge **+30 à +40**, répliquée sur un second règlement |
docs/archive/roadmap-detail-2026-10-29.md:155:| B1.3 | **Les six registres** : juridique, presse, littéraire, parlé préparé, technique (JRC et prose), dialogue | ✅ | marges de +25
… [8286 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' reports/rapport-panini-334.md", "description": "Read Panini 334 technical report part 1"}`

  ```
# J12.1 — Le §334 et les 44 œuvres : le retrieval et la prédiction de l'époque vs la filiation

> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, J12.1 · **Date** : 2026-11-14
> **Verdict** : ✅ **le §334 est une géométrie de filiation, pas d'époque — et le corpus ne permet pas
> de séparer les deux.** La loi H0 de Panini se reproduit (**R² = 0,909139** sur les **655 lignes** de
> paires ; **0,906307** sur les **488 paires uniques non auto**), et l'époque seule explique **0,258**
> de la distance lexicale ; mais elle n'ajoute que **0,0089** de R² **après** la topologie
> (p = 0,86 ; β standardisé **−0,035**). Le plan est **colinéaire** : **180** paires de même tradition
> ont **28,7 ans** d'écart en moyenne (max **230**), les **308** paires inter-traditions en ont
> **1 189** (**136** à ≤ 100 ans). Le contraste de filiation à **date fixe** est fort dans la tranche
> axiale (**Δ = −0,166**, p = 0,0005), mais **disparaît à surface contrôlée** (même langue source
> anglaise : **Δ = −0,135** contre un null de **−0,129**, p = 0,34).
> Sur les **44 signatures** (14 parts flottantes), le retrieval brut donne **61,4 %** de même tradition
> (hasard 22,4 %) et **56,8
… [11901 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '180,384p' reports/rapport-panini-334.md", "description": "Read rest of Panini 334 report"}`

  ```
filiation à date fixe est donc **concentré dans les paires grecques / non grecques**, où la langue
source n'est pas documentée : on ne peut pas le distinguer d'un effet de **source/traduction**.

### 4.4 La tradition seule, et ce qu'elle devient après la topologie

`d_lex ~ 1 + même_tradition_large` donne **R² = 0,369** et **β = −0,189** : les paires de même
tradition sont plus proches. Mais après `d_topo^0,67`, le coefficient de la tradition devient
**−0,0067** et le R² partiel **0,0030** (p = 0,49) : la topologie **absorbe** la tradition. Ce n'est
pas une contradiction : `d_topo` est la distance de transmission qui **définit** la filiation ; le label
de tradition n'ajoute presque rien à sa version topologique. La question « filiation vs époque » au
niveau paire est donc, de fait, « **topologie vs date** » — et la topologie gagne.

## 5. Résultats au niveau œuvre — le retrieval brut, et ce que les contrôles en gardent

### 5.1 Le top-1 brut

| cible du top-1 | observé | hasard | enrichissement | n/44 |
|---|---:|---:|---:|---:|
| **même tradition large** | **61,4 %** | 22,4 % | **2,74×** | **27** |
| **même auteur canonique** | **36,4 %** | 10,0 % | **3,64×** | **16** |
| **à ≤ 50
… [13049 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/panini_334.py", "description": "Read panini_334 tool"}`

  ```
#!/usr/bin/env python3
"""panini_334.py — J12.1 : le corpus §334 et les signatures des 44 œuvres.

LA QUESTION. Panini/Nipada ont mesuré que leur signature lexicale capte l'époque
(β +0,138) bien plus que la filiation (β +0,049). J12.1 demande la même chose sur
la **deuxième vague** de leurs artefacts : le corpus §334 (114 textes actifs, 655
paires finies, 102 sources acquises) et les signatures V14 de 44 œuvres (14 parts
flottantes). Le retrieval retrouve-t-il la **filiation** ou l'**époque** ? La
prédiction de l'année est-elle plus forte que celle de la tradition ? Et que
devient cet arbitrage quand on **contrôle la date** ?

CE QUI EST MESURÉ, EN DEUX TEMPS.
  1. **Niveau paire (655 paires)** : la loi H0 de Panini
     `d_lex ~ d_topo^0,67` (R² = 0,909139 officiel) est reproduite, puis opposée
     à un modèle d'**époque** (`d_lex ~ |Δannée|`), à un modèle joint et à un
     modèle inverse (`d_topo^0,67 ~ |Δannée|`). Les coefficients standardisés,
     les R² partiels et les intervalles bootstrap par texte disent laquelle des
     deux variables porte la variance — et si le plan permet seulement de les
     séparer.
  2. **Niveau œuvre (44 signatures)** : retrieval du plus proch
… [5969 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\ns=set(json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json')))\ng=json.load(open('../Panini/research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nfor k in sorted(s):\n    v=g.get(k,{})\n    print(f\"{k:40s} {str(v. … [163 caractères tronqués]`

  ```
2_esdras                                    100  None JUDEAN_APOCALYPTIC_LATE      anonymous (Ezra apocalypse tradition)
aristotle_categories                       -340   grc GRECO_LATIN_AXIAL            aristotle
aristotle_de_caelo                         -330   grc GRECO_LATIN_AXIAL            aristotle
aristotle_nicomachean_ethics               -340   grc GRECO_LATIN_AXIAL            aristotle
aristotle_parts_of_animals                 -330   grc GRECO_LATIN_AXIAL            aristotle
aristotle_posterior_analytics              -340   grc GRECO_LATIN_AXIAL            aristotle
aristotle_prior_analytics                  -340   grc GRECO_LATIN_AXIAL            aristotle
bengio_2003                                2003   eng NEURAL_LANGUAGE_MODELS       Yoshua Bengio
book_of_enoch                              -200  None JUDEAN_APOCALYPTIC_LATE      anonymous (R.H. Charles trans. 1913)
curry_1930                                 1930   eng COMBINATORY_LOGIC            Haskell B. Curry
daniel_book                                -165  None ABRAHAMIC_PROPHETIC_AXIAL    anonymous (Daniel tradition)
dn1_brahmajala                             -440   pli BUDDHIST_AXIAL               anonymous
… [3251 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, itertools, collections\nS=set(json.load(open('research/nipada/falsification/analytic_sigs_v1.json')))\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\np=json.load(open('research/nipada/falsification/ … [2614 caractères tronqués]`

  ```
unique unordered pairs among 44: 374 of 946
missing pairs: 572
dups rows 98 max 4
trad large counts Counter({'GRECO': 19, 'ABRAHAMIC': 8, 'COGNITIVE_SCIENCE': 4, 'FORMAL_LOGIC': 3, 'BUDDHIST': 3, 'MILLENARIAN': 2, 'CHINESE': 2, 'RENAISSANCE_OCCULT': 1, 'CLASSICAL_ORACULAR': 1, 'NORSE_EDDIC': 1})
G1 large diff <=10, distinct author: 1 {('CLASSICAL_ORACULAR', 'ABRAHAMIC'): 1}
G1 large diff <=20, distinct author: 1 {('CLASSICAL_ORACULAR', 'ABRAHAMIC'): 1}
G1 large diff <=50, distinct author: 39 {('GRECO', 'CHINESE'): 9, ('ABRAHAMIC', 'CLASSICAL_ORACULAR'): 1, ('FORMAL_LOGIC', 'COGNITIVE_SCIENCE'): 5, ('GRECO', 'BUDDHIST'): 5, ('FORMAL_LOGIC', 'MILLENARIAN'): 1, ('BUDDHIST', 'GRECO'): 12, ('CHINESE', 'GRECO'): 5, ('CLASSICAL_ORACULAR', 'ABRAHAMIC'): 1}
G2 same large <=200 distinct author: 141 {'GRECO': 120, 'ABRAHAMIC': 10, 'MILLENARIAN': 1, 'FORMAL_LOGIC': 3, 'COGNITIVE_SCIENCE': 6, 'CHINESE': 1}
G3 same lang cross large trad: 8 {'eng': 8}
G3 same lang same large trad: 120 {'grc': 113, 'eng': 7}
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, itertools, collections\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nrows=[(k,v.get('year'),v.get('language_original') or v.get('lang'),v.get('tradition_label'),v.get('author')) for k,v in g.items … [1912 caractères tronqués]`

  ```
trad large Counter({'EUROPE_MODERN': 15, 'GRECO': 11, 'CHINESE': 5, 'COGNITIVE_SCIENCE': 4, 'FORMAL_LOGIC': 3, 'ANCIENT_EPICUREAN': 2, 'EVOLUTION_NATURELLE': 2, 'SCEPT': 1, 'INDIAN': 1, 'ISLAMIC_RATIONALIST': 1, 'AMERICAN_FREETHINKER': 1, 'MATERIALIST_MODERN': 1, 'ISLAMIC': 1, 'STOIC_ROMAN': 1})
G1 large diff <=10 distinct author: 15
  3 ('EUROPE_MODERN', 'AMERICAN_FREETHINKER')
  2 ('CHINESE', 'GRECO')
  2 ('EUROPE_MODERN', 'EVOLUTION_NATURELLE')
  2 ('GRECO', 'CHINESE')
  2 ('MATERIALIST_MODERN', 'EVOLUTION_NATURELLE')
  1 ('GRECO', 'INDIAN')
  1 ('SCEPT', 'STOIC_ROMAN')
  1 ('EUROPE_MODERN', 'MATERIALIST_MODERN')
  1 ('COGNITIVE_SCIENCE', 'FORMAL_LOGIC')
0 epicurus_letters -300 GRECO | carvaka_fragments -300 INDIAN
0 marx_critique_political_economy_en 1859 MATERIALIST_MODERN | darwin_origin_en 1859 EVOLUTION_NATURELLE
1 marx_critique_political_economy_en 1859 MATERIALIST_MODERN | darwin_origin_de 1860 EVOLUTION_NATURELLE
1 mozi_selections -400 CHINESE | plato_crito_jowett -399 GRECO
1 mozi_selections -400 CHINESE | plato_euthyphro_jowett -399 GRECO
1 plato_crito_jowett -399 GRECO | great_learning_legge_en -400 CHINESE
1 plato_euthyphro_jowett -399 GRECO | great_learning_legge_en
… [693 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nprint('nodes',len(g))\ndated=[(k,v) for k,v in g.items() if v.get('year') is not None]\nprint('dated',len(dated))\nprint('with sig',sum(1  … [565 caractères tronqués]`

  ```
nodes 1753
dated 1730
with sig 57
trad labels 66
[('BUDDHIST_LATE_ANTIQUE', 70), ('BUDDHIST_MEDIEVAL', 70), ('CHINESE_EARLY_MODERN', 70), ('CHINESE_LATE_ANTIQUE', 70), ('CHINESE_MEDIEVAL', 70), ('CHINESE_MODERN', 70), ('GRECO_LATIN_LATE_ANTIQUE', 70), ('GRECO_LATIN_MEDIEVAL', 70), ('INDIAN_EARLY_MODERN', 70), ('INDIAN_LATE_ANTIQUE', 70), ('INDIAN_MEDIEVAL', 70), ('INDIAN_MODERN', 70), ('ISLAMIC_MEDIEVAL', 70), ('ISLAMIC_MODERN', 70), ('ORIENTALIST_TRANSLATION_MODERN', 70), ('WESTERN_RADICAL_CONTEMPORARY', 70), ('WESTERN_RADICAL_MODERN', 70), ('WESTERN_RATIONAL_CONTEMPORARY', 70), ('WESTERN_RATIONAL_MODERN', 70), ('WESTERN_RATIONAL_EARLY_MODERN', 69), ('BUDDHIST_AXIAL', 65), ('CHINESE_AXIAL', 60), ('GRECO_LATIN_AXIAL', 52), ('INDIAN_AXIAL', 51), (None, 36), ('GRECO_PLATONIC', 10), ('ABRAHAMIC_PROPHETIC_AXIAL', 6), ('MODERN_WESTERN', 3), ('EUR_RATIONALIST_CRITIC', 3), ('EUR_ANTI_CHRISTIAN', 3)]
kinds [('canon_work', 1626), ('pivot_author', 37), ('corpus_work', 22), ('proto_atheist_work', 20), ('reference_scientific', 10), ('prophetic_text', 7), ('apocalyptic_text', 2), ('interpretive_work', 2), ('philosopher_proto', 1), (None, 1), ('oracular_text', 1), ('eddic_poem', 1)]
langs [('lzh
… [1780 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, itertools, collections\nS=set(json.load(open('research/nipada/falsification/analytic_sigs_v1.json')))\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nrows=[(k,g[k].get('year'),g[k].get('language_ori … [439 caractères tronqués]`

  ```
0 book_of_enoch                        -200 JUDEAN_APOCALYPTIC_LATE    | sibylline_oracles                    -200 CLASSICAL_ORACULAR         | lang None/None
  0 plato_meno_jowett                    -385 GRECO_PLATONIC             | plato_gorgias                        -385 GRECO_LATIN_AXIAL          | lang grc/grc
  0 plato_meno_jowett                    -385 GRECO_PLATONIC             | plato_meno                           -385 GRECO_LATIN_AXIAL          | lang grc/grc
  0 plato_phaedo                         -380 GRECO_LATIN_AXIAL          | plato_gorgias_jowett                 -380 GRECO_PLATONIC             | lang grc/grc
  0 plato_phaedo                         -380 GRECO_LATIN_AXIAL          | plato_republic_jowett                -380 GRECO_PLATONIC             | lang grc/grc
  0 plato_sophist                        -360 GRECO_LATIN_AXIAL          | plato_philebus_jowett                -360 GRECO_PLATONIC             | lang grc/grc
  0 plato_symposium_jowett               -385 GRECO_PLATONIC             | plato_gorgias                        -385 GRECO_LATIN_AXIAL          | lang grc/grc
  0 plato_symposium_jowett               -385 GRECO_PLATONIC             | plato_meno  
… [2942 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\nfor f in ['research/nipada/falsification/nipada_v334_graph_v35_gps.json','research/nipada/falsification/nipada_v336_graph_v36.json','research/nipada/falsification/nipada_v338_graph_v36.json']:\n    print('==',f)\n    try:\n        d=json.l … [483 caractères tronqués]`

  ```
== research/nipada/falsification/nipada_v334_graph_v35_gps.json
<class 'dict'> ['version', 'section', 'iso_from_v34', 'nodes', 'edges']
  version <class 'str'> 3
  section <class 'str'> 4
  iso_from_v34 <class 'list'> 2
  nodes <class 'dict'> 1753
  edges <class 'list'> 19967
 nodes 1753 signed 57
== research/nipada/falsification/nipada_v336_graph_v36.json
<class 'dict'> ['version', 'section', 'source_graph', 'densification_strategy', 'nodes', 'edges']
  version <class 'str'> 3
  section <class 'str'> 4
  source_graph <class 'str'> 21
  densification_strategy <class 'str'> 16
  nodes <class 'dict'> 1753
 nodes 1753 signed 57
== research/nipada/falsification/nipada_v338_graph_v36.json
<class 'dict'> ['version', 'section', 'densification', 'base_graph', 'added_edges', 'nodes', 'edges']
  version <class 'str'> 3
  section <class 'str'> 4
  densification <class 'str'> 35
  base_graph <class 'str'> 3
  added_edges <class 'int'> 
 nodes 1753 signed 57
  ```

- **bash** `{"command": "cd ../Panini && grep -rn \"v14_signature\" research/nipada/falsification/*.json 2>/dev/null | head -5; echo \"---\"; ls research/nipada/falsification | grep -i sig", "description": "Search signature artifacts"}`

  ```
research/nipada/falsification/nipada_holdout_v1.json:17:   "v14_signature": {
research/nipada/falsification/nipada_holdout_v1.json:38:   "v14_signature": {
research/nipada/falsification/nipada_holdout_v1.json:59:   "v14_signature": {
research/nipada/falsification/nipada_holdout_v1.json:80:   "v14_signature": {
research/nipada/falsification/nipada_holdout_v1.json:101:   "v14_signature": {
---
analytic_sigs_v1.json
modern_corpus_sigs_v2.json
modern_sigs_v1.json
nipada_v151_dense_signatures.json
nipada_v212_propagated_signatures.json
nipada_v223_significance.json
nipada_v280_resign_report.json
structured_sigs_v1.json
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\nfor f in ['nipada_v151_dense_signatures.json','nipada_v212_propagated_signatures.json','modern_sigs_v1.json','structured_sigs_v1.json','modern_corpus_sigs_v2.json']:\n    p='research/nipada/falsification/'+f\n    print('==',f)\n    try: d= … [896 caractères tronqués]`

  ```
== nipada_v151_dense_signatures.json
<class 'dict'> ['version', 'step', 'summary', 'prototypes', 'fragment_signatures', 'work_signatures_aggregated', 'top_fragments_per_atom']
  version <class 'str'> 4
  step <class 'str'> 54
  summary <class 'dict'> 9
  prototypes <class 'dict'> 14
  fragment_signatures <class 'dict'> 50
 cand keys 7 sample ['version', 'step', 'summary']
 sample val "v151"
== nipada_v212_propagated_signatures.json
<class 'dict'> ['version', 'max_hops', 'prop_weights', 'n_signed_input', 'n_unsigned', 'n_propagated', 'coverage_pct', 'propagated_signatures']
  version <class 'str'> 9
  max_hops <class 'int'> 
  prop_weights <class 'dict'> 3
  n_signed_input <class 'int'> 
  n_unsigned <class 'int'> 
 cand keys 8 sample ['version', 'max_hops', 'prop_weights']
 sample val "v212-prop"
== modern_sigs_v1.json
<class 'dict'> ['2_esdras', 'aristotle_categories', 'aristotle_nicomachean_ethics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'daniel_book', 'dn1_brahmajala']
  2_esdras <class 'dict'> 14
  aristotle_categories <class 'dict'> 14
  aristotle_nicomachean_ethics <class 'dict'> 14
  aristotle_prior_analytics <class 'dict'> 14
  bengio_2003 <class 'dict
… [2070 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\nd=json.load(open('research/nipada/falsification/nipada_v151_dense_signatures.json'))\nprint(json.dumps(d['summary'],ensure_ascii=False,indent=1))\nw=d.get('work_signatures_aggregated',{})\nprint('work agg',type(w),len(w), list(w)[:5])\nif  … [492 caractères tronqués]`

  ```
{
 "model": "paraphrase-multilingual-MiniLM-L12-v2",
 "embedding_dim": 384,
 "n_atoms": 14,
 "n_prototypes_per_atom": 3,
 "n_fragments": 50,
 "n_works": 10,
 "cos_min_global": -0.0478,
 "cos_mean_global": 0.2114,
 "cos_max_global": 0.5246
}
work agg <class 'dict'> 10 ['carvaka_fragments', 'democritus_fragments', 'epicurus_letters', 'feuerbach_wesen', 'holbach_systeme']
{"ÊTRE": 0.216, "DIFFÉRENCE": 0.2356, "RAPPORT": 0.2702, "ORIENTATION": 0.2708, "SUJET": 0.3163, "TEMPS": 0.1982, "MODALITÉ": 0.2568, "NOMBRE": 0.292, "ESPACE": 0.3005, "OPÉRATION": 0.2178, "FONCTION": 0.2805, "STRUCTURE": 0.1827, "SYMÉTRIE": 0.2479, "ÉQUATION": 0.2715}
v212 {'version': 'v212-prop', 'max_hops': 2, 'n_signed_input': 37, 'n_unsigned': 1727, 'n_propagated': 254, 'coverage_pct': 14.71}
<class 'dict'> 254 ['leucippe', 'anaxagore', 'pyrrhon']
{"ÊTRE": 0.0965697174453276, "DIFFÉRENCE": 0.20906695469213102, "RAPPORT": 0.1426845475310406, "ORIENTATION": 0.013445886519488182, "SUJET": 0.09942122714029696, "TEMPS": 0.0644356046361059, "MODALITÉ": 0.17396249423290425, "NOMBRE": 0.050999182942694364, "ESPACE": 0.020320581117990753, "OPÉRATION":
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nkeys=collections.Counter()\nfor v in g.values(): keys.update(v.keys())\nprint(keys.most_common(40))\n# titles duplicates\nimport re\ndef n … [552 caractères tronqués]`

  ```
[('kind', 1749), ('author', 1735), ('year', 1730), ('tradition_label', 1714), ('ingestion_status', 1701), ('v14_signature', 1698), ('language_original', 1673), ('title_en', 1673), ('title_original', 1660), ('tradition_micro', 1651), ('tags', 1638), ('label', 40), ('lang', 29), ('v14_top3', 29), ('n_words', 29), ('signed_n_chars', 28), ('language_version', 22), ('source_type', 13), ('tradition', 11), ('publisher', 10), ('relevance_score', 10), ('nipada_relation', 10), ('url', 10), ('note', 9), ('added_in', 4), ('interprets_ref', 2), ('id', 1), ('type', 1), ('source', 1), ('title', 1)]
dated canonical (author,title) groups 1668 dups 29 max 11
[(('james legge', None), 11), (('platon jowett', ''), 9), (('edward west', None), 5), (('julius eggeling', None), 5), (('max muller', None), 4), (('hermann oldenberg', None), 4), (('nietzsche', None), 3), (('georg buhler', None), 3), (('rhys davids tw', None), 3), (('rhys davids tw oldenberg', None), 3)]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, re, itertools, collections\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\ndef norm(s):\n    if not s: return ''\n    s=s.lower()\n    s=re.sub(r'\\(.*?\\)','',s)\n    s=re.sub(r'trans\\.?.*$','',s) … [1311 caractères tronqués]`

  ```
rows 1730
all dated: diff raw label, diff author, <=10: 24229 label pairs 312
  both signed: 28
  one signed: 1479
  top [(('CHINESE_MODERN', 'INDIAN_MODERN'), 1721), (('WESTERN_RADICAL_CONTEMPORARY', 'WESTERN_RATIONAL_CONTEMPORARY'), 1294), (('INDIAN_MODERN', 'ORIENTALIST_TRANSLATION_MODERN'), 1258), (('CHINESE_MODERN', 'WESTERN_RADICAL_MODERN'), 1241), (('INDIAN_MODERN', 'ISLAMIC_MODERN'), 1163), (('INDIAN_MODERN', 'WESTERN_RADICAL_MODERN'), 1158), (('CHINESE_MODERN', 'ISLAMIC_MODERN'), 1131), (('ISLAMIC_MODERN', 'ORIENTALIST_TRANSLATION_MODERN'), 1051), (('ORIENTALIST_TRANSLATION_MODERN', 'WESTERN_RADICAL_MODERN'), 1036), (('ORIENTALIST_TRANSLATION_MODERN', 'WESTERN_RATIONAL_MODERN'), 965)]
  diff family prefix: 21844
  ```

- **bash** `{"command": "sed -n '1,120p' docs/methode/resultats.md", "description": "Read results method doc"}`

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

- **bash** `{"command": "sed -n '1,80p' reports/rapport-gold-reel-50.md 2>/dev/null; echo \"---JSON---\"; python3 - <<'EOF'\nimport json\ntry:\n    d=json.load(open('reports/rapport-gold-reel-50.json'))\n    print(type(d), list(d)[:20] if isinstance(d,dict) else len(d))\nexcept Exception as e: print(e)\nEOF", " … [44 caractères tronqués]`

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
… [3953 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"B1\\|Panini\\|4A\\|protocole\" docs/pilotage/en-cours.md | head -40; echo \"---\"; sed -n '1,60p' docs/pilotage/en-cours.md", "description": "Check current state for B1"}`

  ```
60:- **Plan** : B13.
64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)).
90:- **Pensée — B13 (actif)** : **183/183**, gold 432 ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, restitution v1 (46/46, strict 0,1087), **J9.1** (19 fiches) ; [s065](../../reports/rapport-s065.md), [restitution v1](../../reports/rapport-restitution-v1.md), [J9.1](../../reports/rapport-passe-honnetete.md).
92:- **Panini J2.1–J3.2** : table **14 atomes** ; UDHR **418/438** ; J3.1 script domine, date non significative ; J3.2 : **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, **V14 3/21** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rap
… [4804 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"B1\\|Panini\\|4A\\|protocole\" docs/pilotage/roadmap.md | head -40", "description": "Check roadmap for B1"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [16482 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections, re\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\n# sample nodes with different labels\nseen=set()\nfor k,v in g.items():\n    t=v.get('tradition_label')\n    if t in seen or v.get('ye … [396 caractères tronqués]`

  ```
epicurus_letters | -300 | GRECO_LAT_MATERIAL | None | 'Épicure' | None | None | grc | sig True
lucretius_drn | -55 | ANCIENT_EPICUREAN | None | 'lucretius' | None | None | eng | sig True
sextus_pyrrho | 190 | SCEPT | None | 'Sextus Empiricus' | None | None | grc | sig True
carvaka_fragments | -300 | INDIAN_MATERIAL | None | 'Cārvāka / Lokāyata (école)' | None | None | san | sig True
wang_chong_lunheng | 80 | CHINESE_MATERIAL | None | 'Wang Chong' | None | None | zho | sig True
ibn_rawandi_fragments | 870 | ISLAMIC_RATIONALIST | None | 'Ibn al-Rāwandī' | None | None | ara | sig True
hume_dialogues | 1751 | MODERN_WESTERN | None | 'David Hume' | None | None | eng | sig True
leucippe | -440 | None | None | 'leucippe' | None | None | None | sig False
mozi | -430 | CHINESE_AXIAL | CHINESE_MOHIST | 'mozi' | 'Mozi' | 'Mòzǐ (墨子)' | lzh | sig False
hobbes_leviathan_complete | 1651 | EUR_THEOL_CRITIC | None | 'hobbes' | None | None | eng | sig True
mozi_selections | -400 | CHINESE_RATIONALIST | None | 'mozi' | None | None | lzh | sig True
han_feizi_selections | -250 | CHINESE_LEGALIST | None | 'han_feizi' | None | None | lzh | sig True
seen labels 66
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nfor k,v in g.items():\n    if v.get('tradition_label')=='CHINESE_MODERN':\n        print(k,json.dumps(v,ensure_ascii=False)[:700]); break\nfor k,v in g … [178 caractères tronqués]`

  ```
wei_yuan_haiguo_tuzhi {"kind": "canon_work", "author": "wei_yuan", "year": 1843, "language_original": "lzh", "tradition_label": "CHINESE_MODERN", "tradition_micro": "STATECRAFT_GEOGRAPHIC_LATE_QING", "title_original": "海國圖志 / Hǎi guó tú zhì", "title_en": "Illustrated Treatise on the Maritime Kingdoms", "tags": ["statecraft_late_qing", "world_geography"], "ingestion_status": "catalog_only", "v14_signature": null}
isidore_etymologiae {"kind": "canon_work", "author": "isidore_of_seville", "year": 625, "language_original": "lat", "tradition_label": "GRECO_LATIN_MEDIEVAL", "tradition_micro": "SCHOLASTIC_PRE_THOMIST", "title_original": "Etymologiae", "title_en": "Etymologies", "tags": ["scholastic_pre", "encyclopedia"], "ingestion_status": "catalog_only", "v14_signature": null}
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nc=collections.Counter(v.get('tradition_label') for v in g.values() if v.get('year') is not None)\nfor t,n in c.most_common(): print(f\"{n: … [61 caractères tronqués]`

  ```
70 BUDDHIST_LATE_ANTIQUE
  70 BUDDHIST_MEDIEVAL
  70 CHINESE_EARLY_MODERN
  70 CHINESE_LATE_ANTIQUE
  70 CHINESE_MEDIEVAL
  70 CHINESE_MODERN
  70 GRECO_LATIN_LATE_ANTIQUE
  70 GRECO_LATIN_MEDIEVAL
  70 INDIAN_EARLY_MODERN
  70 INDIAN_LATE_ANTIQUE
  70 INDIAN_MEDIEVAL
  70 INDIAN_MODERN
  70 ISLAMIC_MEDIEVAL
  70 ISLAMIC_MODERN
  70 ORIENTALIST_TRANSLATION_MODERN
  70 WESTERN_RADICAL_CONTEMPORARY
  70 WESTERN_RADICAL_MODERN
  70 WESTERN_RATIONAL_CONTEMPORARY
  70 WESTERN_RATIONAL_MODERN
  69 WESTERN_RATIONAL_EARLY_MODERN
  65 BUDDHIST_AXIAL
  60 CHINESE_AXIAL
  52 GRECO_LATIN_AXIAL
  51 INDIAN_AXIAL
  36 None
  10 GRECO_PLATONIC
   6 ABRAHAMIC_PROPHETIC_AXIAL
   3 MODERN_WESTERN
   3 EUR_RATIONALIST_CRITIC
   3 EUR_ANTI_CHRISTIAN
   2 ANCIENT_EPICUREAN
   2 DAOISM
   2 JUDEAN_APOCALYPTIC_LATE
   2 MILLENARIAN_MODERN_PROTESTANT
   2 FRENCH_ENLIGHTENMENT
   2 EVOLUTION_NATURELLE
   1 GRECO_LAT_MATERIAL
   1 SCEPT
   1 INDIAN_MATERIAL
   1 CHINESE_MATERIAL
   1 ISLAMIC_RATIONALIST
   1 EUR_THEOL_CRITIC
   1 CHINESE_RATIONALIST
   1 CHINESE_LEGALIST
   1 EUR_MATERIALIST_ATHEIST
   1 EUR_PESSIMIST_CRITIC
   1 EUR_SCEPTICAL_EMPIRICIST
   1 AMERICAN_FREETHINKER
   1 GRECO_PRESOCRATIC
   1
… [395 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\nfor f in ['research/nipada/corpus/_cache/sources_manifest.json','research/nipada/corpus/_cache/sources_coverage.json']:\n    d=json.load(open(f)); print('==',f,type(d),len(d) if hasattr(d,'__len__') else '')\n    if isinstance(d,dict):\n   … [263 caractères tronqués]`

  ```
== research/nipada/corpus/_cache/sources_manifest.json <class 'list'> 107
{"id": "dn1_brahmajala", "lang": "eng", "url": "https://suttacentral.net/dn1/en/sujato", "title": "dn1_brahmajala"}
== research/nipada/corpus/_cache/sources_coverage.json <class 'list'> 107
{"id": "dn1_brahmajala", "ok": true, "words": 12773}
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nprint(collections.Counter(v.get('ingestion_status') for v in g.values()).most_common(20))\n# catalog nodes with url\nn=sum(1 for v in g.va … [279 caractères tronqués]`

  ```
[('catalog_only', 1641), (None, 52), ('signed_v208', 28), ('signed_v295', 22), ('signed_v272', 10)]
catalog with url 0
catalog with n_words 0
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\nm=json.load(open('research/nipada/corpus/_cache/sources_manifest.json'))\nc=json.load(open('research/nipada/corpus/_cache/sources_coverage.json'))\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))[ … [746 caractères tronqués]`

  ```
manifest 107 ok 102
unique ids 107
{'id': 'dn1_brahmajala', 'lang': 'eng', 'url': 'https://suttacentral.net/dn1/en/sujato', 'title': 'dn1_brahmajala'}
{'id': 'dn2_samannaphala', 'lang': 'eng', 'url': 'https://suttacentral.net/dn2/en/sujato', 'title': 'dn2_samannaphala'}
{'id': 'dn9_potthapada', 'lang': 'eng', 'url': 'https://suttacentral.net/dn9/en/sujato', 'title': 'dn9_potthapada'}
{'id': 'dn11_kevatta', 'lang': 'eng', 'url': 'https://suttacentral.net/dn11/en/sujato', 'title': 'dn11_kevatta'}
{'id': 'dn14_mahapadana', 'lang': 'eng', 'url': 'https://suttacentral.net/dn14/en/sujato', 'title': 'dn14_mahapadana'}
{'id': 'dn15_mahanidana', 'lang': 'eng', 'url': 'https://suttacentral.net/dn15/en/sujato', 'title': 'dn15_mahanidana'}
{'id': 'dn16_mahaparinibbana', 'lang': 'eng', 'url': 'https://suttacentral.net/dn16/en/sujato', 'title': 'dn16_mahaparinibbana'}
{'id': 'dn21_sakkapanha', 'lang': 'eng', 'url': 'https://suttacentral.net/dn21/en/sujato', 'title': 'dn21_sakkapanha'}
{'id': 'dn22_mahasatipatthana', 'lang': 'eng', 'url': 'https://suttacentral.net/dn22/en/sujato', 'title': 'dn22_mahasatipatthana'}
{'id': 'dn26_cakkavatti', 'lang': 'eng', 'url': 'https://suttacentral.net/dn26/en/s
… [6944 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, itertools, collections\nA=json.load(open('research/nipada/falsification/analytic_sigs_v1.json'))\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nsig=set(A)|{k for k,v in g.items() if v.get('v14_sign … [1698 caractères tronqués]`

  ```
union measured signatures 90
dated 82
G1 raw diff <=10 distinct author: 75 labelpairs 41
  [(('GRECO_LATIN_AXIAL', 'GRECO_PLATONIC'), 14), (('GRECO_PLATONIC', 'GRECO_LATIN_AXIAL'), 13), (('AMERICAN_FREETHINKER', 'EUR_ANTI_CHRISTIAN'), 3), (('EUR_ANTI_CHRISTIAN', 'MILLENARIAN_MODERN_PROTESTANT'), 3), (('EUR_PESSIMIST_CRITIC', 'EVOLUTION_NATURELLE'), 2), (('EVOLUTION_NATURELLE', 'MATERIALIST_MODERN'), 2), (('CHINESE_RATIONALIST', 'GRECO_PLATONIC'), 2), (('GRECO_PLATONIC', 'CONFUCIAN_AXIAL'), 2), (('ABRAHAMIC_PROPHETIC_AXIAL', 'DAOISM'), 2), (('SCEPT', 'STOIC_ROMAN'), 1), (('NEUROSEMIOTICS', 'DISTRIBUTIONAL_SEMANTICS'), 1), (('NEUROSEMIOTICS', 'NEURAL_LANGUAGE_MODELS'), 1), (('COGNITIVE_LIMITS', 'FUZZY_LOGIC'), 1), (('EUR_PESSIMIST_CRITIC', 'EUR_RATIONALIST_CRITIC'), 1), (('EUR_PESSIMIST_CRITIC', 'MODERN_WESTERN'), 1)]
G1 large diff <=10 distinct author: 31 labelpairs 15
  [(('GRECO', 'CHINESE'), 5), (('COGNITIVE_SCIENCE', 'FORMAL_LOGIC'), 3), (('AMERICAN_FREETHINKER', 'EUROPE_MODERN'), 3), (('CHINESE', 'GRECO'), 3), (('EUROPE_MODERN', 'MILLENARIAN'), 3), (('EUROPE_MODERN', 'EVOLUTION_NATURELLE'), 2), (('EVOLUTION_NATURELLE', 'EUROPE_MODERN'), 2), (('MILLENARIAN', 'EUROPE_MODERN'), 2)
… [233 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, numpy as np\nA=json.load(open('research/nipada/falsification/analytic_sigs_v1.json'))\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nov=[k for k in A if g.get(k,{}).get('v14_signature')]\nprint('ov … [465 caractères tronqués]`

  ```
overlap 11 ['bengio_2003', 'kleene_1936', 'lukasiewicz_1920', 'mikolov_2013', 'plato_gorgias_jowett', 'plato_meno_jowett', 'plato_phaedrus_jowett', 'plato_philebus_jowett', 'plato_republic_jowett', 'plato_symposium_jowett', 'plato_theaetetus_jowett']
bengio_2003 L2 0.2567867342361179 cos 0.7162975092155637 maxdiff 0.12396158284120792
kleene_1936 L2 0.31402418614770167 cos 0.625047669093723 maxdiff 0.17544963785544232
lukasiewicz_1920 L2 0.4519200655913998 cos 0.419841803556746 maxdiff 0.23459945438564817
mikolov_2013 L2 0.2742537755855091 cos 0.6460222649393835 maxdiff 0.18358945926374087
plato_gorgias_jowett L2 0.231225051658353 cos 0.7456852587597393 maxdiff 0.12414630695344608
plato_meno_jowett L2 0.1915299944569057 cos 0.8244752610679864 maxdiff 0.10371467005514048
plato_phaedrus_jowett L2 0.19370808534326361 cos 0.8221868188351152 maxdiff 0.10250301800448532
plato_philebus_jowett L2 0.1993127746810157 cos 0.8056795252570575 maxdiff 0.10491694888958833
plato_republic_jowett L2 0.20795436991716743 cos 0.7888241292487799 maxdiff 0.11002353980304551
plato_symposium_jowett L2 0.21940912433175822 cos 0.7648448567616803 maxdiff 0.12363143355078159
plato_theaetetus_jowett L2 0.2234410
… [59 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, itertools, collections\nm=json.load(open('research/nipada/corpus/_cache/sources_manifest.json'))\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nA=json.load(open('research/nipada/falsification/analy … [2422 caractères tronqués]`

  ```
sources 107 dated 106 signed 57
G1 raw diff <=10: 120
  35 ('GRECO_LATIN_AXIAL', 'GRECO_PLATONIC')
  14 ('INDIAN_AXIAL', 'GRECO_LATIN_AXIAL')
  14 ('INDIAN_AXIAL', 'GRECO_PLATONIC')
  7 ('INDIAN_AXIAL', 'CHINESE_AXIAL')
  7 ('INDIAN_AXIAL', 'BUDDHIST_AXIAL')
  6 ('CHINESE_AXIAL', 'GRECO_LATIN_AXIAL')
  5 ('CHINESE_AXIAL', 'GRECO_LAT_MATERIAL')
  5 ('DAOISM', 'CHINESE_AXIAL')
  2 ('INDIAN_AXIAL', 'ABRAHAMIC_PROPHETIC_AXIAL')
  2 ('INDIAN_AXIAL', 'DAOISM')
  2 ('INDIAN_AXIAL', 'GRECO_LAT_MATERIAL')
  1 ('CHINESE_AXIAL', 'DAOISM')
  1 ('CHINESE_AXIAL', 'GRECO_PLATONIC')
  1 ('DAOISM', 'GRECO_LAT_MATERIAL')
  1 ('GRECO_PRESOCRATIC', 'MANY_VALUED_LOGIC')
  1 ('GRECO_PRESOCRATIC', 'RECURSIVE_FUNCTIONS')
  1 ('GRECO_PRESOCRATIC', 'COMBINATORY_LOGIC')
  1 ('CHINESE_AXIAL', 'JUDEAN_APOCALYPTIC_LATE')
  1 ('CHINESE_AXIAL', 'CLASSICAL_ORACULAR')
  1 ('GRECO_LAT_MATERIAL', 'CHINESE_AXIAL')
  1 ('EUR_SCEPTICAL_EMPIRICIST', 'EUR_MATERIALIST_ATHEIST')
  1 ('AMERICAN_FREETHINKER', 'MILLENARIAN_MODERN_PROTESTANT')
  1 ('JUDEAN_APOCALYPTIC_LATE', 'CLASSICAL_ORACULAR')
  1 ('DISTRIBUTIONAL_SEMANTICS', 'NEURAL_LANGUAGE_MODELS')
  1 ('DISTRIBUTIONAL_SEMANTICS', 'NEUROSEMIOTICS')
  1 ('NEURAL_LANGUAGE_M
… [1025 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\nm=json.load(open('research/nipada/corpus/_cache/sources_manifest.json'))\nids=set(x['id'] for x in m)\nA=set(json.load(open('research/nipada/falsification/analytic_sigs_v1.json')))\ng=json.load(open('research/nipada/falsification/nipada_v3 … [408 caractères tronqués]`

  ```
ids 107 A 44 G 57
A&ids 44 G&ids 25 A&G 11
A not ids []
G not ids ['bhagavad_gita_arnold_en', 'carus_gospel_buddha_en', 'carvaka_fragments', 'confucius_analects_en', 'darwin_origin_de', 'darwin_origin_en', 'dhammapada_muller_en', 'feuerbach_christianity_en', 'feuerbach_wesen', 'great_learning_legge_en', 'han_feizi_selections', 'hobbes_leviathan_complete', 'holbach_systeme', 'hume_dialogues', 'khayyam_rubaiyat_fitzgerald_en', 'lucretius_drn_en', 'marcus_aurelius_meditations_en', 'marx_critique_political_economy_en', 'mozi_selections', 'nietzsche_antichrist'] count 32
union&ids 58
A&G&ids 11
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections\nm=json.load(open('research/nipada/corpus/_cache/sources_manifest.json'))\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nids=list(dict.fromkeys(x['id'] for x in m))\nrows=[]\nfor k in i … [426 caractères tronqués]`

  ```
-900  san INDIAN_AXIAL                 atharvaveda_samhita                    anonymous              Atharvaveda
  -750  eng ABRAHAMIC_PROPHETIC_AXIAL    hosea_book                             Hosea ben Beeri (attri Hosea (KJV)
  -700  san INDIAN_AXIAL                 brihadaranyaka_upanishad               anonymous              The Great Forest Upanishad
  -700  san INDIAN_AXIAL                 chandogya_upanishad                    anonymous              Chandogya Upanishad
  -700  eng ABRAHAMIC_PROPHETIC_AXIAL    isaiah_book                            Isaiah ben Amoz (attri Isaiah (KJV)
  -600  eng ABRAHAMIC_PROPHETIC_AXIAL    jeremiah_book                          Jeremiah ben Hilkiah ( Jeremiah (KJV)
  -590  eng ABRAHAMIC_PROPHETIC_AXIAL    ezekiel_book                           Ezekiel ben Buzi (attr Ezekiel (KJV)
  -520  eng ABRAHAMIC_PROPHETIC_AXIAL    zechariah_book                         Zechariah ben Berechia Zechariah (KJV)
  -500  san INDIAN_AXIAL                 isa_upanishad                          anonymous              Isha Upanishad
  -440  pli BUDDHIST_AXIAL               dn1_brahmajala                         anonymous_sangha       All-Embracing Net of Views
 
… [12011 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/select_proto.py <<'EOF'\nimport json, re, itertools, collections, hashlib, pathlib, random\n\nPAN = pathlib.Path('../Panini')\nM = json.load(open(PAN/'research/nipada/corpus/_cache/sources_manifest.json'))\nG = json.load(open(PAN/'research/nipada/falsification/nipada_v334_gra … [7440 caractères tronqués]`

  ```
rows 106 signed A 44
pools 69 214 270
G1 fam pairs Counter({('GRECO', 'INDIAN'): 30, ('CHINESE', 'GRECO'): 14, ('CHINESE', 'INDIAN'): 9, ('BUDDHIST', 'INDIAN'): 7, ('FORMAL_LOGIC', 'GRECO'): 3, ('COGNITIVE_SCIENCE', 'FORMAL_LOGIC'): 3, ('ABRAHAMIC', 'INDIAN'): 2, ('EUROPE_MODERN', 'MILLENARIAN'): 1})
G1 signed both 0
G2 signed both 102
G3 signed both 118
G1 selected 20 uses 33
G2 selected 17 uses 54
G3 selected 7 uses 61

== G1 20
  chandogya_upanishad               -700 INDIAN        san | isaiah_book                       -700 ABRAHAMIC     eng | d=0 sig=FalseTrue
  ingersoll_works                   1879 EUROPE_MODERN  eng | russell_parousia_1878             1878 MILLENARIAN   eng | d=1 sig=FalseTrue
  burnet_early_greek_philosophy     1930 GRECO          en | curry_1930                        1930 FORMAL_LOGIC  eng | d=0 sig=FalseTrue
  brihadaranyaka_upanishad          -700 INDIAN        san | isaiah_book                       -700 ABRAHAMIC     eng | d=0 sig=FalseTrue
  mandukya_upanishad                -300 INDIAN        san | mengzi                            -300 CHINESE       lzh | d=0 sig=FalseTrue
  brahma_sutra_badarayana           -300 INDIAN        san | qiwulun      
… [5672 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nexec(open('/tmp/select_proto.py').read().split(\"def pick\")[0])\nimport collections\nprint('G3 by lang',collections.Counter(a['lang'] for a,b in P3))\nprint('G3 eng by author',collections.Counter((a['author'],b['a … [295 caractères tronqués]`

  ```
rows 106 signed A 44
pools 69 214 270
G1 fam pairs Counter({('GRECO', 'INDIAN'): 30, ('CHINESE', 'GRECO'): 14, ('CHINESE', 'INDIAN'): 9, ('BUDDHIST', 'INDIAN'): 7, ('FORMAL_LOGIC', 'GRECO'): 3, ('COGNITIVE_SCIENCE', 'FORMAL_LOGIC'): 3, ('ABRAHAMIC', 'INDIAN'): 2, ('EUROPE_MODERN', 'MILLENARIAN'): 1})
G1 signed both 0
G2 signed both 102
G3 signed both 118
G3 by lang Counter({'eng': 230, 'grc': 26, 'san': 11, 'lzh': 3})
G3 eng by author [(('lucretius', 'anonymous'), 5), (('hume', 'anonymous'), 5), (('holbach', 'anonymous'), 5), (('ingersoll', 'anonymous'), 5), (('anonymous', 'james stuart russell'), 5), (('anonymous', 'william miller'), 5), (('anonymous', 'tom mikolov'), 5), (('anonymous', 'yoshua bengio'), 5), (('anonymous', 'george a miller'), 5), (('anonymous', 'lotfi a zadeh'), 5), (('anonymous', 'stephen c kleene'), 5), (('anonymous', 'friedemann pulverm ller'), 5), (('anonymous', 'haskell b curry'), 5), (('anonymous', 'm ross quillian'), 5), (('anonymous', 'roger c schank'), 5), (('isaiah ben amoz', 'anonymous'), 4), (('jeremiah ben hilkiah', 'anonymous'), 4), (('ezekiel ben buzi', 'anonymous'), 4), (('zechariah ben berechiah', 'anonymous'), 3), (('hosea ben beeri', 'anonymous'
… [1822 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/select_proto2.py <<'EOF'\nimport json, re, itertools, collections, random, pathlib\nPAN = pathlib.Path('../Panini')\nM = json.load(open(PAN/'research/nipada/corpus/_cache/sources_manifest.json'))\nG = json.load(open(PAN/'research/nipada/falsification/nipada_v334_graph_v35.jso … [6626 caractères tronqués]`

  ```
G1 77 signed both 1
G2 266 signed both 103
G3 326 signed both 125
NO SOLUTION
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nexec(open('/tmp/select_proto2.py').read().split(\"best=None\")[0])\nfor max_use in [2,3,4]:\n  for cap2,cap3 in [(0,0),(6,12),(10,20)]:\n    rng=random.Random(0)\n    chosen,used,pairset=greedy(['G1','G2','G3'],rng … [256 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 71
    
    ^
IndentationError: expected an indented block after 'while' statement on line 70
[exit code: 1]
  ```

- **bash** `{"command": "cat > /tmp/diag.py <<'EOF'\nexec(open('/tmp/select_proto2.py').read().split(\"best=None\")[0])\nfor max_use in [2,3,4]:\n  for cap2,cap3 in [(999,999),(6,12),(10,20)]:\n    rng=random.Random(0)\n    chosen,used,pairset=greedy(['G1','G2','G3'],rng,max_use=max_use,cap2=cap2,cap3=cap3)\n   … [272 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/diag.py", line 1, in <module>
    exec(open('/tmp/select_proto2.py').read().split("best=None")[0])
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 71
    
    ^
IndentationError: expected an indented block after 'while' statement on line 70
[exit code: 1]
  ```

- **bash** `{"command": "python3 -c \"import scipy; print(scipy.__version__); from scipy.optimize import milp; print('milp ok')\"", "description": "Check scipy milp availability"}`

  ```
1.18.1
milp ok
  ```

- **bash** `{"command": "cat > /tmp/ilp_proto.py <<'EOF'\nimport json, re, itertools, collections, pathlib\nimport numpy as np\nfrom scipy.optimize import milp, LinearConstraint, Bounds\nfrom scipy.sparse import lil_matrix\nPAN=pathlib.Path('../Panini')\nM=json.load(open(PAN/'research/nipada/corpus/_cache/sourc … [7108 caractères tronqués]`

  ```
{'G1': 77, 'G2': 266, 'G3': 326}
variables 669
max_use 2 status 0 Optimization terminated successfully. (HiGHS Status 7: Optimal)
sizes {'G1': 20, 'G2': 20, 'G3': 20}
== G1
  mandukya_upanishad                -300 INDIAN        san | qiwulun                           -300 CHINESE       lzh | d=0 sig=FalseTrue
  mandukya_upanishad                -300 INDIAN        san | zhongyong                         -300 CHINESE       lzh | d=0 sig=FalseFalse
  brahma_sutra_badarayana           -300 INDIAN        san | qiwulun                           -300 CHINESE       lzh | d=0 sig=FalseTrue
  brahma_sutra_badarayana           -300 INDIAN        san | mengzi                            -300 CHINESE       lzh | d=0 sig=FalseTrue
  baudhayana_dharmasutra            -400 INDIAN        san | plato_crito                       -399 GRECO         grc | d=1 sig=FalseFalse
  baudhayana_dharmasutra            -400 INDIAN        san | plato_crito_jowett                -399 GRECO         grc | d=1 sig=FalseFalse
  hiranyakesi_grhya_sutra           -400 INDIAN        san | plato_charmides                   -390 GRECO         grc | d=10 sig=FalseTrue
  hiranyakesi_grhya_sutra           -400 INDIAN        sa
… [7562 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/quota_proto.py <<'EOF'\nimport json, re, itertools, collections, pathlib\nPAN=pathlib.Path('../Panini')\nM=json.load(open(PAN/'research/nipada/corpus/_cache/sources_manifest.json'))\nG=json.load(open(PAN/'research/nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nA … [6213 caractères tronqués]`

  ```
pools 77 266 430
G1 family pairs Counter({('GRECO', 'INDIAN'): 30, ('CHINESE', 'INDIAN'): 14, ('CHINESE', 'GRECO'): 14, ('BUDDHIST', 'INDIAN'): 7, ('FORMAL_LOGIC', 'GRECO'): 3, ('COGNITIVE_SCIENCE', 'FORMAL_LOGIC'): 3, ('ABRAHAMIC', 'INDIAN'): 2, ('ABRAHAMIC', 'CHINESE'): 1, ('CHINESE', 'CLASSICAL_ORACULAR'): 1, ('EUROPE_MODERN', 'MILLENARIAN'): 1, ('ABRAHAMIC', 'CLASSICAL_ORACULAR'): 1})
G2 families Counter({'GRECO': 173, 'BUDDHIST': 27, 'INDIAN': 27, 'CHINESE': 15, 'ABRAHAMIC': 9, 'COGNITIVE_SCIENCE': 9, 'FORMAL_LOGIC': 3, 'EUROPE_MODERN': 2, 'MILLENARIAN': 1})
G3 langs Counter({'eng': 264, 'grc': 96, 'san': 55, 'lzh': 15})
selected 20 18 17

== G1 20
  vasistha_dharmasutra              -400 INDIAN        san | plato_charmides                   -390 GRECO         grc | d=10 sig=FalseTrue
  sankhayana_grhya_sutra            -400 INDIAN        san | plato_charmides                   -390 GRECO         grc | d=10 sig=FalseTrue
  paraskara_grhya_sutra             -400 INDIAN        san | plato_charmides                   -390 GRECO         grc | d=10 sig=FalseTrue
  hiranyakesi_grhya_sutra           -400 INDIAN        san | plato_charmides                   -390 GRECO         grc | d
… [7388 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/ilp_proto2.py <<'EOF'\nimport json, re, itertools, collections, pathlib\nimport numpy as np\nfrom scipy.optimize import milp, LinearConstraint, Bounds\nfrom scipy.sparse import lil_matrix\nPAN=pathlib.Path('../Panini')\nM=json.load(open(PAN/'research/nipada/corpus/_cache/sour … [7394 caractères tronqués]`

  ```
{'G1': 77, 'G2': 266, 'G3': 430}
status 2 The problem is infeasible. (HiGHS Status 8: model_status is Infeasible; primal_status is None)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\n# modify the prototype file text and run variants by string replacement\nsrc=open('/tmp/ilp_proto2.py').read()\nfor g1use in [1,2]:\n  for g2cap in [4,5,6]:\n    for g3cap in [5,6,8]:\n      s=src.replace(\"add(0,1 … [694 caractères tronqués]`

  ```
1 4 5 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
1 4 6 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
1 4 8 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
1 5 5 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
1 5 6 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
1 5 8 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
1 6 5 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
1 6 6 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
1 6 8 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
2 4 5 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
2 4 6 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
2 4 8 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
2 5 5 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
2 5 6 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
2 5 8 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
2 6 5 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
2 6 6 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
2 6 8 infeasible {'G1': 77, 'G2': 266, 'G3': 430}
  ```

- **bash** `{"command": "cat > /tmp/final_list.py <<'EOF'\nG1 = [\n ('baudhayana_dharmasutra','plato_crito'),\n ('vasistha_dharmasutra','plato_euthyphro_jowett'),\n ('hiranyakesi_grhya_sutra','plato_charmides'),\n ('paraskara_grhya_sutra','plato_crito'),\n ('apastamba_grhya_sutra','plato_euthyphro_jowett'),\n ( … [6407 caractères tronqués]`

  ```
== G1 20
baudhayana_dharmasutra            -400 INDIAN        san | plato_crito                       -399 GRECO         grc | d=1 fam=!= lang=!= src=True sig=FalseFalse
vasistha_dharmasutra              -400 INDIAN        san | plato_euthyphro_jowett            -399 GRECO         grc | d=1 fam=!= lang=!= src=True sig=FalseFalse
hiranyakesi_grhya_sutra           -400 INDIAN        san | plato_charmides                   -390 GRECO         grc | d=10 fam=!= lang=!= src=True sig=FalseTrue
paraskara_grhya_sutra             -400 INDIAN        san | plato_crito                       -399 GRECO         grc | d=1 fam=!= lang=!= src=True sig=FalseFalse
apastamba_grhya_sutra             -400 INDIAN        san | plato_euthyphro_jowett            -399 GRECO         grc | d=1 fam=!= lang=!= src=True sig=FalseFalse
sankhayana_grhya_sutra            -400 INDIAN        san | plato_charmides                   -390 GRECO         grc | d=10 fam=!= lang=!= src=True sig=FalseTrue
daodejing                         -350 CHINESE       lzh | plato_laws                        -350 GRECO         grc | d=0 fam=!= lang=!= src=True sig=FalseTrue
daodejing                         -350 CHINESE       lzh | plato_
… [8804 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re\nsrc=open('/tmp/final_list.py').read()\nsrc=src.replace(\" ('mn35_culasaccaka','an7_64_kodhana'),\\n\",\" ('isaiah_book','ezekiel_book'),\\n\")\nsrc=src.replace(\" ('plato_phaedo','aristotle_parts_of_anim … [4141 caractères tronqués]`

  ```
== G1 20
baudhayana_dharmasutra            -400 INDIAN        san | plato_crito                       -399 GRECO         grc | d=1 fam=!= lang=!= sig=FalseFalse
vasistha_dharmasutra              -400 INDIAN        san | plato_euthyphro_jowett            -399 GRECO         grc | d=1 fam=!= lang=!= sig=FalseFalse
hiranyakesi_grhya_sutra           -400 INDIAN        san | plato_charmides                   -390 GRECO         grc | d=10 fam=!= lang=!= sig=FalseTrue
paraskara_grhya_sutra             -400 INDIAN        san | plato_crito                       -399 GRECO         grc | d=1 fam=!= lang=!= sig=FalseFalse
apastamba_grhya_sutra             -400 INDIAN        san | plato_euthyphro_jowett            -399 GRECO         grc | d=1 fam=!= lang=!= sig=FalseFalse
sankhayana_grhya_sutra            -400 INDIAN        san | plato_charmides                   -390 GRECO         grc | d=10 fam=!= lang=!= sig=FalseTrue
daodejing                         -350 CHINESE       lzh | plato_laws                        -350 GRECO         grc | d=0 fam=!= lang=!= sig=FalseTrue
daodejing                         -350 CHINESE       lzh | plato_sophist                     -360 GRECO         grc | d=10 fam=!
… [8417 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nsrc=open('/tmp/final_list2.py').read()\nsrc=src.replace(\" ('plato_republic_jowett','aristotle_parts_of_animals'),\\n\",\" ('plato_symposium_jowett','aristotle_de_anima'),\\n\",1)\n# The replacement above may hit G … [193 caractères tronqués]`

  ```
G2 last 3: [('daodejing', 'liji'), ('dn1_brahmajala', 'an7_64_kodhana'), ('isaiah_book', 'ezekiel_book')]
G3: [('sextus_pyrrho', 'plato_republic_jowett'), ('sextus_pyrrho', 'plato_phaedo'), ('sextus_pyrrho', 'plato_gorgias_jowett'), ('plato_gorgias', 'aristotle_de_anima'), ('plato_republic_jowett', 'aristotle_parts_of_animals')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nsrc=open('/tmp/final_list3.py').read()\n# Replace the G3 occurrence (the one after sextus/plato_gorgias_jowett)\nold=\" ('sextus_pyrrho','plato_gorgias_jowett'),\\n ('plato_republic_jowett','aristotle_parts_of_anim … [317 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
AssertionError
[exit code: 1]
  ```

- **bash** `{"command": "grep -n \"sextus\\|plato_republic\\|plato_symposium\\|aristotle_de_anima\\|aristotle_parts\" /tmp/final_list3.py", "description": "Inspect list occurrences"}`

  ```
26: ('plato_symposium_jowett','aristotle_de_anima'),
27: ('plato_symposium_jowett','aristotle_categories'),
28: ('plato_republic_jowett','aristotle_nicomachean_ethics'),
29: ('plato_laws','aristotle_de_anima'),
58: ('sextus_pyrrho','plato_republic_jowett'),  # need id? 
59: ('sextus_pyrrho','plato_phaedo'),
60: ('sextus_pyrrho','plato_gorgias_jowett'),
61: ('plato_gorgias','aristotle_de_anima'),
62: ('plato_republic_jowett','aristotle_parts_of_animals'),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nlines=open('/tmp/final_list3.py').read().splitlines()\n# line numbers 1-based\nlines[25]=\" ('plato_republic_jowett','aristotle_parts_of_animals'),\"\nlines[61]=\" ('plato_symposium_jowett','aristotle_de_anima'),\" … [195 caractères tronqués]`

  ```
G2 ('plato_republic_jowett', 'aristotle_parts_of_animals') ('plato_symposium_jowett', 'aristotle_categories') ('plato_laws', 'aristotle_de_anima')
G3 greek [('sextus_pyrrho', 'plato_republic_jowett'), ('sextus_pyrrho', 'plato_phaedo'), ('sextus_pyrrho', 'plato_gorgias_jowett'), ('plato_gorgias', 'aristotle_de_anima'), ('plato_symposium_jowett', 'aristotle_de_anima')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nexec(open('/tmp/final_list4.py').read())\nimport json,re,collections,pathlib\nPAN=pathlib.Path('../Panini')\nM=json.load(open(PAN/'research/nipada/corpus/_cache/sources_manifest.json'))\nG=json.load(open(PAN/'resea … [3713 caractères tronqués]`

  ```
total 60 unique 60 dups []
n texts 61 max [('isaiah_book', 5), ('daodejing', 4), ('an7_64_kodhana', 4), ('brihadaranyaka_upanishad', 4), ('book_of_enoch', 4), ('yueji', 4), ('baudhayana_dharmasutra', 3), ('plato_charmides', 3), ('plato_gorgias', 3), ('plato_republic_jowett', 3), ('aristotle_de_anima', 3), ('daniel_book', 3)]
G3 langs Counter({'eng': 12, 'grc': 5, 'san': 2, 'lzh': 1})
G3 cross-family 12
signed pairs G1/G2/G3 [0, 11, 10]
one-signed G1 12
G1 family pairs Counter({('GRECO', 'INDIAN'): 7, ('CHINESE', 'GRECO'): 4, ('CHINESE', 'INDIAN'): 3, ('BUDDHIST', 'INDIAN'): 3, ('ABRAHAMIC', 'INDIAN'): 2, ('ABRAHAMIC', 'CHINESE'): 1})
G2 families Counter({'GRECO': 7, 'ABRAHAMIC': 5, 'INDIAN': 4, 'CHINESE': 3, 'BUDDHIST': 1})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nlines=open('/tmp/final_list4.py').read().splitlines()\n# replace last G1 line (line 21? find asvalayana)\nfor i,l in enumerate(lines):\n    if 'asvalayana_grhya_sutra' in l:\n        lines[i]=\" ('book_of_enoch','s … [208 caractères tronqués]`

  ```
('book_of_enoch', 'sibylline_oracles')
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nexec(open('/tmp/final_list5.py').read())\nimport json,re,collections,pathlib\nPAN=pathlib.Path('../Panini')\nM=json.load(open(PAN/'research/nipada/corpus/_cache/sources_manifest.json'))\nG=json.load(open(PAN/'resea … [3716 caractères tronqués]`

  ```
total 60 unique 60 dups []
n texts 60 max [('isaiah_book', 5), ('book_of_enoch', 5), ('daodejing', 4), ('an7_64_kodhana', 4), ('brihadaranyaka_upanishad', 4), ('yueji', 4), ('baudhayana_dharmasutra', 3), ('sibylline_oracles', 3), ('plato_gorgias', 3), ('plato_republic_jowett', 3), ('aristotle_de_anima', 3), ('daniel_book', 3)]
G3 langs Counter({'eng': 12, 'grc': 5, 'san': 2, 'lzh': 1})
G3 cross-family 12
signed pairs G1/G2/G3 [1, 11, 10]
one-signed G1 12
G1 family pairs Counter({('GRECO', 'INDIAN'): 6, ('CHINESE', 'GRECO'): 4, ('CHINESE', 'INDIAN'): 3, ('BUDDHIST', 'INDIAN'): 3, ('ABRAHAMIC', 'INDIAN'): 2, ('ABRAHAMIC', 'CHINESE'): 1, ('ABRAHAMIC', 'CLASSICAL_ORACULAR'): 1})
G2 families Counter({'GRECO': 7, 'ABRAHAMIC': 5, 'INDIAN': 4, 'CHINESE': 3, 'BUDDHIST': 1})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nexec(open('/tmp/final_list5.py').read())\nimport json,collections,pathlib\nPAN=pathlib.Path('../Panini')\nM=json.load(open(PAN/'research/nipada/corpus/_cache/sources_manifest.json'))\nC={x['id']:x for x in json.loa … [872 caractères tronqués]`

  ```
texts 60 in sources 60
signed texts 34 unsigned 26
unsigned: ['an7_64_kodhana', 'apastamba_grhya_sutra', 'aristotle_de_anima', 'atharvaveda_samhita', 'baudhayana_dharmasutra', 'brahma_sutra_badarayana', 'brihadaranyaka_upanishad', 'chandogya_upanishad', 'daodejing', 'epicurus_letters', 'hiranyakesi_grhya_sutra', 'holbach_systeme_en', 'hume_dialogues_nhr', 'isa_upanishad', 'liji', 'lucretius_drn', 'mandukya_upanishad', 'paraskara_grhya_sutra', 'plato_crito', 'plato_euthyphro_jowett', 'sankhayana_grhya_sutra', 'sextus_pyrrho', 'vasistha_dharmasutra', 'xiaojing', 'yueji', 'zhuangzi']
not ok: [('aristotle_de_anima', False), ('atharvaveda_samhita', False), ('an7_64_kodhana', False), ('brahma_sutra_badarayana', False)]
no coverage: []
G1 both 1 one 11 none 8
G2 both 11 one 2 none 7
G3 both 10 one 6 none 4
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json\nC=json.load(open('research/nipada/corpus/_cache/sources_coverage.json'))\nbad=[x['id'] for x in C if not x.get('ok')]\nprint('bad',bad)\ngood=[x['id'] for x in C if x.get('ok')]\nprint('good',len(good))\nEOF", "description": "List non-acqu … [14 caractères tronqués]`

  ```
bad ['brahma_sutra_badarayana', 'atharvaveda_samhita', 'an7_64_kodhana', 'aristotle_de_anima', 'plato_republic_fr']
good 102
  ```

- **bash** `{"command": "cat > /tmp/final_list6.py <<'EOF'\nG1 = [\n ('baudhayana_dharmasutra','plato_crito'),\n ('vasistha_dharmasutra','plato_euthyphro_jowett'),\n ('hiranyakesi_grhya_sutra','plato_charmides'),\n ('paraskara_grhya_sutra','plato_crito'),\n ('apastamba_grhya_sutra','plato_euthyphro_jowett'),\n  … [6431 caractères tronqués]`

  ```
total 60 unique 60 dups []
n texts 59 max [('isaiah_book', 5), ('book_of_enoch', 5), ('daodejing', 4), ('mandukya_upanishad', 4), ('yueji', 4), ('baudhayana_dharmasutra', 3), ('curry_1930', 3), ('chandogya_upanishad', 3), ('brihadaranyaka_upanishad', 3), ('sibylline_oracles', 3), ('plato_gorgias', 3), ('aristotle_de_caelo', 3)]
bad sources []
signed pairs G1/G2/G3 [1, 14, 12]
one-signed G1 14
G1 family pairs Counter({('GRECO', 'INDIAN'): 6, ('CHINESE', 'GRECO'): 4, ('CHINESE', 'INDIAN'): 3, ('ABRAHAMIC', 'INDIAN'): 2, ('FORMAL_LOGIC', 'GRECO'): 1, ('COGNITIVE_SCIENCE', 'FORMAL_LOGIC'): 1, ('EUROPE_MODERN', 'MILLENARIAN'): 1, ('ABRAHAMIC', 'CHINESE'): 1, ('ABRAHAMIC', 'CLASSICAL_ORACULAR'): 1})
G2 families Counter({'GRECO': 8, 'ABRAHAMIC': 6, 'INDIAN': 3, 'CHINESE': 3})
G3 langs Counter({'eng': 12, 'grc': 5, 'san': 2, 'lzh': 1})
G3 cross-family 12
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nexec(open('/tmp/final_list6.py').read())\nimport json,re,collections,pathlib,numpy as np\nPAN=pathlib.Path('../Panini')\nM=json.load(open(PAN/'research/nipada/corpus/_cache/sources_manifest.json'))\nC={x['id']:x fo … [5657 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 38, in <module>
  File "<stdin>", line 31, in pool
  File "<stdin>", line 24, in base_ok
KeyError: 'work'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nexec(open('/tmp/final_list6.py').read())\nimport json,re,collections,pathlib,numpy as np,itertools\nPAN=pathlib.Path('../Panini')\nM=json.load(open(PAN/'research/nipada/corpus/_cache/sources_manifest.json'))\nC={x[ … [5629 caractères tronqués]`

  ```
sources 107 ok 102 dated 106 signed A 44
G1 77 both 1 one 30 none 46
 G1 fam pairs Counter({('GRECO', 'INDIAN'): 30, ('CHINESE', 'INDIAN'): 14, ('CHINESE', 'GRECO'): 14, ('BUDDHIST', 'INDIAN'): 7, ('FORMAL_LOGIC', 'GRECO'): 3, ('COGNITIVE_SCIENCE', 'FORMAL_LOGIC'): 3, ('ABRAHAMIC', 'INDIAN'): 2, ('ABRAHAMIC', 'CHINESE'): 1, ('CHINESE', 'CLASSICAL_ORACULAR'): 1, ('EUROPE_MODERN', 'MILLENARIAN'): 1, ('ABRAHAMIC', 'CLASSICAL_ORACULAR'): 1})
G2 266 both 103 one 85 none 78
 G2 fams Counter({'GRECO': 173, 'BUDDHIST': 27, 'INDIAN': 27, 'CHINESE': 15, 'ABRAHAMIC': 9, 'COGNITIVE_SCIENCE': 9, 'FORMAL_LOGIC': 3, 'EUROPE_MODERN': 2, 'MILLENARIAN': 1})
G3 430 both 157 one 173 none 100
 G3 langs Counter({'eng': 264, 'grc': 96, 'san': 55, 'lzh': 15})
manifest texts 59 signed 33 unsigned 26
max use [('isaiah_book', 5), ('book_of_enoch', 5), ('daodejing', 4), ('mandukya_upanishad', 4), ('yueji', 4), ('baudhayana_dharmasutra', 3), ('curry_1930', 3), ('chandogya_upanishad', 3), ('brihadaranyaka_upanishad', 3), ('sibylline_oracles', 3), ('plato_gorgias', 3), ('aristotle_de_caelo', 3), ('plato_republic_jowett', 3), ('aristotle_parts_of_animals', 3), ('zechariah_book', 3)]
bad []
both pairs [1, 14, 12]

… [267 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, heapq, math, statistics\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))\nnodes=g['nodes']; edges=g['edges']\nP=json.load(open('research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\n# build adjacenc … [1506 caractères tronqués]`

  ```
pairs with graph 655
1/w n 200 r 0.48 sample [(3.6, 2.1052631578947367), (3.6, 2.1052631578947367), (5.84, 48.55263157894737)]
-logw n 200 r 0.428 sample [(3.6, 0.10258658877510116), (3.6, 0.10258658877510116), (5.84, 6.959048573369687)]
1-w n 200 r 0.595 sample [(3.6, 0.10000000000000009), (3.6, 0.10000000000000009), (5.84, 2.55)]
unweighted n 200 r 0.973 sample [(3.6, 2.0), (3.6, 2.0), (5.84, 9.0)]
  ```

- **bash** `{"command": "date -Iseconds; git -C ../Panini rev-parse HEAD; git -C ../Panini status --short | head -5", "description": "Check date and Panini commit"}`

  ```
2026-11-15T02:58:29-05:00
9b80c323629be60c68696f5c5a21f37ad9420073
 M .github/copilot-instructions.md
 M docs/index.md
 m modules/core/filesystem
 m modules/core/knowledge
 m modules/core/semantic
  ```

- **bash** `{"command": "cd ../Panini && sha256sum research/nipada/falsification/pairs334_axes_v1.json research/nipada/falsification/nipada_v334_graph_v35.json research/nipada/falsification/analytic_sigs_v1.json research/nipada/falsification/nipada_v334_revalidation_v35.json research/nipada/corpus/_cache/source … [167 caractères tronqués]`

  ```
8de7a6797d5316293bd29c3e5ac070d2ef5582acdeb96b286397237540528777  research/nipada/falsification/pairs334_axes_v1.json
9ddf050aa1699a3c345c6b9e8ad973b8096d6003219b069dd6a6f51489793cfe  research/nipada/falsification/nipada_v334_graph_v35.json
8aa9c1d50d89e4dc13a8b9bdbf0ae77d4e5a6da4bed00ecd126284f0f7a5519e  research/nipada/falsification/analytic_sigs_v1.json
b2be71436a017b7881fee7f93d26bedd948a7c342166236c8314d1f278abb546  research/nipada/falsification/nipada_v334_revalidation_v35.json
5d06443de6aed73370ba209faacc25a48859b07741fdbe680f0db5914d23f5dd  research/nipada/corpus/_cache/sources_coverage.json
5eda052cadf361a94d0089ea2644c468f9ba62cc70eb81dfa61a74846adb1a1e  research/nipada/corpus/_cache/sources_manifest.json
353168c2fd3846c9238168628ecf9c2956ef519b4589195b035a714bb3a80b9d  research/nipada/falsification/nipada_v150_validation.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/panini-334.json'))\nprint(json.dumps(d['sources'],indent=1)[:2000])\nEOF", "description": "Read recorded hashes from 4A"}`

  ```
{
 "paires": {
  "chemin": "Panini/research/nipada/falsification/pairs334_axes_v1.json",
  "sha256": "8de7a6797d5316293bd29c3e5ac070d2ef5582acdeb96b286397237540528777"
 },
 "graphe": {
  "chemin": "Panini/research/nipada/falsification/nipada_v334_graph_v35.json",
  "sha256": "9ddf050aa1699a3c345c6b9e8ad973b8096d6003219b069dd6a6f51489793cfe"
 },
 "signatures": {
  "chemin": "Panini/research/nipada/falsification/analytic_sigs_v1.json",
  "sha256": "8aa9c1d50d89e4dc13a8b9bdbf0ae77d4e5a6da4bed00ecd126284f0f7a5519e"
 },
 "revalidation": {
  "chemin": "Panini/research/nipada/falsification/nipada_v334_revalidation_v35.json",
  "sha256": "b2be71436a017b7881fee7f93d26bedd948a7c342166236c8314d1f278abb546"
 },
 "couverture": {
  "chemin": "Panini/research/nipada/corpus/_cache/sources_coverage.json",
  "sha256": "5d06443de6aed73370ba209faacc25a48859b07741fdbe680f0db5914d23f5dd"
 },
 "manifeste": {
  "chemin": "Panini/research/nipada/corpus/_cache/sources_manifest.json",
  "sha256": "5eda052cadf361a94d0089ea2644c468f9ba62cc70eb81dfa61a74846adb1a1e"
 },
 "v150": {
  "chemin": "Panini/research/nipada/falsification/nipada_v150_validation.json",
  "sha256": "353168c2fd3846c9238168628ecf9c2956ef519b
… [153 caractères tronqués]
  ```

- **bash** `{"command": "cat > tools/protocole_date.py <<'PYEOF'\n#!/usr/bin/env python3\n\"\"\"protocole_date.py — B1 : le protocole Panini à date contrôlée (suite de la note 4A).\n\nCe script ne modifie jamais Panini. Il lit les artefacts §334 en lecture seule,\nvérifie leurs SHA-256, construit le manifeste d … [45285 caractères tronqués]`

  ```
compiled
  ```

- **bash** `{"command": "python3 tools/protocole_date.py --construire --sortie reports/protocole-date.json", "description": "Build protocol manifest JSON"}`

  ```
OK : 60 paires uniques, 20/20/20, 59 textes, sources acquises.
manifeste écrit : reports/protocole-date.json
  ```

- **bash** `{"command": "python3 tools/protocole_date.py --verifier; echo \"---\"; python3 - <<'EOF'\nimport json\nd=json.load(open('reports/protocole-date.json'))\nprint(list(d))\nprint('paires',len(d['paires']))\nprint('pools',json.dumps(d['faisabilite']['pools'],ensure_ascii=False,indent=1)[:2500])\nprint('c … [250 caractères tronqués]`

  ```
OK : 60 paires uniques, 20/20/20, 59 textes, sources acquises.
commit Drave : f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888
commit Panini lu : 9b80c323629be60c68696f5c5a21f37ad9420073
paires : 60 ; textes : 59 ; à signer : 26
---
['tache', 'version', 'titre', 'date', 'commit_drave', 'commit_panini', 'sources', 'protocole', 'pre_enregistrement', 'faisabilite', 'composition', 'paires', 'textes', 'a_signer', 'commande', 'limites']
paires 60
pools {
 "G1": {
  "critere": "|Δannée| ≤ 10 et familles larges différentes",
  "candidats": 77,
  "deux_signatures_44": 1,
  "une_signature_44": 30,
  "aucune_signature_44": 46,
  "paires_de_familles": {
   "ABRAHAMIC–INDIAN": 2,
   "CHINESE–INDIAN": 14,
   "GRECO–INDIAN": 30,
   "BUDDHIST–INDIAN": 7,
   "CHINESE–GRECO": 14,
   "FORMAL_LOGIC–GRECO": 3,
   "ABRAHAMIC–CHINESE": 1,
   "CHINESE–CLASSICAL_ORACULAR": 1,
   "EUROPE_MODERN–MILLENARIAN": 1,
   "ABRAHAMIC–CLASSICAL_ORACULAR": 1,
   "COGNITIVE_SCIENCE–FORMAL_LOGIC": 3
  }
 },
 "G2": {
  "critere": "20 ≤ |Δannée| ≤ 200 et même famille large",
  "candidats": 266,
  "deux_signatures_44": 103,
  "une_signature_44": 85,
  "aucune_signature_44": 78,
  "familles": {
   "BUDDHIST": 27,
   "INDIAN": 27,
 
… [3693 caractères tronqués]
  ```

- **bash** `{"command": "wc -c reports/protocole-date.json; head -c 1200 reports/protocole-date.json", "description": "Check JSON size and header"}`

  ```
79858 reports/protocole-date.json
{
 "tache": "B1",
 "version": "1.0",
 "titre": "Protocole Panini à date contrôlée — 60 paires en trois groupes",
 "date": "2026-11-15",
 "commit_drave": "f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888",
 "commit_panini": {
  "attendu_4a": "e10d695e65f52031222819cb1bdbb290d08f8e57",
  "lu": "9b80c323629be60c68696f5c5a21f37ad9420073",
  "identique": false,
  "note": "Le HEAD de Panini peut avancer ; les SHA-256 des artefacts §334 sont la référence."
 },
 "sources": {
  "paires334": {
   "chemin": "Panini/research/nipada/falsification/pairs334_axes_v1.json",
   "sha256": "8de7a6797d5316293bd29c3e5ac070d2ef5582acdeb96b286397237540528777"
  },
  "graphe334": {
   "chemin": "Panini/research/nipada/falsification/nipada_v334_graph_v35.json",
   "sha256": "9ddf050aa1699a3c345c6b9e8ad973b8096d6003219b069dd6a6f51489793cfe"
  },
  "signatures44": {
   "chemin": "Panini/research/nipada/falsification/analytic_sigs_v1.json",
   "sha256": "8aa9c1d50d89e4dc13a8b9bdbf0ae77d4e5a6da4bed00ecd126284f0f7a5519e"
  },
  "revalidation334": {
   "chemin": "Panini/research/nipada/falsification/nipada_v334_revalidation_v35.json",
   "sha256": "b2be71436a017b7881fee7f93d26bedd948a7c3
… [26 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/protocole-date.json'))\nfor g in ['G1','G2','G3']:\n    print(f'\\n### {g}\\n')\n    print('| # | paire A × B | années | familles | langues | sig. |')\n    print('|---:|---|---:|---|---|---:|')\n    for p in [x for x in d['paires … [318 caractères tronqués]`

  ```
### G1

| # | paire A × B | années | familles | langues | sig. |
|---:|---|---:|---|---|---:|
| 01 | `baudhayana_dharmasutra` × `plato_crito` | -400 / -399 (Δ1) | INDIAN / GRECO | san / grc | 0 |
| 02 | `vasistha_dharmasutra` × `plato_euthyphro_jowett` | -400 / -399 (Δ1) | INDIAN / GRECO | san / grc | 0 |
| 03 | `hiranyakesi_grhya_sutra` × `plato_charmides` | -400 / -390 (Δ10) | INDIAN / GRECO | san / grc | 1 |
| 04 | `paraskara_grhya_sutra` × `plato_crito` | -400 / -399 (Δ1) | INDIAN / GRECO | san / grc | 0 |
| 05 | `apastamba_grhya_sutra` × `plato_euthyphro_jowett` | -400 / -399 (Δ1) | INDIAN / GRECO | san / grc | 0 |
| 06 | `sankhayana_grhya_sutra` × `plato_charmides` | -400 / -390 (Δ10) | INDIAN / GRECO | san / grc | 1 |
| 07 | `daodejing` × `plato_laws` | -350 / -350 (Δ0) | CHINESE / GRECO | lzh / grc | 1 |
| 08 | `daodejing` × `plato_sophist` | -350 / -360 (Δ10) | CHINESE / GRECO | lzh / grc | 1 |
| 09 | `qiwulun` × `epicurus_letters` | -300 / -300 (Δ0) | CHINESE / GRECO | lzh / grc | 1 |
| 10 | `mengzi` × `epicurus_letters` | -300 / -300 (Δ0) | CHINESE / GRECO | lzh / grc | 1 |
| 11 | `mandukya_upanishad` × `qiwulun` | -300 / -300 (Δ0) | INDIAN / CHINESE | san / lzh | 1 |
| 
… [5367 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def rejouer\\|def main\\|args.rejouer\\|args.sortie\\|G1_controle_positif\\|def _verdict\" tools/protocole_date.py", "description": "Locate replay and CLI sections"}`

  ```
825:def rejouer(manifeste: dict, signatures_path, rapide=False, sortie=None):
859:            resume["tests"]["G1_controle_positif"] = {
909:def _verdict(p1, p2):
929:def main(argv=None):
959:        sortie = pathlib.Path(args.sortie) if args.sortie else SORTIE_DEFAUT
967:    if args.rejouer:
970:        manifeste = lire_json(pathlib.Path(args.sortie) if args.sortie and pathlib.Path(args.sortie).exists() else SORTIE_DEFAUT)
974:        rejouer(manifeste, args.signatures, rapide=args.rapide, sortie=args.sortie)
  ```

- **bash** `{"command": "sed -n '790,990p' tools/protocole_date.py", "description": "View replay function and CLI"}`

  ```
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return beta, r2


def _pente(y, x):
    import numpy as np
    y = np.asarray(y, float); x = np.asarray(x, float)
    if len(y) < 3 or np.std(x) == 0:
        return 0.0, 0.0
    beta, r2 = _ols(y, x)
    return float(beta[1]), float(r2)


def _permutation_p(y, x, n=2000, graine=GRAINE, bilaterale=True):
    import numpy as np
    rng = np.random.default_rng(graine)
    obs, _ = _pente(y, x)
    xs = np.asarray(x, float)
    cnt = 0
    for _ in range(n):
        rng.shuffle(xs)
        b, _ = _pente(y, xs)
        if bilaterale:
            if abs(b) >= abs(obs) - 1e-12:
                cnt += 1
        else:
            if b >= obs - 1e-12:
                cnt += 1
    return (cnt + 1) / (n + 1), obs


def rejouer(manifeste: dict, signatures_path, rapide=False, sortie=None):
    corpus = Corpus()
    sigs = _lire_signatures(pathlib.Path(signatures_path))
    n_perm = 300 if rapide else int(manifeste["protocole"]["inference"]["permutations"])
    paires = manifeste["pai
… [7336 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\np='tools/protocole_date.py'\ns=open(p).read()\n\n# 1) add verifier_hashes after verifier function\nmarker=\"\\n\\n# ---------------------------------------------------------------------------\\n# Rejeu\\n# --------------------------------------------------- … [7529 caractères tronqués]`

  ```
patched
compiled
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='tools/protocole_date.py'\ns=open(p).read()\nstart=s.index('def _g1_controle(')\nend=s.index('def _lire_signatures(')\nnew='''def _g1_controle(g1, sigs, n_perm=2000):\n    \"\"\"Contrôle positif : les paires inter-familles doivent être plus loin que le nul.\n\n    L … [1519 caractères tronqués]`

  ```
patched
compiled
  ```

- **bash** `{"command": "sed -n '825,930p' tools/protocole_date.py", "description": "View current replay function"}`

  ```
return math.sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))


def _ols(y, X):
    """Moindres carrés avec intercept ; renvoie beta, r2."""
    import numpy as np
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    X = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return beta, r2


def _pente(y, x):
    import numpy as np
    y = np.asarray(y, float); x = np.asarray(x, float)
    if len(y) < 3 or np.std(x) == 0:
        return 0.0, 0.0
    beta, r2 = _ols(y, x)
    return float(beta[1]), float(r2)


def _permutation_p(y, x, n=2000, graine=GRAINE, bilaterale=True):
    import numpy as np
    rng = np.random.default_rng(graine)
    obs, _ = _pente(y, x)
    xs = np.asarray(x, float)
    cnt = 0
    for _ in range(n):
        rng.shuffle(xs)
        b, _ = _pente(y, xs)
        if bilaterale:
            if abs(b) >= abs(obs) - 1e-12:
                cnt += 1
        else:
            if b >= obs - 1e-12:
                cnt += 1
    return (cnt + 1) / (n + 1
… [2959 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='tools/protocole_date.py'\ns=open(p).read()\nstart=s.index('    if not lignes:\\n        resume[\"message\"]')\nend=s.index('    if sortie:\\n        chemin = pathlib.Path(sortie).resolve()')\nnew='''    if not lignes:\n        resume[\"message\"] = \"Aucune paire c … [2547 caractères tronqués]`

  ```
patched
compiled
  ```

- **bash** `{"command": "python3 tools/protocole_date.py --rejouer --signatures ../Panini/research/nipada/falsification/analytic_sigs_v1.json --sortie /tmp/protocole-resultats.json; echo \"---\"; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/protocole-resultats.json'))\nprint(json.dumps(d,ensure_ascii= … [88 caractères tronqués]`

  ```
résultats écrits : /tmp/protocole-resultats.json
---
{
 "statut": "incomplet",
 "n_paires": 27,
 "n_manquantes": 33,
 "paires_manquantes": [
  "G1-01",
  "G1-02",
  "G1-03",
  "G1-04",
  "G1-05",
  "G1-06",
  "G1-07",
  "G1-08",
  "G1-09",
  "G1-10",
  "G1-11",
  "G1-12",
  "G1-13",
  "G1-14",
  "G1-15",
  "G1-16",
  "G1-17",
  "G1-18",
  "G1-19",
  "G2-15",
  "G2-16",
  "G2-17",
  "G2-18",
  "G2-19",
  "G2-20",
  "G3-06",
  "G3-07",
  "G3-13",
  "G3-14",
  "G3-15",
  "G3-18",
  "G3-19",
  "G3-20"
 ],
 "n_permutations": 2000,
 "tests": {},
 "verdict": "incomplet : le noyau est décrit, pas testé (pas de p-value sur un sous-ensemble)",
 "date": "2026-11-15T03:00:32",
 "descriptif": {
  "G1": {
   "n": 1,
   "d_sig_moyenne": 0.08538973692164166,
   "delta_annee_moyen": 0.0
  },
  "G2": {
   "n": 14,
   "d_sig_moyenne": 0.06616717697312198,
   "delta_annee_moyen": 69.64285714285714
  },
  "G3": {
   "n": 12,
   "d_sig_moyenne": 0.11342042717549179,
   "delta_annee_moyen": 1521.25
  }
 }
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, numpy as np\nd=json.load(open('reports/protocole-date.json'))\nrng=np.random.default_rng(0)\nsigs={}\nfor t in d['textes']:\n    v=rng.dirichlet(np.ones(14))\n    sigs[t['id']]={a:float(x) for a,x in zip(d['protocole']['atomes'],v)}\njson.dump({'instrumen … [411 caractères tronqués]`

  ```
59
résultats écrits : /tmp/protocole-synth.json
---
{
 "statut": "complet",
 "n_paires": 60,
 "n_manquantes": 0,
 "paires_manquantes": [],
 "n_permutations": 300,
 "tests": {
  "G1_controle_positif": {
   "n": 20,
   "d_sig_moyenne": 0.3377300458515472,
   "p_permutation": 0.5813953488372093,
   "note": "nul : signatures permut\u00e9es entre les textes du groupe G1."
  },
  "P1_G2": {
   "n": 20,
   "beta_brut": -0.5174571180839327,
   "r2": 0.16588307079071707,
   "p_permutation": 0.08637873754152824,
   "beta_standardise": -0.4072874547426142
  },
  "P2_G3": {
   "n": 20,
   "beta_brut": 0.00844783630724349,
   "r2": 0.016453044122878957,
   "p_permutation": 0.6046511627906976,
   "beta_standardise": 0.12826942006136477
  },
  "pooled": {
   "n": 60,
   "beta": [
    0.33357418203507233,
    -0.009887208518600456,
    0.015972190039331348,
    -0.004634375439754853
   ],
   "r2": 0.004102958363036424
  }
 },
 "verdict": "H0 non rejet\u00e9e : aucun effet d'\u00e9poque d\u00e9tectable sur ce plan",
 "date": "2026-11-15T03:00:36",
 "descriptif": {
  "G1": {
   "n": 20,
   "d_sig_moyenne": 0.3377300458515472,
   "delta_annee_moyen": 2.2
  },
  "G2": {
   "n": 20,
   "d_sig_moyenne":
… [159 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='tools/protocole_date.py'\ns=open(p).read()\nstart=s.index('def _verdict(')\nend=s.index('\\n\\n# ---------------------------------------------------------------------------\\n# CLI')\nnew='''def _verdict(tests):\n    \"\"\"Holm sur P1/P2 + ROPE (|β std| < 0,10 ou R … [1598 caractères tronqués]`

  ```
patched
compiled
résultats écrits : /tmp/protocole-synth2.json
  ```

- **bash** `{"command": "cd ../Panini && python3 - <<'EOF'\nimport json, collections, math\ng=json.load(open('research/nipada/falsification/nipada_v334_graph_v35.json'))\nnodes=g['nodes']; edges=g['edges']\nP=json.load(open('research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nadj=collections.defaul … [950 caractères tronqués]`

  ```
n 655 r 0.9427226086011762 x range 0.0 21.230000000000004 y range 0 17
slope 0.7997868720269422 intercept 0.8419737361384114
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='tools/protocole_date.py'\ns=open(p).read()\ns=s.replace(\"elle corrèle à r = 0,973 avec le d_topo publié des 655 paires\",\"elle corrèle à r = 0,943 avec le d_topo publié des 655 paires\")\nopen(p,'w').write(s)\nprint('patched')\nEOF\npython3 tools/protocole_date.p … [165 caractères tronqués]`

  ```
patched
OK : 60 paires uniques, 20/20/20, 59 textes, sources acquises.
manifeste écrit : reports/protocole-date.json
OK : 60 paires uniques, 20/20/20, 59 textes, sources acquises.
commit Drave : f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888
commit Panini lu : 9b80c323629be60c68696f5c5a21f37ad9420073
paires : 60 ; textes : 59 ; à signer : 26
  ```

- **bash** `{"command": "cat > reports/rapport-protocole-date.md <<'MDEOF'\n# B1 — le protocole Panini à date contrôlée : 60 paires, trois strates, et les 26 signatures qui manquent\n\n> **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **L** · **Tâche** : **B1**, suite de la\n> note 4A · **Date** : 2026 … [29014 caractères tronqués]`

  ```
442 reports/rapport-protocole-date.md
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='tools/protocole_date.py'\ns=open(p).read()\nstart=s.index('def verifier_hashes(')\nend=s.index('\\n\\n# ---------------------------------------------------------------------------\\n# Rejeu')\nnew='''def verifier_hashes(manifeste: dict):\n    \"\"\"Refuse de rejoue … [1268 caractères tronqués]`

  ```
patched
compiled
résultats écrits : /tmp/resultats2.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='reports/rapport-protocole-date.md'\ns=open(p).read()\nold=\"puis 4 paires\\nuniques. Le corpus a assez de **paires** inter-traditions contemporaines ; il n'a pas assez de\\n**signatures** sur ces paires.\"\nnew=\"puis 4 familles de paires à un seul candidat\\n(ABRA … [1212 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 10, in <module>
AssertionError
[exit code: 1]
  ```

- **bash** `{"command": "grep -n -A4 -B2 \"paires uniques\\|échantillon indépendant\" reports/rapport-protocole-date.md | head -40", "description": "Locate exact report text"}`

  ```
33-
34-La note 4A ([`note-panini-334.md`](note-panini-334.md)) a rejoué le §334 de Panini/Nipada : 655
35:lignes de paires, 495 paires uniques, 488 paires uniques non auto, 48 textes, 44 signatures V14.
36-Le résultat est double :
37-
38-| mesure | 4A | lecture |
39-|---|---:|---|
--
83-| textes des 655 paires §334 | **48** |
84-| lignes de paires | **655** |
85:| paires uniques | **495** |
86:| paires uniques non auto | **488** |
87-
88-**Le point d'instrument, à ne pas rater.** Les 44 signatures de `analytic_sigs_v1.json` et les 57
89-`v14_signature` du graphe v35 ne sont **pas le même instrument** : sur les 11 œuvres communes, le
90-cosinus va de 0,42 à 0,82. Mélanger les deux dans un même test serait une faute. Le protocole utilise
--
132-Les 60 paires portent **59 textes distincts** (60 paires = 120 positions ; un texte peut servir
133-plusieurs paires). L'usage maximal est de **5** (`isaiah_book`, `book_of_enoch`), puis 4
134:(`daodejing`, `mandukya_upanishad`, `yueji`). Ce n'est pas un échantillon indépendant : l'inférence
135-regroupe par texte (permutation et bootstrap par texte), et le JSON donne l'usage de chaque texte.
136-
137-### G1 — 20 paires contemporaines de tradi
… [760 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '118,136p' reports/rapport-protocole-date.md", "description": "View pool sentence"}`

  ```
n'est donc pas le nombre de paires ; il est **localisé sur G1**, et il est **instrumental**, pas
statistique.

## 4. Les 60 paires gelées

La sélection est **déterministe** et n'utilise que les métadonnées. Les quotas sont fixés avant
lecture des signatures :

- **G1 (20)** : 6 GRECO–INDIAN, 4 CHINESE–GRECO, 3 CHINESE–INDIAN, 2 ABRAHAMIC–INDIAN,
  1 ABRAHAMIC–CHINESE, 1 ABRAHAMIC–CLASSICAL_ORACULAR, 1 GRECO–FORMAL_LOGIC,
  1 COGNITIVE_SCIENCE–FORMAL_LOGIC, 1 EUROPE_MODERN–MILLENARIAN.
- **G2 (20)** : 8 GRECO, 6 ABRAHAMIC, 3 INDIAN, 3 CHINESE.
- **G3 (20)** : 12 anglais inter-familles, 5 grec, 2 sanskrit, 1 chinois.

Les 60 paires portent **59 textes distincts** (60 paires = 120 positions ; un texte peut servir
plusieurs paires). L'usage maximal est de **5** (`isaiah_book`, `book_of_enoch`), puis 4
(`daodejing`, `mandukya_upanishad`, `yueji`). Ce n'est pas un échantillon indépendant : l'inférence
regroupe par texte (permutation et bootstrap par texte), et le JSON donne l'usage de chaque texte.
  ```

- **bash** `{"command": "sed -n '104,120p' reports/rapport-protocole-date.md", "description": "View pool composition text"}`

  ```
| **G3** | \|Δannée\| ≥ 50, même langue source | **430** | **157** | 173 | 100 |

**Le résultat de faisabilité est net.** Le §334 fournit **77** paires G1 candidates, mais **une
seule** a ses deux signatures dans l'instrument de 4A. Les 20 paires G1 existent donc comme
**plan** ; elles n'existent pas comme **mesure** tant que Panini n'a pas signé les textes. C'est le
fait central de cette fiche, et il ne dépend d'aucun résultat : il se lit dans les métadonnées.

La composition des pools explique pourquoi G1 est si mince : les 77 candidates sont
**30 GRECO–INDIAN**, **14 CHINESE–INDIAN**, **14 CHINESE–GRECO**, **7 BUDDHIST–INDIAN**, **3
FORMAL_LOGIC–GRECO**, **3 COGNITIVE_SCIENCE–FORMAL_LOGIC**, **2 ABRAHAMIC–INDIAN**, puis 4 paires
uniques. Le corpus a assez de **paires** inter-traditions contemporaines ; il n'a pas assez de
**signatures** sur ces paires.

G2 et G3 sont largement pourvus : 266 et 430 candidates, dont 103 et 157 déjà signées. Le problème
n'est donc pas le nombre de paires ; il est **localisé sur G1**, et il est **instrumental**, pas
statistique.
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='reports/rapport-protocole-date.md'\ns=open(p).read()\nold=\"**2 ABRAHAMIC–INDIAN**, puis 4 paires\\nuniques. Le corpus a assez de **paires** inter-traditions contemporaines ; il n'a pas assez de\\n**signatures** sur ces paires.\"\nnew=\"**2 ABRAHAMIC–INDIAN**, puis … [1189 caractères tronqués]`

  ```
old1 found True
old2 found True
written
113:FORMAL_LOGIC–GRECO**, **3 COGNITIVE_SCIENCE–FORMAL_LOGIC**, **2 ABRAHAMIC–INDIAN**, puis 4 familles de paires à un seul candidat
138:Deux seuils opérationnalisent les libellés. **G2** exige `20 ≤ |Δannée| ≤ 200` : un décalage nul
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run documentation review"}`

  ```
revue de documentation · 739 fiche(s) · 832 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 737 fichiers, le disque en a 739
     · compteurs : en-cours.md dit 830 JSON, le disque en a 832
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo \"---\"; bash tools/porte-tableaux.sh 2>&1 | tail -20", "description": "Run size and table checks"}`

  ```
3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2346    215   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3996 mots (budget 4 000)

  avertissements :
     · 54 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-p
… [406 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"737\\|830\\|fiche\\|JSON\" docs/pilotage/en-cours.md | head -20", "description": "Find counters in en-cours"}`

  ```
49:- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)).
80:- **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondération) ; `kd2` et `rope2048` **arrêtés** ; **paire propre** : **3,1500** → **3,1119** (−0,06 ; −0,19 anglai
… [1116 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\ns=s.replace('| fichiers / JSON de résultats | **737** / **830** |','| fichiers / JSON de résultats | **739** / **832** |')\nopen(p,'w').write(s)\nprint('updated')\nEOF\npython3 tools/revue_documentation.py 2>&1 | tail - … [59 caractères tronqués]`

  ```
updated
  revue de documentation · 739 fiche(s) · 832 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20", "description": "Check en-cours constraints"}`

  ```
en-cours · 1626 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\nold=\"- **Panini J12.1–J12.2 — §334 et CIC** :\"\nnew=(\"- **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1 inter-traditions à ±10 ans,\\n\"\n\"  20 G2 même tradition à 20–200 ans, 20 G3 même langue à d … [509 caractères tronqués]`

  ```
added
  en-cours · 1675 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  revue de documentation · 739 fiche(s) · 832 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='tools/protocole_date.py'\ns=open(p).read()\ns=s.replace('''    # défaut : vérifier\n    corpus = Corpus()\n    manifeste = lire_json(SORTIE_DEFAUT)\n    erreurs = verifier(manifeste, corpus)''','''    # défaut : vérifier\n    corpus = Corpus()\n    manifeste = lire … [286 caractères tronqués]`

  ```
patched
OK : 60 paires uniques, 20/20/20, 59 textes, sources acquises.
commit Drave : f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888
commit Panini lu : 9b80c323629be60c68696f5c5a21f37ad9420073
paires : 60 ; textes : 59 ; à signer : 26
  ```

- **bash** `{"command": "ls journal/2026-11-15/ 2>/dev/null; echo \"---\"; sed -n '1,40p' journal/2026-11-15/README.md 2>/dev/null", "description": "Inspect today's journal folder"}`

  ```
distribue.md
docs.md
mesures.md
portes.md
README.md
---
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**6 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 1 | [distribue.md](distribue.md) |
| docs | 1 | [docs.md](docs.md) |
| mesures | 3 | [mesures.md](mesures.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 345.8 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATT
… [873 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/toutes-les-portes.sh", "description": "Inspect all-gates script"}`

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
… [2800 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,60p' docs/methode/portes.md", "description": "Read gates method"}`

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
… [1865 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/porte-*.sh | sed 's#tools/porte-##;s#.sh##' | tr '\\n' ' '", "description": "List gate names"}`

  ```
adaptateur-sortie audit-drapeaux b1110-hybride balayage bloc-code bloc-linguistique bloc-maths bloc-tableaux budget bus bus-socket c4-retard cerveau cic consolidation coupe cycle-c2 deepseek delais diff-couche document echange-experts episodique etat flux fusion gain greffe harnais-invariants homeostasie horloge indice jeux jumeaux lecteur lecture m5-brouillon melange memoire miroir-blocs mistral n3-cache n3-composition n3-deux-processus n3-deux-regions n3-generation n3-inventaire n3-placement n3-pont n3-positions n3-profondeur n3-refus n3-reseau n3-routes n3-service-briques n3-service n3-seuil n3-sparsite-compte n3-sparsite occupation-elagage occupation-moteur ocr-scans ocr pannes peripherie poids-creux pont prechargement produit profondeur-routee p-paresseux.sh r13-bpe recurrence reflexe registre reparti-moteur ressources sauvegarde-modele sessions speculatif tableaux tokenizer-kimi topologie trace vision
  ```

- **bash** `{"command": "JOURNAUX=work/portes/b1-protocole-$(date +%Hh%M) PORTES=\"tableaux registre document\" DELAI=600 bash tools/toutes-les-portes.sh", "description": "Run targeted documentation gates"}`

  ```
=== PASSE COMPLÈTE DES PORTES (4 portes, borne 600 s) ===
    journaux : work/portes/b1-protocole-03h03
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-document         ✅                           6 s  ✅ porte document verte
  porte-registre         ✅                          15 s    ✅ région absente : refusée en la nommant (code 2), rien n'est calculé
  porte-tableaux         ✅                           0 s    ✅ la page vivante date du dernier commit (2026-11-15)
--- 4 vertes, 0 rouges ---
TOUTES LES PORTES SONT VERTES — et elles ont TOUTES tourné, ce que rien ne garantissait avant.
Journaux : work/portes/b1-protocole-03h03
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='reports/rapport-protocole-date.md'\ns=open(p).read()\ns=s.replace(\"2. **La date est celle de la composition, pas de la traduction.** 24/44 sources sont anglaises, 19\\nde langue inconnue ;\",\"2. **La date est celle de la composition, pas de la traduction.** 24/44 … [196 caractères tronqués]`

  ```
patched
404:2. **La date est celle de la composition, pas de la traduction.** 24/44 sources sont anglaises, 19
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='reports/rapport-protocole-date.md'\ns=open(p).read().replace(\"24/44 sources sont anglaises\",\"24/44 œuvres sont anglaises\")\nopen(p,'w').write(s)\nprint('patched')\nEOF\ngrep -n \"24/44\" reports/rapport-protocole-date.md", "description": "Fix sources to works"}`

  ```
patched
404:2. **La date est celle de la composition, pas de la traduction.** 24/44 œuvres sont anglaises, 19
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; echo \"---\"; bash tools/porte-tableaux.sh 2>&1 | tail -4", "description": "Recheck docs and tables"}`

  ```
revue de documentation · 739 fiche(s) · 832 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---
  ✅ 1811 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4338 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "python3 tools/protocole_date.py --verifier | tail -4; echo \"---\"; python3 -m py_compile tools/protocole_date.py && echo \"compile ok\"", "description": "Recheck manifest and tool"}`

  ```
OK : 60 paires uniques, 20/20/20, 59 textes, sources acquises.
commit Drave : f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888
commit Panini lu : 9b80c323629be60c68696f5c5a21f37ad9420073
paires : 60 ; textes : 59 ; à signer : 26
---
compile ok
  ```

- **bash** `{"command": "git status --short | grep -E \"protocole|en-cours|tools/protocole\" ; echo \"--- all status ---\"; git status --short | head -20; echo \"--- Panini status ---\"; git -C ../Panini status --short | head -10", "description": "Check working tree status"}`

  ```
M docs/pilotage/en-cours.md
?? reports/protocole-date.json
?? reports/rapport-protocole-date.md
?? tools/protocole_date.py
--- all status ---
 M docs/pilotage/en-cours.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/protocole-date.json
?? reports/rapport-gold-reel-50.json
?? reports/rapport-gold-reel-50.md
?? reports/rapport-protocole-date.md
?? reports/rapport-s-paragraphes.md
?? tools/protocole_date.py
?? tools/tests/linguistique/gold_reel_50.py
--- Panini status ---
 M .github/copilot-instructions.md
 M docs/index.md
 m modules/core/filesystem
 m modules/core/knowledge
 m modules/core/semantic
 m modules/data/attribution
 m modules/data/ingestion
 m modules/missions/autonomous
 m modules/ontowave
 m modules/orchestration/cloud
  ```

- **bash** `{"command": "wc -l reports/rapport-protocole-date.md reports/protocole-date.json tools/protocole_date.py; echo \"---\"; python3 -c \"import json;d=json.load(open('reports/protocole-date.json'));print(d['titre']);print(len(d['paires']),len(d['textes']),len(d['a_signer']))\"", "description": "Check de … [17 caractères tronqués]`

  ```
448 reports/rapport-protocole-date.md
  2944 reports/protocole-date.json
  1056 tools/protocole_date.py
  4448 total
---
Protocole Panini à date contrôlée — 60 paires en trois groupes
60 59 26
  ```

- **bash** `{"command": "sed -n '1,120p' .git/hooks/pre-commit 2>/dev/null || echo \"no pre-commit\"", "description": "Inspect pre-commit hook"}`

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

- **bash** `{"command": "python3 tools/verifie_etat_a_jour.py --index 2>&1 | tail -30", "description": "Check state freshness hook"}`

  ```
✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "git add reports/rapport-protocole-date.md reports/protocole-date.json tools/protocole_date.py docs/pilotage/en-cours.md && python3 tools/verifie_etat_a_jour.py --index 2>&1 | tail -30", "description": "Stage deliverables and check state"}`

  ```
✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "git diff --cached --stat", "description": "Show staged changes"}`

  ```
docs/pilotage/en-cours.md         |    6 +-
 reports/protocole-date.json       | 2944 +++++++++++++++++++++++++++++++++++++
 reports/rapport-protocole-date.md |  448 ++++++
 tools/protocole_date.py           | 1056 +++++++++++++
 4 files changed, 4453 insertions(+), 1 deletion(-)
  ```

- **bash** `{"command": "git commit -m \"B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE\" -m \"Le manifeste reports/protocole-date.json fige 60 paires tirées des 107 sources du §334 (102 acquises), en trois groupes : 20 contempora … [839 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-131]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-131", "wait": true, "timeout_ms": 120000}`

  ```
✅ index : aucun fait stagé sans état
[s/v7 c37fed06] B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE
 19 files changed, 10770 insertions(+), 28 deletions(-)
 create mode 100644 journal/sessions/session-2064d0cb-d031-4316-9674-54d67e6b3ab6/digest.md
 create mode 100644 journal/sessions/session-2064d0cb-d031-4316-9674-54d67e6b3ab6/rapport.md
 create mode 100644 journal/sessions/session-72a370ef-2ad7-4a59-8418-d88c38545f6e/digest.md
 create mode 100644 journal/sessions/session-72a370ef-2ad7-4a59-8418-d88c38545f6e/rapport.md
 create mode 100644 reports/protocole-date.json
 create mode 100644 reports/rapport-protocole-date.md
 create mode 100644 tools/protocole_date.py
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "git log --oneline -3; echo \"---\"; git status --short | head -20; echo \"---\"; git show --stat --oneline HEAD | tail -25", "description": "Verify commit and status"}`

  ```
c37fed06 B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE
f926b5bc C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PROFONDEUR, 41 VERDICTS À RE-JUGER ; PORT 8765 PRIS, PARE-FEU ACTIF ; LES 11 VERDICTS COMMITTÉS (389b99f)
292c70b5 C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09
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
---
c37fed06 B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE
 docs/pilotage/en-cours.md                          |    6 +-
 journal/2026-11-15/README.md                       |    4 +-
 journal/2026-11-15/distribue.md             
… [1120 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/protocole_date.py --verifier | tail -4; echo \"---\"; python3 tools/revue_documentation.py 2>&1 | tail -3", "description": "Post-commit verification"}`

  ```
OK : 60 paires uniques, 20/20/20, 59 textes, sources acquises.
commit Drave : f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888
commit Panini lu : 9b80c323629be60c68696f5c5a21f37ad9420073
paires : 60 ; textes : 59 ; à signer : 26
---
  revue de documentation · 739 fiche(s) · 832 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

### 🤖 Assistant

**Fait — commit `c37fed06`.** Le protocole B1 est gelé, écrit et rejouable ; **aucun fichier de Panini n’a été modifié**.

### Ce qui est livré

| fichier | rôle |
|---|---|
| [`reports/rapport-protocole-date.md`](reports/rapport-protocole-date.md) | la fiche : faisabilité, 60 paires, H0/H1, contrôles, pré-enregistrement, commande |
| [`reports/protocole-date.json`](reports/protocole-date.json) | le manifeste gelé : 60 paires, 59 textes, 26 à signer, SHA-256 des 7 artefacts §334 |
| [`tools/protocole_date.py`](tools/protocole_date.py) | construit, vérifie et rejoue ; lecture seule de Panini |

### Les chiffres qui comptent

- **60 paires** : 20 G1 (inter-traditions, `|Δ| ≤ 10`), 20 G2 (même tradition, `20 ≤ |Δ| ≤ 200`), 20 G3 (même langue, `|Δ| ≥ 50`).
- **59 textes distincts** ; usage maximal 5 (`isaiah_book`, `book_of_enoch`).
- **27 paires déjà signées** dans `analytic_sigs_v1` : **1 G1**, 14 G2, 12 G3.
- **26 textes à signer** par Panini pour que le test existe.
- Le §334 fournit **77 candidates G1**, mais **une seule** a ses deux signatures déjà mesurées. C’est le résultat de faisabilité central : le plan est possible, la mesure ne l’est pas encore.
- Les 44 signatures `analytic_sigs_v1` et les 57 `v14_signature` du graphe v35 sont **deux instruments différents** (cosinus 0,42–0,82 sur 11 œuvres communes) : le protocole interdit de les mélanger.
- Le HEAD de Panini a bougé (`9b80c323` ≠ `e10d695e`), mais les **7 artefacts §334 sont byte-identiques** à ceux de 4A — les SHA-256 le prouvent.

### La commande de rejeu

```bash
python3 tools/protocole_date.py --verifier

python3 tools/protocole_date.py --rejouer \
  --signatures /tmp/v14.json \
  --sortie reports/protocole-date-resultats.json
```

Le test **n’est pas exécuté** : il attend les 26 signatures V14. Le script refuse d’écrire dans Panini, vérifie les SHA-256, et ne teste que si les 60 paires sont complètes ; sinon il décrit le noyau sans p-value.

Contrôles passés : `--verifier`, rejeu sur signatures synthétiques, `revue_documentation.py`, `porte-tableaux.sh`, et 4 portes documentaires/registre/tableaux — toutes vertes.

