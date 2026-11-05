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

