# B3 — Corpus d'or CIC v2 : le type de Bruijn vérifié, le sha256 rejoué deux fois

> **Ligne de roadmap** : **L / R0.7** (le bloc langue) — chantier **Panini** · **Tâche** : **B3** ·
> **Date** : **2026-11-15** ·
> **Verdict** : ✅ **le corpus d'or CIC reste 42/42, et le vérificateur voit maintenant deux choses
> qu'il ne voyait pas** — (1) chaque **type de de Bruijn** est **clos** et **bien formé**
> (`[] ⊢ type : sort n`), chaque preuve est close : **42/42** ; (2) le **sha256** est rejoué par une
> **seconde implémentation** écrite depuis FIPS 180-4, **sans `hashlib`**, sur le fichier, les **42**
> couples `preuve || type` et les **24** termes de l'environnement : **0 écart**. Les contrôles
> négatifs sont étendus : **36/36** preuves altérées rejetées, **42/42** types altérés rejetés,
> **1 020/1 020** mutations de `eq(2,2)` rejetées.
>
> **Code mesuré** : `01b6db6e` + le diff B3.
> **JSON** : [`cic-verificateur-v2.json`](cic-verificateur-v2.json) ·
> **Outil** : [`../tools/verificateur_cic.py`](../tools/verificateur_cic.py) ·
> **Porte** : [`../tools/porte-cic.sh`](../tools/porte-cic.sh) ·
> **Tests** : [`../tools/tests/test_verificateur_cic_v2.py`](../tools/tests/test_verificateur_cic_v2.py)
> (+ les 21 tests J12.2 de [`test_verificateur_cic.py`](../tools/tests/test_verificateur_cic.py)) ·
> **Fixture portable** : [`../tools/tests/cic/`](../tools/tests/cic/).
>
> **Fiche précédente** : [`rapport-cic-verificateur.md`](rapport-cic-verificateur.md) (J12.2, 42/42).

## 1. Ce que B3 ajoute à J12.2

J12.2 avait établi le **verrou de portabilité** : un noyau CIC-lite réécrit côté Drave rejoue les
**42** verdicts sans importer le vérificateur de Panini, et altérer un octet des **36** preuves
acceptées les fait rejeter. B3 ne refait pas ce résultat : il **ferme trois trous de contrôle** que
J12.2 laissait ouverts.

| # | trou dans J12.2 | ce que B3 ajoute | mesure |
|---|---|---|---|
| 1 | le **type** était décodé et utilisé, mais jamais vérifié comme type | **portée de de Bruijn** + **`[] ⊢ type : sort n`** + preuve close | **42/42** types bien formés, **42/42** preuves closes |
| 2 | l'empreinte était recalculée avec `hashlib`, donc par la même bibliothèque que le calcul de référence | **seconde implémentation de SHA-256** (FIPS 180-4), sans `hashlib`, sur le corpus, les 42 couples et les 24 termes | **42/42** couples, **24/24** termes, **0 écart** |
| 3 | le contrôle négatif n'altérait que des **preuves** | altération d'un octet des **42 types** + comparaison des deux sha256 | **42/42** rejets, **36** types devenus invalides, **6** rejets par la preuve |

La question de B3 n'est donc pas « 42/42 tient-il ? » — c'est « **le vérificateur vérifie-t-il le
contrat qu'il prétend vérifier ?** ». Un type ouvert ou mal typé ne doit jamais servir de contrat ;
une empreinte ne doit pas être validée par le même chemin qui l'a produite.

## 2. Le dispositif

### 2.1 L'artefact, inchangé

| élément | valeur |
|---|---|
| source | `Panini/research/nipada/falsification/corpus_dor_cic_v1.json` |
| commit source | `2130310db46ca9d59883500adc607bd86f534678` |
| sha256 source | `3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec` |
| octets | **46 714** |
| copie Drave | `tools/tests/cic/corpus_dor_cic_v1.json` |
| sha256 copie | **identique** à la source |
| contenu | **3** defs, **21** consts, **42** entrées (**36** `accepte`, **6** `rejette`) |

B3 n'ajoute **aucune** entrée au corpus : il étend le vérificateur, pas la fixture. La copie reste
byte-identique et le manifeste [`manifeste.json`](../tools/tests/cic/manifeste.json) fige la
provenance. Le corpus n'exerce toujours que **20** des **39** étiquettes du format ; les **types**
seuls en exercent **12** (`app`, `const`, `def`, `empty`, `id`, `nat`, `pi`, `sigma`, `sort`, `suc`,
`var`, `zero`).

