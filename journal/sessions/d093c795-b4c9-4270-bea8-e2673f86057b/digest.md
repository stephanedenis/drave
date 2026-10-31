# Session DSH — relecture

- identifiant : `d093c795-b4c9-4270-bea8-e2673f86057b`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 14:55:19
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A13 : tester la **seule niche non mesurée de M2** — les surfaces que M1 ne lit pas — sans modifier les modules existants.

État :
- M1 `hub.py` lit 528/528 surfaces réelles ; M2 `voies.py` lit 93,4/93,6 % sur `de`/`vers`, toujours **sous M1** ; aucun étage ne consomme M2 (B14).
- A9 note : « M2 ne pourrait servir que de secours sur des surfaces que le codec ne lit pas, cas absent de ce corpus et non mesuré ».
- Corpus : `semantique.typed_corpus.items()`, `jeux.corpus`, `jeux.corpus_multilingue`, `cerveau.sequences`.
- Base `/tmp/natif-600-512-8-align-s1`, GPU `CUDA_VISIBLE_DEVICES=0`, `/home/stephane/gpu-env/bin/python` ; tests `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` → 126 OK.

Objectif :
1. Créer `tools/cerveau/m2_secours.py` : générer des **surfaces perturbées** (typos, espaces, casse, formes libres FR/EN, notation UCI/SAN absente du corpus) à partir des items réels, en gardant le **code attendu**.
2. Mesurer : M1 exact sur ces surfaces (échec attendu), M2 `de`/`vers` exact, baseline majoritaire, hasard ; par type de perturbation.
3. Contrôle : surface originale (M1 doit réussir), surface permutée, et **code attendu absent**.
4. Écrire `/tmp/a13-m2-secours.json` et `.md` ; si M2 ne sauve rien, le dire nettement.

