# Session DSH — relecture

- identifiant : `session-e9ee2692-96f9-42d2-886c-c5abfb51ce07`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 00:58:43
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J6.2 : la cible `s065` (« elle nage qui commence » — le gold attend `elle`, le bloc prédit `nage`). Reproduis, propose une règle (REL après GV → le sujet du GV), mesure sur dev/test, fiche `reports/rapport-s065.md` + JSON, commit. Attachement à 238/239 si la règle tient.

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

- **bash** `{"command": "pwd && ls && git log --oneline -15", "description": "Inspect repo root and recent commits"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
AGENTS.md
bench
colab
data
docs
drave-core
journal
models
__pycache__
Qtrinet-bootstrap.md
README.md
reports
REPRISE.md
run_8bit_perfection.py
run_clusters.py
run_cpu.py
run_encoding.py
run_harness.py
run_list_mode.py
run_precision.py
run_quantify.py
run_real_clusters.py
run_sparsity.py
run_value_encoding.py
sprints
src
tools
work
64d9dd23 J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CONVENTION DU GOLD À TRANCHER
34e3e4ab J5.1 — LE RAPPORT DE SEMAINE : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 237, TAGGER 0,9475 (+8,49, INTÉGRER), INTÉGRATION BORNÉE (TABLE 14/14, CORPUS 418/438), 13 DÉCISIONS, 21 REJETS
dc78f223 ÉTAT — T0 DANS LE BUDGET (3 991 MOTS) : LA LIGNE R0.7 PORTE LE TAGGER 612 (0,9475, +8,49, INTÉGRER)
a934d779 R0.7 — LE TAGGER POS SUR LE GOLD 612 : 0,9475 (3012/3179), +8,49 PTS, LA RÈGLE DIT INTÉGRER ; LA CLÉ ÉTAIT PRÉSENTE ET 0,8500 ÉTAIT DATÉ (0,8625)
ced21933 CHANTIER — PHASE 2 (12 H) : LE VERDICT ACCEPTATION D'ABORD (TIMEOUT APRÈS COMMIT = FAIT), 12 TÂCHES AJOUTÉES (J4 COORDINATION, J6 SPANS, J7-J10 PANINI/BILAN), 
… [1167 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | head -50; echo ---; ls journal/ | head -30", "description": "List reports and journal entries"}`

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
---
2026-09-25
2026-09-26
2026-09-27
2026-09-28
2026-09-29
2026-09-30
2026-10-01
2026-10-02
2026-10-03
2026-10-04
2026-10-05
2026-10-06
2026-10-07
2026-10-08
2026-10-09
2026-10-10
2026-10-
… [183 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"s065\\|J6.2\\|J6\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md 2>/dev/null | head -40", "description": "Find J6/s065 references in pilotage"}`

  ```
