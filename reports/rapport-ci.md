# Z1 — L'intégration continue : le workflow, la matrice et le contrôle négatif

> **Ligne de roadmap** : **B13 — la protection** (produit exploitable) · **Tâche** : **Z1** ·
> **Date** : 2026-11-16 · **Branche** : `s/v7` · **Verdict** : ✅ **la CI est verte en local** —
> **2 versions**, **5 étapes par version**, **10/10 étapes vertes**, **0 rouge**, **2/2 contrôles
> négatifs** qui cassent et arrêtent la séquence, porte produit **183/183**.
>
> **Le chiffre.** Le workflow `.github/workflows/ci.yml` déclare une matrice **Python 3.10 /
> 3.13** et cinq étapes : `pip install -e .`, `test_produit.py`, `test_tagger_api.py`,
> `porte-produit.sh`, `test_schema_produit.py`. En local, avec **3.10.20** et **3.13.16** :
> **10 étapes vertes**, **0 rouge**, **482,3 s** au total ; la porte produit rend
> `✅ porte produit verte` avec **183/183** portes d'autotest et **27/27** exemples conformes.
> Un test volontairement cassé sort en **1** (`FAILED (failures=1)`) et **l'étape suivante
> n'est pas exécutée**. La mesure principale part d'une archive `git archive HEAD` **sans
> sous-module** : la copie de secours de S restaure les deux fichiers nécessaires.
>
> **Dispositif** : [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) ·
> [`tools/verifier_ci.py`](../tools/verifier_ci.py) ·
> [`.github/ci/structures/`](../.github/ci/structures/) ·
> [`tools/verifie_structures_secours.py`](../tools/verifie_structures_secours.py) ·
> [`tools/tests/test_produit.py`](../tools/tests/test_produit.py) ·
> [`tools/tests/test_tagger_api.py`](../tools/tests/test_tagger_api.py) ·
> [`tools/porte-produit.sh`](../tools/porte-produit.sh) ·
> [`tools/tests/test_schema_produit.py`](../tools/tests/test_schema_produit.py) ·
> [`reports/rapport-ci.json`](rapport-ci.json) ·
> [`docs/produit/ci.md`](../docs/produit/ci.md).

## 1. La question

Le produit s'installe et passe ses portes sur la machine de mesure, mais **rien ne le rejoue
après un `push`**. Une régression de test peut donc dormir dans le dépôt : c'est exactement ce
qui est arrivé à `test_tagger_api.py` — le CI l'a révélé avant de tourner, parce que
`evaluer` appelle maintenant `_module_evaluation(gele=...)` et deux doubles de test avaient
encore une lambda sans argument.

Z1 demande un workflow **GitHub Actions** : la matrice **3.10 / 3.13**, l'installation
éditable, les trois tests du contrat et la porte produit, dans cet ordre ; un **contrôle
négatif** qui prouve qu'un test cassé fait échouer le job ; la doc ; la fiche et le JSON.
`act` n'étant pas installé, la preuve locale doit couvrir le YAML et les commandes.

## 2. Le workflow

| élément | valeur |
|---|---|
| fichier | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| déclencheurs | `push`, `pull_request`, `workflow_dispatch` |
| matrice | `["3.10", "3.13"]` (chaînes, pour que `3.10` ne devienne pas `3.1`) |
| runner | `ubuntu-latest`, `timeout-minutes: 30`, `fail-fast: false` |
| permissions | `contents: read` |
| concurrence | `group: ci-${{ github.workflow }}-${{ github.ref }}`, annulation du run précédent |
| checkout | `actions/checkout@v4` — **sans sous-modules** ; S restauré depuis `.github/ci/structures` |
| Python | `actions/setup-python@v5`, cache `pip` sur `pyproject.toml` |

Les cinq étapes, dans l'ordre demandé :

| # | étape | commande |
|---:|---|---|
| 1 | installation éditable | `pip install -e .` |
| 2 | smoke test produit | `python3 tools/tests/test_produit.py` |
| 3 | tagger API, transport factice | `python3 tools/tests/test_tagger_api.py` |
| 4 | porte produit | `bash tools/porte-produit.sh` |
| 5 | schéma produit | `python3 tools/tests/test_schema_produit.py` |

