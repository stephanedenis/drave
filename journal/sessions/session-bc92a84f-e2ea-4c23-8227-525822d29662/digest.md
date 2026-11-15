# Session DSH — relecture

- identifiant : `session-bc92a84f-e2ea-4c23-8227-525822d29662`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 09:44:49
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche W3 (J2 après-midi) : la matrice du tagger — **défaut** (sans clé, hors ligne, code 0), **avec clé**, **clé invalide**, **réseau coupé**, le coût pour 1 000 phrases, le repli ; la recommandation (défaut hors ligne, `--tagger` opt-in, un mode `auto` seulement si la clé existe et sans changer le code de sortie). Fiche `reports/rapport-tagger-defaut.md` + JSON, avec un test par cas dans `tools/tests/test_tagger_api.py`.

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

- **bash** `{"command": "pwd && ls && git log --oneline -5", "description": "Show repo root and recent commits"}`

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
3439cb0c ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte
1683c2b4 W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
4dbeff45 SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S
6b2208ee PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE, RESTITUTION v3, LE TAGGER PAR DÉFAUT ? ; LA FILE DU CHANTIER À 41 TÂCHES
8cb0a926 PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE CONTRÔLÉE, RESTITUTION V3, TAGGER PAR DÉFAUT ?
  ```

- **bash** `{"command": "ls tools/tests/ 2>/dev/null | head -50; echo ---; ls reports/ | head -50", "description": "List tests and reports directories"}`

  ```
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
test_restitution_v2.py
test_schema_produit.py
test_tagger_api.py
test_verificateur_cic.py
test_verificateur_cic_v2.py
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
a83b-regim
… [401 caractères tronqués]
  ```

- **bash** `{"command": "grep -ril \"tagger\" tools/ src/ --include=*.py | head -50", "description": "Find tagger-related Python files"}`

  ```
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/_cocoa_builtins.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/ncl.py
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py
tools/tests/linguistique/qualifier_neuronal.py
tools/tests/linguistique/qualifier_syntagmes.py
tools/tests/linguistique/qualifier_pragmatique.py
tools/tests/linguistique/qualifier_quatre_modes.py
tools/tests/linguistique/qualifier_tagger_612.py
tools/tests/linguistique/test_bloc_linguistique.py
tools/tests/linguistique/gold_reel_50.py
tools/tests/linguistique/qualifier_tagger_h50.py
tools/tests/test_tagger_api.py
tools/bloc_linguistique.py
tools/verifier_faq.py
tools/drave.py
  ```

- **bash** `{"command": "wc -l tools/tests/test_tagger_api.py && sed -n 1,200p tools/tests/test_tagger_api.py", "description": "Read existing tagger API test"}`

  ```
