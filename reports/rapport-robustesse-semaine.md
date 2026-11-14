# J11.3 — les 50 textes libres : 0 plantage, 50/50 au schéma v2, 115 chevauchements en `alternative`, 0 en `filtrer`

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **J11.3** · **Date** : 2026-11-14 ·
> **Verdict** : ✅
>
> **Commit mesuré** : `09e54143` — **F1 0,7902**, **POS 0,8625**, **attachement 238/238
> labels** (238/239 cibles, 0,9958), **schéma v2**, **restitution v1**.
>
> **Ce que le produit fait sur les 50 textes de l'audit A26**, rejoués avec le code de la
> semaine : **0 plantage**, **50/50 JSON valide**, **50/50 portent les 8 champs** obligatoires
> et passent le schéma v2 ; **4 refus** sont des réponses JSON (code 3) ; en vue
> **`alternative`**, **395 segments** et **115 chevauchements** dans **21/46** textes
> annotés ; en vue **`filtrer`**, **313 segments** et **0 chevauchement** ; **46/46 formes
> canoniques** en restitution, le miroir strict reste **5/46 = 0,1087** ; temps CLI médian
> **159,2 ms**, API **2,7 ms**.
>
> **Dispositif** : [`tools/mesurer_robustesse_semaine.py`](../tools/mesurer_robustesse_semaine.py),
> banc [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json) (audit A26),
> schéma [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json).
> JSON : [`pensee-robustesse-semaine.json`](pensee-robustesse-semaine.json).

## 1. Le dispositif et les définitions

- **Le banc** : les **50 phrases libres** écrites pour l'audit A26 — **41 françaises**,
  **5 anglaises**, **4 refus** (vide, espaces, ponctuation, emoji). **46 textes annotés**.
- **Le CLI** : `python3 tools/drave.py analyser TEXTE --json`, en **subprocess**, **deux
  passages** par texte (le second sert au déterminisme). Langue **auto**, comme l'audit A26.
- **L'API** : `bloc_linguistique.Heuristique(partition=...).analyser(texte)`, dans les vues
  **`alternative`** et **`filtrer`** ; `filtrer_union` est mesurée en contrôle.
- **Le chevauchement** : une paire `(i, j)`, `i < j`, de **syntagmes** dont les spans
  s'intersectent **strictement** (`max(debut) < min(fin)`) ; toutes les paires sont comptées,
  comme dans l'audit A26.
- **Les 8 champs** : `schema`, `version`, `texte`, `langue`, `script`, `refus`,
  `etiquettes`, `unites_semantiques` — les champs obligatoires du schéma v2, validés par
  `fastjsonschema` (pas seulement vérifiés par présence).
- **La restitution** : `restitution.mesurer_banc_v1` — forme canonique, miroir strict,
  structure (segments, rôles, cibles), stabilité et contrôles négatifs.
- **L'invariant de version** : `drave evaluer --json` sur le gold vivant (**612 phrases**)
  pour dire sur quel code porte la mesure : **F1 0,7902**, **POS 0,8625**, **238/238
  labels** d'attachement (238/239 cibles, 0,9958).

## 2. Ce qui tient

| invariant | mesure |
|---|---:|
| plantages (code hors `{0, 3}`, traceback) | **0/50** |
| codes de sortie | **46 × 0**, **4 × 3** |
| JSON valide | **50/50** (46 succès + 4 refus) |
| `stderr` sur un succès | **0/50** |
| 8 champs obligatoires | **50/50** CLI · **50/50** API `alternative` · **50/50** API `filtrer` |
| validation JSON Schema v2 | **50/50** CLI · **50/50** API `alternative` · **50/50** API `filtrer` |
| déterminisme (deux passages) | **50/50** |
| spans hors texte / spans vides | **0/4 827** / **0** |
| cibles absentes du texte | **0/315** |
| étiquettes au total | **4 827** |

**Le refus est devenu une réponse.** Les 4 refus (`f14`–`f17`) sortent en **code 3** avec un
**JSON valide** (`refus: "vide"`, `etiquettes: []`) ; l'audit A26 les avait en **code 1** avec
**0 octet** sur stdout. Un pipeline `... --json | jq` ne casse plus sur un refus.

