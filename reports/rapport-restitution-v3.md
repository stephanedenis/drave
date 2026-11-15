# B13 — la restitution v3 : les rôles des GP se séparent, la fidélité du cadre ne suit pas

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : W5 (J3 après-midi) · **Date** :
> 2026-11-15 · **Verdict** : **positif sur la séparation, négatif sur le produit** — les
> cinq rôles de GP se séparent sur le gold S (**18/18**, **144/144**, permutation **0/18**),
> mais le gold v2 ne gagne qu'un cadre : **20/46** contre 19/46, F1 **0,5406** contre
> 0,5270, `lieu` F1 **0,60** contre 0,40. La fidélité du cadre ne suit pas : le goulot est
> la segmentation et le choix du cadre, pas la préposition.
>
> **La question.** La v2 lisait la préposition seule (`à` → destinataire, `de` → thème,
> `avec` → moyen) ; le `lieu` restait son rôle le plus faible (F1 0,4000). La v3 peut-elle
> distinguer **lieu / temps / destinataire / possession / complément** avec le contexte, et
> la précision/rappel par rôle le montrent-ils sur les deux ors existants — le gold v2
> (46) et le gold S (61 phrases, 144 rôles) — sans que la mesure soit un rôle constant ?
>
> **La réponse.** Oui pour la **règle** : `_role_gp` sépare les cinq catégories avec le
> contexte (ce qui suit la préposition, ce qui la précède), **24/24** cas de séparation,
> et le gold S passe de **139/144** à **144/144** (`cinq rôles 17/18 → 18/18`). Non pour le
> **produit** : sur le gold v2, la règle ne corrige que le `lieu` (`3/6` au lieu de `2/6`)
> et un cadre (`20/46` au lieu de `19/46`) ; le reste est inchangé. Le **contrôle négatif**
> tue bien la mesure : permutation des cinq rôles → **0/18**, permutation de tous les rôles
> → **0,4028** global, rôle constant `lieu` → **0,0208**. Le 144/144 n'est pas un gain de
> rôles seul : le découpage donne **+4 rôles** et **+1 appariement**.
>
> **Le chiffre.** Gold v2 : **20/46** cadres exacts (**17** non vides), **F1 0,5406**,
> `lieu` **3/6** (P 0,75, R 0,50, F1 0,60), `agent` 0,6000, `prédicat` 0,4872. Gold S :
> **144/144**, cinq rôles **18/18** (lieu 3, temps 9, destinataire 5, possession 1,
> complément 0), permutation cinq **0/18**, constante **3/18**, séparation **24/24**.
>
> **Dispositif** : [`roles_gp.py`](../tools/roles_gp.py) (la règle),
> [`restitution_v3.py`](../tools/restitution_v3.py) (`preparer_annotation`, `apparier`,
> `mesurer_banc_v3`, `mesurer_gold_analyseur_v3`, `mesurer_separation`),
> [`drave.py`](../tools/drave.py) (`restituer --roles-v3`),
> [`mesurer_restitution_v3.py`](../tools/mesurer_restitution_v3.py) ;
> JSON [`pensee-restitution-v3.json`](pensee-restitution-v3.json) ;
> gold v2 [`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) ;
> gold S [`gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json) ;
> tests [`test_restitution_v3.py`](../tools/tests/test_restitution_v3.py) ; fiche v2
> [`rapport-restitution-v2.md`](rapport-restitution-v2.md).

## 1. La commande

```bash
python3 tools/drave.py restituer "Le train part à 14 h." --roles-v3
```

```
restitution v3 (rôles de GP)
source          : 'Le train part à 14 h.'
cadre principal :
  agent         : Le train
  prédicat      : part
  lieu          : —

rôles (agent, prédicat, lieu)
  agent     : Le train
  prédicat  : part
  lieu      : —
  autres    : temps: à 14 h
segments de rôle : 2
   1. GN/agent [0:8] « Le train » → part
   2. GV/predicat [9:13] « part » → train

rôles de GP (v3) : temps: 1

restitution du rendu : exacte (relire_roles(rendre_roles(a)))
contrôle négatif      : retrait détecté · permutation détectée · détecté True
```

Le mode banc mesure les rôles contre l'or :

```bash
python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --roles-v3 --json
```

`--roles` reste la **v2** (inchangée, 19/46, F1 0,5270) ; `--roles-v3` est le mode v3 ;
les deux sont exclusifs, comme `--canonique`. `--gold` sert aux deux modes de banc.

La règle se lit seule :

