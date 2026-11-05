# Session DSH — relecture

- identifiant : `ff7e786c-3ece-4eae-864e-19dddfead93c`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 13:11:54
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **vérifier la cohérence** des fiches B13 du 2026-11-05 avec leurs JSON et avec les valeurs attendues par les portes.

À faire :
1. Dans `reports/`, prends les fiches `rapport-pensee-*.md` datées du 05/11 : verbe-gv, lexique-verbal, spans, denominateur, classement, conventions, attachement-cible, lexique-elargi, echecs-cible, topk-strict, convention-doc (et toute autre fiche B13 du jour).
2. Pour chacune : extrais les chiffres clés (titre, verdict, tableaux) et compare-les (a) au JSON homonyme `pensee-*.json`, (b) aux valeurs attendues par les portes T153, T161, T162, T163, T166, T167, T168, T169, T172, T173 dans `tools/pensee/autotest.py`.
3. Écris **uniquement** deux fichiers neufs : `reports/rapport-coherence-fiches.md` (fiche : titre, verdict, tableau fiche | chiffre | fiche | JSON | porte | verdict, divergences, limites) et `reports/pensee-coherence-fiches.json`.
4. Distingue clairement : (a) les **divergences réelles** (un chiffre faux), (b) les **chiffres historiques** (une fiche antérieure qui cite une valeur d'alors, ce n'est pas une erreur si elle est datée). Ne « corrige » aucune fiche.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : nombre de fiches vérifiées, divergences réelles, chiffres historiques reconnus.
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

⏵ Repérage des fiches B13 du 05/11 et des JSON homonymes

- **bash** `{"command": "git branch --show-current && git status --short | head -20 && ls reports/ | head -50", "description": "Check branch and list reports"}`

  ```
s/v7
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/digest.md
MM journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/rapport.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
07
07-mesures-couche-commune.md
a26-bilan.json
a26-lot-disque.json
a80-audit-final.json
a80-indice-qualifie.json
a80-melange-qualifie.json
a80-pannes-ppl.json
a80-porte-adaptateur.json
a80-porte-budget.json
a80-porte-bus.json
a80-porte-bus-socket.json
a80-porte-c4-retard.json
a80-porte-
… [759 caractères tronqués]
  ```

- **glob** `{"pattern": "reports/rapport-pensee-*.md"}`

  ```
reports/rapport-pensee-silencieuse.md
reports/rapport-pensee-sans-verbaliser.md
reports/rapport-pensee-v0.md
reports/rapport-pensee-ac3-alphabeta.md
reports/rapport-pensee-drvf.md
reports/rapport-pensee-banc.md
reports/rapport-pensee-operateurs.md
reports/rapport-pensee-necessaire.md
reports/rapport-pensee-gold-linguistique.md
reports/rapport-pensee-labyrinthe.md
reports/rapport-pensee-porte.md
reports/rapport-pensee-porte-apprise.md
reports/rapport-pensee-courbe.md
reports/rapport-pensee-seule.md
reports/rapport-pensee-stochastique.md
reports/rapport-pensee-sto-seule.md
reports/rapport-pensee-ferme.md
reports/rapport-pensee-minute.md
reports/rapport-pensee-minute-apprise.md
reports/rapport-pensee-minute-seule.md
reports/rapport-pensee-reseau.md
reports/rapport-pensee-mlp.md
reports/rapport-pensee-correction.md
reports/rapport-pensee-minute-entrainee.md
reports/rapport-pensee-shaping.md
reports/rapport-pensee-professeur.md
reports/rapport-pensee-sans-none.md
reports/rapport-pensee-audit.md
reports/rapport-pensee-ouverte.md
reports/rapport-pensee-graines.md
reports/rapport-pensee-mobile.md
reports/rapport-pensee-mobile-graines.md
reports/rapport-pensee-bruit.md
reports/rapport-pense
… [2633 caractères tronqués]
  ```

