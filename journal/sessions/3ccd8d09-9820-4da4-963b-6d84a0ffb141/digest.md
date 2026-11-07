# Session DSH — relecture

- identifiant : `3ccd8d09-9820-4da4-963b-6d84a0ffb141`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 18:33:56
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **réparer les frontières de phrase** du bloc linguistique (P0-4 de l'audit produit `reports/rapport-fiabilite-produit.md`), sans modifier le code du dépôt.

Contexte : `tools/bloc_linguistique.py` (`Heuristique._phrases`, `_mots`, `_langue`), `tools/drave.py` (CLI), les audits `reports/rapport-fiabilite-produit.md` (6/46 frontières cassées, URL/email/chemin/abréviation, 3 fausses questions) et `reports/rapport-produit-bloc-l.md`. Le produit doit analyser des textes libres.

À faire :
1. **Cartographie** : sur des textes libres (écris 40 textes variés : URL, emails, chemins `12.5`, dates `12.03.2024`, `M.`/`Dr.`/`etc.`, ellipses, guillemets, listes, titres, code inline), mesure les frontières actuelles : combien de phrases, lesquelles sont fausses, effet sur POS/syntagmes.
2. **Règles candidates** : (a) décimaux (un point entre deux chiffres n'est pas une frontière), (b) abréviations (`M.`, `Dr.`, `etc.`, `p. ex.`, `cf.`) — une minuscule après n'ouvre pas une phrase, (c) URL/emails/chemins (ne pas couper), (d) ponctuation répétée (`...`, `?!`), (e) espace initial (ne pas compter une phrase vide). Pour chacune : mesure sur dev/test (POS, F1 syntagmes, attachement) et sur les 40 textes.
3. **Contrôles négatifs** : les règles ne doivent pas fusionner deux phrases réelles (`Il part. Elle reste.`) ni casser le gold.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-frontieres-phrase.md` et `reports/pensee-frontieres-phrase.json` (avec les 40 textes et les patchs exacts).
5. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, natifs. Simulation par sous-classe ou copie locale.

Rends un résumé : les frontières cassées (avant/après), le gain dev/test par règle, et les patchs exacts.
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

⏵ Cartographie du dépôt et lecture des fichiers cibles

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && git branch --show-current && ls", "description": "Inspect repo status and branch"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/bloc_linguistique.py tools/drave.py reports/rapport-fiabilite-produit.md reports/rapport-produit-bloc-l.md 2>/dev/null", "description": "Check sizes of target files"}`

  ```
2249 tools/bloc_linguistique.py
   402 tools/drave.py
   661 reports/rapport-fiabilite-produit.md
   424 reports/rapport-produit-bloc-l.md
  3736 total
  ```

### 🤖 Assistant

⏵ Lecture du bloc linguistique et des audits

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Heuristique\\|def _phrases\\|def _mots\\|def _langue\\|def \" tools/bloc_linguistique.py | head -80", "description": "Locate Heuristique methods"}`

  ```
63:    def json(self) -> dict:
81:    def json(self) -> dict:
109:    def par_niveau(self) -> dict[str, list[Etiquette]]:
115:    def couverture(self) -> dict[str, float]:
120:    def json(self, avec_duree: bool = False) -> dict:
139:    def analyser(self, texte: str, langue: str | None = None,
150:def _normaliser(texte: str) -> str:
154:def _trigrammes(texte: str) -> list[str]:
159:def _profil(texte: str, top: int = 200) -> dict[str, int]:
164:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
198:def _score_profil(tri: collections.Counter, profil: dict[str, int]) -> float:
205:def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
236:def _script_char(ch: str) -> str:
262:def detecter_script(texte: str) -> str:
467:def _est_adverbe_seul(g: dict) -> bool:
479:def _sans_enclitique(mot: str) -> str:
487:def _est_verbe(mot: str) -> bool:
506:def _role_gp(prep: str) -> str:
531:class Heuristique:
536:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
546:    def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
555:    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
574:  
… [3856 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fronti\\|phrase\\|P0-4\\|6/46\" reports/rapport-fiabilite-produit.md | head -40", "description": "Find P0-4 section in audit"}`

  ```
1:# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 23/46 textes à chevauchement de syntagmes
11:> **50 phrases libres** écrites pour l'audit (textes dans le JSON) ; harnais local non committé
19:**En une phrase.** Sur **50 phrases libres**, la CLI **ne plante pas**, ne rend **aucun JSON
23:**6/46** textes ont une frontière de phrase cassée, et le JSON n'a **ni `schema` ni `version`**.
39:| temps CLI (50 phrases) | **136,8–226,6 ms**, médiane **152,7 ms** |
44:- **Banc libre** : 50 phrases écrites à la main pour cet audit — **41 françaises** (dont
48:  abréviations, citations, ellipses, latin et un texte multi-paragraphes. **Aucune phrase ne
55:  en direct (durée interne, hors démarrage). Les deux sont rapportés par phrase dans le JSON.
68:python3 tools/drave.py analyser "Le prix est 12.5 euros." # deux phrases
73:## 2. Les 50 phrases : ce qui tient, ce qui casse
95:| frontière de phrase cassée | **6/46** textes | URL (f12, f38, f50), email (f37, f50), chemin (f39), abréviation (f20) |
96:| fausses questions | **3** | `?page=2` dans une URL → phrase `interrogative` |
97:| phrases qui se chevauchent | **1** paire | f20 : `[0:59]` et `[2:59]` sur `M. Du
… [3065 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 531, "limit": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
531: class Heuristique:
532:     """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
533: 
534:     nom = "heuristique"
535: 
536:     def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
537:                  seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
538:                  union: bool = True):
539:         self.profils = profils
540:         self.segmenter_s = segmenter_s
541:         self.seuil_ouvert = seuil_ouvert
542:         self.seuil_langue = seuil_langue
543:         self.union = union
544: 
545:     # -- langues / script ---------------------------------------------------
546:     def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
547:         langue, conf, _ = detecter_langue(texte, self.profils, indice)
548:         script = detecter_script(texte)
549:         if conf < self.seuil_langue:
550:             return "und", conf, script
551:         return langue, conf, script
552: 
553:     # -- tokens ---------------------------------------------
… [6113 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"attachement\\|F1 syntagme\\|f1_syntagme\\|syntagmes\" tools/*.py --include=\"*.py\" -l | head -20", "description": "Find evaluation harness for syntagmes"}`

  ```
tools/bloc_linguistique.py
tools/drave.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"dev.*test\\|gold\" tools/*.py | head -30 && ls tools | head -80", "description": "Find dev/test harness scripts"}`

  ```
tools/banc_complet.py
tools/banc_durci.py
tools/banc_lecture.py
tools/bloc_linguistique.py
tools/bloc_tableaux.py
tools/calibrer.py
tools/corpus_gele.py
tools/domaine_ou_langue.py
tools/drave.py
tools/index_spans.py
tools/mesurer_ocr.py
tools/mesurer_scans.py
tools/simuler_scan.py
tools/tete_survol.py
tools/xnli_entrainement.py
tools/xnli_latent.py
tools/xnli_train_complet.py
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
analyse_litteraire.py
analyse_octets_par_jeton.py
analyse_reutilisation_experts.py
analyse_union_experts.py
ancre_professeur.py
applique_pont.py
approximabilite_bloc.py
apres-telechargement-k3.sh
archive_sessions.py
audit_drapeaux_harnais.py
banc_complet.py
banc_durci.py
banc-experts.py
banc_lecteur.py
banc_lecture.py
banc-prelire.py
blanchiment_entree.py
bloc_code.py
bloc_linguistique.py
bloc_maths.py
bloc_tableaux.py
boucle-cerveau.sh
boucle_directe.py
bruit_entree.py
budget_execution_locale.py
c4_retard.sh
c8_carte_profondeur.sh
c8_corpus.sh
c8_entrainer_tete.py
c8_sonde_lineaire.py
cache_pont.py
calibre_modes.py
calib
… [716 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' reports/rapport-produit-bloc-l.md", "description": "Read bloc L report intro"}`

  ```
# Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **HEAD vérifié en fin d'audit** : `c6904284`
> (le HEAD a bougé pendant l'audit ; module `bloc_linguistique.py` inchangé ; `evaluer_gold.py`
> modifié en `7f73c17f`) ·
> **Date** : 2026-11-06 ·
> **Verdict** : ⚠️ **la surface est utilisable en autonomie ; la structure ne l'est pas encore.**
> **Aucun fichier existant modifié par cet audit ; aucun commit.** Sorties : ce rapport et
> [`pensee-produit-bloc-l.json`](pensee-produit-bloc-l.json).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; **50 phrases libres** écrites pour
> l'audit (textes dans le JSON) ; harnais local non committé dans `/tmp/audit_produit_bl`.
> **Porte** : `bash tools/porte-bloc-linguistique.sh` → **verte** (16 tests, autotest UDHR
> **0,9687**, profils permutés **0,0022**).

**En une phrase.** Sur 50 phrases libres
… [6651 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '110,150p' reports/rapport-fiabilite-produit.md && echo ---- && sed -n '555,600p' reports/rapport-fiabilite-produit.md", "description": "Read P0-4 and boundaries details"}`

  ```
étiquettes de **même span** (`phrase` type/négation, `pragmatique` acte/double sens), **28 textes**
portent au moins un chevauchement — mais ce sont des annotations multi-label attendues, pas des
conflits de structure. Le chiffre à retenir pour un client qui construit un arbre est **23/46**.

**Le cas « Élodie sourit. »** — une phrase canonique, 13 étiquettes, 2 unités sémantiques, mais
**aucun syntagme** :

```
langue=und script=Latn source=heuristique · 13 étiquettes · unités sémantiques=2 (85.7% du texte)
POS  Élodie/NOUN sourit/NOUN
SYNTAGMES —
PRAGMATIQUE
  phrase [0:14] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
```

Un client qui demande « les syntagmes » reçoit une section vide sans savoir si c'est un échec,
une limite ou un texte sans structure. Même chose pour `1234567890` (`POS —`, `SYNTAGMES —`,
0 unité, fraction 0,0).

**Les frontières de phrase.** `12.5` donne deux phrases (`[0:15]` et `[15:23]`), `12.03.2024`
en donne trois, `alice@example.org` deux, `Visitez https://example.com/docs?page=2` trois dont
une **fausse question** (`com/docs?`). `M. Dupont…` rend deux phrases qui se chevauchent
(`[0:59]` et `[2:59]`). C'est le défaut le p
… [6090 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/tests/linguistique/ && sed -n '1,80p' tools/tests/linguistique/evaluer_gold.py", "description": "Inspect gold evaluation tooling"}`

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


def 
… [2249 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 1009, "limit": 300}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1009:     def analyser(self, texte: str, langue: str | None = None,
1010:                  contexte: str | None = None) -> Annotation:
1011:         t0 = time.perf_counter()
1012:         if not isinstance(texte, str):
1013:             # une entrée non textuelle est **refusée** proprement (le produit ne plante pas)
1014:             return Annotation(texte=str(texte)[:200], refus="non_texte", source=self.nom,
1015:                               trace=[{"etape": "refus", "raison": "non_texte",
1016:                                       "type": type(texte).__name__}],
1017:                               cout={"octets": 0, "duree_s": round(time.perf_counter() - t0, 6)})
1018:         texte = texte or ""
1019:         trace: list[dict] = []
1020:         if not texte.strip() or not any(ch.isalpha() or ch.isdigit() for ch in texte):
1021:             return Annotation(texte=texte, refus="vide", source=self.nom,
1022:                               trace=[{"etape": "refus", "raison": "vide"}],
1023:                               cout={"octets": len(texte.encode("utf-8", "r
… [19996 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '80,260p' tools/tests/linguistique/evaluer_gold.py && echo ==== && sed -n '1,120p' tools/tests/linguistique/gold_split.py", "description": "Read rest of evaluator and split logic"}`

  ```
def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
    tp = fp = fn = ttp = tfp = tfn = 0
    pos_ok = pos_n = pos_ok_ferme = pos_n_ferme = pos_ok_ouvert = pos_n_ouvert = 0
    conf = defaultdict(Counter)
    acte_ok = neg_ok = mod_ok = ds_ok = 0
    fractions = []
    att_n = att_labels = att_top1 = att_topk = att_exact = 0
    att_topk_exact = 0
    att_exact_any = 0
    par_langue = {"fr": {"cibles": 0, "labels": 0, "exact": 0, "topk": 0},
                  "en": {"cibles": 0, "labels": 0, "exact": 0, "topk": 0}}
    att_v_n = att_v_ok = att_n_n = att_n_ok = 0
    att_t_n = att_t_labels = att_t_top1 = att_t_topk = 0
    for phrase in phrases:
        a = bloc.analyser(phrase["texte"], phrase["langue"])
        fractions.append(a.fraction_semantique)
        pos = _pos_map(a)
        for mot in phrase["mots"]:
            pred = pos.get((mot["debut"], mot["fin"]), "?")
            pos_n += 1
            pos_ok += int(pred == mot["pos"])
            ferme = mot["pos"] in {"DET", "PREP", "PRON", "CONJ", "AUX", "ADV", "NUM"}
            if ferme:
                pos_n_ferme += 1
                pos_ok_ferme += int(pred == mot["pos"])
            else:
                pos
… [10711 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np=json.load(open('tools/tests/linguistique/gold.json'))\nprint(p.keys())\nprint(len(p['phrases']))\nfor x in p['phrases'][:3]:\n    print(json.dumps(x, ensure_ascii=False)[:800])\nPY", "description": "I … [23 caractères tronqués]`

  ```
dict_keys(['version', 'phrases', 'note'])
20
{"id": "g001", "langue": "fr", "texte": "Le chat dort.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chat", "pos": "NOUN", "debut": 3, "fin": 7}, {"texte": "dort", "pos": "VERB", "debut": 8, "fin": 12}], "segments": [{"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}, {"type": "GV", "texte": "dort", "role": "prédicat", "debut": 8, "fin": 12}], "pragma": {"acte": "assertion"}}
{"id": "g002", "langue": "fr", "texte": "Le chat de la voisine dort.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chat", "pos": "NOUN", "debut": 3, "fin": 7}, {"texte": "de", "pos": "PREP", "debut": 8, "fin": 10}, {"texte": "la", "pos": "DET", "debut": 11, "fin": 13}, {"texte": "voisine", "pos": "NOUN", "debut": 14, "fin": 21}, {"texte": "dort", "pos": "VERB", "debut": 22, "fin": 26}], "segments": [{"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}, {"type": "GP", "texte": "de la voisine", "role": "possession", "debut": 8, "fin": 21, "cibles": ["chat"], "cible": "chat"}, {"type": "GV", "texte": "dort", "role": "prédicat", "debut": 22, "fin": 26}], "pragma": {"act
… [818 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"phrase\\|fronti\" tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/test_bloc_linguistique.py | head -50", "description": "Check phrase tests in gold tooling"}`

  ```
tools/tests/linguistique/evaluer_gold.py:25:    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
tools/tests/linguistique/evaluer_gold.py:26:    reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
tools/tests/linguistique/evaluer_gold.py:27:    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
tools/tests/linguistique/evaluer_gold.py:41:    Le gold vivant grandit (phrases, liens) ; les portes qui codent un chiffre exact
tools/tests/linguistique/evaluer_gold.py:44:    return json.loads(GELE.read_text(encoding="utf-8"))["phrases"]
tools/tests/linguistique/evaluer_gold.py:47:def par_source(phrases: list[dict], source: str) -> list[dict]:
tools/tests/linguistique/evaluer_gold.py:48:    return [p for p in phrases if p.get("source") == source]
tools/tests/linguistique/evaluer_gold.py:66:    neg = any(e.type == "négation" for e in a.etiquettes if e.niveau == "phrase")
tools/tests/linguistique/evaluer_gold.py:67:    mod = any(e.type == "modalité" for e in a.etiquettes if e.niveau == "phrase")
tools/tests/linguistique/evaluer_gold.py:80:def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
tools/tests/linguistique/evaluer_gold.py:93:    for p
… [2577 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' tools/bloc_linguistique.py && grep -n \"python_requires\\|requires-python\\|python =\" pyproject.toml setup.py setup.cfg 2>/dev/null", "description": "Check imports and Python version"}`

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
… [1331 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys; sys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique\ncas = [\"Le prix est 12.5 euros.\",\"Rendez-vous le 12.03.2024 à 9h.\",\"Écrivez à alice@example.org.\",\"Visitez https://example.co … [517 caractères tronqués]`

  ```
'Le prix est 12.5 euros.' -> 2
    0 15 'Le prix est 12.' déclarative
    15 23 '5 euros.' déclarative
'Rendez-vous le 12.03.2024 à 9h.' -> 3
    0 18 'Rendez-vous le 12.' déclarative
    18 21 '03.' déclarative
    21 31 '2024 à 9h.' déclarative
'Écrivez à alice@example.org.' -> 2
    0 24 'Écrivez à alice@example.' déclarative
    24 28 'org.' déclarative
'Visitez https://example.com/docs?page=2' -> 3
    0 24 'Visitez https://example.' déclarative
    24 33 'com/docs?' interrogative
    33 39 'page=2' déclarative
'Ouvrez src/tools/bloc_linguistique.py.' -> 2
    0 35 'Ouvrez src/tools/bloc_linguistique.' déclarative
    35 38 'py.' déclarative
'M. Dupont…' -> 2
    0 10 'M. Dupont…' déclarative
    2 10 ' Dupont…' déclarative
'Il part. Elle reste.' -> 2
    0 8 'Il part.' déclarative
    8 20 ' Elle reste.' déclarative
'Bonjour. Il part.' -> 2
    0 8 'Bonjour.' déclarative
    8 17 ' Il part.' déclarative
'Il hésite... puis il part.' -> 2
    0 12 'Il hésite...' déclarative
    12 26 ' puis il part.' déclarative
'Vraiment ?!' -> 1
    0 11 'Vraiment ?!' interrogative
'« Bonjour. » Elle part.' -> 2
    0 10 '« Bonjour.' déclarative
    10 23 ' » Elle part.' déclarative
'Le Dr. M
… [539 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-produit-bloc-l.json'))\nprint(type(p), list(p)[:20] if isinstance(p,dict) else len(p))\nPY", "description": "Inspect audit JSON keys"}`

  ```
<class 'dict'> ['rapport', 'ligne', 'branche', 'commit', 'date', 'objet', 'verdict', 'dispositif', 'gold', 'banc_50', 'cas_limites', 'performance', 'contrat', 'compositions', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fronti\\|f12\\|f20\\|f37\\|f38\\|f39\\|f50\" reports/pensee-produit-bloc-l.json | head -30", "description": "Find boundary data in audit JSON"}`

  ```
8: "verdict": "⚠️ utilisable en surface (graphème, mot, POS fermées, phrase, document) sur du français/anglais propre ; fragile en structure (syntagmes qui se chevauchent, frontières de phrase, compositions, langue). 0 plantage sur 50 phrases, mais 34/50 avec au moins une anomalie de contrat et 1 plantage sur 25 cas limites.",
549:     "id": "f12",
605:     "id": "f20",
1149:    "id": "f12",
1375:    "id": "f20",
3226:   "titre": "Réparer les frontières de phrase et la tokenisation des réalités numériques",
3575:     "id": "f20",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-produit-bloc-l.json'))\nb=p['banc_50']\nprint(b.keys())\nfor k,v in b.items():\n    if k!='detail': print(k, type(v), str(v)[:500])\nfor x in b['detail'][:5]:\n    print … [92 caractères tronqués]`

  ```
dict_keys(['phrases', 'mots', 'etiquettes', 'attachements', 'categories', 'langues_detectees', 'scripts', 'crashes', 'refus', 'sorties_vides', 'sans_anomalie', 'avec_anomalie', 'anomalies_total', 'anomalies', 'niveaux', 'fraction', 'pos', 'phrases_stats', 'document', 'graphème', 'url_emoji', 'langue', 'double_sens', 'detail'])
phrases <class 'int'> 50
mots <class 'int'> 819
etiquettes <class 'int'> 4320
attachements <class 'dict'> {'total': 265, 'cibles_fermees': 16, 'cibles_fermees_detail': {'au': 3, 'was': 3, 'lui': 2, 'pas': 2, 'have': 2, 'entre': 2, 'ne': 1, 'Tu': 1}, 'cible_absente': 0, 'cible_non_token': 0, 'segment_mismatch': 0, 'cible_ambigue': 3, 'offset_cible': False}
categories <class 'dict'> {'fr': 29, 'en': 14, 'url+email': 1, 'sms': 1, 'sans-ponctuation-finale': 1, 'markdown': 1, 'cyrillique': 1, 'sinogrammes': 1, 'emoji': 1}
langues_detectees <class 'dict'> {'fr': 34, 'en': 14, 'und': 2}
scripts <class 'dict'> {'Latn': 48, 'Cyrl': 1, 'Hani': 1}
crashes <class 'int'> 0
refus <class 'int'> 0
sorties_vides <class 'int'> 0
sans_anomalie <class 'int'> 16
avec_anomalie <class 'int'> 34
anomalies_total <class 'int'> 149
anomalies <class 'dict'> {'chevauchement_syntagme': {'
… [5428 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-produit-bloc-l.json'))\nfor x in p['banc_50']['detail']:\n    if x['id'] in ('f10','f12','f20','f25','f26','f29','f37','f38','f39','f50'):\n        print(x['id'], x['cat … [76 caractères tronqués]`

  ```
f10 fr/abréviations "M. Dupont, le directeur de l'usine, a annoncé hier qu'il prendrait sa retraite à la fin de l'année, etc."
f12 fr/incise-tirets "Le rapport — que personne n'avait lu — fut pourtant cité dans toutes les réunions de la semaine."
f20 fr/question-pourquoi 'Pourquoi les feuilles changent-elles de couleur en automne ?'
f25 fr/concession "Les résultats préliminaires suggèrent une amélioration, bien que la marge d'erreur reste importante."
f26 fr/impérative-familière 'Arrête de tourner autour du pot et dis-nous la vérité, une bonne fois pour toutes !'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/drave.py", "description": "Read CLI implementation head"}`

  ```
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, trois gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques — et sa mesure sur le gold.
Ce qu'elle n'expose pas encore : le neuronal (`llama-cli` ou endpoint local), la restitution
(annotation → texte), la traduction et la génération : ils demandent des poids, un service ou
un GPU, alors que ce prototype est hors ligne, CPU et sans réseau.

Codes de sortie : 0 succès · 2 usage · 1 erreur (ou refus d'analyse).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import random
import sys
import textwrap

# Le dépôt d'abord — 
… [3762 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '70,180p' tools/tests/linguistique/test_bloc_linguistique.py && sed -n '1,70p' tools/tests/linguistique/test_bloc_linguistique.py", "description": "Read existing linguistic tests"}`

  ```
def test_activation_semantique(self):
        a = self.h.analyser(TEXTE, "fr")
        sem = bl.CoucheSemantique()
        r = sem.activer(a)
        self.assertLess(r["fraction"], 1.0)
        self.assertGreater(r["unites"], 0)
        self.assertLess(r["cout"], len(TEXTE))

    def test_refus(self):
        self.assertEqual(self.h.analyser("").refus, "vide")
        self.assertEqual(self.h.analyser("... !!! ???").refus, "vide")
        self.assertEqual(self.h.analyser("qqqqq zzzzz wwwww").langue, "und")

    def test_rejeu(self):
        self.assertEqual(self.h.analyser(TEXTE, "fr").json(),
                         self.h.analyser(TEXTE, "fr").json())

    def test_adaptateur_neuronal_avec_faux_modele(self):
        d = pathlib.Path(tempfile.mkdtemp())
        faux = d / "faux_llama.py"
        faux.write_text(
            "#!/usr/bin/env python3\nimport json\n"
            "print(json.dumps({'langue':'fr','script':'Latn','etiquettes':["
            "{'niveau':'phrase','type':'type','valeur':'déclarative','debut':0,'fin':4,'confiance':0.9},"
            "{'niveau':'pragmatique','type':'acte','valeur':'assertion','debut':0,'fin':4,'confiance':0.8}]}))\n",
            encoding="utf
… [7182 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"_phrases\\|frontière\" tools/tests/ tools/porte-bloc-linguistique.sh 2>/dev/null | head -30 && cat tools/porte-bloc-linguistique.sh", "description": "Find sentence tests and gate"}`

  ```
tools/tests/documents/corpus/technique/contexte-long.md:188:la frontière entière — le détail est dans
tools/tests/documents/corpus/tableau/dependances.md:6:> inversées, frontière) et **dessiné** dans
tools/tests/documents/corpus/tableau/dependances.md:42:- **La frontière fait 12 items** : le « jamais en attente » n'est pas une file d'un seul élément.
tools/tests/documents/corpus/tableau/dependances.md:134:6. **Sept dépendances manquantes.** `R11` prend en entrée les frontières de section de `R01` sans
tools/tests/documents/corpus/tableau/dependances.md:147:## 5. La frontière : ce qui est réellement non bloqué
tools/tests/documents/corpus/tableau/index.md:127:- [Le graphe des dépendances](dependances.md) — les arêtes dures, les plafonds, la frontière et les priorités.
tools/tests/documents/corpus/tableau/roadmap.md:284:  3 plafonds, la frontière et les sous-items.
tools/tests/linguistique/qualifier_frontiere_71.py:2:"""qualifier_frontiere_71.py — la frontière heuristique sur les 71 langues du dépôt.
tools/tests/linguistique/qualifier_frontiere_71.py:5:frontière « couverture × précision par unité de calcul ». Ici, sur le lexique
tools/tests/linguistique/classement_cible.py:538:    id
… [950 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np=json.load(open('reports/pensee-produit-bloc-l.json'))\nfor x in p['banc_50']['detail']:\n    if x['cat'] in ('markdown','sans-ponctuation-finale') or 'markdown' in x['cat']:\n        print(x['id'], x[ … [97 caractères tronqués]`

  ```
x45 sans-ponctuation-finale "Ceci est une phrase sans ponctuation finale et elle continue longtemps sans marquer de pause puis elle s'arrête"
x46 markdown "# Notes de réunion\n\nLe budget 2025 a été validé à l'unanimité.\n\n- Priorité : réduire les coûts.\n- Échéance : fin mars.\n\nProchaine réunion jeudi."
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json','gold_gele.json']:\n    p=json.load(open('tools/tests/linguistique/'+f))\n    n=sum('\\n' in x['texte'] for x in p['phrases'])\n    print(f … [203 caractères tronqués]`

  ```
gold.json 20 avec newline: 0
gold_reel.json 432 avec newline: 0
gold_synthetique.json 160 avec newline: 0
gold_gele.json 602 avec newline: 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,re\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    p=json.load(open('tools/tests/linguistique/'+f))\n    for x in p['phrases']:\n        if re.search(r\"\\.\\.\\.|…\", x['texte']): … [110 caractères tronqués]`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,re\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    p=json.load(open('tools/tests/linguistique/'+f))\n    for x in p['phrases']:\n        if re.search(r\"[.!?…]\\s*[»\\\"”’)]\", x[' … [120 caractères tronqués]`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,re\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    p=json.load(open('tools/tests/linguistique/'+f))\n    multi=[x for x in p['phrases'] if len(re.findall(r'[.!?…]', x['texte']))>1] … [190 caractères tronqués]`

  ```
gold.json 20 multi-ponctuation: 0
gold_reel.json 432 multi-ponctuation: 2
   r308 'Marie lit. Elle aime les livres.'
   r318 'Marie reads. She loves books.'
gold_synthetique.json 160 multi-ponctuation: 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np=json.load(open('tools/tests/linguistique/gold_reel.json'))\nfor x in p['phrases']:\n    if x['id'] in ('r308','r318'): print(json.dumps(x,ensure_ascii=False,indent=1))\nPY", "description": "Inspect mu … [27 caractères tronqués]`

  ```
{
 "id": "r308",
 "langue": "fr",
 "texte": "Marie lit. Elle aime les livres.",
 "mots": [
  {
   "texte": "Marie",
   "pos": "NOUN",
   "debut": 0,
   "fin": 5
  },
  {
   "texte": "lit",
   "pos": "VERB",
   "debut": 6,
   "fin": 9
  },
  {
   "texte": "Elle",
   "pos": "PRON",
   "debut": 11,
   "fin": 15
  },
  {
   "texte": "aime",
   "pos": "VERB",
   "debut": 16,
   "fin": 20
  },
  {
   "texte": "les",
   "pos": "DET",
   "debut": 21,
   "fin": 24
  },
  {
   "texte": "livres",
   "pos": "NOUN",
   "debut": 25,
   "fin": 31
  }
 ],
 "segments": [
  {
   "type": "GN",
   "texte": "Marie",
   "role": "agent",
   "debut": 0,
   "fin": 5
  },
  {
   "type": "GV",
   "texte": "lit",
   "role": "prédicat",
   "debut": 6,
   "fin": 9
  },
  {
   "type": "GN",
   "texte": "Elle",
   "role": "agent",
   "debut": 11,
   "fin": 15
  },
  {
   "type": "GV",
   "texte": "aime",
   "role": "prédicat",
   "debut": 16,
   "fin": 20
  },
  {
   "type": "GN",
   "texte": "les livres",
   "role": "patient",
   "debut": 21,
   "fin": 31
  }
 ],
 "pragma": {
  "acte": "assertion",
  "coref": {
   "elle": "marie"
  }
 },
 "source": "reel"
}
{
 "id": "r318",
 "langue": "en",
 "texte": "Marie read
… [1011 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys; sys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique\nfor t in [\"Le prix est 12.5 euros.\",\"alice@example.org\",\"https://example.com/docs?page=2\",\"src/tools/bloc_linguistique.py\",\ … [164 caractères tronqués]`

  ```
'Le prix est 12.5 euros.'
   [(0, 2, 'Le', 'mot'), (3, 7, 'prix', 'mot'), (8, 11, 'est', 'mot'), (12, 14, '12', 'nombre'), (14, 15, '.', 'ponctuation'), (15, 16, '5', 'nombre'), (17, 22, 'euros', 'mot'), (22, 23, '.', 'ponctuation')]
'alice@example.org'
   [(0, 5, 'alice', 'mot'), (5, 6, '@', 'ponctuation'), (6, 13, 'example', 'mot'), (13, 14, '.', 'ponctuation'), (14, 17, 'org', 'mot')]
'https://example.com/docs?page=2'
   [(0, 5, 'https', 'mot'), (5, 6, ':', 'ponctuation'), (6, 7, '/', 'ponctuation'), (7, 8, '/', 'ponctuation'), (8, 15, 'example', 'mot'), (15, 16, '.', 'ponctuation'), (16, 19, 'com', 'mot'), (19, 20, '/', 'ponctuation'), (20, 24, 'docs', 'mot'), (24, 25, '?', 'ponctuation'), (25, 29, 'page', 'mot'), (29, 30, '=', 'ponctuation'), (30, 31, '2', 'nombre')]
'src/tools/bloc_linguistique.py'
   [(0, 3, 'src', 'mot'), (3, 4, '/', 'ponctuation'), (4, 9, 'tools', 'mot'), (9, 10, '/', 'ponctuation'), (10, 27, 'bloc_linguistique', 'mot'), (27, 28, '.', 'ponctuation'), (28, 30, 'py', 'mot')]
'Rendez-vous le 12.03.2024.'
   [(0, 11, 'Rendez-vous', 'mot'), (12, 14, 'le', 'mot'), (15, 17, '12', 'nombre'), (17, 18, '.', 'ponctuation'), (18, 20, '03', 'nombre'), (20, 21, '.', 'po
… [255 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,re\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    p=json.load(open('tools/tests/linguistique/'+f))\n    d=[x for x in p['phrases'] if re.search(r'\\d',x['texte'])]\n    print(f,le … [141 caractères tronqués]`

  ```
gold.json 0
gold_reel.json 0
gold_synthetique.json 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,re\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    p=json.load(open('tools/tests/linguistique/'+f))\n    for x in p['phrases']:\n        if re.search(r'\\b(M|MM|Mme|Dr|Pr|etc|cf|p| … [150 caractères tronqués]`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,re\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    p=json.load(open('tools/tests/linguistique/'+f))\n    q=[x for x in p['phrases'] if '?' in x['texte']]\n    print(f,len(q))\n     … [123 caractères tronqués]`

  ```
gold.json 1
   g013 'Peux-tu venir ?' {'acte': 'question', 'reponse': 'oui'}
gold_reel.json 19
   r010 'Tu viens demain ?' {'acte': 'question', 'reponse': 'oui'}
   r030 'You come tomorrow?' {'acte': 'question', 'reponse': 'yes'}
   r304 'Viens-tu demain ?' {'acte': 'question', 'reponse': 'oui'}
   r314 'Do you come tomorrow?' {'acte': 'question', 'reponse': 'yes'}
   r408 'Ne viens-tu pas demain ?' {'acte': 'question', 'reponse': 'si'}
   r409 'Ne mange-t-il pas ?' {'acte': 'question', 'reponse': 'si'}
   r410 'Ne dort-elle pas ?' {'acte': 'question', 'reponse': 'si'}
   r411 'Ne partent-ils pas ?' {'acte': 'question', 'reponse': 'si'}
   r412 'Ne lis-tu pas ?' {'acte': 'question', 'reponse': 'si'}
   r413 'Ne parle-t-elle pas ?' {'acte': 'question', 'reponse': 'si'}
gold_synthetique.json 14
   s009 'le lent village cherche?' {'acte': 'question', 'negation': False, 'modalite': False, 'double_sens': False, 'reponse': 'oui'}
   s043 'Hugo écoute?' {'acte': 'question', 'negation': False, 'modalite': False, 'double_sens': False, 'reponse': 'oui'}
   s046 'le canard observe?' {'acte': 'question', 'negation': False, 'modalite': False, 'double_sens': False, 'reponse': 'oui'}
   s062 'Emm
… [883 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,re\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    p=json.load(open('tools/tests/linguistique/'+f))\n    for x in p['phrases']:\n        if '!' in x['texte'] or '?' in x['texte'][: … [140 caractères tronqués]`

  ```
gold.json g010 'Viens ici !' {'acte': 'exclamation'}
gold_reel.json r305 'Ferme la porte !' {'acte': 'ordre'}
gold_reel.json r315 'Close the door!' {'acte': 'ordre'}
gold_synthetique.json s005 'un rapide chemin crie!' {'acte': 'exclamation', 'negation': False, 'modalite': False, 'double_sens': False}
gold_synthetique.json s006 'la forêt crie!' {'acte': 'exclamation', 'negation': False, 'modalite': False, 'double_sens': False}
gold_synthetique.json s007 'Nage!' {'acte': 'exclamation', 'negation': False, 'modalite': False, 'double_sens': False}
gold_synthetique.json s025 'Cherche!' {'acte': 'exclamation', 'negation': False, 'modalite': False, 'double_sens': False}
gold_synthetique.json s028 'elle dessine!' {'acte': 'exclamation', 'negation': False, 'modalite': False, 'double_sens': False}
gold_synthetique.json s034 'Marche!' {'acte': 'exclamation', 'negation': False, 'modalite': False, 'double_sens': False}
gold_synthetique.json s036 'Commence!' {'acte': 'exclamation', 'negation': False, 'modalite': False, 'double_sens': False}
gold_synthetique.json s038 'ils commence!' {'acte': 'exclamation', 'negation': False, 'modalite': False, 'double_sens': False}
gold_synthetique.json s057 'Fin
… [2508 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Prototype des règles de frontière et banc d'essai local

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 - <<'PY'\nimport sys; sys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger, evaluer_bloc\nfrom gold_split import dev, test\np=charger … [251 caractères tronqués]`

  ```
612 422 190
0.8375 0.6165 0.9509 {'acte': 1.0, 'negation': 0.9787, 'modalite': 0.9929, 'double_sens': 0.9336}
[stderr]

real	0m0,444s
user	0m0,416s
sys	0m0,028s
  ```

- **bash** `{"command": "mkdir -p /tmp/frontieres && cat > /tmp/frontieres/proto.py <<'PY'\n\"\"\"Prototype local des frontières de phrase — aucune écriture dans le dépôt.\"\"\"\nfrom __future__ import annotations\nimport re\nimport sys\nsys.path.insert(0, \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools … [11485 caractères tronqués]`

  ```
'Le prix est 12.5 euros.' -> 1
    0 23 'Le prix est 12.5 euros.' déclarative
'Rendez-vous le 12.03.2024 à 9h.' -> 1
    0 31 'Rendez-vous le 12.03.2024 à 9h.' déclarative
'Écrivez à alice@example.org.' -> 1
    0 28 'Écrivez à alice@example.org.' déclarative
'Visitez https://example.com/docs?page=2' -> 1
    0 39 'Visitez https://example.com/docs?page=2' déclarative
'Ouvrez src/tools/bloc_linguistique.py.' -> 1
    0 38 'Ouvrez src/tools/bloc_linguistique.py.' déclarative
'M. Dupont…' -> 1
    0 10 'M. Dupont…' déclarative
'Il part. Elle reste.' -> 2
    0 8 'Il part.' déclarative
    9 20 'Elle reste.' déclarative
'Bonjour. Il part.' -> 2
    0 8 'Bonjour.' déclarative
    9 17 'Il part.' déclarative
'Il hésite... puis il part.' -> 1
    0 26 'Il hésite... puis il part.' déclarative
'Vraiment ?!' -> 1
    0 11 'Vraiment ?!' interrogative
'« Bonjour. » Elle part.' -> 2
    0 12 '« Bonjour. »' déclarative
    13 23 'Elle part.' déclarative
'Le Dr. Martin arrive.' -> 1
    0 21 'Le Dr. Martin arrive.' déclarative
'des pommes, des poires, etc. Il part.' -> 2
    0 28 'des pommes, des poires, etc.' déclarative
    29 37 'Il part.' déclarative
'cf. la note 3.' -> 1
    0 14 'cf. la not
… [2118 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\nimport proto\nt=\"Le lien est https://example.com/a.b?x=1. Cliquez ensuite.\"\nprint(len(t), [(i,c) for i,c in enumerate(t)])\nprint(proto._zones_protegees(t))\nfor i,c in enumerate(t):\n    if c=='.': print('dot',i, 'dans', proto._dans(proto._zon … [108 caractères tronqués]`

  ```
57 [(0, 'L'), (1, 'e'), (2, ' '), (3, 'l'), (4, 'i'), (5, 'e'), (6, 'n'), (7, ' '), (8, 'e'), (9, 's'), (10, 't'), (11, ' '), (12, 'h'), (13, 't'), (14, 't'), (15, 'p'), (16, 's'), (17, ':'), (18, '/'), (19, '/'), (20, 'e'), (21, 'x'), (22, 'a'), (23, 'm'), (24, 'p'), (25, 'l'), (26, 'e'), (27, '.'), (28, 'c'), (29, 'o'), (30, 'm'), (31, '/'), (32, 'a'), (33, '.'), (34, 'b'), (35, '?'), (36, 'x'), (37, '='), (38, '1'), (39, '.'), (40, ' '), (41, 'C'), (42, 'l'), (43, 'i'), (44, 'q'), (45, 'u'), (46, 'e'), (47, 'z'), (48, ' '), (49, 'e'), (50, 'n'), (51, 's'), (52, 'u'), (53, 'i'), (54, 't'), (55, 'e'), (56, '.')]
[(12, 39)]
dot 27 dans True
dot 33 dans True
dot 39 dans False
dot 56 dans False
[(0, 57, 'Le lien est https://example.com/a.b?x=1. Cliquez ensuite.', 'déclarative')]
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\nimport re\np='proto.py'\ns=open(p).read()\ns=s.replace('''# identifiant pointé : os.path, Heuristique._phrases, example.com (point suivi d'une minuscule)\n_IDENT_POINTE = re.compile(r\"\\\\b[A-Za-z_]\\\\w*(?:\\\\.[a-z_]\\\\w*)+(?![\\\\w])\")\n_POI … [1019 caractères tronqués]`

  ```
'Le prix est 12.5 euros.' -> 1
    0 23 'Le prix est 12.5 euros.' déclarative
'Rendez-vous le 12.03.2024 à 9h.' -> 1
    0 31 'Rendez-vous le 12.03.2024 à 9h.' déclarative
'Écrivez à alice@example.org.' -> 1
    0 28 'Écrivez à alice@example.org.' déclarative
'Visitez https://example.com/docs?page=2' -> 1
    0 39 'Visitez https://example.com/docs?page=2' déclarative
'Ouvrez src/tools/bloc_linguistique.py.' -> 1
    0 38 'Ouvrez src/tools/bloc_linguistique.py.' déclarative
'M. Dupont…' -> 1
    0 10 'M. Dupont…' déclarative
'Il part. Elle reste.' -> 2
    0 8 'Il part.' déclarative
    9 20 'Elle reste.' déclarative
'Bonjour. Il part.' -> 2
    0 8 'Bonjour.' déclarative
    9 17 'Il part.' déclarative
'Il hésite... puis il part.' -> 1
    0 26 'Il hésite... puis il part.' déclarative
'Vraiment ?!' -> 1
    0 11 'Vraiment ?!' interrogative
'« Bonjour. » Elle part.' -> 2
    0 12 '« Bonjour. »' déclarative
    13 23 'Elle part.' déclarative
'Le Dr. Martin arrive.' -> 1
    0 21 'Le Dr. Martin arrive.' déclarative
'des pommes, des poires, etc. Il part.' -> 2
    0 28 'des pommes, des poires, etc.' déclarative
    29 37 'Il part.' déclarative
'cf. la note 3.' -> 1
    0 14 'cf. la not
… [2167 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\nimport proto\nt=\"use a tool, e.g. a hammer, to fix it.\"\nprint([(i,c) for i,c in enumerate(t) if c in '.'])\nprint(proto._zones_protegees(t))\nfor i,c in enumerate(t):\n    if c=='.': print(i, proto._dans(proto._zones_protegees(t), i, i+1))\nPY" … [41 caractères tronqués]`

  ```
[(13, '.'), (15, '.'), (36, '.')]
[]
13 False
15 False
36 False
  ```

- **bash** `{"command": "cd /tmp/frontieres && sed -i 's/_ABREV_POINTEE = re.compile(r\"\\\\b(?:\\[A-Za-z\\]\\\\.){2,}\\[A-Za-z\\]\\\\b\")/_ABREV_POINTEE = re.compile(r\"\\\\b(?:[A-Za-z]\\\\.)+[A-Za-z]\\\\b\")/' proto.py && grep -n \"_ABREV_POINTEE\" proto.py && python3 - <<'PY'\nimport proto\nfor t in [\"use a … [236 caractères tronqués]`

  ```
51:_ABREV_POINTEE = re.compile(r"\b(?:[A-Za-z]\.)+[A-Za-z]\b")
69:    for motif in (_URL, _EMAIL, _DOMAINE, _CHEMIN, _EXTENSION, _CODE_BLOC, _CODE_INLINE, _ABREV_POINTEE, _IDENT_POINTE):
'use a tool, e.g. a hammer, to fix it.' [(0, 37, 'use a tool, e.g. a hammer, to fix it.', 'déclarative')]
'i.e. ceci.' [(0, 10, 'i.e. ceci.', 'déclarative')]
'U.S.A. Il part.' [(0, 6, 'U.S.A.', 'déclarative'), (7, 15, 'Il part.', 'déclarative')]
'U.S.A. Paris.' [(0, 13, 'U.S.A. Paris.', 'déclarative')]
'il part.elle reste.' [(0, 8, 'il part.', 'déclarative'), (8, 19, 'elle reste.', 'déclarative')]
  ```

- **bash** `{"command": "cat > /tmp/frontieres/corpus.py <<'PY'\n\"\"\"Les 40 textes libres de la cartographie P0-4.\"\"\"\nfrom __future__ import annotations\n\nTEXTES = [\n {\"id\":\"n01\",\"cat\":\"négatif/2 phrases\",\"texte\":\"Il part. Elle reste.\",\"attendu\":[\"Il part.\",\"Elle reste.\"],\"types\":[\" … [8530 caractères tronqués]`

  ```
40 textes, 59 phrases attendues
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\np='proto.py'\ns=open(p).read()\ns=s.replace('''                if self.regles[\"f\"] and self._nouvelle_ligne(texte, i, j):\n                    d = debut\n                    while d < i and texte[d].isspace():\n                        d += 1\n   … [2624 caractères tronqués]`

  ```
DIFF t03 '1. Ouvrir le fichier.\n2. Lire la première ligne.'
  att [(0, 21), (22, 48)]
  got [(0, 2, '1.', 'déclarative'), (3, 21, 'Ouvrir le fichier.', 'déclarative'), (22, 24, '2.', 'déclarative'), (25, 48, 'Lire la première ligne.', 'déclarative')]
TYPE t03 ['déclarative', 'déclarative', 'déclarative', 'déclarative'] ['déclarative', 'déclarative']
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\np='proto.py'\ns=open(p).read()\ns=s.replace('''        # (a) décimaux : un point entre deux chiffres\n        if self.regles[\"a\"] and run == \".\" and 0 < i < n - 1 \\\\\n                and texte[i - 1].isdigit() and texte[i + 1].isdigit():\n   … [1157 caractères tronqués]`

  ```
écarts: 0
  ```

- **bash** `{"command": "cat > /tmp/frontieres/mesure40.py <<'PY'\n\"\"\"Mesures P0-4 : avant/après sur les 40 textes, POS/syntagmes et frontières.\"\"\"\nfrom __future__ import annotations\nimport json\nimport sys\nsys.path.insert(0, \"/tmp/frontieres\")\nsys.path.insert(0, \"/home/stephane/Data13TB/stephane/G … [8647 caractères tronqués]`

  ```
== 40 textes ==
original     phrases=102 exacts= 2/40 cassés=38 extra=47 missing= 4 chev= 9 esp=31 fq= 5
neutre       phrases=102 exacts= 2/40 cassés=38 extra=45 missing= 2 chev= 0 esp=31 fq= 5
regle_a      phrases= 87 exacts= 6/40 cassés=34 extra=30 missing= 2 chev= 0 esp=29 fq= 5
regle_b      phrases= 92 exacts= 8/40 cassés=32 extra=35 missing= 2 chev= 0 esp=21 fq= 5
regle_c      phrases= 83 exacts=10/40 cassés=30 extra=26 missing= 2 chev= 0 esp=31 fq= 0
regle_d      phrases=101 exacts= 3/40 cassés=37 extra=44 missing= 2 chev= 0 esp=30 fq= 5
regle_e      phrases=102 exacts=13/40 cassés=27 extra=45 missing= 2 chev= 0 esp= 0 fq= 5
regle_f      phrases=104 exacts= 4/40 cassés=36 extra=45 missing= 0 chev= 0 esp=30 fq= 5
toutes       phrases= 59 exacts=40/40 cassés= 0 extra= 0 missing= 0 chev= 0 esp= 0 fq= 0

== effet POS/syntagmes/actes ==
original     pos_diff= 0 syn_diff= 0 att_diff= 0 phr_diff= 0 acte_diff= 0 traversants=0->0 actes_faux=63/102
neutre       pos_diff= 0 syn_diff= 0 att_diff= 0 phr_diff=11 acte_diff=11 traversants=0->0 actes_faux=63/102
regle_a      pos_diff= 0 syn_diff= 0 att_diff= 0 phr_diff=17 acte_diff=17 traversants=0->0 actes_faux=48/87
regle_b      pos_diff= 0
… [625 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\nimport json, mesure40 as m\nr=m.mesurer_40()\nfor nom in ('original','toutes'):\n    ts=r[nom]['textes']\n    print('\\n==',nom)\n    for x in ts:\n        if x['extra'] or x['missing'] or x['overlaps'] or x['fausses_questions'] or x['leading']:\n … [434 caractères tronqués]`

  ```
== original
n01 négatif/2 phrases phr 2 extra [] missing [] chev 0 esp 1 fq 0
n02 négatif/3 phrases phr 3 extra [] missing [] chev 0 esp 2 fq 0
d01 décimal phr 2 extra [15] missing [] chev 0 esp 0 fq 0
d02 décimal+milliers phr 2 extra [30] missing [] chev 0 esp 0 fq 0
d03 date phr 5 extra [17, 20, 46, 49] missing [] chev 0 esp 0 fq 0
d04 version+IP phr 6 extra [13, 15, 32, 36, 38] missing [] chev 0 esp 0 fq 0
u01 URL+query phr 3 extra [24, 33] missing [] chev 0 esp 0 fq 1
u02 URL+phrase phr 5 extra [28, 34, 36] missing [] chev 0 esp 1 fq 1
e01 courriel phr 2 extra [24] missing [] chev 0 esp 0 fq 0
e02 courriel+URL phr 4 extra [26, 55, 63] missing [] chev 0 esp 0 fq 1
c01 chemin+code phr 2 extra [35] missing [] chev 0 esp 0 fq 0
c02 chemin relatif phr 3 extra [12, 23] missing [] chev 0 esp 0 fq 0
c03 code inline phr 2 extra [21] missing [] chev 0 esp 0 fq 0
c04 identifiant pointé phr 2 extra [20] missing [] chev 0 esp 0 fq 0
a01 abréviation M. phr 2 extra [3] missing [] chev 1 esp 1 fq 0
a02 abréviation Dr. phr 2 extra [7] missing [] chev 1 esp 1 fq 0
a03 etc. minuscule phr 2 extra [29] missing [] chev 1 esp 1 fq 0
a04 etc. majuscule phr 2 extra [] missing [] chev 1 esp 1 fq 0
a05 a
… [1474 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\nimport sys; sys.path.insert(0,'/tmp/frontieres')\nimport bloc_linguistique as bl, corpus, proto, mesure40 as m\nh0=bl.Heuristique(); h=m.HPatchee(**{r:True for r in 'abcdef'})\nfor t in corpus.TEXTES:\n    a0=h0.analyser(t['texte']); a=h.analyser( … [450 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ModuleNotFoundError: No module named 'bloc_linguistique'
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\nimport sys; sys.path.insert(0,'/tmp/frontieres'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport bloc_linguistique as bl, corpus, proto, mesure40 as m\nh0=bl.Heuristique(); h=m.HPatchee(**{r:True for r in 'abcde … [521 caractères tronqués]`

  ```
t01 '# Notes de réunion\n\nLe budget 2025 a été validé.'
  frontières [20]
    ('GP', 8, 29, 'de réunion\n\nLe budget')
t02 '- Priorité : réduire les coûts\n- Échéance : fin mars'
  frontières [31]
    ('GN', 21, 41, 'les coûts\n- Échéance')
  ```

- **bash** `{"command": "cat > /tmp/frontieres/mesure_gold.py <<'PY'\n\"\"\"Mesure dev/test par règle + contrôle négatif sur le gold (612 phrases).\"\"\"\nfrom __future__ import annotations\nimport json\nimport sys\nsys.path.insert(0, \"/tmp/frontieres\")\nsys.path.insert(0, \"/home/stephane/Data13TB/stephane/G … [3367 caractères tronqués]`

  ```
split {'phrases': 422, 'cibles': 163, 'sources': {'hand': 15, 'reel': 302, 'synthetique': 105}, 'langues': {'fr': 277, 'en': 145}} {'phrases': 190, 'cibles': 76, 'sources': {'hand': 5, 'reel': 130, 'synthetique': 55}, 'langues': {'fr': 125, 'en': 65}}
original     dev  POS=0.8375 F1=0.6439 P=0.6703 R=0.6196 att_exact=0.9816 att_top1=0.9816 couv=0.9877 acte=1.0000
original     test POS=0.8400 F1=0.6552 P=0.6710 R=0.6402 att_exact=0.9868 att_top1=0.9868 couv=0.9868 acte=0.9895
             diff 612 : {'pos': 0, 'syn': 0, 'att': 0, 'phr': 0, 'acte': 0}
neutre       dev  POS=0.8375 F1=0.6439 P=0.6703 R=0.6196 att_exact=0.9816 att_top1=0.9816 couv=0.9877 acte=1.0000
neutre       test POS=0.8400 F1=0.6552 P=0.6710 R=0.6402 att_exact=0.9868 att_top1=0.9868 couv=0.9868 acte=0.9895
             diff 612 : {'pos': 0, 'syn': 0, 'att': 0, 'phr': 0, 'acte': 0}
regle_a      dev  POS=0.8375 F1=0.6439 P=0.6703 R=0.6196 att_exact=0.9816 att_top1=0.9816 couv=0.9877 acte=1.0000
regle_a      test POS=0.8400 F1=0.6552 P=0.6710 R=0.6402 att_exact=0.9868 att_top1=0.9868 couv=0.9868 acte=0.9895
             diff 612 : {'pos': 0, 'syn': 0, 'att': 0, 'phr': 0, 'acte': 0}
regle_b      dev  POS=0.8375 F1=0.64
… [1838 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re\nmotif = re.compile(r\"\\b[ldmtsnLDMTNS]['’](?=\\w)|\\w+(?:['’\\-]\\w+)*|\\d+(?:[.,]\\d+)*|https?://\\S+|[\\U0001F300-\\U0001FAFF]|[^\\w\\s]\")\nfor t in ['😊','Merci 😊 !','12.5','https://example.com/a?b=1' … [177 caractères tronqués]`

  ```
'😊' [(0, 1, '😊')]
'Merci 😊 !' [(0, 5, 'Merci'), (6, 7, '😊'), (8, 9, '!')]
'12.5' [(0, 2, '12'), (2, 3, '.'), (3, 4, '5')]
'https://example.com/a?b=1' [(0, 5, 'https'), (5, 6, ':'), (6, 7, '/'), (7, 8, '/'), (8, 15, 'example'), (15, 16, '.'), (16, 19, 'com'), (19, 20, '/'), (20, 21, 'a'), (21, 22, '?'), (22, 23, 'b'), (23, 24, '='), (24, 25, '1')]
'alice@example.org' [(0, 5, 'alice'), (5, 6, '@'), (6, 13, 'example'), (13, 14, '.'), (14, 17, 'org')]
'Heuristique._phrases' [(0, 11, 'Heuristique'), (11, 12, '.'), (12, 20, '_phrases')]
  ```

- **bash** `{"command": "cat > /tmp/frontieres/mots_patch.py <<'PY'\n\"\"\"Patch B (tokénisation) — prototype local, hors dépôt.\"\"\"\nfrom __future__ import annotations\nimport re\n\n_MOTIF_MOTS = re.compile(\n    r\"https?://[^\\s<>\\\"'`]*[^\\s<>\\\"'`.,;:!?]\"          # URL entière (ponctuation finale exc … [2251 caractères tronqués]`

  ```
'Le prix est 12.5 euros.'
   [(0, 2, 'Le', 'mot'), (3, 7, 'prix', 'mot'), (8, 11, 'est', 'mot'), (12, 16, '12.5', 'nombre'), (17, 22, 'euros', 'mot'), (22, 23, '.', 'ponctuation')]
'Rendez-vous le 12.03.2024.'
   [(0, 11, 'Rendez-vous', 'mot'), (12, 14, 'le', 'mot'), (15, 25, '12.03.2024', 'nombre'), (25, 26, '.', 'ponctuation')]
'alice@example.org'
   [(0, 17, 'alice@example.org', 'courriel')]
'https://example.com/docs?page=2'
   [(0, 31, 'https://example.com/docs?page=2', 'url')]
'src/tools/bloc_linguistique.py'
   [(0, 30, 'src/tools/bloc_linguistique.py', 'chemin')]
'Appelez Heuristique._phrases(texte)'
   [(0, 7, 'Appelez', 'mot'), (8, 28, 'Heuristique._phrases', 'mot'), (28, 29, '(', 'ponctuation'), (29, 34, 'texte', 'mot'), (34, 35, ')', 'ponctuation')]
'Use os.path.join ici.'
   [(0, 3, 'Use', 'mot'), (4, 16, 'os.path.join', 'mot'), (17, 20, 'ici', 'mot'), (20, 21, '.', 'ponctuation')]
'Merci 😊 !'
   [(0, 5, 'Merci', 'mot'), (6, 7, '😊', 'emoji'), (8, 9, '!', 'ponctuation')]
'et/ou'
   [(0, 2, 'et', 'mot'), (2, 3, '/', 'chemin'), (3, 5, 'ou', 'mot')]
'Le chat dort.'
   [(0, 2, 'Le', 'mot'), (3, 7, 'chat', 'mot'), (8, 12, 'dort', 'mot'), (12, 13, '.', 'ponctuation')]
'Le lien
… [183 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\np='mots_patch.py'\ns=open(p).read()\ns=s.replace('''    r\"|(?:\\\\\\\\.{0,2}/)?(?:[\\\\\\\\w.@+-]+/)+[\\\\\\\\w.@+-]+\\\\\\\\.(?:[A-Za-z0-9]{1,8})\"  # chemin avec extension''','''    r\"|(?:\\\\\\\\.{0,2}/)?(?:[\\\\\\\\w.@+-]+/)+[\\\\\\\\w.@+-]+ … [999 caractères tronqués]`

  ```
'Le prix est 12.5 euros.'
   [(0, 2, 'Le', 'mot'), (3, 7, 'prix', 'mot'), (8, 11, 'est', 'mot'), (12, 16, '12.5', 'nombre'), (17, 22, 'euros', 'mot'), (22, 23, '.', 'ponctuation')]
'Rendez-vous le 12.03.2024.'
   [(0, 11, 'Rendez-vous', 'mot'), (12, 14, 'le', 'mot'), (15, 25, '12.03.2024', 'nombre'), (25, 26, '.', 'ponctuation')]
'alice@example.org'
   [(0, 17, 'alice@example.org', 'courriel')]
'https://example.com/docs?page=2'
   [(0, 31, 'https://example.com/docs?page=2', 'url')]
'src/tools/bloc_linguistique.py'
   [(0, 30, 'src/tools/bloc_linguistique.py', 'chemin')]
'Appelez Heuristique._phrases(texte)'
   [(0, 7, 'Appelez', 'mot'), (8, 28, 'Heuristique._phrases', 'mot'), (28, 29, '(', 'ponctuation'), (29, 34, 'texte', 'mot'), (34, 35, ')', 'ponctuation')]
'Use os.path.join ici.'
   [(0, 3, 'Use', 'mot'), (4, 16, 'os.path.join', 'mot'), (17, 20, 'ici', 'mot'), (20, 21, '.', 'ponctuation')]
'Merci 😊 !'
   [(0, 5, 'Merci', 'mot'), (6, 7, '😊', 'emoji'), (8, 9, '!', 'ponctuation')]
'et/ou'
   [(0, 2, 'et', 'mot'), (2, 3, '/', 'ponctuation'), (3, 5, 'ou', 'mot')]
'Le chat dort.'
   [(0, 2, 'Le', 'mot'), (3, 7, 'chat', 'mot'), (8, 12, 'dort', 'mot'), (12, 13, '.', 'ponctuation')]
'Le
… [188 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/frontieres/mesure_mots.py <<'PY'\n\"\"\"Mesure du patch B (tokénisation) seul et combiné au patch A (frontières).\"\"\"\nfrom __future__ import annotations\nimport json\nimport sys\nsys.path.insert(0, \"/tmp/frontieres\")\nsys.path.insert(0, \"/home/stephane/Data13TB/stephane … [5053 caractères tronqués]`

  ```
== 40 textes : patch B ==
original {"tokens": 477, "types": {"mot": 273, "ponctuation": 171, "nombre": 33}, "pos": 273, "pos_diff_textes": 0, "pos_perdus": 0, "pos_gagnes": 0, "syn_diff_textes": 0, "syn_labels": 176, "att_diff_textes": 0, "phr": 102, "unites": 172, "fraction": 21.728700000000003, "zones_pos_avant": 47, "tokens_par_texte": 11.93, "fraction_moyenne": 0.5432}
mots {"tokens": 362, "types": {"mot": 232, "ponctuation": 107, "nombre": 14, "url": 5, "courriel": 2, "chemin": 2}, "pos": 232, "pos_diff_textes": 10, "pos_perdus": 44, "pos_gagnes": 3, "syn_diff_textes": 7, "syn_labels": 173, "att_diff_textes": 7, "phr": 102, "unites": 133, "fraction": 19.0148, "zones_pos_avant": 47, "tokens_par_texte": 9.05, "fraction_moyenne": 0.4754}
complet {"tokens": 362, "types": {"mot": 232, "ponctuation": 107, "nombre": 14, "url": 5, "courriel": 2, "chemin": 2}, "pos": 232, "pos_diff_textes": 10, "pos_perdus": 44, "pos_gagnes": 3, "syn_diff_textes": 7, "syn_labels": 173, "att_diff_textes": 7, "phr": 59, "unites": 133, "fraction": 19.0148, "zones_pos_avant": 47, "tokens_par_texte": 9.05, "fraction_moyenne": 0.4754}

== gold : patch B ==
mots tokens_diff_textes: 0 exemples: []
  dev: POS=0
… [311 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\nimport sys; sys.path.insert(0,'/tmp/frontieres'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport bloc_linguistique as bl, corpus, mots_patch, mesure_mots as mm\nh0=bl.Heuristique(); hb=mm.HMots()\nfor t in corpu … [675 caractères tronqués]`

  ```
u01 'Visitez https://example.com/docs?page=2 pour la documentation.'
  perdu: [('GV', 8, 13, 'https'), ('GV', 28, 32, 'docs')]
  gagne: []

 u02 'Le lien est https://example.com/a.b?x=1. Cliquez ensuite sur « Connexion ».'
  perdu: [('GV', 32, 33, 'a')]
  gagne: [('GV', 8, 11, 'est')]

 e01 'Écrivez à alice@example.org avant vendredi.'
  perdu: [('GP', 8, 15, 'à alice')]
  gagne: [('GP', 8, 9, 'à')]

 e02 'Contactez support@exemple.fr ou ouvrez https://exemple.fr/aide?lang=fr.'
  perdu: []
  gagne: [('GV', 32, 38, 'ouvrez')]

 c01 'Ouvrez src/tools/bloc_linguistique.py puis cherchez `_phrases`.'
  perdu: [('GV', 0, 10, 'Ouvrez src'), ('GV', 11, 16, 'tools'), ('GV', 38, 51, 'puis cherchez')]
  gagne: [('GV', 0, 6, 'Ouvrez'), ('GV', 43, 51, 'cherchez')]
POS gagnes c01 [(38, 42, 'NOUN')]
POS gagnes c03 [(9, 29, 'NOUN')]
POS gagnes c04 [(8, 28, 'NOUN')]

 u03 "Voir la page (https://example.com/a?b=1) pour plus d'informations."
  perdu: [('GV', 34, 35, 'a')]
  gagne: []

 u04 'Visitez https://example.com?q=1. Que voyez-vous ?'
  perdu: [('GV', 8, 13, 'https')]
  gagne: [('REL', 33, 47, 'Que voyez-vous')]
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\nimport json, mesure40 as m\nr=m.mesurer_40()\norig=r['original']['textes']\nbyid={x['id']:x for x in orig}\nprint('rule, exacts, sans_frontiere_fausse, repares_frontiere, repares_exact, extra, missing, chev, fq, leading, phrases')\nfor nom,d in r. … [1063 caractères tronqués]`

  ```
rule, exacts, sans_frontiere_fausse, repares_frontiere, repares_exact, extra, missing, chev, fq, leading, phrases
original    2  8  0  0 47  4  9  5 31 102
neutre      2 13  5  0 45  2  0  5 31 102
regle_a     6 19 11  4 30  2  0  5 29  87
regle_b     8 20 12  6 35  2  0  5 21  92
regle_c    10 23 15  8 26  2  0  0 31  83
regle_d     3 14  6  1 44  2  0  5 30 101
regle_e    13 13  5 11 45  2  0  5  0 102
regle_f     4 15  7  2 45  0  0  5 30 104
toutes     40 40 32 38  0  0  0  0  0  59
Counter({'extra': 27, 'leading': 24, 'overlaps': 9, 'fq': 5, 'missing': 4})
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\nimport sys; sys.path.insert(0,'/tmp/frontieres'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport bloc_linguistique as bl, corpus, proto\nfor tid in ['d03','u01','a01','a03','a04','g01','t01','t03','x01','d05','u … [389 caractères tronqués]`

  ```
d03 'La réunion du 12.03.2024 a été reportée au 15.04.2024.'
  attendu [(0, 54)] ['La réunion du 12.03.2024 a été reportée au 15.04.2024.']
  avant   [(0, 17, 'La réunion du 12.', 'déclarative'), (17, 20, '03.', 'déclarative'), (20, 46, '2024 a été reportée au 15.', 'déclarative'), (46, 49, '04.', 'déclarative'), (49, 54, '2024.', 'déclarative')]
  apres   [(0, 54, 'La réunion du 12.03.2024 a été reportée au 15.04.2024.', 'déclarative')]

 u01 'Visitez https://example.com/docs?page=2 pour la documentation.'
  attendu [(0, 62)] ['Visitez https://example.com/docs?page=2 pour la documentation.']
  avant   [(0, 24, 'Visitez https://example.', 'déclarative'), (24, 33, 'com/docs?', 'interrogative'), (33, 62, 'page=2 pour la documentation.', 'déclarative')]
  apres   [(0, 62, 'Visitez https://example.com/docs?page=2 pour la documentation.', 'déclarative')]

 a01 'M. Dupont, le directeur, a annoncé sa retraite.'
  attendu [(0, 47)] ['M. Dupont, le directeur, a annoncé sa retraite.']
  avant   [(0, 47, 'M. Dupont, le directeur, a annoncé sa retraite.', 'déclarative'), (2, 47, ' Dupont, le directeur, a annoncé sa retraite.', 'déclarative')]
  apres   [(0, 47, 'M. Dupont, le directeur, a anno
… [2837 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Finalisation des deux patchs et test sur le gold

- **bash** `{"command": "mkdir -p /tmp/frontieres/final && cat > /tmp/frontieres/final/patch_frontieres.py <<'PY'\n# --------------------------------------------------------------------------- frontières de phrase\n# P0-4 : un point décimal, une URL, un courriel, un chemin, une abréviation, un numéro de\n# list … [12472 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ModuleNotFoundError: No module named 'corpus'
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport sys; sys.path.insert(0,'/tmp/frontieres/final'); sys.path.insert(0,'/tmp/frontieres'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport bloc_linguistique as bl, corpus, patch_frontieres, patch_mots\np … [556 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/tmp/frontieres/final/patch_frontieres.py", line 27, in <module>
    _MARQUEUR = re.compile(
                ^^
NameError: name 're' is not defined. Did you forget to import 're'?
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && sed -i '1i import re  # retiré à l’insertion : bloc_linguistique.py importe déjà re' patch_frontieres.py patch_mots.py && python3 - <<'PY'\nimport sys; sys.path.insert(0,'/tmp/frontieres/final'); sys.path.insert(0,'/tmp/frontieres'); sys.path.insert(0,'/home/ … [678 caractères tronqués]`

  ```
phrases 40: 59
mots 40: 362
'Le chat dort.' [(0, 13, 'Le chat dort.', 'déclarative')] [(0, 2, 'Le', 'mot'), (3, 7, 'chat', 'mot'), (8, 12, 'dort', 'mot'), (12, 13, '.', 'ponctuation')]
'Il part. Elle reste.' [(0, 8, 'Il part.', 'déclarative'), (9, 20, 'Elle reste.', 'déclarative')] [(0, 2, 'Il', 'mot'), (3, 7, 'part', 'mot'), (7, 8, '.', 'ponctuation'), (9, 13, 'Elle', 'mot'), (14, 19, 'reste', 'mot'), (19, 20, '.', 'ponctuation')]
'M. Dupont…' [(0, 10, 'M. Dupont…', 'déclarative')] [(0, 1, 'M', 'mot'), (1, 2, '.', 'ponctuation'), (3, 9, 'Dupont', 'mot'), (9, 10, '…', 'ponctuation')]
'12.5' [(0, 4, '12.5', 'déclarative')] [(0, 4, '12.5', 'nombre')]
'alice@example.org' [(0, 17, 'alice@example.org', 'déclarative')] [(0, 17, 'alice@example.org', 'courriel')]
'https://example.com/a?b=1' [(0, 25, 'https://example.com/a?b=1', 'déclarative')] [(0, 25, 'https://example.com/a?b=1', 'url')]
'src/tools/bloc_linguistique.py' [(0, 30, 'src/tools/bloc_linguistique.py', 'déclarative')] [(0, 30, 'src/tools/bloc_linguistique.py', 'chemin')]
'Heuristique._phrases' [(0, 20, 'Heuristique._phrases', 'déclarative')] [(0, 20, 'Heuristique._phrases', 'mot')]
'Merci 😊 !' [(0, 9, 'Merci 😊 !', 'exclamative')
… [188 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/frontieres/final/verifier.py <<'PY'\nimport sys\nsys.path.insert(0, \"/tmp/frontieres/final\")\nsys.path.insert(0, \"/tmp/frontieres\")\nsys.path.insert(0, \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools\")\nsys.path.insert(0, \"/home/stephane/Data13TB/stephane/GitHub … [1459 caractères tronqués]`

  ```
40 textes exacts: 40
A dev 0.8375 0.6439 0.9816 1.0
A test 0.84 0.6552 0.9868 0.9895
B dev 0.8375 0.6439 0.9816 1.0
B test 0.84 0.6552 0.9868 0.9895
AB dev 0.8375 0.6439 0.9816 1.0
AB test 0.84 0.6552 0.9868 0.9895
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _type_phrase\\|def decouper_phrases\\|def decouper_mots\\|_FERMANTS\\|_TITRES\\|_DEBUTS\\|_MARQUEUR\\|_ZONES\" tools/bloc_linguistique.py | head -20", "description": "Check helper name collisions"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport pathlib, re\nsrc = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py').read_text(encoding='utf-8')\na = pathlib.Path('patch_frontieres.py').read_text(encoding='utf-8')\nb = pathlib.Path('patch_mo … [1697 caractères tronqués]`

  ```
écrit 130879 octets
SYNTAXE_OK
diff exit 1
336 patch_complet.diff
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -551,6 +551,286 @@
 # --------------------------------------------------------------------------- heuristique
 
 
+# --------------------------------------------------------------------------- frontières de phrase
+# P0-4 : un point décimal, une URL, un courriel, un chemin, une abréviation, un numéro de
+# liste ou une ponctuation répétée ne coupent pas la phrase ; un saut de ligne structurel
+# la coupe. Le balayage est **unique** : aucun span ne se chevauche, aucune phrase vide.
+_FERMANTS = "»”’)]}›"
+_OUVRANTS = "«“‘([{‹"
+_TITRES = frozenset({
+    "M", "MM", "Mme", "Mmes", "Mlle", "Mlles", "Me", "Mgr", "St", "Ste",
+    "Dr", "Drs", "Pr", "Prs", "Rév", "Père", "Sr", "Sœur",
+})
+_ABREV_TOUJOURS = frozenset({
+    "cf", "p", "pp", "ex", "réf", "ref", "éd", "ed", "trad", "fig", "chap",
+    "sect", "env", "av", "al", "ibid", "id", "infra", "supra", "coll", "pl",
+    "sq", "suiv", "op", "ca", "n", "no", "nos", "vs", "art", "vol",
+})
+_ABREV_MINUSCULE = frozenset({"etc"})
+# après un titre ou une initiale, ces mots ouvrent presque sûrement une p
… [909 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && grep -n \"^@@\\|^---\\|^+++\" patch_complet.diff && sed -n '250,336p' patch_complet.diff", "description": "Inspect diff hunks and method replacements"}`

  ```
1:--- a/tools/bloc_linguistique.py
2:+++ b/tools/bloc_linguistique.py
3:@@ -551,6 +551,286 @@
290:@@ -576,44 +856,11 @@
+    r"|\b[A-Za-z_]\w*(?:\.[a-z_]\w*){2,}\b|\b[A-Za-z_]\w*\.[_]\w*\b"
+    r"|\d+(?:[.,]\d+)*"
+    r"|\b[ldmtsnLDMTNS]['’](?=\w)"
+    r"|\w+(?:['’\-]\w+)*"
+    r"|[\U0001F300-\U0001FAFF]"
+    r"|[^\w\s]",
+    re.I,
+)
+_DOMAINE_SEUL = re.compile(
+    r"(?:[\w-]+\.)+(?:com|org|net|fr|io|dev|ai|edu|gov|co|uk|de|ch|be|ca|info|eu)", re.I)
+
+
+def decouper_mots(texte: str) -> list[tuple[int, int, str, str]]:
+    """Les tokens du bloc : la surface, son span et son type, sans recouvrement."""
+    sortie: list[tuple[int, int, str, str]] = []
+    for m in _MOTIF_MOTS.finditer(texte):
+        t = m.group()
+        if t.startswith(("http://", "https://")):
+            typ = "url"
+        elif re.fullmatch(r"[\w.+-]+@[\w-]+(?:\.[A-Za-z]{2,})+", t):
+            typ = "courriel"
+        elif _DOMAINE_SEUL.fullmatch(t):
+            typ = "url"
+        elif re.fullmatch(r"\d+(?:[.,]\d+)*", t):
+            typ = "nombre"
+        elif len(t) == 1 and ord(t) >= 0x1F300:
+            typ = "emoji"
+        elif re.fullmatch(r"[^\w\s]", t):
+            typ = "ponc
… [2345 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Heuristique\\|def _mots\\|def _phrases\\|def _negation\" tools/bloc_linguistique.py | head && wc -l tools/bloc_linguistique.py && sed -n '545,560p' tools/bloc_linguistique.py", "description": "Recheck current line num … [6 caractères tronqués]`

  ```
554:class Heuristique:
578:    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
597:    def _phrases(texte: str) -> list[tuple[int, int, str, str]]:
619:    def _negation(phrase: str) -> bool:
2273 tools/bloc_linguistique.py
        return "destinataire"
    if p in {"de", "du", "des", "of", "from"}:
        return "theme"
    return "complément"


# --------------------------------------------------------------------------- heuristique


class Heuristique:
    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""

    nom = "heuristique"

    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/bloc_linguistique.py && git diff --stat -- tools/bloc_linguistique.py && git diff -- tools/bloc_linguistique.py | head -120", "description": "Check concurrent changes to target file"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format='%H %ad %s' && git status --short | head -5 && git rev-parse HEAD", "description": "Check HEAD movement"}`

  ```
e8d746e2593abf509130722fb97ba60fb7e757a7 Fri Nov 6 19:35:27 2026 -0500 B13 — LA MORPHOLOGIE DU 1ER GROUPE : 10 SPANS RETROUVÉS, EXACT 235/236, COUVERTURE 0,9874, 3 SPANS ; 183/183
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
e8d746e2593abf509130722fb97ba60fb7e757a7
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -3 --format='%h %ad %s' -- tools/bloc_linguistique.py && sha256sum tools/bloc_linguistique.py && git log -1 --format='%h' -- tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/tests/linguistique/ … [76 caractères tronqués]`

  ```
e8d746e2 Fri Nov 6 19:35:27 2026 -0500 B13 — LA MORPHOLOGIE DU 1ER GROUPE : 10 SPANS RETROUVÉS, EXACT 235/236, COUVERTURE 0,9874, 3 SPANS ; 183/183
e6fad714 Fri Nov 6 18:52:14 2026 -0500 POS — DEUX AJOUTS DE LEXIQUE GÉNÉRAUX (acheter, élision qu'il) ; 183/183
037fe041 Fri Nov 6 18:14:19 2026 -0500 PRODUIT — LE CONTRAT V1 : schema/version, REFUS EN JSON (CODE 3), SURROGATE ET NON-STR TOLÉRÉS ; PORTE À 8 CONTRÔLES ; 183/183
dd0e5e47d522c6a1a1adb799cfa727c54d43b569d542bc2fc9166ae74992d346  tools/bloc_linguistique.py
c5b80dd8
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git apply --check /tmp/frontieres/final/patch_complet.diff && echo APPLY_OK", "description": "Verify patch applies cleanly without modifying"}`

  ```
APPLY_OK
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport sys; sys.path.insert(0,'/tmp/frontieres/final'); sys.path.insert(0,'/tmp/frontieres'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tool … [917 caractères tronqués]`

  ```
r308 'Marie lit. Elle aime les livres.'
  avant [(0, 10, 'déclarative'), (10, 32, 'déclarative')] ['assertion', 'assertion']
  apres [(0, 10, 'déclarative'), (11, 32, 'déclarative')] ['assertion', 'assertion']
r318 'Marie reads. She loves books.'
  avant [(0, 12, 'déclarative'), (12, 29, 'déclarative')] ['assertion', 'assertion']
  apres [(0, 12, 'déclarative'), (13, 29, 'déclarative')] ['assertion', 'assertion']
  ```

- **bash** `{"command": "cat > /tmp/frontieres/final/mesure_final.py <<'PY'\n\"\"\"Mesures consolidées P0-4 — patchs finaux, 40 textes + gold dev/test.\"\"\"\nfrom __future__ import annotations\nimport hashlib\nimport json\nimport pathlib\nimport sys\n\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/G … [12860 caractères tronqués]`

  ```
{
 "commit": "e8d746e2593abf509130722fb97ba60fb7e757a7",
 "module_sha256": "dd0e5e47d522c6a1a1adb799cfa727c54d43b569d542bc2fc9166ae74992d346",
 "quarante": "...",
 "ablations": "...",
 "gold": "...",
 "tokens": "..."
}
40 avant {'phrases': 102, 'textes_exacts': 2, 'textes_frontiere_fausse': 32, 'textes_casses': 38, 'extra': 47, 'missing': 4, 'overlaps': 9, 'leading': 31, 'vides': 0, 'fausses_questions': 5, 'types_faux': 63}
40 apres {'phrases': 59, 'textes_exacts': 40, 'textes_frontiere_fausse': 0, 'textes_casses': 0, 'extra': 0, 'missing': 0, 'overlaps': 0, 'leading': 0, 'vides': 0, 'fausses_questions': 0, 'types_faux': 0}
ablations {
 "original": {
  "phrases": 102,
  "textes_exacts": 2,
  "textes_sans_frontiere_fausse": 8,
  "textes_sans_defaut": 2,
  "extra": 47,
  "missing": 4,
  "overlaps": 9,
  "leading": 31,
  "fausses_questions": 5
 },
 "neutre": {
  "phrases": 102,
  "textes_exacts": 2,
  "textes_sans_frontiere_fausse": 13,
  "textes_sans_defaut": 2,
  "extra": 45,
  "missing": 2,
  "overlaps": 0,
  "leading": 31,
  "fausses_questions": 5
 },
 "regle_a": {
  "phrases": 87,
  "textes_exacts": 6,
  "textes_sans_frontiere_fausse": 19,
  "textes_sans_defaut": 6,
  "extra": 30
… [3231 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres && python3 - <<'PY'\nimport json\ng=json.load(open('gold_resultats.json'))\nfor nom,d in g.items():\n    print(nom, 'diff', d['diff_vs_original'])\n    for sp in ('dev','test'):\n        x=d[sp]\n        print(' ',sp, 'POS',x['pos']['exactitude'],'F1',x['syntagme']['f … [418 caractères tronqués]`

  ```
original diff {'pos': 0, 'syn': 0, 'att': 0, 'phr': 0, 'acte': 0}
  dev POS 0.8375 F1 0.6439 P 0.6703 R 0.6196 att_exact 0.9816 att_top1 0.9816 att_topk 0.9816 couv 0.9877 acte 1.0 neg 0.9787 mod 0.9929
  test POS 0.84 F1 0.6552 P 0.671 R 0.6402 att_exact 0.9868 att_top1 0.9868 att_topk 0.9737 couv 0.9868 acte 0.9895 neg 0.9737 mod 0.9789
neutre diff {'pos': 0, 'syn': 0, 'att': 0, 'phr': 0, 'acte': 0}
  dev POS 0.8375 F1 0.6439 P 0.6703 R 0.6196 att_exact 0.9816 att_top1 0.9816 att_topk 0.9816 couv 0.9877 acte 1.0 neg 0.9787 mod 0.9929
  test POS 0.84 F1 0.6552 P 0.671 R 0.6402 att_exact 0.9868 att_top1 0.9868 att_topk 0.9737 couv 0.9868 acte 0.9895 neg 0.9737 mod 0.9789
regle_a diff {'pos': 0, 'syn': 0, 'att': 0, 'phr': 0, 'acte': 0}
  dev POS 0.8375 F1 0.6439 P 0.6703 R 0.6196 att_exact 0.9816 att_top1 0.9816 att_topk 0.9816 couv 0.9877 acte 1.0 neg 0.9787 mod 0.9929
  test POS 0.84 F1 0.6552 P 0.671 R 0.6402 att_exact 0.9868 att_top1 0.9868 att_topk 0.9737 couv 0.9868 acte 0.9895 neg 0.9737 mod 0.9789
regle_b diff {'pos': 0, 'syn': 0, 'att': 0, 'phr': 0, 'acte': 0}
  dev POS 0.8375 F1 0.6439 P 0.6703 R 0.6196 att_exact 0.9816 att_top1 0.9816 att_topk 0.9816 couv 0.9877 acte 1.0 
… [1858 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport pathlib\nracine = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsrc = (racine/'tools/bloc_linguistique.py').read_text(encoding='utf-8')\na = pathlib.Path('patch_frontieres.py').read_text(encoding='utf-8').replace('i … [1862 caractères tronqués]`

  ```
ok
  269 patch_A.diff
   80 patch_B.diff
  336 patch_complet.diff
  685 total
A_OK
B_OK
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 -m py_compile bloc_linguistique_A.py bloc_linguistique_B.py && echo SYNTAX_OK && grep -n \"^@@\\|^---\\|^+++\" patch_A.diff patch_B.diff", "description": "Syntax-check separate patched copies"}`

  ```
SYNTAX_OK
patch_A.diff:1:--- a/tools/bloc_linguistique.py
patch_A.diff:2:+++ b/tools/bloc_linguistique.py
patch_A.diff:3:@@ -551,6 +551,239 @@
patch_A.diff:243:@@ -595,25 +828,7 @@
patch_B.diff:1:--- a/tools/bloc_linguistique.py
patch_B.diff:2:+++ b/tools/bloc_linguistique.py
patch_B.diff:3:@@ -551,6 +551,53 @@
patch_B.diff:57:@@ -576,22 +623,7 @@
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport sys, time, random, string\nsys.path.insert(0,'/tmp/frontieres/final'); sys.path.insert(0,'/tmp/frontieres'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport bloc_linguistique as bl, patch_frontieres, … [1727 caractères tronqués]`

  ```
baseline phrases 923 temps 2.98 ms
patch phrases 462 temps 8.47 ms
fuzz 500 OK
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport sys,time\nsys.path.insert(0,'/tmp/frontieres/final'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport bloc_linguistique as bl, patch_mots\nbase=\"Le chat dort. https://example.com/a?b=1 alice@example … [289 caractères tronqués]`

  ```
baseline 4101 12.96 ms
patch 1029 8.97 ms
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport sys; sys.path.insert(0,'/tmp/frontieres/final'); sys.path.insert(0,'/tmp/frontieres'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport bloc_linguistique as bl, corpus, patch_frontieres\nclass HA(bl.H … [598 caractères tronqués]`

  ```
textes discours differents 5
u01 ([(0, 62, 'paragraphe', 'suite'), (33, 62, 'connecteur', 'pour')], [(0, 62, 'connecteur', 'pour'), (0, 62, 'paragraphe', 'suite')])
a05 ([(0, 31, 'connecteur', 'pour'), (0, 31, 'paragraphe', 'suite'), (3, 31, 'connecteur', 'pour')], [(0, 31, 'connecteur', 'pour'), (0, 31, 'paragraphe', 'suite')])
en02 ([(0, 37, 'paragraphe', 'suite'), (16, 37, 'connecteur', 'to')], [(0, 37, 'connecteur', 'to'), (0, 37, 'paragraphe', 'suite')])
u03 ([(0, 66, 'paragraphe', 'suite'), (36, 66, 'connecteur', 'pour')], [(0, 66, 'connecteur', 'pour'), (0, 66, 'paragraphe', 'suite')])
u04 ([(0, 49, 'paragraphe', 'suite'), (32, 49, 'connecteur', 'que')], [(0, 49, 'paragraphe', 'suite'), (33, 49, 'connecteur', 'que')])
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i \"fronti\\|pensee-front\" || true && git status --short reports/ | grep -i \"fronti\" || true", "description": "Check target report names are free"}`

  ```
pensee-frontiere-71.json
rapport-loi-frontiere-fenetre.md
rapport-pensee-frontiere-71.md
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && ls -lh mesures.json patch_A.diff patch_B.diff patch_complet.diff && python3 - <<'PY'\nimport json\nm=json.load(open('mesures.json'))\nprint(m.keys())\nprint('quarante keys',m['quarante'].keys(), len(m['quarante']['detail']['avant']))\nprint('gold keys',m['gol … [134 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane  92K  6 nov 19:43 mesures.json
-rw-r--r--. 1 stephane stephane  11K  6 nov 19:45 patch_A.diff
-rw-r--r--. 1 stephane stephane 3,3K  6 nov 19:45 patch_B.diff
-rw-r--r--. 1 stephane stephane  14K  6 nov 19:37 patch_complet.diff
dict_keys(['commit', 'module_sha256', 'quarante', 'ablations', 'gold', 'tokens'])
quarante keys dict_keys(['detail', 'totaux']) 40
gold keys dict_keys(['split', 'mesures']) dict_keys(['original', 'patch_a', 'patch_b', 'patch_ab'])
tokens dict_keys(['original', 'patch_b', 'patch_ab', 'zones_pos_avant'])
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"mot\\|type\\|url\\|emoji\\|courriel\\|chemin\" docs/produit/schema-v1.json 2>/dev/null | head -40 && sed -n '1,80p' docs/produit/schema-v1.json 2>/dev/null", "description": "Check schema constraints on token types"}`

  ```
(no output)
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls docs/produit 2>/dev/null | head && find . -name \"schema-v1.json\" -not -path \"./.git/*\" 2>/dev/null | head", "description": "Locate schema v1"}`

  ```
exemples.md
README.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"courriel\\|chemin\\|\\\"url\\\"\\|'url'\\|emoji\" tools/*.py docs/produit/*.md | head -40", "description": "Check token type expectations"}`

  ```
tools/adaptateur_langue.py:111:    def encoder(chemin):
tools/adaptateur_langue.py:112:        texte = pathlib.Path(chemin).read_text(errors="ignore")
tools/aiguille.py:32:    aiguille.py /chemin/gpt-oss-120b-MXFP4.gguf 4096 0.1,0.5,0.9 --lot 512 --gpu
tools/aiguille.py:111:        # Le moteur n'a pas démarré (chemin de modèle, option refusée…) : le
tools/aligneur_litteraire.py:346:def lire_gutenberg(chemin: Path) -> str:
tools/aligneur_litteraire.py:348:    brut = chemin.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
tools/aligneur_litteraire.py:530:            raise RuntimeError(f"chemin d'alignement interrompu en ({i}, {j})")
tools/aligneur_litteraire.py:999:def rediger_rapport(donnees: dict, chemin: Path) -> None:
tools/aligneur_litteraire.py:1460:    chemin.parent.mkdir(parents=True, exist_ok=True)
tools/aligneur_litteraire.py:1461:    chemin.write_text("\n".join(L) + "\n", encoding="utf-8")
tools/analyse_empreinte.py:34:def charge(chemin, limite=None):
tools/analyse_empreinte.py:36:    for ligne in open(chemin):
tools/analyse_engram.py:25:def lire(chemin):
tools/analyse_engram.py:26:    with open(chemin, "rb") as f:
tools/analyse_experts_statique.py
… [1970 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport importlib.util, sys\nspec=importlib.util.spec_from_file_location('bl_patche','/tmp/frontieres/final/bloc_linguistique_patche.py')\nmod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)\nh=mod.Heuristique(segmenter_s= … [507 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/tmp/frontieres/final/bloc_linguistique_patche.py", line 58, in <module>
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

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport importlib.util, sys\nspec=importlib.util.spec_from_file_location('bl_patche','/tmp/frontieres/final/bloc_linguistique_patche.py')\nmod=importlib.util.module_from_spec(spec); sys.modules['bl_patche']=mod; spec.loader.exec_module(mod)\n … [556 caractères tronqués]`

  ```
'Le prix est 12.5 euros.' [(0, 23, 'déclarative', 'type')]
'Visitez https://example.com/docs?page=2' [(0, 39, 'déclarative', 'type')]
'M. Dupont…' [(0, 10, 'déclarative', 'type')]
'Il part. Elle reste.' [(0, 8, 'déclarative', 'type'), (9, 20, 'déclarative', 'type')]
'« Bonjour. » Elle part.' [(0, 12, 'déclarative', 'type'), (13, 23, 'déclarative', 'type')]
'# Notes\n\nUn texte.' [(0, 7, 'déclarative', 'type'), (9, 18, 'déclarative', 'type')]
'1. Ouvrir.\n2. Lire.' [(0, 10, 'déclarative', 'type'), (11, 19, 'déclarative', 'type')]
module patché OK
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport sys; sys.path.insert(0,'/tmp/frontieres/final'); sys.path.insert(0,'/tmp/frontieres'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport bloc_linguistique as bl, patch_frontieres\ncas = [\n (\"Il part. … [834 caractères tronqués]`

  ```
OK 2 2 'Il part. Elle reste.' ['Il part.', 'Elle reste.']
OK 3 3 'Il part. Elle reste. Nous attendons.' ['Il part.', 'Elle reste.', 'Nous attendons.']
OK 2 2 'Il hésite... Elle part.' ['Il hésite...', 'Elle part.']
OK 1 1 'Il hésite... puis il part.' ['Il hésite... puis il part.']
OK 2 2 'M. Dupont est là. Il part.' ['M. Dupont est là.', 'Il part.']
OK 2 2 'Le Dr. Martin arrive. Il repart.' ['Le Dr. Martin arrive.', 'Il repart.']
OK 2 2 'Il consulte le Dr. Elle est partie.' ['Il consulte le Dr.', 'Elle est partie.']
OK 2 2 'Il a vu le Dr. Puis il part.' ['Il a vu le Dr.', 'Puis il part.']
OK 2 2 'des pommes, etc. Il part.' ['des pommes, etc.', 'Il part.']
OK 1 1 'des pommes, etc. et des poires.' ['des pommes, etc. et des poires.']
OK 2 2 'Le prix est 12.5. Il part.' ['Le prix est 12.5.', 'Il part.']
OK 2 2 'Rendez-vous le 12.03.2024. Il part.' ['Rendez-vous le 12.03.2024.', 'Il part.']
OK 2 2 'Visitez https://example.com?q=1. Que voyez-vous ?' ['Visitez https://example.com?q=1.', 'Que voyez-vous ?']
OK 2 2 '« Bonjour. » Elle part.' ['« Bonjour. »', 'Elle part.']
OK 1 1 'M. Dupont…' ['M. Dupont…']
OK 2 2 'Il part. Elle reste. ' ['Il part.', 'Elle reste.']
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport sys; sys.path.insert(0,'/tmp/frontieres/final'); sys.path.insert(0,'/tmp/frontieres'); sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport bloc_linguistique as bl, corpus, patch_frontieres\nclass HA(bl.H … [802 caractères tronqués]`

  ```
avant 102 63
apres 59 0
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport json\nm=json.load(open('mesures.json'))\na=m['quarante']['detail']['avant']\nprint('textes leading',sum(1 for x in a if x['leading']))\nprint('phrases leading',sum(len(x['leading']) for x in a))\nprint('textes extra',sum(1 for x in a  … [383 caractères tronqués]`

  ```
textes leading 24
phrases leading 31
textes extra 27
textes missing 4
textes overlaps 9
textes fq 5
textes frontiere fausse 32
textes casses 38
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && sed -n '1,20p' patch_A.diff && echo '...' && sed -n '235,280p' patch_A.diff && echo '===== B =====' && sed -n '1,90p' patch_B.diff", "description": "Inspect patch diffs formatting"}`

  ```
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -551,6 +551,239 @@
 # --------------------------------------------------------------------------- heuristique
 
 
+# --------------------------------------------------------------------------- frontières de phrase
+# P0-4 : un point décimal, une URL, un courriel, un chemin, une abréviation, un numéro de
+# liste ou une ponctuation répétée ne coupent pas la phrase ; un saut de ligne structurel
+# la coupe. Le balayage est **unique** : aucun span ne se chevauche, aucune phrase vide.
+_FERMANTS = "»”’)]}›"
+_OUVRANTS = "«“‘([{‹"
+_TITRES = frozenset({
+    "M", "MM", "Mme", "Mmes", "Mlle", "Mlles", "Me", "Mgr", "St", "Ste",
+    "Dr", "Drs", "Pr", "Prs", "Rév", "Père", "Sr", "Sœur",
+})
+_ABREV_TOUJOURS = frozenset({
+    "cf", "p", "pp", "ex", "réf", "ref", "éd", "ed", "trad", "fig", "chap",
+    "sect", "env", "av", "al", "ibid", "id", "infra", "supra", "coll", "pl",
+    "sq", "suiv", "op", "ca", "n", "no", "nos", "vs", "art", "vol",
...
+        i = j
+    ajouter(n, "déclarative")
+    return sortie
+
+
 class Heuristique:
     """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couv
… [4477 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && sed -i 's/if t.startswith((\"http:\\/\\/\", \"https:\\/\\/\")):/if t.lower().startswith((\"http:\\/\\/\", \"https:\\/\\/\")):/' patch_mots.py && grep -n \"startswith\" patch_mots.py && python3 - <<'PY'\nimport pathlib\nracine = pathlib.Path('/home/stephane/Da … [2288 caractères tronqués]`

  ```
29:        if t.lower().startswith(("http://", "https://")):
ok
APPLY_OK
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 verifier.py && python3 mesure_final.py | tail -20", "description": "Re-run verification and final measurements"}`

  ```
40 textes exacts: 40
A dev 0.8375 0.6439 0.9816 1.0
A test 0.84 0.6552 0.9868 0.9895
B dev 0.8375 0.6439 0.9816 1.0
B test 0.84 0.6552 0.9868 0.9895
AB dev 0.8375 0.6439 0.9816 1.0
AB test 0.84 0.6552 0.9868 0.9895
   "mot": 232,
   "ponctuation": 107,
   "nombre": 14,
   "url": 5,
   "courriel": 2,
   "chemin": 2
  },
  "pos": 232,
  "syn": 173,
  "phr": 59,
  "pos_diff_textes": 10,
  "pos_perdus": 44,
  "pos_gagnes": 3,
  "syn_diff_textes": 7,
  "att_diff_textes": 7,
  "unites": 133,
  "fraction_moyenne": 0.4754
 },
 "zones_pos_avant": 47
}
  ```

- **bash** `{"command": "cd /tmp/frontieres/final && python3 - <<'PY'\nimport json\nm=json.load(open('mesures.json'))['quarante']['detail']['avant']\nprint('leading only:',[x['id'] for x in m if x['leading'] and not x['frontiere_fausse']])\nprint('false+leading:',[x['id'] for x in m if x['leading'] and x['front … [208 caractères tronqués]`

  ```
leading only: ['n01', 'n02', 'x02', 'x03', 's02', 's03']
false+leading: ['u02', 'a01', 'a02', 'a03', 'a04', 'a05', 'a06', 'a07', 'a08', 't03', 'g01', 'g02', 'x01', 'en01', 'en02', 'en03', 'd05', 'u04']
Counter({'négatif': 2, 'décimal': 1, 'décimal+milliers': 1, 'date': 1, 'version+IP': 1, 'URL+query': 1, 'URL+phrase': 1, 'courriel': 1, 'courriel+URL': 1, 'chemin+code': 1, 'chemin relatif': 1, 'code inline': 1, 'identifiant pointé': 1, 'abréviation M.': 1, 'abréviation Dr.': 1, 'etc. minuscule': 1, 'etc. majuscule': 1, 'abréviation cf.': 1, 'abréviation p. ex.': 1, 'initiales': 1, 'titre en fin de phrase': 1, 'titre markdown': 1, 'liste sans point': 1, 'liste avec points': 1, 'guillemets': 1, 'guillemets+question': 1, 'ellipse minuscule': 1, 'ellipse majuscule': 1, 'ponctuation répétée': 1, 'ellipse finale': 1, 'sans point final': 1, 'espaces initiaux': 1, 'anglais Dr.': 1, 'anglais e.g.': 1, 'anglais etc.': 1, 'URL entre parenthèses': 1, 'point-virgule': 1, 'date+phrase': 1, 'URL+question réelle': 1})
  ```

