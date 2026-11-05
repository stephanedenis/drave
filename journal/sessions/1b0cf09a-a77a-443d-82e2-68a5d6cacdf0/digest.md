# Session DSH — relecture

- identifiant : `1b0cf09a-a77a-443d-82e2-68a5d6cacdf0`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 14:22:47
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **valider le cache du chunker** proposé par la fiche `reports/rapport-cout-chunker.md` (O(n²) confirmé, cache ×11,6 à 160 tokens) — sans modifier le code du dépôt.

Contexte : `tools/bloc_linguistique.py`, classe `Heuristique` : `analyser` appelle `self._syntagmes_simple(texte, lg)` à l'intérieur de la boucle sur les segments (chemin chunker) et dans `_cible_proche`/`_verbes_proches`. La fiche décrit le correctif (calculer les GV une fois, mémoïser `_syntagmes_simple` par texte).

À faire :
1. Implémente le cache **dans un sous-classe** de `Heuristique` (ou par monkeypatch local, sans modifier le fichier) : mémoïse `_syntagmes_simple(texte, langue)` par couple (texte, langue) sur la durée d'une analyse.
2. Mesure : temps sur les 612 phrases et sur des phrases de 20 à 1 280 tokens, comparaison avec `Heuristique()` non cachée ; **égalité stricte** des annotations (étiquettes, spans, cibles, candidats) entre version cachée et version normale sur les 612.
3. Mesure aussi le chemin par défaut (générateur S) et dis si le cache y change quelque chose.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-cache-chunker.md` (fiche : protocole, tableau temps, complexité, égalité des annotations, contrôles négatifs, limites, correctif proposé avec les lignes) et `reports/pensee-cache-chunker.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : facteur de gain, égalité oui/non, et le correctif exact à appliquer.
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

⏵ Exploration du dépôt et de la fiche de coût du chunker

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && git branch --show-current && ls", "description": "Check repo status and branch"}`

  ```
M docs/pilotage/en-cours.md
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/rapport.md
D  journal/sessions/65495a29-10c0-4571-96be-e7729f1efebf/digest.md
D  journal/sessions/65495a29-10c0-4571-96be-e7729f1efebf/rapport.md
MM journal/sessions/MANIFEST.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/digest.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/rappo
… [1854 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | head -50 && echo '---' && wc -l tools/bloc_linguistique.py reports/rapport-cout-chunker.md 2>/dev/null", "description": "List reports and file sizes"}`

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
---
  1929 tools/bloc_linguistique.py
   388 reports/rapport-cout-chunker.md
  2317 total
