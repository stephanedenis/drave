# Session DSH — relecture

- identifiant : `session-d58794d6-d201-493e-b6ab-fffee9656e15`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 03:18:05
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J9.1 : la passe d'honnêteté — les fiches qui publient des chiffres dépassés (POS 85, F1 0,7535, 236/237, 2 spans) doivent porter « instantané historique » avec le lien vers l'état courant. Écris `reports/rapport-passe-honnetete.md` + JSON, applique la mention aux fiches concernées, commit.

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

- **bash** `{"command": "pwd && ls && git status --short | head -50 && git log --oneline -5", "description": "Inspect repo state and recent commits"}`

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
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/2026-11-14/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-02ebc573-ec84-46cf-945c-cfd7d563a9fc/digest.md
 M journal/sessions/session-02ebc573-ec84-46cf-945c-cfd7d563a9fc/rapport.md
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
 M tools/chantier/plan.json
 M t
… [956 caractères tronqués]
  ```

- **bash** `{"command": "ls reports | head -60 && echo '---' && ls reports | wc -l", "description": "List reports directory"}`

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
… [47 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"J9.1\\|passe d'honnêteté\\|passe-honnetete\\|instantané historique\" --include=\"*.md\" --include=\"*.json\" docs reports tools journal | head -50", "description": "Search for task J9.1 and related terms"}`

  ```
docs/pilotage/semaine-autonome.md:114:   « instantané historique ».
reports/rapport-coherence-fiches-v7.md:254:commit X, ne décrit pas l'état courant ». La v2 est appelée « instantané historique » dans
reports/pensee-audit-v10.json:65:   "fiche_v10": "rapport-pensee-v10.md a été corrigée dans 653a7981 (instantané historique) ; les citations et écarts de ce rapport portent sur la version du commit 710ec7f9."
reports/rapport-audit-v10.md:64:(elle se présente désormais comme un « instantané historique ») ; les citations de ce rapport
tools/chantier/plan.json:281:   "id": "J9.1",
tools/chantier/plan.json:283:   "titre": "La passe d'honnêteté des fiches",
tools/chantier/plan.json:284:   "mandat": "Tâche J9.1 : la passe d'honnêteté — les fiches qui publient des chiffres dépassés (POS 85, F1 0,7535, 236/237, 2 spans) doivent porter « instantané historique » avec le lien vers l'état courant. Écris `reports/rapport-passe-honnetete.md` + JSON, applique la mention aux fiches concernées, commit.",
tools/chantier/plan.json:288:     "commande": "test -f reports/rapport-passe-honnetete.md && echo FICHE-OK",
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:46114:commit X, ne décrit 
… [951 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/chantier/plan.json 2>/dev/null | head -100", "description": "Inspect chantier plan"}`

  ```
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
   "id": "J1.1",
   "jour": 1,
   "titre": "r035 : la relative zéro",
   "mandat": "Tâche J1.1 du chantier : la relative zéro (r035, « The film she talks about is out. »). Reproduis, explique, propose UNE règle générale mesurée sur dev/test ; si elle tient (attachement 236→237, POS/F1 stables), intègre-la et commite avec une fiche `reports/rapport-r035.md` + `reports/pensee-r035.json`. Sinon, écris la fiche du rejet (chiffres, raison) et commite-la. Règles : ne touche pas S/D/N2 ; 183/183 portes ; en-cours à jour.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-r035.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
   
… [2968 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if t['id'].startswith('J9'):\n        print(json.dumps(t, ensure_ascii=False, indent=1))\nEOF", "description": "Show J9 tasks from plan"}`

  ```
{
 "id": "J9.1",
 "jour": 9,
 "titre": "La passe d'honnêteté des fiches",
 "mandat": "Tâche J9.1 : la passe d'honnêteté — les fiches qui publient des chiffres dépassés (POS 85, F1 0,7535, 236/237, 2 spans) doivent porter « instantané historique » avec le lien vers l'état courant. Écris `reports/rapport-passe-honnetete.md` + JSON, applique la mention aux fiches concernées, commit.",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-passe-honnetete.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  },
  {
   "commande": "python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?",
   "attendu": "REVUE-0"
  }
 ]
}
  ```

- **bash** `{"command": "sed -n '80,140p' docs/pilotage/semaine-autonome.md", "description": "Read honesty pass context"}`

  ```
**Chaque vague** : 2 à 4 sous-agents, un **résultat mesuré**, un **contrôle négatif**, une **fiche**
+ son **JSON**, la mise à jour de l'**état**, un **commit vérifié** par l'agent principal (les
sous-agents ne committent jamais).

| jour | vague | objet | livrable mesuré |
|---|---|---|---|
| **J1 · 07/11** | matin | le produit : le **span `g017`**, la **convention des GV** | attachement et F1, fiche v13 |
| | après-midi | le **schéma v2** (`meta.alternative`, `meta.partition`) et la **restitution v0** | schéma validé, miroir mesuré |
| **J2 · 08/11** | matin | **Panini I** : l'inventaire croisé, la **table atomes ↔ niveaux** | la table, 20 exemples mesurés |
| | après-midi | **Panini I** : le **corpus commun** (format, échantillon) | un corpus partagé + sa fiche |
| **J3 · 09/11** | matin | **Panini II** : le **retrieval à époque contrôlée** | une mesure (double contrôle) |
| | après-midi | **Panini II** : la **généalogie** (Glottolog + leur théorie) | une fiche à deux faces |
| **J4 · 10/11** | matin | la **coordination** N2 (le mètre RoPE), S (les 11 verdicts), R (R1.1) | des fiches de coordination, 0 écriture S/D/N2 |
| | après-midi | la **coordination** A (A6.2), B10.3 (l'enc
… [2993 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"POS 85\\|POS : 85\\|POS=85\\|0,7535\\|0.7535\\|236/237\\|236 / 237\\|2 spans\\|2 span\" reports --include=\"*.md\" --include=\"*.json\" | sort | head -80", "description": "Find fiches with outdated numbers"}`

  ```
reports/INDEX.md
reports/pensee-attachement-parfait.json
reports/pensee-couverture-v5.json
reports/pensee-frontieres-phrase.json
reports/pensee-g017.json
reports/pensee-gn-pronom-sujet.json
reports/pensee-multilingue.json
reports/pensee-pos-r4.json
reports/rapport-audit-v7.md
reports/rapport-autotest-parallele.md
reports/rapport-coherence-fiches-v7.md
reports/rapport-composition-sans-perte.md
reports/rapport-convention-gv.md
reports/rapport-frontieres-integrees.md
reports/rapport-frontieres-phrase.md
reports/rapport-g017.md
reports/rapport-gn-pronom-sujet.md
reports/rapport-gold-anglais.md
reports/rapport-morphologie-verbes.md
reports/rapport-partition-integree.md
reports/rapport-pensee-attachement-parfait.md
reports/rapport-pensee-couverture-v5.md
reports/rapport-pos-anglais-v2.md
reports/rapport-pos-nombres.md
reports/rapport-pos-ponctuation.md
reports/rapport-pos-r4-integre.md
reports/rapport-pos-r4.md
reports/rapport-produit-v0.md
reports/rapport-r035.md
reports/rapport-r264-elision.md
reports/rapport-schema-v1.md
reports/rapport-semaine.md
reports/rapport-topk-v8.md
reports/README.md
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/en-cours.md", "description": "Read current state"}`

  ```
# En ce moment

**Mis à jour : 2026-11-14, 02 h 00 HNE (heure locale, EST).**

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
… [9195 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,40p' reports/rapport-pensee-v10.md; echo '=== v12 ==='; sed -n '1,40p' reports/rapport-pensee-v12.md; echo '=== audit-v7 ==='; sed -n '1,30p' reports/rapport-audit-v7.md", "description": "Inspect existing historical snapshot notices"}`

  ```
# B13 — 220/220 (1,0000), couverture 0,9205 : le féminin `-ée` et la garde déterminant du GP

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **Instantané historique** : état au commit `710ec7f9` · **Verdict** : ✅ chiffres, ⚠️ attribution corrigée
> **183/183 portes** : **une seule** des deux corrections annoncées est **effective** — la
> **garde déterminant** du GP (A17 R3b : un « verbe » précédé d'un déterminant est un nom,
> `for the bus`), **+1 exact** (`r153`). Le **féminin `-ée`** est **inerte sur ce gold** (0
> différence d'annotation ; `r255` reste absent car `acheter` n'est pas au lexique). L'attachement
> est à **220/220 (1,0000)** sur **220 labels** (sur 239), **couverture 0,9205**, **F1 0,5880**
> (gelé 602 ; 0,5843 vivant), tête **0,7388** ; **fr 134/134**, **en 86/86** ; **19 spans** dont
> **17 déjà inatteignables** + `s037` et `r303` (deux régressions, corrigées en v11).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_est_verbe`, boucle GP),
> [`autotest.py`](../tools/pensee/autotest.py) (19 assertions) ;
> JSON [`pensee-v10.json`](pensee-v10.json).

## 1. Les deux corrections

| # | correction
… [4828 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"Instantané historique\\|instantané historique\\|INSTANTANÉ HISTORIQUE\" reports --include=\"*.md\" | sort", "description": "List fiches already marked historical"}`

  ```
