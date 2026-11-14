# Session DSH — relecture

- identifiant : `session-b0a87524-43a4-4935-a248-72c1d42c8471`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 04:16:27
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J11.1 : les exemples de la doc produit — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (F1 0,7902, 237/238, le schéma v2) et corrige les sorties qui ont bougé ; fiche `reports/rapport-exemples-rejoues.md` + JSON, commit.

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

- **bash** `{"command": "git status --short && git log --oneline -5", "description": "Show git status and recent commits"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/digest.md
 M journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/rapport.md
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
M  tools/chantier/superviseur.py
 m tools/structures
?? reports/rapport-s-paragraphes.md
03ecee41 J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ
81fc9ecf JOURNAL — 2026-11-14 : J9.1 AU RÉCIT (19 FICHES « INSTANTANÉ HISTORIQUE »)
ecef7250 J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT
229098ec J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STR
… [192 caractères tronqués]
  ```

- **read** `{"file_path": "docs/produit/exemples.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md</path>
<type>file</type>
<content>
1: # Cinq exemples d'analyse, commentés
2: 
3: > **Ce que ce document est.** Cinq exécutions **réelles** du produit, avec leur JSON commenté. Il
4: > complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
5: > *comment lire* ce qui sort. Les sorties ont été produites le **2026-11-06** sur la branche
6: > `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et sans réseau.
7: > Le **format est passé en v2** le 07/11 : `version: 2` et, sur un syntagme qui chevauche un
8: > autre, `meta.partition`/`meta.alternative` ; ces sorties v1 restent lisibles, v1 étant toujours
9: > lue ([schéma v2](../../tools/schemas/drave-annotation-v2.json)).
10: >
11: > **Une commande, un JSON.** `python3 tools/drave.py analyser "…" --json` rend l'annotation
12: > complète (neuf niveaux). Pour la lire, ce document filtre avec `jq` ; le produit, lui, n'a pas
13: > besoin de `jq`.
14: 
15: ## 0. Comment lire les JSON
16: 
17: - `debut` / `fin` : indices en **points de code Unicode**, 0-based, fin exclue : `[debut:fin)`.
18:   « Élodie 
… [22186 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"J11\" -r docs/pilotage docs/methode reports 2>/dev/null | head -50", "description": "Find J11 task references"}`

  ```
docs/pilotage/semaine-autonome.md:179:**A6.2**, la **passe générique d'honnêteté**, puis **J11–J13** (produit, Panini §334/CIC, table des
docs/pilotage/semaine-autonome.md:251:**La suite.** **J11.1–J11.4** (produit : exemples, par-langue, robustesse, schéma documenté) ;
docs/pilotage/en-cours.md:118:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087)** | **trancher `g017`** ; puis T132/T133, gold 200+ ; **J11.1–J11.4** ; **B10.3 bloquée** |
docs/pilotage/en-cours.md:128:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — 11 verdicts + pointeur ; **R0.7** — split réel ; **A** — A6.2, A8.3b2 ; **J14.1** — passe + tag ; **J11–J13** — produit, Panini, table.
reports/rapport-bilan-chantier.json:1085:   "tache": "J11.1",
reports/rapport-bilan-chantier.json:1090:   "tache": "J11.2",
reports/rapport-bilan-chantier.json:1094:   "tache": "J11.3",
reports/rapport-bilan-chantier.json:1098:   "tache": "J11.4",
reports/rapport-b
… [599 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\"; echo \"exit=$?\"", "description": "Run first example current code"}`

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
  ```

