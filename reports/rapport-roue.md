# U2 — la roue : `drave-0.1.0-py3-none-any.whl`, installée hors du dépôt, les gold dedans

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **U2** (suite de T1) ·
> **Date** : 2026-11-16 · **Verdict** : ✅ **la roue est autonome ; une roue sans gold échoue proprement**.
>
> **Le chiffre.** `python3 -m pip wheel . --no-deps --no-build-isolation -w dist` rend
> **`drave-0.1.0-py3-none-any.whl`** : **1 727 201 octets**, **422 entrées**,
> sha256 `d980c4706f575e061faa9611aca4c42c024c1147b654004f724694914a99dbce`. Installée
> dans un venv **propre** depuis la roue (pas le dépôt), elle rend `drave 0.1.0` (code 0),
> `drave analyser "Le chat dort."` (code 0, `rôle=agent`) et `drave evaluer --json` (code 0,
> gold **612** phrases, POS **0,8625**, F1 **0,7902**, attachement exact **0,9958**) depuis
> **`/tmp`**. Les JSON `analyser` et `evaluer` sont **identiques au bit près** à ceux du dépôt.
> **Contrôle négatif** : la même roue **amputée des cinq `gold*.json`** s'installe encore et
> analyse encore, mais `drave evaluer` sort en **4**, `stdout` vide, et nomme les fichiers
> manquants. La mesure ne ment pas : sans référence, elle refuse.
>
> **Dispositif** : [`pyproject.toml`](../pyproject.toml), [`tools/drave.py`](../tools/drave.py),
> [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py),
> [`reports/roue.json`](roue.json), [`docs/produit/README.md`](../docs/produit/README.md) § 8.10.

## 1. La décision : les gold voyagent avec la roue

Une roue **installable** doit pouvoir **mesurer**. Les gold ne sont donc pas laissés au dépôt :
les cinq fichiers `gold*.json` sont des **données du paquet** (`package-data`), et la roue
embarque aussi `evaluer_gold.py`, `miroir.py`, `tools/structures/generateur.py` et
`tools/llm/deepseek.py`. `evaluer`, `evaluer --gold`, `evaluer --reel` et `analyser` rendent
depuis `/tmp` exactement ce qu'ils rendent depuis la racine.

La **roue sans gold doit échouer** — et elle échoue. C'est le contrôle négatif : si `evaluer`
rendait 0 sans les données, le chiffre positif ne prouverait rien. Le code **4** est celui des
dépendances absentes dans la CLI ; `stdout` reste vide ; le message nomme `gold.json`,
`gold_reel.json`, `gold_synthetique.json` (ou `gold_gele.json` avec `--gold`) et dit quoi faire :
réinstaller la roue **complète**, ou mesurer depuis le dépôt. `--gold` sélectionne le gold
**gelé** ; il **ne remplace pas** un gold absent, et son aide le dit.

## 2. Le dispositif

Depuis la racine, avec l'**arbre propre** (l'helper non suivi `gold_reel_50.py` a été écarté du
build) :

```bash
rm -rf build drave.egg-info dist && mkdir -p dist
python3 -m pip wheel . --no-deps --no-build-isolation -w dist
# dist/drave-0.1.0-py3-none-any.whl

python3 -m venv /tmp/venv-drave-roue
/tmp/venv-drave-roue/bin/python -m pip install --no-index --no-deps \
  --no-cache-dir dist/drave-0.1.0-py3-none-any.whl
cd /tmp
/tmp/venv-drave-roue/bin/drave --version
/tmp/venv-drave-roue/bin/drave analyser "Le chat dort."
/tmp/venv-drave-roue/bin/drave evaluer --json
```

- **Python** 3.13.16 ; pip du venv **26.2.1** (pip système 26.2.2) ; **setuptools** 84.0.0.
- **`--no-build-isolation`** : le build utilise le setuptools déjà installé ; avec l'isolation,
  pip doit installer `setuptools>=61`, donc réseau ou cache.
- **`--no-index --no-deps --no-cache-dir`** : l'installation ne peut venir que du fichier, et
  aucune dépendance n'est résolue (le projet n'en a aucune).
- **`HOME=/tmp/drave-home`** et variables `*_API_KEY` / `*_KEY_FILE` retirées : le tagger sans
  clé est reproductible.