```python
from tools.roles_gp import role_gp
role_gp("à", "la maison")                    # lieu
role_gp("à", "14 h")                         # temps
role_gp("à", "Marie")                        # destinataire
role_gp("de", "la voisine", "GN")            # possession
role_gp("de", "son projet", "GV")            # theme
role_gp("avec", "le télescope")              # moyen
role_gp("par", "Marie", "GV", "a été écrit") # agent
role_gp("par", "la porte", "GV", "il entre") # moyen
```

## 2. Ce que la v3 ajoute

La v2 appelait `_role_gp(prep)` : la préposition **seule**. La v3 appelle la même fonction
avec le **contexte** — `suivant` (ce qui suit la préposition dans le GP), `precedent` (le
type du syntagme précédent, `GN` ou `GV`) et `precedent_texte` (pour le passif) :

| préposition | contexte | rôle v3 |
|---|---|---|
| `à` | `la maison`, `Paris` | `lieu` |
| `à` | `14 h`, `demain`, `9` | `temps` |
| `à` | `Marie`, `son fils` | `destinataire` |
| `à` | `manger`, `faire` | `but` |
| `à` + copule | `moi`, `lui` | `possession` (`Le livre est à moi`) |
| `de` | après un `GN` | `possession` (`le chat **de la voisine**`) |
| `de` | après un `GV` | `theme` (`parler **de son projet**`) |
| `avec` | — | `moyen` (le gold S dit `instrument`) |
| `par` | après un passif | `agent` (`écrit **par Marie**`) |
| `par` | sinon | `moyen` (`entrer **par la porte**`) |
| `dans`, `sur`, `vers`… | lieu | `lieu` |
| `dans`, `sur`, `vers`… | temps (`vers 9 h`, `dans 3 jours`) | `temps` |
| `en` | `2020` / `France` / `voiture` / `-ant` | `temps` / `lieu` / `moyen` / `maniere` |
| `over`, `to`, `at` | `the lazy dog` / `Mary` / `9` | `lieu` / `destinataire` / `temps` |

Deux corrections de **préparation** accompagnent la règle :

1. **Dédoublonnage** des GP de même début. L'union S + chunker produit parfois `vers` et
   `vers 9 h`, ou `de la voisine` et `de la voisine dort`. Règle : si le plus court est
   **nu** (une préposition seule), on garde le plus long ; sinon on garde le plus court, le
   plus précis. Sans cela, le GP `vers` (nu) restait `lieu` et le GP `de la voisine dort`
   avalait le verbe.
2. **Rôle recalculé** sur le GP gardé, avec le syntagme précédent. Les GP qui ne commencent
   pas par une préposition connue (`hier`, `demain`) gardent le rôle de l'analyseur.

La v3 ne touche ni à l'analyseur par défaut, ni à la v2, ni au générateur S. C'est une
**vue** préparée sur l'annotation, comme la v2 ; le mode `--roles-v3` est opt-in.

## 3. Les deux ors

### 3.1 Le gold v2 (46 textes)

[`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) :
**46 cadres**, **65 variantes**, un cadre principal par texte, écrit à la main. Il n'annote
que **`agent`, `prédicat`, `lieu`** — pas les cinq rôles de GP. C'est un or de **cadre
principal**, écrit après avoir vu les sorties de la v2 (biais nommé). Les textes sans
prédicat ont un cadre vide.

Conséquence : sur ce banc, la v3 ne peut mesurer que `agent`, `prédicat`, `lieu`. Les cinq
catégories de la tâche n'y sont **pas** annotées ; leur mesure vient du gold S.

### 3.2 Le gold S (61 phrases, 144 rôles)

[`gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json) : **61 phrases**,
**144 rôles**, **17 étiquettes** de rôle. Les cinq catégories de la tâche y ont **18
occurrences** :

| rôle | occurrences |
|---|---:|
| `lieu` | 3 |
| `temps` | 9 |
| `destinataire` | 5 |
| `possession` | 1 |
| `complément` | **0** |

C'est un or de la **même famille de règles**, écrit avant la v3 ; ce n'est pas une
validation humaine indépendante. Un score parfait sur 18 items est une preuve faible, et
`complément` n'est pas mesuré du tout par l'or.

### 3.3 Les cas de séparation (24)

[`roles_gp.CAS_SEPARATION`](../tools/roles_gp.py) : **24 cas** écrits pour couvrir les
distinctions que l'or ne couvre pas (surtout `complément`, `par` passif, l'anglais). Ce sont
des **tests de règle**, pas un or : ils montrent que la fonction ne renvoie pas un rôle
constant, ils ne remplacent pas une annotation.