docs/pilotage/en-cours.md:63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (adverbe final hors SUB : g017 gagné, r264/r288 perdus ; test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v0** (46/46, miroir 0,1087) ; **contrat v1**, **`drave` v0**.
docs/pilotage/en-cours.md:66:- **Prochaine action** : **trancher la convention d'adverbe (`g017`)** ; puis **`s065`** (J6.2), T132/T133, gold 200+.
docs/pilotage/en-cours.md:90:- **Pensée — B13 (actif)** : **183/183**, gold 432, pragmatique 130/432 ; **`r035`** (237/238) ; **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (adverbe final hors SUB, test −0,0028 ; g017 : convention à trancher) ; **schéma v2** (26 cas, 0 échec ; v1 lue) ; **restitution v0** (46/46, miroir 0,1087) ; [restitution](../../reports/rapport-restitution-v0.md), [g017](../../reports/rapport-g017.md).
docs/pilotage/en-cours.md:116:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 et convention des GV (0,7902, 237/238), J6
… [1567 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i \"s0\\|s1\\|g0\" | head -40; echo ---; grep -rln \"s065\" reports/ journal/ docs/ 2>/dev/null | head", "description": "Find related report files"}`

  ```
pensee-g017.json
pensee-gold-complexes100.json
rapport-g017.md
rapport-pensee-gold-complexes100.md
---
reports/rapport-annotation-independante.md
reports/pensee-annotation-independante.json
reports/pensee-replis-cible.json
reports/rapport-replis-cible.md
reports/rapport-spans-v7.md
reports/pensee-spans-v7.json
reports/pensee-topk-v8.json
reports/rapport-audit-r1r3.md
reports/pensee-audit-r1r3.json
reports/pensee-coherence-fiches-v8.json
  ```

- **bash** `{"command": "cat reports/rapport-g017.md", "description": "Read previous J6.1 report"}`

  ```
# B13 — g017 : l'adverbe final hors de la SUB est rejeté (g017 gagné, r264 et r288 perdus)

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.1 · **Date** : 2026-11-14 ·
> **Verdict** : ❌ **règle rejetée**.
> La règle demandée — **l'adverbe final de temps hors de la SUB** — corrige bien `g017`
> (`that she would come` au lieu de `that she would come yesterday`) et retire un faux positif
> de `g005`, mais elle **casse `r264`** (`qu'il vient demain`) et **`r288`**
> (`that he comes tomorrow`) : **F1 0,7902 → 0,7901 (−0,0001)**, **dev +0,0011**, **test
> −0,0028**, **attachement 237/238 → 236/237**, **couverture 0,9958 → 0,9916**. Les deux cas
> favorables sont en **dev**, les deux cas défavorables en **test** : le gain est in-sample, la
> perte est hors échantillon. **Aucun code de production n'est modifié** ; la porte du bloc
> reste verte, et l'état reste à **237/238**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (lecture seule),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; copies locales dans
> `/tmp/g017/` (`bloc_g
… [11160 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nd=json.load(open('reports/pensee-g017.json'))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:4000])\n\"", "description": "Inspect g017 JSON structure"}`

  ```
{
 "date": "2026-11-14",
 "ligne": "B13",
 "tache": "J6.1",
 "objet": "g017 — la règle de l'adverbe final de temps hors de la SUB est mesurée puis rejetée",
 "verdict": {
  "regle": "rejetée",
  "raison": "elle corrige g017 (dev) mais casse r264 et r288 (test) : F1 all −0,0001, test −0,0028, attachement 237/238 → 236/237",
  "f1_avant": 0.7902,
  "f1_apres": 0.7901,
  "delta_f1": -0.0001,
  "dev_avant": 0.7875,
  "dev_apres": 0.7886,
  "delta_dev": 0.0011,
  "test_avant": 0.7962,
  "test_apres": 0.7934,
  "delta_test": -0.0028,
  "attachement_avant": "237/238",
  "attachement_apres": "236/237",
  "couverture_avant": 0.9958,
  "couverture_apres": 0.9916
 },
 "dispositif": {
  "gold": "tools/tests/linguistique/evaluer_gold.py::charger (612 phrases, 239 cibles)",
  "split": "tools/tests/linguistique/gold_split.py (crc32(id) % 3)",
  "module_base": "tools/bloc_linguistique.py (lecture seule, non modifié)",
  "copies": {
   "regle": "/tmp/g017/bloc_g017.py",
   "adv_large": "/tmp/g017/bloc_adv_large.py",
   "garde": "/tmp/g017/bloc_garde.py",
   "placebo": "/tmp/g017/bloc_placebo.py"
  },
  "note_copie": "chaque copie remplace RACINE par le dépôt, sinon generateur.py (le générateur S) n
… [2800 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"s065\" tools/ data/ 2>/dev/null | head -20", "description": "Locate s065 in gold data"}`

  ```
tools/tests/linguistique/gold_synthetique.json:3816:   "id": "s065",
tools/tests/linguistique/gold_gele.json:35574:"id": "s065",
tools/chantier/plan.json:244:   "titre": "La cible s065",
tools/chantier/plan.json:245:   "mandat": "Tâche J6.2 : la cible `s065` (« elle nage qui commence » — le gold attend `elle`, le bloc prédit `nage`). Reproduis, propose une règle (REL après GV → le sujet du GV), mesure sur dev/test, fiche `reports/rapport-s065.md` + JSON, commit. Attachement à 238/239 si la règle tient.",
tools/chantier/plan.json:249:     "commande": "test -f reports/rapport-s065.md && echo FICHE-OK",
data/corpus_wiki_en/train.txt:1737333:Minsk-Pasažyrski (, ) is the main passenger railway station in Minsk, Belarus. It is located in the centre of Minsk. It is sometimes called Minsk Ploshchad Lenina due to the metro station serving the terminal, or simply Minsk. History The station was built in 1873 as Vilen'ski vakzal, Vilnius station ( ). The initial wooden building was demolished in 1890 and rebuilt in stone. During World War II, Minsk railway station was completely destroyed. It was rebuilt in 1945–1946 and served until 1991. The new building of Minsk-Passazhyrski railway station
… [3019 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests/linguistique/; echo ---; sed -n '1,120p' tools/tests/linguistique/evaluer_gold.py", "description": "Inspect linguistics tooling"}`

  ```
anaphore.py
classement_cible.py
classer_gv.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel.json
gold_reel.py
gold_split.py
gold_synthetique.json
gold_synthetique.py
juge.py
miroir.py
__pycache__
qualifier_cascade.py
qualifier_frontiere_71.py
qualifier_lien_appris.py
qualifier_neuronal.py
qualifier_pragmatique.py
qualifier_quatre_modes.py
qualifier_syntagmes.py
qualifier_tagger_612.py
replis_cible.py
test_bloc_linguistique.py
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
SYNTH = pathlib.Path(__file__)
… [4190 caractères tronqués]
  ```

- **job_kill** `{"job_id": "bash-7", "reason": "grep over huge corpus unnecessary"}`

  ```
requested cancellation of job bash-7
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f in ['tools/tests/linguistique/gold_synthetique.json','tools/tests/linguistique/gold_gele.json']:\n    d=json.load(open(f))\n    for p in d['phrases']:\n        if p['id']=='s065':\n            print(f)\n            print(json.dumps(p,ensure_ascii=Fa … [63 caractères tronqués]`

  ```
tools/tests/linguistique/gold_synthetique.json
{
 "id": "s065",
 "langue": "fr",
 "texte": "elle qui commence nage",
 "pragma": {
  "acte": "assertion",
  "negation": false,
  "modalite": false,
  "double_sens": false
 },
 "source": "synthetique",
 "mots": [
  {
   "texte": "elle",
   "pos": "PRON",
   "debut": 0,
   "fin": 4
  },
  {
   "texte": "qui",
   "pos": "PRON",
   "debut": 5,
   "fin": 8
  },
  {
   "texte": "commence",
   "pos": "VERB",
   "debut": 9,
   "fin": 17
  },
  {
   "texte": "nage",
   "pos": "VERB",
   "debut": 18,
   "fin": 22
  }
 ],
 "segments": [
  {
   "type": "GN",
   "texte": "elle",
   "role": "gn",
   "debut": 0,
   "fin": 4
  },
  {
   "type": "REL",
   "texte": "qui commence",
   "role": "rel",
   "debut": 5,
   "fin": 17,
   "cibles": [
    "elle"
   ],
   "cible": "elle"
  },
  {
   "type": "GV",
   "texte": "nage",
   "role": "gv",
   "debut": 18,
   "fin": 22
  }
 ]
}
tools/tests/linguistique/gold_gele.json
{
 "id": "s065",
 "langue": "fr",
 "texte": "elle qui commence nage",
 "pragma": {
  "acte": "assertion",
  "negation": false,
  "modalite": false,
  "double_sens": false
 },
 "source": "synthetique",
 "mots": [
  {
   "texte": "elle",
   "po
… [628 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/bloc_linguistique.py; grep -n \"REL\\|relation\\|rel\\b\\|cible\" tools/bloc_linguistique.py | head -80", "description": "Find REL handling in block"}`

  ```
2881 tools/bloc_linguistique.py
375:RELATIFS = {"qui", "que", "qu", "dont", "où", "which", "that", "who", "whom", "whose",
387:AMBIGUES_REL = {"when", "where", "why", "how", "quand", "où", "pourquoi", "comment"}
565:# liste ou une ponctuation répétée ne coupent pas la phrase ; un saut de ligne structurel
997:    def _cibles_s(self, texte: str) -> dict:
998:        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
1001:        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
1009:            return {(s.debut, s.fin, s.type): (s.cible_gp or s.cible_nom or s.cible_verbe)
1015:    def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
1016:        """REL → tête du GN précédent ; SUB après un GV → son verbe (le gouverneur)."""
1019:        if segment.get("type") == "REL" and precedent.get("type") == "GN":
1029:        """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
1032:        if segment.get("type") == "REL" and precedent.get("type") == "GN":
1048:    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict]) -> str | None:
1063:    
… [5158 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\na=bl.analyser('elle qui commence nage','fr')\nfor e in a.etiquettes:\n    print(e)\nEOF", "description": "Run block on s065"}`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
AttributeError: module 'bloc_linguistique' has no attribute 'analyser'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^class\\|^def \\|^    def \" tools/bloc_linguistique.py | head -60", "description": "List classes and functions"}`

  ```
59:class Span:
63:    def json(self) -> dict:
68:class Etiquette:
81:    def json(self) -> dict:
98:class Annotation:
111:    def par_niveau(self) -> dict[str, list[Etiquette]]:
117:    def couverture(self) -> dict[str, float]:
122:    def json(self, avec_duree: bool = False) -> dict:
138:class BlocLinguistique(Protocol):
141:    def analyser(self, texte: str, langue: str | None = None,
145:class RefusNeuronal(RuntimeError):
152:def _normaliser(texte: str) -> str:
156:def _trigrammes(texte: str) -> list[str]:
161:def _profil(texte: str, top: int = 200) -> dict[str, int]:
166:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
200:def _score_profil(tri: collections.Counter, profil: dict[str, int]) -> float:
207:def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
238:def _script_char(ch: str) -> str:
264:def detecter_script(texte: str) -> str:
489:def _est_adverbe_seul(g: dict) -> bool:
501:def _sans_enclitique(mot: str) -> str:
509:def _est_verbe(mot: str) -> bool:
538:def _role_gp(prep: str) -> str:
615:def _couper_fin(texte: str, debut: int, fin: int) -> int:
624:def _zones_protegees(texte: str) -> list[tuple[int, int]]:
645:def _dans_z
… [2409 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '980,1210p' tools/bloc_linguistique.py", "description": "Read cible logic"}`

  ```
sortie.extend([gn, gv])
                        continue
                sortie.append(s)
            c["segments"] = sortie
        return cands

    def _syntagmes_s(self, texte: str) -> list[dict] | None:
        if not self.segmenter_s:
            return None
        try:
            if str(RACINE / "tools/structures") not in sys.path:
                sys.path.insert(0, str(RACINE / "tools/structures"))
            import generateur  # le générateur S, importé en lecture seule
            return generateur.analyser(texte)
        except Exception:
            return None

    def _cibles_s(self, texte: str) -> dict:
        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).

        Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
        (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
        """
        if not self.segmenter_s:
            return {}
        try:
            import generateur
            base = generateur._segmente(texte, generateur._tokens(texte))
            return {(s.debut, s.fin, s.
… [9905 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1433,1480p' tools/bloc_linguistique.py; tail -40 tools/bloc_linguistique.py", "description": "Read analyser signature and module tail"}`

  ```
def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        if not isinstance(texte, str):
            # une entrée non textuelle est **refusée** proprement (le produit ne plante pas)
            return Annotation(texte=str(texte)[:200], refus="non_texte", source=self.nom,
                              trace=[{"etape": "refus", "raison": "non_texte",
                                      "type": type(texte).__name__}],
                              cout={"octets": 0, "duree_s": round(time.perf_counter() - t0, 6)})
        texte = texte or ""
        trace: list[dict] = []
        if not texte.strip() or not any(ch.isalpha() or ch.isdigit() for ch in texte):
            return Annotation(texte=texte, refus="vide", source=self.nom,
                              trace=[{"etape": "refus", "raison": "vide"}],
                              cout={"octets": len(texte.encode("utf-8", "replace")), "duree_s": round(time.perf_counter() - t0, 6)})

        lg, conf_lg, script = self._langue(texte, langue)
        trace.append({"etape": "langue", "langue": lg, "script": script, "confiance": conf_l
… [3778 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\na=h.analyser('elle qui commence nage','fr')\nfor e in a.etiquettes:\n    print(e.json())\nprint('meta',a.meta if hasattr(a … [64 caractères tronqués]`

  ```
{'niveau': 'graphème', 'type': 'lettres', 'valeur': 'elle', 'debut': 0, 'fin': 4, 'source': 'heuristique', 'confiance': 0.99, 'candidats': [], 'langue': 'fr', 'script': 'Latn', 'meta': {}}
{'niveau': 'mot', 'type': 'mot', 'valeur': 'elle', 'debut': 0, 'fin': 4, 'source': 'heuristique', 'confiance': 0.98, 'candidats': [], 'langue': 'fr', 'script': 'Latn', 'meta': {}}
{'niveau': 'pos', 'type': 'PRON', 'valeur': 'elle', 'debut': 0, 'fin': 4, 'source': 'heuristique', 'confiance': 0.92, 'candidats': [], 'langue': 'fr', 'script': 'Latn', 'meta': {'ouvert': False}}
{'niveau': 'syntagme', 'type': 'GN', 'valeur': 'elle', 'debut': 0, 'fin': 4, 'source': 'heuristique', 'confiance': 0.55, 'candidats': ['« qui commence nage » → elle', 'nage', 'elle'], 'langue': 'fr', 'script': 'Latn', 'meta': {'role': 'agent', 'niveau': 0, 'attachement': {'segment': 'elle', 'cible': 'nage'}}}
{'niveau': 'discours', 'type': 'paragraphe', 'valeur': 'suite', 'debut': 0, 'fin': 22, 'source': 'heuristique', 'confiance': 0.5, 'candidats': ['suite', 'contraste', 'cause', 'conséquence'], 'langue': 'fr', 'script': 'Latn', 'meta': {}}
{'niveau': 'document', 'type': 'paragraphe', 'valeur': 'elle qui commence nage', 'debut
… [5436 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1580,1750p' tools/bloc_linguistique.py", "description": "Read composed segment assembly"}`

  ```
and (_n in ADJECTIFS.get("fr", set()) or _n.endswith(_suf_adj))):
                    etiquettes[_i] = Etiquette("pos", "ADJ", _e.valeur, _e.debut, _e.fin, self.nom,
                                               0.85, candidats=["adj"], langue=lg, script=script,
                                               meta={"ouvert": True, "contexte": "copule_fr"})

        # 3 e. « que » : **PRON** relatif après un nom (« Le livre que j'ai lu »), **CONJ**
        # ailleurs (« Je sais qu'il vient »). Le gold : 7 PRON / 38 CONJ.
        for _k, _i in enumerate(pos_idx):
            _e = etiquettes[_i]
            if _e.type != "PRON" or _normaliser(_e.valeur) not in ("que", "qu'"):
                continue
            _av = etiquettes[pos_idx[_k - 1]] if _k else None
            _cls = "PRON" if (_av is not None and _av.type in ("NOUN", "PRON")) else "CONJ"
            if _cls != _e.type:
                etiquettes[_i] = Etiquette("pos", _cls, _e.valeur, _e.debut, _e.fin, self.nom,
                                           _e.confiance, candidats=[_cls.lower()], langue=lg,
                                           script=script, meta={"ouvert": False, "contexte": "que"})

        # 4. phr
… [10298 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/structures')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nprint('S:', h._syntagmes_s('elle qui commence nage'))\nprint('simp:', h._syntagmes_ … [222 caractères tronqués]`

  ```
S: [{'nom': '« qui commence nage » → elle', 'lecture': '« qui commence nage » se rattache à « elle »', 'attachement': {'segment': 'qui commence nage', 'cible': 'elle', 'genre': 'GN'}, 'segments': [{'debut': 0, 'fin': 4, 'texte': 'elle', 'type': 'GN', 'role': 'agent', 'niveau': 0, 'parent': None, 'profondeur': 0}, {'debut': 5, 'fin': 22, 'texte': 'qui commence nage', 'type': 'REL', 'role': 'qualite', 'niveau': 1, 'parent': 0, 'profondeur': 1}]}]
simp: [{'type': 'REL', 'role': 'qualité', 'niveau': 1, 'debut': 5, 'fin': 17, 'texte': 'qui commence', 'candidats': []}, {'type': 'GV', 'role': 'prédicat', 'niveau': 0, 'debut': 18, 'fin': 22, 'texte': 'nage', 'candidats': []}]
Sujet hors gv: [{'nom': '« qui commence nage » → elle', 'lecture': '« qui commence nage » se rattache à « elle »', 'attachement': {'segment': 'qui commence nage', 'cible': 'elle', 'genre': 'GN'}, 'segments': [{'debut': 0, 'fin': 4, 'texte': 'elle', 'type': 'GN', 'role': 'agent', 'niveau': 0, 'parent': None, 'profondeur': 0}, {'debut': 5, 'fin': 22, 'texte': 'qui commence nage', 'type': 'REL', 'role': 'qualite', 'niveau': 1, 'parent': 0, 'profondeur': 1}]}]
  ```

- **bash** `{"command": "sed -n '120,260p' tools/tests/linguistique/evaluer_gold.py", "description": "Read attachment evaluation"}`

  ```
bloc_langue = par_langue.get(langue, par_langue["fr"])
        for s in phrase["segments"]:
            cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
            if not cibles:
                continue
            att_n += 1
            bloc_langue["cibles"] += 1
            e = labels.get((s["type"], s["debut"], s["fin"]))
            if e is None:
                continue
            att_labels += 1
            bloc_langue["labels"] += 1
            att = (e.meta or {}).get("attachement") or {}
            cible = (att.get("cible") or "").strip()
            juste = cible == cibles[0]
            if juste:
                att_exact += 1
                bloc_langue["exact"] += 1
            # le gold admet parfois plusieurs cibles (43/96 GP) : mesure secondaire
            if cible in cibles:
                att_exact_any += 1
            # le gold mêle deux conventions : la cible est un verbe (le gouverneur) ou un nom
            # (l'antécédent d'un REL, la tête d'un GP). On mesure les deux séparément — en
            # suivant le **POS du gold** (plus fiable que le lexique : « poussent », « aboie »
            # y sont VERB), avec `_est_verbe` en repli si
… [6890 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/tests/linguistique/gold_split.py; echo ---; sed -n '1,80p' tools/tests/linguistique/gold.py", "description": "Read split and gold structure"}`

  ```
"""gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.

Le problème. Toutes les mesures de la session sont **in-sample** : les règles de segmentation et
d'attachement ont été dessinées en regardant les échecs du même gold qui les mesure. Pour juger
une règle, il faut un gold **tenu à l'écart** : on règle sur `dev`, on évalue sur `test`.

Protocole (fixé ici). Le split est un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` →
test, sinon dev), donc reproductible, insensible à l'ordre et indépendant du contenu. Il est
**stratifié par source** (`hand`, `reel`, `synthetique`) et par langue : on vérifie l'équilibre
dans la fiche. Aucune phrase n'est dupliquée entre les deux ; l'union redonne les 612.

Usage :
    from tools.tests.linguistique.gold_split import dev, test, compter
    ph = charger(); d = dev(ph); t = test(ph)
"""
from __future__ import annotations

import zlib

PART_TEST = 3  # une phrase sur trois va au test


def _est_test(phrase: dict) -> bool:
    return zlib.crc32(str(phrase.get("id", "")).encode()) % PART_TEST == 0


def dev(phrases: list[dict]) -> list[dict]:
    """Les phrases de développement (2/3)."""
    return [p for p in phr
… [6456 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ./tools/tests/linguistique/evaluer_gold.py --json /tmp/base.json 2>&1 | tail -20; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/base.json'))\nfor k in ['heuristique']:\n    for s in ['all','reel','hand','reel_new','synthetiq … [203 caractères tronqués]`

  ```
bash: line 1: ./tools/tests/linguistique/evaluer_gold.py: Permission denied
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/base.json'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/base.json >/tmp/base.log 2>&1; echo exit=$?; tail -5 /tmp/base.log; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/base.json'))\nfor s in ['all','reel','hand','reel … [250 caractères tronqués]`

  ```
exit=0
    "cibles": 238,
    "labels": 238,
    "top1": 237,
    "topk"
heuristique all: {"pos": {"exactitude": 0.8625, "exactitude_ferme": 0.9373, "exactitude_ouvert": 0.7918, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 65, "NOUN": 65, "VERB": 4}, "ADV": {"ADV": 131, "NOUN": 7, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 119, "?": 3, "NOUN": 1, "VERB": 1}, "CONJ": {"PRON": 15, "CONJ": 68, "?": 13, "PREP": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"PONCT": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 429, "?": 30, "CONJ": 2, "DET": 14}, "VERB": {"VERB": 546, "NOUN": 218, "PREP": 2, "ADJ": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.786, "rappel": 0.7944, "f1": 0.7902, "tp": 1480, "fp": 403, "fn": 383, "tete": {"precision": 0.9261, "rappel": 0.8808, "f1": 0.9029, "tp": 1641, "fp": 131, "fn": 222}}, "pragmatique": {"acte": 0.9967, "negation": 0.9771, "modalite": 0.9886, "double_sens": 0.9444}, "fraction_semantique": 0.5476}
all 0.7902 237 / 238 cibles 239
reel 0.7906 183 / 183 cibles 184
hand 0.9016 12 / 12 cibles 13
reel_new 0.7857 171 / 171 cibles 171
synthetique 0.7888 54 / 5
… [11 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys,json,collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nph=eg.charger()\nh=bl.Heuristique()\npat=collection … [1111 caractères tronqués]`

  ```
s065  fr 'elle qui commence nage'
   REL 5:17 'qui commence' prev=('GN', 'elle', 0, 4) next=('GV', 'nage', 18, 22) gold='elle' pred='nage' spanok=True
patterns Counter({('GN', 'GV'): 74})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"s065\" docs/ reports/ journal/ tools/ --include=*.md --include=*.json --include=*.py 2>/dev/null | grep -v gold_ | head -30", "description": "Find all docs mentions of s065"}`

  ```
docs/pilotage/chantiers.md:84:| **B — l'intelligence** | le sens, la logique, les jeux, les maîtres : que sait faire le système ? | ✅ B1–B12 ; B10.3 bloqué (encodeur) ; **B13** state store v0 + DRVF + **bloc linguistique** (POS **86,25 %**, F1 **0,7902**, attachement **237/238 (0,9958)**, 1 span + 1 cible) + **produit `drave`** (contrat v1) ; **183/183** portes | B10.3 (encodeur) ; **B13** : 1 span (`g017`) + 1 cible (`s065`) ; la coordination S/A/R/N2 | A, N1, D (corpus) | R (R5), S/L (sémantique, pragmatique) |
docs/pilotage/roadmap.md:38:**État au 07/11 18 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV** réglée (sujet hors du GV + adverbe final : GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **contrat v2 publié et validé** (`meta.partition`/`meta.alternative`, version 2, **v1 lue** : 26 cas, 0 échec) ; **restitution v0** (`restituer` : **46/46 surfaces exactes** sur les 50 textes libres, miroir strict **0,1087**, contrôle négatif **46/46** ; le miroir a trouvé les sauts de ligne, correctif `C` ; [fiche](../../reports/rappor
… [5232 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"REL\" docs/pilotage/backlog/ docs/theorie/lecture-rapide.md 2>/dev/null | head -30", "description": "Search backlog for REL rules"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '160,210p' reports/rapport-spans-v7.md; echo ===; sed -n '490,515p' reports/rapport-spans-v7.md; echo ===; sed -n '180,205p' reports/rapport-annotation-independante.md", "description": "Read prior s065 analyses"}`

  ```
|---|---|---|---|---|---|---|---|---|---|
| `r280` | dev | en | REL | 8:21 | « that I bought » | `that` | `car` | « The car that I bought runs. » | exact (R3a+R1/R2) |

#### SUB synthétique : verbe principal hors lexique → GN l'avale — 3 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `s044` | dev | fr | SUB | 17:29 | « que ils crie » | `que` | `nage` | « une fenêtre nage que ils crie » | absent (lexique disjoint) |
| `s112` | test | fr | SUB | 24:39 | « que Lucas ferme » | `que` | `nage` | « la brillante forêt nage que Lucas ferme » | absent (lexique disjoint) |
| `s114` | dev | fr | SUB | 22:43 | « que les avocat compte » | `que` | `dessine` | « ce doux nuage dessine que les avocat compte » | absent (lexique disjoint) |

#### REL synthétique : 2e verbe hors lexique disjoint — 6 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `s010` | dev | fr | REL | 10:18 | « qui nage » | `qui` | `chemin` | « un chemin qui nage prépare » | absent (lexique disjoint) |
| `s035` | test | fr | REL | 10:19 | « qui ferme » | `qui` | `papier` | 
… [5552 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '230,255p' reports/rapport-audit-r1r3.md; echo ===; sed -n '100,140p' reports/pensee-replis-cible.json", "description": "Read audit and replis context"}`

  ```
d'A17 (même ensemble, mêmes types) ; les 10 autres sont les 7 régressions et les 3 gains A17
non intégrés.

| id | lg | type | source | span | texte | cible | classe |
|---|---|---|---|---:|---|---|---|
| `r153` | en | GP | reel | 8:19 | « for the bus » | `wait` | A17 non intégré (R3b) |
| `r035` | en | REL | reel | 9:24 | « she talks about » | `film` | A17 hors périmètre (relative zéro) |
| `r255` | fr | REL | reel | 11:27 | « que j'ai achetée » | `voiture` | A17 hors périmètre (lexique réel) |
| `r264` | fr | SUB | reel | 8:26 | « qu'il vient demain » | `sais` | A17 hors périmètre (tokenisation) |
| `r288` | en | SUB | reel | 7:29 | « that he comes tomorrow » | `know` | A17 hors périmètre (adverbe final) |
| `s010` | fr | REL | synthetique | 10:18 | « qui nage » | `chemin` | A17 non récupérable (lexique) |
| `s035` | fr | REL | synthetique | 10:19 | « qui ferme » | `papier` | A17 non récupérable (lexique) |
| `s061` | fr | REL | synthetique | 9:18 | « qui saute » | `nuage` | A17 non récupérable (lexique) |
| `s065` | fr | REL | synthetique | 5:17 | « qui commence » | `elle` | A17 non récupérable (antécédent) |
| `s125` | fr | REL | synthetique | 11:21 | « qui compte » | `renard` 
… [1647 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"sujet du GV\\|sujet de GV\\|REL après\\|REL suivie\\|REL.*GV\" docs/ reports/ tools/ --include=*.md --include=*.py --include=*.json 2>/dev/null | grep -v \"gold_\" | head -40", "description": "Search docs for the proposed  … [14 caractères tronqués]`

  ```
docs/implantation/moteur-de-pensee.md:348:| **T176** | comment trancher REL/SUB ? | **le segment précédent** : après un GV → verbe, après un GN → antécédent ; +6 exact | dépend de la segmentation S |
docs/produit/README.md:110:GN Le livre → intéressant · REL que j'ai lu → livre · REL que j'ai lu est intéressant → livre · GV est intéressant → livre
reports/rapport-pensee-gold-linguistique.md:20:  GV (V, AUX+V, V+GN, V+GP, AUX+ADJ, ADV+V), GP, REL (`qui` + GV), SUB (`que` + GN + GV),
reports/rapport-pensee-cibles-500.md:25:  (GP, REL, SUB) et les relations **GN → GV**.
reports/pensee-attachement-cible.json:29: "regle": "REL/SUB → antécédent (tête du GN à gauche, élision séparée) ; GP → verbe du GV",
reports/pensee-contrat-s.json:251:  "regle_courante": "REL/SUB → segment précédent : GV → _verbe_dans (SUB), GN → _tete_nom (REL) ; puis _cible_proche ; GP → _cible_proche",
reports/rapport-pensee-attachement-v2.md:39:| 1 | **segment précédent** (SUB après GV → verbe ; REL après GN → antécédent) | **+6 exact** (s012, s030, s052, s097, s124, s139) | **A7** (annotation indépendante) |
reports/rapport-contrat-s.md:100:segment le plus proche à gauche, ce qui **n'est pas** la cible du gold (po
… [11334 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline --all -- tools/bloc_linguistique.py | head -30", "description": "Recent history of block file"}`

  ```
8eb0cc49 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE
9a259953 B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE
92652984 B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183
25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
efbae885 B13 — LE NOM PROPRE SUJET EST UN GN : F1 0,7438 → 0,7535, TÊTE 0,865, ATTACHEMENT 236/237 ; 183/183
295e0d7b B13 — LES PRONOMS SUJETS ANGLAIS AUSSI : F1 0,7013 → 0,7438, TÊTE 0,8561, ATTACHEMENT PRÉSERVÉ ; 183/183
c78a53bd B13 — LE PRONOM SUJET EST UN GN : F1 0,6519 → 0,7013 (+4,9), TÊTE 0,7709 → 0,8141, ATTACHEMENT PRÉSERVÉ (236/237, 0,9916) ; 183/183
5d2fa775 B13 — r264 RÉGLÉ : LE GV S'ARRÊTE AU MARQUEUR ÉLIDÉ (RADICAL qu), EXACT 236/237, COUVERTURE 0,9874 → 0,9916, F1 0,6519 ; 183/183
c43dd5cc B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183
6b976cb1 B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183
7a45325f B13 — LA PONCTUAT
… [2608 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '330,365p' docs/implantation/moteur-de-pensee.md; echo ===; sed -n '1,90p' reports/rapport-pensee-attachement-v2.md", "description": "Read T176 and attachment v2"}`

  ```
| **T158** | et sur les passifs ? | **5/5 faux** | le sujet est un patient, le `par` un agent |
| **T159** | le correctif suffit-il ? | `_role_gp(par)` = agent ; le generateur S court-circuite | correctif partiel |
| **T160** | les passifs sans `par` ? | chunker **3/3** patient, le S ignore | deux chemins |
| **T161** | la cible par proximité paie-t-elle ? | exact **0,0042 → 0,0544** (×13), top1 0,3975 | 226/239 restent faux |
| **T162** | les candidats verbes paient-ils ? | top-k **0,3264 → 0,4728**, tête **0,7793** | le classement n'est pas appris |
| **T163** | où échoue l'attachement ? | **43 span, 30 cible** (33 avant les correctifs) | le POS tague encore des verbes en noms |
| **T164** | le verbe du GV-phrase ? | **le POS VERB** : exact **0,0586 → 0,0962**, top1 0,4393 | 22 GP restants par le POS |
| **T165** | le lexique verbal arbitre-t-il ? | exact **0,0962 → 0,1381**, tête 0,9034 | 13 verbes hors lexique |
| **T166** | où sont les spans perdus ? | **21 REL, 17 SUB, 5 GP** (v7) | le découpage, plus la couverture |
| **T167** | quel dénominateur pour l'attachement ? | **rendement** (÷239) et **exactitude spans** (÷196) : **0,9949 / 0,8469 / 0,9949** | deux lectures, nommées
… [7888 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as eg\nph=eg.charger(); h=bl.Heuristique()\nn=0\nfor p in ph:\n    simples=h._synt … [799 caractères tronqués]`

  ```
total REL after GV in simples: 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as eg\nph=eg.charger(); h=bl.Heuristique()\nn=0\nfor p in ph:\n    if p['langue']! … [510 caractères tronqués]`

  ```
s037 'Paul qui marche marche' REL 5 22 'qui marche marche' prev GV 'Paul'
s141 'Emma qui trouve compte' REL 5 22 'qui trouve compte' prev GV 'Emma'
total REL after GV in S: 2
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^RACINE\" tools/bloc_linguistique.py; sed -n '1,60p' tools/bloc_linguistique.py; grep -n \"CONVENTION\" tools/tests/linguistique/gold_reel.py | head", "description": "Inspect module header and RACINE"}`

  ```
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
#!/usr/bin/env python3
"""bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.

Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :

  - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
  - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
    substitution et le parallèle sans GPU ;
  - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
    même type d'annotation ;
  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
  - `Parallele` et `Cascade` : les deux modes de composition. Le parallèle fusionne les
    étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
    que l'heuristique ne couvre pas.

La sortie est une **annotation typée** — pas le corps de la RSN : chaque étiquette porte son
`niveau`, son `sp
… [1399 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p /tmp/s065 && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib,re\nsrc=pathlib.Path('tools/bloc_linguistique.py').read_text()\nracine=str(pathlib.Path('.').resolve())\nsrc=src.replace('RACINE = pathlib.Path(__file__).resolve().parent.parent … [184 caractères tronqués]`

  ```
base copy 151931
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nbase=pathlib.Path('/tmp/s065/bloc_base.py').read_text()\n\nmethod = '''\n    @staticmethod\n    def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict]) -> str | None:\n        \"\"\"REL ** … [2528 caractères tronqués]`

  ```
regle written
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/tmp/s065/bloc_regle.py", line 58, in <module>
    @dataclass(frozen=True)
     ~~~~~~~~~^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/dataclasses.py", line 1344, in wrap
    return _process_class(cls, init, repr, eq, order, unsafe_hash,
                          frozen, match_args, kw_only, slots,
                          weakref_slot)
  File "/usr/lib64/python3.13/dataclasses.py", line 997, in _process_class
    and _is_type(type, cls, dataclasses, dataclasses.KW_ONLY,
        ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                 _is_kw_only))):
                 ^^^^^^^^^^^^
  File "/usr/lib64/python3.13/dataclasses.py", line 757, in _is_type
    ns = sys.modules.get(cls.__module__).__dict__
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute '__dict__'. Did you mean: '__dir__'?
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util\nsys.path.insert(0,'tools')\nfor name,path in [('bloc_regle','/tmp/s065/bloc_regle.py')]:\n    spec=importlib.util.spec_from_file_location(name,path)\n    m=importlib.util.module_from_spe … [336 caractères tronqués]`

  ```
GN 0 4 'elle' {'segment': 'elle', 'cible': 'nage'}
REL 5 17 'qui commence' {'segment': 'qui commence', 'cible': 'elle'}
REL 5 22 'qui commence nage' {'segment': 'qui commence nage', 'cible': 'elle'}
GV 18 22 'nage' None
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util, json, pathlib\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg\nimport gold_split as gs\n\ndef charger(nom,path):\n    spec=importlib … [1440 caractères tronqués]`

  ```
all          F1 0.7902 -> 0.7902  tp 1480->1480 fp 403->403 fn 383->383  att 237/238 -> 238/238 (cibles 239)
dev          F1 0.7875 -> 0.7875  tp 1019->1019 fp 273->273 fn 277->277  att 161/162 -> 162/162 (cibles 163)
test         F1 0.7962 -> 0.7962  tp 461->461 fp 130->130 fn 106->106  att 76/76 -> 76/76 (cibles 76)
hand         F1 0.9016 -> 0.9016  tp 55->55 fp 11->11 fn 1->1  att 12/12 -> 12/12 (cibles 13)
reel         F1 0.7857 -> 0.7857  tp 1100->1100 fp 255->255 fn 345->345  att 171/171 -> 171/171 (cibles 171)
synthetique  F1 0.7888 -> 0.7888  tp 325->325 fp 137->137 fn 37->37  att 54/55 -> 55/55 (cibles 55)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg\ndef charger(nom,path):\n    spec=importlib.util.spec_from_file_location … [1095 caractères tronqués]`

  ```
attachment diffs: 1
('s065', ('REL', 5, 17), 'nage', 'elle')
span/pos diffs: []
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '220,270p' tools/chantier/plan.json; echo ===; python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p.get('taches',p if isinstance(p,list) else []):\n    if isinstance(t,dict) and t.get('id', … [137 caractères tronqués]`

  ```
"attendu": "REVUE-0"
    }
   ]
  },
  {
   "id": "J6.1",
   "jour": 6,
   "titre": "Le dernier span g017",
   "mandat": "Tâche J6.1 : le dernier span du gold, `g017` (« She said that she would come yesterday. ») — le gold attend la SUB « that she would come » (sans « yesterday »), le bloc l'inclut. Reproduis, propose UNE règle mesurée (l'adverbe final de temps hors de la SUB), vérifie dev/test et l'attachement, fiche `reports/rapport-g017.md` + JSON, commit. Si la règle casse autre chose, écris la fiche du rejet.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-g017.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
    {
     "commande": "bash tools/porte-bloc-linguistique.sh 2>&1 | tail -1",
     "attendu": "verte"
    }
   ]
  },
  {
   "id": "J6.2",
   "jour": 6,
   "titre": "La cible s065",
   "mandat": "Tâche J6.2 : la cible `s065` (« elle nage qui commence » — le gold attend `elle`, le bloc prédit `nage`). Reproduis, propose une règle (REL après GV → le sujet du GV), mesure sur dev/test, fiche `reports/rapport-s065.md` + JSON, commit. Attachement à 238/239 si la règle tient.",
   "budget_min": 90,
   "acceptation": [
    {
    
… [2021 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,200p' tools/porte-bloc-linguistique.sh", "description": "Read block gate script"}`

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
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"237\\|0,7902\\|0.7902\\|238/239\\|237/238\" tools/ --include=*.py --include=*.sh --include=*.json 2>/dev/null | grep -v \"gold_gele\\|gold.json\\|pensee-\\|__pycache__\" | head -40", "description": "Find numeric assertions … [16 caractères tronqués]`

  ```
tools/essai_decharge.py:344:    Wikipedia complet porte 3 237 caractères distincts, donc un embedding de
tools/essai_decharge.py:345:    3 237 entrées coûterait plus cher que le reste du modèle, et une découpe en
tools/n4_dessin_b.py:79:#   modèle complet   : m32 7,4242 · m20 19,1237
tools/n4_dessin_b.py:82:REPERES_MOTEUR = {"complet": {"m32": 7.4242, "m20": 19.1237},
tools/jeux/mesure.py:338:         [44, 1486, 62379, 2103487]),
tools/jeux/tests/test_regles.py:35:             [44, 1486, 62379]),
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/uts46data.py:3127:        0x3237,
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/uts46data.py:7755:        0x1F237,
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/unistring.py:38:Mn = '\u0300-\u036f\u0483-\u0487\u0591-\u05bd\u05bf\u05c1-\u05c2\u05c4-\u05c5\u05c7\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06dc\u06df-\u06e4\u06e7-\u06e8\u06ea-\u06ed\u0711\u0730-\u074a\u07a6-\u07b0\u07eb-\u07f3\u07fd\u0816-\u0819\u081b-\u0823\u0825-\u0827\u0829-\u082d\u0859-\u085b\u08d3-\u08e1\u08e3-\u0902\u093a\u093c\u0941-\u0948\u094d\u0951-\u0957\u0962-\u0963\u0981\u09bc\u09c1-\u09c4\u09cd\u09e2-\u09
… [38438 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' tools/tests/linguistique/test_bloc_linguistique.py", "description": "Read block unit tests"}`

  ```
"""Tests du bloc linguistique — contrat, substitution, parallèle, cascade, activation."""
import json
import pathlib
import stat
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl

TEXTE = "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat !"


class TestBlocLinguistique(unittest.TestCase):
    def setUp(self):
        self.h = bl.Heuristique(segmenter_s=False)
        self.n = bl.MockNeuronal()

    def test_niveaux_et_spans(self):
        a = self.h.analyser(TEXTE, "fr")
        niveaux = {e.niveau for e in a.etiquettes}
        self.assertEqual(set(bl.NIVEAUX) - niveaux, set(), f"niveaux manquants : {set(bl.NIVEAUX)-niveaux}")
        for e in a.etiquettes:
            self.assertGreaterEqual(e.debut, 0)
            self.assertLessEqual(e.fin, len(TEXTE))
            self.assertLessEqual(e.debut, e.fin)

    def test_relative_zero(self):
        """Relative zéro : [GN] [pronom sujet] [verbe] [préposition orpheline] → REL.

        La règle est **structurelle** : elle ne dépend ni du nom, ni du pronom, ni du verbe,
        ni de la prépositi
… [6214 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as eg\nh=bl.Heuristique(); ph=eg.charger()\nfor pid in ['s010','s035','s061','s065 … [471 caractères tronqués]`

  ```
s010 'un chemin qui nage prépare'
  gold: [('GN', 0, 9, 'un chemin', None), ('REL', 10, 18, 'qui nage', 'chemin'), ('GV', 19, 26, 'prépare', None)]
  pred: [('GN', 0, 9, 'un chemin', 'prépare'), ('REL', 10, 18, 'qui nage', 'chemin'), ('REL', 10, 26, 'qui nage prépare', 'chemin'), ('GV', 19, 26, 'prépare', None)]
s035 'un papier qui ferme observe'
  gold: [('GN', 0, 9, 'un papier', None), ('REL', 10, 19, 'qui ferme', 'papier'), ('GV', 20, 27, 'observe', None)]
  pred: [('GN', 0, 9, 'un papier', 'observe'), ('REL', 10, 19, 'qui ferme', 'papier'), ('REL', 10, 27, 'qui ferme observe', 'papier'), ('GV', 20, 27, 'observe', None)]
s061 'ce nuage qui saute observe'
  gold: [('GN', 0, 8, 'ce nuage', None), ('REL', 9, 18, 'qui saute', 'nuage'), ('GV', 19, 26, 'observe', None)]
  pred: [('GN', 0, 8, 'ce nuage', 'observe'), ('REL', 9, 18, 'qui saute', 'nuage'), ('REL', 9, 26, 'qui saute observe', 'nuage'), ('GV', 19, 26, 'observe', None)]
s065 'elle qui commence nage'
  gold: [('GN', 0, 4, 'elle', None), ('REL', 5, 17, 'qui commence', 'elle'), ('GV', 18, 22, 'nage', None)]
  pred: [('GN', 0, 4, 'elle', 'nage'), ('REL', 5, 17, 'qui commence', 'nage'), ('REL', 5, 22, 'qui commence nage', 'elle')
… [1613 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor txt in ['un chemin qui nage prépare','elle qui commence nage','Emma qui trouve compte','mon renard qui compte crie']:\ … [254 caractères tronqués]`

  ```
'un chemin qui nage prépare'
  nom « qui nage prépare » → un chemin
    {'debut': 0, 'fin': 9, 'texte': 'un chemin', 'type': 'GN', 'role': 'agent', 'niveau': 0, 'parent': None, 'profondeur': 0}
    {'debut': 10, 'fin': 26, 'texte': 'qui nage prépare', 'type': 'REL', 'role': 'qualite', 'niveau': 1, 'parent': 0, 'profondeur': 1}
  simple: [{'type': 'GN', 'role': 'groupe nominal', 'niveau': 0, 'debut': 0, 'fin': 9, 'texte': 'un chemin', 'candidats': []}, {'type': 'REL', 'role': 'qualité', 'niveau': 1, 'debut': 10, 'fin': 18, 'texte': 'qui nage', 'candidats': []}, {'type': 'GV', 'role': 'prédicat', 'niveau': 0, 'debut': 19, 'fin': 26, 'texte': 'prépare', 'candidats': []}]
'elle qui commence nage'
  nom « qui commence nage » → elle
    {'debut': 0, 'fin': 4, 'texte': 'elle', 'type': 'GN', 'role': 'agent', 'niveau': 0, 'parent': None, 'profondeur': 0}
    {'debut': 5, 'fin': 22, 'texte': 'qui commence nage', 'type': 'REL', 'role': 'qualite', 'niveau': 1, 'parent': 0, 'profondeur': 1}
  simple: [{'type': 'REL', 'role': 'qualité', 'niveau': 1, 'debut': 5, 'fin': 17, 'texte': 'qui commence', 'candidats': []}, {'type': 'GV', 'role': 'prédicat', 'niveau': 0, 'debut': 18, 'fin': 22, 'texte': '
… [1254 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor txt in ['Emma qui trouve compte','Paul qui marche marche']:\n    print(repr(txt))\n    print(' simple:',h._syntagmes_s … [181 caractères tronqués]`

  ```
'Emma qui trouve compte'
 simple: [{'type': 'REL', 'role': 'qualité', 'niveau': 1, 'debut': 5, 'fin': 15, 'texte': 'qui trouve', 'candidats': []}, {'type': 'GV', 'role': 'prédicat', 'niveau': 0, 'debut': 16, 'fin': 22, 'texte': 'compte', 'candidats': []}]
 S: [{'nom': '« qui trouve compte » → Emma', 'lecture': '« qui trouve compte » se rattache à « Emma »', 'attachement': {'segment': 'qui trouve compte', 'cible': 'Emma', 'genre': 'GV'}, 'segments': [{'debut': 0, 'fin': 4, 'texte': 'Emma', 'type': 'GV', 'role': 'predicat', 'niveau': 0, 'parent': None, 'profondeur': 0}, {'debut': 5, 'fin': 22, 'texte': 'qui trouve compte', 'type': 'REL', 'role': 'qualite', 'niveau': 1, 'parent': 0, 'profondeur': 1}]}]
'Paul qui marche marche'
 simple: [{'type': 'REL', 'role': 'qualité', 'niveau': 1, 'debut': 5, 'fin': 15, 'texte': 'qui marche', 'candidats': []}, {'type': 'GV', 'role': 'prédicat', 'niveau': 0, 'debut': 16, 'fin': 22, 'texte': 'marche', 'candidats': []}]
 S: [{'nom': '« qui marche marche » → Paul', 'lecture': '« qui marche marche » se rattache à « Paul »', 'attachement': {'segment': 'qui marche marche', 'cible': 'Paul', 'genre': 'GV'}, 'segments': [{'debut': 0, 'fin': 4, 'texte': 'Paul
… [217 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\norig=h._syntagmes_simple\ndef wrap(texte,langue,pos_verbes=None):\n    r=orig(texte,langue,pos_verbes)\n    print('SIMPLE  … [422 caractères tronqués]`

  ```
===  Emma qui trouve compte
SIMPLE CALL 'Emma qui trouve compte' pos_verbes {9}
    {'type': 'REL', 'role': 'qualité', 'niveau': 1, 'debut': 5, 'fin': 15, 'texte': 'qui trouve', 'candidats': []}
    {'type': 'GV', 'role': 'prédicat', 'niveau': 0, 'debut': 16, 'fin': 22, 'texte': 'compte', 'candidats': []}
OUT GV 0 4 'Emma' None
OUT REL 5 15 'qui trouve' {'segment': 'qui trouve', 'cible': 'Emma'}
OUT REL 5 22 'qui trouve compte' {'segment': 'qui trouve compte', 'cible': 'Emma'}
OUT GV 16 22 'compte' None
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nbase=pathlib.Path('/tmp/s065/bloc_base.py').read_text()\nanchor='''    @staticmethod\n    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:'''\nold='''        … [5489 caractères tronqués]`

  ```
variants written
base
  all   F1 0.7902 tp 1480 fp 403 fn 383  att 237/238 cibles 239
  dev   F1 0.7875 tp 1019 fp 273 fn 277  att 161/162 cibles 163
  test  F1 0.7962 tp 461 fp 130 fn 106  att 76/76 cibles 76
regle
  all   F1 0.7902 tp 1480 fp 403 fn 383  att 238/238 cibles 239
  dev   F1 0.7875 tp 1019 fp 273 fn 277  att 162/162 cibles 163
  test  F1 0.7962 tp 461 fp 130 fn 106  att 76/76 cibles 76
rel_gn
  all   F1 0.7902 tp 1480 fp 403 fn 383  att 238/238 cibles 239
  dev   F1 0.7875 tp 1019 fp 273 fn 277  att 162/162 cibles 163
  test  F1 0.7962 tp 461 fp 130 fn 106  att 76/76 cibles 76
rel_apres_gv
  all   F1 0.7902 tp 1480 fp 403 fn 383  att 237/238 cibles 239
  dev   F1 0.7875 tp 1019 fp 273 fn 277  att 161/162 cibles 163
  test  F1 0.7962 tp 461 fp 130 fn 106  att 76/76 cibles 76
placebo
  all   F1 0.7902 tp 1480 fp 403 fn 383  att 235/238 cibles 239
  dev   F1 0.7875 tp 1019 fp 273 fn 277  att 160/162 cibles 163
  test  F1 0.7962 tp 461 fp 130 fn 106  att 75/76 cibles 76
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date -I; ls journal/ | tail -15; echo ---; sed -n '1,80p' docs/pilotage/en-cours.md", "description": "Check date and current state"}`

  ```
2026-11-14
2026-10-29
2026-10-30
2026-10-31
2026-11-01
2026-11-02
2026-11-03
2026-11-04
2026-11-05
2026-11-06
2026-11-07
2026-11-13
2026-11-14
README.md
sessions
THEMES.md
---
# En ce moment

**Mis à jour : 2026-11-14, 00 h 55 HNE (heure locale, EST).**

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
> `plan.md` (`python3 tools/sessions.py --status`)
… [4959 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,140p' docs/methode/resultats.md", "description": "Read result protocol"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal/2026-11-14/; echo ---; tail -80 journal/2026-11-14/*.md 2>/dev/null | head -120", "description": "Inspect today's journal"}`

  ```
docs.md
README.md
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/journal_auto.py | head -60; echo ---; ls journal/sessions/ | tail; grep -rn \"J6.1\\|J6.2\" journal/2026-11-14/ docs/pilotage/ 2>/dev/null | head", "description": "Check journal tooling and session links"}`

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
… [4386 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat journal/2026-11-14/README.md; echo ===; cat journal/2026-11-14/docs.md", "description": "Read today's journal content"}`

  ```
# 2026-11-14

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**1 commits** · **1 session(s)** · **1 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 1 | [docs.md](docs.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 320.3 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:52 | `b76b888a` | J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CONVENTION DU GOLD À TRANCHER |

## Le récit de la journée (écrit à la main)

<!-- notes -->
**J6.1 — g017 : la règle d
… [1994 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/toutes-les-portes.sh; echo ===; cat docs/pilotage/references-non-regression.md | head -80", "description": "Read gates runner and tolerated red list"}`

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
… [8296 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1010,1040p' tools/bloc_linguistique.py; echo ===; sed -n '1700,1730p' tools/bloc_linguistique.py", "description": "Read exact production lines before edit"}`

  ```
for s in base}
        except Exception:
            return {}

    @staticmethod
    def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
        """REL → tête du GN précédent ; SUB après un GV → son verbe (le gouverneur)."""
        if not precedent:
            return None
        if segment.get("type") == "REL" and precedent.get("type") == "GN":
            return Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
        if segment.get("type") == "SUB" and precedent.get("type") == "GV":
            if _est_adverbe_seul(precedent):
                return None
            return Heuristique._verbe_dans(texte, precedent["debut"], precedent["fin"], verbes)
        return None

    @staticmethod
    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:
        """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
        if not precedent:
            return []
        if segment.get("type") == "REL" and precedent.get("type") == "GN":
            tete = Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
            return [tete] if tet
… [2330 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1718,1750p' tools/bloc_linguistique.py", "description": "Read union branch exact lines"}`

  ```
# 5 bis. union : les segments du chunker que le générateur S ne fournit pas
        if cands and self.union:
            deja = {(s.get("type"), s.get("debut"), s.get("fin"))
                    for s in cands[0].get("segments", [])}
            gvs_u = ([x for x in cands[0].get("segments", []) if x.get("type") == "GV"]
                     + gvs_simple)
            prec = None
            for s in simples:
                if (s["type"], s["debut"], s["fin"]) in deja:
                    prec = s
                    continue
                meta = {"role": s["role"], "niveau": s["niveau"], "union": True}
                cible = (self._cible_precedent(texte, s, prec, verbes)
                         or self._repli_cible_gp(texte, s, [x for x in simples if x["type"] == "GN"])
                         or self._cible_proche(texte, s, gvs_u, verbes, cache_gv))
                cible = self._cible_hors_span(texte, s, gvs_u, cible)
                cible = self._repli_verbe_propre(texte, s, cible)
                if cible:
                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
                etiquettes.append(Etiquette("syntagme", s["type"], s["texte"], s["debut"
… [780 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "old_string": "    @staticmethod\n    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:", "new_string": "    @staticmethod\n    def _cible_rel_sujet(texte: str, segment … [1191 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 1012, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1012:             return {}
1013: 
1014:     @staticmethod
1015:     def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
1016:         """REL → tête du GN précédent ; SUB après un GV → son verbe (le gouverneur)."""
1017:         if not precedent:
1018:             return None
1019:         if segment.get("type") == "REL" and precedent.get("type") == "GN":
1020:             return Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
1021:         if segment.get("type") == "SUB" and precedent.get("type") == "GV":
1022:             if _est_adverbe_seul(precedent):
1023:                 return None
1024:             return Heuristique._verbe_dans(texte, precedent["debut"], precedent["fin"], verbes)
1025:         return None
1026: 
1027:     @staticmethod
1028:     def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:
1029:         """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
1030:         if not precedent:
1031:             return [
… [818 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "old_string": "    @staticmethod\n    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:", "new_string": "    @staticmethod\n    def _cible_rel_sujet(texte: str, segment … [1191 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 18, "offset": 1746}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1746:             prec = None
1747:             for s in simples:
1748:                 if (s["type"], s["debut"], s["fin"]) in deja:
1749:                     prec = s
1750:                     continue
1751:                 meta = {"role": s["role"], "niveau": s["niveau"], "union": True}
1752:                 cible = (self._cible_precedent(texte, s, prec, verbes)
1753:                          or self._repli_cible_gp(texte, s, [x for x in simples if x["type"] == "GN"])
1754:                          or self._cible_proche(texte, s, gvs_u, verbes, cache_gv))
1755:                 cible = self._cible_hors_span(texte, s, gvs_u, cible)
1756:                 cible = self._repli_verbe_propre(texte, s, cible)
1757:                 if cible:
1758:                     meta["attachement"] = {"segment": s["texte"], "cible": cible}
1759:                 etiquettes.append(Etiquette("syntagme", s["type"], s["texte"], s["debut"],
1760:                                             s["fin"], self.nom, 0.30,
1761:                                             candidats=([s["type"]]
1762:
… [260 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "                cible = (self._cible_precedent(texte, s, prec, verbes)\n                         or self._cible_rel_sujet(\n                             texte, s,\n                              … [525 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", "limit": 30, "offset": 24}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py</path>
<type>file</type>
<content>
24:         self.assertEqual(set(bl.NIVEAUX) - niveaux, set(), f"niveaux manquants : {set(bl.NIVEAUX)-niveaux}")
25:         for e in a.etiquettes:
26:             self.assertGreaterEqual(e.debut, 0)
27:             self.assertLessEqual(e.fin, len(TEXTE))
28:             self.assertLessEqual(e.debut, e.fin)
29: 
30:     def test_relative_zero(self):
31:         """Relative zéro : [GN] [pronom sujet] [verbe] [préposition orpheline] → REL.
32: 
33:         La règle est **structurelle** : elle ne dépend ni du nom, ni du pronom, ni du verbe,
34:         ni de la préposition. Une préposition avec complément, un adverbe ou l'absence de
35:         pronom ne déclenchent pas ; le français ne fabrique pas de relative zéro à
36:         préposition finale.
37:         """
38:         def syntagmes(txt, lg="en"):
39:             a = self.h.analyser(txt, lg)
40:             return [(e.type, e.debut, e.fin, txt[e.debut:e.fin],
41:                      ((e.meta or {}).get("attachement") or {}).get("cible"))
42:                     for e in a.etiquettes if e.
… [862 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", "limit": 18, "offset": 53}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py</path>
<type>file</type>
<content>
53:             self.assertFalse([s for s in syntagmes(txt) if s[0] == "REL"], txt)
54:         self.assertFalse([s for s in syntagmes("Le film elle parle est sorti.", "fr")
55:                           if s[0] == "REL"])
56: 
57:     def test_sujet_hors_du_gv(self):
58:         """La convention du gold : le sujet est un GN, le GV commence au prédicat.
59: 
60:         Le générateur S inclut le sujet ; on le déplace, sans le modifier. Les formes
61:         inversées (`Peux-tu`) et les clitiques (`s'ouvre`) sont couverts.
62:         """
63:         h = bl.Heuristique()
64: 
65:         def syntagmes(txt, lg="fr"):
66:             a = h.analyser(txt, lg)
67:             return [(e.type, txt[e.debut:e.fin]) for e in a.etiquettes
68:                     if e.niveau == "syntagme"]
69: 
70:         for phrase, gn, gv in (

(Showing lines 53-70 of 258. Use offset=71 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", "new_string": "        self.assertFalse([s for s in syntagmes(\"Le film elle parle est sorti.\", \"fr\")\n                          if s[0] == \"REL\"])\n\n    def test_rel_suivie_d_un … [1443 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m unittest tools.tests.linguistique.test_bloc_linguistique -v 2>&1 | tail -25", "description": "Run block unit tests"}`

  ```
test_cascade (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_cascade) ... ok
test_compose_pos_et_syntagmes (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_compose_pos_et_syntagmes) ... ok
test_langue_et_script (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_langue_et_script) ... ok
test_niveaux_et_spans (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_niveaux_et_spans) ... ok
test_parallele (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_parallele) ... ok
test_priorite_syntagme_confiance (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_priorite_syntagme_confiance) ... ok
test_refus (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_refus) ... ok
test_rejeu (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_rejeu) ... ok
test_rel_suivie_d_un_gv (tools.tests.linguistique.test_bloc_linguistique.TestBlocLinguistique.test_rel_suivie_d_un_gv)
REL suivie d'un GV : son antécédent est le **sujet de ce GV**. ... ok
test_relative_zero (tools.tests.linguistique.test_bloc_linguistique.TestB
… [1296 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/after.json >/tmp/after.log 2>&1; echo exit=$?; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/after.json'))\nfor s in ['all','reel','hand','reel_new','synthetique'] … [333 caractères tronqués]`

  ```
exit=0
all F1 0.7902 att 238 / 238 cibles 239 exact_taux_span 1.0 exact_taux 0.9958
reel F1 0.7906 att 183 / 183 cibles 184 exact_taux_span 1.0 exact_taux 0.9946
hand F1 0.9016 att 12 / 12 cibles 13 exact_taux_span 1.0 exact_taux 0.9231
reel_new F1 0.7857 att 171 / 171 cibles 171 exact_taux_span 1.0 exact_taux 1.0
synthetique F1 0.7888 att 55 / 55 cibles 55 exact_taux_span 1.0 exact_taux 1.0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-bloc-linguistique.sh 2>&1 | tail -8", "description": "Run block gate after integration"}`

  ```
"activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
✅ porte bloc linguistique verte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nb=json.load(open('/tmp/base.json')); a=json.load(open('/tmp/after.json'))\nfor key in ['heuristique']:\n    for s in ['all','reel','hand','reel_new','synthetique']:\n        mb,ma=b[key][s],a[key][s]\n … [179 caractères tronqués]`

  ```
all
  syntagme {'precision': 0.786, 'rappel': 0.7944, 'f1': 0.7902, 'tp': 1480, 'fp': 403, 'fn': 383, 'tete': {'precision': 0.9261, 'rappel': 0.8808, 'f1': 0.9029, 'tp': 1641, 'fp': 131, 'fn': 222}}
  attachement {'cibles': 239, 'labels': 238, 'top1': 237, 'topk': 236, 'exact': 237, 'top1_taux': 0.9916, 'topk_taux': 0.9874, 'exact_taux': 0.9916, 'exact_any': 237, 'exact_any_taux_span': 0.9958, 'top1_taux_span': 0.9958, 'topk_taux_span': 0.9916, 'topk_exact': 236, 'topk_exact_taux': 0.9874, 'topk_exact_taux_span': 0.9916, 'exact_taux_span': 0.9958, 'verbe': {'cibles': 158, 'justes': 158, 'taux': 1.0}, 'nom': {'cibles': 80, 'justes': 79, 'taux': 0.9875}, 'couverture': 0.9958, 'par_langue': {'fr': {'cibles': 151, 'labels': 151, 'exact': 150, 'topk': 149, 'exact_taux_span': 0.9934}, 'en': {'cibles': 88, 'labels': 87, 'exact': 87, 'topk': 87, 'exact_taux_span': 1.0}}}
  -> {'cibles': 239, 'labels': 238, 'top1': 238, 'topk': 236, 'exact': 238, 'top1_taux': 0.9958, 'topk_taux': 0.9874, 'exact_taux': 0.9958, 'exact_any': 238, 'exact_any_taux_span': 1.0, 'top1_taux_span': 1.0, 'topk_taux_span': 0.9916, 'topk_exact': 236, 'topk_exact_taux': 0.9874, 'topk_exact_taux_span': 0.9916, 'exact_taux
… [6262 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/s065/mesure.py <<'PY'\n\"\"\"Mesure J6.2 — la cible s065. Base = copie du bloc avant règle ; règle = production.\"\"\"\nimport importlib.util, json, sys, pathlib\nRACINE = pathlib.Path('/home/stephane/Data13TB/stephane/Git … [2933 caractères tronqués]`

  ```
{
 "all": {
  "cibles": 239,
  "labels": 238,
  "exact": 238,
  "top1": 238,
  "exact_taux_span": 1.0,
  "exact_taux": 0.9958,
  "couverture": 0.9958
 },
 "dev": {
  "cibles": 163,
  "labels": 162,
  "exact": 162,
  "top1": 162,
  "exact_taux_span": 1.0,
  "exact_taux": 0.9939,
  "couverture": 0.9939
 },
 "test": {
  "cibles": 76,
  "labels": 76,
  "exact": 76,
  "top1": 76,
  "exact_taux_span": 1.0,
  "exact_taux": 1.0,
  "couverture": 1.0
 }
}
diffs [{'id': 's065', 'segment': ['REL', 5, 17], 'avant': 'nage', 'apres': 'elle'}]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/s065/mesure-finale.json'))\nprint(json.dumps(d['corpus'],ensure_ascii=False,indent=1))\nfor nom in d['variantes']:\n    print('\\n==',nom)\n    for split in ['all','dev','test',' … [452 caractères tronqués]`

  ```
{
 "phrases": 612,
 "cibles": 239,
 "split": {
  "dev": {
   "phrases": 422,
   "cibles": 163,
   "sources": {
    "hand": 15,
    "reel": 302,
    "synthetique": 105
   },
   "langues": {
    "fr": 277,
    "en": 145
   }
  },
  "test": {
   "phrases": 190,
   "cibles": 76,
   "sources": {
    "hand": 5,
    "reel": 130,
    "synthetique": 55
   },
   "langues": {
    "fr": 125,
    "en": 65
   }
  }
 }
}

== base
all          F1 0.7902 tp 1480 fp 403 fn 383 pos 0.8625 att 237/238 cibles 239 span 0.9958 taux 0.9916
dev          F1 0.7875 tp 1019 fp 273 fn 277 pos 0.8618 att 161/162 cibles 163 span 0.9938 taux 0.9877
test         F1 0.7962 tp 461 fp 130 fn 106 pos 0.8642 att 76/76 cibles 76 span 1.0 taux 1.0
hand         F1 0.9016 tp 55 fp 11 fn 1 pos 0.8857 att 12/12 cibles 13 span 1.0 taux 0.9231
reel         F1 0.7857 tp 1100 fp 255 fn 345 pos 0.8893 att 171/171 cibles 171 span 1.0 taux 1.0
synthetique  F1 0.7888 tp 325 fp 137 fn 37 pos 0.7682 att 54/55 cibles 55 span 0.9818 taux 0.9818

== regle
all          F1 0.7902 tp 1480 fp 403 fn 383 pos 0.8625 att 238/238 cibles 239 span 1.0 taux 0.9958
dev          F1 0.7875 tp 1019 fp 273 fn 277 pos 0.8618 att 162/162 cibles 163 span 1
… [2199 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nfor f in ['/tmp/base.json','/tmp/after.json']:\n    d=json.load(open(f)); print(f, d.get('attachement_hasard'), d.get('gold'))\nEOF", "description": "Get random control and gold counts"}`

  ```
/tmp/base.json {'cibles': 239, 'top1_taux': 0.0042} {'phrases': 612, 'reel': 452, 'hand': 20, 'reel_new': 432, 'synthetique': 160, 'tokens': 3179}
/tmp/after.json {'cibles': 239, 'top1_taux': 0.0042} {'phrases': 612, 'reel': 452, 'hand': 20, 'reel_new': 432, 'synthetique': 160, 'tokens': 3179}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\nM=json.load(open('/tmp/s065/mesure-finale.json'))\nV=M['variantes']\n\ndef pick(v):\n    return {\n      'phrases': v['phrases'],\n      'pos_exactitude': v['pos'],\n      'syntagme': v['synta … [8831 caractères tronqués]`

  ```
written 14814
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-s065.json'))\nfor split in ['all','dev','test','hand','reel','synthetique']:\n    print(split)\n    for nom in ['base','regle']:\n        v=d['mesures'][nom][split]\n   … [395 caractères tronqués]`

  ```
all
  base: P 0.786 R 0.7944 F1 0.7902 tp 1480 fp 403 fn 383 | pos 0.8625 | att 237/238 cibles 239 span 0.9958 taux 0.9916 couv 0.9958 | tete 0.9029
  regle: P 0.786 R 0.7944 F1 0.7902 tp 1480 fp 403 fn 383 | pos 0.8625 | att 238/238 cibles 239 span 1.0 taux 0.9958 couv 0.9958 | tete 0.9029
dev
  base: P 0.7887 R 0.7863 F1 0.7875 tp 1019 fp 273 fn 277 | pos 0.8618 | att 161/162 cibles 163 span 0.9938 taux 0.9877 couv 0.9939 | tete 0.9019
  regle: P 0.7887 R 0.7863 F1 0.7875 tp 1019 fp 273 fn 277 | pos 0.8618 | att 162/162 cibles 163 span 1.0 taux 0.9939 couv 0.9939 | tete 0.9019
test
  base: P 0.78 R 0.8131 F1 0.7962 tp 461 fp 130 fn 106 | pos 0.8642 | att 76/76 cibles 76 span 1.0 taux 1.0 couv 1.0 | tete 0.9052
  regle: P 0.78 R 0.8131 F1 0.7962 tp 461 fp 130 fn 106 | pos 0.8642 | att 76/76 cibles 76 span 1.0 taux 1.0 couv 1.0 | tete 0.9052
hand
  base: P 0.8333 R 0.9821 F1 0.9016 tp 55 fp 11 fn 1 | pos 0.8857 | att 12/12 cibles 13 span 1.0 taux 0.9231 couv 0.9231 | tete 0.9739
  regle: P 0.8333 R 0.9821 F1 0.9016 tp 55 fp 11 fn 1 | pos 0.8857 | att 12/12 cibles 13 span 1.0 taux 0.9231 couv 0.9231 | tete 0.9739
reel
  base: P 0.8118 R 0.7612 F1 0.7857 tp 1100 fp 255 fn 345 | pos 0
… [492 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > reports/rapport-s065.md <<'MD'\n# B13 — s065 : la REL « qui commence » est attachée au sujet du GV qui la suit\n\n> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.2 · **Date** : 2026-11-14 ·\n> **Verdict** : … [10924 caractères tronqués]`

  ```
188 reports/rapport-s065.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '56,70p' docs/pilotage/en-cours.md; echo ===; sed -n '86,94p' docs/pilotage/en-cours.md; echo ===; sed -n '112,128p' docs/pilotage/en-cours.md", "description": "Read en-cours sections to edit"}`

  ```
- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13, bloc linguistique.
- **Stratégie** : v0 mesuré.
- **Ambition** : un runtime cognitif tracé.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (adverbe final hors SUB : g017 gagné, r264/r288 perdus ; test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v0** (46/46, miroir 0,1087) ; **contrat v1**, **`drave` v0**.
- **Ce qu'elle fait** : l'API rejoue le gold (mêmes verdicts).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Prochaine action** : **trancher la convention d'adverbe (`g017`)** ; puis **`s065`** (J6.2), T132/T133, gold 200+.
- **Sous-agents** : 4 mandats, [plan-travail](plan-travail.md) § 9.
- **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**.
- **Journal** : [la session](../../journal/session
… [3944 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '32,44p' docs/pilotage/roadmap.md; echo ===; sed -n '78,88p' docs/pilotage/chantiers.md; echo ===; sed -n '168,182p' docs/pilotage/semaine-autonome.md", "description": "Read roadmap and related sections"}`

  ```
| **N — le natif** | DRVM, `drave-n0`, [distillation](../theorie/glossaire/entrees/distillation.md), usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; **N0.1 6/6** ; N2.h : 3,0904 domaine, 3,85 hors dépôt ; **N2.ac (1 Go) : 3,49 / 6,03 / 8,34 — production** ; **200 k pas : val_fr 3,16, littérature 5,61, anglais 7,28, wikitext2 8,00** ; **fenêtre 1 024 : 2,4759 / 2,4373 au grand corpus — sous 2,5** ; porte propre **2,7856** ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 partiel | **N2** : **clôturée** le 03/11 11 h 25, la **fenêtre est la recette de production** ; **paire propre de distillation** (04/11) ; puis la **porte propre (0,29)** ; **N4** |
| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2 mesurées** (RoPE 
… [10529 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '182,230p' docs/pilotage/semaine-autonome.md", "description": "Read rest of autonomous week plan"}`

  ```
| **J4** | matin : coordination N2 / S / R | ✅ fiches (13/11) | N2 **8,0225 → 2,9726 / 2,7856** ; S **11 verdicts** (7 acceptés / 4 exclus) ; R **0,8625 → 0,9475 (+8,49)** | `commit J5.1` | appliquer N2, committer S + pointeur, route R + split tenu |
| **J4** | après-midi : coordination A | ✅ fiche (13/11) | A6.2 **libre** (MoE 18,56 Go, PPL **37,2013**, porte **54,5202**) ; A8.3b2 libre hors graphe | `commit J5.1` | rapport A6.2, harnais A8.3b2, D1–D8 |
| **J5** | matin : rapport de semaine | ✅ fait (13/11) | [`rapport-semaine.md`](../../reports/rapport-semaine.md) + JSON : chiffres, décisions, rejets, reste | `commit J5.1` | — |
| **J5** | après-midi : passe, tag, release | ⏳ à faire | — | — | `toutes-les-portes.sh`, `revue_documentation.py`, tag annoté |

**Ce que la semaine a produit.** Le **produit** : `r035` tranché (237/238, 0,9958), la convention
des GV (F1 **0,7902**), le schéma v2 (26 cas / 0 échec, v1 lue), la restitution v0 (46/46
surfaces, miroir **0,1087**). Le **tagger** : 0,9475 (+8,49 pts), décision **intégrer**, réserve
sur le réel 432 (+4,67). L'**intégration** : table 14/14, corpus 418/438, retrieval à script
dominant, généalogie à deux faces. La **coordination*
… [538 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Get current date/time"}`

  ```
2026-11-14 01:05 EST
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Mis à jour\" docs/pilotage/en-cours.md | head", "description": "Find state timestamp"}`

  ```
3:**Mis à jour : 2026-11-14, 00 h 55 HNE (heure locale, EST).**
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 8, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-14, 00 h 55 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11

(Showing lines 1-8 of 142. Use offset=9 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-14, 00 h 55 HNE (heure locale, EST).**", "new_string": "**Mis à jour : 2026-11-14, 01 h 10 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejeté … [766 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Prochaine action** : **trancher la convention d'adverbe (`g017`)** ; puis **`s065`** (J6.2), T132/T133, gold 200+.", "new_string": "- **Prochaine action** : **trancher la convention d'adverb … [43 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432, pragmatique 130/432 ; **`r035`** (237/238) ; **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (adverbe final hors SUB, test −0,0028  … [722 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 et convention des GV (0,7902, 237/238), J6.1 rejeté (convention d'adverbe à trancher … [554 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**N2** — porte (0,2856 val / 0,3566 test) ; **Pensée** — convention d'adverbe `g017`, `s065`, T132/T133, gold 200+ ; **J3.2** — **V14 des 21 langues** ; **S** — 11 verdicts + pointeur ; **R0.7** … [386 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 4, "offset": 36}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md", "limit": 4, "offset": 82}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
36: | **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**) ; **PDF** (1 927 doc., 322 Mo) ; **documents** (3 384 doc., 872 M car., 8 Ko 2,07 %) ; **OCR** (20 livres, 7 381 p, 15,36 M, 8 Ko 0 ; [CEGEP](../theorie/glossaire/entrees/cegep.md) **91 scans uniques**, 60 documents, 1 982 p, 4,41 M car., 8 Ko 0) ; **genres** mesurés | **l'OCR est clos** (limite : 8 scans `.PDF`, 58 p) ; la préparation **R1.1/R1.2** (N2) et **A2.6** (A) |
37: 
38: **État au 07/11 18 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV** réglée (sujet hors du GV + adverbe final : GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **contrat v2 publié et validé** (`meta.partition`/`meta.alternative`, version 2, **v1 lue** : 26 cas, 0 échec) ; **restitution v0** (`restituer` : **4
… [721 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md</path>
<type>file</type>
<content>
82: |---|---|---|---|---|---|
83: | **A — le moteur** | un flux de blocs typés peut-il tourner, se placer, se répartir, se rejouer ? | ✅ A1–A8 ; A3.4, A5.4, A6.2 bloqués ; A2.6 partiel ; A8.3 expliqué | **A2.6** (experts, A6.2 bloqué) ; réduire le lot | — | N, B (exécution) |
84: | **B — l'intelligence** | le sens, la logique, les jeux, les maîtres : que sait faire le système ? | ✅ B1–B12 ; B10.3 bloqué (encodeur) ; **B13** state store v0 + DRVF + **bloc linguistique** (POS **86,25 %**, F1 **0,7902**, attachement **237/238 (0,9958)**, 1 span + 1 cible) + **produit `drave`** (contrat v1) ; **183/183** portes | B10.3 (encodeur) ; **B13** : 1 span (`g017`) + 1 cible (`s065`) ; la coordination S/A/R/N2 | A, N1, D (corpus) | R (R5), S/L (sémantique, pragmatique) |
85: | **N — le natif** | le modèle natif peut-il être petit, creux, honnête et général ? | 🔬 N0/N1 mesurés ; **N0.1 6/6** (payload corrompu refusé) ; N2.h : 3,09 en domaine, 16,70 → 3,85 hors dépôt ; N4 partiel | **N2** (français réel, capacité) ; N4 (consigne) | A (moteur), D (corpus) | R1–R3, N5 |

(Showing lin
… [55 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**État au 14/11 01 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le suj … [1977 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md", "new_string": "| **B — l'intelligence** | le sens, la logique, les jeux, les maîtres : que sait faire le système ? | ✅ B1–B12 ; B10.3 bloqué (encodeur) ; **B13** state store v0 + DRVF + **bloc linguistique**  … [797 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md", "limit": 20, "offset": 26}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md</path>
<type>file</type>
<content>
26: | 00:52 | `b76b888a` | J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CONVENTION DU GOLD À TRANCHER |
27: 
28: ## Le récit de la journée (écrit à la main)
29: 
30: <!-- notes -->
31: **J6.1 — g017 : la règle de l'adverbe final hors de la SUB est rejetée.** Le bloc inclut
32: `yesterday` dans la SUB de `g017` (span 9:38 au lieu de 9:28). La règle demandée corrige
33: `g017` et retire un faux positif de `g005`, mais casse `r264` (« qu'il vient demain ») et
34: `r288` (« that he comes tomorrow ») : F1 **0,7902 → 0,7901**, dev **+0,0011**, test
35: **−0,0028**, attachement **237/238 → 236/237**. Les deux cas favorables sont en **dev**, les
36: deux défavorables en **test**. Rejet ; la convention du gold (inclure ou exclure l'adverbe
37: final) doit être tranchée avant toute règle. Fiche [`reports/rapport-g017.md`](../../reports/rapport-g017.md),
38: JSON [`reports/pensee-g017.json`](../../reports/pensee-g017.json).
39: <!-- /notes -->

(End of file - total 
… [20 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md", "new_string": "JSON [`reports/pensee-g017.json`](../../reports/pensee-g017.json).\n\n**J6.2 — s065 : la REL « qui commence » prend le sujet du GV qui la suit.** Le gold attend\n`elle`, le bloc prédisait `na … [752 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo \"exit=$?\"", "description": "Check state document"}`

  ```
en-cours · 1652 mots · 7 sections · 4 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -25; echo \"exit=$?\"", "description": "Check document size budget"}`

  ```
7369    385   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2661    199   T1   2800  reports/README.md
    2404    162   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materie
… [441 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py 2>&1 | tail -25; echo \"exit=$?\"", "description": "Check journal document"}`

  ```
journal · 46 jour(s) · 180 session(s) · 2431 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -15; echo \"exit=$?\"", "description": "Check markdown tables"}`

  ```
✅ 1782 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3952 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | head -40; echo \"exit=${PIPESTATUS[0]}\"", "description": "Inspect T0 breakdown"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    7369    385   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2661    199   T1   2800  reports/README.md
    2404    162   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [526 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '63p' docs/pilotage/en-cours.md | wc -w; sed -n '90p' docs/pilotage/en-cours.md | wc -w; sed -n '116p' docs/pilotage/en-cours.md | wc -w", "description": "Word count of edited lines"}`

  ```
78
63
59
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 2, "offset": 63}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
63: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du GV : 238/238, 0 span, 0 POS ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (adverbe final hors SUB : g017 gagné, r264/r288 perdus ; test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v0** (46/46, miroir 0,1087) ; **contrat v1**, **`drave` v0**.
64: - **Ce qu'elle fait** : l'API rejoue le gold (mêmes verdicts).

(Showing lines 63-64 of 142. Use offset=65 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** ([fiche](../../reports/rapport-s065 … [785 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep -E \"T0|violation|✅|❌\" | tail -6; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3", "description": "Recheck T0 and state"}`

  ```
T0 max : 3996 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
exit=0
  en-cours · 1626 mots · 7 sections · 4 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -60; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run documentation review"}`

  ```
revue de documentation · 720 fiche(s) · 814 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 719 fichiers, le disque en a 720
     · compteurs : en-cours.md dit 813 JSON, le disque en a 814
exit=1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"719\\|813\" docs/pilotage/en-cours.md", "description": "Find counter line"}`

  ```
104:| fichiers / JSON de résultats | **719** / **813** | `reports/*.md` / `reports/*.json` |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 4, "offset": 102}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
102: | portes | **84** (dont `porte-produit` le 07/11) | `tools/porte-*.sh` |
103: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
104: | fichiers / JSON de résultats | **719** / **813** | `reports/*.md` / `reports/*.json` |
105: | documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |

(Showing lines 102-105 of 142. Use offset=106 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **720** / **814** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **719** / **813** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -20; echo \"exit=${PIPESTATUS[0]}\"", "description": "Rerun documentation review"}`

  ```
revue de documentation · 720 fiche(s) · 814 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -40; echo ===; git diff --stat", "description": "Review working tree changes"}`

  ```
M docs/pilotage/chantiers.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/references-non-regression.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-14/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/bloc_linguistique.py
 M tools/chantier/plan.json
 m tools/structures
 M tools/tests/linguistique/test_bloc_linguistique.py
?? reports/pensee-s065.json
?? reports/rapport-s-paragraphes.md
?? reports/rapport-s065.md
===
 docs/pilotage/chantiers.md                         |   2 +-
 docs/pilotage/en-cours.md                          |  14 +-
 docs/pilotage/references-non-regression.md         |   2 +-
 docs/pilotage/roadmap.md                           |   2 +-
 journal/2026-11-14/README.md                       |  10 +
 reports/pensee-coherence-fiches-v7.json            |  19 +
 reports/pensee-dev-test-v10.json                   |   2 +-
 reports/pensee-quatre-modes.json                   | 734 ++++++++++++---------
 reports/rap
… [588 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/pilotage/references-non-regression.md | head -40; echo ===; git diff -- reports/rapport-dev-test-v10.md reports/pensee-dev-test-v10.json | head -40", "description": "Inspect unrelated diffs"}`

  ```
diff --git a/docs/pilotage/references-non-regression.md b/docs/pilotage/references-non-regression.md
index 1e1f58b8..d99dd15d 100644
--- a/docs/pilotage/references-non-regression.md
+++ b/docs/pilotage/references-non-regression.md
@@ -46,7 +46,7 @@
 | quoi | commande | attendu |
 |---|---|---|
 | tests unitaires | `cargo test --release` (dans `drave-core/`) | **138 tests** (le compte est dans la sortie) |
-| toutes les portes | `tools/toutes-les-portes.sh` | **83 portes** ; dernière passe **79 vertes, 4 rouges** (04/11 23 h 43 → 05/11 02 h 12, machine au repos) : 2 connues (`indice`, `melange`), 1 **corrigée** (`lecteur`, ancre du banc), 1 de **coordination** (`sessions`, heartbeat de `e181ce02`) · ⚠ **ne jamais lire une porte à travers un `tail`** |
+| toutes les portes | `tools/toutes-les-portes.sh` | **84 portes** ; voir la **passe du 07/11** ci-dessus · ⚠ **ne jamais lire une porte à travers un `tail`** |
 | une porte | `tools/porte-<nom>.sh` | la dernière ligne dit ce qu'elle verrouille |
 
 > **16/10 — l'audit des 46 portes** (deux vrais défauts corrigés, des faux positifs
===
diff --git a/reports/pensee-dev-test-v10.json b/reports/pensee-dev-test-v10.json
index 29223569..fd8
… [2295 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- tools/chantier/plan.json | head -80", "description": "Inspect plan.json diff"}`

  ```
diff --git a/tools/chantier/plan.json b/tools/chantier/plan.json
index 21ea0cf4..b1ece0d6 100644
--- a/tools/chantier/plan.json
+++ b/tools/chantier/plan.json
@@ -306,6 +306,122 @@
      "attendu": "FICHE-OK"
     }
    ]
+  },
+  {
+   "id": "J11.1",
+   "jour": 11,
+   "titre": "Le produit — les exemples rejoués",
+   "mandat": "Tâche J11.1 : les exemples de la doc produit — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (F1 0,7902, 237/238, le schéma v2) et corrige les sorties qui ont bougé ; fiche `reports/rapport-exemples-rejoues.md` + JSON, commit.",
+   "budget_min": 90,
+   "acceptation": [
+    {
+     "commande": "test -f reports/rapport-exemples-rejoues.md && echo FICHE-OK",
+     "attendu": "FICHE-OK"
+    },
+    {
+     "commande": "bash tools/porte-produit.sh 2>&1 | tail -1",
+     "attendu": "verte"
+    }
+   ]
+  },
+  {
+   "id": "J11.2",
+   "jour": 11,
+   "titre": "Le produit — la mesure par langue",
+   "mandat": "Tâche J11.2 : ajouter `evaluer --par-langue` (le détail fr/en) et le documenter dans `docs/produit/README.md` ; test dans `tools/tests/test_produit.py` ; fiche `reports/rapport-evaluer-langue.md` + JSON, commit.",
+   "budget_
… [1962 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/hooks/ | grep -v sample; echo ---; sed -n '1,120p' tools/verifie_etat_a_jour.py 2>/dev/null | head -80", "description": "Inspect pre-commit hook"}`

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
… [2103 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/chantiers.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-14/README.md reports/pensee-s065.json reports/rapport-s065.md tools/bloc_linguistique.py tools/tests/linguistique/test_bloc_linguis … [123 caractères tronqués]`

  ```
docs/pilotage/chantiers.md                         |   2 +-
 docs/pilotage/en-cours.md                          |  14 +-
 docs/pilotage/roadmap.md                           |   2 +-
 journal/2026-11-14/README.md                       |  10 +
 reports/pensee-s065.json                           | 791 +++++++++++++++++++++
 reports/rapport-s065.md                            | 188 +++++
 tools/bloc_linguistique.py                         |  25 +
 tools/tests/linguistique/test_bloc_linguistique.py |  22 +
 8 files changed, 1045 insertions(+), 9 deletions(-)
===
docs/pilotage/chantiers.md
docs/pilotage/en-cours.md
docs/pilotage/roadmap.md
journal/2026-11-14/README.md
reports/pensee-s065.json
reports/rapport-s065.md
tools/bloc_linguistique.py
tools/tests/linguistique/test_bloc_linguistique.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - <<'MSG'\nJ6.2 — s065 : LA REL SUIVIE D'UN GV PREND LE SUJET DU GV (238/238 LABELS, 238/239 CIBLES, F1 0,7902 INCHANGÉ, 0 SPAN, 0 POS)\n\nLe gold « elle qui commence nage » attend `elle` pour la REL 5:17 ; le bloc préd … [831 caractères tronqués]`
