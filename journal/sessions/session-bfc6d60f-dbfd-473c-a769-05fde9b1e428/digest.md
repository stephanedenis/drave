# Session DSH — relecture

- identifiant : `session-bfc6d60f-dbfd-473c-a769-05fde9b1e428`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 11:05:10
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche W5 (J3 après-midi) : la restitution v3 — `_role_gp` distingue **lieu / temps / destinataire / possession / complément** (des prépositions : `à` + lieu/temps/destinataire, `de` + possession, `avec` + moyen...) ; mesure la **précision et le rappel par rôle** sur le gold v2 (46) et le gold S (61/144 existants), avec le **contrôle négatif** (permuter les rôles doit tuer la mesure). Fiche `reports/rapport-restitution-v3.md` + JSON, tests. Si les rôles ne se séparent pas, écris le négatif.

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

### 🤖 Assistant

Je commence par charger le contexte de la tâche et localiser l'existant.

- **bash** `{"command": "pwd && git status --short | head -50 && git log --oneline -15", "description": "Show repo status and recent commits"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
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
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
93e046f7 SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
be3f41ad SEMAINE 2 — W3 : LA MATRICE DU TAGGER (DÉFAUT HORS LIGNE CODE 0, CLÉ INVALIDE 4, RÉSEAU COUPÉ 0 APRÈS 3 ESSAIS, 1 000 PHRASES = 143 870 TOKENS) ; 4 TESTS DE PLUS
3439cb0c ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte
1683c2b4 W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
4dbeff45 SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAN
… [1249 caractères tronqués]
  ```

- **bash** `{"command": "ls -la && echo \"---reports---\" && ls reports/ 2>/dev/null | head -60", "description": "List root and reports directory"}`

  ```
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 06:29 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198 15 nov 11:05 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 78052 15 nov 10:57 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run
… [2145 caractères tronqués]
  ```

- **grep** `{"pattern": "_role_gp", "include": "*.py"}`

  ```
Found 8 matches

tools/bloc_linguistique.py
Line 538: def _role_gp(prep: str) -> str:
Line 1446:                 segments.append({"type": "GP", "role": _role_gp(t), "niveau": 1,

tools/structures/generateur.py
Line 246: def _role_gp(prep: str, segs: list["Segment"], utiles: list[Token], i: int) -> str:
Line 432:                                 "GP", _role_gp(_norm(t.texte), segs, utiles, i), 1))

tools/pensee/autotest.py
Line 2319:     """Le correctif des passifs : _role_gp rend agent, le generateur S court-circuite."""
Line 2320:     from tools.bloc_linguistique import _role_gp
Line 2321:     return _role_gp("par") == "agent" and _role_gp("avec") == "moyen", (
Line 2322:         f"par → {_role_gp('par')}, avec → {_role_gp('avec')}")
  ```

