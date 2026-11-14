# Session DSH — relecture

- identifiant : `24e34ad3-f423-4394-bb1c-74a6930a57e5`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 09:53:59
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **intégrer le tagger POS par API DeepSeek dans la CLI, en option** (décision 1A du 14/11). La mesure est faite : le tagger vaut **0,9475** contre **0,8625** pour l'heuristique sur le gold 612 (**+8,49 pts**), pour ~0,04 $ sur tout le corpus. Il faut l'exposer **sans** changer le défaut (hors ligne, déterministe).

**Les pièces existent** (lis-les avant d'écrire) :
- `tools/llm/deepseek.py` : `Client(cle=..., ...)` lit `DEEPSEEK_API_KEY`/`DSH_API_KEY`, `client.demande(prompt, system=..., temperature=..., max_tokens=...)` → une réponse avec `.contenu`, `.usage`, `.latence_s` ; cache disque ; un mode `--dry-run` déterministe (tests sans réseau).
- `tools/bloc_linguistique.py` : `NeuronalLLMPOS(modele, transport=...)` (le tagger, transport injectable), `NeuronalLLMCompose`, `Cascade(h, compose, seuil=..., priorite_syntagme="confiance")`, `Parallele`.
- `tools/tests/linguistique/qualifier_quatre_modes.py` : le harnais qui construit `transport` → `client.demande` → `NeuronalLLMPOS("deepseek-chat", transport=transport)` ; recopie ce câblage.
- `tools/drave.py` : la CLI (`analyser`, `evaluer`, `rejouer`), `_dumps`, `_sur`, la clé lue dans `~/.config/drave/deepseek.key` par le chantier.

**À faire** :
1. Dans `tools/drave.py`, ajouter `--tagger` à `analyser` et `evaluer` : quand il est posé, construire le `Client` (clé : `DEEPSEEK_KEY_FILE` puis `~/.config/drave/deepseek.key` puis `DEEPSEEK_API_KEY`), le `transport`, `NeuronalLLMPOS("deepseek-chat", transport=transport)` + `NeuronalLLMCompose` + `Cascade(h, compose, seuil=0.6)`, et analyser avec. **Le défaut reste l'heuristique.** Si la clé manque : message clair, code 4, **jamais** de trace de la clé.
2. **Le cache** : réutiliser le cache du client (ou un cache mémoire par texte) ; deux analyses du même texte ne doivent pas refaire d'appel.
3. **Les tests** dans `tools/tests/test_tagger_api.py` (fichier neuf) : sans réseau, avec un **transport factice** (une fonction qui rend un JSON de POS valide) → la cascade remplace bien les POS, le JSON reste valide (schéma v1), le défaut est inchangé ; un test « sans clé » → code 4.
4. **La mesure** : sur 20 phrases du gold (ou le harnais `qualifier_tagger_612.py` avec `--limite 20` si la clé est là — sinon, dis-le), la POS de la cascade vs l'heuristique ; note le delta et le coût (appels, tokens).
5. **La doc** : `docs/produit/README.md` § « le tagger en option » (la clé, le coût, le hors-ligne par défaut) ; une fiche `reports/rapport-tagger-option.md` + `reports/pensee-tagger-option.json`.
6. **Contraintes** : ne touche pas S/D/N2 ; ne commite pas ; les portes (`revue_documentation`, `taille_documents`, `test_produit`) doivent passer ; le smoke test existant doit rester vert.

Rends un résumé : la commande, le résultat mesuré, les tests, les limites.
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

⏵ Je lis les pièces existantes (deepseek.py, bloc_linguistique.py, drave.py, harnais)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && git branch --show-current && ls", "description": "Vérifier l'état git et la branche"}`

  ```
MM journal/2026-11-14/README.md
MM journal/2026-11-14/distribue.md
MM journal/2026-11-14/docs.md
MM journal/2026-11-14/memoire.md
MM journal/2026-11-14/mesures.md
MM journal/2026-11-14/moteur.md
MM journal/2026-11-14/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
MM journal/sessions/session-a68c9aaf-bd76-458b-8501-5a29431b2e10/digest.md
MM journal/sessions/session-a68c9aaf-bd76-458b-8501-5a29431b2e10/rapport.md
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
s/v7
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
r
… [80 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/llm/deepseek.py tools/bloc_linguistique.py tools/drave.py tools/tests/linguistique/qualifier_quatre_modes.py 2>&1; ls tools/tests/ | head -50", "description": "Compter les lignes des pièces clés"}`

  ```
272 tools/llm/deepseek.py
  2906 tools/bloc_linguistique.py
   598 tools/drave.py
   135 tools/tests/linguistique/qualifier_quatre_modes.py
  3911 total
cic
code
documents
linguistique
maths
__pycache__
qualifier_politique_drvm.py
qualifier_porte_bouge_drvm.py
qualifier_porte_drvm.py
qualifier_porte_fenetre_drvm.py
qualifier_porte_minute_drvm.py
qualifier_porte_mobile_drvm.py
qualifier_porte_sto_drvm.py
qualifier_porte_sto_graines.py
tableaux
test_panini_334.py
test_pensee_politique.py
test_pensee_store.py
test_produit_libre.py
test_produit.py
test_restitution.py
test_schema_produit.py
test_verificateur_cic.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/llm/deepseek.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/llm/deepseek.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """deepseek.py — le professeur externe, sans poids locaux.
3: 
4: POURQUOI CE MODULE. Le dépôt garde ses GPU et ses CPU pour le **modèle natif**
5: Drave (`entrainer_moteur.py`, `drave-core`) et pour les mesures **boîte blanche**
6: (perplexité, activations, flux, sondes). Le **langage** — traduire, juger,
7: générer, évaluer — passe par une API : on ne charge plus un Qwen de 7/14/32 B
8: pour cela. DeepSeek est ce **professeur externe** ; ses sorties peuvent servir à
9: entraîner/distiller l'élève natif (autorisation explicite du propriétaire de la
10: licence).
11: 
12: CE QUE LE MODULE NE FAIT PAS. Il ne remplace pas les mesures d'états internes :
13: une API ne donne pas les poids ni les activations. Il ne met **jamais** la clé
14: dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
15: paquet externe : `urllib` suffit.
16: 
17: CONTRAT.
18: - `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
19: - `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
20: - `DEE
… [11956 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """drave.py — le point d'entrée produit du bloc linguistique.
3: 
4: Une seule commande, quatre gestes, hors ligne et déterministe :
5: 
6:     python3 tools/drave.py analyser "Le chat dort."
7:     python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
8:     python3 tools/drave.py evaluer
9:     python3 tools/drave.py evaluer --gold --json
10:     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
11:     python3 tools/drave.py restituer "Le chat dort."
12:     python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
13:     python3 tools/drave.py --version
14: 
15: Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
16: avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
17: **restitution v0** (annotation → surface, avec la fidélité du miroir). La restitution est un
18: **codec de surface** : elle reconstruit depuis le niveau `graphème`, pas un décodeur neuronal.
19: Ce 
… [29593 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class NeuronalLLMPOS\\|class NeuronalLLMCompose\\|class Cascade\\|class Parallele\\|def __init__\\|transport\" tools/bloc_linguistique.py | head -80", "description": "Repérer les classes neuronales dans le bloc"}`

  ```
801:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
1842:    def __init__(self, profils: dict[str, dict] | None = None):
1898:    def __init__(self, modele: str | pathlib.Path, llama_cli: str = "llama-cli",
1968:class NeuronalLLMPOS:
1978:    180 chargements. `transport` est injectable pour tester le contrat sans modèle.
1987:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18081",
1989:                 transport=None, cache: bool = True):
1995:        self.transport = transport or self._post
2045:            sortie = self.transport(self._invite(noms), grammaire, max_jetons)
2116:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
2118:                 transport=None, cache: bool = True):
2124:        self.transport = transport or self._post
2179:            sortie = self.transport(self._invite(noms), grammaire, max_jetons)
2234:class NeuronalLLMCompose:
2246:    def __init__(self, pos: BlocLinguistique, chunks: BlocLinguistique,
2296:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
2298:                 transport=None, ca
… [421 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_quatre_modes.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_quatre_modes.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """qualifier_quatre_modes.py — la porte des quatre modes du contrat de L sur le gold 432.
3: 
4: Les quatre modes du contrat (`docs/theorie/contrat-bloc-langue.md`) mesurés sur le
5: **même** gold réel 432 :
6: 
7:   1. heuristique seule ;
8:   2. neuronal seul (le composite POS + syntagmes, via l'API DeepSeek — règle 11) ;
9:   3. parallèle (`Parallele`) ;
10:   4. cascade (`Cascade`, seuil 0,6).
11: 
12: Mêmes mesures que la cascade : POS, syntagmes F1, tête F1, acte, fraction, refus.
13: Le coût est mesuré : appels du tagger, tokens API, latence, durée.
14: 
15: Usage :
16:     DEEPSEEK_KEY_FILE=~/.config/drave/deepseek.key \
17:     python3 tools/tests/linguistique/qualifier_quatre_modes.py --limite 3
18: """
19: from __future__ import annotations
20: 
21: import argparse
22: import json
23: import pathlib
24: import statistics
25: import sys
26: import time
27: 
28: RACINE = pathlib.Path(__file__).resolve().parents[3]
29: sys.path.insert(0, str(RACINE))
30: 
31: from tools.bloc_linguistique import (PRIORITE_NIV
… [6059 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 1940, "limit": 300}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 2230, "limit": 130}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1940:         script = d.get("script", detecter_script(texte))
1941:         etiquettes = []
1942:         for e in d.get("etiquettes", []):
1943:             if e.get("niveau") not in NIVEAUX:
1944:                 continue
1945:             debut_e = max(0, min(int(e.get("debut", 0)), len(texte)))
1946:             fin_e = max(debut_e, min(int(e.get("fin", debut_e)), len(texte)))
1947:             etiquettes.append(Etiquette(e["niveau"], str(e.get("type", "")), str(e.get("valeur", "")),
1948:                                         debut_e, fin_e, self.nom, float(e.get("confiance", 0.5)),
1949:                                         langue=lg, script=script))
1950:         return Annotation(texte=texte, langue=lg, script=script, etiquettes=etiquettes,
1951:                           source=self.nom, trace=[{"etape": "neuronal-llm", "modele": self.modele}],
1952:                           cout={"octets": len(texte.encode("utf-8", "replace")), "etiquettes": len(etiquettes),
1953:                                 "duree_s": round(time.perf_counter() - t0, 6)})
1954: 
1
… [16965 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
2230:     return Etiquette("syntagme", typ, texte[debut:fin], debut, fin, nom, confiance,
2231:                      langue=langue, script=script, meta={"bio": True})
2232: 
2233: 
2234: class NeuronalLLMCompose:
2235:     """Deux taggers neuronaux, **une** annotation : POS + syntagmes, même contrat.
2236: 
2237:     Le composite n'invente rien : il appelle les deux taggers (chacun avec son cache), réunit
2238:     leurs étiquettes et leurs traces, et laisse `source = neuronal`. C'est le bloc que la
2239:     cascade complète branche ; la pragmatique reste à l'heuristique, qui la tient à 1,0 sur le
2240:     gold. Un refus d'un des deux taggers n'efface pas l'autre : l'annotation est **partielle**,
2241:     et `refus` dit lequel a manqué.
2242:     """
2243: 
2244:     nom = "neuronal"
2245: 
2246:     def __init__(self, pos: BlocLinguistique, chunks: BlocLinguistique,
2247:                  pragma: BlocLinguistique | None = None):
2248:         self.pos = pos
2249:         self.chunks = chunks
2250:         self.pragma = pragma
2251: 
2252:     def analyser(self, te
… [6426 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 110, "offset": 2630}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
2630:                       source=source, unites_semantiques=unites,
2631:                       fraction_semantique=round(fraction, 4),
2632:                       trace=a.trace + b.trace + [{"etape": "fusion", "source": source,
2633:                               "a": a.source, "b": b.source}],
2634:                       cout={"octets": len(a.texte.encode()),
2635:                             "etiquettes": len(etiquettes),
2636:                             "duree_s": round(a.cout.get("duree_s", 0) + b.cout.get("duree_s", 0), 6)})
2637: 
2638: 
2639: class Parallele:
2640:     """Les deux implémentations en parallèle : le contrat est le même, la fusion est explicite."""
2641: 
2642:     nom = "parallele"
2643: 
2644:     def __init__(self, blocs: Sequence[BlocLinguistique],
2645:                  priorite_syntagme: str = "heuristique",
2646:                  priorite_par_niveau: dict | None = None,
2647:                  priorite_par_type: dict | None = None):
2648:         if len(blocs) != 2:
2649:             raise ValueError("le parallèle attend exactement deux 
… [4671 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/tests/linguistique/ | head -40 && grep -rn \"qualifier_tagger\" --include=*.py --include=*.sh . | head -20", "description": "Chercher le harnais qualifier_tagger_612"}`

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
./tools/tests/linguistique/qualifier_tagger_612.py:2:"""qualifier_tagger_612.py — le tagger POS API sur le gold 612 (hand 20 + reel 432 + synth 160).
./tools/tests/linguistique/qualifier_tagger_612.py:16:    PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_612.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_612.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """qualifier_tagger_612.py — le tagger POS API sur le gold 612 (hand 20 + reel 432 + synth 160).
3: 
4: POURQUOI. Le banc `qualifier_quatre_modes.py` ne charge que `gold_reel.json` (432 phrases) ; le
5: gold courant en compte 612, et le tagger n'y a jamais été mesuré. Ce banc ajoute la ventilation
6: hand / reel / synth, la latence réelle des appels et le modèle effectivement renvoyé par l'API.
7: Il ne modifie aucun autre fichier et n'écrit que le JSON demandé.
8: 
9: COÛT. Deux appels par phrase (POS + syntagmes), partagés par les six modes grâce au cache des
10: tagger : ~1 214 appels, ~360 k tokens, ~20 min pour 612 phrases.
11: 
12: USAGE.
13:     DEEPSEEK_KEY_FILE=$HOME/.config/drave/deepseek.key \
14:     DEEPSEEK_CACHE=$(mktemp -d /tmp/j43-cache.XXXX) \
15:     DEEPSEEK_MODEL=deepseek-chat \
16:     PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
17:       --sortie /tmp/tagger-612.json
18: 
19: La clé n'est jamais lue en dur : `tools/llm/deepseek.py` lit `DEEPSEEK_API_KEY` ou le fichier
… [8424 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,80p tools/tests/linguistique/qualifier_cascade.py && echo ---- && sed -n 1,60p tools/tests/linguistique/evaluer_gold.py", "description": "Lire le harnais 612 et l'évaluateur gold"}`

  ```
#!/usr/bin/env python3
"""qualifier_cascade.py — la cascade **complète** avec le vrai modèle (POS + syntagmes).

Le bloc neuronal est `NeuronalLLMCompose` : `NeuronalLLMPOS` + `NeuronalLLMChunks`, appelés
une fois par phrase, réunis en une annotation. La cascade garde l'heuristique pour la
pragmatique (acte 1,0 sur le gold) et applique la politique `confiance` au syntagme.

On mesure six lectures : heuristique, neuronal composite, cascade POS seule, cascade
syntagmes seule, cascade complète (confiance), cascade complète (priorité heuristique). Les
quatre dernières sont les **ablations** : la complète doit valoir les parties, sans perte.

    python3 tools/tests/linguistique/qualifier_cascade.py --endpoint http://127.0.0.1:18082 \
        --workers 1 --sortie reports/pensee-gold-cascade.json

Le serveur est sur CPU (`-ngl 0`) : les GPU de N2 restent intacts.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bloc_linguistique as
… [4195 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la ~/.config/drave/deepseek.key 2>&1; echo \"DEEPSEEK_KEY_FILE=${DEEPSEEK_KEY_FILE:-}\"; echo \"DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY:+posée}\"; ls data/deepseek/cache 2>/dev/null | wc -l", "description": "Vérifier la présence de l … [19 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane 36  3 nov 11:15 /home/stephane/.config/drave/deepseek.key
DEEPSEEK_KEY_FILE=
DEEPSEEK_API_KEY=
3596
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p tools/tests/test_produit.py && echo ==== && sed -n 1,80p tools/tests/linguistique/test_bloc_linguistique.py", "description": "Lire les tests produit existants"}`

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


… [7091 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"1A\\|tagger\" journal/2026-11-14 docs/pilotage reports/ 2>/dev/null | head -20; echo ----; grep -rn \"0,9475\\|0.9475\\|0,8625\\|0.8625\\|tagger\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-14/*.md … [91 caractères tronqués]`

  ```
journal/2026-11-14/mesures.md
docs/pilotage/semaine-autonome.md
docs/pilotage/roadmap.md
docs/pilotage/en-cours.md
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
reports/rapport-file-taches.md
----
docs/pilotage/en-cours.md:95:- **J5.1 / J10.1 / J13.1 / J14.1 — les bilans et la clôture** : semaine (F1 **0,7533 → 0,7902**, tagger **0,9475** ; [rapport](../../reports/rapport-semaine.md)) ; chantier **20/21**, attachement **236 → 238**, 5 timeouts, 1 échec (J5.2), D1–D20, R1–R30 ; [bilan](../../reports/rapport-bilan-chantier.md) ; **J13.1** — tableau des mesures : **612/602** ; [tableau](../../reports/rapport-tableau-mesures.md) ; **J14.1** — clôture (**84/
… [6561 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i \"tagger\\|612\\|quatre\" ; echo ----; cat reports/pensee-tagger-612.json 2>/dev/null | head -60", "description": "Chercher les rapports tagger existants"}`

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
rapport-vie-quatre-jours.md
tagger-612.json
----
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 30,90p journal/2026-11-14/mesures.md", "description": "Lire le récit de mesure du 14/11"}`

  ```
## Mesures et rapports touchés

- [reports/INDEX.md](../../reports/INDEX.md)
- [reports/README.md](../../reports/README.md)
- [reports/rapport-bilan-chantier.md](../../reports/rapport-bilan-chantier.md)
- [reports/rapport-cloture-chantier.md](../../reports/rapport-cloture-chantier.md)
- [reports/rapport-evaluer-langue.md](../../reports/rapport-evaluer-langue.md)
- [reports/rapport-exemples-rejoues.md](../../reports/rapport-exemples-rejoues.md)
- [reports/rapport-restitution-v1.md](../../reports/rapport-restitution-v1.md)
- [reports/rapport-robustesse-semaine.md](../../reports/rapport-robustesse-semaine.md)
- [reports/rapport-s065.md](../../reports/rapport-s065.md)
- [reports/rapport-tableau-mesures.md](../../reports/rapport-tableau-mesures.md)

<!-- notes -->
**J13.1 — la table des mesures.** Le chantier est consolidé en une table unique, de J1.1 à
J12.2 : **26 tâches**, **25 acceptations vertes**, **1 échec** (J5.2, le tag), **5 timeouts**
dont **4 récupérés**. Chaque ligne porte sa **base** (612/602), son **avant**, son **après**, son
**Δ**, un **contrôle négatif**, son **commit** et sa **fiche**. Le produit tient (**F1 0,7533 →
0,7902**, attachement **236/237 → 238/238 labels**,
… [1465 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('reports/tagger-612.json'))\nprint(json.dumps({k:d[k] for k in d if k not in ('modes',)}, ensure_ascii=False, indent=1)[:3000])\nprint('--- modes keys', list(d['modes']))\nfor m in d['mode … [117 caractères tronqués]`

  ```
{
 "date": "2026-11-13 22:21 EST",
 "gold": {
  "phrases": 612,
  "tokens": 3179,
  "sources": {
   "hand": 20,
   "reel": 432,
   "synth": 160
  },
  "modalite": "api-deepseek (deepseek-chat → modèle renvoyé), aucun serveur local"
 },
 "modeles_renvoyes": {
  "deepseek-flash": 1218
 },
 "pos_par_source": {
  "heuristique": {
   "all": 0.8625,
   "hand": 0.8857,
   "reel": 0.8893,
   "synth": 0.7682
  },
  "neuronal": {
   "all": 0.9475,
   "hand": 0.9714,
   "reel": 0.936,
   "synth": 0.9828
  },
  "parallele": {
   "all": 0.9475,
   "hand": 0.9714,
   "reel": 0.936,
   "synth": 0.9828
  },
  "cascade": {
   "all": 0.9475,
   "hand": 0.9714,
   "reel": 0.936,
   "synth": 0.9828
  },
  "parallele_niveau": {
   "all": 0.9475,
   "hand": 0.9714,
   "reel": 0.936,
   "synth": 0.9828
  },
  "cascade_niveau": {
   "all": 0.9475,
   "hand": 0.9714,
   "reel": 0.936,
   "synth": 0.9828
  }
 },
 "seuils": {
  "heuristique": true,
  "neuronal": true,
  "parallele": true,
  "cascade": true,
  "parallele_niveau": true,
  "cascade_niveau": true,
  "aucun_refus": false
 },
 "refus": 1,
 "refus_detail": [
  "s015"
 ],
 "appels": {
  "pos": 609,
  "syntagmes": 609
 },
 "api": {
  "appels": 1218,

… [715 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"1A\" docs/pilotage/*.md journal/2026-11-1*/*.md reports/*.md 2>/dev/null | head -30", "description": "Chercher la mention de la décision 1A"}`

  ```
docs/pilotage/semaine-autonome.md:263:| **1A** | le **tagger API en option** (`--tagger`), le défaut reste hors ligne | +8,49 pts de POS pour qui a la clé |
docs/pilotage/semaine-autonome.md:270:**Le chantier 6A (le produit)** : le tagger (1A), la restitution, la robustesse. Puis la
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 100,140p docs/pilotage/en-cours.md; echo ----; sed -n 125,145p docs/pilotage/roadmap.md", "description": "Lire l'état et la roadmap autour du tagger"}`

  ```
> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **733** / **826** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **14/11 00 h 30** (84, **81/3**) ; rouges tolérées `indice`, `melange` ; `sessions` **revérifiée verte** le 14/11 06 h 55 | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté
… [3700 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 240,290p docs/pilotage/semaine-autonome.md", "description": "Lire la décision 1A"}`

  ```
| portes / tag | 84 portes | **84, 81 vertes, 3 rouges tolérées** ; **tag absent** | [références](references-non-regression.md) |

**Les décisions.** **D1–D20** : le produit (relative zéro, convention GV, schéma v2, restitution,
`g017` rejeté, `s065` intégré, forme canonique), Panini (table, corpus, retrieval, généalogie,
séparation sœur/famille), la coordination (N2, S, R, A) et la méthode (encart qui pointe,
acceptation d'abord). **Les rejets.** **R1–R30** ; les nouveaux sont R22–R30 : adverbe final hors
SUB, variante étroite non retenue, « `g017` est une règle », famille variable unique, échantillon
20, époque, miroir strict, fidélité sémantique, encart qui recopie. **Les échecs.** **5 timeouts**
(J1.2, J2.2, J3.1, J5.2, J8.1) ; **4 récupérés** ; **1 vrai échec** (J5.2, le tag). La leçon :
**l'acceptation d'abord, le commit n'est pas la clôture**.

**La suite.** **J11.1–J11.4** (produit : exemples, par-langue, robustesse, schéma documenté) ;
**J12.1–J12.2** (Panini §334 et corpus d'or CIC) ; **J13.1** (table des mesures) ; **J14.1**
(clôture : passe + tag `chantier-2026-11-14`). Avant, les lignes bloquées restent nommées :
`g017` (convention), le split réel du tagger, la signatu
… [1070 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls docs/produit/ && wc -l docs/produit/README.md && grep -n \"^#\\|^##\\|tagger\\|hors ligne\" docs/produit/README.md | head -40", "description": "Inspecter la doc produit"}`

  ```
exemples.md
README.md
581 docs/produit/README.md
1:# Le premier produit — analyser un texte avec Drave
22:## 1. À qui s'adresse le produit
37:## 2. Ce que le produit fait
73:## 3. Comment l'utiliser — cinq exemples réels
79:### 3.1 Analyser une phrase
85:drave 0.1.0 — analyse heuristique (CPU, hors ligne)
102:### 3.2 Analyser en JSON et lire l'attachement
119:### 3.3 Mesurer sur le gold
175:### 3.3 quater Traiter un corpus
185:### 3.3 bis La vue des syntagmes qui se chevauchent — les champs du schéma v2
280:### 3.3 ter Le contexte (mémoire de discours)
289:### 3.4 Rejouer et vérifier le déterminisme
306:### 3.5 Le refus, et la langue inconnue
324:### 3.6 Restituer la surface (v0)
359:## 4. Ce que le produit ne fait pas encore
385:`drave evaluer` ne mesure qu'elle. La cascade avec le vrai tagger 7B a été mesurée à **0,9415**
389:**4. Pas de neuronal.** `MockNeuronal` est un **contrat** déterministe, pas un tagger de qualité.
421:## 5. Performance
443:## 6. Garanties
453:| **gold versionné** | les 4 gold sont dans le dépôt ; `evaluer` rejoue hors ligne | `tools/tests/linguistique/gold*.json` |
478:## 7. Le CLI livré — contrat et manques
561:## 8. Où aller ensuite
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 1, "limit": 200}`

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
11: > porte produit est verte. Le format est **version 2** (`schema: "drave.annotation"`,
12: > `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
13: > reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
14: > § 3.5 ont été relancées le 07/11 pour le format v2 ; les mesures chiffrées du § 2 datent du
15: > **06/11**, et l'`evaluer` du § 3.3 a été relancé le **14/11** (gold vivant 612, `--par-langue
16: > fr/en`)
… [11653 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 240, "offset": 280}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
280: ### 3.3 ter Le contexte (mémoire de discours)
281: 
282: ```bash
283: python3 tools/drave.py analyser "Il dort." --contexte "Le chat est sur le toit."
284: ```
285: 
286: Le champ `contexte` est porté dans le JSON ; il alimente la mémoire de discours (coréférence,
287: connecteurs) sans changer le texte analysé.
288: 
289: ### 3.4 Rejouer et vérifier le déterminisme
290: 
291: ```bash
292: python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
293: ```
294: ```
295: rejeu identique : oui
296:   texte      : 'Le chat de la voisine qui dort sur le toit se réveille.'
297:   langue     : fr
298:   étiquettes : 60
299:   JSON       : 13284 octets · sha256 31f3798beebe22f7…
300: ```
301: 
302: **Lecture.** La commande analyse **deux fois**, compare le JSON **canonique** (clés triées,
303: durée exclue) et rend une empreinte sha256. Deux exécutions indépendantes rendent le même octet :
304: l'analyse est déterministe. C'est la garantie de base du rejeu.
305: 
306: ### 3.5 Le refus, et la langue inconnue
307: 
308: ```bash
309: python3 tools
… [13615 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 519, "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
519: 
520: | option | commande | sens |
521: |---|---|---|
522: | `--langue fr\|en` | `analyser`, `rejouer`, `restituer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 2 |
523: | `--json` | `analyser`, `evaluer`, `restituer` | sortie machine UTF-8 |
524: | `--jsonl` | `analyser` | une ligne JSON par phrase (avec `--fichier`) |
525: | `--fichier CHEMIN` | `analyser`, `restituer` | lit un texte UTF-8 au lieu de l'argument |
526: | `--banc CHEMIN` | `restituer` | mesure un banc JSON de textes (les 50 textes libres) |
527: | `--canonique` | `restituer` | ajoute la forme canonique v1 (segments + rôles + cibles) et son miroir |
528: | `--partition MODE` | `analyser`, `rejouer` | `alternative` (défaut), `filtrer_union`, `filtrer`, `brut` |
529: | `--contexte TEXTE` | `analyser`, `restituer` | mémoire de discours portée dans le JSON |
530: | `--gold` | `evaluer` | gold gelé 602 au lieu du vivant 612 |
531: | `--par-langue` | `evaluer` | détail **fr/en** : POS, syntagmes, attachement et contrôle négatif par langue |
532: | `-V`, `--version` | global | `drave 0.
… [4571 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p tools/toutes-les-portes.sh | head -80; echo ====; sed -n 1,80p tools/porte-produit.sh", "description": "Lire la porte produit et le registre des portes"}`

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
… [6265 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _fusion\\|def priorite_par_defaut\\|PRIORITE_NIVEAU\\|PRIORITE_TYPE\\|def couverture\" tools/bloc_linguistique.py | head -20", "description": "Repérer la fusion et les priorités"}`

  ```
117:    def couverture(self) -> dict[str, float]:
1819:def _fusionner(spans: Sequence[Span]) -> list[Span]:
2556:def priorite_par_defaut() -> dict | None:
2562:    return PRIORITE_NIVEAU if os.environ.get("DEEPSEEK_KEY_FILE") else None
2565:PRIORITE_NIVEAU = {
2574:PRIORITE_TYPE = {
2582:def _fusion(a: Annotation, b: Annotation, source: str,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def json\" tools/bloc_linguistique.py | head; grep -n \"class Annotation\" tools/bloc_linguistique.py", "description": "Repérer Annotation.json"}`

  ```
63:    def json(self) -> dict:
81:    def json(self) -> dict:
122:    def json(self, avec_duree: bool = False) -> dict:
98:class Annotation:
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 90, "offset": 98}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 110, "offset": 2545}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
98: class Annotation:
99:     texte: str
100:     langue: str = "und"
101:     script: str = SCRIPT_NEUTRE
102:     etiquettes: list[Etiquette] = field(default_factory=list)
103:     refus: str = ""
104:     trace: list[dict] = field(default_factory=list)
105:     cout: dict = field(default_factory=dict)
106:     unites_semantiques: list[Span] = field(default_factory=list)
107:     fraction_semantique: float = 0.0
108:     source: str = "heuristique"
109:     contexte: str = ""
110: 
111:     def par_niveau(self) -> dict[str, list[Etiquette]]:
112:         sortie: dict[str, list[Etiquette]] = collections.defaultdict(list)
113:         for e in self.etiquettes:
114:             sortie[e.niveau].append(e)
115:         return dict(sortie)
116: 
117:     def couverture(self) -> dict[str, float]:
118:         """La confiance maximale par niveau — la couverture *déclarée*, pas une précision."""
119:         return {n: round(max((e.confiance for e in es), default=0.0), 4)
120:                 for n, es in self.par_niveau().items()}
121: 
122:     def json(self, avec_duree: b
… [3167 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
2545:             for e in candidates:
2546:                 if any(not (e.fin <= g.debut or e.debut >= g.fin) for g in retenues):
2547:                     continue
2548:                 retenues.append(e)
2549:             gardees.extend(retenues)
2550:     return sorted(gardees, key=lambda e: (e.debut, e.fin, e.niveau))
2551: 
2552: 
2553: # La priorité **par niveau** de la fusion : le neuronal tient POS/syntagmes/tête,
2554: # l'heuristique tient phrase/pragmatique/discours/document. C'est la réparation de la
2555: # fusion : les deux sources ne concourent plus par confiance sur les mêmes niveaux.
2556: def priorite_par_defaut() -> dict | None:
2557:     """La fusion par niveau si un neuronal réel est joignable (clé DeepSeek), sinon la confiance.
2558: 
2559:     Le mock a montré que le niveau perd (0,3432) ; le réel (deux passes) a montré qu'il gagne
2560:     (0,9389). Le défaut suit donc la **présence d'un réel**, pas une doctrine.
2561:     """
2562:     return PRIORITE_NIVEAU if os.environ.get("DEEPSEEK_KEY_FILE") else None
2563: 
2564: 
2565: PRIORITE_NIVEAU
… [5380 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 60,220p tools/tests/linguistique/evaluer_gold.py", "description": "Lire evaluer_bloc en entier"}`

  ```
"""La tête d'un segment : son premier token (début) et son type."""
    return {(e.type, e.debut) for e in a.etiquettes if e.niveau == "syntagme"}


def _pragma(a: bl.Annotation) -> dict:
    acte = next((e.valeur for e in a.etiquettes if e.niveau == "pragmatique" and e.type == "acte"), "")
    neg = any(e.type == "négation" for e in a.etiquettes if e.niveau == "phrase")
    mod = any(e.type == "modalité" for e in a.etiquettes if e.niveau == "phrase")
    ds = any(e.type == "double_sens" for e in a.etiquettes if e.niveau == "pragmatique")
    return {"acte": acte, "negation": neg, "modalite": mod, "double_sens": ds}


def _prf(tp: int, fp: int, fn: int) -> dict:
    precision = tp / max(1, tp + fp)
    rappel = tp / max(1, tp + fn)
    return {"precision": round(precision, 4), "rappel": round(rappel, 4),
            "f1": round(2 * precision * rappel / max(1e-9, precision + rappel), 4),
            "tp": tp, "fp": fp, "fn": fn}


def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
    tp = fp = fn = ttp = tfp = tfn = 0
    pos_ok = pos_n = pos_ok_ferme = pos_n_ferme = pos_ok_ouvert = pos_n_ouvert = 0
    conf = defaultdict(Counter)
    acte_ok = neg_ok = mod_ok = ds_ok =
… [7789 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/__init__.py tools/llm/__init__.py tools/tests/__init__.py 2>&1; head -20 tools/llm/deepseek.py >/dev/null; grep -n \"SCHEMA_ANNOTATION\\|VERSION_ANNOTATION\" tools/bloc_linguistique.py | head", "description": "Vérifier les p … [22 caractères tronqués]`

  ```
ls: cannot access 'tools/__init__.py': No such file or directory
ls: cannot access 'tools/tests/__init__.py': No such file or directory
tools/llm/__init__.py
91:SCHEMA_ANNOTATION = "drave.annotation"
94:VERSION_ANNOTATION = 2
128:            "schema": SCHEMA_ANNOTATION, "version": VERSION_ANNOTATION,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/revue_documentation.py tools/taille_documents.py 2>&1; sed -n 1,60p tools/taille_documents.py", "description": "Lire le budget de contexte"}`

  ```
tools/revue_documentation.py
tools/taille_documents.py
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

Les **sources de diagrammes** (` ```plantuml `, ` ```mermaid `) sont **rendues, pas lues** :
elles ne comptent pas dans le budget ; le document les porte, la page montre le SVG.
"""
from __future__ import annotations
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent

# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le
… [1694 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"reports/\\|journal/\\|docs/\" docs/methode/resultats.md | head -30", "description": "Lire la méthode de résultat/fiche"}`

  ```
27:| `reports/` | la **fiche** : chiffres, dispositif, contrôles, pièges, limites ; les JSON de résultats bruts |
28:| `journal/` | le **récit daté** : ce qui a été [fait](../theorie/glossaire/entrees/fait-mesure-projete-deduit.md), quand, et ce qu'on en a appris (généré par `tools/journal_auto.py`, notes à la main entre les marqueurs) |
29:| `docs/pilotage/en-cours.md` | l'**état** : la synthèse, la ligne du chantier, les questions ouvertes |
30:| `docs/pilotage/roadmap.md` | la **ligne de roadmap** (A… / B… / N… / R…) que le résultat fait avancer : son état y est mis à jour |
38:Un résultat n'est **pas fini** tant que [`docs/pilotage/en-cours.md`](../pilotage/en-cours.md) ne porte pas
52:*Tout ce qui n'est pas « ce qui reste vrai quand les chiffres changent » va dans `reports/`, jamais dans `docs/`.*
53:La théorie et les modes d'emploi restent dans `docs/` ; les tableaux, les séries et les erratums vont dans
54:`reports/`.
  ```

### 🤖 Assistant

⏵ J'établis la ligne de base des portes avant de modifier

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_produit.py 2>&1 | tail -5; echo \"test_produit=$?\"", "description": "Lancer le smoke test de base"}`

  ```
..................
----------------------------------------------------------------------
Ran 18 tests in 7.302s

OK
test_produit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -12; echo \"taille=$?\"; python3 tools/revue_documentation.py 2>&1 | tail -20; echo \"revue=$?\"", "description": "Lancer les portes doc de base"}`

  ```
2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 51 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
taille=0
  revue de documentation · 733 fiche(s) · 826 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"compteur\\|733\\|826\\|123\\|ficient\\|JSON\" tools/revue_documentation.py | head -40", "description": "Comprendre les compteurs de la revue"}`

  ```
12:     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
172:    # 5. compteurs : la page d'état est la source unique, et elle dit le disque
176:    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
183:            alertes.append(f"compteurs : la ligne « {nom} » manque dans en-cours.md")
185:            alertes.append(f"compteurs : en-cours.md dit {valeur} {nom}, le disque en a {disque}")
187:        alertes.append("compteurs : la ligne « fichiers / JSON » manque dans en-cours.md")
191:            (int(fiches.group(2)), compte_json(), "JSON"),
195:                    f"compteurs : en-cours.md dit {valeur} {quoi}, le disque en a {disque}"
371:    print(f"  revue de documentation · {compte_fiches()} fiche(s) · {compte_json()} JSON · "
374:        print("  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, "
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 20,70p tools/revue_documentation.py; sed -n 165,205p tools/revue_documentation.py", "description": "Lire le comptage de la revue"}`

  ```
import pathlib, re, subprocess, sys
import xml.etree.ElementTree as ET
from datetime import date

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "tools"))
from verifie_etat_a_jour import etat_modifie, retards  # noqa: E402  (même dossier)

GABARIT = ("<", "*", "AAAA", "...")
CHEMIN = re.compile(
    r"`((?:docs|reports|tools|journal|data|drave-core|sprints)/"
    r"[^`\s]+?\.(?:md|json|sh|py|rs|txt|svg|csv|jsonl))`"
)


def liens(texte: str):
    return re.findall(r"\]\(([^)#]+?)\)", texte)


def cible_generee(f: pathlib.Path, cible: str) -> bool:
    return cible.endswith((".puml.svg", ".mmd.svg")) and (f.parent / cible[:-4]).exists()


def date_dernier_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--format=%ad", "--date=short"], cwd=RACINE, text=True
        ).strip()
    except Exception:
        return ""


def date_dernier_changement(chemin: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", chemin],
            cwd=RACINE, text=True,
        ).strip()
    except Exception:
        return ""


def est_c
… [2383 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def compte_fiches\\|def compte_json\\|def compte_docs\\|def compte_portes\" -A8 tools/revue_documentation.py", "description": "Lire les fonctions de comptage"}`

  ```
100:def compte_portes() -> int:
101-    return len(list((RACINE / "tools").glob("porte-*.sh")))
102-
103-
104-def compte_chapitres() -> int:
105-    return len(list((RACINE / "docs/theorie/synthese").glob("0*.md")))
106-
107-
108:def compte_fiches() -> int:
109-    return len(rapports())
110-
111-
112:def compte_json() -> int:
113-    return len(list((RACINE / "reports").glob("*.json")))
114-
115-
116:def compte_docs() -> int:
117-    return len(docs_vivants())
118-
119-
120-def extrait_entier(texte: str, motif: str):
121-    m = re.search(motif, texte)
122-    return int(m.group(1)) if m else None
123-
124-
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def rapports\" -A6 tools/revue_documentation.py; ls reports/*.md | wc -l; ls reports/*.json | wc -l; ls reports/rapport-s-paragraphes.md 2>&1", "description": "Compter les fiches et JSON sur disque"}`

  ```
75:def rapports():
76-    return list((RACINE / "reports").glob("*.md"))
77-
78-
79-def sources_nav():
80-    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins)."""
81-    return (docs_vivants() + rapports()
733
826
reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,80p tools/verifier_schema_produit.py; echo ====; ls tools/schemas/", "description": "Lire le vérificateur de schéma"}`

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
… [2209 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"import fastjsonschema; print(fastjsonschema.__version__ if hasattr(fastjsonschema,'__version__') else 'ok')\" 2>&1; python3 -c \"import tools.llm.deepseek as d; print(d.__file__)\"", "description": "Vérifier fastjsonsche … [26 caractères tronqués]`

  ```
ok
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/llm/deepseek.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, pathlib\nR=pathlib.Path('.').resolve()\nsys.path.insert(0,str(R)); sys.path.insert(0,str(R/'tools'))\nimport bloc_linguistique as bl\nh=bl.Heuristique()\na=h.analyser(\"Le chat dort.\",\"fr\")\nprint(a.c … [94 caractères tronqués]`

  ```
{'graphème': 0.99, 'mot': 0.98, 'pos': 0.95, 'syntagme': 0.55, 'discours': 0.5, 'document': 0.7, 'phrase': 0.85, 'pragmatique': 0.45}
heuristique
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/tagger-612.json'))\nfor m in ('heuristique','neuronal','cascade','cascade_niveau'):\n    print(m, 'pos', d['modes'][m]['all']['pos']['exactitude'], 'prag', d['modes'][m]['all'] … [94 caractères tronqués]`

  ```
heuristique pos 0.8625 prag {'acte': 0.9967, 'negation': 0.9771, 'modalite': 0.9886, 'double_sens': 0.9444}
neuronal pos 0.9475 prag {'acte': 0.0, 'negation': 0.9559, 'modalite': 0.9526, 'double_sens': 0.9739}
cascade pos 0.9475 prag {'acte': 0.9967, 'negation': 0.9771, 'modalite': 0.9886, 'double_sens': 0.9444}
cascade_niveau pos 0.9475 prag {'acte': 0.0, 'negation': 0.9771, 'modalite': 0.9886, 'double_sens': 0.9739}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"classement\\|donnée de résultat\\|CHIFFRES\\|résultat dans docs\" -B3 -A12 tools/revue_documentation.py | head -80", "description": "Comprendre l'interdiction de résultats dans docs"}`

  ```
2-"""revue_documentation.py — LA REVUE DE FIN DE SOUS-CHANTIER (AGENTS.md §4).
3-
4-Ce qu'elle vérifie, et qu'il faut corriger AVANT le commit de clôture :
5:  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
6-  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
7-  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
8-     ment pas sur la cible ; les sources externes sont citées ;
9-  4. fraîcheur  : en-cours.md date du dernier commit, ET aucun fait n'a été commité après
10-     le dernier état (comparaison de commits, pas de dates : voir verifie_etat_a_jour.py) ;
11-  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
12-     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
13-  6. vocabulaire : « jeton » ne désigne **jamais** la représentation sémantique neutre (RSN) ;
14-  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
15-     ne pointe vers un fichier absent (hors gabarits `AAAA`, `<...>`, `*`).
16-
17-Sortie : un rapport lisible, code 0 si tout 
… [2178 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 205,300p tools/revue_documentation.py", "description": "Lire la navigation/orphelins de la revue"}`

  ```
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
                    f"libellé : {f.relative_to(RACINE)} annonce « {lab} » mais pointe {cible}"
                )

    # 7a. chemins morts en code inline (hors gabarits)
    for f in sources_propres():
        try:
            brut = f.read_t
… [2920 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -w reports/README.md reports/INDEX.md 2>&1; grep -n \"tagger\\|612\\|quatre-modes\" reports/README.md | head -10; grep -n \"tagger\\|612\" reports/INDEX.md | head", "description": "Inspecter les index de reports"}`

  ```
2262 reports/README.md
 12816 reports/INDEX.md
 15078 total
31:| [`rapport-coordination-r.md`](rapport-coordination-r.md) | **R** — tagger POS 612 : **0,9475 (+8,49)** |
44:| [`rapport-etat-r.md`](rapport-etat-r.md) | **B13** — l'état de R : tagger 0,8483/0,9440 |
99:| [rapport-cache-chunker.md](rapport-cache-chunker.md) | Cache du chunker — validation indépendante : ×11,0 à 160 tokens, égalité 612/612 |
126:| [rapport-coordination-r.md](rapport-coordination-r.md) | R — le tagger POS sur le gold 612 : **+8,49 pts**, la règle dit **intégrer** |
173:| [rapport-etat-r.md](rapport-etat-r.md) | État du chantier R — le lecteur : le tagger n'est pas à 0,944 contre 0,85, R1.2-1024 est mesuré, R4.4 attend la vérité humaine |
489:| [rapport-pensee-gold-neuronal.md](rapport-pensee-gold-neuronal.md) | L — le gold neuronal : un tagger 7B local, la cascade POS à 0,944 |
717:| [rapport-tableau-mesures.md](rapport-tableau-mesures.md) | J13.1 — la table des mesures : F1 0,7533 → 0,7902, attachement 236/237 → 238/238, base 612/602 |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nfor v in (1,2):\n    d=json.load(open(f'tools/schemas/drave-annotation-v{v}.json'))\n    print('v',v, 'trace:', json.dumps(d['properties'].get('trace'), ensure_ascii=False)[:500])\n    print('   cout:', … [192 caractères tronqués]`

  ```
v 1 trace: {"type": "array"}
   cout: {"type": "object"}
   additionnel: True
v 2 trace: {"type": "array"}
   cout: {"type": "object"}
   additionnel: True
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/tagger-612.json'))\nfor m in ('heuristique','neuronal','cascade'):\n    x=d['modes'][m]['all']\n    print(m, 'pos',x['pos']['exactitude'],'F1',x['syntagme']['f1'],'tete',x['syn … [202 caractères tronqués]`

  ```
heuristique pos 0.8625 F1 0.7902 tete 0.9029 att None couv None
neuronal pos 0.9475 F1 0.8074 tete 0.8586 att None couv None
cascade pos 0.9475 F1 0.8074 tete 0.8586 att None couv None
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn -- \"--tagger\\|tagger API\\|tagger en option\" docs/ reports/ journal/ 2>/dev/null | head -30", "description": "Chercher une spécification existante du --tagger"}`

  ```
docs/pilotage/semaine-autonome.md:263:| **1A** | le **tagger API en option** (`--tagger`), le défaut reste hors ligne | +8,49 pts de POS pour qui a la clé |
reports/pensee-etat-r.json:784:    "Le tagger API n'a pas ete rejoue : les 0,9389 / 0,8241 / 0,8797 sont du 2026-11-04 (run 2) ; deepseek-chat peut avoir change ; deux passes seulement (0,9389, 0,9389, 0,9385).",
reports/rapport-etat-r.md:311:- **Le trou** : le tagger API n'a pas été mesuré sur le **gold 612** (il s'arrête à 432 réelles).
reports/rapport-etat-r.md:411:- **Le tagger API n'a pas été rejoué** : les 0,9389 / 0,8241 / 0,8797 sont du **2026-11-04**
reports/rapport-semaine.md:322:**schéma v2**, **restitution 46/46**), le tagger API a une mesure et une décision (**0,9475,
reports/rapport-bilan-chantier.md:424:**schéma v2**, **restitution v1**), le tagger API a une mesure et une décision (**0,9475,
reports/rapport-tableau-mesures.md:18:> autre base. Le **tagger API** vaut **0,9475 (+8,49 pts)** ; le **produit** gagne le **schéma v2**,
reports/rapport-tableau-mesures.md:369:**POS inchangée**, **couverture 0,9916 → 0,9958**, **spans 2 → 1**), le tagger API vaut
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.
… [3841 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/ 2>/dev/null; grep -n \"tagger\" journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/rapport.md 2>/dev/null | head -20", "description": "Chercher une tentative antérieure"}`

  ```
digest.md
rapport.md
session.v4.jsonl.zstd
22:**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **intégrer le tagger POS par API DeepSeek dans la CLI, en option** (décision 1A du 14/11). La mesure est faite : le tagger vaut **0,9475** contre **0,8625** pour l'heuristique sur le gold 612 (**+8,49 pts**), pour ~0,04 $ sur tout le corpus. Il faut l'exposer **sans** changer le défaut (hors ligne, … [2946 caractères tronqués]
34:- bash — Chercher le harnais qualifier_tagger_612
38:- bash — Chercher la décision 1A et le chiffre du tagger
39:- bash — Chercher les rapports tagger existants
41:- bash — Inspecter le rapport tagger 612
43:- bash — Lire l'état et la roadmap autour du tagger
62:- **T1** Chercher le harnais qualifier_tagger_612
66:- **T1** Chercher la décision 1A et le chiffre du tagger
67:- **T1** Chercher les rapports tagger existants
69:- **T1** Inspecter le rapport tagger 612
71:- **T1** Lire l'état et la roadmap autour du tagger
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 10490,10530p journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md", "description": "Lire la décision du parent sur le tagger"}`

  ```
**30 lancements**, **32 500 s** d'agent, **25 tâches livrées**, **3 timeouts** (dont 2 après commit, requalifiés « fait » par la règle *acceptation d'abord*). Trois corrections en production : la **clé** (`~/.config/drave/deepseek.key`), le **worktree jamais propre**, le **plan relu à chaque tour**. Le journal d'audit : `work/chantier/journal.log` ; l'état : `work/chantier/etat.json`.

\## 5. Les négatifs, dits


… [1365 caractères tronqués]

### Tour 195 — ok, vulgarise-moi les points de décision à prendre (je reviens de vacances :-) ) et on tranche ici si possible

*1 appels d'outils.* Actions notables :

- bash — Relire les fiches de décision

**Synthèse produite :**

⏵ Voici les décisions, en clair — avec mon avis et ce qu'elles coûtent

\## Décision 1 — Le « tagger » : utiliser l'API pour étiqueter les mots ?

**Le constat.** Notre analyseur trouve la classe grammaticale de chaque mot avec **86,25 %** de justesse. Le même exercice confié à un modèle par API atteint **94,75 %** — soit **+8,5 points**, pour **0,04 $** sur l'ensemble du corpus de test (1 218 appels, 21 min).

- **A. L'ajouter en option** (`--tagger`) : la qualité de qui veut le réseau et la clé ; le défaut reste 
… [1104 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,70p reports/rapport-pensee-quatre-modes.md", "description": "Lire une fiche récente pour le style"}`

  ```
# L — la porte des quatre modes sur le gold 432 : le neuronal API domine (0,9309 / 0,8226 / 0,8784), la fusion dégrade (0,928 / 0,802 / 0,857)

> **Ligne de roadmap** : **L** (le bloc langue) · **Date** : 2026-11-03 · **Verdict** : ⚠️ **le neuronal
> seul est le meilleur sur les niveaux linguistiques** — POS **0,9309**, syntagmes **0,8226**, tête
> **0,8784** —, l'**heuristique** garde la **pragmatique** (acte **0,9954** contre **0,0**), et la
> **fusion** (parallèle et cascade) **régresse** : **0,928 / 0,802 / 0,857**. Un **refus** ; 858
> appels API, **254 341 tokens**, 13,3 min. La porte des quatre modes **révèle le problème de la
> fusion**, pas celui des blocs.

## 1. Le dispositif

- **Gold réel 432** (2 375 tokens), le même pour les quatre modes.
- **Neuronal** : `NeuronalLLMCompose` (POS + syntagmes) via l'**API DeepSeek** (`deepseek-chat`,
  `DEEPSEEK_KEY_FILE`), **aucun serveur local**, **aucun GPU** (règle 11).
- **Parallèle** : `Parallele([heuristique, neuronal], priorite_syntagme="confiance")`.
- **Cascade** : `Cascade(heuristique, neuronal, seuil=0,6, priorite_syntagme="confiance")`.
- **Mesures** : POS, syntagmes F1, tête F1, acte, fraction, refus ; **coût** : appels
… [2624 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-quatre-modes.json'))\ndef walk(o,p=''):\n    if isinstance(o,dict):\n        for k,v in list(o.items())[:8]:\n            print(p+k, type(v).__name__)\n            if is … [193 caractères tronqués]`

  ```
date str
gold dict
  phrases int
  tokens int
  modalite str
modes dict
  heuristique dict
    all dict
      pos dict
        exactitude float
        exactitude_ferme float
        exactitude_ouvert float
        tokens int
        confusions dict
          DET dict
            DET int
          NOUN dict
            NOUN int
            ADJ int
          PRON dict
            PRON int
          VERB dict
            VERB int
            NOUN int
      syntagme dict
        precision float
        rappel float
        f1 float
        tp int
        fp int
        fn int
        tete dict
          precision float
          rappel float
          f1 float
          tp int
          fp int
          fn int
      tete dict
        precision float
        rappel float
        f1 float
        tp int
        fp int
        fn int
      pragmatique dict
        acte float
        negation float
        modalite float
        double_sens float
      fraction_semantique float
    hand dict
      pos dict
        exactitude float
        exactitude_ferme float
        exactitude_ouvert float
        tokens int
        confusions dict
      syntagme dict
        precision float
        ra
… [12853 caractères tronqués]
  ```

### 🤖 Assistant

⏵ J'implémente l'option `--tagger` dans la CLI (client, transport, cascade, cache, code 4)

- **todo_write** `{"todos": [{"content": "Implémenter --tagger dans tools/drave.py (analyser + evaluer, clé, cache, code 4)", "status": "in_progress"}, {"content": "Écrire tools/tests/test_tagger_api.py (transport factice, JSON, défaut, code 4)", "status": "pending"}, {"content": "Mesurer 20 phrases (harnais + CLI) : … [266 caractères tronqués]`

  ```
Updated todo list: 4 pending, 1 in progress, 0 completed.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    python3 tools/drave.py analyser \"Le chat dort.\"\n    python3 tools/drave.py analyser \"The cat sleeps on the roof.\" --langue en --json\n    python3 tools/drave.py evaluer\n    python3 tools/drave.py … [2747 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "import argparse\nimport hashlib\nimport importlib.util\nimport json\nimport pathlib\nimport random\nimport sys\nimport textwrap", "new_string": "import argparse\nimport hashlib\nimport importlib.util\nimpo … [80 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "NOM = \"drave\"\nVERSION = \"0.1.0\"\nLARGEUR = 100\n\n# Le tagger est une **option** : sans `--tagger`, rien de ce bloc n'est importé ni exécuté.\nMODELE_TAGGER = \"deepseek-chat\"\nSEUIL_TAGGER = 0.6\n#  … [438 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "def _canonique(a: bl.Annotation) -> str:\n    \"\"\"La forme comparée par `rejouer` : clés triées, durée exclue, sans espaces inutiles.\"\"\"\n    return _sur(json.dumps(a.json(), ensure_ascii=False, sort_ … [4877 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "def _ligne_tagger(stats: dict) -> str:\n    \"\"\"Une ligne de coût pour l'affichage et la stderr ; pas de clé, pas d'horodatage.\"\"\"\n    return (f\"modèle={MODELE_TAGGER} · appels={stats['appels']} \"\ … [547 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "def formater_annotation(a: bl.Annotation, tagger: bool = False,\n                        stats: dict | None = None) -> str:\n    \"\"\"La sortie lisible : POS compact, syntagmes (rôle + cible), pragmatique … [643 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 30, "offset": 245}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
245:             lignes.append(
246:                 f"  {e.type:<{lt}}  {span:<{lsp}}  {valeur:<{lv}}  "
247:                 f"rôle={role:<{lr}}  → {cible}"
248:             )
249:     else:
250:         lignes.append("SYNTAGMES —")
251: 
252:     phrases = [e for e in a.etiquettes if e.niveau == "phrase" and e.type == "type"]
253:     if phrases:
254:         lignes.append("PRAGMATIQUE")
255:         par_span: dict[tuple[int, int], list[bl.Etiquette]] = {}
256:         for e in a.etiquettes:
257:             if e.niveau == "pragmatique":
258:                 par_span.setdefault((e.debut, e.fin), []).append(e)
259:         for p in phrases:
260:             ici = par_span.get((p.debut, p.fin), [])
261:             acte = next((e.valeur for e in ici if e.type == "acte"), "—")
262:             negation = "oui" if any(e.type == "négation" for e in ici) else "non"
263:             modalite = "oui" if any(e.type == "modalité" for e in ici) else "non"
264:             double_sens = "oui" if any(e.type == "double_sens" for e in ici) else "non"
265:             lignes.append(
266:     
… [446 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 18, "offset": 272}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
272:     couverture = a.couverture()
273:     if couverture:
274:         ordre = [n for n in bl.NIVEAUX if n in couverture]
275:         ordre += sorted(n for n in couverture if n not in bl.NIVEAUX)
276:         lignes.extend(_envelopper(
277:             "COUVERTURE  ",
278:             "(confiance max par niveau)  "
279:             + " · ".join(f"{n}={couverture[n]:.2f}" for n in ordre),
280:         ))
281:     return "\n".join(lignes)
282: 
283: 
284: # --------------------------------------------------------------------------- commandes
285: 
286: 
287: def _lire_entree(args: argparse.Namespace) -> str:
288:     """Le texte : l'argument, ou le **fichier** (`--fichier`)."""
289:     if getattr(args, "fichier", None):

(Showing lines 272-289 of 721. Use offset=290 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "        lignes.extend(_envelopper(\n            \"COUVERTURE  \",\n            \"(confiance max par niveau)  \"\n            + \" · \".join(f\"{n}={couverture[n]:.2f}\" for n in ordre),\n        ))\n    if … [471 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 60, "offset": 284}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
284:         lignes.extend(_envelopper("TAGGER API  ", _ligne_tagger(stats)))
285:     return "\n".join(lignes)
286: 
287: 
288: # --------------------------------------------------------------------------- commandes
289: 
290: 
291: def _lire_entree(args: argparse.Namespace) -> str:
292:     """Le texte : l'argument, ou le **fichier** (`--fichier`)."""
293:     if getattr(args, "fichier", None):
294:         return pathlib.Path(args.fichier).read_text(encoding="utf-8", errors="replace")
295:     return args.texte or ""
296: 
297: 
298: def _analyser_jsonl(texte: str, args: argparse.Namespace) -> int:
299:     """Une **ligne JSON par phrase** (traitement de corpus : `--jsonl`)."""
300:     h = bl.Heuristique(partition=args.partition)
301:     n = 0
302:     for debut, fin, _typ, _ in h._phrases(texte):
303:         phrase = texte[debut:fin]
304:         if not phrase.strip():
305:             continue
306:         a = h.analyser(phrase, args.langue, args.contexte)
307:         sys.stdout.write(_sur(json.dumps(a.json(), ensure_ascii=False)) + "\n")
308:         n += 1
309:     if 
… [1687 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "def _analyser_jsonl(texte: str, args: argparse.Namespace, h: bl.Heuristique, bloc,\n                    stats: dict | None = None) -> int:\n    \"\"\"Une **ligne JSON par phrase** (traitement de corpus : ` … [4524 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 150, "offset": 400}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
400: 
401: def _pct(valeur: float) -> str:
402:     return f"{100.0 * float(valeur):.2f} %"
403: 
404: 
405: def _formater_evaluation(rapport: dict) -> str:
406:     gold = rapport["gold"]
407:     mesure = rapport["heuristique"]
408:     pos = mesure["pos"]
409:     syn = mesure["syntagme"]
410:     tete = syn["tete"]
411:     att = mesure["attachement"]
412:     att_tete = mesure["attachement_tete"]
413:     prag = mesure["pragmatique"]
414:     controle = rapport["controle_negatif"]
415:     lignes = [
416:         f"{NOM} {VERSION} — évaluation de l'heuristique sur le gold",
417:         f"gold {gold['nom']} · {gold['phrases']} phrases · {gold['tokens']} tokens · "
418:         f"{gold['cibles_attachement']} cibles d'attachement",
419:         "",
420:         f"POS         exactitude {_pct(pos['exactitude'])}  "
421:         f"(fermé {_pct(pos['exactitude_ferme'])}, ouvert {_pct(pos['exactitude_ouvert'])})",
422:         f"SYNTAGMES   F1 {_pct(syn['f1'])}  "
423:         f"(P {_pct(syn['precision'])} / R {_pct(syn['rappel'])})",
424:         f"  tête      F1 {_pct(tete['f1']
… [7037 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "def _pct(valeur: float) -> str:\n    return f\"{100.0 * float(valeur):.2f} %\"\n\n\ndef _points(delta: float) -> str:\n    \"\"\"Un écart de taux en **points** de pourcentage, avec son signe.\"\"\"\n    re … [139 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "        f\"CONTRÔLE NÉGATIF cible exacte tirée au hasard {_pct(controle['exact_taux'])} \"\n        f\"(graine {controle['graine']}, {controle['cibles']} cibles)\",\n    ]\n    tagger = rapport.get(\"tagge … [4035 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "def cmd_evaluer(args: argparse.Namespace) -> int:\n    evaluateur = _module_evaluation()\n    phrases = evaluateur.charger_gele() if args.gold else evaluateur.charger()\n    cascade = None\n    stats = Non … [7025 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 100, "offset": 690}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
690:     def error(self, message: str) -> None:  # type: ignore[override]
691:         self.print_usage(sys.stderr)
692:         self.exit(2, f"{self.prog}: erreur d'usage : {message}\n")
693: 
694: 
695: def construire_parseur() -> argparse.ArgumentParser:
696:     epilogue = (
697:         "Commandes : analyser, evaluer, rejouer, restituer.\n"
698:         "Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) · 1 erreur.\n"
699:         "Options : --json, --langue fr|en, --partition brut|alternative|filtrer_union|filtrer,\n"
700:         "--contexte, --banc.\n"
701:         "Limites : heuristique CPU, hors ligne, déterministe ; la restitution est un codec de\n"
702:         "surface (graphème), pas un décodeur neuronal ; ni traduction ni génération.\n"
703:         "Exemples :\n"
704:         "  python3 tools/drave.py analyser \"Le chat dort.\"\n"
705:         "  python3 tools/drave.py evaluer --gold --json\n"
706:         "  python3 tools/drave.py restituer \"Le chat dort.\"\n"
707:         "  python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.
… [5386 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    epilogue = (\n        \"Commandes : analyser, evaluer, rejouer, restituer.\\n\"\n        \"Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) ·\\n\"\n        \"4 clé/tagger absent · 1 erre … [1733 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    analyser = sous.add_parser(\n        \"analyser\",\n        help=\"étiqueter un texte (POS, syntagmes, pragmatique)\",\n        description=\"Analyse un texte avec l'heuristique et rend la lecture comp … [5990 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m py_compile tools/drave.py && python3 tools/drave.py analyser \"Le chat dort.\" && echo \"----\" && python3 tools/drave.py evaluer --json | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['heuristique']['pos'] … [98 caractères tronqués]`

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
----
0.8625 612 ['attachement_lineaire', 'controle_negatif', 'gold', 'heuristique', 'syntagmes_lineaire', 'version']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && env -u DEEPSEEK_API_KEY -u DSH_API_KEY -u DEEPSEEK_KEY_FILE -u DSH_KEY_FILE HOME=/tmp/drave-sans-cle python3 tools/drave.py analyser \"Le chat dort.\" --tagger; echo \"code=$?\"", "description": "Tester l'absence de clé (code 4)"}`

  ```
code=4
[stderr]
drave: dépendance absente : clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans ~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Le chat dort.\" --tagger --json 2>/tmp/tagger-stderr.txt >/tmp/tagger-out.json; echo \"code=$?\"; cat /tmp/tagger-stderr.txt; python3 -c \"\nimport json\nd=json.load(open('/tmp/tagger-out.json'))\npr … [392 caractères tronqués]`

  ```
code=0
drave: tagger · modèle=deepseek-chat · appels=2 · réseau=0 · cache=2 · tokens=0 · latence=0.0 s
schema drave.annotation version 2 source cascade refus 
POS [('Le', 'DET'), ('chat', 'NOUN'), ('dort', 'VERB')]
SYN [('GN', 'Le chat', 'dort'), ('GV', 'dort', 'chat')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('tools/tests/linguistique/gold.json'))\nfor p in d['phrases'][:2]:\n    print(p['id'], p['langue'], repr(p['texte']), len(p['mots']))\nPY", "description": "Voir les deux premières phras … [12 caractères tronqués]`

  ```
g001 fr 'Le chat dort.' 3
g002 fr 'Le chat de la voisine dort.' 6
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "content": "\"\"\"test_tagger_api.py — le tagger POS par API, **en option**, sans réseau.\n\nCe que le fichier verrouille, avec un **transport factice** (une fonction qui rend un JSON de\nPOS valide) :\n\ … [15227 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "new_string": "    def test_evaluer_sans_tagger(self) -> None:\n        resultat = drave_cli(\"evaluer\", \"--json\")\n        self.assertEqual(resultat.returncode, 0, resultat.stderr)\n        donnees =  … [489 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "new_string": "    def test_evaluer_tagger(self) -> None:\n        evaluateur = drave._module_evaluation()\n        chargeur = evaluateur.charger\n        evaluateur.charger = lambda: chargeur()[:2]\n     … [378 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_tagger_api.py 2>&1 | tail -40", "description": "Lancer les tests du tagger"}`

  ```
Un tagger qui rend autre chose qu'un JSON est un refus, pas une exception.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", line 166, in test_transport_invalide_ne_fait_pas_planter
    self.assertIn("neuronal", annotation.refus)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'neuronal' not found in ''

======================================================================
FAIL: test_analyser_tagger_json (__main__.TestCliAvecTransportFactice.test_analyser_tagger_json)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", line 281, in test_analyser_tagger_json
    self.assertIn("TAGGER API", erreur)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'TAGGER API' not found in 'drave: tagger · modèle=deepseek-chat · appels=2 · réseau=2 · cache=0 · tokens=34 · latence=0.0 s\n'

======================================================================
FAIL: test_evaluer_tagger (__main__.
… [1424 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Heuristique\" -A30 tools/bloc_linguistique.py | head -50", "description": "Lire l'init de Heuristique"}`

  ```
796:class Heuristique:
797-    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
798-
799-    nom = "heuristique"
800-
801-    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
802-                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
803-                 union: bool = True, partition: str = "alternative"):
804-        self.profils = profils
805-        self.segmenter_s = segmenter_s
806-        self.seuil_ouvert = seuil_ouvert
807-        self.seuil_langue = seuil_langue
808-        self.union = union
809-        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
810-        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
811-        # "filtrer_union" : on retire le S qui **contient** un segment chunker (le filtre
812-        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
813-        # Dans les deux filtres, le segment retiré reste dans `meta.alternative` (`retire`).
814-        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
815-            raise ValueError("partition atten
… [596 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json, subprocess, pathlib\nR=pathlib.Path('.').resolve(); sys.path.insert(0,str(R)); sys.path.insert(0,str(R/'tools'))\nimport bloc_linguistique as bl\nref=bl.Heuristique().analyser(\"Le chat dort.\",\"f … [444 caractères tronqués]`

  ```
DIFF trace [{'etape': 'langue', 'langue': 'fr', 'script': 'Latn', 'confiance': 0.7067, 'indice': 'fr'}, {'etape': 'niveaux', 'etiquettes': 20, 'niveaux': ['discours', 'document', 'graphème', 'mot', 'phrase', 'po || [{'etape': 'langue', 'langue': 'fr', 'script': 'Latn', 'confiance': 0.6667, 'indice': ''}, {'etape': 'niveaux', 'etiquettes': 20, 'niveaux': ['discours', 'document', 'graphème', 'mot', 'phrase', 'pos'
partition default? alternative
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "class _CascadeTagger:\n    \"\"\"La cascade du tagger, avec le **refus** du neuronal reporté sur l'annotation fusionnée.\n\n    `bl.Cascade`/`_fusion` ne recopie pas `refus` : sans ce relais, un tagger qui … [2406 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"tagger · {_ligne_tagger\" tools/drave.py", "description": "Repérer les lignes de coût stderr"}`

  ```
344:        print(f"{NOM}: tagger · {_ligne_tagger(stats)}", file=sys.stderr)
388:            print(f"{NOM}: tagger · {_ligne_tagger(stats)}", file=sys.stderr)
602:            print(f"{NOM}: tagger · {_ligne_tagger(stats)}", file=sys.stderr)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\nt=p.read_text(encoding='utf-8')\nt=t.replace('print(f\"{NOM}: tagger · {_ligne_tagger(stats)}\", file=sys.stderr)',\n            'print(f\"{NOM}: TAGGER API · {_lign … [187 caractères tronqués]`

  ```
3
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "new_string": "        donnees = json.loads(resultat.stdout)\n        self.assertEqual(donnees, bl.Heuristique().analyser(TEXTE).json())", "old_string": "        donnees = json.loads(resultat.stdout)\n    … [81 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_tagger_api.py 2>&1 | tail -35", "description": "Relancer les tests du tagger"}`

  ```
test_cache_par_texte (__main__.TestCascadeTagger.test_cache_par_texte) ... ok
test_cascade_remplace_les_pos (__main__.TestCascadeTagger.test_cascade_remplace_les_pos) ... FAIL
test_json_valide_schema (__main__.TestCascadeTagger.test_json_valide_schema) ... ok
test_transport_invalide_ne_fait_pas_planter (__main__.TestCascadeTagger.test_transport_invalide_ne_fait_pas_planter)
Un tagger qui rend autre chose qu'un JSON est un refus, pas une exception. ... ok
test_absence_de_cle_ne_fuit_pas (__main__.TestCle.test_absence_de_cle_ne_fuit_pas) ... ok
test_la_cle_ne_sort_pas_du_client (__main__.TestCle.test_la_cle_ne_sort_pas_du_client) ... ok
test_ordre_de_resolution (__main__.TestCle.test_ordre_de_resolution) ... ok
test_sans_cle_code_4 (__main__.TestCle.test_sans_cle_code_4) ... ok
test_analyser_tagger_json (__main__.TestCliAvecTransportFactice.test_analyser_tagger_json) ... ok
test_analyser_tagger_lisible (__main__.TestCliAvecTransportFactice.test_analyser_tagger_lisible) ... ok
test_evaluer_tagger (__main__.TestCliAvecTransportFactice.test_evaluer_tagger) ... ok
test_aide_expose_tagger (__main__.TestDefaultInchange.test_aide_expose_tagger) ... ok
test_analyser_json_sans_tagger (__main_
… [1272 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"_cache\" tools/bloc_linguistique.py | sed -n 1,20p; grep -n \"def analyser\" tools/bloc_linguistique.py | head -10", "description": "Vérifier le cache de l'heuristique"}`

  ```
1998:        self._cache: dict[tuple[str, str | None], Annotation] = {}
2034:        if self.cache and cle in self._cache:
2035:            return copy.deepcopy(self._cache[cle])
2072:            self._cache[cle] = annotation
2127:        self._cache: dict[tuple[str, str | None], Annotation] = {}
2168:        if self.cache and cle in self._cache:
2169:            return copy.deepcopy(self._cache[cle])
2223:            self._cache[cle] = annotation
2307:        self._cache: dict[tuple[str, str | None], Annotation] = {}
2338:        if self.cache and cle in self._cache:
2339:            return copy.deepcopy(self._cache[cle])
2378:            self._cache[cle] = annotation
141:    def analyser(self, texte: str, langue: str | None = None,
1455:    def analyser(self, texte: str, langue: str | None = None,
1845:    def analyser(self, texte: str, langue: str | None = None,
1916:    def analyser(self, texte: str, langue: str | None = None,
2026:    def analyser(self, texte: str, langue: str | None = None,
2160:    def analyser(self, texte: str, langue: str | None = None,
2252:    def analyser(self, texte: str, langue: str | None = None,
2330:    def analyser(self, texte: str, langue: str | 
… [146 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, pathlib\nR=pathlib.Path('.').resolve(); sys.path.insert(0,str(R)); sys.path.insert(0,str(R/'tools'))\nimport bloc_linguistique as bl\nfor txt in (\"Le chat dort.\", \"Le chat, « dort ! »\", \"12,5 %\"):\ … [106 caractères tronqués]`

  ```
'Le chat dort.' [(0, 2, 'Le', 'mot'), (3, 7, 'chat', 'mot'), (8, 12, 'dort', 'mot'), (12, 13, '.', 'ponctuation')]
'Le chat, « dort ! »' [(0, 2, 'Le', 'mot'), (3, 7, 'chat', 'mot'), (7, 8, ',', 'ponctuation'), (9, 10, '«', 'ponctuation'), (11, 15, 'dort', 'mot'), (16, 17, '!', 'ponctuation'), (18, 19, '»', 'ponctuation')]
'12,5 %' [(0, 2, '12', 'nombre'), (2, 3, ',', 'ponctuation'), (3, 4, '5', 'nombre'), (5, 6, '%', 'ponctuation')]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "new_string": "        # l'heuristique, elle, dit DET/NOUN/VERB : la substitution est réelle. Le tagger ne\n        # reçoit que les mots et les nombres : la ponctuation (PONCT) n'est pas rendue.\n        … [499 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_tagger_api.py 2>&1 | tail -8", "description": "Relancer les tests du tagger"}`

  ```
test_aide_expose_tagger (__main__.TestDefaultInchange.test_aide_expose_tagger) ... ok
test_analyser_json_sans_tagger (__main__.TestDefaultInchange.test_analyser_json_sans_tagger) ... ok
test_evaluer_sans_tagger (__main__.TestDefaultInchange.test_evaluer_sans_tagger) ... ok

----------------------------------------------------------------------
Ran 14 tests in 1.936s

OK
  ```

### 🤖 Assistant

⏵ Je lance la mesure 20 phrases (cache neuf) et vérifie le smoke test en parallèle

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf /tmp/drave-tagger-option-cache && mkdir -p /tmp/drave-tagger-option-cache && DEEPSEEK_KEY_FILE=\"$HOME/.config/drave/deepseek.key\" DEEPSEEK_CACHE=/tmp/drave-tagger-option-cache DEEPSEEK_MODEL=deepseek-chat PYTHONPATH=. python … [207 caractères tronqués]`

  ```
started background job bash-4967
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_produit.py 2>&1 | tail -4", "description": "Vérifier le smoke test existant"}`

  ```
----------------------------------------------------------------------
Ran 18 tests in 7.418s

OK
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 120, "offset": 63}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
63: PRIORITE_TAGGER = dict(bl.PRIORITE_NIVEAU)
64: PRIORITE_TAGGER["syntagme"] = "heuristique"
65: 
66: 
67: # --------------------------------------------------------------------------- sorties JSON
68: 
69: 
70: def _sur(s: str) -> str:
71:     """Une chaîne toujours **écrivable** : un surrogate isolé devient U+FFFD (jamais d'exception)."""
72:     return s.encode("utf-8", "replace").decode("utf-8", "replace")
73: 
74: 
75: def _dumps(objet) -> str:
76:     """JSON stable (pas d'horodatage, pas de durée) et lisible."""
77:     return _sur(json.dumps(objet, ensure_ascii=False, indent=1)) + "\n"
78: 
79: 
80: def _canonique(a: bl.Annotation) -> str:
81:     """La forme comparée par `rejouer` : clés triées, durée exclue, sans espaces inutiles."""
82:     return _sur(json.dumps(a.json(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
83: 
84: 
85: # --------------------------------------------------------------------------- le tagger (option)
86: 
87: 
88: class CleTaggerAbsente(RuntimeError):
89:     """Aucune clé : le tagger est une option, jamais un prérequis du pro
… [4240 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-4967"}`

  ```
(no new output)
[status: running]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "        except CleTaggerAbsente as exc:\n            print(f\"{NOM}: dépendance absente : {exc}\", file=sys.stderr)\n            return 4\n        # un texte sans mot ni nombre est un refus d'analyse : on  … [583 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

### 👤 Utilisateur

background job bash-4967 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf /tmp/drave-tagger-option-cache && mkdir -p /tmp/drave-tagger-option-cache && DEEPSEEK_KEY_FILE="$HOME/.config/drave/deepseek.key" DEEPSEEK_CACHE=/tmp/drave-tagger-option-cache DEEPSEEK_MODEL=deepseek-chat PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py --limite 20 --sortie /tmp/tagger-option-20.json 2>&1 | tail -20) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Je lis le résultat de la mesure 20 phrases et son coût

- **job_output** `{"job_id": "bash-4967"}`

  ```
"hand": 0.9714
  },
  "cascade": {
   "all": 0.9714,
   "hand": 0.9714
  },
  "parallele_niveau": {
   "all": 0.9714,
   "hand": 0.9714
  },
  "cascade_niveau": {
   "all": 0.9714,
   "hand": 0.9714
  }
 },
 "appels": 40,
 "tokens": 11868,
 "refus": 0,
 "latence_moyenne": 0.987
}
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/tagger-option-20.json'))\nprint('gold', d['gold'])\nprint('modeles', d['modeles_renvoyes'])\nprint('api', d['api'])\nprint('appels', d['appels'])\nprint('latence', d['latence_s']) … [382 caractères tronqués]`

  ```
gold {'phrases': 20, 'tokens': 105, 'sources': {'hand': 20}, 'modalite': 'api-deepseek (deepseek-chat → modèle renvoyé), aucun serveur local'}
modeles {'deepseek-flash': 40}
api {'appels': 40, 'tokens': 11868, 'latence_s': 39.49}
appels {'pos': 20, 'syntagmes': 20}
latence {'moyenne': 0.987, 'mediane': 0.992}
refus 0 []
heuristique      POS 0.8857  F1 0.9016  tete 0.9739  acte 1.0000  duree 0.04s
neuronal         POS 0.9714  F1 0.8846  tete 0.9038  acte 0.0000  duree 39.57s
parallele        POS 0.9714  F1 0.8846  tete 0.9038  acte 1.0000  duree 0.08s
cascade          POS 0.9714  F1 0.8846  tete 0.9038  acte 1.0000  duree 0.05s
parallele_niveau POS 0.9714  F1 0.8846  tete 0.9038  acte 0.0000  duree 0.05s
cascade_niveau   POS 0.9714  F1 0.8846  tete 0.9038  acte 0.0000  duree 0.05s
seuils {'heuristique': True, 'neuronal': True, 'parallele': True, 'cascade': True, 'parallele_niveau': True, 'cascade_niveau': True, 'aucun_refus': True}
  ```

- **bash** `{"command": "cat > /tmp/mesure_tagger_option.py <<'PY'\nimport json, pathlib, sys\nR = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0, str(R)); sys.path.insert(0, str(R/'tools'))\nimport drave\nfrom tools.tests.linguistique.evaluer_gold import evaluer_bloc\n\nphra … [1635 caractères tronqués]`

  ```
{
 "phrases": 20,
 "tokens": 105,
 "heuristique": {
  "pos": 0.8857,
  "ferme": 0.8772,
  "ouvert": 0.8958,
  "f1": 0.9016,
  "tete": 0.9739,
  "attachement_exact": 0.9231,
  "attachement_couverture": 0.9231
 },
 "cascade": {
  "pos": 0.9714,
  "ferme": 0.9474,
  "ouvert": 1.0,
  "f1": 0.9016,
  "tete": 0.9739,
  "attachement_exact": 0.9231,
  "attachement_couverture": 0.9231
 },
 "delta_pos": 0.0857,
 "refus": 0,
 "refus_detail": [],
 "cout": {
  "modele": "deepseek-chat",
  "appels": 40,
  "requetes": 0,
  "cache": 40,
  "tokens": 0,
  "latence_s": 0.0,
  "modeles_renvoyes": {
   "deepseek-flash": 40
  }
 }
}
  ```

- **bash** `{"command": "cat > /tmp/evaluer_20_cli.py <<'PY'\nimport json, pathlib, sys\nR = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0, str(R)); sys.path.insert(0, str(R/'tools'))\nimport drave\nev = drave._module_evaluation()\nchargeur = ev.charger\nev.charger = lambda: … [983 caractères tronqués]`

  ```
code=0
drave: TAGGER API · modèle=deepseek-chat · appels=40 · réseau=0 · cache=40 · tokens=0 · latence=0.0 s
gold {'nom': 'vivant (hand + reel + synthétique)', 'gele': False, 'phrases': 20, 'tokens': 105, 'cibles_attachement': 13}
heuristique POS 0.8857
tagger POS 0.9714 delta 0.0857
tagger syntagme 0.9016 prag acte 1.0
cout {'modele': 'deepseek-chat', 'appels': 40, 'requetes': 0, 'cache': 40, 'tokens': 0, 'latence_s': 0.0, 'modeles_renvoyes': {'deepseek-flash': 40}}
refus 0
heuristique syntagme 0.9016
  ```

- **bash** `{"command": "cat > /tmp/evaluer_20_cli_txt.py <<'PY'\nimport pathlib, sys\nR = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0, str(R)); sys.path.insert(0, str(R/'tools'))\nimport drave\nev = drave._module_evaluation()\nchargeur = ev.charger\nev.charger = lambda: c … [381 caractères tronqués]`

  ```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 20 phrases · 105 tokens · 13 cibles d'attachement

POS         exactitude 88.57 %  (fermé 87.72 %, ouvert 89.58 %)
SYNTAGMES   F1 90.16 %  (P 83.33 % / R 98.21 %)
  tête      F1 97.39 %  (P 94.92 % / R 100.00 %)
  vue linéaire (partition filtrer) F1 82.57 %  · attachement 69.23 % de couverture
ATTACHEMENT exact 92.31 % · couverture 92.31 % · exact sur span 100.00 % · top-k 92.31 %
  tête      couverture 100.00 % · top-k 100.00 %
PRAGMATIQUE acte 100.00 % · négation 100.00 % · modalité 95.00 % · double sens 90.00 %
FRACTION SÉMANTIQUE 48.35 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 23.08 % (graine 0, 13 cibles)

TAGGER API DEEPSEEK (option --tagger)
  POS         exactitude 97.14 % (fermé 94.74 %, ouvert 100.00 %) · Δ +8.57 pts vs heuristique
  SYNTAGMES   F1 90.16 % (tête 97.39 %) — conservés à l'heuristique
  COÛT        appels 40 · réseau 0 · cache 40 · tokens 0 · modèle deepseek-chat
  modèle renvoyé : deepseek-flash
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, random, collections\nphrases=json.load(open('tools/tests/linguistique/gold.json'))['phrases'][:20]\nclasses=(\"DET\",\"NOUN\",\"VERB\",\"ADJ\",\"ADV\",\"PREP\",\"PRON\",\"AUX\",\"CONJ\",\"NUM\",\"INTJ\" … [585 caractères tronqués]`

  ```
uniforme 11 105 0.1048
majoritaire VERB 24 105 0.2286
NOUN 21 105 0.2
Counter({'VERB': 24, 'DET': 21, 'NOUN': 21, 'PREP': 9, 'AUX': 9, 'PRON': 9, 'ADV': 6, 'CONJ': 3, 'ADJ': 3})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,60p reports/README.md", "description": "Lire le début de l'index des fiches"}`

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
| [`note-panini-334.md`](note-panini-334.md) | **Panini** — la note à envoyer : H0 reproduite, β époque non, la collinéarité |
| [`rapport-panini-334.md`](rapport-panini-334.md) | **Panini** — le §334 : H0 0,909/0,906, la |
| [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md) | **B13** — les 5 exem
… [4134 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Le chat dort.\" --tagger", "description": "Capturer la sortie réelle de analyser --tagger"}`

  ```
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 19 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.60 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=2 · réseau=0 · cache=2 · tokens=0 · latence=0.0 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && DEEPSEEK_KEY_FILE=\"$HOME/.config/drave/deepseek.key\" DEEPSEEK_CACHE=/tmp/drave-tagger-option-cache python3 /tmp/mesure_tagger_option.py > /tmp/mesure-tagger-option-cli.json && python3 -c \"import json; d=json.load(open('/tmp/mesure … [176 caractères tronqués]`

  ```
0.9714 0.0857 40 40
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/genere_pensee_tagger.py <<'PY'\nimport json, pathlib, random, collections\n\nR = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nharnais = json.load(open('/tmp/tagger-option-20.json'))\ncli = json.load(ope … [8451 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-tagger-option.json 5516 octets
uniforme 0.10476190476190476 majoritaire VERB 0.22857142857142856
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-tagger-option.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-tagger-option.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-14",
3:  "branche": "s/v7",
4:  "decision": "1A — le tagger API en option, le défaut reste hors ligne",
5:  "ligne_roadmap": "R0.7 (le lecteur)",
6:  "option": {
7:   "drapeau": "--tagger",
8:   "commandes": [
9:    "analyser",
10:    "evaluer"
11:   ],
12:   "modele_demande": "deepseek-chat",
13:   "seuil_cascade": 0.6,
14:   "fusion": {
15:    "pos": "neuronal (tagger)",
16:    "syntagme": "heuristique",
17:    "pragmatique": "heuristique",
18:    "pourquoi": "le tagger ne rend ni rôle ni cible : forcer ses syntagmes ferait perdre l'attachement mesuré"
19:   },
20:   "cle": [
21:    "DEEPSEEK_KEY_FILE",
22:    "~/.config/drave/deepseek.key",
23:    "DEEPSEEK_API_KEY",
24:    "DSH_KEY_FILE / DSH_API_KEY (repli)"
25:   ],
26:   "cle_absente": {
27:    "code": 4,
28:    "message": "clé DeepSeek absente ; le défaut reste l'heuristique hors ligne"
29:   },
30:   "cache": "mémoire par (texte, langue) dans chaque tagger + cache disque du client (modèle + messages + température + max_tokens, jamais la clé)",
31:   "defaut": "heuristique, CPU
… [5173 caractères tronqués]
  ```

### 🤖 Assistant

⏵ J'écris la fiche et le JSON de résultat, puis la doc produit

- **write** `{"content": "# R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne\n\n> **Ligne de roadmap** : **R0.7** (le lecteur) · **Décision** : **1A** du 14/11 · **Date** :\n> 2026-11-14 · **Verdict** : ✅ **option livrée** — `--tagger` sur `analys … [9644 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-option.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "> **Vérifié le 2026-11-14** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est\n> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`\n> existent … [1521 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**Prérequis** : le dépôt, Python 3.10+ (testé en 3.13), **aucune dépendance externe**, aucun GPU,\naucun accès réseau **par défaut** (le tagger en option, lui, appelle l'API DeepSeek, § 3.7). Les\n … [361 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "### 3.7 Le tagger en option — `--tagger`\n\n```bash\npython3 tools/drave.py analyser \"Le chat dort.\" --tagger\npython3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger\npython3 tools … [3350 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**3. `cascade_pos` : le plancher, pas le gain.** La « rouge » historique est devenue un\n**plancher** : le banc exige **0,70** et la cascade rend **0,7465**, donc la porte\n`porte-bloc-linguistique … [2049 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"hors réseau\\|Codes de sortie\\|non implémenté\\|code \\*\\*4\\*\\*\" docs/produit/README.md | head", "description": "Repérer les lignes des codes et garanties"}`

  ```
386:message clair sur `stderr` et sort avec le code **4** ; rien n'est rendu sur `stdout`.
512:| **hors réseau** | le chemin par défaut n'ouvre aucune socket | analyse `heuristique` seulement ; les adaptateurs neuronaux sont locaux et non utilisés |
527:**Codes de sortie — ce qui existe.** Le CLI implémente **0 / 1 / 2 / 3** ; le code **4** (dépendance
536:| **4** | dépendance absente : modèle, profils | **non implémenté** |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 40, "offset": 505}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
505: phrase. Les temps sont CPU, sur machine partagée ; ils varient avec la charge.
506: 
507: ## 6. Garanties
508: 
509: | garantie | ce que ça veut dire | contrôle |
510: |---|---|---|
511: | **déterminisme** | même entrée → même JSON, octet pour octet | `drave rejouer` (§ 3.4) ; `tools/tests/test_produit.py` compare deux sorties |
512: | **hors réseau** | le chemin par défaut n'ouvre aucune socket | analyse `heuristique` seulement ; les adaptateurs neuronaux sont locaux et non utilisés |
513: | **refus explicite** | texte vide ou sans lettre/chiffre → `refus: "vide"`, 0 étiquette | bloc : JSON ; CLI : JSON sur `stdout` + code 3 |
514: | **pas d'invention** | chaque étiquette porte `source`, `confiance`, `candidats` ; `und` plutôt qu'une langue forcée | JSON ; `--langue` est un indice |
515: | **spans lisibles** | indices en **points de code Unicode**, 0-based, `[debut:fin)` | « Élodie » → `[0:6]` ; emoji = 1 point |
516: | **UTF-8** | le JSON est en UTF-8, non échappé, sans durée | `--json` ; `test_produit.py` vérifie l'absence de `duree_s` |
517: | **gold versionné** 
… [2049 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **hors réseau** | le chemin par défaut n'ouvre aucune socket | analyse `heuristique` seulement ; le tagger API exige `--tagger` et une clé |", "old_string": "| **hors réseau** | le chemin par déf … [119 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**Codes de sortie — ce qui existe.** Le CLI implémente **0 / 1 / 2 / 3 / 4** :\n\n| code | sens | aujourd'hui |\n|---:|---|---|\n| **0** | succès : annotation rendue, évaluation rendue, rejeu ident … [1903 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 80, "offset": 544}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
544: 
545: Le point d'entrée existe : `tools/drave.py`, version **0.1.0**, sans dépendance externe.
546: 
547: ```bash
548: python3 tools/drave.py --version
549: python3 tools/drave.py --aide
550: python3 tools/drave.py analyser "Le chat dort." [--langue fr|en] [--json] \
551:     [--partition brut|alternative|filtrer_union|filtrer] [--contexte TEXTE]
552: python3 tools/drave.py analyser --fichier corpus.txt [--jsonl|--json]
553: python3 tools/drave.py evaluer [--gold] [--json] [--par-langue]
554: python3 tools/drave.py rejouer "TEXTE" [--langue fr|en]
555: python3 tools/drave.py restituer "TEXTE" [--langue fr|en] [--json] [--fichier CHEMIN]
556: python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json [--json]
557: ```
558: 
559: **Sorties réelles des commandes** (07/11 pour le format ; les valeurs d'`evaluer` sont celles
560: mesurées le 14/11) :
561: 
562: ```
563: $ python3 tools/drave.py --version
564: drave 0.1.0
565: 
566: $ python3 tools/drave.py evaluer --gold
567: drave 0.1.0 — évaluation de l'heuristique sur le gold
568: gold gelé (référenc
… [4046 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "```bash\npython3 tools/drave.py --version\npython3 tools/drave.py --aide\npython3 tools/drave.py analyser \"Le chat dort.\" [--langue fr|en] [--json] [--tagger] \\\n    [--partition brut|alternativ … [1262 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| `--json` | `analyser`, `evaluer`, `restituer` | sortie machine UTF-8 |\n| `--tagger` | `analyser`, `evaluer` | POS par l'API DeepSeek (clé et réseau ; défaut : heuristique) ; `evaluer` mesure en  … [125 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **`rejouer` sur un JSON sauvegardé** | `rejouer` prend un **texte**, pas une annotation ; on ne peut pas rejouer un fichier produit hier |\n| **`--mode` / la cascade locale** | le CLI expose l'he … [3664 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "étiqueté en `fr` et `en`, `sha256 f4b7822076a4203d` deux fois, **18 tests** de fumée, **8 tests**", "old_string": "étiqueté en `fr` et `en`, `sha256 f4b7822076a4203d` deux fois, **16 tests** de fum … [17 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **la cascade réelle** (0,9415, 7B, non livrée) | [`reports/rapport-pensee-gold-cascade.md`](../../reports/rapport-pensee-gold-cascade.md) |\n| **le tagger en option** (mesure 20/612, coût, tests) … [323 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-coordination-r.md`](rapport-coordination-r.md) | **R** — tagger POS 612 : **0,9475 (+8,49)** |\n| [`rapport-tagger-option.md`](rapport-tagger-option.md) | **R0.7 / 1A** — le tagger POS en op … [197 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 8, "offset": 28}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
28: | [`rapport-passe-honnetete.md`](rapport-passe-honnetete.md) | **J9.1** — la passe d'honnêteté : **19** fiches |
29: | [`rapport-coordination-n2.md`](rapport-coordination-n2.md) | **N2** — le mètre RoPE : 8,0225 → |
30: | [`rapport-coordination-s.md`](rapport-coordination-s.md) | **S** — les 11 verdicts non committés |
31: | [`rapport-coordination-r.md`](rapport-coordination-r.md) | **R** — tagger POS 612 : **0,9475 (+8,49)** |
32: | [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |
33: | [`rapport-corpus-commun.md`](rapport-corpus-commun.md) | **Panini** — le corpus commun UDHR |
34: | [`rapport-retrieval-epoque.md`](rapport-retrieval-epoque.md) | **Panini** — le retrieval contrôlé |
35: | [`rapport-retrieval-familles.md`](rapport-retrieval-familles.md) | **Panini** — le retrieval approfondi par famille |

(Showing lines 28-35 of 210. Use offset=36 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-coordination-r.md`](rapport-coordination-r.md) | **R** — tagger POS 612 : **0,9475 (+8,49)** |\n| [`rapport-tagger-option.md`](rapport-tagger-option.md) | **R0.7 / 1A** — le tagger POS en op … [197 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Je passe les portes doc et le smoke test après l'ajout de la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -20; echo \"revue=$?\"", "description": "Lancer la revue de documentation"}`

  ```
revue de documentation · 734 fiche(s) · 827 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -4; echo \"taille=$?\"; python3 tools/tests/test_produit.py 2>&1 | tail -3; echo \"produit=$?\"; python3 tools/tests/test_tagger_api.py 2>&1 | tail -3; echo \"tagger=$?\"", "description": … [45 caractères tronqués]`

  ```
avertissements :
     · 51 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
taille=0
Ran 18 tests in 7.429s

OK
produit=0
Ran 14 tests in 2.008s

OK
tagger=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fichiers / JSON\" docs/pilotage/en-cours.md; git status --short | head -20; date", "description": "Vérifier le compteur de l'état et le statut git"}`

  ```
106:| fichiers / JSON de résultats | **734** / **827** | `reports/*.md` / `reports/*.json` |
M  docs/pilotage/en-cours.md
MM docs/produit/README.md
MM journal/2026-11-14/README.md
MM journal/2026-11-14/distribue.md
MM journal/2026-11-14/docs.md
MM journal/2026-11-14/memoire.md
MM journal/2026-11-14/mesures.md
MM journal/2026-11-14/moteur.md
MM journal/2026-11-14/portes.md
MM journal/README.md
MM journal/THEMES.md
D  journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/digest.md
D  journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/rapport.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
MM journal/sessions/session-a68c9aaf-bd76-458b-8501-5a29431b2e10/digest.md
MM journal/sessions/session-a68c9aaf-bd76-458b-8501-5a29431b2e10/rapport.md
 M reports/README.md
 M reports/pensee-coherence-fiches-v7.json
sam 14 nov 2026 11:06:01 EST
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh 2>&1 | tail -15; echo \"porte_produit=$?\"", "description": "Lancer la porte produit complète"}`

  ```
[still running after 60000ms; moved to background job bash-4989]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat tools/drave.py docs/produit/README.md reports/README.md; git diff tools/drave.py | head -120", "description": "Relire le diff de la CLI"}`

  ```
docs/produit/README.md | 1 +
 reports/README.md      | 1 +
 2 files changed, 2 insertions(+)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"drave|tagger|produit|reports/README|en-cours\"; echo ----; git diff --cached --stat | head -20; echo ----; git diff --cached tools/drave.py | head -30", "description": "Vérifier l'index git"}`

  ```
M docs/produit/README.md
 M reports/README.md
----
 journal/2026-11-14/README.md                       |   19 +-
 journal/2026-11-14/distribue.md                    |    7 +-
 journal/2026-11-14/docs.md                         |    7 +-
 journal/2026-11-14/memoire.md                      |    6 +-
 journal/2026-11-14/mesures.md                      |   11 +-
 journal/2026-11-14/moteur.md                       |    3 +-
 journal/2026-11-14/portes.md                       |    3 +-
 journal/README.md                                  |    5 +-
 journal/THEMES.md                                  |    2 +-
 .../24e34ad3-f423-4394-bb1c-74a6930a57e5/digest.md | 2483 --------------------
 .../rapport.md                                     |  141 --
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  799 -------
 .../rapport.md                                     |  144 +-
 .../digest.md                                      |  161 --
 .../rapport.md                                     |   57 +-
 16 files changed, 41 insertions(+), 3814 deletions(-)
----
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -40; echo ----; git log --oneline -5; echo ----; git ls-files tools/drave.py tools/tests/test_tagger_api.py reports/rapport-tagger-option.md reports/pensee-tagger-option.json", "description": "Vérifier si le … [34 caractères tronqués]`

  ```
M docs/produit/README.md
MM journal/2026-11-14/README.md
MM journal/2026-11-14/distribue.md
MM journal/2026-11-14/docs.md
MM journal/2026-11-14/memoire.md
MM journal/2026-11-14/mesures.md
MM journal/2026-11-14/moteur.md
MM journal/2026-11-14/portes.md
MM journal/README.md
MM journal/THEMES.md
D  journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/digest.md
D  journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/rapport.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
MM journal/sessions/session-a68c9aaf-bd76-458b-8501-5a29431b2e10/digest.md
MM journal/sessions/session-a68c9aaf-bd76-458b-8501-5a29431b2e10/rapport.md
 M reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
?? journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/
?? reports/rapport-s-paragraphes.md
----
0bbdbbb3 1A — LE TAGGER POS EN OPTION (--
… [716 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD:docs/produit/README.md | grep -n \"3.7\\|--tagger\\|code \\*\\*4\" | head -12; echo ----; git diff HEAD -- docs/produit/README.md | head -80", "description": "Comparer la doc committée et l'arbre de travail"}`

  ```
11:> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
12:> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le format
33:aucun accès réseau **par défaut** (le tagger en option, lui, appelle l'API DeepSeek, § 3.7). Les
129:gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement
131:POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
134:  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture
342:contrôle négatif : mélange exacte 0.0000 (caractères 0.3077) · troncature exacte 0.0000
362:### 3.7 Le tagger en option — `--tagger`
365:python3 tools/drave.py analyser "Le chat dort." --tagger
366:python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
367:python3 tools/drave.py evaluer --tagger
386:message clair sur `stderr` et sort avec le code **4** ; rien n'est rendu sur `stdout`.
----
diff --git a/docs/produit/README.md b/docs/produit/README.md
index 73248b7f..045a35ae 100644
--- a/docs/produit/README.md
+++ b/docs/produit/README.md
@@ -640,6 +640,7 @@ inchangé), la porte produit et le smoke test. Le reste est nommé ci-dess
… [1059 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-4989"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/drave.py tools/tests/test_tagger_api.py reports/rapport-tagger-option.md reports/pensee-tagger-option.json; git diff HEAD --stat", "description": "Vérifier l'état des fichiers committés"}`

  ```
docs/produit/README.md                             |    1 +
 .../24e34ad3-f423-4394-bb1c-74a6930a57e5/digest.md | 2483 --------------------
 .../rapport.md                                     |  141 --
 reports/README.md                                  |    1 +
 reports/pensee-coherence-fiches-v7.json            |   19 +
 reports/pensee-dev-test-v10.json                   |    2 +-
 reports/pensee-quatre-modes.json                   |  734 +++---
 reports/rapport-audit-v7.md                        |    6 +-
 reports/rapport-coherence-fiches-v7.md             |   17 +-
 reports/rapport-dev-test-v10.md                    |    2 +-
 reports/rapport-pensee-v12.md                      |    4 +-
 reports/rapport-spans-chunker.md                   |   13 +-
 12 files changed, 462 insertions(+), 2961 deletions(-)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "TAGGER API  modèle=deepseek-chat · appels=2 · réseau=0 · cache=2 · tokens=0 · latence=0.0 s\n```\n\nIci le cache disque avait déjà les deux réponses ; un **premier** appel affiche `réseau=2`, les\n … [337 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

### 👤 Utilisateur

background job bash-4989 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh 2>&1 | tail -15; echo "porte_produit=$?") finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-4989"}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 18 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
porte_produit=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show -s --format='%h %ci %s' 0bbdbbb3; git show --stat --oneline 0bbdbbb3 | head -20", "description": "Inspecter le commit existant"}`

  ```
0bbdbbb3 2026-11-14 11:04:54 -0500 1A — LE TAGGER POS EN OPTION (--tagger) : +8,49 PTS SUR LE GOLD 612 (+4,67 SUR LE RÉEL 432), LE DÉFAUT RESTE HORS LIGNE ; 14 TESTS, DOC § 3.7
0bbdbbb3 1A — LE TAGGER POS EN OPTION (--tagger) : +8,49 PTS SUR LE GOLD 612 (+4,67 SUR LE RÉEL 432), LE DÉFAUT RESTE HORS LIGNE ; 14 TESTS, DOC § 3.7
 docs/pilotage/en-cours.md                          |    4 +-
 docs/produit/README.md                             |  123 +-
 journal/2026-11-14/README.md                       |    9 +-
 journal/2026-11-14/distribue.md                    |    4 +-
 journal/2026-11-14/docs.md                         |    7 +-
 journal/2026-11-14/memoire.md                      |    4 +-
 journal/2026-11-14/mesures.md                      |    4 +-
 journal/2026-11-14/moteur.md                       |    4 +-
 journal/2026-11-14/portes.md                       |    4 +-
 journal/README.md                                  |    4 +-
 .../24e34ad3-f423-4394-bb1c-74a6930a57e5/digest.md | 1171 ++++++++++++++++++++
 .../rapport.md                                     |   54 +-
 journal/sessions/MANIFEST.md                       |    6 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest
… [335 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je relance les trois portes demandées et vérifie les liens de la doc finale

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py >/tmp/revue.log 2>&1; echo \"revue=$?\"; tail -3 /tmp/revue.log; python3 tools/taille_documents.py >/tmp/taille.log 2>&1; echo \"taille=$?\"; tail -2 /tmp/taille.log", "description": "Relancer rev … [14 caractères tronqués]`

  ```
revue=0
  revue de documentation · 734 fiche(s) · 827 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
taille=0

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_produit.py >/tmp/produit.log 2>&1; echo \"produit=$?\"; tail -3 /tmp/produit.log; python3 tools/tests/test_tagger_api.py >/tmp/tagger.log 2>&1; echo \"tagger=$?\"; tail -3 /tmp/tagger.log; git diff --check; e … [76 caractères tronqués]`

  ```
produit=0
Ran 18 tests in 7.206s

OK
tagger=0
Ran 14 tests in 1.916s

OK
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:62223: trailing whitespace.
+4012729 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES 
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:62240: trailing whitespace.
+ {"phrase_id": "a003", "candidat_id": "a003-c2", "statut": "resolu", "referents": {"Elle": "Alice", "sa": "Alice", "elle": "Alice", "se": "Alice"}, "note": "", "contexte": "Allons, à quoi bon pleurer ainsi, se dit Alice 
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:62301: trailing whitespace.
+Mêmes mesures que la cascade : POS, syntagmes F1, tête F1, acte, fraction, 
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:62650: trailing whitespace.
+33:aucun accès réseau **par défaut** (le tagger en option, lui, appelle 
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md:11279: trailing whitespace.
+- CHANTIER — LE PLAN RESTAURÉ (29 TÂCHES, J11-J14 RÉINTÉGRÉES) ; ÉTAT HORODATÉ" -- tools/chantier/plan.json docs/pilotage/en-cours.md 2>&1 | tail -1   if git log 
journal/sessions/session-a68c9aaf-bd76-458b-850
… [659 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/evaluer_20_par_langue.py <<'PY'\nimport json, pathlib, sys\nR = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0, str(R)); sys.path.insert(0, str(R/'tools'))\nimport drave\nev = drave._module_evaluation()\nchargeur = ev.charger\nev.charger =  … [756 caractères tronqués]`

  ```
code ok, langues ['fr']
fr {'exactitude': 1.0, 'exactitude_ferme': 1.0, 'exactitude_ouvert': 1.0, 'tokens': 9} 0.0 {'f1': 0.9091, 'tete': {'f1': 1.0}}
global tagger delta 0.0
erreur:
drave: TAGGER API · modèle=deepseek-chat · appels=4 · réseau=0 · cache=4 · tokens=0 · latence=0.0 s
  ```

- **bash** `{"command": "cat > /tmp/evaluer_2_par_langue_txt.py <<'PY'\nimport pathlib, sys\nR = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0, str(R)); sys.path.insert(0, str(R/'tools'))\nimport drave\nev = drave._module_evaluation()\nchargeur = ev.charger\nev.charger = lam … [402 caractères tronqués]`

  ```
TAGGER API DEEPSEEK (option --tagger)
  POS         exactitude 100.00 % (fermé 100.00 %, ouvert 100.00 %) · Δ +0.00 pts vs heuristique
  SYNTAGMES   F1 90.91 % (tête 100.00 %) — conservés à l'heuristique
  COÛT        appels 4 · réseau 0 · cache 4 · tokens 0 · modèle deepseek-chat
  modèle renvoyé : deepseek-flash

PAR LANGUE
  fr  2 phrases · 9 tokens · 1 cibles d'attachement
      POS 100.00 % (fermé 100.00 %, ouvert 100.00 %) · SYNTAGMES F1 90.91 % (tête 100.00 %)
      ATTACHEMENT exact 100.00 % · couverture 100.00 % · top-k 100.00 % · PRAGMATIQUE acte 100.00 %
      CONTRÔLE NÉGATIF cible exacte tirée au hasard 100.00 % (graine 0, 1 cibles)
      TAGGER POS 100.00 % · Δ +0.00 pts · SYNTAGMES F1 90.91 % (tête 100.00 %)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 360,430p docs/produit/README.md", "description": "Relire la section 3.7 finale"}`

  ```
[`rapport-restitution-v1.md`](../../reports/rapport-restitution-v1.md).

### 3.7 Le tagger en option — `--tagger`

```bash
python3 tools/drave.py analyser "Le chat dort." --tagger
python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
python3 tools/drave.py evaluer --tagger
```
```
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 19 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.60 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=2 · réseau=0 · cache=2 · tokens=0 · latence=0.0 s
```

Ici le cache disque avait déjà les deux réponses ; un **premier** appel affiche `réseau=2`, les
tokens et la latence (voir le coût ci-dessous).

**La clé.** Lue dans `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`, puis
`DEEPSEEK_A
… [2880 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD -- docs/pilotage/en-cours.md | head -60", "description": "Voir la mise à jour de l'état par le parent"}`

  ```
commit 0bbdbbb3256cb38a857531ccf9a4abfc6dce075e
Author: Stéphane <stephane@localhost>
Date:   Sat Nov 14 11:04:54 2026 -0500

    1A — LE TAGGER POS EN OPTION (--tagger) : +8,49 PTS SUR LE GOLD 612 (+4,67 SUR LE RÉEL 432), LE DÉFAUT RESTE HORS LIGNE ; 14 TESTS, DOC § 3.7

diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 56db3554..094c7788 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-14, 10 h 10 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-14, 11 h 10 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -103,7 +103,7 @@
 |---|---|---|
 | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
 | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
-| fichiers / JSON de résultats | **733** / **826** | `reports/*.md` / `reports/*.json` |
+| fichiers / JSON de résultats | **734** / **827** | `reports/*.md` / `reports/*.json` |
 | documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
 | dernière passe | **14/11 00 h 30** 
… [152 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD -- docs/pilotage/en-cours.md | grep -n \"tagger\\|1A\" ; grep -n \"tagger\\|1A\" docs/pilotage/en-cours.md | head", "description": "Chercher la ligne tagger dans l'état"}`

  ```
5:    1A — LE TAGGER POS EN OPTION (--tagger) : +8,49 PTS SUR LE GOLD 612 (+4,67 SUR LE RÉEL 432), LE DÉFAUT RESTE HORS LIGNE ; 14 TESTS, DOC § 3.7
95:- **J5.1 / J10.1 / J13.1 / J14.1 — les bilans et la clôture** : semaine (F1 **0,7533 → 0,7902**, tagger **0,9475** ; [rapport](../../reports/rapport-semaine.md)) ; chantier **20/21**, attachement **236 → 238**, 5 timeouts, 1 échec (J5.2), D1–D20, R1–R30 ; [bilan](../../reports/rapport-bilan-chantier.md) ; **J13.1** — tableau des mesures : **612/602** ; [tableau](../../reports/rapport-tableau-mesures.md) ; **J14.1** — clôture (**84/81/3**, tag `chantier-2026-11-14` ; [rapport](../../reports/rapport-cloture-chantier.md)).
120:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9475 (+8,49), intégrer** ; R2/R3 attendent N5/N4 | **route API derrière drapeau** ; **split réel tenu à l'écart** |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-*.sh | sed 's#tools/##' | head -40; echo ----; grep -rln \"test_tagger_api\\|test_produit.py\" tools/porte-*.sh tools/*.sh 2>/dev/null", "description": "Chercher la porte qui exécute les tests"}`

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
----
tools/porte-produit.sh
tools/porte-produit.sh
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,80p tools/porte-deepseek.sh; echo ====; grep -n \"deepseek\" tools/porte-produit.sh", "description": "Lire la porte deepseek"}`

  ```
#!/bin/bash
# porte-deepseek.sh — le banc externe, sans réseau et sans clé.
#
# CE QU'ELLE VERROUILLE :
#   1. les tests de l'adaptateur, du corpus professeur et de la distillation
#      (transport factice, aucun appel réseau, aucune clé réelle) ;
#   2. le dry-run de l'adaptateur : réponse déterministe, pas de requête ;
#   3. les 60 prompts publics : 50 traductions UDHR + 10 questions de jeux ;
#   4. le dry-run du corpus professeur : il écrit, mais `distillation.py`
#      l'ignore — un faux professeur ne devient jamais un corpus d'entraînement.
#
# La mesure **live** est opt-in : `DEEPSEEK_API_KEY=... DEEPSEEK_LIVE=1
# bash tools/porte-deepseek.sh`. Sans clé, la porte est verte et le dit.
set -u
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/tools${PYTHONPATH:+:$PYTHONPATH}"
T="${JOURNAUX:-/tmp}/deepseek-porte"
rm -rf "$T"; mkdir -p "$T"

echo "  === tests (adaptateur, corpus, distillation) ==="
python3 -m unittest discover -s tools/llm/tests -t tools || exit 1

echo "  === dry-run de l'adaptateur ==="
python3 tools/llm/deepseek.py --prompt "test de la porte" --dry-run --json > "$T/dry.json" || exit 1
python3 - "$T/dry.json" <<'PY' || exit 1
import json, sys
d = json.load(ope
… [2143 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff HEAD -- docs/produit/README.md reports/README.md", "description": "Voir les lignes non committées"}`

  ```
diff --git a/docs/produit/README.md b/docs/produit/README.md
index 73248b7f..aa0118ca 100644
--- a/docs/produit/README.md
+++ b/docs/produit/README.md
@@ -380,6 +380,9 @@ COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.60 
 TAGGER API  modèle=deepseek-chat · appels=2 · réseau=0 · cache=2 · tokens=0 · latence=0.0 s
 ```
 
+Ici le cache disque avait déjà les deux réponses ; un **premier** appel affiche `réseau=2`, les
+tokens et la latence (voir le coût ci-dessous).
+
 **La clé.** Lue dans `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`, puis
 `DEEPSEEK_API_KEY` (`DSH_KEY_FILE` / `DSH_API_KEY` en repli). Elle n'est **jamais** affichée :
 ni dans le message, ni dans le JSON, ni dans le cache. **Sans clé**, la commande écrit un
@@ -640,6 +643,7 @@ inchangé), la porte produit et le smoke test. Le reste est nommé ci-dessus, sa
 | **la mesure par langue** (fr/en, source contrôlée) | [`reports/rapport-evaluer-langue.md`](../../reports/rapport-evaluer-langue.md) |
 | **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |
 | **la cascade réelle** (0,9415, 7B, non livré
… [1645 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie le chemin réseau réel de la CLI (cache neuf puis cache chaud)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf /tmp/drave-tagger-cli-frais && DEEPSEEK_KEY_FILE=\"$HOME/.config/drave/deepseek.key\" DEEPSEEK_CACHE=/tmp/drave-tagger-cli-frais python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --tag … [562 caractères tronqués]`

  ```
code=0
drave: TAGGER API · modèle=deepseek-chat · appels=2 · réseau=2 · cache=0 · tokens=685 · latence=2.6 s
--- second passage (cache) ---
code=0
drave: TAGGER API · modèle=deepseek-chat · appels=2 · réseau=0 · cache=2 · tokens=0 · latence=0.0 s
json_identique=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3; git status --short | head -12; date", "description": "Vérifier l'état git final"}`

  ```
9df4a591 ÉTAT — LES DÉCISIONS INSCRITES : g017 INATTEIGNABLE (2A), LE TAGGER EN OPTION (1A), LES 11 VERDICTS (3B), LA NOTE PANINI (4A), A6.2 REPOUSSÉ (5A)
0bbdbbb3 1A — LE TAGGER POS EN OPTION (--tagger) : +8,49 PTS SUR LE GOLD 612 (+4,67 SUR LE RÉEL 432), LE DÉFAUT RESTE HORS LIGNE ; 14 TESTS, DOC § 3.7
883ce817 CHANTIER — LE PLAN RESTAURÉ (29 TÂCHES, J11-J14 RÉINTÉGRÉES) ; ÉTAT HORODATÉ
 M docs/produit/README.md
MM journal/2026-11-14/README.md
MM journal/2026-11-14/distribue.md
MM journal/2026-11-14/docs.md
MM journal/2026-11-14/memoire.md
MM journal/2026-11-14/mesures.md
MM journal/2026-11-14/moteur.md
MM journal/2026-11-14/portes.md
MM journal/README.md
MM journal/THEMES.md
D  journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/digest.md
D  journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/rapport.md
sam 14 nov 2026 11:16:32 EST
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline 9df4a591 | head -15; git show 9df4a591 -- docs/pilotage/en-cours.md | grep -n \"tagger\\|1A\" | head", "description": "Voir le commit d'état du parent"}`

  ```
9df4a591 ÉTAT — LES DÉCISIONS INSCRITES : g017 INATTEIGNABLE (2A), LE TAGGER EN OPTION (1A), LES 11 VERDICTS (3B), LA NOTE PANINI (4A), A6.2 REPOUSSÉ (5A)
 docs/pilotage/en-cours.md                          |   4 +-
 journal/2026-11-14/README.md                       |   9 +-
 journal/2026-11-14/distribue.md                    |   4 +-
 journal/2026-11-14/docs.md                         |   4 +-
 journal/2026-11-14/memoire.md                      |   4 +-
 journal/2026-11-14/mesures.md                      |   4 +-
 journal/2026-11-14/moteur.md                       |   4 +-
 journal/2026-11-14/portes.md                       |   8 +-
 journal/README.md                                  |   4 +-
 .../24e34ad3-f423-4394-bb1c-74a6930a57e5/digest.md | 313 +++++++++++++++++++++
 .../rapport.md                                     |  28 +-
 journal/sessions/MANIFEST.md                       |   4 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  29 ++
 .../rapport.md                                     |  17 +-
5:    ÉTAT — LES DÉCISIONS INSCRITES : g017 INATTEIGNABLE (2A), LE TAGGER EN OPTION (1A), LES 11 VERDICTS (3B), LA NOTE PANINI (4A), A6.2 REPOUSSÉ (5A)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 9df4a591 -- docs/pilotage/en-cours.md | head -50; grep -n \"R0.7\\|tagger\" docs/pilotage/en-cours.md | head", "description": "Lire le diff en-cours du dernier commit"}`

  ```
commit 9df4a5916b967ca01a6724a06bf4e5b416914cf1
Author: Stéphane <stephane@localhost>
Date:   Sat Nov 14 11:10:04 2026 -0500

    ÉTAT — LES DÉCISIONS INSCRITES : g017 INATTEIGNABLE (2A), LE TAGGER EN OPTION (1A), LES 11 VERDICTS (3B), LA NOTE PANINI (4A), A6.2 REPOUSSÉ (5A)

diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 094c7788..2d3b6b9c 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-14, 11 h 10 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-14, 11 h 15 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -61,7 +61,7 @@
 - **Stratégie** : v0 mesuré.
 - **Ambition** : un runtime cognitif tracé.
 - **Objectif final** : un moteur de pensée v0.
-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** ; **restitution v1** (46/46 
… [2129 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -- reports/rapport-tagger-option.md reports/pensee-tagger-option.json tools/drave.py tools/tests/test_tagger_api.py; echo ----; git status --short reports/rapport-tagger-option.md reports/pensee-tagger-option.json t … [134 caractères tronqués]`

  ```
0bbdbbb3 1A — LE TAGGER POS EN OPTION (--tagger) : +8,49 PTS SUR LE GOLD 612 (+4,67 SUR LE RÉEL 432), LE DÉFAUT RESTE HORS LIGNE ; 14 TESTS, DOC § 3.7
09e54143 J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ
229098ec J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
8eb0cc49 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE
5b9c18ef PRODUIT — --fichier ET --jsonl (TRAITEMENT DE CORPUS, UNE LIGNE JSON PAR PHRASE) ; 16 TESTS
662a3698 PRODUIT — evaluer PUBLIE LES DEUX VUES (FIDÈLE F1 75,33 / LINÉAIRE 81,04, COUVERTURE 93,31) ; 14 TESTS
027abba4 PRODUIT — --contexte DANS LA CLI (MÉMOIRE DE DISCOURS PORTÉE DANS LE JSON), 11 TESTS
d31aa9a2 PRODUIT — --partition DANS LA CLI (alternative PAR DÉFAUT, filtrer EN OPTION), 10 TESTS, DOC À JOUR
037fe041 PRODUIT — LE CONTRAT V1 : schema/version, REFUS EN JSON (CODE 3), SURROGATE ET NON-STR TOLÉRÉS ; PORTE À 8 CONTRÔLES ; 183/183
62dad657 B13 — LE PREMIER PRODUIT : drave v0 (ANALYSER/EVALUER/REJOUER), PORTE PRODUIT VERTE (6 CONTRÔLES), SMOKE TEST 6 CAS ; 183/183
----
(vide = committé)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -2; echo \"revue=$?\"; python3 tools/taille_documents.py 2>&1 | tail -1; echo \"taille=$?\"", "description": "Dernière vérification des portes doc"}`

  ```
revue de documentation · 734 fiche(s) · 827 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
     · T0 : 4007 mots (AGENTS + en-cours + une tâche) > budget 4 000
taille=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -15; echo \"code=$?\"; grep -n \"4000\\|T0\\|budget\" tools/taille_documents.py | tail -20", "description": "Comprendre l'avertissement de budget T0"}`

  ```
2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4007 mots (budget 4 000)

  avertissements :
     · 51 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4007 mots (AGENTS + en-cours + une tâche) > budget 4 000
code=0
90:    for cat, motif, budget in BUDGETS:
92:            return cat, budget
101:    for cat, motif, budget in BUDGETS:
110:            lignes.append((n, t.count("\n") + 1, rel, cat, budget))
112:            if cat in ("T0", "
… [1104 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py >/tmp/taille2.log 2>&1; echo \"taille_reel=$?\"; tail -4 /tmp/taille2.log; git log --oneline -1 -- docs/pilotage/en-cours.md", "description": "Obtenir le vrai code de taille_documents"}`

  ```
taille_reel=1
     · 51 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4007 mots (AGENTS + en-cours + une tâche) > budget 4 000
9df4a591 ÉTAT — LES DÉCISIONS INSCRITES : g017 INATTEIGNABLE (2A), LE TAGGER EN OPTION (1A), LES 11 VERDICTS (3B), LA NOTE PANINI (4A), A6.2 REPOUSSÉ (5A)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 80,160p tools/taille_documents.py", "description": "Lire le calcul du budget T0"}`

  ```
r"^[ \t]*```[ \t]*(?:plantuml|puml|pu|mermaid|mmd)[ \t]*\n.*?^[ \t]*```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)


def mots_hors_diagrammes(texte: str) -> int:
    return mots(DIAGRAMME.sub("", texte))


def classe(rel: str) -> tuple[str, int]:
    for cat, motif, budget in BUDGETS:
        if pathlib.Path(rel).match(motif):
            return cat, budget
    return "", 0


def main() -> int:
    lignes: list[tuple[int, int, str, str, int]] = []
    violations: list[str] = []
    avertissements: list[str] = []
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
 
… [2536 caractères tronqués]
  ```

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Alerte porte (pas un blocage de mon côté) : `python3 tools/taille_documents.py` est ROUGE depuis ton commit 9df4a591 — T0 = 4007 mots > budget 4000 (7 mots de trop). La cause est dans `docs/pilotage/en-cours.md` (ligne « Fait » : « g01 … [506 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py >/tmp/taille3.log 2>&1; echo \"taille=$?\"; tail -3 /tmp/taille3.log; git log --oneline -2", "description": "Revérifier le budget T0 après alerte"}`

  ```
taille=0
     · 51 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
9df4a591 ÉTAT — LES DÉCISIONS INSCRITES : g017 INATTEIGNABLE (2A), LE TAGGER EN OPTION (1A), LES 11 VERDICTS (3B), LA NOTE PANINI (4A), A6.2 REPOUSSÉ (5A)
0bbdbbb3 1A — LE TAGGER POS EN OPTION (--tagger) : +8,49 PTS SUR LE GOLD 612 (+4,67 SUR LE RÉEL 432), LE DÉFAUT RESTE HORS LIGNE ; 14 TESTS, DOC § 3.7
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short docs/pilotage/en-cours.md; grep -n \"T0 max\" /tmp/taille3.log; grep -n \"g017\" docs/pilotage/en-cours.md | head -3", "description": "Voir la correction d'en-cours"}`

  ```
M  docs/pilotage/en-cours.md
21:  T0 max : 3996 mots (budget 4 000)
64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`, inatteignable)** ; **`s065` réglé** ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)).
67:- **Prochaine action** : **trancher la convention d'adverbe (`g017`)** ; puis T132/T133, gold 200+.
90:- **Pensée — B13 (actif)** : **183/183**, gold 432 ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejetée** (g017 à trancher), schéma v2, restitution v1 (46/46, strict 0,1087), **J9.1** (19 fiches) ; [s065](../../reports/rapport-s065.md), [restitution v1](../../reports/rapport-restitution-v1.md), [J9.1](../../reports/rapport-passe-honnetete.md).
  ```

### 🤖 Assistant

⏵ Je confirme les trois portes avec leurs codes de sortie réels

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py >/tmp/r.log 2>&1; echo \"revue=$?\"; python3 tools/taille_documents.py >/tmp/t.log 2>&1; echo \"taille=$?\"; python3 tools/tests/test_produit.py >/tmp/p.log 2>&1; echo \"test_produit=$?\"; python3 … [225 caractères tronqués]`

  ```
revue=0
taille=0
test_produit=0
test_tagger=0
---
  revue de documentation · 734 fiche(s) · 827 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
Ran 18 tests in 7.420s

OK
Ran 14 tests in 1.947s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"route API\\|R0.7\" docs/pilotage/en-cours.md | head -5; git status --short docs/produit/README.md docs/pilotage/en-cours.md", "description": "Vérifier la ligne R et l'état des docs"}`

  ```
120:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9475 (+8,49), intégrer** ; R2/R3 attendent N5/N4 | **route API derrière drapeau** ; **split réel tenu à l'écart** |
128:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — 11 verdicts + pointeur ; **R0.7** — split réel ; **A** — A6.2, A8.3b2.
M  docs/pilotage/en-cours.md
 M docs/produit/README.md
  ```

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "RÉSULTAT — 1A « tagger POS en option » livré (défaut inchangé), tout est committé dans 0bbdbbb3.\n\nCOMMANDE\n  python3 tools/drave.py analyser \"TEXTE\" --tagger [--json|--jsonl]\n  python3 tools/drave.py evaluer --tagger [--par-langu … [2941 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

- **todo_write** `{"todos": [{"content": "Implémenter --tagger dans tools/drave.py (analyser + evaluer, clé, cache, code 4)", "status": "completed"}, {"content": "Écrire tools/tests/test_tagger_api.py (transport factice, JSON, défaut, code 4)", "status": "completed"}, {"content": "Mesurer 20 phrases (harnais + CLI) : … [272 caractères tronqués]`

  ```
Updated todo list: 0 pending, 0 in progress, 5 completed.
  ```

### 🤖 Assistant

⏵ Livraison terminée : option `--tagger`, mesure, tests et doc en place

**Commande**
```bash
python3 tools/drave.py analyser "TEXTE" --tagger [--json|--jsonl]
python3 tools/drave.py evaluer --tagger [--par-langue] [--json]
```
Clé : `DEEPSEEK_KEY_FILE` → `~/.config/drave/deepseek.key` → `DEEPSEEK_API_KEY` (repli `DSH_*`). Sans clé : code **4**, message clair, rien sur `stdout`, aucune trace de la clé. Cache mémoire par texte + cache disque du client : la seconde analyse ne refait aucun appel et rend le même JSON. Le défaut, sans le drapeau, est resté l'heuristique hors ligne (comparaison octet pour octet en test).

**Mesure** (20 premières phrases `hand`, 105 tokens, cache neuf)
- POS **0,8857 → 0,9714**, soit **+8,57 pts** (fermé +7,02, ouvert +10,42) ; syntagmes F1, tête, attachement et acte **inchangés** (la fusion ne remplace que le POS).
- **40 appels**, **11 868 tokens**, 39,49 s, 0 refus ; modèle renvoyé `deepseek-flash`.
- Cache chaud : 40 appels transport, **0 réseau, 0 token**, JSON identique.
- Référence 612 : **0,8625 → 0,9475 (+8,49)**, 1 218 appels, 358 962 tokens, ~21 min, ~0,04 $ ; par source : `hand` +8,57, **réel 432 +4,67**, `synth` +21,46 ; 1 refus (`s015`).

**Tests / portes**
- `tools/tests/test_tagger_api.py` : **14 tests OK**, aucun réseau (transport factice, POS remplacés, JSON v2 valide + v1 lisible, cache, défaut inchangé, code 4, ordre de la clé, `evaluer --tagger`).
- `tools/tests/test_produit.py` : **18 tests OK**.
- `revue_documentation` ✅ · `taille_documents` ✅ · `porte-produit` ✅ (183/183).

**Limites**
- Les 20 phrases sont les 20 `hand`, le sous-ensemble le plus facile : ne pas généraliser le +8,57 ; le 612 agrégé vaut +8,49 et le réel 432 seul +4,67.
- Le tagger de syntagmes du composite est appelé mais sa sortie n'est pas utilisée par la fusion (2 appels/phrase, piste 1 appel ~0,02 $ non mesurée).
- `PONCT` n'est plus étiqueté par l'option (le tagger ne reçoit que mots et nombres).
- Modèle effectivement renvoyé `deepseek-flash` ; la mesure exige un cache neuf.
- Aucune porte ne fait d'appel API : le chemin réseau réel est couvert par la mesure 20 phrases et un contrôle 1 phrase.

**État** : code, tests, fiche `reports/rapport-tagger-option.md` et JSON `reports/pensee-tagger-option.json` sont dans le commit `0bbdbbb3` (fait par la session parente). Restent non committées 3 lignes de `docs/produit/README.md` (note cache + lien § 8) ; la ligne R d'`en-cours` mérite d'être requalifiée (« route API derrière drapeau » → livré). Je n'ai pas committé et n'ai pas touché S/D/N2.

