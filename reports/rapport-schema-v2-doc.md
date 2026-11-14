# J11.4 — le contrat : le schéma v2 documenté, 6 cas / 0 échec, v1 toujours lue

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **J11.4** · **Date** : 2026-11-14 ·
> **Verdict** : ✅
>
> **Commit mesuré** : `09e54143` — le code et les deux schémas sont inchangés ; cette fiche
> mesure le contrat existant et documente la notice produit.
>
> **Ce que cette fiche fixe.** Le schéma v2 est **documenté dans la notice**
> [`docs/produit/README.md`](../docs/produit/README.md) § 3.3 bis : les **quatre** champs de
> `meta.partition`, les **dix** champs de `meta.alternative` (sept obligatoires, trois
> optionnels), un exemple réel et la **rétro-compatibilité v1**. Vérification :
> `tools/verifier_schema_produit.py --json` lit **les deux versions** (`versions_lues: [1, 2]`),
> **6 cas / 0 échec** ; `--gold 20` donne **26 cas / 0 échec** ; les **612 phrases du gold**
> passent le schéma v2 (**612/612**) et les **612 annotations dérivées v1** passent le schéma v1
> (**612/612**). Contrôles négatifs : le schéma v2 refuse les 612 annotations v1, le schéma v1
> refuse les 612 annotations v2, et la mutation d'un champ obligatoire est refusée.
>
> **Dispositif** : [`drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json),
> [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json),
> [`verifier_schema_produit.py`](../tools/verifier_schema_produit.py),
> [`mesurer_schema_v2_doc.py`](../tools/mesurer_schema_v2_doc.py),
> [`test_schema_produit.py`](../tools/tests/test_schema_produit.py),
> [`docs/produit/README.md`](../docs/produit/README.md) ; JSON
> [`schema-v2-doc.json`](schema-v2-doc.json).

## 1. Le dispositif

- **Deux schémas publiés** (Draft 2020-12) : `drave-annotation-v1.json` (inchangé) et
  `drave-annotation-v2.json` (le contrat courant). Les deux sont compilés par `fastjsonschema`.
- **Le vérificateur** lit `version` dans l'annotation, choisit le schéma correspondant, valide
  les cas de base (`fr`, `en`, `vide`, `ponctuation`, `long`), un **cas v1** de
  rétro-compatibilité et, si `--gold N` est donné, les `N` premières phrases du gold.
- **La notice produit** documente les champs et la compatibilité ; elle renvoie au schéma et à
  cette fiche.
- **Le code mesuré** est celui du commit `09e54143` (F1 **0,7902**, attachement **238/239**,
  schéma v2, restitution v1) ; J11.4 ne modifie **ni le bloc, ni le vérificateur, ni les
  schémas** : il ajoute le banc [`mesurer_schema_v2_doc.py`](../tools/mesurer_schema_v2_doc.py)
  et la documentation.

Commandes d'acceptation :

```bash
python3 tools/verifier_schema_produit.py --json       # 5 cas v2 + 1 cas v1
python3 tools/verifier_schema_produit.py --gold 20    # + 20 phrases du gold
python3 tools/tests/test_schema_produit.py            # 8 tests du contrat
```

## 2. Les champs documentés

`meta.partition` et `meta.alternative` ne sont présents que sur un **syntagme** qui appartient à
un **groupe de chevauchement** (au moins deux segments dont les spans s'intersectent). Ils sont
**additifs et optionnels** ; `meta` reste ouvert pour les autres clés (`role`, `attachement`,
`union`, `ouvert`, `contexte`).

**`meta.partition` — la place du segment dans son groupe.**

| champ | type | contrainte | sens |
|---|---|---|---|
| `groupe` | entier | `≥ 0` | identifiant du groupe de chevauchement |
| `rang` | entier | `≥ 1` | rang dans le groupe ; `1` = segment préféré (chunker `union`, puis le plus large, puis le plus sûr) |
| `membres` | entier | `≥ 2` | nombre de segments du groupe |
| `vue` | énumération | `alternative`, `filtrer_union`, `filtrer` | vue qui a produit l'annotation (`brut` n'écrit pas ces champs) |

**`meta.alternative` — les autres segments du groupe, vus depuis le porteur.**

| champ | type | contrainte | sens |
|---|---|---|---|
| `type` | énumération | `GN`, `GV`, `GP`, `REL`, `SUB` | type du segment alternatif |
| `debut`, `fin` | entiers | `0 ≤ debut < fin` | span en **points de code Unicode**, 0-based, `[debut:fin)` |
| `source` | énumération | `heuristique`, `neuronal`, `humain` | provenance du segment |
| `union` | booléen | — | le segment vient de l'union S/chunker |
| `relation` | énumération | `inclut`, `inclus`, `meme_span`, `croise` | relation **du point de vue du porteur** : `inclut` = le porteur contient l'alternative ; `inclus` = l'alternative contient le porteur ; `croise` = intersection partielle |
| `rang` | entier | `≥ 1` | rang de l'alternative dans le groupe |
| `retire` | booléen | optionnel | présent en vue `filtrer`/`filtrer_union` ; `true` = segment retiré de la sortie mais toujours lisible ici |
| `attachement` | objet | optionnel, `{segment, cible}` | attachement recopié de l'alternative, quand il existe |
| `role` | chaîne | optionnelle | rôle recopié de l'alternative, quand il existe |

Exemple réel (phrase du § 3.3 bis, vue `alternative`, segment `REL [22:42]`) :

```json
{
  "type": "REL", "debut": 22, "fin": 42, "valeur": "qui dort sur le toit",
  "meta": {
    "partition": {"groupe": 0, "rang": 2, "membres": 3, "vue": "alternative"},
    "alternative": [
      {"type": "REL", "debut": 22, "fin": 54, "source": "heuristique",
       "union": true, "relation": "inclus", "rang": 1,
       "attachement": {"segment": "qui dort sur le toit se réveille", "cible": "réveille"},
       "role": "qualité"},
      {"type": "GV", "debut": 43, "fin": 54, "source": "heuristique",
       "union": false, "relation": "croise", "rang": 3,
       "attachement": {"segment": "se réveille", "cible": "voisine"},
       "role": "predicat"}
    ]
  }
}
```

**Lecture.** Le porteur est le **rang 2** d'un groupe de **3** ; l'alternative de rang 1 (la REL
longue `[22:54]`) le **contient** (`inclus`), celle de rang 3 (le GV `[43:54]`) le **croise**.
En vue `filtrer`, le segment écarté sort de `etiquettes` mais reste décrit ici avec
`retire: true` : **la perte est documentée, pas silencieuse**.

Sur le gold 612, vue `alternative` : **146 groupes**, **437 porteurs**, **930 alternatives**
(GN **393**, GV **357**, REL **103**, GP **49**, SUB **28**) ; relations `croise` **386**,
`inclus` **263**, `inclut` **263**, `meme_span` **18** ; source `heuristique` **930**. Ces comptes
reproduisent ceux de [`rapport-schema-v2.md`](rapport-schema-v2.md) (146/437/930), contrôle de
cohérence entre les deux fiches.

## 3. La validation des deux versions

| contrôle | commande | résultat |
|---|---|---:|
| vérificateur, cas de base | `python3 tools/verifier_schema_produit.py --json` | **6 cas, 0 échec** ; `versions_lues: [1, 2]` ; `v1_lue: true` ; `v2_refuse_v1: true` ; `fastjsonschema` |
| vérificateur, gold 20 | `python3 tools/verifier_schema_produit.py --gold 20` | **26 cas, 0 échec** |
| gold 612, schéma v2 | validation directe `fastjsonschema` | **612/612** |
| gold 612, schéma v1 | 612 annotations dérivées (`version: 1`, champs v2 retirés) | **612/612** |
| contrôle négatif v2 → v1 | les 612 annotations v1 soumises au schéma v2 | **612/612 refusées** |
| contrôle négatif v1 → v2 | les 612 annotations v2 soumises au schéma v1 | **612/612 refusées** |
| mutation | annotation v2 privée de `schema` | **refusée** |
| tests du contrat | `python3 tools/tests/test_schema_produit.py` | **8/8**, `OK` |

Le vérificateur affiche les deux conditions de rétro-compatibilité et les inclut dans son code
de sortie : `0` seulement si tous les cas passent **et** si `v1_lue` et `v2_refuse_v1` sont
vrais.

## 4. La rétro-compatibilité

Les **huit champs obligatoires** de la racine (`schema`, `version`, `texte`, `langue`, `script`,
`refus`, `etiquettes`, `unites_semantiques`) sont **les mêmes** en v1 et en v2 ; le bump n'ajoute
que deux champs **optionnels** dans `meta`. Un client v1 qui ne lit pas `meta` continue donc de
lire l'annotation.

| `version` de l'annotation | schéma choisi | résultat |
|---:|---|---|
| `1` | [`drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json) (inchangé) | lu et validé |
| `2` | [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json) | lu et validé |
| autre | — | refusé (version inconnue) |

