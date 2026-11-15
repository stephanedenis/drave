# Session DSH — relecture

- identifiant : `session-01599146-2479-4a06-8381-4ace3d13f579`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 06:34:32
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche E2 : les cas d'erreur de `--tagger` — la clé absente (code 4), la clé invalide (code 4, message clair), le réseau coupé (code 4 ou repli heuristique ?), le refus du modèle ; documente le comportement **réel** de chacun dans `docs/produit/README.md` § 3.7 et une fiche `reports/rapport-tagger-erreurs.md` + JSON, avec un test pour chacun dans `tools/tests/test_tagger_api.py` (transport factice). Commit.

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

- **bash** `{"command": "pwd && git status --short && git log --oneline -5", "description": "Check repo state and recent commits"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
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
7d4e3bc5 E1 — LA FAQ AU SOMMAIRE ET SES LIENS : 9/9 ANCRES, 5/5 LIENS, 0 MORT ; LA LIGNE FAQ DANS docs/README, LES RÉPONSES INCHANGÉES
503da67e BILAN DE LA SEMAINE — LE PRODUIT (F1 0,7902, 238/239, TAGGER 95,75), PANINI BORNÉ (DEUX NÉGATIFS), LA COORDINATION, LE HARNAIS (38 LANCEMENTS) ; LES 5 DÉCISIONS EXÉCUTÉES
4d6cffc4 PHASE 4 — D1-D3 (LES EXEMPLES DU TAGGER, LA RESTITUTION v2, LA FAQ 10/10) ; L'INDEX, LA FICHE C3 ORPHELINE (GOLD RÉEL 50) ET LE PLAN COMMITTÉS
5b2d07fc D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270)
e42bac4f JOURNAL — 2026-11-15 : D1, LES EXEMPLES --tagger (441 TOKENS, 3,7 S) ET --reel (452 PHRASES) SONT DANS LA DOC ; 5/5 REJ
… [18 caractères tronqués]
  ```

- **glob** `{"pattern": "**/*tagger*"}`

  ```
tools/tests/linguistique/qualifier_tagger_612.py
tools/tests/linguistique/__pycache__/qualifier_tagger_612.cpython-313.pyc
reports/tagger-612.json
tools/tests/test_tagger_api.py
reports/rapport-tagger-option.md
reports/pensee-tagger-option.json
reports/rapport-exemples-tagger.json
reports/rapport-exemples-tagger.md
  ```

- **glob** `{"pattern": "tools/tests/test_tagger_api.py"}`

  ```
tools/tests/test_tagger_api.py
  ```

- **read** `{"file_path": "tools/tests/test_tagger_api.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py</path>
<type>file</type>
<content>
1: """test_tagger_api.py — le tagger POS par API, **en option**, sans réseau.
2: 
3: Ce que le fichier verrouille, avec un **transport factice** (une fonction qui rend un JSON de
4: POS valide) :
5: 
6: 1. la cascade remplace bien les POS par ceux du tagger (et garde les syntagmes de l'heuristique,
7:    avec leurs rôles et leurs cibles) ;
8: 2. le JSON reste valide : le schéma **déclaré** (v2) le lit, et le contrat **v1** reste lisible ;
9: 3. deux analyses du même texte ne refont pas d'appel (cache mémoire des taggers) ;
10: 4. le défaut est inchangé : `analyser --json` sans `--tagger` rend exactement l'heuristique ;
11: 5. sans clé, `--tagger` sort **4** avec un message clair, et jamais la clé ;
12: 6. l'ordre de résolution de la clé : `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`,
13:    puis `DEEPSEEK_API_KEY`.
14: 
15: Aucun test n'ouvre de socket : les transports sont injectés, et le test « sans clé » lance la
16: commande dans un `HOME` vide. Le fichier passe par `python3 tools/tests/test_tagger_api.py`
17: comme par `pytest`.
18: """
19: from _
… [15337 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"tagger\" --include=*.py tools/ | head -50", "description": "Find tagger implementation references"}`

  ```
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/ncl.py:329:                'wrf_user_ll_to_ij', 'wrf_user_unstagger', 'wrf_user_vert_interp',
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:164:    'stagger',
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1892:def stagger(iterable, offsets=(-1, 0, 1), longest=False, fillvalue=None):
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1897:        >>> list(stagger([0, 1, 2, 3]))
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1899:        >>> list(stagger(range(8), offsets=(0, 2, 4)))
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1906:        >>> list(stagger([0, 1, 2, 3], longest=True))
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1944:    staggered = []
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1947:            staggered.append(chain(repeat(fillvalue, -n), it))
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1949:            staggered.append(islice(it, n, None))
tools/docwatch/.venv/lib/python3.13/site-packag
… [5269 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"tagger\\|_cle_tagger\\|_client_tagger\\|_cascade_tagger\\|code 4\\|return 4\" tools/drave.py | head -80", "description": "Find tagger code in drave.py"}`

  ```
8:    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
11:    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
23:En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
26:**Sans `--tagger`, le défaut ne change pas** : heuristique, CPU, hors ligne, déterministe.
30:Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger absent · 1 erreur.
60:# Le tagger est une **option** : sans `--tagger`, rien de ce bloc n'est importé ni exécuté.
63:# La fusion de l'option : le POS vient du tagger, tout le reste de l'heuristique. On ne force
88:# --------------------------------------------------------------------------- le tagger (option)
92:    """Aucune clé : le tagger est une option, jamais un prérequis du produit."""
102:def _cle_tagger() -> str:
120:        "Sans --tagger, le défaut reste l'heuristique hors ligne."
124:def _client_tagger():
127:    return DeepSeek(cle=_cle_tagger())
130:def _transport_tagger(client, stats: dict):
131:    """Le transport attendu par les taggers : invite → contenu, avec le coût mesuré."""
153:    """La cascade du tag
… [4354 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class .*Tagger\\|NeuronalLLMPOS\\|def _transport\\|transport\\|refus\\|disponible\\|class Client\\|APIError\\|Erreur\" tools/bloc_linguistique.py | head -80", "description": "Find tagger classes in bloc_linguistique"}`

  ```
12:  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
103:    refus: str = ""
130:            "source": self.source, "refus": self.refus,
146:    """Le modèle n'a pas rendu une annotation exploitable — le contrat refuse, il n'invente pas."""
1459:            # une entrée non textuelle est **refusée** proprement (le produit ne plante pas)
1460:            return Annotation(texte=str(texte)[:200], refus="non_texte", source=self.nom,
1461:                              trace=[{"etape": "refus", "raison": "non_texte",
1467:            return Annotation(texte=texte, refus="vide", source=self.nom,
1468:                              trace=[{"etape": "refus", "raison": "vide"}],
1968:class NeuronalLLMPOS:
1978:    180 chargements. `transport` est injectable pour tester le contrat sans modèle.
1989:                 transport=None, cache: bool = True):
1995:        self.transport = transport or self._post
2032:            return Annotation(texte=texte, langue=lg, script=script, refus="vide", source=self.nom)
2038:            return Annotation(texte=texte, langue=lg, script=script, refus="vide", source=self.nom)
2045:            sortie = self.transpo
… [1822 caractères tronqués]
  ```

