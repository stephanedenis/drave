# Session DSH — relecture

- identifiant : `session-0ad92682-0d71-421c-be45-3c35e875bb07`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 23:33:46
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche T6 (clôture) : le bilan — relis les fiches T1-T5, écris `reports/rapport-bilan-exploitable.md` + JSON : ce qui est désormais installable, le quickstart, l'API du JSON, la performance, les codes de sortie ; les négatifs ; ce qui reste (le gold de S, les signatures de Panini, la décision du tagger `auto`) ; mets à jour `docs/pilotage/en-cours.md` et la roadmap. **Ne relance pas la passe complète** : lis `work/portes/`.

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

- **bash** `{"command": "pwd; ls; echo ---; ls work/ 2>/dev/null | head -50; echo ---; ls work/portes/ 2>/dev/null | head -50", "description": "List workspace and work/portes"}`

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
atomes_cohortes.py
attente_portes.sh
banc-performance
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
msg-tag-semaine-2.txt
msg-w5.txt
msg-w6.txt
n2ac
n2d
n2h
n2i
n2j
n2k
n2w
---
b1-protocole-03h03
passe-0303-04h10
passe-0303-11h30
passe-1102-19h32
passe-1102-apres-n2
passe-1104-08h00
passe-1311-23h15
passe-1311-23h15.log
pa
… [162 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | head -100; echo ---; ls docs/pilotage/ | head -50", "description": "List reports and pilotage docs"}`

  ```
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
a83b-regimes.json
a83c-ctx.json
a83c-lot.json
a83-defaut.json
a83d-lot-threads.json
aiguille-30b.md
aiguille-gpt-oss.md
alignement-3b.json
alignement-7b.json
alignement-verne.md
analyse-litteraire.json
archive
atomes-niveaux.json
atomes-prediction.json
atomes-prediction-mesures.json
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeur-mots.json
b10-mots-contraste.json
b10-mots-jw.json
b1110-audit.json
b1110b-hybride.json
b1110-cartes.json
b1110c-case.json
b13-porte-134.json
b13-porte-138.json
b13-porte-140.json
bilan
… [1197 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i -E 't[1-5]|t-|install|exploit|bilan' | head -60; echo '--- glob'; find . -iname '*t1*' -o -iname '*t2*' -o -iname '*t3*' -o -iname '*t4*' -o -iname '*t5*' 2>/dev/null | grep -v node_modules | grep -v '.git/' | head -60", "description": "Find T1-T5 fiches"}`

  ```
a26-bilan.json
a26-lot-disque.json
a80-audit-final.json
a83d-lot-threads.json
aiguille-gpt-oss.md
alignement-3b.json
alignement-7b.json
alignement-verne.md
bilan-b11.md
bilan-multi-materiel.md
bruit-entree.json
cca-raisonnement-3b.json
contrat-json.json
corpus-litt-propre.json
corpus-wiki-it-texte-contamination.json
corpus-wiki-it-texte.json
corpus-wiki-pt-texte-contamination.json
corpus-wiki-pt-texte.json
fiche-nuit-17-10.md
kfold-chat-0210.json
kfold-tout-0210.json
m6-conflit2.json
marqueurs-bruit-3b.json
native-best-2.json
native-best-service.json
native-sft-eval.json
pensee-anaphore-bilan.json
pensee-attachement-cible.json
pensee-attachement-parfait.json
pensee-attachement-v2.json
pensee-attachement-v3.json
pensee-audit-attachement.json
pensee-audit-r1r3.json
pensee-audit-v10.json
pensee-audit-v2.json
pensee-audit-v7.json
pensee-autotest-parallele.json
pensee-bilan-nuit.json
pensee-classement-appris.json
pensee-contrat-s.json
pensee-cout-chunker.json
pensee-defaut-conditionnel.json
pensee-defaut-niveau.json
pensee-dev-test-v10.json
pensee-dev-test-v7.json
pensee-etat-a.json
pensee-etat-n2.json
pensee-etat-r.json
pensee-etat-s.json
pensee-produit-bloc-l.json
pensee-produit-v0.js
… [6045 caractères tronqués]
  ```

- **bash** `{"command": "for d in work/portes/*/; do echo \"== $d\"; ls \"$d\" | head -20; done 2>/dev/null | head -120", "description": "Inspect work/portes contents"}`

  ```
== work/portes/b1-protocole-03h03/
porte-bloc-tableaux.log
porte-document.log
porte-registre.log
porte-tableaux.log
registre.txt
== work/portes/passe-0303-04h10/
deepseek-porte
jeux-mesures.json
langues-mesures.json
maitres-mesures.json
porte-adaptateur-sortie.log
porte-audit-drapeaux.log
porte-b1110-hybride.log
porte-balayage.log
porte-bloc-code.log
porte-bloc-linguistique.log
porte-bloc-maths.log
porte-bloc-tableaux.log
porte-budget.log
porte-bus.log
porte-bus-socket.log
porte-c4-retard.log
porte-cerveau.log
porte-consolidation.log
porte-coupe.log
porte-cycle-c2.log
== work/portes/passe-0303-11h30/
deepseek-porte
jeux-mesures.json
langues-mesures.json
maitres-mesures.json
porte-adaptateur-sortie.log
porte-audit-drapeaux.log
porte-b1110-hybride.log
porte-balayage.log
porte-bloc-code.log
porte-bloc-linguistique.log
porte-bloc-maths.log
porte-bloc-tableaux.log
porte-budget.log
porte-bus.log
porte-bus-socket.log
porte-c4-retard.log
porte-cerveau.log
porte-consolidation.log
porte-coupe.log
porte-cycle-c2.log
== work/portes/passe-1102-19h32/
deepseek-porte
jeux-mesures.json
langues-mesures.json
maitres-mesures.json
porte-adaptateur-sortie.log
porte-audit-drapeaux.log
porte-b1110-hybrid
… [1365 caractères tronqués]
  ```

- **bash** `{"command": "grep -rl --include='*.md' -iE '\\bT[1-5]\\b' reports docs journal work 2>/dev/null | head -40", "description": "Find docs mentioning T1-T5"}`

  ```
reports/rapport-modele-drave.md
reports/rapport-pensee-v0.md
reports/rapport-pensee-ac3-alphabeta.md
reports/rapport-pensee-drvf.md
reports/rapport-audit-r1r3.md
reports/rapport-inventaire-panini.md
reports/rapport-schema-v2-doc.md
reports/rapport-cloture-chantier.md
reports/rapport-faq-sommaire.md
reports/rapport-empaquetage.md
reports/rapport-contrat-json.md
reports/rapport-quickstart.md
reports/rapport-performance.md
reports/rapport-cli-robuste.md
docs/methode/contexte.md
docs/pilotage/roadmap.md
docs/pilotage/en-cours.md
docs/theorie/glossaire/README.md
docs/implantation/format-flux.md
docs/implantation/format-clusters.md
docs/implantation/moteur-de-pensee.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md
journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/rapport.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
journal/sessions/e7dfe34f-d596-4f98-93c2-cad5a92d3b1e/rapport.md
journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md
journal/sessions/7d0d2578-0048-4998-8494-7d2daef56769/rapport.md
journal/se
… [700 caractères tronqués]
  ```

- **bash** `{"command": "ls -lt reports/*.md | head -30; echo ---; ls -lt work/chantier/ 2>/dev/null | head -30; echo ---; ls -lt journal/ | head", "description": "List newest report md and chantier"}`

  ```
-rw-r--r--. 1 stephane stephane  10317 15 nov 23:26 reports/rapport-cli-robuste.md
-rw-------. 1 stephane stephane  10520 15 nov 23:20 reports/rapport-faq.md
-rw-r--r--. 1 stephane stephane  16768 15 nov 23:13 reports/rapport-performance.md
-rw-------. 1 stephane stephane  13131 15 nov 22:31 reports/rapport-quickstart.md
-rw-------. 1 stephane stephane  11992 15 nov 22:02 reports/rapport-schema-v2-doc.md
-rw-r--r--. 1 stephane stephane  12095 15 nov 22:00 reports/rapport-contrat-json.md
-rw-------. 1 stephane stephane   9445 15 nov 21:49 reports/rapport-empaquetage.md
-rw-r--r--. 1 stephane stephane 105423 15 nov 15:01 reports/INDEX.md
-rw-------. 1 stephane stephane  20389 15 nov 14:25 reports/rapport-tagger-auto.md
-rw-r--r--. 1 stephane stephane  24224 15 nov 14:10 reports/README.md
-rw-r--r--. 1 stephane stephane   3803 15 nov 14:10 reports/rapport-bilan-jour-1115.md
-rw-------. 1 stephane stephane  21708 15 nov 13:36 reports/rapport-tagger-lot.md
-rw-r--r--. 1 stephane stephane  19473 15 nov 12:52 reports/rapport-or-roles-protocole.md
-rw-r--r--. 1 stephane stephane  27746 15 nov 12:40 reports/rapport-page-s-mesure.md
-rw-r--r--. 1 stephane stephane  28110 15 nov 12:34 reports
… [2732 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -iE 'T[1-5][ :—-]' docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-empaquetage.md reports/rapport-contrat-json.md 2>/dev/null | head -40", "description": "Search T-task references in pilotage"}`

  ```
docs/pilotage/en-cours.md:3:**Mis à jour : 2026-11-15, 23 h 23 HNE (T5 : la CLI robuste — `--duree`, codes 0/3/4/5, aide, `--fichier`)**
docs/pilotage/en-cours.md:66:- **Prochaine action** : **T6 — le bilan** ; **J4 — l'or de rôles** ; T132/T133 ; **T4 : borner `_groupes_partition` et `_cible_proche`** (O(k²)).
docs/pilotage/roadmap.md:32:| **N — le natif** | DRVM, `drave-n0`, [distillation](../theorie/glossaire/entrees/distillation.md), usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; **N0.1 6/6** ; N2.h : 3,0904 domaine, 3,85 hors dépôt ; **N2.ac (1 Go) : 3,49 / 6,03 / 8,34 — production** ; **200 k pas : val_fr 3,16, littérature 5,61, anglais 7,28, wikitext2 8,00** ; **fenêtre 1 024 : 2,4759 / 2,4373 au grand corpus — sous 2,5** ; porte propre **2,7856** ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 partiel | **N2** : **clôturée** le 03/11 11 h 25, la **fenêtre est la recette de production** ; **paire propre de distillation** (04/11) ; puis la **porte propre (0,29)** ; **N4** |
docs/pilotage/roadmap.md:38:**État au 15/11.** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** 
… [5526 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' docs/pilotage/en-cours.md", "description": "Read en-cours beginning"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 23 h 23 HNE (T5 : la CLI robuste — `--duree`, codes 0/3/4/5, aide, `--fichier`)**

> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
- **Prochaine action** : **suivi docs**, puis la **passe**.
- **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état
… [11199 caractères tronqués]
  ```

- **bash** `{"command": "for f in rapport-empaquetage rapport-contrat-json rapport-quickstart rapport-performance rapport-cli-robuste; do echo \"########## $f\"; head -c 300 \"reports/$f.md\"; echo; echo \"--- json?\"; ls reports/*.json | grep -iE 'empaquet|contrat|quickstart|performance|cli' ; done", "descript … [40 caractères tronqués]`

  ```
########## rapport-empaquetage
# T1 — l'empaquetage : `pip install -e .`, `drave` hors du dépôt, chemin historique intact

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T1** (exploitable, 1/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **empaquetage minimal livré**.
>
> **Le chiffre.** `pyproject.toml` : 
--- json?
reports/cli-robuste.json
reports/contrat-json.json
reports/empaquetage.json
reports/pensee-contrat-s.json
reports/performance.json
reports/performance-profil.json
reports/quickstart.json
########## rapport-contrat-json
# T2 — l'API du JSON : candidats d'attachement en objets, rôles normalisés

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T2** (exploitable, 2/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **contrat livré et mesuré**.
>
> **Le chiffre.** Sur le gold vivant **612 phrases** :
--- json?
reports/cli-robuste.json
reports/contrat-json.json
reports/empaquetage.json
reports/pensee-contrat-s.json
reports/performance.json
reports/performance-profil.json
reports/quickstart.json
########## rapport-quickstart
# T3 — le démarrage en 5 minutes : clone public, installation, trois commandes, JSON, tagger, erreurs

> **Ligne de roadmap** : **B13*
… [1384 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -15; echo ---; git status --short | head -40", "description": "Git log and status"}`

  ```
9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS
7e195ee6 T4 — CORRECTION DE LA FICHE : LE POINT 4 000 MOTS A PLUS DE SYNTAGMES (1 075 CONTRE 1 006) ET VA PLUS VITE ; LE TEMPS NE SUIT PAS LES MOTS SEULS
7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))
7d114559 T3 — LE DÉMARRAGE EN 5 MINUTES : 3/3 COMMANDES REJOUÉES, JSON V2 5 899 OCTETS, TAGGER 4/0, ERREURS 3/4/1 ; LE CLONE PUBLIC SANS tools/structures EST DÉGRADÉ, DOCUMENTÉ
7f1519f7 T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 ACCENTUÉ)
71fdf72c CLÔTURE — LE PLAN (51 TÂCHES) ET LE PROTOCOLE OR-ROLES (X2) COMMITTÉS ; L'ÉTAT HORODATÉ
c9067a39 INDEX — RÉGÉNÉRÉ APRÈS LA SEMAINE 2 (W1-W6, X1-X3, Y1)
b8248b2d ÉTAT — T0 VERT (LA LIGNE W5 RACCOURCIE)
75dc9259 ÉTAT — T0 VERT
a1c45477 ÉTAT — T0 TENU (LES LIGNES R ET N RACCOURCIES)
f706aec0 Y1 — LE MODE AUTO DU TAGGER DOCUMENTÉ : L'API SI LA CLÉ EXISTE, L'HEURISTIQUE
… [1104 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-json.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md</path>
<type>file</type>
<content>
1: # T1 — l'empaquetage : `pip install -e .`, `drave` hors du dépôt, chemin historique intact
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T1** (exploitable, 1/5) ·
4: > **Date** : 2026-11-15 · **Verdict** : ✅ **empaquetage minimal livré**.
5: >
6: > **Le chiffre.** `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,
7: > **0** dépendance d'exécution, script console `drave = tools.drave:main`.
8: > `python3 -m pip install -e .` dans **`/tmp/venv-drave`** (Python **3.13.16**, pip **26.2.1**)
9: > rend **0** et `Successfully installed drave-0.1.0` ; `drave --version` rend **`drave 0.1.0`**
10: > et `drave analyser "Le chat dort."` rend **0** depuis **`/tmp`**. Le **contrôle négatif** —
11: > le même nom sans installation — échoue **proprement** : code **127**, `command not found`,
12: > **aucune** trace Python. Le chemin historique `python3 tools/drave.py` reste **vert**.
13: >
14: > **Dispositif** : [`pyproject.toml`](../pyproject.toml),
15: > [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py),
1
… [9003 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-json.md</path>
<type>file</type>
<content>
1: # T2 — l'API du JSON : candidats d'attachement en objets, rôles normalisés
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T2** (exploitable, 2/5) ·
4: > **Date** : 2026-11-15 · **Verdict** : ✅ **contrat livré et mesuré**.
5: >
6: > **Le chiffre.** Sur le gold vivant **612 phrases** : **1 883 syntagmes**, **1 883 rôles**
7: > non vides, **21 rôles bruts** ramenés à **8 rôles normalisés**, **0** hors table et **0**
8: > hors vocabulaire. Les **1 295 attachements** portent tous des `candidats` **objets**
9: > `{span, cible, source}` : **2 139 objets** (dont **1 062** dans `meta.alternative`),
10: > **0 span faux**, **1 295/1 295** cibles choisies présentes dans la liste. **Contrôle
11: > négatif** : un consommateur qui filtre `role == "predicat"` trouve **711** prédicats
12: > (**711 GV**) ; `role == "prédicat"` en trouve **0**. Le schéma v2 valide **612/612**
13: > annotations, les **612** v1 dérivées restent lues, et v2 refuse **612/612** v1.
14: >
15: > **Dispositif** : [`mesurer_contrat_json.py`](../tools/mesurer_contrat_json.py),
16: > [`r
… [11788 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-quickstart.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-quickstart.md</path>
<type>file</type>
<content>
1: # T3 — le démarrage en 5 minutes : clone public, installation, trois commandes, JSON, tagger, erreurs
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T3** (exploitable, 3/5) ·
4: > **Date** : 2026-11-15 · **Verdict** : ✅ **quickstart livré et rejoué** ; ⚠️ le **clone
5: > public** n'a pas le sous-module `tools/structures`, donc la sortie d'un débutant est
6: > **dégradée** par rapport au dépôt de développement. Le document le dit, mesure l'écart et
7: > donne les deux sorties.
8: >
9: > **Le chiffre.** Sur un clone public neuf (commit **7f1519f**, Python **3.13.16**, pip
10: > **26.2.1**, sans clé) : **3/3 commandes** sortent **0**, le JSON fait **5 899 octets** en
11: > schéma **v2**, `--tagger` sans clé sort **4**, `--tagger auto` sort **0**, et les **3
12: > erreurs** rejouées sortent **3 / 4 / 1**. Clone + venv + installation : **13,64 s** de
13: > machine. Le contrôle négatif « un débutant sans le dépôt » passe pour les commandes, mais
14: > découvre l'écart du sous-module : `analyser` rend `rôle=objet` / `GV → —` au lieu de
15: > `agent` 
… [12872 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md</path>
<type>file</type>
<content>
1: # T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T4** (exploitable, 4/5) ·
4: > **Date** : 2026-11-15 · **Verdict** : ✅ **les 10 000 mots sont exploitables** (4,0 s de
5: > fonction, 2 493 mots/s, 126 Mio de pic RSS, 14,8 Mo de JSON) ; ❌ **le contrôle négatif de
6: > linéarité échoue** — le temps croît en **α = 1,55** sur un bloc contrôlé, et le terme
7: > quadratique explique **R² 0,99995** contre **0,957** pour le linéaire. Le coupable est
8: > nommé : `_groupes_partition` (toutes les paires de syntagmes, O(k²)) et `_cible_proche`
9: > (tri de tous les GV pour chaque segment), pas la tokenisation.
10: >
11: > **Les chiffres.** Sur le préfixe exact de **10 000 mots** de
12: > `data/corpus_fr_litterature.txt` (Alice, français), versionné dans
13: > [`reports/performance-corpus-10000.txt`](performance-corpus-10000.txt)
14: > (sha256 `0069b20e28975ca7b504755456aacf014b864b16705d40e6b381c45ae5e08871`,
15: > 57
… [16813 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cli-robuste.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cli-robuste.md</path>
<type>file</type>
<content>
1: # T5 — la robustesse de la CLI : `--duree`, cinq codes de sortie, aide des quatre sous-commandes, `--fichier` sans trace
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T5** (exploitable, 5/5) ·
4: > **Date** : 2026-11-15 · **Verdict** : ✅ **20/20 cas mesurés**, **30 tests** de fumée
5: > verts (dont **6** ajoutés pour T5), aucune trace Python sur les chemins d'erreur.
6: >
7: > **Le chiffre.** `--duree` ajoute `cout.duree_s` au JSON de `analyser` — **4,7 à 5,6 ms**
8: > mesurés sur « Le chat dort. », **5,9 ms** sur la phrase longue — et **ne change rien
9: > d'autre** : texte, étiquettes et durée par défaut sont identiques. Les **cinq codes**
10: > sont désormais **0 succès / 3 refus / 4 clé ou dépendance / 5 usage / 1 autre erreur** ;
11: > les deux erreurs de `--fichier` sortent **4** (chemin inexistant) et **5** (répertoire),
12: > avec un message d'une ligne et **0 trace**. `--aide` et `--help` sortent **0** sur les
13: > **quatre** sous-commandes.
14: >
15: > **Dispositif** : [`tools/banc_cli_robuste.py`](../tools/banc_cli_robuste.py),
1
… [9887 caractères tronqués]
  ```

- **bash** `{"command": "for f in reports/empaquetage.json reports/contrat-json.json reports/quickstart.json reports/performance.json reports/cli-robuste.json; do echo \"===== $f\"; python3 -c \"import json,sys; d=json.load(open('$f')); print(json.dumps(d,ensure_ascii=False,indent=1)[:3000])\"; done", "descript … [37 caractères tronqués]`

  ```
===== reports/empaquetage.json
{
 "schema": "drave.empaquetage.verification",
 "version": 1,
 "date": "2026-11-15",
 "tache": "T1 (exploitable, 1/5)",
 "produit": "0.1.0",
 "pyproject": {
  "fichier": "pyproject.toml",
  "nom": "drave",
  "version": "0.1.0",
  "requires_python": ">=3.10",
  "dependances": [],
  "script_console": "drave = tools.drave:main",
  "build_backend": "setuptools.build_meta",
  "build_requires": [
   "setuptools>=61"
  ],
  "packages": [
   "tools"
  ]
 },
 "environnement": {
  "venv": "/tmp/venv-drave",
  "python": "3.13.16",
  "pip": "26.2.1",
  "commande": "python3 -m pip install -e .",
  "cwd": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet",
  "code": 0,
  "resultat": "Successfully installed drave-0.1.0",
  "editable": true,
  "pip_show": {
   "name": "drave",
   "version": "0.1.0",
   "requires": [],
   "editable_project_location": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"
  }
 },
 "sorties": {
  "drave_version": {
   "commande": "drave --version",
   "cwd": "/tmp",
   "code": 0,
   "stdout": "drave 0.1.0"
  },
  "drave_analyser": {
   "commande": "drave analyser \"Le chat dort.\"",
   "cwd": "/tmp",
   "code": 0,
   "stdout_extrait": [
    "
… [13460 caractères tronqués]
  ```

- **bash** `{"command": "ls -ldt work/portes/*/ | head -20; echo ---; for d in $(ls -dt work/portes/*/ | head -6); do echo \"== $d\"; ls \"$d\" | grep -E 'registre|passe' ; done", "description": "Find latest gate run directories"}`

  ```
drwxr-xr-x. 1 stephane stephane  364 15 nov 12:24 work/portes/w6-final/
drwxr-xr-x. 1 stephane stephane   88 15 nov 12:15 work/portes/w6-ciblage2/
drwxr-xr-x. 1 stephane stephane  364 15 nov 12:11 work/portes/w6-ciblage/
drwxr-xr-x. 1 stephane stephane  178 15 nov 03:03 work/portes/b1-protocole-03h03/
drwxr-xr-x. 1 stephane stephane  190 14 nov 07:12 work/portes/verif-cloture/
drwxr-xr-x. 1 stephane stephane 3512 14 nov 03:48 work/portes/passe-1402-02h00/
drwxr-xr-x. 1 stephane stephane 3512 14 nov 01:00 work/portes/passe-1311-23h15/
drwxr-xr-x. 1 stephane stephane 3478  5 nov 01:54 work/portes/passe-2404-23h45/
drwxr-xr-x. 1 stephane stephane 1080  4 nov 08:31 work/portes/passe-1104-08h00/
drwxr-xr-x. 1 stephane stephane 3432  3 nov 13:07 work/portes/passe-0303-11h30/
drwxr-xr-x. 1 stephane stephane 3432  3 nov 05:42 work/portes/passe-0303-04h10/
drwxr-xr-x. 1 stephane stephane 3392  2 nov 21:13 work/portes/passe-1102-19h32/
drwxr-xr-x. 1 stephane stephane   22  2 nov 16:45 work/portes/passe-1102-apres-n2/
drwxr-xr-x. 1 stephane stephane  316  2 nov 16:35 work/portes/sous-passe-1102-16h35/
---
== work/portes/w6-final/
porte-registre.log
registre.txt
== work/portes/w6-ciblage2/
reg
… [230 caractères tronqués]
  ```

- **bash** `{"command": "ls -lt work/portes/verif-cloture 2>/dev/null | head; echo ---; find work/portes -maxdepth 1 -name 'registre.txt' -printf '%T@ %p\\n' 2>/dev/null | sort -nr | head -20; echo ---; ls -lt work/ | head -20", "description": "Find registre files and recent work"}`

  ```
total 24
-rw-r--r--. 1 stephane stephane  212 14 nov 07:12 revue.log
-rw-r--r--. 1 stephane stephane    2 14 nov 07:08 porte-indice.code
-rw-r--r--. 1 stephane stephane 2135 14 nov 07:08 porte-indice.log
-rw-r--r--. 1 stephane stephane    2 14 nov 06:56 porte-melange.code
-rw-r--r--. 1 stephane stephane  661 14 nov 06:56 porte-melange.log
-rw-r--r--. 1 stephane stephane  295 14 nov 06:54 porte-sessions.log
---
---
total 240
drwxr-xr-x. 1 stephane stephane   562 15 nov 23:13 banc-performance
drwxr-xr-x. 1 stephane stephane   290 15 nov 21:37 chantier
drwxr-xr-x. 1 stephane stephane   178 15 nov 13:34 tagger-lot
drwxr-xr-x. 1 stephane stephane  3538 15 nov 13:18 portes-w5
drwxr-xr-x. 1 stephane stephane    20 15 nov 12:35 page-s-mesure
drwxr-xr-x. 1 stephane stephane   584 15 nov 12:23 portes
-rw-r--r--. 1 stephane stephane  1790 15 nov 12:20 msg-w6.txt
-rw-r--r--. 1 stephane stephane   518 15 nov 12:20 msg-tag-semaine-2.txt
-rw-r--r--. 1 stephane stephane  1277 15 nov 12:08 msg-w5.txt
drwxr-xr-x. 1 stephane stephane  3396 15 nov 12:02 portes-1115-09h53
drwxr-xr-x. 1 stephane stephane   930 15 nov 09:39 portes-1115-09h22
drwxr-xr-x. 1 stephane stephane  1078 15 nov 07:09 portes-1115-
… [490 caractères tronqués]
  ```

- **bash** `{"command": "for f in work/portes/w6-final/registre.txt work/portes/w6-ciblage2/registre.txt work/portes-1115-09h53/registre.txt work/portes-1115-09h22/registre.txt; do echo \"===== $f\"; wc -l \"$f\"; awk '$2 != 0' \"$f\" | head -20; echo \"-- total $(wc -l < \"$f\") / rouges $(awk '$2 != 0' \"$f\" … [77 caractères tronqués]`

  ```
===== work/portes/w6-final/registre.txt
10 work/portes/w6-final/registre.txt
--- 9 vertes, 0 rouges ---
-- total 10 / rouges 1
===== work/portes/w6-ciblage2/registre.txt
3 work/portes/w6-ciblage2/registre.txt
--- 2 vertes, 0 rouges ---
-- total 3 / rouges 1
===== work/portes-1115-09h53/registre.txt
86 work/portes-1115-09h53/registre.txt
porte-indice 1 1149
porte-melange 1 137
porte-prechargement 1 258
porte-sessions 1 0
--- 81 vertes, 4 rouges ---
-- total 86 / rouges 5
===== work/portes-1115-09h22/registre.txt
22 work/portes-1115-09h22/registre.txt
-- total 22 / rouges 0
  ```

- **bash** `{"command": "for d in work/portes/w6-final work/portes-1115-09h53; do echo \"== $d\"; ls \"$d\" | head -5; head -20 \"$d/registre.txt\"; done", "description": "Preview registre format"}`

  ```
== work/portes/w6-final
porte-bloc-linguistique.log
porte-bloc-tableaux.log
porte-document.log
porte-etat.log
porte-lecteur.log
porte-bloc-linguistique 0 17
porte-bloc-tableaux 0 2
porte-document 0 7
porte-etat 0 0
porte-lecteur 0 1
porte-lecture 0 2
porte-registre 0 18
porte-sessions 0 0
porte-tableaux 0 1
--- 9 vertes, 0 rouges ---
== work/portes-1115-09h53
porte-adaptateur-sortie.log
porte-audit-drapeaux.log
porte-b1110-hybride.log
porte-balayage.log
porte-bloc-code.log
porte-adaptateur-sortie 0 76
porte-audit-drapeaux 0 177
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 16
porte-bloc-linguistique 0 16
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 50
porte-bus 0 83
porte-bus-socket 0 104
porte-c4-retard 0 35
porte-cerveau 0 10
porte-cic 0 13
porte-consolidation 0 91
porte-coupe 0 156
porte-cycle-c2 0 147
porte-deepseek 0 0
porte-delais 0 25
porte-diff-couche 0 21
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md</path>
<type>file</type>
<content>
1: # Références de non-régression
2: 
3: > **Passe — 2026-11-15 09 h 53 → 12 h 15 :** **85 portes, 81 vertes, 4 rouges** — `indice` et
4: > `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prechargement`
5: > **environnementale** (deux passes en parallèle ; PPL identique 799,8557 ; verte le 14/11).
6: > Journaux `work/portes-1115-09h53/`. **Pas de passe complète pour W6** ; ciblage
7: > `work/portes/w6-ciblage` (8/9), `w6-ciblage2` (2/2) puis `w6-final` (9/9).
8: 
9: > **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
10: > `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
11: > `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
12: > `work/portes/passe-1311-23h15.log`.
13: >
14: > **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
15: > heartbeat `e181ce02` rafraîchi) ; `porte-indice` et `porte-melange` restent **rouges
16: > structurelles** (indice 482 contre témoin 459 ; état de A san
… [13577 caractères tronqués]
  ```

- **bash** `{"command": "cat work/portes-1115-09h53/registre.txt | tail -8; echo ---; for p in porte-indice porte-melange porte-prechargement porte-sessions; do echo \"== $p\"; tail -12 \"work/portes-1115-09h53/$p.log\" 2>/dev/null; done", "description": "Inspect the four red gates"}`

  ```
porte-sessions 1 0
porte-speculatif 0 81
porte-tableaux 0 1
porte-tokenizer-kimi 0 7
porte-topologie 0 135
porte-trace 0 32
porte-vision 0 676
--- 81 vertes, 4 rouges ---
---
== porte-indice
  écho     indice SÉMANTIQUE : l'état de la question, position 1469, aiguille en 669 :
  écho       épisode rendu : 1469 · recouvrement 64/64 · distance à l'aiguille : 800 jetons
  écho       hasard        : 370 jetons en moyenne sur 1470 épisodes
  écho       ⇒ la mémoire n'a PAS retrouvé l'aiguille : un indice qui ne ressemble pas au contenu cherché ne le retrouve pas. C'est une limite du rappel par le contenu — il n'est pas sémantique —, et elle est mesurée, pas supposée.
  écho   
  extérieur   indice SÉMANTIQUE : EXTÉRIEUR (/tmp/tmp.aHQw1tyS32/etatB.1439, 896 valeurs) — il n'est PAS dans le magasin, aiguille en 669 :
  extérieur     épisode rendu : 187 · recouvrement 4/64 · distance à l'aiguille : 482 jetons
  extérieur     hasard        : 370 jetons en moyenne sur 1470 épisodes
  extérieur     ⇒ la mémoire n'a PAS retrouvé l'aiguille : un indice qui ne ressemble pas au contenu cherché ne le retrouve pas. C'est une limite du rappel par le contenu — il n'est pas sémantique —, et elle est me
… [2082 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -iE 'empaquetage|contrat-json|quickstart|performance|cli-robuste|T1|T2|T3|T4|T5|exploitable' reports/README.md reports/INDEX.md docs/pilotage/roadmap.md | head -80", "description": "Locate T1-T5 references in indexes and roadmap"}`

  ```
reports/INDEX.md:81:| [rapport-b13-porte-138.md](rapport-b13-porte-138.md) | B13 — la porte est à 138/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 restent |
reports/INDEX.md:82:| [rapport-b13-porte-140.md](rapport-b13-porte-140.md) | B13 — la porte est à 140/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 alignés sur 2/5 (distracteurs r428–r432) |
reports/INDEX.md:251:| [rapport-m6-conflit2.md](rapport-m6-conflit2.md) | B26 — le conflit M6 reste à zéro |
docs/pilotage/roadmap.md:31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule*
… [12000 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/roadmap.md", "description": "Read roadmap beginning"}`

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
… [19922 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -iE 'gold de S|gold S|l.or de rôles|J4' reports docs/pilotage | head -60", "description": "Search gold S and J4"}`

  ```
reports/multilingue.json:26619:  "Corpus construit par le code : les attendus et les contextes viennent des mêmes règles que le codec. Ce n'est pas un gold standard indépendant ; le contrôle permuté est la seule vérification externe de la liaison surface → code.",
reports/rapport-r03-banc-durci.md:27:  gold sont repris tels quels, seule la formulation change) ;
reports/rapport-n2-distillation-reelle.md:1:# N2.j4 — La distillation sur le corpus réel : 4,39 → 3,88, et tout le reste baisse
reports/rapport-n2-distillation-reelle.md:57:  professeur 23,57 M, distillation 3 graines, positions conservées (N2.j4) → **3,88** en domaine,
reports/rapport-n2-anglais-distille.md:44:  question de la distillation « de qualité » (les fiches N2.h/N2.j4 utilisent un professeur de
reports/rapport-n2-multilingue-distille.md:11:N2.k avait mesuré la dilution (fr +57 %, en −1,7 PPL face au monolingue) ; N2.n et N2.j4 ont montré
reports/rapport-n2-fenetre-r1.md:18:   (N2.j4, N2.n) : à 512, la distillation ne gagne rien (5,67 → 5,76) parce que le professeur a la
reports/rapport-n2-34m-distille.md:12:N2.j4 a montré que la distillation paie sur 11,47 M. La question : les deux **se composent-ils**, et
reports/
… [7622 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -iE '26 signatures|signatures|V14|reste|bloqu' reports/rapport-panini-manifeste.md | head -40; echo ====; grep -n -iE 'décision|decision|humain|reste|auto' reports/rapport-tagger-auto.md | head -60", "description": "Search Panini signatures and tagger auto decisions"}`

  ```
1:# W4 — Panini : le manifeste des 26 signatures V14 et le rejeu disponible
10:> [`../tools/panini_signatures_26.py`](../tools/panini_signatures_26.py) · **Rejeu** :
17:les **60** paires, **27** ont leurs deux signatures (1 G1, 14 G2, 12 G3) : on les décrit, on ne
20:contrôle des signatures montre que l'instrument voit la **famille** sur G2 mais pas la date, et la
21:**calibration échoue sur 2 des 44 œuvres** : le test est **bloqué**, pas « non significatif ».
26:  descriptif** de ce qui est signé, les **contrôles négatifs** exécutables, et ce qui bloque.
90:  mais ces trois signatures sont **hors du support des 44 références** : elles ne peuvent pas être
96:  sont byte-identiques à `qiwulun`, **déjà signé** ; leur signature est donc déjà connue. Il reste
107:Le script est [`../tools/panini_signatures_26.py`](../tools/panini_signatures_26.py). Il fait deux
108:choses dans le **même** passage : (1) il re-extrait les **44** signatures de référence et vérifie
115:  /chemin/vers/Qtrinet/tools/panini_signatures_26.py \
117:  --sortie /tmp/panini-v14-26.json
122:- La commande écrit `/tmp/panini-v14-26.json`. **C'est ce fichier que Panini renvoie** (ou dépose
123:  dans un dossier partagé
… [10362 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -iE 'gold|or de rôles|reste|manque|prochaine' reports/rapport-page-s-mesure.md | head -60; echo =====; sed -n '1,80p' reports/rapport-page-s-mesure.md", "description": "Read S page measurement report relevant parts"}`

  ```
41:- **Public** : la session S (prochaine action : spécifier la migration et les référents), le
138:attachement**, **46 des 99** candidats profonds reçoivent un verdict migré ; **53** restent à
139:juger. Après normalisation des espaces + attachement, **47/99**. Le reste de la profondeur est
276:forcés). Le `14/14` de la fiche de traduction reste un résultat **côté anglais**, pas une
436:  couverture et de référents changent ; c'est précisément l'objet de la prochaine session.
=====
# La page `/` de S : 369/0 contre 359/99 — la recette, et pourquoi « 0 » n'est pas « zéro verdict »

> **Ligne de roadmap** : S · **Tâche** : X1 / J4 après-midi (la part du pilote) · **Date** :
> 2026-11-15 12 h 37 HNE · **HEAD parent mesuré** : `049343d3` · **Sous-module
> `tools/structures`** : `389b99f` · **Verdict** : la page `/` sert **toujours l'ancien banc** —
> **369 candidats**, **0 avec `profondeur`**, **0 à ≥ 3**, distribution des `niveau` **10 / 277 /
> 82** — alors que la v7 dynamique donne **359 candidats**, **2 / 37 / 221 / 84 / 13 / 2** et
> **99 à ≥ 3**. Le **106 conservés / 41 en quarantaine** de la v2 est **reproduit à la lettre**
> (signature exacte), mais la signature nue ne donne q
… [4683 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -iE 'gold de S|gold S|or de rôles|gold de rôles|gold 60|gold 144' docs reports journal | head -50", "description": "Search exact gold S phrasing"}`

  ```
docs/pilotage/backlog/R02-controleur-lecture.md:41:- les spans gold sont dans les titres et le contrôleur les lit sans comprendre
docs/pilotage/plan-travail.md:365:| **S** `29ad180d` | `tools/structures/`, `docs/schemas/arbre-referents.svg`, `reports/s-*` | **v6** (h050, h053, « si fort que » fermés, gold 60) ; la **validation des paragraphes** sur `/paragraphes` ; la **rétro-traduction** API | `cpu1` 4, `ram` 8 | fiches + tests verts + commit | validation faite ou report nommé |
docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (4/5 familles ≥ 90 %) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) ; **W2 — tagger 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), fermé 402 −1,55** ([fiche](../../reports/rapport-tagger-h50.md)) ; **W3 — matrice du tagger** ([fiche](../../reports/rapport-tagger-defaut.md)) ; **W5 — restitution v3 : gold S 144/144, cinq rôles 18/18, permutation 0/18 ; `--roles-v3` opt-in** ([fiche](../../reports/rapport-rest
… [11125 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,120p' docs/pilotage/semaine-2.md; echo =====; grep -n -iE 'gold S|144|18/18|reste|limite' reports/rapport-restitution-v3.md | head -40", "description": "Read J4 plan and restitution v3 gold S facts"}`

  ```
mesure est : **défaut hors ligne**, `--tagger` **opt-in**, un mode `auto` seulement si la clé
existe et sans changer le code de sortie. J2 fournit le coût et les cas d'erreur ; J5 applique ou
rejette.

## 2 bis. L'état par jour (constaté le 15/11)

> **Le calendrier a bougé, pas le périmètre.** Les cinq vagues **W1–W5** ont été exécutées le
> **15/11** ; le plan les plaçait du **16 au 20/11**. Le tag porte la **date cible**
> `2026-11-20`. **J4** (or de rôles, recette `/`) n'est **pas ouvert** : S est en pause et l'or de
> rôles manque. **J5 matin** (la décision du tagger) est **appliquée par W3** — défaut hors ligne,
> `--tagger` opt-in, pas de `auto` — sans vague séparée.

| jour | vague | état | chiffre / preuve | suite |
|---|---|---|---|---|
| **J1 · 16/11** | **W1** — le gold réel 452 | ✅ **fait** (15/11) | **452** = 20 hand + 432 corpus ; split **402/H50** ; **184 → 194** cibles ; sha256 identique ; 0 « 200+ » | W2 prend le split |
| **J2 · 17/11** | **W2** — le tagger 402/H50 | ✅ **fait, réserve fermée** | 402 **0,9198 → 0,9643** (+4,45) ; H50 **0,6842 → 0,8607** (+17,65) ; F1/att 402 inchangés ; fermé **−1,55** | W3 décide du défaut |
| **J2 · 17/11** | **W3** — la matrice
… [8689 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-restitution-v3.md; echo =====; sed -n '1,50p' reports/rapport-tagger-auto.md; echo =====; sed -n '245,290p' reports/rapport-panini-manifeste.md", "description": "Read openings and blocking sections"}`

  ```
# B13 — la restitution v3 : les rôles des GP se séparent, la fidélité du cadre ne suit pas

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : W5 (J3 après-midi) · **Date** :
> 2026-11-15 · **Verdict** : **positif sur la séparation, négatif sur le produit** — les
> cinq rôles de GP se séparent sur le gold S (**18/18**, **144/144**, permutation **0/18**),
> mais le gold v2 ne gagne qu'un cadre : **20/46** contre 19/46, F1 **0,5406** contre
> 0,5270, `lieu` F1 **0,60** contre 0,40. La fidélité du cadre ne suit pas : le goulot est
> la segmentation et le choix du cadre, pas la préposition.
>
> **La question.** La v2 lisait la préposition seule (`à` → destinataire, `de` → thème,
> `avec` → moyen) ; le `lieu` restait son rôle le plus faible (F1 0,4000). La v3 peut-elle
> distinguer **lieu / temps / destinataire / possession / complément** avec le contexte, et
> la précision/rappel par rôle le montrent-ils sur les deux ors existants — le gold v2
> (46) et le gold S (61 phrases, 144 rôles) — sans que la mesure soit un rôle constant ?
>
> **La réponse.** Oui pour la **règle** : `_role_gp` sépare les cinq catégories avec le
> contexte (ce qui suit la préposition, ce qui la précède), *
… [9405 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/*bilan*.json reports/*semaine*.json 2>/dev/null; echo ---; python3 -c \"\nimport json\nfor f in ['reports/bilan-chantier.json','reports/semaine-2.json']:\n    try:\n        d=json.load(open(f)); print(f, list(d)[:20]); print(json.dumps(d,ensure_ascii=False,indent=1)[:2000])\n … [92 caractères tronqués]`

  ```
reports/a26-bilan.json
reports/pensee-anaphore-bilan.json
reports/pensee-bilan-nuit.json
reports/pensee-robustesse-semaine.json
reports/rapport-bilan-chantier.json
reports/rapport-semaine-2.json
reports/rapport-semaine.json
---
reports/bilan-chantier.json [Errno 2] No such file or directory: 'reports/bilan-chantier.json'
reports/semaine-2.json [Errno 2] No such file or directory: 'reports/semaine-2.json'
  ```

- **bash** `{"command": "grep -n -iE 'code|sortie|exit' docs/produit/README.md | head -30; echo ---; sed -n '1,80p' docs/produit/demarrage.md", "description": "Check product README codes and quickstart"}`

  ```
14:> existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
18:> reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
141:large) : dans la sortie lisible, elle apparaît comme un **doublon REL** ; le JSON la marque
239:(l'ancienne sortie). Le défaut est `alternative`.
262:| `debut`, `fin` | entiers | `0 ≤ debut < fin` | span en **points de code Unicode**, 0-based, `[debut:fin)` |
267:| `retire` | booléen | optionnel | présent en vue `filtrer`/`filtrer_union` ; `true` = segment retiré de la sortie mais toujours lisible ici |
275:| `span` | objet | `{debut, fin}`, `0 ≤ debut < fin` | position de la cible dans `texte`, en points de code Unicode, fin exclue |
281:liste de chaînes : c'est la sortie lisible, et le contrat v1 ne connaît que lui.
374:python3 tools/drave.py analyser ""; echo "exit=$?"
378:exit=3
383:code **3**, distinct des autres erreurs (1) et de l'usage (5). Le message reste sur `stderr`. Un texte
402:              des mots et des POS ; une sortie n'est fidèle que si elle reproduit exactement
413:surfaces exactes**, miroir strict **0,1087**, contrôle négatif **46/46**. C'est un **codec de
414:s
… [4280 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nfor f in ['reports/rapport-semaine-2.json','reports/rapport-bilan-chantier.json']:\n    d=json.load(open(f)); print('=====',f); print(list(d)[:30]); print(json.dumps(d,ensure_ascii=False,indent=1)[:2500])\n\"", "description": "Inspect report JSON schemas"}`

  ```
===== reports/rapport-semaine-2.json
['schema', 'version', 'titre', 'date', 'date_cible', 'tache', 'lignes_roadmap', 'statut', 'base', 'vagues', 'negatifs', 'decisions', 'portes', 'tag', 'reste', 'limites', 'fichiers', 'verdict']
{
 "schema": "drave.rapport-semaine.v2",
 "version": 1,
 "titre": "W6 — le rapport de la semaine 2 : le tagger gagne sur les deux bases, Panini reste bloqué, la restitution sépare sans fidélité",
 "date": "2026-11-15",
 "date_cible": "2026-11-20",
 "tache": "W6",
 "lignes_roadmap": [
  "R0.7",
  "B13",
  "L"
 ],
 "statut": "cloture",
 "base": {
  "gold_phrases": 452,
  "gold_sources": {
   "hand": 20,
   "corpus": 432
  },
  "gold_langues": {
   "fr": 242,
   "en": 210
  },
  "gold_tokens": 2480,
  "gold_segments": 1501,
  "gold_cibles": 184,
  "gold_cibles_apres_annotation": 194,
  "split": "402 / H50",
  "h50_phrases": 50,
  "h50_tokens": 323,
  "h50_cibles": 22,
  "commits": {
   "W1": "4dbeff45",
   "W2": "1683c2b4",
   "W3": "be3f41ad",
   "W4": "93e046f7",
   "W5": "73edb3dd"
  },
  "head_mesure": "73edb3dd",
  "note": "Aucune mesure nouvelle : ce rapport relit les fiches W1-W5 et les journaux de portes."
 },
 "vagues": {
  "W1": {
   "tache": "le go
… [4282 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '150,180p' docs/pilotage/roadmap.md; echo ====; sed -n '280,310p' docs/pilotage/roadmap.md", "description": "Read roadmap T4 section and B13 table row"}`

  ```
**J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag `chantier-2026-11-14`.** La
passe du **14/11 00 h 30** (`work/portes/passe-1311-23h15.log`) n'est **pas refaite** : les trois
rouges sont **revérifiées**. `porte-sessions` passe **verte** après la mise en pause du hub
`1e7ef596` et le rafraîchissement du heartbeat `e181ce02` ; `porte-indice` et `porte-melange`
restent **rouges structurelles** (mêmes causes : écart au témoin nul pour l'indice ; état de A qui
ne rend pas son code pour le mélange). Le tag annoté `chantier-2026-11-14` est posé sur le dernier
commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +
[`JSON`](../../reports/rapport-cloture-chantier.json).
**Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le
gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).

**T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
**14,8 Mo** JSON ; 100 phrases **1,10 ms** ; `--tagger` **1,17 s/phrase**.
**Contrôle de linéarité négatif** : **α = 1,55**, **R² 0,99995** ;
`_groupes_parti
… [7263 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -iE '\\bT6\\b|exploitable' docs/pilotage reports/rapport-file-taches.md tools/chantier/plan.json 2>/dev/null | head -50", "description": "Find T6 task in plan"}`

  ```
docs/pilotage/en-cours.md:66:- **Prochaine action** : **T6 — le bilan** ; **J4 — l'or de rôles** ; T132/T133 ; **T4 : borner `_groupes_partition` et `_cible_proche`** (O(k²)).
tools/chantier/plan.json:744:   "mandat": "Tâche T1 (exploitable, 1/5) : **l'empaquetage** — écris un **`pyproject.toml`** minimal (le nom `drave`, la version 0.1.0, le `requires-python >= 3.10`, **aucune dépendance**, le `console_scripts` `drave = tools.drave:main` ou un module d'entrée propre), vérifie `python3 -m pip install -e .` dans un **venv temporaire** (`/tmp/venv-drave`), puis `drave --version` et `drave analyser \"Le chat dort.\"` depuis un **autre répertoire** (pas la racine du dépôt) ; le contrôle négatif : sans install, `drave` doit échouer proprement. Fiche `reports/rapport-empaquetage.md` + JSON, un test dans `tools/tests/` (ou une note), et la doc `docs/produit/README.md` § 8.10 mise à jour (l'install). **Ne casse pas** `python3 tools/drave.py` (le chemin historique).",
tools/chantier/plan.json:761:   "mandat": "Tâche T2 (exploitable, 2/5) : **l'API du JSON** — (1) les `candidats` de l'attachement deviennent des **objets** `{span, cible, source}` au lieu des chaînes d'affichage (le schéma v2 
… [3618 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='tools/chantier/plan.json'\nd=json.load(open(p))\nprint(type(d), list(d)[:10] if isinstance(d,dict) else len(d))\ns=json.dumps(d,ensure_ascii=False)\nimport re\nfor m in re.finditer(r'.{300}T6.{500}', s):\n    print(m.group(0)); print('---')\nPY", "descr … [34 caractères tronqués]`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
-robuste.md` + JSON, un test par cas dans `tools/tests/test_produit.py`.", "budget_min": 90, "acceptation": [{"commande": "test -f reports/rapport-cli-robuste.md && echo FICHE-OK", "attendu": "FICHE-OK"}, {"commande": "python3 tools/tests/test_produit.py 2>&1 | tail -1", "attendu": "OK"}]}, {"id": "T6", "jour": 19, "titre": "Le bilan de la nuit exploitable", "mandat": "Tâche T6 (clôture) : le bilan — relis les fiches T1-T5, écris `reports/rapport-bilan-exploitable.md` + JSON : ce qui est désormais installable, le quickstart, l'API du JSON, la performance, les codes de sortie ; les négatifs ; ce qui reste (le gold de S, les signatures de Panini, la décision du tagger `auto`) ; mets à jour `docs/pilotage/en-cours.md` et la roadmap. **Ne relance pas la passe complète** : lis `work/portes/`.", "
---
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='tools/chantier/plan.json'\nd=json.load(open(p))\nfor t in d['taches']:\n    if t.get('id') in ('T6','U1','U2','U3','T7'):\n        print(json.dumps(t,ensure_ascii=False,indent=2))\nPY", "description": "Show T6 and following task details"}`

  ```
{
  "id": "T6",
  "jour": 19,
  "titre": "Le bilan de la nuit exploitable",
  "mandat": "Tâche T6 (clôture) : le bilan — relis les fiches T1-T5, écris `reports/rapport-bilan-exploitable.md` + JSON : ce qui est désormais installable, le quickstart, l'API du JSON, la performance, les codes de sortie ; les négatifs ; ce qui reste (le gold de S, les signatures de Panini, la décision du tagger `auto`) ; mets à jour `docs/pilotage/en-cours.md` et la roadmap. **Ne relance pas la passe complète** : lis `work/portes/`.",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f reports/rapport-bilan-exploitable.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    }
  ]
}
{
  "id": "U1",
  "jour": 20,
  "titre": "La performance — les deux points quadratiques",
  "mandat": "Tâche U1 (exploitable, suite de T4) : **répare les deux points O(k²)** identifiés par T4 — `_groupes_partition` (toutes les paires de syntagmes) et `_cible_proche` (le tri de tous les GV pour chaque segment) — **sans changer les résultats** (les 612 phrases et le réel 452 : les mêmes F1, attachement, POS, au bit près) ; mesure le **α** de la croissance avant/après sur le bloc contrôlé de T4 (l'objectif : α ≤
… [1976 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn '764\\|859\\|125' tools/revue_documentation.py docs/pilotage/en-cours.md | head -20; echo ---; sed -n '1,80p' tools/revue_documentation.py", "description": "Inspect revue_documentation counters"}`

  ```
docs/pilotage/en-cours.md:104:| fichiers / JSON de résultats | **764** / **859** | `reports/*.md` / `reports/*.json` |
docs/pilotage/en-cours.md:105:| documents de `docs/` | **125** (hors archive et README) | `docs/**/*.md` |
---
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
  6. vocabulaire : « jeton » ne désigne **jamais** la représentation sémantique neutre (RS
… [2011 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -iE 'rapport-bilan|bilan-exploitable|INDEX|index_reports' tools/revue_documentation.py tools/*.py | head -30", "description": "Find report index tooling"}`

  ```
tools/revue_documentation.py:11:  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
tools/revue_documentation.py:163:            if f.name == "index.json" and f.parent.name == "glossaire":
tools/revue_documentation.py:170:        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")
tools/revue_documentation.py:261:    # 7b bis. les fiches glossaire sont toutes listées dans l'index du dossier
tools/revue_documentation.py:308:    idx = RACINE / "docs/theorie/synthese/index.md"
tools/revue_documentation.py:312:            alertes.append("cohérence : l'index ne dit pas « Huit chapitres »")
tools/revue_documentation.py:319:                alertes.append(f"cohérence : l'index ne mentionne pas {cible}")
tools/revue_documentation.py:326:                alertes.append(f"synthèse : {p.name} n'est pas listé dans l'index")
tools/revue_documentation.py:336:            alertes.append("synthèse : l'index n'a pas de « Dernière mise à jour »")
tools/revue_documentation.py:340:                alertes.append(f"synthèse : index daté {m.group(1)}, dernier changement {dernier}")
tools/revue_documentation.py:349:            alertes.append(f
… [1944 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,240p' tools/revue_documentation.py; echo ====; sed -n '350,430p' tools/revue_documentation.py", "description": "Inspect report nav and counters checks"}`

  ```
def extrait_entier(texte: str, motif: str):
    m = re.search(motif, texte)
    return int(m.group(1)) if m else None


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
    retard = retards(RACINE)
    if retard and not etat_modifie(RACINE):
        etat, _fa
… [5728 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '75,125p' tools/revue_documentation.py; echo ====; sed -n '250,300p' tools/revue_documentation.py; echo ====; grep -n 'def compte_' -A8 tools/revue_documentation.py", "description": "Inspect navigation and counters functions"}`

  ```
def rapports():
    return list((RACINE / "reports").glob("*.md"))


def sources_nav():
    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins)."""
    return (docs_vivants() + rapports()
            + [RACINE / "docs/README.md", RACINE / "README.md",
               RACINE / "REPRISE.md", RACINE / "AGENTS.md"])


def sources_propres():
    """Les documents vivants dont on vérifie les libellés et les chemins en code inline."""
    return (docs_vivants()
            + [RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])


def sources_liens():
    """Les fichiers dont les liens doivent résoudre (docs, fiches courantes, racine)."""
    return (docs_tous()
            + [RACINE / "reports/07-mesures-couche-commune.md",
               RACINE / "reports/fiche-nuit-17-10.md",
               RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])


def compte_portes() -> int:
    return len(list((RACINE / "tools").glob("porte-*.sh")))


def compte_chapitres() -> int:
    return len(list((RACINE / "docs/theorie/synthese").glob("0*.md")))


def compte_fiches() -> int:
    return len(rapports())


def compte_json() -> int:
    return len(l
… [3053 caractères tronqués]
  ```

- **bash** `{"command": "head -40 reports/README.md; echo ====; grep -n 'rapport-performance\\|rapport-cli-robuste\\|rapport-quickstart\\|rapport-empaquetage\\|rapport-contrat-json' reports/README.md | head", "description": "Inspect reports README index format"}`

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
| [`rapport-bilan-jour-1115.md`](rapport-bilan-jour-1115.md) | **Bilan** — le 15/11 : la semaine 2 en un jour, la décision du tagger |
| [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) | **Bilan** — la semaine 07 → 15/11 : le produit, Panini, la coordination, le harnais |
| [`rapport-bilan-nuit.md`](r
… [3040 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'T1\\|T2\\|T3\\|T4\\|T5\\|contrat-json\\|quickstart\\|empaquetage\\|cli-robuste' reports/README.md | head -20; echo ---; wc -l reports/README.md; tail -40 reports/README.md", "description": "Check T-series entries in reports README"}`

  ```
---
230 reports/README.md
| [`rapport-native-ctx256.md`](rapport-native-ctx256.md) | **N2.27** — contexte 256 : PPL **5,675**, arrêté |
| [`rapport-native-local.md`](rapport-native-local.md) | **N2.26** — têtes locales : PPL **2,763**, dégradation |
| [`rapport-native-plafond.md`](rapport-native-plafond.md) | **N2 synthèse** — plafond **2,708**, six essais, porte 2,5 |
| [`rapport-native-prof20k-7.md`](rapport-native-prof20k-7.md) | **N2.24** — T=4 : PPL **2,852**, arrêté |
| `rapport-native-prof30k-2.md` (fiche non écrite) | **N2.22** — professeur 30k, lr 1e-5 : PPL **2,828**, arrêté |
| [`rapport-native-prof20k-5.md`](rapport-native-prof20k-5.md) | **N2.19** — 30 000 pas : PPL **2,708** |
| [`rapport-native-prof20k-4.md`](rapport-native-prof20k-4.md) | **N2.18** — 30 000 pas : PPL **2,714** |
| [`rapport-native-prof20k-3.md`](rapport-native-prof20k-3.md) | **N2.17** — 30 000 pas : PPL **2,726** |
| [`rapport-native-prof20k-2.md`](rapport-native-prof20k-2.md) | **N2.16** — 20 000 pas de plus |
| [`rapport-native-prof20k.md`](rapport-native-prof20k.md) | **N2.14** — professeur 20k : PPL **2,787**, précision |
| [`rapport-native-prof10k-2.md`](rapport-native-prof10k-2.md) | **N2.13*
… [1955 caractères tronqués]
  ```

- **bash** `{"command": "ls tools | grep -i index; echo ---; sed -n '1,40p' tools/index_reports.py 2>/dev/null", "description": "Check index_reports tool"}`

  ```
index_reports.py
index_spans.py
index_wiki_en.py
---
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
        i
… [197 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'T1 —\\|T2 —\\|T3 —\\|T4 —\\|T5 —' reports/INDEX.md | head; echo ---; grep -n 'rapport-empaquetage\\|rapport-contrat-json\\|rapport-quickstart\\|rapport-performance\\|rapport-cli-robuste' reports/INDEX.md | head", "description": "Check T reports in INDEX"}`

  ```
---
  ```

- **bash** `{"command": "echo \"md $(ls reports/*.md | wc -l) json $(ls reports/*.json | wc -l) docs $(python3 -c \"\nimport sys,pathlib\nsys.path.insert(0,'tools')\nfrom revue_documentation import compte_docs, compte_fiches, compte_json, compte_portes\nprint(compte_docs(), compte_fiches(), compte_json(), compt … [82 caractères tronqués]`

  ```
md 764 json 859 docs 125 764 859 86
2026-11-15
  ```

- **bash** `{"command": "ls -l tools/porte-banc-performance.sh 2>/dev/null; grep -n 'banc-performance' work/portes-1115-09h53/registre.txt; echo ---; grep -n 'banc-performance' docs/pilotage/en-cours.md docs/pilotage/references-non-regression.md", "description": "Check new performance gate presence"}`

  ```
-rwxr-xr-x. 1 stephane stephane 3214 15 nov 23:05 tools/porte-banc-performance.sh
---
docs/pilotage/en-cours.md:102:| portes | **86** (dont `porte-banc-performance` le 15/11) | `tools/porte-*.sh` |
  ```

- **bash** `{"command": "sed -n '1,130p' tools/porte-banc-performance.sh", "description": "Read new performance gate"}`

  ```
#!/usr/bin/env bash
# porte-banc-performance — le banc de performance mesure, et son JSON est complet.
#
# Ce qu'elle vérifie : les 12 tests des fondations (préfixe exact, bloc de phrases entières,
# ajustements linéaire/quadratique/log-log, lecture de la ligne TAGGER, extrapolation), puis
# un passage COURT du banc (1 000 mots, 20 phrases, 3 tailles, bloc ×1/×2/×4) hors ligne.
# Elle ne juge PAS le chiffre de performance (il dépend de la machine) : elle vérifie que le
# banc tourne, que le JSON porte les mesures et que le contrôle de linéarité est calculé.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ko=0
dit() { printf '  %s %s\n' "$1" "$2"; }
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

if python3 tools/tests/test_banc_performance.py >"$tmp/tests.log" 2>&1; then
  dit ✅ "tests : $(grep -oE 'Ran [0-9]+ tests' "$tmp/tests.log" | head -1)"
else
  dit ❌ "tests en échec (voir ci-dessous)"; tail -20 "$tmp/tests.log"; ko=1
fi

if timeout 300 python3 tools/banc_performance.py \
     --mots 1000 --phrases-courtes 20 --tailles 250,500,1000 \
     --bloc-repetitions 1,2,4 --repetitions 1 \
     --sortie "$tmp/performance.json" >"$tmp/banc.log" 2>&1; then
  dit ✅ "passage court : $(gre
… [1969 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Get current time"}`

  ```
2026-11-15 23:35 EST
  ```

- **bash** `{"command": "ls journal/2026-11-15/; echo ---; head -50 journal/2026-11-15/README.md 2>/dev/null; echo ---; ls journal/2026-11-15/*.md | head", "description": "Inspect journal day 15/11"}`

  ```
distribue.md
docs.md
memoire.md
mesures.md
modele.md
outils.md
portes.md
README.md
---
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**51 commits** · **1 session(s)** · **7 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 8 | [distribue.md](distribue.md) |
| docs | 14 | [docs.md](docs.md) |
| memoire | 3 | [memoire.md](memoire.md) |
| mesures | 19 | [mesures.md](mesures.md) |
| modele | 3 | [modele.md](modele.md) |
| outils | 1 | [outils.md](outils.md) |
| portes | 3 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 366.8 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réel
… [3539 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'Dernière mise à jour\\|dernière mise à jour' docs/pilotage/roadmap.md; echo ---; grep -n 'T4 — la performance' -A6 docs/pilotage/roadmap.md", "description": "Locate roadmap date and T4 block"}`

  ```
174:L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-11-15 05 h 00**.
---
162:**T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
163-**14,8 Mo** JSON ; 100 phrases **1,10 ms** ; `--tagger` **1,17 s/phrase**.
164-**Contrôle de linéarité négatif** : **α = 1,55**, **R² 0,99995** ;
165-`_groupes_partition`/`_cible_proche` sont **O(k²)**. [Fiche](../../reports/rapport-performance.md) ·
166-[JSON](../../reports/performance.json). Prochaine action : **borner les boucles**.
167-
168-**La vue d'ensemble** est dans [`chantiers.md`](chantiers.md) ; carte,
  ```

- **bash** `{"command": "grep -n 'notes\\|<!--' journal/2026-11-15/README.md | head; tail -60 journal/2026-11-15/README.md", "description": "See journal notes area"}`

  ```
5:> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
86:<!-- notes -->
200:<!-- /notes -->
**+1 appariement**. Le contrôle négatif permute les rôles : cinq rôles **0/18**, tous les rôles
**0,4028**, rôle constant **0,0208**. `--roles-v3` est opt-in ; `--roles` reste la v2.
[`fiche`](../../reports/rapport-restitution-v3.md) · [`JSON`](../../reports/pensee-restitution-v3.json).

### W6 — la clôture : cinq vagues, le tag `semaine-2-2026-11-20`, 85 portes lues

La semaine 2 est close : **W1** gold 452, **W2** tagger 402/H50, **W3** défaut hors ligne,
**W4** Panini bloqué (27/60, calibration 42/44, aucune p-value), **W5** restitution v3
(séparation 18/18, produit 20/46). Le rapport [semaine 2](../../reports/rapport-semaine-2.md) +
[JSON](../../reports/rapport-semaine-2.json) relient les cinq fiches ; le tag annoté
`semaine-2-2026-11-20` est posé sur le dernier commit de code vert `73edb3dd` (W5).
**Aucune passe complète relancée** : le relevé lit `work/portes-1115-09h53` (**85** portes,
**81** vertes, **4** rouges nommées : `indice`, `melange`, `sessions` réparée, `prechargement`
environnementale) et un ciblage **9/9** après heartbeat.

### X3 — le tagge
… [3279 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/porte-banc-performance.sh", "description": "Run new performance gate only", "run_in_background": true}`

  ```
started background job bash-47
  ```

- **bash** `{"command": "sed -n '1,40p' reports/rapport-cloture-chantier.md; echo ====; python3 -c \"\nimport json;d=json.load(open('reports/rapport-cloture-chantier.json'));print(list(d));print(json.dumps(d,ensure_ascii=False,indent=1)[:1800])\"", "description": "Inspect closure report style"}`

  ```
# J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag `chantier-2026-11-14`

> **Ligne de roadmap** : **B13** (le produit), **Panini**, **N2**, **S**, **R**, **A** · **Tâche** :
> J14.1 · **Date** : 2026-11-14 · **Verdict** : ✅
>
> **Ce que ce rapport est.** La **clôture** du chantier, **sans relancer la passe complète** : la
> passe de référence est celle du **14/11 00 h 30** (`work/portes/passe-1311-23h15.log`) —
> **84 portes, 81 vertes, 3 rouges nommées**. J14.1 **rejoue les trois rouges** (`indice`,
> `melange`, `sessions`), met à jour [`references-non-regression.md`](../docs/pilotage/references-non-regression.md),
> pose le **tag annoté** `chantier-2026-11-14` sur le dernier commit vert, et écrit cette fiche.
> Il **ne refait pas** les 81 vertes : ce serait une seconde passe, et le mandat l'interdit.
>
> **Le chiffre.** **84 / 81 / 3** reste le relevé. Après vérification ciblée : `porte-sessions`
> passe **verte** (20 s), `porte-indice` et `porte-melange` restent **rouges structurelles**. Le tag
> `chantier-2026-11-14` est posé sur **`0e75f101`** (J13.1), avec le tag de semaine
> `semaine-2026-11-14` que J5.2 n'avait pas posé : l'échec est **réparé**, pas effa
… [3865 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-47"}`

  ```
✅ tests : Ran 12 tests
[status: running]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable.md", "content": "# T6 — le bilan exploitable : installable, rejouable, mesuré, mais pas encore général\n\n> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **T6** (clôture de la nuit\n> exploit … [21285 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

background job bash-47 (bash: bash tools/porte-banc-performance.sh) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-47"}`

  ```
✅ passage court : 7 étapes
JSON complet : 1000 mots, 20 phrases, 3 points d'échelle, contrôle calculé
  ✅ JSON : contrat et mesures présents
  ✅ mode profil : fonctions dominantes exportées
✅ porte banc-performance verte
[status: completed, exit code: 0]
  ```

- **write** `{"content": "{\n  \"schema\": \"drave.bilan-exploitable\",\n  \"version\": 1,\n  \"titre\": \"T6 — le bilan exploitable : installable, rejouable, mesuré, mais pas encore général\",\n  \"date\": \"2026-11-15\",\n  \"tache\": \"T6\",\n  \"statut\": \"cloture\",\n  \"lignes_roadmap\": [\"B13\", \"R0.7\ … [19347 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-bilan-exploitable.json >/dev/null && echo JSON-OK; python3 - <<'PY'\nimport re\nt=open('reports/rapport-bilan-exploitable.md').read()\nfor lab,c in re.findall(r'\\[([^\\]]+)\\]\\(([^)#]+?)\\)', t):\n    import os\n    p=os.path.normpath(os.path.join( … [201 caractères tronqués]`

  ```
JSON-OK
links checked
  ```

- **bash** `{"command": "grep -n '' docs/pilotage/en-cours.md | sed -n '1,145p'", "description": "Show en-cours with line numbers"}`

  ```
1:# En ce moment
2:
3:**Mis à jour : 2026-11-15, 23 h 23 HNE (T5 : la CLI robuste — `--duree`, codes 0/3/4/5, aide, `--fichier`)**
4:
5:> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
6:
7:### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
8:
9:- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
10:- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
11:- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
12:- **Prochaine action** : **suivi docs**, puis la **passe**.
13:- **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
14:- **Bloquants** : aucun.
15:- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
16:
17:## Sessions en cours
18:
19:> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
20:> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
21:> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
… [11667 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 23 h 23 HNE (T5 : la CLI robuste — `--duree`, codes 0/3/4/5, aide, `--fichier`)**", "new_string": "**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable —  … [91 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../report … [1174 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../.. … [990 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **764** / **859** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **765** / **860** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W … [437 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 150}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 23 h 23 HNE (T5 : la CLI robuste — `--duree`, codes 0/3/4/5, aide, `--fichier`)**
4: 
5: > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
6: 
7: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
8: 
9: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
10: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
11: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
12: - **Prochaine action** : **suivi docs**, puis la **passe**.
13: - **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
14: - **Bloquants** : aucun.
15: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
16: 
17: ## Sessions en cours
18: 
19: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
20: > [`journal/sessions/`](../../journal/sessions/). Ch
… [11970 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable — installable, quickstart, JSON, performance, codes ; passe 85/81/4 lue, 86e porte verte)**", "old_string": "**Mis à jour : 2026 … [91 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../report … [1174 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../.. … [990 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **765** / **860** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **764** / **859** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W … [437 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 (installable, JSON v2, quickstart, performa … [421 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T1–T6 — le produit exploitable est livré** : installable (`pip install -e .`), quickstart **3/3**, JSON v2 (**2 139** objets), 10 000 mots **4,01 s**, CLI **20/20** ; [bilan](../../reports/rap … [1072 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 26, "limit": 18}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 156, "limit": 22}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
26: ## En un coup d'œil
27: 
28: | chantier | ce qu'il couvre | état | prochaine action |
29: |---|---|---|---|
30: | **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
31: | **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs h
… [9161 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
156: commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
157: posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +
158: [`JSON`](../../reports/rapport-cloture-chantier.json).
159: **Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le
160: gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).
161: 
162: **T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
163: **14,8 Mo** JSON ; 100 phrases **1,10 ms** ; `--tagger` **1,17 s/phrase**.
164: **Contrôle de linéarité négatif** : **α = 1,55**, **R² 0,99995** ;
165: `_groupes_partition`/`_cible_proche` sont **O(k²)**. [Fiche](../../reports/rapport-performance.md) ·
166: [JSON](../../reports/performance.json). Prochaine action : **borner les boucles**.
167: 
168: **La vue d'ensemble** est dans [`chantiers.md`](chantiers.md) ; carte,
169: [`chantiers-vision.svg`](../schemas/chantiers-vision.svg) ; plan,
170: [`plan-travail.md`](plan-travail.md).
171: 
172: ## L'ordre du jour (carpe diem)
173
… [481 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\nt=open('docs/pilotage/roadmap.md').read()\nline=t.splitlines()[30]\nprint(len(line))\nfor needle in ['183/183', 'porte 183/183', 'gold 432 réel true', 'R0.7']:\n    i=line.find(needle)\n    print(needle, i, line[max(0,i-200):i+300] if i>=0 else '')\nPY", "de … [37 caractères tronqués]`

  ```
3035
183/183 2204 es longues** + **rôles** + **hybride** + **sémantique** + **[plafond](../theorie/glossaire/entrees/plafond.md)** + **kappa** + **méta** + **pondéré** + **CV** + **CV graines** + **bilan anaphore**, **183/183 portes** (6 S fixés ; T132/T133 2/5) | B10.3 attend un **encodeur qui porte** ; **B13** : **gold neuronal** (POS **0,9415** ; **cascade vrai modèle** : syntagmes **0,6130**, tête **0,7574**, acte **1,0** ; **gold réel 432 : 0,9065 / 0,4598 / 0,5633 / 0,9954, verdict `false`**) ; **politique 
porte 183/183 2892  modalité 0,9846, double sens 0,9769** ; elle qualifie ; **[DRVM](../theorie/glossaire/entrees/drvm.md)/native** (poids et tagger présents) ; **gold 432 réel true** ; **T132/T133** ; **gold B13** ; **porte 183/183** ; **minute 26 nœuds** ; **sto 5/5** ; **fenêtre solvable (BFS 228) mais non discriminante** (oracle 228, aveugle 215, 7B 238) |
gold 432 réel true 2836  ; **pragmatique neuronale 130 : acte 1,0, négation 1,0, modalité 0,9846, double sens 0,9769** ; elle qualifie ; **[DRVM](../theorie/glossaire/entrees/drvm.md)/native** (poids et tagger présents) ; **gold 432 réel true** ; **T132/T133** ; **gold B13** ; **porte 183/183** ; **minute 26 nœuds** 
… [113 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\nt=open('docs/pilotage/roadmap.md').read()\nline=t.splitlines()[32]\nprint(len(line))\nfor needle in ['W5 — restitution v3', 'J4 — l\\'or de rôles', 'T132/T133']:\n    i=line.find(needle)\n    print('---',needle,i,line[max(0,i-250):i+350])\nPY", "description" … [28 caractères tronqués]`

  ```
946
--- W5 — restitution v3 555 nguistique** (398 langues, 0,9687) ; **W2 — tagger 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), fermé 402 −1,55** ([fiche](../../reports/rapport-tagger-h50.md)) ; **W3 — matrice du tagger** ([fiche](../../reports/rapport-tagger-defaut.md)) ; **W5 — restitution v3 : gold S 144/144, cinq rôles 18/18, permutation 0/18 ; `--roles-v3` opt-in** ([fiche](../../reports/rapport-restitution-v3.md)) | **R4.4 close** ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; **J4 — l'or de rôles** (
--- J4 — l'or de rôles 883 roles-v3` opt-in** ([fiche](../../reports/rapport-restitution-v3.md)) | **R4.4 close** ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; **J4 — l'or de rôles** (seconds cadres) ; R2/R3 attendent N5/N4 |
--- T132/T133 -1 | **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R1.2-10
… [139 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés) … [1907 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**État au 15/11 (nuit).** **T1–T6 — le produit exploitable** : installable, quickstart rejoué, JSON v2, performance mesurée, CLI robuste ; [bilan](../../reports/rapport-bilan-exploitable.md). Sem … [252 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "`_groupes_partition`/`_cible_proche` sont **O(k²)**. [Fiche](../../reports/rapport-performance.md) ·\n[JSON](../../reports/performance.json). Prochaine action : **borner les boucles**.\n\n**T6 —  … [1250 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-11-15 23 h 35**.", "old_string": "L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour … [33 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nt=open('docs/pilotage/roadmap.md').read().splitlines()\nprint(t[30][-500:])\nPY", "description": "See B row tail"}`

  ```
s** avec règle, minimal **0** ; labyrinthe **2 sonde** ; porte **27 nœuds** avec la règle (200 sans)) ; **pragmatique neuronale 130 : acte 1,0, négation 1,0, modalité 0,9846, double sens 0,9769** ; elle qualifie ; **[DRVM](../theorie/glossaire/entrees/drvm.md)/native** (poids et tagger présents) ; **gold 432 réel true** ; **T132/T133** ; **gold B13** ; **porte 183/183** ; **minute 26 nœuds** ; **sto 5/5** ; **fenêtre solvable (BFS 228) mais non discriminante** (oracle 228, aveugle 215, 7B 238) |
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\nt=p.read_text()\nold='**fenêtre solvable (BFS 228) mais non discriminante** (oracle 228, aveugle 215, 7B 238) |'\nnew='**fenêtre solvable (BFS 228) mais non discriminante** (oracle 228, aveugle 215, 7B 238) ;  … [249 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
AssertionError: 2
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\nlines=p.read_text().splitlines()\ni=30\nold='**fenêtre solvable (BFS 228) mais non discriminante** (oracle 228, aveugle 215, 7B 238) |'\nnew='**fenêtre solvable (BFS 228) mais non discriminante** (oracle 228,  … [326 caractères tronqués]`

  ```
ok
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md", "offset": 180, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md</path>
<type>file</type>
<content>
180: gold **612**, **1 295/1 295** attachements portent des objets, **2 139** objets au total, **0**
181: span faux. Les `role` passent à un **vocabulaire fermé** de huit valeurs
182: (`predicat`, `agent`, `objet`, `lieu`, `temps`, `qualite`, `possesseur`, `destinataire`) :
183: **21** rôles bruts → **8**, **0** hors table. Le contrôle négatif filtre
184: `role == "predicat"` : **711** GV trouvés, **0** `prédicat` accentué. Le schéma v2 valide
185: **612/612** annotations, v1 **612/612** ; **24** tests produit, **9** tests de schéma.
186: [`fiche T1`](../../reports/rapport-empaquetage.md) · [`fiche T2`](../../reports/rapport-contrat-json.md) ·
187: [`JSON T2`](../../reports/contrat-json.json).
188: 
189: ### T3 — le démarrage en 5 minutes : rejoué sur un clone public
190: 
191: Le quickstart [`docs/produit/demarrage.md`](../../docs/produit/demarrage.md) part d'un clone
192: public neuf, installe dans `.venv` et lance trois commandes ; **3/3** sortent **0**, le JSON
193: fait **5 899 octets** en schéma **v2**, `--tagger` sans clé sort **4**, `auto` sort **0**, et
194
… [617 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md", "new_string": "[`fiche`](../../reports/rapport-quickstart.md) · [`JSON`](../../reports/quickstart.json).\n\n### T4 — la performance : 10 000 mots en 4,0 s, et le contrôle de linéarité échoue\n\n10 000 mots  … [3006 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n 'rejouée à part' reports/rapport-bilan-exploitable.md", "description": "Find gate sentence"}`

  ```
235:**rejouée à part**, pas dans la passe complète. Les compteurs de l'état sont donc **86 portes**
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable.md", "new_string": "**rejouée seule le 15/11**, **verte** (12 tests), pas dans la passe complète. Les compteurs de l'état sont donc **86 portes**", "old_string": "**rejouée à part**, pas dans la passe co … [57 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '12,70p' reports/README.md", "description": "Read reports README current fiches table"}`

  ```
> partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).

## Les fiches courantes

| fichier | ce qu'il porte |
|---|---|
| [`rapport-bilan-jour-1115.md`](rapport-bilan-jour-1115.md) | **Bilan** — le 15/11 : la semaine 2 en un jour, la décision du tagger |
| [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) | **Bilan** — la semaine 07 → 15/11 : le produit, Panini, la coordination, le harnais |
| [`rapport-bilan-nuit.md`](rapport-bilan-nuit.md) | **Bilan** — la nuit du 14 au 15/11 : le tagger, la base honnête, la phase C/B |
| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
| [`rapport-gold-452.md`](rapport-gold-452.md) | **W1/R0.7** — le gold réel 452 : composition, split 402/H50, sha256, 10 candidats GP/SUB |
| [`rapport-tagger-h50.md`](rapport-tagger-h50.md) | **W2/R0.7** — le tagger sur le split : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/attachement 402 inchangés, fermé 402 **−1,55** ; la règle ne le rejette pas |
| [`rapport-tagger-defaut.md`](rapport-tagger-defaut.md) | **W3/R0.7** — la matrice du tagger : défaut hors ligne **code 0*
… [5754 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-semaine-2.md`](rapport-semaine-2.md) | **W6** — la semaine 2 : W1-W5, le tagger, Panini bloqué, la restitution v3 |\n| [`rapport-bilan-exploitable.md`](rapport-bilan-exploitable.md) | **T6/B … [368 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md": file has not been read — read the file, then retry
  ```

- **bash** `{"command": "python3 tools/index_reports.py && echo INDEX-OK; grep -n 'rapport-bilan-exploitable\\|rapport-empaquetage\\|rapport-cli-robuste' reports/INDEX.md | head", "description": "Regenerate reports index"}`

  ```
762 fiches → reports/INDEX.md
INDEX-OK
85:| [rapport-bilan-exploitable.md](rapport-bilan-exploitable.md) | T6 — le bilan exploitable : installable, rejouable, mesuré, mais pas encore général |
116:| [rapport-cli-robuste.md](rapport-cli-robuste.md) | T5 — la robustesse de la CLI : `--duree`, cinq codes de sortie, aide des quatre sous-commandes, `--fichier` sans trace |
178:| [rapport-empaquetage.md](rapport-empaquetage.md) | T1 — l'empaquetage : `pip install -e .`, `drave` hors du dépôt, chemin historique intact |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 5, "offset": 38}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
38: | [`rapport-tableau-mesures.md`](rapport-tableau-mesures.md) | **J13.1** — la table des mesures : POS |
39: | [`rapport-bilan-chantier.md`](rapport-bilan-chantier.md) | **J10.1** — le bilan du chantier : F1 |
40: | [`rapport-semaine.md`](rapport-semaine.md) | **J5.1** — le rapport de semaine : produit |
41: | [`rapport-semaine-2.md`](rapport-semaine-2.md) | **W6** — la semaine 2 : W1-W5, le tagger, Panini bloqué, la restitution v3 |
42: | [`rapport-passe-honnetete.md`](rapport-passe-honnetete.md) | **J9.1** — la passe d'honnêteté : **19** fiches |

(Showing lines 38-42 of 230. Use offset=43 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-semaine-2.md`](rapport-semaine-2.md) | **W6** — la semaine 2 : W1-W5, le tagger, Panini bloqué, la restitution v3 |\n| [`rapport-bilan-exploitable.md`](rapport-bilan-exploitable.md) | **T6/B … [368 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py", "description": "Run documentation review"}`

  ```
revue de documentation · 765 fiche(s) · 860 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py; echo \"code=$?\"", "description": "Validate en-cours"}`

  ```
en-cours · 1742 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
code=0
  ```

- **bash** `{"command": "sed -n '36,48p' docs/pilotage/roadmap.md", "description": "Check roadmap state paragraph flow"}`

  ```
| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**) ; **PDF** (1 927 doc., 322 Mo) ; **documents** (3 384 doc., 872 M car., 8 Ko 2,07 %) ; **OCR** (20 livres, 7 381 p, 15,36 M, 8 Ko 0 ; [CEGEP](../theorie/glossaire/entrees/cegep.md) **91 scans uniques**, 60 documents, 1 982 p, 4,41 M car., 8 Ko 0) ; **genres** mesurés | **l'OCR est clos** (limite : 8 scans `.PDF`, 58 p) ; la préparation **R1.1/R1.2** (N2) et **A2.6** (A) |

**État au 15/11 (nuit).** **T1–T6 — le produit exploitable** : installable, quickstart rejoué, JSON v2, performance mesurée, CLI robuste ; [bilan](../../reports/rapport-bilan-exploitable.md). Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV**
… [3309 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py; echo \"journal=$?\"; python3 tools/taille_documents.py; echo \"taille=$?\"", "description": "Validate journal and document sizes"}`

  ```
journal · 47 jour(s) · 221 session(s) · 2682 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
journal=0
  budget de contexte · documents chargeables
    mots lignes  cat budget  document
    9191    514   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2773    232   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    17
… [722 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py; echo \"schemas=$?\"", "description": "Validate schemas"}`

  ```
schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
schemas=0
  ```

- **bash** `{"command": "sed -n '1,180p' tools/taille_documents.py", "description": "Inspect context budget calculation"}`

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

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re,sys\nsys.path.insert(0,'tools')\nfrom taille_documents import poids\nprint('AGENTS',poids('AGENTS.md'))\nprint('en-cours',poids('docs/pilotage/en-cours.md'))\nspecifiques={'organisation-du-depot.md','modularisation.md','relations-humaines.md'}\nvals=[ … [299 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
ImportError: cannot import name 'poids' from 'taille_documents' (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/taille_documents.py)
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re\ndef m(p): return len(re.findall(r'\\S+', pathlib.Path(p).read_text()))\nprint('AGENTS',m('AGENTS.md'))\nprint('en-cours',m('docs/pilotage/en-cours.md'))\nvals=[]\nfor a in pathlib.Path('docs/methode').glob('*.md'):\n    if a.name not in {'organisatio … [278 caractères tronqués]`

  ```
AGENTS 1196
en-cours 1742
[(1174, 'continuite.md'), (1089, 'contexte.md'), (1068, 'ressources.md'), (886, 'chantier-autonome.md'), (768, 'rangement.md')]
max 1174 sum 4112
  ```

- **bash** `{"command": "git diff --numstat docs/pilotage/en-cours.md docs/pilotage/roadmap.md; git diff docs/pilotage/en-cours.md | head -120", "description": "See en-cours diff"}`

  ```
12	8	docs/pilotage/en-cours.md
17	4	docs/pilotage/roadmap.md
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 1a689e20..e44e48e6 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 23 h 23 HNE (T5 : la CLI robuste — `--duree`, codes 0/3/4/5, aide, `--fichier`)**
+**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable — installable, quickstart, JSON, performance, codes ; passe 85/81/4 lue, 86e porte verte)**
 
 > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
 
@@ -62,8 +62,8 @@
 - **Objectif final** : moteur de pensée v0.
 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
 - **Ce que font les autres** : **N2**, **S**, **hub**.
-- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [ra
… [8324 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable ; passe 85/81/4 lue, 86e porte verte)**", "old_string": "**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable — ins … [88 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../report … [853 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../.. … [975 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6** | **U1 — les deux O(k²)** ; **`g017` tran … [447 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T1–T6 — livré** : installable, quickstart, JSON v2, performance, CLI ; [bilan](../../reports/rapport-bilan-exploitable.md). Reste **U1** (les deux O(k²)), **U2** (la roue), **U3** (`--profils` … [850 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py | tail -12", "description": "Recheck context budgets"}`

  ```
1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4049 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9191 mots > budget 9000 (T1)
     · T0 : 4049 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport subprocess,re\nfor rev in ['HEAD','']:\n    cmd=['git','show','HEAD:docs/pilotage/en-cours.md'] if rev else ['cat','docs/pilotage/en-cours.md']\n    t=subprocess.check_output(cmd,text=True)\n    print(rev or 'WORK', len(re.findall(r'\\S+',t)))\nPY\ngit diff docs … [99 caractères tronqués]`

  ```
HEAD 1627
WORK 1679
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 1a689e20..6648627f 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 23 h 23 HNE (T5 : la CLI robuste — `--duree`, codes 0/3/4/5, aide, `--fichier`)**
+**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable ; passe 85/81/4 lue, 86e porte verte)**
 
 > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
 
@@ -62,8 +62,8 @@
 - **Objectif final** : moteur de pensée v0.
 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
 - **Ce que font les autres** : **N2**, **S**, **hub**.
-- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md) ; **T4** : 10 000 mots **4,01 s**, contr
… [7482 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable)**", "old_string": "**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable ; passe 85/81/4 lue, 86e porte verte)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Prochaine action** : **U1 — borner `_groupes_partition` et `_cible_proche`** (O(k²)) ; **J4 — l'or de rôles** ; T132/T133.", "old_string": "- **Prochaine action** : **U1 — borner `_groupes_p … [119 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../.. … [682 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W … [459 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T1–T6 — livré** : installable, quickstart, JSON v2, performance, CLI ; reste **U1** (les deux O(k²)), **U2** (la roue), **U3** (`--profils`) ; [bilan](../../reports/rapport-bilan-exploitable.m … [219 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py | tail -8", "description": "Recheck budgets"}`

  ```
T0 max : 4024 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9191 mots > budget 9000 (T1)
     · T0 : 4024 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../.. … [458 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py | tail -6", "description": "Recheck T0"}`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9191 mots > budget 9000 (T1)
     · T0 : 4004 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T1–T6 — livré** ; reste **U1** (les deux O(k²)), **U2** (la roue), **U3** (`--profils`) ; [bilan](../../reports/rapport-bilan-exploitable.md).", "old_string": "**T1–T6 — livré** : installable, … [167 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py | tail -5", "description": "Recheck T0 again"}`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9191 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport subprocess,re\nfor rev in ['HEAD','']:\n    t=subprocess.check_output(['git','show','HEAD:docs/pilotage/roadmap.md'] if rev else ['cat','docs/pilotage/roadmap.md'],text=True)\n    print(rev or 'WORK', len(re.findall(r'\\S+',t)))\nPY\ngit diff docs/pilotage/roadm … [72 caractères tronqués]`

  ```
HEAD 9324
WORK 9517
diff --git a/docs/pilotage/roadmap.md b/docs/pilotage/roadmap.md
index 2634591c..3d047213 100644
--- a/docs/pilotage/roadmap.md
+++ b/docs/pilotage/roadmap.md
@@ -28,14 +28,14 @@
 | chantier | ce qu'il couvre | état | prochaine action |
 |---|---|---|---|
 | **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
-| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire
… [18168 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\nt=open('docs/pilotage/roadmap.md').read()\nstart=t.index('**État au 14/11 07 h 10.**')\nend=t.index('poussés ;',start)+len('poussés ;')\nseg=t[start:end]\nprint('words',len(re.findall(r'\\S+',seg)),'chars',len(seg))\nprint(seg[:300]); print('...'); print(seg … [58 caractères tronqués]`

  ```
words 205 chars 1494
**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV** réglée (s
...
 pts de F1) ; les quatre états N2/S/R/A intégrés ; 84 portes, **81 vertes**, 3 rouges nommées (`indice`, `melange`, `sessions` — cette dernière revérifiée verte le 14/11) ; `master` = `s/v7` poussés ;
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re\np=pathlib.Path('docs/pilotage/roadmap.md')\nt=p.read_text()\nstart=t.index('**État au 14/11 07 h 10.**')\nend=t.index('poussés ;',start)+len('poussés ;')\nold=t[start:end]\nnew=(\"**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902**, attac … [1050 caractères tronqués]`

  ```
old words 205 new words 53
168:**T6 — le bilan exploitable (15/11, 23 h 35).** Les cinq briques se tiennent : **installation
169-éditable** (8 tests, code 127 sans install), **quickstart 3/3** (JSON v2 **5 899** octets,
170-erreurs 3/4/1), **API du JSON** (**2 139** objets, **8** rôles, v1 lue), **performance** (10 000
171-mots **4,01 s**, **2 493 mots/s**, **126 Mio**, **14,8 Mo**), **CLI** (**20/20**, codes
172-**0/3/4/5/1**, aide **8/8**). **Passe non relancée** : **85** portes lues (**81/4**), `sessions`
173-réparée, ciblage **9/9**, **86e porte** `porte-banc-performance` verte seule. Trois limites
174-restent : le **clone public** perd `tools/structures` (attachement **88,70 %** au lieu de
175-**99,58 %**), la croissance est **O(k²)** (α = **1,55**), et le **gold de S** n'est pas un or
176-humain indépendant. [Fiche](../../reports/rapport-bilan-exploitable.md) ·
177-[JSON](../../reports/rapport-bilan-exploitable.json). Prochaine action : **U1 — borner les deux
178-O(k²)** ; puis **U2** (la roue), **U3** (`--profils`) ; **J4**, **Panini** et la décision
179-`auto` restent aux dépendances nommées.
180-
  ```

- **bash** `{"command": "python3 tools/taille_documents.py | tail -5", "description": "Recheck roadmap budget"}`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9022 mots > budget 9000 (T1)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques : **installation éditable**\n(127 sans install), **quickstart 3/3** (JSON v2 **5 899** octets), **API** (**2 139** objets,\n**8** rôle … [1709 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 16, "offset": 166}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
166: [JSON](../../reports/performance.json). Prochaine action : **borner les boucles**.
167: 
168: **T6 — le bilan exploitable (15/11, 23 h 35).** Les cinq briques se tiennent : **installation
169: éditable** (8 tests, code 127 sans install), **quickstart 3/3** (JSON v2 **5 899** octets,
170: erreurs 3/4/1), **API du JSON** (**2 139** objets, **8** rôles, v1 lue), **performance** (10 000
171: mots **4,01 s**, **2 493 mots/s**, **126 Mio**, **14,8 Mo**), **CLI** (**20/20**, codes
172: **0/3/4/5/1**, aide **8/8**). **Passe non relancée** : **85** portes lues (**81/4**), `sessions`
173: réparée, ciblage **9/9**, **86e porte** `porte-banc-performance` verte seule. Trois limites
174: restent : le **clone public** perd `tools/structures` (attachement **88,70 %** au lieu de
175: **99,58 %**), la croissance est **O(k²)** (α = **1,55**), et le **gold de S** n'est pas un or
176: humain indépendant. [Fiche](../../reports/rapport-bilan-exploitable.md) ·
177: [JSON](../../reports/rapport-bilan-exploitable.json). Prochaine action : **U1 — borner les deux
178: O(k²)** ; puis **U2** (l
… [264 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques : **installation éditable**\n(127 sans install), **quickstart 3/3** (JSON v2 **5 899** octets), **API** (**2 139** objets,\n**8** rôle … [1709 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py | tail -4", "description": "Check roadmap budget final"}`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py; echo \"revue=$?\"; python3 tools/verifie_en_cours.py; echo \"etat=$?\"", "description": "Re-run review and state checks"}`

  ```
revue de documentation · 765 fiche(s) · 860 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  en-cours · 1627 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
etat=0
  ```

- **bash** `{"command": "bash tools/porte-document.sh; echo \"document=$?\"; bash tools/porte-etat.sh; echo \"etat_gate=$?\"", "description": "Run document and state gates"}`

  ```
=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ===
=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ===
  30 documents · 51 pages · 1487 régions
  types : {'blanc': 1457, 'code': 4, 'figure': 3, 'legende': 1, 'liste': 238, 'note': 120, 'paragraphe': 829, 'section': 230, 'tableau': 30, 'titre': 32}
  deux colonnes : 6 G puis 6 D, 0 retour(s)
  contrôle texte plat : échoue comme attendu
  notes hors corps : 120 région(s), 0 fuite(s)
    data/onu/pdf/A_RES_80_1-en.pdf                         85 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-es.pdf                         93 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-fr.pdf                         91 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-ru.pdf                         95 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-zh.pdf                         83 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_10-en.pdf                       155 régions  fidélité 1.000
    … et 24 autres

✅ les 50 pages sont découpées, les partitions exactes, le rejeu identique,
   la fidélité ≥ 0,99 et les trois contrôles négatifs se comportent comme prévu.
✅ porte document verte
document=0
=== PORTE ÉTAT — LE FAIT ET SA LIGNE ===
  en-cours · 162
… [343 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh; echo \"tableaux=$?\"; bash tools/porte-registre.sh; echo \"registre=$?\"", "description": "Run tableaux and registre gates"}`

  ```
✅ 1842 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4721 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
tableaux=0
=== 1. topologie NOMMÉE + registre ===
  [topologie] chaîne vérifiée : local 0..11 → 127.0.0.1:64055 12..23
  perplexité 113.0068 · code 0
=== 2. la MÊME topologie, adresse en dur : même résultat ===
  perplexité 113.0068 · code 0
  ✅ registre et adresse en dur donnent le MÊME résultat (113.0068)
=== 3. région ABSENTE du registre : refus en la nommant ===
  ✅ région absente : refusée en la nommant (code 2), rien n'est calculé
registre=0
  ```

- **bash** `{"command": "git status --short", "description": "Check working tree status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-15/README.md
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
?? reports/rapport-bilan-exploitable.json
?? reports/rapport-bilan-exploitable.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "git diff --stat reports/INDEX.md; git diff reports/INDEX.md | head -80; grep -n 'rapport-s-paragraphes' reports/INDEX.md", "description": "Inspect INDEX diff for untracked report"}`

  ```
reports/INDEX.md | 8 +++++++-
 1 file changed, 7 insertions(+), 1 deletion(-)
diff --git a/reports/INDEX.md b/reports/INDEX.md
index e006b326..3d18d19e 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **756 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **762 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -82,6 +82,7 @@
 | [rapport-b13-porte-140.md](rapport-b13-porte-140.md) | B13 — la porte est à 140/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 alignés sur 2/5 (distracteurs r428–r432) |
 | [rapport-base-reelle.md](rapport-base-reelle.md) | B13 — la base honnête : `evaluer --reel`, 452 phrases réelles, et ce que le synthétique cachait |
 | [rapport-bilan-chantier.md](rapport-bilan-chantier.md) | J10.1 — le bilan du chantier : F1 0,7533 → 0,7902, attachement 236 → 238, Panini mesuré et borné |
+| [rapport-bilan-exploitable.md](rapport-bilan-exploitable.md) | T6 — le bilan exploitable : installable, rejouable, me
… [5762 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/INDEX.md')\nt=p.read_text()\nold='| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d\\'Alice, sources anglaises et référents |\\n'\nassert t.count(old)==1, t.count(ol … [232 caractères tronqués]`

  ```
ok
3:> **Généré** par `tools/index_reports.py` — **761 fiches**. Les fichiers
  ```

- **bash** `{"command": "git diff --stat reports/INDEX.md; git diff reports/INDEX.md | tail -30", "description": "Verify INDEX diff"}`

  ```
reports/INDEX.md | 9 +++++++--
 1 file changed, 7 insertions(+), 2 deletions(-)
 | [rapport-echecs-v2.md](rapport-echecs-v2.md) | B13 — les 8 échecs restants de l'attachement v2 : qualifiés, chiffrés, 5 règles pour 145/145 |
 | [rapport-elagage-logs.md](rapport-elagage-logs.md) | A6.3 — l'élagage guidé par les logs : aucun neurone ne s'allume jamais, mais 63 % s'allument à peine |
+| [rapport-empaquetage.md](rapport-empaquetage.md) | T1 — l'empaquetage : `pip install -e .`, `drave` hors du dépôt, chemin historique intact |
 | [rapport-empreinte-memoire.md](rapport-empreinte-memoire.md) | Rapport — l'empreinte mémoire : ce qui réduit vraiment ce qu'il faut charger |
 | [rapport-encodage.md](rapport-encodage.md) | Drave — encodage de structure : éliminer la valeur |
 | [rapport-engram-etat.md](rapport-engram-etat.md) | Engram de DeepSeek-V4.1 : ce qui est établi, ce qui manque, et pourquoi on s'arrête là |
@@ -630,6 +634,7 @@
 | [rapport-pensee-votante3.md](rapport-pensee-votante3.md) | B13 — l'observation à trois looks : 20/20, mais 4000 épisodes |
 | [rapport-pensee-vote.md](rapport-pensee-vote.md) | B13 — le vote de signaux : 5 looks, toujours 0/20 |
 | [rapport-pensee-vrais-absen
… [2773 caractères tronqués]
  ```

- **bash** `{"command": "git ls-files reports/rapport-s-paragraphes.md; git show HEAD:reports/INDEX.md | grep -n 'rapport-s-paragraphes'; git show HEAD:reports/INDEX.md | head -3", "description": "Check if S report was already tracked/indexed"}`

  ```
716:| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **756 fiches**. Les fichiers
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/INDEX.md')\nt=p.read_text()\nline='| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d\\'Alice, sources anglaises et référents |\\n'\nanchor='| [rapport-s-limites-v6.m … [490 caractères tronqués]`

  ```
ok
 reports/INDEX.md | 8 +++++++-
 1 file changed, 7 insertions(+), 1 deletion(-)
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
-> **Généré** par `tools/index_reports.py` — **756 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **762 fiches**. Les fichiers
+| [rapport-bilan-exploitable.md](rapport-bilan-exploitable.md) | T6 — le bilan exploitable : installable, rejouable, mesuré, mais pas encore général |
+| [rapport-cli-robuste.md](rapport-cli-robuste.md) | T5 — la robustesse de la CLI : `--duree`, cinq codes de sortie, aide des quatre sous-commandes, `--fichier` sans trace |
+| [rapport-contrat-json.md](rapport-contrat-json.md) | T2 — l'API du JSON : candidats d'attachement en objets, rôles normalisés |
+| [rapport-empaquetage.md](rapport-empaquetage.md) | T1 — l'empaquetage : `pip install -e .`, `drave` hors du dépôt, chemin historique intact |
+| [rapport-performance.md](rapport-performance.md) | T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55) |
+| [rapport-quickstart.md](rapport-quickstart.md) | T3 — le démarrage en 5 minutes : clone public, installation, trois commande
… [26 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/index_reports.py --verifier; echo \"index=$?\"; git diff --check; echo \"diffcheck=$?\"", "description": "Verify index and whitespace"}`

  ```
index=0
diffcheck=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py; echo \"revue=$?\"; python3 tools/taille_documents.py | tail -1; python3 tools/verifie_en_cours.py | tail -1", "description": "Final docs checks"}`

  ```
revue de documentation · 765 fiche(s) · 860 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh; echo \"tableaux=$?\"; python3 tools/verifie_journal.py | tail -1", "description": "Final table and journal checks"}`

  ```
✅ 1842 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4721 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
tableaux=0
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "git add reports/rapport-bilan-exploitable.md reports/rapport-bilan-exploitable.json docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-15/README.md reports/README.md reports/INDEX.md && git diff --cached --stat", "description": "Stage T6 files only"}`

  ```
docs/pilotage/en-cours.md              |  20 +-
 docs/pilotage/roadmap.md               |  18 +-
 journal/2026-11-15/README.md           |  39 +++
 reports/INDEX.md                       |   8 +-
 reports/README.md                      |   1 +
 reports/rapport-bilan-exploitable.json | 534 +++++++++++++++++++++++++++++++++
 reports/rapport-bilan-exploitable.md   | 331 ++++++++++++++++++++
 7 files changed, 938 insertions(+), 13 deletions(-)
  ```

- **bash** `{"command": "git diff --cached docs/pilotage/en-cours.md docs/pilotage/roadmap.md | sed -n '1,220p'", "description": "Review staged pilotage changes"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 1a689e20..117c45ea 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 23 h 23 HNE (T5 : la CLI robuste — `--duree`, codes 0/3/4/5, aide, `--fichier`)**
+**Mis à jour : 2026-11-15, 23 h 35 HNE (T6 : le bilan exploitable)**
 
 > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
 
@@ -62,8 +62,8 @@
 - **Objectif final** : moteur de pensée v0.
 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
 - **Ce que font les autres** : **N2**, **S**, **hub**.
-- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md) ; **T4** : 10 000 mots **4,01 s**, contrôle **α 1,55** ; [fiche](../../reports/rapport-performanc
… [24891 caractères tronqués]
  ```

- **bash** `{"command": "git commit -m \"T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/4 LUE, 86E PORTE VERTE\"", "description": "Commit T6 closure f … [6 caractères tronqués]`

  ```
[stderr]
  ✅ index : aucun fait stagé sans état
[still running after 60000ms; moved to background job bash-92]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-92", "wait": true, "timeout_ms": 120000}`

  ```
[s/v7 83adaa2b] T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/4 LUE, 86E PORTE VERTE
 22 files changed, 3967 insertions(+), 42 deletions(-)
 create mode 100644 journal/sessions/session-0ad92682-0d71-421c-be45-3c35e875bb07/digest.md
 create mode 100644 journal/sessions/session-0ad92682-0d71-421c-be45-3c35e875bb07/rapport.md
 create mode 100644 reports/rapport-bilan-exploitable.json
 create mode 100644 reports/rapport-bilan-exploitable.md
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "git show --stat --oneline HEAD | sed -n '1,60p'; echo ---; git status --short | head -30", "description": "Inspect commit contents"}`

  ```
83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/4 LUE, 86E PORTE VERTE
 docs/pilotage/en-cours.md                          |   20 +-
 docs/pilotage/roadmap.md                           |   18 +-
 journal/2026-11-15/README.md                       |   46 +-
 journal/2026-11-15/distribue.md                    |    7 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/memoire.md                      |    2 +-
 journal/2026-11-15/mesures.md                      |    2 +-
 journal/2026-11-15/modele.md                       |    2 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   49 +
 .../rapport.md                                     |   15 +-
 .../digest.md                                      | 2597 ++++++++++++++++++++
 .../rapport
… [881 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py; echo \"revue=$?\"; python3 tools/verifie_en_cours.py | tail -1; python3 tools/taille_documents.py | tail -1", "description": "Post-commit checks"}`

  ```
revue de documentation · 765 fiche(s) · 860 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  ✅ état court, structuré, multi-session et reprenable
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "git log -1 --format='%h %s'; echo ---; git status --short | head -20", "description": "Confirm commit and remaining tree"}`

  ```
83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE S) ; PASSE 85/81/4 LUE, 86E PORTE VERTE
---
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

### 🤖 Assistant

**T6 est clos.** Commit `83adaa2b` — *T6 — LE BILAN EXPLOITABLE*.

## Livrables

- **[`reports/rapport-bilan-exploitable.md`](reports/rapport-bilan-exploitable.md)** — la fiche de clôture : installable, quickstart, API JSON, performance, codes de sortie, négatifs, reste.
- **[`reports/rapport-bilan-exploitable.json`](reports/rapport-bilan-exploitable.json)** — schéma `drave.bilan-exploitable`, toutes les mesures et les trois lignes restantes.
- **[`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md)** — T6 clos, 765 fiches / 860 JSON, passe et 86e porte, reste réorganisé.
- **[`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md)** — T6 inscrit, lignes B et R mises à jour, **U1** désignée comme prochaine action.
- **[`journal/2026-11-15/README.md`](journal/2026-11-15/README.md)** — récit T4/T5/T6 ; index [`reports/INDEX.md`](reports/INDEX.md) et [`reports/README.md`](reports/README.md) à jour.

## Ce que le bilan retient

- **Installable** : `pip install -e .`, `drave 0.1.0`, 8 tests ; sans installation, code **127** propre. Limite : pas de wheel autonome.
- **Quickstart** : **3/3** commandes, JSON v2 **5 899** octets, erreurs **3/4/1**. Le clone public reste dégradé par l’absence de `tools/structures`.
- **API JSON** : **2 139** objets `{span, cible, source}`, **8** rôles normalisés, **0** span faux, v1 toujours lue.
- **Performance** : 10 000 mots en **4,01 s**, **2 493 mots/s**, **126 Mio**, **14,8 Mo** de JSON ; 100 phrases à **1,10 ms**. Le contrôle de linéarité **échoue** : **α = 1,55**, quadratique **R² 0,99995**, coupables `_groupes_partition` / `_cible_proche`.
- **CLI** : **20/20** cas, codes **0/3/4/5/1**, aide **8/8**, `--duree` sans casser le défaut.

## Portes

Aucune passe complète relancée. Lecture de `work/portes-1115-09h53/registre.txt` : **85 portes, 81 vertes, 4 rouges** ; `sessions` réparée, `indice`, `melange`, `prechargement` tolérées et nommées. Ciblage `work/portes/w6-final/` : **9/9**. Seule la **86e porte** `porte-banc-performance` a été rejouée à part : **verte**, 12 tests.

## Ce qui reste

- **Le gold de S** : 61 phrases / 144 rôles écrits par les mêmes règles — **144/144** n’est pas un or humain indépendant ; **J4** n’est pas ouvert.
- **Panini** : **26 signatures** V14 manquantes, calibration **42/44**, rejeu **27/60** ; le manifeste et la commande sont prêts, le test attend.
- **`--tagger auto`** : prototype opt-in mesuré (30/30 tests, code 0 dans tous les cas) ; la **décision reste humaine**, le défaut hors ligne est inchangé.
- **Suite** : **U1** (les deux O(k²)), **U2** (la roue), **U3** (`--profils`).

Contrôles post-commit : `revue_documentation` ✅, `verifie_en_cours` ✅ (1 627 mots), budget de contexte ✅, `porte-tableaux` ✅. Les modifications non liées présentes dans l’arbre de travail n’ont pas été touchées.

