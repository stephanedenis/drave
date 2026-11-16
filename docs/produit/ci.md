# L'intégration continue — le workflow et sa preuve locale

> **Ce que ce document est.** La **protection** du produit : le workflow GitHub Actions qui
> rejoue, à chaque `push` et à chaque `pull request`, l'installation éditable, les trois tests
> du contrat et la **porte produit**, sur **Python 3.10 et 3.13**. Il dit aussi comment vérifier
> le workflow **sans `act`**, et ce que cette vérification ne prouve pas.
>
> **Vérifié le 2026-11-16** sur `s/v7` : YAML chargé par PyYAML **6.0.3**, **2 × 5 étapes
> vertes** depuis une **archive sans sous-module** (copie de secours S) et depuis le dépôt,
> porte produit **183/183**, et un test volontairement cassé qui sort en **1** et **arrête** la
> séquence. `act` n'est pas installé sur la machine de mesure : la preuve est locale, pas une
> exécution GitHub.
>
> **Fiche** : [`reports/rapport-ci.md`](../../reports/rapport-ci.md) ·
> **JSON** : [`reports/rapport-ci.json`](../../reports/rapport-ci.json) ·
> **Workflow** : [`../../.github/workflows/ci.yml`](../../.github/workflows/ci.yml) ·
> **Vérificateur** : [`../../tools/verifier_ci.py`](../../tools/verifier_ci.py).

## 1. Ce que le workflow lance

| étape | commande | ce qu'elle verrouille |
|---|---|---|
| installation | `pip install -e .` | le paquet s'installe en éditable, sans dépendance externe |
| smoke test | `python3 tools/tests/test_produit.py` | version, aide, `analyser` fr/en, JSON, rejeu, `evaluer`, `--duree`, codes |
| tagger | `python3 tools/tests/test_tagger_api.py` | cascade, cache, clé absente/refusée, réseau coupé, mode `auto`, **sans réseau** |
| porte produit | `bash tools/porte-produit.sh` | le contrat de bout en bout, la restitution, les exemples et l'autotest |
| schéma | `python3 tools/tests/test_schema_produit.py` | schéma v2, rétro-compatibilité v1, refus, entrées hostiles |

La **matrice** est `["3.10", "3.13"]` : les deux versions sont des chaînes dans le YAML, pour
qu'un parseur ne lise pas `3.10` comme le flottant `3.1`. `fail-fast: false` garde les deux
jambes lisibles même si l'une casse ; chaque jambe a un `timeout-minutes: 30`.

Le workflow se déclenche sur `push`, `pull_request` et `workflow_dispatch` ; il a
`permissions: contents: read` et annule le run précédent de la même référence
(`concurrency`). `actions/checkout@v4` ne récupère **pas** les sous-modules : le produit et ses
tests n'en ont pas besoin **si le générateur S est fourni autrement**. Or `tools/structures` est
un sous-module dont l'URL versionnée est un **chemin local** (`/home/stephane/...`) : un runner
hébergé ne peut pas le cloner. Le workflow restaure donc, **avant l'installation**, les deux
fichiers dont le produit a besoin — `generateur.py` et `donnees/gold-analyseur.json` — depuis
[`.github/ci/structures/`](../../.github/ci/structures/). C'est une **copie de secours**
assumée, identique au sous-module au commit `648adce` ; elle n'est utilisée que si
`tools/structures/generateur.py` manque. Sur un poste avec le sous-module, l'étape est un
no-op. `tools/verifie_structures_secours.py` compare les deux copies quand le sous-module est
présent (code **1** si dérive).

## 2. Vérifier sans `act`

`act` n'est pas installé sur la machine de mesure. `tools/verifier_ci.py` fait trois choses :

1. il **charge** le YAML avec PyYAML et vérifie le contrat (matrice, `runs-on`, cinq commandes) ;
2. il **exécute** les commandes dans l'ordre, en **fail-fast**, et relève code et durée ;
3. il **casse** un test : une copie de `tools/tests/test_produit.py` avec un test qui échoue est
   lancée, puis une étape témoin est proposée. Le script exige que la copie sorte en **1** et que
   l'étape témoin ne soit **pas** exécutée — c'est le comportement d'un job qui échoue.

```bash
python3 -m pip install pyyaml          # une fois, si le parseur manque
python3 tools/verifier_ci.py           # YAML + cinq étapes + contrôle négatif
python3 tools/verifier_ci.py --json    # le même résultat, en JSON
python3 tools/verifier_ci.py --sans-porte
```

Le script choisit `python3` dans le `PATH`. Pour mesurer une version précise, on active son
environnement (ou on passe `--python /chemin/venv/bin/python3`) : c'est ainsi que **3.10.20** et
**3.13.16** ont été mesurés séparément. Il **restaure aussi** la copie de secours de S si
`tools/structures/generateur.py` manque, comme le fait le workflow ; c'est ce qui permet de le
lancer depuis une archive `git archive` sans sous-module.

**Ce que la preuve donne.** Les deux jambes passent les cinq étapes, la porte produit rend
`✅ porte produit verte` et **183/183** portes d'autotest. Le contrôle négatif rend **1**, avec
`FAILED (failures=1)` et `AssertionError: contrôle négatif CI volontaire` ; l'étape témoin
n'est pas lancée. Le fichier temporaire est supprimé dans un `finally`. Les **sept blocs `run`**
du YAML (version, restauration, installation, trois tests, porte, schéma) ont aussi été
exécutés **tels quels** avec `bash -e` sur une archive propre : **7/7 code 0** ; seules les
étapes `uses` (`checkout`, `setup-python`) ne sont pas simulées.

## 3. Ce que ça ne prouve pas

- **Pas d'exécution GitHub.** Sans `act`, on ne teste ni l'image `ubuntu-latest`, ni
  `actions/checkout`, ni `actions/setup-python`, ni le cache pip. On prouve le YAML et les
  commandes, pas le runner.
- **Pas de réseau dans les tests.** `test_tagger_api.py` injecte ses transports ; le workflow
  n'a donc pas besoin de clé DeepSeek. L'installation, elle, utilise le réseau pour l'isolation
  de build (`setuptools>=61`), comme sur GitHub.
- **Pas une garantie de branche.** Le workflow suit tous les `push` ; si le dépôt distant ne
  reçoit pas la branche `s/v7`, le workflow ne s'exécute pas. La preuve locale ne remplace pas
  un run vert dans l'onglet Actions.
- **Les versions d'actions peuvent bouger.** `@v4` et `@v5` sont des étiquettes mouvantes ; un
  épinglage par SHA est plus strict, il n'est pas fait ici.
- **La copie de secours de S peut dériver.** Elle est identique au sous-module au commit
  `648adce` ; si S change, `python3 tools/verifie_structures_secours.py` le dit (code **1**), et
  il faut la mettre à jour. C'est une duplication assumée, pas une seconde source.

## 4. Après un échec

Un job rouge se lit par l'étape et la commande, pas par le marqueur : le `stdout` et le
`stderr` sont dans le log de l'étape. En local, `python3 tools/verifier_ci.py` s'arrête à la
première étape non nulle et affiche son code ; le contrôle négatif est indépendant, il ne
masque pas un échec réel. La fiche
[`reports/rapport-ci.md`](../../reports/rapport-ci.md) porte les chiffres et les limites.