## 3. Les chevauchements, les deux vues

| vue | segments | chevauchements | textes avec chevauchement | textes sans syntagme |
|---|---:|---:|---:|---:|
| **`alternative`** (défaut) | **395** | **115** | **21/46** | **7/50** (dont 4 refus) |
| **`filtrer`** (linéaire) | **313** | **0** | **0/46** | **7/50** (dont 4 refus) |
| `filtrer_union` (contrôle) | 352 | 40 | 11/46 | 7/50 |

**Ce que ça dit** :

- **`filtrer` fait exactement ce qu'elle promet** : **0 chevauchement sur 50 textes**, avec
  **313 segments** — la vue n'est pas vide, le zéro n'est pas un artefact.
- **`alternative` documente** les **115 paires** au lieu de les cacher ; les textes les plus
  touchés sont `f50` (**63** paires, le texte long), `f43` (10), `f24` (5), `f45` et `f46`
  (4 chacun), `f41` (3).
- **3 textes annotés n'ont aucun syntagme** : `f18` (`1234567890`), `f27` (`Élodie sourit.`)
  et `f37` (email/téléphone) — plus les **4 refus**, soit **7/50** au total. L'audit A26 en
  comptait **4/46** (`f13`, `f18`, `f27`, `f37`) : **`f13` est désormais segmenté**.
- **La langue d'analyse change le compte** : en forçant `fr`, `f27` et `f37` reçoivent des
  syntagmes et le total des textes sans syntagme retombe à **5/50**, le chiffre du re-test
  B13. La mesure J11.3 est en **langue auto**, la même convention que l'audit A26.

## 4. La restitution

| mesure | J8.1 (référence) | **J11.3** |
|---|---:|---:|
| annotations / refus | 46 / 4 | **46 / 4** |
| forme canonique exacte | 46/46 = 1,0000 | **46/46 = 1,0000** |
| miroir strict | 5/46 = 0,1087 | **5/46 = 0,1087** |
| strict sur la forme canonique | 1/46 = 0,0217 | **1/46 = 0,0217** |
| segments | 395 | **395** |
| segments avec rôle | 395/395 | **395/395** |
| cibles (attachements) | 315 | **315** |
| cibles résolues dans la source | 315/315 | **315/315** |
| cibles portées par un autre segment | 313/315 = 0,9937 | **313/315 = 0,9937** |
| couverture des jetons / caractères | 65,84 % / 75,19 % | **65,84 % / 75,19 %** |
| stabilité structurelle (forme → surface → forme) | 18/46 = 0,3913 | **18/46 = 0,3913** |
| stabilité des jetons | 46/46 | **46/46** |
| contrôle négatif canonique (mélange, troncature) | 46/46 détectés, 0/46 exacts | **46/46 détectés, 0/46 exacts** |
| contrôle négatif de structure | 43/43 éligibles détectés | **43/43 éligibles détectés** |

**Lecture.** La restitution est **identique à la v1** sur ces 50 textes : la semaine
(J11.1, J11.2) n'a pas déplacé la segmentation du banc libre. Le chiffre utile reste
**46/46 canonique**, pas le strict **0,1087** : la forme canonique replie la casse, la
ponctuation et les espaces ; le miroir strict compare à la surface brute et **ne doit pas
monter**. La limite reste la **stabilité structurelle (18/46)** : re-analyser la surface
canonique change la segmentation, même si le lexique est stable **46/46**.

## 5. Le temps

| mesure | min | médiane | moyenne | p95 | max |
|---|---:|---:|---:|---:|---:|
| **CLI**, 50 textes (ms) | **142,3** | **159,2** | 160,4 | 175,4 | **257,7** (`f50`) |
| **API**, 50 textes (ms) | **0,0** | **2,7** | 4,4 | 6,4 | **74,0** (`f50`) |
| API `filtrer` (ms) | 0,0 | 2,5 | 3,9 | 6,7 | 61,4 (`f50`) |

