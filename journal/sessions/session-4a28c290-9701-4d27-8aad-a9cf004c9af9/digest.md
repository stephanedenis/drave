# Session DSH — relecture

- identifiant : `session-4a28c290-9701-4d27-8aad-a9cf004c9af9`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-13 21:38:40
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J4.1 : la coordination N2 — le mètre `eval_n2_propre.py` lit les checkpoints RoPE comme des positions absolues (8,02 au lieu de 2,79). **Ne modifie rien dans N2** (ni `entrainer_native.py`, ni `native_model.py`, ni `work/`). Écris une fiche de coordination `reports/rapport-coordination-n2.md` + JSON : le bug, le correctif proposé (--rope), les chiffres, la commande exacte pour la session N2.

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

- **bash** `{"command": "ls", "description": "List repository root"}`

  ```
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
  ```

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --short | head -50; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet log --oneline -10", "description": "Show git status and recent commits"}`

  ```
M docs/pilotage/references-non-regression.md
D  journal/2026-11-13/README.md
D  journal/2026-11-13/docs.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/digest.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 m tools/structures
?? journal/2026-11-13/
?? reports/rapport-s-paragraphes.md
ced21933 CHANTIER — PHASE 2 (12 H) : LE VERDICT ACCEPTATION D'ABORD (TIMEOUT APRÈS COMMIT = FAIT), 12 TÂCHES AJOUTÉES (J4 COORDINATION, J6 SPANS, J7-J10 PANINI/BILAN), ÉTAT CORRIGÉ
c7f26b35 DOCS — LA PASSE APRÈS LE CHANTIER : 8 FICHES INDEXÉES, L'ÉTAT PAR JOUR DU PLAN, LE JOURNAL DU CHANTIER, CHANTIERS À JOUR (F1 0,7902, 237/238)
c2e629b3 J3.2 — DEUX FACES : 1
… [908 caractères tronqués]
  ```

- **glob** `{"pattern": "**/eval_n2_propre.py"}`

  ```
tools/eval_n2_propre.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """eval_n2_propre.py — la porte honnête : PPL sur un corpus dédupliqué, et hors domaine.
3: 
4: Le corpus de `data/corpus_propre/` est construit par `tools/corpus_propre.py` : passages
5: répétés retirés, split par chunks contigus, **zéro fenêtre de validation dans
6: l'entraînement** (vérifié). Ce script évalue un point de contrôle :
7: 
8:   val / test        : in-domain, fenêtres tirées **dans** un chunk (jamais à cheval sur le
9:                       collage de deux chunks, qui est un artefact du split) ;
10:   litterature       : `data/corpus_fr_litterature.txt` (Verne, public domain) — jamais vu ;
11:   anglais           : `data/corpus_en.txt` (Wikipédia) — jamais vu ;
12:   wikitext2         : `data/wikitext2_test.txt` — jamais vu ;
13:   permute           : contrôle négatif, mêmes octets de validation, ordre détruit ;
14:   decomposition     : PPL des têtes précoces (après 2, 4, 6 blocs) et sans la boucle de
15:                       pensée — ce que chaque pièce porte, et ce que l'arrêt précoce coûte ;
16:   longueurs         : PPL à
… [6366 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools | grep -i n2; find . -name 'entrainer_native.py' -o -name 'native_model.py' | head", "description": "Find N2 related files"}`

  ```
eval_n2_budget.py
eval_n2_propre.py
eval_n2.py
./tools/native_model.py
./tools/entrainer_native.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"rope\\|RoPE\\|position\" tools/native_model.py | head -60", "description": "Find RoPE code in native model"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"rope\" tools/entrainer_native.py | head -60", "description": "Find rope options in trainer"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work | head -40; find work -maxdepth 2 -iname '*n2*' | head -40", "description": "List work dirs and N2 artifacts"}`

  ```
attente_portes.sh
chantier
corpus-commun
corpus-wiki-langues.log
corpus-wiki.log
corpus-wiki-reste.log
dr
entete-references.txt
finaliser_ocr.py
hub-nuit.md
j32
maj_references2.py
maj_references3.py
maj_references.py
maj_table_seule.py
msg-1335.txt
msg-80-2.txt
msg-backlog-n2.txt
msg-bilan.txt
msg-claims.txt
msg-cle2.txt
msg-cle3.txt
msg-cle.txt
msg-cpt.txt
msg-etat.txt
msg-homeo2.txt
msg-homeo.txt
msg-j2.txt
msg-jour.txt
msg-n2-sed.txt
msg-n2-sous25.txt
msg-nuit.txt
msg-p3.txt
msg-passe82.txt
msg-pin.txt
msg-r11.txt
msg-refs.txt
n2ac
n2d
n2h
work/n2d
work/n2h
work/n2i
work/n2j
work/n2k
work/n2w
work/n2ac
work/portes/passe-1102-apres-n2
work/msg-n2-sed.txt
work/msg-n2-sous25.txt
work/msg-backlog-n2.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/native_model.py tools/entrainer_native.py; grep -n \"class NativeConfig\\|@dataclass\\|def forward\\|rotary\\|theta\\|pos\" tools/native_model.py | head -80", "description": "Inspect native model structure"}`

  ```
211 tools/native_model.py
  137 tools/entrainer_native.py
  348 total
24:@dataclass
25:class NativeConfig:
35:    max_pos: int = 2048
50:    def forward(self, x):
80:    def forward(self, x):
85:        q = q.view(b, s, self.cfg.n_heads, dh).transpose(1, 2)
86:        k = k.view(b, s, self.cfg.n_heads, dh).transpose(1, 2)
87:        v = v.view(b, s, self.cfg.n_heads, dh).transpose(1, 2)
91:        y = y.transpose(1, 2).reshape(b, s, d)
101:        self.pos = nn.Embedding(self.cfg.max_pos, self.cfg.d_model)
119:    def forward(self, ids, pos_debut: int = 0, canal=None):
121:        x = self.embed(ids) + self.pos(torch.arange(s, device=ids.device) + pos_debut)[None]
142:    def forward_jusqua(self, ids, n_blocs: int, pos_debut: int = 0, canal=None):
145:        x = self.embed(ids) + self.pos(torch.arange(s, device=ids.device) + pos_debut)[None]
168:    if nom.startswith("embed.") or nom.startswith("pos."):
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"rope\" --include='*.py' . | head -30", "description": "Find python files mentioning rope"}`

  ```
./src/transformer_np.py
./run_harness.py
./tools/mla_synthetique.py
./tools/v41_compresseur_reference.py
./tools/rope_yarn_temoin.py
./tools/v41_attention_reference.py
./tools/v41_attention_coeur.py
./tools/v41_attention_blocs.py
./tools/extrait_article1.py
./tools/premiere_couche_semantique.py
./tools/essai_decharge.py
./tools/porte_mistral.py
./tools/exporter_gguf.py
./tools/mrope_valeurs_or.py
./tools/entrainer_moteur.py
./tools/genealogie_udhr.py
./tools/traduire_bench.py
./tools/decoupage_familles.py
./tools/jeux/grammaire.py
./tools/jeux/codecs/base.py
./tools/jeux/regles/dames.py
./tools/cerveau/voies.py
./tools/cerveau/gating.py
./tools/cerveau/neuromodulation.py
./tools/docwatch/src/docwatch/config.py
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/cache.py
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/configuration.py
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/exceptions.py
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/self_outdated_check.py
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/cli/parser.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports | grep -i -E 'n2|coord' | head -40; ls journal | tail -20", "description": "List N2 reports and recent journal days"}`

  ```
n2-200k.json
n2-budget.json
n2-capacite-fenetre.json
n2-distillation.json
n2-distillation-native.json
n2-fenetre.json
n2-hierarchie.json
n2-porte-propre.json
n2-production-fenetre.json
n2-propre.json
n2-r11.json
n2-r12-2048.json
pensee-etat-n2.json
pensee-quatre-modes-432-run2.json
pensee-quatre-modes-run2.json
rapport-etat-n2.md
rapport-n2-200k.md
rapport-n2-34m-distille.md
rapport-n2-anglais-34m.md
rapport-n2-anglais-distille.md
rapport-n2-anglais.md
rapport-n2-budget.md
rapport-n2-canal-34m.md
rapport-n2-canal-distille.md
rapport-n2-canal-kd-34m.md
rapport-n2-canal.md
rapport-n2-capacite-34m.md
rapport-n2-capacite.md
rapport-n2-capacite-reelle.md
rapport-n2-combine.md
rapport-n2-corpus-1go.md
rapport-n2-corpus-elargi.md
rapport-n2-corpus-reel.md
rapport-n2-distillation.md
rapport-n2-distillation-native.md
rapport-n2-distillation-reelle.md
rapport-n2-diversite.md
rapport-n2-echantillon.md
rapport-n2-fenetre.md
rapport-n2-fenetre-r1.md
2026-10-23
2026-10-24
2026-10-25
2026-10-26
2026-10-27
2026-10-28
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
README.md
sessions
THEMES.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find work/n2w work/n2i work/n2k work/n2j -maxdepth 2 -type f 2>/dev/null | head -60", "description": "List N2 work artifacts"}`

  ```
work/n2w/analyse.py
work/n2w/extraire_big.py
work/n2w/extraire_big.log
work/n2w/corpus_big.log
work/n2w/deduit_leger.py
work/n2w/deduit_leger.log
work/n2w/pipeline_big.sh
work/n2w/pipeline_big.out
work/n2w/canal_big.log
work/n2w/base-big.log
work/n2w/base-big.pt
work/n2w/base-big.drvm
work/n2w/base-big.pt.json
work/n2w/base-big-canal.log
work/n2w/base-big-canal.pt
work/n2w/base-big-canal.drvm
work/n2w/base-big-canal.pt.json
work/n2w/eval_croise.py
work/n2w/big-60k.log
work/n2w/fr-60k.log
work/n2w/big-60k.pt
work/n2w/big-60k.drvm
work/n2w/big-60k.pt.json
work/n2w/fr-60k.pt
work/n2w/fr-60k.drvm
work/n2w/fr-60k.pt.json
work/n2w/eval-fr60-fr.json
work/n2w/eval-big60-fr.json
work/n2w/eval-big60-big.json
work/n2w/eval-fr60-big.json
work/n2w/eval_ood_canal.py
work/n2w/ood-fr60.json
work/n2w/ood-big60.json
work/n2w/mix-60k.log
work/n2w/mix-60k.pt
work/n2w/mix-60k.drvm
work/n2w/mix-60k.pt.json
work/n2w/eval-mix60-fr.json
work/n2w/eval-mix60-big.json
work/n2w/ood-mix60.json
work/n2i/base.log
work/n2i/teacher.log
work/n2i/file-gpu0.sh
work/n2i/file-gpu1.sh
work/n2i/file-gpu0.out
work/n2i/file-gpu1.out
work/n2i/fiche.md
work/n2i/remplit.py
work/n2i/evalue.sh
work/n2i/base-repo.pt
work/n2i/base
… [263 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"8,02\\|2,79\\|8\\.02\\|2\\.79\" reports docs journal --include='*.md' --include='*.json' | head -40", "description": "Search documents for the numbers"}`

  ```
reports/rapport-encodage.md:15:| non structuré | 2 | 49.6 % | 72.46 % | 1.50 | **5.02** | 18.02 | 2.00 | 1.22 | 2.0 |
reports/rapport-8bits.md:9:- `E[|v|]` : **42.79**
reports/rapport-mode-listes.md:40:2. **L'unaires est disqualifié par la mesure** : `E[|v|] = 42,79` pour un Q8_0,
reports/rapport-transport-liste.md:70:contre 18,02). Ce n'est pas une perte de précision, c'est un calcul faux.
reports/rapport-transport-liste.md:128:sur **256 jetons de WikiText-2**, où la référence locale vaut 18,02 :
reports/rapport-transport-liste.md:176:| dense f32 | 3 623 | 0,00e0 | 18,0206 |
reports/rapport-prefill-reparti.md:43:| contrôle `--lot 1` (un flux par jeton) | 255 | **0,00e0** (18,0206 = 18,0206) |
reports/rapport-e5-distillation.md:575:| **distillé, KL PLEIN**, taux 1e-3 *(le réglage publié)* | 748,02 | 561,11 | **24,9 %** | **38,9 %** |
reports/sonde-octets-position.json:66:   98.02946777588454,
reports/restitution-udhr.json:2617:  "exactitude_vue": 62.797419301101144,
reports/restitution-udhr.json:3415:  "exactitude_vue": 58.02190293158803,
reports/restitution-udhr-flux.json:568:  "exactitude_vue": 72.7933624300072,
reports/restitution-udhr-flux.json:2174:  "exactitude_vue": 62.79375
… [1741 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"eval_n2_propre\" --include='*.md' --include='*.json' --include='*.py' . | grep -v '.venv' | head -50", "description": "Find references to eval_n2_propre"}`

  ```
./reports/rapport-n2-propre.md:143:  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py) · agrégat
./reports/rapport-n2-diversite.md:74:  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py).
./reports/rapport-n2-combine.md:57:  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py).
./reports/rapport-n2-corpus-elargi.md:63:  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py).
./reports/rapport-file-taches.md:51:| T09 | N2 | La porte propre (0,29 manquant à 2,7856) : données ou capacité | reports/n2-*, work/n2ac/, tools/entrainer_native.py, GPU | recette N2 1 024 | aucun externe ; GPU libres (0 %) | python3 tools/eval_n2_propre.py <checkpoint> (pas de commande unique) | P0 |
./reports/rapport-file-taches.md:53:| T11 | N4 | Consigne courte : construire le jeu, entraîner, évaluer tenu à l'écart (24/24 vus, 0/4 tenus) | backlog/N4-usage-sft.md ; reports/n4-* ; N2/GPU | recette N2 | aucun externe ; GPU libres | python3 tools/eval_n2_propre.py <checkpoint> (pas de commande unique) | P1 |
./reports/rapport-file-taches.md:135:| H12 | eval_n2_propre.py exige un checkpoint | argparse : point positionnel | Pas de commande unique pour N2 ; nommer le checkpoint |
./reports/rapport
… [9011 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"J4.1\\|J4\\.1\\|coordination N2\\|coordination-n2\" --include='*.md' --include='*.json' --include='*.txt' . | head -40", "description": "Find J4.1 task references"}`

  ```
./data/corpus_wiki_fr/train.txt:777345:Michou (de son vrai nom Marie-Christiane Denise Ducap) est une chanteuse de La Réunion née le à Saint-Denis. Biographie Michou est la fille du compositeur et musicien Narmine Ducap qui découvre ses talents musicaux et lui compose son premier titre Viens dors dans mon dos en 1968 (son frère Christian est aussi musicien). Elle enregistre ses premiers ségas en 1971. À l'âge de douze ans, elle connaît son premier tube avec Crazé salle verte et devient « la petite fiancée des Réunionnais ». En 1974, elle publie Bouscule pas, chanson qui sera reprise en 1982 par Carlos sous le titre Mario mon coco. Son père ayant toujours privilégié pour elle les études à la musique, Michou attendra ses quinze ans pour se produire sur scène. Après de nombreux 45 tours, elle fait une rencontre décisive avec les musiciens du groupe Caméléon (entre autres, Alain Péters, René Lacaille, Loy Ehrlich, Bernard Brancard) qui signeront en 1978 les orchestrations du 33 tours Tombé levé, une des meilleures ventes du label Royal. Au début des années 1980, Michou donnera des concerts à Maurice au théâtre de Port-Louis et au Bataclan de Paris. En 1984, elle intègre le groupe Calyp
… [48730 caractères tronqués]
  ```

