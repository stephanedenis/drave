# Session DSH — relecture

- identifiant : `session-e466b49c-4fcb-4b34-b5a8-5bc193487415`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-16 04:11:48
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche Z2 (clôture technique) : la **passe complète** — `bash tools/toutes-les-portes.sh` avec `JOURNAUX=work/portes/passe-1611` ; lis le registre par `awk '$2 != 0'` (jamais par un tail) ; note les rouges, compare aux **rouges tolérées** de `docs/pilotage/references-non-regression.md`, mets à jour la section « passe » du document, et écris `reports/rapport-passe-1611.md` + JSON (portes, vertes, rouges, la liste).

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

- **bash** `{"command": "pwd && ls && echo \"---\" && ls tools | head -50 && echo \"---\" && ls docs/pilotage | head -50", "description": "Inspect workspace structure"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
AGENTS.md
bench
build
colab
data
dist
docs
drave-core
drave.egg-info
journal
models
__pycache__
pyproject.toml
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
---
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
atomes_prediction.py
audit_drapeaux_harnais.py
banc_cli_robuste.py
banc_complet.py
banc_durci.py
banc-experts.py
banc_lecteur.py
banc_lecture.py
banc_performance.py
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
c8_car
… [414 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md</path>
<type>file</type>
<content>
1: # Références de non-régression
2: 
3: > **Passe — 2026-11-16 00 h 45 → 03 h 01 :** **86 portes, 82 vertes, 4 rouges** — `indice` et
4: > `melange` structurelles ; `produit` (V1 inachevée) et `sessions` (heartbeat) de circonstance.
5: > Journaux `work/portes/roue-1116/`. **Vérification ciblée (V3)** : `sessions` **0** et `produit`
6: > **0** (`--strict` 5 tests, exemples **27/27**, autotest **183/183**) ; journaux
7: > `work/portes/verif-cloture-1116/`. Après : **84 vertes, 2 rouges structurelles**.
8: 
9: > **Passe — 2026-11-15 09 h 53 → 12 h 15 :** **85 portes, 81 vertes, 4 rouges** — `indice` et
10: > `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prechargement`
11: > **environnementale** (deux passes en parallèle ; PPL identique 799,8557 ; verte le 14/11).
12: > Journaux `work/portes-1115-09h53/`. **Pas de passe complète pour W6** ; ciblage
13: > `work/portes/w6-ciblage` (8/9), `w6-ciblage2` (2/2) puis `w6-final` (9/9).
14: 
15: > **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
16
… [14062 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/portes.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/portes.md</path>
<type>file</type>
<content>
1: # Les portes : lancer, lire le verdict, ne pas se tromper de rouge
2: 
3: > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.
4: 
5: ## La commande
6: 
7: ```bash
8: bash tools/toutes-les-portes.sh
9: ```
10: 
11: Elle lance **toutes** les `tools/porte-*.sh`, séquentiellement, **sans s'arrêter à la première rouge** (on veut le
12: [tableau](../theorie/glossaire/entrees/tableau.md), pas la première tuile), et borne **chaque** [porte](../theorie/glossaire/entrees/porte.md) à `DELAI=1800` s. Durée observée d'une passe complète :
13: **1 h 30 – 2 h** sur Hauru (**83 portes** ; certaines entraînent de petits modèles, d'autres utilisent les [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md) ;
14: `porte-deepseek` est **hors réseau** et rapide). La dernière passe complète à **82 portes** (03/11 11 h 30, **machine au repos**, **1 h 48**) a donné
15: **80 vertes, 2 rouges** (les 2 connues : `indice`, `melange`) ;
16: `porte-reparti-moteur` (ré-étalonnée à 8,7434) et `porte-homeostasie` (
… [4409 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/toutes-les-portes.sh && sed -n '1,200p' tools/toutes-les-portes.sh", "description": "Inspect the gates launcher script"}`

  ```
-rwxr-xr-x. 1 stephane stephane 4422  2 nov 15:55 tools/toutes-les-portes.sh
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
#   4. il garde le journal de chacune (`JOURNAUX`) et n'affic
… [3189 caractères tronqués]
  ```

- **bash** `{"command": "ls work/portes/ 2>/dev/null | head -50; echo \"---reports passe---\"; ls reports | grep -i -E 'passe|portes' | head -30", "description": "List previous gate run dirs and reports"}`

  ```
b1-protocole-03h03
passe-0303-04h10
passe-0303-11h30
passe-1102-19h32
passe-1102-apres-n2
passe-1104-08h00
passe-1311-23h15
passe-1311-23h15.log
passe-1402-02h00
passe-2404-23h45
passe-2404-23h45.debut
passe-2404-23h45.log
roue-1116
sous-passe-1102-16h35
tableaux-rejeu.log
verif-cloture
verif-cloture-1116
w6-ciblage
w6-ciblage2
w6-final
---reports passe---
a80-portes-ppl.json
historique-passes-portes.md
passe-honnetete.json
pensee-troisieme-passe.json
rapport-a80-portes-ppl.md
rapport-passe-complete-13-octobre.md
rapport-passe-complete-portes.md
rapport-passe-honnetete.md
rapport-passe-k3-disque.md
rapport-pensee-troisieme-passe.md
rapport-portes-p0-p9.md
  ```