- **glob** `{"pattern": "reports/pensee-*.json"}`

  ```
reports/pensee-multilingue.json
reports/pensee-ac3-alphabeta.json
reports/pensee-drvf.json
reports/pensee-banc.json
reports/pensee-operateurs.json
reports/pensee-necessaire.json
reports/pensee-gold-linguistique.json
reports/pensee-labyrinthe.json
reports/pensee-porte.json
reports/pensee-porte-apprise.json
reports/pensee-stochastique.json
reports/pensee-ferme.json
reports/pensee-minute.json
reports/pensee-minute-apprise.json
reports/pensee-courbe.json
reports/pensee-minute-entrainee.json
reports/pensee-shaping.json
reports/pensee-reseau.json
reports/pensee-mlp.json
reports/pensee-professeur.json
reports/pensee-sans-none.json
reports/pensee-correction.json
reports/pensee-audit.json
reports/pensee-ouverte.json
reports/pensee-graines.json
reports/pensee-mobile.json
reports/pensee-mobile-graines.json
reports/pensee-bruit.json
reports/pensee-bouge.json
reports/pensee-bouge-graines.json
reports/pensee-periode.json
reports/pensee-phase.json
reports/pensee-phase-graines.json
reports/pensee-aleatoire.json
reports/pensee-hasard.json
reports/pensee-partielle.json
reports/pensee-croyance.json
reports/pensee-curieuse.json
reports/pensee-observatrice.json
reports/pensee-bruitee.json
reports/pense
… [2059 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Identification des fiches datées du 05/11 parmi les 204 rapports

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in reports/rapport-pensee-{verbe-gv,lexique-verbal,spans,denominateur,classement,conventions,attachement-cible,lexique-elargi,echecs-cible,topk-strict,convention-doc}.md; do if [ -f \"$f\" ]; then echo \"=== $f ===\"; head -12  … [95 caractères tronqués]`

  ```
=== reports/rapport-pensee-verbe-gv.md ===
# B13 — le verbe du GV-phrase : l'exact passe de 0,0586 à 0,0962

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **167/167 portes** : quand le générateur S produit un GV qui couvre **toute la phrase**
> (`The boy saw the cat in the park`), la règle « dernier token » prenait `park` au lieu de `saw`.
> Le bloc prend désormais le **premier token étiqueté `VERB`** à l'intérieur du GV. Sur le gold
> de T153 (612 phrases, 239 cibles) : **exact 14 → 23 (0,0586 → 0,0962)**, top1 **96 → 105**
> (0,4393), top-k **113 → 122** (0,5105), tête **0,7241 / 0,8414**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_verbe_dans`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-verbe-gv.json`](pensee-verbe-gv.json).
=== reports/rapport-pensee-lexique-verbal.md ===
# B13 — le lexique verbal : l'exact passe de 0,0962 à 0,1381

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **168/168 portes** : le POS de surface se trompe sur les classe
… [8417 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -l \"2026-11-05\" reports/rapport-pensee-*.md 2>/dev/null | sort", "description": "Find fiches mentioning 2026-11-05"}`

  ```
reports/rapport-pensee-attachement-cible.md
reports/rapport-pensee-classement.md
reports/rapport-pensee-convention-doc.md
reports/rapport-pensee-conventions.md
reports/rapport-pensee-denominateur.md
reports/rapport-pensee-echecs-cible.md
reports/rapport-pensee-lexique-elargi.md
reports/rapport-pensee-lexique-verbal.md
reports/rapport-pensee-spans.md
reports/rapport-pensee-topk-strict.md
reports/rapport-pensee-verbe-gv.md
  ```

### 🤖 Assistant

⏵ Les 11 fiches B13 du jour sont bien identifiées ; lecture intégrale et JSON

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l reports/rapport-pensee-{verbe-gv,lexique-verbal,spans,denominateur,classement,conventions,attachement-cible,lexique-elargi,echecs-cible,topk-strict,convention-doc}.md reports/pensee-{verbe-gv,lexique-verbal,spans,denominateur,c … [184 caractères tronqués]`

  ```
68 reports/rapport-pensee-verbe-gv.md
    67 reports/rapport-pensee-lexique-verbal.md
    72 reports/rapport-pensee-spans.md
    58 reports/rapport-pensee-denominateur.md
    71 reports/rapport-pensee-classement.md
    59 reports/rapport-pensee-conventions.md
    64 reports/rapport-pensee-attachement-cible.md
    64 reports/rapport-pensee-lexique-elargi.md
    68 reports/rapport-pensee-echecs-cible.md
    57 reports/rapport-pensee-topk-strict.md
    57 reports/rapport-pensee-convention-doc.md
    32 reports/pensee-verbe-gv.json
    33 reports/pensee-lexique-verbal.json
    38 reports/pensee-spans.json
    24 reports/pensee-denominateur.json
    51 reports/pensee-classement.json
    27 reports/pensee-conventions.json
    36 reports/pensee-attachement-cible.json
    36 reports/pensee-lexique-elargi.json
    34 reports/pensee-echecs-cible.json
    25 reports/pensee-topk-strict.json
    21 reports/pensee-convention-doc.json
  2730 tools/pensee/autotest.py
  3792 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"T153\\|T161\\|T162\\|T163\\|T166\\|T167\\|T168\\|T169\\|T172\\|T173\" tools/pensee/autotest.py | head -80", "description": "Locate gate references in autotest"}`

  ```
