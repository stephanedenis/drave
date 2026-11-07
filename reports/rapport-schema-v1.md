# B13 — le contrat v1 : `schema`/`version`, refus en JSON (code 3), entrées hostiles tolérées

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;
> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,
> F1 0,7535, attachement 236/237, couverture 0,9916, 2 spans).

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Ce qui change pour un client** : le JSON porte désormais **`schema`** (`"drave.annotation"`)
> et **`version`** (`1`) ; un **refus** est une **réponse** (JSON avec `refus`, code de sortie
> **3**) et non plus un stdout vide ; un **surrogate isolé** et une **entrée non textuelle** ne
> font plus planter la CLI ; `--json` est stable (clés triées, sans durée).
> **Le schéma est publié** : [`tools/schemas/drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json)
> (Draft 2020-12) et **validé** par `tools/verifier_schema_produit.py` (5 cas : fr, en, vide,
> ponctuation, long) avec `fastjsonschema`.
> **Porte produit** : **10 contrôles** (dont le **validateur de schéma**), **verte** ;
> **183/183** portes d'autotest.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`SCHEMA_ANNOTATION`,
> `VERSION_ANNOTATION`, `Annotation.json`), [`drave.py`](../tools/drave.py) (`_sur`, refus,
> `reconfigure`), [`test_schema_produit.py`](../tools/tests/test_schema_produit.py),
> [`porte-produit.sh`](../tools/porte-produit.sh) ; JSON [`pensee-schema-v1.json`](pensee-schema-v1.json).

## 1. Les huit champs obligatoires

`schema`, `version`, `texte`, `langue`, `script`, `refus`, `etiquettes`, `unites_semantiques` —
présents sur **toutes** les réponses, refus compris. Le test les fige et un **contrôle négatif**
(mutation : retirer `schema`) est détecté.

## 2. Les trois correctifs

| # | correctif | avant | après |
|---|---|---|---|
| 1 | **format versionné** | 11 clés sans `schema`/`version` | **13 clés**, `schema="drave.annotation"`, `version=1` |
| 2 | **refus** | stdout vide, code 1 | **JSON avec `refus`**, code **3** |
| 3 | **entrées hostiles** | `UnicodeEncodeError` (surrogate, stdout ASCII), `AttributeError` (non-str) | `_sur()` + `reconfigure` + `refus="non_texte"` |

## 3. La porte produit (8 contrôles)

`version`, `analyser fr`, `analyser en`, `rejeu` (sha256 stable), `smoke test` (8 tests),
**`schéma v1`** (6 tests), **`refus`** (JSON + code 3), `autotest` (183/183) — **~2 min**.

## 4. Ce que ce banc ne dit pas

- **Les clients existants** : le passage de 11 à 13 clés est **additif** (aucune clé retirée), mais
  un client qui compte les clés verra la différence.
- **Le refus** : le code 3 est **nouveau** ; un client qui testait `code != 0` continue de marcher.
- **Le schéma** est publié et validé sur **5 cas**, pas sur tous les textes du corpus.
- **Le validateur** dépend de `fastjsonschema` (repli minimal si absent).

## 5. Ce qui pourrait rendre cette fiche fausse

- **le contrat** n'est figé que par un test, pas par un fichier de schéma ;
- **les codes** : 0/2/3/1 — un client qui attendait 0/1 doit être mis à jour ;
- **les surrogates** sont remplacés (U+FFFD) : le texte rendu n'est plus exactement l'entrée.

## 6. La suite

1. ~~Publier le schéma~~ — **fait** (`tools/schemas/drave-annotation-v1.json`, validé, 9e contrôle).
2. **Les frontières de phrase** (URL, décimaux, `M.`) et la **partition des syntagmes**.
3. **Valider le corpus** contre le schéma (les 612 phrases du gold) dans la porte.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — le schéma versionné.
- [`drave.py`](../tools/drave.py) — refus JSON, code 3, sortie tolérante.
- [`test_schema_produit.py`](../tools/tests/test_schema_produit.py) — 6 tests.
- [`pensee-schema-v1.json`](pensee-schema-v1.json).
