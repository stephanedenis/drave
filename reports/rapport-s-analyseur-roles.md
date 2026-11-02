# S — L'analyseur nomme les rôles : 99/100, 38/39 types, et 39 structures au corpus

> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **39 phrases**
> (7 `dev`, 16 `test`, 16 `holdout`), la structure de base retrouve la **séquence de types
> 38/39** (97,4 %), les **rôles 99/100** (99 %), les **compléments 45/45**, et couvre
> **1 156/1 161 octets** (99,6 %). L'échec est **nommé** : « La femme parle » est lu comme un
> GN, le verbe est avalé. Le corpus de référence sort : **39 lignes**, SHA-256
> `973c70a4126896b8557d803b940f58d1f6d1fe1d172cdb7b9abce9671cd7db71`.

## Le dispositif

- **Gold** : [`tools/structures/donnees/gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json),
  **39 phrases** : **7 `dev`** (les phrases du banc, référence écrite à la main), **16 `test`**
  (écrites **avant** les règles de rôles/subordonnées) et **16 `holdout`** (écrites **après**,
  mesurées une fois ; aucun attendu n'est modifié après la mesure). Chaque phrase porte sa suite
  de segments (texte, type, rôle) ; les spans se calculent par sous-chaîne, dans l'ordre.
- **Analyseur** : [`generateur.py`](../tools/structures/generateur.py), fonction `structure()` —
  segmentation (GN, GV, GP, REL, SUB) et rôles **par la préposition et son contexte** ; rien
  n'est appris.
- **Mesure** : [`mesure_analyseur.py`](../tools/structures/mesure_analyseur.py) →
  [`mesure-analyseur.json`](../tools/structures/donnees/mesure-analyseur.json). Trois chiffres
  (types, couverture des octets, rôles) et trois contrôles.
- **Export** : [`exporter_corpus.py`](../tools/structures/exporter_corpus.py) →
  `data/structures/banque.jsonl` ; **vérification** :
  [`verifier_corpus.py`](../tools/structures/verifier_corpus.py).

## Les chiffres

| split | phrases | types | couverture | rôles | compléments (GP/SUB/REL) |
|---|---:|---:|---:|---:|---:|
| `dev` | 7 | **7/7** | 229/229 (100 %) | **22/22** | **10/10** |
| `test` | 16 | **16/16** | 475/475 (100 %) | **40/40** | **19/19** |
| `holdout` | 16 | **15/16** | 452/457 (98,9 %) | **37/38** | **16/16** |
| **global** | **39** | **38/39** (97,4 %) | **1 156/1 161** (99,6 %) | **99/100** (99 %) | **45/45** |

Ce que les règles ajoutent, par type de complément :

- `de` **possession** après un GN, **thème** après un GV (« de la voisine » / « de son projet ») ;
- `avec` **instrument**, et **attribut** quand le candidat l'attache au GN ;
- `à` **but** devant un infinitif, **destinataire** sinon, **lieu** après un verbe de lieu ;
- `par` **agent** après un passif, **moyen** sinon ; le GN sujet du passif devient **patient** ;
- subordonnées : `quand / dès que / pendant que` → **temps**, `parce que / puisque / comme` →
  **cause**, `si / s'il` → **hypothèse**, `bien que` → **concession**, `afin que` → **but**,
  `sans que` → **manière** ; la complétive après un verbe reste **contenu**, la relative après un
  nom **qualité** ;
- copule : « est mon voisin » reste un **GV** attributif au lieu de se couper en « est » + GN.

## Les contrôles négatifs

| contrôle | ce qu'il fait | résultat |
|---|---|---:|
| **baseline** | rôle constant par type (GN=agent, GV=predicat, GP=lieu, SUB=contenu, REL=qualite) | **64/100** (0,64) |
| **règles coupées** | `structure(roles=False)` : mêmes segments, rôles par défaut | **66/100** (0,66) |
| **rôles mélangés** | 200 permutations des rôles attendus des compléments | **0,099** [0,00 ; 0,22] |
| **span corrompu** | `verifier_corpus.py --autotest` : un segment faux doit être refusé | **refusé** |
| **empreinte fausse** | SHA-256 du manifeste ≠ fichier | **refusé** |

Les trois contrôles de rôle sont nécessaires : sans la baseline et les règles coupées, 99/100
pourrait être le score d'un étiqueteur qui répète un rôle ; sans les rôles mélangés, il pourrait
être le score de la distribution des étiquettes. **99/100 contre 64/100 et 0,099** : ce sont bien
les règles qui lisent les mots.

## L'échec nommé

**h033 — « La femme parle à son fils. »** : l'analyseur rend `[GN « La femme parle », GP « à son
fils »]` au lieu de `[GN « La femme », GV « parle », GP « à son fils »]`. La frontière du GN
s'arrête à trois mots pleins et **avale un verbe conjugué** quand il n'y a pas d'auxiliaire
(« La femme **a** vu » ne le fait pas : l'auxiliaire coupe). C'est une **limite de
segmentation**, pas de rôle : les compléments restent 45/45. Elle est nommée, pas corrigée par
une liste de verbes apprise sur le holdout.

**L'histoire du holdout, pour qu'elle ne soit pas cachée** : le premier holdout (h024) a révélé
le même défaut sur « est mon voisin » (« est » + GN). Une règle **générale** de copule a été
ajoutée, puis un **second** holdout (h032–h039) écrit et mesuré une fois ; h033 y échoue. Les
attentes n'ont pas été retouchées après la mesure.

## Le corpus exporté

| mode | sortie | lignes | statut | SHA-256 |
|---|---|---:|---|---|
| **gold** (défaut) | `data/structures/banque.jsonl` | **39** | `reference` | `973c70a4…cd7db71` |
| référence | `data/structures/banque-reference.jsonl` | 7 | `reference` | `77d7a014…42bf86` |
| banque validée | `data/structures/banque-validee.jsonl` | **0** | — | vide |

Le manifeste du corpus principal est copié dans
[`reports/s-banque-structures.json`](s-banque-structures.json) : mode, 39 phrases, 39 structures,
source et sortie **relatives**, SHA-256. `verifier_corpus.py` recalcule l'empreinte, les comptes,
les spans et la **restitution** (segments + trous = texte) : **39/39**.

**Le zéro de la banque validée est un fait, pas un oubli** : `donnees/validations.jsonl` n'existe
pas — aucun verdict humain n'a été enregistré. Le mode `banque` lit le schéma `statut` du serveur
(`resolu`, `compatible`, `double_sens` ; le dernier verdict gagne ; `exclu` ne sort pas) et garde
`verdict: ok` pour les anciens journaux. L'export de **référence** est livré ; la **validation
humaine** reste à faire et c'est elle qui remplira `banque-validee.jsonl`.

## Le miroir entrée/sortie

- **entrée** : surface → structure (l'analyseur) ; mesurée par les types et les rôles ;
- **sortie** : structure → surface (le corpus) ; mesurée par l'empreinte, les comptes, les spans
  et la **restitution** ; `verifier_corpus.py --autotest` corrompt un span et exige l'échec.

La **fluidité n'est pas la fidélité** : le corpus de référence se relit et se restitue, mais il
n'est **pas** une validation humaine — le statut `reference` le dit, et le mode `banque` reste à
zéro.

## Ce qui pourrait le rendre faux

- **Le gold est de la même main que les règles** : les 16 `test` ont été écrits avant, mais par
  le même agent ; le holdout limite le biais, il ne l'annule pas. Un gold écrit par un humain
  aveugle aux règles manquerait probablement les mêmes frontières autrement.
- **39 phrases, 1 161 octets** : c'est un instrument de cohérence, pas de généralité. Les rôles
  hors inventaire (`origine`, `agent` des causatives, `thème` des verbes à double complément)
  ne sont pas mesurés.
- **L'appariement par recouvrement maximal** peut cacher une frontière fausse : un segment
  généré plus court garde le bon rôle et perd des octets (c'est la couverture qui le voit, pas le
  score de rôle). Le cas h033 le montre : types 15/16, rôles 37/38, compléments 16/16.
- **Le lexique de lieu** (`VERBES_LIEU`) est une liste de formes : « à midi » après « arrive »
  serait un lieu. Le gold n'a pas ce cas ; il existe.
- **Le mode `banque` n'a aucun verdict** : le corpus livré est une **référence**, pas une banque
  validée. Le confondre avec une vérité humaine serait l'erreur.

## Fichiers

- Sous-module : commit **`647205a`** (le sous-module est committé **dans son dépôt** avant le
  pointeur), **40 tests**.
- Gold : `tools/structures/donnees/gold-analyseur.json` ; mesure :
  `tools/structures/donnees/mesure-analyseur.json` ; code : `generateur.py`,
  `mesure_analyseur.py`, `exporter_corpus.py`, `verifier_corpus.py`.
- Corpus : `data/structures/banque.jsonl` (39 lignes, non versionné comme tout `data/`) ;
  manifeste committé : `reports/s-banque-structures.json`.

## La suite (ligne S)

1. **Validation humaine** de la banque (le mode `banque` est le contrat ; 0 tant qu'elle n'existe
   pas) ;
2. **frontière du GN** sans auxiliaire (h033) : une règle de verbe, ou un lexique assumé ;
3. **gold plus large** (voix, causatives, verbes à double complément) avant de créditer
   l'analyseur d'autre chose que de la cohérence ;
4. le corpus de référence peut être lu par **N2/R1** comme un petit test de structure, pas comme
   un corpus d'entraînement massif.