2699:              ("T153 attachement", t153_attachement()),
2707:              ("T161 cible proximité", t161_cible_proximite()),
2708:              ("T162 candidats verbes", t162_candidats_verbes()),
2709:              ("T163 échecs attachement", t163_echecs_attachement()),
2712:              ("T166 spans perdus", t166_spans()),
2713:              ("T167 dénominateur", t167_denominateur()),
2714:              ("T168 classement", t168_classement()),
2715:              ("T169 conventions", t169_conventions()),
2718:              ("T172 échecs de cible", t172_echecs_cible()),
2719:              ("T173 top-k strict", t173_topk_strict()),
  ```

### 🤖 Assistant

⏵ Localisation des fonctions de porte T153→T173 dans autotest.py

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^def t1\\(53\\|61\\|62\\|63\\|66\\|67\\|68\\|69\\|72\\|73\\)\" tools/pensee/autotest.py", "description": "Find gate function definitions"}`

  ```
2221:def t153_attachement() -> tuple[bool, str]:
2338:def t161_cible_proximite() -> tuple[bool, str]:
2349:def t162_candidats_verbes() -> tuple[bool, str]:
2359:def t163_echecs_attachement() -> tuple[bool, str]:
2406:def t166_spans() -> tuple[bool, str]:
2426:def t167_denominateur() -> tuple[bool, str]:
2438:def t168_classement() -> tuple[bool, str]:
2462:def t169_conventions() -> tuple[bool, str]:
2499:def t172_echecs_cible() -> tuple[bool, str]:
2525:def t173_topk_strict() -> tuple[bool, str]:
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2640,2730p' tools/pensee/autotest.py", "description": "Read gate registration block"}`

  ```
("T94 anaphore corrigée", t94_anaphore_corrigee()),
              ("T95 pronoms objets", t95_objets()),
              ("T96 chaînes longues", t96_chaines()),
              ("T97 résolution par rôle", t97_roles()),
              ("T98 hybride", t98_hybride()),
              ("T99 sémantique", t99_semantique()),
              ("T100 plafond du gold", t100_plafond()),
              ("T101 accord kappa", t101_kappa()),
              ("T102 méta-règle", t102_meta()),
              ("T103 vote pondéré", t103_pondere()),
              ("T104 validation croisée", t104_cv()),
              ("T105 CV 20 graines", t105_cv_graines()),
              ("T106 bilan anaphore", t106_bilan_anaphore()),
              ("T107 gold complet", t107_gold_complet()),
              ("T108 coréférence 68", t108_anaphore_68()),
              ("T109 coréférence 103", t109_anaphore_103()),
              ("T110 segmenteur", t110_segmenteur()),
              ("T111 hybride segmenteur", t111_hybride_seg()),
              ("T112 union segmenteurs", t112_union()),
              ("T113 union par défaut", t113_union_defaut()),
              ("T114 cascade + union", t114_cascade_union()),
              ("T115 tête cascad
… [3697 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des 11 fiches (chiffres, verdicts, tableaux)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-verbe-gv.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-lexique-verbal.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-spans.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-denominateur.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-verbe-gv.md</path>
<type>file</type>
<content>
1: # B13 — le verbe du GV-phrase : l'exact passe de 0,0586 à 0,0962
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **167/167 portes** : quand le générateur S produit un GV qui couvre **toute la phrase**
5: > (`The boy saw the cat in the park`), la règle « dernier token » prenait `park` au lieu de `saw`.
6: > Le bloc prend désormais le **premier token étiqueté `VERB`** à l'intérieur du GV. Sur le gold
7: > de T153 (612 phrases, 239 cibles) : **exact 14 → 23 (0,0586 → 0,0962)**, top1 **96 → 105**
8: > (0,4393), top-k **113 → 122** (0,5105), tête **0,7241 / 0,8414**.
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_verbe_dans`),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
12: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-verbe-gv.json`](pensee-verbe-gv.json).
13: 
14: ## 1. Avant / après (même gold, 239 cibles)
15: 
16: | mesure | avant | **verbe du GV** | écart |
17: |---|---:|---:|---:|
18: | top1 | 96 (0,4017) | 
… [2363 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-lexique-verbal.md</path>
<type>file</type>
<content>
1: # B13 — le lexique verbal : l'exact passe de 0,0962 à 0,1381
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **168/168 portes** : le POS de surface se trompe sur les classes ouvertes anglaises
5: > (`talks` → `NOUN`, `brother` → `VERB`). Un **lexique verbal bilingue** (≈ 200 formes, avec
6: > désinences) arbitre : le verbe est le premier mot du GV qui appartient au lexique, sinon le
7: > premier `VERB` du POS, sinon le dernier mot. Sur le gold de T153 (612 phrases, 239 cibles) :
8: > **exact 23 → 33 (0,1381)**, top1 **115 (0,4812)**, top-k **132 (0,5523)**, tête **0,7862 /
9: > 0,9034**.
10: >
11: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`VERBES_CONNUS`,
12: > `_est_verbe`), [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
13: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-lexique-verbal.json`](pensee-lexique-verbal.json).
14: 
15: ## 1. Avant / après (même gold, 239 cibles)
16: 
17: | mesure | avant | **lexique verbal*
… [2541 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-spans.md</path>
<type>file</type>
<content>
1: # B13 — les 94 spans : 48 REL, 33 SUB, 12 GP
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **169/169 portes** : les échecs d'attachement par **span** (93 après le correctif) sont
5: > **48 REL**, **33 SUB** et **12 GP** — les subordonnées ne sont **pas produites** (65 cas) ou le
6: > sont avec un span plus large (25). Le correctif testé — borner le GP au verbe et au relatif —
7: > gagne **un span** (couverture 0,6067 → 0,6109, F1 0,2864 → 0,2869) mais **perd une cible** :
8: > le total des échecs ne bouge pas (107).
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
12: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-spans.json`](pensee-spans.json).
13: 
14: ## 1. Les 93 spans
15: 
16: | type | échecs de span |
17: |---|---:|
18: | **REL** | **48** |
19: | **SUB** | **33** |
20: | **GP** | **12** |
21: | **tout** | **93** |
22: 
23: | catégorie | nombre |
24: |---|---:|
25: 
… [2337 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-denominateur.md</path>
<type>file</type>
<content>
1: # B13 — le dénominateur de l'attachement : 239 cibles, 146 segments
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **170/170 portes** : les taux d'attachement étaient divisés par **239** (toutes les cibles)
5: > alors que `top1`, `top-k` et `exact` ne mesurent que les **146 segments prédits au bon span**.
6: > Les deux lectures sont désormais nommées : **rendement global** (0,4812 / 0,5523 / 0,1381) et
7: > **exactitude sur les spans** (0,7877 / 0,9041 / 0,2260). Aucune mesure ne change ; c'est la
8: > lecture qui devient honnête.
9: >
10: > **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
11: > [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
12: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-denominateur.json`](pensee-denominateur.json).
13: 
14: ## 1. Les deux lectures
15: 
16: | mesure | rendement global (÷ 239) | **exactitude spans (÷ 146)** |
17: |---|---:|---:|
18: | top1 | 0,4812 | **0,7877** |
19: | top-k | 0,5523 | **0,9
… [1944 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des fiches restantes (classement → convention-doc)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-classement.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-conventions.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-cible.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-lexique-elargi.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-classement.md</path>
<type>file</type>
<content>
1: # B13 — le classement : l'exact passe de 0,2260 à 0,6438 — et le gold mélange deux conventions
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **171/171 portes** : la cible de S était souvent un **GN entier** (« Le garçon », « Les enfants
5: > jouent ») ; elle est désormais **réduite à sa tête** (le verbe plein du texte de la cible s'il y
6: > en a un, sinon son dernier mot). Sur les 146 segments au bon span : **exact 33 → 94**
7: > (0,2260 → **0,6438**). Mais le contrôle révèle que le gold **mélange deux conventions** :
8: > **51 cibles verbes**, **95 cibles noms** (antécédents de REL, têtes de GP).
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
12: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-classement.json`](pensee-classement.json).
13: 
14: ## 1. Avant / après (146 segments au bon span)
15: 
16: | mesure | avant | **cible réduite à sa tête** | écart |
17: |---
… [2733 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-conventions.md</path>
<type>file</type>
<content>
1: # B13 — les deux conventions du gold : verbes 0,7255, noms 0,6000
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **172/172 portes** : la cible d'attachement du gold n'est pas homogène — **51 cibles sont des
5: > verbes** (le gouverneur : `joue`, `vu`) et **95 sont des noms** (l'antécédent d'un REL, la tête
6: > d'un GP : `livre`, `frère`). Mesurées séparément : **verbes 37/51 (0,7255)**, **noms 57/95
7: > (0,6000)**. Le 0,6438 global de T168 était la moyenne de deux choses différentes.
8: >
9: > **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
10: > [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
11: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-conventions.json`](pensee-conventions.json).
12: 
13: ## 1. Les deux mesures
14: 
15: | nature de la cible | cibles | justes | taux |
16: |---|---:|---:|---:|
17: | **verbe** (le gouverneur) | 51 | 37 | **0,7255** |
18: | **nom** (antécédent de REL, tête de GP) | 95 | 57 | **0,6000** |
19
… [2102 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-cible.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement ciblé : l'exact passe de 0,6438 à 0,8082
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **173/173 portes** : la nature de la cible dépend du **type du segment**, et la règle le dit
5: > maintenant : pour un **REL/SUB**, l'attachement est l'**antécédent** (la tête du GN à gauche,
6: > élision séparée : `L'homme` → `homme`) ; pour un **GP**, c'est le **verbe du GV** le plus
7: > proche. Sur les 146 segments au bon span : **exact 94 → 118** (0,6438 → **0,8082**), top1
8: > 0,8356, top-k 0,9041. Par convention : **verbes 48/51 (0,9412)**, **noms 70/95 (0,7368)**.
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_tete_nom`),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
12: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-attachement-cible.json`](pensee-attachement-cible.json).
13: 
14: ## 1. Avant / après (146 segments au bon span)
15: 
16: | mesure | avant | **attachement ciblé** | écart 
… [2494 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-lexique-elargi.md</path>
<type>file</type>
<content>
1: # B13 — le lexique élargi : l'exact passe de 0,8082 à 0,8483
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **174/174 portes** : `vu`, `couru`, `accroché` n'étaient **pas** reconnus comme verbes — le
5: > bloc prenait l'auxiliaire (`a`) pour la cible. Le lexique verbal reçoit les **participes
6: > irréguliers** et une trentaine de verbes courants. Sur les 145 segments au bon span :
7: > **exact 118 → 123** (0,8082 → **0,8483**), top1 0,8690, top-k **0,9241**.
8: >
9: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`VERBES_CONNUS`),
10: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
11: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-lexique-elargi.json`](pensee-lexique-elargi.json).
12: 
13: ## 1. Avant / après (145 segments au bon span)
14: 
15: | mesure | avant | **lexique élargi** | écart |
16: |---|---:|---:|---:|
17: | top1 | 122 (0,8356) | **126 (0,8690)** | +4 |
18: | top-k | 132 (0,9041) | **134 (0,9241)** | +2 |
1
… [2421 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des 3 dernières fiches (échecs-cible, topk-strict, convention-doc)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-echecs-cible.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-topk-strict.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-convention-doc.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-echecs-cible.md</path>
<type>file</type>
<content>
1: # B13 — les 22 échecs de l'attachement ciblé : 11 hors candidats, 11 mal classés
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **175/175 portes** : sur les 145 segments au bon span, **123** ont la bonne cible et **22** ne
5: > l'ont pas. Ces 22 se partagent en **11 cibles absentes des candidats** et **11 cibles présentes
6: > mais non choisies**. Les absences sont surtout des **verbes anglais hors lexique** (`fly`,
7: > `climbs`, `flows`, `swims`, `get`, `smiles`, `wait`) et quelques **noms que le GP complète**
8: > (`chat` de « de la voisine »).
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
12: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-echecs-cible.json`](pensee-echecs-cible.json).
13: 
14: ## 1. La répartition
15: 
16: | catégorie | nombre |
17: |---|---:|
18: | cible **absente** des candidats | **11** |
19: | cible **présente** mais non choisie | **11** 
… [2369 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-topk-strict.md</path>
<type>file</type>
<content>
1: # B13 — le top-k strict : 0,6069, pas 0,9241
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **176/176 portes** : le top-k publié jusqu'ici acceptait les **sous-chaînes** (`vu` ⊂ `aperçu`,
5: > `a` ⊂ `parle`) et affichait **0,9241** ; en **égalité exacte**, la bonne cible n'est dans les
6: > candidats que **88 fois sur 145** — **0,6069**. L'écart de 32 points est un artefact de mesure,
7: > pas un résultat.
8: >
9: > **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
10: > [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
11: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-topk-strict.json`](pensee-topk-strict.json).
12: 
13: ## 1. Les deux top-k (145 segments au bon span)
14: 
15: | mesure | sous-chaîne | **égalité exacte** |
16: |---|---:|---:|
17: | top-k (count) | 134 | **88** |
18: | taux sur les spans | 0,9241 | **0,6069** |
19: | rendement (÷ 239) | 0,5607 | **0,3682** |
20: 
21: **Ce que ça dit** :
22: 
23: - **Le top-k lenient 
… [1794 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-convention-doc.md</path>
<type>file</type>
<content>
1: # B13 — la convention des cibles est documentée dans le gold
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **177/177 portes** : le gold ne disait pas ce qu'était une `cible` ; la lecture des données
5: > (T169, T172) est désormais **écrite dans le gold** (`CONVENTION_CIBLE`) et vérifiée par une
6: > porte. REL/SUB → **antécédent** (tête du GN à gauche) ; GP → **verbe gouverneur**, ou **nom
7: > complété** pour un génitif ; GN/GV → nom ou verbe dont le segment dépend.
8: >
9: > **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
10: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
11: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-convention-doc.json`](pensee-convention-doc.json).
12: 
13: ## 1. Ce qui est écrit
14: 
15: | type | convention de la cible |
16: |---|---|
17: | **REL** | antécédent (tête du GN à gauche) |
18: | **SUB** | antécédent (tête du GN à gauche) |
19: | **GP** | verbe gouverneur ; nom complété pour un géni
… [1860 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle des JSON homonymes (chiffres bruts et métadonnées)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in verbe-gv lexique-verbal spans denominateur classement conventions; do echo \"===== pensee-$f.json =====\"; cat \"reports/pensee-$f.json\"; echo; done", "description": "Dump first six JSONs"}`

  ```