## 4. Les chiffres

### 4.1 Gold v2 : le cadre principal

| mesure | v2 | v3 | Δ |
|---|---:|---:|---:|
| textes du banc / annotés / refus | 50 / 46 / 4 | 50 / 46 / 4 | — |
| cadres exacts | **19/46 = 0,4130** | **20/46 = 0,4348** | **+1** |
| dont non vides | **16/46 = 0,3478** | **17/46 = 0,3696** | **+1** |
| dont vides | 3 | 3 | 0 |
| cadres partiels | 42/46 = 0,9130 | 43/46 = 0,9348 | +1 |
| cadres exacts stricts (1re variante) | 16/46 = 0,3478 | 17/46 = 0,3696 | +1 |
| rôles exacts (cellules) | 91/138 = 0,6594 | **93/138 = 0,6739** | +2 |
| rôles justes / attendus | 39/77 | **40/77** | +1 |
| rôles prédits | 71 | 71 | 0 |
| précision | 0,5493 | **0,5634** | +0,0141 |
| rappel | 0,5065 | **0,5195** | +0,0130 |
| **F1** | **0,5270** | **0,5406** | **+0,0136** |
| faux positifs / faux négatifs | 32 / 38 | **31 / 37** | −1 / −1 |

Le seul rôle qui bouge est le **lieu** :

| rôle | attendus | prédits | justes | précision v2 → v3 | rappel v2 → v3 | F1 v2 → v3 |
|---|---:|---:|---:|---:|---:|---:|
| **agent** | 32 | 28 | 18 | 0,6429 → 0,6429 | 0,5625 → 0,5625 | 0,6000 → 0,6000 |
| **prédicat** | 39 | 39 | 19 | 0,4872 → 0,4872 | 0,4872 → 0,4872 | 0,4872 → 0,4872 |
| **lieu** | 6 | 4 | **2 → 3** | **0,5000 → 0,7500** | **0,3333 → 0,5000** | **0,4000 → 0,6000** |

Deux corrections expliquent le gain :

- `f20` (« … sont arrivés **vers 9 h**. ») : `vers 9 h` était `lieu` (faux positif) ; le
  contexte temporel en fait `temps`, le faux positif disparaît.
- `f35` (« The quick brown fox jumps **over the lazy dog**. ») : `over` n'était pas dans le
  lexique de lieu et tombait en `complément` ; il devient `lieu`, le cadre passe de 2/3 à
  3/3.

Les trois `lieu` encore manqués ne sont **pas** des erreurs de préposition :

| texte | or | pourquoi la règle ne peut pas le corriger |
|---|---|---|
| `f08` | `Where` | pas de GP produit ; `Where` n'est pas une préposition |
| `f24` | `au bord de la forêt` | le cadre principal est `Il / était`, pas `une petite fille / vivait` |
| `f49` | `salle B12` | `salle B12` est un GN nu, pas un GP ; `à demain` est un temps |
| `f50` | — | cadre principal faux (`il / Notes`), pas un problème de rôle |

Le `lieu` de `f50` (`dans la cour`) est un faux positif qui reste : la phrase a plusieurs
paragraphes et le cadre principal est mal choisi.

### 4.2 Gold S : la précision et le rappel par rôle

Mesure v3 (rôles v3, appariement v3) : **144/144 = 1,0000**.

| rôle | attendus | prédits | justes | précision | rappel | F1 |
|---|---:|---:|---:|---:|---:|---:|
| `agent` | 34 | 34 | 34 | 1,0000 | 1,0000 | 1,0000 |
| `prédicat` | 58 | 58 | 58 | 1,0000 | 1,0000 | 1,0000 |
| `patient` | 5 | 5 | 5 | 1,0000 | 1,0000 | 1,0000 |
| `qualite` | 7 | 7 | 7 | 1,0000 | 1,0000 | 1,0000 |
| `contenu` | 5 | 5 | 5 | 1,0000 | 1,0000 | 1,0000 |
| `cause` | 4 | 4 | 4 | 1,0000 | 1,0000 | 1,0000 |
| `but` | 3 | 3 | 3 | 1,0000 | 1,0000 | 1,0000 |
| `hypothese` | 2 | 2 | 2 | 1,0000 | 1,0000 | 1,0000 |
| `concession` | 1 | 1 | 1 | 1,0000 | 1,0000 | 1,0000 |
| `consequence` | 1 | 1 | 1 | 1,0000 | 1,0000 | 1,0000 |
| `maniere` | 1 | 1 | 1 | 1,0000 | 1,0000 | 1,0000 |
| `moyen` | 1 | 1 | 1 | 1,0000 | 1,0000 | 1,0000 |
| `theme` | 4 | 4 | 4 | 1,0000 | 1,0000 | 1,0000 |
| **`lieu`** | **3** | **3** | **3** | **1,0000** | **1,0000** | **1,0000** |
| **`temps`** | **9** | **9** | **9** | **1,0000** | **1,0000** | **1,0000** |
| **`destinataire`** | **5** | **5** | **5** | **1,0000** | **1,0000** | **1,0000** |
| **`possession`** | **1** | **1** | **1** | **1,0000** | **1,0000** | **1,0000** |
| **`complément`** | **0** | **0** | **0** | — | — | — |
| **les cinq** | **18** | **18** | **18** | **1,0000** | **1,0000** | **1,0000** |

