# Session DSH — relecture

- identifiant : `9fffd87b-4d0b-4ccb-b41a-0fbc7079d4aa`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 18:48:01
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, fenêtre jusqu'à 2026-10-28 08:00 HAE. Sous-agent A20 : mesurer le **seuil de rentabilité réseau** de la grappe sparse (A7.5), sans modifier les modules existants.

Contexte :
- A7.5 `tools/grappe_reseau.py` : flux 4×448, dense 7 416 o, sparse 1 672 o, fidélité 100 %, 0,125 ms loopback.
- A3.3 : attente ≈ calcul distant + 3,2 × latence ; 1,01× à 0 ms, 1,99× à 5 ms, 4,89× à 20 ms.
- Tests : 132 OK.

Objectif :
1. Créer `tools/seuil_reseau.py` : simuler des **latences WAN** (0, 5, 20, 50, 100 ms) et un **calcul distant** (temps de grappe), mesurer le **temps total** sparse vs dense, et le **seuil** où le sparse gagne.
2. Mesurer aussi le **débit** (octets/s) et le **coût par jeton** ; contrôle **dense** et **latence nulle**.
3. Écrire `/tmp/a20-seuil-reseau.json` et `.md` ; si le sparse perd toujours ou gagne toujours, le dire.
4. Ne pas simuler par `sleep` sans le déclarer : le modèle de latence doit être explicite.

