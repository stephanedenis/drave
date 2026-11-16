# T1 — l'empaquetage : `pip install -e .`, `drave` hors du dépôt, chemin historique intact

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T1** (exploitable, 1/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **empaquetage minimal livré**.
>
> **Le chiffre.** `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,
> **0** dépendance d'exécution, script console `drave = tools.drave:main`.
> `python3 -m pip install -e .` dans **`/tmp/venv-drave`** (Python **3.13.16**, pip **26.2.1**)
> rend **0** et `Successfully installed drave-0.1.0` ; `drave --version` rend **`drave 0.1.0`**
> et `drave analyser "Le chat dort."` rend **0** depuis **`/tmp`**. Le **contrôle négatif** —
> le même nom sans installation — échoue **proprement** : code **127**, `command not found`,
> **aucune** trace Python. Le chemin historique `python3 tools/drave.py` reste **vert**.
>
> **Dispositif** : [`pyproject.toml`](../pyproject.toml),
> [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py),
> [`reports/empaquetage.json`](empaquetage.json),
> [`docs/produit/README.md`](../docs/produit/README.md) § 8.10.

## 1. Ce qui est livré

Le paquet est **minimal** et sans dépendance d'exécution :

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "drave"
version = "0.1.0"
description = "Le point d'entrée produit du bloc linguistique de Drave."
requires-python = ">=3.10"
dependencies = []

[project.scripts]
drave = "tools.drave:main"

[tool.setuptools]
packages = ["tools"]
```

- **Le point d'entrée** est `tools.drave:main`, la fonction `main` du CLI historique. `tools`
  est exposé comme **namespace package** (PEP 420, sans `tools/__init__.py`) ; c'est ce que
  `packages = ["tools"]` déclare. Le script console généré importe donc exactement le même
  module que `python3 tools/drave.py`.
- **Aucune dépendance d'exécution** (`dependencies = []`). `setuptools>=61` est une dépendance
  de **construction**, installée par pip en isolation de build, pas au runtime.
- **Le code historique n'est pas modifié** : `tools/drave.py` continue de calculer sa racine
  depuis `__file__`, d'ajouter `tools/` à `sys.path` et de fonctionner lancé directement.
- **Les artefacts d'installation** sont ignorés (`*.egg-info/`, `/build/`, `/dist/` dans
  [`.gitignore`](../.gitignore)).
- **Le test** [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py) vérifie
  les métadonnées, les deux entrées et le contrôle négatif, sans créer de venv ni télécharger.
- **La doc** [`docs/produit/README.md`](../docs/produit/README.md) § 8.10 porte désormais les
  deux chemins d'installation (historique et `drave`).

**Ce qui n'est pas livré.** Aucune **wheel** n'est livrée ni publiée sur PyPI ; l'installation
est **éditable** et pointe vers le dépôt. Un wheel non éditable, construit à part pour vérifier
la portée, **échoue à l'import** (`ModuleNotFoundError: No module named 'tools.tests'`) : il
n'embarque ni `tools/tests` (dont `miroir`) ni les gold (`tools/tests/linguistique/`), et `data/`
est hors dépôt. Ce n'est pas le chemin demandé ; c'est la limite de l'installation éditable.

## 2. Le dispositif

Depuis la racine du dépôt :

```bash
python3 -m venv /tmp/venv-drave
. /tmp/venv-drave/bin/activate
python3 -m pip install -e .
cd /tmp
drave --version
drave analyser "Le chat dort."
```

- **Le venv** : `/tmp/venv-drave`, Python **3.13.16**, pip **26.2.1**.
- **La commande d'installation** : `python3 -m pip install -e .` (le `python3` du venv activé),
  depuis `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`.
- **Les contrôles** sont lancés depuis **`/tmp`**, pas depuis la racine : c'est le point de la
  tâche — la commande installée ne dépend pas du répertoire courant.
- **Le test** `python3 tools/tests/test_empaquetage.py` tourne depuis la racine, sans venv.

## 3. Les sorties observées

| contrôle | commande | cwd | code | sortie |
|---|---|---|---:|---|
| installation éditable | `python3 -m pip install -e .` | racine | **0** | `Successfully installed drave-0.1.0` |
| version installée | `drave --version` | `/tmp` | **0** | `drave 0.1.0` |
| analyse installée | `drave analyser "Le chat dort."` | `/tmp` | **0** | `GN`, `GV`, rôles `agent` / `predicat` |
| évaluation installée | `drave evaluer --json` | `/tmp` | **0** | `version: 0.1.0`, gold vivant |
| tagger sans clé | `drave analyser "Le chat dort." --tagger` | `/tmp` | **4** | `stdout` vide, « dépendance absente » |
| version historique | `python3 tools/drave.py --version` | racine | **0** | `drave 0.1.0` |
| analyse historique | `python3 tools/drave.py analyser "Le chat dort."` | racine | **0** | `GN`, `GV` |
| **sans installation** | `drave --version` | `/tmp` | **127** | `command not found` |