- **bash** `{"command": "ls -la work/portes/passe-1611 2>/dev/null; echo \"---roue-1116---\"; ls -la work/portes/roue-1116 | head; echo \"---registre tail---\"; tail -5 work/portes/roue-1116/registre.txt; echo \"---non-zero---\"; awk '$2 != 0' work/portes/roue-1116/registre.txt", "description": "Inspect latest  … [30 caractères tronqués]`

  ```
---roue-1116---
total 400
drwxr-xr-x. 1 stephane stephane  3590 16 nov 02:50 .
drwxr-xr-x. 1 stephane stephane   638 16 nov 03:04 ..
drwxr-xr-x. 1 stephane stephane    64 16 nov 01:01 deepseek-porte
-rw-r--r--. 1 stephane stephane 26243 16 nov 01:57 jeux-mesures.json
-rw-r--r--. 1 stephane stephane  9218 16 nov 01:57 langues-mesures.json
-rw-r--r--. 1 stephane stephane  3310 16 nov 01:58 maitres-mesures.json
-rw-r--r--. 1 stephane stephane   580 16 nov 00:46 porte-adaptateur-sortie.log
-rw-r--r--. 1 stephane stephane  1407 16 nov 00:49 porte-audit-drapeaux.log
-rw-r--r--. 1 stephane stephane   398 16 nov 00:49 porte-b1110-hybride.log
---registre tail---
porte-tokenizer-kimi 0 7
porte-topologie 0 114
porte-trace 0 31
porte-vision 0 661
--- 82 vertes, 4 rouges ---
---non-zero---
porte-indice 1 1127
porte-melange 1 149
porte-produit 1 187
porte-sessions 1 0
--- 82 vertes, 4 rouges ---
  ```

- **bash** `{"command": "grep -rn \"Z2\" docs reports journal 2>/dev/null | head -30; echo \"---en-cours---\"; sed -n '1,120p' docs/pilotage/en-cours.md", "description": "Find Z2 references and current state"}`

  ```
snov2mZ/qTiDmwihsIlntN/8yFnTmERH9sdx2tbp49DkD3wlanP16g0qFGo5tC96oCyVCUZQ7jiHY280Xnd4touHx6mES51eAGnSI0JHVeDwbKzRDGaEQT6P3aLj5So32u1heV74Xik8snB0rpCxApGX2xBWV8OpVO10tZQ2ST9UdjJmy22u2ku8I5h8HDnYasa6CjuqMFKYclUCP/jrxDrQdtyurxLg46nL5TTqo4reG1IKlmiCUKYyEXygOVBObYUijUxPri6LgWQ2KRXRwn0gswlLJrtQqV8u3BKBHB64ZlOthuuXy6Cb1tjs8Y56TsoYbE8w/FkbaTuWlDtKttd3zw85YBIbiuDVTBQ2X8iXGMpm/dKRzBKDYYDkBb+X0cVNAIgDMWuhOFjTip/tNKl13FJOHN0YPR6pAE8qDh1kO3310u7QM7XXEss9cMrIVUuab78ooWMogAA23k0ngA/bkmdJppFVvhgjg5axAaatC5xbyxGJqpVzGGU2zfD2LLzPPlcu4uWsxb+2sq6izIi0dFFEYQMq+s05v+GgGXeSPvl7oVdkamkg2vlb2Bx1HE61LWctxvxdz3SEh+hXusi/TaXC7+x5r7W1AA6ZS6lWTVa426Xd7M2OyBGJ2pLuB+EKiQ/spHSeBvvIHJxXauLC2OywAv6jr4zKfwzzy4Jhr/i/GFqcWqfmIWaqRWc4SRPltDMul7dFACr0uhquHEVtfAYQ8YSq/UfIDmLt8jcZoOz5T/s4aqhE7/MNF6g+qYjflgFo60+Byh5ECqzLnvAMnbqtMy44jV3YjuinIYQvePCH1DK75PQoXQ41P/rBmd8ZqMCshDz8keZw90MljgsFRGPFh8xljWx9D9t53RlMt/C5pvN/tq6b/HavsOd2wqMnSbqNQNebRcE/A+CBf4zApSlfAeBO5WWoqyD6aTYVLYv4tb6p8xSoPhsFNyXUheX7DQBr1470lvue2a3YL+C81SgIqUc8stMKIK3ot+bPggFdTA6h7o0S2OFfIRcceK6lu52ZRg3giGZsdPGcFEx27DQsHi+Li8a89u++Rz+6nMti3GmbDA2HOmELZtpaRK/ntUEvgC0YVKTVsh0appR8H5Sw9TTPhhEpxE3q7qdH3XC3F5tb87/9tPk+l4xW6i4YBKTbxkbyg+oa+YZvlnXzbwbX6NpNzPd3LCXqn0eMnaS4
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-passe-complete-portes.md", "description": "Read prior pass report format"}`

  ```
# Passe COMPLÈTE des portes : de 22 à 47 portes — et une porte qui était verte en ne mesurant RIEN

> Campagne : **outillage** · expérience : la passe complète (`tools/toutes-les-portes.sh`)
> Question : les portes du dépôt passent-elles **toutes**, quand on les lance **toutes** ?
> Verdict : **oui, à chaque passe** — **22 sur 22** au premier passage (2026-10-10, 11 h 07), puis les passes
> successives consignées ci-dessous, jusqu'à la **47ᵉ porte** (`porte-diff-couche`, ajoutée le 24/10 — elle vérifie
> la reproductibilité du flux et nomme les divergences). Et la passe a trouvé ce qu'une porte lancée seule ne
> pouvait pas montrer : `porte-tokenizer-kimi` sortait **verte en comparant zéro jeton** (elle lisait `stdin`, que
> personne ne lui fournissait). Corrigée, elle compare maintenant **10 textes** en **7,5 s**.
>
> *Les sections 2 bis à 2 quater consignent les passes historiques ; la section 2 quinquies attend le verdict de
> la passe du 24/10 (47 portes) — elle n'est pas écrite d'avance.*
> Date réelle : **2026-10-10 11:10 HAE** (heure de la machine ; la passe a tourné de 09 h 57 à
> 11 h 07).
> Protocole : `DELAI=2400 tools/toutes-les-portes.sh` — chaque porte bornée dans le 
… [8229 caractères tronqués]
  ```

