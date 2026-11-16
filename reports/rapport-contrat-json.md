# T2 — l'API du JSON : candidats d'attachement en objets, rôles normalisés

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T2** (exploitable, 2/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **contrat livré et mesuré**.
>
> **Le chiffre.** Sur le gold vivant **612 phrases** : **1 883 syntagmes**, **1 883 rôles**
> non vides, **21 rôles bruts** ramenés à **8 rôles normalisés**, **0** hors table et **0**
> hors vocabulaire. Les **1 295 attachements** portent tous des `candidats` **objets**
> `{span, cible, source}` : **2 139 objets** (dont **1 062** dans `meta.alternative`),
> **0 span faux**, **1 295/1 295** cibles choisies présentes dans la liste. **Contrôle
> négatif** : un consommateur qui filtre `role == "predicat"` trouve **711** prédicats
> (**711 GV**) ; `role == "prédicat"` en trouve **0**. Le schéma v2 valide **612/612**
> annotations, les **612** v1 dérivées restent lues, et v2 refuse **612/612** v1.
>
> **Dispositif** : [`mesurer_contrat_json.py`](../tools/mesurer_contrat_json.py),
> [`roles_vocabulaire.py`](../tools/roles_vocabulaire.py),
> [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json),
> [`verifier_schema_produit.py`](../tools/verifier_schema_produit.py),
> [`test_produit.py`](../tools/tests/test_produit.py),
> [`test_schema_produit.py`](../tools/tests/test_schema_produit.py),
> JSON [`contrat-json.json`](contrat-json.json), doc
> [`docs/produit/README.md`](../docs/produit/README.md) § 3.2/3.3 bis/4/7.

## 1. Ce qui est livré

**1. Les candidats d'attachement sont des objets.** Le champ historique `candidats` de
l'étiquette reste une liste de **chaînes d'affichage** : c'est la sortie lisible et le
contrat v1. Le schéma v2 gagne **un champ** : `meta.attachement.candidats`, une liste
d'objets

```json
{"span": {"debut": 8, "fin": 12}, "cible": "dort", "source": "heuristique"}
```

- `span` : `{debut, fin}`, indices en points de code Unicode, 0-based, fin exclue ;
- `cible` : la surface du candidat, non vide ;
- `source` : `heuristique`, `neuronal` ou `humain` — ici toujours `heuristique`, car
  l'attachement est produit par les règles.

La **cible choisie** est toujours le premier objet de la liste, même quand la liste
d'affichage ne la contenait pas (cas d'un GV : `dort → chat`). Un candidat dont la cible
n'est pas retrouvée dans le texte est **écarté** plutôt que publié avec un span faux. Les
`meta.alternative[].attachement` recopient les mêmes objets.

**2. Les rôles sont normalisés.** Le vocabulaire est **fermé** :

`predicat`, `agent`, `objet`, `lieu`, `temps`, `qualite`, `possesseur`, `destinataire`.

Le JSON publie la forme canonique (`meta.role`, `meta.alternative[].role`) ; l'objet
Python interne garde la forme brute pour les règles et l'autotest. La **sortie lisible**
du CLI affiche elle aussi le rôle normalisé. Le schéma v2 déclare l'énumération, et
`normaliser_role` lève `RoleHorsVocabulaire` sur une valeur inconnue : aucun rôle hors
contrat n'est publié silencieusement.

**3. V1 reste lue.** Le schéma v1 est inchangé. Une annotation v1 (sans
`meta.attachement.candidats`, sans `meta.partition`/`meta.alternative`) est validée par
le schéma v1 et **refusée** par le schéma v2. Le cas de rétro-compatibilité du
vérificateur ne porte plus le champ v2, sinon il testerait un JSON qui n'existe pas.

## 2. La table des correspondances

La table est dans [`roles_vocabulaire.py`](../tools/roles_vocabulaire.py) ; elle est
exhaustive pour les rôles produits par `bloc_linguistique.py` et le générateur S
(**31 lignes**, plusieurs bruts par rôle).

