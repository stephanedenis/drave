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