Le workflow ne récupère pas les sous-modules : `tools/structures` reste absent, et les tests
qui rendent les rôles (`agent`, `predicat`) et les cibles ont besoin de son **générateur S**.
L'URL versionnée du sous-module est un **chemin local** (`/home/stephane/...`), qu'un runner
hébergé ne peut pas cloner. Le workflow restaure donc, avant l'installation, une **copie de
secours** de deux fichiers — `generateur.py` et `donnees/gold-analyseur.json` — depuis
[`.github/ci/structures/`](../.github/ci/structures/). La copie est identique au sous-module au
commit `648adce` (sha256 vérifiés) ; `tools/verifie_structures_secours.py` compare les deux
quand le sous-module est présent et sort en **1** en cas de dérive. Sur un poste avec le
sous-module, l'étape de restauration est un no-op.

## 3. La preuve locale, sans `act`

`act` n'est pas installé (`which act` → rien). `tools/verifier_ci.py` :

1. charge le YAML avec **PyYAML 6.0.3** et vérifie le contrat (matrice, `runs-on`, cinq
   commandes exactes) ;
2. exécute les cinq commandes en **fail-fast**, avec `python3` du `PATH` (ou `--python`) ;
3. fabrique une copie de `test_produit.py` avec un test qui échoue, la lance, puis une étape
   témoin ; il exige que la copie sorte en **1** et que le témoin ne soit **pas** exécuté.

```bash
python3 tools/verifier_ci.py              # YAML + cinq étapes + négatif
python3 tools/verifier_ci.py --json       # le même résultat, en JSON
python3 tools/verifier_ci.py --sans-porte # plus rapide, sans la porte
```

| version | `pip install -e .` | `test_produit` | `test_tagger_api` | `porte-produit` | `test_schema_produit` | total |
|---|---:|---:|---:|---:|---:|---:|
| **3.10.20** | 0 · 2,933 s | 0 · 15,982 s (30 tests) | 0 · 7,669 s (30 tests) | 0 · 227,457 s | 0 · 1,261 s (9 tests) | **255,30 s** |
| **3.13.16** | 0 · 3,361 s | 0 · 17,393 s (30 tests) | 0 · 7,767 s (30 tests) | 0 · 196,968 s | 0 · 1,532 s (9 tests) | **227,02 s** |

Ces deux runs partent d'une **archive `git archive HEAD`** sans `tools/structures` ; le
vérificateur restaure la copie de secours (comme le workflow), puis exécute les cinq commandes.
Les mêmes cinq commandes passent aussi dans le **dépôt de travail** avec le sous-module
présent (runs du 16/11 : **10/10** étapes, **0 rouge**). Enfin, les **sept blocs `run` du YAML**
(version, restauration, installation, trois tests, porte, schéma) ont été exécutés **tels quels**
avec `bash -e` sur une archive propre : **7/7 code 0**, porte verte ; seules les étapes `uses`
(`checkout`, `setup-python`) ne sont pas simulées.

La porte produit, lue dans les deux runs : `✅ porte produit verte` — `drave 0.1.0`, JSON fr/en,
rejeu `sha256 f6355d8175a75854` deux fois, `test_produit` **30 tests**, `evaluer --strict`
**5 tests**, schéma v2+gold **26 cas**, 50 textes libres, restitutions v0/v1/v2, **27/27**
exemples, autotest **183/183**. Les **10 étapes** sont vertes, **0 rouge**.

**Ce que le CI a trouvé avant de tourner.** `test_tagger_api.py` échouait en HEAD : les deux
doubles `drave._module_evaluation = lambda: evaluateur` ne prenaient pas le mot-clé `gele`
ajouté par `evaluer`. Le correctif est **dans le test** (`lambda gele=False: evaluateur`), pas
dans le produit ; `test_evaluer_strict.py` utilisait déjà cette signature. Sans cette correction,
la matrice aurait été rouge sur les deux versions et la fiche l'aurait dit.

## 4. Le contrôle négatif

Le contrôle est exécuté **deux fois** (une par version), avec une copie temporaire de
`tools/tests/test_produit.py` enrichie d'un test qui appelle `self.fail("contrôle négatif CI
volontaire")`. La copie est supprimée dans un `finally` ; aucun fichier ne reste dans le dépôt.

| mesure | 3.10.20 | 3.13.16 |
|---|---:|---:|
| code du test cassé | **1** | **1** |
| `FAILED (failures=1)` | oui | oui |
| étape témoin exécutée | **non** | **non** |
| job arrêté | **oui** | **oui** |

La sortie contient `Ran 31 tests` (les **30** du smoke test + le test cassé) et
`AssertionError: contrôle négatif CI volontaire`. C'est la preuve demandée : un test qui casse
**sort en 1**, et la séquence **s'arrête** au lieu de continuer — le comportement d'un job
GitHub Actions dont une étape échoue.