reports/rapport-audit-v10.md
reports/rapport-autotest-parallele.md
reports/rapport-coherence-fiches-v7.md
reports/rapport-coherence-fiches-v8.md
reports/rapport-composition-sans-perte.md
reports/rapport-frontieres-integrees.md
reports/rapport-gold-split.md
reports/rapport-morphologie-verbes.md
reports/rapport-partition-integree.md
reports/rapport-pensee-attachement-parfait.md
reports/rapport-pensee-attachement-v2.md
reports/rapport-pensee-attachement-v3.md
reports/rapport-pensee-couverture-v5.md
reports/rapport-pensee-couverture-v7.md
reports/rapport-pensee-r1r3.md
reports/rapport-pensee-segmentation-v4.md
reports/rapport-pensee-v10.md
reports/rapport-pensee-v12.md
reports/rapport-pos-anglais-v2.md
reports/rapport-pos-nombres.md
reports/rapport-pos-r4-integre.md
reports/rapport-produit-v0.md
reports/rapport-schema-v1.md
  ```

- **bash** `{"command": "echo '--- POS 85 ---'; grep -rn \"POS 85\\|POS : 85\\|POS=85\\|85 %\\|85,0\\|0,85\" reports --include=\"*.md\" | head -40\necho '--- F1 7535 ---'; grep -rn \"0,7535\\|0\\.7535\" reports --include=\"*.md\" | head -40\necho '--- 236/237 ---'; grep -rn \"236/237\\|236 / 237\" reports --inc … [171 caractères tronqués]`

  ```
--- POS 85 ---
reports/rapport-parcimonie-imposee.md:51:| 85 % | 301,5 M (−14,9 %) | 23,7468 (+0,57 %) | 26,5785 (+1,23 %) |
reports/rapport-parcimonie-imposee.md:67:| uniforme 85 % | 301,5 M (−14,9 %) | +0,57 % | +1,23 % |
reports/rapport-parcimonie-imposee.md:71:| **FFN complet à 85 %** | **308,0 M (−13,1 %)** | **−0,18 %** | **+0,46 %** |
reports/rapport-parcimonie-imposee.md:74:➡️ **Le point de fonctionnement retenu : k-WTA à 85 % sur les trois projections du
reports/rapport-parcimonie-imposee.md:84:  Résultat : **dégrade** (+0,2 % à 90 %, +1,2 % à 85 %, +3,6 % à 80 %). Le
reports/rapport-attention-creuse.md:156:   −0,45 %, attention 32 + FFN 85 % = **+0,19 %**. Le FFN mange le gain de
reports/rapport-campagne-parcimonie.md:20:| activations du FFN (k-WTA 85 %) | +0,5 à +1,2 % | ⚠️ selon le budget |
reports/rapport-campagne-parcimonie.md:31:**Attention à 32 clés + projection `gate` à 85 %.**
reports/rapport-campagne-parcimonie.md:37:| **+ `gate` à 85 %** | **338,8 M (−4,4 %)** | 23,2811 (**−1,40 %**) | 26,1417 (**−0,44 %**) |
reports/rapport-campagne-parcimonie.md:50:| FFN complet à 85 % + attention creuse | **non additif, défavorable** (+0,19 % en B) |
reports/rapport-croisemen
… [11537 caractères tronqués]
  ```

- **bash** `{"command": "git status --porcelain=v2 | head -60; echo '---branches---'; git branch -vv; echo '---session dirs---'; ls journal/sessions | tail -5", "description": "Check git status details and branches"}`

  ```
1 .M N... 100644 100644 100644 7c52573c94c400495076f2d12546cdda645a7b3c 7c52573c94c400495076f2d12546cdda645a7b3c docs/pilotage/en-cours.md
1 .M N... 100644 100644 100644 675cffbb5ceeb0ed783cede69256fcaf50f116d2 675cffbb5ceeb0ed783cede69256fcaf50f116d2 docs/pilotage/roadmap.md
1 .M N... 100644 100644 100644 bc229b138a9ee877a37e4e351ae687ddb1857cf1 bc229b138a9ee877a37e4e351ae687ddb1857cf1 docs/produit/README.md
1 .M N... 100644 100644 100644 7a44ec7fc3b31bd499de9567c0e203cb1db81818 7a44ec7fc3b31bd499de9567c0e203cb1db81818 journal/2026-11-14/README.md
1 .M N... 100644 100644 100644 d0f384fd29fbc7aaca68998209c612e9b3584190 d0f384fd29fbc7aaca68998209c612e9b3584190 journal/README.md
1 .M N... 100644 100644 100644 68d969e2de1dd296ca6310aa0e001ec83b31de37 68d969e2de1dd296ca6310aa0e001ec83b31de37 journal/sessions/MANIFEST.md
1 .M N... 100644 100644 100644 bb95c771258ab5805f0704c312926ac2c849a14a bb95c771258ab5805f0704c312926ac2c849a14a journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
1 .M N... 100644 100644 100644 2c833a1ba5446ad2c4f569cd71dcb4a8b4eac1ef 2c833a1ba5446ad2c4f569cd71dcb4a8b4eac1ef journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
1 .M N... 100644 
… [3748 caractères tronqués]
  ```

- **bash** `{"command": "for f in rapport-autotest-parallele.md rapport-produit-v0.md rapport-pos-anglais-v2.md rapport-schema-v1.md rapport-morphologie-verbes.md rapport-composition-sans-perte.md rapport-pos-r4-integre.md rapport-frontieres-integrees.md rapport-partition-integree.md rapport-pos-nombres.md; do  … [110 caractères tronqués]`

  ```
=== rapport-autotest-parallele.md ===
# B13 — la vérification parallèle : 183/183 en 1 min 54 (×2,4)

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;
> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,
> F1 0,7535, attachement 236/237, couverture 0,9916, 2 spans).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Ce que ça règle** : l'autotest était **mono-processus** — ~4 min 40 de CPU et ~4 min 40 de
> temps mural sur un poste à 40 cœurs, alors que **183 portes indépendantes** pouvaient tourner de
> front. Avec `AUTOTEST_JOBS=8`, il tient en **1 min 54** (temps mural), **183/183**, mêmes verdicts.
> **Ce que ça ne règle pas** : le reste du dépôt (évaluations gold, portes longues) reste séquentiel ;
> ce round ne fait que la vérification.
=== rapport-produit-v0.md ===
# B13 — le premier produit : `drave` v0, une CLI qui analyse, mesure et rejoue

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;
> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,
> F1 0,7535, attachement 236/23
… [7857 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -S\"Instantané historique\" -- reports | head -20; echo '---'; git log --oneline -15 -- reports/rapport-autotest-parallele.md", "description": "Trace historical notice commits"}`

  ```
1f61caaa FICHES — DIX FICHES ANNOTÉES « INSTANTANÉ HISTORIQUE » (L'ÉTAT COURANT EST 86,25 / 0,7535 / 236-237)
653a7981 B13 — LES DEUX DERNIÈRES RÉGRESSIONS (s037, r303) : EXACT 221/221 (1,0000), COUVERTURE 0,9247, 18 SPANS ; AUDIT V10 INTÉGRÉ, V10 CORRIGÉE ; 183/183
160d08ca B13 — LA GARDE PRON : EXACT 219/219 (1,0000), COUVERTURE 0,9163, F1 0,5822, DEV 152/152 ET TEST 67/67 ; AUDIT DE COHÉRENCE V8 INTÉGRÉ ; 183/183
d497324b B13 — TOP-K 211/239 (LE SITE D'APPEL prec = s), LA V8 RÉÉCRITE HONNÊTEMENT (+17 NET, 7 RÉGRESSIONS), AUDITS A17/A19 INTÉGRÉS ; 183/183
8d6c318d B13 — AUDIT DES 7 FICHES (23 ÉCARTS), DEV/TEST V7 (133/134, 62/62), LA V7 CORRIGÉE AVEC SON CONTRÔLE (195/196 VS 1,67)
---
1f61caaa FICHES — DIX FICHES ANNOTÉES « INSTANTANÉ HISTORIQUE » (L'ÉTAT COURANT EST 86,25 / 0,7535 / 236-237)
a9907a1b B13 — L'AUTOTEST PARALLÈLE : 183/183 EN 1 MIN 54 (×2,4), MÊMES VERDICTS (AUTOTEST_JOBS=8)
  ```

- **bash** `{"command": "sed -n '58240,58320p' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md 2>/dev/null | head -100", "description": "Read prior honesty pass narrative"}`

  ```
COMMIT OK 1
e9088d45 PRODUIT — LE VALIDATEUR PORTE --gold (20 PHRASES DU CORPUS VALIDÉES CONTRE LE SCHÉMA V1) : LA PORTE L'UTILISE
   26c7b7ab..e9088d45  s/v7 -> s/v7
   26c7b7ab..e9088d45  master -> master
  ✅ schéma v1 : Ran 6 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -l \"222/222\\|0,9289\\|17 spans\" reports/rapport-*.md 2>/dev/null | head -12; echo \"---\"; for f in $(grep -l \"222/222\" reports/rapport-*.md 2>/dev/null | head -6); do grep -q \"Instantané historique\" $f && echo \"OK-annot … [98 caractères tronqués]`

  ```
reports/rapport-coherence-fiches-v8.md
reports/rapport-etat-a.md
reports/rapport-fiabilite-produit.md
reports/rapport-file-taches.md
reports/rapport-gold-gp-corrige.md
reports/rapport-partition-syntagmes.md
reports/rapport-pensee-v12.md
reports/rapport-pos-anglais.md
reports/rapport-pos-anglais-v2.md
reports/rapport-pos-r4.md
reports/rapport-produit-bloc-l.md
reports/rapport-produit-v0.md
---
OK-annotée reports/rapport-coherence-fiches-v8.md
À ANNOTER reports/rapport-fiabilite-produit.md
À ANNOTER re
… [2602 caractères tronqués]
  ```

- **bash** `{"command": "grep -rnE \"POS[^0-9]{0,12}8[45]([.,][0-9]+)?[ ]?%?\" reports --include=\"*.md\" | grep -vE \"0,?8[45][0-9]|85 ?%|8[45] ?%\" | head -40; echo '--- 85 exact ---'; grep -rnE \"POS[^0-9]{0,12}85([^0-9]|$)\" reports --include=\"*.md\" | head -40; echo '--- 0,8500/85,00 ---'; grep -rn \"85,0 … [100 caractères tronqués]`

  ```
reports/rapport-pos-r4.md:26:- **R4 bilingue** : **+0,74 dev / +0,71 test** (POS 84,55 %), **23 correctifs / 0 cassé**, F1
reports/rapport-pos-r4.md:29:- **Classes fermées** : **+0,78 dev / +0,81 test** (POS 84,62 %), **25 correctifs / 0 cassé**,
reports/rapport-pos-r4.md:31:- **Paquet sûr** (R4-en + classes fermées) : **+1,19 dev / +1,11 test**, POS **85,00 %**, **37/0**,
reports/rapport-pos-r4.md:34:- **Paquet max** (R4 bilingue + classes fermées) : **+1,51 / +1,51**, POS **85,34 %**, **48/0**,
reports/rapport-pos-r4.md:245:**Mesure du patch core** : POS **84,62 %**, dev **84,53** (**+0,78**), test **84,81** (**+0,81**),
reports/rapport-pos-r4.md:283:- **Bloc « large » (90 mots, dont DET)** : POS test 84,71 (**+0,71**, moins que le core), F1 0,6177,
reports/rapport-pos-r4.md:367:(SHA `0bf4d3eb…`), reproduit **POS 85,34 %** (dev 85,26 / test 85,51), **F1 0,6188**,
reports/rapport-pos-r4.md:408:   POS 85,00 %, 37/0, 2 faux→faux, F1 +0,0007, attachement 222/222. C’est le meilleur rapport
reports/rapport-pos-r4-integre.md:1:# B13 — le paquet POS sûr : classes fermées anglaises + R4-en, POS 84,96 %
reports/rapport-partition-integree.md:12:> exact 235/236, POS 85,00 %** — les mesures d
… [5702 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat 1f61caaa | head -40; echo '=== diff sample ==='; git show 1f61caaa -- reports/rapport-autotest-parallele.md | head -40", "description": "Inspect prior annotation commit"}`

  ```
commit 1f61caaa5fa5782fb42f9095c7625ba644582747
Author: Stéphane <stephane@localhost>
Date:   Sat Nov 7 00:27:33 2026 -0500

    FICHES — DIX FICHES ANNOTÉES « INSTANTANÉ HISTORIQUE » (L'ÉTAT COURANT EST 86,25 / 0,7535 / 236-237)

 docs/pilotage/en-cours.md                          |  2 +-
 journal/2026-11-07/README.md                       |  6 ++--
 journal/2026-11-07/docs.md                         |  2 +-
 journal/2026-11-07/mesures.md                      |  2 +-
 journal/2026-11-07/portes.md                       | 19 ++++++++++
 journal/README.md                                  |  4 +--
 journal/THEMES.md                                  |  1 +
 journal/sessions/MANIFEST.md                       |  2 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 42 ++++++++++++++++++++++
 .../rapport.md                                     | 19 +++++-----
 reports/rapport-autotest-parallele.md              |  4 +++
 reports/rapport-composition-sans-perte.md          |  4 +++
 reports/rapport-frontieres-integrees.md            |  4 +++
 reports/rapport-morphologie-verbes.md              |  4 +++
 reports/rapport-partition-integree.md              |  4 +++
 reports/rapport-pos-angla
… [1415 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-s065.md; echo '=== r035 ==='; sed -n '1,40p' reports/rapport-r035.md; echo '=== convention ==='; sed -n '1,45p' reports/rapport-convention-gv.md", "description": "Read latest measurement fiches"}`

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
… [9905 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"Instantané historique\\|instantané\\|fraîcheur\\|périmé\\|perime\" tools/revue_documentation.py | head -40; echo '---'; sed -n '1,80p' docs/methode/resultats.md", "description": "Check documentation review and result conventions"}`

  ```
9:  4. fraîcheur  : en-cours.md date du dernier commit, ET aucun fait n'a été commité après
138:    # 4. fraîcheur : la date de la page, ET aucun fait commité après le dernier état.
142:        alertes.append("fraîcheur : en-cours.md n'a pas de date « Mis à jour : AAAA-MM-JJ »")
147:                f"fraîcheur : en-cours.md dit {page}, le dernier commit date du {dernier}"
153:            alertes.append("fraîcheur : en-cours.md n'a jamais été commité")
156:                f"fraîcheur : {len(lignes)} fait(s) commité(s) après le dernier état "
374:        print("  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, "
---
# Ce qu'un résultat doit porter

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
> résultats, ou un message de commit.

## Les cinq pièces d'un résultat

1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
   [porte](../theorie/glossaire/entrees/porte.md)) ;
2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rapp
… [3146 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(p['nom'])\nfor t in p['taches']:\n    if t['id'].startswith('J8') or t['id'].startswith('J9'):\n        print(t['id'], t['titre'])\n        print(' ', t['mandat'][:300])\nEOF", "description": "Show J8/J … [21 caractères tronqués]`

  ```
Semaine 07/11 → 14/11 — le produit et l'intégration Panini
J8.1 La restitution v1
  Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotation (segments + rôles + cibles) et la mesurer : le miroir strict (0,1087) doit-il monter ? Fiche `reports/rapport-restitution-v1.md` + JSON, tests, commit.
J9.1 La passe d'honnêteté des fiches
  Tâche J9.1 : la passe d'honnêteté — les fiches qui publient des chiffres dépassés (POS 85, F1 0,7535, 236/237, 2 spans) doivent porter « instantané historique » avec le lien vers l'état courant. Écris `reports/rapport-passe-honnetete.md` + JSON, applique la mention aux fiches concernées, commit.
  ```

- **bash** `{"command": "sed -n '1,40p' reports/rapport-gn-pronom-sujet.md; echo '=== r264 ==='; sed -n '1,20p' reports/rapport-r264-elision.md; echo '=== ponctuation ==='; sed -n '1,15p' reports/rapport-pos-ponctuation.md; echo '=== pos-r4 ==='; sed -n '1,15p' reports/rapport-pos-r4.md", "description": "Inspec … [20 caractères tronqués]`

  ```
# B13 — le pronom sujet est un GN : F1 0,6519 → 0,7013, attachement préservé

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-07 · **Verdict** : ✅
> **La plus grosse erreur de segmentation** était la convention : le gold segmente le **pronom
> sujet** comme un **GN** (« Il | a couru »), le bloc le laissait dans le GV — **417 GN manquants**
> et **333 GV en trop**. La règle (un pronom sujet devant un verbe émet un GN, le GV commence
> après) fait passer la **F1 de 0,6519 à 0,7013** (+4,9), sans perdre un seul attachement :
> **236/237, couverture 0,9916**. **dev 0,6986 / test 0,7073** ; **183/183**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
> branche GV), [`autotest.py`](../tools/pensee/autotest.py) (7 assertions) ; JSON
> [`pensee-gn-pronom-sujet.json`](pensee-gn-pronom-sujet.json).

## 1. La règle

```python
# un pronom sujet devant le verbe est un GN (« Il | a couru ») — convention du gold
if (typ == "mot" and langue == "fr" and n in SUJETS and i + 1 < len(mots)
        and (est_verbe(mots[i+1][0], mots[i+1][2])
             or _normaliser(mots[i+1][2]) in lex.get("AUX", set())
             or _norm
… [3860 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a/; echo '---'; for f in journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a/*; do echo \"=== $f ===\"; head -40 \"$f\"; done", "description": "Inspect untracked session directory"}`

  ```
total 824
drwxr-xr-x. 1 stephane stephane     80 14 nov 02:18 .
drwxr-xr-x. 1 stephane stephane  13544 14 nov 02:17 ..
-rw-r--r--. 1 stephane stephane 154087 14 nov 03:17 digest.md
-rw-r--r--. 1 stephane stephane  10598 14 nov 03:18 rapport.md
-rw-------. 1 stephane stephane 672130 14 nov 03:10 session.v4.jsonl.zstd
---
=== journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a/digest.md ===
# Session DSH — relecture

- identifiant : `session-f198001c-49da-4e65-8a44-782f9605fd7a`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 01:48:04
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotation (segments + rôles + cibles) et la mesurer : le miroir strict (0,1087) doit-il monter ? Fiche `reports/rapport-restitution-v1.md` + JSON, tests, commit.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from:
… [12166 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/pilotage/en-cours.md | head -120; echo '=== roadmap ==='; git diff -- docs/pilotage/roadmap.md | head -80", "description": "Inspect uncommitted state changes"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 7c52573c..2f3fd0fd 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-14, 02 h 10 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-14, 02 h 00 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -27,11 +27,11 @@
 
 - **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
 - **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
-- **Plan** : audit, état, runbook ; nuit.
-- **Ambition** : un état reprenable.
-- **Stratégie** : committer par flux.
-- **Objectif final** : sédimentation à zéro.
-- **Ce qu'elle fait** : intégration ; passe **11 h 30 — 82, 80/2** ; plan de nuit.
+- **Plan** : état.
+- **Ambition** : reprise.
+- **Stratégie** : flux.
+- **Objectif final** : zéro.
+- **Ce qu'elle fait** : intégration ; passe **82, 80/2**.
 - **Ce que font les autres** : **N2**, **S**, **Pensée**.
 - **Prochai
… [13054 caractères tronqués]
  ```

- **bash** `{"command": "git diff --stat; echo '--- untracked sizes ---'; ls -l reports/rapport-restitution-v1.md reports/pensee-restitution-v1.json tools/mesurer_restitution_v1.py 2>/dev/null", "description": "See diff stats and untracked files"}`

  ```
docs/pilotage/en-cours.md                          |  32 +-
 docs/pilotage/roadmap.md                           |   2 +-
 docs/produit/README.md                             |  11 +-
 journal/2026-11-14/README.md                       |  15 +
 journal/README.md                                  |   5 +-
 journal/sessions/MANIFEST.md                       |   7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 145 ++++
 .../rapport.md                                     |  14 +-
 .../digest.md                                      | 210 ++++++
 .../rapport.md                                     |  61 +-
 reports/INDEX.md                                   |   4 +-
 reports/README.md                                  |   1 +
 reports/pensee-coherence-fiches-v7.json            |  19 +
 reports/pensee-dev-test-v10.json                   |   2 +-
 reports/pensee-quatre-modes.json                   | 734 ++++++++++++---------
 reports/rapport-audit-v7.md                        |   6 +-
 reports/rapport-coherence-fiches-v7.md             |  17 +-
 reports/rapport-dev-test-v10.md                    |   2 +-
 reports/rapport-pensee-v12.md                      |   4 +-
 reports/rapport-spa
… [760 caractères tronqués]
  ```

- **bash** `{"command": "git show -s --format='%B' b6e474dc; echo '=== e4288023 ==='; git show -s --format='%B' e4288023 | head -30", "description": "Read latest product commit messages"}`

  ```
J6.2 — s065 : LA REL SUIVIE D'UN GV PREND LE SUJET DU GV (238/238 LABELS, 238/239 CIBLES, F1 0,7902 INCHANGÉ, 0 SPAN, 0 POS)

Le gold « elle qui commence nage » attend `elle` pour la REL 5:17 ; le bloc prédisait `nage`.
La règle exige une REL, un GV à droite et un GN à gauche ; elle attache à la tête du GN.
Elle ne s'applique qu'au chemin union, quand le GN vient de S et la REL courte du chunker.

Mesure : 612 phrases, 239 cibles, split crc32(id)%3. Base 237/238, règle 238/238 (238/239,
0,9958) ; dev 161/162 -> 162/162, test 76/76 inchangé ; F1 0,7902 et POS 0,8625 inchangés.
Une seule annotation change (s065). Contrôles : règle littérale « REL après GV » 0 cas,
237/238 ; variante large 238/238 ; placebo verbe propre 235/238 ; hasard 0,0042.
La règle littérale du mandat ne traite pas la phrase (ordre GN REL GV), la fiche le dit.

Porte bloc verte (20 tests), revue de documentation verte, T0 dans le budget.
Fiche reports/rapport-s065.md ; JSON reports/pensee-s065.json.

=== e4288023 ===
J6.2 — PORTE PRODUIT VERTE (183/183) : FIXTURES D'ATTACHEMENT À 238/238, FICHE ET JSON À JOUR

La règle s065 change une cible : les fixtures de l'autotest qui codaient 237/238
(T153, T161, T162, T164
… [217 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"1 span\\|0 span\\|g017\" reports/rapport-s065.md docs/pilotage/en-cours.md | head -30", "description": "Check span counts in s065 and state"}`

  ```
reports/rapport-s065.md:31:cible, pas le span** : c'est la dernière cible fausse des 239 cibles, l'autre étant `g017`
reports/rapport-s065.md:136:C'est la différence avec `g017` ([fiche](rapport-g017.md)) : là, le gold se contredisait
reports/rapport-s065.md:154:- **Le compte est un compte de cibles.** 238/239 garde `g017` au dénominateur ; 238/238 est
reports/rapport-s065.md:165:(0,9958)**. `g017` reste le dernier écart : ce n'est pas une cible, c'est un **span** et une
reports/rapport-s065.md:166:**convention d'adverbe à trancher** ([fiche](rapport-g017.md)).
reports/rapport-s065.md:175:1. **Trancher la convention d'adverbe** (`g017`), puis rejouer la variante étroite de J6.1.
reports/rapport-s065.md:196:- **Contexte** : [`rapport-g017.md`](rapport-g017.md) § 9 (le dernier span et la convention
reports/rapport-s065.md:197:  d'adverbe), [`rapport-semaine.md`](rapport-semaine.md) (237/238, `g017` et `s065`).
docs/pilotage/en-cours.md:63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **conventio
… [1652 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib, re, json\npat = {\n 'POS85': re.compile(r'POS[^0-9]{0,20}85(?:[.,]0+)?\\s*%'),\n 'F1_7535': re.compile(r'0[.,]7535'),\n 'att_236_237': re.compile(r'236\\s*/\\s*237'),\n 'spans2': re.compile(r'(?<![\\d])2\\s+spans?\\b'),\n}\nrows=[]\nfor p in sorted(path … [597 caractères tronqués]`

  ```
fiche                                            all                              header                 hist
README.md                                        att_236_237                                             -
rapport-autotest-parallele.md                    F1_7535,att_236_237,spans2       F1_7535,att_236_237,spans2 -
rapport-composition-sans-perte.md                F1_7535,att_236_237,spans2       F1_7535,att_236_237,spans2 -
rapport-convention-gv.md                         att_236_237                                             -
rapport-frontieres-integrees.md                  F1_7535,att_236_237,spans2       F1_7535,att_236_237,spans2 -
rapport-frontieres-phrase.md                     spans2                           spans2                 -
rapport-g017.md                                  att_236_237,spans2               att_236_237            -
rapport-gn-pronom-sujet.md                       F1_7535,att_236_237              att_236_237            -
rapport-gold-anglais.md                          spans2                                                  -
rapport-morphologie-verbes.md                    F1_7535,att_236_237,spans2       F1_7535,att_236_237,spans2 -
rapp
… [1109 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re\nt=pathlib.Path('reports/rapport-autotest-parallele.md').read_text()\nprint(repr(t[:300]))\nprint(bool(re.search(r'[Ii]nstant[ée] historique',t)))\nPY", "description": "Debug notice detection"}`

  ```
"# B13 — la vérification parallèle : 183/183 en 1 min 54 (×2,4)\n\n> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;\n> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,\n> F1 0,7535, attachement 236/237, couverture 0,9916, 2 s"
False
  ```

- **bash** `{"command": "grep -n \"passe d'honnêteté\\|Instantané historique\\|À ANNOTER\\|10 fiches annotées\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | head -30", "description": "Locate honesty pass details in prior digest"}`

  ```
46219:reports/rapport-pensee-attachement-v2.md ["# B13 — l'attachement v2 : exact 0,8483 → 0,9448, top-k strict 0,6069 → 0,9724", '', "> **Instantané historique** : état au commit `9d5337ce` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).", '']
46282:> **Instantané historique** : état au commit `392f03aa` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
46291:> **Instantané historique** : état au commit `b975011b` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
48500:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\n# v10 : corriger l'attribution (audit A21)\np=pathlib.Path('reports/rapport-pensee-v10.md'); t=p.read_text()\nt=t.replace(\"> **État courant** · **Verdict** : ✅\",\"> **Instantané historique** : état … [5586 caractères tronqués]`
53641:- Honesty rules applied: every fiche carries a base (612 living vs 602 frozen), historical fiches get "**Instantané historique** : état au comm
… [1146 caractères tronqués]
  ```

- **bash** `{"command": "which zstd || true; zstd -dc journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a/session.v4.jsonl.zstd 2>/dev/null | grep -o 'Instantané historique[^\"]*' | head -5", "description": "Check zstd availability and decompress sample"}`

  ```
/usr/bin/zstd
  ```

- **bash** `{"command": "sed -n '58270,58286p' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md", "description": "See annotation script excerpt"}`

  ```
OK-annotée reports/rapport-pensee-v12.md
À ANNOTER reports/rapport-pos-anglais-v2.md
  ```

### 🤖 Assistant

⏵ Passe d'honnêteté : j'annote les fiches aux chiffres dépassés (« instantané historique »)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib, re\nactuelles = {\"rapport-gn-pronom-sujet.md\",\"rapport-pos-ponctuation.md\",\"rapport-r264-elision.md\",\"rapport-gold-gp-corrige.md\"}\nnote = (\"> **Instantané historique** — les chiffres publié … [2593 caractères tronqués]`

  ```
10 fiches annotées
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ✅ la page vivante date du dernier commit (2026-11-07)
 create mode 100644 journal/2026-11-07/portes.md
COMMIT OK 1
  ```

- **bash** `{"command": "zstd -dc journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a/session.v4.jsonl.zstd 2>&1 | head -c 500; echo; echo EXIT:$?", "description": "Test zstd decompression"}`

  ```
{"type":"session","version":4,"id":"session-f198001c-49da-4e65-8a44-782f9605fd7a","createdAt":1794638884428,"cwd":"/home/stephane/Data13TB/stephane/GitHub/Qtrinet","isSeeded":false,"delegationDepth":0}
{"type":"permission/preset","seq":0,"time":1794638884492,"data":{"preset":"danger-full-access"}}
{"type":"sandbox/mode","seq":1,"time":1794638884495,"data":{"mode":"danger-full-access"}}
{"type":"approval/policy","seq":2,"time":1794638884496,"data":{"policy":"never"}}
{"type":"agent/inbox/spliced"
EXIT:0
  ```

- **bash** `{"command": "ls -la journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/ | head; echo '---'; zstd -dc journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a/session.v4.jsonl.zstd 2>/dev/null | grep -c \"passe\"", "description": "List prior session files"}`

  ```
total 23968
drwxr-xr-x. 1 stephane stephane       94  4 nov 16:38 .
drwxr-xr-x. 1 stephane stephane    13544 14 nov 02:17 ..
-rw-r--r--. 1 stephane stephane  3899744 14 nov 03:17 digest.md
-rw-------. 1 stephane stephane     6898 14 nov 01:16 plan.md
-rw-r--r--. 1 stephane stephane   740135 14 nov 03:18 rapport.md
-rw-------. 1 stephane stephane 19887937 14 nov 03:10 session.v4.jsonl.zstd
---
50
  ```

- **bash** `{"command": "grep -rl \"actuelles = \" journal/sessions 2>/dev/null | head; echo '---'; grep -o 'actuelles = {[^}]*}' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/*.md 2>/dev/null | head", "description": "Look for annotation script in journals"}`

  ```
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
---
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:actuelles = {\"rapport-gn-pronom-sujet.md\",\"rapport-pos-ponctuation.md\",\"rapport-r264-elision.md\",\"rapport-gold-gp-corrige.md\"}
  ```

- **bash** `{"command": "zstd -dc journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/session.v4.jsonl.zstd 2>/dev/null | grep -o '.\\{0,500\\}actuelles = .\\{0,2500\\}' | head -c 5000", "description": "Extract full prior annotation script"}`

  ```
[still running after 60000ms; moved to background job bash-35]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "grep -n \"Fichiers\\|fichiers\" -A 30 journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a/rapport.md | head -60", "description": "See files touched by prior session"}`

  ```
14:| Fichiers touchés | 11 |
15-| Commandes | 88 |
16-| Sous-agents | 0 |
17-| Commits | 0 |
18-| Compactages de contexte | 0 |
19-
20-## 1. Ce qui a été demandé
21-
22-**Tour 1** — Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotation (segments + rôles + cibles) et la mesurer : le miroir strict (0,1087) doit-il monter ? Fiche `reports/rapport-restitution-v1.md` + JSON, tests, commit.
23-
24-## 2. Déroulé, étape par étape
25-
26-### Tour 1 — Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotat … [155 caractères tronqués]
27-
28-*154 appels d'outils.* Actions notables :
29-
30-- bash — List workspace and git state
31-- grep
32-- read
33-- bash — Extract J8 tasks from plan.json
34-- bash — Find restitution code files
35-- bash — Read restitution.py first 400 lines
36-- bash — Read v0 measurement script
37-- bash — Inspect annotation API
38-- bash — Read Annotation and syntagme generation
39-- bash — Read mirror definition
40-- bash — Read CLI restituer handler
41-- bash — List J tasks in plan
42-- bash — Search canonical form references
43-- bash —
… [1600 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- reports/rapport-audit-v7.md reports/rapport-coherence-fiches-v7.md reports/rapport-pensee-v12.md reports/rapport-spans-chunker.md | head -100", "description": "Inspect unrelated report diffs"}`

  ```
diff --git a/reports/rapport-audit-v7.md b/reports/rapport-audit-v7.md
index 84cd244d..e0801691 100644
--- a/reports/rapport-audit-v7.md
+++ b/reports/rapport-audit-v7.md
@@ -263,6 +263,8 @@ sans le dire.
 | T86-T90 | POS 0,8214/0,7897, 0,6471, 0,6829, 0,7013, 0,6984 | 0,8452/0,8221, 0,7353, 0,7236, 0,7327, 0,719 |
 | T111 / T114 / T115 / T119 / T138 | 0,4183 ; 0,3203/0,4817 ; 0,455/0,441 ; 0,7834/0,7472 ; 0,7424/0,3432 | 0,7265 ; 0,5864/0,7285 ; 0,6709 ; 0,7465/0,6914 ; 0,7465/0,3454 |
 
+La liste complète des 26 identifiants est dans le JSON (`portes.docstrings_perimees`).
+
 **6 messages de portes** affichent un dénominateur `/145` qui n'existe plus (196 labels) :
 
 - T161 : `tête 195/145` (devrait être `195/196`) ;
@@ -349,8 +351,8 @@ POS/F1/tête : c'est une règle d'attachement pur.
 top-k 166, fr 135/135, en 60/61, dev 133/134, test 62/62). En ne retirant que la cible
 (`_cible_precedent` + branche S), on retrouve exactement le 160/196. Autrement dit, en v7, le
 top-k 166 vient des **noms S et des verbes proches**, pas des candidats du précédent ; la règle
-du précédent ne porte que la cible. C'est un point à noter pour la fiche amont v5, qui créditait
-les candidats du précé
… [5474 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-35", "wait": true, "timeout_ms": 30000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "for f in rapport-gold-gp-corrige.md rapport-semaine.md rapport-g017.md; do echo \"=== $f ===\"; sed -n '1,35p' \"reports/$f\"; done", "description": "Inspect remaining candidates headers"}`

  ```
=== rapport-gold-gp-corrige.md ===
# B13 — le gold corrigé : 4 GP retrouvés, exact 226/226, couverture 0,9456

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
> `sv`), [`gold_synthetique.json`](../tools/tests/linguistique/gold_synthetique.json) régénéré
> (graine 42, 160 phrases), [`autotest.py`](../tools/pensee/autotest.py) (14 assertions) ;
> JSON [`pensee-gold-gp-corrige.json`](pensee-gold-gp-corrige.json).

## 1. Le défaut

```python
# avant 
… [5496 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"POS\\|F1\\|attachement\\|span\" reports/rapport-gold-gp-corrige.md | head -20", "description": "Check gold-gp-corrige figures"}`

  ```
5:> `gold_synthetique.py`, le span d'un GP partait **après** la préposition (`i = v + index(prep) + 1`)
8:> mêmes segments) et **4 GP** sont réparés : l'attachement passe de **222/222 à 226/226**,
9:> la **couverture de 0,9289 à 0,9456**, les **spans perdus de 17 à 13** (les 4 GP ont disparu de
20:# avant (mode sv) : le span commence après la préposition
36:| spans perdus | 17 (8 REL, 5 SUB, 4 GP) | **13 (8 REL, 5 SUB, 0 GP)** |
38:| F1 syntagmes | 0,6181 | 0,6198 |
44:- **Les 13 spans restants** sont 9 synthétiques (REL/SUB dont les verbes sont hors du lexique du
47:- **La couverture 0,9456** est le nouveau plafond : 13 cibles n'ont pas de segment au bon span.
60:- **Les mesures antérieures** : les fiches v12 et antérieures publient 222/222 et 17 spans — ce
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re\npat = {\n 'POS85': re.compile(r'POS[^0-9]{0,20}85(?:[.,]\\d+)?\\s*%'),\n 'F1_7535': re.compile(r'0[.,]7535'),\n 'att_236_237': re.compile(r'236\\s*/\\s*237'),\n 'spans2': re.compile(r'(?<![\\d])2\\s+spans?\\b'),\n}\nfor p in sorted(pathlib.Path('repo … [466 caractères tronqués]`

  ```
HIST rapport-autotest-parallele.md              F1_7535,att_236_237,spans2
HIST rapport-composition-sans-perte.md          F1_7535,att_236_237,spans2
HIST rapport-frontieres-integrees.md            F1_7535,att_236_237,spans2
     rapport-frontieres-phrase.md               spans2
     rapport-g017.md                            att_236_237
     rapport-gn-pronom-sujet.md                 att_236_237
HIST rapport-morphologie-verbes.md              F1_7535,att_236_237,spans2
HIST rapport-partition-integree.md              F1_7535,att_236_237,spans2
HIST rapport-pos-anglais-v2.md                  F1_7535,att_236_237,spans2
HIST rapport-pos-nombres.md                     F1_7535,att_236_237,spans2
     rapport-pos-ponctuation.md                 POS85
HIST rapport-pos-r4-integre.md                  F1_7535,att_236_237,spans2
HIST rapport-produit-v0.md                      F1_7535,att_236_237,spans2
     rapport-r264-elision.md                    att_236_237,spans2
HIST rapport-schema-v1.md                       F1_7535,att_236_237,spans2
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re\nfor p in sorted(pathlib.Path('reports').glob('rapport-*.md')):\n    t=p.read_text(errors='replace')\n    if 'B13' not in t[:500]: continue\n    if re.search(r'nstant\\S* historique',t): continue\n    title=next((l for l in t.splitlines() if l.startsw … [123 caractères tronqués]`

  ```
rapport-audit-attachement.md                 # Audit de reproductibilité — l'attachement du bloc linguistique (B13)
rapport-audit-r1r3.md                        # Audit R1/R2/R3 — les chiffres rejouent, l'attribution des règles ne rejoue pas
rapport-audit-v2.md                          # Audit B13 — l'attachement v2 : 43 valeurs rejouées, 2 arrondis, 1 erreur de prose (46 → 45), 8 docstrings de
rapport-audit-v7.md                          # Audit v7 — 195/196 sur les deux golds, mais cinq valeurs de qualité sont gelées
rapport-b13-porte-134.md                     # B13 — la porte est à 134/140 : le 140/140 de 702b368c ne se rejoue pas ; quatre rouges viennent du sous-modu
rapport-b13-porte-138.md                     # B13 — la porte est à 138/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 restent
rapport-b13-porte-140.md                     # B13 — la porte est à 140/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 alignés sur 
rapport-cache-chunker-applique.md            # B13 — le cache du chunker appliqué : ×139 en chunker, ×1 en défaut (S domine)
rapport-classement-appris.md                 # B13 — classement appris des candidats d'
… [27015 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/tests/linguistique/evaluer_gold.py | head -80; echo '---'; grep -n \"argparse\\|--json\\|def main\" tools/tests/linguistique/evaluer_gold.py | head -20", "description": "Inspect gold evaluation CLI"}`

  ```
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
SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")


def charger() -> list[dict]:
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in reel:
        p["source"] = "reel"
    return hand + reel + synth


GELE = pathlib.Path(__file__).with_name("gold_ge
… [1993 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py --version 2>&1 | head; echo EXIT:$?; python3 tools/drave.py evaluer --help 2>&1 | head -30", "description": "Check drave CLI evaluate options"}`

  ```
drave 0.1.0
EXIT:0
usage: drave evaluer [-h] [--gold] [--json]

Mesure POS, syntagmes (F1/tête) et attachement (exact/couverture) sur le gold, avec un contrôle négatif reproductible.

options:
  -h, --help, --aide  afficher cette aide et quitter
  --gold              mesurer le gold gelé (référence figée) au lieu du gold vivant
  --json              sortie JSON des mesures complètes

Exemple : python3 tools/drave.py evaluer --gold --json
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --json > /tmp/eval_vivant.json 2>/tmp/eval_vivant.err; echo EXIT:$?; tail -5 /tmp/eval_vivant.err; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/eval_vivant.json'))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:2000])\nPY", "description": "Meas … [46 caractères tronqués]`

  ```
EXIT:0
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
 
… [807 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --gold --json > /tmp/eval_gele.json 2>/tmp/eval_gele.err; echo EXIT:$?; tail -5 /tmp/eval_gele.err; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/eval_gele.json'))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:1600])\nPY", "description": "Measu … [44 caractères tronqués]`

  ```
EXIT:0
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
   "exactitude_ouvert": 0.7914,
   "tokens": 3141,
   "confusions": {
    "ADJ": {
     "ADJ": 65,
     "NOUN": 64,
     "VERB": 4
    },
    "ADV": {
     "ADV": 129,
     "NOUN": 7,
     "PREP": 1,
     "ADJ": 1,
     "?": 1
    },
    "AUX": {
     "PREP": 4,
     "AUX": 117,
     "?": 3,
     "NOUN": 1,
     "VERB": 1
    },
    "CONJ": {
     "PRON": 15,
     "CONJ": 67,
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
     "PONCT": 15
    },
    "PREP": {
     "PREP": 114
    },
    "PRON": {
     "PRON": 419,
     "?": 29,
     "CONJ": 2,
     "DET": 14
    },
    "VERB": {
     "VERB": 538,
     "NOUN": 216,
     "PREP": 2,
     "ADJ": 2,
     "?": 15,
     "AUX": 7,
     "ADV": 1
    }
   }
  },
  "syntagme": {
   "precision"
… [407 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ('/tmp/eval_vivant.json','/tmp/eval_gele.json'):\n d=json.load(open(f)); h=d['heuristique']; a=h['attachement']\n print(f, 'gold', d['gold']['nom'], 'phrases', d['gold']['phrases'])\n print(' POS',h['pos']['exactitude'],'F1',h['syntagme']['f1'],'t … [222 caractères tronqués]`

  ```
/tmp/eval_vivant.json gold vivant (hand + reel + synthétique) phrases 612
 POS 0.8625 F1 0.7902 tete 0.9029
 att {'cibles': 239, 'labels': 238, 'top1': 238, 'topk': 236, 'exact': 238, 'top1_taux': 0.9958, 'topk_taux': 0.9874, 'exact_taux': 0.9958, 'exact_any_taux_span': 1.0}
/tmp/eval_gele.json gold gelé (référence figée) phrases 602
 POS 0.8625 F1 0.7882 tete 0.9025
 att {'cibles': 239, 'labels': 234, 'top1': 234, 'topk': 232, 'exact': 234, 'top1_taux': 0.9791, 'topk_taux': 0.9707, 'exact_taux': 0.9791, 'exact_any_taux_span': 1.0}
  ```

- **bash** `{"command": "grep -n \"POS\\|F1\\|attachement\\|236\\|237\\|spans\" reports/rapport-frontieres-phrase.md | head -20; echo '--- gold-gp ---'; grep -n \"236\\|237\\|0,7535\" reports/rapport-gold-gp-corrige.md | head", "description": "Check frontieres-phrase and gold-gp markers"}`

  ```
9:> par construction** ; **2 spans de phrase du gold corrigés** (espace de tête), **0 régression mesurée**.
11:> [`pensee-frontieres-phrase.json`](pensee-frontieres-phrase.json) (les 40 textes, les spans avant/après,
21:textes sont exacts, **0** défaut, **0** chevauchement, **0** fausse question. Sur le **gold 612**, POS,
22:F1 syntagmes, attachement et tokens sont **inchangés au chiffre près** (delta 0) ; seuls **2 spans de
31:  catégories demandées. Les textes, les spans attendus et les spans prédits avant/après sont dans le JSON
36:  L'évaluateur est `tools/tests/linguistique/evaluer_gold.py` (POS, F1 syntagmes, attachement,
67:| textes exacts (spans + types) | 2/40 | **40/40** | 40/40 |
121:spans, est dans le JSON.
230:### 2.4 Effet sur POS, syntagmes et attachement
232:- **Le patch de frontières ne change aucun POS, aucun syntagme, aucun attachement** : **0/40** textes
235:- **38/40** textes changent de libellés `phrase` et de spans d'acte ; **5/40** changent de connecteurs
236:  `discours` (fragments d'URL supprimés, spans corrigés). Les **actes faux** passent de **63/102** à
241:- **Patch B (tokénisation)** : sur les 40 textes, **477 → 362 tokens** (−115), **273 → 232 POS** 
… [815 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,210p' tools/revue_documentation.py", "description": "Read documentation review checks"}`

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
… [7076 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/verifie_etat_a_jour.py", "description": "Read state freshness checker"}`

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
… [6867 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/ | head; echo '---'; git ls-files journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc | head; echo '--- current session tracked? ---'; git ls-files journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a", "description … [47 caractères tronqués]`

  ```
total 23968
drwxr-xr-x. 1 stephane stephane       94  4 nov 16:38 .
drwxr-xr-x. 1 stephane stephane    13544 14 nov 02:17 ..
-rw-r--r--. 1 stephane stephane  3899744 14 nov 03:17 digest.md
-rw-------. 1 stephane stephane     6898 14 nov 01:16 plan.md
-rw-r--r--. 1 stephane stephane   740135 14 nov 03:18 rapport.md
-rw-------. 1 stephane stephane 19887937 14 nov 03:10 session.v4.jsonl.zstd
---
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
--- current session tracked? ---
  ```

- **bash** `{"command": "git diff --stat -- tools/restitution.py tools/drave.py tools/tests/test_restitution.py tools/porte-produit.sh reports/README.md docs/produit/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-14/README.md reports/INDEX.md", "description": "Diff stats for J8.1 f … [6 caractères tronqués]`

  ```
docs/pilotage/en-cours.md       |  32 +-
 docs/pilotage/roadmap.md        |   2 +-
 docs/produit/README.md          |  11 +-
 journal/2026-11-14/README.md    |  15 +
 reports/INDEX.md                |   4 +-
 reports/README.md               |   1 +
 tools/drave.py                  |  32 +-
 tools/porte-produit.sh          |  18 +-
 tools/restitution.py            | 626 +++++++++++++++++++++++++++++++++++++++-
 tools/tests/test_restitution.py | 136 +++++++++
 10 files changed, 851 insertions(+), 26 deletions(-)
  ```

- **bash** `{"command": "git diff -- tools/porte-produit.sh tools/drave.py | head -140", "description": "Review J8.1 CLI and gate changes"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index c94b3f9a..371473c5 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -345,7 +345,9 @@ def cmd_restituer(args: argparse.Namespace) -> int:
 
     Deux modes : un **texte** (ou un fichier), ou un **banc** JSON de textes
     (`--banc`, le format de `reports/pensee-fiabilite-produit.json`). Le mode banc
-    laisse le bloc détecter la langue, comme le CLI sans `--langue`.
+    laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`
+    ajoute la **forme canonique v1** (segments + rôles + cibles) et son miroir ; la
+    sortie de la v0 reste celle par défaut.
     """
     if args.banc:
         if args.texte is not None or args.fichier:
@@ -358,12 +360,17 @@ def cmd_restituer(args: argparse.Namespace) -> int:
         except (OSError, ValueError) as exc:
             print(f"{NOM}: erreur : banc illisible : {exc}", file=sys.stderr)
             return 1
-        rapport = restitution.mesurer_banc(items, args.langue)
+        if args.canonique:
+            rapport = restitution.mesurer_banc_v1(items, args.langue)
+        else:
+            rapport = restitution.mesurer_banc(items, args.langue)
         rappo
… [4440 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-restitution-v1.md; echo '=== JSON keys ==='; python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-restitution-v1.json'))\nprint(list(d)[:20])\nprint(json.dumps({k:d[k] for k in list(d)[:5]},ensure_ascii=False)[:1200])\nPY", "description": "Inspe … [25 caractères tronqués]`

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
… [3210 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/tests/test_restitution.py 2>&1 | tail -8; echo EXIT:${PIPESTATUS[0]}", "description": "Run restitution unit tests", "timeoutMs": 180000}`

  ```
test_ne_lit_pas_le_texte (__main__.TestReconstruction.test_ne_lit_pas_le_texte) ... ok
test_niveaux_pauvres (__main__.TestReconstruction.test_niveaux_pauvres) ... ok
test_surface_sans_controle (__main__.TestReconstruction.test_surface_sans_controle) ... ok

----------------------------------------------------------------------
Ran 22 tests in 13.567s

OK
EXIT:0
  ```

- **bash** `{"command": "python3 tools/drave.py restituer \"Le chat dort.\" --canonique --json | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['schema']); print(d['forme']['surface_canonique']); print(d['canonique']['exact'], d['strict']['exact'])\"", "description": "Smoke test canonical restitu … [6 caractères tronqués]`

  ```
drave.restitution.canonique
le chat dort
True False
  ```

- **bash** `{"command": "git diff -- journal/2026-11-14/README.md journal/README.md journal/sessions/MANIFEST.md | head -120", "description": "Inspect journal diffs for J8.1"}`

  ```
diff --git a/journal/2026-11-14/README.md b/journal/2026-11-14/README.md
index 7a44ec7f..b923db11 100644
--- a/journal/2026-11-14/README.md
+++ b/journal/2026-11-14/README.md
@@ -74,4 +74,19 @@ sœur dépasse même celui de l'écriture (+0,213) une fois la famille séparée
 [`reports/rapport-retrieval-familles.md`](../../reports/rapport-retrieval-familles.md), JSON
 [`reports/retrieval-familles.json`](../../reports/retrieval-familles.json), outil
 [`tools/retrieval_familles.py`](../../tools/retrieval_familles.py).
+**J8.1 — la restitution v1 : le miroir strict ne monte pas, la forme canonique vaut 1,0000.**
+La v0 restitue la surface **46/46** mais le miroir strict tombe à **5/46 = 0,1087** parce que
+`rendre_mots`/`rendre_pos` séparent la ponctuation (`dort .`). La v1 construit une **forme
+canonique** depuis les **segments + rôles + cibles** : **46/46 formes exactes** contre une
+source canonisée (casse repliée, ponctuation retirée), mais **1/46 = 0,0217** contre la source
+brute — et le **miroir strict reste 0,1087**. C'est la réponse : le strict ne doit pas monter,
+il mesure la surface ; la forme canonique mesure autre chose. La structure tient : **395
+segments**, **395 rôles**, *
… [6889 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/produit/README.md reports/README.md reports/INDEX.md | head -100", "description": "Inspect docs/index diffs"}`

  ```
diff --git a/docs/produit/README.md b/docs/produit/README.md
index bc229b13..5dc0b717 100644
--- a/docs/produit/README.md
+++ b/docs/produit/README.md
@@ -238,6 +238,13 @@ surfaces exactes**, miroir strict **0,1087**, contrôle négatif **46/46**. C'es
 surface**, pas un décodeur neuronal : il ne prouve pas la fidélité sémantique. La fiche est
 [`rapport-restitution-v0.md`](../../reports/rapport-restitution-v0.md).
 
+`--canonique` ajoute la **forme canonique v1** (segments + rôles + cibles) : **46/46** contre
+la source **canonisée**, mais le **miroir strict reste 0,1087** — la forme n'est pas la
+surface, et elle tombe à **1/46** si on la compare à la source brute. Les **395 segments**
+portent **395 rôles** et **315 cibles** (315 résolues, 313 dans un autre segment) ; la
+stabilité structurelle est **18/46**. Fiche
+[`rapport-restitution-v1.md`](../../reports/rapport-restitution-v1.md).
+
 ## 4. Ce que le produit ne fait pas encore
 
 **1. Il ne génère pas de texte.** `restituer` reconstruit la **surface** depuis l'annotation
@@ -406,6 +413,7 @@ rejeu identique : oui
 | `--jsonl` | `analyser` | une ligne JSON par phrase (avec `--fichier`) |
 | `--fichier CHEMIN` | `analyser`, `res
… [4610 caractères tronqués]
  ```

- **bash** `{"command": "les .git/hooks/pre-commit && sed -n '1,120p' .git/hooks/pre-commit", "description": "Inspect pre-commit hook"}`

  ```
[stderr]
bash: line 1: les: command not found
[exit code: 127]
  ```

- **bash** `{"command": "test -f .git/hooks/pre-commit && sed -n '1,160p' .git/hooks/pre-commit || echo 'no pre-commit'", "description": "Read pre-commit hook"}`

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

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nprint('md',len(list(pathlib.Path('reports').glob('*.md'))))\nprint('json',len(list(pathlib.Path('reports').glob('*.json'))))\nPY\ngit status --short reports/rapport-s-paragraphes.md reports/INDEX.md", "description": "Count report files and check untrack … [4 caractères tronqués]`

  ```
md 722
json 816
 M reports/INDEX.md
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "sed -n '210,420p' tools/revue_documentation.py", "description": "Read remaining documentation review checks"}`

  ```
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
                    f"libellé : {f.relative_to(RACINE)} annonce « {lab} » mais pointe {cible}"
                )

    # 7a. chemins morts en code inline (hors gabarits)
    for f in sources_propres():
        try:
            brut = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        texte = re.sub(r"\[[^\]]+\]\([^)]+\)", "", brut)
        for m in CHEMIN.finditer(texte):
            p = m.group(1).rstrip(".,;:)")
            if any(g in p for g in GABARIT):
              
… [6676 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo EXIT:${PIPESTATUS[0]}", "description": "Run documentation review baseline", "timeoutMs": 180000}`

  ```
revue de documentation · 722 fiche(s) · 816 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT:0
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/produit/README.md journal/2026-11-14/README.md reports/README.md reports/rapport-restitution-v1.md reports/pensee-restitution-v1.json tools/drave.py tools/mesurer_restitution_v1.py tools/porte-produit.sh tools/restitution.p … [114 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/produit/README.md
M  journal/2026-11-14/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-02ebc573-ec84-46cf-945c-cfd7d563a9fc/digest.md
 M journal/sessions/session-02ebc573-ec84-46cf-945c-cfd7d563a9fc/rapport.md
 M reports/INDEX.md
M  reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
A  reports/pensee-restitution-v1.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
A  reports/rapport-restitution-v1.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
M  tools/drave.py
A  tools/mesurer_restitution_v1.py
M  tools/porte-produit.sh
M  tools/restitution.py
 m tools/structures
M  tools/tests/test_restitution.py
?? journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a/
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "git commit -m \"J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)\n\n\\`restituer --canonique\\` construit la forme canonique (segments, rôles, cibles) depuis\nl'annotation, sans lire la surface. Contre la source canonisée : 46/46 formes exactes\n(1,0000 … [558 caractères tronqués]`

  ```
✅ index : aucun fait stagé sans état
[s/v7 229098ec] J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
 27 files changed, 19298 insertions(+), 60 deletions(-)
 create mode 100644 journal/sessions/session-d58794d6-d201-493e-b6ab-fffee9656e15/digest.md
 create mode 100644 journal/sessions/session-d58794d6-d201-493e-b6ab-fffee9656e15/rapport.md
 create mode 100644 journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a/digest.md
 create mode 100644 journal/sessions/session-f198001c-49da-4e65-8a44-782f9605fd7a/rapport.md
 create mode 100644 reports/pensee-restitution-v1.json
 create mode 100644 reports/rapport-restitution-v1.md
 create mode 100644 tools/mesurer_restitution_v1.py
EXIT:0
  ```

- **bash** `{"command": "git status --short | head -40; echo '---'; git log --oneline -3; echo '--- state commit ---'; git show --stat --oneline HEAD | head -35", "description": "Check post-J8.1 status and commit"}`

  ```
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
---
229098ec J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
d31e8788 J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE
e4288023 J6.2 — PORTE PRODUIT VERTE (183/183) : FIXTURES D'ATTACHEMENT À 238/238, FICHE ET JSON À JOUR
--- state commit ---
229098ec J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
 docs/pilotage/en-cours.md                          |    32 +-
 docs/pilotage/roadmap.md                           |     2 +-
 docs/produit/README.md                             |    11 +-
 journal/2026-11-14/README.md                       |    23 +-
 journal/2026-11-14/docs.md                         |     2 +-
 journal/20
… [1443 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfiles = \"\"\"rapport-autotest-parallele.md rapport-composition-sans-perte.md rapport-frontieres-integrees.md rapport-morphologie-verbes.md rapport-partition-integree.md rapport-pos-anglais-v2.md rapport-pos-nombres.md rapport-pos-r4-integre.md rapport- … [544 caractères tronqués]`

  ```
rapport-autotest-parallele.md 0 "> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;\n> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,\n> F1 0,7535, attachement 236/237, couverture 0,991"
rapport-composition-sans-perte.md 0 "> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;\n> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,\n> F1 0,7535, attachement 236/237, couverture 0,991"
rapport-frontieres-integrees.md 0 "> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;\n> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,\n> F1 0,7535, attachement 236/237, couverture 0,991"
rapport-morphologie-verbes.md 0 "> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;\n> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,\n> F1 0,7535, attachement 236/237, couverture 0,991"
rapport-partition-integree.md 0 "> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;\n> l
… [1443 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib, re\nnew = (\n    \"> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne\\n\"\n    \"> décrivent pas l'état courant. L'état courant du bloc est dans\\n\"\n    \"> [`en-cours`](../docs/pilotage/en-cours.md) et [` … [1149 caractères tronqués]`

  ```
MAJ  rapport-autotest-parallele.md
MAJ  rapport-composition-sans-perte.md
MAJ  rapport-frontieres-integrees.md
MAJ  rapport-morphologie-verbes.md
MAJ  rapport-partition-integree.md
MAJ  rapport-pos-anglais-v2.md
MAJ  rapport-pos-nombres.md
MAJ  rapport-pos-r4-integre.md
MAJ  rapport-produit-v0.md
MAJ  rapport-schema-v1.md
AJOUT rapport-gn-pronom-sujet.md
AJOUT rapport-pos-ponctuation.md
AJOUT rapport-pos-r4.md
AJOUT rapport-r264-elision.md
  ```

- **bash** `{"command": "for f in rapport-autotest-parallele.md rapport-gn-pronom-sujet.md rapport-pos-r4.md rapport-r264-elision.md rapport-pos-ponctuation.md; do echo \"=== $f ===\"; sed -n '1,12p' \"reports/$f\"; done", "description": "Verify notice formatting"}`

  ```
=== rapport-autotest-parallele.md ===
# B13 — la vérification parallèle : 183/183 en 1 min 54 (×2,4)

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Ce que ça règle** : l'autotest était **mono-processus** — ~4 min 40 de CPU et ~4 min 40 de
> temps mural sur un poste à 40 cœurs, alors que **183 portes indépendantes** pouvaient tourner de
> front. Avec `AUTOTEST_JOBS=8`, il tient en **1 min 54** (temps mural), **183/183**, mêmes verdicts.
> **Ce que ça ne règle pas** : le reste du dépôt (évaluations gold, portes longues) reste séquentiel ;
> ce round ne fait que la vérification.
=== rapport-gn-pronom-sujet.md ===
# B13 — le pronom sujet est un GN : F1 0,6519 → 0,7013, attachement préservé

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cou
… [3036 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfiles = \"\"\"rapport-autotest-parallele.md rapport-composition-sans-perte.md rapport-frontieres-integrees.md\nrapport-morphologie-verbes.md rapport-partition-integree.md rapport-pos-anglais-v2.md\nrapport-pos-nombres.md rapport-pos-r4-integre.md rappor … [431 caractères tronqués]`

  ```
fix rapport-gn-pronom-sujet.md
fix rapport-pos-ponctuation.md
fix rapport-pos-r4.md
fix rapport-r264-elision.md
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-gold-gp-corrige.md')\nt=p.read_text()\nold_start=\"> **Instantané historique**\"\nassert old_start not in t\nnew=(\"> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne\\n\"\n    … [429 caractères tronqués]`

  ```
ajout gold-gp-corrige
# B13 — le gold corrigé : 4 GP retrouvés, exact 226/226, couverture 0,9456

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).


> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Un défaut du générateur de gold**, pas du bloc : dans le mode `sv` de
> `gold_synthetique.py`, le span d'un GP partait **après** la préposition (`i = v + index(prep) + 1`)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-gold-gp-corrige.md'); t=p.read_text()\np.write_text(t.replace('roadmap.md).\\n\\n\\n> **Ligne', 'roadmap.md).\\n\\n> **Ligne'))\nPY", "description": "Normalize blank line in gold-gp-corrige"}`

  ```
(no output)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib, re\nfiles = \"\"\"rapport-autotest-parallele.md rapport-composition-sans-perte.md rapport-frontieres-integrees.md\nrapport-morphologie-verbes.md rapport-partition-integree.md rapport-pos-anglais-v2.md\nrapport-pos-nombres.md rapport-pos-r4-integre.md ra … [1143 caractères tronqués]`

  ```
rapport-autotest-parallele.md            notice=True line=3 old=False
rapport-composition-sans-perte.md        notice=True line=3 old=False
rapport-frontieres-integrees.md          notice=True line=3 old=False
rapport-morphologie-verbes.md            notice=True line=3 old=False
rapport-partition-integree.md            notice=True line=3 old=False
rapport-pos-anglais-v2.md                notice=True line=3 old=False
rapport-pos-nombres.md                   notice=True line=3 old=False
rapport-pos-r4-integre.md                notice=True line=3 old=False
rapport-produit-v0.md                    notice=True line=3 old=False
rapport-schema-v1.md                     notice=True line=3 old=False
rapport-gn-pronom-sujet.md               notice=True line=3 old=False
rapport-pos-ponctuation.md               notice=True line=3 old=False
rapport-pos-r4.md                        notice=True line=3 old=False
rapport-r264-elision.md                  notice=True line=3 old=False
rapport-gold-gp-corrige.md               notice=True line=3 old=False
rapport-s065.md                          notice=False markers= []
rapport-frontieres-phrase.md             notice=False markers= ['2spans']
rapport-r0
… [293 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-35 (bash: zstd -dc journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/session.v4.jsonl.zstd 2>/dev/null | grep -o '.\{0,500\}actuelles = .\{0,2500\}' | head -c 5000) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-35"}`

  ```
s its date/snapshot).\n\nLet me do it with a script: for each fiche, if it has attachment numbers < 236 or F1 < 0.75, add the note (with the link to the current state).\n\nTime 00:45."},{"type":"text","text":"⏵ Passe d'honnêteté : j'annote les fiches aux chiffres dépassés (« instantané historique »)"},{"type":"tool-call","id":"call_00_7sOADsdXTytPDvmutdqD4631","name":"bash","arguments":"{\"command\": \"cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\\nimport pathlib, re\\nactuelles = {\\\"rapport-gn-pronom-sujet.md\\\",\\\"rapport-pos-ponctuation.md\\\",\\\"rapport-r264-elision.md\\\",\\\"rapport-gold-gp-corrige.md\\\"}\\nnote = (\\\"> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;\\\\n\\\"\\n        \\\"> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,\\\\n\\\"\\n        \\\"> F1 0,7535, attachement 236/237, couverture 0,9916, 2 spans).\\\\n\\\\n\\\")\\nretenues = {\\\"rapport-pos-anglais-v2.md\\\",\\\"rapport-produit-v0.md\\\",\\\"rapport-pos-r4-integre.md\\\",\\n            \\\"rapport-morphologie-verbes.md\\\",\\\"rapport-composition-sans-perte.md\\\",\\n            \\\"rappo
… [3842 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re\npat = {\n 'POS85': re.compile(r'POS[^0-9]{0,20}85(?:[.,]\\d+)?\\s*%'),\n 'F1_7535': re.compile(r'0[.,]7535'),\n 'att_236_237': re.compile(r'236\\s*/\\s*237'),\n 'spans2': re.compile(r'(?<![\\d])2\\s+spans?\\b'),\n}\nfor p in sorted(pathlib.Path('repo … [319 caractères tronqués]`

  ```
INDEX.md                                      POS85
README.md                                     POS85,att_236_237
rapport-convention-gv.md                      att_236_237
rapport-frontieres-phrase.md                  spans2
rapport-g017.md                               att_236_237,spans2
rapport-gold-anglais.md                       spans2
rapport-r035.md                               att_236_237
rapport-semaine.md                            att_236_237,spans2
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfiles=['rapport-convention-gv.md','rapport-g017.md','rapport-r035.md','rapport-semaine.md']\nnew=(\"> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne\\n\"\n     \"> décrivent pas l'état courant. L'état coura … [748 caractères tronqués]`

  ```
ajout rapport-convention-gv.md
ajout rapport-g017.md
ajout rapport-r035.md
ajout rapport-semaine.md
=== rapport-convention-gv.md ===
# B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.2 · **Date** : 2026-11-07 ·
> **Verdict** : ✅
> Les **322 FP / 180 FN** du plan sont les erreurs **de GV** du gold d'avant `r035` (F1 0,7533) ;
=== rapport-g017.md ===
# B13 — g017 : l'adverbe final hors de la SUB est rejeté (g017 gagné, r264 et r288 perdus)

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.1 · **Date** : 2026-11-14 ·
> **Verdict** : ❌ **règle rejetée**.
> La règle demandée — **
… [1184 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re\npat = {\n 'POS85': re.compile(r'POS[^0-9]{0,20}85(?:[.,]\\d+)?\\s*%'),\n 'F1_7535': re.compile(r'0[.,]7535'),\n 'att_236_237': re.compile(r'236\\s*/\\s*237'),\n 'spans2': re.compile(r'(?<![\\d])2\\s+spans?\\b'),\n}\nrem=[]\nfor p in sorted(pathlib.Pa … [306 caractères tronqués]`

  ```
4 restants
('INDEX.md', ['POS85'])
('README.md', ['POS85', 'att_236_237'])
('rapport-frontieres-phrase.md', ['spans2'])
('rapport-gold-anglais.md', ['spans2'])
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfiles = \"\"\"rapport-autotest-parallele.md rapport-composition-sans-perte.md rapport-frontieres-integrees.md\nrapport-morphologie-verbes.md rapport-partition-integree.md rapport-pos-anglais-v2.md\nrapport-pos-nombres.md rapport-pos-r4-integre.md rappor … [668 caractères tronqués]`

  ```
19
19/19 notice ligne 3 + 2 liens
  ```

- **bash** `{"command": "sed -n '1,120p' tools/porte-tableaux.sh", "description": "Inspect table gate rules"}`

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
… [4918 caractères tronqués]
  ```

- **write** `{"file_path": "reports/rapport-passe-honnetete.md", "content": "# Passe d'honnêteté — 19 fiches portent « instantané historique », les quatre chiffres dépassés ne se lisent plus comme l'état courant\n\n> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J9.1 · **Date** : 2026-11-14 ·\n … [10531 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-passe-honnetete.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\n\ndef f(fichier, groupe, marqueurs, action):\n    return {\n        \"fichier\": f\"reports/{fichier}\",\n        \"groupe\": groupe,\n        \"marqueurs\": marqueurs,\n        \"action\": action,\n        \"ligne_notice\": 3,\n        \"liens\": … [6329 caractères tronqués]`

  ```
reports/passe-honnetete.json 8485 octets
{
 "notices": {
  "attendues": 19,
  "trouvees": 19,
  "ligne": 3
 },
 "liens": {
  "attendus": 38,
  "resolus": 38
 },
 "scan_apres": {
  "fiches_examinees": 722,
  "marqueurs": [
   "POS 85",
   "0,7535",
   "236/237",
   "2 spans"
  ],
  "fiches_resultats_sans_notice": 0,
  "faux_positifs": [
   {
    "fichier": "reports/rapport-frontieres-phrase.md",
    "pourquoi": "« 2 spans de phrase du gold corrigés » : spans de phrase, pas d'attachement"
   },
   {
    "fichier": "reports/rapport-gold-anglais.md",
    "pourquoi": "« 2 spans exacts » du gold anglais : autre objet"
   }
  ],
  "index": [
   "reports/README.md",
   "reports/INDEX.md"
  ]
 },
 "courante_sans_notice": [
  "reports/rapport-s065.md"
 ],
 "mesure_reproduite": true
}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nprint('md',len(list(pathlib.Path('reports').glob('*.md'))),'json',len(list(pathlib.Path('reports').glob('*.json'))))\nPY\ngrep -n \"fichiers / JSON\" docs/pilotage/en-cours.md", "description": "Count reports after adding files"}`

  ```
md 723 json 817
105:| fichiers / JSON de résultats | **722** / **816** | `reports/*.md` / `reports/*.json` |
  ```

- **bash** `{"command": "sed -n '1,70p' reports/README.md", "description": "Inspect reports README structure"}`

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
| [`rapport-semaine.md`](rapport-semaine.md) | **J5.1** — le rapport de semaine : produit, intégration, décisions, rejets, reste |
| [`rapport-coordination-n2.md`](rapport-coordination-n2.md) | **N2** — le mètre RoPE : 8,0225 → 2,9726/2,7856, `--rope` seul insuffisant |
| [`rapport-coordination-s.md`](rappor
… [5961 caractères tronqués]
  ```

- **edit** `{"file_path": "reports/README.md", "old_string": "| [`rapport-semaine.md`](rapport-semaine.md) | **J5.1** — le rapport de semaine : produit, intégration, décisions, rejets, reste |\n| [`rapport-coordination-n2.md`](rapport-coordination-n2.md) | **N2** — le mètre RoPE : 8,0225 → 2,9726/2,7856, `--rop … [488 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "reports/README.md", "limit": 20}`

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
18: | [`rapport-semaine.md`](rapport-semaine.md) | **J5.1** — le rapport de semaine : produit, intégration, décisions, rejets, reste |
19: | [`
… [331 caractères tronqués]
  ```

- **edit** `{"file_path": "reports/README.md", "new_string": "| [`rapport-semaine.md`](rapport-semaine.md) | **J5.1** — le rapport de semaine : produit, intégration, décisions, rejets, reste |\n| [`rapport-passe-honnetete.md`](rapport-passe-honnetete.md) | **J9.1** — la passe d'honnêteté : **19** fiches « insta … [488 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"722\\|723\" reports/rapport-passe-honnetete.md reports/passe-honnetete.json | head -20", "description": "Find count references in report/JSON"}`

  ```
reports/rapport-passe-honnetete.md:21:> **Dispositif** : scan lexical des 722 fiches de `reports/`, annotation des 19, contrôle des
reports/rapport-passe-honnetete.md:116:**Contrôle négatif 3 — le scan après la passe.** Sur les **722** fiches de `reports/`, il reste
reports/passe-honnetete.json:368:   "fiches_examinees": 722,
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-passe-honnetete.md'); t=p.read_text()\nt=t.replace('scan lexical des 722 fiches', 'scan lexical des 723 fiches')\nt=t.replace('Sur les **722** fiches', 'Sur les **723** fiches')\np.write_text(t)\np=pathlib.Path('reports/p … [280 caractères tronqués]`

  ```
ok
reports/rapport-passe-honnetete.md:21:> **Dispositif** : scan lexical des 723 fiches de `reports/`, annotation des 19, contrôle des
reports/rapport-passe-honnetete.md:116:**Contrôle négatif 3 — le scan après la passe.** Sur les **723** fiches de `reports/`, il reste
reports/passe-honnetete.json:368:   "fiches_examinees": 723,
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Get current local time"}`

  ```
2026-11-14 03:28 EST
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "limit": 135}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-14, 02 h 00 HNE (heure locale, EST).**
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
… [11064 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-14, 03 h 30 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-14, 02 h 00 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **co … [911 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **J5.1** : rapport de semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets**) ; [rapport](../../reports/rapport-semaine.md) + JSON.\n- **J9.1 — la passe d'honnêteté** : **19 fiches** portent « instantané histori … [591 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **723** / **817** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **722** / **816** | `reports/*.md` / `reports/*.json` |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"État au 14/11\" docs/pilotage/roadmap.md; sed -n '38,44p' docs/pilotage/roadmap.md", "description": "Locate roadmap state paragraph"}`

  ```
38:**État au 14/11 02 h 00.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du GV : 238/238, 0 span, 0 POS ; [fiche](../../reports/rapport-s065.md)) ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV** réglée (sujet hors du GV + adverbe final : GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **contrat v2 publié et validé** (`meta.partition`/`meta.alternative`, version 2, **v1 lue** : 26 cas, 0 échec) ; **restitution v1** (`restituer --canonique` : **46/46 formes canoniques exactes** contre la source canonisée, **miroir strict 0,1087 inchangé**, **395 segments / 395 rôles / 315 cibles dont 315 résolues**, stabilité **18/46** ; le strict ne monte pas, la v1 n'est pas la surface ; [fiche](../../reports/rapport-restitution-v1.md)), porte produit **13 contrôles** (16 + 8 + 4 + 22 tests) ; frontières de phrase, partition étiquetée, compositions sans perte, PONCT, R4, « que », `r264`, **GN du pronom sujet et du nom propre** (+10,2 pts de F1) ; les quatre états N2/S/R/A intégrés ; 84 portes, 3 rouges (`indice`, `melange`, `sessions` du hub) ; `mas
… [2096 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md'); t=p.read_text()\nold='**État au 14/11 02 h 00.**'\nnew='**État au 14/11 03 h 30.**'\nassert old in t\nt=t.replace(old,new,1)\nold2='; [fiche](../../reports/rapport-restitution-v1.md)), porte produit **13 contr … [524 caractères tronqués]`

  ```
ok
38:**État au 14/11 03 h 30.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du GV : 238/238, 0 span, 0 POS ; [fiche](../../reports/rapport-s065.md)) ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV** réglée (sujet hors du GV + adverbe final : GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **contrat v2 publié et validé** (`meta.partition`/`meta.alternative`, version 2, **v1 lue** : 26 cas, 0 échec) ; **restitution v1** (`restituer --canonique` : **46/46 formes canoniques exactes** contre la source canonisée, **miroir strict 0,1087 inchangé**, **395 segments / 395 rôles / 315 cibles dont 315 résolues**, stabilité **18/46** ; le strict ne monte pas, la v1 n'est pas la surface ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J9.1 passe d'honnêteté** (**19** fiches « instantané historique » : 10 encarts réécrits, 9 ajoutés ; **0 fiche de résultats** ne publie les quatre marqueurs sans mention, hors 2 faux positifs ; [fiche](../../reports/rapport-passe-honnetete.md)), porte produit **13 contrôles** (16 + 8 + 4 + 22 tests) ; frontièr
… [275 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -30; echo EXIT:${PIPESTATUS[0]}", "description": "Run documentation review", "timeoutMs": 180000}`

  ```
revue de documentation · 723 fiche(s) · 817 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT:0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -20; echo EXIT:${PIPESTATUS[0]}", "description": "Run table formatting gate", "timeoutMs": 120000}`

  ```
✅ 1788 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4036 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
EXIT:0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo EXIT:${PIPESTATUS[0]}; python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo EXIT2:${PIPESTATUS[0]}", "description": "Check context budget and state", "timeoutMs": 120000}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2718    202   T1   2800  reports/README.md
    2450    166   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4064 mots (budget 4 000)

  avertissements :
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [257 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **J9.1 — passe d'honnêteté** : **19 fiches** « instantané historique » (10 réécrites, 9 ajoutées) ; **0 fiche** ne publie les quatre marqueurs sans mention, hors 2 faux positifs ; [fiche](../../reports/rapport-passe-honnetete.md).", "old_st … [497 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **co … [911 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; echo EXIT:${PIPESTATUS[0]}", "description": "Recheck context budget", "timeoutMs": 120000}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4014 mots (budget 4 000)

  avertissements :
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4014 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT:1
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **J9.1 — passe d'honnêteté** : **19 fiches** « instantané historique » ; **0 fiche** ne publie les quatre marqueurs sans mention ; [fiche](../../reports/rapport-passe-honnetete.md).", "old_string": "- **J9.1 — passe d'honnêteté** : **19 fic … [193 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -5; echo EXIT:${PIPESTATUS[0]}", "description": "Recheck context budget after trim", "timeoutMs": 120000}`

  ```
avertissements :
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4006 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT:1
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée** (test −0,0028 ; g017 à trancher) ; **schéma v2 … [976 caractères tronqués]`

  ```
Error: old_string was not found in "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"
  ```

- **bash** `{"command": "sed -n '87,97p' docs/pilotage/en-cours.md", "description": "Inspect current en-cours bullets"}`

  ```
- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
- **N3 — clos** : 17 portes vertes ; inventaire exécutable (5/5) ; deux conditions nommées ; [fiche](../../reports/rapport-n3-inventaire.md).
- **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée** (test −0,0028 ; g017 à trancher) ; **schéma v2** (v1 lue) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; [restitution v0](../../reports/rapport-restitution-v0.md), [g017](../../reports/rapport-g017.md).
- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
- **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significativ
… [1321 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text()\nold_p='- **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6. … [1336 caractères tronqués]`

  ```
ok
  avertissements :
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT:0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -10; echo EXIT:${PIPESTATUS[0]}", "description": "Run revue after state edits", "timeoutMs": 180000}`

  ```
revue de documentation · 723 fiche(s) · 817 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT:0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -6; echo EXIT:${PIPESTATUS[0]}; python3 tools/verifie_en_cours.py 2>&1 | tail -4; echo EXIT2:${PIPESTATUS[0]}", "description": "Run table and state gates", "timeoutMs": 120000}`

  ```
✅ 1788 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4036 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
EXIT:0
  en-cours · 1620 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT2:0
  ```

- **bash** `{"command": "git status --short | sed -n '1,80p'", "description": "Review working tree status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M reports/INDEX.md
 M reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-autotest-parallele.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-composition-sans-perte.md
 M reports/rapport-convention-gv.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-frontieres-integrees.md
 M reports/rapport-g017.md
 M reports/rapport-gn-pronom-sujet.md
 M reports/rapport-gold-gp-corrige.md
 M reports/rapport-morphologie-verbes.md
 M reports/rapport-partition-integree.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-pos-anglais-v2.md
 M reports/rapport-pos-nombres.md
 M reports/rapport-pos-ponctuation.md
 M reports/rapport-pos-r4-integre.md
 M reports/rapport-pos-r4.md
 M reports/rapport-produit-v0.md
 M reports/rapport-r035.md
 M reports/rapport-r264-elision.md
 M reports/rapport-schema-v1.md
 M reports/rapport-semaine.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? reports/passe-honnetete.json
?? reports/rapport-passe-honnetete.md
?? reports/
… [24 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib, re\nj=json.load(open('reports/passe-honnetete.json'))\nprint('JSON ok:', j['tache'], len(j['fiches']), 'fiches')\nmissing=[]; bad=[]\nfor e in j['fiches']:\n    p=pathlib.Path(e['fichier'])\n    if not p.exists(): missing.append(e['fichier']); con … [1318 caractères tronqués]`

  ```
JSON ok: J9.1 19 fiches
missing []
bad []
reports 723 remaining [('INDEX.md', ['POS85']), ('rapport-frontieres-phrase.md', ['spans2']), ('rapport-gold-anglais.md', ['spans2'])]
vivant POS/F1/att 0.8625 0.7902 238 239 0.9958
gele POS/F1/att 0.8625 0.7882 234 239 0.9791
  ```

- **bash** `{"command": "grep -nE \"POS[^0-9]{0,20}85(?:[.,][0-9]+)? *%|236/237|0,7535\" reports/README.md reports/INDEX.md | head -20", "description": "Check index marker occurrences"}`

  ```
reports/README.md:32:| [`rapport-r264-elision.md`](rapport-r264-elision.md) | **B13** — `r264` : 236/237, couverture **0,9916** |
[stderr]
grep: warning: ? at start of expression
  ```

- **bash** `{"command": "grep -n \"Instantané historique\" reports/README.md reports/INDEX.md | head", "description": "Check historical mention in indexes"}`

  ```
(no output)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re\nt=pathlib.Path('reports/README.md').read_text()\nfor k,rx in {'POS85':re.compile(r'POS[^0-9]{0,20}85(?:[.,]\\d+)?\\s*%'),'F1':re.compile(r'0[.,]7535'),'att':re.compile(r'236\\s*/\\s*237'),'spans2':re.compile(r'(?<![\\d])2\\s+spans?\\b')}.items():\n p … [136 caractères tronqués]`

  ```
POS85 True
F1 False
att True
spans2 False
hist True
  ```

- **bash** `{"command": "grep -in \"instantan\" reports/README.md | head", "description": "Find instantané in README"}`

  ```
19:| [`rapport-passe-honnetete.md`](rapport-passe-honnetete.md) | **J9.1** — la passe d'honnêteté : **19** fiches « instantané historique », 0 chiffre dépassé lu comme courant |
  ```

- **bash** `{"command": "bash tools/toutes-les-portes.sh > /tmp/portes-j91.log 2>&1; echo EXIT:$? >> /tmp/portes-j91.log", "description": "Run full gates in background", "run_in_background": true, "timeoutMs": 1200000}`

  ```
started background job bash-101
  ```

- **bash** `{"command": "git diff --stat -- reports/rapport-autotest-parallele.md reports/rapport-composition-sans-perte.md reports/rapport-frontieres-integrees.md reports/rapport-morphologie-verbes.md reports/rapport-partition-integree.md reports/rapport-pos-anglais-v2.md reports/rapport-pos-nombres.md reports … [471 caractères tronqués]`

  ```
docs/pilotage/en-cours.md                 | 6 +++---
 docs/pilotage/roadmap.md                  | 2 +-
 reports/README.md                         | 1 +
 reports/rapport-autotest-parallele.md     | 6 +++---
 reports/rapport-composition-sans-perte.md | 6 +++---
 reports/rapport-convention-gv.md          | 4 ++++
 reports/rapport-frontieres-integrees.md   | 6 +++---
 reports/rapport-g017.md                   | 4 ++++
 reports/rapport-gn-pronom-sujet.md        | 4 ++++
 reports/rapport-gold-gp-corrige.md        | 4 ++++
 reports/rapport-morphologie-verbes.md     | 6 +++---
 reports/rapport-partition-integree.md     | 6 +++---
 reports/rapport-pos-anglais-v2.md         | 6 +++---
 reports/rapport-pos-nombres.md            | 6 +++---
 reports/rapport-pos-ponctuation.md        | 4 ++++
 reports/rapport-pos-r4-integre.md         | 6 +++---
 reports/rapport-pos-r4.md                 | 4 ++++
 reports/rapport-produit-v0.md             | 6 +++---
 reports/rapport-r035.md                   | 4 ++++
 reports/rapport-r264-elision.md           | 4 ++++
 reports/rapport-schema-v1.md              | 6 +++---
 reports/rapport-semaine.md                | 4 ++++
 22 files changed, 71 insertions(+), 34 
… [12 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- reports/rapport-gn-pronom-sujet.md reports/rapport-pos-r4.md reports/rapport-r264-elision.md reports/rapport-pos-ponctuation.md reports/rapport-convention-gv.md reports/rapport-g017.md reports/rapport-r035.md reports/rapport-semaine.md | head -160", "description": "Review no … [29 caractères tronqués]`

  ```
diff --git a/reports/rapport-convention-gv.md b/reports/rapport-convention-gv.md
index 79bb9bf4..938a8be0 100644
--- a/reports/rapport-convention-gv.md
+++ b/reports/rapport-convention-gv.md
@@ -1,5 +1,9 @@
 # B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902
 
+> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
+> décrivent pas l'état courant. L'état courant du bloc est dans
+> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).
+
 > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.2 · **Date** : 2026-11-07 ·
 > **Verdict** : ✅
 > Les **322 FP / 180 FN** du plan sont les erreurs **de GV** du gold d'avant `r035` (F1 0,7533) ;
diff --git a/reports/rapport-g017.md b/reports/rapport-g017.md
index 74b2c7be..1663dcb8 100644
--- a/reports/rapport-g017.md
+++ b/reports/rapport-g017.md
@@ -1,5 +1,9 @@
 # B13 — g017 : l'adverbe final hors de la SUB est rejeté (g017 gagné, r264 et r288 perdus)
 
+> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
+> décrivent pas l'état courant. L'état courant du bloc est dans
+> [`en-cours`](..
… [5100 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-101"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "grep -n \"85,00\\|85,75\\|84,96\" reports/rapport-passe-honnetete.md | head; python3 - <<'PY'\nimport json,pathlib\np=pathlib.Path('reports/passe-honnetete.json'); d=json.loads(p.read_text())\nd['instantane_depasse']['pos']=[0.8496,0.85,0.8575]\np.write_text(json.dumps(d,ensure_ascii=Fa … [119 caractères tronqués]`

  ```
32:| POS (gold vivant 612) | **85,00 – 85,75 %** | **86,25 %** | **+0,50 à +1,25 pt** |
48:- `POS 85` (85,00 / 85,34 / 85,75) ;
75:| [`rapport-partition-integree.md`](rapport-partition-integree.md) | POS 85,00 ; F1 0,7535 ; 236/237 ; 2 spans | encart réécrit | ligne 3 |
77:| [`rapport-pos-nombres.md`](rapport-pos-nombres.md) | POS 85,00 ; F1 0,7535 ; 236/237 ; 2 spans | encart réécrit | ligne 3 |
78:| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | POS 84,96 ; F1 0,7535 ; 236/237 ; 2 spans | encart réécrit | ligne 3 |
82:| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | POS 85,75 ; 235/236 | encart ajouté | ligne 3 |
83:| [`rapport-pos-r4.md`](rapport-pos-r4.md) | POS 85,00 ; POS 85,34 ; 222/222 | encart ajouté | ligne 3 |
[0.8496, 0.85, 0.8575]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-passe-honnetete.md'); t=p.read_text()\nt=t.replace('| POS (gold vivant 612) | **85,00 – 85,75 %** | **86,25 %** | **+0,50 à +1,25 pt** |',\n            '| POS (gold vivant 612) | **84,96 – 85,75 %** | **86,25 %** | **+0,5 … [249 caractères tronqués]`

  ```
ok
**pour leur commit**, mais leurs chiffres ne sont plus l'état courant.

| mesure | instantané publié (06/11) | **état courant (14/11, HEAD `229098ec`)** | écart |
|---|---:|---:|---:|
| POS (gold vivant 612) | **84,96 – 85,75 %** | **86,25 %** | **+0,50 à +1,29 pt** |
| F1 syntagmes (vivant 612) | **0,7535** | **0,7902** | **+0,0367** |
| F1 syntagmes (gelé 602) | — | **0,7882** | — |
| attachement exact / labels | **236/237** (0,9916) | **238/238** (238/239 cibles, 0,9958) | **+2 / +1** |
| spans sans label | **2** (`r035`, `g017`) | **1** (`g017`) | **−1** |

**Pourquoi ces chiffres ont bougé.** `r035` a réglé la relative zéro (236 → 237) ; la convention
des GV a fait monter la F1 de 0,7549 à 0,7902 ; `s065` a attaché la REL « qui commence » au sujet
du GV qui la suit (237/238 → 238/238). `g017` reste le seul span sans label : ce n'est pas une
cible fausse, c'est une convention d'adverbe à trancher.

## 2. La règle appliquée

**Est « concernée »** une fiche de `reports/` qui publie, dans son titre, son résumé ou une
mesure, un des quatre marqueurs de l'instantané **comme son état ou comme l'état du produit** :

- `POS 85` (84,96 / 85,00 / 85,34 / 85,75) ;
- `F1 0,7535` ;
- `23
… [28 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-101", "wait": true, "timeout_ms": 120000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -20 /tmp/portes-j91.log 2>/dev/null; echo '---'; wc -l /tmp/portes-j91.log 2>/dev/null", "description": "Check gates progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-1114-03h29
  porte-adaptateur-sortie ✅                          80 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
---
3 /tmp/portes-j91.log
  ```

- **bash** `{"command": "python3 -m json.tool reports/passe-honnetete.json >/dev/null && echo JSON-OK; python3 - <<'PY'\nimport json\nd=json.load(open('reports/passe-honnetete.json'))\nprint(len(d['fiches']), 'fiches')\nprint('pos depasse', d['instantane_depasse']['pos'])\nprint('current living', d['etat_couran … [110 caractères tronqués]`

  ```
JSON-OK
19 fiches
pos depasse [0.8496, 0.85, 0.8575]
current living 0.8625 0.7902
  ```

- **bash** `{"command": "sed -n '1,80p' tools/index_reports.py", "description": "Inspect report index generator"}`

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

- **bash** `{"command": "tail -8 /tmp/portes-j91.log 2>/dev/null; echo '---'; test -f work/portes-1114-03h29/registre.txt && tail -5 work/portes-1114-03h29/registre.txt || true", "description": "Check gates progress again"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-1114-03h29
  porte-adaptateur-sortie ✅                          80 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
---
porte-adaptateur-sortie 0 80
  ```

- **bash** `{"command": "ps -eo pid,etime,cmd | grep -E 'porte|toutes-les-portes|python3' | grep -v grep | head -20", "description": "See running gate processes"}`

  ```
2062 10-07:58:09 /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
   2233 10-07:58:08 /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
   3002 10-07:58:04 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
  64780  9-20:08:14 /opt/google/chrome/chrome --type=zygote --no-zygote-sandbox --crashpad-handler-pid=64701 --enable-crash-reporter=8755d71b-0329-48b0-8a01-92063bf04a7d, --change-stack-guard-on-fork=enable
  64782  9-20:08:14 /opt/google/chrome/chrome --type=zygote --crashpad-handler-pid=64701 --enable-crash-reporter=8755d71b-0329-48b0-8a01-92063bf04a7d, --change-stack-guard-on-fork=enable
  64797  9-20:08:14 /opt/google/chrome/chrome --type=zygote --crashpad-handler-pid=64701 --enable-crash-reporter=8755d71b-0329-48b0-8a01-92063bf04a7d, --change-stack-guard-on-fork=enable
  64975  9-20:08:14 /opt/google/chrome/chrome --type=gpu-process --gpu-recent-crash-count=0 --ozone-platform=x11 --crashpad-handler-pid=64701 --enable-crash-reporter=8755d71b-0329-48b0-8a01-92063bf04a7d, --change-stack-guard-on-fork=enable --gpu-preferences=YAAAAAAAAAAgAQAEAAAAAAAAAAAAAGAASAAAAAAAAAABAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAAwAAAAAAAAAAEAAAA
… [9711 caractères tronqués]
  ```

- **bash** `{"command": "ls -la work/portes-1114-03h29 2>/dev/null | head; echo '---'; ps -eo pid,etime,cmd | grep -E 'toutes-les-portes|porte-' | grep -v grep | head", "description": "Inspect gate work dir and processes"}`

  ```
total 8
drwxr-xr-x. 1 stephane stephane  126 14 nov 03:31 .
drwxr-xr-x. 1 stephane stephane 1856 14 nov 03:29 ..
-rw-r--r--. 1 stephane stephane  580 14 nov 03:31 porte-adaptateur-sortie.log
-rw-r--r--. 1 stephane stephane    0 14 nov 03:31 porte-audit-drapeaux.log
-rw-r--r--. 1 stephane stephane   29 14 nov 03:31 registre.txt
---
1612744    01:33:16 bash tools/toutes-les-portes.sh
1999929       02:33 bash -c bash tools/toutes-les-portes.sh > /tmp/portes-j91.log 2>&1; echo EXIT:$? >> /tmp/portes-j91.log
1999936       02:32 bash tools/toutes-les-portes.sh
1999972       02:30 timeout 1800 bash tools/porte-profondeur-routee.sh
1999973       02:30 bash tools/porte-profondeur-routee.sh
2004887       02:06 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/porte-profondeur-routee/corpus.ids --limit 8192 --ctx 8192 --threads 8 --couches 0:16 --tete-partielle --etat-sortie /tmp/porte-profondeur-routee/e16/etat --etat-pos 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,
… [48730 caractères tronqués]
  ```

- **bash** `{"command": "git add \\\n  docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md \\\n  reports/rapport-passe-honnetete.md reports/passe-honnetete.json \\\n  reports/rapport-autotest-parallele.md reports/rapport-composition-sans-perte.md \\\n  reports/rapport-frontieres-integrees.md re … [618 caractères tronqués]`

  ```
docs/pilotage/en-cours.md                 |   6 +-
 docs/pilotage/roadmap.md                  |   2 +-
 reports/README.md                         |   1 +
 reports/passe-honnetete.json              | 404 ++++++++++++++++++++++++++++++
 reports/rapport-autotest-parallele.md     |   6 +-
 reports/rapport-composition-sans-perte.md |   6 +-
 reports/rapport-convention-gv.md          |   4 +
 reports/rapport-frontieres-integrees.md   |   6 +-
 reports/rapport-g017.md                   |   4 +
 reports/rapport-gn-pronom-sujet.md        |   4 +
 reports/rapport-gold-gp-corrige.md        |   4 +
 reports/rapport-morphologie-verbes.md     |   6 +-
 reports/rapport-partition-integree.md     |   6 +-
 reports/rapport-passe-honnetete.md        | 164 ++++++++++++
 reports/rapport-pos-anglais-v2.md         |   6 +-
 reports/rapport-pos-nombres.md            |   6 +-
 reports/rapport-pos-ponctuation.md        |   4 +
 reports/rapport-pos-r4-integre.md         |   6 +-
 reports/rapport-pos-r4.md                 |   4 +
 reports/rapport-produit-v0.md             |   6 +-
 reports/rapport-r035.md                   |   4 +
 reports/rapport-r264-elision.md           |   4 +
 reports/rapport-schema-v1.m
… [128 caractères tronqués]
  ```

- **bash** `{"command": "tail -6 /tmp/portes-j91.log 2>/dev/null; echo '---'; cat work/portes-1114-03h29/registre.txt 2>/dev/null; echo '---'; ps -p 1999936 -o pid,etime,cmd 2>/dev/null || true", "description": "Check gate job before commit"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-1114-03h29
  porte-adaptateur-sortie ✅                          80 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
---
porte-adaptateur-sortie 0 80
---
    PID     ELAPSED CMD
1999936       02:44 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "pstree -p 1999936 2>/dev/null | head -20; echo '---'; ls -la work/portes-1114-03h29/", "description": "Inspect gate process tree"}`

  ```
bash(1999936)---timeout(2030851)---bash(2030852)-+-tail(2033668)
                                                 `-timeout(2033667)---python(2033669)-+-python(2056289)-+-{python}(2056306)
                                                                                      |                 |-{python}(2056307)
                                                                                      |                 |-{python}(2056308)
                                                                                      |                 |-{python}(2056309)
                                                                                      |                 |-{python}(2056310)
                                                                                      |                 |-{python}(2056311)
                                                                                      |                 |-{python}(2056312)
                                                                                      |                 |-{python}(2056313)
                                                                                      |                 |-{python}(2056314)
                   
… [1553 caractères tronqués]
  ```

- **bash** `{"command": "ps -p 2033669,2033667 -o pid,etime,%cpu,%mem,cmd 2>/dev/null; echo '---'; tail -5 /tmp/porte-audit-drapeaux.log 2>/dev/null || true; ls -l /tmp/porte-audit-drapeaux 2>/dev/null | head", "description": "Check audit gate resource use"}`

  ```
PID     ELAPSED %CPU %MEM CMD
2033669       01:24  4.7  0.4 /home/stephane/gpu-env/bin/python -u tools/audit_drapeaux_harnais.py --pas 200 --sortie /tmp/porte-audit-drapeaux
2033667       01:24  0.0  0.0 timeout 1800 /home/stephane/gpu-env/bin/python -u tools/audit_drapeaux_harnais.py --pas 200 --sortie /tmp/porte-audit-drapeaux
---
total 13416
drwxr-xr-x. 2 stephane stephane     100 14 nov 03:31 elagage25
-rw-r--r--. 1 stephane stephane 4574656 14 nov 03:31 elagage25.gguf
-rw-r--r--. 1 stephane stephane    1265 14 nov 03:31 elagage25.log
-rw-r--r--. 1 stephane stephane       0 14 nov 03:32 masque10.log
drwxr-xr-x. 2 stephane stephane     100 14 nov 03:32 masque25
-rw-r--r--. 1 stephane stephane 4574656 14 nov 03:32 masque25.gguf
-rw-r--r--. 1 stephane stephane     732 14 nov 03:32 masque25.log
drwxr-xr-x. 2 stephane stephane     100 14 nov 03:31 temoin
-rw-r--r--. 1 stephane stephane 4574656 14 nov 03:31 temoin.gguf
  ```

- **bash** `{"command": "git commit -m \"J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT\n\nLes 19 fiches de la cohorte POS 85 / F1 0,7535 / 236/237 / 2 spans portent un encart\nen ligne 3 qui pointe vers en-cours et la roadmap, sans rec … [648 caractères tronqués]`

  ```
✅ index : aucun fait stagé sans état
[s/v7 ecef7250] J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT
 32 files changed, 1667 insertions(+), 52 deletions(-)
 create mode 100644 reports/passe-honnetete.json
 create mode 100644 reports/rapport-passe-honnetete.md
EXIT:0
  ```

- **bash** `{"command": "git log --oneline -3; echo '---'; git show --stat --oneline HEAD | head -40; echo '--- status ---'; git status --short | head -30", "description": "Verify J9.1 commit and status"}`

  ```
ecef7250 J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT
229098ec J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
d31e8788 J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE
---
ecef7250 J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT
 docs/pilotage/en-cours.md                          |   6 +-
 docs/pilotage/roadmap.md                           |   2 +-
 journal/2026-11-14/README.md                       |   5 +-
 journal/2026-11-14/mesures.md                      |   7 +-
 journal/README.md                                  |   2 +-
 journal/THEMES.md                                  |   2 +-
 journal/sessions/MANIFEST.md                       |   6 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  14 +
 .../digest.md                                      | 985 +++++++++++++++++++++
 .../rapport.md                                     |  25 +-
 reports/README.md                           
… [1761 caractères tronqués]
  ```

- **bash** `{"command": "tail -12 /tmp/portes-j91.log 2>/dev/null; echo '---'; cat work/portes-1114-03h29/registre.txt 2>/dev/null; echo '---'; ps -p 1999936 -o pid,etime,cmd 2>/dev/null || true", "description": "Check full gate progress after commit"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-1114-03h29
  porte-adaptateur-sortie ✅                          80 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         185 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          16 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
---
porte-adaptateur-sortie 0 80
porte-audit-drapeaux 0 185
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 14
porte-bloc-linguistique 0 16
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
---
    PID     ELAPSED CMD
1999936       05:27 bash tools/toutes-les-portes.sh
  ```

- **job_output** `{"job_id": "bash-101", "timeout_ms": 300000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -12 /tmp/portes-j91.log 2>/dev/null; echo '---'; wc -l work/portes-1114-03h29/registre.txt", "description": "Check gate progress"}`

  ```
porte-audit-drapeaux   ✅                         185 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          16 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          54 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          91 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅                         107 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard        ✅                          33 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynch
… [203 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"J9.1\\|honnêteté\\|instantané\" journal/2026-11-14/README.md journal/2026-11-14/mesures.md | head -20", "description": "Check journal entry for J9.1"}`

  ```
(no output)
  ```

- **bash** `{"command": "git show --format=fuller --stat HEAD | head -50; echo '--- message ---'; git show -s --format='%B' HEAD", "description": "Review commit metadata and message"}`

  ```
commit ecef72507c326d77d64e56e59af7aa89e9859422
Author:     Stéphane <stephane@localhost>
AuthorDate: Sat Nov 14 03:32:37 2026 -0500
Commit:     Stéphane <stephane@localhost>
CommitDate: Sat Nov 14 03:32:37 2026 -0500

    J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT
    
    Les 19 fiches de la cohorte POS 85 / F1 0,7535 / 236/237 / 2 spans portent un encart
    en ligne 3 qui pointe vers en-cours et la roadmap, sans recopier de valeurs.
    10 encarts réécrits (l'ancien copiait l'état et avait périmé), 9 ajoutés.
    
    Contrôles : 19/19 notices, 38/38 liens ; 0 fiche de résultats ne publie un marqueur
    sans mention, hors 2 faux positifs (« 2 spans » de phrase) et les index.
    État courant mesuré : vivant 612 POS 0,8625 F1 0,7902 att. 238/238 labels (238/239),
    1 span (g017) ; gelé 602 F1 0,7882 att. 234/239.
    
    Fiche reports/rapport-passe-honnetete.md ; JSON reports/passe-honnetete.json.
    Revue de documentation verte, tableaux verts, T0 dans le budget.

 docs/pilotage/en-cours.md                          |   6 +-
 docs/pilotage/roadmap.md                           |   2 +-
 journal/2
… [2527 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/journal_auto.py 2>&1 | tail -20; echo EXIT:${PIPESTATUS[0]}; grep -n \"J9.1\\|honnêteté\\|instantané\" journal/2026-11-14/*.md | head -20", "description": "Regenerate journal after commit", "timeoutMs": 180000}`

  ```
2026-11-14 : 8 commits
  journal/2026-11-14/docs.md
  journal/2026-11-14/memoire.md
  journal/2026-11-14/mesures.md
  journal/2026-11-14/portes.md
  journal/2026-11-14/README.md
  journal/THEMES.md
6 fichiers écrits · 8 commits classés
EXIT:0
journal/2026-11-14/docs.md:12:| 03:32 | `ecef7250` | J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT | `en-cours.md`, `roadmap.md`, `README.md` (+29) |
journal/2026-11-14/README.md:36:| 03:32 | `ecef7250` | J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT |
  ```

- **bash** `{"command": "tail -8 /tmp/portes-j91.log 2>/dev/null; echo '---'; wc -l work/portes-1114-03h29/registre.txt; awk '$2 != 0' work/portes-1114-03h29/registre.txt | head", "description": "Check gates progress and failures"}`

  ```
porte-bloc-linguistique ✅                          16 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          54 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          91 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅                         107 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard        ✅                          33 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne
  porte-cerveau          ✅                          10 s    ✅ porte tenue (quatre facultés composent, chacune reste active, le tout est déterministe)
---
13 work/portes-1114-03h29/registre.txt
  ```

- **bash** `{"command": "pstree -p 1999936 2>/dev/null | head -5; echo '---'; ps -eo pid,etime,%cpu,cmd | awk '$1==1999936 || $1==2033667 || $1==2033669 {print}'", "description": "Check current long gate"}`

  ```
bash(1999936)---timeout(2136488)---bash(2136489)---bash(2139182)-+-drave(2139183)-+-{drave}(2139187)
                                                                 |                |-{drave}(2139188)
                                                                 |                |-{drave}(2139189)
                                                                 |                |-{drave}(2139340)
                                                                 |                |-{drave}(2139341)
---
1999936       10:48  0.0 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "git status --short journal | head -20", "description": "See journal changes to commit"}`

  ```
M journal/2026-11-14/README.md
 M journal/2026-11-14/docs.md
  ```

- **bash** `{"command": "git add journal/2026-11-14/README.md journal/2026-11-14/docs.md && git commit -m \"JOURNAL — 2026-11-14 : J9.1 AU RÉCIT (19 FICHES « INSTANTANÉ HISTORIQUE »)\" 2>&1 | tail -20; echo EXIT:${PIPESTATUS[0]}", "description": "Commit journal entry for J9.1", "timeoutMs": 300000}`