Le zéro de `complément` est un **trou d'or**, pas une performance : la catégorie n'est pas
mesurée. `moyen` lit l'`instrument` du gold S (1 occurrence) ; la normalisation est publiée
dans `roles_gp.normaliser_role`. Le 18/18 est la seule mesure des cinq rôles sur un or ; les
24 cas de séparation sont le supplément.

### 4.3 Le découpage : rôles ou appariement ?

Le 144/144 mélange deux leviers. Le JSON les sépare en rejouant les quatre combinaisons :

| rôles | appariement | global | cinq rôles | F1 cinq |
|---|---|---:|---:|---:|
| v2 | v2 (ancien) | 139/144 | 17/18 | 0,8947 |
| v2 | v3 (span le plus court) | 142/144 | 18/18 | 0,9730 |
| v3 | v2 (ancien) | 143/144 | 18/18 | 0,9730 |
| **v3** | **v3** | **144/144** | **18/18** | **1,0000** |

- **Gain de rôles** (v2 → v3, appariement v2) : **+4** rôles globaux, **+1** rôle des cinq.
  Les quatre corrigés par la **préparation v3** sont `p002` (`avec` : `attribut` → `moyen`),
  `p005` (`de son projet` : `destinataire` → `theme`), `g019` (`à Marie` : `theme` →
  `destinataire`) et `h060` (`des bonds` : `possession` → `theme`). Deux le sont par le
  **dédoublonnage** (`p005`, `g019`, le GP long avalait le second), deux par la **règle**
  (`p002`, `h060`).
- **Gain d'appariement** (v3, v2 → v3) : **+1** rôle global (`h056`, le SUB long), **0**
  rôle des cinq. Le gain est un gain de **mesure**, pas de règle.
- Le **+1 des cinq** est une **interaction** : le rôle v3 et l'appariement corrigent le même
  `destinataire` (`g019`). Selon l'ordre du découpage, il est attribué aux rôles (v3 + v2
  appariement, 18/18) ou à l'appariement (v2 rôles + v3 appariement, 18/18). Les quatre
  combinaisons sont publiées pour que le lecteur voie l'interaction, pas un gain unique.

Sans ce découpage, le 144/144 ferait croire à un gain de rôles de +5 ; il est de **+4**, et
le +1 restant vient du tie-break du span le plus court. Le chiffre v2 139/144 a été produit
avec l'ancien appariement : c'est la référence correcte.

### 4.4 Les cas de séparation

**24/24**. Les cas qui portent la distinction de la tâche :

| cas | entrée | rôle |
|---|---|---|
| `à` + lieu | `à` + `la maison`, `Paris` | `lieu` |
| `à` + temps | `à` + `14 h`, `demain` | `temps` |
| `à` + destinataire | `à` + `Marie` | `destinataire` |
| `à` + infinitif | `à` + `manger` | `but` |
| `de` + GN | `de` + `la voisine`, précédent `GN` | `possession` |
| `de` + GV | `de` + `son projet`, précédent `GV` | `theme` |
| `avec` | `avec` + `le télescope` | `moyen` |
| `par` passif | `par` + `Marie`, précédent `a été écrit` | `agent` |
| `par` moyen | `par` + `la porte`, précédent `il entre` | `moyen` |
| `en` temps / lieu / moyen / manière | `2020` / `voiture` / `haussant` | `temps` / `lieu` / `moyen` / `maniere` |
| anglais | `over the lazy dog`, `to Mary`, `to the station`, `at 9`, `at home` | `lieu`, `destinataire`, `lieu`, `temps`, `lieu` |

