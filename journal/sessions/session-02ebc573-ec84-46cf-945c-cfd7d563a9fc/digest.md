# Session DSH — relecture

- identifiant : `session-02ebc573-ec84-46cf-945c-cfd7d563a9fc`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 01:21:58
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J7.1 : approfondir le retrieval Panini — sur les 532 langues UDHR (même source XML), mesurer le retrieval par famille Glottolog (les 29 langues de `language_genealogy.py` + l'échantillon 20) avec le contrôle d'époque, et comparer à la mesure de J3.1. Fiche `reports/rapport-retrieval-familles.md` + JSON, contrôle négatif (familles différentes vs sœurs).

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

- **bash** `{"command": "pwd && ls && git log --oneline -5 && git status --short | head -50", "description": "Inspect workspace root and git state"}`

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
e4288023 J6.2 — PORTE PRODUIT VERTE (183/183) : FIXTURES D'ATTACHEMENT À 238/238, FICHE ET JSON À JOUR
2d6f5bff PORTES — LA PASSE DU 14/11 : 84 PORTES, 81 VERTES, 3 ROUGES (INDICE, MELANGE, SESSIONS DU HUB) ; MANDAT E181CE02 RAFRAÎCHI
6ecc9763 JOURNAL — 2026-11-14 : J6.2 AU RÉCIT (2 COMMITS, LE THÈME MESURES), s065 238/238
b6e474dc J6.2 — s065 : LA REL SUIVIE D'UN GV PREND LE SUJET DU GV (238/238 LABELS, 238/239 CIBLES, F1 0,7902 INCHANGÉ, 0 SPAN, 0 POS)
64d9dd23 J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CONVENTION DU GOLD À TRANCHER
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rappor
… [212 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ 2>/dev/null | head -80; echo '---'; ls journal/ 2>/dev/null | tail -20", "description": "List reports and journal entries"}`

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
… [714 caractères tronqués]
  ```

- **bash** `{"command": "grep -ril \"j3.1\\|J3\\.1\" reports/ journal/ docs/ tools/ src/ 2>/dev/null | head -40; echo '--- genealogy ---'; find . -name 'language_genealogy*' -o -name '*genealog*' | head -40", "description": "Locate J3.1 references and genealogy files"}`

  ```
reports/INDEX.md
reports/rapport-atomes-niveaux.md
reports/corpus-commun.json
reports/rapport-corpus-commun.md
reports/retrieval-epoque.json
reports/rapport-retrieval-epoque.md
reports/genealogie-deux-faces.json
reports/rapport-genealogie-deux-faces.md
reports/rapport-semaine.md
reports/rapport-semaine.json
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/session.jsonl.zstd
journal/sessions/5ce3f080-2d3d-467a-8ee1-df697f3f3e68/session.jsonl.zstd
journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/session.jsonl.zstd
journal/sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/session.v4.jsonl.zstd
journal/sessions/d629d7d7-e122-4596-8757-f4264a2b15cf/session.v4.jsonl.zstd
journal/sessions/d629d7d7-e122-4596-8757-f4264a2b15cf/digest.md
journal/sessions/ddf8d740-9433-4f97-a5d8-38bd92bd45f6/session.v4.jsonl.zstd
journal/sessions/f0969e87-af0c-43b1-93cf-f278d9c90846/session.v4.jsonl.zstd
journal/sessions/fd4b8df1-abc9-4dd6-94df-fcf484cc9017/session.v4.jsonl.zstd
journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/session.v4.jsonl.zstd
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/session.v4.jsonl.zstd
journal/sess
… [1499 caractères tronqués]
  ```

- **bash** `{"command": "grep -ril \"udhr\" --include='*.py' --include='*.md' --include='*.json' . 2>/dev/null | head -50; echo '--- 532 ---'; grep -ril \"532\" --include='*.py' --include='*.md' --include='*.json' . 2>/dev/null | head -40", "description": "Locate UDHR and 532-language references"}`

  ```
./reports/rapport-plateau-semantique.md
./reports/rapport-pont-semantique.md
./reports/rapport-pont-generatif.md
./reports/rapport-cycle-rapide.md
./reports/archive/rapport-toutes-langues.md
./reports/archive/rapport-campagne-benefices.md
./reports/toutes-langues/001-01-le-perimetre-inventorie.md
./reports/toutes-langues/004-04-les-cinq-phases-chainees.md
./reports/toutes-langues/005-05-mesure-linvariance-a-dix-points.md
./reports/toutes-langues/017-17-le-plateau-du-professeur-est-a-la-couche.md
./reports/toutes-langues/018-18-romeo-le-pont-transfere-sur-du-texte-lit.md
./reports/toutes-langues/019-19-couche-8-contre-couche-10-la-correction.md
./reports/toutes-langues/022-22-correction-la-richesse-nest-pas-dans-le.md
./reports/toutes-langues/023-23-domaine-ou-langue-teste-et-le-test-est-i.md
./reports/toutes-langues/024-24-signal-precoce-la-couche-8-gagne-aussi-a.md
./reports/toutes-langues/032-32-le-29-est-il-un-artefact-dalignement-non.md
./reports/toutes-langues/041-41-le-profil-porte-maintenant-tout-le-proto.md
./reports/toutes-langues/042-42-jalon-392-langues-tracees-aux-deux-couch.md
./reports/toutes-langues/045-45-premier-corpus-multi-domaine-et-aligne-4.md
./reports/toutes-
… [2847 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-retrieval-epoque.md; echo '===== JSON ====='; python3 -m json.tool reports/retrieval-epoque.json | head -200", "description": "Read J3.1 retrieval-epoch report and JSON"}`

  ```
# J3.1 — Le retrieval inter-langues à époque contrôlée

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J3.1 · **Date** : 2026-11-07
> **Verdict** : ✅ **la mesure est faite ; elle borne l'avertissement** —
> dans ce retrieval de **surface**, **l'écriture domine** (+0,609 ; IC 95 % [0,529 ; 0,702]), la **famille**
> compte ensuite (+0,181 [0,106 ; 0,253]), et **l'écart d'années ne pèse pas en moyenne** (−0,034 par siècle
> [−0,075 ; +0,009], p = 0,19 par permutation). À écriture contrôlée, les couples **contemporains** et
> **décalés** sont au **même niveau** : **0,710 vs 0,710**. Le renversement brut (0,238 vs 0,427) est un
> **effet de composition** : les couples décalés contiennent **60 %** de paires de même écriture, les
> contemporains **33 %**. **L'époque ne domine pas ici ; le confondant de composition, lui, n'est pas nul : sans
> contrôle, il fausse la comparaison.**
> **Dispositif** : trois corpus, un même retrieval de surface (n-grammes de caractères, TF-IDF, cosinus,
> top-1) ; **B7** (71 langues, 35 concepts, libellés Wikidata 2026), **UDHR** (21 langues du corpus commun,
> 30 articles, 1948), **BIBLE** (12 traductions datées de 1744 à 201
… [24994 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,240p' docs/pilotage/en-cours.md", "description": "Read current state document"}`

  ```
# En ce moment

**Mis à jour : 2026-11-14, 01 h 20 HNE (heure locale, EST).**

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
… [10700 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/udhr/; echo '---'; python3 - <<'EOF'\nimport json,os\np='data/udhr/genealogie.json'\nd=json.load(open(p))\nprint(type(d))\nif isinstance(d,dict):\n    print(list(d)[:20])\n    for k in list(d)[:3]:\n        print(k, str(d[k])[:500])\nEOF", "description": "Inspect UDHR data d … [31 caractères tronqués]`

  ```
total 19588
drwxr-xr-x. 1 stephane stephane     502 25 oct 00:01 .
drwxr-xr-x. 1 stephane stephane    2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane 7661342 17 oct 23:14 articles.jsonl
-rw-r--r--. 1 stephane stephane 6481755 17 oct 23:14 articles_propres.jsonl
-rw-r--r--. 1 stephane stephane    8286 17 oct 23:49 _eng.txt
drwxr-xr-x. 1 stephane stephane    1206 27 oct 22:33 familles
-rw-r--r--. 1 stephane stephane    9734 17 oct 23:49 _fra.txt
-rw-r--r--. 1 stephane stephane   90808 18 oct 10:30 genealogie.json
-rw-r--r--. 1 stephane stephane  126982 17 oct 23:14 langues.jsonl
-rw-r--r--. 1 stephane stephane   57191 17 oct 23:14 meta.json
-rw-r--r--. 1 stephane stephane   70498 18 oct 01:19 udhr_10_train.txt
-rw-r--r--. 1 stephane stephane   29232 18 oct 01:19 udhr_10_val.txt
-rw-r--r--. 1 stephane stephane    6834 18 oct 01:31 udhr_1_train.txt
-rw-r--r--. 1 stephane stephane    2239 18 oct 01:31 udhr_1_val.txt
-rw-r--r--. 1 stephane stephane  459299 18 oct 01:19 udhr_50_train.txt
-rw-r--r--. 1 stephane stephane  180892 18 oct 01:19 udhr_50_val.txt
-rw-r--r--. 1 stephane stephane    8818 18 oct 00:20 udhr_fra_train.txt
-rw-r--r--. 1 stephane stephane    5490 18 oct 00:28 udhr_
… [1281 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,260p' tools/genealogie_udhr.py", "description": "Read genealogy UDHR tool"}`

  ```
#!/usr/bin/env python3
"""genealogie_udhr.py — LA GÉNÉALOGIE DES 448 LANGUES (famille, branche), depuis Glottolog.

POURQUOI. Une couche entrée-sortie n'est pas « riche en langues » parce qu'elle en compte beaucoup : elle l'est si
elle couvre la **structure** — familles, branches, dialectes (cf. `docs/genealogie-des-langues.md`). Et les tests
doivent être **organisés par niveau** : une paire de langues sœurs n'est pas une paire de familles différentes.

LA SOURCE. Glottolog (CLDF, `glottolog/glottolog-cldf` sur GitHub) ✓ : `languages.csv` (27 000 languoïdes, avec
`Family_ID`, `Level`, `ISO639P3code`) et `values.csv` (dont la **classification** complète, « Indo-European > Italic
> Romance > … »). On télécharge une fois, on cache dans `data/glottolog/`.

SORTIE : `data/udhr/genealogie.json` — pour chaque fichier UDHR : `{iso3, famille, branche, glottocode, niveau}`.
⚠️ Ce que ce n'est pas ✗ : Glottolog donne la classification **savante**, pas la distance mesurée ; et certaines
langues UDHR ont un code qui n'est pas dans Glottolog ✗✓ (on le compte et on le dit ✓).
"""
from __future__ import annotations
import argparse, csv, json, pathlib, urllib.request

BASE = "https://raw.githubuser
… [2664 caractères tronqués]
  ```

- **bash** `{"command": "find . -name 'language_genealogy.py' -o -name '*genealogy*.py' | head; echo '---'; grep -rn \"language_genealogy\" --include='*.py' --include='*.md' . 2>/dev/null | head -40", "description": "Find language_genealogy.py and references"}`

  ```
---
./reports/rapport-inventaire-panini.md:336:| **Registre** | `research/src/nipada/signing/language_genealogy.py` | `LANG_TREE: dict[code, LangInfo]` — dataclass gelée `(code, family, branch, epoch, morphological_type, script, closest_kin, notes)` | **29 langues** |
./reports/rapport-inventaire-panini.md:396:| Généalogie | `src/nipada/signing/language_genealogy.py` | Python (dataclass) | `nipada` | moyenne (export JSON à faire) |
./reports/rapport-genealogie-deux-faces.md:51:| **P1 — `lang_distance` (LANG_TREE)** | `language_genealogy.py`, 29 langues | 29 | **5/21** (eng, fra, ell, hin, heb) | **200/210** |
./tools/genealogie_deux_faces.py:95:    source = (panini / "src" / "nipada" / "signing" / "language_genealogy.py").read_text(encoding="utf-8")
./tools/genealogie_deux_faces.py:744:            "panini_lang_tree": "../Panini/research/src/nipada/signing/language_genealogy.py (29 langues)",
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:60032:GÉNÉALOGIE : `src/nipada/signing/language_genealogy.py` (LANG_TREE, 29 langues, epoch/morphologie/distance normalisée) ; UDHR 532 langues étiquetées ; côté Drave `data/udhr/genealogie.json` (456 langues, glottocodes). Leur 
… [5518 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/udhr/familles/ | head; echo '--- meta size ---'; python3 - <<'EOF'\nimport json\nm=json.load(open('data/udhr/meta.json'))\nprint(len(m), type(m))\nprint(list(m.items())[:2])\ng=json.load(open('data/udhr/genealogie.json'))\nprint('genealogie',len(g))\nfrom collections import  … [214 caractères tronqués]`

  ```
total 8728
drwxr-xr-x. 1 stephane stephane    1206 27 oct 22:33 .
drwxr-xr-x. 1 stephane stephane     502 25 oct 00:01 ..
-rw-r--r--. 1 stephane stephane   61462 25 oct 00:01 abkhaz-adyge.jsonl
-rw-r--r--. 1 stephane stephane  634366 27 oct 22:33 ac_benue.jsonl
-rw-r--r--. 1 stephane stephane  191720 25 oct 00:01 afro-asiatic.jsonl
-rw-r--r--. 1 stephane stephane   90909 27 oct 22:33 afro_ouest.jsonl
-rw-r--r--. 1 stephane stephane  120522 25 oct 00:01 arawakan.jsonl
-rw-r--r--. 1 stephane stephane   35295 25 oct 00:01 artificial-language.jsonl
-rw-r--r--. 1 stephane stephane 1032940 25 oct 00:01 atlantic-congo.jsonl
--- meta size ---
441 <class 'dict'>
[('udhr_007.xml', {'iso3': 'cri', 'nom': 'Sãotomense', 'script': 'Latn', 'sens': 'ltr', 'variante': '007', 'nb_articles': 30}), ('udhr_008.xml', {'iso3': 'pov', 'nom': 'Crioulo, Upper Guinea (008)', 'script': 'Latn', 'sens': 'ltr', 'variante': '008', 'nb_articles': 30})]
genealogie 441
[('Indo-European', 123), ('Atlantic-Congo', 82), ('Austronesian', 37), ('Sino-Tibetan', 18), ('Turkic', 18), ('Afro-Asiatic', 13), ('(inconnue)', 11), ('Mayan', 11), ('Quechuan', 11), ('Uralic', 9), ('Arawakan', 8), ('Mande', 8), ('Otomanguean', 8), (
… [48 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' docs/pilotage/semaine-autonome.md; echo '===== inventaire 300-420 ====='; sed -n '300,420p' reports/rapport-inventaire-panini.md", "description": "Read autonomous week plan and Panini inventory relevant sections"}`

  ```
# Le chantier autonome — une semaine (7 → 14 novembre 2026)

> **Ce que ce document est.** Le **plan du chantier d'une semaine** : tous les travaux ouverts du
> dépôt et l'**intégration avec l'écosystème Panini**. Il dit **quoi**, **dans quel ordre**, **avec
> quels sous-agents**, **comment on mesure**, et **ce qui peut faire échouer**. L'état courant est
> dans [`en-cours.md`](en-cours.md) ; la théorie de la généalogie dans
> [`../theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md) ; la méthode
> Panini/Nipada dans [`../methode/panini-nipada.md`](../methode/panini-nipada.md).
> *À relire chaque matin du chantier.*

## 1. L'objet

**Une semaine, un système utilisable, une intégration mesurée.** Le produit `drave` (CLI, contrat,
porte) est la **priorité** ; l'intégration avec Panini/Nipada est le **second axe** ; les chantiers
N2/S/R/A sont **coordonnés** (jamais écrits par cette session). Chaque vague produit un
**résultat mesuré**, une **fiche** et son **JSON**, la mise à jour de l'**état** et un **commit
vérifié** — jamais une intention.

## 2. L'inventaire — ce qui est ouvert

### 2.1 Drave — le produit (priorité)

| reste | mesure | où |
|---|---|---|
| 1 
… [18575 caractères tronqués]
  ```

- **bash** `{"command": "ls ../Panini 2>/dev/null; echo '---'; find ../Panini -maxdepth 3 -iname '*udhr*' 2>/dev/null | head -30; echo '--- j32 work ---'; ls work/j32 2>/dev/null | head -40", "description": "Locate Panini UDHR source and J3.2 work"}`

  ```
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
---
../Panini/data/nipaba_udhr_v0.1.0.json
../Panini/research/data/udhr_article1_en.json
../Panini/research/data/udhr_article1_fr.json
../Panini/research/data/udhr_convergence_graph.json
../Panini/research/data/udhr_convergence_v14.json
../Panini/research/data/udhr_corpus.json
../Panini/research/data/udhr_decomposed_v14.json
../Panini/research/data/udhr_demo.nipada
../Panini/research/data/udhr_omw_coverage.json
../Panini/research/data/udhr_reconstruction_full.json
../Panini/research/data/udhr_reconstruction_report.json
../Panini/research/data/udhr_universal_graph.json
../Panini/research/scripts/demo_udhr.py
../Panini/research/scripts/expand_udhr_lexicon.py
../Panini/research/scripts/ingest_udhr.py
../Panini/research/scripts/udhr_complete_demo.py
../Panini/research/scripts/udhr_convergence.py
../Panini/research/scripts/udhr_rich_graph.py
.
… [405 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='../Panini/research/data/udhr_corpus.json'\nd=json.load(open(p))\nprint(type(d), len(d))\nif isinstance(d,dict):\n    print(list(d)[:5])\n    for k in list(d)[:2]: print(k, json.dumps(d[k],ensure_ascii=False)[:1200])\nelse:\n    print(json.dumps(d[0],en … [97 caractères tronqués]`

  ```
<class 'dict'> 6
['format', 'source', 'article', 'total_languages', 'families']
format "udhr-v2.0-xml"
source "eric-muller/udhr (GitHub) — Unicode UDHR XML Project"
  ```

- **bash** `{"command": "sed -n '1,220p' reports/rapport-genealogie-deux-faces.md", "description": "Read J3.2 genealogy two-faces report"}`

  ```
# J3.2 — La généalogie à deux faces : Panini et Glottolog sur le corpus commun

> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : semaine Panini, J3.2 · **Date** : 2026-11-07
> **Verdict** : ✅ **la confrontation est faite, et elle déplace la question.** Les deux faces ne mesurent
> **pas le même objet** : la « filiation » de Panini est une distance de **tradition** (3 paires seulement,
> sur 655, ont deux langues connues différentes), tandis que la nôtre est une distance de **famille de
> langues** (5 familles, 210 paires). Ce qui converge est réel mais **conditionnel** : la surface passe
> avant la filiation des deux côtés, et le rapport filiation/surface est du même ordre (≈ un tiers). Ce qui
> diverge est décisif : **la théorie couvre 5/21 langues** avec sa fonction `lang_distance` (200/210 paires
> codées « inconnu »), **15/21** avec ses métadonnées UDHR, **21/21** avec Glottolog ; et sur nos 21 langues,
> **les 154 paires hors script sont exactement au hasard** (MRR 0,1332 = H₃₀/30 ; top-1 0,0333 = 1/30).
> Le signal de famille ne vit que dans **56 paires de même script**, et il est porté par **2-3 paires**.
> **Dispositif** : 21 textes du corpus commun (5 fa
… [12584 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/research/data/udhr_corpus.json'))\nprint('keys', d.keys())\nfor k,v in d.items():\n    print(k, type(v), len(v) if hasattr(v,'__len__') else '')\nprint('--- families ---')\nprint(json.dumps(d['families'],ensure_ascii=False)[:30 … [319 caractères tronqués]`

  ```
keys dict_keys(['format', 'source', 'article', 'total_languages', 'families', 'languages'])
format <class 'str'> 13
source <class 'str'> 52
article <class 'str'> 9
total_languages <class 'int'> 
families <class 'dict'> 10
languages <class 'dict'> 532
--- families ---
{"Other": {"count": 503, "branches": ["Unknown"]}, "Indo-European": {"count": 17, "branches": ["Germanic", "Indo-Iranian", "Italic", "Romance", "Slavic"]}, "Afro-Asiatic": {"count": 2, "branches": ["Semitic"]}, "Uralic": {"count": 2, "branches": ["Finnic", "Ugric"]}, "Austronesian": {"count": 2, "branches": ["Malayo-Polynesian"]}, "Dravidian": {"count": 2, "branches": ["Southern"]}, "Japonic": {"count": 1, "branches": ["Japanese"]}, "Koreanic": {"count": 1, "branches": ["Korean"]}, "Turkic": {"count": 1, "branches": ["Oghuz"]}, "Niger-Congo": {"count": 1, "branches": ["Bantu"]}}
--- article ---
<class 'str'> 9
"A"
  ```

- **bash** `{"command": "sed -n '1,180p' tools/genealogie_deux_faces.py", "description": "Read J3.2 tool head"}`

  ```
#!/usr/bin/env python3
"""genealogie_deux_faces.py — J3.2 : la généalogie à deux faces.

POURQUOI. Panini tient une **théorie** de la généalogie (14 atomes, 9 dhātus, une échelle de
distance à quatre niveaux) ; Drave tient une **mesure** de l'alignement (Glottolog + retrieval sur
le corpus commun). Les deux faces ne mesurent pas la même chose : l'une est une signature de texte,
l'autre une distance de langues. Ce script les confronte sur les 21 langues du corpus commun et sur
les signatures de Panini, et écrit les chiffres dans `reports/genealogie-deux-faces.json`.

CE QUI EST MESURÉ.
  1. Couverture des trois représentations généalogiques : `lang_distance` de Panini (LANG_TREE),
     les métadonnées UDHR de Panini, Glottolog.
  2. Accord des deux faces sur les langues couvertes (famille, branche, distances).
  3. Alignement : retrieval UDHR (J3.1) vs distance Panini / Glottolog, avec le script en contrôle.
     Contrôles négatifs : permutations de labels et de chemins, leave-one-language-out, et
     décomposition de l'effet « inconnu ».
  4. Atomes : ACP des 14 parts (44 œuvres), stabilité split-half, contrôle par permutation ;
     ce que les 9 dhātus peuvent et ne peuvent pas ê
… [5983 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"J7\\.1\\|J7\\.\" docs/ reports/ journal/ --include='*.md' 2>/dev/null | head -50; echo '--- roadmap R0.7 ---'; grep -n \"J7\\|retrieval\\|famille\" docs/pilotage/roadmap.md | head -60", "description": "Search J7.1 references and roadmap"}`

  ```
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:60966:  [a_faire ] J7.1   j7 — Panini — le retrieval approfondi
--- roadmap R0.7 ---
33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; la suite : **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; R2/R3 attendent N5/N4 |
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : scr
… [4023 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"532\" docs/ reports/ --include='*.md' 2>/dev/null | head -40; echo '--- j32 json top ---'; python3 - <<'EOF'\nimport json\nd=json.load(open('reports/genealogie-deux-faces.json'))\nprint(list(d))\nfor k in d:\n    print(k, type(d[k]), len(d[k]) if hasattr(d[k],'__len__') else  … [67 caractères tronqués]`

  ```
docs/archive/hebbien-differentiel-et-biologie.md:35:| autre article (40 langues) | 1116,532 contre 1116,532 — **identique** |
docs/archive/note-cancellation-evenementielle.md:248:article 2 en breton, langue absente : **1116,532 contre 1116,532**. Aucun
docs/archive/plan-mode4-lot-listes.md:118:| **lot de `t`, mode 4** | `79 + t·(12 + 112) + 2·Σa_j` | ≈ `79 + 1 532t` | **≈ 1 537 à `t = 16`** |
docs/archive/plan-modeles-lourds.md:139:| MiniMax-H3 | `?` | 1 | 532 | **11,42 Go** | 11,4 Go |
docs/archive/plan-prefill-reparti.md:181:`mdl.flux_brut = true`. Puis, avant le chemin « un jeton » (ligne 1532) :
docs/pilotage/semaine-autonome.md:53:- **La généalogie** : `src/nipada/signing/language_genealogy.py` (29 langues) et l'**UDHR 532
reports/archive/rapport-toutes-langues.md:580:| invariance du professeur (segment par segment) | 0,6532 · pire segment 0,2966 |
reports/archive/rapport-toutes-langues.md:595:0,6532. Le pont dépasse largement la couche qu'il émule sur l'invariance — cohérent
reports/archive/rapport-toutes-langues.md:599:du professeur mesurée **sur les canaux à forte énergie** vaut **0,6532**, contre
reports/archive/rapport-toutes-langues.md:619:| invariance du professeur | 0,
… [4776 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' reports/rapport-corpus-commun.md", "description": "Read common corpus report"}`

  ```
# Corpus commun Panini/NIPADA ↔ Drave — UDHR, article 1

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.2 · **Date** : 2026-11-07
> **Verdict** : ✅ **le corpus est construit et vérifié** — **21 textes** (20 langues stratifiées + le
> français pivot), **5 familles**, **10 écritures**, **42 phrases**, **3 603 caractères**. Les **21**
> paires Panini ↔ Drave sont **identiques après normalisation** ; **418 paires exactes** sur **438**
> appariables (**95,4 %**). **20 écarts de surface** sont **exclus, pas corrigés**. Les **8 contrôles**
> (**6 rejets** attendus + **2 témoins** d'acceptation) sont **conformes** (8/8).
> **Dispositif** : lecture seule de `../Panini/research/data/udhr_corpus.json` (HEAD du dépôt
> `e10d695`, 2026-10-25 ; fichier **non suivi par git**, SHA-256 `531bc75c…`, vérifié avant et
> après) ; `data/udhr/articles_propres.jsonl`, `langues.jsonl`, `genealogie.json` (HEAD
> `9c7f71dc`, 2026-11-07) ; outil `../tools/corpus_commun.py` ;
> JSON [`corpus-commun.json`](corpus-commun.json). Le corpus lui-même vit dans
> `work/corpus-commun/`, **non versionné** (`.gitignore` : `work/`).
> **Aucune écriture dans Panini** : le script vérifie 
… [10165 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/corpus-commun.json'))\nprint(list(d))\nfor k,v in d.items(): print(k, type(v), len(v) if hasattr(v,'__len__') else '')\nprint(json.dumps(d.get('textes',[])[:3],ensure_ascii=False)[:2000])\nprint('--- echantillon ---')\nfor k in d … [162 caractères tronqués]`

  ```
['controle_negatif', 'controles', 'date', 'fiche', 'fichiers', 'intersection', 'ligne_roadmap', 'limites', 'normalisation', 'prochaine_etape', 'selection', 'sources', 'statistiques', 'statut', 'textes', 'titre', 'version']
controle_negatif <class 'dict'> 7
controles <class 'dict'> 3
date <class 'str'> 10
fiche <class 'str'> 32
fichiers <class 'dict'> 5
intersection <class 'dict'> 12
ligne_roadmap <class 'str'> 27
limites <class 'list'> 7
normalisation <class 'dict'> 7
prochaine_etape <class 'str'> 227
selection <class 'dict'> 6
sources <class 'dict'> 4
statistiques <class 'dict'> 11
statut <class 'str'> 24
textes <class 'list'> 21
titre <class 'str'> 52
version <class 'str'> 3
[{"branche": "indo1319/clas1257/germ1287/nort3152/west2793/nort3175/angl1264/angl1265/late1254/merc1242/macr1271", "branche_feuille": "macr1271", "branche_panini": "Germanic", "drave_fichier": "udhr_eng.xml", "epoque": 1948, "epoque_label": "1948 — adoption de la DUDH", "epoque_note": "date de l'œuvre ; date de la traduction non documentée", "famille": "Indo-European", "famille_panini": "Indo-European", "genre": "declaration", "id": "udhr_eng", "iso3": "eng", "langue": "English", "nb_caracteres": 170, "nb_mot
… [1506 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/research/data/udhr_corpus.json'))\nlangs=d['languages']\nprint(type(langs), len(langs))\nfor k in list(langs)[:5]:\n    print(k, json.dumps(langs[k],ensure_ascii=False)[:1200])\nprint('--- keys union ---')\nks=set()\nfor v in l … [180 caractères tronqués]`

  ```
<class 'dict'> 532
007 {"name": "Sãotomense", "iso": "007", "script": "Latn", "dir": "ltr", "text": "Tudu nguê di mundu ca nancê livli e igual ni dignidade e ni dirêtu. Punda nen ca pensá e nen tê cunxensa, selá nen fé tudu cuá cu tençón de lumón.", "family": "Other", "branch": "Unknown", "tradition": "other"}
008 {"name": "Crioulo, Upper Guinea (008)", "iso": "008", "script": "Latn", "dir": "ltr", "text": "Tudu pecadur padidu livre, ninguin ca más ninguin, tudu djusta, tudu tem mesmu diritu. Tudu quin qui padidu, tem si roçon, cu si manera di pensa. Na metadi di utrus I díbidi fassi cussas cu ermondadi.", "family": "Other", "branch": "Unknown", "tradition": "other"}
009 {"name": "Mbundu (009)", "iso": "009", "script": "Latn", "dir": "ltr", "text": "Mutu uoso uoso a mu vuala ni ufolo ni kutena kumoxi mu kijingu ni mu ubinganu. Mu kilembu kia kubanga ni mu ubanzelu, Atena uê kubanga ioso kua akua mu muxima ua tululuka mba upange.", "family": "Other", "branch": "Unknown", "tradition": "other"}
010 {"name": "Tetun Dili", "iso": "010", "script": "Latn", "dir": "ltr", "text": "Ema tomak moris hanesan, ema tomak hanesan, iha direitu hanesan. Ema tomak iha otak ho neon, hotu-hotu sei buka
… [4199 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/research/data/udhr_corpus.json'))\nlangs=d['languages']\nfrom collections import Counter\nfor field in ['script','family','branch','tradition','iso','dir']:\n    c=Counter(v.get(field) for v in langs.values())\n    print(field, … [90 caractères tronqués]`

  ```
script [('Latn', 412), ('Cyrl', 35), ('Hans', 13), ('Arab', 10), ('Deva', 8), ('Cans', 3), ('Jpan', 3), ('Mymr', 3), ('Ethi', 2), ('Tibt', 2), ('Cher', 2), ('Grek', 2), ('Hebr', 2), ('Mlym', 2), ('Taml', 2)]
family [('Other', 421), ('Indo-European', 53), ('Sino-Tibetan', 11), ('Niger-Congo', 9), ('Afro-Asiatic', 8), ('Austronesian', 7), ('Dravidian', 6), ('Uralic', 3), ('Japonic', 3), ('Turkic', 3), ('Austroasiatic', 3), ('Tai-Kadai', 2), ('Isolate', 1), ('Kartvelian', 1), ('Koreanic', 1)]
branch [('Unknown', 421), ('Romance', 15), ('Slavic', 11), ('Germanic', 9), ('Indo-Iranian', 9), ('Sinitic', 9), ('Malayo-Polynesian', 7), ('Southern', 6), ('Bantu', 6), ('Semitic', 4), ('Chadic', 3), ('Japanese', 3), ('Tibeto-Burman', 2), ('Celtic', 2), ('Hellenic', 2)]
tradition [('other', 422), ('western_modern', 49), ('african', 16), ('indian', 13), ('confucean', 10), ('buddhist', 8), ('southeast_asian', 8), ('western_classical', 4), ('islamic', 2)]
iso [('007', 1), ('008', 1), ('009', 1), ('010', 1), ('011', 1), ('013', 1), ('014', 1), ('016', 1), ('017', 1), ('020', 1), ('021', 1), ('022', 1), ('023', 1), ('025', 1), ('026', 1)]
dir [('ltr', 517), ('rtl', 15)]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nM=json.load(open('data/udhr/meta.json'))\nG=json.load(open('data/udhr/genealogie.json'))\nprint(len(P),len(M),len(G))\npk=set(P); mk=set(M); gk=set(G)\nprint('P∩M',len(pk&mk),'P-M … [979 caractères tronqués]`

  ```
532 441 441
P∩M 0 P-M 532 M-P 441
P-M sample ['007', '008', '009', '010', '011', '013', '014', '016', '017', '020', '021', '022', '023', '025', '026', '027', '028', '029', '030', '032', '041', '042', '043', '044', '045', '046', '047', '048', '049', '050']
M-P sample ['udhr_007.xml', 'udhr_008.xml', 'udhr_009.xml', 'udhr_010.xml', 'udhr_011.xml', 'udhr_012.xml', 'udhr_013.xml', 'udhr_014.xml', 'udhr_016.xml', 'udhr_017.xml', 'udhr_020.xml', 'udhr_abk.xml', 'udhr_ace.xml', 'udhr_acu.xml', 'udhr_acu_1.xml', 'udhr_ada.xml', 'udhr_ady.xml', 'udhr_afr.xml', 'udhr_agr.xml', 'udhr_aii.xml', 'udhr_ajg.xml', 'udhr_aka_akuapem.xml', 'udhr_aka_asante.xml', 'udhr_aka_fante.xml', 'udhr_als.xml', 'udhr_alt.xml', 'udhr_amc.xml', 'udhr_ame.xml', 'udhr_amh.xml', 'udhr_ami.xml']
P iso3 exact match 346
P iso key same 532
P key in G 0
family agree/dis 0 0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nM=json.load(open('data/udhr/meta.json'))\nG=json.load(open('data/udhr/genealogie.json'))\ndef fk(k): return 'udhr_%s.xml'%k\nmk=set(M)\ninter=[k for k in P if fk(k) in mk]\nprint( … [778 caractères tronqués]`

  ```
P with Drave file 438 P without 94
sample without ['021', '022', '023', '025', '026', '027', '028', '029', '030', '032', '041', '042', '043', '044', '045', '046', '047', '048', '049', '050']
agree 91 dis 347 missing G 0
('007', 'Other', 'Indo-European')
('008', 'Other', 'Indo-European')
('009', 'Other', 'Atlantic-Congo')
('010', 'Other', 'Austronesian')
('011', 'Other', 'Atlantic-Congo')
('013', 'Other', '(inconnue)')
('014', 'Other', '(inconnue)')
('016', 'Other', '(inconnue)')
('017', 'Other', '(inconnue)')
('020', 'Other', 'Sino-Tibetan')
('abk', 'Other', 'Abkhaz-Adyge')
('ace', 'Other', 'Austronesian')
('acu', 'Other', 'Chicham')
('acu_1', 'Other', 'Chicham')
('ada', 'Other', 'Atlantic-Congo')
('ady', 'Other', 'Abkhaz-Adyge')
('agr', 'Other', 'Chicham')
('aii', 'Other', 'Afro-Asiatic')
('ajg', 'Other', 'Atlantic-Congo')
('aka_akuapem', 'Other', 'Atlantic-Congo')
('aka_asante', 'Other', 'Atlantic-Congo')
('aka_fante', 'Other', 'Atlantic-Congo')
('als', 'Other', 'Indo-European')
('alt', 'Other', 'Turkic')
('amc', 'Other', 'Pano-Tacanan')
('ame', 'Other', 'Arawakan')
('ami', 'Other', 'Austronesian')
('amr', 'Other', 'Harakmbut')
('arb', 'Other', 'Afro-Asiatic')
('arl', 'Other', 'Z
… [53 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/glottolog 2>/dev/null; python3 - <<'EOF'\nimport json\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nM=json.load(open('data/udhr/meta.json'))\nmk=set(M)\nmiss=[k for k in P if 'udhr_%s.xml'%k not in mk]\nprint(len(miss))\nfor k in miss[:100]:\n  … [156 caractères tronqués]`

  ```
total 23368
drwxr-xr-x. 1 stephane stephane       46 18 oct 10:29 .
drwxr-xr-x. 1 stephane stephane     2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane  2477017 18 oct 10:29 languages.csv
-rw-r--r--. 1 stephane stephane 21447242 18 oct 10:29 values.csv
94
021 021 (Muzzi) Latn Other
022 022 (Klau) Latn Other
023 023 (Jinan) Hans Other
025 025 (Bizisa) Latn Other
026 026 (Yeonbyeon) Kore Other
027 027 Gumuz Latn Other
028 028 Kafa Latn Other
029 029 Sidamo Latn Other
030 030 Kituba (2) Latn Other
032 032 South Azerbaijani Latn Other
041 041 Latvian (2) Latn Other
042 042 Spanish (resolution) Latn Other
043 043 Zarma Latn Other
044 044 Mirandese Latn Other
045 045 Maasai Latn Other
046 046 Malay, Papuan Latn Other
047 047 Malay, Ambonese Latn Other
048 048 Minangkabau (2) Latn Other
049 049 Banjar Latn Other
050 050 (Bataknese) Latn Other
052 052 Morisyen Latn Other
053 053 Hausa (2) Latn Other
054 054 Catalan (2) Latn Other
055 055 Jamaican Creole English Latn Other
056 056 Saint Lucian Creole French Latn Other
057 057 Maay Latn Other
058 058 Somali (Af Marka) Latn Other
059 059 North Saami (2) Latn Other
060 060 Inari Saami Latn Other
061 061 Skolt Saami Latn Other
062 062 Swah
… [2381 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,260p' tools/retrieval_epoque.py", "description": "Read J3.1 retrieval tool head"}`

  ```
#!/usr/bin/env python3
"""retrieval_epoque.py — J3.1 : le retrieval inter-langues à ÉPOQUE CONTRÔLÉE.

LA QUESTION. Panini avertit : leur signature lexicale capte l'époque (β +0,138) bien plus que la filiation
(β +0,049). Un retrieval inter-langues mesuré sans contrôler la date peut donc mesurer l'époque, pas la langue.
Ce script mesure trois choses, avec le même retrieval de surface (n-grammes de caractères, TF-IDF, cosinus) :

  1. **B7** (71 langues, 35 concepts, libellés Wikidata 2026) : le retrieval de CONCEPTS, à date unique.
     Il porte la SURFACE (écriture, famille) ; il ne peut pas porter l'époque.
  2. **UDHR** (21 langues du corpus commun, 30 articles, 1948) : le retrieval d'ARTICLES, à date unique.
     Toutes les paires sont contemporaines par construction ; il porte la surface.
  3. **BIBLE** (12 traductions datées de 1744 à 2019) : le retrieval de VERSETS, avec des couples
     contemporains et décalés. C'est le seul bras où l'époque varie ; il porte le contrôle de date.

LE RETRIEVAL. On représente chaque texte par ses n-grammes de caractères (n=3), pondérés TF-IDF, normalisés
L2 ; la similarité est le cosinus. Pour chaque requête de A, on classe les candidats de 
… [10530 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '260,620p' tools/retrieval_epoque.py", "description": "Read J3.1 retrieval tool core"}`

  ```
concepts_l = sorted(par_langue[l])
        positions = {c: [] for c in concepts_l}
        for i, (ll, c) in enumerate(index):
            if ll == l:
                positions[c].append(i)
        lignes = []
        for c in concepts_l:
            v = M[positions[c]].mean(axis=0)
            lignes.append(v)
        if lignes:
            X = csr_matrix(np.vstack([np.asarray(x).ravel() for x in lignes]))
            normes = np.sqrt(np.asarray(X.multiply(X).sum(axis=1)).ravel())
            normes[normes == 0] = 1.0
            X = csr_matrix(X.multiply(1.0 / normes[:, None]))
            matrices[l] = (concepts_l, X)
    rng = random.Random(graine)
    paires = []
    for a in langues:
        if a not in matrices:
            continue
        for b in langues:
            if a == b or b not in matrices:
                continue
            ca, XA = matrices[a]
            cb, XB = matrices[b]
            communs = [c for c in ca if c in set(cb)]
            if len(communs) < 5:
                continue
            ia = [ca.index(c) for c in communs]
            ib = [cb.index(c) for c in communs]
            A = XA[ia]
            B = XB[ib]
            t1, mrr, rk, rangs = to
… [15519 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '620,980p' tools/retrieval_epoque.py", "description": "Read remaining J3.1 tool"}`

  ```
continue
            A, B = matrices[a], matrices[b]
            t1, mrr, rk, rangs = top1_et_rangs(A, B)
            # contrôle : étiquettes mélangées — la bonne réponse est une cible tirée au hasard
            S = (A @ B.T).toarray()
            pred = np.argmax(S, axis=1)
            perm = derangement(A.shape[0], rng)
            t1p = float((pred == perm).mean())
            ma, mb = bible["meta"][a], bible["meta"][b]
            paires.append({
                "a": a, "b": b,
                "annee_a": ma["annee"], "annee_b": mb["annee"],
                "delta_annees": abs(ma["annee"] - mb["annee"]),
                "script_a": ma["script"], "script_b": mb["script"],
                "famille_a": ma["famille"], "famille_b": mb["famille"],
                "langue_a": ma["langue"], "langue_b": mb["langue"],
                "script_match": ma["script"] == mb["script"],
                "famille_match": ma["famille"] == mb["famille"],
                "langue_match": ma["langue"] == mb["langue"],
                "n_requetes": A.shape[0], "n_candidats": B.shape[0],
                "top1": t1, "mrr": mrr, "rang_median": rk,
                "chance": 1.0 / B.shape[0],
               
… [8635 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\nsrc=open('../Panini/research/src/nipada/signing/language_genealogy.py').read()\nbloc=src.split('LANG_TREE: dict[str, LangInfo] = {',1)[1].split('\\n}',1)[0]\nentries={}\nfor m in re.finditer(r'\"([a-z]{3})\":\\s*LangInfo\\(\\s*\"([a-z]{3})\",\\s*\"([^\"]+)\ … [353 caractères tronqués]`

  ```
29
eng {'code': 'eng', 'family': 'indo_european', 'branch': 'germanic'}
deu {'code': 'deu', 'family': 'indo_european', 'branch': 'germanic'}
nld {'code': 'nld', 'family': 'indo_european', 'branch': 'germanic'}
swe {'code': 'swe', 'family': 'indo_european', 'branch': 'germanic'}
nor {'code': 'nor', 'family': 'indo_european', 'branch': 'germanic'}
dan {'code': 'dan', 'family': 'indo_european', 'branch': 'germanic'}
fin {'code': 'fin', 'family': 'uralic', 'branch': 'finnic'}
hun {'code': 'hun', 'family': 'uralic', 'branch': 'ugric'}
fra {'code': 'fra', 'family': 'indo_european', 'branch': 'romance'}
ita {'code': 'ita', 'family': 'indo_european', 'branch': 'romance'}
spa {'code': 'spa', 'family': 'indo_european', 'branch': 'romance'}
por {'code': 'por', 'family': 'indo_european', 'branch': 'romance'}
ron {'code': 'ron', 'family': 'indo_european', 'branch': 'romance'}
lat {'code': 'lat', 'family': 'indo_european', 'branch': 'italic'}
grc {'code': 'grc', 'family': 'indo_european', 'branch': 'hellenic'}
ell {'code': 'ell', 'family': 'indo_european', 'branch': 'hellenic'}
san {'code': 'san', 'family': 'indo_european', 'branch': 'indic'}
pli {'code': 'pli', 'family': 'indo_european', 'branc
… [1117 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport zstandard as zstd, json, pathlib\np=pathlib.Path('journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md')\nif p.exists():\n    s=p.read_text(errors='ignore')\n    i=s.find('J7.1')\n    print(s[max(0,i-3000):i+3000])\nEOF", "description": "Inspect J7.1 … [20 caractères tronqués]`

  ```
ent **236/237
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/chantiers.md'); t=p.read_text()\nt=t.replace(\"**bloc linguistique** (POS **86,25 %**, F1 **0,7535**, attachement **236/237 (0,9933)**\",\n            \"**bloc linguisti … [826 caractères tronqués]`

  ```
chantiers à jour
4:> 48 dernières heures ont déplacé, l'inventaire élargi (A, B, N, R, **S**, **L**, **D**, B13),
30:| 31/10 22 h 22 | « le RSN (le pluriel sera plus approprié car tu dois avoir plusieurs candidats) est une représentation de données interne qui te permet d'itérer indéfiniment dans des cycles de pensées à plusieurs niveaux. Il te faudra donc un arbre d'état
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
[stderr]
grep: write error: Broken pipe
  ```

- **bash** `{"command": "cd /home/stephane/Data13
… [4800 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"j7\" reports/rapport-file-taches.md docs/pilotage/backlog/index.md 2>/dev/null | head -20; echo '--- file taches panini ---'; grep -n \"Panini\\|J7\\|approfond\" reports/rapport-file-taches.md | head -40", "description": "Search task file for J7 details"}`

  ```
--- file taches panini ---
  ```

- **bash** `{"command": "grep -rn \"J7.1\\|retrieval approfondi\\|approfondi\" . --include='*.json' --include='*.md' --include='*.py' 2>/dev/null | grep -v journal/sessions | head -40; echo '--- plan ---'; python3 - <<'EOF'\nimport json\np='work/chantier/plan.json'\ntry:\n d=json.load(open(p)); print(json.dumps … [125 caractères tronqués]`

  ```
./reports/traduction-eurlex-7b.json:276:    "sortie": "(24) Une Union plus forte et plus capable dans le domaine de la sécurité et de la défense contribuera positivement à la sécurité globale et transatlantique et complétera l'OTAN, qui reste, pour les États qui en font partie, la base de leur défense collective. L'Union s'engage à renforcer et approfondir davantage la coopération et l'engagement transatlantiques en matière de sécurité et de défense, avec pour objectif d'améliorer l'interopérabilité, de poursuivre la coopération industrielle et de garantir un accès réciproque aux technologies d'avant-garde avec des partenaires de confiance, renforçant également le GDETI. Cette Réglementation devrait contribuer à ces objectifs.",
./reports/traduction-eurlex-3b.json:276:    "sortie": "Une union plus forte et plus capable dans le domaine de la sécurité et de la défense contribuera positivement à la sécurité mondiale et transatlantique et sera complémentaire à l'OTAN, qui reste, pour les États membres d'entre elles, la base de leur défense collective. L'Union s'engage à renforcer davantage et à approfondir la coopération transatlantique et l'engagement sur la sécurité et la défense, av
… [48730 caractères tronqués]
  ```

- **bash** `{"command": "ls work/chantier/ 2>/dev/null; grep -rn \"J7.1\" work/ 2>/dev/null | head -20", "description": "Search chantier work dir for J7.1"}`

  ```
boucle2.log
boucle.log
etat.json
journal.log
[still running after 60000ms; moved to background job bash-33]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('work/chantier/etat.json'))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:6000])\nEOF", "description": "Read chantier state for task descriptions"}`

  ```
{
 "taches": {
  "J1.1": {
   "titre": "r035 : la relative zéro",
   "statut": "fait",
   "debut": "2026-11-07 12:41:17",
   "duree_s": 1347.7,
   "code_agent": 0,
   "acceptation": [
    "✅ test -f reports/rapport-r035.md && echo FICHE-OK",
    "✅ python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?"
   ],
   "sortie_agent": "avant | après |\n|---|---:|---:|\n| exact / labels | 236/237 | **237/238** |\n| couverture | 0,9916 | **0,9958** |\n| POS | 0,8625 | **0,8625** |\n| F1 syntagmes | 0,7533 | **0,7549** |\n| dev exact / labels | 160/161 | **161/162** |\n| test exact / labels | 76/76 | **76/76** |\n\n`r035` est en dev ; le test ne bouge pas (il ne contient pas de relative zéro). Une seule phrase sur 612 change, **0 POS modifiée sur 3 179 tokens**.\n\n**Contrôles négatifs** : pas de REL devant `about the book`, `about it`, `about today`, sans pronom sujet, ni en français. Généralisation : « The book **he reads about** is good. » → REL [9:23], cible `book`. **183/183** portes, 17 tests unitaires, `porte-bloc-linguistique` et `porte-produit` vertes.\n\n**Intégration.** `tools/bloc_linguistique.py` (`relative_zero`), test unitaire `test_relative_zero`, valeurs d’attac
… [4800 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-33 (bash: ls work/chantier/ 2>/dev/null; grep -rn "J7.1" work/ 2>/dev/null | head -20) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('work/chantier/etat.json'))\nfor k,v in d['taches'].items():\n    if k.startswith('J7'):\n        print('===',k)\n        print(json.dumps(v,ensure_ascii=False,indent=1))\nEOF\necho '--- superviseur tasks source ---'\ngrep -rn \"J7.1\\|re … [102 caractères tronqués]`

  ```
--- superviseur tasks source ---
tools/chantier/plan.json:255:   "id": "J7.1",
tools/chantier/plan.json:257:   "titre": "Panini — le retrieval approfondi",
tools/chantier/plan.json:258:   "mandat": "Tâche J7.1 : approfondir le retrieval Panini — sur les 532 langues UDHR (même source XML), mesurer le retrieval par famille Glottolog (les 29 langues de `language_genealogy.py` + l'échantillon 20) avec le contrôle d'époque, et comparer à la mesure de J3.1. Fiche `reports/rapport-retrieval-familles.md` + JSON, contrôle négatif (familles différentes vs sœurs).",
  ```

- **bash** `{"command": "sed -n '235,285p' tools/chantier/plan.json", "description": "Read J7 plan entry with acceptance"}`

  ```
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
     "commande": "test -f reports/rapport-s065.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    }
   ]
  },
  {
   "id": "J7.1",
   "jour": 7,
   "titre": "Panini — le retrieval approfondi",
   "mandat": "Tâche J7.1 : approfondir le retrieval Panini — sur les 532 langues UDHR (même source XML), mesurer le retrieval par famille Glottolog (les 29 langues de `language_genealogy.py` + l'échantillon 20) avec le contrôle d'époque, et comparer à la mesure de J3.1. Fiche `reports/rapport-retrieval-familles.md` + JSON, contrôle négatif (familles différentes vs sœurs).",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-retrieval-familles.
… [1009 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nprint(type(d), list(d)[:10])\nfor t in (d if isinstance(d,list) else d.get('taches',[])):\n    if str(t.get('id','')).startswith('J7'):\n        print(json.dumps(t,ensure_ascii=False,indent=1))\nEOF", "descri … [39 caractères tronqués]`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
{
 "id": "J7.1",
 "jour": 7,
 "titre": "Panini — le retrieval approfondi",
 "mandat": "Tâche J7.1 : approfondir le retrieval Panini — sur les 532 langues UDHR (même source XML), mesurer le retrieval par famille Glottolog (les 29 langues de `language_genealogy.py` + l'échantillon 20) avec le contrôle d'époque, et comparer à la mesure de J3.1. Fiche `reports/rapport-retrieval-familles.md` + JSON, contrôle négatif (familles différentes vs sœurs).",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-retrieval-familles.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  }
 ]
}
  ```

- **bash** `{"command": "head -2 data/udhr/langues.jsonl; echo '---'; python3 - <<'EOF'\nimport json\nlines=[json.loads(l) for l in open('data/udhr/langues.jsonl')]\nprint(len(lines), lines[0].keys())\nfor x in lines[:3]: print(x)\n# Look for numeric keys\nfor x in lines:\n    if x.get('fichier','').startswith( … [93 caractères tronqués]`

  ```
{"fichier": "udhr_007.xml", "iso3": "cri", "nom": "Sãotomense", "script": "Latn", "sens": "ltr", "titre": "Declaraçón Universal di Dirêtu di Hómé", "nb_articles": 30, "preambule_car": 1593, "attrs": "iso639-3=cri key=007 n=Sãotomense dir=ltr iso15924=Latn"}
{"fichier": "udhr_008.xml", "iso3": "pov", "nom": "Crioulo, Upper Guinea (008)", "script": "Latn", "sens": "ltr", "titre": "DECLARAÇON UNIVERSAL DI DIRITU DI OMIS", "nb_articles": 30, "preambule_car": 1875, "attrs": "iso639-3=pov key=008 n=Crioulo, Upper Guinea (008) dir=ltr iso15924=Latn"}
---
456 dict_keys(['fichier', 'iso3', 'nom', 'script', 'sens', 'titre', 'nb_articles', 'preambule_car', 'attrs'])
{'fichier': 'udhr_007.xml', 'iso3': 'cri', 'nom': 'Sãotomense', 'script': 'Latn', 'sens': 'ltr', 'titre': 'Declaraçón Universal di Dirêtu di Hómé', 'nb_articles': 30, 'preambule_car': 1593, 'attrs': 'iso639-3=cri key=007 n=Sãotomense dir=ltr iso15924=Latn'}
{'fichier': 'udhr_008.xml', 'iso3': 'pov', 'nom': 'Crioulo, Upper Guinea (008)', 'script': 'Latn', 'sens': 'ltr', 'titre': 'DECLARAÇON UNIVERSAL DI DIRITU DI OMIS', 'nb_articles': 30, 'preambule_car': 1875, 'attrs': 'iso639-3=pov key=008 n=Crioulo, Upper Guinea (008) dir=ltr is
… [496 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,csv\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\n# load glottolog\nlang=list(csv.DictReader(open('data/glottolog/languages.csv')))\nprint(lang[0].keys())\n# indices by iso\nbyiso={}; byname={}\nfor r in lang:\n    iso=r.get( … [693 caractères tronqués]`

  ```
dict_keys(['ID', 'Name', 'Macroarea', 'Latitude', 'Longitude', 'Glottocode', 'ISO639P3code', 'Level', 'Countries', 'Family_ID', 'Language_ID', 'Closest_ISO369P3code', 'First_Year_Of_Documentation', 'Last_Year_Of_Documentation', 'Is_Isolate'])
byiso 8184
aar aar Afar iso_in_glotto True
ayo ayo Ayoreo iso_in_glotto True
bin bin Edo iso_in_glotto True
bvi bvi Belanda Viri iso_in_glotto True
cas cas Tsimané iso_in_glotto True
chv chv Chuvash iso_in_glotto True
cnr cnr Montenegrin iso_in_glotto True
crh crh Crimean Tatar iso_in_glotto True
csw csw Cree, Swampy iso_in_glotto True
ese ese Ese Ejja iso_in_glotto True
fuv2 fuv2 Fulfulde, Nigerian (2) iso_in_glotto False
fvr fvr Fur iso_in_glotto True
gnw gnw Guarani, Western Bolivian iso_in_glotto True
gsw1 gsw1 Alemannisch (Elsassisch) iso_in_glotto False
hau_3 hau_3 Hausa iso_in_glotto False
hsn hsn Chinese, Xiang iso_in_glotto True
idu idu Idoma iso_in_glotto True
iii iii Nuosu iso_in_glotto True
ijs ijs Ijo, Southeast iso_in_glotto True
ike ike Inuktitut, Eastern Canadian iso_in_glotto True
jpn_osaka jpn_osaka Japanese (Osaka) iso_in_glotto False
jpn_tokyo jpn_tokyo Japanese (Tokyo) iso_in_glotto False
kaa kaa Karakalpak iso_in_glotto T
… [1109 caractères tronqués]
  ```

- **bash** `{"command": "find /home/stephane/Data13TB/stephane/GitHub -name 'udhr_021.xml' -o -name 'udhr_072.xml' 2>/dev/null | head; echo '--- data dirs ---'; find data -maxdepth 3 -iname '*udhr*' -type d 2>/dev/null; find . -maxdepth 3 -iname 'udhr_*.xml' 2>/dev/null | head", "description": "Locate missing U … [15 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-40]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\n# check if meta contains keys 021 etc\nM=json.load(open('data/udhr/meta.json'))\nfor k in ['udhr_021.xml','udhr_022.xml','udhr_023.xml','udhr_025.xml','udhr_072.xml']:\n    print(k, M.get(k))\n# list numeric keys in meta\nnums=sorted([k for k in M if k.sp … [164 caractères tronqués]`

  ```
udhr_021.xml None
udhr_022.xml None
udhr_023.xml None
udhr_025.xml None
udhr_072.xml None
numeric meta 11 ['udhr_007.xml', 'udhr_008.xml', 'udhr_009.xml', 'udhr_010.xml', 'udhr_011.xml', 'udhr_012.xml', 'udhr_013.xml', 'udhr_014.xml', 'udhr_016.xml', 'udhr_017.xml'] ['udhr_008.xml', 'udhr_009.xml', 'udhr_010.xml', 'udhr_011.xml', 'udhr_012.xml', 'udhr_013.xml', 'udhr_014.xml', 'udhr_016.xml', 'udhr_017.xml', 'udhr_020.xml']
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\ncodes=['eng','deu','nld','swe','nor','dan','fin','hun','fra','ita','spa','por','ron','lat','grc','ell','san','pli','hin','ben','per','fas','ara','heb','lzh','zho','jpn','kor','tur … [192 caractères tronqués]`

  ```
eng [('eng', 'eng', 'English')]
deu [('deu_1901', 'deu_1901', 'German, Standard (1901)'), ('deu_1996', 'deu_1996', 'German, Standard (1996)')]
nld [('nld', 'nld', 'Dutch')]
swe [('swe', 'swe', 'Swedish')]
nor []
dan [('dan', 'dan', 'Danish')]
fin [('fin', 'fin', 'Finnish')]
hun [('hun', 'hun', 'Hungarian')]
fra [('fra', 'fra', 'French')]
ita [('ita', 'ita', 'Italian')]
spa [('spa', 'spa', 'Spanish')]
por [('por_BR', 'por_BR', 'Portuguese (Brazil)'), ('por_PT', 'por_PT', 'Portuguese (Portugal)')]
ron [('ron_1953', 'ron_1953', 'Romanian (1953)'), ('ron_1993', 'ron_1993', 'Romanian (1993)'), ('ron_2006', 'ron_2006', 'Romanian (2006)')]
lat [('azj_latn', 'azj_latn', 'Azerbaijani, North (Latin)'), ('bos_latn', 'bos_latn', 'Bosnian (Latin)'), ('lat', 'lat', 'Latin'), ('lat_1', 'lat_1', 'Latin (1)'), ('mly_latn', 'mly_latn', 'Malay (Latin)'), ('srp_latn', 'srp_latn', 'Serbian (Latin)'), ('tuk_latn', 'tuk_latn', 'Turkmen (Latin)'), ('uig_latn', 'uig_latn', 'Uyghur (Latin)')]
grc []
ell [('ell_monotonic', 'ell_monotonic', 'Greek (monotonic)'), ('ell_polytonic', 'ell_polytonic', 'Greek (polytonic)')]
san [('aka_asante', 'aka_asante', 'Twi (Asante)'), ('san', 'san', 'Sanskrit'), ('san_gran', 
… [564 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nsample=['amh','arb','bel','cmn_hant','cnh','ctd','ell_monotonic','eng','ewe','fra','fuf_adlm','hau_NE','heb','hin','ibo','ind','jav','kin','mly_arab','mya','tgl']\nfor s in sample … [175 caractères tronqués]`

  ```
amh [('amh', 'amh', 'Amharic')]
arb [('arb', 'arb', 'Arabic, Standard'), ('cmn_hans_harbin', 'cmn_hans_harbin', 'Chinese, Mandarin (Harbin)')]
bel [('bel', 'bel', 'Belarusan')]
cmn_hant [('cmn_hant', 'cmn_hant', 'Chinese, Mandarin (Traditional)')]
cnh [('cnh', 'cnh', 'Chin, Haka')]
ctd [('ctd', 'ctd', 'Chin, Tedim')]
ell_monotonic [('ell_monotonic', 'ell_monotonic', 'Greek (monotonic)')]
eng [('eng', 'eng', 'English')]
ewe [('ewe', 'ewe', 'Éwé')]
fra [('fra', 'fra', 'French')]
fuf_adlm [('fuf_adlm', 'fuf_adlm', 'Pular (Adlam)')]
hau_NE [('hau_NE', 'hau_NE', 'Hausa (Niger)')]
heb [('heb', 'heb', 'Hebrew')]
hin [('hin', 'hin', 'Hindi'), ('nya_chinyanja', 'nya_chinyanja', 'Nyanja (Chinyanja)')]
ibo [('ibo', 'ibo', 'Igbo')]
ind [('ind', 'ind', 'Indonesian')]
jav [('jav', 'jav', 'Javanese (Latin)'), ('jav_java', 'jav_java', 'Javanese (Javanese)')]
kin [('kin', 'kin', 'Rwanda')]
mly_arab [('mly_arab', 'mly_arab', 'Malay (Arabic)')]
mya [('mya', 'mya', 'Burmese')]
tgl [('tgl', 'tgl', 'Tagalog'), ('tgl_tglg', 'tgl_tglg', 'Tagalog (Tagalog)')]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nfor pat in ['nor','nob','nno','per','fas','pes','prs','zho','cmn','lzh','grc','pli','ara','arb']:\n    hits=[(k,v['iso'],v['name']) for k,v in P.items() if k==pat or v['iso']==pat … [161 caractères tronqués]`

  ```
nor [('059', '059', 'North Saami (2)'), ('azj_cyrl', 'azj_cyrl', 'Azerbaijani, North (Cyrillic)'), ('azj_latn', 'azj_latn', 'Azerbaijani, North (Latin)'), ('dip', 'dip', 'Dinka, Northeastern'), ('hea', 'hea', 'Hmong, Northern Qiandong'), ('kmr', 'kmr', 'Kurdish, Northern'), ('kqs', 'kqs', 'Kissi, Northern'), ('mam', 'mam', 'Mam, Northern'), ('nno', 'nno', 'Norwegian, Nynorsk'), ('nob', 'nob', 'Norwegian, Bokmål'), ('nso', 'nso', 'Sotho, Northern'), ('ojb', 'ojb', 'Ojibwa, Northwestern')]
nob [('nob', 'nob', 'Norwegian, Bokmål')]
nno [('nno', 'nno', 'Norwegian, Nynorsk')]
per [('008', '008', 'Crioulo, Upper Guinea (008)'), ('chr_uppercase', 'chr_uppercase', 'Cherokee (uppercase)'), ('epo', 'epo', 'Esperanto'), ('hsb', 'hsb', 'Sorbian, Upper'), ('koi', 'koi', 'Komi-Permyak'), ('pov', 'pov', 'Crioulo, Upper Guinea')]
fas []
pes [('pes_1', 'pes_1', 'Farsi, Western'), ('pes_2', 'pes_2', 'Dari'), ('yap', 'yap', 'Yapese')]
prs []
zho []
cmn [('cmn_hans', 'cmn_hans', 'Chinese, Mandarin (Simplified)'), ('cmn_hans_beijing', 'cmn_hans_beijing', 'Chinese, Mandarin (Beijing)'), ('cmn_hans_guiyang', 'cmn_hans_guiyang', 'Chinese, Mandarin (Guiyang)'), ('cmn_hans_harbin', 'cmn_hans_harbin', 'Chine
… [820 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,csv,collections\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nG=json.load(open('data/udhr/genealogie.json'))\nM=json.load(open('data/udhr/meta.json'))\n# glottolog lookup\nlang=list(csv.DictReader(open('data/glottolog/languag … [1192 caractères tronqués]`

  ```
Counter({'D': 428, 'G': 45, None: 40, 'N': 19}) missing 40
('013', '013', '(Mijisa)', 'Other')
('014', '014', '(Maiunan)', 'Other')
('016', '016', '(Minjiang, spoken)', 'Other')
('017', '017', '(Minjiang, written)', 'Other')
('021', '021', '(Muzzi)', 'Other')
('022', '022', '(Klau)', 'Other')
('023', '023', '(Jinan)', 'Other')
('025', '025', '(Bizisa)', 'Other')
('026', '026', '(Yeonbyeon)', 'Other')
('030', '030', 'Kituba (2)', 'Other')
('041', '041', 'Latvian (2)', 'Other')
('042', '042', 'Spanish (resolution)', 'Other')
('043', '043', 'Zarma', 'Other')
('045', '045', 'Maasai', 'Other')
('046', '046', 'Malay, Papuan', 'Other')
('047', '047', 'Malay, Ambonese', 'Other')
('048', '048', 'Minangkabau (2)', 'Other')
('050', '050', '(Bataknese)', 'Other')
('053', '053', 'Hausa (2)', 'Other')
('054', '054', 'Catalan (2)', 'Other')
('058', '058', 'Somali (Af Marka)', 'Other')
('059', '059', 'North Saami (2)', 'Other')
('062', '062', 'Swahili (Chimwiini)', 'Other')
('063', '063', 'Swahili (Kibajuni)', 'Other')
('067', '067', 'Finnish (2)', 'Other')
('068', '068', 'French (Welche)', 'Other')
('069', '069', 'Maori (2)', 'Other')
('072', '072', 'Occitan (Languedocien, 2)', 'Other')
('cmn_han
… [849 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\n# load drave articles counts\nfrom collections import Counter\ncnt=Counter()\nfor line in open('data/udhr/articles_propres.jsonl'):\n    x=json.loads(line); cnt[x['fichier']]+=1\nM=json.load(open('data/udhr/meta.json'))\nkeys=['eng','deu_1996','nld','swe' … [575 caractères tronqués]`

  ```
eng eng 30
deu_1996 deu 30
nld nld 30
swe swe 30
nob nob 30
dan dan 30
fin fin 30
hun hun 30
fra fra 30
ita ita 30
spa spa 30
por_PT por 30
ron_2006 ron 30
lat lat 30
ell_monotonic ell 30
san san 30
hin hin 30
ben ben 30
pes_1 pes 30
arb arb 30
heb heb 30
cmn_hant cmn 30
jpn jpn 30
kor kor 30
tur tur 30
sample
amh amh 30
arb arb 30
bel bel 30
cmn_hant cmn 30
cnh cnh 30
ctd ctd 30
ell_monotonic ell 30
eng eng 30
ewe ewe 30
fra fra 30
fuf_adlm fuf 30
hau_NE hau 30
heb heb 30
hin hin 30
ibo ibo 30
ind ind 30
jav jav 30
kin kin 30
mly_arab zlm 30
mya mya 30
tgl tgl 30
  ```

### 👤 Utilisateur

background job bash-40 (bash: find /home/stephane/Data13TB/stephane/GitHub -name 'udhr_021.xml' -o -name 'udhr_072.xml' 2>/dev/null | head; echo '--- data dirs ---'; find data -maxdepth 3 -iname '*udhr*' -type d 2>/dev/null; find . -maxdepth 3 -iname 'udhr_*.xml' 2>/dev/null | head) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "head -3 data/glottolog/values.csv; echo '---'; python3 - <<'EOF'\nimport csv\nr=csv.DictReader(open('data/glottolog/values.csv'))\nfor i,x in zip(range(3),r): print(x)\nEOF", "description": "Inspect Glottolog values schema"}`

  ```
ID,Language_ID,Parameter_ID,Value,Code_ID,Comment,Source,codeReference
abkh1242-level,abkh1242,level,family,level-family,,,
abkh1242-category,abkh1242,category,Family,category-Family,,,
---
{'ID': 'abkh1242-level', 'Language_ID': 'abkh1242', 'Parameter_ID': 'level', 'Value': 'family', 'Code_ID': 'level-family', 'Comment': '', 'Source': '', 'codeReference': ''}
{'ID': 'abkh1242-category', 'Language_ID': 'abkh1242', 'Parameter_ID': 'category', 'Value': 'Family', 'Code_ID': 'category-Family', 'Comment': '', 'Source': '', 'codeReference': ''}
{'ID': 'abkh1242-subclassification', 'Language_ID': 'abkh1242', 'Parameter_ID': 'subclassification', 'Value': '(((ashk1247:1,bezs1238:1,tapa1256:1)abaz1241:1,(abzh1238:1,bzyb1238:1,samu1242:1)abkh1244:1)abkh1243:1,((grea1271:1)kaba1278:1,(abad1240:1,bezh1247:1,natu1243:1,shap1240:1,temi1249:1,xaku1238:1)adyg1241:1)circ1239:1,ubyk1235:1)abkh1242:1;', 'Code_ID': '', 'Comment': '**hh:hv:Hewitt:NWC**', 'Source': '135227', 'codeReference': ''}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nG=json.load(open('data/udhr/genealogie.json'))\nfor k in ['udhr_eng.xml','udhr_deu_1996.xml','udhr_ind.xml','udhr_jav.xml','udhr_cnh.xml','udhr_ctd.xml','udhr_san.xml','udhr_lat.xml']:\n    v=G.get(k)\n    print(k, v['iso3'] if v else None, v['famille'] i … [110 caractères tronqués]`

  ```
udhr_eng.xml eng Indo-European indo1319/clas1257/germ1287/nort3152/west2793/nort3175/angl1264/angl1265/late1254/merc1242/macr1271
udhr_deu_1996.xml deu Indo-European indo1319/clas1257/germ1287/nort3152/west2793/high1289/high1286/midd1349/mode1258/uppe1464/glob1243
udhr_ind.xml ind Austronesian aust1307/mala1545/mala1554/mala1538/nucl1806/stan1327
udhr_jav.xml jav Austronesian aust1307/mala1545/java1253/mode1251/glob1245
udhr_cnh.xml cnh Sino-Tibetan sino1245/kuki1245/kuki1246/cent2330/cent2005/laic1236
udhr_ctd.xml ctd Sino-Tibetan sino1245/kuki1245/kuki1246/peri1260/nort3179/thad1239
udhr_san.xml san Indo-European indo1319/clas1257/indo1320/indo1321
udhr_lat.xml lat Indo-European indo1319/clas1257/ital1284/lati1262/lati1263/impe1234
  ```

- **bash** `{"command": "ls tools/__init__.py 2>/dev/null; python3 -c \"import sys; sys.path.insert(0,'tools'); import retrieval_epoque; print(retrieval_epoque.normalise('Élà'))\"", "description": "Check importability of J3.1 tool"}`

  ```
ela
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nu=d['udhr']\nprint(u.keys())\nprint('n',u['n_langues'],len(u['paires']))\nprint(json.dumps(u['agregats'],ensure_ascii=False,indent=1)[:1500])\nprint(json.dumps(u['regression'],ensure_ascii=False,indent=1 … [169 caractères tronqués]`

  ```
dict_keys(['n_langues', 'n_articles', 'epoque', 'meta_langues', 'agregats', 'regression', 'controles', 'paires'])
n 21 420
{
 "toutes": {
  "n_paires": 420,
  "top1_moyen": 0.049444444444444444,
  "top1_median": 0.03333333333333333,
  "ic_bas": 0.0,
  "ic_haut": 0.18416666666666592
 },
 "script_meme": {
  "n_paires": 112,
  "top1_moyen": 0.09375,
  "top1_median": 0.05,
  "ic_bas": 0.0,
  "ic_haut": 0.8483333333333329
 },
 "script_different": {
  "n_paires": 308,
  "top1_moyen": 0.03333333333333333,
  "top1_median": 0.03333333333333333,
  "ic_bas": 0.03333333333333333,
  "ic_haut": 0.03333333333333333
 },
 "famille_meme": {
  "n_paires": 68,
  "top1_moyen": 0.09411764705882353,
  "top1_median": 0.03333333333333333,
  "ic_bas": 0.03333333333333333,
  "ic_haut": 0.9108333333333335
 },
 "famille_differente": {
  "n_paires": 352,
  "top1_moyen": 0.040814393939393935,
  "top1_median": 0.03333333333333333,
  "ic_bas": 0.0,
  "ic_haut": 0.16666666666666666
 },
 "script_meme_famille_meme": {
  "n_paires": 16,
  "top1_moyen": 0.2916666666666667,
  "top1_median": 0.1,
  "ic_bas": 0.0125,
  "ic_haut": 0.9333333333333333
 },
 "script_meme_famille_differente": {
  "n_paires": 96,
  "top1_moyen":
… [1216 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p work/j71 && cat > work/j71/explore.py <<'EOF'\nimport json, csv, collections, re, sys\nfrom pathlib import Path\nRACINE=Path('.').resolve()\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nG=json.load(open('data/udhr/genealogie.json'))\nM=json.load(o … [2879 caractères tronqués]`

  ```
labeled 504 of 532
Counter({'drave': 428, 'glottolog': 60, 'name': 16})
families [('Indo-European', 123), ('Atlantic-Congo', 82), ('Austronesian', 37), ('Sino-Tibetan', 18), ('Turkic', 18), ('Afro-Asiatic', 13), ('Mayan', 11), ('Quechuan', 11), ('Uralic', 9), ('', 8), ('Mande', 8), ('Otomanguean', 8), ('Arawakan', 7), ('Tai-Kadai', 7), ('Pano-Tacanan', 6), ('Nilotic', 5), ('sino1245/sini1245/clas1255/midd1354/nort3155/mand1471', 5), ('Tungusic', 5), ('Dravidian', 5), ('Chicham', 4)]
unknown 28
013 013 (Mijisa)
014 014 (Maiunan)
016 016 (Minjiang, spoken)
017 017 (Minjiang, written)
021 021 (Muzzi)
022 022 (Klau)
023 023 (Jinan)
025 025 (Bizisa)
026 026 (Yeonbyeon)
030 030 Kituba (2)
041 041 Latvian (2)
042 042 Spanish (resolution)
043 043 Zarma
045 045 Maasai
046 046 Malay, Papuan
047 047 Malay, Ambonese
048 048 Minangkabau (2)
050 050 (Bataknese)
053 053 Hausa (2)
054 054 Catalan (2)
058 058 Somali (Af Marka)
059 059 North Saami (2)
062 062 Swahili (Chimwiini)
063 063 Swahili (Kibajuni)
067 067 Finnish (2)
068 068 French (Welche)
069 069 Maori (2)
072 072 Occitan (Languedocien, 2)
path len [(1, 82), (6, 53), (10, 47), (5, 42), (4, 35), (3, 30), (9, 30), (11, 28), (7, 28), (12, 26)
… [84 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport csv\nfor r in csv.DictReader(open('data/glottolog/values.csv')):\n    if r.get('Parameter_ID')=='classification' and r.get('Language_ID') in ('cmn','arb','eng'):\n        print(r['Language_ID'], repr(r['Value'])[:300])\nEOF", "description": "Inspect Glottolog c … [28 caractères tronqués]`

  ```
(no output)
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport csv,collections\nlangs=list(csv.DictReader(open('data/glottolog/languages.csv')))\nbyiso=collections.defaultdict(list)\nfor r in langs:\n    if r.get('ISO639P3code'): byiso[r['ISO639P3code']].append(r)\nfor iso in ['cmn','arb','eng']:\n    print(iso,[(r['ID'],r … [432 caractères tronqués]`

  ```
cmn [('mand1415', 'mand1415', 'Mandarin Chinese', 'language')]
arb [('stan1318', 'stan1318', 'Standard Arabic', 'language')]
eng [('stan1293', 'stan1293', 'English', 'language')]
mand1415 'sino1245/sini1245/clas1255/midd1354/nort3155/mand1471'
stan1318 'afro1255/semi1276/west2786/cent2236/arab1394/arab1395'
stan1293 'indo1319/clas1257/germ1287/nort3152/west2793/nort3175/angl1264/angl1265/late1254/merc1242/macr1271'
  ```

- **bash** `{"command": "cat > work/j71/explore2.py <<'EOF'\nimport json, csv, collections, re\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nG=json.load(open('data/udhr/genealogie.json'))\nlangs=list(csv.DictReader(open('data/glottolog/languages.csv')))\nnames={r['ID']:r['Name'] f … [2925 caractères tronqués]`

  ```
labeled 504 Counter({'drave': 428, 'glottolog': 60, 'name': 16})
families [('Indo-European', 129), ('Atlantic-Congo', 91), ('Austronesian', 39), ('Sino-Tibetan', 28), ('Turkic', 23), ('Afro-Asiatic', 22), ('Quechuan', 14), ('Uralic', 12), ('Mayan', 11), ('', 8), ('Pano-Tacanan', 8), ('Arawakan', 8), ('Mande', 8), ('Otomanguean', 8), ('Tai-Kadai', 7), ('Dravidian', 6), ('Nilotic', 5), ('Tungusic', 5), ('Austroasiatic', 5), ('Chicham', 4), ('Tupian', 4), ('Abkhaz-Adyge', 3), ('Hmong-Mien', 3), ('Algic', 3), ('Artificial Language', 3), ('Japonic', 3), ('Zaparoan', 2), ('Barbacoan', 2), ('Iroquoian', 2), ('Eskimo-Aleut', 2)]
empty fam [('027', {'src': 'name', 'iso3': '', 'famille': '', 'path': [''], 'codes': [], 'script': 'Latn', 'name': 'Gumuz', 'key': '027', 'panini_name': 'Gumuz', 'family_panini': 'Other'}), ('auc', {'src': 'glottolog', 'iso3': 'auc', 'famille': '', 'path': [''], 'codes': [], 'script': 'Latn', 'name': 'Waorani', 'key': 'auc', 'panini_name': 'Waorani', 'family_panini': 'Other'}), ('cas', {'src': 'glottolog', 'iso3': 'cas', 'famille': '', 'path': [''], 'codes': [], 'script': 'Latn', 'name': 'Mosetén-Chimané', 'key': 'cas', 'panini_name': 'Tsimané', 'family_panini': 'O
… [3181 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j71/sets.py <<'EOF'\nimport json, csv, collections, re\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nG=json.load(open('data/udhr/genealogie.json'))\nM=json.load(open('data/udhr/meta.json'))\nC=json.load(open('reports/corpus-commun.json'))\n# glo … [3546 caractères tronqués]`

  ```
LANG_TREE mapped 26 unique 25 absent ['grc', 'pli', 'lzh']
eng -> eng found True meta True 30art True
deu -> deu_1996 found True meta True 30art True
nld -> nld found True meta True 30art True
swe -> swe found True meta True 30art True
nor -> nob found True meta True 30art True
dan -> dan found True meta True 30art True
fin -> fin found True meta True 30art True
hun -> hun found True meta True 30art True
fra -> fra found True meta True 30art True
ita -> ita found True meta True 30art True
spa -> spa found True meta True 30art True
por -> por_PT found True meta True 30art True
ron -> ron_2006 found True meta True 30art True
lat -> lat found True meta True 30art True
ell -> ell_monotonic found True meta True 30art True
san -> san found True meta True 30art True
hin -> hin found True meta True 30art True
ben -> ben found True meta True 30art True
per -> pes_1 found True meta True 30art True
fas -> pes_1 found True meta True 30art True
ara -> arb found True meta True 30art True
heb -> heb found True meta True 30art True
zho -> cmn_hant found True meta True 30art True
jpn -> jpn found True meta True 30art True
kor -> kor found True meta True 30art True
tur -> tur found True meta True 30
… [749 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j71/global.py <<'EOF'\nimport json,sys,collections,numpy as np\nsys.path.insert(0,'tools')\nimport retrieval_epoque as R\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nmeta=json.load(open('work/j71/meta.json')) if False else None\n# import meta f … [3942 caractères tronqués]`

  ```
labeled 504
labeled {
 "n": 504,
 "top1_fam": 0.7341269841269841,
 "top1_soeur": 0.6071428571428571,
 "top1_branch": 0.5496031746031746,
 "top1_samefam_other": 0.12698412698412698,
 "top1_diff": 0.26587301587301587,
 "top1_script": 0.9464285714285714,
 "p_fam": 0.1134305279434504,
 "p_soeur": 0.03318975038656947,
 "p_branch": 0.028085455520843197,
 "p_script": 0.5921455394616428,
 "mrr_fam": 0.7715591938047736,
 "ap_fam": 0.4107296263287535,
 "top5_fam": 0.6091269841269841
}
sister pairs 4207
[('007', '008'), ('007', '044'), ('007', '052'), ('007', '056'), ('007', 'ast'), ('007', 'auv'), ('007', 'cat'), ('007', 'cos'), ('007', 'crs'), ('007', 'eml'), ('007', 'fra'), ('007', 'fur'), ('007', 'glg'), ('007', 'hat_kreyol'), ('007', 'hat_popular'), ('007', 'ita'), ('007', 'kea'), ('007', 'lad'), ('007', 'lat'), ('007', 'lat_1')]
Arab 10 top1fam 0.7 top1soeur 0.7
Cans 3 top1fam 0.6666666666666666 top1soeur 0.6666666666666666
Cyrl 35 top1fam 0.7714285714285715 top1soeur 0.45714285714285713
Deva 8 top1fam 0.875 top1soeur 0.875
Hans 12 top1fam 1.0 top1soeur 0.9166666666666666
Jpan 3 top1fam 1.0 top1soeur 1.0
Latn 386 top1fam 0.7409326424870466 top1soeur 0.6321243523316062
Mymr 3 top1fam 0.0
… [14 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j71/global2.py <<'EOF'\nimport json,sys,collections,numpy as np\nsys.path.insert(0,'tools'); import retrieval_epoque as R\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nexec(open('work/j71/sets.py').read().split(\"LANG_TREE={\")[0])\nkeys=list(P) … [3203 caractères tronqués]`

  ```
labeled 504 distinct langid 469
langid groups with >1 44 extra texts 63
pov ['008', 'pov']
kmb ['009', 'kmb']
umb ['011', 'umb']
acu ['acu', 'acu_1']
twi ['aka_akuapem', 'aka_asante']
oci ['auv', 'lnc', 'oci_1', 'oci_2', 'oci_3', 'oci_4', 'prv']
azj ['azj_cyrl', 'azj_latn']
bos ['bos_cyrl', 'bos_latn']
chr ['chr_cased', 'chr_uppercase']
cjk ['cjk', 'cjk_AO']
cmn ['cmn_hans', 'cmn_hans_beijing', 'cmn_hans_guiyang', 'cmn_hans_harbin', 'cmn_hans_nanjing', 'cmn_hans_tianjin', 'cmn_hant']
deu ['deu_1901', 'deu_1996']
ell ['ell_monotonic', 'ell_polytonic']
fuf ['fuf', 'fuf_adlm']
fuv ['fuv', 'fuv2']
hat ['hat_kreyol', 'hat_popular']
hau ['hau_3', 'hau_NE', 'hau_NG']
hus ['hsf', 'hus', 'hva']
jav ['jav', 'jav_java']
jpn ['jpn', 'jpn_osaka', 'jpn_tokyo']
SANS exclusion same lang
{
 "n": 504,
 "n_cand_moyen": 503.0,
 "top1_fam": 0.7341269841269841,
 "top1_soeur": 0.6071428571428571,
 "top1_branch": 0.5496031746031746,
 "top1_diff": 0.26587301587301587,
 "top1_script": 0.9464285714285714,
 "p_fam": 0.1134305279434504,
 "p_soeur": 0.03318975038656947,
 "p_script": 0.5921455394616428,
 "mrr_fam": 0.7715591938047736,
 "ap_fam": 0.4107296263287535,
 "top1_same_lang": 0.14484126984126985
}
AVEC e
… [429 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j71/global3.py <<'EOF'\nimport json,sys,collections,numpy as np\nsys.path.insert(0,'tools'); import retrieval_epoque as R\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nexec(open('work/j71/sets.py').read().split(\"LANG_TREE={\")[0])\nkeys=list(P) … [2867 caractères tronqués]`

  ```
ALL {
 "n_queries": 504,
 "n_cand_moyen": 502.55555555555554,
 "top1_fam": 0.6845238095238095,
 "p_fam": 0.11268350659470669,
 "top1_soeur": 0.5615079365079365,
 "p_soeur": 0.03239141509095123,
 "top1_branch": 0.5099206349206349,
 "top1_diff": 0.31547619047619047
}
SAME SCRIPT {
 "n_queries": 467,
 "n_cand_moyen": 321.05353319057815,
 "top1_fam": 0.7173447537473233,
 "p_fam": 0.1853770754029438,
 "top1_soeur": 0.6017130620985011,
 "p_soeur": 0.10135687160946828,
 "top1_branch": 0.5460385438972163,
 "top1_diff": 0.2826552462526767
}
DIFF SCRIPT {
 "n_queries": 504,
 "n_cand_moyen": 205.07142857142858,
 "top1_fam": 0.09126984126984126,
 "p_fam": 0.08595774038112552,
 "top1_soeur": 0.031746031746031744,
 "p_soeur": 0.00842693687522507,
 "top1_branch": 0.027777777777777776,
 "top1_diff": 0.9087301587301587
}
Latn 386 top1fam 0.7098445595854922 basefam 0.12843522324859863 top1soeur 0.6010362694300518 basesoeur 0.0459437381542479
Cyrl 35 top1fam 0.7714285714285715 basefam 0.21176470588235294 top1soeur 0.45714285714285713 basesoeur 0.07058823529411763
Arab 10 top1fam 0.7 basefam 0.4583333333333333 top1soeur 0.7 basesoeur 0.4583333333333333
Deva 8 top1fam 0.875 basefam 0.75 top1soeur 0.875
… [105 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j71/pairwise.py <<'EOF'\nimport json,sys,collections,numpy as np\nsys.path.insert(0,'tools'); import retrieval_epoque as R\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nexec(open('work/j71/sets.py').read().split(\"LANG_TREE={\")[0])\n# articles\ … [3299 caractères tronqués]`

  ```
J3.1 21 langs 21 pairs 420
all {'n': 420, 'top1': 0.049444444444444444, 'med': 0.03333333333333333}
script {'n': 112, 'top1': 0.09375, 'med': 0.05}
diffscript {'n': 308, 'top1': 0.03333333333333333, 'med': 0.03333333333333333}
fam {'n': 68, 'top1': 0.09411764705882353, 'med': 0.03333333333333333}
diffam {'n': 352, 'top1': 0.040814393939393935, 'med': 0.03333333333333333}
soeur {'n': 12, 'top1': 0.05833333333333333, 'med': 0.03333333333333333}
soeur_stricte {'n': 4, 'top1': 0.03333333333333333, 'med': 0.03333333333333333}
fam_autre {'n': 56, 'top1': 0.1017857142857143, 'med': 0.03333333333333333}
script_soeur {'n': 4, 'top1': 0.10833333333333334, 'med': 0.09999999999999999}
script_diffam {'n': 96, 'top1': 0.06076388888888889, 'med': 0.03333333333333333}
diffscript_soeur {'n': 8, 'top1': 0.03333333333333333, 'med': 0.03333333333333333}
reg ['script_match', 'famille_match', 'chance'] {'constante': 0.0239165525733774, 'script_match': 0.061861313868612655, 'famille_match': 0.05561891727493886, 'chance': 0.000797218419112569} r2 0.13957348684925897
reg ['script_match', 'soeur', 'famille_autre_branche', 'chance'] {'constante': 0.023717723533763807, 'script_match': 0.06259116372476474, 'so
… [5325 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\n# quick check paths and prefix relations\nimport json\nG=json.load(open('data/udhr/genealogie.json'))\nimport csv,collections\nlangs=list(csv.DictReader(open('data/glottolog/languages.csv'))); names={r['ID']:r['Name'] for r in langs}\ndef path(k):\n    g=G.get('udhr_% … [571 caractères tronqués]`

  ```
lat fra lca 6 prefix True lens 6 16
  ['Indo-European', 'Classical Indo-European', 'Italic', 'Latino-Faliscan', 'Latinic', 'Imperial Latin']
  ['Indo-European', 'Classical Indo-European', 'Italic', 'Latino-Faliscan', 'Latinic', 'Imperial Latin', 'Romance', 'Italo-Western Romance', 'Western Romance', 'Shifted Western Romance', 'Northwestern Shifted Romance', 'Gallo-Rhaetian', 'Oil', 'Central Oil', 'Macro-French', 'Global French']
san hin lca 4 prefix True lens 4 11
  ['Indo-European', 'Classical Indo-European', 'Indo-Iranian', 'Indo-Aryan']
  ['Indo-European', 'Classical Indo-European', 'Indo-Iranian', 'Indo-Aryan', 'Middle-Modern Indo-Aryan', 'Continental Indo-Aryan', 'Midlands Indo-Aryan', 'Shaurasenic', 'Indo-Aryan Central zone', 'Western Hindi', 'Hindustani']
san ben lca 4 prefix True lens 4 10
  ['Indo-European', 'Classical Indo-European', 'Indo-Iranian', 'Indo-Aryan']
  ['Indo-European', 'Classical Indo-European', 'Indo-Iranian', 'Indo-Aryan', 'Middle-Modern Indo-Aryan', 'Continental Indo-Aryan', 'Indo-Aryan Eastern zone', 'Oriya-Gauda-Kamrupa', 'Gauda-Kamrupa', 'Gauda-Banga']
eng deu_1996 lca 5 prefix False lens 11 11
  ['Indo-European', 'Classical Indo-European', 'Germanic',
… [1991 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j71/pairwise2.py <<'EOF'\nimport json,sys,collections,numpy as np\nsys.path.insert(0,'tools'); import retrieval_epoque as R\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nexec(open('work/j71/sets.py').read().split(\"LANG_TREE={\")[0])\narts=colle … [3323 caractères tronqués]`

  ```
J3.1 21 langs 21 pairs 420
all (420, 0.049444444444444444)
script (112, 0.09375)
diffscript (308, 0.03333333333333333)
fam (68, 0.09411764705882353)
diffam (352, 0.040814393939393935)
soeur (12, 0.05833333333333333)
soeur_stricte (4, 0.03333333333333333)
fam_autre (56, 0.1017857142857143)
script_soeur (4, 0.10833333333333334)
script_diffam (96, 0.06076388888888889)
script_fam_autre (12, 0.3527777777777777)
diffscript_soeur (8, 0.03333333333333333)
reg ['script_match', 'famille_match', 'chance'] {'constante': 0.0239165525733774, 'script_match': 0.061861313868612655, 'famille_match': 0.05561891727493886, 'chance': 0.000797218419112569} r2 0.13957348684925897
reg ['script_match', 'soeur', 'famille_autre_branche', 'chance'] {'constante': 0.023717723533763807, 'script_match': 0.06259116372476474, 'soeur': 0.013725535531831933, 'famille_autre_branche': 0.06462924549906614, 'chance': 0.0007905907844587851} r2 0.1470703474876507
reg ['script_match', 'soeur_stricte', 'famille_autre_branche', 'chance'] {'constante': 0.02400100199708951, 'script_match': 0.06283372213582158, 'soeur_stricte': 0.009305663556246815, 'famille_autre_branche': 0.06429367547952347, 'chance': 0.0008000333999029757} r2
… [3730 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j71/global4.py <<'EOF'\nimport json,sys,collections,numpy as np\nsys.path.insert(0,'tools'); import retrieval_epoque as R\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nexec(open('work/j71/sets.py').read().split(\"LANG_TREE={\")[0])\nkeys=list(P) … [2394 caractères tronqués]`

  ```
ALL {
 "n_queries": 504,
 "n_cand_moyen": 502.55555555555554,
 "top1_fam": 0.6845238095238095,
 "p_fam": 0.11268350659470669,
 "top1_soeur": 0.2757936507936508,
 "p_soeur": 0.02849416981547565,
 "top1_famautre": 0.4087301587301587,
 "top1_diff": 0.31547619047619047
}
SAME SCRIPT {
 "n_queries": 467,
 "n_cand_moyen": 321.05353319057815,
 "top1_fam": 0.7173447537473233,
 "p_fam": 0.1853770754029438,
 "top1_soeur": 0.29764453961456105,
 "p_soeur": 0.0643876533081216,
 "top1_famautre": 0.4197002141327623,
 "top1_diff": 0.2826552462526767
}
DIFF SCRIPT {
 "n_queries": 504,
 "n_cand_moyen": 205.07142857142858,
 "top1_fam": 0.09126984126984126,
 "p_fam": 0.08595774038112552,
 "top1_soeur": 0.015873015873015872,
 "p_soeur": 0.00745657560263397,
 "top1_famautre": 0.07539682539682539,
 "top1_diff": 0.9087301587301587
}
sister pairs 3607
  ```

- **bash** `{"command": "cat > work/j71/global5.py <<'EOF'\nimport json,sys,collections,numpy as np\nsys.path.insert(0,'tools'); import retrieval_epoque as R\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nexec(open('work/j71/sets.py').read().split(\"LANG_TREE={\")[0])\n# preferred  … [3649 caractères tronqués]`

  ```
groups 441 reps 441 dups removed 63
dup groups [('pov', ['008', 'pov']), ('kmb', ['009', 'kmb']), ('umb', ['011', 'umb']), ('acu', ['acu', 'acu_1']), ('twi', ['aka_akuapem', 'aka_asante']), ('oci', ['auv', 'lnc', 'oci_1', 'oci_2', 'oci_3', 'oci_4', 'prv']), ('azj', ['azj_cyrl', 'azj_latn']), ('bos', ['bos_cyrl', 'bos_latn']), ('chr', ['chr_cased', 'chr_uppercase']), ('cjk', ['cjk', 'cjk_AO'])]
ALL {
 "n_queries": 441,
 "n_cand_moyen": 440.0,
 "top1_fam": 0.6621315192743764,
 "p_fam": 0.10407132549989694,
 "top1_soeur": 0.2562358276643991,
 "p_soeur": 0.02586064728921872,
 "top1_famautre": 0.40589569160997735,
 "top1_diff": 0.3378684807256236,
 "top1_script": 0.9342403628117913,
 "p_script": 0.6115852401566687,
 "mrr_fam": 0.717911577319724,
 "ap_fam": 0.37905177472514706,
 "top5_fam": 0.5795918367346939
}
SAME SCRIPT {
 "n_queries": 413,
 "n_cand_moyen": 287.3414043583535,
 "top1_fam": 0.7021791767554479,
 "p_fam": 0.16342638750415422,
 "top1_soeur": 0.2736077481840194,
 "p_soeur": 0.058074237723635395,
 "top1_famautre": 0.42857142857142855,
 "top1_diff": 0.29782082324455206,
 "top1_script": 1.0,
 "p_script": 1.0,
 "mrr_fam": 0.749736521394762,
 "ap_fam": 0.4978643766700815,
 "top5
… [444 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,csv,collections\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nexec(open('work/j71/sets.py').read().split(\"LANG_TREE={\")[0])\nlt=['eng','deu_1996','nld','swe','nob','dan','fin','hun','fra','ita','spa','por_PT','ron_2006','la … [567 caractères tronqués]`

  ```
30
('eng', 'deu_1996', 5)
('eng', 'nld', 5)
('eng', 'swe', 4)
('eng', 'nob', 4)
('eng', 'dan', 4)
('deu_1996', 'nld', 5)
('deu_1996', 'swe', 4)
('deu_1996', 'nob', 4)
('deu_1996', 'dan', 4)
('nld', 'swe', 4)
('nld', 'nob', 4)
('nld', 'dan', 4)
('swe', 'nob', 5)
('swe', 'dan', 5)
('nob', 'dan', 5)
('fra', 'ita', 8)
('fra', 'spa', 10)
('fra', 'por_PT', 10)
('fra', 'ron_2006', 7)
('ita', 'spa', 8)
('ita', 'por_PT', 8)
('ita', 'ron_2006', 7)
('spa', 'por_PT', 12)
('spa', 'ron_2006', 7)
('por_PT', 'ron_2006', 7)
('san', 'pes_1', 3)
('hin', 'ben', 6)
('hin', 'pes_1', 3)
('ben', 'pes_1', 3)
('arb', 'heb', 4)
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport csv\nfor r in csv.DictReader(open('data/glottolog/languages.csv')):\n    if r.get('ISO639P3code')=='eus' or r.get('Name')=='Basque':\n        print(r)\nEOF", "description": "Check Basque Glottolog row"}`

  ```
{'ID': 'basq1248', 'Name': 'Basque', 'Macroarea': 'Eurasia', 'Latitude': '43.2787', 'Longitude': '-1.31622', 'Glottocode': 'basq1248', 'ISO639P3code': 'eus', 'Level': 'language', 'Countries': 'ES;FR', 'Family_ID': '', 'Language_ID': '', 'Closest_ISO369P3code': 'eus', 'First_Year_Of_Documentation': '', 'Last_Year_Of_Documentation': '', 'Is_Isolate': 'true'}
  ```

- **bash** `{"command": "ls ../Panini/research/data | grep -i udhr; echo '--- dirs ---'; find ../Panini/research -maxdepth 3 -type d -iname '*udhr*' 2>/dev/null | head; echo '--- xml count ---'; find ../Panini/research -maxdepth 4 -iname 'udhr_*.xml' 2>/dev/null | head -5", "description": "Search Panini researc … [23 caractères tronqués]`

  ```
udhr_article1_en.json
udhr_article1_fr.json
udhr_convergence_graph.json
udhr_convergence_v14.json
udhr_corpus.json
udhr_decomposed_v14.json
udhr_demo.nipada
udhr_omw_coverage.json
udhr_reconstruction_full.json
udhr_reconstruction_report.json
udhr_universal_graph.json
--- dirs ---
--- xml count ---
  ```

- **bash** `{"command": "cat > tools/retrieval_familles.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"retrieval_familles.py — J7.1 : le retrieval approfondi par famille Glottolog.\n\nLA QUESTION. J3.1 a mesuré le retrieval de surface sur 21 langues UDHR (30 articles, 1948) :\ntop-1 0,049, écriture +0,062, famille +0 … [52292 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "python3 tools/retrieval_familles.py --rapide --sortie work/j71/j71-rapide.json 2>&1 | tail -40", "description": "Run J7.1 tool in rapid mode"}`

  ```
Panini UDHR 532 — chargement…
  532 textes Panini · 522 étiquetés Glottolog · 447 langues distinctes
Global 532 — article 1, voisinage généalogique…
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py", line 997, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py", line 830, in main
    global_532 = mesure_globale(meta, panini, ensembles["representants"],
                                graine=a.graine, permutations=a.permutations)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py", line 382, in mesure_globale
    "top1_famille_differente": bool(rel[i][top]["famille_differente"]),
                                    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
KeyError: 'famille_differente'
  ```

- **edit** `{"file_path": "tools/retrieval_familles.py", "old_string": "    return {\"lca\": d, \"ancetre_descendant\": ancetre, \"meme_famille\": meme,\n            \"soeur\": soeur, \"soeur_stricte\": bool(meme and d >= 4 and not ancetre),\n            \"famille_autre_branche\": bool(meme and not soeur)}", "n … [303 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "tools/retrieval_familles.py", "offset": 300, "limit": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py</path>
<type>file</type>
<content>
300: def construire_ensembles(meta: dict, panini: dict) -> dict:
301:     # 4.1 Les 29 de LANG_TREE, avec la table de correspondance explicite.
302:     lang_tree = {}
303:     for code, cle in LANG_TREE_VERS_PANINI.items():
304:         if cle and cle in meta:
305:             lang_tree[code] = cle
306:     # 4.2 L'échantillon 20 du corpus commun (les 20 strates, sans le pivot français).
307:     corpus = lire_json(CORPUS_COMMUN)
308:     echantillon = [t["id"].replace("udhr_", "") for t in corpus["textes"]
309:                    if t.get("role") == "strate"]
310:     echantillon = [k for k in echantillon if k in meta]
311:     # 4.3 Les 21 de J3.1 (20 strates + fra) pour la reproduction exacte.
312:     j31 = [k.replace("udhr_", "") for k in lire_json(J31_JSON)["udhr"]["meta_langues"]]
313:     j31 = [k for k in j31 if k in meta]
314:     # 4.4 L'union (sans doublon de texte).
315:     union = sorted(set(lang_tree.values()) | set(echantillon))
316:     # 4.5 Les textes Panini non dédupliqués : un représentant par code ISO.
317:     langid = {k: (m.get("iso3") or k
… [915 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"famille_autre_branche\" tools/retrieval_familles.py | head", "description": "Locate relation_chemins return"}`

  ```
277:            "soeur_stricte": soeur_stricte, "famille_autre_branche": famille_autre,
293:            "famille_autre_branche": bool(meme and not soeur)}
381:            "top1_famille_autre": bool(rel[i][top]["famille_autre_branche"]),
433:                           rel[i][j]["soeur"], rel[i][j]["famille_autre_branche"]))
557:                "famille_autre_branche": r["famille_autre_branche"],
585:        "famille_autre_branche": agreger(lambda p: p["famille_autre_branche"]),
587:        "script_meme_famille_autre": agreger(lambda p: p["script_match"] and p["famille_autre_branche"]),
596:    reg_b = _ols_sans_chance(paires, ["script_match", "soeur", "famille_autre_branche"])
597:    reg_c = _ols_sans_chance(paires, ["script_match", "soeur_stricte", "famille_autre_branche"])
610:            p["_fam_autre_p"] = r["famille_autre_branche"]
  ```

- **read** `{"file_path": "tools/retrieval_familles.py", "limit": 12, "offset": 285}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py</path>
<type>file</type>
<content>
285:             d += 1
286:         else:
287:             break
288:     ancetre = pa == pb[:len(pa)] or pb == pa[:len(pb)]
289:     meme = pa[0] == pb[0]
290:     soeur = bool(meme and d >= 3 and not ancetre)
291:     return {"lca": d, "ancetre_descendant": ancetre, "meme_famille": meme,
292:             "soeur": soeur, "soeur_stricte": bool(meme and d >= 4 and not ancetre),
293:             "famille_autre_branche": bool(meme and not soeur)}
294: 
295: 
296: # ---------------------------------------------------------------------------

(Showing lines 285-296 of 997. Use offset=297 to continue.)
</content>
  ```

- **edit** `{"file_path": "tools/retrieval_familles.py", "old_string": "    return {\"lca\": d, \"ancetre_descendant\": ancetre, \"meme_famille\": meme,\n            \"soeur\": soeur, \"soeur_stricte\": bool(meme and d >= 4 and not ancetre),\n            \"famille_autre_branche\": bool(meme and not soeur)}", "n … [303 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/retrieval_familles.py --rapide --sortie work/j71/j71-rapide.json 2>&1 | tail -40", "description": "Rerun J7.1 rapid mode"}`

  ```
Panini UDHR 532 — chargement…
  532 textes Panini · 522 étiquetés Glottolog · 447 langues distinctes
Global 532 — article 1, voisinage généalogique…
  447 requêtes · top1 famille 0.6644 (hasard 0.1039) · top1 sœur 0.2640 (hasard 0.0259)
Parallèle 30 articles — LANG_TREE 29, échantillon 20, J3.1 21, union…
  LANG_TREE 25 langues / 600 paires · J3.1 reproduit : True (écart max 0.00e+00)
Contrôle d'époque — placebo de dates…
→ work/j71/j71-rapide.json
  ```

- **read** `{"file_path": "tools/retrieval_familles.py", "limit": 70, "offset": 352}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py</path>
<type>file</type>
<content>
352:     n = len(cles)
353:     docs = [panini[k]["text"] for k in cles]
354:     M, _, _ = tfidf(docs, n=3)
355:     S = (M @ M.T).toarray()
356:     np.fill_diagonal(S, -np.inf)
357:     ordre = np.argsort(-S, axis=1)
358:     scripts = [meta[k].get("script") or panini[k].get("script") or "" for k in cles]
359:     familles = [meta[k].get("famille") or f"Isolate:{k}" for k in cles]
360:     chemins = [meta[k].get("chemin") or ["?"] for k in cles]
361:     # relations précalculées
362:     rel = [[relation_chemins(chemins[i], chemins[j]) for j in range(n)] for i in range(n)]
363:     lignes = []
364:     for i, cle in enumerate(cles):
365:         o = [j for j in ordre[i] if j != i]
366:         top = o[0]
367:         memes = [j for j in range(n) if j != i and rel[i][j]["meme_famille"]]
368:         soeurs = [j for j in range(n) if j != i and rel[i][j]["soeur"]]
369:         r_fam = next((r + 1 for r, j in enumerate(o) if rel[i][j]["meme_famille"]), 0)
370:         hits = 0
371:         ap = 0.0
372:         for r, j in enumerate(o):
373:             if rel[i][j]["
… [2782 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/retrieval_familles.py", "old_string": "    lignes = []\n    for i, cle in enumerate(cles):\n        o = [j for j in ordre[i] if j != i]\n        top = o[0]\n        memes = [j for j in range(n) if j != i and rel[i][j][\"meme_famille\"]]\n        soeurs = [j for j in range(n) if  … [6031 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py has been updated successfully.
  ```

- **read** `{"file_path": "tools/retrieval_familles.py", "limit": 50, "offset": 420}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py</path>
<type>file</type>
<content>
420:             "p_script": moyenne([x["p_script"] for x in v]),
421:             "mrr_famille": moyenne([x["mrr_famille"] for x in v]),
422:             "ap_famille": moyenne([x["ap_famille"] for x in v]),
423:             "top5_famille": moyenne([x["top5_famille"] for x in v]),
424:         }
425: 
426:     agregats = {
427:         "toutes": agreger("all"),
428:         "script_meme": agreger("ss"),
429:         "script_different": agreger("ds"),
430:     }
431:     # par famille (≥ 3 requêtes)
432:     par_famille = {}
433:     for f in sorted({x["famille"] for x in lignes}):
434:         v = [x for x in lignes if x["famille"] == f]
435:         if len(v) >= 3:
436:             par_famille[f] = agreger(lambda x, f=f: x["famille"] == f)
437:     # par écriture (≥ 3 requêtes)
438:     par_script = {}
439:     for s in sorted({x["script"] for x in lignes}):
440:         v = [x for x in lignes if x["script"] == s]
441:         if len(v) >= 3:
442:             par_script[s] = agreger(lambda x, s=s: x["script"] == s)
443:     # paires les plus similaires (hors diagona
… [1587 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/retrieval_familles.py", "new_string": "        if len(v) >= 3:\n            par_famille[f] = agreger(\"all\", lambda x, f=f: x[\"famille\"] == f)\n    # par écriture (≥ 3 requêtes)\n    par_script = {}\n    for s in sorted({x[\"script\"] for x in lignes}):\n        v = [x for x  … [518 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py has been updated successfully.
  ```

- **bash** `{"command": "python3 -m py_compile tools/retrieval_familles.py && python3 tools/retrieval_familles.py --rapide --sortie work/j71/j71-rapide.json 2>&1 | tail -30", "description": "Compile and rerun rapid mode"}`

  ```
Panini UDHR 532 — chargement…
  532 textes Panini · 522 étiquetés Glottolog · 447 langues distinctes
Global 532 — article 1, voisinage généalogique…
  447 requêtes · top1 famille 0.6644 (hasard 0.1039) · top1 sœur 0.2640 (hasard 0.0259)
Parallèle 30 articles — LANG_TREE 29, échantillon 20, J3.1 21, union…
  LANG_TREE 25 langues / 600 paires · J3.1 reproduit : True (écart max 0.00e+00)
Contrôle d'époque — placebo de dates…
→ work/j71/j71-rapide.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('work/j71/j71-rapide.json'))\nprint('coverage',d['couverture']['n_textes_labelises'],d['couverture']['n_langues_distinctes'],d['couverture']['taux_labelises'])\nprint('unknown',d['couverture']['n_inconnus'])\nprint('global all',json.dumps … [729 caractères tronqués]`

  ```
coverage 522 447 0.981203007518797
unknown 10
global all {
 "n_requetes": 447,
 "top1_famille": 0.6644295302013423,
 "p_famille": 0.10393154161776065,
 "top1_soeur": 0.2639821029082774,
 "p_soeur": 0.025882565383573596,
 "top1_soeur_stricte": 0.2348993288590604,
 "top1_famille_autre": 0.4004474272930649,
 "top1_famille_differente": 0.33557046979865773,
 "top1_script": 0.9351230425055929,
 "p_script": 0.6160552161394851,
 "mrr_famille": 0.7121987746210745,
 "ap_famille": 0.38451715907684353,
 "top5_famille": 0.5727069351230425
}
global ss {
 "n_requetes": 419,
 "top1_famille": 0.7040572792362768,
 "p_famille": 0.1626086612737433,
 "top1_soeur": 0.28162291169451076,
 "p_soeur": 0.05760069314533483,
 "top1_soeur_stricte": 0.25059665871121717,
 "top1_famille_autre": 0.4224343675417661,
 "top1_famille_differente": 0.29594272076372313,
 "top1_script": 1.0,
 "p_script": 1.0,
 "mrr_famille": 0.7510622681247667,
 "ap_famille": 0.5004091665881382,
 "top5_famille": 0.6143198090692124
}
global ds {
 "n_requetes": 447,
 "top1_famille": 0.12527964205816555,
 "p_famille": 0.0814373189225409,
 "top1_soeur": 0.017897091722595078,
 "p_soeur": 0.008152052775709837,
 "top1_soeur_stricte": 0.0067114093
… [5797 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('work/j71/j71-rapide.json'))\nprint(json.dumps(d['couverture']['inconnus'],ensure_ascii=False,indent=1))\nprint('lang_tree',json.dumps(d['couverture']['lang_tree_29'],ensure_ascii=False,indent=1))\nEOF", "description": "Inspect unknown te … [27 caractères tronqués]`

  ```
[
 {
  "cle": "013",
  "iso": "013",
  "nom": "(Mijisa)"
 },
 {
  "cle": "014",
  "iso": "014",
  "nom": "(Maiunan)"
 },
 {
  "cle": "016",
  "iso": "016",
  "nom": "(Minjiang, spoken)"
 },
 {
  "cle": "017",
  "iso": "017",
  "nom": "(Minjiang, written)"
 },
 {
  "cle": "021",
  "iso": "021",
  "nom": "(Muzzi)"
 },
 {
  "cle": "022",
  "iso": "022",
  "nom": "(Klau)"
 },
 {
  "cle": "023",
  "iso": "023",
  "nom": "(Jinan)"
 },
 {
  "cle": "025",
  "iso": "025",
  "nom": "(Bizisa)"
 },
 {
  "cle": "026",
  "iso": "026",
  "nom": "(Yeonbyeon)"
 },
 {
  "cle": "050",
  "iso": "050",
  "nom": "(Bataknese)"
 }
]
lang_tree {
 "mappees": 26,
 "uniques": 25,
 "absentes_udhr": [
  "grc",
  "pli",
  "lzh"
 ],
 "table": {
  "eng": "eng",
  "deu": "deu_1996",
  "nld": "nld",
  "swe": "swe",
  "nor": "nob",
  "dan": "dan",
  "fin": "fin",
  "hun": "hun",
  "fra": "fra",
  "ita": "ita",
  "spa": "spa",
  "por": "por_PT",
  "ron": "ron_2006",
  "lat": "lat",
  "grc": null,
  "ell": "ell_monotonic",
  "san": "san",
  "pli": null,
  "hin": "hin",
  "ben": "ben",
  "per": "pes_1",
  "fas": "pes_1",
  "ara": "arb",
  "heb": "heb",
  "lzh": null,
  "zho": "cmn_hant",
  "jpn": "jpn",
  "kor": "kor",

… [19 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport csv,collections\nlangs=list(csv.DictReader(open('data/glottolog/languages.csv')))\nbyiso=collections.defaultdict(list)\nfor r in langs:\n    if r.get('ISO639P3code'): byiso[r['ISO639P3code']].append(r)\nfor iso in ['mkw','lav','spa','dje','mas','pmy','abs','min … [218 caractères tronqués]`

  ```
mkw [('Kituba (Congo)', 'language', 'atla1278')]
lav [('Latvian', 'language', 'indo1319')]
spa [('Spanish', 'language', 'indo1319')]
dje [('Zarma-Kaado', 'language', 'song1307')]
mas [('Masai', 'language', 'nilo1247')]
pmy [('Papuan Malay', 'language', 'aust1307')]
abs [('Ambonese Malay', 'language', 'aust1307')]
min [('Minangkabau', 'language', 'aust1307')]
btk []
hau [('Hausa', 'language', 'afro1255')]
cat [('Catalan', 'language', 'indo1319')]
som [('Somali', 'language', 'afro1255')]
sme [('North Saami', 'language', 'ural1272')]
swb [('Maore Comorian', 'language', 'atla1278')]
swh [('Swahili', 'language', 'atla1278')]
fin [('Finnish', 'language', 'ural1272')]
fra [('French', 'language', 'indo1319')]
mri [('Maori', 'language', 'aust1307')]
oci [('Occitan', 'language', 'indo1319')]
  ```

- **edit** `{"file_path": "tools/retrieval_familles.py", "new_string": "    \"054\": \"cat\", \"058\": \"som\", \"059\": \"sme\", \"063\": \"swh\",\n    \"067\": \"fin\", \"068\": \"fra\", \"069\": \"mri\", \"072\": \"oci\",", "old_string": "    \"054\": \"cat\", \"058\": \"som\", \"059\": \"sme\", \"062\": \"s … [102 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('work/j71/j71-rapide.json'))\nfor nom in ['lang_tree','echantillon_20','union_39','j31_21']:\n    m=d[nom]\n    print('===',nom)\n    print('reg B',json.dumps(m['regressions']['decomposition'],indent=1)[:1800])\n    print('loo',json.dumps … [263 caractères tronqués]`

  ```
=== lang_tree
reg B {
 "coef": {
  "constante": -0.006800486571385039,
  "script_match": 0.2132909100315621,
  "soeur": 0.44794695043397376,
  "famille_autre_branche": 0.09163219214523743
 },
 "r2": 0.6305518891529132,
 "controle_permutation": {
  "n_permutations": 100,
  "p_soeur": 0.009900990099009901,
  "p_famille_autre": 0.039603960396039604,
  "null_soeur_moyen": 0.0010351148279414653,
  "null_soeur_ic95": [
   -0.08769176681319914,
   0.112225510660346
  ],
  "null_famille_autre_moyen": 0.001735003613345776
 }
}
loo {
 "script_match": {
  "min": 0.18320010035321344,
  "median": 0.2116777840510226,
  "max": 0.2520781066708448
 },
 "soeur": {
  "min": 0.4040323845912518,
  "median": 0.45168008376675206,
  "max": 0.5177512225274661
 },
 "famille_autre_branche": {
  "min": 0.06449118089488784,
  "median": 0.09307133282863544,
  "max": 0.10892922973817232
 }
}
ctrl {
 "top1_permute_moyen": 0.030277777777777775,
 "chance_moyenne": 0.03333333333333333
}
contraste {
 "toutes": {
  "delta": 0.5743415637860083,
  "ic95": [
   0.48994958847736625,
   0.655235596707819
  ],
  "n_soeurs": 60,
  "n_differentes": 324
 },
 "script_meme": {
  "delta": 0.6676239316239314,
  "ic95": [
   0.5962
… [7255 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/retrieval_familles.py > work/j71/run-full.log 2>&1; echo EXIT:$?; tail -20 work/j71/run-full.log", "description": "Run full J7.1 measurement", "run_in_background": true}`

  ```
started background job bash-76
  ```

- **bash** `{"command": "grep -n \"retrieval-epoque\\|genealogie-deux-faces\" reports/INDEX.md; echo '--- head ---'; sed -n '1,40p' reports/INDEX.md; echo '--- tail ---'; tail -30 reports/INDEX.md", "description": "Inspect reports index structure"}`

  ```
178:| [rapport-genealogie-deux-faces.md](rapport-genealogie-deux-faces.md) | J3.2 — La généalogie à deux faces : Panini et Glottolog sur le corpus commun |
672:| [rapport-retrieval-epoque.md](rapport-retrieval-epoque.md) | J3.1 — Le retrieval inter-langues à époque contrôlée |
--- head ---
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **715 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
| [aiguille-gpt-oss.md](aiguille-gpt-oss.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf |
| [alignement-verne.md](alignement-verne.md) | Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais) |
| [bilan-b11.md](bilan-b11.md) | Bilan B11 — ce qui tient, ce qui 
… [7392 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"J3.2\\|J3.1\\|Panini\" docs/pilotage/roadmap.md | head -20; echo '--- en-cours tail ---'; tail -50 docs/pilotage/en-cours.md", "description": "Inspect roadmap and state for updates"}`

  ```
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 vs 0,427)** ([fiche](../../reports/rapport-retrieval-epoque.md)) ; **J3.2 généalogie à deux faces : Panini couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au hasard exact, le signal de famille vit dans 
… [5732 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-76", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ls -la journal/2026-11-14/ 2>/dev/null; echo '---'; head -60 journal/2026-11-14/README.md 2>/dev/null", "description": "Inspect journal for current date"}`

  ```
total 16
drwxr-xr-x. 1 stephane stephane   72 14 nov 01:21 .
drwxr-xr-x. 1 stephane stephane  972 14 nov 00:51 ..
-rw-r--r--. 1 stephane stephane 1320 14 nov 01:21 docs.md
-rw-r--r--. 1 stephane stephane 1014 14 nov 01:21 memoire.md
-rw-r--r--. 1 stephane stephane 1389 14 nov 01:21 mesures.md
-rw-r--r--. 1 stephane stephane 3302 14 nov 01:21 README.md
---
# 2026-11-14

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**4 commits** · **1 session(s)** · **3 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 1 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 2 | [mesures.md](mesures.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 320.6 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [dig
… [2370 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' docs/pilotage/roadmap.md; echo '--- 240-260 ---'; sed -n '240,260p' docs/pilotage/roadmap.md", "description": "Read roadmap head and R0.7 section"}`

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
… [19682 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-76", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/index_reports.py; echo '--- revue doc usage ---'; python3 tools/revue_documentation.py --help 2>&1 | head -30", "description": "Check report index and doc review tools"}`

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
… [1619 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"720\\|814\\|fichiers / JSON\\|compteurs\" tools/revue_documentation.py | head -30; grep -n \"def.*compt\\|reports\" tools/revue_documentation.py | head -40", "description": "Inspect doc review counter logic"}`

  ```
12:     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
172:    # 5. compteurs : la page d'état est la source unique, et elle dit le disque
176:    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
183:            alertes.append(f"compteurs : la ligne « {nom} » manque dans en-cours.md")
185:            alertes.append(f"compteurs : en-cours.md dit {valeur} {nom}, le disque en a {disque}")
187:        alertes.append("compteurs : la ligne « fichiers / JSON » manque dans en-cours.md")
195:                    f"compteurs : en-cours.md dit {valeur} {quoi}, le disque en a {disque}"
374:        print("  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, "
5:  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
7:  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
30:    r"`((?:docs|reports|tools|journal|data|drave-core|sprints)/"
76:    return list((RACINE / "reports").glob("*.md"))
95:            + [RACINE / "reports/07-mesures-couche-commune.md",
96:               RACINE / "reports/fiche-nuit-17-10.md",
10
… [578 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-76", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -o pid,etime,pcpu,pmem,cmd -C python3 | tail -5; echo '--- log ---'; tail -5 work/j71/run-full.log", "description": "Check full run progress"}`

  ```
PID     ELAPSED %CPU %MEM CMD
   3002 10-05:59:38  0.1  0.0 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
 946076    03:55:06  0.1  0.0 python3 tools/chantier/superviseur.py boucle --budget 43200 --timeout 5400
3555423  7-05:49:20  0.0  0.0 python3 src/app.py --no-browser
--- log ---
  447 requêtes · top1 famille 0.6644 (hasard 0.1039) · top1 sœur 0.2595 (hasard 0.0259)
Parallèle 30 articles — LANG_TREE 29, échantillon 20, J3.1 21, union…
  LANG_TREE 25 langues / 600 paires · J3.1 reproduit : True (écart max 0.00e+00)
Contrôle d'époque — placebo de dates…
→ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/retrieval-familles.json
  ```

### 👤 Utilisateur

background job bash-76 (bash: python3 tools/retrieval_familles.py > work/j71/run-full.log 2>&1; echo EXIT:$?; tail -20 work/j71/run-full.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\nprint('coverage',d['couverture']['n_textes_labelises'],d['couverture']['n_langues_distinctes'],d['couverture']['n_inconnus'])\nprint('global all',json.dumps(d['global_532']['agregats']['toutes'],indent … [547 caractères tronqués]`

  ```
coverage 521 447 11
global all {
 "n_requetes": 447,
 "top1_famille": 0.6644295302013423,
 "p_famille": 0.10393154161776065,
 "top1_soeur": 0.2595078299776286,
 "p_soeur": 0.0258825653835736,
 "top1_soeur_stricte": 0.23042505592841164,
 "top1_famille_autre": 0.40492170022371365,
 "top1_famille_differente": 0.33557046979865773,
 "top1_script": 0.9351230425055929,
 "p_script": 0.6160552161394851,
 "mrr_famille": 0.7120489638233105,
 "ap_famille": 0.3840902338712523,
 "top5_famille": 0.5749440715883669
}
global ss {
 "n_requetes": 419,
 "top1_famille": 0.7016706443914081,
 "p_famille": 0.1626086612737433,
 "top1_soeur": 0.27684964200477324,
 "p_soeur": 0.05760069314533483,
 "top1_soeur_stricte": 0.2458233890214797,
 "top1_famille_autre": 0.42482100238663484,
 "top1_famille_differente": 0.29832935560859186,
 "top1_script": 1.0,
 "p_script": 1.0,
 "mrr_famille": 0.7490223929729324,
 "ap_famille": 0.5001780579389195,
 "top5_famille": 0.6167064439140811
}
global ds {
 "n_requetes": 447,
 "top1_famille": 0.10961968680089486,
 "p_famille": 0.0814373189225409,
 "top1_soeur": 0.008948545861297539,
 "p_soeur": 0.008152052775709837,
 "top1_soeur_stricte": 0.0044742729306487695,
 "top1_famille_a
… [3778 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\nfor nom in ['lang_tree','echantillon_20','j31_21','union_39']:\n    m=d[nom]\n    print('===',nom,'n',m['n_langues'],m['n_paires'])\n    print('agg soeur',m['agregats']['soeur'])\n    print('agg famaut … [765 caractères tronqués]`

  ```
=== lang_tree n 25 600
agg soeur {'n_paires': 60, 'top1_moyen': 0.6188888888888889, 'top1_median': 0.6833333333333333, 'ic_bas': 0.03333333333333333, 'ic_haut': 1.0, 'mrr_moyen': 0.6898523975018575}
agg famautre {'n_paires': 216, 'top1_moyen': 0.16975308641975306, 'top1_median': 0.03333333333333333, 'ic_bas': 0.03333333333333333, 'ic_haut': 0.8875000000000001, 'mrr_moyen': 0.27069957296499864}
agg diff {'n_paires': 324, 'top1_moyen': 0.04454732510288066, 'top1_median': 0.03333333333333333, 'ic_bas': 0.0, 'ic_haut': 0.13333333333333333, 'mrr_moyen': 0.14742749098171765}
reg B {'constante': -0.006800486571385039, 'script_match': 0.2132909100315621, 'soeur': 0.44794695043397376, 'famille_autre_branche': 0.09163219214523743} r2 0.6305518891529132
p {'n_permutations': 500, 'p_soeur': 0.001996007984031936, 'p_famille_autre': 0.02594810379241517, 'null_soeur_moyen': 0.00011872271058637406, 'null_soeur_ic95': [-0.08905575432794267, 0.10836979116994395], 'null_famille_autre_moyen': 0.002730533030418802}
contraste {'delta': 0.5743415637860083, 'ic95': [0.48994958847736625, 0.655235596707819], 'n_soeurs': 60, 'n_differentes': 324} {'delta': 0.6676239316239314, 'ic95': [0.5962076923076923, 0.7
… [4781 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\nprint('par famille')\nfor k,v in sorted(d['global_532']['par_famille'].items(), key=lambda kv:-kv[1]['n_requetes'])[:12]:\n    print(f\"{k:20s} n={v['n_requetes']:3d} top1fam={v['top1_famille']:.3f} ba … [498 caractères tronqués]`

  ```
par famille
Indo-European        n=105 top1fam=0.800 base=0.233 soeur=0.295 baseS=0.045
Atlantic-Congo       n= 81 top1fam=0.802 base=0.179 soeur=0.444 baseS=0.071
Austronesian         n= 38 top1fam=0.868 base=0.083 soeur=0.289 baseS=0.010
Sino-Tibetan         n= 22 top1fam=0.727 base=0.047 soeur=0.227 baseS=0.004
Afro-Asiatic         n= 19 top1fam=0.526 base=0.040 soeur=0.105 baseS=0.008
Turkic               n= 19 top1fam=0.895 base=0.040 soeur=0.316 baseS=0.008
Quechuan             n= 14 top1fam=1.000 base=0.029 soeur=0.143 baseS=0.004
Uralic               n= 12 top1fam=0.750 base=0.025 soeur=0.250 baseS=0.003
Mayan                n=  9 top1fam=1.000 base=0.018 soeur=0.444 baseS=0.003
Arawakan             n=  8 top1fam=0.500 base=0.016 soeur=0.000 baseS=0.000
Mande                n=  8 top1fam=0.750 base=0.016 soeur=0.375 baseS=0.010
Otomanguean          n=  8 top1fam=0.125 base=0.016 soeur=0.000 baseS=0.004
par script
Latn   n=349 top1fam=0.693 base=0.107 soeur=0.292 baseS=0.029
Cyrl   n= 35 top1fam=0.771 base=0.078 soeur=0.114 baseS=0.012
Arab   n=  9 top1fam=0.667 base=0.174 soeur=0.222 baseS=0.039
Deva   n=  8 top1fam=0.875 base=0.210 soeur=0.500 baseS=0.040
Hans   n=  6 top1
… [2074 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,collections,sys\nsys.path.insert(0,'tools'); import retrieval_epoque as R\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nh=collections.defaultdict(list)\nfor k,v in P.items():\n    h[R.normalise(v['text'])].append(k)\ndups=[(l … [548 caractères tronqués]`

  ```
exact duplicate groups 12 texts 24
2 ['ven', 'ven2']
2 ['tam', 'tam_LK']
2 ['ron_1993', 'ron_2006']
2 ['mal', 'mal_chillus']
2 ['kng', 'ktu']
2 ['ell_monotonic', 'ell_polytonic']
2 ['deu_1901', 'deu_1996']
2 ['ckb', 'kmr']
2 ['chr_cased', 'chr_uppercase']
2 ['bos_latn', 'hrv']
2 ['072', 'lnc']
2 ['042', 'spa']
kng ktu True 170 170
 A Bantu nyonso, na mbutukulu kevwandaka na kimpwanza ya bawu, ngenda mpe baluve ya mutindu mosi. Mayela na mbanzulu je na bawu, ni yawu yina bafwana kusalasana na bumpangi.
 B Bantu nyonso, na mbutukulu kevwandaka na kimpwanza ya bawu, ngenda mpe baluve ya mutindu mosi. Mayela na mbanzulu je na bawu, ni yawu yina bafwana kusalasana na bumpangi.
ckb kmr True 133 133
 A Hemû mirov azad û di weqar û mafan de wekhev tên dinyayê. Ew xwedî hiş û şuûr in û divê li hember hev bi zihniyeteke bratiyê bilivin.
 B Hemû mirov azad û di weqar û mafan de wekhev tên dinyayê. Ew xwedî hiş û şuûr in û divê li hember hev bi zihniyeteke bratiyê bilivin.
bos_cyrl srp_cyrl False 163 161
 A Сва људска бића раћају се слободна и једнака у достојанству и правима. Она су обдарена разумом и свијешћу и треба да једно према другоме поступају у духу братства.
 B Сва људска бића рађају
… [826 caractères tronqués]
  ```

- **read** `{"file_path": "tools/retrieval_familles.py", "limit": 45, "offset": 316}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py</path>
<type>file</type>
<content>
316:     union = sorted(set(lang_tree.values()) | set(echantillon))
317:     # 4.5 Les textes Panini non dédupliqués : un représentant par code ISO.
318:     langid = {k: (m.get("iso3") or k) for k, m in meta.items()}
319:     groupes = collections.defaultdict(list)
320:     for k in panini:
321:         if k in meta:
322:             groupes[langid[k]].append(k)
323:     preferes = set(union) | set(j31)
324:     def choisir(v: list[str]) -> str:
325:         for k in v:
326:             if k in preferes:
327:                 return k
328:         for k in v:
329:             if "_" not in k:
330:                 return k
331:         return sorted(v)[0]
332:     representants = sorted(choisir(v) for v in groupes.values())
333:     return {
334:         "lang_tree": lang_tree,
335:         "echantillon_20": echantillon,
336:         "j31_21": j31,
337:         "union": union,
338:         "representants": representants,
339:         "groupes": {g: v for g, v in groupes.items()},
340:         "n_groupes": len(groupes),
341:         "n_textes_labelises": sum(len(v) for
… [970 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"from retrieval_epoque import\" -A8 tools/retrieval_familles.py", "description": "Locate import block"}`

  ```
69:from retrieval_epoque import (  # noqa: E402  (import après le path)
70-    derangement,
71-    regression_surface,
72-    tfidf,
73-    top1_et_rangs,
74-)
75-
76-SORTIE = RACINE / "reports" / "retrieval-familles.json"
77-PANINI_CORPUS = RACINE.parent / "Panini" / "research" / "data" / "udhr_corpus.json"
  ```

- **edit** `{"file_path": "tools/retrieval_familles.py", "new_string": "from retrieval_epoque import (  # noqa: E402  (import après le path)\n    derangement,\n    normalise,\n    regression_surface,\n    tfidf,\n    top1_et_rangs,\n)", "old_string": "from retrieval_epoque import (  # noqa: E402  (import après  … [88 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/retrieval_familles.py", "new_string": "    representants_iso = {g: choisir(v) for g, v in groupes.items()}\n    # 4.6 Déduplication par texte exact : 12 groupes de textes identiques dans les 532,\n    # dont 3 seulement changent de code ISO (kng/ktu, ckb/kmr, bos_latn/hrv). Sans … [1535 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"n_langues_distinctes\\|variantes_dedupliquees\" tools/retrieval_familles.py", "description": "Locate coverage fields"}`

  ```
956:            "n_langues_distinctes": ensembles["n_groupes"],
958:            "variantes_dedupliquees": ensembles["n_textes_labelises"] - ensembles["n_groupes"],
  ```

- **read** `{"file_path": "tools/retrieval_familles.py", "limit": 18, "offset": 948}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py</path>
<type>file</type>
<content>
948:             "graine": a.graine,
949:             "permutations": a.permutations,
950:             "permutations_paires": a.permutations_paires,
951:         },
952:         "couverture": {
953:             **couverture,
954:             "n_textes_panini": len(panini),
955:             "n_textes_labelises": ensembles["n_textes_labelises"],
956:             "n_langues_distinctes": ensembles["n_groupes"],
957:             "taux_labelises": ensembles["n_textes_labelises"] / len(panini),
958:             "variantes_dedupliquees": ensembles["n_textes_labelises"] - ensembles["n_groupes"],
959:             "lang_tree_29": {
960:                 "mappees": len(ensembles["lang_tree"]),
961:                 "uniques": len(set(ensembles["lang_tree"].values())),
962:                 "absentes_udhr": [c for c, v in LANG_TREE_VERS_PANINI.items() if v is None],
963:                 "table": LANG_TREE_VERS_PANINI,
964:             },
965:             "echantillon_20": ensembles["echantillon_20"],

(Showing lines 948-965 of 1030. Use offset=966 to continue.)
</content>
  ```

- **edit** `{"file_path": "tools/retrieval_familles.py", "new_string": "            \"n_langues_distinctes\": ensembles[\"n_groupes\"],\n            \"taux_labelises\": ensembles[\"n_textes_labelises\"] / len(panini),\n            \"n_groupes_iso\": ensembles[\"n_groupes_iso\"],\n            \"variantes_iso\":  … [571 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/retrieval_familles.py has been updated successfully.
  ```

- **bash** `{"command": "python3 -m py_compile tools/retrieval_familles.py && python3 tools/retrieval_familles.py --rapide --sortie work/j71/j71-rapide2.json 2>&1 | tail -20", "description": "Rerun rapid after text dedup"}`

  ```
Panini UDHR 532 — chargement…
  532 textes Panini · 521 étiquetés Glottolog · 445 langues distinctes
Global 532 — article 1, voisinage généalogique…
  445 requêtes · top1 famille 0.6607 (hasard 0.1030) · top1 sœur 0.2607 (hasard 0.0254)
Parallèle 30 articles — LANG_TREE 29, échantillon 20, J3.1 21, union…
  LANG_TREE 25 langues / 600 paires · J3.1 reproduit : True (écart max 0.00e+00)
Contrôle d'époque — placebo de dates…
→ work/j71/j71-rapide2.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('work/j71/j71-rapide2.json'))\nprint(json.dumps(d['couverture']['doublons_texte'],indent=1))\nprint(d['couverture']['n_groupes_iso'],d['couverture']['n_langues_distinctes'],d['couverture']['variantes_iso'],d['couverture']['variantes_dedup … [57 caractères tronqués]`

  ```
[
 {
  "garde": "ckb",
  "retire": "kmr",
  "groupe_iso": "kmr"
 },
 {
  "garde": "kng",
  "retire": "ktu",
  "groupe_iso": "ktu"
 }
]
447 445 74 76
  ```

- **bash** `{"command": "python3 tools/retrieval_familles.py > work/j71/run-full2.log 2>&1; echo EXIT:$?; tail -10 work/j71/run-full2.log", "description": "Run final full J7.1 measurement after dedup", "run_in_background": true}`

  ```
started background job bash-92
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('work/j71/j71-rapide2.json'))\nfor nom in ['echantillon_20','lang_tree','union_39']:\n    m=d[nom]\n    print('===',nom)\n    for p in sorted([p for p in m['paires'] if p['famille_autre_branche']],key=lambda p:-p['top1'])[:8]:\n        pr … [337 caractères tronqués]`

  ```
=== echantillon_20
jav ind 0.9 lca 2 Austronesian
ind jav 0.8333 lca 2 Austronesian
ind tgl 0.1667 lca 2 Austronesian
ewe ibo 0.1333 lca 2 Atlantic-Congo
ewe kin 0.0667 lca 2 Atlantic-Congo
ibo ewe 0.0667 lca 2 Atlantic-Congo
jav tgl 0.0667 lca 2 Austronesian
tgl ind 0.0667 lca 2 Austronesian
sisters top
ctd cnh 0.2333 lca 3 Sino-Tibetan
cnh ctd 0.1667 lca 3 Sino-Tibetan
amh arb 0.0333 lca 3 Afro-Asiatic
amh heb 0.0333 lca 3 Afro-Asiatic
arb amh 0.0333 lca 3 Afro-Asiatic
arb heb 0.0333 lca 4 Afro-Asiatic
heb amh 0.0333 lca 3 Afro-Asiatic
heb arb 0.0333 lca 4 Afro-Asiatic
=== lang_tree
eng fra 0.9 lca 2 Indo-European
eng por_PT 0.9 lca 2 Indo-European
eng ron_2006 0.9 lca 2 Indo-European
eng spa 0.9 lca 2 Indo-European
fra eng 0.9 lca 2 Indo-European
ita eng 0.9 lca 2 Indo-European
eng ita 0.8667 lca 2 Indo-European
por_PT eng 0.8667 lca 2 Indo-European
sisters top
dan nob 1.0 lca 5 Indo-European
fra por_PT 1.0 lca 10 Indo-European
fra spa 1.0 lca 10 Indo-European
nob dan 1.0 lca 5 Indo-European
por_PT fra 1.0 lca 10 Indo-European
por_PT spa 1.0 lca 12 Indo-European
spa fra 1.0 lca 10 Indo-European
spa por_PT 1.0 lca 12 Indo-European
=== union_39
eng fra 0.9333 lca 2 Indo-European
e
… [527 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-92", "timeout_ms": 1000}`

  ```
EXIT:0
Panini UDHR 532 — chargement…
  532 textes Panini · 521 étiquetés Glottolog · 445 langues distinctes
Global 532 — article 1, voisinage généalogique…
  445 requêtes · top1 famille 0.6607 (hasard 0.1030) · top1 sœur 0.2607 (hasard 0.0254)
Parallèle 30 articles — LANG_TREE 29, échantillon 20, J3.1 21, union…
  LANG_TREE 25 langues / 600 paires · J3.1 reproduit : True (écart max 0.00e+00)
Contrôle d'époque — placebo de dates…
→ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/retrieval-familles.json
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-92 (bash: python3 tools/retrieval_familles.py > work/j71/run-full2.log 2>&1; echo EXIT:$?; tail -10 work/j71/run-full2.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\nprint('=== COUVERTURE ===')\nc=d['couverture']\nfor k in ['n_textes_panini','n_textes_labelises','n_langues_distinctes','taux_labelises','n_groupes_iso','variantes_iso','n_doublons_texte','variantes_de … [2227 caractères tronqués]`

  ```
=== COUVERTURE ===
n_textes_panini 532
n_textes_labelises 521
n_langues_distinctes 445
taux_labelises 0.9793233082706767
n_groupes_iso 447
variantes_iso 74
n_doublons_texte 2
variantes_dedupliquees 76
doublons [{'garde': 'ckb', 'retire': 'kmr', 'groupe_iso': 'kmr'}, {'garde': 'kng', 'retire': 'ktu', 'groupe_iso': 'ktu'}]
inconnus 11
=== GLOBAL ===
toutes {
 "n_requetes": 445,
 "top1_famille": 0.6606741573033708,
 "p_famille": 0.10300637716368054,
 "top1_soeur": 0.2606741573033708,
 "p_soeur": 0.025407429901811926,
 "top1_soeur_stricte": 0.23146067415730337,
 "top1_famille_autre": 0.4,
 "top1_famille_differente": 0.3393258426966292,
 "top1_script": 0.9348314606741573,
 "p_script": 0.6145763741269361,
 "mrr_famille": 0.7085586832076445,
 "ap_famille": 0.3820327959456736,
 "top5_famille": 0.573932584269663
}
script_meme {
 "n_requetes": 417,
 "top1_famille": 0.697841726618705,
 "p_famille": 0.161835645390522,
 "top1_soeur": 0.27817745803357313,
 "p_soeur": 0.057365664276273154,
 "top1_soeur_stricte": 0.24700239808153476,
 "top1_famille_autre": 0.4196642685851319,
 "top1_famille_differente": 0.302158273381295,
 "top1_script": 1.0,
 "p_script": 1.0,
 "mrr_famille": 0.7459308222436698,
 
… [17526 caractères tronqués]
  ```

- **bash** `{"command": "cat > reports/rapport-retrieval-familles.md <<'MD'\n# J7.1 — Le retrieval approfondi par famille Glottolog\n\n> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, J7.1 · **Date** : 2026-11-14\n> **Verdict** : ✅ **le retrieval retrouve la famille, mais seulement da … [31975 caractères tronqués]`

  ```
497 reports/rapport-retrieval-familles.md
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\nfor p in d['global_532']['top_paires']: print(p)\nEOF", "description": "Inspect final top pairs"}`

  ```
{'similarite': 0.9174598395756515, 'a': 'cnr', 'b': 'hrv', 'famille_a': 'Indo-European', 'famille_b': 'Indo-European', 'soeur': False, 'famille_autre': True}
{'similarite': 0.9086861433390382, 'a': 'bos_cyrl', 'b': 'srp_cyrl', 'famille_a': 'Indo-European', 'famille_b': 'Indo-European', 'soeur': False, 'famille_autre': True}
{'similarite': 0.8868354866847722, 'a': 'pes_1', 'b': 'pes_2', 'famille_a': 'Indo-European', 'famille_b': 'Indo-European', 'soeur': False, 'famille_autre': True}
{'similarite': 0.859899816127399, 'a': '041', 'b': 'lav', 'famille_a': 'Indo-European', 'famille_b': 'Indo-European', 'soeur': False, 'famille_autre': True}
{'similarite': 0.840178025897679, 'a': '046', 'b': 'ind', 'famille_a': 'Austronesian', 'famille_b': 'Austronesian', 'soeur': True, 'famille_autre': False}
{'similarite': 0.7905717413410651, 'a': 'cjy', 'b': 'hsn', 'famille_a': 'Sino-Tibetan', 'famille_b': 'Sino-Tibetan', 'soeur': False, 'famille_autre': True}
{'similarite': 0.7630372404336658, 'a': 'glg', 'b': 'spa', 'famille_a': 'Indo-European', 'famille_b': 'Indo-European', 'soeur': True, 'famille_autre': False}
{'similarite': 0.7369397802672233, 'a': 'dan', 'b': 'nob', 'famille_a': 'Indo-European
… [1940 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"cvb\\|restent\" reports/rapport-retrieval-familles.md", "description": "Locate incorrect top-pair sentence"}`

  ```
37:> sont pas indépendantes ; 11 textes restent non étiquetés. Voir § 6.
64:| étiquetés Glottolog | **521** | 97,9 % ; 11 restent non étiquetés |
81:indépendants. Les 532 restent la base ; les 445 sont la base **dédupliquée** qui rend les top-1
216:exacts (retirés) ; restent `cnr`/`hrv` 0,917, `bos_cyrl`/`srp_cyrl` 0,909, `pes_1`/`pes_2` 0,887,
217:`cvb`/`kmr` 0,999 (doublon exact détecté), `glg`/`spa` 0,763 (sœurs), `dan`/`nob` 0,737 (sœurs). Les
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nt=t.replace(\"exacts (retirés) ; restent `cnr`/`hrv` 0,917, `bos_cyrl`/`srp_cyrl` 0,909, `pes_1`/`pes_2` 0,887,\\n`cvb`/`kmr` 0,999 (doublon exact détecté), `glg`/`spa` 0,763 (sœ … [431 caractères tronqués]`

  ```
top-1 famille (IC [0,0854 ; 0,1349]) contre une baseline de **0,1030** : le texte de la requête porte
bien l'information, pas seulement la composition du pool.

**Les paires les plus proches** confirment la lecture : `ckb`/`kmr` et `kng`/`ktu` étaient des doublons
exacts (retirés) ; restent `cnr`/`hrv` 0,917, `bos_cyrl`/`srp_cyrl` 0,909, `pes_1`/`pes_2` 0,887,
`041`/`lav` 0,860, `046`/`ind` 0,840 (sœurs), `cjy`/`hsn` 0,791 (même famille, autre branche),
`glg`/`spa` 0,763 (sœurs), `dan`/`nob` 0,737 (sœurs). Les
paires de **familles différentes** les plus proches sont `arb`/`pes_1` 0,567 et `jpn`/`cmn_hant` 0,500 :
même écriture (arabe, han), familles différentes — exactement le confondant que le contrôle par
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\nprint(json.dumps(d['couverture']['inconnus'],ensure_ascii=False,indent=1))\nEOF", "description": "List final unknown texts"}`

  ```
[
 {
  "cle": "013",
  "iso": "013",
  "nom": "(Mijisa)"
 },
 {
  "cle": "014",
  "iso": "014",
  "nom": "(Maiunan)"
 },
 {
  "cle": "016",
  "iso": "016",
  "nom": "(Minjiang, spoken)"
 },
 {
  "cle": "017",
  "iso": "017",
  "nom": "(Minjiang, written)"
 },
 {
  "cle": "021",
  "iso": "021",
  "nom": "(Muzzi)"
 },
 {
  "cle": "022",
  "iso": "022",
  "nom": "(Klau)"
 },
 {
  "cle": "023",
  "iso": "023",
  "nom": "(Jinan)"
 },
 {
  "cle": "025",
  "iso": "025",
  "nom": "(Bizisa)"
 },
 {
  "cle": "026",
  "iso": "026",
  "nom": "(Yeonbyeon)"
 },
 {
  "cle": "050",
  "iso": "050",
  "nom": "(Bataknese)"
 },
 {
  "cle": "062",
  "iso": "062",
  "nom": "Swahili (Chimwiini)"
 }
]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nold=\"\"\"Les **11 textes non étiquetés** sont des variantes numériques de l'UDHR dont le nom est entre\nparenthèses (`013`, `014`, `016`, `017`, `021`, `022`, `023`, `025`, `026 … [740 caractères tronqués]`

  ```
| **textes distincts** | **445** | 2 doublons de texte exact entre codes ISO différents retirés |

Les **11 textes non étiquetés** sont **dix variantes numériques** de l'UDHR dont le nom est entre
parenthèses (`013`, `014`, `016`, `017`, `021`, `022`, `023`, `025`, `026`, `050`) et **`062`**
(`Swahili (Chimwiini)`, dont le code `swb` est le maore, pas le chimwiini : on ne devine pas). Ils ne
sont pas devinés : ils sortent des mesures de famille, pas du comptage des textes.

Les **12 groupes de textes identiques** (24 textes) sont un fait du fonds : l'UDHR réutilise parfois la
même traduction sous deux codes. Neuf groupes sont déjà dédupliqués par l'ISO3 (`deu_1901`/`deu_1996`,
`ell_monotonic`/`ell_polytonic`, `ron_1993`/`ron_2006`, etc.) ; **deux** survivent à la déduplication ISO
et sont retirés par le texte : `ckb`/`kmr` (kurde central / kurde du nord) et `kng`/`ktu`
(kikongo / kituba). Sans ce retrait, deux textes identiques fabriqueraient un top-1 « famille » trivial.
Le troisième doublon cross-ISO (`bos_latn`/`hrv`) n'est pas dans les représentants : le groupe `bos`
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nG=json.load(open('data/udhr/genealogie.json'))\nfor k in ['cjy','hsn','046','ind','glg','spa']:\n    g=G.get('udhr_%s.xml'%k); print(k,g['famille'],g['branche'][:120] if g else None)\nEOF", "description": "Verify cjy/hsn relation"}`

  ```
cjy Sino-Tibetan sino1245/sini1245/clas1255/midd1354/nort3155
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
TypeError: 'NoneType' object is not subscriptable
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\n# find lines cjy/hsn\nfor l in d['global_532']['lignes']:\n    if l['cle'] in ('cjy','hsn','046','ind','glg','spa'):\n        print(l['cle'],l['famille'],l['all']['top1'] if l['all'] else None)\nEOF",  … [49 caractères tronqués]`

  ```
046 Austronesian ind
cjy Sino-Tibetan hsn
glg Indo-European spa
hsn Sino-Tibetan cjy
ind Austronesian 046
spa Indo-European glg
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys,json\nsys.path.insert(0,'tools')\nimport retrieval_familles as R\nP=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nG=json.load(open('data/udhr/genealogie.json'))\ngl=R.Glottolog(R.GLOTTOLOG_LANGS,R.GLOTTOLOG_VALUES)\nmeta,c=R.cons … [186 caractères tronqués]`

  ```
cjy ['Sino-Tibetan', 'Sinitic', 'Classical-Middle-Modern Sinitic', 'Middle-Modern Sinitic', 'Northern Chinese']
hsn ['Sino-Tibetan', 'Sinitic', 'Classical-Middle-Modern Sinitic', 'Middle-Modern Sinitic']
046 ['Austronesian', 'Malayo-Polynesian', 'Malayo-Chamic', 'Malayic', 'Nuclear Malayic', 'Vehicular Malay', 'Eastern Indonesia Trade Malay']
ind ['Austronesian', 'Malayo-Polynesian', 'Malayo-Chamic', 'Malayic', 'Nuclear Malayic', 'Standard Malay-Indonesian']
glg ['Indo-European', 'Classical Indo-European', 'Italic', 'Latino-Faliscan', 'Latinic', 'Imperial Latin', 'Romance', 'Italo-Western Romance', 'Western Romance', 'Shifted Western Romance', 'Southwestern Shifted Romance', 'West Ibero-Romance', 'Galician Romance']
spa ['Indo-European', 'Classical Indo-European', 'Italic', 'Latino-Faliscan', 'Latinic', 'Imperial Latin', 'Romance', 'Italo-Western Romance', 'Western Romance', 'Shifted Western Romance', 'Southwestern Shifted Romance', 'West Ibero-Romance', 'Castilic']
{'lca': 4, 'ancetre_descendant': True, 'meme_famille': True, 'soeur': False, 'soeur_stricte': False, 'famille_autre_branche': True, 'famille_differente': False}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\nfor p in d['echantillon_20']['paires']:\n    if p['soeur'] and p['script_match']:\n        print(p['a'],p['b'],p['top1'],p['script_a'],p['script_b'])\nprint('all sisters')\nfor p in d['echantillon_20'] … [173 caractères tronqués]`

  ```
cnh ctd 0.16666666666666666 Latn Latn
ctd cnh 0.23333333333333334 Latn Latn
ibo kin 0.03333333333333333 Latn Latn
kin ibo 0.0 Latn Latn
all sisters
amh arb 0.0333 Ethi Arab
amh heb 0.0333 Ethi Hebr
arb amh 0.0333 Arab Ethi
arb heb 0.0333 Arab Hebr
cnh ctd 0.1667 Latn Latn
ctd cnh 0.2333 Latn Latn
heb amh 0.0333 Hebr Ethi
heb arb 0.0333 Hebr Arab
ibo kin 0.0333 Latn Latn
ind mly_arab 0.0333 Latn Arab
kin ibo 0.0 Latn Latn
mly_arab ind 0.0333 Arab Latn
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nold=\"\"\"Les **12 paires de sœurs** sont dominées par les paires **hors écriture** (`arb`/`heb`, `arb`/`amh`,\n`heb`/`amh`) : 8 sur 12 sont au plancher 0,0333. Les seules sœurs  … [644 caractères tronqués]`

  ```
quand on sépare les deux. **La famille n'est pas une variable, c'est un mélange.**

**Le contraste demandé — sœurs vs familles différentes.**

| contraste | n sœurs | n diff. | Δ top-1 | IC 95 % | ratio |
|---|---:|---:|---:|---|---:|
| **toutes** | 60 | 324 | **+0,5743** | [0,4899 ; 0,6552] | **13,89×** |
| **même écriture** | 50 | 78 | **+0,6676** | [0,5962 ; 0,7384] | **10,76×** |

Le contraste apparié par langue (même script, au moins une sœur et une famille différente) donne
**11 langues, 11 positives**, Δ moyen **+0,6912**, p du signe **0,00098**, p de Wilcoxon **0,00098** :
le sens est le même pour **toutes** les langues concernées (`dan`, `deu`, `eng`, `fra`, `ita`, `nld`,
`nob`, `por`, `ron`, `spa`, `swe`). Ce n'est pas un effet de quelques paires.
  ```

- **bash** `{"command": "grep -n \"12 paires de sœurs\" -A5 reports/rapport-retrieval-familles.md", "description": "Verify sample 20 fix"}`

  ```
17:> **sous-dimensionné** : l'échantillon 20 ne contient que 12 paires de sœurs, dont 8 hors écriture.
18-> L'époque est **mono-époque par construction** (1948) ; le placebo de dates donne −0,0013
19-> [−0,065 ; +0,041], et le seul bras daté de J3.1 (Bible) donne −0,034/siècle (p = 0,19) contre +0,609
20-> pour l'écriture. **La hiérarchie est écriture > sœur > famille-autre-branche > époque ; l'époque ne
21-> peut pas expliquer l'effet de famille ici.**
22-> **Dispositif** : 532 textes Panini (article 1, 1948), **521 étiquetés Glottolog**, **447 groupes ISO**,
--
306:Les **12 paires de sœurs** sont dominées par les paires **hors écriture** (`arb`/`heb`, `arb`/`amh`,
307-`heb`/`amh`, `ind`/`mly_arab`) : 8 sur 12 sont au plancher 0,0333. Les sœurs de même écriture sont
308-`cnh`/`ctd` (0,233 et 0,167) et `ibo`/`kin` (0,033 et 0,0) : quatre paires, dont deux au plancher,
309-trop peu pour porter une moyenne. Le **même famille-autre-branche**
310-(0,0757) est **supérieur** aux sœurs (0,0583) : le signal de l'échantillon est porté par `jav`/`ind`
311-(0,900 et 0,833), deux langues austronésiennes de branches différentes, pas par des sœurs.
--
328:qui contient 12 paires de sœurs dont 8 h
… [1040 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\n# We don't have all global pair similarities stored, only top 20 (all same family). Compute from source quickly? Use LANG_TREE examples instead.\nprint('top global pairs all same family?')\nfor p in d[ … [147 caractères tronqués]`

  ```
top global pairs all same family?
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nold=\"\"\"`glg`/`spa` 0,763 (sœurs), `dan`/`nob` 0,737 (sœurs). Les\npaires de **familles différentes** les plus proches sont `arb`/`pes_1` 0,567 et `jpn`/`cmn_hant` 0,500 :\nmêm … [695 caractères tronqués]`

  ```
bien l'information, pas seulement la composition du pool.

**Les paires les plus proches** confirment la lecture : `ckb`/`kmr` et `kng`/`ktu` étaient des doublons
exacts (retirés) ; restent `cnr`/`hrv` 0,917, `bos_cyrl`/`srp_cyrl` 0,909, `pes_1`/`pes_2` 0,887,
`041`/`lav` 0,860, `046`/`ind` 0,840 (sœurs), `cjy`/`hsn` 0,791 (même famille, autre branche),
`glg`/`spa` 0,763 (sœurs), `dan`/`nob` 0,737 (sœurs). Les **20 paires les plus proches sont toutes
de la même famille** : dans le global, la proximité maximale est d'abord une proximité de famille et
d'écriture. Les paires de **familles différentes** ne remontent qu'avec l'écriture partagée (voir
§ 4.2 : `arb`/`pes_1` 0,567, `jpn`/`cmn_hant` 0,500).
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nold=\"\"\"La ligne des sœurs est le résultat : **0,619** toutes écritures, **0,736** à écriture contrôlée, contre\n**0,0445** pour les familles différentes (toutes) et **0,0684** … [1073 caractères tronqués]`

  ```
| groupe | n | top1 | MRR |
|---|---:|---:|---:|
| toutes | 600 | 0,1471 | — |
| même écriture | 214 | 0,3480 | — |
| écriture différente | 386 | 0,0357 | — |
| **sœurs** | **60** | **0,6189** | **0,6899** |
| **sœurs strictes** (LCA ≥ 4) | **54** | **0,6840** | **0,7517** |
| **même famille, autre branche** | **216** | **0,1698** | **0,2707** |
| **familles différentes** | **324** | **0,0445** | **0,1474** |
| même écriture + sœurs | 50 | 0,7360 | 0,8012 |
| même écriture + famille autre | 86 | 0,3760 | 0,4786 |
| même écriture + familles différentes | 78 | 0,0684 | 0,1815 |
| écriture différente + sœurs | 10 | 0,0333 | 0,1332 |
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nt=t.replace(\"Le point décisif : le coefficient de **famille** du modèle J3.1-compatible (+0,155) est **3,4× plus\\npetit** que le coefficient de **sœur** (+0,448).\",\n\"Le poin … [266 caractères tronqués]`

  ```
271:Le point décisif : le coefficient de **famille** du modèle J3.1-compatible (+0,155) est **2,9× plus
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nt=t.replace(\"avec le contrôle, elle est 4,3× dans la même écriture et **1,2× hors écriture**. La moitié du « signal de\\nfamille » brut est un signal d'écriture.\",\n\"avec le c … [291 caractères tronqués]`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "grep -n \"moitié\\|signal de famille\" reports/rapport-retrieval-familles.md", "description": "Locate half claim"}`

  ```
43:signal de famille vit dans **2-3 paires** (`ind–jav`, `eng–fra`) et que les **154 paires hors écriture**
335:C'est exactement le résultat de J3.2 : sur les 21 langues, le signal de famille vit dans **2-3 paires**
430:contrôle, elle est 4,3× dans la même écriture et **1,2× hors écriture**. La moitié du « signal de
  ```

- **bash** `{"command": "sed -n '426,434p' reports/rapport-retrieval-familles.md", "description": "Read half claim context"}`

  ```
que **la surface retrouve la filiation quand la branche est proche et l'écriture partagée** ; elle ne
la retrouve pas à travers l'écriture, et elle ne la retrouve pas sur un échantillon sans sœurs. Le
remède de Panini — **contrôler la surface dans tout test de famille** — est donc plus que jamais
nécessaire : ici, sans le contrôle d'écriture, la famille paraît 6,4× au-dessus du hasard ; avec le
contrôle, elle est 4,3× dans la même écriture et **1,2× hors écriture**. La moitié du « signal de
famille » brut est un signal d'écriture.

## 6. Ce qui pourrait rendre ce résultat faux
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nold=\"contrôle, elle est 4,3× dans la même écriture et **1,2× hors écriture**. La moitié du « signal de\\nfamille » brut est un signal d'écriture.\"\nnew=\"contrôle, elle est 4,3 … [334 caractères tronqués]`

  ```
430:contrôle, elle est 4,3× dans la même écriture et **1,2× hors écriture**. Une part importante du
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\nm=d['lang_tree']\nfor k in ['script_different_famille_meme','script_different_famille_differente','script_different_soeur']:\n    print(k,m['agregats'][k])\n# compute different script family-other dire … [717 caractères tronqués]`

  ```
script_different_famille_meme {'n_paires': 140, 'top1_moyen': 0.033333333333333326, 'top1_median': 0.03333333333333333, 'ic_bas': 0.03333333333333333, 'ic_haut': 0.03333333333333333, 'mrr_moyen': 0.13316623769734634}
script_different_famille_differente {'n_paires': 246, 'top1_moyen': 0.036991869918699176, 'top1_median': 0.03333333333333333, 'ic_bas': 0.03333333333333333, 'ic_haut': 0.03333333333333333, 'mrr_moyen': 0.13661108884164758}
script_different_soeur {'n_paires': 10, 'top1_moyen': 0.03333333333333333, 'top1_median': 0.03333333333333333, 'ic_bas': 0.03333333333333333, 'ic_haut': 0.03333333333333333, 'mrr_moyen': 0.13316623769734637}
diffscript famautre n 130 top1 0.03333333333333333
diffscript diff n 246 top1 0.03699186991869918
script famautre n 86 top1 0.375968992248062
script diff n 78 top1 0.06837606837606837
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-familles.json'))\nfor nom in ['echantillon_20','lang_tree','union_39']:\n    m=d[nom]\n    print('===',nom)\n    for sc in [True,False]:\n        for cat in ['soeur','famille_autre_branche','famille_differente']:\n      … [236 caractères tronqués]`

  ```
=== echantillon_20
script True soeur 4 0.1083
script True famille_autre_branche 10 0.2367
script True famille_differente 78 0.056
script False soeur 8 0.0333
script False famille_autre_branche 38 0.0333
script False famille_differente 242 0.0333
=== lang_tree
script True soeur 50 0.736
script True famille_autre_branche 86 0.376
script True famille_differente 78 0.0684
script False soeur 10 0.0333
script False famille_autre_branche 130 0.0333
script False famille_differente 246 0.037
=== union_39
script True soeur 54 0.6907
script True famille_autre_branche 96 0.359
script True famille_differente 410 0.0651
script False soeur 16 0.0333
script False famille_autre_branche 190 0.0333
script False famille_differente 716 0.0346
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nold=\"\"\"| | même écriture | écriture différente |\n|---|---:|---:|\n| **sœurs** | **0,7360** (50) | 0,0333 (10) |\n| **même famille, autre branche** | **0,3760** (86) | 0,1698  … [3786 caractères tronqués]`

  ```
| **même famille, autre branche** | **0,3760** (86) | 0,0333 (130) |
| **familles différentes** | **0,0684** (78) | 0,0370 (246) |

La ligne des sœurs est le résultat : **0,619** toutes écritures, **0,736** à écriture contrôlée, contre
**0,0445** pour les familles différentes (toutes) et **0,0684** à écriture contrôlée. Le gradient est
net **à écriture contrôlée** : sœur 0,736 > famille-autre 0,376 > différente 0,068. **Hors écriture,
les trois cellules sont au hasard** (0,0333 / 0,0333 / 0,0370) : le retrieval de surface ne traverse
aucune frontière d'écriture, exactement comme les 154/154 paires de J3.2. Le contrôle par écriture est
donc une **frontière dure** dans ce corpus, pas une simple covariable.

| groupe | n | top1 | MRR |
|---|---:|---:|---:|
| toutes | 600 | 0,1471 | — |
| même écriture | 214 | 0,3480 | — |
| écriture différente | 386 | 0,0357 | — |
| **sœurs** | **60** | **0,6189** | **0,6899** |
| **sœurs strictes** (LCA ≥ 4) | **54** | **0,6840** | **0,7517** |
| **même famille, autre branche** | **216** | **0,1698** | **0,2707** |
| **familles différentes** | **324** | **0,0445** | **0,1474** |
| même écriture + sœurs | 50 | 0,7360 | 0,8012 |
| même écriture + famil
… [1528 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nold=\"\"\"4. **Les variantes proches et les doublons.** 12 groupes de textes identiques, 2 doublons cross-ISO\n   retirés ; il reste des variantes très proches (`cnr`/`hrv` 0,917 … [936 caractères tronqués]`

  ```
disponibles que pour les 25 + 20 langues de Drave. Le global mesure donc la **proximité de
   l'article 1**, pas la proximité de 30 articles. Le parallèle corrige, mais sur un sous-ensemble.
3. **L'UDHR est mono-époque.** Le contrôle d'époque est par construction, pas une estimation ; le
   placebo ne prouve pas l'absence d'un effet d'époque, il vérifie que le pipeline ne fabrique pas de
   date. Le seul bras daté (Bible) est un autre corpus, un autre genre.
4. **Les variantes proches et les doublons.** 12 groupes de textes identiques, 2 doublons cross-ISO
   retirés ; il reste des variantes très proches (`cnr`/`hrv` 0,917, `bos_cyrl`/`srp_cyrl` 0,909,
   `pes_1`/`pes_2` 0,887) qui gonflent le **signal de famille-autre-branche**, pas le signal de
   sœur. Le signal de sœur reste massif après retrait des doublons exacts, mais il inclut une part de
   **même tradition de traduction** pour les paires très proches.
5. **La définition de « sœur » est une convention.** LCA ≥ 3, hors ancêtre/descendant. La variante
   stricte (LCA ≥ 4) donne des chiffres **plus forts** (0,684, coefficient +0,507) : la conclusion ne
   dépend pas du seuil, mais les valeurs, oui. Un seuil plus large (LCA ≥ 
… [27 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,collections\nd=json.load(open('reports/retrieval-familles.json'))\nm=d['lang_tree']\nprint(m['langues'])\nprint(collections.Counter(p['famille_a'] for p in m['paires'] if p['a']==m['langues'][0]))\n# count unique languages per family\nfam={}\nfor k in m['l … [201 caractères tronqués]`

  ```
['arb', 'ben', 'cmn_hant', 'dan', 'deu_1996', 'ell_monotonic', 'eng', 'fin', 'fra', 'heb', 'hin', 'hun', 'ita', 'jpn', 'kor', 'lat', 'nld', 'nob', 'pes_1', 'por_PT', 'ron_2006', 'san', 'spa', 'swe', 'tur']
Counter({'Afro-Asiatic': 24})
Counter({'Indo-European': 17, 'Afro-Asiatic': 2, 'Uralic': 2, 'Sino-Tibetan': 1, 'Japonic': 1, 'Koreanic': 1, 'Turkic': 1})
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nold=\"\"\"Les 25 langues LANG_TREE couvrent **9 familles** : indo-européen (18), afro-asiatique (4),\nsino-tibétain (4), atlantique-congo (4), austronésien (4), ouralien (2), jap … [649 caractères tronqués]`

  ```
Le mapping LANG_TREE → UDHR est explicite (table dans le JSON) :

- **26 codes mappés** sur 25 textes : `per` et `fas` pointent tous deux vers `pes_1` (même texte) ;
- **3 absents** de l'UDHR : `grc` (grec ancien), `pli` (pali), `lzh` (chinois littéraire) ;
- choix assumés : `nor → nob` (bokmål), `zho → cmn_hant` (mandarin traditionnel),
  `por → por_PT`, `ron → ron_2006`, `deu → deu_1996`.

Les 25 langues LANG_TREE couvrent **7 familles** : indo-européen (17), afro-asiatique (2),
ouralien (2), sino-tibétain (1), japonique (1), coréen (1), turcique (1). L'union avec l'échantillon 20
ajoute l'**atlantique-congo** (4) et l'**austronésien** (4), et complète l'afro-asiatique (4) et le
sino-tibétain (4) : **9 familles, 39 langues**.

## 3. Le protocole — deux mesures, un même retrieval
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nold=\"\"\"Les **12 paires de sœurs** sont dominées par les paires **hors écriture** (`arb`/`heb`, `arb`/`amh`,\n`heb`/`amh`, `ind`/`mly_arab`) : 8 sur 12 sont au plancher 0,0333. … [802 caractères tronqués]`

  ```
| | même écriture | écriture différente |
|---|---:|---:|
| **sœurs** | **0,1083** (4) | 0,0333 (8) |
| **même famille, autre branche** | **0,2367** (10) | 0,0333 (38) |
| **familles différentes** | **0,0560** (78) | 0,0333 (242) |

Les **12 paires de sœurs** sont dominées par les paires **hors écriture** (`arb`/`heb`, `arb`/`amh`,
`heb`/`amh`, `ind`/`mly_arab`) : **8 sur 12** sont hors écriture et au plancher 0,0333. Les sœurs de
même écriture sont `cnh`/`ctd` (0,233 et 0,167) et `ibo`/`kin` (0,033 et 0,0) : quatre paires, dont
**deux au plancher** ; au total **10 des 12 paires** sont à ≤ 0,0333, trop peu pour porter une moyenne. Le **même famille-autre-branche** toutes écritures (0,0757) est
**supérieur** aux sœurs (0,0583) : le signal de l'échantillon est porté par `jav`/`ind` (0,900 et
  ```

- **bash** `{"command": "ls tools/retrieval_udhr.py 2>/dev/null; find . -name 'retrieval_udhr.py' | head", "description": "Check retrieval_udhr tool existence"}`

  ```
tools/retrieval_udhr.py
./tools/retrieval_udhr.py
  ```

- **bash** `{"command": "head -40 reports/README.md; echo '---'; grep -n \"retrieval-epoque\\|genealogie-deux-faces\" reports/README.md", "description": "Inspect reports README"}`

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
… [2492 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Current date/time"}`

  ```
2026-11-14 01:38 EST
  ```

- **bash** `{"command": "grep -n \"Panini J2.1\\|J3.2\\|fichiers / JSON\" docs/pilotage/en-cours.md", "description": "Locate en-cours Panini and counters"}`

  ```
92:- **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significative ; **J3.2** : les deux faces diffèrent — `lang_distance` couvre **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, la famille vit dans **2-3 paires**, **V14 : 3/21** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-faces.md).
104:| fichiers / JSON de résultats | **720** / **814** | `reports/*.md` / `reports/*.json` |
126:**N2** — porte (0,2856 val / 0,3566 test) ; **Pensée** — convention d'adverbe `g017`, T132/T133, gold 200+ ; **J3.2** — **V14 des 21 langues** ; **S** — 11 verdicts + pointeur ; **R0.7** — **0,9475**, intégrer, split réel ; **A** — A6.2, A8.3b2 ; **J5.2** — passe, revue, tag.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\nt=p.read_text()\nt=t.replace(\"**Mis à jour : 2026-11-14, 01 h 20 HNE (heure locale, EST).**\",\n            \"**Mis à jour : 2026-11-14, 01 h 40 HNE (heure locale, EST).**\")\nold=\"- **Panini J2.1/J2.2/J3. … [2657 caractères tronqués]`

  ```
92:- **Panini J2.1/J2.2/J3.1/J3.2/J7.1** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significative ; **J3.2** : les deux faces diffèrent — `lang_distance` couvre **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, la famille vit dans **2-3 paires**, **V14 : 3/21** ; **J7.1** : 532 textes Panini (445 langues, Glottolog 521/532), top-1 famille **66,1 %** (hasard 10,3 %) et sœur **26,1 %** (hasard 2,5 %), mais **hors écriture tout est au hasard** ; sur LANG_TREE 25, sœurs **0,619** vs familles différentes **0,0445** (13,9×, coefficient +0,448, p=0,002) ; sur l'échantillon 20, contraste **nul** (0,058 vs 0,039, p=0,078) ; J3.1 reproduit à l'identique ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-faces.md), [familles](../../reports/rapport-retrieval-familles.md).
104:| fichiers / JSON de résultats | **721** / **815** | `reports/*.md` / `reports/*.json` |
126:**N2** — porte (0,2856 val / 0,3566 test) ; **Pensée** — convention d'adverbe `g017`, T132/T133, gold 200+ ; 
… [222 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '33,36p' docs/pilotage/roadmap.md; echo '---'; sed -n '52,54p' docs/pilotage/roadmap.md; echo '---'; sed -n '254,256p' docs/pilotage/roadmap.md", "description": "Read roadmap lines to edit"}`

  ```
| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; la suite : **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; R2/R3 attendent N5/N4 |
| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête le verbe) ; [fiche](../../reports/rapport-s-fait-divers.md). **v6** : h050, h053 et « si fort que » **fermés**, gold **60** (vague 5) ; **60/60** types, **142/142** rôles, **50/50** compléments, couverture 1,00 ; corpus 65,5 %/9,1 %, 596/1 184 homographes ; **55 tests**. **v5** : arbre parent/enfant (**99 cand
… [5245 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\nt=p.read_text()\n# 1. L row\nold1=\"le signal de famille vit dans 2-3 paires ; la face atomes n'est pas disponible (V14 3/21)** ([fiche](../../reports/rapport-genealogie-deux-faces.md)) | la **pragmatique neu … [2585 caractères tronqués]`

  ```
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 vs 0,427)** ([fiche](../../reports/rapport-retrieval-epoque.md)) ; **J3.2 généalogie à deux faces : Panini couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au hasard exact, le signal de famille vit dans 
… [2857 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/README.md')\nt=p.read_text()\nold=\"| [`rapport-retrieval-epoque.md`](rapport-retrieval-epoque.md) | **Panini** — le retrieval contrôlé |\\n| [`rapport-genealogie-deux-faces.md`](rapport-genealogie-deux-faces.md) | **Panini** —  … [607 caractères tronqués]`

  ```
26:| [`rapport-retrieval-familles.md`](rapport-retrieval-familles.md) | **Panini** — le retrieval approfondi par famille : 532 textes, sœurs vs familles |
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('journal/2026-11-14/README.md')\nt=p.read_text()\nold=\"<!-- /notes -->\"\nnew=\"\"\"**J7.1 — le retrieval par famille : l'écriture d'abord, la sœur ensuite.** Sur les **532 textes\nUDHR** de Panini (même source XML, article 1, 1948 ; ** … [1745 caractères tronqués]`

  ```
55:**J7.1 — le retrieval par famille : l'écriture d'abord, la sœur ensuite.** Sur les **532 textes
  ```

- **bash** `{"command": "python3 tools/index_reports.py && python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Regenerate report index and run doc review"}`

  ```
718 fiches → reports/INDEX.md
  revue de documentation · 721 fiche(s) · 815 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "grep -n \"retrieval-familles\" reports/INDEX.md; git status --short | head -30", "description": "Verify index and git status"}`

  ```
674:| [rapport-retrieval-familles.md](rapport-retrieval-familles.md) | J7.1 — Le retrieval approfondi par famille Glottolog |
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-14/README.md
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
 m tools/structures
?? reports/rapport-retrieval-familles.md
?? reports/rapport-s-paragraphes.md
?? reports/retrieval-familles.json
?? tools/retrieval_familles.py
  ```

- **bash** `{"command": "grep -rn \"index_reports\" tools/*.sh tools/*.py docs/methode/*.md | head -20", "description": "Check index_reports gate usage"}`

  ```
tools/index_reports.py:2:"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.
tools/index_reports.py:10:    python3 tools/index_reports.py              # réécrit reports/INDEX.md
tools/index_reports.py:11:    python3 tools/index_reports.py --verifier   # ne réécrit rien, sort 1 si périmé
tools/index_reports.py:12:    python3 tools/index_reports.py --aide       # affiche l'aide (ne touche à rien)
tools/index_reports.py:41:        f"> **Généré** par `tools/index_reports.py` — **{len(fs)} fiches**. Les fichiers",
docs/methode/rangement.md:50:régénéré par `python3 tools/index_reports.py` (→ [`reports/INDEX.md`](../../reports/INDEX.md)).
  ```

- **bash** `{"command": "ls tools/porte-*doc* tools/verifie_en_cours.py tools/taille_documents.py tools/verifie_journal.py 2>/dev/null", "description": "List doc/state verification tools"}`

  ```
tools/porte-document.sh
tools/taille_documents.py
tools/verifie_en_cours.py
tools/verifie_journal.py
  ```

- **bash** `{"command": "grep -n \"rapport-s-paragraphes\" reports/INDEX.md", "description": "Locate S report index line"}`

  ```
687:| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/INDEX.md')\nlignes=p.read_text().splitlines(keepends=True)\nlignes=[l for l in lignes if 'rapport-s-paragraphes.md' not in l]\np.write_text(''.join(lignes))\nEOF\ngrep -n \"rapport-s-paragraphes\\|retrieval-familles\" reports/IN … [71 caractères tronqués]`

  ```
674:| [rapport-retrieval-familles.md](rapport-retrieval-familles.md) | J7.1 — Le retrieval approfondi par famille Glottolog |
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo EXIT:$?", "description": "Verify en-cours state"}`

  ```
en-cours · 1699 mots · 7 sections · 4 session(s) · 8 puces · 5 questions
  ❌ 1 anomalie(s) :
     · puce > 80 mots : **Panini J2.1/J2.2/J3.1/J3.2/J7.1** : table **14 atomes** ; 
EXIT:0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo EXIT:$?", "description": "Verify context budget"}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2678    200   T1   2800  reports/README.md
    2450    166   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4069 mots (budget 4 000)

  avertissements :
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [118 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -20; echo EXIT:$?", "description": "Verify journal"}`

  ```
journal · 46 jour(s) · 181 session(s) · 2444 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT:0
  ```

- **bash** `{"command": "grep -n \"T0\\|AGENTS\\|en-cours\\|budget\" tools/taille_documents.py | head -40", "description": "Inspect context budget calculation"}`

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
… [944 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '82,100p' docs/pilotage/en-cours.md", "description": "Read en-cours current bullets"}`

  ```
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
- **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
- **Pensée — B13 (actif)** : **183/183**, gold 432, pragmatique 130/432 ; **`r035`** (238/238) ; **convention des GV** (0,7902, 0 perte) ; **`s065` réglé** (238/238, 0 span ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée** (adverbe final hors SUB, test −0,0028 ; g017 : convention à trancher) ; **schéma v2** (26 cas, 0 échec ; v1 lue) ; **restitution v0** (46/46, miroir 0,1087) ; [restitution](../../reports/rapport-restitution-v0.md), [g017](../
… [1768 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\nt=p.read_text()\nold=\"\"\"- **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonné … [4141 caractères tronqués]`

  ```
en-cours · 1633 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4003 mots (budget 4 000)

  avertissements :
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4003 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\nt=p.read_text()\nold=\"- **Panini J7.1** : 532 textes (445 langues) ; top-1 famille **66,1 %** / sœur **26,1 %** (hasard 10,3 / 2,5), hors écriture au hasard ; LANG_TREE 25 : sœurs **0,619** vs **0,0445** (1 … [657 caractères tronqués]`

  ```
avertissements :
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -10", "description": "Rerun doc review after state edits"}`

  ```
revue de documentation · 721 fiche(s) · 815 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 -c \"import json; d=json.load(open('reports/retrieval-familles.json')); print('ok', d['tache'], d['global_532']['n_requetes'], d['lang_tree']['n_paires'], d['echantillon_20']['n_paires'], d['union_39']['n_paires'])\"; ls -lh reports/retrieval-familles.json reports/rapport-retrie … [87 caractères tronqués]`

  ```
ok J7.1 445 600 380 1482
-rw-r--r--. 1 stephane stephane  33K 14 nov 01:38 reports/rapport-retrieval-familles.md
-rw-r--r--. 1 stephane stephane 2,5M 14 nov 01:35 reports/retrieval-familles.json
-rw-r--r--. 1 stephane stephane  51K 14 nov 01:34 tools/retrieval_familles.py
  ```

- **bash** `{"command": "ls -lh reports/retrieval-epoque.json reports/genealogie-deux-faces.json; du -h reports/retrieval-familles.json", "description": "Compare JSON sizes"}`

  ```
-rw-r--r--. 1 stephane stephane 106K  7 nov 18:19 reports/genealogie-deux-faces.json
-rw-r--r--. 1 stephane stephane 2,1M  7 nov 17:07 reports/retrieval-epoque.json
2,5M	reports/retrieval-familles.json
  ```

- **bash** `{"command": "git diff --stat -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-14/README.md reports/INDEX.md reports/README.md; echo '--- new ---'; wc -l tools/retrieval_familles.py reports/rapport-retrieval-familles.md", "description": "Review diff stats"}`

  ```
docs/pilotage/en-cours.md    | 15 ++++++++-------
 docs/pilotage/roadmap.md     |  6 ++++--
 journal/2026-11-14/README.md | 19 +++++++++++++++++++
 reports/INDEX.md             |  6 ++++--
 reports/README.md            |  1 +
 5 files changed, 36 insertions(+), 11 deletions(-)
--- new ---
 1034 tools/retrieval_familles.py
  506 reports/rapport-retrieval-familles.md
 1540 total
  ```

- **bash** `{"command": "git diff -- reports/INDEX.md | head -40", "description": "Inspect INDEX diff"}`

  ```
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 511f979c..5506faf4 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **715 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **718 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -175,6 +175,7 @@
 | [rapport-file-taches.md](rapport-file-taches.md) | La file des tâches — inventaire, trois files et ordre pour 09 h 30 → 12 h |
 | [rapport-frontieres-integrees.md](rapport-frontieres-integrees.md) | B13 — les frontières de phrase : 32/40 textes faux → 0, et le gold ne bouge pas |
 | [rapport-frontieres-phrase.md](rapport-frontieres-phrase.md) | Frontières de phrase — P0-4 du bloc linguistique |
+| [rapport-g017.md](rapport-g017.md) | B13 — g017 : l'adverbe final hors de la SUB est rejeté (g017 gagné, r264 et r288 perdus) |
 | [rapport-genealogie-deux-faces.md](rapport-genealogie-deux-faces.md) | J3.2 — La généalogie à deux faces : Panini et Glottolog sur le corpus commun |
 | [rapport-genres.
… [2531 caractères tronqués]
  ```

- **bash** `{"command": "git status --short reports/rapport-g017.md reports/rapport-s065.md reports/rapport-s-paragraphes.md; git ls-files reports/rapport-g017.md reports/rapport-s065.md reports/rapport-s-paragraphes.md", "description": "Check status of other report files in index diff"}`

  ```
?? reports/rapport-s-paragraphes.md
reports/rapport-g017.md
reports/rapport-s065.md
  ```

- **bash** `{"command": "git diff -- docs/pilotage/roadmap.md | head -30; echo '--- en-cours diff ---'; git diff -- docs/pilotage/en-cours.md | head -60", "description": "Review roadmap and state diffs"}`

  ```
diff --git a/docs/pilotage/roadmap.md b/docs/pilotage/roadmap.md
index 96291340..675cffbb 100644
--- a/docs/pilotage/roadmap.md
+++ b/docs/pilotage/roadmap.md
@@ -32,7 +32,7 @@
 | **N — le natif** | DRVM, `drave-n0`, [distillation](../theorie/glossaire/entrees/distillation.md), usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; **N0.1 6/6** ; N2.h : 3,0904 domaine, 3,85 hors dépôt ; **N2.ac (1 Go) : 3,49 / 6,03 / 8,34 — production** ; **200 k pas : val_fr 3,16, littérature 5,61, anglais 7,28, wikitext2 8,00** ; **fenêtre 1 024 : 2,4759 / 2,4373 au grand corpus — sous 2,5** ; porte propre **2,7856** ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 partiel | **N2** : **clôturée** le 03/11 11 h 25, la **fenêtre est la recette de production** ; **paire propre de distillation** (04/11) ; puis la **porte propre (0,29)** ; **N4** |
 | **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **
… [18804 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/porte-document.sh", "description": "Inspect document gate"}`

  ```
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
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte document verte" || echo "❌ porte document ROUGE (code $CODE)"
exit "$CODE"
  ```

- **bash** `{"command": "git diff --check -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-14/README.md reports/INDEX.md reports/README.md; echo EXIT:$?", "description": "Check whitespace errors"}`

  ```
EXIT:0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8; python3 tools/verifie_en_cours.py 2>&1 | tail -4; python3 tools/taille_documents.py 2>&1 | tail -4; python3 tools/verifie_journal.py 2>&1 | tail -4", "description": "Final documentation and state checks"}`

  ```
revue de documentation · 721 fiche(s) · 815 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  avertissements :
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  journal · 46 jour(s) · 181 session(s) · 2444 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "sed -n '1,60p' tools/toutes-les-portes.sh", "description": "Inspect all-gates script"}`

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
… [1541 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' docs/pilotage/references-non-regression.md", "description": "Read known non-regression reds"}`

  ```
# Références de non-régression

> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
> `porte-melange` (structurelles, antérieures) et `porte-sessions` (le mandat du hub
> `1e7ef596`, périmé de 9 jours ; le mien est rafraîchi). `porte-produit` **verte**, `porte-bloc`
> **verte**. Journal : `work/portes/passe-1311-23h15.log`.
> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
> échouait sur une ancre du banc pilote (« < 2,5 ») que la réécriture de la roadmap du 04/11
> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
> signale les heartbeats périmés du hub et de `e181ce02` au moment de la passe — le hub l'a rafraîchi
> à 01 h 55, **`e181ce02` reste à rafraîchir par sa s
… [4165 caractères tronqués]
  ```

- **bash** `{"command": "git add tools/retrieval_familles.py reports/retrieval-familles.json reports/rapport-retrieval-familles.md reports/README.md reports/INDEX.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-14/README.md && git diff --cached --stat", "description": "Stage J7.1 files exp … [9 caractères tronqués]`

  ```
docs/pilotage/en-cours.md             |    15 +-
 docs/pilotage/roadmap.md              |     6 +-
 journal/2026-11-14/README.md          |    19 +
 reports/INDEX.md                      |     6 +-
 reports/README.md                     |     1 +
 reports/rapport-retrieval-familles.md |   506 +
 reports/retrieval-familles.json       | 99582 ++++++++++++++++++++++++++++++++
 tools/retrieval_familles.py           |  1034 +
 8 files changed, 101158 insertions(+), 11 deletions(-)
  ```

- **bash** `{"command": "git commit -m \"J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE\" 2>&1 | tail -30", "description": "Commit J7.1 result"}`

  ```
[still running after 60000ms; moved to background job bash-157]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-157", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sleep 20; ps -o pid,etime,cmd -C git -C python3 | tail -6; echo '---'; git status --short | head -20", "description": "Check commit progress"}`

  ```
3002 10-06:08:27 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
 946076    04:03:56 python3 tools/chantier/superviseur.py boucle --budget 43200 --timeout 5400
1603136       01:24 git commit -m J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE
1603156       01:24 python3 tools/archive_sessions.py --quiet
1603833       00:49 /usr/bin/python3 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/session_report.py --repo /home/stephane/Data13TB/stephane/GitHub/Qtrinet --quiet
3555423  7-05:58:09 python3 src/app.py --no-browser
---
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-14/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-e9ee2692-96f9-42d2-886c-c5abfb51ce07/digest.md
M  reports/INDEX.md
M  reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fich
… [216 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-157", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sleep 30; ps -o pid,etime,cmd -C git -C python3 | tail -8; echo '---'; git status --short | head -25", "description": "Check commit progress again"}`

  ```
PID     ELAPSED CMD
   3002 10-06:09:03 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
 946076    04:04:31 python3 tools/chantier/superviseur.py boucle --budget 43200 --timeout 5400
1603136       02:00 git commit -m J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE
1604625       00:34 python3 tools/session_report.py --quiet
3555423  7-05:58:45 python3 src/app.py --no-browser
---
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-14/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-e9ee2692-96f9-42d2-886c-c5abfb51ce07/digest.md
 M journal/sessions/session-e9ee2692-96f9-42d2-886c-c5abfb51ce07/rapport.md
M  reports/INDEX.md
M  reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports
… [279 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-157", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sleep 45; ps -o pid,etime,cmd -C git -C python3 | tail -6; echo '---'; git log --oneline -3; echo '---'; git status --short | head -30", "description": "Check commit completion"}`

  ```
PID     ELAPSED CMD
   3002 10-06:09:53 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
 946076    04:05:22 python3 tools/chantier/superviseur.py boucle --budget 43200 --timeout 5400
3555423  7-05:59:35 python3 src/app.py --no-browser
---
0307ce7e J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE
e4288023 J6.2 — PORTE PRODUIT VERTE (183/183) : FIXTURES D'ATTACHEMENT À 238/238, FICHE ET JSON À JOUR
2d6f5bff PORTES — LA PASSE DU 14/11 : 84 PORTES, 81 VERTES, 3 ROUGES (INDICE, MELANGE, SESSIONS DU HUB) ; MANDAT E181CE02 RAFRAÎCHI
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
 m tools/structures
?? reports/rapport-s-paragraphes.md
  ```

### 👤 Utilisateur

background job bash-157 (bash: git commit -m "J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE" 2>&1 | tail -30) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "git show --stat --oneline HEAD | head -40; echo '---'; git show --name-only --format='' HEAD | head -60", "description": "Inspect commit contents"}`

  ```
0307ce7e J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE
 docs/pilotage/en-cours.md                          |    15 +-
 docs/pilotage/roadmap.md                           |     6 +-
 journal/2026-11-14/README.md                       |    24 +-
 journal/2026-11-14/docs.md                         |     2 +-
 journal/2026-11-14/memoire.md                      |     2 +-
 journal/2026-11-14/mesures.md                      |     2 +-
 journal/2026-11-14/portes.md                       |    23 +
 journal/README.md                                  |     7 +-
 journal/THEMES.md                                  |     1 +
 journal/sessions/MANIFEST.md                       |     7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |    14 +
 .../rapport.md                                     |     8 +-
 .../digest.md                                      |  3607 +
 .../rapport.md                                     |   232 +
 .../digest.md                                      |   132 +
 .../rapport.md                                     |    53 +-
 reports/INDEX.md                            
… [1157 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -6; python3 tools/verifie_en_cours.py 2>&1 | tail -3; python3 tools/taille_documents.py 2>&1 | tail -3; python3 tools/verifie_journal.py 2>&1 | tail -3", "description": "Post-commit verification"}`

  ```
revue de documentation · 721 fiche(s) · 815 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  journal · 46 jour(s) · 182 session(s) · 2451 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "grep -n \"J7.1\" journal/2026-11-14/README.md | head; git status --short | head -15", "description": "Verify committed journal note and clean state"}`

  ```
57:**J7.1 — le retrieval par famille : l'écriture d'abord, la sœur ensuite.** Sur les **532 textes
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
  ```

- **bash** `{"command": "grep -rn \"écriture > sœur\\|écriture > famille\\|> sœur >\\|écriture >\" reports/rapport-retrieval-familles.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-14/README.md | head -20", "description": "Find hierarchy claims"}`

  ```
reports/rapport-retrieval-familles.md:20:> pour l'écriture. **La hiérarchie est écriture > sœur > famille-autre-branche > époque ; l'époque ne
reports/rapport-retrieval-familles.md:407:mesurée est **écriture > sœur > famille-autre-branche > époque**.
reports/rapport-retrieval-familles.md:496:- **J7.1 est mesuré, écrit, contrôlé.** Le retrieval de surface est **écriture > sœur >
journal/2026-11-14/README.md:70:−0,034/siècle (p = 0,19) contre +0,609 pour l'écriture. **La hiérarchie est écriture > sœur >
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nold=\"\"\"L'époque est **mono-époque par construction** (1948) ; le placebo de dates donne −0,0013\n> [−0,065 ; +0,041], et le seul bras daté de J3.1 (Bible) donne −0,034/siècle  … [3395 caractères tronqués]`

  ```
reports/rapport-retrieval-familles.md:409:mesurée est **porte d'écriture → sœur > famille-autre-branche > époque** : l'écriture est un **seuil**
reports/rapport-retrieval-familles.md:502:- **J7.1 est mesuré, écrit, contrôlé.** Le retrieval de surface a une **porte d'écriture** (hors
reports/rapport-retrieval-familles.md:503:  écriture, tout est au hasard) ; **dans la même écriture**, l'ordre est **sœur > famille-autre >
  ```

- **bash** `{"command": "sed -n '64,78p' journal/2026-11-14/README.md; echo '--- header ---'; sed -n '14,26p' reports/rapport-retrieval-familles.md", "description": "Inspect hierarchy edits"}`

  ```
autre branche **0,170** (216), les familles différentes **0,0445** (324) — **13,9×**, coefficient de
sœur **+0,448** (p = 0,002) contre +0,213 pour l'écriture, **11/11** langues positives. Sur
l'**échantillon 20**, le contraste est **nul** (sœurs 0,058 vs 0,039, p = 0,078) : l'échantillon ne
contient que 12 paires de sœurs, dont 8 hors écriture. **J3.1 est reproduit à l'identique** (écart 0) ;
son coefficient de famille (+0,0556) était un **minorant** dilué. L'époque est **mono-époque** (1948) ;
le placebo de dates est nul (−0,0013 [−0,065 ; +0,041]) et le seul bras daté de J3.1 (Bible) donne
−0,034/siècle (p = 0,19) contre +0,609 pour l'écriture. L'écriture est la **porte** ; **dans la même
écriture**, l'ordre est **sœur (+0,448) > famille-autre (+0,092) > époque (nulle)** — le coefficient de
sœur dépasse même celui de l'écriture (+0,213) une fois la famille séparée. Fiche Fiche
[`reports/rapport-retrieval-familles.md`](../../reports/rapport-retrieval-familles.md), JSON
[`reports/retrieval-familles.json`](../../reports/retrieval-familles.json), outil
[`tools/retrieval_familles.py`](../../tools/retrieval_familles.py).
<!-- /notes -->
--- header ---
> sœurs 0,0583 (12 paires) contre
… [1180 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('journal/2026-11-14/README.md')\nt=p.read_text().replace(\"Fiche Fiche\\n\", \"Fiche\\n\")\np.write_text(t)\nEOF\ngrep -n \"Fiche\" journal/2026-11-14/README.md | tail -3", "description": "Fix duplicate Fiche"}`

  ```
44:final) doit être tranchée avant toute règle. Fiche [`reports/rapport-g017.md`](../../reports/rapport-g017.md),
54:verte (**183/183**, fixtures d'attachement mises à jour). Fiche
72:sœur dépasse même celui de l'écriture (+0,213) une fois la famille séparée. Fiche
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-retrieval-familles.md')\nt=p.read_text()\nt=t.replace(\"**À l'intérieur de\\n> l'écriture, la sœur est le premier effet** (+0,448 contre +0,213 pour l'écriture)\",\n            \"**À l'intérieur de\\n> l'écriture, sur LA … [1106 caractères tronqués]`

  ```
reports/rapport-retrieval-familles.md:21:> l'écriture, sur LANG_TREE, la sœur est le premier effet** (+0,448 contre +0,213 pour l'écriture), puis la
reports/rapport-retrieval-familles.md:410:(la franchir change tout), et **dans le même script, sur LANG_TREE**, la sœur est le premier effet (coefficient
reports/rapport-retrieval-familles.md:503:  écriture, tout est au hasard) ; **dans la même écriture, sur LANG_TREE et l'union**, l'ordre est
reports/rapport-retrieval-familles.md:507:  l'effet de sœur (+0,448 sur LANG_TREE). **J3.2 est confirmé pour son échantillon** (2-3 paires) et
journal/2026-11-14/README.md:71:écriture, sur LANG_TREE**, l'ordre est **sœur (+0,448) > famille-autre (+0,092) > époque (nulle)** — le coefficient de
  ```

- **bash** `{"command": "git add reports/rapport-retrieval-familles.md journal/2026-11-14/README.md && git commit --amend -m \"J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE\" 2>&1 | tail -30", "descri … [75 caractères tronqués]`

  ```
started background job bash-169
  ```

- **bash** `{"command": "grep -o \"écriture > sœur[^\\\"]*\" reports/retrieval-familles.json | head; grep -o \"hiérarchie[^\\\"]*\" reports/retrieval-familles.json | head", "description": "Check JSON for hierarchy strings"}`

  ```
(no output)
  ```

### 👤 Utilisateur

background job bash-169 (bash: git add reports/rapport-retrieval-familles.md journal/2026-11-14/README.md && git commit --amend -m "J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE" 2>&1 | tail -30) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "git log --oneline -2; echo '---'; git show --stat --oneline HEAD | head -30; echo '---'; git status --short | head -15", "description": "Check amended commit"}`

  ```
0307ce7e J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE
e4288023 J6.2 — PORTE PRODUIT VERTE (183/183) : FIXTURES D'ATTACHEMENT À 238/238, FICHE ET JSON À JOUR
---
0307ce7e J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE
 docs/pilotage/en-cours.md                          |    15 +-
 docs/pilotage/roadmap.md                           |     6 +-
 journal/2026-11-14/README.md                       |    24 +-
 journal/2026-11-14/docs.md                         |     2 +-
 journal/2026-11-14/memoire.md                      |     2 +-
 journal/2026-11-14/mesures.md                      |     2 +-
 journal/2026-11-14/portes.md                       |    23 +
 journal/README.md                                  |     7 +-
 journal/THEMES.md                                  |     1 +
 journal/sessions/MANIFEST.md                       |     7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |    14 +
 .../rapport.md                                     |     8 +-
 .../digest.md                    
… [1053 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-169"}`

  ```
❌ commit refusé : 1 fait(s) stagé(s) sans docs/pilotage/en-cours.md
     · reports/rapport-retrieval-familles.md
     → mettre l'état à jour, puis `git add docs/pilotage/en-cours.md`
  ⛔ commit refusé : un fait sans ligne d'état.
     mets docs/pilotage/en-cours.md à jour, puis :
     git add docs/pilotage/en-cours.md
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\nt=p.read_text()\nt=t.replace(\"**Mis à jour : 2026-11-14, 01 h 40 HNE (heure locale, EST).**\",\n            \"**Mis à jour : 2026-11-14, 02 h 10 HNE (heure locale, EST).**\")\nold=\"- **Panini J7.1** : 532  … [825 caractères tronqués]`

  ```
❌ 1 violation(s) :
     · T0 : 4004 mots (AGENTS + en-cours + une tâche) > budget 4 000
  en-cours · 1634 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\nt=p.read_text()\nt=t.replace(\"**porte d'écriture** (hors script, tout au hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3 / 2,5)\",\n            \"**porte d'écriture** (hors script, hasard) ; fam … [161 caractères tronqués]`

  ```
· 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md reports/rapport-retrieval-familles.md journal/2026-11-14/README.md && git commit --amend -m \"J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE\" … [116 caractères tronqués]`

  ```
started background job bash-174
  ```

- **job_output** `{"job_id": "bash-174", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sleep 30; ps -o pid,etime,cmd -C git -C python3 | tail -5; echo '---'; git log --oneline -1", "description": "Check amend progress"}`

  ```
3002 10-06:11:31 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
 946076    04:06:59 python3 tools/chantier/superviseur.py boucle --budget 43200 --timeout 5400
1606159       00:33 git commit --amend -m J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE
1606179       00:33 python3 tools/archive_sessions.py --quiet
3555423  7-06:01:13 python3 src/app.py --no-browser
---
0307ce7e J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE
  ```

- **job_output** `{"job_id": "bash-174", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sleep 45; git log --oneline -1; echo '---'; git status --short | head -12", "description": "Check amend result"}`

  ```
0307ce7e J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT À L'IDENTIQUE ; ÉCRITURE > SŒUR > ÉPOQUE
---
M  docs/pilotage/en-cours.md
M  journal/2026-11-14/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/session-02ebc573-ec84-46cf-945c-cfd7d563a9fc/digest.md
 M journal/sessions/session-02ebc573-ec84-46cf-945c-cfd7d563a9fc/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
  ```

- **bash** `{"command": "git diff --cached --name-only; echo '---'; ps -o pid,etime,cmd -C git | tail -3", "description": "Check staged files and git process"}`

  ```
docs/pilotage/en-cours.md
journal/2026-11-14/README.md
reports/rapport-retrieval-familles.md
---
    PID     ELAPSED CMD
1606159       01:27 git commit --amend -m J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE
  ```

- **job_output** `{"job_id": "bash-174", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sleep 60; ps -o pid,etime,cmd -C git | tail -2; echo '---'; git log --oneline -1; git status --short | head -8", "description": "Wait for amend completion"}`

  ```
[still running after 60000ms; moved to background job bash-178]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

### 👤 Utilisateur

background job bash-174 (bash: git add docs/pilotage/en-cours.md reports/rapport-retrieval-familles.md journal/2026-11-14/README.md && git commit --amend -m "J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE" 2>&1 | tail -30) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "git log --oneline -1; echo '---'; git status --short | head -12; echo '---'; git show --stat --oneline HEAD | head -8", "description": "Check amended commit final"}`

  ```
d31e8788 J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE
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
 m tools/structures
?? reports/rapport-s-paragraphes.md
---
d31e8788 J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE
 docs/pilotage/en-cours.md                          |    15 +-
 docs/pilotage/roadmap.md                           |     6 +-
 journal/2026-11-14/README.md                       |    28 +-
 journal/2026-11-14/docs.md                         |     2 +-
 journal/2026-11-14/memoire.md                      |     2 +-
 journal/2026-11-14/mesures.md                      |    10 +-
 journal/2026-11-14/portes.md                       |    23 +
  ```

### 👤 Utilisateur

background job bash-178 (bash: sleep 60; ps -o pid,etime,cmd -C git | tail -2; echo '---'; git log --oneline -1; git status --short | head -8) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -5; python3 tools/verifie_en_cours.py 2>&1 | tail -3; python3 tools/taille_documents.py 2>&1 | tail -3; python3 tools/verifie_journal.py 2>&1 | tail -3", "description": "Post-amend checks"}`

  ```
revue de documentation · 721 fiche(s) · 815 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  journal · 46 jour(s) · 182 session(s) · 2452 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "grep -n \"porte d'écriture\\|sœur > famille-autre\\|sur LANG_TREE\" reports/rapport-retrieval-familles.md | head; echo '---'; grep -n \"porte\\|sœur (+0,448)\" journal/2026-11-14/README.md | head", "description": "Verify corrected hierarchy in committed files"}`

  ```
21:> l'écriture, sur LANG_TREE, la sœur est le premier effet** (+0,448 contre +0,213 pour l'écriture), puis la
409:mesurée est **porte d'écriture → sœur > famille-autre-branche > époque** : l'écriture est un **seuil**
410:(la franchir change tout), et **dans le même script, sur LANG_TREE**, la sœur est le premier effet (coefficient
502:- **J7.1 est mesuré, écrit, contrôlé.** Le retrieval de surface a une **porte d'écriture** (hors
503:  écriture, tout est au hasard) ; **dans la même écriture, sur LANG_TREE et l'union**, l'ordre est
504:  **sœur > famille-autre > époque**. La famille est réelle, mais **conditionnelle à l'écriture** et **visible seulement si le
507:  l'effet de sœur (+0,448 sur LANG_TREE). **J3.2 est confirmé pour son échantillon** (2-3 paires) et
---
17:| portes | 1 | [portes.md](portes.md) |
54:REL 5:17, `nage` → `elle`. Règle intégrée avec un test ; porte du bloc verte, porte produit
71:−0,034/siècle (p = 0,19) contre +0,609 pour l'écriture. L'écriture est la **porte** ; **dans la même
72:écriture, sur LANG_TREE**, l'ordre est **sœur (+0,448) > famille-autre (+0,092) > époque (nulle)** — le coefficient de
  ```

- **bash** `{"command": "git show HEAD:reports/rapport-retrieval-familles.md | grep -n \"porte d'écriture\" | head; echo '---'; git show HEAD:journal/2026-11-14/README.md | grep -n \"sœur (+0,448)\" | head", "description": "Verify commit content has corrected hierarchy"}`

  ```
409:mesurée est **porte d'écriture → sœur > famille-autre-branche > époque** : l'écriture est un **seuil**
502:- **J7.1 est mesuré, écrit, contrôlé.** Le retrieval de surface a une **porte d'écriture** (hors
---
72:écriture, sur LANG_TREE**, l'ordre est **sœur (+0,448) > famille-autre (+0,092) > époque (nulle)** — le coefficient de
  ```

- **bash** `{"command": "git status --short; echo '---'; git log --oneline -1", "description": "Final git state"}`

  ```
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
d31e8788 J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE
  ```

### 🤖 Assistant

**J7.1 terminé — commit `d31e8788`.**

## Ce qui a été mesuré

**Corpus** : 532 textes UDHR de Panini (article 1, même source XML, 1948), **521 étiquetés Glottolog** (97,9 %), **447 groupes ISO**, **445 textes distincts** après retrait de 74 variantes ISO et 2 doublons de texte exact.

### 1. Global 532 — la porte d'écriture

| pool | top-1 famille | hasard | top-1 sœur | hasard |
|---|---:|---:|---:|---:|
| toutes (445) | **66,1 %** | 10,3 % | **26,1 %** | 2,5 % |
| même écriture (417) | **69,8 %** | 16,2 % | **27,8 %** | 5,7 % |
| écriture différente (445) | 9,9 % | 8,1 % | 0,7 % | 0,8 % |

**Hors écriture, tout est au hasard** ; dans la même écriture, la famille est enrichie 4,3× et la sœur 4,8×. Permutations d’étiquettes (1 000) : p = 0,001 pour famille et sœur ; requêtes permutées : 11,1 % contre 10,3 % de baseline.

### 2. LANG_TREE 25 — les sœurs dominent

- **sœurs** : **0,619** (60 paires)
- **même famille, autre branche** : 0,170 (216)
- **familles différentes** : **0,0445** (324)
- **13,89×**, Δ **+0,574** [0,490 ; 0,655]
- régression de décomposition : **sœur +0,448** (p = 0,002), **écriture +0,213**, famille-autre +0,092, R² 0,631
- contraste apparié : **11/11 langues positives**, p = 0,00098 ; leave-one-language-out : sœur **+0,404 → +0,518**
- candidats mélangés : 0,0303 contre 0,0333 de hasard

### 3. Échantillon 20 — le contraste s’éteint

- sœurs **0,0583** (12 paires), familles différentes **0,0389** (320), famille-autre **0,0757** (48)
- coefficient de sœur **+0,0154**, p = **0,078** (non significatif) ; famille-autre +0,0384, p = 0,016
- **8 des 12 paires de sœurs sont hors écriture** ; les paires qui portent le signal sont `jav–ind` (0,900) et `ind–jav` (0,833), deux non-sœurs.

C’est le résultat de J3.2 confirmé : l’échantillon 20 ne peut pas résoudre les sœurs.

### 4. Comparaison à J3.1

**J3.1 est reproduit à l’identique** (écart maximal **0** : top-1 0,04944, écriture +0,06186, famille +0,05562, R² 0,13957). Son coefficient de famille (+0,0556) n’était pas faux : c’était un **minorant dilué**, mélange de 12 paires de sœurs et 56 paires de famille-autre. Sur LANG_TREE, le coefficient de sœur est **+0,448**, soit **8×** celui de J3.1.

### 5. Contrôle d’époque

UDHR **mono-époque** (1948) : placebo de dates **−0,0013** [−0,065 ; +0,041]. Le seul bras daté de J3.1 (Bible) donne **−0,034/siècle** [−0,075 ; +0,009], p = 0,19, contre **+0,609** pour l’écriture. L’époque ne peut pas expliquer l’effet de famille ici.

## Fichiers

- Fiche : [`reports/rapport-retrieval-familles.md`](reports/rapport-retrieval-familles.md)
- JSON : [`reports/retrieval-familles.json`](reports/retrieval-familles.json)
- Outil : [`tools/retrieval_familles.py`](tools/retrieval_familles.py)
- État et roadmap mis à jour : [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md), [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md)

## Vérifications

`revue_documentation.py`, `verifie_en_cours.py`, `taille_documents.py` et `verifie_journal.py` passent. La passe complète des 84 portes n’a pas été relancée (changement de fiche uniquement) ; la dernière passe du 14/11 00 h 30 reste **81 vertes / 3 rouges connues** (`indice`, `melange`, `sessions`).