## 5. Ce que ça prouve, ce que ça ne prouve pas

**Prouvé.** Le YAML est **valide** (PyYAML 6.0.3), la matrice et les cinq commandes sont
présentes ; les cinq commandes **passent** sur **3.10.20** et **3.13.16**, dans un venv propre
avec `pip install -e .` ; la porte produit est verte et l'autotest est **183/183** ; un test
cassé fait échouer la commande **et** arrête la séquence. La mesure principale part d'une
**archive `git archive HEAD` sans sous-module** : la copie de secours restaure S, les cinq
commandes passent, et `tools/verifie_structures_secours.py` confirme que la copie est
**identique** au sous-module (code **0**). Les **sept blocs `run`** du YAML passent **7/7** sur
cette archive ; seules les étapes `uses` ne sont pas simulées.

**Non prouvé.** Sans `act`, on ne simule **ni** l'image `ubuntu-latest`, **ni**
`actions/checkout`, **ni** `actions/setup-python`, **ni** le cache pip. Le workflow n'a pas
encore de **run GitHub** : la preuve est locale. Les actions sont épinglées par étiquette
majeure (`@v4`, `@v5`), pas par SHA. Le déclenchement suit tous les `push` ; si la branche
n'atteint pas le dépôt distant, il n'y a pas de run.

## 6. Ce qui pourrait rendre ce résultat faux

- **Le runner diffère de la machine.** `ubuntu-latest` change d'image ; les temps locaux
  (227 s et 197 s pour la porte) ne sont pas ceux du runner, et un timeout de 30 min peut
  devenir juste si l'autotest ralentit.
- **Le réseau de l'installation.** `pip install -e .` isole le build et télécharge
  `setuptools>=61` ; sans réseau ni cache, l'étape 1 échoue avant les tests. Les tests, eux,
  n'ouvrent aucune socket.
- **Les versions d'actions.** `@v4`/`@v5` sont des étiquettes mouvantes ; une mise à jour
  majeure peut changer le comportement sans qu'un commit du dépôt ne bouge.
- **La copie de secours peut dériver.** Elle est identique au sous-module au commit `648adce` ;
  si S change, `tools/verifie_structures_secours.py` le dit (code **1**) et il faut la mettre à
  jour. C'est une duplication assumée : un run GitHub testerait sinon une autre version du
  générateur.
- **Le contrôle négatif est synthétique.** Il prouve le **mécanisme** (code 1, arrêt), pas
  qu'un test réel particulier détecte une régression métier. La couverture réelle est celle
  des 30 + 30 + 9 tests et de la porte.
- **La matrice locale n'est pas GitHub.** 3.10.20 vient d'un Python géré par `uv` et 3.13.16
  du système ; ce ne sont pas les builds exacts de `setup-python`.

## 7. Les fichiers

| fichier | changement |
|---|---|
| `.github/workflows/ci.yml` | le workflow : matrice 3.10/3.13, checkout, setup-python, restauration S, cinq étapes |
| `.github/ci/structures/` | la copie de secours de S (`generateur.py`, `donnees/gold-analyseur.json`) et sa notice |
| `tools/verifier_ci.py` | parseur YAML, restauration, exécution fail-fast, contrôle négatif, sortie JSON |
| `tools/verifie_structures_secours.py` | compare la copie de secours au sous-module (code 1 si dérive) |
| `tools/tests/test_tagger_api.py` | deux doubles `_module_evaluation` acceptent `gele=False` |
| `docs/produit/ci.md` | le mode d'emploi, la preuve locale et ses limites |
| `docs/produit/README.md` | la garantie « intégration continue » et le renvoi vers la fiche |
| `docs/README.md` | l'entrée `produit/ci.md` dans la table Produit |
| `reports/rapport-ci.md` | cette fiche |
| `reports/rapport-ci.json` | les runs (archive et dépôt), les durées, le négatif, le sha256 du workflow |

**Verdict.** Z1 est **livré** : le workflow est écrit, la matrice **3.10 / 3.13** est déclarée,
les cinq commandes passent **10/10** depuis une archive **sans sous-module** (copie de secours
S restaurée) comme depuis le dépôt, la porte produit est verte (**183/183**) et le contrôle
négatif casse en **1** et arrête la séquence **2/2**. La limite est nommée : sans `act`, c'est
le YAML et les commandes qui sont prouvés, pas le runner GitHub. La prochaine preuve est un
**run vert dans l'onglet Actions** après le `push`.