- **`cd /tmp`** pour tous les contrôles : la commande installée ne dépend pas du répertoire.

## 3. Ce que la roue contient

| famille | contenu | preuve |
|---|---|---|
| le CLI | `tools/drave.py` + les modules racine de `tools/` | `drave --version` → `drave 0.1.0` |
| la mesure | `tools/tests/linguistique/{evaluer_gold,miroir}.py` | `drave evaluer --json` → 0 |
| les **gold** | `gold.json`, `gold_gele.json`, `gold_reel.json`, `gold_restitution_v2.json`, `gold_synthetique.json` | gold 612 / gelé 602 / réel 452 |
| le générateur S | `tools/structures/generateur.py` (sous-module **648adce3**) | `rôle=agent` sur « Le chat dort. », comme le dépôt |
| le tagger (option) | `tools/llm/deepseek.py` | sans clé : code **4**, `stdout` vide |
| hors roue | `data/`, `models/`, les scripts `tools/tests/test_*.py` de la racine | — |

Le point **S** est un écart trouvé pendant U2 : la roue construite avec la seule liste
`packages = ["tools"]` échouait d'abord à l'import (`No module named 'tools.tests'`), puis,
une fois `tools.tests.linguistique` ajouté, elle **analysait** mais rendait `rôle=objet` au lieu
de `rôle=agent` : `_syntagmes_s` importe `generateur` depuis `tools/structures`, absent de la
roue. `tools.structures` est donc embarqué ; l'analyse de la roue est **identique** au dépôt,
pas seulement « fonctionnelle ».

## 4. Les sorties observées (roue complète)

| contrôle | commande | cwd | code | sortie |
|---|---|---|---:|---|
| version | `drave --version` | `/tmp` | **0** | `drave 0.1.0` |
| analyse fr | `drave analyser "Le chat dort."` | `/tmp` | **0** | `GN`, `GV`, `rôle=agent`, `rôle=predicat` |
| analyse en | `drave analyser "The cat sleeps on the roof." --langue en` | `/tmp` | **0** | `GN`, `GP`, `sleeps/VERB` |
| évaluation | `drave evaluer --json` | `/tmp` | **0** | 612 phrases · POS 0,8625 · F1 0,7902 · exact 0,9958 |
| gold gelé | `drave evaluer --gold --json` | `/tmp` | **0** | 602 phrases · POS 0,8625 · F1 0,7882 · exact 0,9791 |
| base réelle | `drave evaluer --reel --json` | `/tmp` | **0** | 452 phrases · POS 0,8891 · F1 0,7906 · exact 0,9946 |
| restitution | `drave restituer "Le chat dort."` | `/tmp` | **0** | surface exacte 1,0000 · miroir 0,0000 |
| tagger sans clé | `drave analyser "Le chat dort." --tagger` | `/tmp` | **4** | `stdout` vide · « dépendance absente » |

**Identité avec le dépôt.** `cmp` est vide entre le JSON `analyser` de la roue et celui de
`python3 tools/drave.py analyser … --json` (sha256 `586830df…c90c36`) ; idem pour `evaluer` et
`evaluer --gold`. C'est la preuve que la roue exécute **le même code et les mêmes données**,
pas une copie approximative.

## 5. Le contrôle négatif : la roue sans les gold

On dérive la roue officielle en retirant de l'archive les cinq `gold*.json` **et leurs lignes de
`RECORD`**, puis on l'installe dans un second venv propre :

```text
/tmp/drave-amputee/drave-0.1.0-py3-none-any.whl
1 625 372 octets · sha256 969ccd335beb11cfcee99efd434486849007089bb79f4ba712e4ae2e8948f76a
```

| contrôle | code | lecture |
|---|---:|---|
| installation | **0** | `Successfully installed drave-0.1.0` |
| `drave --version` | **0** | `drave 0.1.0` |
| `drave analyser "Le chat dort."` | **0** | **identique** à la roue complète (`cmp` vide) |
| `drave evaluer --json` | **4** | `stdout` **0 octet** ; message « gold absent de cette installation : gold.json, gold_reel.json, gold_synthetique.json » |
| `drave evaluer --gold --json` | **4** | `stdout` **0 octet** ; message « gold absent de cette installation : gold_gele.json » |