| rôle brut | rôle normalisé | pourquoi |
|---|---|---|
| `prédicat`, `predicat` | `predicat` | les deux orthographes du même rôle |
| `agent` | `agent` | — |
| `objet`, `patient`, `complément`, `complement`, `contenu`, `theme`, `thème`, `groupe nominal` | `objet` | le patient, le complément, le thème et le GN sans fonction identifiée |
| `moyen`, `instrument` | `objet` | l'instrument est un objet de l'action |
| `lieu`, `source` | `lieu` | l'origine est un repère spatial |
| `temps` | `temps` | — |
| `qualité`, `qualite`, `attribut`, `maniere`, `manière`, `concession`, `hypothese`, `hypothèse`, `cause`, `consequence`, `conséquence` | `qualite` | l'attribut et les circonstants de manière/cause |
| `possesseur`, `possession` | `possesseur` | — |
| `destinataire`, `but` | `destinataire` | le but est la destination de l'action |

**Ce que la table ne fait pas.** Elle ne **re-annote** pas : elle range ce que les règles
publient déjà. `objet` et `qualite` sont des catégories larges, pas des fonctions
syntaxiques fines. Un `groupe nominal` sans fonction devient `objet` par défaut, ce qui
est une **convention** — le rapport le dit, et la fiche des manques le répétait déjà.

Les **21 rôles bruts observés** sur le gold tombent tous dans la table :

| rôle normalisé | segments | dont types |
|---|---:|---|
| `predicat` | 711 | GV 711 |
| `agent` | 541 | GN 541 |
| `objet` | 390 | GN 322, SUB 57, GP 11 |
| `qualite` | 120 | REL 106, SUB 10, GP 4 |
| `lieu` | 48 | GP 48 |
| `destinataire` | 37 | GP 37 |
| `temps` | 27 | GP 21, SUB 6 |
| `possesseur` | 9 | GP 9 |

## 3. Le dispositif et les mesures

```bash
python3 tools/mesurer_contrat_json.py            # écrit reports/contrat-json.json
python3 tools/mesurer_contrat_json.py --json     # imprime le relevé
```

Le banc analyse les **612 phrases** du gold vivant, valide chaque annotation avec
`fastjsonschema`, puis lit les 612 dérivées v1. Il compte les objets, vérifie que chaque
`span` découpe exactement sa `cible` dans `texte`, et compare les rôles bruts (objets
Python) aux rôles normalisés (JSON).

| mesure | valeur |
|---|---:|
| phrases du gold | **612** |
| syntagmes | **1 883** |
| rôles non vides | **1 883** |
| rôles bruts distincts | **21** |
| rôles normalisés distincts | **8** |
| rôles bruts hors table | **0** |
| rôles hors vocabulaire | **0** |
| attachements | **1 295** |
| attachements avec au moins un objet | **1 295** (1,0000) |
| objets `{span, cible, source}` | **2 139** |
| objets dans `meta.alternative` | **1 062** |
| taille moyenne de la liste | **1,6517** |
| spans faux | **0** |
| cible choisie présente dans la liste | **1 295/1 295** |
| annotations v2 validées | **612/612** |
| annotations v1 validées | **612/612** |
| v1 refusées par v2 | **612/612** |

**Ce que ça dit.** Le contrat est **utilisable sans parser les chaînes** : un consommateur
lit `meta.attachement.candidats[].cible` et `span`, et vérifie lui-même le découpage. Le
champ historique reste là pour la sortie lisible et les clients v1. Le rôle est stable :
`predicat` ne dépend plus de la règle qui a produit le GV.

## 4. Les contrôles négatifs

**1. Le filtre du consommateur.** Sur les 612 annotations, un filtre
`role == "predicat"` rend **711 segments, tous des GV**. Le même filtre sur l'ancienne
forme accentuée `role == "prédicat"` rend **0**. Si la normalisation n'avait pas eu lieu,
le premier filtre aurait manqué les **369** `prédicat` du chunker et n'aurait trouvé que
les **342** `predicat` du générateur S.

**2. Le rôle inconnu.** `normaliser_role("role_invente")` lève
`RoleHorsVocabulaire` avec le message
`rôle hors vocabulaire : 'role_invente' (attendu : predicat, agent, objet, lieu, temps,
qualite, possesseur, destinataire)`. Le test `test_role_hors_vocabulaire_refuse` le fige,
et vérifie aussi que la table ne peut pas produire une valeur hors vocabulaire.

**3. Le candidat qui redevient une chaîne.** Remplacer le premier objet par
`"« une chaîne d'affichage »"` fait **refuser** l'annotation par le schéma v2 ; retirer
son `span` aussi. Le vérificateur public expose ces deux refus dans
`controles_negatifs` (`role_hors_vocabulaire: true`, `candidat_chaine: true`).