### 2.2 La vérification du type de de Bruijn

Un terme bien **encodé** n'est pas forcément un **type**. B3 ajoute deux contrôles indépendants du
jugement de la preuve :

1. **portée** — `indices_hors_portee(t)` parcourt le terme et rend tout `var i` avec `i ≥` nombre de
   lieurs ouverts ; `est_clos(t)` exige la liste vide. Ce contrôle est purement structurel : il ne
   passe ni par `infer`, ni par la conversion, ni par l'environnement.
2. **bien-formedness** — `Kernel.type_bien_forme(A)` exige `A` clos, puis `[] ⊢ A : sort n`. Le
   noyau rend le sort (`("sort", 0)` ou `("sort", 1)`) ou `None`. Un type ouvert
   (`("var", 0)`), une application mal typée (`0 0`) ou un lambda qui n'est pas un type sont
   refusés.

Dans `rejouer`, la preuve n'est acceptée que si le type est **clos et bien formé**. Les 42 entrées
passent : **38** types vivent en `sort 0`, **4** en `sort 1` (`transport`, `ap`, `symm`, `trans`),
et les **42** preuves sont closes. Les définitions et les constantes sont également closes ; les
21 constantes sont des types bien formés (niveaux 0 ou 1).

### 2.3 La seconde implémentation de SHA-256

`sha256_pur(message)` est une réécriture de **FIPS 180-4** dans le module : 64 constantes `K`,
8 valeurs initiales `H`, rotation droite 32 bits, rembourrage `0x80` + zéros + longueur en bits sur
8 octets big-endian. Elle n'appelle **jamais** `hashlib`. Elle est confrontée à `hashlib` sur :

- **16 vecteurs** : les 4 vecteurs FIPS connus (chaîne vide, `abc`, le message à deux blocs, les
  256 octets `00…ff`) et 12 longueurs de rembourrage (1, 55, 56, 57, 63, 64, 65, 119, 120, 127,
  128, 129 octets) ;
- le **sha256 du fichier** du corpus ;
- les **42** couples `preuve || type` — c'est l'empreinte déclarée par le corpus ;
- les **42** preuves seules et les **42** types seuls ;
- les **24** termes de l'environnement (3 définitions + 21 constantes), sérialisés.

`verifier_sha256_independant` rend `pass` seulement si **tous** les chemins concordent. Une
divergence entre la seconde implémentation et `hashlib`, ou entre la seconde implémentation et
l'empreinte déclarée, fait échouer le verdict global — ce n'est pas un avertissement.

### 2.4 Les contrôles négatifs étendus

| contrôle | méthode | ce qui doit arriver |
|---|---|---|
| preuve altérée | dernier octet de la preuve `+1 mod 256`, sur les **36** preuves acceptées | rejet **36/36**, empreinte changée sous les deux sha256 |
| type altéré | dernier octet du type `+1 mod 256`, sur les **42** entrées | type invalide **ou** preuve rejetée, **42/42** |
| exhaustif | toutes les valeurs d'un octet de `eq(2,2)` (4 octets) | **1 020/1 020** rejetées |
| non-trivialité | noyau « accepte tout » / « rejette tout » | **6** / **36** désaccords |
| corpus corrompu | un octet d'une preuve, puis un octet d'un type, fichier réécrit | code de sortie **1** dans les deux cas |

Le contrôle « type altéré » est le contrôle qui donne son sens à la section 2.2 : sur les 42
mutations, **36** rendent le type invalide (le dernier octet touche un `nat`, un `sort`, une
constante ou une structure) ; les **6** autres restent des types bien formés, mais la preuve ne se
vérifie plus contre eux. Aucune des 42 n'est acceptée.

### 2.5 Les commandes

```bash
python3 tools/verificateur_cic.py              # résumé humain
python3 tools/verificateur_cic.py --json       # mesure machine
python3 tools/verificateur_cic.py --verbeux    # une ligne par entrée
python3 tools/verificateur_cic.py --sans-controles  # rejeu seul
bash tools/porte-cic.sh                        # la porte : 42/42 + contrôles étendus
python3 tools/tests/test_verificateur_cic.py       # 21 tests J12.2
python3 tools/tests/test_verificateur_cic_v2.py    # 17 tests B3
```