### 4.5 Le contrôle négatif : permuter les rôles tue la mesure

**Sur le gold v2 (46)** :

| contrôle | cadres exacts | rôles justes | F1 |
|---|---:|---:|---:|
| **vide** (aucun rôle) | 7/46 | 0/77 | 0,0000 |
| **constant par type** (GN=agent, GV=prédicat, GP=lieu) | 6/46 | 39/77 | 0,4382 |
| **rôles mélangés** (agent←prédicat←lieu←agent) | 3/46 | 0/77 | 0,0000 |
| **permutation des cinq rôles de GP** | 17/46 | 37/77 | 0,5139 |
| **v3** (le lecteur) | **20/46** | **40/77** | **0,5406** |

La permutation des cinq rôles fait tomber le `lieu` à **0/6** (P 0, R 0, F1 0) : le rôle
cible est mort, même si les rôles hors GP (agent, prédicat) ne bougent pas. Les cadres
tombent de 20 à 17, les non vides de 17 à 14. Le mélange des trois rôles du cadre tombe à
3/46, comme en v2.

**Sur le gold S (144)** :

| contrôle | global | cinq rôles | F1 cinq |
|---|---:|---:|---:|
| **v3** | **144/144 = 1,0000** | **18/18** | **1,0000** |
| **permutation des cinq** (lieu→temps→destinataire→possession→complément→lieu) | 0,8750 | **0/18** | **0,0000** |
| **permutation de tous les rôles** (rotation) | **0,4028** | **0/18** | **0,0000** |
| **rôle constant `lieu`** (tous les GP) | **0,0208** | **3/18** | **0,0370** |
| **constant par type** (le plancher v2) | 0,7222 | — | — |

