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

