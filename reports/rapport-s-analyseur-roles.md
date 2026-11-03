# S — Le contexte tranche les homographes : 54/55 types, 131/131 rôles, 55 structures au corpus

> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **55 phrases**
> (7 `dev`, 16 `test`, 32 `holdout` en quatre vagues), la structure de base retrouve la **séquence
> de types 54/55** (98,2 %), les **rôles 131/131** (100 %), les **compléments 47/47**, et couvre
> **1 466/1 475 octets** (99,4 % ; holdout **762/771**, 98,8 %). La **règle de contexte** corrige
> les homographes `h046` (« ferme ») et `h047` (« fait ») : un mot du lexique de verbes est un
> **nom** si le suivant est un auxiliaire ou un autre verbe. La **limite nommée** se déplace :
> `h050` (« fait » suivi d'un verbe **hors lexique**) et `h053` (« lit » après un adjectif, en
> fin de phrase). Le corpus de référence sort : **55 lignes**, SHA-256
> `76accf9dbd60a9fcc9fe58a56eecbdbb6aec0ffd5e8dbf0c69443e4a49dd1ac6`.

## Le dispositif

- **Gold** : [`tools/structures/donnees/gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json),
  **55 phrases** : **7 `dev`**, **16 `test`**, **32 `holdout`** en quatre vagues : `h024–h031`
  (première règle), `h032–h039` (copule), `h040–h047` (frontière GN-devant-verbe), `h048–h055`
  (règle de contexte des homographes). Les spans se calculent par sous-chaîne, dans l'ordre.
- **Analyseur** : [`generateur.py`](../tools/structures/generateur.py), `structure()` — rôles par
  la préposition et son contexte, subordonnées typées, passif, copule, frontière GN-devant-verbe,
  **contexte des homographes**.
- **Mesure** : [`mesure_analyseur.py`](../tools/structures/mesure_analyseur.py) →
  [`mesure-analyseur.json`](../tools/structures/donnees/mesure-analyseur.json).
- **Export** : [`exporter_corpus.py`](../tools/structures/exporter_corpus.py) →
  `data/structures/banque.jsonl` ; vérification : [`verifier_corpus.py`](../tools/structures/verifier_corpus.py).

## Les chiffres

| split | phrases | types | couverture | rôles | compléments (GP/SUB/REL) |
|---|---:|---:|---:|---:|---:|
| `dev` | 7 | **7/7** | 229/229 (100 %) | **22/22** | **10/10** |
| `test` | 16 | **16/16** | 475/475 (100 %) | **40/40** | **19/19** |
| `holdout` | 32 | **31/32** | 762/771 (98,8 %) | **69/69** | **18/18** |
| **global** | **55** | **54/55** (98,2 %) | **1 466/1 475** (99,4 %) | **131/131** (100 %) | **47/47** |

## La règle de contexte (v4)

Un mot du lexique de verbes (`VERBES_FINIS`) n'est **pas** une frontière de GN quand le mot
suivant montre qu'il est un **nom** :

- `La petite **ferme** est belle.` → `GN « La petite ferme »` · `GV « est belle »` (le suivant
  « est » est un auxiliaire) ;
- `Le simple **fait** surprend.` → `GN « Le simple fait »` · `GV « surprend »` (le suivant
  « surprend » est un verbe) ;
- mais `La femme **parle** à son fils.` → `GN « La femme »` · `GV « parle »` (le suivant « à »
  n'est ni auxiliaire ni verbe) ;
- et `Le chat **fait** des bonds.` → `GN « Le chat »` · `GV « fait »` (le suivant « des » est un
  déterminant).

Les règles de la v3 restent : frontière du GN devant un verbe conjugué, GV arrêté devant un
adverbe de temps, rôles contextuels, subordonnées, passif, copule.

## Les contrôles négatifs

| contrôle | ce qu'il fait | résultat |
|---|---|---:|
| **baseline** | rôle constant par type (GN=agent, GV=predicat, GP=lieu, SUB=contenu, REL=qualite) | **94/131** (0,718) |
| **règles coupées** | `structure(roles=False)` : mêmes segments, rôles par défaut | **96/131** (0,733) |
| **rôles mélangés** | 200 permutations des rôles attendus des compléments | **0,109** [0,00 ; 0,23] |
| **span corrompu** | `verifier_corpus.py --autotest` : un segment faux doit être refusé | **refusé** |
| **empreinte fausse** | SHA-256 du manifeste ≠ fichier | **refusé** |

**131/131 contre 94/131 et 0,109** : ce sont les règles qui lisent les mots, pas un rôle répété.

## Les limites nommées, et le protocole

- `h050` — « Le triste **fait** demeure. » : le mot suivant (`demeure`) n'est **pas** dans le
  lexique de verbes, donc la règle ne voit pas le nom ; le GN s'arrête à « Le triste »,
  **couverture 0,80**, types `[GN, GV]` (comme l'attendu) ;
- `h053` — « Le grand **lit**. » : le nom est après un adjectif, en **fin de phrase** ; le GN
  s'arrête à « Le grand », le GV « lit » apparaît, **type faux** (`[GN, GV]` au lieu de `[GN]`).

**Les deux limites sont fermées en v6** (le nom après adjectif devant un verbe, et en fin de phrase) ; la v6 ajoute la vague 5, le gold de 60 phrases (60/60 types, 142/142 rôles), et corrige le « si fort que » de conséquence — voir [`rapport-s-limites-v6.md`](rapport-s-limites-v6.md).

**Le protocole, sans le cacher** : `h033` (vague 2), `h046` et `h047` (vague 3) avaient échoué ;
les règles ont été ajoutées **après** ces mesures, donc les vagues 2 et 3 ne sont plus des
holdouts aveugles pour elles. La vague 4 (`h048–h055`) a été écrite **après** la règle de contexte
et mesurée **une fois** ; les deux limites n'ont pas été retouchées après la mesure. Les attendus
n'ont jamais été modifiés après coup.

## Le corpus exporté

| mode | sortie | lignes | statut | SHA-256 |
|---|---|---:|---|---|
| **gold** (défaut) | `data/structures/banque.jsonl` | **55** | `reference` | `76accf9d…49dd1ac6` |
| référence | `data/structures/banque-reference.jsonl` | 7 | `reference` | `77d7a014…42bf86` |
| banque validée | `data/structures/banque-validee.jsonl` | **0** | — | vide |

Le manifeste du corpus principal est copié dans
[`reports/s-banque-structures.json`](s-banque-structures.json) : mode, 55 phrases, 55 structures,
source et sortie **relatives**, SHA-256. `verifier_corpus.py` recalcule l'empreinte, les comptes,
les spans et la **restitution** : **55/55**.

**Le zéro de la banque validée est un fait** : `donnees/validations.jsonl` n'existe pas. La
**banque de candidats réels** (200 phrases, 355 candidats, manifeste `43957a3b…`) est prête
pour la validation humaine ; le mode `banque` la lira quand elle existera.

## Le miroir entrée/sortie

- **entrée** : surface → structure (l'analyseur) ; mesurée par les types, les rôles et la
  couverture ;
- **sortie** : structure → surface (le corpus) ; mesurée par l'empreinte, les comptes, les spans
  et la **restitution** ; `verifier_corpus.py --autotest` corrompt un span et exige l'échec.

La **fluidité n'est pas la fidélité** : le corpus se relit et se restitue, mais il n'est **pas**
une validation humaine — le statut `reference` le dit.

## Ce qui pourrait le rendre faux

- **La règle de contexte dépend du mot suivant** : un verbe hors lexique (`demeure`) ou un nom en
  fin de phrase après un adjectif (`le grand lit`) la trompent ; la vague 4 en montre deux.
- **Le lexique de verbes est une liste** : les verbes absents ne coupent pas le GN ; le contexte
  ne les connaît pas.
- **Le gold est de la même main que les règles** : les 16 `test` sont antérieurs, mais la vague 4
  est écrite par le même agent ; elle limite le biais, elle ne l'annule pas.
- **55 phrases, 1 475 octets** : instrument de cohérence, pas de généralité ; les rôles hors
  inventaire ne sont pas mesurés.
- **L'appariement par recouvrement maximal** peut cacher une frontière fausse : `h050` le montre
  (types et rôles justes, couverture basse). La couverture est le garde-fou.
- **Le mode `banque` n'a aucun verdict** : le corpus livré est une **référence**, pas une banque
  validée.

## Fichiers

- Sous-module : commits **`1445e1d`** (v4) et **`00d2a01`** (manifeste de la banque), **47 tests**.
- Gold : `tools/structures/donnees/gold-analyseur.json` ; mesure :
  `tools/structures/donnees/mesure-analyseur.json` ; code : `generateur.py`,
  `mesure_analyseur.py`, `exporter_corpus.py`, `verifier_corpus.py`.
- Corpus : `data/structures/banque.jsonl` (55 lignes, non versionné comme tout `data/`) ;
  manifeste committé : `reports/s-banque-structures.json`.

## La suite (ligne S)

1. ~~**`h050`/`h053`**~~ : fermées en v6 ; reste le **nom après un adjectif hors lexique** ;
2. **Validation humaine** de la banque de 200 phrases (le mode `banque` est le contrat) ;
3. **gold plus large** (voix, causatives, verbes à double complément) ;
4. le corpus de référence peut être lu par **N2/R1** comme un petit test de structure.