La permutation des cinq laisse le global à 0,8750 parce qu'elle ne touche que 18 des 144
rôles ; mais la mesure **des cinq** tombe à 0/18. La permutation de **tous** les rôles tue
aussi le global (0,4028). Le rôle constant `lieu` donne 3/18 (les trois lieux de l'or) et
un F1 de 0,037. La mesure dépend donc de l'affectation des rôles, pas d'une étiquette
décorative ni d'un rôle constant déguisé.

## 5. Pourquoi le produit ne suit pas

### 5.1 Le gold v2 n'annote pas les cinq rôles

Le seul rôle de GP annoté dans les 46 textes est `lieu` (6 attendus). Les GP lus par la v3
sur ce banc se répartissent en `lieu` 10, `temps` 13, `destinataire` 6, `possession` 5,
`moyen` 5, `theme` 17, `but` 7, `maniere` 3, `agent` 1 : les cinq rôles de la tâche en
comptent **34**, et **aucun** de ces rôles hors `lieu` n'a d'or. Le gain
mesurable est donc structurellement limité à `lieu`.

### 5.2 La segmentation et le cadre pèsent plus que la préposition

Les erreurs qui restent sur les 46 ne sont pas des erreurs de rôle :

- `f08` : aucun GP n'est produit ; `Where` n'est pas une préposition.
- `f24` : le cadre principal est `Il / était`, pas l'événement `une petite fille / vivait`.
- `f49` : `salle B12` est un GN nu, pas un GP ; `à demain` est correctement un temps.
- `f50` : le cadre principal est `il / Notes`, sur un texte de 2 144 caractères.
- `f20` : `vers 9 h` est corrigé, mais l'agent (`Leroy`) et le prédicat (`M`) restent faux.
- `f27` (« Élodie sourit. ») : aucun syntagme, cadre vide.

La règle de rôle ne peut pas créer un GP absent, choisir le bon cadre principal ni réparer
un GV trop court. C'est la même conclusion que la v2, et la v3 ne la change pas.

### 5.3 Le dédoublonnage a un coût

Quand deux GP de même début existent, la v3 garde le plus court sauf si le plus court est
nu. C'est ce qui évite `de la voisine dort` et `à Marie de son projet`, mais cela jette
parfois un GP long correct (`sur le toit de la maison` → `sur le toit`). Le choix est publié
et assumé pour la précision ; il pourra être revu avec un or de spans.

## 6. Ce qui pourrait rendre cette fiche fausse

- **L'or S** : 61 phrases, 144 rôles, de la même famille de règles, écrit avant la v3. Le
  144/144 n'est pas une validation humaine indépendante ; un or aveugle donnerait moins.
- **Les cinq rôles** : 18 occurrences, 0 `complément`. Le 18/18 est un score sur 18 items ;
  il ne prouve pas la catégorie `complément` et ne tient pas compte des rôles hors or.
- **Les lexiques** : temps, lieux et personnes ont été écrits en lisant le gold S. C'est un
  biais nommé ; un autre lexique changerait les chiffres, surtout `à` + nom propre.
- **Le découpage** : le 144/144 dépend du tie-break du span le plus court. Avec l'ancien
  appariement, la v3 donne 143/144. Le gain de rôles seul est +4 ; le +1 restant est un
  gain de mesure.
- **Le dédoublonnage** : garder le plus court (sauf préposition nue) est un choix. Un autre
  choix changerait les spans et peut-être les cadres.
- **Le cadre principal** : « premier prédicat qui porte un agent ou un lieu » favorise les
  cadres complets tardifs et désavantage les cadres simples précoces (`f50`). C'est une
  convention, pas une vérité.
- **Le banc** : 46 textes écrits à la main (audit A26), pas un échantillon aléatoire ; le
  banc mêle français, anglais et `und`, et `agent` n'a pas la même définition dans les trois.
- **Le codec** : 46/46 sur `relire_roles(rendre_roles(a))` est exact par construction ; il
  ne mesure pas la fidélité. Les 194/194 spans sont des sous-chaînes exactes, pas des spans
  corrects.
- **La mesure ouverte** : l'appariement n'apparie que les spans d'or ; les spans prédits en
  trop ne sont pas comptés comme faux positifs. La précision par rôle est donc une
  précision **conditionnelle aux spans appariés**, pas une précision open-world.

## 7. Ce que la v3 ne dit pas

- **Les cinq rôles sur les 46** : le gold v2 ne les annote pas ; la mesure des cinq n'existe
  que sur le gold S (18 items) et les 24 cas synthétiques.
- **Le rôle par défaut** : `--roles` reste la v2. La v3 est un mode opt-in ; elle ne change
  pas le produit par défaut. Le gain sur le gold v2 (+1 cadre) ne paie pas une régression
  de format.
- **La qualité des spans** : la v3 corrige des rôles, pas la segmentation. Elle ne dit pas
  si `de la voisine` est un bon span (il l'est ici), ni si `à Paris dure deux heures` en est
  un (non).
- **Les subordonnées** : le gold v2 ne note qu'un cadre par texte ; une relative correcte
  dans une phrase dont le cadre principal est faux ne compte pas.
- **La généralité** : 46 textes + 61 phrases, ce n'est pas un corpus de production.

## 8. La suite

1. **J4 — l'or de rôles** : annoter les seconds cadres et les rôles hors cadre, plusieurs
   phrases par texte, avec double codage ; c'est le prochain banc de la v3.
2. **Le `complément`** : ajouter des cas à l'or (aujourd'hui zéro) pour mesurer le repli.
3. **La segmentation** : les nombres dans les GP (`à 14 h`), la frontière du verbe
   (`de la voisine | dort`), les GP nus et le cadre principal.
4. **Le défaut** : ne passer `--roles` en v3 que si le gold v2 progresse au-delà du bruit ;
   en attendant, `--roles-v3` est mesuré et la v2 reste reproductible.
5. **Le contrôle externe** : garder le gold S 144/144 comme non-régression de la règle,
   avec le découpage rôles/appariement.

## 9. Fichiers

- [`roles_gp.py`](../tools/roles_gp.py) — `role_gp`, `est_preposition`, `CAS_SEPARATION`.
- [`restitution_v3.py`](../tools/restitution_v3.py) — `preparer_annotation`, `apparier`,
  `apparier_v2`, `mesurer_banc_v3`, `mesurer_gold_analyseur_v3`, `mesurer_separation`,
  `controler_banc_v3`.
- [`drave.py`](../tools/drave.py) — `restituer --roles-v3`, `--gold`, JSON v3.
- [`mesurer_restitution_v3.py`](../tools/mesurer_restitution_v3.py) — produit le JSON.
- [`test_restitution_v3.py`](../tools/tests/test_restitution_v3.py) — 29 tests.
- [`pensee-restitution-v3.json`](pensee-restitution-v3.json) — les 46 résultats, le gold S,
  les contrôles, le découpage, les limites.
- [`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) — l'or
  v2 (46 cadres).
- [`gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json) — l'or S
  (61 phrases, 144 rôles).
- [`rapport-restitution-v2.md`](rapport-restitution-v2.md) — la fiche v2, dont les chiffres
  restent la référence du mode `--roles`.
