# Session DSH — relecture

- identifiant : `session-2064d0cb-d031-4316-9674-54d67e6b3ab6`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 02:34:03
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche C3 : la coordination R — propose et mesure l'extension du gold réel (le « gold 200+ » des fiches R) : prends 50 phrases **réelles** (hand + reel) que l'heuristique rate, écris la fiche `reports/rapport-gold-reel-50.md` + JSON (les erreurs d'attachement par type, les candidats à annoter), sans modifier le gold (S/D territory : le gold est à S).

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

I'll start by understanding the repository structure and the context around the "gold réel" and the R fiches.

- **bash** `{"command": "pwd && ls -la", "description": "List repository root"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198 15 nov 02:34 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 76690 15 nov 02:30 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [971 caractères tronqués]
  ```

- **bash** `{"command": "find reports -maxdepth 2 -type f | sort | head -100", "description": "List report files"}`

  ```
reports/07-mesures-couche-commune.md
reports/07/p10.md
reports/07/p1.md
reports/07/p2.md
reports/07/p3.md
reports/07/p4.md
reports/07/p5.md
reports/07/p6.md
reports/07/p7.md
reports/07/p8.md
reports/07/p9.md
reports/a26-bilan.json
reports/a26-lot-disque.json
reports/a80-audit-final.json
reports/a80-indice-qualifie.json
reports/a80-melange-qualifie.json
reports/a80-pannes-ppl.json
reports/a80-porte-adaptateur.json
reports/a80-porte-budget.json
reports/a80-porte-bus.json
reports/a80-porte-bus-socket.json
reports/a80-porte-c4-retard.json
reports/a80-porte-consolidation.json
reports/a80-porte-cycle-c2.json
reports/a80-porte-delais.json
reports/a80-porte-flux.json
reports/a80-porte-fusion.json
reports/a80-porte-gain.json
reports/a80-porte-pont.json
reports/a80-porte-profondeur.json
reports/a80-porte-reflexe.json
reports/a80-porte-reparti.json
reports/a80-portes-ppl.json
reports/a80-porte-topologie.json
reports/a80-porte-trace.json
reports/a83a-coupe.json
reports/a83a-flux.json
reports/a83a-pont.json
reports/a83b-decision.json
reports/a83b-lot.json
reports/a83b-regimes.json
reports/a83c-ctx.json
reports/a83c-lot.json
reports/a83-defaut.json
reports/a83d-lot-threads.json
reports/aiguille-
… [3063 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/pilotage/ && echo \"---\" && ls docs/methode/", "description": "List pilotage and methode docs"}`

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
semaine-autonome.md
utilisation.md
---
chantier-autonome.md
contexte.md
continuite.md
echantillonnage-vdc.md
illustrations.md
miroir.md
mission.md
modularisation.md
organisation-du-depot.md
panini-nipada.md
portes.md
rangement.md
relations-humaines.md
ressources.md
resultats.md
  ```

- **bash** `{"command": "cat docs/pilotage/programme-r.md", "description": "Read programme R"}`

  ```
# Le programme R — le lecteur, de la surface à la réponse

> **Charte de programme.** Ce document dit ce qu'est **R**, pourquoi il existe, ses six phases, ses
> lois, ce qui tient et ce qui ne tient pas, ses dépendances et sa prochaine action. **État au
> 2026-11-01.** Les chiffres sont dans les fiches [`reports/`](../../reports/) ; l'ordre et les
> états dans [`roadmap.md`](roadmap.md) ; la théorie de la lecture dans
> [`lecture-rapide.md`](../theorie/lecture-rapide.md). Cette page ne remplace ni les unes ni les
> autres : elle dit **ce qu'on peut affirmer** et **ce qui manque**.
>
> **Ce que R n'est pas.** Ni la ligne **N** (le natif), ni la ligne **B** (le sens), ni **A** (le
> moteur). R n'est pas un modèle ni un benchmark : c'est le **lecteur** — la cible mesurable qui
> donne un sens aux trois autres. Un modèle qui a une bonne perplexité mais qui ne sait pas
> répondre à une question sur un document n'a pas encore de lecteur.

## 1. Qu'est-ce que le programme R ?

Drave a quatre lignes de travail : **A** (le moteur : bus, blocs, DRVM), **B** (l'intelligence :
sémantique, codec, jeux), **N** (le natif : `drave-n0`, la RSN, la pensée) et **R** (le lecteur).
Les trois premières 
… [20396 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i -E 'gold|r[0-9]|coord|attache' ", "description": "Find gold/R related reports"}`

  ```
n2-r11.json
n2-r12-2048.json
pensee-attachement-cible.json
pensee-attachement.json
pensee-attachement-parfait.json
pensee-attachement-v2.json
pensee-attachement-v3.json
pensee-audit-attachement.json
pensee-audit-r1r3.json
pensee-echecs-attachement.json
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
pensee-pos-r4-integration.json
pensee-pos-r4.json
pensee-r035.json
pensee-r1r3.json
pensee-r264-elision.json
pont-longueur2-3b.json
r01-graphe-document.json
r02-banc-lecture.json
r03-banc-durci-extractif.json
r03-banc-durci-modele.json
r03-banc-extractif.json
r03-banc-modele.json
r03-lecteur-modele-couverture.json
r03-lecteur-modele.json
r03-pilote-modele.json
r04-tete-survol.json
r04-tete-survol-v2.json
r04-tete-survol-v3.json
r04-tete-surv
… [2707 caractères tronqués]
  ```

- **bash** `{"command": "grep -ril \"gold\" --include=*.md --include=*.json --include=*.py . | head -60", "description": "Find files mentioning gold"}`

  ```
./reports/traduction-litteraire-3b.json
./reports/traduction-litteraire-7b.json
./reports/traduction-24langues-A.json
./reports/traduction-24langues-3b-A.json
./reports/multilingue.json
./reports/rapport-native-test.md
./reports/rapport-r02-controleur.md
./reports/rapport-r03-lecteur-modele.md
./reports/rapport-r03-banc-complet.md
./reports/rapport-r03-banc-durci.md
./reports/rapport-r41-bloc-tableaux.md
./reports/rapport-r04-tete-survol.md
./reports/rapport-r05-balayage.md
./reports/rapport-corpus-gele.md
./reports/rapport-r06-declencheur.md
./reports/rapport-r06-cascade-confiance.md
./reports/rapport-r06-calibration.md
./reports/rapport-r06-publication.md
./reports/rapport-r07-routeur.md
./reports/rapport-bloc-linguistique.md
./reports/pensee-gold-linguistique.json
./reports/rapport-pensee-gold-linguistique.md
./reports/rapport-pensee-operateurs.md
./reports/rapport-pensee-porte.md
./reports/rapport-pensee-porte-apprise.md
./reports/rapport-pensee-courbe.md
./reports/rapport-pensee-seule.md
./reports/rapport-pensee-sto-seule.md
./reports/rapport-pensee-ferme.md
./reports/rapport-pensee-minute.md
./reports/rapport-pensee-minute-apprise.md
./reports/rapport-pensee-minute-seule.md
.
… [1037 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-coordination-r.md", "description": "Read coordination R report"}`

  ```
# R — le tagger POS sur le gold 612 : **+8,49 pts**, la règle dit **intégrer**

> **Ligne de roadmap** : **R0.7** (le bloc linguistique) · **Date** : 2026-11-13 · **HEAD mesuré** :
> `ced21933` · **Verdict** : le tagger POS par **API DeepSeek** mesure **0,9475** (**3012/3179**)
> sur le gold **612**, contre **0,8625** (**2742/3179**) pour l'heuristique du HEAD : **+8,49 pts**,
> IC95 bootstrap par phrase **[+7,23 ; +9,74]**, McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. La règle
> de décision (**≥ +5 pts → intégrer**) donne : **intégrer via l'API**, jamais le 7B local
> (règle 11). La prémisse « clé absente » est **fausse** : la clé est dans
> `~/.config/drave/deepseek.key` (0600) et l'API répond **200** ; c'est `DEEPSEEK_API_KEY` qui
> manque. Coût mesuré : **1 218 appels, 358 962 tokens, 21 min**, **~0,04 $** hors pointe.

**En trois lignes.** (1) La mesure est **réelle**, faite le 2026-11-13 avec un **cache neuf** :
`deepseek-chat` est servi par `deepseek-flash` (DeepSeek-V4.1-Flash-1017), 1 218 appels,
358 962 tokens, 20 min 59 s, **0 refus POS**. (2) La baseline publiée **0,8500** est **datée** :
elle reproduit exactement au commit `97256b8f`, mais trois commits POS du 2026-11-06 l
… [21303 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-pensee-seuils-gold-reel.md", "description": "Read seuils gold reel report"}`

  ```
# B13 — les seuils du gold réel : 0,90 / 0,45 / 0,55 / 0,50, le verdict passe à true

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ✅ **le contrat du gold réel
> est fixé** — le gold 180 (hand+synth) et le gold réel 432 n'ont pas le même plancher. Le banc
> applique désormais **0,94 / 0,60 / 0,75 / 0,60** sur le gold 180 et **0,90 / 0,45 / 0,55 / 0,50**
> sur le gold réel 432. Le gold réel **passe** avec ces seuils.

## 1. Le problème

Le banc `qualifier_cascade.py` avait des seuils **uniques** (0,94 / 0,60 / 0,75 / 0,60), calibrés
sur le gold 180. Sur le gold réel 432, la cascade fait **0,9065 / 0,4598 / 0,5633 / 0,5165** :
`pos_all`, `syntagme_exact_all`, `syntagme_tete_all` et `fraction` échouaient **par construction**,
pas par régression. Un seuil qui n'a jamais été atteignable sur le corpus de test n'est pas un
seuil : c'est un vœu.

## 2. Le contrat

| gold | POS | syntagmes | tête | fraction |
|---|---:|---:|---:|---:|
| **gold 180** (hand+synth) | 0,94 | 0,60 | 0,75 | 0,60 |
| **gold réel 432** | 0,90 | 0,45 | 0,55 | 0,50 |

Les seuils du gold réel sont **figés une fois**, pas ajustés à chaque passe : c'est le plancher
mesuré du corpus réel, pas
… [1449 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-pensee-gold-200.md", "description": "Read gold 200 report"}`

  ```
# B13 — le gold à 200 phrases réelles : POS 0,7738

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **88/88 portes** : le gold réel passe de **180 à 200 phrases** (r181–r200, 10 françaises et 10
> anglaises, écrites à la main). Le POS global gagne **+0,0023** (0,7715 → **0,7738**), sur
> **1 782 tokens** : la cible « 200 phrases réelles » est **atteinte**.
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-gold-200.json`](pensee-gold-200.json).

## 1. Le gold à 200 réels

| mesure | 180 réels (T?) | **200 réels** | delta |
|---|---:|---:|---:|
| tokens | 1 698 | **1 782** | +84 |
| POS (all) | 0,7715 | **0,7738** | +0,0023 |
| syntagme F1 | 0,1988 | 0,1941 | −0,0047 |
| pragmatique (acte) | 1,0 | 1,0 | 0 |
| tête (F1) | 0,4359 | 0,4274 | −0,0085 |

**Ce que ça dit** :

- **La cible est atteinte** : 200 phrases réelles (180 + 20), la ligne B13 tient sa promesse
  « 200 réels ».