Contraintes :
- Crée uniquement `tools/seuil_reseau.py` et `tools/cerveau/tests/test_seuil_reseau.py` ; ne modifie pas les modules existants, docs, reports, journal, `batterie.py`, git.
- Pas de `git add/commit/checkout`.
- CPU. Sois autonome, timebox, autocritique. Réponds avec un résumé et les chemins.
Your parent agent id is "f0969e87-af0c-43b1-93cf-f278d9c90846". Before you finish, send your result to that agent with send_message({ agent_id: "f0969e87-af0c-43b1-93cf-f278d9c90846", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 185 fichiers / 252 JSON, 54 documents**), chemins archivés
> corrigés (`docs/archive/`), B10–B12 réintégrés dans les cartes. **Les règles et le routage
> ci-dessous ne changent pas.** Source de vérité : `docs/en-cours.md` (état)
> et `docs/roadmap.md` (plan). Ne pas recopier ces chiffres dans un nouveau document.

> **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la **vision**, les règles non négociables et le
> **routage** vers le document de chaque tâche. Le détail n'est pas ici : il est dans [`docs/agent/`](docs/agent/)
> (tableau § 3). L'**état courant** est dans [`docs/en-cours.md`](docs/en-cours.md) ; la **roadmap** dans
> [`docs/roadmap.md`](docs/roadmap.md) ; le récit daté dans [`journal/`](journal/).

## 1. La vision (l'essentiel)

**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Les activations d'un
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le projet a pour principe que la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. Bref, révolutionner l'IA avec une approche par bus d'événements où chaque bloc fonctionnel est optimisable, comparable et substituable par des alternatives ayant des architectures différentes. e.g. Blocs neuronaux là où l'intuition est un avantage, blocs computationnels classiques pour les opérations où l'informatique classique est plus fiable et performante.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de
les **combiner**, de les **décomposer en couches et grappes de neurones** exécutables par du matériel divers, voire
**distribué en réseau**, de les **diagnostiquer et faire évoluer** en étudiant leurs **flux**, et de **rejouer à
volonté** des événements.


## 2. Les règles non négociables

1. **Rangement** : `docs/` = état, vision, concepts (ce qui reste vrai quand les chiffres changent) ; `reports/` =
   résultats mesurés, fiches, JSON ; `journal/` = récit daté ; `data/` = corpus. *Un résultat qui traîne dans
   `docs/` **déménage**.* → [`docs/agent/rangement.md`](docs/agent/rangement.md)
2. **Un résultat** porte le chiffre, la mesure, le dispositif, un **contrôle négatif**, et **ce qui pourrait le
   rendre faux** — puis un **commit**, la **fiche** dans `reports/`, le **récit** dans `journal/`, l'**état** dans
   `docs/en-cours.md`, et il **nomme sa ligne de roadmap** (A… / B…). *Sans contrôle négatif, ce n'est pas un
   résultat.* → [`docs/agent/resultats.md`](docs/agent/resultats.md)
3. **Les portes** : `bash tools/toutes-les-portes.sh` ; le registre est dans `$JOURNAUX/registre.txt` (affiché au
   lancement) et le verdict se lit par `awk '$2 != 0'` — **jamais** par les marqueurs ni à travers un tube. Rouges
   structurelles tolérées : **`porte-indice`** et **`porte-melange`** ; toute autre est une régression. →
   [`docs/agent/portes.md`](docs/agent/portes.md)
4. **La revue de documentation** avant chaque commit de clôture : `python3 tools/revue_documentation.py` (et
   `tools/porte-tableaux.sh`) ; **corriger** ce qu'elle signale. → [`docs/agent/rangement.md`](docs/agent/rangement.md)
5. **Panini et Nipada** à chaque cycle : lire ce qui a bougé chez eux, confronter ; la théorie va dans
   [`docs/genealogie-des-langues.md`](docs/genealogie-des-langues.md), **jamais** les chiffres. Leur avertissement :
   la surface capte **l'époque** (β +0,138) bien plus que la **filiation** (β +0,049) — contrôler la date dans tout
   test de style, la surface dans tout test de famille. → [`docs/agent/panini-nipada.md`](docs/agent/panini-nipada.md)
6. **Le miroir entrée/sortie** : toute mesure d'entrée se double d'une mesure de **sortie** (restitution, boucle) ;
   la **fluidité n'est pas la fidélité**. → [`docs/agent/miroir.md`](docs/agent/miroir.md)
7. **La roadmap** ([`docs/roadmap.md`](docs/roadmap.md)) : chaque chantier a une **prochaine action** ; l'ordre est
   celui de la **valeur** et des **dépendances**, jamais celui d'une date. Un chantier est **fini** quand il est
   mesuré, écrit et committé ; il est alors **marqué** dans la roadmap et le suivant est désigné.
8. **Ne jamais bloquer, ne jamais rester en attente** : une question humaine se **consolide** dans
   `docs/en-cours.md` et on **continue** ; si une ligne est bloquée (corpus, compte, matériel), on prend la suivante
   — la **file « jamais en attente »** de la roadmap. → [`docs/agent/ressources.md`](docs/agent/ressources.md)
9. **Les illustrations sont des SVG.** Aucun **ASCII art** dans un bloc de code. Un schéma est un
   **`.svg`** — direct, ou généré par **docwatch** depuis `.mmd`/`.puml` (l'image pointe vers
   `<source>.svg`) — avec `viewBox`, `<title>`, `<desc>`, liens relatifs ; il vit dans
   `docs/schemas/` ou `docs/synthese/schemas/`. Vérifier : `python3 tools/verifier_schemas.py`.
   → [`docs/agent/illustrations.md`](docs/agent/illustrations.md)

## 3. Routage : lire le document de sa tâche, pas les autres

| si la tâche est… | lire |
|---|---|
| comprendre la **vision** (les flots, les cinq axes, ce qu'elle n'est pas) | [`docs/vision.md`](docs/vision.md) |
| la **roadmap** (les deux programmes, l'ordre, la file « jamais en attente ») | [`docs/roadmap.md`](docs/roadmap.md) |
| comprendre la mission, les priorités, la philosophie | [`docs/agent/mission.md`](docs/agent/mission.md) |
| écrire un résultat (fiche, JSON, commit, journal) | [`docs/agent/resultats.md`](docs/agent/resultats.md) |
| ranger un fichier, revue de documentation, synthèse | [`docs/agent/rangement.md`](docs/agent/rangement.md) |
| **charger le contexte** (budget, protocole, ce qu'on ne charge pas) | [`docs/agent/contexte.md`](docs/agent/contexte.md) |
| **dessiner un schéma**, convertir un diagramme, améliorer une illustration | [`docs/agent/illustrations.md`](docs/agent/illustrations.md) |
| lancer ou lire les portes | [`docs/agent/portes.md`](docs/agent/portes.md) |
| étudier Panini/Nipada, la généalogie | [`docs/agent/panini-nipada.md`](docs/agent/panini-nipada.md) |
| concevoir un test d'entrée/sortie, corriger | [`docs/agent/miroir.md`](docs/agent/miroir.md) |
| planifier une campagne, le matériel, carpe diem | [`docs/agent/ressources.md`](docs/agent/ressources.md) |
| **les jeux symboliques** (surface → RSN-jeu → pensée, 71 langues, maîtres) | [`docs/jeux-symboliques.md`](docs/jeux-symboliques.md) |
| **le protocole sémantique** (rejouer, convergence, sens → texte, raisonnement gelé) | [`docs/protocole-semantique.md`](docs/protocole-semantique.md) |
| **l'état courant** (synthèse + chantiers + questions) | [`docs/en-cours.md`](docs/en-cours.md) |
| le **vocabulaire** (couche vs étage, termes du dépôt) | [`docs/glossaire.md`](docs/glossaire.md) |
| **trouver un sujet** (un concept, un chantier, une phase) | [`docs/carte.md`](docs/carte.md) |
| la carte de la documentation (l'inventaire) | [`docs/README.md`](docs/README.md) |

> **Chargement facultatif.** Les documents de cette table, `docs/en-cours.md`, `docs/roadmap.md`, `reports/` et
> `journal/` ne se lisent **que pour la tâche en cours** : le fichier de tâche suffit le plus souvent. Ne pas les
> charger « pour être complet » — c'est du contexte qui coûte et qui périme.

> **Le contexte est un budget.** Par défaut : `AGENTS.md` + `docs/en-cours.md` + **un** document de
> tâche. Le protocole, les budgets et les cas « ne pas charger » sont dans
> [`docs/agent/contexte.md`](docs/agent/contexte.md) ; la vérification est
> `python3 tools/taille_documents.py`.

## 4. Le minimum avant de conclure

- l'état est à jour dans [`docs/en-cours.md`](docs/en-cours.md) (synthèse, chantiers, questions en attente) ;
- la **roadmap** est à jour : le chantier fini y est marqué, le suivant est désigné ;
- la fiche est dans `reports/`, le récit dans `journal/`, le commit porte le chiffre ;
- les portes sont vertes, **hors les deux rouges structurelles connues** ;
- la revue de documentation passe, et les liens résolvent.
- le budget de contexte est vérifié : `python3 tools/taille_documents.py`.
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

⏵ Je commence par explorer le dépôt et A7.5 pour comprendre le modèle réseau existant.

- **bash** `{"command": "pwd && ls", "description": "List repository root", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
/home/stephane/GitHub/Qtrinet
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
  ```

- **bash** `{"command": "ls tools/ | head -80; echo ---; ls tools/cerveau/tests/ | head -40", "description": "List tools and test directories", "workdir": "/home/stephane/GitHub/Qtrinet"}`

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
banc-experts.py
banc_lecteur.py
banc-prelire.py
blanchiment_entree.py
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
campagne-benefices.sh
campagne_synthese.py
cancellation_langue.py
carte_coupe.sh
carte-facultes.sh
carte-fenetre-puits.sh
carte_langues.py
carte_latence.sh
carte-sortie-profondeur.sh
cca_raisonnement.py
census_routage.py
cerveau
chat.py
clusters_moe.py
code_partage.py
colab_cote_local.sh
compare_etats.py
compare_logits.py
compare_professeurs.py
comparer_noyaux.py
composition_latente.py
composition_multilingue.py
composition_verne.py
construire-niah.py
contenu_par_couche.py
contrastif_hors_e
… [868 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/grappe_reseau.py tools/cerveau/tests/test_grappe_reseau.py tools/carte_latence.py 2>/dev/null", "description": "Count lines in key files", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
134 tools/grappe_reseau.py
  26 tools/cerveau/tests/test_grappe_reseau.py
 160 total
[exit code: 1]
  ```

- **grep** `{"pattern": "A7\\.5|grappe_reseau", "include": "*.md", "path": "/home/stephane/GitHub/Qtrinet/docs"}`

  ```
Found 5 matches

/home/stephane/GitHub/Qtrinet/docs/en-cours.md
Line 56: - **A7.5 grappe réseau** — flux sparse **1 672 o** contre **7 416** dense (**4,44×**), fidélité **1 792/1 792**, **5/5** messages identiques, **0,125 ms** loopback ; contrôle dense.

/home/stephane/GitHub/Qtrinet/docs/roadmap.md
Line 125: | A7.5 | **La grappe sur le réseau** : transporter le flux v2 entre deux processus, mesurer latence, octets et fidélité | ✅ **mesuré** | **4,44×** moins d'octets (1 672 o contre 7 416), fidélité **1 792/1 792**, messages **5/5** identiques, **0,125 ms** loopback ; contrôle dense — [`reports/rapport-grappe-reseau.md`](../reports/rapport-grappe-reseau.md) |
Line 127: **Prochaine action** : aucune sur A7.5 — le transport sparse est **mesuré** (4,44×, fidélité 100 %, 0,125 ms loopback). La suite (exécution d'une couche à distance, WAN) reste **hors plan**.
Line 431: 12. **A7.5 — la grappe sur le réseau** : le format sparse est mesuré (4,22×) ; le **transport réel** (latence,

/home/stephane/GitHub/Qtrinet/docs/carte.md
Line 51: | **A7.5** grappe réseau | **mesuré** — 4,44× moins d'octets, fidélité 100 %, 0,125 ms loopback | [la fiche](../reports/rapport-grappe-reseau.md) |
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/grappe_reseau.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_grappe_reseau.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/grappe_reseau.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """grappe_reseau.py — A7.5 : transporter la grappe sparse entre deux processus.
3: 
4: Le format v2 de K3RL (masque 1 bit par canal + valeurs f32 non nulles) est
5: mesuré localement en A7.4 (1 704 o contre 7 196 o). Ici on le **sérialise**,
6: on l'envoie par **TCP loopback** à un second processus, on le **relit** et on
7: compare : octets, fidélité, latence. Le contrôle est le flux **dense**.
8: """
9: from __future__ import annotations
10: 
11: import json
12: import socket
13: import struct
14: import threading
15: import time
16: 
17: MAGIC = b"K3RL"
18: VERSION = 2
19: 
20: 
21: def encoder(flux: list[list[float]], dense: bool = False) -> bytes:
22:     """Encode un flux (n_tokens × canaux) en v2.
23: 
24:     `dense=False` : masque des non-nuls + valeurs (le flux sparse).
25:     `dense=True`  : masque plein + toutes les valeurs (le contrôle).
26:     """
27:     ntok = len(flux)
28:     h = len(flux[0]) if ntok else 0
29:     out = bytearray(MAGIC)
30:     out += struct.pack("<I", VERSION)
31:     out += struct.pack("<Q", ntok)
32:     out += struct.pac
… [4124 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_grappe_reseau.py</path>
<type>file</type>
<content>
1: from __future__ import annotations
2: import sys, pathlib, unittest
3: sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
4: from tools.grappe_reseau import encoder, decoder
5: 
6: 
7: class TestGrappeReseau(unittest.TestCase):
8:     def test_aller_retour(self):
9:         flux = [[0.0, 1.0, 0.0, 2.0], [0.0, 0.0, 3.0, 0.0]]
10:         b = encoder(flux)
11:         relu, meta = decoder(b)
12:         self.assertEqual(relu, flux)
13:         self.assertEqual(meta["nval"], 3)
14: 
15:     def test_sparse(self):
16:         flux = [[0.0, 1.0, 0.0, 2.0]]
17:         dense = encoder(flux, dense=True)
18:         sparse = encoder(flux)
19:         self.assertLess(len(sparse), len(dense))
20:         relu, _ = decoder(sparse)
21:         self.assertEqual(relu[0][3], 2.0)
22:         self.assertEqual(relu[0][1], 1.0)
23: 
24: 
25: if __name__ == "__main__":
26:     unittest.main()

(End of file - total 26 lines)
</content>
  ```

- **grep** `{"pattern": "A3\\.3|3,2 ×|budget_execution_locale|carte_latence", "path": "/home/stephane/GitHub/Qtrinet/docs"}`

  ```
Found 8 matches

/home/stephane/GitHub/Qtrinet/docs/roadmap.md
Line 71: | A3.3 | **Seuil de rentabilité** : à quel débit/latence le découpage gagne | 🔬 | attente ≈ calcul distant + **3,2 × latence** : 1,01× à 0 ms, 1,99× à 5 ms, 4,89× à 20 ms ; le débit ne compte pas (0,25 Mbit/s) |

/home/stephane/GitHub/Qtrinet/docs/glossaire/06-repartition-materiel-et-energie.md
Line 58: compte quatre fois » — `attente ≈ calcul distant + 3,2 × latence`

/home/stephane/GitHub/Qtrinet/docs/glossaire/index.json
Line 1282:       "resume": "Le *débit* est ce qui passe par seconde (Go/s, tok/s, événements/s) ; la *latence* est le délai d'un aller-retour. Leçon du transport réparti : « le débit ne compte pas (0,25 Mbit/s), la latence compte quatre fois » — `attente ≈ calcul distant + 3,2 × latence` (`docs/roadmap.md:57`)."

/home/stephane/GitHub/Qtrinet/docs/archive/plan-kimi-k3.md
Line 48: | **poids lus par jeton** | **86,787 Go** (mesuré, bloc 31 — voir 1b) | `tools/budget_execution_locale.py` sur les 32 shards |

/home/stephane/GitHub/Qtrinet/docs/archive/plan-cerveau-complet.md
Line 96:   `tools/carte_latence.sh`, relais TCP `tools/proxy_latence.py`) et vérifier que la
Line 278:   réglable) et `too
… [651 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i -E 'grappe|latence|reseau|seuil' ; echo ---; sed -n '1,80p' reports/rapport-grappe-reseau.md 2>/dev/null", "description": "Find related reports and read grappe report", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
grappe-reseau.json
rapport-grappe-deportee.md
rapport-grappe-intra-couche.md
rapport-grappe-reseau.md
rapport-grappes.md
rapport-prelire-grappe.md
seuil-bruit-3b.json
---
# A7.5 — la grappe sur le réseau : fidélité exacte, 4,44× moins d'octets

> **Objet.** A7.4 mesurait le **volume** du flux sparse (masque + valeurs). A7.5 le **transporte**
> entre deux processus par TCP loopback, vérifie la **fidélité**, et mesure la **latence**.

## Dispositif

- Flux synthétique **4 jetons × 448 canaux**, **356 non-nuls** (19,9 %).
- Format **K3RL v2** : masque **par jeton**, 1 bit par canal, puis les valeurs `f32`.
- Contrôle **dense** : masque plein, toutes les valeurs.
- Deux processus, **TCP 127.0.0.1**, **5 essais** ; le serveur renvoie `OK`.

## Résultats

| mesure | valeur |
|---|---:|
| flux dense | **7 416 o** |
| flux sparse | **1 672 o** |
| rapport | **4,44×** |
| fidélité (cases exactes) | **1 792 / 1 792 = 100 %** |
| réseau, messages identiques | **5 / 5** |
| latence loopback moyenne | **0,125 ms** |
| latence min / max | 0,073 / 0,186 ms |

## Lecture

- Le flux sparse **passe le réseau sans perte** : les 1 792 cases sont reconstruites, y compris
  les zéros.
- Le **volume** es
… [1148 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/ | grep -i -E 'latence|proxy|reseau|deport'; echo ---; sed -n '1,120p' tools/proxy_latence.py 2>/dev/null", "description": "Inspect latency proxy tooling", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
carte_latence.sh
grappe_reseau.py
proxy_latence.py
---
#!/usr/bin/env python3
"""Relais TCP qui ajoute une latence par message, pour mesurer ce qu'un lien
distant coûte à un découpage de modèle.

Pourquoi : sur localhost, l'attente du pair vaut 1,01× le calcul local — c'est un
plancher optimiste. Une VM Colab est à quelques dizaines de millisecondes, et la
phase 3.3 demande « à partir de quel débit le découpage gagne ». Le débit n'est
jamais le problème (0,25 Mbit/s) ; la latence, si. Ce relais la rend réglable.

    python3 tools/proxy_latence.py <port_écoute> <hôte_cible:port> [délai_ms]
"""
import socket, sys, threading, time


def relais(src, dst, delai):
    try:
        while True:
            donnees = src.recv(65536)
            if not donnees:
                break
            if delai:
                time.sleep(delai)
            dst.sendall(donnees)
    except OSError:
        pass
    finally:
        for s in (src, dst):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass


def main():
    port = int(sys.argv[1])
    hote, port_cible = sys.argv[2].rsplit(":", 1)
    delai = float(sys.argv[3]) / 1000.0 if len(s
… [732 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '30,90p' docs/archive/colab-reparti.md; echo =====; sed -n '1,120p' reports/rapport-grappe-deportee.md", "description": "Read distributed latency doctrine and report", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
|---|---|
| fidélité du découpage | ✅ écart **0,00e0** entre local et deux nœuds (40 et 200 jetons) |
| version du protocole | ✅ dans chaque en-tête ; un pair incompatible est refusé en le disant |
| réglages qui changent les chiffres | ✅ niveaux, seuil, top-k, renorm, les sept top-k par projection, attn/qk/moe top-k (14 champs) voyagent dans l'en-tête |
| latence | ✅ `TCP_NODELAY` : 16,1 ms d'attente contre 15,9 ms de calcul local (97,6 ms avant) |
| au-delà de localhost | ✅ testé sur l'IP du réseau local (`--flux-serveur 0.0.0.0:PORT`) |
| **deux machines avec le même fichier GGUF** | ❌ les deux nœuds chargent le modèle ENTIER (`Model::load` lit tout le fichier) — le découpage porte sur le CALCUL |
| **préremplissage par lots sur le fil** | ✅ mode 3, `--lot T` : 256 jetons en 4 lots, écart **0,00e0** (`reports/rapport-prefill-reparti.md`) ; mode 4 (lot en listes) : 1,5 ko par jeton au lieu de 3,5 |

La limite qui reste est assumée, pas oubliée : **les deux nœuds chargent le
modèle entier**. Un petit modèle tient sur les deux machines ; c'est le
préremplissage par lots (fait depuis) qui manquait pour que la démonstration ne
paie pas la latence 256 fois.

## Dimensionnement (mesuré
… [3843 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/grappe_reseau.py", "description": "Run A7.5 module to check current byte counts", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
{
 "flux": {
  "ntok": 4,
  "canaux": 448,
  "top": 96
 },
 "octets": {
  "dense": 7416,
  "sparse": 1672,
  "ratio": 4.435406698564593
 },
 "fidelite": {
  "exact": 1792,
  "total": 1792,
  "taux": 1.0
 },
 "reseau": {
  "essais": 5,
  "identiques": true,
  "latence_ms_moyenne": 0.16609919839538634,
  "latence_ms_min": 0.1005029771476984,
  "latence_ms_max": 0.23187699844129384
 },
 "meta": {
  "version": 2,
  "ntok": 4,
  "h": 448,
  "nval": 356,
  "octets": 1672
 }
}
  ```

- **bash** `{"command": "cat reports/grappe-reseau.json", "description": "Read stored A7.5 JSON", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
{
 "flux": {
  "ntok": 4,
  "canaux": 448,
  "top": 96
 },
 "octets": {
  "dense": 7416,
  "sparse": 1672,
  "ratio": 4.435406698564593
 },
 "fidelite": {
  "exact": 1792,
  "total": 1792,
  "taux": 1.0
 },
 "reseau": {
  "essais": 5,
  "identiques": true,
  "latence_ms_moyenne": 0.11005760170519352,
  "latence_ms_min": 0.07033199653960764,
  "latence_ms_max": 0.15113898552954197
 },
 "meta": {
  "version": 2,
  "ntok": 4,
  "h": 448,
  "nval": 356,
  "octets": 1672
 }
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nh=448; ntok=4\nn=0; z=[]\nfor t in range(ntok):\n    for i in range(0,h,5):\n        v=float((t+1)*(i+1)%97)/97.0\n        if abs(v)>1e-12: n+=1\n        else: z.append((t,i))\nprint(n, len(z), z)\nEOF", "description": "Count non-null cells in synthetic flux", "workdi … [36 caractères tronqués]`

  ```
356 4 [(0, 290), (1, 290), (2, 290), (3, 290)]
  ```

- **bash** `{"command": "python3 --version; sed -n '1,160p' tools/carte_latence.sh", "description": "Check Python version and latency sweep script", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
Python 3.13.15
#!/bin/bash
# carte_latence.sh — « à partir de quel aller-retour le découpage cesse de payer ? »
#
# POURQUOI CETTE CARTE. Le découpage à deux nœuds est prouvé exact (écart 0,00e0,
# § 8 et portes). Mais il est prouvé sur LOCALHOST, où l'aller-retour vaut quelques
# dizaines de microsecondes — un plancher optimiste. Sur un vrai réseau, la
# question n'est pas le débit (0,25 Mbit/s de flux) mais la LATENCE par message :
# chaque jeton traverse la frontière une fois par couche échangée.
#
# `tools/proxy_latence.py` est un relais TCP qui ajoute un délai réglable. On
# l'intercale entre le pilote et le nœud, et on refait la mesure pour 0, 1, 5, 20
# et 50 ms : le temps mur dit où le découpage perd son avantage, et la perplexité
# dit si le transport reste exact (elle ne doit PAS bouger).
#
# Usage :
#   carte_latence.sh [--modele M.gguf] [--ids F] [--couches 2] ["--delais 0 1 5 20 50"]
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
MODELE=/tmp/m5_d384_route_distille.gguf
IDS=${IDS:-/tmp/campagne24/route_ids128.txt}
COUCHES=2
LIMITE=128
CTX=256
DELAIS="0 1 5 20 50"
while [ $# -gt 0 ]; do
    case "$1" in
        --modele) MODELE="$2"; shift 2 ;;

… [1958 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' tools/analyse_octets_par_jeton.py", "description": "Inspect a comparable measurement tool style", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
#!/usr/bin/env python3
"""analyse_octets_par_jeton.py — combien d'octets de POIDS un jeton fait-il lire ?

Lit l'en-tête d'un GGUF (sans lire les données), repère les tenseurs d'experts,
et calcule le volume lu par jeton :

    octets/jeton = Σ_couches [ (k_routés / n_experts) × octets(exps)
                               + octets(expert partagé) ]

C'est le chiffre qui décide de trois choses :
  - si un modèle tient en RAM (sinon chaque passe relit ces octets du disque) ;
  - ce que coûterait un chemin GPU qui streame les poids (PCIe) au lieu de les
    garder en VRAM ;
  - ce que coûte un découpage en nœuds (chaque nœud ne lit que sa part).

Usage : analyse_octets_par_jeton.py <modele.gguf> [--experts-par-jeton N]
                                    [--tous]
"""
import struct
import sys

# Éléments par bloc et octets par bloc des formats ggml (le strict nécessaire ;
# un type absent est signalé, jamais deviné).
TYPES = {
    0: ("F32", 1, 4), 1: ("F16", 1, 2), 2: ("Q4_0", 32, 18), 3: ("Q4_1", 32, 20),
    6: ("Q5_0", 32, 22), 7: ("Q5_1", 32, 24), 8: ("Q8_0", 32, 34), 9: ("Q8_1", 32, 36),
    10: ("Q2_K", 256, 84), 11: ("Q3_K", 256, 110), 12: ("Q4_K", 256, 144),
    13: ("Q5_K", 2
… [4004 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport time, statistics\nfrom tools.grappe_reseau import encoder, decoder\nh=448; ntok=4\nflux=[[0.0]*h for _ in range(ntok)]\nfor t in range(ntok):\n    for i in range(0,h,5):\n        flux[t][i]=float((t+1)*(i+1)%97)/97.0\nd=encoder(flux,dense=True); s=encoder(flux) … [543 caractères tronqués]`

  ```
7416 1672 4.435406698564593
enc_d median 0.5779 min 0.568 mean 0.5794
enc_s median 0.2491 min 0.2464 mean 0.2514
dec_d median 0.4886 min 0.4797 mean 0.4893
dec_s median 0.3701 min 0.3665 mean 0.3728
  ```

- **bash** `{"command": "grep -rn \"A20\\|seuil de rentabilité\\|rentabilité réseau\" docs reports journal --include=*.md | head -30", "description": "Search for A20 or network break-even references", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
reports/rapport-localite-activation.md:27:| déport GPU | matrices entières, seuil de rentabilité mesuré (8 Mo) | granularité **grossière** : pas de placement par neurone |
reports/rapport-transport-liste.md:229:C'est aussi la réponse à la phase 3.3 : **le seuil de rentabilité est une
reports/rapport-coherence-docs.md:152:| 64 | `docs/roadmap.md:293` | « Ce qui reste : le transport lui-même (3.2), la granularité, le seuil de rentabilité et la version du format » | les quatre sont livrés (tableaux 55-59 du même document) : la conclusion contredit l'état affiché plus haut | CONTRADICTOIRE |
reports/archive/rapport-toutes-langues.md:1308:| **A200 · réservoir (5× plus large)** | 400 | **0,6218** |
reports/archive/rapport-toutes-langues.md:1329:La variante **A200 + entrée** — la plus intéressante, puisqu'elle dirait ce qu'un
reports/archive/rapport-toutes-langues.md:1503:| A200 · réservoir | 400 | 0,6218 | +0,0540 |
reports/archive/rapport-toutes-langues.md:1507:| **A200 + entrée LINÉAIRE** | **1 296** | **0,6738** | **+0,1059** |
reports/archive/rapport-toutes-langues.md:1511:**A200 + entrée (1 296 caractéristiques) bat C_quad (1 792) et A40 + entrée (1 872)
reports/archive/rapport-tout
… [3958 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"A20\\|seuil_reseau\" . --include=*.py --include=*.sh --include=*.md 2>/dev/null | grep -v __pycache__ | head -20", "description": "Search whole repo for existing threshold work", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
./reports/archive/rapport-toutes-langues.md:1308:| **A200 · réservoir (5× plus large)** | 400 | **0,6218** |
./reports/archive/rapport-toutes-langues.md:1329:La variante **A200 + entrée** — la plus intéressante, puisqu'elle dirait ce qu'un
./reports/archive/rapport-toutes-langues.md:1503:| A200 · réservoir | 400 | 0,6218 | +0,0540 |
./reports/archive/rapport-toutes-langues.md:1507:| **A200 + entrée LINÉAIRE** | **1 296** | **0,6738** | **+0,1059** |
./reports/archive/rapport-toutes-langues.md:1511:**A200 + entrée (1 296 caractéristiques) bat C_quad (1 792) et A40 + entrée (1 872)
./reports/archive/rapport-toutes-langues.md:1895:La fidélité de `A200 + entrée` vaut 0,6738 avec **toutes** les lignes et 0,6693 avec
./reports/toutes-langues/031-31-controle-de-capacite-lentree-gagne-t-ell.md:16:| **A200 · réservoir (5× plus large)** | 400 | **0,6218** |
./reports/toutes-langues/031-31-controle-de-capacite-lentree-gagne-t-ell.md:37:La variante **A200 + entrée** — la plus intéressante, puisqu'elle dirait ce qu'un
./reports/toutes-langues/034-34-correction-du-29-le-reservoir-netait-pas.md:20:| A200 · réservoir | 400 | 0,6218 | +0,0540 |
./reports/toutes-langues/034-34-correction-du-29-le-re
… [1291 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '200,270p' reports/rapport-transport-liste.md", "description": "Read transport-list report threshold conclusion", "workdir": "/home/stephane/GitHub/Qtrinet"}`

  ```
(`set_nodelay(true)`, des deux côtés) divise l'attente par six.

### Et si le lien est lent ? Mesuré avec un relais retardateur

Localhost est un plancher optimiste : `tools/proxy_latence.py` ajoute un délai
par message et on refait le banc (256 jetons de vrai texte, 12 couches par nœud).

| latence ajoutée | attente du pair | rapport au calcul local | durée du banc | écart |
|---|---|---|---|---|
| 0 ms | 16,8 ms/jeton | 1,01× | 11,0 s | 0,00e0 |
| 5 ms | 33,0 ms/jeton | 1,99× | 15,1 s | 0,00e0 |
| 20 ms | 81,8 ms/jeton | 4,89× | 27,6 s | 0,00e0 |

La fidélité ne bouge pas d'un bit (0,00e0 partout : la latence ne change pas le
calcul, elle change le temps). Et l'attente suit une droite simple :

```
attente ≈ calcul distant + 3,2 × (latence par message)
```

Le facteur 3,2 est le nombre de messages retardés par jeton dans ce banc (le flux
et sa réponse, dans les deux sens). **C'est la formule de la phase 3.3** :
le débit ne compte pas (0,25 Mbit/s suffisent), la latence compte quatre fois.

Application à Colab : un aller-retour de 60 ms donne 16 + 3,2 × 30 ≈ **112 ms par
jeton**, soit ~8 jetons/s au lieu de ~60 en local. Le découpage ne sert donc pas à
accélérer — il sert à faire 
… [503 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport time, statistics\nfrom tools.grappe_reseau import encoder, decoder\nh=448; ntok=4\n# densité 100 %\nflux=[[float(((t+1)*(i+1))%97)/97.0 for i in range(h)] for t in range(ntok)]\nd=encoder(flux,dense=True); s=encoder(flux)\nprint('bytes', len(d), len(s))\nfor na … [431 caractères tronqués]`

  ```
bytes 7416 7352
enc_d 0.5804 0.5691
enc_s 0.6513 0.6393
dec_d 0.4948 0.431
dec_s 0.4598 0.4293
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport time, statistics\nfrom tools.grappe_reseau import encoder, decoder\nh=448; ntok=4\nflux=[[(1.0+((t+1)*(i+1))%96)/97.0 for i in range(h)] for t in range(ntok)]\nd=encoder(flux,dense=True); s=encoder(flux)\nprint('bytes', len(d), len(s), sum(1 for r in flux for v … [467 caractères tronqués]`

  ```
bytes 7416 7416 1792
enc_d 0.5787 0.5688
enc_s 0.6493 0.5717
dec_d 0.4779 0.4362
dec_s 0.4728 0.4357
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport time, statistics, math\nh=448; top=96; ntok=4\nflux=[[0.0]*h for _ in range(ntok)]\nfor t in range(ntok):\n    for i in range(0,h,5):\n        flux[t][i]=float((t+1)*(i+1)%97)/97.0\nW=[[math.sin((j+1)*(i+1)*0.017) for i in range(h)] for j in range(top)]\ndef ca … [605 caractères tronqués]`

  ```
calc ms median 1.9225 min 1.8975 mean 1.9293
  ```

