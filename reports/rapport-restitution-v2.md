# B13 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : D2 · **Date** : 2026-11-15 ·
> **Verdict** : ❌ **négatif sur la fidélité** — la forme est fidèle (46/46), la sémantique
> ne l'est pas : **19/46 cadres exacts** (dont **16 non vides**), **F1 0,5270**, **32 faux
> positifs** et **38 faux négatifs**.
>
> **La question.** Au-delà de la surface exacte (v0 : 46/46) et de la forme canonique
> (v1 : 46/46), peut-on **restitue les rôles** — agent, prédicat, lieu — dans une forme
> lisible et **mesurer leur fidélité** sur les **46 textes annotables** de la v0 ?
>
> **La réponse.** Les rôles **se restituent** comme **forme** : un cadre principal lisible,
> 198 segments de rôle, 198/198 spans dans la source, et un rendu qui se relit à l'identique
> (**46/46**). Mais leur **fidélité au texte** n'est pas acquise : sur un or écrit à la main,
> **19/46 cadres exacts** (0,4130), **16/46 non vides** (0,3478), **91/138 cellules de rôle
> exactes** (0,6594) — mais seulement **39 justes sur 77 attendus** et **71 prédits**, soit
> **précision 0,5493 · rappel 0,5065 · F1 0,5270**. Le contrôle « rôle constant par type »
> ne fait que **6 cadres exacts** et le contrôle vide **7** : le lecteur lit donc quelque
> chose, mais **ce quelque chose n'est pas fiable**. Le contrôle externe (gold S, 61 phrases,
> 144 rôles) donne **139/144 = 0,9653** : l'instrument n'est pas cassé ; c'est le banc v0 et
> la lecture des rôles qui ne tiennent pas.
>
> **Le chiffre.** **16/46 cadres principaux non vides exacts** (0,3478) ; **F1 0,5270** ;
> **agent 0,6000**, **prédicat 0,4872**, **lieu 0,4000** ; **32 faux positifs / 38 faux
> négatifs** ; **46/46 rendus relus** ; **198/198 spans** dans la source ; **39/39**
> contrôles négatifs de rendu détectés ; **139/144** rôles sur le gold S.
>
> **Dispositif** : [`restitution_v2.py`](../tools/restitution_v2.py) (`rendre_roles`,
> `cadres`, `comparer_cadre`, `mesurer_banc_v2`), [`drave.py`](../tools/drave.py)
> (`restituer --roles`), [`mesurer_restitution_v2.py`](../tools/mesurer_restitution_v2.py) ;
> JSON [`pensee-restitution-v2.json`](pensee-restitution-v2.json) ; or
> [`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) ;
> tests [`test_restitution_v2.py`](../tools/tests/test_restitution_v2.py) ;
> banc [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json) ;
> fiches v0 [`rapport-restitution-v0.md`](rapport-restitution-v0.md) et
> v1 [`rapport-restitution-v1.md`](rapport-restitution-v1.md).

## 1. La commande

```bash
python3 tools/drave.py restituer "Le chat dort." --roles
```

```
restitution v2 (rôles)
source          : 'Le chat dort.'
cadre principal :
  agent         : Le chat
  prédicat      : dort
  lieu          : —
segments de rôle: 2 (1 agents, 1 prédicats, 0 lieux)

rôles (agent, prédicat, lieu)
  agent     : Le chat
  prédicat  : dort
  lieu      : —
segments de rôle : 2
   1. GN/agent [0:7] « Le chat » → dort
   2. GV/predicat [8:12] « dort » → chat

restitution du rendu : exacte (relire_roles(rendre_roles(a)))
contrôle négatif      : retrait détecté · permutation détectée · détecté True
```

La v0 reste la sortie par défaut, la v1 s'obtient avec `--canonique`, la v2 avec `--roles`.
Sur un banc, `--roles` mesure la fidélité à l'or :

```bash
python3 tools/drave.py restituer \
  --banc reports/pensee-fiabilite-produit.json --roles
```

`--roles --json` produit le JSON de la fiche ; `--gold CHEMIN` remplace l'or par défaut.
`--roles` et `--canonique` sont exclusifs ; `--gold` n'a de sens qu'avec `--banc --roles`.

## 2. Ce que la v2 ajoute

La v2 est une **vue** sur l'annotation, pas un second analyseur. Elle lit les syntagmes et
leur `meta` (`role`, `attachement`) et construit :

| pièce | source | rôle |
|---|---|---|
| `principal` | premier prédicat qui porte un agent ou un lieu | le cadre `agent / prédicat / lieu` |
| `cadres` | un par prédicat | l'agent le plus proche à gauche, le lieu le plus proche à droite |
| `segments` | rôles `agent`, `prédicat`, `lieu` | la liste lisible, avec span et cible |
| `autres` | les autres rôles (`patient`, `possessif`, `temps`…) | ce qui n'entre pas dans les trois rôles |
| `lisible` | les trois lignes du cadre | le format que `relire_roles` décode |

Le repli est nommé : si aucun `agent` n'est annoté, un **groupe nominal à gauche** du
prédicat sert d'agent probable (`The cat sleeps`). C'est une heuristique, pas une
annotation — et c'est une source mesurée de faux positifs.

Deux mesures sont séparées, comme le veut la règle du miroir :

- **restitution** : `relire_roles(rendre_roles(a)) == principal` — un codec, **46/46** ;
- **fidélité** : `principal == or` — une exactitude sémantique, **16/46** cadres non vides.

La première ne prouve pas la seconde. C'est le résultat de la fiche.

## 3. L'or : 46 cadres principaux, écrits à la main

Il n'existe pas d'or de rôles pour les 46 textes de la v0 : le gold S (`gold-analyseur.json`)
porte sur 61 autres phrases. La fiche ajoute donc
[`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) :
**46 cadres**, **65 variantes**, un cadre principal par texte, écrit à la main en lisant le
texte — mais **après avoir vu les sorties** : c'est un biais nommé, pas un or aveugle.