- **Le POS est stable** (+0,0023) : les 20 nouvelles phrases sont du même registre (SVQ simple,
  GN/G
… [1576 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"gold 200\\|gold réel\\|gold reel\\|200+\" docs/ journal/ reports/*.md 2>/dev/null | head -50", "description": "Search for gold 200 references"}`

  ```
docs/pilotage/plan-travail.md:39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **166/166** (6 S fixés ; T132/T133 2/5), gold **432**, 116 liens ; **gold neuronal** (POS **0,9415** / syntagmes **0,7539** / acte **1,0**) ; **DRVM/native** règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusion par sous-type : le double sens 0,9884 (+0,0208) ; variance du sous-type : 0,9838 ; tirages : 0,9838 ×3 (déterministe sur ces invites) ; attachement : top1 0,3431, exact 0,0042 ; cibles : 1863 segments, 1624 sans cible (87,2 %), couverture réelle 0,1283 ; cibles 500 : 294 GN / 206 GV ; relation GN → GV : 221/637 ; rôles par position : 301/322, relation 0,8195 (522/637) surévaluée ; correctif `par` → agent (partiel : le générateur S garde `moyen`) ; sans `par` : le chunker 3/3, le générateur S ignore ; cible par proximité : exact 0,0042 → 0,0544 ; candidats verbes : top-k 0,4686, tête 0,7655 ; échecs qualifiés : 127 = 94 span + 33 cible** (négation/modalité sous l'heuristiq
… [21584 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"Tâche C3\\|Tâche C\\|C3\\b\" docs/ journal/ reports/ tools/ 2>/dev/null | head -50", "description": "Search for task C3"}`

  ```
XU1KjqNR0u9tmc3Qfak5EsxibAYMGJs/e66XNqEfcvfl2dCiKkEvrge4ExBB/XQ0zHXAxi/O4MtG79f1LKdDeURS2ddryT3/iQKcKdN/DhzxoszEARC+TgiEuMCEifhIkwqtDodC4rpIGnZPOT+iAmUojAUA/LDcu8A8GMEZt8BeRZRAy+bs/oubhElCNQ90FvOYADy7l4VDTaRE28es/5WoD+I0QkYn4ohFoF8o2qtO3YCpdNZePLkogV5NssPGBMq/X2RH0hKGUgr/7Q/8Aw4hOJMclIYYwK7cLtNzpc0PW4w3whJRHQYIwmYOtEpU80UC1++jBdhscajFiODKgCZ8U8YLW3/bjljlp8U845/1jsS/KDcPWyzGzJpF6D8K2SbQPPgHIo72VwG0UA1K7nzHqQTXJQrcHU6LkwwjK2ar0UYi/KfG0wv7UkWKC8RgU/Fbn2pJbupeljy0/un/J5//0J5xIT0/oq2uKbe5krFIn7JGwxltSa1aWNa8+bt3ngTS9HCxTk4xI1DF9Rxk7TWN+2daVY9D8YkNsP1K9KYDUBOGHkohUopwZWUA2607mLzDk9QSHlN9lee4XgYKo1KRnS2yr0UYvfvKpOeplTKxe8zVGdpmafZuqRfQRFCpE4rPqvfgvMb0DE6PtodJTUZLcZmsTFkQD/b2lexPn1f5n5F8qDjZTu4sGzuLHesw3RzBOvUkaltVQxpKCxDOdysaeZq8xsnXnOw7oSh/Qf9PDANroRLFlawjBbrrddH5PxQIIaiGAhFSt1Nex3O5oO33/Y4G/6j/nRyWuIHE5IcGAOMXbjWbKIb4kpz1DPDWDvUrEaMJuKTEMvjJFSH+8z94hdPX5tmxLLpYOyF1SEEwn++JQ2Gw1JOJFMTdeB0sVhMkfRbITO6et1EB2/xC+4M9+tbh7gxTvzSo+XyKX+8QFQayz82acf6Vn0W8kJvvt5hLfn9/dGGyNytR56ydYosapto2+VtLnLkG120Jgq4uhCSfDASnsEj+llHmLt5u8iWcxorkeFv5W/7CE5kCC4PhwZgIsXdtAqAp38w/IQkqDVcBeGsJeIISZEIPOXWlmJu4K8v31kbyCQmEAlxOCMbZs5lLefuJluRKpho4u7krGNPnsP4Aj4Otynz9LmMZfQl1GitZbT5m1nUusbCyffkNZkAubf8l5TD+dXmmrAjlgwsA
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests/linguistique/ && echo --- && ls tools/pensee/ | head -50", "description": "List linguistic test tools"}`

  ```
anaphore.py
classement_cible.py
classer_gv.py
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
qualifier_tagger_612.py
replis_cible.py
test_bloc_linguistique.py
---
audit.py
autotest.py
banc.py
coeur.py
courbe.py
cruches.py
csp.py
graines.py
__init__.py
jeux.py
moteur.py
operateurs.py
__pycache__
store.py
taquin.py
trace.py
  ```

- **bash** `{"command": "cat reports/rapport-pensee-attachement.md | head -160", "description": "Read attachment report"}`

  ```
# B13 — l'attachement sur le gold 432 : top1 0,3431, exact 0,0042

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **156/156 portes** : l'**attachement** (le segment → sa cible) est mesuré sur le gold 432 :
> **top1 0,3431**, **top-k 0,3264**, **exact 0,0042**, **couverture 0,6067**. La couverture est la
> première limite : **145 cibles sur 239** sont annotées, et l'attachement exact est **quasi nul**
> (1 sur 239).
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-attachement.json`](pensee-attachement.json).

## 1. Les deux mesures

| mesure | cibles | labels | top1 | top-k | exact | couverture |
|---|---:|---:|---:|---:|---:|---:|
| attachement | 239 | 145 | 82 (0,3431) | 78 (0,3264) | **1 (0,0042)** | 0,6067 |
| attachement (tête) | 145 | 145 | 81 (0,5586) | 77 (0,5310) | — | 1,0000 |

**Ce que ça dit** :

- **L'attachement exact est quasi nul** (1/239) : le bloc propose des candidats, pas la bonne
  cible — c'est le point le plus faible de la ligne L.
- **La couvertu
… [1573 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-pensee-echecs-attachement.md | head -180", "description": "Read attachment failure report"}`

  ```
# B13 — les 127 échecs qualifiés : 94 de span, 33 de cible

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **166/166 portes** : les **127 échecs** de l'attachement (avant ce round) se répartissent en
> **94 de span** (aucun segment prédit au même span) et **33 de cible** (le span est bon, la cible
> n'est pas dans les candidats) — **32** après le correctif. Le correctif testé — ajouter les GV du chunker aux GV du générateur S et
> remplir les segments d'union — ne répare **qu'un** des 33. Les 32 autres ont un GV qui couvre
> **toute la phrase** : le dernier token n'est pas le verbe (`… in the park` → `park`, pas `saw`).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-echecs-attachement.json`](pensee-echecs-attachement.json).

## 1. La répartition

| cause | nombre | part |
|---|---:|---:|
| **span faux** (aucun segment prédit au même span) | **94** | 74,0 % |
| **cible hors des candidats** (span bon) | **33** → **32** après le correctif | 26,0 % |
| **tout** | **127**
… [2193 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -30 && echo \"---BRANCH---\" && git log --oneline -8", "description": "Git status and recent log"}`

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
---BRANCH---
f926b5bc C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PROFONDEUR, 41 VERDICTS À RE-JUGER ; PORT 8765 PRIS, PARE-FEU ACTIF ; LES 11 VERDICTS COMMITTÉS (389b99f)
292c70b5 C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09
5891ef8a ÉTAT — T0 TENU : LA LIGNE FAIT RACCOURCIE
6560a0a5 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612)
2d7a7f2b 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5)
ce7241d5 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS
34c0fb0b INDEX — RÉG
… [182 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"coordination R\\|coordination-r\\|Tâche C\" docs/ reports/ journal/ tools/ 2>/dev/null | head -20", "description": "Find coordination R task definitions"}`

  ```
docs/pilotage/semaine-autonome.md
reports/rapport-coordination-r.json
reports/rapport-coordination-r.md
reports/rapport-semaine.md
reports/rapport-semaine.json
reports/rapport-bilan-chantier.json
reports/rapport-bilan-chantier.md
reports/rapport-tableau-mesures.md
reports/tableau-mesures.json
reports/rapport-cloture-chantier.md
reports/rapport-tagger-option.md
reports/INDEX.md
reports/README.md
journal/sessions/4f3e8570-3d81-41e0-a055-1002702a6959/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/session-4a28c290-9701-4d27-8aad-a9cf004c9af9/digest.md
journal/sessions/session-5e097832-2ce1-407d-bf99-228cef7efa82/digest.md
journal/sessions/session-5e097832-2ce1-407d-bf99-228cef7efa82/rapport.md
journal/sessions/session-9f876d8f-5661-44f0-b052-0770211328ec/digest.md
journal/sessions/session-11d99e1c-be38-4727-9c7a-013846234567/digest.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat ce7241d5 | head -40 && echo \"=====\" && git show --stat 6560a0a5 | head -40", "description": "Show recent commit stats"}`

  ```
commit ce7241d5cf946d86dfdcc5c6f97768b83328803a
Author: Stéphane <stephane@localhost>
Date:   Sun Nov 15 01:31:34 2026 -0500

    6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS

 docs/pilotage/en-cours.md                          |   4 +-
 docs/produit/README.md                             |  10 +
 journal/2026-11-15/README.md                       |  25 ++
 journal/README.md                                  |   2 +-
 journal/sessions/MANIFEST.md                       |   4 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 271 +++++++++++++++++++++
 .../rapport.md                                     |  98 +++++++-
 reports/INDEX.md                                   |   3 +-
 reports/README.md                                  |   2 +
 reports/pensee-base-reelle.json                    |  29 +++
 reports/rapport-base-reelle.md                     |  70 ++++++
 tools/drave.py                                     |  25 +-
 tools/tests/test_produit.py                        |  19 ++
 13 files changed, 547 insertions(+), 15 deletions(-)
=====
commit 6560a0a5330f5
… [957 caractères tronqués]
  ```

- **bash** `{"command": "ls -lt reports/ | head -40", "description": "List newest reports"}`

  ```
total 27144
-rw-r--r--. 1 stephane stephane   22126 15 nov 02:30 rapport-coordination-s-v2.json
-rw-------. 1 stephane stephane   23828 15 nov 02:30 rapport-coordination-s-v2.md
-rw-r--r--. 1 stephane stephane   21394 15 nov 02:25 README.md
-rw-r--r--. 1 stephane stephane  102003 15 nov 02:25 INDEX.md
-rw-------. 1 stephane stephane   15412 15 nov 02:12 rapport-coordination-n2-v2.md
-rw-------. 1 stephane stephane   11559 15 nov 02:12 rapport-coordination-n2-v2.json
-rw-r--r--. 1 stephane stephane    5864 15 nov 01:42 pensee-tagger-option.json
-rw-------. 1 stephane stephane   10801 15 nov 01:42 rapport-tagger-option.md
-rw-r--r--. 1 stephane stephane     660 15 nov 01:31 pensee-base-reelle.json
-rw-r--r--. 1 stephane stephane    3355 15 nov 01:31 rapport-base-reelle.md
-rw-r--r--. 1 stephane stephane    4468 14 nov 09:54 note-panini-334.md
-rw-r--r--. 1 stephane stephane   11310 14 nov 07:15 rapport-cloture-chantier.json
-rw-------. 1 stephane stephane   14878 14 nov 07:15 rapport-cloture-chantier.md
-rw-r--r--. 1 stephane stephane   40403 14 nov 06:58 tableau-mesures.json
-rw-r--r--. 1 stephane stephane   39498 14 nov 06:58 rapport-tableau-mesures.md
-rw-r--r--. 1 stephane stepha
… [1851 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/pilotage/semaine-autonome.md", "description": "Read autonomous week plan"}`

  ```
# Le chantier autonome — une semaine (7 → 14 novembre 2026)

> **Ce que ce document est.** Le **plan du chantier d'une semaine** : tous les travaux ouverts du
> dépôt et l'**intégration avec l'écosystème Panini**. Il dit **quoi**, **dans quel ordre**, **avec
> quels sous-agents**, **comment on mesure**, et **ce qui peut faire échouer**. L'état courant est
> dans [`en-cours.md`](en-cours.md) ; la théorie de la généalogie dans
> [`../theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md) ; la méthode
> Panini/Nipada dans [`../methode/panini-nipada.md`](../methode/panini-nipada.md).
> *À relire chaque matin du chantier.*
>
> **Bilan J10.1 (14/11).** Le chantier est **mesuré et écrit** ; la **clôture formelle** (tag,
> release) reste à faire (J5.2, reprise par J14.1). Les chiffres avant/après, les décisions, les
> rejets et les échecs sont dans
> [`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON ; l'état courant
> est dans [`en-cours.md`](en-cours.md).

## 1. L'objet

**Une semaine, un système utilisable, une intégration mesurée.** Le produit `drave` (CLI, contrat,
porte) est la **priorité** ; l'intégration avec Panini/Nipada est le **seco
… [20026 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/2026-11-15/ && echo \"=====\" && sed -n '1,200p' journal/2026-11-15/README.md", "description": "Read today's journal"}`

  ```
total 20
drwxr-xr-x. 1 stephane stephane   94 15 nov 02:32 .
drwxr-xr-x. 1 stephane stephane  992 15 nov 01:33 ..
-rw-r--r--. 1 stephane stephane 1246 15 nov 02:32 distribue.md
-rw-r--r--. 1 stephane stephane  905 15 nov 02:32 docs.md
-rw-r--r--. 1 stephane stephane 1886 15 nov 02:32 mesures.md
-rw-r--r--. 1 stephane stephane 1412 15 nov 02:32 portes.md
-rw-r--r--. 1 stephane stephane 2076 15 nov 02:32 README.md
=====
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**6 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 1 | [distribue.md](distribue.md) |
| docs | 1 | [docs.md](docs.md) |
| mesures | 3 | [mesures.md](mesures.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentatio
… [1239 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"C3\\|gold réel\\|gold 200\" journal/2026-11-15/ docs/pilotage/en-cours.md tools/chantier/ 2>/dev/null | head -40", "description": "Search C3 in today's journal"}`

  ```
docs/pilotage/en-cours.md:67:- **Prochaine action** : **trancher la convention d'adverbe (`g017`)** ; puis T132/T133, gold 200+.
docs/pilotage/en-cours.md:69:- **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**.
docs/pilotage/en-cours.md:118:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1–J11.4 (produit)** | **trancher `g017`** ; puis T132/T133, gold 200+ ; **B10.3 bloquée** |
docs/pilotage/en-cours.md:124:**C1** · **C2** · **C3** · **C4** · **C5** · **C6** · **C7** — hors graphe.
docs/pilotage/en-cours.md:128:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — migration `/` v7 (106/41) ; référents ; **R0.7** — split réel ; **A** — A6.2, A8.3b2.
tools/chantier/plan.json:449:   "id": "C3",
tools/chantier/plan.json:451:   "titre": "Coordination R — le gold réel étendu",
tools/chantier/plan.json:452:   "mandat": "Tâche C3 : la coordination R — propose et mesure l'extension du gold réel (le « g
… [272 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' docs/pilotage/en-cours.md", "description": "Read current state"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 02 h 32 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**

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
> le h
… [10943 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(type(p), list(p)[:10] if isinstance(p,dict) else len(p))\nPY", "description": "Inspect plan.json structure"}`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if t.get('id') in ('C1','C2','C3','C4','C5'):\n        print(json.dumps(t, ensure_ascii=False, indent=2))\n        print('-'*80)\nPY", "description": "Print C tasks definitions"}`

  ```
{
  "id": "C1",
  "jour": 15,
  "titre": "Coordination N2 — la commande validée",
  "mandat": "Tâche C1 : la coordination N2, suite de J4.1 — écris `reports/rapport-coordination-n2-v2.md` + JSON : la commande **validée** `python3 work/n2ac/eval_longueurs.py --rope --canal-dir <dir>` (le correctif mesuré 2,79), la commande à ne PAS utiliser (`--rope` seul : 40,07), le test de non-régression proposé (`porte-n2.sh` : la porte à 3,09 doit rester à 3,09), et la mise à jour de la ligne N2 de `docs/pilotage/en-cours.md`. **Ne modifie rien dans `tools/n2/` ni `work/n2ac/`.**",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f reports/rapport-coordination-n2-v2.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    }
  ]
}
--------------------------------------------------------------------------------
{
  "id": "C2",
  "jour": 15,
  "titre": "Coordination S — la page / et la v7",
  "mandat": "Tâche C2 : la coordination S, suite de J4.2 — écris `reports/rapport-coordination-s-v2.md` + JSON : l'état de la page `/` (le service de la v7), le pare-feu réseau, la commande de lancement, ce qui reste à S ; les 11 verdicts sont désormais committés (389b99f). **Ne touche pas `to
… [962 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/tests/linguistique/gold_reel.py tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold.json tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_split.py tools/tests/linguistique/qualifier_quatre_modes.py tools/tests/linguistique/gold_synthet … [80 caractères tronqués]`

  ```
1385 tools/tests/linguistique/gold_reel.py
 31004 tools/tests/linguistique/gold_reel.json
  1332 tools/tests/linguistique/gold.json
   307 tools/tests/linguistique/evaluer_gold.py
    50 tools/tests/linguistique/gold_split.py
   135 tools/tests/linguistique/qualifier_quatre_modes.py
   205 tools/tests/linguistique/gold_synthetique.py
  2906 tools/bloc_linguistique.py
 37324 total
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    print(f, type(d), len(d))\n    if isinstance(d,list):\n        print('  keys of first:', list(d[0]) if isinstance(d[0],dict) else d[ … [127 caractères tronqués]`

  ```
gold.json <class 'dict'> 3
gold_reel.json <class 'dict'> 4
gold_synthetique.json <class 'dict'> 5
  ```

- **bash** `{"command": "sed -n '1,200p' tools/tests/linguistique/evaluer_gold.py", "description": "Read evaluator"}`

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
… [8215 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '200,340p' tools/tests/linguistique/evaluer_gold.py", "description": "Read rest of evaluator"}`

  ```
"exact_any_taux_span": round(att_exact_any / max(1, att_labels), 4),
                        # exactitude sur les segments au bon span : l'attachement seul
                        "top1_taux_span": round(att_top1 / max(1, att_labels), 4),
                        "topk_taux_span": round(att_topk / max(1, att_labels), 4),
                        "topk_exact": att_topk_exact,
                        "topk_exact_taux": round(att_topk_exact / max(1, att_n), 4),
                        "topk_exact_taux_span": round(att_topk_exact / max(1, att_labels), 4),
                        "exact_taux_span": round(att_exact / max(1, att_labels), 4),
                        "verbe": {"cibles": att_v_n, "justes": att_v_ok,
                                  "taux": round(att_v_ok / max(1, att_v_n), 4)},
                        "nom": {"cibles": att_n_n, "justes": att_n_ok,
                                "taux": round(att_n_ok / max(1, att_n_n), 4)},
                        "couverture": round(att_labels / max(1, att_n), 4),
                        "par_langue": {lg: {"cibles": v["cibles"], "labels": v["labels"],
                                            "exact": v["exact"], "topk": v["topk"],
     
… [5171 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    print('===',f, list(d.keys()))\n    for k,v in d.items():\n        if k!='phrases': print('  ',k,':',repr(v)[:300])\n    print('  n  … [150 caractères tronqués]`

  ```
=== gold.json ['version', 'phrases', 'note']
   version : 1
   note : 'Gold v0, écrit à la main ; spans calculés par sous-chaîne.'
  n phrases: 20
  first: {"id": "g001", "langue": "fr", "texte": "Le chat dort.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chat", "pos": "NOUN", "debut": 3, "fin": 7}, {"texte": "dort", "pos": "VERB", "debut": 8, "fin": 12}], "segments": [{"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}, {"type": "GV", "texte": "dort", "role": "prédicat", "debut": 8, "fin": 12}], "pragma": {"acte": "assertion"}}
=== gold_reel.json ['version', 'source', 'note', 'phrases']
   version : 1
   source : 'reel'
   note : '200 phrases réelles.'
  n phrases: 432
  first: {"id": "r001", "langue": "fr", "texte": "Le chien mange une pomme.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chien", "pos": "NOUN", "debut": 3, "fin": 8}, {"texte": "mange", "pos": "VERB", "debut": 9, "fin": 14}, {"texte": "une", "pos": "DET", "debut": 15, "fin": 18}, {"texte": "pomme", "pos": "NOUN", "debut": 19, "fin": 24}], "segments": [{"type": "GN", "texte": "Le chien", "role": "agent", "debut": 0, "fin": 8}, {"type": 
… [1147 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"gold 200\" -B 12 -A 12 docs/produit/README.md", "description": "Read product README around gold 200+"}`

  ```
473-cas, pas une règle.
474-
475-**6. La langue n'est pas forcée.** `--langue` est un **indice**, limité à `fr` et `en` dans le
476-CLI ; sous le seuil de confiance, la sortie reste `und`. Il n'y a pas de `--langue-forcee`. Les
477-profils UDHR (398 langues, 0,9687) ne sont pas exposés par le CLI et ne sont pas versionnés :
478-`data/` est hors dépôt, et le corpus XML source est externe. Sans eux, la détection se rabat sur
479-les indices internes.
480-
481-**7. Pas de RSN, pas de DRVM, pas de serveur.** Le bloc a le contrat, la trace et le coût ; il
482-ne produit pas le corps de la RSN, n'est pas un port DRVM et n'expose pas d'API HTTP. La couche
483-sémantique est un **compteur d'unités**, pas une représentation.
484-
485:**8. Pas de classement appris ni de gold 200+.** L'attachement est une **heuristique de
486-proximité** avec candidats ; il n'y a pas de modèle de classement. Le gold fait 612 phrases, dont
487:160 synthétiques ; le gold 200+ réel reste à faire.
488-
489-**9. Pas de calibration des confiances.** `confiance` est **déclarée** (0,3 pour un NOUN ouvert,
490-0,92 pour un DET), pas mesurée comme une probabilité. Elle sert à trier, pas à seuiller une
491-décision auto
… [426 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-base-reelle.md && echo \"=====JSON=====\" && cat reports/pensee-base-reelle.json", "description": "Read base reelle report"}`

  ```
# B13 — la base honnête : `evaluer --reel`, 452 phrases réelles, et ce que le synthétique cachait

> **Ligne de roadmap** : **B13** (le produit) · **Décision** : 6A · **Date** : 2026-11-15 ·
> **Verdict** : ✅ **la CLI sait maintenant mesurer le réel** (`evaluer --reel`) et **publie la
> base réelle à côté du global** dans la sortie par défaut. Ce que ça révèle : sur les **452
> phrases réelles** (main + corpus, sans les 160 synthétiques), le **POS monte** (88,91 % contre
> 86,25 %) et la **F1 est la même** (79,06 % contre 79,02 %) — le synthétique n'aidait donc **pas**
> le POS, contrairement à ce qu'on pouvait craindre, mais il **tirait la moyenne vers le bas**.
>
> **Dispositif** : [`drave.py`](../tools/drave.py) (`--reel`, la ligne `BASE RÉELLE`),
> [`test_produit.py`](../tools/tests/test_produit.py) (2 tests) ; JSON
> [`pensee-base-reelle.json`](pensee-base-reelle.json).

## 1. Les deux bases

| mesure | vivant 612 | **réel 452** |
|---|---:|---:|
| POS | 86,25 % | **88,91 %** (fermé 92,94 / ouvert 84,66) |
| F1 syntagmes | 79,02 % | **79,06 %** |
| tête F1 | 90,29 % | 89,90 % |
| attachement exact | 99,58 % | **99,46 %** |
| couverture | 99,58 % | 99,46 % |
| cibles | 239 | 18
… [2721 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"attachement\\|cible\\|attachement\" tools/bloc_linguistique.py | head -60", "description": "Find attachment code in bloc"}`

  ```
997:    def _cibles_s(self, texte: str) -> dict:
998:        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
1001:        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
1009:            return {(s.debut, s.fin, s.type): (s.cible_gp or s.cible_nom or s.cible_verbe)
1015:    def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
1028:    def _cible_rel_sujet(texte: str, segment: dict, tous: list[dict]) -> str | None:
1031:        Le gold : « elle qui commence nage » → REL « qui commence » a pour cible `elle`,
1070:    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict]) -> str | None:
1085:    def _repli_verbe_propre(texte: str, segment: dict, cible: str | None):
1087:        if cible or segment.get("type") not in ("SUB", "REL"):
1088:            return cible
1089:        return Heuristique._verbe_dans(texte, segment["debut"], segment["fin"]) or cible
1092:    def _cible_hors_span(texte: str, segment: dict, gvs: list[dict], cible: str | None):
1098:        if not cible or segment.get("type") not in ("GP", "SUB"):
1099:            return cible
1101:        if _normali
… [3510 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Heuristique\\|class Annotation\\|class Etiquette\\|def analyser\\|class NeuronalLLM\\|class Cascade\\|class Parallele\" tools/bloc_linguistique.py | head -30", "description": "Find classes in bloc"}`

  ```
68:class Etiquette:
98:class Annotation:
141:    def analyser(self, texte: str, langue: str | None = None,
796:class Heuristique:
1455:    def analyser(self, texte: str, langue: str | None = None,
1845:    def analyser(self, texte: str, langue: str | None = None,
1889:class NeuronalLLM:
1916:    def analyser(self, texte: str, langue: str | None = None,
1968:class NeuronalLLMPOS:
2026:    def analyser(self, texte: str, langue: str | None = None,
2099:class NeuronalLLMChunks:
2160:    def analyser(self, texte: str, langue: str | None = None,
2234:class NeuronalLLMCompose:
2252:    def analyser(self, texte: str, langue: str | None = None,
2284:class NeuronalLLMPragmatique:
2330:    def analyser(self, texte: str, langue: str | None = None,
2639:class Parallele:
2656:    def analyser(self, texte: str, langue: str | None = None,
2664:class Cascade:
2684:    def analyser(self, texte: str, langue: str | None = None,
  ```

- **bash** `{"command": "grep -n \"def evaluer\\|BASE RÉELLE\\|def cmd_evaluer\\|--reel\" tools/drave.py | head -30", "description": "Find evaluer in CLI"}`

  ```
467:        (f"BASE RÉELLE (hand + reel, {rapport['reel']['phrases']} phrases)  "
470:         if rapport.get("reel") else f"BASE RÉELLE — (déjà la base, ou gold gelé)"),
530:def cmd_evaluer(args: argparse.Namespace) -> int:
822:    evaluer.add_argument("--reel", action="store_true",
  ```

- **bash** `{"command": "sed -n '1,120p' tools/bloc_linguistique.py", "description": "Read bloc header"}`

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
… [3304 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, collections\nd=json.load(open('tools/tests/linguistique/gold_reel.json'))\nph=d['phrases']\nprint('phrases', len(ph))\nprint('langues', collections.Counter(p.get('langue') for p in ph))\nseg_types=colle … [876 caractères tronqués]`

  ```
phrases 432
langues Counter({'fr': 228, 'en': 204})
segments 1445 {'GN': 658, 'GV': 532, 'GP': 71, 'REL': 57, 'SUB': 53, 'ADJ': 35, 'ADV': 30, 'PONCT': 9}
has cible 171 no cible 1274
by type/cible:
   ('ADJ', False) 35
   ('ADV', False) 30
   ('GN', False) 658
   ('GP', False) 9
   ('GP', True) 62
   ('GV', False) 532
   ('PONCT', False) 9
   ('REL', True) 57
   ('SUB', False) 1
   ('SUB', True) 52
sentences with >=1 segment no cible: 432
tokens 2375
  ```

- **bash** `{"command": "grep -rn \"candidats à annoter\\|candidat.*annoter\\|annoter\" reports/ docs/ tools/ --include=*.md --include=*.py --include=*.json 2>/dev/null | head -40", "description": "Search annotation candidates phrase"}`

  ```
reports/07/p4.md:574:   **annoter** (« 41 % de tokens coûteux ») et **laisser l'humain ou une boucle** corriger ✓✗ ;
reports/pensee-fiabilite-produit.json:3657:  "code": "\"\"\"test_schema_produit.py — le contrat de sortie de `drave analyser --json`.\n\nDeux contrats cohabitent :\n\n- **actuel** (drave 0.1.0) : 11 champs racine, 11 champs par étiquette, spans valides,\n  déterminisme. Ce test passe sur le produit livré ; il gèle l'enveloppe et attrape une\n  disparition de champ, un span hors texte ou une valeur qui n'est plus la surface.\n- **cible v1** (`schema: \"drave.annotation\"`, `version: \"1.0\"`, 8 champs requis) : il est\n  **sauté** tant que le champ `schema` n'existe pas, puis il devient strict. C'est le test\n  de non-régression du schéma versionné : il échoue si `schema`/`version` disparaissent,\n  si un des 8 champs manque, ou si le refus ne rend plus de JSON avec le code 3.\n\nÀ placer dans `tools/tests/test_schema_produit.py`. Stdlib seulement, lancé par\n`python3 tools/tests/test_schema_produit.py` ou `pytest`.\n\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport os\nimport pathlib\nimport re\nimport subprocess\nimport sys\nimport unittest\n\nRACINE
… [10518 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"attachement par type\\|erreurs d'attachement\\|erreur d'attachement\" reports/ docs/ tools/ 2>/dev/null | head -30", "description": "Search attachment errors phrase"}`

  ```
reports/pensee-spans-v7.json:1854:   "hypothese": "Les 43 sont des erreurs d'attachement",
reports/rapport-evaluer-langue.md:35:c'est la convention rejetée, pas une erreur d'attachement. Le français est **parfait en
reports/rapport-evaluer-langue.md:89:  (87/88), pas une erreur d'attachement (87/87 sur les spans) ;
reports/tableau-mesures.json:607:   "note": "g017 n'est pas une erreur d'attachement : c'est une convention d'annotation à trancher.",
tools/chantier/plan.json:452:   "mandat": "Tâche C3 : la coordination R — propose et mesure l'extension du gold réel (le « gold 200+ » des fiches R) : prends 50 phrases **réelles** (hand + reel) que l'heuristique rate, écris la fiche `reports/rapport-gold-reel-50.md` + JSON (les erreurs d'attachement par type, les candidats à annoter), sans modifier le gold (S/D territory : le gold est à S).",
  ```

- **bash** `{"command": "grep -rn \"gold 200+\" reports/ docs/ journal/ 2>/dev/null | head -40", "description": "Search gold 200+ mentions"}`

  ```
reports/rapport-pensee-porte-llm.md:93:3. **La pragmatique neuronale** et le **gold 200+ phrases** : la ligne L, pas B13.
reports/rapport-b13-porte-134.md:104:4. **L/B13** : le gold 200+, la porte qui bouge, la cascade complète restent les faits suivants.
reports/rapport-pensee-porte-minute.md:91:3. **Le gold 200+ phrases** et la **pragmatique** (l'heuristique garde) : la ligne L.
reports/rapport-pensee-porte-mobile.md:90:3. **Le gold 200+ phrases** et la **pragmatique** (l'heuristique garde) : la ligne L.
reports/rapport-b13-porte-138.md:82:3. **Le gold 200+ phrases** et la **pragmatique** (l'heuristique garde) : la ligne L.
reports/rapport-b13-porte-140.md:86:3. **Le gold 200+ phrases** et la **pragmatique** (l'heuristique garde) : la ligne L.
reports/rapport-pensee-porte-bouge.md:79:3. **Le gold 200+** et la **pragmatique** (l'heuristique garde) : la ligne L.
reports/rapport-pensee-porte-sto.md:84:3. **Le gold 200+** et la **pragmatique** (l'heuristique garde) : la ligne L.
reports/rapport-pensee-porte-sto-graines.md:74:2. **Le gold 200+** et la **pragmatique** (l'heuristique garde) : la ligne L.
reports/rapport-pensee-porte-fenetre.md:73:2. **Le gold 200+** et la **pragmatique*
… [10208 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tools/tests/ … [2313 caractères tronqués]`

  ```
total real 452
sentences with POS errors: 191 / 452
POS error tokens: 275
sentences with segment span errors: 213
attachment errors: 1
   ('g017', 'SUB', 'span_absent', 'that she would come', 'said')

Top POS error sentences:
r255 reel fr 4 | La voiture que j'ai achetée roule. | [("j'", 'PRON', '?'), ('ai', 'AUX', '?'), ('achetée', 'VERB', 'NOUN'), ('roule', 'VERB', 'NOUN')]
r349 reel fr 4 | Le livre est sur la table ; je le lis. | [('est', 'VERB', 'AUX'), ('table', 'NOUN', 'ADJ'), ('le', 'PRON', 'DET'), ('lis', 'VERB', 'NOUN')]
g004 hand fr 3 | Il a couru pour attraper le bus. | [('a', 'AUX', 'PREP'), ('couru', 'VERB', 'NOUN'), ('attraper', 'VERB', 'NOUN')]
r203 reel fr 3 | Le livre que j'ai lu est bon. | [("j'", 'PRON', '?'), ('ai', 'AUX', '?'), ('lu', 'VERB', 'NOUN')]
r210 reel fr 3 | Bien qu'il soit tard, il travaille. | [("qu'", 'CONJ', '?'), ('il', 'PRON', '?'), ('soit', 'AUX', 'NOUN')]
r225 reel fr 3 | Je crois qu'il a raison. | [("qu'", 'CONJ', '?'), ('il', 'PRON', '?'), ('a', 'AUX', 'PREP')]
r227 reel fr 3 | Pendant qu'il dort, elle lit. | [('Pendant', 'CONJ', 'PREP'), ("qu'", 'CONJ', '?'), ('il', 'PRON', '?')]
r260 reel fr 3 | Bien qu'il pleuve, il sort. | [("qu'", 'CONJ'
… [2753 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '45,70p' reports/rapport-file-taches.md && echo \"=====\" && sed -n '195,215p' reports/rapport-file-taches.md", "description": "Read T15 and D5 details"}`

  ```
## 4. File (b) — coordination requise (11)

Critère : la tâche est réelle et non bloquée par une ressource externe, mais elle s'écrit dans un territoire qui n'est pas celui de la fenêtre (S, D, N2, A, produit) ou elle demande un arbitrage d'architecture. On **lit, on propose, on ne code pas** dans ces fichiers.

| id | chantier | action | fichier / outil | dépend de | bloquant | commande exacte | prio |
|---|---|---|---|---|---|---|---|
| T09 | N2 | La porte propre (0,29 manquant à 2,7856) : données ou capacité | reports/n2-*, work/n2ac/, tools/entrainer_native.py, GPU | recette N2 1 024 | aucun externe ; GPU libres (0 %) | python3 tools/eval_n2_propre.py <checkpoint> (pas de commande unique) | P0 |
| T10 | R1 | Aiguille native >= 15/18 à 4 000 non atteinte (copie 0,0078) : décider R11 close ou passer à R2.1 (tampon en entrée) | reports/rapport-n2-r12-2048.md ; backlog/R11-contexte-hierarchique.md ; backlog/R21-memoire-travail-gist.md | R11/R12 mesurées | décision d'architecture | python3 tools/verifie_backlog.py | P1 |
| T11 | N4 | Consigne courte : construire le jeu, entraîner, évaluer tenu à l'écart (24/24 vus, 0/4 tenus) | backlog/N4-usage-sft.md ; reports/n4-* ; N2/GPU | recet
… [5716 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"gold.*réel\\|gold réel\" reports/rapport-tagger-option.md reports/rapport-coordination-r.md reports/rapport-pensee-gold-*.md 2>/dev/null | head -40", "description": "Search gold reel in R fiches"}`

  ```
reports/rapport-tagger-option.md:8:> le seul gold réel 432 : lire le chiffre avec sa source.
reports/rapport-tagger-option.md:104:(**+21,46**). Le seul gold **réel 432** ne vaut que **+4,67**. Ne pas annoncer +8,49 sans sa
reports/rapport-coordination-r.md:115:- **Gold** : `gold.json` **20 hand** + `gold_reel.json` **432 réel** + `gold_synthetique.json`
reports/rapport-pensee-gold-200.md:1:# B13 — le gold à 200 phrases réelles : POS 0,7738
reports/rapport-pensee-gold-200.md:4:> **88/88 portes** : le gold réel passe de **180 à 200 phrases** (r181–r200, 10 françaises et 10
reports/rapport-pensee-gold-200.md:12:## 1. Le gold à 200 réels
reports/rapport-pensee-gold-200.md:37:- **Le gold 380** (200 réels + 160 synthétiques + 20 de `gold.py`) est un jouet.
reports/rapport-pensee-gold-200-subsets.md:4:> **89/89 portes** : le gold réel de 200 phrases est scindé en deux sous-ensembles. Les **20
reports/rapport-pensee-gold-200-subsets.md:34:- **Le gold 380** (200 réels + 160 synthétiques + 20 de `gold.py`).
reports/rapport-pensee-gold-342.md:40:- **Le gold réel (342)** est le sous-ensemble qui compte ; le synthétique dilue.
reports/rapport-pensee-gold-342.md:60:- [`gold_reel.py`](../tools/te
… [1695 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '150,185p' reports/rapport-tagger-option.md", "description": "Read tagger option suite"}`

  ```
- **Aucune porte ne fait d'appel API** : le chemin réseau réel est couvert par la mesure du
  § 3 et par le harnais `qualifier_tagger_612.py`, pas par la porte. C'est le prix de la règle
  « hors ligne par défaut ».

## 7. Les limites et la suite

- Le gain est **conditionnel** à la clé et au réseau ; le défaut reste l'heuristique.
- Le tagger est **français** (prompt), même s'il étiquette l'anglais du gold ; la ventilation
  par langue du 612 n'est pas faite ici.
- Les **2 appels/phrase** incluent le tagger de syntagmes dont la sortie est ignorée. Si l'on
  ne veut que le POS, un appel suffirait : ~0,02 $ pour 612 et ~590 tokens/phrase en moins.
  C'est une optimisation **non mesurée** ; on ne l'a pas prise pour rester sur le câblage du
  harnais.
- La **mesure 612 via le CLI** (`evaluer --tagger` complet) n'a pas été refaite : elle coûterait
  un second ~0,04 $ et ~21 min. Le CLI a été validé sur 20 phrases avec le même cache ; le
  chiffre 612 est celui du harnais, déjà publié.
- **Suite** : mesurer le 612 par le CLI (mêmes réponses en cache), puis trancher l'appel de
  syntagmes inutile. La décision 1A est **livrée** ; la ligne R0.7 garde le split réel et le
  gold 200+.

## 8.
… [566 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nfor f in ['reports/tagger-612.json','reports/pensee-quatre-modes-432-run2.json']:\n    try:\n        d=json.load(open(f))\n    except Exception as e:\n        print(f,'ERR',e); continue\n    print('===' … [611 caractères tronqués]`

  ```
=== reports/tagger-612.json <class 'dict'> ['date', 'gold', 'modeles_renvoyes', 'modes', 'pos_par_source', 'seuils', 'refus', 'refus_detail', 'appels', 'api', 'latence_s', 'duree_totale_s', 'limites']
 date str 20
 gold dict 4
   phrases int 
   tokens int 
   sources dict 3
     hand int 
     reel int 
     synth int 
   modalite str 66
 modeles_renvoyes dict 1
   deepseek-flash int 
 modes dict 6
   heuristique dict 5
     all dict 5
     hand dict 5
     reel dict 5
     synth dict 5
     duree_s float 
   neuronal dict 5
     all dict 5
     hand dict 5
     reel dict 5
     synth dict 5
     duree_s float 
   parallele dict 5
     all dict 5
     hand dict 5
     reel dict 5
     synth dict 5
     duree_s float 
   cascade dict 5
     all dict 5
     hand dict 5
     reel dict 5
     synth dict 5
     duree_s float 
   parallele_niveau dict 5
     all dict 5
     hand dict 5
     reel dict 5
     synth dict 5
     duree_s float 
   cascade_niveau dict 5
     all dict 5
     hand dict 5
     reel dict 5
     synth dict 5
     duree_s float 
 pos_par_source dict 6
   heuristique dict 4
     all float 
     hand float 
     reel float 
     synth float 
   neuronal dict 4
     a
… [2072 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,240p' tools/tests/linguistique/qualifier_tagger_612.py", "description": "Read tagger 612 harness"}`

  ```
#!/usr/bin/env python3
"""qualifier_tagger_612.py — le tagger POS API sur le gold 612 (hand 20 + reel 432 + synth 160).

POURQUOI. Le banc `qualifier_quatre_modes.py` ne charge que `gold_reel.json` (432 phrases) ; le
gold courant en compte 612, et le tagger n'y a jamais été mesuré. Ce banc ajoute la ventilation
hand / reel / synth, la latence réelle des appels et le modèle effectivement renvoyé par l'API.
Il ne modifie aucun autre fichier et n'écrit que le JSON demandé.

COÛT. Deux appels par phrase (POS + syntagmes), partagés par les six modes grâce au cache des
tagger : ~1 214 appels, ~360 k tokens, ~20 min pour 612 phrases.

USAGE.
    DEEPSEEK_KEY_FILE=$HOME/.config/drave/deepseek.key \
    DEEPSEEK_CACHE=$(mktemp -d /tmp/j43-cache.XXXX) \
    DEEPSEEK_MODEL=deepseek-chat \
    PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
      --sortie /tmp/tagger-612.json

La clé n'est jamais lue en dur : `tools/llm/deepseek.py` lit `DEEPSEEK_API_KEY` ou le fichier
`DEEPSEEK_KEY_FILE` (0600). Le cache doit être neuf : le cache par défaut contient les réponses
du 2026-11-04 et rejouerait l'ancien modèle au lieu de mesurer celui d'aujourd'hui.
"""
from __future__ impo
… [7445 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/tests/linguistique/gold_split.py && echo \"=====\" && sed -n '1,120p' tools/tests/linguistique/gold_reel.py", "description": "Read gold split and gold reel source"}`

  ```
"""gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.

Le problème. Toutes les mesures de la session sont **in-sample** : les règles de segmentation et
d'attachement ont été dessinées en regardant les échecs du même gold qui les mesure. Pour juger
une règle, il faut un gold **tenu à l'écart** : on règle sur `dev`, on évalue sur `test`.

Protocole (fixé ici). Le split est un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` →
test, sinon dev), donc reproductible, insensible à l'ordre et indépendant du contenu. Il est
**stratifié par source** (`hand`, `reel`, `synthetique`) et par langue : on vérifie l'équilibre
dans la fiche. Aucune phrase n'est dupliquée entre les deux ; l'union redonne les 612.

Usage :
    from tools.tests.linguistique.gold_split import dev, test, compter
    ph = charger(); d = dev(ph); t = test(ph)
"""
from __future__ import annotations

import zlib

PART_TEST = 3  # une phrase sur trois va au test


def _est_test(phrase: dict) -> bool:
    return zlib.crc32(str(phrase.get("id", "")).encode()) % PART_TEST == 0


def dev(phrases: list[dict]) -> list[dict]:
    """Les phrases de développement (2/3)."""
    return [p for p in phr
… [9687 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections, zlib\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tools/ … [2483 caractères tronqués]`

  ```
universe 452

== pos == {('reel', 'fr'): 35, ('hand', 'fr'): 4, ('reel', 'en'): 11}
POS err 120 seg_fn 46 seg_fp 55 att 0
ids: ['r255', 'r349', 'g004', 'r203', 'r210', 'r225', 'r227', 'r260', 'r261', 'r262', 'r266', 'r272', 'r309', 'r331', 'r339', 'r357', 'r409', 'r429', 'g003', 'g005', 'g011', 'r014', 'r034', 'r051', 'r091', 'r102', 'r126', 'r179', 'r189', 'r206', 'r208', 'r223', 'r229', 'r230', 'r246', 'r256', 'r264', 'r267', 'r274', 'r287', 'r291', 'r297', 'r304', 'r324', 'r328', 'r346', 'r354', 'r363', 'r366', 'r368']
min score (-2, 'r368')

== pos+fn == {('reel', 'fr'): 42, ('reel', 'en'): 8}
POS err 87 seg_fn 141 seg_fp 70 att 0
ids: ['r339', 'r346', 'r349', 'r408', 'r409', 'r091', 'r179', 'r203', 'r261', 'r304', 'r331', 'r343', 'r347', 'r410', 'r411', 'r412', 'r413', 'r414', 'r415', 'r416', 'r417', 'r422', 'r046', 'r081', 'r089', 'r096', 'r099', 'r119', 'r121', 'r128', 'r129', 'r133', 'r134', 'r135', 'r137', 'r140', 'r141', 'r143', 'r146', 'r148', 'r149', 'r163', 'r246', 'r255', 'r287', 'r291', 'r297', 'r309', 'r323', 'r324']
min score (-4, 'r324')

== pos+fn+att == {('reel', 'fr'): 42, ('reel', 'en'): 7, ('hand', 'fr'): 1}
POS err 113 seg_fn 105 seg_fp 67 att 0
ids: ['r339'
… [650 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tools/tests/ … [1281 caractères tronqués]`

  ```
missing by type {'SUB': 1, 'GN': 124, 'GV': 147, 'ADJ': 35, 'ADV': 30, 'PONCT': 9}
extra by type {'GP': 25, 'GV': 125, 'SUB': 4, 'REL': 11, 'GN': 101}

 r408 Ne viens-tu pas demain ?
  gold [('GV', 'viens'), ('GN', 'tu'), ('ADV', 'pas'), ('ADV', 'demain')]
  miss [('ADV', 'pas'), ('ADV', 'demain'), ('GN', 'tu'), ('GV', 'viens')]
  extra [('GP', 'demain'), ('GV', 'Ne viens-tu pas')]

 r409 Ne mange-t-il pas ?
  gold [('GV', 'mange'), ('GN', 'il'), ('ADV', 'pas')]
  miss [('ADV', 'pas'), ('GN', 'il'), ('GV', 'mange')]
  extra [('GV', 'Ne mange-t-il pas')]

 r410 Ne dort-elle pas ?
  gold [('GV', 'dort'), ('GN', 'elle'), ('ADV', 'pas')]
  miss [('ADV', 'pas'), ('GN', 'elle'), ('GV', 'dort')]
  extra [('GV', 'Ne dort-elle pas')]

 r411 Ne partent-ils pas ?
  gold [('GV', 'partent'), ('GN', 'ils'), ('ADV', 'pas')]
  miss [('ADV', 'pas'), ('GN', 'ils'), ('GV', 'partent')]
  extra [('GV', 'Ne partent-ils pas')]

 r412 Ne lis-tu pas ?
  gold [('GV', 'lis'), ('GN', 'tu'), ('ADV', 'pas')]
  miss [('ADV', 'pas'), ('GN', 'tu'), ('GV', 'lis')]
  extra [('GV', 'Ne lis-tu pas')]

 r413 Ne parle-t-elle pas ?
  gold [('GV', 'parle'), ('GN', 'elle'), ('ADV', 'pas')]
  miss [('ADV', 'pas'), ('GN', 'e
… [1398 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tools/tests/ … [2804 caractères tronqués]`

  ```
error sentences per lang: {'fr': 167, 'en': 91}
total per lang Counter({'fr': 242, 'en': 210})

 fr top25: {'reel': 24, 'hand': 1}
  POS err 70 seg_fn 40 att 0
  min r412 2 3
  ids ['r349', 'r255', 'r339', 'r409', 'r203', 'r261', 'r331', 'r309', 'r357', 'g004', 'r210', 'r225', 'r227', 'r260', 'r262', 'r266', 'r272', 'r429', 'r346', 'r408', 'r091', 'r304', 'r410', 'r411', 'r412']

 en top25: {'reel': 25}
  POS err 37 seg_fn 44 att 0
  min r076 1 1
  ids ['r179', 'r422', 'r246', 'r287', 'r291', 'r297', 'r328', 'r363', 'r368', 'r034', 'r102', 'r366', 'r119', 'r163', 'r104', 'r106', 'r159', 'r217', 'r241', 'r285', 'r293', 'r362', 'r370', 'r071', 'r076']

g017 in sel? False
sel sources Counter({'reel': 49, 'hand': 1})
sel langs Counter({'fr': 25, 'en': 25})
sel POS err 107 seg_fn 84 seg_fp 56 att 0
sel tokens 316
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tools/tests/ … [2144 caractères tronqués]`

  ```
weights att 3 pos 2 fn 1
 sources {'reel': 49, 'hand': 1} langs {'fr': 43, 'en': 7}
 pos 113 fn 105 fp 67 att 0
 g017 False hand ['g004']
 ids ['r339', 'r349', 'r409', 'r203', 'r255', 'r261', 'r331', 'r346', 'r408', 'r091', 'r179', 'r304', 'r309', 'r357', 'r410', 'r411', 'r412', 'r413', 'r414', 'r415', 'r416', 'r417', 'r422', 'g004', 'r210', 'r225', 'r227', 'r246', 'r260', 'r262', 'r266', 'r272', 'r287', 'r291', 'r297', 'r324', 'r328', 'r343', 'r347', 'r374', 'r376', 'r379', 'r389', 'r429', 'r046', 'r051', 'r081', 'r089', 'r096', 'r099']

weights att 5 pos 2 fn 1
 sources {'reel': 48, 'hand': 2} langs {'fr': 42, 'en': 8}
 pos 112 fn 103 fp 67 att 1
 g017 True hand ['g004', 'g017']
 ids ['r339', 'r349', 'r409', 'r203', 'r255', 'r261', 'r331', 'r346', 'r408', 'r091', 'r179', 'r304', 'r309', 'r357', 'r410', 'r411', 'r412', 'r413', 'r414', 'r415', 'r416', 'r417', 'r422', 'g004', 'g017', 'r210', 'r225', 'r227', 'r246', 'r260', 'r262', 'r266', 'r272', 'r287', 'r291', 'r297', 'r324', 'r328', 'r343', 'r347', 'r374', 'r376', 'r379', 'r389', 'r429', 'r046', 'r051', 'r081', 'r089', 'r096']

weights att 2 pos 1 fn 1
 sources {'reel': 50} langs {'fr': 42, 'en': 8}
 pos 87 fn 141 fp 70 att 0
 g0
… [1493 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/llm/deepseek.py", "description": "Read DeepSeek client/cache"}`

  ```
#!/usr/bin/env python3
"""deepseek.py — le professeur externe, sans poids locaux.

POURQUOI CE MODULE. Le dépôt garde ses GPU et ses CPU pour le **modèle natif**
Drave (`entrainer_moteur.py`, `drave-core`) et pour les mesures **boîte blanche**
(perplexité, activations, flux, sondes). Le **langage** — traduire, juger,
générer, évaluer — passe par une API : on ne charge plus un Qwen de 7/14/32 B
pour cela. DeepSeek est ce **professeur externe** ; ses sorties peuvent servir à
entraîner/distiller l'élève natif (autorisation explicite du propriétaire de la
licence).

CE QUE LE MODULE NE FAIT PAS. Il ne remplace pas les mesures d'états internes :
une API ne donne pas les poids ni les activations. Il ne met **jamais** la clé
dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
paquet externe : `urllib` suffit.

CONTRAT.
- `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
- `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
- `DEEPSEEK_MODEL` (ou `DSH_MODEL`) : `deepseek-chat` par défaut ;
- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages
  + température + max_tokens, **jamais
… [8271 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1968,2100p' tools/bloc_linguistique.py", "description": "Read NeuronalLLMPOS"}`

  ```
class NeuronalLLMPOS:
    """Le **tagger** neuronal réel : un modèle local, des POS alignés sur la tokenisation du bloc.

    Le modèle ne rend pas une annotation complète : il rend **une classe par token**, contrainte
    par une grammaire GBNF (`grammaire_pos`) qui interdit un JSON tronqué, un token manquant ou
    une classe hors du jeu. Les spans sont ceux de `Heuristique._mots` (la tokenisation du bloc),
    pas ceux que le modèle inventerait ; c'est ce qui rend la mesure POS exacte.

    Le modèle est servi par `llama-server` (`/v1/chat/completions`, `grammar`) : le serveur est
    lancé une fois, le modèle chargé une fois, et les 180 phrases coûtent une passe CPU, pas
    180 chargements. `transport` est injectable pour tester le contrat sans modèle.

    La confiance par défaut (`0.6`) est **celle du seuil ouvert de l'heuristique** (0.55) : dans
    une `Cascade`, le tagger ne remplace donc que les tokens que l'heuristique déclare peu sûrs,
    et laisse les classes fermées (0.92) à l'heuristique. C'est la politique mesurée.
    """

    nom = "neuronal"

    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18081",
                 confiance:
… [5844 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/deepseek/ 2>/dev/null; find data/deepseek -maxdepth 2 -type f 2>/dev/null | head -10; du -sh data/deepseek/cache 2>/dev/null", "description": "Inspect DeepSeek cache directory"}`

  ```
total 5016
drwxr-xr-x. 1 stephane stephane     574 26 oct 15:08 .
drwxr-xr-x. 1 stephane stephane    2664  2 nov 18:33 ..
drwxr-xr-x. 1 stephane stephane  518742 15 nov 01:38 cache
drwxr-xr-x. 1 stephane stephane      50 26 oct 11:25 distillation
drwxr-xr-x. 1 stephane stephane      50 26 oct 11:39 distillation-300
drwxr-xr-x. 1 stephane stephane      50 26 oct 11:39 distillation-300-controle
drwxr-xr-x. 1 stephane stephane      50 26 oct 14:46 distillation-600
drwxr-xr-x. 1 stephane stephane      50 26 oct 14:46 distillation-600-controle
drwxr-xr-x. 1 stephane stephane      50 26 oct 15:08 distillation-910
drwxr-xr-x. 1 stephane stephane      50 26 oct 15:08 distillation-910-controle
drwxr-xr-x. 1 stephane stephane      50 26 oct 11:25 distillation-controle
-rw-r--r--. 1 stephane stephane  571079 26 oct 11:39 enseignant-300.jsonl
-rw-r--r--. 1 stephane stephane 1147125 26 oct 14:46 enseignant-600.jsonl
-rw-r--r--. 1 stephane stephane 1655674 26 oct 15:07 enseignant-910.jsonl
-rw-r--r--. 1 stephane stephane  109007 26 oct 11:24 enseignant.jsonl
-rw-r--r--. 1 stephane stephane  667025 26 oct 14:38 prompts_publics_600.jsonl
-rw-r--r--. 1 stephane stephane  974641 26 oct 14:59 prompts
… [942 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && DEEPSEEK_KEY_FILE=\"$HOME/.config/drave/deepseek.key\" PYTHONPATH=. timeout 120 python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'tools')\nfrom tools.llm.deepseek import DeepSeek\nfrom tools.bloc_linguistique import NeuronalLLMP … [679 caractères tronqués]`

  ```
disponible True cache /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/deepseek/cache
Le chien mange une pomme. refus=  [('Le', 'DET'), ('chien', 'NOUN'), ('mange', 'VERB'), ('une', 'DET'), ('pomme', 'NOUN')]
Le chat boit du lait. refus=  [('Le', 'DET'), ('chat', 'NOUN'), ('boit', 'VERB'), ('du', 'DET'), ('lait', 'NOUN')]
Ne viens-tu pas demain ? refus=  [('Ne', 'ADV'), ('viens-tu', 'VERB'), ('pas', 'ADV'), ('demain', 'NOUN')]
{'appels': 3, 'cache': 3}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tools/tests/ … [3301 caractères tronqués]`

  ```
fr picked 25 hand 1 score min 6 pos sum 67 fn 44 att 0
en picked 25 hand 1 score min 3 pos sum 35 fn 43 att 1

TOTAL sources Counter({'reel': 48, 'hand': 2}) langs Counter({'fr': 25, 'en': 25})
TOTAL pos 102 fn 87 fp 60 att 1 tokens 323
g017 True
signatures distinct 42

selected:
r179  reel en score= 7 pos=2 fn=3 fp=1 att=0 | The rain washes the streets.
r422  reel en score= 7 pos=2 fn=3 fp=1 att=0 | You don't come tomorrow?
r246  reel en score= 6 pos=2 fn=2 fp=1 att=0 | The dog that barks is mean.
r287  reel en score= 6 pos=2 fn=2 fp=1 att=0 | The bird that flies is blue.
r291  reel en score= 6 pos=2 fn=2 fp=1 att=0 | The book that is on the table is mine.
r328  reel en score= 6 pos=2 fn=2 fp=1 att=0 | The book is on the table; it is red.
r119  reel en score= 5 pos=1 fn=3 fp=1 att=0 | The tourists visit the museum.
r163  reel en score= 5 pos=1 fn=3 fp=1 att=0 | The students review their lessons.
r363  reel en score= 5 pos=2 fn=1 fp=1 att=0 | The book is on the table; I read it.
r368  reel en score= 5 pos=2 fn=1 fp=1 att=0 | Marie and Paul dance; they have fun.
g017  hand en score= 4 pos=0 fn=1 fp=1 att=1 | She said that she would come yesterday.
r034  reel en score= 4 pos=2 fn=0 f
… [3072 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tools/tests/ … [3508 caractères tronqués]`

  ```
Global segments without cible by type: Counter({'GN': 681, 'GV': 552, 'ADJ': 35, 'ADV': 30, 'GP': 9, 'PONCT': 9, 'SUB': 1})
Global GP/REL/SUB without cible:
   ('r267', 'GP', 'à moi', 34, 39, 'Le livre qui est sur la table est à moi.')
   ('r324', 'GP', 'sur la table', 13, 25, 'Le livre est sur la table ; il est rouge.')
   ('r328', 'GP', 'on the table', 12, 24, 'The book is on the table; it is red.')
   ('r336', 'GP', 'to her', 27, 33, 'Paul sees Marie; he speaks to her.')
   ('r342', 'GP', 'to her', 27, 33, 'Paul sees Marie; he speaks to her; she listens.')
   ('r349', 'GP', 'sur la table', 13, 25, 'Le livre est sur la table ; je le lis.')
   ('r358', 'GP', 'to her', 27, 33, 'Paul sees Marie; he speaks to her.')
   ('r363', 'GP', 'on the table', 12, 24, 'The book is on the table; I read it.')
   ('r367', 'GP', 'to him', 40, 46, 'The teacher speaks; the students listen to him.')
   ('r429', 'SUB', "que c'est vrai", 7, 21, "On dit que c'est vrai.")

In 50: segments without cible by type: Counter({'GN': 79, 'GV': 65, 'ADJ': 11, 'ADV': 9, 'GP': 4})
In 50: GP/REL/SUB without cible:
   ('r324', 'GP', 'sur la table', 13, 25, 'Le livre est sur la table ; il est rouge.')
   ('r328', 'GP',
… [501 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor f in ['gold.json','gold_reel.json']:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    p=next(q for q in  … [469 caractères tronqués]`

  ```
gold.json {'id': 'g017', 'langue': 'en', 'texte': 'She said that she would come yesterday.', 'mots': [{'texte': 'She', 'pos': 'PRON', 'debut': 0, 'fin': 3}, {'texte': 'said', 'pos': 'VERB', 'debut': 4, 'fin': 8}, {'texte': 'that', 'pos': 'CONJ', 'debut': 9, 'fin': 13}, {'texte': 'she', 'pos': 'PRON', 'debut': 14, 'fin': 17}, {'texte': 'would', 'pos': 'AUX', 'debut': 18, 'fin': 23}, {'texte': 'come', 'pos': 'VERB', 'debut': 24, 'fin': 28}, {'texte': 'yesterday', 'pos': 'ADV', 'debut': 29, 'fin': 38}], 'segments': [{'type': 'GN', 'texte': 'She', 'role': 'agent', 'debut': 0, 'fin': 3}, {'type': 'GV', 'texte': 'said', 'role': 'prédicat', 'debut': 4, 'fin': 8}, {'type': 'SUB', 'texte': 'that she would come', 'role': 'contenu', 'debut': 9, 'fin': 28, 'cibles': ['said'], 'cible': 'said'}], 'pragma': {'acte': 'assertion', 'modalite': True}}
segments pred: [('GN', 'She', 0, 3, {'segment': 'She', 'cible': 'said'}, ['GN', 'said']), ('GV', 'said', 4, 8, None, ['GV']), ('SUB', 'that she would come yesterday', 9, 38, {'segment': 'that she would come yesterday', 'cible': 'said'}, ['SUB', 'said', 'said'])]
POS pred: [('She', 'PRON'), ('said', 'VERB'), ('that', 'CONJ'), ('she', 'PRON'), ('would', '
… [312 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && DEEPSEEK_KEY_FILE=\"$HOME/.config/drave/deepseek.key\" PYTHONPATH=. timeout 300 python3 - <<'PY'\nimport json,sys,pathlib,collections\nsys.path.insert(0,'tools')\nfrom tools.llm.deepseek import DeepSeek, _cache_cle\nfrom tools.bloc_l … [1417 caractères tronqués]`

  ```
cache /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/deepseek/cache modele deepseek-chat
phrases 452 tokens 2480
POS 0.9399 ferme 0.9231 ouvert 0.9577
F1 0.0 att 0.0 0 / 184
refus? 449 miss 0
refus 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections, random\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tool … [5392 caractères tronqués]`

  ```
GLOBAL {'n': 452, 'tokens': 2480, 'pos': 0.8891, 'pos_ferme': 0.9294, 'pos_ouvert': 0.8466, 'tp': 1155, 'fp': 266, 'fn': 346, 'precision': 0.8128, 'rappel': 0.7695, 'f1': 0.7906, 'targets': 184, 'att_ok': 183, 'att_exact': 0.9946}
HARD50 {'n': 50, 'tokens': 323, 'pos': 0.6842, 'pos_ferme': 0.7542, 'pos_ouvert': 0.5972, 'tp': 103, 'fp': 60, 'fn': 87, 'precision': 0.6319, 'rappel': 0.5421, 'f1': 0.5836, 'targets': 22, 'att_ok': 21, 'att_exact': 0.9545}
REST402 {'n': 402, 'tokens': 2157, 'pos': 0.9198, 'pos_ferme': 0.958, 'pos_ouvert': 0.8804, 'tp': 1052, 'fp': 206, 'fn': 259, 'precision': 0.8362, 'rappel': 0.8024, 'f1': 0.819, 'targets': 162, 'att_ok': 162, 'att_exact': 1.0}
HARD POS errors 102 / 275 FN 87 / 346 ATT 1 / 1
random 50 controls:
 seed 0 pos 0.8685 f1 0.8228 att 1.0 targets 23
 seed 1 pos 0.8942 f1 0.8 att 1.0 targets 22
 seed 2 pos 0.8858 f1 0.7622 att 1.0 targets 16
 seed 3 pos 0.8678 f1 0.7744 att 1.0 targets 22
 seed 4 pos 0.85 f1 0.8013 att 1.0 targets 24
HARD by lang:
  fr {'n': 25, 'tokens': 168, 'pos': 0.6012, 'pos_ferme': 0.6224, 'pos_ouvert': 0.5714, 'tp': 54, 'fp': 38, 'fn': 44, 'precision': 0.587, 'rappel': 0.551, 'f1': 0.5684, 'targets': 12, 'att_ok': 12, 'at
… [1960 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tools/tests/ … [818 caractères tronqués]`

  ```
global segments {'GN': 681, 'GV': 552, 'GP': 81, 'SUB': 55, 'REL': 58, 'ADJ': 35, 'ADV': 30, 'PONCT': 9}
targets {'GP': 72, 'SUB': 54, 'REL': 58} total 184
no cible {'GN': 681, 'GV': 552, 'ADJ': 35, 'ADV': 30, 'GP': 9, 'PONCT': 9, 'SUB': 1}

hand:
g001 []
g002 [('GP', 'de la voisine', 'chat', ['chat'])]
g003 [('GP', 'dans le parc', 'vu', ['vu', "l'homme"])]
g004 [('GP', 'pour attraper le bus', 'couru', ['couru'])]
g005 [('SUB', "qu'elle viendrait", 'dit', ['dit'])]
g006 [('GP', 'du voisin', 'chien', ['chien'])]
g007 [('GP', 'dans le jardin', 'jouent', ['jouent', 'enfants'])]
g008 []
g009 []
g010 [('GP', 'ici', 'Viens', ['Viens'])]
g011 [('REL', "que j'ai lu", 'livre', ['livre'])]
g012 [('GP', 'à manger', 'prêt', ['prêt', 'canard'])]
g013 []
g014 [('GP', 'avec le télescope', 'vu', ['vu'])]
g015 []
g016 [('GP', 'in the park', 'saw', ['saw', 'man'])]
g017 [('SUB', 'that she would come', 'said', ['said'])]
g018 []
g019 []
g020 [('GP', 'to eat', 'ready', ['ready', 'duck'])]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections, random\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tool … [3643 caractères tronqués]`

  ```
== GLOBAL ==
  GN {'tp': 557, 'fp': 101, 'fn': 124, 'precision': 0.8465, 'rappel': 0.8179, 'f1': 0.832}
  GV {'tp': 405, 'fp': 125, 'fn': 147, 'precision': 0.7642, 'rappel': 0.7337, 'f1': 0.7486}
  GP {'tp': 81, 'fp': 25, 'fn': 0, 'precision': 0.7642, 'rappel': 1.0, 'f1': 0.8663}
  REL {'tp': 58, 'fp': 11, 'fn': 0, 'precision': 0.8406, 'rappel': 1.0, 'f1': 0.9134}
  SUB {'tp': 54, 'fp': 4, 'fn': 1, 'precision': 0.931, 'rappel': 0.9818, 'f1': 0.9558}
  ADJ {'tp': 0, 'fp': 0, 'fn': 35, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0}
  ADV {'tp': 0, 'fp': 0, 'fn': 30, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0}
  PONCT {'tp': 0, 'fp': 0, 'fn': 9, 'precision': 0.0, 'rappel': 0.0, 'f1': 0.0}

== HARD50 ==
  GN {'tp': 51, 'fp': 22, 'fn': 28, 'precision': 0.6986, 'rappel': 0.6456, 'f1': 0.6711}
  GV {'tp': 27, 'fp': 28, 'fn': 38, 'precision': 0.4909, 'rappel': 0.4154, 'f1': 0.45}
  GP {'tp': 6, 'fp': 4, 'fn': 0, 'precision': 0.6, 'rappel': 1.0, 'f1': 0.75}
  REL {'tp': 11, 'fp': 5, 'fn': 0, 'precision': 0.6875, 'rappel': 1.0, 'f1': 0.8148}
  SUB {'tp': 8, 'fp': 1, 'fn': 1, 'precision': 0.8889, 'rappel': 0.8889, 'f1': 0.8889}
  ADJ {'tp': 0, 'fp': 0, 'fn': 11, 'precision': 0.0, 'rappel': 0.0, 
… [932 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, collections, random\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nreel=json.load(open('tool … [3965 caractères tronqués]`

  ```
stratified random controls (24 reel fr+1 hand fr, 24 reel en+1 hand en):
 seed 0 {'pos': 0.8631, 'f1': 0.7862, 'att': 1.0, 'tokens': 263, 'targets': 17}
 seed 1 {'pos': 0.9015, 'f1': 0.8089, 'att': 1.0, 'tokens': 264, 'targets': 20}
 seed 2 {'pos': 0.9035, 'f1': 0.7759, 'att': 1.0, 'tokens': 259, 'targets': 20}
 seed 3 {'pos': 0.8801, 'f1': 0.7677, 'att': 1.0, 'tokens': 267, 'targets': 22}
 seed 4 {'pos': 0.893, 'f1': 0.8146, 'att': 1.0, 'tokens': 271, 'targets': 22}
 seed 5 {'pos': 0.8571, 'f1': 0.8182, 'att': 0.9444, 'tokens': 266, 'targets': 18}
 seed 6 {'pos': 0.9164, 'f1': 0.8118, 'att': 1.0, 'tokens': 275, 'targets': 19}
 seed 7 {'pos': 0.8881, 'f1': 0.8571, 'att': 1.0, 'tokens': 277, 'targets': 26}

hard {'pos': 0.6842, 'f1': 0.5836, 'att': 0.9545, 'tokens': 323, 'targets': 22}
hard majority PRON 71 / 323 0.2198 dist {'NOUN': 57, 'VERB': 70, 'DET': 44, 'PRON': 71, 'PREP': 7, 'ADV': 21, 'PONCT': 4, 'AUX': 22, 'ADJ': 13, 'CONJ': 14}
global majority VERB 582 / 2480 0.2347 dist {'DET': 443, 'NOUN': 519, 'VERB': 582, 'PREP': 90, 'AUX': 125, 'PRON': 432, 'CONJ': 83, 'ADV': 99, 'ADJ': 80, 'NUM': 2, 'PONCT': 25}
hard uniform 0.096 31 / 323
global uniform 0.0847 210 / 2480
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\n# Sensitivity of the diversity-capped selection to score weights\nimport json, sys, collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nhand=json.load(open('tools/tests/lingu … [2399 caractères tronqués]`

  ```
base 50
(2, 2, 1) overlap 50 /50 jaccard 1.0
(5, 2, 1) overlap 50 /50 jaccard 1.0
(3, 1, 1) overlap 39 /50 jaccard 0.639
(3, 3, 1) overlap 48 /50 jaccard 0.923
(1, 1, 1) overlap 39 /50 jaccard 0.639
(0, 1, 0) overlap 35 /50 jaccard 0.538
(10, 1, 1) overlap 39 /50 jaccard 0.639
  ```

### 🤖 Assistant

Now I have a clear picture. Let me write a reproducible measurement script (additive, read-only on the gold) that selects the 50 hard real sentences, computes the error taxonomy by type, and lists the annotation candidates.

- **bash** `{"command": "ls -la tools/tests/linguistique/__init__.py 2>/dev/null; head -5 tools/tests/linguistique/qualifier_syntagmes.py", "description": "Check package init and style"}`

  ```
#!/usr/bin/env python3
"""qualifier_syntagmes.py — qualifie le tagger de syntagmes local sur le gold (180 phrases).

Le tagger est `bloc_linguistique.NeuronalLLMChunks` : un modèle GGUF servi par `llama-server`,
une étiquette **BIO par token** contrainte par grammaire GBNF, et les spans reconstruits sur
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "content": "#!/usr/bin/env python3\n\"\"\"gold_reel_50.py — les 50 phrases réelles que l'heuristique rate (proposition C3/R).\n\nPOURQUOI. Le gold réel (`gold.json` 20 hand + `gold_reel.json` 43 … [28057 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "old_string": "import argparse\nimport collections\nimport hashlib\nimport json\nimport pathlib\nimport random\nimport subprocess\nimport sys\nimport time", "new_string": "import argparse\nimpor … [132 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "old_string": "        signatures = collections.Counter()\n        prises = []\n        for r in candidates:\n            if len(prises) >= quota:\n                break\n            if signatur … [1148 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "old_string": "    def planchers(rs: list[dict]) -> dict:\n        classes = collections.Counter()\n        for r in rs:\n            classes.update(m[\"pos\"] for m in [{\"pos\": p} for p in _t … [497 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "old_string": "def _tokens_gold(r: dict) -> list[str]:\n    return r.get(\"_tokens\", [])\n\n\ndef sensibilite(rows: list[dict], reference: list[dict]) -> list[dict]:\n    \"\"\"Le lot change-t- … [839 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "    pos_par_type_global = collections.Counter()\n    for r in rows:\n        for e in r[\"pos\"][\"erreurs\"]:\n            pos_par_type_global[(e[\"gold\"], e[\"predit\"])] += 1\ … [367 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "                \"pos\": {\"total\": somme(rows, \"pos\"),\n                        \"par_type\": {f\"{g}->{p}\": n\n                                     for (g, p), n in pos_par_ … [210 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "            \"pos_par_type\": {f\"{g}->{p}\": n\n                             for (g, p), n in pos_par_type_hard.most_common()},", "old_string": "            \"pos_par_type\": {f\ … [62 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/tests/linguistique/gold_reel_50.py --sortie reports/rapport-gold-reel-50.json", "description": "Run gold reel 50 measurement"}`

  ```
{
 "phrases": 452,
 "selection": 50,
 "global": 0.8891,
 "hard": 0.6842,
 "reste": 0.9198,
 "hard_f1": 0.5836,
 "hard_att": 0.9545,
 "part_pos": {
  "lot": 102,
  "total": 275,
  "part": 0.3709
 },
 "part_fn": {
  "lot": 87,
  "total": 346,
  "part": 0.2514
 },
 "part_att": {
  "lot": 1,
  "total": 1,
  "part": 1.0
 },
 "gold_intact": true,
 "sortie": "reports/rapport-gold-reel-50.json"
}
[stderr]

real	0m0,689s
user	0m0,654s
sys	0m0,036s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nprint('top keys',list(d))\nprint('objet',json.dumps(d['objet'],ensure_ascii=False,indent=1)[:1200])\nprint('\\nselection composition',d['selection … [1752 caractères tronqués]`

  ```
top keys ['date', 'ligne', 'tache', 'commit_mesure', 'objet', 'heuristique', 'selection', 'mesure', 'erreurs_hard_50', 'candidats_a_annoter', 'controles_negatifs', 'gold_intact', 'limites', 'ce_qui_ferait_faux', 'fichiers']
objet {
 "definition": "le gold linguistique réel (hand + reel) des fiches R/B13, et non le « gold de pensée » ; « 200+ » est un libellé obsolète (452 phrases) et ambigu (T15).",
 "phrases": 452,
 "hand": 20,
 "reel": 432,
 "tokens": 2480,
 "segments": 1501,
 "cibles_attachement": 184,
 "fichiers": {
  "tools/tests/linguistique/gold.json": "3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a",
  "tools/tests/linguistique/gold_reel.json": "05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11"
 }
}

selection composition {'sources': {'hand': 2, 'reel': 48}, 'langues': {'en': 25, 'fr': 25}, 'signatures_distinctes': 42, 'score_min': 3, 'score_max': 10}
ids ['g017', 'r034', 'r071', 'r076', 'r102', 'r104', 'r106', 'r119', 'r159', 'r163', 'r179', 'r217', 'r241', 'r246', 'r285', 'r287', 'r291', 'r293', 'r328', 'r362', 'r363', 'r366', 'r368', 'r370', 'r422', 'g004', 'r091', 'r203', 'r210', 'r225', 'r227', 'r255', 'r260', 'r261', 'r262', 'r266', '
… [5275 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "    simple, stratifie = [], []\n    for graine in range(tirages):\n        rng = random.Random(graine)\n        simple.append({\"graine\": graine, \"mesure\": metriques(rng.sample … [706 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "    hard_gn_gv = [x for x in gn_gv if x[\"dans_hard_50\"]]\n    autres_gn_gv = [x for x in gn_gv if not x[\"dans_hard_50\"]]\n    return {\n        \"priorite_1_attachement\": {\n … [2061 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "            \"tirage_simple\": \"50 phrases au hasard, 8 graines : le POS reste ≥ 85 %.\",", "old_string": "            \"tirage_simple\": \"50 phrases au hasard, 8 graines : le P … [32 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/gold_reel_50.py --sortie reports/rapport-gold-reel-50.json && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nprint('simple:')\nfor x in d['mesure']['controles'] … [800 caractères tronqués]`

  ```
{
 "phrases": 452,
 "selection": 50,
 "global": 0.8891,
 "hard": 0.6842,
 "reste": 0.9198,
 "hard_f1": 0.5836,
 "hard_att": 0.9545,
 "part_pos": {
  "lot": 102,
  "total": 275,
  "part": 0.3709
 },
 "part_fn": {
  "lot": 87,
  "total": 346,
  "part": 0.2514
 },
 "part_att": {
  "lot": 1,
  "total": 1,
  "part": 1.0
 },
 "gold_intact": true,
 "sortie": "reports/rapport-gold-reel-50.json"
}
simple:
  0 0.8685 0.8228 1.0 23
  1 0.8942 0.8 1.0 22
  2 0.8858 0.7622 1.0 16
  3 0.8678 0.7744 1.0 22
  4 0.85 0.8013 1.0 24
  5 0.9101 0.8385 1.0 20
  6 0.8796 0.8012 1.0 19
  7 0.8868 0.8267 1.0 26
stratifie:
  0 0.902 0.7706 1.0 22
  1 0.9048 0.828 1.0 16
  2 0.8942 0.8363 1.0 26
  3 0.8724 0.7795 1.0 21
  4 0.8838 0.7881 1.0 19
  5 0.8964 0.7368 0.95 20
  6 0.9077 0.8117 1.0 16
  7 0.8727 0.7375 1.0 16
majoritaire {'hard_50': {'classe': 'PRON', 'justes': 71, 'tokens': 323, 'exactitude': 0.2198}, 'global_452': {'classe': 'VERB', 'justes': 582, 'tokens': 2480, 'exactitude': 0.2347}}
uniforme {'hard_50': {'graine': 0, 'justes': 27, 'tokens': 323, 'exactitude': 0.0836}, 'global_452': {'graine': 0, 'justes': 237, 'tokens': 2480, 'exactitude': 0.0956}}
p2 exemples hard [('g004', 'GN', 'Il'), ('g0
… [602 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nprint('| # | id | src | lg | phrase | POS | FN | FP | att |')\nprint('|---:|---|---|---|---|---:|---:|---:|---:|')\nfor i,p in enumerate(sorted(d[ … [324 caractères tronqués]`

  ```
| # | id | src | lg | phrase | POS | FN | FP | att |
|---:|---|---|---|---|---:|---:|---:|---:|
| 1 | `g017` | hand | en | She said that she would come yesterday. | 0 | 1 | 1 | 1 |
| 2 | `r034` | reel | en | The book that I read is exciting. | 2 | 0 | 0 | 0 |
| 3 | `r071` | reel | en | The car drives fast. | 1 | 1 | 1 | 0 |
| 4 | `r076` | reel | en | They arrive tomorrow morning. | 1 | 1 | 1 | 0 |
| 5 | `r102` | reel | en | The rain falls since this morning. | 2 | 0 | 0 | 0 |
| 6 | `r104` | reel | en | We prepare dinner. | 1 | 2 | 1 | 0 |
| 7 | `r106` | reel | en | The children laugh loudly. | 1 | 2 | 1 | 0 |
| 8 | `r119` | reel | en | The tourists visit the museum. | 1 | 3 | 1 | 0 |
| 9 | `r159` | reel | en | The farmers grow wheat. | 1 | 2 | 1 | 0 |
| 10 | `r163` | reel | en | The students review their lessons. | 1 | 3 | 1 | 0 |
| 11 | `r179` | reel | en | The rain washes the streets. | 2 | 3 | 1 | 0 |
| 12 | `r217` | reel | en | The student whom I mention is absent. | 1 | 2 | 1 | 0 |
| 13 | `r241` | reel | en | The day when we left was beautiful. | 1 | 2 | 1 | 0 |
| 14 | `r246` | reel | en | The dog that barks is mean. | 2 | 2 | 1 | 0 |
| 15 | `r285` | reel | en | The table that
… [2828 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nph={}\nfor f in ['gold.json','gold_reel.json']:\n    for p in json.load(open('tools/tests/linguistique/'+f))['phrases' … [660 caractères tronqués]`

  ```
r324 Le livre est sur la table ; il est rouge.
 gold [('GN', 'Le livre', None), ('GV', 'est', None), ('GP', 'sur la table', None), ('GN', 'il', None), ('GV', 'est', None), ('ADJ', 'rouge', None)]
 pred [('GN', 'Le livre', {'segment': 'Le livre', 'cible': 'rouge'}), ('GV', 'est', {'segment': 'est', 'cible': 'livre'}), ('GP', 'sur la table', {'segment': 'sur la table', 'cible': 'rouge'}), ('GN', 'il', {'segment': 'il', 'cible': 'rouge'}), ('GV', 'est rouge', None)]
 POS gold [('Le', 'DET'), ('livre', 'NOUN'), ('est', 'VERB'), ('sur', 'PREP'), ('la', 'DET'), ('table', 'NOUN'), ('il', 'PRON'), ('est', 'AUX'), ('rouge', 'ADJ')]
 POS pred [('Le', 'DET'), ('livre', 'NOUN'), ('est', 'AUX'), ('sur', 'PREP'), ('la', 'DET'), ('table', 'ADJ'), (';', 'PONCT'), ('il', 'PRON'), ('est', 'AUX'), ('rouge', 'ADJ'), ('.', 'PONCT')]

 r328 The book is on the table; it is red.
 gold [('GN', 'The book', None), ('GV', 'is', None), ('GP', 'on the table', None), ('GN', 'it', None), ('GV', 'is', None), ('ADJ', 'red', None)]
 pred [('GN', 'The book', {'segment': 'The book', 'cible': 'red'}), ('GV', 'is', None), ('GP', 'on the table', {'segment': 'on the table', 'cible': 'red'}), ('GN', 'it', {'segment': 'it',
… [5954 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "        if not juste:\n            pos_erreurs.append({\"token\": m[\"texte\"], \"gold\": m[\"pos\"], \"predit\": pred,\n                                \"debut\": m[\"debut\"], \ … [701 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "    pos_par_type_global = collections.Counter()\n    genre_global = collections.Counter()\n    for r in rows:\n        for e in r[\"pos\"][\"erreurs\"]:\n            pos_par_type_ … [727 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "                \"pos\": {\"total\": somme(rows, \"pos\"),\n                        \"par_type\": {f\"{g}->{p}\": n\n                                     for (g, p), n in pos_par_ … [544 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "            \"pos_par_type\": {f\"{g}->{p}\": n\n                             for (g, p), n in pos_par_type_hard.most_common()},\n            \"pos_genre\": dict(genre_hard),", "o … [143 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "    targets = sum(r[\"attachement\"][\"cibles\"] for r in rows)\n    att_ok = sum(r[\"attachement\"][\"justes\"] for r in rows)\n    att_err = sum(len(r[\"attachement\"][\"erreurs … [375 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "        \"pos\": {\"exactitude\": round(pos_ok / max(1, pos_n), 4),\n                \"ferme\": round(okf / max(1, nf), 4), \"ouvert\": round(oko / max(1, no), 4),\n               … [615 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/gold_reel_50.py --sortie reports/rapport-gold-reel-50.json && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nfor k in ['global_452','hard_50','reste_402']:\n    … [381 caractères tronqués]`

  ```
{
 "phrases": 452,
 "selection": 50,
 "global": 0.8891,
 "hard": 0.6842,
 "reste": 0.9198,
 "hard_f1": 0.5836,
 "hard_att": 0.9545,
 "part_pos": {
  "lot": 102,
  "total": 275,
  "part": 0.3709
 },
 "part_fn": {
  "lot": 87,
  "total": 346,
  "part": 0.2514
 },
 "part_att": {
  "lot": 1,
  "total": 1,
  "part": 1.0
 },
 "gold_intact": true,
 "sortie": "reports/rapport-gold-reel-50.json"
}
global_452 exact 0.8891 tokenisation 66 etiquette 0.9134 err 275
hard_50 exact 0.6842 tokenisation 31 etiquette 0.7568 err 102
reste_402 exact 0.9198 tokenisation 35 etiquette 0.935 err 173
genre global {'etiquette': 209, 'tokenisation': 66}
genre hard {'etiquette': 71, 'tokenisation': 31}
gold intact True
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nfor kind in ['simple','stratifie']:\n    print(kind)\n    for x in d['mesure']['controles'][kind]:\n        m=x['mesure']; print(' ',x['graine'],' … [220 caractères tronqués]`

  ```
simple
  0 pos 0.8685 etiq 0.9094 tok 13 f1 0.8228 att 1.0
  1 pos 0.8942 etiq 0.9387 tok 13 f1 0.8 att 1.0
  2 pos 0.8858 etiq 0.9073 tok 6 f1 0.7622 att 1.0
  3 pos 0.8678 etiq 0.8951 tok 9 f1 0.7744 att 1.0
  4 pos 0.85 etiq 0.8848 tok 11 f1 0.8013 att 1.0
  5 pos 0.9101 etiq 0.9275 tok 5 f1 0.8385 att 1.0
  6 pos 0.8796 etiq 0.9163 tok 11 f1 0.8012 att 1.0
  7 pos 0.8868 etiq 0.9073 tok 6 f1 0.8267 att 1.0
stratifie
  0 pos 0.902 etiq 0.9144 tok 4 f1 0.7706 att 1.0
  1 pos 0.9048 etiq 0.9148 tok 3 f1 0.828 att 1.0
  2 pos 0.8942 etiq 0.9129 tok 6 f1 0.8363 att 1.0
  3 pos 0.8724 etiq 0.894 tok 7 f1 0.7795 att 1.0
  4 pos 0.8838 etiq 0.9161 tok 10 f1 0.7881 att 1.0
  5 pos 0.8964 etiq 0.9331 tok 11 f1 0.7368 att 0.95
  6 pos 0.9077 etiq 0.9291 tok 6 f1 0.8117 att 1.0
  7 pos 0.8727 etiq 0.8955 tok 7 f1 0.7375 att 1.0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nprint('commit',d['commit_mesure'],'date',d['date'])\nprint('objet',d['objet'])\nprint('heur global',json.dumps(d['heuristique']['global'],ensure_a … [607 caractères tronqués]`

  ```
commit f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888 date 2026-11-15 02:41 EST
objet {'definition': 'le gold linguistique réel (hand + reel) des fiches R/B13, et non le « gold de pensée » ; « 200+ » est un libellé obsolète (452 phrases) et ambigu (T15).', 'phrases': 452, 'hand': 20, 'reel': 432, 'tokens': 2480, 'segments': 1501, 'cibles_attachement': 184, 'fichiers': {'tools/tests/linguistique/gold.json': '3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a', 'tools/tests/linguistique/gold_reel.json': '05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11'}}
heur global {
 "phrases": 452,
 "tokens": 2480,
 "pos": {
  "exactitude": 0.8891,
  "ferme": 0.9294,
  "ouvert": 0.8466,
  "justes": 2205,
  "erreurs": 275,
  "tokenisation": 66,
  "etiquette_exactitude": 0.9134,
  "note": "`exactitude` compte la tokenisation ; `etiquette_exactitude` retire les tokens gold sans token prédit (« ? »)."
 },
 "segmentation": {
  "tp": 1155,
  "fp": 266,
  "fn": 346,
  "precision": 0.8128,
  "rappel": 0.7695,
  "f1": 0.7906
 },
 "segmentation_par_type": {
  "GN": {
   "tp": 557,
   "fp": 101,
   "fn": 124,
   "precision": 0.8465,
   "rappel": 0.8179,
   "f1": 0.832
  },
  "GV": {

… [6353 caractères tronqués]
  ```

### 🤖 Assistant

All measurements are in place. Now let me write the report.

- **write** `{"content": "# R0.7 / B13 — le gold réel étendu : 50 phrases que l'heuristique rate, et ce qu'elles disent\n\n> **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **B13** · **Tâche** : C3 (coordination R) ·\n> **Date** : 2026-11-15 · **HEAD mesuré** : `f926b5bc` · **Verdict** : ✅ **le gold rée … [25297 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nph=[]\nfor f in ['gold.json','gold_reel.json']:\n    for p in json.load(open('tools/tests/linguistique/'+f))['phrases']:\n        p['_src']='hand' if f=='gold.json' else 'reel'; ph.append(p)\nneg=[p for … [1733 caractères tronqués]`

  ```
neg sentences 11 ['r408', 'r409', 'r410', 'r411', 'r412', 'r413', 'r414', 'r415', 'r416', 'r417', 'r422']
selected neg ['r408', 'r409', 'r410', 'r422']
sel segments 190 tokens 323 targets 22
sentences with pos err 191 seg err 213 att err 1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "    part = {}\n    for nom in (\"pos\", \"fn\", \"att\"):\n        total = somme(rows, nom)\n        lot = somme(choisies, nom)\n        part[nom] = {\"lot\": lot, \"total\": tota … [569 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "            \"erreurs\": {\n                \"phrases_avec_pos\": phrases_avec[\"pos\"],\n                \"phrases_avec_segmentation\": phrases_avec[\"segmentation\"],\n          … [233 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "Le plafond empêche une construction de prendre le lot : les **11 négations** (10 françaises\n`r408`–`r417` + l'anglaise `r422`) sont ramenées à **4**. Sans le plafond, le top 50 serait\n** … [360 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "**L'unique erreur** : `g017` « She said that she would come yesterday. » — la cible est **bonne**\n(`said`), le span est **faux** : le gold a SUB `that she would come` (9–28), l'heuristiqu … [1025 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "**Ce que l'extension n'est pas** : 50 phrases de plus. Les 50 sont **déjà** dans le gold ; ce qui\nmanque, c'est leur **statut de test** et **10 cibles** — ou **154** si S accepte aussi la … [274 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/gold_reel_50.py --sortie reports/rapport-gold-reel-50.json && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nprint('phrases_avec', {k:d['heuristique']['erreurs' … [448 caractères tronqués]`

  ```
{
 "phrases": 452,
 "selection": 50,
 "global": 0.8891,
 "hard": 0.6842,
 "reste": 0.9198,
 "hard_f1": 0.5836,
 "hard_att": 0.9545,
 "part_pos": {
  "lot": 102,
  "total": 275,
  "part": 0.3709
 },
 "part_fn": {
  "lot": 87,
  "total": 346,
  "part": 0.2514
 },
 "part_att": {
  "lot": 1,
  "total": 1,
  "part": 1.0
 },
 "gold_intact": true,
 "sortie": "reports/rapport-gold-reel-50.json"
}
phrases_avec {'phrases_avec_pos': 191, 'phrases_avec_segmentation': 213, 'phrases_avec_attachement': 1}
gold_intact True
selection count 50 ids 50
candidats p1 10
COMPILE-OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nfor kind in ['simple','stratifie']:\n    vals=[(x['graine'],x['mesure']['tokens'],x['mesure']['attachement']['cibles']) for x in d['mesure']['cont … [211 caractères tronqués]`

  ```
simple tokens 254 295 targets 16 26 [(0, 289, 23), (1, 274, 22), (2, 254, 16), (3, 295, 22), (4, 280, 24), (5, 267, 20), (6, 274, 19), (7, 265, 26)]
stratifie tokens 260 296 targets 16 26 [(0, 296, 22), (1, 273, 16), (2, 293, 26), (3, 290, 21), (4, 284, 19), (5, 280, 20), (6, 260, 16), (7, 275, 16)]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "| phrases | 452 | 50 | 402 | 50 |\n| tokens | 2 480 | 323 | 2 157 | 260–296 |", "old_string": "| phrases | 452 | 50 | 402 | 50 |\n| tokens | 2 480 | 323 | 2 157 | 259–277 |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "Le lot dur **amplifie** les deux : GV F1 **45,00 %** (le pire des types **produits**), GN\n**67,11 %**, et 20 des 87 segments absents sont ADJ/ADV (structurels). Il reste **67 segments\nab … [288 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la .git/hooks/ | head -20 && echo \"=====\" && for f in .git/hooks/pre-commit .git/hooks/commit-msg; do if [ -f \"$f\" ]; then echo \"--- $f\"; cat \"$f\"; fi; done", "description": "Inspect git hooks"}`

  ```
total 68
drwxr-xr-x. 1 stephane stephane  576 31 oct 12:55 .
drwxr-xr-x. 1 stephane stephane  198 15 nov 02:34 ..
-rw-r--r--. 1 stephane stephane  478 25 sep 13:48 applypatch-msg.sample
-rw-r--r--. 1 stephane stephane 1972 25 sep 13:48 commit-msg.sample
-rw-r--r--. 1 stephane stephane 4611 25 sep 13:48 fsmonitor-watchman.sample
-rw-r--r--. 1 stephane stephane  189 25 sep 13:48 post-update.sample
-rw-r--r--. 1 stephane stephane  424 25 sep 13:48 pre-applypatch.sample
-rwxr-xr-x. 1 stephane stephane 1470 31 oct 12:55 pre-commit
-rw-r--r--. 1 stephane stephane 1649 25 sep 13:48 pre-commit.sample
-rw-r--r--. 1 stephane stephane  416 25 sep 13:48 pre-merge-commit.sample
-rw-r--r--. 1 stephane stephane 1492 25 sep 13:48 prepare-commit-msg.sample
-rw-r--r--. 1 stephane stephane 1374 25 sep 13:48 pre-push.sample
-rw-r--r--. 1 stephane stephane 4898 25 sep 13:48 pre-rebase.sample
-rw-r--r--. 1 stephane stephane  544 25 sep 13:48 pre-receive.sample
-rw-r--r--. 1 stephane stephane 2783 25 sep 13:48 push-to-checkout.sample
-rw-r--r--. 1 stephane stephane 2308 25 sep 13:48 sendemail-validate.sample
-rw-r--r--. 1 stephane stephane 3650 25 sep 13:48 update.sample
=====
--- .git/hooks/pre-commit
#
… [1433 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/revue_documentation.py", "description": "Read doc review script"}`

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
… [2953 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat 292c70b5 | head -30 && echo ===== && git show --stat 17932bca | head -30", "description": "Inspect C1/C2 commit stats"}`

  ```
commit 292c70b52a5656c16360db2570950abbe51c56b6
Author: Stéphane <stephane@localhost>
Date:   Sun Nov 15 02:13:09 2026 -0500

    C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09

 docs/pilotage/en-cours.md                          |   10 +-
 journal/2026-11-15/README.md                       |    6 +-
 journal/2026-11-15/docs.md                         |   19 +
 journal/2026-11-15/mesures.md                      |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    3 +-
 journal/THEMES.md                                  |    1 +
 journal/sessions/MANIFEST.md                       |    5 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   34 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 1514 ++++++++++++++++++++
 .../rapport.md                                     |  171 +++
 reports/INDEX.md                                   |    3 +-
 reports/README.md                                  |    1 +
 reports/rapport-coordination-n2-v2.json            |  247 ++++
 reports/rapport-coordina
… [1643 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/verifie_etat_a_jour.py", "description": "Read state freshness checker"}`

  ```
#!/usr/bin/env python3
"""verifie_etat_a_jour.py — aucun fait commité sans sa ligne d'état.

POURQUOI CET OUTIL EXISTE. `en-cours` est la seule source de l'état, et le contrat
disait « seul le principal écrit ». Ce n'est pas une garantie : l'identité se déduit
d'une variable d'environnement absente — un « pair » est autodéclaré — et si la
principale s'arrête, l'état se fige. Surtout, rien ne comparait les commits : la
revue ne regardait que la DATE, donc deux commits du même jour passaient. Le 29/10,
A8.0 (15 h 51) a été commité après le dernier état (15 h 34) sans aucune alerte.

La garantie est au commit, pas dans la discipline d'un écrivain :
  --index  (hook pre-commit) : un commit qui prépare un fait (reports/, roadmap,
           backlog) sans toucher `en-cours` est REFUSÉ ;
  --head   : si un fait a été commité après le dernier commit d'`en-cours`, l'état
           est en retard — la session qui le voit le corrige, sans attendre.

Le journal est du récit dérivé (le hook l'archive) : il n'exige pas de ligne d'état.

Usage :
  python3 tools/verifie_etat_a_jour.py             # --head
  python3 tools/verifie_etat_a_jour.py --index     # pour le hook
  python3 tools/verifie_eta
… [2088 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/revue_documentation.py 2>&1 | tail -60", "description": "Run documentation review"}`

  ```
revue de documentation · 738 fiche(s) · 831 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 737 fichiers, le disque en a 738
     · compteurs : en-cours.md dit 830 JSON, le disque en a 831
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md</path>
<type>file</type>
<content>
1: # R0.7 / B13 — le gold réel étendu : 50 phrases que l'heuristique rate, et ce qu'elles disent
2: 
3: > **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **B13** · **Tâche** : C3 (coordination R) ·
4: > **Date** : 2026-11-15 · **HEAD mesuré** : `f926b5bc` · **Verdict** : ✅ **le gold réel n'est pas un
5: > problème de nombre** (452 phrases, déjà > 200) : c'est un problème de **discrimination**. Les
6: > **50 phrases réelles les plus dures** (2 hand + 48 reel ; 25 fr + 25 en) portent **37,1 %** des
7: > erreurs POS et **25,1 %** des segments absents pour **11,1 %** des phrases ; l'heuristique y fait
8: > **68,42 %** de POS (étiquettes seules **75,68 %**) contre **91,98 %** sur le reste. L'attachement,
9: > lui, est **saturé** : **183/184** (une seule erreur, `g017`). L'extension utile est donc **un lot
10: > dur tenu à l'écart** + **10 cibles GP/SUB à annoter** (dont 4 dans le lot), **pas 50 phrases de
11: > plus**.
12: 
13: **En trois lignes.** (1) Le « gold 200+ » est **défini** : c'est le gold **linguistique** hand + reel
14: (452 phrases, 2 480 tokens,
… [26228 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "Le lot est **stable** tant que le POS pèse au moins **2** (et l'attachement **3**) ; il change si\nle POS tombe à **1** : c'est le signe que le lot est **piloté par le POS**, pas par le ha … [235 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "- **Pas une faute d'étiquette.** Les 66 `?` globaux (31 dans le lot) sont une **convention non\n  tranchée** (élision/trait d'union), pas une faute d'étiquette : le POS « hors tokenisation … [352 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "- **Commit (session principale)** : la fiche, le JSON et le script ; `git add` explicite. Le gold\n  **n'est pas** indexé (aucun fichier du gold n'est modifié) ; `en-cours`, `INDEX` et `RE … [234 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/eval-gold.json > /tmp/eval-gold.out 2>&1; echo \"exit=$?\"; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/eval-gold.json'))\nh=d['heuristique']\nfor k in ['all','re … [290 caractères tronqués]`

  ```
exit=0
all phrases 612 POS 0.8625 F1 0.7902 att 0.9958 238 / 239
reel phrases 452 POS 0.8891 F1 0.7906 att 0.9946 183 / 184
gold {'phrases': 612, 'reel': 452, 'hand': 20, 'reel_new': 432, 'synthetique': 160, 'tokens': 3179}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/revue_documentation.py 2>&1 | tail -20", "description": "Re-run doc review"}`

  ```
revue de documentation · 738 fiche(s) · 831 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 737 fichiers, le disque en a 738
     · compteurs : en-cours.md dit 830 JSON, le disque en a 831
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,re,pathlib\np=pathlib.Path('reports/rapport-gold-reel-50.md')\nt=p.read_text(encoding='utf-8')\nlinks=re.findall(r'\\]\\(([^)#]+?)\\)',t)\nfor l in links:\n    c=(p.parent/l).resolve()\n    print('OK' if … [81 caractères tronqués]`

  ```
OK rapport-file-taches.md
OK rapport-gold-reel-50.json
OK rapport-gold-reel-50.md
OK rapport-gold-reel-50.json
OK ../tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -30 && echo \"---\" && git diff --stat -- tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/bloc_linguistique.py", "description": "Check git status and gold unchanged"}`

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
?? reports/rapport-gold-reel-50.json
?? reports/rapport-gold-reel-50.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -lh reports/rapport-gold-reel-50.md reports/rapport-gold-reel-50.json tools/tests/linguistique/gold_reel_50.py && python3 -c \"import json; d=json.load(open('reports/rapport-gold-reel-50.json')); print('JSON OK', len(d), 'cles rac … [144 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 141K 15 nov 02:42 reports/rapport-gold-reel-50.json
-rw-------. 1 stephane stephane  26K 15 nov 02:43 reports/rapport-gold-reel-50.md
-rw-------. 1 stephane stephane  28K 15 nov 02:42 tools/tests/linguistique/gold_reel_50.py
JSON OK 15 cles racine
  442 reports/rapport-gold-reel-50.md
  587 tools/tests/linguistique/gold_reel_50.py
 1029 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l tools/tests/linguistique/qualifier_tagger_612.py tools/tests/linguistique/evaluer_gold.py reports/rapport-coordination-r.md reports/rapport-coordination-r.json", "description": "Check permissions of comparable files"}`

  ```
-rw-r--r--. 1 stephane stephane 13019 13 nov 22:35 reports/rapport-coordination-r.json
-rw-r--r--. 1 stephane stephane 22988 13 nov 22:36 reports/rapport-coordination-r.md
-rw-r--r--. 1 stephane stephane 15762  6 nov 19:50 tools/tests/linguistique/evaluer_gold.py
-rw-r--r--. 1 stephane stephane  8688 13 nov 22:02 tools/tests/linguistique/qualifier_tagger_612.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 644 reports/rapport-gold-reel-50.md reports/rapport-gold-reel-50.json tools/tests/linguistique/gold_reel_50.py && ls -l reports/rapport-gold-reel-50.md reports/rapport-gold-reel-50.json tools/tests/linguistique/gold_reel_50.py" … [47 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 143877 15 nov 02:42 reports/rapport-gold-reel-50.json
-rw-r--r--. 1 stephane stephane  25678 15 nov 02:43 reports/rapport-gold-reel-50.md
-rw-r--r--. 1 stephane stephane  28292 15 nov 02:42 tools/tests/linguistique/gold_reel_50.py
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "## 5. Les candidats à annoter\n\n**Principe.** Le gold ne peut pas être étendu par des phrases (elles y sont déjà) ; il peut l'être\npar des **cibles d'attachement**. Le gold courant a **0 … [784 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "offset": 250, "limit": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md</path>
<type>file</type>
<content>
250: 
251: ## 5. Les candidats à annoter
252: 
253: **Principe.** Le gold ne peut pas être étendu par des phrases (elles y sont déjà) ; il peut l'être
254: par des **cibles d'attachement**. Le gold courant a **0 cible** sur 1 233 GN/GV et **10 segments
255: GP/SUB sans cible** (9 GP + 1 SUB ; 0 REL). Ce sont eux qui manquent, pas des phrases.
256: 
257: ### 5.1 Priorité 1 — les 10 GP/SUB sans cible (attachement)
258: 
259: | # | id | type | segment | dans le lot dur | phrase |
260: |---:|---|---|---|---|---|
261: | 1 | `r267` | GP | `à moi` | non | Le livre qui est sur la table est à moi. |
262: | 2 | `r324` | GP | `sur la table` | **oui** | Le livre est sur la table ; il est rouge. |
263: | 3 | `r328` | GP | `on the table` | **oui** | The book is on the table; it is red. |
264: | 4 | `r336` | GP | `to her` | non | Paul sees Marie; he speaks to her. |
265: | 5 | `r342` | GP | `to her` | non | Paul sees Marie; he speaks to her; she listens. |
266: | 6 | `r349` | GP | `sur la table` | **oui** | Le livre est sur la table ; je le lis. |
267: | 7 | `r358` | GP | `to h
… [303 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "**Principe.** Le gold ne peut pas être étendu par des phrases (elles y sont déjà) ; il peut l'être\npar des **cibles d'attachement**. Le gold courant a **0 cible** sur 1 233 GN/GV et **10  … [718 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,re\nmd=open('reports/rapport-gold-reel-50.md',encoding='utf-8').read()\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nrows={p['id']:p for p in d['selection']['phrases']}\n# extract table rows a … [744 caractères tronqués]`

  ```
rows checked 50 mismatches 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,statistics\nd=json.load(open('reports/rapport-gold-reel-50.json'))\ng=d['mesure']['global_452']; h=d['mesure']['hard_50']; r=d['mesure']['reste_402']\n# projection\ntp=g['segmentation']['tp']+h['segmenta … [2198 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
KeyError: 'tokens'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,statistics\nd=json.load(open('reports/rapport-gold-reel-50.json'))\ng=d['mesure']['global_452']; h=d['mesure']['hard_50']; r=d['mesure']['reste_402']\ntp=g['segmentation']['tp']+h['segmentation']['tp']\n … [2161 caractères tronqués]`

  ```
projection POS 86.55 F1 76.82 att 99.03 F1 P/R 79.42 74.39
delta POS 2.36 F1 2.24 att 0.43
simple POS mean 88.03 min/max 85.0 91.01
   F1 mean 80.34 min/max 76.22 83.85
   att mean 100.0 min/max 100.0 100.0
   label mean 91.08 min/max 88.48 93.87
stratifie POS mean 89.18 min/max 87.24 90.77
   F1 mean 78.61 min/max 73.68 83.63
   att mean 99.38 min/max 95.0 100.0
   label mean 91.37 min/max 89.4 93.31
hard delta POS 23.56 F1 23.54 att 4.55
part phrases/tokens 11.06 13.02
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "**Projection (pas une mesure).** Si S ajoutait un **nouveau** lot de 50 phrases du **même profil**\n(le gold passerait à 502), les chiffres agrégés deviendraient : POS **86,55 %** (−2,36 p … [728 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "def projeter(global_: dict, hard: dict) -> dict:\n    \"\"\"Projection si un **nouveau** lot du même profil était ajouté (452 → 502).\n\n    Ce n'est **pas** une mesure : les 50 s … [1437 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py": file changed since it was read — re-read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "            \"part_des_erreurs\": part,\n            \"controles\": controler(rows, choisies),\n            \"sensibilite_poids\": sensibilite(rows, choisies),\n            \"proj … [273 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py": file changed since it was read — re-read the file, then retry
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def controler\\|def projeter\\|part_des_erreurs\\|sensibilite_poids\\|resultat = {\" tools/tests/linguistique/gold_reel_50.py", "description": "Locate lines to edit"}`

  ```
267:def controler(rows: list[dict], choisies: list[dict], tirages: int = 8) -> dict:
447:    resultat = {
512:            "part_des_erreurs": part,
514:            "sensibilite_poids": sensibilite(rows, choisies),
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "offset": 300, "limit": 40}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "offset": 500, "limit": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py</path>
<type>file</type>
<content>
300:     return {
301:         "simple": simple,
302:         "stratifie": stratifie,
303:         "majoritaire": {"hard_50": majoritaire(choisies), "global_452": majoritaire(rows)},
304:         "uniforme": {"hard_50": uniforme(choisies), "global_452": uniforme(rows)},
305:     }
306: 
307: 
308: def sensibilite(rows: list[dict], reference: list[dict]) -> list[dict]:
309:     """Le lot change-t-il quand on change les poids ? (contrôle de la règle)."""
310:     base = {r["id"] for r in reference}
311:     sorties = []
312:     for wa, wp, wf in ((3, 2, 1), (2, 2, 1), (5, 2, 1), (3, 3, 1), (3, 1, 1), (1, 1, 1)):
313:         # copie : `_rangs` réécrit `score` sur les objets, et le lot de référence doit garder
314:         # les scores du poids 3/2/1 pour la fiche.
315:         lot = {r["id"] for r in selectionner(copy.deepcopy(rows), wa, wp, wf)}
316:         sorties.append({"poids": f"{wa}/{wp}/{wf}", "commun": len(base & lot),
317:                         "jaccard": round(len(base & lot) / len(base | lot), 3)})
318:     return sorties
319: 
320: 
321: #
… [1045 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py</path>
<type>file</type>
<content>
500:                 "score_max": max(r["score"] for r in choisies),
501:             },
502:             "phrases": [{"id": r["id"], "source": r["source"], "langue": r["langue"],
503:                          "texte": r["texte"], "score": r["score"],
504:                          "pos_erreurs": len(r["pos"]["erreurs"]),
505:                          "segments_fn": len(r["segments"]["fn"]),
506:                          "segments_fp": len(r["segments"]["fp"]),
507:                          "att_erreurs": len(r["attachement"]["erreurs"])}
508:                         for r in choisies],
509:         },
510:         "mesure": {
511:             **mesures,
512:             "part_des_erreurs": part,
513:             "controles": controler(rows, choisies),
514:             "sensibilite_poids": sensibilite(rows, choisies),
515:         },
516:         "erreurs_hard_50": {
517:             "pos_par_type": {f"{g}->{p}": n
518:                              for (g, p), n in pos_par_type_hard.most_common()},
519:             "pos_genre": dict(genre_hard),
520:     
… [1339 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "def projeter(global_: dict, hard: dict) -> dict:\n    \"\"\"Projection si un **nouveau** lot du même profil était ajouté (452 → 502).\n\n    Ce n'est **pas** une mesure : les 50 s … [1437 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "            \"part_des_erreurs\": part,\n            \"controles\": controler(rows, choisies),\n            \"sensibilite_poids\": sensibilite(rows, choisies),\n            \"proj … [273 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m py_compile tools/tests/linguistique/gold_reel_50.py && python3 tools/tests/linguistique/gold_reel_50.py --sortie reports/rapport-gold-reel-50.json && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-re … [292 caractères tronqués]`

  ```
{
 "phrases": 452,
 "selection": 50,
 "global": 0.8891,
 "hard": 0.6842,
 "reste": 0.9198,
 "hard_f1": 0.5836,
 "hard_att": 0.9545,
 "part_pos": {
  "lot": 102,
  "total": 275,
  "part": 0.3709
 },
 "part_fn": {
  "lot": 87,
  "total": 346,
  "part": 0.2514
 },
 "part_att": {
  "lot": 1,
  "total": 1,
  "part": 1.0
 },
 "gold_intact": true,
 "sortie": "reports/rapport-gold-reel-50.json"
}
projection {"phrases": 502, "pos": 0.8655, "f1": 0.7682, "attachement": 0.9903, "delta_pos": -2.36, "delta_f1": -2.24, "delta_attachement": -0.43, "note": "projection, pas une mesure : les 50 sont déjà dans le gold."}
gold_intact True
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "limit": 20, "offset": 94}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "limit": 22, "offset": 250}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "limit": 12, "offset": 432}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md</path>
<type>file</type>
<content>
94: **Robustesse de la règle** (mêmes phrases quand on change les poids) :
95: 
96: | poids att/POS/segment | phrases communes au lot | Jaccard |
97: |---|---:|---:|
98: | **3 / 2 / 1** (référence) | **50** | 1,000 |
99: | 2 / 2 / 1 | **50** | 1,000 |
100: | 5 / 2 / 1 | **50** | 1,000 |
101: | 3 / 3 / 1 | 48 | 0,923 |
102: | 3 / 1 / 1 | 39 | 0,639 |
103: | 1 / 1 / 1 | 39 | 0,639 |
104: 
105: Le lot est **stable** tant que le POS pèse au moins **2** (et l'attachement **3**) ; il change si
106: le POS tombe à **1** : c'est le signe que le lot est **piloté par le POS**, pas par le hasard.
107: 
108: ## 3. Les erreurs du lot, par type
109: 
110: ### 3.1 POS : 102 erreurs, dont 31 de tokenisation
111: 
112: | mesure | global 452 | **lot dur 50** | reste 402 |
113: |---|---:|---:|---:|

(Showing lines 94-113 of 447. Use offset=114 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md</path>
<type>file</type>
<content>
250: 
251: ## 5. Les candidats à annoter
252: 
253: **Principe.** Le gold ne peut pas être étendu par des phrases (elles y sont déjà) ; il peut l'être
254: par des **cibles d'attachement**. Le gold courant a **0 cible** sur 1 233 GN/GV et **10 segments
255: GP/SUB sans cible** (9 GP + 1 SUB ; 0 REL). Ce sont eux qui manquent, pas des phrases.
256: 
257: **Le lot lui-même** est le **candidat de première ligne** : les 50 phrases sont déjà dans le gold,
258: mais elles n'ont **pas de statut de test** et 4 d'entre elles ont un GP sans cible. Le JSON les
259: liste dans `candidats_a_annoter.phrases_du_lot` ; S peut les **valider** (ou corriger) avant de les
260: tenir à l'écart.
261: 
262: ### 5.1 Priorité 1 — les 10 GP/SUB sans cible (attachement)
263: 
264: | # | id | type | segment | dans le lot dur | phrase |
265: |---:|---|---|---|---|---|
266: | 1 | `r267` | GP | `à moi` | non | Le livre qui est sur la table est à moi. |
267: | 2 | `r324` | GP | `sur la table` | **oui** | Le livre est sur la table ; il est rouge. |
268: | 3 | `r328` | GP | `on the table` | **oui
… [379 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md</path>
<type>file</type>
<content>
432: - **Lus, non modifiés** : `tools/tests/linguistique/gold.json` (sha256
433:   `3663be6c…`), `tools/tests/linguistique/gold_reel.json` (sha256 `05d4f6df…`),
434:   `tools/bloc_linguistique.py`.
435: - **Reproduire** :
436: 
437: ```bash
438: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
439: python3 tools/tests/linguistique/gold_reel_50.py \
440:   --sortie reports/rapport-gold-reel-50.json
441: # attendu : phrases 452, selection 50, global 0.8891, hard 0.6842,
442: #           reste 0.9198, hard_f1 0.5836, hard_att 0.9545, gold_intact true
443: ```

(Showing lines 432-443 of 447. Use offset=444 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "new_string": "> **50 phrases réelles dures** (2 hand + 48 reel ; 25 fr + 25 en ; les plus coûteuses, à\n> diversité plafonnée) portent **37,1 %** des erreurs POS et **25,1 %** des segments absents pour\ … [889 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md", "limit": 24}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md</path>
<type>file</type>
<content>
1: # R0.7 / B13 — le gold réel étendu : 50 phrases que l'heuristique rate, et ce qu'elles disent
2: 
3: > **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **B13** · **Tâche** : C3 (coordination R) ·
4: > **Date** : 2026-11-15 · **HEAD mesuré** : `f926b5bc` · **Verdict** : ✅ **le gold réel n'est pas un
5: > problème de nombre** (452 phrases, déjà > 200) : c'est un problème de **discrimination**. Les
6: > **50 phrases réelles dures** (2 hand + 48 reel ; 25 fr + 25 en ; les plus coûteuses, à
7: > diversité plafonnée) portent **37,1 %** des erreurs POS et **25,1 %** des segments absents pour
8: > **11,1 %** des phrases ; l'heuristique y fait **68,42 %** de POS (étiquettes seules **75,68 %**)
9: > contre **91,98 %** sur le reste. L'attachement, lui, est **saturé** : **183/184** (une seule
10: > erreur, `g017`). L'extension utile est donc **un lot dur tenu à l'écart** + **10 cibles GP/SUB à
11: > annoter** (dont 4 dans le lot), **pas 50 phrases de plus**.
12: 
13: **En trois lignes.** (1) Le « gold 200+ » est **défini** : c'est le gold **linguistique** hand + r
… [884 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"rapport-gold-reel-50\" reports/INDEX.md reports/README.md docs/ 2>/dev/null | head -10; echo \"---\"; grep -n \"orphelin\\|orphelins\" tools/revue_documentation.py | head -10", "description": "Check index references and or … [12 caractères tronqués]`

  ```
---
14:  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
80:    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins)."""
244:    # 7b. orphelins : tout document vivant doit avoir au moins un lien entrant
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '235,280p' tools/revue_documentation.py", "description": "Read orphan check"}`

  ```
texte = re.sub(r"\[[^\]]+\]\([^)]+\)", "", brut)
        for m in CHEMIN.finditer(texte):
            p = m.group(1).rstrip(".,;:)")
            if any(g in p for g in GABARIT):
                continue
            if not (RACINE / p).exists():
                ligne = texte[: m.start()].count("\n") + 1
                alertes.append(f"chemin mort : {f.relative_to(RACINE)}:{ligne} → {p}")

    # 7b. orphelins : tout document vivant doit avoir au moins un lien entrant
    entrants: set[pathlib.Path] = set()
    for f in sources_nav():
        try:
            texte = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for cible in liens(texte):
            if cible.startswith(("http://", "https://", "mailto:")):
                continue
            p = (f.parent / cible).resolve()
            if p.suffix == ".md":
                entrants.add(p)
    for p in docs_vivants():
        if p.resolve() not in entrants:
            alertes.append(f"navigation : {p.relative_to(RACINE)} n'a aucun lien entrant")

    # 7b bis. les fiches glossaire sont toutes listées dans l'index du dossier
    cartes = sorted((RACINE / "docs/theorie/glossaire/en
… [775 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"737\\|830\\|fichiers / JSON\" docs/pilotage/en-cours.md | head -10", "description": "Locate counters in en-cours"}`

  ```
106:| fichiers / JSON de résultats | **737** / **830** | `reports/*.md` / `reports/*.json` |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/chantier/ && grep -rn \"commit\\|acceptation\" tools/chantier/*.py 2>/dev/null | head -30", "description": "Inspect chantier supervisor"}`

  ```
plan.json
superviseur.py
6:plusieurs jours : file de tâches persistante, vérification d'acceptation **indépendante** de
10:1. **Une tâche n'est finie que si son acceptation passe** — une commande, un attendu, exécutés par
15:   tâches) arrête la boucle ; l'agent n'est jamais tué au milieu d'un commit.
20:    python3 tools/chantier/superviseur.py executer      # exécute UNE tâche (agent + acceptation)
92:# ------------------------------------------------------------------ acceptation
94:def verifier_acceptation(tache: dict) -> tuple[bool, list[str]]:
95:    """Exécute les commandes d'acceptation de la tâche ; rend (ok, détails)."""
97:    for test in tache.get("acceptation", []):
124:    vérifier, après la tâche, qu'un commit a bien été produit.
136:    """Lance l'agent sur le mandat, puis vérifie l'acceptation. Rend le résultat."""
150:                "acceptation": ["clé DeepSeek absente"], "sortie_agent": "", "cle": False}
160:    ok, details = verifier_acceptation(tache)
161:    # l'acceptation **prime** : un agent qui a fini son travail (fiche + portes) puis dépasse le
166:                "acceptation": details, "sortie_agent": sortie[-1500:]}
194:    for a in t.get("acceptatio
… [179 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '110,180p' tools/chantier/superviseur.py && echo \"=====\" && sed -n '210,240p' tools/chantier/superviseur.py", "description": "Read supervisor acceptance/commit logic"}`

  ```
details.append(f"❌ {commande} → code {r.returncode} (attendu {test['code']})")
        elif attendu and attendu not in sortie:
            ok = False
            details.append(f"❌ {commande} → « {attendu} » absent")
        else:
            details.append(f"✅ {commande}")
    return ok, details


def git_avant() -> dict:
    """L'état git **avant** la tâche : HEAD et fichiers modifiés (note, jamais blocage).

    Un dépôt multi-sessions n'est jamais propre : d'autres sessions écrivent `reports/` et
    `journal/` en continu. Le superviseur n'exige pas un worktree propre ; il note le HEAD pour
    vérifier, après la tâche, qu'un commit a bien été produit.
    """
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=RACINE,
                          capture_output=True, text=True).stdout.strip()
    r = subprocess.run(["git", "status", "--porcelain"], cwd=RACINE, capture_output=True, text=True)
    modifies = [l for l in r.stdout.splitlines() if l.strip()]
    return {"head": head, "modifies": modifies[:10]}


# ------------------------------------------------------------------ exécution

def executer_tache(tache: dict, etat: dict, timeout_s: int) -> dict:
    """Lance l'age
… [3864 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test -f reports/rapport-gold-reel-50.md && echo FICHE-OK && test -f reports/rapport-gold-reel-50.json && echo JSON-OK && test -f tools/tests/linguistique/gold_reel_50.py && echo SCRIPT-OK && git diff --quiet -- tools/tests/linguistiq … [119 caractères tronqués]`

  ```
FICHE-OK
JSON-OK
SCRIPT-OK
GOLD-INTACT
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '\"signatures_distinctes\"\\|\"score_min\"\\|\"score_max\"' tools/tests/linguistique/gold_reel_50.py", "description": "Locate composition block"}`

  ```
524:                "signatures_distinctes": len({r["signature"] for r in choisies}),
525:                "score_min": min(r["score"] for r in choisies),
526:                "score_max": max(r["score"] for r in choisies),
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "limit": 14, "offset": 518}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py</path>
<type>file</type>
<content>
518:                      "au plus 2 phrases par signature d'erreur ; départage par id.",
519:             "phrases": len(choisies),
520:             "ids": [r["id"] for r in choisies],
521:             "composition": {
522:                 "sources": dict(collections.Counter(r["source"] for r in choisies)),
523:                 "langues": dict(collections.Counter(r["langue"] for r in choisies)),
524:                 "signatures_distinctes": len({r["signature"] for r in choisies}),
525:                 "score_min": min(r["score"] for r in choisies),
526:                 "score_max": max(r["score"] for r in choisies),
527:             },
528:             "phrases": [{"id": r["id"], "source": r["source"], "langue": r["langue"],
529:                          "texte": r["texte"], "score": r["score"],
530:                          "pos_erreurs": len(r["pos"]["erreurs"]),
531:                          "segments_fn": len(r["segments"]["fn"]),

(Showing lines 518-531 of 614. Use offset=532 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py", "new_string": "            \"composition\": {\n                \"sources\": dict(collections.Counter(r[\"source\"] for r in choisies)),\n                \"langues\": dict(collections.Counter(r[\ … [979 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m py_compile tools/tests/linguistique/gold_reel_50.py && python3 tools/tests/linguistique/gold_reel_50.py --sortie reports/rapport-gold-reel-50.json > /tmp/gold50.out && cat /tmp/gold50.out && python3 - <<'PY'\nimport json\n … [351 caractères tronqués]`

  ```
{
 "phrases": 452,
 "selection": 50,
 "global": 0.8891,
 "hard": 0.6842,
 "reste": 0.9198,
 "hard_f1": 0.5836,
 "hard_att": 0.9545,
 "part_pos": {
  "lot": 102,
  "total": 275,
  "part": 0.3709
 },
 "part_fn": {
  "lot": 87,
  "total": 346,
  "part": 0.2514
 },
 "part_att": {
  "lot": 1,
  "total": 1,
  "part": 1.0
 },
 "gold_intact": true,
 "sortie": "reports/rapport-gold-reel-50.json"
}
composition {'sources': {'hand': 2, 'reel': 48}, 'langues': {'en': 25, 'fr': 25}, 'signatures_distinctes': 42, 'score_min': 3, 'score_max': 10, 'tokens': 323, 'segments': 190, 'cibles_attachement': 22}
gold_intact True
projection {'phrases': 502, 'pos': 0.8655, 'f1': 0.7682, 'attachement': 0.9903, 'delta_pos': -2.36, 'delta_f1': -2.24, 'delta_attachement': -0.43, 'note': 'projection, pas une mesure : les 50 sont déjà dans le gold.'}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,re\nmd=open('reports/rapport-gold-reel-50.md',encoding='utf-8').read()\nd=json.load(open('reports/rapport-gold-reel-50.json'))\nrows={p['id']:p for p in d['selection']['phrases']}\nsec=md.split('## 6.')[ … [1090 caractères tronqués]`

  ```
table rows 50 mismatches []
global/hard/reste POS 0.8891 0.6842 0.9198
hard F1/att 0.5836 0.9545
candidates 10 144
gold intact True
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"gold-reel-50|gold_reel_50\" && echo \"--- gold diff ---\" && git diff --stat -- tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json && echo \"--- acceptance ---\" && test -f repor … [91 caractères tronqués]`

  ```
?? reports/rapport-gold-reel-50.json
?? reports/rapport-gold-reel-50.md
?? tools/tests/linguistique/gold_reel_50.py
--- gold diff ---
--- acceptance ---
FICHE-OK
  ```

### 🤖 Assistant

## C3 livré — le gold réel étendu

**Fiche** : `reports/rapport-gold-reel-50.md` · **JSON** : `reports/rapport-gold-reel-50.json` · **Script reproductible** : `tools/tests/linguistique/gold_reel_50.py` · **Acceptation** : `FICHE-OK`.

### Le résultat en chiffres

| mesure | global 452 | **lot dur 50** | reste 402 | hasard stratifié (8 graines) |
|---|---:|---:|---:|---:|
| POS exact | 88,91 % | **68,42 %** | 91,98 % | 87,24–90,77 % |
| POS hors tokenisation | 91,34 % | **75,68 %** | 93,50 % | 89,40–93,31 % |
| F1 syntagmes | 79,06 % | **58,36 %** | 81,90 % | 73,68–83,63 % |
| attachement | 183/184 | **21/22** | 162/162 | 95,0–100 % |

Le lot fait **11,1 %** des phrases mais porte **37,1 %** des erreurs POS (102/275), **25,1 %** des segments absents (87/346) et **100 %** de l'erreur d'attachement (1/1). Il est **hors** des contrôles pour le POS et la F1 ; il ne l'est **pas** pour l'attachement.

### Ce que ça dit

- **« gold 200+ » est défini** : c'est le gold **linguistique** hand + reel (452 phrases, 2 480 tokens, 184 cibles), pas le gold de pensée. Le libellé « 200+ » est obsolète et ambigu (T15) : le gold fait déjà 452 phrases.
- **L'attachement est saturé** (183/184). L'unique erreur est `g017` : SUB `that she would come` (gold 9–28) prédit `that she would come yesterday` (9–38) — la cible `said` est **bonne**, seul le span est faux. Ajouter des phrases ne testera pas l'attachement : il faut **annoter des cibles**.
- **L'extension utile n'est pas 50 phrases de plus** : c'est un **lot dur tenu à l'écart** (les 50 y sont déjà) + **10 cibles GP/SUB** (9 GP + 1 SUB, dont 4 dans le lot), qui font passer le dénominateur d'attachement de **184 à 194**. Priorité 2 facultative : les **144 GN/GV** du lot (79 GN + 65 GV), soit 338 cibles au total.
- **Sélection déterministe** : score `3×att + 2×POS + 1×segment absent`, 25 fr + 25 en, au plus 2 par signature d'erreur (42 signatures). Sans le plafond : 43 fr / 7 en, monoculture de négations. Sensibilité : 50/50 avec 2/2/1 et 5/2/1, 48/50 avec 3/3/1, 39/50 si le POS tombe à poids 1.

### Contrôles et honnêteté

- **Hasard** : 50 simples (POS 85,00–91,01 %) et 50 stratifiées (87,24–90,77 %) ; le lot dur (68,42 %) est sous les deux.
- **Planchers** : majoritaire 21,98 % (lot) / 23,47 % (global) ; uniforme 8,36 % / 9,56 %.
- **Tokenisation** : 31 des 102 erreurs POS du lot sont des fusions d'élision/trait d'union (`j'ai`, `qu'il`, `viens-tu`), pas des fautes d'étiquette — c'est nommé dans la fiche.
- **Gold intact** : `gold.json` et `gold_reel.json` inchangés (sha256 avant/après identiques, `git diff` vide, `GOLD-INTACT`).
- **Projection** (pas une mesure) si 50 nouvelles phrases du même profil : POS 86,55 % (−2,36), F1 76,82 % (−2,24), attachement 99,03 % (−0,43).

### Reste

- **Non committé** : les trois fichiers sont prêts ; `en-cours`, `reports/INDEX.md`, `reports/README.md` et le commit relèvent de la session principale (comme C1/C2). La revue de documentation ne signale que les compteurs attendus : **737→738 fiches, 830→831 JSON**.
- **Prochaine mesure** : le tagger sur H50 (cache chaud puis API), et une règle qui améliore H50 **sans** dégrader le reste 402 — sinon c'est du sur-apprentissage.

