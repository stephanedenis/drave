# B13 — le schéma v2 : `meta.partition` et `meta.alternative` typés, version 2, v1 toujours lue

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.3 · **Date** : 2026-11-07 ·
> **Verdict** : ✅
> **Ce qui change pour un client** : l'annotation porte `schema: "drave.annotation"` et
> `version: 2`. Le schéma v2 publie les deux champs qui documentent les syntagmes qui se
> chevauchent : `meta.partition` (`{groupe, rang, membres, vue}`) et `meta.alternative` (la liste
> des autres segments du groupe, avec `relation`, `union`, `rang`, `retire`, `role`,
> `attachement`). Les champs sont **additifs** : un client qui ne lit pas `meta` continue de lire
> l'annotation. **La version 1 reste lue** : `verifier_schema_produit.py` choisit le schéma
> d'après `version`, et un **contrôle négatif** vérifie que le schéma v2 refuse bien une
> annotation v1.
>
> **Dispositif** : [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json),
> [`drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json) (inchangé),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`VERSION_ANNOTATION = 2`),
> [`verifier_schema_produit.py`](../tools/verifier_schema_produit.py),
> [`test_schema_produit.py`](../tools/tests/test_schema_produit.py) ; JSON
> [`pensee-schema-v2.json`](pensee-schema-v2.json).

## 1. Les deux champs ajoutés

`meta.partition` et `meta.alternative` ne sont présents que sur un **syntagme** qui appartient à
un groupe de chevauchement (au moins deux segments). Le schéma v2 les type ; il laisse `meta`
ouvert (`additionalProperties: true`) pour les autres méta-données (`ouvert`, `role`,
`attachement`, `union`, `contexte`).

```json
{
  "meta": {
    "partition": {"groupe": 0, "rang": 1, "membres": 3, "vue": "alternative"},
    "alternative": [
      {"type": "REL", "debut": 18, "fin": 42, "source": "heuristique",
       "union": true, "relation": "inclut", "rang": 2,
       "role": "sujet", "attachement": {"segment": "qui dort", "cible": "voisine"}}
    ]
  }
}
```

Les contraintes publiées : `groupe ≥ 0`, `rang ≥ 1`, `membres ≥ 2`, `vue ∈ {alternative,
filtrer_union, filtrer}` ; pour chaque alternative, `type ∈ {GN, GV, GP, REL, SUB}`,
`relation ∈ {inclut, inclus, meme_span, croise}`, `source ∈ {heuristique, neuronal, humain}`,
`union` et `retire` booléens, `attachement = {segment, cible}`. Le schéma **vérifie la forme**,
pas les invariants sémantiques (réciprocité des relations, permutation des rangs, unicité des
groupes) : ceux-là restent couverts par les tests du bloc, pas par le validateur JSON.

## 2. La rétro-compatibilité

Le vérificateur compile les deux schémas une fois, puis choisit :

| `version` de l'annotation | schéma utilisé | résultat |
|---:|---|---|
| `1` | `drave-annotation-v1.json` | lu et validé |
| `2` | `drave-annotation-v2.json` | lu et validé |
| autre | — | refusé (version inconnue) |

Le cas de rétro-compatibilité est une annotation réelle ramenée à `version: 1` et privée de
`meta.partition`/`meta.alternative` ; elle passe le schéma v1. Le **contrôle négatif** la
soumet au schéma v2 : il la refuse (`version` attend `2`). Les deux conditions sont affichées et
comptent dans le code de sortie.

## 3. La validation

Commande d'acceptation :

```bash
python3 tools/verifier_schema_produit.py --gold 20
```

Résultat : **26 cas, 0 échec** — 5 cas de base (`fr`, `en`, `vide`, `ponctuation`, `long`) en
v2, **1 cas v1** de rétro-compatibilité, **20 phrases du gold** (`g001`–`g020`) en v2 ; les
deux contrôles (v1 lue, v2 refuse v1) passent. Validateur : `fastjsonschema`.

Mesure complémentaire (hors acceptance) : les **612 phrases du gold** analysées dans les trois
vues `alternative`, `filtrer_union` et `filtrer`, soit **1 836 annotations**, passent le schéma
v2 (**0 échec**). En vue `alternative` sur le gold : **146 groupes**, **437 porteurs**,
**930 alternatives** (GN 393, GV 357, REL 103, GP 49, SUB 28) ; relations `croise` 386,
`inclus` 263, `inclut` 263, `meme_span` 18 ; **0 retiré** (aucune suppression dans cette vue).

## 4. Ce que ce banc ne dit pas

- **La forme, pas le sens** : le schéma valide les types et les énumérations ; il ne prouve pas
  que le rang 1 est la bonne coupe ni que la relation est réciproque.
- **Les clients** : le bump v1 → v2 change les octets et le `sha256` de rejeu ; un client qui
  comptait les clés ou comparait des octets doit être mis à jour.
- **Les types** : l'énumération `GN, GV, GP, REL, SUB` est celle des syntagmes observés sur le
  gold ; un nouveau type demanderait une v3.
- **Le repli** : sans `fastjsonschema`, la validation est minimale (champs obligatoires et
  version), pas structurelle.

## 5. Ce qui pourrait rendre cette fiche fausse

- **Un type de syntagme non prévu** (ou un champ ajouté dans `meta.alternative`) : le schéma v2,
  qui ferme les alternatives (`additionalProperties: false`), le refuserait.
- **Une annotation sans `version`** : elle n'est pas lue par le vérificateur (le champ est
  obligatoire depuis la v1).
- **Le gold** : les 1 836 annotations sont un corpus **in-sample** ; elles prouvent la forme sur
  les cas du dépôt, pas sur un texte arbitraire.
- **Le contrôle négatif** : il vérifie que v2 refuse une v1, pas que v1 refuse une v2.

## 6. La suite

1. **J1.4 — la restitution v0** : reconstruire la surface depuis l'annotation et mesurer le
   miroir sur 50 textes libres.
2. **`g017`** : le dernier span inatteignable nommé.
3. **La porte produit** : elle valide désormais le schéma **v2** et garde le cas v1.

## 7. Fichiers

- [`tools/schemas/drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json) — le schéma publié.
- [`tools/schemas/drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json) — le schéma v1, inchangé.
- [`tools/verifier_schema_produit.py`](../tools/verifier_schema_produit.py) — sélection par version, 26 cas, contrôle négatif.
- [`tools/tests/test_schema_produit.py`](../tools/tests/test_schema_produit.py) — 8 tests (dont v2 et rétro-compatibilité).
- [`reports/pensee-schema-v2.json`](pensee-schema-v2.json).