- **bash** `{"command": "sed -n '160,270p' docs/pilotage/semaine-autonome.md", "description": "Read J11 task definitions"}`

  ```
| J1.2 convention GV | ✅ livré (timeout) | F1 **0,7549 → 0,7902** | `92652984` |
| J1.3 schéma v2 | ✅ fait | `meta.partition`/`meta.alternative`, 26 cas | `9a259953` |
| J1.4 restitution v0 | ✅ fait | 46/46 surfaces exactes | `8eb0cc49` |
| J2.1 atomes ↔ niveaux | ✅ fait | 14/14 lignes | `9c7f71dc` |
| J2.2 + J3.1 corpus/retrieval | ✅ livré (timeout) | 418/438 paires exactes | `c3467170` (par J3.2) |
| J3.2 généalogie | ✅ fait | 154/154 paires hors script | `c2e629b3` |
| J4 N2/S/R/A | ✅ fait (13/11) | 4 fiches + 4 JSON ; D1–D8 | `commit J5.1` |
| J5.1 rapport de semaine | ✅ fait (13/11) | [`rapport-semaine.md`](../../reports/rapport-semaine.md) + JSON | `34e3e4ab` |
| J5.2 passe, tag, release | ❌ **échec** | passe 84/81/3 faite ailleurs (`2d6f5bff`) ; **tag absent** | — |
| J6.1 `g017` | ✅ fait (rejet) | règle rejetée ; convention d'adverbe à trancher | `64d9dd23` |
| J6.2 `s065` | ✅ fait | attachement **238/238 labels** (238/239 cibles) | `b6e474dc` |
| J7.1 retrieval familles | ✅ fait | 532 textes ; sœurs **0,619** contre **0,0445** | `d31e8788` |
| J8.1 restitution v1 | ✅ fait (timeout) | canonique **46/46**, strict **0,1087** | `229098ec` (par J9.1) |
| J9.1 honnêteté | ✅ fait
… [8248 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1050,1130p' reports/rapport-bilan-chantier.json; echo ---; sed -n '320,370p' reports/rapport-bilan-chantier.md", "description": "Read J11 section of bilan report"}`

  ```
"bloquant": "corpus Panini (lecture seule)"
  },
  {
   "ligne": "N2",
   "reste": "porte propre : 0,2856 en validation / 0,3566 en test ; rope_model.py dans tools/",
   "prochaine_action": "appliquer le correctif, re-épingler, porte-n2.sh",
   "bloquant": "GPU / runs N2"
  },
  {
   "ligne": "S",
   "reste": "committer les 11 verdicts + pointeur ; corriger 9/16 référents ; .gitmodules en chemin absolu",
   "prochaine_action": "commande § 3 de la fiche",
   "bloquant": "accès au sous-module"
  },
  {
   "ligne": "R",
   "reste": "voir R0.7 / tagger",
   "prochaine_action": "-",
   "bloquant": "-"
  },
  {
   "ligne": "A",
   "reste": "rapport A6.2 ; M1/M2/M3 ; harnais A8.3b2 ; 18/19 pins ; cache Q4_K si besoin",
   "prochaine_action": "D1–D8 de la fiche",
   "bloquant": "GPU 16 GiB ; code Q4_K"
  },
  {
   "ligne": "J9.1 / honnêteté",
   "reste": "la passe générique (tout chiffre d'arrivée antérieur à HEAD)",
   "prochaine_action": "commencer par rapport-pensee-v11.md, rapport-pensee-v9.md",
   "bloquant": "aucun"
  }
 ],
 "suite_plan": [
  {
   "tache": "J11.1",
   "objet": "rejouer les exemples de docs/produit/exemples.md",
   "note": "le mandat porte encore 237/238 ; l'état cour
… [5976 caractères tronqués]
  ```

- **bash** `{"command": "which jq; python3 tools/drave.py --version 2>&1 | head; python3 tools/drave.py analyser \"Le chat dort.\" --json | jq -r '.version, (.etiquettes|length)'", "description": "Check jq and CLI version/schema"}`

  ```
/usr/bin/jq
drave 0.1.0
2
20
  ```