La sortie de `drave analyser` depuis `/tmp` :

```text
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
```

**Deux vérifications de plus, propres à l'installation.** `drave evaluer --json` depuis `/tmp`
rend `0` et lit le gold **vivant** : sous installation éditable, `RACINE` dans
`tools/drave.py` résout bien le dépôt, pas le répertoire courant. `drave analyser … --tagger`
sans clé rend **4** avec `stdout` vide : le sous-module optionnel `tools.llm.deepseek` est
importable sous l'installation éditable, et l'absence de clé reste un refus propre.

**Contrôle de portée (hors chemin demandé).** Un wheel **non éditable**, construit à part
(`pip wheel .`) puis installé dans un venv séparé, échoue à l'import de `drave --version` :
`ModuleNotFoundError: No module named 'tools.tests'`. Le wheel n'embarque ni `tools/tests`
(dont `miroir`) ni les gold. Le chemin demandé — `pip install -e .` — n'est pas affecté ;
c'est la limite de l'installation éditable, pas une régression du produit.

## 4. Le contrôle négatif

Le contrôle négatif est le **même nom de commande, sans l'installation**. On vide le `PATH` et
on retire `PYTHONPATH` / `VIRTUAL_ENV`, puis on lance depuis `/tmp` :

```bash
env -i PATH=/usr/bin:/bin HOME=/tmp bash -c 'drave --version'
# code 127
# stdout : (vide)
# stderr : bash: line 1: drave: command not found
```

**Lecture.** L'échec est **propre** : c'est un échec de **résolution** (127), pas une trace
Python, pas un import partiel, pas un code 0 trompeur. Si `drave` restait résolu sans
installation, le test positif ne prouverait rien ; ici, le contraste est net.

## 5. Le test

```bash
python3 tools/tests/test_empaquetage.py
# Ran 8 tests in 0.5 s
# OK
```

Le test fige **huit** points :

1. `pyproject.toml` existe ;
2. nom `drave`, version `0.1.0`, `requires-python >= 3.10` ;
3. aucune dépendance d'exécution, backend `setuptools.build_meta` ;
4. script console `drave = tools.drave:main` ;
5. `python3 tools/drave.py --version` → `drave 0.1.0` ;
6. `python3 tools/drave.py analyser "Le chat dort."` → `0`, avec `GN` et `Le chat` ;
7. `from tools.drave import main` depuis un **autre** répertoire ;
8. sans installation, `drave` échoue **proprement** (127, `command not found`, pas de trace).

Le test **ne crée pas de venv** et ne télécharge rien : c'est la vérification réelle
`pip install -e .` de ce rapport qui couvre l'installation ; le test couvre ce qui doit rester
vrai à chaque passe.

## 6. Ce qui pourrait rendre ce résultat faux

1. **Le plancher 3.10 n'est pas exécuté.** La mesure tourne en **3.13.16** ; `>= 3.10` est
   vérifié par la métadonnée et par l'AST (`ast.parse(..., feature_version=(3, 10))` dans la
   FAQ), pas par une exécution réelle en 3.10.
2. **Le build a besoin du réseau ou d'un cache.** pip installe `setuptools>=61` en isolation ;
   sur une machine **sans réseau ni cache**, `pip install -e .` échoue **avant** l'installation
   du paquet. Ce n'est pas une dépendance d'exécution, mais c'est une condition du dispositif.
3. **L'installation est éditable.** Un wheel non éditable, construit à part, **échoue à
   l'import** (`No module named 'tools.tests'`) : il n'embarque ni `tools/tests` ni les gold de
   `tools/tests/linguistique/`, et `data/` est hors dépôt. Le chemin demandé reste l'éditable.
4. **Le contrôle négatif est un `PATH` vidé.** Si un binaire `drave` existait dans `/usr/bin`,
   ce contrôle ne représenterait plus « sans installation ». Dans l'environnement mesuré, il
   n'y en avait pas.
5. **Le script console dépend du namespace `tools`.** Il a été vérifié depuis `/tmp` avec le
   Python du venv ; un autre interpréteur, ou un `tools` homonyme sur le `PYTHONPATH`, pourrait
   changer la résolution.

## 7. Les fichiers

- [`pyproject.toml`](../pyproject.toml) — le paquet minimal.
- [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py) — les 8 contrôles.
- [`reports/empaquetage.json`](empaquetage.json) — le relevé complet.
- [`docs/produit/README.md`](../docs/produit/README.md) § 8.10 — l'install utilisateur.
- [`reports/rapport-faq.md`](rapport-faq.md) et [`reports/faq.json`](faq.json) — la FAQ
  produit mise à jour (l'ancienne réponse « pas d'empaquetage » n'est plus vraie).
