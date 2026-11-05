# Session DSH — relecture

- identifiant : `65495a29-10c0-4571-96be-e7729f1efebf`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 13:16:52
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **mesurer le coût** des règles d'attachement récentes dans `tools/bloc_linguistique.py` et proposer un correctif de cache, sans modifier le fichier.

Contexte : dans `Heuristique.analyser`, le chemin des syntagmes appelle `self._syntagmes_simple(texte, lg)` **à l'intérieur** de la boucle sur les segments (pour obtenir les GV), et `_cible_proche`/`_verbes_proches` reparcourent les GV. Sur les phrases longues, c'est O(n²).

À faire :
1. Écris un banc (heredoc, pas de fichier dans le dépôt) qui mesure le temps d'analyse de `Heuristique()` sur : les 612 phrases de `charger()`, puis sur des phrases de 20, 40, 80, 160 tokens (répétition d'une phrase simple). Mesure aussi le nombre d'appels à `_syntagmes_simple` par phrase (monkeypatch d'un compteur, sans modifier le fichier).
2. Établis la **complexité empirique** (temps vs longueur) et le surcoût par rapport à une variante « GV calculés une seule fois » que tu coderas dans le banc (copie locale de la logique, pas de patch du dépôt).
3. Estime le gain (facteur) et écris le correctif proposé en **pseudo-code précis** (fonction, ligne, variable), sans l'appliquer.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-cout-chunker.md` (fiche : titre, verdict, protocole, tableau temps/longueur, complexité, correctif proposé, contrôle négatif, limites) et `reports/pensee-cout-chunker.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : temps mesurés, complexité, gain estimé du cache.
Your parent agent id is "e181ce02-cd50-488a-a6be-e84b79d40dcc". Before you finish, send your result to that agent with send_message({ agent_id: "e181ce02-cd50-488a-a6be-e84b79d40dcc", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Exploration du dépôt et du fichier `tools/bloc_linguistique.py`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && git branch --show-current && ls", "description": "Show git status, branch, and root files"}`

  ```
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/rapport.md
MM journal/sessions/MANIFEST.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/digest.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/rapport.md
MM journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/digest.md
MM journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/rapport.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
D  journal/sessions/f5
… [1253 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/bloc_linguistique.py && ls reports | head -50", "description": "Count lines and list reports dir"}`

  ```
1881 tools/bloc_linguistique.py
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
[stderr]
ls: write error: Broken pipe
  ```

### 🤖 Assistant

⏵ Lecture ciblée de `bloc_linguistique.py` (analyser, syntagmes, cible_proche, charger)

- **grep** `{"pattern": "def (analyser|_syntagmes_simple|_cible_proche|_verbes_proches|charger)\\b|class Heuristique|_syntagmes_simple\\(|_cible_proche\\(|_verbes_proches\\(", "path": "tools/bloc_linguistique.py"}`

  ```
Found 26 matches

tools/bloc_linguistique.py
Line 133:     def analyser(self, texte: str, langue: str | None = None,
Line 472: class Heuristique:
Line 643:     def _cible_proche(texte: str, segment: dict, gvs: list[dict],
Line 670:     def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
Line 688:     def _syntagmes_simple(self, texte: str, langue: str) -> list[dict]:
Line 746:     def analyser(self, texte: str, langue: str | None = None,
Line 824:             gvs_simple = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
Line 846:                         cible = self._cible_proche(texte, s, gvs, verbes)
Line 854:                         cible = self._cible_proche(texte, s, gvs, verbes)
Line 858:                     candidats = list(noms) + self._verbes_proches(texte, s, gvs, verbes=verbes)
Line 866:             for s in self._syntagmes_simple(texte, lg):
Line 868:                 cible = self._cible_proche(texte, s, [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"], verbes)
Line 871:                 gvs_s = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
Line 874:                                             candida
… [988 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/bloc_linguistique.py", "description": "Show file header"}`

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
… [1731 caractères tronqués]
  ```

- **read** `{"file_path": "tools/bloc_linguistique.py", "offset": 472, "limit": 460}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
472: class Heuristique:
473:     """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
474: 
475:     nom = "heuristique"
476: 
477:     def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
478:                  seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
479:                  union: bool = True):
480:         self.profils = profils
481:         self.segmenter_s = segmenter_s
482:         self.seuil_ouvert = seuil_ouvert
483:         self.seuil_langue = seuil_langue
484:         self.union = union
485: 
486:     # -- langues / script ---------------------------------------------------
487:     def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
488:         langue, conf, _ = detecter_langue(texte, self.profils, indice)
489:         script = detecter_script(texte)
490:         if conf < self.seuil_langue:
491:             return "und", conf, script
492:         return langue, conf, script
493: 
494:     # -- tokens ---------------------------------------------
… [26202 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"612\\|def charger\" tools/bloc_linguistique.py | head -40", "description": "Find charger and 612 references"}`

  ```
158:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '932,1040p' tools/bloc_linguistique.py", "description": "Show rest of analyser and nearby"}`

  ```
return Annotation(texte=texte, langue=lg, script=script, etiquettes=etiquettes,
                          trace=trace, source=self.nom, unites_semantiques=unites,
                          fraction_semantique=round(fraction, 4), contexte=contexte or "",
                          cout={"octets": len(texte.encode()), "caracteres": len(texte),
                                "etiquettes": len(etiquettes), "duree_s": round(time.perf_counter() - t0, 6)})


def _fusionner(spans: Sequence[Span]) -> list[Span]:
    spans = sorted(set(spans), key=lambda s: (s.debut, s.fin))
    sortie: list[Span] = []
    for s in spans:
        if not sortie or s.debut > sortie[-1].fin:
            sortie.append(s)
        else:
            sortie[-1] = Span(sortie[-1].debut, max(sortie[-1].fin, s.fin))
    return sortie


# --------------------------------------------------------------------------- neuronal


class MockNeuronal:
    """Le neuronal **de contrat** : même sortie, source `neuronal`, déterministe, sans GPU.

    Il ne prétend pas être un modèle : il prouve que le contrat accepte une autre implémentation,
    que le parallèle fusionne et que la cascade n'appelle le neuronal que sur le résidu.
 
… [4358 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"def charger(\" --include=*.py . | head -20", "description": "Find all charger functions"}`

  ```
./tools/vision_mtmd.py:32:def charger():
./tools/essai_decharge.py:340:def charger(chemins):
./tools/speculatif.py:37:def charger(nom):
./tools/m8_plage_activations.py:38:def charger(chemin: str, appareil: str):
./tools/boucle_directe.py:68:    def charger(chemin):
./tools/comparer_noyaux.py:52:    def charger(chemin, adapt=None):
./tools/semantique/corpus.py:25:def charger(langues: list[str] | None = None, max_art: int = 30,
./tools/semantique/modele.py:64:    def charger(cls, checkpoint: str, n_langues: int, d_sem: int = 128,
./tools/semantique/corpus_jw.py:29:def charger(langues: list[str] | None = None, max_art: int | None = None,
./tools/cerveau/memoire_travail.py:22:    def charger(self, codes) -> None:
./tools/docwatch/src/docwatch/glossaire.py:68:def charger(racine: Optional[pathlib.Path] = None) -> Dict[str, dict]:
./tools/distiller_natif.py:23:def charger(txt: str) -> torch.Tensor:
./tools/generer_natif.py:20:def charger(chemin: str, device: str = "cpu"):
./tools/tests/linguistique/evaluer_gold.py:24:def charger() -> list[dict]:
./tools/tests/linguistique/qualifier_neuronal.py:40:def charger() -> list[dict]:
./tools/tests/linguistique/qualifier_syntagmes.py:38:def charger
… [350 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"612\" --include=*.py --include=*.md tools reports docs | head -20", "description": "Find 612 references"}`

  ```
tools/cerveau/tests/test_couche_distante.py:58:        self.assertEqual(bits_masque(16128), 2016)
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/utils/logging.py:51:    # https://bugs.python.org/issue19612
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/compat.py:93:        """Matching according to RFC 6125, section 6.4.3
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/compat.py:95:        http://tools.ietf.org/html/rfc6125#section-6.4.3
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/compat.py:116:        # RFC 6125, section 6.4.3, subitem 1.
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/compat.py:124:            # RFC 6125, section 6.4.3, subitem 3.
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/compat.py:142:        SSLSocket.getpeercert()) matches the *hostname*.  RFC 2818 and RFC 6125
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/idnadata.py:602:        0x1611E0001612A,
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/idnadata.py:603:        0x1612D00016130,
tools/docwatch/.venv/lib/python3.13/site-packages/pip
… [1515 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/tests/linguistique/qualifier_syntagmes.py", "description": "Inspect qualifier_syntagmes charger"}`

  ```
#!/usr/bin/env python3
"""qualifier_syntagmes.py — qualifie le tagger de syntagmes local sur le gold (180 phrases).

Le tagger est `bloc_linguistique.NeuronalLLMChunks` : un modèle GGUF servi par `llama-server`,
une étiquette **BIO par token** contrainte par grammaire GBNF, et les spans reconstruits sur
la tokenisation du bloc. On mesure quatre lectures — **heuristique**, **neuronal seul**,
**cascade à priorité heuristique** (le défaut), **cascade à priorité confiance** — et trois
contrôles négatifs (vide, BIO aléatoire, têtes au hasard).

    python3 tools/tests/linguistique/qualifier_syntagmes.py --demarrer --port 18082 --workers 1 \
        --sortie reports/pensee-gold-syntagmes.json

Le serveur est lancé sur CPU (`-ngl 0`) : les GPU de N2 restent intacts.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import pathlib
import random
import statistics
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bloc_linguistique as bl  # noqa: E402
from evaluer_gold import evaluer_blo
… [1689 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,70p' tools/tests/linguistique/evaluer_gold.py && echo ---- && sed -n '1,70p' tools/tests/linguistique/qualifier_cascade.py", "description": "Inspect evaluer_gold and qualifier_cascade chargers"}`

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
… [4126 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib, sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json','gold_gele.json']:\n    p = pathlib.Path('tools/te … [419 caractères tronqués]`

  ```
gold.json 20
gold_reel.json 432
gold_synthetique.json 160
gold_gele.json 602
charger 612 5.194444444444445
charger_gele 602 5.217607973421927
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la reports | tail -20 && ls reports/*chunk* reports/*syntagm* 2>/dev/null | head", "description": "Look for existing chunker reports"}`

  ```
-rw-r--r--. 1 stephane stephane   77854 20 oct 09:48 traduction-presse-7b.json
-rw-r--r--. 1 stephane stephane   15035 19 oct 13:26 traduction-udhr-propre-3b-fraeng.json
-rw-r--r--. 1 stephane stephane   15140 19 oct 13:26 traduction-udhr-propre-7b-fraeng.json
-rw-r--r--. 1 stephane stephane   47303 19 oct 13:14 traduction-udhr-propre-7b.json
-rw-r--r--. 1 stephane stephane    3625 26 oct 23:08 universaux-mesures.json
-rw-r--r--. 1 stephane stephane     177 22 oct 19:24 xnli-14b.json
-rw-r--r--. 1 stephane stephane     265 24 oct 14:27 xnli-14b-l18.json
-rw-r--r--. 1 stephane stephane     268 24 oct 09:54 xnli-14b-l24.json
-rw-r--r--. 1 stephane stephane     266 24 oct 13:21 xnli-14b-l30.json
-rw-r--r--. 1 stephane stephane     267 24 oct 14:03 xnli-14b-l36.json
-rw-r--r--. 1 stephane stephane     266 24 oct 08:52 xnli-1.5b.json
-rw-r--r--. 1 stephane stephane     268 24 oct 09:07 xnli-1.5b-l14.json
-rw-r--r--. 1 stephane stephane     267 24 oct 14:42 xnli-1.5b-l22.json
-rw-r--r--. 1 stephane stephane     265 24 oct 09:00 xnli-32b.json
-rw-r--r--. 1 stephane stephane     267 24 oct 09:33 xnli-32b-l32.json
-rw-r--r--. 1 stephane stephane     178 22 oct 19:16 xnli-3b.json
-rw-r--r--.
… [363 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du corpus `charger()` et du chemin S-gen pris selon les options

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib, sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg\nph = eg.charger()\nprint(len(ph), ph[0].keys())\nfor p in ph[:3]:\n    print({k:(v if  … [311 caractères tronqués]`

  ```
612 dict_keys(['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source'])
{'id': 'g001', 'langue': 'fr', 'texte': 'Le chat dort.', 'mots': [{'texte': 'Le', 'pos': 'DET', 'debut': 0, 'fin': 2}, {'texte': 'chat', 'pos': 'NOUN', 'debut': 3, 'fin': 7}, {'texte': 'dort', 'pos': 'VERB', 'debut': 8, 'fin': 12}], 'segments': [{'type': 'GN', 'texte': 'Le chat', 'role': 'agent', 'debut': 0, 'fin': 7}, {'type': 'GV', 'texte': 'dort', 'role': 'prédicat', 'debut': 8, 'fin': 12}], 'pragma': {'acte': 'assertion'}, 'source': 'hand'}
{'id': 'g002', 'langue': 'fr', 'texte': 'Le chat de la voisine dort.', 'mots': [{'texte': 'Le', 'pos': 'DET', 'debut': 0, 'fin': 2}, {'texte': 'chat', 'pos': 'NOUN', 'debut': 3, 'fin': 7}, {'texte': 'de', 'pos': 'PREP', 'debut': 8, 'fin': 10}, {'texte': 'la', 'pos': 'DET', 'debut': 11, 'fin': 13}], 'segments': [{'type': 'GN', 'texte': 'Le chat', 'role': 'agent', 'debut': 0, 'fin': 7}, {'type': 'GP', 'texte': 'de la voisine', 'role': 'possession', 'debut': 8, 'fin': 21, 'cibles': ['chat'], 'cible': 'chat'}, {'type': 'GV', 'texte': 'dort', 'role': 'prédicat', 'debut': 22, 'fin': 26}], 'pragma': {'acte': 'assertion'}, 'source': 'hand'}
{'id': 'g003', 'langue': 'fr'
… [775 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh = bl.Heuristique()\nt = \"Le chat de la voisine a vu la souris.\"\nimport json\nc = h._syntagmes_s(t)\nprint('cands:', type(c), len(c) if c e … [233 caractères tronqués]`

  ```
cands: <class 'list'> 1
{"nom": "« de la voisine » → Le chat", "lecture": "« de la voisine » se rattache à « Le chat »", "attachement": {"segment": "de la voisine", "cible": "Le chat", "genre": "GN"}, "segments": [{"debut": 0, "fin": 7, "texte": "Le chat", "type": "GN", "role": "agent", "niveau": 1, "parent": 2, "profondeur": 1}, {"debut": 8, "fin": 21, "texte": "de la voisine", "type": "GP", "role": "possession", "niveau": 1, "parent": 0, "profondeur": 2}, {"debut": 22, "fin": 26, "texte": "a vu", "type": "GV", "role": "predicat", "niveau": 0, "parent": null, "profondeur": 0}, {"debut": 27, "fin": 36, "texte": "la souris", "type": "GN", "role": "patient", "niveau": 1, "parent": 2, "profondeur": 1}]}
simple: [('GN', 'Le chat'), ('GP', 'de la voisine'), ('GP', 'a'), ('GN', 'la souris')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, time, statistics\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nph = eg.charger()\norig = bl.Heuristique._syntagmes … [667 caractères tronqués]`

  ```
segmenter_s= False total_s=0.252 appels_syntagmes_simple= 1966 moy/phase=3.21
segmenter_s= True total_s=0.403 appels_syntagmes_simple= 1224 moy/phase=2.00
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique(segmenter_s=False)\nfor t in [\"Le chat est sur le toit.\", \"Le chat a vu la souris.\", \"Le chat est dans la maison.\", \"Le … [268 caractères tronqués]`

  ```
'Le chat est sur le toit.' -> [('GN', 'Le chat'), ('GV', 'est sur le toit')] GV= 1
'Le chat a vu la souris.' -> [('GN', 'Le chat'), ('GP', 'a'), ('GN', 'la souris')] GV= 0
'Le chat est dans la maison.' -> [('GN', 'Le chat'), ('GV', 'est dans la maison')] GV= 1
'Le chat dort sur le toit.' -> [('GN', 'Le chat dort'), ('GP', 'sur le toit')] GV= 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, time\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nbase=\"Le chat est sur le toit.\"\nfor k in (1,2,4,8,16):\n    t=\" \".join([base]*k)\n    print(k, len(h._mots(t)),  … [318 caractères tronqués]`

  ```
1 7 mots
 cands: 3 segments S
 simple: 2 dont GV 1
2 14 mots
 cands: 6 segments S
 simple: 4 dont GV 2
4 28 mots
 cands: 12 segments S
 simple: 8 dont GV 4
8 56 mots
 cands: 24 segments S
 simple: 16 dont GV 8
16 112 mots
 cands: 48 segments S
 simple: 32 dont GV 16
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique(segmenter_s=False)\nbase=\"Le chat de la voisine est sur le toit.\"\nprint(len(h._mots(base)), [(s['type'],s['texte']) for s i … [425 caractères tronqués]`

  ```
10 [('GN', 'Le chat'), ('GP', 'de la voisine'), ('GV', 'est sur le toit')]
2 20 mots; S segs 8 ; simple 6 GV 2
4 40 mots; S segs 16 ; simple 12 GV 4
8 80 mots; S segs 32 ; simple 24 GV 8
16 160 mots; S segs 64 ; simple 48 GV 16
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, time, statistics\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nbase=\"Le chat de la voisine est sur le toit.\"\ndef med(f, n=7):\n    ts=[]\n    for _ in range(n):\n        t0=time.perf_co … [424 caractères tronqués]`

  ```
segmenter_s= False
  N= 20  t=0.0024s
  N= 40  t=0.0049s
  N= 80  t=0.0169s
  N=160  t=0.0588s
  N=320  t=0.2410s
segmenter_s= True
  N= 20  t=0.0019s
  N= 40  t=0.0041s
  N= 80  t=0.0174s
  N=160  t=0.0318s
  N=320  t=0.0850s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, cProfile, pstats, io\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nbase=\"Le chat de la voisine est sur le toit.\"\nt=\" \".join([base]*16)\nh=bl.Heuristique(segmenter_s=False)\nh.analyser … [230 caractères tronqués]`

  ```
492142 function calls in 1.450 seconds

   Ordered by: cumulative time
   List reduced from 89 to 18 due to restriction <18>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.010    0.010    1.450    1.450 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:746(analyser)
       97    0.124    0.001    1.124    0.012 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:688(_syntagmes_simple)
       98    0.198    0.002    0.518    0.005 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:495(_mots)
     7856    0.246    0.000    0.516    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:428(_est_verbe)
      640    0.018    0.000    0.236    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:623(_verbe_dans)
   156352    0.213    0.000    0.213    0.000 {method 'endswith' of 'str' objects}
       48    0.003    0.000    0.209    0.004 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:642(_cible_proche)
    15728    0.067    0.000    0.164    0.000 /usr/lib64/python3.13/re/__init__.py:169(fullma
… [1010 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, cProfile, pstats, io\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nbase=\"Le chat de la voisine est sur le toit.\"\nt=\" \".join([base]*16)\nh=bl.Heuristique()\nh.analyser(t)\npr=cProfile. … [213 caractères tronqués]`

  ```
243652 function calls in 0.700 seconds

   Ordered by: cumulative time
   List reduced from 134 to 14 due to restriction <14>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.011    0.011    0.700    0.700 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:746(analyser)
       81    0.008    0.000    0.483    0.006 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:642(_cible_proche)
     2320    0.045    0.000    0.482    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:623(_verbe_dans)
     8144    0.179    0.000    0.386    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:428(_est_verbe)
   110163    0.151    0.000    0.151    0.000 {method 'endswith' of 'str' objects}
    13377    0.054    0.000    0.091    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:144(_normaliser)
      144    0.020    0.000    0.041    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:573(_morphemes)
        1    0.000    0.000    0.035    0.035 /home/stephane/Data13TB/stephane/GitHub/Qtrinet
… [876 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Prototype du cache (chunker + verbes de GV) et contrôle d'égalité de sortie

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, time, statistics\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\n\nclass HCache(bl.Heuristique):\n    cache_actif =  … [1846 caractères tronqués]`

  ```
opt False egalite corpus 612 / 612
  N 20 egal etiquettes 87 87
  N 40 egal etiquettes 173 173
  N 80 egal etiquettes 345 345
  N 160 egal etiquettes 689 689
opt True egalite corpus 612 / 612
  N 20 egal etiquettes 91 91
  N 40 egal etiquettes 181 181
  N 80 egal etiquettes 361 361
  N 160 egal etiquettes 721 721
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, time, statistics\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\n\nclass HCache(bl.Heuristique):\n    variante = 'V2 … [2656 caractères tronqués]`

  ```
opt False egalite corpus 612 / 612
  N 20 egal
  N 40 egal
  N 80 egal
  N 160 egal
opt True egalite corpus 612 / 612
  N 20 egal
  N 40 egal
  N 80 egal
  N 160 egal
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '100,175p' tools/bloc_linguistique.py && grep -n \"AUXILIAIRES\\s*=\\|RELATIFS\\s*=\" tools/bloc_linguistique.py | head && sed -n '400,445p' tools/bloc_linguistique.py", "description": "Inspect Annotation and helper sets"}`

  ```
unites_semantiques: list[Span] = field(default_factory=list)
    fraction_semantique: float = 0.0
    source: str = "heuristique"
    contexte: str = ""

    def par_niveau(self) -> dict[str, list[Etiquette]]:
        sortie: dict[str, list[Etiquette]] = collections.defaultdict(list)
        for e in self.etiquettes:
            sortie[e.niveau].append(e)
        return dict(sortie)

    def couverture(self) -> dict[str, float]:
        """La confiance maximale par niveau — la couverture *déclarée*, pas une précision."""
        return {n: round(max((e.confiance for e in es), default=0.0), 4)
                for n, es in self.par_niveau().items()}

    def json(self, avec_duree: bool = False) -> dict:
        cout = dict(self.cout)
        if not avec_duree:
            cout.pop("duree_s", None)
        return {
            "texte": self.texte, "langue": self.langue, "script": self.script,
            "source": self.source, "refus": self.refus,
            "etiquettes": [e.json() for e in self.etiquettes],
            "unites_semantiques": [u.json() for u in self.unites_semantiques],
            "fraction_semantique": round(float(self.fraction_semantique), 4),
            "trace": 
… [4651 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '78,112p' tools/bloc_linguistique.py", "description": "Show Annotation dataclass fields"}`

  ```
script: str = SCRIPT_NEUTRE
    meta: dict = field(default_factory=dict)

    def json(self) -> dict:
        return {
            "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
            "debut": self.debut, "fin": self.fin, "source": self.source,
            "confiance": round(float(self.confiance), 4),
            "candidats": list(self.candidats), "langue": self.langue,
            "script": self.script, "meta": dict(self.meta),
        }


@dataclass
class Annotation:
    texte: str
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    etiquettes: list[Etiquette] = field(default_factory=list)
    refus: str = ""
    trace: list[dict] = field(default_factory=list)
    cout: dict = field(default_factory=dict)
    unites_semantiques: list[Span] = field(default_factory=list)
    fraction_semantique: float = 0.0
    source: str = "heuristique"
    contexte: str = ""

    def par_niveau(self) -> dict[str, list[Etiquette]]:
        sortie: dict[str, list[Etiquette]] = collections.defaultdict(list)
        for e in self.etiquettes:
            sortie[e.niveau].append(e)
        return dict(sortie)

    def couverture(self) -> dict[str, float]:
        """La c
… [78 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture du banc complet hors dépôt (`/tmp`) et lancement des mesures

- **bash** `{"command": "cat > /tmp/bench_cout_chunker.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"Banc de coût du chunker / des règles d'attachement — HORS DÉPÔT.\n\nMesure, sans modifier tools/bloc_linguistique.py :\n  1. le corpus de `evaluer_gold.charger()` (612 phrases) ;\n  2. des phrases de 20/40/80/160 (et … [21156 caractères tronqués]`

  ```
== Système ==
{
 "python": "3.13.16",
 "platform": "Linux-7.2.6-1-default-x86_64-with-glibc2.44",
 "cpu": "Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz",
 "cpu_count": 40,
 "commit": "e1171032906de46f1a93fee0f6275f39b5d67692",
 "branche": "s/v7",
 "fichier": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py",
 "sha256_fichier": "d9c9d5592b0ba8a942860518b67b5dce04223e47c47904fbf8e185f0511b186d",
 "sha256_banc": "236a4d797e1c1c30164ab198d97c86435fc66f7ebec6896b00e589e2d0d9013c",
 "date": "2026-11-05T13:29:56-0500"
}

== Corpus 612 phrases ==
segmenter_s=False: original=228.8 ms | V1=247.6 ms (x0.92) | V2=188.1 ms (x1.22) | OFF=251.1 ms (x0.91)
segmenter_s=True: original=436.8 ms | V1=405.9 ms (x1.08) | V2=386.6 ms (x1.13) | OFF=449.0 ms (x0.97)

== Longueurs ==
opt=False N= 20: orig=1.63 ms | V1=0.85 ms | V2=0.67 ms | OFF=1.63 ms
opt=False N= 40: orig=4.66 ms | V1=1.75 ms | V2=1.20 ms | OFF=4.79 ms
opt=False N= 80: orig=15.57 ms | V1=4.15 ms | V2=2.36 ms | OFF=15.73 ms
opt=False N=160: orig=64.18 ms | V1=15.52 ms | V2=7.40 ms | OFF=63.22 ms
opt=False N=320: orig=234.26 ms | V1=34.69 ms | V2=12.67 ms | OFF=247.21 ms
opt=True N= 20: orig=2.24 ms | V1=3.26 ms | V
… [1328 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/bench_cout_chunker.json'))\nfor opt in ('False','True'):\n    c=d['corpus']['resultats'][opt]\n    print('opt',opt)\n    print(' orig',c['original'])\n    print(' V1', {k:v for k, … [534 caractères tronqués]`

  ```
opt False
 orig {'total_s': 0.22882321913493797, 'moyenne_s': 0.0003738941489132973, 'mediane_s': 0.00034327599860262126, 'p95_s': 0.0006004360038787127, 'max_s': 0.0011744709918275476, 'etiquettes_moy': None}
 V1 {'total_s': 0.2475746006530244, 'egalite': '612/612', 'gain_vs_original': 0.9242596717570133}
 V2 {'total_s': 0.18805358817917295, 'egalite': '612/612', 'gain_vs_original': 1.2167979422807966}
 OFF {'total_s': 0.25110101044992916, 'egalite': '612/612', 'gain_vs_original': 0.9112795632519627}
 compteurs_orig {'simple_total': 1966, 'simple_moy': 3.212418300653595, 'simple_min': 1, 'simple_max': 7, 'verbe_total': 197, 'verbe_moy': 0.32189542483660133, 'segments_moy': 1.1045751633986929, 'gv_moy': 0.18627450980392157, 'tokens_moy': 6.125816993464053}
 compteurs_v2 {'simple_appels_moy': 3.212418300653595, 'simple_miss_moy': 1, 'simple_miss_max': 1, 'gv_appels_moy': 0.32189542483660133, 'gv_miss_moy': 0.13562091503267973, 'gv_miss_max': 2}
opt True
 orig {'total_s': 0.4367706402554177, 'moyenne_s': 0.0007136775167572184, 'mediane_s': 0.0006780310213798657, 'p95_s': 0.0010868890094570816, 'max_s': 0.004372628987766802, 'etiquettes_moy': None}
 V1 {'total_s': 0.4059087041532621, 
… [1158 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, time, statistics, cProfile, pstats, io\nsys.path.insert(0,'tools'); sys.path.insert(0,'/tmp')\nimport bloc_linguistique as bl\nsys.argv=['x']\nimport bench_cout_chunker as b\nbase=b.BASE\nfor opt in (Fal … [976 caractères tronqués]`

  ```
--- opt False
 N 160 orig median 0.0668 min 0.0633
   V2 median 0.0054 min 0.0052  appels_gv 640 miss 16
   simple seul median 0.0009
 N 320 orig median 0.2570 min 0.2440
   V2 median 0.0146 min 0.0123  appels_gv 2304 miss 32
   simple seul median 0.0019
 N 640 orig median 1.0001 min 0.9663
   V2 median 0.0420 min 0.0340  appels_gv 8704 miss 64
   simple seul median 0.0036
--- opt True
 N 160 orig median 0.0370 min 0.0266
   V2 median 0.0132 min 0.0129  appels_gv 2289 miss 32
   simple seul median 0.0009
 N 320 orig median 0.0955 min 0.0906
   V2 median 0.0375 min 0.0335  appels_gv 8673 miss 64
   simple seul median 0.0018
 N 640 orig median 0.3195 min 0.2824
   V2 median 0.0896 min 0.0877  appels_gv 33729 miss 128
   simple seul median 0.0033
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, cProfile, pstats, io\nsys.path.insert(0,'tools'); sys.path.insert(0,'/tmp')\nimport bloc_linguistique as bl\nimport bench_cout_chunker as b\nfor n in (320,640):\n    t=' '.join([b.BASE]*(n//10))\n    for … [390 caractères tronqués]`

  ```
=== 320 orig
         814004 function calls in 2.326 seconds

   Ordered by: internal time
   List reduced from 134 to 12 due to restriction <12>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    30624    0.668    0.000    1.439    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:428(_est_verbe)
   410851    0.559    0.000    0.559    0.000 {method 'endswith' of 'str' objects}
    49281    0.199    0.000    0.334    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:144(_normaliser)
     8736    0.167    0.000    1.807    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:623(_verbe_dans)
    49377    0.070    0.000    0.070    0.000 {method 'casefold' of 'str' objects}
    51764    0.069    0.000    0.069    0.000 {built-in method unicodedata.normalize}
    38108    0.051    0.000    0.051    0.000 {built-in method builtins.len}
      288    0.041    0.000    0.082    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:573(_morphemes)
    27450    0.040    0.000    0.040    0.000 {method 'group' of 're.Match' objects}
     8769    0.03
… [4568 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesures robustes (rounds entrelacés, temps CPU) pour stabiliser les facteurs

- **bash** `{"command": "cat > /tmp/bench_cout_robuste.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"Mesures robustes (hors dépôt) : rounds entrelacés, médiane des totaux, temps CPU + mur.\"\"\"\nfrom __future__ import annotations\nimport gc, json, math, pathlib, statistics, sys, time\nRACINE = pathlib.Path(\"/home/ … [7088 caractères tronqués]`

  ```
== corpus ==
opt=False: original=226.7ms x1.00 | V1=195.7ms x1.16 | V2=190.3ms x1.19 | OFF=228.3ms x0.99
opt=True: original=389.3ms x1.00 | V1=381.0ms x1.02 | V2=372.3ms x1.05 | OFF=394.7ms x0.99
== longueurs ==
opt=False N= 20: original=1.63ms x1.00 | V1=0.86ms x1.89 | V2=0.69ms x2.38 | OFF=1.64ms x0.99
opt=False N= 40: original=4.84ms x1.00 | V1=1.79ms x2.70 | V2=1.21ms x4.00 | OFF=4.76ms x1.02
opt=False N= 80: original=15.71ms x1.00 | V1=4.18ms x3.76 | V2=2.44ms x6.45 | OFF=15.76ms x1.00
opt=False N=160: original=61.20ms x1.00 | V1=11.09ms x5.52 | V2=5.23ms x11.69 | OFF=57.76ms x1.06
opt=False N=320: original=233.65ms x1.00 | V1=36.48ms x6.41 | V2=12.34ms x18.93 | OFF=263.18ms x0.89
opt=True N= 20: original=1.86ms x1.00 | V1=1.83ms x1.02 | V2=1.50ms x1.24 | OFF=1.88ms x0.99
opt=True N= 40: original=3.96ms x1.00 | V1=3.83ms x1.03 | V2=2.76ms x1.43 | OFF=3.97ms x1.00
opt=True N= 80: original=9.66ms x1.00 | V1=9.17ms x1.05 | V2=5.62ms x1.72 | OFF=9.49ms x1.02
opt=True N=160: original=25.49ms x1.00 | V1=25.06ms x1.02 | V2=12.34ms x2.07 | OFF=25.73ms x0.99
opt=True N=320: original=88.96ms x1.00 | V1=83.22ms x1.07 | V2=32.83ms x2.71 | OFF=95.74ms x0.93
== pentes ==
opt=False original 
… [846 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Implémentation d'une variante V3 (index de GV trié + cache) pour mesurer le plafond

- **bash** `{"command": "cat > /tmp/bench_v3.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"V3 locale : cache V2 + index de GV pré-trié (gauche/droite) au lieu du tri par segment.\"\"\"\nfrom __future__ import annotations\nimport bisect, json, pathlib, statistics, sys, time\nRACINE = pathlib.Path(\"/home/stephane/Dat … [5115 caractères tronqués]`

  ```
== égalité V3 ==
opt False corpus 612 / 612
  N 20 egal
  N 40 egal
  N 80 egal
  N 160 egal
  N 320 egal
opt True corpus 611 / 612
  N 20 egal
  N 40 egal
  N 80 egal
  N 160 egal
  N 320 egal
== temps V3 (entrelacé) ==
opt=False N=  20: original=1.86ms x1.00 | V2=0.71ms x2.61 | V3=0.73ms x2.56
opt=False N=  40: original=4.74ms x1.00 | V2=1.25ms x3.79 | V3=1.32ms x3.59
opt=False N=  80: original=16.31ms x1.00 | V2=2.49ms x6.56 | V3=2.71ms x6.02
opt=False N= 160: original=71.57ms x1.00 | V2=5.55ms x12.91 | V3=6.57ms x10.90
opt=False N= 320: original=252.89ms x1.00 | V2=13.54ms x18.68 | V3=16.02ms x15.78
opt=False N= 640: original=989.78ms x1.00 | V2=35.66ms x27.75 | V3=48.58ms x20.37
opt=False N=1280: original=3844.42ms x1.00 | V2=109.05ms x35.25 | V3=143.35ms x26.82
opt=True N=  20: original=3.30ms x1.00 | V2=2.41ms x1.37 | V3=2.50ms x1.32
opt=True N=  40: original=3.97ms x1.00 | V2=2.82ms x1.41 | V3=2.83ms x1.40
opt=True N=  80: original=10.60ms x1.00 | V2=6.50ms x1.63 | V3=6.23ms x1.70
opt=True N= 160: original=26.99ms x1.00 | V2=14.36ms x1.88 | V3=14.18ms x1.90
opt=True N= 320: original=85.26ms x1.00 | V2=33.93ms x2.51 | V3=42.02ms x2.03
opt=True N= 640: original=306.67ms x1.00
… [201 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'/tmp')\nimport bloc_linguistique as bl, evaluer_gold as eg\nimport bench_v3 as v3\nph=eg.charger()\nh0= … [757 caractères tronqués]`

  ```
== égalité V3 ==
opt False corpus 612 / 612
  N 20 egal
  N 40 egal
  N 80 egal
  N 160 egal
  N 320 egal
opt True corpus 611 / 612
  N 20 egal
  N 40 egal
  N 80 egal
  N 160 egal
  N 320 egal
== temps V3 (entrelacé) ==
opt=False N=  20: original=1.88ms x1.00 | V2=0.74ms x2.52 | V3=0.80ms x2.34
opt=False N=  40: original=4.63ms x1.00 | V2=1.23ms x3.76 | V3=1.32ms x3.51
opt=False N=  80: original=16.78ms x1.00 | V2=2.43ms x6.92 | V3=2.61ms x6.42
opt=False N= 160: original=57.01ms x1.00 | V2=5.37ms x10.62 | V3=5.97ms x9.55
opt=False N= 320: original=238.72ms x1.00 | V2=13.75ms x17.36 | V3=15.27ms x15.64
opt=False N= 640: original=987.77ms x1.00 | V2=38.41ms x25.72 | V3=44.11ms x22.39
opt=False N=1280: original=3834.43ms x1.00 | V2=107.20ms x35.77 | V3=157.06ms x24.41
opt=True N=  20: original=1.98ms x1.00 | V2=1.50ms x1.32 | V3=1.50ms x1.32
opt=True N=  40: original=4.08ms x1.00 | V2=4.18ms x0.98 | V3=3.51ms x1.16
opt=True N=  80: original=9.26ms x1.00 | V2=5.72ms x1.62 | V3=5.75ms x1.61
opt=True N= 160: original=26.33ms x1.00 | V2=13.90ms x1.89 | V3=18.51ms x1.42
opt=True N= 320: original=88.70ms x1.00 | V2=32.91ms x2.69 | V3=34.19ms x2.59
opt=True N= 640: original=310.70ms x1.00 |
… [550 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'/tmp')\nimport bloc_linguistique as bl\nimport bench_v3 as v3\ntexte='The car is red; it runs fast.'\nh=v3.HV3()\norig_vp=bl.Heuristique._verbes_proches\nor … [874 caractères tronqués]`

  ```
== égalité V3 ==
opt False corpus 612 / 612
  N 20 egal
  N 40 egal
  N 80 egal
  N 160 egal
  N 320 egal
opt True corpus 611 / 612
  N 20 egal
  N 40 egal
  N 80 egal
  N 160 egal
  N 320 egal
== temps V3 (entrelacé) ==
opt=False N=  20: original=1.60ms x1.00 | V2=0.68ms x2.36 | V3=0.74ms x2.17
opt=False N=  40: original=5.02ms x1.00 | V2=1.24ms x4.05 | V3=1.30ms x3.85
opt=False N=  80: original=15.36ms x1.00 | V2=2.44ms x6.30 | V3=2.61ms x5.88
opt=False N= 160: original=61.64ms x1.00 | V2=5.45ms x11.30 | V3=6.16ms x10.01
opt=False N= 320: original=230.59ms x1.00 | V2=12.65ms x18.23 | V3=15.07ms x15.30
opt=False N= 640: original=946.70ms x1.00 | V2=38.01ms x24.91 | V3=44.28ms x21.38
opt=False N=1280: original=3700.94ms x1.00 | V2=124.83ms x29.65 | V3=149.15ms x24.81
opt=True N=  20: original=2.02ms x1.00 | V2=1.64ms x1.23 | V3=1.66ms x1.22
opt=True N=  40: original=4.14ms x1.00 | V2=2.92ms x1.42 | V3=3.01ms x1.38
opt=True N=  80: original=10.24ms x1.00 | V2=6.23ms x1.64 | V3=6.33ms x1.62
opt=True N= 160: original=30.42ms x1.00 | V2=13.95ms x2.18 | V3=14.10ms x2.16
opt=True N= 320: original=102.01ms x1.00 | V2=40.06ms x2.55 | V3=39.80ms x2.56
opt=True N= 640: original=322.17ms x1.0
… [150 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique(segmenter_s=False)\nt=\"Le chat de la voisine est sur le toit.\"\nmots=h._mots(t)\nprint(mots)\nprint('POS:',[(x[2],h._pos('fr … [688 caractères tronqués]`

  ```
[(0, 2, 'Le', 'mot'), (3, 7, 'chat', 'mot'), (8, 10, 'de', 'mot'), (11, 13, 'la', 'mot'), (14, 21, 'voisine', 'mot'), (22, 25, 'est', 'mot'), (26, 29, 'sur', 'mot'), (30, 32, 'le', 'mot'), (33, 37, 'toit', 'mot'), (37, 38, '.', 'ponctuation')]
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 8, in <module>
AttributeError: 'Heuristique' object has no attribute '_est_verbe'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, statistics, time\nsys.path.insert(0,'tools'); sys.path.insert(0,'/tmp')\nimport bloc_linguistique as bl\nimport bench_cout_chunker as b\nfor n in (160,320,640):\n    t=' '.join([b.BASE]*(n//10)); h=bl.He … [1110 caractères tronqués]`

  ```
N 160 segments 48 gvs 16
  appels verbe_dans cible: 512 par segment 10.666666666666666
  premier GV 'est sur le toit' -> 'est'
N 320 segments 96 gvs 32
  appels verbe_dans cible: 2048 par segment 21.333333333333332
  premier GV 'est sur le toit' -> 'est'
N 640 segments 192 gvs 64
  appels verbe_dans cible: 8192 par segment 42.666666666666664
  premier GV 'est sur le toit' -> 'est'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, statistics, time\nsys.path.insert(0,'tools'); sys.path.insert(0,'/tmp')\nimport bloc_linguistique as bl\nimport bench_cout_chunker as b\nbases={\n 'A_aux': \"Le chat de la voisine est sur le toit.\",\n ' … [1646 caractères tronqués]`

  ```
=== A_aux 'Le chat de la voisine est sur le toit.' tokens 10
 opt False simple segs [('GN', 'Le chat'), ('GP', 'de la voisine'), ('GV', 'est sur le toit')] simple GV 1 S GV []
   N 160 orig 61.68ms V2 9.83ms gain x6.27
   N 320 orig 235.91ms V2 12.73ms gain x18.53
 opt True simple segs [('GN', 'Le chat'), ('GP', 'de la voisine'), ('GV', 'est sur le toit')] simple GV 1 S GV ['est']
   N 160 orig 26.53ms V2 23.58ms gain x1.13
   N 320 orig 88.88ms V2 32.14ms gain x2.77

=== B_plein 'Le chat de la voisine a vu la souris.' tokens 10
 opt False simple segs [('GN', 'Le chat'), ('GP', 'de la voisine'), ('GP', 'a'), ('GN', 'la souris')] simple GV 0 S GV []
   N 160 orig 87.80ms V2 4.49ms gain x19.54
   N 320 orig 323.82ms V2 9.88ms gain x32.77
 opt True simple segs [('GN', 'Le chat'), ('GP', 'de la voisine'), ('GP', 'a'), ('GN', 'la souris')] simple GV 0 S GV ['a vu']
   N 160 orig 16.07ms V2 11.61ms gain x1.38
   N 320 orig 28.74ms V2 24.83ms gain x1.16

=== C_plein2 'Le chat de la voisine regarde la souris.' tokens 9
 opt False simple segs [('GN', 'Le chat'), ('GP', 'de la voisine'), ('GN', 'la souris')] simple GV 0 S GV []
   N 160 orig 54.25ms V2 4.23ms gain x12.81
   N 320 orig 227.90
… [218 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Variante V4 : fusionner `_cible_proche` et `_verbes_proches` (un seul tri par segment)

- **bash** `{"command": "cat > /tmp/bench_v4.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"V4 locale : cache V2 + un seul tri de GV par segment, partagé cible/candidats.\"\"\"\nfrom __future__ import annotations\nimport json, pathlib, statistics, sys, time\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/Gi … [3876 caractères tronqués]`

  ```
== égalité V4 ==
opt False corpus 612 / 612
  N 20 egal
  N 40 egal
  N 80 egal
  N 160 egal
  N 320 egal
opt True corpus 611 / 612
  N 20 egal
  N 40 egal
  N 80 egal
  N 160 egal
  N 320 egal
== temps V4 (entrelacé) ==
opt=False N= 20: original=1.66ms x1.00 | V2=0.70ms x2.38 | V4=0.85ms x1.96
opt=False N= 40: original=4.81ms x1.00 | V2=1.34ms x3.58 | V4=2.09ms x2.30
opt=False N= 80: original=17.20ms x1.00 | V2=2.61ms x6.58 | V4=4.96ms x3.47
opt=False N=160: original=67.14ms x1.00 | V2=5.44ms x12.34 | V4=15.46ms x4.34
opt=False N=320: original=234.86ms x1.00 | V2=17.06ms x13.77 | V4=57.16ms x4.11
opt=True N= 20: original=1.90ms x1.00 | V2=1.46ms x1.30 | V4=1.73ms x1.09
opt=True N= 40: original=3.93ms x1.00 | V2=2.71ms x1.45 | V4=3.21ms x1.22
opt=True N= 80: original=9.11ms x1.00 | V2=5.55ms x1.64 | V4=7.66ms x1.19
opt=True N=160: original=26.50ms x1.00 | V2=13.83ms x1.92 | V4=22.47ms x1.18
opt=True N=320: original=84.45ms x1.00 | V2=33.45ms x2.52 | V4=74.59ms x1.13
JSON -> /tmp/bench_v4.json
[stderr]

real	0m8,928s
user	0m8,893s
sys	0m0,040s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, cProfile, pstats, io\nsys.path.insert(0,'tools'); sys.path.insert(0,'/tmp')\nimport bloc_linguistique as bl\nimport bench_cout_chunker as b\nfor n in (640,1280):\n    t=b.texte_n(n)\n    for nom,h in ((' … [381 caractères tronqués]`

  ```
=== 640 orig
         2935956 function calls in 8.511 seconds

   Ordered by: internal time
   List reduced from 135 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   118592    2.627    0.000    5.657    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:428(_est_verbe)
  1583619    2.192    0.000    2.192    0.000 {method 'endswith' of 'str' objects}
   188673    0.771    0.000    1.299    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:144(_normaliser)
    33856    0.671    0.000    7.159    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:638(_verbe_dans)
   188865    0.273    0.000    0.273    0.000 {method 'casefold' of 'str' objects}
   193652    0.262    0.000    0.262    0.000 {built-in method unicodedata.normalize}
    33921    0.146    0.000    0.381    0.000 /usr/lib64/python3.13/re/__init__.py:280(finditer)
    95898    0.142    0.000    0.142    0.000 {method 'group' of 're.Match' objects}
      321    0.131    0.000    7.578    0.024 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:657(_cible_p
… [3698 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection du format des fiches et JSON `pensee-*` existants

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' reports/rapport-pensee-gold-syntagmes.md", "description": "Read an existing report format"}`

  ```
# B13 — les syntagmes neuronaux : BIO, tête 0,7606, et la politique de fusion

> **Ligne de roadmap** : **B13** (moteur de pensée) / **R0.7** (bloc linguistique) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **le tagger de syntagmes 7B local est qualifié** — exact **0,6173** (heuristique
> **0,1992**), **tête 0,7606** (heuristique **0,5614**), **0 refus**, **180 appels**. La cascade à
> **priorité confiance** rend **0,6168 / 0,7592** ; la cascade par défaut (priorité heuristique)
> reste à **0,2137 / 0,5670** : **la politique de fusion est le goulot**, pas le modèle.
>
> **Dispositif** : [`qualifier_syntagmes.py`](../tools/tests/linguistique/qualifier_syntagmes.py) ;
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`NeuronalLLMChunks`,
> `priorite_syntagme`) ; JSON [`pensee-gold-syntagmes.json`](pensee-gold-syntagmes.json).

## 1. Ce qui était mesuré

Le gold neuronal POS est qualifié : **0,8483** seul, **0,9440** en cascade, sans perte sur les
réelles ([`pensee-gold-neuronal`](rapport-pensee-gold-neuronal.md)). Le niveau suivant est le
**syntagme** : GN, GV, GP, REL, SUB. L'heuristique y est faible — exact **0,1992**, tête
**0,5614** sur les 180 — parce que ses découpes so
… [6416 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nfor f in ['reports/pensee-quatre-modes.json','reports/pensee-gold-syntagmes.json']:\n    d=json.load(open(f))\n    print('===',f, type(d), list(d)[:20] if isinstance(d,dict) else len(d))\n    print(json … [98 caractères tronqués]`

  ```
=== reports/pensee-quatre-modes.json <class 'dict'> ['date', 'gold', 'modes', 'seuils', 'refus', 'refus_detail', 'appels', 'api', 'latence_s', 'duree_totale_s', 'limites']
{
 "date": "2026-11-04 10:37 EST",
 "gold": {
  "phrases": 3,
  "tokens": 14,
  "modalite": "api-deepseek (deepseek-chat), aucun serveur local"
 },
 "modes": {
  "heuristique": {
   "all": {
    "pos": {
     "exactitude": 0.8571,
     "exactitude_ferme": 1.0,
     "exactitude_ouvert": 0.75,
     "tokens": 14,
     "confusions": {
      "DET": {
       "DET": 5
      },
      "NOUN": {
       "NOUN": 4,
       "ADJ": 1
      },
      "PRON": {
       "PRON": 1
      },
      "VERB": {
       "VERB": 2,
       "NOUN": 1
      }
     }
    },
    "syntagme": {
     "precision": 0.7,
     "rappel": 0.7778,
     "f1": 0.7368,
     "tp": 7,
     "fp": 3,
     "fn": 2,
     "tete": {
      "precision": 0.875,
      "rappel": 0.7778,
      "f1": 0.8235,
      "tp": 7,
      "fp": 1,
      "fn": 2
     }
    },
    "tete": {
     "precision": 0.875,
     "rappel": 0.7778,
     "f1": 0.8235,
     "tp": 7,
     "fp": 1,
     "fn": 2
    },
    "pragmatique": {
     "acte": 1.0,
     "negation": 1.0,
     "modalite": 1.0,
 
… [2770 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction et vérification des chiffres pour la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, math\nR=json.load(open('/tmp/bench_cout_robuste.json'))\nF=json.load(open('/tmp/bench_cout_chunker.json'))\nV3=json.load(open('/tmp/bench_v3.json'))\nprint('--- corpus ---')\nprint('n',F['corpus']['n'], … [1995 caractères tronqués]`

  ```
--- corpus ---
n 612 tokens_gold 3179 chars 16371
opt False
  original cpu=  226.7ms min=  219.1 gain=1.000
  V1       cpu=  195.7ms min=  192.4 gain=1.158
  V2       cpu=  190.3ms min=  184.2 gain=1.191
  OFF      cpu=  228.3ms min=  221.6 gain=0.993
  counts orig {'simple_total': 1966, 'simple_moy': 3.212418300653595, 'simple_min': 1, 'simple_max': 7, 'verbe_total': 197, 'verbe_moy': 0.32189542483660133, 'segments_moy': 1.1045751633986929, 'gv_moy': 0.18627450980392157, 'tokens_moy': 6.125816993464053}
  counts v2 {'simple_appels_moy': 3.212418300653595, 'simple_miss_moy': 1, 'simple_miss_max': 1, 'gv_appels_moy': 0.32189542483660133, 'gv_miss_moy': 0.13562091503267973, 'gv_miss_max': 2}
opt True
  original cpu=  389.3ms min=  383.0 gain=1.000
  V1       cpu=  381.0ms min=  370.1 gain=1.022
  V2       cpu=  372.3ms min=  356.2 gain=1.045
  OFF      cpu=  394.7ms min=  383.2 gain=0.986
  counts orig {'simple_total': 1224, 'simple_moy': 2, 'simple_min': 2, 'simple_max': 2, 'verbe_total': 1961, 'verbe_moy': 3.204248366013072, 'segments_moy': 1.1045751633986929, 'gv_moy': 0.18627450980392157, 'tokens_moy': 6.125816993464053}
  counts v2 {'simple_appels_moy': 2, 'simple_miss_moy': 1, 
… [8506 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum tools/bloc_linguistique.py /tmp/bench_cout_chunker.py /tmp/bench_cout_robuste.py /tmp/bench_v3.py /tmp/bench_v4.py && git rev-parse --short HEAD && date '+%Y-%m-%d %H:%M %Z'", "description": "Get hashes, commit, and date"}`

  ```
6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65  tools/bloc_linguistique.py
236a4d797e1c1c30164ab198d97c86435fc66f7ebec6896b00e589e2d0d9013c  /tmp/bench_cout_chunker.py
e9474ee92cea8130355870ff6b406d383667613aad1d0ee990bbbb51e7f9cee3  /tmp/bench_cout_robuste.py
dd84de8e72e6de2e4d71e3683da44e29ffcc9e6f43fd108ceee16a5fd532ed70  /tmp/bench_v3.py
70f40fb38438ba509df977c67106f09db62330f7599d95af5c5b8022afb3f777  /tmp/bench_v4.py
e1171032
2026-11-05 13:54 EST
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la reports/rapport-cout-chunker.md reports/pensee-cout-chunker.json 2>&1 || true && grep -n \"gvs_simple\\|for s in self._syntagmes_simple\\|gvs_u\\|simples = self._syntagmes_simple\" tools/bloc_linguistique.py", "description": " … [43 caractères tronqués]`

  ```
ls: cannot access 'reports/rapport-cout-chunker.md': No such file or directory
ls: cannot access 'reports/pensee-cout-chunker.json': No such file or directory
861:            gvs_simple = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
866:                gvs = gvs_s + [x for x in gvs_simple if (x["debut"], x["fin"]) not in deja]
914:            for s in self._syntagmes_simple(texte, lg):
928:            simples = self._syntagmes_simple(texte, lg)
929:            gvs_u = ([x for x in cands[0].get("segments", []) if x.get("type") == "GV"]
935:                cible = self._cible_proche(texte, s, gvs_u, verbes)
940:                                            candidats=[s["type"]] + self._verbes_proches(texte, s, gvs_u, verbes=verbes),
  ```

### 🤖 Assistant

⏵ Alerte : le fichier mesuré a changé (hash différent) — vérification du diff concurrent

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/bloc_linguistique.py && git diff --stat -- tools/bloc_linguistique.py && git diff -- tools/bloc_linguistique.py | head -120", "description": "Check concurrent modification of measured file"}`

  ```
M tools/bloc_linguistique.py
 tools/bloc_linguistique.py | 66 +++++++++++++++++++++++++++++++++++++++-------
 1 file changed, 57 insertions(+), 9 deletions(-)
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 65fb0d76..5cc3858f 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -413,6 +413,9 @@ come comes came coming take takes took taken taking put puts putting say says sa
 see sees saw seen seeing know knows knew known knowing want wants wanted wanting need needs
 needed needing help helps helped helping look looks looked looking give gives gave given
 find finds found finding open opens opened opening close closes closed closing
+fly flies flew flown flying climb climbs climbed climbing flow flows flowed flowing
+swim swims swam swum swimming get gets got gotten getting smile smiles smiled smiling
+wait waits waited waiting belong belongs belonged belonging
 """.split())
 
 
@@ -613,6 +616,21 @@ class Heuristique:
         except Exception:
             return {}
 
+    @staticmethod
+    def _tete_texte(texte: str) -> str | None:
+        """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.
+

… [5026 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '810,950p' tools/bloc_linguistique.py", "description": "Read current syntagm section"}`

  ```
self.nom, 0.99, langue=lg, script=script))
            i = j

        # 2. mot + POS fermées / ouvertes
        mots = self._mots(texte)
        for d, f, t, typ in mots:
            etiquettes.append(Etiquette("mot", typ, t, d, f, self.nom, 0.98, langue=lg, script=script))
            if typ == "mot":
                classe, ouvert, conf = self._pos(lg, t)
                etiquettes.append(Etiquette("pos", classe, t, d, f, self.nom, conf,
                                            candidats=[] if not ouvert else [classe.lower()],
                                            langue=lg, script=script, meta={"ouvert": ouvert}))
                if ouvert:
                    unites.append(Span(d, f))
                # 3. morphème (candidat, basse confiance)
                for genre, md, mf, aff in self._morphemes(t):
                    etiquettes.append(Etiquette("morphème", genre, aff, d + md, d + mf,
                                                self.nom, 0.32, candidats=[genre],
                                                langue=lg, script=script))

        # 4. phrase + pragmatique
        for d, f, p, typ in self._phrases(texte):
            etiquettes.append(Etiquette("p
… [8066 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Le fichier a été édité concurremment ; je re-mesure sur l'instantané courant et je fige le hash

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _cible_proche\\|def _verbes_proches\\|def _syntagmes_simple\\|def analyser\" tools/bloc_linguistique.py | head -12 && grep -n \"gvs_simple\\|for s in self._syntagmes_simple\\|simples = self._syntagmes_simple\\|gvs_u\" t … [70 caractères tronqués]`

  ```
133:    def analyser(self, texte: str, langue: str | None = None,
661:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
688:    def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
725:    def _syntagmes_simple(self, texte: str, langue: str) -> list[dict]:
783:    def analyser(self, texte: str, langue: str | None = None,
1013:    def analyser(self, texte: str, langue: str | None = None,
1082:    def analyser(self, texte: str, langue: str | None = None,
1192:    def analyser(self, texte: str, langue: str | None = None,
1326:    def analyser(self, texte: str, langue: str | None = None,
1418:    def analyser(self, texte: str, langue: str | None = None,
1496:    def analyser(self, texte: str, langue: str | None = None,
1679:    def analyser(self, texte: str, langue: str | None = None,
861:            gvs_simple = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
866:                gvs = gvs_s + [x for x in gvs_simple if (x["debut"], x["fin"]) not in deja]
914:            for s in self._syntagmes_simple(texte, lg):
928:            simples = self._syntagmes_simple(texte, lg)
929:            gvs_u = ([x for x in cands[0].get("segments", []) if
… [221 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nl -ba tools/bloc_linguistique.py | sed -n '852,945p'", "description": "Numbered current syntagm section"}`

  ```
852	
   853	        # 5. syntagmes : le générateur S (candidats) ou un chunker simple
   854	        verbes = [(e.debut, e.fin, e.valeur) for e in etiquettes
   855	                  if e.niveau == "pos" and e.type == "VERB"]
   856	        cands = self._syntagmes_s(texte)
   857	        cibles_s = self._cibles_s(texte) if cands else {}
   858	        if cands:
   859	            # les GV du chunker complètent ceux du générateur S : sans eux, un GP n'a aucun
   860	            # candidat d'attachement (diagnostic des 33 échecs de T162).
   861	            gvs_simple = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
   862	            for c in cands[:1]:
   863	                noms = [x.get("nom", "") for x in cands]
   864	                gvs_s = [x for x in c.get("segments", []) if x.get("type") == "GV"]
   865	                deja = {(x["debut"], x["fin"]) for x in gvs_s}
   866	                gvs = gvs_s + [x for x in gvs_simple if (x["debut"], x["fin"]) not in deja]
   867	                for s in c.get("segments", []):
   868	                    # la cible de S **convertie en son verbe** : « Les enfants jouent » →
   869	                    # `jouent` (le 
… [5776 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _verbe_dans\\|_cible_proche(texte\\|_verbes_proches(texte\\|_verbe_dans(texte\" tools/bloc_linguistique.py | sed -n '1,30p'", "description": "Locate helper definitions and calls"}`

  ```
642:    def _verbe_dans(texte: str, debut: int, fin: int,
661:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
681:            v = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
685:        return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
688:    def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
701:            v = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
883:                                cible = self._verbe_dans(texte, g["debut"], g["fin"], verbes)
887:                        cible = self._cible_proche(texte, s, gvs, verbes)
891:                            cible = self._verbe_dans(texte, i, i + len(brute), verbes)
895:                        cible = self._cible_proche(texte, s, gvs, verbes)
899:                    candidats = list(noms) + self._verbes_proches(texte, s, gvs, verbes=verbes)
916:                cible = self._cible_proche(texte, s, [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"], verbes)
922:                                            candidats=[s["type"]] + self._verbes_proches(texte, s, gvs_s, verbes=verbes),
935:                cible = self._cible_proche(texte,
… [144 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Banc consolidé sur l'instantané courant (hash figé) : corpus, longueurs, continuité, contrôles

- **bash** `{"command": "cat > /tmp/bench_final.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"Banc consolidé — instantané courant de tools/bloc_linguistique.py, HORS DÉPÔT.\n\nMesure : corpus 612, longueurs 20..320 (+640/1280 en continuité), appels réels,\nvariantes V1 (chunking caché), V2 (chunking + verbes de GV c … [15047 caractères tronqués]`

  ```
corpus opt=False: original=230.6ms x1.00 | V1=197.2ms x1.17 | V2=189.4ms x1.22 | OFF=228.7ms x1.01
corpus opt=True: original=385.1ms x1.00 | V1=371.8ms x1.04 | V2=396.0ms x0.97 | OFF=402.4ms x0.96
longueurs...
  opt=False N= 20: original=1.75ms x1.00 | V1=0.93ms x1.87 | V2=0.73ms x2.40 | OFF=1.75ms x1.00
  opt=False N= 40: original=5.04ms x1.00 | V1=1.95ms x2.58 | V2=1.31ms x3.83 | OFF=5.58ms x0.90
  opt=False N= 80: original=17.29ms x1.00 | V1=4.51ms x3.83 | V2=2.57ms x6.73 | OFF=16.39ms x1.05
  opt=False N=160: original=64.82ms x1.00 | V1=11.80ms x5.49 | V2=5.58ms x11.61 | OFF=57.61ms x1.13
  opt=False N=320: original=238.00ms x1.00 | V1=34.80ms x6.84 | V2=14.09ms x16.89 | OFF=233.01ms x1.02
  opt=True N= 20: original=1.98ms x1.00 | V1=1.92ms x1.03 | V2=1.58ms x1.26 | OFF=1.99ms x0.99
  opt=True N= 40: original=4.23ms x1.00 | V1=4.10ms x1.03 | V2=2.99ms x1.41 | OFF=4.19ms x1.01
  opt=True N= 80: original=9.89ms x1.00 | V1=9.62ms x1.03 | V2=6.08ms x1.63 | OFF=9.82ms x1.01
  opt=True N=160: original=27.83ms x1.00 | V1=26.71ms x1.04 | V2=13.94ms x2.00 | OFF=28.41ms x0.98
  opt=True N=320: original=88.38ms x1.00 | V1=89.73ms x0.99 | V2=36.88ms x2.40 | OFF=89.10ms x0.99
continuité...

… [682 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/bench_final.json'))\nprint('meta', {k:v for k,v in d['meta'].items() if k not in ('sha256_mesure','mtime_mesure')})\nprint('\\negalite corpus', d['corpus']['egalite'])\nprint('cor … [1254 caractères tronqués]`

  ```
meta {'titre': "Coût des règles d'attachement du chunker", 'date': '2026-11-05T13:58:19-0500', 'branche': 's/v7', 'commit': 'e1171032', 'fichier': 'tools/bloc_linguistique.py', 'python': '3.13.16', 'cpu': 'Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz', 'methode': 'time.process_time(), rounds entrelacés, médiane ; sortie comparée champ à champ', 'banc': {'chemin': '/tmp/bench_final.py', 'sha256': '6c823a1f5cbcc249e619ef27465f0ff4c8cb2cc4c40b9cb9ba5de5db6b58a7e3'}, 'duree_banc_s': 82.89590978622437, 'sha256_apres_banc': '6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65', 'fichier_change_pendant_banc': False}

egalite corpus {'False': {'V1': '612/612', 'V2': '612/612', 'OFF': '612/612'}, 'True': {'V1': '612/612', 'V2': '612/612', 'OFF': '612/612'}}
corpus stats {'n': 612, 'mots_gold': 3179, 'chars': 16371, 'langues': {'en': 210, 'fr': 402}, 'segments_moy': 1.1045751633986929, 'gv_moy': 0.18627450980392157, 'tokens_mots_moy': 6.125816993464053}
compteurs orig {'False': {'simple_total': 1966, 'simple_moy': 3.212418300653595, 'simple_min': 1, 'simple_max': 7, 'verbe_total': 197, 'verbe_moy': 0.32189542483660133}, 'True': {'simple_total': 1224, 'simple_moy': 2, 'simple_min':
… [7997 caractères tronqués]
  ```

- **read** `{"file_path": "tools/bloc_linguistique.py", "offset": 642, "limit": 64}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
642:     def _verbe_dans(texte: str, debut: int, fin: int,
643:                     verbes: list[tuple[int, int, str]] | None = None,
644:                     strict: bool = False) -> str | None:
645:         """Le **verbe** du span : le lexique d'abord, puis le POS `VERB`, sinon le dernier mot."""
646:         mots = [(m.start() + debut, m.group()) for m in re.finditer(r"[\wÀ-ÿ'-]+", texte[debut:fin])]
647:         # le verbe **plein** d'abord : « J'ai vu » donne `vu`, pas `ai`
648:         for _, m in mots:
649:             if _est_verbe(m) and _normaliser(m) not in AUXILIAIRES:
650:                 return m
651:         for _, m in mots:
652:             if _est_verbe(m):
653:                 return m
654:         if verbes:
655:             for d, f, v in verbes:
656:                 if d >= debut and f <= fin:
657:                     return v
658:         return None if strict else (mots[-1][1] if mots else None)
659: 
660:     @staticmethod
661:     def _cible_proche(texte: str, segment: dict, gvs: list[dict],
662:                       verbes: list[tuple[int, 
… [2426 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Re-mesure ciblée du corpus (11 passes) pour trancher le gain court

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, time, statistics\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'/tmp')\nimport bloc_linguistique as bl, evaluer_gold as eg, bench_cout_chunker as b\nph=eg. … [927 caractères tronqués]`

  ```
opt False {'original': 231.4, 'V1': 193.3, 'V2': 196.6, 'OFF': 228.8} {'original': 1.0, 'V1': 1.197, 'V2': 1.177, 'OFF': 1.011}
  tous V2 [236.5, 222.2, 196.6, 191.1, 194.8, 192.2, 216.3, 207.7, 185.5, 216.0, 191.0]
opt True {'original': 394.4, 'V1': 374.2, 'V2': 367.6, 'OFF': 393.5} {'original': 1.0, 'V1': 1.054, 'V2': 1.073, 'OFF': 1.002}
  tous V2 [370.7, 367.6, 392.4, 395.1, 366.7, 367.0, 357.9, 363.3, 373.3, 376.0, 353.6]
  ```

### 🤖 Assistant

⏵ Vérification de l'état git (fichiers générés, pas de modification induite)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | sed -n '1,80p' && echo '--- pycache ---' && git status --short --ignored | grep -i pycache | head -10 || true && echo '--- hash ---' && sha256sum tools/bloc_linguistique.py", "description": "Check git status and  … [9 caractères tronqués]`

  ```
M docs/implantation/moteur-de-pensee.md
 M docs/pilotage/chantiers.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/rapport.md
D  journal/sessions/65495a29-10c0-4571-96be-e7729f1efebf/digest.md
D  journal/sessions/65495a29-10c0-4571-96be-e7729f1efebf/rapport.md
MM journal/sessions/MANIFEST.md
D  journal/sessions/a8035275-c
… [2742 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Construction du JSON `pensee-cout-chunker.json` à partir des mesures

- **bash** `{"command": "cat > /tmp/build_pensee.py <<'PY'\nimport json, pathlib, time\nR = json.load(open('/tmp/bench_final.json'))\nout = {}\nout['date'] = R['meta']['date']\nout['titre'] = \"Coût des règles d'attachement du chunker\"\nout['verdict'] = (\n    \"O(n²) confirmé sur le chemin chunker seul : 1+2S … [15369 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-cout-chunker.json 23415
JSON_VALIDE
{
 "date": "2026-11-05T13:58:19-0500",
 "titre": "Coût des règles d'attachement du chunker",
 "verdict": "O(n²) confirmé sur le chemin chunker seul : 1+2S appels à _syntagmes_simple (3,21/phrase sur le gold, 97 à 160 tokens, 193 à 320) ; temps ×3,7 par doublement 160→320. Le cache mesuré (un chunking + un verbe de GV par analyse) donne ×11,6 à 160 et ×16,9 à 320 sur ce chemin, ×2,0 et ×2,4 sur le chemin par défaut. Le chemin par défaut n'appelle _syntagmes_simple que 2 fois/phrase : le re-chunking y est du code mort ; son coût quadratique vient de _verbe_dans (2 320 appels pour 32 GV distincts à 160 ; 8 736 pour 64 à 320), ramenés aux GV distincts par le cache. Le tri sorted(gvs, key=ecart) par segment reste : la cache ne rend pas la complexité strictement linéaire (pente V2 1,44-1,55 sur 160-1280). Sur le corpus court : ×1,18-1,20 (chunker) et ×1,05-1,07 (défaut).",
 "instantane": {
  "fichier": "tools/bloc_linguistique.py",
  "sha256": "6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65",
  "sha256_apres_banc": "6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b40
… [2107 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-cout-chunker.json'))\nfor k in ('longueurs','complexite','controle_negatif','correctif_propose','sensibilite_base_verbe_plein','pistes_rejetees'):\n    print('===',k); p … [103 caractères tronqués]`

  ```
=== longueurs
{
 "base": "Le chat de la voisine est sur le toit.",
 "base_tokens": 10,
 "note": "base de 10 tokens répétée 2/4/8/16/32 fois ; N exact en tokens _mots",
 "points": [
  {
   "chemin": "chunker",
   "N": 20,
   "chars": 77,
   "segments_simple": 6,
   "gv_simple": 2,
   "segments_s": 0,
   "gv_s": 0,
   "etiquettes": 87,
   "temps_ms": {
    "original": 1.747,
    "V1": 0.933,
    "V2": 0.727,
    "OFF": 1.751
   },
   "gains": {
    "V1": 1.873,
    "V2": 2.402,
    "OFF": 0.998
   },
   "appels_origine": {
    "simple": 13,
    "verbe": 20
   },
   "appels_v2": {
    "appels_simple": 13,
    "miss_simple": 1,
    "appels_gv": 20,
    "miss_gv": 2
   },
   "egalite": {
    "V1": "1/1",
    "V2": "1/1",
    "OFF": "1/1"
   }
  },
  {
   "chemin": "chunker",
   "N": 40,
   "chars": 155,
   "segments_simple": 12,
   "gv_simple": 4,
   "segments_s": 0,
   "gv_s": 0,
   "etiquettes": 173,
   "temps_ms": {
    "original": 5.038,
    "V1": 1.95,
    "V2": 1.315,
    "OFF": 5.582
   },
   "gains": {
    "V1": 2.583,
    "V2": 3.832,
    "OFF": 0.902
   },
   "appels_origine": {
    "simple": 25,
    "verbe": 64
   },
   "appels_v2": {
    "appels_simple": 25,
    "miss_simple
… [10865 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/rapport-bloc-linguistique.md reports/pensee-bloc-linguistique.json 2>&1 || true && grep -n \"rapport-bloc-linguistique\\|bloc-linguistique\" reports/README.md | head -5", "description": "Check existing bloc report links"}`

  ```
ls: cannot access 'reports/pensee-bloc-linguistique.json': No such file or directory
reports/rapport-bloc-linguistique.md
76:| [`rapport-bloc-linguistique.md`](rapport-bloc-linguistique.md) | **R0.7** — le bloc linguistique : 9 niveaux, heuristique/neuronal, **398 langues** à 0,9687, activation 51–76 % |
  ```

### 🤖 Assistant

⏵ Génération des tableaux markdown à partir du JSON validé

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-cout-chunker.json'))\npts=d['longueurs']['points']\ndef fmt(x): return f\"{x:.2f}\".replace('.',',')\ndef f1(x): return f\"{x:.1f}\".replace('.',',')\ndef f3(x): return  … [3757 caractères tronqués]`

  ```
TABLE CORPUS
chunker
| original | 231,4 | ×1,000 | 378,1 |
| V1 | 193,3 | ×1,197 | 315,8 |
| V2 | 196,6 | ×1,177 | 321,2 |
| OFF | 228,8 | ×1,011 | 373,9 |
defaut
| original | 394,4 | ×1,000 | 644,4 |
| V1 | 374,2 | ×1,054 | 611,4 |
| V2 | 367,6 | ×1,073 | 600,7 |
| OFF | 393,5 | ×1,002 | 643,0 |

TABLE LONGUEURS CHUNKER
| N | S | G | original (ms) | V1 (ms) | gain V1 | V2 (ms) | gain V2 | OFF (ms) |
| 20 | 6 | 2 | 1,75 | 0,93 | ×1,873 | 0,73 | ×2,402 | 1,75 |
| 40 | 12 | 4 | 5,04 | 1,95 | ×2,583 | 1,31 | ×3,832 | 5,58 |
| 80 | 24 | 8 | 17,29 | 4,51 | ×3,829 | 2,57 | ×6,729 | 16,39 |
| 160 | 48 | 16 | 64,82 | 11,80 | ×5,494 | 5,58 | ×11,615 | 57,61 |
| 320 | 96 | 32 | 238,00 | 34,80 | ×6,840 | 14,10 | ×16,886 | 233,01 |

TABLE LONGUEURS DEFAUT
| N | S_S | G_S | original (ms) | V1 (ms) | gain V1 | V2 (ms) | gain V2 | OFF (ms) |
| 20 | 8 | 2 | 1,98 | 1,92 | ×1,033 | 1,58 | ×1,258 | 1,99 |
| 40 | 16 | 4 | 4,23 | 4,10 | ×1,032 | 2,99 | ×1,414 | 4,19 |
| 80 | 32 | 8 | 9,89 | 9,62 | ×1,027 | 6,08 | ×1,626 | 9,82 |
| 160 | 64 | 16 | 27,83 | 26,71 | ×1,042 | 13,94 | ×1,996 | 28,41 |
| 320 | 128 | 32 | 88,38 | 89,73 | ×0,985 | 36,88 | ×2,397 | 89,10 |

TABLE COMPLEXITE
| chemin | variante |
… [2032 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche `reports/rapport-cout-chunker.md`

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md", "content": "# Coût des règles d'attachement du chunker — O(n²) réel, cache ×12 à 160 tokens\n\n> **Date** : 2026-11-05 · **Instantané** : [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py)\n>  … [23313 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Corrections de la fiche (composition du corpus, facteur de doublement, ligne de contrôle)

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md", "old_string": "- **Corpus** : `evaluer_gold.charger()` = 542 phrases réelles/synthétiques + 20 « hand » = **612\n  phrases** (402 fr, 210 en), **3 179 mots gold**, **16 371 caractères**, **6,13 tokens\n  … [368 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md", "old_string": "   `sorted(gvs, key=ecart)` par segment est encore là, en O(S·G log G). À 1 280 tokens, le\n   doublement 640→1 280 coûte encore ×2,4 (chunker) et ×3,5 (défaut) pour V2.", "new_string": "  … [170 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md", "old_string": "| **compteurs N=160** | chunker : `_syntagmes_simple` 97 appels → 1 chunking, `_verbe_dans` 640 → 16 ; défaut : 2 → 1, 2 320 → 63 |", "new_string": "| **compteurs N=160** | chunker : `_syn … [114 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"542\\|×2,4 (chunker)\\|la cache\\|le cache ne rend\" reports/rapport-cout-chunker.md reports/pensee-cout-chunker.json | head -20", "description": "Search remaining inconsistencies"}`

  ```
reports/pensee-cout-chunker.json:4: "verdict": "O(n²) confirmé sur le chemin chunker seul : 1+2S appels à _syntagmes_simple (3,21/phrase sur le gold, 97 à 160 tokens, 193 à 320) ; temps ×3,7 par doublement 160→320. Le cache mesuré (un chunking + un verbe de GV par analyse) donne ×11,6 à 160 et ×16,9 à 320 sur ce chemin, ×2,0 et ×2,4 sur le chemin par défaut. Le chemin par défaut n'appelle _syntagmes_simple que 2 fois/phrase : le re-chunking y est du code mort ; son coût quadratique vient de _verbe_dans (2 320 appels pour 32 GV distincts à 160 ; 8 736 pour 64 à 320), ramenés aux GV distincts par le cache. Le tri sorted(gvs, key=ecart) par segment reste : la cache ne rend pas la complexité strictement linéaire (pente V2 1,44-1,55 sur 160-1280). Sur le corpus court : ×1,18-1,20 (chunker) et ×1,05-1,07 (défaut).",
reports/pensee-cout-chunker.json:102:    "verbe_moy": 0.32189542483660133
reports/pensee-cout-chunker.json:118:    "appels_gv_moy": 0.32189542483660133,
reports/pensee-cout-chunker.json:126:    "appels_gv_moy": 2.6013071895424837,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/pensee-cout-chunker.json')\ns=p.read_text(encoding='utf-8')\ns=s.replace('la cache ne rend pas la complexité strictement linéaire', 'le cache ne rend pas la complexité stricte … [352 caractères tronqués]`

  ```
ok
JSON_VALIDE
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"×1,0-1,07\\|×1,05-1,07\\|×0,97-1,07\" reports/rapport-cout-chunker.md reports/pensee-cout-chunker.json", "description": "Locate corpus gain ranges"}`

  ```
reports/rapport-cout-chunker.md:88:**Le gain corpus est donc faible et non monotone** — ×1,18-1,22 en chunker, ×0,97-1,07 en
reports/rapport-cout-chunker.md:182:- **corpus** : ×1,18-1,22 (chunker), ×1,0-1,07 (défaut). Pas de gain spectaculaire sur des
reports/rapport-cout-chunker.md:342:  faible (×1,18-1,22 chunker ; ×1,0-1,07 défaut) ; le O(n²) ne mord pas sur le gold actuel.
reports/rapport-cout-chunker.md:383:  ×1,18-1,22 (chunker) et ×1,0-1,07 (défaut). Le chantier suivant, si la linéarité devient
reports/pensee-cout-chunker.json:4: "verdict": "O(n²) confirmé sur le chemin chunker seul : 1+2S appels à _syntagmes_simple (3,21/phrase sur le gold, 97 à 160 tokens, 193 à 320) ; temps ×3,7 par doublement 160→320. Le cache mesuré (un chunking + un verbe de GV par analyse) donne ×11,6 à 160 et ×16,9 à 320 sur ce chemin, ×2,0 et ×2,4 sur le chemin par défaut. Le chemin par défaut n'appelle _syntagmes_simple que 2 fois/phrase : le re-chunking y est du code mort ; son coût quadratique vient de _verbe_dans (2 320 appels pour 32 GV distincts à 160 ; 8 736 pour 64 à 320), ramenés aux GV distincts par le cache. Le tri sorted(gvs, key=ecart) par segment reste : le cache ne rend pas la complex
… [343 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\nfor f in ('reports/rapport-cout-chunker.md','reports/pensee-cout-chunker.json'):\n    p=pathlib.Path(f); s=p.read_text(encoding='utf-8')\n    s=s.replace('×1,0-1,07', '×0,97-1,07')\n    s=s.replace(' … [388 caractères tronqués]`

  ```
ok
JSON_VALIDE
reports/rapport-cout-chunker.md:88:**Le gain corpus est donc faible et non monotone** — ×1,18-1,22 en chunker, ×0,97-1,07 en
reports/rapport-cout-chunker.md:182:- **corpus** : ×1,18-1,22 (chunker), ×0,97-1,07 (défaut). Pas de gain spectaculaire sur des
reports/rapport-cout-chunker.md:342:  faible (×1,18-1,22 chunker ; ×0,97-1,07 défaut) ; le O(n²) ne mord pas sur le gold actuel.
reports/rapport-cout-chunker.md:383:  ×1,18-1,22 (chunker) et ×0,97-1,07 (défaut). Le chantier suivant, si la linéarité devient
reports/pensee-cout-chunker.json:4: "verdict": "O(n²) confirmé sur le chemin chunker seul : 1+2S appels à _syntagmes_simple (3,21/phrase sur le gold, 97 à 160 tokens, 193 à 320) ; temps ×3,7 par doublement 160→320. Le cache mesuré (un chunking + un verbe de GV par analyse) donne ×11,6 à 160 et ×16,9 à 320 sur ce chemin, ×2,0 et ×2,4 sur le chemin par défaut. Le chemin par défaut n'appelle _syntagmes_simple que 2 fois/phrase : le re-chunking y est du code mort ; son coût quadratique vient de _verbe_dans (2 320 appels pour 32 GV distincts à 160 ; 8 736 pour 64 à 320), ramenés aux GV distincts par le cache. Le tri sorted(gvs, key=ecart) par segment reste : le cache ne r
… [361 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-cout-chunker.md'); s=p.read_text(encoding='utf-8')\ns=s.replace(\"Aucun fichier existant du dépôt n'a été modifié ; les deux fichiers de cette fiche sont\\n  neufs et  … [528 caractères tronqués]`

  ```
ok
72:  Aucun fichier existant n'a été modifié **par cette mission** ; les deux fichiers de cette
386:- **Aucun fichier existant n'a été modifié par cette mission ; aucun commit n'a été fait.** Les deux livrables
  ```

### 🤖 Assistant

⏵ Relecture complète de la fiche et vérification des liens/tableaux

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('reports/rapport-cout-chunker.md')\nlines=p.read_text(encoding='utf-8').splitlines()\n# tables: consecutive lines starting with |\ni=0; bad=[]\nwhile i < len(lines):\n    if lines[ … [692 caractères tronqués]`

  ```
lignes suspectes: [(79, 7, '| variante | chunker seul (ms) | gain | µs/phrase | défaut S (ms) | gain | µs/phrase |'), (80, 7, '|---|---:|---:|---:|---:|---:|---:|'), (81, 7, '| original | 231,4 | ×1,000 | 378,1 | 394,4 | ×1,000 | 644,4 |'), (82, 7, '| V1 (chunking caché) | 193,3 | ×1,197 | 315,8 | 374,2 | ×1,054 | 611,4 |'), (83, 7, '| **V2 (chunking + verbes)** | **196,6** | **×1,177** | **321,2** | **367,6** | **×1,073** | **600,7** |'), (84, 7, '| OFF (caches off) | 228,8 | ×1,011 | 373,9 | 393,5 | ×1,002 | 643,0 |'), (127, 8, '| chemin | variante | pente 20-160 | R² | pente 20-320 | R² | pente 160-1 280 | R² |'), (128, 8, '|---|---|---:|---:|---:|---:|---:|---:|'), (129, 8, '| chunker | original | **1,742** | 0,9976 | **1,786** | 0,9982 | **1,943** | 0,9996 |'), (130, 8, '| chunker | V1 | 1,219 | 0,9965 | 1,304 | 0,9943 | — | — |'), (131, 8, '| chunker | V2 | 0,979 | 0,9963 | 1,064 | 0,9921 | **1,438** | 0,9983 |'), (132, 8, '| chunker | OFF | 1,667 | 0,9991 | 1,748 | 0,9975 | — | — |'), (133, 8, '| défaut | original | **1,266** | 0,9949 | **1,367** | 0,9923 | **1,861** | 0,9964 |'), (134, 8, '| défaut | V1 | 1,263 | 0,9955 | 1,380 | 0,9910 | — | — |'), (135, 8, '| défaut | V2 
… [1074 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' reports/rapport-cout-chunker.md", "description": "Read report first part"}`

  ```
# Coût des règles d'attachement du chunker — O(n²) réel, cache ×12 à 160 tokens

> **Date** : 2026-11-05 · **Instantané** : [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py)
> sha256 `6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65`, commit
> `e1171032` (branche `s/v7`, arbre de travail modifié) · **Verdict** : ✅ **le O(n²) est
> confirmé** ; le cache « un chunking + un verbe de GV par analyse » divise le temps par
> **11,6 à 160 tokens** et **16,9 à 320** sur le chemin chunker seul, par **2,0 / 2,4** sur le
> chemin par défaut ; **mais** il ne rend pas la complexité strictement linéaire (le tri des GV
> par segment reste) et il ne gagne presque rien sur le corpus court.
>
> **Dispositif** : banc hors dépôt (`/tmp/bench_final.py`, sha256 `6c823a1f…`), 612 phrases de
> [`evaluer_gold.charger()`](../tools/tests/linguistique/evaluer_gold.py), phrases synthétiques
> de 20 à 1 280 tokens, variantes V1/V2/OFF ; JSON
> [`pensee-cout-chunker.json`](pensee-cout-chunker.json). Contexte : la fiche
> [`rapport-bloc-linguistique.md`](rapport-bloc-linguistique.md) décrit le bloc, pas son coût.

## 1. Ce qui était mesuré

Dans `Heuristique.analyser`, la section 5 (lig
… [6242 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '120,260p' reports/rapport-cout-chunker.md", "description": "Read report middle"}`

  ```
fois pour seulement **4/8/16/32/64** GV distincts (×72 à 160 tokens, ×136 à 320). C'est le
vrai terme quadratique du chemin par défaut.

## 4. Complexité empirique

Ajustement log-log `temps = a · N^p` sur les points mesurés (R² indiqué) :

| chemin | variante | pente 20-160 | R² | pente 20-320 | R² | pente 160-1 280 | R² |
|---|---|---:|---:|---:|---:|---:|---:|
| chunker | original | **1,742** | 0,9976 | **1,786** | 0,9982 | **1,943** | 0,9996 |
| chunker | V1 | 1,219 | 0,9965 | 1,304 | 0,9943 | — | — |
| chunker | V2 | 0,979 | 0,9963 | 1,064 | 0,9921 | **1,438** | 0,9983 |
| chunker | OFF | 1,667 | 0,9991 | 1,748 | 0,9975 | — | — |
| défaut | original | **1,266** | 0,9949 | **1,367** | 0,9923 | **1,861** | 0,9964 |
| défaut | V1 | 1,263 | 0,9955 | 1,380 | 0,9910 | — | — |
| défaut | V2 | 1,046 | 0,9966 | 1,131 | 0,9928 | **1,551** | 0,9965 |
| défaut | OFF | 1,273 | 0,9934 | 1,372 | 0,9919 | — | — |

Trois lectures :

1. **La pente 20-160 sous-estime le O(n²)**. Sur le chunker, elle vaut 1,74, mais à
   640-1 280 elle monte à **1,94**, et le doublement 160→320 coûte déjà **×3,67** (au lieu de
   ×2 pour un algorithme linéaire). Sur le défaut, la pente passe de 1,27 à **1,86**. L
… [6222 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '260,410p' reports/rapport-cout-chunker.md", "description": "Read report end"}`

  ```
def _verbe_gv(texte, g, verbes, cache_gv):
    """Le verbe d'un GV, calculé une fois par analyse. Clé valide dans un seul texte."""
    if cache_gv is None:                       # compatibilité avec les appels existants
        return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
    cle = (g["debut"], g["fin"])
    if cle not in cache_gv:
        cache_gv[cle] = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
    return cache_gv[cle]


# Dans _cible_proche (lignes 661-686), remplacer les appels des lignes 681 et 685 :
v = Heuristique._verbe_gv(texte, g, verbes, cache_gv)
# et ajouter `cache_gv=None` à la signature, après `verbes=None`.

# Dans _verbes_proches (lignes 688-704), remplacer l'appel de la ligne 701 :
v = Heuristique._verbe_gv(texte, g, verbes, cache_gv)
# et ajouter `cache_gv=None` à la signature, après `verbes=None`.
```

Points de vigilance :

- La clé `(debut, fin)` est valide **parce que `cache_gv` est créé dans `analyser`** : `texte`
  et `verbes` sont constants pendant l'appel. Ne pas promouvoir ce cache en attribut
  d'instance : `analyser` peut être appelé sur des textes différents, et un état partagé
  exposerait à des courses si u
… [7185 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib, json\np=pathlib.Path('reports/rapport-cout-chunker.md'); s=p.read_text(encoding='utf-8')\ns=s.replace(\"# Dans Heuristique.analyser, après la ligne 854 (calcul de `verbes`).\", \"# Dans Heuristique.a … [1481 caractères tronqués]`

  ```
ok
JSON_VALIDE
63:  8/16/32/64/128. Deux points de continuité à **640 et 1 280 tokens** (3 passes).
176:Les lignes 640 et 1 280 sont les points de continuité (3 passes, médianes plus bruitées) ; les autres sont à 9 passes.
216:# Dans Heuristique.analyser, après la ligne 855 (calcul de `verbes`).
313:sur le tri quand un GV recouvre le segment). Deux prototypes locaux ont été testés sur l'instantané antérieur (`d9c9d5…`), non re-mesurés ici :
358:  `e1171032`) et a changé pendant la préparation (`d9c9d5…` → `6e8430…`). Toutes les mesures
374:- **Le O(n²) est réel, et il y en a deux.** Sur le chemin
  ```

### 🤖 Assistant

⏵ Vérification finale : hash de l'instantané, fichiers livrés, JSON valide

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum tools/bloc_linguistique.py && git status --short reports/rapport-cout-chunker.md reports/pensee-cout-chunker.json tools/bloc_linguistique.py && wc -l reports/rapport-cout-chunker.md && wc -c reports/pensee-cout-chunker.json … [57 caractères tronqués]`

  ```
6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65  tools/bloc_linguistique.py
A  reports/pensee-cout-chunker.json
A  reports/rapport-cout-chunker.md
389 reports/rapport-cout-chunker.md
23561 reports/pensee-cout-chunker.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/pensee-cout-chunker.json > /dev/null && echo JSON_VALIDE && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-cout-chunker.json'))\nprint('sections:', list(d))\nprint('verdict len:', len(d[' … [262 caractères tronqués]`

  ```
JSON_VALIDE
sections: ['date', 'titre', 'verdict', 'instantane', 'dispositif', 'corpus', 'longueurs', 'complexite', 'continuite', 'profils_n160', 'controle_negatif', 'correctif_propose', 'sensibilite_base_verbe_plein', 'pistes_rejetees', 'limites']
verdict len: 771
points longueurs: 10
limites: 9
sha: 6e8430180ccc change: False
  ```

### 🤖 Assistant

⏵ Contrôle inattendu : le fichier n'apparaît plus modifié — vérification de l'historique git

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -20 && echo '--- log ---' && git log --oneline -5 && echo '--- diff HEAD file ---' && git diff HEAD --stat -- tools/bloc_linguistique.py reports/rapport-cout-chunker.md reports/pensee-cout-chunker.json && ec … [256 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/rapport.md
--- log ---
9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
e1171032 PILOTAGE — PROTOCOLE D'INTÉGRATION DES SOUS-AGENTS (REJOUER, REJETER, COMMITTER VÉRIFIÉ) ; § 9
4a65d44f PILOTAGE — VAGUE 1
… [737 caractères tronqués]
  ```

