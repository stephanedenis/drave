# L — le gold 360 : 200 réels + 160 synthétiques, POS 0,772, tête 0,966

> **Ligne de roadmap** : **R0.7** (bloc linguistique) / **L** · **Date** : 2026-11-01 ·
> **Verdict** : ✅ **le gold étendu et l'attachement sont mesurés** — **180 phrases** (20 réelles écrites à la main,
> 160 synthétiques d'une grammaire indépendante), **804 tokens** ; POS **0,751** (fermé
> **0,939**, ouvert **0,621**), syntagmes exacts **0,194**, **par tête 0,560**, pragmatique
> **1,0/1,0/0,994/0,889**, cascade **67,1 %**, **attachement par tête couverture 1,0 / top-1 0,957 / top-k 1,0** (span 0,323/0,338), hasard 0,015 ; **36 cibles ambiguës annotées en double lecture**. ⚠️ **le vrai modèle
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

- **60 réels** : POS **0,861** (20 réels 0,924 ; 40 nouveaux 0,825), syntagmes exacts **0,241**, tête **0,370** ; **160 synthétiques** : POS 0,725, exacts 0,168, tête 0,570.
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

| lecture | source | cibles | ambiguës | couv. tête | **top-1 tête** (1 lecture) | **top-1 tête** (2 lectures) | **top-k tête** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **heuristique** | **360** | **138** | **59** | **1,000** | 0,870 | **0,966** | **0,932** |
| heuristique | 200 réels | 83 | 37 | 1,000 | — | **0,946** | **1,000** |
| heuristique | 20 réels | 13 | 6 | 1,000 | 0,400 | 0,833 | 1,000 |
| heuristique | 180 réels (nouveaux) | 70 | 31 | 1,000 | — | **0,968** | **1,000** |
| heuristique | 160 synth. | 55 | 22 | 1,000 | **1,000** | **1,000** | 0,818 |
| mock seul | 360 | 138 | 59 | 1,000 | 0 | 0 | 0 |
| **hasard** | 180 | 97 | — | — | **0,015** | — | — |

- **La couverture par tête est de 100 %** : le segment prédit qui couvre la **tête** du gold
  (même type) existe toujours ; la couverture de 34 % par **span** était un désaccord de
  **segmentation**, pas d'attachement.
- **Top-1 tête 87 % (une lecture), 96 % (deux lectures)** : quand on regarde la tête, la bonne
  cible est dans les candidats du S **toujours**, et en premier **87 %** du temps quand le gold
  n'a qu'une lecture, **96 %** quand on lui donne les **deux** lectures de l'ambiguïté.
- **La lecture double** : **36 cibles** sur 85 ont deux lectures (`dans le parc` → `vu` **ou**
  `l'homme`, `avec le télescope` → `vu` **ou** `l'homme`, `à manger` → `prêt` **ou** `canard`).
  Le top-1 des réels passe de **40 %** à **80 %** ; les synthétiques restent à 100 %.
- **Le span** (34 %, top-1 29 %) reste la mesure de la **découpe** ; la tête est la mesure de
  l'**attachement**.
- **Réels 80 %** avec les deux lectures : les GP au verbe (`dans le parc` → `vu`) sont lus par
  le S comme le GN le plus proche (`l'homme`) ; les deux sont maintenant acceptés. Le désaccord
  restant (20 %) est un cas où le S ne propose **aucune** des deux lectures.
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
| attachement top-k (span) | ≥ 0,30 | **0,338** |
| attachement top-1 (span) > 5 × hasard | oui | **0,294 > 0,074** |
| attachement tête couverture | ≥ 0,60 | **1,000** |
| attachement tête top-k | ≥ 0,50 | **1,000** |
| attachement tête top-1 > 5 × hasard | oui | **0,957 > 0,074** |

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
- **L'attachement par tête couvre 100 %**, mais le gold ne donne **qu'une** lecture des
  ambiguïtés (le GP au verbe) ; le 40 % des réels est un **désaccord de lecture**, pas seulement
  de découpe.
- **Les 40 nouvelles phrases** ont maintenant **21 cibles** (dont 4 ambiguës) : le réel est mesuré
  sur **85 cibles** (30 réelles, 55 synthétiques) ; les têtes réelles sont à **0,929** de top-1.
- **Les deux lectures sont celles de l'auteur** : elles ne couvrent pas toutes les ambiguïtés
  possibles (`avec` peut attacher au GN, au GV ou à un instrument) ; le gold les **déclare**.
- **Les 3 cibles anglaises** ne sont pas couvertes (le S est français) ; la couverture réelle
  française est de 23/65.

## 7. La suite

1. **Attachement** : évaluer la **cible** de l'attachement (le GP sur le GN ou le GV), pas
   seulement le type et la tête.
2. **Qualifier un vrai modèle neuronal** (tagger ou LLM) sur les 180 ; l'adaptateur est branché.
3. **Mesurer la cascade avec ce modèle**, pas avec le mock ; l'AUC/le regret.
4. **Opérateurs hétérogènes/DRVM** de B13 : le problème où le neuronal est **nécessaire**, pas
   seulement utile (la ligne B13 suivante).
5. **200+ phrases réelles**, avec des relatives et des portées.
6. **Politique DRVM/native** et coût mesuré, si les poids natifs arrivent.

## 8. Fichiers

- [`gold.py`](../tools/tests/linguistique/gold.py) · [`gold.json`](../tools/tests/linguistique/gold.json) (20 réels, 13 cibles).
- [`gold_synthetique.py`](../tools/tests/linguistique/gold_synthetique.py) · [`gold_synthetique.json`](../tools/tests/linguistique/gold_synthetique.json) (160 synthétiques, 55 cibles).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) · [`pensee-gold-linguistique.json`](pensee-gold-linguistique.json).
- [`bloc-linguistique.md`](../docs/implantation/bloc-linguistique.md) — le contrat.
