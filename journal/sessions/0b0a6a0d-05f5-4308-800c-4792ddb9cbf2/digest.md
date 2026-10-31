# Session DSH — relecture

- identifiant : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-31 17:17:48
- agent : standard


## Tour 1

### 👤 Utilisateur

continue

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
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le projet a pour principe que la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. Bref, révolutionner l'IA avec une approche par bus d'événements où chaque bloc fonctionnel est optimisable, comparable et substituable par des alternatives ayant des architectures différentes. e.g. Blocs neuronaux là où l'intuition est un avantage, blocs computationnels classiques pour les opérations où l'informatique classique est plus fiable et performante.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de
les **combiner**, de les **décomposer en couches et grappes de neurones** exécutables par du matériel divers, voire
**distribué en réseau**, de les **diagnostiquer et faire évoluer** en étudiant leurs **flux**, et de **rejouer à
volonté** des événements.


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

⏵ Checking the current session goal before resuming work

- **get_goal** `{}`

  ```
{"goal":null}
  ```

### 🤖 Assistant

⏵ Reading current state and recent history to resume correctly

- **bash** `{"command": "git status --short && echo \"---BRANCH---\" && git branch --show-current && echo \"---LOG---\" && git log --oneline -12", "description": "Show git status and recent commits"}`

  ```
M journal/README.md
 m tools/docwatch
---BRANCH---
master
---LOG---
9f1dcaae N2 — LES POINTS DE CONTRÔLE SONT CONSERVÉS SUR DEUX DISQUES (1,4 GO, EMPREINTES VÉRIFIÉES)
660c479c N2 — LA HIÉRARCHIE NE PAIE PAS SUR LA DISTILLATION NON PLUS (2,9935 CONTRE 2,9927, TROIS GRAINES)
48243e3d RÉFÉRENCES — LA PASSE DU 31 ENTRE EN TÊTE, LA PAGE RESTE SOUS SON BUDGET (2 489 MOTS)
4442c64c N2 — L'ÉTAT DE SECTION NE SE DISTINGUE PAS D'UN ÉTAT ÉTRANGER (+0,36 % CONTRE +0,37 %)
3b9d179c PORTES — CINQ ÉCHECS SILENCIEUX CORRIGÉS : UNE PASSE VIDE, UNE ASSERTION PERDUE, UN HOOK MUET
93f094e5 GRAPHE — LE PARSEUR PERDAIT LES LIENS MARKDOWN : 42 ARÊTES DEVENAIENT 43, LA FRONTIÈRE PASSAIT DE 12 À 4
2edb3079 JEUX — LE SAN L'EMPORTE SUR LA CASE QUAND UNE POSITION EST FOURNIE (110/112 → 112/112)
a2344c84 ÉTAT — LA CLÔTURE `eff8d8e4` ACTÉE, `22e518ee` CLOSE, N2 DÉSIGNÉE
eff8d8e4 SESSIONS — 104 ARCHIVES RETROUVÉES, CINQ CLÔTURES, L'ÉTAT À UNE SEULE SESSION
f590d884 DOCS — CONTINUITÉ 1 134 MOTS, ORGANISATION 1 579 : T0 3 989
b33b56ab LA CARTE DE DÉCISION DES CHANTIERS — LA PROFONDEUR DE DÉPENDANCE COMME AXE, LES SOURCES NOMMÉES
21a361f9 R13.4 — DEUX GRAINES : BPE512 DANS LE BRUIT, BPE1024 PERD 4,09 %
  ```

- **bash** `{"command": "wc -l docs/pilotage/en-cours.md docs/pilotage/roadmap.md 2>/dev/null; echo \"---\"; ls -la journal/ 2>/dev/null | tail -8", "description": "Check state file sizes and recent journal"}`

  ```
142 docs/pilotage/en-cours.md
  341 docs/pilotage/roadmap.md
  483 total
---
drwxr-xr-x. 1 stephane stephane   290 28 oct 14:11 2026-10-27
drwxr-xr-x. 1 stephane stephane   216 28 oct 14:06 2026-10-28
drwxr-xr-x. 1 stephane stephane   208 29 oct 17:08 2026-10-29
drwxr-xr-x. 1 stephane stephane   150 31 oct 11:22 2026-10-30
drwxr-xr-x. 1 stephane stephane   124 31 oct 17:03 2026-10-31
-rw-r--r--. 1 stephane stephane 30813 31 oct 17:17 README.md
drwxr-xr-x. 1 stephane stephane  7504 31 oct 11:23 sessions
-rw-r--r--. 1 stephane stephane 26647 31 oct 17:03 THEMES.md
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-10-31, 17 h 15 HAE (heure locale, EDT).**
4: 
5: > **État courant, pas histoire.** Une sous-section par **session active** ; une ligne par **chantier** avec son
6: > **bloquant**. Les détails de méthode sont dans [`methode/`](../methode/) — chargement et budget dans
7: > [`contexte.md`](../methode/contexte.md), contrat des sessions dans [`continuite.md`](../methode/continuite.md).
8: > Les résultats sont dans [`reports/`](../../reports/) ; l'histoire dans
9: > [`journal/`](../../journal/) ; le plan dans [`roadmap.md`](roadmap.md).
10: 
11: ## Sessions en cours
12: 
13: > Contrat et budget : [`continuite.md`](../methode/continuite.md) ; sessions terminées :
14: > [`journal/sessions/`](../../journal/sessions/).
15: 
16: > **Plan d'abord.** Chaque session active expose son mandat dans
17: > [`journal/sessions/`](../../journal/sessions/) (`<id>/plan.md`) ; `python3 tools/sessions.py --status`
18: > avant d'écrire ici.
19: 
20: > **Écriture.** Toute session écrit l'état, **une à la fois** : un commit est atomique, et
21: > aucun 
… [8789 caractères tronqués]
  ```

- **bash** `{"command": "git diff --stat; echo \"=== journal README diff ===\"; git diff journal/README.md | head -60; echo \"=== submodule ===\"; git diff tools/docwatch | head -20; cd tools/docwatch 2>/dev/null && git status --short | head -20", "description": "Inspect uncommitted changes"}`

  ```
journal/README.md | 2 +-
 tools/docwatch    | 0
 2 files changed, 1 insertion(+), 1 deletion(-)
=== journal README diff ===
diff --git a/journal/README.md b/journal/README.md
index 214341ab..01fbf1cf 100644
--- a/journal/README.md
+++ b/journal/README.md
@@ -13,7 +13,7 @@ chaque rapport renvoie à son jour et à `en-cours`.
 
 | jour | index | thèmes |
 |---|---|---|
-| **2026-10-31** | [2026-10-31/README.md](2026-10-31/README.md) | [distribue](2026-10-31/distribue.md) · [docs](2026-10-31/docs.md) · [modele](2026-10-31/modele.md) · [portes](2026-10-31/portes.md) |
+| **2026-10-31** | [2026-10-31/README.md](2026-10-31/README.md) | [apprentissage](2026-10-31/apprentissage.md) · [distribue](2026-10-31/distribue.md) · [docs](2026-10-31/docs.md) · [modele](2026-10-31/modele.md) · [portes](2026-10-31/portes.md) |
 | **2026-10-30** | [2026-10-30/README.md](2026-10-30/README.md) | [distribue](2026-10-30/distribue.md) · [docs](2026-10-30/docs.md) · [memoire](2026-10-30/memoire.md) · [mesures](2026-10-30/mesures.md) · [modele](2026-10-30/modele.md) · [moteur](2026-10-30/moteur.md) · [portes](2026-10-30/portes.md) |
 | **2026-10-29** | [2026-10-29/README.md](2026-10-29/README.md) | [attention](
… [1240 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/sessions.py --status 2>&1 | head -40", "description": "Check session status"}`

  ```
sessions · plans de mandat
    0b69f616-5c75-4c34 · terminé  · 1158 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
    22e518ee-81b8-4081 · terminé  · 329 min · archives de sessions, journal, en-cours, roadmap, backlog, outillage d'archivage
      → clôture committée (`eff8d8e4`) — session close ; la suite est **N2** (la hiérarchie), portée par la session à ouvrir
    71d57f53-8b41-4220 · terminé  · 1662 min · docs/pilotage/en-cours.md, docs/methode/continuite.md, tools/sessions.py
      → aucune — coordination close ; les trois plans migrés et les sessions archivées par `22e518ee`.
    8156fdcb-5033-4ba4 · terminé  · 1666 min · R0.1–R0.5
      → la boucle de lecture (R11, dépend de N2) ou la restitution (R31, dépend de R21) — toutes deux hors R0 ; sinon consolidation.
    N2-GPU             · terminé  · 1694 min · N2
      → N2 — la **hiérarchie** (état de section), porte **< 2,5** (meilleur **2,6998**, plateau **2,708**) ; **N5 gelé**.
    c3d0f0bd-e344-4600 · terminé  · 1921 min · R4.1–R4.3, B10.2bis, A8.3b
      → **B10.2bis** suite (encodeur) ; **A8.3b** ; **R4.4 bloqué**.
  ```

- **bash** `{"command": "ls journal/2026-10-31/; echo \"=== git log for apprentissage ===\"; git log --oneline -3 -- journal/2026-10-31/apprentissage.md; echo \"=== status ===\"; git status --short journal/", "description": "Check today's journal files"}`

  ```
apprentissage.md
distribue.md
docs.md
modele.md
portes.md
README.md
=== git log for apprentissage ===
9f1dcaae N2 — LES POINTS DE CONTRÔLE SONT CONSERVÉS SUR DEUX DISQUES (1,4 GO, EMPREINTES VÉRIFIÉES)
=== status ===
 M journal/README.md
  ```