- **bash** `{"command": "sed -n '500,580p' tools/bloc_linguistique.py && echo \"=== generateur ===\" && sed -n '220,280p' tools/structures/generateur.py", "description": "Read _role_gp implementations"}`

  ```
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
                "ez", "ons", "iez", "ais", "ra", "rai", "ras", "rons", "rez", "ront",
                "s", "ed", "ing", "en"):
        if n.endswith(suf) and n[:-len(suf)] in VERBES_CONNUS:
            return True
    # participes en -é/-és/-ée : `accroché` → `accrocher`
    for suf in ("ées", "ée", "és", "é"):
        if n.endswith(suf) and (n[:-len(suf)] + "er") in VERBES_CONNUS:
            return True
    # 1er groupe : `nage` → `nager`, `commence` → `commencer` (la voyelle finale tombe)
    for suf in ("es", "ent", "e", "ait", "aient", "ais", "ons", "ez"):
        if n.endswith(suf):
            radical = 
… [4476 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -iE \"gold|restitution|s-paragraphe|46|144\" | head -60; echo \"---\"; find . -maxdepth 3 -iname \"*gold*\" -not -path \"./.git/*\" | head -60", "description": "Find gold and restitution files"}`

  ```
pensee-gold-200.json
pensee-gold-342.json
pensee-gold-anglais.json
pensee-gold-cascade-200.json
pensee-gold-cascade.json
pensee-gold-complexes100.json
pensee-gold-complexes20.json
pensee-gold-complexes50.json
pensee-gold-complexes.json
pensee-gold-discours.json
pensee-gold-gele.json
pensee-gold-gp-corrige.json
pensee-gold-linguistique.json
pensee-gold-neuronal.json
pensee-gold-pragmatique.json
pensee-gold-reel-cascade.json
pensee-gold-split.json
pensee-gold-subsets.json
pensee-gold-syntagmes.json
pensee-restitution-v0.json
pensee-restitution-v1.json
pensee-restitution-v2.json
rapport-gold-452.json
rapport-gold-452.md
rapport-gold-anglais.md
rapport-gold-gp-corrige.md
rapport-gold-reel-50.json
rapport-gold-reel-50.md
rapport-gold-split.md
rapport-pensee-gold-200.md
rapport-pensee-gold-200-subsets.md
rapport-pensee-gold-342.md
rapport-pensee-gold-api.md
rapport-pensee-gold-cascade.md
rapport-pensee-gold-complexes100.md
rapport-pensee-gold-complexes20.md
rapport-pensee-gold-complexes50.md
rapport-pensee-gold-complexes.md
rapport-pensee-gold-discours.md
rapport-pensee-gold-gele.md
rapport-pensee-gold-linguistique.md
rapport-pensee-gold-neuronal.md
rapport-pensee-gold-syntagmes.md
rappo
… [1856 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"restitution\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -40", "description": "Find restitution references in pilotage docs"}`

  ```
docs/pilotage/en-cours.md:89:- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** ([FAQ](../../reports/rapport-faq.md)), **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
docs/pilotage/en-cours.md:119:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, fermé −1,55 ; W3 : défaut hors ligne code 0, `--tagger` code 4 sans clé, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe** ; R2/R3 attendent N5/N4 | **J3 — restitution v3** (rôles) ; **Panini** si les 26 signatures arrivent ; **[fiche W3](../../reports/rapport-tagger-defaut.md)** |
docs/pilotage/en-cours.md:127:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold de pensée, **qualité des rôles** ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — migration `/` v7 (106/41) ; référents ; **J3 — restitution v3** (rôles) ; **Panini** si les 26 signatures arrivent ; **A
… [7060 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-restitution-v2.md; echo \"=== JSON keys ===\"; python3 -c \"\nimport json\nfor f in ['reports/pensee-restitution-v2.json','reports/pensee-restitution-v1.json','reports/pensee-restitution-v0.json']:\n    d=json.load(open(f))\n    print(f, type(d), list(d.keys())[:20]  … [104 caractères tronqués]`

  ```
# B13 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : D2 · **Date** : 2026-11-15 ·
> **Verdict** : ❌ **négatif sur la fidélité** — la forme est fidèle (46/46), la sémantique
> ne l'est pas : **19/46 cadres exacts** (dont **16 non vides**), **F1 0,5270**, **32 faux
> positifs** et **38 faux négatifs**.
>
> **La question.** Au-delà de la surface exacte (v0 : 46/46) et de la forme canonique
> (v1 : 46/46), peut-on **restitue les rôles** — agent, prédicat, lieu — dans une forme
> lisible et **mesurer leur fidélité** sur les **46 textes annotables** de la v0 ?
>
> **La réponse.** Les rôles **se restituent** comme **forme** : un cadre principal lisible,
> 198 segments de rôle, 198/198 spans dans la source, et un rendu qui se relit à l'identique
> (**46/46**). Mais leur **fidélité au texte** n'est pas acquise : sur un or écrit à la main,
> **19/46 cadres exacts** (0,4130), **16/46 non vides** (0,3478), **91/138 cellules de rôle
> exactes** (0,6594) — mais seulement **39 justes sur 77 attendus** et **71 prédits**, soit
> **précision 0,5493 · rappel 0,5065 · F1 0,5270**. Le contrôle « rôle constant par type »
> n
… [16681 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/pilotage/; echo ---; grep -rln \"W5\\|SEMAINE 2\" docs/pilotage/*.md | head; echo ---; grep -rn \"gold v2\\|gold S\\|61/144\\|144\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -20", "description": "Find week plan and gold references"}`

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
---
docs/pilotage/en-cours.md:49:- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
docs/pilotage/en-cours.md:87:- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
docs/pilotage/roadmap.md:34:| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 acceptés, 8 exclus) **committés `389b99f`** ; le fait divers tranché (la tête du GN arrête le verbe) ; [fiche](../../repo
… [734 caractères tronqués]
  ```

- **bash** `{"command": "git status --short && git diff --stat && git diff docs/pilotage/roadmap.md | head -80", "description": "Inspect working tree changes"}`

  ```
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
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
 docs/pilotage/roadmap.md                |   2 +-
 docs/produit/README.md                  |  25 +-
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
 12 files changed, 591 insertions(+), 345 deletions(-)
diff --git a/docs/pilotage/roadmap.md b/doc
… [9751 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/pilotage/semaine-2.md", "description": "Read week 2 plan"}`

  ```
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
> [D3](../../reports/rapport-faq.md), [E1](../../reports/rapport-faq-sommaire.md),
> [E2](../../reports/rapport-tagger-erreurs.md). Le plan ne promet aucun chiffre : il nomme la
> mesure, son **contrôle
… [10691 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='tools/structures/donnees/gold-analyseur.json'\nd=json.load(open(p))\nprint(type(d), list(d.keys())[:20] if isinstance(d,dict) else len(d))\nprint(json.dumps(d if not isinstance(d,dict) else {k:(v[:2] if isinstance(v,list) else v) for k,v in d.items()}, … [78 caractères tronqués]`

  ```
<class 'dict'> ['version', 'note', 'segments', 'phrases']
{"version": 1, "note": "Gold de l'analyseur. split=dev : les 7 phrases du banc. split=test : 16 phrases écrites AVANT les règles. split=holdout : 32 phrases en quatre vagues — h024-h031 (première règle, h024 a révélé « est mon voisin », corrigé par la copule), h032-h039 (après la copule), h040-h047 (après la frontière GN-devant-verbe) et h048-h055 (après la règle de contexte des homographes, 02/11 20 h). h033, h046 et h047, qui avaient révélé les défauts, sont corrigés ; les vagues 2 et 3 ne sont donc plus aveugles à ces règles, et la vague 4 est écrite après la règle de contexte, mesurée une fois. Deux échecs de la vague 4 sont nommés : h050 (« fait » suivi d'un verbe hors lexique) et h053 (« lit » après un adjectif, en fin de phrase). Aucun attendu n'a été modifié après mesure. Cinquième vague h056-h060, écrite APRÈS les règles v6 (h050, h053, « si fort que ») et mesurée une fois : elle teste la conséquence, l'hypothèse conditionnelle, le nom après adjectif et le verbe « fait » après un nom. Sixième vague h061 : le nom après un adjectif hors lexique (« fait divers »), ajouté après la règle v7 et mesuré une fois.", "segment
… [492 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='tools/tests/linguistique/gold_restitution_v2.json'\nd=json.load(open(p))\nprint(type(d), list(d.keys())[:20] if isinstance(d,dict) else len(d))\ns=json.dumps(d,ensure_ascii=False)\nprint(s[:3000])\nEOF", "description": "Inspect gold v2 structure"}`

  ```
<class 'dict'> ['schema', 'version', 'date', 'ligne', 'tache', 'note', 'textes']
{"schema": "drave.restitution.v2.gold", "version": 1, "date": "2026-11-15", "ligne": "B13", "tache": "D2", "note": "Or **écrit à la main** sur les 46 textes annotables du banc v0 : le **cadre principal** (agent, prédicat, lieu), valeurs en surface et variantes pour les ambiguïtés réelles (coordination, contraction, inversion). Ce n'est pas une annotation complète : les propositions subordonnées et les seconds cadres ne sont pas notés. Les textes sans prédicat (numérique, courriel, symboles, remplissage latin) ont un cadre vide.", "textes": [{"id": "f01", "texte": "Le chat dort.", "langue": "fr", "variantes": [{"agent": "Le chat", "predicat": "dort", "lieu": ""}]}, {"id": "f02", "texte": "Le chat de la voisine qui dort sur le toit se réveille.", "langue": "fr", "variantes": [{"agent": "Le chat de la voisine", "predicat": "se réveille", "lieu": ""}, {"agent": "Le chat", "predicat": "se réveille", "lieu": ""}]}, {"id": "f03", "texte": "Bonjour ! Comment allez-vous aujourd'hui ?", "langue": "fr", "variantes": [{"agent": "vous", "predicat": "allez", "lieu": ""}, {"agent": "vous", "predicat": "allez-vous", "
… [1880 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nd=json.load(open('tools/structures/donnees/gold-analyseur.json'))\nph=d['phrases']\nprint('phrases',len(ph))\nroles=collections.Counter(); types=collections.Counter(); byrole=collections.defaultdict(list)\nfor p in ph:\n    for seg,t,role in  … [397 caractères tronqués]`

  ```
phrases 61
roles Counter({'predicat': 58, 'agent': 34, 'temps': 9, 'qualite': 7, 'patient': 5, 'destinataire': 5, 'contenu': 5, 'theme': 4, 'cause': 4, 'lieu': 3, 'but': 3, 'hypothese': 2, 'possession': 1, 'instrument': 1, 'concession': 1, 'maniere': 1, 'consequence': 1})
types Counter({'GV': 58, 'GN': 36, 'GP': 23, 'SUB': 20, 'REL': 7})

## lieu 3
   ('p003', 'dans le parc', 'GP', "La femme a vu l'homme dans le parc.")
   ('g010', 'à la maison', 'GP', 'Quand il pleut, je reste à la maison.')
   ('h041', 'sur le canapé', 'GP', 'Le chat dort sur le canapé.')

## temps 9
   ('p006', 'hier', 'GP', "Elle a dit qu'elle viendrait hier.")
   ('g010', 'Quand il pleut', 'SUB', 'Quand il pleut, je reste à la maison.')
   ('g014', "dès qu'il arrivera", 'SUB', "Nous partirons dès qu'il arrivera.")
   ('g020', 'demain', 'GP', "Je crois qu'il viendra demain.")
   ('h024', 'hier', 'GP', "L'homme que tu as vu hier est mon voisin.")
   ('h025', 'quand il fera beau', 'SUB', "Je sais qu'elle partira quand il fera beau.")
   ('h026', "Pendant qu'il dormait", 'SUB', "Pendant qu'il dormait, elle lisait.")
   ('h035', 'Quand elle chante', 'SUB', 'Quand elle chante, il danse.')
   ('h042', 'demain', 'GP',
… [869 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/restitution_v2.py; echo \"...\"; grep -n \"def \\|gold\\|role\" tools/restitution_v2.py | head -60", "description": "Read restitution v2 module"}`

  ```
"""restitution_v2.py — la restitution v2 : les rôles (agent, prédicat, lieu).

La v0 restitue la **surface** (graphème → texte) ; la v1 restitue la **forme canonique**
(segments + rôles + cibles). La v2 ajoute une lecture **lisible des rôles** : un cadre
principal `agent / prédicat / lieu`, les cadres de chaque prédicat, et les segments de rôle.

La fidélité des rôles ne se mesure pas contre l'annotation qui les produit (ce serait une
tautologie) : elle se mesure contre un **or de rôles écrit à la main** sur les 46 textes
annotables du banc v0 (`tools/tests/linguistique/gold_restitution_v2.json`). L'or ne porte
que le **cadre principal** et quelques variantes d'ambiguïté ; il ne prétend pas annoter
toutes les propositions.

Deux mesures sont séparées :

- la **restitution** du rôle (le rôle est-il lisible et relu à l'identique ?) — un codec ;
- la **fidélité** du rôle (le rôle est-il celui de l'or ?) — une exactitude sémantique.

Le contrôle négatif retire ou permute les rôles du rendu : le lecteur doit le voir. Le
contrôle « cadre vide » et le contrôle « rôle constant par type » donnent les planchers.

    python3 tools/mesurer_restitution_v2.py
    python3 tools/drave.py restitue
… [8608 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '280,340p' tools/structures/generateur.py; echo \"=== full role_gp ===\"; sed -n '235,290p' tools/structures/generateur.py", "description": "Read rest of generator _role_gp"}`

  ```
if prep in {"pendant", "depuis", "durant", "avant", "apres"}:
        return "temps"
    if prep == "malgre":
        return "concession"
    if prep == "selon":
        return "source"
    if prep == "sans":
        return "maniere"
    if prep == "en":
        return "lieu"
    return "complement"


class Segment:
    __slots__ = ("debut", "fin", "type", "role", "niveau", "texte", "cible_nom", "cible_gp",
                 "cible_verbe", "parent", "profondeur")

    def __init__(self, debut, fin, texte, typ, role, niveau=0):
        self.debut, self.fin, self.texte = debut, fin, texte
        self.type, self.role, self.niveau = typ, role, niveau
        self.cible_nom = None   # le GN le plus proche à gauche
        self.cible_gp = None    # la tête du GP le plus proche à gauche
        self.cible_verbe = None  # le GV le plus proche à gauche
        self.parent = None      # l'index du segment père dans la liste
        self.profondeur = 0     # la profondeur dans l'arbre (le GV racine = 0)

    def dict(self):
        return {"debut": self.debut, "fin": self.fin, "texte": self.texte,
                "type": self.type, "role": self.role, "niveau": self.niveau,
                "pa
… [3222 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '160,430p' tools/restitution_v2.py", "description": "Read rest of restitution_v2.py"}`

  ```
def cadres(a: bl.Annotation) -> list[dict]:
    """Les cadres (agent, prédicat, lieu), un par prédicat, dans l'ordre de la surface.

    Les prédicats qui commencent au même point sont fusionnés au **plus large** : dans
    `Il n'y a`, `n'y` et `n'y a` sont deux étiquettes du même prédicat ; garder la plus
    large évite de lire un prédicat tronqué. Les autres chevauchements restent des cadres
    distincts (la v1 les documente déjà).
    """
    segments = _segments_syntagmes(a)
    predicats: list[dict] = []
    for e in segments:
        if e["role_normalise"] != "predicat":
            continue
        # même début : garder le plus large (le prédicat complet).
        if predicats and predicats[-1]["debut"] == e["debut"]:
            if e["fin"] > predicats[-1]["fin"]:
                predicats[-1] = e
            continue
        predicats.append(e)
    if not predicats:
        return []
    agents = [e for e in segments if e["role_normalise"] == "agent"]
    lieux = [e for e in segments if e["role_normalise"] == "lieu"]
    groupes = [e for e in segments if e["type"] == "GN"
               and e["role_normalise"] in ("", "groupe nominal")]
    return [_cadre_de(p, agents, l
… [10047 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/mesurer_restitution_v2.py", "description": "Read v2 measurement script"}`

  ```
#!/usr/bin/env python3
"""mesurer_restitution_v2.py — produit le JSON de la fiche D2.

Mesure la **restitution v2** — les rôles (agent, prédicat, lieu) — sur les **46 textes
annotables** du banc v0 (`reports/pensee-fiabilite-produit.json`) et compare le cadre
principal à l'**or écrit à la main** (`tools/tests/linguistique/gold_restitution_v2.json`).
Écrit `reports/pensee-restitution-v2.json`. La fiche `reports/rapport-restitution-v2.md`
cite ce JSON.

    python3 tools/mesurer_restitution_v2.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import tools.restitution as restitution  # noqa: E402
import tools.restitution_v2 as v2  # noqa: E402

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
GOLD = v2.GOLD_DEFAUT
SORTIE = RACINE / "reports" / "pensee-restitution-v2.json"

LIMITES = [
    "L'or ne note que le **cadre principal** (agent, prédicat, lieu) : 46 textes, 46 cadres, "
    "65 variantes. Il ne note ni les subordonnées, ni les seconds cadres, ni les rôles "
    "patient / destinata
… [4204 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1400,1470p' tools/bloc_linguistique.py; echo ====; grep -n \"_role_gp\" -n tools/bloc_linguistique.py tools/structures/generateur.py tools/pensee/autotest.py", "description": "Inspect GP role call site in bloc_linguistique"}`

  ```
or _normaliser(mots[i + 1][2]) in lex.get("AUX", set())
                         or _normaliser(mots[i + 1][2]) in {"ne", "n'", "n’"})):
                segments.append({"type": "GN", "role": "agent", "niveau": 0,
                                 "debut": d, "fin": f, "texte": texte[d:f], "candidats": []})
                i += 1
                continue
            if typ == "mot" and (n in lex.get("AUX", set()) or est_verbe(d, t)
                                 or (i + 1 < len(mots) and _normaliser(mots[i + 1][2]) in lex.get("AUX", set()))):
                j = i + 1
                # le GV s'arrête à la préposition, au déterminant, au relatif : un prédicat
                # par clause (« joue | au ballon », « saw | the cat »).
                while (j < len(mots) and mots[j][3] == "mot"
                       and _normaliser(mots[j][2]) not in lex.get("PREP", set())
                       and _normaliser(mots[j][2]) not in lex.get("DET", set())
                       and _normaliser(mots[j][2]) not in RELATIFS
                       and _normaliser(mots[j][2]) not in SUBORDONNANTS
                       # l'adverbe **final** de la phrase n'est pas dans le GV
                    
… [4228 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '430,760p' tools/restitution_v2.py", "description": "Read v2 metrics and gold S matcher"}`

  ```
"melange": (comparer_cadre(melanger_roles(principal), variantes)
                    if variantes else None),
        "rendu": {"exact": rendu_juste, "relu": relu,
                  "principal": principal, "definition": "relire_roles(rendre_roles(a))"},
        "controle_negatif_rendu": controler_negatif_rendu(rendu),
        "spans_dans_source": _dans_source(a, source),
    }


def _moyenne(valeurs: list[float]) -> float:
    return round(sum(valeurs) / max(1, len(valeurs)), 4)


def _taux(a: int, b: int) -> float:
    return round(a / b, 4) if b else 0.0


def _agreger_comparaisons(comparaisons: list[dict]) -> dict:
    par_role = {
        role: {"exacts": 0, "attendus": 0, "predits": 0,
               "justes": 0, "faux_positifs": 0, "faux_negatifs": 0,
               "vrais_negatifs": 0}
        for role in ROLES
    }
    for c in comparaisons:
        for role in ROLES:
            x = c["par_role"][role]
            p = par_role[role]
            p["exacts"] += int(x["egal"])
            p["attendus"] += int(bool(x["attendu"]))
            p["predits"] += int(bool(x["predit"]))
            p["justes"] += int(x["juste"])
            p["faux_positifs"] += int(x["faux_positif"
… [13919 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/tests/test_restitution_v2.py", "description": "Read v2 tests"}`

  ```
#!/usr/bin/env python3
"""test_restitution_v2.py — la restitution v2 (D2) : les rôles agent / prédicat / lieu.

Ce que le test fige :
- `drave restituer TEXTE --roles` rend un cadre principal lisible et un JSON v2 ;
- `relire_roles(rendre_roles(a))` redonne le cadre principal (codec) ;
- le contrôle négatif retire/permute un rôle et le lecteur le voit ;
- sur les **46 textes** de la v0, le cadre principal est exact **19/46** et **16/46**
  non vides ; les rôles exacts sont **91/138**, avec **32 faux positifs** et **38 faux
  négatifs** — la fidélité n'est donc pas acquise ;
- l'or externe (gold S, 61 phrases) donne **139/144** : le lecteur n'est pas cassé quand
  l'or est propre ; l'écart mesure la difficulté du banc v0, pas un bug de format.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

import tools.bloc_linguistique as bl  # noqa: E402
import tools.restitution as restitution  # noqa: E402
import tools.restitution_v2 as v2  # noqa: E402

CLI = RACINE / "tools" / "drave.py"
BANC = RACINE / "reports" / "pensee-fiabilite-produit.json
… [9346 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"mesurer_gold_analyseur\\|gold_analyseur\\|gold-analyseur\" tools/*.py tools/tests/*.py | head -30", "description": "Find gold S usage"}`

  ```
tools/mesurer_restitution_v2.py:66:    externe = v2.mesurer_gold_analyseur()
tools/restitution_v2.py:744:GOLD_ANALYSEUR = RACINE / "tools" / "structures" / "donnees" / "gold-analyseur.json"
tools/restitution_v2.py:759:def mesurer_gold_analyseur(chemin: pathlib.Path | None = None) -> dict:
tools/tests/test_restitution_v2.py:216:    def test_gold_analyseur(self):
tools/tests/test_restitution_v2.py:217:        r = v2.mesurer_gold_analyseur()
  ```

- **bash** `{"command": "sed -n '744,900p' tools/restitution_v2.py", "description": "Read gold S matcher implementation"}`

  ```
GOLD_ANALYSEUR = RACINE / "tools" / "structures" / "donnees" / "gold-analyseur.json"


def _spans_gold(phrase: dict) -> list[dict]:
    curseur, spans = 0, []
    for texte, type_, role in phrase.get("attendus", []):
        debut = phrase["texte"].find(texte, curseur)
        if debut < 0:
            raise ValueError(f"{phrase.get('id')} : segment introuvable {texte!r}")
        spans.append({"debut": debut, "fin": debut + len(texte), "texte": texte,
                      "type": type_, "role": role})
        curseur = debut + len(texte)
    return spans


def mesurer_gold_analyseur(chemin: pathlib.Path | None = None) -> dict:
    """Le **contrôle externe** : le lecteur de rôles v2 sur le gold S de 61 phrases.

    Ce n'est pas le banc v0 : c'est un gold de rôles **écrit avant** la v2 (le gold de
    l'analyseur S, 144 rôles). Il sert à montrer que la lecture des rôles n'est pas cassée
    quand l'or est propre ; l'écart avec les 46 textes v0 mesure la difficulté du banc,
    pas la qualité du code.
    """
    chemin = chemin or GOLD_ANALYSEUR
    donnees = json.loads(chemin.read_text(encoding="utf-8"))
    h = bl.Heuristique()
    justes = total = base_justes = 0
    par_type =
… [1652 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -- tools/tests/test_restitution_v2.py tools/restitution_v2.py tools/bloc_linguistique.py | head -30", "description": "History of v2 and role code"}`

  ```
5b2d07fc D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270)
b6e474dc J6.2 — s065 : LA REL SUIVIE D'UN GV PREND LE SUJET DU GV (238/238 LABELS, 238/239 CIBLES, F1 0,7902 INCHANGÉ, 0 SPAN, 0 POS)
8eb0cc49 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE
9a259953 B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE
92652984 B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183
25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
efbae885 B13 — LE NOM PROPRE SUJET EST UN GN : F1 0,7438 → 0,7535, TÊTE 0,865, ATTACHEMENT 236/237 ; 183/183
295e0d7b B13 — LES PRONOMS SUJETS ANGLAIS AUSSI : F1 0,7013 → 0,7438, TÊTE 0,8561, ATTACHEMENT PRÉSERVÉ ; 183/183
c78a53bd B13 — LE PRONOM SUJET EST UN GN : F1 0,6519 → 0,7013 (+4,9), TÊTE 0,7709 → 0,8141, ATTACHEMENT PRÉSERVÉ (236/237, 0,9916) ; 183/183
5d2fa775 B13 — r264 RÉGLÉ : LE GV S'ARRÊTE AU MARQUEUR ÉLIDÉ (RADICAL qu), EXACT 236/237, COUVERTURE 0,9874 → 0,9916, 
… [2616 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"roles_v3\\|restitution_v3\\|gold_restitution_v3\\|restituer --roles\" tools docs reports | head -40", "description": "Check for existing v3 work"}`

  ```
docs/produit/README.md:495:**1 bis. La restitution v2 lit les rôles, pas leur justesse.** `restituer --roles` rend un
reports/rapport-restitution-v2.md:30:> (`restituer --roles`), [`mesurer_restitution_v2.py`](../tools/mesurer_restitution_v2.py) ;
reports/rapport-restitution-v2.md:320:- [`drave.py`](../tools/drave.py) — `restituer --roles`, `--gold`, JSON v2.
  ```

- **bash** `{"command": "ls work/ | head -40; find work -maxdepth 2 -iname \"*w5*\" -o -iname \"*restitution*\" | head -30", "description": "Look for prior work artifacts"}`

  ```
atomes_cohortes.py
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
j71
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
  ```

- **bash** `{"command": "sed -n '1290,1460p' tools/bloc_linguistique.py", "description": "Read heuristic analyzer token loop"}`

  ```
_n_elic_e = (_n_elic + "e") if _n_elic.endswith("qu") else _n_elic
            if typ == "mot" and (n in RELATIFS or _n_elic in RELATIFS
                                 or _n_elic_e in RELATIFS or _n_elic_e in SUBORDONNANTS
                                 or est_sub(n) or est_sub(_n_elic_e)):
                suivant = mots[i + 1] if i + 1 < len(mots) else None
                # « since/before/after/until/as » : SUB devant une clause, PRÉP devant un GN
                prep_ambigue = (n in AMBIGUES_PREP and (suivant is None
                                or not (_normaliser(suivant[2]) in lex.get("PRON", set())
                                        or est_verbe(suivant[0], suivant[2]))))
                ambigu = n in lex.get("DET", set())
                marqueur = (not prep_ambigue) and ((not ambigu) or (suivant is not None and (
                    _normaliser(suivant[2]) in lex.get("PRON", set())
                    or _normaliser(suivant[2]) in lex.get("AUX", set())
                    or est_verbe(suivant[0], suivant[2]))))
                if marqueur:
                    precedent = segments[-1]["type"] if segments else None
                    # R2 : un **subordonnant** o
… [9710 caractères tronqués]
  ```

- **bash** `{"command": "git diff tools/drave.py | head -120", "description": "Inspect uncommitted drave.py change"}`

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
… [875 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"restituer\\|roles\\|canonique\" tools/drave.py | head -60", "description": "Find restituter CLI code"}`

  ```
13:    python3 tools/drave.py restituer "Le chat dort."
14:    python3 tools/drave.py restituer "Le chat dort." --roles
15:    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
84:def _canonique(a: bl.Annotation) -> str:
329:        roles = [str(e.meta.get("role") or "—") for e in syntagmes]
335:        lr = max(len(r) for r in roles)
337:        for e, valeur, role, cible, span in zip(syntagmes, valeurs, roles, cibles, spans):
708:    canonique_1 = _canonique(premiere)
709:    canonique_2 = _canonique(seconde)
710:    identique = canonique_1 == canonique_2
711:    empreinte = hashlib.sha256(canonique_1.encode("utf-8")).hexdigest()[:16]
716:    print(f"  JSON       : {len(canonique_1.encode('utf-8'))} octets "
719:        print("  divergence : les deux analyses ne rendent pas le même JSON canonique",
728:def cmd_restituer(args: argparse.Namespace) -> int:
733:    laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`
734:    ajoute la **forme canonique v1** (segments + rôles + cibles) et son miroir ;
735:    `--roles` ajoute la **v2** (agent, prédicat, lieu) et, sur un banc, sa fidélité à
738:    if args.roles and args.cano
… [2535 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '470,530p' docs/produit/README.md", "description": "Read product README on v2 limitation"}`

  ```
(la ligne `TAGGER API DEEPSEEK` sur 20 phrases, exemple réel) :

```
TAGGER API DEEPSEEK (option --tagger)
  POS         exactitude 97.14 % (fermé 94.74 %, ouvert 100.00 %) · Δ +8.57 pts vs heuristique
  SYNTAGMES   F1 90.16 % (tête 97.39 %) — conservés à l'heuristique
  COÛT        appels 20 · réseau 0 · cache 20 · tokens 0 · modèle deepseek-chat
  modèle renvoyé : deepseek-flash
```

**Le défaut ne bouge pas.** Sans `--tagger`, la commande ne lit aucune clé, n'importe pas le
module réseau, n'ouvre aucune socket, sort **code 0** et rend exactement l'heuristique d'avant
(le test [`test_tagger_api.py`](../../tools/tests/test_tagger_api.py) le compare octet pour
octet ; le test W3 piège `socket.socket` et vérifie que `tools.llm.deepseek` n'est pas importé).
Le `--tagger` est une **option**, pas un changement de produit : c'est la seule porte qui peut
sortir **4** (clé absente ou refusée).

## 4. Ce que le produit ne fait pas encore

**1. Il ne génère pas de texte.** `restituer` reconstruit la **surface** depuis l'annotation
(codec), mais il n'y a **pas de génération** : pas de traduction, pas de réponse libre, pas de
paraphrase. Le produit rend des **étiquettes** et, avec `restituer`
… [2814 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution_v2 as v2\nd=json.load(open('tools/structures/donnees/gold-analyseur.json'))\nh=bl.Heuristique()\nfor p in d['phrases']:\n    a=h.analyser(p['texte'])\n    segs=v2. … [760 caractères tronqués]`

  ```
OK p001  GP possession   | pred possession   | 'de la voisine' -> 'de la voisine'
   p002  GP instrument   | pred attribut     | 'avec le télescope' -> 'avec le télescope'
OK p003  GP lieu         | pred lieu         | 'dans le parc' -> 'dans le parc'
OK p004  GP but          | pred but          | 'pour attraper le bus' -> 'pour attraper le bus'
OK p005  GP destinataire | pred destinataire | 'à Marie' -> 'à Marie'
   p005  GP theme        | pred destinataire | 'de son projet' -> 'à Marie de son projet'
OK p006  SUB contenu      | pred contenu      | "qu'elle viendrait" -> "qu'elle viendrait"
OK p006  GP temps        | pred temps        | 'hier' -> 'hier'
OK p007  GP but          | pred but          | 'à manger' -> 'à manger'
OK g009  SUB contenu      | pred contenu      | 'que le chat dort' -> 'que le chat dort'
OK g010  SUB temps        | pred temps        | 'Quand il pleut' -> 'Quand il pleut'
OK g010  GP lieu         | pred lieu         | 'à la maison' -> 'à la maison'
OK g011  SUB cause        | pred cause        | "parce qu'elle est fatiguée" -> "parce qu'elle est fatiguée"
OK g012  SUB concession   | pred concession   | "Bien qu'il soit tard" -> "Bien qu'il soit tard"
OK g013
… [2407 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, sys\nsys.path.insert(0,'.')\nimport tools.restitution as r, tools.restitution_v2 as v2\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nm=v2.mesurer_banc_v2(r.items_ … [572 caractères tronqués]`

  ```
{
 "agent": {
  "exacts": 29,
  "attendus": 32,
  "predits": 28,
  "justes": 18,
  "faux_positifs": 10,
  "faux_negatifs": 14,
  "vrais_negatifs": 11,
  "taux_exact": 0.6304,
  "precision": 0.6429,
  "rappel": 0.5625,
  "f1": 0.6
 },
 "predicat": {
  "exacts": 22,
  "attendus": 39,
  "predits": 39,
  "justes": 19,
  "faux_positifs": 20,
  "faux_negatifs": 20,
  "vrais_negatifs": 3,
  "taux_exact": 0.4783,
  "precision": 0.4872,
  "rappel": 0.4872,
  "f1": 0.4872
 },
 "lieu": {
  "exacts": 40,
  "attendus": 6,
  "predits": 4,
  "justes": 2,
  "faux_positifs": 2,
  "faux_negatifs": 4,
  "vrais_negatifs": 38,
  "taux_exact": 0.8696,
  "precision": 0.5,
  "rappel": 0.3333,
  "f1": 0.4
 }
}
f07 lieu pred= 'on the roof' att= 'on the roof' egal True
    GP on the roof role= lieu
f08 lieu pred= '' att= 'Where' egal False
f20 lieu pred= 'vers 9 h' att= '' egal False
    GP vers role= lieu
    GP vers 9 h role= lieu
f24 lieu pred= '' att= 'au bord de la forêt' egal False
f35 lieu pred= '' att= 'over the lazy dog' egal False
f46 lieu pred= 'dans le réfrigérateur' att= 'dans le réfrigérateur' egal True
    GP dans le réfrigérateur role= lieu
f49 lieu pred= '' att= 'salle B12' egal False
f50 li
… [412 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"possession\\|attribut\\|destinataire\\|def _role\" tools/bloc_linguistique.py | head -40", "description": "Find role assignment in bloc_linguistique"}`

  ```
538:def _role_gp(prep: str) -> str:
554:        return "destinataire"
1340:                                predicat_vu = True   # « is red » : copule + attribut
1574:        # ADJECTIF attribut (« the car is fast ») — mesuré +0,41 dev / +0,31 test, 0 cassé.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nh=bl.Heuristique()\nfor txt in [\"Le chat de la voisine qui dort sur le toit se réveille.\",\"J'ai vu l'homme avec le télescope.\",\"Il a parlé à Marie de son projet.\",\"Le chat fait des bonds. … [251 caractères tronqués]`

  ```
Le chat de la voisine qui dort sur le toit se réveille.
  GN  agent          'Le chat'
  GP  possession     'de la voisine'
  REL qualite        'qui dort sur le toit'
  REL qualité        'qui dort sur le toit se réveille'
  GV  predicat       'se réveille'

 J'ai vu l'homme avec le télescope.
  GN  agent          "J'ai"
  GV  predicat       'vu'
  GV  prédicat       "vu l'homme"
  GN  patient        "l'homme"
  GP  attribut       'avec le télescope'

 Il a parlé à Marie de son projet.
  GN  agent          'Il'
  GV  predicat       'a parlé'
  GP  destinataire   'à Marie'
  GP  destinataire   'à Marie de son projet'
  GP  theme          'de son projet'

 Le chat fait des bonds.
  GN  agent          'Le chat'
  GV  predicat       'fait'
  GP  possession     'des bonds'
  ```

- **bash** `{"command": "grep -rn \"possession\\|attribut\" tools/*.py tools/**/*.py | head -40", "description": "Find role post-processing"}`

  ```
tools/bloc_code.py:17:     pas d'attribut, pas, itérations et profondeur bornés) rend la valeur exacte ;
tools/bloc_code.py:347:    """Exécute un extrait en SABLE : liste blanche de nœuds, pas d'import, pas d'attribut.
tools/bloc_code.py:518:            raise Refus("attribut interdit", noeud.lineno, ast.unparse(noeud))
tools/bloc_code.py:801:        "attribut": lambda: execute("obj.methode()"),
tools/bloc_linguistique.py:1340:                                predicat_vu = True   # « is red » : copule + attribut
tools/bloc_linguistique.py:1574:        # ADJECTIF attribut (« the car is fast ») — mesuré +0,41 dev / +0,31 test, 0 cassé.
tools/census_routage.py:60:            # lève « 'tuple' object has no attribute 'detach' ».
tools/corpus_wikipedia.py:164:        "licence": "Wikipédia : CC-BY-SA 4.0 (et GFDL) — attribution et partage à l'identique ; corpus local, non diffusé",
tools/corpus_wikipedia_texte.py:223:        "licence": "Wikipédia : CC-BY-SA 4.0 (et GFDL) — attribution et partage à l'identique ; corpus local",
tools/vision_hf_ref.py:109:        # les deux sont acceptés (et l'erreur « no attribute float » a coûté un essai).
tools/cerveau/predictif.py:58:    `pas` peut être un
… [1397 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"_role_gp\\|role.*GP\\|GP.*role\\|reclass\\|corrig\" tools/bloc_linguistique.py | head -60", "description": "Find GP role refinement"}`

  ```
538:def _role_gp(prep: str) -> str:
1446:                segments.append({"type": "GP", "role": _role_gp(t), "niveau": 1,
  ```

- **bash** `{"command": "sed -n '1460,1740p' tools/bloc_linguistique.py", "description": "Read analyzer post-processing"}`

  ```
return Annotation(texte=str(texte)[:200], refus="non_texte", source=self.nom,
                              trace=[{"etape": "refus", "raison": "non_texte",
                                      "type": type(texte).__name__}],
                              cout={"octets": 0, "duree_s": round(time.perf_counter() - t0, 6)})
        texte = texte or ""
        trace: list[dict] = []
        if not texte.strip() or not any(ch.isalpha() or ch.isdigit() for ch in texte):
            return Annotation(texte=texte, refus="vide", source=self.nom,
                              trace=[{"etape": "refus", "raison": "vide"}],
                              cout={"octets": len(texte.encode("utf-8", "replace")), "duree_s": round(time.perf_counter() - t0, 6)})

        lg, conf_lg, script = self._langue(texte, langue)
        trace.append({"etape": "langue", "langue": lg, "script": script, "confiance": conf_lg,
                      "indice": langue or ""})
        etiquettes: list[Etiquette] = []
        unites: list[Span] = []

        # 1. graphème — des plages de classes, pas un caractère par étiquette.
        # `C` couvre les **contrôles** (saut de ligne, tabulation, BOM, marques de format) :

… [17159 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/structures/construire_donnees.py; echo ====; sed -n '490,520p' tools/structures/generateur.py", "description": "Read S data builder and attachment role refinement"}`

  ```
#!/usr/bin/env python3
"""construire_donnees.py — fabrique donnees/phrases.json en calculant les spans par sous-chaîne.

Écrire les spans à la main est une source d'erreurs ; ici, chaque segment est donné par son
**texte exact**, et l'outil vérifie qu'il apparaît bien, dans l'ordre, dans la phrase.
"""
import json, pathlib

PHRASES = [
    ("p001", "Le chat de la voisine qui dort sur le toit se réveille.",
     [("Le chat", "GN", "agent", 0), (" de la voisine", "GP", "possession", 0),
      (" qui dort sur le toit", "REL", "qualite", 1), (" se réveille", "GV", "predicat", 0)],
     "« qui dort » sur le chat",
     "C'est le chat qui dort ; il est à la voisine ; il est sur le toit.",
     (" qui dort sur le toit", "Le chat", "relative")),
    ("p001", "Le chat de la voisine qui dort sur le toit se réveille.",
     [("Le chat", "GN", "agent", 0), (" de la voisine", "GP", "possession", 0),
      (" qui dort sur le toit", "REL", "qualite", 2), (" se réveille", "GV", "predicat", 0)],
     "« qui dort » sur la voisine",
     "C'est la voisine qui dort ; le chat est à elle ; il est sur le toit.",
     (" qui dort sur le toit", " de la voisine", "relative")),
    ("p002", "J'ai vu l'homme 
… [6022 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _syntagmes_s\\|def _syntagmes_simple\\|def _sujet_hors_gv\" tools/bloc_linguistique.py", "description": "Find S call methods"}`

  ```
911:    def _sujet_hors_gv(self, texte: str, langue: str, cands: list[dict] | None,
986:    def _syntagmes_s(self, texte: str) -> list[dict] | None:
1222:    def _syntagmes_simple(self, texte: str, langue: str,
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, sys, collections\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nh=bl.Heuristique()\nd=json.load(open('tools/structures/donnees/gold-analyseur.json'))\n# compare per phrase how many gold roles equal predicted by best overlap\nfrom tools.res … [878 caractères tronqués]`

  ```
role    ok/tot
predicat       58/58
agent          34/34
temps           9/ 9
qualite         7/ 7
patient         5/ 5
destinataire    4/ 5
contenu         5/ 5
theme           2/ 4
cause           4/ 4
lieu            3/ 3
but             3/ 3
hypothese       2/ 2
possession      1/ 1
instrument      0/ 1
concession      1/ 1
maniere         1/ 1
consequence     0/ 1
  ```

- **bash** `{"command": "grep -n \"VERBES_LIEU\\|ADVERBES_TEMPS\\|MOTS_TEMPS\\|JOURS\\|MOIS\" tools/structures/generateur.py tools/bloc_linguistique.py | head -40; echo ====; grep -n \"VERBES_LIEU\" -A30 tools/structures/generateur.py | head -50", "description": "Find place/time lexicons"}`

  ```
tools/structures/generateur.py:28:ADVERBES_TEMPS = set("hier aujourd'hui demain maintenant ici la toujours jamais souvent deja encore tard tot".split())
tools/structures/generateur.py:65:VERBES_LIEU = set("""
tools/structures/generateur.py:266:        if gv is not None and _dernier_mot(gv.texte) in VERBES_LIEU:
tools/structures/generateur.py:372:                        and _norm(utiles[j].texte) in ADVERBES_TEMPS):
tools/structures/generateur.py:392:                             or _norm(utiles[j].texte) in VERBES_LIEU)):
tools/structures/generateur.py:402:                                 or _norm(suivant.texte) in VERBES_LIEU)))
tools/structures/generateur.py:407:                                                        or _norm(apres.texte) in VERBES_LIEU)):
tools/structures/generateur.py:446:        if t.cls == "MOT" and _norm(t.texte) in ADVERBES_TEMPS:
tools/structures/generateur.py:457:                    and _norm(utiles[j].texte) in ADVERBES_TEMPS):
tools/structures/generateur.py:588:                and _norm(m) not in VERBES_FINIS and _norm(m) not in VERBES_LIEU]
tools/bloc_linguistique.py:480:ADVERBES_TEMPS = {"hier", "demain", "aujourd'hui", "maintenant", "yesterday", "tomo
… [3095 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nh=bl.Heuristique()\ntextes=[\"Il reste à la maison.\",\"Il va à Paris.\",\"Il parle à Marie.\",\"Le train part à 14 h.\",\"La réunion est à demain.\",\"Le livre est à moi.\",\"Il pense à son pro … [716 caractères tronqués]`

  ```
Il reste à la maison.
  GN  agent          'Il'
  GV  predicat       'reste'
  GP  lieu           'à la maison'

 Il va à Paris.
  GN  agent          'Il'
  GV  predicat       'va'
  GP  lieu           'à Paris'

 Il parle à Marie.
  GN  agent          'Il'
  GV  predicat       'parle'
  GP  destinataire   'à Marie'

 Le train part à 14 h.
  GN  agent          'Le train'
  GV  predicat       'part'
  GP  destinataire   'à'
  GP  lieu           'à 14 h'

 La réunion est à demain.
  GN  agent          'La réunion'
  GV  predicat       'est'
  GP  lieu           'à demain'

 Le livre est à moi.
  GN  agent          'Le livre'
  GV  predicat       'est'
  GP  destinataire   'à moi'
  GN  patient        'moi'

 Il pense à son projet.
  GN  agent          'Il'
  GV  predicat       'pense'
  GP  destinataire   'à son projet'

 Le chat dort sur le canapé.
  GN  agent          'Le chat'
  GV  predicat       'dort'
  GP  lieu           'sur le canapé'

 Il part vers 9 h.
  GN  agent          'Il'
  GV  predicat       'part'
  GP  lieu           'vers'
  GP  lieu           'vers 9 h'

 Il court vers la gare.
  GN  agent          'Il'
  GV  predicat       'court'
  GP  lieu           'vers la 
… [1476 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nprint(type(d), list(d.keys())[:10] if isinstance(d,dict) else len(d))\ns=json.dumps(d,ensure_ascii=False)\nimport re\nfor m in re.finditer(r'.{200}W5.{400}', s):\n    print(m.group(0)); print('---')\nEOF", "d … [47 caractères tronqués]`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
nifeste.md` + JSON. **Ne modifie rien chez Panini.**", "budget_min": 90, "acceptation": [{"commande": "test -f reports/rapport-panini-manifeste.md && echo FICHE-OK", "attendu": "FICHE-OK"}]}, {"id": "W5", "jour": 17, "titre": "J3 — la restitution v3 : les rôles des GP", "mandat": "Tâche W5 (J3 après-midi) : la restitution v3 — `_role_gp` distingue **lieu / temps / destinataire / possession / complément** (des prépositions : `à` + lieu/temps/destinataire, `de` + possession, `avec` + moyen...) ; mesure la **précision et le rappel par rôle** sur le gold v2 (46) et le gold S (61/144 existants), avec
---
e": "J5 — la clôture de la semaine 2", "mandat": "Tâche W6 (J5 après-midi) : la clôture de la semaine 2 — le rapport `reports/rapport-semaine-2.md` + JSON (les chiffres avant/après de chaque vague W1-W5, les négatifs, les décisions), la mise à jour de `docs/pilotage/en-cours.md` et `semaine-2.md` (l'état par jour), le **tag annoté** `semaine-2-2026-11-20` sur le dernier commit vert, et le relevé des portes. Ne relance pas la passe complète : lis `work/portes/`.", "budget_min": 90, "acceptation": [{"commande": "git tag -l 'semaine-2-2026-11-20
… [58 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"W4\\|W5\\|J3\" docs/pilotage/chantiers.md docs/pilotage/plan-travail.md tools/chantier/*.json 2>/dev/null | head -40", "description": "Search chantier plan for W5"}`

  ```
tools/chantier/plan.json:117:   "id": "J3.1",
tools/chantier/plan.json:120:   "mandat": "Tâche J3.1 : le retrieval inter-langues **à époque contrôlée** (l'avertissement de Panini : l'époque domine). Sur le lexique B7 (71 langues) et/ou le corpus commun, mesure le retrieval avec un contrôle de date (couples contemporains vs décalés) et la surface (écriture, famille). Fiche `reports/rapport-retrieval-epoque.md` + JSON, contrôle négatif.",
tools/chantier/plan.json:130:   "id": "J3.2",
tools/chantier/plan.json:133:   "mandat": "Tâche J3.2 : la généalogie à deux faces — confronter la théorie de Panini (14 atomes, 9 dhātus) à nos mesures d'alignement (Glottolog) sur le corpus commun. Fiche `reports/rapport-genealogie-deux-faces.md` + JSON : ce qui converge, ce qui diverge, ce qui reste à mesurer. La théorie va dans `docs/theorie/genealogie-des-langues.md` (mise à jour), les chiffres restent dans reports/.",
tools/chantier/plan.json:258:   "mandat": "Tâche J7.1 : approfondir le retrieval Panini — sur les 532 langues UDHR (même source XML), mesurer le retrieval par famille Glottolog (les 29 langues de `language_genealogy.py` + l'échantillon 20) avec le contrôle d'époque, et comparer à la m
… [2230 caractères tronqués]
  ```

- **bash** `{"command": "ls journal/ | tail -20; echo ---; ls journal/2026-11* 2>/dev/null | tail -10", "description": "List recent journal entries"}`

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

journal/2026-11-15:
distribue.md
docs.md
memoire.md
mesures.md
modele.md
outils.md
portes.md
README.md
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d['taches']:\n    if t.get('id') in ('W4','W5','W6'):\n        print(json.dumps(t,ensure_ascii=False,indent=2))\nEOF", "description": "Read W5 task entry and acceptance"}`

  ```
{
  "id": "W4",
  "jour": 17,
  "titre": "J3 — Panini : le manifeste et le rejeu",
  "mandat": "Tâche W4 (J3 matin, la part du pilote) : le manifeste à envoyer à Panini — les **26 signatures manquantes** (la liste des œuvres du §334 sans signature V14), la commande exacte qu'ils doivent lancer, le format attendu ; et le **rejeu des 60 paires** du protocole (`rapport-protocole-date.md`) sur ce qui est disponible, avec le contrôle négatif. Fiche `reports/rapport-panini-manifeste.md` + JSON. **Ne modifie rien chez Panini.**",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f reports/rapport-panini-manifeste.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    }
  ]
}
{
  "id": "W5",
  "jour": 17,
  "titre": "J3 — la restitution v3 : les rôles des GP",
  "mandat": "Tâche W5 (J3 après-midi) : la restitution v3 — `_role_gp` distingue **lieu / temps / destinataire / possession / complément** (des prépositions : `à` + lieu/temps/destinataire, `de` + possession, `avec` + moyen...) ; mesure la **précision et le rappel par rôle** sur le gold v2 (46) et le gold S (61/144 existants), avec le **contrôle négatif** (permuter les rôles doit tuer la mesure). Fiche `reports/rap
… [1031 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat 93e046f7 | head -60; echo ====; git show --stat be3f41ad | head -50", "description": "See file patterns of previous W tasks"}`

  ```
commit 93e046f720fbe4d8cff4a105f6a03c8be134b657
Author: Stéphane <stephane@localhost>
Date:   Sun Nov 15 10:59:16 2026 -0500

    SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
    
    Le manifeste reports/panini-manifeste.json liste les 26 textes du protocole B1 sans signature analytic_sigs_v1 (dont 1 seul des 655 paires : zadeh_1965), leur source et SHA-256, la commande Panini (tools/panini_signatures_26.py : calibration 44 + 26 signatures, sortie hors Panini) et le format attendu (14 clés, somme 1). Le rejeu disponible calcule 27/60 paires (1 G1, 14 G2, 12 G3) ; 33 manquantes ; aucune p-value de H0. Contrôles : N2 dates permutées G2 p=0,252 ; N3 G3 p=0,001 (tiré par G3-08 / bengio_2003 non calibré) ; N4 signatures permutées ; N5 colonnes vide par isométrie ; N6 doublons ; calibration 42/44 (bengio_2003, mengzi). 3 sources <300 mots, 5 groupes de doublons parmi les 26. Aucune écriture dans Panini (statut git identique).

 docs/pilotage/en-cours.md                          |    6 +-
 journal/2026-11-15/README.md                       |    9 +-
 journal/2026-11-15/distribue.md            
… [3014 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/structures/; echo ---; grep -rn \"instrument\\|possession\\|_role_gp\\|role\" tools/structures/*.py tools/tests/*structure* 2>/dev/null | head -60", "description": "Inspect S module tests and role expectations"}`

  ```
arbre_svg.py
candidats_corpus.py
construire_donnees.py
donnees
exporter_corpus.py
generateur.py
llm.py
mesure_analyseur.py
mesure_arbre.py
mesure_corpus.py
__pycache__
README.md
serveur.py
static
tests
verifier_corpus.py
---
tools/structures/arbre_svg.py:80:        f'width="{largeur:g}" height="{hauteur:g}" role="img">',
tools/structures/arbre_svg.py:116:        morceaux.append(_noeud(x, y, s["texte"], f'{s["type"]} · {s["role"]}',
tools/structures/construire_donnees.py:11:     [("Le chat", "GN", "agent", 0), (" de la voisine", "GP", "possession", 0),
tools/structures/construire_donnees.py:17:     [("Le chat", "GN", "agent", 0), (" de la voisine", "GP", "possession", 0),
tools/structures/construire_donnees.py:24:      (" avec le télescope", "GP", "instrument", 1)],
tools/structures/construire_donnees.py:50:     (" pour attraper le bus", "Il a couru", "role")),
tools/structures/construire_donnees.py:55:     (" pour attraper le bus", "Il a couru", "role")),
tools/structures/construire_donnees.py:61:     (" de son projet", "Il a parlé", "possession")),
tools/structures/construire_donnees.py:67:     (" de son projet", " à Marie", "possession")),
tools/structures/construire_donnees.py:7
… [5054 caractères tronqués]
  ```

- **bash** `{"command": "find tools -iname \"*structure*\" -o -iname \"*generateur*\" | head -20; echo ---; grep -rn \"generateur\\|construire_donnees\" tools/tests/*.py | head -30", "description": "Find S test files"}`

  ```
tools/__pycache__/canal_structure.cpython-313.pyc
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/_structures.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/__pycache__/_structures.cpython-313.pyc
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/requests/structures.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/requests/__pycache__/structures.cpython-313.pyc
tools/docwatch/.venv/lib/python3.13/site-packages/packaging/_structures.py
tools/docwatch/.venv/lib/python3.13/site-packages/packaging/__pycache__/_structures.cpython-313.pyc
tools/docwatch/.venv/lib/python3.13/site-packages/requests/structures.py
tools/docwatch/.venv/lib/python3.13/site-packages/requests/__pycache__/structures.cpython-313.pyc
tools/docwatch/.venv/lib/python3.13/site-packages/_pytest/mark/structures.py
tools/docwatch/.venv/lib/python3.13/site-packages/_pytest/mark/__pycache__/structures.cpython-313.pyc
tools/structures
tools/structures/tests/__pycache__/test_generateur.cpython-313.pyc
tools/structures/tests/test_generateur.py
tools/structures/__pycache__/generateur.cpython-313.pyc
tools/structures/generateur.py
tools/canal_struct
… [10 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"role\\|instrument\\|possession\\|lieu\\|temps\" tools/structures/tests/test_generateur.py | head -60; echo ====; grep -rn \"instrument\\|possession\" tools/structures/tests/*.py | head -20", "description": "Inspect S generator tests"}`

  ```
29:    def test_role_pour(self):
31:        roles = {s["role"] for c in cs for s in c["segments"] if s["type"] == "GP"}
32:        self.assertIn("but", roles)
33:        self.assertIn("cause", roles)
47:                         if (x["debut"], x["fin"], x["type"], x["role"], x["niveau"]) !=
48:                            (y["debut"], y["fin"], y["type"], y["role"], y["niveau"])]
55:    def _roles(self, texte):
56:        return {(s["texte"].strip(), s["type"]): s["role"]
59:    def test_de_possession_ou_theme(self):
60:        self.assertEqual(self._roles("Le chat de la voisine qui dort sur le toit se réveille.")
61:                         [("de la voisine", "GP")], "possession")
62:        self.assertEqual(self._roles("Il a parlé à Marie de son projet.")
65:    def test_avec_instrument_ou_attribut(self):
66:        # La structure de base est l'instrument ; l'attachement au GN en fait un attribut.
67:        self.assertEqual(self._roles("J'ai vu l'homme avec le télescope.")
68:                         [("avec le télescope", "GP")], "instrument")
71:                     next(s["role"] for s in c["segments"] if s["type"] == "GP")
73:        self.assertEqual(par_cible.get("J'ai vu"),
… [2577 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/structures/tests/test_generateur.py", "description": "Read S test header"}`

  ```
"""Tests du générateur de candidats."""
import unittest

import generateur


class TestGenerateur(unittest.TestCase):
    def test_segments_alignes(self):
        for texte in ("Le chat de la voisine qui dort sur le toit se réveille.",
                      "J'ai vu l'homme avec le télescope.",
                      "Il a couru pour attraper le bus.",
                      "Elle a dit qu'elle viendrait hier."):
            for c in generateur.analyser(texte):
                prec = 0
                for s in c["segments"]:
                    self.assertGreaterEqual(s["debut"], prec, texte)
                    self.assertLessEqual(s["fin"], len(texte), texte)
                    self.assertEqual(texte[s["debut"]:s["fin"]], s["texte"], texte)
                    prec = s["fin"]
                self.assertGreaterEqual(len(c["segments"]), 2, texte)

    def test_relative_deux_lectures(self):
        cs = generateur.analyser("Le chat de la voisine qui dort sur le toit se réveille.")
        cibles = {c["attachement"]["cible"] for c in cs if c["attachement"]}
        self.assertIn("voisine", cibles)
        self.assertIn("Le chat", cibles)
        self.assertEqual(len(cs), 2)

    def t
… [2701 caractères tronqués]
  ```

### 🤖 Assistant

Je vais prototyper la nouvelle règle de rôle avant de toucher au code partagé, pour mesurer honnêtement si les rôles se séparent.

- **bash** `{"command": "cat > /tmp/proto_v3.py <<'PY'\nimport json, re, sys\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nimport tools.restitution_v2 as v2\n\nTEMPS = set(\"\"\"demain hier aujourd'hui maintenant midi  … [10542 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/proto_v3.py", line 22, in <module>
    pré vallon colline berge lac etang étang fleuve ocean océan terre air espace""" ).split()
                                                                                      ^^^^^
AttributeError: 'set' object has no attribute 'split'
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\np='/tmp/proto_v3.py'\ns=open(p).read()\ns=s.replace('espace\"\"\" ).split()','espace\"\"\".split())')\nopen(p,'w').write(s)\nEOF\npython3 /tmp/proto_v3.py", "description": "Fix set literal and rerun prototype"}`

  ```
=== banc ===
banc v3: cadres exacts 19 non vides 16 F1 0.5333
{
 "agent": {
  "exacts": 29,
  "attendus": 32,
  "predits": 28,
  "justes": 18,
  "faux_positifs": 10,
  "faux_negatifs": 14,
  "vrais_negatifs": 11,
  "taux_exact": 0.6304,
  "precision": 0.6429,
  "rappel": 0.5625,
  "f1": 0.6
 },
 "predicat": {
  "exacts": 22,
  "attendus": 39,
  "predits": 39,
  "justes": 19,
  "faux_positifs": 20,
  "faux_negatifs": 20,
  "vrais_negatifs": 3,
  "taux_exact": 0.4783,
  "precision": 0.4872,
  "rappel": 0.4872,
  "f1": 0.4872
 },
 "lieu": {
  "exacts": 40,
  "attendus": 6,
  "predits": 6,
  "justes": 3,
  "faux_positifs": 3,
  "faux_negatifs": 3,
  "vrais_negatifs": 37,
  "taux_exact": 0.8696,
  "precision": 0.5,
  "rappel": 0.5,
  "f1": 0.5
 }
}
 lieu f08 '' att 'Where' exacts 0
 lieu f20 'vers' att '' exacts 0
 lieu f21 'en haussant les épaules' att '' exacts 2
 lieu f24 '' att 'au bord de la forêt' exacts 0
 lieu f49 '' att 'salle B12' exacts 2
 lieu f50 'dans la cour' att '' exacts 0

=== gold S ===
gold S v3 per role:
  predicat       58/58  preds=48
  agent          34/34  preds=34
  temps           5/ 9  preds=6
  qualite         7/ 7  preds=7
  patient         5/ 5  preds=5
  
… [397 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\np='/tmp/proto_v3.py'\ns=open(p).read()\n# insert known preps set and skip logic\ns=s.replace('PREP_DEST = set(\"a à au aux to\".split())',\n'PREP_DEST = set(\"a à au aux to\".split())\\nPREP_CONNUES = PREP_LIEU | PREP_TEMPS | PREP_MOYEN | PREP_BUT | PREP_PO … [1095 caractères tronqués]`

  ```
=== banc ===
banc v3: cadres exacts 19 non vides 16 F1 0.5333
{
 "agent": {
  "exacts": 29,
  "attendus": 32,
  "predits": 28,
  "justes": 18,
  "faux_positifs": 10,
  "faux_negatifs": 14,
  "vrais_negatifs": 11,
  "taux_exact": 0.6304,
  "precision": 0.6429,
  "rappel": 0.5625,
  "f1": 0.6
 },
 "predicat": {
  "exacts": 22,
  "attendus": 39,
  "predits": 39,
  "justes": 19,
  "faux_positifs": 20,
  "faux_negatifs": 20,
  "vrais_negatifs": 3,
  "taux_exact": 0.4783,
  "precision": 0.4872,
  "rappel": 0.4872,
  "f1": 0.4872
 },
 "lieu": {
  "exacts": 40,
  "attendus": 6,
  "predits": 6,
  "justes": 3,
  "faux_positifs": 3,
  "faux_negatifs": 3,
  "vrais_negatifs": 37,
  "taux_exact": 0.8696,
  "precision": 0.5,
  "rappel": 0.5,
  "f1": 0.5
 }
}
 lieu f08 '' att 'Where' exacts 0
 lieu f20 'vers' att '' exacts 0
 lieu f21 'en haussant les épaules' att '' exacts 2
 lieu f24 '' att 'au bord de la forêt' exacts 0
 lieu f49 '' att 'salle B12' exacts 2
 lieu f50 'dans la cour' att '' exacts 0

=== gold S ===
gold S v3 per role:
  predicat       58/58  preds=48
  agent          34/34  preds=34
  temps           9/ 9  preds=10
  qualite         7/ 7  preds=7
  patient         5/ 5  preds=5
 
… [398 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _mots\" -A40 tools/bloc_linguistique.py | head -60", "description": "Read tokenizer types"}`

  ```
828:    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
829-        motif = re.compile(r"\b[ldmtsnLDMTNS]['’](?=\w)|\w+(?:['’\-]\w+)*|\d+(?:[.,]\d+)*|https?://\S+|[\U0001F300-\U0001FAFF]|[^\w\s]")
830-        sortie = []
831-        for m in motif.finditer(texte):
832-            t = m.group()
833-            if t.startswith(("http://", "https://")):
834-                typ = "url"
835-            elif t[0].isdigit():
836-                typ = "nombre"
837-            elif re.fullmatch(r"[^\w\s]", t):
838-                typ = "ponctuation"
839-            elif len(t) == 1 and ord(t) >= 0x1F300:
840-                typ = "emoji"
841-            else:
842-                typ = "mot"
843-            sortie.append((m.start(), m.end(), t, typ))
844-        return sortie
845-
846-    @staticmethod
847-    def _phrases(texte: str) -> list[tuple[int, int, str, str]]:
848-        return decouper_phrases(texte)
849-
850-
851-    @staticmethod
852-    def _negation(phrase: str) -> bool:
853-        return bool(re.search(r"\b(?:ne|n['’])\b.{0,40}\b(?:pas|plus|jamais|rien|guère)\b", phrase, re.I)
854-                    or re.search(r"\b(?:not|no|never|none|nothing|n't)\b", phrase, r
… [915 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nh=bl.Heuristique()\nfor t in [\"Le train part à 14 h.\",\"Il part vers 9 h.\",\"Rendez-vous le 12/03/2026 à 14h30.\",\"La réunion est reportée à demain, 10 h 30, salle B12.\"]:\n    print('\\n', … [246 caractères tronqués]`

  ```
Le train part à 14 h.
[('Le', 'mot'), ('train', 'mot'), ('part', 'mot'), ('à', 'mot'), ('14', 'nombre'), ('h', 'mot'), ('.', 'ponctuation')]
  GN  agent          'Le train'
  GV  predicat       'part'
  GP  destinataire   'à'
  GP  lieu           'à 14 h'

 Il part vers 9 h.
[('Il', 'mot'), ('part', 'mot'), ('vers', 'mot'), ('9', 'nombre'), ('h', 'mot'), ('.', 'ponctuation')]
  GN  agent          'Il'
  GV  predicat       'part'
  GP  lieu           'vers'
  GP  lieu           'vers 9 h'

 Rendez-vous le 12/03/2026 à 14h30.
[('Rendez-vous', 'mot'), ('le', 'mot'), ('12', 'nombre'), ('/', 'ponctuation'), ('03', 'nombre'), ('/', 'ponctuation'), ('2026', 'nombre'), ('à', 'mot'), ('14h30', 'nombre'), ('.', 'ponctuation')]
  GV  predicat       'Rendez-vous'
  GN  patient        'le'
  GP  destinataire   'à'
  GP  destinataire   'à 14h'

 La réunion est reportée à demain, 10 h 30, salle B12.
[('La', 'mot'), ('réunion', 'mot'), ('est', 'mot'), ('reportée', 'mot'), ('à', 'mot'), ('demain', 'mot'), (',', 'ponctuation'), ('10', 'nombre'), ('h', 'mot'), ('30', 'nombre'), (',', 'ponctuation'), ('salle', 'mot'), ('B12', 'mot'), ('.', 'ponctuation')]
  GN  agent          'La réunion'
  GV  predic
… [111 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, json; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl, tools.restitution_v2 as v2\nh=bl.Heuristique()\nd=json.load(open('tools/structures/donnees/gold-analyseur.json'))\nfor pid in ['p005','g019','h060','p002','h056']:\n    p=next(x for x in d … [382 caractères tronqués]`

  ```
## p005 Il a parlé à Marie de son projet.
 GOLD GV predicat 'Il a parlé' 0 10
 GOLD GP destinataire 'à Marie' 11 18
 GOLD GP theme 'de son projet' 19 32
  SEG GN agent 'Il' 0 2
  SEG GV predicat 'a parlé' 3 10
  SEG GP destinataire 'à Marie' 11 18
  SEG GP destinataire 'à Marie de son projet' 11 32
  SEG GP theme 'de son projet' 19 32

## g019 Il a parlé de son projet à Marie.
 GOLD GV predicat 'Il a parlé' 0 10
 GOLD GP theme 'de son projet' 11 24
 GOLD GP destinataire 'à Marie' 25 32
  SEG GN agent 'Il' 0 2
  SEG GV predicat 'a parlé' 3 10
  SEG GP theme 'de son projet' 11 24
  SEG GP theme 'de son projet à Marie' 11 32
  SEG GP destinataire 'à Marie' 25 32

## h060 Le chat fait des bonds.
 GOLD GN agent 'Le chat' 0 7
 GOLD GV predicat 'fait' 8 12
 GOLD GP theme 'des bonds' 13 22
  SEG GN agent 'Le chat' 0 7
  SEG GV predicat 'fait' 8 12
  SEG GP possession 'des bonds' 13 22

## p002 J'ai vu l'homme avec le télescope.
 GOLD GV predicat "J'ai vu" 0 7
 GOLD GN patient "l'homme" 8 15
 GOLD GP instrument 'avec le télescope' 16 33
  SEG GN agent "J'ai" 0 4
  SEG GV predicat 'vu' 5 7
  SEG GV prédicat "vu l'homme" 5 15
  SEG GN patient "l'homme" 8 15
  SEG GP attribut 'avec le télescop
… [391 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\np='/tmp/proto_v3.py'\ns=open(p).read()\n# add en gerund rule\ns=s.replace('''    if base == \"en\":\n        if est_temps(suivant): return \"temps\"''','''    if base == \"en\":\n        if est_temps(suivant): return \"temps\"\n        if re.match(r\"^[a-zà … [1231 caractères tronqués]`

  ```
=== banc ===
banc v3: cadres exacts 20 non vides 17 F1 0.5406
{
 "agent": {
  "exacts": 29,
  "attendus": 32,
  "predits": 28,
  "justes": 18,
  "faux_positifs": 10,
  "faux_negatifs": 14,
  "vrais_negatifs": 11,
  "taux_exact": 0.6304,
  "precision": 0.6429,
  "rappel": 0.5625,
  "f1": 0.6
 },
 "predicat": {
  "exacts": 22,
  "attendus": 39,
  "predits": 39,
  "justes": 19,
  "faux_positifs": 20,
  "faux_negatifs": 20,
  "vrais_negatifs": 3,
  "taux_exact": 0.4783,
  "precision": 0.4872,
  "rappel": 0.4872,
  "f1": 0.4872
 },
 "lieu": {
  "exacts": 42,
  "attendus": 6,
  "predits": 4,
  "justes": 3,
  "faux_positifs": 1,
  "faux_negatifs": 3,
  "vrais_negatifs": 39,
  "taux_exact": 0.913,
  "precision": 0.75,
  "rappel": 0.5,
  "f1": 0.6
 }
}
 lieu f08 '' att 'Where' exacts 0
 lieu f24 '' att 'au bord de la forêt' exacts 0
 lieu f49 '' att 'salle B12' exacts 2
 lieu f50 'dans la cour' att '' exacts 0

=== gold S ===
gold S v3 per role:
  predicat       58/58  preds=57
  agent          34/34  preds=34
  temps           9/ 9  preds=10
  qualite         7/ 7  preds=7
  patient         5/ 5  preds=5
  destinataire    5/ 5  preds=5
  contenu         5/ 5  preds=5
  theme           3/ 4
… [313 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nexec(open('/tmp/proto_v3.py').read().split(\"if __name__\")[0])\nimport json, sys, collections\nimport tools.bloc_linguistique as bl, tools.restitution_v2 as v2\nd=json.load(open('/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/gold … [819 caractères tronqués]`

  ```
h060 gold theme 'des bonds' pred temps 'des bonds'
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nexec(open('/tmp/proto_v3.py').read().split(\"if __name__\")[0])\nimport tools.bloc_linguistique as bl, tools.restitution_v2 as v2\nh=bl.Heuristique(); t='Le chat fait des bonds.'\na=h.analyser(t); appliquer(a,t)\nfor e in a.etiquettes:\n    if e.niveau=='sy … [123 caractères tronqués]`

  ```
GN agent 'Le chat' 0 7
GV predicat 'fait' 8 12
GP temps 'des bonds' 13 22
  ```

- **bash** `{"command": "cd /tmp && sed -i 's/ after des dès jusqu/ after dès jusqu/' /tmp/proto_v3.py && python3 /tmp/proto_v3.py | tail -25", "description": "Fix des/dès collision and rerun"}`

  ```
lieu f08 '' att 'Where' exacts 0
 lieu f24 '' att 'au bord de la forêt' exacts 0
 lieu f49 '' att 'salle B12' exacts 2
 lieu f50 'dans la cour' att '' exacts 0

=== gold S ===
gold S v3 per role:
  predicat       58/58  preds=57
  agent          34/34  preds=34
  temps           9/ 9  preds=9
  qualite         7/ 7  preds=7
  patient         5/ 5  preds=5
  destinataire    5/ 5  preds=5
  contenu         5/ 5  preds=5
  theme           4/ 4  preds=4
  cause           4/ 4  preds=4
  lieu            3/ 3  preds=3
  but             3/ 3  preds=3
  hypothese       2/ 2  preds=2
  possession      1/ 1  preds=1
  instrument      1/ 1  preds=0
  concession      1/ 1  preds=1
  maniere         1/ 1  preds=1
  consequence     1/ 1  preds=1
total 144 / 144
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys; sys.path.insert(0,'.')\nimport tools.restitution as r, tools.restitution_v2 as v2\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nm=v2.mesurer_banc_v2(r.items_b … [405 caractères tronqués]`

  ```
f20 exacts 0
  agent pred 'Leroy' att 'M. Dupont, le Dr Martin et Mme Leroy' egal False
  predicat pred 'M' att 'sont arrivés' egal False
  lieu pred 'vers 9 h' att '' egal False

 f21 exacts 3
  agent pred 'Je' att 'Je' egal True
  predicat pred 'ne sais pas' att 'ne sais pas' egal True
  lieu pred '' att '' egal True

 f35 exacts 2
  agent pred 'The quick brown fox' att 'The quick brown fox' egal True
  predicat pred 'jumps' att 'jumps' egal True
  lieu pred '' att 'over the lazy dog' egal False

 f49 exacts 2
  agent pred 'La réunion' att 'La réunion' egal True
  predicat pred 'est reportée' att 'est reportée' egal True
  lieu pred '' att 'salle B12' egal False

 f50 exacts 0
  agent pred 'il' att 'Le chat de la voisine' egal False
  predicat pred 'Notes' att 'se réveille' egal False
  lieu pred 'dans la cour' att '' egal False
  ```

- **bash** `{"command": "sed -n '720,830p' tools/drave.py; echo ====; sed -n '940,985p' tools/drave.py", "description": "Read cmd_restituer and argparse"}`

  ```
file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------- restitution


def cmd_restituer(args: argparse.Namespace) -> int:
    """Reconstruit la surface depuis l'annotation et rend la fidélité du miroir.

    Deux modes : un **texte** (ou un fichier), ou un **banc** JSON de textes
    (`--banc`, le format de `reports/pensee-fiabilite-produit.json`). Le mode banc
    laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`
    ajoute la **forme canonique v1** (segments + rôles + cibles) et son miroir ;
    `--roles` ajoute la **v2** (agent, prédicat, lieu) et, sur un banc, sa fidélité à
    l'or. La sortie de la v0 reste celle par défaut.
    """
    if args.roles and args.canonique:
        print(f"{NOM}: erreur d'usage : --roles et --canonique sont exclusifs",
              file=sys.stderr)
        return 2
    if args.gold and not (args.banc and args.roles):
        print(f"{NOM}: erreur d'usage : --gold ne sert qu'avec --banc --roles",
              file=sys.stderr)
        return 2
    if args.banc:
        if args.texte is not None or args.fichier:
            print(f"{NOM}: erreur d'us
… [6331 caractères tronqués]
  ```

### 🤖 Assistant

Le prototype montre une séparation nette sur le gold S et un gain marginal sur le gold v2. J'implémente maintenant la règle dans un module dédié, sans casser la v2.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "content": "\"\"\"roles_gp.py — les rôles des groupes prépositionnels (restitution v3).\n\nLa v2 lisait la **préposition seule** : `à` était toujours un destinataire, `de` toujours\nun thème, `avec` toujours un moyen. … [16767 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "sed -n '530,565p' tools/bloc_linguistique.py; echo ====; sed -n '1,40p' tools/bloc_linguistique.py", "description": "Read _role_gp and imports"}`

  ```
if forme in VERBES_CONNUS:
                    return True
    # formes du 1er groupe : `range` → `ranger` (le e reste, le g durcit)
    if n.endswith("e") and (n[:-1] + "ger") in VERBES_CONNUS:
        return True
    return False


def _role_gp(prep: str) -> str:
    p = prep.casefold()
    if p in {"dans", "sur", "sous", "chez", "vers", "entre", "devant", "derrière", "près", "loin",
             "in", "on", "at", "under", "between"}:
        return "lieu"
    if p in {"pendant", "depuis", "durant", "avant", "après", "during", "since", "before", "after"}:
        return "temps"
    if p in {"pour", "afin", "for", "to"}:
        return "but"
    if p in {"par", "by"}:
        # `par` + GN est l'**agent** d'un passif (`Le chat est mangé par le chien`) ;
        # `avec`/`sans` restent le moyen.
        return "agent"
    if p in {"avec", "sans", "with", "without"}:
        return "moyen"
    if p in {"à", "a", "au", "aux", "to"}:
        return "destinataire"
    if p in {"de", "du", "des", "of", "from"}:
        return "theme"
    return "complément"


# --------------------------------------------------------------------------- heuristique


# ------------------------------------
… [2215 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '40,75p' tools/bloc_linguistique.py; grep -n \"^from tools\\|^import tools\\|RACINE\" tools/bloc_linguistique.py | head -20", "description": "Check import style in bloc_linguistique"}`

  ```
import subprocess
import sys
import threading
import time
import unicodedata
import urllib.request
from dataclasses import dataclass, field
from typing import Protocol, Sequence

RACINE = pathlib.Path(__file__).resolve().parent.parent
NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
           "pragmatique", "document")
SOURCES = ("heuristique", "neuronal", "humain")
SCRIPT_NEUTRE = "Zyyy"

# --------------------------------------------------------------------------- types


@dataclass(frozen=True)
class Span:
    debut: int
    fin: int

    def json(self) -> dict:
        return {"debut": self.debut, "fin": self.fin}


@dataclass
class Etiquette:
    niveau: str
    type: str
    valeur: str
    debut: int
    fin: int
    source: str = "heuristique"
    confiance: float = 0.5
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
990:            if str(RACINE / "tools/structures") not in sys.path:
991:                sys.path.insert(0, str(RACINE / "tools/structures"))
2877:    ap.add_argument("--modele", default=str(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf"))
2882:    ap.add_argument("--udhr", default=str(RACINE / "data/udhr/articles.jsonl")
… [1 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/__init__.py && cat tools/__init__.py | head -40", "description": "Check tools package init"}`

  ```
[stderr]
ls: cannot access 'tools/__init__.py': No such file or directory
[exit code: 2]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "old_string": "RACINE = pathlib.Path(__file__).resolve().parent.parent\nNIVEAUX = (\"graphème\", \"morphème\", \"mot\", \"pos\", \"syntagme\", \"phrase\", \"discours\",\n           \"pragmatique\", \"document … [408 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 44, "limit": 10}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 536, "limit": 28}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
44: import unicodedata
45: import urllib.request
46: from dataclasses import dataclass, field
47: from typing import Protocol, Sequence
48: 
49: RACINE = pathlib.Path(__file__).resolve().parent.parent
50: NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
51:            "pragmatique", "document")
52: SOURCES = ("heuristique", "neuronal", "humain")
53: SCRIPT_NEUTRE = "Zyyy"

(Showing lines 44-53 of 2906. Use offset=54 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
536: 
537: 
538: def _role_gp(prep: str) -> str:
539:     p = prep.casefold()
540:     if p in {"dans", "sur", "sous", "chez", "vers", "entre", "devant", "derrière", "près", "loin",
541:              "in", "on", "at", "under", "between"}:
542:         return "lieu"
543:     if p in {"pendant", "depuis", "durant", "avant", "après", "during", "since", "before", "after"}:
544:         return "temps"
545:     if p in {"pour", "afin", "for", "to"}:
546:         return "but"
547:     if p in {"par", "by"}:
548:         # `par` + GN est l'**agent** d'un passif (`Le chat est mangé par le chien`) ;
549:         # `avec`/`sans` restent le moyen.
550:         return "agent"
551:     if p in {"avec", "sans", "with", "without"}:
552:         return "moyen"
553:     if p in {"à", "a", "au", "aux", "to"}:
554:         return "destinataire"
555:     if p in {"de", "du", "des", "of", "from"}:
556:         return "theme"
557:     return "complément"
558: 
559: 
560: # --------------------------------------------------------------------------- heuristique
561: 
562: 
563: # ------------
… [157 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "old_string": "RACINE = pathlib.Path(__file__).resolve().parent.parent\nNIVEAUX = (\"graphème\", \"morphème\", \"mot\", \"pos\", \"syntagme\", \"phrase\", \"discours\",\n           \"pragmatique\", \"document … [408 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "old_string": "def _role_gp(prep: str) -> str:\n    p = prep.casefold()\n    if p in {\"dans\", \"sur\", \"sous\", \"chez\", \"vers\", \"entre\", \"devant\", \"derrière\", \"près\", \"loin\",\n             \" … [2555 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nfrom tools.roles_gp import CAS_SEPARATION, role_gp\nok=0\nfor c in CAS_SEPARATION:\n    got=role_gp(c['prep'], c.get('suivant',''), c.get('precedent',''), c.get('precedent_texte',''))\n    flag='OK' if got==c['attendu'] else 'XX'\n  … [220 caractères tronqués]`

  ```
XX à + lieu à 'la maison' → temps (attendu lieu)
OK à + ville à 'Paris' → lieu (attendu lieu)
OK à + heure à '14 h' → temps (attendu temps)
OK à + jour à 'demain' → temps (attendu temps)
OK à + personne à 'Marie' → destinataire (attendu destinataire)
OK à + infinitif à 'manger' → but (attendu but)
OK de + GN de 'la voisine' → possession (attendu possession)
OK de + GV de 'son projet' → theme (attendu theme)
OK avec + moyen avec 'le télescope' → moyen (attendu moyen)
XX dans + lieu dans 'le parc' → temps (attendu lieu)
XX sur + lieu sur 'le canapé' → temps (attendu lieu)
OK pendant + temps pendant 'deux heures' → temps (attendu temps)
OK vers + temps vers '9 h' → temps (attendu temps)
XX vers + lieu vers 'la gare' → temps (attendu lieu)
XX sur + durée sur 'deux ans' → lieu (attendu temps)
OK en + année en '2020' → temps (attendu temps)
OK en + véhicule en 'voiture' → moyen (attendu moyen)
OK par + passif par 'Marie' → agent (attendu agent)
OK par + moyen par 'la porte' → moyen (attendu moyen)
OK over + lieu over 'the lazy dog' → lieu (attendu lieu)
OK to + personne to 'Mary' → destinataire (attendu destinataire)
OK to + lieu to 'the station' → lieu (attendu lieu)
XX at + heure at '9
… [75 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nfrom tools import roles_gp as r\nfor s in ['la maison','le parc','le canapé','la gare','deux ans','9','9 h','demain','Paris','Marie','the lazy dog']:\n    print(repr(s),'temps',r.est_temps(s),'lieu',r.est_lieu(s),'mots',r.mots(r.nor … [62 caractères tronqués]`

  ```
'la maison' temps True lieu True mots ['la', 'maison']
'le parc' temps True lieu True mots ['le', 'parc']
'le canapé' temps True lieu True mots ['le', 'canapé']
'la gare' temps True lieu True mots ['la', 'gare']
'deux ans' temps False lieu False mots ['deux', 'ans']
'9' temps False lieu False mots ['9']
'9 h' temps True lieu False mots ['9', 'h']
'demain' temps True lieu False mots ['demain']
'Paris' temps False lieu True mots ['paris']
'Marie' temps False lieu False mots ['marie']
'the lazy dog' temps False lieu False mots ['the', 'lazy', 'dog']
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nfrom tools import roles_gp as r\nfor s in ['la maison','le parc','le canapé','la gare']:\n    n=r.normaliser(s); print(s, [m for m in r.mots(n)[:2] if m in r.TEMPS], 'TEMPS size',len(r.TEMPS))\nprint('la' in r.TEMPS, 'maison' in r.T … [143 caractères tronqués]`

  ```
la maison ['la'] TEMPS size 100
le parc ['le'] TEMPS size 100
le canapé ['le'] TEMPS size 100
la gare ['la'] TEMPS size 100
True False True False
['ce', 'cet', 'ete', 'la', 'le', 'mai', 'tot', 'tôt', 'été']
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "offset": 37, "limit": 18}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py</path>
<type>file</type>
<content>
37: soirée nuit jour journee journée semaine quinzaine mois annee année heure fois instant
38: moment periode période siecle siècle printemps ete été automne hiver lundi mardi mercredi
39: jeudi vendredi samedi dimanche janvier fevrier février mars avril mai juin juillet aout
40: août septembre octobre novembre decembre décembre noel noël paques pâques tot tôt tard
41: bientot bientôt ensuite puis enfin deja déjà jamais toujours souvent parfois quelquefois
42: recemment récemment actuellement desormais désormais auparavant jadis apres apres-midi
43: après après-midi avant-hier apres-demain après-demain hier-soir ce-soir aujourdhui
44: aujourd'hui ce matin cet apres-midi cet après-midi cette nuit ce mois cette semaine cette
45: annee année l'annee l'année le mois la semaine l'heure la fois
46: """.split())
47: 
48: # Noms de lieux communs et de grandes villes/pays : un repère géographique, pas une liste
49: # de noms propres. Un nom propre inconnu après `à` reste un destinataire (le défaut).
50: LIEUX = frozenset("""
51: maison parc ecole école gare salle rue ville pays bord to
… [383 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "old_string": "soirée nuit jour journee journée semaine quinzaine mois annee année heure fois instant\nmoment periode période siecle siècle printemps ete été automne hiver lundi mardi mercredi\njeudi vendredi samedi d … [1318 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "offset": 122, "limit": 28}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py</path>
<type>file</type>
<content>
122: VERBES_EN = frozenset("""
123: eat go see be have do make take get come know think say tell give find work call try ask
124: need feel become leave put mean keep let begin seem help talk turn start show hear play run
125: move like live believe hold bring happen write provide sit stand lose pay meet include
126: continue set learn change lead understand watch follow stop create speak read allow add
127: spend grow open walk win offer remember love consider appear buy wait serve die send expect
128: build stay fall cut reach kill remain
129: """.split())
130: 
131: MOT = re.compile(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’][0-9A-Za-zÀ-ÖØ-öø-ÿ]+)?")
132: DET = frozenset("""
133: le la les l' un une des du de d' the a an mon ma mes ton ta tes son sa ses notre nos votre vos
134: leur leurs ce cette ces cet
135: """.split())
136: 
137: 
138: # --------------------------------------------------------------------------- outils
139: 
140: 
141: def normaliser(texte: str) -> str:
142:     """Minuscules, apostrophe droite ; les accents sont **gardés** (`dès` ≠ `des`)."""
143:     return (texte
… [221 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "offset": 170, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py</path>
<type>file</type>
<content>
170:     n = normaliser(texte)
171:     if not n:
172:         return False
173:     for m in mots(n)[:2]:
174:         if m in TEMPS:
175:             return True
176:     if re.search(r"\d{1,2}\s*h(?:\s*\d{2})?", n):        # 14 h, 14h30, 9 h 05
177:         return True
178:     if re.search(r"\d{1,2}\s*:\s*\d{2}", n):             # 14:30
179:         return True
180:     if re.search(r"\d{1,2}\s*/\s*\d{1,2}(?:\s*/\s*\d{2,4})?", n):  # 12/03/2026
181:         return True
182:     if re.search(r"\d{1,4}\s*(ans?|annees?|années?|jours?|mois|semaines?|heures?|minutes?|"
183:                  r"secondes?|siecles?|siècles?)\b", n):
184:         return True
185:     if re.fullmatch(r"\d{4}", mots(n)[0] if mots(n) else ""):      # 2020
186:         return True
187:     return False
188: 
189: 
190: def est_lieu(texte: str) -> bool:
191:     """Le texte qui suit la préposition est-il un lieu (nom commun ou ville/pays) ?"""
192:     t = tete(texte)
193:     if not t:
194:         return False
195:     n = normaliser(t)
196:     return n in LIEUX or n in VILLES
197: 
198: 
199: def est
… [102 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "old_string": "    for m in mots(n)[:2]:\n        if m in TEMPS:\n            return True\n    if re.search(r\"\\d{1,2}\\s*h(?:\\s*\\d{2})?\", n):        # 14 h, 14h30, 9 h 05", "new_string": "    for m in mots(n)[:2] … [235 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nfrom tools.roles_gp import CAS_SEPARATION, role_gp, est_temps, est_lieu\nok=0\nfor c in CAS_SEPARATION:\n    got=role_gp(c['prep'], c.get('suivant',''), c.get('precedent',''), c.get('precedent_texte',''))\n    if got==c['attendu']:  … [300 caractères tronqués]`

  ```
24/24
'la maison' False True
'le parc' False True
'deux ans' True False
'9' True False
'14 h' True False
'demain' True False
  ```

### 🤖 Assistant

La règle de séparation passe 24/24. J'écris maintenant le module de mesure v3 (or 46, or S, appariement, contrôles négatifs).

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "content": "\"\"\"restitution_v3.py — la restitution v3 : les rôles des groupes prépositionnels.\n\nLa v2 lisait la préposition seule. La v3 ajoute le **contexte** et sépare les cinq rôles\nnommés par la tâche : … [22264 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "grep -n \"def est_preposition\\|PREP_LIEU\\|PREP_AUTRES\" tools/roles_gp.py | head -10", "description": "Locate prep sets for helper"}`

  ```
102:PREP_LIEU = frozenset("""
106:PREP_AUTRES = {
248:    if base in PREP_LIEU:
280:    if base in PREP_AUTRES:
281:        return PREP_AUTRES[base]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "offset": 100, "limit": 14}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py</path>
<type>file</type>
<content>
100: PREP_POSSESSION = frozenset("de du des d' of from".split())
101: PREP_DEST = frozenset("a à au aux to".split())
102: PREP_LIEU = frozenset("""
103: dans sur sous chez vers entre devant derriere derrière pres près loin in on at under between
104: over above below behind near around through across
105: """.split())
106: PREP_AUTRES = {
107:     "malgre": "concession", "malgré": "concession", "selon": "source",
108:     "sans": "maniere", "sans": "maniere",
109: }
110: 
111: # Mots qui ressemblent à un infinitif mais n'en sont pas (noms en -er/-ir/-re).
112: FAUX_INFINITIFS = frozenset("""
113: hier hiver fer mer pere père mere mère frere frère ver cher leger léger premier dernier

(Showing lines 100-113 of 325. Use offset=114 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "old_string": "PREP_POSSESSION = frozenset(\"de du des d' of from\".split())\nPREP_DEST = frozenset(\"a à au aux to\".split())\nPREP_LIEU = frozenset(\"\"\"\ndans sur sous chez vers entre devant derriere derrière pres … [891 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "offset": 210, "limit": 18}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py</path>
<type>file</type>
<content>
210:     t = tete(texte)
211:     if not t:
212:         return False
213:     n = normaliser(t)
214:     if n in FAUX_INFINITIFS:
215:         return False
216:     if langue == "en":
217:         return n in VERBES_EN
218:     return len(n) > 2 and n.endswith(("er", "ir", "re"))
219: 
220: 
221: def est_passif(precedent_texte: str) -> bool:
222:     """Un `par` après un auxiliaire + participe est un agent, pas un moyen."""
223:     n = normaliser(precedent_texte)
224:     return bool(re.search(r"\b(est|sont|etais|était|etaient|étaient|ete|été|sera|seront|suis|"
225:                           r"es|sommes|etes|êtes|was|were|is|are|been|be)\b", n))
226: 
227: 

(Showing lines 210-227 of 327. Use offset=228 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "old_string": "def est_passif(precedent_texte: str) -> bool:\n    \"\"\"Un `par` après un auxiliaire + participe est un agent, pas un moyen.\"\"\"\n    n = normaliser(precedent_texte)\n    return bool(re.search(r\"\\b … [724 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "offset": 300, "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py</path>
<type>file</type>
<content>
300:               if precision + rappel else 0.0)
301:         par_role[role] = {
302:             "attendus": attendus, "predits": predits, "justes": j,
303:             "precision": precision, "rappel": rappel, "f1": f1,
304:         }
305:     total = sum(or_counts.values())
306:     j_total = sum(justes.values())
307:     cinq = {role: par_role.get(role, {"attendus": 0, "predits": 0, "justes": 0,
308:                                        "precision": 0.0, "rappel": 0.0, "f1": 0.0})
309:             for role in CINQ}
310:     attendus_cinq = sum(x["attendus"] for x in cinq.values())
311:     predits_cinq = sum(x["predits"] for x in cinq.values())
312:     justes_cinq = sum(x["justes"] for x in cinq.values())
313:     precision_cinq = round(justes_cinq / predits_cinq, 4) if predits_cinq else 0.0
314:     rappel_cinq = round(justes_cinq / attendus_cinq, 4) if attendus_cinq else 0.0
315:     f1_cinq = (round(2 * precision_cinq * rappel_cinq / (precision_cinq + rappel_cinq), 4)
316:                if precision_cinq + rappel_cinq else 0.0)
317:     return {
318:        
… [2398 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "offset": 270, "limit": 36}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py</path>
<type>file</type>
<content>
270: def _cycle_tous(roles: list[str]) -> dict[str, str]:
271:     """Une permutation sans point fixe des rôles présents (rotation)."""
272:     uniques = sorted(set(roles))
273:     if len(uniques) < 2:
274:         return {r: r for r in uniques}
275:     return {r: uniques[(i + 1) % len(uniques)] for i, r in enumerate(uniques)}
276: 
277: 
278: def _agreger_paires(paires: list[dict], mapping: dict[str, str] | None = None) -> dict:
279:     """Agrège des paires (role_or, role_predit, type) en précision/rappel par rôle."""
280:     mapping = mapping or {}
281:     or_counts = collections.Counter()
282:     pred_counts = collections.Counter()
283:     justes = collections.Counter()
284:     for p in paires:
285:         r_or = roles_gp.normaliser_role(p["or"])
286:         r_pred = roles_gp.normaliser_role(_role_permute(p["predit"], mapping)
287:                                           if mapping else p["predit"])
288:         or_counts[r_or] += 1
289:         pred_counts[r_pred] += 1
290:         if r_or == r_pred:
291:             justes[r_or] += 1
292:     par_role =
… [759 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "old_string": "    for p in paires:\n        r_or = roles_gp.normaliser_role(p[\"or\"])\n        r_pred = roles_gp.normaliser_role(_role_permute(p[\"predit\"], mapping)\n                                          … [637 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "old_string": "    base = _agreger_paires(paires)\n    cycle = {role: CINQ[(i + 1) % len(CINQ)] for i, role in enumerate(CINQ)}\n    tous = _cycle_tous([p[\"predit\"] for p in paires])\n    constant = {role: \"l … [1106 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nimport tools.restitution_v3 as v3\nprint('import ok')\nprint(v3.mesurer_separation()['justes'], '/', v3.mesurer_separation()['total'])\nEOF", "description": "Test v3 import and separation"}`

  ```
import ok
24 / 24
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, sys; sys.path.insert(0,'.')\nimport tools.restitution as r, tools.restitution_v3 as v3\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nm=v3.mesurer_banc_v3(r.items_ … [1496 caractères tronqués]`

  ```
annotations 46 or 46
cadres exacts 20 non vides 17 partiels 43
roles 40 / 77 P 0.5634 R 0.5195 F1 0.5406
{
 "agent": {
  "exacts": 29,
  "attendus": 32,
  "predits": 28,
  "justes": 18,
  "faux_positifs": 10,
  "faux_negatifs": 14,
  "vrais_negatifs": 11,
  "taux_exact": 0.6304,
  "precision": 0.6429,
  "rappel": 0.5625,
  "f1": 0.6
 },
 "predicat": {
  "exacts": 22,
  "attendus": 39,
  "predits": 39,
  "justes": 19,
  "faux_positifs": 20,
  "faux_negatifs": 20,
  "vrais_negatifs": 3,
  "taux_exact": 0.4783,
  "precision": 0.4872,
  "rappel": 0.4872,
  "f1": 0.4872
 },
 "lieu": {
  "exacts": 42,
  "attendus": 6,
  "predits": 4,
  "justes": 3,
  "faux_positifs": 1,
  "faux_negatifs": 3,
  "vrais_negatifs": 39,
  "taux_exact": 0.913,
  "precision": 0.75,
  "rappel": 0.5,
  "f1": 0.6
 }
}
gp roles {'agent': 1, 'lieu': 10}
rendu {'exacts': 46, 'taux': 1.0}
neg {'eligibles': 39, 'sans_predicat': 39, 'permute': 39, 'detectes': 39}
spans {'justes': 194, 'total': 194, 'taux': 1.0}

--- gold S ---
phrases 61 roles 144 justes 143 taux 0.9931
cinq {
 "roles": [
  "lieu",
  "temps",
  "destinataire",
  "possession",
  "complement"
 ],
 "attendus": 18,
 "predits": 19,
 "justes": 18,
 "precision
… [3920 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl, tools.restitution_v2 as v2, tools.restitution_v3 as v3, tools.roles_gp as rg\nd=json.load(open('tools/structures/donnees/gold-analyseur.json'))\nh=bl.Heuristique()\nfor p in d['phrases']:\n … [701 caractères tronqués]`

  ```
h060 gold theme 'des bonds' -> pred temps 'des bonds' span 13 22
  gold span 13 22
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl, tools.restitution_v3 as v3, tools.roles_gp as rg\nt='Le chat fait des bonds.'\nprep,suiv=v3._prep_et_suivant('des bonds')\nprint('prep',repr(prep),'suiv',repr(suiv),'est_prep',rg.est_preposition … [225 caractères tronqués]`

  ```
prep 'des' suiv ' bonds' est_prep True role temps
des base des in temps True in poss True
dès base dès in temps True in poss False
de base de in temps False in poss True
du base du in temps False in poss True
  ```

- **bash** `{"command": "grep -n \"PREP_TEMPS\" -A3 tools/roles_gp.py; python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nfrom tools import roles_gp as rg\nprint(sorted(rg.PREP_TEMPS))\nEOF", "description": "Inspect PREP_TEMPS set"}`

  ```
95:PREP_TEMPS = frozenset("""
96-pendant depuis durant avant apres après des dès jusqu'à jusqua during since before after
97-""".split())
98-PREP_MOYEN = frozenset("avec with".split())
--
110:PREP_CONNUES = (PREP_TEMPS | PREP_MOYEN | PREP_BUT | PREP_POSSESSION | PREP_DEST
111-                | PREP_LIEU | frozenset(PREP_AUTRES) | frozenset({"en", "par", "by"}))
112-
113-# Mots qui ressemblent à un infinitif mais n'en sont pas (noms en -er/-ir/-re).
--
247:    if base in PREP_TEMPS:
248-        return "temps"
249-    if base in PREP_MOYEN:
250-        return "moyen"
['after', 'apres', 'après', 'avant', 'before', 'depuis', 'des', 'durant', 'during', 'dès', "jusqu'à", 'jusqua', 'pendant', 'since']
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py", "old_string": "pendant depuis durant avant apres après des dès jusqu'à jusqua during since before after", "new_string": "pendant depuis durant avant apres après dès jusqu'à jusqua during since before after"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_gp.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nimport tools.restitution_v3 as v3\ng=v3.mesurer_gold_analyseur_v3()\nprint('justes',g['base']['justes'],'/',g['base']['total'],g['base']['taux'])\nprint('cinq',g['base']['cinq_roles']['justes'],'/',g['base']['cinq_roles']['attendus' … [659 caractères tronqués]`

  ```
justes 144 / 144 1.0
cinq 18 / 18 P 1.0 R 1.0 F1 1.0
lieu {'attendus': 3, 'predits': 3, 'justes': 3, 'precision': 1.0, 'rappel': 1.0, 'f1': 1.0}
temps {'attendus': 9, 'predits': 9, 'justes': 9, 'precision': 1.0, 'rappel': 1.0, 'f1': 1.0}
destinataire {'attendus': 5, 'predits': 5, 'justes': 5, 'precision': 1.0, 'rappel': 1.0, 'f1': 1.0}
possession {'attendus': 1, 'predits': 1, 'justes': 1, 'precision': 1.0, 'rappel': 1.0, 'f1': 1.0}
complement {'attendus': 0, 'predits': 0, 'justes': 0, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0}
perm cinq 0 18 0.0
perm tous taux 0.4028 cinq 0
constant lieu 0.0208 3
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "old_string": "    c = collections.Counter()\n    if not rendu:\n        return {}\n    for s in rendu.get(\"segments\", []):\n        if s.get(\"type\") == \"GP\":\n            c[roles_gp.normaliser_role(s.get( … [372 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 728, "limit": 100}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
728: def cmd_restituer(args: argparse.Namespace) -> int:
729:     """Reconstruit la surface depuis l'annotation et rend la fidélité du miroir.
730: 
731:     Deux modes : un **texte** (ou un fichier), ou un **banc** JSON de textes
732:     (`--banc`, le format de `reports/pensee-fiabilite-produit.json`). Le mode banc
733:     laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`
734:     ajoute la **forme canonique v1** (segments + rôles + cibles) et son miroir ;
735:     `--roles` ajoute la **v2** (agent, prédicat, lieu) et, sur un banc, sa fidélité à
736:     l'or. La sortie de la v0 reste celle par défaut.
737:     """
738:     if args.roles and args.canonique:
739:         print(f"{NOM}: erreur d'usage : --roles et --canonique sont exclusifs",
740:               file=sys.stderr)
741:         return 2
742:     if args.gold and not (args.banc and args.roles):
743:         print(f"{NOM}: erreur d'usage : --gold ne sert qu'avec --banc --roles",
744:               file=sys.stderr)
745:         return 2
746:     if args.banc:
747:         if args.texte is n
… [3685 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"import tools.restitution\\|import restitution\" tools/drave.py | head -20", "description": "Find restitution imports in drave"}`

  ```
54:import restitution  # noqa: E402  (la restitution v0 : annotation → surface)
55:import restitution_v2  # noqa: E402  (la restitution v2 : les rôles)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 48, "limit": 12}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
48: sys.path.insert(0, ".")
49: RACINE = pathlib.Path(__file__).resolve().parent.parent
50: sys.path.insert(0, str(RACINE / "tools"))
51: sys.path.insert(0, str(RACINE))
52: 
53: import bloc_linguistique as bl  # noqa: E402  (import après l'installation des chemins)
54: import restitution  # noqa: E402  (la restitution v0 : annotation → surface)
55: import restitution_v2  # noqa: E402  (la restitution v2 : les rôles)
56: 
57: NOM = "drave"
58: VERSION = "0.1.0"
59: LARGEUR = 100

(Showing lines 48-59 of 1008. Use offset=60 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "import restitution  # noqa: E402  (la restitution v0 : annotation → surface)\nimport restitution_v2  # noqa: E402  (la restitution v2 : les rôles)", "new_string": "import restitution  # noqa: E402  (la res … [184 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    `--roles` ajoute la **v2** (agent, prédicat, lieu) et, sur un banc, sa fidélité à\n    l'or. La sortie de la v0 reste celle par défaut.\n    \"\"\"\n    if args.roles and args.canonique:\n        print … [1341 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "        if args.roles:\n            chemin_gold = pathlib.Path(args.gold or restitution_v2.GOLD_DEFAUT)\n            try:\n                gold = json.loads(chemin_gold.read_text(encoding=\"utf-8\"))\n     … [2332 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    if args.roles:\n        mesure_v2 = restitution_v2.mesurer_annotation_v2(annotation, texte)", "new_string": "    if args.roles_v3:\n        mesure_v3 = restitution_v3.mesurer_annotation_v3(annotation,  … [431 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 965, "limit": 35}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
965:     rejouer.add_argument("--langue", choices=("fr", "en"), default=None,
966:                          help="indice de langue (fr/en) ; sans lui, le bloc détecte")
967:     rejouer.set_defaults(fonction=cmd_rejouer)
968: 
969:     restituer = sous.add_parser(
970:         "restituer",
971:         help="reconstruire la surface depuis l'annotation et mesurer le miroir",
972:         description="Analyse un texte, reconstruit la surface depuis le niveau `graphème` "
973:                     "(sans lire le champ `texte` de l'annotation) et compare à la source. "
974:                     "Affiche la fidélité binaire du miroir, la fidélité de caractères et un "
975:                     "contrôle négatif. Avec --canonique, produit en plus la forme canonique v1 "
976:                     "(segments + rôles + cibles) et son miroir canonique ; avec --roles, produit "
977:                     "la forme lisible des rôles (agent, prédicat, lieu) et, sur un banc, leur "
978:                     "fidélité à un or écrit à la main.",
979:         epilog="Exemples : python3 tools/drave.py re
… [1682 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "                    \"(segments + rôles + cibles) et son miroir canonique ; avec --roles, produit \"\n                    \"la forme lisible des rôles (agent, prédicat, lieu) et, sur un banc, leur \"\n     … [1310 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    restituer.add_argument(\"--roles\", action=\"store_true\",\n                           help=\"ajouter la forme lisible des rôles (agent, prédicat, lieu) ; \"\n                                \"avec --b … [1061 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/drave.py restituer \"Le voyage à Paris dure deux heures.\" --roles-v3; echo \"EXIT=$?\"", "description": "Test v3 CLI text output"}`

  ```
restitution v3 (rôles de GP)
source          : 'Le voyage à Paris dure deux heures.'
cadre principal :
  agent         : —
  prédicat      : —
  lieu          : —
segments de rôle: 2 (1 agents, 0 prédicats, 1 lieux)

rôles (agent, prédicat, lieu)
  agent     : —
  prédicat  : —
  lieu      : —
segments de rôle : 2
   1. GN/agent [0:9] « Le voyage » → —
   2. GP/lieu [10:34] « à Paris dure deux heures » → voyage

rôles de GP (v3) : lieu: 1

restitution du rendu : exacte (relire_roles(rendre_roles(a)))
contrôle négatif      : retrait non détecté · permutation non détectée · détecté False
EXIT=0
  ```

- **bash** `{"command": "python3 tools/drave.py restituer \"Le chat dort.\" --roles | head -20; echo \"EXIT=$?\"", "description": "Verify v2 CLI unchanged"}`

  ```
restitution v2 (rôles)
source          : 'Le chat dort.'
cadre principal :
  agent         : Le chat
  prédicat      : dort
  lieu          : —
segments de rôle: 2 (1 agents, 1 prédicats, 0 lieux)

rôles (agent, prédicat, lieu)
  agent     : Le chat
  prédicat  : dort
  lieu      : —
segments de rôle : 2
   1. GN/agent [0:7] « Le chat » → dort
   2. GV/predicat [8:12] « dort » → chat

restitution du rendu : exacte (relire_roles(rendre_roles(a)))
contrôle négatif      : retrait détecté · permutation détectée · détecté True
EXIT=0
  ```

- **bash** `{"command": "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --roles-v3 | head -35; echo \"EXIT=$?\"", "description": "Test v3 CLI bank output"}`

  ```
restitution v3 — les rôles de GP — banc reports/pensee-fiabilite-produit.json
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

cadre principal (agent, prédicat, lieu)
  cadres exacts                20/46       0.4348
  dont non vides               17/46     (0.3696) · vides 3
  rôles exacts                93/138      0.6739
  justes / attendus           40/77    
  précision / rappel / F1 0.5634 / 0.5195 / 0.5406

par rôle                  exacts    attendus   prédits   justes   préc.   rappel
  agent                     29/46         32        28       18  0.6429   0.5625
  prédicat                  22/46         39        39       19  0.4872   0.4872
  lieu                      42/46          6         4        3  0.7500   0.5000

rôles de GP lus : {'agent': 1, 'but': 7, 'destinataire': 6, 'lieu': 10, 'maniere': 3, 'moyen': 5, 'possession': 5, 'temps': 13, 'theme': 17}
segments de rôle 194 · agents 41 · prédicats 143 · lieux 10 · cadres 139
restitution du rendu     : 46/46 (1.0000)
contrôle vide            : 7/46 cadres exacts
contrôle constant (type) : 6/46 cadres exacts
contrôle rôles mélangés  : 3/46 cadres exacts
contrôle négatif rendu   : 39/39 éligibles détectés
EXIT=
… [1 caractères tronqués]
  ```

- **bash** `{"command": "for t in \"Le train part à 14 h.\" \"Il parle à Marie de son projet.\" \"Le chat de la voisine dort sur le toit.\" \"Le livre est à moi.\" \"The cat sleeps on the roof.\" \"The quick brown fox jumps over the lazy dog.\"; do echo \"=== $t\"; python3 tools/drave.py restituer \"$t\" --role … [78 caractères tronqués]`

  ```
=== Le train part à 14 h.
restitution v3 (rôles de GP)
source          : 'Le train part à 14 h.'
cadre principal :
  agent         : Le train
  prédicat      : part
  lieu          : —
segments de rôle: 2 (1 agents, 1 prédicats, 0 lieux)

rôles (agent, prédicat, lieu)
  agent     : Le train
  prédicat  : part
  lieu      : —
  autres    : temps: à 14 h
segments de rôle : 2
   1. GN/agent [0:8] « Le train » → part
   2. GV/predicat [9:13] « part » → train

rôles de GP (v3) : temps: 1
=== Il parle à Marie de son projet.
restitution v3 (rôles de GP)
source          : 'Il parle à Marie de son projet.'
cadre principal :
  agent         : Il
  prédicat      : parle
  lieu          : —
segments de rôle: 2 (1 agents, 1 prédicats, 0 lieux)

rôles (agent, prédicat, lieu)
  agent     : Il
  prédicat  : parle
  lieu      : —
  autres    : destinataire: à Marie de son projet · theme: de son projet
segments de rôle : 2
   1. GN/agent [0:2] « Il » → parle
   2. GV/predicat [3:8] « parle » → —

rôles de GP (v3) : destinataire: 1 · theme: 1
=== Le chat de la voisine dort sur le toit.
restitution v3 (rôles de GP)
source          : 'Le chat de la voisine dort sur le toit.'
cadre principal :
  agent  
… [2070 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "offset": 62, "limit": 32}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py</path>
<type>file</type>
<content>
62:     if not m:
63:         return "", texte
64:     return m.group(1), texte[m.end():]
65: 
66: 
67: def preparer_annotation(a: bl.Annotation, source: str) -> bl.Annotation:
68:     """Dédoublonne les GP de même début (garde le plus long) et applique les rôles v3.
69: 
70:     Le dédoublonnage est nécessaire parce que l'union S + chunker produit parfois deux GP
71:     au même début (`vers` et `vers 9 h`) : le plus court est un préfixe, pas une lecture
72:     concurrente. Le rôle est recalculé avec le contexte (le syntagme précédent, ce qui
73:     suit la préposition). Les GP qui ne commencent pas par une préposition connue
74:     (`hier`, `demain`) gardent le rôle que l'analyseur leur a donné.
75:     """
76:     segs = [e for e in a.etiquettes if e.niveau == "syntagme"]
77:     par_debut: dict[int, bl.Etiquette] = {}
78:     for e in segs:
79:         if e.type != "GP":
80:             continue
81:         if e.debut not in par_debut or e.fin > par_debut[e.debut].fin:
82:             par_debut[e.debut] = e
83:     garder = {id(e) for e in par_debut.values()}
84: 
… [503 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "old_string": "def preparer_annotation(a: bl.Annotation, source: str) -> bl.Annotation:\n    \"\"\"Dédoublonne les GP de même début (garde le plus long) et applique les rôles v3.\n\n    Le dédoublonnage est néce … [2074 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys; sys.path.insert(0,'.')\nimport tools.restitution as r, tools.restitution_v3 as v3\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nm=v3.mesurer_banc_v3(r.items_b … [553 caractères tronqués]`

  ```
cadres 20 non vides 17 roles 40 / 77 F1 0.5406
lieu {'exacts': 42, 'attendus': 6, 'predits': 4, 'justes': 3, 'faux_positifs': 1, 'faux_negatifs': 3, 'vrais_negatifs': 39, 'taux_exact': 0.913, 'precision': 0.75, 'rappel': 0.5, 'f1': 0.6}
gp {'agent': 1, 'but': 7, 'destinataire': 6, 'lieu': 10, 'maniere': 3, 'moyen': 5, 'possession': 5, 'temps': 13, 'theme': 17} spans {'justes': 194, 'total': 194, 'taux': 1.0}
goldS 144 / 144 cinq 18 / 18
  ```

- **bash** `{"command": "for t in \"Le chat de la voisine dort sur le toit.\" \"Il parle à Marie de son projet.\" \"Le train part à 14 h.\"; do echo \"=== $t\"; python3 tools/drave.py restituer \"$t\" --roles-v3 | sed -n '1,16p'; done", "description": "Check CLI spans after dedupe fix"}`

  ```
=== Le chat de la voisine dort sur le toit.
restitution v3 (rôles de GP)
source          : 'Le chat de la voisine dort sur le toit.'
cadre principal :
  agent         : Le chat
  prédicat      : dort
  lieu          : sur le toit
segments de rôle: 3 (1 agents, 1 prédicats, 1 lieux)

rôles (agent, prédicat, lieu)
  agent     : Le chat
  prédicat  : dort
  lieu      : sur le toit
  autres    : possession: de la voisine
segments de rôle : 3
   1. GN/agent [0:7] « Le chat » → dort
   2. GV/prédicat [22:26] « dort » → —
=== Il parle à Marie de son projet.
restitution v3 (rôles de GP)
source          : 'Il parle à Marie de son projet.'
cadre principal :
  agent         : Il
  prédicat      : parle
  lieu          : —
segments de rôle: 2 (1 agents, 1 prédicats, 0 lieux)

rôles (agent, prédicat, lieu)
  agent     : Il
  prédicat  : parle
  lieu      : —
  autres    : destinataire: à Marie · theme: de son projet
segments de rôle : 2
   1. GN/agent [0:2] « Il » → parle
   2. GV/predicat [3:8] « parle » → —
=== Le train part à 14 h.
restitution v3 (rôles de GP)
source          : 'Le train part à 14 h.'
cadre principal :
  agent         : Le train
  prédicat      : part
  lieu          : —
seg
… [270 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys; sys.path.insert(0,'.')\nimport tools.restitution as r, tools.restitution_v3 as v3\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nc=v3.controler_banc_v3(r.items … [640 caractères tronqués]`

  ```
vide cadres 7 roles justes 0 / 77 F1 0.0
constant_par_type cadres 6 roles justes 39 / 77 F1 0.4382
melange cadres 3 roles justes 0 / 77 F1 0.0
permutation mapping {'lieu': 'temps', 'temps': 'destinataire', 'destinataire': 'possession', 'possession': 'complement', 'complement': 'lieu'}
permutation cadres 20 non vides 17 roles justes 40 / 77 P 0.5634 R 0.5195 F1 0.5406
permutation lieu {'exacts': 42, 'attendus': 6, 'predits': 4, 'justes': 3, 'faux_positifs': 1, 'faux_negatifs': 3, 'vrais_negatifs': 39, 'taux_exact': 0.913, 'precision': 0.75, 'rappel': 0.5, 'f1': 0.6}
base {'exacts': 20, 'taux': 0.4348, 'exacts_non_vides': 17, 'exacts_vides': 3, 'partiels': 43, 'partiels_taux': 0.9348, 'exacts_stricts': 17, 'taux_strict': 0.3696, 'roles_exacts_moyens': 2.0217}
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "offset": 128, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py</path>
<type>file</type>
<content>
128:                 e.meta["role_v3"] = True
129: 
130: 
131: # --------------------------------------------------------------------------- mesure texte
132: 
133: 
134: def mesurer_annotation_v3(a: bl.Annotation, source: str,
135:                           gold: dict | None = None) -> dict:
136:     """La mesure v3 d'une annotation : mêmes champs que la v2, rôles préparés en v3."""
137:     preparer_annotation(a, source)
138:     m = v2.mesurer_annotation_v2(a, source, gold)
139:     m["schema"] = SCHEMA
140:     m["version"] = VERSION
141:     m["roles_gp"] = _distribution_gp(m["roles"])
142:     return m
143: 
144: 
145: def _distribution_gp(rendu: dict | None) -> dict:
146:     """La distribution des rôles de GP lus (pas jugés)."""
147:     c = collections.Counter()
148:     if not rendu:
149:         return {}
150:     for s in list(rendu.get("segments", [])) + list(rendu.get("autres", [])):
151:         if s.get("type") == "GP":
152:             c[roles_gp.normaliser_role(s.get("role", ""))] += 1
153:     return dict(sorted(c.items()))
154: 
155: 
156: # ---------
… [156 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "offset": 158, "limit": 22}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py</path>
<type>file</type>
<content>
158: 
159: def _resultat_v3(a, source, ident, attendu, langue=None) -> dict:
160:     m = mesurer_annotation_v3(a, source, attendu)
161:     return {
162:         "id": ident,
163:         "refus": "",
164:         "langue": a.langue,
165:         "caracteres": len(source),
166:         "or_variantes": (attendu or {}).get("variantes"),
167:         "roles": m["roles"],
168:         "roles_gp": m["roles_gp"],
169:         "comparaison": m["comparaison"],
170:         "comparaison_stricte": m["comparaison_stricte"],
171:         "constant_par_type": m["constant_par_type"],
172:         "vide": m["vide"],
173:         "melange": m["melange"],
174:         "rendu": m["rendu"],
175:         "controle_negatif_rendu": m["controle_negatif_rendu"],
176:         "spans_dans_source": m["spans_dans_source"],
177:     }
178: 
179: 

(Showing lines 158-179 of 518. Use offset=180 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "old_string": "def _resultat_v3(a, source, ident, attendu, langue=None) -> dict:\n    m = mesurer_annotation_v3(a, source, attendu)\n    return {\n        \"id\": ident,\n        \"refus\": \"\",\n        \"lang … [882 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys; sys.path.insert(0,'.')\nimport tools.restitution as r, tools.restitution_v3 as v3\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nc=v3.controler_banc_v3(r.items … [703 caractères tronqués]`

  ```
vide cadres 7 roles justes 0 / 77 F1 0.0
constant_par_type cadres 6 roles justes 39 / 77 F1 0.4382
melange cadres 3 roles justes 0 / 77 F1 0.0
permutation cadres 17 non vides 14 roles justes 37 / 77 P 0.5522 R 0.4805 F1 0.5139
permutation lieu {'exacts': 40, 'attendus': 6, 'predits': 0, 'justes': 0, 'faux_positifs': 0, 'faux_negatifs': 6, 'vrais_negatifs': 40, 'taux_exact': 0.8696, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0}
base cadres 20 non vides 17 F1 0.5406
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-restitution-v2.json'))\nprint(d['schema'],d['version'],d['date'])\nprint('synthese keys',list(d['synthese'].keys()))\nprint('cadre',d['synthese']['cadre'])\nprint('roles',d['synthese']['roles']['justes'],d['synthese']['rol … [158 caractères tronqués]`

  ```
drave.restitution.v2.banc 1 2026-11-15
synthese keys ['n', 'annotations', 'refus', 'refus_ids', 'or', 'cadre', 'or_textes', 'roles', 'couverture', 'controles']
cadre {'exacts': 19, 'taux': 0.413, 'exacts_non_vides': 16, 'exacts_vides': 3, 'partiels': 42, 'partiels_taux': 0.913, 'exacts_stricts': 16, 'taux_strict': 0.3478, 'roles_exacts_moyens': 1.9783}
roles 39 77 0.527
externe {'or': 'tools/structures/donnees/gold-analyseur.json', 'phrases': 61, 'roles_justes': 139, 'roles_total': 144, 'taux': 0.9653, 'baseline_role_constant': {'justes': 104, 'total': 144, 'taux': 0.7222}, 'par_type': {'GN': 36, 'GP': 23, 'GV': 58, 'REL': 7, 'SUB': 20}, 'definition': 'appariement par recouvrement maximal à type égal, puis comparaison du rôle normalisé (prédicat/predicat)'}
  ```

- **bash** `{"command": "date -I", "description": "Check system date"}`

  ```
2026-11-15
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "offset": 240, "limit": 42}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py</path>
<type>file</type>
<content>
240:         "permutation_gp": {
241:             "mapping": cycle,
242:             "synthese": permute["synthese"],
243:         },
244:     }
245: 
246: 
247: # --------------------------------------------------------------------------- gold S
248: 
249: 
250: def apparier(segments: list[dict], gold_spans: list[dict]) -> dict[int, int]:
251:     """Apparie chaque span d'or à un span prédit : recouvrement max, puis le plus court.
252: 
253:     L'ancien appariement prenait le premier span à recouvrement maximal. Sur `à Marie de
254:     son projet`, le GP long et le GP court ont le même recouvrement : le premier choisi
255:     était le long, et le thème était perdu. Ici, à recouvrement égal, le span **le plus
256:     court** gagne (le plus précis), puis l'or le plus court, puis l'indice le plus petit.
257:     """
258:     paires = []
259:     for gi, g in enumerate(gold_spans):
260:         for pi, p in enumerate(segments):
261:             if p["type"] != g["type"]:
262:                 continue
263:             inter = min(g["fin"], p["fin"]) - max(g["debut"], p["
… [694 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "old_string": "def apparier(segments: list[dict], gold_spans: list[dict]) -> dict[int, int]:\n    \"\"\"Apparie chaque span d'or à un span prédit : recouvrement max, puis le plus court.\n\n    L'ancien apparieme … [3462 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "offset": 375, "limit": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py</path>
<type>file</type>
<content>
375: def mesurer_gold_analyseur_v3(chemin: pathlib.Path | None = None) -> dict:
376:     """La mesure **par rôle** sur le gold S (61 phrases, 144 rôles).
377: 
378:     Le même appariement que la v2, mais par rôle et avec le tie-break du span le plus
379:     court. Les contrôles négatifs permutent les rôles prédits, sans toucher aux spans.
380:     """
381:     chemin = chemin or GOLD_ANALYSEUR
382:     donnees = json.loads(chemin.read_text(encoding="utf-8"))
383:     h = bl.Heuristique()
384:     paires: list[dict] = []
385:     par_phrase = []
386:     for phrase in donnees.get("phrases", []):
387:         a = h.analyser(phrase["texte"])
388:         if a.refus:
389:             continue
390:         preparer_annotation(a, phrase["texte"])
391:         segments = v2._segments_syntagmes(a)
392:         gold_spans = v2._spans_gold(phrase)
393:         app = apparier(segments, gold_spans)
394:         justes = 0
395:         for gi, g in enumerate(gold_spans):
396:             pred = segments[app[gi]]["role"] if gi in app else ""
397:             paires.append({"or": g["
… [1654 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "old_string": "def mesurer_gold_analyseur_v3(chemin: pathlib.Path | None = None) -> dict:\n    \"\"\"La mesure **par rôle** sur le gold S (61 phrases, 144 rôles).\n\n    Le même appariement que la v2, mais par r … [1709 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "offset": 413, "limit": 32}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py</path>
<type>file</type>
<content>
413:     paires_type = [{"or": p["or"], "predit": ROLE_CONSTANT.get(p["type"], ""), "type": p["type"]}
414:                    for p in paires]
415:     base_type = _agreger_paires(paires_type)
416:     return {
417:         "or": str(chemin.relative_to(RACINE)),
418:         "phrases": len(donnees.get("phrases", [])),
419:         "roles": len(paires),
420:         "apparies": sum(1 for p in par_phrase if p["apparies"] == p["roles"]),
421:         "par_phrase": par_phrase,
422:         "base": base,
423:         "baseline_role_constant": {
424:             "justes": base_type["justes"], "total": base_type["total"],
425:             "taux": base_type["taux"], "par_role": base_type["par_role"],
426:         },
427:         "role_constant_lieu": _agreger_paires(paires, constant),
428:         "permutation_cinq": {
429:             "mapping": cycle,
430:             "mesure": _agreger_paires(paires, cycle),
431:         },
432:         "permutation_tous": {
433:             "mapping": tous,
434:             "mesure": _agreger_paires(paires, tous),
435:         },
436:      
… [410 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "old_string": "    return {\n        \"or\": str(chemin.relative_to(RACINE)),\n        \"phrases\": len(donnees.get(\"phrases\", [])),\n        \"roles\": len(paires),\n        \"apparies\": sum(1 for p in par_p … [339 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nimport tools.restitution_v3 as v3\nfor a in ['v2','v3']:\n    g=v3.mesurer_gold_analyseur_v3(appariement=a)\n    c=g['base']['cinq_roles']\n    print(a,'global',g['base']['justes'],'/',g['base']['total'],'taux',g['base']['taux'],'ci … [326 caractères tronqués]`

  ```
v2 global 143 / 144 taux 0.9931 cinq 18 / 18 P 0.9474 R 1.0 F1 0.973
    lieu 3 3 3 1.0 1.0
    temps 9 9 9 1.0 1.0
    destinataire 5 5 5 1.0 1.0
    possession 1 1 1 1.0 1.0
    complement 0 1 0 0.0 0.0
v3 global 144 / 144 taux 1.0 cinq 18 / 18 P 1.0 R 1.0 F1 1.0
    lieu 3 3 3 1.0 1.0
    temps 9 9 9 1.0 1.0
    destinataire 5 5 5 1.0 1.0
    possession 1 1 1 1.0 1.0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "offset": 375, "limit": 28}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py</path>
<type>file</type>
<content>
375: def mesurer_gold_analyseur_v3(chemin: pathlib.Path | None = None,
376:                               appariement: str = "v3") -> dict:
377:     """La mesure **par rôle** sur le gold S (61 phrases, 144 rôles).
378: 
379:     `appariement="v3"` utilise le tie-break du span le plus court ; `appariement="v2"`
380:     garde l'ancien appariement, pour séparer le gain de rôles du gain d'appariement.
381:     Les contrôles négatifs permutent les rôles prédits, sans toucher aux spans.
382:     """
383:     fonction = apparier_v2 if appariement == "v2" else apparier
384:     chemin = chemin or GOLD_ANALYSEUR
385:     donnees = json.loads(chemin.read_text(encoding="utf-8"))
386:     h = bl.Heuristique()
387:     paires: list[dict] = []
388:     par_phrase = []
389:     for phrase in donnees.get("phrases", []):
390:         a = h.analyser(phrase["texte"])
391:         if a.refus:
392:             continue
393:         preparer_annotation(a, phrase["texte"])
394:         segments = v2._segments_syntagmes(a)
395:         gold_spans = v2._spans_gold(phrase)
396:         app = fon
… [466 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "old_string": "def mesurer_gold_analyseur_v3(chemin: pathlib.Path | None = None,\n                              appariement: str = \"v3\") -> dict:\n    \"\"\"La mesure **par rôle** sur le gold S (61 phrases, 14 … [1883 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py", "old_string": "        \"or\": str(chemin.relative_to(RACINE)),\n        \"appariement\": appariement,\n        \"phrases\": len(donnees.get(\"phrases\", [])),", "new_string": "        \"or\": str(chemin.relativ … [144 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v3.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nimport tools.restitution_v3 as v3\nfor prep in [False, True]:\n  for app in ['v2','v3']:\n    g=v3.mesurer_gold_analyseur_v3(appariement=app, preparer=prep)\n    c=g['base']['cinq_roles']\n    print(f\"prepare={prep} app={app} globa … [348 caractères tronqués]`

  ```
prepare=False app=v2 global=139/144 cinq=17/18 P=0.85 R=0.9444 F1=0.8947
    lieu 3 3 3
    temps 9 9 9
    destinataire 5 5 4
    possession 1 2 1
    complement 0 1 0
prepare=False app=v3 global=142/144 cinq=18/18 P=0.9474 R=1.0 F1=0.973
    lieu 3 3 3
    temps 9 9 9
    destinataire 5 5 5
    possession 1 2 1
prepare=True app=v2 global=143/144 cinq=18/18 P=0.9474 R=1.0 F1=0.973
    lieu 3 3 3
    temps 9 9 9
    destinataire 5 5 5
    possession 1 1 1
    complement 0 1 0
prepare=True app=v3 global=144/144 cinq=18/18 P=1.0 R=1.0 F1=1.0
    lieu 3 3 3
    temps 9 9 9
    destinataire 5 5 5
    possession 1 1 1
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl, tools.restitution_v2 as v2, tools.restitution_v3 as v3, tools.roles_gp as rg\nd=json.load(open('tools/structures/donnees/gold-analyseur.json'))\nh=bl.Heuristique()\nfor prep in [False,True] … [553 caractères tronqués]`

  ```
--- prepare False
  p002 gold instrument 'avec le télescope' pred attribut 'avec le télescope'
  p005 gold theme 'de son projet' pred destinataire 'à Marie de son projet'
  g019 gold destinataire 'à Marie' pred theme 'de son projet à Marie'
  h056 gold consequence 'que la maison tremble' pred complément 'si fort que la maison tremble'
  h060 gold theme 'des bonds' pred possession 'des bonds'
--- prepare True
  h056 gold consequence 'que la maison tremble' pred complément 'si fort que la maison tremble'
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys; sys.path.insert(0,'.')\nimport tools.restitution_v3 as v3\ng=v3.mesurer_gold_analyseur_v3()\nprint('base',g['base']['justes'],'/',g['base']['total'],g['base']['taux'])\nprint('cinq',g['base']['cinq_roles']['justes'],'/',g['base']['cinq_roles']['attend … [818 caractères tronqués]`

  ```
base 144 / 144 1.0
cinq 18 / 18 1.0 1.0 1.0
baseline type 104 0.7222
constant lieu global 3 0.0208 cinq {'roles': ['lieu', 'temps', 'destinataire', 'possession', 'complement'], 'attendus': 18, 'predits': 144, 'justes': 3, 'precision': 0.0208, 'rappel': 0.1667, 'f1': 0.037, 'par_role': {'lieu': {'attendus': 3, 'predits': 144, 'justes': 3, 'precision': 0.0208, 'rappel': 1.0, 'f1': 0.0408}, 'temps': {'attendus': 9, 'predits': 0, 'justes': 0, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0}, 'destinataire': {'attendus': 5, 'predits': 0, 'justes': 0, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0}, 'possession': {'attendus': 1, 'predits': 0, 'justes': 0, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0}, 'complement': {'attendus': 0, 'predits': 0, 'justes': 0, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0}}}
perm cinq global 0.875 cinq 0 0.0
perm tous global 0.4028 cinq 0 0.0
par role
  agent          34 34 34 P1.0000 R1.0000 F11.0000
  but             3  3  3 P1.0000 R1.0000 F11.0000
  cause           4  4  4 P1.0000 R1.0000 F11.0000
  concession      1  1  1 P1.0000 R1.0000 F11.0000
  consequence     1  1  1 P1.0000 R1.0000 F11.0000
  contenu         5  5  5 P1.0000 R1.0000 F11.0000
  destinataire    5
… [541 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_restitution_v3.py", "content": "#!/usr/bin/env python3\n\"\"\"mesurer_restitution_v3.py — produit le JSON de la fiche W5 (restitution v3).\n\nMesure la **restitution v3** — les rôles des groupes prépositionnels — sur les de … [13332 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_restitution_v3.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/mesurer_restitution_v3.py; echo \"EXIT=$?\"", "description": "Generate v3 JSON"}`

  ```
restitution v3 — les rôles de GP — banc reports/pensee-fiabilite-produit.json
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

cadre principal (agent, prédicat, lieu)
  cadres exacts                20/46       0.4348
  dont non vides               17/46     (0.3696) · vides 3
  rôles exacts                93/138      0.6739
  justes / attendus           40/77    
  précision / rappel / F1 0.5634 / 0.5195 / 0.5406

par rôle                  exacts    attendus   prédits   justes   préc.   rappel
  agent                     29/46         32        28       18  0.6429   0.5625
  prédicat                  22/46         39        39       19  0.4872   0.4872
  lieu                      42/46          6         4        3  0.7500   0.5000

rôles de GP lus : {'agent': 1, 'but': 7, 'destinataire': 6, 'lieu': 10, 'maniere': 3, 'moyen': 5, 'possession': 5, 'temps': 13, 'theme': 17}
segments de rôle 194 · agents 41 · prédicats 143 · lieux 10 · cadres 139
restitution du rendu     : 46/46 (1.0000)
contrôle vide            : 7/46 cadres exacts
contrôle constant (type) : 6/46 cadres exacts
contrôle rôles mélangés  : 3/46 cadres exacts
contrôle négatif rendu   : 39/39 éligibles détectés

gold
… [187 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='reports/pensee-restitution-v3.json'\nd=json.load(open(p))\nprint('keys',list(d.keys()))\nprint('size',len(open(p,'rb').read()))\nprint('synthese cadre',d['synthese']['cadre'])\nprint('ref v2',json.dumps(d['reference_v2'],ensure_ascii=False)[:400])\npri … [336 caractères tronqués]`

  ```
keys ['schema', 'version', 'date', 'ligne', 'tache', 'titre', 'banc', 'banc_sha256', 'gold', 'gold_sha256', 'gold_s', 'gold_s_sha256', 'reference_v2', 'commande', 'dispositif', 'synthese', 'resultats', 'controles', 'gold_s_decoupage', 'separation', 'comparaison_v2_v3', 'limites']
size 633932
synthese cadre {'exacts': 20, 'taux': 0.4348, 'exacts_non_vides': 17, 'exacts_vides': 3, 'partiels': 43, 'partiels_taux': 0.9348, 'exacts_stricts': 17, 'taux_strict': 0.3696, 'roles_exacts_moyens': 2.0217}
ref v2 {"fichier": "reports/pensee-restitution-v2.json", "date": "2026-11-15", "banc": {"cadres_exacts": 19, "exacts_non_vides": 16, "roles_justes": 39, "roles_attendus": 77, "precision": 0.5493, "rappel": 0.5065, "f1": 0.527, "par_role": {"agent": {"exacts": 29, "attendus": 32, "predits": 28, "justes": 18, "faux_positifs": 10, "faux_negatifs": 14, "vrais_negatifs": 11, "taux_exact": 0.6304, "precision":
comparaison {"v2_roles_v2_appariement": {"global": "139/144", "cinq": "17/18", "f1_cinq": 0.8947, "par_role": {"agent": {"attendus": 34, "predits": 34, "justes": 34, "precision": 1.0, "rappel": 1.0, "f1": 1.0}, "attribut": {"attendus": 0, "predits": 1, "justes": 0, "precision": 0.0, "rappel":
… [1061 caractères tronqués]
  ```

- **bash** `{"command": "python3 -m unittest tools.tests.test_restitution_v2 -v 2>&1 | tail -30", "description": "Run existing v2 tests"}`

  ```
test_banc_roles_json (tools.tests.test_restitution_v2.TestCommandeRoles.test_banc_roles_json) ... ok
test_gold_sans_banc_refuse (tools.tests.test_restitution_v2.TestCommandeRoles.test_gold_sans_banc_refuse) ... ok
test_restituer_roles (tools.tests.test_restitution_v2.TestCommandeRoles.test_restituer_roles) ... ok
test_restituer_roles_json (tools.tests.test_restitution_v2.TestCommandeRoles.test_restituer_roles_json) ... ok
test_roles_et_canonique_exclusifs (tools.tests.test_restitution_v2.TestCommandeRoles.test_roles_et_canonique_exclusifs) ... ok
test_gold_analyseur (tools.tests.test_restitution_v2.TestGoldExterne.test_gold_analyseur) ... ok
test_sans_or (tools.tests.test_restitution_v2.TestMesureSansOr.test_sans_or) ... ok
test_cas_connus (tools.tests.test_restitution_v2.TestOrEtBanc.test_cas_connus) ... ok
test_controles_v2 (tools.tests.test_restitution_v2.TestOrEtBanc.test_controles_v2) ... ok
test_or_46_textes (tools.tests.test_restitution_v2.TestOrEtBanc.test_or_46_textes) ... ok
test_roles_par_role (tools.tests.test_restitution_v2.TestOrEtBanc.test_roles_par_role) ... ok
test_synthese_v2 (tools.tests.test_restitution_v2.TestOrEtBanc.test_synthese_v2) ... ok
test_controle_nega
… [606 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\n# autotest role check\nfrom tools.pensee.autotest import *  # may run? avoid\nEOF\npython3 tools/bloc_linguistique.py --autotest 2>&1 | tail -10", "description": "Run bloc autotest"}`

  ```
"niveaux": true,
  "substitution": true,
  "parallele": true,
  "activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys; sys.path.insert(0,'.')\nimport tools.restitution as r, tools.restitution_v3 as v3\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nitems=r.items_banc(banc)\nm=v3 … [2162 caractères tronqués]`

  ```
BANK
cadre {'exacts': 20, 'taux': 0.4348, 'exacts_non_vides': 17, 'exacts_vides': 3, 'partiels': 43, 'partiels_taux': 0.9348, 'exacts_stricts': 17, 'taux_strict': 0.3696, 'roles_exacts_moyens': 2.0217}
roles {'exacts': 93, 'total': 138, 'justes': 40, 'attendus': 77, 'predits': 71, 'precision': 0.5634, 'rappel': 0.5195, 'f1': 0.5406, 'faux_positifs': 31, 'faux_negatifs': 37, 'vrais_negatifs': 53}
agent {'exacts': 29, 'attendus': 32, 'predits': 28, 'justes': 18, 'precision': 0.6429, 'rappel': 0.5625, 'f1': 0.6}
predicat {'exacts': 22, 'attendus': 39, 'predits': 39, 'justes': 19, 'precision': 0.4872, 'rappel': 0.4872, 'f1': 0.4872}
lieu {'exacts': 42, 'attendus': 6, 'predits': 4, 'justes': 3, 'precision': 0.75, 'rappel': 0.5, 'f1': 0.6}
couv {'textes_avec_role': 40, 'taux_textes_avec_role': 0.8696, 'segments_role': 194, 'agents': 41, 'predicats': 143, 'lieux': 10, 'cadres': 139, 'gp_roles': {'agent': 1, 'but': 7, 'destinataire': 6, 'lieu': 10, 'maniere': 3, 'moyen': 5, 'possession': 5, 'temps': 13, 'theme': 17}, 'cinq_roles': 34}
ctrl rendu {'exacts': 46, 'taux': 1.0}
ctrl neg {'eligibles': 39, 'sans_predicat': 39, 'permute': 39, 'detectes': 39}
ctrl spans {'justes': 194, 'total': 194
… [1639 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution_v3.py", "content": "#!/usr/bin/env python3\n\"\"\"test_restitution_v3.py — la restitution v3 (W5) : les rôles des GP.\n\nCe que le test fige :\n- `role_gp` sépare `lieu / temps / destinataire / possession / c … [17109 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution_v3.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 -m unittest tools.tests.test_restitution_v3 -v 2>&1 | tail -60", "description": "Run v3 tests"}`

  ```
test_controles (tools.tests.test_restitution_v3.TestBancV3.test_controles) ... ok
test_couverture_et_codec (tools.tests.test_restitution_v3.TestBancV3.test_couverture_et_codec) ... ok
test_par_role (tools.tests.test_restitution_v3.TestBancV3.test_par_role) ... ok
test_synthese (tools.tests.test_restitution_v3.TestBancV3.test_synthese) ... ok
test_mapping (tools.tests.test_restitution_v3.TestBancV3Negatif.test_mapping) ... ok
test_melange_des_trois (tools.tests.test_restitution_v3.TestBancV3Negatif.test_melange_des_trois) ... ok
test_permutation_des_cinq (tools.tests.test_restitution_v3.TestBancV3Negatif.test_permutation_des_cinq) ... ok
test_banc_v3_json (tools.tests.test_restitution_v3.TestCLI.test_banc_v3_json) ... ok
test_exclusifs (tools.tests.test_restitution_v3.TestCLI.test_exclusifs) ... ok
test_gold_avec_roles_v3 (tools.tests.test_restitution_v3.TestCLI.test_gold_avec_roles_v3) ... ok
test_roles_v2_inchange (tools.tests.test_restitution_v3.TestCLI.test_roles_v2_inchange) ... ok
test_roles_v3 (tools.tests.test_restitution_v3.TestCLI.test_roles_v3) ... ok
test_roles_v3_json (tools.tests.test_restitution_v3.TestCLI.test_roles_v3_json) ... ok
test_baseline_type (tools.tests.tes
… [1679 caractères tronqués]
  ```

### 🤖 Assistant

Les mesures sont stables. J'écris la fiche v3 avec le positif de séparation et le négatif produit.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v3.md", "content": "# B13 — la restitution v3 : les rôles des GP se séparent, la fidélité du cadre ne suit pas\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : W5 (J3 après-midi) · **Date** :\n> 202 … [21662 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v3.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v3.md", "old_string": "Le seul rôle de GP annoté dans les 46 textes est `lieu` (6 attendus). Les 34 GP lus par la\nv3 sur ce banc se répartissent en `lieu` 10, `temps` 13, `destinataire` 6, `possession` 5,\n`m … [429 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v3.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -60; echo \"EXIT=$?\"", "description": "Run documentation review"}`

  ```
revue de documentation · 753 fiche(s) · 846 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 752 fichiers, le disque en a 753
     · compteurs : en-cours.md dit 845 JSON, le disque en a 846
EXIT=0
  ```

- **bash** `{"command": "grep -n \"restitution\" reports/README.md reports/INDEX.md | head -20; echo ---; tail -20 reports/README.md; echo ---; head -30 reports/INDEX.md", "description": "Check reports index conventions"}`

  ```
reports/README.md:63:| [`rapport-restitution-v0.md`](rapport-restitution-v0.md) | **B13** — restitution v0 : **46/46** surfaces, miroir |
reports/README.md:64:| [`rapport-restitution-v1.md`](rapport-restitution-v1.md) | **B13** — restitution v1 : forme canonique **46/46** |
reports/README.md:65:| [`rapport-restitution-v2.md`](rapport-restitution-v2.md) | **B13** — restitution v2 : rôles **16/46**, F1 **0,5270** |
reports/README.md:214:- [`restitution-mesures.json`](restitution-mesures.json) · [`hybride-mesures.json`](hybride-mesures.json) ·
reports/INDEX.md:267:| [rapport-modules-famille.md](rapport-modules-famille.md) | C3.2b — un module de restitution par famille : l'indo-européen recopie à 100 % |
reports/INDEX.md:533:| [rapport-pensee-miroir-espaces.md](rapport-pensee-miroir-espaces.md) | B13 — la restitution avec les intervalles : 1,0, la perte était le rendu |
reports/INDEX.md:534:| [rapport-pensee-miroir-pos.md](rapport-pensee-miroir-pos.md) | B13 — la sortie POS : 0,201, la restitution sémantique ne restitue pas |
reports/INDEX.md:536:| [rapport-pensee-miroir-resume.md](rapport-pensee-miroir-resume.md) | B13 — la restitution sémantique : le résumé rappelle 78 % |
reports/IN
… [5128 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "offset": 58, "limit": 12}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
58: | [`rapport-etat-s.md`](rapport-etat-s.md) | **B13** — l'état de S : /paragraphes 19/19 |
59: | [`rapport-etat-r.md`](rapport-etat-r.md) | **B13** — l'état de R : tagger 0,8483/0,9440 |
60: | [`rapport-etat-n2.md`](rapport-etat-n2.md) | **B13** — l'état de N2 (porte propre, `porte-n2.sh`) |
61: | [`rapport-etat-a.md`](rapport-etat-a.md) | **B13** — l'état de A (frontière) |
62: | [`rapport-re-test-produit.md`](rapport-re-test-produit.md) | **B13** — re-test des 50 textes |
63: | [`rapport-restitution-v0.md`](rapport-restitution-v0.md) | **B13** — restitution v0 : **46/46** surfaces, miroir |
64: | [`rapport-restitution-v1.md`](rapport-restitution-v1.md) | **B13** — restitution v1 : forme canonique **46/46** |
65: | [`rapport-restitution-v2.md`](rapport-restitution-v2.md) | **B13** — restitution v2 : rôles **16/46**, F1 **0,5270** |
66: | [`rapport-pos-nombres.md`](rapport-pos-nombres.md) | **B13** — les nombres ont une POS (NUM) |
67: | [`rapport-partition-integree.md`](rapport-partition-integree.md) | **B13** — partition : alternatives étiquetées |
68: | [`rapport-partiti
… [270 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "old_string": "| [`rapport-restitution-v2.md`](rapport-restitution-v2.md) | **B13** — restitution v2 : rôles **16/46**, F1 **0,5270** |\n| [`rapport-pos-nombres.md`](rapport-pos-nombres.md) | **B13** — les nombres ont … [406 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/index_reports.py 2>&1 | tail -10; echo \"EXIT=$?\"; grep -n \"restitution-v3\" reports/INDEX.md", "description": "Regenerate reports index"}`

  ```
750 fiches → reports/INDEX.md
EXIT=0
696:| [rapport-restitution-v3.md](rapport-restitution-v3.md) | B13 — la restitution v3 : les rôles des GP se séparent, la fidélité du cadre ne suit pas |
  ```

- **bash** `{"command": "git diff --stat reports/INDEX.md; git diff reports/INDEX.md | head -40; echo ---; git status --short reports/ | head -20", "description": "Check index diff and untracked reports"}`

  ```
reports/INDEX.md | 4 +++-
 1 file changed, 3 insertions(+), 1 deletion(-)
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 03a54867..7e3867ec 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **748 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **750 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -400,6 +400,7 @@
 | [rapport-outillage-index.md](rapport-outillage-index.md) | B13 — l'outillage repris : `index_reports` a une aide, et l'index passe de 625 à 677 fiches |
 | [rapport-p0-flux.md](rapport-p0-flux.md) | P0 — Le harnais de flux : compter ce qu'on paie, par provenance |
 | [rapport-panini-334.md](rapport-panini-334.md) | J12.1 — Le §334 et les 44 œuvres : le retrieval et la prédiction de l'époque vs la filiation |
+| [rapport-panini-manifeste.md](rapport-panini-manifeste.md) | W4 — Panini : le manifeste des 26 signatures V14 et le rejeu disponible |
 | [rapport-pannes-nommees.md](rapport-pannes-nommees.md) | C11 — la panne du
… [1708 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"s-paragraphes\" reports/INDEX.md; echo \"count files:\"; ls reports/*.md | wc -l; grep -c '^| \\[' reports/INDEX.md", "description": "Check untracked report in index"}`

  ```
713:| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
count files:
753
750
  ```

- **bash** `{"command": "git show HEAD:reports/INDEX.md | grep -c \"s-paragraphes\\|panini-manifeste\\|restitution-v3\"; git show HEAD:reports/INDEX.md | grep \"s-paragraphes\\|panini-manifeste\\|restitution-v3\"", "description": "Check which entries were already in HEAD index"}`

  ```
1
| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
  ```

- **bash** `{"command": "sed -n '1,150p' docs/pilotage/en-cours.md", "description": "Read current state document"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 11 h 10 HNE (W4 : le manifeste Panini et le rejeu disponible)**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **État** : **en pause** depuis le 05/11 (dernier heartbeat) ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hoo
… [11252 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"restitution v3\\|restitution v2\\|B13\" docs/pilotage/roadmap.md | head -20", "description": "Locate roadmap restitution lines"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [10138 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '28,40p' docs/pilotage/roadmap.md; echo ====; sed -n '78,95p' docs/pilotage/roadmap.md", "description": "Read roadmap R row and B13 details"}`

  ```
| chantier | ce qu'il couvre | état | prochaine action |
|---|---|---|---|
| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** +
… [10936 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 1, "limit": 6}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 11 h 10 HNE (W4 : le manifeste Panini et le rejeu disponible)**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).

(Showing lines 1-6 of 144. Use offset=7 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 11 h 10 HNE (W4 : le manifeste Panini et le rejeu disponible)**", "new_string": "**Mis à jour : 2026-11-15, 11 h 40 HNE (W5 : la restitution v3 — les rôles des GP)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 50, "limit": 12}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
50: - **Ce qu'elle fait** : **session close** ; **`/paragraphes`** v7, **`/`** ancien arbre (369) ; **`s/v7`** à fusionner.
51: - **Ce que font les autres** : **hub**, **N2**, **Pensée**.
52: - **Prochaine action** : **migration `/` v7** (106/41) ; référents ; rétro-traduction.
53: - **Bloquants** : aucun ; 8765 pris (lancer 9000) ; migration = choix.
54: - **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).
55: 
56: ### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)*
57: 
58: - **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
59: - **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
60: - **Plan** : B13.
61: - **Stratégie** : v0.

(Showing lines 50-61 of 144. Use offset=62 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 62, "limit": 10}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
62: - **Ambition** : runtime tracé.
63: - **Objectif final** : moteur de pensée v0.
64: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; **D1–D3**, **E1–E2** livrés ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
65: - **Ce que font les autres** : **N2**, **S**, **hub**.
66: - **Ce qu'elle fait** : chantier.
67: - **Prochaine action** : **qualité des rôles** ; T132/T133, gold de pensée.
68: - **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
69: - **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).
70: 
71: ### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*

(Showing lines 62-71 of 144. Use offset=72 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; **D1–D3**, **E1–E2** livrés ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md … [1277 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 86, "limit": 10}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
86: 
87: - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
88: - **N2 — en pause** : commande **`eval_longueurs.py --rope --val <dir>`** (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
89: - **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** ([FAQ](../../reports/rapport-faq.md)), **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
90: - **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
91: - **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut sans clé **code 0**, **0 socket** ; `--tagger` sans cl
… [1839 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** ([FAQ](../../reports/rappor … [712 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 99, "limit": 10}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
99: > Vérifié par `tools/revue_documentation.py`.
100: 
101: | invariant | valeur | contrôle |
102: |---|---|---|
103: | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
104: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
105: | fichiers / JSON de résultats | **752** / **845** | `reports/*.md` / `reports/*.json` |
106: | documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
107: | dernière passe | **14/11 00 h 30** (84, **81/3**) ; rouges tolérées `indice`, `melange` ; `sessions` **revérifiée verte** le 14/11 06 h 55 | `docs/pilotage/references-non-regression.md` |
108: 

(Showing lines 99-108 of 144. Use offset=109 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **752** / **845** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **753** / **846** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 116, "limit": 24}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
116: | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
117: | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit (J11)** | **`g017` tranché** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
118: | **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 (manque **0,2856** val / **0,3566** test) ; **[v2](../../reports/rapport-coordination-n2-v2.md)** ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |
119: | **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, fermé −1,55 ; W3 : défaut hors ligne code 0, `--tagger` code 4 sans clé, 1 000 phrases = 143 870 tokens 
… [1720 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, fermé −1,55 ; W3 : défaut h … [933 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold de pensée, **qualité des rôles** ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — migration `/`  … [444 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche ; la\n  **restitution v1** : le miroir strict **ne monte pas** (0,1087), la forme canonique vaut\n  **46/46** ; le g … [419 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 33, "limit": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
33: | **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (4/5 familles ≥ 90 %) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) ; **W2 — tagger 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), fermé 402 −1,55** ([fiche](../../reports/rapport-tagger-h50.md)) ; **W3 — matrice du tagger** ([fiche](../../reports/rapport-tagger-defaut.md)) | **R4.4 close** ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; **J3 — restitution v3** ; R2/R3 attendent N5/N4 |

(Showing lines 33-33 of 492. Use offset=34 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "**W3 — matrice du tagger** ([fiche](../../reports/rapport-tagger-defaut.md)) | **R4.4 close** ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; **1 024 octets entraî … [644 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 38, "limit": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
38: **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du GV : 238/238, 0 span, 0 POS ; [fiche](../../reports/rapport-s065.md)) ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV** réglée (sujet hors du GV + adverbe final : GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **contrat v2 publié et validé** (`meta.partition`/`meta.alternative`, version 2, **v1 lue** : 26 cas, 0 échec) ; **restitution v1** (`restituer --canonique` : **46/46 formes canoniques exactes** contre la source canonisée, **miroir strict 0,1087 inchangé**, **395 segments / 395 rôles / 315 cibles dont 315 résolues**, stabilité **18/46** ; le strict ne monte pas, la v1 n'est pas la surface ; [fiche](../../reports/rapport-restitution-v1.md)) ; **restitution v2** : **16/46** cadres non vides exacts, F1 **0,5270** ; [fiche](../../reports/rapport-restitution-v2.md). **J9.1 passe d'honnêteté** (**19** fiches « instantané historique » : 10 encart
… [613 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "**restitution v2** : **16/46** cadres non vides exacts, F1 **0,5270** ; [fiche](../../reports/rapport-restitution-v2.md). **J9.1 passe d'honnêteté**", "new_string": "**restitution v2** : **16/46* … [504 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "for f in journal/2026-11-15/README.md journal/2026-11-15/mesures.md journal/2026-11-15/outils.md journal/2026-11-15/docs.md; do echo \"===== $f\"; tail -50 \"$f\"; done", "description": "Read journal entries for 2026-11-15"}`

  ```
===== journal/2026-11-15/README.md
<!-- notes -->
### B2 — les atomes ne prédisent pas les niveaux

La table J2.1 promettait un **porteur** pour chacun des 14 atomes ; B2 devait la mesurer. Le résultat est
un **négatif contrôlé**. Sur les **44 signatures** de Panini, **36 œuvres** ont assez de prose pour être
mesurées, **28** ont une fenêtre de signature propre et ≥ 1 000 jetons. Sur ces 28, les 14 atomes ne
prédisent pas **POS** (R²_CV **−0,092**, p=0,56), les **syntagmes** (**−0,160**, p=0,85) ni
l'**attachement** (**−0,092**, p=0,67). Le seul ρ nominal (POS **+0,176**, p=0,029) tombe à **Holm 0,088**
et ne survit pas à la date (**p_resid=1,0**).

Le dispositif n'est pas muet : il prédit l'**entropie des graphèmes** (**+0,811**), la **longueur des
mots** (**+0,657**), la **négation** (**+0,440**) et la **part de verbes** (**+0,429**). Mais la date
explique **0,16–0,54** de ces métriques et **aucune** ne survit au contrôle de date (**p_resid=0,76–1,0**).
Les atomes sont une signature **d'époque et de genre**, pas une entrée syntaxique.

Le signal brut des **36 mesurables** (POS **+0,102**, syntagmes **+0,060**) tombe à **+0,010 / +0,014**
sur 34, puis **−0,080 / −0,204** sur 26 : 
… [11701 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('journal/2026-11-15/mesures.md')\ns=p.read_text(encoding='utf-8')\nblock='''\n### W5 — la restitution v3 : les rôles des GP se séparent, le cadre ne suit pas\n\n`_role_gp` quitte la préposition seule pour le **contexte** : `à` + lieu (`l … [1395 caractères tronqués]`

  ```
mesures ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('journal/2026-11-15/README.md')\ns=p.read_text(encoding='utf-8')\nblock='''\n### W5 — la restitution v3 : les cinq rôles se séparent, le cadre ne suit pas\n\n`_role_gp` passe au contexte et sépare **lieu / temps / destinataire / possessi … [680 caractères tronqués]`

  ```
readme ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('journal/2026-11-15/outils.md')\ns=p.read_text(encoding='utf-8')\nblock='''\n### W5 — la règle de rôle et son banc\n\nNouveau module pur [`tools/roles_gp.py`](../../tools/roles_gp.py) (règle + 24 cas), mesure\n[`tools/restitution_v3.py`] … [1233 caractères tronqués]`

  ```
outils ok
docs ok
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py; echo \"EXIT=$?\"", "description": "Run documentation review"}`

  ```
revue de documentation · 753 fiche(s) · 846 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py; echo \"EXIT=$?\"; python3 tools/taille_documents.py 2>&1 | tail -10; echo \"EXIT2=$?\"", "description": "Verify state and document size"}`

  ```
en-cours · 1747 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT=0
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4117 mots (budget 4 000)

  avertissements :
     · 60 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9072 mots > budget 9000 (T1)
     · T0 : 4117 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT2=0
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -20; echo \"EXIT=$?\"", "description": "Verify journal"}`

  ```
journal · 47 jour(s) · 211 session(s) · 2626 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | head -60", "description": "Read document size details"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    9072    493   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2645    228   T1   2800  reports/README.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [582 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace(\n\" ; **W5 — restitution v3 : gold v2 20/46, F1 0,5406, `lieu` F1 0,60 ; gold S 144/144, cinq rôles 18/18, permutation 0/18 ; `--roles-v3` opt-in** ([fiche](../.. … [1420 caractères tronqués]`

  ```
roadmap trimmed
  avertissements :
     · 60 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9031 mots > budget 9000 (T1)
     · T0 : 4117 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace(\n\" ; **restitution v3** (`--roles-v3` : **20/46**, **17** non vides, F1 **0,5406**, `lieu` 0,60 ; gold S **144/144**, cinq rôles **18/18**, permutation **0/18**  … [395 caractères tronqués]`

  ```
roadmap trimmed 2
  avertissements :
     · 60 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9015 mots > budget 9000 (T1)
     · T0 : 4117 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\nold=\"**restitution v1** (`restituer --canonique` : **46/46 formes canoniques exactes** contre la source canonisée, **miroir strict 0,1087 inchangé**, **395 segments / 395 rôl … [574 caractères tronqués]`

  ```
roadmap trimmed 3

  avertissements :
     · 60 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4117 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\n# W5 session block\nold=\"- **Ce qu'elle fait** : **W5 — restitution v3** : `_role_gp` sépare **lieu / temps / destinataire / possession / complément** ; gold S **144/144** ( … [1770 caractères tronqués]`

  ```
en-cours W5 compressed
  avertissements :
     · 60 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4077 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "sed -n '44,56p' docs/pilotage/en-cours.md; echo ---; sed -n '71,85p' docs/pilotage/en-cours.md; echo ---; sed -n '87,96p' docs/pilotage/en-cours.md", "description": "Read en-cours old verbose sections"}`

  ```
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : validation.
- **Ambition** : rôles.
- **Stratégie** : contrôles.
- **Objectif final** : gold 60.
- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
- **Ce qu'elle fait** : **session close** ; **`/paragraphes`** v7, **`/`** ancien arbre (369) ; **`s/v7`** à fusionner.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**.
- **Prochaine action** : **migration `/` v7** (106/41) ; référents ; rétro-traduction.
- **Bloquants** : aucun ; 8765 pris (lancer 9000) ; migration = choix.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)*
---
### Session `0733c5bb-f90b
… [4187 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\nrepls=[\n(\"- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes` … [3437 caractères tronqués]`

  ```
en-cours trimmed
  avertissements :
     · 60 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4010 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace(\"**W5 — restitution v3** : cinq rôles séparés, gold S **144/144** (cinq **18/18**), gold v2 **20/46** (F1 **0,5406**), permutation **0/18** ; `--roles-v3` opt-in … [803 caractères tronqués]`

  ```
trim 10
  avertissements :
     · 60 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4001 mots (AGENTS + en-cours + une tâche) > budget 4 000
  en-cours · 1631 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace(\" ; **W2/W3/W4/W5** livrés ;\", \" ;\")\np.write_text(s,encoding='utf-8')\nprint('trim final')\nEOF\npython3 tools/taille_documents.py 2>&1 | tail -5", "descript … [39 caractères tronqués]`

  ```
trim final

  avertissements :
     · 60 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py; echo \"EXIT=$?\"", "description": "Re-run documentation review"}`

  ```
revue de documentation · 753 fiche(s) · 846 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py; echo \"EXIT=$?\"; python3 tools/verifie_journal.py 2>&1 | tail -5; echo \"EXIT2=$?\"; python3 tools/verifier_schemas.py 2>&1 | tail -5; echo \"EXIT3=$?\"", "description": "Run state, journal, schema checks"}`

  ```
en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT=0
  journal · 47 jour(s) · 211 session(s) · 2626 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT2=0
  schémas · 464 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
EXIT3=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -20; echo \"EXIT=$?\"", "description": "Run table gate"}`

  ```
✅ 1829 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4529 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
EXIT=0
  ```

- **bash** `{"command": "python3 -m unittest tools.tests.test_restitution_v3 tools.tests.test_restitution_v2 2>&1 | tail -8; echo \"EXIT=$?\"", "description": "Run v2 and v3 test suites"}`

  ```
..............................................
----------------------------------------------------------------------
Ran 46 tests in 3.731s

OK
EXIT=0
  ```

- **bash** `{"command": "python3 tools/bloc_linguistique.py --autotest >/tmp/autotest.json 2>&1; echo \"EXIT=$?\"; tail -8 /tmp/autotest.json", "description": "Run bloc autotest"}`

  ```
EXIT=0
  "parallele": true,
  "activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
  ```

- **bash** `{"command": "cd tools/structures && python3 -m unittest discover -s tests -v 2>&1 | tail -15; echo \"EXIT=$?\"", "description": "Run S structure tests"}`

  ```
ok
test_static (test_serveur.TestBanc.test_static) ...   127.0.0.1 · "GET / HTTP/1.1" 200 -
ok
test_statut_invalide (test_serveur.TestBanc.test_statut_invalide) ...   127.0.0.1 · "POST /api/valider HTTP/1.1" 400 -
ok
test_valider_et_export (test_serveur.TestBanc.test_valider_et_export) ...   127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
ok

----------------------------------------------------------------------
Ran 56 tests in 4.337s

OK
EXIT=0
  ```

- **bash** `{"command": "sed -n '1,120p' tools/toutes-les-portes.sh", "description": "Read full gates script"}`

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
… [3112 caractères tronqués]
  ```

- **bash** `{"command": "DELAI=600 JOURNAUX=work/portes-w5 bash tools/toutes-les-portes.sh", "description": "Run full gates in background", "run_in_background": true}`

  ```
started background job bash-129
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-restitution-v3.md')\ns=p.read_text(encoding='utf-8')\nold=\"Le zéro de `complément` est un **trou d'or**, pas une performance : la catégorie n'est pas\\nmesurée. Le 18/18 est la seule mesure des cinq rôles sur un or ; le … [545 caractères tronqués]`

  ```
note moyen ajoutée
  ```

- **job_output** `{"job_id": "bash-129", "wait": true, "timeout_ms": 600000}`

  ```
=== PASSE COMPLÈTE DES PORTES (85 portes, borne 600 s) ===
    journaux : work/portes-w5
  porte-adaptateur-sortie ✅                          91 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         177 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          17 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          18 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          55 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          92 s    ✅ le canal diffusé par fichier change la région du milieu
[status: running]
  ```

- **bash** `{"command": "git diff tools/drave.py", "description": "Inspect full drave.py diff"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index 045d895d..ec45a311 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -53,6 +53,7 @@ sys.path.insert(0, str(RACINE))
 import bloc_linguistique as bl  # noqa: E402  (import après l'installation des chemins)
 import restitution  # noqa: E402  (la restitution v0 : annotation → surface)
 import restitution_v2  # noqa: E402  (la restitution v2 : les rôles)
+import restitution_v3  # noqa: E402  (la restitution v3 : les rôles des GP)
 
 NOM = "drave"
 VERSION = "0.1.0"
@@ -245,6 +246,30 @@ def _cout_tagger(stats: dict) -> dict:
             "modeles_renvoyes": dict(stats["modeles"])}
 
 
+def _cout_pour_phrases(cout: dict, mesurees: int, cible: int) -> dict:
+    """Le coût d'un lot de `cible` phrases, au prorata du lot **mesuré**.
+
+    Le tagger fait **un appel par phrase** : le coût est linéaire en nombre de phrases. On ne
+    modélise pas la longueur des phrases (le prompt la porte), donc ce chiffre vaut pour un lot
+    de même longueur moyenne que le lot mesuré. `mesurees` est le nombre de phrases réellement
+    passées au tagger ; il ne doit pas être confondu avec le nombre d'appels (le cache mémoire
+    peut en servir plusieu
… [7442 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff tools/drave.py > /tmp/drave_full.diff && python3 - <<'EOF'\nimport re\ns=open('/tmp/drave_full.diff').read()\nlines=s.splitlines(keepends=True)\n# header = lines before first @@\nfirst=next(i for i,l in enumerate(lines) if l … [746 caractères tronqués]`

  ```
DROP @@ -245,6 +246,30 @@ def _cout_tagger(stats: dict) -> dict:
DROP @@ -635,6 +660,8 @@ def cmd_evaluer(args: argparse.Namespace) -> int:
kept 7 hunks
APPLIED
 tools/drave.py | 53 +++++++++++++++++++++++++++++++++++++++++++----------
 1 file changed, 43 insertions(+), 10 deletions(-)
diff --git a/tools/drave.py b/tools/drave.py
index 045d895d..b4b767d2 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -53,6 +53,7 @@ sys.path.insert(0, str(RACINE))
 import bloc_linguistique as bl  # noqa: E402  (import après l'installation des chemins)
 import restitution  # noqa: E402  (la restitution v0 : annotation → surface)
 import restitution_v2  # noqa: E402  (la restitution v2 : les rôles)
+import restitution_v3  # noqa: E402  (la restitution v3 : les rôles des GP)
 
 NOM = "drave"
 VERSION = "0.1.0"
@@ -707,15 +708,24 @@ def cmd_restituer(args: argparse.Namespace) -> int:
     laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`
     ajoute la **forme canonique v1** (segments + rôles + cibles) et son miroir ;
     `--roles` ajoute la **v2** (agent, prédicat, lieu) et, sur un banc, sa fidélité à
-    l'or. La sortie de la v0 reste celle par défaut.
+    l'or ; `
… [157 caractères tronqués]
  ```

- **bash** `{"command": "git diff --stat tools/bloc_linguistique.py reports/README.md journal/2026-11-15/README.md journal/2026-11-15/mesures.md journal/2026-11-15/outils.md journal/2026-11-15/docs.md; echo ====; git diff tools/bloc_linguistique.py | head -80", "description": "Check diffs of other modified file … [3 caractères tronqués]`

  ```
journal/2026-11-15/README.md  | 10 ++++++++++
 journal/2026-11-15/docs.md    |  8 ++++++++
 journal/2026-11-15/mesures.md | 18 ++++++++++++++++++
 journal/2026-11-15/outils.md  | 10 ++++++++++
 reports/README.md             |  1 +
 tools/bloc_linguistique.py    | 18 +++++++++++++++++-
 6 files changed, 64 insertions(+), 1 deletion(-)
====
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 53bf63bc..edb29e19 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -47,6 +47,10 @@ from dataclasses import dataclass, field
 from typing import Protocol, Sequence
 
 RACINE = pathlib.Path(__file__).resolve().parent.parent
+try:  # paquet : `tools.bloc_linguistique`
+    from . import roles_gp as _roles_gp
+except ImportError:  # script : `python3 tools/bloc_linguistique.py`
+    import roles_gp as _roles_gp
 NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
            "pragmatique", "document")
 SOURCES = ("heuristique", "neuronal", "humain")
@@ -535,7 +539,19 @@ def _est_verbe(mot: str) -> bool:
     return False
 
 
-def _role_gp(prep: str) -> str:
+def _role_gp(prep: str, suivant: str = "", precedent: str = ""
… [949 caractères tronqués]
  ```

- **bash** `{"command": "git diff reports/README.md | head -30; echo ====; git diff journal/2026-11-15/README.md | head -40", "description": "Check reports README and journal diff"}`

  ```
diff --git a/reports/README.md b/reports/README.md
index 6b3ed679..bd23fd80 100644
--- a/reports/README.md
+++ b/reports/README.md
@@ -63,6 +63,7 @@
 | [`rapport-restitution-v0.md`](rapport-restitution-v0.md) | **B13** — restitution v0 : **46/46** surfaces, miroir |
 | [`rapport-restitution-v1.md`](rapport-restitution-v1.md) | **B13** — restitution v1 : forme canonique **46/46** |
 | [`rapport-restitution-v2.md`](rapport-restitution-v2.md) | **B13** — restitution v2 : rôles **16/46**, F1 **0,5270** |
+| [`rapport-restitution-v3.md`](rapport-restitution-v3.md) | **B13** — restitution v3 : cinq rôles **18/18** sur le gold S, **20/46** sur le gold v2 |
 | [`rapport-pos-nombres.md`](rapport-pos-nombres.md) | **B13** — les nombres ont une POS (NUM) |
 | [`rapport-partition-integree.md`](rapport-partition-integree.md) | **B13** — partition : alternatives étiquetées |
 | [`rapport-partition-syntagmes.md`](rapport-partition-syntagmes.md) | **B13** — la partition (A29) |
====
diff --git a/journal/2026-11-15/README.md b/journal/2026-11-15/README.md
index bdeb2889..e281c069 100644
--- a/journal/2026-11-15/README.md
+++ b/journal/2026-11-15/README.md
@@ -113,4 +113,14 @@ fermé perd **−1,55 pt*
… [972 caractères tronqués]
  ```

- **bash** `{"command": "git status --short | head -40", "description": "Current git status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/2026-11-15/README.md
 M journal/2026-11-15/docs.md
 M journal/2026-11-15/mesures.md
 M journal/2026-11-15/outils.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-5d421585-1af2-4f07-ac86-e4879cc23d4f/digest.md
 M journal/sessions/session-5d421585-1af2-4f07-ac86-e4879cc23d4f/rapport.md
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
 M tools/bloc_linguistique.py
 M tools/chantier/plan.json
MM tools/drave.py
?? journal/sessions/session-bfc6d60f-dbfd-473c-a769-05fde9b1e428/
?? reports/pensee-restitution-v3.json
?? reports/rapport-restitution-v3.md
?? reports/rapport-s-paragraphes.md
?? tools/mesurer_restitution_v3.py
?? tools/restitution_v3.py
?? t
… [98 caractères tronqués]
  ```

- **bash** `{"command": "sha256sum reports/pensee-restitution-v3.json > /tmp/hash_before; python3 tools/mesurer_restitution_v3.py >/tmp/v3_run.txt 2>&1; echo \"EXIT=$?\"; sha256sum reports/pensee-restitution-v3.json > /tmp/hash_after; cat /tmp/hash_before /tmp/hash_after; diff /tmp/hash_before /tmp/hash_after & … [89 caractères tronqués]`

  ```
EXIT=0
049a169363edf43f71421ccb4551ec4b53f8e285a8be77cab93f8cd952b20aeb  reports/pensee-restitution-v3.json
049a169363edf43f71421ccb4551ec4b53f8e285a8be77cab93f8cd952b20aeb  reports/pensee-restitution-v3.json
STABLE
contrôle constant (type) : 6/46 cadres exacts
contrôle rôles mélangés  : 3/46 cadres exacts
contrôle négatif rendu   : 39/39 éligibles détectés

gold S : 144/144 (1.0000) · cinq rôles 18/18 (F1 1.0000)
permutation des cinq : 0/18 ; permutation de tous : 0.4028 global
séparation : 24/24
écrit : reports/pensee-restitution-v3.json
  ```

- **bash** `{"command": "git add tools/roles_gp.py tools/restitution_v3.py tools/mesurer_restitution_v3.py tools/tests/test_restitution_v3.py tools/bloc_linguistique.py reports/rapport-restitution-v3.md reports/pensee-restitution-v3.json reports/README.md reports/INDEX.md docs/pilotage/en-cours.md docs/pilotage … [205 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
 M docs/produit/README.md
M  journal/2026-11-15/README.md
M  journal/2026-11-15/docs.md
M  journal/2026-11-15/mesures.md
M  journal/2026-11-15/outils.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-5d421585-1af2-4f07-ac86-e4879cc23d4f/digest.md
 M journal/sessions/session-5d421585-1af2-4f07-ac86-e4879cc23d4f/rapport.md
M  reports/INDEX.md
M  reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
A  reports/pensee-restitution-v3.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
A  reports/rapport-restitution-v3.md
 M reports/rapport-spans-chunker.md
M  tools/bloc_linguistique.py
 M tools/chantier/plan.json
MM tools/drave.py
A  tools/mesurer_restitution_v3.py
A  tools/restitution_v3.py
A  tools/roles_gp.py
A  tools/tests/test_restitution_v3.py
?? journal/sessions/session-bfc6d60f-dbfd-473c
… [99 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached --stat", "description": "Show staged diff stat"}`

  ```
docs/pilotage/en-cours.md          |    29 +-
 docs/pilotage/roadmap.md           |     4 +-
 journal/2026-11-15/README.md       |    10 +
 journal/2026-11-15/docs.md         |     8 +
 journal/2026-11-15/mesures.md      |    18 +
 journal/2026-11-15/outils.md       |    10 +
 reports/INDEX.md                   |     4 +-
 reports/README.md                  |     1 +
 reports/pensee-restitution-v3.json | 27174 +++++++++++++++++++++++++++++++++++
 reports/rapport-restitution-v3.md  |   417 +
 tools/bloc_linguistique.py         |    18 +-
 tools/drave.py                     |    53 +-
 tools/mesurer_restitution_v3.py    |   256 +
 tools/restitution_v3.py            |   553 +
 tools/roles_gp.py                  |   332 +
 tools/tests/test_restitution_v3.py |   346 +
 16 files changed, 29205 insertions(+), 28 deletions(-)
  ```

- **bash** `{"command": "git diff --cached tools/drave.py | grep -E \"^\\+|^-\" | head -60", "description": "The text before the last \"Received\" is:"}`

  ```
--- a/tools/drave.py
+++ b/tools/drave.py
+import restitution_v3  # noqa: E402  (la restitution v3 : les rôles des GP)
-    l'or. La sortie de la v0 reste celle par défaut.
+    l'or ; `--roles-v3` ajoute la **v3** (les rôles des GP : lieu, temps, destinataire,
+    possession, complément). La sortie de la v0 reste celle par défaut.
+    if args.roles_v3 and args.canonique:
+        print(f"{NOM}: erreur d'usage : --roles-v3 et --canonique sont exclusifs",
+              file=sys.stderr)
+        return 2
+    if args.roles and args.roles_v3:
+        print(f"{NOM}: erreur d'usage : --roles (v2) et --roles-v3 sont exclusifs",
+              file=sys.stderr)
+        return 2
-    if args.gold and not (args.banc and args.roles):
-        print(f"{NOM}: erreur d'usage : --gold ne sert qu'avec --banc --roles",
-              file=sys.stderr)
+    if args.gold and not (args.banc and (args.roles or args.roles_v3)):
+        print(f"{NOM}: erreur d'usage : --gold ne sert qu'avec --banc --roles ou "
+              "--banc --roles-v3", file=sys.stderr)
-        if args.roles:
-            chemin_gold = pathlib.Path(args.gold or restitution_v2.GOLD_DEFAUT)
+        if args.roles_v3 or args.
… [1804 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -120", "description": "Review state/roadmap staged diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index e8d05f9b..9d8a725c 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 11 h 10 HNE (W4 : le manifeste Panini et le rejeu disponible)**
+**Mis à jour : 2026-11-15, 11 h 40 HNE (W5 : la restitution v3 — les rôles des GP)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -46,7 +46,7 @@
 - **Ambition** : rôles.
 - **Stratégie** : contrôles.
 - **Objectif final** : gold 60.
-- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
+- **Fait** : types **61/61**, rôles **144/144** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../repo
… [24567 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\nold=\"; W5 : restitution v3, **20/46** (F1 0,5406), gold S **144/144**, `--roles-v3` opt-in**\"\nnew=\"; W5 : restitution v3, 20/46 (F1 0,5406), gold S 144/144, `--roles-v3` o … [305 caractères tronqués]`

  ```
revue de documentation · 753 fiche(s) · 846 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
     · 60 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
AssertionError
  ```

- **bash** `{"command": "grep -n \"W5 : restitution\" docs/pilotage/roadmap.md | head -3", "description": "Locate W5 R row text"}`

  ```
(no output)
  ```

- **bash** `{"command": "grep -n \"W5\" docs/pilotage/roadmap.md | head -5", "description": "Find W5 in roadmap"}`

  ```
33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (4/5 familles ≥ 90 %) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) ; **W2 — tagger 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), fermé 402 −1,55** ([fiche](../../reports/rapport-tagger-h50.md)) ; **W3 — matrice du tagger** ([fiche](../../reports/rapport-tagger-defaut.md)) ; **W5 — restitution v3 : gold S 144/144, cinq rôles 18/18, permutation 0/18 ; `--roles-v3` opt-in** ([fiche](../../reports/rapport-restitution-v3.md)) | **R4.4 close** ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; **J4 — l'or de rôles** (seconds cadres) ; R2/R3 attendent N5/N4 |
  ```

- **bash** `{"command": "grep -n \"W5 : restitution\" docs/pilotage/en-cours.md", "description": "Find nested bold in en-cours"}`

  ```
119:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, fermé −1,55 ; W3 : défaut hors ligne code 0, `--tagger` code 4 sans clé, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; W5 : restitution v3, **20/46** (F1 0,5406), gold S **144/144**, `--roles-v3` opt-in** ; R2/R3 attendent N5/N4 | **J4 — l'or de rôles** (seconds cadres) ; **Panini** si les 26 signatures arrivent ; **[fiche W3](../../reports/rapport-tagger-defaut.md)**, **[fiche W5](../../reports/rapport-restitution-v3.md)** |
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\nold=\"W5 : restitution v3, **20/46** (F1 0,5406), gold S **144/144**, `--roles-v3` opt-in**\"\nnew=\"W5 : restitution v3, 20/46 (F1 0,5406), gold S 144/144, `--roles-v3` opt- … [257 caractères tronqués]`

  ```
fixed en-cours nested bold
  revue de documentation · 753 fiche(s) · 846 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **job_output** `{"job_id": "bash-129", "wait": true, "timeout_ms": 600000}`

  ```
porte-bus-socket       ✅                         198 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard        ✅                          41 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne
  porte-cerveau          ✅                          11 s    ✅ porte tenue (quatre facultés composent, chacune reste active, le tout est déterministe)
  porte-cic              ✅                          13 s  ✅ porte CIC verte : 42/42 verdicts, empreintes, de Bruijn, sha256 2e implémentation,
  porte-consolidation    ✅                          89 s    ✅ porte tenue (fusion exacte : nulle ⇒ identique, réelle ⇒ visible, lecteur ⇒ hors fichier)
  porte-coupe            ✅                         175 s    ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit
  porte-cycle-c2         ✅                         138 s    ✅ porte tenue (chaîne exacte · pas 1 exact · borné · coût dit · trajectoire déterministe ·
  porte-deepseek         ✅                           1 s    ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
  porte-delais           ✅                        
… [393 caractères tronqués]
  ```

- **bash** `{"command": "python3 -m py_compile tools/roles_gp.py tools/restitution_v3.py tools/mesurer_restitution_v3.py tools/tests/test_restitution_v3.py tools/bloc_linguistique.py tools/drave.py && echo \"COMPILE OK\"", "description": "Compile new and modified modules"}`

  ```
COMPILE OK
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys; sys.path.insert(0,'.')\nimport tools.restitution_v3 as v3\n# sanity: all gold S per-role counts sum to 144, all five 18\ng=v3.mesurer_gold_analyseur_v3()\ntot=sum(x['attendus'] for x in g['base']['par_role'].values())\nprint('per-role attendus sum',to … [216 caractères tronqués]`

  ```
per-role attendus sum 144 roles 144
apparies phrases 61 / 61
cinq 18 18
  ```

- **bash** `{"command": "git diff --cached --check; echo \"EXIT=$?\"", "description": "Check staged diff whitespace"}`

  ```
EXIT=0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-restitution-v3.md')\ns=p.read_text(encoding='utf-8')\nold=\"- **Gain d'appariement** (v3, v2 → v3) : **+1** rôle global (`h056`, le SUB long), **0**\\n  rôle des cinq. Le gain est un gain de **mesure**, pas de règle.\"\n … [697 caractères tronqués]`

  ```
interaction note added
  ```

- **job_output** `{"job_id": "bash-129", "wait": true, "timeout_ms": 900000}`

  ```
porte-episodique       ✅                         274 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           1 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          30 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                          10 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         281 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
[status: running]
  ```

- **bash** `{"command": "grep -n \"_r\\.\" tools/restitution_v3.py; grep -n \"collections\" tools/restitution_v3.py | head; grep -n \"re\\.\" tools/restitution_v3.py | head", "description": "Find unused imports in v3 module"}`

  ```
26:import collections
147:    c = collections.Counter()
210:    gp = collections.Counter()
319:    or_counts = collections.Counter()
320:    pred_counts = collections.Counter()
321:    justes = collections.Counter()
58:    m = re.match(r"\s*([A-Za-zÀ-ÖØ-öø-ÿ]+)(['’])(.*)$", texte)
61:    m = re.match(r"\s*([A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿ]+)?)", texte)
  ```

- **bash** `{"command": "command -v ruff || command -v pyflakes || true; python3 -m pyflakes tools/restitution_v3.py tools/roles_gp.py tools/mesurer_restitution_v3.py tools/tests/test_restitution_v3.py 2>&1 | head -20", "description": "Check lint tools"}`

  ```
/usr/bin/python3: No module named pyflakes
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/restitution_v3.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('import tools.restitution as _r  # noqa: E402\\n','')\np.write_text(s,encoding='utf-8')\np=pathlib.Path('tools/mesurer_restitution_v3.py')\ns=p.read_text(encoding=' … [551 caractères tronqués]`

  ```
removed unused
----------------------------------------------------------------------
Ran 29 tests in 2.579s

OK
  ```

- **bash** `{"command": "sha256sum reports/pensee-restitution-v3.json > /tmp/h1; python3 tools/mesurer_restitution_v3.py >/tmp/v3_run2.txt 2>&1; echo \"EXIT=$?\"; sha256sum reports/pensee-restitution-v3.json > /tmp/h2; diff /tmp/h1 /tmp/h2 && echo STABLE; python3 tools/revue_documentation.py 2>&1 | tail -2", "d … [42 caractères tronqués]`

  ```
EXIT=0
STABLE
  revue de documentation · 753 fiche(s) · 846 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "git add tools/restitution_v3.py tools/mesurer_restitution_v3.py reports/rapport-restitution-v3.md && git diff --cached --stat && git diff --cached --check; echo \"EXIT=$?\"", "description": "Stage latest edits and check"}`

  ```
docs/pilotage/en-cours.md          |    29 +-
 docs/pilotage/roadmap.md           |     4 +-
 journal/2026-11-15/README.md       |    10 +
 journal/2026-11-15/docs.md         |     8 +
 journal/2026-11-15/mesures.md      |    18 +
 journal/2026-11-15/outils.md       |    10 +
 reports/INDEX.md                   |     4 +-
 reports/README.md                  |     1 +
 reports/pensee-restitution-v3.json | 27174 +++++++++++++++++++++++++++++++++++
 reports/rapport-restitution-v3.md  |   421 +
 tools/bloc_linguistique.py         |    18 +-
 tools/drave.py                     |    53 +-
 tools/mesurer_restitution_v3.py    |   250 +
 tools/restitution_v3.py            |   552 +
 tools/roles_gp.py                  |   332 +
 tools/tests/test_restitution_v3.py |   346 +
 16 files changed, 29202 insertions(+), 28 deletions(-)
EXIT=0
  ```

- **job_output** `{"job_id": "bash-129", "wait": true, "timeout_ms": 900000}`

  ```
porte-greffe           ⏱ (borne 600 s dépassée)  600 s    ✅ l'état injecté porte bien la direction du contenu de A
[status: running]
  ```

- **bash** `{"command": "tail -5 work/portes-w5/registre.txt; wc -l work/portes-w5/registre.txt; ls work/portes-w5 | wc -l", "description": "Check gate progress"}`

  ```
porte-etat 0 1
porte-flux 0 30
porte-fusion 0 10
porte-gain 0 281
porte-greffe 124 600
28 work/portes-w5/registre.txt
31
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-restitution-v3.md')\ns=p.read_text(encoding='utf-8')\nold=\"- **Gain de rôles** (v2 → v3, appariement v2) : **+4** rôles globaux, **+1** rôle des cinq.\\n  Les quatre corrigés sont `p002` (`avec` : `attribut` → `moyen`), … [855 caractères tronqués]`

  ```
precision dedupe/regle
  ```

- **job_output** `{"job_id": "bash-129", "wait": true, "timeout_ms": 900000}`