Contraintes :
- Crée uniquement `tools/cerveau/m2_secours.py` et `tools/cerveau/tests/test_m2_secours.py` ; ne modifie pas les modules existants, docs, reports, journal, `batterie.py`, git.
- Pas de `git add/commit/checkout`.
- GPU `CUDA_VISIBLE_DEVICES=0`. Sois autonome, timebox, autocritique. Réponds avec un résumé et les chemins.
Your parent agent id is "f0969e87-af0c-43b1-93cf-f278d9c90846". Before you finish, send your result to that agent with send_message({ agent_id: "f0969e87-af0c-43b1-93cf-f278d9c90846", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 181 fichiers / 248 JSON, 54 documents**), chemins archivés
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
9. **Les illustrations sont des SVG.** Aucun **ASCII art** : pas de `┌─┬─┐`, pas de flèches `──►`
   dans un bloc de code. Un schéma est un fichier **`.svg`** (directement, ou converti depuis
   Mermaid/PlantUML), avec `viewBox`, `<title>`, `<desc>`, liens relatifs ; il vit dans
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

⏵ Cartographie du dépôt : M1, M2 et le corpus

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls && echo '---' && ls tools/cerveau | head -80", "description": "List repo root and cerveau tools"}`

  ```
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
---
batterie.py
bus.py
episodique.py
gating.py
hub.py
__init__.py
lesion.py
memoire_travail.py
multilingue.py
neuromodulation.py
pipeline_memoire.py
pipeline.py
pipeline_semantique_m2.py
pipeline_semantique.py
predictif.py
__pycache__
restitution.py
sequences.py
sommeil.py
tests
voies.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | head -40 && echo '--- branch' && git branch --show-current && echo '--- recent' && git log --oneline -5", "description": "Check git status and recent commits"}`

  ```
--- branch
master
--- recent
0df610ec PORTES — PASSE FINALE : 49 PORTES, 47 VERTES, 2 ROUGES STRUCTURELLES ; AUCUNE RÉGRESSION
c7e5cdbe ILLUSTRATIONS — MÉTADONNÉES ACCENTUÉES DES SCHÉMAS (TITLES ET DESCRIPTIONS)
15effc93 ILLUSTRATIONS — ANNOTATION ÉTAT DANS LE PANNEAU (ANATOMIE)
95108777 DOCWATCH — v0.3.0 : NAVIGATION SPA, URL PROPRES, 69 TESTS
75bc27af ILLUSTRATIONS — SVG OBLIGATOIRE, 4 DIAGRAMMES ASCII CONVERTIS, 18 SCHÉMAS ACCESSIBLES ET VÉRIFIÉS (54 DOCS)
  ```

### 🤖 Assistant

⏵ Lecture de M1 (hub.py) et M2 (voies.py)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/cerveau/hub.py tools/cerveau/voies.py tools/cerveau/pipeline_semantique_m2.py tools/cerveau/semantique.py tools/cerveau/jeux.py 2>/dev/null; ls tools/cerveau/tests", "description": "Line counts of modules and list tests"}`

  ```
47 tools/cerveau/hub.py
  737 tools/cerveau/voies.py
  903 tools/cerveau/pipeline_semantique_m2.py
 1687 total
__init__.py
__pycache__
test_bus.py
test_episodique.py
test_gating.py
test_lesion.py
test_memoire_travail.py
test_modules.py
test_multilingue.py
test_neuromodulation.py
test_pipeline_memoire.py
test_pipeline.py
test_pipeline_semantique_m2.py
test_pipeline_semantique.py
test_predictif.py
test_restitution.py
test_sommeil.py
test_voies.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p tools/cerveau/hub.py", "description": "Read start of hub.py"}`

  ```
#!/usr/bin/env python3
"""M1 — hub sémantique typé : surface → code RSN, et retour canonique.

Le hub est la **zone de convergence** du système : il ne produit pas un vecteur
libre, il produit le code fixe de `universaux.py` (15 champs, 502 classes) en
s'appuyant sur le codec classique. Chaque perception et chaque restitution est
publiée sur le bus.
"""
from __future__ import annotations

from jeux.codecs import codec
from semantique.universaux import code_rsn, rsn_depuis_code
from .bus import Bus

FORMATS = {"morpion": "cellule", "echecs": "san", "dames": "numerique",
           "go": "gtp", "cartes": "carte"}


class Hub:
    nom = "M1-hub"

    def __init__(self, bus: Bus | None = None) -> None:
        self.bus = bus or Bus()
        self.dernier = None

    def percevoir(self, texte: str, jeu: str, contexte=None):
        try:
            lec = codec(jeu).lit(texte, niveau=4, contexte=contexte)
        except Exception as e:
            self.bus.publier("echec", {"texte": texte, "erreur": type(e).__name__}, self.nom)
            return None
        if not (lec and lec.rsn):
            self.bus.publier("echec", {"texte": texte, "erreur": "pas de RSN"}, self.nom)
            re
… [575 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de voies.py (M2)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,160p tools/cerveau/voies.py", "description": "Read start of voies.py"}`

  ```
#!/usr/bin/env python3
"""M2 — deux voies : ventrale (quoi) et dorsale (où/comment).

Un même encodeur de surface, **gelé**, alimente deux familles de têtes :

- la voie **ventrale** lit l'**action** ;
- la voie **dorsale** lit un ou plusieurs champs de lieu : `de`, `vers`,
  `point`, `chemin_0`…

Chaque tête est indépendante : on peut en léser une (logits aléatoires) sans
toucher les autres. C'est la double dissociation minimale, étendue à plusieurs
champs dorsaux.

L'entraînement est **synthétique** (`items_synth`) ; l'évaluation porte sur les
surfaces **réelles** (`items`). Le module expose aussi les ablations :

- `pool="mean"` : moyenne seule (ablation du dernier état) ;
- `pool="last"` : dernier état seul ;
- `contexte=True` : ajout du RSN de contexte, encodé par le même encodeur gelé.

Les surfaces et le contexte sont normalisés (`normaliser`) puis lus en octets,
comme dans le prototype d'origine. L'API `entrainer`/`evaluer` reste compatible
avec `batterie.py` quand aucun champ dorsal supplémentaire n'est demandé.

## Généralisation aux surfaces inédites (A5)

Deux leviers sont ajoutés, tous deux **désactivés par défaut** :

- `augmentation_*` (voir `augmenter`) : le corpus 
… [5601 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^class \\|^def \\|^    def \" tools/cerveau/voies.py", "description": "Structure of voies.py"}`

  ```
63:def _normaliser(texte: str) -> str:
68:def normaliser_coordonnees(texte: str) -> str:
95:def _san_francais(san: str) -> str:
103:class Voies(nn.Module):
108:    def __init__(self, base: nn.Module, champs_dorsaux=("de",),
138:    def dorsal(self) -> nn.Linear:
142:    def _pool(self, h: torch.Tensor, masque: torch.Tensor) -> torch.Tensor:
154:    def encode(self, ids, masque, ctx_ids=None, ctx_masque=None):
165:    def logits(self, ids, masque, ctx_ids=None, ctx_masque=None):
170:def _lot(items_, lot, seq, rng, normaliseur=None):
176:def _entrees(mor, seq, seq_ctx, contexte, contextes=None, normaliseur=None):
192:def _cibles(choix, nom, idx, device):
197:def _aleatoire_like(t: torch.Tensor, g: torch.Generator) -> torch.Tensor:
215:def _positions_echecs(n: int, graine: int):
236:def _positions_dames(n: int, graine: int):
252:def _textes_echecs(pos, coup):
298:def _textes_dames(coup):
324:def _textes_go(point: int):
342:def augmenter(champs=CHAMPS_DORSAUX, familles=("formes",), positions: int = 0,
362:    def ajoute(texte, r, code, famille, langue, contexte):
424:def entrainer(base, pas: int = 400, lot: int = 32, seq: int = 64, graine: int = 1,
546:def _stats_classes(pred, cible, n
… [404 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des API d'entraînement/évaluation de M2

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 160,240p tools/cerveau/voies.py && echo '===== 424-546' && sed -n 424,546p tools/cerveau/voies.py", "description": "Read M2 entry construction and training"}`

  ```
sc = self.base(input_ids=ctx_ids, attention_mask=ctx_masque,
                           output_hidden_states=True)
            z = torch.cat([z, self._pool(sc.hidden_states[-1], ctx_masque)], dim=-1)
        return z

    def logits(self, ids, masque, ctx_ids=None, ctx_masque=None):
        h = self.encode(ids, masque, ctx_ids, ctx_masque)
        return self.ventral(h), {nom: tete(h) for nom, tete in self.dorsaux.items()}


def _lot(items_, lot, seq, rng, normaliseur=None):
    norm = normaliseur or _normaliser
    choix = [rng.choice(items_) for _ in range(lot)]
    return pad([octets(norm(i.texte), seq) for i in choix]), choix


def _entrees(mor, seq, seq_ctx, contexte, contextes=None, normaliseur=None):
    """Prépare surfaces + contexte (facultatif) pour un lot d'items."""
    norm = normaliseur or _normaliser
    x, masque = pad([octets(norm(i.texte), seq) for i in mor])
    if not contexte:
        if contextes is not None:
            raise ValueError("contexte fourni à un modèle sans contexte")
        return x, masque, None, None
    if contextes is None:
        contextes = [i.contexte for i in mor]
    if len(contextes) != len(mor):
        raise ValueError("un contexte
… [7926 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 546,737p tools/cerveau/voies.py", "description": "Read M2 evaluation functions"}`

  ```
def _stats_classes(pred, cible, n_classes_tete: int):
    """Exactitude, hasard, majorité, rappel macro et rappel par classe."""
    n = len(cible)
    ok = sum(int(a == b) for a, b in zip(pred, cible))
    classes = collections.Counter(cible)
    par_classe = {}
    for c, cnt in sorted(classes.items(), key=lambda kv: (-kv[1], str(kv[0]))):
        bons = sum(1 for a, b in zip(pred, cible) if b == c and a == c)
        par_classe[str(c)] = {"n": cnt, "rappel": bons / cnt}
    macro = sum(v["rappel"] for v in par_classe.values()) / max(1, len(par_classe))
    return {
        "n": n,
        "exact": ok / max(1, n),
        "chance": 1.0 / n_classes_tete,
        "majorite": max(classes.values(), default=0) / max(1, n),
        "n_classes": len(classes),
        "n_classes_tete": n_classes_tete,
        "macro_rappel": macro,
        "par_classe": par_classe,
    }


def _stats(m, mor, nom, pa, pf, retour_pred: bool = False):
    pred = [VALEURS[nom][p] for p in pf]
    cible = [it.code[nom] for it in mor]
    pred_a = [VALEURS["action"][p] for p in pa]
    cible_a = [it.code["action"] for it in mor]
    res = _stats_classes(pred, cible, len(VALEURS[nom]))
    res_a = _stats_classe
… [7366 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection du checkpoint /tmp/natif-600-512-8-align-s1 et du pipeline M2

- **bash** `{"command": "ls -la /tmp/natif-600-512-8-align-s1 2>/dev/null | head -30; echo '--- find ckpt'; find /tmp/natif-600-512-8-align-s1 -maxdepth 2 -type f 2>/dev/null | head -40", "description": "Inspect checkpoint directory"}`

  ```
total 123596
drwxr-xr-x.   2 stephane stephane       100 26 oct 16:04 .
drwxrwxrwt. 797 root     root         24500 27 oct 14:55 ..
-rw-r--r--.   1 stephane stephane       974 26 oct 16:04 config.json
-rw-r--r--.   1 stephane stephane       153 26 oct 16:04 generation_config.json
-rw-------.   1 stephane stephane 126553768 26 oct 16:04 model.safetensors
--- find ckpt
/tmp/natif-600-512-8-align-s1/model.safetensors
/tmp/natif-600-512-8-align-s1/generation_config.json
/tmp/natif-600-512-8-align-s1/config.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,140p tools/cerveau/pipeline_semantique_m2.py", "description": "Read pipeline_semantique_m2 start"}`

  ```
#!/usr/bin/env python3
"""pipeline_semantique_m2.py — B13 + M2 : la chaîne M1 → M2 → M5 → M6.

Ce module est un **test d'intégration**, pas un nouveau module de perception.
Il branche les briques existantes sur un seul flux et mesure chaque étage sur
son propre banc :

- **M1** (`hub.py`) lit la surface et rend le code typé ; la mesure est le code
  exact sur les 528 surfaces réelles, avec et sans contexte ;
- **M2** (`voies.py`) relit la surface et rend les champs dorsaux `de`/`vers`
  (encodeur natif gelé, têtes linéaires) ; la mesure est l'exactitude de champ
  sur les 146 items réels qui portent `de`/`vers`, découpée en surfaces **vues**
  (forme normalisée présente dans l'entraînement synthétique) et **inédites**,
  avec les lésions ventrale/dorsale ;
- **M5** (`predictif.py`) prédit la source/la cible du pas suivant avec le
  plateau ; la mesure est l'exactitude et la surprisal sur un split 80/20 par
  partie, avec le plateau et sans lui ;
- **M6** (`gating.py`) sélectionne la tâche ; la mesure est la porte de
  confluence et la tâche de commutation ;
- **M9** (`lesion.py` pour les principes) applique les privations : M1 sans
  contexte, M2 sans voie ventrale/dorsale, M5 sans
… [4454 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche du chargement du modèle de base et du checkpoint M2

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"natif\\|checkpoint\\|safetensors\\|from_pretrained\\|AutoModel\\|charger\\|torch.load\\|Voies(\" tools/cerveau/pipeline_semantique_m2.py | head -60", "description": "Find model loading in pipeline"}`

  ```
11:  (encodeur natif gelé, têtes linéaires) ; la mesure est l'exactitude de champ
456:    config = {"checkpoint": str(base.config._name_or_path), "pas": int(pas),
464:            m = Voies(base, champs_dorsaux=CHAMPS_DORSAUX, pool="mean+last",
468:            charge = torch.load(cache, map_location=device, weights_only=False)
520:            checkpoint: str = "/tmp/natif-600-512-8-align-s1",
532:    from transformers import AutoModelForCausalLM
536:    base = AutoModelForCausalLM.from_pretrained(checkpoint,
791:            "checkpoint": checkpoint,
872:    ap.add_argument("--checkpoint", default="/tmp/natif-600-512-8-align-s1")
883:                checkpoint=args.checkpoint, cache_dir=args.cache,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 140,330p tools/cerveau/pipeline_semantique_m2.py", "description": "Read pipeline M2 model loading region"}`

  ```
# ---------------------------------------------------------------------------
def _entrees_voies(m, textes, contextes, seq: int = 64, seq_ctx: int = 192):
    x, masque = pad([octets(normaliser(t), seq) for t in textes])
    if not m.contexte:
        return x, masque, None, None
    c, cm = pad([octets(t or "", seq_ctx) for t in contextes])
    return x, masque, c, cm


def _device_de(m) -> str:
    return str(next(m.parameters()).device)


class PipelineSemantiqueM2:
    """La chaîne B13 avec M2 intercalé entre M1 et M5.

    `voies` est un modèle `Voies` déjà entraîné (ou None : la chaîne reste
    utilisable pour M1/M5/M6, M2 est alors déclaré absent). `device` sert aux
    appels M2 ; M1/M5/M6 sont des modules Python déterministes.
    """

    nom = "B13-M2-pipeline-semantique"

    def __init__(self, voies: Voies | None = None, device: str = "cuda") -> None:
        self.bus = Bus()
        self.hub = Hub(self.bus)
        self.voies = voies
        self.device = device
        self.predictif = Predictif(cible="source", ordre=1, contexte=True,
                                   melange=0.5)
        self.porte = Porte()
        self.memoire = Episodique()

    # ---- M1 -----
… [6524 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de l'entraînement M2 du pipeline (cache, graines)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 430,600p tools/cerveau/pipeline_semantique_m2.py", "description": "Read pipeline training cache region"}`

  ```
"""
    out = {}
    for jeu in sorted({s.jeu for s in test}):
        sous = [s for s in test if s.jeu == jeu]
        if not sous:
            continue
        r = modele.evaluer(sous)
        if r["n"]:
            out[jeu] = {cle: r[cle] for cle in
                        ("n", "exact", "majoritaire", "surprise",
                         "surprise_majoritaire", "gain_surprise")}
    return out


# ---------------------------------------------------------------------------
# M2 : entraînement (avec cache de têtes) et évaluation
# ---------------------------------------------------------------------------
def _cle_cache(config: dict) -> str:
    brut = json.dumps(config, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(brut.encode("utf-8")).hexdigest()[:12]


def _train_m2(base, pas: int, graine: int, contexte: bool, lot: int = 32,
              seq: int = 64, device: str = "cuda", cache_dir=None,
              reuse: bool = False):
    """Entraîne M2 sur les surfaces synthétiques, ou recharge les têtes du cache."""
    config = {"checkpoint": str(base.config._name_or_path), "pas": int(pas),
              "graine": int(graine), "contexte": bool(contexte),
             
… [6623 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 600,903p tools/cerveau/pipeline_semantique_m2.py", "description": "Read pipeline remainder"}`

  ```
plat.update({f"{champ}_{k}": v
                             for k, v in r["conditions"][champ].items()})
            par_graine[nom][graine] = plat
            if nom in predictions:
                predictions[nom][graine] = {
                    champ: r["predictions"][champ] for champ in CHAMPS_DORSAUX}
    m2 = {nom: _agg_dict(v) for nom, v in par_graine.items()}
    m2["predictions"] = predictions
    m2["entrainements"] = infos_train

    # ---- Chaîne : M1 seul, M1 remplacé par M2, M1 sans contexte -----
    # Le seul point où M2 peut agir est le champ dorsal : on compare les trois
    # lectures sur les mêmes 146 items.
    chaine = {"sans_m2": {"de": m1_avec["de"]["exact"],
                          "vers": m1_avec["vers"]["exact"]},
              "m1_sans_contexte": {"de": m1_sans["de"]["exact"],
                                   "vers": m1_sans["vers"]["exact"]},
              "avec_m2": {}, "par_graine": {}}
    # La lecture M1 sans contexte, par item et par champ : la même pour toutes
    # les graines, on la calcule une fois.
    m1_sans_ok = {}
    for champ in CHAMPS_DORSAUX:
        ok = []
        for it in items_146:
            lu = hub.percevoir(it.texte, it.j
… [13345 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du corpus typé et des champs universaux

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p tools/semantique/typed_corpus.py && echo ===== && grep -n \"class ItemType\\|def items\\|def decouper\\|def octets\" -A25 tools/semantique/typed_corpus.py | head -120", "description": "Read typed_corpus"}`

  ```
#!/usr/bin/env python3
"""typed_corpus.py — les surfaces de jeux avec leur code typé fixe.

La source est le corpus B5/B6 (112 items, formats canoniques) et le corpus
multilingue B7 (449 surfaces, 66 langues). On ne garde que les **coups** : ce
sont les items dont le code typé est complet (source, cible, matériel).
Le découpage se fait **par paire** : les surfaces d'un même sens restent du même
côté ; aucune langue d'une paire de validation n'est vue à l'entraînement.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from jeux.corpus import construire_corpus
from jeux.corpus_multilingue import construire_corpus_multilingue
from semantique.universaux import code_item, resume_contexte


@dataclass(frozen=True)
class ItemType:
    texte: str
    code: dict
    jeu: str
    nature: str
    langue: str
    paire: str
    format: str
    contexte: str = ""


def items() -> list[ItemType]:
    out = []
    vus = set()
    for corpus in (construire_corpus(), construire_corpus_multilingue()):
        for it in corpus.items:
            if it.attendu.nature != "coup":
                continue
            cle = (it.texte, it.jeu, it.paire, it.langue)
   
… [4235 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"CHAMPS\" -A40 tools/semantique/universaux.py | head -100; echo '---'; ls /tmp/a9-m2-cache 2>/dev/null | head", "description": "Read CHAMPS and check M2 cache"}`

  ```
30:CHAMPS: tuple[tuple[str, tuple], ...] = (
31-    ("jeu", JEUX),
32-    ("action", ACTIONS),
33-    ("de", (None,) + tuple(range(64))),
34-    ("vers", (None,) + tuple(range(64))),
35-    ("promotion", PROMOTIONS),
36-    ("roque", ROQUES),
37-    ("case", (None,) + tuple(range(9))),
38-    ("symbole", SYMBOLES),
39-    ("carte", (None,) + tuple(range(52))),
40-    ("taille", TAILLES),
41-    ("point", (None,) + tuple(range(81))),
42-    ("passe", PASSES),
43-    ("chemin_0", (None,) + tuple(range(64))),
44-    ("chemin_1", (None,) + tuple(range(64))),
45-    ("chemin_2", (None,) + tuple(range(64))),
46-)
47:INDEX = {nom: {val: i for i, val in enumerate(vals)} for nom, vals in CHAMPS}
48:DIM = sum(len(vals) for _, vals in CHAMPS)
49-VERSION = 1
50-
51-
52-def action(corps: dict) -> str:
53-    if corps.get("chemin"):
54-        return "prendre"
55-    if "carte" in corps:
56-        return "jouer_carte"
57-    if corps.get("passe"):
58-        return "passer"
59-    if "case" in corps:
60-        return "jouer_case"
61-    if corps.get("promotion") is not None:
62-        return "promouvoir"
63-    if "de" in corps and "vers" in corps:
64-        return "deplacer"
65-    if "poin
… [2541 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du cache M2 et du corpus synthétique

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p tools/semantique/synth_corpus.py", "description": "Read synth corpus"}`

  ```
#!/usr/bin/env python3
"""synth_corpus.py — des surfaces synthétiques multilingues, labels RSN exacts.

Le codec classique est le professeur : on génère des surfaces à partir des
règles (coups légaux, cartes, points) et des libellés multilingues, puis on
entraîne le natif à lire ces surfaces. Les surfaces **réelles** B5/B7 ne sont
jamais utilisées à l'entraînement : elles servent de test de transfert.
"""
from __future__ import annotations

from dataclasses import dataclass

from jeux.lexique_multilingue import MULTI
from jeux.regles import cartes as C
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G
from jeux.regles import morpion as M
from jeux.rsn import RSN
from semantique.typed_corpus import ItemType
from semantique.universaux import code_rsn, resume_contexte

PIECES = ("P", "N", "B", "R", "Q", "K")
LETTRES_DAMES = "abcdefgh"


def _forme(concept: str, langue: str) -> str | None:
    f = MULTI.formes(concept, langue)
    return f[0] if f else None


def _item(texte: str, r: RSN, langue: str, paire: str, fmt: str = "synthetique",
          contexte: str = "") -> ItemType:
    return ItemType(texte, code_rsn(r), r.jeu, r.natu
… [3477 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'PY'\nimport json, hashlib, os, sys\nsys.path.insert(0,'tools')\n# compute cache keys without loading model: read config name_or_path? config.json has no name\nfrom transformers import AutoConfig … [643 caractères tronqués]`

  ```
name_or_path '/tmp/natif-600-512-8-align-s1'
1 True a4b4e6d1086d True
1 False 9f40f60c0ec5 True
2 True 661fe406e6c0 True
2 False 0369dd173eb5 True
3 True a39530146036 True
3 False fd2abd86cc08 True
  ```

### 🤖 Assistant

⏵ Inventaire du corpus : jeux, formats, langues, de/vers

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'PY'\nimport sys, collections\nsys.path.insert(0,'tools')\nfrom semantique.typed_corpus import items\nits=items()\nprint('n',len(its))\nfor key in ('jeu','format','langue'):\n    print(key, colle … [546 caractères tronqués]`

  ```
n 528
jeu [('cartes', 161), ('echecs', 146), ('go', 87), ('dames', 70), ('morpion', 64)]
format [('multilingue', 449), ('cellule', 22), ('san', 12), ('numerique', 11), ('gtp', 10), ('uci', 8), ('carte', 8), ('francais', 5), ('algebrique', 2), ('sgf', 1)]
langue [('fr', 55), ('notation', 31), ('en', 15), ('de', 11), ('es', 11), ('it', 11), ('ja', 11), ('nl', 11), ('pl', 11), ('pt', 11), ('ru', 11), ('zh', 11), ('cs', 10), ('da', 10), ('eo', 10), ('et', 10), ('fa', 10), ('fi', 10), ('hu', 10), ('nb', 10), ('sl', 10), ('sr', 10), ('sv', 10), ('uk', 10), ('vi', 10), ('sq', 9), ('ar', 8), ('bn', 8), ('ca', 8), ('eu', 8), ('af', 8), ('be', 8), ('lv', 7), ('tr', 7), ('el', 6), ('ko', 6), ('sk', 6), ('th', 6), ('gl', 5), ('he', 5), ('hr', 5), ('id', 5), ('lt', 5), ('ms', 5), ('ro', 5), ('hy', 5), ('hi', 4), ('is', 4), ('ka', 4), ('mk', 4), ('nn', 4), ('ta', 4), ('ur', 4), ('az', 4), ('bs', 4), ('cy', 4), ('mn', 4), ('uz', 4), ('sw', 3), ('ga', 3), ('kk', 2), ('ne', 2), ('am', 1), ('km', 1), ('pa', 1), ('so', 1), ('zu', 1)]
de/vers 146 146
--- exemples par jeu/format
('morpion', 'cellule') fr 'A1' {'action': 'jouer_case', 'case': 0, 'symbole': 'X'}
('echecs', 'uci') notation 'e2e4' {'action
… [1045 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nfrom jeux.codecs import codec\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import code_rsn\nits=items()\nok=bad=0\nfor it i … [385 caractères tronqués]`

  ```
'point': 288, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None} {'jeu': 'go', 'action': 'poser', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 9, 'point': 48, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
ECHEC go sgf 'B[dd]' {'jeu': 'go', 'action': 'poser', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 19, 'point': 60, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None} {'jeu': 'go', 'action': 'poser', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 9, 'point': 30, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
ECHEC go gtp 'pass' {'jeu': 'go', 'action': 'passer', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 19, 'point': None, 'passe': True, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None} {'jeu': 'go', 'action': 'passer', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': N
… [48731 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du contenu des têtes M2 en cache

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'PY'\nimport torch, glob, json\nfor f in sorted(glob.glob('/tmp/a9-m2-cache/*.pt')):\n    d=torch.load(f, map_location='cpu', weights_only=False)\n    print(f.split('/')[-1], d.get('config'), lis … [87 caractères tronqués]`

  ```
m2-0369dd173eb5.pt {'checkpoint': '/tmp/natif-600-512-8-align-s1', 'pas': 300, 'graine': 2, 'contexte': False, 'champs': ['de', 'vers'], 'pool': 'mean+last', 'lot': 32, 'seq': 64} ['ventral.weight', 'ventral.bias', 'dorsaux.de.weight'] ...
m2-661fe406e6c0.pt {'checkpoint': '/tmp/natif-600-512-8-align-s1', 'pas': 300, 'graine': 2, 'contexte': True, 'champs': ['de', 'vers'], 'pool': 'mean+last', 'lot': 32, 'seq': 64} ['ventral.weight', 'ventral.bias', 'dorsaux.de.weight'] ...
m2-9f40f60c0ec5.pt {'checkpoint': '/tmp/natif-600-512-8-align-s1', 'pas': 300, 'graine': 1, 'contexte': False, 'champs': ['de', 'vers'], 'pool': 'mean+last', 'lot': 32, 'seq': 64} ['ventral.weight', 'ventral.bias', 'dorsaux.de.weight'] ...
m2-a39530146036.pt {'checkpoint': '/tmp/natif-600-512-8-align-s1', 'pas': 300, 'graine': 3, 'contexte': True, 'champs': ['de', 'vers'], 'pool': 'mean+last', 'lot': 32, 'seq': 64} ['ventral.weight', 'ventral.bias', 'dorsaux.de.weight'] ...
m2-a4b4e6d1086d.pt {'checkpoint': '/tmp/natif-600-512-8-align-s1', 'pas': 300, 'graine': 1, 'contexte': True, 'champs': ['de', 'vers'], 'pool': 'mean+last', 'lot': 32, 'seq': 64} ['ventral.weight', 'ventral.bias', 'dorsaux.de.weight'] ...
m2-
… [236 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nt=5 && sed -n 1,200p tools/cerveau/sequences.py", "description": "Read sequences module"}`

  ```
#!/usr/bin/env python3
"""sequences.py — des parties jouées par les règles, pour M3/M5/M8.

Chaque pas porte : le code typé, la surface canonique, le contexte (résumé) et
la RSN. Les parties sont déterministes pour une graine donnée.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from jeux.codecs import codec
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G
from jeux.regles import morpion as M
from jeux.rsn import RSN
from semantique.universaux import code_rsn, resume_contexte


@dataclass(frozen=True)
class Pas:
    jeu: str
    code: dict
    surface: str
    contexte: str
    rsn: RSN


@dataclass(frozen=True)
class Sequence:
    jeu: str
    pas: tuple[Pas, ...]


def _surface(jeu: str, rsn: RSN, contexte, fmt: str) -> str:
    try:
        return codec(jeu).rend(rsn, format=fmt, contexte=contexte)
    except Exception:
        return ""


def _echecs(rng: random.Random, n: int) -> Sequence:
    pos = E.Position.depart()
    pas = []
    for _ in range(n):
        coups = pos.coups_legaux()
        if not coups:
            break
        c = rng.choice(coups)
        ctx = E.rsn_depu
… [2245 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des mesures A9 existantes et des masques vu/inédit

- **bash** `{"command": "ls -la /tmp/a9-* 2>/dev/null | head -20; echo '---'; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"_masques_m2\" -A45 tools/cerveau/pipeline_semantique_m2.py | head -70", "description": "Check A9 outputs and masks"}`

  ```
-rw-r--r--. 1 stephane stephane 141502 27 oct 12:33 /tmp/a9-pipeline-m2.json
-rw-------. 1 stephane stephane  16853 27 oct 12:39 /tmp/a9-pipeline-m2.md
-rw-r--r--. 1 stephane stephane 139871 27 oct 12:30 /tmp/a9-pipeline-m2-run1.json
-rw-r--r--. 1 stephane stephane    443 27 oct 12:33 /tmp/a9-run2.log
-rw-r--r--. 1 stephane stephane    444 27 oct 12:27 /tmp/a9-run.log
-rw-r--r--. 1 stephane stephane  62205 27 oct 12:21 /tmp/a9-smoke.json

/tmp/a9-m2-cache:
total 4992
drwxr-xr-x.   2 stephane stephane     160 27 oct 12:26 .
drwxrwxrwt. 798 root     root       24520 27 oct 14:57 ..
-rw-r--r--.   1 stephane stephane  569013 27 oct 12:24 m2-0369dd173eb5.pt
-rw-r--r--.   1 stephane stephane 1134261 27 oct 12:24 m2-661fe406e6c0.pt
-rw-r--r--.   1 stephane stephane  569013 27 oct 12:23 m2-9f40f60c0ec5.pt
-rw-r--r--.   1 stephane stephane 1134261 27 oct 12:25 m2-a39530146036.pt
-rw-r--r--.   1 stephane stephane 1134261 27 oct 12:23 m2-a4b4e6d1086d.pt
-rw-r--r--.   1 stephane stephane  569013 27 oct 12:26 m2-fd2abd86cc08.pt

/tmp/a9-smoke-cache:
total 1664
---
330:def _masques_m2(items_, synth, champ):
331-    """Vu = forme normalisée présente dans l'entraînement ; couvert = classe."""
332-
… [3175 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'PY'\nimport sys, json\nsys.path.insert(0,'tools')\nfrom semantique.synth_corpus import items_synth\nfrom semantique.typed_corpus import items\nsyn=items_synth(); its=items()\nfor champ in ('de', … [520 caractères tronqués]`

  ```
de synth classes 10 [48, 49, 50, 51, 52, 53, 54, 55, 57, 62]
de reel classes 6 [8, 28, 52, 57, 60, 62] hors synth [8, 28, 60]
vers synth classes 16 [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
vers reel classes 8 [0, 19, 36, 42, 44, 45, 58, 62] hors synth [0, 19, 58, 62]
Counter({('echecs', 'ar'): 60, ('echecs', 'bn'): 60, ('echecs', 'ca'): 60, ('echecs', 'cs'): 60, ('echecs', 'da'): 60, ('echecs', 'de'): 60, ('echecs', 'el'): 60, ('echecs', 'en'): 60, ('echecs', 'eo'): 60, ('echecs', 'es'): 60, ('echecs', 'et'): 60, ('echecs', 'eu'): 60, ('echecs', 'fa'): 60, ('echecs', 'fi'): 60, ('echecs', 'fr'): 60, ('echecs', 'gl'): 60, ('echecs', 'he'): 60, ('echecs', 'hi'): 60, ('echecs', 'hr'): 60, ('echecs', 'hu'): 60, ('echecs', 'id'): 60, ('echecs', 'is'): 60, ('echecs', 'it'): 60, ('echecs', 'ja'): 60, ('echecs', 'ka'): 60, ('echecs', 'ko'): 60, ('echecs', 'lt'): 60, ('echecs', 'lv'): 60, ('echecs', 'mk'): 60, ('echecs', 'ms'): 60, ('echecs', 'nb'): 60, ('echecs', 'nl'): 60, ('echecs', 'nn'): 60, ('echecs', 'pl'): 60, ('echecs', 'pt'): 60, ('echecs', 'ro'): 60, ('echecs', 'ru'): 60, ('echecs', 'sk'): 60, ('echecs', 'sl'): 60, ('echecs', 'sq'): 60, ('echecs', 'sr'): 6
… [465 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des chiffres A9 et des prédictions par item

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'PY'\nimport json, collections\nr=json.load(open('/tmp/a9-pipeline-m2.json'))\nprint(json.dumps(r['verdict'], ensure_ascii=False, indent=1))\nprint('corpus', r['corpus'])\nprint('M1', json.dumps( … [314 caractères tronqués]`

  ```
{
 "M1_code_exact": 1.0,
 "M1_de_exact": 1.0,
 "M1_vers_exact": 1.0,
 "M2_de_exact": 0.9337899543378995,
 "M2_vers_exact": 0.9360730593607306,
 "M2_ecart_de": -0.06621004566210054,
 "M2_ecart_vers": -0.0639269406392694,
 "M2_sans_contexte_de": 0.9360730593607306,
 "M2_sans_contexte_vers": 0.9360730593607306,
 "M2_egal_M1": false,
 "M2_avec_m2_de": 0.9337899543378995,
 "M2_avec_m2_vers": 0.9360730593607306,
 "M5_source_avec_plateau": 0.18701298701298702,
 "M5_source_sans_plateau": 0.12597402597402596,
 "M5_source_surprise_avec": 2.4233681002594083,
 "M5_source_surprise_sans": 3.1116004007138085,
 "M5_source_gain_surprise": -0.6882323004544002,
 "M5_source_m1_sans_contexte": 0.2803030303030303,
 "M6_confluence": 0.9431818181818182,
 "M6_commutation": 0.9494949494949495,
 "ajoute": false,
 "phrase": "M2 n'ajoute rien à la chaîne : M1 lit 100 % des 146 items réels, M2 93–94 %, et aucun étage ne consomme M2. Remplacer M1 par M2 ne peut que dégrader le champ dorsal.",
 "nuance": "M2 est un rameau neural parallèle, pas un étage de la chaîne ; il ne pourrait servir que de secours sur des surfaces que le codec ne lit pas, cas absent de ce corpus et non mesuré ici."
}
corpus {'n_items_types'
… [1041 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse des prédictions A9 par item (vu/inédit)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'PY'\nimport json, sys, collections\nsys.path.insert(0,'tools')\nfrom semantique.typed_corpus import items\nr=json.load(open('/tmp/a9-pipeline-m2.json'))\nits=[i for i in items() if i.code.get('d … [453 caractères tronqués]`

  ```
n 146 ok 137
echecs uci notation 'e2-e4' cible 52 pred 52 vu False cov True ok 1
echecs uci notation 'e2 e4' cible 52 pred 52 vu False cov True ok 1
echecs uci notation 'e4' cible 52 pred 52 vu False cov True ok 1
echecs uci notation 'E4' cible 52 pred 52 vu False cov True ok 1
echecs francais fr 'le pion de e2 vers e4' cible 52 pred 52 vu False cov True ok 1
echecs francais en 'pawn from e2 to e4' cible 52 pred 52 vu False cov True ok 1
echecs san notation 'Nf3' cible 62 pred 62 vu False cov True ok 1
echecs san fr 'Cf3' cible 62 pred 50 vu False cov True ok 0
echecs san fr 'cavalier de g1 vers f3' cible 62 pred 62 vu False cov True ok 1
echecs san fr 'le cavalier g1 va en f3' cible 62 pred 62 vu False cov True ok 1
echecs san en 'knight from g1 to f3' cible 62 pred 62 vu False cov True ok 1
echecs san notation 'O-O' cible 60 pred 55 vu False cov False ok 0
echecs francais fr 'petit roque' cible 60 pred 49 vu False cov False ok 0
echecs san notation 'O-O-O' cible 60 pred 51 vu False cov False ok 0
echecs francais fr 'grand roque' cible 60 pred 62 vu False cov False ok 0
echecs san notation 'exd6' cible 28 pred 51 vu False cov False ok 0
echecs san notation 'a8=Q' cible 8 pred 49 v
… [336 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la normalisation et des codecs (formats UCI/SAN)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/semantique/normalisation.py && echo '===== codecs' && sed -n 1,120p tools/jeux/codecs.py", "description": "Read normalization and codecs"}`

  ```
#!/usr/bin/env python3
"""normalisation.py — la surface vers des concepts, avant le parseur natif.

Le lexique multilingue connaît les noms de jeux, les pièces, les rangs et les
enseignes dans 66 langues. On remplace ces formes par un **concept canonique**
(`[jeu.morpion]`, `[echecs.piece.N]`, `[cartes.rang.13]`) ; les coordonnées et les
nombres restent. Deux surfaces qui disent la même chose dans deux langues
deviennent alors **presque identiques** — c'est ce qui doit rendre le natif
cohérent entre langues.
"""
from __future__ import annotations

from jeux.lexique import normalise_forme
from jeux.lexique_multilingue import MULTI

DOMAINES = ("jeu.nom", "echecs.piece", "cartes.rang", "cartes.couleur",
            "go.passe", "commun.couleur")


def normaliser(texte: str) -> str:
    t = normalise_forme(texte)
    if not t:
        return t
    tokens = t.split()
    trouves = []
    for domaine in DOMAINES:
        trouves.extend(MULTI.cherche(domaine, texte))
    jeux = {m.concept for m in trouves if m.domaine == "jeu.nom"}
    # Une enseigne de carte tranche l'ambiguïté « roi » (pièce d'échecs vs rang).
    cartes = any(m.domaine == "cartes.couleur" for m in trouves) or "jeu.cart
… [1031 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def rend\\|uci\\|san\\|format\" tools/jeux/codecs.py | head -80", "description": "Find codec rendering formats"}`

  ```
[stderr]
grep: tools/jeux/codecs.py: No such file or directory
  ```

### 🤖 Assistant

⏵ Localisation du module codecs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find . -name 'codecs*' -not -path '*/__pycache__/*' | head; echo '---'; PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"import jeux.codecs as c; print(c.__file__)\"", "description": "Find codecs module file"}`

  ```
./tools/jeux/codecs
---
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/jeux/codecs/__init__.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/semantique/normalisation.py | head -5; echo '---'; grep -rn \"def normalise_forme\" -A20 tools/jeux/lexique.py | head -40", "description": "Check normalise_forme lowercase behavior"}`

  ```
#!/usr/bin/env python3
"""normalisation.py — la surface vers des concepts, avant le parseur natif.

Le lexique multilingue connaît les noms de jeux, les pièces, les rangs et les
enseignes dans 66 langues. On remplace ces formes par un **concept canonique**
---
107:def normalise_forme(texte: str) -> str:
108-    """Forme de comparaison d'un libellé multilingue (même règle que le constructeur).
109-
110-    NFKC, casse pliée, diacritiques **optionnels** retirés (latin, grec,
111-    cyrillique, arabe, hébreu), diacritiques **constitutifs** gardés (indic,
112-    thaï), parenthèses de désambiguïsation retirées (« 馬 (國際象棋) » → « 馬 »),
113-    espaces normalisés, ponctuation de bord ôtée.
114-    """
115-    t = unicodedata.normalize("NFD", normalise(texte).casefold())
116-    t = sans_diacritiques(t)
117-    t = re.sub(r"\s*\([^)]*\)\s*$", "", t)
118-    t = t.replace("\u2019", "'").replace("`", "'")
119-    t = re.sub(r"\s+", " ", t).strip(" .,;:!?«»\"'")
120-    return unicodedata.normalize("NFC", t)
121-
122-
123-def unites(texte: str) -> list[str]:
124-    """Découpe une surface en unités : mots, nombres, symboles, ponctuation.
125-
126-    Le découpage est **manuel** et non une re
… [108 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de l'API des codecs (formats, rend)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,160p tools/jeux/codecs/__init__.py", "description": "Read codecs init"}`

  ```
"""Les codecs de jeux : un fichier par jeu, un seul contrat (`base.Codec`)."""
from .base import Arbre, Codec, Lecture, codec, detecte_jeu, lit, rend, tous_les_codecs  # noqa: F401
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def rend\\|uci\\|format=\\|\\\"san\\\"\\|'san'\" tools/jeux/codecs/*.py | head -80", "description": "Find rendering implementation"}`

  ```
tools/jeux/codecs/base.py:115:    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
tools/jeux/codecs/base.py:146:                       format=format, langue=lang)
tools/jeux/codecs/base.py:150:        return Annotation(langue=lecture.langue, format=lecture.format,
tools/jeux/codecs/base.py:165:        rsn = rsn.avec_annotation(langue=lecture.langue, format=lecture.format,
tools/jeux/codecs/base.py:219:def rend(rsn: RSN, format: str = "canonique", langue: str = "fr",
tools/jeux/codecs/base.py:221:    return codec(rsn.jeu).rend(rsn, format=format, langue=langue, contexte=contexte)
tools/jeux/codecs/cartes.py:257:    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
tools/jeux/codecs/dames.py:217:    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
tools/jeux/codecs/echecs.py:254:    formats = ("fen", "diagramme", "san", "uci", "francais", "pgn", "canonique")
tools/jeux/codecs/echecs.py:321:                c, cands, amb = pos.parse_uci(texte)
tools/jeux/codecs/echecs.py:323:                    lec.format = "uci"
tools/jeux/codecs/echecs.py:324:                    return self.reussi(lec, E.action_depuis_coup(c), "uci"
… [1290 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du rendu SAN/UCI du codec échecs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 300,360p tools/jeux/codecs/echecs.py && echo '===== rend 409-455' && sed -n 409,455p tools/jeux/codecs/echecs.py", "description": "Read echecs parse/render"}`

  ```
pos = E.position_depuis_rsn(contexte, valide=True)
            except Exception as e:
                return self.echoue(lec, f"position de contexte invalide : {e}")

        # 4a. roque en toutes lettres (niveau 2) — une forme fermée, pas une phrase
        if niveau >= 2 and re.search(r"\b(petit roque|grand roque|roque court|roque long|"
                                     r"roque cote|kingside|queenside|castle|o o)\b",
                                     naturel(texte)):
            c, cands, amb, _ = _lit_phrase(texte, pos, niveau, langue)
            if c is not None:
                lec.format = "francais"
                return self.reussi(lec, E.action_depuis_coup(c), "francais", 0.95, amb)
            if cands:
                lec.candidats = [E.action_depuis_coup(x) for x in cands]
                return self.echoue(lec, "coup ambigu : " + " ; ".join(amb))
            return self.echoue(lec, "roque impossible dans cette position")

        # 4b. UCI / LAN — la forme canonique d'un coup, sans position
        m = _RE_UCI.fullmatch(texte)
        if m:
            if pos is not None:
                c, cands, amb = pos.parse_uci(texte)
                if c is not None:
  
… [4310 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def rsn_depuis_position\\|def action_depuis_coup\\|def coup_depuis\\|class Position\" tools/jeux/regles/echecs.py | head -20 && grep -n \"def rsn_depuis_resume\\|def rsn\" -n tools/jeux/regles/echecs.py | head", "descriptio … [29 caractères tronqués]`

  ```
183:class Position:
794:def rsn_depuis_position(pos: Position, annotation: Annotation | None = None) -> RSN:
816:def action_depuis_coup(coup: Coup, annotation: Annotation | None = None) -> RSN:
827:def coup_depuis_action(rsn: RSN, pos: Position | None = None) -> Coup:
794:def rsn_depuis_position(pos: Position, annotation: Annotation | None = None) -> RSN:
855:def rsn_partie(depart: RSN, coups: list[Coup], annotation: Annotation | None = None) -> RSN:
  ```

### 🤖 Assistant

⏵ Inspection du corpus source (contexte RSN, items)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p tools/jeux/corpus.py", "description": "Read jeux.corpus"}`

  ```
#!/usr/bin/env python3
"""corpus.py — le corpus de surfaces, avec leur sens attendu.

Un item est un triplet (surface, contexte, RSN attendue). Le corpus est
**construit par le code**, pas stocké dans `data/` : il est reproductible, et on
peut le régénérer après chaque correction. Il couvre les cinq jeux, deux
langues, plusieurs notations, et des paires d'expressions **équivalentes** (pour
l'invariance) et **non équivalentes** (pour le contrôle de collision).

Règle : l'attendu est calculé par les **règles**, jamais recopié à la main. Si
le codec et les règles se contredisent, le corpus le dit — c'est un test, pas
une illustration.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .regles import cartes as C
from .regles import dames as D
from .regles import echecs as E
from .regles import go as G
from .regles import morpion as M
from .rsn import RSN


@dataclass(frozen=True)
class Item:
    jeu: str
    texte: str
    nature: str
    attendu: RSN
    contexte: RSN | None = None
    format: str = ""
    langue: str = ""
    groupe: str = ""
    paire: str | None = None
    contre: str | None = None  # paire NÉGATIVE : même `contre`, sens différen
… [4457 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.typed_corpus import ite … [1057 caractères tronqués]`

  ```
manquants 0
<class 'jeux.rsn.RSN'> RSN(jeu='morpion', nature='etat', corps={'cases': [None, None, None, None, None, None, None, None, None], 'taille': 3, 'trait': 'X'}, annotation=Annotation(langue='notation', format='canonique', confiance=1.0, ambiguites=(), surface='', niveau=4))
M1 avec contexte source 528 / 528
de/vers 146 ctx non null 146
jeux {'echecs'} formats ['francais', 'multilingue', 'san', 'uci']
  ```

### 🤖 Assistant

⏵ Vérification de l'environnement de tests (python3 vs gpu-env)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"import torch; print(torch.__version__)\" 2>&1 | head -2; python3 -c \"import numpy; print(numpy.__version__)\" 2>&1 | head -2; echo '--- gpu'; /home/stephane/gpu-env/bin/python -c \"import torch; print(torch.__version__, … [106 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
2.5.3
--- gpu
2.11.0+cu130 True Quadro RTX 5000
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 300 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -5", "description": "Run baseline test suite"}`

  ```
...............................................................................sssssssssss............................ssssssss
----------------------------------------------------------------------
Ran 126 tests in 11.496s

OK (skipped=19)
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point et écris /tmp/a13-m2-secours.json/.md dès qu'une mesure existe, même partielle ; termine ensuite.

### 🤖 Assistant

⏵ Inventaire des codes distincts des 146 items (roque, prise, promotion)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'PY'\nimport sys, collections\nsys.path.insert(0,'tools')\nfrom semantique.typed_corpus import items\nits=[i for i in items() if i.code.get('de') is not None]\nseen={}\nfor i in its:\n    k=(i.co … [364 caractères tronqués]`

  ```
(8, 0, 'q', None, 'promouvoir') 2 [('san', 'notation', 'a8=Q'), ('uci', 'notation', 'a7a8q')]
(28, 19, None, None, 'deplacer') 1 [('san', 'notation', 'exd6')]
(52, 36, None, None, 'deplacer') 69 [('uci', 'notation', 'e2e4'), ('uci', 'notation', 'e2-e4'), ('uci', 'notation', 'e2 e4'), ('uci', 'notation', 'e4')]
(52, 44, None, None, 'deplacer') 1 [('uci', 'notation', 'e2e3')]
(57, 42, None, None, 'deplacer') 1 [('san', 'notation', 'Nc3')]
(60, 58, None, 'Q', 'deplacer') 2 [('san', 'notation', 'O-O-O'), ('francais', 'fr', 'grand roque')]
(60, 62, None, 'K', 'deplacer') 2 [('san', 'notation', 'O-O'), ('francais', 'fr', 'petit roque')]
(62, 45, None, None, 'deplacer') 68 [('san', 'notation', 'Nf3'), ('san', 'fr', 'Cf3'), ('san', 'notation', 'g1f3'), ('san', 'fr', 'cavalier de g1 vers f3')]
formats par valeur Counter({(52, 36): 69, (62, 45): 68, (60, 62): 2, (60, 58): 2, (8, 0): 2, (28, 19): 1, (52, 44): 1, (57, 42): 1})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import rsn_depuis_code\nfrom jeux.codecs import codec\nits=[i for i in items()  … [967 caractères tronqués]`

  ```
'Nf3' 62 45 None None -> san 'Nf3' uci 'g1f3' fr 'g1f3'
'O-O' 60 62 None K -> san 'O-O' uci 'e1g1' fr 'petit roque'
'exd6' 28 19 None None -> san 'exd6' uci 'e5d6' fr 'e5d6'
'a8=Q' 8 0 q None -> san 'a8=Q+' uci 'a7a8q' fr 'a7a8q'
'e2e4' 52 36 None None -> san 'e4' uci 'e2e4' fr 'e2e4'
  ```

### 🤖 Assistant

⏵ Écriture de `tools/cerveau/m2_secours.py`