**4. La rétro-compatibilité.** Les 612 annotations dérivées v1 passent le schéma v1
(**612/612**) et sont refusées par v2 (**612/612**). Le cas v1 du vérificateur a été
privé de `meta.attachement.candidats` : sans cela, le test de rétro-compatibilité
validerait un champ v2 dans un document v1.

## 5. Les tests produit

```bash
python3 tools/tests/test_produit.py          # Ran 24 tests, OK
python3 tools/tests/test_schema_produit.py   # Ran 9 tests, OK
python3 tools/verifier_schema_produit.py     # 6 cas, 0 échec + contrôles négatifs
```

Quatre tests T2 s'ajoutent aux 20 du smoke test :

1. `test_candidats_attachement_en_objets` — chaque attachement a des objets, chaque objet
   a exactement `{span, cible, source}`, et `texte[debut:fin] == cible` ;
2. `test_candidat_negatif_absent_du_texte` — aucun candidat sans span n'est publié, et
   `structure la plus proche` n'apparaît jamais comme cible ;
3. `test_roles_normalises_et_filtre_predicat` — les rôles publiés sont dans le
   vocabulaire, `predicat` trouve des GV, `prédicat` n'en trouve aucun ;
4. `test_role_hors_vocabulaire_refuse` — la table, les alias et le refus sont figés.

Le test du schéma vérifie en plus que `meta.attachement.candidats` et l'énumération
`role` sont **déclarés** dans le schéma v2, pas seulement tolérés.

## 6. Ce qui pourrait rendre ce résultat faux

1. **La normalisation est grossière.** `objet` regroupe `patient`, `complément`,
   `contenu`, `theme` et `groupe nominal` ; `qualite` regroupe `attribut`, `maniere`,
   `concession`, `hypothese`, `cause` et `consequence`. Un consommateur qui attend une
   fonction syntaxique fine lira une catégorie large.
2. **Le span est la première occurrence.** Pour une surface répétée, `texte.find` donne
   la première position, pas la position du candidat visé. C'est une **position de
   candidat**, pas une résolution d'anaphore ; le rapport le nomme.
3. **`source` ne distingue pas le générateur S.** Les candidats viennent du chunker, du
   générateur S ou de `_verbes_proches` ; tous portent `heuristique`. Un consommateur ne
   peut pas savoir quelle règle a produit le candidat.
4. **Le gold est in-sample.** Les règles ont été dessinées sur les 612 phrases ; les 21
   rôles bruts sont ceux de ce corpus. Les rôles `instrument`, `maniere`, `source`,
   `consequence` et `objet` (brut) sont dans la table mais **non observés** ici : le
   corpus ne les exerce pas.
5. **Les annotations v1 sont dérivées.** Les 612 v1 sont les 612 v2 privées des champs
   ajoutés ; ce n'est pas un corpus v1 indépendant.
6. **Le schéma valide la forme, pas la qualité.** Un candidat peut avoir le bon span et
   être un mauvais candidat ; l'attachement exact reste **238/239** (fiche B13), et la
   normalisation ne change pas cette mesure.
7. **Un rôle nouveau casserait la sérialisation.** C'est voulu : `normaliser_role` est
   strict. Une règle qui ajoute un rôle doit ajouter sa ligne à la table et son test ;
   sinon le JSON lève, il ne publie pas un rôle hors contrat.

## 7. Les fichiers

- [`tools/roles_vocabulaire.py`](../tools/roles_vocabulaire.py) — le vocabulaire fermé et
  la table des 31 correspondances.
- [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_attachement`,
  `_candidats_attachement`, `_meta_json`.
- [`tools/drave.py`](../tools/drave.py) — la sortie lisible affiche le rôle normalisé.
- [`tools/schemas/drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json) —
  le champ `meta.attachement.candidats` et l'énumération `role`.
- [`tools/verifier_schema_produit.py`](../tools/verifier_schema_produit.py) — les deux
  nouveaux contrôles négatifs.
- [`tools/tests/test_produit.py`](../tools/tests/test_produit.py) — 4 tests T2.
- [`tools/tests/test_schema_produit.py`](../tools/tests/test_schema_produit.py) — le
  schéma déclare les candidats et les rôles.
- [`tools/mesurer_contrat_json.py`](../tools/mesurer_contrat_json.py) — le banc.
- [`reports/contrat-json.json`](contrat-json.json) — le relevé complet.
- [`docs/produit/README.md`](../docs/produit/README.md) § 3.2, 3.3 bis, 4 et 7 — la doc
  du produit.
