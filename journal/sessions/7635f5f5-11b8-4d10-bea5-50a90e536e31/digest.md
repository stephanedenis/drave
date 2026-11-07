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