- **job_kill** `{"job_id": "bash-13", "reason": "grep hit data corpus, irrelevant"}`

  ```
requested cancellation of job bash-13
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-n2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-n2.md</path>
<type>file</type>
<content>
1: # N2 — l'état du chantier et de sa porte : inventaire, vérification, proposition
2: 
3: > **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-06 · **Verdict** :
4: > N2 n'a **pas** de porte unique dans la passe : sa rouge est une **mesure** — **2,7856** de PPL
5: > sur le corpus propre à 1 024 octets contre la porte **< 2,5**, soit **0,29** en validation
6: > (**0,36** en test). Le mètre est **reproductible** (2,7856 / 2,8566 à l'identique, contrôle
7: > permuté **1 692,39**, deux exécutions égales) et tient en **12 s** de GPU. `tools/eval_n2_propre.py`
8: > **tourne** sur le checkpoint le plus récent mais **ne le mesure pas** : il charge l'architecture à
9: > positions **absolues** et rend **12,91** (pire que l'uniforme, 5,55) là où le mètre RoPE rend
10: > **4,63** ; sur le checkpoint de la porte, **8,02** contre **2,97** à 128 octets. Une
11: > `tools/porte-n2.sh` est **proposable** : non-régression **≤ 2,80** par défaut, seuil **2,5** en
12: > mode chantier, **~30–40 s** de GPU, dépendante de `work/` et `data/` **non suivis**.
13: 
14: ## La
… [19372 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-etat-n2.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-etat-n2.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-06",
3:  "ligne": "N2",
4:  "head": "bfd98892",
5:  "objet": "état de N2 et de sa porte",
6:  "checkpoints": {
7:   "total_work": 123,
8:   "taille_go": 9.52,
9:   "avec_metadonnees": 67,
10:   "suivis_git": false,
11:   "note": "work/ et data/ sont gitignorés ; un 124e .pt vit sous data/adaptateurs/ (hors N2)",
12:   "plus_recent": {
13:    "fichier": "work/n2ac/rope2048-20k.pt",
14:    "date": "2026-11-04 21:09",
15:    "octets": 137248474,
16:    "parametres": 34301224,
17:    "corpus": "data/wiki_fr/propre/train.txt",
18:    "pas": 20000,
19:    "pas_segment": 10000,
20:    "seq": 2048,
21:    "window": 2048,
22:    "positions": "rope",
23:    "init": "work/n2ac/rope2048-10k.pt",
24:    "ppl_val_interne": 2.4953,
25:    "fiche": "reports/rapport-n2-r12-2048.md"
26:   },
27:   "porte_propre": {
28:    "fichier": "work/n2ac/propre512-8k.pt",
29:    "date": "2026-11-03 02:01",
30:    "octets": 137248474,
31:    "sha256": "37c5673b3d51f6f871c4391b97015b401f73c842d04d4a05f78a70c2b264eefc",
32:    "parametres": 34301224,
33:    "corpus": "data
… [9277 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(type(p))\ns=json.dumps(p,ensure_ascii=False)\ni=s.find('J4.1')\nprint(s[max(0,i-2500):i+1500])\nEOF", "description": "Read J4.1 plan context"}`

  ```
<class 'dict'>
2.1", "jour": 2, "titre": "Panini I — la table atomes ↔ niveaux", "mandat": "Tâche J2.1 : la table de correspondance entre les **14 atomes** de Panini (∃ ∆ ∼ ↗ ⊙ ⧖ ◇ № ⊕ ⊗ λ ⊞ ≍ ≡) et nos **niveaux** (graphème, mot, pos, syntagme, phrase, pragmatique, discours, document). Lis `../Panini/README.md`, `../Panini-Research/`, `docs/theorie/genealogie-des-langues.md`. Produis `reports/rapport-atomes-niveaux.md` + JSON : 14 lignes, ce que chaque atome capte, quel niveau le porte, la mesure possible. Aucune écriture dans Panini.", "budget_min": 90, "acceptation": [{"commande": "test -f reports/rapport-atomes-niveaux.md && echo FICHE-OK", "attendu": "FICHE-OK"}, {"commande": "grep -c '∃' reports/rapport-atomes-niveaux.md", "attendu": ""}]}, {"id": "J2.2", "jour": 2, "titre": "Panini I — le corpus commun", "mandat": "Tâche J2.2 : le corpus commun — choisir un échantillon (10-50 textes) présent des deux côtés (Panini/NIPADA et Drave), le normaliser (UTF-8, une phrase par ligne, métadonnées langue/époque), l'écrire dans `work/corpus-commun/` (non versionné) + une fiche `reports/rapport-corpus-commun.md` + JSON. Lire les corpus Panini sans les modifier.", "budget_min": 90, "accep
… [2815 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/native_model.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/entrainer_native.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/native_model.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """native_model.py — `drave-n0`, le modèle natif du programme N.
3: 
4: Ce n'est pas un Qwen3-MoE : c'est un graphe de blocs en **octets**, avec
5: attention locale, FFN creux routé, sorties précoces, cellule de pensée et pont.
6: Le modèle est petit (12 M) : c'est un **banc de mécanismes**, pas un assistant.
7: 
8: Le fichier définit l'architecture, l'export DRVM et les tests de forme. Il ne
9: prétend pas que l'entraînement est fait : N1.2 reste à mesurer.
10: """
11: from __future__ import annotations
12: 
13: import json
14: import math
15: from dataclasses import dataclass
16: 
17: import torch
18: import torch.nn as nn
19: import torch.nn.functional as F
20: 
21: from tools.drvm import TensorSpec, write_drvm
22: 
23: 
24: @dataclass
25: class NativeConfig:
26:     vocab: int = 256
27:     d_model: int = 224
28:     n_blocks: int = 6
29:     n_heads: int = 4
30:     expert_hidden: int = 288
31:     n_experts: int = 8
32:     top_k: int = 2
33:     kwta: float = 0.25
34:     window: int = 256
35:     max_pos: int = 2048
36:     thought_step
… [9742 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/entrainer_native.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """entrainer_native.py — entraînement de base de `drave-n0`.
3: 
4: Ce n'est que le **prochain octet** : les pertes locales, les têtes précoces, la
5: pensée et le pont viendront après. Le but est de mesurer la PPL du modèle natif
6: et de produire un DRVM lisible par le moteur.
7: """
8: from __future__ import annotations
9: 
10: import argparse
11: import json
12: import math
13: import pathlib
14: import random
15: import time
16: 
17: import torch
18: import torch.nn.functional as F
19: 
20: from tools.native_model import NativeConfig, NativeModel, exporter_drvm
21: from tools.vdc import departs_vdc
22: 
23: 
24: def charger(chemin: str) -> torch.Tensor:
25:     b = pathlib.Path(chemin).read_bytes()
26:     if len(b) < 100_000:
27:         raise SystemExit(f"{chemin} : corpus trop court")
28:     return torch.tensor(list(b), dtype=torch.long)
29: 
30: 
31: def lot(data: torch.Tensor, n: int, seq: int, device: str, compteur: int, canal=None):
32:     # Van der Corput : même compteur = mêmes fenêtres, sans état aléatoire.
33:     i = torc
… [6055 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la work/n2ac | head -80", "description": "List n2ac directory"}`

  ```
total 8032656
drwxr-xr-x. 1 stephane stephane     10412  5 nov 10:19 .
drwxr-xr-x. 1 stephane stephane      1816  7 nov 18:22 ..
-rw-r--r--. 1 stephane stephane 137224476  2 nov 17:31 absolu-pos1152.drvm
-rw-r--r--. 1 stephane stephane     21807  2 nov 17:31 absolu-pos1152.log
-rw-r--r--. 1 stephane stephane 137248740  2 nov 17:30 absolu-pos1152.pt
-rw-r--r--. 1 stephane stephane       561  2 nov 17:31 absolu-pos1152.pt.json
-rw-------. 1 stephane stephane      2763  2 nov 21:05 agrege_fenetre.py
-rw-r--r--. 1 stephane stephane      1680  2 nov 23:31 agrege_production.py
-rw-------. 1 stephane stephane      3151  2 nov 18:50 agrege_r11.py
-rw-r--r--. 1 stephane stephane  47283932  3 nov 04:04 cap-1147m-128.drvm
-rw-r--r--. 1 stephane stephane     35105  3 nov 04:04 cap-1147m-128.log
-rw-r--r--. 1 stephane stephane  47308063  3 nov 04:04 cap-1147m-128.pt
-rw-r--r--. 1 stephane stephane       505  3 nov 04:04 cap-1147m-128.pt.json
-rw-r--r--. 1 stephane stephane  47283932  3 nov 03:33 cap-1147m-512.drvm
-rw-r--r--. 1 stephane stephane      9444  3 nov 03:33 cap-1147m-512.log
-rw-r--r--. 1 stephane stephane  47308063  3 nov 03:33 cap-1147m-512.pt
-rw-r--r--. 1 stephane stephane       
… [4700 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2ac/rope_model.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2ac/eval_longueurs.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2ac/rope_model.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """rope_model.py — la variante **positions relatives** du modèle natif (R1.1/R1.2).
3: 
4: Le modèle de `tools/native_model.py` ajoute une **position apprise absolue** (`self.pos`) et
5: compte sur les positions aléatoires à l'entraînement (N2.j2) : le gain à 512 octets est réel
6: (÷2,1 à ÷2,4) mais c'est une **astuce d'entraînement**, pas une propriété de l'architecture.
7: Ce module remplace la position absolue par un **RoPE** (rotation des q/k, aucune position
8: apprise) : le score d'attention ne dépend plus que de l'**écart** entre positions, donc
9: l'extrapolation en longueur est acquise par construction.
10: 
11: Rien n'est modifié dans `tools/` : les blocs réutilisent les **mêmes noms de paramètres**
12: (`ln1`, `qkv`, `out`, `ln2`, `ffn`), ce qui permet de charger un point de contrôle absolu
13: comme initialisation (`strict=False`, `pos` reste inutilisé).
14: 
15: Usage :
16:   PYTHONPATH=. python3 -c "from work.n2ac.rope_model import charge_rope; ..."
17: """
18: from __future__ import annotations
19: 
20: import math
21: 
22: im
… [4599 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2ac/eval_longueurs.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """eval_longueurs.py — la courbe de longueur d'un point de contrôle (absolu ou RoPE).
3: 
4: Le mètre est celui de N2 (`work/n2j/evalue_canal.py`) : canal fourni, fenêtres Van der Corput
5: dans des chunks de 8192 octets, 8 lots × 16 fenêtres. On peut demander n'importe quelle
6: longueur, y compris **1 000 octets** (la porte R1.1).
7: 
8: Usage :
9:   PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/eval_longueurs.py <point.pt> \
10:       --longueurs 128,256,512,1000 [--rope] [--val data/wiki_fr/propre]
11: """
12: from __future__ import annotations
13: 
14: import argparse
15: import json
16: import pathlib
17: import sys
18: 
19: sys.path.insert(0, ".")
20: sys.path.insert(0, "work/n2j")
21: 
22: import torch  # noqa: E402
23: 
24: from tools.eval_n2_propre import charge, charger_bytes  # noqa: E402
25: import evalue_canal as ec  # noqa: E402
26: 
27: 
28: def main() -> None:
29:     ap = argparse.ArgumentParser()
30:     ap.add_argument("point")
31:     ap.add_argument("--longueurs", default="128,256,512")
32:     ap.add_argument("--rope"
… [1111 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat work/n2ac/propre512-8k.pt.json; echo '---'; cat work/n2ac/rope2048-20k.pt.json; echo '---'; cat work/n2h/A-propre-g1.pt.json 2>/dev/null | head -30", "description": "Read checkpoint sidecars"}`

  ```
{
 "modele": "drave-n0-rope",
 "parametres": 34301224,
 "corpus": "data/corpus_propre/train.txt",
 "octets": 3244858,
 "pas": 8000,
 "seq": 512,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "window": 512,
 "positions": "rope",
 "init": "work/n2j/base-wiki-45m.pt",
 "perte_finale": 0.8525079488754272,
 "ppl_val": 3.363862704237594,
 "jetons_val": 32768,
 "tetes": true,
 "drvm": "work/n2ac/propre512-8k.drvm",
 "sha256_drvm": "b2034de3cd0d84f4ea2481fe5f7b449eabf5534e4a8463fa0b000fbb73fb8bcf",
 "duree_s": 1561.0706672668457
}
---
{
 "modele": "drave-n0-rope",
 "parametres": 34301224,
 "corpus": "data/wiki_fr/propre/train.txt",
 "octets": 186089472,
 "pas": 10000,
 "seq": 2048,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "window": 2048,
 "positions": "rope",
 "init": "work/n2ac/rope2048-10k.pt",
 "perte_finale": 0.8965461254119873,
 "ppl_val": 2.4953209637199847,
 "jetons_val": 131072,
 "tetes": true,
 "drvm": "work/n2ac/rope2048-20k.drvm",
 "sha256_drvm": "91a302872988691e1a489ea1dea88a3e1787bd6ababaf637041ef2f3c1c6c529",
 "duree_s": 10220.861443519592
}
---
  ```