**Lecture.** L'**installation** et l'**analyse** ne dépendent pas des gold ; la **mesure**, si.
La roue complète rend 0 et des chiffres ; l'amputée rend 4 et un message qui dit quoi faire. Le
contraste est net : aucun code 0 trompeur, aucune trace Python, aucun `stdout` partiel. C'est le
contrôle qui manquait à T1, où le wheel non éditable échouait à l'import avant même d'analyser.

## 6. Le test

```bash
python3 tools/tests/test_empaquetage.py   # Ran 11 tests — OK
python3 tools/tests/test_produit.py       # Ran 30 tests — OK
python3 tools/tests/test_restitution.py   # 22 tests — OK
python3 tools/tests/test_restitution_v2.py # 17 tests — OK
python3 tools/tests/test_restitution_v3.py # 29 tests — OK
```

`test_empaquetage.py` fige désormais **onze** points : les métadonnées, les **sous-paquets** de
la roue (`tools.tests.linguistique`, `tools.structures`, `tools.llm`), les **cinq gold** en
`package-data`, les deux entrées, le contrôle négatif « sans installation » (127) et le contrôle
négatif « sans gold » (4, `stdout` vide, message qui nomme `--gold`). Le test ne crée pas de venv
et ne télécharge rien : la roue réelle est le dispositif de ce rapport, pas du test unitaire.

## 7. Ce qui pourrait rendre ce résultat faux

1. **La roue n'est pas un build isolé.** Le build mesuré utilise `--no-build-isolation` et
   setuptools 84.0.0 ; un build isolé dépend du réseau ou d'un cache pour `setuptools>=61`.
2. **Le contrôle négatif est une roue dérivée**, pas un build où `package-data` est vide. Les
   fichiers sont retirés de l'archive et de `RECORD` ; le chemin « données absentes » est le
   même, mais le build sans gold n'a pas été rejoué. Le résultat prouve le **chemin d'échec**,
   pas l'absence de warning de build.
3. **Le plancher 3.10 n'est pas exécuté.** La mesure tourne en 3.13.16 ; `>=3.10` est vérifié
   par la métadonnée, pas par une exécution en 3.10.
4. **La roue dépend du sous-module `tools/structures`** (commit `648adce3`). Sans lui, elle se
   construit sans `generateur` et l'analyse retombe sur l'heuristique : sur « Le chat dort. »,
   `rôle=objet` au lieu de `rôle=agent`. Le build d'un clone public sans sous-module est donc
   **dégradé**, comme T3 l'avait documenté ; la roue mesurée ici a le sous-module.
5. **La roue n'est pas minimale.** `packages = ["tools"]` embarque tous les modules racine de
   `tools/` (370 fichiers `.py`), pas seulement les sept du CLI. C'est assumé : le point de U2
   est l'autonomie, pas la taille. Un découpage en paquet `drave` propre serait un autre
   chantier.
6. **Le hash est celui d'un arbre précis.** Il dépend des fichiers suivis et des sorties du
   sous-module ; il vaut pour ce dispositif, pas comme identité publiée. La roue n'est ni signée
   ni sur PyPI ; `dist/` est ignoré par git.
7. **Le tagger n'est mesuré que sans clé.** Le seul contrôle est le refus propre (code 4). Le
   cache par défaut de `tools.llm.deepseek` pointe sous `site-packages/data`, non testé en
   écriture ; un tagger réel demanderait une clé, du réseau et un cache accessible.
8. **L'identité avec le dépôt n'est pas une preuve de correction.** Elle prouve que la roue
   n'ajoute ni ne retire de comportement ; elle ne dit pas que les chiffres sont bons — c'est le
   rôle des fiches de mesure et de leurs contrôles.

## 8. Les fichiers

- [`pyproject.toml`](../pyproject.toml) — sous-paquets et `package-data` des gold.
- [`tools/drave.py`](../tools/drave.py) — `GoldAbsent`, vérification des gold, code 4, aide de `--gold`.
- [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py) — les 11 contrôles.
- [`reports/roue.json`](roue.json) — le relevé complet (build, installation, sorties, contrôle négatif, limites).
- [`docs/produit/README.md`](../docs/produit/README.md) § 8.10 — les trois chemins d'installation.
- [`reports/rapport-empaquetage.md`](rapport-empaquetage.md) — T1, avec le renvoi vers U2.