- **bash** `{"command": "grep -n \"N2\" docs/pilotage/roadmap.md | head -40", "description": "Find N2 section in roadmap"}`

  ```
32:| **N — le natif** | DRVM, `drave-n0`, distillation, usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2 plafonne à 2,708 ; N4 partiel | **N2** (la hiérarchie), **N4** (consigne courte) |
33:| **R — le lecteur** | document, politique de lecture, fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R4.1–R4.3 mesurées** | **R4.4 bloqué** (OCR) ; R1/R2/R3 attendent N2 |
46:2. **N2 — la distillation et la hiérarchie** (en cours) : 49 999 fenêtres, 4 sources ; professeur 30k **1,734**
48:   atteinte**. Le levier retenu est la **hiérarchie** (état de section), portée par N2.
52:5. **R11/R12 — la fenêtre** : après N2 ; PPL à 1 000 octets et aiguille native.
85:[N2] lasts 4 days and is 30% complete and is colored in #b26a00
100:[N2] starts at [N0/N1]'s end
101:[N4] starts at [N2]'s end
169:| **N2** | la distillation : 49 999 fenêtres, 4 sources, professeur Qwen/DeepSeek | 🔬 | **N2** — la **hiérarchie** (état de section, 3 graines) ; porte **< 2,5** non atteinte (meilleur **2,6998**, plateau **2,708**) |
205:| **R1 — la fenêtre native** | contexte hiérarchique, curriculum, tokenisation | PPL à 1 000 octets, aiguille native, stabilité
… [352 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 40,60p docs/pilotage/roadmap.md; echo \"=== 160,180 ===\"; sed -n 160,180p docs/pilotage/roadmap.md", "description": "Read roadmap N2 details"}`

  ```
30 % sur 5 types et **249 questions**) ; **R0.4** (tête de survol) et **R0.5** (routeur) sont
   **closes en négatif** — 0,540 contre BM25 0,720 sur le corpus gelé, et un signal qui prédit
   (AUC 0,839) sans règle qui transfère.
   **R4.1 — le bloc tableaux** est **mesurée** (996 cellules, **802** exactes, texte plat **0/3**),
   **R4.2 — le bloc code** aussi (294 fichiers, 24/24 extraits, texte seul **0/3**) et **R4.3 —
   le bloc maths** (32 formules, 10/10 dérivées, surface **0/3**) ; **R4.4 est bloqué** (OCR).
2. **N2 — la distillation et la hiérarchie** (en cours) : 49 999 fenêtres, 4 sources ; professeur 30k **1,734**
   (0,794 bit/octet) ; student **3,123** à 20 000 pas ; meilleur **2,6998** ; plateau **2,708** ; porte **< 2,5 non
   atteinte**. Le levier retenu est la **hiérarchie** (état de section), portée par N2.
3. ~~N0.3b — la parité de perplexité DRVM ↔ GGUF~~ **close** : conversion **68,1917 / 92,1875**, natif **4,6585 / 18,6394**.
4. **N4 — l'usage** : la **consigne courte** tenue à l'écart ; SFT **24/24 vus, 0/4 tenus** ; service 69 octets /
   611 ms. La restitution depuis un document lu est **R31**.
5. **R11/R12 — la fenêtre** : après N2 ; PPL à 1 000 octets et 
… [2938 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ | grep -i n2; echo \"=== scripts ===\"; ls tools/ | head -50; echo \"=== models ===\"; ls models/ 2>/dev/null | head", "description": "List N2 reports and tooling"}`

  ```
-rw-r--r--. 1 stephane stephane    2487 31 oct 16:37 n2-distillation.json
-rw-r--r--. 1 stephane stephane    7376 31 oct 12:57 n2-hierarchie.json
-rw-------. 1 stephane stephane    6036 31 oct 17:01 rapport-n2-distillation.md
-rw-------. 1 stephane stephane    4620 31 oct 12:58 rapport-n2-hierarchie.md
-rw-------. 1 stephane stephane   56947 16 oct 03:19 rapport-vision-qwen2vl.md
=== scripts ===
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
calibr
… [231 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-n2-distillation.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n2-distillation.md</path>
<type>file</type>
<content>
1: # N2 — la hiérarchie ne paie pas non plus sur le dispositif de distillation
2: 
3: > **Ligne de roadmap** : N2 (la hiérarchie) · **Date** : 2026-10-31 · **Verdict** : ❌ **négatif** —
4: > à budget strictement égal, l'état de section transporté entre segments ne bat pas le modèle nu :
5: > **2,9935 contre 2,9927** (protocole segmenté, trois graines). L'écart, **+0,029 %**, est du même
6: > ordre que la dispersion entre graines.
7: 
8: ## La question
9: 
10: N2 plafonne à **2,6998** et le contexte s'arrête à 129 octets. Le levier retenu par la roadmap est
11: la **hiérarchie** — un état de section qui résume les octets lus et se transporte d'un segment au
12: suivant. Une première ablation, sur le petit corpus (`rapport-n2-hierarchie.md`), avait rendu un
13: négatif net : état **3,9759** contre témoin **3,9617**, et surtout **confondu avec un état
14: étranger** (3,9764). Il fallait refaire la mesure sur le **vrai dispositif de N2** : professeur
15: byte-level, distillation, 11,5 M d'élève.
16: 
17: ## Le dispositif — reconstruit, parce que tout avait disparu
… [5160 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"curriculum\" tools/ docs/ reports/ --include=*.py --include=*.md | head -20; echo \"=== distiller ===\"; ls -la tools/distiller*.py tools/eval_n2.py 2>/dev/null", "description": "Find curriculum references and distiller scripts"}`

  ```
tools/tests/documents/corpus/tableau/dependances.md
tools/tests/documents/corpus/tableau/index.md
tools/tests/documents/corpus/tableau/roadmap.md
tools/tests/documents/corpus/prose/lecture-rapide.md
docs/archive/roadmap-native-2026-10-29.md
docs/pilotage/backlog/R12-curriculum-contexte.md
docs/pilotage/backlog/index.md
docs/pilotage/backlog/dependances.md
docs/pilotage/roadmap.md
docs/pilotage/en-cours.md
docs/theorie/glossaire/README.md
docs/theorie/glossaire/12-la-lecture-le-document-et-ses-mesures.md
docs/theorie/lecture-rapide.md
reports/INDEX.md
reports/rapport-native-distillation.md
reports/rapport-native-ctx256.md
reports/rapport-native-ctx160.md
reports/rapport-native-ctx136.md
reports/rapport-native-ctx130.md
reports/rapport-native-ctx129.md
=== distiller ===
-rw-r--r--. 1 stephane stephane 5759 29 oct 04:27 tools/distiller_natif.py
-rwxr-xr-x. 1 stephane stephane 9496 31 oct 15:44 tools/distiller_section.py
-rwxr-xr-x. 1 stephane stephane 3676 31 oct 16:37 tools/eval_n2.py
  ```

- **bash** `{"command": "nvidia-smi --query-gpu=name,memory.total,memory.used,utilization.gpu --format=csv 2>&1; echo \"=== disk ===\"; df -h /home/stephane/Data13TB 2>/dev/null | tail -2", "description": "Check GPU availability"}`

  ```
name, memory.total [MiB], memory.used [MiB], utilization.gpu [%]
Quadro RTX 5000, 16384 MiB, 1 MiB, 0 %
Quadro RTX 5000, 16384 MiB, 1 MiB, 0 %
=== disk ===
Filesystem               Size  Used Avail Use% Mounted on
/dev/mapper/system-root   11T  8,9T  2,0T  82% /home/stephane/Data13TB
  ```

- **bash** `{"command": "cat docs/pilotage/backlog/R12-curriculum-contexte.md", "description": "Read R12 curriculum backlog card"}`

  ```
# R12 — Curriculum de contexte long (129 → 1 000 octets)

> **Statut** : spécifiée · **Priorité** : P1 · **Programme** : R · **Dépend de** : R11 · **Contraint par** : les cinq négatifs 129–256
> **Ligne de roadmap** : R1.2 · **Fiche de résultat attendue** : rapport-r12-curriculum-contexte.md (à créer dans `reports/`)
> **Résumé** : Trouver une recette d'allongement du contexte qui ne refait pas les négatifs 130/136/160/256.
> **Glossaire** : [curriculum](../../theorie/glossaire/entrees/curriculum.md) · [perplexité](../../theorie/glossaire/entrees/perplexite.md) · [test de l'aiguille](../../theorie/glossaire/entrees/test-de-l-aiguille.md).

## Le besoin

Les essais 130, 136, 160 et 256 sont tous négatifs ; le point 129 est isolé. Allonger le contexte demande un autre schéma (états de résumé, données, curriculum), pas un pas de plus.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | un plan d'entraînement (longueurs, données, état, pas) et un jeu d'évaluation |
| **sortie** | une courbe de PPL et d'aiguille de 129 à 1 000+ octets |
| **coût** | même budget de calcul que les essais négatifs, pour comparer |
| **trace** | chaque essai est tracé (longueur, données, graine, 
… [1106 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,80p tools/distiller_section.py", "description": "Read distillation script header"}`

  ```
#!/usr/bin/env python3
"""distiller_section.py — N2 : distillation avec ou sans état de section.

Le dispositif de N2 est reconstruit : professeur byte-level (23,5 M) entraîné par
`entrainer_moteur.py`, élève `drave-n0` (11,5 M) distillé par `distiller_natif.py`.
Ce script rejoue la distillation **par segments** pour comparer trois bras à budget
strictement égal :

  temoin     : l'élève nu, segments indépendants (aucun état) ;
  hierarchie : un état de section (GRUCell) transporté du segment précédent ;
  controle   : même architecture, état **roulé** = celui d'un autre document du lot.

Chaque pas voit `lot × nseg × seg` octets ; les deux bras voient les mêmes fenêtres
(Van der Corput, déterministe par graine). L'état est détaché entre segments (BPTT
tronquée à un segment) et repart de zéro à chaque pas : les échantillons sont des
documents indépendants.

Usage :
  PYTHONPATH=. gpu-env/bin/python tools/distiller_section.py \
      --enseignant /tmp/n2-campagne/route-teacher-20k \
      --init /tmp/n2-campagne/drave-n0-base-20k.pt \
      --bras hierarchie --graine 1 --pas 5000 --lot 8 --nseg 4 --seg 128 \
      --sortie /tmp/n2-campagne/hierarchie-g1.pt
"""
from __future__ import
… [1941 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"curriculum\\|129\" tools/distiller_natif.py | head -20; echo \"=== header ===\"; sed -n 1,50p tools/distiller_natif.py", "description": "Check original distillation script for curriculum"}`

  ```
=== header ===
#!/usr/bin/env python3
"""distiller_natif.py — N2.3 : distiller `drave-n0` depuis un professeur octet.

Le professeur est un Qwen3-MoE byte-level entraîné par `entrainer_moteur.py`
(`/tmp/route-teacher`), le student est `drave-n0`. Les deux parlent 256 octets :
la distillation est donc directe, sans tokenizer intermédiaire.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import time

import torch
import torch.nn.functional as F

from tools.native_model import NativeConfig, NativeModel, exporter_drvm
from tools.vdc import departs_vdc


def charger(txt: str) -> torch.Tensor:
    b = pathlib.Path(txt).read_bytes()
    return torch.tensor(list(b), dtype=torch.long)


def lot(data, n, seq, device, compteur=0):
    i = torch.tensor(departs_vdc(compteur, n, len(data) - seq - 1, seq), dtype=torch.long)
    x = torch.stack([data[j:j + seq] for j in i]).to(device)
    y = torch.stack([data[j + 1:j + seq + 1] for j in i]).to(device)
    return x, y


def ppl(modele, data, seq, lot_n, device, n_lots=8, compteur=0):
    modele.eval(); tot = 0.0; n = 0
    with torch.no_grad():
        for _ in range(n_lots):
            x, y = lot(da
… [532 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-native-distillation.md | head -60", "description": "Read original distillation report"}`

  ```
# N2.3 — distillation : PPL 3,297 contre 3,465

> **Objet.** Distiller `drave-n0` (11,47 M) depuis le professeur byte-level (23,76 M, PPL 2.355),
> avec la divergence KL sur les 256 octets et l'entropie croisée.

## Dispositif

- Professeur : `/tmp/route-teacher`, **23,76 M**, PPL **2.355**, gelé.
- Student : `drave-n0`, **11 469 192** paramètres, initialisé depuis `/tmp/drave-n0-pont.pt`.
- **2 000 pas**, lot 16, séquence 128, lr 2e-4, température 2, alpha 0,7 (KL) / 0,3 (CE).
- Corpus : `data/corpus_fr_train.txt` ; validation : derniers 5 %.
- **133 s** GPU.

## Résultats

| mesure | valeur |
|---|---:|
| PPL student avant | **3,465** |
| PPL student après | **3,297** |
| **gain** | **−4,85 %** |
| PPL professeur | **2.355** |
| gap student − professeur | **+0,942** |
| durée | 133 s |

## Lecture

- La distillation **améliore** le student de **4,85 %** sans changer son architecture.
- Le **gap** au professeur reste **+0,942** de PPL : le student de 11,47 M ne rattrape pas 23,76 M en
  2 000 pas.
- Le professeur partage le **vocabulaire octet** : aucun tokenizer, aucune perte d'alignement.
- Le student distillé est **exporté** en DRVM (`/tmp/drave-n0-distille.drvm`).

## Verdict

… [579 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"2,6998\\|2.6998\\|2.6997\" reports/*.md | head; echo \"=== ctx129 ===\"; head -50 reports/rapport-native-ctx129.md", "description": "Locate the 2.6998 result and ctx129 report"}`

  ```
reports/INDEX.md
reports/rapport-n2-distillation.md
reports/rapport-n2-hierarchie.md
reports/rapport-native-best-2.md
reports/rapport-native-ctx129-2.md
reports/rapport-native-ctx129.md
reports/rapport-native-ctx130-2.md
reports/README.md
=== ctx129 ===
# N2.33 — contexte 129 : PPL 2,700, nouveau meilleur

> **Objet.** Curriculum au pas de **1** : passer de 128 à **129**, depuis le meilleur **2,708**.

## Résultat

| mesure | N2.19 (128) | N2.33 (129) |
|---|---:|---:|
| PPL validation | **2,708** | **2,6998** |
| gain | — | **−0,008** |
| précision principale | 72,80 % | **72,40 %** |
| tête 3 | 72,60 % | **72,53 %** |
| durée | 1 945 s | **1 468 s** |

- 10 000 pas, lot 15, lr 5e-6, professeur 20k.
- **Nouveau meilleur français** : **2,6998**.

## Lecture

- Le **pas de 1** fonctionne là où 130, 136, 160 et 256 échouaient.
- Le gain est **faible** (−0,008) mais le sens est **inversé** : pour la première fois, un
  entraînement supplémentaire **améliore** le meilleur.
- La précision principale **baisse** légèrement (72,40 contre 72,80) : la PPL et le top-1 ne bougent
  pas ensemble.
- La porte **2,5** reste à **0,20**.

## Verdict

**N2.33 — nouveau meilleur** : **2,6998**. Le cur
… [362 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"21,63\\|21.63\" reports/*.md docs/ | head; echo \"=== best-2 ===\"; head -40 reports/rapport-native-best-2.md", "description": "Find capacity result at 21.63M"}`

  ```
reports/INDEX.md
reports/rapport-coherence-docs-2.md
reports/rapport-n2-distillation.md
reports/rapport-native-21m-20k.md
reports/rapport-native-capacite-egal.md
reports/rapport-native-distillation-20m.md
reports/README.md
docs/archive/roadmap-native-2026-10-29.md
docs/pilotage/backlog/N2-distillation.md
docs/pilotage/roadmap.md
=== best-2 ===
# N0.15/N4.7 — le meilleur 2,6998, servi par le moteur natif

> **Objet.** Exporter le nouveau meilleur `drave-n0` (**PPL 2,6998**, contexte 129) en DRVM, vérifier
> la parité native et remplacer le modèle du service.

## Résultat

| mesure | valeur |
|---|---:|
| paramètres | **11 814 792** |
| PPL validation | **2,6998** |
| PPL native 1 996 octets | **54,1350** |
| PPL Python 1 997 octets | **54,1327** |
| écart | **0,0023** |
| latence service 53 octets | **650,1 ms** |
| texte | `La France est un pays de travail de route et le contr` |

- DRVM : `/tmp/n0-ctx129.drvm`, SHA `ac5149…`.
- CLI : `drave --drvm-serve /tmp/n0-ctx129.drvm 8769`.
- Top-5 natif **identique** à Python : espace 6,8601 ; `e` 6,3866 ; `.` 5,4702 ; `\n` 5,2625 ; `o` 4,6627.

## Lecture

- Le **meilleur** student est **exécutable** et **servi** par le moteur Rust.
- La p
… [708 caractères tronqués]
  ```