- **bash** `{"command": "nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader 2>&1 | head; ls -la ~/gpu-env/bin/python 2>&1", "description": "Check GPU and python environment"}`

  ```
0, Quadro RTX 5000, 154 MiB, 16384 MiB, 0 %
1, Quadro RTX 5000, 4 MiB, 16384 MiB, 0 %
lrwxrwxrwx. 1 stephane stephane 7 31 jui 08:53 /home/stephane/gpu-env/bin/python -> python3
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 300 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2ac/propre512-8k.pt 2>&1 | grep -v Loading", "description": "Reproduce absolute-position eval on RoPE checkp … [27 caractères tronqués]`

  ```
{"fichier": "propre512-8k.pt", "params": 34301224, "val": 8.0225, "test": 8.0126, "litterature": 18.5021, "litterature_propre": 18.8906, "anglais": 43.2434, "wikitext2": 47.3566, "permute": 1404.2994}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 300 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/propre512-8k.pt --rope --longueurs 128,256,512,1024 --val data/corpus_propre 2>&1 | grep -v Loading" … [80 caractères tronqués]`

  ```
L128 : 2.9726
  L256 : 2.8988
  L512 : 2.8443
  L1024 : 2.7856
{"fichier": "propre512-8k.pt", "val": "data/corpus_propre", "positions": "rope", "L128": 2.9726, "L256": 2.8988, "L512": 2.8443, "L1024": 2.7856}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 300 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2ac/rope2048-20k.pt 2>&1 | grep -v Loading", "description": "Reproduce absolute eval on rope2048 checkpoint" … [22 caractères tronqués]`

  ```
{"fichier": "rope2048-20k.pt", "params": 34301224, "val": 12.9098, "test": 12.5881, "litterature": 11.5343, "litterature_propre": 11.942, "anglais": 16.9982, "wikitext2": 17.8491, "permute": 272.4992}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 600 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/rope2048-20k.pt --rope --longueurs 128,1024 --val data/corpus_propre 2>&1 | grep -v Loading", "descr … [75 caractères tronqués]`

  ```
L128 : 5.4773
  L1024 : 4.6321
{"fichier": "rope2048-20k.pt", "val": "data/corpus_propre", "positions": "rope", "L128": 5.4773, "L1024": 4.6321}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. ~/gpu-env/bin/python - <<'EOF'\nimport torch\nfrom tools.native_model import NativeConfig, NativeModel\nck=torch.load('work/n2ac/propre512-8k.pt',map_location='cpu',weights_only=False)\ncfg=Nati … [609 caractères tronqués]`

  ```
cles checkpoint 127
missing 0 unexpected 0
pos.weight dans checkpoint (2048, 384)
pos.weight norme 830.0988159179688
config positions? None
cfg dict keys ['d_model', 'early_blocks', 'expert_hidden', 'kwta', 'max_pos', 'n_blocks', 'n_experts', 'n_heads', 'rsn_dim', 'thought_steps', 'top_k', 'vocab', 'window']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports | grep -i coord; ls reports | grep -i 'pensee.*coord'", "description": "Check existing coordination reports"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"coordination\" reports/*.md | head -30", "description": "Find coordination fiche conventions"}`

  ```
reports/rapport-atomes-niveaux.md:106:| 13 | **≍ SYMÉTRIE** (41) | équilibre, invariance, harmonie, répétition équilibrée | graphème → discours | émergent | parallélisme, coordination, sections équilibrées, palindromes → score de parallélisme, variance des longueurs ; ρ avec la part de ≍ | casser le parallélisme ; permutation |
reports/rapport-contrat-s.md:231:- **60 absences.** 54 sont anglaises. Les 6 françaises sont : `car` traité comme coordination
reports/rapport-etat-a.md:127:- `rapport-file-taches.md` : **29 tâches** (8 autonomes, 11 coordination, 10 bloquées), **6 doublons**,
reports/rapport-file-taches.md:5:> **Verdict** : **29 tâches** — **8 autonomes**, **11 en coordination**, **10 bloquées** ; **6 doublons**, **18 périmées**, **12 dépendances cachées**.
reports/rapport-file-taches.md:10:La file est **courte** une fois les doublons retirés : **8 tâches sont exécutables en autonomie** dans le territoire L/B13 et le pilotage, **11 demandent une coordination** (S, D, N2, A, produit), **10 sont bloquées** par une ressource externe nommée. Le reste de ce que les documents appellent « ce qui reste » est **déjà fait** ou **mal daté** : 18 mentions périmées, dont 6 répétées dans
… [2639 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' reports/rapport-file-taches.md", "description": "Read task file report header"}`

  ```
# La file des tâches — inventaire, trois files et ordre pour 09 h 30 → 12 h

> **Ligne de roadmap** : B13 (moteur de pensée) · **Date** : 2026-11-06, 10 h 20 HNE · **Branche** : `s/v7` · **HEAD mesuré** : `7679a2d4`.
> **Mission** : inventer toutes les prochaines actions nommées dans `roadmap.md`, `en-cours.md`, `plan-travail.md` § 9 et § 12, `backlog/index.md`, `backlog/dependances.md`, `references-non-regression.md` et les 12 fiches récentes ; les classer en trois files ; détecter doublons et périmées ; proposer l'ordre de la fenêtre.
> **Verdict** : **29 tâches** — **8 autonomes**, **11 en coordination**, **10 bloquées** ; **6 doublons**, **18 périmées**, **12 dépendances cachées**.
> **Ce que cette fiche n'est pas** : un commit, une modification d'existant, ou une mesure nouvelle sur S/D/N2. Elle ne crée que deux fichiers neufs.

## 1. Résumé exécutif

La file est **courte** une fois les doublons retirés : **8 tâches sont exécutables en autonomie** dans le territoire L/B13 et le pilotage, **11 demandent une coordination** (S, D, N2, A, produit), **10 sont bloquées** par une ressource externe nommée. Le reste de ce que les documents appellent « ce qui reste » est **déjà fait** o
… [12483 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%Y-%m-%d %H:%M:%S %Z'; git branch --show-current; git rev-parse --short HEAD; git status --short reports | head", "description": "Check date, branch, HEAD"}`

  ```
2026-11-13 21:42:01 EST
s/v7
ced21933
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,40p' reports/rapport-n2-porte-propre.md", "description": "Read porte propre fiche header"}`

  ```
# N2 — La porte < 2,5 sur le corpus propre, attaquée avec la fenêtre

> **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-03 · **Verdict** :
> la porte **< 2,5 n'est pas atteinte** : le meilleur point est **2,7856** en
> validation et **2,8566** en test (fenêtre 512, contexte 1 024) — il manque **0,29**. Mais la
> fenêtre est le **seul bras dont la courbe descend avec la longueur** : à octets égaux (33 Mo),
> la fenêtre 512 fait **2,9726 → 2,8443 → 2,7856** de 128 à 1 024 octets, quand la fenêtre 128
> fait **2,9027 → 3,0464 → 3,1107** : elle gagne à courte longueur, puis elle est **0,33
> derrière** à 1 024.
> Les deux bras battent la chaîne honnête de N2.h (val **3,0904**, test **3,1960**). Et la
> **capacité ne ferme pas la porte** : à fenêtre 512, init aléatoire et 33 Mo vus, 11,47 M donne
> 2,8960 à 1 024 octets, 21,65 M 2,8688, 34,3 M **2,8662** — elle **sature** à 21,65 M et laisse
> encore **0,37**.

## La question

La porte de N2 est **PPL < 2,5 sur le corpus propre**, tenu à l'écart par construction (N2.h :
corpus dédupliqué, split par chunks, **0 % de fuite**). La chaîne honnête y valait **3,0904** avec
la recette à fenêtre 128 ; la porte était à **
… [1179 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p.get('taches', p if isinstance(p,list) else []):\n    if isinstance(t,dict) and str(t.get('id','')).startswith('J4'):\n        print(t['id'], t[ … [166 caractères tronqués]`

  ```
J4.1 Coordination N2 — le mètre RoPE
Tâche J4.1 : la coordination N2 — le mètre `eval_n2_propre.py` lit les checkpoints RoPE comme des positions absolues (8,02 au lieu de 2,79). **Ne modifie rien dans N2** (ni `entrainer_native.py`, ni `native_model.py`, ni `work/`). Écris une fiche de coordination `reports/rapport-coordination-n2.md` + JSON : le bug, le correctif proposé (--rope), les chiffres, la commande exacte pour la session N2.
acceptation [{'commande': 'test -f reports/rapport-coordination-n2.md && echo FICHE-OK', 'attendu': 'FICHE-OK'}]

J4.2 Coordination S — les 11 verdicts
Tâche J4.2 : la coordination S — 11 verdicts de `/paragraphes` non committés. **Ne touche pas `tools/structures/`**. Fiche `reports/rapport-coordination-s.md` + JSON : la liste exacte des 11 verdicts (fichier, lignes, statuts), la commande de commit pour la session S, le risque d'un clone à 523d8c1.
acceptation [{'commande': 'test -f reports/rapport-coordination-s.md && echo FICHE-OK', 'attendu': 'FICHE-OK'}]

J4.3 Coordination R — le tagger sur 612
Tâche J4.3 : la coordination R — décider le tagger POS sur le gold 612 via l'API DeepSeek (clé absente). Fiche `reports/rapport-coordination-r.md` + JSON : 
… [711 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work/chantier; find work/chantier -maxdepth 2 -type f | head -30", "description": "Inspect chantier work dir"}`

  ```
boucle2.log
boucle.log
etat.json
journal.log
work/chantier/journal.log
work/chantier/etat.json
work/chantier/boucle.log
work/chantier/boucle2.log
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports | grep -E 'etat-a|coordination|contrat-s' ; ls reports | grep -E '^rapport-.*\\.json$' | head", "description": "Check report/JSON pairing conventions"}`

  ```
pensee-contrat-s.json
pensee-etat-a.json
rapport-contrat-s.md
rapport-etat-a.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"JSON\\|pensee\" reports/rapport-etat-a.md | tail -20; tail -30 reports/rapport-etat-a.md", "description": "Inspect etat-a JSON reference"}`

  ```
19:> `python3 -m tools.pensee.autotest`, `python3 tools/tests/linguistique/evaluer_gold.py`,
29:| `python3 -m tools.pensee.autotest` | **183/183**, exit 0 | l'état B13 est à jour |
82:  choisie à 5 %. **Ce n'est pas une mesure courante** : le JSON dit « pas de chiffre courant » ; la
88:- **Chiffre à corriger** : la fiche et le JSON disent **4 tests** ; `placement.rs` en a **8**
110:  **19/19** ; il reste **refusé**. Le JSON `a83a-flux.json` dit encore « pont/coupe restent » :
201:  (VRAM/offload) ; fiche `reports/rapport-a62-moe.md` + JSON.
212:  alors un régime dual ; fiche `reports/rapport-a83b2-lot.md` + JSON.
231:- **Fichiers neufs** : `reports/rapport-etat-a.md` (ce rapport) et `reports/pensee-etat-a.json`
  les fiches A24/A26 sont des instantanés et le code du bloc a changé à 21 h 47 ; les portes
  `pont`/`coupe` n'ont pas été rejouées ; le harnais A17 n'est pas committé ; le MoE n'a pas été
  relancé ici (les chiffres C9/A8.3c sont lus, pas reproduits).
- **Le contrôle qui compte** : `cargo test placement` (**8/8**) et `DRAVE_PERTE_MAX=1 porte-flux`
  (**exit 0**, 58,3200 / 62,7357) sont des **rejeux**, pas des lectures. Ils confirment A2.6
  (règle) et A8.3a (régime 1 %) au
… [1487 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"JSON\\|json\" docs/methode/resultats.md | head -40", "description": "Read result naming convention"}`

  ```
3:> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
27:| `reports/` | la **fiche** : chiffres, dispositif, contrôles, pièges, limites ; les JSON de résultats bruts |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md</path>
<type>file</type>
<content>
1: # Ce qu'un résultat doit porter
2: 
3: > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
4: > résultats, ou un message de commit.
5: 
6: ## Les cinq pièces d'un résultat
7: 
8: 1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
9:    [porte](../theorie/glossaire/entrees/porte.md)) ;
10: 2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
11:    mesure pas ;
12: 3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
13:    quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
14:    grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire co
… [2865 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la work/n2h/A-propre-g1.pt* 2>&1; ls work/n2h | head -20", "description": "Check absolute control checkpoint"}`

  ```
-rw-r--r--. 1 stephane stephane 47302035 31 oct 23:12 work/n2h/A-propre-g1.pt
agrege.py
A-propre-g1.json
A-propre-g1.log
A-propre-g1.out
A-propre-g1.pt
A-propre-g2.json
A-propre-g2.log
A-propre-g2.out
A-propre-g2.pt
A-propre-g3.json
A-propre-g3.log
A-propre-g3.out
A-propre-g3.pt
base-capacite.drvm
base-capacite.log
base-capacite.pt
base-capacite.pt.json
base.log
base-mixte.drvm
base-mixte.log
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la work/n2ac/propre512-8k.pt work/n2ac/rope2048-20k.pt; sha256sum work/n2ac/propre512-8k.pt", "description": "Verify checkpoints and sha256"}`

  ```
-rw-r--r--. 1 stephane stephane 137248474  3 nov 02:01 work/n2ac/propre512-8k.pt
-rw-r--r--. 1 stephane stephane 137248474  4 nov 21:09 work/n2ac/rope2048-20k.pt
37c5673b3d51f6f871c4391b97015b401f73c842d04d4a05f78a70c2b264eefc  work/n2ac/propre512-8k.pt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 300 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2ac/propre512-8k.pt --longueurs 2>&1 | grep -v Loading", "description": "Measure wrong length curve on RoPE  … [33 caractères tronqués]`

  ```
{"fichier": "propre512-8k.pt", "params": 34301224, "val": 8.0225, "test": 8.0126, "litterature": 18.5021, "litterature_propre": 18.8906, "anglais": 43.2434, "wikitext2": 47.3566, "permute": 1404.2994, "longueurs": {"129": 8.1024, "192": 8.4072, "256": 8.971, "384": 10.0906, "512": 11.3357}}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 300 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2h/A-propre-g1.pt --longueurs 128,1024 --val data/corpus_propre 2>&1 | grep -v Loading", "description":  … [66 caractères tronqués]`

  ```
L128 : 10.9904
  L1024 : 34.988
{"fichier": "A-propre-g1.pt", "val": "data/corpus_propre", "positions": "absolues", "L128": 10.9904, "L1024": 34.988}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 600 ~/gpu-env/bin/python - <<'EOF' 2>&1 | grep -v Loading\nimport json, pathlib\nfrom tools.eval_n2_propre import charger_bytes, ppl_protocole, RACINE\nfrom work.n … [427 caractères tronqués]`

  ```
128 40.0658
256 49.5308
512 59.8126
1024 65.7898
{"128": 40.0658, "256": 49.5308, "512": 59.8126, "1024": 65.7898}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat work/n2ac/chaine_porte.sh; echo '---'; grep -n \"canal\" work/n2ac/entrainer_rope.py | head -20; echo '---'; grep -n \"canal\" work/n2ac/entrainer_rope.py | wc -l", "description": "Inspect gate training script for canal"}`

  ```
#!/usr/bin/env bash
# chaine_porte.sh — la porte < 2,5 sur le corpus propre, avec et sans fenêtre.
#
# Corpus : data/corpus_propre (train 3,24 Mo, val 180 Ko, 0 % de fuite — N2.h).
# Deux bras à OCTETS ÉGAUX (33 Mo vus), init base-wiki-45m, canal :
#   1. fenêtre 512, 8 000 pas × 8 × 512
#   2. fenêtre 256 (seq 128), 32 000 pas × 8 × 128
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=${1:-1}
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/corpus_propre/train.txt --canal data/corpus_propre/train.canal \
  --seq 512 --window 512 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
  --init work/n2j/base-wiki-45m.pt --pas 8000 \
  --sortie work/n2ac/propre512-8k.pt --drvm work/n2ac/propre512-8k.drvm \
  > work/n2ac/propre512-8k.log 2>&1
echo "propre512-8k fini $(date '+%H:%M:%S')"
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/corpus_propre/train.txt --canal data/corpus_propre/train.canal \
  --seq 128 --window 256 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
  --init work/n2j/base-wiki-45m.pt --pas 32000 \
  --sortie work/n2ac/propre128-32k.pt --drvm work/n2ac/
… [840 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' work/n2ac/entrainer_rope.py", "description": "Read RoPE trainer"}`

  ```
#!/usr/bin/env python3
"""entrainer_rope.py — la recette N2 avec positions **relatives** (R1.1/R1.2).

Identique à `tools/entrainer_native.py` (mêmes fenêtres Van der Corput, même mètre, même
supervision des têtes précoces) à trois exceptions près, toutes déclarées :

  - les blocs sont des `BlockRoPE` (`work/n2ac/rope_model.py`) : plus de table de positions ;
  - `--window` règle le masque d'attention (256 par défaut, la recette N2) ;
  - `--seq` peut dépasser la fenêtre (R1.2) : c'est la fenêtre qui décide de ce que le
    modèle peut lire, pas la longueur de la séquence.

`--positions-aleatoires` est conservé pour la parité d'interface : avec RoPE il est **neutre**
(le décalage de position n'entre plus dans le calcul), ce que l'autotest vérifie.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
      --corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
      --pas 20000 --dim 384 --expert-hidden 512 --init work/n2j/base-wiki-45m.pt \
      --sortie work/n2ac/rope-20k.pt --drvm work/n2ac/rope-20k.drvm
"""
from __future__ import annotations

import argparse
import json
import pathlib
import time

import torch
import torch.nn.fun
… [4102 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2j/evalue_canal.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2j/evalue_canal.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """evalue_canal.py — PPL avec et sans le canal de structure, par longueur, et au mélange."""
3: import json, math, pathlib, random, sys
4: import torch, torch.nn.functional as F
5: sys.path.insert(0, '.')
6: from tools.eval_n2_propre import charge, charger_bytes, departs_vdc
7: from tools.canal_structure import canal as canal_de
8: 
9: CHUNK = 8192
10: 
11: 
12: def fenetres(data, canal, n, long, compteur):
13:     n_chunks = max(1, len(data) // CHUNK)
14:     xs, cs = [], []
15:     for k in range(n):
16:         c = departs_vdc(compteur + k, 1, n_chunks, long)[0]
17:         debut = c * CHUNK
18:         marge = min(CHUNK, len(data) - debut) - long - 1
19:         if marge <= 0:
20:             continue
21:         r = departs_vdc(compteur + 10_000_003 + k, 1, marge, long)[0]
22:         j = debut + r
23:         xs.append(data[j:j + long])
24:         cs.append(canal[j:j + long] if canal is not None else torch.zeros(long, dtype=torch.long))
25:     return torch.stack(xs).cuda(), (torch.stack(cs).cuda() if canal is not None else None)
26: 
… [2433 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 300 ~/gpu-env/bin/python - <<'EOF' 2>&1 | grep -v Loading\nimport pathlib, torch\nfrom work.n2ac.rope_model import charge_rope\nfrom tools.eval_n2_propre import ch … [508 caractères tronqués]`

  ```
L 128 sans canal 40.0658 avec canal 2.9726
L 1024 sans canal 65.7898 avec canal 2.7856
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """eval_n2.py — PPL des points de contrôle N2, trois protocoles.
3: 
4:   standard     : 128 octets indépendants — comparable entre bras et à d'autres runs ;
5:   segmente     : 4×128 avec état transporté — le protocole de l'entraînement ;
6:   segmente-sans: 4×128 avec état remis à zéro à chaque segment — contrôle du précédent.
7: 
8: Usage : PYTHONPATH=. gpu-env/bin/python tools/eval_n2.py /tmp/n2-campagne/*-g*.pt
9:         (sans argument : les points de contrôle de /tmp/n2-campagne)
10: """
11: import glob
12: import json
13: import math
14: import pathlib
15: import sys
16: 
17: import torch
18: import torch.nn.functional as F
19: 
20: from tools.native_model import NativeConfig, NativeModel
21: from tools.distiller_section import HierarchieModel, decoupes
22: from tools.vdc import departs_vdc
23: 
24: LOTS = 32          # 32 lots × 8 = 256 fenêtres par protocole
25: 
26: 
27: def charger(txt):
28:     return torch.tensor(list(pathlib.Path(txt).read_bytes()), dtype=torch.long)
29: 
30: 
31: def ppl_standard(m, data, seq=128, lot=8, device="cuda
… [2949 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"rope\\|canal\" tools/eval_n2_budget.py | head -20; ls data/corpus_propre", "description": "Check other eval tools and canal files"}`

  ```
dev.txt
test.canal
test.txt
train.canal
train.txt
val.canal
val.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git worktree list; git branch -a | head -30", "description": "List worktrees and branches"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet ced21933 [s/v7]
  backup/pre-scrub-20261101-133055
  master
  s/close
* s/v7
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/s/close
  remotes/origin/s/v7
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -i \"N2\\|eval_n2\\|rope\" docs/pilotage/en-cours.md | head -50", "description": "Read N2 state in en-cours"}`

  ```
12:- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
35:- **Ce que font les autres** : **N2**, **S**, **Pensée**.
50:- **Ce que font les autres** : **hub**, **N2**, **Pensée**.
65:- **Ce que font les autres** : **N2**, **S**, **hub**.
71:### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*
74:- **Rôle** : **N2** — la production et la capacité.
79:- **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondération) ; `kd2` et `rope2048` **arrêtés** ; **paire propre de production** : **3,1500** → **3,1119** (−0,06 ; −0,19 anglais) ; **repondération : −0,05** ; **2 048 mesuré** : ne bat pas 1 024 ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [production](../../reports/rapport-n2-production-fenetre.md), [erratum](../../reports/rapport-n2-distillation-native.md), [porte](../../reports/rapport-n2-porte-propre.md).
88:- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-j
… [1267 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -i \"N2\\|eval_n2\\|rope\" docs/pilotage/roadmap.md | head -50", "description": "Read N2 roadmap lines"}`

  ```
32:| **N — le natif** | DRVM, `drave-n0`, [distillation](../theorie/glossaire/entrees/distillation.md), usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; **N0.1 6/6** ; N2.h : 3,0904 domaine, 3,85 hors dépôt ; **N2.ac (1 Go) : 3,49 / 6,03 / 8,34 — production** ; **200 k pas : val_fr 3,16, littérature 5,61, anglais 7,28, wikitext2 8,00** ; **fenêtre 1 024 : 2,4759 / 2,4373 au grand corpus — sous 2,5** ; porte propre **2,7856** ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 partiel | **N2** : **clôturée** le 03/11 11 h 25, la **fenêtre est la recette de production** ; **paire propre de distillation** (04/11) ; puis la **porte propre (0,29)** ; **N4** |
33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2 mesurées** 
… [6763 caractères tronqués]
  ```

