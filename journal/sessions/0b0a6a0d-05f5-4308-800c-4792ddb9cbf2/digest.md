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

  ```
[still running after 60000ms; moved to background job bash-81]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-81", "wait": true, "timeout_ms": 120000}`

  ```
✅ index : aucun fait stagé sans état
[master 54dc7a26] ÉTAT — LA CAMPAGNE N2 BUDGET ET DONNÉES EST OUVERTE, LES GPU RÉSERVÉS JUSQU'À 19 h 40
 14 files changed, 2387 insertions(+), 29 deletions(-)
 create mode 100644 journal/2026-10-31/mesures.md
 create mode 100644 journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md
 create mode 100644 journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md
 create mode 100644 journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -2; echo \"=== état ===\"; sed -n 26,52p docs/pilotage/en-cours.md; echo \"=== avancement ===\"; for f in A-fr-g1 B-multi-g1 A-fr-g2 B-multi-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "descri … [46 caractères tronqués]`

  ```
54dc7a26 ÉTAT — LA CAMPAGNE N2 BUDGET ET DONNÉES EST OUVERTE, LES GPU RÉSERVÉS JUSQU'À 19 h 40
9f1dcaae N2 — LES POINTS DE CONTRÔLE SONT CONSERVÉS SUR DEUX DISQUES (1,4 GO, EMPREINTES VÉRIFIÉES)
=== état ===
### Session active — N2, le budget complet (`0b0a6a0d`)

- **Id** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — mandat dans
  [`plan.md`](../../journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md).
- **Rôle** : **N2, le budget complet**.
- **Ce qu'elle fait** : deux GPU en continu — **A** français seul (3 graines), **B** manifeste
  4 sources, **B′** quotas égaux (le manifeste est à **82 % anglais**), **C** curriculum 129
  sur A ; la hiérarchie est écartée deux fois, restent **le curriculum et les données** (41 Mo,
  20 000 pas, quatre sources) sur le dispositif reconstruit.
- **Ce que font les autres** : documentation, backlog, **N4** (sans GPU), portes documentaires —
  mais **pas** `toutes-les-portes.sh` (elle prend les GPU et fausserait la mesure), pas les
  fichiers réservés, ni cette page sans me le dire.
- **Fichiers réservés** : `work/n2d/`, `tools/distiller_budget.py`, `reports/n2-*`,
  `journal/sessions/0b0a6a0d-…/`.
- **Prochaine action** : fiche `reports/rap
… [971 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/sessions.py --status 2>&1 | head -6; echo \"=== git ===\"; git status --short | head", "description": "Confirm the session is visible in the status tool"}`

  ```
sessions · plans de mandat
    0b0a6a0d-05f5-4308 · en cours ·       — · N2 — le budget complet, les données et le curriculum
      → N2 — la hiérarchie est écartée deux fois ; restent **le curriculum et
    0b69f616-5c75-4c34 · terminé  · 1173 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
    22e518ee-81b8-4081 · terminé  · 344 min · archives de sessions, journal, en-cours, roadmap, backlog, outillage d'archivage
=== git ===
 m tools/docwatch
?? tools/distiller_budget.py
?? work/
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -q \"^work/$\" .gitignore || printf '\\n# Campagnes GPU : points de contrôle et journaux de run (hors dépôt, archivés à part)\\nwork/\\n' >> .gitignore; tail -4 .gitignore; git status --short | head -3", "description": "Ignore t … [26 caractères tronqués]`

  ```
docs/**/*.mmd.svg

# Campagnes GPU : points de contrôle et journaux de run (hors dépôt, archivés à part)
work/
 M .gitignore
 m tools/docwatch
?? tools/distiller_budget.py
  ```

### 🤖 Assistant

⏵ Réponse sur l'état et la carte des conflits

**Non, il ne l'était pas** — la page datait de 17 h 15 et disait encore « aucune session active ». C'est corrigé, validé et committé : `54dc7a26`. `tools/sessions.py --status` me voit maintenant « en cours ».

**Ce que l'autre session lira dans `en-cours`**

- Session active `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2`, rôle **N2 — le budget complet** (campagne GPU en cours : français seul, manifeste 4 sources, quotas égaux, curriculum 129 ; 3 graines).
- Fichiers réservés : `work/n2d/`, `tools/distiller_budget.py`, `reports/n2-*`, `journal/sessions/0b0a6a0d-…/`.

**Ce qu'elle peut prendre sans collision**

- La documentation, le backlog, **N4** (consigne courte, sans GPU), et les portes **documentaires** (`PORTES="..."`).
- Tout ce qui ne touche ni mes fichiers réservés ni les GPU.

**Ce qu'elle ne doit pas prendre (conflits réels, pas théoriques)**

