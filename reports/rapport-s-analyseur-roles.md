# S — La frontière du GN s'arrête devant le verbe : 47/47 types, 117/117 rôles, 47 structures au corpus

> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **47 phrases**
> (7 `dev`, 16 `test`, 24 `holdout` en trois vagues), la structure de base retrouve la **séquence
> de types 47/47** (100 %), les **rôles 117/117** (100 %), les **compléments 47/47**, et couvre
> **1 309/1 320 octets** (99,2 % ; holdout **605/616**, 98,2 %). La règle de **frontière du GN**
> corrige l'échec `h033` (« La femme parle ») ; la **limite nommée** se déplace : les homographes
> nominaux `h046` (« ferme ») et `h047` (« fait ») sont coupés comme des verbes, et c'est la
> **couverture** qui le voit (0,75 et 0,77), pas le type ni le rôle. Le corpus de référence sort :
> **47 lignes**, SHA-256 `f2a0d2fb3a9b0a9aebd562b170503f4d1a98251efdc4a3645a2523b5197227a2`.

## Le dispositif

- **Gold** : [`tools/structures/donnees/gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json),
  **47 phrases** : **7 `dev`** (les phrases du banc), **16 `test`** (écrites avant les règles) et
  **24 `holdout`** en trois vagues : `h024–h031` (première règle), `h032–h039` (après la copule),
  `h040–h047` (après la frontière GN-devant-verbe). Chaque phrase porte sa suite de segments
  (texte, type, rôle) ; les spans se calculent par sous-chaîne, dans l'ordre.
- **Analyseur** : [`generateur.py`](../tools/structures/generateur.py), fonction `structure()` —
  segmentation (GN, GV, GP, REL, SUB), rôles par la préposition et son contexte, subordonnées
  typées, passif, copule, et **frontière GN-devant-verbe**.
- **Mesure** : [`mesure_analyseur.py`](../tools/structures/mesure_analyseur.py) →
  [`mesure-analyseur.json`](../tools/structures/donnees/mesure-analyseur.json). Trois chiffres
  (types, couverture, rôles) et trois contrôles.
- **Export** : [`exporter_corpus.py`](../tools/structures/exporter_corpus.py) →
  `data/structures/banque.jsonl` ; vérification : [`verifier_corpus.py`](../tools/structures/verifier_corpus.py).

## Les chiffres

| split | phrases | types | couverture | rôles | compléments (GP/SUB/REL) |
|---|---:|---:|---:|---:|---:|
| `dev` | 7 | **7/7** | 229/229 (100 %) | **22/22** | **10/10** |
| `test` | 16 | **16/16** | 475/475 (100 %) | **40/40** | **19/19** |
| `holdout` | 24 | **24/24** | 605/616 (98,2 %) | **55/55** | **18/18** |
| **global** | **47** | **47/47** (100 %) | **1 309/1 320** (99,2 %) | **117/117** (100 %) | **47/47** |

## La frontière du GN (la règle v3)

Le GN s'arrête devant un **verbe conjugué fréquent** (`VERBES_FINIS`, lexique assumé) et le GV
s'arrête devant un **adverbe de temps** :

- « La femme parle à son fils. » → `GN « La femme »` · `GV « parle »` · `GP « à son fils »` ;
- « Le train part demain. » → `GN « Le train »` · `GV « part »` · `GP « demain »` (temps) ;
- « Le petit chat noir dort. » → `GN « Le petit chat noir »` · `GV « dort »` ;
- « Une belle maison. » → un seul `GN` (aucun verbe).

Les règles de rôle de la v2 restent : possession/thème, instrument/attribut, but/lieu,
agent/moyen, passif, copule, subordonnées (temps, cause, concession, hypothèse, but, manière,
contenu).

## Les contrôles négatifs

| contrôle | ce qu'il fait | résultat |
|---|---|---:|
| **baseline** | rôle constant par type (GN=agent, GV=predicat, GP=lieu, SUB=contenu, REL=qualite) | **80/117** (0,684) |
| **règles coupées** | `structure(roles=False)` : mêmes segments, rôles par défaut | **82/117** (0,701) |
| **rôles mélangés** | 200 permutations des rôles attendus des compléments | **0,109** [0,00 ; 0,23] |
| **span corrompu** | `verifier_corpus.py --autotest` : un segment faux doit être refusé | **refusé** |
| **empreinte fausse** | SHA-256 du manifeste ≠ fichier | **refusé** |

Les trois contrôles de rôle sont nécessaires : sans la baseline et les règles coupées, 117/117
pourrait être le score d'un étiqueteur qui répète un rôle ; sans les rôles mélangés, il pourrait
être le score de la distribution. **117/117 contre 80/117 et 0,109** : ce sont les règles qui
lisent les mots.

## L'échec nommé, et le protocole qui le rend honnête

**`h033` est corrigé** : « La femme parle à son fils. » rend maintenant `GN « La femme »` ·
`GV « parle »` · `GP « à son fils »` (types 3/3, couverture 1,0). La règle est un **lexique de
verbes finis**, pas un étiqueteur.

**La nouvelle limite est nommée** : les homographes nominaux.

- `h046` — « La petite **ferme** est belle. » → le GN s'arrête à « La petite », le GV commence à
  « ferme » : types `[GN, GV]` (comme l'attendu), rôles 2/2, mais **couverture 0,75** ;
- `h047` — « Le simple **fait** surprend. » → même coupe, **couverture 0,77**.

C'est un cas où le **type et le rôle sont aveugles** à la frontière : seule la couverture la voit.
La leçon vaut pour la mesure : un score de types à 100 % ne dit pas que les spans sont justes.

**Le protocole du gold, sans le cacher** : `h033` avait échoué dans la vague 2 ; la règle de
verbe a été ajoutée **après** cette mesure, donc la vague 2 n'est plus un holdout aveugle pour
cette règle. La vague 3 (`h040–h047`) a été écrite **après** la règle et mesurée **une fois** ;
les deux homographes n'ont pas été retouchés après la mesure. Les attendus n'ont jamais été
modifiés après coup.

## Le corpus exporté

| mode | sortie | lignes | statut | SHA-256 |
|---|---|---:|---|---|
| **gold** (défaut) | `data/structures/banque.jsonl` | **47** | `reference` | `f2a0d2fb…7227a2` |
| référence | `data/structures/banque-reference.jsonl` | 7 | `reference` | `77d7a014…42bf86` |
| banque validée | `data/structures/banque-validee.jsonl` | **0** | — | vide |

Le manifeste du corpus principal est copié dans
[`reports/s-banque-structures.json`](s-banque-structures.json) : mode, 47 phrases, 47 structures,
source et sortie **relatives**, SHA-256. `verifier_corpus.py` recalcule l'empreinte, les comptes,
les spans et la **restitution** (segments + trous = texte) : **47/47**.

**Le zéro de la banque validée est un fait, pas un oubli** : `donnees/validations.jsonl` n'existe
pas — aucun verdict humain n'a été enregistré. Le mode `banque` lit le schéma `statut` du serveur
(`resolu`, `compatible`, `double_sens` ; le dernier verdict gagne ; `exclu` ne sort pas) et garde
`verdict: ok` pour les anciens journaux. L'export de **référence** est livré ; la **validation
humaine** reste à faire et c'est elle qui remplira `banque-validee.jsonl`.

## Le miroir entrée/sortie

- **entrée** : surface → structure (l'analyseur) ; mesurée par les types, les rôles et la
  couverture ;
- **sortie** : structure → surface (le corpus) ; mesurée par l'empreinte, les comptes, les spans
  et la **restitution** ; `verifier_corpus.py --autotest` corrompt un span et exige l'échec.

La **fluidité n'est pas la fidélité** : le corpus se relit et se restitue, mais il n'est **pas**
une validation humaine — le statut `reference` le dit, et le mode `banque` reste à zéro.

## Ce qui pourrait le rendre faux

- **Le lexique de verbes est une liste** : les verbes absents ne coupent pas le GN ; les
  homographes nominaux (`ferme`, `fait`, `lit`, `porte`, `danse`) le coupent à tort. La vague 3
  en montre deux ; c'est la limite de l'heuristique, pas un accident.
- **Le gold est de la même main que les règles** : les 16 `test` ont été écrits avant, mais par
  le même agent ; la vague 3 limite le biais, elle ne l'annule pas. Un gold écrit par un humain
  aveugle aux règles manquerait probablement les mêmes frontières autrement.
- **47 phrases, 1 320 octets** : c'est un instrument de cohérence, pas de généralité. Les rôles
  hors inventaire (`origine`, causatives, double complément) ne sont pas mesurés.
- **L'appariement par recouvrement maximal** peut cacher une frontière fausse : `h046`/`h047` le
  montrent (types et rôles justes, couverture basse). La couverture est le garde-fou, pas le
  score de type.
- **Le mode `banque` n'a aucun verdict** : le corpus livré est une **référence**, pas une banque
  validée. Le confondre avec une vérité humaine serait l'erreur.

## Fichiers

- Sous-module : commit **`90e507b`** (committé **dans son dépôt** avant le pointeur), **46 tests** aujourd'hui.
- Gold : `tools/structures/donnees/gold-analyseur.json` ; mesure :
  `tools/structures/donnees/mesure-analyseur.json` ; code : `generateur.py`,
  `mesure_analyseur.py`, `exporter_corpus.py`, `verifier_corpus.py`.
- Corpus : `data/structures/banque.jsonl` (47 lignes, non versionné comme tout `data/`) ;
  manifeste committé : `reports/s-banque-structures.json`.

## La suite (ligne S)

1. **Homographes et lexique** : distinguer le verbe du nom (`ferme`, `fait`, `lit`, `porte`) par
   le contexte — ou assumer la liste et la documenter ;
2. **Validation humaine** de la banque (le mode `banque` est le contrat ; 0 tant qu'elle n'existe
   pas) ;
3. **gold plus large** (voix, causatives, verbes à double complément) avant de créditer
   l'analyseur d'autre chose que de la cohérence ;
4. le corpus de référence peut être lu par **N2/R1** comme un petit test de structure, pas comme
   un corpus d'entraînement massif.