- **bash** `{"command": "sed -n '1,120p' tools/drave.py", "description": "Read CLI header"}`

  ```
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, quatre gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
**restitution v0** (annotation → surface, avec la fidélité du miroir). La restitution est un
**codec de surface** : elle reconstruit depuis le niveau `graphème`, pas un décodeur neuronal.
Ce qu'elle n'expose pas encore : le neuronal (`llama-cli` ou endpoint local), la traduction et la
génération : ils demandent des poids, un service ou un GPU, alors que ce pro
… [3886 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p /tmp/j111\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"Le chat dort.\" > /tmp/j111/ex1-lisible.txt 2>&1; echo \"ex1 lisible exit=$?\"\npython3 tools/drave.py analyser \"Le chat dort.\" --json \\\n  | jq '{langue, script, refus,\n        … [660 caractères tronqués]`

  ```
ex1 lisible exit=0
ex1 json exit=0
80 /tmp/j111/ex1.json
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
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" --json \\\n  | jq '{langue, script, refus,\n         syntagmes: [.etiquettes[] | select(.niveau==\"syntagme\")\n           | {valeur, type, debut, fin, confiance … [380 caractères tronqués]`

  ```
ex2 exit=0
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "syntagmes": [
    {
      "valeur": "Le livre",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.55,
      "role": "agent",
      "cible": "intéressant",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ]
    },
    {
      "valeur": "que j'ai lu",
      "type": "REL",
      "debut": 9,
      "fin": 20,
      "confiance": 0.55,
      "role": "qualite",
      "cible": "livre",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ]
    },
    {
      "valeur": "que j'ai lu est intéressant",
      "type": "REL",
      "debut": 9,
      "fin": 36,
      "confiance": 0.3,
      "role": "qualité",
      "cible": "livre",
      "union": true,
      "candidats": [
        "REL",
        "livre",
        "intéressant"
      ]
    },
    {
      "valeur": "est intéressant",
      "type": "GV",
      "debut": 21,
      "fin": 36,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "livre",
      "union": null,
      "candidats": [
        "
… [302 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"The day when we left was beautiful.\" --langue en --json \\\n  | jq '{langue, script, refus,\n         pos: [.etiquettes[] | select(.niveau==\"pos\")\n           | {valeur, type, debut, fin, confiance, … [348 caractères tronqués]`

  ```
ex3 exit=0
{
  "langue": "en",
  "script": "Latn",
  "refus": "",
  "pos": [
    {
      "valeur": "The",
      "type": "DET",
      "debut": 0,
      "fin": 3,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "day",
      "type": "NOUN",
      "debut": 4,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "when",
      "type": "CONJ",
      "debut": 8,
      "fin": 12,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "we",
      "type": "PRON",
      "debut": 13,
      "fin": 15,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "left",
      "type": "VERB",
      "debut": 16,
      "fin": 20,
      "confiance": 0.85,
      "ouvert": true
    },
    {
      "valeur": "was",
      "type": "AUX",
      "debut": 21,
      "fin": 24,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "beautiful",
      "type": "ADJ",
      "debut": 25,
      "fin": 34,
      "confiance": 0.68,
      "ouvert": true
    },
    {
      "valeur": ".",
      "type": "PONCT",
      "debut": 34,
      "fin": 35,
      "confiance": 0.95,
      "ouvert": false
    }
  
… [797 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"\" > /tmp/j111/ex4-cli-out.txt 2> /tmp/j111/ex4-cli-err.txt; echo \"ex4 cli exit=$?\"\necho \"--- stdout\"; cat /tmp/j111/ex4-cli-out.txt; echo \"--- stderr\"; cat /tmp/j111/ex4-cli-err.txt\npython3 to … [244 caractères tronqués]`

  ```
ex4 cli exit=3
--- stdout
--- stderr
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
ex4 api exit=0
{
  "langue": "und",
  "script": "Zyyy",
  "refus": "vide",
  "etiquettes": 0
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"The film she talks about is out.\" --json \\\n  | jq '{langue, script, refus,\n         syntagmes: [.etiquettes[] | select(.niveau==\"syntagme\")\n           | {valeur, type, debut, fin, confiance, rol … [375 caractères tronqués]`

  ```
ex5 exit=0
{
  "langue": "en",
  "script": "Latn",
  "refus": "",
  "syntagmes": [
    {
      "valeur": "The film",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.35,
      "role": "groupe nominal",
      "cible": "out",
      "union": null,
      "candidats": [
        "GN",
        "out"
      ]
    },
    {
      "valeur": "she talks about",
      "type": "REL",
      "debut": 9,
      "fin": 24,
      "confiance": 0.35,
      "role": "qualité",
      "cible": "film",
      "union": null,
      "candidats": [
        "REL",
        "film",
        "out"
      ]
    },
    {
      "valeur": "is out",
      "type": "GV",
      "debut": 25,
      "fin": 31,
      "confiance": 0.35,
      "role": "prédicat",
      "cible": null,
      "union": null,
      "candidats": [
        "GV"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type",
      "valeur": "déclarative"
    }
  ],
  "pragmatique": [
    {
      "type": "acte",
      "valeur": "assertion"
    }
  ]
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ncat /tmp/j111/ex1.json | head -50\necho ===\npython3 tools/drave.py evaluer --gold --json > /tmp/j111/eval.json 2>&1; echo \"eval exit=$?\"; head -60 /tmp/j111/eval.json", "description": "Inspect example 1 JSON and current eval"}`

  ```
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "pos": [
    {
      "valeur": "Le",
      "type": "DET",
      "debut": 0,
      "fin": 2,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "chat",
      "type": "NOUN",
      "debut": 3,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "dort",
      "type": "VERB",
      "debut": 8,
      "fin": 12,
      "confiance": 0.72,
      "ouvert": true
    },
    {
      "valeur": ".",
      "type": "PONCT",
      "debut": 12,
      "fin": 13,
      "confiance": 0.95,
      "ouvert": false
    }
  ],
  "syntagmes": [
    {
      "valeur": "Le chat",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confiance": 0.55,
      "role": "agent",
      "cible": "dort",
      "union": null,
      "candidats": [
        "structure la plus proche",
===
eval exit=0
{
 "version": "0.1.0",
 "gold": {
  "nom": "gelé (référence figée)",
  "gele": true,
  "phrases": 602,
  "tokens": 3141,
  "cibles_attachement": 239
 },
 "heuristique": {
  "bloc": "heuristique",
  "phrases": 602,
  "pos": {
   "exactitude": 0.8625,
   "exactitude_ferme": 0.9373,
   "exactitude_ouvert": 0
… [608 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -rn \"r035\" reports/rapport-pensee-v12.md reports/rapport-r035.md 2>/dev/null | head -20\necho ===\nsed -n '1,80p' reports/rapport-r035.md", "description": "Read r035 report"}`

  ```
reports/rapport-r035.md:1:# B13 — la relative zéro (r035) : exact 236 → 237, POS inchangée
reports/rapport-r035.md:9:> **`r035` est réglé** : « The film **she talks about** is out. » n'a aucun marqueur de relative.
reports/rapport-r035.md:18:> JSON [`pensee-r035.json`](pensee-r035.json).
reports/rapport-r035.md:22:Gold de `r035` (`tools/tests/linguistique/gold_reel.json`) :
reports/rapport-r035.md:63:[`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; `r035` est en **dev**. Mesure
reports/rapport-r035.md:81:Lecture : l'attachement **exact** gagne le cas `r035` (236 → 237) ; le nombre de labels gagne
reports/rapport-r035.md:90:- **Diff du gold entier** : une seule phrase sur **612** change (`r035`) ; **0 token POS** sur
reports/rapport-r035.md:103:- **Généralisation hors du lexique de `r035`** : « The book **he reads about** is good. » rend
reports/rapport-r035.md:111:1. **Un seul cas dans le gold, et il est en dev.** La règle a été écrite après avoir vu `r035` :
reports/rapport-r035.md:117:3. **La frontière du GN est plus générale que `r035`.** Elle s'applique à tout GN à déterminant
reports/rapport-r035.md:118:   suivi d'un pronom sujet + verbe ; sur le gold elle ne cha
… [4173 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\njq '{version, gold, sync: .[\"synchro\"]?, heuristique: {phrases: .heuristique.phrases, pos: .heuristique.pos.exactitude, f1: .heuristique.syntagmes.f1, precision: .heuristique.syntagmes.precision, rappel: .heuristique.syntagmes.rappel … [200 caractères tronqués]`

  ```
{
  "version": "0.1.0",
  "gold": {
    "nom": "gelé (référence figée)",
    "gele": true,
    "phrases": 602,
    "tokens": 3141,
    "cibles_attachement": 239
  },
  "sync": null,
  "heuristique": {
    "phrases": 602,
    "pos": 0.8625,
    "f1": null,
    "precision": null,
    "rappel": null,
    "attachement": {
      "cibles": 239,
      "labels": 234,
      "top1": 234,
      "topk": 232,
      "exact": 234,
      "top1_taux": 0.9791,
      "topk_taux": 0.9707,
      "exact_taux": 0.9791,
      "exact_any": 234,
      "exact_any_taux_span": 1.0,
      "top1_taux_span": 1.0,
      "topk_taux_span": 0.9915,
      "topk_exact": 232,
      "topk_exact_taux": 0.9707,
      "topk_exact_taux_span": 0.9915,
      "exact_taux_span": 1.0,
      "verbe": {
        "cibles": 154,
        "justes": 154,
        "taux": 1.0
      },
      "nom": {
        "cibles": 80,
        "justes": 80,
        "taux": 1.0
      },
      "couverture": 0.9791,
      "par_langue": {
        "fr": {
          "cibles": 151,
          "labels": 147,
          "exact": 147,
          "topk": 145,
          "exact_taux_span": 1.0
        },
        "en": {
          "cibles": 88,
          "labels": 87,
  
… [359 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"evaluer\\|gold\" tools/drave.py | head -60", "description": "Find evaluer options"}`

  ```
8:    python3 tools/drave.py evaluer
9:    python3 tools/drave.py evaluer --gold --json
16:avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
210:    """Charge `evaluer_gold.py` (le gold et sa mesure) sans dépendre du répertoire courant."""
211:    chemin = RACINE / "tools" / "tests" / "linguistique" / "evaluer_gold.py"
213:        raise FileNotFoundError(f"mesure du gold introuvable : {chemin}")
214:    spec = importlib.util.spec_from_file_location("_drave_evaluer_gold", chemin)
223:def _cibles_gold(phrases: list[dict]) -> list[str]:
228:    """Contrôle négatif : une cible **exacte** tirée au hasard parmi les cibles du gold.
232:    cibles = _cibles_gold(phrases)
246:    gold = rapport["gold"]
256:        f"{NOM} {VERSION} — évaluation de l'heuristique sur le gold",
257:        f"gold {gold['nom']} · {gold['phrases']} phrases · {gold['tokens']} tokens · "
258:        f"{gold['cibles_attachement']} cibles d'attachement",
280:def cmd_evaluer(args: argparse.Namespace) -> int:
282:    phrases = evaluateur.charger_gele() if args.gold else evaluateur.charger()
283:    mesure = evaluateur.evaluer_bloc("heuristique", bl.Heuristique(), phrases)
… [1146 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py evaluer --json > /tmp/j111/eval-vivant.json 2>&1; echo \"exit=$?\"\njq '{gold, h: {pos: .heuristique.pos.exactitude, syntagme: .heuristique.syntagme, attachement: (.heuristique.attachement|{cibles,labels,exact,ex … [96 caractères tronqués]`

  ```
exit=0
{
  "gold": {
    "nom": "vivant (hand + reel + synthétique)",
    "gele": false,
    "phrases": 612,
    "tokens": 3179,
    "cibles_attachement": 239
  },
  "h": {
    "pos": 0.8625,
    "syntagme": {
      "precision": 0.786,
      "rappel": 0.7944,
      "f1": 0.7902,
      "tp": 1480,
      "fp": 403,
      "fn": 383,
      "tete": {
        "precision": 0.9261,
        "rappel": 0.8808,
        "f1": 0.9029,
        "tp": 1641,
        "fp": 131,
        "fn": 222
      }
    },
    "attachement": {
      "cibles": 239,
      "labels": 238,
      "exact": 238,
      "exact_taux": 0.9958,
      "couverture": 0.9958
    }
  }
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" --json > /tmp/j111/ex2-full.json 2>&1\njq '{version, meta: .meta, n: (.etiquettes|length), syntagmes: [.etiquettes[]|select(.niveau==\"syntagme\")|{valeur,type,d … [95 caractères tronqués]`

  ```
{
  "version": 2,
  "meta": null,
  "n": 43,
  "syntagmes": [
    {
      "valeur": "Le livre",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "meta": {
        "role": "agent",
        "niveau": 1,
        "attachement": {
          "segment": "Le livre",
          "cible": "intéressant"
        }
      }
    },
    {
      "valeur": "que j'ai lu",
      "type": "REL",
      "debut": 9,
      "fin": 20,
      "meta": {
        "role": "qualite",
        "niveau": 1,
        "attachement": {
          "segment": "que j'ai lu",
          "cible": "livre"
        },
        "partition": {
          "groupe": 0,
          "rang": 3,
          "membres": 3,
          "vue": "alternative"
        },
        "alternative": [
          {
            "type": "REL",
            "debut": 9,
            "fin": 36,
            "source": "heuristique",
            "union": true,
            "relation": "inclus",
            "rang": 1,
            "attachement": {
              "segment": "que j'ai lu est intéressant",
              "cible": "livre"
            },
            "role": "qualité"
          },
          {
            "type": "GV",
            "debut": 21,
            "f
… [2746 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"The film she talks about is out.\" --json > /tmp/j111/ex5-full.json 2>&1\njq '{version, refus, n: (.etiquettes|length), syntagmes: [.etiquettes[]|select(.niveau==\"syntagme\")|{valeur,type,debut,fin,co … [94 caractères tronqués]`

  ```
{
  "version": 2,
  "refus": "",
  "n": 37,
  "syntagmes": [
    {
      "valeur": "The film",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.35,
      "meta": {
        "role": "groupe nominal",
        "niveau": 0,
        "attachement": {
          "segment": "The film",
          "cible": "out"
        }
      }
    },
    {
      "valeur": "she talks about",
      "type": "REL",
      "debut": 9,
      "fin": 24,
      "confiance": 0.35,
      "meta": {
        "role": "qualité",
        "niveau": 1,
        "attachement": {
          "segment": "she talks about",
          "cible": "film"
        }
      }
    },
    {
      "valeur": "is out",
      "type": "GV",
      "debut": 25,
      "fin": 31,
      "confiance": 0.35,
      "meta": {
        "role": "prédicat",
        "niveau": 0
      }
    }
  ]
}
  ```

- **bash** `{"command": "date -u +%Y-%m-%d; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git log -1 --format='%ci %H'; grep -n \"J11\" reports/INDEX.md | head", "description": "Check current date and HEAD"}`

  ```
2026-11-14
2026-11-14 03:53:52 -0500 03ecee413cb05cf906d623765443d98d317e7f59
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '80,140p' reports/rapport-r035.md\necho === g011\ngrep -rn \"g011\" reports/*.md | head", "description": "Read r035 caveats and g011 refs"}`

  ```
Lecture : l'attachement **exact** gagne le cas `r035` (236 → 237) ; le nombre de labels gagne
aussi le label REL (237 → 238), donc la couverture est **238/239 = 0,9958**, et non 1,0. Les
deux mesures restantes sont hors du périmètre de cette tâche : **1 span manquant** (`g017`, SUB
« that she would come ») et **1 cible fausse** (`s065`, REL synthétique : cible gold `elle`,
prédite `nage`). Le test ne bouge pas : il ne contient pas de relative zéro, donc il ne confirme
rien — il montre seulement l'absence d'effet de bord.

## 4. Contrôles

- **Diff du gold entier** : une seule phrase sur **612** change (`r035`) ; **0 token POS** sur
  **3 179** change. Le diff exact est : `+GN [0:8]`, `+REL [9:24]`, `+GV [25:31]` ;
  `−GN [0:12]`, `−GV [13:18]`, `−GV [19:31]`.
- **Contrôles négatifs de la règle** (même analyseur, anglais sauf mention) :

| phrase | attendu | observé |
|---|---|---|
| « The film she talks about **the book** is out. » | pas de REL (complément nominal) | pas de REL |
| « The film she talks about **it** is out. » | pas de REL (pronom objet) | pas de REL |
| « The film she talks about **today** is out. » | pas de REL (adverbe complément) | pas de REL |
| « The film talks
… [2299 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -rn \"inatteignable\\|17 spans\\|17 cibles\" reports/*.md docs/**/*.md 2>/dev/null | head -30", "description": "Find unreachable spans references"}`

  ```
reports/INDEX.md:600:| [rapport-pensee-v12.md](rapport-pensee-v12.md) | B13 — 222/222 (1,0000) : le dernier marqueur ambigu, et 17 spans inatteignables |
reports/rapport-audit-r1r3.md:16:**10 ne sont pas inatteignables** : 7 régressions nouvelles et 3 gains A17 non intégrés.
reports/rapport-audit-r1r3.md:68:| « inatteignables » | 17 | **17** (même ensemble que A17) | **17** | 0 |
reports/rapport-audit-r1r3.md:265:- **Le compte est juste** : 27 = 16 REL + 6 SUB + 5 GP ; les 17 « inatteignables » sont bien
reports/rapport-audit-r1r3.md:266:  les 17 d'A17. Mais **4 de ces 17 ne sont pas inatteignables** : ce sont les 4
reports/rapport-audit-r1r3.md:274:- **Les 10 non-A17 ne sont pas des inatteignables** : 7 régressions (dont 6 dues à R1a) et
reports/rapport-audit-r1r3.md:395:8. **Moyenne — les 27 ne sont pas 17 + 10 inatteignables** : 7 régressions nouvelles + 3
reports/rapport-audit-r1r3.md:405:13. **Mineure — « 17 inatteignables »** : 13 non récupérables + 4 récupérables hors
reports/rapport-audit-v10.md:16:(`r153`, test), **+1 exact**. Les **19 spans** ne sont pas « 17 inatteignables + `r255` +
reports/rapport-audit-v10.md:134:- **La décomposition des 20 spans est fausse** : « 17 é
… [3939 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\njq '.heuristique.attachement.par_langue' /tmp/j111/eval-vivant.json\necho ===\npython3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" | head -30", "description": "Inspect per-language attachment and ex2 readable"}`

  ```
{
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
===
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 43 étiquettes · unités sémantiques=3 (48.6% du texte)
POS  Le/DET livre/NOUN que/PRON j'ai/PRON lu/NOUN est/AUX intéressant/ADJ ./PONCT
SYNTAGMES
  GN   [0:8]    Le livre                     rôle=agent     → intéressant
  REL  [9:20]   que j'ai lu                  rôle=qualite   → livre
  REL  [9:36]   que j'ai lu est intéressant  rôle=qualité   → livre
  GV   [21:36]  est intéressant              rôle=predicat  → livre
PRAGMATIQUE
  phrase [0:37] déclarative · acte=assertion · négation=non · modalité=non · double sens=oui
COUVERTURE  (confiance max par niveau)  graphème=0.99 · morphème=0.32 · mot=0.98 · pos=0.95 ·
            syntagme=0.55 · phrase=0.85 · discours=0.55 · pragmatique=0.45 · document=0.70
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"^def \\|^class \" tools/tests/linguistique/evaluer_gold.py | head -50\nsed -n '1,80p' tools/tests/linguistique/evaluer_gold.py", "description": "Inspect gold evaluator functions"}`

  ```
24:def charger() -> list[dict]:
38:def charger_gele() -> list[dict]:
47:def par_source(phrases: list[dict], source: str) -> list[dict]:
51:def _pos_map(a: bl.Annotation) -> dict[tuple[int, int], str]:
55:def _seg(a: bl.Annotation) -> set[tuple[str, int, int]]:
59:def _tete(a: bl.Annotation) -> set[tuple[str, int]]:
64:def _pragma(a: bl.Annotation) -> dict:
72:def _prf(tp: int, fp: int, fn: int) -> dict:
80:def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
225:def main() -> int:
"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).

Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
(`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import Counter, defaultdict

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl  # noqa: E402

GOLD = pathlib.Path(__file__).with_name("gold.json")
REEL = pathlib.Path(__file__).with_name
… [2340 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nsys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as ev\nphrases = ev.charger()\nh = bl.Heuristique()\nmissed=[]\ntargets_m … [633 caractères tronqués]`