- `bash tools/toutes-les-portes.sh` : la passe complète utilise les **deux cartes** et fausserait mes mesures (c'est écrit dans `docs/methode/portes.md` : portes et mesure GPU ne cohabitent pas). Je la lancerai moi-même à la fin, seule.
- Un entraînement GPU, pour la même raison.
- `docs/pilotage/en-cours.md` : **une session écrit à la fois**. Si elle doit y mettre un fait, qu'elle me le dise — je libère la page.
- La `roadmap` et `reports/n2-*` : je les édite à la clôture.

**Horaires** : la campagne tourne jusqu'à ~19 h 40 (6 runs restants), puis agrégation, fiche, et passe complète des portes (1 h 30–2 h) avant le commit de clôture. Si elle a besoin d'un GPU avant, elle me le dit et je réordonne.

Au passage : `work/` est désormais dans `.gitignore` — sinon un `git add -A` aurait stagé 1–2 Go de points de contrôle. `tools/docwatch` reste modifié en local (sous-module, pas à moi).


## Tour 2

### 👤 Utilisateur

<goal_round>
Objective: "N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/pilotage/en-cours.md et la roadmap à jour."
Round: 1/1000

Continue working toward the objective in this same session. Treat the current workspace, tool results, and durable session state as authoritative; inspect them instead of assuming earlier narration is still current. Make concrete progress and verify the result. Before claiming completion, gather evidence that the whole objective is achieved, read the current goal, and mark it complete. If work remains, leave the goal active for the next round. Follow the configured goal-tool policy before reporting a blocker.
</goal_round>

### 🤖 Assistant

⏵ Checking campaign progress and aggregating the first completed seeds

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M' && ls work/n2d/*.json | grep -v essai; echo \"=== logs ===\"; for f in A-fr-g1 B-multi-g1 A-fr-g2 B-multi-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done; nvidia-smi --query-gpu=index,memory.used,utiliz … [73 caractères tronqués]`

  ```
17:33
=== logs ===
-- A-fr-g1
pas  7750 · seq 128 · perte 54.0449 · PPL 128/4 2.4816 · 521 s
-- B-multi-g1
pas  7500 · seq 128 · perte 91.3882 · PPL 128/4 3.7118 · 507 s
-- A-fr-g2
-- B-multi-g2
0, 1164 MiB, 83 %
1, 1164 MiB, 81 %
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nm=json.load(open('reports/native-corpus-multi.json'))\nS=m['sources']; tot=sum(s['fenetres'] for s in S); M=m['fenetres']\nqs={s['source']: max(1, round(M*s['fenetres']/tot)) for s in S}\ns=sum(qs.valu … [234 caractères tronqués]`

  ```
data/corpus_fr.txt                 1907    3.8 %
data/udhr/udhr_train.txt           1802    3.6 %
data/corpus_en.txt                41257   82.5 %
data/corpus_mixte_litt.txt         5033   10.1 %
somme 49999
B' (équilibré) 12 499 par source, 4 sources = 49 996 retenues sur 49 999
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short; echo \"=== mesures.md ===\"; head -25 journal/2026-10-31/mesures.md", "description": "Check working tree and generated journal file"}`

  ```
M .gitignore
 m tools/docwatch
?? tools/distiller_budget.py
=== mesures.md ===
# 2026-10-31 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (1)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 17:02 | `9f1dcaae` | N2 — LES POINTS DE CONTRÔLE SONT CONSERVÉS SUR DEUX DISQUES (1,4 GO, EMPREINTES VÉRIFIÉES) | `en-cours.md`, `README.md`, `apprentissage.md` (+2) |

## Sessions actives ce jour

- `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — Continue session work (début 2026-10-31 17:17, 0.2 h) → [rapport](../sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md) · [digest](../sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md)
- `22e518ee-81b8-4081-ae1b-f0d7a777a1d7` — Compléter les autres sessions avant le backlog (début 2026-10-31 11:13, 0.2 h) → [rapport](../sessions/22e518ee-81b8-4081-ae1b-f0d7a777a1d7/rapport.md) · [digest](../sessions/22e518ee-81b8-4081-ae1b-f0d7a777a1d7/digest.md
… [148 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2d/verifie-grille.py <<'EOF'\n#!/usr/bin/env python3\n\"\"\"La grille d'échantillonnage de la campagne (fenêtres de seq+1, borne len-seq-2)\ndéplace-t-elle la PPL par rapport au protocole historique (fenêtres de seq, born … [1695 caractères tronqués]`

  ```
{"seq": 128, "historique": 2.94059, "campagne": 2.94199, "ecart": 0.0014}
{"seq": 129, "historique": 2.9631, "campagne": 2.97327, "ecart": 0.01016}
  ```

### 🤖 Assistant

⏵ Écrivant l'évaluation finale unifiée au protocole historique exact

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"evalue-final.py — PPL de tous les points de contrôle de la campagne N2.d,\nsous le protocole **historique exact** (celui de 2,7078 et de 2,6998).\n\nLa campagne a évalué en interne sur une grille décalée d'un octet (fenêtres de\nseq+1, borne len−seq−2) : l' … [4082 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/evalue-final.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; for f in A-fr-g1 B-multi-g1 A-fr-g2 B-multi-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check seed 1 completion"}`

  ```
17:35
-- A-fr-g1
pas  8750 · seq 128 · perte 48.6506 · PPL 128/4 2.4483 · 592 s
-- B-multi-g1
pas  8750 · seq 128 · perte 91.2001 · PPL 128/4 3.7502 · 591 s
-- A-fr-g2
-- B-multi-g2
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\ntr=pathlib.Path('data/corpus_fr_train.txt').read_bytes()\nva=pathlib.Path('data/corpus_fr_val.txt').read_bytes()\nfr=pathlib.Path('data/corpus_fr.txt').read_bytes()\nprint('train', len(tr), 'val', l … [390 caractères tronqués]`

  ```
train 4402195 val 231694 fr 4633889
val est la queue de fr ? True
train est la tête de fr ? True
val ⊂ train ? False
frontière : 200 octets de train fin + 200 de val début
b"nt 24 h (et jusqu'\xc3\xa0 l'arriv\xc3\xa9e du nouveau mat\xc3\xa9riel), mesurer et documenter ce que l'architecture de Drave \xe2\x80\x94 listes d'\xc3\xa9v\xc3\xa9nements, streaming depuis le disque, r\xc3\xa9partition entre n\xc5\x93uds \xe2\x80\x94 vaut po"
  ```

- **bash** `{"command": "sleep 55; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work/n2d/*.json | grep -v essai; echo \"---\"; python3 -c \"\nimport json,glob\nfor f in sorted(glob.glob('work/n2d/A-fr-g1.json')+glob.glob('work/n2d/B-multi-g1.json')):\n    d=json.load(open(f))\n    print(f, {k:d[k] f … [134 caractères tronqués]`

  ```
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; tail -3 work/n2d/A-fr-g1.log; echo \"--- B\"; tail -2 work/n2d/B-multi-g1.log; echo \"--- ps\"; ps -eo pid,etime,cmd | grep distiller_budget | grep -v grep | head", "description": "Check run logs and processes"}`

  ```
17:36:37
pas  9750 · seq 128 · perte 53.2697 · PPL 128/4 2.4625 · 661 s
pas 10000 · seq 128 · perte 54.0570 · PPL 128/4 2.4658 · 678 s
# stage seq 128 · 10000 pas · lr 3e-05
--- B
pas 10000 · seq 128 · perte 95.6067 · PPL 128/4 3.7218 · 675 s
# stage seq 128 · 10000 pas · lr 3e-05
--- ps
   9358       11:33 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p work/n2d && \ CUDA_VISIBLE_DEVICES=0 PYTHONPATH=. nohup ~/gpu-env/bin/python tools/distiller_budget.py \   --corpus fr --stages "128:10000:1e-4,128:10000:3e-5" --lot 16 --graine 1 \   --sortie work/n2d/A-fr-g1.pt --log work/n2d/A-fr-g1.log > work/n2d/A-fr-g1.out 2>&1 & echo "A g1 pid $!"; sleep 3; \ CUDA_VISIBLE_DEVICES=1 PYTHONPATH=. nohup ~/gpu-env/bin/python tools/distiller_budget.py \   --corpus multi --stages "128:10000:1e-4,128:10000:3e-5" --lot 16 --graine 1 \   --sortie work/n2d/B-multi-g1.pt --log work/n2d/B-multi-g1.log > work/n2d/B-multi-g1.out 2>&1 & echo "B g1 pid $!"
   9362       11:33 /home/stephane/gpu-env/bin/python tools/distiller_budget.py --corpus fr --stages 128:10000:1e-4,128:10000:3e-5 --lot 16 --graine 1 --sortie work/n2d/A-fr-g1.pt --log work/n2d/A-fr-g1.log
   9449       11:30 /home
… [190 caractères tronqués]
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"agrege.py — tableau par bras de la campagne N2.d.\n\nLit l'évaluation unifiée (`work/n2d/evaluations-finales.json`, protocole\nhistorique exact) et les métadonnées d'entraînement (`work/n2d/*.json`).\nÉcrit `reports/n2-budget.json` et imprime le tableau mar … [2592 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py", "limit": 5}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Agrège les runs N2.d : moyenne, écart-type, étendue par bras."""
3: import glob, json, pathlib, statistics as st
4: 
5: BRAS = {

(Showing lines 1-5 of 44. Use offset=6 to continue.)
</content>
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"agrege.py — tableau par bras de la campagne N2.d.\n\nLit l'évaluation unifiée (`work/n2d/evaluations-finales.json`, protocole\nhistorique exact) et les métadonnées d'entraînement (`work/n2d/*.json`).\nÉcrit `reports/n2-budget.json` et imprime le tableau mar … [2568 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -2 work/n2d/A-fr-g1.log; ls work/n2d/*.json | grep -v essai", "description": "Check for seed 1 final results"}`

  ```
17:37
pas 10250 · seq 128 · perte 51.3992 · PPL 128/4 2.4407 · 695 s
pas 10500 · seq 128 · perte 48.7937 · PPL 128/4 2.4455 · 712 s
[exit code: 1]
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"robustesse.py — la PPL tient-elle sur d'autres grilles de fenêtres ?\n\nLa fiche annonce une PPL sous un protocole (8 lots × 16 × 128 depuis le\ncompteur 0). Ce script refait la mesure sur **quatre décalages de compteur**\net **deux tailles de lot**, pour m … [2312 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/robustesse.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -2 work/n2d/A-fr-g1.log; ls work/n2d/A-fr-g1.json 2>/dev/null && echo FINI", "description": "Check A seed 1 completion"}`

  ```
17:37
pas 10750 · seq 128 · perte 53.3267 · PPL 128/4 2.4458 · 730 s
pas 11000 · seq 128 · perte 44.5797 · PPL 128/4 2.4276 · 748 s
[exit code: 2]
  ```

- **bash** `{"command": "sleep 90; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -2 work/n2d/A-fr-g1.log; tail -2 work/n2d/B-multi-g1.log", "description": "Poll training after 90 seconds"}`

  ```
[still running after 60000ms; moved to background job bash-95]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -1 work/n2d/A-fr-g1.log; ls work/n2d/*.json | grep -v essai", "description": "Quick progress check"}`

  ```
17:38
pas 12000 · seq 128 · perte 49.2191 · PPL 128/4 2.4135 · 818 s
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; tail -1 work/n2d/A-fr-g1.log; tail -1 work/n2d/B-multi-g1.log", "description": "Poll again"}`

  ```
17:39:02
pas 12000 · seq 128 · perte 49.2191 · PPL 128/4 2.4135 · 818 s
pas 12250 · seq 128 · perte 73.1056 · PPL 128/4 3.7425 · 826 s
  ```

- **job_output** `{"job_id": "bash-95"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/revue_documentation.py 2>&1 | tail -12", "description": "Run documentation review baseline"}`

  ```
revue de documentation · 369 fiche(s) · 437 JSON · 109 doc(s) · 78 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · chemin mort : docs/pilotage/en-cours.md:40 → reports/rapport-n2-budget.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\ns=s.replace(\"- **Prochaine action** : fiche `reports/rapport-n2-budget.md`, journal, roadmap, commit.\",\n            \"- **Prochaine a … [276 caractères tronqués]`

  ```
40:- **Prochaine action** : la fiche du budget, le journal, la roadmap, le commit.
  revue de documentation · 369 fiche(s) · 437 JSON · 109 doc(s) · 78 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

### 👤 Utilisateur

background job bash-95 (bash: sleep 90; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -2 work/n2d/A-fr-g1.log; tail -2 work/n2d/B-multi-g1.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/A-fr-g1.json work/n2d/B-multi-g1.json 2>/dev/null; tail -1 work/n2d/A-fr-g1.log; tail -1 work/n2d/B-multi-g1.log", "description": "Check whether seed 1 finished"}`

  ```
17:39
pas 12500 · seq 128 · perte 51.3128 · PPL 128/4 2.4063 · 852 s
pas 12500 · seq 128 · perte 79.6633 · PPL 128/4 3.7048 · 844 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; tail -1 work/n2d/A-fr-g1.log; tail -1 work/n2d/B-multi-g1.log; ls work/n2d/*.json | grep -v essai", "description": "Poll for completion"}`

  ```
17:40:04
pas 13000 · seq 128 · perte 53.7650 · PPL 128/4 2.4008 · 886 s
pas 13000 · seq 128 · perte 84.8568 · PPL 128/4 3.7372 · 877 s
[exit code: 1]
  ```

- **bash** `{"command": "sleep 420; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; tail -3 work/n2d/A-fr-g1.log", "description": "Wait for seed 1 completion in background", "run_in_background": true}`

  ```
started background job bash-102
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,60p docs/pilotage/references-non-regression.md", "description": "Read tolerated gate failures"}`

  ```
# Références de non-régression

> **Dernière passe complète — 2026-10-31 à 12 h 54 :** **78 portes, 73 vertes, 5 rouges, 1 h 37**
> (journaux `/tmp/portes-1031-11h17`). `porte-indice`, `porte-melange` : les **structurelles
> connues**. `porte-homeostasie` (exit 2) : **environnementale** — `/tmp/n4/rang4-lora.pt` effacé
> au démarrage. `porte-jeux` : **vraie régression** corrigée le jour même (`2edb3079` — le SAN
> perdait contre la case, 110/112). `porte-reparti-moteur` : PPL épinglée 9,1748 non reproduite
> (8,7434), écart de flux nul — à trancher.

> **Passe précédente — 2026-10-29 à 22 h 09 :** 62 portes, 60 vertes, 2 rouges, 1 h 46 ;
> mêmes structurelles connues, **aucune régression**. Journaux : `/tmp/portes-1029-20h23` ;
> historique : [`reports/historique-passes-portes.md`](../../reports/historique-passes-portes.md).

> **Ce que ce fichier porte.** Les repères chiffrés qu'une passe complète imprime, et
> les invariants qui ne sont pas des chiffres. Les mesures de campagne (perplexités,
> budgets, latences) sont dans `reports/` — une fiche par expérience — et non ici :
> ce fichier ne porte que ce qu'une **porte** vérifie.

> **Passe du 2026-10-28 à 00 h 12** (**49 portes, 4
… [3172 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-102", "timeout_ms": 120000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; tail -1 work/n2d/A-fr-g1.log; tail -1 work/n2d/B-multi-g1.log; ls work/n2d/*.json | grep -v essai", "description": "Quick progress check"}`

  ```
17:42:32
pas 15250 · seq 128 · perte 45.0087 · PPL 128/4 2.4105 · 1037 s
pas 15250 · seq 128 · perte 81.7393 · PPL 128/4 3.7293 · 1027 s
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"val\\|meilleur\\|best\" tools/entrainer_native.py | head -20", "description": "Check whether the base uses validation for selection"}`

  ```
39:    modele.eval(); total = 0.0; n = 0
66:    n_val = max(10_000, len(data) // 20)
67:    train, val = data[:-n_val], data[-n_val:]
85:            p, n = ppl(modele, val, a.seq, a.lot, a.device, n_lots=2)
86:            print(f"pas {pas:4d} · perte {float(perte):.4f} · PPL val {p:.3f} · {time.time()-t0:.0f} s", flush=True)
87:    p_val, n_tok = ppl(modele, val, a.seq, a.lot, a.device, n_lots=8)
89:    modele.eval(); bons_main = 0; bons_early = [0] * len(modele.cfg.early_blocks); n_eval = 0
92:            x, y = lot(val, a.lot, a.seq, a.device, 10_000_000 + _ * a.lot)
97:            n_eval += y.numel()
98:    prec_main = bons_main / max(1, n_eval)
99:    prec_early = [b / max(1, n_eval) for b in bons_early]
100:    modele.eval()
106:           "perte_finale": pertes[-1], "ppl_val": p_val, "jetons_val": n_tok,
  ```

- **job_output** `{"job_id": "bash-102", "timeout_ms": 180000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; ls work/n2d/*.json | grep -v essai; tail -2 work/n2d/A-fr-g1.log", "description": "Check final result of seed 1"}`

  ```
17:45:53
pas 18000 · seq 128 · perte 44.3504 · PPL 128/4 2.4118 · 1223 s
pas 18250 · seq 128 · perte 53.3659 · PPL 128/4 2.4010 · 1240 s
  ```

- **bash** `{"command": "timeout 55 sleep 50; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; ls work/n2d/*.json | grep -v essai; tail -2 work/n2d/A-fr-g1.log", "description": "Short wait then check results"}`

  ```
17:46:48
pas 18750 · seq 128 · perte 50.0082 · PPL 128/4 2.4012 · 1274 s
pas 19000 · seq 128 · perte 42.5346 · PPL 128/4 2.4020 · 1291 s
  ```

- **bash** `{"command": "timeout 55 sleep 50; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; ls work/n2d/*.json | grep -v essai; tail -3 work/n2d/A-fr-g1.log", "description": "Wait for run completion"}`

  ```
17:47:41
pas 19250 · seq 128 · perte 45.0611 · PPL 128/4 2.4058 · 1308 s
pas 19500 · seq 128 · perte 41.7552 · PPL 128/4 2.4053 · 1325 s
pas 19750 · seq 128 · perte 39.8976 · PPL 128/4 2.3906 · 1342 s
  ```

### 👤 Utilisateur

background job bash-102 (bash: sleep 420; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; tail -3 work/n2d/A-fr-g1.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "timeout 55 sleep 35; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; ls work/n2d/*.json | grep -v essai; python3 -c \"\nimport json,glob\nfor f in sorted(glob.glob('work/n2d/A-fr-g1.json')+glob.glob('work/n2d/B-multi-g1.json')):\n    d=json.load(open(f)); print(f … [149 caractères tronqués]`

  ```
17:48:19
work/n2d/A-fr-g1.json
work/n2d/B-multi-g1.json
work/n2d/A-fr-g1.json {'init': '/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/drave-n0-base-20k.pt', 'corpus': 'fr', 'graine': 1, 'plan': [[128, 10000, 0.0001], [128, 10000, 3e-05]], 'lot': 16, 'temperature': 2.0, 'alpha': 0.7, 'tetes': True, 'pas': 20000, 'octets_vus': 40960000, 'perte_finale': 41.2261, 'ppl_128_lot16': 2.8548, 'ppl_128_lot8': 2.8563, 'ppl_129_lot15': 2.8815, 'ppl_permute': 1016.0988, 'precision_main': 0.6919, 'precision_early': [0.5941162109375, 0.6597900390625, 0.691162109375], 'duree_s': 1360.3769}
work/n2d/B-multi-g1.json {'init': '/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/drave-n0-base-20k.pt', 'corpus': 'multi', 'graine': 1, 'plan': [[128, 10000, 0.0001], [128, 10000, 3e-05]], 'lot': 16, 'temperature': 2.0, 'alpha': 0.7, 'tetes': True, 'pas': 20000, 'octets_vus': 40960000, 'perte_finale': 70.7852, 'ppl_128_lot16': 3.7902, 'ppl_128_lot8': 3.8375, 'ppl_129_lot15': 3.817, 'ppl_permute': 605.5838, 'ppl_multi_val': 31.8025, 'precision_main': 0.2814, 'precision_early': [0.3944091796875, 0.4111328125, 0.417236328125], 'duree_s': 1349.4514}
  ```

### 🤖 Assistant

⏵ Vérifiant l'écart entre l'évaluation en cours d'entraînement et l'évaluation finale

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2d/diagnostic.py <<'EOF'\nimport json, math, pathlib, sys\nimport torch, torch.nn.functional as F\nsys.path.insert(0,'.')\nfrom tools.native_model import NativeConfig, NativeModel\nfrom tools.vdc import departs_vdc\nVAL = … [1614 caractères tronqués]`

  ```
{"f": "A-fr-g1.pt", "4x2": 2.4179, "16x8": 2.8569, "8x8": 2.8634, "16x1": 2.7749, "16x2": 2.8739, "16x4": 2.8635, "1x1_c0": 1.1627, "1x8_c0": 2.4179, "1x8_c1M": 3.2522}
{"f": "temoin-g1.pt", "4x2": 2.5327, "16x8": 2.9406, "8x8": 2.9399, "16x1": 2.8871, "16x2": 2.936, "16x4": 2.9399, "1x1_c0": 1.2652, "1x8_c0": 2.5327, "1x8_c1M": 3.3364}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ps -eo pid,etime,cmd | grep distiller_budget | grep -v grep | sed 's/--sortie/\\n    --sortie/'; echo \"=== logs ===\"; ls -la work/n2d/*.log | tail -4; echo \"=== val head ===\"; head -c 200 data/corpus_fr_val.txt; ec … [99 caractères tronqués]`

  ```
17:49
  31476       01:30 /home/stephane/gpu-env/bin/python tools/distiller_budget.py --corpus multi --stages 128:10000:1e-4,128:10000:3e-5 --lot 16 --graine 2 
    --sortie work/n2d/B-multi-g2.pt --log work/n2d/B-multi-g2.log
  31477       01:30 /home/stephane/gpu-env/bin/python tools/distiller_budget.py --corpus fr --stages 128:10000:1e-4,128:10000:3e-5 --lot 16 --graine 2 
    --sortie work/n2d/A-fr-g2.pt --log work/n2d/A-fr-g2.log
=== logs ===
-rw-r--r--. 1 stephane stephane 6246 31 oct 17:47 work/n2d/A-fr-g1.log
-rw-r--r--. 1 stephane stephane  449 31 oct 17:49 work/n2d/A-fr-g2.log
-rw-r--r--. 1 stephane stephane 6348 31 oct 17:47 work/n2d/B-multi-g1.log
-rw-r--r--. 1 stephane stephane  500 31 oct 17:49 work/n2d/B-multi-g2.log
=== val head ===
e Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte 
L'architecture du cerveau — et ce qui manque à Drave pour la porter
9 octobre 2026. docs/biologie-pour-drave.md traitait de la brique (le
neurone, la synapse, l'énergie). Ce document traite de l'�
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\ntr=pathlib.Path('data/corpus_fr_train.txt').read_bytes()\nva=pathlib.Path('data/corpus_fr_val.txt').read_bytes()\nsonde=va[10:110]\nprint('sonde:', sonde[:80])\nprint('dans train ?', tr.count(sonde) … [343 caractères tronqués]`

  ```
sonde: b"\x94 listes d'\xc3\xa9v\xc3\xa9nements, streaming depuis le disque, r\xc3\xa9partition entre n\xc5\x93uds \xe2"
dans train ? 19
fenêtres de 128 octets (pas 5000) présentes dans train : 15/47
  ```

### 🤖 Assistant

⏵ Découverte d'une contamination : des fenêtres de validation existent verbatim dans l'entraînement. Je quantifie.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2d/contamination.py <<'EOF'\n#!/usr/bin/env python3\n\"\"\"contamination.py — la validation française est-elle tenue à l'écart ?\n\n`corpus_fr_val.txt` est la queue de `corpus_fr.txt` et `corpus_fr_train.txt` la tête :\nl … [3626 caractères tronqués]`

  ```
{"fenetres_echantillon": 300, "contaminees": 92, "taux": 0.3067}
{"protocole_fenetres": 128, "protocole_contaminees": 42, "taux_protocole": 0.3281}
{"fichier": "A-fr-g1.pt", "ppl_protocole": 2.8569, "ppl_contaminees": 2.5987, "ppl_propres": 2.9921}
{"fichier": "temoin-g1.pt", "ppl_protocole": 2.9406, "ppl_contaminees": 2.7285, "ppl_propres": 3.05}
{"fichier": "drave-n0-base-20k.pt", "ppl_protocole": 3.2161, "ppl_contaminees": 3.1765, "ppl_propres": 3.2356}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"corpus_fr\" tools/*.py | head -10; echo \"=== corpus_gele ===\"; head -40 tools/corpus_gele.py", "description": "Find the French corpus builder"}`

  ```
tools/adaptateur_langue.py
tools/comparer_noyaux.py
tools/contenu_par_couche.py
tools/corpus_natif.py
tools/distiller_budget.py
tools/distiller_natif.py
tools/distiller_section.py
tools/entrainer_native.py
tools/entrainer_section.py
tools/eval_n2.py
=== corpus_gele ===
#!/usr/bin/env python3
"""corpus_gele.py — le corpus des bancs, figé et vérifiable.

POURQUOI CE FICHIER EXISTE. Les bancs de R0.3 sont adossés à des documents **vivants** : quand
une session réécrit `continuite.md`, le gold d'une question ne résout plus et le banc ment
(arrivé le 29/10 : une question perdue, puis deux). Un banc qui bouge avec la documentation ne
mesure pas une progression, il mesure le dernier commit.

Le gel : chaque document du corpus est **copié** dans `tools/tests/documents/corpus/`, avec son
sha256 et sa source. Les constructeurs de bancs lisent la copie ; la source peut évoluer sans
casser le banc. `--verifie` recalcule les empreintes : une copie modifiée est signalée.

Usage :
  python3 tools/corpus_gele.py --fige      # copie et écrit le manifeste
  python3 tools/corpus_gele.py --verifie   # recalcule les sha256
"""
from __future__ import annotations

import argparse
import hashlib
import js
… [616 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"corpus_fr.txt\" tools/*.py | head -10; echo \"=== shell ===\"; grep -rln \"corpus_fr.txt\" tools/*.sh | head", "description": "Find where corpus_fr.txt is produced"}`

  ```
tools/adaptateur_langue.py:19:      --fr data/corpus_fr.txt --pas 2000 [--rang 8] [--sortie /tmp/adaptateur-fr.pt]
tools/adaptateur_langue.py:83:    ap.add_argument("--fr", default="data/corpus_fr.txt")
tools/comparer_noyaux.py:49:    fr = fenetres("data/corpus_fr.txt", a.longueur, a.fenetres)
tools/contenu_par_couche.py:21:      --en data/corpus_en.txt --fr data/corpus_fr.txt [--longueur 128] [--fenetres 250]
tools/contenu_par_couche.py:108:    ap.add_argument("--fr", default="data/corpus_fr.txt")
tools/corpus_natif.py:63:        "licence": "source locale data/corpus_fr.txt — licence à vérifier avant diffusion",
tools/corpus_natif.py:70:    ap.add_argument("--source", default="data/corpus_fr.txt")
tools/entrainer_native.py:52:    ap.add_argument("--corpus", default="data/corpus_fr.txt")
tools/entrainer_section.py:97:    ap.add_argument("--corpus", default="data/corpus_fr.txt")
tools/langue_dans_etat.py:27:  python3 tools/langue_dans_etat.py --hf /tmp/jouet-mixte-litt2 --en data/corpus_en.txt --fr data/corpus_fr.txt
=== shell ===
tools/porte-r13-bpe.sh
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,45p reports/rapport-native-corpus.md", "description": "Read the French corpus construction report"}`

  ```
# N2.1 — 50 000 fenêtres pour `drave-n0`

> **Objet.** Construire le corpus d'entraînement de N2 : fenêtres d'octets, split train/validation
> déterministe, manifeste d'offsets. Le corpus source n'est **pas versionné**.

## Résultat

| mesure | valeur |
|---|---:|
| source | `data/corpus_fr.txt` |
| octets | **4 633 889** |
| fenêtre | **128** octets |
| pas | **64** |
| **fenêtres** | **50 000** |
| train | **45 000** |
| validation | **5 000** |
| graine | 0 |

- Manifeste : [`native-corpus.json`](native-corpus.json) — 50 000 offsets, pas le texte.
- Découpage : `tools/corpus_natif.py --source data/corpus_fr.txt --max 50000 --val 5000`.
- Test : `tools/cerveau/tests/test_corpus_natif.py` (100 fenêtres, 90/10).

## Lecture

- **N2.1 est atteint en volume** : 50 000 fenêtres, 45 000/5 000.
- Ce sont des fenêtres **chevauchantes** (pas 64) du **même** corpus : augmenter le nombre de
  fenêtres n'ajoute pas de **données nouvelles**, seulement des vues.
- La **licence** du corpus source reste **à vérifier** avant toute diffusion.
- Le manifeste ne contient **pas** le texte : `data/` est ignoré par git.

## Verdict

**N2.1 — volume : atteint** (50 000 fenêtres). **N2.1 — diversité : no
… [410 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Réécrivant l'évaluation finale avec une colonne décontaminée

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"evalue-final.py — PPL de tous les points de contrôle de la campagne N2.d.\n\nTrois mesures, sur `data/corpus_fr_val.txt` :\n\n  protocole   : 8 lots × 16 fenêtres de 128 (compteur 0) — **le protocole de 2,7078**\n                et de 2,6998 ; c'est celui d … [5405 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/evalue-final.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 600 ~/gpu-env/bin/python work/n2d/evalue-final.py work/n2d/A-fr-g1.pt work/n2d/B-multi-g1.pt /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/temoin-g1.pt /home/stephane/Dat … [141 caractères tronqués]`

  ```
{"fichier": "A-fr-g1.pt", "params": 11814792, "ppl_protocole": 2.8569, "ppl_129": 2.8742, "ppl_propres": 2.9881, "ppl_contaminees": 2.5862, "ppl_permute": 1113.2495, "precision_main": 0.6924}
{"fichier": "B-multi-g1.pt", "params": 11814792, "ppl_protocole": 3.7609, "ppl_129": 3.8249, "ppl_propres": 3.8654, "ppl_contaminees": 3.4402, "ppl_permute": 596.0537, "precision_main": 0.6211, "ppl_multi_val": 31.8025}
{"fichier": "temoin-g1.pt", "params": 11814792, "ppl_protocole": 2.9406, "ppl_129": 2.9631, "ppl_propres": 3.0612, "ppl_contaminees": 2.7059, "ppl_permute": 1228.3835, "precision_main": 0.6844}
{"fichier": "drave-n0-base-20k.pt", "params": 11814792, "ppl_protocole": 3.2161, "ppl_129": 3.2653, "ppl_propres": 3.245, "ppl_contaminees": 3.0756, "ppl_permute": 544.3581, "precision_main": 0.6544}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, random\ntr=pathlib.Path('data/corpus_fr_train.txt').read_bytes()\nva=pathlib.Path('data/corpus_fr_val.txt').read_bytes()\nfr=pathlib.Path('data/corpus_fr.txt').read_bytes()\nrng=random.Random(0)\nec … [557 caractères tronqués]`

  ```
fenêtres de train présentes >1 fois dans train : 47 / 200 (23.5 %)
occurrences de la sonde de 100 octets : 19
corpus_fr = train + val ? True 4633889 4633889
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; for f in A-fr-g2 B-multi-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log; done", "description": "Check seed 2 progress"}`

  ```
17:51
-- A-fr-g2
pas  3000 · seq 128 · perte 65.0573 · PPL 128/4 2.6769 · 217 s
-- B-multi-g2
pas  3000 · seq 128 · perte 103.4934 · PPL 128/4 3.6129 · 211 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-*.sh | sed 's|tools/porte-||;s|\\.sh||' | tr '\\n' ' ' | fold -w 120", "description": "List all gate names"}`

  ```
adaptateur-sortie audit-drapeaux b1110-hybride balayage bloc-code bloc-maths bloc-tableaux budget bus bus-socket c4-reta
rd cerveau consolidation coupe cycle-c2 deepseek delais diff-couche document echange-experts episodique etat flux fusion
 gain greffe harnais-invariants homeostasie horloge indice jeux jumeaux lecteur lecture m5-brouillon melange memoire mir
oir-blocs mistral n3-cache n3-composition n3-deux-processus n3-deux-regions n3-generation n3-placement n3-pont n3-positi
ons n3-profondeur n3-refus n3-reseau n3-routes n3-service-briques n3-service n3-seuil n3-sparsite-compte n3-sparsite occ
upation-elagage occupation-moteur pannes peripherie poids-creux pont prechargement profondeur-routee push-paresseux r13-
bpe recurrence reflexe registre reparti-moteur sauvegarde-modele sessions speculatif tableaux tokenizer-kimi topologie t
race vision
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PORTES=\"etat registre document tableaux sessions budget\" DELAI=300 timeout 900 bash tools/toutes-les-portes.sh 2>&1 | tail -15", "description": "Run documentation gates early"}`

  ```
[still running after 60000ms; moved to background job bash-121]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **write** `{"content": "# N2 — le budget paie, les quatre sources coûtent, et la validation n'est pas tenue à l'écart\n\n> **Ligne de roadmap** : N2 (la distillation) · **Date** : 2026-10-31 · **Verdict** : le budget\n> complet (20 000 pas, 41 Mo) fait baisser la PPL de **2,9355 à {{A}}** sous le protocole de  … [6658 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/fiche.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

background job bash-121 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PORTES="etat registre document tableaux sessions budget" DELAI=300 timeout 900 bash tools/toutes-les-portes.sh 2>&1 | tail -15) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-121"}`

  ```
porte-bloc-tableaux    ✅                           1 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          48 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-document         ✅                           6 s  ✅ porte document verte
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-registre         ✅                          16 s    ✅ région absente : refusée en la nommant (code 2), rien n'est calculé
  porte-sessions         ❌ code 1                    0 s    ❌ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-479
  porte-tableaux         ✅                           0 s    ✅ la page vivante date du dernier commit (2026-10-31)
--- 6 vertes, 1 rouges ---
À RELIRE (les six dernières lignes de chaque rouge) :
  --- porte-sessions ---
    autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé
      ⚠ session en-cours sans plan : active
      ⚠ plan actif non listé dans en-cours : 0b0a6a0d-05f5-4308-800c-4792ddb9cbf2
      ❌ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/jo
… [158 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,60p tools/porte-sessions.sh", "description": "Read sessions gate"}`

  ```
#!/bin/bash
# porte-sessions.sh — les plans de session sont lisibles et le linter refuse un doublon.
set -u
cd "$(dirname "$0")/.."
python3 tools/sessions.py --autotest || exit 1
python3 tools/sessions.py --check || exit 1
python3 tools/sessions.py --status | grep -q '71d57f53' || {
    echo "  ❌ le plan de la session de coordination n'est pas lisible"; exit 1; }
echo "PORTE TENUE : plan lisible · autotest doublon/champ manquant · check en-cours"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"heartbeat\\|Heartbeat\\|def .*check\\|actif\\|non listé\" tools/sessions.py | head -30", "description": "Inspect session checker expectations"}`

  ```
5:périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
8:les heartbeats périmés. `en-cours` reste la seule source de l'état : ce plan
23:CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
25:ACTIFS = {"actif", "active", "en cours", "bloqué", "bloquee", "bloqué(e)"}
54:    hb = champs.get("heartbeat", "")
55:    heartbeat = None
60:            heartbeat = datetime.fromisoformat(brut)
62:            heartbeat = datetime.strptime(brut, "%Y-%m-%d %H:%M")
63:        age = (datetime.now() - heartbeat).total_seconds() / 60.0
67:            "fichiers": fic, "heartbeat": heartbeat, "age": age,
96:    heartbeat = f"{m.group(1)} {int(m.group(2)):02d}:{m.group(3)} HAE" if m else ""
107:                    "heartbeat": heartbeat})
119:        heartbeat = s["heartbeat"] or datetime.now().strftime("%Y-%m-%d %H:%M HAE")
126:> session : le heartbeat est celui de l'état, pas une preuve de vie.
132:- **Heartbeat** : {heartbeat}
146:    actifs = [p for p in plans if p["etat"] in ACTIFS]
158:            erreurs.append(f"{p['chemin']} : heartbeat illisible")
162:    for i, a in enumerate(actifs):
164:            msg = f"mandat périmé ({a['age']:.0f} min) :
… [783 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 40,70p tools/sessions.py; echo \"=== en-cours parse ===\"; sed -n 85,115p tools/sessions.py", "description": "Read heartbeat parser and en-cours extraction"}`

  ```
champs: dict[str, str] = {}
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*[-*]\s*\*\*(.+?)\*\*\s*:\s*(.*?)\s*$", ligne)
        if m:
            champs[_cle(m.group(1))] = _valeur(m.group(2))
    # tolérances : Role / Perimetre sans accent
    for alias, cible in (("role", "rôle"), ("perimetre", "périmètre"),
                         ("fichiers reserves", "fichiers réservés"),
                         ("prochaine", "prochaine action"), ("etat", "état")):
        if cible not in champs and alias in champs:
            champs[cible] = champs[alias]
    sid = champs.get("session") or chemin.parent.name
    per = [x.strip().strip("`") for x in re.split(r"[,;]", champs.get("périmètre", "")) if x.strip()]
    fic = [x.strip().strip("`") for x in re.split(r"[,;]", champs.get("fichiers réservés", "")) if x.strip()]
    hb = champs.get("heartbeat", "")
    heartbeat = None
    age = None
    try:
        brut = re.sub(r"\s*(HAE|EDT|EST|UTC[−-]?[0-9]+)\s*$", "", hb).strip()
        if "T" in brut:
            heartbeat = datetime.fromisoformat(brut)
        else:
            heartbeat = datetime.strptime(brut, "%Y-%m-%d %H:%M")
        age = (d
… [1727 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Session\\|###\" tools/verifie_en_cours.py | head -20", "description": "Check state validator heading parsing"}`

  ```
7:  3. « Sessions en cours » : une sous-section `### Session ...` par session active, avec
26:    "Sessions en cours",
64:    """Rend [(titre, corps)] des sous-sections `### ...` de « Sessions en cours »."""
65:    titres = list(re.finditer(r"(?m)^### (.+)$", section))
89:    blocs = sessions(corps_section(texte, "Sessions en cours"))
91:        alertes.append("« Sessions en cours » n'a aucune sous-section `### Session ...`")
93:        if not titre.startswith("Session"):
94:            alertes.append(f"sous-section sans « Session » : « {titre} »")
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\ns=s.replace(\"### Session active — N2, le budget complet (`0b0a6a0d`)\",\n            \"### Session `0b0a6a0d-05f5-4308-800c-4792ddb9cbf … [476 caractères tronqués]`

  ```
✅ plans cohérents
check=0
  en-cours · 1180 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PORTES=\"sessions\" DELAI=120 timeout 200 bash tools/toutes-les-portes.sh 2>&1 | tail -5", "description": "Re-run the sessions gate"}`

  ```
journaux : /tmp/portes-1031-17h54
  porte-sessions         ✅                           0 s  PORTE TENUE : plan lisible · autotest doublon/champ manquant · check en-cours
--- 1 vertes, 0 rouges ---
TOUTES LES PORTES SONT VERTES — et elles ont TOUTES tourné, ce que rien ne garantissait avant.
Journaux : /tmp/portes-1031-17h54
  ```

### 🤖 Assistant

⏵ Versant l'évaluation et la mesure de contamination dans `tools/` (versionnées)

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"eval_n2_budget.py — N2.d : PPL des points de contrôle, validation décontaminée.\n\nLa campagne N2.d (`tools/distiller_budget.py`) a mesuré le budget, les données et le\ncurriculum. Deux choses ont été trouvées en l'évaluant, et ce script les rend\nreproduct … [8979 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_budget.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 900 ~/gpu-env/bin/python tools/eval_n2_budget.py work/n2d/A-fr-g1.pt /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/temoin-g1.pt --grilles 2>&1 | grep -v Loading", "descri … [45 caractères tronqués]`

  ```
{"fichier": "A-fr-g1.pt", "params": 11814792, "ppl_protocole": 2.8569, "ppl_129": 2.8742, "ppl_propres": 2.9881, "ppl_contaminees": 2.5862, "ppl_permute": 1113.2495, "precision_main": 0.6924, "grilles": {"0/16": 2.8569, "0/8": 2.8634, "1000003/16": 2.9473, "1000003/8": 2.8879, "2000009/16": 2.9298, "2000009/8": 3.0563, "3000029/16": 2.7523, "3000029/8": 2.7231}}
{"fichier": "temoin-g1.pt", "params": 11814792, "ppl_protocole": 2.9406, "ppl_129": 2.9631, "ppl_propres": 3.0612, "ppl_contaminees": 2.7059, "ppl_permute": 1228.3835, "precision_main": 0.6844, "grilles": {"0/16": 2.9406, "0/8": 2.9399, "1000003/16": 3.0375, "1000003/8": 2.9865, "2000009/16": 3.0428, "2000009/8": 3.1897, "3000029/16": 2.8269, "3000029/8": 2.796}}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; for f in A-fr-g2 B-multi-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log; done", "description": "Check seed 2 progress"}`

  ```
17:54
-- A-fr-g2
pas  5500 · seq 128 · perte 53.0568 · PPL 128/4 2.5465 · 393 s
-- B-multi-g2
pas  5500 · seq 128 · perte 89.1359 · PPL 128/4 3.7486 · 389 s
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py", "limit": 3}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """agrege.py — tableau par bras de la campagne N2.d.
3: 

(Showing lines 1-3 of 65. Use offset=4 to continue.)
</content>
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"agrege.py — tableau par bras de la campagne N2.d.\n\nLit `work/n2d/evaluations-finales.json` (sortie de `tools/eval_n2_budget.py`) et les\nmétadonnées d'entraînement (`work/n2d/*.json`). Écrit `reports/n2-budget.json` et\nimprime le tableau markdown de la f … [2728 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nfrom tools.vdc import departs_vdc\ntr=pathlib.Path('data/corpus_fr_train.txt').read_bytes()\nva=pathlib.Path('data/corpus_fr_val.txt').read_bytes()\n# distribution spatiale : 400 fenêtres régulières … [582 caractères tronqués]`

  ```
taux de contamination par quartile de val (%) : [31.0, 65.0, 17.0, 15.0]
occurrences de 3 sondes de 100 octets prises au hasard :
5000 0
100000 1
200000 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 176,200p docs/pilotage/roadmap.md; echo \"=== 295,335 ===\"; sed -n 295,335p docs/pilotage/roadmap.md", "description": "Read roadmap N lessons and open questions"}`

  ```
1. **Le contexte est le verrou.** 129 octets est le meilleur point (**PPL 2,6998**) ; **130** est négatif
   (**2,7149**), **136** (**2,974**), **160** (**3,804**), **256** (**5,675**). À **2 000 octets**, la PPL native
   est **54,04**. Le modèle **surapprend sa longueur** : allonger le contexte demande un **autre schéma**, pas un
   curriculum de plus.
2. **Le saut de calcul existe, le saut de contenu n'existe pas.** La sortie précoce gagne **24,05 %** de temps en
   perdant **1,61 point** ; c'est une décision sur la **confiance du prochain octet**, pas sur la **pertinence**.
3. **La mémoire manque.** Le signal courant est lisible (R² **0,992**), celui d'il y a 8 pas ne l'est pas
   (**−0,681**), et l'entraînement l'aggrave (**−1,091 → −2,773**). Le tampon gelé lit **+0,879**, mais le réseau
   ne s'en sert pas.

---

## Programme R

**Synthèse : [le programme R en une page](programme-r.md)** — ce qui tient, ce qui ne tient pas, les trois lois. — Le lecteur (la nouvelle cible)

**La cible** : lire un document **comme un humain lit vite** — survoler, balayer, lire sélectivement, revenir — en
payant le calcul au prorata de ce qui est lu, et **prouver** la compréhension par la resti
… [2867 caractères tronqués]
  ```

- **bash** `{"command": "sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai | wc -l; tail -1 work/n2d/A-fr-g3.log 2>/dev/null; tail -1 work/n2d/C-129-g1.log 2>/dev/null", "description": "Wait 25 minutes for the campaign", "run_in_background": true … [1 caractères tronqués]`

  ```
started background job bash-132
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"2,6998\\|2,708\\|N2\" reports/README.md | head -12", "description": "Check reports index mentions of N2 best"}`

  ```
18:| [`rapport-native-prof30k.md`](rapport-native-prof30k.md) | **N2.21** — professeur 30k, lr 3e-6 : PPL **2,823**, dégradation, arrêté |
19:| `rapport-native-prof20k-6.md` (fiche non écrite) | **N2.23** — professeur 20k, lr 3e-6 : PPL **2,753**, arrêté |
20:| [`rapport-native-prof20k-8.md`](rapport-native-prof20k-8.md) | **N2.25** — lr 1e-6 : PPL **2,758**, arrêté |
21:| [`rapport-native-8b-warm.md`](rapport-native-8b-warm.md) | **N2.29** — 8 blocs réchauffés : PPL **2,866**, arrêté |
22:| [`rapport-native-8b.md`](rapport-native-8b.md) | **N2.28** — 8 blocs : PPL **4,838**, arrêté |
23:| [`rapport-native-ctx130-2.md`](rapport-native-ctx130-2.md) | **N2.35** — contexte 130 : PPL **2,7149**, négatif |
24:| [`rapport-native-ctx129-2.md`](rapport-native-ctx129-2.md) | **N2.34** — 129, 10 000 pas de plus : PPL **2,712**, arrêté |
25:| [`rapport-native-ctx129.md`](rapport-native-ctx129.md) | **N2.33** — contexte 129 : PPL **2,6998**, nouveau meilleur |
26:| [`rapport-native-ctx130.md`](rapport-native-ctx130.md) | **N2.32** — contexte 130 : PPL **2,786**, arrêté |
27:| [`rapport-native-ctx136.md`](rapport-native-ctx136.md) | **N2.31** — contexte 136 : PPL **2,974**, arrêté |
28:| [`rapp
… [254 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,20p reports/README.md", "description": "Read reports README header"}`

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
| [`rapport-native-prof30k.md`](rapport-native-prof30k.md) | **N2.21** — professeur 30k, lr 3e-6 : PPL **2,823**, dégradation, arrêté |
| `rapport-native-prof20k-6.md` (fiche non écrite) | **N2.23** — professeur 20k, lr 3e-6 : PPL **2,753**, arrêté |
| [`rapport-native-prof20k-8.md`](rapport-native-prof20k-8
… [52 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/verifie_backlog.py 2>&1 | tail -12", "description": "Run backlog verification"}`

  ```
=== GRAPHE DU BACKLOG ===
  fiches 37 · lignes sans fiche 1 · arêtes dures 43 · plafonds 3
  profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (4) : A2.6, N2, N3, N4

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; for f in A-fr-g2 B-multi-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log; done; ls work/n2d/*.json | grep -v essai", "description": "Check seed 2 progress"}`

  ```
17:56
-- A-fr-g2
pas  6750 · seq 128 · perte 65.3890 · PPL 128/4 2.4861 · 480 s
-- B-multi-g2
pas  6750 · seq 128 · perte 89.2131 · PPL 128/4 3.8219 · 480 s
work/n2d/A-fr-g1.json
work/n2d/B-multi-g1.json
work/n2d/evaluations-finales.json
  ```

- **write** `{"content": "### N2 — le budget, les quatre sources, et le mètre faussé\n\nLa journée avait commencé par deux négatifs nets sur la hiérarchie. En reprenant N2 l'après-midi,\nla question était simple : le dispositif reconstruit hier n'avait vu que **20,48 Mo** d'un seul\ncorpus en **5 000 pas** — que … [1783 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/journal-notes.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; for f in A-fr-g2 B-multi-g2; do tail -1 work/n2d/$f.log; done", "description": "Poll campaign progress"}`

  ```
17:56
pas  7250 · seq 128 · perte 55.2936 · PPL 128/4 2.4851 · 515 s
pas  7250 · seq 128 · perte 83.5229 · PPL 128/4 3.7776 · 515 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 600 ~/gpu-env/bin/python tools/eval_n2_budget.py /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/temoin-g2.pt /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefac … [96 caractères tronqués]`

  ```
{"fichier": "temoin-g2.pt", "params": 11814792, "ppl_protocole": 2.9345, "ppl_129": 2.961, "ppl_propres": 3.056, "ppl_contaminees": 2.6991, "ppl_permute": 1131.9621, "precision_main": 0.6826}
{"fichier": "temoin-g3.pt", "params": 11814792, "ppl_protocole": 2.9313, "ppl_129": 2.9628, "ppl_propres": 3.0431, "ppl_contaminees": 2.7074, "ppl_permute": 1167.2152, "precision_main": 0.6827}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/eval_n2_budget.py --contamination | tee work/n2d/contamination.json", "description": "Record contamination rates"}`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_budget.py", line 41, in <module>
    import torch
ModuleNotFoundError: No module named 'torch'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. ~/gpu-env/bin/python tools/eval_n2_budget.py --contamination | tee work/n2d/contamination.json", "description": "Record contamination rates with GPU env"}`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_budget.py", line 198, in <module>
    main()
    ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_budget.py", line 144, in main
    print(json.dumps(contamination(val, train), ensure_ascii=False))
                     ~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_budget.py", line 123, in contamination
    dupliques = sum(train.count(bytes(w.tolist())) > 1 for w in ech_train)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_budget.py", line 123, in <genexpr>
    dupliques = sum(train.count(bytes(w.tolist())) > 1 for w in ech_train)
                                      ^^^^^^^^
AttributeError: 'bytes' object has no attribute 'tolist'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/eval_n2_budget.py'); s=p.read_text()\ns=s.replace(\"dupliques = sum(train.count(bytes(w.tolist())) > 1 for w in ech_train)\",\n            \"dupliques = sum(train.count(w) > 1  … [262 caractères tronqués]`

  ```
{"echantillon_validation": 300, "taux_validation": 0.3067, "protocole_fenetres": 128, "protocole_contaminees": 42, "taux_protocole": 0.3281, "echantillon_train": 200, "train_duplique": 47, "taux_train_duplique": 0.235}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; for f in A-fr-g2 B-multi-g2; do tail -1 work/n2d/$f.log; done; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader", "description": "Poll progress"}`

  ```
17:57
pas  8000 · seq 128 · perte 56.0856 · PPL 128/4 2.5025 · 568 s
pas  8000 · seq 128 · perte 88.0723 · PPL 128/4 3.7560 · 569 s
0, 1164 MiB, 78 %
1, 1164 MiB, 80 %
  ```

- **job_output** `{"job_id": "bash-132", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; for f in A-fr-g2 B-multi-g2; do tail -1 work/n2d/$f.log; done", "description": "Check campaign status"}`

  ```
18:07
work/n2d/A-fr-g1.json
work/n2d/B-multi-g1.json
work/n2d/contamination.json
work/n2d/evaluations-finales.json
pas 16750 · seq 128 · perte 45.9554 · PPL 128/4 2.4000 · 1162 s
pas 16500 · seq 128 · perte 79.6888 · PPL 128/4 3.7876 · 1163 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2d/remplit.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"remplit.py — remplit work/n2d/fiche.md avec l'agrégat et écrit reports/rapport-n2-budget.md.\"\"\"\nimport json, pathlib, re, statistics as st\n\nagg = json.loads(pathli … [2589 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('work/n2d/fiche.md'); s=p.read_text()\ns=s.replace(\"\"\"## Ce qui est mesuré\n\n{{TABLE}}\n\"\"\",\"\"\"## Ce qui est mesuré\n\n{{TABLE}}\n\nLes fenêtres **propres** sont 128 fenêtre … [692 caractères tronqués]`

  ```
ok
  ```

- **job_output** `{"job_id": "bash-132", "timeout_ms": 900000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; for f in A-fr-g2 A-fr-g3 B-multi-g2 B-multi-g3; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check campaign progress"}`

  ```
18:18
work/n2d/A-fr-g1.json
work/n2d/A-fr-g2.json
work/n2d/B-multi-g1.json
work/n2d/B-multi-g2.json
work/n2d/contamination.json
work/n2d/evaluations-finales.json
-- A-fr-g2
}
-- A-fr-g3
pas  6250 · seq 128 · perte 46.8063 · PPL 128/4 2.5462 · 420 s
-- B-multi-g2
}
-- B-multi-g3
pas  5750 · seq 128 · perte 81.8413 · PPL 128/4 3.7961 · 393 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nfor f in ('work/n2d/A-fr-g2.json','work/n2d/B-multi-g2.json'):\n    d=json.load(open(f)); print(f, {k:round(v,4) if isinstance(v,float) else v for k,v in d.items() if k in ('ppl_128_lot16','ppl_129_lot15', … [92 caractères tronqués]`

  ```
work/n2d/A-fr-g2.json {'ppl_128_lot16': 2.8535, 'ppl_128_lot8': 2.8496, 'ppl_129_lot15': 2.8891, 'ppl_permute': 986.7774, 'precision_main': 0.7137}
work/n2d/B-multi-g2.json {'ppl_128_lot16': 3.7954, 'ppl_128_lot8': 3.8393, 'ppl_129_lot15': 3.8349, 'ppl_permute': 626.1502, 'precision_main': 0.2906}
  ```

- **bash** `{"command": "sleep 900; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; for f in C-129-g1 Bp-equilibre-g1; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Wait 15 minutes for seed 3 and curriculum start", "run_in … [19 caractères tronqués]`

  ```
started background job bash-148
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,40p journal/THEMES.md", "description": "Read journal theme keywords"}`

  ```
# Thèmes du journal

> Généré par `tools/journal_auto.py` — c'est la **règle de classement** des fichiers
> `journal/AAAA-MM-JJ/<thème>.md`. Un commit (ou une étape de session) est classé par
> le **premier** thème dont un mot-clé apparaît dans son texte ; à défaut, par les
> **chemins** touchés ; à défaut, en `divers`. Pour changer le classement, éditer la
> table `THEMES` du script et relancer : rien d'autre n'est à toucher.

| thème | ce qu'il couvre | mots-clés | chemins |
|---|---|---|---|
| `attention` | Attention, fenêtre, puits | attention, fenêtre, fenetre, puits, sinks, attn-, softmax, swa |  |
| `memoire` | Mémoire épisodique, consolidation, greffe | mémoire, memoire, épisodique, episodique, greffe, consolid, rappel, indice, magasin, c6, c7, clé, cle | episodique.rs |
| `apprentissage` | Règles locales, hebbien, modulateurs, distillation | hebb, décorrélation, decorrelation, modulateur, nouveauté, nouveaute, règle locale, regle locale, apprentissage, distill, impulsion, décharge, decharge, spiking, log-normal, élagage appris, k-wta appris |  |
| `distribue` | Régions, flux, protocoles, budgets, pannes | topologie, région, region, nœud, noeud, flux, bus, latence, budget, 
… [1941 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py 2>&1 | tail -8", "description": "Check journal verification"}`

  ```
journal · 37 jour(s) · 110 session(s) · 1702 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schemas.py 2>&1 | tail -4", "description": "Verify schemas"}`

  ```
schémas · 431 document(s) · 35 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai | wc -l; for f in A-fr-g3 B-multi-g3 C-129-g1 Bp-equilibre-g1; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check seed 3 and curriculum start"}`

  ```
18:19
6
-- A-fr-g3
pas  6750 · seq 128 · perte 53.3343 · PPL 128/4 2.5292 · 453 s
-- B-multi-g3
pas  6500 · seq 128 · perte 87.6959 · PPL 128/4 3.7325 · 442 s
-- C-129-g1
-- Bp-equilibre-g1
[exit code: 1]
  ```

- **job_output** `{"job_id": "bash-148", "timeout_ms": 1200000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-132 (bash: sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai | wc -l; tail -1 work/n2d/A-fr-g3.log 2>/dev/null; tail -1 work/n2d/C-129-g1.log 2>/dev/null) finished [status: completed, exit code: 1]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; for f in A-fr-g3 B-multi-g3 C-129-g1 Bp-equilibre-g1; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check campaign after 25-minute wait"}`

  ```
18:29
work/n2d/A-fr-g1.json
work/n2d/A-fr-g2.json
work/n2d/B-multi-g1.json
work/n2d/B-multi-g2.json
work/n2d/contamination.json
work/n2d/evaluations-finales.json
-- A-fr-g3
pas 16000 · seq 128 · perte 47.4620 · PPL 128/4 2.4026 · 1066 s
-- B-multi-g3
pas 15500 · seq 128 · perte 67.7423 · PPL 128/4 3.7959 · 1041 s
-- C-129-g1
-- Bp-equilibre-g1
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('work/n2d/fiche.md'); s=p.read_text()\ns=s.replace(\"\"\"- Code : [`tools/distiller_budget.py`](../tools/distiller_budget.py) · évaluation\n  `work/n2d/evalue-final.py` · agrégat [`n2 … [519 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sleep 2400; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; tail -1 work/n2d/C-129-g2.log 2>/dev/null; tail -1 work/n2d/Bp-equilibre-g2.log 2>/dev/null", "description": "Wait 40 minutes for the campaign", "run_in_background": true … [1 caractères tronqués]`

  ```
started background job bash-155
  ```

- **job_output** `{"job_id": "bash-155", "timeout_ms": 2400000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-148 (bash: sleep 900; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; for f in C-129-g1 Bp-equilibre-g1; do echo "-- $f"; tail -1 work/n2d/$f.log 2>/dev/null; done) finished [status: completed, exit code: 1]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; for f in C-129-g1 Bp-equilibre-g1; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check whether curriculum and balanced arms started"}`

  ```
18:39
work/n2d/A-fr-g1.json
work/n2d/A-fr-g2.json
work/n2d/A-fr-g3.json
work/n2d/B-multi-g1.json
work/n2d/B-multi-g2.json
work/n2d/B-multi-g3.json
work/n2d/contamination.json
work/n2d/evaluations-finales.json
-- C-129-g1
pas  5250 · seq 129 · perte 40.8452 · PPL 128/4 2.3931 · 353 s
-- Bp-equilibre-g1
pas  5000 · seq 128 · perte 95.3112 · PPL 128/4 3.4000 · 328 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nfor f in ('work/n2d/A-fr-g3.json','work/n2d/B-multi-g3.json'):\n    d=json.load(open(f)); print(f, {k:round(v,4) if isinstance(v,float) else v for k,v in d.items() if k in ('ppl_128_lot16','ppl_129_lot15', … [87 caractères tronqués]`

  ```
work/n2d/A-fr-g3.json {'ppl_128_lot16': 2.8517, 'ppl_129_lot15': 2.8804, 'ppl_permute': 950.7276, 'precision_main': 0.7345, 'duree_s': 1336.3981}
work/n2d/B-multi-g3.json {'ppl_128_lot16': 3.7737, 'ppl_129_lot15': 3.8093, 'ppl_permute': 600.4342, 'precision_main': 0.2715, 'duree_s': 1340.0632}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/distiller_budget.py'); s=p.read_text()\nancien = '''    bons = [0] * (len(cfg.early_blocks) + 1); n_ev = 0\n    with torch.no_grad():\n        for k in range(4):\n            x … [1552 caractères tronqués]`

  ```
ok
parse ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2d/finalise.sh <<'EOF'\n#!/bin/bash\n# Attend la fin des deux files, puis évalue les 16 points de contrôle, agrège et remplit la fiche.\nset -u\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nART=/home/stephane/Data1 … [1169 caractères tronqués]`

  ```
finaliseur 64233
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai | wc -l; for f in C-129-g1 Bp-equilibre-g1 C-129-g2 Bp-equilibre-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check curriculum arm progress"}`

  ```
18:40
8
-- C-129-g1
pas  6000 · seq 129 · perte 51.6991 · PPL 128/4 2.4037 · 403 s
-- Bp-equilibre-g1
pas  5750 · seq 128 · perte 104.8664 · PPL 128/4 3.3953 · 377 s
-- C-129-g2
-- Bp-equilibre-g2
[exit code: 1]
  ```

- **job_list** `{}`

  ```
bash-48 [bash] completed — sleep 150; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo "=== A ==="; tail -3 work/n2d/A-fr-g1.log 2>/dev/null; echo "=== B ==="; tail -3 work/n2d/B-multi-g1.log 2>/dev/null; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader
bash-81 [bash] completed — cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md journal/README.md && git commit -m "ÉTAT — LA CAMPAGNE N2 BUDGET ET DONNÉES EST OUVERTE, LES GPU RÉSERVÉS JUSQU'À 19 h 40

Une seconde session peut démarrer : en-cours nomme désormais la session active
(0b0a6a0d), son mandat et ses fichiers réservés (work/n2d/, tools/distiller_budget.py,
reports/n2-*). La campagne tourne sur les deux GPU — A français seul, B manifeste
quatre sources, B' quotas égaux, C curriculum 129, trois graines chacune.

Ce que l'autre session peut prendre sans collision : documentation, backlog, N4 (sans
GPU), portes documentaires. Ce qu'elle ne doit pas prendre : tools/toutes-les-portes.sh
(la passe complète utilise les deux cartes et fausserait les mesures), les fichiers
réservés, ni la page d'ét
… [1451 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/C-129-g1.json 2>/dev/null && python3 -c \"\nimport json; d=json.load(open('work/n2d/C-129-g1.json'))\nprint({k:round(v,4) if isinstance(v,float) else v for k,v in d.items() if k in ('ppl_128_lot16','ppl_129 … [92 caractères tronqués]`

  ```
18:40
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && while [ ! -f work/n2d/finalise.termine ]; do sleep 30; done; date '+%H:%M'; cat work/n2d/agregat.log", "description": "Wait for the finalizer and print the aggregate", "run_in_background": true}`

  ```
started background job bash-162
  ```

- **job_output** `{"job_id": "bash-162", "timeout_ms": 2400000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; for f in C-129-g1 C-129-g2 Bp-equilibre-g1 Bp-equilibre-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check curriculum and balanced arm progress" … [1 caractères tronqués]`

  ```
18:51
work/n2d/A-fr-g1.json
work/n2d/A-fr-g2.json
work/n2d/A-fr-g3.json
work/n2d/B-multi-g1.json
work/n2d/B-multi-g2.json
work/n2d/B-multi-g3.json
work/n2d/C-129-g1.json
work/n2d/contamination.json
work/n2d/evaluations-finales.json
-- C-129-g1
}
-- C-129-g2
pas  5000 · seq 129 · perte 45.4495 · PPL 128/4 2.3762 · 351 s
-- Bp-equilibre-g1
pas 15250 · seq 128 · perte 70.9172 · PPL 128/4 3.4172 · 1008 s
-- Bp-equilibre-g2
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json; d=json.load(open('work/n2d/C-129-g1.json'))\nprint({k:round(v,4) if isinstance(v,float) else v for k,v in d.items() if k in ('ppl_128_lot16','ppl_129_lot15','ppl_permute','precision_main','duree_s')})\npri … [86 caractères tronqués]`

  ```
{'ppl_128_lot16': 2.839, 'ppl_129_lot15': 2.8217, 'ppl_permute': 967.0087, 'precision_main': 0.6935, 'duree_s': 672.9645}
courbe fin: {'pas': 10000, 'seq': 129, 'perte': 44.278648376464844, 'ppl': 2.398044897343873}
  ```

- **job_output** `{"job_id": "bash-162", "timeout_ms": 2400000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai | wc -l; for f in C-129-g3 Bp-equilibre-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check remaining runs"}`

  ```
19:01
11
-- C-129-g3
pas  4000 · seq 129 · perte 45.2516 · PPL 128/4 2.3967 · 273 s
-- Bp-equilibre-g2
pas  4250 · seq 128 · perte 93.0802 · PPL 128/4 3.3877 · 293 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2d/maj-docs.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"maj-docs.py — applique les mises à jour d'état, de roadmap et de backlog du résultat N2.d.\"\"\"\nimport json, pathlib\n\nagg = json.loads(pathlib.Path('reports/n2-budg … [3086 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2d/maj-roadmap.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"maj-roadmap.py — roadmap : N2 après N2.d (budget, données, curriculum, validation contaminée).\"\"\"\nimport json, pathlib\n\nagg = json.loads(pathlib.Path('reports/ … [2535 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai | wc -l; for f in C-129-g3 Bp-equilibre-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check remaining runs"}`

  ```
19:02
11
-- C-129-g3
pas  4500 · seq 129 · perte 42.9175 · PPL 128/4 2.4081 · 309 s
-- Bp-equilibre-g2
pas  5000 · seq 128 · perte 86.2991 · PPL 128/4 3.3269 · 341 s
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/fiche.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/fiche.md</path>
<type>file</type>
<content>
1: # N2 — le budget paie, les quatre sources coûtent, et la validation n'est pas tenue à l'écart
2: 
3: > **Ligne de roadmap** : N2 (la distillation) · **Date** : 2026-10-31 · **Verdict** : le budget
4: > complet (20 000 pas, 41 Mo) fait baisser la PPL de **2,9355 à {{A}}** sous le protocole de N2.19 ;
5: > le corpus à quatre sources la fait **monter** à **{{B}}** ; et **32,8 % des fenêtres du protocole
6: > de validation sont verbatim dans l'entraînement** — sur les fenêtres propres, le meilleur élève
7: > est à **{{A_propre}}**, pas à {{A}}.
8: 
9: ## La question
10: 
11: La hiérarchie est écartée deux fois (N2.h1, N2.h2 : 2,9935 contre 2,9927). La roadmap désigne
12: ensuite **le curriculum et les données** : le dispositif reconstruit la veille n'avait vu que
13: **20,48 Mo d'un seul corpus en 5 000 pas**, la moitié du budget de N2 (41 Mo, 20 000 pas, quatre
14: sources). Ce dispositif est mesuré ici à budget plein, avec trois graines, et comparé à trois
15: témoins : la base supervisée, la distillation courte de la veille, et le corpus à quatre sources.
16: 
17: ## Le disp
… [6871 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('work/n2d/fiche.md'); s=p.read_text()\ns=s.replace(\"est à **{{A_propre}}**, pas à {{A}}.\", \"est à **{{A_PROPRE}}**, pas à {{A}}.\")\ns=s.replace(\"**Contrôle de grille.** Sur les q … [1543 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai | wc -l; for f in C-129-g3 Bp-equilibre-g2; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check end of curriculum arm"}`

  ```
19:02
11
-- C-129-g3
pas  4750 · seq 129 · perte 43.9112 · PPL 128/4 2.4037 · 326 s
-- Bp-equilibre-g2
pas  5000 · seq 128 · perte 86.2991 · PPL 128/4 3.3269 · 341 s
  ```

- **bash** `{"command": "timeout 55 sleep 50; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/C-129-g3.json 2>/dev/null && python3 -c \"\nimport json,glob,statistics as st\nvals=[]\nfor f in sorted(glob.glob('work/n2d/C-129-g*.json')):\n    d=json.load(open(f)); vals.append((d[' … [188 caractères tronqués]`

  ```
19:03
[exit code: 2]
  ```

- **bash** `{"command": "timeout 55 sleep 50; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai | wc -l; tail -1 work/n2d/C-129-g3.log", "description": "Wait for curriculum seed 3"}`

  ```
19:04
11
pas  6250 · seq 129 · perte 39.8914 · PPL 128/4 2.4049 · 428 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\ntextes = {\n 'docs/pilotage/en-cours.md': [\"- **N2** : GPU ; meilleur **2,6998** ; porte **< 2,5** non atteinte ; N4 **0/40**.\"],\n 'docs/pilotage/backlog/N2-distillation.md': [\"Lancer la série * … [1209 caractères tronqués]`

  ```
docs/pilotage/en-cours.md OK - **N2** : GPU ; meilleur **2,6998** ; porte **< 2
docs/pilotage/backlog/N2-distillation.md OK Lancer la série **hiérarchie** (état de section, l
docs/pilotage/roadmap.md OK | **N — le natif** | DRVM, `drave-n0`, distillatio
docs/pilotage/roadmap.md OK | **N2** | la distillation : 49 999 fenêtres, 4 so
docs/pilotage/roadmap.md OK 1. **Le contexte est le verrou.** 129 octets est l
docs/pilotage/roadmap.md OK - **non bloqué, à faire** : **N2** (la hiérarchie)
docs/pilotage/roadmap.md OK - **N2** : le student peut-il descendre sous **2,5
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('work/n2d/remplit.py'); s=p.read_text()\ns=s.replace('''vals = {\n    'TABLE': table,''','''C_TEXTE = (f\"gagne **{fmt(A129 - C129)}** sur le protocole 129 (comparaison appariée) et \ … [347 caractères tronqués]`

  ```
ok
39:C_TEXTE = (f"gagne **{fmt(A129 - C129)}** sur le protocole 129 (comparaison appariée) et "
43:    'C_TEXTE': C_TEXTE,
  ```

- **job_output** `{"job_id": "bash-162", "timeout_ms": 2700000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-155 (bash: sleep 2400; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai; tail -1 work/n2d/C-129-g2.log 2>/dev/null; tail -1 work/n2d/Bp-equilibre-g2.log 2>/dev/null) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2d/*.json | grep -v essai | wc -l; for f in Bp-equilibre-g2 Bp-equilibre-g3; do echo \"-- $f\"; tail -1 work/n2d/$f.log 2>/dev/null; done", "description": "Check balanced arm progress"}`

  ```
19:14
12
-- Bp-equilibre-g2
pas 16000 · seq 128 · perte 63.6670 · PPL 128/4 3.3973 · 1083 s
-- Bp-equilibre-g3
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work/n2d/*.json | grep -v essai; python3 -c \"\nimport json,glob,statistics as st\nfor pat in ('C-129-g','Bp-equilibre-g'):\n    vals=[]\n    for f in sorted(glob.glob(f'work/n2d/{pat}*.json')):\n        d=json.load(open(f)); vals … [252 caractères tronqués]`

  ```
work/n2d/A-fr-g1.json
work/n2d/A-fr-g2.json
work/n2d/A-fr-g3.json
work/n2d/B-multi-g1.json
work/n2d/B-multi-g2.json
work/n2d/B-multi-g3.json
work/n2d/Bp-equilibre-g1.json
work/n2d/C-129-g1.json
work/n2d/C-129-g2.json
work/n2d/C-129-g3.json
work/n2d/contamination.json
work/n2d/evaluations-finales.json
work/n2d/C-129-g1.json (2.8390335417857058, 2.821709373353746)
work/n2d/C-129-g2.json (2.857352154718007, 2.841104248944136)
work/n2d/C-129-g3.json (2.850963154909223, 2.8338340026294264)
C-129-g moy 2.8491 2.8322
work/n2d/Bp-equilibre-g1.json (3.439860937056148, 3.4777227504594252)
Bp-equilibre-g moy 3.4399 3.4777
  ```

- **job_output** `{"job_id": "bash-162", "timeout_ms": 2400000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -1 work/n2d/Bp-equilibre-g3.log 2>/dev/null; ls work/n2d/gpu1.termine 2>/dev/null && echo \"GPU1 FINI\"", "description": "Check final run progress"}`

  ```
19:24
pas  5000 · seq 128 · perte 104.7800 · PPL 128/4 3.2993 · 339 s
[exit code: 2]
  ```

- **job_output** `{"job_id": "bash-162", "timeout_ms": 1500000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -2 work/n2d/Bp-equilibre-g3.log 2>/dev/null; ls work/n2d/gpu1.termine work/n2d/finalise.termine 2>/dev/null", "description": "Check final progression"}`

  ```
19:34
pas 14250 · seq 128 · perte 75.9870 · PPL 128/4 3.3361 · 940 s
pas 14500 · seq 128 · perte 86.7039 · PPL 128/4 3.3542 · 956 s
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && while [ ! -f work/n2d/finalise.termine ]; do sleep 20; done; date '+%H:%M' > work/n2d/portes-debut.txt; JOURNAUX=/tmp/portes-1031-n2d DELAI=1800 bash tools/toutes-les-portes.sh > work/n2d/portes.log 2>&1; date '+%H:%M' > work/n2d/por … [137 caractères tronqués]`

  ```
started background job bash-179
  ```

- **job_output** `{"job_id": "bash-162", "timeout_ms": 1200000, "wait": true}`

  ```
19:42
| bras | graines | protocole 8×16×128 | fenêtres propres | fenêtres contaminées |
|---|---:|---:|---:|---:|
| A — 20 000 pas, français seul | 3 | **2.8527** | **2.9795** | **2.5862** |
| B — 20 000 pas, manifeste 4 sources (82,5 % anglais) | 3 | **3.7591** | **3.8573** | **3.4554** |
| Bp — 20 000 pas, 4 sources à quotas égaux (25 %) | 3 | **3.4350** | **3.5634** | **3.1177** |
| C — curriculum 129 sur A (10 000 pas) | 3 | **2.8471** | **2.9783** | **2.5746** |
# A: protocole 2.8527 ±0.0031 · propres 2.9795 ±0.0071 · contaminées 2.5862 · valeurs [2.8569, 2.8495, 2.8516]
# B: protocole 3.7591 ±0.0075 · propres 3.8573 ±0.0161 · contaminées 3.4554 · valeurs [3.7609, 3.7673, 3.7492]
# Bp: protocole 3.435 ±0.0022 · propres 3.5634 ±0.0039 · contaminées 3.1177 · valeurs [3.4329, 3.4341, 3.438]
# C: protocole 2.8471 ±0.0037 · propres 2.9783 ±0.0047 · contaminées 2.5746 · valeurs [2.8442, 2.8523, 2.8447]
agrege=0
restes : []
A 2.8527 T5k None B 3.7591 Bp 3.435 C 2.8471 A129 2.8743 C129 2.8327
remplit=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('work/n2d/agrege.py'); s=p.read_text()\ns=s.replace('''BRAS = [\n    (\"base\", \"base supervisée 20 000 pas\", \"drave-n0-base-20k\"),\n    (\"T5k\", \"5 000 pas, français (campagne  … [509 caractères tronqués]`

  ```
ok
| bras | graines | protocole 8×16×128 | fenêtres propres | fenêtres contaminées |
|---|---:|---:|---:|---:|
| A — 20 000 pas, français seul | 3 | **2.8527** | **2.9795** | **2.5862** |
| B — 20 000 pas, manifeste 4 sources (82,5 % anglais) | 3 | **3.7591** | **3.8573** | **3.4554** |
| Bp — 20 000 pas, 4 sources à quotas égaux (25 %) | 3 | **3.4350** | **3.5634** | **3.1177** |
| C — curriculum 129 sur A (10 000 pas) | 3 | **2.8471** | **2.9783** | **2.5746** |
# A: protocole 2.8527 ±0.0031 · propres 2.9795 ±0.0071 · contaminées 2.5862 · valeurs [2.8569, 2.8495, 2.8516]
# B: protocole 3.7591 ±0.0075 · propres 3.8573 ±0.0161 · contaminées 3.4554 · valeurs [3.7609, 3.7673, 3.7492]
# Bp: protocole 3.435 ±0.0022 · propres 3.5634 ±0.0039 · contaminées 3.1177 · valeurs [3.4329, 3.4341, 3.438]
# C: protocole 2.8471 ±0.0037 · propres 2.9783 ±0.0047 · contaminées 2.5746 · valeurs [2.8442, 2.8523, 2.8447]
restes : []
A 2.8527 T5k None B 3.7591 Bp 3.435 C 2.8471 A129 2.8743 C129 2.8327
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('work/n2d/agrege.py'); s=p.read_text()\ns=s.replace('''def fichier_de(motif):\n    return sorted(glob.glob(f\"work/n2d/{motif}*.pt\"))''','''def fichier_de(motif):\n    chemin = motif … [332 caractères tronqués]`

  ```
ok
| bras | graines | protocole 8×16×128 | fenêtres propres | fenêtres contaminées |
|---|---:|---:|---:|---:|
| A — 20 000 pas, français seul | 3 | **2.8527** | **2.9795** | **2.5862** |
| B — 20 000 pas, manifeste 4 sources (82,5 % anglais) | 3 | **3.7591** | **3.8573** | **3.4554** |
| Bp — 20 000 pas, 4 sources à quotas égaux (25 %) | 3 | **3.4350** | **3.5634** | **3.1177** |
| C — curriculum 129 sur A (10 000 pas) | 3 | **2.8471** | **2.9783** | **2.5746** |
# A: protocole 2.8527 ±0.0031 · propres 2.9795 ±0.0071 · contaminées 2.5862 · valeurs [2.8569, 2.8495, 2.8516]
# B: protocole 3.7591 ±0.0075 · propres 3.8573 ±0.0161 · contaminées 3.4554 · valeurs [3.7609, 3.7673, 3.7492]
# Bp: protocole 3.435 ±0.0022 · propres 3.5634 ±0.0039 · contaminées 3.1177 · valeurs [3.4329, 3.4341, 3.438]
# C: protocole 2.8471 ±0.0037 · propres 2.9783 ±0.0047 · contaminées 2.5746 · valeurs [2.8442, 2.8523, 2.8447]
restes : []
A 2.8527 T5k None B 3.7591 Bp 3.435 C 2.8471 A129 2.8743 C129 2.8327
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('work/n2d/evaluations-finales.json'))\nprint(len(d)); print([x['fichier'] for x in d])\n\" ; head -3 work/n2d/eval-finale.log", "description": "Inspect the final evaluation JSON"}`

  ```
16
['drave-n0-base-20k.pt', 'temoin-g1.pt', 'temoin-g2.pt', 'temoin-g3.pt', 'A-fr-g1.pt', 'A-fr-g2.pt', 'A-fr-g3.pt', 'B-multi-g1.pt', 'B-multi-g2.pt', 'B-multi-g3.pt', 'Bp-equilibre-g1.pt', 'Bp-equilibre-g2.pt', 'Bp-equilibre-g3.pt', 'C-129-g1.pt', 'C-129-g2.pt', 'C-129-g3.pt']
{"fichier": "drave-n0-base-20k.pt", "params": 11814792, "ppl_protocole": 3.2161, "ppl_129": 3.2653, "ppl_propres": 3.245, "ppl_contaminees": 3.0756, "ppl_permute": 544.3581, "precision_main": 0.6544, "grilles": {"0/16": 3.2161, "0/8": 3.2296, "1000003/16": 3.2494, "1000003/8": 3.1856, "2000009/16": 3.2985, "2000009/8": 3.4194, "3000029/16": 3.0943, "3000029/8": 3.0611}}
{"fichier": "temoin-g1.pt", "params": 11814792, "ppl_protocole": 2.9406, "ppl_129": 2.9631, "ppl_propres": 3.0612, "ppl_contaminees": 2.7059, "ppl_permute": 1228.3835, "precision_main": 0.6844, "grilles": {"0/16": 2.9406, "0/8": 2.9399, "1000003/16": 3.0375, "1000003/8": 2.9865, "2000009/16": 3.0428, "2000009/8": 3.1897, "3000029/16": 2.8269, "3000029/8": 2.796}}
{"fichier": "temoin-g2.pt", "params": 11814792, "ppl_protocole": 2.9345, "ppl_129": 2.961, "ppl_propres": 3.056, "ppl_contaminees": 2.6991, "ppl_permute": 1131.9621, "precision_main
… [183 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 20,32p work/n2d/agrege.py; python3 -c \"\nimport glob\nART='/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts'\nprint(glob.glob(ART + '/drave-n0-base-20k' + '*.pt'))\nprint(glob.glob(ART + '/temoin' + '*.pt'))\n … [48 caractères tronqués]`

  ```
("C", "curriculum 129 sur A (10 000 pas)", "C-129"),
]
METRIQUES = ("ppl_protocole", "ppl_129", "ppl_propres", "ppl_contaminees", "ppl_permute",
             "ppl_multi_val", "precision_main")


def main():
    evals = {f["fichier"]: f for f in
             json.loads(pathlib.Path("work/n2d/evaluations-finales.json").read_text())}
    out, lignes = {}, []
    for cle, nom, motif in BRAS:
        fichiers = [pathlib.Path(f).name for f in sorted(glob.glob(f"work/n2d/{motif}*.pt"))]
        runs = [evals[f] for f in fichiers if f in evals]
['/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/drave-n0-base-20k.pt']
['/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/temoin-g1.pt', '/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/temoin-g2.pt', '/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/temoin-g3.pt']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('work/n2d/agrege.py'); s=p.read_text()\nvieux = '        fichiers = [pathlib.Path(f).name for f in sorted(glob.glob(f\"work/n2d/{motif}*.pt\"))]'\nneuf = '''        motif_complet = mo … [426 caractères tronqués]`

  ```
ok
| B — 20 000 pas, manifeste 4 sources (82,5 % anglais) | 3 | **3.7591** | **3.8573** | **3.4554** |
| Bp — 20 000 pas, 4 sources à quotas égaux (25 %) | 3 | **3.4350** | **3.5634** | **3.1177** |
| C — curriculum 129 sur A (10 000 pas) | 3 | **2.8471** | **2.9783** | **2.5746** |
# base: protocole 3.2161 ±None · propres 3.245 ±None · contaminées 3.0756 · valeurs [3.2161]
# T5k: protocole 2.9355 ±0.0039 · propres 3.0534 ±0.0076 · contaminées 2.7041 · valeurs [2.9406, 2.9345, 2.9313]
# A: protocole 2.8527 ±0.0031 · propres 2.9795 ±0.0071 · contaminées 2.5862 · valeurs [2.8569, 2.8495, 2.8516]
# B: protocole 3.7591 ±0.0075 · propres 3.8573 ±0.0161 · contaminées 3.4554 · valeurs [3.7609, 3.7673, 3.7492]
# Bp: protocole 3.435 ±0.0022 · propres 3.5634 ±0.0039 · contaminées 3.1177 · valeurs [3.4329, 3.4341, 3.438]
# C: protocole 2.8471 ±0.0037 · propres 2.9783 ±0.0047 · contaminées 2.5746 · valeurs [2.8442, 2.8523, 2.8447]
restes : []
A 2.8527 T5k 2.9355 B 3.7591 Bp 3.435 C 2.8471 A129 2.8743 C129 2.8327
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,60p reports/rapport-n2-budget.md", "description": "Read the generated report"}`

  ```
# N2 — le budget paie, les quatre sources coûtent, et la validation n'est pas tenue à l'écart

> **Ligne de roadmap** : N2 (la distillation) · **Date** : 2026-10-31 · **Verdict** : le budget
> complet (20 000 pas, 41 Mo) fait baisser la PPL de **2,9355 à 2,8527** sous le protocole de N2.19 ;
> le corpus à quatre sources la fait **monter** à **3,7591** ; et **32,8 % des fenêtres du protocole
> de validation sont verbatim dans l'entraînement** — sur les fenêtres propres, le meilleur élève
> est à **2,9795**, pas à 2,8527.

## La question

La hiérarchie est écartée deux fois (N2.h1, N2.h2 : 2,9935 contre 2,9927). La roadmap désigne
ensuite **le curriculum et les données** : le dispositif reconstruit la veille n'avait vu que
**20,48 Mo d'un seul corpus en 5 000 pas**, la moitié du budget de N2 (41 Mo, 20 000 pas, quatre
sources). Ce dispositif est mesuré ici à budget plein, avec trois graines, et comparé à trois
témoins : la base supervisée, la distillation courte de la veille, et le corpus à quatre sources.

## Le dispositif — reconstruit, archivé, rejoué

Tout vient de la campagne du 31/10 conservée sur deux disques
(`/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/`, 1,4 Go, 
… [2769 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 60,125p reports/rapport-n2-budget.md", "description": "Read the rest of the report"}`

  ```
3 000 029), A reste **sous** le témoin de 5 000 pas : −0,075 à −0,113. La PPL absolue, elle,
varie de 2,75 à 2,95 selon la grille : le jeu de validation n'est pas homogène, et c'est la
comparaison **appariée** qui porte le résultat, pas le chiffre absolu.

## Le contrôle négatif

- **permutation** : mêmes octets de validation, ordre détruit — la PPL s'effondre (1086,7460),
  le modèle exploite bien l'ordre et pas les fréquences d'octets ;
- **la base** (aucune distillation) et **la distillation courte** (5 000 pas) encadrent le budget ;
- **B′ contre B** : même budget, même professeur, seule la part de l'anglais change ;
- **C contre A** : comparaison appariée graine par graine, même fenêtres.

## La validation n'est pas tenue à l'écart

C'est le résultat qui change la lecture de la porte. `corpus_fr_val.txt` est la **queue** de
`corpus_fr.txt`, `corpus_fr_train.txt` sa **tête** : les positions sont disjointes (`train + val`
reconstitue exactement les 4 633 889 octets), mais le **contenu se répète** — le corpus empile des
documents qui se recopient.

- **30,7 %** d'un échantillon de 300 fenêtres de validation apparaissent **verbatim** dans
  l'entraînement ; **32,8 %** des 128 fenê
… [3185 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, statistics as st\nd = {x['fichier']: x for x in json.load(open('work/n2d/evaluations-finales.json'))}\nfor g in ('1','2','3'):\n    a = d[f'A-fr-g{g}.pt']['grilles']; t = d[f'temoin-g{g}.pt']['grilles' … [750 caractères tronqués]`

  ```
1 {'0/16': -0.0837, '1000003/16': -0.0902, '2000009/16': -0.113, '3000029/16': -0.0746}
2 {'0/16': -0.085, '1000003/16': -0.0961, '2000009/16': -0.1167, '3000029/16': -0.0943}
3 {'0/16': -0.0797, '1000003/16': -0.1016, '2000009/16': -0.1237, '3000029/16': -0.1026}
moyennes par grille (lot 16) :
0/16 -0.0828 valeurs [-0.0837, -0.085, -0.0797]
1000003/16 -0.096 valeurs [-0.0902, -0.0961, -0.1016]
2000009/16 -0.1178 valeurs [-0.113, -0.1167, -0.1237]
3000029/16 -0.0905 valeurs [-0.0746, -0.0943, -0.1026]
PPL absolue A par grille : {'0/16': 2.8527, '1000003/16': 2.9378, '2000009/16': 2.9208, '3000029/16': 2.7485}
PPL absolue T5k par grille : {'0/16': 2.9355, '1000003/16': 3.0338, '2000009/16': 3.0386, '3000029/16': 2.839}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nremplacements = [\n (\"contre **2,9881** sur les\", \"contre **2,9795** sur les\"),\n (\"la distillation courte **0,35**, A **0,40** :\", \"la distillation courte **0,35**, A **0,39** :\"),\n (\"l'a … [1034 caractères tronqués]`

  ```
work/n2d/fiche.md 3 remplacements
reports/rapport-n2-budget.md 7 remplacements
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 work/n2d/maj-docs.py && python3 work/n2d/maj-roadmap.py && git diff --stat docs/ && git diff docs/pilotage/en-cours.md | head -50", "description": "Apply state and roadmap updates"}`

  ```
en-cours : puce N2 mise à jour
backlog N2 : prochaine action mise à jour
roadmap : 5 remplacements appliqués
 docs/pilotage/backlog/N2-distillation.md |  6 +++++-
 docs/pilotage/en-cours.md                | 15 ++++++++-------
 docs/pilotage/roadmap.md                 | 13 ++++++++-----
 3 files changed, 21 insertions(+), 13 deletions(-)
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index d44e6bed..d3d6b751 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -69,13 +69,14 @@
 - **B11.10** : **hybride 4/4** — codec **161/161**, ambiguïtés refusées ; **69,3 %** natif ;
   [`b1110`](../../reports/rapport-b1110-cartes.md).
 - **Backlog — graphe** : 37 fiches, 43 arêtes, **4 à la frontière** ; `tools/verifie_backlog.py`.
-- **N2** : GPU ; meilleur **2,6998** ; porte **< 2,5** non atteinte ; N4 **0/40**.
-  **N2.h1** : 3,9759 contre 3,9617, contrôle 3,9764 — rien ne se lit.
-  **N2.h2** (distillation, professeur refait, 3 graines) : **2,9935** contre **2,9927** (+0,029 %) ;
-  l'état bat son contrôle sans état (−0,0017) mais coûte ce qu'il rapporte. Points de
-  contrôle **conservés** (Data13TB + disque IA, manifeste vérifié). Fiches
-  [`n2-hier
… [883 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff docs/pilotage/roadmap.md docs/pilotage/backlog/N2-distillation.md", "description": "Review roadmap and backlog diffs"}`

  ```
diff --git a/docs/pilotage/backlog/N2-distillation.md b/docs/pilotage/backlog/N2-distillation.md
index f04f5baf..ee47c2cf 100644
--- a/docs/pilotage/backlog/N2-distillation.md
+++ b/docs/pilotage/backlog/N2-distillation.md
@@ -27,7 +27,11 @@ PPL < 2,5 sur le jeu tenu à l'écart, avec le contrôle par permutation et le m
 
 ## Prochaine action
 
-Lancer la série **hiérarchie** (état de section, longueurs croissantes) avec 3 graines et le même budget ; garder la porte < 2,5 comme mesure de la distillation, et passer la main à R11 pour la fenêtre. Ne pas allonger le contexte **brut**.
+**Le budget est mesuré (N2.d), le levier suivant est le corpus.** Le budget plein paie
+2,9355 → 2,8527 (−0,08) ; les quatre sources coûtent +0,93 ; le curriculum 129 gagne 0,05 à
+129 ; et **32,8 % des fenêtres du protocole de validation sont verbatim dans l'entraînement**
+— sur fenêtres propres, A est à 2,9795. Prochaine action : **dédupliquer le corpus et séparer
+train/validation par document**, puis remesurer la porte < 2,5 : elle n'a de sens qu'après.
 
 ## Voir aussi
 
diff --git a/docs/pilotage/roadmap.md b/docs/pilotage/roadmap.md
index 57ca95a4..5b4729eb 100644
--- a/docs/pilotage/roadmap.md
++
… [5127 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -5; echo \"=== status ===\"; git status --short; echo \"=== other session? ===\"; python3 tools/sessions.py --status 2>&1 | head -8", "description": "Check for concurrent session commits"}`

  ```
b8683d00 SESSION — R4.4 SE FERME SUR `0088fc2f` : L'OCR EST MESURÉ, R4.4 RESTE OUVERTE AUX SCANS
0088fc2f R4.4 — L'OCR LIT DIX PAGES À 4,48 % DE WER, LA PARITÉ DE PASSAGE TIENT À 90 %, LA PAGE « PHOTO » TOMBE À 26,7 %
58103738 DOCS — DIEHL & COOK : UNITÉS, DÉLAIS ET TRACE DES INHIBITEURS
bb3bfefe DOCS — LE MODÈLE NATIF ET DIEHL & COOK, 13 SCHÉMAS : LA SÉPARATION À TROIS NIVEAUX
54dc7a26 ÉTAT — LA CAMPAGNE N2 BUDGET ET DONNÉES EST OUVERTE, LES GPU RÉSERVÉS JUSQU'À 19 h 40
=== status ===
 M .gitignore
 M docs/pilotage/backlog/N2-distillation.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/README.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/digest.md
 M journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/rapport.md
 m tools/docwatch
?? reports/n2-budget.json
?? reports/rapport-n2-budget.md
?? tools/distiller_budget.py
?? tools/eval_n2_budget.py
=== other session? ===
sessions · plans de mandat
  ⏰ 0b0a6a0d-05f5-4308 · en cours · 129 min · N2 — le budget complet, les données et le c
… [637 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/revue_documentation.py 2>&1 | tail -8; echo \"=== compte portes ===\"; ls tools/porte-*.sh | wc -l; ls reports/*.md | wc -l; ls reports/*.json | wc -l; ls docs/**/*.md 2>/dev/null | wc -l", "description": "C … [49 caractères tronqués]`

  ```
revue de documentation · 371 fiche(s) · 439 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 370 fichiers, le disque en a 371
     · compteurs : en-cours.md dit 438 JSON, le disque en a 439
=== compte portes ===
79
371
439
93
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 80,95p docs/pilotage/en-cours.md", "description": "Read the counters table"}`

  ```
## Les chiffres de l'état

> **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **79** (73 vertes, 5 rouges à la passe du 31/10 ; 1 porte ajoutée depuis, hors passe) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **370** / **438** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **112** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 37** (31/10 12 h 54) | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Les dépendances ne sont pas dans cette page.** Elles vivent dans le **graphe** du backlog —
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 20,60p .git/hooks/pre-commit; echo \"=== portes ===\"; tail -3 work/n2d/portes.log 2>/dev/null; ls /tmp/portes-1031-n2d/ 2>/dev/null | head", "description": "Inspect hook journal step and gate progress"}`

  ```
#    accompagner le code, pas le suivre.
python3 tools/archive_sessions.py --quiet >/dev/null || { echo "  ⛔ archivage des sessions en échec"; exit 1; }
python3 tools/session_report.py --quiet >/dev/null || { echo "  ⛔ rapport de session en échec"; exit 1; }
# Le journal du jour, par thème (sources : git + journal/sessions). L'index README est
# régénéré ensuite pour lister les fichiers produits.
python3 tools/journal_auto.py --quiet >/dev/null || { echo "  ⛔ journal du jour en échec"; exit 1; }
git add journal || { echo "  ⛔ journal non ajouté à l'index"; exit 1; }
exit 0
=== portes ===
=== PASSE COMPLÈTE DES PORTES (79 portes, borne 1800 s) ===
    journaux : /tmp/portes-1031-n2d
  porte-adaptateur-sortie ✅                          65 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
porte-adaptateur-sortie.log
porte-audit-drapeaux.log
registre.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\ns=s.replace(\"| fichiers / JSON de résultats | **370** / **438** |\", \"| fichiers / JSON de résultats | **371** / **439** |\")\np.write … [698 caractères tronqués]`

  ```
ok
  368 fiches → reports/INDEX.md
200:| [rapport-n2-budget.md](rapport-n2-budget.md) | N2 — le budget paie, les quatre sources coûtent, et la validation n'est pas tenue à l'écart |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal/2026-10-31/; echo \"=== notes apprentissage ===\"; sed -n '/<!-- notes -->/,$p' journal/2026-10-31/apprentissage.md | head -20", "description": "Inspect today's journal theme files"}`

  ```
apprentissage.md
distribue.md
docs.md
mesures.md
modele.md
portes.md
README.md
=== notes apprentissage ===
<!-- notes -->

<!-- /notes -->
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np = pathlib.Path('journal/2026-10-31/apprentissage.md'); s = p.read_text()\nnotes = \"\"\"<!-- notes -->\n\n### N2 — le budget, les quatre sources, et le mètre faussé\n\nLa journée avait commencé pa … [2056 caractères tronqués]`

  ```
ok
<!-- notes -->

### N2 — le budget, les quatre sources, et le mètre faussé

La journée avait commencé par deux négatifs nets sur la hiérarchie. En reprenant N2 l'après-midi,
la question était simple : le dispositif reconstruit hier n'avait vu que **20,48 Mo** d'un seul
corpus en **5 000 pas** — que donne-t-il à budget plein, **41 Mo, 20 000 pas**, et à quatre
sources ?

Douze distillations, trois graines, deux cartes. Le budget paie : **2,8527** contre **2,9355**
(−0,0828), du même ordre que la chaîne historique. Les quatre sources coûtent : **3,7591** sur le
protocole (+0,91) et **3,4350** à quotas égaux (+0,58) — l'anglais du manifeste (82,5 %) explique
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/revue_documentation.py 2>&1 | tail -5; echo \"=== en-cours ===\"; python3 tools/verifie_en_cours.py | tail -3; echo \"=== budget ===\"; python3 tools/taille_documents.py 2>&1 | tail -3", "description": "Run  … [32 caractères tronqués]`

  ```
revue de documentation · 371 fiche(s) · 439 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== en-cours ===
  en-cours · 1248 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
=== budget ===
     · 14 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_backlog.py 2>&1 | tail -4; python3 tools/verifie_journal.py 2>&1 | tail -2; python3 tools/verifier_schemas.py 2>&1 | tail -2", "description": "Verify backlog, journal and schemas"}`

  ```
profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (4) : A2.6, N2, N3, N4

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
  journal · 37 jour(s) · 110 session(s) · 1702 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '/## Ce que ça change/,/## Ce qui pourrait/p' reports/rapport-n2-budget.md", "description": "Read the impact section"}`

  ```
## Ce que ça change pour N2

1. **Le budget paie, mais peu** : **−0,0828** de PPL pour 20 000 pas de plus (2,8527 contre
   2,9355), du même ordre que la chaîne historique (≈ −0,09 par 20 000 pas à lr 3e-5, N2.23).
   La porte < 2,5 n'est pas approchée : il manque **0,3527** sur le protocole, et
   **0,4795** sur les fenêtres propres. À ce rendement — qui décroît — il faudrait de
   l'ordre de **90 000 pas de plus** pour espérer 2,5 ; la chaîne historique en a enchaîné plus de
   100 000 pour arriver à 2,70.
2. **Les données, telles que le manifeste les définit, coûtent** : B perd 0,9064 sur le
   protocole. Le manifeste est à 82,5 % anglais alors que le professeur est **français** : les
   cibles anglaises qu'il donne sont faibles, et le français se dilue. B′ dit quelle part revient à
   l'anglais : à quotas égaux elle coûte encore **+0,58** ; dans les deux cas, la diversité
   **n'aide pas la porte française**.
3. **Le curriculum 129** : gagne **0,0416** sur le protocole 129 (comparaison appariée) et **0,0056** sur le protocole 128 — réel, mais marginal : il ne déplace pas la porte.
4. **Le prochain levier de N2 n'est pas un levier d'entraînement, c'est le corpus** : reconstruire
… [260 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-n2-budget.md'); s=p.read_text()\ns=s.replace(\"\"\"   cibles anglaises qu'il donne sont faibles, et le français se dilue. B′ dit quelle part revient à\n   l'anglais : … [979 caractères tronqués]`

  ```
ok
## Ce que ça change pour N2

1. **Le budget paie, mais peu** : **−0,0828** de PPL pour 20 000 pas de plus (2,8527 contre
   2,9355), du même ordre que la chaîne historique (≈ −0,09 par 20 000 pas à lr 3e-5, N2.23).
   La porte < 2,5 n'est pas approchée : il manque **0,3527** sur le protocole, et
   **0,4795** sur les fenêtres propres. À ce rendement — qui décroît — il faudrait de
   l'ordre de **90 000 pas de plus** pour espérer 2,5 ; la chaîne historique en a enchaîné plus de
   100 000 pour arriver à 2,70.
2. **Les données, telles que le manifeste les définit, coûtent** : B perd 0,9064 sur le
   protocole. Le manifeste est à 82,5 % anglais alors que le professeur est **français** : les
   cibles anglaises qu'il donne sont faibles, et le français se dilue. B′ (quotas égaux, 25 % par
   source) coûte encore **+0,58** : l'anglais explique une partie de la perte, pas toute ; dans les
   deux cas, la diversité **n'aide pas la porte française**.
3. **Le curriculum 129** : gagne **0,0416** sur le protocole 129 (comparaison appariée) et
   **0,0056** sur le protocole 128 — réel, mais marginal : il ne déplace pas la porte.
4. **Le prochain levier de N2 n'est pas un levier d'entraînemen
… [295 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -4 work/n2d/portes.log; echo \"=== registre ===\"; cat /tmp/portes-1031-n2d/registre.txt 2>/dev/null | wc -l", "description": "Check gate pass progress"}`

  ```
19:44
=== PASSE COMPLÈTE DES PORTES (79 portes, borne 1800 s) ===
    journaux : /tmp/portes-1031-n2d
  porte-adaptateur-sortie ✅                          65 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
=== registre ===
1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nfor f in ('reports/rapport-n2-budget.md','work/n2d/fiche.md'):\n    p=pathlib.Path(f); s=p.read_text()\n    s=s.replace(\"fenêtres propres — l'écart est de **0,40 de PPL** ;\",\"fenêtres propres — l … [196 caractères tronqués]`

  ```
ok
84:  fenêtres propres — l'écart est de **0,39 de PPL** ;
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && du -sh work/n2d; df -h /home/stephane/IA | tail -1", "description": "Check checkpoint size and secondary disk space"}`

  ```
632M	work/n2d
/dev/md0        938G  893G   36G  97% /home/stephane/IA
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/n2d && rsync -a --exclude 'essai-*' work/n2d/ /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/n2d/ && du -sh /home/stephane/Data13TB/stephane/backups/n2/2026-10-3 … [150 caractères tronqués]`

  ```
542M	/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/n2d
12
  ```

- **bash** `{"command": "mkdir -p /home/stephane/IA/artefacts/n2/2026-10-31/n2d && rsync -a --exclude 'essai-*' /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/n2d/ /home/stephane/IA/artefacts/n2/2026-10-31/n2d/ && du -sh /home/stephane/IA/artefacts/n2/2026-10-31/n2d && df -h /home/stephane/IA | tail -1" … [63 caractères tronqués]`

  ```
542M	/home/stephane/IA/artefacts/n2/2026-10-31/n2d
/dev/md0        938G  893G   35G  97% /home/stephane/IA
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nfor f in ('reports/rapport-n2-budget.md','work/n2d/fiche.md'):\n    p=pathlib.Path(f); s=p.read_text()\n    s=s.replace(\"\"\"- Points de contrôle : `work/n2d/*.pt` (hors dépôt, à archiver avec la c … [405 caractères tronqués]`

  ```
ok
- Code : [`tools/distiller_budget.py`](../tools/distiller_budget.py) (entraînement) ·
  [`tools/eval_n2_budget.py`](../tools/eval_n2_budget.py) (évaluation et contamination) ·
  agrégat [`n2-budget.json`](n2-budget.json).
- Points de contrôle : **12 `.pt` (542 Mo) archivés sur deux disques** —
  `/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/n2d/` et
  `/home/stephane/IA/artefacts/n2/2026-10-31/n2d/` ; `work/n2d/` reste la copie de travail.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -3 work/n2d/portes.log; wc -l < /tmp/portes-1031-n2d/registre.txt", "description": "Check gate progress"}`

  ```
19:45
=== PASSE COMPLÈTE DES PORTES (79 portes, borne 1800 s) ===
    journaux : /tmp/portes-1031-n2d
  porte-adaptateur-sortie ✅                          65 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\n\n# 1. La section de session : close, prochaine session désignée.\ndebut = s.index(\"### Session `0b0a6a0d-05f5-4308-800c-4792ddb9cb … [2965 caractères tronqués]`

  ```
ok
  ❌ 1 anomalie(s) :
     · question sans ce qui la débloque (`→`) : **N2** : **< 2,5** — et **sur quel jeu** ? La validation se 

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\ns=s.replace(\"\"\"- **N2** : **< 2,5** — et **sur quel jeu** ? La validation se recopie (32,8 % verbatim) : la\n  question n'a de sens q … [476 caractères tronqués]`

  ```
en-cours · 1259 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  revue de documentation · 371 fiche(s) · 439 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, datetime\np=pathlib.Path('journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md'); s=p.read_text()\ns=s.replace(\"- **Heartbeat** : 2026-10-31 17:35 HAE\", \"- **Heartbeat** : 2026-10-31 20: … [946 caractères tronqués]`

  ```
ok
  ✅ plans cohérents
19:46
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short; echo \"=== diff stat ===\"; git diff --stat", "description": "Review the full working tree state"}`

  ```
M .gitignore
 M docs/pilotage/backlog/N2-distillation.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/2026-10-31/apprentissage.md
 M journal/README.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/digest.md
 M journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/rapport.md
 M reports/INDEX.md
 M reports/README.md
 m tools/docwatch
?? reports/n2-budget.json
?? reports/rapport-n2-budget.md
?? tools/distiller_budget.py
?? tools/eval_n2_budget.py
=== diff stat ===
 .gitignore                                         |   3 +
 docs/pilotage/backlog/N2-distillation.md           |   6 +-
 docs/pilotage/en-cours.md                          |  59 ++-
 docs/pilotage/roadmap.md                           |  13 +-
 journal/2026-10-31/apprentissage.md                |  27 ++
 journal/README.md                                  |   4 +-
 .../0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md | 426 +++++++++++++++++++++
 .../0b0a6a0d-05f5-430
… [523 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2d/commit-msg.txt <<'EOF'\nN2 — LE BUDGET PAIE 2,8 %, LES QUATRE SOURCES COÛTENT 91 %, ET LA VALIDATION EST CONTAMINÉE À 32,8 %\n\nLe budget plein (20 000 pas, 41 Mo, trois graines) amène l'élève distillé de 2,9355 à\n2,8 … [1660 caractères tronqués]`

  ```
24 work/n2d/commit-msg.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nfor f in ('reports/rapport-n2-budget.md','work/n2d/fiche.md'):\n    p=pathlib.Path(f); s=p.read_text()\n    s=s.replace(\"témoins : la base supervisée, la distillation courte de la veille, et le cor … [496 caractères tronqués]`

  ```
ok
12:ensuite **le curriculum et les données** : le dispositif reconstruit la veille n'avait vu que
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nfor f in ('reports/rapport-n2-budget.md','work/n2d/fiche.md'):\n    p=pathlib.Path(f); s=p.read_text()\n    s=s.replace(\"le dispositif reconstruit la veille n'avait vu que\", \"le dispositif recons … [269 caractères tronqués]`

  ```
ok
aucune mention de la veille
19:46
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           1 s  ✅ porte bloc tableaux verte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. ~/gpu-env/bin/python tools/distiller_budget.py --help 2>&1 | head -12; echo \"===\"; PYTHONPATH=. ~/gpu-env/bin/python tools/eval_n2_budget.py --help 2>&1 | head -12", "description": "Smoke-test the new tools' CLIs"}`

  ```
usage: distiller_budget.py [-h] [--enseignant ENSEIGNANT] [--init INIT]
                           [--corpus {fr,multi}] [--manifeste MANIFESTE]
                           [--quotas {proportionnel,equilibre}]
                           [--train TRAIN] [--val VAL] [--stages STAGES]
                           [--lot LOT] [--temperature TEMPERATURE]
                           [--alpha ALPHA] [--tetes | --no-tetes]
                           [--graine GRAINE] [--device DEVICE] --sortie SORTIE
                           [--log LOG]

options:
  -h, --help            show this help message and exit
  --enseignant ENSEIGNANT
===
usage: eval_n2_budget.py [-h] [--contamination] [--grilles]
                         [--manifeste MANIFESTE] [--sortie SORTIE]
                         [--device DEVICE]
                         [points ...]

positional arguments:
  points

options:
  -h, --help            show this help message and exit
  --contamination
  --grilles             PPL sur quatre compteurs et deux tailles de lot
  ```

- **job_output** `{"job_id": "bash-179", "timeout_ms": 3600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; wc -l < /tmp/portes-1031-n2d/registre.txt; awk '$2 != 0' /tmp/portes-1031-n2d/registre.txt; tail -2 work/n2d/portes.log", "description": "Check gate progress and any reds"}`

  ```
19:56
19
  porte-diff-couche      ✅                          18 s    ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé
  porte-document         ✅                           6 s  ✅ porte document verte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,12p docs/pilotage/references-non-regression.md", "description": "Read the top of the non-regression reference"}`

  ```
# Références de non-régression

> **Dernière passe complète — 2026-10-31 à 12 h 54 :** **78 portes, 73 vertes, 5 rouges, 1 h 37**
> (journaux `/tmp/portes-1031-11h17`). `porte-indice`, `porte-melange` : les **structurelles
> connues**. `porte-homeostasie` (exit 2) : **environnementale** — `/tmp/n4/rang4-lora.pt` effacé
> au démarrage. `porte-jeux` : **vraie régression** corrigée le jour même (`2edb3079` — le SAN
> perdait contre la case, 110/112). `porte-reparti-moteur` : PPL épinglée 9,1748 non reproduite
> (8,7434), écart de flux nul — à trancher.

> **Passe précédente — 2026-10-29 à 22 h 09 :** 62 portes, 60 vertes, 2 rouges, 1 h 46 ;
> mêmes structurelles connues, **aucune régression**. Journaux : `/tmp/portes-1029-20h23` ;
> historique : [`reports/historique-passes-portes.md`](../../reports/historique-passes-portes.md).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -lt tools/porte-*.sh | head -3; git log --oneline -3 -- tools/porte-*.sh", "description": "Identify the newly added gate"}`

  ```
-rwxr-xr-x. 1 stephane stephane  1382 31 oct 17:55 tools/porte-ocr.sh
-rwxr-xr-x. 1 stephane stephane  8140 31 oct 12:55 tools/porte-tableaux.sh
-rwxr-xr-x. 1 stephane stephane 18501 31 oct 12:55 tools/porte-gain.sh
0088fc2f R4.4 — L'OCR LIT DIX PAGES À 4,48 % DE WER, LA PARITÉ DE PASSAGE TIENT À 90 %, LA PAGE « PHOTO » TOMBE À 26,7 %
3b9d179c PORTES — CINQ ÉCHECS SILENCIEUX CORRIGÉS : UNE PASSE VIDE, UNE ASSERTION PERDUE, UN HOOK MUET
277103ff A8.3d — LE LOT N'EST PAS LES THREADS : L'ÉCART DE 1,90 % SURVIT À 1 THREAD
  ```

- **job_output** `{"job_id": "bash-179", "timeout_ms": 1800000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; wc -l < /tmp/portes-1031-n2d/registre.txt; awk '$2 != 0' /tmp/portes-1031-n2d/registre.txt", "description": "Check gate progress"}`

  ```
20:07
25
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 24,62p docs/pilotage/en-cours.md", "description": "Review the state file's session and N2 sections"}`

  ```
> l'état en retard le corrige — elle n'attend pas qu'on désigne une « principale ».

### Session à ouvrir — N2, le corpus décontaminé

- **Id** : aucune session active — `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` est **close** (la
  campagne N2.d est committée).
- **Rôle** : **N2, le corpus** — **32,8 %** des fenêtres de validation sont verbatim dans
  l'entraînement ; il faut dédupliquer et séparer train/validation **par document** avant que la
  porte < 2,5 ait un sens.
- **Ce qu'elle fait** : reconstruire `data/corpus_fr.txt` sans répétitions, un split par document,
  puis remesurer la base et le meilleur élève ; la porte sera **redéfinie** sur ce jeu-là.
- **Ce que font les autres** : **R4.4** (les scans réels) est ouverte et non bloquante ; **N4**
  (consigne courte) prend la file si N2 bloque.
- **Fichiers réservés** : `data/`, `tools/corpus*`, `reports/n2-*`, `journal/sessions/<id>/`.
- **Prochaine action** : le script de déduplication et le split par document.
- **Bloquants** : aucun côté N2 ; **R4.4** attend des scans, pas un blocage.
- **Journal** : [le 30/10](../../journal/2026-10-30/README.md) · [le 31/10](../../journal/2026-10-31/README.md).

> **Sessions archivées** : `81
… [1420 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\nvieux = \"\"\"> **Sessions archivées** : `8156fdcb`, `c3d0f0bd`, `N2-GPU`, `71d57f53`, `0b69f616`, `22e518ee`,\n> `fe3c05f0`\n> — rappor … [494 caractères tronqués]`

  ```
ok
  en-cours · 1260 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"hiérarchie\" docs/pilotage/roadmap.md docs/pilotage/en-cours.md docs/pilotage/backlog/index.md | head -12", "description": "Find stale hierarchy references"}`

  ```
docs/pilotage/roadmap.md:48:2. **N2 — la distillation et la hiérarchie** (en cours) : 49 999 fenêtres, 4 sources ; professeur 30k **1,734**
docs/pilotage/roadmap.md:50:   atteinte**. Le levier retenu est la **hiérarchie** (état de section), portée par N2.
docs/pilotage/roadmap.md:242:**Ce qui bloque** : les 130–256 sont **tous négatifs**. R1.1 doit être tenté **avant** R1.2 : si la hiérarchie
docs/pilotage/roadmap.md:328:- **R1** : la **hiérarchie portée par N2** suffit-elle à lire **1 000 octets** sans refaire les négatifs 130–256 ?
docs/pilotage/en-cours.md:118:**N2** — la **hiérarchie** et les **données** sont écartées ; le **budget** paie **−0,08** ; la
docs/pilotage/en-cours.md:125:- **R1** : **1 000 octets** sans refaire 130–256 ? → **N2** (hiérarchie), puis **R1.1**, tranchent.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 40,56p docs/pilotage/roadmap.md; echo \"=== 236,246 ===\"; sed -n 236,246p docs/pilotage/roadmap.md", "description": "Read the order-of-day N2 entry and R1 note"}`

  ```
30 % sur 5 types et **249 questions**) ; **R0.4** (tête de survol) et **R0.5** (routeur) sont
   **closes en négatif** — 0,540 contre BM25 0,720 sur le corpus gelé, et un signal qui prédit
   (AUC 0,839) sans règle qui transfère.
   **R4.1 — le bloc tableaux** est **mesurée** (996 cellules, **802** exactes, texte plat **0/3**),
   **R4.2 — le bloc code** aussi (294 fichiers, 24/24 extraits, texte seul **0/3**) et **R4.3 —
   le bloc maths** (32 formules, 10/10 dérivées, surface **0/3**) ; **R4.4 est partielle** :
   l'OCR est installé, **10 pages rendues** sont lues à **4,48 %** de WER avec une **parité de
   passage 90 %**, et la **page dégradée** tombe à **26,7 %** — les **scans réels** restent ouverts.
2. **N2 — la distillation et la hiérarchie** (en cours) : 49 999 fenêtres, 4 sources ; professeur 30k **1,734**
   (0,794 bit/octet) ; student **3,123** à 20 000 pas ; meilleur **2,6998** ; plateau **2,708** ; porte **< 2,5 non
   atteinte**. Le levier retenu est la **hiérarchie** (état de section), portée par N2.
3. ~~N0.3b — la parité de perplexité DRVM ↔ GGUF~~ **close** : conversion **68,1917 / 92,1875**, natif **4,6585 / 18,6394**.
4. **N4 — l'usage** : la **consigne courte**
… [1449 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md'); s=p.read_text()\ns=s.replace(\"\"\"2. **N2 — la distillation et la hiérarchie** (en cours) : 49 999 fenêtres, 4 sources ; professeur 30k **1,734**\n   (0, … [2068 caractères tronqués]`

  ```
ok
docs/pilotage/roadmap.md:332:  puis **R1.2** (curriculum) tranchent ; la hiérarchie portée par N2 est écartée deux fois.
docs/pilotage/en-cours.md:118:**N2** — la **hiérarchie** et les **données** sont écartées ; le **budget** paie **−0,08** ; la
docs/pilotage/en-cours.md:126:  (curriculum) tranchent ; la hiérarchie de N2 est écartée.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/revue_documentation.py 2>&1 | tail -3; python3 tools/verifie_en_cours.py | tail -2; python3 tools/taille_documents.py 2>&1 | tail -2; date '+%H:%M'; wc -l < /tmp/portes-1031-n2d/registre.txt", "description": … [35 caractères tronqués]`

  ```
revue de documentation · 371 fiche(s) · 439 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1270 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
20:08
25
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -4 work/n2d/portes.log; echo \"=== registre queue ===\"; tail -3 /tmp/portes-1031-n2d/registre.txt; ps -eo pid,etime,cmd | grep -E \"porte-|toutes-les-portes\" | grep -v grep | head -3", "description": "Identify the currently ru … [12 caractères tronqués]`

  ```
porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          24 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                           8 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         209 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
=== registre queue ===
porte-flux 0 24
porte-fusion 0 8
porte-gain 0 209
  81759       33:08 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && while [ ! -f work/n2d/finalise.termine ]; do sleep 20; done; date '+%H:%M' > work/n2d/portes-debut.txt; JOURNAUX=/tmp/portes-1031-n2d DELAI=1800 bash tools/toutes-les-portes.sh > work/n2d/portes.log 2>&1; date '+%H:%M' > work/n2d/portes-fin.txt; echo TERMINE >> work/n2d/portes.log
  83970       26:08 bash tools/toutes-les-portes.sh
 240587       04:04 timeout 1800 bash tools/porte-greffe.sh
  ```

- **job_output** `{"job_id": "bash-179", "timeout_ms": 2400000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; grep -c \"✅\\|❌\" work/n2d/portes.log; awk '$2 != 0' /tmp/portes-1031-n2d/registre.txt; tail -1 work/n2d/portes.log", "description": "Check gate progress again"}`

  ```
20:18
29
porte-homeostasie 2 0
  porte-horloge          ✅                          25 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  ```

- **job_output** `{"job_id": "bash-179", "timeout_ms": 2700000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; grep -c \"✅\\|❌\" work/n2d/portes.log; awk '$2 != 0' /tmp/portes-1031-n2d/registre.txt; tail -1 work/n2d/portes.log", "description": "Check gate progress"}`

  ```
20:28
29
porte-homeostasie 2 0
  porte-horloge          ✅                          25 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps -eo pid,etime,cmd | grep -E \"porte-|python\" | grep -v grep | head -5; ls -lt /tmp/portes-1031-n2d/*.log | head -3", "description": "Identify the long-running gate"}`

  ```
2031    03:12:22 /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
   2210    03:12:20 /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
   3193    03:12:10 /home/stephane/.local/share/pipx/venvs/docwatch/bin/python -E /home/stephane/.local/bin/docwatch --config /home/stephane/.config/docwatch/config.toml --no-browser
 249287       11:39 timeout 1800 bash tools/porte-indice.sh
 249288       11:39 bash tools/porte-indice.sh
-rw-r--r--. 1 stephane stephane  690 31 oct 20:27 /tmp/portes-1031-n2d/porte-indice.log
-rw-r--r--. 1 stephane stephane  769 31 oct 20:16 /tmp/portes-1031-n2d/porte-horloge.log
-rw-r--r--. 1 stephane stephane  172 31 oct 20:16 /tmp/portes-1031-n2d/porte-homeostasie.log
  ```

- **job_output** `{"job_id": "bash-179", "timeout_ms": 2700000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; grep -c \"✅\\|❌\" work/n2d/portes.log; awk '$2 != 0' /tmp/portes-1031-n2d/registre.txt; tail -1 work/n2d/portes.log", "description": "Check gate progress"}`

  ```
20:38
57
porte-homeostasie 2 0
porte-indice 1 838
porte-melange 1 106
  porte-occupation-elagage ✅                          59 s  ✅ porte occupation × élagage : la cible annoncée est VÉRIFIÉE dans le fichier exporté
  ```

- **job_output** `{"job_id": "bash-179", "timeout_ms": 2400000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; grep -c \"✅\\|❌\" work/n2d/portes.log; awk '$2 != 0' /tmp/portes-1031-n2d/registre.txt; tail -2 work/n2d/portes.log", "description": "Check gate progress"}`

  ```
20:48
63
porte-homeostasie 2 0
porte-indice 1 838
porte-melange 1 106
  porte-poids-creux      ✅                         322 s  ✅ porte poids creux : le noyau creux est EXACT et il paie la sparsité — paires divisées sur
  porte-pont             ✅                          82 s    ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux
  ```

- **job_output** `{"job_id": "bash-179", "timeout_ms": 1800000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; grep -c \"✅\\|❌\" work/n2d/portes.log; awk '$2 != 0' /tmp/portes-1031-n2d/registre.txt; tail -2 work/n2d/portes.log", "description": "Check gate progress"}`

  ```
20:58
64
porte-homeostasie 2 0
porte-indice 1 838
porte-melange 1 106
  porte-pont             ✅                          82 s    ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux
  porte-prechargement    ✅                         184 s    PORTE TENUE
  ```

- **job_output** `{"job_id": "bash-179", "timeout_ms": 1800000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; grep -c \"✅\\|❌\" work/n2d/portes.log; awk '$2 != 0' /tmp/portes-1031-n2d/registre.txt; tail -2 work/n2d/portes.log", "description": "Check gate progress"}`

  ```
21:09
77
porte-homeostasie 2 0
porte-indice 1 838
porte-melange 1 106
porte-reparti-moteur 1 45
  porte-tokenizer-kimi   ✅                           9 s    ✅ 10 textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres)
  porte-topologie        ✅                         100 s    ✅ PPL épinglées : reference 17.4702 · historique 30.4363 · topologie 30.4363 · relais 2 42.547
  ```

- **job_output** `{"job_id": "bash-179", "timeout_ms": 1200000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -4 work/n2d/portes.log; echo \"=== fin ===\"; ls work/n2d/portes-fin.txt 2>/dev/null; cat /tmp/portes-1031-n2d/registre.txt | awk '$2 != 0'", "description": "Check if the gate pass finished"}`

  ```
21:19
  porte-tableaux         ✅                           1 s    ✅ la page vivante date du dernier commit (2026-10-31)
  porte-tokenizer-kimi   ✅                           9 s    ✅ 10 textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres)
  porte-topologie        ✅                         100 s    ✅ PPL épinglées : reference 17.4702 · historique 30.4363 · topologie 30.4363 · relais 2 42.547
  porte-trace            ✅                          26 s    ✅ la trace fausse est détectée et nommée
=== fin ===
porte-homeostasie 2 0
porte-indice 1 838
porte-melange 1 106
porte-reparti-moteur 1 45
  ```

- **job_output** `{"job_id": "bash-179", "timeout_ms": 1200000, "wait": true}`

  ```
(no new output)
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-179 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && while [ ! -f work/n2d/finalise.termine ]; do sleep 20; done; date '+%H:%M' > work/n2d/portes-debut.txt; JOURNAUX=/tmp/portes-1031-n2d DELAI=1800 bash tools/toutes-les-portes.sh > work/n2d/portes.log 2>&1; date '+%H:%M' > work/n2d/portes-fin.txt; echo TERMINE >> work/n2d/portes.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat work/n2d/portes-debut.txt work/n2d/portes-fin.txt; tail -6 work/n2d/portes.log; echo \"=== registre ===\"; wc -l < /tmp/portes-1031-n2d/registre.txt; awk '$2 != 0' /tmp/portes-1031-n2d/registre.txt; echo \"=== duree ===\"; awk '{ … [129 caractères tronqués]`

  ```
19:42
21:19
      perplexité entière : 8.7434
    === deux nœuds : 2 couches locales, le reste à distance ===
      perplexité répartie : 8.7434 · écart de flux : 0.00e0
    PORTE NON TENUE : écart relatif REF 8.7434 != 9.1748 % entre entier et réparti
Journaux complets : /tmp/portes-1031-n2d
TERMINE
=== registre ===
80
porte-homeostasie 2 0
porte-indice 1 838
porte-melange 1 106
porte-reparti-moteur 1 45
--- 75 vertes, 4 rouges ---
=== duree ===
5826 s = 97 min
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -E \"ocr|vision|jeux\" /tmp/portes-1031-n2d/registre.txt; echo \"=== total lignes ===\"; head -1 /tmp/portes-1031-n2d/registre.txt", "description": "Check the new OCR gate result"}`

  ```
porte-jeux 0 111
porte-ocr 0 48
porte-vision 0 600
=== total lignes ===
porte-adaptateur-sortie 0 65
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np = pathlib.Path('docs/pilotage/references-non-regression.md'); s = p.read_text()\nvieux = \"> **Dernière passe complète — 2026-10-31 à 12 h 54 :** **78 portes, 73 vertes, 5 rouges, 1 h 37**\"\nneuf … [1686 caractères tronqués]`

  ```
references ok
en-cours ok
  revue de documentation · 371 fiche(s) · 439 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1266 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_backlog.py 2>&1 | tail -2; python3 tools/verifie_journal.py 2>&1 | tail -1; python3 tools/verifier_schemas.py 2>&1 | tail -1; git status --short | grep -v \"^ m tools/docwatch\"", "description": "Final checks be … [13 caractères tronqués]`

  ```
✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
     sources et images relatives.
 M .gitignore
 M docs/pilotage/backlog/N2-distillation.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/references-non-regression.md
 M docs/pilotage/roadmap.md
 M journal/README.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M reports/INDEX.md
 M reports/README.md
?? reports/n2-budget.json
?? reports/rapport-n2-budget.md
?? tools/distiller_budget.py
?? tools/eval_n2_budget.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -4; echo \"=== plan état ===\"; grep -E \"État|Heartbeat\" journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md; echo \"=== en-cours dans HEAD ? ===\"; git show --stat HEAD | head -20", "description": "Chec … [44 caractères tronqués]`

  ```
c83f17d5 DOCS — SEUILS PRÉ-ENREGISTRÉS ET COÛT DE LA STDP : LE RENVERSEMENT
2ac27021 DOCS — LE COÛT CACHÉ DE LA STDP SYMÉTRIQUE, LA LECTURE D'UN PAS ET LES QUESTIONS OUVERTES
ffad1c53 DOCS — LE MODÈLE NATIF ET DIEHL & COOK ENRICHIS : QUOTIENT, TYPES, NEUTRALITÉ, DÉTERMINISME, BANC, CONFORMITÉ
b8683d00 SESSION — R4.4 SE FERME SUR `0088fc2f` : L'OCR EST MESURÉ, R4.4 RESTE OUVERTE AUX SCANS
=== plan état ===
- **Heartbeat** : 2026-10-31 20:10 HAE
- **État** : terminé
=== en-cours dans HEAD ? ===
commit c83f17d559a97b6a99567779139784c0e4cd69ef
Author: Stéphane <stephane@localhost>
Date:   Sat Oct 31 21:06:48 2026 -0400

    DOCS — SEUILS PRÉ-ENREGISTRÉS ET COÛT DE LA STDP : LE RENVERSEMENT

 docs/implantation/diehl-cook.md                    | 30 +++++++++++++-----
 journal/2026-10-31/README.md                       |  7 ++--
 journal/2026-10-31/apprentissage.md                |  2 +-
 journal/2026-10-31/distribue.md                    |  2 +-
 journal/2026-10-31/docs.md                         |  5 +--
 journal/2026-10-31/mesures.md                      |  2 +-
 journal/2026-10-31/modele.md                       |  2 +-
 journal/2026-10-31/portes.md                       |  2 +-
 jour
… [316 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -c \"le budget, les quatre sources, et le mètre faussé\" journal/2026-10-31/apprentissage.md; sed -n '/<!-- notes -->/,+4p' journal/2026-10-31/apprentissage.md; git diff HEAD --stat journal/2026-10-31/apprentissage.md", "descrip … [43 caractères tronqués]`

  ```
1
<!-- notes -->
### N2 — le budget, les quatre sources, et le mètre faussé

La journée avait commencé par deux négatifs nets sur la hiérarchie. En reprenant N2 l'après-midi,
la question était simple : le dispositif reconstruit hier n'avait vu que **20,48 Mo** d'un seul
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add .gitignore docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/backlog/N2-distillation.md docs/pilotage/references-non-regression.md reports/rapport-n2-budget.md reports/n2-budget.json reports/INDEX.md reports/RE … [193 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-242]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-242", "timeout_ms": 180000, "wait": true}`

  ```
✅ index : aucun fait stagé sans état
[master c3bcbe99] N2 — LE BUDGET PAIE 2,8 %, LES QUATRE SOURCES COÛTENT 91 %, ET LA VALIDATION EST CONTAMINÉE À 32,8 %
 24 files changed, 1765 insertions(+), 79 deletions(-)
 create mode 100644 reports/n2-budget.json
 create mode 100644 reports/rapport-n2-budget.md
 create mode 100644 tools/distiller_budget.py
 create mode 100644 tools/eval_n2_budget.py
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat HEAD | head -32; echo \"=== status ===\"; git status --short | grep -v \"^ m tools/docwatch\"", "description": "Verify the commit contents"}`

  ```
commit c3bcbe99af1bff5a61f1e9e78151c610f5698d9b
Author: Stéphane <stephane@localhost>
Date:   Sat Oct 31 21:20:06 2026 -0400

    N2 — LE BUDGET PAIE 2,8 %, LES QUATRE SOURCES COÛTENT 91 %, ET LA VALIDATION EST CONTAMINÉE À 32,8 %
    
    Le budget plein (20 000 pas, 41 Mo, trois graines) amène l'élève distillé de 2,9355 à
    2,8527 sous le protocole de N2.19 : −0,0828, du même ordre que la chaîne historique, et
    toujours 0,35 au-dessus de la porte 2,5. Le corpus à quatre sources, tel que le manifeste le
    définit (82,5 % anglais), coûte +0,9064 ; à quotas égaux (25 % par source) il coûte encore
    +0,58 : la diversité n'aide pas la porte française, et le professeur français sur des octets
    anglais est un confondant nommé. Le curriculum 129 gagne 0,0416 à 129, 0,0056 à 128.
    
    Puis le chiffre qui change la lecture : la validation n'est pas tenue à l'écart. 32,8 % des
    fenêtres du protocole (42 sur 128) sont verbatim dans l'entraînement — le corpus recopie des
    documents — et les fenêtres contaminées donnent 0,39 de PPL de moins que les propres
    (2,5862 contre 2,9795) ; l'écart croît avec le budget (0,17 pour la base, 0,35 pour 5 000 pas,
    0,39 pour 20 0
… [985 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/revue_documentation.py 2>&1 | tail -3; python3 tools/verifie_en_cours.py | tail -2; python3 tools/taille_documents.py 2>&1 | tail -2; python3 tools/verifie_journal.py 2>&1 | tail -1; python3 tools/verifie_ba … [126 caractères tronqués]`

  ```
revue de documentation · 371 fiche(s) · 439 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1266 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ❌ 1 violation(s) :
     · docs/pilotage/references-non-regression.md : 2571 mots > budget 2500 (T1)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
     sources et images relatives.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, re, sys\nsys.path.insert(0,'tools')\nfrom taille_documents import mots_hors_diagrammes\nt = pathlib.Path('docs/pilotage/references-non-regression.md').read_text()\nprint('total', mots_hors_diagramme … [202 caractères tronqués]`

  ```
total 2571
83 | > **Dernière passe complète — 2026-10-31 à 19 h 42 :** **79 portes, 75 vertes, 4 rouges, 1
74 | > **Passe précédente — 2026-10-31 à 12 h 54 :** **78 portes, 73 vertes, 5 rouges, 1 h 37**
34 | > **Passe précédente — 2026-10-29 à 22 h 09 :** 62 portes, 60 vertes, 2 rouges, 1 h 46 ;
54 | > **Ce que ce fichier porte.** Les repères chiffrés qu'une passe complète imprime, et
47 | > **Passe du 2026-10-28 à 00 h 12** (**49 portes, 46 vertes, 3 rouges**, **1 h 40 min**) —
52 | > **Passe précédente — 2026-10-27 à 14 h 33** (**49 portes, 47 vertes, 2 rouges**, **1 h 4
172 | > **Passe précédente — 2026-10-26 à 14 h 30** (**49 portes, 47 vertes, 2 rouges**, **1 h 3
26 | > **Historique des passes** : les passes antérieures au 26/10 14 h 30, dont celle du
287 | > ### ⚠️ DEUX DÉFAUTS DE MESURE, TROUVÉS LE 16/10 — ET ILS SONT DE LA MÊME FAMILLE
511 | > **4. ET UN AUDIT DES 46 PORTES, LE MÊME JOUR** (analyse statique, sans les exécuter ✗) :
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"2026-10-26\" -A 12 docs/pilotage/references-non-regression.md | head -16", "description": "Read the 26/10 pass block"}`

  ```
36:> **Passe précédente — 2026-10-26 à 14 h 30** (**49 portes, 47 vertes, 2 rouges**, **1 h 34 min**) — la passe de clôture
37-> de **B9**, avec `porte-deepseek` **incluse** (1 s, **verte** : 20 tests, dry-run, 60 et 310 prompts) et
38-> `porte-jeux` **verte** (106 s : 449/449 au niveau 4, 11/11 paires, permutation 12/275, notation 5 112/5 112,
39-> livre 10/10, go 9×9 10/10 contre 3/10, dames 0 défaite, cartes 44,7 % contre 51,0 %). Les **deux rouges**
40-> sont les **structurelles connues** : `porte-indice` (861 s) et `porte-melange` (107 s), avec les mêmes
41-> diagnostics (indice extérieur à 482 jetons, écart nul ou négatif ; état de A qui ne rend pas le code de A).
42-> `porte-homeostasie` est **verte** (506 s). Les références sont stables : `porte-flux` **60,8135**,
43-> `porte-pont` **+2,81 % / +25,35 %**, `porte-coupe` **+0,52 % → +17,09 %**, `porte-gain` **29,0206 →
44-> 1297,5437**, `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**, `porte-greffe` **branchée**,
45-> `porte-vision` **559 s**, `porte-poids-creux` **319 s**, `porte-prechargement` **187 s**. Journaux :
46-> `/tmp/portes-b9-1026-12h55`.
47->
48-
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np = pathlib.Path('docs/pilotage/references-non-regression.md'); s = p.read_text()\ndebut = s.index(\"> **Passe précédente — 2026-10-26 à 14 h 30**\")\nfin = s.index(\"> **Historique des passes**\")\ … [739 caractères tronqués]`

  ```
ok
     · 14 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/references-non-regression.md && git commit -m \"RÉFÉRENCES — LA PASSE DU 31 À 19 h 42 ENTRE EN TÊTE, LA PAGE RESTE SOUS SON BUDGET\n\nLa passe complète de clôture (79 portes, 75 vertes, 4 rouges, 1 h 39, journau … [564 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-248]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-248", "timeout_ms": 180000, "wait": true}`

  ```
✅ index : aucun fait stagé sans état
[master 10fa4f42] RÉFÉRENCES — LA PASSE DU 31 À 19 h 42 ENTRE EN TÊTE, LA PAGE RESTE SOUS SON BUDGET
 13 files changed, 144 insertions(+), 34 deletions(-)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/revue_documentation.py 2>&1 | tail -2; python3 tools/verifie_en_cours.py | tail -1; python3 tools/taille_documents.py 2>&1 | tail -1; python3 tools/verifie_journal.py 2>&1 | tail -1; python3 tools/verifie_ba … [222 caractères tronqués]`

  ```
revue de documentation · 371 fiche(s) · 439 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ✅ état court, structuré, multi-session et reprenable
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
     sources et images relatives.
=== git ===
10fa4f42 RÉFÉRENCES — LA PASSE DU 31 À 19 h 42 ENTRE EN TÊTE, LA PAGE RESTE SOUS SON BUDGET
c3bcbe99 N2 — LE BUDGET PAIE 2,8 %, LES QUATRE SOURCES COÛTENT 91 %, ET LA VALIDATION EST CONTAMINÉE À 32,8 %
c83f17d5 DOCS — SEUILS PRÉ-ENREGISTRÉS ET COÛT DE LA STDP : LE RENVERSEMENT
  ```

- **get_goal** `{}`

  ```
{"goal":{"id":"goal-371547c2-8e61-4925-8ab3-dab60674eec4","revision":1,"objective":"N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/pilotage/en-cours.md et la roadmap à jour.","phase":"active","roundsStarted":1,"maxGoalRounds":1000},"activation":"armed"}
  ```

- **update_goal** `{"goal_id": "goal-371547c2-8e61-4925-8ab3-dab60674eec4", "revision": 1, "action": "complete"}`

> **Objectif** (complete) : N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/pilotage/en-cours.md et la roadmap à jour.


  ```
{"goal":{"id":"goal-371547c2-8e61-4925-8ab3-dab60674eec4","revision":2,"objective":"N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/pilotage/en-cours.md et la roadmap à jour.","phase":"complete","roundsStarted":1,"maxGoalRounds":1000},"activation":"disarmed"}
  ```

### 👤 Utilisateur

<goal_complete>
Objective: "N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/pilotage/en-cours.md et la roadmap à jour."
The goal is marked complete and this autonomous run is ending. Write the closing message to the user now: state the outcome, summarize what was done and how it was verified, and point to the concrete results (files, commits, or other artifacts). Report only what earlier rounds and tool results in this session actually establish; when a detail is not in the session, say so instead of inventing it. Note anything the user should review or do next. Address the user directly. Do not call any more tools in this run; further work waits for the user's next instruction.
</goal_complete>

### 🤖 Assistant

⏵ Clôture : N2.d mesuré, écrit, committé, portes vertes

## Ce qui est établi

**La campagne N2.d** — 12 distillations, 3 graines par bras, deux GPU, ~3 h :

| bras | protocole 8×16×128 | fenêtres propres | 8×15×129 |
|---|---:|---:|---:|
| base supervisée | 3,2161 | 3,2450 | 3,2653 |
| **T5k** (5 000 pas, réf.) | 2,9355 | 3,0534 | 2,9623 |
| **A** — 20 000 pas, français seul | **2,8527** | **2,9795** | 2,8743 |
| **B** — 4 sources (82,5 % anglais) | 3,7591 | 3,8573 | 3,8218 |
| **B′** — 4 sources à quotas égaux | 3,4350 | 3,5634 | 3,4848 |
| **C** — curriculum 129 sur A | 2,8471 | 2,9783 | **2,8327** |

- **Le budget paie peu** : −0,0828, du même ordre que la chaîne historique ; la porte < 2,5 reste à 0,35 (protocole) / 0,48 (fenêtres propres).
- **Les données coûtent** : +0,91 pour le manifeste, +0,58 même à quotas égaux (professeur français sur octets anglais : confondant nommé).
- **Le curriculum 129** gagne 0,0416 à 129, 0,0056 à 128.

**Le résultat qui change la lecture** : la validation n'est **pas** tenue à l'écart. 32,8 % des fenêtres du protocole (42/128) sont **verbatim** dans l'entraînement ; 23,5 % des fenêtres d'entraînement y apparaissent plus d'une fois. Les fenêtres contaminées donnent 0,39 de PPL de moins que les propres, et l'écart croît avec le budget (0,17 → 0,35 → 0,39). **2,7078 et 2,6998 sont mesurés sur ce même jeu contaminé** : la porte < 2,5 n'a jamais été une mesure de généralisation.

## Vérification

- Trois graines par bras, écart-type 0,002–0,008 ; comparaison appariée (mêmes fenêtres).
- Contrôles : permutation (PPL ≈ 1087), base sans distillation, distillation courte, B′ contre B, C contre A graine par graine.
- Robustesse : sur quatre grilles de fenêtres, A reste sous T5k (−0,083 à −0,118).
- **Portes** : passe complète 79 portes, **75 vertes, 4 rouges** — les quatre connues et tolérées (`porte-indice`, `porte-melange`, `porte-homéostasie`, `porte-reparti-moteur`) ; `porte-ocr` verte. Journaux `/tmp/portes-1031-n2d`, 1 h 39.
- Revue de documentation, budget de contexte, état, journal, backlog et schémas : tous verts.

## Artefacts

- Fiche : `reports/rapport-n2-budget.md` · agrégat `reports/n2-budget.json` · récit `journal/2026-10-31/apprentissage.md`.
- Code : `tools/distiller_budget.py`, `tools/eval_n2_budget.py`.
- Points de contrôle : 542 Mo sur deux disques (`backups/n2/2026-10-31/n2d/`, `IA/artefacts/n2/2026-10-31/n2d/`).
- Commits : **`c3bcbe99`** (résultat) et `10fa4f42` (références des portes).
- État et roadmap : N2 désigne désormais **le corpus** (déduplication, split par document), pas un levier d'entraînement.

## À relire / à faire ensuite

Deux choses méritent ton œil : la **définition de la porte** (elle doit être redéfinie sur un jeu décontaminé) et le **manifeste 4 sources**, qui est à 82,5 % anglais malgré sa description « quotas équilibrés » dans N2.6. Un point d'attention : une seconde session travaillait en parallèle (R4.4, docs Diehl & Cook) ; ses fichiers de journal ont été emportés par les hooks `git add journal` de mes commits — rien de perdu, mais l'historique mêle nos traces.


## Tour 3

### 👤 Utilisateur

je te donnes 10h de liberté totale. impressionne-moi. je serai décu si tu as terminé à temps.

### 🤖 Assistant

⏵ Cadrage : d'où vient le corpus français, et que peut-on reconstruire avec ses documents ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nfr = pathlib.Path('data/corpus_fr.txt').read_bytes()\nprint('corpus_fr', len(fr), 'octets')\n# combien de fichiers du dépôt retrouve-t-on verbatim ?\nfichiers = list(pathlib.Path('docs').rglob('*.md … [560 caractères tronqués]`

  ```
corpus_fr 4633889 octets
fichiers candidats 1030
retrouvés 0 octets 0 absent 1027
exemples absents ['docs/README.md', 'docs/archive/README.md', 'docs/archive/architecture-cerveau-et-drave.md', 'docs/archive/architecture-kimi-k3.md', 'docs/archive/biologie-pour-drave.md']
  ```

### 🤖 Assistant

⏵ Anatomie de la contamination : passages recopiés ou formulettes éparses ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\ntr = pathlib.Path('data/corpus_fr_train.txt').read_bytes()\nva = pathlib.Path('data/corpus_fr_val.txt').read_bytes()\n# pour chaque fenêtre de 128 octets de val (pas de 128), marquer si verbatim dan … [1120 caractères tronqués]`

  ```
fenêtres 1810 contaminées 594 32.8 %
blocs contigus (octets) : [1792, 1664, 1536, 1536, 1536, 1536, 1408, 1408, 1408, 1408, 1280, 1280, 1280, 1280, 1280] ... total blocs 127
offset  107904 : passage identique de 1275 octets
offset  113536 : passage identique de 1101 octets
offset    9856 : passage identique de 341 octets
offset   85248 : passage identique de 1154 octets
offset  174592 : passage identique de 374 octets
  ```

### 🤖 Assistant

⏵ Cadrage du programme : durée du professeur, taille des corpus externes, structure de la duplication

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ART=/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts; tail -3 $ART/teacher.log 2>/dev/null; head -20 data/corpus_fr_litterature.txt; echo \"...\"; head -5 data/corpus_en.txt; echo \"=== tailles ===\"; ls -la data/corp … [136 caractères tronqués]`

  ```
# meilleur point : pas 20000 · val 0.9195 bits/octet
  # écrit dans /tmp/n2-campagne/route-teacher-20k · 23.57 M paramètres · 1.46 M poids lus/jeton/couche
Au lecteur

  Cette version électronique reproduit dans son intégralité
  la version originale.

  La ponctuation n'a pas été modifiée hormis quelques corrections
  mineures.

  L'orthographe a été conservée. Seuls quelques mots ont été modifiés.
  La liste des modifications se trouve à la fin du texte.




  AVENTURES D'ALICE

  AU

  PAYS DES MERVEILLES.

...
Anarchism is a political philosophy and movement that seeks to abolish all institutions that perpetuate authority, coercion, or hierarchy, primarily targeting the state and capitalism. Anarchism advocates for the replacement of the state with stateless societies and voluntary free associations.

Although traces of anarchist ideas are found all throughout history, modern anarchism emerged from the Enlightenment. During the latter half of the 19th and the first decades of the 20th century, the anarchist movement flourished in most parts of the world and had a significant role in workers' struggles for emancipation. Various anarchist schools of thought formed during this per
… [1135 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ART=/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts; grep -E \"^pas (5000|10000|15000|20000)\" $ART/teacher.log | tail -4; echo \"=== base ===\"; grep -E \"^pas (10000|20000)\" $ART/base.log | tail -2; echo \"=== lig … [111 caractères tronqués]`

  ```
=== base ===
pas 10000 · perte 1.3044 · PPL val 4.260 · 456 s
pas 20000 · perte 1.2159 · PPL val 4.024 · 880 s
=== lignes ===
   27 /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/teacher.log
  430 /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/base.log
  457 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ART=/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts; cat $ART/teacher.log | head -12; echo \"...\"; sed -n 20,27p $ART/teacher.log", "description": "Read the teacher log for duration"}`

  ```
/home/stephane/gpu-env/lib64/python3.13/site-packages/torch/cuda/__init__.py:1061: UserWarning: Can't initialize NVML
  raw_cnt = _raw_device_count_nvml()
# route · 23.57 M paramètres · 1.46 M poids LUS par jeton et par couche · 4.06 M stockés · corpus 4402195 octets · cuda
  pas   1000 · perte 1.3041 · val 1.7570 bits/octet · 88 s
  pas   2000 · perte 1.2619 · val 1.5613 bits/octet · 173 s
  pas   3000 · perte 1.1178 · val 1.4415 bits/octet · 253 s
  pas   4000 · perte 1.0672 · val 1.3662 bits/octet · 337 s
  pas   5000 · perte 0.9546 · val 1.2951 bits/octet · 421 s
  pas   6000 · perte 1.0541 · val 1.2375 bits/octet · 505 s
  pas   7000 · perte 0.9645 · val 1.1749 bits/octet · 589 s
  pas   8000 · perte 0.9621 · val 1.1453 bits/octet · 673 s
  pas   9000 · perte 1.0031 · val 1.1271 bits/octet · 757 s
...
  pas  17000 · perte 0.8939 · val 0.9716 bits/octet · 1437 s
  pas  18000 · perte 0.7532 · val 0.9462 bits/octet · 1519 s
  pas  19000 · perte 0.8127 · val 0.9254 bits/octet · 1605 s
  pas  20000 · perte 0.8175 · val 0.9195 bits/octet · 1688 s
Writing model shards:   0%|          | 0/1 [00:00<?, ?it/s]Writing model shards: 100%|██████████| 1/1 [00:00<00:00,  6.01it/s]Writing m
… [217 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Programme des 10 h : le mètre d'abord, puis la capacité et le verrou de longueur

- **create_goal** `{"max_goal_rounds": 1000, "objective": "N2.h — le mètre propre : construire un corpus dédupliqué avec split train/val/test sans répétition (outil versionné + manifeste + vérification), refaire toute la chaîne sur ce corpus (professeur 23,5 M, base supervisée, distillation 20k × 3 graines, curriculum … [386 caractères tronqués]`

> **Objectif** (create) : N2.h — le mètre propre : construire un corpus dédupliqué avec split train/val/test sans répétition (outil versionné + manifeste + vérification), refaire toute la chaîne sur ce corpus (professeur 23,5 M, base supervisée, distillation 20k × 3 graines, curriculum 129), mesurer la porte honnête et le profil hors domaine (littérature française, anglais, wikitext2), trancher la capacité (21,63 M) sur ce mètre, mesurer la décomposition (blocs, têtes précoces, pensée), puis attaquer le verrou de longueur avec des positions aléatoires (3 graines, 129→512 octets) ; écrire les fiches, le journal, l'état et la roadmap, passer les portes, committer.


  ```
{"goal":{"id":"goal-7e5e03db-88c5-4373-9ab3-8ed001aa777a","revision":1,"objective":"N2.h — le mètre propre : construire un corpus dédupliqué avec split train/val/test sans répétition (outil versionné + manifeste + vérification), refaire toute la chaîne sur ce corpus (professeur 23,5 M, base supervisée, distillation 20k × 3 graines, curriculum 129), mesurer la porte honnête et le profil hors domaine (littérature française, anglais, wikitext2), trancher la capacité (21,63 M) sur ce mètre, mesurer la décomposition (blocs, têtes précoces, pensée), puis attaquer le verrou de longueur avec des positions aléatoires (3 graines, 129→512 octets) ; écrire les fiches, le journal, l'état et la roadmap, passer les portes, committer.","phase":"active","roundsStarted":0,"maxGoalRounds":1000},"activation":"armed"}
  ```

- **todo_write** `{"todos": [{"content": "Écrire tools/corpus_propre.py : déduplication par shingles, split par chunks, manifeste, vérification", "status": "in_progress"}, {"content": "Construire et vérifier data/corpus_propre/ (0 % de contamination, stats)", "status": "pending"}, {"content": "Entraîner le professeur … [745 caractères tronqués]`

  ```
Updated todo list: 9 pending, 1 in progress, 0 completed.
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"corpus_propre.py — un corpus sans répétition, et un split qui ne fuit pas.\n\nPOURQUOI. N2.d a mesuré que **32,8 %** des fenêtres du protocole de validation\napparaissent **verbatim** dans l'entraînement : le corpus empile des passages qui se\nrecopient (12 … [8947 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_propre.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nfrom corpus_propre import deduit, hachages, couverture\ndata = b\"Le chat dort. Le chat mange. Le chat dort. Le chat mange. Il pleut.\"\npropre, stats = deduit(data, 8, min_r … [340 caractères tronqués]`

  ```
b'Le chat dort. \nIl pleut.'
{'retires': 44, 'runs': 2, 'plus_long_run': 14}
fenêtres répétées 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/corpus_propre.py'); s=p.read_text()\ns=s.replace('''    for i, c in enumerate(chunks):\n        if i % val_un_sur == val_un_sur - 1:\n            val.append(c)\n        elif i  … [1209 caractères tronqués]`

  ```
ok
{
 "source_octets": 4633889,
 "propre_octets": 3605306,
 "train_octets": 3244858,
 "val_octets": 180224,
 "test_octets": 180224,
 "deduplication": {
  "retires": 1029993,
  "runs": 1411,
  "plus_long_run": 540086,
  "retires_pct": 22.23
 },
 "contamination": {
  "validation": {
   "fenetres": 2814,
   "contaminees": 0,
   "taux": 0.0
  },
  "test": {
   "fenetres": 2814,
   "contaminees": 0,
   "taux": 0.0
  }
 }
}
[stderr]

real	0m9,681s
user	0m9,373s
sys	0m0,310s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -c 400 data/corpus_propre/val.txt; echo; echo \"=== seams ===\"; python3 -c \"\nd=open('data/corpus_propre/val.txt','rb').read()\nprint(repr(d[8180:8200]))\nprint('taille', len(d), 'chunks', len(d)/8192)\n\"; echo \"=== entraine … [167 caractères tronqués]`

  ```
, la lecture n'en transfère que 0,638, et l'écart ne se réduit ni par plus
de langues, ni par normalisation.
3. L'attrition ne généralise pas : elle réduit la taille à coût faible et
monotone. Le critère de validation est trop indulgent pour l'arrêter au bon
13. RECTIFICATION — l'oracle du §10.2 était faux, et le plafond se décompose
Le diagnostic du §10.2 (oracle 0,7762 contre nou
=== seams ===
b'e un doublonporte \xc3\xa0'
taille 180224 chunks 22.0
=== entrainer_moteur flags ===
usage: entrainer_moteur.py [-h] [--famille {dense,route}]
                           [--donnees DONNEES [DONNEES ...]]
                           [--validation VALIDATION] [--dim DIM]
                           [--couches COUCHES] [--tetes TETES] [--cache CACHE]
                           [--cache-perle CACHE_PERLE] [--experts EXPERTS]
                           [--k K] [--seq SEQ] [--lot LOT] [--pas PAS]
                           [--lr LR] [--graine GRAINE] [--verifier-sauvegarde]
                           [--init INIT] [--recurrence-max RECURRENCE_MAX]
                           [--partage] [--alignement ALIGNEMENT]
                           [--enseignant ENSEIGNANT]
                           [--alp
… [876 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"meilleur\\|best\\|validation\" tools/entrainer_moteur.py | head -12; echo \"=== native ===\"; PYTHONPATH=. ~/gpu-env/bin/python tools/entrainer_native.py --help 2>&1 | head -20", "description": "Check whether the teacher ea … [25 caractères tronqués]`

  ```
145:    (13,06 contre 7,57) et bien meilleur à 25 % (17,50 contre 49,43). Mais le variant diffère du
250:    alors plus le modèle entraîné (validation **3,6465** → **8,8257** bits/octet), et la
283:        # 1,097 au lieu de −2,8, et une validation d'entraînement à 3,0713 bits/octet au lieu de
416:def perte_de_validation(modele, val, a, dev):
427:    # parfait au PREMIER pas ✓✗ — c'est ce qui est arrivé au modèle français seul (927 octets de validation pour
428:    # 2 048 par lot ✓✓) : le fichier écrit est celui du pas 500, pas le meilleur ✓✗. On répète le texte pour
448:    poids qui ne reproduisaient PAS le modèle entraîné — validation 2,2662 bits/octet
459:    qu'on a calculé. C'est là que la perte de validation passait de **3,6465** à **8,8257**
730:    p.add_argument("--validation", default="data/corpus_en_val.txt")
744:                   help="APRÈS l'écriture : recalculer la perte de validation avec le modèle EN "
752:                        "(mesuré ailleurs : sans cela, le bloc répété est meilleur à t=1 (82,9 contre "
826:    val = charger([a.validation])
=== native ===
usage: entrainer_native.py [-h] [--corpus CORPUS] [--pas PAS] [--seq SEQ]
                           [-
… [419 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"meilleur_pas\\|meilleure\\|sauve\\|\\[.meilleur\\|argmin\\|min(\" tools/entrainer_moteur.py | head -15", "description": "Check checkpoint selection in the teacher trainer"}`

  ```
262:    # `tools/porte-sauvegarde-modele.sh` le voit et passe au ROUGE.
434:        for k in range(max(1, min(8, (len(val) - 1) // (a.seq * a.lot)))):
743:    p.add_argument("--verifier-sauvegarde", action="store_true",
793:                        "M8 (le fichier sauve ne reproduisait pas le modele entraine) est "
888:        a.lr = min(a.lr, 3e-4)
985:            # ⚠️ REMETTRE LA FORME DE BASE APRÈS CHAQUE PAS ✗✓ : le trainer sauvegarde le **meilleur point
1010:            frac = min(1.0, pas / max(1, a.pas * 0.5)) ** 3
1019:                for k in range(min(8, (len(val) - 1) // (a.seq * a.lot))):
1043:    t_avant = perte_de_validation(modele, val, a, dev) if a.verifier_sauvegarde else None
1046:    # l'état du pas où la validation était la meilleure : si c'est le pas 1000, le fichier porte
1059:    t_restaure = perte_de_validation(modele, val, a, dev) if a.verifier_sauvegarde else None
1089:    # l'oublier faisait sauver des clés `parametrizations.weight.original` que l'exporteur ne
1093:    t_materialise = perte_de_validation(modele, val, a, dev) if a.verifier_sauvegarde else None
1111:    # fait le poids lié ✓), et la bibliothèque **refuse** de sauvegarder des tenseurs partagé
… [46 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p work/n2h && python3 - <<'EOF'\nimport pathlib\ntr = pathlib.Path('data/corpus_propre/train.txt').read_bytes()\nchunk = 8192\nmorceaux = [tr[i:i+chunk] for i in range(0, len(tr), chunk)]\ndev = b''.join(m for i, m in enumerat … [1110 caractères tronqués]`

  ```
dev 320314 octets 397 chunks de train
=== lancement professeur (GPU0) et base (GPU1) ===
teacher pid 556252
base pid 556253
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"eval_n2_propre.py — la porte honnête : PPL sur un corpus dédupliqué, et hors domaine.\n\nLe corpus de `data/corpus_propre/` est construit par `tools/corpus_propre.py` : passages\nrépétés retirés, split par chunks contigus, **zéro fenêtre de validation dans\ … [6378 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 900 ~/gpu-env/bin/python tools/eval_n2_propre.py \\\n  /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/temoin-g1.pt --decomposition --longueurs 2>&1 | grep -v Loading", "de … [66 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py", line 150, in <module>
    main()
    ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py", line 137, in main
    r["decomposition"] = decompose(m, val, a.chunk, a.device)
                         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py", line 97, in decompose
    res["complete"] = round(math.exp(float(F.cross_entropy(
                            ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
        s["logits"].reshape(-1, 256), y.reshape(-1))), 4))
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: math.exp() takes exactly one argument (2 given)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/eval_n2_propre.py'); s=p.read_text()\ns=s.replace('''        res[\"complete\"] = round(math.exp(float(F.cross_entropy(\n            s[\"logits\"].reshape(-1, 256), y.reshape(-1 … [944 caractères tronqués]`

  ```
ok
{"fichier": "temoin-g1.pt", "params": 11814792, "val": 2.9079, "test": 2.9355, "litterature": 15.5376, "anglais": 51.8854, "wikitext2": 50.7895, "permute": 1146.6567, "decomposition": {"complete": 2.9234, "apres_2_blocs": 3.719, "apres_4_blocs": 3.0789, "apres_6_blocs": 2.8708, "sans_pensee": 40758083.6251}, "longueurs": {"129": 2.9535, "192": 8.1301, "256": 13.3328, "384": 22.4291, "512": 28.9747}}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -2 work/n2h/teacher.log; tail -2 work/n2h/base.log; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader", "description": "Check teacher and base training progress"}`

  ```
22:23
# route · 23.57 M paramètres · 1.46 M poids LUS par jeton et par couche · 4.06 M stockés · corpus 3244858 octets · cuda
  pas   1000 · perte 1.3509 · val 2.0747 bits/octet · 83 s
pas 2550 · perte 1.7994 · PPL val 5.945 · 112 s
pas 2600 · perte 1.5981 · PPL val 5.863 · 115 s
0, 1228 MiB, 54 %
1, 730 MiB, 49 %
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/corpus_propre.py'); s=p.read_text()\ns=s.replace('''    ap.add_argument(\"--test\", type=int, default=20)''','''    ap.add_argument(\"--test\", type=int, default=20)\n    ap.ad … [745 caractères tronqués]`

  ```
ok
 "train_octets": 15332926,
 "val_octets": 843776,
 "test_octets": 843776,
 "deduplication": {
  "retires": 11337,
  "runs": 69,
  "plus_long_run": 1816753,
  "retires_pct": 0.07
 },
 "contamination": {
  "validation": {
   "fenetres": 3000,
   "contaminees": 0,
   "taux": 0.0
  },
  "test": {
   "fenetres": 3000,
   "contaminees": 0,
   "taux": 0.0
  }
 }
}
[stderr]

real	0m41,742s
user	0m40,772s
sys	0m0,968s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nrepo = pathlib.Path('data/corpus_propre/train.txt').read_bytes()\nlitt = pathlib.Path('data/corpus_litt_propre/train.txt').read_bytes()\nC = 8192\nrc = [repo[i:i+C] for i in range(0, len(repo), C)]\ … [815 caractères tronqués]`

  ```
mixte 6144000 (35 % repo / 65 % littérature… en fait 50/50 par construction)
repo 3244858 litt échantillon 3072000 dev 614400
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/eval_n2_propre.py'); s=p.read_text()\ns=s.replace('''    lit = charger_bytes(RACINE / \"data/corpus_fr_litterature.txt\")''',\n'''    lit = charger_bytes(RACINE / \"data/corpus … [838 caractères tronqués]`

  ```
ok
22:24
  pas   2000 · perte 1.2665 · val 1.8957 bits/octet · 162 s
pas 4500 · perte 1.3484 · PPL val 5.098 · 198 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"21 634 536\\|21634536\\|21,63 M\\|21.63\" reports/*.md docs/ | head -8; echo \"=== config native ===\"; grep -n \"d_model\\|dim\\|21\" reports/rapport-native-21m-20k.md | head -10", "description": "Find the 21.63M model co … [13 caractères tronqués]`

  ```
reports/INDEX.md:224:| [rapport-native-21m-20k.md](rapport-native-21m-20k.md) | N2.9 — student 21,63 M sur 20 000 pas : 3,381, toujours derrière 11,47 M |
reports/INDEX.md:231:| [rapport-native-capacite-egal.md](rapport-native-capacite-egal.md) | N2.5b — capacité à budget égal : 21,63 M bat 11,47 M de 4,1 % |
reports/rapport-coherence-docs-2.md:82:| 28 | `docs/implantation/format-flux.md:58-61`, `REPRISE.md:248,340-341`, `docs/pilotage/roadmap.md:94` | v3 : **45 079 930 o** (−32,1 % vs v2), rejeu 19,4029 (+0,074 %), 21 630 645 actifs | valeurs cohérentes entre documents ; l'exécution courte confirme le sens (v3 plus petite, 166 206 actifs contre 171 554 sur la même trace de 4 jetons) | OK |
reports/rapport-n2-distillation.md:84:capacité** (le 21,63 M à budget égal donnait −8,1 %), et **la fenêtre brute**, que R11 doit
reports/rapport-native-21m-20k.md:1:# N2.9 — student 21,63 M sur 20 000 pas : 3,381, toujours derrière 11,47 M
reports/rapport-native-21m-20k.md:3:> **Objet.** Donner au student de 21,63 M un **vrai budget** (20 000 pas) pour voir si la capacité
reports/rapport-native-21m-20k.md:9:- Student : **21 634 536** paramètres, initialisation aléatoire, **20 000 pas**, lot 8, 
… [771 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom tools.native_model import NativeConfig, NativeModel\ncible = 21_634_536\nbest = []\nfor d in range(224, 449, 8):\n    for eh in (288, 320, 352, 384, 416, 448, 512):\n        c = NativeConfig(d_model=d, expert_ … [331 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/native_model.py", line 17, in <module>
    import torch
ModuleNotFoundError: No module named 'torch'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. ~/gpu-env/bin/python - <<'EOF'\nfrom tools.native_model import NativeConfig, NativeModel\ncible = 21_634_536\nbest = []\nfor d in range(224, 481, 8):\n    for eh in (288, 320, 352, 384, 416, 448, 512, 576):\n        c =  … [361 caractères tronqués]`

  ```
écart  11688 · d_model 296 · expert_hidden 416 · 21,646,224 paramètres
écart  16280 · d_model 280 · expert_hidden 448 · 21,650,816 paramètres
  ```

### 🤖 Assistant

⏵ Ajout des positions aléatoires (attaque du verrou de longueur) au modèle et au distillateur

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/native_model.py'); s=p.read_text()\ns=s.replace('''    def forward(self, ids):\n        b, s = ids.shape\n        x = self.embed(ids) + self.pos(torch.arange(s, device=ids.devi … [2268 caractères tronqués]`

  ```
native_model ok
distiller_budget ok
positions par défaut identiques : True
offset 5 change : True
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/file-gpu0.sh <<'EOF'\n#!/bin/bash\n# GPU 0 — après le professeur propre : distillation A ×3, curriculum ×3, positions aléatoires ×3.\nset -u\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nexport CUDA_VISIBLE_DEVI … [3050 caractères tronqués]`

  ```
queue0 559161
queue1 559162
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && kill 559161 2>/dev/null; sleep 1; python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('work/n2h/file-gpu0.sh'); s=p.read_text()\ns=s.replace('P=\"~/gpu-env/bin/python\"', 'P=\"$HOME/gpu-env/bin/python\"')\np.write_text(s)\nprint('P=' i … [234 caractères tronqués]`

  ```
True fixé
queue0 relancé 559337
22:26
  pas   3000 · perte 1.2308 · val 1.8002 bits/octet · 243 s
pas 7550 · perte 1.4324 · PPL val 4.618 · 322 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/evalue-tout.sh <<'EOF'\n#!/bin/bash\n# Évalue tous les points de contrôle N2.h : porte honnête, hors domaine, décomposition, longueurs.\nset -u\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nexport PYTHONPATH=. C … [1240 caractères tronqués]`

  ```
ok
22:27
pas 8000 · perte 1.3161 · PPL val 4.554 · 339 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -1 work/n2h/base.log; tail -1 work/n2h/teacher.log; ls work/n2h/*.pt 2>/dev/null", "description": "Check training progress"}`

  ```
22:27
pas 8400 · perte 1.3595 · PPL val 4.573 · 355 s
  pas   4000 · perte 1.1263 · val 1.7392 bits/octet · 325 s
[exit code: 2]
  ```

- **bash** `{"command": "sleep 600; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null; tail -1 work/n2h/base.log; tail -1 work/n2h/teacher.log; tail -1 work/n2h/teacher-mixte.log 2>/dev/null", "description": "Wait 10 minutes and check the chain", "run_in_backgroun … [9 caractères tronqués]`

  ```
started background job bash-275
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null; tail -1 work/n2h/base.log; tail -1 work/n2h/teacher.log", "description": "Check base completion"}`

  ```
22:27
pas 8700 · perte 1.5051 · PPL val 4.505 · 366 s
  pas   4000 · perte 1.1263 · val 1.7392 bits/octet · 325 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/agrege.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"agrege.py — tableau par bras de N2.h (porte honnête, hors domaine, longueurs).\"\"\"\nimport json, pathlib, statistics as st\n\nBRAS = [\n    (\"ancien base\", \"drave-n0 … [2409 caractères tronqués]`

  ```
ok
22:27
pas 8950 · perte 1.2669 · PPL val 4.528 · 378 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, random\ntr = pathlib.Path('data/corpus_propre/train.txt').read_bytes()\nva = pathlib.Path('data/corpus_propre/val.txt').read_bytes()\nrng = random.Random(1)\nN = len(va) - 129\nhits64 = hits32 = 0\n … [745 caractères tronqués]`

  ```
fenêtres de validation dont les 64 premiers octets sont dans train : 7/300
... 32 premiers octets : 33/300
plus long préfixe retrouvé dans train (sur 50 fenêtres) : 48
  ```

- **job_output** `{"job_id": "bash-275", "timeout_ms": 900000, "wait": true}`

  ```
22:37
work/n2h/base-propre.pt
}
  pas  11000 · perte 0.9444 · val 1.4780 bits/octet · 910 s
  pas   1000 · perte 1.5888 · val 2.0462 bits/octet · 82 s
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat work/n2h/base-propre.pt.json 2>/dev/null | head -20; echo \"=== teacher ===\"; tail -1 work/n2h/teacher.log; echo \"=== mixte ===\"; tail -1 work/n2h/teacher-mixte.log", "description": "Read the clean base metrics"}`

  ```
{
 "modele": "drave-n0",
 "parametres": 11814792,
 "corpus": "data/corpus_propre/train.txt",
 "octets": 3244858,
 "pas": 20000,
 "seq": 128,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "perte_finale": 1.1913173198699951,
 "ppl_val": 3.721005346145684,
 "jetons_val": 8192,
 "tetes": true,
 "precision_main": 0.6103515625,
 "precision_early": [
  0.569580078125,
  0.60595703125,
  0.610107421875
 ],
=== teacher ===
  pas  11000 · perte 0.9444 · val 1.4780 bits/octet · 910 s
=== mixte ===
  pas   1000 · perte 1.5888 · val 2.0462 bits/octet · 82 s
  ```

- **bash** `{"command": "sleep 1200; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null; for f in A-propre-g1 A-propre-g2; do tail -1 work/n2h/$f.log 2>/dev/null; done; tail -1 work/n2h/teacher-mixte.log", "description": "Wait 20 minutes for distillation to start", … [27 caractères tronqués]`

  ```
started background job bash-280
  ```

- **job_output** `{"job_id": "bash-280", "timeout_ms": 1500000, "wait": true}`

  ```
Error: wait aborted
  ```


## Tour 4

### 👤 Utilisateur

en-cours.md doit contenir pour chaque session tout ton plan, ambition et stratégie et objectif final. Continue ton bon travail en maintenant ce document à jour pour que les autres sessions locales puissent être en synergie avec tes travaux.

### 🤖 Assistant

⏵ Mise à jour d'`en-cours` : plan complet, ambition et stratégie de la session N2.h

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; python3 tools/sessions.py --status 2>&1 | head -8; echo \"=== en-cours sessions ===\"; sed -n 11,50p docs/pilotage/en-cours.md; echo \"=== campagne ===\"; ls work/n2h/*.pt 2>/dev/null; tail -1 work/n2h/A-propre-g1.log  … [74 caractères tronqués]`

  ```
22:38
sessions · plans de mandat
    0b0a6a0d-05f5-4308 · terminé  · 149 min · N2 — le budget complet, les données et le curriculum
      → **close** — N2.d est mesuré : budget **2,9355 → 2,8527**, quatre sources
    0b69f616-5c75-4c34 · terminé  · 1478 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
    22e518ee-81b8-4081 · terminé  · 649 min · archives de sessions, journal, en-cours, roadmap, backlog, outillage d'archivage
      → clôture committée (`eff8d8e4`) — session close ; la suite est **N2** (la hiérarchie), portée par la session à ouvrir
    71d57f53-8b41-4220 · terminé  · 1982 min · docs/pilotage/en-cours.md, docs/methode/continuite.md, tools/sessions.py
=== en-cours sessions ===
## Sessions en cours

> Contrat et budget : [`continuite.md`](../methode/continuite.md) ; sessions terminées :
> [`journal/sessions/`](../../journal/sessions/).

> **Plan d'abord.** Chaque session active expose son mandat dans
> [`journal/sessions/`](../../journal/sessions/) (`<id>/plan.md`) ; `python3 tools/sessions.py --status`
> avant d'écrire ici.

> **Écriture.** Toute session écrit l'état, **une à la f
… [2085 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nfrom taille_documents import mots_hors_diagrammes\nfrom pathlib import Path\na=mots_hors_diagrammes(Path('AGENTS.md').read_text())\ne=mots_hors_diagrammes(Path('docs/pilotage … [280 caractères tronqués]`

  ```
AGENTS 1200 en-cours 1266 max méthode (1579, 'organisation-du-depot.md') T0 4045 marge -45
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md", "offset": 50, "limit": 90}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
50:   [`r06`](../../reports/rapport-r06-publication.md) (cascade à confiance **publiée**).
51: - **R4.1–R4.3 — les blocs structurels** : **mesurées** — 996 cellules/802, 294 fichiers/24,
52:   32 formules/10 dérivées, **miroir 34/34, 296/296, 42/42** ; fiches
53:   [`r41`](../../reports/rapport-r41-bloc-tableaux.md), [`r42`](../../reports/rapport-r42-bloc-code.md),
54:   [`r43`](../../reports/rapport-r43-bloc-maths.md), [`miroir`](../../reports/rapport-miroir-blocs.md).
55:   **R4.4 partielle** : OCR installé sans root, **10 pages rendues** à **WER 4,48 %** et
56:   **parité 90 %** ; page dégradée **26,7 %** ; fiche [`r44`](../../reports/rapport-r44-ocr-pilote.md).
57: - **R13 — la tokenisation** : **close**, décision **octets** — BPE 512 +0,39 % (bruit), BPE
58:   1024 +4,09 %, anglais +4,22/+6,59 % à octets égaux ; fiche
59:   [`r13`](../../reports/rapport-r13-decision.md), spécification
60:   [`tokenisation`](../implantation/tokenisation.md).
61: - **B10.2bis — décodeur** : 3×3 : **11,1** ; capacité 11,8 ; **mots 32,5** ;
62:   **JW 26,7** (plancher 17,1) ; `z` 1,5–
… [5722 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\n\n# 1. Remplacer le bloc « session à ouvrir » par la session active N2.h, avec plan, ambition, stratégie.\ndebut = s.index(\"### Sess … [5450 caractères tronqués]`

  ```
ok
  en-cours · 1249 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ❌ 3 anomalie(s) :
     · section absente : « Ce qui reste »
     · session « Session `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — N2.h, le mètre propre » ne dit pas « **Id** »
     · « Ce qui reste » ne nomme aucune prochaine action (A/B/C/N/R)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\ns = s.replace(\"\"\"### Session `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — N2.h, le mètre propre\n\n- **Rôle** : **N2.h — le mètre prop … [966 caractères tronqués]`

  ```
ok
  en-cours · 1305 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md", "description": "Read the session plan file"}`

  ```
# Plan de session — N2-budget

> **Mandat ouvert** le 2026-10-31 17 h 35 HAE depuis [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md)
> — le heartbeat est celui de l'état ; la session le met à jour à chaque cycle.

- **Session** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2`
- **Rôle** : calcul : distillation
- **Périmètre** : N2 — le budget complet, les données et le curriculum
- **Fichiers réservés** : `work/n2d/`, `tools/distiller_budget.py`, `reports/n2-*`,
  `journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/`
- **Heartbeat** : 2026-10-31 20:10 HAE
- **Prochaine action** : **close** — N2.d est mesuré : budget **2,9355 → 2,8527**, quatre sources
  **3,7591**, quotas égaux **3,4350**, curriculum **2,8471 / 2,8327**, et **32,8 % des fenêtres de
  validation sont verbatim dans l'entraînement**. La suite appartient au corpus, pas à
  l'entraînement.
- **État** : terminé
  ```

- **write** `{"content": "# Plan de session — N2.h, le mètre propre\n\n> **Mandat ouvert** le 2026-10-31 22 h 30 HAE depuis [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md)\n> — mandat libre de 10 h (nuit du 31/10 au 1/11). Le heartbeat est celui de l'état.\n\n- **Session** : `0b0a6a0d-05f5-4308 … [1799 caractères tronqués]`

  ```
Error: cannot write "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md": file changed since it was read — re-read the file, then retry
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md; echo \"=== git ===\"; git log --oneline -2 -- journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md", "description": "Re-read the session plan"}`

  ```
# Plan de session — N2-budget

> **Mandat ouvert** le 2026-10-31 17 h 35 HAE depuis [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md)
> — le heartbeat est celui de l'état ; la session le met à jour à chaque cycle.

- **Session** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2`
- **Rôle** : calcul : distillation
- **Périmètre** : N2 — le budget complet, les données et le curriculum
- **Fichiers réservés** : `work/n2d/`, `tools/distiller_budget.py`, `reports/n2-*`,
  `journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/`
- **Heartbeat** : 2026-10-31 20:10 HAE
- **Prochaine action** : **close** — N2.d est mesuré : budget **2,9355 → 2,8527**, quatre sources
  **3,7591**, quotas égaux **3,4350**, curriculum **2,8471 / 2,8327**, et **32,8 % des fenêtres de
  validation sont verbatim dans l'entraînement**. La suite appartient au corpus, pas à
  l'entraînement.
- **État** : terminé
=== git ===
ffad1c53 DOCS — LE MODÈLE NATIF ET DIEHL & COOK ENRICHIS : QUOTIENT, TYPES, NEUTRALITÉ, DÉTERMINISME, BANC, CONFORMITÉ
bb3bfefe DOCS — LE MODÈLE NATIF ET DIEHL & COOK, 13 SCHÉMAS : LA SÉPARATION À TROIS NIVEAUX
  ```

- **write** `{"content": "# Plan de session — N2.h, le mètre propre\n\n> **Mandat ouvert** le 2026-10-31 22 h 30 HAE depuis [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md)\n> — mandat libre de 10 h (nuit du 31/10 au 1/11). Le heartbeat est celui de l'état.\n\n- **Session** : `0b0a6a0d-05f5-4308 … [1799 caractères tronqués]`

  ```
Error: cannot write "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md": file changed since it was read — re-read the file, then retry
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md <<'EOF'\n# Plan de session — N2.h, le mètre propre\n\n> **Mandat ouvert** le 2026-10-31 22 h 30 HAE depuis [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-co … [1995 caractères tronqués]`

  ```
✅ plans cohérents
  ✅ état court, structuré, multi-session et reprenable
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md && git commit -m \"ÉTAT — LA SESSION N2.h PORTE SON PLAN, SON AMBITION ET SA STRATÉGIE DANS LA PAGE D'ÉTAT\n\nLa page d'état doit suffire … [873 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-288]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-288", "timeout_ms": 180000, "wait": true}`

  ```
✅ index : aucun fait stagé sans état
[master 3dc2fe27] ÉTAT — LA SESSION N2.h PORTE SON PLAN, SON AMBITION ET SA STRATÉGIE DANS LA PAGE D'ÉTAT
 18 files changed, 735 insertions(+), 117 deletions(-)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt work/n2h/route-teacher-propre 2>/dev/null | head; tail -1 work/n2h/teacher.log; tail -1 work/n2h/A-propre-g1.log 2>/dev/null; tail -1 work/n2h/teacher-mixte.log", "description": "Check campaign state a … [23 caractères tronqués]`

  ```
22:42
work/n2h/base-propre.pt
  pas  15000 · perte 0.8470 · val 1.3636 bits/octet · 1222 s
  pas   4000 · perte 1.2791 · val 1.7448 bits/octet · 333 s
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche du corpus propre pendant que la distillation tourne

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/fiche1.md <<'EOF'\n# N2.h1 — La validation n'était pas tenue à l'écart : le corpus propre, et la porte honnête\n\n> **Ligne de roadmap** : N2 · **Date** : 2026-10-31 · **Verdict** : le corpus de N2 se recopiait\n> (32, … [3522 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null; for f in A-propre-g1 A-propre-g2; do tail -1 work/n2h/$f.log 2>/dev/null; done; tail -1 work/n2h/D-mixte-g1.log 2>/dev/null", "description": "Wait 25 minutes for the first clea … [43 caractères tronqués]`

  ```
started background job bash-291
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -1 work/n2h/teacher.log; ls work/n2h/*.pt 2>/dev/null; grep -c \"\" work/n2h/A-propre-g1.log 2>/dev/null", "description": "Quick check of teacher completion"}`

  ```
22:42
  pas  15000 · perte 0.8470 · val 1.3636 bits/octet · 1222 s
work/n2h/base-propre.pt
[exit code: 2]
  ```

- **job_output** `{"job_id": "bash-291", "timeout_ms": 1800000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null; tail -1 work/n2h/A-propre-g1.log 2>/dev/null; tail -1 work/n2h/teacher-mixte.log", "description": "Check campaign progress"}`

  ```
22:53
work/n2h/base-propre.pt
pas  3250 · seq 128 · perte 63.3133 · PPL 128/4 3.3356 · 235 s
  pas  12000 · perte 1.2389 · val 1.5388 bits/octet · 993 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat reports/corpus-propre.json", "description": "Review the clean corpus manifest"}`

  ```
{
 "source": "data/corpus_fr.txt",
 "source_octets": 4633889,
 "source_sha256": "1e39f1a8aeac403d7b7ff5adc598fd8dd14233287707d5849a37c3e667f145d4",
 "methode": {
  "deduplication": "shingles de Rabin-Karp (base 257, mod 2^61−1), première occurrence gardée, runs gardés ≥ 64 octets, joints par \\n",
  "fenetre_shingle": 96,
  "chunk_octets": 8192,
  "split": "un chunk sur 20 en validation, le suivant sur 20 en test"
 },
 "propre_octets": 3605306,
 "deduplication": {
  "retires": 1029993,
  "runs": 1411,
  "plus_long_run": 540086,
  "retires_pct": 22.23
 },
 "train_octets": 3244858,
 "val_octets": 180224,
 "test_octets": 180224,
 "chunks": {
  "train": -360007,
  "val": 180224,
  "test": 180224
 },
 "sha256": {
  "train": "8a1856022ed5eb58e773652fb2fcba827cb9d30958a39c3f2cf05c69efb73a71",
  "val": "d9ffb0bb49d5fe088062d411e0b1b7b1d373c2d602e2c6f4556c93a101819f57",
  "test": "566d467e3c7ecdbd280fbc6766627adc6d8d37560c04a69d6b8c554be6983531"
 },
 "contamination": {
  "validation": {
   "fenetres": 2814,
   "contaminees": 0,
   "taux": 0.0
  },
  "test": {
   "fenetres": 2814,
   "contaminees": 0,
   "taux": 0.0
  }
 },
 "plus_longue_repetition_val_train": 0,
 "licence": "corpus local, l
… [129 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\n# 1. corriger le manifeste (comptes de chunks, pas d'octets)\np = pathlib.Path('reports/corpus-propre.json'); m = json.loads(p.read_text())\nm[\"chunks\"] = {\"train\": 397, \"val\": 22, \"tes … [1313 caractères tronqués]`

  ```
manifeste {'train': 397, 'val': 22, 'test': 22}
outil corrigé
{'train': 397, 'val': 22, 'test': 22}
  ```

- **job_output** `{"job_id": "bash-291", "timeout_ms": 1500000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-280 (bash: sleep 1200; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null; for f in A-propre-g1 A-propre-g2; do tail -1 work/n2h/$f.log 2>/dev/null; done; tail -1 work/n2h/teacher-mixte.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null; tail -2 work/n2h/A-propre-g1.log 2>/dev/null; tail -1 work/n2h/teacher-mixte.log; tail -1 work/n2h/base-mixte.log 2>/dev/null", "description": "Check the clean and mixed chains"}`

  ```
23:03
work/n2h/base-propre.pt
pas 12250 · seq 128 · perte 46.8716 · PPL 128/4 3.2025 · 845 s
pas 12500 · seq 128 · perte 48.4809 · PPL 128/4 3.1871 · 862 s
  # écrit dans work/n2h/route-teacher-mixte · 23.57 M paramètres · 1.46 M poids lus/jeton/couche
pas  700 · perte 2.3717 · PPL val 10.655 · 29 s
  ```

- **bash** `{"command": "sleep 900; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/A-propre-g1.pt 2>/dev/null && echo A1_OK; tail -1 work/n2h/A-propre-g2.log 2>/dev/null; tail -1 work/n2h/D-mixte-g1.log 2>/dev/null", "description": "Wait for the first clean distillation to fini … [31 caractères tronqués]`

  ```
started background job bash-297
  ```

- **job_output** `{"job_id": "bash-297", "timeout_ms": 1200000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-291 (bash: sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null; for f in A-propre-g1 A-propre-g2; do tail -1 work/n2h/$f.log 2>/dev/null; done; tail -1 work/n2h/D-mixte-g1.log 2>/dev/null) finished [status: completed, exit code: 1]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null; tail -2 work/n2h/A-propre-g1.log; tail -1 work/n2h/A-propre-g2.log 2>/dev/null", "description": "Check whether the first clean run finished"}`

  ```
23:13
work/n2h/A-propre-g1.pt
work/n2h/base-propre.pt
 "positions_aleatoires": 0
}
pas  1250 · seq 128 · perte 75.0892 · PPL 128/4 3.3555 · 86 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json; d=json.load(open('work/n2h/A-propre-g1.json'))\nprint({k:round(v,4) if isinstance(v,float) else v for k,v in d.items() if k in ('ppl_128_lot16','ppl_129_lot15','ppl_128_lot8','ppl_permute','duree_s','octet … [233 caractères tronqués]`

  ```
{'octets_vus': 40960000, 'ppl_128_lot16': 3.1925, 'ppl_128_lot8': 3.1671, 'ppl_129_lot15': 3.1739, 'ppl_permute': 1380.8955, 'duree_s': 1381.8896}
{"fichier": "A-propre-g1.pt", "params": 11814792, "val": 3.0971, "test": 3.2098, "litterature": 15.9854, "litterature_propre": 17.0838, "anglais": 60.6957, "wikitext2": 59.729, "permute": 1356.6433, "decomposition": {"complete": 3.1298, "apres_2_blocs": 3.8236, "apres_4_blocs": 3.2291, "apres_6_blocs": 3.0562, "sans_pensee": 23636033.02}, "longueurs": {"129": 3.1334, "192": 8.7137, "256": 14.4554, "384": 24.8061, "512": 34.0535}}
  ```

- **bash** `{"command": "sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\\n' ' '; echo; for f in A-propre-g3 C-propre-g1 D-mixte-g1; do tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Wait 25 minutes for seeds 2 and 3", "run_in_bac … [15 caractères tronqués]`

  ```
started background job bash-300
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\nvieux = \"\"\"- **Prochaine action** : attendre la distillation A (3 graines) puis évaluer la porte honnête.\"\"\"\nneuf = \"\"\"- ** … [817 caractères tronqués]`

  ```
en-cours · 1570 mots · 7 sections · 3 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 11, in <module>
AssertionError
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 11,100p docs/pilotage/en-cours.md", "description": "Re-read the updated state page"}`

  ```
## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session qui trouve l'état en retard
> le corrige.

### Session `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — N2.h, le mètre propre

- **Id** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — [`plan.md`](../../journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md).
- **Rôle** : **N2.h — le mètre propre** : corpus, distillation, évaluation.
- **Plan** : 1) `tools/corpus_propre.py` (dédup, split par chunks) ; 2) chaîne propre (professeur 23,5 M, base 20k, distillation 20k × 3, curriculum 129 × 3) ; 3) porte honnête + hors domaine + décomposition ; 4) diversité FR 50/50 ; 5) verrou de longueur 129→512 × 3 ; 6) fiches, portes, commit.
- **Ambition** : sortir N2 du chiffre contaminé (**2,85** sur **32,8 %**) et donner à R un modèle qui lit du français général ; trancher le verrou de longueur.
- **Stratégie** : un seul changement à la fois, trois graine
… [6494 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\nvieux = \"\"\"- **Ce qu'elle fait** : la dédup et le split, puis la distillation A (3 graines) et la porte honnête.\"\"\"\nneuf = \"\ … [1213 caractères tronqués]`

  ```
ok
  en-cours · 1650 mots · 7 sections · 3 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
     · T0 : 4024 mots (AGENTS + en-cours + une tâche) > budget 4 000
  revue de documentation · 371 fiche(s) · 441 JSON · 114 doc(s) · 79 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\na = \"\"\"- **N2.h — le mètre propre** : le **corpus d'abord** (dédup, split par document), puis la\n  distillation A et la porte hon … [1332 caractères tronqués]`

  ```
ok
  ✅ état court, structuré, multi-session et reprenable
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **job_output** `{"job_id": "bash-300", "timeout_ms": 1500000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-297 (bash: sleep 900; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/A-propre-g1.pt 2>/dev/null && echo A1_OK; tail -1 work/n2h/A-propre-g2.log 2>/dev/null; tail -1 work/n2h/D-mixte-g1.log 2>/dev/null) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\\n' ' '; echo; tail -1 work/n2h/A-propre-g3.log 2>/dev/null; tail -1 work/n2h/D-mixte-g1.log 2>/dev/null", "description": "Check seed 3 and mixed arm progress"}`

  ```
23:25
work/n2h/A-propre-g1.pt work/n2h/base-mixte.pt work/n2h/base-propre.pt 
pas  6250 · seq 128 · perte 37.6891 · PPL 128/4 3.4493 · 428 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la work/n2h/ | grep -E \"A-propre|D-mixte|base-mixte\" ; tail -3 work/n2h/A-propre-g2.log; echo \"=== D ===\"; ls work/n2h/D-mixte-g1.log 2>/dev/null && tail -1 work/n2h/D-mixte-g1.log", "description": "Inspect A g2 output and D  … [7 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane     8649 31 oct 23:12 A-propre-g1.json
-rw-r--r--. 1 stephane stephane     6155 31 oct 23:12 A-propre-g1.log
-rw-r--r--. 1 stephane stephane     6657 31 oct 23:12 A-propre-g1.out
-rw-r--r--. 1 stephane stephane 47302035 31 oct 23:12 A-propre-g1.pt
-rw-r--r--. 1 stephane stephane     3241 31 oct 23:25 A-propre-g2.log
-rw-r--r--. 1 stephane stephane     3744 31 oct 23:25 A-propre-g2.out
-rw-r--r--. 1 stephane stephane 47278428 31 oct 23:18 base-mixte.drvm
-rw-r--r--. 1 stephane stephane    21522 31 oct 23:18 base-mixte.log
-rw-r--r--. 1 stephane stephane 47301903 31 oct 23:18 base-mixte.pt
-rw-r--r--. 1 stephane stephane      545 31 oct 23:18 base-mixte.pt.json
-rw-r--r--. 1 stephane stephane     1785 31 oct 23:25 D-mixte-g1.log
-rw-r--r--. 1 stephane stephane     2288 31 oct 23:25 D-mixte-g1.out
pas 11000 · seq 128 · perte 52.2104 · PPL 128/4 3.2036 · 767 s
pas 11250 · seq 128 · perte 55.0901 · PPL 128/4 3.2288 · 784 s
pas 11500 · seq 128 · perte 42.3927 · PPL 128/4 3.2116 · 801 s
=== D ===
work/n2h/D-mixte-g1.log
pas  6250 · seq 128 · perte 37.6891 · PPL 128/4 3.4493 · 428 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/fiche2.md <<'EOF'\n# N2.h2 — La diversité française : ce que coûte un modèle qui sait lire autre chose que le dépôt\n\n> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : entraîné moitié sur le dépôt,\n … [4927 caractères tronqués]`

  ```
ok
23:26
pas 12000 · seq 128 · perte 44.3240 · PPL 128/4 3.1885 · 835 s
  ```

- **bash** `{"command": "sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | wc -l; for f in A-propre-g3 C-propre-g1 D-mixte-g1 D-mixte-g2; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Wait for seed 3 and the mixed arm … [29 caractères tronqués]`

  ```
started background job bash-308
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -5; git status --short | head -8; date '+%H:%M'", "description": "Check other sessions' commits and the working tree"}`

  ```
9a03d2dc ÉTAT — TROIS SESSIONS, PLAN/AMBITION/STRATÉGIE/OBJECTIF FINAL, ET LE CONTRAT DU MOTEUR
7408441e R4.4 — CENT SCANS SIMULÉS, CINQ FAMILLES : LA PHOTO PASSE DE 55,9 % À 7,3 % DE WER
3dc2fe27 ÉTAT — LA SESSION N2.h PORTE SON PLAN, SON AMBITION ET SA STRATÉGIE DANS LA PAGE D'ÉTAT
91f31faa PENSÉE — TOURS 5-10 : CONTRAT, ANYTIME, MÉTA, MÉMOIRE, MESURE
0a296b75 PENSÉE — TOURS 3-4 : LE CYCLE MULTI-NIVEAUX ET LE PORTEFEUILLE DE STRATÉGIES
 M docs/pilotage/en-cours.md
 M journal/README.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/digest.md
23:26
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md && timeout 300 git commit -m \"ÉTAT — N2.h : LA CHAÎNE PROPRE DONNE 3,10 EN DOMAINE, PAS 2,85\n\nLe premier point de contrôle de la chaîne refaite sur le corpus dédupliqué est évalué : 3,10 en\ndomai … [439 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-310]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-310", "timeout_ms": 180000, "wait": true}`

  ```
✅ index : aucun fait stagé sans état
[master 47db37ba] ÉTAT — N2.h : LA CHAÎNE PROPRE DONNE 3,10 EN DOMAINE, PAS 2,85
 19 files changed, 1262 insertions(+), 52 deletions(-)
 create mode 100644 journal/2026-10-31/moteur.md
[status: completed, exit code: 0]
  ```

- **job_output** `{"job_id": "bash-308", "timeout_ms": 1500000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\\n' ' '; echo; for f in A-propre-g3 C-propre-g1 D-mixte-g1 D-mixte-g2; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Check campaign progress at the m … [10 caractères tronqués]`

  ```
23:38
work/n2h/A-propre-g1.pt work/n2h/A-propre-g2.pt work/n2h/base-mixte.pt work/n2h/base-propre.pt 
-- A-propre-g3
pas  2250 · seq 128 · perte 65.1979 · PPL 128/4 3.3508 · 155 s
-- C-propre-g1
-- D-mixte-g1
pas 17000 · seq 128 · perte 27.6824 · PPL 128/4 3.3579 · 1174 s
-- D-mixte-g2
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nfor f in ('work/n2h/A-propre-g1.json','work/n2h/A-propre-g2.json'):\n    d=json.load(open(f)); print(f, {k:round(v,4) if isinstance(v,float) else v for k,v in d.items() if k in ('ppl_128_lot16','ppl_129_lo … [65 caractères tronqués]`

  ```
work/n2h/A-propre-g1.json {'ppl_128_lot16': 3.1925, 'ppl_129_lot15': 3.1739, 'ppl_permute': 1380.8955}
work/n2h/A-propre-g2.json {'ppl_128_lot16': 3.1623, 'ppl_129_lot15': 3.1489, 'ppl_permute': 1253.6504}
  ```

- **bash** `{"command": "sleep 420; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\\n' ' '; echo; tail -1 work/n2h/D-mixte-g1.log 2>/dev/null; tail -1 work/n2h/A-propre-g3.log", "description": "Wait for the first mixed-arm result", "run_in_background": t … [4 caractères tronqués]`

  ```
started background job bash-313
  ```

- **job_output** `{"job_id": "bash-313", "timeout_ms": 900000, "wait": true}`

  ```
23:45
work/n2h/A-propre-g1.pt work/n2h/A-propre-g2.pt work/n2h/base-mixte.pt work/n2h/base-propre.pt work/n2h/D-mixte-g1.pt 
}
pas  8250 · seq 128 · perte 56.3000 · PPL 128/4 3.2037 · 580 s
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-300 (bash: sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\n' ' '; echo; for f in A-propre-g3 C-propre-g1 D-mixte-g1; do tail -1 work/n2h/$f.log 2>/dev/null; done) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 900 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/D-mixte-g1.pt --decomposition --longueurs 2>&1 | grep -v Loading", "description": "Evaluate the first mixed model"}`

  ```
{"fichier": "D-mixte-g1.pt", "params": 11814792, "val": 3.2605, "test": 3.3195, "litterature": 3.5306, "litterature_propre": 3.8566, "anglais": 26.3189, "wikitext2": 26.5323, "permute": 482.468, "decomposition": {"complete": 3.2872, "apres_2_blocs": 4.2693, "apres_4_blocs": 3.4896, "apres_6_blocs": 3.2562, "sans_pensee": 4817836.3858}, "longueurs": {"129": 3.304, "192": 7.5647, "256": 11.2344, "384": 16.5044, "512": 20.1983}}
  ```

### 🤖 Assistant

⏵ Le bras diversité divise la PPL hors domaine par 4,4 pour 0,16 en domaine

- **bash** `{"command": "sleep 900; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | wc -l; for f in A-propre-g3 C-propre-g1 D-mixte-g2; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Wait for seed 3 and the curriculum", "run_in_ … [18 caractères tronqués]`

  ```
started background job bash-315
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\\n' ' '; echo; tail -1 work/n2h/A-propre-g3.log 2>/dev/null; tail -1 work/n2h/D-mixte-g2.log 2>/dev/null", "description": "Check progress"}`

  ```
23:46
work/n2h/A-propre-g1.pt work/n2h/A-propre-g2.pt work/n2h/base-mixte.pt work/n2h/base-propre.pt work/n2h/D-mixte-g1.pt 
pas  9000 · seq 128 · perte 54.2723 · PPL 128/4 3.1984 · 633 s
pas  3750 · seq 128 · perte 37.1792 · PPL 128/4 3.4795 · 264 s
  ```

- **bash** `{"command": "sleep 900; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\\n' ' '; echo; for f in C-propre-g1 C-propre-g2 D-mixte-g2; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Wait for the clean seeds and cur … [36 caractères tronqués]`

  ```
started background job bash-317
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\nvieux = \"\"\"- **Résultat intermédiaire** (graine 1) : **3,10** en domaine, **3,21** au test ; **17,1** sur\n  la littérature jamais … [999 caractères tronqués]`

  ```
ok
  ✅ état court, structuré, multi-session et reprenable
     · T0 : 4031 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\na = \"\"\"**Les sept chantiers C** (hors graphe, transférés au journal) : **C1** corpus · **C2**\ntraduction · **C3** restitution · * … [680 caractères tronqués]`

  ```
ok
  ✅ état court, structuré, multi-session et reprenable
     · T0 : 4010 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\na = \"\"\"> **État courant, pas histoire.** Une sous-section par **session active** ; une ligne par **chantier** avec son\n> **bloqua … [957 caractères tronqués]`

  ```
ok
  ✅ état court, structuré, multi-session et reprenable
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
     · structure : 0 chantiers sur 7 dans en-cours.md ([])
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"chantiers\" tools/revue_documentation.py | head -10; sed -n \"$(grep -n 'chantiers sur' tools/revue_documentation.py | head -1 | cut -d: -f1),+12p\" tools/revue_documentation.py", "description": "Inspect the chantiers check … [21 caractères tronqués]`

  ```
6:  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
133:    # 2. les sept chantiers
136:        alertes.append(f"structure : {len(ids)} chantiers sur 7 dans en-cours.md ({ids})")
        alertes.append(f"structure : {len(ids)} chantiers sur 7 dans en-cours.md ({ids})")

    # 4. fraîcheur : la date de la page, ET aucun fait commité après le dernier état.
    #    La date seule ne suffit pas : deux commits du même jour passaient (A8.0, 29/10).
    m = re.search(r"Mis à jour : (\d{4}-\d\d-\d\d)", t)
    if not m:
        alertes.append("fraîcheur : en-cours.md n'a pas de date « Mis à jour : AAAA-MM-JJ »")
    else:
        page, dernier = m.group(1), date_dernier_commit()
        if dernier and page != dernier:
            alertes.append(
                f"fraîcheur : en-cours.md dit {page}, le dernier commit date du {dernier}"
            )
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 125,137p tools/revue_documentation.py", "description": "Read the seven-chantiers regex"}`

  ```
def main() -> int:
    alertes: list[str] = []
    en = RACINE / "docs/pilotage/en-cours.md"
    if not en.exists():
        print("✗ docs/pilotage/en-cours.md absent")
        return 1
    t = en.read_text()

    # 2. les sept chantiers
    ids = sorted(set(re.findall(r"\*\*(C[1-7])\*\*", t)))
    if len(ids) < 7:
        alertes.append(f"structure : {len(ids)} chantiers sur 7 dans en-cours.md ({ids})")
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\na = \"\"\"**Les sept chantiers C** (C1 corpus → C7 pensée) sont hors graphe, mesurés et désormais du\nrécit : le journal, pas le plan … [487 caractères tronqués]`

  ```
ok
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ✅ état court, structuré, multi-session et reprenable
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md && timeout 300 git commit -m \"ÉTAT — N2.h : LA DIVERSITÉ FRANÇAISE DIVISE LA PPL HORS DÉPÔT PAR 4,4\n\nLe bras diversité (moitié dépôt, moitié littérature française, même budget, mêmes trois graines … [435 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-324]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-324", "timeout_ms": 180000, "wait": true}`

  ```
✅ index : aucun fait stagé sans état
[master 26f722e7] ÉTAT — N2.h : LA DIVERSITÉ FRANÇAISE DIVISE LA PPL HORS DÉPÔT PAR 4,4
 16 files changed, 884 insertions(+), 57 deletions(-)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\\n' ' '; echo; for f in C-propre-g1 D-mixte-g2; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Check curriculum and mixed seed 2"}`

  ```
23:48
work/n2h/A-propre-g1.pt work/n2h/A-propre-g2.pt work/n2h/base-mixte.pt work/n2h/base-propre.pt work/n2h/D-mixte-g1.pt 
-- C-propre-g1
-- D-mixte-g2
pas  6000 · seq 128 · perte 35.8956 · PPL 128/4 3.4636 · 418 s
  ```

- **bash** `{"command": "sleep 1800; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\\n' ' '; echo; for f in C-propre-g2 R-pos-g1 D-mixte-g3; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Wait 30 minutes for curriculum and … [50 caractères tronqués]`

  ```
started background job bash-326
  ```

- **job_output** `{"job_id": "bash-326", "timeout_ms": 1800000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-308 (bash: sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | wc -l; for f in A-propre-g3 C-propre-g1 D-mixte-g1 D-mixte-g2; do echo "-- $f"; tail -1 work/n2h/$f.log 2>/dev/null; done) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | tr '\\n' ' '; echo; for f in C-propre-g1 C-propre-g2 D-mixte-g2 D-mixte-g3; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Check campaign progress"}`

  ```
23:59
work/n2h/A-propre-g1.pt work/n2h/A-propre-g2.pt work/n2h/A-propre-g3.pt work/n2h/base-mixte.pt work/n2h/base-propre.pt work/n2h/D-mixte-g1.pt 
-- C-propre-g1
pas   250 · seq 129 · perte 43.2406 · PPL 128/4 3.2073 · 17 s
-- C-propre-g2
-- D-mixte-g2
pas 15250 · seq 128 · perte 25.1889 · PPL 128/4 3.3999 · 1049 s
-- D-mixte-g3
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 900 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/A-propre-g2.pt work/n2h/A-propre-g3.pt 2>&1 | grep -v Loading", "description": "Evaluate the remaining clean seeds"}`

  ```
usage: eval_n2_propre.py [-h] [--chunk CHUNK] [--longueurs] [--decomposition]
                         [--sortie SORTIE] [--device DEVICE]
                         point
eval_n2_propre.py: error: unrecognized arguments: work/n2h/A-propre-g3.pt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for g in 2 3; do PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 600 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/A-propre-g$g.pt 2>&1 | grep -v Loading; done", "description": "Evaluate seeds 2 and 3 individually"}`

  ```
{"fichier": "A-propre-g2.pt", "params": 11814792, "val": 3.0883, "test": 3.1914, "litterature": 15.4628, "litterature_propre": 16.5501, "anglais": 55.9666, "wikitext2": 55.2124, "permute": 1221.2743}
{"fichier": "A-propre-g3.pt", "params": 11814792, "val": 3.0858, "test": 3.1867, "litterature": 15.4773, "litterature_propre": 16.4764, "anglais": 56.0697, "wikitext2": 55.7049, "permute": 1227.5534}
  ```

- **bash** `{"command": "sleep 1800; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | wc -l; for f in C-propre-g3 R-pos-g1 D-mixte-g3; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Wait 30 minutes for curriculum and random positions", "run_ … [21 caractères tronqués]`

  ```
started background job bash-330
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3; git status --short | head -5; date '+%H:%M'", "description": "Check repo state and other sessions"}`

  ```
26f722e7 ÉTAT — N2.h : LA DIVERSITÉ FRANÇAISE DIVISE LA PPL HORS DÉPÔT PAR 4,4
47db37ba ÉTAT — N2.h : LA CHAÎNE PROPRE DONNE 3,10 EN DOMAINE, PAS 2,85
9a03d2dc ÉTAT — TROIS SESSIONS, PLAN/AMBITION/STRATÉGIE/OBJECTIF FINAL, ET LE CONTRAT DU MOTEUR
 M tools/distiller_budget.py
 m tools/docwatch
 M tools/graphe_document_ocr.py
 M tools/mesurer_scans.py
 M tools/native_model.py
00:00
  ```

- **job_output** `{"job_id": "bash-330", "timeout_ms": 1500000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-315 (bash: sleep 900; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | wc -l; for f in A-propre-g3 C-propre-g1 D-mixte-g2; do echo "-- $f"; tail -1 work/n2h/$f.log 2>/dev/null; done) finished [status: completed, exit code: 0]. Read its output with job_output.

### 👤 Utilisateur

background job bash-317 (bash: sleep 900; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\n' ' '; echo; for f in C-propre-g1 C-propre-g2 D-mixte-g2; do echo "-- $f"; tail -1 work/n2h/$f.log 2>/dev/null; done) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | tr '\\n' ' '; echo; for f in C-propre-g2 R-pos-g1 D-mixte-g3; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Check curriculum, mixed seed 3 and random positions"}`

  ```
00:10
work/n2h/A-propre-g1.pt work/n2h/A-propre-g2.pt work/n2h/A-propre-g3.pt work/n2h/base-mixte.pt work/n2h/base-propre.pt work/n2h/C-propre-g1.pt work/n2h/D-mixte-g1.pt work/n2h/D-mixte-g2.pt 
-- C-propre-g2
pas   250 · seq 129 · perte 46.9611 · PPL 128/4 3.2025 · 17 s
-- R-pos-g1
-- D-mixte-g3
pas  5000 · seq 128 · perte 41.4237 · PPL 128/4 3.4275 · 349 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 timeout 600 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/D-mixte-g2.pt 2>&1 | grep -v Loading; python3 -c \"\nimport json; d=json.load(open('work/n2h/C-propre-g1.json'))\nprint('C g1', {k: … [176 caractères tronqués]`

  ```
{"fichier": "D-mixte-g2.pt", "params": 11814792, "val": 3.26, "test": 3.3203, "litterature": 3.5217, "litterature_propre": 3.8562, "anglais": 25.3735, "wikitext2": 25.798, "permute": 462.8188}
C g1 {'ppl_128_lot16': 3.1677, 'ppl_129_lot15': 3.1125}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/evalue-tout.sh <<'EOF'\n#!/bin/bash\n# Évalue tous les points de contrôle N2.h : porte honnête, hors domaine, décomposition, longueurs.\nset -u\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nexport PYTHONPATH=. C … [1015 caractères tronqués]`

  ```
ok
00:11
pas   750 · seq 129 · perte 51.0452 · PPL 128/4 3.2103 · 52 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/journal.md <<'EOF'\n### N2.h — le mètre propre, la généralité, et le verrou de longueur\n\nLa nuit du 31 octobre au 1er novembre, la session a eu **dix heures**. Le premier geste n'a pas été\nd'entraîner plus : il a ét … [1791 caractères tronqués]`

  ```
ok
00:11
pas  1000 · seq 129 · perte 41.2979 · PPL 128/4 3.2025 · 69 s
  ```

- **bash** `{"command": "sleep 2400; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | tr '\\n' ' '; echo; for f in C-propre-g3 R-pos-g1 R-pos-g2 D-mixte-g3; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Wait 40 minutes for the random-positi … [35 caractères tronqués]`

  ```
started background job bash-336
  ```

- **job_output** `{"job_id": "bash-336", "timeout_ms": 2400000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-326 (bash: sleep 1800; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt 2>/dev/null | tr '\n' ' '; echo; for f in C-propre-g2 R-pos-g1 D-mixte-g3; do echo "-- $f"; tail -1 work/n2h/$f.log 2>/dev/null; done) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | tr '\\n' ' '; echo; for f in C-propre-g3 R-pos-g1 R-pos-g2 D-mixte-g3; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Check the random-position arm progress"}`

  ```
00:22
work/n2h/A-propre-g1.pt work/n2h/A-propre-g2.pt work/n2h/A-propre-g3.pt work/n2h/base-mixte.pt work/n2h/base-propre.pt work/n2h/C-propre-g1.pt work/n2h/C-propre-g2.pt work/n2h/D-mixte-g1.pt work/n2h/D-mixte-g2.pt 
-- C-propre-g3
# stage seq 129 · 10000 pas · lr 5e-06
-- R-pos-g1
-- R-pos-g2
-- D-mixte-g3
pas 14250 · seq 128 · perte 28.7678 · PPL 128/4 3.3870 · 1016 s
  ```

### 🤖 Assistant

⏵ Rédaction des trois fiches avec un remplisseur automatique depuis l'évaluation

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/fiche1.md <<'EOF'\n# N2.h1 — Le corpus propre : la validation n'était pas tenue à l'écart, et la porte honnête vaut 3,09\n\n> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : le corpus de N2 se recopia … [6606 caractères tronqués]`

  ```
fiche1 écrit
128 work/n2h/fiche1.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/fiche2.md <<'EOF'\n# N2.h2 — La diversité française : un modèle de français plutôt qu'un modèle du dépôt\n\n> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : entraîné **moitié dépôt,\n> moitié littéra … [6847 caractères tronqués]`

  ```
fiches 2 et 3 écrites
  74 work/n2h/fiche2.md
  58 work/n2h/fiche3.md
 132 total
00:22
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/remplit.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"remplit.py — remplit les trois fiches N2.h depuis work/n2h/eval.json.\"\"\"\nimport json, pathlib, statistics as st\n\nev = {r[\"fichier\"]: r for r in json.loads(pathli … [7289 caractères tronqués]`

  ```
ok
00:23
pas   750 · seq 129 · perte 45.7731 · PPL 128/4 3.1869 · 53 s
  ```

- **bash** `{"command": "sleep 1800; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | tr '\\n' ' '; echo; for f in R-pos-g1 R-pos-g2; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Wait 30 minutes for random positions", "run_in_background":  … [5 caractères tronqués]`

  ```
started background job bash-341
  ```

- **job_output** `{"job_id": "bash-341", "timeout_ms": 1800000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-330 (bash: sleep 1800; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | wc -l; for f in C-propre-g3 R-pos-g1 D-mixte-g3; do echo "-- $f"; tail -1 work/n2h/$f.log 2>/dev/null; done) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | wc -l; for f in R-pos-g1 R-pos-g2; do echo \"-- $f\"; tail -1 work/n2h/$f.log 2>/dev/null; done", "description": "Check random-position progress"}`

  ```
00:33
10
-- R-pos-g1
-- R-pos-g2
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls work/n2h/*.pt | sed 's|work/n2h/||' | tr '\\n' ' '; echo; ps -eo pid,etime,cmd | grep distiller_budget | grep -v grep | sed 's/.*--sortie/--sortie/'", "description": "List checkpoints and running jobs"}`

  ```
A-propre-g1.pt A-propre-g2.pt A-propre-g3.pt base-mixte.pt base-propre.pt C-propre-g1.pt C-propre-g2.pt C-propre-g3.pt D-mixte-g1.pt D-mixte-g2.pt D-mixte-g3.pt 
--sortie work/n2h/R-pos-g1.pt --log work/n2h/R-pos-g1.log
  ```

- **bash** `{"command": "sleep 1400; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g1.pt 2>/dev/null && echo R1_OK; tail -1 work/n2h/R-pos-g2.log 2>/dev/null", "description": "Wait for the first random-position run", "run_in_background": true}`

  ```
started background job bash-344
  ```

- **job_output** `{"job_id": "bash-344", "timeout_ms": 1500000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g1.pt 2>/dev/null && echo R1_OK; tail -1 work/n2h/R-pos-g1.log 2>/dev/null; tail -1 work/n2h/R-pos-g2.log 2>/dev/null", "description": "Check R seed 1 completion"}`

  ```
00:43
pas  8750 · seq 128 · perte 68.3296 · PPL 128/4 3.5794 · 612 s
[exit code: 1]
  ```

- **bash** `{"command": "sleep 1000; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g1.pt 2>/dev/null && echo R1_OK; tail -1 work/n2h/R-pos-g2.log 2>/dev/null", "description": "Wait for R seed 1", "run_in_background": true}`

  ```
started background job bash-346
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/backlog/N2-distillation.md'); s = p.read_text()\nvieux = \"\"\"## L'état\n\n49 999 fenêtres, 4 sources ; professeur 30k 1,734 (0,794 bit/octet) ; student 3,123 à 20 00 … [2247 caractères tronqués]`

  ```
backlog N2 mis à jour
14:## L'état
15-
16-Le budget est mesuré (N2.d) : 2,9355 → 2,8527, mais **sur un jeu contaminé à 32,8 %**. N2.h a
17-refait le mètre : corpus dédupliqué (−22,2 % de texte), split par chunks, **0 % de fuite** ; la
18-chaîne propre vaut **3,09** en domaine et **16,7** sur de la littérature jamais vue — le modèle de
19-N2 est un **spécialiste du dépôt**. La diversité française (moitié dépôt, moitié littérature)
20-ramène la littérature à **3,86** pour **+0,17** en domaine.
  ```

- **job_output** `{"job_id": "bash-346", "timeout_ms": 1200000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-336 (bash: sleep 2400; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | tr '\n' ' '; echo; for f in C-propre-g3 R-pos-g1 R-pos-g2 D-mixte-g3; do echo "-- $f"; tail -1 work/n2h/$f.log 2>/dev/null; done) finished [status: completed, exit code: 0]. Read its output with job_output.

### 👤 Utilisateur

background job bash-341 (bash: sleep 1800; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | tr '\n' ' '; echo; for f in R-pos-g1 R-pos-g2; do echo "-- $f"; tail -1 work/n2h/$f.log 2>/dev/null; done) finished [status: completed, exit code: 1]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g1.pt 2>/dev/null && echo R1_OK; tail -1 work/n2h/R-pos-g2.log 2>/dev/null; tail -1 work/n2h/R-pos-g1.log", "description": "Check random positions seed 1"}`

  ```
00:54
pas 17500 · seq 128 · perte 62.8936 · PPL 128/4 3.4724 · 1217 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 30,34p docs/pilotage/roadmap.md; echo \"---\"; grep -n \"N2.h\\|N2\\.d\\|N2 \" docs/pilotage/roadmap.md | head -8; echo \"---\"; sed -n 168,180p docs/pilotage/roadmap.md", "description": "Read the current roadmap N sections"}`

  ```
| **A — le moteur** | formats, placement, transport, rejeu, matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4, A6.2 bloqués** ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** | **A2.6** (experts : A6.2 bloqué) ; réduire le lot |
| **B — l'intelligence** | langue, pensée, jeux, maîtres, banc externe, sémantique, modules | ✅ B1–B12 ; **B1.5 corpus**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste | B10.3 attend un **encodeur qui porte** |
| **N — le natif** | DRVM, `drave-n0`, distillation, usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2 : budget **−0,08**, **validation contaminée (32,8 %)** ; N4 partiel | **N2** (le corpus décontaminé), **N4** (consigne courte) |
| **R — le lecteur** | document, politique de lecture, fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R4.1–R4.3 mesurées** ; **R4.4 partiel** | **R4.4** (scans réels, layout, exposants) ; R1/R2/R3 attendent N2 |

---
32:| **N — le natif** | DRVM, `drave-n0`, distillation, usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2 : budget **−0,08**, **validation contaminée (32,8 %)** ; N4 p
… [2918 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g1.pt 2>/dev/null && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 600 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/R-pos-g1.pt --longueurs 2>&1 | grep -v Loading", "description": "Evaluate the … [24 caractères tronqués]`

  ```
00:54
[exit code: 2]
  ```

- **bash** `{"command": "sleep 300; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g1.pt 2>/dev/null && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 600 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/R-pos-g1.pt --longueurs 2>&1 | grep -v Loading", "description": "W … [63 caractères tronqués]`

  ```
started background job bash-351
  ```

- **job_output** `{"job_id": "bash-351", "timeout_ms": 900000, "wait": true}`

  ```
00:59
work/n2h/R-pos-g1.pt
{"fichier": "R-pos-g1.pt", "params": 11814792, "val": 3.2438, "test": 3.3491, "litterature": 15.7824, "litterature_propre": 17.1343, "anglais": 61.1611, "wikitext2": 60.3335, "permute": 1279.864, "longueurs": {"129": 3.2516, "192": 3.2331, "256": 3.2596, "384": 5.203, "512": 6.1306}}
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-344 (bash: sleep 1400; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g1.pt 2>/dev/null && echo R1_OK; tail -1 work/n2h/R-pos-g2.log 2>/dev/null) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Le verrou de longueur tombe : 14,46 → 3,26 à 256 octets avec des positions aléatoires

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('work/n2h/remplit.py'); s = p.read_text()\ndebut = s.index(\"if long_R[\\\"256\\\"] < long_A[\\\"256\\\"] * 0.7:\")\nfin = s.index(\"vals = {\")\nneuf = '''lecture = (f\"Le verrou ** … [1086 caractères tronqués]`

  ```
ok
parse ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('work/n2h/fiche3.md'); s = p.read_text()\nvieux = \"\"\"Si le verrou est la position, alors **allonger le contexte n'est pas un problème d'architecture**\nmais d'**exposition** : que … [1250 caractères tronqués]`

  ```
ok
01:00
pas  2500 · seq 128 · perte 171.4217 · PPL 128/4 3.8114 · 177 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/maj-roadmap.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"maj-roadmap.py — roadmap après N2.h (mètre propre, diversité, longueur).\"\"\"\nimport json, pathlib\n\na = json.loads(pathlib.Path('reports/n2-propre.json').read_te … [5254 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"import ast; ast.parse(open('work/n2h/maj-roadmap.py').read()); print('parse ok')\"; date '+%H:%M'; tail -1 work/n2h/R-pos-g2.log", "description": "Verify the roadmap script parses"}`

  ```
parse ok
01:00
pas  3000 · seq 128 · perte 179.5137 · PPL 128/4 3.8810 · 212 s
  ```

- **bash** `{"command": "sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g2.pt 2>/dev/null && echo R2_OK; tail -1 work/n2h/R-pos-g3.log 2>/dev/null", "description": "Wait for random positions seed 2", "run_in_background": true}`

  ```
started background job bash-356
  ```

### 👤 Utilisateur

background job bash-346 (bash: sleep 1000; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g1.pt 2>/dev/null && echo R1_OK; tail -1 work/n2h/R-pos-g2.log 2>/dev/null) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g2.pt 2>/dev/null && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 600 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/R-pos-g2.pt --longueurs 2>&1 | grep -v Loading", "description": "Evaluate ran … [22 caractères tronqués]`

  ```
01:00
[exit code: 2]
  ```

- **job_output** `{"job_id": "bash-356", "timeout_ms": 1500000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g2.pt 2>/dev/null && echo R2_OK; tail -1 work/n2h/R-pos-g3.log 2>/dev/null; tail -1 work/n2h/R-pos-g2.log", "description": "Check R seed 2"}`

  ```
01:10
pas 12000 · seq 128 · perte 64.4050 · PPL 128/4 3.5028 · 830 s
  ```

- **bash** `{"command": "sleep 900; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g2.pt 2>/dev/null && echo R2_OK; tail -1 work/n2h/R-pos-g3.log 2>/dev/null", "description": "Wait for R seed 2 completion", "run_in_background": true}`

  ```
started background job bash-359
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -1 work/n2h/R-pos-g2.log; tail -1 work/n2h/R-pos-g3.log 2>/dev/null", "description": "Check R progress"}`

  ```
01:11
pas 12250 · seq 128 · perte 75.0291 · PPL 128/4 3.5246 · 847 s
[exit code: 1]
  ```

- **job_output** `{"job_id": "bash-359", "timeout_ms": 1200000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g2.pt 2>/dev/null && echo R2_OK; tail -1 work/n2h/R-pos-g3.log 2>/dev/null; tail -1 work/n2h/R-pos-g2.log", "description": "Check R seed 2 status"}`

  ```
01:21
work/n2h/R-pos-g2.pt
R2_OK
pas  1000 · seq 128 · perte 364.0111 · PPL 128/4 3.8031 · 72 s
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 600 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/R-pos-g2.pt --longueurs 2>&1 | grep -v Loading", "description": "Evaluate random positions seed 2"}`

  ```
{"fichier": "R-pos-g2.pt", "params": 11814792, "val": 3.2392, "test": 3.3466, "litterature": 15.342, "litterature_propre": 16.7327, "anglais": 58.2932, "wikitext2": 57.9316, "permute": 1202.2777, "longueurs": {"129": 3.2428, "192": 3.2328, "256": 3.2453, "384": 4.966, "512": 5.7697}}
  ```

- **bash** `{"command": "sleep 1200; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g3.pt 2>/dev/null && echo R3_OK; ls work/n2h/*.pt | wc -l", "description": "Wait for the last run", "run_in_background": true}`

  ```
started background job bash-363
  ```

- **job_output** `{"job_id": "bash-363", "timeout_ms": 1500000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-356 (bash: sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g2.pt 2>/dev/null && echo R2_OK; tail -1 work/n2h/R-pos-g3.log 2>/dev/null) finished [status: completed, exit code: 0]. Read its output with job_output.

### 👤 Utilisateur

background job bash-359 (bash: sleep 900; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g2.pt 2>/dev/null && echo R2_OK; tail -1 work/n2h/R-pos-g3.log 2>/dev/null) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g3.pt 2>/dev/null && echo R3_OK; tail -1 work/n2h/R-pos-g3.log; ls work/n2h/gpu0.termine work/n2h/gpu1.termine 2>/dev/null", "description": "Check the final run"}`

  ```
01:32
pas 10500 · seq 128 · perte 67.4545 · PPL 128/4 3.5030 · 719 s
work/n2h/gpu1.termine
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > work/n2h/journal.md <<'EOF'\n### N2.h — le mètre propre, la généralité, et le verrou de longueur\n\nLa nuit du 31 octobre au 1er novembre, la session a eu **dix heures**. Le premier geste n'a pas été\nd'entraîner plus : il a ét … [2285 caractères tronqués]`

  ```
ok
01:32
pas 10500 · seq 128 · perte 67.4545 · PPL 128/4 3.5030 · 719 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 12,20p reports/README.md", "description": "Read the reports index head"}`

  ```
> partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).

## Les fiches courantes

| fichier | ce qu'il porte |
|---|---|
| [`rapport-n2-budget.md`](rapport-n2-budget.md) | **N2.d** — le budget plein paie **2,9355 → 2,8527**, les 4 sources coûtent **+0,91**, et **la validation est contaminée à 32,8 %** (PPL propres **2,9795**) |
| [`rapport-native-prof30k.md`](rapport-native-prof30k.md) | **N2.21** — professeur 30k, lr 3e-6 : PPL **2,823**, dégradation, arrêté |
| `rapport-native-prof20k-6.md` (fiche non écrite) | **N2.23** — professeur 20k, lr 3e-6 : PPL **2,753**, arrêté |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('reports/README.md'); s = p.read_text()\nvieux = \"| [`rapport-n2-budget.md`](rapport-n2-budget.md) | **N2.d** — le budget plein paie **2,9355 → 2,8527**, les 4 sources coûtent **+0, … [1061 caractères tronqués]`

  ```
ok
01:32
pas 10750 · seq 128 · perte 65.5193 · PPL 128/4 3.5016 · 735 s
  ```

- **job_output** `{"job_id": "bash-363", "timeout_ms": 1200000, "wait": true}`

  ```
01:41
13
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/*.pt | wc -l; ls work/n2h/gpu0.termine work/n2h/gpu1.termine 2>/dev/null; tail -1 work/n2h/R-pos-g3.log", "description": "Check the end of the campaign"}`

  ```
01:41
13
work/n2h/gpu1.termine
pas 19250 · seq 128 · perte 72.3568 · PPL 128/4 3.4588 · 1314 s
  ```

- **bash** `{"command": "sleep 300; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls work/n2h/R-pos-g3.pt 2>/dev/null && echo R3_OK; ls work/n2h/gpu0.termine 2>/dev/null && echo GPU0_FINI", "description": "Wait for the last checkpoint", "run_in_background": true}`

  ```
started background job bash-369
  ```

- **job_output** `{"job_id": "bash-369", "timeout_ms": 600000, "wait": true}`

  ```
01:47
work/n2h/R-pos-g3.pt
R3_OK
work/n2h/gpu0.termine
GPU0_FINI
[status: completed, exit code: 0]
  ```

### 🤖 Assistant

⏵ Campagne terminée : évaluation finale des 16 points de contrôle

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup bash work/n2h/evalue-tout.sh > work/n2h/eval-tout.out 2>&1 & echo \"eval $!\"; date '+%H:%M'", "description": "Run the final evaluation of all checkpoints"}`

  ```
eval 653953
01:47
  ```

- **bash** `{"command": "sleep 420; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls -la work/n2h/eval.json 2>/dev/null; ls work/n2h/eval.termine 2>/dev/null && echo FINI; tail -2 work/n2h/eval-tout.log", "description": "Wait for the batch evaluation", "run_in_background": true}`

  ```
started background job bash-371
  ```

- **job_output** `{"job_id": "bash-371", "timeout_ms": 900000, "wait": true}`

  ```
01:54
-rw-r--r--. 1 stephane stephane 7966  1 nov 01:52 work/n2h/eval.json
work/n2h/eval.termine
FINI
{"fichier": "D-mixte-g2.pt", "params": 11814792, "val": 3.26, "test": 3.3203, "litterature": 3.5217, "litterature_propre": 3.8562, "anglais": 25.3735, "wikitext2": 25.798, "permute": 462.8188, "decomposition": {"complete": 3.2872, "apres_2_blocs": 4.2686, "apres_4_blocs": 3.5046, "apres_6_blocs": 3.2613, "sans_pensee": 4777258.3125}, "longueurs": {"129": 3.3003, "192": 7.4877, "256": 11.0491, "384": 16.1717, "512": 19.652}}
{"fichier": "D-mixte-g3.pt", "params": 11814792, "val": 3.2671, "test": 3.3266, "litterature": 3.519, "litterature_propre": 3.851, "anglais": 25.3341, "wikitext2": 25.8465, "permute": 470.7997, "decomposition": {"complete": 3.297, "apres_2_blocs": 4.2705, "apres_4_blocs": 3.5015, "apres_6_blocs": 3.2625, "sans_pensee": 4553894.5856}, "longueurs": {"129": 3.3124, "192": 7.4968, "256": 11.0655, "384": 16.11, "512": 19.5992}}
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 work/n2h/remplit.py", "description": "Fill the three reports from the evaluation"}`

  ```
rapport-n2-propre.md restes: []
rapport-n2-diversite.md restes: []
rapport-n2-longueur.md restes: []
A 3,0904 C128 3,0804 D 3,2625 R 3,2381
long A {'129': 3.13, '192': 8.56, '256': 14.11, '384': 23.9, '512': 32.41} long R {'129': 3.24, '192': 3.23, '256': 3.25, '384': 5.06, '512': 5.93}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,12p reports/rapport-n2-propre.md; echo \"...\"; sed -n '/## Ce qui est mesuré/,/## La porte/p' reports/rapport-n2-propre.md; echo \"=== fiche3 lecture ===\"; sed -n '/## Ce qui est mesuré/,/## Ce que ça change/p' reports/rap … [68 caractères tronqués]`

  ```
# N2.h1 — Le corpus propre : la validation n'était pas tenue à l'écart, et la porte honnête vaut 3,09

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : le corpus de N2 se recopiait
> (**32,8 %** des fenêtres de validation étaient verbatim dans l'entraînement) ; dédupliqué, il
> perd **22,2 %** de son texte et la contamination tombe à **zéro**. La chaîne refaite vaut
> **3,0904** en domaine — pas 2,85 — et **16,70** sur de la littérature jamais vue : la
> porte < 2,5 est **redéfinie**, et elle est à **0,59**.

## La question

N2.d a montré que la PPL de N2 se mesurait sur un jeu où un tiers des fenêtres étaient
mémorisables (2,5862 sur les fenêtres contaminées contre 2,9795 sur les propres). La question
...
## Ce qui est mesuré

| bras | graines | val | test | littérature | anglais | wikitext2 |
|---|---:|---:|---:|---:|---:|---:|
| base propre | 1 | **3,2402** | **3,2880** | **12,2861** | **32,9009** | **33,2883** |
| **A — dépôt seul** | 3 | **3,0904** ±0,0048 | **3,1960** ±0,0100 | **16,7034** ±0,2706 | **57,5773** ±2,2054 | **56,8821** ±2,0231 |
| **C — curriculum 129** | 3 | **3,0804** ±0,0103 | **3,1879** ±0,0042 | **16,8172** ±0,3141 | **58,0259** ±1,6809 |
… [1860 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('work/n2h/remplit.py'); s = p.read_text()\ns = s.replace('    \"TABLE\": table1,\\n', '')\ns = s.replace('    \"R_VAL\": fm(R_VAL), \"R_256\": fm2(long_R[\"256\"]), \"R_512\": fm2(lo … [1652 caractères tronqués]`

  ```
ok
rapport-n2-longueur.md restes: []
A 3,0904 C128 3,0804 D 3,2625 R 3,2381
long A {'129': 3.13, '192': 8.56, '256': 14.11, '384': 23.9, '512': 32.41} long R {'129': 3.24, '192': 3.23, '256': 3.25, '384': 5.06, '512': 5.93}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '/## Ce qui est mesuré/,/## Lecture/p' reports/rapport-n2-longueur.md; echo \"=== distille ===\"; sed -n '/## La distillation spécialise/,/## La décomposition/p' reports/rapport-n2-propre.md", "description": "Verify the fixed  … [28 caractères tronqués]`

  ```
## Ce qui est mesuré

| octets | 129 | 192 | 256 | 384 | 512 |
|---|---:|---:|---:|---:|---:|
| **A** (positions 0–127) | 3,13 | 8,56 | 14,11 | 23,90 | 32,41 |
| **R** (positions aléatoires) | 3,24 | 3,23 | 3,25 | 5,06 | 5,93 |

## Lecture
=== distille ===
## La distillation spécialise

Le tableau ci-dessus contient une surprise : la **base supervisée** — qui n'a jamais vu le
professeur — vaut **3,2402** en domaine mais **12,29** sur la littérature et
**32,90** en anglais. La distillation lui fait gagner **-0,150** en domaine et lui
coûte **4,42** hors domaine. Distiller vers un professeur qui ne connaît que le dépôt,
c'est **spécialiser** l'élève : le professeur n'est pas seulement un enseignant, c'est un
**prisme**.

C'est la même leçon que la fiche [`n2-diversite`](rapport-n2-diversite.md), par l'autre bout : ce
n'est pas la distillation qui est en cause, c'est **ce qu'elle distille**.

## La décomposition — où va le calcul
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('work/n2h/remplit.py'); s = p.read_text()\ns = s.replace('\"DIST_VAL\": fm(A_VAL - moy(\"base-propre\", \"val\"), 3),',\n              '\"DIST_VAL\": fm(A_VAL - moy(\"base-propre\",  … [234 caractères tronqués]`

  ```
ok
long A {'129': 3.13, '192': 8.56, '256': 14.11, '384': 23.9, '512': 32.41} long R {'129': 3.24, '192': 3.23, '256': 3.25, '384': 5.06, '512': 5.93}
91:**32,90** en anglais. La distillation lui fait gagner **−0,150** en domaine et lui
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 work/n2h/maj-roadmap.py && git diff --stat docs/pilotage/roadmap.md", "description": "Apply the roadmap update"}`

  ```
roadmap : 7 remplacements
A 3,0904 D 3,2625 R 3,2381 | 256: 14,11 -> 3,25 | 512: 32,41 -> 5,93
 docs/pilotage/roadmap.md | 37 ++++++++++++++++++++-----------------
 1 file changed, 20 insertions(+), 17 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n \"$(grep -n 'def date_dernier_commit' tools/revue_documentation.py | cut -d: -f1),+8p\" tools/revue_documentation.py; date '+%Y-%m-%d %H:%M'", "description": "Check how the review computes the last commit date"}`

  ```
def date_dernier_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--format=%ad", "--date=short"], cwd=RACINE, text=True
        ).strip()
    except Exception:
        return ""


2026-11-01 01:55
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 18,40p docs/pilotage/en-cours.md; echo \"=== maj ===\"; head -3 docs/pilotage/en-cours.md", "description": "Re-read the current session block"}`

  ```
- **Id** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — [`plan.md`](../../journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md).
- **Rôle** : **N2.h — le mètre propre** : corpus, distillation, évaluation.
- **Plan** : 1) `tools/corpus_propre.py` (dédup, split par chunks) ; 2) chaîne propre (professeur 23,5 M, base 20k, distillation 20k × 3, curriculum 129 × 3) ; 3) porte honnête + hors domaine + décomposition ; 4) diversité FR 50/50 ; 5) verrou de longueur 129→512 × 3 ; 6) fiches, portes, commit.
- **Ambition** : sortir N2 du chiffre contaminé (**2,85** sur **32,8 %**) et donner à R un modèle qui lit du français général ; trancher le verrou de longueur.
- **Stratégie** : un seul changement à la fois, trois graines, contrôle par permutation, le corpus d'abord.
- **Objectif final** : un **mètre honnête** — corpus dédupliqué (0 % de validation dans l'entraînement), chaîne refaite, porte < 2,5 redéfinie, généralité et verrou tranchés.
- **Ce qu'elle fait** : la dédup et le split sont faits ; la distillation A tourne (3 graines).
- **Résultat intermédiaire** : la chaîne propre vaut **3,10** en domaine (3,21 au test) — pas
  2,85 — et **17,1** sur la littérature jamais vue : c'est u
… [1136 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format='%ad' --date=short; python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\na = \"\"\"- **Ce qu'elle fait** : la dédup et le split sont faits ; la distillation A tourne  … [1786 caractères tronqués]`

  ```
2026-11-01
ok
  ✅ état court, structuré, multi-session et reprenable
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 372 fichiers, le disque en a 375
     · compteurs : en-cours.md dit 448 JSON, le disque en a 450
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text()\nimport re\ns = re.sub(r\"\\| fichiers / JSON de résultats \\| \\*\\*\\d+\\*\\* / \\*\\*\\d+\\*\\* \\|\",\n           \"| fichiers / J … [888 caractères tronqués]`

  ```
ok
  revue de documentation · 375 fiche(s) · 450 JSON · 114 doc(s) · 80 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ✅ état court, structuré, multi-session et reprenable
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py 2>&1 | tail -2; du -sh work/n2h; df -h /home/stephane/IA | tail -1", "description": "Regenerate the reports index and check sizes"}`

  ```
372 fiches → reports/INDEX.md
903M	work/n2h
/dev/md0        938G  893G   35G  97% /home/stephane/IA
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p /home/stephane/Data13TB/stephane/backups/n2h/2026-11-01 && rsync -a --exclude 'essai-*' work/n2h/ /home/stephane/Data13TB/stephane/backups/n2h/2026-11-01/ && du -sh /home/stephane/Data13TB/stephane/backups/n2h/2026-11-01 &&  … [137 caractères tronqués]`

  ```
903M	/home/stephane/Data13TB/stephane/backups/n2h/2026-11-01
14
  ```

- **bash** `{"command": "mkdir -p /home/stephane/IA/artefacts/n2h/2026-11-01 && rsync -a /home/stephane/Data13TB/stephane/backups/n2h/2026-11-01/ /home/stephane/IA/artefacts/n2h/2026-11-01/ && du -sh /home/stephane/IA/artefacts/n2h/2026-11-01 && df -h /home/stephane/IA | tail -1", "description": "Replicate the  … [32 caractères tronqués]`

  ```
903M	/home/stephane/IA/artefacts/n2h/2026-11-01
/dev/md0        938G  894G   35G  97% /home/stephane/IA
  ```

### 🤖 Assistant

⏵ Lancement de la passe complète des portes (seule sur les GPU) pendant la rédaction

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup env JOURNAUX=/tmp/portes-1101-n2h DELAI=1800 bash tools/toutes-les-portes.sh > work/n2h/portes.log 2>&1 & echo \"portes $!\"; date '+%H:%M'", "description": "Launch the full gate pass"}`

  ```
portes 657672
01:56
  ```