- **bash** `{"command": "ls data/*.txt 2>/dev/null | head -20; echo \"=== sizes ===\"; du -h data/corpus*.txt 2>/dev/null | sort -h | tail -12", "description": "List corpus sources"}`

  ```
data/corpus_en.txt
data/corpus_en_val.txt
data/corpus_fr_litterature.txt
data/corpus_fr_train.txt
data/corpus_fr.txt
data/corpus_fr_val.txt
data/corpus_mixte_litt2.txt
data/corpus_mixte_litt.txt
data/corpus_mixte.txt
data/corpus_multi_train.txt
data/corpus_multi.txt
data/corpus_multi_val.txt
data/wikitext2_test.txt
=== sizes ===
228K	data/corpus_fr_val.txt
2,0M	data/corpus_en_val.txt
4,2M	data/corpus_fr_train.txt
4,5M	data/corpus_fr.txt
5,8M	data/corpus_multi_val.txt
11M	data/corpus_mixte.txt
12M	data/corpus_mixte_litt.txt
15M	data/corpus_mixte_litt2.txt
17M	data/corpus_fr_litterature.txt
96M	data/corpus_en.txt
111M	data/corpus_multi_train.txt
116M	data/corpus_multi.txt
  ```

- **bash** `{"command": "head -45 reports/rapport-native-capacite-egal.md; echo \"==== 21M ====\"; head -45 reports/rapport-native-21m-20k.md", "description": "Read capacity reports"}`

  ```
# N2.5b — capacité à budget égal : 21,63 M bat 11,47 M de 4,1 %

> **Objet.** Lever le biais de N2.5 : le student 21,63 M partait de zéro et le 11,47 M d'un checkpoint.
> Ici, les deux partent d'une **initialisation aléatoire**, avec le **même budget** (5 000 pas, lot 8),
> le même professeur, le même corpus et le même échantillonnage VDC.

## Dispositif

| | 11,47 M | 21,63 M |
|---|---:|---:|
| paramètres | **11 469 192** | **21 634 536** |
| initialisation | aléatoire | aléatoire |
| pas | 5 000 | 5 000 |
| lot / séquence | 8 / 128 | 8 / 128 |
| professeur | `/tmp/route-teacher` (PPL **2,355**) | idem |
| échantillonnage | VDC | VDC |

## Résultats — trois graines

| graine | 11,47 M | 21,63 M |
|---:|---:|---:|
| 1 | 4,4756 | 4,2944 |
| 2 | 4,5294 | 4,0654 |
| 3 | 4,5160 | 4,0666 |
| **moyenne** | **4,5070** | **4,1421** |
| **écart-type** | **0,028** | **0,132** |
| **écart moyen** | — | **−8,1 %** |
| précision principale (moyenne) | **59,23 %** | **60,16 %** |
| tête 3 (moyenne) | **57,13 %** | **57,81 %** |

**Contrôle** : le même 11,47 M **parti d'un checkpoint** (`/tmp/drave-n0-pont.pt`) atteint **3,295**.
Le passage de 4,476 à 3,295 mesure donc le **budget antérieur**, p
… [2283 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"4 sources\" reports/*.md | head -10; echo \"=== card ===\"; sed -n 1,80p docs/pilotage/backlog/N2-distillation.md", "description": "Find 4-source distillation recipe"}`

  ```
reports/rapport-n2-distillation.md
reports/rapport-n2-hierarchie.md
reports/rapport-native-corpus-multi.md
reports/README.md
=== card ===
# N2 — Distillation native (50 000 séquences)

> **Statut** : en cours · **Priorité** : P1 · **Programme** : N · **Dépend de** : N1
> **Ligne de roadmap** : N2 · **Fiche de résultat attendue** : rapport-n2-distillation.md (à créer dans `reports/`)
> **Résumé** : Faire tenir le natif sans professeur, sur 50 000 séquences, avec la porte < 2,5 de PPL.
> **Glossaire** : [distillation](../../theorie/glossaire/entrees/distillation.md) · [professeur / élève](../../theorie/glossaire/entrees/professeur-eleve.md) · [perplexité](../../theorie/glossaire/entrees/perplexite.md) · [BPE](../../theorie/glossaire/entrees/bpe.md).

## Le besoin

Le student plafonne à 2,708 et la porte < 2,5 n'est pas atteinte. Les 130–256 de contexte sont négatifs ; il faut décider si le levier est la donnée, la capacité ou la hiérarchie.

**Le levier retenu le 2026-10-29 est la hiérarchie** (l'état de section), et c'est **N2 qui la porte** : R11 en mesurera la fenêtre. Les longueurs brutes ne sont plus essayées — cinq négatifs suffisent.

## L'état

49 999 fenêtres, 4 sources ; pr
… [887 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/ 2>&1 | head -20; echo \"=== /tmp ===\"; ls /tmp/n2-campagne/ 2>&1 | head -20", "description": "Check archived checkpoints"}`

  ```
total 1276816
drwxr-xr-x. 1 stephane stephane        110 31 oct 17:00 .
drwxr-xr-x. 1 stephane stephane         20 31 oct 16:57 ..
drwxr-xr-x. 1 stephane stephane       2070 31 oct 16:34 artefacts
-rw-r--r--. 1 stephane stephane       6154 31 oct 16:58 MANIFESTE.sha256
-rw-r--r--. 1 stephane stephane 1307445674 31 oct 16:58 n2-2026-10-31.tar.zst
-rw-------. 1 stephane stephane       3758 31 oct 17:00 README.md
=== /tmp ===
ls: cannot access '/tmp/n2-campagne/': No such file or directory
  ```

- **bash** `{"command": "head -40 reports/rapport-native-corpus-multi.md", "description": "Read multi-source corpus report"}`

  ```
# N2.6 — corpus diversifié : 49 999 fenêtres, quatre sources

> **Objet.** Répondre au reproche de N2.1 : un seul corpus, français. On construit un manifeste
> multi-sources sans concaténer les fichiers.

## Résultat

| mesure | valeur |
|---|---:|
| sources | **4** |
| fenêtres | **49 999** |
| train / validation | **44 999 / 5 000** |
| fenêtre / pas | 128 / 64 |
| `corpus_fr.txt` | 4,63 Mo, 72 403 fenêtres possibles |
| `udhr_train.txt` | 4,38 Mo, 68 433 |
| `corpus_en.txt` | 100,28 Mo, 1 566 813 |
| `corpus_mixte_litt.txt` | 12,23 Mo, 191 143 |

- Manifeste : [`native-corpus-multi.json`](native-corpus-multi.json).
- Répartition **équilibrée par quotas** entre sources, puis tirage déterministe (graine 0).

## Lecture

- La **diversité** est là : français, anglais, UDHR multilingue, littérature mixte.
- Les **49 999** fenêtres sont un plafond de quotas, pas 50 000 exactement (arrondi).
- Les **licences** ne sont **pas** vérifiées : le manifeste le dit.
- **Aucun entraînement** n'utilise encore ce corpus : c'est N2.7.

## Verdict

**N2.6 — diversité : atteint** (4 sources, 49 999 fenêtres). La **qualité** et les **licences** restent à
vérifier ; la **distillation** sur ce corpus n
… [241 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/ | head -40; echo \"=== README ===\"; cat /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/README.md", "description": "List archived artefacts and read backup README"}`

  ```
total 1312604
drwxr-xr-x. 1 stephane stephane     2070 31 oct 16:34 .
drwxr-xr-x. 1 stephane stephane      110 31 oct 17:00 ..
-rw-r--r--. 1 stephane stephane    21688 31 oct 13:58 base.log
-rw-------. 1 stephane stephane     4028 31 oct 15:47 CHECKPOINT.md
-rw-r--r--. 1 stephane stephane 48714013 31 oct 15:17 controle-g1.pt
-rw-r--r--. 1 stephane stephane 48689436 31 oct 15:17 controle-g1.pt.drvm
-rw-r--r--. 1 stephane stephane      511 31 oct 15:17 controle-g1.pt.json
-rw-r--r--. 1 stephane stephane 48714013 31 oct 16:18 controle-g2.pt
-rw-r--r--. 1 stephane stephane 48689436 31 oct 16:18 controle-g2.pt.drvm
-rw-r--r--. 1 stephane stephane      510 31 oct 16:18 controle-g2.pt.json
-rw-r--r--. 1 stephane stephane 48714013 31 oct 16:33 controle-g3.pt
-rw-r--r--. 1 stephane stephane 48689436 31 oct 16:33 controle-g3.pt.drvm
-rw-r--r--. 1 stephane stephane      512 31 oct 16:33 controle-g3.pt.json
-rw-r--r--. 1 stephane stephane 47278428 31 oct 13:58 drave-n0-base-20k.drvm
-rw-r--r--. 1 stephane stephane 47302891 31 oct 13:58 drave-n0-base-20k.pt
-rw-r--r--. 1 stephane stephane      557 31 oct 13:58 drave-n0-base-20k.pt.json
-rw-------. 1 stephane stephane     3733 31 oct 15:07 eval_
… [5333 caractères tronqués]
  ```