===== pensee-verbe-gv.json =====
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "167/167",
 "gold": 612,
 "cibles": 239,
 "avant": {
  "top1": 96,
  "topk": 113,
  "exact": 14,
  "tete_top1": 96,
  "tete_topk": 113
 },
 "apres": {
  "top1": 105,
  "topk": 122,
  "exact": 23,
  "tete_top1": 105,
  "tete_topk": 122
 },
 "echecs": {
  "span": 94,
  "cible_avant": 32,
  "cible_apres": 23
 },
 "cause_23": "le POS tague le verbe en NOUN (play, talks, leaves...)",
 "limites": [
  "94 spans non qualifiés",
  "POS verbe/nom anglais",
  "gold 612"
 ]
}

===== pensee-lexique-verbal.json =====
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "168/168",
 "gold": 612,
 "cibles": 239,
 "avant": {
  "top1": 105,
  "topk": 122,
  "exact": 23,
  "tete_top1": 105,
  "tete_topk": 122
 },
 "apres": {
  "top1": 115,
  "topk": 132,
  "exact": 33,
  "tete_top1": 114,
  "tete_topk": 131
 },
 "echecs": {
  "span": 94,
  "cible_avant": 23,
  "cible_apres": 13
 },
 "cause_13": "verbes hors lexique (fly, climbs, flows, wait, swims, passes, get, smiles)",
 "limites": [
  "lexique écrit à la main",
  "13 verbes non ajoutés (fuite de test)",
  "94 spans",
  "gold 612"
 ]
}

