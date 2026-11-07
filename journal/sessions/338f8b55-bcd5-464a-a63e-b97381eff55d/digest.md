# Session DSH — relecture

- identifiant : `338f8b55-bcd5-464a-a63e-b97381eff55d`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 18:33:56
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **les deux derniers leviers POS** — R4 (copule → ADJ) et les classes fermées anglaises — mesurés sur dev/test, sans modifier le code du dépôt.

Contexte : `tools/bloc_linguistique.py` (`_pos`, `POS_FERME`, `ADJECTIFS`, `SUJETS`, les boucles 3 a/3 b/3 a bis), la fiche `reports/rapport-pos-anglais.md` (A25 : R4 +0,73 dev / +0,70 test, 23/0 ; classes fermées anglaises 28 erreurs : `where` 6, `late` 4, `out` 2, `as` 2, `As` 2, `Maybe` 1, PRON 9, CONJ 2, AUX 1). État : POS **83,83 %** (fermé 91,33 / ouvert 76,73), F1 0,6181, attachement 222/222.

À faire :
1. **R4** : « après une copule (`is`, `are`, `was`, `seems`, `looks`…), un mot inconnu est un ADJ » — mesure sur dev/test (POS, F1, attachement), et contrôle : ne pas convertir un nom (`he is a doctor`) ni un verbe (`he is running`).
2. **Classes fermées anglaises** : complète `POS_FERME["en"]` (ADV : where, late, out, as, maybe… ; PRON : whose, whom… ; CONJ ; AUX) — mesure l'effet sur dev/test et sur les 50 textes libres de `reports/pensee-fiabilite-produit.json`.
3. **Contrôles** : placebo (même action, position aléatoire), et vérifie que l'attachement reste 222/222.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-pos-r4.md` et `reports/pensee-pos-r4.json` (avec les patchs exacts).
5. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, natifs. Simulation par sous-classe ou copie locale.

Rends un résumé : le gain POS/F1 dev/test de R4 et des classes fermées, les pertes, les patchs exacts.
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

⏵ Exploration du dépôt et des fichiers POS concernés