Le cas v1 du vérificateur est l'annotation `fr` ramenée à `version: 1` et **privée** de
`meta.partition`/`meta.alternative` ; il passe le schéma v1, et le schéma v2 le refuse. C'est une
preuve de **sélection par version** et de **compatibilité structurelle**, pas une preuve sur les
anciens clients : le passage à `version: 2` change les **octets** et le `sha256` de rejeu. La
compatibilité est donc **de forme et de lecture**, jamais **octet pour octet**.

## 5. Ce que ce banc ne dit pas

- **La forme, pas le sens** : le schéma valide les types, les énumérations et les champs requis ;
  il ne prouve ni la réciprocité des relations, ni l'unicité des groupes, ni que le rang 1 est la
  bonne coupe. Ces invariants restent couverts par les tests du bloc.
- **Le corpus v1 dérivé** : les 612 annotations v1 sont les annotations v2 **downgradées**, pas
  un corpus v1 indépendant. Elles prouvent que le schéma v1 et la sélection par version
  fonctionnent sur 612 formes réelles ; elles ne prouvent pas qu'une annotation v1 d'un autre
  outil passerait.
- **Le repli** : sans `fastjsonschema`, la validation du vérificateur est **minimale** (champs
  obligatoires + version), pas structurelle. Le run publié utilise `fastjsonschema`.