- **bash** `{"command": "date; echo \"---git---\"; git status --short | head -30; git log --oneline -3; echo \"---nvidia---\"; nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader 2>/dev/null || echo \"no nvidia-smi\"; echo \"---load---\"; uptime", "description": "Check da … [23 caractères tronqués]`

  ```
lun 16 nov 2026 04:12:02 EST
---git---
 M tools/chantier/plan.json
19992f2f Z1 — L'INTÉGRATION CONTINUE : MATRICE 3.10/3.13, 10/10 ÉTAPES VERTES (ARCHIVE SANS SOUS-MODULE, COPIE DE SECOURS S) ; PORTE 183/183 ; TEST CASSÉ → 1, JOB ARRÊTÉ ; act ABSENT, YAML PARSÉ
3c10e3ee V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON
ae3c24f2 V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
---nvidia---
0, 154 MiB, 16384 MiB, 1 %
1, 4 MiB, 16384 MiB, 0 %
---load---
 04:12:03  up 12 days  8:38,  2 users,  load average: 11,00, 14,84, 15,07
  ```

- **bash** `{"command": "ls journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/ 2>/dev/null; echo \"---plan---\"; sed -n '1,160p' journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/plan.md 2>/dev/null", "description": "Read the Z session plan"}`

  ```
digest.md
rapport.md
session.v4.jsonl.zstd
---plan---
[exit code: 2]
  ```

- **bash** `{"command": "ls -la work | head; echo \"---porte count---\"; ls tools/porte-*.sh | wc -l; echo \"---ressources---\"; bash tools/porte-ressources.sh 2>&1 | tail -15", "description": "Count gates and check resources gate"}`

  ```
total 240
drwxr-xr-x. 1 stephane stephane  2514 16 nov 00:30 .
drwxr-xr-x. 1 stephane stephane   774 16 nov 03:32 ..
-rw-r--r--. 1 stephane stephane  1040 15 nov 03:23 atomes_cohortes.py
-rwxr-xr-x. 1 stephane stephane  2133  2 nov 16:46 attente_portes.sh
drwxr-xr-x. 1 stephane stephane   562 16 nov 00:49 banc-performance
drwxr-xr-x. 1 stephane stephane   362 16 nov 03:27 chantier
drwxr-xr-x. 1 stephane stephane   168  7 nov 15:06 corpus-commun
-rw-r--r--. 1 stephane stephane  6879  1 nov 12:49 corpus-wiki-langues.log
-rw-r--r--. 1 stephane stephane  1004  1 nov 11:14 corpus-wiki.log
---porte count---
86
---ressources---
=== PORTE RESSOURCES — REGISTRE, CLAIMS, COHÉRENCE ===
  ✅ autotest : 9 cas (claim, conflit, file, admission, check)
  ✅ registre cohérent : aucune ressource sur-réservée.
  ⚠ nvme_raid : 33 Gio libres seulement
  ✅ registre cohérent ; les avertissements de stockage/NUMA sont affichés, pas fatals
  === GPU : aucun serveur local d'inférence (llama-server, ollama) ===
     ✅ GPU libres ou occupés par Drave ; aucun serveur local
✅ porte ressources verte : autotest 9 cas, registre cohérent, GPU réservés à Drave
  ```

- **bash** `{"command": "pgrep -af \"toutes-les-portes|porte-\" | head -20; echo \"---\"; ls -d work/portes/passe-1611 2>/dev/null || echo \"pas encore de dossier\"", "description": "Check for a running pass"}`

  ```
1759640 node26 /home/stephane/.local/share/../bin/dsh --profile headless Tâche Z2 (clôture technique) : la **passe complète** — `bash tools/toutes-les-portes.sh` avec `JOURNAUX=work/portes/passe-1611` ; lis le registre par `awk '$2 != 0'` (jamais par un tail) ; note les rouges, compare aux **rouges tolérées** de `docs/pilotage/references-non-regression.md`, mets à jour la section « passe » du document, et écris `reports/rapport-passe-1611.md` + JSON (portes, vertes, rouges, la liste).
1759913 bash -c pgrep -af "toutes-les-portes|porte-" | head -20; echo "---"; ls -d work/portes/passe-1611 2>/dev/null || echo "pas encore de dossier"
---
pas encore de dossier
  ```