- **write** `{"file_path": "/tmp/eval_n2_propre_rope.py", "content": "#!/usr/bin/env python3\n\"\"\"Copie de travail /tmp : eval_n2_propre.py + --rope + --canal-dir + --longueurs liste.\n\nCe fichier n'est PAS dans le dépôt : il sert à vérifier le correctif proposé dans\nreports/rapport-coordination-n2.md. Aucun … [7776 caractères tronqués]`

  ```
<path>/tmp/eval_n2_propre_rope.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 600 ~/gpu-env/bin/python /tmp/eval_n2_propre_rope.py work/n2ac/propre512-8k.pt --rope --canal-dir data/corpus_propre --longueurs 128,256,512,1024 2>&1 | grep -v Lo … [88 caractères tronqués]`

  ```
{"fichier": "propre512-8k.pt", "params": 34301224, "val": 2.9726, "test": 3.0807, "litterature": 52.2935, "litterature_propre": 53.7013, "anglais": 117.4252, "wikitext2": 117.7308, "permute": 1673.4162, "longueurs": {"128": 2.9726, "256": 2.8988, "512": 2.8443, "1024": 2.7856}}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 600 ~/gpu-env/bin/python /tmp/eval_n2_propre_rope.py work/n2ac/propre512-8k.pt --longueurs 128,256,512,1024 2>&1 | grep -v Loading", "description": "Measure wrong  … [50 caractères tronqués]`

  ```
{"fichier": "propre512-8k.pt", "params": 34301224, "val": 8.0225, "test": 8.0126, "litterature": 18.5021, "litterature_propre": 18.8906, "anglais": 43.2434, "wikitext2": 47.3566, "permute": 1404.2994, "longueurs": {"128": 8.0225, "256": 8.971, "512": 11.3357, "1024": 38.5288}}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 600 ~/gpu-env/bin/python /tmp/eval_n2_propre_rope.py work/n2ac/propre512-8k.pt --rope --longueurs 128,256,512,1024 2>&1 | grep -v Loading", "description": "Measure … [53 caractères tronqués]`

  ```
{"fichier": "propre512-8k.pt", "params": 34301224, "val": 40.0658, "test": 39.8109, "litterature": 52.2935, "litterature_propre": 53.7013, "anglais": 117.4252, "wikitext2": 117.7308, "permute": 1673.4162, "longueurs": {"128": 40.0658, "256": 49.5308, "512": 59.8126, "1024": 65.7898}}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 300 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/A-propre-g1.pt 2>&1 | grep -v Loading", "description": "Reproduce absolute control checkpoint", "timeoutM … [11 caractères tronqués]`

  ```
{"fichier": "A-propre-g1.pt", "params": 11816136, "val": 3.0971, "test": 3.2098, "litterature": 15.9854, "litterature_propre": 17.0838, "anglais": 60.6957, "wikitext2": 59.729, "permute": 1356.6433}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"eval_n2_propre import\\|from tools.eval_n2_propre\" --include='*.py' . | grep -v '.venv'", "description": "Find importers of eval_n2_propre"}`

  ```
./journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/eval_200k.py:26:from tools.eval_n2_propre import charge, charger_bytes, ordre_vdc  # noqa: E402
./journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/eval_fenetre.py:32:from tools.eval_n2_propre import charge, charger_bytes  # noqa: E402
./journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/eval_longueurs.py:24:from tools.eval_n2_propre import charge, charger_bytes  # noqa: E402
./journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/mirroir_copie.py:33:from tools.eval_n2_propre import charge  # noqa: E402
./journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/eval_production.py:27:from tools.eval_n2_propre import charge, charger_bytes, ordre_vdc  # noqa: E402
./work/n2h/fenetre.py:14:from tools.eval_n2_propre import charge, charger_bytes, ppl_protocole
./work/n2i/typoglycemie.py:14:from tools.eval_n2_propre import charge, ppl_protocole
./work/n2j/evalue_canal.py:6:from tools.eval_n2_propre import charge, charger_bytes, departs_vdc
./work/n2j/typo_sans.py:4:from tools.eval_n2_propre import charge, charger_bytes
./work/n2k/evalue.py:5:from tools.eval_n2_propre import charge, charger_bytes, ppl_prot
… [780 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"eval_n2_propre\" tools/porte-*.sh 2>/dev/null | head", "description": "Find gate scripts using eval_n2_propre"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 300 ~/gpu-env/bin/python - <<'EOF' 2>&1 | grep -v Loading\nimport pathlib, torch, sys\nfrom work.n2ac.rope_model import charge_rope\nfrom tools.eval_n2_propre impo … [606 caractères tronqués]`

  ```
val 1024 2.7856
permute 1024 1880.6648
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 300 ~/gpu-env/bin/python - <<'EOF' 2>&1 | grep -v Loading\nimport pathlib, torch, sys\nfrom work.n2ac.rope_model import charge_rope\nfrom tools.eval_n2_propre impo … [607 caractères tronqués]`

  ```
perm texte, canal inchange 1692.3919
perm texte, canal permute   1880.6648
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 600 ~/gpu-env/bin/python /tmp/eval_n2_propre_rope.py work/n2ac/rope2048-20k.pt --rope --canal-dir data/corpus_propre --longueurs 128,1024 2>&1 | grep -v Loading",  … [76 caractères tronqués]`

  ```
{"fichier": "rope2048-20k.pt", "params": 34301224, "val": 5.4773, "test": 5.1464, "litterature": 20.8831, "litterature_propre": 20.9998, "anglais": 24.0812, "wikitext2": 24.2146, "permute": 261.2092, "longueurs": {"128": 5.4773, "1024": 4.6321}}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf /tmp/propre_test_j41 && mkdir -p /tmp/propre_test_j41 && cp data/corpus_propre/test.txt /tmp/propre_test_j41/val.txt && cp data/corpus_propre/test.canal /tmp/propre_test_j41/val.canal && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.  … [260 caractères tronqués]`

  ```
L128 : 3.0649
  L512 : 2.8875
  L1024 : 2.8566
{"fichier": "propre512-8k.pt", "val": "/tmp/propre_test_j41", "positions": "rope", "L128": 3.0649, "L512": 2.8875, "L1024": 2.8566}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat work/n2h/A-propre-g1.json | head -40", "description": "Read absolute control result"}`

  ```
{
 "init": "work/n2h/base-propre.pt",
 "corpus": "fr",
 "graine": 1,
 "plan": [
  [
   128,
   10000,
   0.0001
  ],
  [
   128,
   10000,
   3e-05
  ]
 ],
 "lot": 16,
 "temperature": 2.0,
 "alpha": 0.7,
 "tetes": true,
 "pas": 20000,
 "octets_vus": 40960000,
 "perte_finale": 43.96200942993164,
 "ppl_128_lot16": 3.1924699109630237,
 "ppl_128_lot8": 3.167137889124645,
 "ppl_129_lot15": 3.173856155927436,
 "ppl_permute": 1380.8954794478022,
 "precision_main": 0.664794921875,
 "precision_early": [
  0.599365234375,
  0.6451416015625,
  0.6680908203125
 ],
 "duree_s": 1381.8896000385284,
 "positions_aleatoires": 0,
 "courbe": [
  {
   "pas": 250,
   "seq": 128,
   "perte": 78.6990737915039,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la reports/rapport-coordination-n2.* 2>&1", "description": "Check target files do not exist"}`

  ```
ls: cannot access 'reports/rapport-coordination-n2.*': No such file or directory
[exit code: 2]
  ```

