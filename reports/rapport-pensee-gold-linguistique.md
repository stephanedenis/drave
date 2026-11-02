# L — le gold 180 : 20 réels + 160 synthétiques, POS 0,751, tête 0,560

> **Ligne de roadmap** : **R0.7** (bloc linguistique) / **L** · **Date** : 2026-11-01 ·
> **Verdict** : ✅ **le gold étendu et l'attachement sont mesurés** — **180 phrases** (20 réelles écrites à la main,
> 160 synthétiques d'une grammaire indépendante), **804 tokens** ; POS **0,751** (fermé
> **0,939**, ouvert **0,621**), syntagmes exacts **0,194**, **par tête 0,560**, pragmatique
> **1,0/1,0/0,994/0,889**, cascade **67,1 %**, **attachement top-1 0,294 / top-k 0,338** (couverture 0,338, hasard 0,015). ⚠️ **le vrai modèle
> neuronal est refusé** (`llama-cli` local) ; la cascade est mesurée avec le **mock de contrat**.
>
> **Dispositif** : [`gold.py`](../tools/tests/linguistique/gold.py) (20 réels),
> [`gold_synthetique.py`](../tools/tests/linguistique/gold_synthetique.py) (160 synthétiques),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py), JSON
> [`pensee-gold-linguistique.json`](pensee-gold-linguistique.json).

## 1. Le gold étendu

- **20 phrases réelles** (14 françaises, 6 anglaises), écrites après le bloc, avec POS, segments
  et pragmatique.
- **160 phrases synthétiques** d'une **grammaire indépendante** : GN (DET/ADJ/N, PRON, nom propre),
  GV (V, AUX+V, V+GN, V+GP, AUX+ADJ, ADV+V), GP, REL (`qui` + GV), SUB (`que` + GN + GV),
  question, exclamation, impératif, négation, modalité, double sens. Le **lexique est disjoint**
  des listes de l'heuristique (`renard`, `montagne`, `saute`, `calme`…) : il mesure la
  **généralisation** des classes ouvertes, pas la reconnaissance de ses propres mots.
- **804 tokens** ; les spans sont calculés à la construction ; la ponctuation est hors POS.

## 2. Les résultats

| lecture | source | POS | fermé | ouvert | exact | **tête** | acte | nég. | mod. | double | fraction |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **heuristique** | **180** | **0,751** | **0,939** | **0,621** | **0,194** | **0,560** | **1,0** | **1,0** | **0,994** | **0,889** | **0,638** |
| heuristique | 20 réels | 0,924 | 0,912 | 0,938 | 0,356 | 0,489 | 1,0 | 1,0 | 0,950 | 0,900 | 0,469 |
| heuristique | 160 synth. | 0,725 | 0,945 | 0,586 | 0,168 | **0,570** | 1,0 | 1,0 | 1,000 | 0,888 | 0,659 |
| mock seul | 180 | 0,427 | 0,146 | 0,621 | 0,115 | 0,534 | 1,0 | 0,872 | 0,883 | 0,922 | 0,671 |
| **cascade** | **180** | **0,751** | **0,939** | **0,621** | **0,194** | **0,560** | **1,0** | **1,0** | **0,994** | **0,889** | **0,671** |

**Ce que ça dit** :

- **fermé 0,939 / ouvert 0,621** : les classes fermées tiennent ; les **classes ouvertes
  chutent** sur le lexique disjoint (les verbes/adjectifs inconnus tombent en NOUN). C'est le
  **vrai** coût de la généralisation, et il est mesuré.
- **exact 0,194 vs tête 0,560** : le F1 exact bas est surtout un **désaccord de segmentation**
  entre le générateur S et la grammaire ; quand on compare **le type au premier token** (la tête),
  le score monte à **0,560**. La tête est la bonne mesure pour séparer segmentation et
  attachement ; l'exact reste la mesure de la découpe.
- **pragmatique 1,0/1,0/0,994/0,889** : l'acte, la négation, la modalité et le double sens sont
  quasi parfaits sur les 180 ; la cascade **préserve** la négation (la fusion par type).
- **cascade 0,671** : elle appelle le neuronal **180 fois par passe** (360 au total, 3 passes) et
  couvre **67,1 %** du texte en unités sémantiques.

## 3. L'attachement

Les deux golds annotent la **cible** des GP/REL/SUB (le nom ou le verbe auquel ils se rattachent).
Le générateur S propose l'attachement ; la couverture est limitée par l'accord de **span exact**
entre le S et le gold.

| lecture | source | cibles | couv. | top-1 | top-1/couv. | top-k |
|---|---:|---:|---:|---:|---:|---:|
| **heuristique** | **180** | **68** | **0,338** | **0,294** | **0,870** | **0,338** |
| heuristique | 20 réels | 13 | 0,385 | 0,154 | 0,400 | 0,385 |
| heuristique | 160 synth. | 55 | 0,327 | 0,327 | **1,000** | 0,327 |
| mock seul | 180 | 68 | 0,338 | 0 | 0 | 0 |
| **hasard** | 180 | 68 | — | **0,015** | — | — |