Ce que l'or note :

- les trois rôles `agent`, `prédicat`, `lieu` du **cadre principal** ;
- des **variantes complètes** pour les ambiguïtés réelles : coordination (`f22`, `f28`,
  `f36`), contraction (`f13`, `f31`, `f46`), inversion (`f19`), tête ou GN complet (`f02`,
  `f38`, `f50`), lieu plus ou moins large (`f49`) ;
- un cadre **vide** pour les textes sans prédicat (numérique, courriel, symboles, remplissage
  latin : `f18`, `f25`, `f37`, `f39`, `f40`, `f42`, `f48`).

Ce que l'or ne note pas : les subordonnées, les seconds cadres, les rôles `patient`,
`destinataire`, `moyen`, `temps`. Un cadre exact ne dit donc **pas** que tous les rôles du
texte sont justes ; un cadre faux ne dit pas que tous sont faux. C'est une mesure du
**cadre principal**, pas une annotation complète.

La comparaison est canonique (casse, ponctuation, espaces) : `Le chat` et `le chat` sont
égaux ; `C'` et `C'est` ne le sont pas. La meilleure variante est retenue pour chaque texte ;
la variante stricte (la première) est publiée à part (`exacts_stricts = 16/46`).

## 4. Les chiffres

### 4.1 Le cadre principal

| mesure | valeur |
|---|---:|
| textes du banc / annotés / refus | 50 / **46** / **4** |
| cadres exacts (toutes variantes) | **19/46 = 0,4130** |
| dont **non vides** | **16/46 = 0,3478** |
| dont vides (textes sans rôle) | 3 (`f18`, `f37`, `f40`) |
| cadres partiels (au moins un rôle) | **42/46 = 0,9130** |
| cadres exacts stricts (1re variante) | **16/46 = 0,3478** |
| rôles exacts (cellules) | **91/138 = 0,6594** |

Le **0,6594** est trompeur si on le lit seul : une cellule vide correctement vide compte
comme exacte. La mesure utile est le couple **justes / attendus** et la précision :