- **bash** `{"command": "mkdir -p work/portes/passe-1611\nJOURNAUX=work/portes/passe-1611 bash tools/toutes-les-portes.sh > work/portes/passe-1611/passe-1611.log 2>&1\necho \"EXIT=$?\"", "description": "Run the complete gates pass", "run_in_background": true}`

  ```
started background job bash-11
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md"}`

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

- **bash** `{"command": "echo \"=== passe-honnetete.json ===\"; sed -n '1,80p' reports/passe-honnetete.json; echo \"=== a80-portes-ppl.json ===\"; sed -n '1,60p' reports/a80-portes-ppl.json", "description": "Read example result JSON files"}`

  ```
=== passe-honnetete.json ===
{
 "schema": "drave.passe-honnetete",
 "version": 1,
 "tache": "J9.1",
 "titre": "La passe d'honnêteté des fiches",
 "date": "2026-11-14",
 "ligne": "B13",
 "verdict": "ok",
 "head": "229098ec",
 "etat_courant": {
  "source": [
   "reports/rapport-s065.md",
   "docs/pilotage/en-cours.md"
  ],
  "commande": [
   "python3 tools/drave.py evaluer --json",
   "python3 tools/drave.py evaluer --gold --json"
  ],
  "vivant": {
   "phrases": 612,
   "tokens": 3179,
   "pos": 0.8625,
   "f1_syntagmes": 0.7902,
   "tete": 0.9029,
   "cibles_attachement": 239,
   "labels_attachement": 238,
   "exact": 238,
   "exact_taux": 0.9958,
   "topk": 236,
   "topk_taux": 0.9874,
   "spans_sans_label": 1,
   "span_sans_label": "g017",
   "span_exact_taux": 1.0
  },
  "gele": {
   "phrases": 602,
   "tokens": 3141,
   "pos": 0.8625,
   "f1_syntagmes": 0.7882,
   "tete": 0.9025,
   "cibles_attachement": 239,
   "labels_attachement": 234,
   "exact": 234,
   "exact_taux": 0.9791,
   "topk": 232,
   "topk_taux": 0.9707,
   "spans_sans_label": 1,
   "span_sans_label": "g017",
   "span_exact_taux": 1.0
  }
 },
 "instantane_depasse": {
  "pos": [
   0.8496,
   0.85,
   0.8575
  ],

… [1723 caractères tronqués]
  ```

- **bash** `{"command": "echo \"=== k3 md ===\"; sed -n '1,80p' reports/rapport-passe-k3-disque.md; echo \"=== verif-cloture-1116 registre ===\"; cat work/portes/verif-cloture-1116/registre.txt 2>/dev/null", "description": "Read modern pass report and verification registry"}`

  ```
=== k3 md ===
# Où passe le temps d'une passe Kimi-K3 : le disque, et rien d'autre

> Mesuré le 07/10. Répond à la question laissée ouverte par `REPRISE.md`, qui
> demandait explicitement de la trancher **en premier** :
>
> *« la passe complète coûte 2,95 s par couple (couche, jeton) contre 0,75 s à
> chaud — quatre fois plus — et réduire de 25 % les experts lus ne change rien.
> Hypothèse non mesurée : la dispersion (~144 lectures par couple × ~10 ms de
> déplacement). Le pas pour trancher : `majflt` et le temps d'attente disque sur
> une passe complète. »*

La réponse est **le disque**, et elle est exacte à 0,1 % près. La sonde est
`tools/sonde-passe-k3.sh`, le relevé brut `/tmp/sonde_k3.csv` (793 échantillons,
2 s), la sortie moteur `/tmp/sonde_k3_moteur.log`.

---

## 1. Le montage

`DRAVE_K3_PASSE=93` sur `Kimi-K3-UD-Q4_K_XL` — **1,4 To, 32 shards**, quatre
jetons (les identifiants de la référence `[3638, 275, 1309, 3140]`), soit
**372 couples (couche, jeton)**. Une seule couche en mémoire à la fois.

**Où est le modèle, et c'est le fait qui commande tout le reste** :

```
sda              10,9T    1 disk     (ROTA=1 : disque DUR)
└─sda2           10,9T    1 part  →  /dev/mapp
… [2348 caractères tronqués]
  ```

- **bash** `{"command": "git diff tools/chantier/plan.json | head -60; echo \"=== plan.json ===\"; python3 -c \"\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nprint(json.dumps(d, ensure_ascii=False, indent=1)[:3000])\n\"", "description": "Inspect modified chantier plan"}`

  ```
diff --git a/tools/chantier/plan.json b/tools/chantier/plan.json
index 297606eb..be82fe39 100644
--- a/tools/chantier/plan.json
+++ b/tools/chantier/plan.json
@@ -924,6 +924,53 @@
      "attendu": "FICHE-OK"
     }
    ]