- **write** `{"content": "# N2 — la coordination du mètre : `--rope` ne suffit pas, il faut le canal\n\n> **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-13 · **HEAD mesuré** :\n> `ced21933` · **Verdict** : `tools/eval_n2_propre.py` lit les checkpoints RoPE comme des positions\n> absolues … [18307 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "{\n  \"date\": \"2026-11-13\",\n  \"head\": \"ced21933\",\n  \"ligne\": \"N2\",\n  \"objet\": \"coordination du mètre eval_n2_propre.py pour les checkpoints RoPE\",\n  \"fiche\": \"reports/rapport-coordination-n2.md\",\n  \"verdict\": \"eval_n2_propre.py lit les checkpoints RoPE comme d … [11907 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-coordination-n2.json > /tmp/coordination-n2.pretty.json && echo JSON-OK && wc -l reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json /tmp/coordination-n2.pretty.json", "descrip … [36 caractères tronqués]`

  ```
JSON-OK
  392 reports/rapport-coordination-n2.md
  246 reports/rapport-coordination-n2.json
  246 /tmp/coordination-n2.pretty.json
  884 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/native_model.py tools/entrainer_native.py tools/eval_n2_propre.py reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json; find work/n2ac work/n2h work/n2j -name '__pycache__' -newermt '2026-1 … [90 caractères tronqués]`

  ```
?? reports/rapport-coordination-n2.json
?? reports/rapport-coordination-n2.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md</path>
<type>file</type>
<content>
1: # N2 — la coordination du mètre : `--rope` ne suffit pas, il faut le canal
2: 
3: > **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-13 · **HEAD mesuré** :
4: > `ced21933` · **Verdict** : `tools/eval_n2_propre.py` lit les checkpoints RoPE comme des positions
5: > absolues et rend **8,0225** sur `propre512-8k` à 128 octets, là où le mètre RoPE rend **2,9726**
6: > à 128 et **2,7856** à 1 024. Le correctif `--rope` est **nécessaire mais non suffisant** : le
7: > checkpoint de la porte a été entraîné **avec le canal**, et `--rope` seul rend **40,0658** à 128.
8: > Le correctif validé est **`--rope --canal-dir`** ; la commande qui donne 2,79 aujourd'hui est le
9: > mètre existant `work/n2ac/eval_longueurs.py --rope`. **Aucun fichier de N2 modifié**
10: > (`native_model.py`, `entrainer_native.py`, `work/` intacts).
11: 
12: ## Ce que cette fiche est, et n'est pas
13: 
14: - **Est** : une coordination en lecture seule. Elle rejoue les mesures, isole **deux** causes,
15:   propose un correctif daté et donne les commandes exactes.
16: - **N'e
… [18770 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. ~/gpu-env/bin/python - <<'EOF'\nimport torch\nfrom tools.native_model import NativeConfig, NativeModel\nm=NativeModel(NativeConfig(d_model=32, expert_hidden=16))\nr=m.load_state_dict(m.state_dic … [119 caractères tronqués]`

  ```
<class 'torch.nn.modules.module._IncompatibleKeys'> [] []
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find tools work -name '__pycache__' -newermt '2026-11-13 21:35' 2>/dev/null | head -20; find tools work -name '*.pyc' -newermt '2026-11-13 21:35' 2>/dev/null | head -20", "description": "Check no bytecode written into N2 or tools"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | sed -n '1,40p'", "description": "Review working tree status"}`

  ```
M docs/pilotage/references-non-regression.md
D  journal/2026-11-13/README.md
D  journal/2026-11-13/docs.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/digest.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 m tools/structures
?? journal/2026-11-13/
?? reports/rapport-coordination-n2.json
?? reports/rapport-coordination-n2.md
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls data/corpus_litt_propre 2>/dev/null; ls data | grep -E 'litt|en|wikitext' | head -20", "description": "Check canal availability for OOD corpora"}`

  ```
test.txt
train.txt
val.txt
alignement
corpus_en.txt
corpus_en_val.txt
corpus_fr_litterature.txt
corpus_litt_propre
corpus_mixte_litt2.txt
corpus_mixte_litt.txt
corpus_pdf_documents
corpus_wiki_en
corpus_wiki_en_texte
opensubtitles
pensee-etats-7b.npz
pensee-etats.npz
raisonnement
wiki_en
wikitext2_test.txt
wikitext2_test.txt.ids
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "old_string": "  **1 692,3919** à 1 024 avec le canal inchangé (chiffre publié, reproduit) ; en permutant **aussi\n  le canal**, on obtient **1 880,6648**. Les deux sont trois ordres de grandeur au-de … [292 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "old_string": "- **`work/` et `data/` sont gitignorés** : la commande est locale à Hauru ; un clone neuf ne peut\n  pas la rejouer sans le checkpoint, le corpus et `rope_model.py`. Le sha256 du `.pt`  … [293 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "old_string": "- **Références** : [`rapport-etat-n2`](rapport-etat-n2.md),\n  [`rapport-n2-porte-propre`](rapport-n2-porte-propre.md),\n  [`n2-porte-propre.json`](n2-porte-propre.json).\n- **Aucun com … [696 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json", "new_string": "        \"verdict\": \"le mètre est sensible à l'ordre ; les deux permutations valent 600 à 700 fois la valeur propre\"", "old_string": "        \"verdict\": \"le mètre est sensible à … [96 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "Tant que (1) ou (2) n'est pas fait, le correctif est **local à Hauru**, comme le mètre actuel.\n\n### 3.6 Décision recommandée\n\n**Ne pas livrer `--rope` seul** : il rend 40,07 au lieu … [865 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json", "new_string": "    \"durabilite\": \"work/ est gitignoré : --rope importe work/n2ac/rope_model.py, donc le correctif est local à Hauru. Pour un clone neuf, promouvoir rope_model.py en tools/rope_mod … [759 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-coordination-n2.json > /dev/null && echo JSON-OK; grep -n \"trois ordres\\|première fois\" reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json || true", "description": "Revalid … [32 caractères tronqués]`

  ```
JSON-OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\np=pathlib.Path('reports/rapport-coordination-n2.json')\nd=json.loads(p.read_text())\nprint('top keys:', list(d))\nprint('verdict:', d['verdict'][:120])\nprint('courbes:', list(d['chiffres']['p … [118 caractères tronqués]`

  ```
top keys: ['date', 'head', 'ligne', 'objet', 'fiche', 'verdict', 'aucune_modification_n2', 'bug', 'checkpoints', 'chiffres', 'correctif', 'commande_n2', 'limites', 'fichiers_lus_non_modifies', 'references']
verdict: eval_n2_propre.py lit les checkpoints RoPE comme des positions absolues et rend 8,0225 sur propre512-8k à 128 octets, co
courbes: ['absolu_sans_canal', 'rope_sans_canal', 'rope_avec_canal']
commands: ['aujourdhui_sans_patch', 'apres_patch', 'test_1024', 'temoin_bug']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in reports/rapport-coordination-n2.json reports/rapport-etat-n2.md reports/rapport-n2-porte-propre.md reports/n2-porte-propre.json tools/canal_structure.py work/n2ac/rope_model.py work/n2ac/eval_longueurs.py work/n2j/evalue_can … [284 caractères tronqués]`

  ```
CHECKED
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\ns=pathlib.Path('reports/rapport-coordination-n2.md').read_text()\nprint('fences', s.count('```'))\nprint('lines', len(s.splitlines()))\nprint('tabs', s.count('\\t'))\nEOF", "description": "Check mar … [25 caractères tronqués]`

  ```
fences 28
lines 407
tabs 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test -f reports/rapport-coordination-n2.md && echo FICHE-OK; test -f reports/rapport-coordination-n2.json && echo JSON-OK", "description": "Run task acceptance check"}`

  ```
FICHE-OK
JSON-OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run documentation review", "timeoutMs": 130000}`

  ```
revue de documentation · 714 fiche(s) · 807 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 713 fichiers, le disque en a 714
     · compteurs : en-cours.md dit 806 JSON, le disque en a 807
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "- **Fichier neuf, non ajouté à `reports/README.md` ni à `reports/INDEX.md`** (ce serait modifier\n  un existant) ; il est découvrable par son nom, comme les autres fiches de coordinatio … [766 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 bash tools/porte-tableaux.sh 2>&1 | tail -40; echo \"exit=$?\"", "description": "Run table formatting gate", "timeoutMs": 130000}`

  ```
✅ 1772 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3847 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-13)
exit=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "```bash\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nmkdir -p /tmp/propre_test\ncp data/corpus_propre/test.txt  /tmp/propre_test/val.txt\ncp data/corpus_propre/test.canal /tmp/p … [625 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "```bash\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nPYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \\\n  ~/gpu-env/bin/python tools/eval_n2_propre.py \\\n  work/ … [227 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json", "new_string": "      \"commande\": \"cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p /tmp/propre_test && cp data/corpus_propre/test.txt /tmp/propre_test/val.txt && cp data/corpus_prop … [625 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json", "new_string": "      \"commande\": \"cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python tools/eval_n2_propre.py  … [229 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-coordination-n2.json > /dev/null && echo JSON-OK; bash tools/porte-tableaux.sh 2>&1 | tail -5", "description": "Revalidate JSON and tables"}`

  ```
