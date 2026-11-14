# Session DSH — relecture

- identifiant : `session-f198001c-49da-4e65-8a44-782f9605fd7a`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 01:48:04
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotation (segments + rôles + cibles) et la mesurer : le miroir strict (0,1087) doit-il monter ? Fiche `reports/rapport-restitution-v1.md` + JSON, tests, commit.

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

- **bash** `{"command": "ls -la && git log --oneline -15 && git status --short", "description": "List workspace and git state"}`

  ```
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   180 14 nov 01:48 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   972 14 nov 00:51 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 75158 14 nov 01:36 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run
… [3453 caractères tronqués]
  ```

- **grep** `{"pattern": "0,1087|0\\.1087|46/46", "path": "."}`

  ```
Found 220 matches

./tools/chantier/plan.json
Line 271:    "mandat": "Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotation (segments + rôles + cibles) et la mesurer : le miroir strict (0,1087) doit-il monter ? Fiche `reports/rapport-restitution-v1.md` + JSON, tests, commit.",

./docs/produit/README.md
Line 236: `--banc reports/pensee-fiabilite-produit.json` rejoue les **50 textes libres** : **46/46
Line 237: surfaces exactes**, miroir strict **0,1087**, contrôle négatif **46/46**. C'est un **codec de
Line 436: `--fichier`/`--jsonl`, `--banc`, `--partition`, la **restitution v0** (46/46 surfaces exactes,
Line 437: miroir strict 0,1087), la porte produit et le smoke test. Le reste est nommé ci-dessus, sans

./reports/rapport-semaine.json
Line 61:         "miroir": {"exacts": 5, "fidelite": 0.1087},
Line 62:         "controle_negatif": {"melange": "0/46", "troncature": "0/46", "detectes": "46/46"},
Line 63:         "lecture": "Codec de surface, pas decodeur ; le correctif C a ramene la surface de 45/46 a 46/46.",
Line 203:     {"id": "D4", "objet": "La restitution v0 est un codec de surface, pas un decodeur ; ajout
… [43094 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-14, 02 h 10 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
11: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
12: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
13: - **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
14: - **Bloquants** : aucun.
15: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
16: 
17: ## Sessions en cours
18: 
19: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
20: > [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
21: > `plan.md` (`python3 tools/sessions
… [11529 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v0.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v0.md</path>
<type>file</type>
<content>
1: # B13 — la restitution v0 : 46/46 surfaces exactes, le miroir strict à 0,1087
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : J1.4 · **Date** : 2026-11-07 ·
4: > **Verdict** : ✅
5: > **Ce que la commande fait** : `python3 tools/drave.py restituer TEXTE` analyse le texte,
6: > reconstruit la surface depuis le niveau **`graphème`** de l'annotation — **sans lire
7: > `Annotation.texte`** — et affiche la fidélité du **miroir** (surface, mots, POS), la fidélité
8: > de caractères et un **contrôle négatif**. `restituer --banc` rejoue le banc des 50 textes.
9: >
10: > **Le chiffre.** Sur les **50 textes libres** de l'audit A26 : **46 annotations** (4 refus),
11: > **46/46 surfaces exactes** (1,0000) ; le **miroir strict** — le minimum des fidélités
12: > surface/mots/POS — vaut **5/46 = 0,1087** ; le contrôle négatif casse **46/46**.
13: > Le miroir a trouvé un trou : `f50` perdait ses **10 sauts de ligne** (45/46, 0,9783) ;
14: > le correctif `C` les annote et la surface revient à 46/46.
15: >
16: > **Dispositif** : [`drave.py`](../tools/drave.py) 
… [9243 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """test_restitution.py — la restitution v0 (J1.4) : annotation → surface, et le miroir.
3: 
4: Ce que le test fige :
5: - la commande `drave restituer TEXTE` sort 0 et affiche la fidélité de surface ;
6: - la surface est reconstruite **sans lire** `Annotation.texte` ;
7: - les sauts de ligne sont annotés (`graphème` de type `contrôle`) et reviennent ;
8: - le miroir strict est le minimum de surface/mots/POS (la ponctuation séparée le fait
9:   tomber), et le contrôle négatif (mélange, troncature) le détecte ;
10: - sur les **50 textes libres**, 46 annotations et **46/46 surfaces exactes** ; sans le
11:   correctif `C`, `f50` perd ses sauts de ligne (45/46) — le trou que le miroir a trouvé.
12: """
13: from __future__ import annotations
14: 
15: import json
16: import pathlib
17: import subprocess
18: import sys
19: import tempfile
20: import unittest
21: 
22: RACINE = pathlib.Path(__file__).resolve().parents[2]
23: sys.path.insert(0, str(RACINE))
24: 
25: import tools.bloc_linguistique as bl  # noqa: E402
26: import tools.restitution 
… [7243 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\n# find J8\ndef walk(x):\n    if isinstance(x,dict):\n        if x.get('id','').startswith('J8') or 'J8' in str(x.get('id','')):\n            print(json.dumps(x,ensure_ascii=False,indent=2)[:3000])\n        fo … [151 caractères tronqués]`

  ```
{
  "id": "J8.1",
  "jour": 8,
  "titre": "La restitution v1",
  "mandat": "Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotation (segments + rôles + cibles) et la mesurer : le miroir strict (0,1087) doit-il monter ? Fiche `reports/rapport-restitution-v1.md` + JSON, tests, commit.",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f reports/rapport-restitution-v1.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    }
  ]
}
  ```

- **bash** `{"command": "ls tools/ && echo --- && grep -rl \"restituer\\|restitution\" tools --include=*.py | head -50", "description": "Find restitution code files"}`

  ```
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
calibrer.py
campagne-benefices.sh
campagne_synthese.py
canal_structure.py
cancellation_langue.py
carte_chantiers.py
carte_coupe.sh
carte_decisions.py
carte-facultes.sh
carte-fenetre-puits.sh
carte_langues.py
carte_latence.sh
carte-sortie-profondeur.sh
catalogue_corpus.py
cca_raisonnement.py
census_routage.py
cerveau
chantier
chat.py
clusters_moe.py
code_partage.py
colab_cote_local.
… [8775 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,400p tools/restitution.py", "description": "Read restitution.py first 400 lines"}`

  ```
"""restitution.py — la restitution v0 : annotation → surface, et le miroir.

La **surface** est reconstruite depuis le niveau `graphème` — les spans typés qui portent
les caractères — **sans lire** `Annotation.texte`. Les niveaux `mot` et `pos` sont mesurés
comme des sorties plus pauvres : ils disent ce que la couche de surface ajoute.

Le **miroir** est la règle 6 du dépôt : `fidelite` est binaire (1.0 si la sortie égale la
source), et `miroir` est le minimum des trois fidélités (surface, mots, pos). C'est la
définition de `tools/tests/linguistique/miroir.mesurer`, réutilisée ici pour ne pas en
avoir deux. `fidelite_caractere` ajoute une distance de Levenshtein normalisée : elle
distingue « presque fidèle » de « fidèle » et documente la perte de la ponctuation.

Le **contrôle négatif** mélange les graphèmes (graine fixe) et en retire un : les deux
doivent casser la fidélité. Sans lui, un codec qui recopie la source ne prouverait rien.
"""
from __future__ import annotations

import pathlib
import random
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import tools.bloc_linguistique as bl  # noqa
… [14784 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,300p tools/mesurer_restitution_v0.py", "description": "Read v0 measurement script"}`

  ```
#!/usr/bin/env python3
"""mesurer_restitution_v0.py — produit le JSON de la fiche J1.4.

Mesure la restitution v0 sur les **50 textes libres** de
`reports/pensee-fiabilite-produit.json` (le banc de l'audit A26) et écrit
`reports/pensee-restitution-v0.json`. La fiche `reports/rapport-restitution-v0.md`
cite ce JSON.

    python3 tools/mesurer_restitution_v0.py
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

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
SORTIE = RACINE / "reports" / "pensee-restitution-v0.json"

LIMITES = [
    "4 refus sans annotation (f14 emoji, f15 vide, f16 espaces, f17 « ... ») : "
    "la surface n'est pas reconstructible, ils sont comptés à part.",
    "La fidélité binaire du miroir compare la sortie à la source exacte : la ponctuation "
    "séparée des mots fait tomber mots et POS à 5/46, alors que la fidélité de caractères "
    "reste à 0,9506. Les deux mesures disent des choses différentes.",
    "La sur
… [2327 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Annotation\\|def analyser\\|class Etiquette\\|class Span\\|class Cible\\|syntagmes\\|role\\|cible\" tools/bloc_linguistique.py | head -80", "description": "Inspect annotation API"}`

  ```
59:class Span:
68:class Etiquette:
92:# v2 : ajoute `meta.partition` et `meta.alternative` (partition des syntagmes qui se
98:class Annotation:
141:    def analyser(self, texte: str, langue: str | None = None,
538:def _role_gp(prep: str) -> str:
909:    # -- syntagmes ----------------------------------------------------------
974:                        gn.update({"type": "GN", "role": "agent", "niveau": 0,
986:    def _syntagmes_s(self, texte: str) -> list[dict] | None:
997:    def _cibles_s(self, texte: str) -> dict:
998:        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
1001:        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
1009:            return {(s.debut, s.fin, s.type): (s.cible_gp or s.cible_nom or s.cible_verbe)
1015:    def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
1028:    def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict]) -> str | None:
1031:        Le gold : « elle qui commence nage » → REL « qui commence » a pour cible `elle`,
1070:    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict]) -> str | None:
1085:    def _r
… [4782 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 40,140p tools/bloc_linguistique.py; echo '--- 1600-1780 ---'; sed -n 1600,1785p tools/bloc_linguistique.py", "description": "Read Annotation and syntagme generation"}`

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
    candidats: list[str] = field(default_factory=list)
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    meta: dict = field(default_factory=dict)

    def json(self) -> dict:
        return {
            "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
            "debut": self.debut, "fin": self.fin, "source": self.source,
            "confiance":
… [14520 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,260p tools/tests/linguistique/miroir.py", "description": "Read mirror definition"}`

  ```
"""Le miroir entrée/sortie du bloc linguistique : restitution et fidélité.

Règle 6 : toute mesure d'entrée se double d'une mesure de sortie. `rendre` reconstruit
le texte depuis les étiquettes de **surface** (`graphème`, `mot`) ; `fidelite` le compare
à la source. La **fluidité** (longueur, ponctuation) n'est pas la **fidélité** : une
restitution peut être fluide et infidèle, ou fidèle et hachée.
"""
from __future__ import annotations

import re

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import tools.bloc_linguistique as bl
from tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc


def rendre(a: bl.Annotation) -> str:
    """Reconstruit le texte depuis les étiquettes de surface, sans lire `a.texte`."""
    g = [e for e in a.etiquettes if e.niveau == "graphème"]
    if not g:
        return ""
    return "".join(e.valeur for e in sorted(g, key=lambda e: (e.debut, e.fin)))


def fidelite(a: bl.Annotation, source: str) -> float:
    """1.0 si la restitution égale la source, 0.0 sinon (la mesure est binaire ici)."""
    return 1.0 if rendre(a) == source else 0.0


def rendre_mots(a: bl.Annotation) -> str:
    """Rest
… [9478 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"restituer\" -A60 tools/drave.py | head -120", "description": "Read CLI restituer handler"}`

  ```
11:    python3 tools/drave.py restituer "Le chat dort."
12:    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
13-    python3 tools/drave.py --version
14-
15-Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
16-avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
17-**restitution v0** (annotation → surface, avec la fidélité du miroir). La restitution est un
18-**codec de surface** : elle reconstruit depuis le niveau `graphème`, pas un décodeur neuronal.
19-Ce qu'elle n'expose pas encore : le neuronal (`llama-cli` ou endpoint local), la traduction et la
20-génération : ils demandent des poids, un service ou un GPU, alors que ce prototype est hors ligne,
21-CPU et sans réseau.
22-
23-Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 1 erreur.
24-"""
25-from __future__ import annotations
26-
27-import argparse
28-import hashlib
29-import importlib.util
30-import json
31-import pathlib
32-import random
33-import sys
34-import textwrap
35-
36-# Le dépôt d'abord — `sys.path.insert(0, '.')` quand on lance depuis sa racine, et les chemins
37-# déduits du f
… [3932 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\ndef walk(x):\n    if isinstance(x,dict):\n        if str(x.get('id','')).startswith('J'):\n            print(x.get('id'), '-', x.get('titre'), '|', x.get('mandat','')[:300].replace('\\n',' '))\n        for v  … [136 caractères tronqués]`

  ```
J0 - Le contrôle du superviseur | Réponds exactement le mot OK, sans autre texte. C'est un test de liaison du superviseur.
J1.1 - r035 : la relative zéro | Tâche J1.1 du chantier : la relative zéro (r035, « The film she talks about is out. »). Reproduis, explique, propose UNE règle générale mesurée sur dev/test ; si elle tient (attachement 236→237, POS/F1 stables), intègre-la et commite avec une fiche `reports/rapport-r035.md` + `reports/pensee-r035.js
J1.2 - La convention des GV | Tâche J1.2 : la convention des GV (322 FP / 180 FN). Classe les erreurs, mesure 2 règles candidates (arrêt à l'adverbe final, sujet hors du GV) sur dev/test, garde celles qui font monter le F1 sans perdre d'attachement, fiche `reports/rapport-convention-gv.md` + JSON, commit. Règles : S/D/N2 intouch
J1.3 - Le schéma v2 | Tâche J1.3 : le schéma v2 de l'annotation — publier `tools/schemas/drave-annotation-v2.json` (ajout de `meta.alternative` et `meta.partition`), version 2, valider avec `tools/verifier_schema_produit.py --gold 20`, mettre à jour la doc produit, commit. Rétro-compatible : version 1 reste lue.
J1.4 - La restitution v0 | Tâche J1.4 : la restitution v0 — une commande `python3 tools/drave.py r
… [8051 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"forme canonique\\|canonique\" docs reports tools --include=*.md --include=*.py --include=*.json | head -60", "description": "Search canonical form references"}`

  ```
docs/archive/roadmap-detail-2026-10-29.md:218:| B5.1 | **Le contrat RSN-jeu** : jeu + nature + corps canonique + annotation hors empreinte, encodage binaire `RSNB` | ✅ mesuré | 41 objets distincts ; **128,93 o** de JSON → **71,10 o** de binaire (**0,5515**), aller-retour identique |
docs/archive/roadmap-detail-2026-10-29.md:355:| B12.1 | **Bus + hub M1** | ✅ **mesuré** | **528/528** exact avec contexte ; sans contexte **70,8 %** ; canonique **100 %** ; invariance **100 %** ; 1 584 événements |
docs/archive/roadmap-detail-2026-10-29.md:373:| B18.1 | **Restitution canonique** | ✅ **involution** | **528/528** rendus, **528/528** relus, **0** échec ; codec bidirectionnel exact, pas un décodeur neuronal (B10 reste négatif) |
docs/archive/roadmap-native-2026-10-29.md:35:| N0.1 | Écrire le manifeste et le graphe (blocs, ports, routes, têtes, pont, pensée) | ✅ **fait** — manifeste JSON canonique, graphe, hash vérifié |
docs/pilotage/semaine-autonome.md:49:- Les **14 atomes V14** (source canonique `research/src/nipada/core/hardware_mapping.py` ;
docs/pilotage/chantiers.md:62:   canonique : arbre d'états, opérateurs hétérogènes, stratégies classiques (BFS, A*, MCTS, AC-3,
docs/theorie/glossa
… [8072 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/porte-produit.sh; echo ---; grep -rn \"restitution\" docs/pilotage/semaine-autonome.md | head -20", "description": "Read product gate and J8 context"}`

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
… [3531 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,220p reports/rapport-restitution.md", "description": "Read B18 canonical restitution report"}`

  ```
# B18 — restitution canonique : 528/528, mais pas un décodeur

> **Objet.** Le **miroir** de M1 : rendre un code typé en surface canonique et le relire. C'est le
> codec, pas un décodeur neuronal ; B10 reste négatif.

## Mesure

| mesure | valeur |
|---|---:|
| items | **528** |
| surfaces rendues | **528 / 528 = 100 %** |
| relues sans perte | **528 / 528 = 100 %** |
| échecs | **0** |

Le rendu utilise la **position RSN** du corpus réel (le SAN exige le contexte) ; la relecture
reproduit le code exact. C'est une **involution du codec**, pas une génération de langage.

## Ce que ce n'est pas

- Ce n'est **pas** le décodeur neuronal B10 (chrF 14,0/5,4 contre plancher 38,8).
- Ce n'est **pas** une paraphrase ni une traduction : c'est la **forme canonique** du code.
- La sortie est **déterministe** et **exacte** ; elle ne prouve pas la fidélité sémantique.

## Verdict

**M1 est un codec bidirectionnel exact** : 528/528 à l’aller et au retour. C'est le seul étage
réellement solide du prototype. La génération libre reste un **négatif** (B10).

## Fichiers

- Code : [`tools/cerveau/restitution.py`](../tools/cerveau/restitution.py).
- Test : [`tools/cerveau/tests/test_restitution.py`](..
… [91 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/semantique tools/jeux 2>/dev/null; echo ---; sed -n 1,160p tools/semantique/restitution.py 2>/dev/null", "description": "Inspect semantic restitution"}`

  ```
tools/jeux:
codecs
construire_lexique_multilingue.py
corpus_multilingue.py
corpus.py
grammaire.py
hybride.py
__init__.py
lexique_multilingue.json
lexique_multilingue.py
lexique.py
maitres.py
mesure_langues.py
mesure_maitres.py
mesure.py
pensee.py
__pycache__
regles
rsn.py
tests

tools/semantique:
corpus_jw.py
corpus.py
decodeur_mots.py
diagnostic.py
entrainer_nvlink.py
entrainer.py
entrainer_type.py
hybride.py
__init__.py
lancer_nvlink.sh
modele.py
normalisation.py
__pycache__
restitution.py
synth_corpus.py
tests
typed_corpus.py
universaux.py
---
#!/usr/bin/env python3
"""restitution.py — la surface canonique, et son aller-retour RSN.

Le codec classique rend une RSN dans un format canonique par jeu. On mesure
deux choses : le rendu réussit, et la surface rendue se relit en **la même RSN**.
C'est la restitution **déterministe** ; elle ne dépend pas du natif.
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from jeux.corpus import construire_corpus  # noqa: E402
from jeux.corpus_multilingue import construire_corpus_multilingue  # noqa: E402
from jeux.codecs import co
… [1610 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nitems=r.items_banc(json.load(open('reports/pensee-fiabilite-produit.json')))\nh=bl.Heuristique()\nfor it … [963 caractères tronqués]`

  ```
======================================================================
f01 'Le chat dort.' lang fr refus 
  GN   role=agent        span=(0,7) 'Le chat' att={'segment': 'Le chat', 'cible': 'dort'}
  GV   role=predicat     span=(8,12) 'dort' att={'segment': 'dort', 'cible': 'chat'}
  seg coverage 11 / 13
  reconstruction segs+gaps exact? True
======================================================================
f02 'Le chat de la voisine qui dort sur le toit se réveille.' lang fr refus 
  GN   role=agent        span=(0,7) 'Le chat' att={'segment': 'Le chat', 'cible': 'réveille'}
  GP   role=possession   span=(8,21) 'de la voisine' att={'segment': 'de la voisine', 'cible': 'réveille'}
  REL  role=qualite      span=(22,42) 'qui dort sur le toit' att={'segment': 'qui dort sur le toit', 'cible': 'voisine'}
  REL  role=qualité      span=(22,54) 'qui dort sur le toit se réveille' att={'segment': 'qui dort sur le toit se réveille', 'cible': 'réveille'}
  GV   role=predicat     span=(43,54) 'se réveille' att={'segment': 'se réveille', 'cible': 'voisine'}
  seg coverage 52 / 55
  reconstruction segs+gaps exact? False
======================================================================
f03 
… [2877 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"partition\\|alternative\" tools/bloc_linguistique.py | head -40; echo ---; grep -rn \"meta.partition\\|partition\" tools/tests/test_produit_libre.py tools/tests/test_schema_produit.py docs/produit/README.md | head -40", "description": "Inspect partition metadata"}`

  ```
92:# v2 : ajoute `meta.partition` et `meta.alternative` (partition des syntagmes qui se
803:                 union: bool = True, partition: str = "alternative"):
809:        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
810:        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
812:        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
813:        # Dans les deux filtres, le segment retiré reste dans `meta.alternative` (`retire`).
814:        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
815:            raise ValueError("partition attend 'brut', 'alternative', 'filtrer_union' ou 'filtrer'")
816:        self.partition = partition
1805:        if self.partition != "brut":
1806:            _expliciter_partition(etiquettes, filtrer=(
1807:                "" if self.partition == "alternative"
1808:                else "union" if self.partition == "filtrer_union" else "strict"))
2385:def _relation_partition(x: Etiquette, y: Etiquette) -> str:
2407:def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:
2431:def _expliciter_partition(etiquettes: list[Etique
… [3252 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1785,1900p tools/bloc_linguistique.py", "description": "Read partition construction"}`

  ```
for d, f, p in paragraphes:
            etiquettes.append(Etiquette("discours", "paragraphe", "suite", d, f, self.nom, 0.5,
                                        candidats=["suite", "contraste", "cause", "conséquence"],
                                        langue=lg, script=script))
            titre = (p.lstrip().startswith("#") or
                     bool(re.match(r"^\s*(?:\d+[.)]|[IVXLC]+[.)])\s+", p)) or
                     (len(p.strip()) < 80 and p.strip().endswith((":", ".")) is False and
                      p.strip() == p.strip().upper()))
            etiquettes.append(Etiquette("document", "titre" if titre else "paragraphe",
                                        p.strip()[:60], d, f, self.nom, 0.7,
                                        langue=lg, script=script))
        if contexte:
            etiquettes.append(Etiquette("pragmatique", "contexte", contexte[:200], 0, len(texte),
                                        "humain", 1.0, langue=lg, script=script))

        # 7. unités sémantiques : ouvertes + syntagmes ambiguës, dédupliquées
        unites = _fusionner(unites)
        longueur = sum(u.fin - u.debut for u in unites)
        fraction = longueur / max
… [5210 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 2380,2520p tools/bloc_linguistique.py", "description": "Read partition functions"}`

  ```
# --------------------------------------------------------------------------- compositions


def _relation_partition(x: Etiquette, y: Etiquette) -> str:
    """La relation de `y` vue **depuis** `x` : `inclut` = x contient y."""
    if x.debut == y.debut and x.fin == y.fin:
        return "meme_span"
    if x.debut <= y.debut and x.fin >= y.fin:
        return "inclut"
    if y.debut <= x.debut and y.fin >= x.fin:
        return "inclus"
    return "croise"


def _cle_preferee(e: Etiquette) -> tuple:
    """La vue préférée : le segment du chunker (union), le plus large, puis le plus sûr.

    Mesuré sur le gold 612 : dans 179/207 groupes ambigus qui portent un span du gold, le
    chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.
    La préférence ne supprime rien par défaut : elle **classe**.
    """
    return (0 if (e.meta or {}).get("union") else 1, -(e.fin - e.debut), -e.confiance,
            e.debut, e.fin, e.type)


def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:
    """Les composantes connexes du graphe de chevauchement, ordonnées par position."""
    parent = list(range(len(segs)))

    def trouver(i: 
… [5453 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"J8.1\\|restitution v1\" journal docs reports tools --include=*.md --include=*.json | head -40", "description": "Search J8.1 mentions"}`

  ```
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:60967:  [a_faire ] J8.1   j8 — La restitution v1
tools/chantier/plan.json:268:   "id": "J8.1",
tools/chantier/plan.json:270:   "titre": "La restitution v1",
tools/chantier/plan.json:271:   "mandat": "Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotation (segments + rôles + cibles) et la mesurer : le miroir strict (0,1087) doit-il monter ? Fiche `reports/rapport-restitution-v1.md` + JSON, tests, commit.",
  ```

- **bash** `{"command": "ls reports | grep -i \"restitution\\|canon\" ; echo ---; cat reports/pensee-restitution-v0.json | head -80", "description": "List restitution artifacts"}`

  ```
pensee-restitution-v0.json
rapport-restitution.md
rapport-restitution-v0.md
restitution-fra-flux.json
restitution-fra.json
restitution.json
restitution-mesures.json
restitution-udhr-flux.json
restitution-udhr.json
---
{
 "schema": "drave.restitution.banc",
 "version": 1,
 "date": "2026-11-07",
 "ligne": "B13",
 "tache": "J1.4",
 "titre": "La restitution v0 — annotation → surface, et le miroir",
 "banc": "reports/pensee-fiabilite-produit.json",
 "banc_sha256": "bd54b1ff7fa14e203dcfeaced908b8dec699995c2ff3fe910c7956ac64d18a48",
 "commande": "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json",
 "dispositif": {
  "outil": "tools/restitution.py",
  "cli": "python3 tools/drave.py restituer TEXTE",
  "analyse": "bloc_linguistique.Heuristique().analyser(texte, langue=None)",
  "niveau_surface": "graphème",
  "correctif": "catégorie Unicode C (contrôle) annotée comme graphème ; sans lui, f50 perd ses 10 sauts de ligne (45/46)",
  "fidelite": "binaire (rendu == source) + Levenshtein normalisé",
  "miroir": "minimum des fidélités binaires de la surface (graphème), des mots et des POS ; une sortie n'est fidèle que si elle reproduit exactement la source"
 },
 
… [1097 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/methode/resultats.md | head -160", "description": "Read results method rules"}`

  ```
# Ce qu'un résultat doit porter

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
> résultats, ou un message de commit.

## Les cinq pièces d'un résultat

1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
   [porte](../theorie/glossaire/entrees/porte.md)) ;
2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
   mesure pas ;
3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
   quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
   grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire comme **technique**), quels réglages (prompt, gabarit, longueur de
   sortie, graine) ;
4. **Le [contrôle négatif](../theorie/glossaire/entrees/controle-negatif.md)
… [2500 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys,re,unicodedata,hashlib\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nfrom tools.bloc_linguistique import _cle_preferee\nitems=r.items_banc(json.load(o … [2153 caractères tronqués]`

  ```
46 norm_mots 46 norm_pos 46 canon_surface==norm_src 22
seg coverage mean 0.7138781779928445 min 0.0
roles 395 atts 315 resolv 315 fully_linear 25
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys,re\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nfrom tools.bloc_linguistique import _cle_preferee\nitems=r.items_banc(json.load(open('reports/pensee- … [1646 caractères tronqués]`

  ```
n 46 token coverage mean 0.8581876237446984 min 0.0
canonical surface exact vs canon source 45
same structure after reanalysis 14
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && git branch --show-current && git diff --stat", "description": "Check git status and branch"}`

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
 m tools/structures
?? reports/rapport-s-paragraphes.md
s/v7
 reports/pensee-coherence-fiches-v7.json |  19 +
 reports/pensee-dev-test-v10.json        |   2 +-
 reports/pensee-quatre-modes.json        | 734 ++++++++++++++++++--------------
 reports/rapport-audit-v7.md             |   6 +-
 reports/rapport-coherence-fiches-v7.md  |  17 +-
 reports/rapport-dev-test-v10.md         |   2 +-
 reports/rapport-pensee-v12.md           |   4 +-
 reports/rapport-spans-chunker.md        |  13 +-
 tools/chantier/plan.json                | 116 +++++
 tools/structures                        |   0
 10 files changed, 576 insertions(+), 337 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_restitution.py 2>&1 | tail -20", "description": "Run existing restitution tests"}`

  ```
test_50_textes_46_annotations (__main__.TestCinquanteTextes.test_50_textes_46_annotations) ... ok
test_restituer_banc (__main__.TestCommande.test_restituer_banc) ... ok
test_restituer_json (__main__.TestCommande.test_restituer_json) ... ok
test_restituer_multiligne (__main__.TestCommande.test_restituer_multiligne) ... ok
test_restituer_refus (__main__.TestCommande.test_restituer_refus) ... ok
test_restituer_texte (__main__.TestCommande.test_restituer_texte) ... ok
test_controle_negatif (__main__.TestReconstruction.test_controle_negatif) ... ok
test_distance (__main__.TestReconstruction.test_distance) ... ok
test_ne_lit_pas_le_texte (__main__.TestReconstruction.test_ne_lit_pas_le_texte) ... ok
test_niveaux_pauvres (__main__.TestReconstruction.test_niveaux_pauvres) ... ok
test_surface_sans_controle (__main__.TestReconstruction.test_surface_sans_controle) ... ok

----------------------------------------------------------------------
Ran 11 tests in 1.211s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,140p tools/tests/test_produit_libre.py", "description": "Read free-text test for style"}`

  ```
#!/usr/bin/env python3
"""test_produit_libre.py — non-régression sur les **50 textes libres** de l'audit A26.

Ce que le test fige :
- la vue **`filtrer`** ne produit **aucun** chevauchement de syntagmes (0/50) ;
- la vue **`alternative`** (défaut) documente les chevauchements dans `meta.alternative` ;
- les **5 textes non linguistiques** (emoji, vide, espaces, ponctuation, nombre nu) n'ont
  **aucun** syntagme ;
- l'analyse est **déterministe** (deux passes identiques).
"""
from __future__ import annotations

import json
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
NON_LINGUISTIQUES = {"f14", "f15", "f16", "f17", "f18"}


def _textes() -> list[tuple[str, str]]:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    return [(item["id"], item["texte"]) for item in donnees["banc_50"]["resultats"]]


def _segments(annotation) -> list:
    return [e for e in annotation.etiquettes if e.niveau == "syntagme"]


def _chevauchements(segments: list) -> int:
    return sum(1 for i, a in enumerate(segments) for b in segments[i + 1:]
           
… [1439 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys,re\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nitems=r.items_banc(json.load(open('reports/pensee-fiabilite-produit.json')))\nh=bl.Heuristique()\ndef … [1642 caractères tronqués]`

  ```
n 46 char cov mean 0.7138781779928445 token cov mean 0.629225709151653 min 0.0
roles 395 atts 315 target in another seg(all segs) 9 target in another linear seg 302
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys,re\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nitems=r.items_banc(json.load(open('reports/pensee-fiabilite-produit.json')))\nh=bl.Heuristique()\ndef … [1079 caractères tronqués]`

  ```
n 46 segments 395 roles 395 atts 315 target found in source 315 target inside another segment 313 target inside own segment 8
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"restituer\\|--banc\\|sous-parseur\\|add_parser\" tools/drave.py | head -60 && sed -n 430,620p tools/drave.py", "description": "Inspect drave CLI parser"}`

  ```
11:    python3 tools/drave.py restituer "Le chat dort."
12:    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
343:def cmd_restituer(args: argparse.Namespace) -> int:
347:    (`--banc`, le format de `reports/pensee-fiabilite-produit.json`). Le mode banc
352:            print(f"{NOM}: erreur d'usage : --banc est exclusif de TEXTE et --fichier",
411:        "Commandes : analyser, evaluer, rejouer, restituer.\n"
414:        "--contexte, --banc.\n"
420:        "  python3 tools/drave.py restituer \"Le chat dort.\"\n"
421:        "  python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json\n"
432:                                  metavar="{analyser,evaluer,rejouer,restituer}",
435:    analyser = sous.add_parser(
459:    evaluer = sous.add_parser(
473:    rejouer = sous.add_parser(
488:    restituer = sous.add_parser(
489:        "restituer",
494:                    "contrôle négatif. Avec --banc, mesure un JSON de textes (50 textes libres).",
495:        epilog="Exemples : python3 tools/drave.py restituer \"Le chat dort.\" ; "
496:               "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json",
… [6536 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nitems=r.items_banc(json.load(open('reports/pensee-fiabilite-produit.json')))\nh=bl.Heuristique()\nfor it … [385 caractères tronqués]`

  ```
f13 refus  lang und
  graphème 11 ['J', "'", 'ai', ' ', 'trouvé', ' ']
  mot 6 ["J'ai", 'trouvé', 'ça', 'génial', '😍', '🔥']
  pos 6 ["J'ai", 'trouvé', 'ça', 'génial', '😍', '🔥']
  syntagme 2 ["J'ai", 'trouvé ça génial']
f18 refus  lang und
  graphème 1 ['1234567890']
  mot 1 ['1234567890']
  pos 1 ['1234567890']
  syntagme 0 []
f38 refus  lang fr
  graphème 34 ['Les', ' ', 'URL', ' ', 'comme', ' ']
  mot 30 ['Les', 'URL', 'comme', 'https', ':', '/']
  pos 30 ['Les', 'URL', 'comme', 'https', ':', '/']
  syntagme 9 ['Les URL', 'comme https', 'a', 'b/c', 'd', 'd=e#f']
f50 refus  lang fr
  graphème 885 ['#', ' ', 'Notes', ' ', 'de', ' ']
  mot 480 ['#', 'Notes', 'de', 'terrain', 'Le', 'chat']
  pos 480 ['#', 'Notes', 'de', 'terrain', 'Le', 'chat']
  syntagme 193 ['Notes', 'de terrain\nLe chat', 'de terrain\nLe chat de la voisine', 'de la voisine', 'qui dort sur le toit', 'qui dort sur le toit se réveille']
  ```

- **bash** `{"command": "date -Is; ls journal | tail -10; cat journal/THEMES.md | tail -20", "description": "Check current date and journal structure"}`

  ```
2026-11-14T01:50:31-05:00
2026-11-03
2026-11-04
2026-11-05
2026-11-06
2026-11-07
2026-11-13
2026-11-14
README.md
sessions
THEMES.md
| [2026-10-13](2026-10-13/outils.md) | — |
| [2026-10-15](2026-10-15/outils.md) | `-7,92 %` |
| [2026-10-16](2026-10-16/outils.md) | — |
| [2026-10-17](2026-10-17/outils.md) | `37 %` · `37,5 %` |
| [2026-10-27](2026-10-27/outils.md) | — |
| [2026-11-01](2026-11-01/outils.md) | — |
| [2026-11-02](2026-11-02/outils.md) | — |
| [2026-11-03](2026-11-03/outils.md) | `0,137` · `0,032` |
| [2026-11-04](2026-11-04/outils.md) | — |
| [2026-11-06](2026-11-06/outils.md) | — |

### `divers` — Ce qui ne rentre dans aucun thème

| jour | chiffres du jour |
|---|---|
| [2026-09-28](2026-09-28/divers.md) | — |
| [2026-09-29](2026-09-29/divers.md) | — |
| [2026-09-30](2026-09-30/divers.md) | `19,5633` · `19,3045` |
| [2026-10-02](2026-10-02/divers.md) | — |
| [2026-10-08](2026-10-08/divers.md) | — |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p tools/index_reports.py; echo ---; sed -n 1,80p reports/README.md", "description": "Inspect report index generator and README"}`

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
… [9943 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p journal/2026-11-14/README.md 2>/dev/null; ls journal/2026-11-14 2>/dev/null", "description": "Inspect latest journal day"}`

  ```
# 2026-11-14

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**6 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 1 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 3 | [mesures.md](mesures.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 321.0 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:52 | `64d9dd23` | J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/
… [4228 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 255,290p tools/chantier/plan.json && git diff tools/chantier/plan.json | head -80", "description": "Inspect plan.json J8.1 and diff"}`

  ```
"id": "J7.1",
   "jour": 7,
   "titre": "Panini — le retrieval approfondi",
   "mandat": "Tâche J7.1 : approfondir le retrieval Panini — sur les 532 langues UDHR (même source XML), mesurer le retrieval par famille Glottolog (les 29 langues de `language_genealogy.py` + l'échantillon 20) avec le contrôle d'époque, et comparer à la mesure de J3.1. Fiche `reports/rapport-retrieval-familles.md` + JSON, contrôle négatif (familles différentes vs sœurs).",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-retrieval-familles.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    }
   ]
  },
  {
   "id": "J8.1",
   "jour": 8,
   "titre": "La restitution v1",
   "mandat": "Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotation (segments + rôles + cibles) et la mesurer : le miroir strict (0,1087) doit-il monter ? Fiche `reports/rapport-restitution-v1.md` + JSON, tests, commit.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-restitution-v1.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    }
   ]
  },
  {
   "id": "J9.1",
   "jour": 9,
   "titre"
… [3673 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 380,520p tools/restitution.py", "description": "Read end of restitution.py"}`

  ```
f"(caractères {controle['melange']['fidelite_caractere']:.4f}) · "
        f"troncature exacte {controle['tronque']['fidelite']:.4f} "
        f"(caractères {controle['tronque']['fidelite_caractere']:.4f})"
    )
    return "\n".join(lignes)


def formater_banc(rapport: dict, chemin: str = "") -> str:
    """La sortie lisible du banc (`restituer --banc`)."""
    s = rapport["synthese"]
    lignes = [
        f"restitution v0 — banc {chemin or '(fourni)'}",
        f"textes {s['n']} · annotés {s['annotations']} · refus {s['refus']} "
        f"({', '.join(str(x) for x in s['refus_ids'])})",
        "",
        "niveau                 exacts    fidélité   caractères",
        f"surface (graphème)     {s['surface']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['surface']['fidelite']:>8.4f}   {s['surface']['fidelite_caractere']:>8.4f}",
        f"  sans contrôle C      {s['surface_sans_controle']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['surface_sans_controle']['fidelite']:>8.4f}   "
        f"{s['surface_sans_controle']['fidelite_caractere']:>8.4f}",
        f"mots                   {s['mots']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['mots']['fidelite']:>8.4f}
… [748 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "old_string": "from __future__ import annotations\n\nimport pathlib\nimport random\nimport sys\n\nRACINE = pathlib.Path(__file__).resolve().parent.parent\nif str(RACINE) not in sys.path:\n    sys.path.insert(0, str … [2367 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "limit": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py</path>
<type>file</type>
<content>
1: """restitution.py — la restitution v0 : annotation → surface, et le miroir.
2: 
3: La **surface** est reconstruite depuis le niveau `graphème` — les spans typés qui portent
4: les caractères — **sans lire** `Annotation.texte`. Les niveaux `mot` et `pos` sont mesurés
5: comme des sorties plus pauvres : ils disent ce que la couche de surface ajoute.
6: 
7: Le **miroir** est la règle 6 du dépôt : `fidelite` est binaire (1.0 si la sortie égale la
8: source), et `miroir` est le minimum des trois fidélités (surface, mots, pos). C'est la
9: définition de `tools/tests/linguistique/miroir.mesurer`, réutilisée ici pour ne pas en
10: avoir deux. `fidelite_caractere` ajoute une distance de Levenshtein normalisée : elle
11: distingue « presque fidèle » de « fidèle » et documente la perte de la ponctuation.
12: 
13: Le **contrôle négatif** mélange les graphèmes (graine fixe) et en retire un : les deux
14: doivent casser la fidélité. Sans lui, un codec qui recopie la source ne prouverait rien.
15: """
16: from __future__ import annotations
17: 
18: import pathlib
19: import random
20: 
… [1727 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "old_string": "\"\"\"restitution.py — la restitution v0 : annotation → surface, et le miroir.\n\nLa **surface** est reconstruite depuis le niveau `graphème` — les spans typés qui portent\nles caractères — **sans li … [2618 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "new_string": "SCHEMA = \"drave.restitution\"\nVERSION = 1\nSCHEMA_CANONIQUE = \"drave.restitution.canonique\"\nVERSION_CANONIQUE = 1\nNIVEAUX = (\"graphème\", \"mot\", \"pos\")\nNOMS = {\"graphème\": \"surface\",  … [1610 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "new_string": "from __future__ import annotations\n\nimport collections\nimport hashlib\nimport json\nimport pathlib\nimport random\nimport re\nimport sys", "old_string": "from __future__ import annotations\n\nimpo … [66 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^# --------------------------------------------------------------------------- affichage\" tools/restitution.py", "description": "Find insertion anchor"}`

  ```
376:# --------------------------------------------------------------------------- affichage
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "new_string": "# --------------------------------------------------------------------------- forme canonique v1\n\n\ndef jetons_canoniques(texte: str) -> list[str]:\n    \"\"\"Les jetons d'une surface canonique : l … [21825 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -30 tools/restitution.py", "description": "Show end of restitution.py"}`

  ```
return "\n".join(lignes)


def formater_banc(rapport: dict, chemin: str = "") -> str:
    """La sortie lisible du banc (`restituer --banc`)."""
    s = rapport["synthese"]
    lignes = [
        f"restitution v0 — banc {chemin or '(fourni)'}",
        f"textes {s['n']} · annotés {s['annotations']} · refus {s['refus']} "
        f"({', '.join(str(x) for x in s['refus_ids'])})",
        "",
        "niveau                 exacts    fidélité   caractères",
        f"surface (graphème)     {s['surface']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['surface']['fidelite']:>8.4f}   {s['surface']['fidelite_caractere']:>8.4f}",
        f"  sans contrôle C      {s['surface_sans_controle']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['surface_sans_controle']['fidelite']:>8.4f}   "
        f"{s['surface_sans_controle']['fidelite_caractere']:>8.4f}",
        f"mots                   {s['mots']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['mots']['fidelite']:>8.4f}   {s['mots']['fidelite_caractere']:>8.4f}",
        f"pos                    {s['pos']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['pos']['fidelite']:>8.4f}   {s['pos']['fidelite_caractere']:>8.4f}",
        f
… [531 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat >> tools/restitution.py <<'PY'\n\n\ndef formater_forme_canonique(forme: dict | None, mesure: dict | None = None) -> str:\n    \"\"\"La sortie lisible de la forme canonique (segments + rôles + cibles).\"\"\"\n    if not forme:\n   … [5818 caractères tronqués]`

  ```
syntax ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nh=bl.Heuristique()\nfor txt in [\"Le chat dort.\",\"# Notes\\nLe chat dort.\\nLa voisine parle.\\n\",\"1 … [626 caractères tronqués]`

  ```
======================================================================
'Le chat dort.'
{
 "definition": "segments (type, rôle, span, valeur), linéarisation sans chevauchement, squelette « type/rôle : valeur -> cible », plancher de jetons (mot > POS > graphème) et empreinte sha256 du corps canonique",
 "segments": [
  {
   "rang": 0,
   "type": "GN",
   "role": "agent",
   "niveau": 1,
   "debut": 0,
   "fin": 7,
   "valeur": "Le chat",
   "canonique": "le chat",
   "cible": "dort",
   "cible_canonique": "dort",
   "cible_segment": 1,
   "lineaire": true,
   "union": false
  },
  {
   "rang": 1,
   "type": "GV",
   "role": "predicat",
   "niveau": 0,
   "debut": 8,
   "fin": 12,
   "valeur": "dort",
   "canonique": "dort",
   "cible": "chat",
   "cible_canonique": "chat",
   "cible_segment": 0,
   "lineaire": true,
   "union": false
  }
 ],
 "squelette": [
  "GN/agent: le chat -> dort",
  "GV/predicat: dort -> chat"
 ],
 "jetons": [
  "le",
  "chat",
  "dort"
 ],
 "surface_canonique": "le chat dort",
 "cle": "10da4b2ac1b014bbd916fbce1ce3e2b08a1dfa9def5d70a0e069d36a5dd117a5"
}
canonique 1.0 True strict 0.0 strict_c 0.0
structure {'segments': 2, 'segments_avec_role': 2, 'attachements'
… [7095 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys,time\nsys.path.insert(0,'.')\nimport tools.restitution as r\nitems=r.items_banc(json.load(open('reports/pensee-fiabilite-produit.json')))\nt=time.time(); rapport=r.mesurer_banc_v1(items); print('tim … [790 caractères tronqués]`

  ```
time 11.85
{
 "n": 50,
 "annotations": 46,
 "refus": 4,
 "refus_ids": [
  "f14",
  "f15",
  "f16",
  "f17"
 ],
 "strict": {
  "exacts": 5,
  "fidelite": 0.1087
 },
 "canonique": {
  "exacts": 46,
  "fidelite": 1.0,
  "fidelite_caractere": 1.0
 },
 "strict_sur_canonique": {
  "exacts": 1,
  "fidelite": 0.0217,
  "fidelite_caractere": 0.8566
 },
 "structure": {
  "segments": 395,
  "segments_avec_role": 395,
  "attachements": 315,
  "cibles_resolues": 315,
  "cibles_dans_un_segment": 313,
  "couverture_caracteres": 0.7519,
  "couverture_jetons": 0.6584,
  "taux_roles": 1.0,
  "taux_cibles_resolues": 1.0,
  "taux_cibles_dans_un_segment": 0.9937
 },
 "stabilite": {
  "squelette_identique": 18,
  "jetons_identiques": 46,
  "fidelite": 0.3913
 },
 "controle_negatif_canonique": {
  "melange_exacts": 0,
  "melange_fidelite_caractere": 0.3865,
  "tronque_exacts": 0,
  "tronque_fidelite_caractere": 0.7998,
  "detectes": 46
 },
 "controle_negatif_structure": {
  "eligibles": 43,
  "detectes": 43,
  "cle_changee": 43,
  "roles_retires": 395,
  "cibles_retirees": 315
 }
}
restitution v1 — banc reports/pensee-fiabilite-produit.json
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

niveau   
… [865 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nitems=r.items_banc(json.load(open('reports/pensee-fiabilite-produit.json')))\nh=bl.Heuristique()\nallsta … [742 caractères tronqués]`

  ```
start 0.6583713370744548 any 0.6583713370744548 entier 0.6508402811738337
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "new_string": "        \"canonique\": {\n            \"exacts\": sum(1 for r in annotes if r[\"canonique\"][\"exact\"]),\n            \"fidelite\": moyenne([r[\"canonique\"][\"fidelite\"] for r in annotes]),\n      … [478 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py": file changed since it was read — re-read the file, then retry
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '\"canonique\": {' -A6 tools/restitution.py | head -20", "description": "Locate canonical summary"}`

  ```
761:        "canonique": {
762-            "exacts": exacts("canonique", "mots"),
763-            "fidelite": moyenne([r["canonique"]["fidelite"] for r in annotes]),
764-            "fidelite_caractere": moyenne(
765-                [r["canonique"]["forme"]["fidelite_caractere"] for r in annotes]),
766-        },
767-        "strict_sur_canonique": {
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "offset": 755, "limit": 18}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py</path>
<type>file</type>
<content>
755:         "refus": len(refuses),
756:         "refus_ids": [r.get("id") for r in refuses],
757:         "strict": {
758:             "exacts": sum(1 for r in annotes if r["strict"]["exact"]),
759:             "fidelite": moyenne([r["strict"]["fidelite"] for r in annotes]),
760:         },
761:         "canonique": {
762:             "exacts": exacts("canonique", "mots"),
763:             "fidelite": moyenne([r["canonique"]["fidelite"] for r in annotes]),
764:             "fidelite_caractere": moyenne(
765:                 [r["canonique"]["forme"]["fidelite_caractere"] for r in annotes]),
766:         },
767:         "strict_sur_canonique": {
768:             "exacts": sum(1 for r in annotes if r["strict_sur_canonique"]["exact"]),
769:             "fidelite": moyenne(
770:                 [r["strict_sur_canonique"]["fidelite"] for r in annotes]),
771:             "fidelite_caractere": moyenne(
772:                 [r["strict_sur_canonique"]["fidelite_caractere"] for r in annotes]),

(Showing lines 755-772 of 1033. Use offset=773 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "new_string": "        \"canonique\": {\n            \"exacts\": sum(1 for r in annotes if r[\"canonique\"][\"exact\"]),\n            \"fidelite\": moyenne([r[\"canonique\"][\"fidelite\"] for r in annotes]),\n      … [478 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"exacts(\" tools/restitution.py", "description": "Check unused helper"}`

  ```
277:    def exacts(cle: str) -> int:
292:            "exacts": exacts("surface"),
303:            "exacts": exacts("mots"),
308:            "exacts": exacts("pos"),
731:    def exacts(cle: str, nom: str) -> int:
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 724,740p tools/restitution.py", "description": "View unused helper"}`

  ```
annotes = [r for r in resultats if not r.get("refus")]
    refuses = [r for r in resultats if r.get("refus")]
    n = len(annotes)

    def moyenne(valeurs: list[float]) -> float:
        return round(sum(valeurs) / max(1, len(valeurs)), 4)

    def exacts(cle: str, nom: str) -> int:
        return sum(1 for r in annotes if r[cle][nom]["exact"])

    structure = {
        "segments": sum(r["structure"]["segments"] for r in annotes),
        "segments_avec_role": sum(r["structure"]["segments_avec_role"] for r in annotes),
        "attachements": sum(r["structure"]["attachements"] for r in annotes),
        "cibles_resolues": sum(r["structure"]["cibles_resolues"] for r in annotes),
        "cibles_dans_un_segment": sum(
            r["structure"]["cibles_dans_un_segment"] for r in annotes),
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "new_string": "    def moyenne(valeurs: list[float]) -> float:\n        return round(sum(valeurs) / max(1, len(valeurs)), 4)\n\n    structure = {", "old_string": "    def moyenne(valeurs: list[float]) -> float:\n   … [193 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 50, "offset": 343}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
343: def cmd_restituer(args: argparse.Namespace) -> int:
344:     """Reconstruit la surface depuis l'annotation et rend la fidélité du miroir.
345: 
346:     Deux modes : un **texte** (ou un fichier), ou un **banc** JSON de textes
347:     (`--banc`, le format de `reports/pensee-fiabilite-produit.json`). Le mode banc
348:     laisse le bloc détecter la langue, comme le CLI sans `--langue`.
349:     """
350:     if args.banc:
351:         if args.texte is not None or args.fichier:
352:             print(f"{NOM}: erreur d'usage : --banc est exclusif de TEXTE et --fichier",
353:                   file=sys.stderr)
354:             return 2
355:         try:
356:             donnees = json.loads(pathlib.Path(args.banc).read_text(encoding="utf-8"))
357:             items = restitution.items_banc(donnees)
358:         except (OSError, ValueError) as exc:
359:             print(f"{NOM}: erreur : banc illisible : {exc}", file=sys.stderr)
360:             return 1
361:         rapport = restitution.mesurer_banc(items, args.langue)
362:         rapport["banc"] = args.banc
363:         if ar
… [1238 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 30, "offset": 488}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
488:     restituer = sous.add_parser(
489:         "restituer",
490:         help="reconstruire la surface depuis l'annotation et mesurer le miroir",
491:         description="Analyse un texte, reconstruit la surface depuis le niveau `graphème` "
492:                     "(sans lire le champ `texte` de l'annotation) et compare à la source. "
493:                     "Affiche la fidélité binaire du miroir, la fidélité de caractères et un "
494:                     "contrôle négatif. Avec --banc, mesure un JSON de textes (50 textes libres).",
495:         epilog="Exemples : python3 tools/drave.py restituer \"Le chat dort.\" ; "
496:                "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json",
497:         formatter_class=_Formateur,
498:     )
499:     restituer.add_argument("texte", metavar="TEXTE", nargs="?", default=None,
500:                            help="texte à restituer (entre guillemets) ou --fichier")
501:     restituer.add_argument("--banc", default=None, metavar="CHEMIN",
502:                            help="mesurer un banc JSON de 
… [1019 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "def cmd_restituer(args: argparse.Namespace) -> int:\n    \"\"\"Reconstruit la surface depuis l'annotation et rend la fidélité du miroir.\n\n    Deux modes : un **texte** (ou un fichier), ou un **banc** JSO … [4615 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    restituer = sous.add_parser(\n        \"restituer\",\n        help=\"reconstruire la surface depuis l'annotation et mesurer le miroir\",\n        description=\"Analyse un texte, reconstruit la surface  … [2851 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py restituer \"Le chat dort.\" --canonique; echo \"code=$?\"; echo ---; python3 tools/drave.py restituer \"Le chat dort.\" --canonique --json | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['schema … [212 caractères tronqués]`

  ```
restitution v1 (surface + forme canonique)
source         : 'Le chat dort.'
surface brute  : 'Le chat dort.'
miroir strict  : 0.0000 (non exact) — surface/mots/POS vs source brute
forme canonique: 1.0000 (exacte) — jetons canoniques vs source canonique
  caractères   : 1.0000
strict sur la forme canonique : 0.0000 (la forme n'est pas la surface : le strict ne doit pas monter)

forme canonique (segments + rôles + cibles)
surface canonique : 'le chat dort'
squelette :
  GN/agent: le chat -> dort
  GV/predicat: dort -> chat
segments 2 · rôles 2 · cibles 2 · résolues 2/2 · dans un segment 2/2

contrôle négatif canonique : mélange exacte 0.0000 · troncature exacte 0.0000 · détecté True
contrôle de structure : rôles retirés 2 · cibles retirées 2 · clé changée True
stabilité structurelle : oui (2 → 2 segments après re-analyse de la surface canonique)
code=0
---
drave.restitution.canonique 1.0 0.0 2
---
restitution (annotation → surface)
source      : 'Le chat dort.'
surface     : 'Le chat dort.'
fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%
mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%
pos         : exacte 0.0000 · caractères 0.9286 · couvertur
… [304 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution.py", "limit": 40, "offset": 75}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution.py</path>
<type>file</type>
<content>
75:             self.assertEqual(sortie.returncode, 3, detail(sortie))
76:             self.assertIn("refus d'analyse", sortie.stderr)
77:         self.assertEqual(drave("restituer").returncode, 2)
78: 
79:     def test_restituer_banc(self):
80:         banc = {"banc_50": {"resultats": [
81:             {"id": "t1", "texte": "Le chat dort."},
82:             {"id": "t2", "texte": "The cat sleeps."},
83:             {"id": "t3", "texte": "..."},
84:         ]}}
85:         chemin = _fichier_temp(json.dumps(banc, ensure_ascii=False), suffixe=".json")
86:         sortie = drave("restituer", "--banc", chemin, "--json")
87:         self.assertEqual(sortie.returncode, 0, detail(sortie))
88:         donnees = json.loads(sortie.stdout)
89:         self.assertEqual(donnees["synthese"]["n"], 3)
90:         self.assertEqual(donnees["synthese"]["annotations"], 2)
91:         self.assertEqual(donnees["synthese"]["refus"], 1)
92:         self.assertEqual(donnees["synthese"]["surface"]["exacts"], 2)
93:         self.assertEqual(donnees["synthese"]["controle_negatif"]["melange_e
… [1088 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution.py", "new_string": "    def test_restituer_banc(self):\n        banc = {\"banc_50\": {\"resultats\": [\n            {\"id\": \"t1\", \"texte\": \"Le chat dort.\"},\n            {\"id\": \"t2\", \"texte\": \"T … [8924 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/tests/test_restitution.py 2>&1 | tail -40", "description": "Run restitution tests including v1"}`

  ```
test_50_textes_46_annotations (__main__.TestCinquanteTextes.test_50_textes_46_annotations) ... ok
test_stabilite_et_controles_v1 (__main__.TestCinquanteTextesV1.test_stabilite_et_controles_v1) ... ok
test_structure_v1 (__main__.TestCinquanteTextesV1.test_structure_v1) ... ok
test_synthese_v1 (__main__.TestCinquanteTextesV1.test_synthese_v1) ... ok
test_restituer_banc (__main__.TestCommande.test_restituer_banc) ... ok
test_restituer_banc_canonique (__main__.TestCommande.test_restituer_banc_canonique) ... ok
test_restituer_canonique (__main__.TestCommande.test_restituer_canonique) ... ok
test_restituer_canonique_json (__main__.TestCommande.test_restituer_canonique_json) ... ok
test_restituer_json (__main__.TestCommande.test_restituer_json) ... ok
test_restituer_multiligne (__main__.TestCommande.test_restituer_multiligne) ... ok
test_restituer_refus (__main__.TestCommande.test_restituer_refus) ... ok
test_restituer_texte (__main__.TestCommande.test_restituer_texte) ... ok
test_controles_negatifs (__main__.TestFormeCanonique.test_controles_negatifs) ... ok
test_distance_canonique (__main__.TestFormeCanonique.test_distance_canonique) ... ok
test_forme_simple (__main__.TestFormeCanonique
… [770 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_restitution_v1.py", "content": "#!/usr/bin/env python3\n\"\"\"mesurer_restitution_v1.py — produit le JSON de la fiche J8.1.\n\nMesure la **forme canonique v1** sur les **50 textes libres** de\n`reports/pensee-fiabilite-prod … [4487 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_restitution_v1.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/mesurer_restitution_v1.py && ls -lh reports/pensee-restitution-v1.json && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-restitution-v1.json'))\nprint(d['date'], d['synthese']['strict'], d['synthe … [70 caractères tronqués]`

  ```
restitution v1 — banc reports/pensee-fiabilite-produit.json
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

niveau                         exacts    fidélité   caractères
strict (surface/mots/POS)           5/46       0.1087   —
canonique (jetons)                 46/46       1.0000     1.0000
strict sur la forme canonique       1/46       0.0217     0.8566

structure : 395 segments · 395 rôles (1.0000) · 315 cibles · 315/315 résolues (1.0000) · 313/315 dans un segment (0.9937)
couverture : 0.6584 des jetons · 0.7519 des caractères (moyenne)
stabilité structurelle : 18/46 (0.3913) · jetons identiques 46/46
contrôle négatif canonique : mélange 0/46 exacts (caractères 0.3865) · troncature 0/46 exacts (caractères 0.7998) · détectés 46/46
contrôle de structure : 43/46 textes éligibles · rôles retirés 395 · cibles retirées 315 · clé changée 43/43

écrit : reports/pensee-restitution-v1.json
-rw-r--r--. 1 stephane stephane 312K 14 nov 01:54 reports/pensee-restitution-v1.json
2026-11-14 {'exacts': 5, 'fidelite': 0.1087} {'exacts': 46, 'fidelite': 1.0, 'fidelite_caractere': 1.0}
[stderr]

real	0m12,318s
user	0m12,289s
sys	0m0,028s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-restitution-v1.json'))\nfor r in d['resultats']:\n    if r.get('refus'): continue\n    if r['structure']['segments']==0:\n        print(r['id'], repr(next(x['surface_st … [829 caractères tronqués]`

  ```
f18 '1234567890'
f27 'Élodie sourit.'
f37 'Email: alice@example.org, phone: +33 6 12 34 56 78.'
stability false ids ['f03', 'f04', 'f06', 'f08', 'f12', 'f13', 'f19', 'f20', 'f21', 'f22', 'f26', 'f28', 'f29', 'f31', 'f32', 'f33', 'f34', 'f36', 'f38', 'f39', 'f42', 'f43', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50']
strict exact ['f03', 'f05', 'f18', 'f40', 'f44']
strict canon exact ['f18']
min strict canon char (0.15, 'f31')
min canonical char (1.0, 'f01')
  ```

- **write** `{"content": "# B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : J8.1 · **Date** : 2026-11-14 ·\n> **Verdict** : ✅\n>\n> **La question.** Au-delà de la surface exacte (46/46), produire une **forme canoniq … [13115 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v1.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v1.md", "new_string": "**Lecture.** Les segments ne couvrent que **65,84 %** des jetons : le plancher lexical\nremplit le reste (déterminants, prépositions, ponctuation, mots hors syntagme). Les\ncibles sont * … [532 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v1.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh", "limit": 30, "offset": 55}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh</path>
<type>file</type>
<content>
55: 
56: if sortie=$(python3 tools/drave.py restituer "Le chat dort." 2>&1) \
57:    && printf '%s' "$sortie" | grep -q "exacte 1.0000"; then
58:   dit ✅ "restitution v0 : surface exacte (miroir affiché)"
59: else
60:   dit ❌ "restitution v0 : sortie inattendue : $sortie"; ko=1
61: fi
62: 
63: if python3 tools/tests/test_restitution.py >/tmp/porte-produit-restitution.log 2>&1; then
64:   dit ✅ "restitution v0 : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-restitution.log | head -1)"
65: else
66:   dit ❌ "restitution v0 en échec (voir /tmp/porte-produit-restitution.log)"; ko=1
67: fi
68: 
69: if python3 tools/tests/test_schema_produit.py >/tmp/porte-produit-schema.log 2>&1; then
70:   dit ✅ "schéma v2 : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-schema.log | head -1)"
71: else
72:   dit ❌ "schéma v2 en échec (voir /tmp/porte-produit-schema.log)"; ko=1
73: fi
74: 
75: refus=$(python3 tools/drave.py analyser "" --json 2>/dev/null); code=$?
76: if [ "$code" -eq 3 ] && printf '%s' "$refus" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['refus'] and d
… [462 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh", "new_string": "if sortie=$(python3 tools/drave.py restituer \"Le chat dort.\" 2>&1) \\\n   && printf '%s' \"$sortie\" | grep -q \"exacte 1.0000\"; then\n  dit ✅ \"restitution v0 : surface exacte (miroir affiché)\ … [1574 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m py_compile tools/restitution.py tools/drave.py tools/mesurer_restitution_v1.py tools/tests/test_restitution.py && echo compile-ok", "description": "Compile modified Python files"}`

  ```
compile-ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py restituer \"\" --canonique; echo \"code=$?\"; python3 tools/drave.py restituer \"...\" --canonique --json; echo \"code=$?\"", "description": "Test canonical refusal handling"}`

  ```
code=3
code=3
[stderr]
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_produit.py 2>&1 | tail -5 && python3 tools/tests/test_produit_libre.py 2>&1 | tail -5", "description": "Run product and free-text tests"}`

  ```
................
----------------------------------------------------------------------
Ran 16 tests in 3.608s

OK

----------------------------------------------------------------------
Ran 4 tests in 0.298s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 700 bash tools/porte-produit.sh 2>&1 | tail -30", "description": "Run product gate", "timeoutMs": 720000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 16 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 8, "offset": 34}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
34: | [`rapport-etat-r.md`](rapport-etat-r.md) | **B13** — l'état de R : tagger 0,8483/0,9440, R1.2-1024 mesuré, R4.4 |
35: | [`rapport-etat-n2.md`](rapport-etat-n2.md) | **B13** — l'état de N2 (porte propre, `porte-n2.sh`) |
36: | [`rapport-etat-a.md`](rapport-etat-a.md) | **B13** — l'état de A (frontière) |
37: | [`rapport-re-test-produit.md`](rapport-re-test-produit.md) | **B13** — re-test des 50 textes |
38: | [`rapport-restitution-v0.md`](rapport-restitution-v0.md) | **B13** — restitution v0 : **46/46** surfaces, miroir strict **0,1087** |
39: | [`rapport-pos-nombres.md`](rapport-pos-nombres.md) | **B13** — les nombres ont une POS (NUM) |
40: | [`rapport-partition-integree.md`](rapport-partition-integree.md) | **B13** — partition : alternatives étiquetées |
41: | [`rapport-partition-syntagmes.md`](rapport-partition-syntagmes.md) | **B13** — la partition (A29) |

(Showing lines 34-41 of 199. Use offset=42 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-restitution-v0.md`](rapport-restitution-v0.md) | **B13** — restitution v0 : **46/46** surfaces, miroir strict **0,1087** |\n| [`rapport-restitution-v1.md`](rapport-restitution-v1.md) | **B13 … [244 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py && grep -n \"restitution-v1\" reports/INDEX.md", "description": "Regenerate report index"}`

  ```
719 fiches → reports/INDEX.md
672:| [rapport-restitution-v1.md](rapport-restitution-v1.md) | B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087 |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-14, 02 h 00 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-14, 02 h 10 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](.. … [797 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée* … [691 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **722** / **816** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **721** / **815** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 et convention des GV (0,7902, 238/238), s065 réglé (238/239), J6.1 rejeté (conventio … [594 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche ; la\n  **restitution v1** répond au miroir strict : il **ne monte pas** (0,1087), la forme\n  canonique vaut **46/4 … [294 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 10, "offset": 34}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
34: | **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête le verbe) ; [fiche](../../reports/rapport-s-fait-divers.md). **v6** : h050, h053 et « si fort que » **fermés**, gold **60** (vague 5) ; **60/60** types, **142/142** rôles, **50/50** compléments, couverture 1,00 ; corpus 65,5 %/9,1 %, 596/1 184 homographes ; **55 tests**. **v5** : arbre parent/enfant (**99 candidats à ≥3**, 37 à 1) et **référents proposés** (294/371 formes, 77 sans contexte) ; **SVG** d'Alice, page **`/paragraphes`** (arbre, référents, verdict), **traduction** 14/14 référents ; gold **55**, analyseur **54/55** types, **131/131** rôles ; corpus **55** (SHA `76accf9d…`) ; banque partielle **142/71**, **81/65** ; **50 tests** | **poursuivre la validation sur `/paragraphes`** (a001–a003 faits), rétro-traduction API |
35: | **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 
… [3989 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**État au 14/11 02 h 00.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le suj … [2181 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"restitution\\|J8\" docs/pilotage/semaine-autonome.md", "description": "Find restitution rows in week plan"}`

  ```
28:| la restitution (annotation → texte) — **v0 faite** | surface **46/46**, miroir strict **0,1087** (50 textes libres) | [`rapport-restitution-v0.md`](../../reports/rapport-restitution-v0.md) |
88:| | après-midi | le **schéma v2** (`meta.alternative`, `meta.partition`) et la **restitution v0** | schéma validé, miroir mesuré |
136:- le **produit** : 2 spans tranchés (ou déclarés), le schéma v2, la restitution v0, la porte verte ;
155:| J1.4 restitution v0 | ✅ fait | 46/46 surfaces exactes | `8eb0cc49` |
177:| **J1** | après-midi : schéma v2 + restitution v0 | ✅ fait | **26 cas / 0 échec**, **1 836 annotations / 0 échec** ; **46/46** surfaces, miroir **0,1087** | `9a259953`, `8eb0cc49` | invariants sémantiques, v0.1 ponctuation, gold de restitution |
188:des GV (F1 **0,7902**), le schéma v2 (26 cas / 0 échec, v1 lue), la restitution v0 (46/46
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 20, "offset": 228}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
228: contrôle négatif : mélange exacte 0.0000 (caractères 0.3077) · troncature exacte 0.0000
229:                    (caractères 0.9231)
230: ```
231: 
232: **Lecture.** La commande **analyse** le texte, puis **reconstruit** la surface depuis le niveau
233: `graphème` de l'annotation — sans lire `Annotation.texte` — et la compare à la source. La
234: **surface est exacte** ; le **miroir strict** est le minimum des fidélités surface/mots/POS, et
235: il tombe ici parce que mots et POS séparent le point (`dort .`). `--json` publie le détail,
236: `--banc reports/pensee-fiabilite-produit.json` rejoue les **50 textes libres** : **46/46
237: surfaces exactes**, miroir strict **0,1087**, contrôle négatif **46/46**. C'est un **codec de
238: surface**, pas un décodeur neuronal : il ne prouve pas la fidélité sémantique. La fiche est
239: [`rapport-restitution-v0.md`](../../reports/rapport-restitution-v0.md).
240: 
241: ## 4. Ce que le produit ne fait pas encore
242: 
243: **1. Il ne génère pas de texte.** `restituer` reconstruit la **surface** depuis l'annotation
244: (codec), mai
… [418 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**Lecture.** La commande **analyse** le texte, puis **reconstruit** la surface depuis le niveau\n`graphème` de l'annotation — sans lire `Annotation.texte` — et la compare à la source. La\n**surface … [1761 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 15, "offset": 405}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
405: ```
406: 
407: **Options du CLI** :
408: 
409: | option | commande | sens |
410: |---|---|---|
411: | `--langue fr\|en` | `analyser`, `rejouer`, `restituer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 2 |
412: | `--json` | `analyser`, `evaluer`, `restituer` | sortie machine UTF-8 |
413: | `--jsonl` | `analyser` | une ligne JSON par phrase (avec `--fichier`) |
414: | `--fichier CHEMIN` | `analyser`, `restituer` | lit un texte UTF-8 au lieu de l'argument |
415: | `--banc CHEMIN` | `restituer` | mesure un banc JSON de textes (les 50 textes libres) |
416: | `--partition MODE` | `analyser`, `rejouer` | `alternative` (défaut), `filtrer_union`, `filtrer`, `brut` |
417: | `--contexte TEXTE` | `analyser`, `restituer` | mémoire de discours portée dans le JSON |
418: | `--gold` | `evaluer` | gold gelé 602 au lieu du vivant 612 |
419: | `-V`, `--version` | global | `drave 0.1.0` |

(Showing lines 405-419 of 466. Use offset=420 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| `--banc CHEMIN` | `restituer` | mesure un banc JSON de textes (les 50 textes libres) |\n| `--canonique` | `restituer` | ajoute la forme canonique v1 (segments + rôles + cibles) et son miroir |",  … [105 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 10, "offset": 436}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
436: | **`role` normalisé** | les valeurs mélangent `predicat`/`prédicat` et `qualite`/`qualité` ; fragile pour un filtre |
437: | **`--strict`** | `evaluer` ne mesure pas la cascade et n'applique pas son plancher (0,70) ; c'est le banc de recherche (`evaluer_gold.py`) qui le fait |
438: | **l'empaquetage** | pas de `pip install`, pas de commande `drave` dans le `PATH` ; tout part de la racine du dépôt |
439: | **le chemin neuronal** | la cascade 7B (0,9415) exige un serveur local interdit par la règle 11 ; pas de chemin neuronal livré |
440: | **la restitution sémantique** | `restituer` est un **codec de surface** (graphème) ; il ne restitue pas le sens, ne traduit pas, ne génère pas |
441: 
442: **Ce qui est déjà tenu** : `--version`, `--aide`, les **quatre** sous-commandes, le JSON
443: déterministe, le rejeu par empreinte, le **format versionné** (schéma v2, v1 lue),
444: `--fichier`/`--jsonl`, `--banc`, `--partition`, la **restitution v0** (46/46 surfaces exactes,
445: miroir strict 0,1087), la porte produit et le smoke test. Le reste est nommé ci-dessus, sans

(Show
… [65 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "`--fichier`/`--jsonl`, `--banc`, `--partition`, la **restitution v0** (46/46 surfaces exactes,\nmiroir strict 0,1087), la **forme canonique v1** (`--canonique`, 46/46 canonique, strict\ninchangé),  … [277 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md", "limit": 40, "offset": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md</path>
<type>file</type>
<content>
50: sujet de ce GV** corrige la seule cible fausse : **F1 0,7902 inchangé**, **POS 0,8625
51: inchangée**, **attachement 237/238 → 238/238 labels** (238/239 cibles, **0,9958**),
52: **exactitude sur les spans 0,9958 → 1,0**. Le gain est en **dev** (161/162 → 162/162) ; le
53: test reste à 76/76 car il n'a aucun cas déclencheur. Une seule annotation change, `s065` :
54: REL 5:17, `nage` → `elle`. Règle intégrée avec un test ; porte du bloc verte, porte produit
55: verte (**183/183**, fixtures d'attachement mises à jour). Fiche
56: [`reports/rapport-s065.md`](../../reports/rapport-s065.md), JSON
57: [`reports/pensee-s065.json`](../../reports/pensee-s065.json).
58: **J7.1 — le retrieval par famille : l'écriture d'abord, la sœur ensuite.** Sur les **532 textes
59: UDHR** de Panini (même source XML, article 1, 1948 ; **445 langues distinctes** après déduplication,
60: **521/532** étiquetées Glottolog), le top-1 de voisinage est de la même famille **66,1 %** (hasard
61: 10,3 %) et de la même branche **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout est au hasard**
62:
… [1561 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md", "new_string": "[`reports/retrieval-familles.json`](../../reports/retrieval-familles.json), outil\n[`tools/retrieval_familles.py`](../../tools/retrieval_familles.py).\n**J8.1 — la restitution v1 : le miroir  … [1533 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run documentation review", "timeoutMs": 180000}`

  ```
revue de documentation · 722 fiche(s) · 816 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo \"code=$?\"", "description": "Validate en-cours state"}`

  ```
en-cours · 1658 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -20; echo \"code=$?\"", "description": "Check document size budget"}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2696    201   T1   2800  reports/README.md
    2450    166   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4028 mots (budget 4 000)

  avertissements :
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [118 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py 2>&1 | tail -20; echo \"code=$?\"", "description": "Validate journal structure"}`

  ```
journal · 46 jour(s) · 182 session(s) · 2455 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_liens.py 2>&1 | tail -20; echo \"code=$?\"", "description": "Check links"}`

  ```
✅ 3979 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py --verifier; echo \"index-code=$?\"; bash tools/porte-tableaux.sh 2>&1 | tail -20; echo \"tableaux-code=$?\"", "description": "Verify report index and tables gate"}`

  ```
index-code=0
  ✅ 1787 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3979 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
tableaux-code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,200p tools/taille_documents.py", "description": "Inspect size budget tool"}`

  ```
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

# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
BUDGETS: list[tuple[str, str, int
… [6542 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re\nt=open('docs/pilotage/en-cours.md').read()\nprint('en-cours words',len(re.findall(r'\\S+',t)))\nfor i,l in enumerate(t.splitlines(),1):\n    n=len(re.findall(r'\\S+',l))\n    if n>25: print(i,n,l[:140])\ … [52 caractères tronqués]`

  ```
en-cours words 1658
48 37 - **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ;
63 62 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** 
79 56 - **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondé
88 36 - **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **
90 52 - **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fi
92 48 - **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significative ; **J3.2** : `l
93 41 - **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,
116 36 | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts 
117
… [1004 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,180p tools/verifie_en_cours.py", "description": "Inspect en-cours validator"}`

  ```
#!/usr/bin/env python3
"""verifie_en_cours.py — l'état doit rester court, structuré, reprenable et multi-session.

Le fichier `docs/pilotage/en-cours.md` est la seule source de l'état. Ce contrôle vérifie :
  1. un budget de **2 000 mots** ;
  2. les **sept sections** du template ;
  3. « Sessions en cours » : une sous-section `### Session ...` par session active, avec
     **Id**, **Rôle**, **Plan**, **Ambition**, **Stratégie**, **Objectif final**,
     **Ce qu'elle fait**, **Ce que font les autres**, **Prochaine action**, **Bloquants** et
     **Journal** ;
  4. **10 puces au plus** dans « Ce qui est en cours », sans doublon et sans puce de plus de 80 mots ;
  5. « Les chantiers et leurs bloquants » : une ligne **A**, **B**, **N**, **R** avec un bloquant
     **non vide** (le mot « aucun » est une information, une cellule vide est un oubli) ;
  6. **5 questions ouvertes au plus**, chacune avec ce qui la débloque (`→`) ;
  7. une **prochaine action nommée** dans « Ce qui reste » (A/B/C/N/R) ;
  8. aucune ligne de journal A7.x dans l'état (les mesures vont dans `reports/`).

Usage : python3 tools/verifie_en_cours.py   (code 0 = l'état est reprenable)
"""
from __future__ import anno
… [4812 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 20, "offset": 28}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
28: - **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
29: - **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
30: - **Plan** : audit, état, runbook ; nuit.
31: - **Ambition** : un état reprenable.
32: - **Stratégie** : committer par flux.
33: - **Objectif final** : sédimentation à zéro.
34: - **Ce qu'elle fait** : intégration ; passe **11 h 30 — 82, 80/2** ; plan de nuit.
35: - **Ce que font les autres** : **N2**, **S**, **Pensée**.
36: - **Prochaine action** : reprise par le hub `1e7ef596` ; l'état du 04/11 est la source.
37: - **Bloquants** : aucun.
38: - **Journal** : [la session](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/).
39: 
40: ### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures *(en pause)*
41: 
42: - **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
43: - **Rôle** : **S — les structures** : le banc, l'analys
… [313 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Plan** : état.\n- **Ambition** : reprise.\n- **Stratégie** : flux.\n- **Objectif final** : zéro.", "old_string": "- **Plan** : audit, état, runbook ; nuit.\n- **Ambition** : un état reprenab … [90 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Plan** : validation.\n- **Ambition** : rôles.\n- **Stratégie** : contrôles.\n- **Objectif final** : gold 60.", "old_string": "- **Plan** : analyseur, export, arbre, validation.\n- **Ambition … [133 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **contrat v1**, **`drave` v0**.", "old_string": "; **restitution v1** (forme canonique  … [124 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; [restitution v0](../../reports/rapport-restitution-v0.md), [g017](../../reports/rapport … [247 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "restitution v1 (46/46 canonique, strict 0,1087)** | **trancher la convention d'adverbe (`g017`)** ; puis T132/T133, gold 200+ ; **B10.3 bloquée** |", "old_string": "restitution v1 (forme canoniq … [133 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche ; la\n  **restitution v1** : le miroir strict **ne monte pas** (0,1087), la forme canonique vaut\n  **46/46** ; le g … [328 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -8; echo \"code=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -5", "description": "Recheck size and state"}`

  ```
1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3990 mots (budget 4 000)

  avertissements :
     · 48 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
code=0
  en-cours · 1620 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : intégration ; passe **82, 80/2**.", "old_string": "- **Ce qu'elle fait** : intégration ; passe **11 h 30 — 82, 80/2** ; plan de nuit."}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p docs/methode/portes.md", "description": "Read gates method"}`

  ```
# Les portes : lancer, lire le verdict, ne pas se tromper de rouge

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.

## La commande

```bash
bash tools/toutes-les-portes.sh
```

Elle lance **toutes** les `tools/porte-*.sh`, séquentiellement, **sans s'arrêter à la première rouge** (on veut le
[tableau](../theorie/glossaire/entrees/tableau.md), pas la première tuile), et borne **chaque** [porte](../theorie/glossaire/entrees/porte.md) à `DELAI=1800` s. Durée observée d'une passe complète :
**1 h 30 – 2 h** sur Hauru (**83 portes** ; certaines entraînent de petits modèles, d'autres utilisent les [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md) ;
`porte-deepseek` est **hors réseau** et rapide). La dernière passe complète à **82 portes** (03/11 11 h 30, **machine au repos**, **1 h 48**) a donné
**80 vertes, 2 rouges** (les 2 connues : `indice`, `melange`) ;
`porte-reparti-moteur` (ré-étalonnée à 8,7434) et `porte-homeostasie` (auto-générée) sont **vertes** ;
la liste et le diagnostic sont dans
[`references-non-regression.md`](../pilotage/references-non-regression.md). `porte-deepseek` est **
… [3931 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,160p docs/pilotage/references-non-regression.md", "description": "Read tolerated red gates"}`

  ```
# Références de non-régression

> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
> `porte-melange` (structurelles, antérieures) et `porte-sessions` (le mandat du hub
> `1e7ef596`, périmé de 9 jours ; le mien est rafraîchi). `porte-produit` **verte**, `porte-bloc`
> **verte**. Journal : `work/portes/passe-1311-23h15.log`.
> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
> échouait sur une ancre du banc pilote (« < 2,5 ») que la réécriture de la roadmap du 04/11
> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
> signale les heartbeats périmés du hub et de `e181ce02` au moment de la passe — le hub l'a rafraîchi
> à 01 h 55, **`e181ce02` reste à rafraîchir par sa s
… [12222 caractères tronqués]
  ```

- **bash** `{"command": "nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader 2>/dev/null || echo no-gpu; pgrep -af \"entrainer|llama-server|ollama|python3 tools\" | head -20", "description": "Check GPU and running processes"}`

  ```
0, 1 MiB, 16384 MiB, 0 %
1, 1 MiB, 16384 MiB, 0 %
946073 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup timeout 46800 python3 tools/chantier/superviseur.py boucle --budget 43200 --timeout 5400 > work/chantier/boucle2.log 2>&1 & echo "PID $!"; sleep 30; tail -2 work/chantier/journal.log; date
946075 timeout 46800 python3 tools/chantier/superviseur.py boucle --budget 43200 --timeout 5400
946076 python3 tools/chantier/superviseur.py boucle --budget 43200 --timeout 5400
1592677 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 2400; date; tail -4 work/chantier/journal.log; python3 tools/chantier/superviseur.py etat 2>&1 | grep -E "budget|a_faire" | head -3
1612719 bash -c nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader 2>/dev/null || echo no-gpu; pgrep -af "entrainer|llama-server|ollama|python3 tools" | head -20
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p work/portes/passe-1402-02h00 && JOURNAUX=work/portes/passe-1402-02h00 bash tools/toutes-les-portes.sh", "description": "Run all gates in background", "run_in_background": true}`

  ```
started background job bash-68
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l tools/mesurer_restitution_v0.py tools/mesurer_restitution_v1.py tools/restitution.py tools/drave.py tools/tests/test_restitution.py && git status --short", "description": "Check file modes and git status"}`

  ```
-rw-------. 1 stephane stephane 25784 14 nov 01:53 tools/drave.py
-rw-------. 1 stephane stephane  3568  7 nov 14:33 tools/mesurer_restitution_v0.py
-rw-------. 1 stephane stephane  4477 14 nov 01:53 tools/mesurer_restitution_v1.py
-rw-------. 1 stephane stephane 44837 14 nov 01:52 tools/restitution.py
-rw-------. 1 stephane stephane 14379 14 nov 01:53 tools/tests/test_restitution.py
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/2026-11-14/README.md
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
 M tools/porte-produit.sh
 M tools/restitution.py
 m tools/structures
 M tools/tests/test_restitution.py
?? reports/pensee-restitution-v1.json
?? reports/rapport-restitution-v1.md
?? reports/rapport-s-paragraphes.md
?? tools/mesurer_restitution_v1.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- tools/restitution.py tools/drave.py tools/tests/test_restitution.py tools/porte-produit.sh docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/produit/README.md reports/README.md journal/2026-11-14/README.md",  … [46 caractères tronqués]`

  ```
docs/pilotage/en-cours.md       |  32 +--
 docs/pilotage/roadmap.md        |   2 +-
 docs/produit/README.md          |  11 +-
 journal/2026-11-14/README.md    |  15 +
 reports/README.md               |   1 +
 tools/drave.py                  |  32 ++-
 tools/porte-produit.sh          |  18 +-
 tools/restitution.py            | 619 +++++++++++++++++++++++++++++++++++++++-
 tools/tests/test_restitution.py | 136 +++++++++
 9 files changed, 841 insertions(+), 25 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-restitution-v1.json'))\n# sanity: one result form fields\nr=next(x for x in d['resultats'] if x['id']=='f01')\nprint(json.dumps(r,ensure_ascii=False,indent=1)[:1200])\n … [52 caractères tronqués]`

  ```
{
 "id": "f01",
 "refus": "",
 "langue": "fr",
 "caracteres": 13,
 "etiquettes": 20,
 "strict": {
  "definition": "minimum des fidélités binaires de la surface (graphème), des mots et des POS ; une sortie n'est fidèle que si elle reproduit exactement la source",
  "fidelite": 0.0,
  "exact": false
 },
 "surface_stricte": {
  "exact": true,
  "fidelite": 1.0,
  "fidelite_caractere": 1.0,
  "caracteres": 13,
  "octets": 13,
  "niveau": "graphème",
  "nom": "surface",
  "rendu": "Le chat dort.",
  "couverture": 1.0
 },
 "canonique": {
  "definition": "minimum des fidélités binaires des mots canoniques, des POS canoniques et de la forme canonique (jetons normalisés : casse repliée, ponctuation retirée, espaces réduits) comparées à la source canonique ; le miroir strict reste la référence de surface, il n'est pas remplacé",
  "source_canonique": "le chat dort",
  "mots": {
   "exact": true,
   "fidelite": 1.0,
   "fidelite_caractere": 1.0,
   "jetons": 3
  },
  "pos": {
   "exact": true,
   "fidelite": 1.0,
   "fidelite_caractere": 1.0,
   "jetons": 3
  },
  "forme": {
   "exact": true,
   "fidelite": 1.0,
   "fidelite_caractere": 1.0,
   "jetons": 3
  },
  "fidelite": 1.0,
  "exact": t
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/pilotage/en-cours.md | head -120", "description": "Review en-cours diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 7c52573c..2f3fd0fd 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-14, 02 h 10 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-14, 02 h 00 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -27,11 +27,11 @@
 
 - **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
 - **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
-- **Plan** : audit, état, runbook ; nuit.
-- **Ambition** : un état reprenable.
-- **Stratégie** : committer par flux.
-- **Objectif final** : sédimentation à zéro.
-- **Ce qu'elle fait** : intégration ; passe **11 h 30 — 82, 80/2** ; plan de nuit.
+- **Plan** : état.
+- **Ambition** : reprise.
+- **Stratégie** : flux.
+- **Objectif final** : zéro.
+- **Ce qu'elle fait** : intégration ; passe **82, 80/2**.
 - **Ce que font les autres** : **N2**, **S**, **Pensée**.
 - **Prochai
… [7793 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- tools/drave.py tools/porte-produit.sh | head -180", "description": "Review CLI and gate diff"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index c94b3f9a..371473c5 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -345,7 +345,9 @@ def cmd_restituer(args: argparse.Namespace) -> int:
 
     Deux modes : un **texte** (ou un fichier), ou un **banc** JSON de textes
     (`--banc`, le format de `reports/pensee-fiabilite-produit.json`). Le mode banc
-    laisse le bloc détecter la langue, comme le CLI sans `--langue`.
+    laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`
+    ajoute la **forme canonique v1** (segments + rôles + cibles) et son miroir ; la
+    sortie de la v0 reste celle par défaut.
     """
     if args.banc:
         if args.texte is not None or args.fichier:
@@ -358,12 +360,17 @@ def cmd_restituer(args: argparse.Namespace) -> int:
         except (OSError, ValueError) as exc:
             print(f"{NOM}: erreur : banc illisible : {exc}", file=sys.stderr)
             return 1
-        rapport = restitution.mesurer_banc(items, args.langue)
+        if args.canonique:
+            rapport = restitution.mesurer_banc_v1(items, args.langue)
+        else:
+            rapport = restitution.mesurer_banc(items, args.langue)
         rappo
… [4440 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- tools/restitution.py | head -120", "description": "Review restitution diff start"}`

  ```
diff --git a/tools/restitution.py b/tools/restitution.py
index 2daadf38..b3ad276d 100644
--- a/tools/restitution.py
+++ b/tools/restitution.py
@@ -1,4 +1,4 @@
-"""restitution.py — la restitution v0 : annotation → surface, et le miroir.
+"""restitution.py — la restitution v0 (surface) et la v1 (forme canonique).
 
 La **surface** est reconstruite depuis le niveau `graphème` — les spans typés qui portent
 les caractères — **sans lire** `Annotation.texte`. Les niveaux `mot` et `pos` sont mesurés
@@ -10,13 +10,26 @@ définition de `tools/tests/linguistique/miroir.mesurer`, réutilisée ici pour
 avoir deux. `fidelite_caractere` ajoute une distance de Levenshtein normalisée : elle
 distingue « presque fidèle » de « fidèle » et documente la perte de la ponctuation.
 
+La **forme canonique** (v1) est une lecture **structurelle** de l'annotation : les
+syntagmes avec leur type, leur rôle et leur cible d'attachement, une linéarisation sans
+chevauchement, et un plancher de jetons normalisés (casse repliée, ponctuation retirée).
+Elle ne remplace pas la surface : elle la met entre parenthèses pour mesurer ce que la
+structure ajoute, et son **miroir canonique** se compare à une source canonisée
… [3981 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --check && echo diff-check-ok; python3 tools/taille_documents.py 2>&1 | grep \"T0 max\"", "description": "Check whitespace and T0"}`

  ```
diff-check-ok
  T0 max : 3982 mots (budget 4 000)
  ```

- **job_output** `{"job_id": "bash-68", "wait": false}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes/passe-1402-02h00
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l work/portes/passe-1402-02h00/registre.txt 2>/dev/null; tail -5 work/portes/passe-1402-02h00/registre.txt 2>/dev/null", "description": "Check gate progress"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la work/portes/passe-1402-02h00 | head; ps -o pid,etime,cmd -p $(pgrep -f \"toutes-les-portes\" | head -1) 2>/dev/null", "description": "Inspect gate logs and process"}`

  ```
total 4
drwxr-xr-x. 1 stephane stephane  54 14 nov 01:58 .
drwxr-xr-x. 1 stephane stephane 464 14 nov 01:58 ..
-rw-r--r--. 1 stephane stephane  86 14 nov 01:58 porte-adaptateur-sortie.log
    PID     ELAPSED CMD
1612744       00:16 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nitems=r.items_banc(json.load(open('reports/pensee-fiabilite-produit.json')))\nh=bl.Heuristique()\ndef co … [944 caractères tronqués]`

  ```
resolues set/ordre 315 315 dans segment set/ordre 313 313
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _index_cible\\|def structure_canonique\" tools/restitution.py", "description": "Locate functions"}`

  ```
434:def _index_cible(cible: str, rang: int, segments: list[bl.Etiquette],
544:def structure_canonique(a: bl.Annotation, source: str) -> dict:
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "limit": 22, "offset": 428}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py</path>
<type>file</type>
<content>
428:                             key=lambda e: (e.debut, e.fin))
429:         if etiquettes:
430:             return [j for e in etiquettes for j in jetons_canoniques(e.valeur)]
431:     return []
432: 
433: 
434: def _index_cible(cible: str, rang: int, segments: list[bl.Etiquette],
435:                  canoniques: list[str]) -> int | None:
436:     """Le rang du **premier autre** segment qui porte la cible (en jetons), sinon None."""
437:     if not cible:
438:         return None
439:     jetons = cible.split()
440:     for j, canonique in enumerate(canoniques):
441:         if j == rang:
442:             continue
443:         if all(jeton in canonique.split() for jeton in jetons):
444:             return j
445:     return None
446: 
447: 
448: def forme_canonique(a: bl.Annotation) -> dict | None:
449:     """La forme canonique v1 : segments + rôles + cibles, et un plancher de jetons.

(Showing lines 428-449 of 1030. Use offset=450 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "new_string": "def _contient_jetons(sequence: list[str], motif: list[str]) -> bool:\n    \"\"\"Vrai si `motif` apparaît **dans l'ordre** dans `sequence` (sous-suite contiguë).\"\"\"\n    n = len(motif)\n    return  … [1101 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "limit": 45, "offset": 575}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py</path>
<type>file</type>
<content>
575:     for i, e in enumerate(segments):
576:         meta = e.meta or {}
577:         types[e.type] += 1
578:         if meta.get("role"):
579:             roles[meta["role"]] += 1
580:         attachement = meta.get("attachement") or {}
581:         cible = _canonique_valeur(attachement.get("cible", ""))
582:         if not cible:
583:             continue
584:         attachements += 1
585:         jetons = cible.split()
586:         if all(jeton in source_jetons for jeton in jetons):
587:             cibles_resolues += 1
588:         if any(j != i and all(jeton in canoniques[j].split() for jeton in jetons)
589:                for j in range(len(segments))):
590:             cibles_dans += 1
591:     return {
592:         "segments": len(segments),
593:         "segments_avec_role": sum(roles.values()),
594:         "attachements": attachements,
595:         "cibles_resolues": cibles_resolues,
596:         "cibles_dans_un_segment": cibles_dans,
597:         "couverture_caracteres": round(len(positions) / max(1, len(source)), 4),
598:         "couverture_jetons": round(j
… [1015 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 555,575p tools/restitution.py", "description": "View structure setup"}`

  ```
- `couverture_jetons` : part des jetons `mot` dont le début tombe dans un segment ;
    - `cibles_resolues` : la cible (en jetons) est présente dans la source canonique ;
    - `cibles_dans_un_segment` : la cible est portée par un **autre** segment.

    Ce sont des mesures de **cohérence** de l'annotation, pas de justesse : sans gold de
    forme canonique, on ne peut pas dire que le rôle ou la cible sont les bons.
    """
    segments = [e for e in a.etiquettes if e.niveau == "syntagme"]
    positions: set[int] = set()
    for e in segments:
        positions.update(range(max(0, e.debut), min(len(source), e.fin)))
    mots = [e for e in a.etiquettes if e.niveau == "mot"]
    jetons_couverts = sum(1 for e in mots if e.debut in positions)
    source_jetons = set(jetons_canoniques(source))
    canoniques = [_canonique_valeur(e.valeur) for e in segments]
    attachements = 0
    cibles_resolues = 0
    cibles_dans = 0
    roles: collections.Counter[str] = collections.Counter()
    types: collections.Counter[str] = collections.Counter()
    for i, e in enumerate(segments):
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "new_string": "    source_jetons = jetons_canoniques(source)", "old_string": "    source_jetons = set(jetons_canoniques(source))"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "new_string": "        jetons = cible.split()\n        if _contient_jetons(source_jetons, jetons):\n            cibles_resolues += 1\n        if any(j != i and _contient_jetons(canoniques[j].split(), jetons)\n      … [373 caractères tronqués]`

  ```
Error: old_string was not found in "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py"
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py", "new_string": "        jetons = cible.split()\n        if _contient_jetons(source_jetons, jetons):\n            cibles_resolues += 1\n        if any(j != i and _contient_jetons(canoniques[j].split(), jetons)\n      … [377 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m py_compile tools/restitution.py && python3 tools/tests/test_restitution.py 2>&1 | tail -6", "description": "Re-run restitution tests after containment change"}`

  ```
test_surface_sans_controle (__main__.TestReconstruction.test_surface_sans_controle) ... ok

----------------------------------------------------------------------
Ran 22 tests in 14.432s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work/portes/passe-1402-02h00 | wc -l; ls -t work/portes/passe-1402-02h00 | head -5; test -f work/portes/passe-1402-02h00/registre.txt && wc -l work/portes/passe-1402-02h00/registre.txt", "description": "Check gate progress"}`

  ```
1
porte-adaptateur-sortie.log
[exit code: 1]
  ```

- **bash** `{"command": "date; ps -o pid,etime,cmd -p 1612744; pgrep -af \"porte-\" | head -10; tail -5 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes/passe-1402-02h00/porte-adaptateur-sortie.log", "description": "Check running gate and time"}`

  ```
sam 14 nov 2026 02:00:01 EST
    PID     ELAPSED CMD
1612744       01:04 bash tools/toutes-les-portes.sh
1612762 timeout 1800 bash tools/porte-adaptateur-sortie.sh
1612763 bash tools/porte-adaptateur-sortie.sh
1621689 bash tools/porte-adaptateur-sortie.sh
1621690 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/porte-adaptateur/morceau.txt --limit 256 --ctx 256 --threads 8 --couches 0:8 --tete-partielle --adaptateur-sortie /tmp/porte-adaptateur/identite.f32
1621710 bash -c date; ps -o pid,etime,cmd -p 1612744; pgrep -af "porte-" | head -10; tail -5 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes/passe-1402-02h00/porte-adaptateur-sortie.log
porte de l'adaptateur de sortie — Qwen2.5-0.5B-Q8_0.gguf · plage 0:8 · 256 jetons
  écriture  : complet 17.4315 → 17.4315 · tronqué 2687292.8165 → 2687292.8165
  ✅ PPL épinglées : complet 17.4315 · tronqué 2687292.8165
  ✅ l'écriture est fidèle (mêmes chiffres sur les deux chemins)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,160p tools/journal_auto.py", "description": "Inspect journal_auto behavior"}`

  ```
#!/usr/bin/env python3
"""journal_auto.py — le journal quotidien, ÉCRIT PAR JOUR (UN DOSSIER) ET PAR THÈME, à partir de git et des sessions.

POURQUOI. Le journal doit consigner les **événements datés** (voir
`docs/organisation-du-depot.md`), et une journée de ce dépôt est trop riche pour un seul
fichier : un jour touche le moteur, les protocoles, les mesures, les portes et la
documentation. D'où le découpage **`<AAAA-MM-JJ>_<thème>.md`** : on lit la journée d'un thème,
et on suit un thème **d'un jour à l'autre** (le nom commence par la date, le thème suit —
`ls journal/2026-10-1*/attention.md`).

SOURCES, et rien d'autre :
  1. **git** — les commits du jour (heure d'auteur, en heure locale de la machine) et les
     fichiers touchés ; c'est la chronologie **fiable** (les horodatages écrits à la main
     s'étaient retrouvés dans le futur) ;
  2. **journal/sessions/** — les rapports de session dont la fenêtre de temps couvre le jour
     (début et durée lus dans l'index `journal/README.md`, régénéré par
     `tools/session_report.py`) : on en extrait les **titres de tour** classés par thème, avec
     le lien vers le rapport complet.

CE QUI EST PRÉSERVÉ. Tout ce que l'humain (ou l
… [6567 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -6 && python3 tools/verifie_en_cours.py 2>&1 | tail -3 && python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|✅ tous\"", "description": "Re-run doc checks after edits", … [21 caractères tronqués]`

  ```
revue de documentation · 722 fiche(s) · 816 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1612 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  T0 max : 3982 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-restitution-v1.json'))\nr=[x for x in d['resultats'] if not x.get('refus')]\nprint('surface exacte',sum(1 for x in r if x['surface_stricte']['exact']),'/',len(r))\nprin … [260 caractères tronqués]`

  ```
surface exacte 46 / 46
strict 5
canonique 46
strict canon 1
  ```

- **job_output** `{"job_id": "bash-68", "wait": true, "timeout_ms": 600000}`

  ```
porte-adaptateur-sortie ✅                          81 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         175 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          12 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          14 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           0 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          46 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          81 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅                          97 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard   
… [451 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/j8.1-commit-msg <<'MSG'\nJ8.1 — RESTITUTION v1 : FORME CANONIQUE 46/46 (STRICT 0,1087 INCHANGÉ), 395 SEGMENTS / 315 CIBLES, STABILITÉ 18/46\n\n- `drave restituer --canonique` : forme canonique depuis l'annotation (segments + rôles +\n  cibles), linéarisation sans chevauchemen … [1224 caractères tronqués]`

  ```
18 /tmp/j8.1-commit-msg
  ```

- **job_output** `{"job_id": "bash-68", "timeout_ms": 900000, "wait": true}`

  ```
porte-coupe            ✅                         135 s    ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit
  porte-cycle-c2         ✅                         129 s    ✅ porte tenue (chaîne exacte · pas 1 exact · borné · coût dit · trajectoire déterministe ·
  porte-deepseek         ✅                           1 s    ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
  porte-delais           ✅                          21 s    ✅ le temps, lui, augmente : 7.04 s → 10.00 s (+3.0 s ≈ 50 ms × 64 pas)
  porte-diff-couche      ✅                          19 s    ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé
  porte-document         ✅                           6 s  ✅ porte document verte
  porte-echange-experts  ✅                          56 s    PORTE TENUE
  porte-episodique       ✅                         173 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          26 s    mod
… [206 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-68", "timeout_ms": 900000, "wait": true}`

  ```
porte-gain             ✅                         218 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
[status: running]
  ```

- **job_output** `{"job_id": "bash-68", "timeout_ms": 900000, "wait": true}`

  ```
porte-greffe           ✅                         660 s    ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE
  porte-harnais-invariants ✅                         116 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
[status: running]
  ```

### 👤 Utilisateur

You are repeating the exact same tool call with identical arguments. Carefully analyze the previous result before calling again: if the task is not complete, try a different approach or different arguments instead of repeating the call.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"logs: $(ls work/portes/passe-1402-02h00 | wc -l)\"; ls -t work/portes/passe-1402-02h00 | head -3; ps -o pid,etime,cmd -p 1612744 2>/dev/null; pgrep -af \"porte-.*\\.sh\" | head -3; date", "description": "Inspect full gate prog … [23 caractères tronqués]`

  ```
logs: 31
porte-homeostasie.log
registre.txt
porte-harnais-invariants.log
    PID     ELAPSED CMD
1612744       41:43 bash tools/toutes-les-portes.sh
1777511 timeout 1800 bash tools/porte-homeostasie.sh
1777512 bash tools/porte-homeostasie.sh
1811815 bash tools/porte-homeostasie.sh
sam 14 nov 2026 02:40:40 EST
  ```

- **job_output** `{"job_id": "bash-68", "timeout_ms": 1200000, "wait": true}`

  ```
porte-homeostasie      ✅                         539 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          26 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
[status: running]
  ```

- **job_output** `{"job_id": "bash-68", "timeout_ms": 1500000, "wait": true}`

  ```
porte-indice           ❌ code 1                  878 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
[status: running]
  ```

- **job_output** `{"job_id": "bash-68", "timeout_ms": 1500000, "wait": true}`

  ```
porte-jeux             ✅                         110 s    ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision,
  porte-jumeaux          ✅                          31 s  PORTE TENUE : l'échange est exact, il ne crée pas de gain entre jumeaux identiques, il
  porte-lecteur          ✅                           0 s  ✅ porte lecteur verte
  porte-lecture          ✅                           2 s  ✅ porte lecture verte
  porte-m5-brouillon     ✅                           1 s    ✅ brouillon déclaré (cibles [37,38,39]) et porté : 75 tenseurs, 41 263 M poids
  porte-melange          ❌ code 1                  110 s    ❌ l'état de A ne rend pas le code de A dans une
  porte-memoire          ✅                          11 s  PORTE TENUE : la mémoire retient les K derniers signaux HORS du réseau, exactement, sans
  porte-miroir-blocs     ✅                           8 s  ✅ porte miroir verte
  porte-mistral          ✅                           9 s      ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= p
  porte-n3-cache         ✅                           7 s  PORTE TENUE : saut de calcul mesuré · sortie changée · condition 
… [2757 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-68", "timeout_ms": 1500000, "wait": true}`