- **read** `{"file_path": "tools/eval_n2.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """eval_n2.py — PPL des points de contrôle N2, trois protocoles.
3: 
4:   standard     : 128 octets indépendants — comparable entre bras et à d'autres runs ;
5:   segmente     : 4×128 avec état transporté — le protocole de l'entraînement ;
6:   segmente-sans: 4×128 avec état remis à zéro à chaque segment — contrôle du précédent.
7: 
8: Usage : PYTHONPATH=. gpu-env/bin/python tools/eval_n2.py /tmp/n2-campagne/*-g*.pt
9:         (sans argument : les points de contrôle de /tmp/n2-campagne)
10: """
11: import glob
12: import json
13: import math
14: import pathlib
15: import sys
16: 
17: import torch
18: import torch.nn.functional as F
19: 
20: from tools.native_model import NativeConfig, NativeModel
21: from tools.distiller_section import HierarchieModel, decoupes
22: from tools.vdc import departs_vdc
23: 
24: LOTS = 32          # 32 lots × 8 = 256 fenêtres par protocole
25: 
26: 
27: def charger(txt):
28:     return torch.tensor(list(pathlib.Path(txt).read_bytes()), dtype=torch.long)
29: 
30: 
31: def ppl_standard(m, data, seq=128, lot=8, device="cuda
… [2949 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 50,200p tools/distiller_natif.py", "description": "Read distillation training loop"}`

  ```
ap.add_argument("--train", default="data/corpus_fr_train.txt")
    ap.add_argument("--val", default="data/corpus_fr_val.txt")
    ap.add_argument("--pas", type=int, default=2000)
    ap.add_argument("--lot", type=int, default=16)
    ap.add_argument("--seq", type=int, default=128)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--temperature", type=float, default=2.0)
    ap.add_argument("--alpha", type=float, default=0.7)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--sortie", default="/tmp/drave-n0-distille.pt")
    ap.add_argument("--drvm", default="/tmp/drave-n0-distille.drvm")
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--tetes", action=argparse.BooleanOptionalAction, default=True,
                    help="ajouter les têtes précoces à la distillation")
    a = ap.parse_args()
    torch.manual_seed(a.graine)
    from transformers import AutoModelForCausalLM
    prof = AutoModelForCausalLM.from_pretrained(a.enseignant, dtype=torch.float32).to(a.device).eval()
    for p in prof.parameters(): p.requires_grad_(False)
    ck = torch.load(a.init, map_location="cpu", weights_only=False)
    cfg = NativeC
… [2891 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nd=json.load(open('reports/native-corpus-multi.json'))\nprint(type(d), list(d)[:10] if isinstance(d,dict) else len(d))\nprint(json.dumps(d, ensure_ascii=False)[:1200])\n\"", "description": "Inspect multi-source manifest"}`

  ```
<class 'dict'> ['sources', 'fenetre', 'pas', 'ordre', 'fenetres', 'train', 'val', 'graine', 'premier_offset', 'licence']
{"sources": [{"source": "data/corpus_fr.txt", "octets": 4633889, "fenetres": 72403}, {"source": "data/udhr/udhr_train.txt", "octets": 4379837, "fenetres": 68433}, {"source": "data/corpus_en.txt", "octets": 100276153, "fenetres": 1566813}, {"source": "data/corpus_mixte_litt.txt", "octets": 12233263, "fenetres": 191143}], "fenetre": 128, "pas": 64, "ordre": "van_der_corput", "fenetres": 49999, "train": 44999, "val": 5000, "graine": 0, "premier_offset": {"source": "data/corpus_fr.txt", "offset": 0}, "licence": "sources locales — licences à vérifier avant diffusion", "note": "manifeste d'offsets multi-sources ; les corpus ne sont pas versionnés"}
  ```

- **bash** `{"command": "sed -n 1,90p tools/native_model.py", "description": "Read native model config"}`

  ```
#!/usr/bin/env python3
"""native_model.py — `drave-n0`, le modèle natif du programme N.

Ce n'est pas un Qwen3-MoE : c'est un graphe de blocs en **octets**, avec
attention locale, FFN creux routé, sorties précoces, cellule de pensée et pont.
Le modèle est petit (12 M) : c'est un **banc de mécanismes**, pas un assistant.

Le fichier définit l'architecture, l'export DRVM et les tests de forme. Il ne
prétend pas que l'entraînement est fait : N1.2 reste à mesurer.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F

from tools.drvm import TensorSpec, write_drvm


@dataclass
class NativeConfig:
    vocab: int = 256
    d_model: int = 224
    n_blocks: int = 6
    n_heads: int = 4
    expert_hidden: int = 288
    n_experts: int = 8
    top_k: int = 2
    kwta: float = 0.25
    window: int = 256
    max_pos: int = 2048
    thought_steps: int = 2
    early_blocks: tuple[int, ...] = (1, 3, 5)  # 0-based : après 2, 4, 6
    rsn_dim: int = 120


class SparseFFN(nn.Module):
    def __init__(self, cfg: NativeConfig):
        super().__init__()
        self.cfg = cfg
        self.rou
… [2084 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/native-ctx129.json 2>/dev/null | head -40; echo \"=== base json ===\"; cat /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/drave-n0-base-20k.pt.json", "description": "Read historical protocol JSON"}`

  ```
{
 "professeur": "/tmp/route-teacher-20k",
 "student": "/tmp/drave-n0-ctx129.pt",
 "pas": 10000,
 "lot": 15,
 "seq": 129,
 "lr": 5e-06,
 "temperature": 2.0,
 "alpha": 0.7,
 "tetes": true,
 "perte_finale": 35.23850631713867,
 "ppl_val": 2.699767641509761,
 "precision_main": 0.724031007751938,
 "precision_early": [
  0.5713178294573643,
  0.6688630490956072,
  0.7253229974160207
 ],
 "drvm": "/tmp/drave-n0-ctx129.drvm",
 "sha256_drvm": "ac514962fffddb2b3d7dffa9ce8d6be110b050936b035917e3ce85ae49897e22",
 "duree_s": 1468.331059217453,
 "ppl_avant": 2.7077790503722454,
 "gain": 0.008011408862484526
}=== base json ===
{
 "modele": "drave-n0",
 "parametres": 11814792,
 "corpus": "data/corpus_fr_train.txt",
 "octets": 4402195,
 "pas": 20000,
 "seq": 128,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "perte_finale": 1.2159148454666138,
 "ppl_val": 3.573728805050751,
 "jetons_val": 8192,
 "tetes": true,
 "precision_main": 0.610107421875,
 "precision_early": [
  0.547607421875,
  0.59765625,
  0.6103515625
 ],
 "drvm": "/tmp/n2-campagne/drave-n0-base-20k.drvm",
 "sha256_drvm": "b651710841a2f94e549fdf73f9e4c11a5e2313bd1cc4a002d56d599348ee0ce7",
 "duree_s": 880.581111907959
}
  ```

- **bash** `{"command": "ls reports/ | grep -i \"native\" | head -40", "description": "List native reports"}`

  ```
native-21m-20k.json
native-8b.json
native-8b-warm.json
native-best-2.json
native-best-service.json
native-cache-gain.json
native-cache.json
native-capacite-egal.json
native-consignes.json
native-corpus.json
native-corpus-multi.json
native-ctx129-2.json
native-ctx129.json
native-ctx130-2.json
native-ctx130.json
native-ctx136.json
native-ctx160.json
native-ctx256.json
native-distillation-20k.json
native-distillation-20m.json
native-distillation-50k.json
native-distillation.json
native-distillation-multi.json
native-distillation-tetes.json
native-generation.json
native-local.json
native-n0.json
native-parite.json
native-pensee.json
native-pont.json
native-ppl-2k.json
native-ppl-corpus.json
native-ppl.json
native-prof10k-2.json
native-prof10k.json
native-prof20k-2.json
native-prof20k-3.json
native-prof20k-4.json
native-prof20k-5.json
native-prof20k-7.json
  ```

- **bash** `{"command": "grep -l \"corpus-multi\\|corpus_multi\" reports/rapport-native-*.md | head -20", "description": "Find reports using multi corpus"}`

  ```
reports/rapport-native-corpus-multi.md
reports/rapport-native-distillation-multi.md
  ```