- **read** `{"file_path": "tools/drave.py", "offset": 1, "limit": 240}`
- **read** `{"file_path": "tools/drave.py", "offset": 330, "limit": 120}`

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
8:     python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
9:     python3 tools/drave.py evaluer
10:     python3 tools/drave.py evaluer --gold --json
11:     python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
12:     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
13:     python3 tools/drave.py restituer "Le chat dort."
14:     python3 tools/drave.py restituer "Le chat dort." --roles
15:     python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
16:     python3 tools/drave.py --version
17: 
18: Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
19: avec rôle et cible d'attacheme
… [10853 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
330:         return pathlib.Path(args.fichier).read_text(encoding="utf-8", errors="replace")
331:     return args.texte or ""
332: 
333: 
334: def _analyser_jsonl(texte: str, args: argparse.Namespace, h: bl.Heuristique, bloc,
335:                     stats: dict | None = None) -> int:
336:     """Une **ligne JSON par phrase** (traitement de corpus : `--jsonl`).
337: 
338:     `h` segmente (le tagger ne change pas les frontières de phrase) ; `bloc` analyse — la
339:     cascade du tagger quand `--tagger` est posé. Le coût va sur `stderr`, jamais dans le JSONL.
340:     """
341:     n = 0
342:     refus = 0
343:     for debut, fin, _typ, _ in h._phrases(texte):
344:         phrase = texte[debut:fin]
345:         if not phrase.strip():
346:             continue
347:         a = bloc.analyser(phrase, args.langue, args.contexte)
348:         refus += int(bool(a.refus))
349:         sys.stdout.write(_sur(json.dumps(a.json(), ensure_ascii=False)) + "\n")
350:         n += 1
351:     if n == 0:
352:         print(f"{NOM}: refus d'analyse : vide", file=sys.stderr)
353:         return 3
35
… [4521 caractères tronqués]
  ```

- **read** `{"file_path": "tools/llm/deepseek.py"}`

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

- **bash** `{"command": "grep -n \"3.7\\|3\\.7\\|tagger\" docs/produit/README.md | head -40", "description": "Find tagger section in product README"}`

  ```
11:> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
12:> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le format
47:aucun accès réseau **par défaut** (le tagger en option, lui, appelle l'API DeepSeek, § 3.7). Les
64:| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger` |
143:gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement
145:POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
148:  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture
356:contrôle négatif : mélange exacte 0.0000 (caractères 0.3077) · troncature exacte 0.0000
386:### 3.7 Le tagger en option — `--tagger`
389:python3 tools/drave.py analyser "Le chat dort." --tagger
390:python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
391:python3 tools/drave.py evaluer --tagger
394:drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
416:**Ce que l'option change — et ce qu'elle ne change pas.** Le **POS** vient du tagger
418:**cib
… [2611 caractères tronqués]
  ```

- **read** `{"file_path": "docs/produit/README.md", "offset": 380, "limit": 110}`
- **read** `{"file_path": "docs/produit/README.md", "offset": 540, "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
380: ```
381: 
382: `--reel` mesure les **452 phrases réelles** (main + corpus), sans les 160 synthétiques : POS
383: **88,91 %**, F1 **79,06 %**, attachement **99,46 %**. Sans lui, `evaluer` publie la ligne
384: `BASE RÉELLE` à côté du global (612 phrases) — le chiffre global seul peut tromper.
385: 
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
402: COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=
… [6319 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
540: textes longs et répétés ne s'effondrent plus.
541: 
542: **Ce que le produit ne consomme pas** : pas de GPU, pas de modèle, pas de réseau, pas d'écriture
543: disque (hors le fichier de sortie). Le cache est **local à une analyse** et libéré à chaque
544: phrase. Les temps sont CPU, sur machine partagée ; ils varient avec la charge.
545: 
546: ## 6. Garanties
547: 
548: | garantie | ce que ça veut dire | contrôle |
549: |---|---|---|
550: | **déterminisme** | même entrée → même JSON, octet pour octet | `drave rejouer` (§ 3.4) ; `tools/tests/test_produit.py` compare deux sorties |
551: | **hors réseau** | le chemin par défaut n'ouvre aucune socket | analyse `heuristique` seulement ; le tagger API exige `--tagger` et une clé |
552: | **refus explicite** | texte vide ou sans lettre/chiffre → `refus: "vide"`, 0 étiquette | bloc : JSON ; CLI : JSON sur `stdout` + code 3 |
553: | **pas d'invention** | chaque étiquette porte `source`, `confiance`, `candidats` ; `und` plutôt qu'une langue forcée | JSON ; `--langue` est un indice |
554: | **spans lisibles** | indices en **poi
… [3709 caractères tronqués]
  ```

- **read** `{"file_path": "tools/bloc_linguistique.py", "limit": 130, "offset": 1960}`
- **read** `{"file_path": "tools/bloc_linguistique.py", "limit": 70, "offset": 2230}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1960: def grammaire_pos(n: int) -> str:
1961:     """La grammaire GBNF : exactement `n` classes, dans l'ordre — le JSON ne peut pas dériver."""
1962:     corps = " tag" + ' ("," tag)' * (n - 1) if n > 1 else " tag"
1963:     texte = 'root ::= "{\\"pos\\":["' + corps + ' "]}"\n'
1964:     texte += "tag ::= " + " | ".join('"\\"%s\\""' % c for c in CLASSES_POS) + "\n"
1965:     return texte
1966: 
1967: 
1968: class NeuronalLLMPOS:
1969:     """Le **tagger** neuronal réel : un modèle local, des POS alignés sur la tokenisation du bloc.
1970: 
1971:     Le modèle ne rend pas une annotation complète : il rend **une classe par token**, contrainte
1972:     par une grammaire GBNF (`grammaire_pos`) qui interdit un JSON tronqué, un token manquant ou
1973:     une classe hors du jeu. Les spans sont ceux de `Heuristique._mots` (la tokenisation du bloc),
1974:     pas ceux que le modèle inventerait ; c'est ce qui rend la mesure POS exacte.
1975: 
1976:     Le modèle est servi par `llama-server` (`/v1/chat/completions`, `grammar`) : le serveur est
1977:     lancé une fois, le modèl
… [6709 caractères tronqués]
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
… [2909 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"E2\\|tagger-erreurs\\|cas d'erreur\\|clé invalide\" docs/pilotage tools/chantier reports journal 2>/dev/null | head -40", "description": "Search for E2 task references"}`

  ```
docs/pilotage/programme-r.md:257:qui la porte. C'est le lien avec E2 (encodeur de formes) et E3 (politique de saccades), et avec
docs/pilotage/programme-r.md:283:  manquante — une **forme** et un `z` qui la porte. C'est E2, et peut-être la couche
tools/chantier/plan.json:561:   "id": "E2",
tools/chantier/plan.json:563:   "titre": "Le tagger — les cas d'erreur",
tools/chantier/plan.json:564:   "mandat": "Tâche E2 : les cas d'erreur de `--tagger` — la clé absente (code 4), la clé invalide (code 4, message clair), le réseau coupé (code 4 ou repli heuristique ?), le refus du modèle ; documente le comportement **réel** de chacun dans `docs/produit/README.md` § 3.7 et une fiche `reports/rapport-tagger-erreurs.md` + JSON, avec un test pour chacun dans `tools/tests/test_tagger_api.py` (transport factice). Commit.",
tools/chantier/plan.json:568:     "commande": "test -f reports/rapport-tagger-erreurs.md && echo FICHE-OK",
reports/rapport-passage-a-l-echelle.md:78:  (une **puissance de deux**) + 16 octets de valeurs E2M1. Les 8 magnitudes
reports/rapport-passage-a-l-echelle.md:90:E8M0 + 16 octets de nibbles E2M1). Les huit magnitudes du format sont
reports/rapport-passage-a-l-echelle.md:109:
… [4710 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/chantier/plan.json", "description": "Read chantier plan"}`

  ```
{
 "nom": "Semaine 07/11 → 14/11 — le produit et l'intégration Panini",
 "principe": "Une tâche n'est finie que si son acceptation passe ; l'agent commite, le superviseur vérifie.",
 "taches": [
  {
   "id": "J0",
   "jour": 0,
   "titre": "Le contrôle du superviseur",
   "mandat": "Réponds exactement le mot OK, sans autre texte. C'est un test de liaison du superviseur.",
   "budget_min": 2,
   "acceptation": [
    {
     "commande": "python3 -c \"print('LIAISON-OK')\"",
     "attendu": "LIAISON-OK"
    }
   ]
  },
  {
   "id": "J1.1",
   "jour": 1,
   "titre": "r035 : la relative zéro",
   "mandat": "Tâche J1.1 du chantier : la relative zéro (r035, « The film she talks about is out. »). Reproduis, explique, propose UNE règle générale mesurée sur dev/test ; si elle tient (attachement 236→237, POS/F1 stables), intègre-la et commite avec une fiche `reports/rapport-r035.md` + `reports/pensee-r035.json`. Sinon, écris la fiche du rejet (chiffres, raison) et commite-la. Règles : ne touche pas S/D/N2 ; 183/183 portes ; en-cours à jour.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-r035.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
   
… [4040 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '550,585p' tools/chantier/plan.json", "description": "Read E2 plan entry"}`

  ```
{
     "commande": "test -f reports/rapport-faq-sommaire.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
    {
     "commande": "python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?",
     "attendu": "REVUE-0"
    }
   ]
  },
  {
   "id": "E2",
   "jour": 15,
   "titre": "Le tagger — les cas d'erreur",
   "mandat": "Tâche E2 : les cas d'erreur de `--tagger` — la clé absente (code 4), la clé invalide (code 4, message clair), le réseau coupé (code 4 ou repli heuristique ?), le refus du modèle ; documente le comportement **réel** de chacun dans `docs/produit/README.md` § 3.7 et une fiche `reports/rapport-tagger-erreurs.md` + JSON, avec un test pour chacun dans `tools/tests/test_tagger_api.py` (transport factice). Commit.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-tagger-erreurs.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
    {
     "commande": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -1",
     "attendu": "OK"
    }
   ]
  }
 ]
}
  ```

- **bash** `{"command": "ls reports/ | grep -i tagger; echo ---; sed -n '1,80p' reports/rapport-tagger-option.md", "description": "Inspect existing tagger reports"}`

  ```
pensee-tagger-option.json
rapport-exemples-tagger.json
rapport-exemples-tagger.md
rapport-tagger-option.md
tagger-612.json
---
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

**La mesure sur le gold 612** (avec la clé, cache partiel) : POS **0,9575** cont
… [3515 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"ErreurDeepSeek\\|HTTP 401\\|401\\|clé invalide\\|réseau coupé\\|repli\" tools/*.py tools/llm/*.py docs/produit/README.md | head -60", "description": "Search for error handling patterns"}`

  ```
tools/bloc_linguistique.py:1070:    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict]) -> str | None:
tools/bloc_linguistique.py:1085:    def _repli_verbe_propre(texte: str, segment: dict, cible: str | None):
tools/bloc_linguistique.py:1697:                        cible = (self._repli_cible_gp(texte, s, gns_s)
tools/bloc_linguistique.py:1700:                    cible = self._repli_verbe_propre(texte, s, cible)
tools/bloc_linguistique.py:1726:                         or self._repli_cible_gp(texte, s, [x for x in simples if x["type"] == "GN"])
tools/bloc_linguistique.py:1729:                cible = self._repli_verbe_propre(texte, s, cible)
tools/bloc_linguistique.py:1756:                         or self._repli_cible_gp(texte, s, [x for x in simples if x["type"] == "GN"])
tools/bloc_linguistique.py:1759:                cible = self._repli_verbe_propre(texte, s, cible)
tools/bloc_linguistique.py:2602:        # Choix **strict** par niveau : la source désignée, sans repli. Le repli (prendre
tools/bloc_maths.py:135:    """Somme ; les deux constantes se replient — l'AST est canonique."""
tools/couche_distante.py:1391:        print("[A18] CUDA indisponible : repli sur CPU", fil
… [4381 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline --all -- tools/drave.py | head -30; echo ---; git log -S \"CleTaggerAbsente\" --oneline --all | head", "description": "Check git history for tagger error handling"}`

  ```
5b2d07fc D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270)
2d7a7f2b 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5)
ce7241d5 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS
0bbdbbb3 1A — LE TAGGER POS EN OPTION (--tagger) : +8,49 PTS SUR LE GOLD 612 (+4,67 SUR LE RÉEL 432), LE DÉFAUT RESTE HORS LIGNE ; 14 TESTS, DOC § 3.7
09e54143 J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ
229098ec J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
8eb0cc49 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE
5b9c18ef PRODUIT — --fichier ET --jsonl (TRAITEMENT DE CORPUS, UNE LIGNE JSON PAR PHRASE) ; 16 TESTS
662a3698 PRODUIT — evaluer PUBLIE LES DEUX VUES (FIDÈLE F1 75,33 / LINÉAIRE 81,04, COUVERTURE 93,31) ; 14 TESTS
027abba4 PRODUIT — --contexte 
… [931 caractères tronqués]
  ```

- **read** `{"file_path": "tools/llm/enseignant.py", "limit": 120, "offset": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/llm/enseignant.py</path>
<type>file</type>
<content>
50:             d = json.loads(ligne)
51:         except json.JSONDecodeError:
52:             continue
53:         if bool(d.get("dry_run")) == dry_run:
54:             faits.add(d.get("id", ""))
55:     return faits
56: 
57: 
58: def generer(prompts: list[dict], sortie: str | pathlib.Path, client: DeepSeek,
59:             *, dry_run: bool = False, limite: int | None = None,
60:             reprise: bool = True, temperature: float = 0.0,
61:             max_tokens: int = 1024, cache: bool = True,
62:             ecraser: bool = False) -> dict:
63:     chemin = pathlib.Path(sortie)
64:     chemin.parent.mkdir(parents=True, exist_ok=True)
65:     if ecraser and chemin.is_file():
66:         chemin.unlink()
67:     faits = _deja_faits(chemin, dry_run) if reprise and not ecraser else set()
68:     a_faire = [p for p in prompts if p["id"] not in faits]
69:     if limite is not None:
70:         a_faire = a_faire[:limite]
71:     stats = {"demandes": 0, "reussies": 0, "echecs": 0,
72:              "tokens_entree": 0, "tokens_sortie": 0,
73:              "latence_s": 0.0, "ca
… [3070 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"refus partiel\\|tagger :\\|code 4\\|Clé\\|clé\" docs/produit/README.md | sed -n '1,60p'", "description": "Find all tagger error docs in README"}`

  ```
12:> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le format
163:bloc `PAR LANGUE` (et une clé `par_langue` au JSON) : phrases, tokens, cibles, POS, syntagmes,
215:`meta.alternative` ; les autres n'en portent pas, et `meta` reste **ouvert** pour les clés
319:**Lecture.** La commande analyse **deux fois**, compare le JSON **canonique** (clés triées,
411:**La clé.** Lue dans `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`, puis
413:ni dans le message, ni dans le JSON, ni dans le cache. **Sans clé**, la commande écrit un
447:**Le défaut ne bouge pas.** Sans `--tagger`, la commande ne lit aucune clé, n'importe pas le
551:| **hors réseau** | le chemin par défaut n'ouvre aucune socket | analyse `heuristique` seulement ; le tagger API exige `--tagger` et une clé |
574:| **4** | dépendance absente : la clé du tagger | `--tagger` sans clé (message clair, rien sur `stdout`) |
600:`--tagger` est la **seule** option qui sort du hors ligne : elle appelle l'API DeepSeek (clé et
633:| `--tagger` | `analyser`, `evaluer` | POS par l'API DeepSeek (clé et réseau ; défaut : heuristique) ; `evaluer` mesure en plus la cascade et le Δ (§ 3.7) |
666:`--fichier
… [359 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport contextlib, io, json, sys\nsys.path.insert(0, '.'); sys.path.insert(0, 'tools')\nimport drave\nfrom tools.llm.deepseek import DeepSeek, ErreurDeepSeek\n\ndef run(label, client):\n    old = drave._client_tagge … [1361 caractères tronqués]`

  ```
### cle invalide code= 0
STDERR: drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: HTTP 401 : {"error": "invalid key"}
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s

STDOUT: {
 "schema": "drave.annotation",
 "version": 2,
 "texte": "Le chat dort.",
 "langue": "fr",
 "script": "Latn",
 "source": "cascade",
 "refus": "neuronal-pos: ErreurDeepSeek: HTTP 401 : {\"error\": \"invalid key\"}",
 "etiquettes": [
  {
   "niveau": "graphème",
   "type": "lettres",
   "valeur": "Le",
   "debut": 0,
   "fin": 2,
   "source": "heuristique",
   "confiance": 0.99,
   "candidats": [],
   "langue": "fr",
   "script": "Latn",
   "meta": {}
  },
  {
   "niveau": "mot",
   "type": "mot",
   "valeur": "Le",
   "debut": 0,
   "fin": 2,
   "source": "heuristique",
   "confiance": 0.98,
   "candidats": [],
   "langue": "fr",
   "script": "Latn",
   "meta": {}
  },
  {
   "niveau": "pos",
   "type": "DET",
   "valeur": "Le",
   "debut": 0,
   "fin": 2,
   "source": "heuristique",
   "c

### reseau code= 0
STDERR: drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau : [Errno -2] Name or service not known
drave: TAGGER API · mod
… [2780 caractères tronqués]
  ```

- **read** `{"file_path": "tools/drave.py", "limit": 150, "offset": 510}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
510:             pr = m["pragmatique"]
511:             lignes += [
512:                 f"  {langue}  {m['phrases']} phrases · {p['tokens']} tokens · "
513:                 f"{a['cibles']} cibles d'attachement",
514:                 f"      POS {_pct(p['exactitude'])} (fermé {_pct(p['exactitude_ferme'])}, "
515:                 f"ouvert {_pct(p['exactitude_ouvert'])}) · SYNTAGMES F1 {_pct(s['f1'])} "
516:                 f"(tête {_pct(s['tete']['f1'])})",
517:                 f"      ATTACHEMENT exact {_pct(a['exact_taux'])} · "
518:                 f"couverture {_pct(a['couverture'])} · top-k {_pct(a['topk_taux'])} · "
519:                 f"PRAGMATIQUE acte {_pct(pr['acte'])}",
520:                 f"      CONTRÔLE NÉGATIF cible exacte tirée au hasard {_pct(c['exact_taux'])} "
521:                 f"(graine {c['graine']}, {c['cibles']} cibles)",
522:             ]
523:             t = m.get("tagger")
524:             if t:
525:                 lignes.append(
526:                     f"      TAGGER POS {_pct(t['pos']['exactitude'])} "
527:                     f"· Δ {_points(t['
… [7466 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"NeuronalLLMPOS\\|neuronal-pos\" tools/tests --include=*.py | head -40", "description": "Find tests for NeuronalLLMPOS"}`

  ```
tools/tests/linguistique/qualifier_neuronal.py:4:Le tagger est `bloc_linguistique.NeuronalLLMPOS` : un modèle GGUF servi par `llama-server`, une
tools/tests/linguistique/qualifier_neuronal.py:205:    tagger = bl.NeuronalLLMPOS(modele, endpoint=endpoint, confiance=args.confiance)
tools/tests/linguistique/qualifier_neuronal.py:267:            "tagger": {"classe": "NeuronalLLMPOS", "confiance": args.confiance,
tools/tests/linguistique/qualifier_cascade.py:4:Le bloc neuronal est `NeuronalLLMCompose` : `NeuronalLLMPOS` + `NeuronalLLMChunks`, appelés
tools/tests/linguistique/qualifier_cascade.py:95:    pos = bl.NeuronalLLMPOS(modele, endpoint=endpoint, confiance=args.confiance)
tools/tests/linguistique/qualifier_cascade.py:144:                     "pos": "NeuronalLLMPOS", "syntagmes": "NeuronalLLMChunks",
tools/tests/linguistique/qualifier_quatre_modes.py:33:                                     NeuronalLLMPOS, NeuronalLLMPragmatique, Parallele)
tools/tests/linguistique/qualifier_quatre_modes.py:64:    pos = NeuronalLLMPOS("deepseek-chat", transport=transport)
tools/tests/linguistique/qualifier_tagger_612.py:39:                                     NeuronalLLMPOS, Parallele)
tools/tests/li
… [577 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"test_tagger_api\\|tagger\" tools/toutes-les-portes.sh tools/porte-produit.sh tools/porte-*.sh 2>/dev/null | head -30", "description": "Find gates running tagger tests"}`

  ```
(no output)
  ```

- **read** `{"file_path": "tools/tests/linguistique/test_bloc_linguistique.py", "limit": 60, "offset": 185}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py</path>
<type>file</type>
<content>
185:             encoding="utf-8")
186:         faux.chmod(faux.stat().st_mode | stat.S_IEXEC)
187:         modele = pathlib.Path(__file__).resolve()
188:         n = bl.NeuronalLLM(modele, llama_cli=str(faux), timeout=10)
189:         a = n.analyser("Le chat dort.", "fr")
190:         self.assertEqual(a.source, "neuronal")
191:         self.assertEqual(a.langue, "fra")
192:         self.assertEqual({e.niveau for e in a.etiquettes}, {"phrase", "pragmatique"})
193: 
194:     def test_tagger_neuronal_pos_avec_faux_transport(self):
195:         appels = []
196: 
197:         def transport(invite, grammaire, max_jetons):
198:             appels.append((invite, grammaire, max_jetons))
199:             return '{"pos":["DET","NOUN","VERB"]}'
200: 
201:         n = bl.NeuronalLLMPOS("faux-modele", transport=transport)
202:         a = n.analyser("Le chat dort.", "fr")
203:         self.assertEqual(a.source, "neuronal")
204:         self.assertEqual([(e.debut, e.fin, e.type) for e in a.etiquettes],
205:                          [(0, 2, "DET"), (3, 7, "N
… [2060 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"test_tagger_api\" tools/ --include=*.sh --include=*.py | head", "description": "Find where tagger tests are invoked"}`

  ```
tools/tests/test_tagger_api.py:1:"""test_tagger_api.py — le tagger POS par API, **en option**, sans réseau.
tools/tests/test_tagger_api.py:16:commande dans un `HOME` vide. Le fichier passe par `python3 tools/tests/test_tagger_api.py`
  ```

- **bash** `{"command": "ls tools/porte-*.sh; echo ---; grep -n \"unittest\\|test_\\|pytest\" tools/porte-produit.sh tools/toutes-les-portes.sh | head -40", "description": "Inspect gate scripts"}`

  ```
tools/porte-adaptateur-sortie.sh
tools/porte-audit-drapeaux.sh
tools/porte-b1110-hybride.sh
tools/porte-balayage.sh
tools/porte-bloc-code.sh
tools/porte-bloc-linguistique.sh
tools/porte-bloc-maths.sh
tools/porte-bloc-tableaux.sh
tools/porte-budget.sh
tools/porte-bus.sh
tools/porte-bus-socket.sh
tools/porte-c4-retard.sh
tools/porte-cerveau.sh
tools/porte-cic.sh
tools/porte-consolidation.sh
tools/porte-coupe.sh
tools/porte-cycle-c2.sh
tools/porte-deepseek.sh
tools/porte-delais.sh
tools/porte-diff-couche.sh
tools/porte-document.sh
tools/porte-echange-experts.sh
tools/porte-episodique.sh
tools/porte-etat.sh
tools/porte-flux.sh
tools/porte-fusion.sh
tools/porte-gain.sh
tools/porte-greffe.sh
tools/porte-harnais-invariants.sh
tools/porte-homeostasie.sh
tools/porte-horloge.sh
tools/porte-indice.sh
tools/porte-jeux.sh
tools/porte-jumeaux.sh
tools/porte-lecteur.sh
tools/porte-lecture.sh
tools/porte-m5-brouillon.sh
tools/porte-melange.sh
tools/porte-memoire.sh
tools/porte-miroir-blocs.sh
tools/porte-mistral.sh
tools/porte-n3-cache.sh
tools/porte-n3-composition.sh
tools/porte-n3-deux-processus.sh
tools/porte-n3-deux-regions.sh
tools/porte-n3-generation.sh
tools/porte-n3-inventaire.sh
tools/por
… [1570 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Cascade\" tools/bloc_linguistique.py", "description": "Find Cascade class"}`

  ```
2664:class Cascade:
  ```

- **read** `{"file_path": "tools/bloc_linguistique.py", "limit": 90, "offset": 2664}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
2664: class Cascade:
2665:     """L'heuristique d'abord ; le neuronal seulement si un niveau reste sous le seuil."""
2666: 
2667:     nom = "cascade"
2668: 
2669:     def __init__(self, heuristique: BlocLinguistique, neuronal: BlocLinguistique,
2670:                  seuil: float = 0.6, niveaux=("morphème", "pos", "syntagme", "discours", "pragmatique"),
2671:                  priorite_syntagme: str = "heuristique",
2672:                  priorite_par_niveau: dict | None = None,
2673:                  priorite_par_type: dict | None = None):
2674:         self.h = heuristique
2675:         self.n = neuronal
2676:         self.seuil = seuil
2677:         self.niveaux = niveaux
2678:         self.priorite_syntagme = priorite_syntagme
2679:         self.priorite_par_niveau = (priorite_par_niveau if priorite_par_niveau is not None
2680:                                      else priorite_par_defaut())
2681:         self.priorite_par_type = dict(priorite_par_type or {})
2682:         self.appels_neuronal = 0
2683: 
2684:     def analyser(self, texte: str, langue: str | None =
… [3620 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"deepseek\" tools/tests/test_produit.py tools/tests/test_produit_libre.py tools/porte-produit.sh | head -30", "description": "Check no-network default test"}`

  ```
(no output)
  ```

- **bash** `{"command": "grep -rn \"n'est même pas importé\\|pas importé\\|deepseek\" tools/tests --include=*.py | head -20; sed -n '680,720p' docs/produit/README.md", "description": "Find network import guarantees"}`

  ```
tools/tests/linguistique/qualifier_quatre_modes.py:16:    DEEPSEEK_KEY_FILE=~/.config/drave/deepseek.key \
tools/tests/linguistique/qualifier_quatre_modes.py:34:from tools.llm.deepseek import DeepSeek
tools/tests/linguistique/qualifier_quatre_modes.py:64:    pos = NeuronalLLMPOS("deepseek-chat", transport=transport)
tools/tests/linguistique/qualifier_quatre_modes.py:65:    chunks = NeuronalLLMChunks("deepseek-chat", transport=transport)
tools/tests/linguistique/qualifier_quatre_modes.py:66:    pragma = NeuronalLLMPragmatique("deepseek-chat", transport=transport)
tools/tests/linguistique/qualifier_quatre_modes.py:109:                 "modalite": "api-deepseek (deepseek-chat), aucun serveur local"},
tools/tests/linguistique/qualifier_tagger_612.py:13:    DEEPSEEK_KEY_FILE=$HOME/.config/drave/deepseek.key \
tools/tests/linguistique/qualifier_tagger_612.py:15:    DEEPSEEK_MODEL=deepseek-chat \
tools/tests/linguistique/qualifier_tagger_612.py:19:La clé n'est jamais lue en dur : `tools/llm/deepseek.py` lit `DEEPSEEK_API_KEY` ou le fichier
tools/tests/linguistique/qualifier_tagger_612.py:40:from tools.llm.deepseek import DeepSeek
tools/tests/linguistique/qualifier_tagger_612.py:104:    po
… [3284 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"comportement\\|code 4\\|réel de\\|attendu\\|vérifie\" tools/chantier/plan.json | head -40", "description": "Look at task mandate style"}`

  ```
3: "principe": "Une tâche n'est finie que si son acceptation passe ; l'agent commite, le superviseur vérifie.",
14:     "attendu": "LIAISON-OK"
27:     "attendu": "FICHE-OK"
31:     "attendu": "REVUE-0"
44:     "attendu": "FICHE-OK"
48:     "attendu": "verte"
61:     "attendu": "V2-OK"
65:     "attendu": "VALIDE-0"
78:     "attendu": "REST-0"
82:     "attendu": "FICHE-OK"
95:     "attendu": "FICHE-OK"
99:     "attendu": ""
112:     "attendu": "FICHE-OK"
125:     "attendu": "FICHE-OK"
138:     "attendu": "FICHE-OK"
151:     "attendu": "FICHE-OK"
164:     "attendu": "FICHE-OK"
177:     "attendu": "FICHE-OK"
190:     "attendu": "FICHE-OK"
203:     "attendu": "FICHE-OK"
216:     "attendu": "semaine-2026-11-14"
220:     "attendu": "REVUE-0"
228:   "mandat": "Tâche J6.1 : le dernier span du gold, `g017` (« She said that she would come yesterday. ») — le gold attend la SUB « that she would come » (sans « yesterday »), le bloc l'inclut. Reproduis, propose UNE règle mesurée (l'adverbe final de temps hors de la SUB), vérifie dev/test et l'attachement, fiche `reports/rapport-g017.md` + JSON, commit. Si la règle casse autre chose, écris la fiche du rejet.",
233:     "attendu": "FICHE-OK"
237: 
… [497 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport contextlib, io, json, sys\nsys.path.insert(0, '.'); sys.path.insert(0, 'tools')\nimport drave\nfrom tools.llm.deepseek import DeepSeek, ErreurDeepSeek\n\nclass Refus:\n    def demande(self, prompt, **kw):\n   … [872 caractères tronqués]`

  ```
code 0
ERR drave: TAGGER API · modèle=deepseek-chat · appels=2 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s

tagger {'refus': 2, 'refus_detail': ['g001', 'g002'], 'delta_pos': 0.0}
cout {'modele': 'deepseek-chat', 'appels': 2, 'requetes': 0, 'cache': 0, 'tokens': 0, 'latence_s': 0.0, 'modeles_renvoyes': {}}
  ```

- **read** `{"file_path": "docs/methode/resultats.md"}`

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

- **bash** `{"command": "sed -n '1,100p' reports/rapport-exemples-tagger.md; echo =====; cat reports/rapport-exemples-tagger.json | head -50", "description": "Inspect recent report style"}`

  ```
# D1 — les exemples `--tagger` et `--reel` : le coût affiché, la base honnête, cinq blocs rejoués

> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **D1** · **Date** : 2026-11-15 ·
> **Verdict** : ✅
> **Cinq blocs ajoutés** à [`docs/produit/exemples.md`](../docs/produit/exemples.md) : **3** avec
> `--tagger` (la clé, le réseau, le **coût affiché**) et **2** avec `--reel` (la **base
> honnête**). Les trois exemples `--tagger` réparent **2 tokens sur 17** (14/17 → 16/17) ;
> **3 appels**, **441 tokens**, **3,7 s**. Les deux `--reel` donnent **452 phrases**, POS
> **0,8891**, F1 **0,7906**, attachement **183/184 = 0,9946**. Le code courant n'a pas bougé :
> F1 **0,7902**, attachement **238/238 labels** (**238/239 cibles**, 0,9958), schéma **v2**.
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) 0.1.0, clé
> `~/.config/drave/deepseek.key`, cache disque neuf (`DEEPSEEK_CACHE`), `jq`. **Contrôle
> négatif** : doc mutée (`lu/VERB` → `lu/NOUN`) détectée **4/5**, schéma v2 qui refuse une
> version 3. **JSON** : [`rapport-exemples-tagger.json`](rapport-exemples-tagger.json).

## 1. Ce qui a été ajouté

| bloc | cas | commande | ce que la sortie montre | coût |
|---|---|---
… [7282 caractères tronqués]
  ```

- **read** `{"file_path": "tools/drave.py", "limit": 80, "offset": 770}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
770:     """Un parseur francophone : `-h`, `--help` et `--aide` partout, sans doublon."""
771: 
772:     def __init__(self, *args, **kwargs):
773:         kwargs["add_help"] = False
774:         super().__init__(*args, **kwargs)
775:         self._positionals.title = "arguments"
776:         self._optionals.title = "options"
777:         self.add_argument("-h", "--help", "--aide", action="help",
778:                           help="afficher cette aide et quitter")
779: 
780:     def error(self, message: str) -> None:  # type: ignore[override]
781:         self.print_usage(sys.stderr)
782:         self.exit(2, f"{self.prog}: erreur d'usage : {message}\n")
783: 
784: 
785: def construire_parseur() -> argparse.ArgumentParser:
786:     epilogue = (
787:         "Commandes : analyser, evaluer, rejouer, restituer.\n"
788:         "Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) ·\n"
789:         "4 clé/tagger absent · 1 erreur.\n"
790:         "Options : --json, --langue fr|en, --partition brut|alternative|filtrer_union|filtrer,\n"
791:         "--contexte, --banc, --ta
… [4018 caractères tronqués]
  ```

- **read** `{"file_path": "tools/drave.py", "limit": 60, "offset": 885}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
885:         description="Analyse un texte, reconstruit la surface depuis le niveau `graphème` "
886:                     "(sans lire le champ `texte` de l'annotation) et compare à la source. "
887:                     "Affiche la fidélité binaire du miroir, la fidélité de caractères et un "
888:                     "contrôle négatif. Avec --canonique, produit en plus la forme canonique v1 "
889:                     "(segments + rôles + cibles) et son miroir canonique ; avec --roles, produit "
890:                     "la forme lisible des rôles (agent, prédicat, lieu) et, sur un banc, leur "
891:                     "fidélité à un or écrit à la main.",
892:         epilog="Exemples : python3 tools/drave.py restituer \"Le chat dort.\" ; "
893:                "python3 tools/drave.py restituer \"Le chat dort.\" --canonique ; "
894:                "python3 tools/drave.py restituer \"Le chat dort.\" --roles ; "
895:                "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --roles",
896:         formatter_class=_Formateur,
897:     )
898:     resti
… [2862 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/llm/__init__.py 2>/dev/null; python3 -c \"import sys; sys.path.insert(0,'.'); from tools.llm.deepseek import DeepSeek; print('ok')\"", "description": "Check import path for DeepSeek"}`

  ```
tools/llm/__init__.py
ok
  ```

### 🤖 Assistant

I'll implement the error-handling contract, then add the tests, docs and report. Let me set up a task list first.

- **todo_write** `{"todos": [{"content": "Implement explicit 401/403 key-refusal path in drave.py (code 4, clear message)", "status": "in_progress"}, {"content": "Add tests for missing key, invalid key, network cut, model refusal in test_tagger_api.py", "status": "pending"}, {"content": "Document real behavior in doc … [284 caractères tronqués]`

  ```
Updated todo list: 4 pending, 1 in progress, 0 completed.
  ```

- **edit** `{"file_path": "tools/drave.py", "old_string": "Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger absent · 1 erreur.\n\"\"\"", "new_string": "Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible\n(absente ou refusée) · 1 erreur.\n\"\"\""}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/drave.py", "old_string": "class CleTaggerAbsente(RuntimeError):\n    \"\"\"Aucune clé : le tagger est une option, jamais un prérequis du produit.\"\"\"\n\n\ndef _lire_cle(chemin: pathlib.Path) -> str:", "new_string": "class CleTaggerAbsente(RuntimeError):\n    \"\"\"Aucune clé : … [808 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/drave.py", "new_string": "    def transport(invite: str, _grammaire: str, max_jetons: int) -> str:\n        stats[\"appels\"] += 1\n        try:\n            reponse = client.demande(invite, temperature=0.0,\n                                     max_tokens=max(64, int(max_jetons … [805 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/drave.py", "new_string": "    def __init__(self, cascade, compose, stats: dict | None = None):\n        self.cascade = cascade\n        self.compose = compose\n        self.stats = stats if stats is not None else {}\n        self.h = cascade.h\n        self.n = cascade.n\n\n     … [938 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/drave.py", "new_string": "def _cascade_tagger(transport, partition: str = \"alternative\", stats: dict | None = None):\n    \"\"\"Le câblage mesuré : tagger POS + syntagmes → compose → cascade à 0,6.\n\n    `transport` est injectable : les tests le remplacent par une fonction qu … [2745 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/drave.py", "new_string": "    except KeyboardInterrupt:\n        print(f\"{NOM}: interrompu\", file=sys.stderr)\n        return 1\n    except CleTaggerRefusee as exc:\n        # même dépendance manquante qu'une clé absente : code 4, message clair, rien sur stdout\n        print( … [385 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/drave.py", "new_string": "        \"Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) ·\\n\"\n        \"4 clé/tagger indisponible (absente ou refusée) · 1 erreur.\\n\"", "old_string": "        \"Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) ·\\n\" … [50 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport contextlib, io, json, sys, tempfile, pathlib\nsys.path.insert(0, '.'); sys.path.insert(0, 'tools')\nimport drave\nfrom tools.llm.deepseek import DeepSeek, ErreurDeepSeek\n\ndef run(label, client, command=(\"a … [1925 caractères tronqués]`

  ```
### cle invalide code= 4
STDERR: drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.

STDOUT: 

### cle invalide evaluer code= 4
STDERR: drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.

STDOUT: 

### reseau code= 0
STDERR: drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau : [Errno -2] Name or service not known
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s

STDOUT: {
 "schema": "drave.annotation",
 "version": 2,
 "texte": "Le chat dort.",
 "langue": "fr",
 "script": "Latn",
 "source": "cascade",
 "refus": "neuronal-pos: ErreurDeepSeek: réseau : [Errno -2] Name or service not known",
 "etiquettes": [
  {
   "niveau": "graphème",
   "type": "lettres",
   "valeur...
refus: neuronal-pos: ErreurDeepSeek: réseau : [Errno -2] Name or service not known
pos sources: ['heuristique']

tentatives transport: 3
### modele refuse code= 0
… [623 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_tagger_api.py 2>&1 | tail -25", "description": "Run existing tagger tests"}`

  ```
test_cache_par_texte (__main__.TestCascadeTagger.test_cache_par_texte) ... ok
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
test_analyser_json_sans_tagger (__main__.
… [245 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/tests/test_tagger_api.py", "new_string": "3. deux analyses du même texte ne refont pas d'appel (cache mémoire des taggers) ;\n4. le défaut est inchangé : `analyser --json` sans `--tagger` rend exactement l'heuristique ;\n5. les quatre cas d'erreur, chacun avec un transport facti … [1388 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/tests/test_tagger_api.py", "new_string": "import bloc_linguistique as bl  # noqa: E402\nimport drave  # noqa: E402\nfrom tools.llm.deepseek import DeepSeek, ErreurDeepSeek  # noqa: E402", "old_string": "import bloc_linguistique as bl  # noqa: E402\nimport drave  # noqa: E402"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/tests/test_tagger_api.py", "new_string": "class TestErreursTagger(unittest.TestCase):\n    \"\"\"Les cas d'erreur de l'option, **sans réseau** : un client dont le transport échoue.\n\n    Ce que chaque cas verrouille :\n\n    - **clé invalide** : 401/403 n'est pas un refus de ph … [5765 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_tagger_api.py 2>&1 | tail -30", "description": "Run tagger tests with new error cases"}`

  ```
test_cache_par_texte (__main__.TestCascadeTagger.test_cache_par_texte) ... ok
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
test_analyser_json_sans_tagger (__main__.
… [764 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/porte-tableaux.sh", "description": "Understand table gate"}`

  ```
#!/bin/bash
# porte-tableaux.sh — un tableau Markdown qui ne rend pas est un tableau qui n'existe PAS.
#
# POURQUOI CETTE PORTE EXISTE. Le 13/10, le premier tableau de `docs/etat-cerveau.md` s'affichait
# comme du TEXTE dans docwatch : une seule ligne (`| **C2 (cycle 2 régions)** | … |`) avait
# **4 cellules pour 5 colonnes** — un lien qui avait glissé d'une colonne. Le rendu (mistune,
# puis markdown_it, puis markdown) refuse alors le tableau ENTIER, sans rien dire : les 13 lignes
# disparaissent de la page et personne ne le voit, parce que le texte est toujours là, en gris.
#
# CE QU'ELLE VÉRIFIE (trois conditions, toutes nécessaires au rendu) :
#   1. l'en-tête et le séparateur d'un tableau ont le MÊME nombre de cellules ;
#   2. chaque ligne du corps a ce nombre de cellules ;
#   3. aucun `\|` ne subsiste : mistune ne le déséchappe NI dans un espace de code NI dans la
#      prose (il s'affiche alors littéralement). Pour une barre de valeur absolue dans du code,
#      on écrit `∣` (U+2223), qui rend partout et ne casse pas la lecture.
# Les tableaux DANS une citation (`> | … |`) sont valides et vérifiés aussi.
#
# CE QU'ELLE NE VÉRIFIE PAS : les tableaux « écrasés » sur une se
… [6759 caractères tronqués]
  ```

- **bash** `{"command": "date -u +%F; git log -1 --format='%ad %cd' --date=short; grep -n \"Mis à jour\" docs/pilotage/en-cours.md | head", "description": "Check current and commit dates"}`

  ```
2026-11-15
2026-11-15 2026-11-15
3:**Mis à jour : 2026-11-15, 06 h 30 HNE (E1 : la FAQ au sommaire et ses liens)**
  ```

- **edit** `{"file_path": "docs/produit/README.md", "new_string": "**La clé.** Lue dans `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`, puis\n`DEEPSEEK_API_KEY` (`DSH_KEY_FILE` / `DSH_API_KEY` en repli). Elle n'est **jamais** affichée :\nni dans le message, ni dans le JSON, ni dans le cache. **Sans cl … [2389 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/README.md", "new_string": "| **4** | dépendance absente : la clé du tagger (absente **ou refusée**) | `--tagger` sans clé, ou clé refusée HTTP 401/403 : message clair, rien sur `stdout`, pas de repli |", "old_string": "| **4** | dépendance absente : la clé du tagger | `-- … [55 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/produit/README.md", "new_string": "La clé est lue dans `DEEPSEEK_KEY_FILE`, `~/.config/drave/deepseek.key`, puis\n`DEEPSEEK_API_KEY` (repli `DSH_*`) ; sans clé **ou avec une clé refusée**, code **4**, rien sur\n`stdout` (§ 3.7). C'est une option **best-effort** : sa justesse dépe … [348 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && env -i HOME=/tmp/drave-e2-home PATH=\"$PATH\" python3 tools/drave.py analyser \"Le chat dort.\" --tagger --json > /tmp/e2-missing-out.txt 2> /tmp/e2-missing-err.txt; echo \"code=$?\"; echo '--- stdout'; cat /tmp/e2-missing-out.txt; e … [94 caractères tronqués]`

  ```
code=4
--- stdout
--- stderr
drave: dépendance absente : clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans ~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/mesurer_e2.py <<'PY'\nimport contextlib, io, json, pathlib, subprocess, sys, tempfile\nsys.path.insert(0, '.'); sys.path.insert(0, 'tools')\nimport drave\nfrom tools.llm.deepseek import DeepSeek, ErreurDeepSeek\n\nRACINE = … [3938 caractères tronqués]`

  ```
[
 {
  "nom": "cle_invalide_analyser",
  "code": 4,
  "stdout_vide": true,
  "stdout_octets": 0,
  "refus": null,
  "source": null,
  "pos_sources": [],
  "stderr": "drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.",
  "commande": "analyser Le chat dort. --tagger --json",
  "fuite_cle": false
 },
 {
  "nom": "cle_invalide_evaluer",
  "code": 4,
  "stdout_vide": true,
  "stdout_octets": 0,
  "refus": null,
  "source": null,
  "pos_sources": [],
  "stderr": "drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.",
  "commande": "evaluer --tagger --json",
  "fuite_cle": false
 },
 {
  "nom": "reseau_coupe",
  "code": 0,
  "stdout_vide": false,
  "stdout_octets": 6265,
  "refus": "neuronal-pos: ErreurDeepSeek: réseau : [Errno -2] Name or service not known",
  "source": "cascade",
  "pos_sources": [
   "heuristique"
  ],
  "stderr": "drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau 
… [1360 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport contextlib, io, json, sys, tempfile\nsys.path.insert(0, '.'); sys.path.insert(0, 'tools')\nimport drave\nfrom tools.llm.deepseek import DeepSeek, ErreurDeepSeek\n\nev = drave._module_evaluation(); chargeur =  … [1104 caractères tronqués]`

  ```
code 0
stderr drave: TAGGER API · modèle=deepseek-chat · appels=2 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s

tagger {'refus': 2, 'refus_detail': ['g001', 'g002'], 'delta_pos': 0.0}
pos tagger 1.0 heur 1.0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp tools/drave.py /tmp/drave-e2-sauve.py && sha256sum tools/drave.py /tmp/drave-e2-sauve.py && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('tools/drave.py')\ns = p.read_text(encoding='utf-8')\nold = '        code = self.stats. … [620 caractères tronqués]`

  ```
dc37c914e5e531ef8867ebbb84ed4598a749fcb54ba92cbc5471f59e88c90dea  tools/drave.py
dc37c914e5e531ef8867ebbb84ed4598a749fcb54ba92cbc5471f59e88c90dea  /tmp/drave-e2-sauve.py
======================================================================
FAIL: test_cle_invalide_code_4 (__main__.TestErreursTagger.test_cle_invalide_code_4)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", line 363, in test_cle_invalide_code_4
    self.assertEqual(code, 4, f"{arguments} → {code} : {erreur}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 4 : ('analyser', 'Le chat dort.', '--tagger', '--json') → 0 : drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: HTTP 401 : invalid key
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s


----------------------------------------------------------------------
Ran 1 test in 0.010s

FAILED (failures=1)
MUTATION-CODE=1
dc37c914e5e531ef8867ebbb84ed4598a749fcb54ba92cbc5471f59e88c90dea  tools/drave.py
dc37c914e5e531ef8867ebbb84ed4
… [59 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib, subprocess\n\ncases = {c[\"nom\"]: c for c in json.loads(pathlib.Path('/tmp/e2-cases.json').read_text())}\nhead = subprocess.check_output([\"git\", \"rev-parse\", \"HEAD\"], text=True).strip()\ … [5012 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 48, in <module>
  File "<stdin>", line 7, in sans_stdout
KeyError: 'commande'
Traceback (most recent call last):
  File "<frozen runpy>", line 203, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/usr/lib64/python3.13/json/tool.py", line 88, in <module>
    main()
    ~~~~^^
  File "/usr/lib64/python3.13/json/tool.py", line 63, in main
    infile = open(options.infile, encoding='utf-8')
FileNotFoundError: [Errno 2] No such file or directory: 'reports/rapport-tagger-erreurs.json'
sed: can't read reports/rapport-tagger-erreurs.json: No such file or directory
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib, subprocess\n\ncases = {c[\"nom\"]: c for c in json.loads(pathlib.Path('/tmp/e2-cases.json').read_text())}\nhead = subprocess.check_output([\"git\", \"rev-parse\", \"HEAD\"], text=True).strip()\ … [5225 caractères tronqués]`

  ```
reports/rapport-tagger-erreurs.json 6629
JSON-OK
{
 "tache": "E2",
 "titre": "Les cas d'erreur de --tagger",
 "date": "2026-11-15",
 "head": "7d4e3bc564590cc47e8a3429dac1a3f33ec75a1f",
 "verdict": "4/4 cas caractérisés ; clé invalide 401 → code 4 (avant : 0, repli muet) ; réseau et refus du modèle → repli heuristique code 0, refus publié ; 18/18 tests.",
 "code": {
  "cli": "drave 0.1.0",
  "schema": 2,
  "fichiers": [
   "tools/drave.py",
   "tools/tests/test_tagger_api.py",
   "docs/produit/README.md",
   "reports/rapport-tagger-erreurs.md"
  ],
  "tests": {
   "commande": "python3 tools/tests/test_tagger_api.py",
   "resultat": "OK",
   "tests": 18
  }
 },
 "dispositif": {
  "mode": "CLI en processus (drave.main) avec un client DeepSeek injecté et un transport factice",
  "reseau": false,
  "sockets": 0,
  "cache": "répertoire temporaire vide par cas (aucune réponse rejouée)",
  "cle": "cle-de-test-sentinelle (factice, jamais affichée)",
  "essais_reseau": 3,
  "date_execution": "2026-11-15",
  "note": "le transport factice lève ErreurDeepSeek ou rend un contenu ; aucun DNS, TLS ni HTTP réel n'est touché"
 },
 "cas_erreur": [
  {
   "nom": "cle_absente",
   "commande": "env -i H
… [2382 caractères tronqués]
  ```

- **write** `{"file_path": "reports/rapport-tagger-erreurs.md", "content": "# E2 — les cas d'erreur de `--tagger` : clé refusée = code 4, réseau et refus du modèle = repli heuristique\n\n> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **E2** · **Date** : 2026-11-15 ·\n> **Verdict** : ✅ **4/4 cas cara … [10512 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-erreurs.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "docs/produit/README.md", "new_string": "`N/M phrase(s) refusée(s)` vont sur `stderr` ; le JSONL partiel est publié. `evaluer --tagger`\nsuit la même règle : clé refusée → **4**, sans sortie ; refus par phrase → `refus: N`,\nmétriques égales à l'heuristique et `delta_pos: 0`, avec la l … [345 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"REVUE-CODE=${PIPESTATUS[0]}\"", "description": "Run documentation review"}`

  ```
revue de documentation · 748 fiche(s) · 841 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 747 fichiers, le disque en a 748
     · compteurs : en-cours.md dit 840 JSON, le disque en a 841
REVUE-CODE=1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -20; echo \"TABLEAUX-CODE=${PIPESTATUS[0]}\"", "description": "Run Markdown table gate"}`

  ```
✅ 1821 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4463 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
TABLEAUX-CODE=0
  ```

- **bash** `{"command": "grep -n \"747\\|840\\|fichiers\\|JSON\" docs/pilotage/en-cours.md | head -30; sed -n '1,60p' docs/pilotage/en-cours.md", "description": "Inspect en-cours counters and header"}`

  ```
97:  [JSON](../../reports/protocole-date.json).
98:- **Panini J12.1–J12.2 + B3** : CIC **42/42** verdicts ; B3 : **42/42** types de Bruijn valides, **42/42** empreintes par **deux** implémentations, **36/36** preuves et **42/42** types altérés rejetés ; [§334](../../reports/rapport-panini-334.md), [CIC](../../reports/rapport-cic-verificateur.md), [v2](../../reports/rapport-cic-v2.md), [JSON](../../reports/cic-verificateur-v2.json).
109:| fichiers / JSON de résultats | **747** / **840** | `reports/*.md` / `reports/*.json` |
# En ce moment

**Mis à jour : 2026-11-15, 06 h 30 HNE (E1 : la FAQ au sommaire et ses liens)**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- 
… [3093 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,130p' docs/pilotage/en-cours.md; echo ====; tail -40 docs/pilotage/en-cours.md", "description": "Read en-cours relevant sections"}`

  ```
- **Plan** : B13.
- **Stratégie** : v0 mesuré.
- **Ambition** : un runtime cognitif tracé.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **att. 238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)) ; **D2** ([v2](../../reports/rapport-restitution-v2.md)) ; **D3** ([FAQ](../../reports/rapport-faq.md), 10/10) ; **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Ce qu'elle fait** : chantier.
- **Prochaine action** : **qualité des rôles** ; T132/T133, gold 200+.
- **Clôture** : **J14.1 faite** (84/81/3 ; `sessions` verte, `indice` et `melange` structurelles ; tag `chantier-2026-11-14`).
- **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**
… [9687 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"B13\\|R0.7\\|tagger\" docs/pilotage/roadmap.md | head -40", "description": "Find roadmap B13/R0.7 lines"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [12532 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '55,75p' docs/pilotage/roadmap.md; echo ====; sed -n '140,165p' docs/pilotage/roadmap.md", "description": "Read roadmap recent-work sections"}`

  ```
J7.1) ; la coordination N2/S/R/A est **datée**. La **clôture formelle** est faite en **J14.1** : sans refaire la passe, les trois rouges sont revérifiées et le tag `chantier-2026-11-14` est posé sur le dernier commit vert. Le détail — chiffres, décisions
D1–D20, rejets R1–R30, échecs, reste — est dans
[`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON.

**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
avec le code courant ; **4 sont corrigés** : la ponctuation finale entre dans le POS (`g001`,
`r241`), le refus sort en **3** et `r035` — l'ancien échec connu — rend exactement le gold
(`REL [9:24] « she talks about » → film`). Le seul bloc identique est `g011`. F1 **0,7902**,
attachement **238/238 labels** (238/239 cibles, 0,9958) ; le mandat 237/238 est l'état d'avant
`s065`. Le contrôle négatif (mutation d'un token dans une copie de la doc) est détecté 4/5.
[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. **D1** ajoute **3** exemples
`--tagger` et **2** `--reel` à [`exemples.md`](../produit/exemples.md)
([`fiche`](../../reports/rapport-exemples-tagger.md)).

**J11.2 — la mesure par langue.** `eval
… [2895 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/*.md | wc -l && ls reports/*.json | wc -l", "description": "Count report files"}`

  ```
748
841
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 07 h 00 HNE (E2 : les cas d'erreur de --tagger)**", "old_string": "**Mis à jour : 2026-11-15, 06 h 30 HNE (E1 : la FAQ au sommaire et ses liens)**"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "limit": 5}`
- **read** `{"file_path": "docs/pilotage/en-cours.md", "limit": 10, "offset": 65}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 06 h 30 HNE (E1 : la FAQ au sommaire et ses liens)**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et

(Showing lines 1-5 of 147. Use offset=6 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
65: - **Ce que font les autres** : **N2**, **S**, **hub**.
66: - **Ce qu'elle fait** : chantier.
67: - **Prochaine action** : **qualité des rôles** ; T132/T133, gold 200+.
68: - **Clôture** : **J14.1 faite** (84/81/3 ; `sessions` verte, `indice` et `melange` structurelles ; tag `chantier-2026-11-14`).
69: - **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**.
70: - **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).
71: 
72: ### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*
73: 
74: - **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).

(Showing lines 65-74 of 147. Use offset=75 to continue.)
</content>
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "limit": 6, "offset": 61}`
- **read** `{"file_path": "docs/pilotage/en-cours.md", "limit": 8, "offset": 90}`
- **read** `{"file_path": "docs/pilotage/en-cours.md", "limit": 8, "offset": 105}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
61: - **Stratégie** : v0 mesuré.
62: - **Ambition** : un runtime cognitif tracé.
63: - **Objectif final** : un moteur de pensée v0.
64: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **att. 238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)) ; **D2** ([v2](../../reports/rapport-restitution-v2.md)) ; **D3** ([FAQ](../../reports/rapport-faq.md), 10/10) ; **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)).
65: - **Ce que font les autres** : **N2**, **S**, **hub**.
66: - **Ce qu'elle fait** : chantier.

(Showing lines 61-66 of 147. Use offset=67 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
90: - **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** ([FAQ](../../reports/rapport-faq.md)), **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
91: - **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
92: - **Panini J2.1–J3.2 + B2** : **14 atomes** ; UDHR **418/438** ; J3.2 : **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, **V14 3/21** ; **B2 : atomes → niveaux négatif** (POS −0,092, syntagmes −0,160, attachement −0,092 ; style absorbé par la date) ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-faces.md), [
… [731 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
105: | invariant | valeur | contrôle |
106: |---|---|---|
107: | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
108: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
109: | fichiers / JSON de résultats | **747** / **840** | `reports/*.md` / `reports/*.json` |
110: | documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
111: | dernière passe | **14/11 00 h 30** (84, **81/3**) ; rouges tolérées `indice`, `melange` ; `sessions` **revérifiée verte** le 14/11 06 h 55 | `docs/pilotage/references-non-regression.md` |
112: 

(Showing lines 105-112 of 147. Use offset=113 to continue.)
</content>
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 07 h 00 HNE (E2 : les cas d'erreur de --tagger)**", "old_string": "**Mis à jour : 2026-11-15, 06 h 30 HNE (E1 : la FAQ au sommaire et ses liens)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **att. 238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J … [1306 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** … [720 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **748** / **841** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **747** / **840** | `reports/*.md` / `reports/*.json` |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restitution v1, produit (J11), cas d'erreur `--tagger` (E2 : clé refusée → 4, repli réseau/modèle → 0)** | **`g017`  … [295 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "docs/pilotage/roadmap.md", "limit": 8, "offset": 152}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
152: rouges sont **revérifiées**. `porte-sessions` passe **verte** après la mise en pause du hub
153: `1e7ef596` et le rafraîchissement du heartbeat `e181ce02` ; `porte-indice` et `porte-melange`
154: restent **rouges structurelles** (mêmes causes : écart au témoin nul pour l'indice ; état de A qui
155: ne rend pas son code pour le mélange). Le tag annoté `chantier-2026-11-14` est posé sur le dernier
156: commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
157: posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +
158: [`JSON`](../../reports/rapport-cloture-chantier.json).
159: La **prochaine mesure** est **B13 — trancher `g017`** (convention d'adverbe), puis T132/T133 et le

(Showing lines 152-159 of 492. Use offset=160 to continue.)
</content>
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "new_string": "posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +\n[`JSON`](../../reports/rapport-cloture-chantier.json).\n\n**E2 — les cas d'erreur de `--tagger`.** La clé **refusée** (HTTP 401/403) sort désormais **4**\navec  … [801 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "ls journal | tail -20; echo ---; ls journal/2026-11-15* 2>/dev/null; echo ---; grep -rn \"E1\\|FAQ\" journal/2026-11-15* 2>/dev/null | head", "description": "Find today's journal file"}`

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
---
distribue.md
docs.md
mesures.md
outils.md
portes.md
README.md
---
journal/2026-11-15/README.md:45:| 06:08 | `5b2d07fc` | D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270) |
journal/2026-11-15/README.md:46:| 06:20 | `4d6cffc4` | PHASE 4 — D1-D3 (LES EXEMPLES DU TAGGER, LA RESTITUTION v2, LA FAQ 10/10) ; L'INDEX, LA FICHE C3 ORPHELINE (GOLD RÉEL 50) ET LE PLAN COMMITTÉS |
journal/2026-11-15/mesures.md:18:| 06:08 | `5b2d07fc` | D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270) | `en-cours.md`, `roadmap.md`, `README.md` (+26) |
journal/2026-11-15/mesures.md:19:| 06:20 | `4d6cffc4` | PHASE 4 — D1-D3 (LES EXEMPLES DU TAGGER, LA RESTITUTION v2, LA FAQ 10/10) ; L'INDEX, LA FICHE C3 ORPHELINE (GOLD RÉEL 50) ET LE PLAN COMMITTÉS | `en-cours.md`, `README.md`, `distribue.md` (+15) |
jo
… [656 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' journal/2026-11-15/README.md; echo =====; sed -n '20,60p' journal/2026-11-15/docs.md; echo =====; sed -n '1,40p' journal/2026-11-15/mesures.md", "description": "Inspect journal structure"}`

  ```
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**18 commits** · **1 session(s)** · **5 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 3 | [distribue.md](distribue.md) |
| docs | 4 | [docs.md](docs.md) |
| mesures | 9 | [mesures.md](mesures.md) |
| outils | 1 | [outils.md](outils.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 349.8 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 
… [10589 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"THEMES\\|theme\\|docs.md\\|mesures.md\\|outils.md\" tools/journal_auto.py | head -60", "description": "Inspect journal theme classification"}`

  ```
48:THEMES: list[tuple[str, str, list[str], list[str]]] = [
95:def theme_de(sujet: str, fichiers: list[str]) -> str:
97:    for slug, _, mots, chemins in THEMES:
100:    for slug, _, _, chemins in THEMES:
106:def titre_theme(slug: str) -> str:
107:    for s, titre, _, _ in THEMES:
306:    par_theme: dict[str, list[dict]] = {}
308:        par_theme.setdefault(theme_de(c["sujet"], c["fichiers"]), []).append(c)
314:            tours.setdefault(theme_de(t, []), []).append((s["id"], t))
317:            etapes.setdefault(theme_de(texte, []), []).append(f"**{heure}** — {texte}")
319:    themes = sorted(set(par_theme) | set(tours))
320:    fichiers_theme = []
321:    for th in themes:
322:        cs = par_theme.get(th, [])
324:            f"# {jour} — {titre_theme(th)}", "",
387:        fichiers_theme.append((th, len(cs), f"{th}.md"))
391:    connus = {s_[0] for s_ in THEMES} | {THEME_DEFAUT[0]}
392:    produits = {th for th, _, _ in fichiers_theme}
409:        f"**{len(themes)} thème(s)**", "",
412:    for th, n, nom in fichiers_theme:
415:    noms_themes = {th for th, _, _ in fichiers_theme}
417:                    if p.name != "README.md" and p.stem not in noms_themes)
449:def generer_th
… [610 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '48,110p' tools/journal_auto.py", "description": "Read journal themes"}`

  ```
THEMES: list[tuple[str, str, list[str], list[str]]] = [
    ("attention", "Attention, fenêtre, puits",
     ["attention", "fenêtre", "fenetre", "puits", "sinks", "attn-", "softmax", "swa"],
     []),
    ("memoire", "Mémoire épisodique, consolidation, greffe",
     ["mémoire", "memoire", "épisodique", "episodique", "greffe", "consolid", "rappel", "indice",
      "magasin", "c6", "c7", "clé", "cle"],
     ["episodique.rs"]),
    ("apprentissage", "Règles locales, hebbien, modulateurs, distillation",
     ["hebb", "décorrélation", "decorrelation", "modulateur", "nouveauté", "nouveaute",
      "règle locale", "regle locale", "apprentissage", "distill", "impulsion", "décharge",
      "decharge", "spiking", "log-normal", "élagage appris", "k-wta appris"],
     []),
    ("distribue", "Régions, flux, protocoles, budgets, pannes",
     ["topologie", "région", "region", "nœud", "noeud", "flux", "bus", "latence", "budget",
      "panne", "registre", "trace", "protocole", "v7", "v8", "paires", "message", "gigue",
      "réparti", "reparti", "relais", "découpage", "decoupage", "lien"],
     ["topologie.rs", "trace_globale.rs", "bus.rs", "flux.rs"]),
    ("modele", "Modèles, entraînement, parci
… [1726 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/verifie_journal.py", "description": "Read journal verifier"}`

  ```
#!/usr/bin/env python3
"""verifie_journal.py — un dossier par jour, et les sessions ancrées.

Règles vérifiées :
  1. aucun fichier `journal/AAAA-MM-JJ*.md` à la racine : chaque jour est un **dossier** ;
  2. chaque dossier `journal/AAAA-MM-JJ/` a un `README.md` ;
  3. chaque `README.md` de jour porte une section « Sessions DSH » et un lien vers
     `../README.md#sessions` ;
  4. chaque `journal/sessions/<id>/rapport.md` porte le bloc « Journaux » avec un lien vers
     son jour (ou le journal), vers `en-cours.md` et vers l'index des sessions ;
  5. les liens relatifs de `journal/README.md`, `journal/THEMES.md`, des `README.md` de jour
     et des rapports de session résolvent.

Usage : python3 tools/verifie_journal.py   (code 0 = journal propre)
"""
from __future__ import annotations
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "journal"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# les liens markdown, sans les ancres ni les liens externes
LIEN = re.compile(r"\]\(([^)#]+?)(?:#[^)]*)?\)")
EXTERNE = ("http://", "https://", "mailto:", "#")


def liens(texte: str) -> list[str]:
    return [c for c in LIEN.findall(texte)
          
… [3313 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -30; echo \"REVUE-CODE=${PIPESTATUS[0]}\"", "description": "Re-run documentation review"}`

  ```
revue de documentation · 748 fiche(s) · 841 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -10; echo \"TABLEAUX-CODE=${PIPESTATUS[0]}\"", "description": "Re-run table gate"}`

  ```
✅ 1821 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4463 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
TABLEAUX-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_tagger_api.py 2>&1 | tail -3; echo \"TAGGER-CODE=${PIPESTATUS[0]}\"", "description": "Run tagger tests"}`

  ```
Ran 18 tests in 3.679s

OK
TAGGER-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo \"EN-COURS-CODE=${PIPESTATUS[0]}\"", "description": "Verify en-cours constraints"}`

  ```
en-cours · 1658 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN-COURS-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -15; echo \"TAILLE-CODE=${PIPESTATUS[0]}\"", "description": "Check document size budget"}`

  ```
2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4028 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9070 mots > budget 9000 (T1)
     · T0 : 4028 mots (AGENTS + en-cours + une tâche) > budget 4 000
TAILLE-CODE=1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py 2>&1 | tail -8; echo \"JOURNAL-CODE=${PIPESTATUS[0]}\"", "description": "Verify journal structure"}`

  ```
journal · 47 jour(s) · 204 session(s) · 2587 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
JOURNAL-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schemas.py 2>&1 | tail -8; echo \"SCHEMAS-CODE=${PIPESTATUS[0]}\"", "description": "Verify SVG schemas"}`

  ```
schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
SCHEMAS-CODE=0
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "new_string": "posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +\n[`JSON`](../../reports/rapport-cloture-chantier.json).\nLa **prochaine mesure** est **B13 — trancher `g017`** (convention d'adverbe), puis T132/T133 et le\n", " … [801 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "docs/pilotage/roadmap.md", "limit": 6, "offset": 155}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
155: ne rend pas son code pour le mélange). Le tag annoté `chantier-2026-11-14` est posé sur le dernier
156: commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
157: posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +
158: [`JSON`](../../reports/rapport-cloture-chantier.json).
159: La **prochaine mesure** est **B13 — trancher `g017`** (convention d'adverbe), puis T132/T133 et le
160: gold 200+.

(Showing lines 155-160 of 492. Use offset=161 to continue.)
</content>
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "new_string": "La **prochaine mesure** est **B13 — trancher `g017`** (convention d'adverbe), puis T132/T133 et le\ngold 200+. **E2** (cas d'erreur `--tagger`) est livré ([fiche](../../reports/rapport-tagger-erreurs.md)).", "old_string": "La **prochaine mesur … [92 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 07 h 00 HNE (E2 : erreurs --tagger)**", "old_string": "**Mis à jour : 2026-11-15, 07 h 00 HNE (E2 : les cas d'erreur de --tagger)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **att. 238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J … [1373 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** … [720 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restitution v1, produit (J11)** | **`g017` tranché** ; T132/T133, gold 452 ; **B10.3 bloquée** |", "old_string": "|  … [295 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -18; echo \"TAILLE-CODE=${PIPESTATUS[0]}\"", "description": "Re-check document size budget"}`

  ```
2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2495    223   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3998 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9007 mots > budget 9000 (T1)
TAILLE-CODE=1
  ```

- **bash** `{"command": "grep -n \"mots\\|split\\|LIEN\\|link\" tools/taille_documents.py | head -40", "description": "Inspect word counting"}`

  ```
5:  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
12:ils ne sont pas chargés automatiquement. Le budget est en **mots** ; l'estimation de tokens
25:# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
72:def mots(texte: str) -> int:
85:def mots_hors_diagrammes(texte: str) -> int:
86:    return mots(DIAGRAMME.sub("", texte))
109:            n = mots_hors_diagrammes(t)
111:            tete = "\n".join(t.splitlines()[:20])
123:                violations.append(f"{rel} : {n} mots > budget {budget} ({cat})")
143:        return mots_hors_diagrammes(q.read_text(encoding="utf-8", errors="ignore")) if q.exists() else 0
146:    # T0 (≤ 1 200 mots) : les trois documents `specifiques` ci-dessus sont des T1, avec leur
147:    # propre budget. Les compter ici faisait payer 1 579 mots au T0 (organisation-du-depot.md)
148:    # au lieu des 1 134 du plus gros T0 — un budget faux de 445 mots, dans le sens qui bloque.
154:        violations.append(f"T0 : {t0} mots (AGENTS + en-cours + une tâche) > budget 4 000")
159:    print(f"  {'mots':>6} {'lignes':>6} {'cat':>4} {'budget':>6}  document")
163:    print(f"  T0 max 
… [28 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '65,90p' tools/taille_documents.py", "description": "Read word counting function"}`

  ```
"docs/implantation/convertisseur.md",
    "docs/implantation/configuration-nvme-raid-amd.md",
    "docs/methode/modularisation.md",
    "docs/pilotage/manques.md",
}


def mots(texte: str) -> int:
    return len(re.findall(r"\S+", texte))


#: Une source de diagramme est **rendue**, pas lue comme de la prose : elle ne compte
#: pas dans le budget de contexte. Le rendu (docwatch) est ce que voit le lecteur ;
#: la source reste dans le document pour être révisée avec lui.
DIAGRAMME = re.compile(
    r"^[ \t]*```[ \t]*(?:plantuml|puml|pu|mermaid|mmd)[ \t]*\n.*?^[ \t]*```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)


def mots_hors_diagrammes(texte: str) -> int:
    return mots(DIAGRAMME.sub("", texte))


def classe(rel: str) -> tuple[str, int]:
    for cat, motif, budget in BUDGETS:
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "new_string": "**Prochaine mesure** : **B13 — trancher `g017`** (convention d'adverbe), puis T132/T133 et le\ngold 200+ ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).", "old_string": "La **prochaine mesure** est **B13 — trancher `g017`** (conve … [147 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -8; echo \"TAILLE-CODE=${PIPESTATUS[0]}\"", "description": "Re-check size budget"}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3998 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9002 mots > budget 9000 (T1)
TAILLE-CODE=1
  ```

- **edit** `{"file_path": "docs/pilotage/roadmap.md", "new_string": "**Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le\ngold 200+ ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).", "old_string": "**Prochaine mesure** : **B13 — trancher `g017`** (convention d'adverbe), puis T132/T133  … [79 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -7; echo \"TAILLE-CODE=${PIPESTATUS[0]}\"", "description": "Check size budget again"}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3998 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
TAILLE-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -6; echo \"REVUE-CODE=${PIPESTATUS[0]}\"", "description": "Run doc review"}`

  ```
revue de documentation · 748 fiche(s) · 841 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -6; echo \"TABLEAUX-CODE=${PIPESTATUS[0]}\"", "description": "Run table/link gate"}`

  ```
✅ 1821 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4463 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
TABLEAUX-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -5; echo \"EN-COURS-CODE=${PIPESTATUS[0]}\"", "description": "Verify en-cours"}`

  ```
en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN-COURS-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh 2>&1 | tail -30; echo \"PRODUIT-CODE=${PIPESTATUS[0]}\"", "description": "Run product gate", "timeoutMs": 300000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 20 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
PRODUIT-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- tools/drave.py tools/tests/test_tagger_api.py | sed -n '1,240p'", "description": "Review code diff"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index 25f0a204..045d895d 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -27,7 +27,8 @@ l'API DeepSeek : la clé est lue dans `DEEPSEEK_KEY_FILE`, `~/.config/drave/deep
 Ce que la commande n'expose pas : le neuronal local (`llama-cli` ou endpoint), la traduction et la
 génération : ils demandent des poids, un service ou un GPU.
 
-Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger absent · 1 erreur.
+Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible
+(absente ou refusée) · 1 erreur.
 """
 from __future__ import annotations
 
@@ -92,6 +93,22 @@ class CleTaggerAbsente(RuntimeError):
     """Aucune clé : le tagger est une option, jamais un prérequis du produit."""
 
 
+class CleTaggerRefusee(RuntimeError):
+    """L'API refuse la clé (HTTP 401/403) : ce n'est pas un refus de phrase, c'est un arrêt.
+
+    Une clé absente et une clé refusée sont la même dépendance manquante du point de vue du
+    produit : le code 4, un message qui nomme les trois sources de la clé, et rien sur `stdout`.
+    """
+
+    def __init__(self, code: int) -> None:
+        self.code = int(code)
+        s
… [11039 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --check -- tools/drave.py tools/tests/test_tagger_api.py docs/produit/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-tagger-erreurs.md reports/rapport-tagger-erreurs.json; echo \"DIFF-CHECK=$?\" … [68 caractères tronqués]`

  ```
DIFF-CHECK=0
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
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
?? reports/rapport-tagger-erreurs.json
?? reports/rapport-tagger-erreurs.md
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"rapport-tagger-option\\|rapport-exemples-tagger\\|rapport-faq-sommaire\" reports/INDEX.md reports/README.md | head -20", "description": "Check report indexes"}`

  ```
reports/INDEX.md:185:| [rapport-exemples-tagger.md](rapport-exemples-tagger.md) | D1 — les exemples `--tagger` et `--reel` : le coût affiché, la base honnête, cinq blocs rejoués |
reports/INDEX.md:187:| [rapport-faq-sommaire.md](rapport-faq-sommaire.md) | E1 — la FAQ dans le sommaire et les liens : 9 ancres, 5 liens, 0 mort |
reports/INDEX.md:732:| [rapport-tagger-option.md](rapport-tagger-option.md) | R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne |
reports/README.md:27:| [`rapport-exemples-tagger.md`](rapport-exemples-tagger.md) | **D1** — les 3 exemples `--tagger` (coût affiché) et les 2 `--reel` (base honnête) |
reports/README.md:41:| [`rapport-tagger-option.md`](rapport-tagger-option.md) | **R0.7 / 1A** — le tagger POS en option : **+8,57** sur 20 phrases, **+9,5** sur 612, défaut hors ligne |
  ```

- **bash** `{"command": "grep -rln \"INDEX.md\" tools/*.py | head; grep -n \"INDEX\" tools/revue_documentation.py | head", "description": "Find report index generator"}`

  ```
tools/index_reports.py
tools/surveille_sessions.py
tools/taille_documents.py
  ```

- **bash** `{"command": "sed -n '1,60p' tools/index_reports.py", "description": "Read report index generator"}`

  ```
#!/usr/bin/env python3
"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.

L'index est **exhaustif** et **déterministe** : une ligne par fiche, triée par nom,
avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
et `historique-*`) sont exclus du tableau ; les compteurs de `docs/pilotage/en-cours.md`
comptent, eux, tous les `.md` de `reports/`.

Usage :
    python3 tools/index_reports.py              # réécrit reports/INDEX.md
    python3 tools/index_reports.py --verifier   # ne réécrit rien, sort 1 si périmé
    python3 tools/index_reports.py --aide       # affiche l'aide (ne touche à rien)
"""
from __future__ import annotations

import argparse
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent


def titre(p: pathlib.Path) -> str:
    for ligne in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if ligne.startswith("# "):
            return ligne[2:].strip().replace("|", "—")
    return p.stem.replace("-", " ")


def fiches() -> list[pathlib.Path]:
    return sorted(
        p for p in (RACINE / "reports").glob("*.md")
        if p.name not in ("README.md", "INDEX.md") and not p.n
… [1005 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py && python3 tools/index_reports.py --verifier; echo \"INDEX-CODE=$?\"; grep -n \"rapport-tagger-erreurs\" reports/INDEX.md", "description": "Regenerate report index"}`

  ```
745 fiches → reports/INDEX.md
INDEX-CODE=0
732:| [rapport-tagger-erreurs.md](rapport-tagger-erreurs.md) | E2 — les cas d'erreur de `--tagger` : clé refusée = code 4, réseau et refus du modèle = repli heuristique |
  ```

- **bash** `{"command": "tail -60 journal/2026-11-15/mesures.md", "description": "Read end of measures journal"}`

  ```
| 04:03 | `2067a6f0` | B3 — LE CORPUS D'OR CIC V2 : 42/42 TYPES DE BRUJIN BIEN FORMÉS, 42/42 SHA256 PAR DEUX IMPLÉMENTATIONS, 36/36 PREUVES ET 42/42 TYPES ALTÉRÉS REJETÉS | `en-cours.md`, `roadmap.md`, `README.md` (+18) |
| 04:33 | `ee04ea91` | BILAN DE LA NUIT — LE TAGGER (95,75), LA BASE HONNÊTE (452), LA PHASE C/B (N2, S, R, PANINI) ET LES NÉGATIFS DITS | `en-cours.md`, `README.md`, `distribue.md` (+11) |
| 04:46 | `d23780d7` | D1 — LES EXEMPLES DU TAGGER ET DE LA BASE RÉELLE : 3 BLOCS --tagger (441 TOKENS, 3,7 S), 2 BLOCS --reel (452 PHRASES, POS 88,91, F1 79,06), 5/5 REJOUÉS, MUTATION 4/5 | `en-cours.md`, `roadmap.md`, `README.md` (+16) |
| 06:08 | `5b2d07fc` | D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270) | `en-cours.md`, `roadmap.md`, `README.md` (+26) |
| 06:20 | `4d6cffc4` | PHASE 4 — D1-D3 (LES EXEMPLES DU TAGGER, LA RESTITUTION v2, LA FAQ 10/10) ; L'INDEX, LA FICHE C3 ORPHELINE (GOLD RÉEL 50) ET LE PLAN COMMITTÉS | `en-cours.md`, `README.md`, `distribue.md` (+15) |

## Chiffres du jour

`0,5270` · `0,092` · `0,160` · `0,811` · `0,657` · `0,440` · `0,429` · `2,7856` · `40
… [3456 caractères tronqués]
  ```

- **edit** `{"file_path": "journal/2026-11-15/mesures.md", "new_string": "[`rapport-faq.md`](../../reports/rapport-faq.md).\n\n### E2 — les cas d'erreur du tagger : la clé refusée sort 4, le reste replie\n\nQuatre cas, un transport factice, **18/18 tests**, **0 socket**. La **clé absente** sortait déjà\n**4** ; … [718 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "journal/2026-11-15/mesures.md", "limit": 10, "offset": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md</path>
<type>file</type>
<content>
70: 22 299 tokens / 155 s / ~0,02 $**. Le vérificateur est
71: [`tools/verifier_faq.py`](../../tools/verifier_faq.py), le relevé
72: [`faq.json`](../../reports/faq.json), la fiche
73: [`rapport-faq.md`](../../reports/rapport-faq.md).
74: <!-- /notes -->

(End of file - total 74 lines)
</content>
  ```

- **edit** `{"file_path": "journal/2026-11-15/mesures.md", "new_string": "[`rapport-faq.md`](../../reports/rapport-faq.md).\n\n### E2 — les cas d'erreur du tagger : la clé refusée sort 4, le reste replie\n\nQuatre cas, un transport factice, **18/18 tests**, **0 socket**. La **clé absente** sortait déjà\n**4** ; … [718 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/toutes-les-portes.sh > /tmp/e2-portes.log 2>&1; echo \"PORTES-CODE=$?\" >> /tmp/e2-portes.log", "description": "Run all gates in background", "run_in_background": true}`

  ```
started background job bash-71
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/drave.py tools/tests/test_tagger_api.py docs/produit/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-tagger-erreurs.md reports/rapport-tagger-erreurs.json reports/INDEX.md journal/2026-11-15 … [133 caractères tronqués]`

  ```
CHECK=0
 docs/pilotage/en-cours.md           |   6 +-
 docs/pilotage/roadmap.md            |   4 +-
 docs/produit/README.md              |  27 ++++++-
 journal/2026-11-15/mesures.md       |  11 +++
 reports/INDEX.md                    |   3 +-
 reports/rapport-tagger-erreurs.json | 154 ++++++++++++++++++++++++++++++++++++
 reports/rapport-tagger-erreurs.md   | 148 ++++++++++++++++++++++++++++++++++
 tools/drave.py                      |  57 ++++++++++---
 tools/tests/test_tagger_api.py      | 118 ++++++++++++++++++++++++++-
 9 files changed, 508 insertions(+), 20 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --cached -- reports/INDEX.md docs/pilotage/roadmap.md docs/pilotage/en-cours.md | sed -n '1,160p'", "description": "Review index/state diffs"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 9189bf57..3313bcc8 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 06 h 30 HNE (E1 : la FAQ au sommaire et ses liens)**
+**Mis à jour : 2026-11-15, 07 h 00 HNE (E2 : erreurs --tagger)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -61,7 +61,7 @@
 - **Stratégie** : v0 mesuré.
 - **Ambition** : un runtime cognitif tracé.
 - **Objectif final** : un moteur de pensée v0.
-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **att. 238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)) ; **D2** ([v2](../../reports/rapport-restitut
… [4418 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-71", "wait": true, "timeout_ms": 240000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"HTTP 401\\|401\\|ErreurDeepSeek\" tools/tests --include=*.py | head -20", "description": "Search tests for 401 expectations"}`

  ```
tools/tests/linguistique/gold_reel.py:1255:    ('r401', 'en', 'The wind blows; it freezes.',
tools/tests/test_tagger_api.py:13:   - **clé invalide** (HTTP 401/403) → code **4**, message clair, `stdout` vide, pas de repli ;
tools/tests/test_tagger_api.py:46:from tools.llm.deepseek import DeepSeek, ErreurDeepSeek  # noqa: E402
tools/tests/test_tagger_api.py:328:    - **clé invalide** : 401/403 n'est pas un refus de phrase ; le CLI sort **4**, `stdout`
tools/tests/test_tagger_api.py:357:                raise ErreurDeepSeek("HTTP 401 : invalid key", code=401)
tools/tests/test_tagger_api.py:366:                self.assertIn("HTTP 401", erreur)
tools/tests/test_tagger_api.py:378:                raise ErreurDeepSeek("réseau : [Errno -2] Name or service not known",
  ```

- **job_output** `{"job_id": "bash-71", "timeout_ms": 240000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -20 /tmp/e2-portes.log; echo ---; wc -l /tmp/e2-portes.log", "description": "Check gate progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (85 portes, borne 1800 s) ===
    journaux : work/portes-1115-06h45
  porte-adaptateur-sortie ✅                          69 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         170 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          15 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          51 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          99 s    ✅ le canal diffusé par fichier change la région du milieu
---
12 /tmp/e2-portes.log
  ```

- **bash** `{"command": "grep -n \"rapport-faq-sommaire\\|E1\\|rapport-tagger\" reports/README.md", "description": "Check curated report index"}`

  ```
41:| [`rapport-tagger-option.md`](rapport-tagger-option.md) | **R0.7 / 1A** — le tagger POS en option : **+8,57** sur 20 phrases, **+9,5** sur 612, défaut hors ligne |
  ```

- **job_output** `{"job_id": "bash-71", "timeout_ms": 300000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -12 /tmp/e2-portes.log; echo ---; wc -l /tmp/e2-portes.log", "description": "Check gate progress"}`

  ```
porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          15 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          51 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          99 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅                          99 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard        ✅                          32 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne
  porte-cerveau          ✅                           9 s    ✅ porte tenue (quatre facultés composent, chacune reste active, le tout est déterministe)
  porte-cic              ✅                          12 s  ✅ porte CIC verte : 42/42 verdicts, empreintes, de Bruijn, sha256 2e implémentation,
  porte-consolidation    ✅                  
… [288 caractères tronqués]
  ```

- **edit** `{"file_path": "docs/produit/README.md", "new_string": "lisible.\n\n**En `--jsonl`**, une clé refusée peut laisser sur `stdout` les lignes déjà écrites avant le\ncode **4** (le premier texte sans appel neuronal ne déclenche pas le 401) ; le message et le\ncode restent les mêmes. Le tableau ci-dessus  … [67 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"En \\`--jsonl\\`\" -B4 -A4 docs/produit/README.md", "description": "Check inserted jsonl note"}`

  ```
432-suit la même règle : clé refusée → **4**, sans sortie ; refus par phrase → `refus: N`,
433-métriques égales à l'heuristique et `delta_pos: 0`, avec la ligne `REFUS` dans la sortie
434-lisible.
435-
436:**En `--jsonl`**, une clé refusée peut laisser sur `stdout` les lignes déjà écrites avant le
437-code **4** (le premier texte sans appel neuronal ne déclenche pas le 401) ; le message et le
438-code restent les mêmes. Le tableau ci-dessus décrit `analyser` sur **un** texte.
439-
440-**Ce que l'option change — et ce qu'elle ne change pas.** Le **POS** vient du tagger
  ```

- **edit** `{"file_path": "reports/rapport-tagger-erreurs.md", "new_string": "- **Le code 0 du repli n'est pas un feu vert** : il dit « l'analyse est rendue », pas « le\n  tagger a fonctionné ». Un script qui ne lit que le code de sortie doit lire aussi `refus`\n  (ou `stderr`) pour distinguer les deux.\n- **`- … [445 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-erreurs.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-tagger-erreurs.json", "new_string": "  \"le coût affiché (appels=1) compte les appels du tagger, pas les 3 tentatives internes du client réseau\",\n  \"en --jsonl, le code 4 peut arriver après des lignes déjà écrites (le premier texte sans appel neuronal ne déclenche p … [201 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-erreurs.json": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "reports/rapport-tagger-erreurs.json", "limit": 12, "offset": 145}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-erreurs.json</path>
<type>file</type>
<content>
145:   "pourquoi": "une clé refusée n'est pas un refus de phrase : c'est la même dépendance manquante qu'une clé absente"
146:  },
147:  "limites": [
148:   "le transport factice ne teste ni DNS, ni TLS, ni proxy : un 401/403 réel peut arriver avec un corps différent",
149:   "le code HTTP est lu sur ErreurDeepSeek.code : un proxy qui rend 400 avec « invalid key » suivrait le repli, pas le code 4",
150:   "le refus du modèle est simulé (texte non JSON, JSON de mauvaise longueur), pas un refus d'un modèle réel",
151:   "le cache disque est vide par cas : avec un cache déjà rempli, une panne réseau peut être masquée par une réponse ancienne",
152:   "le coût affiché (appels=1) compte les appels du tagger, pas les 3 tentatives internes du client réseau"
153:  ]
154: }

(End of file - total 154 lines)
</content>
  ```

- **edit** `{"file_path": "reports/rapport-tagger-erreurs.json", "new_string": "  \"le coût affiché (appels=1) compte les appels du tagger, pas les 3 tentatives internes du client réseau\",\n  \"en --jsonl, le code 4 peut arriver après des lignes déjà écrites (le premier texte sans appel neuronal ne déclenche p … [201 caractères tronqués]`

  ```
Error: old_string was not found in "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-erreurs.json"
  ```

- **edit** `{"file_path": "reports/rapport-tagger-erreurs.json", "new_string": "  \"le coût affiché (appels=1) compte les appels du tagger, pas les 3 tentatives internes du client réseau\",\n  \"en --jsonl, le code 4 peut arriver après des lignes déjà écrites (le premier texte sans appel neuronal ne déclenche p … [201 caractères tronqués]`

  ```
Error: old_string was not found in "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-erreurs.json"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\nlines = pathlib.Path('reports/rapport-tagger-erreurs.json').read_text(encoding='utf-8').splitlines()\nfor i in (151, 152):\n    print(i+1, repr(lines[i]))\nPY", "description": "Inspect exact JSON lin … [3 caractères tronqués]`

  ```
152 '  "le coût affiché (appels=1) compte les appels du tagger, pas les 3 tentatives internes du client réseau"'
153 ' ]'
  ```

- **edit** `{"file_path": "reports/rapport-tagger-erreurs.json", "new_string": "  \"le coût affiché (appels=1) compte les appels du tagger, pas les 3 tentatives internes du client réseau\",\n  \"en --jsonl, le code 4 peut arriver après des lignes déjà écrites (le premier texte sans appel neuronal ne déclenche p … [191 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-erreurs.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-tagger-erreurs.json > /dev/null && echo JSON-OK && tail -5 reports/rapport-tagger-erreurs.json", "description": "Validate updated JSON"}`

  ```
JSON-OK
  "le cache disque est vide par cas : avec un cache déjà rempli, une panne réseau peut être masquée par une réponse ancienne",
  "le coût affiché (appels=1) compte les appels du tagger, pas les 3 tentatives internes du client réseau",
  "en --jsonl, le code 4 peut arriver après des lignes déjà écrites (le premier texte sans appel neuronal ne déclenche pas 401) ; les mesures portent sur analyser avec un seul texte"
 ]
}
  ```

- **bash** `{"command": "tail -8 /tmp/e2-portes.log; echo ---; wc -l /tmp/e2-portes.log", "description": "Check gate progress"}`

  ```
porte-budget           ✅                          51 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          99 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅                          99 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard        ✅                          32 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne
  porte-cerveau          ✅                           9 s    ✅ porte tenue (quatre facultés composent, chacune reste active, le tout est déterministe)
  porte-cic              ✅                          12 s  ✅ porte CIC verte : 42/42 verdicts, empreintes, de Bruijn, sha256 2e implémentation,
  porte-consolidation    ✅                          83 s    ✅ porte tenue (fusion exacte : nulle ⇒ identique, réelle ⇒ visible, lecteur ⇒ hors fichier)
  porte-coupe            ✅                         138 s    ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit
---
18 /tmp/e2-portes.log
  ```

- **job_output** `{"job_id": "bash-71", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -4; echo \"REVUE-CODE=${PIPESTATUS[0]}\"", "description": "Doc review after README edit"}`

  ```
revue de documentation · 748 fiche(s) · 841 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -4; echo \"TABLEAUX-CODE=${PIPESTATUS[0]}\"", "description": "Table gate after README edit"}`

  ```
✅ 1821 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4464 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
TABLEAUX-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/produit/README.md reports/rapport-tagger-erreurs.md reports/rapport-tagger-erreurs.json && git diff --cached --check; echo \"CHECK=$?\"; git diff --cached --stat", "description": "Re-stage modified docs"}`

  ```
CHECK=0
 docs/pilotage/en-cours.md           |   6 +-
 docs/pilotage/roadmap.md            |   4 +-
 docs/produit/README.md              |  31 +++++++-
 journal/2026-11-15/mesures.md       |  11 +++
 reports/INDEX.md                    |   3 +-
 reports/rapport-tagger-erreurs.json | 155 ++++++++++++++++++++++++++++++++++++
 reports/rapport-tagger-erreurs.md   | 151 +++++++++++++++++++++++++++++++++++
 tools/drave.py                      |  57 ++++++++++---
 tools/tests/test_tagger_api.py      | 118 ++++++++++++++++++++++++++-
 9 files changed, 516 insertions(+), 20 deletions(-)
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C bash -C python3 | grep -E \"toutes-les-portes|porte-|python3\" | head -10", "description": "Check running gate process"}`

  ```
3002 11-11:25:30 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
2725526    14:46:01 bash -c sleep 2; cd /home/stephane/Data13TB/stephane/GitHub/financemeteo && python3 src/app.py --no-browser
2725542    14:45:59 python3 src/app.py --no-browser
3013484    01:50:56 bash -c bash tools/toutes-les-portes.sh 2>&1 | tail -120
3013491    01:50:56 bash tools/toutes-les-portes.sh
3370403       32:43 python3 tools/chantier/superviseur.py boucle --budget 7200 --timeout 3000
3497177       14:15 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/toutes-les-portes.sh > /tmp/e2-portes.log 2>&1; echo "PORTES-CODE=$?" >> /tmp/e2-portes.log
3497202       14:14 bash tools/toutes-les-portes.sh
3615681       03:00 bash tools/porte-vision.sh
3629253       01:00 bash tools/porte-cycle-c2.sh
  ```

- **job_output** `{"job_id": "bash-71", "timeout_ms": 300000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -10 /tmp/e2-portes.log; echo ---; wc -l /tmp/e2-portes.log", "description": "Check gate progress"}`

  ```
porte-cerveau          ✅                           9 s    ✅ porte tenue (quatre facultés composent, chacune reste active, le tout est déterministe)
  porte-cic              ✅                          12 s  ✅ porte CIC verte : 42/42 verdicts, empreintes, de Bruijn, sha256 2e implémentation,
  porte-consolidation    ✅                          83 s    ✅ porte tenue (fusion exacte : nulle ⇒ identique, réelle ⇒ visible, lecteur ⇒ hors fichier)
  porte-coupe            ✅                         138 s    ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit
  porte-cycle-c2         ✅                         127 s    ✅ porte tenue (chaîne exacte · pas 1 exact · borné · coût dit · trajectoire déterministe ·
  porte-deepseek         ✅                           0 s    ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
  porte-delais           ✅                          21 s    ✅ le temps, lui, augmente : 6.91 s → 9.67 s (+2.8 s ≈ 50 ms × 64 pas)
  porte-diff-couche      ✅                          18 s    ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé
  porte-document         ✅           
… [141 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"TAGGER — LES CAS D'ERREUR MESURÉS : CLÉ REFUSÉE → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES\" -m \"Tâche E2. Quatre cas, transport factice, 0 socket.\n\n- c … [755 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-87]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-87", "timeout_ms": 120000, "wait": true}`

  ```
✅ index : aucun fait stagé sans état
[s/v7 d1c1e467] TAGGER — LES CAS D'ERREUR MESURÉS : CLÉ REFUSÉE → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES
 22 files changed, 3564 insertions(+), 49 deletions(-)
 create mode 100644 journal/sessions/session-01599146-2479-4a06-8381-4ace3d13f579/digest.md
 create mode 100644 journal/sessions/session-01599146-2479-4a06-8381-4ace3d13f579/rapport.md
 create mode 100644 reports/rapport-tagger-erreurs.json
 create mode 100644 reports/rapport-tagger-erreurs.md
COMMIT-CODE=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline HEAD | sed -n '1,60p'; echo ---; git status --short | head -30", "description": "Inspect committed files"}`

  ```
d1c1e467 TAGGER — LES CAS D'ERREUR MESURÉS : CLÉ REFUSÉE → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES
 docs/pilotage/en-cours.md                          |    6 +-
 docs/pilotage/roadmap.md                           |    4 +-
 docs/produit/README.md                             |   31 +-
 journal/2026-11-15/README.md                       |    7 +-
 journal/2026-11-15/distribue.md                    |    6 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/mesures.md                      |   13 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    7 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   34 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 2635 ++++++++++++++++++++
 .../rapport.md                                     |  159 ++
 .../digest.md                                      |  165 ++
 .../rapport.md              
… [801 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline 7d4e3bc5 | sed -n '1,30p'; echo ---; git show --stat --oneline ee04ea91 | sed -n '1,20p'", "description": "Compare previous commit stats"}`

  ```
7d4e3bc5 E1 — LA FAQ AU SOMMAIRE ET SES LIENS : 9/9 ANCRES, 5/5 LIENS, 0 MORT ; LA LIGNE FAQ DANS docs/README, LES RÉPONSES INCHANGÉES
 docs/README.md                                     |    1 +
 docs/pilotage/en-cours.md                          |    8 +-
 docs/produit/README.md                             |   13 +
 journal/2026-11-15/README.md                       |    6 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |   15 +-
 journal/2026-11-15/mesures.md                      |    2 +-
 journal/2026-11-15/outils.md                       |   31 +
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    3 +-
 journal/THEMES.md                                  |    1 +
 journal/sessions/MANIFEST.md                       |    5 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   50 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 1900 ++++++++++++++++++++
 .../rapport.md                                     |  166 ++
 reports/INDEX.md                                   |    3 +
… [1314 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD:journal/2026-11-15/mesures.md | grep -n \"E2 — les cas\" -A 12 | head -20; echo ---; git show HEAD:journal/2026-11-15/README.md | grep -n \"TAGGER\\|TAGGER\" | head", "description": "Check journal note in commit"}`

  ```
75:### E2 — les cas d'erreur du tagger : la clé refusée sort 4, le reste replie
76-
77-Quatre cas, un transport factice, **18/18 tests**, **0 socket**. La **clé absente** sortait déjà
78-**4** ; la **clé invalide** (HTTP 401/403) rendait **0** avec un repli heuristique muet — elle
79-sort désormais **4**, message clair, `stdout` vide, sans repli. Le **réseau coupé** (3 essais du
80-client) et le **refus du modèle** (texte non JSON, JSON incomplet) restent des refus **par
81-phrase** : repli heuristique, code **0**, cause dans `refus`, POS `source=heuristique`. Un
82-transport valide donne code **0** et des POS neuronaux (contrôle négatif) ; retirer le contrôle
83-401/403 fait échouer le test (`0 != 4`). [`fiche`](../../reports/rapport-tagger-erreurs.md) ·
84-[`JSON`](../../reports/rapport-tagger-erreurs.json).
85-<!-- /notes -->
---
31:| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |
32:| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |
41:| 04:
… [867 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD:journal/2026-11-15/README.md | grep -n \"d1c1e467\\|CAS D'ERREUR\" | head; echo ---; git show HEAD:journal/2026-11-15/mesures.md | grep -n \"d1c1e467\\|CAS D'ERREUR\" | head", "description": "Check if new commit in jour … [11 caractères tronqués]`

  ```
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/journal_auto.py 2>&1 | tail -20; echo \"JOURNAL-AUTO-CODE=${PIPESTATUS[0]}\"; git status --short | head -30", "description": "Regenerate journal with new commit"}`

  ```
2026-11-15 : 20 commits
  journal/2026-11-15/distribue.md
  journal/2026-11-15/docs.md
  journal/2026-11-15/memoire.md
  journal/2026-11-15/mesures.md
  journal/2026-11-15/outils.md
  journal/2026-11-15/portes.md
  journal/2026-11-15/README.md
  journal/THEMES.md
8 fichiers écrits · 20 commits classés
JOURNAL-AUTO-CODE=0
 M journal/2026-11-15/README.md
 M journal/THEMES.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? journal/2026-11-15/memoire.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/hooks/ | grep -v sample; echo ---; sed -n '1,120p' .git/hooks/pre-commit 2>/dev/null", "description": "Inspect pre-commit hook"}`

  ```
pre-commit
---
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
# Le journal du jour, par thème (sources : git + journal/sessions). L'i
… [249 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"unlink\\|supprim\\|orphelin\\|fichiers_theme\" tools/journal_auto.py | head -30", "description": "Check journal stale theme handling"}`

  ```
320:    fichiers_theme = []
387:        fichiers_theme.append((th, len(cs), f"{th}.md"))
392:    produits = {th for th, _, _ in fichiers_theme}
398:            vieux.unlink()
412:    for th, n, nom in fichiers_theme:
415:    noms_themes = {th for th, _, _ in fichiers_theme}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit --amend -m \"TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES\" -m \"Tâche E2. Quatre cas, transport fact … [796 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-95]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-95", "timeout_ms": 120000, "wait": true}`

  ```
[s/v7 840e613e] TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES
 Date: Sun Nov 15 07:04:51 2026 -0500
 24 files changed, 3763 insertions(+), 49 deletions(-)
 create mode 100644 journal/2026-11-15/memoire.md
 create mode 100644 journal/sessions/session-01599146-2479-4a06-8381-4ace3d13f579/digest.md
 create mode 100644 journal/sessions/session-01599146-2479-4a06-8381-4ace3d13f579/rapport.md
 create mode 100644 reports/rapport-tagger-erreurs.json
 create mode 100644 reports/rapport-tagger-erreurs.md
AMEND-CODE=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/journal_auto.py 2>&1 | tail -20; echo \"JOURNAL-AUTO-CODE=${PIPESTATUS[0]}\"; git status --short | head -30", "description": "Regenerate journal after amend"}`

  ```
2026-11-15 : 20 commits
  journal/2026-11-15/distribue.md
  journal/2026-11-15/docs.md
  journal/2026-11-15/mesures.md
  journal/2026-11-15/outils.md
  journal/2026-11-15/portes.md
  (retiré, thème vide) journal/2026-11-15/memoire.md
  journal/2026-11-15/README.md
  journal/THEMES.md
8 fichiers écrits · 20 commits classés
JOURNAL-AUTO-CODE=0
 M journal/2026-11-15/README.md
 D journal/2026-11-15/memoire.md
 M journal/2026-11-15/mesures.md
 M journal/THEMES.md
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
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"840e613e\\|CAS D'ERREUR\" journal/2026-11-15/README.md journal/2026-11-15/mesures.md | head; echo ---; git diff --stat -- journal", "description": "Check journal includes commit"}`

  ```
journal/2026-11-15/README.md:49:| 07:04 | `840e613e` | TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES |
journal/2026-11-15/mesures.md:20:| 07:04 | `840e613e` | TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES | `en-cours.md`, `roadmap.md`, `README.md` (+21) |
---
 journal/2026-11-15/README.md  |  7 +++----
 journal/2026-11-15/memoire.md | 24 ------------------------
 journal/2026-11-15/mesures.md |  4 +++-
 journal/THEMES.md             |  1 -
 4 files changed, 6 insertions(+), 30 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"E2 — les cas\" -A 10 journal/2026-11-15/mesures.md | head -14; echo ---; git diff -- journal/2026-11-15/mesures.md | sed -n '1,80p'", "description": "Verify E2 note preserved"}`

  ```
77:### E2 — les cas d'erreur du tagger : la clé refusée sort 4, le reste replie
78-
79-Quatre cas, un transport factice, **18/18 tests**, **0 socket**. La **clé absente** sortait déjà
80-**4** ; la **clé invalide** (HTTP 401/403) rendait **0** avec un repli heuristique muet — elle
81-sort désormais **4**, message clair, `stdout` vide, sans repli. Le **réseau coupé** (3 essais du
82-client) et le **refus du modèle** (texte non JSON, JSON incomplet) restent des refus **par
83-phrase** : repli heuristique, code **0**, cause dans `refus`, POS `source=heuristique`. Un
84-transport valide donne code **0** et des POS neuronaux (contrôle négatif) ; retirer le contrôle
85-401/403 fait échouer le test (`0 != 4`). [`fiche`](../../reports/rapport-tagger-erreurs.md) ·
86-[`JSON`](../../reports/rapport-tagger-erreurs.json).
87-<!-- /notes -->
---
diff --git a/journal/2026-11-15/mesures.md b/journal/2026-11-15/mesures.md
index 6a4dfdee..d2f20e61 100644
--- a/journal/2026-11-15/mesures.md
+++ b/journal/2026-11-15/mesures.md
@@ -4,7 +4,7 @@
 > Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
 > Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](READM
… [1546 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add journal/2026-11-15/README.md journal/2026-11-15/memoire.md journal/2026-11-15/mesures.md journal/THEMES.md && git diff --cached --check; echo \"CHECK=$?\"; git commit -m \"JOURNAL — 2026-11-15 : E2, LES CAS D'ERREUR DU TAGGER … [192 caractères tronqués]`

  ```
CHECK=0
[still running after 60000ms; moved to background job bash-99]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-99", "timeout_ms": 120000, "wait": true}`

  ```
✅ index : aucun fait stagé sans état
[s/v7 7ee92dd9] JOURNAL — 2026-11-15 : E2, LES CAS D'ERREUR DU TAGGER (REFUS D'AUTHENTIFICATION → CODE 4, RÉSEAU ET RÉPONSE NON CONFORME → REPLI 0 ; 18/18)
 8 files changed, 110 insertions(+), 41 deletions(-)
 delete mode 100644 journal/2026-11-15/memoire.md
JOURNAL-COMMIT-CODE=0
[status: completed, exit code: 0]
  ```

- **job_output** `{"job_id": "bash-71", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -12 /tmp/e2-portes.log; echo ---; wc -l /tmp/e2-portes.log", "description": "Check full gate progress"}`

  ```
porte-coupe            ✅                         138 s    ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit
  porte-cycle-c2         ✅                         127 s    ✅ porte tenue (chaîne exacte · pas 1 exact · borné · coût dit · trajectoire déterministe ·
  porte-deepseek         ✅                           0 s    ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
  porte-delais           ✅                          21 s    ✅ le temps, lui, augmente : 6.91 s → 9.67 s (+2.8 s ≈ 50 ms × 64 pas)
  porte-diff-couche      ✅                          18 s    ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé
  porte-document         ✅                           5 s  ✅ porte document verte
  porte-echange-experts  ✅                          53 s    PORTE TENUE
  porte-episodique       ✅                         167 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          27 s    mode
… [368 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -4; echo \"REVUE-CODE=${PIPESTATUS[0]}\"", "description": "Post-commit doc review"}`

  ```
revue de documentation · 748 fiche(s) · 841 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -4; echo \"TAILLE-CODE=${PIPESTATUS[0]}\"", "description": "Post-commit size budget"}`

  ```
avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
TAILLE-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py 2>&1 | tail -4; echo \"JOURNAL-CODE=${PIPESTATUS[0]}\"", "description": "Post-commit journal check"}`

  ```
journal · 47 jour(s) · 205 session(s) · 2592 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
JOURNAL-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -4; echo \"EN-COURS-CODE=${PIPESTATUS[0]}\"", "description": "Post-commit en-cours check"}`

  ```
en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN-COURS-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short; echo ---; git log --oneline -3", "description": "Check final git state"}`

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
7ee92dd9 JOURNAL — 2026-11-15 : E2, LES CAS D'ERREUR DU TAGGER (REFUS D'AUTHENTIFICATION → CODE 4, RÉSEAU ET RÉPONSE NON CONFORME → REPLI 0 ; 18/18)
840e613e TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES
7d4e3bc5 E1 — LA FAQ AU SOMMAIRE ET SES LIENS : 9/9 ANCRES, 5/5 LIENS, 0 MORT ; LA LIGNE FAQ DANS docs/README, LES RÉPONSES INCHANGÉES
  ```

- **bash** `{"command": "tail -8 /tmp/e2-portes.log; echo ---; wc -l /tmp/e2-portes.log", "description": "Check gate progress"}`

  ```
porte-diff-couche      ✅                          18 s    ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé
  porte-document         ✅                           5 s  ✅ porte document verte
  porte-echange-experts  ✅                          53 s    PORTE TENUE
  porte-episodique       ✅                         167 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          27 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                           8 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         215 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
---
29 /tmp/e2-portes.log
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C bash -C python3 | grep -E \"toutes-les-portes|porte-\" | head -10", "description": "Check current gate process"}`

  ```
3497177       27:32 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/toutes-les-portes.sh > /tmp/e2-portes.log 2>&1; echo "PORTES-CODE=$?" >> /tmp/e2-portes.log
3497202       27:32 bash tools/toutes-les-portes.sh
3725250       03:37 bash tools/porte-greffe.sh
3728566       00:44 bash tools/porte-greffe.sh
3729195       00:00 bash -c ps -o pid,etime,cmd -C bash -C python3 | grep -E "toutes-les-portes|porte-" | head -10
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_etat_a_jour.py 2>&1 | tail -6; echo \"ETAT-CODE=${PIPESTATUS[0]}\"", "description": "Verify state freshness"}`

  ```
état · dernier fait 840e613e · dernier état 840e613e
  ✅ aucun fait commité après le dernier état
ETAT-CODE=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py --aide | sed -n '1,20p'; echo \"AIDE-CODE=${PIPESTATUS[0]}\"", "description": "Check CLI help epilogue"}`

  ```
usage: drave [-h] [-V] {analyser,evaluer,rejouer,restituer} ...

Point d'entrée produit du bloc linguistique (analyse et restitution).

arguments:
  {analyser,evaluer,rejouer,restituer}
    analyser            étiqueter un texte (POS, syntagmes, pragmatique)
    evaluer             mesurer l'heuristique sur le gold
    rejouer             analyser deux fois et vérifier le déterminisme
    restituer           reconstruire la surface depuis l'annotation et mesurer le miroir

options:
  -h, --help, --aide    afficher cette aide et quitter
  -V, --version         afficher la version et quitter

Commandes : analyser, evaluer, rejouer, restituer.
Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) ·
4 clé/tagger indisponible (absente ou refusée) · 1 erreur.
Options : --json, --langue fr|en, --partition brut|alternative|filtrer_union|filtrer,
--contexte, --banc, --tagger.
AIDE-CODE=0
  ```

- **bash** `{"command": "tail -6 /tmp/e2-portes.log; echo ---; wc -l /tmp/e2-portes.log", "description": "Check gate progress"}`

  ```
porte-echange-experts  ✅                          53 s    PORTE TENUE
  porte-episodique       ✅                         167 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          27 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                           8 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         215 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
---
29 /tmp/e2-portes.log
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C bash | grep -E \"porte-greffe|toutes-les-portes\" | head", "description": "Check greffe gate duration"}`

  ```
3497177       27:44 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/toutes-les-portes.sh > /tmp/e2-portes.log 2>&1; echo "PORTES-CODE=$?" >> /tmp/e2-portes.log
3497202       27:44 bash tools/toutes-les-portes.sh
3725250       03:49 bash tools/porte-greffe.sh
3728566       00:57 bash tools/porte-greffe.sh
3729303       00:00 bash -c ps -o pid,etime,cmd -C bash | grep -E "porte-greffe|toutes-les-portes" | head
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test -f reports/rapport-tagger-erreurs.md && echo FICHE-OK; python3 tools/tests/test_tagger_api.py 2>&1 | tail -1", "description": "Run E2 acceptance checks"}`

  ```
FICHE-OK
OK
  ```

- **job_output** `{"job_id": "bash-71", "timeout_ms": 300000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -6 /tmp/e2-portes.log; echo ---; wc -l /tmp/e2-portes.log; ps -o pid,etime,cmd -C bash | grep -E \"porte-greffe|toutes-les-portes\" | head", "description": "Check gate progress"}`

  ```
porte-echange-experts  ✅                          53 s    PORTE TENUE
  porte-episodique       ✅                         167 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          27 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                           8 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         215 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
---
29 /tmp/e2-portes.log
3497177       32:55 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/toutes-les-portes.sh > /tmp/e2-portes.log 2>&1; echo "PORTES-CODE=$?" >> /tmp/e2-portes.log
3497202       32:55 bash tools/toutes-les-portes.sh
3725250       09:01 bash tools/porte-greffe.sh
3732310       00:12 bash tools/porte-greffe.sh
3732464       00:00 bash -c tail -6 /tmp/e2-portes.log; echo ---; wc -l /tmp/e2-portes.log; ps -o pid
… [68 caractères tronqués]
  ```

- **job_kill** `{"job_id": "bash-71", "reason": "Suite complète bloquée sur porte-greffe (hors périmètre, autre passe concurrente) ; porte-produit et contrôles ciblés verts."}`

  ```
requested cancellation of job bash-71
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C bash | grep -E \"3497177|3497202|tools/toutes-les-portes.sh\" | head; echo \"---\"; tail -3 /tmp/e2-portes.log", "description": "Confirm background gates stopped"}`

  ```
3732588       00:00 bash -c ps -o pid,etime,cmd -C bash | grep -E "3497177|3497202|tools/toutes-les-portes.sh" | head; echo "---"; tail -3 /tmp/e2-portes.log
---
  porte-flux             ✅                          27 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                           8 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         215 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD~1:docs/produit/README.md | grep -n \"En \\`--jsonl\\`\" -A2; echo ---; git show HEAD~1:reports/rapport-tagger-erreurs.md | grep -n \"\\-\\-jsonl\" | head; echo ---; git show HEAD~1:reports/rapport-tagger-erreurs.json |  … [73 caractères tronqués]`

  ```
436:**En `--jsonl`**, une clé refusée peut laisser sur `stdout` les lignes déjà écrites avant le
437-code **4** (le premier texte sans appel neuronal ne déclenche pas le 401) ; le message et le
438-code restent les mêmes. Le tableau ci-dessus décrit `analyser` sur **un** texte.
---
136:- **`--jsonl`** : le code 4 peut arriver après des lignes déjà écrites (le premier texte sans
---
153:  "en --jsonl, le code 4 peut arriver après des lignes déjà écrites (le premier texte sans appel neuronal ne déclenche pas 401) ; les mesures portent sur analyser avec un seul texte"
[stderr]
grep: warning: stray \ before -
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git ls-tree HEAD journal/2026-11-15/memoire.md; echo \"MEMOIRE-TREE-CODE=$?\"; git show --stat --oneline HEAD | sed -n '1,20p'; echo ---; git show --stat --oneline HEAD~1 | sed -n '1,12p'", "description": "Verify final tree and commi … [4 caractères tronqués]`

  ```
MEMOIRE-TREE-CODE=0
7ee92dd9 JOURNAL — 2026-11-15 : E2, LES CAS D'ERREUR DU TAGGER (REFUS D'AUTHENTIFICATION → CODE 4, RÉSEAU ET RÉPONSE NON CONFORME → REPLI 0 ; 18/18)
 journal/2026-11-15/README.md                       |  7 +-
 journal/2026-11-15/memoire.md                      | 24 ------
 journal/2026-11-15/mesures.md                      |  4 +-
 journal/README.md                                  |  4 +-
 journal/THEMES.md                                  |  1 -
 journal/sessions/MANIFEST.md                       |  4 +-
 .../digest.md                                      | 91 ++++++++++++++++++++++
 .../rapport.md                                     | 16 ++--
 8 files changed, 110 insertions(+), 41 deletions(-)
---
840e613e TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES
 docs/pilotage/en-cours.md                          |    6 +-
 docs/pilotage/roadmap.md                           |    4 +-
 docs/produit/README.md                             |   31 +-
 journal/2026-11-15/README.md                       |    9 +-
 journal/2026-11-15/distribue.md              
… [386 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD:journal/2026-11-15/README.md | sed -n '1,20p'; echo ---; git show HEAD:journal/2026-11-15/README.md | grep -n \"840e613e\\|07:04\"", "description": "Check final journal index"}`

  ```
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**20 commits** · **1 session(s)** · **5 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 4 | [distribue.md](distribue.md) |
| docs | 4 | [docs.md](docs.md) |
| mesures | 10 | [mesures.md](mesures.md) |
| outils | 1 | [outils.md](outils.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH
---
49:| 07:04 | `840e613e` | TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat HEAD~2..HEAD; echo ---; git status --short | wc -l; git status --short", "description": "Final diff and status"}`

  ```
docs/pilotage/en-cours.md                          |    6 +-
 docs/pilotage/roadmap.md                           |    4 +-
 docs/produit/README.md                             |   31 +-
 journal/2026-11-15/README.md                       |   10 +-
 journal/2026-11-15/distribue.md                    |    6 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/mesures.md                      |   17 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    7 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   34 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 2894 ++++++++++++++++++++
 .../rapport.md                                     |  165 ++
 .../digest.md                                      |  165 ++
 .../rapport.md                                     |   35 +-
 reports/INDEX.md                                   |    3 +-
 reports/rapport-tagger-erreurs.json                |  155 ++
 repor
… [979 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh 2>&1 | tail -4; echo \"PRODUIT-CODE=${PIPESTATUS[0]}\"", "description": "Post-commit product gate", "timeoutMs": 300000}`

  ```
✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
PRODUIT-CODE=0
  ```

- **todo_write** `{"todos": [{"content": "Implement explicit 401/403 key-refusal path in drave.py (code 4, clear message)", "status": "completed"}, {"content": "Add tests for missing key, invalid key, network cut, model refusal in test_tagger_api.py", "status": "completed"}, {"content": "Document real behavior in doc … [290 caractères tronqués]`

  ```
Updated todo list: 0 pending, 0 in progress, 5 completed.
  ```

### 🤖 Assistant

## E2 — les cas d'erreur de `--tagger`

### Comportement livré (mesuré, transport factice)

| cas | code | `stdout` | comportement |
|---|---:|---|---|
| **clé absente** | **4** | vide | message clair, rien n'est analysé |
| **clé invalide** (HTTP 401/403) | **4** | vide | **pas de repli** ; message clair nommant les trois sources de la clé |
| **réseau coupé** (3 essais du client) | **0** | annotation heuristique | **repli heuristique**, `refus` non vide, POS `source=heuristique` |
| **refus du modèle** (texte non JSON, JSON incomplet) | **0** | annotation heuristique | même repli, `refus` nomme le défaut |

**Le changement principal** : avant, une clé 401/403 était avalée par `NeuronalLLMPOS` et le CLI rendait **0** avec un repli heuristique muet. Désormais `_transport_tagger` retient le code dans `stats["cle_refusee"]`, `_CascadeTagger` lève `CleTaggerRefusee`, et `main` rend **4**.

### Fichiers

- [`tools/drave.py`](tools/drave.py) — `CleTaggerRefusee`, drapeau `cle_refusee`, code 4.
- [`tools/tests/test_tagger_api.py`](tools/tests/test_tagger_api.py) — **18/18 tests**, dont les 4 cas d'erreur + JSON incomplet.
- [`docs/produit/README.md`](docs/produit/README.md) § 3.7 — tableau des cas, règle des deux familles, nuance `--jsonl`.
- [`reports/rapport-tagger-erreurs.md`](reports/rapport-tagger-erreurs.md) + [`reports/rapport-tagger-erreurs.json`](reports/rapport-tagger-erreurs.json) — dispositif, mesures, contrôles.
- [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md), [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md), [`journal/2026-11-15/mesures.md`](journal/2026-11-15/mesures.md).

### Contrôles

- **Transport valide** → code 0, POS neuronaux : les cas d'erreur ne sont pas un « tout échoue ».
- **Mutation** : retirer le contrôle 401/403 fait échouer `test_cle_invalide_code_4` (`0 != 4`).
- **Fuite de clé** : la sentinelle `cle-de-test-sentinelle` n'apparaît ni dans `stdout` ni dans `stderr`.

### Portes

- `python3 tools/tests/test_tagger_api.py` → **OK** (18 tests).
- `bash tools/porte-produit.sh` → **verte** (183/183 autotests).
- `revue_documentation`, `porte-tableaux`, `taille_documents`, `verifie_journal`, `verifie_en_cours` → **verts**.
- La suite complète `toutes-les-portes.sh` a été arrêtée sur `porte-greffe` (hors périmètre, autre passe concurrente) après **29 portes toutes vertes** ; les portes liées au changement sont vertes.

### Commits

- `840e613e` — **TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES**
- `7ee92dd9` — journal du jour (E2).