439 tools/tests/test_tagger_api.py
"""test_tagger_api.py — le tagger POS par API, **en option**, sans réseau.

Ce que le fichier verrouille, avec un **transport factice** (une fonction qui rend un JSON de
POS valide) :

1. la cascade remplace bien les POS par ceux du tagger (et garde les syntagmes de l'heuristique,
   avec leurs rôles et leurs cibles) ;
2. le JSON reste valide : le schéma **déclaré** (v2) le lit, et le contrat **v1** reste lisible ;
3. deux analyses du même texte ne refont pas d'appel (cache mémoire des taggers) ;
4. le défaut est inchangé : `analyser --json` sans `--tagger` rend exactement l'heuristique ;
5. les quatre cas d'erreur, chacun avec un transport factice :
   - **clé absente** → code **4**, message clair, `stdout` vide (`TestCle.test_sans_cle_code_4`) ;
   - **clé invalide** (HTTP 401/403) → code **4**, message clair, `stdout` vide, pas de repli ;
   - **réseau coupé** → **repli heuristique**, code **0**, `refus` non vide et message sur `stderr` ;
   - **refus du modèle** (texte non JSON, JSON incomplet) → **repli heuristique**, code **0**,
     `refus` non vide ;
6. l'ordre de résolution de la clé : `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.k
… [7829 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 200,439p tools/tests/test_tagger_api.py", "description": "Read rest of tagger API test"}`

  ```
class TestCle(unittest.TestCase):
    """La clé : ordre de résolution, code 4, et aucune trace dans les sorties."""

    def _env_propre(self, home: pathlib.Path, **extra: str) -> dict[str, str]:
        env = {cle: valeur for cle, valeur in os.environ.items()
               if cle not in {"DEEPSEEK_API_KEY", "DSH_API_KEY", "DEEPSEEK_KEY_FILE",
                              "DSH_KEY_FILE", "HOME"}
               and not cle.startswith("DEEPSEEK") and not cle.startswith("DSH_")}
        env["HOME"] = str(home)
        env.update(extra)
        return env

    def test_sans_cle_code_4(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = self._env_propre(pathlib.Path(tmp))
            for commande in (("analyser", TEXTE, "--tagger"),
                             ("evaluer", "--tagger")):
                resultat = drave_cli(*commande, env=env)
                self.assertEqual(resultat.returncode, 4,
                                 f"{commande} → {resultat.returncode} : {resultat.stderr}")
                self.assertIn("clé DeepSeek absente", resultat.stderr)
                self.assertIn("heuristique hors ligne", resultat.stderr)
                self.as
… [10743 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"tagger\\|deepseek\\|DEEPSEEK\" tools/drave.py | head -80", "description": "Find tagger wiring in drave CLI"}`

  ```
8:    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
11:    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
23:En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
24:l'API DeepSeek : la clé est lue dans `DEEPSEEK_KEY_FILE`, `~/.config/drave/deepseek.key` puis
25:`DEEPSEEK_API_KEY` ; le cache du client évite de refaire un appel ; la clé n'est jamais affichée.
26:**Sans `--tagger`, le défaut ne change pas** : heuristique, CPU, hors ligne, déterministe.
30:Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible
61:# Le tagger est une **option** : sans `--tagger`, rien de ce bloc n'est importé ni exécuté.
62:MODELE_TAGGER = "deepseek-chat"
64:# La fusion de l'option : le POS vient du tagger, tout le reste de l'heuristique. On ne force
89:# --------------------------------------------------------------------------- le tagger (option)
93:    """Aucune clé : le tagger est une option, jamais un prérequis du produit."""
106:            f"clé DeepSeek refusée (HTTP {self.code}) : vérifiez DEEPSEEK_KEY_FILE, "
107:            f"~/.
… [4651 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"W3\" journal/ docs/pilotage/ reports/ --include=*.md | head -40", "description": "Locate W3 task definition"}`

  ```
journal/sessions/8734fc13-aeb8-4cdf-b005-c182f77be0dc/digest.md:2832:**W3 — §6 l.166 « aucune source d'exécution lue à ce jour »** : elle existe (`attention.py`, `DeepseekV4Indexer`, `candidate_write`, masquage). Et le rapport ne mentionne nulle part `index_source_layer_ids = [2,8,14,20,24,28,32,36]`, déclaré et **jamais lu** par le moteur (`grep -c index_source drave-core/src/model.rs` → 0) : les clés d'indexeur de 24/28/32/36 viennent du cache de leur `kv_source` (20), pas d'un compresseur propre.
journal/sessions/1820cf6b-c8a4-411c-894c-31195b9ff7a8/digest.md:446:W3 py: bloc3 prefixe == bloc2 fenetre ? False
journal/sessions/1820cf6b-c8a4-411c-894c-31195b9ff7a8/digest.md:460:cols divergentes W3 : [16, 17, 18, 19, 20, 21, 22, 23, 40, 41, 42, 43, 44, 45, 46, 47]
journal/sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/digest.md:11307:EK/Hzg5WwkZeP0vEdBQVbLmwX3C7tZ5unAxxqyWsak65Zx+i/YGBTI5dwtzSwn/74RPT6/yxQIFOlQdrPe8NslIAhXE0dULgLUiVU9+MaZkrS4//NYtS9qHB1Ar23Y1eJpb1lYwQI1/HeTR/gYk/nq4sZx/HsknDL01B2FjvGpyZhnyIrK5mZYRDY6hRygYaoDZ78uzIgbSn/r2w/B/VMve3yjlEEAdrMo75aVw6JdkTHBrNUaDIs4iMrpb1KMS3VnSxq8KS5awapNAqFdR8uRd5g84fwphjpJX6w6oVcec1uWv68O14DyOwdcc5rTOr3BAxguKBJNeveR/4KWxSHoGJ9zF2zREnAMUj
… [14567 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,120p journal/2026-11-15*.md 2>/dev/null | head -120; ls journal | tail -20", "description": "Inspect recent journal entries"}`

  ```
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
2026-11-14
2026-11-15
README.md
sessions
THEMES.md
  ```

- **bash** `{"command": "sed -n 1,220p reports/rapport-tagger-h50.md", "description": "Read tagger H50 report"}`

  ```
# W2 — le tagger POS sur le split 402 / H50 : +4,45 pts sur 402, +17,65 sur H50 ; il gagne sur les deux, donc la règle ne le rejette pas

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **W2** (semaine 2, J2 matin) ·
> **Date** : 2026-11-15 (mesure) · **Cible** : J2 · 17/11 · **HEAD mesuré** : `6b2208ee` ·
> **Verdict** : ✅ **le tagger n'est pas H50-only** — il gagne **+4,45 pts** sur **402** et
> **+17,65 pts** sur **H50** ; le F1 et l'attachement du 402 sont **inchangés**. **Réserve nommée** :
> sur 402, le gain est **ouvert** (+10,64 pts) et le **fermé baisse** (−1,55 pt) ; une règle qui
> exigerait la non-régression du fermé rejetterait le tagger tel quel.

**En trois lignes.** (1) Sur les **402** phrases de l'entraînement, le POS passe de **0,9198** à
**0,9643** (**+4,45 pts**, **96 tokens** réparés sur 2 157) ; sur les **50** de **H50**, de
**0,6842** à **0,8607** (**+17,65 pts**, **57 tokens** sur 323). (2) Le **F1** et l'**attachement**
ne bougent pas (le tagger ne remplace que le POS) ; le total 452 donne **0,9508** contre **0,8891**
(**+6,17 pts**), à **0,0008** du 0,9500 déjà publié. (3) La passe **API** paie **447 requêtes** et
**65 029 tokens rés
… [13116 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/*tagger*; echo ---; for f in reports/*tagger*.json; do echo \"== $f\"; python3 -m json.tool \"$f\" | head -80; done", "description": "List and inspect tagger JSON reports"}`

  ```
reports/pensee-tagger-option.json
reports/rapport-exemples-tagger.json
reports/rapport-exemples-tagger.md
reports/rapport-tagger-erreurs.json
reports/rapport-tagger-erreurs.md
reports/rapport-tagger-h50.json
reports/rapport-tagger-h50.md
reports/rapport-tagger-option.md
reports/tagger-612.json
---
== reports/pensee-tagger-option.json
{
    "date": "2026-11-14",
    "branche": "s/v7",
    "decision": "1A \u2014 le tagger API en option, le d\u00e9faut reste hors ligne",
    "ligne_roadmap": "R0.7 (le lecteur)",
    "option": {
        "drapeau": "--tagger",
        "commandes": [
            "analyser",
            "evaluer"
        ],
        "modele_demande": "deepseek-chat",
        "seuil_cascade": 0.6,
        "fusion": {
            "pos": "neuronal (tagger)",
            "syntagme": "heuristique",
            "pragmatique": "heuristique",
            "pourquoi": "le tagger ne rend ni r\u00f4le ni cible : forcer ses syntagmes ferait perdre l'attachement mesur\u00e9"
        },
        "cle": [
            "DEEPSEEK_KEY_FILE",
            "~/.config/drave/deepseek.key",
            "DEEPSEEK_API_KEY",
            "DSH_KEY_FILE / DSH_API_KEY (repli)"
        ],
        "cle_absen
… [17186 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,200p reports/rapport-tagger-erreurs.md", "description": "Read tagger errors report"}`

  ```
# E2 — les cas d'erreur de `--tagger` : clé refusée = code 4, réseau et refus du modèle = repli heuristique

> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **E2** · **Date** : 2026-11-15 ·
> **Verdict** : ✅ **4/4 cas caractérisés**, **18/18 tests**, **0 socket**.
> **La clé invalide (HTTP 401/403) sort désormais 4** avec un message clair et **rien sur
> `stdout`** ; avant, elle était avalée par le tagger et le CLI rendait **0** avec un repli
> heuristique déguisé en cascade. Le **réseau coupé** (3 essais du client) et le **refus du
> modèle** restent des refus **par phrase** : repli heuristique, code **0**, cause dans `refus`.
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) 0.1.0, client `DeepSeek` injecté,
> transport factice, cache temporaire vide, aucun socket. **Contrôle négatif** : un transport
> valide donne code 0 et des POS neuronaux ; la mutation qui retire le contrôle 401/403 fait
> échouer le test (`0 != 4`). **JSON** : [`rapport-tagger-erreurs.json`](rapport-tagger-erreurs.json).

## 1. Les quatre cas

Le tableau dit le comportement **du code courant**, pas l'intention. Chaque ligne a son test
dans [`test_tagger_api.py`](../tools/tests/test_tagger_
… [9556 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,180p reports/rapport-tagger-option.md", "description": "Read tagger option report"}`

  ```
# R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne

> **Ligne de roadmap** : **R0.7** (le lecteur) · **Décision** : **1A** du 14/11 · **Date** :
> 2026-11-14 · **Verdict** : ✅ **option livrée** — `--tagger` sur `analyser` et `evaluer` ; POS
> **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre
> 0,8625** du gold 612 (**+8,49**) ; **40 appels**, **11 868 tokens** (cache neuf), **0 refus** ;
> le **défaut** reste l'**heuristique**, CPU, hors ligne, déterministe. Le gain est **+4,67** sur
> le seul gold réel 432 : lire le chiffre avec sa source.

## 1 bis. Les deux défauts corrigés (15/11)

| défaut | avant | **après** |
|---|---|---|
| **2 appels par phrase** (le tagger de syntagmes était appelé sans être utilisé) | 2 appels | **1 appel** |
| **`PONCT` perdu** (le tagger ne reçoit que mots et nombres) | 0 ponctuation étiquetée | **25/25** (restituée depuis l'heuristique) |

**La mesure sur le gold 612** (avec la clé, cache partiel) : POS **0,9575** contre 0,8625 pour
l'heuristique — **+9,5 points** (le `PONCT` restitué ajoute 0,25 pt ; le reste vient du tagger).
**Sur la base r
… [9371 caractères tronqués]
  ```

- **bash** `{"command": "ls -la ~/.config/drave/deepseek.key 2>&1; echo \"DEEPSEEK_KEY_FILE=${DEEPSEEK_KEY_FILE:-}\"; echo \"DEEPSEEK_API_KEY set? ${DEEPSEEK_API_KEY:+yes}\"; ls -la data/deepseek/cache 2>/dev/null | head -3", "description": "Check API key presence without printing it"}`

  ```
-rw-------. 1 stephane stephane 36  3 nov 11:15 /home/stephane/.config/drave/deepseek.key
DEEPSEEK_KEY_FILE=
DEEPSEEK_API_KEY set? 
total 15100
drwxr-xr-x. 1 stephane stephane 518742 15 nov 01:38 .
drwxr-xr-x. 1 stephane stephane    574 26 oct 15:08 ..
  ```

- **bash** `{"command": "grep -rn \"tokens.*\\$\\\\|tarif\\\\|prix.*token\\|par million\\|M tokens\\|/M\\\\b\" reports/*tagger* docs/produit/README.md 2>/dev/null | head -30", "description": "Search for token pricing references"}`

  ```
reports/pensee-tagger-option.json:30:  "cache": "mémoire par (texte, langue) dans chaque tagger + cache disque du client (modèle + messages + température + max_tokens, jamais la clé)",
reports/pensee-tagger-option.json:34:  "dispositif": "20 premières phrases de gold.json (source hand), 105 tokens ; transport réel via tools/llm/deepseek.py, température 0, cache neuf /tmp/drave-tagger-option-cache",
reports/pensee-tagger-option.json:37:   "tokens": 105,
reports/pensee-tagger-option.json:77:   "tokens": 11868,
reports/pensee-tagger-option.json:89:   "tokens": 0,
reports/pensee-tagger-option.json:103:   "tokens": 3179,
reports/pensee-tagger-option.json:132:  "tokens": 358962,
reports/pensee-tagger-option.json:162:  "105 tokens seulement : 3 erreurs séparent 0,9714 de 0,9429 ; l'intervalle est large",
reports/pensee-tagger-option.json:179:   "tokens": 22299,
reports/rapport-exemples-tagger.json:17:  "note": "les trois exemples --tagger ont été lancés avec un cache disque vide ; les appels suivants du rejeu sont servis par le cache (réseau=0, tokens=0)"
reports/rapport-exemples-tagger.json:26:    "sortie": "drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)\nlangue=fr scrip
… [4905 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"auto\" tools/drave.py | head -20; echo ---; grep -rn \"mode auto\\|--auto\\|auto\" docs/produit/README.md | head -20", "description": "Check for existing auto mode"}`

  ```
47:# externe n'est importé : le point d'entrée est autonome.
---
63:| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; le CLI n'expose que `fr`/`en` comme indice) |
542:décision automatique sans contrôle.
583:| **porte produit** | version, JSON fr/en, rejeu, smoke test, autotest | `bash tools/porte-produit.sh` → ✅ |
588:restitution, **183/183** portes d'autotest ; **12 contrôles**. Le smoke test est
679:| **`--profils`** | les 398 langues de l'autotest UDHR ne sont pas accessibles par le CLI |
710:(**0,9687** sur l'autotest), mais le **CLI** n'expose que `fr` et `en` comme **indice**
  ```

- **bash** `{"command": "sed -n 1,270p tools/drave.py", "description": "Read drave tagger implementation"}`

  ```
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, quatre gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer "Le chat dort." --roles
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
**restitution v0** (annotation → surface, avec la fidélité du miroir) et la **v2** (rôles
agent/prédicat
… [11236 caractères tronqués]
  ```

- **bash** `{"command": "ls journal/2026-11-15; echo ---; sed -n 1,160p journal/2026-11-15/*.md 2>/dev/null | head -160", "description": "Inspect today's journal"}`

  ```
distribue.md
docs.md
mesures.md
modele.md
outils.md
portes.md
README.md
---
# 2026-11-15 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (5)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 02:27 | `f926b5bc` | C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PROFONDEUR, 41 VERDICTS À RE-JUGER ; PORT 8765 PRIS, PARE-FEU ACTIF ; LES 11 VERDICTS COMMITTÉS (389b99f) | `en-cours.md`, `roadmap.md`, `README.md` (+17) |
| 03:04 | `c37fed06` | B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE | `en-cours.md`, `README.md`, `distribue.md` (+16) |
| 04:26 | `f1c6b506` | PHASE 3 (C PUIS B) — N2 (--rope --canal-dir), S (page / et 11 VERDICTS), R (GOLD RÉEL 452), PANINI (PROTOCOLE À DATE CONTRÔLÉE, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX, CIC 42/42) ; 6 FICHES, SEPT. 9 DU PLAN | `en-cours.md`,
… [11899 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"W3\\|tagger par défaut\\|tagger\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -40", "description": "Find W3 in state and roadmap"}`

  ```
docs/pilotage/en-cours.md:3:**Mis à jour : 2026-11-15, 09 h 25 HNE (W2 : tagger 402/H50)**
docs/pilotage/en-cours.md:64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; **D1–D3**, **E1–E2** livrés ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
docs/pilotage/en-cours.md:91:- **W2 — tagger 402/H50** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/att 402 **inchangés**, **fermé −1,55** ; [fiche](../../reports/rapport-tagger-h50.md) ; la règle ne le rejette pas, réserve à **W3**.
docs/pilotage/en-cours.md:99:- **J5.1 / J10.1 / J13.1 / J14.1 — bilans et clôture** : F1 **0,7902** (tagger **0,9475**), chantier **20/21** ; **J13.1** **612/602** ; **J14.1** clôture **84/81/3** (tag `chantier-2026-11-14`) ; [semaine](../../reports/rapport-semaine.md), [bilan](../../reports/rapport-bilan-chantier.md), [tableau](../../reports/rapport-tableau-mesures.md), [clôture](../../reports/rapport-cloture-chantier.md).
docs/pilotage/en-cours.md:123:| **R — le lecteur**
… [6742 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"W3\" docs/pilotage/*.md | head -20", "description": "Find W3 in planning docs"}`

  ```
docs/pilotage/en-cours.md:91:- **W2 — tagger 402/H50** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/att 402 **inchangés**, **fermé −1,55** ; [fiche](../../reports/rapport-tagger-h50.md) ; la règle ne le rejette pas, réserve à **W3**.
docs/pilotage/en-cours.md:123:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, fermé −1,55** ; R2/R3 attendent N5/N4 | **W3 — tagger par défaut** ; **[fiche](../../reports/rapport-tagger-h50.md)** |
docs/pilotage/en-cours.md:131:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold de pensée, **qualité des rôles** ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — migration `/` v7 (106/41) ; référents ; **W3** — tagger par défaut ; **A** — A6.2, A8.3b2.
docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (4/5 familles ≥ 90 %) ; **R
… [439 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -20", "description": "Run tagger API tests baseline"}`

  ```
test_absence_de_cle_ne_fuit_pas (__main__.TestCle.test_absence_de_cle_ne_fuit_pas) ... ok
test_la_cle_ne_sort_pas_du_client (__main__.TestCle.test_la_cle_ne_sort_pas_du_client) ... ok
test_ordre_de_resolution (__main__.TestCle.test_ordre_de_resolution) ... ok
test_sans_cle_code_4 (__main__.TestCle.test_sans_cle_code_4) ... ok
test_analyser_tagger_json (__main__.TestCliAvecTransportFactice.test_analyser_tagger_json) ... ok
test_analyser_tagger_lisible (__main__.TestCliAvecTransportFactice.test_analyser_tagger_lisible) ... ok
test_evaluer_tagger (__main__.TestCliAvecTransportFactice.test_evaluer_tagger) ... ok
test_aide_expose_tagger (__main__.TestDefaultInchange.test_aide_expose_tagger) ... ok
test_analyser_json_sans_tagger (__main__.TestDefaultInchange.test_analyser_json_sans_tagger) ... ok
test_evaluer_sans_tagger (__main__.TestDefaultInchange.test_evaluer_sans_tagger) ... ok
test_cle_invalide_code_4 (__main__.TestErreursTagger.test_cle_invalide_code_4) ... ok
test_modele_json_incomplet_repli_heuristique (__main__.TestErreursTagger.test_modele_json_incomplet_repli_heuristique)
Un JSON qui n'a pas une classe par token est un refus de contrat, pas une exception. ... ok
test_refus_du
… [307 caractères tronqués]
  ```

- **bash** `{"command": "tmp=$(mktemp -d); env -i HOME=\"$tmp\" PATH=\"$PATH\" python3 tools/drave.py analyser \"Le chat dort.\" --json >/tmp/w3-defaut.json 2>/tmp/w3-defaut.err; echo \"code=$?\"; python3 -c \"import json;d=json.load(open('/tmp/w3-defaut.json'));print(d['source'], len(d['etiquettes']), bool(d.g … [104 caractères tronqués]`

  ```
code=0
heuristique 20 False
  ```

- **bash** `{"command": "grep -n \"cache\\|CACHE\\|def __init__\\|DEEPSEEK\" tools/llm/deepseek.py | head -60", "description": "Inspect DeepSeek client cache config"}`

  ```
14:dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
18:- `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
19:- `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
20:- `DEEPSEEK_MODEL` (ou `DSH_MODEL`) : `deepseek-chat` par défaut ;
21:- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages
27:    DEEPSEEK_API_KEY=... python3 tools/llm/deepseek.py --prompt ... --json
44:CACHE_DEFAUT = RACINE / "data" / "deepseek" / "cache"
52:    def __init__(self, message: str, *, code: int | None = None,
66:    cache: bool = False
76:    `DEEPSEEK_API_KEY` / `DSH_API_KEY` d'abord ; sinon `DEEPSEEK_KEY_FILE` /
80:    for var in ("DEEPSEEK_API_KEY", "DSH_API_KEY"):
84:    for var in ("DEEPSEEK_KEY_FILE", "DSH_KEY_FILE"):
96:def _cache_cle(modele: str, messages: list[dict], temperature: float,
127:    def __init__(self, cle: str | None = None, base_url: str | None = None,
128:                 modele: str | None = None, cache_dir: str | pathlib.Path | None = None,
132:        self.base_url = (base_url or os.environ.get("DEEPSEEK_BASE_URL")
135:        self.modele = (modele or os.environ.ge
… [1347 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 120,240p tools/llm/deepseek.py", "description": "Read client retry logic"}`

  ```
try:
        return json.loads(texte)
    except json.JSONDecodeError as e:
        raise ErreurDeepSeek(f"réponse non JSON : {texte[:200]}") from e


class DeepSeek:
    def __init__(self, cle: str | None = None, base_url: str | None = None,
                 modele: str | None = None, cache_dir: str | pathlib.Path | None = None,
                 transport=None, sleep=time.sleep, timeout: float = 120.0,
                 essais: int = 3) -> None:
        self.cle = cle if cle is not None else _cle_env()
        self.base_url = (base_url or os.environ.get("DEEPSEEK_BASE_URL")
                         or os.environ.get("DSH_BASE_URL")
                         or BASE_DEFAUT).rstrip("/")
        self.modele = (modele or os.environ.get("DEEPSEEK_MODEL")
                       or os.environ.get("DSH_MODEL") or MODELE_DEFAUT)
        self.cache_dir = pathlib.Path(cache_dir or os.environ.get("DEEPSEEK_CACHE")
                                      or CACHE_DEFAUT)
        self.transport = transport or _http
        self.sleep = sleep
        self.timeout = timeout
        self.essais = max(1, essais)

    # ------------------------------------------------------------------
    def disponibl
… [4467 caractères tronqués]
  ```

- **bash** `{"command": "set -u\nCACHE=/tmp/w3-tagger-cache-avec-cle; rm -rf \"$CACHE\"; mkdir -p \"$CACHE\"\nt0=$(date +%s.%N)\nenv -u DEEPSEEK_API_KEY -u DSH_API_KEY -u DEEPSEEK_KEY_FILE -u DSH_KEY_FILE \\\n  DEEPSEEK_CACHE=\"$CACHE\" python3 tools/drave.py analyser \"Le chat dort.\" --tagger --json \\\n  > / … [714 caractères tronqués]`

  ```
code=0 duree=1.341
source cascade refus ''
pos [('DET', 'neuronal'), ('NOUN', 'neuronal'), ('VERB', 'neuronal'), ('PONCT', 'heuristique')]
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.2 s
1
usage {'prompt_tokens': 116, 'completion_tokens': 14, 'total_tokens': 130, 'prompt_tokens_details': {'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 116} modele deepseek-flash latence 1.153
  ```

- **bash** `{"command": "set -u\ntmp=$(mktemp -d); printf 'cle-invalide-sentinelle\\n' > \"$tmp/bad.key\"; CACHE=\"$tmp/cache\"; mkdir -p \"$CACHE\"\nt0=$(date +%s.%N)\nenv -i HOME=\"$tmp/home\" PATH=\"$PATH\" DEEPSEEK_KEY_FILE=\"$tmp/bad.key\" DEEPSEEK_CACHE=\"$CACHE\" \\\n  python3 tools/drave.py analyser \"L … [297 caractères tronqués]`

  ```
code=4 duree=0.644 stdout_octets=0
drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.
  ```

- **bash** `{"command": "set -u\ntmp=$(mktemp -d); CACHE=\"$tmp/cache\"; mkdir -p \"$CACHE\"\nt0=$(date +%s.%N)\nenv -u DEEPSEEK_API_KEY -u DSH_API_KEY -u DEEPSEEK_KEY_FILE -u DSH_KEY_FILE \\\n  DEEPSEEK_BASE_URL=\"http://127.0.0.1:9\" DEEPSEEK_CACHE=\"$CACHE\" \\\n  python3 tools/drave.py analyser \"Le chat do … [531 caractères tronqués]`

  ```
code=0 duree=3.257 stdout_octets=6253
source cascade refus 'neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused'
pos_sources ['heuristique']
drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-tagger-h50.json'))\ndef walk(o,path=''):\n    if isinstance(o,dict):\n        for k,v in o.items():\n            if any(s in k.lower() for s in ('cout','token','latence','requete','appel')):\n                print(path+'/' … [246 caractères tronqués]`

  ```
/or/tokens 2480
/split/composition/h50/tokens 323
/split/composition/reste_402/tokens 2157
/split/composition/total/tokens 2480
/split/composition/tirage_hors_h50/tokens 248
/controles_negatifs/hasard_402/tokens 2157
/controles_negatifs/hasard_h50/tokens 323
/controles_negatifs/hasard_tirage/tokens 248
/passes/cache_chaud/bases/reste_402/composition/tokens 2157
/passes/cache_chaud/bases/reste_402/heuristique/pos/tokens 2157
/passes/cache_chaud/bases/reste_402/heuristique/syntagme/rappel 0.8024
/passes/cache_chaud/bases/reste_402/heuristique/syntagme/tete/rappel 0.8825
/passes/cache_chaud/bases/reste_402/tagger/pos/tokens 2157
/passes/cache_chaud/bases/reste_402/tagger/syntagme/rappel 0.8024
/passes/cache_chaud/bases/reste_402/tagger/syntagme/tete/rappel 0.8825
/passes/cache_chaud/bases/reste_402/par_langue/en/tokens 993
/passes/cache_chaud/bases/reste_402/par_langue/en/heuristique/tokens 993
/passes/cache_chaud/bases/reste_402/par_langue/en/tagger/tokens 993
/passes/cache_chaud/bases/reste_402/par_langue/fr/tokens 1164
/passes/cache_chaud/bases/reste_402/par_langue/fr/heuristique/tokens 1164
/passes/cache_chaud/bases/reste_402/par_langue/fr/tagger/tokens 1164
/passes/cache_chaud/ba
… [25918 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"_cout_tagger\\|stats_tagger\\|\\\"cout\\\"\" tools/drave.py", "description": "Find cost usage sites"}`

  ```
240:def _cout_tagger(stats: dict) -> dict:
402:            cascade, stats_tagger = _construire_tagger(partition=args.partition)
408:            bloc, stats = cascade, stats_tagger
519:        tp, ts, cout = tagger["pos"], tagger["syntagme"], tagger["cout"]
637:            "cout": _cout_tagger(stats),
  ```

- **bash** `{"command": "sed -n 540,690p tools/drave.py", "description": "Read evaluer implementation"}`

  ```
lignes += ["", "PAR LANGUE"]
        for langue, m in par_langue.items():
            p, s, a, c = m["pos"], m["syntagme"], m["attachement"], m["controle_negatif"]
            pr = m["pragmatique"]
            lignes += [
                f"  {langue}  {m['phrases']} phrases · {p['tokens']} tokens · "
                f"{a['cibles']} cibles d'attachement",
                f"      POS {_pct(p['exactitude'])} (fermé {_pct(p['exactitude_ferme'])}, "
                f"ouvert {_pct(p['exactitude_ouvert'])}) · SYNTAGMES F1 {_pct(s['f1'])} "
                f"(tête {_pct(s['tete']['f1'])})",
                f"      ATTACHEMENT exact {_pct(a['exact_taux'])} · "
                f"couverture {_pct(a['couverture'])} · top-k {_pct(a['topk_taux'])} · "
                f"PRAGMATIQUE acte {_pct(pr['acte'])}",
                f"      CONTRÔLE NÉGATIF cible exacte tirée au hasard {_pct(c['exact_taux'])} "
                f"(graine {c['graine']}, {c['cibles']} cibles)",
            ]
            t = m.get("tagger")
            if t:
                lignes.append(
                    f"      TAGGER POS {_pct(t['pos']['exactitude'])} "
                    f"· Δ {_points(t['delta_pos'])} "
              
… [6646 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"tagger par défaut\\|tagger.*défaut\" docs/pilotage docs/methode | head -20", "description": "Find planning text about tagger default"}`

  ```
docs/pilotage/semaine-autonome.md
docs/pilotage/semaine-2.md
docs/pilotage/roadmap.md
docs/pilotage/en-cours.md
  ```

- **bash** `{"command": "ls docs/pilotage/ | head -40; echo ---; sed -n 1,140p docs/pilotage/semaine-2.md 2>/dev/null", "description": "Look for week 2 plan"}`

  ```
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
# La semaine 2 — cinq jours, deux vagues, quatre chantiers et une décision

> **Ce que ce document est.** Le plan du **16 au 22 novembre 2026** : ce qui se fait, dans quel
> ordre, avec quelles dépendances, quels contrôles et quels livrables. Il **succède** à
> [`semaine-autonome.md`](semaine-autonome.md), qui reste l'**archive** de la semaine 1 et n'est
> **pas modifié**. L'état courant est dans [`en-cours.md`](en-cours.md) ; les chiffres sont dans
> les fiches citées, jamais recopiés ici.
>
> **Sources.** Le [bilan de la semaine](../../reports/rapport-bilan-semaine.md) et les fiches des
> tâches C/B/D/E : [C1](../../reports/rapport-coordination-n2-v2.md), [C2](../../reports/rapport-coordination-s-v2.md),
> [C3](../../reports/rapport-gold-reel-50.md), [B1](../../reports/rapport-protocole-date.md),
> [B2](../../reports/rapport-atomes-prediction.md), [B3](../../reports/rapport-cic-v2.md),
> [D1](../../reports/rapport-exemples-tagger.md), [D2](../../reports/rapport-restitution-v2.md),
> [D3](../../reports/rapp
… [10868 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 360,460p tools/drave.py", "description": "Read analyser command"}`

  ```
def _lire_entree(args: argparse.Namespace) -> str:
    """Le texte : l'argument, ou le **fichier** (`--fichier`)."""
    if getattr(args, "fichier", None):
        return pathlib.Path(args.fichier).read_text(encoding="utf-8", errors="replace")
    return args.texte or ""