- **bash** `{"command": "head -50 reports/rapport-native-distillation-multi.md; echo \"=== json ===\"; cat reports/native-distillation-multi.json", "description": "Read multi-source distillation report"}`

  ```
# N2.7 — distillation multi-sources : 9,517, au niveau du professeur

> **Objet.** Distiller `drave-n0` sur le corpus multi-sources (fr, UDHR, en, littérature) avec un
> professeur **multi**, tous deux échantillonnés par van der Corput.

## Dispositif

- Professeur : Qwen3-MoE byte-level **23,76 M**, **5 000 pas**, validation **3,2587 bit/octet**, PPL **9.571**.
- Student : `drave-n0` **11 469 192** paramètres, initialisé depuis `/tmp/drave-n0-pont.pt`.
- **5 000 pas**, lot 16, séquence 128, lr 2e-4, T=2, alpha 0,7, têtes précoces.
- Corpus : `data/corpus_multi_train.txt` (115,4 Mo) ; validation 6,08 Mo.
- **341 s** GPU.

## Résultats

| mesure | professeur | student |
|---|---:|---:|
| PPL validation | **9.571** | **9.517** |
| bits/octet | **3,2587** | — |
| précision principale | — | **36,34 %** |
| têtes précoces | — | **30,10 / 34,08 / 36,83 %** |
| paramètres | 23,76 M | **11,47 M** |

- **Écart student − professeur** : **-0.055** de PPL (**-0.6 %**).
- Le student **égale** le professeur avec **deux fois moins** de paramètres.

## Lecture

- Sur le corpus **multi**, le student **rattrape** le professeur : **9,517** contre **9,571**.
- Mais les deux sont **bien plus mauvais** 
… [1481 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, glob, os\nrows=[]\nfor f in glob.glob('reports/native-*.json'):\n    try: d=json.load(open(f))\n    except Exception: continue\n    if 'ppl_val' in d:\n        rows.append((d['ppl_val'], os.path.basename(f), d.get('pas'), d.get('seq'), d.get('lot'), str(d … [196 caractères tronqués]`

  ```
1.7339  native-professeur-30k.json             pas=30000 seq=128 lot=16 
   1.8707  native-professeur-20k.json             pas=20000 seq=128 lot=16 
   2.1037  native-professeur-10k.json             pas=10000 seq=128 lot=16 
   2.3553  native-professeur.json                 pas=5000 seq=128 lot=16 
   2.6998  native-ctx129.json                     pas=10000 seq=129 lot=15 /tmp/drave-n0-ctx129.pt
   2.7078  native-prof20k-5.json                  pas=30000 seq=128 lot=16 /tmp/drave-n0-prof20k-5.pt
   2.7139  native-prof20k-4.json                  pas=30000 seq=128 lot=16 /tmp/drave-n0-prof20k-4.pt
   2.7149  native-ctx130-2.json                   pas=5000 seq=130 lot=15 /tmp/drave-n0-ctx130-2.pt
   2.7264  native-prof20k-3.json                  pas=30000 seq=128 lot=16 /tmp/drave-n0-prof20k-3.pt
   2.7548  native-prof20k-2.json                  pas=20000 seq=128 lot=16 /tmp/drave-n0-prof20k-2.pt
   2.7871  native-prof20k.json                    pas=20000 seq=128 lot=16 /tmp/drave-n0-prof20k.pt
   2.8764  native-prof10k-2.json                  pas=20000 seq=128 lot=16 /tmp/drave-n0-prof10k-2.pt
   2.9097  native-prof10k.json                    pas=20000 seq=128 lot=16 /tmp/drave-n0-pr
… [1114 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f in ['native-prof20k.json','native-prof20k-5.json','native-ctx129.json','native-distillation-20k.json','native-distillation-tetes.json']:\n    d=json.load(open('reports/'+f))\n    print(f, {k:d[k] for k in d if k in ('professeur','init','student','pa … [219 caractères tronqués]`

  ```
native-prof20k.json {'professeur': '/tmp/route-teacher-20k', 'student': '/tmp/drave-n0-prof20k.pt', 'pas': 20000, 'lot': 16, 'seq': 128, 'lr': 3e-05, 'tetes': True, 'ppl_val': 2.7870780134647015, 'ppl_avant': 2.876413568419352}
native-prof20k-5.json {'professeur': '/tmp/route-teacher-20k', 'student': '/tmp/drave-n0-prof20k-5.pt', 'pas': 30000, 'lot': 16, 'seq': 128, 'lr': 5e-06, 'tetes': True, 'ppl_val': 2.7077790503722454, 'ppl_avant': 2.7139378014106175}
native-ctx129.json {'professeur': '/tmp/route-teacher-20k', 'student': '/tmp/drave-n0-ctx129.pt', 'pas': 10000, 'lot': 15, 'seq': 129, 'lr': 5e-06, 'tetes': True, 'ppl_val': 2.699767641509761, 'ppl_avant': 2.7077790503722454}
native-distillation-20k.json {'professeur': '/tmp/route-teacher', 'student': '/tmp/drave-n0-distille-20k.pt', 'pas': 20000, 'lot': 16, 'seq': 128, 'lr': 0.0001, 'tetes': True, 'ppl_val': 3.123330521983312, 'ppl_avant': 3.295}
native-distillation-tetes.json {'professeur': '/tmp/route-teacher', 'student': '/tmp/drave-n0-distille-tetes.pt', 'pas': 5000, 'lot': 16, 'seq': 128, 'lr': 0.0002, 'tetes': True, 'ppl_val': 3.295052371818759, 'ppl_avant': 3.297}
=== report prof20k-5 ===
# N2.19 — 30 000 pas de plus : PP
… [1004 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"corpus-multi\\|corpus_multi\\|manifeste\" tools/*.py | head -15; echo \"=== grep manifest ===\"; grep -rn \"native-corpus-multi\" tools/*.py | head", "description": "Find multi-source corpus consumer"}`

  ```
tools/archive_sessions.py
tools/banc_complet.py
tools/banc_durci.py
tools/banc_lecture.py
tools/bloc_tableaux.py
tools/calibrer.py
tools/convertir_clusters.py
tools/corpus_gele.py
tools/corpus_natif.py
tools/declencheur.py
tools/drvm.py
tools/drvm_trace.py
tools/essai_blocs.py
tools/gguf_drvm.py
tools/glossaire_cartes.py
=== grep manifest ===
  ```

- **bash** `{"command": "sed -n 1,60p tools/corpus_natif.py", "description": "Read native corpus builder"}`

  ```
#!/usr/bin/env python3
"""corpus_natif.py — N2.1 : fenêtres d'entraînement pour `drave-n0`.

Découpe un corpus d'octets en fenêtres de `fenetre` octets, avec un pas fixe,
puis un split train/validation déterministe. Écrit un manifeste JSON (offsets)
et, si demandé, un fichier binaire concaténé — les corpus de `data/` sont
ignorés par git.
"""
from __future__ import annotations

import argparse
import json
import pathlib
from tools.vdc import ordre_vdc


def construire_multi(sources: list[str], fenetre: int = 128, pas: int = 64,
                     max_fenetres: int = 50_000, val: int = 5_000,
                     graine: int = 0) -> dict:
    """Fenêtres sur plusieurs sources, sans concaténer les fichiers."""
    par_source = []
    for src in sources:
        b = pathlib.Path(src).read_bytes()
        offsets = list(range(0, max(0, len(b) - fenetre + 1), pas))
        par_source.append({"source": src, "octets": len(b), "fenetres": len(offsets)})
    # Répartition équilibrée, plafonnée à max_fenetres.
    total = sum(x["fenetres"] for x in par_source)
    quotas = {x["source"]: max(1, max_fenetres * x["fenetres"] // total) for x in par_source}
    offsets = []
    for src, q in qu
… [1484 caractères tronqués]
  ```

- **bash** `{"command": "cat .gitignore 2>/dev/null | head -30; echo \"=== gpu-env ===\"; ls gpu-env/bin/python 2>/dev/null && gpu-env/bin/python -c \"import torch, transformers; print(torch.__version__, transformers.__version__, torch.cuda.is_available())\"", "description": "Check gitignore and GPU environment … [2 caractères tronqués]`

  ```
__pycache__/
*.pyc
reports/*.tmp
models/
data/
qtrinet-core/target/

# Traces de session : la copie brute reste sur disque (volumineuse, binaire),
# le digest markdown est versionné.
journal/sessions/*/session*.jsonl.zstd
journal/sessions/archive.log

# Outil de référence : la source est versionnée, le binaire se recompile
# (commande exacte dans tools/ref_logits.md).
tools/ref_logits
target/

# docwatch — SVG générés depuis les sources .puml/.mmd (docwatch les produit)
docs/**/*.puml.svg
docs/**/*.mmd.svg
=== gpu-env ===
[exit code: 2]
  ```

- **bash** `{"command": "ls -d venv .venv gpu-env 2>/dev/null; python3 -c \"import torch; print('sys torch', torch.__version__, torch.cuda.is_available())\" 2>&1 | tail -2; echo \"=== find python envs ===\"; ls ~/ | head -20", "description": "Locate the GPU Python environment"}`

  ```
^^^^^^^^^^^^
ModuleNotFoundError: No module named 'torch'
=== find python envs ===
altera_pro
Applications
Bureau
data
Data13TB
Desktop
Documents
Downloads
FastNVMe
flex
fpga-compat
GitHub
gpu-env
IA
Images
intelFPGA
intelFPGA_std
iverilog
lib64_shim
lvm-cache-backup-20251222-131716
  ```

- **bash** `{"command": "~/gpu-env/bin/python -c \"import torch, transformers; print(torch.__version__, transformers.__version__, torch.cuda.is_available(), torch.cuda.device_count())\"", "description": "Verify GPU env at home"}`

  ```
2.11.0+cu130 5.15.0 True 2
  ```

- **bash** `{"command": "cat /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/CHECKPOINT.md", "description": "Read campaign checkpoint notes"}`

  ```
# Checkpoint — campagne N2 (état au 2026-10-31 14 h 20)

## Dispositif reconstruit (tout était dans /tmp, effacé au boot de 07:09)

| pièce | état | fichier |
|---|---|---|
| professeur 23,57 M, 20 k pas | **en cours** ~13 k/20 k, val 1,00 bit/octet | `/tmp/n2-campagne/route-teacher-20k` (dossier HF) |
| élève de base 20 k pas | **fait** — PPL **3,5737** (880 s) | `/tmp/n2-campagne/drave-n0-base-20k.pt` |
| distillateur 3 bras | écrit, testé côté élève | `tools/distiller_section.py` |
| évaluation post-hoc | écrite | `/tmp/n2-campagne/evalue.py` |

Commandes exactes :
```
# professeur (23,57 M ; la référence historique est 23,76 M)
PYTHONUNBUFFERED=1 PYTHONPATH=. gpu-env/bin/python tools/entrainer_moteur.py \
  --famille route --dim 384 --couches 6 --tetes 4 --cache 752 --experts 8 --k 2 \
  --pas 20000 --lot 16 --seq 128 --lr 1e-3 --graine 1 \
  --donnees data/corpus_fr_train.txt --validation data/corpus_fr_val.txt \
  --sortie /tmp/n2-campagne/route-teacher-20k

# élève de base
PYTHONPATH=. gpu-env/bin/python tools/entrainer_native.py --corpus data/corpus_fr_train.txt \
  --pas 20000 --seq 128 --lot 8 --lr 3e-4 --graine 1 \
  --sortie /tmp/n2-campagne/drave-n0-base-20k.pt --drvm 