Le vérificateur lit le corpus en lecture seule, n'écrit aucun fichier et sort en **0** si et
seulement si le sha256 du corpus, les sérialisations, les empreintes (les deux chemins), les types
de de Bruijn, les verdicts et les contrôles négatifs passent.

## 3. Les résultats

### 3.1 Le rejeu reste 42/42

| mesure | valeur |
|---|---:|
| entrées | **42** |
| attendues `accepte` | **36** |
| attendues `rejette` | **6** |
| accord | **42 / 42** |
| désaccord | **0** |
| taux d'accord | **1,000000** |
| empreintes valides (`hashlib`) | **42 / 42** |
| empreintes valides (seconde implémentation) | **42 / 42** |
| empreintes concordantes entre les deux | **42 / 42** |
| sérialisations canoniques | **42 / 42** |
| définitions / constantes | **3 / 21** |
| durée du rejeu complet | **≈ 1,04 s** (avec contrôles) |

Le rejeu complet inclut désormais la seconde implémentation de SHA-256 et la vérification des
types ; il reste de l'ordre de la seconde sur cette machine.

### 3.2 Le type de de Bruijn — 42/42

| mesure | valeur |
|---|---:|
| types examinés | **42** |
| types clos (aucun indice hors portée) | **42 / 42** |
| types bien formés (`[] ⊢ type : sort n`) | **42 / 42** |
| preuves closes | **42 / 42** |
| types en `sort 0` | **38** |
| types en `sort 1` | **4** |
| types par les 42 entrées exerçant des étiquettes | **12** |

Les 4 types de niveau 1 sont les théorèmes généraux sur l'identité (`transport`, `ap`, `symm`,
`trans`) ; les 38 autres sont des propositions closes de niveau 0 (égalités, `Σ`, implications,
arithmétique). Le contrôle n'est pas un typage de la **preuve** une seconde fois : il vérifie un
objet différent, le **contrat** lui-même.

### 3.3 Le sha256 indépendant — 42/42 et 24/24

| mesure | valeur |
|---|---:|
| vecteurs de l'auto-test | **16** |
| écart sur les vecteurs | **0** |
| sha256 du corpus (`hashlib`) | `3018f6f4…aaec` |
| sha256 du corpus (seconde implémentation) | `3018f6f4…aaec` |
| couples `preuve ‖ type` concordants | **42 / 42** |
| empreintes déclarées retrouvées | **42 / 42** |
| preuves seules concordantes | **42 / 42** |
| types seuls concordants | **42 / 42** |
| termes de l'environnement concordants | **24 / 24** |
| écarts | **0** |

