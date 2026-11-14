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

  ```
phrases 612 missed segments 383
Counter({'GV': 168, 'GN': 140, 'ADJ': 35, 'ADV': 30, 'PONCT': 9, 'SUB': 1})
g017 ('SUB', 9, 28) 'that she would come' | She said that she would come yesterday.
r004 ('GN', 0, 9) 'brille' | Le soleil brille.
r004 ('GV', 10, 16) 'brille' | Le soleil brille.
r019 ('GV', 8, 15) 'souffle' | Le vent souffle fort.
r023 ('GN', 8, 13) 'music' | We love music.
r023 ('GV', 3, 7) 'music' | We love music.
r039 ('GV', 9, 14) 'blows' | The wind blows hard.
r046 ('GN', 0, 7) 'du lait' | Le chat boit du lait.
r046 ('GN', 13, 20) 'du lait' | Le chat boit du lait.
r046 ('GV', 8, 12) 'du lait' | Le chat boit du lait.
r047 ('GN', 0, 10) 'dans le jardin' | Les fleurs poussent dans le jardin.
r047 ('GV', 11, 19) 'dans le jardin' | Les fleurs poussent dans le jardin.
r049 ('GV', 8, 12) 'dort' | Le bébé dort profondément.
r051 ('GV', 11, 16) 'roule' | La voiture roule vite.
r065 ('GN', 12, 22) 'television' | She watches television.
r065 ('GV', 4, 11) 'television' | She watches television.
r066 ('GN', 15, 19) 'milk' | The cat drinks milk.
r066 ('GV', 8, 14) 'milk' | The cat drinks milk.
r069 ('GV', 9, 15) 'sleeps' | The baby sleeps deeply.
r071 ('GV', 8, 14) 'drives' | The ca
… [22641 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"17\\|inatteignable\\|couverture\" reports/rapport-pensee-v12.md | head -40\necho ====\nsed -n '1,90p' reports/rapport-pensee-v12.md", "description": "Read v12 report context"}`

  ```
1:# B13 — 222/222 (1,0000) : le dernier marqueur ambigu, et 17 spans inatteignables
4:> **Instantané historique** · **Verdict** : ✅ — **la cible de A17 est atteinte**.
5:> *Depuis, le gold a été corrigé (4 GP sans préposition) : l'état courant est **226/226**, couverture
10:> **couverture 0,9289**, **F1 0,5893** (union ; S 0,5014, chunker 0,6203), tête **0,7392** ;
11:> **17 spans** restants (8 REL, 5 SUB, 4 GP) — **tous inatteignables** sans corriger le gold ou
31:| **couverture** | 0,9247 | **0,9289** |
36:| spans perdus | 18 | **17** (8 REL, 5 SUB, 4 GP) |
42:- **Les 17 spans restants sont inatteignables** : 12 formes synthétiques (le lexique du gold
45:- **L'attachement ne peut plus progresser que par la couverture**, et la couverture par le gold
57:- **Les 17 spans** : non prédits, donc hors mesure d'attachement.
64:  qui a raison dans la mesure — c'est une limite de **couverture du lexique**, pas d'attachement ;
70:1. **Les 17 spans** : corriger le gold (GP sans préposition) et étendre le lexique réel, ou les
71:   accepter comme couverture du gold.
====
# B13 — 222/222 (1,0000) : le dernier marqueur ambigu, et 17 spans inatteignables

> **Ligne de roadmap** : **B13** (moteur
… [3725 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '1,70p' reports/rapport-gold-gp-corrige.md", "description": "Read gold GP corrected report"}`

  ```
# B13 — le gold corrigé : 4 GP retrouvés, exact 226/226, couverture 0,9456

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Un défaut du générateur de gold**, pas du bloc : dans le mode `sv` de
> `gold_synthetique.py`, le span d'un GP partait **après** la préposition (`i = v + index(prep) + 1`)
> alors que le mode `sv_gp` l'inclut (`i - 1`). Quatre GP du gold étaient donc **sans préposition** —
> inatteignables par construction. Corrigé, le gold garde **les mêmes 160 phrases** (mêmes ids,
> mêmes segments) et **4 GP** sont réparés : l'attachement passe de **222/222 à 226/226**,
> la **couverture de 0,9289 à 0,9456**, les **spans perdus de 17 à 13** (les 4 GP ont disparu de
> la liste). **dev 155/155, test 71/71.**
>
> **Dispositif** : [`gold_synthetique.py`](../tools/tests/linguistique/gold_synthetique.py) (mode
> `sv`), [`gold_synthetique.json`](../tools/tests/linguistique/gold_synt
… [2342 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '1,80p' reports/rapport-s065.md", "description": "Read s065 report"}`

  ```
# B13 — s065 : la REL « qui commence » est attachée au sujet du GV qui la suit

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.2 · **Date** : 2026-11-14 ·
> **Verdict** : ✅ **règle intégrée**.
> La cible `s065` (« elle qui commence nage ») attend `elle` ; le bloc prédisait `nage`, le GV
> le plus proche. La règle **« REL suivie d'un GV → le sujet de ce GV »** corrige la cible
> **sans toucher un seul span, ni une seule POS** : **F1 0,7902 inchangé**, **attachement
> 237/238 → 238/238 labels** (238/239 cibles, **0,9958**), **exactitude sur les spans
> 0,9958 → 1,0**. Le gain est **en dev** ; le test ne contient aucun cas déclencheur et reste
> à **76/76**. La règle est intégrée avec un test unitaire, la porte du bloc est verte.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (règle intégrée),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; copies locales dans
> `/tmp/s065/` (`bloc_base.py` avant règle, `bloc_rel_gn.py`, `bloc_rel_apres_gv.py`,
> `bloc_placebo.py` pour les contrôles) ; **0 fichier du dépôt modifié pour la 
… [3083 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"refus\\|code 3\\|exit\" docs/produit/README.md | head -30\necho ===\ngrep -n \"refus\\|return 3\\|exit\" tools/drave.py | head -30", "description": "Check README refusal contract and CLI code"}`

  ```
195:### 3.5 Le refus, et la langue inconnue
198:python3 tools/drave.py analyser ""; echo "exit=$?"
201:drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
202:exit=3
205:**Lecture.** Le refus est une **réponse** : le CLI écrit un **JSON d'annotation** sur `stdout`
206:(`refus: "vide"`, `schema: "drave.annotation"`, `version: 2`, `etiquettes: []`) et sort avec le
338:| **refus explicite** | texte vide ou sans lettre/chiffre → `refus: "vide"`, 0 étiquette | bloc : JSON ; CLI : JSON sur `stdout` + code 3 |
360:| **3** | refus **distinct** de l'erreur, avec l'annotation de refus sur `stdout` | `analyser ""`, `restituer "..."` |
===
23:Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 1 erreur.
183:        print(f"{NOM}: refus d'analyse : vide", file=sys.stderr)
184:        return 3
194:    if annotation.refus:
195:        # un refus est une **réponse** : le JSON la porte, le code 3 la distingue d'une erreur
199:            print(f"{NOM}: refus d'analyse : {annotation.refus} "
201:        return 3
318:    if premiere.refus or seconde.refus:
319:        refus = premiere.refus or seconde.refus
320:        print(f"{NOM}: refus d'analyse : {refu
… [283 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '170,215p' tools/drave.py\necho === README\nsed -n '190,215p' docs/produit/README.md", "description": "Inspect refusal implementation and README"}`

  ```
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
        # un refus est une **réponse** : le JSON la porte, le code 3 la distingue d'une erreur
        if args.json:
            sys.stdout.write(_dumps(annotation.json()))
        else:
            print(f"{NOM}: refus d'analyse : {annotation.refus} "
     
… [1786 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"\" --json > /tmp/j111/refus-json.txt 2>/tmp/j111/refus-json-err.txt; echo \"exit=$?\"; echo stdout; cat /tmp/j111/refus-json.txt; echo stderr; cat /tmp/j111/refus-json-err.txt", "description": "Test re … [19 caractères tronqués]`

  ```
exit=3
stdout
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
stderr
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -rn \"exemples.md\" --include=\"*.py\" --include=\"*.sh\" --include=\"*.md\" . | grep -v \"^./docs/produit/exemples.md\" | head -20", "description": "Find references to examples doc"}`

  ```
./reports/rapport-bilan-chantier.md:346:**La suite immédiate du plan.** **J11.1** rejoue les exemples de `docs/produit/exemples.md` — le
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:50770:     · annotation : docs/produit/README.md → exemples.md (cassé)
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:50771:     · annotation : docs/produit/README.md → exemples.md (cassé)
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:50802:⏵ J'écris `exemples.md` avec des sorties réelles (dont la limite du doublon REL)
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:50804:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > docs/produit/exemples.md <<'MD'\n# Exemples — entrées et sorties réelles\n\n> Tous les exemples ci-dessous ont été **lancés** avec `tools/drave.py` le 2026-11-06 sur `s/v7`.\n> Les sorties sont recopiées telles quelles (espaces … [3816 caractères tronqués]`
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:50808:     · navigation : docs/produit/exemples.md n'a aucun lien entrant
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:50883: create m
… [3174 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nls reports | grep -i \"exemple\\|j11\" ; sed -n '1,40p' reports/INDEX.md", "description": "Check reports index and existing example reports"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **719 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
| [aiguille-gpt-oss.md](aiguille-gpt-oss.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf |
| [alignement-verne.md](alignement-verne.md) | Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais) |
| [bilan-b11.md](bilan-b11.md) | Bilan B11 — ce qui tient, ce qui ne tient pas |
| [bilan-multi-materiel.md](bilan-multi-materiel.md) | Bilan multi-matériel — CPU, FPGA, GPU |
| [campagne-benefices.md](campagne-benefices.md) | Campagne 24 h — où Drave est à son meilleur, tâche par tâche |
| [fiche-nuit-17-10.md](fiche-nuit-17-10.md) | La nuit du 17 au 18 
… [3274 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '1,160p' docs/methode/resultats.md", "description": "Read result-report method"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nls tools | head -50; grep -rln \"exemples\" tools --include=\"*.py\" --include=\"*.sh\" | head -20", "description": "Look for doc replay tooling"}`

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
apres-telechargement-k3.sh
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
boucle-cerveau.sh
boucle_directe.py
bruit_entree.py
budget_execution_locale.py
c4_retard.sh
c8_carte_profondeur.sh
c8_corpus.sh
c8_entrainer_tete.py
c8_sonde_lineaire.py
cache_pont.py
calibre_modes.py
calibrer.py
campagne-benefices.sh
campagne_synthese.py
canal_structure.py
cancellation_langue.py
carte_chantiers.py
carte_coupe.sh
carte_decisions.py
tools/pont_recurrent.py
tools/lecture_locale.py
tools/c8_entrainer_tete.py
tools/profondeur_routee_oracle.py
tools/verifier_liens.py
tools/pensee_multilingue.py
tools/pidgin_fewshot.py
tools/lora_pidgin.py
tools/corpus_raisonnement.py
… [334 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -rn \"bloc de code\\|blocs de code\\|rejoue\" tools/*.py | head -20", "description": "Search replay helpers"}`

  ```
tools/aiguille.py:178:              f"caractères — certaines sondes rejoueront la même invite, et des "
tools/banc_lecteur.py:59:                    help="rejouer la comparaison de la FALAISE (§ 18) : on répète le bloc t fois, pour "
tools/bloc_linguistique.py:172:    de test. Un profil est une donnée, pas un prompt : il se versionne et se rejoue.
tools/corpus_commun.py:659:`--controle-negatif` rejoue les tests de contrôle. Le script ne modifie jamais Panini : il vérifie
tools/corpus_commun.py:1112:        "--controle-negatif", action="store_true", help="rejouer les tests de contrôle"
tools/distiller_budget.py:8:rejoue le **budget complet** — 20 000 pas × 16 × 128 = **41 Mo** — et permet de
tools/distiller_section.py:6:Ce script rejoue la distillation **par segments** pour comparer trois bras à budget
tools/drave.py:10:    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
tools/drave.py:66:    """La forme comparée par `rejouer` : clés triées, durée exclue, sans espaces inutiles."""
tools/drave.py:315:def cmd_rejouer(args: argparse.Namespace) -> int:
tools/drave.py:429:        "Commandes : analyser, evaluer, rejouer, restituer.\n"
tools/drave.p
… [730 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -rn \"13 spans\\|r255.*r264\\|12 spans\" reports/*.md | head -20", "description": "Find the 13-span list"}`

  ```
reports/rapport-audit-r1r3.md:224:| **A17 non récupérables** (13) + hors périmètre (4) | **17** | 8 REL / 5 SUB / 4 GP | `r035 r255 r264 r288 s010 s027 s035 s044 s061 s065 s112 s114 s125 s141 s146 s148 s160` |
reports/rapport-audit-r1r3.md:267:  « récupérables hors périmètre » d'A17 (`r035`, `r255`, `r264`, `r288`) ; seuls 13 sont
reports/rapport-audit-v10.md:17:`r264` » : `r255`/`r264` sont déjà dans les 17 ; les deux extras réels sont **`s037`**
reports/rapport-audit-v10.md:135:  de A17 (`r153`, `r255`, `r264`) ». `r255` et `r264` **appartiennent aux 17** ; les trois
reports/rapport-audit-v10.md:233:et `r303`. La fiche v10 annonce « 17 inatteignables + `r255` + `r264` » : `r255` et `r264`
reports/rapport-audit-v10.md:259:gold sans préposition) et **4 hors périmètre mais récupérables** (`r035`, `r255`, `r264`,
reports/rapport-audit-v10.md:336:   périmètre récupérables (`r035`, `r255`, `r264`, `r288`). La v10 répète le raccourci.
reports/rapport-audit-v7.md:417:**12 spans français REL+SUB manquants** (8 REL + 4 SUB), pas aux « qui ». La répartition par
reports/rapport-coherence-fiches-v8.md:243:| V8-2 | **C** | en-tête et § 2, lignes 10 et 44-46 | « 27 spans (16 REL, 6 SUB, 5 GP), 
… [2237 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as ev\nphr={p['id']:p for p in ev.charger()}\nh=bl.Heuristique()\nfor pid in ['r035', … [591 caractères tronqués]`

  ```
r035 'The film she talks about is out.'
  gold [('GN', 0, 8), ('GV', 25, 31), ('REL', 9, 24)]
  pred [('GN', 0, 8), ('GV', 25, 31), ('REL', 9, 24)]
  missed []
  gold targets [('REL', 9, 24, 'film')]
r255 "La voiture que j'ai achetée roule."
  gold [('GN', 0, 10), ('GV', 28, 33), ('REL', 11, 27)]
  pred [('GN', 0, 10), ('GV', 28, 33), ('REL', 11, 27), ('REL', 11, 33)]
  missed []
  gold targets [('REL', 11, 27, 'voiture')]
r264 "Je sais qu'il vient demain."
  gold [('GN', 0, 2), ('GV', 3, 7), ('SUB', 8, 26)]
  pred [('GN', 0, 2), ('GP', 20, 26), ('GV', 3, 7), ('SUB', 8, 19), ('SUB', 8, 26)]
  missed []
  gold targets [('SUB', 8, 26, 'sais')]
r288 'I know that he comes tomorrow.'
  gold [('GN', 0, 1), ('GV', 2, 6), ('SUB', 7, 29)]
  pred [('GN', 0, 1), ('GV', 2, 6), ('SUB', 7, 29)]
  missed []
  gold targets [('SUB', 7, 29, 'know')]
g017 'She said that she would come yesterday.'
  gold [('GN', 0, 3), ('GV', 4, 8), ('SUB', 9, 28)]
  pred [('GN', 0, 3), ('GV', 4, 8), ('SUB', 9, 38)]
  missed [('SUB', 9, 28)]
  gold targets [('SUB', 9, 28, 'said')]
s065 'elle qui commence nage'
  gold [('GN', 0, 4), ('GV', 18, 22), ('REL', 5, 17)]
  pred [('GN', 0, 4), ('GV', 18, 22), ('REL', 5, 17), (
… [66 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as ev\nphr=ev.charger(); h=bl.Heuristique()\nmissing=[]; total=0\nfor p in phr:\n     … [499 caractères tronqués]`

  ```
targets 239 missing 1
('g017', 'SUB', 9, 28, 'said', 'She said that she would come yesterday.')
  ```

- **bash** `{"command": "cat /tmp/j111/ex1.json", "description": "Show full example 1 JSON"}`

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
        "dort"
      ]
    },
    {
      "valeur": "dort",
      "type": "GV",
      "debut": 8,
      "fin": 12,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "chat",
      "union": null,
      "candidats": [
        "structure la plus proche"
      ]
    }
  ],
  "phrase": [
    {
      "type": "ty
… [132 caractères tronqués]
  ```

- **bash** `{"command": "cat /tmp/j111/ex3.json", "description": "Show full example 3 JSON"}`

  ```
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
  ],
  "synta
… [786 caractères tronqués]
  ```

- **bash** `{"command": "cat /tmp/j111/ex5.json", "description": "Show full example 5 JSON"}`

  ```
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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '1,150p' docs/pilotage/en-cours.md", "description": "Read current state file"}`

  ```
# En ce moment

**Mis à jour : 2026-11-14, 04 h 20 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 11** : serveurs loca
… [10949 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nls .git/hooks | head -20; ls tools | grep -i \"etat\\|hook\"", "description": "List hooks and state tools"}`

  ```
applypatch-msg.sample
commit-msg.sample
fsmonitor-watchman.sample
post-update.sample
pre-applypatch.sample
pre-commit
pre-commit.sample
pre-merge-commit.sample
prepare-commit-msg.sample
pre-push.sample
pre-rebase.sample
pre-receive.sample
push-to-checkout.sample
sendemail-validate.sample
update.sample
compare_etats.py
etat_de_plan.py
etats_sans_langue.py
greffe_etat.sh
hooks
installe_hooks.sh
langue_dans_etat.py
langue_dans_etat_v1_fautif.py
lecture_etat.py
porte-etat.sh
predictibilite_etats.py
verifie_etat_a_jour.py
verifier_chaine_etat.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit diff --stat; git diff -- tools/chantier/plan.json | head -40", "description": "Inspect worktree modifications"}`

  ```
journal/README.md                                  |   5 +-
 journal/sessions/MANIFEST.md                       |   7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  65 ++
 .../rapport.md                                     |  20 +-
 .../digest.md                                      | 146 ++++
 .../rapport.md                                     |  52 +-
 reports/INDEX.md                                   |   4 +-
 reports/pensee-coherence-fiches-v7.json            |  19 +
 reports/pensee-dev-test-v10.json                   |   2 +-
 reports/pensee-quatre-modes.json                   | 734 ++++++++++++---------
 reports/rapport-audit-v7.md                        |   6 +-
 reports/rapport-coherence-fiches-v7.md             |  17 +-
 reports/rapport-dev-test-v10.md                    |   2 +-
 reports/rapport-pensee-v12.md                      |   4 +-
 reports/rapport-spans-chunker.md                   |  13 +-
 tools/chantier/plan.json                           | 116 ++++
 tools/structures                                   |   0
 17 files changed, 852 insertions(+), 360 deletions(-)
diff --git a/tools/chantier/plan.json b/tools/chantier/plan.json
index 21ea0cf4..b1ece0d6 
… [1373 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '1,120p' .git/hooks/pre-commit", "description": "Read pre-commit hook"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '1,120p' tools/verifie_etat_a_jour.py", "description": "Read state check tool"}`

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
… [3540 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ncat tools/porte-produit.sh", "description": "Read product gate"}`

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
… [3266 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\njq '.heuristique.pos | {exactitude, exactitude_ferme, exactitude_ouvert, tokens}' /tmp/j111/eval-vivant.json\njq '.heuristique.pos | {exactitude, exactitude_ferme, exactitude_ouvert, tokens}' /tmp/j111/eval.json", "description": "Check … [24 caractères tronqués]`

  ```
{
  "exactitude": 0.8625,
  "exactitude_ferme": 0.9373,
  "exactitude_ouvert": 0.7918,
  "tokens": 3179
}
{
  "exactitude": 0.8625,
  "exactitude_ferme": 0.9373,
  "exactitude_ouvert": 0.7914,
  "tokens": 3141
}
  ```

- **todo_write** `{"todos": [{"content": "Rejouer les 5 blocs et collecter les sorties courantes", "status": "completed"}, {"content": "Corriger docs/produit/exemples.md (sorties + commentaires)", "status": "in_progress"}, {"content": "Écrire reports/rapport-exemples-rejoues.md + JSON", "status": "pending"}, {"conten … [149 caractères tronqués]`

  ```
Updated todo list: 3 pending, 1 in progress, 1 completed.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "old_string": "> **Ce que ce document est.** Cinq exécutions **réelles** du produit, avec leur JSON commenté. Il\n> complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit\n> *comment lire* ce qui sort. Les sorties ont été p … [1600 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "```\ndrave 0.1.0 — analyse heuristique (CPU, hors ligne)\nlangue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VERB ./PONCT\nSYNTAGMES\n  GN   [0:7]   Le chat  rôle=agent  … [935 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "```json\n{\n  \"langue\": \"fr\",\n  \"script\": \"Latn\",\n  \"refus\": \"\",\n  \"pos\": [\n    {\n      \"valeur\": \"Le\",\n      \"type\": \"DET\",\n      \"debut\": 0,\n      \"fin\": 2,\n      \"confiance\": 0.92,\n      \"ouvert\": fal … [2779 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "- `langue: fr`, `script: Latn`, `refus: \"\"` : le texte est accepté.\n- Quatre POS : `Le/DET`, `chat/NOUN`, `dort/VERB` et `.`/`PONCT` (0,95). `chat` et `dort` sont\n  **ouverts** (confiance 0,3 et 0,72) : le lexique ne les connaît pas comme  … [994 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "- `REL « que j'ai lu est intéressant » [9:36] → livre` avec **`union: true`** : c'est la **seconde\n  lecture d'union**, un **doublon REL** qui chevauche la première. La sortie lisible du CLI ne\n  montre pas `union` : elle affiche deux REL, e … [1745 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "    {\n      \"valeur\": \"left\",\n      \"type\": \"VERB\",\n      \"debut\": 16,\n      \"fin\": 20,\n      \"confiance\": 0.85,\n      \"ouvert\": true\n    },\n    {\n      \"valeur\": \"was\",\n      \"type\": \"AUX\",\n      \"debut\":  … [942 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "- `when` est tagué **CONJ** par le POS, mais il déclenche une **REL** `[8:20] « when we left »`\n  → `day` : c'est la correction `AMBIGUES_REL` de la v12 (« when » après un GN = relative ;\n  ailleurs, subordonnée). Sans elle, la REL était une … [1550 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "**Ce qu'il faut en conclure.** Le produit n'est pas monolingue : il analyse l'anglais et publie\nles mêmes champs. Mais une réussite d'attachement peut coexister avec des erreurs de POS ; les\ndeux mesures sont séparées (POS **0,8625** ; attac … [475 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '455,510p' docs/produit/exemples.md", "description": "View section 4 after edits"}`

  ```
]
}
```

**Lecture.**

- `when` est tagué **CONJ** par le POS, mais il déclenche une **REL** `[8:20] « when we left »`
  → `day` : c'est la correction `AMBIGUES_REL` de la v12 (« when » après un GN = relative ;
  ailleurs, subordonnée). Sans elle, la REL était une SUB et le span était perdu.
- `left` est désormais **VERB** (0,85) et `was` **AUX** ; le POS anglais n'est pas parfait pour
  autant (POS global **0,8625**, ouvert **0,7918**). L'attachement juste et le POS imparfait
  continuent de coexister dans la même sortie.
- `beautiful` est **ADJ**, `The day` **GN**, `was beautiful` **GV** : la segmentation est
  complète. La ponctuation finale sort en **PONCT** depuis le correctif de ponctuation.
- L'attachement `REL → day` est celui du gold ; c'est le **87/87 labels** anglais (88 cibles ;
  `g017` est la seule cible sans span prédit).
- `GV « was beautiful »` a `cible: null` : le bloc ne publie pas d'attachement pour ce GV. `null`
  veut dire « pas de cible publiée », pas « pas de relation ».

**Ce qu'il faut en conclure.** Le produit n'est pas monolingue : il analyse l'anglais et publie
les mêmes champs. Mais une réussite d'attachement peut coexister avec des erreurs de POS ; le
… [830 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '510,540p' docs/produit/exemples.md", "description": "View rest of section 4"}`

  ```
"langue": "und",
  "script": "Zyyy",
  "refus": "vide",
  "etiquettes": 0
}
```

**Lecture.**

- `refus: "vide"` : le bloc **refuse** au lieu d'inventer une analyse.
- `langue: und`, `script: Zyyy` : rien à détecter.
- Zéro étiquette, zéro unité, fraction 0.
- **Le CLI, lui, sort 1 et ne rend pas l'annotation** : un pipeline qui veut le JSON de refus doit
  passer par le bloc. Le contrat cible (code **3** + JSON sur `stdout`) n'est pas implémenté
  (notice § 7).

**Ce qu'il faut en conclure.** Un pipeline doit traiter `refus` comme un état de première classe :
un texte vide ne produit pas une annotation vide « comme les autres ». Aujourd'hui, le CLI le
traite comme une erreur ; l'API le dit dans le JSON. C'est une garantie de non-invention, pas un
bug.

## 5. L'échec connu — un span non prédit (`r035`)

**Entrée.** `The film she talks about is out.` (phrase `reel` du gold, `r035`).

**Le gold attend** (extrait de `tools/tests/linguistique/gold_reel.json`) :

```json
{
  "type": "REL",
  "texte": "she talks about",
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "```\ndrave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)\nexit=3\n```\n\nSans `--json`, le CLI écrit sur `stderr` et sort **3**. Avec `--json`, il écrit l'annotation de\nrefus sur `stdout` (`schema: \"drave … [525 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "- `refus: \"vide\"` : le bloc **refuse** au lieu d'inventer une analyse.\n- `langue: und`, `script: Zyyy` : rien à détecter.\n- Zéro étiquette, zéro unité, fraction 0.\n- **Le CLI sort 3** ; avec `--json`, il rend le même JSON de refus. Le con … [1065 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '533,660p' docs/produit/exemples.md", "description": "View section 5 full"}`

  ```
**Entrée.** `The film she talks about is out.` (phrase `reel` du gold, `r035`).

**Le gold attend** (extrait de `tools/tests/linguistique/gold_reel.json`) :

```json
{
  "type": "REL",
  "texte": "she talks about",
  "debut": 9,
  "fin": 24,
  "cible": "film"
}
```

**Commande.**

```bash
python3 tools/drave.py analyser "The film she talks about is out." --json \
  | jq '{langue, script, refus,
         syntagmes: [.etiquettes[] | select(.niveau=="syntagme")
           | {valeur, type, debut, fin, confiance, role:.meta.role,
              cible:.meta.attachement.cible, union:.meta.union, candidats}],
         phrase: [.etiquettes[] | select(.niveau=="phrase") | {type, valeur}],
         pragmatique: [.etiquettes[] | select(.niveau=="pragmatique") | {type, valeur}]}'
```

**Sortie (réelle).**

```json
{
  "langue": "en",
  "script": "Latn",
  "refus": "",
  "syntagmes": [
    {
      "valeur": "The film she",
      "type": "GN",
      "debut": 0,
      "fin": 12,
      "confiance": 0.35,
      "role": "groupe nominal",
      "cible": "talks",
      "union": null,
      "candidats": [
        "GN",
        "talks",
        "out"
      ]
    },
    {
      "valeur": "talks",
      "ty
… [3160 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '526,535p' docs/produit/exemples.md", "description": "View section 5 title"}`

  ```
**Ce qu'il faut en conclure.** Un pipeline doit traiter `refus` comme un état de première classe :
un texte vide ne produit pas une annotation vide « comme les autres ». Le CLI et l'API le disent
dans le JSON et le code de sortie ; c'est une garantie de non-invention, pas un bug.

## 5. L'échec connu — un span non prédit (`r035`)

**Entrée.** `The film she talks about is out.` (phrase `reel` du gold, `r035`).

**Le gold attend** (extrait de `tools/tests/linguistique/gold_reel.json`) :
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "## 5. L'échec autrefois connu — `r035`, désormais prédit\n\n**Entrée.** `The film she talks about is out.` (phrase `reel` du gold, `r035`).\n\n> **Ce bloc était l'échec connu de la doc.** Il ne l'est plus : la règle de **relative zéro**\n> (J1 … [301 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "```json\n{\n  \"langue\": \"en\",\n  \"script\": \"Latn\",\n  \"refus\": \"\",\n  \"syntagmes\": [\n    {\n      \"valeur\": \"The film\",\n      \"type\": \"GN\",\n      \"debut\": 0,\n      \"fin\": 8,\n      \"confiance\": 0.35,\n      \"ro … [2149 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "**Lecture.**\n\n- Le bloc prédit exactement les trois spans du gold : `GN « The film » [0:8]`, `REL « she talks\n  about » [9:24] → film` et `GV « is out » [25:31]`. **La REL est là**, avec la cible attendue.\n- La relative est **sans marqueur … [2697 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "3. **Pas de couverture complète** : sur les **239 cibles d'attachement**, **238** ont un span\n   prédit (**0,9958**) ; la seule qui manque est `g017` (`SUB [9:28]`). `r035`, autrefois manqué,\n   est désormais prédit (§ 5).", "old_string": "3 … [141 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '650,700p' docs/produit/exemples.md", "description": "View section 7"}`

  ```
`g017` montre que la couverture n'est pas encore complète.

## 6. Ce que ces exemples ne montrent pas

1. **Pas de restitution, pas de traduction, pas de génération** : la sortie ne contient aucun
   texte produit ; seulement des étiquettes. Le produit ne réécrit pas la phrase.
2. **Pas de neuronal** : tout vient de `Heuristique` (CPU) ; `MockNeuronal` est un contrat, pas un
   tagger, et le CLI ne l'expose pas. La cascade 7B (0,9415) n'est pas un chemin livré.
3. **Pas de couverture complète** : sur les **239 cibles d'attachement**, **238** ont un span
   prédit (**0,9958**) ; la seule qui manque est `g017` (`SUB [9:28]`). `r035`, autrefois manqué,
   est désormais prédit (§ 5).
4. **Pas de lecture unique garantie** : le **doublon REL de l'union** (`union: true`) est publié ;
   il faut le filtrer si l'on veut un seul segment par span.
5. **Pas de valeurs normalisées** : `candidats` sont des chaînes et `role` n'est pas normalisé
   (`predicat`/`prédicat`). Le **format** est versionné (v2 ; v1 reste lue), mais le vocabulaire
   des valeurs, lui, n'a pas de schéma.

Pour mesurer sur votre propre corpus, il faut le format du gold (mots + segments + pragma) : il
n'est pas publié comme
… [883 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/produit/exemples.md", "new_string": "| **la notice d'usage** | [`README.md`](README.md) |\n| **le schéma du JSON (v2, v1)** | [`drave-annotation-v2.json`](../../tools/schemas/drave-annotation-v2.json) · [`drave-annotation-v1.json`](../../tools/schemas/drave-annotation-v1.json) |\ … [1348 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -rn \"0,9415\\|0.9415\" reports/*.md docs/**/*.md 2>/dev/null | head -10\ngrep -rn \"cascade 7B\" reports/*.md docs/**/*.md 2>/dev/null | head -10", "description": "Check cascade 7B number"}`

  ```
reports/INDEX.md:436:| [rapport-pensee-cascade-vrai-modele.md](rapport-pensee-cascade-vrai-modele.md) | B13 — la cascade complète avec le vrai modèle : POS 0,9415 / syntagmes 0,6130 / tête 0,7574 / acte 1,0 sur 180 phrases |
reports/INDEX.md:473:| [rapport-pensee-gold-cascade.md](rapport-pensee-gold-cascade.md) | B13 — la cascade complète : POS 0,9415, syntagmes 0,7539, acte 1,0 |
reports/rapport-pensee-cascade-vrai-modele.md:1:# B13 — la cascade complète avec le vrai modèle : POS 0,9415 / syntagmes 0,6130 / tête 0,7574 / acte 1,0 sur 180 phrases
reports/rapport-pensee-cascade-vrai-modele.md:6:> (latence médiane 6,6 s). POS **0,9415**, syntagmes F1 **0,6130** (précision 0,6066, rappel
reports/rapport-pensee-cascade-vrai-modele.md:36:| **cascade complète (all)** | **0,9415** | **0,6130** | **0,7574** | **1,0** |
reports/rapport-pensee-cascade-vrai-modele.md:40:- **POS** : 0,9415 (fermé 0,9392, ouvert 0,9432) — au-dessus de l'heuristique (0,7544) et du
reports/rapport-pensee-gold-cascade.md:1:# B13 — la cascade complète : POS 0,9415, syntagmes 0,7539, acte 1,0
reports/rapport-pensee-gold-cascade.md:4:> **Verdict** : ✅ **la cascade complète est mesurée** — POS **0,9415**, syntagmes ex
… [547 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"19 étiquettes\\|0,6234\\|0.6234\\|0,8383\\|235/236\\|237/238\\|0,9874\\|92,89\\|17 cibles\\|17 spans\\|exit=1\\|Aucune REL\" docs/produit/exemples.md", "description": "Scan for stale values in doc"}`

  ```
635:  sujet, verbe, préposition orpheline. C'était l'un des « 17 spans inatteignables » de la v12 ;
680:| **les 17 spans de la v12 (instantané)** | [`reports/rapport-pensee-v12.md`](../../reports/rapport-pensee-v12.md) |
  ```

- **bash** `{"command": "cat > /tmp/j111/verifier.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"Compare les blocs JSON de docs/produit/exemples.md aux sorties courantes.\"\"\"\nimport json, re, subprocess, sys, pathlib\n\nDOC = pathlib.Path(\"docs/produit/exemples.md\")\n\nFILTRE_POS = '''{langue, script, refus,\n p … [4172 caractères tronqués]`

  ```
OK    ex1
OK    ex2
OK    ex3
OK    ex4
OK    ex5
5/5 blocs identiques
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/exemples.md').read_text(encoding='utf-8')\n# mutation : remet left/NOUN dans le bloc JSON de l'exemple 3\nancien='''      \"valeur\": \"left\",\n      \"type\": \"VERB\", … [412 caractères tronqués]`

  ```
mutation écrite
OK    ex1
OK    ex2
ÉCART ex3
  .pos[4].type: 'NOUN' != 'VERB'
OK    ex4
OK    ex5
4/5 blocs identiques
code=1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"\" >/tmp/j111/ex4-cli-stdout.txt 2>/tmp/j111/ex4-cli-stderr.txt; c=$?; echo \"exit=$c\"; wc -c /tmp/j111/ex4-cli-stdout.txt; cat /tmp/j111/ex4-cli-stderr.txt\npython3 tools/drave.py analyser \"\" --jso … [221 caractères tronqués]`

  ```
exit=3
0 /tmp/j111/ex4-cli-stdout.txt
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
json exit=3
{
  "schema": "drave.annotation",
  "version": 2,
  "refus": "vide",
  "n": 0,
  "langue": "und",
  "script": "Zyyy"
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,re,subprocess,pathlib\nold=subprocess.run(['git','show','HEAD:docs/produit/exemples.md'],capture_output=True,text=True).stdout\nnew=pathlib.Path('docs/produit/exemples.md').read_text(encoding='utf-8')\ndef … [992 caractères tronqués]`

  ```
5 5
==== 1 CHANGÉ
  .pos: liste 3 -> 4
==== 2 identique
==== 3 CHANGÉ
  .pos: liste 7 -> 8
  .pos[4].confiance: 0.3 -> 0.85
  .pos[4].type: 'NOUN' -> 'VERB'
==== 4 identique
==== 5 CHANGÉ
  .syntagmes[0].candidats: liste 3 -> 2
  .syntagmes[0].candidats[1]: 'talks' -> 'out'
  .syntagmes[0].cible: 'talks' -> 'out'
  .syntagmes[0].fin: 12 -> 8
  .syntagmes[0].valeur: 'The film she' -> 'The film'
  .syntagmes[1].candidats: liste 1 -> 3
  .syntagmes[1].candidats[0]: 'GV' -> 'REL'
  .syntagmes[1].cible: None -> 'film'
  .syntagmes[1].debut: 13 -> 9
  .syntagmes[1].fin: 18 -> 24
  .syntagmes[1].role: 'prédicat' -> 'qualité'
  .syntagmes[1].type: 'GV' -> 'REL'
  .syntagmes[1].valeur: 'talks' -> 'she talks about'
  .syntagmes[2].debut: 19 -> 25
  .syntagmes[2].valeur: 'about is out' -> 'is out'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json, pathlib, subprocess\n\ndef load(p):\n    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))\n\nex1=load('/tmp/j111/ex1.json')\nex2=load('/tmp/j111/ex2.json')\nex3=load('/tmp/j111/ex3.json')\ne … [5158 caractères tronqués]`

  ```
écrit 7940
497 reports/rapport-exemples-rejoues.json
  ```

- **write** `{"file_path": "reports/rapport-exemples-rejoues.md", "content": "# J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec\n\n> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : **J11.1** · **Date** : 2026-11-14 ·\n> **Verdict** : ✅\n> **Cinq blocs rejou … [8953 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-rejoues.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit diff -- reports/INDEX.md | head -30", "description": "Inspect pending INDEX changes"}`

  ```
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 5506faf4..e5dd4473 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **718 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **719 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -669,6 +669,7 @@
 | [rapport-regle-placement-perte.md](rapport-regle-placement-perte.md) | A8.3 — la règle place et perte choisit le KV comme la main |
 | [rapport-replis-cible.md](rapport-replis-cible.md) | B13 — les trois retouches A3 sur le live : +1, +2, +1, et 145/145 exact/top1 |
 | [rapport-restitution-v0.md](rapport-restitution-v0.md) | B13 — la restitution v0 : 46/46 surfaces exactes, le miroir strict à 0,1087 |
+| [rapport-restitution-v1.md](rapport-restitution-v1.md) | B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087 |
 | [rapport-restitution.md](rapport-restitution.md) | B18 — restitution canonique : 528/528, mais pas un décodeur |
 | [rapport-retrieval-epoque.md]
… [1321 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/index_reports.py >/tmp/j111/index.log 2>&1; echo \"exit=$?\"; tail -5 /tmp/j111/index.log\ngit diff --stat -- reports/INDEX.md; git diff -- reports/INDEX.md | head -40", "description": "Regenerate reports index"}`

  ```
exit=0
  722 fiches → reports/INDEX.md
 reports/INDEX.md | 7 ++++++-
 1 file changed, 6 insertions(+), 1 deletion(-)
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
+| [rapport-bilan-chantier.md](rapport-bilan-chantier.m
… [3192 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"J11\\|J10.1\\|B13\" docs/pilotage/roadmap.md | head -20", "description": "Find B13/J11 in roadmap"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [8561 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '48,64p' docs/pilotage/roadmap.md", "description": "Read roadmap suite section"}`

  ```
**S** : **54/55** types, **131/131** rôles, **47/47** compléments, gold **55**. **D/R/A** close (OCR
CEGEP **91 scans uniques**, 1 982 p). **Passe** : 81 portes, **76/5**, 1 h 52 ; la **82e**
(`porte-ressources`) est validée ; compteurs **574 fiches / 660 JSON**.

**J3.2** : les deux faces ne mesurent pas le même objet — Panini §150 est une distance de tradition (3/655 paires inter-langues), sa fonction `lang_distance` couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au hasard exact, le signal de famille vit dans 2-3 paires ; la face atomes n'est pas disponible (V14 3/21) ([fiche](../../reports/rapport-genealogie-deux-faces.md)).

**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard 2,5 %), mais **hors écriture tout est au hasard** ; sur les 25 langues LANG_TREE, les sœurs valent **0,619** contre **0,0445** pour les familles différentes (**13,9×**, coefficient **+0,448**, p=0,002, 11/11 langues positives), alors que l'échantillon 20 ne montre **aucun** contraste de sœur (0,058 vs 0,039, p=
… [1134 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run documentation review"}`

  ```
revue de documentation · 725 fiche(s) · 819 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 724 fichiers, le disque en a 725
     · compteurs : en-cours.md dit 818 JSON, le disque en a 819
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Get current time"}`

  ```
2026-11-14 04:21 EST
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **J10.1 — le bilan** : **20/21** ; F1 **0,7533 → 0,7902**, attachement **236 → 238 labels**, POS inchangée ; **5 timeouts**, **1 échec** (J5.2, tag absent) ; **D1–D20**, **R1–R30** ; [bilan](../../reports/rapport-bilan-chantier.md) + JSON.\ … [543 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "offset": 100, "limit": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
100: > Vérifié par `tools/revue_documentation.py`.
101: 
102: | invariant | valeur | contrôle |
103: |---|---|---|
104: | portes | **84** (dont `porte-produit` le 07/11) | `tools/porte-*.sh` |
105: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
106: | fichiers / JSON de résultats | **724** / **818** | `reports/*.md` / `reports/*.json` |
107: | documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
108: | dernière passe | **14/11 00 h 30** (84, **81/3**) ; rouges tolérées `indice`, `melange`, `sessions` | `docs/pilotage/references-non-regression.md` |
109: 
110: ## Les chantiers et leurs bloquants
111: 
112: **Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
113: externes** et la **prochaine action**.
114: 
115: | chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
116: |---|---|---|---|
117: | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8
… [2275 caractères tronqués]
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "limit": 25, "offset": 74}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
74: - **Rôle** : **N2** — la production et la capacité.
75: - **Plan** : fenêtre.
76: - **Ambition** : la longueur et la capacité.
77: - **Stratégie** : budgets contrôlés, mêmes bancs.
78: - **Objectif final** : la production qui tient.
79: - **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondération) ; `kd2` et `rope2048` **arrêtés** ; **paire propre** : **3,1500** → **3,1119** (−0,06 ; −0,19 anglais) ; **repondération : −0,05** ; **2 048** ne bat pas 1 024 ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [production](../../reports/rapport-n2-production-fenetre.md), [erratum](../../reports/rapport-n2-distillation-native.md), [porte](../../reports/rapport-n2-porte-propre.md).
80: - **Ce que font les autres** : **hub**, **S**, **Pensée**.
81: - **Prochaine action** : la **porte propre (0,29)** ; le **2 048** est fini.
82: - **Bloquants** : aucun.
83: - **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).
84: 
85: ## Ce qui est en cours
86: 

… [2753 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "old_string": "- **J10.1 — le bilan** : **20/21** ; F1 **0,7533 → 0,7902**, attachement **236 → 238 labels**, POS inchangée ; **5 timeouts**, **1 échec** (J5.2, tag absent) ; **D1–D20**, **R1–R30** ; [bilan](../../reports/rapport-bilan-chantier.md) + JSON." … [543 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **725** / **819** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **724** / **818** | `reports/*.md` / `reports/*.json` |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1 (exemples r … [444 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — 11 verdicts + pointeur ; **R0.7** — split réel ; **A** — A6.2, A8.3b2 ; **J14.1** — passe  … [356 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-14, 04 h 25 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-14, 04 h 20 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"Fait.*B13\" docs/pilotage/en-cours.md", "description": "Locate Pensée Fait line"}`

  ```
63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **contrat v1**, **`drave` v0**.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **co … [885 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "new_string": "[`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON.\n\n**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits\navec le code courant ; **4 sont corrigés** : la ponctuation fina … [685 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "docs/pilotage/roadmap.md", "limit": 14, "offset": 56}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
56: **J10.1 — le bilan du chantier.** **20 tâches sur 21** passent l'acceptation ; **5 timeouts**
57: (J1.2, J2.2, J3.1, J5.2, J8.1), dont **4 récupérés** par une acceptation verte ou le commit de la
58: tâche suivante, et **1 vrai échec** (J5.2, le tag absent). Le produit gagne **2 attachements**
59: (236 → 238 labels) et **+0,0369 de F1** (0,7533 → 0,7902), la POS ne bouge pas ; Panini est
60: **mesuré et borné** (table 14/14, corpus 418/438, retrieval J3.1, généalogie J3.2, familles
61: J7.1) ; la coordination N2/S/R/A est **datée**. La **clôture formelle** reste à faire : **J14.1**
62: doit refaire la passe et poser le tag `chantier-2026-11-14`. Le détail — chiffres, décisions
63: D1–D20, rejets R1–R30, échecs, reste — est dans
64: [`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON.
65: 
66: **La vue d'ensemble des chantiers** — huit chantiers (A, B, N, R, **S**, **L**, **D**, B13), leurs relations, leurs chemins critiques et les tensions à trancher — est dans [`chantiers.md`](chantiers.md) ; la carte est [`chantiers-vision.svg`](../schema
… [327 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "new_string": "[`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON.\n\n**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits\navec le code courant ; **4 sont corrigés** : la ponctuation fina … [685 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/revue_documentation.py 2>&1 | tail -20\necho \"=== liens\"\npython3 tools/verifier_liens.py 2>&1 | tail -20", "description": "Run doc review and link check"}`

  ```
revue de documentation · 725 fiche(s) · 819 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== liens
  ✅ 4116 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/verifie_en_cours.py 2>&1 | tail -20\necho \"=== taille\"\npython3 tools/taille_documents.py 2>&1 | tail -15", "description": "Check state and document size"}`

  ```
en-cours · 1677 mots · 7 sections · 4 session(s) · 11 puces · 5 questions
  ❌ 1 anomalie(s) :
     · 11 puces dans « Ce qui est en cours » > 10
=== taille
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4047 mots (budget 4 000)

  avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4047 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "limit": 7, "offset": 93}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
93: - **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002), échantillon 20 nul ; J3.1 reproduit ; [fiche](../../reports/rapport-retrieval-familles.md).
94: - **J5.1** : rapport de semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets**) ; [rapport](../../reports/rapport-semaine.md) + JSON.
95: - **J10.1 — le bilan** : **20/21** ; F1 **0,7533 → 0,7902**, attachement **236 → 238 labels**, POS inchangée ; **5 timeouts**, **1 échec** (J5.2, tag absent) ; **D1–D20**, **R1–R30** ; [bilan](../../reports/rapport-bilan-chantier.md) + JSON.
96: - **J11.1 — les exemples rejoués** : **5/5** blocs reproduits, **4 corrigés** ; `r035` désormais prédit (`REL [9:24] → film`), refus code **3**, `./PONCT` ; F1 **0,7902**, attachement **238/238 labels** (238/239, 0,9958) ; [fiche](../../reports/rapport-exemples-rejoues.md) + JSON.
97: - **Coordination J4** : N2 **2,9726/2,7856** ; S **7/4** ; R **0,9475 (+8,49)
… [312 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **J5.1 / J10.1 — les bilans** : semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets** ; [rapport](../../reports/rapport-semaine.md)) ; chantier (**20/21**, attachement **236 → 238 labels**, **5 timeouts**, **1  … [535 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '92,98p' docs/pilotage/en-cours.md", "description": "Check merged bullet"}`

  ```
- **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significative ; **J3.2** : `lang_distance` couvre **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, la famille vit dans **2-3 paires**, **V14 : 3/21** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-faces.md).
- **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002), échantillon 20 nul ; J3.1 reproduit ; [fiche](../../reports/rapport-retrieval-familles.md).
- **J5.1 / J10.1 — les bilans** : semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets** ; [rapport](../../reports/rapport-semaine.md)) ; chantier (**20/21**, attachement **236 → 238 labels**, **5 timeouts**, **1 échec** (J5.2, tag absent), **D1–D20**, **R1–R30** ; [bilan](../../reports/rapport-bilan-chantier.md)) + JSON.
- **J11.1 — les exemples rejoués**
… [559 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/verifie_en_cours.py 2>&1 | tail -10\npython3 tools/taille_documents.py 2>&1 | tail -6", "description": "Recheck state and size"}`

  ```
en-cours · 1665 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4035 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **J5.1 / J10.1 — les bilans** : semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets** ; [rapport](../../reports/rapport-semaine.md)) ; chantier (**20/21**, attachement **236 → 238 labels**, **5 timeouts**, **1  … [990 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/taille_documents.py 2>&1 | tail -5", "description": "Recheck T0 size"}`

  ```
avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4027 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nfrom pathlib import Path\nt=Path('docs/pilotage/en-cours.md').read_text(encoding='utf-8')\nfor i,line in enumerate(t.splitlines(),1):\n    if line.startswith('### ') or line.startswith('- **'):\n        print(len(line … [72 caractères tronqués]`

  ```
10 8 ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
6 10 - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7
11 11 - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
17 12 - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tab
12 13 - **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
4 14 - **Bloquants** : aucun.
5 15 - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/)
12 26 ### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise *
6 28 - **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536
16 29 - **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après rebo
4 30 - **Plan** : état.
4 31 - **Ambition** : reprise.
4 32 - **Stratégie** : flux.
5 33 - **Objectif final** : zéro.
10 34 - **Ce qu'elle fait** : intégration ; passe **82, 80/2**.
10 35 - **Ce que font les autres** : **N2**, **S**, **Pensée**.
16 36 - **Prochaine action** : reprise par le hub `1e7ef596` ; l'état du 04/11 est la source.
4 37 - **Bloq
… [4330 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **J11.1** : **5/5** exemples reproduits, **4 corrigés** ; `r035` prédit, refus code **3** ; F1 **0,7902**, attachement **238/238** (238/239) ; [fiche](../../reports/rapport-exemples-rejoues.md) + JSON.", "old_string": "- **J11.1 — exemples  … [216 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\nt=p.read_text(encoding='utf-8')\nold='- **N3 — clos** : 17 portes vertes ; inventaire exécutable (5/5) ; deux conditions nommées ; [fiche](../../reports/r … [292 caractères tronqués]`

  ```
N3 retiré de « en cours »
  avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4003 mots (AGENTS + en-cours + une tâche) > budget 4 000
  en-cours · 1633 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **J11.1** : **5/5** blocs, **4 corrigés** ; `r035` prédit, refus **3** ; F1 **0,7902**, attachement **238/238** (238/239) ; [fiche](../../reports/rapport-exemples-rejoues.md) + JSON.", "old_string": "- **J11.1** : **5/5** exemples reproduit … [165 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "limit": 4, "offset": 94}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
94: - **J11.1** : **5/5** exemples reproduits, **4 corrigés** ; `r035` prédit, refus code **3** ; F1 **0,7902**, attachement **238/238** (238/239) ; [fiche](../../reports/rapport-exemples-rejoues.md) + JSON.
95: - **Coordination J4** : N2 **2,9726/2,7856** ; S **7/4** ; R **0,9475 (+8,49)** ; A6.2 **libre** ; [N2](../../reports/rapport-coordination-n2.md), [S](../../reports/rapport-coordination-s.md), [R](../../reports/rapport-coordination-r.md), [A](../../reports/rapport-coordination-a.md).
96: 
97: ## Les chiffres de l'état

(Showing lines 94-97 of 143. Use offset=98 to continue.)
</content>
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **J11.1** : **5/5** blocs, **4 corrigés** ; `r035` prédit, refus **3** ; F1 **0,7902**, attachement **238/238** (238/239) ; [fiche](../../reports/rapport-exemples-rejoues.md) + JSON.", "old_string": "- **J11.1** : **5/5** exemples reproduit … [165 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/taille_documents.py 2>&1 | tail -4\npython3 tools/revue_documentation.py 2>&1 | tail -4", "description": "Recheck size and doc review"}`

  ```
· 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4001 mots (AGENTS + en-cours + une tâche) > budget 4 000
  revue de documentation · 725 fiche(s) · 819 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **J11.1** : **5/5**, **4 corrigés** ; `r035` prédit, refus **3** ; F1 **0,7902**, attachement **238/238** (238/239) ; [fiche](../../reports/rapport-exemples-rejoues.md) + JSON.", "old_string": "- **J11.1** : **5/5** blocs, **4 corrigés** ;  … [140 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/taille_documents.py 2>&1 | tail -4", "description": "Recheck T0"}`

  ```
avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nbash tools/porte-produit.sh > /tmp/j111/porte-produit.log 2>&1; echo \"EXIT=$?\"; tail -3 /tmp/j111/porte-produit.log", "description": "Run product gate", "run_in_background": true}`

  ```
started background job bash-78
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nbash tools/porte-tableaux.sh 2>&1 | tail -5\npython3 tools/verifier_schemas.py 2>&1 | tail -5", "description": "Run table and schema gates"}`

  ```
✅ 1790 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4116 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
  schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 /tmp/j111/verifier.py; echo \"code=$?\"\npython3 /tmp/j111/verifier.py /tmp/j111/exemples-mute.md >/tmp/j111/mute.out 2>&1; echo \"muté code=$?\"; cat /tmp/j111/mute.out", "description": "Re-run doc comparison and negative cont … [5 caractères tronqués]`

  ```
OK    ex1
OK    ex2
OK    ex3
OK    ex4
OK    ex5
5/5 blocs identiques
code=0
muté code=1
OK    ex1
OK    ex2
ÉCART ex3
  .pos[4].type: 'NOUN' != 'VERB'
OK    ex4
OK    ex5
4/5 blocs identiques
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit status --short | head -40", "description": "Show current git status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/exemples.md
MM journal/2026-11-14/README.md
MM journal/2026-11-14/docs.md
MM journal/2026-11-14/memoire.md
MM journal/2026-11-14/mesures.md
MM journal/2026-11-14/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
D  journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/digest.md
D  journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/rapport.md
MM journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/digest.md
MM journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/rapport.md
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
?? journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/
?? reports/rapport-
… [96 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit diff --cached --stat | tail -30", "description": "Show staged changes"}`

  ```
journal/2026-11-14/README.md                       |    7 +-
 journal/2026-11-14/docs.md                         |    2 +-
 journal/2026-11-14/memoire.md                      |    2 +-
 journal/2026-11-14/mesures.md                      |    8 +-
 journal/2026-11-14/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/THEMES.md                                  |    2 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   65 --
 .../rapport.md                                     |   20 +-
 .../digest.md                                      | 1035 --------------------
 .../rapport.md                                     |  122 ---
 .../digest.md                                      |  146 ---
 .../rapport.md                                     |   52 +-
 14 files changed, 32 insertions(+), 1443 deletions(-)
  ```

- **job_output** `{"job_id": "bash-78"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -20 /tmp/j111/porte-produit.log 2>/dev/null; echo \"---\"; ps -o pid,etime,cmd -C python3 | tail -10", "description": "Check gate progress"}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 16 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
---
    PID     ELAPSED CMD
   3002 10-08:49:12 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
2234057       06:53 python3 tools/chantier/superviseur.py boucle --budget 43200 --timeout 5400
2239911       00:11 python3 tools/tests/test_restitution.py
3555423  7-08:38:54 python3 src/app.py --no-browser
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 -c \"import json; d=json.load(open('reports/rapport-exemples-rejoues.json')); print(d['tache'], d['head'][:12], len(d['blocs']), d['mesure']['syntagmes']['f1'])\"\ngrep -n \"03ecee\\|0,7902\\|238/238\\|238/239\" reports/rapport … [84 caractères tronqués]`

  ```
J11.1 a6808c5edf74 5 0.7902
8:> **Le chiffre.** F1 syntagmes **0,7902** ; POS **0,8625** (fermé 0,9373, ouvert 0,7918) ;
9:> attachement **238/238 labels** (238/239 cibles, **0,9958**). Le mandat porte encore **237/238** :
97:Conséquence sur les chiffres : l'exactitude d'attachement est **238/238 labels = 1,0000**, mais
98:elle reste **conditionnelle aux spans prédits** ; la couverture est **238/239 = 0,9958**. Le seul
115:| F1 syntagmes | **0,7902** | précision 0,7860 · rappel 0,7944 |
118:| attachement exact / labels | **238/238** | 1,0000 conditionnel |
119:| couverture (cibles) | **238/239 = 0,9958** | `g017` manquante |
124:une **cible** sans toucher un span, donc **238/238 labels** et **F1 0,7902 inchangé**. Écrire
144:1. **Le rejeu est daté.** Les sorties valent pour `03ecee413cb05cf906d623765443d98d317e7f59` et le
155:   est 238/238 labels (238/239 cibles). Un rapport qui recopie le mandat se trompe.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit log --oneline -3; git rev-parse HEAD; date '+%Y-%m-%d %H:%M %Z'", "description": "Check HEAD moved"}`

  ```
a6808c5e CHANTIER — LE PLAN EST RELU À CHAQUE TOUR (LA BOUCLE VOYAIT UNE FILE VIDE APRÈS UN AJOUT DE TÂCHES) ; ÉTAT HORODATÉ
03ecee41 J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ
81fc9ecf JOURNAL — 2026-11-14 : J9.1 AU RÉCIT (19 FICHES « INSTANTANÉ HISTORIQUE »)
a6808c5edf741ea59d45602fdfeee0916488beaf
2026-11-14 04:23 EST
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit show --stat --oneline a6808c5 | head -20; git show --name-only --format='' a6808c5 | head", "description": "Inspect supervisor commit"}`

  ```
a6808c5e CHANTIER — LE PLAN EST RELU À CHAQUE TOUR (LA BOUCLE VOYAIT UNE FILE VIDE APRÈS UN AJOUT DE TÂCHES) ; ÉTAT HORODATÉ
 docs/pilotage/en-cours.md                          |    2 +-
 journal/2026-11-14/README.md                       |    7 +-
 journal/2026-11-14/docs.md                         |    2 +-
 journal/2026-11-14/memoire.md                      |    2 +-
 journal/2026-11-14/mesures.md                      |    8 +-
 journal/2026-11-14/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/THEMES.md                                  |    2 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   65 ++
 .../rapport.md                                     |   20 +-
 .../digest.md                                      | 1035 ++++++++++++++++++++
 .../rapport.md                                     |  122 +++
 .../digest.md                                      |  146 +++
 .../rapport.md                                     |   52 +-
 tools/chantier/superviseur.py                      |    4 +-
 16 files changed, 1447 insertions(+), 34 deletions(-)
docs/pil
… [291 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit show a6808c5 -- docs/pilotage/en-cours.md | head -40\necho ===\ngrep -n \"J11.1\\|725\\|819\" docs/pilotage/en-cours.md | head", "description": "Check whether en-cours changes survived"}`

  ```
commit a6808c5edf741ea59d45602fdfeee0916488beaf
Author: Stéphane <stephane@localhost>
Date:   Sat Nov 14 04:16:57 2026 -0500

    CHANTIER — LE PLAN EST RELU À CHAQUE TOUR (LA BOUCLE VOYAIT UNE FILE VIDE APRÈS UN AJOUT DE TÂCHES) ; ÉTAT HORODATÉ

diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 20210fd7..18874984 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-14, 03 h 55 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-14, 04 h 20 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
===
63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1** (5/5 b
… [743 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json, pathlib, subprocess\np=pathlib.Path('reports/rapport-exemples-rejoues.json')\nd=json.loads(p.read_text(encoding='utf-8'))\nd['head_rejeu']='03ecee413cb05cf906d623765443d98d317e7f59'\nd['head_rapport']=sub … [495 caractères tronqués]`

  ```
03ecee41 a6808c5e
  ```

- **edit** `{"file_path": "reports/rapport-exemples-rejoues.md", "new_string": "1. **Le rejeu est daté.** Les sorties valent pour le code de\n   `03ecee413cb05cf906d623765443d98d317e7f59` et le CLI 0.1.0 ; le HEAD du rapport est\n   `a6808c5edf741ea59d45602fdfeee0916488beaf` (commit superviseur, sans changement … [283 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-rejoues.md has been updated successfully.
  ```

- **job_output** `{"job_id": "bash-78"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -8 /tmp/j111/porte-produit.log; ps -o pid,etime,cmd -C python3 | grep -E \"autotest|test_produit|test_schema|restitution\" | head", "description": "Check gate progress again"}`

  ```
✅ smoke test : Ran 16 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
2240069       00:20 python3 -m tools.pensee.autotest
2240070       00:20 python3 -m tools.pensee.autotest
2240071       00:20 python3 -m tools.pensee.autotest
2240072       00:20 python3 -m tools.pensee.autotest
2240073       00:20 python3 -m tools.pensee.autotest
2240074       00:20 python3 -m tools.pensee.autotest
2240075       00:20 python3 -m tools.pensee.autotest
2240076       00:20 python3 -m tools.pensee.autotest
2240077       00:20 python3 -m tools.pensee.autotest
  ```

- **bash** `{"command": "sleep 20; tail -4 /tmp/j111/porte-produit.log", "description": "Wait and check gate log"}`

  ```
✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit diff --stat -- docs/produit/exemples.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/INDEX.md\necho ===\ngit diff -- docs/produit/exemples.md | head -120", "description": "Review doc diff"}`

  ```
docs/pilotage/en-cours.md |  15 +++--
 docs/pilotage/roadmap.md  |   9 +++
 docs/produit/exemples.md  | 151 +++++++++++++++++++++++++++++-----------------
 reports/INDEX.md          |   7 ++-
 4 files changed, 118 insertions(+), 64 deletions(-)
===
diff --git a/docs/produit/exemples.md b/docs/produit/exemples.md
index 005a463e..c4d2c3a6 100644
--- a/docs/produit/exemples.md
+++ b/docs/produit/exemples.md
@@ -3,10 +3,17 @@
 > **Ce que ce document est.** Cinq exécutions **réelles** du produit, avec leur JSON commenté. Il
 > complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
 > *comment lire* ce qui sort. Les sorties ont été produites le **2026-11-06** sur la branche
-> `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et sans réseau.
-> Le **format est passé en v2** le 07/11 : `version: 2` et, sur un syntagme qui chevauche un
-> autre, `meta.partition`/`meta.alternative` ; ces sorties v1 restent lisibles, v1 étant toujours
-> lue ([schéma v2](../../tools/schemas/drave-annotation-v2.json)).
+> `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et sans réseau ;
+> elles ont été **rejouées 
… [5493 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit diff -- docs/produit/exemples.md | sed -n '120,320p'", "description": "Review remaining doc diff"}`

  ```
-  le POS faux coexistent dans la même sortie.
+- `left` est désormais **VERB** (0,85) et `was` **AUX** ; le POS anglais n'est pas parfait pour
+  autant (POS global **0,8625**, ouvert **0,7918**). L'attachement juste et le POS imparfait
+  continuent de coexister dans la même sortie.
 - `beautiful` est **ADJ**, `The day` **GN**, `was beautiful` **GV** : la segmentation est
-  complète.
-- L'attachement `REL → day` est celui du gold ; c'est le **86/86** anglais de la fiche v12.
+  complète. La ponctuation finale sort en **PONCT** depuis le correctif de ponctuation.
+- L'attachement `REL → day` est celui du gold ; c'est le **87/87 labels** anglais (88 cibles ;
+  `g017` est la seule cible sans span prédit).
 - `GV « was beautiful »` a `cible: null` : le bloc ne publie pas d'attachement pour ce GV. `null`
   veut dire « pas de cible publiée », pas « pas de relation ».
 
 **Ce qu'il faut en conclure.** Le produit n'est pas monolingue : il analyse l'anglais et publie
 les mêmes champs. Mais une réussite d'attachement peut coexister avec des erreurs de POS ; les
-deux mesures sont séparées (POS **0,8383** ; attachement **235/236** conditionnel). Ne pas
-conclure « tout est bon » à parti
… [8534 caractères tronqués]
  ```

- **bash** `{"command": "sleep 30; tail -5 /tmp/j111/porte-produit.log", "description": "Wait for autotest"}`

  ```
✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C python3 | grep autotest | head -2; tail -c 200 /tmp/j111/porte-produit-autotest.log 2>/dev/null", "description": "Check autotest progress"}`

  ```
2240069       01:24 python3 -m tools.pensee.autotest
2240070       01:24 python3 -m tools.pensee.autotest
[exit code: 1]
  ```

- **bash** `{"command": "wc -l /tmp/j111/porte-produit-autotest.log; tail -30 /tmp/j111/porte-produit-autotest.log", "description": "Inspect autotest log"}`

  ```
[stderr]
wc: /tmp/j111/porte-produit-autotest.log: No such file or directory
tail: cannot open '/tmp/j111/porte-produit-autotest.log' for reading: No such file or directory
[exit code: 1]
  ```

- **bash** `{"command": "tail -20 /tmp/porte-produit-autotest.log 2>/dev/null; echo \"---\"; ps -o pid,etime,cmd -C python3 | grep autotest | head -2", "description": "Check actual autotest log"}`

  ```
---
2240069       01:29 python3 -m tools.pensee.autotest
2240070       01:29 python3 -m tools.pensee.autotest
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit diff -- reports/INDEX.md", "description": "Full INDEX diff"}`

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
… [4693 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"INDEX\\|index_reports\\|fiches\" tools/revue_documentation.py | head -30", "description": "Check index count validation"}`

  ```
5:  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
12:     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
93:    """Les fichiers dont les liens doivent résoudre (docs, fiches courantes, racine)."""
108:def compte_fiches() -> int:
176:    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
186:    if not fiches:
190:            (int(fiches.group(1)), compte_fiches(), "fichiers"),
191:            (int(fiches.group(2)), compte_json(), "JSON"),
261:    # 7b bis. les fiches glossaire sont toutes listées dans l'index du dossier
371:    print(f"  revue de documentation · {compte_fiches()} fiche(s) · {compte_json()} JSON · "
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '104,118p' tools/revue_documentation.py\ngrep -n \"INDEX\" tools/verifier_liens.py | head", "description": "Inspect fiche counter"}`

  ```
def compte_chapitres() -> int:
    return len(list((RACINE / "docs/theorie/synthese").glob("0*.md")))


def compte_fiches() -> int:
    return len(rapports())


def compte_json() -> int:
    return len(list((RACINE / "reports").glob("*.json")))


def compte_docs() -> int:
    return len(docs_vivants())
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"index\" tools/revue_documentation.py | head -20", "description": "Search index checks in review"}`

  ```
11:  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
163:            if f.name == "index.json" and f.parent.name == "glossaire":
170:        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")
261:    # 7b bis. les fiches glossaire sont toutes listées dans l'index du dossier
308:    idx = RACINE / "docs/theorie/synthese/index.md"
312:            alertes.append("cohérence : l'index ne dit pas « Huit chapitres »")
319:                alertes.append(f"cohérence : l'index ne mentionne pas {cible}")
326:                alertes.append(f"synthèse : {p.name} n'est pas listé dans l'index")
336:            alertes.append("synthèse : l'index n'a pas de « Dernière mise à jour »")
340:                alertes.append(f"synthèse : index daté {m.group(1)}, dernier changement {dernier}")
349:            alertes.append(f"synthèse : l'index ne dit pas « {forme} schémas » ({n} fichiers)")
  ```

- **bash** `{"command": "sleep 45; tail -4 /tmp/j111/porte-produit.log; ps -o pid,etime,cmd -C python3 | grep autotest | head -1", "description": "Wait for autotest completion"}`

  ```
✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
  ```

### 👤 Utilisateur

background job bash-78 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
bash tools/porte-produit.sh > /tmp/j111/porte-produit.log 2>&1; echo "EXIT=$?"; tail -3 /tmp/j111/porte-produit.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-78"}`

  ```
EXIT=0
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit log --oneline -2; git status --short | grep -E \"rapport-exemples|exemples.md|en-cours|roadmap|INDEX\"", "description": "Check HEAD and target files status"}`

  ```
a6808c5e CHANTIER — LE PLAN EST RELU À CHAQUE TOUR (LA BOUCLE VOYAIT UNE FILE VIDE APRÈS UN AJOUT DE TÂCHES) ; ÉTAT HORODATÉ
03ecee41 J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/exemples.md
 M reports/INDEX.md
?? reports/rapport-exemples-rejoues.json
?? reports/rapport-exemples-rejoues.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/verifie_en_cours.py 2>&1 | tail -3\npython3 tools/taille_documents.py 2>&1 | tail -2", "description": "Final state and size checks"}`

  ```
en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **todo_write** `{"todos": [{"content": "Rejouer les 5 blocs et collecter les sorties courantes", "status": "completed"}, {"content": "Corriger docs/produit/exemples.md (sorties + commentaires)", "status": "completed"}, {"content": "Écrire reports/rapport-exemples-rejoues.md + JSON", "status": "completed"}, {"conten … [155 caractères tronqués]`

  ```
Updated todo list: 0 pending, 1 in progress, 4 completed.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit add docs/produit/exemples.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-exemples-rejoues.md reports/rapport-exemples-rejoues.json\ngit diff --cached --stat", "description": "Stage J11.1 files"}`

  ```
docs/pilotage/en-cours.md                          |   15 +-
 docs/pilotage/roadmap.md                           |    9 +
 docs/produit/exemples.md                           |  151 +--
 journal/2026-11-14/README.md                       |    7 +-
 journal/2026-11-14/docs.md                         |    2 +-
 journal/2026-11-14/memoire.md                      |    2 +-
 journal/2026-11-14/mesures.md                      |    8 +-
 journal/2026-11-14/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/THEMES.md                                  |    2 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   65 --
 .../rapport.md                                     |   20 +-
 .../digest.md                                      | 1035 --------------------
 .../rapport.md                                     |  122 ---
 .../digest.md                                      |  146 ---
 .../rapport.md                                     |   52 +-
 reports/rapport-exemples-rejoues.json              |  500 ++++++++++
 reports/rapport-exemples-rejoues.md                |  17
… [62 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit commit --dry-run -- docs/produit/exemples.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-exemples-rejoues.md reports/rapport-exemples-rejoues.json 2>&1 | head -20", "description": "Dry-run commit with pathspe … [3 caractères tronqués]`

  ```
On branch s/v7
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   docs/pilotage/en-cours.md
	modified:   docs/pilotage/roadmap.md
	modified:   docs/produit/exemples.md
	new file:   reports/rapport-exemples-rejoues.json
	new file:   reports/rapport-exemples-rejoues.md

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
  (commit or discard the untracked or modified content in submodules)
	modified:   reports/INDEX.md
	modified:   reports/pensee-coherence-fiches-v7.json
	modified:   reports/pensee-dev-test-v10.json
	modified:   reports/pensee-quatre-modes.json
	modified:   reports/rapport-audit-v7.md
	modified:   reports/rapport-coherence-fiches-v7.md
	modified:   reports/rapport-dev-test-v10.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/verifie_etat_a_jour.py --index; echo \"exit=$?\"", "description": "Verify state accompanies facts"}`

  ```
✅ index : aucun fait stagé sans état
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit commit -- docs/produit/exemples.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-exemples-rejoues.md reports/rapport-exemples-rejoues.json <<'MSG'\nJ11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035  … [1190 caractères tronqués]`

  ```
[stderr]
  ✅ index : aucun fait stagé sans état
error: Terminal is dumb, but EDITOR unset
Please supply the message using either -m or -F option.
[exit code: 1]
  ```

- **bash** `{"command": "cat > /tmp/j111/commit-msg.txt <<'MSG'\nJ11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238\n\nLes 5 blocs de docs/produit/exemples.md sont rejoués sur le code courant\n(CLI drave 0.1.0, schéma v2) : 5/5 reproduits, 4 corrigés, … [1256 caractères tronqués]`

  ```
[s/v7 84e393bb] J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238
 16 files changed, 2970 insertions(+), 94 deletions(-)
 create mode 100644 reports/rapport-exemples-rejoues.json
 create mode 100644 reports/rapport-exemples-rejoues.md
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit show --stat --oneline HEAD | head -30", "description": "Inspect commit contents"}`

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
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit status --short | head -30\necho ===\ngit log --oneline -3", "description": "Check status after commit"}`

  ```
MM journal/2026-11-14/README.md
MM journal/2026-11-14/docs.md
MM journal/2026-11-14/memoire.md
MM journal/2026-11-14/mesures.md
MM journal/2026-11-14/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
D  journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/digest.md
D  journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/rapport.md
MM journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/digest.md
MM journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/rapport.md
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
?? journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/
?? reports/rapport-s-paragraphes.md
===
84e393bb J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉ
… [333 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit show HEAD:docs/pilotage/en-cours.md | grep -n \"J11.1\\|725\\|819\"\ngit show HEAD:reports/rapport-exemples-rejoues.md | head -5\ngit show HEAD:docs/produit/exemples.md | grep -n \"rejouées le 2026-11-14\\|r035.*désormais prédit\\| … [61 caractères tronqués]`

  ```
63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1** (5/5 blocs rejoués, 4 corrigés ; [fiche](../../reports/rapport-exemples-rejoues.md)) ; **contrat v1**, **`drave` v0**.
94:- **J11.1** : **5/5**, **4 corrigés** ; `r035` prédit, refus **3** ; F1 **0,7902**, attachement **238/238** (238/239) ; [fiche](../../reports/rapport-exemples-rejoues.md) + JSON.
105:| fichiers / JSON de résultats | **725** / **819** | `reports/*.md` / `reports/*.json` |
117:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1 (exemples rejoués)** | **J11.2–J11.4** (produit) ; **trancher `g017`** ; puis T132/T
… [794 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/verifie_etat_a_jour.py --head 2>&1 | tail -5\npython3 tools/revue_documentation.py 2>&1 | tail -3\npython3 tools/verifie_en_cours.py 2>&1 | tail -2", "description": "Final state and doc checks"}`

  ```
état · dernier fait 84e393bb · dernier état 84e393bb
  ✅ aucun fait commité après le dernier état
  revue de documentation · 725 fiche(s) · 819 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit status --short -- docs/produit/exemples.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-exemples-rejoues.md reports/rapport-exemples-rejoues.json; echo \"clean=$?\"", "description": "Confirm target files commi … [6 caractères tronqués]`

  ```
clean=0
  ```

- **todo_write** `{"todos": [{"content": "Rejouer les 5 blocs et collecter les sorties courantes", "status": "completed"}, {"content": "Corriger docs/produit/exemples.md (sorties + commentaires)", "status": "completed"}, {"content": "Écrire reports/rapport-exemples-rejoues.md + JSON", "status": "completed"}, {"conten … [153 caractères tronqués]`

  ```
Updated todo list: 0 pending, 0 in progress, 5 completed.
  ```

### 🤖 Assistant

**J11.1 terminé et committé** (`84e393bb`).

### Ce que le rejeu a montré

| bloc | verdict | changement |
|---|---|---|
| §1 `g001` | corrigé | **19 → 20 étiquettes**, `./PONCT`, couverture POS `0,92 → 0,95` |
| §2 `g011` | identique | v2 publie `meta.partition`/`meta.alternative` sur le groupe 0 |
| §3 `r241` | corrigé | `left` : `NOUN 0,3 → VERB 0,85`, `./PONCT` ajouté |
| §4 refus | corrigé | code de sortie **1 → 3** ; `--json` rend l'annotation de refus |
| §5 `r035` | corrigé | **l'ancien échec est désormais prédit** : `REL [9:24] « she talks about » → film` |

Le point important : **`r035` n'est plus un échec**. Il ne reste que `g017` comme cible sans span prédit.

### Chiffres courants

- F1 syntagmes **0,7902**
- POS **0,8625** (ouvert **0,7918**)
- attachement **238/238 labels** — **238/239 cibles**, couverture **0,9958**
- gold vivant : **612 phrases**, **3 179 tokens**, **239 cibles**

Le mandat disait `237/238` : c'est l'état d'avant `s065` (J6.2), qui a ajouté un label sans toucher un span.

### Contrôle négatif

Mutation d'un token dans une copie de la doc (`left/VERB → NOUN`) : le comparateur signale **4/5** et l'écart exact `.pos[4].type: 'NOUN' != 'VERB'`. Sur la doc réelle : **5/5**.

### Livrables

- [`docs/produit/exemples.md`](docs/produit/exemples.md) — 5 blocs corrigés, en-tête daté, §5 réécrit
- [`reports/rapport-exemples-rejoues.md`](reports/rapport-exemples-rejoues.md)
- [`reports/rapport-exemples-rejoues.json`](reports/rapport-exemples-rejoues.json)
- état [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) et roadmap mis à jour

### Portes

- `porte-produit` : **verte**, autotest **183/183**
- revue de documentation : **verte** (725 fiches / 819 JSON)
- liens, tableaux, schémas : **verts**
- `en-cours` : 1 630 mots, T0 dans le budget
- `verifie_etat_a_jour --head` : **aucun fait après le dernier état**

Note : `reports/INDEX.md` reste modifié dans l'arbre par le cycle concurrent (ligne `s-paragraphes` non committée) ; la ligne de cette fiche y figure déjà.