… [2718 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Calibrating the archived checkpoints against the historical evaluation protocol

- **bash** `{"command": "mkdir -p /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d && cat > /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/calibrer.py <<'EOF'\n#!/usr/bin/env python3\n\"\"\"Calibration : PPL des points de contrôle archivés sous le protocole historique.\n\nprotocole historique  … [2331 caractères tronqués]`

  ```
{"fichier": "temoin-g1.pt", "ppl_128_lot16": 2.9406, "ppl_128_lot8": 2.9399, "ppl_129_lot15": 2.9631}
{"fichier": "drave-n0-base-20k.pt", "ppl_128_lot16": 3.2161, "ppl_128_lot8": 3.2296, "ppl_129_lot15": 3.2653}
  ```

- **bash** `{"command": "sed -n 90,190p tools/native_model.py; echo \"=== vdc ===\"; sed -n 1,60p tools/vdc.py", "description": "Read model forward and VDC helpers"}`

  ```
y = F.scaled_dot_product_attention(q, k, v, attn_mask=masque)
        y = y.transpose(1, 2).reshape(b, s, d)
        x = x + self.out(y)
        return x + self.ffn(self.ln2(x))


class NativeModel(nn.Module):
    def __init__(self, cfg: NativeConfig | None = None):
        super().__init__()
        self.cfg = cfg or NativeConfig()
        self.embed = nn.Embedding(self.cfg.vocab, self.cfg.d_model)
        self.pos = nn.Embedding(self.cfg.max_pos, self.cfg.d_model)
        self.blocks = nn.ModuleList([Block(self.cfg) for _ in range(self.cfg.n_blocks)])
        self.early_heads = nn.ModuleList([nn.Linear(self.cfg.d_model, self.cfg.vocab)
                                          for _ in self.cfg.early_blocks])
        # Têtes LOCALES : une sortie après CHAQUE bloc, pour la supervision
        # profonde. Elles n'existaient pas dans les checkpoints antérieurs :
        # le chargement se fait en strict=False et elles apprennent.
        self.local_heads = nn.ModuleList([nn.Linear(self.cfg.d_model, self.cfg.vocab)
                                          for _ in range(self.cfg.n_blocks)])
        self.bridge = nn.Linear(self.cfg.d_model, self.cfg.d_model)
        self.thought = nn
… [5191 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Setting up the N2 campaign goal and the budget/data experiment

- **create_goal** `{"objective": "N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre e … [83 caractères tronqués]`

> **Objectif** (create) : N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/pilotage/en-cours.md et la roadmap à jour.


  ```
{"goal":{"id":"goal-371547c2-8e61-4925-8ab3-dab60674eec4","revision":1,"objective":"N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/pilotage/en-cours.md et la roadmap à jour.","phase":"active","roundsStarted":0,"maxGoalRounds":1000},"activation":"armed"}
  ```

- **todo_write** `{"todos": [{"content": "Écrire tools/distiller_budget.py (stages seq/lr, corpus fr|multi, graines, éval 3 protocoles)", "status": "in_progress"}, {"content": "Vérifier le manifeste multi-sources reconstruit (49 999 fenêtres, 44 999/5 000)", "status": "pending"}, {"content": "Lancer A (français, 20 0 … [455 caractères tronqués]`

  ```
Updated todo list: 6 pending, 1 in progress, 0 completed.
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/distiller_budget.py", "content": "#!/usr/bin/env python3\n\"\"\"distiller_budget.py — N2 : le budget, les données et le curriculum de longueur.\n\nLe dispositif de N2 est reconstruit (professeur byte-level 23,57 M, élève\n`drave-n0 … [11804 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/distiller_budget.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, pathlib\np = pathlib.Path('tools/distiller_budget.py')\ns = p.read_text()\ns = s.replace('''def lot_fr(data, n, seq, device, compteur):\n    i = torch.tensor(departs_vdc(compteur, n, len(data) - seq - 1, … [3640 caractères tronqués]`

  ```
ok
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/distiller_budget.py", "offset": 150, "limit": 65}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/distiller_budget.py</path>
<type>file</type>
<content>
150:     sortie.parent.mkdir(parents=True, exist_ok=True)
151:     log = open(a.log, "a") if a.log else None
152: 
153:     def dire(txt):
154:         print(txt, flush=True)
155:         if log:
156:             log.write(txt + "\n"); log.flush()
157: 
158:     from transformers import AutoModelForCausalLM
159:     prof = AutoModelForCausalLM.from_pretrained(a.enseignant, dtype=torch.float32).to(a.device).eval()
160:     for p in prof.parameters():
161:         p.requires_grad_(False)
162:     ck = torch.load(a.init, map_location="cpu", weights_only=False)
163:     cfg = NativeConfig(**{k: v for k, v in ck["config"].items()
164:                           if k in NativeConfig.__annotations__})
165:     etu = NativeModel(cfg).to(a.device)
166:     manquants = etu.load_state_dict(ck["state"], strict=False)
167:     dire(f"# init {a.init} · manquants {list(manquants.missing_keys)[:6]} · "
168:          f"graine {a.graine} · décalage {decalage}")
169:     opt = torch.optim.AdamW(etu.parameters(), lr=plan[0][2], weight_decay=0.01)
170: 
171:     if a.corpus == "fr":
172:   
… [2309 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np = pathlib.Path('tools/distiller_budget.py')\ns = p.read_text()\ns = s.replace('''    if a.corpus == \"fr\":\n        train = charger(a.train)\n        lots = lambda compteur, n, seq: lot_fr(train, … [1696 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. timeout 900 ~/gpu-env/bin/python tools/distiller_budget.py \\\n  --corpus fr --stages \"128:20:1e-4\" --lot 4 --graine 1 \\\n  --sortie work/n2d/essai-fr.pt 2>&1 | tail -25", "description": "Smoke-test French corpus run" … [1 caractères tronqués]`

  ```
[
   128,
   20,
   0.0001
  ]
 ],
 "lot": 4,
 "temperature": 2.0,
 "alpha": 0.7,
 "tetes": true,
 "pas": 20,
 "octets_vus": 10240,
 "perte_finale": 105.2849349975586,
 "ppl_128_lot16": 3.3086749971250318,
 "ppl_128_lot8": 3.292275900102567,
 "ppl_129_lot15": 3.3533693141845546,
 "ppl_permute": 816.7429927362388,
 "precision_main": 0.66650390625,
 "precision_early": [
  0.609375,
  0.6572265625,
  0.6708984375
 ],
 "duree_s": 2.8708770275115967
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. timeout 900 ~/gpu-env/bin/python tools/distiller_budget.py \\\n  --corpus multi --stages \"128:20:1e-4\" --lot 4 --graine 1 \\\n  --sortie work/n2d/essai-multi.pt 2>&1 | tail -30", "description": "Smoke-test multi-source … [6 caractères tronqués]`

  ```
Loading weights:   0%|          | 0/68 [00:00<?, ?it/s]Loading weights: 100%|██████████| 68/68 [00:00<00:00, 932.90it/s]
# init /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/drave-n0-base-20k.pt · manquants [] · graine 1 · décalage 0
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/distiller_budget.py", line 261, in <module>
    main()
    ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/distiller_budget.py", line 176, in main
    corpus = CorpusMulti(a.manifeste)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/distiller_budget.py", line 85, in __init__
    assert len(self.train) == m["train"] and len(self.val) == m["val"], (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: manifeste non reproduit : 44997/5000 au lieu de 44999/5000
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\nm=json.load(open('reports/native-corpus-multi.json'))\ntot=sum(s['fenetres'] for s in m['sources'])\nprint('total', tot, 'max', m['fenetres'])\nfor s in m['sources']:\n    q=max(1, m['fenetres … [434 caractères tronqués]`

  ```
total 1898792 max 49999
data/corpus_fr.txt               fenetres_m=   72403 recalc=   72403 octets_m=   4633889 reel=   4633889 quota=1906
data/udhr/udhr_train.txt         fenetres_m=   68433 recalc=   68433 octets_m=   4379837 reel=   4379837 quota=1801
data/corpus_en.txt               fenetres_m= 1566813 recalc= 1566813 octets_m= 100276153 reel= 100276153 quota=41257
data/corpus_mixte_litt.txt       fenetres_m=  191143 recalc=  191143 octets_m=  12233263 reel=  12233263 quota=5033
somme quotas 49997
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, math\nm=json.load(open('reports/native-corpus-multi.json'))\nS=m['sources']; tot=sum(s['fenetres'] for s in S); M=m['fenetres']\ndef mont(tag, qs): print(f\"{tag:28s} {qs} somme={sum(qs)}\")\nmont('flo … [693 caractères tronqués]`

  ```
floor fenetres               [1906, 1801, 41257, 5033] somme=49997
round fenetres               [1907, 1802, 41257, 5033] somme=49999
ceil fenetres                [1907, 1802, 41258, 5034] somme=50001
floor octets                 [1906, 1802, 41257, 5033] somme=49998
round octets                 [1907, 1802, 41257, 5033] somme=49999
40000 fenetres               [1525, 1441, 33006, 4026] somme=39998
redistribue [1907, 1802, 41257, 5033] 49999
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/distiller_budget.py'); s=p.read_text()\ns=s.replace('''        quotas = {s[\"source\"]: max(1, self.max_fenetres * s[\"fenetres\"] // total)\n                  for s in sources … [566 caractères tronqués]`

  ```
ok
  [
   128,
   20,
   0.0001
  ]
 ],
 "lot": 4,
 "temperature": 2.0,
 "alpha": 0.7,
 "tetes": true,
 "pas": 20,
 "octets_vus": 10240,
 "perte_finale": 220.3186798095703,
 "ppl_128_lot16": 3.282691243296492,
 "ppl_128_lot8": 3.2855321383530263,
 "ppl_129_lot15": 3.321579579434593,
 "ppl_permute": 496.6914211503149,
 "ppl_multi_val": 24.24006368561966,
 "precision_main": 0.236328125,
 "precision_early": [
  0.2177734375,
  0.22607421875,
  0.23828125
 ],
 "duree_s": 2.4665653705596924
}
  ```

### 🤖 Assistant

⏵ Launching the first seed of both arms (French vs four sources) on the two GPUs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p work/n2d && \\\nCUDA_VISIBLE_DEVICES=0 PYTHONPATH=. nohup ~/gpu-env/bin/python tools/distiller_budget.py \\\n  --corpus fr --stages \"128:10000:1e-4,128:10000:3e-5\" --lot 16 --graine 1 \\\n  --sortie work/n2d/A-fr-g1.pt --l … [445 caractères tronqués]`

  ```
A g1 pid 9358
B g1 pid 9449
  ```

- **bash** `{"command": "sleep 150; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== A ===\"; tail -3 work/n2d/A-fr-g1.log 2>/dev/null; echo \"=== B ===\"; tail -3 work/n2d/B-multi-g1.log 2>/dev/null; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader", "description": … [33 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-48]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== A ===\"; tail -2 work/n2d/A-fr-g1.log 2>/dev/null; echo \"=== B ===\"; tail -2 work/n2d/B-multi-g1.log 2>/dev/null; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader", "description": "Check tra … [12 caractères tronqués]`

  ```
=== A ===
pas   500 · seq 128 · perte 73.1487 · PPL 128/4 2.8929 · 33 s
pas   750 · seq 128 · perte 72.3916 · PPL 128/4 2.8508 · 50 s
=== B ===
pas   500 · seq 128 · perte 145.5955 · PPL 128/4 3.3868 · 34 s
pas   750 · seq 128 · perte 124.0605 · PPL 128/4 3.4512 · 51 s
0, 1164 MiB, 82 %
1, 1164 MiB, 78 %
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -30 reports/INDEX.md; echo \"...\"; grep -n \"n2-\" reports/INDEX.md | head", "description": "Inspect reports index format"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **364 fiches**. Les fichiers
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
… [1959 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat 9f1dcaae | head -20; echo \"=== message ===\"; git log -1 --format=%B 9f1dcaae", "description": "Review last commit structure"}`

  ```
commit 9f1dcaae0a2096d866b81e9e146c9addd26915ae
Author: Stéphane <stephane@localhost>
Date:   Sat Oct 31 17:02:06 2026 -0400

    N2 — LES POINTS DE CONTRÔLE SONT CONSERVÉS SUR DEUX DISQUES (1,4 GO, EMPREINTES VÉRIFIÉES)
    
    Les poids de N2 vivaient dans /tmp, un tmpfs vidé à chaque démarrage — c'est ce qui a coûté les
    deux heures de reconstruction du dispositif. La campagne est désormais archivée : 1,4 Go et
    65 fichiers sur Data13TB (2 To libres), répliqués sur le disque IA (autre périphérique), avec
    MANIFESTE.sha256 vérifié et archive n2-2026-10-31.tar.zst testée. Restauration essayée : un point
    de contrôle extrait de l'archive porte la même empreinte que dans le manifeste.
    
    À côté : 232 transcripts de sessions (413 Mo) et un bundle git du dépôt (31 Mo, historique
    complet). rclone 1.75.2 est installé et vérifié contre la somme de la release ; l'envoi hors site
    attend l'autorisation du compte Google. Le script sauve-drave.sh refait tout cela en une commande.

 docs/pilotage/en-cours.md           |  7 ++++---
 journal/2026-10-31/README.md        |  4 +++-
 journal/2026-10-31/apprentissage.md | 29 +++++++++++++++++++++++++++++
 journal/THEMES.md 
… [881 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"369\\|437\\|fichiers / JSON\\|reports/\\*.md\" tools/revue_documentation.py | head -20", "description": "Check documentation review invariants"}`

  ```
176:    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
187:        alertes.append("compteurs : la ligne « fichiers / JSON » manque dans en-cours.md")
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 150,215p tools/revue_documentation.py", "description": "Read review counters logic"}`

  ```
if retard and not etat_modifie(RACINE):
        etat, _fait, lignes = retard
        if etat == "absent":
            alertes.append("fraîcheur : en-cours.md n'a jamais été commité")
        else:
            alertes.append(
                f"fraîcheur : {len(lignes)} fait(s) commité(s) après le dernier état "
                f"({etat[1]}) — mettre en-cours.md à jour"
            )

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
    portes = ex
… [2025 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in A-fr-g1 B-multi-g1; do echo \"== $f ==\"; tail -1 work/n2d/$f.log; done; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader", "description": "Poll training progress"}`

  ```
== A-fr-g1 ==
pas  1000 · seq 128 · perte 68.3328 · PPL 128/4 2.7952 · 66 s
== B-multi-g1 ==
pas  1000 · seq 128 · perte 115.1838 · PPL 128/4 3.5248 · 68 s
0, 1164 MiB, 83 %
1, 1164 MiB, 83 %
  ```

### 🤖 Assistant

⏵ Adding a balanced-quota variant: the manifest is 82% English windows

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/distiller_budget.py'); s=p.read_text()\ns=s.replace('''    def __init__(self, manifeste: str, seq_max: int = 256):\n        m = json.loads(pathlib.Path(manifeste).read_text())' … [2169 caractères tronqués]`

  ```
ok
14:                    reconstruit à l'identique (quotas + ordre de van der Corput).
67:    def __init__(self, manifeste: str, quotas: str = "proportionnel", seq_max: int = 256):
69:        self.mode = quotas
78:        if quotas == "equilibre":
79:            quotas = {s["source"]: self.max_fenetres // len(sources) for s in sources}
81:            quotas = {s["source"]: max(1, round(self.max_fenetres * s["fenetres"] / total))
85:            q = quotas[s["source"]]
92:        if quotas == "proportionnel":
141:    ap.add_argument("--quotas", choices=("proportionnel", "equilibre"), default="proportionnel",
186:        corpus = CorpusMulti(a.manifeste, a.quotas)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, re\np=pathlib.Path('tools/distiller_budget.py'); s=p.read_text()\ns=s.replace('''        if quotas == \"equilibre\":\n            quotas = {s[\"source\"]: self.max_fenetres // len(sources) for s in  … [862 caractères tronqués]`

  ```
ok
    i = torch.tensor(departs_vdc(compteur, n, len(data) - seq - 2, seq), dtype=torch.long)
    return torch.stack([data[j:j + seq + 1] for j in i]).to(device)


class CorpusMulti:
    """Fenêtres multi-sources reconstruites depuis le manifeste (offsets seuls)."""

    def __init__(self, manifeste: str, quotas: str = "proportionnel", seq_max: int = 256):
        m = json.loads(pathlib.Path(manifeste).read_text())
        self.mode = quotas
        self.fenetre, self.pas, self.max_fenetres = m["fenetre"], m["pas"], m["fenetres"]
        self.fichiers = {s["source"]: pathlib.Path(s["source"]).read_bytes()
                         for s in m["sources"]}
        sources = m["sources"]
        total = sum(s["fenetres"] for s in sources)
        # `round` reproduit le manifeste (49 999 fenêtres) ; `//` en perdait deux.
        # Le manifeste est **proportionnel** : l'anglais y prend 41 257 des 49 999
        # fenêtres (82 %). `equilibre` donne le même quota à chaque source.
        if self.mode == "equilibre":
            par_source = {s["source"]: self.max_fenetres // len(sources) for s in sources}
        else:
            par_source = {s["source"]: max(1, round(self.max_fenetres * 
… [994 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in A-fr-g1 B-multi-g1; do echo \"== $f ==\"; tail -1 work/n2d/$f.log; done", "description": "Poll training progress again"}`

  ```
== A-fr-g1 ==
pas  1500 · seq 128 · perte 66.3886 · PPL 128/4 2.7499 · 99 s
== B-multi-g1 ==
pas  1250 · seq 128 · perte 120.9031 · PPL 128/4 3.5366 · 84 s
  ```

- **bash** `{"command": "date; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -1 work/n2d/A-fr-g1.log; tail -1 work/n2d/B-multi-g1.log", "description": "Check current date and progress"}`

  ```
sam 31 oct 2026 17:27:01 EDT
pas  1500 · seq 128 · perte 66.3886 · PPL 128/4 2.7499 · 99 s
pas  1500 · seq 128 · perte 117.4079 · PPL 128/4 3.5682 · 100 s
  ```

### 🤖 Assistant

⏵ Queueing the remaining seeds and the curriculum stage for both GPUs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2d/file-gpu0.sh <<'EOF'\n#!/bin/bash\n# GPU 0 : A (français) graines 2 et 3, puis le curriculum 129 sur chaque graine.\nset -u\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nexport CUDA_VISIBLE_DEVICES=0 PYTHONPATH= … [1866 caractères tronqués]`

  ```
queue0 9964
queue1 9965
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,60p docs/methode/portes.md", "description": "Read gates method"}`

  ```
# Les portes : lancer, lire le verdict, ne pas se tromper de rouge

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.

## La commande

```bash
bash tools/toutes-les-portes.sh
```

Elle lance **toutes** les `tools/porte-*.sh`, séquentiellement, **sans s'arrêter à la première rouge** (on veut le
tableau, pas la première tuile), et borne **chaque** porte à `DELAI=1800` s. Durée observée d'une passe complète :
**1 h 30 – 2 h** sur Hauru (**49 portes** ; certaines entraînent de petits modèles, d'autres utilisent les GPU ;
`porte-deepseek` est **hors réseau** et rapide). La dernière passe complète à **49 portes** (28/10 00 h 12) a donné
**46 vertes, 3 rouges** ; la liste et le diagnostic sont dans
[`references-non-regression.md`](../pilotage/references-non-regression.md). `porte-deepseek` est **incluse** et verte.

## Où est le registre (et comment lire le verdict)

Le registre n'est **pas** à la racine : il est écrit dans le dossier des journaux, par défaut
`/tmp/portes-<date>-<heure>/registre.txt` (variable `JOURNAUX`). Chaque ligne vaut :

```
nom-de-la-porte   code-de-sortie   durée-en-secondes
```

On lit le verdict 
… [1655 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. ~/gpu-env/bin/python work/n2d/calibrer.py \\\n  /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/temoin-g1.pt \\\n  /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/temoin-g2.pt \\\n  /hom … [252 caractères tronqués]`

  ```
{"fichier": "temoin-g1.pt", "ppl_128_lot16": 2.9406, "ppl_128_lot8": 2.9399, "ppl_129_lot15": 2.9631}
{"fichier": "temoin-g2.pt", "ppl_128_lot16": 2.9345, "ppl_128_lot8": 2.9369, "ppl_129_lot15": 2.961}
{"fichier": "temoin-g3.pt", "ppl_128_lot16": 2.9313, "ppl_128_lot8": 2.9298, "ppl_129_lot15": 2.9628}
{"fichier": "drave-n0-base-20k.pt", "ppl_128_lot16": 3.2161, "ppl_128_lot8": 3.2296, "ppl_129_lot15": 3.2653}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in A-fr-g1 B-multi-g1; do echo \"== $f ==\"; tail -2 work/n2d/$f.log; done; ls -la work/n2d/*.json 2>/dev/null", "description": "Check whether seed 1 runs finished"}`

  ```
== A-fr-g1 ==
pas  1750 · seq 128 · perte 62.2280 · PPL 128/4 2.7311 · 116 s
pas  2000 · seq 128 · perte 70.6559 · PPL 128/4 2.7148 · 133 s
== B-multi-g1 ==
pas  1750 · seq 128 · perte 119.7154 · PPL 128/4 3.5746 · 117 s
pas  2000 · seq 128 · perte 116.7664 · PPL 128/4 3.5804 · 134 s
-rw-r--r--. 1 stephane stephane 610 31 oct 17:24 work/n2d/essai-fr.json
-rw-r--r--. 1 stephane stephane 650 31 oct 17:24 work/n2d/essai-multi.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2d/agrege.py <<'EOF'\n#!/usr/bin/env python3\n\"\"\"Agrège les runs N2.d : moyenne, écart-type, étendue par bras.\"\"\"\nimport glob, json, pathlib, statistics as st\n\nBRAS = {\n    \"fr\": \"A — français seul (41 Mo)\", … [1874 caractères tronqués]`

  ```
ok
  ```

### 👤 Utilisateur

background job bash-48 (bash: sleep 150; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo "=== A ==="; tail -3 work/n2d/A-fr-g1.log 2>/dev/null; echo "=== B ==="; tail -3 work/n2d/B-multi-g1.log 2>/dev/null; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la work/n2d/*.json 2>/dev/null | tail -5; echo \"=== logs ===\"; for f in A-fr-g1 B-multi-g1 A-fr-g2 B-multi-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check completion of seed 1 and start  … [11 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 610 31 oct 17:24 work/n2d/essai-fr.json
-rw-r--r--. 1 stephane stephane 650 31 oct 17:24 work/n2d/essai-multi.json
=== logs ===
-- A-fr-g1
pas  2250 · seq 128 · perte 58.9078 · PPL 128/4 2.7067 · 151 s
-- B-multi-g1
pas  2250 · seq 128 · perte 109.0897 · PPL 128/4 3.5626 · 151 s
-- A-fr-g2
-- B-multi-g2
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat journal/2026-10-31/apprentissage.md; echo \"=== README jour ===\"; head -40 journal/2026-10-31/README.md", "description": "Read today's journal theme file"}`

  ```
# 2026-10-31 — Règles locales, hebbien, modulateurs, distillation

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (1)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 16:38 | `660c479c` | N2 — LA HIÉRARCHIE NE PAIE PAS SUR LA DISTILLATION NON PLUS (2,9935 CONTRE 2,9927, TROIS GRAINES) | `en-cours.md`, `README.md`, `distribue.md` (+4) |

## Chiffres du jour

`2,9935` · `2,9927`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `22e518ee-81b8-4081-ae1b-f0d7a777a1d7` — Compléter les autres sessions avant le backlog (début 2026-10-31 11:13, 0.2 h) → [rapport](../sessions/22e518ee-81b8-4081-ae1b-f0d7a777a1d7/rapport.md) · [digest](../sessions/22e518ee-81b8-4081-ae1b-f0d7a777a1d7/digest.md)

## Mesures et rapports touchés

- [reports/rapport-n2-distillation.md](../../reports/rapport-n2-distillation.md)

<!
… [2076 caractères tronqués]
  ```

- **bash** `{"command": "env | grep -i -E \"dsh|session\" | head -20; echo \"=== journal_auto usage ===\"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,40p tools/journal_auto.py; echo \"=== sessions ===\"; ls journal/sessions | tail -5", "description": "Check DSH session env and journal toolin … [3 caractères tronqués]`

  ```
SESSION_MANAGER=local/Hauru:@/tmp/.ICE-unix/3616,unix/Hauru:/tmp/.ICE-unix/3616
XDG_SESSION_PATH=/org/freedesktop/DisplayManager/Session2
DSH_PROFILE=dsh-tui
SHELL_SESSION_ID=1c8b3614707743c9b05fd06114b64381
DSH_PROFILE_DIR=/home/stephane/.dsh/profiles/dsh-tui
DESKTOP_SESSION=plasma6
DSH_SHELL=1
XDG_SESSION_DESKTOP=KDE
XDG_SESSION_TYPE=x11
DSH_SESSION_ID=0b0a6a0d-05f5-4308-800c-4792ddb9cbf2
MEMORY_PRESSURE_WATCH=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-ksmserver.service/memory.pressure
KONSOLE_DBUS_SESSION=/Sessions/1
XSESSION_IS_UP=yes
KDE_SESSION_UID=1000
XDG_SESSION_CLASS=user
KDE_SESSION_VERSION=6
XDG_SESSION_ID=4
DSH_HOME=/home/stephane/.dsh
KDE_FULL_SESSION=true
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
=== journal_auto usage ===
#!/usr/bin/env python3
"""journal_auto.py — le journal quotidien, ÉCRIT PAR JOUR (UN DOSSIER) ET PAR THÈME, à partir de git et des sessions.

POURQUOI. Le journal doit consigner les **événements datés** (voir
`docs/organisation-du-depot.md`), et une journée de ce dépôt est trop riche pour un seul
fichier : un jour touche le moteur, les protocoles, les mesures, les portes et la
documentation. D'où le
… [1588 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal/sessions/N2-GPU/; echo \"=== plan ===\"; cat journal/sessions/N2-GPU/plan.md 2>/dev/null | head -40", "description": "Read an existing session plan"}`

  ```
plan.md
rapport.md
=== plan ===
# Plan de session — N2-GPU

> **Mandat confirmé** le 2026-10-30 13:05 depuis `en-cours` — le heartbeat est celui de
> l'état ; la session le met à jour à chaque cycle.

- **Session** : `N2-GPU`
- **Rôle** : calcul : distillation
- **Périmètre** : N2
- **Fichiers réservés** : `models/`, `data/`, `reports/n2-*`
- **Heartbeat** : 2026-10-30 13:05 HAE
- **Prochaine action** : N2 — la **hiérarchie** (état de section), porte **< 2,5** (meilleur **2,6998**, plateau **2,708**) ; **N5 gelé**.
- **État** : terminé
  ```

- **write** `{"content": "# Plan de session — N2-budget\n\n> **Mandat ouvert** le 2026-10-31 17 h 35 HAE depuis [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md)\n> — le heartbeat est celui de l'état ; la session le met à jour à chaque cycle.\n\n- **Session** : `0b0a6a0d-05f5-4308-800c-4792ddb9cb … [821 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work/n2d/*.json | tail -4; for f in A-fr-g1 B-multi-g1 A-fr-g2 B-multi-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done; date", "description": "Check seed 1 results"}`

  ```
work/n2d/essai-fr.json
work/n2d/essai-multi.json
-- A-fr-g1
pas  2500 · seq 128 · perte 68.8635 · PPL 128/4 2.6890 · 168 s
-- B-multi-g1
pas  2500 · seq 128 · perte 113.9989 · PPL 128/4 3.6012 · 168 s
-- A-fr-g2
-- B-multi-g2
sam 31 oct 2026 17:28:08 EDT
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,25p tools/index_reports.py", "description": "Read reports index generator"}`

  ```
#!/usr/bin/env python3
"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.

L'index est **exhaustif** et **déterministe** : une ligne par fiche, triée par nom,
avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
et `historique-*`) sont exclus du tableau ; les compteurs de `docs/en-cours.md`
comptent, eux, tous les `.md` de `reports/`.
"""
from __future__ import annotations
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent


def titre(p: pathlib.Path) -> str:
    for ligne in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if ligne.startswith("# "):
            return ligne[2:].strip().replace("|", "—")
    return p.stem.replace("-", " ")


def main() -> int:
    fiches = sorted(
        p for p in (RACINE / "reports").glob("*.md")
        if p.name not in ("README.md", "INDEX.md") and not p.name.startswith("historique-")
  ```

- **bash** `{"command": "sleep 45; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work/n2d/*.json | grep -v essai; for f in A-fr-g1 B-multi-g1; do echo \"-- $f\"; tail -1 work/n2d/$f.log; done", "description": "Wait and check run completion"}`

  ```
-- A-fr-g1
pas  3250 · seq 128 · perte 73.3329 · PPL 128/4 2.6767 · 218 s
-- B-multi-g1
pas  3250 · seq 128 · perte 97.8212 · PPL 128/4 3.6275 · 219 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"N2\" docs/pilotage/backlog/index.md | head -10; echo \"=== graphe ===\"; grep -n \"N2\" docs/pilotage/backlog/dependances.md | head -10", "description": "Check backlog index N2 entries"}`

  ```
57:| R11 | [Contexte hiérarchique et état de section](R11-contexte-hierarchique.md) | spécifiée | P1 | R01, N1, N2 | R1.1 |
79:| N2 | [Distillation native (50 000 séquences)](N2-distillation.md) | en cours | P1 | N1 | N2 |
=== graphe ===
24:où il est bloqué : `R11` dépendait de `N2`, qui plafonne à **2,708** — alors que la hiérarchie est
25:justement le levier que `N2` n'a pas encore essayé.
87:| **N2** | en cours | N1 (acquis) | — | N5, R11 | [N2-distillation.md](N2-distillation.md) |
89:| **N4** | partiel | — | N2 (plafond) | N5 | [N4-usage-sft.md](N4-usage-sft.md) |
90:| **N5** | sans fiche | N2 (dure), N4 (dure) | — | — | — |
103:| **R11** | spécifiée | R01 (dure), N1 (acquis), N2 (dure) | — | R12, R21 | [R11-contexte-hierarchique.md](R11-contexte-hierarchique.md) |
105:| **R13** | mesurée | — | N2 (plafond) | — | [R13-tokenisation-bpe.md](R13-tokenisation-bpe.md) |
163:| **N2** | en cours | `N1` acquis | la **hiérarchie** (état de section, 3 graines) ; porte **< 2,5** |
165:| **N4** | partiel | aucune arête dure ; `N2` est un plafond | la **consigne courte**, tenue à l'écart |
169:qui porte** ; `N5` attend `N2` et `N4` ; R1/R2/R3 attendent **N2** et le banc ; les lignes
  ```

- **bash** `{"command": "sleep 40; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work/n2d/*.json | grep -v essai; for f in A-fr-g1 B-multi-g1; do echo \"-- $f\"; tail -1 work/n2d/$f.log; done", "description": "Check if seed 1 finished"}`

  ```
-- A-fr-g1
pas  4000 · seq 128 · perte 59.3033 · PPL 128/4 2.5815 · 268 s
-- B-multi-g1
pas  4000 · seq 128 · perte 90.4789 · PPL 128/4 3.6719 · 269 s
  ```

### 👤 Utilisateur

je vais démarer une session en parallèle. est-ce que en-cours.md est à jour pour que l'autrre session travaille sans conflit avec toi?

### 🤖 Assistant

⏵ Mettant `en-cours` à jour pour déclarer ma session et la carte des conflits

Non — il ne l'était pas : la page datait de 17 h 15 et disait encore « aucune session active ». Je le corrige tout de suite, avec ma session, mes fichiers réservés et ce qu'une autre session peut prendre sans collision.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%Y-%m-%d %H h %M HAE' && tail -1 work/n2d/A-fr-g1.log && tail -1 work/n2d/B-multi-g1.log", "description": "Check time and campaign progress"}`

  ```
2026-10-31 17 h 30 HAE
pas  4500 · seq 128 · perte 56.7976 · PPL 128/4 2.5701 · 302 s
pas  4250 · seq 128 · perte 86.4410 · PPL 128/4 3.6647 · 286 s
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-10-31, 17 h 15 HAE (heure locale, EDT).**", "new_string": "**Mis à jour : 2026-10-31, 17 h 30 HAE (heure locale, EDT).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "### Session active — N2, le budget complet (`0b0a6a0d`)\n\n- **Id** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — mandat dans\n  [`plan.md`](../../journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9c … [2826 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\ns=s.replace(\"\"\"  suite : curriculum et capacité.\"\"\",\"\"\"  suite : **campagne budget et données en cours** (`0b0a6a0d`, deux GPU) … [577 caractères tronqués]`

  ```
ok
  en-cours · 1268 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ❌ 1 anomalie(s) :
     · session « Session active — N2, le budget complet (`0b0a6a0d`) » ne dit pas « **Ce que font les autres** »
exit=1
  avertissements :
     · 14 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 1 violation(s) :
     · T0 : 4047 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"T0\\|tache\\|budget\" tools/taille_documents.py | head -20", "description": "Check context budget composition"}`

  ```
2:"""taille_documents.py — le budget de contexte et la cohésion des documents.
5:  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
11:Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
12:ils ne sont pas chargés automatiquement. Le budget est en **mots** ; l'estimation de tokens
16:elles ne comptent pas dans le budget ; le document les porte, la page montre le SVG.
25:# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
27:    ("T0", "AGENTS.md", 1200),
28:    ("T0", "docs/pilotage/en-cours.md", 2000),
32:    ("T0", "docs/methode/*.md", 1200),
77:#: pas dans le budget de contexte. Le rendu (docwatch) est ce que voit le lecteur ;
90:    for cat, motif, budget in BUDGETS:
92:            return cat, budget
101:    for cat, motif, budget in BUDGETS:
110:            lignes.append((n, t.count("\n") + 1, rel, cat, budget))
112:            if cat in ("T0", "T1"):
122:            if budget and n > budget:
123:                violations.append(f"{rel} : {n} mots > budget {budget} ({cat})")
140:    # T0 : la somme des trois lectures par défaut
150:        violations.appe
… [130 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 25,45p tools/taille_documents.py; sed -n 135,152p tools/taille_documents.py", "description": "Read budget category definitions"}`

  ```
# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
BUDGETS: list[tuple[str, str, int]] = [
    ("T0", "AGENTS.md", 1200),
    ("T0", "docs/pilotage/en-cours.md", 2000),
    ("T1", "docs/methode/organisation-du-depot.md", 1800),
    ("T1", "docs/methode/modularisation.md", 1600),
    ("T1", "docs/methode/relations-humaines.md", 1400),
    ("T0", "docs/methode/*.md", 1200),
    ("T1", "docs/README.md", 1000),
    ("T1", "docs/theorie/carte.md", 1100),
    ("T1", "docs/theorie/synthese/index.md", 2000),
    ("T1", "docs/theorie/synthese/0*.md", 2000),
    ("T1", "docs/pilotage/roadmap.md", 9000),
    ("T1", "docs/theorie/glossaire.md", 1500),
    ("T1", "docs/theorie/glossaire/0*.md", 5000),
    ("T1", "docs/theorie/glossaire/1*.md", 5000),
    ("T1", "docs/theorie/glossaire/README.md", 2000),
    ("T1", "docs/schemas/README.md", 1500),
    ("CARTE", "docs/theorie/glossaire/entrees/*.md", 150),
    ("T1", "reports/README.md", 2800),
    ("T1", "README.md", 3500),
        avertissements.append(
            f"{len(longues)} fiche(s) > 300 lignes : lire le verdict + une section, jamais tout "
            f"(plus longues : {', '.join(f'{n} l. {nom
… [591 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\ndebut = s.index(\"### Session active — N2, le budget complet\")\nfin = s.index(\"> **Sessions archivées**\")\nnouveau = \"\"\"### Sessio … [1346 caractères tronqués]`

  ```
ok
  en-cours · 1200 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ❌ 2 anomalie(s) :
     · session « Session active — N2, le budget complet (`0b0a6a0d`) » ne dit pas « **Ce qu'elle fait** »
     · session « Session active — N2, le budget complet (`0b0a6a0d`) » ne dit pas « **Journal** »
  avertissements :
     · 14 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nfrom taille_documents import mots_hors_diagrammes\nfrom pathlib import Path\na=mots_hors_diagrammes(Path('AGENTS.md').read_text())\ne=mots_hors_diagrammes(Path('docs/pilotage … [213 caractères tronqués]`

  ```
1200 1200 1579 T0= 3979 marge= 21
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\ndebut = s.index(\"### Session active — N2, le budget complet\")\nfin = s.index(\"> **Sessions archivées**\")\nnouveau = \"\"\"### Sessio … [2203 caractères tronqués]`

  ```
ok
  en-cours · 1176 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
     · 14 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,50p tools/verifie_etat_a_jour.py; echo \"=== hook ===\"; cat .git/hooks/pre-commit 2>/dev/null | head -20", "description": "Inspect pre-commit state hook"}`

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
… [1872 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md journal/README.md && git commit -m \"ÉTAT — LA CAMPAGNE N2 BUDGET ET DONNÉES EST OUVERTE, LES GPU RÉSERVÉS JUSQU'À 19 h 40\n\nUne seconde … [867 caractères tronqués]`