JSON-OK
  ✅ 1772 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3847 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-13)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "Les autres corpus (`litterature`, `anglais`, `wikitext2`) n'ont pas de `.canal` : ils restent\nsans canal, et leurs chiffres ne sont **pas** comparables pour ce checkpoint (voir § 5).\n … [355 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "- **Le canal n'est pas disponible pour les corpus hors domaine** : les colonnes `litterature`,\n  `litterature_propre`, `anglais`, `wikitext2` de `eval_n2_propre` sur ce checkpoint ne s … [733 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json", "new_string": "    \"Les corpus hors domaine n'ont pas de .canal : les colonnes litterature/litterature_propre/anglais/wikitext2 de eval_n2_propre ne sont pas comparables pour ce checkpoint (52,29 / … [256 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-coordination-n2.json > /dev/null && echo JSON-OK && bash tools/porte-tableaux.sh 2>&1 | tail -4", "description": "Final JSON and table validation"}`

  ```
JSON-OK
  ✅ 1772 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3847 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-13)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "Le champ `val` de l'outil reste à 128 après le correctif **complet (`--rope --canal-dir`)** : il\nvaudra **2,9726**. Le chiffre de la porte est `longueurs[\"1024\"]` = **2,7856**. Il ne … [241 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "> mètre existant `work/n2ac/eval_longueurs.py --rope`. **Aucun fichier de N2 modifié**\n> (`native_model.py`, `entrainer_native.py`, `work/` intacts).\n\n**En trois lignes.** (1) `charg … [496 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-coordination-n2.json > /dev/null && echo JSON-OK && bash tools/porte-tableaux.sh 2>&1 | tail -4 && wc -l reports/rapport-coordination-n2.md", "description": "Final checks after summary addition"}`

  ```
JSON-OK
  ✅ 1772 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3847 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-13)
420 reports/rapport-coordination-n2.md
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json", "new_string": "        \"detail\": \"charge() construit NativeModel (table de positions apprise absolue) au lieu de NativeModelRoPE ; les checkpoints N2 depuis le 02/11 sont des NativeModelRoPE, ave … [295 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-coordination-n2.json > /dev/null && echo JSON-OK", "description": "Validate JSON after wording fix"}`

  ```
JSON-OK
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "- **Compteurs** : cette fiche ajoute **1 fiche** et **1 JSON** aux compteurs de `en-cours`\n  (au moment de l'écriture : 713 → 714 fiches, 806 → 807 JSON). La session principale les met … [298 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json; git status --short reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json tools/native_model.py tools/entrainer_native.py tools/eval_n2_p … [59 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane 11915 13 nov 21:52 reports/rapport-coordination-n2.json
-rw-------. 1 stephane stephane 20063 13 nov 21:52 reports/rapport-coordination-n2.md
?? reports/rapport-coordination-n2.json
?? reports/rapport-coordination-n2.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 644 reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json && ls -l reports/rapport-coordination-n2.*", "description": "Set report file permissions to 644"}`

  ```
-rw-r--r--. 1 stephane stephane 11915 13 nov 21:52 reports/rapport-coordination-n2.json
-rw-r--r--. 1 stephane stephane 20063 13 nov 21:52 reports/rapport-coordination-n2.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "limit": 40}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "offset": 280, "limit": 100}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md</path>
<type>file</type>
<content>
1: # N2 — la coordination du mètre : `--rope` ne suffit pas, il faut le canal
2: 
3: > **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-13 · **HEAD mesuré** :
4: > `ced21933` · **Verdict** : `tools/eval_n2_propre.py` lit les checkpoints RoPE comme des positions
5: > absolues et rend **8,0225** sur `propre512-8k` à 128 octets, là où le mètre RoPE rend **2,9726**
6: > à 128 et **2,7856** à 1 024. Le correctif `--rope` est **nécessaire mais non suffisant** : le
7: > checkpoint de la porte a été entraîné **avec le canal**, et `--rope` seul rend **40,0658** à 128.
8: > Le correctif validé est **`--rope --canal-dir`** ; la commande qui donne 2,79 aujourd'hui est le
9: > mètre existant `work/n2ac/eval_longueurs.py --rope`. **Aucun fichier de N2 modifié**
10: > (`native_model.py`, `entrainer_native.py`, `work/` intacts).
11: 
12: **En trois lignes.** (1) `charge()` construit `NativeModel` absolu et `ppl_protocole()` oublie le
13: canal : **deux** causes, pas une. (2) `--rope` seul rend **40,07** ; `--rope --canal-dir` rend
14: **2,9726** à 128 e
… [1374 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md</path>
<type>file</type>
<content>
280: clone neuf ne peut donc pas utiliser le correctif tel quel. Pour rendre le mètre durable, la
281: session N2 doit, dans l'ordre :
282: 
283: 1. **promouvoir** `work/n2ac/rope_model.py` en `tools/rope_model.py` (le module ne dépend que de
284:    `tools.native_model`) et importer `from tools.rope_model import charge_rope` ;
285: 2. ou intégrer RoPE dans `tools/native_model.py` via un champ de configuration
286:    (`positions: "absolues" | "rope"`), ce qui est un changement d'architecture plus lourd ;
287: 3. épingler le sha256 du `.pt` et les valeurs de référence dans la future `tools/porte-n2.sh`.
288: 
289: Tant que (1) ou (2) n'est pas fait, le correctif est **local à Hauru**, comme le mètre actuel.
290: 
291: ### 3.6 Décision recommandée
292: 
293: **Ne pas livrer `--rope` seul** : il rend 40,07 au lieu de 2,79. Deux chemins propres :
294: 
295: - **(A) `--rope --canal-dir` dans `eval_n2_propre.py`** : le mètre générique devient correct pour
296:   la porte et pour l'OOD canalisé. C'est le plus utile, et c'est celui qui a été validé en copie
297:   ho
… [3472 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "- **(A) `--rope --canal-dir` dans `eval_n2_propre.py`** : le mètre générique devient correct pour\n  la porte (val/test) ; l'OOD reste à canalierser par un autre chemin, faute de `.cana … [463 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md", "new_string": "Les deux dernières lignes (validation) sont **identiques au chiffre près** : le correctif proposé\nreproduit le mètre de référence. Le `1024` de la première ligne est mesuré avec la lis … [386 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test -f reports/rapport-coordination-n2.md && echo FICHE-OK && python3 -m json.tool reports/rapport-coordination-n2.json > /dev/null && echo JSON-OK && bash tools/porte-tableaux.sh 2>&1 | tail -3", "description": "Final acceptance an … [14 caractères tronqués]`

  ```
FICHE-OK
JSON-OK
  ✅ 1772 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3847 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-13)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/native_model.py tools/entrainer_native.py tools/eval_n2_propre.py work/ reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json | head -20", "description": "Confirm only new coordination files … [2 caractères tronqués]`

  ```
?? reports/rapport-coordination-n2.json
?? reports/rapport-coordination-n2.md
  ```

### 🤖 Assistant

Fiche écrite, avec son JSON :

- `reports/rapport-coordination-n2.md`
- `reports/rapport-coordination-n2.json`

**Le résultat principal corrige la prémisse** : le bug a **deux** causes, pas une.

1. `charge()` construit `NativeModel` (positions absolues) au lieu de `NativeModelRoPE` ; `strict=False` charge les 127 clés sans alerte.
2. `ppl_protocole()` ne passe **pas le canal**, alors que `propre512-8k` a été entraîné avec `--canal data/corpus_propre/train.canal`.

Conséquence mesurée : **`--rope` seul rend 40,0658 à 128**, pas 2,79. Il faut `--rope --canal-dir` pour retrouver **2,9726 / 2,8988 / 2,8443 / 2,7856**.

Le piège de longueur est explicité : **8,02** est le `val` à **128** ; **2,79** est la PPL à **1 024**. À longueur égale 128, la référence est **2,9726**.

**Commande exacte pour la session N2, aujourd’hui sans patch** (elle donne 2,79) :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \
  ~/gpu-env/bin/python work/n2ac/eval_longueurs.py \
  work/n2ac/propre512-8k.pt --rope \
  --longueurs 128,256,512,1024 --val data/corpus_propre
```

Attendu : `2.9726 / 2.8988 / 2.8443 / 2.7856`.

La fiche contient aussi le diff proposé (`--rope`, `--canal-dir`, `--longueurs` liste avec 1024, garde-fou sidecar), la commande après patch, le test à 1 024 (`2,8566`, manque `0,3566`) et les contrôles négatifs (`1 692,39` / `1 880,66`).

**Aucun fichier de N2 modifié** (`native_model.py`, `entrainer_native.py`, `work/` intacts), aucun commit. Vérifications : JSON valide, `porte-tableaux` verte (tableaux + 3 847 liens). La revue de documentation signale seulement les deux compteurs à mettre à jour par la session principale : `713 → 714` fiches, `806 → 807` JSON.