**Ce que ça dit** :

- Les **50 invocations CLI** coûtent **8,0 s** au total (une par texte, sans lot) ; la
  médiane est dominée par le **démarrage de Python** (~150 ms), pas par l'analyse.
- L'API est à **quelques ms** ; le maximum est `f50` (74,0 ms), le texte long de 2 144
  caractères.
- Le batch de restitution (46 annotations, re-analyse et contrôles compris) prend
  **12,0 s** : c'est un coût de banc, pas le coût d'une analyse.

## 6. La comparaison avec l'audit A26

L'audit A26 est daté du **2026-11-06**, commit **`56eb43af`**. La comparaison n'est donc
**pas à code constant** : le module a changé (morphologie, chunker, `s065`, J11.1/J11.2).
Les écarts de chevauchements sont des effets du **code**, pas du compteur.

| mesure | A26 (06/11) | **J11.3 (14/11)** | lecture |
|---|---:|---:|---|
| plantages | 0/50 | **0/50** | = |
| JSON invalide | 0/46 | **0/50** | les refus rendent un JSON |
| refus | 4/50, code 1, stdout 0 o | **4/50, code 3, JSON** | corrigé |
| 8 champs obligatoires | 0/46 (ni `schema` ni `version`) | **50/50** | corrigé |
| schéma v2 | absent | **50/50** | nouveau |
| chevauchements, `alternative` | **107 paires / 23/46** | **115 paires / 21/46** | même définition ; code différent |
| chevauchements, `filtrer` | 0 conflit après filtre `meta.union` (hors schéma) | **0/50** (vue publiée) | la promesse est tenue |
| textes annotés sans syntagme | 4/46 (`f13`, `f18`, `f27`, `f37`) | **3/46** (`f18`, `f27`, `f37`) | `f13` segmenté |
| étiquettes / cibles | 4 501 / 284 | **4 827 / 315** | le code produit plus de structure |
| spans hors texte / cibles absentes | 0 / 0 | **0 / 0** | = |
| temps CLI médian | 152,7 ms (136,8–226,6) | **159,2 ms** (142,3–257,7) | même ordre |
| temps API médian | 1,0 ms (0,2–45,1) | **2,7 ms** (0,0–74,0) | même ordre ; bruit de machine |

**Le détail des écarts de chevauchements par texte** montre que le compteur n'est pas la
cause : les textes qui changent sont ceux dont le chunker a bougé, pas tous les textes.

| texte | A26 | J11.3 |
|---|---:|---:|
| `f50` | 50 | **63** |
| `f43` | 10 | **10** |
| `f24` | 5 | **5** |
| `f06` | 4 | **2** |
| `f26` | 1 | **0** |
| `f29` | 2 | **0** |
| `f20` | 2 | **3** |
| `f21` | 3 | **2** |
| `f31` | 1 | **2** |
| `f34` | 3 | **2** |
| **total** | **107** | **115** |

Les deux textes qui passent à **0** (`f26`, `f29`) expliquent la baisse du nombre de textes
touchés (**23 → 21**) malgré la hausse du total. `f50` à lui seul passe de **50 à 63**
paires : c'est le texte long, et c'est là que le chunker a le plus bougé.

## 7. Les contrôles négatifs

| contrôle | attendu | observé |
|---|---:|---:|
| le schéma v1 lit une annotation v1 | oui | **oui** |
| le schéma v2 refuse une annotation v1 | oui | **oui** |
| le schéma v2 refuse une annotation sans `refus` | oui | **oui** |
| le compteur détecte un chevauchement injecté | 1 | **1** (témoin à 0) |
| la vue `filtrer` n'est pas vide | > 0 | **313 segments** |
| restitution : mélange exact | 0/46 | **0/46** (détecté **46/46**) |
| restitution : troncature exacte | 0/46 | **0/46** (détecté **46/46**) |
| restitution : rôles retirés | 43/43 | **43/43** |
| restitution : cibles retirées | 43/43 | **43/43** |
| refus : code 3 + JSON valide | 4/4 | **4/4** |