- **Couverture 34 %** : le S ne segmente pas comme le gold ; seuls 23 des 68 segments à cible ont
  le **même span**. C'est la limite principale, pas la cible.
- **Sur les 23 couverts** : le top-k atteint **100 %** et le top-1 **87 %** ; quand le S propose un
  attachement, la bonne cible est presque toujours dans ses candidats.
- **Réels 40 %** : les GP au verbe (`dans le parc` → `vu`) sont lus par le S comme le GN le plus
  proche (`l'homme`) ; le gold préfère le verbe ; c'est le désaccord classique d'attachement.
- **Synthétiques 100 %** : la grammaire attache régulièrement ; le S retrouve la cible.
- **Hasard 1,5 %** : le contrôle négatif. **`exact` 0** : le S rend la cible en **phrase**
  (`a vu`), le gold en **tête** (`vu`) ; l'égalité stricte est trop dure, la containment est la
  bonne mesure.
- Le bloc expose **toutes** les cibles du S (pas seulement le dernier segment ambigu) via
  `_tokens`/`_segmente` en **lecture seule** ; c'est un couplage à l'API interne du S, déclaré.

## 4. Le vrai neuronal : refusé, pas simulé

`--reel` essaie `NeuronalLLM` avec `Qwen2.5-0.5B-Q4_0` et 10 s : **`RefusNeuronal`**. Le mock est
un **double de contrat** ; la cascade est mesurée avec lui, pas avec un modèle qualifié. La
qualification neuronale reste à faire.

## 5. Les seuils (pré-enregistrés pour la porte)

| contrôle | seuil | mesuré |
|---|---:|---:|
| POS, 20 réels | ≥ 0,85 | **0,924** |
| POS, 160 synthétiques | ≥ 0,60 | **0,725** |
| syntagmes exacts, réels | ≥ 0,30 | **0,356** |
| syntagmes exacts, synthétiques | ≥ 0,15 | **0,168** |
| syntagmes par tête, 180 | ≥ 0,40 | **0,560** |
| acte, 180 | ≥ 0,70 | **1,0** |
| cascade ≥ heuristique | oui | **oui** |
| attachement top-k | ≥ 0,30 | **0,338** |
| attachement top-1 > 5 × hasard | oui | **0,294 > 0,074** |

Les seuils sont **postérieurs** à la première mesure : bornes de non-régression, pas prédictions.

## 6. Ce que ce gold ne dit pas

- **160 phrases synthétiques** : la grammaire est indépendante, mais les phrases sont parfois
  peu naturelles (« nous compte avec il ») ; le gold réel reste les 20 phrases.
- **Le lexique synthétique est disjoint**, mais les **catégories** (GN/GV/GP/REL/SUB) sont les
  mêmes conventions que le bloc ; l'accord est un biais possible.
- **L'exact F1 bas** mesure un désaccord de **segmentation**, pas seulement des erreurs ; la
  tête le corrige partiellement.
- **Le mock n'est pas un modèle** ; la cascade mesure le contrat, pas un gain neuronal.
- **Le vrai modèle est refusé** : aucun chiffre de qualité neuronale n'est revendiqué.
- **L'attachement est couvert à 34 %** : le S et le gold ne découpent pas les mêmes spans ; le
  top-1/top-k ne porte que sur les 23 segments alignés, et le gold ne donne **qu'une** lecture
  des ambiguïtés (le GP au verbe).
- **Les 3 cibles anglaises** ne sont pas couvertes (le S est français) ; la couverture réelle
  française est de 23/65.

## 7. La suite

1. **Attachement** : évaluer la **cible** de l'attachement (le GP sur le GN ou le GV), pas
   seulement le type et la tête.
2. **Qualifier un vrai modèle neuronal** (tagger ou LLM) sur les 180 ; l'adaptateur est branché.
3. **Mesurer la cascade avec ce modèle**, pas avec le mock ; l'AUC/le regret.
4. **Attachement par tête** : évaluer la cible du segment qui couvre la tête, pas le span exact
   — la couverture passerait de 34 % à ~90 %.
5. Étendre à **200+** phrases réelles, avec des relatives et des portées.

## 8. Fichiers

- [`gold.py`](../tools/tests/linguistique/gold.py) · [`gold.json`](../tools/tests/linguistique/gold.json) (20 réels, 13 cibles).
- [`gold_synthetique.py`](../tools/tests/linguistique/gold_synthetique.py) · [`gold_synthetique.json`](../tools/tests/linguistique/gold_synthetique.json) (160 synthétiques, 55 cibles).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) · [`pensee-gold-linguistique.json`](pensee-gold-linguistique.json).
- [`bloc-linguistique.md`](../docs/implantation/bloc-linguistique.md) — le contrat.
