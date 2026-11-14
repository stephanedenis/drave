# Session DSH — relecture

- identifiant : `session-4271ad32-61f1-46a0-8494-7c94c3f8050f`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 06:23:04
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J13.1 : la table des mesures du chantier — POS, F1, attachement, couverture, spans, le produit, Panini — avant/après, avec la base (612/602), les commits et les contrôles négatifs ; fiche `reports/rapport-tableau-mesures.md` + JSON.

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

- **bash** `{"command": "pwd && ls -la | head -50 && git log --oneline -10", "description": "List working directory and recent commits"}`

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
drwxr-xr-x. 1 stephane stephane   180 14 nov 06:23 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   972 14 nov 00:51 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 76026 14 nov 05:51 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [2564 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"J13.1\\|J13\\.1\\|tableau-mesures\\|table des mesures\" --include=*.md --include=*.json --include=*.py . | head -50", "description": "Search for task J13.1 references"}`

  ```
./reports/rapport-bilan-chantier.json:1110:   "tache": "J13.1",
./reports/rapport-bilan-chantier.json:1111:   "objet": "la table des mesures du chantier"
./reports/rapport-bilan-chantier.md:350:vérificateur CIC ; **J13.1** publie la table des mesures ; **J14.1** clôt par la passe et le tag
./reports/rapport-panini-334.md:380:  (le vérificateur indépendant du corpus d'or CIC, 42 verdicts), puis **J13.1** (la table des mesures).
./reports/rapport-cic-verificateur.md:243:La prochaine action de la ligne Panini est **J13.1** (la table des mesures), puis **J14.1**
./tools/chantier/plan.json:397:   "id": "J13.1",
./tools/chantier/plan.json:399:   "titre": "Les bilans — la table des mesures",
./tools/chantier/plan.json:400:   "mandat": "Tâche J13.1 : la table des mesures du chantier — POS, F1, attachement, couverture, spans, le produit, Panini — avant/après, avec la base (612/602), les commits et les contrôles négatifs ; fiche `reports/rapport-tableau-mesures.md` + JSON.",
./tools/chantier/plan.json:404:     "commande": "test -f reports/rapport-tableau-mesures.md && echo FICHE-OK",
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:61638:  [a_faire ] J13.1  j13 — Les bilans 
… [3112 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if t['id'] in ('J10.1','J11.1','J11.2','J11.3','J11.4','J12.1','J12.2','J13.1','J14.1'):\n        print('='*70)\n        print(json.dumps(t, ensure_ascii=False, indent=1))\nEOF", "d … [48 caractères tronqués]`

  ```
======================================================================
{
 "id": "J10.1",
 "jour": 10,
 "titre": "Le bilan de la semaine",
 "mandat": "Tâche J10.1 : le bilan — relis les fiches du chantier, écris `reports/rapport-bilan-chantier.md` + JSON : les chiffres avant/après (POS, F1, attachement, le produit, Panini), les décisions, les rejets, les échecs (J1.2/J2.2/J3.1 : timeout après commit), ce qui reste pour la suite. Mets à jour `docs/pilotage/semaine-autonome.md`.",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-bilan-chantier.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  }
 ]
}
======================================================================
{
 "id": "J11.1",
 "jour": 11,
 "titre": "Le produit — les exemples rejoués",
 "mandat": "Tâche J11.1 : les exemples de la doc produit — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (F1 0,7902, 237/238, le schéma v2) et corrige les sorties qui ont bougé ; fiche `reports/rapport-exemples-rejoues.md` + JSON, commit.",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-exemples-rejoues.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  },
 
