# Session DSH — relecture

- identifiant : `7635f5f5-11b8-4d10-bea5-50a90e536e31`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 21:13:31
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier R** (le lecteur : R0.7 tagger, R1.2-1024, R44, R2/R3/R5) — lecture seule, aucun code.

Contexte : `docs/pilotage/roadmap.md` (R), `docs/pilotage/en-cours.md`, les fiches `reports/rapport-r*.md`, `tools/` (le tagger : `evaluer_tagger.py`? cherche), le modèle natif (`tools/native_model.py`), R1.2-1024 (documenté comme fait), R44 (10 scans, plus bloqué par l'OCR ?), la chaîne R2/R3/R5.

À faire :
1. **Inventaire** : chaque ligne R, son état (fait / bloqué / à faire), la commande qui la vérifie, le chiffre publié.
2. **Vérifie** R1.2-1024 et R44 : les chiffres, les artefacts, les fiches ; ce qui reste.
3. **Le tagger** : où est-il, quel POS mesure-t-il, sur quel corpus, quel est l'écart avec l'heuristique du bloc L (0,85 aujourd'hui).
4. **Propose** les 3 prochaines actions de R, mesurables.
5. Écris **uniquement** deux fichiers neufs : `reports/rapport-etat-r.md` et `reports/pensee-etat-r.json`.
6. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, natifs.

Rends un résumé : l'état de chaque ligne R, le tagger, les 3 prochaines actions.
Your parent agent id is "e181ce02-cd50-488a-a6be-e84b79d40dcc". Before you finish, send your result to that agent with send_message({ agent_id: "e181ce02-cd50-488a-a6be-e84b79d40dcc", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Inventaire du chantier R : lecture de la roadmap et de l'état courant

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --short --branch | head -20; echo '---'; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet log --oneline -5", "description": "Vérifier branche et état git"}`

  ```
## s/v7
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/2026-11-06/README.md
D  journal/2026-11-06/distribue.md
D  journal/2026-11-06/docs.md
D  journal/2026-11-06/memoire.md
D  journal/2026-11-06/mesures.md
D  journal/2026-11-06/modele.md
D  journal/2026-11-06/outils.md
D  journal/2026-11-06/portes.md
MM journal/README.md
MM journal/THEMES.md
---
d31aa9a2 PRODUIT — --partition DANS LA CLI (alternative PAR DÉFAUT, filtrer EN OPTION), 10 TESTS, DOC À JOUR
6a1148c2 B13 — L'ÉLISION « que » → « qu » DANS LE TEST DES MARQUEURS (AUCUN EFFET MESURÉ, ROBUSTESSE) ; 183/183
4e6de0ee P0-3 — LES RAPPORTS FINAUX DE LA PARTITION (MESURES ÉPINGLÉES À fa1b0c6e) ; README DANS LE BUDGET
97f41554 B13 — LE STRIP DE LA FUSION : PLUS DE RÉFÉRENCE MORTE VERS UN SEGMENT DÉDUPLIQUÉ ; MESURES INCHANGÉES (0,85 / 0,6482 / 235-236)
5c0d5329 FICHE — LES PERTES DE R4 DITES HONNÊTEMENT (5/8 FAUX EN FRANÇAIS, NOMS NUS, PARTICIPES) ; README DANS LE BUDGET T1
  ```

- **bash** `{"command": "ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/ | grep -i 'rapport-r' ; echo '---'; ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ | head -60", "description": "Lister fiches R et outils"}`

  ```
rapport-r01-graphe-document.md
rapport-r02-controleur.md
rapport-r03-banc-complet.md
rapport-r03-banc-durci.md
rapport-r03-lecteur-modele.md
rapport-r04-tete-survol.md
rapport-r05-balayage.md
rapport-r06-calibration.md
rapport-r06-cascade-confiance.md
rapport-r06-cascade.md
rapport-r06-declencheur.md
rapport-r06-pipeline.md
rapport-r06-publication.md
rapport-r06-relecture.md
rapport-r07-routeur.md
rapport-r13.1-bpe.md
rapport-r13.1-campagne.md
rapport-r13.1-condition.md
rapport-r13.2-vocab1024.md
rapport-r13.3-anglais.md
rapport-r13.4-graines.md
rapport-r13-decision.md
rapport-r13-tokenisation.md
rapport-r1-preparation.md
rapport-r41-bloc-tableaux.md
rapport-r42-bloc-code.md
rapport-r43-bloc-maths.md
rapport-r44-ocr-pilote.md
rapport-r44-scans.md
rapport-raid0-nvme.md
rapport-regle-placement-perte.md
rapport-replis-cible.md
rapport-restitution.md
rapport-reutilisation-experts.md
rapport-robustesse-produit.md
rapport-routage-experts.md
rapport-routeur-confiance.md
rapport-routeur-m1-m2.md
---
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
a
… [986 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l docs/pilotage/roadmap.md docs/pilotage/en-cours.md; echo '---'; grep -n '^#\\|^##\\|^###' docs/pilotage/roadmap.md | head -80", "description": "Structure roadmap et taille docs"}`

  ```
382 docs/pilotage/roadmap.md
  145 docs/pilotage/en-cours.md
  527 total
---
1:# La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers
13:## Comment lire cette roadmap
26:## En un coup d'œil
54:## L'ordre du jour (carpe diem)
85:## Le Gantt indicatif
138:## Programme A — Le moteur (la drave, les flux)
159:## Programme B — L'intelligence (les deux étages)
187:## Programme N — Le natif (DRVM, `drave-n0`, distillation)
219:## Programme R
231:### Les six phases
242:### R0 — le lecteur v0 (système, sans entraînement)
263:### R1 — la fenêtre native
277:### R2 — la mémoire
287:### R3 — la restitution
297:### R4 — les blocs structurels
309:### R5 — la lecture croisée et le multilingue
316:### Ce que R ne fait pas
333:## La file « jamais en attente »
346:## Ce qui est bloqué, et par quoi
358:## Les questions ouvertes
370:## Le détail et l'histoire
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/ | grep -i 'tag'; echo '---'; grep -rln 'tagger' tools/ docs/ reports/ --include='*.py' --include='*.md' | head -30", "description": "Chercher le tagger"}`

  ```
census_routage.py
code_partage.py
---
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/ncl.py
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py
tools/tests/linguistique/qualifier_neuronal.py
tools/tests/linguistique/qualifier_syntagmes.py
tools/tests/linguistique/test_bloc_linguistique.py
tools/tests/linguistique/qualifier_pragmatique.py
tools/tests/linguistique/qualifier_quatre_modes.py
tools/bloc_linguistique.py
docs/pilotage/roadmap.md
docs/pilotage/en-cours.md
docs/implantation/bloc-linguistique.md
docs/produit/exemples.md
docs/produit/README.md
reports/rapport-bloc-linguistique.md
reports/rapport-pensee-gold-linguistique.md
reports/rapport-pensee-gold-200.md
reports/rapport-pensee-gold-neuronal.md
reports/rapport-pensee-gold-syntagmes.md
reports/rapport-pensee-gold-cascade.md
reports/rapport-pensee-politique-llm.md
reports/rapport-pensee-pragmatique-neuronale.md
reports/rapport-pensee-fusion-reparee.md
reports/rapport-pensee-pragmatique-full.md
reports/INDEX.md
reports/rapport-file-taches.md
reports/rapport-produit-bloc-l.md
reports/rapport-pos-anglais.md
reports/rapport-partition-syntagmes.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 219, "limit": 164}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
219: ## Programme R
220: 
221: **Charte : [le programme R](programme-r.md)** — les six phases, ce qui tient, ce qui ne tient pas, les trois lois. — Le lecteur (la nouvelle cible)
222: 
223: **La cible** : lire un document **comme un humain lit vite** — survoler, balayer, lire sélectivement, revenir — en
224: payant le calcul au prorata de ce qui est lu, et **prouver** la compréhension par la restitution. Le concept, les
225: 14 techniques et les six couches manquantes sont dans [`lecture-rapide.md`](../theorie/lecture-rapide.md).
226: 
227: **La métrique** n'est pas le [débit](../theorie/glossaire/entrees/debit-latence-aller-retour-ttft.md) : c'est **la compréhension par [unité](../theorie/glossaire/entrees/unite.md) de calcul** — une courbe
228: vitesse-compréhension, avec un **contrôle négatif** (ce qu'on perd quand on saute). Un « lecteur rapide » qui ne
229: sait pas dire ce qu'il a sauté n'est pas un lecteur, c'est un filtre.
230: 
231: ### Les six phases
232: 
233: | phase | livrable | ce qui est mesuré | dépend de |
234: |---|---|---|---|
235: | **R0 — le lecteur
… [15370 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-06, 21 h 15 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: >
8: > **Reboot du 03/11 19 h 33** : la nuit a été coupée (`kd2` **8 250/30 000**, `rope2048`
9: > **3 350/20 000**, sans checkpoint) ; les quatre sessions ont été mises en pause. **Reprise du
10: > 04/11** : hub `1e7ef596` (08 h 50), N2 09 h 41, S 09 h 46, L/B13 10 h 14 ; **N3** clos en
11: > session courte (11 h 30–11 h 38). Runbook [`plan-travail.md`](plan-travail.md) § 9 et § 12.
12: 
13: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
14: 
15: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
16: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
17: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
18: - **Prochaine action** : **suivi docs**, puis la **passe** ap
… [10722 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'R1\\.2' reports/ docs/ --include='*.md' --include='*.json' | grep -i '1024\\|1 024\\|R1.2' | head -40", "description": "Chercher R1.2-1024"}`

  ```
reports/r03-banc-extractif.json:7153:   "or": "R1.1 doit être tenté avant R1.2 : si la hiérarchie suffit, le contexte",
reports/r03-banc-extractif.json:7159:    "reponse": "R1.1 doit être tenté avant R1.2 : si la hiérarchie suffit, le contexte brut n'est pas le premier chantier."
reports/r03-banc-extractif.json:7166:    "reponse": "R1.1 doit être tenté avant R1.2 : si la hiérarchie suffit, le contexte brut n'est pas le premier chantier."
reports/r03-banc-extractif.json:7173:    "reponse": "R1.1 doit être tenté avant R1.2 : si la hiérarchie suffit, le contexte brut n'est pas le premier chantier."
reports/r03-banc-extractif.json:7180:    "reponse": "R1.1 doit être tenté avant R1.2 : si la hiérarchie suffit, le contexte brut n'est pas le premier chantier."
reports/r03-banc-extractif.json:7187:    "reponse": "R1.1 doit être tenté avant R1.2 : si la hiérarchie suffit, le contexte brut n'est pas le premier chantier."
reports/r03-banc-extractif.json:7194:    "reponse": "R1.1 doit être tenté avant R1.2 : si la hiérarchie suffit, le contexte brut n'est pas le premier chantier."
reports/r03-banc-extractif.json:8889:   "or": "R12\tCurriculum de contexte long\tspécifiée\tP1\tR11\tR1.2",
report
… [4098 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln 'tagger' reports/ docs/ tools/ --include='*.md' --include='*.py' --include='*.json' | head -40; echo '---'; grep -rn 'tagger' reports/*.md docs/pilotage/*.md | head -40", "description": "Chercher le tagger dans les fiches"}`

  ```
reports/traduction-eurlex-14b.json
reports/rapport-bloc-linguistique.md
reports/rapport-pensee-gold-linguistique.md
reports/rapport-pensee-gold-200.md
reports/pensee-gold-neuronal.json
reports/rapport-pensee-gold-neuronal.md
reports/pensee-gold-syntagmes.json
reports/rapport-pensee-gold-syntagmes.md
reports/rapport-pensee-gold-cascade.md
reports/rapport-pensee-politique-llm.md
reports/pensee-gold-pragmatique.json
reports/rapport-pensee-pragmatique-neuronale.md
reports/rapport-pensee-fusion-reparee.md
reports/pensee-pragmatique-130.json
reports/rapport-pensee-pragmatique-full.md
reports/INDEX.md
reports/rapport-file-taches.md
reports/pensee-file-taches.json
reports/rapport-produit-bloc-l.md
reports/pensee-produit-bloc-l.json
reports/rapport-pos-anglais.md
reports/pensee-partition-syntagmes.json
reports/rapport-partition-syntagmes.md
docs/pilotage/roadmap.md
docs/pilotage/en-cours.md
docs/implantation/bloc-linguistique.md
docs/produit/exemples.md
docs/produit/README.md
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/ncl.py
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py
tools/tests/linguistique/qualifier_neuronal.py
tools/tests/linguistique/
… [5633 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -iE 'r12|1024|tagger|lecteur|r1-|r1_' ; echo '---'; grep -rln 'evaluer_tagger\\|tagger' tools/*.py tools/tests/ tools/llm/ 2>/dev/null | head -30", "description": "Lister fiches R1.2/tagger et scripts"}`

  ```
n2-r12-2048.json
r03-lecteur-modele-couverture.json
r03-lecteur-modele.json
r13.2-vocab1024.json
rapport-lecteur-multifichiers.md
rapport-n2-r12-2048.md
rapport-r03-lecteur-modele.md
rapport-r13.2-vocab1024.md
rapport-r1-preparation.md
---
tools/bloc_linguistique.py
tools/tests/linguistique/__pycache__/qualifier_syntagmes.cpython-313.pyc
tools/tests/linguistique/__pycache__/qualifier_neuronal.cpython-313.pyc
tools/tests/linguistique/__pycache__/test_bloc_linguistique.cpython-313.pyc
tools/tests/linguistique/__pycache__/qualifier_pragmatique.cpython-313.pyc
tools/tests/linguistique/__pycache__/qualifier_quatre_modes.cpython-313.pyc
tools/tests/linguistique/qualifier_neuronal.py
tools/tests/linguistique/qualifier_syntagmes.py
tools/tests/linguistique/test_bloc_linguistique.py
tools/tests/linguistique/qualifier_pragmatique.py
tools/tests/linguistique/qualifier_quatre_modes.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'R1\\.2-1024\\|R1.2-1 024\\|R1.2.*1024\\|3,0107\\|3.0107' reports/ docs/ journal/2026-11-0* --include='*.md' --include='*.json' 2>/dev/null | head -40", "description": "Chercher R1.2-1024 et chiffre 3,0107"}`

  ```
reports/restitution-udhr.json:4558:  "bits_octet": 2.2103401074975526,
reports/kfold-pidgin-web.json:177:   "chrf": 13.243100330107449,
reports/n2-r11.json:42:  "L1000": 3.0107
reports/rapport-n2-r11.md:14:> à **toutes** les longueurs, **−0,244** à 1 000 (3,0107 contre 3,2545), et le modèle **utilise**
reports/rapport-n2-r11.md:150:| 1 000 | 3,2545 | **3,0107** | **−0,244** |
reports/rapport-n2-fenetre.md:6:> 3,2545 (fenêtre 256) → 3,0107 (512) → **2,9950** (1 024) ; à **2 000**, 3,2459 → 2,9728 →
reports/rapport-n2-fenetre.md:32:| **R1.2-1 024** | `data/wiki_fr` | **1 024 / 1 024** | **2 500** | **20,5 Mo** | `base-wiki-45m` |
reports/rapport-n2-fenetre.md:33:| R1.2-1 024 long | `data/wiki_fr` | 1 024 / 1 024 | 20 000 | 164 Mo | (suite du précédent) |
reports/rapport-n2-fenetre.md:49:| 1 000 | 3,2545 | 3,0107 | **2,9950** |
reports/n2-fenetre.json:22:  "L1000": 3.0107
reports/n2-fenetre.json:293:   "R1.2-1024": "wiki_fr, 1 024/1 024, 2 500 pas, 20,5 Mo, init base-wiki-45m",
reports/n2-fenetre.json:294:   "R1.2-1024-long": "wiki_fr, 1 024/1 024, +17 500 pas (20 000), 164 Mo",
reports/n2-r12-2048.json:22:  "L1000": 3.0107
reports/rapport-n2-r12-2048.md:44:| 512 (5 000 pas) | **3,339
… [2334 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n2-fenetre.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n2-r12-2048.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n2-fenetre.md</path>
<type>file</type>
<content>
1: # N2/R1 — La fenêtre entraînée, de 128 à 1 024 : elle gagne où elle sert, et elle bat 200 000 pas
2: 
3: > **Lignes de roadmap** : **R1** (la fenêtre native) et **N2** (le modèle de production) ·
4: > **Date** : 2026-11-02/03 · **Verdict** : à **octets constants** (20,5 Mo vus), entraîner sur des
5: > séquences longues avec RoPE abaisse la PPL là où la fenêtre sert — à **1 000 octets**,
6: > 3,2545 (fenêtre 256) → 3,0107 (512) → **2,9950** (1 024) ; à **2 000**, 3,2459 → 2,9728 →
7: > **2,9449** — et à courte longueur l'ordre **s'inverse** (128 : 3,3399 pour 512 contre 3,3878
8: > pour 1 024) : la fenêtre longue échange du **démarrage à froid** contre de la **profondeur**.
9: > Le contrôle « même texte » le tranche : **chaque modèle sature exactement à sa fenêtre** —
10: > fenêtre 256 : 3,0663 → 3,1411 (il **se dégrade** au-delà de 256) ; 512 : 2,9068 → 2,8076 ;
11: > 1 024 : 2,9197 → **2,7837**, et 1 024 = 2 000 au millième. Sur le **modèle de production**,
12: > affiner N2.ac avec RoPE et 512 octets pendant **61,4 Mo** (le budget même de N2.ac) le bat
13: > **
… [8890 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n2-r12-2048.md</path>
<type>file</type>
<content>
1: # R1.2 — La fenêtre 2 048 et le point d'équilibre : à octets constants, 1 024 gagne ; à pas constants, plus de données gagnent
2: 
3: > **Ligne de roadmap** : R1 (la fenêtre native) · **Date** : 2026-11-03 · **Verdict** : à
4: > **octets constants** (20,5 Mo vus sur `data/wiki_fr`), la fenêtre entraînée paie jusqu'à
5: > **1 024** — à 2 000 octets, 3,2459 (fenêtre 256) → 2,9728 (512) → **2,9449** (1 024) — et
6: > **2 048 ne la bat pas** à octets constants (2,9630 ; et au complément 164 Mo, 3,0466 contre
7: > 2,9955) : à budget d'octets fixé, doubler encore la fenêtre divise les **pas** par deux et le
8: > gain s'annule — **à pas constants en revanche, 2 048 gagne 0,08 à 0,10** (2,9121 contre 2,9955
9: > à 128 octets, 2,4383 contre 2,5429 à 4 000). À **pas constants** (20 000), la même
10: > recette à fenêtre **1 024** voit **8× plus d'octets** et **écrase** tout : **2,9955** à 128
11: > octets, **2,6256** à 1 000, **2,5429** à 4 000 — à **0,13** et **0,04** de 2,5 en domaine
12: > (`val_fr`, pas le corpus propre : ce n'est pas la porte, c'en est le voisinage).
… [11255 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline --all -30 --grep='R1' -i; echo '---'; git log --oneline -20", "description": "Chercher commits R1"}`

  ```
4d34c37a PILOTAGE — LES VAGUES 5 À 7 (AUDITS V7/V8, R1/R3, TOP-K, V10) DOCUMENTÉES AU PLAN-TRAVAIL
f908d7b0 B13 — R1/R2/R3 : EXACT 212/212 (1,0000), COUVERTURE 0,887, F1 0,5763, FR 1,0 / EN 1,0 ; 27 SPANS DONT 17 INATTEIGNABLES ; 183/183
86000584 ÉTAT — HEURE 01 H 51 ; PASSE 72 JOURNAUX : R13-BPE ET RÉCURRENCE VERTES, RÉFLEXE EN COURS
f50ad713 BACKLOG — LA FICHE N2 PASSE AU RÉEL : LA FENÊTRE EST LA RECETTE, LA PORTE PROPRE RESTE
bfd51b90 NUIT — CLÔTURE : LA FENÊTRE EST MESURÉE DE 128 À 2 048, LA PRODUCTION PASSE SOUS 2,5 AU GRAND CORPUS, LA PORTE PROPRE RESTE À 0,29
e1c1064d NUIT — LA FENÊTRE EST LA RECETTE DE PRODUCTION : 2,9943 À 128 ET SOUS 2,5 AU GRAND CORPUS ; LA PORTE PROPRE RESTE À 2,7856 ; LA FENÊTRE PAIE À TOUTES LES CAPACITÉS
19eacae6 N2 — LES SIX FICHIERS DE LA NUIT COMMITTÉS PAR LE HUB APRÈS LA PAUSE
3026dc6a NUIT — LA ROADMAP PASSE AU 03/11 : LA FENÊTRE EST SOLVABLE MAIS NON DISCRIMINANTE ; LA CASCADE VRAI MODÈLE
c7ef9bc4 FENÊTRE 2 048 — À OCTETS CONSTANTS LE GAIN S'ARRÊTE À 1 024 (2,9950 À 1 000 OCTETS) ; À 20 000 PAS ELLE DONNE 2,9955 À 128 ET 2,6256 À 1 000
b1c0bcda PILOTAGE — UN MANDAT LONG AVEC UN CLAIM ACTIF N'EST PAS PÉRIMÉ ; LA PORTE SESSIONS LIT LE REGISTRE
c0
… [4335 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '80,130p' reports/rapport-file-taches.md", "description": "Lire table des tâches P8/P17"}`

  ```
## 6. Doublons (6)

Même action nommée dans plusieurs documents, ou même libellé pour deux objets. Un doublon n'est pas une faute de frappe : il fait croire à deux chantiers et double le travail de mesure.

| # | action | où | preuve | décision |
|---|---|---|---|---|
| D1 | dev/test à re-mesurer | v9, v10, v11 §6 ; plan-travail §9 vague 7 | v12 : dev 153/153, test 69/69 ; rapport-dev-test-v10 | Une seule mesure, faite ; retirer des suites |
| D2 | Les N spans | v5 (52), v7 (43), r1r3 (27), v9 (20), v10 (19), v11 (18), v12 (17) | v12 §2 : 17 spans (8 REL, 5 SUB, 4 GP) | Seul 17 est vivant ; les autres sont historiques |
| D3 | T132/T133 | roadmap:178 ; chantiers:90 ; plan:39 et 195 ; en-cours:131 | autotest : T132 5/5, T133 5/5 | Fermer ; retirer les 5 mentions |
| D4 | Passe complète | en-cours:131 ; plan:401 ; references:3 | ea7d3275 ; registre 06/11 (79/4) | Une seule passe de référence ; la prochaine sera 84 portes |
| D5 | gold 200+ | roadmap:31 et 178 ; chantiers:83 et 89 ; en-cours:131 ; plan:39 et 195 | 13 occurrences, aucune définition | Définir l'objet avant d'en faire une tâche |
| D6 | A2.6 experts | roadmap:30 et 146 ; chantiers:84 ; dependances:162 ; en-cours:120 ; ba
… [4175 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-file-taches.md", "limit": 80}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r44-scans.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-file-taches.md</path>
<type>file</type>
<content>
1: # La file des tâches — inventaire, trois files et ordre pour 09 h 30 → 12 h
2: 
3: > **Ligne de roadmap** : B13 (moteur de pensée) · **Date** : 2026-11-06, 10 h 20 HNE · **Branche** : `s/v7` · **HEAD mesuré** : `7679a2d4`.
4: > **Mission** : inventer toutes les prochaines actions nommées dans `roadmap.md`, `en-cours.md`, `plan-travail.md` § 9 et § 12, `backlog/index.md`, `backlog/dependances.md`, `references-non-regression.md` et les 12 fiches récentes ; les classer en trois files ; détecter doublons et périmées ; proposer l'ordre de la fenêtre.
5: > **Verdict** : **29 tâches** — **8 autonomes**, **11 en coordination**, **10 bloquées** ; **6 doublons**, **18 périmées**, **12 dépendances cachées**.
6: > **Ce que cette fiche n'est pas** : un commit, une modification d'existant, ou une mesure nouvelle sur S/D/N2. Elle ne crée que deux fichiers neufs.
7: 
8: ## 1. Résumé exécutif
9: 
10: La file est **courte** une fois les doublons retirés : **8 tâches sont exécutables en autonomie** dans le territoire L/B13 et le pilotage, **11 demandent une coordination** (S, D, 
… [12982 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r44-scans.md</path>
<type>file</type>
<content>
1: # R4.4 — les scans : la photo passe de 55,9 % à 6,7 % de WER, les colonnes de 89 % à 0,5 %
2: 
3: > **Objet.** La ligne R4.4 était **partielle** : dix pages **rendues** lues, mais aucun scan.
4: > Ce programme fabrique cinq familles de dégradations, mesure ce qu'elles coûtent, ajoute le
5: > prétraitement, la récupération des exposants, l'ordre de lecture des colonnes et les cellules
6: > des tableaux — et valide la chaîne sur un **vrai scan** d'Internet Archive.
7: >
8: > **Ce que ce n'est pas.** Les scans sont **simulés** (il n'y a pas de scanner sur la machine) ;
9: > la validation réelle compare à la **couche OCR** d'Internet Archive, pas à une vérité humaine.
10: > Les deux limites sont dites, pas contournées.
11: 
12: ## Dispositif
13: 
14: - **100 scans simulés** : 10 pages de développement (9 portent les 30 questions du banc R0.3) et
15:   10 pages de test, × **5 familles** : `propre` (contrôle), `photocopie` (200 dpi, flou, 1,2°,
16:   mouchetures, JPEG q45), `photo` (180 dpi, perspective, éclairage inégal + ombre, flou de
17:   mouvement, bruit, JPEG q2
… [24088 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/llm/ 2>/dev/null; echo '---'; grep -rn 'llama-server\\|7B\\|Qwen\\|tagger' tools/tests/linguistique/qualifier_neuronal.py tools/tests/linguistique/qualifier_syntagmes.py tools/tests/linguistique/qualifier_pragmatique.py | he … [54 caractères tronqués]`

  ```
deepseek.py
distillation.py
enseignant.py
entrainer_masque.py
__init__.py
masque.py
mesure.py
prompts_publics_300.jsonl
prompts_publics.jsonl
prompts_publics.py
__pycache__
tests
---
tools/tests/linguistique/qualifier_neuronal.py:2:"""qualifier_neuronal.py — qualifie un tagger neuronal local sur le gold (180 phrases, 804 tokens).
tools/tests/linguistique/qualifier_neuronal.py:4:Le tagger est `bloc_linguistique.NeuronalLLMPOS` : un modèle GGUF servi par `llama-server`, une
tools/tests/linguistique/qualifier_neuronal.py:133:    """`llama-server --version` écrit sur stderr ; on lit les deux flux."""
tools/tests/linguistique/qualifier_neuronal.py:134:    for commande in (["llama-server", "--version"], ["llama-cli", "--version"]):
tools/tests/linguistique/qualifier_neuronal.py:162:    commande = ["llama-server", "-m", str(modele), "--host", "127.0.0.1", "--port", str(port),
tools/tests/linguistique/qualifier_neuronal.py:182:    ap.add_argument("--demarrer", action="store_true", help="lance llama-server sur CPU")
tools/tests/linguistique/qualifier_neuronal.py:205:    tagger = bl.NeuronalLLMPOS(modele, endpoint=endpoint, confiance=args.confiance)
tools/tests/linguistique/qualifier_neurona
… [3702 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-gold-neuronal.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-gold-neuronal.md</path>
<type>file</type>
<content>
1: # L — le gold neuronal : un tagger 7B local, la cascade POS à 0,944
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) / **R0.7** (bloc linguistique) · **Date** : 2026-11-02 ·
4: > **Verdict** : ✅ **le tagger 7B-Instruct local est qualifié** — POS seul **0,8483** (heuristique
5: > **0,7512**), **cascade à 0,6 : 0,9440** (20 réelles **0,9238**, 160 synthétiques **0,9471**),
6: > **0 refus**, **180 appels**. La cascade **garde** les classes fermées de l'heuristique (**0,9392**)
7: > et lui **prend** les ouvertes (**0,9474**) : c'est la complémentarité, pas le remplacement.
8: >
9: > **Dispositif** : [`qualifier_neuronal.py`](../tools/tests/linguistique/qualifier_neuronal.py) ;
10: > [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`NeuronalLLMPOS`) ; JSON
11: > [`pensee-gold-neuronal.json`](pensee-gold-neuronal.json).
12: 
13: ## 1. Ce qui était bloqué
14: 
15: Le rapport du gold ([`pensee-gold`](rapport-pensee-gold-linguistique.md) § 4) disait : « le vrai
16: modèle neuronal est **refusé** (`llama-cli` local) ; la qualification neuronale
… [10025 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-*.sh | sed 's|tools/||'; echo '---'; ls tools/ | grep -E 'lecteur|banc|graphe|doc|controleur|routeur|survol|balayage|relecture|pipeline|tableau|code|maths|ocr|scan|fenetre|eval' | head -80", "description": "Lister port … [16 caractères tronqués]`

  ```
porte-adaptateur-sortie.sh
porte-audit-drapeaux.sh
porte-b1110-hybride.sh
porte-balayage.sh
porte-bloc-code.sh
porte-bloc-linguistique.sh
porte-bloc-maths.sh
porte-bloc-tableaux.sh
porte-budget.sh
porte-bus.sh
porte-bus-socket.sh
porte-c4-retard.sh
porte-cerveau.sh
porte-consolidation.sh
porte-coupe.sh
porte-cycle-c2.sh
porte-deepseek.sh
porte-delais.sh
porte-diff-couche.sh
porte-document.sh
porte-echange-experts.sh
porte-episodique.sh
porte-etat.sh
porte-flux.sh
porte-fusion.sh
porte-gain.sh
porte-greffe.sh
porte-harnais-invariants.sh
porte-homeostasie.sh
porte-horloge.sh
porte-indice.sh
porte-jeux.sh
porte-jumeaux.sh
porte-lecteur.sh
porte-lecture.sh
porte-m5-brouillon.sh
porte-melange.sh
porte-memoire.sh
porte-miroir-blocs.sh
porte-mistral.sh
porte-n3-cache.sh
porte-n3-composition.sh
porte-n3-deux-processus.sh
porte-n3-deux-regions.sh
porte-n3-generation.sh
porte-n3-inventaire.sh
porte-n3-placement.sh
porte-n3-pont.sh
porte-n3-positions.sh
porte-n3-profondeur.sh
porte-n3-refus.sh
porte-n3-reseau.sh
porte-n3-routes.sh
porte-n3-service-briques.sh
porte-n3-service.sh
porte-n3-seuil.sh
porte-n3-sparsite-compte.sh
porte-n3-sparsite.sh
porte-occupation-elagage.sh
porte-occupation-mote
… [1402 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '^#\\|^##' reports/rapport-pensee-gold-syntagmes.md reports/rapport-pensee-gold-cascade.md reports/rapport-pensee-pragmatique-neuronale.md | head -50", "description": "Structure des fiches tagger"}`

  ```
reports/rapport-pensee-gold-syntagmes.md:1:# B13 — les syntagmes neuronaux : BIO, tête 0,7606, et la politique de fusion
reports/rapport-pensee-gold-syntagmes.md:13:## 1. Ce qui était mesuré
reports/rapport-pensee-gold-syntagmes.md:21:## 2. Le dispositif
reports/rapport-pensee-gold-syntagmes.md:43:## 3. Les résultats
reports/rapport-pensee-gold-syntagmes.md:66:## 4. Les contrôles négatifs
reports/rapport-pensee-gold-syntagmes.md:79:## 5. Le coût
reports/rapport-pensee-gold-syntagmes.md:87:## 6. Ce qui pourrait rendre ce résultat faux
reports/rapport-pensee-gold-syntagmes.md:108:## 7. Ce que la politique de fusion dit
reports/rapport-pensee-gold-syntagmes.md:122:## 8. La suite
reports/rapport-pensee-gold-syntagmes.md:135:## 9. Fichiers
reports/rapport-pensee-gold-cascade.md:1:# B13 — la cascade complète : POS 0,9415, syntagmes 0,7539, acte 1,0
reports/rapport-pensee-gold-cascade.md:14:## 1. Ce qui était mesuré
reports/rapport-pensee-gold-cascade.md:23:## 2. Le dispositif
reports/rapport-pensee-gold-cascade.md:41:## 3. Les résultats
reports/rapport-pensee-gold-cascade.md:63:## 4. Les ablations et la politique
reports/rapport-pensee-gold-cascade.md:80:## 5. Les contrôles négatifs
repo
… [768 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '85,00\\|84,96\\|0,8500\\|0.8500' reports/*.md | tail -30; echo '---'; ls tools/tests/linguistique/ | grep -v pycache", "description": "Chercher POS 85 et fichiers gold"}`

  ```
reports/INDEX.md:608:| [rapport-pos-r4-integre.md](rapport-pos-r4-integre.md) | B13 — le paquet POS sûr : classes fermées anglaises + R4-en, POS 84,96 % |
reports/rapport-partition-integree.md:8:> exact 235/236, POS 85,00 %** — les mesures de la base, **sans déduplication silencieuse**. Le mode
reports/rapport-pos-r4-integre.md:1:# B13 — le paquet POS sûr : classes fermées anglaises + R4-en, POS 84,96 %
reports/rapport-pos-r4.md:31:- **Paquet sûr** (R4-en + classes fermées) : **+1,19 dev / +1,11 test**, POS **85,00 %**, **37/0**,
reports/rapport-pos-r4.md:65:| **R4-en + classes** | **85,00** | **84,94** | **+1,19** | **85,11** | **+1,11** | **37 / 0** | **2** | 0,6188 | 222/222 | 1 faux (`Where`) |
reports/rapport-pos-r4.md:310:| R4-en + classes | 85,00 | 84,94 | +1,19 | 85,11 | +1,11 | 37 / 0 | 2 | 0,6188 | 222/222 | 92,95 | 77,46 | 94,25 | 79,76 |
reports/rapport-pos-r4.md:408:   POS 85,00 %, 37/0, 2 faux→faux, F1 +0,0007, attachement 222/222. C’est le meilleur rapport
reports/rapport-pos-r4.md:457:85,00 %** (dev 84,94 / test 85,11), **37 correctifs / 0 cassé / 2 faux→faux** : c’est exactement le
reports/README.md:22:| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **
… [460 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-gold-cascade.md", "limit": 130}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-gold-cascade.md</path>
<type>file</type>
<content>
1: # B13 — la cascade complète : POS 0,9415, syntagmes 0,7539, acte 1,0
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) / **R0.7** (bloc linguistique) · **Date** : 2026-11-02 ·
4: > **Verdict** : ✅ **la cascade complète est mesurée** — POS **0,9415**, syntagmes exacts **0,6088**,
5: > **tête 0,7539**, acte **1,0**, fraction **0,6381**, **0 refus**, **180 + 180 appels**. Les
6: > **ablations sont exactes** : la cascade complète vaut la cascade POS (0,9415) **et** la cascade
7: > syntagmes (0,6088 / 0,7539) ; les parties s'additionnent sans perte. La politique de fusion
8: > reste le levier : **0,5670** avec la priorité heuristique contre **0,7539** avec `confiance`.
9: >
10: > **Dispositif** : [`qualifier_cascade.py`](../tools/tests/linguistique/qualifier_cascade.py) ;
11: > [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`NeuronalLLMCompose`) ; JSON
12: > [`pensee-gold-cascade.json`](pensee-gold-cascade.json).
13: 
14: ## 1. Ce qui était mesuré
15: 
16: Les deux taggers étaient qualifiés séparément : POS **0,8483** seul / cascade **0,94
… [7536 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'class Neuronal\\|class Cascade\\|class Heuristique\\|def priorite_par_defaut\\|DeepSeek\\|deepseek' tools/bloc_linguistique.py | head -40; echo '---'; grep -n 'Neuronal' tools/bloc_linguistique.py | head -30", "description": … [36 caractères tronqués]`

  ```
787:class Heuristique:
1648:class NeuronalLLM:
1727:class NeuronalLLMPOS:
1858:class NeuronalLLMChunks:
1993:class NeuronalLLMCompose:
2043:class NeuronalLLMPragmatique:
2315:def priorite_par_defaut() -> dict | None:
2316:    """La fusion par niveau si un neuronal réel est joignable (clé DeepSeek), sinon la confiance.
2423:class Cascade:
---
8:  - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
10:  - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
12:  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
143:class RefusNeuronal(RuntimeError):
1592:class MockNeuronal:
1648:class NeuronalLLM:
1652:    `RefusNeuronal`. Le `MockNeuronal` sert aux tests de contrat, pas à la qualité.
1679:            raise RefusNeuronal(f"modèle absent : {self.modele}")
1686:            raise RefusNeuronal(str(e)) from e
1691:            raise RefusNeuronal(f"pas de JSON : {texte_sortie[:120]!r}")
1695:            raise RefusNeuronal(f"JSON invalide : {e}") from e
1727:class NeuronalLLMPOS:
1858:class NeuronalLLMChunks:
1869:    le niveau `syntagme` seulement ; le POS et la pragma
… [345 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' reports/rapport-pos-r4.md", "description": "Lire l'intro du paquet POS 85 %"}`

  ```
# POS — R4 + classes fermées : +1,19 pt dev / +1,11 test en paquet sûr, +1,51/+1,51 en paquet max

> **Ligne de roadmap** : **A25** (gold anglais) · **B13** (moteur de pensée) · **Date** : 2026-11-06 ·
> **Verdict** : ✅ les deux derniers leviers POS sont mesurés. **R4 bilingue** vaut **+0,74 dev /
> +0,71 test** (23 correctifs, 0 cassé), **les classes fermées** **+0,78 / +0,81** (25 correctifs,
> 0 cassé). Le **paquet sûr** (R4-en + classes fermées) vaut **+1,19 / +1,11**, **37/0**, F1
> **+0,0007**, attachement **222/222**. Le **paquet max** (R4 bilingue) vaut **+1,51 / +1,51**,
> 48/0, mais **11 faux→faux** et **5 faux positifs français** sur les 50 textes libres. R4 n’est
> donc **pas « 0 perte »** : « 0 cassé » est une propriété d’exactitude, pas de sens.
>
> **Snapshot** : référence **B13** commit `2ba393b0`, `bloc_linguistique.py` SHA
> `f3db75fc…`, gold `3663be6c…` / `05d4f6df…` / `e3e704ce…` ; split `gold_split.py`
> (`crc32(id) % 3 == 0` → test). Le dépôt a bougé **pendant** la mesure (correctif d’élision,
> gold corrigé) : un instantané HEAD `dd0e5e47…` sert de contrôle de reproductibilité (§ 2.2),
> pas de référence.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools
… [4623 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/evaluer_gold.py --help 2>&1 | head -40; echo '---'; sed -n '1,60p' tools/tests/linguistique/evaluer_gold.py", "description": "Voir le banc d'évaluation POS"}`

  ```
usage: evaluer_gold.py [-h] [--json JSON] [--reel]

evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) +
synthétique (160). Trois niveaux : POS (token, exact), syntagmes (exact +
**par tête**), pragmatique. Quatre lectures : heuristique, mock neuronal,
parallèle, cascade. Le vrai modèle est optionnel (`--reel`) : s'il ne répond
pas, il est refusé, pas simulé.

options:
  -h, --help   show this help message and exit
  --json JSON
  --reel
---
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
REEL = pathlib.Path(__file__).with_name("gold_reel.json")
SYNTH = pathli
… [1368 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nfor f in ['tools/tests/linguistique/gold.json','tools/tests/linguistique/gold_synthetique.json','tools/tests/linguistique/gold_reel.json','tools/tests/linguistique/gold_gele.json']:\n    try:\n        d … [432 caractères tronqués]`

  ```
tools/tests/linguistique/gold.json dict keys ['version', 'phrases', 'note'] len 3
  version <class 'int'> 
  phrases <class 'list'> 20
  note <class 'str'> 58
tools/tests/linguistique/gold_synthetique.json dict keys ['version', 'source', 'graine', 'note', 'phrases'] len 5
  version <class 'int'> 
  source <class 'str'> 11
  graine <class 'int'> 
tools/tests/linguistique/gold_reel.json dict keys ['version', 'source', 'note', 'phrases'] len 4
  version <class 'int'> 
  source <class 'str'> 4
  note <class 'str'> 20
tools/tests/linguistique/gold_gele.json dict keys ['gele', 'phrases'] len 2
  gele <class 'str'> 10
  phrases <class 'list'> 602
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold-etat-r.json 2>&1 | tail -40", "description": "Rejouer l'évaluation POS du bloc L", "timeoutMs": 300000}`

  ```
"top1_taux_span": 0.9958,
    "topk_taux_span": 0.9915,
    "topk_exact": 234,
    "topk_exact_taux": 0.9791,
    "topk_exact_taux_span": 0.9915,
    "exact_taux_span": 0.9958,
    "verbe": {
     "cibles": 157,
     "justes": 157,
     "taux": 1.0
    },
    "nom": {
     "cibles": 79,
     "justes": 78,
     "taux": 0.9873
    },
    "couverture": 0.9874,
    "par_langue": {
     "fr": {
      "cibles": 151,
      "labels": 150,
      "exact": 149,
      "topk": 148,
      "exact_taux_span": 0.9933
     },
     "en": {
      "cibles": 88,
      "labels": 86,
      "exact": 86,
      "topk": 86,
      "exact_taux_span": 1.0
     }
    }
   },
   "attachement_tete": {
    "cibles": 236,
    "labels": 236,
    "top1": 235,
    "topk": 234
heuristique all: {"pos": {"exactitude": 0.85, "exactitude_ferme": 0.9295, "exactitude_ouvert": 0.7746, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 62, "NOUN": 68, "VERB": 4}, "ADV": {"ADV": 131, "NOUN": 7, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 119, "?": 3, "NOUN": 1, "VERB": 1}, "CONJ": {"CONJ": 55, "PRON": 28, "?": 13, "PREP": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2
… [512 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,collections\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json','gold_gele.json']:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    ph=d['phrases']\n    lang=collections.Counter(p.g … [239 caractères tronqués]`

  ```
gold.json 20 phrases 0 tokens {'fr': 14, 'en': 6}
  keys ['id', 'langue', 'texte', 'mots', 'segments', 'pragma']
gold_reel.json 432 phrases 0 tokens {'fr': 228, 'en': 204}
  keys ['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source']
gold_synthetique.json 160 phrases 0 tokens {'fr': 160}
  keys ['id', 'langue', 'texte', 'pragma', 'source', 'mots', 'segments']
gold_gele.json 602 phrases 0 tokens {'fr': 394, 'en': 208}
  keys ['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee-gold-etat-r.json'))\nprint('top keys',list(d))\nfor k,v in d.items():\n    if isinstance(v,dict) and 'pos' in v:\n        p=v['pos']; print(k, 'POS',p.get('exactitude'),'fe … [312 caractères tronqués]`

  ```
top keys ['date', 'heuristique', 'mock_neuronal', 'parallele', 'cascade', 'reel', 'attachement_hasard', 'gold', 'verdict', 'ok']
--- meta
gold {"phrases": 612, "reel": 452, "hand": 20, "reel_new": 432, "synthetique": 160, "tokens": 3179}
date "2026-11-01"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\ng=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\ns=json.load(open('tools/tests/linguistique/gold_synthetique.json'))['phrases']\nr=json.load(open('tools/tests/linguistique/gold_reel.j … [334 caractères tronqués]`

  ```
20+160 (180, 804)
20+432+160 (612, 3179)
reel432 (432, 2375)
gele (602, 3141)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee-gold-etat-r.json'))\nfor k in ('heuristique','mock_neuronal','parallele','cascade','reel'):\n    v=d.get(k)\n    if not isinstance(v,dict): print(k,v); continue\n    p=v.ge … [223 caractères tronqués]`

  ```
heuristique {'exactitude': None, 'exactitude_ferme': None, 'exactitude_ouvert': None, 'tokens': None}
mock_neuronal {'exactitude': None, 'exactitude_ferme': None, 'exactitude_ouvert': None, 'tokens': None}
parallele {'exactitude': None, 'exactitude_ferme': None, 'exactitude_ouvert': None, 'tokens': None}
cascade {'exactitude': None, 'exactitude_ferme': None, 'exactitude_ouvert': None, 'tokens': None}
reel {'exactitude': None, 'exactitude_ferme': None, 'exactitude_ouvert': None, 'tokens': None}
verdict {'pos_hand': True, 'pos_reel': True, 'pos_synthetique': True, 'syntagme_hand': True, 'syntagme_reel': True, 'syntagme_synthetique': True, 'tete': True, 'acte': True, 'cascade_pos': True, 'cascade_syntagme': True, 'attachement_topk': True, 'attachement_hasard': True, 'attachement_tete_couverture': True, 'attachement_tete_topk': True, 'attachement_tete_hasard': True, 'reel_non_requis': True} ok True
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/porte-bloc-linguistique.sh | head -40; echo '---'; bash tools/porte-bloc-linguistique.sh >/tmp/porte-bl.log 2>&1; echo exit=$?; tail -20 /tmp/porte-bl.log", "description": "Rejouer la porte du bloc linguistique", "timeoutMs … [10 caractères tronqués]`

  ```
#!/usr/bin/env bash
# Porte du bloc linguistique — tests de contrat + mesure UDHR (langue/script).
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "=== PORTE BLOC LINGUISTIQUE ==="
python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' || { echo "❌ tests"; exit 1; }
python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl --sortie /tmp/bloc-linguistique-porte.json || { echo "❌ autotest"; exit 1; }
python3 tools/tests/linguistique/gold.py >/dev/null || { echo "❌ gold"; exit 1; }
python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold-porte.json >/dev/null || { echo "❌ évaluation gold"; exit 1; }
echo "✅ porte bloc linguistique verte"
---
exit=0
  "ponctuation_refus": "vide",
  "langue_inconnue": "und",
  "indice_faux": "und",
  "rejeu_identique": true
 },
 "verdicts": {
  "langue": true,
  "script": true,
  "permute_faible": true,
  "niveaux": true,
  "substitution": true,
  "parallele": true,
  "activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
✅ porte bloc linguistique verte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee-gold-etat-r.json'))\nfor k in ('heuristique','cascade'):\n    print('==',k, list(d[k])[:20])\n    print(json.dumps(d[k],ensure_ascii=False)[:800])\nprint('== reel keys', li … [133 caractères tronqués]`

  ```
== heuristique ['all', 'reel', 'hand', 'reel_new', 'synthetique']
{"all": {"bloc": "heuristique", "phrases": 612, "pos": {"exactitude": 0.85, "exactitude_ferme": 0.9295, "exactitude_ouvert": 0.7746, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 62, "NOUN": 68, "VERB": 4}, "ADV": {"ADV": 131, "NOUN": 7, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 119, "?": 3, "NOUN": 1, "VERB": 1}, "CONJ": {"CONJ": 55, "PRON": 28, "?": 13, "PREP": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 430, "?": 30, "CONJ": 1, "DET": 14}, "VERB": {"VERB": 546, "NOUN": 218, "PREP": 2, "ADJ": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.6715, "rappel": 0.6264, "f1": 0.6482, "tp": 1167, "fp": 571, "fn": 696, "tete": {"precision": 0.8208, 
== cascade ['all', 'reel', 'hand', 'reel_new', 'synthetique', 'appels_neuronal']
{"all": {"bloc": "cascade", "phrases": 612, "pos": {"exactitude": 0.85, "exactitude_ferme": 0.9295, "exactitude_ouvert": 0.7746, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 62, "NOUN": 68, "VERB": 4}, "ADV": {"ADV": 131, "NOUN": 7, "PREP": 1, "ADJ": 
… [598 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -lh work/n2ac/rope1024-20k.pt work/n2ac/rope1024-2.5k.pt work/n2ac/mix512-15k.pt work/n2ac/mix1024-7.5k.pt work/n2ac/rope2048-20k.pt 2>&1; echo '---'; find work -maxdepth 3 -name '*1024*' -o -name '*2048*' 2>/dev/null | head -20;  … [131 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 131M  2 nov 21:50 work/n2ac/mix1024-7.5k.pt
-rw-r--r--. 1 stephane stephane 131M  2 nov 20:54 work/n2ac/mix512-15k.pt
-rw-r--r--. 1 stephane stephane 131M  2 nov 22:30 work/n2ac/rope1024-20k.pt
-rw-r--r--. 1 stephane stephane 131M  2 nov 20:16 work/n2ac/rope1024-2.5k.pt
-rw-r--r--. 1 stephane stephane 131M  4 nov 21:09 work/n2ac/rope2048-20k.pt
---
work/r44/ocr/98c10248fe3c032c-fra-3.json
work/r44/ocr/98c10248fe3c032c-fra-3-col.json
work/r44/ocr/98c10248fe3c032c-fra-3-m3.json
work/r44/ocr/98c10248fe3c032c-fra-3-m3-col.json
work/r44/ocr/98c10248fe3c032c-fra-3-m4.json
work/r44/ocr/98c10248fe3c032c-fra-3-m4-col.json
work/r44/ocr/98c10248fe3c032c-fra-3-m5.json
work/r44/ocr/98c10248fe3c032c-fra-3-m5-col.json
work/r44/ocr/98c10248fe3c032c-fra-3-m6.json
work/r44/ocr/98c10248fe3c032c-fra-3-m6-col.json
work/r44/ocr/98c10248fe3c032c-fra-3-m7.json
work/r44/ocr/98c10248fe3c032c-fra-3-m7-col.json
work/n2ac/chaine_1024.sh
work/n2ac/chaine_1024.out
work/n2ac/rope1024-2.5k.log
work/n2ac/rope1024-2.5k.pt
work/n2ac/rope1024-2.5k.drvm
work/n2ac/rope1024-2.5k.pt.json
work/n2ac/rope1024-20k.log
work/n2ac/eval-rope1024-2.5k.json
---
/home/stephane/.local/bin/llama-server

… [195 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nfor f in ['reports/n2-r12-2048.json','reports/n2-fenetre.json','reports/pensee-gold-neuronal.json']:\n    d=json.load(open(f))\n    print('==',f, list(d)[:15])\n    for k in ('date','verdict','gold','ta … [185 caractères tronqués]`

  ```
== reports/n2-r12-2048.json ['loi_256', 'loi_512', 'loi_1024', 'loi_2048', 'loi_1024_20k', 'meme_texte_1024', 'miroir_1024', 'entrainement_2048', 'entrainement_1024_20k', 'dispositif', 'loi_2048_15k', 'loi_2048_10k', 'loi_2048_20k']
== reports/n2-fenetre.json ['loi_fenetre_256', 'loi_fenetre_512', 'loi_fenetre_1024', 'meme_texte_256', 'meme_texte_512', 'meme_texte_1024', 'production_n2ac', 'production_200k', 'production_512', 'production_512_meme_texte', 'production_1024', 'production_1024_meme_texte', 'miroir_1024', 'miroir_production_512', 'miroir_256']
== reports/pensee-gold-neuronal.json ['date', 'modele', 'gold', 'tagger', 'mesures', 'controles', 'seuils', 'verdict', 'duree_totale_s', 'limites']
  date "2026-11-02 16:52 EST"
  verdict true
  gold {"phrases": 180, "tokens": 804, "hand": 20, "synth": 160}
  tagger {"classe": "NeuronalLLMPOS", "confiance": 0.6, "tokenisation": "Heuristique._mots (mot/nombre)", "contrainte": "grammaire GBNF, une classe par token"}
  modele {"nom": "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf", "fichiers": [{"nom": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf", "octets": 3993201344, "sha2
… [600 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -lh models/ | head -20; echo '---'; find /home/stephane -maxdepth 5 -iname '*qwen2.5-7b*' 2>/dev/null | head -10", "description": "Vérifier présence du 7B"}`

  ```
total 844M
-rw-r--r--. 1 stephane stephane 337M 25 sep 17:13 Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 507M 25 sep 16:52 Qwen2.5-0.5B-Q8_0.gguf
drwxr-xr-x. 1 stephane stephane  138 15 oct 09:02 vision
---
/home/stephane/IA/cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-gold-neuronal.json'))\nm=d['mesures']\nfor k,v in m.items():\n    a=v.get('all',{}) if isinstance(v,dict) else {}\n    print(k, {x:a.get(x) for x in ('tokens','exactitud … [221 caractères tronqués]`

  ```
heuristique {'tokens': 804, 'exactitude': 0.7512, 'ferme': 0.9392, 'ouvert': 0.6211}
neuronal {'tokens': 804, 'exactitude': 0.8483, 'ferme': 0.766, 'ouvert': 0.9053}
cascade {'tokens': 804, 'exactitude': 0.944, 'ferme': 0.9392, 'ouvert': 0.9474}
controles {"majoritaire": {"description": "toujours NOUN", "exactitude": 0.2289}, "uniforme": {"description": "tirage uniforme sur les 12 classes", "exactitude": 0.0833}, "permutation": {"description": "les POS prédits sont permutés entre tokens (graine 0)", "exactitude": 0.1729}, "hasard": {"graine": 0, "tokens": 804}}
limites ["POS seulement : le tagger ne rend ni syntagmes ni pragmatique.", "20 phrases réelles (hand) ont servi au choix du modèle et du prompt ; les 160 synthétiques sont le jeu de test.", "Le seuil 0,6 de la cascade vient du seuil ouvert de l'heuristique (0,55), pas d'un balayage sur le gold.", "CPU seulement (les GPU de N2 sont réservés) ; pas de mesure GPU.", "Le gold utilise la même tokenisation que le bloc (vérifié : 180/180)."]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in porte-document porte-lecteur porte-lecture porte-balayage porte-tableaux porte-bloc-tableaux porte-bloc-code porte-bloc-maths porte-ocr-scans porte-ocr porte-r13-bpe; do echo \"=== $f\"; sed -n '1,12p' tools/$f.sh; done", "d … [43 caractères tronqués]`

  ```
=== porte-document
#!/bin/bash
# porte-document.sh — R0.1 : le document est un graphe, et le graphe se vérifie.
#
# POURQUOI CETTE PORTE EXISTE. Une découpe de document qui « a l'air bonne » n'est pas une
# découpe : sans partition exacte, un offset faux ne se voit pas ; sans extraction
# indépendante, un extracteur qui invente des mots ne se voit pas non plus. Cette porte
# exige donc les trois choses ensemble — partition, fidélité, rejeu — plus trois contrôles
# négatifs qui doivent ÉCHOUER (texte plat, deux colonnes, notes hors corps).
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ==="
python3 tools/graphe_document.py --porte
=== porte-lecteur
#!/bin/bash
# porte-lecteur.sh — R0.2 : à 30 % du budget, le contrôleur retrouve la réponse.
#
# POURQUOI CETTE PORTE EXISTE. Un contrôleur de lecture peut sembler bon et ne rien
# sélectionner : sans comparaison à la lecture intégrale, sans contrôle aléatoire et sans
# contrôle « sans but », on mesure une impression. Cette porte exige les quatre à la fois :
# récupération ≥ 90 % à 30 % du budget, réponse préservée, hasard nettement plus bas, et
# closed-book silencieux.
set -u
cd "$(dirname "$0")/.."
echo "==
… [6715 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' reports/rapport-r44-ocr-pilote.md", "description": "Lire la fiche pilote OCR"}`

  ```
# R4.4 — l'OCR lit dix pages à 4,48 % de WER, parité 90 %, et la page « photo » tombe à 26,7 %

> **Objet.** La ligne R4.4 était **bloquée** par une ressource absente, pas par une question
> ouverte : « aucun OCR installé (ni tesseract ni pytesseract) ». Ce pilote installe l'OCR sans
> root, le branche sur le graphe de document de R0.1 et mesure ce qu'il vaut : WER contre le
> texte natif de la **même page**, parité des réponses sur les questions du banc R0.3, et deux
> contrôles négatifs. **Il ne clôt pas R4.4** : les pages sont des **rendus propres**, pas des
> scans — le contrôle dégradé mesure exactement ce qui manque encore.

## Dispositif

- **Dix pages** rendues à **300 dpi** depuis **6 PDF** du corpus gelé, **3 langues** (fr, en, es) :
  les 9 pages qui portent les **30 questions** du banc `bench-complet.json` (type juridique) et
  une page de plus (`A_RES_80_1-en` p2) pour le WER.
- **OCR** : tesseract **5.5.3** (leptonica 1.87.0), langues `fra`, `eng`, `spa`, installé **sans
  root** par [`tools/installer_ocr.sh`](../tools/installer_ocr.sh) dans `work/ocr/root`.
- **Lecture** : sortie TSV de tesseract (mots, boîtes, **confiance**) → blocs
  ([`graphe_document_ocr.py`](../
… [6194 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for p in document lecteur lecture balayage bloc-tableaux bloc-code bloc-maths; do echo \"=== $p\"; bash tools/porte-$p.sh >/tmp/porte-$p.log 2>&1; echo \"exit=$? $(tail -1 /tmp/porte-$p.log)\"; done", "description": "Rejouer les port … [41 caractères tronqués]`

  ```
started background job bash-4002
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-ocr-scans.sh >/tmp/porte-ocr-scans.log 2>&1; echo exit=$?; tail -3 /tmp/porte-ocr-scans.log", "description": "Rejouer la porte des scans OCR", "run_in_background": true}`

  ```
started background job bash-4003
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls docs/pilotage/backlog/ | grep -i '^R' ; echo '---'; ls docs/pilotage/backlog/ | grep -i 'R0\\|R1\\|R2\\|R3\\|R4\\|R5' | head -40", "description": "Lister les fiches backlog R"}`

  ```
R01-graphe-document.md
R02-controleur-lecture.md
R03-banc-lecture-rapide.md
R04-tete-survol.md
R05-tete-balayage.md
R06-tete-relecture.md
R07-routeur-extractif-generatif.md
R11-contexte-hierarchique.md
R12-curriculum-contexte.md
R13-tokenisation-bpe.md
R21-memoire-travail-gist.md
R22-memoire-episodique.md
R31-restitution-sft.md
R32-citations-provenance.md
R41-bloc-tableaux.md
R42-bloc-code.md
R43-bloc-maths.md
R44-encodeur-visuel.md
R51-lecture-croisee.md
R52-multilingue-decodeur.md
---
R01-graphe-document.md
R02-controleur-lecture.md
R03-banc-lecture-rapide.md
R04-tete-survol.md
R05-tete-balayage.md
R06-tete-relecture.md
R07-routeur-extractif-generatif.md
R11-contexte-hierarchique.md
R12-curriculum-contexte.md
R13-tokenisation-bpe.md
R21-memoire-travail-gist.md
R22-memoire-episodique.md
R31-restitution-sft.md
R32-citations-provenance.md
R41-bloc-tableaux.md
R42-bloc-code.md
R43-bloc-maths.md
R44-encodeur-visuel.md
R51-lecture-croisee.md
R52-multilingue-decodeur.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ocr-cegep-64.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ocr-cegep-64.md</path>
<type>file</type>
<content>
1: # D — le corpus CEGEP à 64 documents est contaminé : DOC2 (val) est un quasi-doublon du train
2: 
3: > **Ligne de roadmap** : D · **Date** : 2026-11-04 · **Verdict** : ⛔ **le re-split 64 (2/1/1) est
4: > contaminé** — **DOC2**, placé en **val**, a **18/20 fenêtres de 500 o** déjà dans l'ancien train
5: > (**17 001 o contigus**, offsets 4 026 047 → 4 044 047) ; **DOC1** (train) est un quasi-doublon
6: > intra-train (**24/26** fenêtres, une fenêtre de **8 188 o exacte**). Le contrôle **8 Ko exact est
7: > à 0** et **ne le voit pas** (les deux scans du même document ont été OCRisés deux fois, le texte
8: > diffère légèrement). ✅ **le corpus propre à 62 documents est prêt et vérifié** :
9: > `work/ocr/cegep64/propre/` — 60 anciens + **Choquette** (6 p) + **Assurance** (1 p), DOC1/DOC2
10: > écartés ; 8 Ko 0, 500 o 0, val/test anciens intacts.
11: >
12: > **Dispositif** : `tools/verifie_contamination.py` (fenêtres de 8 192 o) + contrôle exact de
13: > fenêtres de 500 o (pas de 1 000) ; corpus `data/corpus_ocr_cegep/` (état 15 h 57) ; corpus propre
14: > préparé ; d
… [5397 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R44-encodeur-visuel.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R44-encodeur-visuel.md</path>
<type>file</type>
<content>
1: # R44 — Encodeur visuel / OCR (scans, figures, layout)
2: 
3: > **Statut** : partiel · **Priorité** : P3 · **Programme** : R · **Dépend de** : R41, R42, R43 · **Bloqué par** : — (l'OCR est installé ; restent les scans réels, le layout et les exposants)
4: > **Ligne de roadmap** : R4.4 · **Fiche de résultat attendue** : rapport-r44-encodeur-visuel.md (à créer dans `reports/`)
5: > **Résumé** : Lire les pages scannées, les figures et le layout, et retrouver la réponse du texte natif.
6: > **Glossaire** : [OCR](../../theorie/glossaire/entrees/ocr.md) · [layout](../../theorie/glossaire/entrees/layout.md) · [WER](../../theorie/glossaire/entrees/wer.md).
7: 
8: ## Le besoin
9: 
10: Une partie des documents n'existe qu'en image. Sans OCR et layout, Drave ne lit que le texte déjà extrait. C'est le dernier bloc de R4, après les blocs structurels classiques.
11: 
12: ## Le contrat
13: 
14: | élément | contenu |
15: |---|---|
16: | **entrée** | une image ou une page PDF et une question |
17: | **sortie** | des régions, du texte et un layout ; la même réponse
… [3728 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum data/corpus_ocr_cegep/train.txt data/corpus_ocr_cegep/val.txt data/corpus_ocr_cegep/test.txt 2>&1; echo '---'; wc -c data/corpus_ocr_cegep/train.txt data/corpus_ocr_cegep/val.txt data/corpus_ocr_cegep/test.txt 2>&1; echo '- … [94 caractères tronqués]`

  ```
f57154df3ca5ecbd487c649c9177fddc7b4ffc2073f3488b8a2d1ad436d3da47  data/corpus_ocr_cegep/train.txt
dd605833f27eab63df46de3437b1e74b479c2c3abcd6ea683365647063ccd0e1  data/corpus_ocr_cegep/val.txt
1c9ab73459c1e44ae7c1e23e46210091c54a5be360df698bdad150e9c1153b84  data/corpus_ocr_cegep/test.txt
---
4440987 data/corpus_ocr_cegep/train.txt
  12536 data/corpus_ocr_cegep/val.txt
  10524 data/corpus_ocr_cegep/test.txt
4464047 total
---
test.txt
train.txt
val.txt
  ```

### 👤 Utilisateur

background job bash-4002 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for p in document lecteur lecture balayage bloc-tableaux bloc-code bloc-maths; do echo "=== $p"; bash tools/porte-$p.sh >/tmp/porte-$p.log 2>&1; echo "exit=$? $(tail -1 /tmp/porte-$p.log)"; done) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-4002"}`

  ```
=== document
exit=0 ✅ porte document verte
=== lecteur
exit=0 ✅ porte lecteur verte
=== lecture
exit=0 ✅ porte lecture verte
=== balayage
exit=0 ✅ porte balayage verte
=== bloc-tableaux
exit=0 ✅ porte bloc tableaux verte
=== bloc-code
exit=0 ✅ porte bloc code verte
=== bloc-maths
exit=0 ✅ porte bloc maths verte
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for p in document lecteur lecture balayage bloc-tableaux bloc-code bloc-maths; do echo \"=== $p\"; grep -E '✅|❌|fidélité|exactitude|rappel|WER|préservation|cellules|questions|pages|langues|0\\.[0-9]{3}|[0-9]+/[0-9]+' /tmp/porte-$p.lo … [78 caractères tronqués]`

  ```
=== document
  30 documents · 51 pages · 1466 régions
    data/onu/pdf/A_RES_80_1-en.pdf                         85 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-es.pdf                         93 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-fr.pdf                         91 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-ru.pdf                         95 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-zh.pdf                         83 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_10-en.pdf                       155 régions  fidélité 1.000
✅ les 50 pages sont découpées, les partitions exactes, le rejeu identique,
   la fidélité ≥ 0,99 et les trois contrôles négatifs se comportent comme prévu.
✅ porte document verte
=== lecteur
  tableau    sans_but           0.000  0.000   0.000     2153
  tableau    closed_book        0.000  0.000   0.000        0
  technique  integrale          1.000  0.784   0.750    10441
  technique  controlee_0.10     0.750  0.784   0.750      908
  technique  controlee_0.30     1.000  0.784   0.750     2567
  technique  controlee_0.50     1.000  0.784   0.750     3764
  technique  aleatoire_0.30     0.500  0.538   0.500     3131
  tec
… [2828 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in docs/pilotage/backlog/R11-contexte-hierarchique.md docs/pilotage/backlog/R12-curriculum-contexte.md docs/pilotage/backlog/R21-memoire-travail-gist.md docs/pilotage/backlog/R31-restitution-sft.md docs/pilotage/backlog/R51-lec … [168 caractères tronqués]`

  ```
=== docs/pilotage/backlog/R11-contexte-hierarchique.md
1:# R11 — Contexte hiérarchique et état de section
3:> **Statut** : spécifiée · **Priorité** : P1 · **Programme** : R · **Dépend de** : R01, N1, N2
5:> **Résumé** : Lire par sections avec un état de section, sans exiger que l'attention voie toute la page.
10:Le natif surapprend 129 octets et échoue à 130–256. Avant d'allonger le contexte brut, il faut une hiérarchie : span → paragraphe → section → document, avec un état qui résume chaque section.
12:**Ordre arrêté le 2026-10-29** : c'est **N2** qui porte la hiérarchie (l'état de section, 3 graines) ; R11 mesure la fenêtre qui en résulte et n'ouvre donc qu'après N2. La mesure reste ici : PPL à 1 000 octets, aiguille native, stabilité.
18:| **entrée** | des octets, des frontières de section (R01) et un état courant |
19:| **sortie** | un état de section et un état de document, utilisables par le décodeur |
20:| **coût** | coût linéaire en octets, mémoire d'état bornée |
=== docs/pilotage/backlog/R12-curriculum-contexte.md
3:> **Statut** : spécifiée · **Priorité** : P1 · **Programme** : R · **Dépend de** : R11 · **Contraint par** : les cinq négatifs 129–256
10:Les essais 130, 136,
… [1282 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in rapport-r01-graphe-document rapport-r02-controleur rapport-r03-banc-complet rapport-r03-banc-durci rapport-r04-tete-survol rapport-r05-balayage rapport-r06-pipeline rapport-r07-routeur; do echo \"##### $f\"; sed -n '1,14p' r … [76 caractères tronqués]`

  ```
##### rapport-r01-graphe-document
# R0.1 — le graphe de document : 51 pages, partitions exactes, fidélité 1,000

> **Ligne de roadmap** : R0.1 · **Date** : 2026-10-29 · **Verdict** : ✅ la découpe est
> mesurée — partition exacte, provenance exacte, rejeu identique, et les trois contrôles
> négatifs se comportent comme prévu.
>
> **Dispositif** : 30 documents, **51 pages**, 5 formats ; `tools/graphe_document.py` ;
> porte `tools/porte-document.sh` ; JSON brut
> [`r01-graphe-document.json`](r01-graphe-document.json) ; spécification
> [`document-graph.md`](../docs/implantation/document-graph.md).

## La question

Un document peut-il être découpé en **régions typées** (titre, section, paragraphe, tableau,

##### rapport-r02-controleur
# R0.2 — le contrôleur de lecture : 100 % de récupération à 30 % du budget

> **Ligne de roadmap** : R0.2 (et première tranche de R0.3) · **Date** : 2026-10-29 ·
> **Verdict** : ✅ le contrôleur **préserve la lecture intégrale** à **30 %** du budget sur
> les **5 types** — et le plafond n'est pas le contrôleur, c'est le **lecteur**.
>
> **Dispositif** : 20 questions, 5 types, 5 documents ; `tools/lecteur_controleur.py` +
> `tools/banc_lecture.py` ; porte `
… [5750 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -nE 'récupère|agrégat|moyenne|1,000|0,231|0,375|249|331|0,871|0,373' /tmp/porte-lecteur.log | head -20; echo '---'; python3 tools/banc_complet.py --help 2>&1 | head -20; echo '---'; python3 tools/routeur.py --help 2>&1 | head -2 … [54 caractères tronqués]`

  ```
30:  tableau    controlee_0.10     1.000  0.030   0.250     3312
46:✅ à 30 % du budget, la lecture contrôlée récupère ≥ 90 % des passages de la
---
usage: banc_complet.py [-h] [--ecrit ECRIT] [--verifie VERIFIE]

R0.3 — le banc complet (30 documents).

options:
  -h, --help         show this help message and exit
  --ecrit ECRIT
  --verifie VERIFIE
---
usage: routeur.py [-h] [--json JSON]

R0.5 — le routeur extractif/génératif.

options:
  -h, --help   show this help message and exit
  --json JSON
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -30 /tmp/porte-lecteur.log; echo '---'; sed -n '1,35p' reports/rapport-lecteur-multifichiers.md", "description": "Agrégat R0.2 et fiche multifichiers"}`

  ```
juridique  sans_but           0.500  0.000   0.000      315
  juridique  closed_book        0.000  0.000   0.000        0
  prose      integrale          1.000  0.750   0.750     7082
  prose      controlee_0.10     1.000  0.750   0.750      463
  prose      controlee_0.30     1.000  0.750   0.750      463
  prose      controlee_0.50     1.000  0.750   0.750      463
  prose      aleatoire_0.30     0.000  0.000   0.000     2117
  prose      melangee_0.30      1.000  0.750   0.750      463
  prose      sans_but           0.750  0.000   0.000     1730
  prose      closed_book        0.000  0.000   0.000        0
  tableau    integrale          1.000  0.030   0.250    39239
  tableau    controlee_0.10     1.000  0.030   0.250     3312
  tableau    controlee_0.30     1.000  0.030   0.250     8599
  tableau    controlee_0.50     1.000  0.030   0.250    10682
  tableau    aleatoire_0.30     0.250  0.074   0.250    11765
  tableau    melangee_0.30      1.000  0.030   0.250     8601
  tableau    sans_but           0.000  0.000   0.000     2153
  tableau    closed_book        0.000  0.000   0.000        0
  technique  integrale          1.000  0.784   0.750    10441
  technique  controlee_0
… [1874 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-4003"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -lh work/n2ac/*.json 2>/dev/null | tail -20; echo '---'; cat work/n2ac/rope1024-20k.pt.json 2>/dev/null | head -40; echo '---'; tail -5 work/n2ac/rope1024-20k.log 2>/dev/null", "description": "Vérifier métadonnées du run 1024-20k" … [1 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 199  2 nov 20:29 work/n2ac/queue-rope256-2000.json
-rw-r--r--. 1 stephane stephane 201  2 nov 20:30 work/n2ac/queue-rope512-2000.json
-rw-r--r--. 1 stephane stephane 134  2 nov 17:53 work/n2ac/queue-rope512.json
-rw-r--r--. 1 stephane stephane 132  2 nov 17:02 work/n2ac/queue-rope.json
-rw-r--r--. 1 stephane stephane 137  2 nov 18:49 work/n2ac/queue-zero-rope-40k.json
-rw-r--r--. 1 stephane stephane 133  2 nov 18:27 work/n2ac/queue-zero-rope.json
-rw-r--r--. 1 stephane stephane 529  2 nov 22:30 work/n2ac/rope1024-20k.pt.json
-rw-r--r--. 1 stephane stephane 531  2 nov 20:16 work/n2ac/rope1024-2.5k.pt.json
-rw-r--r--. 1 stephane stephane 532  4 nov 18:18 work/n2ac/rope2048-10k.pt.json
-rw-r--r--. 1 stephane stephane 531  2 nov 22:22 work/n2ac/rope2048-1.25k.pt.json
-rw-r--r--. 1 stephane stephane 536  3 nov 01:33 work/n2ac/rope2048-12.5k.pt.json
-rw-r--r--. 1 stephane stephane 532  4 nov 21:09 work/n2ac/rope2048-20k.pt.json
-rw-r--r--. 1 stephane stephane 527  2 nov 17:20 work/n2ac/rope-20k-g2.pt.json
-rw-r--r--. 1 stephane stephane 524  2 nov 16:44 work/n2ac/rope-20k.pt.json
-rw-r--r--. 1 stephane stephane 525  2 nov 17:51 work/n2ac/rope512-5k.pt.json
… [1093 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/n2-r12-2048.json'))\nfor k in ('loi_1024_20k','entrainement_1024_20k','dispositif','miroir_1024'):\n    print('==',k)\n    print(json.dumps(d.get(k),ensure_ascii=False)[:900])\ … [49 caractères tronqués]`

  ```
== loi_1024_20k
{"fichier": "rope1024-20k.pt", "params": 34301224, "positions": "rope", "ppl": {"val_fr": {"128": 2.9955, "256": 2.8513, "512": 2.7201, "1000": 2.6256, "2000": 2.5757, "4000": 2.5429}, "val_big": {"128": 3.3086, "256": 3.1437, "512": 3.015, "1000": 2.9055, "2000": 2.8726, "4000": 2.8828}}, "permute_fr": 195.3449, "litterature": 5.6071, "anglais": 7.8817, "wikitext2": 8.7751, "corpus_propre": 7.7208}
== entrainement_1024_20k
{"modele": "drave-n0-rope", "parametres": 34301224, "corpus": "data/wiki_fr/propre/train.txt", "octets": 186089472, "pas": 17500, "seq": 1024, "lot": 8, "lr": 0.0003, "graine": 1, "window": 1024, "positions": "rope", "init": "work/n2ac/rope1024-2.5k.pt", "perte_finale": 1.0205986499786377, "ppl_val": 2.66090749837826, "jetons_val": 65536, "tetes": true, "drvm": "work/n2ac/rope1024-20k.drvm", "sha256_drvm": "76628995a51cd54d52d564112f557bacfbea5f6119947c7b20f710e060f4e9af", "duree_s": 8000.274173498154}
== dispositif
{"modele": "drave-n0 34,3 M (384/512), RoPE, seq = fenêtre", "corpus": "data/wiki_fr/propre/train.txt (186 Mo) + canal", "budget": "20,5 Mo vus pour la loi (20 000 / 5 000 / 2 500 / 1 250 pas) ; 164 Mo pour le run à 20 000 pas", "cont
… [516 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'gold\\|GOLD\\|REEL\\|charger\\|phrases' tools/tests/linguistique/qualifier_neuronal.py | head -30; echo '---'; sed -n '185,235p' tools/tests/linguistique/qualifier_neuronal.py", "description": "Vérifier le corpus du banc tag … [5 caractères tronqués]`

  ```
2:"""qualifier_neuronal.py — qualifie un tagger neuronal local sur le gold (180 phrases, 804 tokens).
8:passe ; le JSON sort dans `reports/` et la fiche dans `reports/rapport-pensee-gold-neuronal.md`.
10:    python3 tools/tests/linguistique/qualifier_neuronal.py --demarrer --sortie reports/pensee-gold-neuronal.json
34:GOLD = pathlib.Path(__file__).with_name("gold.json")
35:SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")
40:def charger() -> list[dict]:
41:    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
42:    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
54:def _score(annotations: dict[str, bl.Annotation], phrases: list[dict]) -> dict:
59:    for p in phrases:
90:def _sources(annotations: dict[str, bl.Annotation], phrases: list[dict]) -> dict:
91:    hand = [p for p in phrases if p["source"] == "hand"]
92:    synth = [p for p in phrases if p["source"] == "synth"]
93:    return {"all": _score(annotations, phrases), "hand": _score(annotations, hand),
97:def _controles(phrases: list[dict]) -> dict:
99:    n = sum(len(p["mots"]) for p in phrases)
100:    majoritaire = sum(1 for p in phrases for m in p["mots"] if m["pos"] == "NOUN")
… [3144 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-gold-neuronal.json'))\nprint(json.dumps({k:d[k] for k in ('date','gold','tagger','seuils','verdict')},ensure_ascii=False,indent=1)[:1200])\nprint('modele fichiers:')\nfo … [116 caractères tronqués]`

  ```
{
 "date": "2026-11-02 16:52 EST",
 "gold": {
  "phrases": 180,
  "tokens": 804,
  "hand": 20,
  "synth": 160
 },
 "tagger": {
  "classe": "NeuronalLLMPOS",
  "confiance": 0.6,
  "tokenisation": "Heuristique._mots (mot/nombre)",
  "contrainte": "grammaire GBNF, une classe par token"
 },
 "seuils": {
  "neuronal_all": true,
  "cascade_all": true,
  "cascade_synth": true,
  "cascade_hand_sans_regression": true,
  "aucun_refus": true,
  "controles_sous_0_40": true
 },
 "verdict": true
}
modele fichiers:
  /home/stephane/Data13TB/stephane/GitHub/Qtrinet/models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf 3993201344
  /home/stephane/Data13TB/stephane/GitHub/Qtrinet/models/qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf 689872288
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/qualifier_neuronal.py --limite 1 --sortie /tmp/tagger-essai.json 2>&1 | head -5; echo exit=${PIPESTATUS[0]}", "description": "Vérifier que le tagger est rejouable"}`

  ```
modèle absent : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf
exit=1
  ```

- **bash** `{"command": "ls -lh /home/stephane/IA/cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/*/ 2>/dev/null | head -20; echo '---'; du -sh /home/stephane/IA/cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct 2>/dev/null", "description": "Vérifier le cache HF du 7B"}`

  ```
total 16K
lrwxrwxrwx. 1 stephane stephane 52 19 oct 07:31 config.json -> ../../blobs/0178295f88afc3c7f279ed284f961f8c1be00654
lrwxrwxrwx. 1 stephane stephane 52 19 oct 07:31 generation_config.json -> ../../blobs/0eb3c536657dcd12626e09eca4b6198c0cbcde1e
lrwxrwxrwx. 1 stephane stephane 52 19 oct 07:31 LICENSE -> ../../blobs/6634c8cc3133b3848ec74b9f275acaaa1ea618ab
lrwxrwxrwx. 1 stephane stephane 52 19 oct 07:31 merges.txt -> ../../blobs/20024bfe7c83998e9aeaf98a0cd6a2ce6306c2f0
lrwxrwxrwx. 1 stephane stephane 76 19 oct 07:33 model-00001-of-00004.safetensors -> ../../blobs/a1333e6293854747c481288ea83b348226af178dd565c49b6f9495ba1966aba7
lrwxrwxrwx. 1 stephane stephane 76 19 oct 07:33 model-00002-of-00004.safetensors -> ../../blobs/f5d25a2772cb825164a2a2c0fb6d51a87e282abf21e4dd75bc5cfb3cd0ea6185
lrwxrwxrwx. 1 stephane stephane 76 19 oct 07:33 model-00003-of-00004.safetensors -> ../../blobs/8efdec4c1bc12317ae1a38dc42b595ce777738a64deea3fcb8a0a91381bcdfd5
lrwxrwxrwx. 1 stephane stephane 76 19 oct 07:33 model-00004-of-00004.safetensors -> ../../blobs/1a72d403cdf0c1ec3cb7f289f17b394a01e64394c2e9b3c0f94dbce3faf879bd
lrwxrwxrwx. 1 stephane stephane 52 19 oct 07:31 model.safetensors.index.json
… [612 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-4003"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in R21-memoire-travail-gist R22-memoire-episodique R31-restitution-sft R32-citations-provenance R51-lecture-croisee R52-multilingue-decodeur; do echo \"##### $f\"; sed -n '1,42p' docs/pilotage/backlog/$f.md; echo; done", "descr … [38 caractères tronqués]`

  ```
##### R21-memoire-travail-gist
# R21 — Mémoire de travail et gist

> **Statut** : spécifiée · **Priorité** : P1 · **Programme** : R · **Dépend de** : R01, R11 · **Contraint par** : la mémoire à 8 pas est négative (mesuré)
> **Ligne de roadmap** : R2.1 · **Fiche de résultat attendue** : rapport-r21-memoire-gist.md (à créer dans `reports/`)
> **Résumé** : Tenir un état de résumé, une table d'entités et de faits, et un tampon en entrée.
> **Glossaire** : [gist](../../theorie/glossaire/entrees/gist.md) · [closed-book](../../theorie/glossaire/entrees/closed-book.md) · [span](../../theorie/glossaire/entrees/span.md).

## Le besoin

Sans gist, le modèle ne comprend pas un document en plusieurs sections. N5 est négatif : le réseau ne retient pas le signal à 8 pas, mais le tampon gelé lit +0,879. Il faut donc commencer par le tampon, pas par un entraînement de mémoire.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | les sections lues (R01), les états de section (R11) et une question éventuelle |
| **sortie** | un gist : résumé, entités, faits, dates, citations ; état borné |
| **coût** | coût linéaire en sections ; le gist ne dépasse pas une taille fixée |
| **trace** | chaqu
… [9605 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'N4\\|24/24\\|0/4' reports/rapport-n4* reports/*n4* 2>/dev/null | head -20; echo '---'; ls reports/ | grep -i 'n4\\|restitution'", "description": "Vérifier l'état N4 et restitution"}`

  ```
reports/rapport-n4-dessin-b.md:1:# N4 — le chemin court entraîné (dessin B) : ÷1,2 à ÷1,9 selon la profondeur, et deux corrections de mesure
reports/rapport-n4-dessin-b.md:3:> Campagne : **cerveau** · expérience : dessin **B** de N4 (« les couches basses apprennent »), et
reports/rapport-n4-porte-execution.md:1:# N4 — la porte d'exécution : le chemin court entraîné est mesuré par le MOTEUR (÷1,47 et ÷1,24)
reports/rapport-n4-dessin-b.md:1:# N4 — le chemin court entraîné (dessin B) : ÷1,2 à ÷1,9 selon la profondeur, et deux corrections de mesure
reports/rapport-n4-dessin-b.md:3:> Campagne : **cerveau** · expérience : dessin **B** de N4 (« les couches basses apprennent »), et
reports/rapport-n4-porte-execution.md:1:# N4 — la porte d'exécution : le chemin court entraîné est mesuré par le MOTEUR (÷1,47 et ÷1,24)
---
rapport-n4-dessin-b.md
rapport-n4-porte-execution.md
rapport-restitution.md
restitution-fra-flux.json
restitution-fra.json
restitution.json
restitution-mesures.json
restitution-udhr-flux.json
restitution-udhr.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '0,879\\|0.879' reports/ docs/ --include='*.md' | head -10; echo '---'; grep -rn 'tampon' docs/pilotage/roadmap.md docs/theorie/lecture-rapide.md reports/rapport-*.md | grep -i '0,8\\|entrée\\|R2' | head -10", "description": … [40 caractères tronqués]`

  ```
reports/rapport-memoire-travail-n5.md:11:> déjà `v[t−8]` à **+0,879** et l'entraînement le porte à **+0,964** — et le moteur, mesuré par
reports/rapport-memoire-travail-n5.md:26:| **gelé** (sonde seule) | **−1,091** | **+0,879** |
reports/rapport-memoire-travail-n5.md:36:* **avec la structure, le passé est lisible sans entraîner le réseau** (+0,879) : le tampon écrit
reports/rapport-memoire-travail-n5.md:57:  **+0,879 en linéaire** et le moteur à **−0,338 en linéaire / +0,766 en non linéaire**. Les deux
reports/rapport-memoire-travail-n5.md:76:  Un LoRA entraîné pour lire ce tampon apporte **+0,085** de R² (0,879 → 0,964) au prix de 1,4 M de
reports/rapport-memoire-travail-n5.md:78:* **ce qui reste vrai** : le réseau *peut* apprendre à **lire** une structure (0,879 → 0,964), donc
reports/rapport-pensee-pragmatique-neuronale.md:18:| syntagmes F1 | 0,8795 |
reports/rapport-pensee-quatre-modes-run2.md:6:> gagne encore** : POS **0,9389** (+0,008), syntagmes **0,8241**, tête **0,8797**, acte 0,9954.
reports/rapport-pensee-quatre-modes-run2.md:18:| neuronal | 0,9309 | **0,9389** | 0,8241 | 0,8797 | 0,0000 |
reports/rapport-pensee-quatre-modes-run2.md:21:| **parallele_niveau** | 0,9309 | 
… [1734 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'mémoire à 8 pas\\|8 pas' reports/*.md | head -10; echo '---'; sed -n '1,35p' reports/rapport-n2-r11.md", "description": "Trouver le négatif mémoire à 8 pas"}`

  ```
reports/INDEX.md:568:| [rapport-pensee-seule.md](rapport-pensee-seule.md) | B13 — la politique seule : 8 pas, 15/15 buts, sans A* |
reports/rapport-budget-decision.md:69:* **un seul contexte** (8 pas) : le coût des clés croît avec la position, donc la part de
reports/rapport-c2-recurrence.md:9:> (α = 0,5) et **0,125** (α = 1,0) ; la lecture du signal d'il y a 8 pas passe de **−0,350** à
reports/rapport-c8-peripherie.md:10:> **pas** le signal d'il y a 8 pas (R² = **−0,973**) : le modèle ne garde rien de linéairement
reports/rapport-c8-peripherie.md:89:| **ligne à retard de 8 pas** (tampon) | **+1,000** (exact par construction) |
reports/rapport-c8-peripherie.md:93:1. la tâche **n'est pas dure** : un tampon de 8 pas la résout exactement. Le plancher existe et il
reports/rapport-c8-peripherie.md:117:| **récurrent + tampon de 8 pas** | R² +0,852 | R² **+0,283** |
reports/rapport-cerveau-corrections.md:175:**Mesure du 2026-10-29.** Le pipeline M1 → M4 → M8 passait `ItemType.contexte` — un **résumé**
reports/rapport-memoire-travail-n5.md:5:> Question : le réseau peut-il **apprendre** à retenir un scalaire injecté 8 pas plus tôt — ou
reports/rapport-memoire-travail-n5.md:8:> 2 048 pas, ob
… [2528 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-4003", "timeout_ms": 120000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -15 /tmp/porte-ocr-scans.log; echo '---'; ps -o pid,etime,cmd -C python3 2>/dev/null | grep -E 'mesurer|ocr|scan' | head -5", "description": "Suivre la porte OCR"}`

  ```
100 mesures en 107 s → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/r44/mesure.json
--- 2. les colonnes (10 pages × 2 versions × 3 familles)

  ✅ deux colonnes · propre : WER ≤ 3% (mesuré 0.5%)
  ✅ deux colonnes · photocopie : WER ≤ 6% (mesuré 1.0%)
  ✅ deux colonnes · photo : WER ≤ 20% (mesuré 6.5%)
  ✅ contrôle sans gouttière · photo : ≥ 50 % (mesuré 88.3%)
  ✅ mono-colonne · photo : écart ≤ 0,5 pt (mesuré 0.00%)
  ✅ contrôle sans gouttière · propre : ≥ 50 % (mesuré 89.4%)
  ✅ mono-colonne · propre : écart ≤ 0,5 pt (mesuré 0.00%)
  ✅ contrôle sans gouttière · photocopie : ≥ 50 % (mesuré 90.1%)
  ✅ mono-colonne · photocopie : écart ≤ 0,5 pt (mesuré 0.00%)

  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/r44/colonnes.json
--- 3. les tableaux (10 pages × 3 familles)
---
3621255       02:32 python3 tools/mesurer_tables.py --porte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee-gold-etat-r.json'))\nfor part in ('hand','reel_new','synthetique'):\n    print('==',part)\n    for lecture in ('heuristique','cascade'):\n        a=d[lecture][part]\n       … [576 caractères tronqués]`

  ```
== hand
  heuristique POS 0.8952 ferme 0.8947 ouvert 0.8958 tokens 105
   synt F1 0.7288 tete F1 0.8288 acte 1.0
  cascade POS 0.8952 ferme 0.8947 ouvert 0.8958 tokens 105
   synt F1 0.7288 tete F1 0.8288 acte 1.0
== reel_new
  heuristique POS 0.8754 ferme 0.9277 ouvert 0.8204 tokens 2375
   synt F1 0.6251 tete F1 0.7458 acte 0.9954
  cascade POS 0.8754 ferme 0.9277 ouvert 0.8204 tokens 2375
   synt F1 0.6251 tete F1 0.7458 acte 0.9954
== synthetique
  heuristique POS 0.7568 ferme 0.9449 ouvert 0.637 tokens 699
   synt F1 0.7113 tete F1 0.8336 acte 1.0
  cascade POS 0.7568 ferme 0.9449 ouvert 0.637 tokens 699
   synt F1 0.7113 tete F1 0.8336 acte 1.0
--- langues
['date', 'niveaux', 'langue', 'controle_permute', 'echantillons', 'niveaux_vus', 'niveaux_manquants', 'controles', 'verdicts', 'ok']
langue {"langues_profil": 398, "articles_test": 447, "accuracy": 0.9687, "accuracy_script": 1.0, "duree_s": 4.882, "langues": {"hus": [3, 3], "oci": [7, 6], "roh": [7, 7], "ron": [3, 3]}}
niveaux ["graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours", "pragmatique", "document"]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, pathlib\nRACINE=pathlib.Path('.').resolve()\nsys.path.insert(0,str(RACINE/'tools'))\nsys.path.insert(0,str(RACINE/'tools/tests/linguistique'))\nimport bloc_linguistique as bl\nimport evaluer_gold a … [813 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 12, in <module>
AttributeError: module 'evaluer_gold' has no attribute '_score'
[exit code: 1]
  ```

### 👤 Utilisateur

background job bash-4003 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-ocr-scans.sh >/tmp/porte-ocr-scans.log 2>&1; echo exit=$?; tail -3 /tmp/porte-ocr-scans.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-4003"}`

  ```
exit=0

  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/r44/tables.json
✅ porte OCR-scans verte : familles, colonnes et tableaux tiennent leurs planchers
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '^def ' tools/tests/linguistique/evaluer_gold.py | head -20", "description": "Lister les fonctions d'évaluation"}`

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
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, pathlib\nRACINE=pathlib.Path('.').resolve()\nsys.path.insert(0,str(RACINE/'tools'))\nsys.path.insert(0,str(RACINE/'tools/tests/linguistique'))\nimport bloc_linguistique as bl\nimport evaluer_gold a … [816 caractères tronqués]`

  ```
heuristique 180: 0.7749 ferme 0.9362 ouvert 0.6632 tokens 804
syntagme 0.7135 tete 0.8329 acte 1.0
hand 0 0.0 0
synth 0 0.0 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -E '✅|❌|WER|préservation|cellules|lignes|formes|page noire' /tmp/porte-ocr-scans.log | tail -35", "description": "Extraire le bilan de la porte OCR"}`

  ```
✅ tesseract 5.5.3 · langues : eng fra osd spa 
  contrôle page noire : 0 mot(s) lu(s), 0 région(s)
  ✅ page noire : aucun mot lu
  ✅ fax · dev : WER ≤ 25% (mesuré 21.9%)
  ✅ fax · dev : préservation ≥ 30% (mesuré 56.7%)
  ✅ fax · test : WER ≤ 25% (mesuré 15.5%)
  ✅ papier · dev : WER ≤ 10% (mesuré 6.9%)
  ✅ papier · dev : préservation ≥ 55% (mesuré 90.0%)
  ✅ papier · test : WER ≤ 10% (mesuré 6.4%)
  ✅ photo · dev : WER ≤ 10% (mesuré 6.7%)
  ✅ photo · dev : préservation ≥ 60% (mesuré 90.0%)
  ✅ photo · test : WER ≤ 10% (mesuré 5.7%)
  ✅ photocopie · dev : WER ≤ 8% (mesuré 6.3%)
  ✅ photocopie · dev : préservation ≥ 60% (mesuré 93.3%)
  ✅ photocopie · test : WER ≤ 8% (mesuré 4.7%)
  ✅ propre · dev : WER ≤ 6% (mesuré 4.1%)
  ✅ propre · dev : préservation ≥ 85% (mesuré 96.7%)
  ✅ propre · test : WER ≤ 6% (mesuré 3.0%)
  ✅ deux colonnes · propre : WER ≤ 3% (mesuré 0.5%)
  ✅ deux colonnes · photocopie : WER ≤ 6% (mesuré 1.0%)
  ✅ deux colonnes · photo : WER ≤ 20% (mesuré 6.5%)
  ✅ contrôle sans gouttière · photo : ≥ 50 % (mesuré 88.3%)
  ✅ mono-colonne · photo : écart ≤ 0,5 pt (mesuré 0.00%)
  ✅ contrôle sans gouttière · propre : ≥ 50 % (mesuré 89.4%)
  ✅ mono-colonne · propre : écart ≤
… [562 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,40p' tools/banc_complet.py; echo '---'; grep -n 'def main\\|--verifie\\|--ecrit\\|verifie' tools/banc_complet.py | head -20", "description": "Comprendre banc_complet"}`

  ```
#!/usr/bin/env python3
"""banc_complet.py — R0.3 : 30 documents, 10 questions par document, générées et vérifiées.

POURQUOI GÉNÉRER. Trois cents questions annotées à la main, ce n'est pas une heure de travail :
c'est une semaine. Le banc **pilote** (20 questions main, R0.2) reste la référence de difficulté ;
le banc **complet** mesure la **sélection** à l'échelle, avec des questions **gabarit** :

  - on prend un passage qui porte une **valeur** (un nombre, une date) ;
  - on demande cette valeur par **deux mots rares** du passage (les moins fréquents du document,
    donc les plus discriminants) ;
  - le passage est le gold, la valeur est la réponse attendue.

Ce que ce banc mesure donc : le contrôleur va-t-il chercher le bon passage quand le document en
compte des centaines ? Ce qu'il ne mesure pas : la paraphrase — un gabarit partage forcément des
mots avec son gold. Les questions de paraphrase restent le banc pilote, et R0.3 « durci » est la
suite.

Usage :
  python3 tools/banc_complet.py --ecrit tools/tests/documents/bench-complet.json
  python3 tools/banc_complet.py --verifie tools/tests/documents/bench-complet.json
"""
from __future__ import annotations

import argparse
imp
… [1032 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/routeur.py --json /tmp/routeur-etat-r.json 2>&1 | tail -25; echo exit=${PIPESTATUS[0]}", "description": "Rejouer le routeur R0.5"}`

  ```
=== ROUTEUR EXTRACTIF / GÉNÉRATIF ===
  331 questions · 203 où les deux lecteurs diffèrent
  AUC du signal BM25   : 0.839
  AUC couverture       : 0.584
  AUC z                : 0.793
  AUC ratio            : 0.727
  AUC etendue          : 0.265
  AUC longueur (faux)  : 0.453
  AUC aléatoire        : 0.510
  exactitude : fixe extractif 0.719 · fixe modèle 0.269 · oracle 0.801
  testé sur lexical     (n=248) · fixe ext 0.871 · fixe modèle 0.234 · oracle 0.915
     seuil appris ailleurs · z           (seuil   4.62) → exactitude 0.819
     seuil appris ailleurs · ratio       (seuil  24.76) → exactitude 0.706
     seuil appris ailleurs · etendue     (seuil   0.17) → exactitude 0.234
     seuil appris ailleurs · couverture  (seuil   0.83) → exactitude 0.234
     seuil appris ailleurs · signal      (seuil   6.30) → exactitude 0.754
  testé sur paraphrase  (n= 83) · fixe ext 0.265 · fixe modèle 0.373 · oracle 0.458
     seuil appris ailleurs · z           (seuil   3.12) → exactitude 0.313
     seuil appris ailleurs · ratio       (seuil   8.03) → exactitude 0.313
     seuil appris ailleurs · etendue     (seuil   0.01) → exactitude 0.289
     seuil appris ailleurs · couverture  (seuil   0.4
… [142 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -lh tools/tests/documents/bench-complet.json 2>&1; python3 tools/banc_complet.py --verifie tools/tests/documents/bench-complet.json 2>&1 | tail -8; echo exit=${PIPESTATUS[0]}", "description": "Vérifier le banc complet R0.3"}`

  ```
-rw-r--r--. 1 stephane stephane 96K 29 oct 17:05 tools/tests/documents/bench-complet.json
248 questions · 30 documents · 5 types · 0 problème(s)
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -lh work/n2ac/miroir_copie.py work/n2ac/eval_production.py work/n2ac/eval_fenetre.py work/n2ac/chaine_1024.sh 2>&1; echo '---'; grep -n 'argparse\\|add_argument\\|def main' work/n2ac/miroir_copie.py 2>/dev/null | head -15", "descr … [43 caractères tronqués]`

  ```
ls: cannot access 'work/n2ac/miroir_copie.py': No such file or directory
-rw-------. 1 stephane stephane 1,5K  2 nov 19:56 work/n2ac/chaine_1024.sh
-rw-------. 1 stephane stephane 3,4K  2 nov 20:23 work/n2ac/eval_fenetre.py
-rw-------. 1 stephane stephane 3,1K  2 nov 20:03 work/n2ac/eval_production.py
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find . -name 'miroir_copie.py' -not -path './tools/docwatch/*' 2>/dev/null | head; echo '---'; ls work/n2ac/ | head -60", "description": "Chercher miroir_copie"}`

  ```
---
absolu-pos1152.drvm
absolu-pos1152.log
absolu-pos1152.pt
absolu-pos1152.pt.json
agrege_fenetre.py
agrege_production.py
agrege_r11.py
cap-1147m-128.drvm
cap-1147m-128.log
cap-1147m-128.pt
cap-1147m-128.pt.json
cap-1147m-512.drvm
cap-1147m-512.log
cap-1147m-512.pt
cap-1147m-512.pt.json
cap1147.out
cap-2165m-128.drvm
cap-2165m-128.log
cap-2165m-128.pt
cap-2165m-128.pt.json
cap-2165m-512.drvm
cap-2165m-512.log
cap-2165m-512.pt
cap-2165m-512.pt.json
cap2165.out
cappropre.out
chaine_1024.out
chaine_1024.sh
chaine_2048_10k.sh
chaine_2048_20k.sh
chaine_2048_2x10k.sh
chaine_2048_mix.out
chaine_2048_mix.sh
chaine_2048.sh
chaine_2048_wiki.out
chaine_2048_wiki.sh
chaine_capacite_propre.sh
chaine_capacite.sh
chaine_kd_60k.sh
chaine_kd_controle.sh
chaine_kd_production_propre.sh
chaine_kd_production.sh
chaine_kd.sh
chaine_mix2048_long.sh
chaine_porte.out
chaine_porte.sh
chaine_prod1024_60k.sh
chaine_prod1024_long.out
chaine_prod1024_long.sh
chaine_production.out
chaine_production.sh
chaine_prod_zero.out
chaine_prod_zero.sh
chaine_r1.out
chaine_r1.sh
chaine_zero.out
chaine_zero.sh
courbe-absolu.json
courbe-absolu.log
courbe-absolu-pos1152.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('tools/tests/documents/bench-complet.json'))\nprint(type(d), list(d)[:8] if isinstance(d,dict) else len(d))\nqs=d.get('questions') if isinstance(d,dict) else d\nprint('questions', len(q … [110 caractères tronqués]`

  ```
<class 'dict'> ['version', 'date', 'note', 'documents', 'questions']
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
TypeError: object of type 'int' has no len()
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('tools/tests/documents/bench-complet.json'))\nprint({k:(type(v).__name__, len(v) if hasattr(v,'__len__') else v) for k,v in d.items()})\nprint('questions field', d['questions'])\nfor k  … [199 caractères tronqués]`

  ```
{'version': ('int', 1), 'date': ('str', 10), 'note': ('str', 218), 'documents': ('list', 30), 'questions': ('int', 248)}
questions field 248
documents len 30 first keys ['chemin', 'source', 'type', 'questions']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find journal/sessions -name '*miroir*' -o -name '*aiguille*' 2>/dev/null | head -20; echo '---'; ls journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/ 2>/dev/null | head -30", "description": "Chercher les bancs dans la sessi … [7 caractères tronqués]`

  ```
---
agrege_fenetre.py
agrege_production.py
agrege_r11.py
chaine_1024.sh
chaine_2048_mix.sh
chaine_2048.sh
chaine_2048_wiki.sh
chaine_capacite.sh
chaine_kd.sh
chaine_mix2048_long.sh
chaine_porte.sh
chaine_prod1024_long.sh
chaine_production.sh
chaine_prod_zero.sh
chaine_r1.sh
chaine_zero.sh
cout_fenetre.py
distiller_natif.py
entrainer_rope.py
eval_200k.py
eval_fenetre.py
eval_longueurs.py
eval_production.py
init_figee.py
mirroir_copie.py
rope_model.py
table_200k.py
trajectoire.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'miroir_copie' reports/rapport-n2-*.md journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/ 2>/dev/null | head -10", "description": "Tracer le banc miroir"}`

  ```
reports/rapport-n2-fenetre.md:39:contexte 256/512/1 000/2 000), `miroir_copie.py`. Le témoin `mix-60k` repassé dans le même mètre
reports/rapport-n2-fenetre.md:144:- Bancs : `work/n2ac/eval_production.py`, `eval_fenetre.py`, `miroir_copie.py`,
reports/rapport-n2-r11.md:41:  (`eval_fenetre.py`), et le **miroir de copie** à distance (`miroir_copie.py`).
reports/rapport-n2-r11.md:167:`miroir_copie.py` plante un code de 16 octets deux fois dans du texte réel (8 sondes, remplissages
reports/rapport-n2-r11.md:212:  `work/n2ac/miroir_copie.py`, `work/n2ac/agrege_r11.py`.
journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/agrege_r11.py:28:    "miroir_copie_rope": "miroir-rope.json",
journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/agrege_r11.py:66:            "miroir de copie à distance (miroir_copie) — muet, voir la fiche",
journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/mirroir_copie.py:2:"""miroir_copie.py — le miroir de sortie de R1 : le modèle **restitue-t-il** un code vu ?
journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/agrege_fenetre.py:62:            "miroir de copie à distance (miroir_copie)",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work/n2ac/ | grep -i 'mirro\\|aiguille'; echo '---'; sed -n '1,40p' journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/mirroir_copie.py", "description": "Vérifier le nom réel du miroir"}`

  ```
mirroir_copie.py
---
#!/usr/bin/env python3
"""miroir_copie.py — le miroir de sortie de R1 : le modèle **restitue-t-il** un code vu ?

La PPL est une mesure d'**entrée** : elle dit que la suite est moins surprenante, pas que le
modèle a **lu** l'octet lointain. Ici, on plante un code de 16 octets **deux fois** dans du
texte réel (un remplissage différent par sonde), à `d` octets d'écart, et on demande au modèle
(teacher forcing) de **prédire** la seconde occurrence : justesse top-1 sur les 16 octets.

Attendu si la **fenêtre d'attention** est la contrainte (256 pour R1.1, 512 pour R1.2) :
  d ≤ 240 → le code est copiable (justesse élevée) ;
  d > 240 → justesse au hasard (1/256 ≈ 0,004).
C'est le **contrôle négatif** de R1.1 : le RoPE ne fait pas lire au-delà de la fenêtre ; il
fait seulement disparaître la table de positions absolues.

Le contexte fait 512 octets et les codes restent sous la position 512, donc **les deux schémas
de position sont dans leur plage entraînée** : l'écart mesuré ne peut pas venir d'une ligne de
table non entraînée.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/mirroir_copie.py <point.pt> [--rope] [--sortie x.json]
"""
from __future__ import ann
… [393 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-ocr.sh >/tmp/porte-ocr.log 2>&1; echo exit=$?; tail -5 /tmp/porte-ocr.log", "description": "Rejouer la porte OCR pilote", "run_in_background": true}`

  ```
started background job bash-4154
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nfor f in ('reports/r44-reel.json','reports/r44-reel-second.json','reports/r44-scans.json'):\n    d=json.load(open(f))\n    print('==',f, list(d)[:12])\n    for k in ('reference','livres','pages','agrega … [151 caractères tronqués]`

  ```
== reports/r44-reel.json ['date', 'ligne', 'nature', 'reference', 'djvu', 'source', 'note_colonnes', 'agregat', 'pages', 'dispositif']
  reference "couche OCR du PDF (Internet Archive) — pas une vérité humaine"
  pages [{"page": 30, "mots_reference": 482, "mots_ocr": 476, "wer": 0.0768, "wer_brut": 0.0768, "rappel": 0.9253, "precision": 0.937, "confiance": 89.9, "trace": ["recadrage"], "wer_colonnes": 0.9212, "wer_colonnes_inverse": 0.9274, "mots_reference_colonnes": 482}, {"page": 50, "mots_reference": 383, "mots_ocr": 381, "wer": 0.0731, "wer_brut": 0.0731, "rappel": 0.9269, "precision": 0.9318, "confiance": 9
  agregat {"pages": 10, "mots_reference": 4494, "wer": 0.071, "wer_brut": 0.0705, "rappel": 0.9372, "confiance": 91.1, "wer_colonnes": 0.8996, "wer_colonnes_inverse": 0.9101}
  dispositif "tools/mesurer_reel.py (couche OCR du PDF comme référence ; ordre des colonnes depuis les coordonnées DjVu)"
== reports/r44-reel-second.json ['date', 'ligne', 'nature', 'reference', 'djvu', 'source', 'note_colonnes', 'agregat', 'pages', 'dispositif']
  reference "couche OCR du PDF (Internet Archive) — pas une vérité humaine"
  pages [{"page": 40, "mots_reference": 303, "mots_ocr": 295, "we
… [1279 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/r44*; echo '---'; python3 - <<'PY'\nimport json\nfor f in ('reports/r44-reel-troisieme.json','reports/r44-reel-3.json'):\n    try:\n        d=json.load(open(f)); print(f, d.get('reference'), d.get('agregat'))\n    except E … [69 caractères tronqués]`

  ```
reports/r44-colonnes.json
reports/r44-cout.json
reports/r44-ocr-pilote.json
reports/r44-petit.json
reports/r44-reel.json
reports/r44-reel-second.json
reports/r44-reel-third.json
reports/r44-rotation.json
reports/r44-sans-exposants.json
reports/r44-scans.json
reports/r44-seed2.json
reports/r44-seed3.json
reports/r44-tableaux.json
---
reports/r44-reel-troisieme.json [Errno 2] No such file or directory: 'reports/r44-reel-troisieme.json'
reports/r44-reel-3.json [Errno 2] No such file or directory: 'reports/r44-reel-3.json'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/r44-reel-third.json'))\nprint('reference:',d.get('reference'))\nprint('agregat:',json.dumps(d.get('agregat'),ensure_ascii=False)[:500])\nprint('pages:',len(d.get('pages',[])))\ … [145 caractères tronqués]`

  ```
reference: couche OCR du PDF (Internet Archive) — pas une vérité humaine
agregat: {"pages": 10, "mots_reference": 3071, "wer": 0.0873, "wer_brut": 0.0938, "rappel": 0.9189, "confiance": 90.9, "wer_colonnes": 0.9095, "wer_colonnes_inverse": 0.9163}
pages: 10
---
  ✅ tesseract 5.5.3 · langues : eng fra osd spa
  ```

- **job_output** `{"job_id": "bash-4154", "timeout_ms": 120000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in rapport-r13-decision rapport-r13.2-vocab1024 rapport-r06-relecture rapport-r06-cascade-confiance; do echo \"##### $f\"; sed -n '1,12p' reports/$f.md; echo; done", "description": "Lire R1.3 et relecture"}`

  ```
##### rapport-r13-decision
# R13 — la décision : rester en octets, parce que le BPE ne gagne pas à octets égaux

> **Ligne de roadmap** : R13 / R1.3 · **Date** : 2026-10-30 · **Verdict** : ✅ **décision
> mesurée — le natif reste en octets** (`vocab = 256`). À budget d'**octets** égal, le BPE perd
> partout : **+0,39 %** (512, deux graines), **+3,92 à +4,09 %** (1024 selon la graine), **+4,22 % / +6,59 %** (anglais).
> Le « gain de 11 % » du pilote était un **artefact de budget** : à pas égaux, le BPE voit deux
> fois plus d'octets.
>
> **Dispositif** : synthèse de six fiches et de six JSON — français (4,4 Mo) et anglais
> (100 Mo), vocabulaires 512 et 1024, deux graines ; comparaison en **bits/octet** à octets vus
> égaux, train/val séparés ; `tools/tokenizer_bpe.py`, `tools/entrainer_native_tokens.py`,
> `tools/r13_anglais.py` ; données [`r13-tokenisation.json`](r13-tokenisation.json),

##### rapport-r13.2-vocab1024
# R13.2 — vocab 1024 : le BPE perd encore plus à octets égaux

> **Ligne de roadmap** : R13.2 · **Date** : 2026-10-29 · **Verdict** : ⛔ **négatif** — à budget
> d’octets égal, BPE 1024 fait **1,8726** bits/octet contre **1,8021** pour bytes : il **perd
> 3,9 %**. Le vo
… [1870 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -nE '249|248' reports/rapport-r03-banc-complet.md reports/rapport-r02-controleur.md reports/rapport-r06-pipeline.md | head -20; echo '---'; grep -nE '0,894|0.894|oracle' reports/rapport-r06-relecture.md reports/rapport-r06-casca … [76 caractères tronqués]`

  ```
reports/rapport-r03-banc-complet.md:1:# R0.3 — le banc complet : 249 questions, 30 documents, et le modèle sur GPU
reports/rapport-r03-banc-complet.md:9:> **Dispositif** : 30 documents, 5 types, **249 questions** générées à valeur numérique ;
reports/rapport-r03-banc-complet.md:24:juridique (résolutions ONU), code (documents à blocs de code). **249 questions** construites par
reports/rapport-r03-banc-complet.md:36:## Ce qui est mesuré — le lecteur extractif (249 questions, 3 s)
reports/rapport-r03-banc-complet.md:52:## Ce qui est mesuré — le modèle sur GPU (249 questions, ~13 min)
reports/rapport-r03-banc-complet.md:102:   des cas sur 249 questions et 5 types. R0.2 n'a plus besoin d'être amélioré pour cela.
reports/rapport-r03-banc-complet.md:111:- `tools/banc_complet.py` — le corpus de 30 documents et le générateur de questions (249).
reports/rapport-r06-pipeline.md:68:| lexical (249, questions à valeur) | **0,944** | 0,835 | **+0,109** |
---
reports/rapport-r06-cascade-confiance.md:1:# R06 v4 — la cascade à confiance calibrée égale l'oracle, hors échantillon
reports/rapport-r06-cascade-confiance.md:5:> atteint **0,911** sur le lexical (fixe 0,870, oracle 0,911) et **0,415** sur l
… [727 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-4154 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-ocr.sh >/tmp/porte-ocr.log 2>&1; echo exit=$?; tail -5 /tmp/porte-ocr.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-4154"}`

  ```
exit=0
  ✅ exactitude natif ≥ 90%
  ✅ sans OCR : aucune réponse
  ✅ le WER MONTE sur la page dégradée
  ✅ la parité de région BAISSE sur la page dégradée
✅ porte OCR verte : 10 pages lues, WER sous le seuil, parité tenue et contrôles en échec
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '0,894\\|0.894' reports/*.md | head -10; echo '---'; grep -E '✅|❌|WER|parité|page noire' /tmp/porte-ocr.log | tail -15", "description": "Trouver 0.894 et bilan porte OCR"}`

  ```
reports/rapport-audit-r1r3.md:281:| **fr** | 151 | 135 → **129** (−6) | 135 → **129** (−6) | 0,8940 → **0,8543** |
reports/rapport-audit-r1r3.md:393:7. **Majeure — le français recule** : 135 → 129 exacts (couverture 0,894 → 0,854), masqué par
reports/rapport-audit-v10.md:103:   le **test v10 est 68/68** (couverture 0,8947), le **dev reste 152/152** (0,9325). Le
reports/rapport-audit-v10.md:267:| **test** | 190 | 76 | 64/64 | 67/67 | **68/68** | **0,8947** | **0,5890** | **0,7337** |
reports/rapport-coherence-fiches-v8.md:117:0,9432**. Pour la v7 : fr **135/151 = 0,8940**, en **61/88 = 0,6932** — la couverture anglaise
reports/rapport-dev-test-v10.md:7:> **0,9325 / 0,8947 / 0,9205** ; F1 **0,5812 / 0,5890 / 0,5836** (vivant 612) ;
reports/rapport-dev-test-v10.md:65:| **test** | 190 | 994 | 76 | 68 | 68/76 = **0,8947** | **68/68 = 1,0** | 0,5890 | 0,7337 | 0,7656 |
reports/rapport-dev-test-v10.md:87:| **REL** | 57 | 51 | 0,8947 | 51/51 | 0,7907 | 0,9573 | 17 | 14 | **0,8235** | 14/14 | 0,7179 | 0,9444 |
reports/rapport-dev-test-v10.md:239:| canonique | `%3==0` | 422 | 163 | 152 | 152 | 0,9325 | 0,5812 | 0,7330 | 0,7547 | 190 | 76 | 68 | 68 | 0,8947 | 0,5890 | 0,7337 | 0,7656 |
report
… [717 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '36,75p' reports/rapport-r03-banc-complet.md; echo '---'; sed -n '1,20p' reports/rapport-memoire-travail-n5.md; echo '---'; git log -1 --format='%h %ci %s'; git status --short | grep -v '^ M journal\\|^M  journal\\|^D  journal … [101 caractères tronqués]`

  ```
## Ce qui est mesuré — le lecteur extractif (249 questions, 3 s)

| type | récup. 10 % | récup. 30 % | récup. 50 % | valeur 30 % | valeur 100 % | aléatoire 30 % |
|---|---:|---:|---:|---:|---:|---:|
| code | 0,89 | **1,00** | 1,00 | 0,72 | 0,72 | 0,39 |
| juridique | 0,87 | **1,00** | 1,00 | 1,00 | 1,00 | 0,20 |
| prose | 1,00 | **1,00** | 1,00 | 0,76 | 0,76 | 0,33 |
| tableau | 0,98 | **1,00** | 1,00 | 0,93 | 0,93 | 0,29 |
| technique | 1,00 | **1,00** | 1,00 | 0,90 | 0,90 | 0,30 |

À **30 %** du budget, le passage gold est lu dans **100 %** des cas sur les cinq types — la
courbe est plate entre 30 et 50 %, et commence à mordre à 10 % (0,87–1,00). Le **hasard** reste
à 0,20–0,39. Le taux de réponse est **exactement** celui de la lecture intégrale : c'est
structurel (le lecteur est le même, ancré sur l'index du document entier), et c'est le contrôle
qui dit que la sélection ne coûte rien.

## Ce qui est mesuré — le modèle sur GPU (249 questions, ~13 min)

| type | contrôleur 30 % | début 30 % | closed-book |
|---|---:|---:|---:|
| code | **0,204** | 0,056 | 0,000 |
| juridique | **0,167** | 0,100 | 0,000 |
| prose | **0,265** | 0,000 | 0,000 |
| tableau | **0,220** | 0,017 | 0,000 
… [3487 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee-gold-porte.json'))\nh=d['heuristique']['all']\nprint('heur POS',h['pos']['exactitude'],h['pos']['exactitude_ferme'],h['pos']['exactitude_ouvert'],h['pos']['tokens'])\nprint … [203 caractères tronqués]`

  ```
heur POS 0.85 0.9295 0.7746 3179
heur synt 0.6482 0.7673
heur pragma {'acte': 0.9967, 'negation': 0.9771, 'modalite': 0.9886, 'double_sens': 0.9444}
att tete {'cibles': 236, 'labels': 236, 'top1': 235, 'topk': 234, 'top1_taux': 0.9958, 'topk_taux': 0.9915, 'couverture': 1.0}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'DEEPSEEK\\|deepseek\\|enseignant' tools/tests/linguistique/*.py tools/bloc_linguistique.py | head -20; echo '---'; ls -l ~/.config/drave/deepseek.key 2>&1", "description": "Vérifier la voie API DeepSeek du tagger"}`

  ```
tools/tests/linguistique/qualifier_quatre_modes.py:16:    DEEPSEEK_KEY_FILE=~/.config/drave/deepseek.key \
tools/tests/linguistique/qualifier_quatre_modes.py:34:from tools.llm.deepseek import DeepSeek
tools/tests/linguistique/qualifier_quatre_modes.py:52:        raise SystemExit("clé DeepSeek absente : exporter DEEPSEEK_KEY_FILE")
tools/tests/linguistique/qualifier_quatre_modes.py:64:    pos = NeuronalLLMPOS("deepseek-chat", transport=transport)
tools/tests/linguistique/qualifier_quatre_modes.py:65:    chunks = NeuronalLLMChunks("deepseek-chat", transport=transport)
tools/tests/linguistique/qualifier_quatre_modes.py:66:    pragma = NeuronalLLMPragmatique("deepseek-chat", transport=transport)
tools/tests/linguistique/qualifier_quatre_modes.py:109:                 "modalite": "api-deepseek (deepseek-chat), aucun serveur local"},
tools/bloc_linguistique.py:2324:    return PRIORITE_NIVEAU if os.environ.get("DEEPSEEK_KEY_FILE") else None
---
-rw-------. 1 stephane stephane 36  3 nov 11:15 /home/stephane/.config/drave/deepseek.key
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'NeuronalLLMPOS\\|tagger' docs/implantation/bloc-linguistique.md docs/produit/*.md 2>/dev/null | head -15; echo '---'; grep -n 'R0.7\\|tagger\\|0,944\\|0.944' docs/pilotage/roadmap.md | head -10", "description": "Vérifier la … [16 caractères tronqués]`

  ```
docs/implantation/bloc-linguistique.md:138:- **`NeuronalLLMPOS`** : le **tagger réel qualifié**. Il tokenise avec `Heuristique._mots` (mots
docs/implantation/bloc-linguistique.md:144:- **`NeuronalLLMChunks`** : le **tagger de syntagmes**. Il demande une étiquette **BIO** par token
docs/implantation/bloc-linguistique.md:150:  Il appelle les deux taggers (chacun avec son cache), réunit leurs étiquettes et laisse la
docs/implantation/bloc-linguistique.md:153:- **`NeuronalLLMPragmatique`** : le **tagger de pragmatique**. Un prompt d'analyse, une grammaire
docs/implantation/bloc-linguistique.md:163:sans régression sur les réelles). Le **tagger de syntagmes** est qualifié sur le même gold :
docs/implantation/bloc-linguistique.md:166:tagger de syntagmes ne rend que ce niveau. La **cascade complète** (composite + politique
docs/implantation/bloc-linguistique.md:189:et `bloc` peut être `Heuristique`, `MockNeuronal`, `NeuronalLLM`, `NeuronalLLMPOS`,
docs/implantation/bloc-linguistique.md:204:  nécessaire quand le tagger réel est meilleur (mesure : 0,6168 / 0,7592 contre 0,2137 / 0,5670
docs/implantation/bloc-linguistique.md:318:2. **Un modèle neuronal qualifié** (tagger ou LLM) sur ce gold ;
… [8548 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/tests/linguistique/qualifier_quatre_modes.py; echo '---'; sed -n '80,140p' tools/tests/linguistique/qualifier_quatre_modes.py", "description": "Lire le banc API des quatre modes"}`

  ```
#!/usr/bin/env python3
"""qualifier_quatre_modes.py — la porte des quatre modes du contrat de L sur le gold 432.

Les quatre modes du contrat (`docs/theorie/contrat-bloc-langue.md`) mesurés sur le
**même** gold réel 432 :

  1. heuristique seule ;
  2. neuronal seul (le composite POS + syntagmes, via l'API DeepSeek — règle 11) ;
  3. parallèle (`Parallele`) ;
  4. cascade (`Cascade`, seuil 0,6).

Mêmes mesures que la cascade : POS, syntagmes F1, tête F1, acte, fraction, refus.
Le coût est mesuré : appels du tagger, tokens API, latence, durée.

Usage :
    DEEPSEEK_KEY_FILE=~/.config/drave/deepseek.key \
    python3 tools/tests/linguistique/qualifier_quatre_modes.py --limite 3
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE))

from tools.bloc_linguistique import (PRIORITE_NIVEAU, PRIORITE_TYPE, Cascade, Heuristique,
                                     NeuronalLLMChunks, NeuronalLLMCompose,
                                     NeuronalLLMPOS, NeuronalLLMPragmatique, Parallele)
from tools.llm.deepseek import DeepSeek
from tool
… [5341 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '120,180p' docs/implantation/bloc-linguistique.md", "description": "Lire la doc du tagger et de l'API"}`

  ```
modalité ;
- **discours** : les paragraphes, les connecteurs (contraste, cause, conséquence, but) et une
  relation candidate ;
- **pragmatique** : l'acte de parole (question, exclamation, ordre, assertion) à basse
  confiance, le double sens possible (`ou`, guillemets, question), le contexte fourni ;
- **document** : les paragraphes, les titres Markdown/numérotés, la provenance.

### 5.2 La version neuronale

Six objets, un même contrat :

- **`MockNeuronal`** : le **double de contrat**. Il est déterministe, sans GPU, et rend les
  niveaux profonds (morphème, POS ouverte, syntagme, pragmatique) avec `source = neuronal`. Il
  ne prétend pas être un modèle : il prouve que le contrat accepte une autre implémentation,
  que le parallèle fusionne et que la cascade n'appelle le neuronal que sur le résidu.
- **`NeuronalLLM`** : l'**adaptateur réel**. Il construit un prompt JSON, appelle un modèle local
  (`llama-cli`), parse la réponse et la convertit en `Annotation` ; si le modèle est absent, ne
  répond pas ou rend un JSON invalide, il lève `RefusNeuronal` — il ne simule pas.
- **`NeuronalLLMPOS`** : le **tagger réel qualifié**. Il tokenise avec `Heuristique._mots` (mots
  et nombres),
… [3283 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' reports/rapport-pensee-quatre-modes-run2.md; echo '---'; sed -n '1,60p' reports/rapport-pensee-quatre-modes.md 2>/dev/null", "description": "Lire les quatre modes API"}`

  ```
# B13 — la confirmation (run 2) : refus 0, le niveau gagne encore

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **145/145 portes** : la passe API est **rejouée** sur le gold 432 après le
> correctif d'élision. **Aucun refus** (`aucun_refus: True`), le `r353` passe, et le **niveau
> gagne encore** : POS **0,9389** (+0,008), syntagmes **0,8241**, tête **0,8797**, acte 0,9954.
> Le réel confirme le réel.
>
> **Dispositif** : [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432-run2.json`](pensee-quatre-modes-432-run2.json),
> [`autotest.py`](../tools/pensee/autotest.py).

## 1. Run 1 contre run 2

| mode | POS (run 1) | **POS (run 2)** | syntagmes | tête | acte |
|---|---:|---:|---:|---:|---:|
| heuristique | 0,7394 | **0,7444** | 0,2520 | 0,4511 | 0,9954 |
| neuronal | 0,9309 | **0,9389** | 0,8241 | 0,8797 | 0,0000 |
| parallèle | 0,9280 | 0,9326 | 0,8029 | 0,8571 | 0,9954 |
| cascade | 0,9280 | 0,9326 | 0,8029 | 0,8571 | 0,9954 |
| **parallele_niveau** | 0,9309 | **0,9389** | **0,8241** | **0,8797** | 0,9954 |
| **cascade_niveau** | 0,9309 | **0,9389** | **
… [5140 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i 'quatre-modes'; echo '---'; python3 - <<'PY'\nimport json\nfor f in ('reports/pensee-quatre-modes.json','reports/pensee-quatre-modes-run2.json'):\n    try:\n        d=json.load(open(f)); print('==',f, list(d)[:1 … [414 caractères tronqués]`

  ```
pensee-quatre-modes-432.json
pensee-quatre-modes-432-pragma.json
pensee-quatre-modes-432-run2.json
pensee-quatre-modes-432-run3.json
pensee-quatre-modes-432-soustype.json
pensee-quatre-modes-432-soustype-t03b.json
pensee-quatre-modes-432-soustype-t03c.json
pensee-quatre-modes-432-soustype-t03.json
pensee-quatre-modes-432-t03.json
pensee-quatre-modes.json
pensee-quatre-modes-niveau.json
pensee-quatre-modes-run2.json
rapport-pensee-quatre-modes-432.md
rapport-pensee-quatre-modes.md
rapport-pensee-quatre-modes-run2.md
---
== reports/pensee-quatre-modes.json ['date', 'gold', 'modes', 'seuils', 'refus', 'refus_detail', 'appels', 'api', 'latence_s', 'duree_totale_s']
gold {'phrases': 3, 'tokens': 14, 'modalite': 'api-deepseek (deepseek-chat), aucun serveur local'}
  heuristique POS 0.8571 synt 0.7368 tete 0.8235 acte 1.0
  neuronal POS 1.0 synt 1.0 tete 1.0 acte 0.0
  parallele POS 1.0 synt 1.0 tete 1.0 acte 1.0
  cascade POS 1.0 synt 1.0 tete 1.0 acte 1.0
  parallele_niveau POS 1.0 synt 1.0 tete 1.0 acte 1.0
  cascade_niveau POS 1.0 synt 1.0 tete 1.0 acte 1.0
== reports/pensee-quatre-modes-run2.json ['date', 'ligne', 'portes', 'run1', 'run2', 'refus', 'seuils', 'api', 'limites']
gold No
… [2 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,55p' reports/rapport-pensee-quatre-modes-432.md; echo '---'; python3 - <<'PY'\nimport json,glob\nfor f in sorted(glob.glob('reports/pensee-quatre-modes-432*.json')):\n    d=json.load(open(f))\n    print('==',f, 'date',d.get … [558 caractères tronqués]`

  ```
# B13 — les quatre modes sur le gold 432 : le niveau gagne avec le réel

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6 et règle 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **143/143 portes** : les **six modes** du contrat de L sont mesurés sur le
> **gold réel 432**, avec le **neuronal réel** (l'API DeepSeek, `deepseek-chat`, température 0).
> Le **niveau** (`PRIORITE_NIVEAU`) gagne : POS **0,9309**, syntagmes **0,8226**, tête **0,8784**,
> et garde la pragmatique de l'heuristique (**0,9954**). Le **mock** avait conclu l'inverse :
> le défaut par défaut reste la confiance **faute de clé dans les portes**, pas par choix.
>
> **Dispositif** : [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432.json`](pensee-quatre-modes-432.json),
> [`autotest.py`](../tools/pensee/autotest.py).

## 1. Les six modes (432 phrases, API réelle)

| mode | POS | syntagmes F1 | tête F1 | acte |
|---|---:|---:|---:|---:|
| heuristique | 0,7394 | 0,2520 | 0,4511 | **0,9954** |
| neuronal (compose) | **0,9309** | **0,8226** | **0,8784** | 0,0000 |
| parallèle (confiance) | 0,9280 | 0,8020 | 0,8570 | 0,9954 |
| cascade (confiance) |
… [4570 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'def charger\\|def _sources\\|gold_reel\\|REEL\\|phrases' tools/tests/linguistique/qualifier_cascade.py | head -20; echo '---'; sed -n '1,60p' tools/tests/linguistique/qualifier_cascade.py", "description": "Comprendre le corp … [16 caractères tronqués]`

  ```
38:GOLD_REEL = pathlib.Path(__file__).with_name("gold_reel.json")
41:def charger(reel: bool = False) -> list[dict]:
43:        ph = json.loads(GOLD_REEL.read_text(encoding="utf-8"))["phrases"]
47:    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
48:    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
56:def _lecture(nom: str, bloc, phrases: list[dict]) -> dict:
57:    r = evaluer_bloc(nom, bloc, phrases)
62:def _sources(bloc, phrases: list[dict]) -> dict:
63:    hand = [p for p in phrases if p["source"] == "hand"]
64:    synth = [p for p in phrases if p["source"] == "synth"]
66:            for nom, ps in (("all", phrases), ("hand", hand), ("synth", synth))}
78:                    help="charger gold_reel.json (432 phrases réelles)")
82:    phrases = charger(args.gold_reel)
84:        phrases = phrases[:args.limite]
102:        mesures = {"neuronal": _sources(compose, phrases)}
103:        mesures["heuristique"] = _sources(h, phrases)
104:        mesures["cascade_pos"] = _sources(bl.Cascade(h, pos), phrases)
106:            bl.Cascade(h, chunks, priorite_syntagme="confiance"), phrases)
108:            bl.Cascade(h, compose, priorite_syntagme="confianc
… [2403 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -8 -- tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold.json tools/tests/linguistique/gold_synthetique.json; echo '---'; git log -1 --format='%h %ci' -- tools/tests/linguistique/gold_reel.json; e … [383 caractères tronqués]`

  ```
c5b80dd8 B13 — LE GOLD CORRIGÉ (4 GP SANS PRÉPOSITION) : EXACT 226/226 (1,0000), COUVERTURE 0,9289 → 0,9456, 17 → 13 SPANS ; 183/183
702b368c B13 — LES VRAIS ABSENTS : 5 PHRASES, 0 LIEN, GOLD 432 ; 140/140
651c1fc0 B13 — LE LIEN AUTOMATIQUE RÉPARÉ : 5/5 APRÈS RÉORDONNANCEMENT ET REPLI PRON/NOUN ; 136/136
297c4f17 B13 — LA RÉPONSE CONTEXTUELLE : 5/5, LA PHRASE PRÉCÉDENTE TRANCHE ; 134/134
26e4df27 B13 — LES QUESTIONS PIÈGES : 29/34, LE SI EST UNE CONVENTION ; 132/132
866fcaa7 B13 — LES QUESTIONS NÉGATIVES : 19/29, LA RÈGLE DE SURFACE NE S'INVERSE PAS ; 130/130
56b22212 B13 — LES 19 RÉPONSES DE RÉFÉRENCE : COUVERTURE 19/19, LE JUGE EST UTILISABLE ; 127/127
41c7d1f1 B13 — LA CORÉFÉRENCE À 103 LIENS : 86/103, CIBLE 100 ATTEINTE, GOLD 407 ; 112/112
---
702b368c 2026-11-02 15:57:58 -0500
---
gold_reel.json 1 reel 200 phrases réelles. 432
  keys ['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source'] mots 5
gold.json 1 None Gold v0, écrit à la main ; spans calculés par sous-chaîne. 20
  keys ['id', 'langue', 'texte', 'mots', 'segments', 'pragma'] mots 3
gold_synthetique.json 1 synthetique 160 phrases d'une grammaire indépendante ; lexique disjoint de l'heuristique. 160
  keys ['
… [70 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, pathlib\nsys.path.insert(0,str(pathlib.Path('.').resolve()))\nsys.path.insert(0,str(pathlib.Path('.').resolve()/'tools'))\nsys.path.insert(0,str(pathlib.Path('.').resolve()/'tools/tests/linguistique'))\n … [534 caractères tronqués]`

  ```
phrases 432 tokens 2375 sources {'reel'}
heur POS 0.8754 ferme 0.9277 ouvert 0.8204 tokens 2375
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/aiguille.py --help 2>&1 | head -30; echo '---'; grep -n 'aiguille\\|4 000\\|4000\\|15/18' reports/rapport-n2-r11.md reports/rapport-n2-fenetre-r1.md | head -20", "description": "Vérifier le banc aiguille R1.1"}`

  ```
usage: aiguille.py [-h] [--n N] [--threads THREADS] [--lot LOT]
                   [--timeout TIMEOUT] [--gpu] [--gpu-kv]
                   [--attn-topk ATTN_TOPK] [--gpu-topk] [--journal JOURNAL]
                   modele longueurs profondeurs

positional arguments:
  modele
  longueurs
  profondeurs

options:
  -h, --help            show this help message and exit
  --n N                 jetons générés (réponse)
  --threads THREADS
  --lot LOT             lot de préremplissage
  --timeout TIMEOUT
  --gpu                 DRAVE_GPU=1 (déport des projections)
  --gpu-kv              DRAVE_GPU=1 DRAVE_GPU_KV=1 (KV en VRAM)
  --attn-topk ATTN_TOPK
                        --attn-topk N (0 = attention complète)
  --gpu-topk            DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1
  --journal JOURNAL
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' tools/aiguille.py; echo '---'; grep -n 'def main\\|add_argument' tools/aiguille.py | head -20", "description": "Lire le banc aiguille"}`

  ```
#!/usr/bin/env python3
"""Aiguille dans la botte de foin — version 2, celle qui mesure vraiment.

La perplexité ne dit pas si un modèle RETROUVE une information. Ce script plante
un code à une profondeur donnée dans un contexte long, puis le redemande.

Ce qui a changé par rapport à la v1 (mesurée et arrêtée) :

1. **le remplissage est du vrai texte VARIÉ** (`data/wikitext2_test.txt`), et non
   la même phrase recopiée jusqu'à la longueur voulue. Un remplissage répété ne
   teste rien : le modèle pouvait répondre en devinant la structure. Chaque sonde
   prend en plus une FENÊTRE DIFFÉRENTE du corpus, pour que les sondes ne
   partagent pas leur remplissage ;
2. **la réponse est longue** (`--n 40` par défaut) : un code peut sortir au
   deuxième ou troisième jeton, et s'arrêter à 8 jetons faisait échouer des
   sondes que le modèle savait résoudre ;
3. **le préremplissage par lots** (`--lot`) rend chaque sonde abordable : le
   moteur ne l'utilisait que pour la perplexité ;
   ⚠️ et depuis le sprint 4, le décalage de fenêtre est RÉELLEMENT appliqué (il
   comparait à une marge de 400 000 caractères pour un corpus qui en fait 353 778,
   donc il remettait l'offset à zéro à chaque so
… [2352 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'aiguille' reports/rapport-n2-*.md reports/rapport-r1-*.md | head -20; echo '---'; grep -rn 'aiguille\\|15/18\\|4 000' docs/pilotage/backlog/R11-contexte-hierarchique.md | head -20", "description": "Tracer l'aiguille native" … [1 caractères tronqués]`

  ```
reports/rapport-n2-r12-2048.md:122:limite dure de R1 — et la raison pour laquelle la porte « aiguille native ≥ 15/18 à 4 000 octets »
---
6:> **Glossaire** : [perplexité](../../theorie/glossaire/entrees/perplexite.md) · [test de l'aiguille](../../theorie/glossaire/entrees/test-de-l-aiguille.md) · [graphe de document](../../theorie/glossaire/entrees/graphe-de-document.md).
12:**Ordre arrêté le 2026-10-29** : c'est **N2** qui porte la hiérarchie (l'état de section, 3 graines) ; R11 mesure la fenêtre qui en résulte et n'ouvre donc qu'après N2. La mesure reste ici : PPL à 1 000 octets, aiguille native, stabilité.
26:- aiguille native à 4 000 octets
32:2. aiguille native ≥ 15/18 à 4 000 octets
50:3. mesurer PPL, aiguille, stabilité ; écrire la fiche
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'copie\\|miroir\\|0,0078\\|0.0078' reports/rapport-n2-r12-2048.md reports/rapport-n2-r11.md | head -20", "description": "Tracer le miroir de copie"}`

  ```
reports/rapport-n2-r12-2048.md:35:4 000 octets. Contrôles : même texte (contexte 256 → 2 000), permutation, miroir de copie.
reports/rapport-n2-r12-2048.md:117:## 4. Le miroir de copie reste muet
reports/rapport-n2-r12-2048.md:119:Sur tous les modèles de la nuit, la justesse de copie à distance est **0,0078** au mieux (le
reports/rapport-n2-r12-2048.md:121:ne crée pas de circuit de copie** : la PPL baisse, la restitution ne vient pas avec. C'est la
reports/rapport-n2-r11.md:41:  (`eval_fenetre.py`), et le **miroir de copie** à distance (`miroir_copie.py`).
reports/rapport-n2-r11.md:165:## 6. Le miroir de sortie est muet — et c'est un résultat
reports/rapport-n2-r11.md:167:`miroir_copie.py` plante un code de 16 octets deux fois dans du texte réel (8 sondes, remplissages
reports/rapport-n2-r11.md:168:différents) et demande au modèle de **prédire** la seconde occurrence : justesse top-1 **0,0078**
reports/rapport-n2-r11.md:171:copie** à 34,3 M / 20 000 pas. Conséquence à ne pas dépasser : **la PPL n'est pas la lecture** ;
reports/rapport-n2-r11.md:173:ne crée pas la copie.
reports/rapport-n2-r11.md:212:  `work/n2ac/miroir_copie.py`, `work/n2ac/agrege_r11.py`.
reports/rapport-n2-r11.md
… [23 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work/n2ac/ | grep -i 'miroir\\|mirroir'; echo '---'; python3 - <<'PY'\nimport json,glob\nfor f in sorted(glob.glob('work/n2ac/miroir*.json'))+sorted(glob.glob('work/n2ac/mirroir*.json')):\n    d=json.load(open(f)); print(f, d.get( … [84 caractères tronqués]`

  ```
miroir-kd-mix512-15k.json
miroir-mix1024-60k.json
miroir-mix512-15k.json
miroir-rope1024-2.5k.json
miroir-rope512.json
miroir-rope.json
mirroir_copie.py
---
work/n2ac/miroir-kd-mix512-15k.json kd-mix512-15k.pt {'16': 0.0, '64': 0.0, '128': 0.0, '200': 0.0, '240': 0.0, '255': 0.0078, '300': 0.0, '400': 0.0}
work/n2ac/miroir-mix1024-60k.json mix1024-60k.pt {'16': 0.0, '64': 0.0, '128': 0.0, '200': 0.0, '240': 0.0, '255': 0.0078, '300': 0.0, '400': 0.0}
work/n2ac/miroir-mix512-15k.json mix512-15k.pt {'16': 0.0078, '64': 0.0078, '128': 0.0, '200': 0.0, '240': 0.0, '255': 0.0078, '300': 0.0, '400': 0.0}
work/n2ac/miroir-rope.json rope-20k.pt {'16': 0.0078, '64': 0.0, '128': 0.0, '200': 0.0, '240': 0.0, '255': 0.0, '300': 0.0, '400': 0.0}
work/n2ac/miroir-rope1024-2.5k.json rope1024-2.5k.pt {'16': 0.0078, '64': 0.0, '128': 0.0, '200': 0.0, '240': 0.0, '255': 0.0, '300': 0.0156, '400': 0.0}
work/n2ac/miroir-rope512.json rope512-5k.pt {'16': 0.0, '64': 0.0, '128': 0.0, '200': 0.0, '240': 0.0, '255': 0.0, '300': 0.0078, '400': 0.0}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short -- reports/ tools/ data/ docs/ | head -30; echo '---'; git check-ignore -v work/r44/mesure.json work/n2ac/rope1024-20k.pt 2>&1 | head -5; echo '---'; git diff --stat -- tools/bloc_linguistique.py tools/tests/lingui … [84 caractères tronqués]`

  ```
M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
M  reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/porte-produit.sh
 m tools/structures
 M tools/verifier_schema_produit.py
?? reports/rapport-etat-a.md
?? reports/rapport-etat-n2.md
?? reports/rapport-s-paragraphes.md
---
.gitignore:23:work/	work/r44/mesure.json
.gitignore:23:work/	work/n2ac/rope1024-20k.pt
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,35p' reports/rapport-etat-a.md; echo '===='; sed -n '1,25p' reports/rapport-etat-n2.md", "description": "Regarder les fiches sœurs A/N2"}`

  ```
# État du chantier A — le moteur : deux bloqués réels, un faux bloqué, une frontière à requalifier

> **Ligne de roadmap** : **A** (le moteur) · **Date** : 2026-11-06, 21 h 51 HNE · **Branche** : `s/v7` ·
> **HEAD** : `7a876f70` (le HEAD a bougé pendant l'audit : `d31aa9a2` → `7a876f70`) ·
> **Mission** : lecture seule, aucun code, aucun fichier existant modifié ; deux fichiers neufs.
>
> **Verdict** : ⚠️ **l'état A est sain, le récit A est en retard.** Les lignes fermées le sont
> réellement ; **A8.3a est fait pour 3 portes sur 19** (et non « fait » tout court) ; **A2.6 est
> partiel mais libre** — sa tête est **décidée** (refusée), ses experts ne sont **pas** bloqués par
> l'absence d'un MoE : un **Qwen3-30B-A3B Q4 de 18 Go est présent et tourne**. Les **deux seuls
> bloqués réels** de A sont **A3.4** (compte Colab) et **A5.4** (carte Stratix V). **A6.2 est
> mal classé** : il est libre, pas bloqué. **A23 a raison sur l'effet** (A2.6 ne doit pas être la
> tête de frontière) **mais tort sur la cause** (les experts ne sont pas bloqués par A6.2).
>
> **Dispositif** : lecture de `docs/pilotage/roadmap.md`, `en-cours.md`, `backlog/index.md`,
> `backlog/dependances.md`, des fiches `bac
… [3472 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l reports/rapport-etat-a.md reports/rapport-etat-n2.md reports/rapport-etat-r.md reports/pensee-etat-r.json 2>&1", "description": "Vérifier si les fichiers R existent déjà"}`

  ```
ls: cannot access 'reports/rapport-etat-r.md': No such file or directory
ls: cannot access 'reports/pensee-etat-r.json': No such file or directory
-rw-------. 1 stephane stephane 20802  6 nov 22:01 reports/rapport-etat-a.md
-rw-------. 1 stephane stephane 19438  6 nov 21:59 reports/rapport-etat-n2.md
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format='%h %ci %s'; echo '---'; git status --short -- docs/pilotage/ docs/pilotage/roadmap.md docs/pilotage/en-cours.md | head; echo '---'; grep -n 'R — le lecteur\\|R1.2\\|R0.7\\|R4.4' docs/pilotage/en-cours.md | head - … [47 caractères tronqués]`

  ```
97256b8f 2026-11-06 21:57:10 -0500 PLAN — § 14 : LA NUIT DES P0 (VAGUES, RÉSULTATS, RESTE)
---
---
123:| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **1 024 octets entraînés** ; **2 048** fini (2×10 000 pas) ; la restitution |
131:**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+ ; **S** — poursuivre la validation ; **N4** — consigne ; **B10.3** — `z` ; **B13** — 178/178 ; **R0.7** — tagger ; **D** — **restauré** : le corpus à **62 documents** (Choquette + Assurance ; DOC1/DOC2, quasi-doublons, écartés) est en place (`data/corpus_ocr_cegep` : train 4 440 987, val 12 536, test 10 524 ; 8 Ko 0, 500 o 0) ; [fiche](../../reports/rapport-ocr-cegep-64.md) ; **la passe complète est finie** (`work/portes/passe-2404-23h45` ; **79 vertes, 4 rouges** : `indice`, `melange` tolérées ; `lecteur` corrigée ; `sessions` → heartbeat de `e181ce02` à rafraîchir).
135:- **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline de7c9113..HEAD 2>/dev/null | head -10; echo '---'; git diff --stat de7c9113..HEAD -- docs/pilotage 2>/dev/null | head", "description": "Voir les commits depuis ma mesure"}`

  ```
97256b8f PLAN — § 14 : LA NUIT DES P0 (VAGUES, RÉSULTATS, RESTE)
5940ea53 B13 — LE GV S'ARRÊTE AU MARQUEUR ÉLIDÉ (qu'il) ; AUCUN EFFET MESURÉ, 183/183
7a876f70 PRODUIT — RE-TEST DES 50 TEXTES : filtrer = 0 CHEVAUCHEMENT (297 SEGMENTS), LES 5 SANS SYNTAGME SONT NON LINGUISTIQUES
---
 docs/pilotage/en-cours.md     |  4 ++--
 docs/pilotage/plan-travail.md | 16 ++++++++++++++++
 2 files changed, 18 insertions(+), 2 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold-etat-r-head.json 2>&1 | tail -1; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee-gold-etat-r-head.json'))\np=d['heuristique']['all']['pos']\nprint( … [266 caractères tronqués]`

  ```
heuristique all: {"pos": {"exactitude": 0.85, "exactitude_ferme": 0.9295, "exactitude_ouvert": 0.7746, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 62, "NOUN": 68, "VERB": 4}, "ADV": {"ADV": 131, "NOUN": 7, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 119, "?": 3, "NOUN": 1, "VERB": 1}, "CONJ": {"CONJ": 55, "PRON": 28, "?": 13, "PREP": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 430, "?": 30, "CONJ": 1, "DET": 14}, "VERB": {"VERB": 546, "NOUN": 218, "PREP": 2, "ADJ": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.6715, "rappel": 0.6264, "f1": 0.6482, "tp": 1167, "fp": 571, "fn": 696, "tete": {"precision": 0.8208, "rappel": 0.7203, "f1": 0.7673, "tp": 1342, "fp": 293, "fn": 521}}, "pragmatique": {"acte": 0.9967, "negation": 0.9771, "modalite": 0.9886, "double_sens": 0.9444}, "fraction_semantique": 0.5482}
heuristique HEAD: 0.85 0.9295 0.7746 3179
synt 0.6482 tete 0.7673
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat de7c9113..HEAD -- tools/bloc_linguistique.py tools/tests/linguistique/gold_reel.json tools/tests/linguistique/evaluer_gold.py; echo '---'; git diff de7c9113..HEAD -- docs/pilotage/en-cours.md | head -30", "description … [55 caractères tronqués]`

  ```
tools/bloc_linguistique.py | 9 ++++++++-
 1 file changed, 8 insertions(+), 1 deletion(-)
---
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 4fc69f89..aa319080 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-06, 21 h 45 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-06, 21 h 50 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -106,7 +106,7 @@
 |---|---|---|
 | portes | **84** (dont `porte-produit` le 06/11) | `tools/porte-*.sh` |
 | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
-| fichiers / JSON de résultats | **696** / **789** | `reports/*.md` / `reports/*.json` |
+| fichiers / JSON de résultats | **697** / **790** | `reports/*.md` / `reports/*.json` |
 | documents de `docs/` | **121** (hors archive et README) | `docs/**/*.md` |
 | dernière passe | **03/11 11 h 30** (82, **80/2**, les 2 connues) ; **04/11 08 h 40 arrêtée** ; N3 **17/17** à 11 h 32 ; complète après les runs | `docs/pilotage/references-non-regression.md` |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -E 'juridique  controlee_0.30|code       controlee_0.30|prose      controlee_0.30|tableau    controlee_0.30|technique  controlee_0.30' /tmp/porte-lecteur.log; echo '---'; grep -E 'refus|12/20|9/10|7/8|20/20' /tmp/porte-lecture.l … [68 caractères tronqués]`

  ```
code       controlee_0.30     1.000  0.522   0.500     1244
  juridique  controlee_0.30     1.000  0.306   0.250      837
  prose      controlee_0.30     1.000  0.750   0.750      463
  tableau    controlee_0.30     1.000  0.030   0.250     8599
  technique  controlee_0.30     1.000  0.784   0.750     2567
---
✅ refus : « meilleur score 0.00 < seuil 1.00 — la question ne partage ri… »
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-bloc-linguistique.sh >/tmp/porte-bl-head.log 2>&1; echo exit=$?; tail -2 /tmp/porte-bl-head.log", "description": "Rejouer la porte L au HEAD courant", "run_in_background": true}`

  ```
started background job bash-4237
  ```

- **job_output** `{"job_id": "bash-4237", "timeout_ms": 120000}`

  ```
(no new output)
[status: running]
  ```

- **job_output** `{"job_id": "bash-4237", "timeout_ms": 60000}`

  ```
exit=0
}
✅ porte bloc linguistique verte
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-4237 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-bloc-linguistique.sh >/tmp/porte-bl-head.log 2>&1; echo exit=$?; tail -2 /tmp/porte-bl-head.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('tools/tests/documents/bench-complet.json'))\ns=sum(len(doc.get('questions',[])) for doc in d['documents'])\nprint('field',d['questions'],'sum per doc',s,'docs',len(d['documents']))\nPY … [55 caractères tronqués]`

  ```
field 248 sum per doc 248 docs 30
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche d'état R et du JSON

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md", "content": "# État du chantier R — le lecteur : le tagger n'est pas à 0,944 contre 0,85, R1.2-1024 est mesuré, R4.4 attend la vérité humaine\n\n> **Ligne de roadmap** : **R** (le lecteur) · **Date** : 2026-11- … [37193 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md", "old_string": "**Lecture d'ensemble** : sur **19 lignes R**, **8 sont faites et vérifiées** (R0.1, R0.2, R0.3,\nR0.6, R0.7 heuristique, R1.3, R4.1, R4.2, R4.3 — 9 si l'on compte R4.4-pilote), **2 sont closes\n … [721 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md has been updated successfully.
  ```

- **write** `{"content": "{\n  \"fiche\": \"reports/rapport-etat-r.md\",\n  \"date\": \"2026-11-06\",\n  \"heure\": \"22:10 HNE\",\n  \"branche\": \"s/v7\",\n  \"head\": \"97256b8f\",\n  \"head_au_debut\": \"de7c9113\",\n  \"mission\": \"Etat du chantier R (le lecteur) en lecture seule : inventaire des lignes, v … [31488 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-etat-r.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/pensee-etat-r.json >/dev/null && echo 'JSON OK'; python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-etat-r.json'))\nprint('lignes',len(d['lignes']),'rejeux',len(d['rejeux']),'actions',len(d[' … [273 caractères tronqués]`

  ```
JSON OK
lignes 20 rejeux 13 actions 3 ecarts 13
ids ['R0.1', 'R0.2', 'R0.3', 'R0.4', 'R0.5', 'R0.6', 'R0.7', 'R1.1', 'R1.2', 'R1.3', 'R2.1', 'R2.2', 'R3.1', 'R3.2', 'R4.1', 'R4.2', 'R4.3', 'R4.4', 'R5.1', 'R5.2']
verdict len 1024
---
  443  5967 reports/rapport-etat-r.md
  341  3768 reports/pensee-etat-r.json
  784  9735 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -30; echo exit=${PIPESTATUS[0]}", "description": "Revue documentaire"}`

  ```
revue de documentation · 700 fiche(s) · 793 JSON · 121 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · compteurs : en-cours.md dit 792 JSON, le disque en a 793
exit=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md", "new_string": "**Ce que je n'ai pas rejoué** : le modèle du banc R0.3 (GPU, Qwen2.5-0.5B), la tête de survol\nR0.4 (états précoces Qwen), les entraînements R1.1/R1.2 (checkpoints `work/`), la porte BPE\nR1.3 ( … [623 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '20 réelles 0,9238\\|il reste +6 à +7\\|les scans réels R4.4' reports/rapport-etat-r.md", "description": "Localiser les formulations à corriger"}`

  ```
56:R1.3 (GPU), les scans réels R4.4 (mesures `mesurer_reel.py` ; les deux portes couvrent le pilote
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '0,9238\\|0,9471\\|reste.*6\\|réel 432' reports/rapport-etat-r.md | head -10", "description": "Chercher les passages du tagger"}`

  ```
18:> (heuristique **0,7749** aujourd'hui) et **+6,35 pts** sur le réel 432 (heuristique **0,8754**
240:| `tools/tests/linguistique/qualifier_quatre_modes.py` | le banc **API DeepSeek** (`deepseek-chat`), **gold réel 432**, six modes (heuristique, neuronal, parallèle, cascade, parallèle_niveau, cascade_niveau) |
255:| **7B local** (Qwen2.5-7B-Instruct Q4_K_M, `llama-server` b11017, **CPU** `-ngl 0`) | `gold.json` **20 réelles** (14 fr / 6 en) + `gold_synthetique.json` **160 synthétiques** (fr) | **180 / 804** | POS **0,8483** seul, cascade 0,6 **0,9440** ; 20 réelles **0,9238**, 160 synthétiques **0,9471** ; 0 refus, 180 appels, 3,043 s de moyenne, 548 s |
282:**Pourquoi la baseline a monté** : l'heuristique du bloc L a gagné **+13,1 pts** sur le réel 432
285:tagger a donc fondu** : il reste **+6 à +7 pts** sur le réel, pas **+19**.
389:| 3 | `en-cours.md` R | « **R0.7 — tagger** » dans ce qui reste | le tagger est mesuré (7B local + API) ; il reste **à re-mesurer sur 612** et à **décider** |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md", "new_string": "| **7B local** (Qwen2.5-7B-Instruct Q4_K_M, `llama-server` b11017, **CPU** `-ngl 0`) | `gold.json` **20 réelles** (14 fr / 6 en) + `gold_synthetique.json` **160 synthétiques** (fr) | **180 / 804 … [528 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md", "new_string": "tagger a donc fondu** : il reste **+6,35 pts sur le réel 432** et **+7,34 pts sur le gold\n180**, pas **+19**.", "old_string": "tagger a donc fondu** : il reste **+6 à +7 pts** sur le réel, pas  … [10 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'Non rejouées\\|scans réels' reports/rapport-etat-r.md | tail -6; sed -n '430,443p' reports/rapport-etat-r.md", "description": "Voir la fin de la fiche"}`

  ```
56:R1.3 (GPU), les scans réels R4.4 (mesures `mesurer_reel.py` ; les deux portes couvrent le pilote
217:| `roadmap.md` (R4.4) | 🔬 **« mesuré sur scans simulés ; ouvert sur les scans réels »** |
221:| `rapport-r44-scans.md` (verdict) | **« la ligne reste ouverte pour les scans réels de bout en bout »** |
417:- **R4.4** : les portes tournent sur des **caches** (`work/r44/`) ; les scans réels sont
441:- **Non rejouées** : `tools/tete_survol.py` ; `work/n2ac/eval_fenetre.py` ;
442:  `work/n2ac/mirroir_copie.py` ; `bash tools/porte-r13-bpe.sh` ; les scans réels (portes
  `reports/rapport-r01…r07`, `r13*`, `r44-*`, `n2-r11`, `n2-fenetre`, `n2-r12-2048`,
  `pensee-gold-neuronal`, `pensee-gold-syntagmes`, `pensee-gold-cascade`,
  `pensee-quatre-modes-432`, `pensee-quatre-modes-run2`, `memoire-travail-n5`, `file-taches`.
- **Rejouées** : `bash tools/porte-document.sh` ; `bash tools/porte-lecteur.sh` ;
  `bash tools/porte-lecture.sh` ; `bash tools/porte-balayage.sh` ;
  `bash tools/porte-bloc-tableaux.sh` ; `bash tools/porte-bloc-code.sh` ;
  `bash tools/porte-bloc-maths.sh` ; `bash tools/porte-bloc-linguistique.sh` ;
  `bash tools/porte-ocr.sh` ; `bash tools/porte-ocr-scans.sh` ;
  `python3
… [423 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md", "new_string": "- **Non rejouées** : `tools/tete_survol.py` ; `work/n2ac/eval_fenetre.py` ;\n  `work/n2ac/mirroir_copie.py` ; `bash tools/porte-r13-bpe.sh` ; les scans réels\n  (`tools/mesurer_reel.py` et les J … [244 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md", "new_string": "- **`porte-ocr-scans.sh`** (5 familles, colonnes, tableaux) : **exit 0** ; les 5 familles\n  tiennent leurs planchers, les colonnes et les tableaux aussi ; page noire **0 mot**,\n  mono-colonne  … [855 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-r.md has been updated successfully.
  ```