| mesure | valeur |
|---|---:|
| rôles justes (les deux non vides et égaux) | **39** |
| rôles attendus (or non vide) | **77** |
| rôles prédits (sortie non vide) | **71** |
| précision | **0,5493** |
| rappel | **0,5065** |
| **F1** | **0,5270** |
| faux positifs / faux négatifs | **32 / 36** |

### 4.2 Par rôle

| rôle | exacts / 46 | attendus | prédits | justes | précision | rappel | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **agent** | 29 | 32 | 28 | **18** | 0,6429 | 0,5625 | **0,6000** |
| **prédicat** | 22 | 39 | 39 | **19** | 0,4872 | 0,4872 | **0,4872** |
| **lieu** | 40 | 6 | 4 | **2** | 0,5000 | 0,3333 | **0,4000** |

L'**agent** est le rôle le mieux lu ; le **prédicat** est le plus fréquent et le plus
faux ; le **lieu** a peu d'occurrences dans l'or (6) et seulement **2** justes : les GP de
lieu sont souvent absents ou étiquetés `complément` / `destinataire` / `possession`.

### 4.3 La couverture

| mesure | valeur |
|---|---:|
| segments de rôle | **198** (`43` agents, `143` prédicats, `12` lieux) |
| cadres (un par prédicat) | **139** |
| textes avec au moins un rôle | **40/46 = 0,8696** |
| spans de rôle dans la source | **198/198 = 1,0000** |

Les 198 spans sont des sous-chaînes exactes de la source : la vue ne fabrique pas de texte.
Elle peut en revanche **fabriquer un rôle** par le repli `groupe nominal` ; c'est mesuré plus
bas.

## 5. Pourquoi la fidélité ne suit pas

### 5.1 Des rôles d'annotation déjà faux

La v2 ne ré-analyse pas : elle expose les rôles de l'annotation. Quand l'annotation se
trompe, la v2 se trompe. Exemples pris dans le JSON :

| texte | cadre prédit | or | exacts |
|---|---|---|---:|
| `f03` « Bonjour ! Comment allez-vous aujourd'hui ? » | `Comment` / `Bonjour` / — | `vous` / `allez` / — | 1 |
| `f20` « M. Dupont, le Dr Martin et Mme Leroy sont arrivés vers 9 h. » | `Leroy` / `M` / `vers 9 h` | `M. Dupont, le Dr Martin et Mme Leroy` / `sont arrivés` / — | 0 |
| `f41` « Le texte contient des accents… » | `Le texte contient` / `ß ñ ø å et` / — | `Le texte` / `contient` / — | 1 |
| `f50` (2 144 caractères) | `il` / `Notes` / `dans la cour` | `Le chat de la voisine` / `se réveille` / — | 0 |

`Bonjour` est un GV, `Comment` un agent, `M` et `Dupont` sont des prédicats : l'union
S + chunker produit des spans courts et des rôles de surface. La v2 les lit fidèlement — et
c'est précisément pourquoi elle ne peut pas être meilleure que l'annotation.

### 5.2 Des phrases simples sans syntagme

`f27` « Élodie sourit. » ne produit **aucun** syntagme : le cadre est vide, l'or attend
`Élodie / sourit` (1/3 : le lieu vide est juste). `f33` « Si tu viens, apporte le dessert. »
n'a pas de prédicat principal dans l'annotation. `f08` « Where is the nearest train
station, please? » n'a pas de cadre. Le texte est simple ; c'est le bloc qui ne le segmente
pas.

### 5.3 Le lieu est le parent pauvre

`f35` « The quick brown fox jumps over the lazy dog. » a le bon agent et le bon prédicat,
mais `over the lazy dog` est un `GP/complément`, pas un `lieu` : **2/3**. `f49` « La réunion
est reportée à demain, 10 h 30, salle B12. » a le bon agent et le bon prédicat, mais le GP
est `destinataire` : **2/3**. Le rôle `lieu` n'est pas produit par la règle `_role_gp` pour
ces prépositions.