===== pensee-spans.json =====
… [2167 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in attachement-cible lexique-elargi echecs-cible topk-strict convention-doc; do echo \"===== pensee-$f.json =====\"; cat \"reports/pensee-$f.json\"; echo; done", "description": "Dump last five JSONs"}`

  ```
===== pensee-attachement-cible.json =====
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "173/173",
 "gold": 612,
 "cibles": 239,
 "labels": 146,
 "avant": {
  "exact": 94,
  "exact_span": 0.6438,
  "top1": 114,
  "top1_span": 0.7808,
  "verbe": 0.7255,
  "nom": 0.6
 },
 "apres": {
  "exact": 118,
  "exact_span": 0.8082,
  "top1": 122,
  "top1_span": 0.8356,
  "verbe": 0.9412,
  "nom": 0.7368
 },
 "rendement": {
  "top1": 0.5105,
  "topk": 0.5523,
  "exact": 0.4937
 },
 "regle": "REL/SUB → antécédent (tête du GN à gauche, élision séparée) ; GP → verbe du GV",
 "limites": [
  "28 échecs non qualifiés",
  "convention non documentée",
  "top-k lenient",
  "gold 612"
 ]
}

===== pensee-lexique-elargi.json =====
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "174/174",
 "gold": 612,
 "cibles": 239,
 "labels": 145,
 "avant": {
  "exact": 118,
  "exact_span": 0.8082,
  "top1": 122,
  "topk": 132,
  "verbe": 0.9412,
  "nom": 0.7368
 },
 "apres": {
  "exact": 123,
  "exact_span": 0.8483,
  "top1": 126,
  "topk": 134,
  "verbe": 0.9524,
  "nom": 0.7683
 },
 "rendement": {
  "top1": 0.5272,
  "topk": 0.5607,
  "exact": 0.5146
 },
 "note": "la part verbes passe de 51 à 62 cibles pa
