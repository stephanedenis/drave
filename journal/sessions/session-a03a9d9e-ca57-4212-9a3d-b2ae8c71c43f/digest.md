# Session DSH — relecture

- identifiant : `session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 21:50:56
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche T2 (exploitable, 2/5) : **l'API du JSON** — (1) les `candidats` de l'attachement deviennent des **objets** `{span, cible, source}` au lieu des chaînes d'affichage (le schéma v2 gagne un champ, v1 toujours lue ; la sortie lisible garde les chaînes) ; (2) les `role` sont **normalisés** (un vocabulaire fermé : predicat, agent, objet, lieu, temps, qualite, possesseur, destinataire — sans accents mélangés), avec une table des correspondances et un test qui refuse un rôle hors vocabulaire. Fiche `reports/rapport-contrat-json.md` + JSON, les tests produit à jour, la doc § 3/4. **Contrôle négatif** : un consommateur qui filtre sur `role == "predicat"` doit trouver les prédicats.

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

- **bash** `{"command": "pwd; ls; echo \"---\"; ls docs/pilotage/; echo \"---\"; git log --oneline -10", "description": "Inspect repository root and recent history"}`

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
pyproject.toml
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
---
backlog
chantiers.md
en-cours.md
manques.md
plan-travail.md
programme-r.md
README.md
references-non-regression.md
roadmap.md
semaine-2.md
semaine-autonome.md
utilisation.md
---
71fdf72c CLÔTURE — LE PLAN (51 TÂCHES) ET LE PROTOCOLE OR-ROLES (X2) COMMITTÉS ; L'ÉTAT HORODATÉ
c9067a39 INDEX — RÉGÉNÉRÉ APRÈS LA SEMAINE 2 (W1-W6, X1-X3, Y1)
b8248b2d ÉTAT — T0 VERT (LA LIGNE W5 RACCOURCIE)
75dc9259 ÉTAT — T0 VERT
a1c45477 ÉTAT — T0 TENU (LES LIGNES R ET N RACCOURCIES)
f706aec0 Y1 — LE MODE AUTO DU TAGGER DOCUMENTÉ : L'API SI LA CLÉ EXISTE, L'HEURISTIQUE SINON, CODE 0 DANS TOUS LES CAS ; LA DÉCISION RESTE À L'HUMAIN
519b729f J5 — Y1 : LE MODE AUTO DU TAGGER (CLÉ 0/130 TOKENS, INVALIDE 0, SANS CLÉ 0 IDENTIQUE AU DÉFAUT, RÉSEAU 0 APRÈS 3 ESSAIS) ; 30/30 TESTS
f63ad709 BILAN DU 15/11 — LA SEMAINE 2 
… [453 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"attachement\" --include=*.py -l . | head -50", "description": "Find attachment-related Python files"}`

  ```
./tools/tests/linguistique/evaluer_gold.py
./tools/tests/linguistique/gold_reel.py
./tools/tests/linguistique/classement_cible.py
./tools/tests/linguistique/replis_cible.py
./tools/tests/linguistique/gold_split.py
./tools/tests/linguistique/test_bloc_linguistique.py
./tools/tests/linguistique/gold_reel_50.py
./tools/tests/linguistique/qualifier_tagger_h50.py
./tools/tests/test_restitution.py
./tools/tests/test_produit.py
./tools/tests/test_tagger_api.py
./tools/pensee/autotest.py
./tools/structures/tests/test_generateur.py
./tools/structures/construire_donnees.py
./tools/structures/llm.py
./tools/structures/serveur.py
./tools/structures/exporter_corpus.py
./tools/structures/generateur.py
./tools/restitution.py
./tools/mesurer_robustesse_semaine.py
./tools/mesurer_schema_v2_doc.py
./tools/atomes_prediction.py
./tools/restitution_v2.py
./tools/mesurer_restitution_v2.py
./tools/bloc_linguistique.py
./tools/drave.py
./tools/verifier_faq.py
./work/tableaux_atomes.py
./work/page-s-mesure/mesurer.py
  ```

- **bash** `{"command": "grep -rn \"T2\" docs/pilotage/plan-travail.md | head -20; echo \"---\"; wc -l docs/pilotage/plan-travail.md; echo \"---\"; ls reports | head -50", "description": "Locate T2 in the work plan"}`

  ```
---
456 docs/pilotage/plan-travail.md
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
atomes-prediction.json
atomes-prediction-mesures.json
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeur-mots.json
[stderr]
ls: write error: Broken pipe
  ```