+  },
+  {
+   "id": "Z1",
+   "jour": 22,
+   "titre": "L'intégration continue — le workflow",
+   "mandat": "Tâche Z1 (exploitable, la protection) : l'**intégration continue** — un `.github/workflows/ci.yml` : la matrice **Python 3.10 / 3.13**, `pip install -e .`, `python3 tools/tests/test_produit.py`, `python3 tools/tests/test_tagger_api.py`, `bash tools/porte-produit.sh`, `python3 tools/tests/test_schema_produit.py` ; le **contrôle négatif** : un test qui casse doit faire échouer le job (le prouver en local) ; la doc. Fiche `reports/rapport-ci.md` + JSON. Si l'environnement n'a pas `act`, prouve au moins que le YAML est valide (un parseur) et que les commandes qu'il lance passent en local.",
+   "budget_min": 90,
+   "acceptation": [
+    {
+     "commande": "test -f .github/workflows/ci.yml && echo CI-OK",
+     "attendu": "CI-OK"
+    },
+    {
+     "commande": "test -f reports/rapport-ci.md && echo FICHE-OK",
+     "attendu": "FICHE-OK"
+    }
+   ]
+  },
+
… [4546 caractères tronqués]
  ```

- **bash** `{"command": "echo \"=== session rapport head ===\"; sed -n '1,60p' journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/rapport.md; echo \"=== grep Z2 in digest lines 400-470 ===\"; sed -n '400,470p' journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/digest.md", "description": "R … [42 caractères tronqués]`

  ```
=== session rapport head ===
# Session session- — CI GitHub Actions matrice tests

> **Journaux :** [le jour](../../2026-11-16/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-b9138a2a-648e-490d-a349-124ac1aa1ef0` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-16 03:27 |
| Durée | 0.7 h |
| Tours | 1 |
| Messages | 186 |
| Appels d'outils | 239 |
| Fichiers touchés | 13 |
| Commandes | 144 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche Z1 (exploitable, la protection) : l'**intégration continue** — un `.github/workflows/ci.yml` : la matrice **Python 3.10 / 3.13**, `pip install -e .`, `python3 tools/tests/test_produit.py`, `python3 tools/tests/test_tagger_api.py`, `bash tools/porte-produit.sh`, `python3 tools/tests/test_schema_produit.py` ; le **contrôle négatif** : un test qui casse doit faire échouer le job (le prouver en  … [191 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche Z1 (exploitable, la protection) : l'**intégration continue** — un `.github
… [5427 caractères tronqués]
  ```

- **bash** `{"command": "git show 3c10e3ee -- docs/pilotage/references-non-regression.md | sed -n '1,120p'", "description": "See how prior pass updated the reference doc"}`

  ```
commit 3c10e3ee78a1c1593aecbbbd6bde8085ab8ef142
Author: Stéphane <stephane@localhost>
Date:   Mon Nov 16 03:12:25 2026 -0500

    V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON

diff --git a/docs/pilotage/references-non-regression.md b/docs/pilotage/references-non-regression.md
index f8462718..901c2e66 100644
--- a/docs/pilotage/references-non-regression.md
+++ b/docs/pilotage/references-non-regression.md
@@ -1,5 +1,11 @@
 # Références de non-régression
 
+> **Passe — 2026-11-16 00 h 45 → 03 h 01 :** **86 portes, 82 vertes, 4 rouges** — `indice` et
+> `melange` structurelles ; `produit` (V1 inachevée) et `sessions` (heartbeat) de circonstance.
+> Journaux `work/portes/roue-1116/`. **Vérification ciblée (V3)** : `sessions` **0** et `produit`
+> **0** (`--strict` 5 tests, exemples **27/27**, autotest **183/183**) ; journaux
+> `work/portes/verif-cloture-1116/`. Après : **84 vertes, 2 rouges structurelles**.
+
 > **Passe — 2026-11-15 09 h 53 → 12 h 15 :** **85 portes, 81 vertes, 4 rouges** — `indice` et
 > `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prec
… [104 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"PASSE 1611\\|passe du 16/11\" docs/pilotage/references-non-regression.md || echo \"absent (attendu)\"; echo \"---registre count---\"; awk 'END{print NR}' work/portes/passe-1611/registre.txt 2>/dev/null; echo \"---rouges---\"; awk '$2 != 0' work/portes/passe-1611/registre.txt 2 … [72 caractères tronqués]`

  ```
absent (attendu)
---registre count---
---rouges---
[exit code: 2]
  ```

- **bash** `{"command": "ls -la work/portes/passe-1611/ 2>/dev/null | head; echo \"---stdout size---\"; wc -l work/portes/passe-1611/passe-1611.log 2>/dev/null; echo \"---registre---\"; test -f work/portes/passe-1611/registre.txt && awk 'END{print NR}' work/portes/passe-1611/registre.txt || echo \"pas encore\"" … [49 caractères tronqués]`

  ```
total 8
drwxr-xr-x. 1 stephane stephane  82 16 nov 04:12 .
drwxr-xr-x. 1 stephane stephane 658 16 nov 04:12 ..
-rw-r--r--. 1 stephane stephane  99 16 nov 04:12 passe-1611.log
-rw-r--r--. 1 stephane stephane  86 16 nov 04:12 porte-adaptateur-sortie.log
---stdout size---
2 work/portes/passe-1611/passe-1611.log
---registre---
pas encore
  ```

- **bash** `{"command": "echo \"=== indice (roue-1116) ===\"; tail -20 work/portes/roue-1116/porte-indice.log; echo; echo \"=== melange (roue-1116) ===\"; tail -20 work/portes/roue-1116/porte-melange.log; echo; echo \"=== produit (roue-1116) ===\"; tail -12 work/portes/roue-1116/porte-produit.log; echo; echo \" … [137 caractères tronqués]`

  ```
=== indice (roue-1116) ===
  A : Answer: ZQ-447
  B : Answer: 12345
  ✅ les deux invites diffèrent bien par l'aiguille seule
=== 2. indice EXTÉRIEUR : l'état de la question de B (pas dans le magasin de A) ===
    capture d'état    : position(s) [1439] écrite(s) dans /tmp/tmp.3sI30HizL0/etatB.*
    capture d'état    : position(s) [1469] écrite(s) dans /tmp/tmp.3sI30HizL0/etatA.*
=== 3. la mémoire interroge A, avec puis sans l'indice extérieur ===
  témoin   capture d'état    : position(s) [1440] écrite(s) dans /tmp/tmp.3sI30HizL0/etatC.*
  écho     indice SÉMANTIQUE : l'état de la question, position 1469, aiguille en 669 :
  écho       épisode rendu : 1469 · recouvrement 64/64 · distance à l'aiguille : 800 jetons
  écho       hasard        : 370 jetons en moyenne sur 1470 épisodes
  écho       ⇒ la mémoire n'a PAS retrouvé l'aiguille : un indice qui ne ressemble pas au contenu cherché ne le retrouve pas. C'est une limite du rappel par le contenu — il n'est pas sémantique —, et elle est mesurée, pas supposée.
  écho   
  extérieur   indice SÉMANTIQUE : EXTÉRIEUR (/tmp/tmp.3sI30HizL0/etatB.1439, 896 valeurs) — il n'est PAS dans le magasin, aiguille en 669 :
  extérieur     épisode ren
… [2280 caractères tronqués]
  ```

- **bash** `{"command": "test -f work/portes/passe-1611/registre.txt && { echo \"portes enregistrées: $(awk 'END{print NR}' work/portes/passe-1611/registre.txt)\"; awk '$2 != 0' work/portes/passe-1611/registre.txt; } || echo \"registre pas encore créé\"; echo \"---dernier log---\"; ls -t work/portes/passe-1611/ … [91 caractères tronqués]`

  ```
registre pas encore créé
---dernier log---
work/portes/passe-1611/porte-adaptateur-sortie.log
  ```

- **bash** `{"command": "date; ps -o pid,ppid,etime,stat,pcpu,cmd -C bash | grep -E \"toutes|porte-\" | head; echo \"---logs mtime---\"; ls -la --time-style=+%H:%M:%S work/portes/passe-1611/*.log; echo \"---stdout---\"; cat work/portes/passe-1611/passe-1611.log", "description": "Check whether the pass process i … [9 caractères tronqués]`

  ```
lun 16 nov 2026 04:12:54 EST
1759938 1759640       00:39 Ss    0.3 bash -c mkdir -p work/portes/passe-1611 JOURNAUX=work/portes/passe-1611 bash tools/toutes-les-portes.sh > work/portes/passe-1611/passe-1611.log 2>&1 echo "EXIT=$?"
1759946 1759938       00:39 S     0.0 bash tools/toutes-les-portes.sh
1759958 1759957       00:39 S     0.0 bash tools/porte-adaptateur-sortie.sh
1760186 1759958       00:13 S     0.0 bash tools/porte-adaptateur-sortie.sh
1762054 1759640       00:00 Ss   85.7 bash -c date; ps -o pid,ppid,etime,stat,pcpu,cmd -C bash | grep -E "toutes|porte-" | head; echo "---logs mtime---"; ls -la --time-style=+%H:%M:%S work/portes/passe-1611/*.log; echo "---stdout---"; cat work/portes/passe-1611/passe-1611.log
---logs mtime---
-rw-r--r--. 1 stephane stephane 99 04:12:14 work/portes/passe-1611/passe-1611.log
-rw-r--r--. 1 stephane stephane 86 04:12:14 work/portes/passe-1611/porte-adaptateur-sortie.log
---stdout---
=== PASSE COMPLÈTE DES PORTES (86 portes, borne 1800 s) ===
    journaux : work/portes/passe-1611
  ```

- **bash** `{"command": "ls -la journal/2026-11-16/ 2>/dev/null; echo \"---README---\"; sed -n '1,80p' journal/2026-11-16/README.md 2>/dev/null; echo \"---journal index sessions---\"; ls journal/sessions | tail -10", "description": "Inspect journal day structure"}`

  ```
total 28
drwxr-xr-x. 1 stephane stephane  108 16 nov 04:11 .
drwxr-xr-x. 1 stephane stephane 1012 16 nov 00:22 ..
-rw-r--r--. 1 stephane stephane 2120 16 nov 04:11 docs.md
-rw-r--r--. 1 stephane stephane 1076 16 nov 04:11 memoire.md
-rw-r--r--. 1 stephane stephane 1879 16 nov 04:11 mesures.md
-rw-r--r--. 1 stephane stephane 1269 16 nov 04:11 modele.md
-rw-r--r--. 1 stephane stephane 1001 16 nov 04:11 moteur.md
-rw-r--r--. 1 stephane stephane 7204 16 nov 04:11 README.md
---README---
# 2026-11-16

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-16/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**8 commits** · **1 session(s)** · **5 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 2 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 3 | [mesures.md](mesures.md) |
| modele | 1 | [modele.md](modele.md) |
| moteur | 1 | [moteur.md](moteur.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|-
… [4765 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,60p' docs/pilotage/roadmap.md; echo \"---\"; grep -n \"passe\\|portes\" docs/pilotage/en-cours.md | head -20", "description": "Inspect roadmap and state pass references"}`

  ```
# La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers

> **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
> L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
> contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
>
> **Détail et histoire** : l'ancien plan [A/B](../theorie/glossaire/entrees/a-b.md) est archivé dans
> [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
> [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
> dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
> [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).

## Comment lire cette roadmap

- **Les états** : ✅ mesuré et écrit · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
- **Le carpe diem** : pas d'échéance. Un chantier est **[fait](../theorie/glossaire/entrees
… [14959 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/revue_documentation.py", "description": "Read documentation review checks"}`

  ```
#!/usr/bin/env python3
"""revue_documentation.py — LA REVUE DE FIN DE SOUS-CHANTIER (AGENTS.md §4).

Ce qu'elle vérifie, et qu'il faut corriger AVANT le commit de clôture :
  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
     ment pas sur la cible ; les sources externes sont citées ;
  4. fraîcheur  : en-cours.md date du dernier commit, ET aucun fait n'a été commité après
     le dernier état (comparaison de commits, pas de dates : voir verifie_etat_a_jour.py) ;
  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
  6. vocabulaire : « jeton » ne désigne **jamais** la représentation sémantique neutre (RSN) ;
  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
     ne pointe vers un fichier absent (hors gabarits `AAAA`, `<...>`, `*`).

Sortie : un rapport lisible, code 0 si tout passe, 1 sinon (u
… [4497 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,100p' tools/verifie_en_cours.py; echo \"=== taille ===\"; sed -n '1,80p' tools/taille_documents.py", "description": "Read state and size validators"}`

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
… [6102 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '160,360p' tools/revue_documentation.py", "description": "Read rest of documentation review"}`

  ```
# 1. classement : aucune donnée de résultat dans docs/
    for f in (RACINE / "docs").rglob("*"):
        if f.suffix in (".json", ".csv", ".npz", ".jsonl") and f.is_file():
            if f.name == "index.json" and f.parent.name == "glossaire":
                continue
            alertes.append(f"classement : donnée de résultat dans docs/ → {f.relative_to(RACINE)}")
    for nom in ("07-mesures-couche-commune.md", "fiche-nuit-17-10.md"):
        if not (RACINE / "reports" / nom).exists():
            alertes.append(f"classement : la fiche courante reports/{nom} manque")
    if not (RACINE / "reports/README.md").exists():
        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")

    # 5. compteurs : la page d'état est la source unique, et elle dit le disque
    portes = extrait_entier(t, r"\|\s*portes\s*\|\s*\*\*(\d+)\*\*")
    chapitres = extrait_entier(t, r"\|\s*chapitres de la synthèse\s*\|\s*\*\*(\d+)\*\*")
    documents = extrait_entier(t, r"\|\s*documents de[^|]*\|\s*\*\*(\d+)\*\*")
    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
    for nom, valeur, disque in (
        ("portes", portes, comp
… [8348 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/porte-tableaux.sh; echo \"=== tableaux tool ===\"; ls tools | grep -i tableau", "description": "Read tableaux gate"}`

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
… [6860 caractères tronqués]
  ```

- **bash** `{"command": "echo \"rapports md: $(ls reports/*.md | wc -l)\"; echo \"rapports json: $(ls reports/*.json | wc -l)\"; echo \"portes: $(ls tools/porte-*.sh | wc -l)\"; echo \"docs vivants: $(python3 -c \"\nimport sys; sys.path.insert(0,'tools')\nimport revue_documentation as r\nprint(len(r.docs_vivant … [139 caractères tronqués]`

  ```
rapports md: 772
rapports json: 867
portes: 86
docs vivants: 126
---commit Z1 stat---
19992f2f Z1 — L'INTÉGRATION CONTINUE : MATRICE 3.10/3.13, 10/10 ÉTAPES VERTES (ARCHIVE SANS SOUS-MODULE, COPIE DE SECOURS S) ; PORTE 183/183 ; TEST CASSÉ → 1, JOB ARRÊTÉ ; act ABSENT, YAML PARSÉ
 .github/ci/structures/README.md                    |   30 +
 .github/ci/structures/donnees/gold-analyseur.json  | 1158 ++++++
 .github/ci/structures/generateur.py                |  657 ++++
 .github/workflows/ci.yml                           |   74 +
 docs/README.md                                     |    3 +-
 docs/pilotage/en-cours.md                          |    6 +-
 docs/pilotage/roadmap.md                           |   11 +-
 docs/produit/README.md                             |   12 +
 docs/produit/ci.md                                 |  100 +
 journal/2026-11-16/README.md                       |   23 +-
 journal/2026-11-16/docs.md                         |    2 +-
 journal/2026-11-16/memoire.md                      |    2 +-
 journal/2026-11-16/mesures.md                      |    2 +-
 journal/2026-11-16/modele.md                       |   25 +
 journal/2026-11-16/moteur.md                     
… [1010 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-11", "wait": true, "timeout_ms": 600000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "date; echo \"portes enregistrées: $(awk 'END{print NR}' work/portes/passe-1611/registre.txt 2>/dev/null || echo 0)\"; echo \"---rouges (brut)---\"; awk '$2 != 0' work/portes/passe-1611/registre.txt 2>/dev/null; echo \"---derniers logs---\"; ls -t work/portes/passe-1611/porte-*.log 2>/de … [67 caractères tronqués]`

  ```
lun 16 nov 2026 04:23:20 EST
portes enregistrées: 15
---rouges (brut)---
---derniers logs---
work/portes/passe-1611/porte-consolidation.log
work/portes/passe-1611/porte-cic.log
  ```

- **job_output** `{"job_id": "bash-11", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "date; echo \"portes enregistrées: $(awk 'END{print NR}' work/portes/passe-1611/registre.txt 2>/dev/null || echo 0)\"; echo \"---rouges (brut)---\"; awk '$2 != 0' work/portes/passe-1611/registre.txt 2>/dev/null; echo \"---derniers logs---\"; ls -t work/portes/passe-1611/porte-*.log 2>/de … [56 caractères tronqués]`

  ```
lun 16 nov 2026 04:33:27 EST
portes enregistrées: 23
---rouges (brut)---
---derniers logs---
work/portes/passe-1611/porte-episodique.log
work/portes/passe-1611/porte-echange-experts.log
  ```

- **job_output** `{"job_id": "bash-11", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "date; echo \"portes enregistrées: $(awk 'END{print NR}' work/portes/passe-1611/registre.txt 2>/dev/null || echo 0)\"; echo \"---rouges (brut)---\"; awk '$2 != 0' work/portes/passe-1611/registre.txt 2>/dev/null; echo \"---derniers logs---\"; ls -t work/portes/passe-1611/porte-*.log 2>/de … [56 caractères tronqués]`

  ```
lun 16 nov 2026 04:43:32 EST
portes enregistrées: 28
---rouges (brut)---
---derniers logs---
work/portes/passe-1611/porte-greffe.log
work/portes/passe-1611/porte-gain.log
  ```

- **job_output** `{"job_id": "bash-11", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "date; echo \"portes enregistrées: $(awk 'END{print NR}' work/portes/passe-1611/registre.txt 2>/dev/null || echo 0)\"; echo \"---rouges (brut)---\"; awk '$2 != 0' work/portes/passe-1611/registre.txt 2>/dev/null; echo \"---derniers logs---\"; ls -t work/portes/passe-1611/porte-*.log 2>/de … [56 caractères tronqués]`

  ```
lun 16 nov 2026 04:53:37 EST
portes enregistrées: 29
---rouges (brut)---
---derniers logs---
work/portes/passe-1611/porte-harnais-invariants.log
work/portes/passe-1611/porte-greffe.log
  ```

- **job_output** `{"job_id": "bash-11", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "date; echo \"portes enregistrées: $(awk 'END{print NR}' work/portes/passe-1611/registre.txt 2>/dev/null || echo 0)\"; echo \"---rouges (brut)---\"; awk '$2 != 0' work/portes/passe-1611/registre.txt 2>/dev/null; echo \"---derniers logs---\"; ls -t work/portes/passe-1611/porte-*.log 2>/de … [56 caractères tronqués]`

  ```
lun 16 nov 2026 05:03:41 EST
portes enregistrées: 30
---rouges (brut)---
---derniers logs---
work/portes/passe-1611/porte-homeostasie.log
work/portes/passe-1611/porte-harnais-invariants.log
  ```

- **job_output** `{"job_id": "bash-11", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "date; echo \"portes enregistrées: $(awk 'END{print NR}' work/portes/passe-1611/registre.txt 2>/dev/null || echo 0)\"; echo \"---rouges (brut)---\"; awk '$2 != 0' work/portes/passe-1611/registre.txt 2>/dev/null; echo \"---derniers logs---\"; ls -t work/portes/passe-1611/porte-*.log 2>/de … [56 caractères tronqués]`

  ```
lun 16 nov 2026 05:13:46 EST
portes enregistrées: 32
---rouges (brut)---
---derniers logs---
work/portes/passe-1611/porte-indice.log
work/portes/passe-1611/porte-horloge.log
  ```

- **job_output** `{"job_id": "bash-11", "timeout_ms": 600000, "wait": true}`