… [4388 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' docs/pilotage/en-cours.md", "description": "Read current state document"}`

  ```
# En ce moment

**Mis à jour : 2026-11-14, 06 h 15 HNE (heure locale, EST).**

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
… [11274 caractères tronqués]
  ```

- **bash** `{"command": "wc -l reports/rapport-bilan-chantier.md reports/rapport-bilan-chantier.json && sed -n '1,180p' reports/rapport-bilan-chantier.md", "description": "Read previous bilan report"}`

  ```
432 reports/rapport-bilan-chantier.md
 1347 reports/rapport-bilan-chantier.json
 1779 total
# J10.1 — le bilan du chantier : F1 0,7533 → 0,7902, attachement 236 → 238, Panini mesuré et borné

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (le moteur de pensée), **R0.7** (le bloc langue), **N2**, **S**,
> **R**, **A**, **Panini** · **Tâche** : J10.1 · **Date** : 2026-11-14 · **Verdict** : ✅
>
> **Ce que ce rapport est.** La **relecture consolidée** des fiches du chantier, de J1.1 à J9.1 :
> les chiffres avant/après, les décisions, les rejets, les échecs de la boucle et ce qui reste.
> **Aucune mesure nouvelle** : chaque chiffre est celui de sa fiche, avec sa base, son contrôle
> négatif et sa limite. Le bilan **ne remplace pas** les fiches ; il les ordonne.
>
> **Base.** HEAD `81fc9ecf` (J9.1) ; gold vivant **612 phrases / 239 cibles / 3 179 jetons** ;
> gold gelé **602** ; POS heuristique **0,8625** ; F1 **0,7533** au départ du chantier ;
> **21 
… [14378 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' reports/rapport-bilan-chantier.json", "description": "Read previous bilan JSON head"}`

  ```
{
 "schema": "drave.bilan-chantier",
 "version": 1,
 "titre": "J10.1 — le bilan du chantier : F1 0,7533 → 0,7902, attachement 236 → 238, Panini mesuré et borné",
 "date": "2026-11-14",
 "tache": "J10.1",
 "lignes_roadmap": [
  "B13",
  "R0.7",
  "N2",
  "S",
  "R",
  "A",
  "Panini"
 ],
 "statut": "bilan",
 "head": "81fc9ecf",
 "base": {
  "gold_vivant": {
   "phrases": 612,
   "cibles": 239,
   "jetons": 3179,
   "pos": 0.8625,
   "f1_depart": 0.7533
  },
  "gold_gele": {
   "phrases": 602,
   "cibles": 239,
   "f1": 0.7882,
   "attachement": "234/239"
  },
  "lancements": 21,
  "timeouts": 5,
  "echecs_acceptation": 1,
  "budget_s": 22032.2,
  "note": "Aucune mesure nouvelle : ce bilan relit les fiches du chantier, de J1.1 à J9.1."
 },
 "chiffres": {
  "produit": {
   "pos": {
    "avant": 0.8625,
    "apres": 0.8625,
    "delta": 0.0,
    "jetons": 3179,
    "jetons_changes": 0,
    "lecture": "J1.1, J1.2, J6.1 et J6.2 sont des règles de syntagmes ou d'attachement ; la POS ne bouge pas.",
    "fiches": [
     "reports/rapport-r035.md",
     "reports/rapport-s065.md"
    ]
   },
   "f1": {
    "avant": {
     "all": 0.7533,
     "dev": 0.7476,
     "test": 0.7663,
     "lineaire"
… [3277 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '180,432p' reports/rapport-bilan-chantier.md", "description": "Read rest of previous bilan"}`

  ```
11 acceptés / 0 candidat sans verdict** ; un clone à `523d8c1` voit **8 / 4 / 11**. Les 11
lignes portent **16 mappings uniques** ; **7/16** sont justes, **9/16** faux ou restés aux
défauts de la page. L'option **A** (committer tel quel, puis corriger) est recommandée.

**R.** Voir § 2.3. Les cinq modes neuronaux rendent la **même** exactitude : la fusion est
**neutre** sur ce gold. L'hybride « fermé heuristique / ouvert modèle » gagne **+0,41 pt** mais
McNemar **31/44, p = 0,17** : non significatif, piste et non décision.

**A.** Le MoE `qwen3-30b-a3b-Q4_K_M` existe : **18 556 686 752 o = 17,28 GiB**, **48 couches**,
**128 experts**, **8 utilisés** par jeton. `--ppl` rend **37,2013** ; la porte
`porte-echange-experts` rend **54,5202** à N = 16 avec **768** décisions de routage et un routage
étranger à **36 074,9497**. Le blocage est la **résidence mono-GPU** (17,28 > 16 GiB) et le cache
VRAM câblé pour **MXFP4** seulement, pas pour le **Q4_K**. A8.3b2 est **libre** mais **hors du
graphe** ; le compte des pins A8 reste à trancher : **18** ou **19**.

### 2.6 Les portes et la clôture

| élément | valeur | lecture |
|---|---|---|
| passe complète | **84 portes, 81 vertes, 3 rouges** 
… [20580 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/methode/resultats.md", "description": "Read results method doc"}`

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

- **bash** `{"command": "git log --oneline --decorate -80 | sed -n '1,80p'", "description": "List recent commits with tasks"}`

  ```
b20a4c31 (HEAD -> s/v7) J12.2 — LE CORPUS D'OR CIC EST REJOUÉ HORS DE PANINI : 42/42 VERDICTS, 42/42 EMPREINTES, 36/36 PREUVES ALTÉRÉES REJETÉES (1 020/1 020 MUTATIONS DE eq(2,2)) ; NOYAU DRAVE INDÉPENDANT, CORPUS PORTABLE
bb68b820 (origin/s/v7, origin/master, origin/HEAD, master) J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0089 APRÈS TOPO (p=0,86) ; FILIATION 61,4 % vs 50,0 % (HOLM 0,128), ÉPOQUE 56,8 % vs 53,8 % (p=0,373), ANNÉE INTRA-TRADITION R²=0,042 (HOLM 0,034) ; V150 β DATE −0,006 ≠ +0,138
febfdfff J11.4 — SCHÉMA v2 DOCUMENTÉ : 4 CHAMPS PARTITION + 10 CHAMPS ALTERNATIVE, 6 CAS / 0 ÉCHEC, LES DEUX VERSIONS LUES (612 v2 + 612 v1)
55bde5c5 J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 SCHÉMA V2, 115 CHEVAUCHEMENTS ALTERNATIVE / 0 FILTRER ; RESTITUTION 46/46, STRICT 0,1087 (F1 0,7902)
09e54143 J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ
84e393bb J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238
a6808c5e CHANTIER — LE PLAN EST RE
… [8571 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | sed -n '1,120p'", "description": "List report names"}`

  ```
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
a83b-lot.json
a83b-regimes.json
a83c-ctx.json
a83c-lot.json
a83-defaut.json
a83d-lot-threads.json
aiguille-30b.md
aiguille-gpt-oss.md
alignement-3b.json
alignement-7b.json
alignement-verne.md
analyse-litteraire.json
archive
atomes-niveaux.json
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeur-mots.json
b10-mots-contraste.json
b10-mots-jw.json
b1110-audit.json
b1110b-hybride.json
b1110-cartes.json
b1110c-case.json
b13-porte-134.json
b13-porte-138.json
b13-porte-140.json
bilan-b11.md
bilan-multi-materiel.md
bloc-linguistique.json
… [1580 caractères tronqués]
  ```

- **bash** `{"command": "wc -l reports/rapport-exemples-rejoues.md reports/rapport-evaluer-langue.md reports/rapport-robustesse-semaine.md reports/rapport-schema-v2-doc.md reports/rapport-panini-334.md reports/rapport-cic-verificateur.md; echo ---; for f in rapport-exemples-rejoues rapport-evaluer-langue rappor … [302 caractères tronqués]`

  ```
171 reports/rapport-exemples-rejoues.md
  108 reports/rapport-evaluer-langue.md
  238 reports/rapport-robustesse-semaine.md
  190 reports/rapport-schema-v2-doc.md
  384 reports/rapport-panini-334.md
  244 reports/rapport-cic-verificateur.md
 1335 total
---
== rapport-exemples-rejoues.json
{
 "tache": "J11.1",
 "titre": "Les cinq exemples de la doc produit rejoués",
 "date": "2026-11-14",
 "head": "a6808c5edf741ea59d45602fdfeee0916488beaf",
 "code": {
  "cli": "drave 0.1.0",
  "schema": 2,
  "commande": "python3 tools/drave.py"
 },
 "gold": {
  "nom": "vivant (hand + reel + synthétique)",
  "gele": false,
  "phrases": 612,
  "tokens": 3179,
  "cibles_attachement": 239
 },
 "mesure": {
  "pos": {
   "exactitude": 0.8625,
   "ferme": 0.9373,
   "ouvert": 0.7918,
   "tokens": 3179
  },
  "syntagmes": {
   "f1": 0.7902,
   "precision": 0.786,
   "rappel": 0.7944,
   "tp": 1480,
   "fp": 403,
   "fn": 383,
   "tete_f1": 0.9029
  },
  "attachement": {
   "labels": 238,
   "cibles": 239,
   "exact": 238,
   "exact_taux": 0.9958,
   "couverture": 0.9958,
   "par_langue": {
    "fr": {
     "cibles": 151,
     "labels": 151,
     "exact": 151,
     "topk": 149,
     "exact_taux_span": 1.0
  
… [3673 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -Ei \"exemple|langue|robust|schema|334|cic\" ", "description": "Find related JSON names"}`

  ```
carte-24langues-3b.json
carte-24langues.json
cic-verificateur.json
evaluer-langue.json
jeux-langues-mesures.json
panini-334.json
pensee-par-langue.json
pensee-robustesse-produit.json
pensee-robustesse-semaine.json
pensee-schema-v1.json
pensee-schema-v2.json
rapport-c8-inter-langue.md
rapport-cic-verificateur.md
rapport-evaluer-langue.md
rapport-exemples-rejoues.json
rapport-exemples-rejoues.md
rapport-langues-maitres.md
rapport-panini-334.md
rapport-pensee-par-langue.md
rapport-robustesse-produit.md
rapport-robustesse-semaine.md
rapport-schema-v1.md
rapport-schema-v2-doc.md
rapport-schema-v2.md
schema-v2-doc.json
toutes-langues
toutes-langues.md
traduction-24langues-3b-A.json
traduction-24langues-3b-B.json
traduction-24langues-A.json
traduction-24langues-B.json
traduction-langues-3b.json
traduction-langues-7b.json
  ```

- **bash** `{"command": "git show --stat --oneline 84e393bb 09e54143 55bde5c5 febfdfff bb68b820 b20a4c31 | sed -n '1,200p'", "description": "Show files changed in J11/J12 commits"}`

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
09e54143 J11.
… [7980 caractères tronqués]
  ```

- **bash** `{"command": "for f in evaluer-langue pensee-robustesse-semaine schema-v2-doc panini-334 cic-verificateur; do echo \"===== $f\"; python3 - <<EOF\nimport json\nd=json.load(open('reports/$f.json'))\ndef walk(o,p='',depth=0):\n    if depth>2: return\n    if isinstance(o,dict):\n        for k,v in o.item … [546 caractères tronqués]`

  ```
===== evaluer-langue
date: 2026-11-14
tache: J11.2
ligne: B13
commande: python3 tools/drave.py evaluer --par-langue --json
gold dict 5
  nom: vivant (hand + reel + synthétique)
  gele: False
  phrases: 612
  tokens: 3179
  cibles_attachement: 239
global dict 12
  phrases: 612
  tokens: 3179
  pos dict 3
    exactitude: 0.8625
    exactitude_ferme: 0.9373
    exactitude_ouvert: 0.7918
  syntagme dict 6
    precision: 0.786
    rappel: 0.7944
    f1: 0.7902
    tp: 1480
    fp: 403
    fn: 383
  tete dict 3
    precision: 0.9261
    rappel: 0.8808
    f1: 0.9029
  attachement dict 8
    cibles: 239
    labels: 238
    exact: 238
    couverture: 0.9958
    exact_taux: 0.9958
    exact_taux_span: 1.0
    topk: 236
    topk_taux: 0.9874
  pragmatique dict 4
    acte: 0.9967
    negation: 0.9771
    modalite: 0.9886
    double_sens: 0.9444
  fraction_semantique: 0.5476
  controle_negatif dict 4
    nom: cible exacte tirée au hasard dans le gold
    graine: 0
    cibles: 239
    exact_taux: 0.0167
  syntagmes_lineaire dict 7
    precision: 0.8539
    rappel: 0.7783
    f1: 0.8144
    tp: 1450
    fp: 248
    fn: 413
    tete dict 6
  attachement_lineaire dict 3
    exact: 224
    labels: 
… [20822 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,110p' reports/rapport-evaluer-langue.md", "description": "Read J11.2 report"}`

  ```
# J11.2 — la mesure par langue : l'anglais devant, mais le gold n'est pas le même

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Tâche** : **J11.2** ·
> **Date** : 2026-11-14 · **Verdict** : ✅
> **Le chiffre.** `evaluer --par-langue` scinde la mesure du gold vivant 612 en **fr** et **en**
> sans changer le global (F1 **0,7902**, POS **0,8625**, attachement **238/239**). Le français
> fait **402 phrases / 2 031 tokens / 151 cibles** (POS **0,8159**, F1 **0,7475**, attachement
> **151/151**) ; l'anglais **210 phrases / 1 148 tokens / 88 cibles** (POS **0,9451**, F1
> **0,8656**, attachement **87/88**). L'anglais est devant, mais les deux golds **n'ont pas la
> même composition** : l'anglais est **100 % réel**, le français ajoute **160 synthétiques**.
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) (`evaluer --par-langue`, 0.1.0),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`test_produit.py`](../tools/tests/test_produit.py) (18 tests) ; gold vivant 612 phrases.
> **JSON** : [`evaluer-langue.json`](evaluer-langue.json).

## 1. Le détail fr/en

Le drapeau rejoue `evaluer_bloc` sur chaque sous-gold, avec le **même** bloc heuristique.
… [5510 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,130p' reports/rapport-robustesse-semaine.md", "description": "Read J11.3 report"}`

  ```
# J11.3 — les 50 textes libres : 0 plantage, 50/50 au schéma v2, 115 chevauchements en `alternative`, 0 en `filtrer`

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **J11.3** · **Date** : 2026-11-14 ·
> **Verdict** : ✅
>
> **Commit mesuré** : `09e54143` — **F1 0,7902**, **POS 0,8625**, **attachement 238/238
> labels** (238/239 cibles, 0,9958), **schéma v2**, **restitution v1**.
>
> **Ce que le produit fait sur les 50 textes de l'audit A26**, rejoués avec le code de la
> semaine : **0 plantage**, **50/50 JSON valide**, **50/50 portent les 8 champs** obligatoires
> et passent le schéma v2 ; **4 refus** sont des réponses JSON (code 3) ; en vue
> **`alternative`**, **395 segments** et **115 chevauchements** dans **21/46** textes
> annotés ; en vue **`filtrer`**, **313 segments** et **0 chevauchement** ; **46/46 formes
> canoniques** en restitution, le miroir strict reste **5/46 = 0,1087** ; temps CLI médian
> **159,2 ms**, API **2,7 ms**.
>
> **Dispositif** : [`tools/mesurer_robustesse_semaine.py`](../tools/mesurer_robustesse_semaine.py),
> banc [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json) (audit A26),
> schéma [`drave-annotation-v2.json`](../tools/schemas
… [6284 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-exemples-rejoues.md; echo '--- J11.4'; sed -n '1,100p' reports/rapport-schema-v2-doc.md", "description": "Read J11.1/J11.4 report heads"}`

  ```
# J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : **J11.1** · **Date** : 2026-11-14 ·
> **Verdict** : ✅
> **Cinq blocs rejoués** avec le code courant, **4 corrigés**, **1 identique** : la ponctuation
> finale entre dans le POS (`g001`, `r241`), le refus sort en **3**, et **`r035` est désormais
> prédit** — span `REL [9:24] « she talks about »` et cible `film`, exactement le gold.
> **Le chiffre.** F1 syntagmes **0,7902** ; POS **0,8625** (fermé 0,9373, ouvert 0,7918) ;
> attachement **238/238 labels** (238/239 cibles, **0,9958**). Le mandat porte encore **237/238** :
> c'est l'état d'avant `s065` (J6.2), qui a ajouté un label **sans toucher un span** — F1 inchangé.
> **Dispositif** : [`docs/produit/exemples.md`](../docs/produit/exemples.md) (les 5 blocs),
> [`tools/drave.py`](../tools/drave.py) 0.1.0, [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> `jq` ; mesure par `python3 tools/drave.py evaluer --json` sur le gold vivant (612 phrases).
> **JSON** : [`rapport-exemples-rejoues.json`](rapport-exemples-rejoues.json).

## 1. Le verdict du rejeu

Les cinq commandes de 
… [8777 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,130p' reports/rapport-panini-334.md", "description": "Read J12.1 report head"}`

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
… [8472 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"^##\\|^###\" reports/rapport-panini-334.md; echo ---; sed -n '160,290p' reports/rapport-panini-334.md", "description": "Read J12.1 results sections"}`

  ```
39:## 1. La question
61:## 2. Le matériau et son audit — 114, 655, 102, 48, 44
88:## 3. Le protocole
90:### 3.1 Niveau paire — la loi H0, l'époque, la filiation
105:### 3.2 Niveau œuvre — retrieval et prédiction
129:### 3.3 Les tests principaux et la correction
137:## 4. Résultats au niveau paire — la filiation porte, l'époque n'ajoute rien
139:### 4.1 La H0 se reproduit, et elle est robuste à la dé-duplication
156:### 4.2 Le plan est colinéaire — et c'est le résultat principal
169:### 4.3 À date fixe, la filiation survit — mais la surface la retire
183:### 4.4 La tradition seule, et ce qu'elle devient après la topologie
192:## 5. Résultats au niveau œuvre — le retrieval brut, et ce que les contrôles en gardent
194:### 5.1 Le top-1 brut
206:### 5.2 Date contrôlée vs filiation contrôlée
223:### 5.3 Prédiction — l'année brute, la tradition, et le résidu
241:### 5.4 Surface — `eng–eng`, et les doublons
254:## 6. La tentative de reproduction de la v150 — le β époque n'est pas là
280:## 7. Ce que cela dit de l'avertissement de Panini
309:## 8. Ce qui pourrait rendre ce résultat faux
345:## 9. Fichiers et reproduction
370:## 10. Verdict et suite
---
| **même tradition large** | 180 | **2
… [8830 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"^##\\|^###\" reports/rapport-cic-verificateur.md; echo ---; sed -n '1,120p' reports/rapport-cic-verificateur.md", "description": "Read J12.2 report"}`

  ```
20:## 1. La question
36:## 2. Le dispositif
38:### 2.1 L'artefact, sa provenance et sa copie portable
56:### 2.2 Le vérificateur indépendant
86:### 2.3 Les commandes
100:## 3. Les résultats
102:### 3.1 42/42 verdicts
122:### 3.2 Les six rejets, et pourquoi ils sont rejetés
140:### 3.3 Le contrôle négatif — altérer un octet
180:### 3.4 La porte et les tests
200:## 4. Ce qui pourrait rendre ce résultat faux
230:## 5. Ce que la fiche fixe
---
# J12.2 — Le corpus d'or CIC : 42/42 verdicts rejoués par un vérificateur indépendant

> **Ligne de roadmap** : **L / R0.7** (le bloc langue) — chantier **Panini** · **Tâche** : **J12.2** ·
> **Date** : **2026-11-14** ·
> **Verdict** : ✅ **le corpus d'or CIC est portable et rejouable hors de Panini** — un noyau
> CIC-lite réécrit côté Drave, sans importer le code de Panini, rend **42/42** verdicts
> (**36** acceptés, **6** rejetés), **42/42** empreintes `sha256(preuve || type)` et **42/42**
> sérialisations canoniques. Le contrôle négatif tient : altérer le dernier octet des **36**
> preuves acceptées les fait **36/36** rejeter, et les **1 020** mutations d'un octet de
> `eq(2,2)` sont **1 020/1 020** rejetées. Un noyau « accepte tout » et un noy
… [5669 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"602\" reports/rapport-*.md docs/pilotage/*.md | grep -Ei \"gel|F1|attachement|234|0,78\" | head -40", "description": "Find frozen gold 602 values"}`

  ```
reports/rapport-audit-attachement.md:157:- **Gold vivant** : 612 phrases ; `gold_gele` (602) n'est pas utilisé ici. Le chiffre « gold
reports/rapport-audit-r1r3.md:22:- **Gold gelé** : `evaluer_gold.charger_gele()` — 602 phrases, mêmes 239 cibles ; les 10
reports/rapport-audit-r1r3.md:54:| grandeur | fiche / JSON | vivant 612 | gelé 602 | écart |
reports/rapport-audit-r1r3.md:72:sont donnés par la fiche sur le **gelé 602** ; sur le vivant 612 ils valent respectivement
reports/rapport-audit-r1r3.md:73:0,5720 / 0,4910 / 0,6018 / 0,7262. La fiche indique « gelé 602 » sur la ligne F1 ; elle ne
reports/rapport-audit-r1r3.md:79:| grandeur | fiche / JSON | mesuré vivant 612 | mesuré gelé 602 | écart |
reports/rapport-audit-r1r3.md:403:12. **Mineure — bases de mesure** : `F1` et `tête` ne sont pas annoncés comme « gelé 602 »
reports/rapport-audit-v10.md:10:rejouent presque toutes : **220/220**, couverture **0,9205**, **F1 0,5880** (gelé 602),
reports/rapport-audit-v10.md:19:listée). Enfin, le F1 « avant » **0,5822** est la valeur du **vivant 612** ; le **gelé 602**
reports/rapport-audit-v10.md:27:- **Gold gelé** : `evaluer_gold.charger_gele()` — **602** phrases, mêmes **239** cibles ;
repo
… [3341 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"0,7882\\|0.7882\\|234/239\\|234 / 239\" reports/*.md reports/*.json | head -30", "description": "Find frozen gold metrics"}`

  ```
reports/rapport-bilan-chantier.md:360:   (F1 0,7882 ; 234/239).
reports/rapport-passe-honnetete.md:19:> **0,7882**, attachement **234 labels sur 239 cibles**. La commande est en § 4.
reports/rapport-passe-honnetete.md:34:| F1 syntagmes (gelé 602) | — | **0,7882** | — |
reports/rapport-passe-honnetete.md:132:| **gelé** | 602 | **0,8625** | **0,7882** | 0,9025 | **234 / 239** | 0,9791 | 1,0 |
reports/rapport-passe-honnetete.md:147:  (0,7902 / 0,7882 ; 238/239 / 234/239). Une fiche qui ne nomme pas sa base peut tromper même
reports/m7-frequence.json:2699:    "ecart_type": 0.03764506788226314,
reports/m7-frequence.json:6285:    "ecart_type": 0.03764506788226314,
reports/m7-frequence.json:6397:    "ecart_type": 0.03764506788226314,
reports/m7-frequence.json:7181:    "ecart_type": 0.03764506788226314,
reports/m7-frequence.json:7853:    "ecart_type": 0.03764506788226314,
reports/m7-frequence.json:8525:    "ecart_type": 0.03764506788226314,
reports/passe-honnetete.json:39:   "f1_syntagmes": 0.7882,
reports/passe-honnetete.json:400:  "La base change les chiffres : vivant 612 (F1 0,7902 ; 238/239) vs gelé 602 (F1 0,7882 ; 234/239).",
reports/rapport-bilan-chantier.json:29:   "f1": 0.7882,
re
… [363 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '100,150p' reports/rapport-passe-honnetete.md; echo ---; sed -n '1,90p' reports/rapport-passe-honnetete.md", "description": "Read base table in honesty pass report"}`

  ```
**Contrôle positif — les 19 encarts.** `19/19` fiches portent exactement le bloc en ligne 3 ;
`19/19` contiennent les deux liens ; `38/38` cibles résolvent (`../docs/pilotage/en-cours.md` et
`../docs/pilotage/roadmap.md` existent). Aucun encart ne contient encore
`F1 0,7535, attachement 236/237` : l'ancien texte a bien disparu.

**Contrôle négatif 1 — la fiche courante n'est pas annotée.** [`rapport-s065.md`](rapport-s065.md)
publie **238/238** et **0 POS changée** : elle ne porte pas l'encart et ne doit pas le porter.
C'est la frontière entre « historique » et « courant ».

**Contrôle négatif 2 — les faux positifs du scan.** Le motif `2 spans` attrape deux fiches qui
parlent d'une **autre unité** : [`rapport-frontieres-phrase.md`](rapport-frontieres-phrase.md)
(« 2 spans **de phrase** du gold corrigés ») et
[`rapport-gold-anglais.md`](rapport-gold-anglais.md) (« 2 spans exacts » du gold anglais). Elles
ne sont **pas** annotées : leur `2 spans` n'est pas l'attachement. Les index
(`reports/README.md`, `reports/INDEX.md`) sont exclus par construction.

**Contrôle négatif 3 — le scan après la passe.** Sur les **723** fiches de `reports/`, il reste
**0 fiche de résultats** qui publie u
… [7923 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"^##\\|^###\" reports/rapport-semaine.md | head -60; echo ---; sed -n '1,120p' reports/rapport-semaine.md", "description": "Read week report overview"}`

  ```
26:## 1. Ce que la semaine devait produire — et ce qu'elle a produit
40:## 2. Les chiffres avant/après
42:### 2.1 Le produit : F1, attachement, POS
70:### 2.2 Le tagger POS : la seule mesure qui change l'ordre de grandeur
93:### 2.3 L'intégration Panini : quatre briques, quatre contrôles
130:### 2.4 La coordination N2 / S / R / A
172:## 3. Les décisions
190:## 4. Les rejets
216:## 5. Ce qui reste
247:## 6. La chronologie et les commits
262:## 7. Ce qui pourrait rendre ce rapport faux
295:## 8. Fichiers
319:## 9. Verdict
---
# J5.1 — le rapport de semaine : le produit gagne 3,69 points de F1, l'intégration est bornée

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (le moteur de pensée), **R0.7** (le bloc langue), **N2**, **S**,
> **R**, **A**, **Panini** · **Tâche** : J5.1 · **Date** : 2026-11-13 · **Verdict** : ✅
>
> **Ce que ce rapport est.** La **relecture consolidée** des fiches des jours 1 à 4 : les chiffres
> avant/après, les décisions, les 
… [8703 caractères tronqués]
  ```

- **bash** `{"command": "for f in atomes-niveaux corpus-commun retrieval-epoque genealogie-deux-faces retrieval-familles; do echo \"===== $f\"; python3 - <<EOF\nimport json\nd=json.load(open('reports/$f.json'))\ndef walk(o,p='',depth=0):\n    if depth>1: return\n    if isinstance(o,dict):\n        for k,v in o. … [504 caractères tronqués]`

  ```
===== atomes-niveaux
fiche: reports/rapport-atomes-niveaux.md
version: 1.0
date: 2026-11-07
titre: Table de correspondance — 14 atomes V14 de Panini et 8 niveaux Drave
statut: hypothese_de_lecture_et_protocole_non_mesure
sources dict 2
  atomes dict 5
  niveaux dict 2
niveaux list 8
  ['graphème', 'mot', 'pos', 'syntagme', 'phrase', 'pragmatique', 'discours', 'document']
niveaux_du_contrat list 9
  ['graphème', 'morphème', 'mot', 'pos', 'syntagme', 'phrase', 'discours', 'pragmatique', 'document']
principe dict 5
  non_bijection: True
  ancrage: plus petite unite ou l'atome a une marque observable dediee
  porteur: niveau ou l'atome est une contribution semantique mesurable
  portee list 3
  note: Le porteur est un choix de mesure, pas une essence ; le JSON conserve les niveaux secondaires et la portee.
atomes list 14
  [0] keys: ['rang', 'symbole', 'nom', 'prime', 'colonne', 'periode', 'capte', 'ancrage', 'porteur', 'niveaux_secondaires', 'portee', 'signal', 'mesure', 'controle_negatif', 'falsification', 'exemple']
calibration_44_oeuvres dict 9
  source: ../../Panini/research/nipada/falsification/analytic_sigs_v1.json
  n_oeuvres: 44
  parts_somme_1: True
  statistiques dict 14
  c
… [11628 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor name in ['atomes-niveaux','corpus-commun','retrieval-epoque','genealogie-deux-faces','retrieval-familles']:\n    d=json.load(open(f'reports/{name}.json'))\n    print('='*80); print(name)\n    if name=='retrieval-epoque':\n        for k in ['b7','udhr' … [1514 caractères tronqués]`

  ```
================================================================================
atomes-niveaux
calibration {"source": "../../Panini/research/nipada/falsification/analytic_sigs_v1.json", "n_oeuvres": 44, "parts_somme_1": true, "statistiques": {"ÊTRE": {"moyenne": 0.107443, "ecart_type": 0.032566, "min": 0.050592, "max": 0.165658, "cv": 0.3031}, "DIFFÉRENCE": {"moyenne": 0.023207, "ecart_type": 0.010585, "min": 0.004031, "max": 0.043502, "cv": 0.4561}, "RAPPORT": {"moyenne": 0.088174, "ecart_type": 0.034694, "min": 0.033223, "max": 0.175124, "cv": 0.3935}, "ORIENTATION": {"moyenne": 0.006197, "ecart_type": 0.00308, "min": 0.000913, "max": 0.014632, "cv": 0.4971}, "SUJET": {"moyenne": 0.189031, "ecart_type": 0.028152, "min": 0.087297, "max": 0.233076, "cv": 0.1489}, "TEMPS": {"moyenne": 0.080068, "ecart_type": 0.023334, "min": 0.018835, "max": 0.127257, "cv": 0.2914}, "MODALITÉ": {"moyenne": 0.03647, "ecart_type": 0.019462, "min": 0.002513, "max": 0.098077, "cv": 0.5336}, "NOMBRE": {"moyenne": 0
================================================================================
corpus-commun
{"appariables_article1": 438, "article1_drave": 440, "drave_article1_hors_panini": 2, "drave_lan
… [19020 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-niveaux.json'))\nc=d['calibration_44_oeuvres']\nfor k,v in c.items():\n    if isinstance(v,(int,float,str,bool,list)): print(k, json.dumps(v,ensure_ascii=False)[:400])\nprint('--- correlations brutes')\nprint(json.dumps(c[ … [245 caractères tronqués]`

  ```
source "../../Panini/research/nipada/falsification/analytic_sigs_v1.json"
n_oeuvres 44
parts_somme_1 true
comparaison_brut_clr [{"a": "NOMBRE", "b": "ÉQUATION", "r_brut": 0.9232, "r_clr": 0.5771}, {"a": "ÊTRE", "b": "DIFFÉRENCE", "r_brut": 0.8574, "r_clr": 0.581}, {"a": "ÊTRE", "b": "RAPPORT", "r_brut": -0.8463, "r_clr": -0.4195}, {"a": "RAPPORT", "b": "ESPACE", "r_brut": -0.8286, "r_clr": -0.7513}]
lecture "Les 44 oeuvres sont majoritairement philosophiques et religieuses ; les correlations refletent le genre, l'epoque et le lexique, pas la structure linguistique. Les parts sont compositionnelles : passer au CLR change la structure (NOMBRE-EQUATION +0,923 -> +0,577 ; ETRE-RAPPORT -0,846 -> -0,420). Quatre composantes ont une valeur propre > 1 ; les trois premieres expliquent 80,7 % de la variance : 
--- correlations brutes
{"n_paires_abs_r_sup_0_5": 33, "top": [{"a": "NOMBRE", "b": "ÉQUATION", "r": 0.9232}, {"a": "ÊTRE", "b": "DIFFÉRENCE", "r": 0.8574}, {"a": "ÊTRE", "b": "RAPPORT", "r": -0.8463}, {"a": "RAPPORT", "b": "ESPACE", "r": -0.8286}, {"a": "ÊTRE", "b": "ESPACE", "r": 0.7958}, {"a": "RAPPORT", "b": "MODALITÉ", "r": -0.7598}, {"a": "DIFFÉRENCE", "b": "RAPPORT", "r": -0.758
… [615 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(p.keys())\nfor t in p['taches'][:30]:\n    print(t['id'], '|', t['titre'], '|', t.get('jour'))\nEOF", "description": "List all plan tasks"}`

  ```
dict_keys(['nom', 'principe', 'taches'])
J0 | Le contrôle du superviseur | 0
J1.1 | r035 : la relative zéro | 1
J1.2 | La convention des GV | 1
J1.3 | Le schéma v2 | 1
J1.4 | La restitution v0 | 1
J2.1 | Panini I — la table atomes ↔ niveaux | 2
J2.2 | Panini I — le corpus commun | 2
J3.1 | Panini II — le retrieval à époque contrôlée | 3
J3.2 | Panini II — la généalogie à deux faces | 3
J4.1 | Coordination N2 — le mètre RoPE | 4
J4.2 | Coordination S — les 11 verdicts | 4
J4.3 | Coordination R — le tagger sur 612 | 4
J4.4 | Coordination A — A6.2 et A8.3b2 | 4
J5.1 | Le rapport de semaine | 5
J5.2 | La passe complète et le tag | 5
J6.1 | Le dernier span g017 | 6
J6.2 | La cible s065 | 6
J7.1 | Panini — le retrieval approfondi | 7
J8.1 | La restitution v1 | 8
J9.1 | La passe d'honnêteté des fiches | 9
J10.1 | Le bilan de la semaine | 10
J11.1 | Le produit — les exemples rejoués | 11
J11.2 | Le produit — la mesure par langue | 11
J11.3 | Le produit — la robustesse des 50 textes | 11
J11.4 | Le contrat — le schéma v2 documenté | 11
J12.1 | Panini — le §334 et les 44 œuvres | 12
J12.2 | Panini — le corpus d'or CIC | 12
J13.1 | Les bilans — la table des mesures | 13
J14.1 | La clôture — l
… [22 caractères tronqués]
  ```

- **bash** `{"command": "for c in 25a6c0ff 92652984 9a259953 8eb0cc49 9c7f71dc c3467170 c2e629b3 a934d779 34e3e4ab 64d9dd23 b6e474dc e4288023 d31e8788 229098ec ecef7250 03ecee41 84e393bb 09e54143 55bde5c5 febfdfff bb68b820 b20a4c31; do git show -s --format='%h %ad %s' --date=format:'%Y-%m-%d %H:%M' $c | cut -c1 … [60 caractères tronqués]`

  ```
25a6c0ff 2026-11-07 12:40 B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
92652984 2026-11-07 13:44 B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ;
9a259953 2026-11-07 14:23 B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE
8eb0cc49 2026-11-07 14:45 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE
9c7f71dc 2026-11-07 14:55 PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE
c3467170 2026-11-07 18:12 PANINI — J2.2 ET J3.1 : LE CORPUS COMMUN (418/438 PAIRES EXACTES, 8/8 CONTRÔLES) ET LE RETRIEVAL À ÉPOQU
c2e629b3 2026-11-07 18:15 J3.2 — DEUX FACES : 154/154 PAIRES HORS SCRIPT AU HASARD, PANINI 3/655 PAIRES INTER-LANGUES ET 5/21 LANG
a934d779 2026-11-13 22:37 R0.7 — LE TAGGER POS SUR LE GOLD 612 : 0,9475 (3012/3179), +8,49 PTS, LA RÈGLE DIT INTÉGRER ; LA CLÉ ÉTA
34e3e4ab 2026-11-13 23:08 J5.1 — LE RAPPORT DE SEMAINE : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 237, TAGGER 0,9475 (+8,49, INTÉGRER
64d9dd23 2026-11-14 00:52 J6.1 — g017 : LA RÈGLE DE L'ADVERBE
… [1604 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py evaluer --json > /tmp/eval612.json 2>/tmp/eval612.err; echo rc=$?; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/eval612.json'))\nh=d.get('heuristique',d)\nfor k in ['phrases','tokens']:\n    print(k,h … [393 caractères tronqués]`

  ```
rc=0
phrases 612
tokens None
pos {'exactitude': 0.8625, 'exactitude_ferme': 0.9373, 'exactitude_ouvert': 0.7918, 'tokens': 3179, 'confusions': {'ADJ': {'ADJ': 65, 'NOUN': 65, 'VERB': 4}, 'ADV': {'ADV': 131, 'NOUN': 7, 'PREP': 1, 'ADJ': 1, '?': 1}, 'AUX': {'PREP': 4, 'AUX': 119, '?': 3, 'NOUN': 1, 'VERB': 1}, 'CONJ': {'PRON': 15, 'CONJ': 68, '?': 13, 'PREP': 2}, 'DET': {'DET': 586, '?': 2}, 'NOUN': {'NOUN': 657, 'ADJ': 17, 'VERB': 7, '?': 1}, 'NUM': {'NUM': 2}, 'PONCT': {'PONCT': 25}, 'PREP': {'PREP': 114}, 'PRON': {'PRON': 429, '?': 30, 'CONJ': 2, 'DET': 14}, 'VERB': {'VERB': 546, 'NOUN': 218, 'PREP': 2, 'ADJ': 2, '?': 16, 'AUX': 7, 'ADV': 1}}}
syntagme {'precision': 0.786, 'rappel': 0.7944, 'f1': 0.7902, 'tp': 1480, 'fp': 403, 'fn': 383, 'tete': {'precision': 0.9261, 'rappel': 0.8808, 'f1': 0.9029, 'tp': 1641, 'fp': 131, 'fn': 222}}
tete None
attachement {'cibles': 239, 'labels': 238, 'top1': 238, 'topk': 236, 'exact': 238, 'top1_taux': 0.9958, 'topk_taux': 0.9874, 'exact_taux': 0.9958, 'exact_any': 238, 'exact_any_taux_span': 1.0, 'top1_taux_span': 1.0, 'topk_taux_span': 0.9916, 'topk_exact': 236, 'topk_exact_taux': 0.9874, 'topk_exact_taux_span': 0.9916, 'exact_taux_span': 1.0, 
… [387 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py evaluer --gold --json > /tmp/eval602.json 2>/tmp/eval602.err; echo rc=$?; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/eval602.json'))\nh=d.get('heuristique',d)\nfor k in ['phrases','tokens']:\n    pr … [282 caractères tronqués]`

  ```
rc=0
phrases 602
tokens None
pos {'exactitude': 0.8625, 'exactitude_ferme': 0.9373, 'exactitude_ouvert': 0.7914, 'tokens': 3141, 'confusions': {'ADJ': {'ADJ': 65, 'NOUN': 64, 'VERB': 4}, 'ADV': {'ADV': 129, 'NOUN': 7, 'PREP': 1, 'ADJ': 1, '?': 1}, 'AUX': {'PREP': 4, 'AUX': 117, '?': 3, 'NOUN': 1, 'VERB': 1}, 'CONJ': {'PRON': 15, 'CONJ': 67, '?': 13, 'PREP': 2}, 'DET': {'DET': 586, '?': 2}, 'NOUN': {'NOUN': 657, 'ADJ': 17, 'VERB': 7, '?': 1}, 'NUM': {'NUM': 2}, 'PONCT': {'PONCT': 15}, 'PREP': {'PREP': 114}, 'PRON': {'PRON': 419, '?': 29, 'CONJ': 2, 'DET': 14}, 'VERB': {'VERB': 538, 'NOUN': 216, 'PREP': 2, 'ADJ': 2, '?': 15, 'AUX': 7, 'ADV': 1}}}
syntagme {'precision': 0.7818, 'rappel': 0.7946, 'f1': 0.7882, 'tp': 1455, 'fp': 406, 'fn': 376, 'tete': {'precision': 0.9234, 'rappel': 0.8826, 'f1': 0.9025, 'tp': 1616, 'fp': 134, 'fn': 215}}
tete None
attachement {'cibles': 239, 'labels': 234, 'top1': 234, 'topk': 232, 'exact': 234, 'top1_taux': 0.9791, 'topk_taux': 0.9707, 'exact_taux': 0.9791, 'exact_any': 234, 'exact_any_taux_span': 1.0, 'top1_taux_span': 1.0, 'topk_taux_span': 0.9915, 'topk_exact': 232, 'topk_exact_taux': 0.9707, 'topk_exact_taux_span': 0.9915, 'exact_taux_span': 1.0,
… [338 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"gelé 602\" reports/*.md | grep -E \"0,7[0-9]{3}|23[0-9]|0,86|0,85\" | head -40", "description": "Find historical frozen 602 metrics"}`

  ```
reports/rapport-audit-r1r3.md:73:0,5720 / 0,4910 / 0,6018 / 0,7262. La fiche indique « gelé 602 » sur la ligne F1 ; elle ne
reports/rapport-audit-v7.md:205:| T107 | **gelé 602** | 602 phrases, POS 0,7603 | 602, 0,7603, tête 0,7205 | ✅ |
reports/rapport-audit-v7.md:207:| T111 | **gelé 602** | tête hybride 0,7265 | 0,7265 | ✅ |
reports/rapport-audit-v7.md:209:| T113 | **gelé 602** | F1 0,5595, tête 0,7205 | idem | ✅ |
reports/rapport-audit-v7.md:210:| T114 | **gelé 602** | cascade 0,5864 / 0,7285, 602 appels | idem | ✅ |
reports/rapport-audit-v7.md:212:| T119 | **gelé 602** | résumé 0,7465 / 0,6914 | idem | ✅ |
reports/rapport-coherence-fiches-v7.md:189:| V7-2 | **critique** | en-tête, § 2 | F1 **0,5595**, tête **0,7205**, POS **0,7603** présentées avec le gold **612** (§ 3) | ces trois valeurs sont celles du gold **gelé 602** ; sur 612, le code donne F1 **0,5555**, tête **0,7152**, POS **0,7581**. La couverture (196/239) et l'exactitude (195/196) sont, elles, sur le 612 |
reports/rapport-coherence-fiches-v8.md:148:- **v8** publie `0,5763` / `0,7316`, valeurs du **602** ; la table le dit (« gelé 602 »), mais
reports/rapport-dev-test-v7.md:28:> **F1 0,5595, tête 0,7205, POS 0,7603** s
… [1125 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' journal/2026-11-14/mesures.md; echo '--- README'; sed -n '1,80p' journal/2026-11-14/README.md", "description": "Inspect journal entries for the day"}`

  ```
# 2026-11-14 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (7)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:06 | `b6e474dc` | J6.2 — s065 : LA REL SUIVIE D'UN GV PREND LE SUJET DU GV (238/238 LABELS, 238/239 CIBLES, F1 0,7902 INCHANGÉ, 0 SPAN, 0 POS) | `chantiers.md`, `en-cours.md`, `roadmap.md` (+14) |
| 01:08 | `6ecc9763` | JOURNAL — 2026-11-14 : J6.2 AU RÉCIT (2 COMMITS, LE THÈME MESURES), s065 238/238 | `README.md`, `mesures.md`, `README.md` (+4) |
| 03:23 | `229098ec` | J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS) | `en-cours.md`, `roadmap.md`, `README.md` (+24) |
| 03:53 | `03ecee41` | J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ | `en-cours.md`, `roadmap.md`, `semaine-autonome.md` (+16) |
| 04:28 | `84e393bb` | J11.1 — LES 5 EXEMPLES R
… [8077 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' docs/pilotage/roadmap.md", "description": "Read roadmap"}`

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
… [25123 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/porte-tableaux.sh; echo '---'; sed -n '1,160p' tools/revue_documentation.py", "description": "Inspect table gate and doc review"}`

  ```
#!/bin/bash
# porte-tableaux.sh — un tableau Markdown qui ne rend pas est un tableau qui n'existe PAS.
#
# POURQUOI CETTE PORTE EXISTE. Le 13/10, le premier tableau de `docs/etat-cerveau.md` s'affichait
# comme du TEXTE dans docwatch : une seule ligne (`| **C2 (cycle 2 régions)** | … |`) avait
# **4 cellules pour 5 colonnes** — un lien qui avait glissé d'une colonne. Le rendu (mistune,
# puis markdown_it, puis markdown) refuse alors le tableau ENTIER, sans rien dire : les 13 lignes
# disparaissent de la page et personne ne le voit, parce que le texte est toujours là, en gris.
#
# CE QU'ELLE VÉRIFIE (trois conditions, toutes nécessaires au rendu) :
#   1. l'en-tête et le séparateur d'un tableau ont le MÊME nombre de cellules ;
#   2. chaque ligne du corps a ce nombre de cellules ;
#   3. aucun `\|` ne subsiste : mistune ne le déséchappe NI dans un espace de code NI dans la
#      prose (il s'affiche alors littéralement). Pour une barre de valeur absolue dans du code,
#      on écrit `∣` (U+2223), qui rend partout et ne casse pas la lecture.
# Les tableaux DANS une citation (`> | … |`) sont valides et vérifiés aussi.
#
# CE QU'ELLE NE VÉRIFIE PAS : les tableaux « écrasés » sur une se
… [12461 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"def charger\\|gold\" tools/tests/linguistique/evaluer_gold.py | head -30; echo ---; sed -n '1,80p' tools/tests/linguistique/evaluer_gold.py", "description": "Inspect gold loader paths"}`

  ```
1:"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).
19:GOLD = pathlib.Path(__file__).with_name("gold.json")
20:REEL = pathlib.Path(__file__).with_name("gold_reel.json")
21:SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")
24:def charger() -> list[dict]:
35:GELE = pathlib.Path(__file__).with_name("gold_gele.json")
38:def charger_gele() -> list[dict]:
39:    """Le gold **gelé** : une copie figée pour les portes à nombre absolu.
41:    Le gold vivant grandit (phrases, liens) ; les portes qui codent un chiffre exact
109:        pred_seg, gold_seg = _seg(a), {(s["type"], s["debut"], s["fin"]) for s in phrase["segments"]}
110:        tp += len(pred_seg & gold_seg)
111:        fp += len(pred_seg - gold_seg)
112:        fn += len(gold_seg - pred_seg)
114:        gold_tete = {(s["type"], s["debut"]) for s in phrase["segments"]}
115:        ttp += len(pred_tete & gold_tete)
116:        tfp += len(pred_tete - gold_tete)
117:        tfn += len(gold_tete - pred_tete)
138:            # le gold admet parfois plusieurs cibles (43/96 GP) : mesure secondaire
141:            # le gold mêle deux conventions : la cible est un verbe (le gouverneu
… [3380 caractères tronqués]
  ```

- **bash** `{"command": "git ls-files tools/tests/linguistique/ | head; git ls-files data/ | head; git status --porcelain | head -20", "description": "Check tracked gold files and working tree status"}`

  ```
tools/tests/linguistique/anaphore.py
tools/tests/linguistique/classement_cible.py
tools/tests/linguistique/classer_gv.py
tools/tests/linguistique/evaluer_gold.py
tools/tests/linguistique/gold.json
tools/tests/linguistique/gold.py
tools/tests/linguistique/gold_gele.json
tools/tests/linguistique/gold_reel.json
tools/tests/linguistique/gold_reel.py
tools/tests/linguistique/gold_split.py
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-c3f599ea-570a-4db4-ad78-8eff22004a4c/digest.md
 M journal/sessions/session-c3f599ea-570a-4db4-ad78-8eff22004a4c/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/structures
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "git rev-parse 25a6c0ff^ && git log -1 --format='%h %ad %s' --date=short 25a6c0ff^", "description": "Identify parent commit of first chantier task"}`

  ```
d7469b5c2cb258598fe6ac573d4c652575f99601
d7469b5c 2026-11-07 INDEX — RÉGÉNÉRÉ APRÈS L'INVENTAIRE PANINI (702 FICHES) ; ÉTAT HORODATÉ
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git worktree add --detach /tmp/qtrinet-pre d7469b5c >/tmp/wt.log 2>&1; echo rc=$?; tail -3 /tmp/wt.log; cd /tmp/qtrinet-pre && python3 tools/drave.py evaluer --json >/tmp/pre612.json 2>/tmp/pre612.err; echo rc612=$?; python3 tools/dr … [195 caractères tronqués]`

  ```
rc=0
Preparing worktree (detached HEAD d7469b5c)
HEAD is now at d7469b5c INDEX — RÉGÉNÉRÉ APRÈS L'INVENTAIRE PANINI (702 FICHES) ; ÉTAT HORODATÉ
rc612=0
rc602=0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor tag,path in [('pre612','/tmp/pre612.json'),('pre602','/tmp/pre602.json'),('post612','/tmp/eval612.json'),('post602','/tmp/eval602.json')]:\n    d=json.load(open(path)); h=d.get('heuristique',d)\n    pos=h['pos']; syn=h['syntagme']; att=h['attachement' … [687 caractères tronqués]`

  ```
pre612 phrases 612 tokens 3179
  POS 0.8625 ferme 0.9373 ouvert 0.7918
  F1 0.8143 P 0.8616 R 0.7719 tp/fp/fn 1438 231 425
  tete 0.9071
  att labels/cibles 223 239 exact 211 exact_taux 0.8828 couv 0.9331 span 0.9462 topk 213 0.8912
  lineaire None None
pre602 phrases 602 tokens 3141
  POS 0.8625 ferme 0.9373 ouvert 0.7914
  F1 0.8135 P 0.8586 R 0.7728 tp/fp/fn 1415 233 416
  tete 0.9066
  att labels/cibles 219 239 exact 207 exact_taux 0.8661 couv 0.9163 span 0.9452 topk 209 0.8745
  lineaire None None
post612 phrases 612 tokens 3179
  POS 0.8625 ferme 0.9373 ouvert 0.7918
  F1 0.7902 P 0.786 R 0.7944 tp/fp/fn 1480 403 383
  tete 0.9029
  att labels/cibles 238 239 exact 238 exact_taux 0.9958 couv 0.9958 span 1.0 topk 236 0.9874
  lineaire None None
post602 phrases 602 tokens 3141
  POS 0.8625 ferme 0.9373 ouvert 0.7914
  F1 0.7882 P 0.7818 R 0.7946 tp/fp/fn 1455 406 376
  tete 0.9025
  att labels/cibles 234 239 exact 234 exact_taux 0.9791 couv 0.9791 span 1.0 topk 232 0.9707
  lineaire None None
  ```

- **bash** `{"command": "cd /tmp/qtrinet-pre && python3 tools/drave.py evaluer --help 2>&1 | head -40; echo ---; grep -n \"vue\\|alternative\\|lineaire\\|union\" tools/drave.py | head -40", "description": "Inspect pre-era evaluer options"}`

  ```
usage: drave evaluer [-h] [--gold] [--json]

Mesure POS, syntagmes (F1/tête) et attachement (exact/couverture) sur le gold, avec un contrôle négatif reproductible.

options:
  -h, --help, --aide  afficher cette aide et quitter
  --gold              mesurer le gold gelé (référence figée) au lieu du gold vivant
  --json              sortie JSON des mesures complètes

Exemple : python3 tools/drave.py evaluer --gold --json
---
261:        f"  vue linéaire (partition filtrer) F1 {_pct(rapport['syntagmes_lineaire']['f1'])}  "
262:        f"· attachement {_pct(rapport['attachement_lineaire']['couverture'])} de couverture",
279:    # transparence : la vue **fidèle** (défaut) et la vue **linéaire** (partition filtrer)
280:    _lineaire = evaluateur.evaluer_bloc("lineaire", bl.Heuristique(partition="filtrer"), phrases)
292:        "syntagmes_lineaire": _lineaire["syntagme"],
293:        "attachement_lineaire": {"exact": _lineaire["attachement"]["exact"],
294:                                 "labels": _lineaire["attachement"]["labels"],
295:                                 "couverture": _lineaire["attachement"]["couverture"]},
357:        "Options : --json, --langue fr|en, --partition brut|al
… [464 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor tag,path in [('pre612','/tmp/pre612.json'),('post612','/tmp/eval612.json')]:\n    d=json.load(open(path))\n    print(tag, list(d.keys()))\n    h=d.get('heuristique',{})\n    print('  heur keys', list(h.keys()))\n    if 'syntagmes_lineaire' in h: print … [248 caractères tronqués]`

  ```
pre612 ['version', 'gold', 'heuristique', 'syntagmes_lineaire', 'attachement_lineaire', 'controle_negatif']
  heur keys ['bloc', 'phrases', 'pos', 'syntagme', 'pragmatique', 'fraction_semantique', 'attachement', 'attachement_tete']
  syntagmes_lineaire {'precision': 0.8616, 'rappel': 0.7719, 'f1': 0.8143, 'tp': 1438, 'fp': 231, 'fn': 425, 'tete': {'precision': 0.9599, 'rappel': 0.8599, 'f1': 0.9071, 'tp': 1602, 'fp': 67, 'fn': 261}}
  attachement_lineaire {'exact': 211, 'labels': 223, 'couverture': 0.9331}
post612 ['version', 'gold', 'heuristique', 'syntagmes_lineaire', 'attachement_lineaire', 'controle_negatif']
  heur keys ['bloc', 'phrases', 'pos', 'syntagme', 'pragmatique', 'fraction_semantique', 'attachement', 'attachement_tete']
  syntagmes_lineaire {'precision': 0.8539, 'rappel': 0.7783, 'f1': 0.8144, 'tp': 1450, 'fp': 248, 'fn': 413, 'tete': {'precision': 0.9482, 'rappel': 0.8642, 'f1': 0.9042, 'tp': 1610, 'fp': 88, 'fn': 253}}
  attachement_lineaire {'exact': 224, 'labels': 224, 'couverture': 0.9372}
    return "\n".join([
        f"{NOM} {VERSION} — évaluation de l'heuristique sur le gold",
        f"gold {gold['nom']} · {gold['phrases']} phrases · {gold['tokens']} tokens
… [2823 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet-pre && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nsys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as ev\nfor name, phrases in [('612', ev.charger()), ('602', ev.charger_gele())]:\n    for view in [' … [477 caractères tronqués]`

  ```
612 alternative pos 0.8625 f1 0.8143 P 0.8616 R 0.7719 tete 0.9071 att 211 / 239 labels 223 couv 0.9331 span 0.9462 topk 213
612 filtrer pos 0.8625 f1 0.8143 P 0.8616 R 0.7719 tete 0.9071 att 211 / 239 labels 223 couv 0.9331 span 0.9462 topk 213
612 brut pos 0.8625 f1 0.8143 P 0.8616 R 0.7719 tete 0.9071 att 211 / 239 labels 223 couv 0.9331 span 0.9462 topk 213
602 alternative pos 0.8625 f1 0.8135 P 0.8586 R 0.7728 tete 0.9066 att 207 / 239 labels 219 couv 0.9163 span 0.9452 topk 209
602 filtrer pos 0.8625 f1 0.8135 P 0.8586 R 0.7728 tete 0.9066 att 207 / 239 labels 219 couv 0.9163 span 0.9452 topk 209
602 brut pos 0.8625 f1 0.8135 P 0.8586 R 0.7728 tete 0.9066 att 207 / 239 labels 219 couv 0.9163 span 0.9452 topk 209
  ```

- **bash** `{"command": "git show -s --format='%h author=%ai committer=%ci %s' 25a6c0ff d7469b5c | cut -c1-160; echo ---; git log --oneline --graph --decorate -15 25a6c0ff", "description": "Check commit dates and graph"}`

  ```
25a6c0ff author=2026-11-07 12:40:29 -0500 committer=2026-11-07 12:40:29 -0500 B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
d7469b5c author=2026-11-07 11:16:18 -0500 committer=2026-11-07 11:16:18 -0500 INDEX — RÉGÉNÉRÉ APRÈS L'INVENTAIRE PANINI (702 FICHES) ; ÉTAT HORODATÉ
---
* 25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
* d7469b5c INDEX — RÉGÉNÉRÉ APRÈS L'INVENTAIRE PANINI (702 FICHES) ; ÉTAT HORODATÉ
* 34fdd4ef DOCS — README T1 TENU (DEUX LIGNES LONGUES RACCOURCIES)
* fffbbe5d PANINI — L'INVENTAIRE INTÉGRÉ AU PLAN : 14 DÉPÔTS, 7 AXES, 14 ATOMES, 9 CORPUS, TROIS INTÉGRATIONS MÛRES (UDHR+GÉNÉALOGIE, ATOMES↔NIVEAUX, CORPUS CIC) AVEC LEURS CONTRÔLES NÉGATIFS
* f93ddc60 DOCS — README T1 : DEUX LIGNES RACCOURCIES, BUDGET TENU
* f1b837a3 DOCS — README T1 SOUS 1 000 MOTS ET COMPTEUR DES DOCUMENTS À 123
* fae117e5 DOCS — README T1 ET COMPTEURS APRÈS LE MÉTA-HARNAIS
* c49367e0 CHANTIER AUTONOME — LE MÉTA-HARNAIS : FILE DE 15 TÂCHES, SUPERVISEUR QUI LANCE dsh headless (CLÉ LUE), VÉRIFIE L'ACCEPTATION, PERSISTE L'ÉTAT ET S'ARRÊTE PROPREMENT ; DOCTRINE ET MODES DE PANNE
* a2ad039d DOCS — README T1 : UN MOT DE MOINS
* 
… [616 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat --oneline 25a6c0ff | sed -n '1,60p'; echo ---; git show --stat --oneline 92652984 | sed -n '1,60p'", "description": "Check files changed in J1.1/J1.2"}`

  ```
25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
 docs/pilotage/en-cours.md                          |  19 +-
 docs/pilotage/roadmap.md                           |   2 +-
 docs/pilotage/semaine-autonome.md                  |   6 +-
 reports/INDEX.md                                   |   3 +-
 reports/README.md                                  |   1 +
 reports/pensee-r035.json                           | 191 +++++++++++++++++++++
 reports/rapport-r035.md                            | 128 ++++++++++++++
 tools/bloc_linguistique.py                         |  50 +++++-
 tools/pensee/autotest.py                           |  44 ++---
 tools/tests/linguistique/test_bloc_linguistique.py |  27 +++
 10 files changed, 431 insertions(+), 40 deletions(-)
---
92652984 B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183
 docs/pilotage/en-cours.md                          |   14 +-
 docs/pilotage/roadmap.md                           |    2 +-
 docs/pilotage/semaine-autonome.md                  |    2 +-
 journal/2026-11-07/README.md                       |   10 +-
 journal/2026-11-07/distribue.md     
… [1406 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet-pre && for c in 25a6c0ff 92652984; do git checkout -q --detach $c; echo \"=== $c $(git log -1 --format=%s | cut -c1-60)\"; python3 tools/drave.py evaluer --json > /tmp/ev_$c.json 2>/dev/null; python3 - <<EOF\nimport json\nd=json.load(open('/tmp/ev_$c.json')); h=d['heuris … [402 caractères tronqués]`

  ```
=== 25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS IN
default f1 0.816 P 0.8634 R 0.7735 att 212 / 239 labels 224 couv 0.9372 span 0.9464
lineaire f1 0.816 att 212 / 224
=== 92652984 B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINA
default f1 0.8188 P 0.8664 R 0.7762 att 212 / 239 labels 224 couv 0.9372 span 0.9464
lineaire f1 0.8188 att 212 / 224
  ```

- **bash** `{"command": "cd /tmp/qtrinet-pre && git checkout -q --detach d7469b5c && sha256sum tools/tests/linguistique/gold.json tools/tests/linguistique/gold_gele.json tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold_synthetique.json; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet &&  … [294 caractères tronqués]`

  ```
3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a  tools/tests/linguistique/gold.json
f2632969fbe38f67320deae3dc0052b607ffd79fcbeec29cb55d08dbb34105f1  tools/tests/linguistique/gold_gele.json
05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11  tools/tests/linguistique/gold_reel.json
e159dbfaa97a12907f79f5440981db39232c1ec4d96d48dfcafc33c4bba6dd7d  tools/tests/linguistique/gold_synthetique.json
3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a  tools/tests/linguistique/gold.json
f2632969fbe38f67320deae3dc0052b607ffd79fcbeec29cb55d08dbb34105f1  tools/tests/linguistique/gold_gele.json
05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11  tools/tests/linguistique/gold_reel.json
e159dbfaa97a12907f79f5440981db39232c1ec4d96d48dfcafc33c4bba6dd7d  tools/tests/linguistique/gold_synthetique.json
56b22212 B13 — LES 19 RÉPONSES DE RÉFÉRENCE : COUVERTURE 19/19, LE JUGE EST UTILISABLE ; 127/127
c6fb94e2 L — LECTURE DOUBLE : TOP-1 TÊTE 0,957 (0,800 RÉEL/1,0 SYNTH), 29 CIBLES AMBIGUËS
c5d38030 L — ATTACHEMENT : TOP-1 0,294 / TOP-K 0,338 SUR 68 CIBLES (COUVERTURE 0,338), HASARD 0,015
550cd76d L — GOLD v0 : 20 PHRASES, POS 0,924, SYNTAGMES 0,356
… [30 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet-pre && git checkout -q --detach 92652984 && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nprint(bl.__file__)\nprint(sys.path[:5])\nimport os\nprint('cwd',os.getcwd())\nEOF\npython3 tools/drave.py evaluer --json | python3 -c \" … [202 caractères tronqués]`

  ```
/tmp/qtrinet-pre/tools/bloc_linguistique.py
['tools', '', '/usr/lib64/python313.zip', '/usr/lib64/python3.13', '/usr/lib64/python3.13/lib-dynload']
cwd /tmp/qtrinet-pre
{'nom': 'vivant (hand + reel + synthétique)', 'gele': False, 'phrases': 612, 'tokens': 3179, 'cibles_attachement': 239}
0.8188 224
  ```

- **bash** `{"command": "cd /tmp/qtrinet-pre && git checkout -q --detach 92652984 && sed -n '1,80p' reports/rapport-convention-gv.md; grep -n \"0,7902\\|237/238\\|238/239\\|F1\" reports/rapport-convention-gv.md | head -30", "description": "Inspect J1.2 report in its commit"}`

  ```
# B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.2 · **Date** : 2026-11-07 ·
> **Verdict** : ✅
> Les **322 FP / 180 FN** du plan sont les erreurs **de GV** du gold d'avant `r035` (F1 0,7533) ;
> après `r035` (J1.1), la base courante est **320 FP / 179 FN** (F1 0,7549). Le classement ne
> change pas : **144 FP de sujet (45 %)** dominent, puis 73 d'objet, 39 de troncature. Deux règles
> candidates sont mesurées : **le sujet hors du GV** (F1 **+0,0332**, 0 perte d'attachement) et
> **l'arrêt à l'adverbe final de temps** (F1 **+0,0026**). Les deux sont **gardées** et combinées :
> **F1 0,7549 → 0,7902** (dev **0,7875**, test **0,7962**), **POS 0,8625 inchangée**, **attachement
> 237/238 inchangé** (0 cible perdue), **183/183 portes**. S/D/N2 intouchés.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_sujet_hors_gv`,
> `ADVERBES_TEMPS`, la condition d'adverbe du GV), [`autotest.py`](../tools/pensee/autotest.py)
> (T110–T115, T156 recalés) ; JSON [`pensee-convention-gv.json`](pensee-convention-gv.json).

## 1. Le chiffre du plan et le chiffre courant

Le plan J1.2 po
… [5627 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -- tools/tests/linguistique/evaluer_gold.py | head -20; echo ---; cd /tmp/qtrinet-pre && git checkout -q --detach 92652984; sha256sum tools/tests/linguistique/evaluer_gold.py tools/bloc_linguistique.py; echo ---; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sh … [218 caractères tronqués]`

  ```
2b3e1796 B13 — LES COMPOSITIONS NE PERDENT PLUS : CASCADE = HEURISTIQUE (0,8383, 235/236), VERDICT COMPARATIF RESTAURÉ ; 183/183
9952a330 PRODUIT — LA DOC D'USAGE ET LES EXEMPLES ; cascade_pos DEVIENT UN PLANCHER (0,70) ET LA PORTE BLOC REPASSE VERTE ; 84 PORTES
841e0e71 B13 — LA MESURE PAR LANGUE : FR 113/117 (0,9658), EN 28/28 (1,000) MAIS 28 LABELS SUR 88 CIBLES ; 183/183
e59ba071 B13 — MULTI-CIBLES (EXACT_ANY 143/145), AUDITS A8/A10/A13 INTÉGRÉS, DOCSTRINGS ET CODE MORT NETTOYÉS ; 182/182
9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
e223a98d B13 — LE TOP-K STRICT : 0,6069 EN ÉGALITÉ EXACTE, PAS 0,9241 (SOUS-CHAÎNES) ; 176/176
f70a1b2a B13 — LES DEUX CONVENTIONS DU GOLD : VERBES 37/51 (0,7255), NOMS 57/95 (0,6000) ; 172/172
f8f5bc04 B13 — LE DÉNOMINATEUR DE L'ATTACHEMENT : RENDEMENT (÷239) ET EXACTITUDE SPANS (÷146), 0,7877/0,9041/0,2260 ; 170/170
20194fb1 B13 — LE GOLD GELÉ : 602 PHRASES, 21 PORTES PROTÉGÉES ; 133/133
41c7d1f1 B13 — LA CORÉFÉRENCE À 103 LIENS : 86/103, CIBLE 100 ATTEINTE, GOLD 407 ; 112/112
4d8c9905 B13 — LA CORÉFÉRENCE À 68 LIENS : LE RÔLE PASSE DEVANT (5
… [1156 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet-pre && git checkout -q --detach 92652984 && for opt in \"\" \"--gold\"; do echo \"=== opt='$opt'\"; python3 tools/drave.py evaluer $opt --json > /tmp/evx.json 2>/dev/null; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/evx.json')); h=d['heuristique']; s=h['syntag … [351 caractères tronqués]`

  ```
=== opt=''
{'nom': 'vivant (hand + reel + synthétique)', 'gele': False, 'phrases': 612, 'tokens': 3179, 'cibles_attachement': 239}
f1 0.8188 P 0.8664 R 0.7762 tp/fp/fn 1446 223 417 att 212 / 239 labels 224 couv 0.9372 span 0.9464
lineaire 0.8188
=== opt='--gold'
{'nom': 'gelé (référence figée)', 'gele': True, 'phrases': 602, 'tokens': 3141, 'cibles_attachement': 239}
f1 0.8169 P 0.8623 R 0.7761 tp/fp/fn 1421 227 410 att 208 / 239 labels 220 couv 0.9205 span 0.9455
lineaire 0.8169
  ```

- **bash** `{"command": "cd /tmp/qtrinet-pre && git checkout -q --detach 92652984 && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-convention-gv.json'))\ndef walk(o,p='',depth=0):\n    if depth>2: return\n    if isinstance(o,dict):\n        for k,v in o.items():\n            if isinstance(v,d … [257 caractères tronqués]`

  ```
date: 2026-11-07
ligne: B13
tache: J1.2
objet: la convention des GV
baseline_commit: 25a6c0ff
dispositif {...}
  code: tools/bloc_linguistique.py
  classement: tools/tests/linguistique/classer_gv.py
  mesure: tools/tests/linguistique/evaluer_gold.py
  fiche: reports/rapport-convention-gv.md
gold {...}
  phrases: 612
  tokens: 3179
  dev: 422
  test: 190
  note: gold vivant 612 (hand 20 + reel 200 + synthetique 392) ; split crc32(id)%3
convention_du_gold {...}
  gv_total: 712
  debut_verbe: 590
  debut_aux: 97
  debut_adv: 25
  debut_sujet: 0
  verdict: 712/712 GV du gold commencent par VERB, AUX ou ADV (négation) ; aucun par un sujet.
  adverbe_final {...}
    gv_finissant_par_adv: 39
    adv_hors_gv: 72
    contradictions_exactes [...] 2
    verdict: le gold n'a pas une convention unique pour l'adverbe final : 39 GV l'incluent, 72 ADV sont hors GV, et deux phrases iden
avant_plan {...}
  all {...}
    phrases: 612
    f1: 0.7533
    precision: 0.7239
    rappel: 0.7853
    tp: 1463
    fp: 558
    fn: 400
    tete_f1: 0.864
    pos: 0.8625
    att_exact: 236
    att_labels: 237
    att_cibles: 239
    att_couverture: 0.9916
  dev {...}
    phrases: 422
    f1: 0.7476
    precision
… [4084 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"602\\|612\\|0,7533\\|236/237\" docs/pilotage/semaine-autonome.md | head -40; echo ---; grep -n \"602\\|612\\|0,7533\\|236/237\" tools/chantier/plan.json | head -40", "description": "Search plan for baseline bases"}`

  ```
42:| **R** | R0.7 heuristique ; R1.2-1024 mesuré | le tagger sur 612 (**clé absente**), R1.1, R2.1 | R (lecture seule) |
118:5. **L'honnêteté** : un chiffre porte sa **base** (gold vivant 612 / gelé 602), son **commit**, son
128:| **la clé DeepSeek absente** | le tagger sur 612 et la rétro-traduction sont bloqués | décider : mesure < +2 pts → négatif nommé ; sinon demander la clé |
194:| **J1** | matin : `r035` + convention GV | ✅ fait | exact **237/238**, couverture **0,9958**, F1 **0,7533 → 0,7902**, POS inchangée | `25a6c0ff`, `92652984` | `g017`, `s065`, objet (75 FP / 51 FN), 5 FP sujet |
204:| **J6** | matin : le dernier span `g017` | ✅ fait (rejet) | règle rejetée : F1 **0,7901**, test **−0,0028**, attachement **236/237** | `64d9dd23` | convention du gold à trancher |
234:| POS (gold vivant 612) | 0,8625 | **0,8625** (0 token changé) | [r035](../../reports/rapport-r035.md) |
235:| F1 syntagmes | 0,7533 | **0,7902** (+0,0369) | [convention](../../reports/rapport-convention-gv.md) |
236:| attachement | 236/237 labels (236/239 cibles, 0,9916) | **238/238 labels** (238/239 cibles, 0,9958) | [s065](../../reports/rapport-s065.md) |
---
171:   "titre": "Coordination R — le tagger s
… [647 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/eval612.json'))\nprint('lineaire',d['syntagmes_lineaire'])\nprint('att lineaire',d['attachement_lineaire'])\nprint('controle negatif',d['controle_negatif'])\nd2=json.load(open('/tmp/eval602.json'))\nprint('602 lineaire',d2['syntagme … [194 caractères tronqués]`

  ```
lineaire {'precision': 0.8539, 'rappel': 0.7783, 'f1': 0.8144, 'tp': 1450, 'fp': 248, 'fn': 413, 'tete': {'precision': 0.9482, 'rappel': 0.8642, 'f1': 0.9042, 'tp': 1610, 'fp': 88, 'fn': 253}}
att lineaire {'exact': 224, 'labels': 224, 'couverture': 0.9372}
controle negatif {'nom': 'cible exacte tirée au hasard dans le gold', 'graine': 0, 'cibles': 239, 'exact_taux': 0.0167}
602 lineaire {'precision': 0.8502, 'rappel': 0.7783, 'f1': 0.8127, 'tp': 1425, 'fp': 251, 'fn': 406, 'tete': {'precision': 0.9457, 'rappel': 0.8656, 'f1': 0.9039, 'tp': 1585, 'fp': 91, 'fn': 246}}
602 att lineaire {'exact': 220, 'labels': 220, 'couverture': 0.9205}
602 controle negatif {'nom': 'cible exacte tirée au hasard dans le gold', 'graine': 0, 'cibles': 239, 'exact_taux': 0.0167}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-bilan-chantier.json'))\nprint(json.dumps(d['chiffres']['tagger'],ensure_ascii=False,indent=1)[:3000])\nEOF", "description": "Extract tagger data from J10.1 JSON"}`

  ```
{
 "n": 612,
 "jetons": 3179,
 "avant": 0.8625,
 "apres": 0.9475,
 "comptes": {
  "avant": "2742/3179",
  "apres": "3012/3179"
 },
 "gain_pts": 8.49,
 "ic95": [
  7.23,
  9.74
 ],
 "mcnemar": {
  "b": 344,
  "c": 74,
  "p": 1.0847968259787153e-42
 },
 "reel_432": {
  "avant": 0.8893,
  "apres": 0.936,
  "gain_pts": 4.67,
  "ic95": [
   3.45,
   6.01
  ]
 },
 "synth_160": {
  "avant": 0.7682,
  "apres": 0.9828,
  "gain_pts": 21.46,
  "ic95": [
   18.8,
   24.15
  ]
 },
 "hand_20": {
  "avant": 0.8857,
  "apres": 0.9714,
  "gain_pts": 8.57,
  "note": "in-sample : a servi au choix du modèle et du prompt"
 },
 "controles": {
  "majoritaire": 0.2145,
  "classe_frequente": 0.2491,
  "permutation": 0.1667,
  "uniforme": 0.0833
 },
 "cout": {
  "appels": 1218,
  "tokens": 358962,
  "duree_s": 1259.2,
  "dollars": 0.04,
  "cache": "neuf",
  "modele_renvoye": "deepseek-flash"
 },
 "baseline_085": {
  "statut": "datée",
  "commit": "97256b8f",
  "reference_head": 0.8625,
  "surestimation_pts": 1.26
 },
 "decision": "intégrer",
 "mode": "NeuronalLLMPOS seul (API), derrière un drapeau, repli heuristique",
 "reserve": "réel 432 seul +4,67 pts ; le 612 est tiré par les 160 synthétiques (+21,46)",
… [153 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet-pre && git checkout -q --detach 92652984 && sed -n '240,360p' tools/tests/linguistique/evaluer_gold.py; echo '--- argparse'; grep -n \"argparse\\|add_argument\\|def main\\|__main__\" tools/tests/linguistique/evaluer_gold.py", "description": "Inspect J1.2 evaluator main"}`

  ```
resultats = {nom: {src: evaluer_bloc(nom, bloc, ps) for src, ps in sources.items()}
                 for nom, bloc in blocs.items()}
    resultats["cascade"]["appels_neuronal"] = cascade.appels_neuronal
    reel = {"statut": "non demandé"}
    if args.reel:
        try:
            from bloc_linguistique import NeuronalLLM
            m = NeuronalLLM(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf", timeout=10)
            a = m.analyser("Le chat dort.", "fr")
            reel = {"statut": "ok", "etiquettes": len(a.etiquettes)}
        except Exception as e:
            reel = {"statut": "refus", "detail": type(e).__name__ + ": " + str(e)[:160]}
    resultats["reel"] = reel
    # contrôle négatif : une cible tirée au hasard parmi les cibles du gold
    import random as _r
    cibles = [s["cible"] for p in phrases for s in p["segments"] if s.get("cible")]
    rng = _r.Random(0)
    hasard_ok = sum(1 for c in cibles if c in rng.choice(cibles))
    resultats["attachement_hasard"] = {"cibles": len(cibles),
                                       "top1_taux": round(hasard_ok / max(1, len(cibles)), 4)}
    resultats["gold"] = {"phrases": len(phrases),
                         "reel": len(sources[
… [2937 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet-pre && sed -n '80,210p' tools/tests/linguistique/evaluer_gold.py", "description": "Inspect J1.2 evaluer_bloc implementation"}`

  ```
def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
    tp = fp = fn = ttp = tfp = tfn = 0
    pos_ok = pos_n = pos_ok_ferme = pos_n_ferme = pos_ok_ouvert = pos_n_ouvert = 0
    conf = defaultdict(Counter)
    acte_ok = neg_ok = mod_ok = ds_ok = 0
    fractions = []
    att_n = att_labels = att_top1 = att_topk = att_exact = 0
    att_topk_exact = 0
    att_exact_any = 0
    par_langue = {"fr": {"cibles": 0, "labels": 0, "exact": 0, "topk": 0},
                  "en": {"cibles": 0, "labels": 0, "exact": 0, "topk": 0}}
    att_v_n = att_v_ok = att_n_n = att_n_ok = 0
    att_t_n = att_t_labels = att_t_top1 = att_t_topk = 0
    for phrase in phrases:
        a = bloc.analyser(phrase["texte"], phrase["langue"])
        fractions.append(a.fraction_semantique)
        pos = _pos_map(a)
        for mot in phrase["mots"]:
            pred = pos.get((mot["debut"], mot["fin"]), "?")
            pos_n += 1
            pos_ok += int(pred == mot["pos"])
            ferme = mot["pos"] in {"DET", "PREP", "PRON", "CONJ", "AUX", "ADV", "NUM"}
            if ferme:
                pos_n_ferme += 1
                pos_ok_ferme += int(pred == mot["pos"])
            else:
                pos
… [6030 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' tools/verifier_liens.py", "description": "Inspect link checker"}`

  ```
#!/usr/bin/env python3
"""verifier_liens.py — LES LIENS RELATIFS DES DOCUMENTS RÉSOLVENT-ILS ?

POURQUOI. Un document qui renvoie à une fiche **renommée** ou **supprimée** ne casse rien au moment
où on l'écrit ✗ : il casse **six semaines plus tard**, quand quelqu'un suit le lien et tombe sur un
fichier absent ✓. Et un document de ce dépôt **est** fait de renvois ✗ (chaque affirmation porte sa
fiche ✓, chaque fiche porte sa porte ✗) : les liens **sont** la documentation ✓. Les vérifier coûte
deux secondes ✓ et se fait à chaque passe ✓ (appelé par `porte-tableaux.sh`, la porte des documents ✓).

CE QUI EST EXAMINÉ : les liens relatifs de `docs/*.md` et `reports/*.md` — les documents **écrits à la
main** ✓. Les **journaux** sont exclus ✗ : ils sont auto-générés et renvoient à des sessions
(`sessions/<id>/rapport.md`) qui ne sont pas versionnées ✓ ; les signaler serait du bruit ✗✓. Les
**exemples de code** sont exclus aussi ✗ (un `[chemin](chemin)` dans un bloc ``` n'est pas un lien ✓),
**et les cibles sans barre ni point** ✓ (le même motif écrit **en prose**, pour décrire la vérification
elle-même, dans `rapport-coherence-docs-2.md` ✓ — les deux familles de faux positifs que le premie
… [2285 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/README.md; echo '--- INDEX head'; sed -n '1,80p' reports/INDEX.md", "description": "Inspect reports index files"}`

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
| [`rapport-bilan-chantier.md`](rapport-bilan-chantier.md) | **J10.1** — le bilan du chantier : F1 **0,7533 → 0,7902**, attachement **236 → 238**, Panini borné, **20/21**, 5 timeouts, 1 échec (le tag) |
| [`rapport-semaine.md`](rapport-semaine.md) | **J5.1** — le rapport de semaine : produit, intégration, dé
… [23074 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/verifie_journal.py", "description": "Inspect journal verifier"}`

  ```
#!/usr/bin/env python3
"""verifie_journal.py — un dossier par jour, et les sessions ancrées.

Règles vérifiées :
  1. aucun fichier `journal/AAAA-MM-JJ*.md` à la racine : chaque jour est un **dossier** ;
  2. chaque dossier `journal/AAAA-MM-JJ/` a un `README.md` ;
  3. chaque `README.md` de jour porte une section « Sessions DSH » et un lien vers
     `../README.md#sessions` ;
  4. chaque `journal/sessions/<id>/rapport.md` porte le bloc « Journaux » avec un lien vers
     son jour (ou le journal), vers `en-cours.md` et vers l'index des sessions ;
  5. les liens relatifs de `journal/README.md`, `journal/THEMES.md`, des `README.md` de jour
     et des rapports de session résolvent.

Usage : python3 tools/verifie_journal.py   (code 0 = journal propre)
"""
from __future__ import annotations
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "journal"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# les liens markdown, sans les ancres ni les liens externes
LIEN = re.compile(r"\]\(([^)#]+?)(?:#[^)]*)?\)")
EXTERNE = ("http://", "https://", "mailto:", "#")


def liens(texte: str) -> list[str]:
    return [c for c in LIEN.findall(texte)
          
… [3313 caractères tronqués]
  ```

### 🤖 Assistant

I'll assemble the consolidated measurement table, JSON, and verify the base numbers at HEAD. Let me first build the data file.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | grep -E '^ M tools|^\\?\\? tools' | head -10; git diff --stat HEAD -- tools/ | tail -5", "description": "Confirm no tool code was reverted"}`

  ```
M tools/structures
 tools/structures | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
  ```

- **write** `{"file_path": "/tmp/build_tableau.py", "content": "# -*- coding: utf-8 -*-\n\"\"\"Construit reports/rapport-tableau-mesures.md et reports/tableau-mesures.json (J13.1).\"\"\"\nimport json\nimport pathlib\n\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nDATE = \"2026-11-1 … [60656 caractères tronqués]`

  ```
<path>/tmp/build_tableau.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/build_tableau.py && wc -l reports/rapport-tableau-mesures.md && python3 -m json.tool reports/tableau-mesures.json >/dev/null && echo JSON-OK", "description": "Generate report and JSON"}`

  ```
md 376 lignes ; json 35166 octets
376 reports/rapport-tableau-mesures.md
JSON-OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CIBLES=\"reports/rapport-tableau-mesures.md\" bash tools/porte-tableaux.sh 2>&1 | head -40; echo RC=${PIPESTATUS[0]}", "description": "Run table gate on new report"}`

  ```
✅ 1 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4250 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,90p' reports/rapport-tableau-mesures.md", "description": "Read generated report head"}`

  ```
# J13.1 — la table des mesures : F1 0,7533 → 0,7902, attachement 236/237 → 238/238, base 612/602

> **Ligne de roadmap** : **B13** (le produit), **R0.7** (le bloc langue), **L**, **Panini**, **N2**, **S**, **R**, **A** · **Tâche** : J13.1 · **Date** : 2026-11-14 · **Verdict** : ✅
>
> **Ce que ce tableau est.** La **table consolidée** des mesures du chantier, de J1.1 à J12.2 :
> POS, F1, attachement, couverture, spans, le produit (schéma, restitution, robustesse, exemples,
> langues), le tagger et Panini (table, corpus, retrieval, généalogie, familles, §334, CIC) —
> **avant/après**, avec la **base** (612/602), les **commits** et les **contrôles négatifs**. Il
> **ne remplace pas** les fiches : il les ordonne et il nomme, pour chaque ligne, la fiche qui la
> porte. **Aucune mesure nouvelle** n'est revendiquée, sauf la **re-mesure de la base** au HEAD
> `b20a4c31` (`drave evaluer` sur le vivant 612 et le gelé 602), qui fixe les valeurs « après » du
> cœur produit et montre l'écart entre les deux bases.
>
> **Le chiffre.** Sur le **vivant 612** : **POS 0,8625** (inchangée), **F1 0,7533 → 0,7902**
> (**+0,0369**), **attachement 236/237 → 238/238 labels** (238/239 cibles, **0,9958**),
>
… [7343 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"md $(ls reports/*.md | wc -l) json $(ls reports/*.json | wc -l) docs $(find docs -name '*.md' -not -path '*/archive/*' -not -name README.md | wc -l) portes $(ls tools/porte-*.sh | wc -l)\"; date; date -u", "description": "Coun … [33 caractères tronqués]`

  ```
md 731 json 825 docs 458 portes 85
sam 14 nov 2026 06:29:23 EST
sam 14 nov 2026 11:29:23 UTC
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"J13.1\\|J12.2\\|J14.1\\|prochaine mesure\\|Ce qui reste\\|fichiers / JSON\\|dernière passe\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md", "description": "Locate state and roadmap lines to update"}`

  ```
docs/pilotage/en-cours.md:93:- **Panini J12.1–J12.2 — §334 et CIC** : §334 — 655 lignes = 495 paires uniques ; [§334](../../reports/rapport-panini-334.md). CIC — **42/42** verdicts, **42/42** empreintes, **36/36** preuves altérées rejetées, **1 020/1 020** mutations de `eq(2,2)` rejetées ; [CIC](../../reports/rapport-cic-verificateur.md).
docs/pilotage/en-cours.md:106:| fichiers / JSON de résultats | **730** / **824** | `reports/*.md` / `reports/*.json` |
docs/pilotage/en-cours.md:108:| dernière passe | **14/11 00 h 30** (84, **81/3**) ; rouges tolérées `indice`, `melange`, `sessions` | `docs/pilotage/references-non-regression.md` |
docs/pilotage/en-cours.md:126:## Ce qui reste
docs/pilotage/en-cours.md:128:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **J13.1** — table des mesures ; **S** — 11 verdicts + pointeur ; **R0.7** — split réel ; **A** — A6.2, A8.3b2 ; **J14.1** — passe + tag.
docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langu
… [4590 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '86,132p' docs/pilotage/en-cours.md", "description": "Read en-cours relevant block"}`

  ```
- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
- **N2 — en pause** : **1 024** = recette ; **2 048 fini** ; distillation mesurée ; prochaine : **porte propre (0,29)** ; **GPUs libres**.
- **Pensée — B13 (actif)** : **183/183**, gold 432 ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejetée** (g017 à trancher), schéma v2, restitution v1 (46/46, strict 0,1087), **J9.1** (19 fiches) ; [s065](../../reports/rapport-s065.md), [restitution v1](../../reports/rapport-restitution-v1.md), [J9.1](../../reports/rapport-passe-honnetete.md).
- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
- **Panini J2.1–J3.2** : table **14 atomes** ; UDHR **418/438** ; J3.1 script domine, date non significative ; J3.2 : **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, **V14 3/21** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-f
… [3987 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-14, 06 h 15 HNE (heure locale, EST).**", "new_string": "**Mis à jour : 2026-11-14, 06 h 29 HNE (heure locale, EST).**"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **J5.1 / J10.1 — les bilans** : semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, 13 décisions, 21 rejets ; [rapport](../../reports/rapport-semaine.md)) ; chantier **20/21**, attachement **2 … [591 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **730** / **824** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **731** / **825** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **J13.1** — table des mesures ; **S** — 11 verdict … [354 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 1, "limit": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-14, 06 h 15 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
11: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
12: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
13: - **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
14: - **Bloquants** : aucun.
15: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
16: 
17: ## Sessions en cours
18: 
19: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
20: > [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
21: > `plan.md` (`python3 tools/sessions
… [11756 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-14, 06 h 15 HNE (heure locale, EST).**", "new_string": "**Mis à jour : 2026-11-14, 06 h 29 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **J5.1 / J10.1 — les bilans** : semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, 13 décisions, 21 rejets ; [rapport](../../reports/rapport-semaine.md)) ; chantier **20/21**, attachement **2 … [591 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **730** / **824** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **731** / **825** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **J13.1** — table des mesures ; **S** — 11 verdict … [354 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 30, "offset": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
120: d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150
121: n'est pas reproduit (**−0,006**, p=0,093). L'avertissement de Panini est **indexé à son corpus**.
122: [`fiche`](../../reports/rapport-panini-334.md) + [`JSON`](../../reports/panini-334.json).
123: 
124: **J12.2 — le corpus d'or CIC rejoué hors de Panini.** Le corpus portable de Panini
125: (**3** defs, **21** consts, **42** entrées : **36** `accepte`, **6** `rejette`) est rejoué par un
126: noyau **CIC-lite réécrit côté Drave**, sans importer le vérificateur de Panini : **42/42** verdicts,
127: **42/42** empreintes `sha256(preuve || type)`, **42/42** sérialisations canoniques. Le contrôle
128: négatif est net : altérer le dernier octet des **36** preuves acceptées les fait **36/36** rejeter,
129: et les **1 020** mutations d'un octet de `eq(2,2)` sont **1 020/1 020** rejetées ; un noyau
130: « accepte tout » et un noyau « rejette tout » échouent (respectivement **6** et **36** désaccords).
131: La copie `tools/tests/cic/corpus_dor_cic_v1.json` est **byte-ide
… [1913 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "[`fiche`](../../reports/rapport-cic-verificateur.md) + [`JSON`](../../reports/cic-verificateur.json).\nLa prochaine mesure est **J13.1** (la table des mesures), puis **J14.1** (passe et tag).", " … [1207 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 20, "offset": 1}`

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
18: | [`rapport-bilan-chantier.md`](rapport-bilan-chantier.md) | **J10.1** — le bilan du chantier : F1 **0,7533 → 0,7902**, attachement **236 →
… [445 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "old_string": "| fichier | ce qu'il porte |\n|---|---|\n| [`rapport-bilan-chantier.md`](rapport-bilan-chantier.md) | **J10.1** — le bilan du chantier : F1 **0,7533 → 0,7902**, attachement **236 → 238**, Panini borné,  … [521 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py 2>&1 | tail -10; echo rc=$?; head -5 reports/INDEX.md; grep -n \"rapport-tableau-mesures\" reports/INDEX.md", "description": "Regenerate reports index"}`

  ```
728 fiches → reports/INDEX.md
rc=0
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **728 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.
715:| [rapport-tableau-mesures.md](rapport-tableau-mesures.md) | J13.1 — la table des mesures : F1 0,7533 → 0,7902, attachement 236/237 → 238/238, base 612/602 |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/mesures.md", "limit": 40, "offset": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/mesures.md</path>
<type>file</type>
<content>
20: 
21: `0,1087` · `0,7902` · `0,8159` · `0,7475` · `0,9451` · `0,8656` · `0,7533`
22: 
23: *Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*
24: 
25: ## Sessions actives ce jour
26: 
27: - `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 325.2 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)
28: 
29: ## Mesures et rapports touchés
30: 
31: - [reports/README.md](../../reports/README.md)
32: - [reports/rapport-bilan-chantier.md](../../reports/rapport-bilan-chantier.md)
33: - [reports/rapport-evaluer-langue.md](../../reports/rapport-evaluer-langue.md)
34: - [reports/rapport-exemples-rejoues.md](../../reports/rapport-exemples-rejoues.md)
35: - [reports/rapport-restitution-v1.md](../../reports/rapport-restitution-v1.md)
36: - [reports/rapport-robustesse-semaine.md](../../reports/rapport-robustesse-semaine.md)
37: - [reports/rapp
… [135 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/mesures.md", "old_string": "<!-- notes -->\n\n<!-- /notes -->", "new_string": "<!-- notes -->\n\n**J13.1 — la table des mesures.** Le chantier est consolidé en une table unique, de J1.1 à\nJ12.2 : **26 tâches**, **25 a … [895 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/mesures.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -60; echo RC=${PIPESTATUS[0]}", "description": "Run documentation review"}`

  ```
revue de documentation · 731 fiche(s) · 825 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo RC=${PIPESTATUS[0]}", "description": "Verify current state document"}`

  ```
en-cours · 1643 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py 2>&1 | tail -20; echo RC=${PIPESTATUS[0]}", "description": "Verify journal structure"}`

  ```
journal · 46 jour(s) · 191 session(s) · 2506 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -20; echo RC=${PIPESTATUS[0]}", "description": "Check document size budget"}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2788    205   T1   2800  reports/README.md
    2450    166   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4013 mots (budget 4 000)

  avertissements :
     · 51 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [116 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schemas.py 2>&1 | tail -20; echo RC=${PIPESTATUS[0]}", "description": "Verify schemas"}`

  ```
schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"T0\\|4013\\|budget\" tools/taille_documents.py | head -40; python3 tools/taille_documents.py 2>&1 | grep -A5 -B5 \"T0 max\"", "description": "Inspect T0 budget calculation"}`

  ```
2:"""taille_documents.py — le budget de contexte et la cohésion des documents.
5:  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
11:Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
12:ils ne sont pas chargés automatiquement. Le budget est en **mots** ; l'estimation de tokens
16:elles ne comptent pas dans le budget ; le document les porte, la page montre le SVG.
25:# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
27:    ("T0", "AGENTS.md", 1200),
28:    ("T0", "docs/pilotage/en-cours.md", 2000),
32:    ("T0", "docs/methode/*.md", 1200),
77:#: pas dans le budget de contexte. Le rendu (docwatch) est ce que voit le lecteur ;
90:    for cat, motif, budget in BUDGETS:
92:            return cat, budget
101:    for cat, motif, budget in BUDGETS:
110:            lignes.append((n, t.count("\n") + 1, rel, cat, budget))
112:            if cat in ("T0", "T1"):
122:            if budget and n > budget:
123:                violations.append(f"{rel} : {n} mots > budget {budget} ({cat})")
140:    # T0 : la somme des trois lectures par défaut
145:    # Le T0 est « AGENT
… [1563 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '130,156p' tools/taille_documents.py", "description": "Inspect T0 sum logic"}`

  ```
n = p.read_text(encoding="utf-8", errors="ignore").count("\n") + 1
        if n > 300:
            longues.append((n, p.name))
    if longues:
        longues.sort(reverse=True)
        avertissements.append(
            f"{len(longues)} fiche(s) > 300 lignes : lire le verdict + une section, jamais tout "
            f"(plus longues : {', '.join(f'{n} l. {nom}' for n, nom in longues[:5])})"
        )

    # T0 : la somme des trois lectures par défaut
    def poids(rel: str) -> int:
        q = RACINE / rel
        return mots_hors_diagrammes(q.read_text(encoding="utf-8", errors="ignore")) if q.exists() else 0

    # Le T0 est « AGENTS + en-cours + UN document de tâche », et le document de tâche est un
    # T0 (≤ 1 200 mots) : les trois documents `specifiques` ci-dessus sont des T1, avec leur
    # propre budget. Les compter ici faisait payer 1 579 mots au T0 (organisation-du-depot.md)
    # au lieu des 1 134 du plus gros T0 — un budget faux de 445 mots, dans le sens qui bloque.
    agents = [a for a in (RACINE / "docs/methode").glob("*.md") if a.name not in specifiques]
    t0 = poids("AGENTS.md") + poids("docs/pilotage/en-cours.md") + max(
        (poids(str(a.relative_to(RACINE)
… [164 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib,sys\nsys.path.insert(0,'tools')\nimport taille_documents as t\nfor f in ['AGENTS.md','docs/pilotage/en-cours.md']:\n    print(f, t.mots_hors_diagrammes(pathlib.Path(f).read_text()))\nagents=[a for a  … [405 caractères tronqués]`

  ```
AGENTS.md 1196
docs/pilotage/en-cours.md 1643
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
AttributeError: module 'taille_documents' has no attribute 'specifiques'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib,sys\nsys.path.insert(0,'tools')\nimport taille_documents as t\nvals=sorted(((t.mots_hors_diagrammes(a.read_text()),a.name) for a in pathlib.Path('docs/methode').glob('*.md')),reverse=True)\nprint(val … [100 caractères tronqués]`

  ```
[(1579, 'organisation-du-depot.md'), (1260, 'relations-humaines.md'), (1234, 'modularisation.md'), (1174, 'continuite.md'), (1089, 'contexte.md'), (1068, 'ressources.md'), (886, 'chantier-autonome.md'), (768, 'rangement.md')]
sum 4418
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **J5.1 / J10.1 / J13.1 — les bilans** : semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, 13 décisions, 21 rejets ; [rapport](../../reports/rapport-semaine.md)) ; chantier **20/21**, attache … [715 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|✅ tous\" ; echo RC=${PIPESTATUS[0]}", "description": "Recheck context budget"}`

  ```
T0 max : 4005 mots (budget 4 000)
  ❌ 1 violation(s) :
RC=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **J5.1 / J10.1 / J13.1 — les bilans** : semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, 13 décisions, 21 rejets ; [rapport](../../reports/rapport-semaine.md)) ; chantier **20/21**, attache … [635 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|✅ tous\" ; echo RC=${PIPESTATUS[0]}", "description": "Recheck context budget again"}`

  ```
T0 max : 3999 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-bilan-chantier.json'))\n# find runs\ndef walk(o,p=''):\n    if isinstance(o,dict):\n        if o.get('tache')=='J5.2' or o.get('id')=='J5.2':\n            print(json.d … [194 caractères tronqués]`

  ```
{"tache": "J5.2", "titre": "La passe complète et le tag", "duree_s": 5400.1, "code": 124, "acceptation": "rouge (tag absent)", "commit": null, "commit_le": null, "verdict": "echec", "note": "le seul échec d'acceptation : la passe 84/81/3 a été faite ailleurs (2d6f5bff), le tag n'existe pas"}
{"date": "2026-11-14", "tache": "J5.2", "livrable": "passe et tag : tag absent", "commit": null, "verdict": "echec"}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline 34e3e4ab | grep -E \"coordination|rapport-semaine\" | head -20", "description": "Verify coordination reports in J5.1 commit"}`

  ```
reports/rapport-coordination-a.json                |  328 +++
 reports/rapport-coordination-a.md                  |  474 +++
 reports/rapport-coordination-n2.json               |  247 ++
 reports/rapport-coordination-n2.md                 |  421 +++
 reports/rapport-coordination-s.json                |  533 ++++
 reports/rapport-coordination-s.md                  |  303 ++
 reports/rapport-semaine.json                       |  283 ++
 reports/rapport-semaine.md                         |  322 +++
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def split\\|dev\\|test\" tools/tests/linguistique/evaluer_gold.py | head -30; grep -n \"def split\\|dev\\|test\" tools/tests/linguistique/gold_split.py | head -30", "description": "Find dev/test split functions"}`

  ```
1:"""gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.
5:une règle, il faut un gold **tenu à l'écart** : on règle sur `dev`, on évalue sur `test`.
8:test, sinon dev), donc reproductible, insensible à l'ordre et indépendant du contenu. Il est
13:    from tools.tests.linguistique.gold_split import dev, test, compter
14:    ph = charger(); d = dev(ph); t = test(ph)
20:PART_TEST = 3  # une phrase sur trois va au test
23:def _est_test(phrase: dict) -> bool:
27:def dev(phrases: list[dict]) -> list[dict]:
29:    return [p for p in phrases if not _est_test(p)]
32:def test(phrases: list[dict]) -> list[dict]:
34:    return [p for p in phrases if _est_test(p)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nsys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as ev\nfrom gold_split import dev, test\nph=ev.charger()\nfor name, s … [321 caractères tronqués]`

  ```
dev 422 f1 0.7875 P 0.7887 R 0.7863 att 162 / 163
test 190 f1 0.7962 P 0.78 R 0.8131 att 76 / 76
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"re-mesurées.*HEAD\\|Comment lire\\|cœur produit\" /tmp/build_tableau.py | head -10", "description": "Locate sentences in builder"}`

  ```
399:    "Ce tableau agrège, il ne remplace pas les fiches. Les valeurs « avant » sont celles publiées par la fiche à son commit ; les valeurs « après » du cœur produit (P01–P12) sont re-mesurées au HEAD `b20a4c31`, les autres sont publiées par leur fiche. Si une fiche change, le tableau devient faux sans qu'aucun calcul ne l'ait signalé.",
480:> cœur produit et montre l'écart entre les deux bases.
497:> **Comment lire.** Chaque ligne porte sa **base**, son **avant**, son **après**, son **Δ**, un
499:> « avant » sont **publiées** par la fiche ; les valeurs « après » du cœur produit sont
500:> **re-mesurées** au HEAD, les autres sont **publiées** (tagger, Panini, livrables). Un chiffre
679:   par la fiche à son commit ; les valeurs « après » du cœur produit (P01–P12) sont re-mesurées au
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/build_tableau.py')\ns=p.read_text()\ns=s.replace(\"les valeurs « après » du cœur produit (P01–P12) sont re-mesurées au HEAD `b20a4c31`, les autres sont publiées par leur fiche.\ … [1083 caractères tronqués]`

  ```
ok
md 376 lignes ; json 35186 octets
32:> **re-mesurées** au HEAD (sauf P10, publiée), les autres sont **publiées** (tagger, Panini,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}", "description": "Re-run documentation review"}`

  ```
revue de documentation · 731 fiche(s) · 825 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}", "description": "Re-run table/document gate"}`

  ```
✅ 1797 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4255 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|✅ tous\"; echo RC=${PIPESTATUS[0]}", "description": "Re-check context budget"}`

  ```
T0 max : 3999 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | sed -n '1,60p'", "description": "Review working tree status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-14/mesures.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-c3f599ea-570a-4db4-ad78-8eff22004a4c/digest.md
 M journal/sessions/session-c3f599ea-570a-4db4-ad78-8eff22004a4c/rapport.md
 M reports/INDEX.md
 M reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/structures
?? reports/rapport-s-paragraphes.md
?? reports/rapport-tableau-mesures.md
?? reports/tableau-mesures.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md | sed -n '1,160p'", "description": "Inspect state/roadmap diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 76f99f4e..61b56378 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-14, 06 h 15 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-14, 06 h 29 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -91,7 +91,7 @@
 - **Panini J2.1–J3.2** : table **14 atomes** ; UDHR **418/438** ; J3.1 script domine, date non significative ; J3.2 : **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, **V14 3/21** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-faces.md).
 - **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../../reports/rapport-retrieval-familles.md).
 - **Panini J12.1–J12.2 — §334 et CIC** : §334 — 655
… [5947 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- journal/2026-11-14/mesures.md | sed -n '1,80p'; echo '--- INDEX diff'; git diff --stat -- reports/INDEX.md", "description": "Inspect journal and index diff"}`

  ```
diff --git a/journal/2026-11-14/mesures.md b/journal/2026-11-14/mesures.md
index 29c6dca5..e6e5ce76 100644
--- a/journal/2026-11-14/mesures.md
+++ b/journal/2026-11-14/mesures.md
@@ -38,4 +38,16 @@
 
 <!-- notes -->
 
+**J13.1 — la table des mesures.** Le chantier est consolidé en une table unique, de J1.1 à
+J12.2 : **26 tâches**, **25 acceptations vertes**, **1 échec** (J5.2, le tag), **5 timeouts**
+dont **4 récupérés**. Chaque ligne porte sa **base** (612/602), son **avant**, son **après**, son
+**Δ**, un **contrôle négatif**, son **commit** et sa **fiche**. Le produit tient (**F1 0,7533 →
+0,7902**, attachement **236/237 → 238/238 labels**, couverture **0,9916 → 0,9958**, spans
+**2 → 1**, schéma v2, restitution v1, 50 textes, 5 exemples, fr/en) ; le tagger vaut **0,9475
+(+8,49)** ; Panini est **borné** (table 14/14, corpus 418/438, généalogie 154/154, familles
+0,619 vs 0,0445, §334, CIC 42/42). La **base 612/602** est re-mesurée au HEAD `b20a4c31` :
+**0,7902 / 0,7882** (F1), **238/239 / 234/239** (attachement). La clôture reste **J14.1** (passe
++ tag). Fiche [`reports/rapport-tableau-mesures.md`](../../reports/rapport-tableau-mesures.md) +
+[`JSON`](../../reports/tableau-
… [125 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -6; echo RC=${PIPESTATUS[0]}", "description": "Final state document check"}`

  ```
en-cours · 1629 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py 2>&1 | tail -6; echo RC=${PIPESTATUS[0]}", "description": "Final journal check"}`

  ```
journal · 46 jour(s) · 191 session(s) · 2506 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --check -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md reports/INDEX.md journal/2026-11-14/mesures.md; echo RC=$?", "description": "Check whitespace in changed files"}`

  ```
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '150,330p' reports/rapport-tableau-mesures.md", "description": "Read rest of generated report"}`

  ```
| # | mesure | base | avant | après | Δ | contrôle négatif (résumé) | commit · fiche |
|---|---|---|---|---|---|---|---|
| N01 | Table atomes ↔ niveaux | 14 atomes × 8 niveaux | 0 ligne mesurée | **14/14 lignes** ; 33 paires ∣r∣ ≥ 0,5 ; 4 composantes > 1 ; 3 premières = **80,7 %** de la variance (6,967 / 2,845 / 1,491) | 14 lignes | hypothèse, pas corrélation ; protocole CLR/permutations/BH/split-half ; aucune correspondance atome ↔ niveau mesurée | J2.1 `9c7f71dc` · [atomes](rapport-atomes-niveaux.md) |
| N02 | Corpus commun UDHR | 532 langues Panini / 456 Drave / 438 appariables | 0 texte commun | 21 textes ; **418/438 paires exactes (95,4 %)** ; 20 écarts de surface exclus ; 5 familles, 10 écritures, 42 phrases, 3 603 caractères | 418 exactes | 8/8 (6 rejets + 2 témoins) ; altérer un caractère casse l'égalité ; appariement croisé rejeté | J2.2 `c3467170` · [corpus](rapport-corpus-commun.md) |
| N03 | Retrieval à époque contrôlée | B7 4 004 paires ; UDHR 420 ; Bible 132 | 0 mesure | B7 top-1 **0,138** vs 0,055 ; UDHR **0,049** vs 0,0333 ; Bible **0,293** vs 0,001 ; Bible écriture **+0,609** [0,529 ; 0,702], famille **+0,181** [0,106 ; 0,253], date **−0,034/siècle** [−0,075 ; +0,0
… [18513 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"P01\" /tmp/build_tableau.py | head -5", "description": "Check P01 mention in builder limits"}`

  ```
89:    dict(id="P01", section="produit", mesure="POS heuristique", base="612 · 3 179 jetons",
399:    "Ce tableau agrège, il ne remplace pas les fiches. Les valeurs « avant » sont celles publiées par la fiche à son commit ; les valeurs « après » du cœur produit (P01–P12, sauf P10) sont re-mesurées au HEAD `b20a4c31`, les autres sont publiées par leur fiche. Si une fiche change, le tableau devient faux sans qu'aucun calcul ne l'ait signalé.",
679:   par la fiche à son commit ; les valeurs « après » du cœur produit (P01–P12) sont re-mesurées au
777:        "principe": "Chaque ligne porte sa base, son avant, son apres, son delta, un controle negatif, son commit et sa fiche. Les valeurs avant sont publiees par la fiche ; les valeurs apres du coeur produit (P01-P12, sauf P10) sont re-mesurees au HEAD b20a4c31, les autres sont publiees.",
  ```

- **bash** `{"command": "sed -n '670,690p' /tmp/build_tableau.py", "description": "Inspect hardcoded section 9 text"}`

  ```
années, signatures), **altération** (un octet, un token, un champ), **version adverse** (v1/v2),
**mutation de structure** (rôles, cibles, clé), **placebo** (sujet, adverbe, dates). Chacun est
reproductible par la commande de sa fiche. Les contrôles qui **échouent** sont nommés : J5.2 (le
tag), `g017` (la convention d'adverbe), l'échantillon 20 (sous-puissant), le split réel du tagger
(pas fait), la V14 des 21 langues (pas de données), les 19 étiquettes CIC non exercées.

## 9. Ce qui pourrait rendre ce tableau faux

1. **Ce tableau agrège, il ne remplace pas les fiches.** Les valeurs « avant » sont celles publiées
   par la fiche à son commit ; les valeurs « après » du cœur produit (P01–P12) sont re-mesurées au
   HEAD `b20a4c31`, les autres sont publiées par leur fiche. Si une fiche change, le tableau devient
   faux sans qu'aucun calcul ne l'ait signalé.
2. **La base change les chiffres** : vivant 612 (F1 0,7902 ; 238/239) contre gelé 602 (F1 0,7882 ;
   234/239). Une ligne sans base peut tromper même avec des chiffres exacts.
3. **Le gain F1 est in-sample** : la convention du sujet est lue dans le gold (712/712 GV) puis
   appliquée au gold ; `s065` est un seul cas, en dev. Le 
… [444 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/build_tableau.py')\ns=p.read_text()\ns=s.replace(\"les valeurs « après » du cœur produit (P01–P12) sont re-mesurées au\\n   HEAD `b20a4c31`, les autres sont publiées par leur fi … [347 caractères tronqués]`

  ```
ok
md 376 lignes ; json 35186 octets
295:   par la fiche à son commit ; les valeurs « après » du cœur produit (P01–P12, sauf P10) sont re-mesurées
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -4; echo RC=${PIPESTATUS[0]}", "description": "Final doc review"}`

  ```
revue de documentation · 731 fiche(s) · 825 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -4; echo RC=${PIPESTATUS[0]}", "description": "Final table/document gate"}`

  ```
✅ 1797 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4255 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
RC=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md reports/INDEX.md reports/rapport-tableau-mesures.md reports/tableau-mesures.json journal/2026-11-14/mesures.md && git status --porcelain | grep -E '^[MA] '  … [59 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-14/mesures.md
M  reports/INDEX.md
M  reports/README.md
A  reports/rapport-tableau-mesures.md
A  reports/tableau-mesures.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - <<'EOF'\nJ13.1 — LA TABLE DES MESURES : F1 0,7533 → 0,7902, ATTACHEMENT 236/237 → 238/238, BASE 612/602, 26 TÂCHES (25 VERTES, 1 ÉCHEC), 18 CONTRÔLES ; J14.1 RESTE (PASSE + TAG)\n\n26 tâches de J1.1 à J12.2 : 25 accep … [751 caractères tronqués]`