[stderr]
ls: write error: Broken pipe
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md</path>
<type>file</type>
<content>
1: # Coût des règles d'attachement du chunker — O(n²) réel, cache ×12 à 160 tokens
2: 
3: > **Date** : 2026-11-05 · **Instantané** : [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py)
4: > sha256 `6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65`, commit
5: > `9d5337ce` (branche `s/v7` ; le fichier mesuré y est committé ; il était encore modifié
6: > dans l'arbre au moment du banc) · **Verdict** : ✅ **le O(n²) est confirmé** ; le cache « un chunking + un verbe de GV par analyse » divise le temps par
7: > **11,6 à 160 tokens** et **16,9 à 320** sur le chemin chunker seul, par **2,0 / 2,4** sur le
8: > chemin par défaut ; **mais** il ne rend pas la complexité strictement linéaire (le tri des GV
9: > par segment reste) et il ne gagne presque rien sur le corpus court.
10: >
11: > **Dispositif** : banc hors dépôt (`/tmp/bench_final.py`, sha256 `6c823a1f…`), 612 phrases de
12: > [`evaluer_gold.charger()`](../tools/tests/linguistique/evaluer_gold.py), phrases synthétiques
13: > de 20 à 1 280 tokens, variantes V1/V2/OFF ; JSON
14: > [`pensee-co
… [24176 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum tools/bloc_linguistique.py && git diff --stat -- tools/bloc_linguistique.py && git log --oneline -3", "description": "Hash and diff of the linguistic block"}`

  ```
6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65  tools/bloc_linguistique.py
2e08cbc7 B13 — LA VAGUE 1 COMPLÈTE : CONTRAT S, COÛT DU CHUNKER, COHÉRENCE DES FICHES ; 3 DIVERGENCES CORRIGÉES
9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
e1171032 PILOTAGE — PROTOCOLE D'INTÉGRATION DES SOUS-AGENTS (REJOUER, REJETER, COMMITTER VÉRIFIÉ) ; § 9
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"_syntagmes_simple\\|def analyser\\|def _cible_proche\\|def _verbes_proches\\|def _verbe_dans\\|def _syntagmes_s\\b\" tools/bloc_linguistique.py", "description": "Locate key functions in the source"}`

  ```
133:    def analyser(self, texte: str, langue: str | None = None,
591:    def _syntagmes_s(self, texte: str) -> list[dict] | None:
642:    def _verbe_dans(texte: str, debut: int, fin: int,
661:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
688:    def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
725:    def _syntagmes_simple(self, texte: str, langue: str) -> list[dict]:
783:    def analyser(self, texte: str, langue: str | None = None,
861:            gvs_simple = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
914:            for s in self._syntagmes_simple(texte, lg):
916:                cible = self._cible_proche(texte, s, [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"], verbes)
919:                gvs_s = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
928:            simples = self._syntagmes_simple(texte, lg)
1013:    def analyser(self, texte: str, langue: str | None = None,
1041:        for s in h._syntagmes_simple(texte, lg):
1082:    def analyser(self, texte: str, langue: str | None = None,
1192:    def analyser(self, texte: str, langue: str | None = None,
1326:    def analyser(sel
… [309 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 560, "limit": 420}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
560:             return "ADJ", True, 0.68
561:         if re.fullmatch(r"\d+(?:[.,]\d+)*", mot):
562:             return "NUM", False, 0.95
563:         if mot[:1].isupper() and mot[1:].islower() and mot not in {"Le", "La", "Les", "Un", "Une", "The"}:
564:             return "NOUN", True, 0.55
565:         if len(n) >= 4 and n.endswith(("ment", "ly")):
566:             return "ADV", True, 0.45
567:         if len(n) >= 4 and n.endswith(("tion", "sion", "ness", "ity", "ité", "ance", "ence")):
568:             return "NOUN", True, 0.45
569:         if len(n) >= 4 and n.endswith(("er", "ir", "ing", "ed")):
570:             return "VERB", True, 0.4
571:         if len(n) >= 4 and n.endswith(("eux", "euse", "able", "ible", "ous", "ive", "al")):
572:             return "ADJ", True, 0.38
573:         return ("NOUN" if (n and n[0].islower()) else "MOT"), True, 0.3
574: 
575:     # -- morphèmes ----------------------------------------------------------
576:     @staticmethod
577:     def _morphemes(mot: str) -> list[tuple[str, int, int, str]]:
578:         n = _normaliser(mot)
… [24388 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' tools/bloc_linguistique.py", "description": "Read top of linguistic block"}`

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
… [4701 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '979,1120p' tools/bloc_linguistique.py", "description": "Read rest of analyser and next classes"}`

  ```
"unites_semantiques": len(unites), "fraction": round(fraction, 4)})
        return Annotation(texte=texte, langue=lg, script=script, etiquettes=etiquettes,
                          trace=trace, source=self.nom, unites_semantiques=unites,
                          fraction_semantique=round(fraction, 4), contexte=contexte or "",
                          cout={"octets": len(texte.encode()), "caracteres": len(texte),
                                "etiquettes": len(etiquettes), "duree_s": round(time.perf_counter() - t0, 6)})


def _fusionner(spans: Sequence[Span]) -> list[Span]:
    spans = sorted(set(spans), key=lambda s: (s.debut, s.fin))
    sortie: list[Span] = []
    for s in spans:
        if not sortie or s.debut > sortie[-1].fin:
            sortie.append(s)
        else:
            sortie[-1] = Span(sortie[-1].debut, max(sortie[-1].fin, s.fin))
    return sortie


# --------------------------------------------------------------------------- neuronal


class MockNeuronal:
    """Le neuronal **de contrat** : même sortie, source `neuronal`, déterministe, sans GPU.

    Il ne prétend pas être un modèle : il prouve que le contrat accepte une autre implémentation,
    que le par
… [6348 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Heuristique\" -A 40 tools/bloc_linguistique.py | head -60", "description": "Read Heuristique class init"}`

  ```
475:class Heuristique:
476-    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
477-
478-    nom = "heuristique"
479-
480-    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
481-                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
482-                 union: bool = True):
483-        self.profils = profils
484-        self.segmenter_s = segmenter_s
485-        self.seuil_ouvert = seuil_ouvert
486-        self.seuil_langue = seuil_langue
487-        self.union = union
488-
489-    # -- langues / script ---------------------------------------------------
490-    def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
491-        langue, conf, _ = detecter_langue(texte, self.profils, indice)
492-        script = detecter_script(texte)
493-        if conf < self.seuil_langue:
494-            return "und", conf, script
495-        return langue, conf, script
496-
497-    # -- tokens -------------------------------------------------------------
498-    @staticmethod
499-    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
500-        motif = re.compile(r"\
… [686 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/tests/linguistique/ && sed -n '1,120p' tools/tests/linguistique/evaluer_gold.py", "description": "Inspect gold evaluation corpus loader"}`

  ```
anaphore.py
classement_cible.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel.json
gold_reel.py
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
test_bloc_linguistique.py
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
    h
… [4032 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0, 'tools/tests/linguistique')\nsys.path.insert(0, 'tools')\nimport evaluer_gold as eg\nph = eg.charger()\nprint('n phrases', len(ph))\nprint('sources', collections.Counter( … [295 caractères tronqués]`

  ```
n phrases 612
sources Counter({'reel': 432, 'synthetique': 160, 'hand': 20})
langues Counter({'fr': 402, 'en': 210})
mots 3179
caracteres 16371
exemple Le chat dort.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/pensee-cout-chunker.json | head -80 && echo '----' && ls reports/pensee-*.json | head", "description": "Inspect pensee JSON schema"}`

  ```
{
    "date": "2026-11-05T13:58:19-0500",
    "titre": "Co\u00fbt des r\u00e8gles d'attachement du chunker",
    "verdict": "O(n\u00b2) confirm\u00e9 sur le chemin chunker seul : 1+2S appels \u00e0 _syntagmes_simple (3,21/phrase sur le gold, 97 \u00e0 160 tokens, 193 \u00e0 320) ; temps \u00d73,7 par doublement 160\u2192320. Le cache mesur\u00e9 (un chunking + un verbe de GV par analyse) donne \u00d711,6 \u00e0 160 et \u00d716,9 \u00e0 320 sur ce chemin, \u00d72,0 et \u00d72,4 sur le chemin par d\u00e9faut. Le chemin par d\u00e9faut n'appelle _syntagmes_simple que 2 fois/phrase : le re-chunking y est du code mort ; son co\u00fbt quadratique vient de _verbe_dans (2 320 appels pour 32 GV distincts \u00e0 160 ; 8 736 pour 64 \u00e0 320), ramen\u00e9s aux GV distincts par le cache. Le tri sorted(gvs, key=ecart) par segment reste : le cache ne rend pas la complexit\u00e9 strictement lin\u00e9aire (pente V2 1,44-1,55 sur 160-1280). Sur le corpus court : \u00d71,18-1,22 (chunker) et \u00d70,97-1,07 (d\u00e9faut).",
    "instantane": {
        "fichier": "tools/bloc_linguistique.py",
        "sha256": "6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65",
        "sha256_apres
… [3447 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections\np = json.load(open('reports/pensee-cout-chunker.json'))\nprint(type(p), list(p)[:20] if isinstance(p, dict) else len(p))\nEOF", "description": "Top-level structure of pensee file"}`

  ```
<class 'dict'> ['date', 'titre', 'verdict', 'instantane', 'dispositif', 'corpus', 'longueurs', 'complexite', 'continuite', 'profils_n160', 'controle_negatif', 'correctif_propose', 'sensibilite_base_verbe_plein', 'pistes_rejetees', 'limites']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np = json.load(open('reports/pensee-cout-chunker.json'))\nfor k in ['longueurs','complexite','controle_negatif','correctif_propose']:\n    print('=====', k)\n    print(json.dumps(p[k], ensure_ascii=Fals … [81 caractères tronqués]`

  ```
===== longueurs
{
 "base": "Le chat de la voisine est sur le toit.",
 "base_tokens": 10,
 "note": "base de 10 tokens répétée 2/4/8/16/32 fois ; N exact en tokens _mots",
 "points": [
  {
   "chemin": "chunker",
   "N": 20,
   "chars": 77,
   "segments_simple": 6,
   "gv_simple": 2,
   "segments_s": 0,
   "gv_s": 0,
   "etiquettes": 87,
   "temps_ms": {
    "original": 1.747,
    "V1": 0.933,
    "V2": 0.727,
    "OFF": 1.751
   },
   "gains": {
    "V1": 1.873,
    "V2": 2.402,
    "OFF": 0.998
   },
   "appels_origine": {
    "simple": 13,
    "verbe": 20
   },
   "appels_v2": {
    "appels_simple": 13,
    "miss_simple": 1,
    "appels_gv": 20,
    "miss_gv": 2
   },
   "egalite": {
    "V1": "1/1",
    "V2": "1/1",
    "OFF": "1/1"
   }
  },
  {
   "chemin": "chunker",
   "N": 40,
   "chars": 155,
   "segments_simple": 12,
   "gv_simple": 4,
   "segments_s": 0,
   "gv_s": 0,
   "etiquettes": 173,
   "temps_ms": {
    "original": 5.038,
    "V1": 1.95,
    "V2": 1.315,
    "OFF": 5.582
   },
   "gains": {
    "V1": 2.583,
    "V2": 3.832,
    "OFF": 0.902
   },
   "appels_origine": {
    "simple": 25,
    "verbe": 64
   },
   "appels_v2": {
    "appels_simple": 25,
    "miss_simp
… [6970 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np = json.load(open('reports/pensee-cout-chunker.json'))\nfor pt in p['longueurs']['points']:\n    if pt['chemin'] == 'defaut':\n        print(json.dumps(pt, ensure_ascii=False))\nEOF", "description": " … [34 caractères tronqués]`

  ```
{"chemin": "defaut", "N": 20, "chars": 77, "segments_simple": 6, "gv_simple": 2, "segments_s": 8, "gv_s": 2, "etiquettes": 91, "temps_ms": {"original": 1.984, "V1": 1.92, "V2": 1.577, "OFF": 1.994}, "gains": {"V1": 1.033, "V2": 1.258, "OFF": 0.995}, "appels_origine": {"simple": 2, "verbe": 66}, "appels_v2": {"appels_simple": 2, "miss_simple": 1, "appels_gv": 63, "miss_gv": 4}, "egalite": {"V1": "1/1", "V2": "1/1", "OFF": "1/1"}}
{"chemin": "defaut", "N": 40, "chars": 155, "segments_simple": 12, "gv_simple": 4, "segments_s": 16, "gv_s": 4, "etiquettes": 181, "temps_ms": {"original": 4.232, "V1": 4.102, "V2": 2.993, "OFF": 4.193}, "gains": {"V1": 1.032, "V2": 1.414, "OFF": 1.009}, "appels_origine": {"simple": 2, "verbe": 196}, "appels_v2": {"appels_simple": 2, "miss_simple": 1, "appels_gv": 189, "miss_gv": 8}, "egalite": {"V1": "1/1", "V2": "1/1", "OFF": "1/1"}}
{"chemin": "defaut", "N": 80, "chars": 311, "segments_simple": 24, "gv_simple": 8, "segments_s": 32, "gv_s": 8, "etiquettes": 361, "temps_ms": {"original": 9.886, "V1": 9.623, "V2": 6.08, "OFF": 9.824}, "gains": {"V1": 1.027, "V2": 1.626, "OFF": 1.006}, "appels_origine": {"simple": 2, "verbe": 648}, "appels_v2": {"appels_simp
… [1014 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%dT%H:%M:%S%z' && python3 --version && nproc && lscpu | grep -E 'Model name|Socket|Core|Thread' | head -5", "description": "Environment and CPU information"}`

  ```
2026-11-05T14:26:24-0500
Python 3.13.16
40
Model name:                              Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz
Thread(s) per core:                      2
Core(s) per socket:                      10
Socket(s):                               2
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '120,220p' tools/tests/linguistique/evaluer_gold.py", "description": "Read gold evaluation attachment logic"}`

  ```
att_n += 1
            e = labels.get((s["type"], s["debut"], s["fin"]))
            if e is None:
                continue
            att_labels += 1
            att = (e.meta or {}).get("attachement") or {}
            cible = (att.get("cible") or "").strip()
            juste = cible == cibles[0]
            if juste:
                att_exact += 1
            # le gold mêle deux conventions : la cible est un verbe (le gouverneur) ou un nom
            # (l'antécédent d'un REL, la tête d'un GP). On mesure les deux séparément — en
            # suivant le **POS du gold** (plus fiable que le lexique : « poussent », « aboie »
            # y sont VERB), avec `_est_verbe` en repli si la cible n'est pas un token.
            pos_cible = next((m["pos"] for m in phrase.get("mots", [])
                              if phrase["texte"][m["debut"]:m["fin"]] == cibles[0]), None)
            if (pos_cible == "VERB") if pos_cible else bl._est_verbe(cibles[0]):
                att_v_n += 1
                att_v_ok += int(juste)
            else:
                att_n_n += 1
                att_n_ok += int(juste)
            if cible and any(c in cible or cible in c for c in cibles):
         
… [4617 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture du banc de mesure hors dépôt (cache par sous-classe)

- **write** `{"file_path": "/tmp/bench_cache_chunker.py", "content": "#!/usr/bin/env python3\n\"\"\"Banc de validation du cache du chunker — HORS DÉPÔT.\n\nSous-classe locale de `Heuristique` :\n  - C1  : `_syntagmes_simple` mémoïsé par (texte, langue) sur la durée d'une analyse ;\n  - C2  : C1 + le verbe de cha … [18457 caractères tronqués]`

  ```
<path>/tmp/bench_cache_chunker.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp && python3 -m py_compile bench_cache_chunker.py && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0, '/tmp')\nimport bench_cache_chunker as b\n\nph = b.eg.charger()[:30]\nfor seg in (False, True):\n    ref = b.bl.Heuristique(segmenter_s=seg).analyser(ph[0]['texte'], ph[0][ … [542 caractères tronqués]`

  ```
False C1 egal True n_etq 18
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
  File "/tmp/bench_cache_chunker.py", line 84, in analyser
    return super().analyser(texte, langue, contexte)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/bench_cache_chunker.py", line 49, in analyser
    return super().analyser(texte, langue, contexte)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", line 933, in analyser
    cible = self._cible_proche(texte, s, gvs_s, verbes, cache_gv)
TypeError: C2._cible_proche() takes from 4 to 5 positional arguments but 6 were given
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum tools/bloc_linguistique.py && git status --short -- tools/bloc_linguistique.py && sed -n '850,945p' tools/bloc_linguistique.py", "description": "Re-check current source around analyser"}`

  ```
e568c9fbb4e71b02b1f3cea26e07bea921b06152e0a9cd64507abf4813dca445  tools/bloc_linguistique.py
 M tools/bloc_linguistique.py
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
                                            self.nom, 0.25, candidats=["littéral", "figuré"],
                             
… [5466 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- tools/bloc_linguistique.py && git diff -- tools/bloc_linguistique.py | head -120 && echo '=== HEAD hash ===' && git show HEAD:tools/bloc_linguistique.py | sha256sum", "description": "Inspect concurrent modification … [25 caractères tronqués]`

  ```
tools/bloc_linguistique.py | 35 ++++++++++++++++++++++++++---------
 1 file changed, 26 insertions(+), 9 deletions(-)
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 5cc3858f..ba126afc 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -657,9 +657,21 @@ class Heuristique:
                     return v
         return None if strict else (mots[-1][1] if mots else None)
 
+    @staticmethod
+    def _verbe_gv(texte: str, g: dict, verbes, cache: dict | None = None):
+        """`_verbe_dans` mémoïsé par span de GV : le même GV est relu pour chaque segment."""
+        cle = (g["debut"], g["fin"])
+        if cache is not None and cle in cache:
+            return cache[cle]
+        v = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
+        if cache is not None:
+            cache[cle] = v
+        return v
+
     @staticmethod
     def _cible_proche(texte: str, segment: dict, gvs: list[dict],
-                      verbes: list[tuple[int, int, str]] | None = None) -> str | None:
+                      verbes: list[tuple[int, int, str]] | None = None,
+                      cache: dict | None = None) -> str | None:
   
… [3528 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"RACINE\" tools/bloc_linguistique.py && echo '--- generateur paths ---' && grep -n \"RACINE\\|__file__\\|pathlib\" tools/structures/generateur.py | head -30", "description": "Check RACINE usage and generator path deps"}`

  ```
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
595:            if str(RACINE / "tools/structures") not in sys.path:
596:                sys.path.insert(0, str(RACINE / "tools/structures"))
1917:    ap.add_argument("--modele", default=str(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf"))
1922:    ap.add_argument("--udhr", default=str(RACINE / "data/udhr/articles.jsonl"))
--- generateur paths ---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- tools/bloc_linguistique.py | sed -n '120,220p'", "description": "Read remainder of concurrent patch"}`

  ```
(no output)
  ```

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Alerte drift : `tools/bloc_linguistique.py` a été modifié dans l'arbre pendant ma validation (sha 6e8430… → e568c9…, +26/−9). Le diff ajoute `_verbe_gv` + un cache local, mais **seulement dans la branche `else`** (chunker seul) ; la br … [464 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD:tools/bloc_linguistique.py > /tmp/bloc_linguistique_snapshot.py && sha256sum /tmp/bloc_linguistique_snapshot.py && git rev-parse HEAD", "description": "Freeze HEAD snapshot of the block"}`

  ```
6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65  /tmp/bloc_linguistique_snapshot.py
de292c7d680d5c1b09edc240e03c8dbdcf21cb91
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -4 && echo '---' && git status --short -- tools/bloc_linguistique.py && sha256sum tools/bloc_linguistique.py && git show HEAD:tools/bloc_linguistique.py | sha256sum", "description": "Check new commit and file state" … [1 caractères tronqués]`

  ```
de292c7d ÉTAT — B13 180/180, T0 DANS LE BUDGET ; VAGUE 3 LANCÉE (AUDIT V2, ÉCHECS, REPLIS, CACHE)
2e08cbc7 B13 — LA VAGUE 1 COMPLÈTE : CONTRAT S, COÛT DU CHUNKER, COHÉRENCE DES FICHES ; 3 DIVERGENCES CORRIGÉES
9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
e1171032 PILOTAGE — PROTOCOLE D'INTÉGRATION DES SOUS-AGENTS (REJOUER, REJETER, COMMITTER VÉRIFIÉ) ; § 9
---
 M tools/bloc_linguistique.py
e568c9fbb4e71b02b1f3cea26e07bea921b06152e0a9cd64507abf4813dca445  tools/bloc_linguistique.py
6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65  -
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nfrom pathlib import Path\np = Path('/tmp/bench_cache_chunker.py')\ns = p.read_text()\ns = s.replace('''import json\nimport math\nimport pathlib\nimport platform\nimport statistics\nimport subprocess\nimport sys\nimport time\nfrom collections import Counter\ … [4010 caractères tronqués]`

  ```
ok
32:spec = importlib.util.spec_from_file_location("bloc_snapshot", SNAPSHOT)
34:sys.modules["bloc_snapshot"] = bl
40:SHA_SNAPSHOT = hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest()
41:SHA_ARBRE_DEBUT = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
409:            "sha256": SHA_SNAPSHOT,
410:            "sha256_fichier_git": SHA_SNAPSHOT,
411:            "sha256_arbre_debut": SHA_ARBRE_DEBUT,
412:            "sha256_arbre_fin": sha_arbre_fin,
413:            "arbre_modifie_pendant_banc": SHA_ARBRE_DEBUT != sha_arbre_fin,
437:        "sha256_apres": SHA_SNAPSHOT,
461:        "sha256": SHA_SNAPSHOT,
462:        "sha256_arbre_debut": SHA_ARBRE_DEBUT,
463:        "sha256_arbre_fin": sha_arbre_fin,
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport sys\nsys.path.insert(0, '/tmp')\nimport bench_cache_chunker as b\nph = b.eg.charger()[:40]\nprint('snapshot', b.SHA_SNAPSHOT, 'arbre', b.SHA_ARBRE_DEBUT)\nfor seg in (False, True):\n    for arm in ('C1','C2','OFF'):\n        ok = 0\n        for p in  … [593 caractères tronqués]`

  ```
snapshot 6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65 arbre e568c9fbb4e71b02b1f3cea26e07bea921b06152e0a9cd64507abf4813dca445
False C1 40 / 40
False C2 40 / 40
False OFF 40 / 40
True C1 40 / 40
True C2 40 / 40
True OFF 40 / 40
falsifie egal ? False ['cout', 'etiquettes(44!=43)', 'trace']
  ```

- **bash** `{"command": "cd /tmp && python3 /tmp/bench_cache_chunker.py > /tmp/bench_cache_chunker.out 2>&1; echo \"EXIT=$?\"", "description": "Run full cache validation benchmark", "run_in_background": true}`

  ```
started background job bash-1078
  ```

- **job_output** `{"job_id": "bash-1078", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **job_output** `{"job_id": "bash-1078", "timeout_ms": 30000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la reports/rapport-cache-chunker.md reports/pensee-cache-chunker.json 2>&1; git log --all --oneline -- reports/rapport-cache-chunker.md reports/pensee-cache-chunker.json | head", "description": "Check target files do not exist"}`

  ```
ls: cannot access 'reports/rapport-cache-chunker.md': No such file or directory
ls: cannot access 'reports/pensee-cache-chunker.json': No such file or directory
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np = json.load(open('reports/pensee-cout-chunker.json'))\nprint(json.dumps(p.get('limites', {}), ensure_ascii=False, indent=1)[:2500])\nprint('--- pistes ---')\nprint(json.dumps(p.get('pistes_rejetees', … [107 caractères tronqués]`

  ```
[
 "Base synthétique A (« est sur le toit ») : le GV a pour tête l'auxiliaire « est » ; _cible_proche le saute et scanne tous les GV. C'est un cas défavorable réel (copules), mais il amplifie le coût. Avec la base B à verbe plein, le gain défaut tombe à ×1,07-1,13.",
 "Corpus court : 6,13 tokens _mots/phrase, 1,10 segment, 0,19 GV. Le gain corpus est faible (×1,18-1,22 chunker, ×0,97-1,07 défaut) ; le O(n²) ne mord pas sur le gold actuel.",
 "Chemin par défaut : le générateur S répond pour les 612 phrases ; _syntagmes_simple n'est appelé que 2 fois/phrase. Le re-chunking dans la boucle est du code mort sur ce chemin ; il ne devient chaud que si S est absent (segmenter_s=False) ou échoue.",
 "Le cache seul ne linéarise pas : pente V2 1,44 (chunker) / 1,55 (défaut) sur 160-1280 ; le tri par segment reste. Une vraie linéarité demande un index pré-trié, non retenu en l'état.",
 "Bruit de mesure : Xeon partagé, temps CPU, 3-11 passes ; l'OFF varie de ×0,90 à ×1,13 selon le point (médiane ×1,00). Les facteurs à ±10 % près.",
 "Instantané de travail : tools/bloc_linguistique.py a changé pendant la préparation (d9c9d5… → 6e8430…) puis a été committé dans 9d5337ce ; les mesures et lignes ci
… [1419 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-1078", "timeout_ms": 60000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -o pid,etime,time,pcpu,cmd -C python3 | grep -E 'bench_cache|PID' ; uptime", "description": "Check benchmark progress and load"}`

  ```
PID     ELAPSED     TIME %CPU CMD
2151587       02:01 00:02:01 99.9 python3 /tmp/bench_cache_chunker.py
 14:35:42  up 1 day 19:01,  2 users,  load average: 13,65, 13,65, 13,11
  ```

- **job_output** `{"job_id": "bash-1078", "timeout_ms": 90000}`

  ```
EXIT=0
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-1078 (bash: cd /tmp && python3 /tmp/bench_cache_chunker.py > /tmp/bench_cache_chunker.out 2>&1; echo "EXIT=$?") finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cat /tmp/bench_cache_chunker.out", "description": "Read benchmark summary output"}`

  ```
{
 "duree_s": 132.685,
 "temps_corpus": {
  "chunker": {
   "temps_ms": {
    "original": 245.288,
    "C1": 198.019,
    "C2": 196.056,
    "OFF": 275.648
   },
   "gains": {
    "original": 1.0,
    "C1": 1.2387,
    "C2": 1.2511,
    "OFF": 0.8899
   },
   "us_par_phrase": {
    "original": 400.8,
    "C1": 323.56,
    "C2": 320.35,
    "OFF": 450.41
   }
  },
  "defaut": {
   "temps_ms": {
    "original": 395.237,
    "C1": 388.287,
    "C2": 385.072,
    "OFF": 398.36
   },
   "gains": {
    "original": 1.0,
    "C1": 1.0179,
    "C2": 1.0264,
    "OFF": 0.9922
   },
   "us_par_phrase": {
    "original": 645.81,
    "C1": 634.46,
    "C2": 629.2,
    "OFF": 650.92
   }
  }
 },
 "compteurs_corpus": {
  "chunker": {
   "C1": {
    "analyses": 612,
    "simple_appels": 1966,
    "simple_calc": 612,
    "simple_hits": 1354
   },
   "C2": {
    "analyses": 612,
    "simple_appels": 1966,
    "simple_calc": 612,
    "simple_hits": 1354,
    "verbe_appels": 197,
    "verbe_calc": 83,
    "verbe_hits": 114
   },
   "OFF": {
    "analyses": 612,
    "simple_appels": 1966,
    "simple_calc": 1966,
    "verbe_appels": 197,
    "verbe_calc": 197
   },
   "original": {
    "analyses": 612,
… [1669 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport json\np = json.load(open('/tmp/bench_cache_chunker.json'))\nfor pt in p['longueurs']['points']:\n    print(pt['chemin'], 'N', pt['N'], 'S', pt['segments_simple'], 'G', pt['gv_simple'],\n          'Ss', pt['segments_s'], 'Gs', pt['gv_s'], 'etq', pt['e … [310 caractères tronqués]`

  ```
chunker N 20 S 6 G 2 Ss 8 Gs 2 etq 86 temps {'original': 1.6413, 'C1': 0.8752, 'C2': 0.7077, 'OFF': 1.6723} gains {'original': 1.0, 'C1': 1.8753, 'C2': 2.3192, 'OFF': 0.9815} eq {'C1': '1/1', 'C2': '1/1', 'OFF': '1/1'}
defaut N 20 S 6 G 2 Ss 8 Gs 2 etq 90 temps {'original': 2.0173, 'C1': 1.954, 'C2': 1.6025, 'OFF': 2.0347} gains {'original': 1.0, 'C1': 1.0324, 'C2': 1.2588, 'OFF': 0.9914} eq {'C1': '1/1', 'C2': '1/1', 'OFF': '1/1'}
chunker N 40 S 12 G 4 Ss 16 Gs 4 etq 170 temps {'original': 4.9741, 'C1': 2.3819, 'C2': 1.4001, 'OFF': 4.9888} gains {'original': 1.0, 'C1': 2.0883, 'C2': 3.5527, 'OFF': 0.9971} eq {'C1': '1/1', 'C2': '1/1', 'OFF': '1/1'}
defaut N 40 S 12 G 4 Ss 16 Gs 4 etq 178 temps {'original': 4.0449, 'C1': 3.9044, 'C2': 2.9205, 'OFF': 4.1024} gains {'original': 1.0, 'C1': 1.036, 'C2': 1.385, 'OFF': 0.986} eq {'C1': '1/1', 'C2': '1/1', 'OFF': '1/1'}
chunker N 80 S 24 G 8 Ss 32 Gs 8 etq 338 temps {'original': 16.1915, 'C1': 4.2609, 'C2': 2.5047, 'OFF': 16.4367} gains {'original': 1.0, 'C1': 3.8, 'C2': 6.4644, 'OFF': 0.9851} eq {'C1': '1/1', 'C2': '1/1', 'OFF': '1/1'}
defaut N 80 S 24 G 8 Ss 32 Gs 8 etq 354 temps {'original': 14.8828, 'C1': 12.541, 'C2': 6.0333, 'OFF': 
… [3171 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Résultats principaux obtenus : je vérifie le contrôle OFF et je prépare le patch réel

- **bash** `{"command": "cd /tmp && cat > /tmp/appliquer_correctif.py <<'PYEOF'\n#!/usr/bin/env python3\n\"\"\"Applique le correctif de cache de la fiche à une COPIE /tmp, jamais au dépôt.\"\"\"\nfrom pathlib import Path\n\nsrc = Path('/tmp/bloc_linguistique_snapshot.py').read_text(encoding='utf-8')\nn = 0\n\nd … [5955 caractères tronqués]`

  ```
diff exit=1
[stderr]
Traceback (most recent call last):
  File "/tmp/appliquer_correctif.py", line 93, in <module>
    rem('return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)',
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        'return Heuristique._verbe_gv(texte, g, verbes, cache_gv)')
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/appliquer_correctif.py", line 10, in rem
    assert src.count(old) == count, (src.count(old), count, old[:80])
           ^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: (2, 1, 'return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)')
wc: /tmp/correctif.diff: No such file or directory
sed: can't read /tmp/correctif.diff: No such file or directory
[exit code: 2]
  ```

- **bash** `{"command": "grep -n 'return Heuristique._verbe_dans' /tmp/bloc_linguistique_snapshot.py", "description": "Locate duplicate return statement"}`

  ```
685:        return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
  ```

- **bash** `{"command": "grep -n 'Heuristique\\._verbe_dans(texte, g' /tmp/bloc_linguistique_snapshot.py && sed -n '675,705p' /tmp/bloc_linguistique_snapshot.py", "description": "Inspect all GV verb calls"}`

  ```
681:            v = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
685:        return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
701:            v = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
            if g["debut"] >= segment["fin"]:
                return g["debut"] - segment["fin"]
            return 0
        # un GV réduit à l'auxiliaire (« a », « est ») ne donne pas la cible : on prend le
        # premier GV proche dont le verbe est **plein** (mesuré : « a » au lieu de « vu »).
        for g in sorted(gvs, key=ecart):
            v = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
            if v and _normaliser(v) not in AUXILIAIRES:
                return v
        g = min(gvs, key=ecart)
        return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)

    @staticmethod
    def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
                        k: int = 3, verbes: list[tuple[int, int, str]] | None = None) -> list[str]:
        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
        if segment.get("type") == "GV" or not gvs:
            return []
   
… [494 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nfrom pathlib import Path\np = Path('/tmp/appliquer_correctif.py')\ns = p.read_text()\ns = s.replace(\"\"\"rem('return Heuristique._verbe_dans(texte, g[\"debut\"], g[\"fin\"], verbes)',\n    'return Heuristique._verbe_gv(texte, g, verbes, cache_gv)')\"\"\",\ … [548 caractères tronqués]`

  ```
ok
15 remplacements ; ecrit /tmp/bloc_linguistique_patche.py
diff exit=1
136 /tmp/correctif.diff
--- /tmp/bloc_linguistique_snapshot.py	2026-11-05 14:32:45.367941902 -0500
+++ /tmp/bloc_linguistique_patche.py	2026-11-05 14:39:35.946375921 -0500
@@ -658,8 +658,19 @@
         return None if strict else (mots[-1][1] if mots else None)
 
     @staticmethod
+    def _verbe_gv(texte: str, g: dict, verbes, cache_gv: dict | None = None):
+        """Le verbe d'un GV, calculé **une fois par analyse** (clé valide dans un seul texte)."""
+        if cache_gv is None:
+            return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
+        cle = (g["debut"], g["fin"])
+        if cle not in cache_gv:
+            cache_gv[cle] = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
+        return cache_gv[cle]
+
+    @staticmethod
     def _cible_proche(texte: str, segment: dict, gvs: list[dict],
-                      verbes: list[tuple[int, int, str]] | None = None) -> str | None:
+                      verbes: list[tuple[int, int, str]] | None = None,
+                      cache_gv: dict | None = None) -> str | None:
         """La cible d'un segment : le **verbe d
… [7268 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/bench_patch_et_off.py <<'PYEOF'\n#!/usr/bin/env python3\n\"\"\"Deux contrôles : (1) OFF corpus remesuré, (2) patch hoisté réel sur copie /tmp.\"\"\"\nfrom __future__ import annotations\nimport importlib.util, json, pathlib, platform, statistics, sys, time\nfrom collections im … [6674 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nfrom pathlib import Path\np = Path('/tmp/bench_patch_et_off.py')\ns = p.read_text()\n# fixer les fabriques C1OFF/C2OFF\ns = s.replace('''mods = {n: Mini((lambda seg, n=n: b.fabrique(n, seg))) for n in (\"C1\", \"C2\", \"C1OFF\", \"C2OFF\")}\nmods[\"original … [3514 caractères tronqués]`

  ```
ok
COMPILE_OK
  ```

- **bash** `{"command": "cd /tmp && python3 /tmp/bench_patch_et_off.py > /tmp/bench_patch_et_off.out 2>&1; echo \"EXIT=$?\"", "description": "Run OFF re-measure and real patch benchmark", "run_in_background": true}`

  ```
started background job bash-1127
  ```