La seconde implémentation n'est pas une seconde **exécution** de `hashlib` : elle ne partage ni ses
tables, ni son code, ni son interface. Elle est écrite depuis la norme, avec les mêmes constantes
(c'est inévitable — ce sont celles de SHA-256) mais un chemin de calcul indépendant.

### 3.4 Les contrôles négatifs

| contrôle | résultat | verdict |
|---|---|---:|
| preuves altérées (36) | **36/36** rejetées, **0** acceptée | pass |
| empreintes des preuves altérées | **36/36** changées sous les deux sha256 | pass |
| types altérés (42) | **42/42** rejetés, **36** types devenus invalides | pass |
| empreintes des types altérés | **42/42** changées sous les deux sha256 | pass |
| exhaustif `eq(2,2)` | **1 020/1 020** rejetées | pass |
| accepte-tout | **36/42** d'accord, **6** désaccords | pass |
| rejette-tout | **6/42** d'accord, **36** désaccords | pass |
| corpus corrompu (preuve) | refusé, code **1** | pass |
| corpus corrompu (type) | refusé, code **1** | pass |

Le point important est la ligne « types altérés » : **36** mutations suffisent à rendre le type
invalide, mais **6** produisent encore un type bien formé. C'est précisément le cas où un
vérificateur qui ne regarde que l'empreinte pourrait laisser passer autre chose : ici la preuve est
rejetée contre le type muté, et l'empreinte a changé. Les deux verrous sont indépendants.

### 3.5 La porte et les tests

`bash tools/porte-cic.sh` :

```text
  42/42 verdicts · 42/42 empreintes · 42/42 sérialisations
  de Bruijn : 42/42 types bien formés · 42/42 preuves closes · niveaux [0, 1]
  sha256 2e implémentation : corpus ok · 42/42 couples · 24/24 termes · 16 vecteurs
  octet altéré : 36/36 rejetés · type altéré : 42/42 rejetés · exhaustif eq(2,2) : 1020/1020 rejetés
  non-trivialité : accepte-tout 6 désaccords, rejette-tout 36 désaccords
  corpus corrompu (preuve) : refusé (code 1)
  corpus corrompu (type) : refusé (code 1)
  tests : 21 (J12.2) + 17 (B3) = 38 cas
✅ porte CIC verte
```

Les **21 tests J12.2** restent inchangés et verts. Les **17 tests B3** couvrent : les 16 vecteurs
SHA-256, le sha256 du corpus, les 42 empreintes, les 24 termes, la sensibilité à un octet, les
42 types clos et bien formés, le rejet d'un type ouvert ou mal typé, l'acceptation de types valides,
les indices hors portée, les 36 preuves altérées, les 42 types altérés, l'exhaustif `eq(2,2)`, la
mesure globale et le refus d'un corpus au type corrompu.

## 4. Ce qui pourrait rendre ce résultat faux

1. **La vérification du type partage le noyau.** La portée est structurelle et indépendante, mais la
   bien-formedness (`[] ⊢ type : sort n`) passe par le même `infer` que la preuve. Un bug de
   spécification dans `infer` (par exemple la règle de J ou l'univers de Panini) validerait un type
   que Panini refuserait — et inversement. B3 ferme le trou « type jamais vérifié », pas le trou
   « spécification partagée ».
2. **Un type bien formé n'est pas un type habité.** `[] ⊢ A : sort n` dit que `A` est un contrat
   syntaxiquement valide, pas qu'il a un témoin. Le corpus fournit les témoins ; B3 ne prouve pas la
   cohérence de CIC-lite.
3. **La seconde implémentation de SHA-256 est une réimplémentation, pas une preuve.** Elle valide le
   chemin `hashlib` et la formule `sha256(preuve || type)` sur ces 42 entrées. Elle ne prouve ni la
   résistance aux collisions, ni l'absence d'un bug partagé avec la norme telle que lue ici.
4. **Le contrôle « un octet » reste un échantillon.** Il est systématique sur le **dernier** octet
   des 36 preuves et des 42 types, et exhaustif sur les 4 octets de `eq(2,2)`. Il ne prouve pas que
   **toutes** les mutations d'un octet de toutes les preuves sont rejetées ; une mutation qui
   produirait un autre terme bien typé serait acceptée, et c'est correct du point de vue du typage.
5. **Le corpus reste petit et partiel.** 42 entrées, 20 des 39 étiquettes exercées par les preuves,
   12 par les types. Les branches `bool`, `list`, `expr`, `abort`, `fst`/`snd` restent implémentées
   mais non mesurées ici.
6. **La copie portable peut dériver.** Elle est byte-identique à la source au commit
   `2130310d…` ; une modification de la source Panini après le 2026-11-14 ne serait pas vue. Le
   manifeste fige le commit et les deux empreintes.
7. **Le temps de la seconde implémentation est celui de Python.** Le sha256 pur est plus lent que
   `hashlib` (le rejeu complet passe d'environ 0,4 s à 1,04 s). Ce n'est pas un problème de
   correction, mais un coût à connaître si le corpus grandit.

## 5. Ce que la fiche fixe

- **Le corpus d'or CIC reste 42/42** : 36 acceptés, 6 rejetés, 42/42 empreintes, 42/42
  sérialisations — le résultat J12.2 n'est pas cassé par l'extension.
- **Le type de de Bruijn est vérifié** : 42/42 types clos et bien formés (`[] ⊢ type : sort n`),
  42/42 preuves closes ; un type ouvert ou mal typé est rejeté.
- **Le sha256 est rejoué par une seconde implémentation** : FIPS 180-4, sans `hashlib`, 16 vecteurs,
  42/42 couples, 24/24 termes, 0 écart avec `hashlib` et avec les empreintes déclarées.
- **Les contrôles négatifs sont étendus** : 36/36 preuves altérées rejetées, 42/42 types altérés
  rejetés, 1 020/1 020 mutations de `eq(2,2)` rejetées, non-trivialité vérifiée, corpus corrompu
  (preuve ou type) refusé.
- **La porte et les tests suivent** : `bash tools/porte-cic.sh`, 21 tests J12.2 + 17 tests B3.

La ligne Panini garde son verrou de portabilité et gagne un **verrou de contrat** : le type lu dans
l'artefact est maintenant un objet vérifié, et l'empreinte n'est plus validée par un seul chemin.