- **bash** `{"command": "grep -rn \"candidats\\|schema_v2\\|schéma v2\\|schema v2\" --include=*.py --include=*.md -l . | head -40", "description": "Find schema v2 / candidates references"}`

  ```
./reports/rapport-capteur-hebbien.md
./reports/rapport-programme-evolutif.md
./reports/rapport-tete-garantie.md
./reports/rapport-v4-hca.md
./reports/rapport-engram-etat.md
./reports/rapport-v41-mhc.md
./reports/rapport-execution-v41.md
./reports/rapport-portes-p0-p9.md
./reports/archive/rapport-toutes-langues.md
./reports/archive/rapport-campagne-benefices.md
./reports/toutes-langues/045-45-premier-corpus-multi-domaine-et-aligne-4.md
./reports/toutes-langues/070-70-ou-entre-la-langue-dans-lentree-du-profe.md
./reports/campagne-benefices/027-24-memoire-episodique-c6-ce-qui-marche-et-c.md
./reports/campagne-benefices/042-39-audit-des-drapeaux-par-chemin-une-method.md
./reports/campagne-benefices/049-46-inventaire-des-drapeaux-en-chemin-repart.md
./reports/rapport-politique-budget-attention.md
./reports/rapport-vision-qwen2vl.md
./reports/07/p1.md
./reports/07/p3.md
./reports/07/p4.md
./reports/07/p7.md
./reports/07/p8.md
./reports/rapport-b1110-cartes.md
./reports/rapport-r04-tete-survol.md
./reports/rapport-pensee-v0.md
./reports/rapport-n2-corpus-reel.md
./reports/rapport-bloc-linguistique.md
./reports/rapport-pensee-drvf.md
./reports/rapport-pensee-gold-linguistique.md
./reports/
… [408 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"contrat-json\\|contrat json\\|T2 \" docs reports journal sprints tools --include=*.md --include=*.txt --include=*.py 2>/dev/null | head -40", "description": "Search contract JSON and T2 mentions"}`

  ```
docs/methode/contexte.md:16:| **T2 — jamais en entier** | l'histoire, les mesures brutes, les archives, les journaux | **0 mot par défaut** | `journal/` · `docs/archive/` · `reports/` (sauf verdict) · les documents datés |
docs/implantation/moteur-de-pensee.md:366:| **4** | `tools/pensee/` (`moteur.py`) | BFS, greedy, A*, MCTS-lite | T2 |
reports/rapport-pensee-ac3-alphabeta.md:94:| T2 stratégies | ✅ BFS et A* atteignent le but ; l'aveugle échoue |
reports/rapport-pensee-ac3-alphabeta.md:113:  boucle ; le contrat le dit, et la porte T2 (stratégie) ne le confond pas avec une stratégie.
reports/rapport-pensee-drvf.md:41:- T0 store canonique, T1 rejeu, T1 graine, **T1 DRVF thought**, T2 stratégies, T3 anytime,
journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/digest.md:281:- **bash** `{"command": "mkdir -p /tmp/toktest/{data,src,out} && cat > /tmp/toktest/gen_corpus.py <<'PYEOF'\n\"\"\"Génère /tmp/toktest/out/corpus.txt : un cas de test par ligne, texte échappé.\"\"\"\nimport sys\nsys.path.insert(0, \"/tmp/toktest\")\nWT2 = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/w … [3615 caractères tronqués]`
journal/sessions/8734fc13-aeb8-4cdf-b005-c182f77be0dc/digest.md:2818:**T
… [6321 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/rapport-pensee-attachement.md; wc -l reports/rapport-pensee-attachement.md; sed -n 1,80p reports/rapport-pensee-attachement.md", "description": "Read attachment report head"}`

  ```
reports/rapport-pensee-attachement.md
56 reports/rapport-pensee-attachement.md
# B13 — l'attachement sur le gold 432 : top1 0,3431, exact 0,0042

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **156/156 portes** : l'**attachement** (le segment → sa cible) est mesuré sur le gold 432 :
> **top1 0,3431**, **top-k 0,3264**, **exact 0,0042**, **couverture 0,6067**. La couverture est la
> première limite : **145 cibles sur 239** sont annotées, et l'attachement exact est **quasi nul**
> (1 sur 239).
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-attachement.json`](pensee-attachement.json).

## 1. Les deux mesures

| mesure | cibles | labels | top1 | top-k | exact | couverture |
|---|---:|---:|---:|---:|---:|---:|
| attachement | 239 | 145 | 82 (0,3431) | 78 (0,3264) | **1 (0,0042)** | 0,6067 |
| attachement (tête) | 145 | 145 | 81 (0,5586) | 77 (0,5310) | — | 1,0000 |

**Ce que ça dit** :

- **L'attachement exact est quasi nul** (1/239) : le bloc propose des candidats, pas 
… [1652 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"exploitable\" docs sprints reports --include=*.md | head -40", "description": "Search for exploitable task plan"}`

  ```
docs/archive/biologie-pour-drave.md:132:C'est le fait le plus directement exploitable de tout ce document, et il se voit en
docs/archive/note-chemin-court-n4.md:54:  dessin B ne rend pas l'état nativement lisible, il le rend **exploitable par un lecteur
docs/archive/plan-deepseek41-complet.md:197:  modèle — et elle est exploitable (si 12 des 16 sont négligeables, la couche se
docs/theorie/glossaire/06-repartition-materiel-et-energie.md:187:cartes graphiques (2 × 16 Go, 30,2 Go exploitables) ; *RSS* (resident set size) :
docs/theorie/glossaire/08-points-releves-non-corriges.md:109:    signale lui-même (`:62-65`) que ces chiffres ne sont pas exploitables.
docs/theorie/glossaire/entrees/ram-vram-rss.md:4:> **Fiche glossaire — RAM · VRAM · RSS.** *RAM* : mémoire de l'hôte (125 Go ici) ; *VRAM* : mémoire des cartes graphiques (2 × 16 Go, 30,2 Go exploitables) ; *RSS* (resident set size) : mémoire réellement occupée par un processus. Le contraste qui résume le projet : **47 Mo de RSS pour 365,7 Go de modèle adressé** en `mmap` (`reports/rapport-architecture-memoire.md:370-376`).
docs/theorie/protocole-semantique.md:101:- l'étage 3 sur `z` ne bat pas la surface → le sens n'est pas exploit
… [2437 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"candidats\" tools/*.py tools/pensee/*.py tools/structures/*.py 2>/dev/null | head -50", "description": "Find candidates implementation"}`

  ```
tools/aligneur_litteraire.py:453:                f"[ERREUR] chapitres {langue} non contigus : {nums} (candidats {stats['lignes_candidates']}, "
tools/banc_complet.py:93:    candidats: list[dict] = []
tools/banc_complet.py:109:        candidats.append({"question": question, "indice": texte[:70], "valeur": valeur,
tools/banc_complet.py:112:    if len(candidats) > n:
tools/banc_complet.py:113:        pas = len(candidats) / n
tools/banc_complet.py:114:        candidats = [candidats[int(i * pas)] for i in range(n)]
tools/banc_complet.py:115:    return candidats[:n]
tools/bloc_linguistique.py:7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
tools/bloc_linguistique.py:19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
tools/bloc_linguistique.py:80:    candidats: list[str] = field(default_factory=list)
tools/bloc_linguistique.py:90:            "candidats": list(self.candidats), "langue": self.langue,
tools/bloc_linguistique.py:1066:    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:
tools/bloc_linguistique.py:1067:        """Les candidats que le **précédent** impose : 
… [4387 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"attachement\\|attacher\\|attachment\" tools --include=*.py | head -60", "description": "Find attachment code"}`

  ```
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_css_builtins.py:33:    'background-attachment',
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_lasso_builtins.py:739:        'email_attachment_mime_type',
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_lasso_builtins.py:3113:        'addattachment',
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_lasso_builtins.py:4871:        'addattachment',
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_lilypond_builtins.py:3022:  "ly:note-head::calc-stem-attachment",
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_lilypond_builtins.py:3023:  "ly:note-head::calc-tab-stem-attachment",
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_lilypond_builtins.py:3026:  "ly:note-head::stem-attachment",
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_lilypond_builtins.py:4567:  "X-attachment",
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_lilypond_builtins.py:4573:  "Y-attachment",
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_lilypond_builtins.py:4993:  "stem-attachm
… [6412 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"role\\b\\|\\\"role\\\"\\|'role'\" tools/pensee tools/bloc_linguistique.py tools/restitution*.py --include=*.py | head -80", "description": "Find role handling in code"}`

  ```
tools/pensee/coeur.py:22:    def controle(x):
tools/pensee/coeur.py:26:            return {k: controle(v) for k, v in sorted(x.items())}
tools/pensee/coeur.py:28:            return [controle(v) for v in x]
tools/pensee/coeur.py:30:    return json.dumps(controle(objet), ensure_ascii=False, sort_keys=True,
tools/pensee/autotest.py:1538:        "role": mesurer_roles(ps)["justes"],
tools/pensee/autotest.py:1547:    """L'accord entre règles : role/sémantique 1,0, dernier nom/role −0,16."""
tools/pensee/autotest.py:1554:    return (paires["role/semantique"] == 1.0
tools/pensee/autotest.py:1555:            and paires["dernier_nom/role"] < 0), (
tools/pensee/autotest.py:1556:        f"kappa : role/semantique {paires['role/semantique']}, "
tools/pensee/autotest.py:1557:        f"dernier/role {paires['dernier_nom/role']}")
tools/pensee/autotest.py:1578:    return (r["poids"]["dernier_nom"] == 1 and r["poids"]["role"] == 0
tools/pensee/autotest.py:1628:          and abs(accords(tout)["paires"]["role/semantique"] - 1.0) < 1e-9)
tools/pensee/autotest.py:1652:    role = mesurer_roles(ps)
tools/pensee/autotest.py:1654:            and role["justes"] == 52), (
tools/pensee/autotest.py:1655:        
… [6275 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,180p tools/restitution_v2.py", "description": "Read restitution v2 beginning"}`

  ```
"""restitution_v2.py — la restitution v2 : les rôles (agent, prédicat, lieu).

La v0 restitue la **surface** (graphème → texte) ; la v1 restitue la **forme canonique**
(segments + rôles + cibles). La v2 ajoute une lecture **lisible des rôles** : un cadre
principal `agent / prédicat / lieu`, les cadres de chaque prédicat, et les segments de rôle.

La fidélité des rôles ne se mesure pas contre l'annotation qui les produit (ce serait une
tautologie) : elle se mesure contre un **or de rôles écrit à la main** sur les 46 textes
annotables du banc v0 (`tools/tests/linguistique/gold_restitution_v2.json`). L'or ne porte
que le **cadre principal** et quelques variantes d'ambiguïté ; il ne prétend pas annoter
toutes les propositions.

Deux mesures sont séparées :

- la **restitution** du rôle (le rôle est-il lisible et relu à l'identique ?) — un codec ;
- la **fidélité** du rôle (le rôle est-il celui de l'or ?) — une exactitude sémantique.

Le contrôle négatif retire ou permute les rôles du rendu : le lecteur doit le voir. Le
contrôle « cadre vide » et le contrôle « rôle constant par type » donnent les planchers.

    python3 tools/mesurer_restitution_v2.py
    python3 tools/drave.py restitue
… [5833 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"schéma v2\\|schema v2\\|schema_v2\\|v2\" docs/theorie/contrat-bloc-langue.md docs/implantation/bloc-linguistique.md docs/implantation/moteur-de-pensee.md 2>/dev/null | head -40", "description": "Find v2 schema docs"}`

  ```
(no output)
  ```

- **bash** `{"command": "sed -n 1,140p tools/bloc_linguistique.py", "description": "Read bloc_linguistique header"}`

  ```
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
`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script`
… [4258 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"drave.bloc\\|SCHEMA\\|schema\" tools/bloc_linguistique.py | head -30; echo ---; grep -rn \"drave\\..*\\.v[12]\\|schéma.*v[12]\\|schema.*v[12]\" docs tools --include=*.md --include=*.py | grep -v docwatch | head -40", "description": "Find schema names"}`

  ```
95:SCHEMA_ANNOTATION = "drave.annotation"
132:            "schema": SCHEMA_ANNOTATION, "version": VERSION_ANNOTATION,
2821:            "schema_identique": set(ah.json()) == set(an.json()),
2839:        "substitution": all(s["schema_identique"] for s in substitutions),
---
docs/pilotage/plan-travail.md:453:**Intégré** : schéma v1 publié (`tools/schemas/`), gold corrigé (4 GP), morphologie du 1er groupe
docs/pilotage/semaine-autonome.md:33:| `meta.alternative` / `meta.partition` — **publiés en v2** (v1 lue) | 26 cas, 0 échec | [`rapport-schema-v2.md`](../../reports/rapport-schema-v2.md) |
docs/pilotage/semaine-autonome.md:94:| | après-midi | le **schéma v2** (`meta.alternative`, `meta.partition`) et la **restitution v0** | schéma validé, miroir mesuré |
docs/pilotage/semaine-autonome.md:142:- le **produit** : 2 spans tranchés (ou déclarés), le schéma v2, la restitution v0, la porte verte ;
docs/pilotage/semaine-autonome.md:161:| J1.3 schéma v2 | ✅ fait | `meta.partition`/`meta.alternative`, 26 cas | `9a259953` |
docs/pilotage/semaine-autonome.md:195:| **J1** | après-midi : schéma v2 + restitution v0 | ✅ fait | **26 cas / 0 échec**, **1 836 annotations / 0 échec** ; **46/46** surfaces
… [7123 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/schemas/; echo ---; cat tools/schemas/drave-annotation-v2.json; echo ---; cat tools/schemas/drave-annotation-v1.json", "description": "Read product schemas"}`

  ```
drave-annotation-v1.json
drave-annotation-v2.json
---
{
 "$schema": "https://json-schema.org/draft/2020-12/schema",
 "$id": "https://drave.local/schema/annotation-v2.json",
 "title": "drave.annotation v2",
 "description": "L'annotation du bloc linguistique heuristique, version 2 : identique à la v1 et documente, dans `meta`, la partition des syntagmes qui se chevauchent (`meta.partition`) et les segments alternatifs du groupe (`meta.alternative`). Les deux champs sont additifs et optionnels : v1 reste lue.",
 "type": "object",
 "required": [
  "schema",
  "version",
  "texte",
  "langue",
  "script",
  "refus",
  "etiquettes",
  "unites_semantiques"
 ],
 "properties": {
  "schema": {
   "const": "drave.annotation"
  },
  "version": {
   "const": 2
  },
  "texte": {
   "type": "string"
  },
  "langue": {
   "type": "string",
   "pattern": "^[a-z]{2,3}$|^und$"
  },
  "script": {
   "type": "string"
  },
  "source": {
   "type": "string"
  },
  "refus": {
   "type": "string",
   "enum": [
    "",
    "vide",
    "non_texte",
    "trop_long",
    "neuronal"
   ]
  },
  "etiquettes": {
   "type": "array",
   "items": {
    "type": "object",
    "required": [
     "niveau",
     "type",

… [5878 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,240p tools/verifier_schema_produit.py", "description": "Read schema verifier"}`

  ```
#!/usr/bin/env python3
"""verifier_schema_produit.py — valide une annotation `drave.annotation` contre le schéma de sa version.

Deux schémas sont publiés (Draft 2020-12) :

- `tools/schemas/drave-annotation-v1.json` — le contrat d'origine (version 1) ;
- `tools/schemas/drave-annotation-v2.json` — le contrat courant (version 2) : il ajoute
  `meta.partition` et `meta.alternative`, les deux champs qui documentent les syntagmes qui se
  chevauchent.

Le vérificateur lit `version` dans l'annotation et choisit le schéma correspondant : une
annotation v1 reste donc **lue** et validée par le schéma v1. Il compile les schémas une fois,
puis valide les annotations de cas choisis : français, anglais, refus (texte vide), entrée non
textuelle, texte très long, plus une annotation v1 de rétro-compatibilité. Il ne dépend que de
`fastjsonschema` (sinon il se rabat sur une validation minimale des champs obligatoires et de la
version). Un **contrôle négatif** vérifie que le schéma v2 refuse bien une annotation v1.

Usage :
    python3 tools/verifier_schema_produit.py              # 5 cas v2 + 1 cas v1, sortie 0/1
    python3 tools/verifier_schema_produit.py --json       # le détail des cas
    pyt
… [5948 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"attachement\\|candidats\" tools/bloc_linguistique.py | sed -n 1,120p", "description": "Find attachment blocks and candidates"}`

  ```
7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
80:    candidats: list[str] = field(default_factory=list)
90:            "candidats": list(self.candidats), "langue": self.langue,
1066:    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:
1067:        """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
1222:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
1363:                                     "texte": texte[d:mots[j - 1][1]], "candidats": []})
1390:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
1399:                                     "candidats": []})
1405:            # convention du gold (FN GN 417) — mesuré F1 0,6519 → 0,7013, attachement inchangé.
1411:                                 "debut": d, "fin": f, "texte": texte[d:f], "candidats": []})
1419:                                 "debut": d, "fin": f, "texte": texte[d:f], "candidats": []})
1447:                                 "texte":
… [3113 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1640,1800p tools/bloc_linguistique.py", "description": "Read syntagm generation and attachment"}`

  ```
if self._negation(p):
                etiquettes.append(Etiquette("phrase", "négation", "oui", d, f, self.nom, 0.65,
                                            langue=lg, script=script))
            if self._modalite(p):
                etiquettes.append(Etiquette("phrase", "modalité", "oui", d, f, self.nom, 0.55,
                                            langue=lg, script=script))
            premier = next((m.group() for m in re.finditer(r"\w+", p)), "")
            acte = ("question" if typ == "interrogative" else
                    "exclamation" if typ == "exclamative" else
                    "ordre" if premier.casefold() in VERBES_IMPERATIFS else "assertion")
            etiquettes.append(Etiquette("pragmatique", "acte", acte, d, f, self.nom, 0.45,
                                        candidats=["assertion", "question", "ordre"],
                                        langue=lg, script=script))
            if (" ou " in p or "«" in p or "“" in p
                    or any(m in _normaliser(p) for m in MOTS_DOUBLE_SENS)):
                etiquettes.append(Etiquette("pragmatique", "double_sens", "candidat", d, f,
                                            self.nom, 0.25
… [9539 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1190,1260p tools/bloc_linguistique.py; echo ---; sed -n 2480,2540p tools/bloc_linguistique.py", "description": "Read verb candidates and vue"}`

  ```
dernier token du GV (`a vu` → `vu`, `est mangé` → `mangé`).
        """
        gvs = [g for g in gvs if not _est_adverbe_seul(g)]
        if segment.get("type") == "GV" or not gvs:
            return None
        if segment.get("type") == "GP":
            # un GP n'est pas gouverné par un mot de son propre span (« est prêt à manger »)
            dehors = [g for g in gvs
                      if not (g["debut"] >= segment["debut"] and g["fin"] <= segment["fin"])]
            if dehors:
                gvs = dehors
        # le plus proche, tous côtés mêlés : la variante « GV de gauche d'abord » a été
        # mesurée (2026-11-05) et donne **le même** exact — elle n'est pas retenue.
        def ecart(g: dict) -> int:
            if g["fin"] <= segment["debut"]:
                return segment["debut"] - g["fin"]
            if g["debut"] >= segment["fin"]:
                return g["debut"] - segment["fin"]
            return 0
        # un GV réduit à l'auxiliaire (« a », « est ») ne donne pas la cible : on prend le
        # premier GV proche dont le verbe est **plein** (mesuré : « a » au lieu de « vu »).
        for g in sorted(gvs, key=ecart):
            v = Heuristique._verbe
… [5605 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"\\\"role\\\"\\|\\\"role\\\":\\|role =\\|role=\\|'role'\" tools/bloc_linguistique.py tools/roles_gp.py tools/restitution_v2.py tools/restitution.py | head -120", "description": "Inventory role assignments"}`

  ```
tools/bloc_linguistique.py:990:                        gn.update({"type": "GN", "role": "agent", "niveau": 0,
tools/bloc_linguistique.py:1361:                                     "role": "complément" if stype == "SUB" else "qualité",
tools/bloc_linguistique.py:1382:                role = "groupe nominal"
tools/bloc_linguistique.py:1387:                    role = "patient"
tools/bloc_linguistique.py:1388:                segments.append({"type": "GN", "role": role, "niveau": 0,
tools/bloc_linguistique.py:1396:                    segments.append({"type": "REL", "role": "qualité", "niveau": 1,
tools/bloc_linguistique.py:1410:                segments.append({"type": "GN", "role": "agent", "niveau": 0,
tools/bloc_linguistique.py:1418:                segments.append({"type": "GN", "role": "agent", "niveau": 0,
tools/bloc_linguistique.py:1445:                segments.append({"type": "GV", "role": "prédicat", "niveau": 0,
tools/bloc_linguistique.py:1462:                segments.append({"type": "GP", "role": _role_gp(t), "niveau": 1,
tools/bloc_linguistique.py:1717:                    meta = {"role": s.get("role", ""), "niveau": s.get("niveau", 0)}
tools/bloc_linguistique.py:1740:           
… [2702 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"role\" tools/roles_gp.py | head -80; echo ---; grep -rn \"def _role_gp\\|_roles_gp\\|role_gp\" tools/bloc_linguistique.py", "description": "Inspect role module"}`

  ```
1:"""roles_gp.py — les rôles des groupes prépositionnels (restitution v3).
11:le bloc le réutilise. La fonction de compatibilité `_role_gp(prep)` du bloc garde son
15:    from tools.roles_gp import role_gp
16:    role_gp("à", suivant="la maison")          # lieu
17:    role_gp("à", suivant="14 h")               # temps
18:    role_gp("à", suivant="Marie")              # destinataire
19:    role_gp("de", suivant="la voisine", precedent="GN")   # possession
20:    role_gp("de", suivant="son projet", precedent="GV")   # theme
21:    role_gp("avec", suivant="le télescope")    # moyen
160:def normaliser_role(role: str) -> str:
162:    r = normaliser(role)
236:def role_gp(prep: str, suivant: str = "", precedent: str = "",
---
51:    from . import roles_gp as _roles_gp
53:    import roles_gp as _roles_gp
542:def _role_gp(prep: str, suivant: str = "", precedent: str = "",
553:        return _roles_gp.role_gp(prep, suivant=suivant, precedent=precedent,
1462:                segments.append({"type": "GP", "role": _role_gp(t), "niveau": 1,
  ```

- **bash** `{"command": "sed -n 1,330p tools/roles_gp.py", "description": "Read roles_gp module"}`

  ```
"""roles_gp.py — les rôles des groupes prépositionnels (restitution v3).

La v2 lisait la **préposition seule** : `à` était toujours un destinataire, `de` toujours
un thème, `avec` toujours un moyen. La v3 ajoute le **contexte** : ce qui suit la
préposition (un lieu, un temps, une personne, un infinitif) et ce qui la précède (un GN
ou un GV, un passif). Le rôle sort alors parmi les cinq catégories nommées par la tâche
— `lieu`, `temps`, `destinataire`, `possession`, `complement` — plus les rôles déjà
connus (`theme`, `moyen`, `but`, `agent`, `maniere`, `concession`, `source`).

Le module est **pur** (pas d'import du bloc linguistique) : il peut être testé seul, et
le bloc le réutilise. La fonction de compatibilité `_role_gp(prep)` du bloc garde son
ancien comportement quand aucun contexte n'est fourni ; c'est la v3 qui passe le
contexte.

    from tools.roles_gp import role_gp
    role_gp("à", suivant="la maison")          # lieu
    role_gp("à", suivant="14 h")               # temps
    role_gp("à", suivant="Marie")              # destinataire
    role_gp("de", suivant="la voisine", precedent="GN")   # possession
    role_gp("de", suivant="son projet", precedent="GV")   # theme
  
… [14940 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 960,1000p tools/bloc_linguistique.py; echo ---; sed -n 1330,1475p tools/bloc_linguistique.py", "description": "Read role production context"}`

  ```
n0 = _normaliser(mots[0][2])
                n0e = _elisions.get(n0.split("'")[0], n0)
                # le prédicat peut commencer par un clitique élidé (« elle s'ouvre »,
                # « il l'aime ») : on saute le clitique pour trouver le verbe, mais le GV
                # commence au clitique (il en fait partie).
                k = 1
                while k < len(mots) and _normaliser(mots[k][2]) in _clitiques:
                    k += 1
                if k >= len(mots):
                    sortie.append(s)
                    continue
                suivant = mots[k]
                ns = _normaliser(suivant[2])
                sv = (suivant[0] in pos_verbes or _est_verbe(suivant[2])
                      or ns in AUXILIAIRES
                      or self._pos(langue, suivant[2])[0] == "VERB"
                      or ns in {"ne", "n'", "n’"})
                # un nom propre sujet : un seul mot, majuscule, pas un mot fermé ; la
                # forme inversée « Peux-tu » est un verbe + enclitique, pas un sujet.
                nom_propre = ("-" not in mots[0][2] and mots[0][2][:1].isupper()
                              and not _est_verbe(mots[0][2])
                    
… [10156 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"exploitable,\" docs reports sprints journal --include=*.md | head -30; echo ---; ls sprints | tail -30", "description": "Search task batch"}`

  ```
reports/rapport-design-H-profondeur-routee.md:106:  **apprendraient** à rendre la sortie de la couche 16 exploitable, au lieu de laisser un adaptateur
reports/rapport-empaquetage.md:3:> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T1** (exploitable, 1/5) ·
---
02-fusionner-la-cha-ne-du-top-k-d-port-desc.md
03-qualit-de-l-attention-creuse-long-contex.md
04-le-k-de-l-attention-creuse-l-chec-au-mil.md
05-refaire-la-grille-avec-de-vraies-fenetres.md
06-le-taux-de-recuperation.md
07-cloture-de-la-nuit.md
08-un-modele-eclate-se-lit-comme-un-seul.md
09-empreinte-memoire-ce-qui-reduit-vraiment.md
10-v41-la-chaine-retardee-et-le-compresseur.md
11-v41-la-passe-complete.md
12-la-rotation-des-couches-compressees.md
13-les-deux-enigmes-du-decoupage-v41.md
14-p8-la-vivacit-de-l-engram-interrupteur-d.md
15-p9-le-poste-d-attention-v4-1-profiler-le.md
16-les-experts-sur-nvme-la-reutilisation.md
17-les-experts-io-ou-calcul.md
18-vectoriser-la-dequantification-des-experts.md
19-v41-a-1024-jetons.md
20-la-passe-longue-instrumentee.md
21-localiser-le-defaut-v41.md
22-la-composition-verifiee-et-les-deux-portes.md
23-la-porte-de-correction-outillee-et-longue.md
24-le-produit-scalaire-des-expe
… [368 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"contrat-json\\|T1.*T2.*T3\\|T2.*T3.*T4\" . --include=*.md 2>/dev/null | grep -v journal/sessions | head -20", "description": "Find T1-T5 plan"}`

  ```
./reports/rapport-pensee-drvf.md
  ```

- **bash** `{"command": "sed -n 1,200p reports/rapport-empaquetage.md", "description": "Read T1 exploitability report"}`

  ```
# T1 — l'empaquetage : `pip install -e .`, `drave` hors du dépôt, chemin historique intact

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T1** (exploitable, 1/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **empaquetage minimal livré**.
>
> **Le chiffre.** `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,
> **0** dépendance d'exécution, script console `drave = tools.drave:main`.
> `python3 -m pip install -e .` dans **`/tmp/venv-drave`** (Python **3.13.16**, pip **26.2.1**)
> rend **0** et `Successfully installed drave-0.1.0` ; `drave --version` rend **`drave 0.1.0`**
> et `drave analyser "Le chat dort."` rend **0** depuis **`/tmp`**. Le **contrôle négatif** —
> le même nom sans installation — échoue **proprement** : code **127**, `command not found`,
> **aucune** trace Python. Le chemin historique `python3 tools/drave.py` reste **vert**.
>
> **Dispositif** : [`pyproject.toml`](../pyproject.toml),
> [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py),
> [`reports/empaquetage.json`](empaquetage.json),
> [`docs/produit/README.md`](../docs/produit/README.md) § 8.10.

## 1. Ce qui est livré

Le paquet est **minimal** et sans
… [8032 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"^##\\|^###\" docs/produit/README.md | head -80", "description": "List product doc headings"}`

  ```
29:## Sommaire
41:## 1. À qui s'adresse le produit
57:## 2. Ce que le produit fait
93:## 3. Comment l'utiliser — cinq exemples réels
99:### 3.1 Analyser une phrase
122:### 3.2 Analyser en JSON et lire l'attachement
139:### 3.3 Mesurer sur le gold
195:### 3.3 quater Traiter un corpus
205:### 3.3 bis La vue des syntagmes qui se chevauchent — les champs du schéma v2
300:### 3.3 ter Le contexte (mémoire de discours)
309:### 3.4 Rejouer et vérifier le déterminisme
326:### 3.5 Le refus, et la langue inconnue
344:### 3.6 Restituer la surface (v0)
379:### 3.6 bis La base honnête — `--reel`
389:### 3.7 Le tagger en option — `--tagger`
517:## 4. Ce que le produit ne fait pas encore
590:## 5. Performance
612:## 6. Garanties
648:## 7. Le CLI livré — contrat et manques
738:## 8. FAQ — dix questions
748:### 8.1 Quelles langues le produit reconnaît-il ?
758:### 8.2 Est-ce que ça marche hors ligne ?
765:### 8.3 Combien ça coûte ?
774:### 8.4 Qu'est-ce que `--tagger` change ?
785:### 8.5 Quel est le format de sortie, et est-il stable ?
795:### 8.6 Que veut dire « attachement », et à quel point est-il fiable ?
806:### 8.7 Pourquoi reste-t-il un span inatteignable ?
816:### 8.8 Que peut-on restituer 
… [179 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"candidat\\|role\\|rôle\\|attachement\" docs/produit/README.md | head -80", "description": "Find product doc role/candidate sections"}`

  ```
26:> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
27:> candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.
45:| **linguiste, enseignant, curieux** | une analyse immédiate : POS, syntagmes, rôles, attachement, acte de parole | c'est une **annotation**, pas une traduction ni une correction |
46:| **développeur NLP** | un JSON déterministe, des spans, une confiance, des candidats | le format est **versionné** (schéma v2) ; v1 reste lue (§ 7) |
69:| **attachement** | par syntagme : `role`, `cible`, `candidats` | **238/239** exacts ; couverture **0,9958** ; exact sur span **1,0000** |
71:| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |
74:**Ce que « attachement » veut dire.** Pour un syntagme, le bloc publie la **cible** à laquelle il
76:**candidats**. C'est une lecture, avec sa confiance ; ce n'est pas un arbre syntaxique complet.
79:synthétiques ; **239 cibles** d'attachement ; **3 179 tokens**. Les règles ont été dessinées sur
83:1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat
88:**Les troi
… [6349 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 93,145p docs/produit/README.md; echo ---; sed -n 205,300p docs/produit/README.md", "description": "Read product doc §3.1-3.3bis"}`

  ```
## 3. Comment l'utiliser — cinq exemples réels

Tout se lance **depuis la racine du dépôt**. Les commandes ci-dessous sont celles d'aujourd'hui ;
elles n'utilisent ni modèle, ni GPU, ni réseau. Les JSON complets et commentés sont dans
[`exemples.md`](exemples.md).

### 3.1 Analyser une phrase

```bash
python3 tools/drave.py analyser "Le chat dort."
```
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
```

**Lecture.** La phrase est reconnue comme française, deux syntagmes sont posés, chacun avec sa
cible : le GN « Le chat » est rattaché à « dort », le GV « dort » à « chat ». Le gold `g001`
attend exactement ces deux spans et `assertion`. `POS` est la suite des mots ; `COU
… [6965 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 517,590p docs/produit/README.md; echo ---; sed -n 700,740p docs/produit/README.md", "description": "Read product doc §4 and §7 manques"}`

  ```
## 4. Ce que le produit ne fait pas encore

**1. Il ne génère pas de texte.** `restituer` reconstruit la **surface** depuis l'annotation
(codec), mais il n'y a **pas de génération** : pas de traduction, pas de réponse libre, pas de
paraphrase. Le produit rend des **étiquettes** et, avec `restituer`, la surface qu'elles
portent. Les résultats de traduction de la vitrine ([`README.md`](../../README.md)) sont une
recherche sur un modèle externe ; ils ne sont pas dans ce produit.

**1 bis. La restitution v2 lit les rôles, pas leur justesse.** `restituer --roles` rend un
cadre `agent / prédicat / lieu` lisible, mais la fidélité mesurée sur les 46 textes de la v0
est **19/46** cadres exacts (**16/46** non vides), **F1 0,5270** : la commande expose les
rôles de l'annotation, elle ne les corrige pas. La fiche
[`rapport-restitution-v2.md`](../../reports/rapport-restitution-v2.md) nomme le négatif.

**2. Un span reste inatteignable.** Sur **239 cibles**, **238** sont attachées (couverture
**0,9958**) ; **1** ne l'est pas : `g017` (une convention du gold, déclarée inatteignable le
14/11 — la règle coûtait deux autres spans). Elles sont
**inatteignables sans corriger le gold ou le lexique** — 
… [7160 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,260p tools/tests/test_produit.py", "description": "Read product tests"}`

  ```
"""test_produit.py — le smoke test de bout en bout du point d'entrée `tools/drave.py`.

Huit assertions, deux phrases (fr/en), le déterminisme et les codes de sortie. Le test passe
aussi bien par `python3 tools/tests/test_produit.py` que par `pytest` : il n'importe rien du
dépôt directement, il lance la commande comme un utilisateur.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
CLI = RACINE / "tools" / "drave.py"


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Lance la commande depuis la racine du dépôt, en UTF-8, sans réseau."""
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )


def detail(resultat: subprocess.CompletedProcess[str]) -> str:
    return (f"code={resultat.returncode}\n"
            f"stdout={resultat.stdout}\n"
            f"stderr={resultat.stderr}")


class TestProduit(unittest.TestCase):
    """Le contrat produit : version/aide, analyse, JSON, rejeu, usage."""


… [9863 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"candidat\\|role\\|rôle\\|attachement\" tools/drave.py | head -80", "description": "Find rendering in CLI"}`

  ```
15:    python3 tools/drave.py restituer "Le chat dort." --roles
20:avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
21:**restitution v0** (annotation → surface, avec la fidélité du miroir) et la **v2** (rôles
60:import restitution_v2  # noqa: E402  (la restitution v2 : les rôles)
61:import restitution_v3  # noqa: E402  (la restitution v3 : les rôles des GP)
71:# pas les syntagmes du neuronal (`PRIORITE_NIVEAU` le ferait) parce qu'ils n'ont ni rôle ni
72:# cible : l'attachement mesuré du produit serait perdu. Le gain mesuré porte sur le POS.
334:    rôles et attachements restent à l'heuristique (le neuronal n'en rend pas). `stats` porte le
422:    """La sortie lisible : POS compact, syntagmes (rôle + cible), pragmatique, couverture.
446:        roles = [str(e.meta.get("role") or "—") for e in syntagmes]
447:        cibles = [str((e.meta.get("attachement") or {}).get("cible") or "—") for e in syntagmes]
452:        lr = max(len(r) for r in roles)
454:        for e, valeur, role, cible, span in zip(syntagmes, valeurs, roles, cibles, spans):
457:                f"rôle={role:<{lr}}  → {cible}"
649:def _controle_hasard(phrases: list[dict]) 
… [4418 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,120p tools/restitution.py; echo ---; sed -n 450,610p tools/restitution.py", "description": "Read restitution forms"}`

  ```
"""restitution.py — la restitution v0 (surface) et la v1 (forme canonique).

La **surface** est reconstruite depuis le niveau `graphème` — les spans typés qui portent
les caractères — **sans lire** `Annotation.texte`. Les niveaux `mot` et `pos` sont mesurés
comme des sorties plus pauvres : ils disent ce que la couche de surface ajoute.

Le **miroir** est la règle 6 du dépôt : `fidelite` est binaire (1.0 si la sortie égale la
source), et `miroir` est le minimum des trois fidélités (surface, mots, pos). C'est la
définition de `tools/tests/linguistique/miroir.mesurer`, réutilisée ici pour ne pas en
avoir deux. `fidelite_caractere` ajoute une distance de Levenshtein normalisée : elle
distingue « presque fidèle » de « fidèle » et documente la perte de la ponctuation.

La **forme canonique** (v1) est une lecture **structurelle** de l'annotation : les
syntagmes avec leur type, leur rôle et leur cible d'attachement, une linéarisation sans
chevauchement, et un plancher de jetons normalisés (casse repliée, ponctuation retirée).
Elle ne remplace pas la surface : elle la met entre parenthèses pour mesurer ce que la
structure ajoute, et son **miroir canonique** se compare à une source canonisée
… [10648 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"candidat\\|attachement\\|role\" docs/produit/exemples.md | head -60", "description": "Find candidates in examples"}`

  ```
8:> attachement **238/238 labels** (238/239 cibles), schéma **v2**. Le format v2 ajoute
15:> les syntagmes, rôles et attachements restent à l'heuristique. La base `--reel` est la **base
19:> attachement **238/238 labels** (**238/239 cibles**, 0,9958), schéma **v2**. Gold **réel 452** :
20:> POS **0,8891**, F1 **0,7906**, attachement **183/184 labels** (0,9946). Les trois annotations
50:  `gold.cibles_attachement: 184` et `reel: null` (la base mesurée **est** déjà la base réelle).
51:- `meta.attachement` : `{segment, cible}` ; `cible` est une **chaîne**, pas un span.
55:  `union`, `relation`, `rang`, `role`, `attachement`, `retire` en vue filtrée) — v2.
56:- `candidats` : des **chaînes d'affichage** (parfois « « qui dort » → voisine »), pas des objets.
57:- `null` : pas d'attachement publié pour ce syntagme.
70:        | {valeur, type, debut, fin, confiance, role:.meta.role,
71:           cible:.meta.attachement.cible, union:.meta.union,
72:           partition:.meta.partition, alternative:.meta.alternative, candidats}],
113:           | {valeur, type, debut, fin, confiance, role:.meta.role,
114:              cible:.meta.attachement.cible, union:.meta.union, candidats}],
167:      "
… [2501 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,120p docs/produit/exemples.md", "description": "Read examples head"}`

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
… [5621 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 150,210p docs/produit/exemples.md; echo ---; sed -n 240,310p docs/produit/exemples.md", "description": "Read example candidates JSON"}`

  ```
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

**Lecture.**

- `langue: fr`, `script: Latn`, `refus: ""` : le texte est accepté.
- Quatre POS : `Le/DET`, `chat/NOUN`, `dort/VERB` et `.`/`PONCT` (0,95). `chat` et `dort` sont
  **ouverts** (confiance 0,3 et 0,72) : le lexique ne les connaît pas comme classes fermées.
- Deux syntagmes : `GN « Le chat » [0:7] → dort` et `GV « dort » [8:12
… [1453 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"candidats\" tools/tests tools/*.py --include=*.py | grep -v docwatch | head -80", "description": "Find candidate assertions in tests"}`

  ```
tools/tests/linguistique/evaluer_gold.py:155:            if any(any(c in nom for c in cibles) for nom in (e.candidats or [])):
tools/tests/linguistique/evaluer_gold.py:159:            if any(nom == cibles[0] for nom in (e.candidats or [])):
tools/tests/linguistique/evaluer_gold.py:173:            if any(any(c in nom for c in cibles) for nom in (et.candidats or [])):
tools/tests/linguistique/qualifier_lien_appris.py:46:    """Prépare les 9 questions de la vérité et leurs candidats annotés (mémoïsé)."""
tools/tests/linguistique/classement_cible.py:1:"""classement_cible.py — prototype **autonome** d'un classement appris des candidats d'attachement.
tools/tests/linguistique/classement_cible.py:166:def _candidats(phrase: dict, annotation) -> list[dict]:
tools/tests/linguistique/classement_cible.py:192:        vivier = _candidats(phrase, annotation)
tools/tests/linguistique/classement_cible.py:216:            candidats = []
tools/tests/linguistique/classement_cible.py:225:                candidats.append({**c, "distance": distance, "cote": cote})
tools/tests/linguistique/classement_cible.py:228:            candidats.sort(key=lambda c: (ordre[c["cote"]], c["distance"], c["i"]))
tools/test
… [7625 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"normaliser_role\\|ROLES\\b\\|vocabulaire\" tools tests 2>/dev/null --include=*.py | grep -v docwatch | head -60", "description": "Find role normalization usage"}`

  ```
tools/compare_logits.py:120:    assert nv_a == nv_b, f"vocabulaires différents : {nv_a} contre {nv_b}"
tools/corpus_wikipedia.py:42:CONTROLES = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
tools/corpus_wikipedia.py:51:    t = CONTROLES.sub(" ", t)
tools/speculatif.py:82:        print("# ATTENTION : vocabulaires différents — la mesure ne vaut rien")
tools/census_routage.py:50:    # Le corpus est lu en octets : le vocabulaire de ces modèles est de 256.
tools/speculatif_moteur.py:19:partager leur vocabulaire, sinon la comparaison ne mesure rien : l'outil le
tools/speculatif_moteur.py:70:    côtés, donc un faux « vocabulaire NON partagé ».
tools/speculatif_moteur.py:79:def vocabulaire_identique(modele_a, modele_b, sonde):
tools/speculatif_moteur.py:123:    ok, na, nb = vocabulaire_identique(a.brouillon, a.cible, sonde)
tools/speculatif_moteur.py:124:    dire(f"vocabulaire partagé : {'oui' if ok else 'NON'} "
tools/c8_entrainer_tete.py:18:La perplexité obtenue est donc **plein vocabulaire**, directement comparable à 1 127 368 (chemin
tools/n4_dessin_b.py:565:                         "volume, même vocabulaire, plus de séquence) — si la consolidation "
tools/entrainer_moteur.py:943:       
… [4934 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"role\" tools/structures/generateur.py | head -60; echo ---; sed -n 190,225p tools/structures/tests/test_generateur.py", "description": "Inspect generator roles"}`

  ```
246:def _role_gp(prep: str, segs: list["Segment"], utiles: list[Token], i: int) -> str:
294:    __slots__ = ("debut", "fin", "type", "role", "niveau", "texte", "cible_nom", "cible_gp",
297:    def __init__(self, debut, fin, texte, typ, role, niveau=0):
299:        self.type, self.role, self.niveau = typ, role, niveau
308:                "type": self.type, "role": self.role, "niveau": self.niveau,
432:                                "GP", _role_gp(_norm(t.texte), segs, utiles, i), 1))
479:                    g.role = "patient"
483:                    g.role = "agent"
505:def _role_attache(role: str, genre: str) -> str | None:
507:    if role == "instrument" and genre == "GN":
509:    if role == "possession" and genre == "GV":
511:    if role == "theme" and genre == "GN":
523:    variantes = []  # (role, cible, niveau)
526:            variantes.append((_role_attache(s.role, "GP"), ("GP", s.cible_gp), 2))
528:            variantes.append((_role_attache(s.role, "GN"), ("GN", s.cible_nom), 1))
530:            variantes.append((_role_attache(s.role, "GV"), ("GV", s.cible_verbe), 1))
533:            for role in ROLES_AMBIGUS.get(prep, []):
534:                if role != s.role:
535:      
… [2762 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"roles\\|rôle\" tools/tests/linguistique/gold_restitution_v2.json | head; echo ---; python3 - <<'PY'\nimport json\np='tools/tests/linguistique/gold_restitution_v2.json'\nd=json.load(open(p))\nprint(type(d), list(d)[:10] if isinstance(d,dict) else len(d))\nprint(json.dumps(d, e … [81 caractères tronqués]`

  ```
---
<class 'dict'> ['schema', 'version', 'date', 'ligne', 'tache', 'note', 'textes']
{"schema": "drave.restitution.v2.gold", "version": 1, "date": "2026-11-15", "ligne": "B13", "tache": "D2", "note": "Or **écrit à la main** sur les 46 textes annotables du banc v0 : le **cadre principal** (agent, prédicat, lieu), valeurs en surface et variantes pour les ambiguïtés réelles (coordination, contraction, inversion). Ce n'est pas une annotation complète : les propositions subordonnées et les seconds cadres ne sont pas notés. Les textes sans prédicat (numérique, courriel, symboles, remplissage latin) ont un cadre vide.", "textes": [{"id": "f01", "texte": "Le chat dort.", "langue": "fr", "variantes": [{"agent": "Le chat", "predicat": "dort", "lieu": ""}]}, {"id": "f02", "texte": "Le chat de la voisine qui dort sur le toit se réveille.", "langue": "fr", "variantes": [{"agent": "Le chat de la voisine", "predicat": "se réveille", "lieu": ""}, {"agent": "Le chat", "predicat": "se réveille", "lieu": ""}]}, {"id": "f03", "texte": "Bonjour ! Comment allez-vous aujourd'hui ?", "langue": "fr", "variantes": [{"agent": "vous", "predicat": "allez", "lieu": ""}, {"agent": "vous", "predicat": "allez-vous
… [385 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"API du JSON\\|l'API du JSON\\|candidats de l'attachement\\|schéma v2 gagne\" journal reports docs 2>/dev/null | head -20", "description": "Search exact task phrasing"}`

  ```
(no output)
  ```

- **bash** `{"command": "sed -n 1,180p docs/pilotage/en-cours.md", "description": "Read current state"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 15 h 05 HNE (clôture : le plan et le protocole or-roles committés)**

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
> l
… [11157 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 2250,2350p tools/pensee/autotest.py; echo ---; grep -rn \"prédicat\\|qualité\\|complément\\|predicat\\|qualite\\|complement\" tools/tests --include=*.py | head -60", "description": "Inspect role tests"}`

  ```
for s in p["segments"]:
            if not s.get("cible"):
                n += 1
                if n <= 500:
                    if s.get("type") == "GN":
                        gn += 1
                    elif s.get("type") == "GV":
                        gv += 1
    return gn == 294 and gv == 206, f"500 premiers : {gn} GN, {gv} GV"


def t156_relation() -> tuple[bool, str]:
    """La relation GN → GV : 570/863 (0,6605) après le sujet hors du GV."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger
    h = bl.Heuristique()
    n = avec = 0
    for p in charger():
        a = h.analyser(p["texte"], p["langue"])
        gv = any(e.niveau == "syntagme" and e.type == "GV" for e in a.etiquettes)
        for e in a.etiquettes:
            if e.niveau == "syntagme" and e.type == "GN":
                n += 1
                if gv and (e.meta or {}).get("role") in ("agent", "patient", "destinataire"):
                    avec += 1
    return n == 863 and avec == 570, f"relation : {avec}/{n} ({round(avec/n, 4)})"


def t157_roles() -> tuple[bool, str]:
    """Les GN sans rôle : 231, dont 151 avant le GV et 46 après."""
    import tools.bl
… [12503 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"role\" tools/tests/linguistique/evaluer_gold.py | head -60; echo ---; sed -n 1,140p tools/tests/linguistique/evaluer_gold.py", "description": "Read gold evaluation role logic"}`

  ```
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


GELE = pathlib.Path(__file__).with_name("gol
… [4555 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1040,1100p tools/bloc_linguistique.py; echo ---; grep -n \"def _tete_texte\\|def _verbe_dans\\|def _cible_precedent\\|def _cible_proche\\|def _verbe_gv\" tools/bloc_linguistique.py", "description": "Read previous candidates and helpers"}`

  ```
return Heuristique._verbe_dans(texte, precedent["debut"], precedent["fin"], verbes)
        return None

    @staticmethod
    def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict]) -> str | None:
        """REL **suivie d'un GV** : le sujet de ce GV (le GN le plus proche à gauche).

        Le gold : « elle qui commence nage » → REL « qui commence » a pour cible `elle`,
        sujet du GV `nage`. La règle ne s'applique qu'aux REL sans antécédent dans le
        chemin courant (union S/chunker) et exige un GV à droite **et** un GN à gauche.
        La règle littérale « REL après un GV » ne s'applique à aucun segment du gold.
        """
        if segment.get("type") != "REL":
            return None
        droites = [x for x in tous if x.get("type") == "GV"
                   and x.get("debut", 0) >= segment.get("fin", 0)]
        if not droites:
            return None
        gauches = [x for x in tous if x.get("type") == "GN"
                   and x.get("fin", 0) <= segment.get("debut", 0)]
        if not gauches:
            return None
        gn = max(gauches, key=lambda x: x["fin"])
        return Heuristique._tete_nom(texte, gn["debut"], gn["fin"])

    @stat
… [2241 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1100,1200p tools/bloc_linguistique.py; echo ---; sed -n 1260,1330p tools/bloc_linguistique.py", "description": "Read candidate helpers"}`

  ```
@staticmethod
    def _repli_verbe_propre(texte: str, segment: dict, cible: str | None):
        """Sans gouverneur extérieur, une SUB/REL prend son propre verbe (« qu'il viendra »)."""
        if cible or segment.get("type") not in ("SUB", "REL"):
            return cible
        return Heuristique._verbe_dans(texte, segment["debut"], segment["fin"]) or cible

    @staticmethod
    def _cible_hors_span(texte: str, segment: dict, gvs: list[dict], cible: str | None):
        """Un GP n'est pas gouverné par un mot de son span : on prend la tête du GV extérieur.

        `est prêt à manger` : `manger` est **dans** le GP `à manger` → on écarte et on prend la
        tête du GV extérieur `est prêt` → `prêt` (mesuré : g012, r018).
        """
        if not cible or segment.get("type") not in ("GP", "SUB"):
            return cible
        span = texte[segment["debut"]:segment["fin"]]
        if _normaliser(cible) not in _normaliser(span):
            return cible
        dehors = [g for g in gvs
                  if not (g["debut"] >= segment["debut"] and g["fin"] <= segment["fin"])
                  and not _est_adverbe_seul(g)]
        # pour une SUB, le gouverneur est le verbe de la 
… [7691 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _syntagmes_s\\|nom\\b\" tools/bloc_linguistique.py | head -40; echo ---; sed -n 760,930p tools/bloc_linguistique.py", "description": "Read S generator integration"}`

  ```
143:    nom: str
246:        nom = unicodedata.name(ch)
263:        if prefixe in nom:
389:# « car » est français : en anglais c'est un nom commun (r280)
815:    nom = "heuristique"
933:        le sujet (pronom, clitique ou nom propre) hors du GV, sans toucher au générateur
977:                # un nom propre sujet : un seul mot, majuscule, pas un mot fermé ; la
1002:    def _syntagmes_s(self, texte: str) -> list[dict] | None:
1017:        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
1025:            return {(s.debut, s.fin, s.type): (s.cible_gp or s.cible_nom or s.cible_verbe)
1036:            return Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
1063:        return Heuristique._tete_nom(texte, gn["debut"], gn["fin"])
1071:            tete = Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
1077:            # GP génitif (« de la voisine ») : le nom qu'il complète est un candidat
1081:                    tete = Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
1098:        return Heuristique._tete_nom(texte, g["debut"], g["fin"])
1146:    def _tete_nom(texte: str, debut: int, fin: int) -> st
… [9606 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 140,150p tools/bloc_linguistique.py; sed -n 1000,1040p tools/bloc_linguistique.py; echo ---; grep -n \"candidats\\|nom\" tools/structures/generateur.py | sed -n 1,50p", "description": "Inspect generateur interface"}`

  ```
class BlocLinguistique(Protocol):
    nom: str

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation: ...


class RefusNeuronal(RuntimeError):
    """Le modèle n'a pas rendu une annotation exploitable — le contrat refuse, il n'invente pas."""
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
        if not self.segm
… [3411 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn '\"role\"\\|role =\\|role=' tools/structures/generateur.py | head -80; echo ---; sed -n 240,340p tools/structures/generateur.py; echo ---; sed -n 460,520p tools/structures/generateur.py", "description": "Inventory generator roles"}`

  ```
294:    __slots__ = ("debut", "fin", "type", "role", "niveau", "texte", "cible_nom", "cible_gp",
308:                "type": self.type, "role": self.role, "niveau": self.niveau,
479:                    g.role = "patient"
483:                    g.role = "agent"
507:    if role == "instrument" and genre == "GN":
509:    if role == "possession" and genre == "GV":
511:    if role == "theme" and genre == "GN":
548:                    copie.role = role
632:            d["role"] = ROLES_DEFAUT[s.type]
---

def _infinitif(tok: Token) -> bool:
    n = _norm(tok.texte)
    return tok.cls == "MOT" and len(n) > 2 and n.endswith(("er", "ir", "re"))


def _role_gp(prep: str, segs: list["Segment"], utiles: list[Token], i: int) -> str:
    """Le rôle du GP, par la préposition **et son contexte** (ce qui précède, ce qui suit).

    Le contexte est ce qui distingue « de la voisine » (possession, après un GN) de
    « de son projet » (thème, après un GV), « à manger » (but, infinitif) de « à Marie »
    (destinataire), ou « par Marie » (agent, après un passif) de « par la porte » (moyen).
    """
    def _proche(types: tuple[str, ...]) -> "Segment | None":
        for s in reversed(segs):
          
… [5741 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"\\.json()\\|meta\\]\\|\\[\\\"meta\\\"\\]\\|meta:\" tools --include=*.py | grep -v docwatch | head -80", "description": "Find meta serialization usage"}`

  ```
tools/aligneur_litteraire.py:936:    meta: dict,
tools/aligneur_litteraire.py:1000:    meta = donnees["meta"]
tools/composition_multilingue.py:92:                            couches=np.array(couches), noms=np.array([f"{i}|{l}|{q}" for i, l, q in meta]))
tools/llm/tests/test_pipeline.py:28:        self.assertEqual(sum(1 for p in prompts if p["meta"]["categorie"] == "traduction"), 50)
tools/llm/tests/test_pipeline.py:29:        self.assertEqual(sum(1 for p in prompts if p["meta"]["categorie"] == "jeu"), 10)
tools/cerveau/tests/test_multilingue.py:16:        meta = self.r["meta"]
tools/cerveau/tests/test_multilingue.py:30:        meta = self.r["meta"]
tools/cerveau/tests/test_multilingue.py:42:        self.assertEqual(self.r["meta"]["langues_n1"],
tools/cerveau/tests/test_multilingue.py:44:        for langue in self.r["meta"]["langues_n1"]:
tools/cerveau/tests/test_multilingue.py:153:        self.assertEqual(self.r["meta"]["items_sans_paire"], 10)
tools/cerveau/bus.py:20:    meta: tuple[tuple[str, Any], ...] = ()
tools/cerveau/bus.py:37:                meta: dict | None = None) -> Evenement:
tools/cerveau/episodique.py:23:    meta: dict = field(default_factory=dict)
tools/cerveau/mult
… [6154 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,180p tools/tests/test_schema_produit.py; echo ---; sed -n 1,120p tools/mesurer_schema_v2_doc.py", "description": "Read schema tests and measure tool"}`

  ```
#!/usr/bin/env python3
"""test_schema_produit.py — le **contrat** du produit : schéma v2, v1 lue, refus, entrées hostiles.

Ce que le test fige (et qu'un client peut supposer) :
- 8 champs **obligatoires** à la racine : `schema`, `version`, `texte`, `langue`, `script`,
  `refus`, `etiquettes`, `unites_semantiques` ;
- `schema == "drave.annotation"` et `version == 2` ;
- `meta.partition` et `meta.alternative` sont déclarés dans le schéma v2 ;
- une annotation **v1 reste lue** par le vérificateur (schéma v1), et le schéma v2 la refuse ;
- un refus est une **réponse** : JSON valide avec `refus`, code de sortie 3 ;
- un surrogate isolé et une entrée non textuelle ne font pas planter.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_V1 = RACINE / "tools" / "schemas" / "drave-annotation-v1.json"
SCHEMA_V2 = RACINE / "tools" / "schemas" / "drave-annotation-v2.json"
VERIFICATEUR = RACINE / "tools" / "verifier_schema_produit.py"
OBLIGATOIRES = ("schema", "version", "texte", "langue", "script", "refus",
                "etiquettes", "unites_semantiques")


def _cli(*arg
… [9292 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/porte-*.sh | sed 's#tools/##' | head -100; echo ---; ls tools/porte-*.sh | wc -l", "description": "List gates"}`

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
porte-cic.sh
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
porte-oc
… [492 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/porte-produit.sh 2>/dev/null; echo ---; cat tools/porte-bloc-linguistique.sh | head -120", "description": "Read product gates"}`

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
… [4957 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"candidats\\|role\\|prédicat\\|qualité\" tools/tests/linguistique/test_bloc_linguistique.py | head -60; echo ---; grep -n \"candidats\\|role\" tools/tests/test_produit_libre.py tools/tests/test_restitution_v2.py | head -40", "description": "Check role/candidate assertions"}`

  ```
80:        """La convention du gold : le sujet est un GN, le GV commence au prédicat.
---
tools/tests/test_restitution_v2.py:5:- `drave restituer TEXTE --roles` rend un cadre principal lisible et un JSON v2 ;
tools/tests/test_restitution_v2.py:6:- `relire_roles(rendre_roles(a))` redonne le cadre principal (codec) ;
tools/tests/test_restitution_v2.py:46:    def test_restituer_roles(self):
tools/tests/test_restitution_v2.py:47:        sortie = drave("restituer", "Le chat dort.", "--roles")
tools/tests/test_restitution_v2.py:55:    def test_restituer_roles_json(self):
tools/tests/test_restitution_v2.py:56:        sortie = drave("restituer", "Le chat dort.", "--roles", "--json")
tools/tests/test_restitution_v2.py:61:        self.assertEqual(donnees["roles"]["principal"]["agent"], "Le chat")
tools/tests/test_restitution_v2.py:62:        self.assertEqual(donnees["roles"]["principal"]["predicat"], "dort")
tools/tests/test_restitution_v2.py:63:        self.assertEqual(donnees["roles"]["principal"]["lieu"], "")
tools/tests/test_restitution_v2.py:65:        self.assertTrue(donnees["controle_negatif_rendu"]["detecte"])
tools/tests/test_restitution_v2.py:68:    def test_roles_et_canonique_excl
… [2704 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _partitionner\\|_partitionner(\" tools/bloc_linguistique.py; sed -n 2400,2490p tools/bloc_linguistique.py", "description": "Read partition function context"}`

  ```
def _relation_partition(x: Etiquette, y: Etiquette) -> str:
    """La relation de `y` vue **depuis** `x` : `inclut` = x contient y."""
    if x.debut == y.debut and x.fin == y.fin:
        return "meme_span"
    if x.debut <= y.debut and x.fin >= y.fin:
        return "inclut"
    if y.debut <= x.debut and y.fin >= x.fin:
        return "inclus"
    return "croise"


def _cle_preferee(e: Etiquette) -> tuple:
    """La vue préférée : le segment du chunker (union), le plus large, puis le plus sûr.

    Mesuré sur le gold 612 : dans 179/207 groupes ambigus qui portent un span du gold, le
    chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.
    La préférence ne supprime rien par défaut : elle **classe**.
    """
    return (0 if (e.meta or {}).get("union") else 1, -(e.fin - e.debut), -e.confiance,
            e.debut, e.fin, e.type)


def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:
    """Les composantes connexes du graphe de chevauchement, ordonnées par position."""
    parent = list(range(len(segs)))

    def trouver(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
        
… [3030 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nh=bl.Heuristique()\nc=collections.Counter()\nex=collections.defaultdict(list)\nfor p in charger():\n    a=h.analyser(p['tex … [388 caractères tronqués]`

  ```
21 1883
'agent' 541 [('g001', 'Le chat', 'GN'), ('g002', 'Le chat', 'GN'), ('g003', 'La femme', 'GN')]
'prédicat' 369 [('g002', 'dort', 'GV'), ('g003', "a vu l'homme", 'GV'), ('g006', 'aboie', 'GV')]
'predicat' 342 [('g001', 'dort', 'GV'), ('g003', 'a vu', 'GV'), ('g004', 'a couru', 'GV')]
'groupe nominal' 267 [('g006', 'la nuit', 'GN'), ('g015', 'The cat', 'GN'), ('g016', 'The woman', 'GN')]
'patient' 55 [('g003', "l'homme", 'GN'), ('g008', 'un livre', 'GN'), ('g014', "l'homme", 'GN')]
'qualité' 55 [('g011', "que j'ai lu est intéressant", 'REL'), ('r014', "que j'ai lu est passionnant", 'REL'), ('r034', 'that I read', 'REL')]
'qualite' 51 [('g011', "que j'ai lu", 'REL'), ('r014', "que j'ai lu", 'REL'), ('r015', 'dont elle parle', 'REL')]
'lieu' 48 [('g003', 'dans le parc', 'GP'), ('g007', 'dans le jardin', 'GP'), ('g016', 'in the park', 'GP')]
'complément' 39 [('g005', "qu'elle viendrait hier", 'SUB'), ('g017', 'that she would come yesterday', 'SUB'), ('r050', 'en vacances', 'GP')]
'temps' 27 [('g005', 'hier', 'GP'), ('g010', 'ici', 'GP'), ('r008', 'depuis hier', 'GP')]
'but' 22 [('g004', 'pour attraper le bus', 'GP'), ('g012', 'à manger', 'GP'), ('g020', 'to eat', 'GP')]
'contenu'
… [1088 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"T1\\|empaquetage\\|exploitable\" docs/pilotage/roadmap.md docs/pilotage/en-cours.md | head -20", "description": "See T1 state references"}`

  ```
docs/pilotage/roadmap.md:31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observ
… [6008 caractères tronqués]
  ```

- **bash** `{"command": "git status --short | head -40; echo ---; git log --oneline -1 --stat | head -40", "description": "Check working tree"}`

  ```
M .gitignore
 M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M reports/faq.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-faq.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/verifier_faq.py
?? pyproject.toml
?? reports/empaquetage.json
?? reports/rapport-empaquetage.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
?? tools/tests/test_empaquetage.py
---
71fdf72c CLÔTURE — LE PLAN (51 TÂCHES) ET LE PROTOCOLE OR-ROLES (X2) COMMITTÉS ; L'ÉTAT HORODATÉ
 docs/pilotage/en-cours.md                          |    2 +-
 journal/2026-11-15/README.md                       |    7 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/
… [746 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -20; echo \"---\"; python3 tools/tests/test_schema_produit.py 2>&1 | tail -20", "description": "Run baseline product tests"}`

  ```
....................
----------------------------------------------------------------------
Ran 20 tests in 13.040s

OK
---
test_v1_reste_lue_et_v2_la_refuse (__main__.TestRetrocompatibilite.test_v1_reste_lue_et_v2_la_refuse)
Le vérificateur choisit le schéma par `version` ; v2 refuse bien une annotation v1. ... ok
test_anglais_meme_schema (__main__.TestSchemaDuProduit.test_anglais_meme_schema) ... ok
test_les_huit_champs_obligatoires (__main__.TestSchemaDuProduit.test_les_huit_champs_obligatoires) ... ok
test_mutation_detectee (__main__.TestSchemaDuProduit.test_mutation_detectee)
Contrôle négatif : un JSON amputé d'un champ obligatoire est bien refusé par le test. ... ok
test_refus_est_une_reponse_json (__main__.TestSchemaDuProduit.test_refus_est_une_reponse_json) ... ok
test_rejeu_identique (__main__.TestSchemaDuProduit.test_rejeu_identique) ... ok
test_surrogate_isole_ne_plante_pas (__main__.TestSchemaDuProduit.test_surrogate_isole_ne_plante_pas)
Le surrogate ne peut pas passer par argv (l'OS l'encode) : on teste l'API puis l'écriture. ... ok
test_le_schema_v2_declare_partition_et_alternative (__main__.TestSchemaV2.test_le_schema_v2_declare_partition_et_alternative)
Les deux cha
… [157 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/tests/test_restitution_v2.py 2>&1 | tail -20; echo \"---\"; python3 tools/tests/linguistique/test_bloc_linguistique.py 2>&1 | tail -15", "description": "Run baseline block tests"}`

  ```
test_restituer_roles (__main__.TestCommandeRoles.test_restituer_roles) ... ok
test_restituer_roles_json (__main__.TestCommandeRoles.test_restituer_roles_json) ... ok
test_roles_et_canonique_exclusifs (__main__.TestCommandeRoles.test_roles_et_canonique_exclusifs) ... ok
test_gold_analyseur (__main__.TestGoldExterne.test_gold_analyseur) ... ok
test_sans_or (__main__.TestMesureSansOr.test_sans_or) ... ok
test_cas_connus (__main__.TestOrEtBanc.test_cas_connus) ... ok
test_controles_v2 (__main__.TestOrEtBanc.test_controles_v2) ... ok
test_or_46_textes (__main__.TestOrEtBanc.test_or_46_textes) ... ok
test_roles_par_role (__main__.TestOrEtBanc.test_roles_par_role) ... ok
test_synthese_v2 (__main__.TestOrEtBanc.test_synthese_v2) ... ok
test_controle_negatif_rendu (__main__.TestRenduRoles.test_controle_negatif_rendu) ... ok
test_controle_non_eligible (__main__.TestRenduRoles.test_controle_non_eligible) ... ok
test_melange_roles (__main__.TestRenduRoles.test_melange_roles) ... ok
test_rendu_ne_lit_pas_le_texte (__main__.TestRenduRoles.test_rendu_ne_lit_pas_le_texte) ... ok
test_rendu_simple (__main__.TestRenduRoles.test_rendu_simple) ... ok

--------------------------------------------------
… [170 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,120p tools/restitution_v3.py", "description": "Read restitution v3 role expectations"}`

  ```
"""restitution_v3.py — la restitution v3 : les rôles des groupes prépositionnels.

La v2 lisait la préposition seule. La v3 ajoute le **contexte** et sépare les cinq rôles
nommés par la tâche : `lieu`, `temps`, `destinataire`, `possession`, `complement`
(plus `theme`, `moyen`, `but`, `agent`, `maniere`, `concession`, `source`).

Deux mesures, deux ors :

- le **gold v2** (46 textes) n'annote que `agent / prédicat / lieu` : on y mesure la
  précision et le rappel de ces trois rôles, avant (v2) et après (v3) ;
- le **gold S** (61 phrases, 144 rôles) annote les cinq catégories : on y mesure la
  précision et le rappel **par rôle**, avec les effectifs. Les cinq rôles n'y ont que
  18 occurrences — un `complement` zéro — et c'est une limite nommée, pas un résultat
  triomphal.

Le **contrôle négatif** permute les rôles prédits (les cinq, puis tous) : la mesure doit
s'effondrer. Le contrôle « rôle constant » et le contrôle « règles coupées » donnent les
planchers. Le codec `relire_roles(rendre_roles(a)) == principal` est mesuré à part : il
ne compte **pas** comme fidélité.

    python3 tools/drave.py restituer "Le voyage à Paris dure deux heures." --roles-v3
    python3 tools/mesurer_res
… [3562 caractères tronqués]
  ```

- **write** `{"content": "\"\"\"roles_vocabulaire.py — le vocabulaire **fermé** des rôles de l'annotation.\n\nLe produit publie un rôle par syntagme (`meta.role`). Les règles internes en produisent\nplusieurs orthographes et plusieurs granularités : `prédicat`/`predicat`, `qualité`/\n`qualite`, `patient`/`complé … [4625 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_vocabulaire.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "sed -n 44,100p tools/bloc_linguistique.py", "description": "Read imports and Etiquette"}`

  ```
import unicodedata
import urllib.request
from dataclasses import dataclass, field
from typing import Protocol, Sequence

RACINE = pathlib.Path(__file__).resolve().parent.parent
try:  # paquet : `tools.bloc_linguistique`
    from . import roles_gp as _roles_gp
except ImportError:  # script : `python3 tools/bloc_linguistique.py`
    import roles_gp as _roles_gp
NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
           "pragmatique", "document")
SOURCES = ("heuristique", "neuronal", "humain")
SCRIPT_NEUTRE = "Zyyy"

# --------------------------------------------------------------------------- types


@dataclass(frozen=True)
class Span:
    debut: int
    fin: int

    def json(self) -> dict:
        return {"debut": self.debut, "fin": self.fin}


@dataclass
class Etiquette:
    niveau: str
    type: str
    valeur: str
    debut: int
    fin: int
    source: str = "heuristique"
    confiance: float = 0.5
    candidats: list[str] = field(default_factory=list)
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    meta: dict = field(default_factory=dict)

    def json(self) -> dict:
        return {
            "niveau": self.niveau, "type": self
… [538 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/bloc_linguistique.py')\nt=p.read_text(encoding='utf-8')\nold='''try:  # paquet : `tools.bloc_linguistique`\n    from . import roles_gp as _roles_gp\nexcept ImportError:  # script : `python3 tools/bloc_linguistique.py`\n    import … [2656 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/bloc_linguistique.py')\nt=p.read_text(encoding='utf-8')\nanchor='''    @staticmethod\n    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:\n'''\nnew='''    @staticmethod\n    def _cible_ca … [3056 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"meta\\[\\\"attachement\\\"\\]\" tools/bloc_linguistique.py", "description": "Locate attachment assignments"}`

  ```
1812:                        meta["attachement"] = {"segment": s.get("texte", ""), "cible": cible}
1840:                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
1870:                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
  ```

- **bash** `{"command": "sed -n 1795,1835p tools/bloc_linguistique.py", "description": "Read first assignment block"}`

  ```
cible = self._tete_nom(texte, g["debut"], g["fin"])
                    if not cible and s.get("type") == "GP":
                        cible = self._cible_proche(texte, s, gvs, verbes, cache_gv)
                    if not cible and brute and _normaliser(brute) not in ADVERBES_SEULS:
                        i = texte.find(brute)
                        if i >= 0:
                            cible = self._verbe_dans(texte, i, i + len(brute), verbes)
                    if cible and _normaliser(cible) in AUXILIAIRES:
                        cible = None  # « a » / « est » ne sont pas des cibles
                    if not cible:
                        gns_s = [x for x in c.get("segments", []) if x.get("type") == "GN"]
                        cible = (self._repli_cible_gp(texte, s, gns_s)
                                 or self._cible_proche(texte, s, gvs, verbes, cache_gv))
                    cible = self._cible_hors_span(texte, s, gvs, cible)
                    cible = self._repli_verbe_propre(texte, s, cible)
                    meta = {"role": s.get("role", ""), "niveau": s.get("niveau", 0)}
                    if cible:
                        meta["attachement"] = {"segment":
… [1479 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/bloc_linguistique.py')\nt=p.read_text(encoding='utf-8')\nold='''                    cible = self._cible_hors_span(texte, s, gvs, cible)\n                    cible = self._repli_verbe_propre(texte, s, cible)\n                    m … [5055 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sed -n 2550,2585p tools/bloc_linguistique.py", "description": "Read alternative attachment copy"}`

  ```
drapeau `retire`. Aucun segment n'est supprimé en mode `alternative`.

    `filtrer="union"` : on retire le S qui **contient** un segment chunker (le filtre
    union du P0-3) ; les autres chevauchements restent documentés. `filtrer="strict"` :
    le chunker est la partition — **tous** les segments `union` sont conservés, et tous
    les S qui les chevauchent sont retirés. Dans les deux cas, le retiré reste lisible
    dans `meta.alternative` du segment conservé, avec `retire: true`.
    """
    segs = [e for e in etiquettes if e.niveau == "syntagme"]
    groupes = _groupes_partition(segs)
    rangs: dict[int, tuple[int, int]] = {}
    for gid, groupe in enumerate(groupes):
        for i, e in enumerate(sorted(groupe, key=_cle_preferee)):
            rangs[id(e)] = (gid, i + 1)
    retirees: set[int] = set()
    if filtrer == "union":
        for groupe in groupes:
            unions = [e for e in groupe if (e.meta or {}).get("union")]
            for e in groupe:
                if not (e.meta or {}).get("union") and any(
                        u.debut >= e.debut and u.fin <= e.fin
                        and (u.fin - u.debut) < (e.fin - e.debut) for u in unions):
              
… [746 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 2585,2625p tools/bloc_linguistique.py", "description": "Read alternative copy exact"}`

  ```
if not paires:
                break
            for x, y in paires:
                rx = rangs.get(id(x), (0, 99))[1]
                ry = rangs.get(id(y), (0, 99))[1]
                retirees.add(id(x if rx >= ry else y))
    for gid, groupe in enumerate(groupes):
        for e in groupe:
            if filtrer and id(e) in retirees:
                continue
            meta = dict(e.meta or {})
            meta["partition"] = {"groupe": gid, "rang": rangs[id(e)][1],
                                 "membres": len(groupe),
                                 "vue": ("alternative" if not filtrer
                                         else "filtrer_union" if filtrer == "union"
                                         else "filtrer")}
            vues = []
            for autre in groupe:
                if autre is e:
                    continue
                vue = {"type": autre.type, "debut": autre.debut, "fin": autre.fin,
                       "source": autre.source,
                       "union": bool((autre.meta or {}).get("union")),
                       "relation": _relation_partition(e, autre),
                       "rang": rangs[id(autre)][1]}
                if filt
… [738 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/bloc_linguistique.py')\nt=p.read_text(encoding='utf-8')\nold='''                att = (autre.meta or {}).get(\"attachement\")\n                if att:\n                    vue[\"attachement\"] = {\"segment\": att.get(\"segment\", … [660 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sed -n 420,465p tools/drave.py", "description": "Read readable output function"}`

  ```
def formater_annotation(a: bl.Annotation, tagger: bool = False,
                        stats: dict | None = None, titre: str | None = None) -> str:
    """La sortie lisible : POS compact, syntagmes (rôle + cible), pragmatique, couverture.

    Avec `--tagger`, l'en-tête le dit, le coût de l'API est affiché et un refus du tagger est
    nommé — le JSON d'annotation, lui, garde exactement le même contrat. `titre` permet au mode
    `auto` de nommer la voie qui a réellement servi (API, heuristique, ou repli).
    """
    if titre is None:
        titre = (f"{NOM} {VERSION} — analyse cascade POS (tagger API DeepSeek, réseau)"
                 if tagger else f"{NOM} {VERSION} — analyse heuristique (CPU, hors ligne)")
    lignes = [titre]
    lignes.append(
        f"langue={a.langue} script={a.script} source={a.source} · {len(a.etiquettes)} étiquettes "
        f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"
    )

    pos = [e for e in a.etiquettes if e.niveau == "pos"]
    if pos:
        lignes.extend(_envelopper("POS  ", " ".join(f"{e.valeur}/{e.type}" for e in pos)))
    else:
        lignes.append("POS  —")

    syntagmes = [e for e in a
… [1066 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/drave.py')\nt=p.read_text(encoding='utf-8')\nold='''        roles = [str(e.meta.get(\"role\") or \"—\") for e in syntagmes]\n'''\nnew='''        roles = [bl.normaliser_role(e.meta.get(\"role\", \"\")) or \"—\" for e in syntagmes] … [148 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nh=bl.Heuristique()\nd=h.analyser(\"Le chat dort.\", \"fr\").json()\nprint(json.dumps([{k:e[k] for k in ('type','valeur','candidats','meta')} for e in d['etiquettes'] if e['niveau']=='syntag … [179 caractères tronqués]`

  ```
[
 {
  "type": "GN",
  "valeur": "Le chat",
  "candidats": [
   "structure la plus proche",
   "dort"
  ],
  "meta": {
   "role": "agent",
   "niveau": 1,
   "attachement": {
    "segment": "Le chat",
    "cible": "dort",
    "candidats": [
     {
      "span": {
       "debut": 8,
       "fin": 12
      },
      "cible": "dort",
      "source": "heuristique"
     }
    ]
   }
  }
 },
 {
  "type": "GV",
  "valeur": "dort",
  "candidats": [
   "structure la plus proche"
  ],
  "meta": {
   "role": "predicat",
   "niveau": 0,
   "attachement": {
    "segment": "dort",
    "cible": "chat",
    "candidats": [
     {
      "span": {
       "debut": 3,
       "fin": 7
      },
      "cible": "chat",
      "source": "heuristique"
     }
    ]
   }
  }
 }
]
roles ['agent', 'predicat']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nd=bl.Heuristique().analyser(\"Le livre que j'ai lu est intéressant.\", \"fr\").json()\nfor e in d['etiquettes']:\n    if e['niveau']=='syntagme':\n        print(e['type'], e['valeur'], 'rol … [380 caractères tronqués]`

  ```
GN Le livre role= agent cands= ["« que j'ai lu » → Le livre", 'intéressant', 'livre']
  att= {"segment": "Le livre", "cible": "intéressant", "candidats": [{"span": {"debut": 25, "fin": 36}, "cible": "intéressant", "source": "heuristique"}, {"span": {"debut": 0, "fin": 8}, "cible": "Le livre", "source": "heuristique"}, {"span": {"debut": 3, "fin": 8}, "cible": "livre", "source": "heuristique"}]}
REL que j'ai lu role= qualite cands= ["« que j'ai lu » → Le livre", 'intéressant', 'livre']
  att= {"segment": "que j'ai lu", "cible": "livre", "candidats": [{"span": {"debut": 3, "fin": 8}, "cible": "livre", "source": "heuristique"}, {"span": {"debut": 0, "fin": 8}, "cible": "Le livre", "source": "heuristique"}, {"span": {"debut": 25, "fin": 36}, "cible": "intéressant", "source": "heuristique"}]}
  alt REL qualite {'segment': "que j'ai lu est intéressant", 'cible': 'livre', 'candidats': [{'span': {'debut': 3, 'fin': 8}, 'cible': 'livre', 'source': 'heuristique'}, {'span': {'debut': 25, 'fin': 36}, 'cible': 'intéressant', 'source': 'heuristique'}]}
  alt GV predicat {'segment': 'est intéressant', 'cible': 'livre', 'candidats': [{'span': {'debut': 3, 'fin': 8}, 'cible': 'livre', 'source': 'he
… [1867 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfrom pathlib import Path\np=Path('tools/schemas/drave-annotation-v2.json')\ns=json.loads(p.read_text(encoding='utf-8'))\n\nROLES = [\"predicat\",\"agent\",\"objet\",\"lieu\",\"temps\",\"qualite\",\"possesseur\",\"destinataire\"]\n\ndef span_schema():\n     … [2366 caractères tronqués]`

  ```
ok
json-ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\ns=json.load(open('tools/schemas/drave-annotation-v2.json'))\nm=s['properties']['etiquettes']['items']['properties']['meta']\nprint(json.dumps(m, ensure_ascii=False, indent=1)[:3000])\nPY", "description": "Inspect schema meta"}`

  ```
{
 "type": "object",
 "properties": {
  "partition": {
   "type": "object",
   "required": [
    "groupe",
    "rang",
    "membres",
    "vue"
   ],
   "properties": {
    "groupe": {
     "type": "integer",
     "minimum": 0
    },
    "rang": {
     "type": "integer",
     "minimum": 1
    },
    "membres": {
     "type": "integer",
     "minimum": 2
    },
    "vue": {
     "enum": [
      "alternative",
      "filtrer_union",
      "filtrer"
     ]
    }
   },
   "additionalProperties": true
  },
  "alternative": {
   "type": "array",
   "minItems": 1,
   "items": {
    "type": "object",
    "required": [
     "type",
     "debut",
     "fin",
     "source",
     "union",
     "relation",
     "rang"
    ],
    "properties": {
     "type": {
      "enum": [
       "GN",
       "GV",
       "GP",
       "REL",
       "SUB"
      ]
     },
     "debut": {
      "type": "integer",
      "minimum": 0
     },
     "fin": {
      "type": "integer",
      "minimum": 1
     },
     "source": {
      "enum": [
       "heuristique",
       "neuronal",
       "humain"
      ]
     },
     "union": {
      "type": "boolean"
     },
     "relation": {
      "enum": [
       "inclut",
     
… [1797 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/verifier_schema_produit.py')\nt=p.read_text(encoding='utf-8')\nold='''- `tools/schemas/drave-annotation-v2.json` — le contrat courant (version 2) : il ajoute\n  `meta.partition` et `meta.alternative`, les deux champs qui document … [6327 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/mesurer_schema_v2_doc.py')\nt=p.read_text(encoding='utf-8')\nold='''    for etiquette in d.get(\"etiquettes\", []):\n        meta = etiquette.get(\"meta\")\n        if isinstance(meta, dict):\n            meta.pop(\"partition\",  … [604 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --json 2>&1 | tail -60", "description": "Run schema verifier"}`

  ```
{
 "schemas": {
  "1": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v1.json",
  "2": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v2.json"
 },
 "versions_lues": [
  1,
  2
 ],
 "validateur": true,
 "retrocompatibilite": {
  "v1_lue": true,
  "v2_refuse_v1": true
 },
 "controles_negatifs": {
  "role_hors_vocabulaire": true,
  "candidat_chaine": true
 },
 "cas": [
  {
   "cas": "fr",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "en",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "vide",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "ponctuation",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "long",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "v1",
   "version": 1,
   "ok": true,
   "erreurs": []
  }
 ]
}
  ```

- **bash** `{"command": "python3 tools/tests/test_schema_produit.py 2>&1 | tail -20", "description": "Run schema tests"}`

  ```
test_v1_reste_lue_et_v2_la_refuse (__main__.TestRetrocompatibilite.test_v1_reste_lue_et_v2_la_refuse)
Le vérificateur choisit le schéma par `version` ; v2 refuse bien une annotation v1. ... ok
test_anglais_meme_schema (__main__.TestSchemaDuProduit.test_anglais_meme_schema) ... ok
test_les_huit_champs_obligatoires (__main__.TestSchemaDuProduit.test_les_huit_champs_obligatoires) ... ok
test_mutation_detectee (__main__.TestSchemaDuProduit.test_mutation_detectee)
Contrôle négatif : un JSON amputé d'un champ obligatoire est bien refusé par le test. ... ok
test_refus_est_une_reponse_json (__main__.TestSchemaDuProduit.test_refus_est_une_reponse_json) ... ok
test_rejeu_identique (__main__.TestSchemaDuProduit.test_rejeu_identique) ... ok
test_surrogate_isole_ne_plante_pas (__main__.TestSchemaDuProduit.test_surrogate_isole_ne_plante_pas)
Le surrogate ne peut pas passer par argv (l'OS l'encode) : on teste l'API puis l'écriture. ... ok
test_le_schema_v2_declare_partition_et_alternative (__main__.TestSchemaV2.test_le_schema_v2_declare_partition_et_alternative)
Les deux champs ajoutés en v2 sont typés, pas seulement tolérés. ... ok

---------------------------------------------------------------
… [33 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -30", "description": "Run product tests after change"}`

  ```
....................
----------------------------------------------------------------------
Ran 20 tests in 13.303s

OK
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/test_bloc_linguistique.py 2>&1 | tail -25", "description": "Run block tests after change"}`

  ```
....................
----------------------------------------------------------------------
Ran 20 tests in 0.079s

OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/tests/test_produit.py')\nt=p.read_text(encoding='utf-8')\nold='''class TestRobustesse(unittest.TestCase):\n'''\nnew='''class TestContratJSON(unittest.TestCase):\n    \"\"\"T2 — l'API du JSON : candidats d'attachement en objets, r … [4848 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/tests/test_schema_produit.py')\nt=p.read_text(encoding='utf-8')\nold='''    def test_le_schema_v2_declare_partition_et_alternative(self):\n        \"\"\"Les deux champs ajoutés en v2 sont typés, pas seulement tolérés.\"\"\"\n     … [2623 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -35", "description": "Run product tests with T2 cases"}`

  ```
........................
----------------------------------------------------------------------
Ran 24 tests in 13.893s

OK
  ```

- **bash** `{"command": "python3 tools/tests/test_schema_produit.py 2>&1 | tail -20", "description": "Run schema tests with T2 case"}`

  ```
test_v1_reste_lue_et_v2_la_refuse (__main__.TestRetrocompatibilite.test_v1_reste_lue_et_v2_la_refuse)
Le vérificateur choisit le schéma par `version` ; v2 refuse bien une annotation v1. ... ok
test_anglais_meme_schema (__main__.TestSchemaDuProduit.test_anglais_meme_schema) ... ok
test_les_huit_champs_obligatoires (__main__.TestSchemaDuProduit.test_les_huit_champs_obligatoires) ... ok
test_mutation_detectee (__main__.TestSchemaDuProduit.test_mutation_detectee)
Contrôle négatif : un JSON amputé d'un champ obligatoire est bien refusé par le test. ... ok
test_refus_est_une_reponse_json (__main__.TestSchemaDuProduit.test_refus_est_une_reponse_json) ... ok
test_rejeu_identique (__main__.TestSchemaDuProduit.test_rejeu_identique) ... ok
test_surrogate_isole_ne_plante_pas (__main__.TestSchemaDuProduit.test_surrogate_isole_ne_plante_pas)
Le surrogate ne peut pas passer par argv (l'OS l'encode) : on teste l'API puis l'écriture. ... ok
test_le_schema_v2_declare_candidats_structures_et_roles (__main__.TestSchemaV2.test_le_schema_v2_declare_candidats_structures_et_roles)
T2 : `meta.attachement.candidats` est typé, et `role` est un vocabulaire fermé. ... ok
test_le_schema_v2_declare_partition_et_
… [256 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/tests/test_produit_libre.py 2>&1 | tail -20", "description": "Run free-text product tests"}`

  ```
test_alternative_etiquettes (__main__.TestProduitLibre.test_alternative_etiquettes) ... ok
test_deterministe (__main__.TestProduitLibre.test_deterministe) ... ok
test_filtrer_sans_chevauchement (__main__.TestProduitLibre.test_filtrer_sans_chevauchement) ... ok
test_non_linguistiques_sans_syntagme (__main__.TestProduitLibre.test_non_linguistiques_sans_syntagme) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.369s

OK
  ```

- **bash** `{"command": "python3 tools/tests/test_restitution_v2.py 2>&1 | tail -12; echo ---; python3 tools/tests/test_restitution.py 2>&1 | tail -12", "description": "Run restitution tests"}`

  ```
test_roles_par_role (__main__.TestOrEtBanc.test_roles_par_role) ... ok
test_synthese_v2 (__main__.TestOrEtBanc.test_synthese_v2) ... ok
test_controle_negatif_rendu (__main__.TestRenduRoles.test_controle_negatif_rendu) ... ok
test_controle_non_eligible (__main__.TestRenduRoles.test_controle_non_eligible) ... ok
test_melange_roles (__main__.TestRenduRoles.test_melange_roles) ... ok
test_rendu_ne_lit_pas_le_texte (__main__.TestRenduRoles.test_rendu_ne_lit_pas_le_texte) ... ok
test_rendu_simple (__main__.TestRenduRoles.test_rendu_simple) ... ok

----------------------------------------------------------------------
Ran 17 tests in 1.446s

OK
---
test_miroir_canonique_et_strict (__main__.TestFormeCanonique.test_miroir_canonique_et_strict) ... ok
test_ne_lit_pas_le_texte (__main__.TestFormeCanonique.test_ne_lit_pas_le_texte) ... ok
test_controle_negatif (__main__.TestReconstruction.test_controle_negatif) ... ok
test_distance (__main__.TestReconstruction.test_distance) ... ok
test_ne_lit_pas_le_texte (__main__.TestReconstruction.test_ne_lit_pas_le_texte) ... ok
test_niveaux_pauvres (__main__.TestReconstruction.test_niveaux_pauvres) ... ok
test_surface_sans_controle (__main__.TestReconstru
… [140 caractères tronqués]
  ```

- **bash** `{"command": "AUTOTEST_JOBS=8 timeout 900 python3 -m tools.pensee.autotest 2>&1 | tail -25", "description": "Run full autotest", "timeoutMs": 900000}`

  ```
✅ T157 rôles par position rôles : 267 sans rôle, 198 avant le GV, 64 après
  ✅ T158 passifs           passifs : 5/5 faux (le sujet est un patient)
  ✅ T159 correctif passifs par → agent, avec → moyen
  ✅ T160 passifs sans par  passif sans par (chunker) : 3/3 patient
  ✅ T161 cible proximité   proximité : top1 238/239, exact 238/239, tête 238/238
  ✅ T162 candidats verbes  candidats : top-k 236/239 (0.9874), tête 236/238
  ✅ T163 échecs attachement échecs : 1 de span, 2 de cible (33 avant les correctifs)
  ✅ T164 verbe du GV       verbe du GV : saw (attendu saw) ; exact 238/239
  ✅ T165 lexique verbal    lexique : talks True, joue True, brother False ; cible GP talks
  ✅ T166 spans perdus      spans : 0 REL, 1 SUB, 0 GP
  ✅ T167 dénominateur      dénominateur : spans 1.0 / 0.9916 / 1.0
  ✅ T168 classement        classement : exact 238/238 ; cibles 158 verbes, 80 noms
  ✅ T169 conventions       conventions : verbes 158/158 (1.0), noms 80/80 (1.0)
  ✅ T170 attachement ciblé ciblé : REL « homme » homme, GP « joue » joue
  ✅ T171 lexique élargi    lexique élargi : vu True, accroché True, couru True ; exact 238/238
  ✅ T172 échecs de cible   échecs de cible : 0 hors candidats, 0 mal clas
… [596 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/mesurer_schema_v2_doc.py --json 2>&1 | tail -40", "description": "Run schema v2 documentation measure", "timeoutMs": 300000}`

  ```
"v2_refuse_v1": 612,
  "v1_refuse_v2": 612,
  "mutation_champ_obligatoire_refusee": true
 },
 "champs_vus_sur_le_gold": {
  "vue": "alternative",
  "porteurs_de_partition": 437,
  "groupes": 146,
  "alternatives": 930,
  "types": {
   "GN": 393,
   "GP": 49,
   "GV": 357,
   "REL": 103,
   "SUB": 28
  },
  "relations": {
   "croise": 386,
   "inclus": 263,
   "inclut": 263,
   "meme_span": 18
  },
  "sources": {
   "heuristique": 930
  }
 },
 "tests_schema": {
  "commande": "python3 tools/tests/test_schema_produit.py",
  "code_sortie": 0,
  "tests": 8,
  "echecs": 0
 },
 "limites": [
  "les 612 annotations v1 sont dérivées des 612 annotations v2 (version=1, champs v2 retirés), pas un corpus v1 indépendant",
  "le schéma valide la forme et les énumérations, pas les invariants sémantiques (réciprocité, unicité des groupes, rangs)",
  "sans fastjsonschema, la validation du vérificateur est minimale (champs obligatoires + version)",
  "le bump v1 -> v2 change les octets et le sha256 de rejeu ; la compatibilité est structurelle, pas octet pour octet",
  "les comptes de champs (146 groupes, 437 porteurs, 930 alternatives) sont in-sample sur le gold 612"
 ]
}
  ```

- **bash** `{"command": "grep -n \"tests_schema\\|Ran\\|test_schema\" -A12 -B4 tools/mesurer_schema_v2_doc.py", "description": "Inspect test count parsing"}`

  ```
102-                         cwd=str(RACINE), text=True, capture_output=True)
103-    cli_d = json.loads(cli.stdout)
104-    gold20 = subprocess.run([sys.executable, str(RACINE / "tools/verifier_schema_produit.py"),
105-                             "--gold", "20"], cwd=str(RACINE), text=True, capture_output=True)
106:    tests = subprocess.run([sys.executable, str(RACINE / "tools/tests/test_schema_produit.py")],
107-                           cwd=str(RACINE), text=True, capture_output=True)
108-
109-    return {
110-        "date": "2026-11-14",
111-        "tache": "J11.4",
112-        "ligne": "B13",
113-        "objet": "documentation et validation du schéma v2",
114-        "code_mesure": "09e54143",
115-        "outil": "tools/mesurer_schema_v2_doc.py",
116-        "schemas": {str(v): str(p.relative_to(RACINE)) for v, p in SCHEMAS.items()},
117-        "documentation": {
118-            "fichier": "docs/produit/README.md",
--
164-            "types": dict(sorted(types.items())),
165-            "relations": dict(sorted(relations.items())),
166-            "sources": dict(sorted(sources.items())),
167-        },
168:        "tests_schema": {
169:            "commande": "python3
… [886 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json, collections, time\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nfrom tools.roles_vocabulaire import ROLES, CORRESPONDANCES, normaliser_role\nh=bl.Heuristique()\nphrases=charge … [1858 caractères tronqués]`

  ```
time 1.1
phrases 612 segments 1883 roles_non_vides 1883 raw_distinct 21 norm_distinct 8
attachments 1295 avec_objets 1295 sans 0 objets 2139 objets_alt 1062 spans_bad 0 cible_dans_objets 1295
norm roles Counter({'predicat': 711, 'agent': 541, 'objet': 390, 'qualite': 120, 'lieu': 48, 'destinataire': 37, 'temps': 27, 'possesseur': 9})
raw roles Counter({'agent': 541, 'prédicat': 369, 'predicat': 342, 'groupe nominal': 267, 'patient': 55, 'qualité': 55, 'qualite': 51, 'lieu': 48, 'complément': 39, 'temps': 27, 'but': 22, 'contenu': 22, 'destinataire': 15, 'possession': 9, 'cause': 5, 'attribut': 4, 'theme': 3, 'moyen': 3, 'concession': 3, 'hypothese': 2, 'complement': 1})
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nh=bl.Heuristique()\nc=collections.Counter()\nfor p in charger():\n    for e in h.analyser(p['texte'],p['langue']).json()['e … [231 caractères tronqués]`

  ```
agent GN 541
destinataire GP 37
lieu GP 48
objet GN 322
objet GP 11
objet SUB 57
possesseur GP 9
predicat GV 711
qualite GP 4
qualite REL 106
qualite SUB 10
temps GP 21
temps SUB 6
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"mesurer_contrat_json.py — T2 : les candidats d'attachement en objets, les rôles normalisés.\n\nLe banc mesure, sur le gold vivant (612 phrases), ce que le consommateur du JSON peut\nsupposer :\n\n- chaque `meta.attachement` porte des `candidats` **objets**  … [15533 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_contrat_json.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/mesurer_contrat_json.py 2>&1 | tail -20", "description": "Run T2 measurement", "timeoutMs": 300000}`

  ```
phrases 612 · segments 1883 · rôles 1883
  candidats : 2139 objets (1295/1295 attachements) · spans faux 0
  rôles : 21 bruts → 8 normalisés · hors table 0 · hors vocabulaire 0
  contrôle négatif : filtre predicat 711 (711 GV) · prédicat accentué 0 · rôle inconnu levé True
  validation : v2 0 échec(s), v1 0 échec(s)
  écrit : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/contrat-json.json
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/contrat-json.json'))\nprint(json.dumps({k:d[k] for k in ('corpus','candidats','controles_negatifs','validation','tests')}, ensure_ascii=False, indent=1))\nprint('roles', d['vocabulaire_roles']['normalises_observes'])\nprint('table … [85 caractères tronqués]`

  ```
{
 "corpus": {
  "nom": "gold vivant (hand + reel + synthétique)",
  "phrases": 612,
  "segments": 1883,
  "roles_non_vides": 1883
 },
 "candidats": {
  "attachements": 1295,
  "attachements_avec_objets": 1295,
  "attachements_sans_objet": 0,
  "objets": 2139,
  "objets_alternatives": 1062,
  "taille_moyenne": 1.6517,
  "cible_choisie_presente": 1295,
  "spans_faux": 0
 },
 "controles_negatifs": {
  "filtre_predicat": {
   "role": "predicat",
   "segments": 711,
   "gv": 711,
   "verdict": "trouve"
  },
  "filtre_predicat_accentue": {
   "role": "prédicat",
   "segments": 0,
   "verdict": "vide"
  },
  "role_inconnu_leve": true,
  "role_inconnu_message": "rôle hors vocabulaire : 'role_invente' (attendu : predicat, agent, objet, lieu, temps, qualite, possesseur, destinataire)",
  "candidat_chaine_refuse": true,
  "candidat_sans_span_refuse": true,
  "v2_refuse_v1": true,
  "v1_lue": true,
  "role_schema_refuse": true,
  "candidat_chaine_schema_refuse": true
 },
 "validation": {
  "v2_annotations": 612,
  "v2_echecs": 0,
  "v1_annotations": 612,
  "v1_echecs": 0,
  "v2_refuse_v1": 612
 },
 "tests": {
  "test_produit": {
   "code": 0,
   "tests": 24,
   "echecs": 0
  },
  "test_schema
… [209 caractères tronqués]
  ```

- **bash** `{"command": "cat > reports/rapport-contrat-json.md <<'EOF'\n# T2 — l'API du JSON : candidats d'attachement en objets, rôles normalisés\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T2** (exploitable, 2/5) ·\n> **Date** : 2026-11-15 · **Verdict** : ✅ **contrat livré et mesuré**.\n>\n> … [11916 caractères tronqués]`

  ```
220 reports/rapport-contrat-json.md
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json | jq -r '.etiquettes[] | select(.niveau==\"syntagme\") | \"\\(.type) \\(.valeur) role=\\(.meta.role) → \\(.meta.attachement.cible) · \" + ([.meta.attachement.candidats[] | \"\\(.cible)[\\(.span.debut):\\(.span.fin)]\"] | join(\",  … [53 caractères tronqués]`

  ```
GN Le chat role=agent → dort · dort[8:12]
GV dort role=predicat → chat · chat[3:7]
  ```

- **bash** `{"command": "sed -n 785,840p docs/produit/README.md", "description": "Read FAQ format limits"}`

  ```
### 8.5 Quel est le format de sortie, et est-il stable ?

Le JSON est estampillé `schema: "drave.annotation"` et `version: 2`. La v2 ajoute deux champs
**optionnels** dans `meta` — `partition` et `alternative` — pour documenter les syntagmes qui
se chevauchent ; les **huit champs obligatoires** de la racine sont ceux de la v1, et un client
v1 qui ignore `meta` continue de lire. `tools/verifier_schema_produit.py` lit les versions
**1 et 2**, valide **6 cas** (dont un cas v1) et, avec `--gold 20`, **26 cas, 0 échec** ; le
contrôle négatif soumet le cas v1 au schéma v2, qui le **refuse**. La compatibilité **octet
pour octet** entre versions n'est pas garantie : le bump change le JSON et son `sha256`.

### 8.6 Que veut dire « attachement », et à quel point est-il fiable ?

Pour chaque syntagme, le produit publie un **rôle**, une **cible** d'attachement et des
**candidats** : « Le chat » → `dort`, la REL « que j'ai lu » → `livre`. Ce n'est **pas un
arbre syntaxique complet**. Sur le gold vivant 612, **238/239 cibles** sont attachées
(**0,9958**) ; sur les 238 segments dont le span est prédit, l'exactitude est **1,0000** ; le
top-k vaut **0,9874**. Le contrôle négatif du CLI — une cible 
… [2622 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 57,95p docs/produit/README.md", "description": "Read product overview table"}`

  ```
## 2. Ce que le produit fait

Une seule opération : `analyser(texte, langue)` → une **annotation**. Elle porte neuf niveaux ;
le produit en expose cinq, plus le coût et la trace. Le JSON est estampillé `schema`
(`"drave.annotation"`) et `version` (`2`) ; en v2, `meta.partition` et `meta.alternative`
documentent les syntagmes qui se chevauchent.

| ce que vous demandez | ce que vous obtenez | mesure du 15/11 |
|---|---|---|
| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; le CLI n'expose que `fr`/`en` comme indice) |
| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger` |
| **syntagmes** | GN, GV, GP, REL, SUB, avec leur span | F1 **0,7902** ; tête **0,9029** (vivant 612) ; **0,7906** sur le réel 452 |
| **attachement** | par syntagme : `role`, `cible`, `candidats` | **238/239** exacts ; couverture **0,9958** ; exact sur span **1,0000** |
| **pragmatique** | acte (assertion, question, exclamation), négation, modalité, double sens | acte **0,9967**, négation **0,9771**, modalité **0,9886**, d
… [1683 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/README.md')\nt=p.read_text(encoding='utf-8')\n\n# 1. overview\nold='''le produit en expose cinq, plus le coût et la trace. Le JSON est estampillé `schema`\n(`\"drave.annotation\"`) et `version` (`2`) ; en v2, `meta.partiti … [11858 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 53, in <module>
AssertionError
[exit code: 1]
  ```

- **bash** `{"command": "grep -n \"attachement.*objet\\|role.*chaîne\\|candidats.*structurés\\|role.*normalisé\" docs/produit/README.md | head -20", "description": "Find exact table rows"}`

  ```
243:| `attachement` | objet | optionnel, `{segment, cible}` | attachement recopié de l'alternative, quand il existe |
244:| `role` | chaîne | optionnelle | rôle recopié de l'alternative, quand il existe |
723:| **`candidats` structurés** | ce sont des **chaînes d'affichage** (« « qui dort » → voisine »), pas des objets `{span, cible}` ; un programme doit les reparser |
724:| **`role` normalisé** | les valeurs mélangent `predicat`/`prédicat` et `qualite`/`qualité` ; fragile pour un filtre |
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/README.md')\nt=p.read_text(encoding='utf-8')\ndef rep(name, old, new):\n    global t\n    if old not in t:\n        print('MISS', name); raise SystemExit(1)\n    t=t.replace(old,new,1); print('OK', name)\nrep('overview', ' … [2988 caractères tronqués]`

  ```
OK overview
OK row_att
MISS 3.2
[exit code: 1]
  ```

- **bash** `{"command": "sed -n 130,142p docs/produit/README.md | cat -A | head -20", "description": "Inspect exact 3.2 ending"}`

  ```
GN Le livre M-bM-^FM-^R intM-CM-)ressant M-BM-7 REL que j'ai lu M-bM-^FM-^R livre M-BM-7 REL que j'ai lu est intM-CM-)ressant M-bM-^FM-^R livre M-BM-7 GV est intM-CM-)ressant M-bM-^FM-^R livre$
```$
$
**Lecture.** Un appel = **une annotation** ; les phrases sont des M-CM-)tiquettes de niveau `phrase`,$
pas des objets sM-CM-)parM-CM-)s. La REL M-BM-+ que j'ai lu M-BM-; est bien rattachM-CM-)e M-CM-  M-BM-+ livre M-BM-; (cas `g011` du$
gold). Le JSON publie aussi une **seconde lecture d'union** (`meta.union: true`, span plus$
large) : dans la sortie lisible, elle apparaM-CM-.t comme un **doublon REL** ; le JSON la marque$
`union: true`, M-CM-  filtrer pour une lecture unique (voir [`exemples.md`](exemples.md) M-BM-' 2).$
$
### 3.3 Mesurer sur le gold$
$
```bash$
python3 tools/drave.py evaluer$
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/README.md')\nt=p.read_text(encoding='utf-8')\ndef rep(name, old, new):\n    global t\n    if old not in t:\n        print('MISS', name); raise SystemExit(1)\n    t=t.replace(old,new,1); print('OK', name)\nrep('overview', ' … [3131 caractères tronqués]`

  ```
OK overview
OK row_att
OK 3.2
OK table_alt
  ```

- **bash** `{"command": "sed -n 243,255p docs/produit/README.md", "description": "Inspect table for new insertion"}`

  ```
**ferme** chaque alternative (`additionalProperties: false`).

**`meta.partition` — la place du segment dans son groupe.**

| champ | type | contrainte | sens |
|---|---|---|---|
| `groupe` | entier | `≥ 0` | identifiant du groupe de chevauchement, stable dans l'annotation |
| `rang` | entier | `≥ 1` | rang du segment dans le groupe ; `1` = segment préféré (chunker `union`, puis le plus large, puis le plus sûr) |
| `membres` | entier | `≥ 2` | nombre de segments du groupe |
| `vue` | énumération | `alternative`, `filtrer_union`, `filtrer` | vue qui a produit l'annotation (`brut` n'écrit pas ces champs) |

**`meta.alternative` — les autres segments du groupe, vus depuis le porteur.**
  ```

- **bash** `{"command": "sed -n 255,285p docs/produit/README.md", "description": "Inspect alt table end"}`

  ```
| champ | type | contrainte | sens |
|---|---|---|---|
| `type` | énumération | `GN`, `GV`, `GP`, `REL`, `SUB` | type du segment alternatif |
| `debut`, `fin` | entiers | `0 ≤ debut < fin` | span en **points de code Unicode**, 0-based, `[debut:fin)` |
| `source` | énumération | `heuristique`, `neuronal`, `humain` | provenance du segment |
| `union` | booléen | — | le segment vient de l'union S/chunker |
| `relation` | énumération | `inclut`, `inclus`, `meme_span`, `croise` | relation **du point de vue du porteur** : `inclut` = le porteur contient l'alternative ; `inclus` = l'alternative contient le porteur ; `croise` = intersection partielle |
| `rang` | entier | `≥ 1` | rang de l'alternative dans le groupe |
| `retire` | booléen | optionnel | présent en vue `filtrer`/`filtrer_union` ; `true` = segment retiré de la sortie mais toujours lisible ici |
| `attachement` | objet | optionnel, `{segment, cible, candidats?}` | attachement recopié de l'alternative, avec ses candidats objets quand ils existent |
| `role` | chaîne | optionnelle, vocabulaire fermé | rôle normalisé recopié de l'alternative, quand il existe |

```json
{
  "type": "REL", "debut": 22, "fin": 42, "valeur": "qui dort
… [610 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/README.md')\nt=p.read_text(encoding='utf-8')\ndef rep(name, old, new):\n    global t\n    if old not in t:\n        print('MISS', name); raise SystemExit(1)\n    t=t.replace(old,new,1); print('OK', name)\n\nrep('candidates … [8340 caractères tronqués]`

  ```
OK candidates table
OK example alt1
OK example alt2
OK 4 1ter
OK 7 manques rows
OK 7 tenu
OK 8.5
OK 8.6
OK 8.9
  ```

- **bash** `{"command": "python3 - <<'PY'\nt=\"Le chat de la voisine qui dort sur le toit se réveille.\"\nfor c in (\"réveille\",\"voisine\",\"se réveille\"):\n    i=t.find(c); print(c,i,i+len(c),repr(t[i:i+len(c)]))\nprint(len(t))\nPY", "description": "Check example spans"}`

  ```
réveille 46 54 'réveille'
voisine 14 21 'voisine'
se réveille 43 54 'se réveille'
55
  ```

- **bash** `{"command": "python3 - <<'PY'\nt=\"Le chat de la voisine qui dort sur le toit se réveille.\"\nfor c in (\"qui dort sur le toit\",\"qui dort sur le toit se réveille\",\"se réveille\"):\n    i=t.find(c); print(repr(c),i,i+len(c))\nPY", "description": "Check example REL spans"}`

  ```
'qui dort sur le toit' 22 42
'qui dort sur le toit se réveille' 22 54
'se réveille' 43 54
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/README.md')\nt=p.read_text(encoding='utf-8')\nt=t.replace('{\"span\": {\"debut\": 43, \"fin\": 52}, \"cible\": \"réveille\", \"source\": \"heuristique\"}',\n            '{\"span\": {\"debut\": 46, \"fin\": 54}, \"cible\":  … [363 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/exemples.md')\nt=p.read_text(encoding='utf-8')\nold='''- `meta.attachement` : `{segment, cible}` ; `cible` est une **chaîne**, pas un span.\n'''\nnew='''- `meta.attachement` : `{segment, cible, candidats}` ; `cible` est un … [809 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sed -n 115,135p tools/mesurer_schema_v2_doc.py", "description": "Inspect schema measure docs fields"}`

  ```
"outil": "tools/mesurer_schema_v2_doc.py",
        "schemas": {str(v): str(p.relative_to(RACINE)) for v, p in SCHEMAS.items()},
        "documentation": {
            "fichier": "docs/produit/README.md",
            "section": "3.3 bis — La vue des syntagmes qui se chevauchent — les champs du schéma v2",
            "champs_documentes": {
                "meta.partition": ["groupe", "rang", "membres", "vue"],
                "meta.alternative": ["type", "debut", "fin", "source", "union", "relation", "rang",
                                     "retire (optionnel)", "attachement (optionnel)",
                                     "role (optionnel)"],
            },
            "retrocompatibilite": {
                "v1_inchangee": True,
                "champs_racine_identiques": True,
                "champs_ajoutes_optionnels": True,
                "compatibilite_octet_pour_octet": False,
            },
        },
        "validation_verificateur": {
            "commande": "python3 tools/verifier_schema_produit.py --json",
            "code_sortie": cli.returncode,
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/mesurer_schema_v2_doc.py')\nt=p.read_text(encoding='utf-8')\nold='''                \"meta.alternative\": [\"type\", \"debut\", \"fin\", \"source\", \"union\", \"relation\", \"rang\",\n                                     \"retir … [1566 caractères tronqués]`

  ```
ok
29:import re
  ```

- **bash** `{"command": "python3 tools/mesurer_schema_v2_doc.py --json 2>&1 | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['tests_schema']); print(d['documentation']['champs_documentes'])\"", "description": "Verify schema measure parse", "timeoutMs": 300000}`

  ```
{'commande': 'python3 tools/tests/test_schema_produit.py', 'code_sortie': 0, 'tests': 9, 'echecs': 0}
{'meta.partition': ['groupe', 'rang', 'membres', 'vue'], 'meta.alternative': ['type', 'debut', 'fin', 'source', 'union', 'relation', 'rang', 'retire (optionnel)', 'attachement (optionnel)', 'role (optionnel)'], 'meta.attachement.candidats': ['span', 'cible', 'source'], 'meta.role': 'vocabulaire fermé (8 rôles, sans accent)'}
  ```

- **bash** `{"command": "python3 tools/mesurer_schema_v2_doc.py >/tmp/mesurer-schema.log 2>&1; echo code=$?; tail -5 /tmp/mesurer-schema.log; git diff --stat reports/schema-v2-doc.json; git diff reports/schema-v2-doc.json | head -60", "description": "Regenerate schema v2 doc JSON", "timeoutMs": 300000}`

  ```
code=0
  612 annotations v2 (0 échec) · 612 annotations v1 (0 échec)
  vérificateur : 6 cas, 0 échec · versions lues [1, 2]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/schema-v2-doc.json
 reports/schema-v2-doc.json | 10 ++++++++--
 1 file changed, 8 insertions(+), 2 deletions(-)
diff --git a/reports/schema-v2-doc.json b/reports/schema-v2-doc.json
index a4142a65..c4f50099 100644
--- a/reports/schema-v2-doc.json
+++ b/reports/schema-v2-doc.json
@@ -30,7 +30,13 @@
     "retire (optionnel)",
     "attachement (optionnel)",
     "role (optionnel)"
-   ]
+   ],
+   "meta.attachement.candidats": [
+    "span",
+    "cible",
+    "source"
+   ],
+   "meta.role": "vocabulaire fermé (8 rôles, sans accent)"
   },
   "retrocompatibilite": {
    "v1_inchangee": true,
@@ -99,7 +105,7 @@
  "tests_schema": {
   "commande": "python3 tools/tests/test_schema_produit.py",
   "code_sortie": 0,
-  "tests": 8,
+  "tests": 9,
   "echecs": 0
  },
  "limites": [
  ```

- **bash** `{"command": "grep -n \"8 tests\\|deux champs\\|meta.partition.*meta.alternative\\|26 cas\" reports/rapport-schema-v2-doc.md | head -20", "description": "Check old schema report for stale numbers"}`

  ```
11:> `meta.partition`, les **dix** champs de `meta.alternative` (sept obligatoires, trois
14:> **6 cas / 0 échec** ; `--gold 20` donne **26 cas / 0 échec** ; les **612 phrases du gold**
46:python3 tools/tests/test_schema_produit.py            # 8 tests du contrat
51:`meta.partition` et `meta.alternative` ne sont présents que sur un **syntagme** qui appartient à
116:| vérificateur, gold 20 | `python3 tools/verifier_schema_produit.py --gold 20` | **26 cas, 0 échec** |
132:que deux champs **optionnels** dans `meta`. Un client v1 qui ne lit pas `meta` continue donc de
142:`meta.partition`/`meta.alternative` ; il passe le schéma v1, et le schéma v2 le refuse. C'est une
183:- [`docs/produit/README.md`](../docs/produit/README.md) — § 3.3 bis : les deux champs, l'exemple,
189:- [`tools/tests/test_schema_produit.py`](../tools/tests/test_schema_produit.py) — 8 tests du contrat.
  ```

- **bash** `{"command": "sed -n 1,60p reports/rapport-schema-v2-doc.md", "description": "Read old schema report head"}`

  ```
# J11.4 — le contrat : le schéma v2 documenté, 6 cas / 0 échec, v1 toujours lue

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **J11.4** · **Date** : 2026-11-14 ·
> **Verdict** : ✅
>
> **Commit mesuré** : `09e54143` — le code et les deux schémas sont inchangés ; cette fiche
> mesure le contrat existant et documente la notice produit.
>
> **Ce que cette fiche fixe.** Le schéma v2 est **documenté dans la notice**
> [`docs/produit/README.md`](../docs/produit/README.md) § 3.3 bis : les **quatre** champs de
> `meta.partition`, les **dix** champs de `meta.alternative` (sept obligatoires, trois
> optionnels), un exemple réel et la **rétro-compatibilité v1**. Vérification :
> `tools/verifier_schema_produit.py --json` lit **les deux versions** (`versions_lues: [1, 2]`),
> **6 cas / 0 échec** ; `--gold 20` donne **26 cas / 0 échec** ; les **612 phrases du gold**
> passent le schéma v2 (**612/612**) et les **612 annotations dérivées v1** passent le schéma v1
> (**612/612**). Contrôles négatifs : le schéma v2 refuse les 612 annotations v1, le schéma v1
> refuse les 612 annotations v2, et la mutation d'un champ obligatoire est refusée.
>
> **Dispositif** : [`drave-annotation-v1.json`
… [2117 caractères tronqués]
  ```

- **bash** `{"command": "git checkout -- reports/schema-v2-doc.json && git status --short reports/schema-v2-doc.json; git diff --stat reports/schema-v2-doc.json", "description": "Revert historical schema JSON"}`

  ```
(no output)
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-schema-v2-doc.md')\nt=p.read_text(encoding='utf-8')\nold='''> **Commit mesuré** : `09e54143` — le code et les deux schémas sont inchangés ; cette fiche\n> mesure le contrat existant et documente la notice produit.\n'''\ … [661 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sed -n 400,456p docs/pilotage/plan-travail.md", "description": "Read end of work plan"}`

  ```
`verifie_en_cours.py`, `taille_documents.py`, `verifie_journal.py`, `verifier_liens.py`,
`porte-tableaux.sh` ; la **passe complète** attend la fin des runs (règle § 11).

## 13. La tranche autonome du 05/11 (11 h 15 → 18 h) et ses sous-agents

**L'agent principal (Pensée, `e181ce02`) tient seul ce dossier** : `en-cours`, `roadmap`,
`chantiers`, ce plan et le `journal`. Les **sous-agents** ne les écrivent **jamais**.

| sous-agent | mandat | sortie (fichier neuf) |
|---|---|---|
| **A1** | audit de reproductibilité de l'attachement (labels, exact, top-k, conventions, spans) | une fiche d'audit + son JSON, dans `reports/` |
| **A2** | diagnostic du top-k strict (57 échecs) | une fiche de diagnostic + son JSON |
| **A3** | prototype de classement appris des candidats (fichier neuf, hors bloc) | un prototype dans `tools/tests/` + sa fiche |
| **A4** | cohérence fiches ↔ JSON ↔ portes | une fiche de cohérence + son JSON |

**Intégration (agent principal)** : pour chaque vague, l'agent principal (1) lit les fiches
rendues et vérifie qu'elles ne modifient aucun fichier hors de leur périmètre ; (2) rejoue
**lui-même** les mesures annoncées (une valeur non reproduite est rejetée) ; (3) n'in
… [2628 caractères tronqués]
  ```

- **bash** `{"command": "grep -n '\"T1\"\\|\"T2\"\\|empaquetage\\|contrat' tools/chantier/plan.json | head -20", "description": "Check plan.json for T2"}`

  ```
352:   "titre": "Le contrat — le schéma v2 documenté",
741:   "id": "T1",
743:   "titre": "L'empaquetage — pip install et la commande drave",
744:   "mandat": "Tâche T1 (exploitable, 1/5) : **l'empaquetage** — écris un **`pyproject.toml`** minimal (le nom `drave`, la version 0.1.0, le `requires-python >= 3.10`, **aucune dépendance**, le `console_scripts` `drave = tools.drave:main` ou un module d'entrée propre), vérifie `python3 -m pip install -e .` dans un **venv temporaire** (`/tmp/venv-drave`), puis `drave --version` et `drave analyser \"Le chat dort.\"` depuis un **autre répertoire** (pas la racine du dépôt) ; le contrôle négatif : sans install, `drave` doit échouer proprement. Fiche `reports/rapport-empaquetage.md` + JSON, un test dans `tools/tests/` (ou une note), et la doc `docs/produit/README.md` § 8.10 mise à jour (l'install). **Ne casse pas** `python3 tools/drave.py` (le chemin historique).",
752:     "commande": "test -f reports/rapport-empaquetage.md && echo FICHE-OK",
758:   "id": "T2",
760:   "titre": "Le contrat — les candidats structurés et les rôles normalisés",
761:   "mandat": "Tâche T2 (exploitable, 2/5) : **l'API du JSON** — (1) les `candidats` de l'attachement 
… [683 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 730,790p tools/chantier/plan.json", "description": "Read T1/T2 plan entries"}`

  ```
{
     "commande": "test -f reports/rapport-tagger-auto.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
    {
     "commande": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -1",
     "attendu": "OK"
    }
   ]
  },
  {
   "id": "T1",
   "jour": 19,
   "titre": "L'empaquetage — pip install et la commande drave",
   "mandat": "Tâche T1 (exploitable, 1/5) : **l'empaquetage** — écris un **`pyproject.toml`** minimal (le nom `drave`, la version 0.1.0, le `requires-python >= 3.10`, **aucune dépendance**, le `console_scripts` `drave = tools.drave:main` ou un module d'entrée propre), vérifie `python3 -m pip install -e .` dans un **venv temporaire** (`/tmp/venv-drave`), puis `drave --version` et `drave analyser \"Le chat dort.\"` depuis un **autre répertoire** (pas la racine du dépôt) ; le contrôle négatif : sans install, `drave` doit échouer proprement. Fiche `reports/rapport-empaquetage.md` + JSON, un test dans `tools/tests/` (ou une note), et la doc `docs/produit/README.md` § 8.10 mise à jour (l'install). **Ne casse pas** `python3 tools/drave.py` (le chemin historique).",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f pyproject.toml && echo PYPROJEC
… [2144 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(type(p), list(p)[:10])\nfor t in p.get('taches',[])[-10:]:\n    print(t.get('id'), t.keys())\nPY", "description": "Inspect plan structure"}`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
X1 dict_keys(['id', 'jour', 'titre', 'mandat', 'budget_min', 'acceptation'])
X2 dict_keys(['id', 'jour', 'titre', 'mandat', 'budget_min', 'acceptation'])
X3 dict_keys(['id', 'jour', 'titre', 'mandat', 'budget_min', 'acceptation'])
Y1 dict_keys(['id', 'jour', 'titre', 'mandat', 'budget_min', 'acceptation'])
T1 dict_keys(['id', 'jour', 'titre', 'mandat', 'budget_min', 'acceptation'])
T2 dict_keys(['id', 'jour', 'titre', 'mandat', 'budget_min', 'acceptation'])
T3 dict_keys(['id', 'jour', 'titre', 'mandat', 'budget_min', 'acceptation'])
T4 dict_keys(['id', 'jour', 'titre', 'mandat', 'budget_min', 'acceptation'])
T5 dict_keys(['id', 'jour', 'titre', 'mandat', 'budget_min', 'acceptation'])
T6 dict_keys(['id', 'jour', 'titre', 'mandat', 'budget_min', 'acceptation'])
  ```

- **bash** `{"command": "sed -n 84,95p docs/pilotage/en-cours.md; echo ---; sed -n 112,120p docs/pilotage/en-cours.md", "description": "Locate en-cours B13 lines"}`

  ```
## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles ; **19/19 verdicts `389b99f`** ; [v2](../../reports/rapport-coordination-s-v2.md).
- **N2 — en pause** : commande **`eval_longueurs.py --rope --val <dir>`** (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
- **L — le bloc langue** : contrat ; frontière script 1,0 / langue 0,137/0,9687 ; fusion réparée **0,9309/0,8226/0,8784/0,9954**.
- **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ; réseau coupé **code 0** + repli ; **143 870 tokens / 0,031 $** pour 1 000 ; [W2](../../reports/rapport-tagger-h50.md), [W3](../../reports/rapport-tagger-defaut.md).
- **Panini** : **14 atomes** ; 
… [2760 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/tests/test_empaquetage.py 2>&1 | tail -8", "description": "Verify T1 tests still pass"}`

  ```
test_identite_et_python (__main__.TestMetadonnees.test_identite_et_python) ... ok
test_pyproject_existe (__main__.TestMetadonnees.test_pyproject_existe) ... ok
test_script_console (__main__.TestMetadonnees.test_script_console) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.574s

OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\nt=p.read_text(encoding='utf-8')\nold='''- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports … [1676 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sed -n 150,165p docs/pilotage/roadmap.md", "description": "Read roadmap B13 next measure"}`

  ```
**J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag `chantier-2026-11-14`.** La
passe du **14/11 00 h 30** (`work/portes/passe-1311-23h15.log`) n'est **pas refaite** : les trois
rouges sont **revérifiées**. `porte-sessions` passe **verte** après la mise en pause du hub
`1e7ef596` et le rafraîchissement du heartbeat `e181ce02` ; `porte-indice` et `porte-melange`
restent **rouges structurelles** (mêmes causes : écart au témoin nul pour l'indice ; état de A qui
ne rend pas son code pour le mélange). Le tag annoté `chantier-2026-11-14` est posé sur le dernier
commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +
[`JSON`](../../reports/rapport-cloture-chantier.json).
**Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le
gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).

**La vue d'ensemble des chantiers** — huit chantiers (A, B, N, R, **S**, **L**, **D**, B13), leurs relations, leurs chemins critiques et les tensions à trancher — est dans [`chantiers.md`](chantiers.md) ; la carte est [`chantiers-vision.svg`](../s
… [250 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md')\nt=p.read_text(encoding='utf-8')\nold='''**Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le\ngold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).\n'''\nnew='''**Prochaine mesur … [802 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -60", "description": "Run documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 761 fiche(s) · 855 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 3 anomalie(s) :
     · fraîcheur : en-cours.md dit 2026-11-16, le dernier commit date du 2026-11-15
     · compteurs : en-cours.md dit 760 fichiers, le disque en a 761
     · compteurs : en-cours.md dit 854 JSON, le disque en a 855
  ```

- **bash** `{"command": "grep -n \"2026-11-16\\|11-16\" docs/pilotage/en-cours.md | head; head -3 docs/pilotage/en-cours.md; date +%Y-%m-%d", "description": "Find date mismatch"}`

  ```
3:**Mis à jour : 2026-11-16, 21 h 55 HNE (T1 : l'empaquetage)**
# En ce moment

**Mis à jour : 2026-11-16, 21 h 55 HNE (T1 : l'empaquetage)**
2026-11-15
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Get current date/time"}`

  ```
2026-11-15 22:03 EST
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\nt=p.read_text(encoding='utf-8')\nt=t.replace('**Mis à jour : 2026-11-16, 21 h 55 HNE (T1 : l\\'empaquetage)**',\n            '**Mis à jour : 2026-11-15, 22 h 03 HNE (T2 : l\\'API du JSON)**')\nt=t.replace(' … [306 caractères tronqués]`

  ```
ok
  revue de documentation · 761 fiche(s) · 855 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -20; echo code=${PIPESTATUS[0]}", "description": "Run table format gate", "timeoutMs": 300000}`

  ```
✅ 1837 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4636 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
code=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo code=$?; python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo code=$?", "description": "Check document size and state", "timeoutMs": 300000}`

  ```
2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2733    231   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4056 mots (budget 4 000)

  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/
… [255 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\nt=Path('docs/pilotage/en-cours.md').read_text(encoding='utf-8')\nfor line in t.splitlines():\n    if 'Produit — T2' in line or 'T2 — API JSON' in line:\n        print(len(line.split()), line)\nr=Path('docs/pilotage/roadmap.md').read_text(encod … [183 caractères tronqués]`

  ```
49 - **Produit — T2 (API JSON)** : candidats d'attachement en **objets** (`{span, cible, source}`) — **2 139** objets, **0** span faux, **1 295/1 295** attachements ; rôles normalisés **21 → 8**, **0** hors table, **711** prédicats (GV), **0** `prédicat` accentué ; schéma v2 **612/612**, v1 **612/612** ; [fiche](../../reports/rapport-contrat-json.md), [JSON](../../reports/contrat-json.json).
49 | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit (J11) ; T2 — API JSON (candidats objets, rôles 21 → 8)** | **`g017` tranché** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
roadmap line words 13
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\n# revert roadmap T2 paragraph\np=Path('docs/pilotage/roadmap.md')\nt=p.read_text(encoding='utf-8')\nold='''\n**T2 — l'API du JSON (15/11).** Les candidats d'attachement sont publiés en **objets**\n`{span, cible, source}` (`meta.attachement.can … [1836 caractères tronqués]`

  ```
ok
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4008 mots (budget 4 000)

  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4008 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "grep -n \"Produit — T2\" docs/pilotage/en-cours.md", "description": "Show T2 bullet"}`

  ```
90:- **Produit — T2** : objets **2 139**, **0** span faux ; rôles **21 → 8**, **0** hors table ; [fiche](../../reports/rapport-contrat-json.md), [JSON](../../reports/contrat-json.json).
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\nt=p.read_text(encoding='utf-8')\nold='''- **Produit — T2** : objets **2 139**, **0** span faux ; rôles **21 → 8**, **0** hors table ; [fiche](../../reports/rapport-contrat-json.md), [JSON](../../reports/con … [567 caractères tronqués]`

  ```
ok

  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4002 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\nt=p.read_text(encoding='utf-8')\nt=t.replace('**T2** : **2 139** objets, **0** span faux ; rôles **21 → 8** ;',\n            '**T2** : **2 139** objets ; rôles **21 → 8** ;',1)\np.write_text(t,encoding='utf … [139 caractères tronqués]`

  ```
ok
  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -10; echo ---; bash tools/porte-tableaux.sh 2>&1 | tail -5", "description": "Re-run documentation review and table gate", "timeoutMs": 300000}`

  ```
revue de documentation · 761 fiche(s) · 855 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---
  ✅ 1837 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4636 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "ls journal/2026-11-15/; echo ---; sed -n 1,80p journal/2026-11-15/README.md", "description": "Inspect today's journal"}`

  ```
distribue.md
docs.md
memoire.md
mesures.md
modele.md
outils.md
portes.md
README.md
---
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**47 commits** · **1 session(s)** · **7 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 8 | [distribue.md](distribue.md) |
| docs | 13 | [docs.md](docs.md) |
| memoire | 3 | [memoire.md](memoire.md) |
| mesures | 17 | [mesures.md](mesures.md) |
| modele | 3 | [modele.md](modele.md) |
| outils | 1 | [outils.md](outils.md) |
| portes | 2 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 365.2 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réel
… [7270 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -20; echo code=$?", "description": "Verify journal consistency", "timeoutMs": 120000}`

  ```
journal · 47 jour(s) · 218 session(s) · 2658 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
code=0
  ```

- **bash** `{"command": "grep -n \"notes\\|NOTE\\|T1\\|empaquetage\" journal/2026-11-15/README.md | tail -20; tail -60 journal/2026-11-15/README.md", "description": "Inspect journal notes section"}`

  ```
5:> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
82:<!-- notes -->
166:<!-- /notes -->
inchangée. **Le type d'abord** : les 42 types de de Bruijn sont **clos** (aucun indice hors portée)
et **bien formés** (`[] ⊢ type : sort n`, 38 en `sort 0`, 4 en `sort 1`), les 42 preuves sont closes.
Un type ouvert ou mal typé est refusé avant de servir de contrat. **L'empreinte ensuite** : `sha256`
est réécrit depuis **FIPS 180-4**, sans `hashlib` ; il retrouve le sha256 du fichier, les **42**
couples `preuve || type` et les **24** termes de l'environnement, **0 écart** avec `hashlib`. **Les
contrôles négatifs** : les **36/36** preuves altérées sont rejetées, les **42/42** types altérés
aussi (**36** deviennent invalides, **6** restent bien formés mais la preuve ne passe plus), les
**1 020/1 020** mutations de `eq(2,2)` sont rejetées, et un corpus corrompu (preuve ou type) sort en
**1**. La porte `tools/porte-cic.sh` et **21 + 17 = 38** tests rejouent le tout :
[`reports/rapport-cic-v2.md`](../../reports/rapport-cic-v2.md) et
[`reports/cic-verificateur-v2.json`](../../reports/cic-verificateur-v2.json).

### W2 — le tagger sur 402/H50 : il gagne sur les deux
… [3540 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('journal/2026-11-15/README.md')\nt=p.read_text(encoding='utf-8')\nold='''[`fiche`](../../reports/rapport-tagger-lot.md) · [`JSON`](../../reports/rapport-tagger-lot.json).\n<!-- /notes -->\n'''\nnew='''[`fiche`](../../reports/rapport-tag … [1592 caractères tronqués]`

  ```
ok
  journal · 47 jour(s) · 218 session(s) · 2661 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "git status --short | head -80; echo ---; git diff --stat | tail -40", "description": "Review working tree"}`

  ```
M .gitignore
 M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M docs/produit/exemples.md
MM journal/2026-11-15/README.md
M  journal/2026-11-15/distribue.md
M  journal/2026-11-15/docs.md
M  journal/2026-11-15/memoire.md
M  journal/2026-11-15/mesures.md
M  journal/2026-11-15/modele.md
M  journal/2026-11-15/outils.md
M  journal/2026-11-15/portes.md
M  journal/README.md
M  journal/sessions/MANIFEST.md
M  journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
M  journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
A  journal/sessions/session-8217267f-fd89-462c-8112-cba3ba9877b3/digest.md
A  journal/sessions/session-8217267f-fd89-462c-8112-cba3ba9877b3/rapport.md
A  journal/sessions/session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f/digest.md
A  journal/sessions/session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f/rapport.md
 M reports/faq.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-faq.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-schema-v2-doc.md
 M reports/rappor
… [1973 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached --stat | tail -20", "description": "Inspect staged changes"}`

  ```
journal/2026-11-15/README.md                       |    7 +-
 journal/2026-11-15/distribue.md                    |    5 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/memoire.md                      |    2 +-
 journal/2026-11-15/mesures.md                      |    2 +-
 journal/2026-11-15/modele.md                       |    2 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    4 +-
 journal/sessions/MANIFEST.md                       |    6 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  248 ++
 .../rapport.md                                     |  115 +-
 .../digest.md                                      | 2567 ++++++++++++++++++++
 .../rapport.md                                     |  168 ++
 .../digest.md                                      | 2059 ++++++++++++++++
 .../rapport.md                                     |  126 +
 16 files changed, 5295 insertions(+), 22 deletions(-)
  ```

- **bash** `{"command": "bash tools/porte-produit.sh 2>&1 | tail -30", "description": "Run product gate", "timeoutMs": 900000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f6355d8175a75854 deux fois
  ✅ smoke test : Ran 24 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
  ```

- **bash** `{"command": "bash tools/porte-bloc-linguistique.sh 2>&1 | tail -20", "description": "Run language block gate", "timeoutMs": 900000}`

  ```
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

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --gold 20 2>&1 | tail -12; echo ---; python3 tools/revue_documentation.py 2>&1 | tail -5", "description": "Validate schema on gold and review docs", "timeoutMs": 300000}`

  ```
✅ gold:g014 (v2)
  ✅ gold:g015 (v2)
  ✅ gold:g016 (v2)
  ✅ gold:g017 (v2)
  ✅ gold:g018 (v2)
  ✅ gold:g019 (v2)
  ✅ gold:g020 (v2)
  ✅ rétro-compatibilité : annotation v1 lue par le schéma v1
  ✅ contrôle négatif : le schéma v2 refuse une annotation v1
  ✅ contrôle négatif : le schéma v2 refuse un rôle hors vocabulaire
  ✅ contrôle négatif : le schéma v2 refuse un candidat chaîne
  ✅ validateur JSON Schema · 26 cas
---
  revue de documentation · 761 fiche(s) · 855 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -3; python3 tools/verifie_en_cours.py 2>&1 | tail -2; python3 tools/verifie_journal.py 2>&1 | tail -2; python3 tools/verifier_schemas.py 2>&1 | tail -4", "description": "Run state, journal, schema checks", "timeoutMs": 300000}`

  ```
· 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  journal · 47 jour(s) · 218 session(s) · 2661 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  schémas · 464 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "git diff -- tools/bloc_linguistique.py tools/drave.py tools/verifier_schema_produit.py tools/tests/test_produit.py tools/tests/test_schema_produit.py | sed -n 1,260p", "description": "Review code diff part 1"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index edb29e19..eb703168 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -49,8 +49,14 @@ from typing import Protocol, Sequence
 RACINE = pathlib.Path(__file__).resolve().parent.parent
 try:  # paquet : `tools.bloc_linguistique`
     from . import roles_gp as _roles_gp
+    from .roles_vocabulaire import (ROLES as ROLES_NORMALISES,
+                                    RoleHorsVocabulaire,
+                                    normaliser_role as _normaliser_role)
 except ImportError:  # script : `python3 tools/bloc_linguistique.py`
     import roles_gp as _roles_gp
+    from roles_vocabulaire import (ROLES as ROLES_NORMALISES,
+                                   RoleHorsVocabulaire,
+                                   normaliser_role as _normaliser_role)
 NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
            "pragmatique", "document")
 SOURCES = ("heuristique", "neuronal", "humain")
@@ -88,10 +94,31 @@ class Etiquette:
             "debut": self.debut, "fin": self.fin, "source": self.source,
             "confiance": round(float(self.confiance), 4),
… [12891 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/porte-bloc-code.sh | head -80", "description": "Inspect code gate for lint"}`

  ```
#!/bin/bash
# porte-bloc-code.sh — R4.2 : un code lu est un AST exécuté, et l'AST se vérifie.
#
# POURQUOI CETTE PORTE EXISTE. Un document de code n'est pas de la prose : la réponse à
# « que vaut cette expression ? » est dans l'EXÉCUTION, pas dans la ligne. R0.1 range le
# code en région et le texte reste du texte ; le banc R0.3 demande des valeurs par deux
# mots rares, ce qui mesure la recherche d'une ligne, pas la compréhension. Cette porte
# exige donc les trois choses ensemble : le PARSEUR (tout le corpus accepté), la PORTÉE
# (chaque nom rattaché à sa portée), l'EXÉCUTION EN SABLE (liste blanche, bornes) — plus
# le contrôle négatif « texte seul » qui doit ÉCHOUER.
#
# Ce qu'elle ne vérifie PAS : la sémantique d'un langage hors Python ; les bibliothèques
# (aucun import n'est exécuté) ; l'intention du code (c'est le modèle, et R0.3 le mesure).
#
# Usage : tools/porte-bloc-code.sh
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R4.2 — LE BLOC CODE ==="
python3 tools/bloc_code.py --porte
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte bloc code verte" || echo "❌ porte bloc code ROUGE (code $CODE)"
exit "$CODE"
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/bloc_linguistique.py')\nt=p.read_text(encoding='utf-8')\nold='''try:  # paquet : `tools.bloc_linguistique`\n    from . import roles_gp as _roles_gp\n    from .roles_vocabulaire import (ROLES as ROLES_NORMALISES,\n                 … [986 caractères tronqués]`

  ```
ok
predicat
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/bloc_linguistique.py')\nt=p.read_text(encoding='utf-8')\nold='''            debut = texte.find(v)\n            if debut < 0:\n                debut = texte.casefold().find(v.casefold())\n            if debut < 0:\n                … [478 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"\\[\\\"role\\\"\\]\\|e\\['role'\\]\\|role_normalise\" tools/restitution_v2.py | sed -n 1,60p", "description": "Inspect restitution role usage"}`

  ```
82:            "role_normalise": normaliser_role(meta.get("role", "")),
151:        "agent_role": agent["role"] if agent else "",
153:        "lieu_role": lieu["role"] if lieu else "",
172:        if e["role_normalise"] != "predicat":
182:    agents = [e for e in segments if e["role_normalise"] == "agent"]
183:    lieux = [e for e in segments if e["role_normalise"] == "lieu"]
185:               and e["role_normalise"] in ("", "groupe nominal")]
209:    roles_segments = [e for e in segments if e["role_normalise"] in ROLES]
210:    autres = [e for e in segments if e["role_normalise"] not in ROLES]
219:            f"{e['role'] or e['type']}: {_valeur_lisible(e['valeur'])}" for e in autres))
223:            f"  {i:2}. {e['type']}/{e['role'] or '—'} [{e['debut']}:{e['fin']}] "
235:            "agents": sum(1 for e in segments if e["role_normalise"] == "agent"),
236:            "predicats": sum(1 for e in segments if e["role_normalise"] == "predicat"),
237:            "lieux": sum(1 for e in segments if e["role_normalise"] == "lieu"),
383:        if e["role_normalise"] not in ROLES:
790:                if normaliser_role(meilleur[2]["role"]) == normaliser_role(attendu["role"]):
793:     
… [32 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/mesurer_contrat_json.py 2>&1 | tail -8", "description": "Regenerate T2 measurement JSON", "timeoutMs": 300000}`

  ```
phrases 612 · segments 1883 · rôles 1883
  candidats : 2139 objets (1295/1295 attachements) · spans faux 0
  rôles : 21 bruts → 8 normalisés · hors table 0 · hors vocabulaire 0
  contrôle négatif : filtre predicat 711 (711 GV) · prédicat accentué 0 · rôle inconnu levé True
  validation : v2 0 échec(s), v1 0 échec(s)
  écrit : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/contrat-json.json
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -5; python3 tools/tests/test_schema_produit.py 2>&1 | tail -5; python3 tools/verifier_schema_produit.py >/dev/null 2>&1; echo verifier=$?", "description": "Re-run product and schema tests", "timeoutMs": 300000}`

  ```
........................
----------------------------------------------------------------------
Ran 24 tests in 13.728s

OK

----------------------------------------------------------------------
Ran 9 tests in 1.557s

OK
verifier=0
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/test_bloc_linguistique.py 2>&1 | tail -4; python3 tools/tests/test_restitution_v2.py 2>&1 | tail -4", "description": "Re-run block and restitution tests", "timeoutMs": 300000}`

  ```
----------------------------------------------------------------------
Ran 20 tests in 0.084s

OK
----------------------------------------------------------------------
Ran 17 tests in 1.511s

OK
  ```

- **bash** `{"command": "git diff -- docs/produit/README.md | sed -n 1,260p", "description": "Review product README diff"}`

  ```
diff --git a/docs/produit/README.md b/docs/produit/README.md
index 184a7c11..7f371b1e 100644
--- a/docs/produit/README.md
+++ b/docs/produit/README.md
@@ -59,14 +59,16 @@ un serveur. Le produit **lit** et **étiquette** ; il n'écrit pas de texte.
 Une seule opération : `analyser(texte, langue)` → une **annotation**. Elle porte neuf niveaux ;
 le produit en expose cinq, plus le coût et la trace. Le JSON est estampillé `schema`
 (`"drave.annotation"`) et `version` (`2`) ; en v2, `meta.partition` et `meta.alternative`
-documentent les syntagmes qui se chevauchent.
+documentent les syntagmes qui se chevauchent, `meta.attachement.candidats` publie les
+candidats en **objets** `{span, cible, source}`, et `meta.role` appartient à un
+**vocabulaire fermé** de huit rôles.
 
 | ce que vous demandez | ce que vous obtenez | mesure du 15/11 |
 |---|---|---|
 | **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; le CLI n'expose que `fr`/`en` comme indice) |
 | **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger
… [13618 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/verifier_schema_produit.py')\nt=p.read_text(encoding='utf-8')\nold='''CAS = [\n'''\nnew='''try:  # script : `python3 tools/verifier_schema_produit.py`\n    from roles_vocabulaire import ROLES as ROLES_VOCABULAIRES\nexcept ImportE … [3195 caractères tronqués]`

  ```
ok
verifier=0
role True
candidat True
valide []
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/mesurer_contrat_json.py')\nt=p.read_text(encoding='utf-8')\nt=t.replace('import pathlib\\nimport subprocess', 'import pathlib\\nimport re\\nimport subprocess',1)\nold='''        \"tests\": {\n            \"test_produit\": {\"code … [1497 caractères tronqués]`

  ```
ok
  phrases 612 · segments 1883 · rôles 1883
  candidats : 2139 objets (1295/1295 attachements) · spans faux 0
  rôles : 21 bruts → 8 normalisés · hors table 0 · hors vocabulaire 0
  contrôle négatif : filtre predicat 711 (711 GV) · prédicat accentué 0 · rôle inconnu levé True
  validation : v2 0 échec(s), v1 0 échec(s)
  écrit : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/contrat-json.json
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/contrat-json.json'))\nprint(d['tests'])\nPY", "description": "Check parsed test counts"}`

  ```
{'test_produit': {'code': 0, 'tests': 24, 'echecs': 0}, 'test_schema_produit': {'code': 0, 'tests': 9, 'echecs': 0}}
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; python3 tools/taille_documents.py 2>&1 | tail -2", "description": "Re-run doc checks", "timeoutMs": 300000}`

  ```
revue de documentation · 761 fiche(s) · 855 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -4; python3 tools/tests/test_schema_produit.py 2>&1 | tail -4", "description": "Final product tests", "timeoutMs": 300000}`

  ```
----------------------------------------------------------------------
Ran 24 tests in 13.522s

OK
----------------------------------------------------------------------
Ran 9 tests in 1.420s

OK
  ```

- **bash** `{"command": "git diff -- reports/faq.json | head -60; echo ---; git diff -- tools/verifier_faq.py | head -60", "description": "Inspect FAQ changes for T1 relation"}`

  ```
diff --git a/reports/faq.json b/reports/faq.json
index 4d72b66a..2abcf281 100644
--- a/reports/faq.json
+++ b/reports/faq.json
@@ -264,8 +264,12 @@
      "--sortie",
      "parcours de répertoire",
      "rejeu d'une annotation sauvegardée",
-     "pip install"
+     "publication PyPI"
     ],
+    "empaquetage": {
+     "livre": "pip install -e . + commande drave",
+     "non_livre": "wheel / paquet PyPI"
+    },
     "options_fantomes": {
      "--sortie": "code 2",
      "--mode": "code 2",
@@ -299,14 +303,23 @@
      "sans_site_packages": "code 0"
     },
     "dependances_externes": 0,
-    "empaquetage": "aucun (pas de pip install, pas de commande drave dans le PATH)",
+    "empaquetage": {
+     "fichier": "pyproject.toml",
+     "nom": "drave",
+     "version": "0.1.0",
+     "requires_python": ">=3.10",
+     "dependances": [],
+     "script_console": "drave = tools.drave:main",
+     "installation": "python3 -m pip install -e . (venv)",
+     "hors_depot": "commande drave depuis n'importe quel répertoire"
+    },
     "gold_versionnes": [
      "gold.json",
      "gold_gele.json",
      "gold_reel.json",
      "gold_synthetique.json"
     ],
-    "racine": "tout part de l
… [3352 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"candidats\\|role\\|rôles\" tools/verifier_faq.py | head -40; echo ---; sed -n 300,360p tools/verifier_faq.py", "description": "Inspect FAQ verifier role/candidate claims"}`

  ```
6:code. Ce vérificateur exécute les dix contrôles, imprime un JSON (ou un résumé) et sort
66:# ------------------------------------------------------------------ les dix contrôles
178:        "change": {"pos": "API", "syntagmes": "heuristique", "roles": "heuristique",
218:    """L'attachement : 238/239, exact sur les spans prédits, contrôles négatifs durs."""
226:    assert d["controle_negatif"]["exact_taux"] == 0.0167, d["controle_negatif"]
228:    audit = _lire("reports/pensee-audit-v10.json")["controle_negatif"]
234:        "controle_cli": {"cible_au_hasard": 0.0167},
235:        "controle_audit_v10": {"candidat_aleatoire_top1": 0.4214,
274:    """Trois vues : surface exacte, forme canonique, rôles lisibles mais peu fidèles."""
280:    assert s0["controle_negatif"]["detectes"] == 46, s0["controle_negatif"]
289:    v2 = _json(["restituer", "--banc", banc, "--roles"])
292:    assert s2["roles"]["f1"] == 0.527, s2["roles"]
293:    assert s2["controles"]["rendu"]["exacts"] == 46, s2["controles"]["rendu"]
294:    assert s2["controles"]["spans_dans_source"] == {"justes": 198, "total": 198,
295:                                                    "taux": 1.0}, s2["controles"]
297:    un
… [4735 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 430,520p tools/verifier_faq.py", "description": "Read FAQ verifier main"}`

  ```
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
            ok = False
            erreur = f"{type(exc).__name__} : {exc}"
        questions.append({"id": ident, "question": question, "observe": observe,
                          "ok": ok, "erreur": erreur})
    negatif = controle_negatif()
    return {
        "schema": "drave.faq.verification",
        "version": 1,
        "date": DATE,
        "produit": VERSION,
        "fichier": FAQ,
        "questions": questions,
        "controle_negatif": negatif,
        "ok": all(q["ok"] for q in questions) and negatif["detecte"],
    }


def _resume(rapport: dict) -> str:
    lignes = [f"FAQ produit — {sum(q['ok'] for q in rapport['questions'])}/10 réponses "
              f"vérifiées · contrôle négatif "
            
… [1287 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,70p tools/verifier_faq.py", "description": "Read FAQ verifier imports"}`

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
… [1351 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/verifier_faq.py')\nt=p.read_text(encoding='utf-8')\nold='''    # Les rôles ne sont pas normalisés : les deux chemins du bloc n'écrivent pas pareil.\n    bloc = (RACINE / \"tools/bloc_linguistique.py\").read_text(encoding=\"utf-8\ … [4464 caractères tronqués]`

  ```
ok
FAQ produit — 10/10 réponses vérifiées · contrôle négatif détecté
  ✅  1. Quelles langues le produit reconnaît-il ?
  ✅  2. Est-ce que ça marche hors ligne ?
  ✅  3. Combien ça coûte ?
  ✅  4. Qu'est-ce que --tagger change ?
  ✅  5. Quel est le format de sortie, et est-il stable ?
  ✅  6. Que veut dire « attachement », et à quel point est-il fiable ?
  ✅  7. Pourquoi reste-t-il un span inatteignable ?
  ✅  8. Que peut-on restituer : la surface, la forme, les rôles ?
  ✅  9. Quelles limites faut-il connaître avant de s'en servir ?
  ✅ 10. Comment l'installer et le lancer ?
✅ FAQ vérifiée
code=0
  ```

- **bash** `{"command": "grep -rn \"faq.json\\|rapport-faq\" tools/*.py | head -20", "description": "Find FAQ report generator"}`

  ```
tools/verifier_faq.py:14:    python3 tools/verifier_faq.py --json     # le JSON de reports/faq.json
tools/verifier_faq.py:490:    parseur.add_argument("--json", action="store_true", help="le JSON de reports/faq.json")
  ```

- **bash** `{"command": "grep -n \"candidat\\|rôle\\|role\\|normalis\" reports/rapport-faq.md | head -30", "description": "Find Q9 claims in FAQ report"}`

  ```
5:> **contrôle négatif détecté** (deux affirmations fausses sont rejetées par le code).
14:> un JSON de `reports/`, et **dix contrôles exécutables** les rejouent. Les dix passent. Le
15:> contrôle négatif est explicite : le CLI **refuse** `--langue de` (code 2) et le schéma v2
20:> de rôles exacts (dont **16** non vides), **F1 0,5270** ; **609 appels**, **22 299 tokens**,
23:> **Dispositif** : [`tools/verifier_faq.py`](../tools/verifier_faq.py) (les dix contrôles, le
24:> contrôle négatif, `--json`), [`docs/produit/README.md`](../docs/produit/README.md) § 8 (la
48:La FAQ **ne prouve pas** que le tagger est bon, que les rôles sont justes ou que le produit
54:| # | question | réponse (chiffre vérifié) | contrôle |
70:python3 tools/verifier_faq.py            # résumé : 10/10 + contrôle négatif
72:python3 tools/verifier_faq.py --autotest # vérifie que le contrôle négatif échoue bien
82:valeurs réellement lues), `ok` et `erreur` (vide si tout passe). Le champ `controle_negatif`
87:| contrôle | valeur observée |
97:| contrôles négatifs | cible au hasard **0,0167** ; candidat aléatoire **0,4214** ; permutation **0,00908** |
99:| restitution v0 | **46/46** surfaces, miroir strict **0,1087*
… [625 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 54,70p reports/rapport-faq.md; sed -n 87,104p reports/rapport-faq.md", "description": "Read FAQ report table"}`

  ```
| # | question | réponse (chiffre vérifié) | contrôle |
|---:|---|---|---|
| 1 | **Quelles langues ?** | détection `de`/`es`, `und` sous le seuil ; `--langue` limité à `fr`/`en` ; `--langue de` → code 2 ; 398 profils UDHR (0,9687) | `q1_langue` |
| 2 | **Hors ligne ?** | socket interdite : analyse code 0 ; module réseau non importé ; `--tagger` sans clé → code 4, `stdout` vide | `q2_hors_ligne` |
| 3 | **Combien ça coûte ?** | défaut : 0 $ d'API ; tagger : **609 appels**, **22 299 tokens**, **155 s**, **~0,02 $** ; 3 exemples : **441 tokens**, **3,7 s** | `q3_cout` |
| 4 | **Que change `--tagger` ?** | POS seul : **95,75 %** contre **86,25 %** (612) ; **95,00 %** contre **88,91 %** (réel 452) ; ponctuation **25/25** | `q4_tagger` |
| 5 | **Quel schéma ?** | `drave.annotation` **v2**, v1 lue ; **6 cas**, **26** avec `--gold 20`, **0 échec** ; v2 refuse v1 | `q5_schema` |
| 6 | **L'attachement ?** | **238/239** cibles (**0,9958**) ; **1,0000** sur les spans prédits ; top-k **0,9874** ; hasard **1,67 %** ; audit **42,14 %** / **0,908 %** | `q6_attachement` |
| 7 | **Les spans inatteignables ?** | **1** : `g017`, SUB **[9:28]** attendue / **[9:38]** prédite ; règle rejetée (F1 **0,7901
… [2216 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifier_faq.py --json > reports/faq.json && python3 -m json.tool reports/faq.json >/dev/null && echo ok; grep -n \"candidats\\|vocabulaire\\|normalisés\" reports/faq.json | head -10", "description": "Regenerate FAQ JSON", "timeoutMs": 300000}`

  ```
ok
278:    "candidats": {
290:     "vocabulaire": [
301:     "lecture": "rôles normalisés, sans accents mélangés"
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; bash tools/porte-tableaux.sh 2>&1 | tail -4", "description": "Doc review and table gate after FAQ", "timeoutMs": 300000}`

  ```
revue de documentation · 761 fiche(s) · 855 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ✅ 1837 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4636 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "python3 tools/verifier_faq.py >/dev/null 2>&1; echo faq=$?; python3 tools/verifier_schema_produit.py >/dev/null 2>&1; echo schema=$?; python3 tools/tests/test_produit.py 2>&1 | tail -3", "description": "Run FAQ, schema, product tests", "timeoutMs": 300000}`

  ```
faq=0
schema=0
Ran 24 tests in 13.733s

OK
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -3; python3 tools/taille_documents.py 2>&1 | tail -2; python3 tools/verifie_journal.py 2>&1 | tail -2", "description": "Final state checks", "timeoutMs": 300000}`

  ```
en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  journal · 47 jour(s) · 218 session(s) · 2661 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "git diff -- .gitignore; echo ---; git diff --stat -- pyproject.toml tools/tests/test_empaquetage.py reports/rapport-empaquetage.md reports/empaquetage.json 2>/dev/null", "description": "Inspect T1 file changes"}`

  ```
diff --git a/.gitignore b/.gitignore
index e85c4a81..7937dc3f 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,5 +1,8 @@
 __pycache__/
 *.pyc
+*.egg-info/
+/build/
+/dist/
 reports/*.tmp
 models/
 data/
---
  ```

- **bash** `{"command": "git reset >/dev/null 2>&1 || true\ngit add \\\n  .gitignore pyproject.toml tools/tests/test_empaquetage.py reports/rapport-empaquetage.md reports/empaquetage.json \\\n  reports/faq.json reports/rapport-faq.md tools/verifier_faq.py \\\n  tools/roles_vocabulaire.py tools/bloc_linguistique … [507 caractères tronqués]`

  ```
.gitignore                             |   3 +
 docs/pilotage/en-cours.md              |   8 +-
 docs/produit/README.md                 | 131 ++++++++++---
 docs/produit/exemples.md               |   8 +-
 journal/2026-11-15/README.md           |  25 ++-
 pyproject.toml                         |  16 ++
 reports/contrat-json.json              | 301 ++++++++++++++++++++++++++++++
 reports/empaquetage.json               | 124 ++++++++++++
 reports/faq.json                       |  46 ++++-
 reports/rapport-contrat-json.md        | 220 ++++++++++++++++++++++
 reports/rapport-empaquetage.md         | 183 ++++++++++++++++++
 reports/rapport-faq.md                 |   6 +-
 reports/rapport-schema-v2-doc.md       |   5 +
 tools/bloc_linguistique.py             | 125 +++++++++++--
 tools/drave.py                         |   2 +-
 tools/mesurer_contrat_json.py          | 331 +++++++++++++++++++++++++++++++++
 tools/mesurer_schema_v2_doc.py         |   8 +-
 tools/roles_vocabulaire.py             | 117 ++++++++++++
 tools/schemas/drave-annotation-v2.json | 129 ++++++++++++-
 tools/tests/test_empaquetage.py        | 119 ++++++++++++
 tools/tests/test_produit.py            |  78 ++++++++
 tools
… [206 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached -- journal/2026-11-15/README.md | sed -n 1,80p; echo ---; git diff --cached -- reports/rapport-faq.md | head -40", "description": "Inspect staged journal/FAQ diffs"}`

  ```
diff --git a/journal/2026-11-15/README.md b/journal/2026-11-15/README.md
index 56c740f8..3ad1543b 100644
--- a/journal/2026-11-15/README.md
+++ b/journal/2026-11-15/README.md
@@ -5,13 +5,13 @@
 > le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
 > [l'index des sessions](../README.md#sessions).
 
-**46 commits** · **1 session(s)** · **7 thème(s)**
+**47 commits** · **1 session(s)** · **7 thème(s)**
 
 ## Thèmes du jour
 
 | thème | commits | fichier |
 |---|---|---|
-| distribue | 7 | [distribue.md](distribue.md) |
+| distribue | 8 | [distribue.md](distribue.md) |
 | docs | 13 | [docs.md](docs.md) |
 | memoire | 3 | [memoire.md](memoire.md) |
 | mesures | 17 | [mesures.md](mesures.md) |
@@ -23,7 +23,7 @@
 
 | session | titre | début | durée | liens |
 |---|---|---|---|---|
-| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 358.4 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |
+| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 
… [4404 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached --check; echo code=$?", "description": "Check staged diff whitespace"}`

  ```
code=0
  ```

- **bash** `{"command": "git commit -m \"T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)\" 2>&1 | tail -20", "description": "Commit T1/T2 result"}`

  ```
[still running after 60000ms; moved to background job bash-181]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-181", "wait": true, "timeout_ms": 180000}`

  ```
✅ index : aucun fait stagé sans état
[s/v7 7f1519f7] T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
 39 files changed, 9312 insertions(+), 107 deletions(-)
 create mode 100644 journal/sessions/session-8217267f-fd89-462c-8112-cba3ba9877b3/digest.md
 create mode 100644 journal/sessions/session-8217267f-fd89-462c-8112-cba3ba9877b3/rapport.md
 create mode 100644 journal/sessions/session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f/digest.md
 create mode 100644 journal/sessions/session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f/rapport.md
 create mode 100644 pyproject.toml
 create mode 100644 reports/contrat-json.json
 create mode 100644 reports/empaquetage.json
 create mode 100644 reports/rapport-contrat-json.md
 create mode 100644 reports/rapport-empaquetage.md
 create mode 100644 tools/mesurer_contrat_json.py
 create mode 100644 tools/roles_vocabulaire.py
 create mode 100644 tools/tests/test_empaquetage.py
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "git status --short | head -40; echo ---; git show --stat --oneline HEAD | head -50", "description": "Check post-commit state"}`

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
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
---
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
 .gitignore                                         |    3 +
 docs/pilotage/en-cours.md                          |    8 +-
 docs/produit/README.md                             |  131 +-
 docs/produit/exemples.md                           |    8 +-
 journal/2026-11-15/README.md                       |   25 +-
 journal/2026-11-15/distribue.md                    |    5 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/memoire.md                      |    2 +-
 journal/2026-11-15/mesures.md                      |    2 +-
 journal/2026-11-15/modele.md                       |    2 +-

… [1872 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -10; echo code=$?; python3 tools/revue_documentation.py 2>&1 | tail -5", "description": "Post-commit journal and docs checks", "timeoutMs": 300000}`

  ```
journal · 47 jour(s) · 218 session(s) · 2661 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
code=0
  revue de documentation · 761 fiche(s) · 855 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "git log -1 --format='%h %cd %s' --date=format:'%Y-%m-%d %H:%M'", "description": "Show last commit date"}`

  ```
7f1519f7 2026-11-15 22:12 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
  ```

- **bash** `{"command": "test -f reports/rapport-contrat-json.md && echo FICHE-OK; python3 tools/tests/test_produit.py 2>&1 | tail -1", "description": "Run T2 acceptance commands", "timeoutMs": 300000}`

  ```
FICHE-OK
OK
  ```

- **bash** `{"command": "python3 tools/mesurer_contrat_json.py --json 2>/dev/null | python3 -c \"import json,sys; d=json.load(sys.stdin); print('candidats', d['candidats']['objets'], 'spans_faux', d['candidats']['spans_faux']); print('roles', d['vocabulaire_roles']['bruts_distincts'], '->', d['vocabulaire_roles … [309 caractères tronqués]`

  ```
candidats 2139 spans_faux 0
roles 21 -> 8 hors 0
predicats 711 accent 0
  ```

### 🤖 Assistant

## T2 livré — l’API du JSON

**Commit** : `7f1519f7` (T1/T2 ; T1 était déjà dans l’arbre de travail).

### 1. Candidats d’attachement en objets

- Nouveau champ v2 : **`meta.attachement.candidats`**, liste d’objets `{span, cible, source}`.
- `span` = `{debut, fin}` et vérifie `texte[debut:fin] == cible`.
- La **cible choisie** est toujours le premier objet ; les cibles introuvables dans le texte sont écartées.
- Le champ historique `candidats` de l’étiquette reste une liste de **chaînes** : sortie lisible et contrat v1 inchangés.
- `meta.alternative[].attachement` recopie les mêmes objets.
- Schéma v2 étendu, **v1 toujours lue**.

**Mesure sur le gold 612** : **1 295/1 295** attachements avec objets, **2 139** objets, **1 062** dans les alternatives, **0 span faux**, **1 295/1 295** cibles choisies présentes.

### 2. Rôles normalisés

Vocabulaire fermé : **`predicat`, `agent`, `objet`, `lieu`, `temps`, `qualite`, `possesseur`, `destinataire`**.

- Table de **31 correspondances** dans [`tools/roles_vocabulaire.py`](tools/roles_vocabulaire.py).
- `normaliser_role` strict : un rôle inconnu lève `RoleHorsVocabulaire`.
- Normalisation appliquée au JSON (`meta.role`, `meta.alternative[].role`) et à la sortie lisible du CLI ; l’objet Python interne garde la forme brute pour les règles et l’autotest.

**Mesure sur le gold 612** : **21 rôles bruts → 8**, **0 hors table**, **0 hors vocabulaire**.

### 3. Contrôle négatif demandé

Un filtre `role == "predicat"` trouve **711 prédicats, tous des GV**.  
Un filtre `role == "prédicat"` trouve **0** segment.  
Un rôle inventé (`role_invente`) est refusé.  
Un candidat ramené à une chaîne, ou privé de `span`, est refusé par le schéma v2.

### 4. Tests et docs

- [`tools/tests/test_produit.py`](tools/tests/test_produit.py) : **24 tests OK** (4 nouveaux tests T2).
- [`tools/tests/test_schema_produit.py`](tools/tests/test_schema_produit.py) : **9 tests OK**.
- `verifier_schema_produit.py` : **26 cas, 0 échec**, plus les nouveaux contrôles négatifs.
- **Portes vertes** : `porte-produit`, `porte-bloc-linguistique`, `revue_documentation`, `porte-tableaux`, `taille_documents`, `verifie_en_cours`, `verifie_journal`, `verifier_schemas`.
- Docs mises à jour : [`docs/produit/README.md`](docs/produit/README.md) § 2/3.2/3.3 bis/4/7/8, [`docs/produit/exemples.md`](docs/produit/exemples.md).
- Fiche : [`reports/rapport-contrat-json.md`](reports/rapport-contrat-json.md) · JSON : [`reports/contrat-json.json`](reports/contrat-json.json) · banc : [`tools/mesurer_contrat_json.py`](tools/mesurer_contrat_json.py).

### 5. Limites nommées

La normalisation **ne raffine pas** le rôle : `objet` regroupe `patient`, `complément`, `contenu`, `theme`, `groupe nominal` ; `qualite` regroupe `attribut`, `maniere`, `concession`, `hypothese`, `cause`, `consequence`. Le `span` d’un candidat est sa **première occurrence** dans le texte, pas une résolution d’anaphore. Ces limites sont dans la fiche, avec ce qui pourrait rendre le résultat faux.

Les modifications préexistantes hors périmètre (`reports/pensee-*`, `tools/chantier/plan.json`, etc.) n’ont pas été touchées.