### 5.4 Le cadre principal est un choix

Le cadre principal est le **premier prédicat qui porte un agent ou un lieu**. Sur `f50`, ce
n'est pas la phrase principale : le titre `Notes` ouvre un GV, et le premier cadre complet
est plus loin. Sur `f24` (« Il était une fois une petite fille qui vivait… »), le premier
prédicat `était` avec l'agent `Il` donne un cadre présentatif, pas l'événement
`une petite fille / vivait / au bord de la forêt`. La définition est publiée ; elle reste
une convention, pas une vérité.

### 5.5 Le repli fabrique des agents

Le repli `groupe nominal à gauche` fait lire `The cat` comme agent de `sleeps` (`f07`,
correct) mais aussi `Les caractères spéciaux` comme agent d'un texte sans prédicat (`f40`,
cadre vide attendu) ou `Un fichier /home/user` comme agent de `notes` (`f39`, or vide). Le
repli est nécessaire pour l'anglais, mais il crée des faux positifs ; il est nommé dans le
JSON (`agent_origine = groupe_nominal_avant`).

## 6. Les contrôles

### 6.1 Les planchers

| contrôle | rôles exacts | cadres exacts |
|---|---:|---:|
| **vide** (aucun rôle) | 61/138 | **7/46** |
| **constant par type** (GN=agent, GV=prédicat, GP=lieu) | 68/138 | **6/46** |
| **rôles mélangés** (agent←prédicat, prédicat←lieu, lieu←agent) | 29/138 | **3/46** |
| **v2** (le lecteur) | **91/138** | **19/46** |

Le lecteur bat les planchers, mais **19/46** reste loin de 1. Le mélange tombe à **3/46** :
les rôles comptent, la mesure ne lit pas un rôle constant déguisé. Le contrôle vide a **7**
cadres exacts parce que **7** cadres d'or sont vides ; la v2 n'en laisse que **3** vides et
invente des rôles sur les **4** autres (`f25`, `f39`, `f42`, `f48`).

### 6.2 Le rendu

| contrôle | valeur |
|---|---:|
| `relire_roles(rendre_roles(a)) == principal` | **46/46 = 1,0000** |
| contrôle négatif : retrait du prédicat | **39/39** éligibles changent |
| contrôle négatif : permutation agent/prédicat | **39/39** éligibles changent |
| détection combinée | **39/39** |

Le rendu est **fidèle par construction** : il recopie les valeurs, puis les relit. Ce 46/46
est un invariant de codec, pas une compréhension. Les 7 textes non éligibles n'ont pas de
prédicat (dont `f18`, `f37`, `f40`).

### 6.3 Le contrôle externe

Sur le gold S (`tools/structures/donnees/gold-analyseur.json`, **61 phrases**, **144 rôles**),
le même lecteur — appariement par recouvrement maximal à type égal, rôle normalisé
`prédicat`/`predicat` — rend **139/144 = 0,9653**, contre **104/144 = 0,7222** pour le rôle
constant par type. Ce n'est **pas** le banc v0 : c'est un gold de la même famille de règles,
écrit avant la v2. Il montre que la lecture des rôles n'est pas cassée quand l'or est propre ;
l'écart avec les 46 textes v0 mesure la difficulté du banc et le bruit de l'annotation, pas
un bug de format.

## 7. Ce que la v2 ne dit pas

- **La fidélité sémantique** : 46/46 sur le rendu est un codec ; 16/46 sur l'or est une
  exactitude de **cadre principal**, pas une compréhension de la phrase.
- **Les rôles hors cadre** : `patient`, `destinataire`, `moyen`, `temps`, `contenu` ne sont
  pas notés par l'or et ne sont pas mesurés. La v2 les affiche dans `autres`, sans les juger.
- **Les subordonnées** : l'or ne note qu'un cadre par texte ; une relative correcte dans une
  phrase dont le cadre principal est faux ne compte pas.