- **Le gold** : les 146 groupes / 437 porteurs / 930 alternatives sont **in-sample** ; ils
  décrivent le corpus du dépôt, pas un texte arbitraire.
- **Les clients** : aucun client réel n'est testé ; seule la lecture des deux schémas l'est.

## 6. Ce qui pourrait rendre cette fiche fausse

- **Un changement de schéma après `09e54143`** : la fiche mesure ce commit ; un ajout de type ou
  de champ (fermé par `additionalProperties: false` dans `meta.alternative`) la périmerait.
- **Une annotation sans `version`** : elle n'est pas lue par le vérificateur (champ obligatoire
  depuis la v1).
- **Un validateur absent** : le repli minimal ne vérifie pas la forme ; les chiffres 612/612
  supposent `fastjsonschema`.
- **La dérive de la doc** : la notice et cette fiche citent les mêmes champs ; si l'une change
  sans l'autre, la revue de documentation ne le voit pas forcément (elle vérifie les liens, pas
  la sémantique des tableaux).

## 7. La suite

J11.4 **ferme la suite produit** de la semaine (J11.1–J11.4) : exemples rejoués, mesure par
langue, robustesse des 50 textes, schéma documenté. La prochaine action de **B13** reste
**trancher la convention d'adverbe (`g017`)** ; puis T132/T133 et le **gold 200+**. Le reste de
la roadmap est dans [`docs/pilotage/roadmap.md`](../docs/pilotage/roadmap.md).

## 8. Fichiers

- [`docs/produit/README.md`](../docs/produit/README.md) — § 3.3 bis : les deux champs, l'exemple,
  la rétro-compatibilité et les commandes de validation.
- [`tools/schemas/drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json) — le schéma v2.
- [`tools/schemas/drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json) — le schéma v1, inchangé.
- [`tools/verifier_schema_produit.py`](../tools/verifier_schema_produit.py) — sélection par version, cas v1, contrôle négatif.
- [`tools/mesurer_schema_v2_doc.py`](../tools/mesurer_schema_v2_doc.py) — le banc de cette fiche (612 v2 + 612 v1 + contrôles).
- [`tools/tests/test_schema_produit.py`](../tools/tests/test_schema_produit.py) — 8 tests du contrat.
- [`reports/schema-v2-doc.json`](schema-v2-doc.json) — les chiffres bruts de cette fiche.