… [1628 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des portes T153→T174 dans autotest.py

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2221,2470p' tools/pensee/autotest.py", "description": "Read gates T153-T169 bodies"}`

  ```
def t153_attachement() -> tuple[bool, str]:
    """L'attachement sur le gold 612 (239 cibles) : top1 0,5272, exact 0,5105."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.5272) < 0.001
            and abs(r["exact_taux"] - 0.5146) < 0.001), (
        f"attachement : top1 {r['top1_taux']}, exact {r['exact_taux']}, "
        f"couverture {r['couverture']}")


def t154_cibles() -> tuple[bool, str]:
    """Les cibles de l'attachement : 1624 segments sans cible sur 1863."""
    from ..tests.linguistique.evaluer_gold import charger
    ph = charger()
    tot = sum(len(p["segments"]) for p in ph)
    sans = sum(1 for p in ph for s in p["segments"] if not s.get("cible"))
    return tot == 1863 and sans == 1624, (
        f"cibles : {sans}/{tot} segments sans cible (couverture {round((tot-sans)/tot,4)})")


def t155_cibles_500() -> tuple[bool, str]:
    """Les 500 premiers segments : 294 GN, 206 GV."""
    from ..tests.linguistique.evaluer_gold import charger
    ph = charger()
    n = 0
    gn = g
… [10188 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2470,2565p' tools/pensee/autotest.py", "description": "Read gates T172-T174 bodies"}`

  ```
f"conventions : verbes {v['justes']}/{v['cibles']} ({v['taux']}), "
        f"noms {n['justes']}/{n['cibles']} ({n['taux']})")


def t170_attachement_cible() -> tuple[bool, str]:
    """L'attachement ciblé : REL → antécédent (nom à gauche), GP → verbe du GV."""
    import tools.bloc_linguistique as bl
    h = bl.Heuristique()
    a = h.analyser("L'homme que j'ai vu dort.", "fr")
    rel = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "REL"]
    cible = ((rel[0].meta or {}).get("attachement") or {}).get("cible") if rel else None
    b = h.analyser("Le garçon joue au ballon.", "fr")
    gp = [e for e in b.etiquettes if e.niveau == "syntagme" and e.type == "GP"]
    cible2 = ((gp[0].meta or {}).get("attachement") or {}).get("cible") if gp else None
    return cible == "homme" and cible2 == "joue", (
        f"ciblé : REL « homme » {cible}, GP « joue » {cible2}")


def t171_lexique_elargi() -> tuple[bool, str]:
    """Le lexique élargi : participes irréguliers et verbes courants (« vu » n'était pas un verbe)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    ok = (bl._est_verbe("vu"), bl._est_verbe
… [3621 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection de evaluer_gold.py pour comprendre `labels`, `topk_exact`, conventions

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"labels\\|topk_exact\\|taux_span\\|def evaluer_bloc\\|def _attachement\\|verbe\\|nom\\|couverture\" tools/tests/linguistique/evaluer_gold.py | head -80", "description": "Locate metrics in evaluer_gold.py"}`

  ```
39:    """Le gold **gelé** : une copie figée pour les portes à nombre absolu.
80:def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
86:    att_n = att_labels = att_top1 = att_topk = att_exact = 0
87:    att_topk_exact = 0
89:    att_t_n = att_t_labels = att_t_top1 = att_t_topk = 0
115:        labels = {(e.type, e.debut, e.fin): e for e in a.etiquettes if e.niveau == "syntagme"}
121:            e = labels.get((s["type"], s["debut"], s["fin"]))
124:            att_labels += 1
130:            # le gold mêle deux conventions : la cible est un verbe (le gouverneur) ou un nom
132:            if bl._est_verbe(cibles[0]):
140:            if any(any(c in nom for c in cibles) for nom in (e.candidats or [])):
143:            if any(nom == cibles[0] for nom in (e.candidats or [])):
144:                att_topk_exact += 1
152:            att_t_labels += 1
157:            if any(any(c in nom for c in cibles) for nom in (et.candidats or [])):
166:        "bloc": nom, "phrases": n,
177:        "attachement": {"cibles": att_n, "labels": att_labels,
184:                        "top1_taux_span": round(att_top1 / max(1, att_labels), 4),
185:                        "topk_taux_span": round(a
… [1004 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/tests/linguistique/evaluer_gold.py && git log --oneline -8 -- reports/rapport-pensee-verbe-gv.md reports/rapport-pensee-convention-doc.md tools/pensee/autotest.py", "description": "Check file size and commit history"}`

  ```
283 tools/tests/linguistique/evaluer_gold.py
0ddd4fb9 B13 — LA CONVENTION DES CIBLES EST DOCUMENTÉE DANS LE GOLD (REL/SUB → ANTÉCÉDENT, GP → VERBE) ; 177/177
e223a98d B13 — LE TOP-K STRICT : 0,6069 EN ÉGALITÉ EXACTE, PAS 0,9241 (SOUS-CHAÎNES) ; 176/176
a048cb83 B13 — LES 22 ÉCHECS DE CIBLE : 11 HORS CANDIDATS, 11 MAL CLASSÉS ; 175/175
a408a909 B13 — LE LEXIQUE ÉLARGI (PARTICIPES IRRÉGULIERS ET EN -É) : EXACT 0,8082 → 0,8483 ; 174/174
23853cb7 B13 — L'ATTACHEMENT CIBLÉ : REL → ANTÉCÉDENT, GP → VERBE ; EXACT 0,6438 → 0,8082, VERBES 0,9412 ; 173/173
f70a1b2a B13 — LES DEUX CONVENTIONS DU GOLD : VERBES 37/51 (0,7255), NOMS 57/95 (0,6000) ; 172/172
d8edd1d9 B13 — LE CLASSEMENT : EXACT 0,2260 → 0,6438 (CIBLE RÉDUITE À SA TÊTE) ; LE GOLD MÊLE DEUX CONVENTIONS (51 VERBES, 95 NOMS) ; 171/171
f8f5bc04 B13 — LE DÉNOMINATEUR DE L'ATTACHEMENT : RENDEMENT (÷239) ET EXACTITUDE SPANS (÷146), 0,7877/0,9041/0,2260 ; 170/170
  ```

### 🤖 Assistant

⏵ Lecture du calcul des métriques d'attachement

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py", "offset": 80, "limit": 125}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py</path>
<type>file</type>
<content>
80: def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
81:     tp = fp = fn = ttp = tfp = tfn = 0
82:     pos_ok = pos_n = pos_ok_ferme = pos_n_ferme = pos_ok_ouvert = pos_n_ouvert = 0
83:     conf = defaultdict(Counter)
84:     acte_ok = neg_ok = mod_ok = ds_ok = 0
85:     fractions = []
86:     att_n = att_labels = att_top1 = att_topk = att_exact = 0
87:     att_topk_exact = 0
88:     att_v_n = att_v_ok = att_n_n = att_n_ok = 0
89:     att_t_n = att_t_labels = att_t_top1 = att_t_topk = 0
90:     for phrase in phrases:
91:         a = bloc.analyser(phrase["texte"], phrase["langue"])
92:         fractions.append(a.fraction_semantique)
93:         pos = _pos_map(a)
94:         for mot in phrase["mots"]:
95:             pred = pos.get((mot["debut"], mot["fin"]), "?")
96:             pos_n += 1
97:             pos_ok += int(pred == mot["pos"])
98:             ferme = mot["pos"] in {"DET", "PREP", "PRON", "CONJ", "AUX", "ADV", "NUM"}
99:             if ferme:
100:                 pos_n_ferme += 1
101:                 pos_ok_ferme += int(pred == m
… [6340 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Exécution ciblée des portes pour établir l'état réel actuel

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 280 python3 - <<'EOF'\nimport time\nfrom tools.pensee import autotest\nnoms = [\"t153_attachement\",\"t161_cible_proximite\",\"t162_candidats_verbes\",\"t163_echecs_attachement\",\n        \"t164_verbe_gv\",\"t165_lexique_ver … [574 caractères tronqués]`

  ```
t153_attachement: OK | attachement : top1 0.5272, exact 0.5146, couverture 0.6067 | 0.5s
t161_cible_proximite: OK | proximité : top1 126/239, exact 123/239, tête 126/145 | 0.4s
t162_candidats_verbes: OK | candidats : top-k 134/239 (0.5607), tête 134/145 | 0.4s
t163_echecs_attachement: OK | échecs : 94 de span, 11 de cible (33 avant les correctifs) | 0.4s
t164_verbe_gv: OK | verbe du GV : saw (attendu saw) ; exact 123/239 | 0.4s
t165_lexique_verbal: OK | lexique : talks True, joue True, brother False ; cible GP talks | 0.0s
t166_spans: OK | spans : 48 REL, 33 SUB, 13 GP | 0.4s
t167_denominateur: OK | dénominateur : spans 0.869 / 0.9241 / 0.8483 | 0.4s
t168_classement: OK | classement : exact 123/146 ; cibles 63 verbes, 82 noms | 0.8s
t169_conventions: OK | conventions : verbes 60/63 (0.9524), noms 63/82 (0.7683) | 0.4s
t170_attachement_cible: OK | ciblé : REL « homme » homme, GP « joue » joue | 0.0s
t171_lexique_elargi: OK | lexique élargi : vu True, accroché True, couru True ; exact 123/145 | 0.4s
t172_echecs_cible: OK | échecs de cible : 11 hors candidats, 11 mal classés | 0.4s
t173_topk_strict: OK | top-k : 134 sous-chaîne, 88 exacts (0.6069) | 0.4s
t174_convention_documentee: OK
… [66 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche d'autres fiches B13 du jour et de leur mode de génération

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -l \"B13\" reports/rapport-*.md 2>/dev/null | wc -l && grep -l \"B13\" reports/rapport-*.md 2>/dev/null | xargs grep -l \"2026-11-05\" 2>/dev/null | sort", "description": "Count and list B13 fiches dated 2026-11-05"}`

  ```
206
reports/rapport-pensee-attachement-cible.md
reports/rapport-pensee-classement.md
reports/rapport-pensee-convention-doc.md
reports/rapport-pensee-conventions.md
reports/rapport-pensee-denominateur.md
reports/rapport-pensee-echecs-cible.md
reports/rapport-pensee-lexique-elargi.md
reports/rapport-pensee-lexique-verbal.md
reports/rapport-pensee-spans.md
reports/rapport-pensee-topk-strict.md
reports/rapport-pensee-verbe-gv.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"pensee-lexique-elargi\\|pensee-convention-doc\" --include=*.py --include=*.sh --include=*.md . | head -20 && git log --oneline -5 -- reports/pensee-lexique-elargi.json", "description": "Find generation references and JSON  … [9 caractères tronqués]`

  ```
./reports/README.md:18:| [`rapport-pensee-convention-doc.md`](rapport-pensee-convention-doc.md) | **B13** — la convention des cibles documentée dans le gold, **177/177** |
./reports/README.md:21:| [`rapport-pensee-lexique-elargi.md`](rapport-pensee-lexique-elargi.md) | **B13** — le lexique élargi : exact 0,8082 → **0,8483**, **174/174** |
./reports/rapport-pensee-lexique-elargi.md:11:> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-lexique-elargi.json`](pensee-lexique-elargi.json).
./reports/rapport-pensee-lexique-elargi.md:64:- [`pensee-lexique-elargi.json`](pensee-lexique-elargi.json) — avant/après.
./reports/rapport-pensee-convention-doc.md:11:> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-convention-doc.json`](pensee-convention-doc.json).
./reports/rapport-pensee-convention-doc.md:57:- [`pensee-convention-doc.json`](pensee-convention-doc.json) — la convention.
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:40056:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > reports/rapport-pensee-lexique-elargi.md <<'MD'\n# B13 — le lexique élargi : l'exact passe de 0,8082 à 0,8414\n\n> **Ligne de roadmap** : 
… [2704 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reconstitution de l'état au commit de la fiche spans

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -20 -- reports/rapport-pensee-spans.md tools/bloc_linguistique.py | head -20", "description": "Log around spans fiche"}`

  ```
a408a909 B13 — LE LEXIQUE ÉLARGI (PARTICIPES IRRÉGULIERS ET EN -É) : EXACT 0,8082 → 0,8483 ; 174/174
23853cb7 B13 — L'ATTACHEMENT CIBLÉ : REL → ANTÉCÉDENT, GP → VERBE ; EXACT 0,6438 → 0,8082, VERBES 0,9412 ; 173/173
d8edd1d9 B13 — LE CLASSEMENT : EXACT 0,2260 → 0,6438 (CIBLE RÉDUITE À SA TÊTE) ; LE GOLD MÊLE DEUX CONVENTIONS (51 VERBES, 95 NOMS) ; 171/171
13e8bb2d B13 — LES SPANS PERDUS : 48 REL, 33 SUB, 12 GP (81 CHEZ S) ; LE GP EST BORNÉ AU VERBE ; 169/169
d400e188 B13 — LE LEXIQUE VERBAL : EXACT 0,0962 → 0,1381, TÊTE 0,9034 ; 168/168
9ff4adda B13 — LE VERBE DU GV-PHRASE : EXACT 0,0586 → 0,0962, TOP-K 0,5105, TÊTE 0,8414 ; 167/167
425754c3 B13 — LES 127 ÉCHECS QUALIFIÉS : 94 DE SPAN, 33 DE CIBLE (32 APRÈS L'UNION) ; 166/166
f7195ce0 B13 — LES CANDIDATS VERBES : TOP-K 0,3264 → 0,4686, TÊTE 0,7655 ; 165/165
f661728c B13 — LE CODE DE LA CIBLE PAR PROXIMITÉ ENTRE DANS HEAD : _cible_proche, T153 À JOUR, T161 ; 164/164
1f74e6cf B13 — LES PASSIFS SANS PAR ENTRENT VRAIMENT DANS HEAD : CHUNKER 3/3 PATIENT, T156/T157 À JOUR, T160 ; 163/163
cc3c73fe B13 — LE CORRECTIF DES PASSIFS : PAR → AGENT, LE GÉNÉRATEUR S COURT-CIRCUITE ; 162/162
92769981 B13 — LA FUSION PAR SOUS-TYPE : LE DOUBLE SENS 
… [927 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -c '              (\"T' tools/pensee/autotest.py; grep -n '(\"T176\\|(\"T175\\|(\"T177' tools/pensee/autotest.py", "description": "Count gate entries"}`

  ```
172
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Comptage exact des portes et vérification du 177/177

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -o '(\"T[0-9]' tools/pensee/autotest.py | wc -l && grep -o '(\"T[0-9]*' tools/pensee/autotest.py | sed 's/.*T//' | sort -n | tail -8 && python3 - <<'EOF'\nimport ast\nsrc=open('tools/pensee/autotest.py').read()\ntree=ast.parse(s … [522 caractères tronqués]`

  ```
177
167
168
169
170
171
172
173
174
portes entries: 177
first,last: T0 store canonique | T174 convention documentée
count: 177
  ```