- **La généralité** : 46 textes écrits à la main (audit A26), 50 avec les refus ; pas un
  échantillon aléatoire, pas un corpus de production.
- **La langue** : le banc mêle français, anglais et `und` ; `agent` n'a pas la même définition
  syntaxique dans les trois. Le repli `groupe nominal` est surtout un pansement anglais.
- **Le temps** : la mesure complète prend ≈ 0,2 s (sans Levenshtein) ; elle n'est pas un
  decodeur neuronal.

## 8. Ce qui pourrait rendre cette fiche fausse

- **L'or** : 46 cadres écrits à la main, de la même main que la fiche, **après avoir vu les
  sorties**. Une autre lecture du « cadre principal » (première phrase, premier verbe conjugué,
  premier GV linéaire) changerait le chiffre. Les variantes déclarent les ambiguïtés, mais elles
  ne sont pas neutres.
- **La définition du cadre principal** : « premier prédicat qui porte un agent ou un lieu »
  favorise les cadres complets tardifs et désavantage les cadres simples précoces (`f50`).
- **La comparaison canonique** : `[^\W_]+` replie la casse et retire la ponctuation ; une
  comparaison exacte de surface donnerait un score plus bas. `C'` / `C'est` et `l'eau` /
  `leau` sont des cas de bord.
- **Le repli `groupe nominal`** : sans lui, l'anglais et les GN sans rôle tombent ; avec lui,
  des agents sont inventés. Le chiffre dépend de ce choix, publié dans le JSON.
- **L'appariement du contrôle externe** : recouvrement maximal à type égal, un segment par
  attendu ; un autre appariement changerait 139/144. Le gold S est de la même famille de
  règles, pas une validation humaine.
- **Le banc** : 46 annotations, 4 refus, textes hétérogènes ; les textes très longs (`f50`)
  pèsent par leurs nombreux prédicats, pas par leur longueur dans le score.

## 9. La suite

1. **Ne pas maquiller la v2 en analyseur** : elle restera une vue tant que les rôles de
   l'annotation ne seront pas meilleurs. La prochaine action est la **qualité des rôles de
   l'analyseur** (`agent`, `prédicat`, `lieu`), pas un nouveau format.
2. **Un or de rôles plus large** : annoter les seconds cadres et les rôles hors cadre, puis
   mesurer la précision/rappel par rôle sur plusieurs phrases par texte.
3. **Le lieu** : la règle `_role_gp` doit distinguer `lieu`, `temps`, `destinataire`,
   `possession`, `complément` ; c'est le rôle le plus faible (F1 0,4000).
4. **Les phrases simples** : `f27` (`Élodie sourit.`), `f33` (`Si tu viens, apporte…`) et
   `f08` n'ont pas de cadre ; la segmentation est la première cause.
5. **Le contrôle externe** : le gold S à 139/144 est le prochain banc de non-régression des
   rôles ; il ne remplace pas un or humain sur la v0.

## 10. Fichiers

- [`restitution_v2.py`](../tools/restitution_v2.py) — `rendre_roles`, `cadres`,
  `relire_roles`, `comparer_cadre`, `mesurer_banc_v2`, `mesurer_gold_analyseur`.
- [`drave.py`](../tools/drave.py) — `restituer --roles`, `--gold`, JSON v2.
- [`mesurer_restitution_v2.py`](../tools/mesurer_restitution_v2.py) — produit le JSON.
- [`test_restitution_v2.py`](../tools/tests/test_restitution_v2.py) — 17 tests.
- [`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) — 46
  cadres, 65 variantes.
- [`pensee-restitution-v2.json`](pensee-restitution-v2.json) — les 50 résultats, la synthèse,
  les contrôles et les limites.
- [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json) — le banc des 50 textes.
- [`gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json) — le gold S du
  contrôle externe.
- [`rapport-restitution-v0.md`](rapport-restitution-v0.md) et
  [`rapport-restitution-v1.md`](rapport-restitution-v1.md) — les deux étages précédents.