Le contrôle du compteur est un **ajout au témoin** : `Le chat dort.` n'a **0** chevauchement ;
on duplique un segment, le compteur en trouve **1**. Le zéro de `filtrer` n'est donc pas un
compteur qui ne compte rien : c'est un compteur qui compte, sur une vue qui ne produit pas de
paire.

## 8. Ce que ce banc ne dit pas — et ce qui pourrait rendre cette fiche fausse

- **Le corpus** : 50 phrases **écrites à la main** pour l'audit A26, pas un échantillon
  aléatoire. C'est un banc de robustesse d'entrée, pas de justesse linguistique.
- **La définition** du chevauchement est **stricte** (toutes les paires de syntagmes). Une
  autre définition — paires de types différents, spans identiques exclus, chevauchements de
  `phrase`/`pragmatique` inclus — donnerait un autre chiffre. Le compte A26 est reproduit à
  définition constante, mais **à code non constant**.
- **La langue** : en forçant `fr`, `f27` et `f37` reçoivent des syntagmes et le compte des
  textes sans syntagme passe de **3/46 à 5/50**. La fiche mesure en **auto** ; toute
  comparaison doit dire sa convention.
- **Les 4 refus** n'ont pas d'annotation : les mesures de structure portent sur **46 textes**,
  pas 50. Ils sont comptés séparément, et validés comme réponses JSON.
- **Le temps** est une **seule passe** sur une machine chargée ; le CLI inclut le démarrage
  (~150 ms) et l'API ne l'inclut pas. Les deux mesures ne répondent pas à la même question.
- **La restitution canonique** vaut 1,0000 **par construction** : les jetons viennent des
  spans, qui sont des sous-chaînes de la source. C'est un invariant de codec, pas une
  compréhension sémantique ; il n'y a **pas de gold de forme canonique**.
- **Le schéma** valide la **forme** (types, énumérations, champs obligatoires), pas le sens :
  les 8 champs présents ne prouvent pas que `langue`, `refus` ou `unites_semantiques` sont
  linguistiquement justes.
- **Le F1 0,7902** est mesuré sur le **gold vivant de 612 phrases**, pas sur les 50 textes :
  il identifie le **code** de la semaine, il ne note pas la qualité des 50 textes.

## 9. La suite

1. **J11.4 — le schéma v2 documenté** : la dernière tâche produit de la semaine.
2. **Trancher `g017`** (convention de l'adverbe final), puis **T132/T133** et le **gold 200+**.
3. **Un test de non-régression sur les 8 champs des 50 textes** : `test_produit_libre.py`
   couvre les chevauchements, `test_schema_produit.py` couvre 6 textes ; ajouter les 50
   textes au test de schéma figerait le contrat sur le banc libre.
4. **Décider le défaut produit** : `alternative` (fidèle, 115 paires documentées) ou
   `filtrer` (linéaire, 0 paire). La mesure ne tranche pas la politique, elle chiffre les
   deux choix.

## 10. Fichiers

- [`pensee-robustesse-semaine.json`](pensee-robustesse-semaine.json) — les 50 résultats par
  texte, la synthèse, la comparaison A26 et les contrôles.
- [`tools/mesurer_robustesse_semaine.py`](../tools/mesurer_robustesse_semaine.py) — le banc
  reproductible (`python3 tools/mesurer_robustesse_semaine.py`).
- [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json) — le banc des 50 textes
  (audit A26).
- [`rapport-fiabilite-produit.md`](rapport-fiabilite-produit.md) — l'audit A26.
- [`rapport-restitution-v1.md`](rapport-restitution-v1.md) · [`pensee-restitution-v1.json`](pensee-restitution-v1.json)
  — la restitution v1 de référence.
- [`rapport-schema-v2.md`](rapport-schema-v2.md) · [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json)
  — le schéma v2.
- [`rapport-re-test-produit.md`](rapport-re-test-produit.md) — le re-test B13 du 06/11
  (405/145 en forçant `fr`) ; la mesure J11.3 est en langue auto (395/115) et sur le code
  J11.2.