- **bash** `{"command": "git status --short && git branch --show-current && ls", "description": "Check git status and repo layout"}`

  ```
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/2026-11-06/README.md
D  journal/2026-11-06/distribue.md
D  journal/2026-11-06/docs.md
D  journal/2026-11-06/mesures.md
D  journal/2026-11-06/modele.md
D  journal/2026-11-06/outils.md
D  journal/2026-11-06/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/digest.md
D  journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/rapport.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/digest.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/rapport.md
D  journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/digest.md
D  journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/rapport.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/digest.md
D  journal/sessions/1b0cf09a-a7
… [6636 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | head -50 && ls tools/ | head -50", "description": "List reports and tools"}`

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
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeur-mots.json
b10-mots-contraste.json
b10-mots-jw.json
b1110-audit.json
adaptateur_langue.py
aiguille.py
aligneur_litteraire.py
amplification.py
analyse_alignement.py
analyse_empreinte.py
analyse_engram.py
analyse_experts_statique.py
analyse_flux.py
analyse_hc.py
… [841 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/bloc_linguistique.py reports/rapport-pos-anglais.md reports/pensee-fiabilite-produit.json 2>/dev/null; ls reports/ | grep -i pos", "description": "Check sizes of POS files"}`

  ```
2249 tools/bloc_linguistique.py
   439 reports/rapport-pos-anglais.md
  3884 reports/pensee-fiabilite-produit.json
  6572 total
composition-latente-14b.json
composition-latente-3b.json
composition-latente-7b.json
composition-multilingue.json
composition-penalite-3b.json
composition-penalite-7b.json
composition-verne-14b.json
composition-verne-7b.json
composition-verne.json
composition-verne-large.json
composition-verne-plan.json
n3.4a-composition.json
n3.5f-positions.json
pensee-miroir-pos.json
pensee-pos-anglais.json
pensee-pos-anglais-v2.json
position-multilingue.json
r44-sans-exposants.json
rapport-n3.4a-composition.md
rapport-n3.5f-positions.md
rapport-parcimonie-imposee.md
rapport-pensee-miroir-pos.md
rapport-pos-anglais.md
rapport-pos-anglais-v2.md
sonde-octets-position.json
  ```

- **grep** `{"pattern": "attachement|F1|POS", "path": "reports/rapport-pos-anglais.md"}`

  ```
Found 29 matches

reports/rapport-pos-anglais.md
Line 1: # POS anglaise — les 176 VERB gold tagués NOUN viennent du défaut nominal, pas de la règle de contexte
Line 5: > vaut **+7,44 pts de POS au test** et **+3,3 pts de F1** (+9,3 pts sur le F1 anglais) ; le paquet complet (**R1+R2+R3**)
Line 13: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_pos`, `POS_FERME`,
Line 35:   **+3,3 pts de F1**, **0 attachement perdu**.
Line 37:   membres exacts de `VERBES_CONNUS`, lexique ajouté le 05/11 pour les cibles d'attachement du **même**
Line 48: **Mesure.** `evaluer_gold.evaluer_bloc` : POS exacte au jeton, exactitude **fermée** (DET, PREP, PRON,
Line 49: CONJ, AUX, ADV, NUM) et **ouverte** (le reste, ponctuation incluse), F1 syntagme et F1 « tête »,
Line 50: attachement (exact, top-1, top-k). Les règles sont appliquées à une **copie en mémoire** du module
Line 62: | | jetons | erreurs | POS | fermé | ouvert* | part des erreurs |
Line 138: | **C1** | **défaut nominal : le POS ouvert ne consulte pas le lexique verbal** | **176** | **65,2 %** | leave, sings, play, stay, arrives | R1 (lexique) + R2 (position) |
Line 151: **C2 en détail.** `that` est dans `POS_FERM
… [1705 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pos-anglais.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pos-anglais.md</path>
<type>file</type>
<content>
1: # POS anglaise — les 176 VERB gold tagués NOUN viennent du défaut nominal, pas de la règle de contexte
2: 
3: > **Ligne de roadmap** : **A14** (gold anglais) · **Date** : 2026-11-06 · **Verdict** : ✅ trois règles
4: > générales mesurées sur **dev** puis **test** ; le paquet **R2+R3** — sans un mot de lexique nouveau —
5: > vaut **+7,44 pts de POS au test** et **+3,3 pts de F1** (+9,3 pts sur le F1 anglais) ; le paquet complet (**R1+R2+R3**)
6: > vaut **+9,76 pts au test**, mais **R1 exploite un lexique écrit sur ce gold** : son gain mesuré est
7: > en partie de la mémorisation et n'est pas comptable comme généralisation.
8: >
9: > **Snapshot** : HEAD `56eb43af` · `bloc_linguistique.py` SHA `084517d9…` · `gold.json` `3663be6c…`,
10: > `gold_reel.json` `05d4f6df…`, `gold_synthetique.json` `e3e704ce…` · split `gold_split.py`
11: > (`crc32(id) % 3 == 0` → test).
12: >
13: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_pos`, `POS_FERME`,
14: > `VERBES`, `ADJECTIFS`, `_est_verbe`, règle 3 bis), [`evaluer_gold.py`](../tools/tests/linguis
… [27677 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"POS_FERME\\|ADJECTIFS\\|SUJETS\\|def _pos\\|3 a\\.\\|3 b\\.\\|3 a bis\\|pos_idx\" tools/bloc_linguistique.py | head -80", "description": "Locate POS structures in module"}`

  ```
304:POS_FERME = {
346:ADJECTIFS = {
378:SUJETS = {"i", "you", "he", "she", "it", "we", "they", "there", "who", "that", "which",
607:    def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
608:        lex = POS_FERME.get(langue, POS_FERME["fr"])
615:        if n in ADJECTIFS.get(langue, ADJECTIFS["fr"]):
864:        lex = POS_FERME.get(langue, POS_FERME["fr"])
887:                if avant in SUJETS:
1064:        pos_idx = [i for i, e in enumerate(etiquettes) if e.niveau == "pos"]
1065:        for k, i in enumerate(pos_idx):
1069:            avant = etiquettes[pos_idx[k - 1]]
1075:        # 3 a. après un pronom sujet, un mot inconnu est un verbe (« she sings ») ; l'exception
1078:        for _k, _i in enumerate(pos_idx):
1082:            _av = etiquettes[pos_idx[_k - 1]]
1083:            if (_av.type == "PRON" and _normaliser(_av.valeur) in SUJETS
1089:        # 3 b. un DET **ambigu** sans nom à sa droite n'est pas un DET (« the book that I
1091:        _lexd = POS_FERME.get(lg, POS_FERME["fr"])
1092:        for _k, _i in enumerate(pos_idx):
1098:            _suiv = etiquettes[pos_idx[_k + 1]] if _k + 1 < len(pos_idx) else None
1103:            _av = etiquettes[pos_idx[
… [457 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests/linguistique/ && python3 tools/tests/linguistique/gold_split.py --help 2>&1 | head -30", "description": "Inspect linguistic test tooling"}`

  ```
anaphore.py
classement_cible.py
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
replis_cible.py
test_bloc_linguistique.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 290, "limit": 130}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 590, "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
290:     "es": set("el la los las un una unos unas de del a al y o pero sino que quien como donde "
291:               "yo tú él ella nosotros vosotros ellos me te se le les mi tu su nuestro vuestro "
292:               "es son era eran ser haber he has ha han no nunca muy en con por para".split()),
293:     "it": set("il lo la i gli le un uno una di del della a al alla e o ma però che chi cui "
294:               "dove io tu lui lei noi voi loro mi ti si ci vi mio tuo suo nostro vostro è sono "
295:               "era erano essere avere ho hai ha hanno non mai molto in con per su tra fra".split()),
296:     "pt": set("o a os as um uma uns umas de do da dos das a ao aos à às e ou mas porém que quem "
297:               "como onde eu tu ele ela nós vós eles elas me te se lhe lhes meu tua seu nosso "
298:               "vosso é são era eram ser haver tenho tem têm não nunca muito em com por para".split()),
299:     "nl": set("de het een en of maar want dat die dit deze ik jij hij zij wij jullie zij mij "
300:               "jou hem haar ons hen mijn jouw zijn haar ons j
… [9957 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
590:                 morceau = texte[debut:fin]
591:             typ = "interrogative" if "?" in morceau else ("exclamative" if "!" in morceau else "déclarative")
592:             sortie.append((debut, fin, morceau, typ))
593:         return sortie
594: 
595:     @staticmethod
596:     def _negation(phrase: str) -> bool:
597:         return bool(re.search(r"\b(?:ne|n['’])\b.{0,40}\b(?:pas|plus|jamais|rien|guère)\b", phrase, re.I)
598:                     or re.search(r"\b(?:not|no|never|none|nothing|n't)\b", phrase, re.I))
599: 
600:     @staticmethod
601:     def _modalite(phrase: str) -> bool:
602:         return bool(re.search(r"\b(?:peut|peuvent|peux|pouvons|pouvez|doit|doivent|devons|devez|"
603:                               r"pourrait|pourraient|pourrais|devrait|devraient|voudrais|voudrait|"
604:                               r"faut|falloir|might|may|must|should|could|would|can)\b", phrase, re.I))
605: 
606:     # -- POS ----------------------------------------------------------------
607:     def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
60
… [3229 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 130, "offset": 1030}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1030: 
1031:         # 1. graphème — des plages de classes, pas un caractère par étiquette
1032:         classes = {"L": "lettres", "N": "chiffres", "P": "ponctuation", "Z": "espace",
1033:                    "S": "symbole", "M": "marque"}
1034:         i = 0
1035:         while i < len(texte):
1036:             cat = unicodedata.category(texte[i])[0]
1037:             j = i + 1
1038:             while j < len(texte) and unicodedata.category(texte[j])[0] == cat:
1039:                 j += 1
1040:             if cat in classes:
1041:                 etiquettes.append(Etiquette("graphème", classes[cat], texte[i:j], i, j,
1042:                                             self.nom, 0.99, langue=lg, script=script))
1043:             i = j
1044: 
1045:         # 2. mot + POS fermées / ouvertes
1046:         mots = self._mots(texte)
1047:         for d, f, t, typ in mots:
1048:             etiquettes.append(Etiquette("mot", typ, t, d, f, self.nom, 0.98, langue=lg, script=script))
1049:             if typ == "mot":
1050:                 classe, ouvert, conf = self._pos(lg, t)
… [7809 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"A25\\|R4\" reports/*.md reports/*.json docs/pilotage/*.md 2>/dev/null | head -30", "description": "Find A25/R4 references"}`

  ```
reports/INDEX.md
reports/inventaire-donnees-entrainement.md
reports/rapport-coherence-docs-2.md
reports/rapport-coherence-docs.md
reports/rapport-coherence-fiches-v7.md
reports/rapport-coherence-fiches-v8.md
reports/rapport-corpus-pdf.md
reports/rapport-echecs-v2.md
reports/rapport-file-taches.md
reports/rapport-matvec-f32-parallele.md
reports/rapport-miroir-blocs.md
reports/rapport-mode4-lot-listes.md
reports/rapport-ocr-cegep.md
reports/rapport-ocr-pdf.md
reports/rapport-ocr-pdf-restants.md
reports/rapport-passage-a-l-echelle.md
reports/rapport-pensee-attachement-v3.md
reports/rapport-pos-anglais.md
reports/rapport-pos-anglais-v2.md
reports/rapport-r01-graphe-document.md
reports/rapport-r04-tete-survol.md
reports/rapport-r07-routeur.md
reports/rapport-r41-bloc-tableaux.md
reports/rapport-r42-bloc-code.md
reports/rapport-r43-bloc-maths.md
reports/rapport-r44-ocr-pilote.md
reports/rapport-r44-scans.md
reports/rapport-session-2026-09-30.md
reports/rapport-spans-v7.md
reports/rapport-typoglycemie.md
  ```

- **bash** `{"command": "sed -n '1,120p' tools/tests/linguistique/evaluer_gold.py && echo ---- && sed -n '1,80p' tools/tests/linguistique/gold_split.py", "description": "Read evaluer_gold and split"}`

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
… [5657 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pos-anglais-v2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pos-anglais-v2.md</path>
<type>file</type>
<content>
1: # B13 — la POS passe à 83,83 % : la position du sujet tranche (R2a + R3 + R2b)
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
4: > **183/183 portes** : trois règles de la fiche [POS anglaise](rapport-pos-anglais.md) (A25) sont
5: > intégrées — **R2a** (après un pronom sujet, un mot inconnu est un verbe, sauf désinence
6: > nominale), **R3** (un DET ambigu sans nom à sa droite est un PRON/CONJ) et **R2b** (`-s`/`-es`
7: > après un nom sujet est un verbe). Résultat : **POS 75,81 → 83,83 %** (dev **83,75**, test
8: > **84,00**), **F1 syntagmes 0,5849 → 0,6181** (anglais **0,6341 → 0,7273**), et
9: > **l'attachement est strictement inchangé** : **222/222**, couverture **0,9289**.
10: >
11: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`analyser`, boucles
12: > 3 a/3 b/3 a bis), [`autotest.py`](../tools/pensee/autotest.py) (18 assertions recalées) ;
13: > fiche A25 [`rapport-pos-anglais.md`](rapport-pos-anglais.md) ; JSON
14: > [`pensee-pos-anglais-v2.json`](pensee-pos-anglais-v2.
… [3072 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py", "limit": 160, "offset": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py</path>
<type>file</type>
<content>
120:         bloc_langue = par_langue.get(langue, par_langue["fr"])
121:         for s in phrase["segments"]:
122:             cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
123:             if not cibles:
124:                 continue
125:             att_n += 1
126:             bloc_langue["cibles"] += 1
127:             e = labels.get((s["type"], s["debut"], s["fin"]))
128:             if e is None:
129:                 continue
130:             att_labels += 1
131:             bloc_langue["labels"] += 1
132:             att = (e.meta or {}).get("attachement") or {}
133:             cible = (att.get("cible") or "").strip()
134:             juste = cible == cibles[0]
135:             if juste:
136:                 att_exact += 1
137:                 bloc_langue["exact"] += 1
138:             # le gold admet parfois plusieurs cibles (43/96 GP) : mesure secondaire
139:             if cible in cibles:
140:                 att_exact_any += 1
141:             # le gold mêle deux conventions : la cible est un verbe (le gouverneur) ou un
… [8943 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-fiabilite-produit.json'))\nprint(type(p), list(p)[:20] if isinstance(p,dict) else len(p))\nPY", "description": "Inspect fiabilite JSON structure"}`

  ```
<class 'dict'> ['rapport', 'ligne', 'branche', 'commit_mesure', 'commit_module', 'date', 'objet', 'verdict', 'snapshot', 'dispositif', 'banc_50', 'robustesse', 'contrat', 'schema_propose', 'test_non_regression', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-fiabilite-produit.json'))\nfor k,v in p.items():\n    s=json.dumps(v,ensure_ascii=False)\n    print('==',k,'==',s[:600].replace('\\n',' '))\nPY", "description": "Dump top-level JSON keys"}`

  ```
== rapport == "fiabilite-produit"
== ligne == "B13"
== branche == "s/v7"
== commit_mesure == "56eb43af"
== commit_module == "1962eb15"
== date == "2026-11-06"
== objet == "Audit de fiabilité du produit hors gold : 50 phrases libres via la CLI, robustesse des entrées, contrat de sortie, schéma minimal versionné et test de non-régression."
== verdict == "⚠️ surface fiable (0 plantage, 0 JSON invalide, 0 span hors texte, 50/50 déterminisme) ; contrat non versionné et structure fragile (107 chevauchements, 302 tokens sans POS, 6/46 frontières de phrase cassées, refus sans JSON)."
== snapshot == {"drave_py_sha256": "59a06f3e4f7d633ae8caa30412fd4c01e14374914226f5e54629f544e47aea8c", "bloc_linguistique_sha256": "084517d9c10088b3adedc01658adbb33e3de69e7f5ca8c2f563f427abdd79f4f", "bloc_linguistique_git": "c1a08588", "module_change_pendant_audit": true, "note": "HEAD est passé de 6ef2a3f5 à 56eb43af pendant l'audit ; le module a reçu le correctif non-str/surrogate à 11 h 34 (c1a08588) ; le banc a tourné à 11 h 40, après ce correctif ; drave.py n'a pas changé (59a06f3e)."}
== dispositif == {"banc_50": "50 phrases écrites à la main (41 fr, 5 en, 4 refus, 1 très long), 4501 étiquettes, 1068 mot
… [5547 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"pensee-fiabilite-produit\" reports/*.md tools/*.py tools/**/*.py 2>/dev/null | head", "description": "Find producer of fiabilite JSON"}`

  ```
reports/rapport-fiabilite-produit.md
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-fiabilite-produit.json'))\nb=p['banc_50']\nprint(list(b))\nfor k,v in b.items():\n    if isinstance(v,list):\n        print(k, len(v), json.dumps(v[0], ensure_ascii=False)[:1200])\nPY", "description": "Inspect banc_50 entri … [4 caractères tronqués]`

  ```
['synthese', 'resultats']
resultats 50 {"id": "f01", "categorie": "fr", "attendu": "fr", "texte": "Le chat dort.", "caracteres": 13, "octets_utf8": 13, "rc": 0, "temps_cli_ms": 150.79, "temps_api_ms": 0.796, "deterministe": true, "json_octets": 5561, "json_valide": true, "langue": "fr", "script": "Latn", "labels": 19, "mots": 4, "pos": 3, "syntagmes": 2, "attaches": 2, "sans_attachement": 0, "chevauchements_syntagme": 0, "chevauchements_phrase_type": 0, "syntagmes_union": 0, "conflits_apres_filtre_union": 0, "cibles_fermees": 0, "cibles_absentes": 0, "phrases": 1, "phrases_espaces_initiaux": 0, "documents": 1, "doc_tronquees": 0, "doc_titres": [], "unites_semantiques": 2, "fraction_semantique": 0.6154, "trous_pos": {"mot": {"total": 3, "sans_pos": 0}, "ponctuation": {"total": 1, "sans_pos": 1}}, "sans_syntagme": false, "sans_pos": false}
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.
3: 
4: Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :
5: 
6:   - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
7:     **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
8:   - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
9:     substitution et le parallèle sans GPU ;
10:   - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
11:     même type d'annotation ;
12:   - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
13:     POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
14:   - `Parallele` et `Cascade` : les deux modes de composition. Le parallèle fusionne les
15:     étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
16:     que l'heuristique ne couvre pas.
… [2228 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Heuristique\\|class MockNeuronal\\|class Cascade\\|def analyser\\|def _est_verbe\\|RACINE\\|def _syntagmes_simple\\|attachement\" tools/bloc_linguistique.py | head -60", "description": "Locate classes and attachment logic"}`

  ```
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
139:    def analyser(self, texte: str, langue: str | None = None,
487:def _est_verbe(mot: str) -> bool:
531:class Heuristique:
651:            if str(RACINE / "tools/structures") not in sys.path:
652:                sys.path.insert(0, str(RACINE / "tools/structures"))
845:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
861:    def _syntagmes_simple(self, texte: str, langue: str,
1009:    def analyser(self, texte: str, langue: str | None = None,
1198:                        meta["attachement"] = {"segment": s.get("texte", ""), "cible": cible}
1226:                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
1253:                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
1321:class MockNeuronal:
1333:    def analyser(self, texte: str, langue: str | None = None,
1402:    def analyser(self, texte: str, langue: str | None = None,
1512:    def analyser(self, texte: str, langue: str | None = None,
1646:    def analyser(self, texte: str, langue: str | None = None,
1738:    def analyser(self, texte: str, langue: str | None = None,
1816:    def analys
… [378 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json, time\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nfrom tools. … [679 caractères tronqués]`

  ```
dev 0.8375 test 0.84 all 0.8383
ferme 0.9133 ouvert 0.7673
F1 0.6181 tete 0.7511
att 222 222 1.0 couv 0.9289
time 0.8029694557189941
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-pos-anglais.json'))\nprint(list(p))\nfor k,v in p.items():\n    s=json.dumps(v,ensure_ascii=False)\n    if 'R4' in s or 'copule' in s:\n        print('===',k)\n        p … [73 caractères tronqués]`

  ```
['version', 'date', 'ligne', 'objet', 'verdict', 'snapshot', 'gold', 'baseline', 'causes', 'hypotheses_refutees', 'regles', 'paquets', 'controles', 'limites', 'recommandation', 'reproduction']
=== causes
[{"id": "C1", "nom": "défaut nominal : le POS ouvert ne consulte pas le lexique verbal", "effectif": 176, "part": 0.652, "confiance_sortie": {"0.30": 172, "0.45": 4}, "formes": {"-s/-es": 126, "nues": 50, "-ing/-ed": 0}, "deja_dans_verbes_connus": 100, "precedees_d_un_sujet": 165, "precedees_par": {"PRON": 85, "NOUN": 80, "AUX": 6, "ADV": 2, "VERB": 2, "ADJ": 1}, "traitee_par": ["R1", "R2"]}, {"id": "C2", "nom": "classes fermées ambiguës : DET prioritaire sur PRON/CONJ", "effectif": 26, "part": 0.096, "detail": {"that": 23, "her": 3}, "traitee_par": ["R3"]}, {"id": "C3", "nom": "lexiques fermés anglais incomplets (+ règle de majuscule)", "effectif": 28, "part": 0.104, "detail": {"ADV": 16, "PRON": 9, "CONJ": 2, "AUX": 1}, "exemples": ["where 6", "late 4", "out 2", "as 2", "whose", "when", "mine", "outside", "am"], "via_majuscule": 3, "traitee_par": ["données"]}, {"id": "C4", "nom": "morphologie française appliquée à l'anglais", "effectif": 19, "part": 0.07, "detail": {"-able/-al->A
… [5688 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-pos-anglais-v2.json'))\nprint(list(p))\nfor k,v in p.items():\n    print('==',k,'==',json.dumps(v,ensure_ascii=False)[:400])\nPY", "description": "Inspect v2 JSON keys"}`

  ```
['date', 'ligne', 'portes', 'avant', 'apres', 'regles', 'rejetees', 'controles', 'limites']
== date == "2026-11-06"
== ligne == "B13"
== portes == "183/183"
== avant == {"pos": 0.7581, "pos_dev": 0.7547, "pos_test": 0.7656, "f1": 0.5849, "f1_en": 0.6341, "tete": 0.7336, "attachement": "222/222", "couverture": 0.9289}
== apres == {"pos": 0.8383, "pos_dev": 0.8375, "pos_test": 0.84, "f1": 0.6181, "f1_en": 0.7273, "tete": 0.7568, "attachement": "222/222", "couverture": 0.9289}
== regles == ["R2a pronom sujet → verbe", "R3 DET ambigu sans nom → PRON/CONJ", "R2b -s/-es après nom sujet"]
== rejetees == ["R1 lexique verbal (101/101 membres de VERBES_CONNUS écrits sur le gold)"]
== controles == {"placebo": "-2,46 à -4,18 pts", "corriges": 255, "casses": 0}
== limites == ["test 347 jetons", "R3 affiné après r117", "désinences en liste"]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -o '\"R4\"[^}]*}' reports/pensee-pos-anglais.json | head -5; grep -n \"R4\" reports/pensee-pos-anglais.json | head", "description": "Search R4 entry in v1 JSON"}`

  ```
473:    "R4 (piste)"
754:   "id": "R4",
1046:   "action": "pistes mesurées : R4 copule->ADJ, puis compléter les classes fermées anglaises (C3 : 28 erreurs)",
1047:   "gain": "R4 +0,70 pt test, 23 correctifs, 0 cassé",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-pos-anglais.json'))\nfor r in p['regles']:\n    if r['id'].startswith('R4'):\n        print(json.dumps(r,ensure_ascii=False,indent=1))\nPY", "description": "Dump R4 entr … [3 caractères tronqués]`

  ```
{
 "id": "R4",
 "nom": "copule -> ADJ pour un mot inconnu (piste)",
 "enonce": "après une copule, un mot inconnu (NOUN à confiance <= 0,45) est un ADJECTIF",
 "dev": {
  "pos": 0.762,
  "delta_pts": 0.73,
  "ferme": 0.8952,
  "ouvert": 0.6344,
  "f1": 0.582,
  "f1_tete": 0.7333,
  "attachement_exact": 0.9387,
  "attachement_topk": 0.9387
 },
 "test": {
  "pos": 0.7726,
  "delta_pts": 0.7,
  "ferme": 0.9119,
  "ouvert": 0.6441,
  "f1": 0.5914,
  "f1_tete": 0.7344,
  "attachement_exact": 0.9079,
  "attachement_topk": 0.8947
 },
 "en_union": 0.7753,
 "fr_union": 0.7597,
 "corriges": 23,
 "casses": 0,
 "corriges_en": 12,
 "corriges_fr": 11,
 "statut": "piste mesurée, non retenue dans les trois règles (périmètre)"
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nfrom tools.tests.linguistique.evaluer_gold import charger\nfrom tools.tests.linguistique.gold_split import dev, test\nph=charger … [234 caractères tronqués]`

  ```
612 3179
{'reel', 'hand', 'synthetique'}
dict_keys(['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source'])
{"id": "g001", "langue": "fr", "texte": "Le chat dort.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chat", "pos": "NOUN", "debut": 3, "fin": 7}, {"texte": "dort", "pos": "VERB", "debut": 8, "fin": 12}], "segments": [{"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}, {"type": "GV", "texte": "dort", "role": "prédicat", "debut": 8, "fin": 12}], "pragma": {"acte": "assertion"}, "source": "hand"}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nfrom tools.tests.linguistique.evaluer_gold import charger\nfrom tools.tests.linguistique.gold_split import _e … [671 caractères tronqués]`

  ```
### where
  r075  TEST gold=PRON  ctx=...'The city '[where]' we live is beautiful.'
  r115  TEST gold=PRON  ctx=...'The house '[where]' I was born is small.'
  r236  dev  gold=PRON  ctx=...'The village '[where]' I live is small.'
  r250  dev  gold=PRON  ctx=...'The place '[where]' we go is far.'
  r289  dev  gold=PRON  ctx=...'The place '[where]' we live is quiet.'
  r300  dev  gold=PRON  ctx=...'The house '[where]' she lives is small.'

### late
  r199  dev  gold=ADV   ctx=...'The train arrives '[late]'.'
  r218  dev  gold=ADV   ctx=...'Although it is '[late]', he works.'
  r313  dev  gold=ADV   ctx=...'I leave because it is '[late]'.'
  r365  dev  gold=ADV   ctx=...'train leaves; it arrives '[late]'.'

### out
  r035  dev  gold=ADV   ctx=...' film she talks about is '[out]'.'
  r284  TEST gold=ADV   ctx=...'though it rains, he goes '[out]'.'

### as

### As
  r249  dev  gold=CONJ  ctx=...''[As]' it was raining, we staye'
  r292  TEST gold=CONJ  ctx=...''[As]' she sang, he danced.'

### maybe
  r036  dev  gold=ADV   ctx=...'She is '[maybe]' tired.'

### Maybe
  r319  TEST gold=ADV   ctx=...''[Maybe]' he will come.'

### whose
  r239  TEST gold=PRON  ctx=...'The man '[whose]' car i
… [1190 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du gold et repérage des formes fermées manquantes

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport bloc_linguistique as bl\nfrom tools.tests.linguis … [1152 caractères tronqués]`

  ```
word gold->pred n in_lex
The        tot=129 wrong= 0 {('DET', 'DET'): 129} lex=['DET']
the        tot=57 wrong= 0 {('DET', 'DET'): 57} lex=['DET']
is         tot=44 wrong= 0 {('AUX', 'AUX'): 44} lex=['AUX']
it         tot=41 wrong= 0 {('PRON', 'PRON'): 41} lex=['PRON']
that       tot=23 wrong= 6 {('CONJ', 'CONJ'): 9, ('CONJ', 'PRON'): 3, ('PRON', 'PRON'): 8, ('PRON', 'DET'): 3} lex=['DET', 'PRON']
I          tot=21 wrong= 0 {('PRON', 'PRON'): 21} lex=['PRON']
she        tot=19 wrong= 0 {('PRON', 'PRON'): 19} lex=['PRON']
She        tot=18 wrong= 0 {('PRON', 'PRON'): 18} lex=['PRON']
he         tot=16 wrong= 0 {('PRON', 'PRON'): 16} lex=['PRON']
to         tot=15 wrong= 0 {('PREP', 'PREP'): 15} lex=['PREP']
we         tot=13 wrong= 0 {('PRON', 'PRON'): 13} lex=['PRON']
a          tot=12 wrong= 0 {('DET', 'DET'): 12} lex=['DET']
He         tot= 9 wrong= 0 {('PRON', 'PRON'): 9} lex=['PRON']
We         tot= 9 wrong= 0 {('PRON', 'PRON'): 9} lex=['PRON']
you        tot= 9 wrong= 0 {('PRON', 'PRON'): 9} lex=['PRON']
in         tot= 8 wrong= 0 {('PREP', 'PREP'): 8} lex=['PREP']
on         tot= 8 wrong= 0 {('PREP', 'PREP'): 8} lex=['PREP']
her        tot= 7 wrong= 0 {('DET', 'DET'): 4, ('PR
… [4001 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor w in ['am','is','seems','looks','fast','where','late','out','as','As','maybe','Maybe','whose','when','mine','outside',' … [469 caractères tronqués]`

  ```
am ('NOUN', True, 0.3)
is ('AUX', False, 0.92)
seems ('NOUN', True, 0.3)
looks ('VERB', True, 0.72)
fast ('NOUN', True, 0.3)
where ('NOUN', True, 0.3)
late ('NOUN', True, 0.3)
out ('NOUN', True, 0.3)
as ('NOUN', True, 0.3)
As ('NOUN', True, 0.55)
maybe ('NOUN', True, 0.3)
Maybe ('NOUN', True, 0.55)
whose ('NOUN', True, 0.3)
when ('CONJ', False, 0.92)
mine ('NOUN', True, 0.3)
outside ('PREP', False, 0.92)
again ('NOUN', True, 0.3)
now ('NOUN', True, 0.3)
down ('NOUN', True, 0.3)
n't ('NOUN', True, 0.3)
hard ('NOUN', True, 0.3)
far ('NOUN', True, 0.3)
am in VERBES False
False
Although I am tired, I continue.
[{'texte': 'Although', 'pos': 'CONJ', 'debut': 0, 'fin': 8}, {'texte': 'I', 'pos': 'PRON', 'debut': 9, 'fin': 10}, {'texte': 'am', 'pos': 'AUX', 'debut': 11, 'fin': 13}, {'texte': 'tired', 'pos': 'ADJ', 'debut': 14, 'fin': 19}, {'texte': 'I', 'pos': 'PRON', 'debut': 21, 'fin': 22}, {'texte': 'continue', 'pos': 'VERB', 'debut': 23, 'fin': 31}]
[('Although', 'CONJ', 0, 8), ('I', 'PRON', 9, 10), ('am', 'VERB', 11, 13), ('tired', 'VERB', 14, 19), ('I', 'PRON', 21, 22), ('continue', 'VERB', 23, 31)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-fiabilite-produit.json'))\nfor r in p['banc_50']['resultats']:\n    print(r['id'], r['categorie'], r['attendu'], 'langue=',r.get('langue'), 'rc=',r.get('rc'), 'pos=',r.g … [99 caractères tronqués]`

  ```
f01 fr fr langue= fr rc= 0 pos= 3 mots= 4 'Le chat dort.'
f02 fr fr langue= fr rc= 0 pos= 12 mots= 13 'Le chat de la voisine qui dort sur le toit se réveille.'
f03 fr fr langue= fr rc= 0 pos= 4 mots= 6 "Bonjour ! Comment allez-vous aujourd'hui ?"
f04 fr fr langue= fr rc= 0 pos= 7 mots= 9 "Ferme la porte, s'il te plaît."
f05 fr fr langue= fr rc= 0 pos= 5 mots= 6 'Ne touche pas à ça !'
f06 fr fr langue= fr rc= 0 pos= 11 mots= 13 "Je ne pense pas qu'il viendra demain, mais nous verrons bien."
f07 en en langue= en rc= 0 pos= 6 mots= 7 'The cat sleeps on the roof.'
f08 en en langue= en rc= 0 pos= 7 mots= 9 'Where is the nearest train station, please?'
f09 en en langue= en rc= 0 pos= 6 mots= 7 "Don't forget to bring your passport."
f10 fr fr langue= fr rc= 0 pos= 6 mots= 13 'Le prix est de 1 234,56 € pour 3 articles.'
f11 fr fr langue= fr rc= 0 pos= 3 mots= 10 'Rendez-vous le 12/03/2026 à 14h30.'
f12 fr fr langue= fr rc= 0 pos= 9 mots= 18 'Visitez https://example.com/docs?page=2 pour la documentation.'
f13 fr fr langue= und rc= 0 pos= 4 mots= 6 "J'ai trouvé ça génial 😍🔥"
f14 refus refus langue= None rc= 1 pos= None mots= None '🚀'
f15 refus refus langue= None rc= 1 pos= None mots= None ''
… [3340 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _normaliser\" -A15 tools/bloc_linguistique.py && sed -n '480,530p' tools/bloc_linguistique.py", "description": "Read normalizer and _est_verbe"}`

  ```
150:def _normaliser(texte: str) -> str:
151-    return unicodedata.normalize("NFC", texte).casefold()
152-
153-
154-def _trigrammes(texte: str) -> list[str]:
155-    t = _normaliser(texte)
156-    return [t[i:i + 3] for i in range(max(0, len(t) - 2))]
157-
158-
159-def _profil(texte: str, top: int = 200) -> dict[str, int]:
160-    c = collections.Counter(_trigrammes(texte))
161-    return dict(c.most_common(top))
162-
163-
164-def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
165-                         min_train: int = 5, min_test: int = 3,
def _sans_enclitique(mot: str) -> str:
    """`appelle-moi` → `appelle` (les enclitiques ne font pas partie de la tête)."""
    for suf in ENCLITIQUES:
        if mot.endswith(suf) and len(mot) > len(suf):
            return mot[: -len(suf)]
    return mot


def _est_verbe(mot: str) -> bool:
    """Le mot est-il un verbe ? Lexique + désinences courantes (fr/en)."""
    n = _normaliser(_sans_enclitique(mot))
    if not n:
        return False
    if n in VERBES_CONNUS:
        return True
    for suf in ("er", "ir", "e", "es", "ent", "ait", "aient", "é", "ée", "és", "i", "u",
                "ez", "ons", "iez", "ais",
… [1318 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfor w in ['reportée','coupées','calme','calmes','fatigué','fatiguée','intéressant','génial','ouverte','parti','médecin','tired','running','fast … [285 caractères tronqués]`

  ```
reportée       est_verbe=False pos_en=('NOUN', True, 0.3) pos_fr=('NOUN', True, 0.3)
coupées        est_verbe=False pos_en=('NOUN', True, 0.3) pos_fr=('NOUN', True, 0.3)
calme          est_verbe=False pos_en=('NOUN', True, 0.3) pos_fr=('NOUN', True, 0.3)
calmes         est_verbe=False pos_en=('NOUN', True, 0.3) pos_fr=('NOUN', True, 0.3)
fatigué        est_verbe=False pos_en=('NOUN', True, 0.3) pos_fr=('NOUN', True, 0.3)
fatiguée       est_verbe=False pos_en=('NOUN', True, 0.3) pos_fr=('NOUN', True, 0.3)
intéressant    est_verbe=False pos_en=('NOUN', True, 0.3) pos_fr=('ADJ', True, 0.68)
génial         est_verbe=False pos_en=('ADJ', True, 0.38) pos_fr=('ADJ', True, 0.38)
ouverte        est_verbe=True  pos_en=('NOUN', True, 0.3) pos_fr=('NOUN', True, 0.3)
parti          est_verbe=True  pos_en=('NOUN', True, 0.3) pos_fr=('NOUN', True, 0.3)
médecin        est_verbe=False pos_en=('NOUN', True, 0.3) pos_fr=('NOUN', True, 0.3)
tired          est_verbe=False pos_en=('VERB', True, 0.4) pos_fr=('VERB', True, 0.4)
running        est_verbe=True  pos_en=('VERB', True, 0.4) pos_fr=('VERB', True, 0.4)
fast           est_verbe=False pos_en=('NOUN', True, 0.3) pos_fr=('NOUN', True, 0.3)
late      
… [839 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Construction du harnais hors dépôt (copie en mémoire)

- **bash** `{"command": "mkdir -p /tmp/pos_r4 && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/pos_r4/harness.py <<'PY'\n\"\"\"Harnais local hors dépôt : copie en mémoire de bloc_linguistique.py + variantes R4/CC.\"\"\"\nfrom __future__ import annotations\nimport copy, json, pathlib, random,  … [4981 caractères tronqués]`

  ```
loaded 13 ('NOUN', True, 0.3)
r4 ('NOUN', True, 0.3)
[('She', 'PRON'), ('is', 'AUX'), ('calm', 'ADJ')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, time\nsys.path.insert(0,'/tmp/pos_r4')\nimport harness as H\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nfrom tools.tests.linguistique.gold_split import dev, test\n\nph=charg … [1530 caractères tronqués]`

  ```
BASE 0.8383 0.9133 0.7673 0.6198 226 226 0.8375 0.84
r4_en POS 0.8421 dev 0.8416 test 0.8431 delta dev 0.41 test 0.31 F1 0.6198 att 226 226 ferme 0.9133 ouvert 0.7746
r4_fr POS 0.8418 dev 0.8407 test 0.8441 delta dev 0.32 test 0.41 F1 0.6198 att 226 226 ferme 0.9133 ouvert 0.774
r4_bilingue POS 0.8455 dev 0.8449 test 0.8471 delta dev 0.74 test 0.71 F1 0.6198 att 226 226 ferme 0.9133 ouvert 0.7814
r4_bilingue_guard POS 0.8452 dev 0.8449 test 0.8461 delta dev 0.74 test 0.61 F1 0.6198 att 226 226 ferme 0.9133 ouvert 0.7808
r4_en_large POS 0.8418 dev 0.8412 test 0.8431 delta dev 0.37 test 0.31 F1 0.6198 att 226 226 ferme 0.9133 ouvert 0.774
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'/tmp/pos_r4'); sys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport harness as H\nimport bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gol … [913 caractères tronqués]`

  ```
import 0.6198 226 226 239
exec 0.6198 226 226 239
files /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
racine /home/stephane/Data13TB/stephane/GitHub/Qtrinet /home/stephane/Data13TB/stephane/GitHub/Qtrinet
init sig (None, True, 0.55, 0.12, True)
h1 segmenter_s True h2 True
g001 True {('GV', 8, 12), ('GN', 0, 7)} {('GV', 8, 12), ('GN', 0, 7)}
g002 True {('GV', 22, 26), ('GP', 8, 26), ('GP', 8, 21), ('GN', 0, 7)} {('GV', 22, 26), ('GP', 8, 26), ('GP', 8, 21), ('GN', 0, 7)}
g003 True {('GV', 9, 13), ('GP', 22, 34), ('GV', 9, 21), ('GN', 0, 8), ('GN', 14, 21)} {('GV', 9, 13), ('GP', 22, 34), ('GV', 9, 21), ('GN', 0, 8), ('GN', 14, 21)}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum tools/bloc_linguistique.py && git log --oneline -5 -- tools/bloc_linguistique.py && git diff HEAD --stat -- tools/bloc_linguistique.py && git status --short tools/bloc_linguistique.py tools/structures && git -C tools/struct … [84 caractères tronqués]`

  ```
c4d8f09b6038fb26829517d62b9ea421dff43452bea2e20fc944a5dcff0544dd  tools/bloc_linguistique.py
e6fad714 POS — DEUX AJOUTS DE LEXIQUE GÉNÉRAUX (acheter, élision qu'il) ; 183/183
037fe041 PRODUIT — LE CONTRAT V1 : schema/version, REFUS EN JSON (CODE 3), SURROGATE ET NON-STR TOLÉRÉS ; PORTE À 8 CONTRÔLES ; 183/183
2ba393b0 B13 — LA POS À 83,83 % (R2a/R3/R2b) : F1 0,5849 → 0,6181, ANGLAIS 0,6341 → 0,7273, ATTACHEMENT INCHANGÉ (222/222) ; 183/183
1962eb15 PRODUIT — LA ROBUSTESSE : SURROGATE ET NON-STR FERMÉS (refus non_texte), 8 TESTS ; L'AUDIT A24 (50 PHRASES, 132 CHEVAUCHEMENTS, 18 CORRECTIFS)
0911ae29 B13 — 222/222 (1,0000) : LE DERNIER MARQUEUR AMBIGU (when APRÈS UN GN), COUVERTURE 0,9289, 17 SPANS TOUS INATTEIGNABLES ; 183/183
 m tools/structures
 M donnees/paragraphes-validations.jsonl
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline e6fad714 && git show e6fad714 -- tools/bloc_linguistique.py | head -80 && git log -1 --format='%H %s'", "description": "Inspect latest POS commit"}`

  ```
e6fad714 POS — DEUX AJOUTS DE LEXIQUE GÉNÉRAUX (acheter, élision qu'il) ; 183/183
 journal/2026-11-06/README.md                       |  13 +-
 journal/2026-11-06/distribue.md                    |   8 +-
 journal/2026-11-06/docs.md                         |   8 +-
 journal/2026-11-06/mesures.md                      |   8 +-
 journal/2026-11-06/modele.md                       |   8 +-
 journal/2026-11-06/outils.md                       |   8 +-
 journal/2026-11-06/portes.md                       |  11 +-
 journal/README.md                                  |   8 +-
 .../338f8b55-bcd5-464a-a63e-b97381eff55d/digest.md | 129 ++++++++
 .../rapport.md                                     |  19 +-
 .../3ccd8d09-9820-4da4-963b-6d84a0ffb141/digest.md | 270 ++++++++++++++++
 .../rapport.md                                     |  28 +-
 journal/sessions/MANIFEST.md                       |  10 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 107 +++++++
 .../rapport.md                                     |  20 +-
 .../eedb7a58-2a33-4caa-8509-f46d9e328080/digest.md | 353 +++++++++++++++++++++
 .../rapport.md                                     |  29 +-
 tools/bloc_linguistique.py          
… [1782 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 2ba393b0:tools/bloc_linguistique.py > /tmp/pos_r4/bloc_b13.py && sha256sum /tmp/pos_r4/bloc_b13.py && grep -n \"# 4. phrase + pragmatique\" /tmp/pos_r4/bloc_b13.py && git diff 2ba393b0 -- tools/tests/linguistique/gold.json t … [156 caractères tronqués]`

  ```
f3db75fcaf0ced187c8ddc204e2b8509f34e080c3b81021b1e7ca66327afcc87  /tmp/pos_r4/bloc_b13.py
1114:        # 4. phrase + pragmatique
diff --git a/tools/tests/linguistique/gold_synthetique.json b/tools/tests/linguistique/gold_synthetique.json
index 4307946c..079562ee 100644
--- a/tools/tests/linguistique/gold_synthetique.json
+++ b/tools/tests/linguistique/gold_synthetique.json
@@ -1577,9 +1577,9 @@
     },
     {
      "type": "GP",
-     "texte": "il",
+     "texte": "avec il",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat >> /tmp/pos_r4/harness.py <<'PY'\n\ndef load_source(src, r4=False, name='bl_src', file_path=None):\n    if r4:\n        assert src.count(R4_ANCHOR) == 1, src.count(R4_ANCHOR)\n        src = src.replace(R4_ANCHOR, R4_BLOCK + R4_AN … [1078 caractères tronqués]`

  ```
all 0.8383 0.9133 0.7673 0.6204 226 226 239 0.9456
dev 0.8375 0.9093 0.7688 0.617 155 155 163 0.9509
test 0.84 0.9224 0.764 0.628 71 71 76 0.9342
  ```

