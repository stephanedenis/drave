# Session DSH — relecture

- identifiant : `session-e1ad947b-50b1-4758-a921-5267225bf642`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-07 12:41:19
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J1.2 : la convention des GV (322 FP / 180 FN). Classe les erreurs, mesure 2 règles candidates (arrêt à l'adverbe final, sujet hors du GV) sur dev/test, garde celles qui font monter le F1 sans perdre d'attachement, fiche `reports/rapport-convention-gv.md` + JSON, commit. Règles : S/D/N2 intouchés ; 183/183.

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

- **bash** `{"command": "pwd && ls", "description": "List repository root"}`

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
  ```

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --short | head -50 && echo \"---\" && git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet log --oneline -10", "description": "Show git status and recent commits"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 m tools/structures
?? reports/rapport-s-paragraphes.md
---
25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
d7469b5c INDEX — RÉGÉNÉRÉ APRÈS L'INVENTAIRE PANINI (702 FICHES) ; ÉTAT HORODATÉ
34fdd4ef DOCS — README T1 TENU (DEUX LIGNES LONGUES RACCOURCIES)
fffbbe5d PANINI — L'INVENTAIRE INTÉGRÉ AU PLAN : 14 DÉPÔTS, 7 AXES, 14 ATOMES, 9 CORPUS, TROIS INTÉGRATIONS MÛRES (UDHR+GÉNÉALOGIE, ATOMES↔NIVEAUX, CORPUS CIC) AVEC LEURS CONTRÔLES NÉGATIFS
f93ddc60 DOCS — README T1 : DEUX LIGNES RACCOURCIES, BUDGET TENU
f1b837a3 DOCS — README T1 SOUS 1 000 MOTS ET COMPTEUR DES DOCUMENTS À 123
fae117e5 DOCS — README T1 ET COMPTEURS APRÈS LE MÉTA-HARNAIS
c49367e0 CHANTIER AUTONOME — LE MÉTA-H
… [273 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"J1.2\" --include=\"*.md\" --include=\"*.json\" --include=\"*.txt\" . | head -40", "description": "Find J1.2 references"}`

  ```
observables pendant environ . Liste de PWN La liste suivante est tirée en grande partie du Pulsar Wind Nebulae Catalog de l'Université Mc Gill : Nom Constellation Pulsar3C 58SN 1181 Cassiopée PSR J0205+6449G253.4-42.0 PSR J0437-4715Nébuleuse du Crabe SN 1054 Taureau PSR J0534+2200N 157B30 Dor B PSR J0537-6910N 158AB0540-69 PSR J0540-6919Geminga Gémeaux PSR J0633+1746Vela X PSR J0835-4510B0906-49 PSR J0908-49133EG J1013-5915 PSR J1016-5857B1046-58 PSR J1048-5832G292.2-0.5 PSR J1119-6127MSH 11-54 PSR J1124-5916G308.8-0.1 PSR J1341-6220Kookaburra PSR J1420-6048B1509-58MSH 15-52 PSR J1513-5908B1643-43 PSR J1646-4346B1706-44 PSR J1709-4429Souris PSR J1747-2958Nébuleuse du Canard B1757-24 PSR J1801-2451SN 386Nébuleuse de la Tortue Scorpion PSR J1811-1925B18
./data/corpus_wiki_fr/train.txt:1049341:Complete TV Studio Recordings est un album d'Art Pepper. Une partie est également disponible sous le titre The Gerry Mulligan Quartet/The Art Pepper Quartet - Jazz Casual et sur le DVD Ralph Gleason's Jazz Casual - Art Pepper Quartet / Bola Sete & Vince Guaraldi. Les CD Complete TV Studio Recordings réunit pour la première fois l'intégralité des enregistrements d'Art Pepper à la télévision. Les 
… [48730 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports | tail -60 && echo \"---TOOLS---\" && ls tools | head -80", "description": "List reports and tools"}`

  ```
sessions-plans.json
seuil-bruit-3b.json
seuil-reseau.json
sonde-octets-moyenne.json
sonde-octets-position.json
sources-pidgin.json
sous-familles-autres.json
toutes-langues
toutes-langues.md
traduction-24langues-3b-A.json
traduction-24langues-3b-B.json
traduction-24langues-A.json
traduction-24langues-B.json
traduction-eurlex-0.5b.json
traduction-eurlex-14b.json
traduction-eurlex-1.5b.json
traduction-eurlex2509-3b.json
traduction-eurlex2509-7b.json
traduction-eurlex-3b-fraeng.json
traduction-eurlex-3b.json
traduction-eurlex-7b-fraeng.json
traduction-eurlex-7b.json
traduction-jw-A.json
traduction-jw-B.json
traduction-langues-3b.json
traduction-langues-7b.json
traduction-legal-0.5b-6.json
traduction-legal-1.5b.json
traduction-legal-3b.json
traduction-legal-7b.json
traduction-legal.json
traduction-litteraire-3b.json
traduction-litteraire-7b.json
traduction-onu-3b.json
traduction-onu6-3b.json
traduction-onu6-7b.json
traduction-onu-7b.json
traduction-pidgin-14b.json
traduction-pidgin-7b.json
traduction-presse-3b.json
traduction-presse-7b.json
traduction-udhr-propre-3b-fraeng.json
traduction-udhr-propre-7b-fraeng.json
traduction-udhr-propre-7b.json
universaux-mesures.json
xnli-14b.json
xnl
… [1798 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"convention.*GV\\|GV.*convention\\|J1\\.2\" docs reports journal tools 2>/dev/null | head -40", "description": "Find GV convention docs"}`

  ```
docs/pilotage/chantiers.md
docs/pilotage/semaine-autonome.md
docs/pilotage/en-cours.md
docs/implantation/moteur-de-pensee.md
reports/rapport-pensee-gold-syntagmes.md
reports/rapport-coherence-fiches.md
reports/pensee-gn-pronom-sujet.json
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md
journal/sessions/ea169cb1-75d7-43fa-b69d-5e2a210f6c38/digest.md
journal/sessions/a0d33fb7-37a9-4834-8a94-0da119e3b18f/digest.md
journal/sessions/538288b3-117b-4daf-8d16-0cd8d6b0090d/digest.md
journal/sessions/b8f0bcb1-5609-4053-818b-ade88583a99b/digest.md
journal/sessions/b8f0bcb1-5609-4053-818b-ade88583a99b/rapport.md
tools/chantier/plan.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports | head -60 && echo \"---\" && ls reports | grep -i \"gv\\|groupe\\|verbal\\|s-paragraphe\\|attachement\"", "description": "List head reports and GV-related"}`

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
bilan-b11.md
bilan-multi-materiel.md
bloc-linguistique.json
bruit-entree.json
-
… [690 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(type(p))\nprint(json.dumps(p,ensure_ascii=False)[:3000])\n\"", "description": "Inspect chantier plan json"}`

  ```
<class 'dict'>
{"nom": "Semaine 07/11 → 14/11 — le produit et l'intégration Panini", "principe": "Une tâche n'est finie que si son acceptation passe ; l'agent commite, le superviseur vérifie.", "taches": [{"id": "J0", "jour": 0, "titre": "Le contrôle du superviseur", "mandat": "Réponds exactement le mot OK, sans autre texte. C'est un test de liaison du superviseur.", "budget_min": 2, "acceptation": [{"commande": "python3 -c \"print('LIAISON-OK')\"", "attendu": "LIAISON-OK"}]}, {"id": "J1.1", "jour": 1, "titre": "r035 : la relative zéro", "mandat": "Tâche J1.1 du chantier : la relative zéro (r035, « The film she talks about is out. »). Reproduis, explique, propose UNE règle générale mesurée sur dev/test ; si elle tient (attachement 236→237, POS/F1 stables), intègre-la et commite avec une fiche `reports/rapport-r035.md` + `reports/pensee-r035.json`. Sinon, écris la fiche du rejet (chiffres, raison) et commite-la. Règles : ne touche pas S/D/N2 ; 183/183 portes ; en-cours à jour.", "budget_min": 90, "acceptation": [{"commande": "test -f reports/rapport-r035.md && echo FICHE-OK", "attendu": "FICHE-OK"}, {"commande": "python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?", 
… [1815 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"J1\" docs/pilotage/semaine-autonome.md docs/pilotage/chantiers.md | head -40", "description": "Find J1 tasks in docs"}`

  ```
docs/pilotage/semaine-autonome.md:87:| **J1 · 07/11** | matin | le produit : le **span `g017`**, la **convention des GV** | attachement et F1, fiche v13 |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"322\" reports/*.md reports/*.json docs/pilotage/*.md 2>/dev/null | grep -i \"fp\\|faux\\|180\" | head -20; echo \"===\"; grep -rln \"180 FN\\|322 FP\\|322 faux\\|180 faux\" . --include=\"*.md\" --include=\"*.json\" 2>/dev/ … [57 caractères tronqués]`

  ```
docs/pilotage/roadmap.md:178:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **porte** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **professeur** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + **votante** + **trois looks** + **bayésien** + **bayésien 2** + **vraisemblance** + **dérive** + **adaptative** + **glisse** + **rupture** + **alternance** + **chaotique** + **fréquent** + **rapide** + **limite** + **hasard 2** + **intra** + **asym** + **rare** + **très rare** + **ultra-rare** + **un look** + **look tardif** + **oubli** + **oubli fort** + **oubli total** + **seuil** + **seuil fin** 
… [2430 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' reports/rapport-pensee-verbe-gv.md && echo \"===JSON===\" && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-verbe-gv.json'))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:4000])\n\"", "description": " … [31 caractères tronqués]`

  ```
# B13 — le verbe du GV-phrase : l'exact passe de 0,0586 à 0,0962

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **167/167 portes** : quand le générateur S produit un GV qui couvre **toute la phrase**
> (`The boy saw the cat in the park`), la règle « dernier token » prenait `park` au lieu de `saw`.
> Le bloc prend désormais le **premier token étiqueté `VERB`** à l'intérieur du GV. Sur le gold
> de T153 (612 phrases, 239 cibles) : **exact 14 → 23 (0,0586 → 0,0962)**, top1 **96 → 105**
> (0,4393), top-k **113 → 122** (0,5105), tête **0,7241 / 0,8414**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_verbe_dans`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-verbe-gv.json`](pensee-verbe-gv.json).

## 1. Avant / après (même gold, 239 cibles)

| mesure | avant | **verbe du GV** | écart |
|---|---:|---:|---:|
| top1 | 96 (0,4017) | **105 (0,4393)** | +9 |
| top-k | 113 (0,4728) | **122 (0,5105)** | +9 |
| **exact** | 14 (0,0586) | **23 (0,0962)** | **+9 (×1,6)** |
| tête top1 | 96 (0,6621) | **105 (0,7241)** | +9 |

… [2466 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' docs/pilotage/semaine-autonome.md", "description": "Read semaine-autonome doc"}`

  ```
# Le chantier autonome — une semaine (7 → 14 novembre 2026)

> **Ce que ce document est.** Le **plan du chantier d'une semaine** : tous les travaux ouverts du
> dépôt et l'**intégration avec l'écosystème Panini**. Il dit **quoi**, **dans quel ordre**, **avec
> quels sous-agents**, **comment on mesure**, et **ce qui peut faire échouer**. L'état courant est
> dans [`en-cours.md`](en-cours.md) ; la théorie de la généalogie dans
> [`../theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md) ; la méthode
> Panini/Nipada dans [`../methode/panini-nipada.md`](../methode/panini-nipada.md).
> *À relire chaque matin du chantier.*

## 1. L'objet

**Une semaine, un système utilisable, une intégration mesurée.** Le produit `drave` (CLI, contrat,
porte) est la **priorité** ; l'intégration avec Panini/Nipada est le **second axe** ; les chantiers
N2/S/R/A sont **coordonnés** (jamais écrits par cette session). Chaque vague produit un
**résultat mesuré**, une **fiche** et son **JSON**, la mise à jour de l'**état** et un **commit
vérifié** — jamais une intention.

## 2. L'inventaire — ce qui est ouvert

### 2.1 Drave — le produit (priorité)

| reste | mesure | où |
|---|---|---|
| 1 
… [6884 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3 -- reports/rapport-r035.md && sed -n '1,160p' reports/rapport-r035.md", "description": "Read r035 report"}`

  ```
25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
# B13 — la relative zéro (r035) : exact 236 → 237, POS inchangée

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.1 · **Date** : 2026-11-07 ·
> **Verdict** : ✅
> **`r035` est réglé** : « The film **she talks about** is out. » n'a aucun marqueur de relative.
> La règle **structurelle** `[GN antécédent] [pronom sujet] [verbe] [préposition orpheline] → REL`
> retrouve le span **[9:24]**, cible **`film`**. L'attachement exact passe de **236 à 237**,
> les labels de **237 à 238**, la couverture de **0,9916 à 0,9958** ; **POS inchangée**
> (0,8625), **F1 0,7533 → 0,7549**. **183/183 portes**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
> `relative_zero`), [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py)
> (test unitaire), [`autotest.py`](../tools/pensee/autotest.py) (183 portes, valeurs recalées) ;
> JSON [`pensee-r035.json`](pensee-r035.json).

## 1. Le cas, reproduit

Gold de `r035` (`tools/tests/linguistique/gold_reel.json`) :

| segment | span | texte | cible |
|---|---|---|---|
| GN | [0
… [5884 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"faux positifs\\|faux négatifs\\|FP\\b\\|FN\\b\" reports/*.md tools/tests/linguistique/*.py 2>/dev/null | head -30", "description": "Find FP FN reports"}`

  ```
reports/bilan-multi-materiel.md
reports/historique-passes-portes.md
reports/INDEX.md
reports/rapport-a80-porte-gain.md
reports/rapport-attention-creuse.md
reports/rapport-audit-v10.md
reports/rapport-budget-decision.md
reports/rapport-campagne-parcimonie.md
reports/rapport-cerveau-corrections.md
reports/rapport-cerveau-modules.md
reports/rapport-decoupage-v41.md
reports/rapport-dev-test-v10.md
reports/rapport-drapeaux-ignores.md
reports/rapport-elagage-logs.md
reports/rapport-fenetre-puits-attention.md
reports/rapport-frontieres-integrees.md
reports/rapport-gold-anglais.md
reports/rapport-grappe-intra-couche.md
reports/rapport-lecteur-multifichiers.md
reports/rapport-localite-activation.md
reports/rapport-mla-experts.md
reports/rapport-modele-moteur.md
reports/rapport-morphologie-verbes.md
reports/rapport-multicibles.md
reports/rapport-mur-memoire-4bits.md
reports/rapport-n2-capacite-34m.md
reports/rapport-n2-fenetre.md
reports/rapport-n2-production-fenetre.md
reports/rapport-n2-r12-2048.md
reports/rapport-native-n0.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/tests/linguistique/ && echo \"---\" && grep -rn \"322\\|180\" tools/tests/linguistique/*.py | head -20", "description": "List linguistique tests and find numbers"}`

  ```
anaphore.py
classement_cible.py
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
replis_cible.py
test_bloc_linguistique.py
---
tools/tests/linguistique/gold_reel.py:5:par `construire()` ; le gold réel total devient **200 phrases** (20 de `gold.py` + 180).
tools/tests/linguistique/gold_reel.py:592:    ("r180", "en", "The book belongs to the library.",
tools/tests/linguistique/gold_reel.py:1018:    ('r322', 'fr', 'Le chien voit le chat ; il dort.',
tools/tests/linguistique/qualifier_cascade.py:12:    python3 tools/tests/linguistique/qualifier_cascade.py --endpoint http://127.0.0.1:18082 \
tools/tests/linguistique/qualifier_cascade.py:73:    ap.add_argument("--port", type=int, default=18082)
tools/tests/linguistique/qualifier_cascade.py:118:        # Seuils : le gold 180 (hand+synth) et le gold réel n'ont pas le même plancher.
tools/tests/linguistique/qualifier_cascade.py:160:                "Seuils : 0,94/0
… [1273 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"322\" reports/*.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/*.md journal/sessions/b8f0bcb1-5609-4053-818b-ade88583a99b/*.md 2>/dev/null | grep -v \"^Binary\" | head -30", "description": "Grep 322 in reports an … [11 caractères tronqués]`

  ```
reports/INDEX.md:558:| [rapport-pensee-roles.md](rapport-pensee-roles.md) | B13 — les 322 GN sans rôle : 129 avant le GV, 172 après |
reports/rapport-audit-v7.md:257:| T157 | « 322 GN sans rôle : 129 avant, 172 après » | 231 sans rôle, 151 avant, 46 après |
reports/rapport-c8-inter-langue.md:26:| empruntée (identité) | — | 582 361,8322 | 29,9154 |
reports/rapport-c8-inter-langue.md:27:| **entraînée** | corpus de campagne (français, 30 morceaux) | **582 361,8322** — aucun gain | 29,9154 |
reports/rapport-chargement-paresseux.md:42:  paire de jetons à froid, que l'emprunt était « plus fidèle » (93228 contre 95592). C'était un
reports/rapport-consolidation-structure-partagee.md:54:| **A + B** (somme) | **6,8845 (−7,3 %)** | 17,3228 (+1,2 %) |
reports/rapport-corpus-pdf.md:5:> **322,5 Mo**, **39 506 tronçons** — **8 Ko à zéro** entre les splits, **0 / 40** sur les trois
reports/rapport-corpus-pdf.md:78:- `data/corpus_pdf/` — le corpus (322,5 Mo, gitignoré).
reports/rapport-corpus-wiki-texte.md:92:| ar | 1 000 310 | 1,994 G | 322 M | 3,57 Go | 28,9 % | **0** | XNLI 0/40 | 1/161/0 |
reports/rapport-cycle-rapide.md:158:| **13** | 0,8134 | 0,7812 | **+0,0322** ← pic |
reports/rapport-cycle
… [2504 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0,7549\\|0.7549\" --include=\"*.py\" --include=\"*.md\" --include=\"*.json\" . 2>/dev/null | grep -v corpus | head -30", "description": "Find F1 0.7549 source"}`

  ```
./reports/rapport-dev-test-v7.md:123:| décalé 2 | 0,8364 | 0,5622 | 0,7187 | 0,7596 | 0,7838 | 0,5410 | 0,7076 | 0,7549 |
./reports/pensee-dev-test-v7.json:1872:     "exactitude": 0.7549,
./reports/pensee-dev-test-v7.json:2426:    "decale2": 0.7549
./reports/pensee-dev-test-v7.json:2625:     0.7549
./reports/pensee-dev-test-v10.json:4935:     "exactitude": 0.7549,
./reports/pensee-dev-test-v10.json:5681:      "p": 0.7549,
./reports/pensee-dev-test-v10.json:5933:    "decale_2": 0.7549,
./reports/pensee-dev-test-v10.json:6078:    0.7549
./reports/rapport-dev-test-v10.md:241:| décalé 2 | `%3==2` | 419 | 165 | 153 | 153 | 0,9273 | 0,5900 | 0,7366 | 0,7596 | 193 | 74 | 67 | 67 | 0,9054 | 0,5699 | 0,7259 | 0,7549 |
./reports/rapport-r035.md:9:> (0,8625), **F1 0,7533 → 0,7549**. **183/183 portes**.
./reports/rapport-r035.md:65:| F1 syntagmes | 0,7533 | **0,7549** | +0,0016 |
./reports/pensee-r035.json:50:   "f1": 0.7549,
./reports/pensee-r035.json:89:  "f1": "0,7533 → 0,7549",
./journal/sessions/f0969e87-af0c-43b1-93cf-f278d9c90846/digest.md:23869:- [on color language and cognition](https://pure.mpg.de/rest/items/item_1047549_10/component/file_2425090/content#3#4#3)
./journal/sessions/c27
… [48730 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1400,1480p' journal/sessions/b8f0bcb1-5609-4053-818b-ade88583a99b/digest.md", "description": "Read digest around 1400-1480"}`

  ```
860-                     "s": "se", "c": "ce", "m": "me", "t": "te"}
861-        n = _ELISIONS.get(n, n)
862-        # les **nombres** ont une classe (l'audit produit : 45 nombres sans POS)
863-        if re.fullmatch(r"\d+(?:[.,]\d+)*", n):
864-            return "NUM", False, 0.9
865-        for classe, mots in lex.items():
866-            if n in mots:
867-                return classe, False, 0.92
868-        if n in VERBES.get(langue, VERBES["fr"]):
869-            return "VERB", True, 0.72
870-        if n in ADJECTIFS.get(langue, ADJECTIFS["fr"]):
871-            return "ADJ", True, 0.68
872-        if re.fullmatch(r"\d+(?:[.,]\d+)*", mot):
873-            return "NUM", False, 0.95
874-        if mot[:1].isupper() and mot[1:].islower() and mot not in {"Le", "La", "Les", "Un", "Une", "The"}:
875-            retu
… [591 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('measure.py'); t=p.read_text()\nt=t.replace('h = bl.Heuristique()','part = sys.argv[2] if len(sys.argv) > 2 else \"alternative\"\\nh = bl.Heuristique(partition=part)')\nt=t.replace('sortie = {\"variante\": VAR.name,','sort … [151 caractères tron
… [3413 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1600,1720p' journal/sessions/b8f0bcb1-5609-4053-818b-ade88583a99b/digest.md", "description": "Read digest around 1600-1720"}`

  ```
- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('variantes.py'); t=p.read_text()\nadd='''\n# placebo : le **même** déclencheur, mais une frontière qui n'en est pas une\nGPL_OLD = GE2_OLD\nGPL_NEW = GE2_NEW.replace('_su.type in (\"PONCT\", \"PREP\", \"DET\")', '_su.type  … [890 caractères tronqués]`

  ```
gv_E_pos2                all 0.7836 (P 0.7376 R 0.8357 tp 1557 fp 554 fn 306) dev 0.7802 test 0.7912 att 236/237
placebo_E2               all 0.7389 (P 0.7032 R 0.7783 tp 1450 fp 612 fn 413) dev 0.7359 test 0.7455 att 231/232
base                     all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
--- partition filtrer_union
all 0.8044 tp 1456 fp 301 fn 407 att 230 / 231 couv 0.9665
dev 0.7982 tp 999 fp 208 fn 297 att 155 / 156 couv 0.9571
test 0.8183 tp 457 fp 93 fn 110 att 75 / 75 couv 0.9868
--- partition filtrer
all 0.8104 tp 1440 fp 251 fn 423 att 222 / 223 couv 0.9331
dev 0.8003 tp 984 fp 179 fn 312 att 148 / 149 couv 0.9141
test 0.8329 tp 456 fp 72 fn 111 att 74 / 74 couv 0.9737
--- partition brut
all 0.7533 tp 1463 fp 558 fn 400 att 236 / 237 couv 0.9916
dev 0.7476 tp 1004 fp 386 fn 292 att 1
… [6842 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /tmp/seg 2>/dev/null | head; echo \"---\"; ls /tmp/seg/variants 2>/dev/null | head -20", "description": "Check /tmp/seg remnants"}`

  ```
total 1952
drwxr-xr-x.   3 stephane stephane     220  7 nov 01:53 .
drwxrwxrwt. 319 root     root       27780  7 nov 12:42 ..
-rw-r--r--.   1 stephane stephane    7900  7 nov 01:51 class_base.json
-rw-r--r--.   1 stephane stephane    3805  7 nov 01:51 classer.py
-rw-r--r--.   1 stephane stephane    7931  7 nov 01:51 class_tout.json
-rw-r--r--.   1 stephane stephane    2636  7 nov 01:53 croisements.py
-rw-r--r--.   1 stephane stephane   23288  7 nov 01:47 diffs.txt
-rw-------.   1 stephane stephane    2591  7 nov 01:58 measure.py
-rw-r--r--.   1 stephane stephane 1927748  7 nov 01:59 resultats.json
---
base
comb_E2_GB
comb_g017_E2
comb_g017_GB_E2
comb_r035_g017
comb_r035_g017_E2
comb_tout
g017_G1
gv_A_B
gv_A_objet
gv_B_adverbe
gv_C_prep
gv_E_pos
gv_E_pos2
gv_E_pos3
placebo_E2
r035_P1
r035_P1P2
r035_P1_P3
r035_P2
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,200p' tools/tests/linguistique/evaluer_gold.py", "description": "Read evaluer_gold.py"}`

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

- **bash** `{"command": "cd /tmp/seg && sed -n '1,240p' variantes.py 2>/dev/null || ls | head", "description": "Read variantes.py"}`

  ```
"""Construit les variantes patchées de bloc_linguistique.py et mesure chacune.

Chaque variante = copie du fichier du dépôt + patchs textuels exacts (old→new), appliqués
une seule fois chacun. Le module de la variante est importé dans un sous-processus (pas de
cache de module), et la mesure appelle evaluer_gold.evaluer_bloc sur all/dev/test.
"""
import json
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path("/home/stephane/Data13TB/stephane/GitHub/Qtrinet")
SRC = REPO / "tools/bloc_linguistique.py"
RACINE_SEG = pathlib.Path("/tmp/seg")
BASE_TXT = SRC.read_text(encoding="utf-8")

# ---------------------------------------------------------------- patchs exacts
P1_OLD = '''                       and (j == i + 1 or not est_verbe(mots[j][0], mots[j][2]))):
                    j += 1'''
P1_NEW = '''                       and (j == i + 1 or not est_verbe(mots[j][0], mots[j][2]))
                       # le GN ne traverse pas un **pronom sujet** devant un verbe :
                       # « The film | she talks about » (relative zéro, r035)
                       and not (j > i + 1
                                and _normaliser(mots[j][2]) in (
                 
… [13004 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/seg && cat classer.py && echo \"===CROISEMENTS===\" && cat croisements.py", "description": "Read classer and croisements scripts"}`

  ```
"""Classe les erreurs GV (FP/FN) du gold 612, sur une variante donnée."""
import collections
import json
import pathlib
import sys

REPO = pathlib.Path("/home/stephane/Data13TB/stephane/GitHub/Qtrinet")
VAR = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(VAR / "tools"))
sys.path.insert(0, str(REPO / "tools/tests/linguistique"))
import bloc_linguistique as bl  # noqa: E402
import evaluer_gold as eg  # noqa: E402

assert str(bl.__file__).startswith(str(VAR))
phrases = eg.charger()
h = bl.Heuristique()
fp_c = collections.Counter()
fn_c = collections.Counter()
double_c = collections.Counter()
origine = collections.Counter()
ex = collections.defaultdict(list)
for p in phrases:
    a = h.analyser(p["texte"], p["langue"])
    segs = [(e.type, e.debut, e.fin, e.valeur, e.confiance, (e.meta or {}).get("union"))
            for e in a.etiquettes if e.niveau == "syntagme"]
    pm = {(m["debut"], m["fin"]): m["pos"] for m in p["mots"]}
    pred = {(s[0], s[1], s[2]) for s in segs}
    gold = {(s["type"], s["debut"], s["fin"]) for s in p["segments"]}
    gold_gv = [(s["debut"], s["fin"]) for s in p["segments"] if s["type"] == "GV"]
    pred_gv = [s for s in segs if s[0] == "GV"]
    tp_gv = 
… [5255 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/bloc_linguistique.py && grep -n \"def _syntagmes_simple\\|GV\\|ADVERBES_SEULS\\|ADVERBES_TEMPS\\|def _pos\\|class Heuristique\\|def analyser\" tools/bloc_linguistique.py | head -80", "description": "Locate GV logic in blo … [16 caractères tronqués]`

  ```
2785 tools/bloc_linguistique.py
139:    def analyser(self, texte: str, langue: str | None = None,
476:ADVERBES_SEULS = {"peut-être", "vite", "bien", "mal", "hier", "demain", "aujourd'hui", "ici",
482:    """Un GV d'un seul token adverbe n'est pas un gouverneur (« Peut-être »)."""
484:            and _normaliser(g.get("texte") or "") in ADVERBES_SEULS)
788:class Heuristique:
855:    def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
918:        (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
932:        """REL → tête du GN précédent ; SUB après un GV → son verbe (le gouverneur)."""
937:        if segment.get("type") == "SUB" and precedent.get("type") == "GV":
951:        if segment.get("type") == "SUB" and precedent.get("type") == "GV":
965:        """Cible vide d'un GP : génitif → tête du GN à gauche (sinon None, le GV tranchera)."""
987:        """Un GP n'est pas gouverné par un mot de son span : on prend la tête du GV extérieur.
990:        tête du GV extérieur `est prêt` → `prêt` (mesuré : g012, r018).
1052:        """`_verbe_dans` mémoïsé par span de GV : le même GV est relu pour chaque segment."""
1065:        """La cible d'un segment : le **ver
… [3429 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '460,500p' tools/bloc_linguistique.py && echo \"===1116-1330===\" && sed -n '1116,1340p' tools/bloc_linguistique.py", "description": "Read chunker GV section"}`

  ```
speak speaks spoke spoken speaking voler vole voles volent volait
rêver rêve rêves rêvent rêvait sauter saute sautes sautent sautait
marcher marche marches marchent marchait
""".split())


AUXILIAIRES = set("""
suis es est sommes êtes sont étais était étions étiez étaient été sera serai seras seront
serais serait serions seriez seraient sois soit soyons soyez soient étant
ai as a avons avez ont avais avait avions aviez avaient aurai auras aura aurons aurez auront
aurais aurait aurions auriez auraient aie aies ait ayons ayez aient ayant eu
am is are was were be been being have has had having do does did done
would must can could should will shall may might ought cannot
""".split())


ADVERBES_SEULS = {"peut-être", "vite", "bien", "mal", "hier", "demain", "aujourd'hui", "ici",
                  "là", "souvent", "toujours", "jamais", "déjà", "encore", "enfin", "alors",
                  "puis", "donc", "aussi", "très", "trop", "plus", "moins", "maybe", "perhaps"}


def _est_adverbe_seul(g: dict) -> bool:
    """Un GV d'un seul token adverbe n'est pas un gouverneur (« Peut-être »)."""
    return (len((g.get("texte") or "").split()) == 1
            and _normaliser(g.get("texte") or "")
… [13988 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/porte-bloc-linguistique.sh && echo \"=== autotest relevant ===\" && grep -n \"183\\|attachement\\|0.7549\\|7549\\|0.8625\\|237\\|238\" tools/pensee/autotest.py | head -40", "description": "Read gate and autotest constants"}`

  ```
#!/usr/bin/env bash
# Porte du bloc linguistique — tests de contrat + mesure UDHR (langue/script).
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "=== PORTE BLOC LINGUISTIQUE ==="
python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' || { echo "❌ tests"; exit 1; }
python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl --sortie /tmp/bloc-linguistique-porte.json || { echo "❌ autotest"; exit 1; }
python3 tools/tests/linguistique/gold.py >/dev/null || { echo "❌ gold"; exit 1; }
python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold-porte.json >/dev/null || { echo "❌ évaluation gold"; exit 1; }
echo "✅ porte bloc linguistique verte"
=== autotest relevant ===
1640:            and abs(r["pos"]["exactitude"] - 0.8625) < 0.001), (
2026:    return abs(r_conf - 0.8625) < 0.001 and abs(r_niv - 0.754) < 0.001 and r_conf > r_niv, (
2061:    return abs(pos - 0.8625) < 0.001, f"élision : POS {pos}"
2222:def t153_attachement() -> tuple[bool, str]:
2223:    """L'attachement sur le gold 612 (239 cibles) : top1 0,9247, exact 0,9247, couverture 0,9247."""
2226:    r = evaluer_bloc("h", bl.Heuristique(), charger(
… [2551 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '200,320p' tools/tests/linguistique/evaluer_gold.py", "description": "Read rest of evaluer_gold"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2200,2260p' tools/pensee/autotest.py && echo \"=== 2320-2470 ===\" && sed -n '2320,2470p' tools/pensee/autotest.py", "description": "Read autotest attachment tests"}`

  ```
racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-quatre-modes-432-soustype-t03.json").read_text(encoding="utf-8"))
    m = d["modes"]["parallele_niveau"]["all"]["pragmatique"]
    h = d["modes"]["heuristique"]["all"]["pragmatique"]
    return abs(m["double_sens"] - 0.9838) < 0.001 and m["double_sens"] > h["double_sens"], (
        f"sous-type 0,3 : double sens {m['double_sens']} > {h['double_sens']}")


def t152_tirages() -> tuple[bool, str]:
    """Les trois tirages : 0,9838 exactement — le modèle est déterministe sur ces invites."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    val = []
    for suffixe in ("", "b", "c"):
        f = racine / f"reports/pensee-quatre-modes-432-soustype-t03{suffixe}.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        val.append(round(d["modes"]["parallele_niveau"]["all"]["pragmatique"]["double_sens"], 4))
    return val == [0.9838, 0.9838, 0.9838], (
        f"tirages : {val} (écart-type 0, modèle déterministe)")


def t153_attachement() -> tuple[bool, str]:
    """L'attachement sur le gold 612 (239 cibles) : top1 0,9247, exact 0,9247, 
… [8704 caractères tronqués]
  ```

- **bash** `{"command": "set -e\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nrm -rf /tmp/gv && mkdir -p /tmp/gv/variants/base/tools\ncp tools/bloc_linguistique.py /tmp/gv/variants/base/tools/\nln -s /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures /tmp/gv/variants/base/tools/structures\n … [635 caractères tronqués]`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/gv && ls -la && cat err.txt 2>/dev/null | head -30 && python3 classer.py variants/base 2>&1 | head -40", "description": "Debug classer run"}`

  ```
total 12
drwxr-xr-x.   3 stephane stephane   140  7 nov 12:42 .
drwxrwxrwt. 319 root     root     27760  7 nov 12:42 ..
-rw-r--r--.   1 stephane stephane     0  7 nov 12:42 class_base.json
-rw-r--r--.   1 stephane stephane  3805  7 nov 12:42 classer.py
-rw-r--r--.   1 stephane stephane  2636  7 nov 12:42 croisements.py
-rw-r--r--.   1 stephane stephane   198  7 nov 12:42 err.txt
drwxr-xr-x.   3 stephane stephane    60  7 nov 12:42 variants
Traceback (most recent call last):
  File "/tmp/gv/classer.py", line 14, in <module>
    assert str(bl.__file__).startswith(str(VAR))
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
AssertionError
Traceback (most recent call last):
  File "/tmp/gv/classer.py", line 14, in <module>
    assert str(bl.__file__).startswith(str(VAR))
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
AssertionError
  ```

- **bash** `{"command": "cd /tmp/gv && python3 classer.py /tmp/gv/variants/base > class_base.json 2>err.txt; echo \"exit=$?\"; cat err.txt | head; python3 -c \"\nimport json\nd=json.load(open('/tmp/gv/class_base.json'))\nprint('FP',d['fp_total'],d['fp'])\nprint('FN',d['fn_total'],d['fn'])\nprint('double',d['dou … [258 caractères tronqués]`

  ```
exit=0
FP 320 {'objet': 73, 'sujet': 144, 'adverbe': 16, 'tronque': 39, 'parasite': 16, 'deux_cotes': 27, 'gauche_autre': 5}
FN 179 {'chev_deux': 28, 'avale_GN': 51, 'chev_droite': 75, 'chev_gauche': 6, 'tronque': 19}
double 153 {'objet': 4, 'sujet': 133, 'adverbe': 1, 'tronque': 11, 'deux_cotes': 1, 'gauche_autre': 3}
origine {'chunker': 96, 'S': 224}
--- objet
  g003 fp a vu l'homme | La femme a vu l'homme dans le parc.
  g014 fp vu l'homme | J'ai vu l'homme avec le télescope.
  r023 fp love music | We love music.
  r056 fp arrivent demain matin | Ils arrivent demain matin.
  r065 fp watches television | She watches television.
--- sujet
  g004 fp Il a couru | Il a couru pour attraper le bus.
  g005 fp Elle a dit | Elle a dit qu'elle viendrait hier.
  g008 fp Marie lit | Marie lit un livre.
  g009 fp Il ne dort pas | Il ne dort pas.
  g014 fp J'ai vu | J'ai vu l'homme avec le télescope.
--- adverbe
  g010 fp Viens ici | Viens ici !
  r010 fp viens demain | Tu viens demain ?
  r019 fp souffle fort | Le vent souffle fort.
  r030 fp come tomorrow | You come tomorrow?
  r039 fp blows hard | The wind blows hard.
--- tronque
  g013 fp venir | Peux-tu venir ?
  s004 fp ouvre | mon calme
… [2020 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1345,1450p' tools/bloc_linguistique.py", "description": "Read analyser start"}`

  ```
def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        if not isinstance(texte, str):
            # une entrée non textuelle est **refusée** proprement (le produit ne plante pas)
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
        trace.append({"etape": "langue", "langue": lg, "script": script, "confiance": conf_l
… [5204 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class .*S\\b\\|Segmenter\\|_segments_s\\|segmenter_s\\|0.55\\|0.4,\" tools/bloc_linguistique.py | head -40", "description": "Find S segmenter"}`

  ```
700:    # (a) un point entre deux chiffres est décimal (12.5, 12.03.2024, 192.168.1.10)
793:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
794:                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
797:        self.segmenter_s = segmenter_s
875:            return "NOUN", True, 0.55
903:        if not self.segmenter_s:
920:        if not self.segmenter_s:
1515:                etiquettes.append(Etiquette("phrase", "modalité", "oui", d, f, self.nom, 0.55,
1598:                                                0.55 if len(cands) == 1 else 0.4,
1657:                                                self.nom, 0.55, candidats=[relation],
1733:        h = Heuristique(segmenter_s=False)
1847:class NeuronalLLMPOS:
1859:    La confiance par défaut (`0.6`) est **celle du seuil ouvert de l'heuristique** (0.55) : dans
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '890,945p' tools/bloc_linguistique.py && echo \"=== 1520-1680 ===\" && sed -n '1520,1680p' tools/bloc_linguistique.py", "description": "Read S segmenter and fusion"}`

  ```
sortie = []
        for suf in SUFFIXES:
            if len(n) > len(suf) + 2 and n.endswith(suf):
                sortie.append(("suffixe", len(mot) - len(suf), len(mot), suf))
                break
        for pre in PREFIXES:
            if len(n) > len(pre) + 2 and n.startswith(pre):
                sortie.append(("préfixe", 0, len(pre), pre))
                break
        return sortie

    # -- syntagmes ----------------------------------------------------------
    def _syntagmes_s(self, texte: str) -> list[dict] | None:
        if not self.segmenter_s:
            return None
        try:
            if str(RACINE / "tools/structures") not in sys.path:
                sys.path.insert(0, str(RACINE / "tools/structures"))
            import generateur  # le générateur S, importé en lecture seule
            return generateur.analyser(texte)
        except Exception:
            return None

    def _cibles_s(self, texte: str) -> dict:
        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).

        Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut reten
… [12099 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools/structures')\nimport generateur as g\nfor txt in [\"Il a couru pour attraper le bus.\",\"Marie lit un livre.\",\"We love music.\",\"Elle a dit qu'elle viendrait hier.\",\"J'ai v … [295 caractères tronqués]`

  ```
== Il a couru pour attraper le bus.
  None None None None role= None
  None None None None role= None
== Marie lit un livre.
  None None None None role= None
== We love music.
  None None None None role= None
== Elle a dit qu'elle viendrait hier.
  None None None None role= None
== J'ai vu l'homme avec le télescope.
  None None None None role= None
  None None None None role= None
== Le garçon joue au ballon.
  None None None None role= None
  None None None None role= None
== Tu viens demain ?
  None None None None role= None
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools/structures')\nimport generateur as g\nfor txt in [\"Il a couru pour attraper le bus.\",\"Marie lit un livre.\",\"Elle a dit qu'elle viendrait hier.\",\"J'ai vu l'homme avec le t … [326 caractères tronqués]`

  ```
== Il a couru pour attraper le bus.
  dict {}
  dict {}
== Marie lit un livre.
  dict {}
== Elle a dit qu'elle viendrait hier.
  dict {}
== J'ai vu l'homme avec le télescope.
  dict {}
  dict {}
== Le garçon joue au ballon.
  dict {}
  dict {}
== Tu viens demain ?
  dict {}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools/structures')\nimport generateur as g\nprint(g.analyser(\"Il a couru pour attraper le bus.\"))\nprint('---')\nprint(g._segmente(\"Il a couru pour attraper le bus.\", g._tok … [87 caractères tronqués]`

  ```
[{'nom': '« pour attraper le bus » → Il a couru', 'lecture': '« pour attraper le bus » se rattache à « Il a couru »', 'attachement': {'segment': 'pour attraper le bus', 'cible': 'Il a couru', 'genre': 'GV'}, 'segments': [{'debut': 0, 'fin': 10, 'texte': 'Il a couru', 'type': 'GV', 'role': 'predicat', 'niveau': 0, 'parent': None, 'profondeur': 0}, {'debut': 11, 'fin': 31, 'texte': 'pour attraper le bus', 'type': 'GP', 'role': 'but', 'niveau': 1, 'parent': 0, 'profondeur': 1}]}, {'nom': '« pour attraper le bus » = cause', 'lecture': '« pour attraper le bus » est un complément de cause.', 'attachement': None, 'segments': [{'debut': 0, 'fin': 10, 'texte': 'Il a couru', 'type': 'GV', 'role': 'predicat', 'niveau': 0, 'parent': None, 'profondeur': 0}, {'debut': 11, 'fin': 31, 'texte': 'pour attraper le bus', 'type': 'GP', 'role': 'cause', 'niveau': 1, 'parent': 0, 'profondeur': 1}]}]
---
[<generateur.Segment object at 0x7f744cf602c0>, <generateur.Segment object at 0x7f744cf60340>]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools/structures')\nimport generateur as g\nfor txt in [\"Marie lit un livre.\",\"Elle a dit qu'elle viendrait hier.\",\"J'ai vu l'homme avec le télescope.\",\"Le garçon joue au ballo … [268 caractères tronqués]`

  ```
== Marie lit un livre.
   {'debut': 0, 'fin': 9, 'texte': 'Marie lit', 'type': 'GV', 'role': 'predicat', 'niveau': 0, 'parent': None, 'profondeur': 0}
   {'debut': 10, 'fin': 18, 'texte': 'un livre', 'type': 'GN', 'role': 'patient', 'niveau': 1, 'parent': 0, 'profondeur': 1}
== Elle a dit qu'elle viendrait hier.
   {'debut': 0, 'fin': 10, 'texte': 'Elle a dit', 'type': 'GV', 'role': 'predicat', 'niveau': 0, 'parent': None, 'profondeur': 0}
   {'debut': 11, 'fin': 28, 'texte': "qu'elle viendrait", 'type': 'SUB', 'role': 'contenu', 'niveau': 1, 'parent': 0, 'profondeur': 1}
   {'debut': 29, 'fin': 33, 'texte': 'hier', 'type': 'GP', 'role': 'temps', 'niveau': 1, 'parent': 0, 'profondeur': 1}
== J'ai vu l'homme avec le télescope.
   {'debut': 0, 'fin': 7, 'texte': "J'ai vu", 'type': 'GV', 'role': 'predicat', 'niveau': 0, 'parent': None, 'profondeur': 0}
   {'debut': 8, 'fin': 15, 'texte': "l'homme", 'type': 'GN', 'role': 'patient', 'niveau': 1, 'parent': 0, 'profondeur': 1}
   {'debut': 16, 'fin': 33, 'texte': 'avec le télescope', 'type': 'GP', 'role': 'attribut', 'niveau': 1, 'parent': 1, 'profondeur': 2}
== Le garçon joue au ballon.
   {'debut': 0, 'fin': 9, 'texte': 'Le garçon', 'ty
… [1707 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"syntagme\\|\\.754\\|0\\.75\\|f1\\b\" tools/pensee/autotest.py | head -80", "description": "Find F1 assertions in autotest"}`

  ```
56:    f1 = m.store.put(a)
58:    if f1 != f2:
60:    if m.store.get(f1) is None:
62:    if m.store.put(a) != f1:
65:    if m.store.put(different) == f1:
1370:    """Les phrases complexes : POS 0,6471, syntagme 0,4828 sur r201-r205."""
1380:        f"syntagme {round(r['syntagme']['f1'], 4)}")
1384:    """Les 20 phrases complexes : POS 0,6829, syntagme 0,2963."""
1394:        f"syntagme {round(r['syntagme']['f1'], 4)}")
1398:    """Les 50 phrases complexes : POS 0,7013, syntagme 0,3060."""
1408:        f"syntagme {round(r['syntagme']['f1'], 4)}")
1412:    """Les 100 phrases complexes : POS 0,6984, syntagme 0,2677."""
1422:        f"syntagme {round(r['syntagme']['f1'], 4)}")
1642:        f"tête {round(r['syntagme']['tete']['f1'], 4)}")
1681:    f1 = round(r1["syntagme"]["f1"], 4)
1682:    f2 = round(r2["syntagme"]["f1"], 4)
1683:    t1 = round(r1["syntagme"]["tete"]["f1"], 4)
1684:    t2 = round(r2["syntagme"]["tete"]["f1"], 4)
1685:    return (abs(f1 - 0.6007) < 0.001 and abs(f2 - 0.8152) < 0.001
1687:        f"segmenteur : S F1 {f1} tête {t1} ; chunker F1 {f2} tête {t2}")
1703:        seg_s = [(e.type, e.debut, e.fin) for e in a1.etiquettes if e.niveau == "syntagme"]
1704:        s
… [2997 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/seg && cat measure.py", "description": "Read measure.py"}`

  ```
"""Mesure une variante de bloc_linguistique (copie patchée en /tmp/seg/variants/<nom>)."""
import json
import pathlib
import sys

REPO = pathlib.Path("/home/stephane/Data13TB/stephane/GitHub/Qtrinet")
VAR = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(VAR / "tools"))
sys.path.insert(0, str(REPO / "tools/tests/linguistique"))

import bloc_linguistique as bl  # noqa: E402
import evaluer_gold as eg  # noqa: E402
from gold_split import dev, test  # noqa: E402

assert str(bl.__file__).startswith(str(VAR)), bl.__file__

phrases = eg.charger()
part = sys.argv[2] if len(sys.argv) > 2 else "alternative"
h = bl.Heuristique(partition=part)
sortie = {"variante": VAR.name, "partition": part, "module": str(bl.__file__), "mesures": {}, "phrases": {}}
gele = eg.charger_gele()
for nom, ps in [("all", phrases), ("gele", gele), ("dev", dev(phrases)), ("test", test(phrases))]:
    r = eg.evaluer_bloc(nom, h, ps)
    s, a, t = r["syntagme"], r["attachement"], r["syntagme"]["tete"]
    sortie["mesures"][nom] = {
        "f1": s["f1"], "precision": s["precision"], "rappel": s["rappel"],
        "tp": s["tp"], "fp": s["fp"], "fn": s["fn"],
        "tete_f1": t["f1"],
        "att_cibles": a["cibles"],
… [1389 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nfor f in ('tools/tests/linguistique/gold.json','tools/tests/linguistique/gold_reel.json'):\n    d=json.load(open(f))['phrases']\n    for p in d:\n        if p['id'] in ('g003','g004','g008','g009','r02 … [359 caractères tronqués]`

  ```
== g003 fr La femme a vu l'homme dans le parc.
   GN 0 8 'La femme' cible= None cibles= None
   GV 9 13 'a vu' cible= None cibles= None
   GN 14 21 "l'homme" cible= None cibles= None
   GP 22 34 'dans le parc' cible= vu cibles= ['vu', "l'homme"]
== g004 fr Il a couru pour attraper le bus.
   GN 0 2 'Il' cible= None cibles= None
   GV 3 10 'a couru' cible= None cibles= None
   GP 11 31 'pour attraper le bus' cible= couru cibles= ['couru']
== g008 fr Marie lit un livre.
   GN 0 5 'Marie' cible= None cibles= None
   GV 6 9 'lit' cible= None cibles= None
   GN 10 18 'un livre' cible= None cibles= None
== g009 fr Il ne dort pas.
   GN 0 2 'Il' cible= None cibles= None
   GV 3 14 'ne dort pas' cible= None cibles= None
== r010 fr Tu viens demain ?
   GN 0 2 'Tu' cible= None cibles= None
   GV 3 8 'viens' cible= None cibles= None
== r019 fr Le vent souffle fort.
   GN 0 7 'Le vent' cible= None cibles= None
   GV 8 15 'souffle' cible= None cibles= None
== r023 en We love music.
   GN 0 2 'We' cible= None cibles= None
   GV 3 7 'love' cible= None cibles= None
   GN 8 13 'music' cible= None cibles= None
== r030 en You come tomorrow?
   GN 0 3 'You' cible= None cibles= None
   GV 4 8 'come' ci
… [807 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/gv && python3 croisements.py /tmp/gv/variants/base 2>&1 | head -20", "description": "Cross-tab FP categories by origin"}`

  ```
FP par classe×origine: {'adverbe|S': 2, 'adverbe|chunker': 14, 'deux_cotes|S': 21, 'deux_cotes|chunker': 6, 'gauche_autre|S': 3, 'gauche_autre|chunker': 2, 'objet|S': 20, 'objet|chunker': 53, 'parasite|S': 11, 'parasite|chunker': 5, 'sujet|S': 142, 'sujet|chunker': 2, 'tronque|S': 25, 'tronque|chunker': 14}
doublons par classe×origine: {'adverbe|chunker': 1, 'deux_cotes|S': 1, 'gauche_autre|S': 3, 'objet|S': 3, 'objet|chunker': 1, 'sujet|S': 133, 'tronque|S': 10, 'tronque|chunker': 1}
FN: {'chev_deux': 28, 'avale_GN': 51, 'chev_droite': 75, 'chev_gauche': 6, 'tronque': 19}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^SUJETS\\|SUJETS =\\|_ELISIONS\\|ELISIONS\" tools/bloc_linguistique.py | head && sed -n '40,90p' tools/bloc_linguistique.py", "description": "Find SUJETS and elisions"}`

  ```
378:SUJETS = {"i", "you", "he", "she", "it", "we", "they", "there", "who", "that", "which",
859:        _ELISIONS = {"j": "je", "l": "le", "d": "de", "qu": "que", "n": "ne",
861:        n = _ELISIONS.get(n, n)
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

    def j
… [383 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '375,390p' tools/bloc_linguistique.py && sed -n '850,875p' tools/bloc_linguistique.py", "description": "Read SUJETS and elisions map"}`

  ```
# les subordonnants qui n'ont pas d'antécédent : toujours SUB
AMBIGUES_PREP = {"since", "before", "after", "until", "as", "depuis", "avant", "après", "pendant", "durant"}

SUJETS = {"i", "you", "he", "she", "it", "we", "they", "there", "who", "that", "which",
          "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles", "qui", "qu"}

SUBORDONNANTS = {"because", "although", "though", "if", "while", "as", "since", "unless",
                 "whether", "car", "parce", "puisque", "comme", "quand", "si", "lorsque"}
# « car » est français : en anglais c'est un nom commun (r280)
# marqueurs **ambigus** : relatifs après un GN (« The day when we left »), SUB ailleurs
AMBIGUES_REL = {"when", "where", "why", "how", "quand", "où", "pourquoi", "comment"}

SUB_PAR_LANGUE = {"fr": {"car", "parce", "puisque", "comme", "quand", "si", "lorsque"},
                  "en": {"because", "although", "though", "if", "while", "as", "since",
                         "unless", "whether", "when"}}

        return bool(re.search(r"\b(?:peut|peuvent|peux|pouvons|pouvez|doit|doivent|devons|devez|"
                              r"pourrait|pourraient|pourrais|devrait|devraient|voudrais|voudrait|"
      
… [1313 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"partition\" tools/bloc_linguistique.py | head -30 && sed -n '788,810p' tools/bloc_linguistique.py", "description": "Inspect partition parameter"}`

  ```
795:                 union: bool = True, partition: str = "alternative"):
804:        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
806:        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
807:            raise ValueError("partition attend 'brut', 'alternative', 'filtrer_union' ou 'filtrer'")
808:        self.partition = partition
1684:        if self.partition != "brut":
1685:            _expliciter_partition(etiquettes, filtrer=(
1686:                "" if self.partition == "alternative"
1687:                else "union" if self.partition == "filtrer_union" else "strict"))
2264:def _relation_partition(x: Etiquette, y: Etiquette) -> str:
2286:def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:
2310:def _expliciter_partition(etiquettes: list[Etiquette], filtrer: str = "") -> None:
2313:    `meta.partition` porte le groupe, le rang et la vue ; `meta.alternative` porte les
2319:    le chunker est la partition — **tous** les segments `union` sont conservés, et tous
2324:    groupes = _groupes_partition(segs)
2361:            meta["partition"] = {"groupe": gid, "rang": rangs[id(e)][1],
2373:               
… [1409 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _mots\" tools/bloc_linguistique.py && sed -n '680,760p' tools/bloc_linguistique.py", "description": "Read _mots"}`

  ```
820:    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
    """Un saut de ligne coupe la phrase s'il est vide ou s'il borde un titre / une liste."""
    if texte.count("\n", i, j) >= 2:
        return True
    avant = texte[texte.rfind("\n", 0, i) + 1:i]
    fin = texte.find("\n", j)
    apres = texte[j:fin if fin >= 0 else len(texte)]
    return bool(_MARQUEUR.match(avant) or _MARQUEUR.match(apres))


def _type_phrase(ponctuation: str) -> str:
    if "?" in ponctuation:
        return "interrogative"
    if "!" in ponctuation:
        return "exclamative"
    return "déclarative"


def _est_frontiere(texte: str, i: int, j: int, zones: list[tuple[int, int]]) -> bool:
    n = len(texte)
    terme = texte[i:j]
    # (a) un point entre deux chiffres est décimal (12.5, 12.03.2024, 192.168.1.10)
    if terme == "." and 0 < i < n - 1 and texte[i - 1].isdigit() and texte[i + 1].isdigit():
        return False
    # (a bis) un numéro de liste en début de ligne (1. Ouvrir) n'est pas une phrase
    if terme == "." and 0 < i < n - 1 and texte[i + 1].isspace():
        avant = texte[texte.rfind("\n", 0, i) + 1:i].strip()
        if avant.isdigit() and len(avant) <= 3:
            ret
… [2210 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '815,850p' tools/bloc_linguistique.py", "description": "Read _mots body"}`

  ```
return "und", conf, script
        return langue, conf, script

    # -- tokens -------------------------------------------------------------
    @staticmethod
    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
        motif = re.compile(r"\b[ldmtsnLDMTNS]['’](?=\w)|\w+(?:['’\-]\w+)*|\d+(?:[.,]\d+)*|https?://\S+|[\U0001F300-\U0001FAFF]|[^\w\s]")
        sortie = []
        for m in motif.finditer(texte):
            t = m.group()
            if t.startswith(("http://", "https://")):
                typ = "url"
            elif t[0].isdigit():
                typ = "nombre"
            elif re.fullmatch(r"[^\w\s]", t):
                typ = "ponctuation"
            elif len(t) == 1 and ord(t) >= 0x1F300:
                typ = "emoji"
            else:
                typ = "mot"
            sortie.append((m.start(), m.end(), t, typ))
        return sortie

    @staticmethod
    def _phrases(texte: str) -> list[tuple[int, int, str, str]]:
        return decouper_phrases(texte)


    @staticmethod
    def _negation(phrase: str) -> bool:
        return bool(re.search(r"\b(?:ne|n['’])\b.{0,40}\b(?:pas|plus|jamais|rien|guère)\b", phrase, re.I)
                    or re.search
… [214 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections, json\nsys.path.insert(0,'tools/structures'); sys.path.insert(0,'tools')\nimport generateur as g\nfrom bloc_linguistique import Heuristique, POS_FERME, SUJETS, _normaliser, _est_verbe, AUXIL … [1280 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 24, in <module>
TypeError: _est_verbe() takes 1 positional argument but 2 were given
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections, json\nsys.path.insert(0,'tools/structures'); sys.path.insert(0,'tools')\nimport generateur as g\nfrom bloc_linguistique import Heuristique, POS_FERME, SUJETS, _normaliser, _est_verbe, AUXIL … [1132 caractères tronqués]`

  ```
('PRON', True, False) 86 [('g004', 'Il a couru'), ('g005', 'Elle a dit'), ('g014', "J'ai vu")]
('VERB', False, True) 71 [('g001', 'dort'), ('g007', 'jouent'), ('r001', 'mange')]
('PRON', False, False) 45 [('g009', 'Il ne dort pas'), ('r008', 'Il pleut'), ('r009', 'Je ne comprends pas')]
('AUX', False, False) 27 [('g011', 'est intéressant'), ('r014', 'est passionnant'), ('r054', 'est long')]
('NOUN', False, True) 24 [('r011', 'part'), ('r082', 'tombe'), ('r085', 'vend')]
('NOUN', False, False) 23 [('g008', 'Marie lit'), ('r056', 'matin'), ('r089', 'urs')]
('NOUN', True, False) 19 [('g013', 'Peux-tu venir'), ('r183', 'Marie écrit'), ('r325', 'Marie lisent')]
('ADV', False, False) 11 [('r309', 'Peut-être'), ('r408', 'Ne viens-tu pas'), ('r409', 'Ne mange-t-il pas')]
('AUX', False, True) 10 [('g012', 'est prêt'), ('r012', 'est rapide'), ('r018', 'est prête')]
('VERB', False, False) 8 [('g010', 'Viens'), ('r305', 'Ferme'), ('s025', 'Cherche')]
('ADV', False, True) 7 [('r331', 'aiment'), ('s063', 'pas'), ('s080', 'pas')]
('AUX', True, True) 4 [('r058', 'est ouverte'), ('r132', 'est accroché'), ('s031', 'sont rêve')]
('VERB', True, True) 4 [('s008', 'peut compte'), ('s023', 'doit dessine'
… [164 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nfor f in ('tools/tests/linguistique/gold.json','tools/tests/linguistique/gold_reel.json'):\n    for p in json.load(open(f))['phrases']:\n        if p['id'] in ('g014','g013','g005','g009','r183'):\n    … [231 caractères tronqués]`

  ```
== g005 Elle a dit qu'elle viendrait hier.
   GN 0 4 'Elle'
   GV 5 10 'a dit'
   SUB 11 28 "qu'elle viendrait"
== g009 Il ne dort pas.
   GN 0 2 'Il'
   GV 3 14 'ne dort pas'
== g013 Peux-tu venir ?
   GV 0 13 'Peux-tu venir'
== g014 J'ai vu l'homme avec le télescope.
   GN 0 4 "J'ai"
   GV 5 7 'vu'
   GN 8 15 "l'homme"
   GP 16 33 'avec le télescope'
== r183 Marie écrit une lettre.
   GN 0 5 'Marie'
   GV 6 11 'écrit'
   GN 12 22 'une lettre'
  ```

- **bash** `{"command": "mkdir -p /tmp/gv && cat > /tmp/gv/build.py <<'PYEOF'\n\"\"\"Construit les variantes GV depuis le bloc courant (post-r035).\"\"\"\nimport pathlib, shutil, sys\n\nREPO = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nSRC = REPO / \"tools/bloc_linguistique.py\"\nROOT =  … [6455 caractères tronqués]`

  ```
écrit base
écrit gv_adverbe
écrit gv_sujet
écrit gv_deux
  ```

- **bash** `{"command": "cat > /tmp/gv/measure.py <<'PYEOF'\n\"\"\"Mesure une variante GV sur all/gele/dev/test + par langue/source.\"\"\"\nimport json, pathlib, sys\nREPO = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nVAR = pathlib.Path(sys.argv[1])\nsys.path.insert(0, str(VAR / \"tools\" … [3205 caractères tronqués]`

  ```
variante          F1     dev    test    tp   fp   fn     POS       att    couv
base          0.7549  0.7498  0.7663  1466  555  397  0.8625 237/238  0.9958
gv_adverbe    0.7575  0.7520  0.7696  1471  550  392  0.8625 237/238  0.9958
gv_sujet      0.7829  0.7813  0.7866  1477  433  386  0.8625 237/238  0.9958
gv_deux       0.7850  0.7826  0.7904  1479  426  384  0.8625 237/238  0.9958
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections\nph=json.load(open('tools/tests/linguistique/gold.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_synt … [966 caractères tronqués]`

  ```
GV finissant par ADV: 39
  ('g009', 'fr', 'Il ne dort pas.', 'ne dort pas')
  ('r009', 'fr', 'Je ne comprends pas.', 'ne comprends pas')
  ('r035', 'en', 'The film she talks about is out.', 'is out')
  ('r186', 'fr', 'Le vent souffle fort.', 'souffle fort')
  ('r189', 'fr', 'La voiture roule vite.', 'roule vite')
  ('r190', 'fr', 'Ils arrivent demain.', 'arrivent demain')
  ('r197', 'en', 'The children play outside.', 'play outside')
  ('r198', 'en', 'My sister sings well.', 'sings well')
  ('r199', 'en', 'The train arrives late.', 'arrives late')
  ('r284', 'en', 'Although it rains, he goes out.', 'goes out')
  ('r306', 'fr', 'Il ne vient pas.', 'ne vient pas')
  ('r312', 'en', 'She came, but she leaves again.', 'leaves again')
  ('r348', 'fr', 'La voiture est rouge ; elle roule vite.', 'roule vite')
  ('r351', 'fr', 'Le train part ; il arrive tard.', 'arrive tard')
  ('r356', 'fr', 'La maison est vieille ; elle tient encore.', 'tient encore')
  ('r362', 'en', 'The car is red; it runs fast.', 'runs fast')
  ('r365', 'en', 'The train leaves; it arrives late.', 'arrives late')
  ('r374', 'fr', 'La fleur pousse ; elle sent bon.', 'sent bon')
  ('s013', 'fr', 'elle ne compte pas', 'ne
… [1814 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nph=json.load(open('tools/tests/linguistique/gold.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_synthetique.json' … [419 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
KeyError: 'source'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nph=json.load(open('tools/tests/linguistique/gold.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_synthetique.json' … [431 caractères tronqués]`

  ```
== g010 fr None Viens ici !
   GV 0 5 'Viens' cible None
   GP 6 9 'ici' cible Viens
== r010 fr reel Tu viens demain ?
   GN 0 2 'Tu' cible None
   GV 3 8 'viens' cible None
== r019 fr reel Le vent souffle fort.
   GN 0 7 'Le vent' cible None
   GV 8 15 'souffle' cible None
== r023 en reel We love music.
   GN 0 2 'We' cible None
   GV 3 7 'love' cible None
   GN 8 13 'music' cible None
== r030 en reel You come tomorrow?
   GN 0 3 'You' cible None
   GV 4 8 'come' cible None
== r039 en reel The wind blows hard.
   GN 0 8 'The wind' cible None
   GV 9 14 'blows' cible None
== r049 fr reel Le bébé dort profondément.
   GN 0 7 'Le bébé' cible None
   GV 8 12 'dort' cible None
== r065 en reel She watches television.
   GN 0 3 'She' cible None
   GV 4 11 'watches' cible None
   GN 12 22 'television' cible None
== r186 fr reel Le vent souffle fort.
   GN 0 7 'Le vent' cible None
   GV 8 20 'souffle fort' cible None
== r189 fr reel La voiture roule vite.
   GN 0 10 'La voiture' cible None
   GV 11 21 'roule vite' cible None
== r190 fr reel Ils arrivent demain.
   GN 0 3 'Ils' cible None
   GV 4 19 'arrivent demain' cible None
== r197 en reel The children play outside.
   GN 0 12 'The chil
… [272 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique\nh=Heuristique()\nfor w in ['ici','fort','hard','profondément','deeply','vite','fast','bien','well','tard','late','demain','tomorrow … [153 caractères tronqués]`

  ```
ici ('ADV', False, 0.92) ('NOUN', True, 0.3)
fort ('ADV', False, 0.92) ('NOUN', True, 0.3)
hard ('NOUN', True, 0.3) ('ADV', False, 0.92)
profondément ('ADV', True, 0.45) ('ADV', True, 0.45)
deeply ('ADV', True, 0.45) ('ADV', True, 0.45)
vite ('NOUN', True, 0.3) ('NOUN', True, 0.3)
fast ('NOUN', True, 0.3) ('NOUN', True, 0.3)
bien ('ADV', False, 0.92) ('NOUN', True, 0.3)
well ('NOUN', True, 0.3) ('ADV', False, 0.92)
tard ('ADV', False, 0.92) ('NOUN', True, 0.3)
late ('NOUN', True, 0.3) ('ADV', False, 0.92)
demain ('ADV', False, 0.92) ('NOUN', True, 0.3)
tomorrow ('NOUN', True, 0.3) ('ADV', False, 0.92)
matin ('NOUN', True, 0.3) ('NOUN', True, 0.3)
pas ('ADV', False, 0.92) ('NOUN', True, 0.3)
plus ('ADV', False, 0.92) ('NOUN', True, 0.3)
jamais ('ADV', False, 0.92) ('NOUN', True, 0.3)
encore ('ADV', False, 0.92) ('NOUN', True, 0.3)
dehors ('NOUN', True, 0.3) ('NOUN', True, 0.3)
outside ('NOUN', True, 0.3) ('ADV', False, 0.92)
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('build.py'); t=p.read_text()\nadd='''\n# --- B large : tout adverbe final (POS) hors du GV, sauf la négation ---\nADV_LARGE_OLD = GB_OLD\nADV_LARGE_NEW = \\'\\'\\'                       # tout adverbe **final** hors du GV,  … [2205 caractères tronqués]`

  ```
ok
écrit base
écrit gv_adverbe
écrit gv_sujet
écrit gv_deux
écrit gv_adverbe_large
écrit placebo_adverbe
placebo_sujet: motif 0 fois : '                if (n0e in _suj or nom_propre) and sv:'
  ```

- **bash** `{"command": "grep -n \"n0e in _suj\" /tmp/gv/build.py /tmp/gv/variants/gv_sujet/tools/bloc_linguistique.py | head", "description": "Check indentation of subject condition"}`

  ```
/tmp/gv/build.py:83:                if (n0e in _suj or nom_propre) and sv:
/tmp/gv/build.py:123:PLACEBO_A_OLD = '''                if (n0e in _suj or nom_propre) and sv:'''
/tmp/gv/variants/gv_sujet/tools/bloc_linguistique.py:945:                if (n0e in _suj or nom_propre) and sv:
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('build.py'); t=p.read_text()\nt=t.replace('if nom in (\"gv_sujet\", \"gv_deux\"):','if nom in (\"gv_sujet\", \"gv_deux\", \"placebo_sujet\"):')\np.write_text(t)\nEOF\npython3 /tmp/gv/build.py 2>&1 | tail -10\ncd /tmp/gv &&  … [699 caractères tronqués]`

  ```
écrit base
écrit gv_adverbe
écrit gv_sujet
écrit gv_deux
écrit gv_adverbe_large
écrit placebo_adverbe
placebo_sujet: motif 0 fois : '                if (n0e in _suj or nom_propre) and sv:'
FAIL placebo_sujet
Traceback (most recent call last):
  File "/tmp/gv/measure.py", line 7, in <module>
    import bloc_linguistique as bl  # noqa
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'bloc_linguistique'
variante                F1     dev    test    tp   fp   fn       att
base                0.7549  0.7498  0.7663  1466  555  397 237/238
gv_adverbe          0.7575  0.7520  0.7696  1471  550  392 237/238
gv_adverbe_large    0.7552  0.7506  0.7656  1467  555  396 237/238
gv_sujet            0.7829  0.7813  0.7866  1477  433  386 237/238
gv_deux             0.7850  0.7826  0.7904  1479  426  384 237/238
placebo_adverbe     0.7440  0.7473  0.7366  1475  627  388 237/238
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
  File "/usr/lib64/python3.13/json/__init__.py", line 298, in load
    return loads(fp.read(),
        cls=cls, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_
… [600 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('build.py'); t=p.read_text()\nold='''    txt = BASE\n    for old, new in patchs:\n        if txt.count(old) != 1:\n            raise SystemExit(f\"{nom}: motif {txt.count(old)} fois : {old[:80]!r}\")\n        txt = txt.repl … [1808 caractères tronqués]`

  ```
écrit base
écrit gv_adverbe
écrit gv_sujet
écrit gv_deux
écrit gv_adverbe_large
écrit placebo_adverbe
écrit placebo_sujet
variante                F1     dev    test    tp   fp   fn       att
base                0.7549  0.7498  0.7663  1466  555  397 237/238
gv_adverbe          0.7575  0.7520  0.7696  1471  550  392 237/238
gv_adverbe_large    0.7552  0.7506  0.7656  1467  555  396 237/238
gv_sujet            0.7829  0.7813  0.7866  1477  433  386 237/238
gv_deux             0.7850  0.7826  0.7904  1479  426  384 237/238
placebo_adverbe     0.7440  0.7473  0.7366  1475  627  388 237/238
placebo_sujet       0.7758  0.7728  0.7826  1476  466  387 237/238
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3 25a6c0ff && git show 25a6c0ff^:tools/bloc_linguistique.py > /tmp/gv/avant_r035.py && wc -l /tmp/gv/avant_r035.py && grep -c \"relative_zero\" /tmp/gv/avant_r035.py", "description": "Extract pre-r035 bloc version" … [1 caractères tronqués]`

  ```
25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
d7469b5c INDEX — RÉGÉNÉRÉ APRÈS L'INVENTAIRE PANINI (702 FICHES) ; ÉTAT HORODATÉ
34fdd4ef DOCS — README T1 TENU (DEUX LIGNES LONGUES RACCOURCIES)
2737 /tmp/gv/avant_r035.py
0
[exit code: 1]
  ```

- **bash** `{"command": "set -e\nmkdir -p /tmp/gv/variants/base_avant_r035/tools\ncp /tmp/gv/avant_r035.py /tmp/gv/variants/base_avant_r035/tools/bloc_linguistique.py\nln -sfn /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures /tmp/gv/variants/base_avant_r035/tools/structures\ncd /tmp/gv\npython3  … [609 caractères tronqués]`

  ```
avant r035 0.7533 1463 558 400 236 237
FP 322 {'objet': 73, 'sujet': 144, 'adverbe': 16, 'tronque': 39, 'parasite': 17, 'gauche_autre': 6, 'deux_cotes': 27}
FN 180 {'chev_deux': 28, 'avale_GN': 51, 'chev_droite': 75, 'chev_gauche': 7, 'tronque': 19}
  ```

- **bash** `{"command": "cd /tmp/gv && for v in gv_adverbe gv_sujet gv_deux placebo_adverbe placebo_sujet gv_adverbe_large; do python3 classer.py /tmp/gv/variants/$v > class_$v.json 2>ec_$v.txt || { echo FAIL $v; head ec_$v.txt; }; done\npython3 - <<'EOF'\nimport json\nfor v in ('base','gv_adverbe','gv_sujet',' … [246 caractères tronqués]`

  ```
base               FP 320 {'objet': 73, 'sujet': 144, 'adverbe': 16, 'tronque': 39, 'parasite': 16, 'deux_cotes': 27, 'gauche_autre': 5} FN 179 {'chev_deux': 28, 'avale_GN': 51, 'chev_droite': 75, 'chev_gauche': 6, 'tronque': 19}
gv_adverbe         FP 315 {'objet': 73, 'sujet': 145, 'adverbe': 10, 'tronque': 40, 'parasite': 16, 'deux_cotes': 25, 'gauche_autre': 6} FN 174 {'chev_deux': 23, 'avale_GN': 51, 'chev_droite': 72, 'chev_gauche': 9, 'tronque': 19}
gv_sujet           FP 197 {'objet': 75, 'adverbe': 16, 'tronque': 41, 'parasite': 16, 'sujet': 28, 'gauche_autre': 3, 'deux_cotes': 18} FN 171 {'tronque': 20, 'avale_GN': 51, 'chev_droite': 80, 'chev_gauche': 3, 'chev_deux': 17}
gv_deux            FP 190 {'objet': 75, 'adverbe': 10, 'tronque': 41, 'parasite': 16, 'sujet': 29, 'gauche_autre': 4, 'deux_cotes': 15} FN 169 {'tronque': 21, 'avale_GN': 51, 'chev_droite': 77, 'chev_gauche': 5, 'chev_deux': 15}
gv_adverbe_large   FP 320 {'objet': 73, 'sujet': 145, 'tronque': 50, 'parasite': 17, 'adverbe': 4, 'deux_cotes': 25, 'gauche_autre': 6} FN 178 {'chev_deux': 23, 'avale_GN': 51, 'chev_droite': 66, 'tronque': 27, 'chev_gauche': 11}
placebo_adverbe    FP 384 {'objet': 26, 'sujet': 143
… [419 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/gv/diff_att.py <<'PYEOF'\n\"\"\"Diff de l'attachement segment par segment entre deux variantes.\"\"\"\nimport json, pathlib, sys\nREPO = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nA = pathlib.Path(sys.argv[1]); B = pathlib.Path(sys.argv[2])\ndef charge … [2481 caractères tronqués]`

  ```
gv_adverbe lost 0 gain 0 span_lost 0
gv_sujet lost 0 gain 0 span_lost 0
gv_deux lost 0 gain 0 span_lost 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections\nph=json.load(open('tools/tests/linguistique/gold.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_synt … [664 caractères tronqués]`

  ```
('fr', 'VERB') 379 []
('en', 'VERB') 211 []
('fr', 'AUX') 50 []
('en', 'AUX') 47 []
('fr', 'ADV') 24 []
('en', 'ADV') 1 []
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport sys, collections, json\nREPO='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nVAR='/tmp/gv/variants/base'\nsys.path.insert(0,VAR+'/tools'); sys.path.insert(0,REPO+'/tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as eg\n … [1058 caractères tronqués]`

  ```
r252 Elle lit et il écrit. | GV 'lit et il écrit' gold GV 'écrit' conf 0.3
r277 She reads and he writes. | GV 'reads and he writes' gold GV 'writes' conf 0.35
  ```

- **bash** `{"command": "cat > /tmp/gv/measure_part.py <<'PYEOF'\nimport json, pathlib, sys\nREPO = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nVAR = pathlib.Path(sys.argv[1]); PART = sys.argv[2]\nsys.path.insert(0, str(VAR / \"tools\")); sys.path.insert(0, str(REPO / \"tools/tests/lingui … [850 caractères tronqués]`

  ```
base alternative {"all": {"f1": 0.7549, "p": 0.7254, "r": 0.7869, "tp": 1466, "fp": 555, "fn": 397, "att": "237/238", "couv": 0.9958}, "dev": {"f1": 0.7498, "p": 0.7245, "r": 0.777, "tp": 1007, "fp": 383, "fn": 289, "att": "161/162", "couv": 0.9939}, "test": {"f1": 0.7663, "p": 0.7274, "r": 0.8095, "tp": 459, "fp": 172, "fn": 108, "att": "76/76", "couv": 1.0}}
base filtrer_union {"all": {"f1": 0.8061, "p": 0.8304, "r": 0.7831, "tp": 1459, "fp": 298, "fn": 404, "att": "231/232", "couv": 0.9707}, "dev": {"f1": 0.8006, "p": 0.8302, "r": 0.7731, "tp": 1002, "fp": 205, "fn": 294, "att": "156/157", "couv": 0.9632}, "test": {"f1": 0.8183, "p": 0.8309, "r": 0.806, "tp": 457, "fp": 93, "fn": 110, "att": "75/75", "couv": 0.9868}}
base filtrer {"all": {"f1": 0.812, "p": 0.8533, "r": 0.7746, "tp": 1443, "fp": 248, "fn": 420, "att": "223/224", "couv": 0.9372}, "dev": {"f1": 0.8028, "p": 0.8487, "r": 0.7616, "tp": 987, "fp": 176, "fn": 309, "att": "149/150", "couv": 0.9202}, "test": {"f1": 0.8329, "p": 0.8636, "r": 0.8042, "tp": 456, "fp": 72, "fn": 111, "att": "74/74", "couv": 0.9737}}
base brut {"all": {"f1": 0.7549, "p": 0.7254, "r": 0.7869, "tp": 1466, "fp": 555, "fn": 397, "att": "237/238",
… [4635 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"linéaire\" reports/rapport-r035.md docs/pilotage/semaine-autonome.md reports/rapport-*.md 2>/dev/null | grep -i \"0,81\\|0.81\\|F1\" | head -20", "description": "Find linear F1 reference"}`

  ```
docs/pilotage/semaine-autonome.md:26:| la convention des GV (322 FP / 180 FN) | F1 **0,7549** (linéaire 0,8104) | [`rapport-r035.md`](../../reports/rapport-r035.md) |
reports/rapport-partition-integree.md:13:> **`filtrer`** (option) donne une vue linéaire : **F1 0,6954 (+0,047)** mais **217/218** (18
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections\nph=json.load(open('tools/tests/linguistique/gold.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_synt … [636 caractères tronqués]`

  ```
textes dupliqués avec annotations différentes: 2
== Le vent souffle fort.
   r019 fr [('GN', 'Le vent'), ('GV', 'souffle')]
   r186 fr [('GN', 'Le vent'), ('GV', 'souffle fort')]
== La voiture roule vite.
   r051 fr [('GN', 'La voiture'), ('GV', 'roule')]
   r189 fr [('GN', 'La voiture'), ('GV', 'roule vite')]
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport json\nbase=json.load(open('m_base.json'))['phrases']\nfor v in ('gv_adverbe','gv_sujet','gv_deux'):\n    d=json.load(open(f'm_{v}.json'))['phrases']\n    print('===',v)\n    n=0\n    for pid in base:\n        if base[pid]!=d[pid]:\n            n+= … [250 caractères tronqués]`

  ```
=== gv_adverbe
  r010 - [('GV', 3, 15)] + [('GV', 3, 8)]
  r030 - [('GV', 4, 17)] + [('GV', 4, 8)]
  r190 - [('GV', 4, 19)] + [('GV', 4, 12)]
  r310 - [('GV', 3, 25)] + [('GV', 3, 14)]
  r314 - [('GV', 0, 20)] + [('GV', 0, 11)]
  r320 - [('GV', 2, 16)] + [('GV', 2, 12)]
  r423 - [('GV', 3, 15)] + [('GV', 3, 8)]
  r427 - [('GV', 4, 17)] + [('GV', 4, 8)]
  r418 - [('GV', 3, 22)] + [('GV', 3, 15)]
  r422 - [('GV', 4, 23)] + [('GV', 4, 14)]
 phrases changées: 10
=== gv_sujet
  g004 - [('GV', 0, 10)] + []
  g005 - [('GV', 0, 10)] + []
  g008 - [('GV', 0, 9)] + []
  g009 - [('GV', 0, 14)] + []
  g013 - [('GV', 0, 13)] + []
  g014 - [('GV', 0, 7)] + [('GV', 5, 7)]
  r003 - [('GV', 0, 11)] + []
  r005 - [('GV', 0, 10)] + []
  r008 - [('GV', 0, 8)] + []
  r009 - [('GV', 0, 19)] + []
  r010 - [('GV', 0, 8)] + [('GV', 3, 8)]
  r013 - [('GV', 0, 14)] + []
  r016 - [('GV', 0, 27)] + []
  r017 - [('GV', 0, 22)] + []
  r043 - [('GV', 0, 13)] + []
  r045 - [('GV', 0, 12)] + []
  r048 - [('GV', 0, 8)] + []
  r050 - [('GV', 0, 24)] + [('GV', 5, 24)]
  r053 - [('GV', 0, 11)] + []
  r056 - [('GV', 0, 12)] + [('GV', 4, 12)]
  r084 - [('GV', 0, 14)] + []
  r087 - [('GV', 0, 10)] + []
  r090 - [('GV', 0,
… [950 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport json, sys\nREPO='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nsys.path.insert(0,REPO+'/tools/tests/linguistique')\nimport evaluer_gold as eg\nph={p['id']:p for p in eg.charger()}\nbase=json.load(open('m_base.json'))['phrases']; adv=json.load( … [496 caractères tronqués]`

  ```
r010 Tu viens demain ? base (1, 3, 1) adv (2, 2, 0) delta (1, -1, -1)
r030 You come tomorrow? base (1, 1, 1) adv (2, 0, 0) delta (1, -1, -1)
r190 Ils arrivent demain. base (2, 2, 0) adv (1, 3, 1) delta (-1, 1, 1)
r310 Je dois partir maintenant. base (1, 3, 2) adv (2, 2, 1) delta (1, -1, -1)
r314 Do you come tomorrow? base (0, 1, 3) adv (0, 1, 3) delta (0, 0, 0)
r320 I must leave now. base (1, 1, 2) adv (2, 0, 1) delta (1, -1, -1)
r423 Tu viens demain. base (1, 3, 3) adv (2, 2, 2) delta (1, -1, -1)
r427 You come tomorrow. base (1, 1, 3) adv (2, 0, 2) delta (1, -1, -1)
r418 Tu ne viens pas demain ? base (1, 3, 3) adv (1, 3, 3) delta (0, 0, 0)
r422 You don't come tomorrow? base (1, 1, 3) adv (1, 1, 3) delta (0, 0, 0)
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport json, sys\nREPO='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nsys.path.insert(0,REPO+'/tools/tests/linguistique')\nimport evaluer_gold as eg\nph={p['id']:p for p in eg.charger()}\nbase=json.load(open('m_base.json'))['phrases']\nfor v in ('gv_ … [911 caractères tronqués]`

  ```
=== gv_sujet changed 126 neutral 6 pos 119 neg 1
  NEG ('g013', (-1, 0, 1), 'Peux-tu venir ?')
  POS ('g004', (0, -1, 0), 'Il a couru pour attraper le bus.')
  POS ('g005', (0, -1, 0), "Elle a dit qu'elle viendrait hier.")
  POS ('g008', (0, -1, 0), 'Marie lit un livre.')
  POS ('g009', (0, -1, 0), 'Il ne dort pas.')
  POS ('g014', (1, -1, -1), "J'ai vu l'homme avec le télescope.")
=== gv_deux changed 131 neutral 6 pos 123 neg 2
  NEG ('g013', (-1, 0, 1), 'Peux-tu venir ?')
  NEG ('r190', (-1, 0, 1), 'Ils arrivent demain.')
  POS ('g004', (0, -1, 0), 'Il a couru pour attraper le bus.')
  POS ('g005', (0, -1, 0), "Elle a dit qu'elle viendrait hier.")
  POS ('g008', (0, -1, 0), 'Marie lit un livre.')
  POS ('g009', (0, -1, 0), 'Il ne dort pas.')
  POS ('g014', (1, -1, -1), "J'ai vu l'homme avec le télescope.")
=== placebo_sujet changed 186 neutral 7 pos 141 neg 38
  NEG ('g011', (-1, 2, 1), "Le livre que j'ai lu est intéressant.")
  NEG ('g013', (-1, 0, 1), 'Peux-tu venir ?')
  NEG ('r014', (-1, 2, 1), "Le livre que j'ai lu est passionnant.")
  NEG ('r015', (0, 2, 0), 'Le film dont elle parle est sorti.')
  NEG ('r054', (0, 2, 0), 'Le livre que tu lis est long.')
  NEG ('r055', (0, 2
… [894 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('build.py'); t=p.read_text()\nold='''                nom_propre = (mots[0][2][:1].isupper() and n0 not in lex.get(\"DET\", set())\n                              and n0 not in lex.get(\"PREP\", set())\n                       … [1590 caractères tronqués]`

  ```
ok
variante            F1     dev    test    tp   fp   fn       att
base            0.7549  0.7498  0.7663  1466  555  397 237/238
gv_adverbe      0.7575  0.7520  0.7696  1471  550  392 237/238
gv_sujet        0.7833  0.7813  0.7877  1478  433  385 237/238
gv_deux         0.7854  0.7826  0.7914  1480  426  383 237/238
placebo_sujet   0.7758  0.7728  0.7826  1476  466  387 237/238
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport json, sys\nREPO='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nsys.path.insert(0,REPO+'/tools/tests/linguistique')\nimport evaluer_gold as eg\nph={p['id']:p for p in eg.charger()}\nbase=json.load(open('m_base.json'))['phrases']\nfor v in ('gv_ … [838 caractères tronqués]`

  ```
=== gv_sujet changed 125 neutral 6 pos 119 neg 0
=== gv_deux changed 130 neutral 6 pos 123 neg 1
  NEG ('r190', (-1, 0, 1), 'Ils arrivent demain.')
  ```

- **bash** `{"command": "cd /tmp/gv && for v in gv_sujet gv_deux gv_adverbe; do python3 classer.py /tmp/gv/variants/$v > class_$v.json 2>/dev/null || echo FAIL $v; python3 att_detail.py /tmp/gv/variants/$v > att_$v.json 2>/dev/null || echo FAILATT $v; done\npython3 - <<'EOF'\nimport json\nfor v in ('base','gv_a … [723 caractères tronqués]`

  ```
base         FP 320 {'objet': 73, 'sujet': 144, 'adverbe': 16, 'tronque': 39, 'parasite': 16, 'deux_cotes': 27, 'gauche_autre': 5}
             FN 179 {'chev_deux': 28, 'avale_GN': 51, 'chev_droite': 75, 'chev_gauche': 6, 'tronque': 19}
gv_adverbe   FP 315 {'objet': 73, 'sujet': 145, 'adverbe': 10, 'tronque': 40, 'parasite': 16, 'deux_cotes': 25, 'gauche_autre': 6}
             FN 174 {'chev_deux': 23, 'avale_GN': 51, 'chev_droite': 72, 'chev_gauche': 9, 'tronque': 19}
gv_sujet     FP 197 {'objet': 75, 'adverbe': 16, 'tronque': 41, 'parasite': 16, 'sujet': 28, 'gauche_autre': 3, 'deux_cotes': 18}
             FN 170 {'avale_GN': 51, 'chev_droite': 80, 'chev_gauche': 3, 'chev_deux': 17, 'tronque': 19}
gv_deux      FP 190 {'objet': 75, 'adverbe': 10, 'tronque': 41, 'parasite': 16, 'sujet': 29, 'gauche_autre': 4, 'deux_cotes': 15}
             FN 168 {'avale_GN': 51, 'chev_droite': 77, 'tronque': 20, 'chev_gauche': 5, 'chev_deux': 15}
gv_adverbe att lost 0 gain 0 span_lost 0
gv_sujet att lost 0 gain 0 span_lost 0
gv_deux att lost 0 gain 0 span_lost 0
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport json\nd=json.load(open('class_gv_deux.json'))\nfor e in d['exemples'].get('sujet',[]): print(e)\nEOF\n# list all remaining sujet FPs in gv_deux\ncd /tmp/gv && python3 - <<'EOF'\nimport sys, collections, json\nREPO='/home/stephane/Data13TB/stephane … [1120 caractères tronqués]`

  ```
{'id': 'r097', 'span': 'Elle téléphone', 'sens': 'fp', 'origine': 'S', 'phrase': 'Elle téléphone à sa mère.'}
{'id': 'r142', 'span': 'Nous visitons', 'sens': 'fp', 'origine': 'S', 'phrase': 'Nous visitons un château.'}
{'id': 'r145', 'span': 'Il répare', 'sens': 'fp', 'origine': 'S', 'phrase': 'Il répare la bicyclette.'}
{'id': 'r212', 'span': 'Il faut', 'sens': 'fp', 'origine': 'S', 'phrase': 'Il faut que tu partes.'}
{'id': 'r225', 'span': 'Je crois', 'sens': 'fp', 'origine': 'S', 'phrase': "Je crois qu'il a raison."}
r097 fr Elle téléphone à sa mère. | GV 'Elle téléphone' gold 'téléphone' conf 0.55
r142 fr Nous visitons un château. | GV 'Nous visitons' gold 'visitons' conf 0.55
r145 fr Il répare la bicyclette. | GV 'Il répare' gold 'répare' conf 0.55
r212 fr Il faut que tu partes. | GV 'Il faut' gold 'faut' conf 0.55
r225 fr Je crois qu'il a raison. | GV 'Je crois' gold 'crois' conf 0.55
r229 fr Il pleure parce qu'il est triste. | GV 'Il pleure' gold 'pleure' conf 0.55
r252 fr Elle lit et il écrit. | GV 'lit et il écrit' gold 'écrit' conf 0.3
r266 fr Elle pleure parce qu'elle est seule. | GV 'Elle pleure' gold 'pleure' conf 0.55
r277 en She reads and he writes. | GV 'reads and h
… [1699 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools/structures')\nimport generateur as g\nfor t in [\"Elle téléphone à sa mère.\",\"Nous visitons un château.\",\"Il faut que tu partes.\",\"Elle lit et il écrit.\",\"Paul et Marie  … [247 caractères tronqués]`

  ```
== Elle téléphone à sa mère.
   GV 0 14 'Elle téléphone'
   GP 15 24 'à sa mère'
== Nous visitons un château.
   GV 0 13 'Nous visitons'
   GN 14 24 'un château'
== Il faut que tu partes.
   GV 0 7 'Il faut'
   SUB 8 21 'que tu partes'
== Elle lit et il écrit.
   GV 0 8 'Elle lit'
   GV 12 20 'il écrit'
== Paul et Marie lisent ; ils rient.
   GV 0 4 'Paul'
   GV 8 20 'Marie lisent'
   GV 23 32 'ils rient'
== Marie et Paul dansent ; ils s'amusent.
   GV 0 5 'Marie'
   GV 9 21 'Paul dansent'
   GV 24 37 "ils s'amusent"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique, _est_verbe\nh=Heuristique()\nfor w in ['téléphone','visitons','répare','faut','crois','pleure','repart','rient','mouille','ronfle', … [248 caractères tronqués]`

  ```
téléphone _est_verbe False _pos ('NOUN', True, 0.3)
visitons _est_verbe False _pos ('NOUN', True, 0.3)
répare _est_verbe False _pos ('NOUN', True, 0.3)
faut _est_verbe False _pos ('NOUN', True, 0.3)
crois _est_verbe False _pos ('NOUN', True, 0.3)
pleure _est_verbe False _pos ('NOUN', True, 0.3)
repart _est_verbe False _pos ('NOUN', True, 0.3)
rient _est_verbe False _pos ('NOUN', True, 0.3)
mouille _est_verbe False _pos ('NOUN', True, 0.3)
ronfle _est_verbe False _pos ('NOUN', True, 0.3)
chauffe _est_verbe False _pos ('NOUN', True, 0.3)
s'ouvre _est_verbe False _pos ('PRON', False, 0.92)
serpente _est_verbe False _pos ('NOUN', True, 0.3)
éclaire _est_verbe False _pos ('NOUN', True, 0.3)
résiste _est_verbe False _pos ('NOUN', True, 0.3)
gèle _est_verbe False _pos ('NOUN', True, 0.3)
fume _est_verbe False _pos ('NOUN', True, 0.3)
livre _est_verbe False _pos ('NOUN', True, 0.3)
réchauffe _est_verbe False _pos ('NOUN', True, 0.3)
avance _est_verbe False _pos ('NOUN', True, 0.45)
appelle _est_verbe False _pos ('NOUN', True, 0.3)
téléphone _est_verbe False _pos ('NOUN', True, 0.3)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique\nh=Heuristique()\nfor t in [\"Elle téléphone à sa mère.\",\"Elle s'ouvre.\",\"Il faut que tu partes.\",\"Paul et Marie lisent ; ils  … [335 caractères tronqués]`

  ```
== Elle téléphone à sa mère.
  POS PRON 'Elle' 0 0.92
  POS VERB 'téléphone' 5 0.85
  POS PREP 'à' 15 0.92
  POS DET 'sa' 17 0.92
  POS NOUN 'mère' 20 0.3
  POS PONCT '.' 24 0.95
  SEG [('GN', 0, 4, 'Elle'), ('GV', 0, 14, 'Elle téléphone'), ('GV', 5, 14, 'téléphone'), ('GP', 15, 24, 'à sa mère')]
== Elle s'ouvre.
  POS PRON 'Elle' 0 0.92
  POS PRON "s'" 5 0.92
  POS VERB 'ouvre' 7 0.72
  POS PONCT '.' 12 0.95
  SEG [('GN', 0, 4, 'Elle'), ('GV', 0, 12, "Elle s'ouvre"), ('GV', 5, 12, "s'ouvre")]
== Il faut que tu partes.
  POS PRON 'Il' 0 0.92
  POS VERB 'faut' 3 0.85
  POS CONJ 'que' 8 0.92
  POS PRON 'tu' 12 0.92
  POS VERB 'partes' 15 0.85
  POS PONCT '.' 21 0.95
  SEG [('GN', 0, 2, 'Il'), ('GV', 0, 7, 'Il faut'), ('GV', 3, 7, 'faut'), ('SUB', 8, 21, 'que tu partes')]
== Paul et Marie lisent ; ils rient.
  POS NOUN 'Paul' 0 0.55
  POS CONJ 'et' 5 0.92
  POS NOUN 'Marie' 8 0.55
  POS VERB 'lisent' 14 0.72
  POS PONCT ';' 21 0.95
  POS PRON 'ils' 23 0.92
  POS VERB 'rient' 27 0.85
  POS PONCT '.' 32 0.95
  SEG [('GV', 0, 4, 'Paul'), ('GN', 8, 13, 'Marie'), ('GV', 8, 20, 'Marie lisent'), ('GV', 14, 20, 'lisent'), ('GN', 23, 26, 'ils'), ('GV', 23, 32, 'ils rient'), ('GV', 27, 32, 'rie
… [5 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('build.py'); t=p.read_text()\n# --- call patch : computes pos_verbes before and passes it ---\nold_call='''CALL_OLD = \\'\\'\\'        cands = self._syntagmes_s(texte) if (langue or lg) == \"fr\" else []\n        cibles_s = … [5512 caractères tronqués]`

  ```
variante            F1     dev    test    tp   fp   fn       att
base            0.7549  0.7498  0.7663  1466  555  397 237/238
gv_adverbe      0.7575  0.7520  0.7696  1471  550  392 237/238
gv_sujet        0.7833  0.7813  0.7877  1478  433  385 237/238
gv_deux         0.7854  0.7826  0.7914  1480  426  383 237/238
placebo_sujet   0.7758  0.7728  0.7826  1476  466  387 237/238
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 34, in <module>
AssertionError
  ```

- **bash** `{"command": "cd /tmp/gv && sed -n '1,80p' build.py", "description": "Inspect build.py current state"}`

  ```
"""Construit les variantes GV depuis le bloc courant (post-r035)."""
import pathlib, shutil, sys

REPO = pathlib.Path("/home/stephane/Data13TB/stephane/GitHub/Qtrinet")
SRC = REPO / "tools/bloc_linguistique.py"
ROOT = pathlib.Path("/tmp/gv")
BASE = SRC.read_text(encoding="utf-8")

# --- règle B : l'adverbe final de phrase n'est pas dans le GV (chunker) ---
CONST_OLD = "ADVERBES_SEULS = {"
CONST_NEW = '''# adverbes de **temps** (circonstants finaux) : le gold les laisse hors du GV
# (« Tu viens | demain », r010, r030) ; la négation (« ne dort pas ») n'en est pas un.
ADVERBES_TEMPS = {"hier", "demain", "aujourd'hui", "maintenant", "yesterday", "tomorrow",
                  "today", "now", "later", "soon", "tonight"}


ADVERBES_SEULS = {'''

GB_OLD = '''                       # un marqueur **élidé** arrête aussi le GV (« sais | qu'il vient ») :
                       # le radical « qu » + « e » = « que »
                       and (_normaliser(mots[j][2]).split("'")[0] + "e"'''
GB_NEW = '''                       # l'adverbe **final** de la phrase n'est pas dans le GV
                       # (« viens | demain »), sauf la négation (« ne dort pas »)
                       and not (_norm
… [3122 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/gv/build.py <<'PYEOF'\n\"\"\"Construit les variantes GV depuis le bloc courant (post-r035).\"\"\"\nimport pathlib, shutil\n\nREPO = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nSRC = REPO / \"tools/bloc_linguistique.py\"\nROOT = pathlib.Path(\"/tmp/gv\") … [9077 caractères tronqués]`

  ```
File "/tmp/gv/build.py", line 137
    "(self._pos(langue, mots[j][2])[0] == \\"ADV\\" or _normaliser(mots[j][2]) in ADVERBES_TEMPS) && NEG")],
                                                 ^
SyntaxError: unexpected character after line continuation character
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport pathlib, re\np=pathlib.Path('build.py'); t=p.read_text()\nstart=t.index('VARIANTS = {')\nend=t.index('def ecrire(')\nnew='''VARIANTS = {\n    \"base\": [],\n    \"gv_adverbe\": [(CONST_OLD, CONST_NEW), (GB_OLD, GB_NEW)],\n    \"gv_sujet\": [(POS_O … [1078 caractères tronqués]`

  ```
ok
écrit base
écrit gv_adverbe
écrit gv_sujet
écrit gv_deux
écrit placebo_sujet
variante            F1     dev    test    tp   fp   fn       att
base            0.7549  0.7498  0.7663  1466  555  397 237/238
gv_adverbe      0.7575  0.7520  0.7696  1471  550  392 237/238
gv_sujet        0.7881  0.7861  0.7924  1478  410  385 237/238
gv_deux         0.7902  0.7875  0.7962  1480  403  383 237/238
placebo_sujet   0.7758  0.7728  0.7826  1476  466  387 237/238
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport json, sys\nREPO='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nsys.path.insert(0,REPO+'/tools/tests/linguistique')\nimport evaluer_gold as eg\nph={p['id']:p for p in eg.charger()}\nbase=json.load(open('m_base.json'))['phrases']\nfor v in ('gv_ … [1094 caractères tronqués]`

  ```
=== gv_sujet changed 147 neutral 7 pos 140 neg 0
=== gv_deux changed 152 neutral 7 pos 144 neg 1
  NEG ('r190', (-1, 0, 1), 'Ils arrivent demain.')
FP 167 {'objet': 75, 'adverbe': 10, 'tronque': 42, 'parasite': 16, 'gauche_autre': 4, 'sujet': 5, 'deux_cotes': 15}
FN 168 {'avale_GN': 51, 'chev_droite': 77, 'tronque': 20, 'chev_gauche': 5, 'chev_deux': 15}
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport sys\nREPO='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'; VAR='/tmp/gv/variants/gv_deux'\nsys.path.insert(0,VAR+'/tools'); sys.path.insert(0,REPO+'/tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as eg\nh=bl.Heuristique … [898 caractères tronqués]`

  ```
r252 fr Elle lit et il écrit. | GV 'lit et il écrit' gold 'écrit' conf 0.3
r277 en She reads and he writes. | GV 'reads and he writes' gold 'writes' conf 0.35
r314 en Do you come tomorrow? | GV 'Do you come' gold 'come' conf 0.35
r354 fr Marie et Paul dansent ; ils s'amusent. | GV "ils s'amusent" gold "s'amusent" conf 0.55
r389 fr Le bateau tangue ; il avance. | GV 'il avance' gold 'avance' conf 0.55
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && diff -u tools/bloc_linguistique.py /tmp/gv/variants/gv_deux/tools/bloc_linguistique.py | head -220", "description": "Diff final variant against source"}`

  ```
--- tools/bloc_linguistique.py	2026-11-07 12:35:27.694589431 -0500
+++ /tmp/gv/variants/gv_deux/tools/bloc_linguistique.py	2026-11-07 12:49:46.509081637 -0500
@@ -473,6 +473,12 @@
 """.split())
 
 
+# adverbes de **temps** (circonstants finaux) : le gold les laisse hors du GV
+# (« Tu viens | demain », r010, r030) ; la négation (« ne dort pas ») n'en est pas un.
+ADVERBES_TEMPS = {"hier", "demain", "aujourd'hui", "maintenant", "yesterday", "tomorrow",
+                  "today", "now", "later", "soon", "tonight"}
+
+
 ADVERBES_SEULS = {"peut-être", "vite", "bien", "mal", "hier", "demain", "aujourd'hui", "ici",
                   "là", "souvent", "toujours", "jamais", "déjà", "encore", "enfin", "alors",
                   "puis", "donc", "aussi", "très", "trop", "plus", "moins", "maybe", "perhaps"}
@@ -899,6 +905,82 @@
         return sortie
 
     # -- syntagmes ----------------------------------------------------------
+
+    def _sujet_hors_gv(self, texte: str, langue: str, cands: list[dict] | None,
+                       pos_verbes: set[int] | None = None) -> list[dict] | None:
+        """La convention du gold : le sujet est un **GN**, pas le début du GV.
+
+        Le générat
… [6115 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "old_string": "ADVERBES_SEULS = {\"peut-être\", \"vite\", \"bien\", \"mal\", \"hier\", \"demain\", \"aujourd'hui\", \"ici\",", "new_string": "# adverbes de **temps** (circonstants finaux) : le gold les laisse … [392 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 470, "limit": 15}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 890, "limit": 20}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 1300, "limit": 20}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 1528, "limit": 22}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
470: aurais aurait aurions auriez auraient aie aies ait ayons ayez aient ayant eu
471: am is are was were be been being have has had having do does did done
472: would must can could should will shall may might ought cannot
473: """.split())
474: 
475: 
476: ADVERBES_SEULS = {"peut-être", "vite", "bien", "mal", "hier", "demain", "aujourd'hui", "ici",
477:                   "là", "souvent", "toujours", "jamais", "déjà", "encore", "enfin", "alors",
478:                   "puis", "donc", "aussi", "très", "trop", "plus", "moins", "maybe", "perhaps"}
479: 
480: 
481: def _est_adverbe_seul(g: dict) -> bool:
482:     """Un GV d'un seul token adverbe n'est pas un gouverneur (« Peut-être »)."""
483:     return (len((g.get("texte") or "").split()) == 1
484:             and _normaliser(g.get("texte") or "") in ADVERBES_SEULS)

(Showing lines 470-484 of 2785. Use offset=485 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
890:         sortie = []
891:         for suf in SUFFIXES:
892:             if len(n) > len(suf) + 2 and n.endswith(suf):
893:                 sortie.append(("suffixe", len(mot) - len(suf), len(mot), suf))
894:                 break
895:         for pre in PREFIXES:
896:             if len(n) > len(pre) + 2 and n.startswith(pre):
897:                 sortie.append(("préfixe", 0, len(pre), pre))
898:                 break
899:         return sortie
900: 
901:     # -- syntagmes ----------------------------------------------------------
902:     def _syntagmes_s(self, texte: str) -> list[dict] | None:
903:         if not self.segmenter_s:
904:             return None
905:         try:
906:             if str(RACINE / "tools/structures") not in sys.path:
907:                 sys.path.insert(0, str(RACINE / "tools/structures"))
908:             import generateur  # le générateur S, importé en lecture seule
909:             return generateur.analyser(texte)

(Showing lines 890-909 of 2785. Use offset=910 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1300:             if typ == "mot" and (n in lex.get("AUX", set()) or est_verbe(d, t)
1301:                                  or (i + 1 < len(mots) and _normaliser(mots[i + 1][2]) in lex.get("AUX", set()))):
1302:                 j = i + 1
1303:                 # le GV s'arrête à la préposition, au déterminant, au relatif : un prédicat
1304:                 # par clause (« joue | au ballon », « saw | the cat »).
1305:                 while (j < len(mots) and mots[j][3] == "mot"
1306:                        and _normaliser(mots[j][2]) not in lex.get("PREP", set())
1307:                        and _normaliser(mots[j][2]) not in lex.get("DET", set())
1308:                        and _normaliser(mots[j][2]) not in RELATIFS
1309:                        and _normaliser(mots[j][2]) not in SUBORDONNANTS
1310:                        # un marqueur **élidé** arrête aussi le GV (« sais | qu'il vient ») :
1311:                        # le radical « qu » + « e » = « que »
1312:                        and (_normaliser(mots[j][2]).split("'")[0] + "e"
1313:                             i
… [570 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1528:                                             langue=lg, script=script))
1529: 
1530:         # 5. syntagmes : le générateur S (candidats) ou un chunker simple
1531:         verbes = [(e.debut, e.fin, e.valeur) for e in etiquettes
1532:                   if e.niveau == "pos" and e.type == "VERB"]
1533:         # le générateur S est **français** : il ne segmente pas l'anglais (A14) — on ne
1534:         # l'interroge que pour le français, sinon ses segments polluent l'union.
1535:         cands = self._syntagmes_s(texte) if (langue or lg) == "fr" else []
1536:         cibles_s = self._cibles_s(texte) if cands else {}
1537:         cache_gv: dict = {}  # un GV n'est analysé qu'une fois par analyse
1538:         # **un seul chunking par analyse**, partagé par les trois chemins (S, union, chunker) :
1539:         # le O(n²) mesuré venait des re-chunkings (A6, A11) — sortie identique (T178).
1540:         pos_verbes = {e.debut for e in etiquettes if e.niveau == "pos" and e.type == "VERB"}
1541:         simples = self._syntagmes_simple(texte, lg, pos_verbes)
1542:      
… [569 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "old_string": "ADVERBES_SEULS = {\"peut-être\", \"vite\", \"bien\", \"mal\", \"hier\", \"demain\", \"aujourd'hui\", \"ici\",", "new_string": "# adverbes de **temps** (circonstants finaux) : le gold les laisse … [392 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "    # -- syntagmes ----------------------------------------------------------\n\n    def _sujet_hors_gv(self, texte: str, langue: str, cands: list[dict] | None,\n                       pos_verb … [4318 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "                       and _normaliser(mots[j][2]) not in SUBORDONNANTS\n                       # l'adverbe **final** de la phrase n'est pas dans le GV\n                       # (« viens | dema … [483 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "new_string": "        # le générateur S est **français** : il ne segmente pas l'anglais (A14) — on ne\n        # l'interroge que pour le français, sinon ses segments polluent l'union.\n        # le POS **con … [1666 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && diff -u tools/bloc_linguistique.py /tmp/gv/variants/gv_deux/tools/bloc_linguistique.py | head -40; echo \"diff_exit=$?\"; python3 -c \"import sys; sys.path.insert(0,'tools'); import bloc_linguistique; print('import ok')\"", "descript … [46 caractères tronqués]`

  ```
diff_exit=0
import ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-bloc-linguistique.sh 2>&1 | tail -30", "description": "Run bloc linguistique gate", "timeoutMs": 600000}`

  ```
"morphème",
  "mot",
  "phrase",
  "pos",
  "pragmatique",
  "syntagme"
 ],
 "niveaux_manquants": [],
 "controles": {
  "vide_refus": "vide",
  "ponctuation_refus": "vide",
  "langue_inconnue": "und",
  "indice_faux": "und",
  "rejeu_identique": true
 },
 "verdicts": {
  "langue": true,
  "script": true,
  "permute_faible": true,
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
✅ porte bloc linguistique verte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/pensee/autotest.py 2>&1 | tail -40", "description": "Run pensee autotest", "timeoutMs": 900000}`

  ```
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", line 33, in <module>
    from .coeur import Candidat, Etat
ImportError: attempted relative import with no known parent package
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"autotest\" tools/toutes-les-portes.sh tools/porte-*.sh | head -20", "description": "Find autotest invocation"}`

  ```
tools/porte-balayage.sh:11:python3 tools/index_spans.py --autotest
tools/porte-bloc-linguistique.sh:8:python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl --sortie /tmp/bloc-linguistique-porte.json || { echo "❌ autotest"; exit 1; }
tools/porte-etat.sh:19:python3 tools/verifie_etat_a_jour.py --autotest || { echo "❌ porte état ROUGE : contrôle négatif"; exit 1; }
tools/porte-lecture.sh:11:python3 tools/lecture.py --autotest
tools/porte-n3-inventaire.sh:17:# Le contrôle négatif est l'autotest de l'outil : retirer une porte, ajouter une
tools/porte-n3-inventaire.sh:22:python3 tools/n3_inventaire.py --autotest || { echo "  ❌ le vérificateur ne sait pas échouer"; exit 1; }
tools/porte-produit.sh:69:if AUTOTEST_JOBS=8 timeout 600 python3 -m tools.pensee.autotest >/tmp/porte-produit-autotest.log 2>&1; then
tools/porte-produit.sh:70:  dit ✅ "autotest parallèle : $(grep -oE '[0-9]+/[0-9]+ portes tenues' /tmp/porte-produit-autotest.log | tail -1)"
tools/porte-produit.sh:72:  dit ❌ "autotest en échec (voir /tmp/porte-produit-autotest.log)"; ko=1
tools/porte-ressources.sh:2:# porte-ressources.sh — le registre des ressources tient : autotest et cohérence.
tools/porte-res
… [569 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && AUTOTEST_JOBS=8 timeout 900 python3 -m tools.pensee.autotest 2>&1 | tail -30", "description": "Run pensee autotest as module", "timeoutMs": 900000}`

  ```
✅ T152 trois tirages     tirages : [0.9838, 0.9838, 0.9838] (écart-type 0, modèle déterministe)
  ✅ T153 attachement       attachement : top1 0.9916, exact 0.9916, couverture 0.9958
  ✅ T154 cibles            cibles : 1624/1863 segments sans cible (couverture 0.1283)
  ✅ T155 cibles 500        500 premiers : 294 GN, 206 GV
  ❌ T156 relation GN-GV    relation : 570/863 (0.6605)
  ✅ T157 rôles par position rôles : 267 sans rôle, 198 avant le GV, 64 après
  ✅ T158 passifs           passifs : 5/5 faux (le sujet est un patient)
  ✅ T159 correctif passifs par → agent, avec → moyen
  ✅ T160 passifs sans par  passif sans par (chunker) : 3/3 patient
  ✅ T161 cible proximité   proximité : top1 237/239, exact 237/239, tête 237/145
  ✅ T162 candidats verbes  candidats : top-k 236/239 (0.9874), tête 236/238
  ✅ T163 échecs attachement échecs : 1 de span, 2 de cible (33 avant les correctifs)
  ✅ T164 verbe du GV       verbe du GV : saw (attendu saw) ; exact 237/239
  ✅ T165 lexique verbal    lexique : talks True, joue True, brother False ; cible GP talks
  ✅ T166 spans perdus      spans : 0 REL, 1 SUB, 0 GP
  ✅ T167 dénominateur      dénominateur : spans 0.9958 / 0.9916 / 0.9958
  ✅ T168 classem
… [987 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && AUTOTEST_JOBS=8 timeout 900 python3 -m tools.pensee.autotest 2>&1 | grep \"❌\"", "description": "List failing autotests", "timeoutMs": 900000}`

  ```
❌ T110 segmenteur        segmenteur : S F1 0.7353 tête 0.8767 ; chunker F1 0.8169 tête 0.9077
  ❌ T111 hybride segmenteur hybride : tête F1 0.8726 (S 0,3552, chunker 0,4707)
  ❌ T112 union segmenteurs union : segments F1 0.7882 (S 0,6007)
  ❌ T113 union par défaut  union par défaut : F1 0.7882, tête 0.9025
  ❌ T114 cascade + union   cascade : F1 0.7882, tête 0.9025, 602 appels
  ❌ T115 tête cascade      tête cascade corrigée : 0.9082 (cascade 0,441 ; union 0,466)
  ❌ T156 relation GN-GV    relation : 570/863 (0.6605)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1660,1765p' tools/pensee/autotest.py && echo \"=== T156 ===\" && grep -n \"def t156\" tools/pensee/autotest.py && sed -n '2340,2360p' tools/pensee/autotest.py", "description": "Read T110-T115 and T156"}`

  ```
from ..tests.linguistique.anaphore import mesurer, mesurer_roles
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 407]
    dernier = mesurer(ps, ignorer_pp=True)
    role = mesurer_roles(ps)
    return (dernier["liens"] == 103 and dernier["justes"] == 86
            and role["justes"] == 86), (
        f"103 liens : dernier nom {dernier['justes']}/103, rôle {role['justes']}/103")


def t110_segmenteur() -> tuple[bool, str]:
    """Le segmenteur : S F1 0,5396 (français seul), chunker 0,7013 ; tête 0,6877 / 0,8035 (gelé 602)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
    ph = charger()
    h1 = bl.Heuristique(union=False)
    h2 = bl.Heuristique(union=False)
    h2.segmenter_s = False
    r1 = evaluer_bloc("h", h1, ph)
    r2 = evaluer_bloc("h", h2, ph)
    f1 = round(r1["syntagme"]["f1"], 4)
    f2 = round(r2["syntagme"]["f1"], 4)
    t1 = round(r1["syntagme"]["tete"]["f1"], 4)
    t2 = round(r2["syntagme"]["tete"]["f1"], 4)
    return (abs(f1 - 0.6007) < 0.001 and abs(f2 - 0.8152) < 0.001
            
… [4746 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"relation :\" tools/pensee/autotest.py && grep -n \"T156\\|relation GN\" tools/pensee/autotest.py", "description": "Find T156 relation test"}`

  ```
2275:    return n == 859 and avec == 566, f"relation : {avec}/{n} ({round(avec/n, 4)})"
2262:    """La relation GN → GV : 257/546 (0,4707)."""
2804:              ("T156 relation GN-GV", t156_relation),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2258,2280p' tools/pensee/autotest.py", "description": "Read T156 relation test body"}`

  ```
return gn == 294 and gv == 206, f"500 premiers : {gn} GN, {gv} GV"


def t156_relation() -> tuple[bool, str]:
    """La relation GN → GV : 257/546 (0,4707)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger
    h = bl.Heuristique()
    n = avec = 0
    for p in charger():
        a = h.analyser(p["texte"], p["langue"])
        gv = any(e.niveau == "syntagme" and e.type == "GV" for e in a.etiquettes)
        for e in a.etiquettes:
            if e.niveau == "syntagme" and e.type == "GN":
                n += 1
                if gv and (e.meta or {}).get("role") in ("agent", "patient", "destinataire"):
                    avec += 1
    return n == 859 and avec == 566, f"relation : {avec}/{n} ({round(avec/n, 4)})"


def t157_roles() -> tuple[bool, str]:
    """Les GN sans rôle : 231, dont 151 avant le GV et 46 après."""
    import tools.bloc_linguistique as bl
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2280,2330p' tools/pensee/autotest.py", "description": "Read T157 roles test"}`

  ```
import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger
    h = bl.Heuristique()
    n = avant = apres = 0
    for p in charger():
        a = h.analyser(p["texte"], p["langue"])
        gv = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GV"]
        for e in a.etiquettes:
            if (e.niveau == "syntagme" and e.type == "GN"
                    and (e.meta or {}).get("role") == "groupe nominal"):
                n += 1
                if gv:
                    if gv[0].debut > e.debut:
                        avant += 1
                    else:
                        apres += 1
    return n == 267 and avant == 198 and apres == 64, (
        f"rôles : {n} sans rôle, {avant} avant le GV, {apres} après")


def t158_passifs() -> tuple[bool, str]:
    """Les passifs : 5/5 faux par la position seule."""
    import tools.bloc_linguistique as bl
    h = bl.Heuristique()
    phrases = ["Le chat est mangé par le chien.", "La souris est chassée par le chat.",
               "Le livre est lu par Paul.", "La lettre est écrite par Marie.",
               "Le gâteau est fait par le boulanger."]
    faux = 0
    for txt in phrases:
… [1017 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1765,1810p' tools/pensee/autotest.py", "description": "Read T115 fully"}`

  ```
import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    ph = charger()
    h, n = bl.Heuristique(), bl.MockNeuronal()
    cas = bl.Cascade(h, n)
    tp = fp = fn = 0
    for phrase in ph:
        ah = h.analyser(phrase["texte"], phrase["langue"])
        ac = cas.analyser(phrase["texte"], phrase["langue"])
        gold = {(s["type"], s["debut"]) for s in phrase["segments"]}
        seg_h = [(e.type, e.debut, e.fin) for e in ah.etiquettes if e.niveau == "syntagme"]
        seg_c = [(e.type, e.debut, e.fin) for e in ac.etiquettes if e.niveau == "syntagme"]
        pred = set()
        for (t, d, f) in seg_c:
            cand = [hd for (ht, hd, hf) in seg_h if ht == t and hd <= d < hf]
            pred.add((t, cand[0] if cand else d))
        tp += len(pred & gold); fp += len(pred - gold); fn += len(gold - pred)
    p = tp / max(1, tp + fp); r = tp / max(1, tp + fn)
    f1 = round(2 * p * r / max(1e-9, p + r), 4)
    return abs(f1 - 0.8299) < 0.001, (
        f"tête cascade corrigée : {f1} (cascade 0,441 ; union 0,466)")


def t116_miroir() -> tuple[bool, str]:
    """Le miroir : surface 1,0, sortie POS 0,2276 (PONCT)."""
    
… [861 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"0\\.6007\\|0\\.8152\\|0\\.8242\\|0\\.7551\\|0\\.8661\\|0\\.8299\\|859\\|566\\|0\\.4707\\|0\\.5396\\|0\\.7013\" tools/pensee/autotest.py | head -40", "description": "Locate all values to update"}`

  ```
1685:    return (abs(f1 - 0.6007) < 0.001 and abs(f2 - 0.8152) < 0.001
1711:    return abs(f1 - 0.8242) < 0.001, (
1732:    return abs(f1 - 0.7551) < 0.001, f"union : segments F1 {f1} (S 0,6007)"
1744:    return abs(f1 - 0.7551) < 0.001 and abs(tete - 0.8661) < 0.001, (
1758:    return (abs(f1 - 0.7551) < 0.001 and abs(tete - 0.8661) < 0.001
1784:    return abs(f1 - 0.8299) < 0.001, (
2275:    return n == 859 and avec == 566, f"relation : {avec}/{n} ({round(avec/n, 4)})"
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "limit": 120, "offset": 1676}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "limit": 20, "offset": 2260}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
1676:     h1 = bl.Heuristique(union=False)
1677:     h2 = bl.Heuristique(union=False)
1678:     h2.segmenter_s = False
1679:     r1 = evaluer_bloc("h", h1, ph)
1680:     r2 = evaluer_bloc("h", h2, ph)
1681:     f1 = round(r1["syntagme"]["f1"], 4)
1682:     f2 = round(r2["syntagme"]["f1"], 4)
1683:     t1 = round(r1["syntagme"]["tete"]["f1"], 4)
1684:     t2 = round(r2["syntagme"]["tete"]["f1"], 4)
1685:     return (abs(f1 - 0.6007) < 0.001 and abs(f2 - 0.8152) < 0.001
1686:             and t1 < t2), (
1687:         f"segmenteur : S F1 {f1} tête {t1} ; chunker F1 {f2} tête {t2}")
1688: 
1689: 
1690: def t111_hybride_seg() -> tuple[bool, str]:
1691:     """L'hybride frontières/têtes : tête F1 0,7402 (S 0,3552, chunker 0,4707)."""
1692:     import tools.bloc_linguistique as bl
1693:     from ..tests.linguistique.evaluer_gold import charger_gele as charger, _tete
1694:     ph = charger()
1695:     h1 = bl.Heuristique(union=False)
1696:     h2 = bl.Heuristique(union=False)
1697:     h2.segmenter_s = False
1698:     tp = fp = fn = 0
1699:     for phrase in ph:
1700:         a
… [5184 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2260: 
2261: def t156_relation() -> tuple[bool, str]:
2262:     """La relation GN → GV : 257/546 (0,4707)."""
2263:     import tools.bloc_linguistique as bl
2264:     from ..tests.linguistique.evaluer_gold import charger
2265:     h = bl.Heuristique()
2266:     n = avec = 0
2267:     for p in charger():
2268:         a = h.analyser(p["texte"], p["langue"])
2269:         gv = any(e.niveau == "syntagme" and e.type == "GV" for e in a.etiquettes)
2270:         for e in a.etiquettes:
2271:             if e.niveau == "syntagme" and e.type == "GN":
2272:                 n += 1
2273:                 if gv and (e.meta or {}).get("role") in ("agent", "patient", "destinataire"):
2274:                     avec += 1
2275:     return n == 859 and avec == 566, f"relation : {avec}/{n} ({round(avec/n, 4)})"
2276: 
2277: 
2278: def t157_roles() -> tuple[bool, str]:
2279:     """Les GN sans rôle : 231, dont 151 avant le GV et 46 après."""

(Showing lines 2260-2279 of 2863. Use offset=2280 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "limit": 10, "offset": 1668}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
1668:         f"103 liens : dernier nom {dernier['justes']}/103, rôle {role['justes']}/103")
1669: 
1670: 
1671: def t110_segmenteur() -> tuple[bool, str]:
1672:     """Le segmenteur : S F1 0,5396 (français seul), chunker 0,7013 ; tête 0,6877 / 0,8035 (gelé 602)."""
1673:     import tools.bloc_linguistique as bl
1674:     from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
1675:     ph = charger()
1676:     h1 = bl.Heuristique(union=False)
1677:     h2 = bl.Heuristique(union=False)

(Showing lines 1668-1677 of 2863. Use offset=1678 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "def t110_segmenteur() -> tuple[bool, str]:\n    \"\"\"Le segmenteur : S F1 0,7353 (sujet hors du GV), chunker 0,8169 ; tête 0,8767 / 0,9077 (gelé 602).\"\"\"", "old_string": "def t110_segmenteur( … [136 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "    return (abs(f1 - 0.7353) < 0.001 and abs(f2 - 0.8169) < 0.001\n            and t1 < t2), (", "old_string": "    return (abs(f1 - 0.6007) < 0.001 and abs(f2 - 0.8152) < 0.001\n            and  … [13 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "def t111_hybride_seg() -> tuple[bool, str]:\n    \"\"\"L'hybride frontières/têtes : tête F1 0,8726 (S 0,3552, chunker 0,4707).\"\"\"", "old_string": "def t111_hybride_seg() -> tuple[bool, str]:\n … [89 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "    return abs(f1 - 0.8726) < 0.001, (", "old_string": "    return abs(f1 - 0.8242) < 0.001, ("}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "def t112_union() -> tuple[bool, str]:\n    \"\"\"L'union des segmenteurs : segments F1 0,7882 (S 0,6007).\"\"\"", "old_string": "def t112_union() -> tuple[bool, str]:\n    \"\"\"L'union des segme … [47 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "    return abs(f1 - 0.7882) < 0.001, f\"union : segments F1 {f1} (S 0,6007)\"", "old_string": "    return abs(f1 - 0.7551) < 0.001, f\"union : segments F1 {f1} (S 0,6007)\""}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "def t113_union_defaut() -> tuple[bool, str]:\n    \"\"\"L'union par défaut : F1 0,7882, tête 0,9025 dans l'analyseur.\"\"\"", "old_string": "def t113_union_defaut() -> tuple[bool, str]:\n    \"\" … [71 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "    return abs(f1 - 0.7882) < 0.001 and abs(tete - 0.9025) < 0.001, (\n        f\"union par défaut : F1 {f1}, tête {tete}\")", "old_string": "    return abs(f1 - 0.7551) < 0.001 and abs(tete - 0. … [73 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "def t114_cascade_union() -> tuple[bool, str]:\n    \"\"\"La cascade avec l'union : F1 0,7882, tête 0,9025, 602 appels neuronaux.\"\"\"", "old_string": "def t114_cascade_union() -> tuple[bool, str … [93 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "    return (abs(f1 - 0.7882) < 0.001 and abs(tete - 0.9025) < 0.001\n            and cascade.appels_neuronal == 602), (", "old_string": "    return (abs(f1 - 0.7551) < 0.001 and abs(tete - 0.8661 … [63 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "    return abs(f1 - 0.9082) < 0.001, (", "old_string": "    return abs(f1 - 0.8299) < 0.001, ("}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "def t156_relation() -> tuple[bool, str]:\n    \"\"\"La relation GN → GV : 570/863 (0,6605) après le sujet hors du GV.\"\"\"", "old_string": "def t156_relation() -> tuple[bool, str]:\n    \"\"\"La … [45 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "new_string": "    return n == 863 and avec == 570, f\"relation : {avec}/{n} ({round(avec/n, 4)})\"", "old_string": "    return n == 859 and avec == 566, f\"relation : {avec}/{n} ({round(avec/n, 4)})\""}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && AUTOTEST_JOBS=8 timeout 900 python3 -m tools.pensee.autotest 2>&1 | tail -15", "description": "Re-run autotest after updating values", "timeoutMs": 900000}`

  ```
✅ T167 dénominateur      dénominateur : spans 0.9958 / 0.9916 / 0.9958
  ✅ T168 classement        classement : exact 237/238 ; cibles 158 verbes, 80 noms
  ✅ T169 conventions       conventions : verbes 158/158 (1.0), noms 79/80 (0.9875)
  ✅ T170 attachement ciblé ciblé : REL « homme » homme, GP « joue » joue
  ✅ T171 lexique élargi    lexique élargi : vu True, accroché True, couru True ; exact 237/238
  ✅ T172 échecs de cible   échecs de cible : 1 hors candidats, 0 mal classés
  ✅ T173 top-k strict      top-k : 236 sous-chaîne, 236 exacts (0.9916)
  ✅ T174 convention documentée convention : ['GN', 'GP', 'GV', 'REL', 'SUB'] documentée
  ✅ T175 audit attachement audit : 14/14, écarts 0
  ✅ T176 segment précédent segment précédent : s052 ouvre, s012 écoute
  ✅ T177 candidats têtes   candidats têtes : 236/238 (0.9916)
  ✅ T178 cache chunker     cache : 1 chunking chunker, 1 défaut (1+2S avant)
  ✅ T179 multi-cibles      multi-cibles : exact 237/238, exact_any 237/238
  ✅ T180 par langue        langues : fr 150/151, en 87/87 (87/88 labels)
  183/183 portes tenues
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/toutes-les-portes.sh && echo \"=== refs ===\" && sed -n '1,120p' docs/pilotage/references-non-regression.md", "description": "Read all-gates script and tolerated reds"}`

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
… [12873 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && JOURNAUX=work/portes-j12-$(date +%m%d-%Hh%M) nohup bash tools/toutes-les-portes.sh > /tmp/gv/portes-j12.out 2>&1 &\necho \"job_pid=$!\"", "description": "Start full gate pass in background", "run_in_background": true}`

  ```
started background job bash-100
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections\nph=json.load(open('tools/tests/linguistique/gold.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']+json.load(open('tools/tests/linguistique/gold_synt … [655 caractères tronqués]`

  ```
total GV 712
('fr', 'VERB') 379
('en', 'VERB') 211
('fr', 'AUX') 50
('en', 'AUX') 47
('fr', 'ADV') 24
('en', 'ADV') 1
ADV-init: 25
  ('g009', 'ne', 'ne dort pas')
  ('r009', 'ne', 'ne comprends pas')
  ('r306', 'ne', 'ne vient pas')
  ('r370', 'still', 'still stands')
  ('s013', 'ne', 'ne compte pas')
  ('s021', 'ne', 'ne observe pas')
  ('s026', 'ne', 'ne écoute pas')
  ('s029', 'ne', 'ne commence pas')
  ('s063', 'ne', 'ne prépare pas')
  ('s066', 'ne', 'ne trouve pas')
  ('s067', 'ne', 'ne crie pas')
  ('s073', 'ne', 'ne compte pas')
  ('s080', 'ne', 'ne saute pas')
  ('s094', 'ne', 'ne prépare pas')
  ('s095', 'ne', 'ne écoute pas')
  ('s107', 'ne', 'ne commence pas')
  ('s121', 'ne', 'ne écoute pas')
  ('s126', 'ne', 'ne observe pas')
  ('s134', 'ne', 'ne saute pas')
  ('s142', 'ne', 'ne dessine pas')
  ('s143', 'ne', 'ne prépare pas')
  ('s152', 'ne', 'ne écoute pas')
  ('s155', 'ne', 'ne rêve pas')
  ('s158', 'ne', 'ne range pas')
  ('s159', 'ne', 'ne cherche pas')
  ```

### 👤 Utilisateur

background job bash-100 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && JOURNAUX=work/portes-j12-$(date +%m%d-%Hh%M) nohup bash tools/toutes-les-portes.sh > /tmp/gv/portes-j12.out 2>&1 &
echo "job_pid=$!") finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "ps aux | grep -E \"toutes-les-portes|porte-\" | grep -v grep | head -10; echo \"---out---\"; tail -5 /tmp/gv/portes-j12.out 2>/dev/null; echo \"---dirs---\"; ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head", "description": "Check detached gate … [14 caractères tronqués]`

  ```
stephane  237736  0.0  0.0   7700  2156 ?        S    12:58   0:00 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && JOURNAUX=work/portes-j12-$(date +%m%d-%Hh%M) nohup bash tools/toutes-les-portes.sh > /tmp/gv/portes-j12.out 2>&1 & echo "job_pid=$!"
stephane  237738  0.0  0.0   7832  4256 ?        S    12:58   0:00 bash tools/toutes-les-portes.sh
stephane  237749  0.0  0.0   5848  2504 ?        S    12:58   0:00 timeout 1800 bash tools/porte-adaptateur-sortie.sh
stephane  237750  0.0  0.0   7832  4220 ?        S    12:58   0:00 bash tools/porte-adaptateur-sortie.sh
stephane  237760  100  1.7 2361800 2313700 ?     R    12:58   0:12 python3 tools/exporter_gguf_dense.py --depuis-gguf models/Qwen2.5-0.5B-Q8_0.gguf --sortie /tmp/porte-adaptateur/reecrit.gguf
---out---
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
---dirs---
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat reports/pensee-r035.json", "description": "Read r035 JSON for style"}`

  ```
{
 "date": "2026-11-07",
 "ligne": "B13",
 "tache": "J1.1",
 "cas": "r035",
 "phrase": "The film she talks about is out.",
 "regle": "relative zéro à préposition orpheline : [GN antécédent] [pronom sujet] [verbe] [préposition sans complément nominal] → REL ; la cible est la tête du GN. Anglais seulement.",
 "avant": {
  "all": {
   "phrases": 612,
   "pos": 0.8625,
   "f1": 0.7533,
   "precision": 0.7239,
   "rappel": 0.7853,
   "tete": 0.864,
   "exact": 236,
   "labels": 237,
   "cibles": 239,
   "couverture": 0.9916
  },
  "dev": {
   "phrases": 422,
   "pos": 0.8618,
   "f1": 0.7476,
   "precision": 0.7223,
   "rappel": 0.7747,
   "tete": 0.8603,
   "exact": 160,
   "labels": 161,
   "cibles": 163,
   "couverture": 0.9877
  },
  "test": {
   "phrases": 190,
   "pos": 0.8642,
   "f1": 0.7663,
   "precision": 0.7274,
   "rappel": 0.8095,
   "tete": 0.8724,
   "exact": 76,
   "labels": 76,
   "cibles": 76,
   "couverture": 1.0
  }
 },
 "apres": {
  "all": {
   "phrases": 612,
   "pos": 0.8625,
   "f1": 0.7549,
   "precision": 0.7254,
   "rappel": 0.7869,
   "tete": 0.8651,
   "exact": 237,
   "labels": 238,
   "cibles": 239,
   "couverture": 0.9958
  },
  "dev": {
   "phrases": 42
… [2713 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/gv && python3 measure.py /home/stephane/Data13TB/stephane/GitHub/Qtrinet > m_integrated.json 2>e_integrated.txt || { echo FAIL; head e_integrated.txt; }\npython3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/gv/m_integrated.json'))['mesures']\nfor k in ('all','dev','test','gele … [436 caractères tronqués]`

  ```
all 0.7902 0.786 0.7944 1480 403 383 tete 0.9029 att 237 238 couv 0.9958 POS 0.8625
dev 0.7875 0.7887 0.7863 1019 273 277 tete 0.9019 att 161 162 couv 0.9939 POS 0.8618
test 0.7962 0.78 0.8131 461 130 106 tete 0.9052 att 76 76 couv 1.0 POS 0.8642
gele 0.7882 0.7818 0.7946 1455 406 376 tete 0.9025 att 233 234 couv 0.9791 POS 0.8625
integrated alternative {"all": {"f1": 0.7902, "p": 0.786, "r": 0.7944, "tp": 1480, "fp": 403, "fn": 383, "att": "237/238", "couv": 0.9958}, "dev": {"f1": 0.7875, "p": 0.7887, "r": 0.7863, "tp": 1019, "fp": 273, "fn": 277, "att": "161/162", "couv": 0.9939}, "test": {"f1": 0.7962, "p": 0.78, "r": 0.8131, "tp": 461, "fp": 130, "fn": 106, "att": "76/76", "couv": 1.0}}
integrated filtrer_union {"all": {"f1": 0.8105, "p": 0.8325, "r": 0.7896, "tp": 1471, "fp": 296, "fn": 392, "att": "231/232", "couv": 0.9707}, "dev": {"f1": 0.8057, "p": 0.8322, "r": 0.7809, "tp": 1012, "fp": 204, "fn": 284, "att": "156/157", "couv": 0.9632}, "test": {"f1": 0.8211, "p": 0.833, "r": 0.8095, "tp": 459, "fp": 92, "fn": 108, "att": "75/75", "couv": 0.9868}}
integrated filtrer {"all": {"f1": 0.8144, "p": 0.8539, "r": 0.7783, "tp": 1450, "fp": 248, "fn": 413, "att": "223/224", "couv":
… [237 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/gv && python3 classer.py /home/stephane/Data13TB/stephane/GitHub/Qtrinet > class_integrated.json 2>eci.txt || { echo FAIL; head eci.txt; }\npython3 -c \"\nimport json\nd=json.load(open('/tmp/gv/class_integrated.json'))\nprint('FP',d['fp_total'],d['fp']); print('FN',d['fn_total'] … [516 caractères tronqués]`

  ```
FP 167 {'objet': 75, 'adverbe': 10, 'tronque': 42, 'parasite': 16, 'gauche_autre': 4, 'sujet': 5, 'deux_cotes': 15}
FN 168 {'avale_GN': 51, 'chev_droite': 77, 'tronque': 20, 'chev_gauche': 5, 'chev_deux': 15}
double 27 {'objet': 7, 'adverbe': 1, 'tronque': 15, 'gauche_autre': 1, 'sujet': 3}
origine {'chunker': 82, 'S': 85}
gv_adverbe FP 315 {'objet': 73, 'sujet': 145, 'adverbe': 10, 'tronque': 40, 'parasite': 16, 'deux_cotes': 25, 'gauche_autre': 6}
  FN 174 {'chev_deux': 23, 'avale_GN': 51, 'chev_droite': 72, 'chev_gauche': 9, 'tronque': 19}
gv_sujet FP 174 {'objet': 75, 'adverbe': 16, 'tronque': 42, 'parasite': 16, 'gauche_autre': 3, 'sujet': 4, 'deux_cotes': 18}
  FN 170 {'avale_GN': 51, 'chev_droite': 80, 'chev_gauche': 3, 'chev_deux': 17, 'tronque': 19}
gv_deux FP 167 {'objet': 75, 'adverbe': 10, 'tronque': 42, 'parasite': 16, 'gauche_autre': 4, 'sujet': 5, 'deux_cotes': 15}
  FN 168 {'avale_GN': 51, 'chev_droite': 77, 'tronque': 20, 'chev_gauche': 5, 'chev_deux': 15}
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport json\nfor v in ('base','gv_adverbe','gv_sujet','gv_deux'):\n    d=json.load(open(f'm_{v}.json'))['mesures']\n    print('===',v)\n    for k in ('all','dev','test'):\n        a=d[k]\n        print(f\"  {k:4} F1 {a['f1']:.4f} P {a['precision']:.4f} R … [396 caractères tronqués]`

  ```
=== base
  all  F1 0.7549 P 0.7254 R 0.7869 tp 1466 fp 555 fn 397 tete 0.8651 att 237/238 couv 0.9958 POS 0.8625
  dev  F1 0.7498 P 0.7245 R 0.7770 tp 1007 fp 383 fn 289 tete 0.8618 att 161/162 couv 0.9939 POS 0.8618
  test F1 0.7663 P 0.7274 R 0.8095 tp 459 fp 172 fn 108 tete 0.8724 att 76/76 couv 1.0000 POS 0.8642
  fr          F1 0.6980 tp 883 fp 486 fn 278
  en          F1 0.8612 tp 583 fp 69 fn 119
  hand        F1 0.8571 tp 54 fp 16 fn 2
  reel        F1 0.7503 tp 1091 fp 372 fn 354
  synthetique F1 0.7553 tp 321 fp 167 fn 41
=== gv_adverbe
  all  F1 0.7575 P 0.7279 R 0.7896 tp 1471 fp 550 fn 392 tete 0.8651 att 237/238 couv 0.9958 POS 0.8625
  dev  F1 0.7520 P 0.7266 R 0.7793 tp 1010 fp 380 fn 286 tete 0.8618 att 161/162 couv 0.9939 POS 0.8618
  test F1 0.7696 P 0.7306 R 0.8131 tp 461 fp 170 fn 106 tete 0.8724 att 76/76 couv 1.0000 POS 0.8642
  fr          F1 0.6996 tp 885 fp 484 fn 276
  en          F1 0.8656 tp 586 fp 66 fn 116
  hand        F1 0.8571 tp 54 fp 16 fn 2
  reel        F1 0.7538 tp 1096 fp 367 fn 349
  synthetique F1 0.7553 tp 321 fp 167 fn 41
=== gv_sujet
  all  F1 0.7881 P 0.7828 R 0.7933 tp 1478 fp 410 fn 385 tete 0.9029 att 237/238 couv 0.9958 POS 0.8625
 
… [964 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique\nh=Heuristique()\ncas=[\"Il a couru.\",\"Il ne dort pas.\",\"Marie lit un livre.\",\"Le garçon joue au ballon.\",\"Peux-tu venir ?\" … [411 caractères tronqués]`

  ```
Il a couru.                      [('GN', 'Il'), ('GV', 'a couru')]
Il ne dort pas.                  [('GN', 'Il'), ('GV', 'ne dort pas')]
Marie lit un livre.              [('GN', 'Marie'), ('GV', 'lit'), ('GN', 'un livre')]
Le garçon joue au ballon.        [('GN', 'Le garçon'), ('GV', 'joue'), ('GP', 'au ballon'), ('GV', 'au ballon')]
Peux-tu venir ?                  [('GN', 'Peux-tu'), ('GV', 'Peux-tu venir'), ('GV', 'venir')]
Viens ici !                      [('GV', 'Viens'), ('GV', 'Viens ici'), ('GP', 'ici')]
Il l'aime.                       [('GN', 'Il'), ('GN', "Il l'aime"), ('GN', "l'aime")]
Elle s'ouvre.                    [('GN', 'Elle'), ('GV', "s'ouvre")]
Tu viens demain ?                [('GN', 'Tu'), ('GV', 'viens'), ('GP', 'demain')]
Tu viens demain matin.           [('GN', 'Tu'), ('GV', 'viens'), ('GV', 'viens demain matin'), ('GP', 'demain'), ('GV', 'matin')]
Le vent souffle fort.            [('GN', 'Le vent'), ('GN', 'Le vent souffle fort'), ('GV', 'souffle fort')]
Ils arrivent demain.             [('GN', 'Ils'), ('GV', 'arrivent'), ('GP', 'demain')]
Nous partons en vacances.        [('GN', 'Nous'), ('GV', 'partons'), ('GV', 'partons en vacances'), ('GP', 'en vacan
… [111 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools/structures')\nimport generateur as g\nfor t in [\"Il l'aime.\",\"Peux-tu venir ?\",\"Viens ici !\",\"Le vent souffle fort.\",\"Nous partons en vacances.\",\"J'ai vu l'homme.\"]: … [182 caractères tronqués]`

  ```
== Il l'aime.
   GN 0 9 "Il l'aime"
== Peux-tu venir ?
   GV 0 13 'Peux-tu venir'
== Viens ici !
   GV 0 5 'Viens'
   GP 6 9 'ici'
== Le vent souffle fort.
   GN 0 20 'Le vent souffle fort'
== Nous partons en vacances.
   GV 0 24 'Nous partons en vacances'
== J'ai vu l'homme.
   GV 0 7 "J'ai vu"
   GN 8 15 "l'homme"
  ```

- **bash** `{"command": "cd /tmp/gv && python3 -c \"\nimport json\nd=json.load(open('m_base_avant_r035.json'))['mesures']\nfor k in ('all','dev','test'):\n    a=d[k]; print(k,a['f1'],a['precision'],a['rappel'],a['tp'],a['fp'],a['fn'],a['tete_f1'],a['att_exact'],a['att_labels'],a['att_couverture'],a['pos'])\n\"" … [43 caractères tronqués]`

  ```
all 0.7533 0.7239 0.7853 1463 558 400 0.864 236 237 0.9916 0.8625
dev 0.7476 0.7223 0.7747 1004 386 292 0.8603 160 161 0.9877 0.8618
test 0.7663 0.7274 0.8095 459 172 108 0.8724 76 76 1.0 0.8642
  ```

- **bash** `{"command": "cat > /tmp/gv/faire_json.py <<'PYEOF'\nimport json, pathlib\n\nR = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nG = pathlib.Path(\"/tmp/gv\")\n\ndef m(v):\n    return json.loads((G / f\"m_{v}.json\").read_text())[\"mesures\"]\n\ndef c(v):\n    return json.loads((G  … [8477 caractères tronqués]`

  ```
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-convention-gv.json
{'phrases': 612, 'f1': 0.7902, 'precision': 0.786, 'rappel': 0.7944, 'tp': 1480, 'fp': 403, 'fn': 383, 'tete_f1': 0.9029, 'pos': 0.8625, 'att_exact': 237, 'att_labels': 238, 'att_cibles': 239, 'att_couverture': 0.9958}
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('faire_json.py'); t=p.read_text()\nt=t.replace('\"tp\": \"+12\", \"fp\": \"-110\", \"fn\": \"-12\"','\"tp\": \"+12\", \"fp\": \"-145\", \"fn\": \"-12\"')\nt=t.replace('\"note\": \"partition « filtrer » (un segment par group … [597 caractères tronqués]`

  ```
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-convention-gv.json
{'f1': '+0,0332', 'dev': '+0,0363', 'test': '+0,0261', 'tp': '+12', 'fp': '-145', 'fn': '-12'}
{'f1': '+0,0353', 'dev': '+0,0377', 'test': '+0,0299', 'tp': '+14', 'fp': '-152', 'fn': '-14'}
{'note': 'partition « filtrer » (un segment par groupe, la vue linéaire du plan) ; la référence du plan (0,8104) est un instantané antérieur, la base mesurée ici est 0,8120', 'reference_plan': 0.8104, 'avant': {'f1': 0.812, 'tp': 1443, 'fp': 248, 'fn': 420, 'att': '223/224'}, 'apres': {'f1': 0.8144, 'tp': 1450, 'fp': 248, 'fn': 413, 'att': '223/224'}, 'delta': '+0,0024'}
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md", "content": "# B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902\n\n> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.2 · **Date** : 2026-11-07 ·\n> **Verdict** : ✅\ … [14343 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "tail -20 /tmp/gv/portes-j12.out 2>/dev/null; echo \"---registre---\"; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"$d\"; [ -n \"$d\" ] && tail -5 \"$d/registre.txt\" 2>/dev/null; echo \"---procs---\"; ps aux | grep -E \"tout … [90 caractères tronqués]`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
---registre---
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58
porte-adaptateur-sortie 0 86
---procs---
7
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -40 && echo \"=== en-cours header ===\" && sed -n '1,100p' docs/pilotage/en-cours.md", "description": "Check status and en-cours"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/bloc_linguistique.py
 M tools/pensee/autotest.py
 m tools/structures
?? reports/pensee-convention-gv.json
?? reports/rapport-convention-gv.md
?? reports/rapport-s-paragraphes.md
=== en-cours header ===
# En ce moment

**Mis à jour : 2026-11-07, 12 h 34 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index r
… [6925 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '100,220p' docs/pilotage/en-cours.md", "description": "Read en-cours numbers and next"}`

  ```
| invariant | valeur | contrôle |
|---|---|---|
| portes | **84** (dont `porte-produit` le 06/11) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **706** / **799** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **03/11 11 h 30** (82, **80/2**, les 2 connues) ; **04/11 08 h 40 arrêtée** ; N3 **17/17** à 11 h 32 ; complète après les runs | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 fait (237/238)** | **B13 : g017, convention des GV ; T132/T133, gold 200+** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,
… [2260 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"B13\\|r035\\|convention des GV\\|J1\\.\" docs/pilotage/roadmap.md | head -20 && sed -n '30,50p' docs/pilotage/roadmap.md", "description": "Inspect roadmap B13 section"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [15885 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"INDEX.md\" tools/*.py | head -10 && ls tools | grep -i index", "description": "Find report index generator"}`

  ```
tools/index_reports.py:2:"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.
tools/index_reports.py:5:avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
tools/index_reports.py:10:    python3 tools/index_reports.py              # réécrit reports/INDEX.md
tools/index_reports.py:32:        if p.name not in ("README.md", "INDEX.md") and not p.name.startswith("historique-")
tools/index_reports.py:42:        "> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;",
tools/index_reports.py:53:    ap = argparse.ArgumentParser(description="Génère reports/INDEX.md (déterministe).")
tools/index_reports.py:61:    sortie = RACINE / "reports/INDEX.md"
tools/index_reports.py:67:    print(f"  {len(fiches())} fiches → reports/INDEX.md")
tools/surveille_sessions.py:33:            "docs/pilotage/README.md", "AGENTS.md", "reports/INDEX.md",
tools/taille_documents.py:128:        if p.name in ("README.md", "INDEX.md") or p.name.startswith("historique-"):
index_reports.py
index_spans.py
index_wiki_en.py
  ```

- **bash** `{"command": "tail -12 /tmp/gv/portes-j12.out 2>/dev/null; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"---\"; wc -l \"$d/registre.txt\" 2>/dev/null; awk '$2 != 0' \"$d/registre.txt\" 2>/dev/null | tail -10", "description": "Check gate re … [17 caractères tronqués]`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
---
1 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' tools/verifie_etat_a_jour.py", "description": "Read state hook"}`

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
… [5141 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal | tail -10 && ls journal/2026-11-07 2>/dev/null || echo \"no 2026-11-07\" && sed -n '1,80p' journal/README.md", "description": "Inspect journal structure"}`

  ```
2026-11-01
2026-11-02
2026-11-03
2026-11-04
2026-11-05
2026-11-06
2026-11-07
README.md
sessions
THEMES.md
distribue.md
docs.md
memoire.md
mesures.md
modele.md
portes.md
README.md
# Journal

Le journal consigne les **événements datés**, avec des liens vers le reste : les
**mesures** sont dans `reports/` (une fiche par expérience) et l'**état** dans
`docs/pilotage/en-cours.md` — convention : `docs/methode/organisation-du-depot.md`.
Tout horodatage est en heure locale de la machine (**HAE = EDT, UTC−4**).

**Une journée = un dossier** `journal/AAAA-MM-JJ/` : `README.md` (index), les thèmes
et les autres pièces datées. Les sessions DSH sont dans `journal/sessions/<id>/` ;
chaque rapport renvoie à son jour et à `en-cours`.

## Journées

| jour | index | thèmes |
|---|---|---|
| **2026-11-07** | [2026-11-07/README.md](2026-11-07/README.md) | [distribue](2026-11-07/distribue.md) · [docs](2026-11-07/docs.md) · [memoire](2026-11-07/memoire.md) · [mesures](2026-11-07/mesures.md) · [modele](2026-11-07/modele.md) · [portes](2026-11-07/portes.md) |
| **2026-11-06** | [2026-11-06/README.md](2026-11-06/README.md) | [distribue](2026-11-06/distribue.md) · [docs](2026-11-06/docs.md) · [memoire](2026
… [16825 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' journal/2026-11-07/README.md && echo \"=== mesures ===\" && sed -n '1,80p' journal/2026-11-07/mesures.md", "description": "Read today's journal index and measures"}`

  ```
# 2026-11-07

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-07/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**23 commits** · **5 session(s)** · **6 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 3 | [distribue.md](distribue.md) |
| docs | 10 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 4 | [mesures.md](mesures.md) |
| modele | 1 | [modele.md](modele.md) |
| portes | 4 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `77d26bc7-1657-4c96-83c9-bba7c25dd828` | Tu travailles dans /home/stephane/Data13 | 2026-11-07 00:49 | 1.4 h | [rapport](../sessions/77d26bc7-1657-4c96-83c9-bba7c25dd828/rapport.md) · [digest](../sessions/77d26bc7-1657-4c96-83c9-bba7c25dd828/digest.md) |
| `7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0` | Tu travailles dans /home/stephane/Data13 | 2026-11-07 02:09 | 0.1 h | [rapport](../sessions/7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0/rap
… [7358 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline 25a6c0ff | head -30", "description": "Inspect J1.1 commit files"}`

  ```
25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
 docs/pilotage/en-cours.md                          |  19 +-
 docs/pilotage/roadmap.md                           |   2 +-
 docs/pilotage/semaine-autonome.md                  |   6 +-
 reports/INDEX.md                                   |   3 +-
 reports/README.md                                  |   1 +
 reports/pensee-r035.json                           | 191 +++++++++++++++++++++
 reports/rapport-r035.md                            | 128 ++++++++++++++
 tools/bloc_linguistique.py                         |  50 +++++-
 tools/pensee/autotest.py                           |  44 ++---
 tools/tests/linguistique/test_bloc_linguistique.py |  27 +++
 10 files changed, 431 insertions(+), 40 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '20,32p' docs/pilotage/semaine-autonome.md && grep -n \"J1.1\\|J1.2\\|r035\" docs/pilotage/semaine-autonome.md | head", "description": "Read semaine-autonome table"}`

  ```
### 2.1 Drave — le produit (priorité)

| reste | mesure | où |
|---|---|---|
| 1 span (`g017` arbitrage d'adverbe) ; `r035` relative zéro **réglé** | attachement exact **237/238 (0,9958)** | [`rapport-r035.md`](../../reports/rapport-r035.md) |
| la convention des GV (322 FP / 180 FN) | F1 **0,7549** (linéaire 0,8104) | [`rapport-r035.md`](../../reports/rapport-r035.md) |
| `meta.alternative` hors schéma v1 | le schéma publié | [`tools/schemas/`](../../tools/schemas/) |
| la restitution (annotation → texte) | miroir **0,2276** | [`../methode/miroir.md`](../methode/miroir.md) |

### 2.2 Drave — les chantiers voisins (coordination)

| chantier | état | ce qui reste | territoire |
25:| 1 span (`g017` arbitrage d'adverbe) ; `r035` relative zéro **réglé** | attachement exact **237/238 (0,9958)** | [`rapport-r035.md`](../../reports/rapport-r035.md) |
26:| la convention des GV (322 FP / 180 FN) | F1 **0,7549** (linéaire 0,8104) | [`rapport-r035.md`](../../reports/rapport-r035.md) |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 10, "offset": 1}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 18, "offset": 55}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 14, "offset": 85}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 18, "offset": 108}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-07, 12 h 34 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).

(Showing lines 1-10 of 140. Use offset=11 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
55: - **Bloquants** : aucun ; la page **`/paragraphes`** porte l'arbre/les référents.
56: - **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).
57: 
58: ### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif ; heartbeat à rafraîchir)*
59: 
60: - **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
61: - **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
62: - **Plan** : B13, bloc linguistique.
63: - **Stratégie** : v0 mesuré.
64: - **Ambition** : un runtime cognitif tracé.
65: - **Objectif final** : un moteur de pensée v0.
66: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **contrat v1** validé ; frontières, partition, GN ; **`drave` v0**.
67: - **Ce qu'elle fait** : l'API rejoue le gold (mêmes verdicts).
68: - **Ce que font les autres** : **N2**, **S**, **hub**.
69: - **Pro
… [392 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
85: - **Bloquants** : aucun.
86: - **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).
87: 
88: ## Ce qui est en cours
89: 
90: - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
91: - **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
92: - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
93: - **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; la fusion garde l'heuristique ; **`r035` réglé** (237/238, 0,9958).
94: - **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusio
… [212 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
108: ## Les chantiers et leurs bloquants
109: 
110: **Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
111: externes** et la **prochaine action**.
112: 
113: | chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
114: |---|---|---|---|
115: | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
116: | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 fait (237/238)** | **B13 : g017, convention des GV ; T132/T133, gold 200+** ; **B10.3 bloquée** |
117: | **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre (0,29)** ; **N4** |
118: | **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **1 024 octets entraînés** ; **2 048** fini (2×10 000 pas) ; la restitution |
119: 
… [386 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 10, "offset": 124}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
124: ## Ce qui reste
125: 
126: **N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035` fait**, reste `g017` ; **S** — poursuivre la validation ; **N4** — consigne ; **B10.3** — `z` ; **B13** — 183/183 ; **R0.7** — tagger ; **D** — **restauré** : le corpus à **62 documents** (Choquette + Assurance ; DOC1/DOC2, quasi-doublons, écartés) est en place (`data/corpus_ocr_cegep` : train 4 440 987, val 12 536, test 10 524 ; 8 Ko 0, 500 o 0) ; [fiche](../../reports/rapport-ocr-cegep-64.md) ; **la passe complète est finie** (`work/portes/passe-2404-23h45` ; **79 vertes, 4 rouges** : `indice`, `melange` tolérées ; `lecteur` corrigée ; `sessions` → heartbeat de `e181ce02` à rafraîchir).
127: 
128: ## Les questions ouvertes
129: 
130: - **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
131: - **N2** : **< 2,5** ? → **oui par la fenêtre** : 2,4759 / 2,4373 au grand corpus (1 024, 30 k pas) ; la porte **propre** reste à 2,7856.
132: - **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ?
… [265 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-07, 13 h 30 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-07, 12 h 34 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors d … [818 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; la fusion garde l'heuristique ; **`r035` réglé** (237/238, 0,9958) ; **convention des GV r … [272 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 et convention des GV faits (F1 0,7902, 237/238)** | **J1.3 schéma v2, J1.4 restituti … [293 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035` et convention des GV faits**, reste `g017` (J1.3/J1.4) ; **S** — poursu … [1296 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 6, "offset": 38}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
38: **État au 07/11 12 h 34.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé ; contrat v1 publié et validé, porte produit 10 contrôles (13 tests) ; frontières de phrase, partition étiquetée, compositions sans perte, PONCT, R4, « que », `r264`, **GN du pronom sujet et du nom propre** (+10,2 pts de F1) ; les quatre états N2/S/R/A intégrés ; 84 portes, 3 rouges (`indice`, `melange`, `sessions` du hub) ; `master` = `s/v7` poussés ;
39: la **cascade vrai modèle** tient sur **180 phrases** (POS **0,9415**, syntagmes **0,6130**, tête
40: **0,7574**, acte **1,0**) mais sur le **gold réel 432** elle donne **0,9065 / 0,4598 / 0,5633 /
41: 0,9954** — **verdict `false`** ; la **fenêtre B13** est **solvable** (BFS **228** nœuds, FIFO) mais **non
42: discriminante** (oracle 228, aveugle 215, 7B 238 : tout passe) — c'est le banc qu'il faut réparer ;
43: la **politique DRVM/native** ouvre le cadenas (**3 nœuds** avec la règle, **0** sans) ; la

(Showing lines 3
… [51 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**État au 07/11 13 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) r … [1046 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "limit": 6, "offset": 24}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md</path>
<type>file</type>
<content>
24: |---|---|---|
25: | 1 span (`g017` arbitrage d'adverbe) ; `r035` relative zéro **réglé** | attachement exact **237/238 (0,9958)** | [`rapport-r035.md`](../../reports/rapport-r035.md) |
26: | la convention des GV (322 FP / 180 FN) | F1 **0,7549** (linéaire 0,8104) | [`rapport-r035.md`](../../reports/rapport-r035.md) |
27: | `meta.alternative` hors schéma v1 | le schéma publié | [`tools/schemas/`](../../tools/schemas/) |
28: | la restitution (annotation → texte) | miroir **0,2276** | [`../methode/miroir.md`](../methode/miroir.md) |
29: 

(Showing lines 24-29 of 140. Use offset=30 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "new_string": "| la convention des GV (322 FP / 180 FN) — **réglée** (sujet hors du GV + adverbe final) | F1 **0,7902** (linéaire 0,8144) ; attachement **237/238** | [`rapport-convention-gv.md`](../../ … [184 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py 2>&1 | tail -5 && git diff --stat reports/INDEX.md && head -30 reports/README.md", "description": "Regenerate reports index"}`

  ```
704 fiches → reports/INDEX.md
 reports/INDEX.md | 5 +++--
 1 file changed, 3 insertions(+), 2 deletions(-)
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
| [`rapport-r035.md`](rapport-r035.md) | **B13** — relative zéro : **236 → 237**, **0,9958** |
| [`rapport-gn-pronom-sujet.md`](rapport-gn-pronom-sujet.md) | **B13** — le pronom sujet est un GN : **F1 0
… [1198 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"rapport-r035\" reports/README.md | head", "description": "Locate r035 line in reports README"}`

  ```
18:| [`rapport-r035.md`](rapport-r035.md) | **B13** — relative zéro : **236 → 237**, **0,9958** |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 6, "offset": 16}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
16: | fichier | ce qu'il porte |
17: |---|---|
18: | [`rapport-r035.md`](rapport-r035.md) | **B13** — relative zéro : **236 → 237**, **0,9958** |
19: | [`rapport-gn-pronom-sujet.md`](rapport-gn-pronom-sujet.md) | **B13** — le pronom sujet est un GN : **F1 0,7013** |
20: | [`rapport-r264-elision.md`](rapport-r264-elision.md) | **B13** — `r264` : 236/237, couverture **0,9916** |
21: | [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir 0,2276 |

(Showing lines 16-21 of 189. Use offset=22 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-convention-gv.md`](rapport-convention-gv.md) | **B13** — convention des GV : F1 **0,7549 → 0,7902**, attachement **237/238** |\n| [`rapport-r035.md`](rapport-r035.md) | **B13** — relative zé … [146 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "tail -15 /tmp/gv/portes-j12.out 2>/dev/null; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"---registre---\"; cat \"$d/registre.txt\" 2>/dev/null | tail -15", "description": "Check gate pass progress again"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
---registre---
porte-adaptateur-sortie 0 86
  ```

- **bash** `{"command": "ps -eo pid,etimes,pcpu,pmem,args | grep -E \"porte-|toutes-les\" | grep -v grep | head -10", "description": "Inspect running gate process"}`

  ```
237736     215  0.0  0.0 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && JOURNAUX=work/portes-j12-$(date +%m%d-%Hh%M) nohup bash tools/toutes-les-portes.sh > /tmp/gv/portes-j12.out 2>&1 & echo "job_pid=$!"
 237738     215  0.0  0.0 bash tools/toutes-les-portes.sh
 251117     129  0.0  0.0 timeout 1800 bash tools/porte-audit-drapeaux.sh
 251118     129  0.0  0.0 bash tools/porte-audit-drapeaux.sh
 251260     116  0.0  0.0 timeout 1800 /home/stephane/gpu-env/bin/python -u tools/audit_drapeaux_harnais.py --pas 200 --sortie /tmp/porte-audit-drapeaux
 251262     116  4.6  0.3 /home/stephane/gpu-env/bin/python -u tools/audit_drapeaux_harnais.py --pas 200 --sortie /tmp/porte-audit-drapeaux
 252762      16  142  1.3 /home/stephane/gpu-env/bin/python -u tools/entrainer_moteur.py --famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 --lot 32 --lr 3e-4 --graine 1 --pas 200 --eval-tous 200 --sortie /tmp/porte-audit-drapeaux/croissance --masque 0.10 --croissance 0.02 --croissance-tous 50 --densite-cible 0.25
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > tools/tests/linguistique/classer_gv.py <<'PYEOF'\n\"\"\"classer_gv.py — classe les erreurs de GV (FP et FN) du bloc linguistique.\n\nLe classement porte sur les **GV seuls** : un GV prédit qui n'est pas exactement un GV du\ngol … [6794 caractères tronqués]`

  ```
FP 167 167 FN 168 168 dbl 27 27
True True
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('faire_json.py'); t=p.read_text()\nold='''    \"baseline_commit\": \"25a6c0ff\",'''\nnew='''    \"baseline_commit\": \"25a6c0ff\",\n    \"dispositif\": {\n        \"code\": \"tools/bloc_linguistique.py\",\n        \"classem … [481 caractères tronqués]`

  ```
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-convention-gv.json
{'code': 'tools/bloc_linguistique.py', 'classement': 'tools/tests/linguistique/classer_gv.py', 'mesure': 'tools/tests/linguistique/evaluer_gold.py', 'fiche': 'reports/rapport-convention-gv.md'}
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md", "new_string": "La classification ci-dessous est faite sur les **GV seuls** (320 FP, 179 FN) ; les 555 FP et\n397 FN du F1 incluent aussi les GN, GP, REL et SUB. Elle est reproductible par\n`python3 tool … [261 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md", "new_string": "- [`pensee-convention-gv.json`](pensee-convention-gv.json) — les chiffres, le classement, les\n  contrôles et les limites.\n- [`classer_gv.py`](../tools/tests/linguistique/classer_gv.py)  … [500 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md has been updated successfully.
  ```

- **bash** `{"command": "tail -20 /tmp/gv/portes-j12.out 2>/dev/null; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"---registre---\"; cat \"$d/registre.txt\" 2>/dev/null | tail -20", "description": "Check gate pass progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
---registre---
porte-adaptateur-sortie 0 86
  ```

- **bash** `{"command": "ps -eo pid,etimes,pcpu,pmem,args | grep -E \"porte-|toutes-les|audit_drapeaux|entrainer\" | grep -v grep | head -10; echo \"---log tail---\"; tail -5 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/porte-audit-drapeaux.log 2>/dev/null", "description": "Check l … [18 caractères tronqués]`

  ```
237736     242  0.0  0.0 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && JOURNAUX=work/portes-j12-$(date +%m%d-%Hh%M) nohup bash tools/toutes-les-portes.sh > /tmp/gv/portes-j12.out 2>&1 & echo "job_pid=$!"
 237738     242  0.0  0.0 bash tools/toutes-les-portes.sh
 251117     156  0.0  0.0 timeout 1800 bash tools/porte-audit-drapeaux.sh
 251118     156  0.0  0.0 bash tools/porte-audit-drapeaux.sh
 251260     143  0.0  0.0 timeout 1800 /home/stephane/gpu-env/bin/python -u tools/audit_drapeaux_harnais.py --pas 200 --sortie /tmp/porte-audit-drapeaux
 251262     143  3.8  0.4 /home/stephane/gpu-env/bin/python -u tools/audit_drapeaux_harnais.py --pas 200 --sortie /tmp/porte-audit-drapeaux
 253186      20  128  1.3 /home/stephane/gpu-env/bin/python -u tools/entrainer_moteur.py --famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 --lot 32 --lr 3e-4 --graine 1 --pas 200 --eval-tous 200 --sortie /tmp/porte-audit-drapeaux/ratio50 --ratio-signes 0.5
---log tail---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0\\.7549\\|0,7549\\|0\\.7551\\|0,7551\\|237/238\\|237 / 238\\|0\\.8661\" tools --include=\"*.py\" --include=\"*.sh\" | grep -v \"tools/pensee/autotest.py\" | head -30", "description": "Find other hard-coded values"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 707 fiche(s) · 800 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 706 fichiers, le disque en a 707
     · compteurs : en-cours.md dit 799 JSON, le disque en a 800
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"706\\|799\" docs/pilotage/en-cours.md | head", "description": "Locate counters in en-cours"}`

  ```
104:| fichiers / JSON de résultats | **706** / **799** | `reports/*.md` / `reports/*.json` |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 4, "offset": 103}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
103: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
104: | fichiers / JSON de résultats | **706** / **799** | `reports/*.md` / `reports/*.json` |
105: | documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
106: | dernière passe | **03/11 11 h 30** (82, **80/2**, les 2 connues) ; **04/11 08 h 40 arrêtée** ; N3 **17/17** à 11 h 32 ; complète après les runs | `docs/pilotage/references-non-regression.md` |

(Showing lines 103-106 of 140. Use offset=107 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **707** / **800** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **706** / **799** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -10; echo \"=== tableaux ===\"; bash tools/porte-tableaux.sh 2>&1 | tail -5", "description": "Rerun doc review and table gate", "timeoutMs": 300000}`

  ```
revue de documentation · 707 fiche(s) · 800 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== tableaux ===
  ✅ 1763 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3779 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== en-cours ===\" && python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo \"=== taille ===\" && python3 tools/taille_documents.py 2>&1 | tail -10; echo \"=== journal ===\" && python3 tools/verifie_journal.py 2>&1 | tail -1 … [160 caractères tronqués]`

  ```
=== en-cours ===
  en-cours · 1621 mots · 7 sections · 4 session(s) · 5 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
=== taille ===
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3991 mots (budget 4 000)

  avertissements :
     · 38 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · reports/README.md : 2814 mots > budget 2800 (T1)
=== journal ===
  journal · 44 jour(s) · 165 session(s) · 2339 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
=== schemas ===
  schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 6, "offset": 16}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
16: | fichier | ce qu'il porte |
17: |---|---|
18: | [`rapport-convention-gv.md`](rapport-convention-gv.md) | **B13** — convention des GV : F1 **0,7549 → 0,7902**, attachement **237/238** |
19: | [`rapport-r035.md`](rapport-r035.md) | **B13** — relative zéro : **236 → 237**, **0,9958** |
20: | [`rapport-gn-pronom-sujet.md`](rapport-gn-pronom-sujet.md) | **B13** — le pronom sujet est un GN : **F1 0,7013** |
21: | [`rapport-r264-elision.md`](rapport-r264-elision.md) | **B13** — `r264` : 236/237, couverture **0,9916** |

(Showing lines 16-21 of 190. Use offset=22 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-convention-gv.md`](rapport-convention-gv.md) | GV : F1 **0,7902** |\n| [`rapport-r035.md`](rapport-r035.md) | **B13** — relative zéro : **237/238** |\n| [`rapport-gn-pronom-sujet.md`](rappor … [438 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -12", "description": "Recheck document size budget"}`

  ```
2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3991 mots (budget 4 000)

  avertissements :
     · 38 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -5 && echo \"=== acceptation ===\" && bash tools/porte-bloc-linguistique.sh 2>&1 | tail -1", "description": "Rerun doc review and acceptance gate", "timeoutMs": 600000}`

  ```
revue de documentation · 707 fiche(s) · 800 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== acceptation ===
✅ porte bloc linguistique verte
  ```

- **bash** `{"command": "tail -30 /tmp/gv/portes-j12.out 2>/dev/null; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"---registre---\"; cat \"$d/registre.txt\" 2>/dev/null | tail -30", "description": "Check full gate pass progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         187 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
---registre---
porte-adaptateur-sortie 0 86
porte-audit-drapeaux 0 187
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 14
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/tests/linguistique/test_bloc_linguistique.py && echo \"=== tail ===\" && tail -80 tools/tests/linguistique/test_bloc_linguistique.py", "description": "Read unit test style"}`

  ```
"""Tests du bloc linguistique — contrat, substitution, parallèle, cascade, activation."""
import json
import pathlib
import stat
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl

TEXTE = "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat !"


class TestBlocLinguistique(unittest.TestCase):
    def setUp(self):
        self.h = bl.Heuristique(segmenter_s=False)
        self.n = bl.MockNeuronal()

    def test_niveaux_et_spans(self):
        a = self.h.analyser(TEXTE, "fr")
        niveaux = {e.niveau for e in a.etiquettes}
        self.assertEqual(set(bl.NIVEAUX) - niveaux, set(), f"niveaux manquants : {set(bl.NIVEAUX)-niveaux}")
        for e in a.etiquettes:
            self.assertGreaterEqual(e.debut, 0)
            self.assertLessEqual(e.fin, len(TEXTE))
            self.assertLessEqual(e.debut, e.fin)

    def test_relative_zero(self):
        """Relative zéro : [GN] [pronom sujet] [verbe] [préposition orpheline] → REL.

        La règle est **structurelle** : elle ne dépend ni du nom, ni du pronom, ni du verbe,
        ni de la prépositi
… [6546 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique\nfor seg in (False, True):\n    h=Heuristique(segmenter_s=seg)\n    print('S=',seg)\n    for t in [\"Tu viens demain ?\",\"Il ne dor … [300 caractères tronqués]`

  ```
S= False
  Tu viens demain ? [('GN', 'Tu'), ('GV', 'viens')]
  Il ne dort pas. [('GN', 'Il'), ('GV', 'ne dort pas')]
  Tu viens demain matin. [('GN', 'Tu'), ('GV', 'viens demain matin')]
  Il a couru. [('GN', 'Il'), ('GV', 'a couru')]
  Marie lit un livre. [('GN', 'Marie'), ('GV', 'lit'), ('GN', 'un livre')]
  Elle s'ouvre. [('GN', 'Elle'), ('GV', "s'ouvre")]
  Peux-tu venir ? [('GN', 'Peux-tu'), ('GV', 'venir')]
S= True
  Tu viens demain ? [('GN', 'Tu'), ('GV', 'viens'), ('GP', 'demain')]
  Il ne dort pas. [('GN', 'Il'), ('GV', 'ne dort pas')]
  Tu viens demain matin. [('GN', 'Tu'), ('GV', 'viens'), ('GV', 'viens demain matin'), ('GP', 'demain'), ('GV', 'matin')]
  Il a couru. [('GN', 'Il'), ('GV', 'a couru')]
  Marie lit un livre. [('GN', 'Marie'), ('GV', 'lit'), ('GN', 'un livre')]
  Elle s'ouvre. [('GN', 'Elle'), ('GV', "s'ouvre")]
  Peux-tu venir ? [('GN', 'Peux-tu'), ('GV', 'Peux-tu venir'), ('GV', 'venir')]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", "limit": 18, "offset": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py</path>
<type>file</type>
<content>
50:                     "The film she talks about it is out.",
51:                     "The film she talks about today is out.",
52:                     "The film talks about is out."):
53:             self.assertFalse([s for s in syntagmes(txt) if s[0] == "REL"], txt)
54:         self.assertFalse([s for s in syntagmes("Le film elle parle est sorti.", "fr")
55:                           if s[0] == "REL"])
56: 
57:     def test_langue_et_script(self):
58:         for texte, langue in (("Le chat dort dans la maison.", "fr"),
59:                               ("The cat sleeps in the house.", "en"),
60:                               ("Die Katze schläft im Haus.", "de"),
61:                               ("El gato duerme en la casa.", "es"),
62:                               ("Il gatto dorme in casa.", "it")):
63:             lg, conf, _ = bl.detecter_langue(texte)
64:             self.assertEqual(lg, langue)
65:             self.assertGreater(conf, 0)
66:         self.assertEqual(bl.detecter_script("Привет мир"), "Cyrl")
67:         self.assertEqua
… [115 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py", "new_string": "        self.assertFalse([s for s in syntagmes(\"Le film elle parle est sorti.\", \"fr\")\n                          if s[0] == \"REL\"])\n\n    def test_sujet_hors_du_g … [2222 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' -v 2>&1 | tail -20", "description": "Run bloc unit tests", "timeoutMs": 300000}`

  ```
test_niveaux_et_spans (test_bloc_linguistique.TestBlocLinguistique.test_niveaux_et_spans) ... ok
test_parallele (test_bloc_linguistique.TestBlocLinguistique.test_parallele) ... ok
test_priorite_syntagme_confiance (test_bloc_linguistique.TestBlocLinguistique.test_priorite_syntagme_confiance) ... ok
test_refus (test_bloc_linguistique.TestBlocLinguistique.test_refus) ... ok
test_rejeu (test_bloc_linguistique.TestBlocLinguistique.test_rejeu) ... ok
test_relative_zero (test_bloc_linguistique.TestBlocLinguistique.test_relative_zero)
Relative zéro : [GN] [pronom sujet] [verbe] [préposition orpheline] → REL. ... ok
test_substitution (test_bloc_linguistique.TestBlocLinguistique.test_substitution) ... ok
test_sujet_hors_du_gv (test_bloc_linguistique.TestBlocLinguistique.test_sujet_hors_du_gv)
La convention du gold : le sujet est un GN, le GV commence au prédicat. ... ok
test_tagger_neuronal_chunks_avec_faux_transport (test_bloc_linguistique.TestBlocLinguistique.test_tagger_neuronal_chunks_avec_faux_transport) ... ok
test_tagger_neuronal_chunks_refus (test_bloc_linguistique.TestBlocLinguistique.test_tagger_neuronal_chunks_refus) ... ok
test_tagger_neuronal_pos_avec_faux_transport (test_bloc_l
… [418 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"17 tests\\|tests unitaires\\|test_bloc\" reports/rapport-convention-gv.md reports/pensee-convention-gv.json", "description": "Find test count references"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('faire_json.py'); t=p.read_text()\nt=t.replace('\"tests_unitaires\": 17','\"tests_unitaires\": 19')\np.write_text(t)\nEOF\npython3 /tmp/gv/faire_json.py\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"tests … [92 caractères tronqués]`

  ```
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-convention-gv.json
695:  "tests_unitaires": 19,
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md", "new_string": "- [`autotest.py`](../tools/pensee/autotest.py) — T110–T115 et T156 recalés sur les nouvelles\n  valeurs (183/183).\n- [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_l … [227 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md has been updated successfully.
  ```

- **bash** `{"command": "tail -25 /tmp/gv/portes-j12.out 2>/dev/null; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"---\"; awk '$2 != 0' \"$d/registre.txt\" 2>/dev/null | tail -10; echo \"count:\"; wc -l \"$d/registre.txt\" 2>/dev/null", "description … [35 caractères tronqués]`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         187 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          18 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
---
count:
8 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -8 journal/2026-11-07/mesures.md", "description": "Read journal measures tail"}`

  ```
## Mesures et rapports touchés

- [reports/rapport-gn-pronom-sujet.md](../../reports/rapport-gn-pronom-sujet.md)
- [reports/rapport-inventaire-panini.md](../../reports/rapport-inventaire-panini.md)

<!-- notes -->

<!-- /notes -->
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/mesures.md", "limit": 6, "offset": 34}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/mesures.md</path>
<type>file</type>
<content>
34: 
35: <!-- notes -->
36: 
37: <!-- /notes -->

(End of file - total 37 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/mesures.md", "new_string": "<!-- notes -->\n\n**13 h 30 — la convention des GV.** Le classement des erreurs de GV (320 FP / 179 FN après\n`r035`, 322/180 avant) donnait **144 FP de sujet (45 %)** et 73 d'objet. La règl … [709 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/mesures.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py 2>&1 | tail -5 && python3 tools/revue_documentation.py 2>&1 | tail -5 && python3 tools/taille_documents.py 2>&1 | tail -4", "description": "Recheck journal, docs, size", "timeoutMs": 300000}`

  ```
journal · 44 jour(s) · 165 session(s) · 2339 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  revue de documentation · 707 fiche(s) · 800 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  avertissements :
     · 38 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"0\\.7\\|F1\\|syntagme\\|attachement\\|237\\|238\" tools/porte-produit.sh | head -30", "description": "Inspect porte-produit checks"}`

  ```
25:assert any(e['niveau'] == 'syntagme' for e in d['etiquettes'])
28:    dit ✅ "analyser $langue : JSON valide, étiquettes et syntagmes"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/hooks/ | grep -v sample && echo \"=== pre-commit ===\" && sed -n '1,160p' .git/hooks/pre-commit 2>/dev/null", "description": "Inspect pre-commit hook"}`

  ```
pre-commit
=== pre-commit ===
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
# Le journal du jour, par thème (sources : git + journal
… [264 caractères tronqués]
  ```

- **bash** `{"command": "tail -25 /tmp/gv/portes-j12.out 2>/dev/null; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"---count---\"; wc -l \"$d/registre.txt\" 2>/dev/null; echo \"---reds---\"; awk '$2 != 0' \"$d/registre.txt\" 2>/dev/null", "descriptio … [31 caractères tronqués]`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         187 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          18 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          52 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
---count---
9 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
---reds---
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport sys, json\nREPO='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nsys.path.insert(0,REPO+'/tools'); sys.path.insert(0,REPO+'/tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as eg\nph=eg.charger(); h=bl.Heuristique()\n# PO … [913 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 11, in <module>
  File "/usr/lib64/python3.13/json/__init__.py", line 181, in dump
    for chunk in iterable:
                 ^^^^^^^^
  File "/usr/lib64/python3.13/json/encoder.py", line 435, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "/usr/lib64/python3.13/json/encoder.py", line 409, in _iterencode_dict
    yield from chunks
  File "/usr/lib64/python3.13/json/encoder.py", line 378, in _iterencode_dict
    raise TypeError(f'keys must be str, int, float, bool or None, '
                    f'not {key.__class__.__name__}')
TypeError: keys must be str, int, float, bool or None, not tuple
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/usr/lib64/python3.13/json/__init__.py", line 298, in load
    return loads(fp.read(),
        cls=cls, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
  File "/usr/lib64/python3.13/json/__init__.py", line 352, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "/usr
… [434 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/gv/pos_dump.py <<'PYEOF'\nimport json, pathlib, sys\nREPO = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nVAR = pathlib.Path(sys.argv[1])\nsys.path.insert(0, str(VAR / \"tools\")); sys.path.insert(0, str(REPO / \"tools/tests/linguistique\"))\nimport bloc_ … [821 caractères tronqués]`

  ```
tokens avant 3749 apres 3749
diff symétrique 0
  ```

- **bash** `{"command": "tail -30 /tmp/gv/portes-j12.out 2>/dev/null; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"---count/reds---\"; wc -l \"$d/registre.txt\" 2>/dev/null; awk '$2 != 0' \"$d/registre.txt\" 2>/dev/null", "description": "Check pass  … [10 caractères tronqués]`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         187 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          18 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          52 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
---count/reds---
9 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
  ```

- **bash** `{"command": "ps -eo pid,etimes,pcpu,pmem,args | grep -E \"porte-\" | grep -v grep | head -8", "description": "Check running gate"}`

  ```
259510      24  0.0  0.0 timeout 1800 bash tools/porte-bus.sh
 259511      24  0.0  0.0 bash tools/porte-bus.sh
 261925       1  0.0  0.0 bash tools/porte-bus.sh
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -40", "description": "Check current git status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/pilotage/semaine-autonome.md
 M journal/2026-11-07/mesures.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
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
 M tools/pensee/autotest.py
 m tools/structures
 M tools/tests/linguistique/test_bloc_linguistique.py
?? reports/pensee-convention-gv.json
?? reports/rapport-convention-gv.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/classer_gv.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --check -- tools/bloc_linguistique.py tools/pensee/autotest.py tools/tests/linguistique/test_bloc_linguistique.py docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/semaine-autonome.md reports/rapport-conventio … [168 caractères tronqués]`

  ```
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- tools/bloc_linguistique.py tools/pensee/autotest.py tools/tests/linguistique/test_bloc_linguistique.py docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/semaine-autonome.md reports/README.md reports/ … [105 caractères tronqués]`

  ```
docs/pilotage/en-cours.md                          | 14 ++--
 docs/pilotage/roadmap.md                           |  2 +-
 docs/pilotage/semaine-autonome.md                  |  2 +-
 reports/INDEX.md                                   |  5 +-
 reports/README.md                                  |  5 +-
 tools/bloc_linguistique.py                         | 93 +++++++++++++++++++++-
 tools/pensee/autotest.py                           | 26 +++---
 tools/tests/linguistique/test_bloc_linguistique.py | 40 ++++++++++
 8 files changed, 160 insertions(+), 27 deletions(-)
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 1aea295f..3fabf083 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -473,6 +473,12 @@ would must can could should will shall may might ought cannot
 """.split())
 
 
+# adverbes de **temps** (circonstants finaux) : le gold les laisse hors du GV
+# (« Tu viens | demain », r010, r030) ; la négation (« ne dort pas ») n'en est pas un.
+ADVERBES_TEMPS = {"hier", "demain", "aujourd'hui", "maintenant", "yesterday", "tomorrow",
+                  "today", "now", "later", "soon", "tonight"}
+
+
 ADVERBES_SEULS = {"peut-être", "vite", "
… [6808 caractères tronqués]
  ```

- **bash** `{"command": "tail -30 /tmp/gv/portes-j12.out 2>/dev/null; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"---count/reds---\"; wc -l \"$d/registre.txt\" 2>/dev/null; awk '$2 != 0' \"$d/registre.txt\" 2>/dev/null", "description": "Check pass  … [10 caractères tronqués]`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         187 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          18 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          52 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
---count/reds---
9 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
  ```

- **bash** `{"command": "ps -eo pid,etimes,pcpu,pmem,args | grep -E \"porte-bus|porte-c4|toutes-les\" | grep -v grep | head -8; echo \"---log---\"; tail -5 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/porte-bus.log 2>/dev/null", "description": "Check porte-bus progress"}`

  ```
237736     404  0.0  0.0 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && JOURNAUX=work/portes-j12-$(date +%m%d-%Hh%M) nohup bash tools/toutes-les-portes.sh > /tmp/gv/portes-j12.out 2>&1 & echo "job_pid=$!"
 237738     404  0.0  0.0 bash tools/toutes-les-portes.sh
 259510      44  0.0  0.0 timeout 1800 bash tools/porte-bus.sh
 259511      44  0.0  0.0 bash tools/porte-bus.sh
---log---
  gain=1.5 : 64.1160
  ✅ PPL bus épinglée : 64.116
  ✅ la sortie change : le bus agit
  ✅ les empreintes changent aussi
=== 3. le bus sur un nœud RELAIS (région du MILIEU) ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-convention-gv.json'))\nprint('keys',list(d))\nprint('avant_plan all',d['avant_plan']['all'])\nprint('avant_courant all',d['avant_courant']['all'])\nprint('sujet all',d[ … [292 caractères tronqués]`

  ```
keys ['date', 'ligne', 'tache', 'objet', 'baseline_commit', 'dispositif', 'gold', 'convention_du_gold', 'avant_plan', 'avant_courant', 'regles', 'controles_negatifs', 'partition_lineaire', 'portes', 'limites']
avant_plan all {'phrases': 612, 'f1': 0.7533, 'precision': 0.7239, 'rappel': 0.7853, 'tp': 1463, 'fp': 558, 'fn': 400, 'tete_f1': 0.864, 'pos': 0.8625, 'att_exact': 236, 'att_labels': 237, 'att_cibles': 239, 'att_couverture': 0.9916}
avant_courant all {'phrases': 612, 'f1': 0.7549, 'precision': 0.7254, 'rappel': 0.7869, 'tp': 1466, 'fp': 555, 'fn': 397, 'tete_f1': 0.8651, 'pos': 0.8625, 'att_exact': 237, 'att_labels': 238, 'att_cibles': 239, 'att_couverture': 0.9958}
sujet all {'phrases': 612, 'f1': 0.7881, 'precision': 0.7828, 'rappel': 0.7933, 'tp': 1478, 'fp': 410, 'fn': 385, 'tete_f1': 0.9029, 'pos': 0.8625, 'att_exact': 237, 'att_labels': 238, 'att_cibles': 239, 'att_couverture': 0.9958}
adverbe all {'phrases': 612, 'f1': 0.7575, 'precision': 0.7279, 'rappel': 0.7896, 'tp': 1471, 'fp': 550, 'fn': 392, 'tete_f1': 0.8651, 'pos': 0.8625, 'att_exact': 237, 'att_labels': 238, 'att_cibles': 239, 'att_couverture': 0.9958}
comb all {'phrases': 612, 'f1': 0.7902, 'precision': 0.7
… [320 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- reports/INDEX.md | head -40", "description": "Inspect index diff"}`

  ```
diff --git a/reports/INDEX.md b/reports/INDEX.md
index a596c26d..1c02f518 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **703 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **704 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -115,6 +115,7 @@
 | [rapport-consolidation-c7.md](rapport-consolidation-c7.md) | C7 — la consolidation : le rejeu met bien l'expérience dans les poids (−16,4 % en domaine, **+1,3 % hors domaine**) |
 | [rapport-consolidation-structure-partagee.md](rapport-consolidation-structure-partagee.md) | Ce qui se consolide, c'est la STRUCTURE PARTAGÉE — même mémorisation (−22,5 %), transfert −7,4 % ou +1,2 % |
 | [rapport-contrat-s.md](rapport-contrat-s.md) | B13 — Contrat d'interface L ↔ S : les subordonnées REL/SUB |
+| [rapport-convention-gv.md](rapport-convention-gv.md) | B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902 |
 | [rapport-corpus-documents.md](rapport-corpus-documents.md) | Le corpus Doc
… [2207 caractères tronqués]
  ```

- **bash** `{"command": "tail -30 /tmp/gv/portes-j12.out 2>/dev/null; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"---count/reds---\"; wc -l \"$d/registre.txt\" 2>/dev/null; awk '$2 != 0' \"$d/registre.txt\" 2>/dev/null", "description": "Check pass  … [10 caractères tronqués]`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         187 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          18 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          52 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
---count/reds---
9 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
  ```

- **bash** `{"command": "ps -eo pid,etimes,pcpu,pmem,args | grep -E \"porte-bus|porte-c4|toutes-les\" | grep -v grep | head -6; echo \"---log tail---\"; tail -8 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/porte-bus.log 2>/dev/null", "description": "Check porte-bus detail"}`

  ```
237736     416  0.0  0.0 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && JOURNAUX=work/portes-j12-$(date +%m%d-%Hh%M) nohup bash tools/toutes-les-portes.sh > /tmp/gv/portes-j12.out 2>&1 & echo "job_pid=$!"
 237738     416  0.0  0.0 bash tools/toutes-les-portes.sh
 259510      56  0.0  0.0 timeout 1800 bash tools/porte-bus.sh
 259511      56  0.0  0.0 bash tools/porte-bus.sh
 264413       6  0.0  0.0 bash tools/porte-bus.sh
---log tail---
  sans bus : 59.0790 · bus neutre : 59.0790
  ✅ perplexité ET empreintes identiques (126 croisements, horodatage exclu)
=== 2. bus NON NEUTRE : le bus doit être BRANCHÉ ===
  gain=1.5 : 64.1160
  ✅ PPL bus épinglée : 64.116
  ✅ la sortie change : le bus agit
  ✅ les empreintes changent aussi
=== 3. le bus sur un nœud RELAIS (région du MILIEU) ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-bloc-linguistique.sh 2>&1 | tail -1", "description": "Rerun acceptance gate after test addition", "timeoutMs": 600000}`

  ```
✅ porte bloc linguistique verte
  ```

- **bash** `{"command": "tail -15 /tmp/gv/portes-j12.out 2>/dev/null; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"---\"; wc -l \"$d/registre.txt\" 2>/dev/null; awk '$2 != 0' \"$d/registre.txt\" 2>/dev/null", "description": "Check pass progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes-j12-1107-12h58
  porte-adaptateur-sortie ✅                          86 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         187 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          14 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          18 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          52 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
---
9 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
  ```

- **bash** `{"command": "ps -eo pid,etimes,pcpu,pmem,args | grep -E \"porte-bus|python|rust\" | grep -v grep | head -10; echo \"---\"; tail -15 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/porte-bus.log", "description": "Inspect porte-bus process"}`

  ```
2062  322305  0.0  0.0 /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
   2233  322303  0.1  0.0 /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
   3002  322299  0.1  0.0 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
   3291  322293  2.0  0.0 /home/stephane/.local/share/pipx/venvs/docwatch/bin/python -E /home/stephane/.local/bin/docwatch --config /home/stephane/.config/docwatch/config.toml --no-browser
 216359    2818  0.0  0.0 timeout 25200 python3 tools/chantier/superviseur.py boucle --budget 21600 --timeout 5400
 216362    2818  0.2  0.0 python3 tools/chantier/superviseur.py boucle --budget 21600 --timeout 5400
 268001       1  0.0  0.0 timeout 1800 bash tools/porte-bus-socket.sh
 268002       1  0.0  0.0 bash tools/porte-bus-socket.sh
3555395   62483  0.0  0.0 bash -c sleep 2; cd /home/stephane/Data13TB/stephane/GitHub/financemeteo && python3 src/app.py --no-browser
3555423   62481  0.0  0.0 python3 src/app.py --no-browser
---
  sans bus : 59.0790 · bus neutre : 59.0790
  ✅ perplexité ET empreintes identiques (126 croisements, horodatage exclu)
=== 2. bus NON NEUTRE : le bus doit être BRANCHÉ ===
  gain=1.5 : 64.1160
  ✅ PPL bus épinglée :
… [547 caractères tronqués]
  ```

- **bash** `{"command": "d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); echo \"$d\"; cat \"$d/registre.txt\"; echo \"---reds---\"; awk '$2 != 0' \"$d/registre.txt\"", "description": "Read registry directly"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58
porte-adaptateur-sortie 0 86
porte-audit-drapeaux 0 187
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 14
porte-bloc-linguistique 0 18
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 86
---reds---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/semaine-autonome.md | sed -n '1,160p'", "description": "Review state diffs"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index ecf1b95a..53475073 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-07, 12 h 34 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-07, 13 h 30 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -63,10 +63,10 @@
 - **Stratégie** : v0 mesuré.
 - **Ambition** : un runtime cognitif tracé.
 - **Objectif final** : un moteur de pensée v0.
-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **contrat v1** validé ; frontières, partition, GN ; **`drave` v0**.
+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV + adverbe final : 320/179 → GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **contrat v1** validé ; frontières, partition, GN ; **`drave` v0**.
 - **Ce qu'elle fait** : l'API rejou
… [9285 caractères tronqués]
  ```

- **bash** `{"command": "d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); wc -l \"$d/registre.txt\"; tail -5 \"$d/registre.txt\"; echo \"---running---\"; ps -eo pid,etimes,args | grep -E \"porte-[a-z]\" | grep -v grep | head -4", "description": "Check pass pro … [7 caractères tronqués]`

  ```
10 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
porte-bloc-linguistique 0 18
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 86
---running---
 268001      13 timeout 1800 bash tools/porte-bus-socket.sh
 268002      13 bash tools/porte-bus-socket.sh
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/sessions.py --status 2>&1 | head -30", "description": "Check session status"}`

  ```
sessions · plans de mandat
    0733c5bb-f90b-4f58 · terminé  · 3044 min · N2 (200 000 pas sur le mélange, PPL domaine/littérature/anglais/wikitext2, courbe de longueur), R1.1/R1.2 mesurés depuis N2
      → **surveiller les runs relancés à 09 h 30** — `kd2` (gpu0, chargement du corpus) et `rope2048` (gpu1, en cours) ; puis mesurer et committer ; ensuite la **porte propre (0,29)**.
    0b0a6a0d-05f5-4308 · terminé  · 8911 min · N2.h — corpus propre, porte honnête, généralité, verrou de longueur
      → close — N2.i (3,13 / 12,93 / 33,83) et Pensée v0 (6/6 portes) sont committés.
    0b69f616-5c75-4c34 · terminé  · 10985 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
  ⏰ 1e7ef596-93e6-45f1 · actif    · 3551 min · docs/pilotage/` (en-cours, roadmap, chantiers, plan-travail, références), journal/` (hors `sessions/<id>/`), reports/README.md, reports/INDEX.md, tools/sessions.py, tools/ressources.py, tools/index_reports.py, tools/surveille_sessions.py, l'index git.
      → **suivi docs** (N3 intégré, état au 04/11), puis la **passe** après les runs.
    22e518ee-81b8-4081 · terminé  · 10156 min · arch
… [2606 caractères tronqués]
  ```

- **bash** `{"command": "sleep 60; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); wc -l \"$d/registre.txt\"; tail -6 \"$d/registre.txt\"; echo \"---running---\"; ps -eo pid,etimes,args | grep -E \"porte-[a-z]\" | grep -v grep | head -3", "description": "Wait … [46 caractères tronqués]`

  ```
10 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
porte-bloc-code 0 14
porte-bloc-linguistique 0 18
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 86
---running---
 268001      82 timeout 1800 bash tools/porte-bus-socket.sh
 268002      82 bash tools/porte-bus-socket.sh
  ```

- **bash** `{"command": "sleep 90; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); wc -l \"$d/registre.txt\"; tail -8 \"$d/registre.txt\"; echo \"---running---\"; ps -eo pid,etimes,args | grep -E \"porte-[a-z]\" | grep -v grep | head -3", "description": "Wait … [47 caractères tronqués]`

  ```
13 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
porte-bloc-linguistique 0 18
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 86
porte-bus-socket 0 101
porte-c4-retard 0 34
porte-cerveau 0 10
---running---
 284926      31 timeout 1800 bash tools/porte-consolidation.sh
 284927      31 bash tools/porte-consolidation.sh
 285271      11 /home/stephane/gpu-env/bin/python tools/exporter_gguf_dense.py --hf /home/stephane/IA/cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775 --lora /tmp/porte-consolidation/nul.pt --couches-lora 2 --sortie /tmp/porte-consolidation/nul.gguf
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --check -- tools/tests/linguistique/test_bloc_linguistique.py tools/tests/linguistique/classer_gv.py; echo \"exit=$?\"; python3 -m py_compile tools/tests/linguistique/classer_gv.py tools/tests/linguistique/test_bloc_linguist … [116 caractères tronqués]`

  ```
exit=0
compile ok
  ```

- **bash** `{"command": "sleep 180; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); wc -l \"$d/registre.txt\"; tail -10 \"$d/registre.txt\"; echo \"---running---\"; ps -eo pid,etimes,args | grep -E \"porte-[a-z]\" | grep -v grep | head -3", "description": "Wa … [49 caractères tronqués]`

  ```
14 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
porte-bloc-code 0 14
porte-bloc-linguistique 0 18
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 52
porte-bus 0 86
porte-bus-socket 0 101
porte-c4-retard 0 34
porte-cerveau 0 10
porte-consolidation 0 86
---running---
 290160     133 timeout 1800 bash tools/porte-coupe.sh
 290161     133 bash tools/porte-coupe.sh
 303340       6 bash tools/porte-coupe.sh
  ```

- **bash** `{"command": "sleep 240; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); wc -l \"$d/registre.txt\"; tail -12 \"$d/registre.txt\"; echo \"---running---\"; ps -eo pid,etimes,args | grep -E \"porte-[a-z]\" | grep -v grep | head -3", "description": "Wa … [49 caractères tronqués]`

  ```
20 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
porte-budget 0 52
porte-bus 0 86
porte-bus-socket 0 101
porte-c4-retard 0 34
porte-cerveau 0 10
porte-consolidation 0 86
porte-coupe 0 152
porte-cycle-c2 0 142
porte-deepseek 0 0
porte-delais 0 24
porte-diff-couche 0 20
porte-document 0 6
---running---
 337310      33 timeout 1800 bash tools/porte-echange-experts.sh
 337311      33 bash tools/porte-echange-experts.sh
 350181       4 bash tools/porte-echange-experts.sh
  ```

- **bash** `{"command": "date '+%H:%M:%S' && d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); wc -l \"$d/registre.txt\"; ps -eo pid,etimes,args | grep -E \"porte-[a-z]\" | grep -v grep | head -2", "description": "Check time and pass progress"}`

  ```
13:16:01
20 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
 337310      41 timeout 1800 bash tools/porte-echange-experts.sh
 337311      41 bash tools/porte-echange-experts.sh
  ```

- **bash** `{"command": "sleep 300; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); date '+%H:%M:%S'; wc -l \"$d/registre.txt\"; tail -8 \"$d/registre.txt\"; echo \"---running---\"; ps -eo pid,etimes,args | grep -E \"porte-[a-z]\" | grep -v grep | head -2", " … [63 caractères tronqués]`

  ```
13:21:04
25 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
porte-delais 0 24
porte-diff-couche 0 20
porte-document 0 6
porte-echange-experts 0 58
porte-episodique 0 200
porte-etat 0 0
porte-flux 0 27
porte-fusion 0 9
---running---
 368746      51 timeout 1800 bash tools/porte-gain.sh
 368747      51 bash tools/porte-gain.sh
  ```

- **bash** `{"command": "sleep 360; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); date '+%H:%M:%S'; wc -l \"$d/registre.txt\"; tail -8 \"$d/registre.txt\"; echo \"---running---\"; ps -eo pid,etimes,args | grep -E \"porte-[a-z]\" | grep -v grep | head -2", " … [63 caractères tronqués]`

  ```
13:27:10
26 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
porte-diff-couche 0 20
porte-document 0 6
porte-echange-experts 0 58
porte-episodique 0 200
porte-etat 0 0
porte-flux 0 27
porte-fusion 0 9
porte-gain 0 240
---running---
 401868     176 timeout 1800 bash tools/porte-greffe.sh
 401869     176 bash tools/porte-greffe.sh
  ```

- **bash** `{"command": "sleep 420; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); date '+%H:%M:%S'; wc -l \"$d/registre.txt\"; tail -8 \"$d/registre.txt\"; echo \"---running---\"; ps -eo pid,etimes,args | grep -E \"porte-[a-z]\" | grep -v grep | head -2", " … [63 caractères tronqués]`

  ```
13:34:14
26 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
porte-diff-couche 0 20
porte-document 0 6
porte-echange-experts 0 58
porte-episodique 0 200
porte-etat 0 0
porte-flux 0 27
porte-fusion 0 9
porte-gain 0 240
---running---
 401868     601 timeout 1800 bash tools/porte-greffe.sh
 401869     601 bash tools/porte-greffe.sh
  ```

- **bash** `{"command": "sleep 480; d=$(ls -dt /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-* 2>/dev/null | head -1); date '+%H:%M:%S'; wc -l \"$d/registre.txt\"; tail -8 \"$d/registre.txt\"; echo \"---running---\"; ps -eo pid,etimes,args | grep -E \"porte-[a-z]\" | grep -v grep | head -2", " … [63 caractères tronqués]`

  ```
13:42:17
28 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/portes-j12-1107-12h58/registre.txt
porte-echange-experts 0 58
porte-episodique 0 200
porte-etat 0 0
porte-flux 0 27
porte-fusion 0 9
porte-gain 0 240
porte-greffe 0 727
porte-harnais-invariants 0 118
---running---
 410878     238 timeout 1800 bash tools/porte-homeostasie.sh
 410879     238 bash tools/porte-homeostasie.sh
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-*.sh | sed 's|tools/porte-||;s|\\.sh||' | sort | nl | sed -n '1,84p' | tail -40", "description": "List remaining gates"}`

  ```
45	n3-generation
    46	n3-inventaire
    47	n3-placement
    48	n3-pont
    49	n3-positions
    50	n3-profondeur
    51	n3-refus
    52	n3-reseau
    53	n3-routes
    54	n3-service
    55	n3-service-briques
    56	n3-seuil
    57	n3-sparsite
    58	n3-sparsite-compte
    59	occupation-elagage
    60	occupation-moteur
    61	ocr
    62	ocr-scans
    63	pannes
    64	peripherie
    65	poids-creux
    66	pont
    67	prechargement
    68	produit
    69	profondeur-routee
    70	push-paresseux
    71	r13-bpe
    72	recurrence
    73	reflexe
    74	registre
    75	reparti-moteur
    76	ressources
    77	sauvegarde-modele
    78	sessions
    79	speculatif
    80	tableaux
    81	tokenizer-kimi
    82	topologie
    83	trace
    84	vision
  ```

- **bash** `{"command": "cd /tmp/gv && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('faire_json.py'); t=p.read_text()\nt=t.replace('\"toutes_les_portes\": \"à compléter par la passe\"','\"toutes_les_portes\": \"en cours : 28/84 vertes à 13 h 42, 0 rouge\"')\np.write_text(t)\nEOF\npython3 /tmp/gv/faire_json … [215 caractères tronqués]`

  ```
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-convention-gv.json
{'autotest': '183/183', 'porte_bloc_linguistique': 'verte', 'tests_unitaires': 19, 'toutes_les_portes': 'en cours : 28/84 vertes à 13 h 42, 0 rouge'}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add \\\n  tools/bloc_linguistique.py \\\n  tools/pensee/autotest.py \\\n  tools/tests/linguistique/test_bloc_linguistique.py \\\n  tools/tests/linguistique/classer_gv.py \\\n  reports/rapport-convention-gv.md \\\n  reports/pensee … [275 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/pilotage/semaine-autonome.md
M  journal/2026-11-07/mesures.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
M  reports/INDEX.md
M  reports/README.md
 M reports/pensee-coherence-fiches-v7.json
A  reports/pensee-convention-gv.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
A  reports/rapport-convention-gv.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
M  tools/bloc_linguistique.py
M  tools/pensee/autotest.py
 m tools/structures
A  tools/tests/linguistique/classer_gv.py
M  tools/tests/linguistique/test_bloc_linguistique.py
?? journal/sessions/session-a25a85ea-061e-49bd-bb61-64ed4a4433d0/
?? journal/sessions/session-e1ad947b-50b1-4758-a921-5267225bf642/
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_etat_a_jour.py --index; echo \"etat_index=$?\"; AUTOTEST_JOBS=8 timeout 900 python3 -m tools.pensee.autotest 2>&1 | tail -2", "description": "Final state and autotest checks", "timeoutMs": 900000}`

  ```
✅ index : aucun fait stagé sans état
etat_index=0
  ✅ T180 par langue        langues : fr 150/151, en 87/87 (87/88 labels)
  183/183 portes tenues
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183\" 2>&1 | tail -30", "description": "Commit J1.2 result", "timeoutMs": 300000}`
