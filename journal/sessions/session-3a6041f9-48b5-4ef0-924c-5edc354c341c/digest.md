# Session DSH — relecture

- identifiant : `session-3a6041f9-48b5-4ef0-924c-5edc354c341c`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 06:26:56
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche E1 : la FAQ (D3) est dans `docs/produit/README.md` — ajoute-la au sommaire du document, vérifie les **liens** de la section (aucun lien mort), et mets la ligne FAQ dans `docs/README.md` si elle n'y est pas. Fiche `reports/rapport-faq-sommaire.md` + JSON, commit. Ne change pas le contenu des réponses.

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

- **bash** `{"command": "pwd && git status --short && git log --oneline -5", "description": "Show repo status and recent commits"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
503da67e BILAN DE LA SEMAINE — LE PRODUIT (F1 0,7902, 238/239, TAGGER 95,75), PANINI BORNÉ (DEUX NÉGATIFS), LA COORDINATION, LE HARNAIS (38 LANCEMENTS) ; LES 5 DÉCISIONS EXÉCUTÉES
4d6cffc4 PHASE 4 — D1-D3 (LES EXEMPLES DU TAGGER, LA RESTITUTION v2, LA FAQ 10/10) ; L'INDEX, LA FICHE C3 ORPHELINE (GOLD RÉEL 50) ET LE PLAN COMMITTÉS
5b2d07fc D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270)
e42bac4f JOURNAL — 2026-11-15 : D1, LES EXEMPLES --tagger (441 TOKENS, 3,7 S) ET --reel (452 PHRASES) SONT DANS LA DOC ; 5/5 REJOUÉS, MUTATION 4/5
d23780d7 D1 — LES EXEMPLES DU TAGGER ET DE LA BASE RÉELLE : 3 BLOCS --tagger (441 TOKENS, 3,7 S), 2 BLOCS --reel (45
… [58 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
1: # Le premier produit — analyser un texte avec Drave
2: 
3: > **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
4: > linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
5: > il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
6: > qu'il garantit.
7: >
8: > **Vérifié le 2026-11-14** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
9: > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
10: > existent, et la
11: > porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
12: > § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le format
13: > est **version 2** (`schema: "drave.annotation"`,
14: > `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
15: > reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
16: > § 3.5 ont été relancées le 07/11 pour le format
… [51645 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md</path>
<type>file</type>
<content>
1: # La documentation de [Drave](theorie/glossaire/entrees/drave.md) — quatre familles
2: 
3: > **`docs/` dit ce qui reste vrai** : la méthode, l'[état](theorie/glossaire/entrees/etat.md), la théorie, l'implantation. Les **chiffres** et les
4: > séries vivent dans [`reports/`](../reports/) ; le **récit daté** dans [`journal/`](../journal/). Une page de
5: > `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/`.
6: 
7: > **Chargement facultatif.** Aucun document de ce dossier n'est nécessaire pour commencer une tâche : lire
8: > [`AGENTS.md`](../AGENTS.md), puis le document de la tâche. Le reste se [charge](theorie/glossaire/entrees/charge-flux-chargeflux.md) au besoin.
9: 
10: ## En trois portes
11: 
12: | si vous voulez… | lisez |
13: |---|---|
14: | **comprendre le projet** | [la vision](theorie/vision.md) · [la mission](methode/mission.md) · [le protocole sémantique](theorie/protocole-semantique.md) · [le glossaire](theorie/glossaire.md) · [la synthèse](theorie/synthese/index.md) |
15: | **faire** (résultat, [porte](theorie/glossaire/entrees/porte.md), ran
… [9152 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"E1\" --include=\"*.md\" --include=\"*.json\" docs reports tools/chantier 2>/dev/null | head -40", "description": "Search for task E1 references"}`

  ```
docs/archive/biologie-pour-drave.md:342:### 4 bis. E1 — le résultat : un connectome inné ALÉATOIRE coûte 1 %
docs/archive/biologie-pour-drave.md:439:| **E1** | **masque inné creux** : masque aléatoire fixe à **25 %** des connexions par ligne, seuls ces poids sont appris, mesuré au protocole 8 × 128 contre un dense iso-tout | la structure fixe suffit-elle, ou faut-il apprendre *où* sont les connexions ? | **FAIT — voir § 4 bis** — **RE-MESURÉ le 11/10 avec un masque qui couvre TOUT le modèle** (le précédent ne couvrait que les `nn.Linear`, 5,8 % des poids, et se taisait) : **+9,4 %** à 25 % de densité et **+18,4 %** à 12,5 %, contre le « 1 % » annoncé qui décrivait l'attention seule |
docs/archive/biologie-pour-drave.md:446:**La première à faire est E1** : c'est la moins chère, elle teste directement la
docs/archive/cerveau-facultes.md:15:> expériences **E1-E9**, `docs/pilotage/manques.md` ce qui **manque** (M1-M9, N1-N5). Ici, l'entrée est la
docs/archive/etat-cerveau.md:21:> `docs/biologie-pour-drave.md` (expériences E1-E9), `docs/pilotage/manques.md` (ce qui manque).
docs/archive/etat-cerveau.md:29:> 3. **les expériences de biologie E1-E9** → § 3 (**E9** — l'homéostasie synaptiqu
… [6246 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -i \"sommaire\" docs/produit docs/README.md reports 2>/dev/null | head -40", "description": "Search for sommaire mentions"}`

  ```
reports/historique-passes-portes.md:196:> outils de la nuit (distillation E5, `--lora-depart`, fusion **sommaire** de plusieurs LoRA,
  ```

- **bash** `{"command": "ls reports/ | grep -i faq; echo ---; ls reports/ | head -30; echo ---; sed -n '1,80p' tools/chantier/plan.json", "description": "List FAQ reports and plan beginning"}`

  ```
faq.json
rapport-faq.md
---
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
a80-porte-consolidation.json
a80-porte-cycle-c2.json
a80-porte-delais.json
a80-porte-flux.json
a80-porte-fusion.json
a80-porte-gain.json
a80-porte-pont.json
a80-porte-profondeur.json
a80-porte-reflexe.json
a80-porte-reparti.json
a80-portes-ppl.json
a80-porte-topologie.json
a80-porte-trace.json
a83a-coupe.json
a83a-flux.json
a83a-pont.json
a83b-decision.json
---
{
 "nom": "Semaine 07/11 → 14/11 — le produit et l'intégration Panini",
 "principe": "Une tâche n'est finie que si son acceptation passe ; l'agent commite, le superviseur vérifie.",
 "taches": [
  {
   "id": "J0",
   "jour": 0,
   "titre": "Le contrôle du superviseur",
   "mandat": "Réponds exactement le mot OK, sans autre texte. C'est un test de liaison du superviseur.",
   "budget_min": 2,
   "acceptation": [
    {
     "commande": "python3 -c \"print('LIAISON-OK')\"",
     "attendu": "LIAISON-OK"
    }
   ]
  },
  {
   "id
… [2743 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d['taches']:\n    if t['id']=='E1':\n        print(json.dumps(t,ensure_ascii=False,indent=2))\nEOF", "description": "Print E1 task from plan"}`

  ```
{
  "id": "E1",
  "jour": 15,
  "titre": "La FAQ dans le sommaire et les liens",
  "mandat": "Tâche E1 : la FAQ (D3) est dans `docs/produit/README.md` — ajoute-la au sommaire du document, vérifie les **liens** de la section (aucun lien mort), et mets la ligne FAQ dans `docs/README.md` si elle n'y est pas. Fiche `reports/rapport-faq-sommaire.md` + JSON, commit. Ne change pas le contenu des réponses.",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f reports/rapport-faq-sommaire.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    },
    {
      "commande": "python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?",
      "attendu": "REVUE-0"
    }
  ]
}
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md</path>
<type>file</type>
<content>
1: # B13 / D3 — la FAQ du produit : dix questions, dix réponses vérifiées
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : **D3** · **Date** : 2026-11-15 ·
4: > **Verdict** : ✅ **10/10 réponses vérifiées** contre le code courant (`drave 0.1.0`) ;
5: > **contrôle négatif détecté** (deux affirmations fausses sont rejetées par le code).
6: >
7: > **La question.** Un utilisateur qui découvre le produit se pose dix questions concrètes :
8: > la langue, le hors-ligne, le coût, le tagger, le schéma, l'attachement, les spans
9: > inatteignables, la restitution, les limites, l'installation. La notice y répond-elle
10: > encore, ou répète-t-elle des chiffres d'hier ?
11: >
12: > **La réponse.** La section **§ 8** de [`docs/produit/README.md`](../docs/produit/README.md)
13: > porte les dix questions ; chacune est adossée à une commande, à une constante du code ou à
14: > un JSON de `reports/`, et **dix contrôles exécutables** les rejouent. Les dix passent. Le
15: > contrôle négatif est explicite : le CLI **refuse** `--langue de` (code 2) et le schéma v2
16: > **refuse
… [9790 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/faq.json", "description": "Read FAQ JSON"}`

  ```
{
 "schema": "drave.faq.verification",
 "version": 1,
 "date": "2026-11-15",
 "produit": "0.1.0",
 "fichier": "docs/produit/README.md#8-faq--dix-questions",
 "questions": [
  {
   "id": 1,
   "question": "Quelles langues le produit reconnaît-il ?",
   "observe": {
    "detection": {
     "Der Hund schläft.": "de",
     "El perro duerme.": "es"
    },
    "und": {
     "Élodie sourit.": "und",
     "avec --langue fr": "und"
    },
    "indice_cli": {
     "choix": [
      "fr",
      "en"
     ],
     "--langue de": "code 2"
    },
    "profils_udhr": {
     "langues": 398,
     "exactitude": 0.9687,
     "seuil": 0.12,
     "source": "reports/rapport-bloc-linguistique.md"
    }
   },
   "ok": true,
   "erreur": ""
  },
  {
   "id": 2,
   "question": "Est-ce que ça marche hors ligne ?",
   "observe": {
    "socket_interdite": {
     "code": 0,
     "module_reseau_importe": false
    },
    "tagger_sans_cle": {
     "code": 4,
     "stdout_vide": true,
     "stderr": "dépendance absente … hors ligne"
    },
    "defaut": "heuristique, CPU, sans modèle, sans GPU, sans réseau"
   },
   "ok": true,
   "erreur": ""
  },
  {
   "id": 3,
   "question": "Combien ça coûte ?",
   "observe": {
… [5714 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -i \"^#\\+ .*sommaire\\|sommaire\" docs --include=\"*.md\" | head -40", "description": "Search for Sommaire headings in docs"}`

  ```
docs/implantation/lecteur-controleur.md:34:| **survol** | les en-têtes (`titre`, `section`) | leur texte | c'est le sommaire : il oriente tout le reste, et il est court |
  ```

- **bash** `{"command": "grep -rn \"produit/README.md\" docs reports --include=\"*.md\" --include=\"*.json\" | head -40", "description": "Find references to produit README"}`

  ```
docs/pilotage/roadmap.md:91:[`docs/produit/README.md`](../produit/README.md) § 3.3 bis documente les **quatre** champs de
docs/README.md:96:| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte avec Drave |
reports/rapport-evaluer-langue.md:98:2. **J11.4** — documenter le schéma v2 (rétro-compatibilité v1) dans `docs/produit/README.md`.
reports/rapport-evaluer-langue.md:107:- [`docs/produit/README.md`](../docs/produit/README.md) — § 3.3 et § 7 (option documentée).
reports/schema-v2-doc.json:13:  "fichier": "docs/produit/README.md",
reports/rapport-schema-v2-doc.md:10:> [`docs/produit/README.md`](../docs/produit/README.md) § 3.3 bis : les **quatre** champs de
reports/rapport-schema-v2-doc.md:24:> [`docs/produit/README.md`](../docs/produit/README.md) ; JSON
reports/rapport-schema-v2-doc.md:183:- [`docs/produit/README.md`](../docs/produit/README.md) — § 3.3 bis : les deux champs, l'exemple,
reports/rapport-tagger-option.md:176:- [`docs/produit/README.md`](../docs/produit/README.md) § 3.7 — la notice d'usage de l'option.
reports/rapport-exemples-tagger.md:148:- [`docs/produit/README.md`](../docs/produit/README.md) § 3.7 — recalé sur le code courant :
r
… [417 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -20 -- docs/produit/README.md docs/README.md reports/rapport-faq.md", "description": "History of the docs and FAQ report"}`

  ```
5b2d07fc D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270)
d23780d7 D1 — LES EXEMPLES DU TAGGER ET DE LA BASE RÉELLE : 3 BLOCS --tagger (441 TOKENS, 3,7 S), 2 BLOCS --reel (452 PHRASES, POS 88,91, F1 79,06), 5/5 REJOUÉS, MUTATION 4/5
c24253ee DOC PRODUIT — LA PASSE D'HONNÊTETÉ : LES TROIS BASES (612, 602, RÉEL 452), L'ATTACHEMENT 238/239, LE TAGGER 95,75, LES CHIFFRES DATÉS ANNOTÉS
ce7241d5 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS
5b03a0dd DOC PRODUIT — LE TAGGER EN OPTION DOCUMENTÉ (CACHE CHAUD, COÛT, LIEN DE LA FICHE) ; § 3.7 COMPLET
0bbdbbb3 1A — LE TAGGER POS EN OPTION (--tagger) : +8,49 PTS SUR LE GOLD 612 (+4,67 SUR LE RÉEL 432), LE DÉFAUT RESTE HORS LIGNE ; 14 TESTS, DOC § 3.7
febfdfff J11.4 — SCHÉMA v2 DOCUMENTÉ : 4 CHAMPS PARTITION + 10 CHAMPS ALTERNATIVE, 6 CAS / 0 ÉCHEC, LES DEUX VERSIONS LUES (612 v2 + 612 v1)
09e54143 J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ
229098ec J8.1 — RESTITUTION V1 
… [1107 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -i \"faq\" journal --include=\"*.md\" | head -30; echo ===; grep -rn -i \"sommaire\" journal --include=\"*.md\" | head -20", "description": "Search journal for FAQ and sommaire"}`

  ```
journal/sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/digest.md:11307:EK/Hzg5WwkZeP0vEdBQVbLmwX3C7tZ5unAxxqyWsak65Zx+i/YGBTI5dwtzSwn/74RPT6/yxQIFOlQdrPe8NslIAhXE0dULgLUiVU9+MaZkrS4//NYtS9qHB1Ar23Y1eJpb1lYwQI1/HeTR/gYk/nq4sZx/HsknDL01B2FjvGpyZhnyIrK5mZYRDY6hRygYaoDZ78uzIgbSn/r2w/B/VMve3yjlEEAdrMo75aVw6JdkTHBrNUaDIs4iMrpb1KMS3VnSxq8KS5awapNAqFdR8uRd5g84fwphjpJX6w6oVcec1uWv68O14DyOwdcc5rTOr3BAxguKBJNeveR/4KWxSHoGJ9zF2zREnAMUjCxLIl6XonyUEN6WWBaHX5CVk2Sola1qykydOjVuyk12T3Oydudock8FzsxcX+/Un2mPg0BIKk+OGYU8FoaIdEC1cOAmMvB68rHaK5AruXb568ButqI55eXpcMJUcveZcK9zU5cBar81SjI93k2vYAq7oeaxco+SdPCFnLsAEF4l/VmuqvqLNgYnJWx9R+HQ1KJosHuTQsojrW8py4CX7CPgEwC1Xnpp9Gb8OKLFqFsazU520HZH6XoLORlYbG/TNdTuW/rx4Sl8YmelUU/wZoJJ9VbkvGbAYIPu5e1K0LT5ncMVyC7eMrSjPFUG8ElZrwW3jMepPeWYntkPIU9DVe9Aa9t1yHyJGQ7q0YLw9w5ahC84a4FGBAnlLPSifaqNIL8fsPYZXWoCbl8xLjxlcN/Y7evubFTLTLjNKgAhwST6swawR29P2qTbmXYwnK9cBkHVkMq93Z7zWXEtPNqcU8jMPE612kOJRdRYZlTDu/FZp7ubHlsamWpl7Vl+g0j4CjYMyMaGhDqaQlLMXKhFwIHaMwiyvXPsBYIOOA5uUC6vb4M4vpxY+LbvOdkH/KzRj+gHib3R1b6mBpswByQH7sdWeBESEU+8PQZKW4Bf47gZtGKZmqZjZTgPHZ7CtNYOP8GRjJto41/l/HVO5UdfyWI9nwPT18fpA3DA0nHkr0Ia9AVP9u/qULj9BomnzT0m3KPzRZ+8CFGuWwrlOFh/EZAYY9ggsCXTkIf4lJoQjFExCR4uPhVOenNRkziIhtBYRyb+9G3
… [10066 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/roadmap.md | grep -n -i \"faq\\|produit\" ; echo ===; grep -n -i \"faq\" docs/pilotage/*.md docs/pilotage/backlog/*.md 2>/dev/null | head -30", "description": "Search roadmap for FAQ"}`

  ```
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 vs 0,427)** ([fiche](../../reports/rapport-retrieval-epoque.md)) ; **J3.2 généalogie à deux faces : Panini couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au hasard exact, le signal de famille vit dans 
… [5624 caractères tronqués]
  ```

- **bash** `{"command": "wc -w docs/README.md docs/produit/README.md; grep -c \"\" docs/README.md; python3 tools/taille_documents.py 2>&1 | tail -20", "description": "Check document word budgets"}`

  ```
980 docs/README.md
 7602 docs/produit/README.md
 8582 total
111
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2495    223   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3990 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-visi
… [203 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/revue_documentation.py", "description": "Read revue documentation script"}`

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
… [6605 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"produit\\|README\" tools/taille_documents.py | head -30; echo ===; sed -n '1,80p' tools/taille_documents.py", "description": "Inspect document size tool classification"}`

  ```
11:Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
33:    ("T1", "docs/README.md", 1000),
41:    ("T1", "docs/theorie/glossaire/README.md", 2000),
42:    ("T1", "docs/schemas/README.md", 1500),
44:    ("T1", "reports/README.md", 2800),
45:    ("T1", "README.md", 3500),
128:        if p.name in ("README.md", "INDEX.md") or p.name.startswith("historique-"):
===
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

Les **sources de diagrammes** (
… [2735 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline --follow -- docs/produit/README.md | tail -10; echo ===; git log --oneline --follow -- docs/produit/README.md | wc -l", "description": "Full history of produit README"}`

  ```
8eb0cc49 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE
9a259953 B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE
5b9c18ef PRODUIT — --fichier ET --jsonl (TRAITEMENT DE CORPUS, UNE LIGNE JSON PAR PHRASE) ; 16 TESTS
662a3698 PRODUIT — evaluer PUBLIE LES DEUX VUES (FIDÈLE F1 75,33 / LINÉAIRE 81,04, COUVERTURE 93,31) ; 14 TESTS
027abba4 PRODUIT — --contexte DANS LA CLI (MÉMOIRE DE DISCOURS PORTÉE DANS LE JSON), 11 TESTS
bfd98892 DOC PRODUIT — RESYNCHRONISÉE : POS 85,00 %, F1 0,6482, ATTACHEMENT 235/236, GELÉ 85,32 / 0,6511 ; SORTIE D'EVALUER REJOUÉE
d31aa9a2 PRODUIT — --partition DANS LA CLI (alternative PAR DÉFAUT, filtrer EN OPTION), 10 TESTS, DOC À JOUR
e2258fb9 DOC PRODUIT — LES CHIFFRES À JOUR : POS 83,83 %, F1 64,74 %, ATTACHEMENT 235/236 (98,33 %), 3 SPANS ; SORTIE D'EVALUER REJOUÉE
7f73c17f PRODUIT — LA DOC D'USAGE ET LES 5 EXEMPLES VÉRIFIÉS (5/5 REJOUÉS) ; CASCADE_POS N'EST PLUS UNE ROUGE (PLANCHER 0,70)
9952a330 PRODUIT — LA DOC D'USAGE ET LES EXEMPLES ; cascade_pos DEVIENT UN PLANCHER (0,70) ET LA PORTE BLOC REPASSE VERTE ; 84 PORTES
===
19
  ```

- **bash** `{"command": "git show $(git log --format=%H --follow -- docs/produit/README.md | tail -1):docs/produit/README.md 2>/dev/null | sed -n '1,60p'", "description": "Inspect first version of produit README"}`

  ```
# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-06** sur la branche `s/v7`. Le CLI unifié **`tools/drave.py`** est
> **livré** : `analyser`, `evaluer`, `rejouer`, `--version` ; la **porte produit**
> (`bash tools/porte-produit.sh`) le vérifie en **6 contrôles** et **1 min 56** ; le smoke test
> `tools/tests/test_produit.py` passe **6 tests en 1,2 s**. Les exemples du § 3 sont réels : ils
> ont été lancés pour ce document.
>
> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
> candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.

## 1. À qui s'adresse le produit

| vous êtes… | ce que vous obtenez | ce qu'il faut savoir |
|---|---|---|
| **linguiste, enseignant, curieux** | une analyse 
… [3027 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"produit\" tools/docwatch* tools/*.py 2>/dev/null | head -20; ls tools/docwatch 2>/dev/null", "description": "Check docwatch references to produit"}`

  ```
tools/docwatch/src/docwatch/diagrams.py:233:            # Ne pas écraser un SVG qui n'a pas été produit par docwatch.
tools/docwatch/src/docwatch/diagrams.py:261:        produit = generer_fichier_source(source, settings)
tools/docwatch/src/docwatch/diagrams.py:262:        if produit is not None:
tools/docwatch/src/docwatch/diagrams.py:263:            faits.append(str(produit))
tools/docwatch/src/docwatch/render.py:160:#: URL d'annexe produite par :func:`reecrire_assets`. On ne capture que la
tools/amplification.py:17:produit exactement le tableau du §57 — `S_langue ≈ S_domaine ≈ 1`.
tools/analyse_litteraire.py:6:**déjà produites** (200 paires 1:1 du *Tour du monde*) et on les décompose ✓✓ :
tools/banc-experts.py:11:Ce banc reproduit ce motif — des **plages d'expert** (4 Mio) dispersées, parcourues page
tools/bloc_linguistique.py:6:  - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
tools/bloc_linguistique.py:870:        # les **nombres** ont une classe (l'audit produit : 45 nombres sans POS)
tools/bloc_linguistique.py:1459:            # une entrée non textuelle est **refusée** proprement (le produit ne plante pas)
tools/bloc_maths.py:16:  
… [863 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '200,420p' tools/revue_documentation.py", "description": "Read rest of revue documentation script"}`

  ```
try:
            texte = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for cible in liens(texte):
            if cible.startswith(("http://", "https://", "mailto:")):
                continue
            p = (f.parent / cible).resolve()
            if not p.exists() and not cible_generee(f, cible):
                alertes.append(f"annotation : {f.relative_to(RACINE)} → {cible} (cassé)")
    for f in sources_propres():
        try:
            texte = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for label, cible in re.findall(r"\[([^\]]+)\]\(([^)#]+?)\)", texte):
            if cible.startswith(("http://", "https://", "mailto:")):
                continue
            lab = label.strip("`")
            if not (re.match(r"^(docs|reports|tools|journal)/", lab)
                    and lab.endswith((".md", ".json", ".sh"))):
                continue
            p = (f.parent / cible).resolve()
            lp = (RACINE / lab).resolve()
            if p.exists() and lp != p:
                alertes.append(
                    f"libellé : {f.relative_to(RACINE)} annonce « {lab} » mai
… [7124 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '100,240p' tools/taille_documents.py", "description": "Read budget comparison logic"}`

  ```
specifiques = {"organisation-du-depot.md", "modularisation.md", "relations-humaines.md"}
    for cat, motif, budget in BUDGETS:
        for p in sorted(RACINE.glob(motif)):
            if not p.is_file():
                continue
            if motif == "docs/methode/*.md" and p.name in specifiques:
                continue
            rel = str(p.relative_to(RACINE))
            t = p.read_text(encoding="utf-8", errors="ignore")
            n = mots_hors_diagrammes(t)
            lignes.append((n, t.count("\n") + 1, rel, cat, budget))
            tete = "\n".join(t.splitlines()[:20])
            if cat in ("T0", "T1"):
                if not t.lstrip().startswith("#"):
                    violations.append(f"{rel} : pas de titre (#) en tête")
                if "> " not in tete:
                    violations.append(f"{rel} : pas de résumé (blockquote) dans les 20 premières lignes")
            if rel in DATE_DOCS:
                if "Résumé" not in tete:
                    violations.append(f"{rel} : document daté sans « Résumé » en tête")
                if "ne pas charger" not in tete.lower() and "ne jamais charger" not in tete.lower():
                    violations.append(f"
… [2573 caractères tronqués]
  ```

- **bash** `{"command": "date; grep -n \"Mis à jour\" docs/pilotage/en-cours.md | head; grep -n \"fichiers / JSON\\|documents de\\|portes |\\*\\*\" docs/pilotage/en-cours.md | head", "description": "Check date and en-cours counters"}`

  ```
dim 15 nov 2026 06:27:47 EST
3:**Mis à jour : 2026-11-15, 06 h 40 HNE (bilan de la semaine écrit)**
109:| fichiers / JSON de résultats | **746** / **839** | `reports/*.md` / `reports/*.json` |
110:| documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
  ```

- **bash** `{"command": "ls reports/*.md | wc -l; ls reports/*.json | wc -l; git ls-files 'reports/*.md' | wc -l; git ls-files 'reports/*.json' | wc -l; echo ===; sed -n '1,40p' reports/INDEX.md; echo ===; tail -30 reports/INDEX.md", "description": "Count reports and inspect index"}`

  ```
746
839
915
839
===
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **743 fiches**. Les fichiers
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
| [fiche-nuit-17-10.md](fiche-nuit-17-10.md) | 
… [7192 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"rapport-faq\\|faq.json\\|rapport-s-paragraphes\\|rapport-restitution-v2\" reports/INDEX.md reports/README.md 2>/dev/null", "description": "Check FAQ index entries"}`

  ```
reports/INDEX.md:187:| [rapport-faq.md](rapport-faq.md) | B13 / D3 — la FAQ du produit : dix questions, dix réponses vérifiées |
reports/INDEX.md:692:| [rapport-restitution-v2.md](rapport-restitution-v2.md) | B13 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas |
reports/INDEX.md:709:| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
reports/README.md:61:| [`rapport-restitution-v2.md`](rapport-restitution-v2.md) | **B13** — restitution v2 : rôles **16/46**, F1 **0,5270** |
  ```

- **bash** `{"command": "sed -n '1,130p' docs/pilotage/en-cours.md", "description": "Read current state document"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 06 h 40 HNE (bilan de la semaine écrit)**

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
> le hook pre-commit refuse un
… [10039 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re, pathlib\np=pathlib.Path('docs/produit/README.md')\nt=p.read_text()\nm=re.search(r'^## 8\\. .*$', t, re.M)\nn=re.search(r'^## 9\\. .*$', t, re.M)\ns=t[m.start():n.start()]\nfor label,target in re.findall(r'\\[([^\\]]+)\\]\\(([^)]+)\\)', s):\n    print(repr(l … [76 caractères tronqués]`

  ```
'`tools/verifier_faq.py`' -> ../../tools/verifier_faq.py
'`reports/rapport-faq.md`' -> ../../reports/rapport-faq.md
'`reports/faq.json`' -> ../../reports/faq.json
'`exemples.md`' -> exemples.md
'`rapport-g017.md`' -> ../../reports/rapport-g017.md
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re, pathlib\np=pathlib.Path('docs/produit/README.md')\nt=p.read_text()\nfor m in re.finditer(r'^#{1,4} .*$', t, re.M):\n    print(m.group(0))\nEOF", "description": "List all headings in produit README"}`

  ```
# Le premier produit — analyser un texte avec Drave
## 1. À qui s'adresse le produit
## 2. Ce que le produit fait
## 3. Comment l'utiliser — cinq exemples réels
### 3.1 Analyser une phrase
### 3.2 Analyser en JSON et lire l'attachement
### 3.3 Mesurer sur le gold
### 3.3 quater Traiter un corpus
### 3.3 bis La vue des syntagmes qui se chevauchent — les champs du schéma v2
### 3.3 ter Le contexte (mémoire de discours)
### 3.4 Rejouer et vérifier le déterminisme
### 3.5 Le refus, et la langue inconnue
### 3.6 Restituer la surface (v0)
### 3.6 bis La base honnête — `--reel`
### 3.7 Le tagger en option — `--tagger`
## 4. Ce que le produit ne fait pas encore
## 5. Performance
## 6. Garanties
## 7. Le CLI livré — contrat et manques
## 8. FAQ — dix questions
### 8.1 Quelles langues le produit reconnaît-il ?
### 8.2 Est-ce que ça marche hors ligne ?
### 8.3 Combien ça coûte ?
### 8.4 Qu'est-ce que `--tagger` change ?
### 8.5 Quel est le format de sortie, et est-il stable ?
### 8.6 Que veut dire « attachement », et à quel point est-il fiable ?
### 8.7 Pourquoi reste-t-il un span inatteignable ?
### 8.8 Que peut-on restituer : la surface, la forme, les rôles ?
### 8.9 Quelles limites faut-il
… [100 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/index_reports.py 2>/dev/null || true", "description": "Inspect reports index generator"}`

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

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d['taches']:\n    if t.get('jour') in (15,16) or t['id'].startswith(('E','F')):\n        print(t['id'], '|', t.get('titre'), '|', t.get('mandat','')[:160])\nEOF", "description": "List E/F tasks in pl … [4 caractères tronqués]`

  ```
C1 | Coordination N2 — la commande validée | Tâche C1 : la coordination N2, suite de J4.1 — écris `reports/rapport-coordination-n2-v2.md` + JSON : la commande **validée** `python3 work/n2ac/eval_longueurs.
C2 | Coordination S — la page / et la v7 | Tâche C2 : la coordination S, suite de J4.2 — écris `reports/rapport-coordination-s-v2.md` + JSON : l'état de la page `/` (le service de la v7), le pare-feu rés
C3 | Coordination R — le gold réel étendu | Tâche C3 : la coordination R — propose et mesure l'extension du gold réel (le « gold 200+ » des fiches R) : prends 50 phrases **réelles** (hand + reel) que l'he
B1 | Panini — le protocole à date contrôlée | Tâche B1 : le protocole Panini à date contrôlée (la suite de la note 4A) — construis `reports/rapport-protocole-date.md` + JSON : 60 paires en trois groupes (20
B2 | Panini — les atomes et les niveaux, prédiction | Tâche B2 : les 14 atomes comme prédicteurs des 8 niveaux Drave — sur les 44 œuvres × 14 flottants (JSON plat, lecture seule chez Panini), mesure la prédiction d
B3 | Panini — le corpus d'or CIC étendu | Tâche B3 : le corpus d'or CIC (42 verdicts, 42/42 reproduits en J12.2) — étends le vérificateur : les 36 preuves altérées
… [1039 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"sommaire\\|table des matières\" tools/*.py docs/methode docs/produit 2>/dev/null | head -30", "description": "Search for TOC conventions in tools/method"}`

  ```
tools/aligneur_litteraire.py:5:**invalide** ✗✗ : découpage par titres (84 sections françaises contre 37 anglaises, la table des matières comptée
tools/aligneur_litteraire.py:1049:    L.append("### 2.2 Découpage en chapitres — et le piège de la table des matières")
tools/aligneur_litteraire.py:1060:    L.append("| langue | lignes candidates | chapitres retenus | lignes écartées (table des matières) |")
tools/lecteur_controleur.py:185:        """Lire les en-têtes (titre/section) : c'est le sommaire, et il coûte peu."""
tools/lecteur_controleur.py:187:        self._lire(entetes, "survol", "sommaire")
tools/session_report.py:73:    de l'assistant cassent la table des matières du rapport."""
  ```

- **bash** `{"command": "python3 tools/index_reports.py --verifier; echo \"exit=$?\"; python3 tools/index_reports.py --aide | head", "description": "Check if reports index is stale"}`

  ```
exit=0
usage: index_reports.py [-h] [--verifier] [--aide]

Génère reports/INDEX.md (déterministe).

options:
  -h, --help  show this help message and exit
  --verifier  ne réécrit rien : compare l'index au disque, sort 1 s'il est
              périmé
  --aide      affiche l'aide et sort
  ```

- **bash** `{"command": "grep -n \"rapport-faq\" reports/README.md; sed -n '40,80p' reports/README.md", "description": "Inspect curated reports README"}`

  ```
| [`rapport-coordination-r.md`](rapport-coordination-r.md) | **R** — tagger POS 612 : **0,9475 (+8,49)** |
| [`rapport-tagger-option.md`](rapport-tagger-option.md) | **R0.7 / 1A** — le tagger POS en option : **+8,57** sur 20 phrases, **+9,5** sur 612, défaut hors ligne |
| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |
| [`rapport-atomes-prediction.md`](rapport-atomes-prediction.md) | **Panini B2** — les atomes ne prédisent pas POS/syntagmes/attachement sur 28 œuvres propres ; le style est prédit, la date l'absorbe |
| [`rapport-corpus-commun.md`](rapport-corpus-commun.md) | **Panini** — le corpus commun UDHR |
| [`rapport-retrieval-epoque.md`](rapport-retrieval-epoque.md) | **Panini** — le retrieval contrôlé |
| [`rapport-retrieval-familles.md`](rapport-retrieval-familles.md) | **Panini** — le retrieval approfondi par famille |
| [`rapport-genealogie-deux-faces.md`](rapport-genealogie-deux-faces.md) | **Panini** — la généalogie à deux faces |
| [`rapport-cic-verificateur.md`](rapport-cic-verificateur.md) | **J12.2** — corpus d'or CIC : **42/42** verdicts |
| [`rapport-convention-gv.md`](rapport-convention-gv.md) | GV : F1 **0,7902*
… [3185 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"B13\" docs/pilotage/roadmap.md | head -20", "description": "Locate B13 roadmap rows"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [9317 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,60p' reports/README.md", "description": "Read reports README top"}`

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
… [4645 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,50p' docs/produit/exemples.md", "description": "Inspect examples doc header for TOC style"}`

  ```
# Dix exemples d'analyse, commentés

> **Ce que ce document est.** Dix exécutions **réelles** du produit, avec leur JSON commenté. Il
> complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
> *comment lire* ce qui sort. Les **cinq premiers blocs** ont été produits le **2026-11-06** sur
> la branche `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et
> sans réseau ; ils ont été **rejoués le 2026-11-14** sur le code courant — F1 **0,7902**,
> attachement **238/238 labels** (238/239 cibles), schéma **v2**. Le format v2 ajoute
> `version: 2` et, sur un syntagme qui chevauche un autre, `meta.partition`/`meta.alternative` ;
> v1 reste lue ([schéma v2](../../tools/schemas/drave-annotation-v2.json)).
>
> **Les cinq blocs du 15/11.** Trois exécutions avec `--tagger` (§ 6) et deux avec `--reel`
> (§ 7), produites le **2026-11-15** avec la **clé DeepSeek** et un **cache disque neuf** : le
> coût affiché est donc réel (`réseau=1`, tokens non nuls). Le tagger ne change que le **POS** ;
> les syntagmes, rôles et attachements restent à l'heuristique. La base `--reel` est la **base
> honnête** : 452 phrases réelles (main + corpus),
… [2511 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -i \"toc\\|sommaire\\|table of contents\" tools/docwatch/src/docwatch/*.py tools/docwatch/README.md | head -30", "description": "Check docwatch for auto TOC"}`

  ```
tools/docwatch/src/docwatch/server.py:65:        protocol_version = "HTTP/1.1"
tools/docwatch/src/docwatch/tree.py:188:    reconstruits au fil du parcours, jamais stockés dans les nœuds
tools/docwatch/README.md:31:| **Épingles** | dossiers **et** documents, stockés dans `~/.config/docwatch/pins.json` |
  ```

- **bash** `{"command": "grep -rn \"produit/README\\|docs/produit\" tools/docwatch* tools/*.sh tools/*.py 2>/dev/null | head -20", "description": "Check whether produit doc is rendered"}`

  ```
tools/mesurer_schema_v2_doc.py:115:            "fichier": "docs/produit/README.md",
tools/verifier_faq.py:4:La FAQ de `docs/produit/README.md` (§ 8) ne doit pas être une prose recopiée : chaque
tools/verifier_faq.py:35:FAQ = "docs/produit/README.md#8-faq--dix-questions"
  ```

- **bash** `{"command": "sed -n '1,140p' tools/verifier_faq.py", "description": "Read verifier_faq top"}`

  ```
#!/usr/bin/env python3
"""verifier_faq.py — les dix réponses de la FAQ produit, vérifiées contre le code courant.

La FAQ de `docs/produit/README.md` (§ 8) ne doit pas être une prose recopiée : chaque
réponse est adossée à une commande, à un chiffre de `reports/` ou à une constante du
code. Ce vérificateur exécute les dix contrôles, imprime un JSON (ou un résumé) et sort
avec le code 1 si une réponse ne tient plus.

Ce qu'il ne fait pas : aucune mesure nouvelle, aucun appel réseau, aucune clé lue. Il
rejoue le CLI en local, lit les JSON de résultats déjà publiés et inspecte le source.

Usage :
    python3 tools/verifier_faq.py            # résumé lisible
    python3 tools/verifier_faq.py --json     # le JSON de reports/faq.json

Le **contrôle négatif** est explicite : on vérifie qu'une affirmation fausse (« le CLI
accepte --langue de ») est bien rejetée par le code. Si ce contrôle passait, le
vérificateur ne prouverait rien.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import pathlib
import subprocess
import sys
import tempfile

RACINE = pathlib.Path(__file__).resolve().parent.parent
DRAVE = RACINE / "tools" / "drave.py"
DATE = "2026-11-1
… [4836 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def \\|__main__\\|argparse\\|--json\\|--autotest\" tools/verifier_faq.py | head -60", "description": "List functions in verifier_faq"}`

  ```
14:    python3 tools/verifier_faq.py --json     # le JSON de reports/faq.json
22:import argparse
38:def _run(args: list[str], *, env: dict | None = None, script: pathlib.Path | None = None,
47:def _json(args: list[str], *, env: dict | None = None) -> dict:
48:    r = _run([*args, "--json"], env=env)
54:def _lire(chemin: str):
58:def _sans_cle() -> dict:
69:def q1_langue() -> dict:
95:def q2_hors_ligne() -> dict:
101:def deny(*a, **k):
106:    rc = drave.main(["analyser", "Le chat dort.", "--json"])
129:def q3_cout() -> dict:
156:def q4_tagger() -> dict:
188:def q5_schema() -> dict:
190:    base = json.loads(_run(["--json"], script=RACINE / "tools/verifier_schema_produit.py").stdout)
195:    vingt = json.loads(_run(["--gold", "20", "--json"],
217:def q6_attachement() -> dict:
241:def q7_span_inatteignable() -> dict:
273:def q8_restitution() -> dict:
311:def q9_limites() -> dict:
354:def q10_installation() -> dict:
360:        [sys.executable, "-S", str(DRAVE), "analyser", "Le chat dort.", "--json"],
400:def controle_negatif() -> dict:
405:    base = json.loads(_run(["--json"], script=RACINE / "tools/verifier_schema_produit.py").stdout)
419:def principal() -> dict:
445:def _resume(ra
… [326 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '400,485p' tools/verifier_faq.py", "description": "Read verifier_faq main and negative control"}`

  ```
def controle_negatif() -> dict:
    """Une affirmation fausse doit être rejetée par le code, sinon le vérificateur ment."""
    # Faux : « le CLI accepte --langue de ». Le code doit sortir 2.
    r = _run(["analyser", "Le chat dort.", "--langue", "de"])
    # Faux : « le schéma v2 accepte une annotation v1 ». Le vérificateur doit le refuser.
    base = json.loads(_run(["--json"], script=RACINE / "tools/verifier_schema_produit.py").stdout)
    detecte = (r.returncode == 2
               and base["retrocompatibilite"]["v2_refuse_v1"] is True)
    return {
        "affirmations_fausses": [
            "le CLI accepte --langue de (il sort 2)",
            "le schéma v2 accepte l'annotation v1 (il la refuse)",
        ],
        "observe": {"--langue de": f"code {r.returncode}",
                    "v2_refuse_v1": base["retrocompatibilite"]["v2_refuse_v1"]},
        "detecte": detecte,
    }


def principal() -> dict:
    questions = []
    for ident, question, fonction in CONTROLES:
        try:
            observe = fonction()
            ok = True
            erreur = ""
        except Exception as exc:  # noqa: BLE001 — on veut le rapport, pas la trace
            observe = {}
     
… [2010 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport hashlib, pathlib, re\nt=pathlib.Path('docs/produit/README.md').read_text()\ni=t.index('## 8. FAQ')\nj=t.index('## 9.', i)\ns=t[i:j]\nprint('sha256', hashlib.sha256(s.encode()).hexdigest())\nprint('lignes', s.count('\\n'))\nprint(repr(s[:60]), repr(s[-60:]))\nEO … [51 caractères tronqués]`

  ```
sha256 8855b475faef9079ecadcf9f5426cca62965160403f5542ecc1bc209e6912364
lignes 110
'## 8. FAQ — dix questions\n\n> **Vérifié le 2026-11-15** contr' '`, puis\n`python3 tools/drave.py analyser "Le chat dort."`.\n\n'
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "## 1. À qui s'adresse le produit", "new_string": "## Sommaire\n\n- [1. À qui s'adresse le produit](#1-à-qui-sadresse-le-produit)\n- [2. Ce que le produit fait](#2-ce-que-le-produit-fait)\n- [3. Com … [453 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "| **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |", "new_string": "| **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |\n| **la FAQ du produit** (dix questions vérifiées) | … [139 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "old_string": "| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte avec Drave |", "new_string": "| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte … [140 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport hashlib, pathlib, re\nt=pathlib.Path('docs/produit/README.md').read_text()\ni=t.index('## 8. FAQ'); j=t.index('## 9.', i)\nprint('sha256 §8 apres', hashlib.sha256(t[i:j].encode()).hexdigest())\nprint('mots docs/README', len(re.findall(r'\\S+', pathlib.Path('doc … [96 caractères tronqués]`

  ```
sha256 §8 apres 8855b475faef9079ecadcf9f5426cca62965160403f5542ecc1bc209e6912364
mots docs/README 995
  ```

- **bash** `{"command": "sed -n '20,45p' docs/produit/README.md; echo ===; sed -n '90,105p' docs/README.md; echo ===; sed -n '785,800p' docs/produit/README.md", "description": "Show edited regions"}`

  ```
> [`tools/verifier_faq.py`](../../tools/verifier_faq.py) : **10/10** réponses.
>
> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
> candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.

## Sommaire

- [1. À qui s'adresse le produit](#1-à-qui-sadresse-le-produit)
- [2. Ce que le produit fait](#2-ce-que-le-produit-fait)
- [3. Comment l'utiliser — cinq exemples réels](#3-comment-lutiliser--cinq-exemples-réels)
- [4. Ce que le produit ne fait pas encore](#4-ce-que-le-produit-ne-fait-pas-encore)
- [5. Performance](#5-performance)
- [6. Garanties](#6-garanties)
- [7. Le CLI livré — contrat et manques](#7-le-cli-livré--contrat-et-manques)
- [**8. FAQ — dix questions**](#8-faq--dix-questions)
- [9. Où aller ensuite](#9-où-aller-ensuite)

## 1. À qui s'adresse le produit

| vous êtes… | ce que vous obtenez | ce qu'il faut savoir |
|---|---|---|
| **linguiste, enseignant, curieux** | une analyse immédiate : POS, syntagmes, rôles, attachement, acte de parole | c'est une **annotation**, pas une traduction ni une corre
… [3283 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py", "content": "#!/usr/bin/env python3\n\"\"\"verifier_liens_faq.py — les liens de la FAQ produit et de son sommaire.\n\nTâche **E1** : la FAQ (D3) vit dans `docs/produit/README.md` § 8. Ce vérificateur\ncontrôl … [8941 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/verifier_liens_faq.py; echo \"exit=$?\"; echo ===; python3 tools/verifier_liens_faq.py --autotest; echo \"exit=$?\"", "description": "Run new FAQ link verifier"}`

  ```
Sommaire — 9 ancre(s), 9 morte(s) · FAQ listée : oui
Section § 8 — 5 lien(s), 0 mort(s) · contenu inchangé : oui
docs/README — ligne FAQ : oui · 995/1000 mots
Contrôle négatif : détecté
❌ liens ou sommaire non vérifiés
exit=1
===
✅ autotest : les deux liens faux sont rejetés
exit=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py", "old_string": "#: Le budget de `docs/README.md` (T1, `tools/taille_documents.py`).\nBUDGET_DOCS_README = 1000\nBUDGET_DOCS_README_URL = \"#produit--ce-qui-sutilise-aujourdhui\"", "new_string": "#: Le budget  … [83 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py", "old_string": "def inspecter(texte: str, base: pathlib.Path) -> list[dict]:\n    \"\"\"Inspecte chaque lien du bloc ; rend un dict par lien (ok = fichier + ancre).\"\"\"\n    resultats = []\n    for libelle, … [1459 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py", "old_string": "    liens = inspecter(faux, DOC.parent)\n    morts = [l for l in liens if not l[\"ok\"]]\n    detecte = len(morts) == 2 and all(l[\"ok\"] for l in liens if l not in morts)", "new_string": "    … [178 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py", "old_string": "    liens_sommaire = inspecter(sommaire, DOC.parent)\n    ancres_sommaire = [l for l in liens_sommaire if l[\"ancre\"]]\n    faq_dans_sommaire = any(l[\"ancre\"] == \"8-faq--dix-questions\" fo … [364 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py", "old_string": "    liens_readme = inspecter(f\"[FAQ]({cible_readme})\", README_DOCS.parent)", "new_string": "    liens_readme = inspecter(f\"[FAQ]({cible_readme})\", README_DOCS.parent, readme)"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifier_liens_faq.py; echo \"exit=$?\"; echo ===; python3 tools/verifier_liens_faq.py --json | head -40", "description": "Re-run FAQ link verifier"}`

  ```
Sommaire — 9 ancre(s), 0 morte(s) · FAQ listée : oui
Section § 8 — 5 lien(s), 0 mort(s) · contenu inchangé : oui
docs/README — ligne FAQ : oui · 995/1000 mots
Contrôle négatif : détecté
✅ liens et sommaire vérifiés
exit=0
===
{
 "schema": "drave.faq.sommaire.liens",
 "version": 1,
 "date": "2026-11-15",
 "tache": "E1",
 "document": "docs/produit/README.md",
 "sommaire": {
  "trouve": true,
  "entrees": 9,
  "ancres": 9,
  "mortes": 0,
  "faq_dans_sommaire": true,
  "ligne_faq": "#8-faq--dix-questions",
  "details": [
   {
    "libelle": "1. À qui s'adresse le produit",
    "cible": "#1-à-qui-sadresse-le-produit",
    "fichier": "",
    "fichier_ok": true,
    "ancre": "1-à-qui-sadresse-le-produit",
    "ancre_ok": true,
    "ok": true
   },
   {
    "libelle": "2. Ce que le produit fait",
    "cible": "#2-ce-que-le-produit-fait",
    "fichier": "",
    "fichier_ok": true,
    "ancre": "2-ce-que-le-produit-fait",
    "ancre_ok": true,
    "ok": true
   },
   {
    "libelle": "3. Comment l'utiliser — cinq exemples réels",
    "cible": "#3-comment-lutiliser--cinq-exemples-réels",
    "fichier": "",
    "fichier_ok": true,
    "ancre": "3-comment-lutiliser--cinq-exemples-réels",
    "a
… [30 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifier_liens_faq.py --json", "description": "Show full link verification JSON"}`

  ```
{
 "schema": "drave.faq.sommaire.liens",
 "version": 1,
 "date": "2026-11-15",
 "tache": "E1",
 "document": "docs/produit/README.md",
 "sommaire": {
  "trouve": true,
  "entrees": 9,
  "ancres": 9,
  "mortes": 0,
  "faq_dans_sommaire": true,
  "ligne_faq": "#8-faq--dix-questions",
  "details": [
   {
    "libelle": "1. À qui s'adresse le produit",
    "cible": "#1-à-qui-sadresse-le-produit",
    "fichier": "",
    "fichier_ok": true,
    "ancre": "1-à-qui-sadresse-le-produit",
    "ancre_ok": true,
    "ok": true
   },
   {
    "libelle": "2. Ce que le produit fait",
    "cible": "#2-ce-que-le-produit-fait",
    "fichier": "",
    "fichier_ok": true,
    "ancre": "2-ce-que-le-produit-fait",
    "ancre_ok": true,
    "ok": true
   },
   {
    "libelle": "3. Comment l'utiliser — cinq exemples réels",
    "cible": "#3-comment-lutiliser--cinq-exemples-réels",
    "fichier": "",
    "fichier_ok": true,
    "ancre": "3-comment-lutiliser--cinq-exemples-réels",
    "ancre_ok": true,
    "ok": true
   },
   {
    "libelle": "4. Ce que le produit ne fait pas encore",
    "cible": "#4-ce-que-le-produit-ne-fait-pas-encore",
    "fichier": "",
    "fichier_ok": true,
    "ancre": "4-ce-que-le-p
… [3010 caractères tronqués]
  ```

- **write** `{"content": "# E1 — la FAQ dans le sommaire et les liens : 9 ancres, 5 liens, 0 mort\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **E1** · **Date** : 2026-11-15 ·\n> **Verdict** : ✅ **la FAQ est au sommaire**, ses **5 liens** et les **9 ancres** du\n> sommaire résolvent, **0 lien mort … [7554 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq-sommaire.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/verifier_liens_faq.py --json > reports/faq-sommaire.json && python3 -c \"import json;d=json.load(open('reports/faq-sommaire.json'));print('ok',d['ok'],'| ancres',d['sommaire']['ancres'],'| liens',d['section_8']['liens'],'| morts',d['section_8']['morts'],'| mots',d['docs_re … [64 caractères tronqués]`

  ```
ok True | ancres 9 | liens 5 | morts 0 | mots 995
  ```

- **bash** `{"command": "python3 tools/taille_documents.py | tail -8; echo ===; python3 tools/revue_documentation.py; echo \"revue_exit=$?\"", "description": "Run size and documentation review"}`

  ```
1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3990 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
===
  revue de documentation · 747 fiche(s) · 840 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 746 fichiers, le disque en a 747
     · compteurs : en-cours.md dit 839 JSON, le disque en a 840
revue_exit=1
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Get current time"}`

  ```
2026-11-15 06:30 EST
  ```

- **bash** `{"command": "grep -n \"D3\\*\\* (\\[FAQ\\]\\|fichiers / JSON\" docs/pilotage/en-cours.md", "description": "Locate lines to edit in en-cours"}`

  ```
64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **att. 238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)) ; **D2** ([v2](../../reports/rapport-restitution-v2.md)) ; **D3** ([FAQ](../../reports/rapport-faq.md), 10/10).
90:- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** ([FAQ](../../reports/rapport-faq.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
109:| fichiers / JSON de résultats | **746** / **839** | `reports/*.md` / `reports/*.json` |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 06 h 40 HNE (bilan de la semaine écrit)**", "new_string": "**Mis à jour : 2026-11-15, 06 h 30 HNE (E1 : la FAQ au sommaire et ses liens)**"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**D3** ([FAQ](../../reports/rapport-faq.md), 10/10).", "new_string": "**D3** ([FAQ](../../reports/rapport-faq.md), 10/10) ; **E1** ([sommaire + liens](../../reports/rapport-faq-sommaire.md), 9/9 … [30 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**D1–D3** ([FAQ](../../reports/rapport-faq.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).", "new_string": "**D1–D3** ([FAQ](../../reports/rapport … [162 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **746** / **839** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **747** / **840** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 10}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 60, "limit": 35}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 105, "limit": 8}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 06 h 40 HNE (bilan de la semaine écrit)**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).

(Showing lines 1-10 of 147. Use offset=11 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
60: - **Plan** : B13.
61: - **Stratégie** : v0 mesuré.
62: - **Ambition** : un runtime cognitif tracé.
63: - **Objectif final** : un moteur de pensée v0.
64: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **att. 238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)) ; **D2** ([v2](../../reports/rapport-restitution-v2.md)) ; **D3** ([FAQ](../../reports/rapport-faq.md), 10/10).
65: - **Ce que font les autres** : **N2**, **S**, **hub**.
66: - **Ce qu'elle fait** : chantier.
67: - **Prochaine action** : **qualité des rôles** ; T132/T133, gold 200+.
68: - **Clôture** : **J14.1 faite** (84/81/3 ; `sessions` verte, `indice` et `melange` structurelles ; tag 
… [3455 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
105: | invariant | valeur | contrôle |
106: |---|---|---|
107: | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
108: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
109: | fichiers / JSON de résultats | **746** / **839** | `reports/*.md` / `reports/*.json` |
110: | documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
111: | dernière passe | **14/11 00 h 30** (84, **81/3**) ; rouges tolérées `indice`, `melange` ; `sessions` **revérifiée verte** le 14/11 06 h 55 | `docs/pilotage/references-non-regression.md` |
112: 

(Showing lines 105-112 of 147. Use offset=113 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 06 h 30 HNE (E1 : la FAQ au sommaire et ses liens)**", "old_string": "**Mis à jour : 2026-11-15, 06 h 40 HNE (bilan de la semaine écrit)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**D3** ([FAQ](../../reports/rapport-faq.md), 10/10) ; **E1** ([sommaire + liens](../../reports/rapport-faq-sommaire.md), 9/9 ancres, 5/5 liens, 0 mort).", "old_string": "**D3** ([FAQ](../../repo … [30 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**D1–D3** ([FAQ](../../reports/rapport-faq.md)), **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete. … [162 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **747** / **840** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **746** / **839** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/index_reports.py && python3 tools/revue_documentation.py; echo \"revue_exit=$?\"", "description": "Regenerate reports index and run revue"}`

  ```
744 fiches → reports/INDEX.md
  revue de documentation · 747 fiche(s) · 840 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue_exit=0
  ```

- **bash** `{"command": "ls tools/porte-*.sh | sed 's#tools/##' | tr '\\n' ' '; echo; ls tools/porte-*.sh | wc -l", "description": "List available gates"}`

  ```
porte-adaptateur-sortie.sh porte-audit-drapeaux.sh porte-b1110-hybride.sh porte-balayage.sh porte-bloc-code.sh porte-bloc-linguistique.sh porte-bloc-maths.sh porte-bloc-tableaux.sh porte-budget.sh porte-bus.sh porte-bus-socket.sh porte-c4-retard.sh porte-cerveau.sh porte-cic.sh porte-consolidation.sh porte-coupe.sh porte-cycle-c2.sh porte-deepseek.sh porte-delais.sh porte-diff-couche.sh porte-document.sh porte-echange-experts.sh porte-episodique.sh porte-etat.sh porte-flux.sh porte-fusion.sh porte-gain.sh porte-greffe.sh porte-harnais-invariants.sh porte-homeostasie.sh porte-horloge.sh porte-indice.sh porte-jeux.sh porte-jumeaux.sh porte-lecteur.sh porte-lecture.sh porte-m5-brouillon.sh porte-melange.sh porte-memoire.sh porte-miroir-blocs.sh porte-mistral.sh porte-n3-cache.sh porte-n3-composition.sh porte-n3-deux-processus.sh porte-n3-deux-regions.sh porte-n3-generation.sh porte-n3-inventaire.sh porte-n3-placement.sh porte-n3-pont.sh porte-n3-positions.sh porte-n3-profondeur.sh porte-n3-refus.sh porte-n3-reseau.sh porte-n3-routes.sh porte-n3-service-briques.sh porte-n3-service.sh porte-n3-seuil.sh porte-n3-sparsite-compte.sh porte-n3-sparsite.sh porte-occupation-elagage.sh porte-oc
… [489 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifier_liens_faq.py; echo \"exit=$?\"; python3 tools/taille_documents.py | tail -3", "description": "Re-run link and size checks"}`

  ```
Sommaire — 9 ancre(s), 0 morte(s) · FAQ listée : oui
Section § 8 — 5 lien(s), 0 mort(s) · contenu inchangé : oui
docs/README — ligne FAQ : oui · 995/1000 mots
Contrôle négatif : détecté
✅ liens et sommaire vérifiés
exit=0

  ❌ 1 violation(s) :
     · T0 : 4007 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "ls journal/2026-11-15/ 2>/dev/null; echo ===; sed -n '1,40p' journal/2026-11-15/README.md 2>/dev/null", "description": "Inspect today's journal folder"}`

  ```
distribue.md
docs.md
mesures.md
portes.md
README.md
===
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**17 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 3 | [distribue.md](distribue.md) |
| docs | 4 | [docs.md](docs.md) |
| mesures | 9 | [mesures.md](mesures.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 349.7 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, AT
… [1963 caractères tronqués]
  ```

- **bash** `{"command": "git config core.hooksPath; ls .git/hooks/ | head; echo ===; grep -n \"notes\\|NOTE\" journal/2026-11-15/README.md | head; tail -40 journal/2026-11-15/README.md", "description": "Check hooks and journal notes block"}`

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
===
5:> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
49:<!-- notes -->
85:<!-- /notes -->

## Le récit de la journée (écrit à la main)

<!-- notes -->
### B2 — les atomes ne prédisent pas les niveaux

La table J2.1 promettait un **porteur** pour chacun des 14 atomes ; B2 devait la mesurer. Le résultat est
un **négatif contrôlé**. Sur les **44 signatures** de Panini, **36 œuvres** ont assez de prose pour être
mesurées, **28** ont une fenêtre de signature propre et ≥ 1 000 jetons. Sur ces 28, les 14 atomes ne
prédisent pas **POS** (R²_CV **−0,092**, p=0,56), les **syntagmes** (**−0,160**, p=0,85) ni
l'**attachement** (**−0,092**, p=0,67). Le seul ρ nominal (POS **+0,176**, p=0,029) tombe à **Holm 0,088**
et ne survit pas à la date (**p_resid=1,0**).

Le dispositif n'est pas muet : il prédit l'**entropie des graphèmes** (**+0,811**), la **longueur des
mots** (**+0,657**), la **négation** (**+0,440**) et la **part de verbes** (**+0,429**). Mais la dat
… [1963 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' journal/2026-11-15/docs.md", "description": "Read today's docs journal"}`

  ```
# 2026-11-15 — Documentation, état, conventions

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (4)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 02:00 | `5891ef8a` | ÉTAT — T0 TENU : LA LIGNE FAIT RACCOURCIE | `en-cours.md`, `README.md`, `mesures.md` (+6) |
| 03:51 | `01b6db6e` | JOURNAL — 2026-11-15 : B2, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX (NÉGATIF CONTRÔLÉ ; LE STYLE EST ABSORBÉ PAR LA DATE) | `README.md`, `mesures.md`, `README.md` (+4) |
| 04:30 | `c24253ee` | DOC PRODUIT — LA PASSE D'HONNÊTETÉ : LES TROIS BASES (612, 602, RÉEL 452), L'ATTACHEMENT 238/239, LE TAGGER 95,75, LES CHIFFRES DATÉS ANNOTÉS | `en-cours.md`, `README.md`, `README.md` (+5) |
| 04:48 | `e42bac4f` | JOURNAL — 2026-11-15 : D1, LES EXEMPLES --tagger (441 TOKENS, 3,7 S) ET --reel (452 PHRASES) SONT DANS LA DOC ; 5/5 REJOUÉS, MUTATION 4/5 | `README.md`, `distribue.md`, `docs.md` (+8) |

## Sessions actives ce jour

- `e181ce02-
… [1099 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re,pathlib\nfor f in ['AGENTS.md','docs/pilotage/en-cours.md']:\n    print(f, len(re.findall(r'\\S+',pathlib.Path(f).read_text())))\n# longest task doc\nfor p in pathlib.Path('docs/methode').glob('*.md'):\n    print(p, len(re.findall(r'\\S+',p.read_text())))\nE … [45 caractères tronqués]`

  ```
AGENTS.md 1196
docs/pilotage/en-cours.md 1637
docs/methode/miroir.md 412
docs/methode/panini-nipada.md 262
docs/methode/rangement.md 768
docs/methode/resultats.md 524
docs/methode/relations-humaines.md 1260
docs/methode/modularisation.md 1234
docs/methode/echantillonnage-vdc.md 330
docs/methode/mission.md 744
docs/methode/illustrations.md 666
docs/methode/contexte.md 1089
docs/methode/organisation-du-depot.md 1579
docs/methode/continuite.md 1174
docs/methode/ressources.md 1068
docs/methode/portes.md 692
docs/methode/chantier-autonome.md 886
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": " ; **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)).", "old_string": " ; **E1** ([sommaire + liens](../../reports/rapport-faq-sommaire.md), 9/9 ancres, 5/5 liens, 0 mort)."}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py | grep -E \"T0 max|violation|tous les documents\"; echo \"exit=$?\"", "description": "Recheck context budget"}`

  ```
T0 max : 3999 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
exit=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py >/tmp/revue-e1.txt 2>&1; echo \"revue_exit=$?\"; tail -3 /tmp/revue-e1.txt", "description": "Run revue again"}`

  ```
revue_exit=0
  revue de documentation · 747 fiche(s) · 840 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "sed -n '1,120p' .git/hooks/pre-commit", "description": "Inspect pre-commit hook"}`

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

- **bash** `{"command": "sed -n '1,100p' tools/journal_auto.py", "description": "Inspect journal auto generator"}`

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
… [3768 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md", "offset": 30, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md</path>
<type>file</type>
<content>
30: **238/239** cibles. [`fiche`](../../reports/rapport-exemples-tagger.md).
31: <!-- /notes -->

(End of file - total 31 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md", "new_string": "**238/239** cibles. [`fiche`](../../reports/rapport-exemples-tagger.md).\n\n### E1 — la FAQ entre au sommaire, ses liens sont vérifiés\n\nLa FAQ de `docs/produit/README.md` (§ 8) n'était listée … [890 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md has been updated successfully.
  ```

- **bash** `{"command": "bash tools/porte-document.sh; echo \"document_exit=$?\"", "description": "Run document gate"}`

  ```
=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ===
=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ===
  30 documents · 51 pages · 1484 régions
  types : {'blanc': 1454, 'code': 4, 'figure': 3, 'legende': 1, 'liste': 239, 'note': 120, 'paragraphe': 825, 'section': 230, 'tableau': 30, 'titre': 32}
  deux colonnes : 6 G puis 6 D, 0 retour(s)
  contrôle texte plat : échoue comme attendu
  notes hors corps : 120 région(s), 0 fuite(s)
    data/onu/pdf/A_RES_80_1-en.pdf                         85 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-es.pdf                         93 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-fr.pdf                         91 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-ru.pdf                         95 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-zh.pdf                         83 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_10-en.pdf                       155 régions  fidélité 1.000
    … et 24 autres

✅ les 50 pages sont découpées, les partitions exactes, le rejeu identique,
   la fidélité ≥ 0,99 et les trois contrôles négatifs se comportent comme prévu.
✅ porte document verte
document_exit=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh; echo \"tableaux_exit=$?\"", "description": "Run table gate"}`

  ```
✅ 1819 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4456 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
tableaux_exit=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py; echo \"en_cours_exit=$?\"; python3 tools/verifie_journal.py; echo \"journal_exit=$?\"", "description": "Run state and journal checks"}`

  ```
en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
en_cours_exit=0
  journal · 47 jour(s) · 203 session(s) · 2581 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
journal_exit=0
  ```

- **bash** `{"command": "git status --short", "description": "Show working tree status"}`

  ```
M docs/README.md
 M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M journal/2026-11-15/docs.md
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
?? reports/faq-sommaire.json
?? reports/rapport-faq-sommaire.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
?? tools/verifier_liens_faq.py
  ```

- **bash** `{"command": "git diff -- docs/produit/README.md docs/README.md docs/pilotage/en-cours.md reports/INDEX.md journal/2026-11-15/docs.md | sed -n '1,220p'", "description": "Review tracked-file diffs"}`

  ```
diff --git a/docs/README.md b/docs/README.md
index 114337f6..81e94db9 100644
--- a/docs/README.md
+++ b/docs/README.md
@@ -94,6 +94,7 @@
 | document | pour quoi |
 |---|---|
 | [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte avec Drave |
+| [`produit/README.md` § 8](produit/README.md#8-faq--dix-questions) | la **FAQ** : dix questions vérifiées contre le code |
 | [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels (entrée → sortie), dont un cas d'échec connu |
 
 ## Transversal et archive
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 3fc61bfa..9189bf57 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 06 h 40 HNE (bilan de la semaine écrit)**
+**Mis à jour : 2026-11-15, 06 h 30 HNE (E1 : la FAQ au sommaire et ses liens)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -61,7 +61,7 @@
 - **Stratégie** : v0 mesuré.
 - **Ambition** : un runtime cognitif tracé.
 - **Objectif final** : un moteur de pensée v0.
-- **Fait** : B13 **183/183** ;
… [9119 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' tools/verifie_etat_a_jour.py", "description": "Inspect state freshness checker"}`

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

- **bash** `{"command": "git diff -- tools/chantier/plan.json | head -40", "description": "Check plan.json modifications"}`

  ```
diff --git a/tools/chantier/plan.json b/tools/chantier/plan.json
index af52ed5c..d81b3cbb 100644
--- a/tools/chantier/plan.json
+++ b/tools/chantier/plan.json
@@ -539,6 +539,40 @@
      "attendu": "FICHE-OK"
     }
    ]
+  },
+  {
+   "id": "E1",
+   "jour": 15,
+   "titre": "La FAQ dans le sommaire et les liens",
+   "mandat": "Tâche E1 : la FAQ (D3) est dans `docs/produit/README.md` — ajoute-la au sommaire du document, vérifie les **liens** de la section (aucun lien mort), et mets la ligne FAQ dans `docs/README.md` si elle n'y est pas. Fiche `reports/rapport-faq-sommaire.md` + JSON, commit. Ne change pas le contenu des réponses.",
+   "budget_min": 90,
+   "acceptation": [
+    {
+     "commande": "test -f reports/rapport-faq-sommaire.md && echo FICHE-OK",
+     "attendu": "FICHE-OK"
+    },
+    {
+     "commande": "python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?",
+     "attendu": "REVUE-0"
+    }
+   ]
+  },
+  {
+   "id": "E2",
+   "jour": 15,
+   "titre": "Le tagger — les cas d'erreur",
+   "mandat": "Tâche E2 : les cas d'erreur de `--tagger` — la clé absente (code 4), la clé invalide (code 4, message clair), le réseau coupé (code 4 ou repli heuristique 
… [526 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py", "new_string": "import argparse\nimport hashlib\nimport json\nimport pathlib\nimport re", "old_string": "import argparse\nimport hashlib\nimport json\nimport pathlib\nimport re\nimport sys"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_liens_faq.py has been updated successfully.
  ```

- **bash** `{"command": "python3 -m py_compile tools/verifier_liens_faq.py && echo COMPILE-OK; python3 tools/verifier_liens_faq.py --autotest; python3 tools/verifier_liens_faq.py --json > reports/faq-sommaire.json; python3 -c \"import json; d=json.load(open('reports/faq-sommaire.json')); print('JSON-OK', d['ok' … [59 caractères tronqués]`

  ```
COMPILE-OK
✅ autotest : les deux liens faux sont rejetés
JSON-OK True
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq-sommaire.md", "new_string": "Les **dix réponses** de § 8 ne sont pas touchées : la fiche ne réécrit aucun chiffre, aucun\nargument, aucune commande. Aucune ligne de § 8 n'apparaît dans le diff ; l'empreinte le\nconfir … [219 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq-sommaire.md has been updated successfully.
  ```

- **bash** `{"command": "test -f reports/rapport-faq-sommaire.md && echo FICHE-OK; python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?; bash tools/porte-tableaux.sh | tail -1", "description": "Run E1 acceptance checks"}`

  ```
FICHE-OK
REVUE-0
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "git add docs/produit/README.md docs/README.md docs/pilotage/en-cours.md reports/rapport-faq-sommaire.md reports/faq-sommaire.json reports/INDEX.md tools/verifier_liens_faq.py journal/2026-11-15/docs.md && git status --short", "description": "Stage E1 files explicitly"}`

  ```
M  docs/README.md
M  docs/pilotage/en-cours.md
M  docs/produit/README.md
M  journal/2026-11-15/docs.md
M  reports/INDEX.md
A  reports/faq-sommaire.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
A  reports/rapport-faq-sommaire.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
A  tools/verifier_liens_faq.py
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "git commit -m \"E1 — LA FAQ AU SOMMAIRE ET SES LIENS : 9/9 ANCRES, 5/5 LIENS, 0 MORT ; LA LIGNE FAQ DANS docs/README, LES RÉPONSES INCHANGÉES\" 2>&1 | tail -40", "description": "Commit E1 changes", "timeoutMs": 300000}`
