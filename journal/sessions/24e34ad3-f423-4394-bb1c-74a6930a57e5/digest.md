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