def _analyser_jsonl(texte: str, args: argparse.Namespace, h: bl.Heuristique, bloc,
                    stats: dict | None = None) -> int:
    """Une **ligne JSON par phrase** (traitement de corpus : `--jsonl`).

    `h` segmente (le tagger ne change pas les frontières de phrase) ; `bloc` analyse — la
    cascade du tagger quand `--tagger` est posé. Le coût va sur `stderr`, jamais dans le JSONL.
    """
    n = 0
    refus = 0
    for debut, fin, _typ, _ in h._phrases(texte):
        phrase = texte[debut:fin]
        if not phrase.strip():
            continue
        a = bloc.analyser(phrase, args.langue, args.contexte)
        refus += int(bool(a.refus))
        sys.stdout.write(_sur(json.dumps(a.json(), ensure_ascii=False)) + "\n")
        n += 1
    if n == 0:
        print(f"{NOM}: refus d'analyse : vide", file=sys.stderr)
        return 3
    if stats is not None:
        print(f"{NOM}: TAGGER API · {_ligne_
… [3307 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"reports/\" tools/tests/*.py tools/tests/**/*.py 2>/dev/null | head -20", "description": "Check tests reading reports"}`

  ```
tools/tests/qualifier_politique_drvm.py:10:        --sortie reports/pensee-politique-llm.json
tools/tests/qualifier_politique_drvm.py:53:    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-politique-llm.json"))
tools/tests/qualifier_porte_bouge_drvm.py:11:        --sortie reports/pensee-porte-bouge.json
tools/tests/qualifier_porte_bouge_drvm.py:53:    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-porte-bouge.json"))
tools/tests/qualifier_porte_drvm.py:10:        --sortie reports/pensee-porte-llm.json
tools/tests/qualifier_porte_drvm.py:51:    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-porte-llm.json"))
tools/tests/qualifier_porte_fenetre_drvm.py:10:        --sortie reports/pensee-porte-fenetre.json
tools/tests/qualifier_porte_fenetre_drvm.py:51:    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-porte-fenetre.json"))
tools/tests/qualifier_porte_minute_drvm.py:10:        --sortie reports/pensee-porte-minute.json
tools/tests/qualifier_porte_minute_drvm.py:51:    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-porte-minute.json"))
tools/tests/qualifier_porte_mobile_drvm.py:11:        --sortie r
… [1157 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"0,0[0-9] \\$\\|0\\.0[0-9] \\$\\|tarif\\|prix\" reports/rapport-*.md docs/produit/README.md | head -30", "description": "Search previous dollar estimates"}`

  ```
reports/rapport-8bits.md:53:5. **Conclusion** : la perfection sans perte se paie au prix de l'entropie, et
reports/rapport-b1110-cartes.md:66:  notation légitime sans jeu — c'est le prix de l'explicite.
reports/rapport-c4-retard.md:1:# C4 — le prix d'un état en retard : **×633 pour UN pas**, et ce que ça impose à un ordonnanceur
reports/rapport-c4-retard.md:18:| retard k | perplexité (128 jetons, couche 12) | prix |
reports/rapport-c4-retard.md:43:état). Le prix des deux derniers est mesuré (128 jetons, couche 12 ; un état « manquant » est mis à
reports/rapport-c4-retard.md:46:| situation | perplexité | prix |
reports/rapport-c4-retard.md:71:état reçu. Le prix est ×633 par pas, mesuré.
reports/rapport-c8-peripherie.md:163:le déterminisme est tenu au bit près, le délai est exact, et **chaque décision a son prix en
reports/rapport-c9-lateralite.md:63:prix en perplexité ?** Mesure (64 jetons, couche 12, état quantifié par blocs de 32 canaux comme
reports/rapport-c9-lateralite.md:66:| encodage de l'état échangé | octets / pas | ÷ | perplexité | prix |
reports/rapport-campagne-parcimonie.md:61:**L'écart est exactement le prix de l'entraînement.** Un réseau *entraîné* à
reports/rapport-c
… [2291 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 135,175p reports/rapport-coordination-r.md; echo ---; sed -n 50,70p reports/rapport-exemples-tagger.md", "description": "Read pricing approach in prior reports"}`

  ```
| tokens | ~360 000 | **358 962** | −0,3 % |
| durée | ~20 min | **20 min 59 s** (1 259,2 s) | +5 % |
| latence moyenne / appel | 0,94 s (run 432) | **1,033 s** | +10 % |
| latence médiane | — | **1,011 s** | — |

Le run 432 de référence (`pensee-quatre-modes-432-run2.json`) : **858 appels**, **254 454
tokens**, **807,6 s**, soit **1,986 appel/phrase**, **296,6 tokens/appel**, **0,941 s/appel**.
Le passage à 612 donne **1 218 appels**, **358 962 tokens**, **1 259,2 s** : la consigne était
juste à quelques pour cent.

### 3.3 Le coût facturé

Tarif public `deepseek-flash` au 2026-11-13 (hors pointe / pointe) : entrée **cache hit**
0,003 / 0,006 $ par M, entrée **cache miss** 0,15 / 0,30 $ par M, sortie 0,60 / 1,20 $ par M
([tarifs](https://api-docs.deepseek.com/quick_start/pricing)). Le run a consommé, d'après les
`usage` du cache : **155 136 tokens d'entrée en cache hit**, **174 822 en cache miss**,
**27 326 tokens de sortie** (totaux à ±0,5 % près, six prompts dupliqués).

| tarif | entrée hit | entrée miss | sortie | **total** |
|---|---:|---:|---:|---:|
| **hors pointe** (run à 03:00 UTC, samedi) | 0,0005 $ | 0,0262 $ | 0,0164 $ | **~0,043 $** |
| **pointe** | 0,0009 $ | 0,0524 
… [1894 caractères tronqués]
  ```

- **bash** `{"command": "ls -d /tmp/tagger-h50-api-cache /tmp/drave-tagger-option-cache /tmp/drave-exemples-tagger-cache 2>/dev/null; ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l", "description": "Check if W2 API cache still exists"}`

  ```
/tmp/drave-exemples-tagger-cache
/tmp/drave-tagger-option-cache
/tmp/tagger-h50-api-cache
447
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,glob,collections,statistics\nf=glob.glob('/tmp/tagger-h50-api-cache/*.json')[0]\nd=json.load(open(f))\nprint(d.keys())\nprint('usage',d.get('usage'))\nprint('modele',d.get('modele'))\n# aggregate\nprompt=completion=total=0\nn=0\nmods=collections.Counter()\n … [457 caractères tronqués]`

  ```
dict_keys(['contenu', 'modele', 'usage', 'raisonnement', 'latence_s', 'recu_le', 'brut'])
usage {'prompt_tokens': 120, 'completion_tokens': 17, 'total_tokens': 137, 'prompt_tokens_details': {'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 120}
modele deepseek-flash
n 447 prompt 55572 completion 9457 total 65029 mods Counter({'deepseek-flash': 447})
per phrase prompt 55.572 completion 9.457
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,glob,collections\nhit=miss=prompt=comp=0\nfor f in glob.glob('/tmp/tagger-h50-api-cache/*.json'):\n    d=json.load(open(f)); u=d.get('usage') or {}\n    prompt+=u.get('prompt_tokens',0); comp+=u.get('completion_tokens',0)\n    hit+=u.get('prompt_cache_hit_t … [612 caractères tronqués]`

  ```
prompt 55572 hit 0 miss 55572 comp 9457
452 prompt 55572.0 comp 9457.0 hit 0.0 miss 55572.0 offpeak 0.01401 peak 0.02802
1000 prompt 122946.9 comp 20922.6 hit 0.0 miss 122946.9 offpeak 0.030996 peak 0.061991
  ```

- **bash** `{"command": "cat > /tmp/w3_mesure.py <<'PY'\nimport json, os, pathlib, subprocess, sys, tempfile, time\n\nRACINE = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nCLI = RACINE / 'tools' / 'drave.py'\nBASE = {k: v for k, v in os.environ.items()\n        if not k.startswith(('DEEPSEEK … [4128 caractères tronqués]`

  ```
{"nom": "defaut_sans_cle_analyser", "commande": "python3 tools/drave.py analyser Le chat dort. --json", "code": 0, "duree_s": 0.161, "stdout_octets": 5852, "stderr": ""}
{"nom": "defaut_sans_cle_evaluer", "commande": "python3 tools/drave.py evaluer --json", "code": 0, "duree_s": 1.364, "stdout_octets": 3165, "stderr": ""}
{"nom": "avec_cle_analyser", "commande": "python3 tools/drave.py analyser Le chat dort. --tagger --json", "code": 0, "duree_s": 1.01, "stdout_octets": 6117, "stderr": "drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=0.8 s"}
{"nom": "cle_invalide_analyser", "commande": "python3 tools/drave.py analyser Le chat dort. --tagger --json", "code": 4, "duree_s": 0.658, "stdout_octets": 0, "stderr": "drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne."}
{"nom": "reseau_coupe_analyser", "commande": "python3 tools/drave.py analyser Le chat dort. --tagger --json", "code": 0, "duree_s": 3.253, "stdout_octets": 6253, "stderr": "drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: 
… [253 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/w3-matrix.json'))\nfor k in ('defaut_analyser','defaut_evaluer','avec_cle','cle_invalide','reseau_coupe'):\n    r=d[k]; j=r.get('stdout_json')\n    print('\\n==',k,'code',r['code'],'octets',r['stdout_octets'],'duree',r['duree_s'])\n  … [454 caractères tronqués]`

  ```
== defaut_analyser code 0 octets 5852 duree 0.161
stderr: 
source heuristique refus ''
pos [(0, 2, 'DET', 'heuristique'), (3, 7, 'NOUN', 'heuristique'), (8, 12, 'VERB', 'heuristique'), (12, 13, 'PONCT', 'heuristique')]

== defaut_evaluer code 0 octets 3165 duree 1.364
stderr: 
source None refus None
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
KeyError: 'etiquettes'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/w3-matrix.json'))\nfor k in ('defaut_evaluer','avec_cle','reseau_coupe'):\n    r=d[k]; j=r.get('stdout_json')\n    print('\\n==',k,'code',r['code'],'octets',r['stdout_octets'],'duree',r['duree_s'])\n    print('stderr:',r['stderr'])\n … [408 caractères tronqués]`

  ```
== defaut_evaluer code 0 octets 3165 duree 1.364
stderr: 
keys ['version', 'gold', 'heuristique', 'reel', 'syntagmes_lineaire', 'attachement_lineaire', 'controle_negatif'] gold {'nom': 'vivant (hand + reel + synthétique)', 'gele': False, 'phrases': 612, 'tokens': 3179, 'cibles_attachement': 239}

== avec_cle code 0 octets 6117 duree 1.01
stderr: drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=0.8 s
source cascade refus ''
pos [(0, 2, 'DET', 'neuronal'), (3, 7, 'NOUN', 'neuronal'), (8, 12, 'VERB', 'neuronal'), (12, 13, 'PONCT', 'heuristique')]
cache [{'usage': {'prompt_tokens': 116, 'completion_tokens': 14, 'total_tokens': 130, 'prompt_tokens_details': {'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 116}, 'modele': 'deepseek-flash', 'latence_s': 0.834}]

== reseau_coupe code 0 octets 6253 duree 3.253
stderr: drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s
source cascade refus 'neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused'
pos [(
… [125 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _cout_tagger\" -A 12 tools/drave.py", "description": "Locate cost helper region"}`

  ```
240:def _cout_tagger(stats: dict) -> dict:
241-    """Le coût d'une exécution, tel qu'il va dans un rapport (`evaluer --json`)."""
242-    return {"modele": MODELE_TAGGER, "appels": stats["appels"],
243-            "requetes": stats["requetes"], "cache": stats["cache"],
244-            "tokens": stats["tokens"], "latence_s": round(stats["latence_s"], 3),
245-            "modeles_renvoyes": dict(stats["modeles"])}
246-
247-
248-def _ligne_tagger(stats: dict) -> str:
249-    """Une ligne de coût pour l'affichage et la stderr ; pas de clé, pas d'horodatage."""
250-    return (f"modèle={MODELE_TAGGER} · appels={stats['appels']} "
251-            f"· réseau={stats['requetes']} · cache={stats['cache']} "
252-            f"· tokens={stats['tokens']} · latence={stats['latence_s']:.1f} s")
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "def _ligne_tagger(stats: dict) -> str:\n    \"\"\"Une ligne de coût pour l'affichage et la stderr ; pas de clé, pas d'horodatage.\"\"\"", "new_string": "def _cout_pour_phrases(cout: dict, mesurees: int, ci … [1256 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 232, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
232:     """Rend (cascade, stats) ; lève `CleTaggerAbsente` si la clé manque (et ne l'affiche pas)."""
233:     stats = {"appels": 0, "requetes": 0, "cache": 0, "tokens": 0, "latence_s": 0.0,
234:              "modeles": {}, "cle_refusee": 0}
235:     client = _client_tagger()
236:     return _cascade_tagger(_transport_tagger(client, stats), partition=partition,
237:                            stats=stats), stats
238: 
239: 
240: def _cout_tagger(stats: dict) -> dict:
241:     """Le coût d'une exécution, tel qu'il va dans un rapport (`evaluer --json`)."""
242:     return {"modele": MODELE_TAGGER, "appels": stats["appels"],
243:             "requetes": stats["requetes"], "cache": stats["cache"],
244:             "tokens": stats["tokens"], "latence_s": round(stats["latence_s"], 3),
245:             "modeles_renvoyes": dict(stats["modeles"])}
246: 
247: 
248: def _ligne_tagger(stats: dict) -> str:
249:     """Une ligne de coût pour l'affichage et la stderr ; pas de clé, pas d'horodatage."""
250:     return (f"modèle={MODELE_TAGGER} · appels={stats['appels']} "
251:             f"· r
… [564 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "def _ligne_tagger(stats: dict) -> str:\n    \"\"\"Une ligne de coût pour l'affichage et la stderr ; pas de clé, pas d'horodatage.\"\"\"", "new_string": "def _cout_pour_phrases(cout: dict, mesurees: int, ci … [1256 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 30, "offset": 642}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
642:     }
643:     if cascade is not None:
644:         # `evaluer_bloc` mesure l'annotation de la cascade ; le POS y vient du tagger. Les
645:         # appels sont ensuite servis par le cache mémoire des taggers (aucun appel en plus).
646:         mesure_tag = evaluateur.evaluer_bloc("cascade", cascade, phrases)
647:         refus = [p.get("id", "") for p in phrases
648:                  if cascade.analyser(p["texte"], p["langue"]).refus]
649:         rapport["tagger"] = {
650:             "nom": "cascade POS (tagger API DeepSeek)",
651:             "modele": MODELE_TAGGER,
652:             "seuil": SEUIL_TAGGER,
653:             "priorite": "pos → neuronal ; syntagmes, rôles et pragmatique → heuristique",
654:             "pos": mesure_tag["pos"],
655:             "syntagme": mesure_tag["syntagme"],
656:             "pragmatique": mesure_tag["pragmatique"],
657:             "fraction_semantique": mesure_tag["fraction_semantique"],
658:             "delta_pos": round(mesure_tag["pos"]["exactitude"] - mesure["pos"]["exactitude"], 4),
659:             "refus": len(refus),
660:  
… [790 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "        rapport[\"tagger\"] = {\n            \"nom\": \"cascade POS (tagger API DeepSeek)\",\n            \"modele\": MODELE_TAGGER,\n            \"seuil\": SEUIL_TAGGER,\n            \"priorite\": \"pos → … [1479 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "limit": 60, "offset": 380}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py</path>
<type>file</type>
<content>
380: 
381:             code, sortie, erreur = self._lancer(
382:                 self._client(tmp, transport), "analyser", TEXTE, "--tagger", "--json")
383:             self.assertEqual(code, 0, erreur)
384:             self.assertEqual(len(tentatives), 3, "le client doit réessayer avant de replier")
385:             donnees = json.loads(sortie)
386:             self.assertIn("réseau", donnees["refus"])
387:             self.assertEqual(donnees["source"], "cascade")
388:             self.assertEqual(_pos_map(donnees),
389:                              _pos_map(bl.Heuristique().analyser(TEXTE).json()))
390:             self.assertEqual({e["source"] for e in donnees["etiquettes"]
391:                               if e["niveau"] == "pos"}, {"heuristique"})
392:             self.assertIn("refus partiel", erreur)
393:             self.assertIn("réseau", erreur)
394:             self.assertIn("TAGGER API", erreur)
395: 
396:     def test_refus_du_modele_repli_heuristique(self) -> None:
397:         with tempfile.TemporaryDirectory() as tmp:
398:             def transpo
… [2299 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "new_string": "class TestMatriceW3(unittest.TestCase):\n    \"\"\"La matrice de W3 : le défaut hors ligne, le coût pour 1 000 phrases, zéro socket.\n\n    Les autres lignes de la matrice ont déjà leur tes … [4835 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -30", "description": "Run tests with new matrix cases"}`

  ```
test_cascade_remplace_les_pos (__main__.TestCascadeTagger.test_cascade_remplace_les_pos) ... ok
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
test_analyser_json_sans_tagger (__main__.TestDefaultInchange.test_analyser_json_sans_tagger) ... ok
test_evaluer_sans_t
… [1176 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nn=452\nappels=449; requetes=447; cache=2; tokens=65029; lat=443.813\nprompt=55572; completion=9457\nscale=1000/n\ndef r(x): return int(round(x*scale))\nout={\n 'phrases_mesurees': n,\n 'phrases_cible': 1000,\n 'appels': r(appels), 'requetes': r(requetes),  … [849 caractères tronqués]`

  ```
{
 "phrases_mesurees": 452,
 "phrases_cible": 1000,
 "appels": 993,
 "requetes": 989,
 "cache": 4,
 "tokens": 143869,
 "latence_s": 981.887,
 "tokens_entree": 122947,
 "tokens_sortie": 20923,
 "tokens_entree_par_phrase": 122.95,
 "tokens_sortie_par_phrase": 20.92,
 "tokens_par_phrase": 143.87,
 "latence_par_phrase_s": 0.9819,
 "latence_par_requete_s": 0.9929,
 "tokens_total": 143870,
 "cout_usd_hors_pointe": 0.031,
 "cout_usd_pointe": 0.062,
 "cache_chaud": {
  "tokens": 0,
  "requetes": 0,
  "cout_usd": 0.0,
  "latence_s": 0.139
 }
}
  ```

- **bash** `{"command": "python3 - <<'PY'\nn=452; p=55572; c=9457\nfor label, tm, om in [('hors_pointe',0.15,0.60),('pointe',0.30,1.20)]:\n    cost=(p*1000/n)*tm/1e6 + (c*1000/n)*om/1e6\n    print(label, cost, round(cost,4))\nprint('tokens exact', (p+c)*1000/n, round((p+c)*1000/n,0))\nprint('per phrase', (p+c)/ … [54 caractères tronqués]`

  ```
hors_pointe 0.030995575221238934 0.031
pointe 0.06199115044247787 0.062
tokens exact 143869.46902654867 143869.0
per phrase 143.86946902654867
  ```

- **bash** `{"command": "grep -rn \"W[0-9]\" docs/pilotage/semaine-2.md | head -30; grep -rn \"W4\\|W5\\|W6\" docs/pilotage/*.md reports/*.md | head -20", "description": "Find task numbering after W3"}`

  ```
(no output)
  ```

- **bash** `{"command": "tail -80 journal/2026-11-15/mesures.md", "description": "Inspect journal notes end"}`

  ```
| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) | `en-cours.md`, `README.md`, `mesures.md` (+7) |
| 02:13 | `292c70b5` | C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09 | `en-cours.md`, `README.md`, `docs.md` (+13) |
| 03:48 | `011b8b8e` | B2 — LES ATOMES NE PRÉDISENT PAS POS, SYNTAGMES NI ATTACHEMENT : SUR 28 ŒUVRES PROPRES, R² −0,092 / −0,160 / −0,092 (p 0,56 / 0,85 / 0,67) ; LE STYLE EST PRÉDIT (GRAPHÈMES +0,811, MOTS +0,657, NÉGATION +0,440, VERBES +0,429) MAIS ABSORBÉ PAR LA DATE (p_resid 0,76–1,0) | `en-cours.md`, `roadmap.md`, `README.md` (+18) |
| 04:03 | `2067a6f0` | B3 — LE CORPUS D'OR CIC V2 : 42/42 TYPES DE BRUJIN BIEN FORMÉS, 42/42 SHA256 PAR DEUX IMPLÉMENTATIONS, 36/36 PREUVES ET 42/42 TYPES ALTÉRÉS REJETÉS | `en-cours.md`, `roadmap.md`, `README.md` (+18) |
| 04:33 | `ee04ea91` | BILAN DE LA NUIT — LE TAGGER (95,75), LA BASE HONNÊTE (452), LA PHASE C/B (N2, S, R, PANINI) ET LES NÉGATIFS DITS | `en-cours.md`, `README.md`, `distribue.md` (+11) |
| 04:46 | `d23780d7` | D1 — LES EXEMPLES DU TAGGER ET DE LA 
… [5944 caractères tronqués]
  ```

- **bash** `{"command": "python3 /tmp/w3_mesure.py", "description": "Re-run real matrix after code change", "timeoutMs": 180000}`

  ```
{"nom": "defaut_sans_cle_analyser", "commande": "python3 tools/drave.py analyser Le chat dort. --json", "code": 0, "duree_s": 0.162, "stdout_octets": 5852, "stderr": ""}
{"nom": "defaut_sans_cle_evaluer", "commande": "python3 tools/drave.py evaluer --json", "code": 0, "duree_s": 1.358, "stdout_octets": 3165, "stderr": ""}
{"nom": "avec_cle_analyser", "commande": "python3 tools/drave.py analyser Le chat dort. --tagger --json", "code": 0, "duree_s": 1.326, "stdout_octets": 6117, "stderr": "drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.2 s"}
{"nom": "cle_invalide_analyser", "commande": "python3 tools/drave.py analyser Le chat dort. --tagger --json", "code": 4, "duree_s": 0.672, "stdout_octets": 0, "stderr": "drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne."}
{"nom": "reseau_coupe_analyser", "commande": "python3 tools/drave.py analyser Le chat dort. --tagger --json", "code": 0, "duree_s": 3.258, "stdout_octets": 6253, "stderr": "drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek:
… [254 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/w3-matrix.json'))\nfor k in ('avec_cle','cle_invalide','reseau_coupe'):\n    print(k, d[k]['code'], d[k]['duree_s'], d[k]['stdout_octets'])\n    print(' stderr', d[k]['stderr'])\nprint('avec cache', d['avec_cle']['cache'])\nprint('ze … [78 caractères tronqués]`

  ```
avec_cle 0 1.326 6117
 stderr drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.2 s
cle_invalide 4 0.672 0
 stderr drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.
reseau_coupe 0 3.258 6253
 stderr drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s
avec cache [{'usage': {'prompt_tokens': 116, 'completion_tokens': 14, 'total_tokens': 130, 'prompt_tokens_details': {'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 116}, 'modele': 'deepseek-flash', 'latence_s': 1.156}]
zero {'code_processus': 0, 'stdout': 'CODE 0\nDEEPSEEK False\nSOCKET True', 'stderr': ''}
  ```

- **bash** `{"command": "sed -n 1,80p reports/INDEX.md; echo ---; grep -n \"tagger\" reports/INDEX.md reports/README.md | head -20", "description": "Inspect reports index"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **746 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
| [aiguille-gpt-oss.md](aiguille-gpt-oss.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf |
| [alignement-verne.md](alignement-verne.md) | Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais) |
| [bilan-b11.md](bilan-b11.md) | Bilan B11 — ce qui tient, ce qui ne tient pas |
| [bilan-multi-materiel.md](bilan-multi-materiel.md) | Bilan multi-matériel — CPU, FPGA, GPU |
| [campagne-benefices.md](campagne-benefices.md) | Campagne 24 h — où Drave est à son meilleur, tâche par tâche |
| [fiche-nuit-17-10.md](fiche-nuit-17-10.md) | La nuit du 17 au 18 
… [11159 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,70p reports/README.md", "description": "Inspect reports README curated index"}`

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
| [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) | **Bilan** — la semaine 07 → 15/11 : le produit, Panini, la coordination, le harnais |
| [`rapport-bilan-nuit.md`](rapport-bilan-nuit.md) | **Bilan** — la nuit du 14 au 15/11 : le tagger, la base honnête, la phase C/B |
| [`rapport-gold-reel-50.md`](r
… [5852 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.md", "content": "# W3 — la matrice du tagger : le défaut reste hors ligne (code 0), `--tagger` est la seule porte qui peut sortir 4\n\n> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : * … [22059 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "grep -n \"0,9193\\|0,9198\" reports/rapport-tagger-defaut.md", "description": "Check typo in report"}`

  ```
29:- **N'est pas** : une nouvelle mesure de qualité (W2 la porte : 402 **0,9193 → 0,9643**, H50
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-tagger-defaut.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('402 **0,9193 → 0,9643**','402 **0,9198 → 0,9643**')\np.write_text(s,encoding='utf-8')\nprint('ok')\nPY", "description": "Fix W2 score typo"}`

  ```
ok
  ```

- **write** `{"content": "{\n  \"tache\": \"W3 — la matrice du tagger et le défaut\",\n  \"titre\": \"Le défaut reste hors ligne (code 0), --tagger est la seule porte qui peut sortir 4\",\n  \"date\": \"2026-11-15\",\n  \"ligne_roadmap\": \"R0.7 (le lecteur) / B13\",\n  \"head_mesure\": \"3439cb0c + ce diff (cha … [12437 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-tagger-defaut.json >/dev/null && echo \"JSON valide\"", "description": "Validate report JSON"}`

  ```
JSON valide
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-tagger-defaut.json'))\nc=d['cout_1000_phrases']\nb=c['base_mesuree']; e=c['extrapolation']\nfor k in ('appels','requetes','cache_local','tokens_entree','tokens_sortie','tokens_total'):\n    print(k, b[k], e[k], 'ratio', ro … [320 caractères tronqués]`

  ```
appels 449 993 ratio 2.2116
requetes 447 989 ratio 2.2125
cache_local 2 4 ratio 2.0
tokens_entree 55572 122947 ratio 2.2124
tokens_sortie 9457 20923 ratio 2.2124
tokens_total 65029 143869 ratio 2.2124
tokens total sum 143870 143869
cost check 0.031 0.062
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\nfor name in ('reports/rapport-tagger-defaut.md','reports/rapport-tagger-defaut.json'):\n    p=Path(name); s=p.read_text(encoding='utf-8')\n    s=s.replace('143 869','143 870').replace('143869','143870')\n    p.write_text(s,encoding='utf-8')\np … [247 caractères tronqués]`

  ```
ok
valide
reports/rapport-tagger-defaut.md:8:> après **3 essais**, repli heuristique explicite. **Coût pour 1 000 phrases** : **143 870
reports/rapport-tagger-defaut.md:170:| **tokens total** | **65 029** | **143 870** |
reports/rapport-tagger-defaut.md:189:tarif déplace le dollar, pas les **143 870 tokens**.
reports/rapport-tagger-defaut.md:198:tokens coûteront plus que 143 870 tokens. Le chiffre est donc **143 870 tokens pour 1 000
reports/rapport-tagger-defaut.md:244:- **Le prix et la latence.** **143 870 tokens** et **~16 min** pour 1 000 phrases : ce n'est
reports/rapport-tagger-defaut.md:274:  (143 870) sont stables, le prix ne l'est pas. Un cache hit côté API réduirait l'entrée ;
reports/rapport-tagger-defaut.json:7:  "verdict": "matrice mesurée : défaut sans clé code 0 et 0 socket ; avec clé code 0 (130 tokens, 1,156 s) ; clé invalide code 4, stdout vide ; réseau coupé code 0 après 3 essais, repli explicite ; coût 1 000 phrases = 143 870 tokens, 989 requêtes, 981,9 s, 0,031 $ hors pointe / 0,062 $ en pointe ; 21/21 tests.",
reports/rapport-tagger-defaut.json:160:      "tokens_total": 143870,
reports/rapport-tagger-defaut.json:265:    "Le tarif change : les dollars sont ceux
… [69 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.md</path>
<type>file</type>
<content>
1: # W3 — la matrice du tagger : le défaut reste hors ligne (code 0), `--tagger` est la seule porte qui peut sortir 4
2: 
3: > **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **W3** (semaine 2, J2
4: > après-midi) · **Date** : 2026-11-15 · **HEAD mesuré** : `3439cb0c` + ce diff (champ de coût
5: > additif) · **Verdict** : ✅ **la matrice est mesurée** — le **défaut sans clé** rend
6: > l'heuristique, **code 0**, **0 socket** ; avec clé, **code 0**, **130 tokens** et **1,16 s**
7: > pour une phrase ; **clé invalide**, **code 4**, `stdout` vide ; **réseau coupé**, **code 0**
8: > après **3 essais**, repli heuristique explicite. **Coût pour 1 000 phrases** : **143 870
9: > tokens**, **989 requêtes**, **981,9 s** de réseau, **~0,031 $ hors pointe / ~0,062 $ en
10: > pointe**. **Recommandation** : garder le **défaut hors ligne** et `--tagger` **opt-in** ; ne
11: > pas livrer `auto` maintenant, et si `auto` vient, **seulement si la clé existe** et **sans
12: > changer le code de sortie**. **21/21 tests**.
13: 
14: **En trois lignes.** (1) Le **défa
… [8106 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-tagger-defaut.md'); s=p.read_text(encoding='utf-8')\nold=\"\"\"Les quatre premières lignes sont des **mesures réelles** (CLI en sous-processus, cache neuf,\nclé jamais affichée). Les deux dernières sont les **refus du m … [580 caractères tronqués]`

  ```
ok
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.md", "offset": 121, "limit": 130}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.md</path>
<type>file</type>
<content>
121: code 4 · stdout 0 octet · 0,672 s
122: stderr : drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez
123:          DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY.
124:          Sans --tagger, le défaut reste l'heuristique hors ligne.
125: ```
126: 
127: Le contrôle 401/403 est **avant** le repli : une clé refusée n'est pas un refus de phrase. Le
128: test couvre `analyser` **et** `evaluer`, et vérifie que `stdout` reste **vide** : aucune
129: métrique n'est publiée, aucun repli heuristique n'est déguisé en cascade. Le message nomme les
130: trois sources de la clé, jamais sa valeur.
131: 
132: ### 3.4 Réseau coupé : 3 essais, puis repli explicite, code 0
133: 
134: ```
135: $ DEEPSEEK_BASE_URL=http://127.0.0.1:9 drave analyser "Le chat dort." --tagger --json
136: code 0 · stdout 6 253 octets · 3,258 s (3 essais : 1 s + 2 s d'attente)
137: stderr : drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek:
138:          réseau : [Errno 111] Connection refused
139:          drave: TAGGER API · modèle=deepseek-chat · a
… [7505 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.md", "offset": 251}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.md</path>
<type>file</type>
<content>
251: 
252: ## 5. Les contrôles négatifs
253: 
254: | contrôle | ce qui est mesuré | résultat |
255: |---|---|---|
256: | **paire défaut / `--tagger`** | même `HOME` vide, même texte | défaut **0** ; `--tagger` **4** : le code 0 du défaut n'est pas un 4 déguisé |
257: | **avec clé / clé invalide** | même transport, même texte | valide **0** + POS `neuronal` ; invalide **4** + `stdout` vide : le 4 vient bien de la clé |
258: | **avec clé / réseau coupé** | même client, endpoint fermé | valide **0** + POS `neuronal` ; coupé **0** + POS `heuristique` + `refus` : le repli est visible |
259: | **socket piégée** | `socket.socket` remplacé par une classe qui lève, défaut lancé | processus **0**, aucune exception, `tools.llm.deepseek` **non importé** |
260: | **cache chaud / cache neuf** | même run W2, cache local | **0** réseau, **0** token, **0 $** en chaud contre **65 029** tokens en neuf : le coût est le réseau, pas le CPU |
261: | **mutation 401/403** | retirer `if code: raise CleTaggerRefusee(code)` dans `_CascadeTagger.analyser` | `test_cle_invalide_code_4` **écho
… [4780 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 8, "offset": 18}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
18: | [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) | **Bilan** — la semaine 07 → 15/11 : le produit, Panini, la coordination, le harnais |
19: | [`rapport-bilan-nuit.md`](rapport-bilan-nuit.md) | **Bilan** — la nuit du 14 au 15/11 : le tagger, la base honnête, la phase C/B |
20: | [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
21: | [`rapport-gold-452.md`](rapport-gold-452.md) | **W1/R0.7** — le gold réel 452 : composition, split 402/H50, sha256, 10 candidats GP/SUB |
22: | [`rapport-tagger-h50.md`](rapport-tagger-h50.md) | **W2/R0.7** — le tagger sur le split : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/attachement 402 inchangés, fermé 402 **−1,55** ; la règle ne le rejette pas |
23: | [`rapport-protocole-date.md`](rapport-protocole-date.md) | **Panini** — le protocole à date contrôlée : 60 paires, trois strates |
24: | [`rapport-cic-v2.md`](rapport-cic-v2.md) | **Panini** — le CIC v2 : 42/42, les types clos, le sha256 sans hashlib |
25: | [`rapport-base-reel
… [179 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-tagger-h50.md`](rapport-tagger-h50.md) | **W2/R0.7** — le tagger sur le split : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/attachement 402 inchangés, fermé 402 ** … [617 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/index_reports.py 2>&1 | tail -5; grep -n \"rapport-tagger-defaut\" reports/INDEX.md", "description": "Regenerate reports index"}`

  ```
748 fiches → reports/INDEX.md
733:| [rapport-tagger-defaut.md](rapport-tagger-defaut.md) | W3 — la matrice du tagger : le défaut reste hors ligne (code 0), `--tagger` est la seule porte qui peut sortir 4 |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 50, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 09 h 25 HNE (W2 : tagger 402/H50)**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
11: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
12: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.
13: - **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
14: - **État** : **en pause** depuis le 05/11 (dernier heartbeat) ; la clôture J14.1 est portée par `e181ce02`.
15: - **Bloquants** : aucun.
16: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
17: 
18: ## Sessions en cours
19: 
20: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
21: > [`journal/sessions/`](../../j
… [2269 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 70, "offset": 78}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
78: - **Objectif final** : la production qui tient.
79: - **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondération) ; `kd2` et `rope2048` **arrêtés** ; **paire propre** : **3,1500** → **3,1119** (−0,06 ; −0,19 anglais) ; **repondération : −0,05** ; **2 048** ne bat pas 1 024 ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [production](../../reports/rapport-n2-production-fenetre.md), [erratum](../../reports/rapport-n2-distillation-native.md), [porte](../../reports/rapport-n2-porte-propre.md).
80: - **Ce que font les autres** : **hub**, **S**, **Pensée**.
81: - **Prochaine action** : la **porte propre (0,29)** ; le **2 048** est fini.
82: - **Bloquants** : aucun.
83: - **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).
84: 
85: ## Ce qui est en cours
86: 
87: - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coord
… [6920 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/*.md | wc -l; ls reports/*.json | wc -l; ls docs/**/*.md 2>/dev/null | wc -l", "description": "Count reports and docs files"}`

  ```
751
844
106
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md'); s=p.read_text(encoding='utf-8')\ns=s.replace('**Mis à jour : 2026-11-15, 09 h 25 HNE (W2 : tagger 402/H50)**',\n            '**Mis à jour : 2026-11-15, 10 h 30 HNE (W3 : la matrice du tagger)**')\nold='- ** … [2475 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"W2 — tagger\\|W3 — tagger\" docs/pilotage/roadmap.md", "description": "Find roadmap W2/W3 lines"}`

  ```
33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (4/5 familles ≥ 90 %) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) ; **W2 — tagger 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), fermé 402 −1,55** ([fiche](../../reports/rapport-tagger-h50.md)) | **R4.4 close** (limites nommées) ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; la suite : **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; **W3 — tagger par défaut** ; R2/R3 attendent N5/N4 |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 6, "offset": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
30: | **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
31: | **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise*
… [5971 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**W2 — tagger 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), fermé 402 −1,55** ([fiche](../../reports/rapport-tagger-h50.md)) ; **W3 — matrice du tagger : défaut hors ligne code 0, `--tagger` … [854 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md", "limit": 20, "offset": 75}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md</path>
<type>file</type>
<content>
75: v1 **46/46**, v2 **19/46** cadres (**16** non vides, F1 **0,5270**), tagger **609 appels /
76: 22 299 tokens / 155 s / ~0,02 $**. Le vérificateur est
77: [`tools/verifier_faq.py`](../../tools/verifier_faq.py), le relevé
78: [`faq.json`](../../reports/faq.json), la fiche
79: [`rapport-faq.md`](../../reports/rapport-faq.md).
80: 
81: ### E2 — les cas d'erreur du tagger : la clé refusée sort 4, le reste replie
82: 
83: Quatre cas, un transport factice, **18/18 tests**, **0 socket**. La **clé absente** sortait déjà
84: **4** ; la **clé invalide** (HTTP 401/403) rendait **0** avec un repli heuristique muet — elle
85: sort désormais **4**, message clair, `stdout` vide, sans repli. Le **réseau coupé** (3 essais du
86: client) et le **refus du modèle** (texte non JSON, JSON incomplet) restent des refus **par
87: phrase** : repli heuristique, code **0**, cause dans `refus`, POS `source=heuristique`. Un
88: transport valide donne code **0** et des POS neuronaux (contrôle négatif) ; retirer le contrôle
89: 401/403 fait échouer le test (`0 != 4`). [`fiche`](../../reports/r
… [147 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md", "new_string": "401/403 fait échouer le test (`0 != 4`). [`fiche`](../../reports/rapport-tagger-erreurs.md) ·\n[`JSON`](../../reports/rapport-tagger-erreurs.json).\n\n### W3 — la matrice du tagger : le défa … [1176 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"cout\\|--tagger\\|TAGGER API\\|evaluer\" docs/produit/README.md | head -40", "description": "Find tagger docs"}`

  ```
9:> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
11:> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
17:> **06/11**, et l'`evaluer` du § 3.3 a été relancé le **14/11** (gold vivant 612, `--par-langue
64:| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger` |
139:python3 tools/drave.py evaluer
168:python3 tools/drave.py evaluer --par-langue
190:complète est [`rapport-evaluer-langue.md`](../../reports/rapport-evaluer-langue.md).
379:python3 tools/drave.py evaluer --reel
383:**88,91 %**, F1 **79,06 %**, attachement **99,46 %**. Sans lui, `evaluer` publie la ligne
386:### 3.7 Le tagger en option — `--tagger`
389:python3 tools/drave.py analyser "Le chat dort." --tagger
390:python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
391:python3 tools/drave.py evaluer --tagger
404:TAGGER API  modèle=deepseek-chat · appels=1 · réseau=0 · cache=1 · tokens=0 · latence=0.0 s
422:| **clé invalide** (HTTP 401/403) | refuse de démarrer, **sans repli** | **4** | vide | `drave: dépendance
… [2817 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 100, "offset": 386}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
386: ### 3.7 Le tagger en option — `--tagger`
387: 
388: ```bash
389: python3 tools/drave.py analyser "Le chat dort." --tagger
390: python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
391: python3 tools/drave.py evaluer --tagger
392: ```
393: ```
394: drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
395: langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
396: POS  Le/DET chat/NOUN dort/VERB ./PONCT
397: SYNTAGMES
398:   GN   [0:7]   Le chat  rôle=agent     → dort
399:   GV   [8:12]  dort     rôle=predicat  → chat
400: PRAGMATIQUE
401:   phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
402: COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
403:             phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
404: TAGGER API  modèle=deepseek-chat · appels=1 · réseau=0 · cache=1 · tokens=0 · latence=0.0 s
405: ```
406: 
407: Ici le cache disque avait déjà la réponse ; un **premier** appel affiche `réseau=1`
… [6003 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/README.md'); s=p.read_text(encoding='utf-8')\nold=\"\"\"**`evaluer --tagger`.** La commande mesure **les deux** lectures et publie l'écart et le coût\n(la ligne `TAGGER API DEEPSEEK` sur 20 phrases, exemple réel) :\"\"\"\n … [1874 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/README.md'); s=p.read_text(encoding='utf-8')\nold=\"\"\"**Le coût.** **Un appel par phrase** (le tagger de syntagmes, qui était appelé sans contribuer,\na été retiré), **22 299 tokens** et **155 s** pour les **612 phrases* … [1170 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -5", "description": "Run tagger tests"}`

  ```
----------------------------------------------------------------------
Ran 21 tests in 5.704s

OK
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -8", "description": "Run product tests"}`

  ```
....................
----------------------------------------------------------------------
Ran 20 tests in 11.929s

OK
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run documentation review"}`

  ```
revue de documentation · 751 fiche(s) · 844 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20", "description": "Verify state document"}`

  ```
en-cours · 1746 mots · 7 sections · 4 session(s) · 11 puces · 5 questions
  ❌ 1 anomalie(s) :
     · 11 puces dans « Ce qui est en cours » > 10
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -20", "description": "Verify journal"}`

  ```
journal · 47 jour(s) · 208 session(s) · 2609 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -20; python3 tools/taille_documents.py 2>&1 | tail -20", "description": "Verify schemas and doc size"}`

  ```
schémas · 464 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2601    226   T1   2800  reports/README.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4116 mots (budget 4 000)

  avertissements :
     · 59 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qw
… [276 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport subprocess\nfor label,cmd in [('HEAD','git show HEAD:docs/pilotage/roadmap.md'),('WORK','cat docs/pilotage/roadmap.md')]:\n    s=subprocess.check_output(cmd,shell=True,text=True)\n    print(label, len(s.split()))\nPY", "description": "Compare roadmap word counts … [10 caractères tronqués]`

  ```
HEAD 9324
WORK 9364
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md'); s=p.read_text(encoding='utf-8')\nold='**W2 — tagger 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), fermé 402 −1,55** ([fiche](../../reports/rapport-tagger-h50.md)) ; **W3 — matrice du tagger : défaut hor … [1103 caractères tronqués]`

  ```
ok
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4116 mots (budget 4 000)

  avertissements :
     · 59 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4116 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "grep -n \"T0\\|AGENTS\\|en-cours\\|une t\" tools/taille_documents.py | head -40", "description": "Understand T0 composition"}`

  ```
5:  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
27:    ("T0", "AGENTS.md", 1200),
28:    ("T0", "docs/pilotage/en-cours.md", 2000),
32:    ("T0", "docs/methode/*.md", 1200),
112:            if cat in ("T0", "T1"):
140:    # T0 : la somme des trois lectures par défaut
145:    # Le T0 est « AGENTS + en-cours + UN document de tâche », et le document de tâche est un
146:    # T0 (≤ 1 200 mots) : les trois documents `specifiques` ci-dessus sont des T1, avec leur
147:    # propre budget. Les compter ici faisait payer 1 579 mots au T0 (organisation-du-depot.md)
148:    # au lieu des 1 134 du plus gros T0 — un budget faux de 445 mots, dans le sens qui bloque.
150:    t0 = poids("AGENTS.md") + poids("docs/pilotage/en-cours.md") + max(
154:        violations.append(f"T0 : {t0} mots (AGENTS + en-cours + une tâche) > budget 4 000")
163:    print(f"  T0 max : {t0} mots (budget 4 000)")
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\ns=Path('docs/pilotage/en-cours.md').read_text(encoding='utf-8')\nstart=s.index('## Ce qui est en cours')\nend=s.index('## Les chiffres de l\\'état')\nsection=s[start:end]\nfor line in section.splitlines():\n    if line.startswith('- '):\n      … [140 caractères tronqués]`

  ```
26 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; **19/19 ve
28 - **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,785
33 - **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 reje
20 - **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion ré
34 - **W2 — tagger 402/H50** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,
75 - **W3 — la matrice du tagger** : défaut sans clé **code 0**, heuristique, **0 socket** ; 
52 - **Panini J2.1–J3.2 + B2** : **14 atomes** ; UDHR **418/438** ; J3.2 : **5/21** langues (
33 - **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / 
17 - **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1 inter-traditions à ±10
34 - **Panini J12.1–J12.2 + B3** : CIC **42/42** verdicts ; B3 : **42/42** types de Bruijn va
33 - **J5.1 / J10.1 / J13.1 / J14.1 — bilans et clôture** : F1 **0,7902** (tagger **0,9475**)
total section 423
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md'); s=p.read_text(encoding='utf-8')\nstart=s.index('## Ce qui est en cours')\nend=s.index(\"## Les chiffres de l'état\")\nnew='''## Ce qui est en cours\n\n- **S — les structures** : 61/61 types, 144/144 rôles,  … [3155 caractères tronqués]`

  ```
ok
  en-cours · 1655 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  avertissements :
     · 59 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4025 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md'); s=p.read_text(encoding='utf-8')\nrepls=[\n('402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65), fermé 402 **−1,55** ; défaut sans clé','402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607* … [764 caractères tronqués]`

  ```
ok
  en-cours · 1624 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  avertissements :
     · 59 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -10", "description": "Re-run documentation review"}`

  ```
revue de documentation · 751 fiche(s) · 844 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -6; python3 tools/verifier_schemas.py 2>&1 | tail -4", "description": "Verify journal and schemas"}`

  ```
journal · 47 jour(s) · 208 session(s) · 2609 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  schémas · 464 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "git status --short", "description": "Show working tree status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/2026-11-15/mesures.md
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
 M tools/drave.py
 M tools/tests/test_tagger_api.py
?? reports/rapport-s-paragraphes.md
?? reports/rapport-tagger-defaut.json
?? reports/rapport-tagger-defaut.md
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "git diff --stat", "description": "Show diff stats"}`

  ```
docs/pilotage/en-cours.md               |  28 +-
 docs/pilotage/roadmap.md                |   2 +-
 docs/produit/README.md                  |  27 +-
 journal/2026-11-15/mesures.md           |  13 +
 reports/INDEX.md                        |   5 +-
 reports/README.md                       |   1 +
 reports/pensee-coherence-fiches-v7.json |  19 +
 reports/pensee-dev-test-v10.json        |   2 +-
 reports/pensee-quatre-modes.json        | 734 ++++++++++++++++++--------------
 reports/rapport-audit-v7.md             |   6 +-
 reports/rapport-coherence-fiches-v7.md  |  17 +-
 reports/rapport-dev-test-v10.md         |   2 +-
 reports/rapport-pensee-v12.md           |   4 +-
 reports/rapport-spans-chunker.md        |  13 +-
 tools/chantier/plan.json                |  86 ++++
 tools/drave.py                          |  26 ++
 tools/tests/test_tagger_api.py          |  90 ++++
 17 files changed, 712 insertions(+), 363 deletions(-)
  ```

- **bash** `{"command": "git diff reports/INDEX.md", "description": "Inspect index diff"}`

  ```
diff --git a/reports/INDEX.md b/reports/INDEX.md
index dbd4bb75..03a54867 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **746 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **748 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -730,8 +730,9 @@
 | [rapport-sprint-24h.md](rapport-sprint-24h.md) | Sprint 24 h — bilan B12 → B18 |
 | [rapport-tableau-mesures.md](rapport-tableau-mesures.md) | J13.1 — la table des mesures : F1 0,7533 → 0,7902, attachement 236/237 → 238/238, base 612/602 |
 | [rapport-tableaux-casses.md](rapport-tableaux-casses.md) | Un tableau qui ne rend pas est un tableau qui n'existe pas — 17 lignes, 9 fichiers, et une porte |
+| [rapport-tagger-defaut.md](rapport-tagger-defaut.md) | W3 — la matrice du tagger : le défaut reste hors ligne (code 0), `--tagger` est la seule porte qui peut sortir 4 |
 | [rapport-tagger-erreurs.md](rapport-tagger-erreurs.md) | E2 — les cas d'erreur de `--tagger` : clé refusée = code 4, réseau 
… [854 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"s-paragraphes\\|s-paragraphe\" reports/INDEX.md | head", "description": "Check untracked report in index"}`

  ```
711:| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
  ```

- **bash** `{"command": "git ls-files reports/rapport-s-paragraphes.md; git show HEAD:reports/INDEX.md | grep -c \"s-paragraphes\"; git diff reports/INDEX.md | grep \"s-paragraphes\"", "description": "Check if s-paragraphes tracked"}`

  ```
1
[exit code: 1]
  ```

- **bash** `{"command": "git diff tools/drave.py tools/tests/test_tagger_api.py", "description": "Review code and test diff"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index 045d895d..76c0715a 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -245,6 +245,30 @@ def _cout_tagger(stats: dict) -> dict:
             "modeles_renvoyes": dict(stats["modeles"])}
 
 
+def _cout_pour_phrases(cout: dict, mesurees: int, cible: int) -> dict:
+    """Le coût d'un lot de `cible` phrases, au prorata du lot **mesuré**.
+
+    Le tagger fait **un appel par phrase** : le coût est linéaire en nombre de phrases. On ne
+    modélise pas la longueur des phrases (le prompt la porte), donc ce chiffre vaut pour un lot
+    de même longueur moyenne que le lot mesuré. `mesurees` est le nombre de phrases réellement
+    passées au tagger ; il ne doit pas être confondu avec le nombre d'appels (le cache mémoire
+    peut en servir plusieurs).
+    """
+    mesurees = max(1, int(mesurees))
+    cible = max(0, int(cible))
+    ratio = cible / mesurees
+    return {
+        "phrases": cible,
+        "phrases_mesurees": mesurees,
+        "modele": cout.get("modele", MODELE_TAGGER),
+        "appels": int(round(cout.get("appels", 0) * ratio)),
+        "requetes": int(round(cout.get("requetes", 0) * ratio)),
+        "cache": int(ro
… [6110 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,80p tools/toutes-les-portes.sh", "description": "Inspect all-gates script"}`

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
… [2800 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/toutes-les-portes.sh", "description": "Run all repository gates", "run_in_background": true}`

  ```
started background job bash-86
  ```

- **bash** `{"command": "git diff docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/produit/README.md journal/2026-11-15/mesures.md reports/README.md | sed -n 1,240p", "description": "Review docs and journal diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index b63d9194..e94d1c9d 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 09 h 25 HNE (W2 : tagger 402/H50)**
+**Mis à jour : 2026-11-15, 10 h 30 HNE (W3 : la matrice du tagger)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -84,19 +84,15 @@
 
 ## Ce qui est en cours
 
-- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
-- **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
-- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** ([FAQ](../.
… [24001 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/produit/README.md'); s=p.read_text(encoding='utf-8')\nold=\"\"\"a été retiré). La référence mesurée est la passe API de W2 sur **452 phrases** : **65 029\ntokens** (55 572 d'entrée + 9 457 de sortie), **447 requêtes** et **443,8 s … [1098 caractères tronqués]`

  ```
ok
  avertissements :
     · 59 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **job_output** `{"job_id": "bash-86"}`

  ```
=== PASSE COMPLÈTE DES PORTES (85 portes, borne 1800 s) ===
    journaux : work/portes-1115-09h53
[status: running]
  ```

- **bash** `{"command": "git diff --check -- tools/drave.py tools/tests/test_tagger_api.py reports/rapport-tagger-defaut.md reports/rapport-tagger-defaut.json docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/produit/README.md journal/2026-11-15/mesures.md reports/README.md reports/INDEX.md", "description … [29 caractères tronqués]`

  ```
(no output)
  ```

- **job_output** `{"job_id": "bash-86"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -5 work/portes-1115-09h53/registre.txt 2>/dev/null; wc -l work/portes-1115-09h53/registre.txt 2>/dev/null", "description": "Check gate progress"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "sed -n 1,80p tools/porte-produit.sh", "description": "Inspect product gate"}`

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
… [2142 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.json", "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.json</path>
<type>file</type>
<content>
1: {
2:   "tache": "W3 — la matrice du tagger et le défaut",
3:   "titre": "Le défaut reste hors ligne (code 0), --tagger est la seule porte qui peut sortir 4",
4:   "date": "2026-11-15",
5:   "ligne_roadmap": "R0.7 (le lecteur) / B13",
6:   "head_mesure": "3439cb0c + ce diff (champ de coût additif)",
7:   "verdict": "matrice mesurée : défaut sans clé code 0 et 0 socket ; avec clé code 0 (130 tokens, 1,156 s) ; clé invalide code 4, stdout vide ; réseau coupé code 0 après 3 essais, repli explicite ; coût 1 000 phrases = 143 870 tokens, 989 requêtes, 981,9 s, 0,031 $ hors pointe / 0,062 $ en pointe ; 21/21 tests.",
8:   "recommande": {
9:     "defaut": "heuristique, CPU, hors ligne, déterministe, code 0, 0 socket",
10:     "tagger": "opt-in, code 0 avec clé, code 4 sans clé ou clé refusée",
11:     "auto": "non implémenté ; si un jour, seulement avec une clé présente et sans changer le code de sortie",
12:     "decision": "statu quo — garder le défaut hors ligne et --tagger opt-in ; pas de auto en W3 ; J5 applique ou rejette"
13:   },
14:   "dispositif": {
15:  
… [3022 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-86"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ls -ld work/portes-1115-09h53 2>&1; ls work/portes-1115-09h53 2>/dev/null | tail -5; tail -3 work/portes-1115-09h53/registre.txt 2>/dev/null", "description": "Check gate logs progress"}`

  ```
drwxr-xr-x. 1 stephane stephane 54 15 nov 09:53 work/portes-1115-09h53
porte-adaptateur-sortie.log
[exit code: 1]
  ```

- **bash** `{"command": "tail -5 work/portes-1115-09h53/porte-adaptateur-sortie.log 2>/dev/null; ps -o pid,etime,cmd -C python3 | head -10", "description": "Check first gate progress"}`

  ```
porte de l'adaptateur de sortie — Qwen2.5-0.5B-Q8_0.gguf · plage 0:8 · 256 jetons
    PID     ELAPSED CMD
   3002 11-14:19:53 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
2725542    17:40:21 python3 src/app.py --no-browser
3773802       57:00 python3 tools/chantier/superviseur.py boucle --budget 23400 --timeout 3600
  ```

- **bash** `{"command": "sed -n 1,40p tools/porte-adaptateur-sortie.sh; grep -n \"timeout\\|llama\\|python\" tools/porte-adaptateur-sortie.sh | head", "description": "Inspect slow gate"}`

  ```
#!/bin/bash
# porte-adaptateur-sortie.sh — l'écriture d'un GGUF est-elle FIDÈLE, et l'adaptateur de sortie
# fait-il quelque chose ?
#
# POURQUOI CETTE PORTE. N4 (le chemin court entraîné) a été mesuré en torch le 14/10
# (`reports/rapport-n4-dessin-b.md`) ; la **porte d'exécution** consiste à rendre ce modèle
# exécutable par le MOTEUR — donc à écrire un GGUF (`tools/exporter_gguf_dense.py`, dense Qwen2 :
# biais q/k/v, tête liée) et à poser le lecteur appris sur le chemin tronqué
# (`--adaptateur-sortie`). Deux façons de se tromper en silence, et c'est ce qu'on vérifie :
#
#   1. un GGUF écrit de travers (dimensions inversées, quantification refaite, métadonnées
#      perdues) — le moteur le lirait quand même et rendrait un AUTRE modèle : la porte compare
#      donc les chiffres du fichier RÉÉCRIT à ceux de l'ORIGINAL, sur place ;
#   2. un drapeau qui ne fait rien — le défaut le plus coûteux du dépôt. L'invariant d'identité
#      (adaptateur = I ⇒ chiffre EXACTEMENT identique) ne suffit pas à l'exclure : une échelle
#      globale est absorbée par la norme finale, donc la porte vérifie AUSSI qu'un adaptateur qui
#      n'est pas une échelle globale CHANGE le chiffre, et que l
… [1010 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 45, "offset": 540}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
540:     ]
541:     tagger = rapport.get("tagger")
542:     if tagger:
543:         tp, ts, cout = tagger["pos"], tagger["syntagme"], tagger["cout"]
544:         lignes += [
545:             "",
546:             "TAGGER API DEEPSEEK (option --tagger)",
547:             f"  POS         exactitude {_pct(tp['exactitude'])} "
548:             f"(fermé {_pct(tp['exactitude_ferme'])}, ouvert {_pct(tp['exactitude_ouvert'])}) "
549:             f"· Δ {_points(tagger['delta_pos'])} vs heuristique",
550:             f"  SYNTAGMES   F1 {_pct(ts['f1'])} (tête {_pct(ts['tete']['f1'])}) "
551:             "— conservés à l'heuristique",
552:             f"  COÛT        appels {cout['appels']} · réseau {cout['requetes']} "
553:             f"· cache {cout['cache']} · tokens {cout['tokens']} · modèle {cout['modele']}",
554:         ]
555:         renvoyes = cout.get("modeles_renvoyes") or {}
556:         if renvoyes and set(renvoyes) - {cout["modele"]}:
557:             lignes.append(f"  modèle renvoyé : {', '.join(sorted(renvoyes))}")
558:         if tagger.get("refus"):
559:             detail 
… [1640 caractères tronqués]
  ```

- **bash** `{"command": "ls work/portes-1115-09h53 | wc -l; tail -3 work/portes-1115-09h53/registre.txt 2>/dev/null; tail -2 work/portes-1115-09h53/porte-adaptateur-sortie.log 2>/dev/null", "description": "Check gate progress again"}`

  ```
1
porte de l'adaptateur de sortie — Qwen2.5-0.5B-Q8_0.gguf · plage 0:8 · 256 jetons
  ```

- **bash** `{"command": "ps -eo pid,etime,pcpu,pmem,cmd | grep -E \"porte-adaptateur|drave-core|llama|gguf\" | grep -v grep | head -10", "description": "Check gate process activity"}`

  ```
3923673       00:51  0.0  0.0 timeout 1800 bash tools/porte-adaptateur-sortie.sh
3923674       00:51  0.0  0.0 bash tools/porte-adaptateur-sortie.sh
3930314       00:02  0.0  0.0 bash tools/porte-adaptateur-sortie.sh
3930315       00:02  612  0.5 ./drave-core/target/release/drave /tmp/porte-adaptateur/reecrit.gguf --ppl /tmp/porte-adaptateur/morceau.txt --limit 256 --ctx 256 --threads 8 --couches 0:8 --tete-partielle
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys; sys.path[:0]=['.','tools']\nimport drave\nprint(drave._cout_pour_phrases({'modele':'m','appels':2,'requetes':1,'cache':0,'tokens':34,'latence_s':1.0},2,1000))\nprint(drave._cout_pour_phrases({'appels':0,'requetes':0,'cache':0,'tokens':0,'latence_s':0.0},0,0 … [61 caractères tronqués]`

  ```
{'phrases': 1000, 'phrases_mesurees': 2, 'modele': 'm', 'appels': 1000, 'requetes': 500, 'cache': 0, 'tokens': 17000, 'latence_s': 500.0}
{'phrases': 0, 'phrases_mesurees': 1, 'modele': 'deepseek-chat', 'appels': 0, 'requetes': 0, 'cache': 0, 'tokens': 0, 'latence_s': 0.0}
  ```

- **bash** `{"command": "wc -l work/portes-1115-09h53/registre.txt 2>/dev/null; tail -3 work/portes-1115-09h53/registre.txt 2>/dev/null; ls work/portes-1115-09h53 | tail -3", "description": "Check gate progress"}`

  ```
porte-adaptateur-sortie.log
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 60000, "wait": true}`

  ```
porte-adaptateur-sortie ✅                          76 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
[status: running]
  ```

- **bash** `{"command": "grep -rln \"test_tagger_api\" tools/porte-*.sh tools/*.sh | head", "description": "Find gate running tagger tests"}`

  ```
(no output)
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 120000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "wc -l work/portes-1115-09h53/registre.txt 2>/dev/null; tail -3 work/portes-1115-09h53/registre.txt 2>/dev/null; ls work/portes-1115-09h53 | tail -3", "description": "Check gate progress"}`

  ```
4 work/portes-1115-09h53/registre.txt
porte-audit-drapeaux 0 177
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-balayage.log
porte-bloc-code.log
registre.txt
  ```

- **bash** `{"command": "sed -n 84,100p docs/pilotage/en-cours.md", "description": "Review compressed state section"}`

  ```
## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
- **N2 — en pause** : commande **`eval_longueurs.py --rope --val <dir>`** (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** ([FAQ](../../reports/rapport-faq.md)), **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
- **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut sans clé **code 0**, **0 socket** ; `--tagger` sans clé ou clé refusée **code 4** ; réseau coupé **code 0** + repli ; **1 000 phrases = 143 870 tokens / 0,031 $ hors poin
… [1625 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 180000, "wait": true}`

  ```
porte-audit-drapeaux   ✅                         177 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          16 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          16 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          50 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          83 s    ✅ le canal diffusé par fichier change la région du milieu
[status: running]
  ```

- **bash** `{"command": "python3 -m pytest -q tools/tests/test_tagger_api.py 2>&1 | tail -8", "description": "Run tagger tests under pytest"}`

  ```
.....................                                                    [100%]
21 passed in 7.00s
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 240000, "wait": true}`

  ```
porte-bus-socket       ✅                         104 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard        ✅                          35 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne
  porte-cerveau          ✅                          10 s    ✅ porte tenue (quatre facultés composent, chacune reste active, le tout est déterministe)
  porte-cic              ✅                          13 s  ✅ porte CIC verte : 42/42 verdicts, empreintes, de Bruijn, sha256 2e implémentation,
  porte-consolidation    ✅                          91 s    ✅ porte tenue (fusion exacte : nulle ⇒ identique, réelle ⇒ visible, lecteur ⇒ hors fichier)
[status: running]
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 240000, "wait": true}`

  ```
porte-coupe            ✅                         156 s    ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit
[status: running]
  ```

- **bash** `{"command": "awk '$2 != 0' work/portes-1115-09h53/registre.txt; tail -2 work/portes-1115-09h53/registre.txt", "description": "Check for red gates so far"}`

  ```
porte-consolidation 0 91
porte-coupe 0 156
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 300000, "wait": true}`

  ```
porte-cycle-c2         ✅                         147 s    ✅ porte tenue (chaîne exacte · pas 1 exact · borné · coût dit · trajectoire déterministe ·
  porte-deepseek         ✅                           0 s    ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
  porte-delais           ✅                          25 s    ✅ le temps, lui, augmente : 8.48 s → 12.34 s (+3.9 s ≈ 50 ms × 64 pas)
  porte-diff-couche      ✅                          21 s    ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé
  porte-document         ✅                           6 s  ✅ porte document verte
  porte-echange-experts  ✅                          61 s    PORTE TENUE
[status: running]
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 300000, "wait": true}`

  ```
porte-episodique       ✅                         204 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           1 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          28 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                           9 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
[status: running]
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 300000, "wait": true}`

  ```
porte-gain             ✅                         249 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
[status: running]
  ```

### 👤 Utilisateur

You are repeating the exact same tool call with identical arguments. Carefully analyze the previous result before calling again: if the task is not complete, try a different approach or different arguments instead of repeating the call.

- **bash** `{"command": "python3 - <<'PY'\nimport json, re, pathlib\nmd=pathlib.Path('reports/rapport-tagger-defaut.md').read_text(encoding='utf-8')\nd=json.loads(pathlib.Path('reports/rapport-tagger-defaut.json').read_text(encoding='utf-8'))\nchecks={\n '143 870': d['cout_1000_phrases']['extrapolation']['token … [929 caractères tronqués]`

  ```
143 870 ok dans md
122 947 ok dans md
20 923 ok dans md
989 ok dans md
993 ok dans md
0,031 ok dans md
0,062 ok dans md
test test_analyser_tagger_json présent
test test_cle_invalide_code_4 présent
test test_cout_pour_1000_phrases présent
test test_defaut_n_ouvre_aucune_socket présent
test test_defaut_sans_cle_code_0 présent
test test_modele_json_incomplet_repli_heuristique présent
test test_refus_du_modele_repli_heuristique présent
test test_reseau_coupe_repli_heuristique présent
test test_tagger_api présent
  ```

- **bash** `{"command": "grep -n \"0,9193\\|143 869\\|0.031\\|0.062\" reports/rapport-tagger-defaut.md reports/rapport-tagger-defaut.json", "description": "Search for stale numbers"}`

  ```
reports/rapport-tagger-defaut.md:9:> tokens**, **989 requêtes**, **981,9 s** de réseau, **~0,031 $ hors pointe / ~0,062 $ en
reports/rapport-tagger-defaut.md:174:| **prix hors pointe** (entrée miss 0,15 $/M, sortie 0,60 $/M) | **0,0140 $** | **0,0310 $** |
reports/rapport-tagger-defaut.md:175:| **prix en pointe** (0,30 $/M, 1,20 $/M) | **0,0280 $** | **0,0620 $** |
reports/rapport-tagger-defaut.json:7:  "verdict": "matrice mesurée : défaut sans clé code 0 et 0 socket ; avec clé code 0 (130 tokens, 1,156 s) ; clé invalide code 4, stdout vide ; réseau coupé code 0 après 3 essais, repli explicite ; coût 1 000 phrases = 143 870 tokens, 989 requêtes, 981,9 s, 0,031 $ hors pointe / 0,062 $ en pointe ; 21/21 tests.",
reports/rapport-tagger-defaut.json:190:        "hors_pointe": 0.0310,
reports/rapport-tagger-defaut.json:191:        "pointe": 0.0620
  ```

- **bash** `{"command": "grep -n \"18 tests\\|21 tests\\|tests\" tools/tests/test_tagger_api.py | head -10", "description": "Check test docstring counts"}`

  ```
21:commande dans un `HOME` vide. Le fichier passe par `python3 tools/tests/test_tagger_api.py`
  ```

- **bash** `{"command": "sed -n 1,80p docs/pilotage/references-non-regression.md", "description": "Read tolerated red gates"}`

  ```
# Références de non-régression

> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
> `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
> `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
> `work/portes/passe-1311-23h15.log`.
>
> **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
> heartbeat `e181ce02` rafraîchi) ; `porte-indice` et `porte-melange` restent **rouges
> structurelles** (indice 482 contre témoin 459 ; état de A sans son code). Journaux
> `work/portes/verif-cloture/`.
> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
> échouait sur une ancre du banc pilote (« < 2,5 ») que la réécriture de la roadma
… [3886 caractères tronqués]
  ```

- **bash** `{"command": "awk '$2 != 0' work/portes-1115-09h53/registre.txt; wc -l < work/portes-1115-09h53/registre.txt", "description": "Check gate progress and reds"}`

  ```
27
  ```

- **bash** `{"command": "sed -n 34,40p reports/rapport-tagger-defaut.md", "description": "Check table intro"}`

  ```
## 1. La matrice, en une table

Les six premières lignes sont des **mesures réelles** (CLI en sous-processus, cache neuf,
clé jamais affichée). Les deux suivantes sont les **refus du modèle** couverts par les tests :
on ne peut pas les provoquer à volonté sur l'API réelle. La dernière est le **contrat de
calcul** du coût, testé sur un transport factice.
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 300000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "wc -l < work/portes-1115-09h53/registre.txt; tail -2 work/portes-1115-09h53/registre.txt; ps -eo pid,etime,pcpu,cmd | grep -E \"porte-|drave-core/target\" | grep -v grep | tail -5", "description": "Check current gate activity"}`

  ```
27
porte-fusion 0 9
porte-gain 0 249
4088084       09:55  0.0 timeout 1800 bash tools/porte-greffe.sh
4088085       09:55  0.0 bash tools/porte-greffe.sh
4093363       00:24  0.0 bash tools/porte-greffe.sh
4093364       00:24  863 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --prompt  Division . On August 1 , the 23rd Regiment was in a new sector of which it had only a limited knowledge . It took over a 16 @,@ 000 yards ( 15 @,@ 000 m ) Naktong River front without its 3rd Battalion which had been attached to the US 1st Cavalry Division to the north . Colonel Paul L. Freeman , the regimental commander , deployed the 1st Battalion on the high ground along the river with the three companies abreast . The 1st Battalion , under US Lieutenant Colonel Claire E. Hutchin , Jr . , outposted the hills with platoons and squads . He placed the 2nd Battalion in a reserve position 8 miles ( 13 km ) behind the 1st Battalion and in a position where it commanded the road net in the regimental sector . On August 31h the 2nd Division moved E Company south to a reserve position in the 9th Infantry sector .    Two roads ran through the regimental sector from the Naktong River 
… [5310 caractères tronqués]
  ```

- **bash** `{"command": "python3 -m py_compile tools/drave.py tools/tests/test_tagger_api.py && echo \"compile ok\"", "description": "Compile changed Python files"}`

  ```
compile ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/tests/test_tagger_api.py'); s=p.read_text(encoding='utf-8')\nold=\"\"\"        client = _FauxClient()\n        ancien_client = drave._client_tagger\n        evaluateur = drave._module_evaluation()\n        chargeur = evaluateur.c … [3307 caractères tronqués]`

  ```
ok
Le défaut ne charge pas le client réseau et ne construit aucune socket. ... ok
test_defaut_sans_cle_code_0 (__main__.TestMatriceW3.test_defaut_sans_cle_code_0)
Sans clé, le défaut rend l'heuristique, code 0, et n'appelle jamais le tagger. ... ok

----------------------------------------------------------------------
Ran 21 tests in 5.868s

OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-tagger-defaut.md'); s=p.read_text(encoding='utf-8')\nold='| **extrapolation ×500** | 2 phrases factices, 17 tokens/appel | `cout_pour_1000_phrases` = **1 000 appels**, **17 000 tokens**, exactement **×500** : le facteur … [1902 caractères tronqués]`

  ```
ok
json-ok
reports/rapport-tagger-defaut.md:19:(3) Le coût du même câblage pour **1 000 phrases** est une **extrapolation linéaire** de la
reports/rapport-tagger-defaut.md:51:| **coût 1 000 phrases** | `evaluer --tagger --json` (2 phrases, transport factice) | **0** | `cout_pour_1000_phrases` | extrapolation ×500 | `TestMatriceW3.test_cout_pour_1000_phrases` |
reports/rapport-tagger-defaut.md:262:| **extrapolation par phrase** | 2 phrases **identiques** : 1 appel, 17 tokens | `cout_pour_1000_phrases` = **500 appels**, **8 500 tokens** : l'extrapolation suit les **phrases**, pas les appels (la différence 449 / 452 de W2) |
reports/rapport-tagger-defaut.md:271:- **Le coût 1 000 est une extrapolation**, pas un run de 1 000 phrases. La base est 452
reports/rapport-tagger-defaut.md:324:`tagger.cout_pour_1000_phrases` (extrapolation du run mesuré) ; le chiffre de référence de
reports/rapport-tagger-defaut.json:18:    "cout": "extrapolation linéaire de la passe API W2 (452 phrases, 65 029 tokens, 443,813 s) à 1 000 phrases",
reports/rapport-tagger-defaut.json:154:    "extrapolation": {
reports/rapport-tagger-defaut.json:218:      "extrapolation linéaire, pas un run réel de 1 000 phrases"

… [240 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-tagger-defaut.md'); s=p.read_text(encoding='utf-8')\ns=s.replace('| **coût 1 000 phrases** | `evaluer --tagger --json` (2 phrases, transport factice) | **0** | `cout_pour_1000_phrases` | extrapolation ×500 | `TestMatric … [352 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -4", "description": "Re-run tagger tests"}`

  ```
----------------------------------------------------------------------
Ran 21 tests in 5.821s

OK
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -5; python3 tools/verifie_en_cours.py 2>&1 | tail -4", "description": "Re-run doc and state checks"}`

  ```
revue de documentation · 751 fiche(s) · 844 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1624 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "wc -l < work/portes-1115-09h53/registre.txt; tail -2 work/portes-1115-09h53/registre.txt", "description": "Check gate count"}`

  ```
27
porte-fusion 0 9
porte-gain 0 249
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 240000, "wait": true}`

  ```
porte-greffe           ✅                         780 s    ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE
[status: running]
  ```

- **bash** `{"command": "ls .git/hooks/pre-commit 2>/dev/null; sed -n 1,80p .git/hooks/pre-commit 2>/dev/null", "description": "Inspect pre-commit hook"}`

  ```
.git/hooks/pre-commit
#!/bin/sh
# pre-commit — l'état accompagne le fait, le journal accompagne le code.
#
# Versionné dans tools/hooks/ et installé par tools/installe_hooks.sh : un hook qui
# ne vit que dans .git/hooks ne survit ni au clone ni au nettoyage.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 0

# 1. Aucun fait (reports/, roadmap, backlog) ne se commite sans sa ligne d'état.
#    C'est la garantie de fraîcheur de docs/pilotage/en-cours.md : elle ne dépend
#    pas de la survie d'une session « principale », elle est vérifiée au commit.
if ! python3 tools/verifie_etat_a_jour.py --index; then
    echo "  ⛔ commit refusé : un fait sans ligne d'état."
    echo "     mets docs/pilotage/en-cours.md à jour, puis :"
    echo "     git add docs/pilotage/en-cours.md"
    exit 1
fi

# 2. Archive les traces de session DSH avant chaque commit : le journal doit
#    accompagner le code, pas le suivre.
python3 tools/archive_sessions.py --quiet >/dev/null || { echo "  ⛔ archivage des sessions en échec"; exit 1; }
python3 tools/session_report.py --quiet >/dev/null || { echo "  ⛔ rapport de session en échec"; exit 1; }
# Le journal du jour, par thème (sources : git + journal/session
… [256 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 600000, "wait": true}`

  ```
porte-harnais-invariants ✅                         121 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
  porte-homeostasie      ✅                         579 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
[status: running]
  ```

- **job_output** `{"job_id": "bash-86", "timeout_ms": 600000, "wait": true}`
