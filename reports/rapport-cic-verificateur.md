# J12.2 — Le corpus d'or CIC : 42/42 verdicts rejoués par un vérificateur indépendant

> **Ligne de roadmap** : **L / R0.7** (le bloc langue) — chantier **Panini** · **Tâche** : **J12.2** ·
> **Date** : **2026-11-14** ·
> **Verdict** : ✅ **le corpus d'or CIC est portable et rejouable hors de Panini** — un noyau
> CIC-lite réécrit côté Drave, sans importer le code de Panini, rend **42/42** verdicts
> (**36** acceptés, **6** rejetés), **42/42** empreintes `sha256(preuve || type)` et **42/42**
> sérialisations canoniques. Le contrôle négatif tient : altérer le dernier octet des **36**
> preuves acceptées les fait **36/36** rejeter, et les **1 020** mutations d'un octet de
> `eq(2,2)` sont **1 020/1 020** rejetées. Un noyau « accepte tout » et un noyau « rejette
> tout » échouent (respectivement **6** et **36** désaccords) : le banc n'est pas vide.
>
> **Code mesuré** : `bb68b820` (HEAD au moment de la mesure) + le vérificateur de cette fiche.
> **JSON** : [`cic-verificateur.json`](cic-verificateur.json) ·
> **Outil** : [`../tools/verificateur_cic.py`](../tools/verificateur_cic.py) ·
> **Porte** : [`../tools/porte-cic.sh`](../tools/porte-cic.sh) ·
> **Tests** : [`../tools/tests/test_verificateur_cic.py`](../tools/tests/test_verificateur_cic.py) ·
> **Fixture portable** : [`../tools/tests/cic/`](../tools/tests/cic/).

## 1. La question

Le corpus d'or CIC de Panini/Research est présenté comme **auto-portant et falsifiable** :
3 définitions, 21 constantes, **42 entrées** (36 `accepte`, 6 `rejette`), chaque preuve et son
type sérialisés en **de Bruijn** (hexadécimal), une empreinte **SHA-256**, et une doctrine
explicite — *toute implémentation doit reproduire exactement ces verdicts à partir de cet
artefact seul* ([inventaire Panini](rapport-inventaire-panini.md) § 4.3).

La question de J12.2 est donc simple à énoncer : **une seconde implémentation, côté Drave,
retrouve-t-elle les 42 verdicts sans importer le vérificateur de Panini ?** Et le contrôle qui
donne son sens à la réponse : **altérer un octet d'une preuve doit produire un rejet**, sinon le
vérificateur accepte n'importe quoi.

Réponse courte : **oui, 42/42**, et le contrôle négatif est net sur les 36 preuves acceptées
comme sur l'énumération exhaustive de la plus petite preuve.

## 2. Le dispositif

### 2.1 L'artefact, sa provenance et sa copie portable

| élément | valeur |
|---|---|
| source | `Panini/research/nipada/falsification/corpus_dor_cic_v1.json` |
| commit source | `2130310db46ca9d59883500adc607bd86f534678` |
| sha256 source | `3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec` |
| octets | **46 714** |
| copie Drave | `tools/tests/cic/corpus_dor_cic_v1.json` |
| sha256 copie | **identique** (byte pour byte) |
| manifeste | `tools/tests/cic/manifeste.json` |
| contenu | **3** defs, **21** consts, **42** entrées (**36** `accepte`, **6** `rejette`) |

La copie existe pour que le vérificateur soit **portable** : il ne lit pas le dépôt Panini au
moment du rejeu. Le manifeste fige aussi le sha256 du TSV source
(`9aa1a5f4…7424`), qui n'est pas utilisé par le vérificateur — le JSON contient tout
l'environnement (`defs`/`consts`), donc l'artefact seul suffit.

### 2.2 Le vérificateur indépendant

Le fichier [`tools/verificateur_cic.py`](../tools/verificateur_cic.py) réimplémente, côté Drave :

1. **le format** : étiquettes d'octets (`var`, `sort`, `pi`, `lam`, `app`, `nat`, `zero`, `suc`,
   `natrec`, `id`, `refl`, `j`, `sigma`, `pair`, `def`, `const`, …), varints canoniques,
   sérialisation/désérialisation exactes ;
2. **le noyau** : termes de de Bruijn, substitution, formes normales, conversion
   (β, ι, δ, η de Σ), typage bidirectionnel `check(contexte, terme, type)` ;
3. **les empreintes** : `sha256(preuve || type)` sur les octets binaires ;
4. **le rejeu** : chaque entrée est décodée, son empreinte vérifiée, son verdict recalculé,
   puis comparé au verdict déclaré.

Il **n'importe rien de Panini** : aucune ligne de `nipada.formalkernel.cic` n'est chargée, aucun
appel au dépôt Panini n'est fait. Les règles de typage sont celles de la spécification CIC-lite
(univers hiérarchiques, Π, λ, application, ℕ + récurseur, Id + `refl` + J, Σ + paires +
projections, définitions transparentes, constantes, unité, vide, Bool/Liste/Expr et leurs
récurseurs). C'est une **indépendance de code**, pas une indépendance de spécification : deux
implémentations du même contrat doivent rendre les mêmes verdicts, c'est précisément ce que l'on
mesure.

Le fragment portable couvre **39 étiquettes** ; le corpus en exerce **20** :

| étiquettes exercées (20) | étiquettes du format non exercées (19) |
|---|---|
| `var`, `sort`, `pi`, `lam`, `app`, `nat`, `zero`, `suc`, `natrec`, `id`, `refl`, `j`, `sigma`, `pair`, `def`, `const`, `natind`, `unit`, `tt`, `empty` | `abort`, `bool`, `boolind`, `boolrec`, `cons`, `eadd`, `emul`, `eone`, `erec`, `evar`, `expr`, `ezero`, `false`, `fst`, `list`, `listrec`, `nil`, `snd`, `true` |

Cette couverture est un **fait de mesure** : les 42 verdicts ne prouvent pas les 19 étiquettes
non exercées. Le vérificateur les implémente, mais elles ne sont pas validées par ce corpus.

### 2.3 Les commandes

```bash
python3 tools/verificateur_cic.py              # résumé humain
python3 tools/verificateur_cic.py --verbeux    # une ligne par entrée
python3 tools/verificateur_cic.py --json       # mesure machine
bash tools/porte-cic.sh                        # la porte : 42/42 + contrôles négatifs
python3 tools/tests/test_verificateur_cic.py   # 21 tests
```

Le vérificateur lit le corpus (lecture seule), ne modifie aucun fichier et sort en **0** si et
seulement si toutes les conditions passent : sha256 du corpus, sérialisation canonique,
empreintes, verdicts, contrôles négatifs.

## 3. Les résultats

### 3.1 42/42 verdicts

| mesure | valeur |
|---|---:|
| entrées | **42** |
| attendues `accepte` | **36** |
| attendues `rejette` | **6** |
| accord | **42 / 42** |
| désaccord | **0** |
| taux d'accord | **1,000000** |
| empreintes valides | **42 / 42** |
| sérialisations canoniques | **42 / 42** |
| définitions / constantes | **3 / 21** |
| durée du rejeu complet | **≈ 0,36 s** (avec contrôles négatifs) |
| durée du rejeu seul | **≈ 0,18 s** |

Le rejeu ne se contente pas de comparer des verdicts : il **vérifie** chaque preuve contre le
type attendu, par conversion. Les 36 acceptations passent par le noyau, pas par une table de
verdicts.

### 3.2 Les six rejets, et pourquoi ils sont rejetés

Les six entrées `rejette` sont de petits témoins dont le type inféré n'est pas le type attendu.
Le décodage (de Bruijn) et la conversion donnent :

| entrée | preuve (lisible) | type attendu | ce qui échoue |
|---|---|---|---|
| `refl2:Id2_3` | `refl 2` | `Id(ℕ; 2; 3)` | `refl 2` a le type `Id(ℕ; 2; 2)` : les extrémités diffèrent |
| `refl0:Id1_2` | `refl 0` | `Id(ℕ; 1; 2)` | `refl 0` a le type `Id(ℕ; 0; 0)` |
| `refl4:Id4_5` | `refl 4` | `Id(ℕ; 4; 5)` | `refl 4` a le type `Id(ℕ; 4; 4)` |
| `add2_3=6` | `refl 6` | `Id(ℕ; add 2 3; 6)` | `add 2 3 ≡ 5`, donc le type attendu est `Id(ℕ; 5; 6)` |
| `preuve_pas_un_nat` | `refl 2` | `ℕ` | `refl 2` a le type `Id(ℕ; 2; 2)`, pas `ℕ` |
| `mauvais_temoin` | `⟨3, refl(mul 2 2)⟩` | `Σ x:ℕ. Id(ℕ; mul 2 x; 4)` | le second composant est `Id(ℕ; mul 2 2; 4) = Id(ℕ; 4; 4)` ; avec `x = 3`, il faudrait `Id(ℕ; 6; 4)` |

Cinq rejets sont donc des **identités dont les extrémités ne coïncident pas** ; le sixième est
une **paire dont le second composant ne se convertit pas** au type attendu après substitution du
témoin. Aucun n'est rejeté par une règle ad hoc : c'est la conversion du noyau qui tranche.

### 3.3 Le contrôle négatif — altérer un octet

Trois contrôles, tous exécutés par défaut.

**a) Un octet sur chaque preuve acceptée.** Pour chacune des **36** preuves `accepte`, le
**dernier octet** est incrémenté modulo 256, puis la preuve mutée est rejouée contre son type :

| mesure | valeur |
|---|---:|
| mutations | **36** |
| acceptées après mutation | **0** |
| rejetées après mutation | **36 / 36** |
| empreintes changées | **36 / 36** |
| verdict | **pass** |

**b) Énumération exhaustive de `eq(2,2)`.** La plus petite preuve acceptée fait **4 octets**
(`0a 07 07 06`). Toutes les substitutions d'un octet par une autre valeur sont essayées :
**4 × 255 = 1 020** mutations.

| mesure | valeur |
|---|---:|
| octets de la preuve | **4** |
| mutations essayées | **1 020** |
| acceptées après mutation | **0** |
| rejetées après mutation | **1 020 / 1 020** |
| verdict | **pass** |

C'est le contrôle le plus fort : il ne choisit pas un octet « qui fait mal », il les essaie
tous.

**c) Non-trivialité du banc.** Si le noyau acceptait tout, il aurait **36/42** d'accord et
**6** désaccords ; s'il rejetait tout, **6/42** et **36** désaccords. Les deux témoins échouent
donc, ce qui montre que les 6 rejets et les 36 acceptations sont réellement discriminants.

**d) Corpus corrompu de bout en bout.** La porte copie le corpus, altère un octet d'une preuve
dans le JSON, puis relance le vérificateur avec `--sha256 ""` (pour ne pas l'arrêter sur le
hash du fichier) : le vérificateur sort en **code 1** parce que l'empreinte de l'entrée ne
correspond plus et que la sérialisation/le décodage échouent. Un fichier corrompu n'est pas
absorbé silencieusement.

### 3.4 La porte et les tests

`bash tools/porte-cic.sh` :

```text
  42/42 verdicts · 42/42 empreintes · 42/42 sérialisations
  octet altéré : 36/36 rejetés · exhaustif eq(2,2) : 1020/1020 rejetés
  non-trivialité : accepte-tout 6 désaccords, rejette-tout 36 désaccords
  corpus corrompu : refusé (code 1)
  tests : 21 cas
✅ porte CIC verte
```

Les **21 tests** couvrent : le manifeste et la copie byte-identique, la structure du corpus, la
sérialisation canonique, les 42 empreintes, le rejeu 42/42, les six rejets, les sept preuves
arithmétiques (`add_zero`, `add_succ`, `add_comm`, `add_assoc`, `mul_zero`, `mul_succ`,
`mul_comm`), les trois contrôles négatifs, la substitution simultanée, le décodage strict
(octet en trop, étiquette inconnue, varint non canonique), la détection d'un corpus altéré, la
détection d'un verdict falsifié et le code de sortie de la CLI.

## 4. Ce qui pourrait rendre ce résultat faux

1. **Les 19 étiquettes non exercées.** Le corpus n'utilise que **20** des **39** étiquettes du
   format portable. Les règles `bool`, `list`, `expr`, `abort`, `fst`/`snd` sont implémentées
   mais **non mesurées** ici : un bug dans ces branches ne changerait pas les 42/42.
2. **L'indépendance est celle du code, pas celle des règles.** Le vérificateur Drave et le
   vérificateur Panini implémentent la même spécification CIC-lite. Une erreur de spécification
   (par exemple la règle de J, ou l'univers `U₀ : U₀` de Panini) serait reproduite par les deux.
   Le corpus prouve l'**accord d'implémentation**, pas la cohérence de la théorie sous-jacente.
3. **La conversion suit la spécification de Panini.** Le normaliseur est volontairement calqué
   sur les réductions β/ι/δ et l'η de Σ de la spécification ; il ne prétend pas être un
   vérificateur de CIC complet (pas de W, pas d'inductifs définis par l'utilisateur, pas de
   vérification de positivité — le fragment est fixe).
4. **Le contrôle « un octet » est un échantillon.** Il est exhaustif sur `eq(2,2)` (4 octets) et
   sur le **dernier** octet des 36 preuves acceptées. Il ne prouve pas que **toutes** les
   mutations d'un octet de **toutes** les preuves sont rejetées ; une mutation qui produirait un
   autre terme bien typé serait acceptée, et c'est correct du point de vue du typage. Le contrôle
   mesure la **sensibilité à la corruption**, pas l'injectivité du format.
5. **L'empreinte est une convention.** Le corpus déclare `sha256(preuve || type)` ; le
   vérificateur recalcule cette formule et la confronte aux 42 empreintes déclarées. Si la
   formule de Panini changeait, les 42 empreintes seraient à revalider — mais les verdicts, eux,
   ne dépendent pas de la formule.
6. **La copie portable est une copie.** Elle est byte-identique à la source
   (`3018f6f4…aaec`), mais une modification de la source Panini après le 2026-11-14 ne serait
   pas vue. Le manifeste fige le commit source et les deux empreintes.
7. **Le corpus reste petit.** 42 entrées, dont 6 rejets volontairement faux ; ce n'est pas une
   campagne de vérification formelle à grande échelle. Le résultat est un **verrou de portabilité**
   (« nos deux systèmes vérifient les mêmes preuves »), pas une preuve de correction du noyau
   Panini.

## 5. Ce que la fiche fixe

- **Le corpus d'or CIC est rejoué hors de Panini** : un noyau Drave indépendant rend **42/42**
  verdicts, sans importer le checker de Panini.
- **L'artefact est portable** : la copie `tools/tests/cic/corpus_dor_cic_v1.json` est
  byte-identique à la source, et le vérificateur ne lit que ce fichier.
- **Les empreintes sont vérifiées** : `sha256(preuve || type)` pour les 42 entrées, plus le
  sha256 du fichier.
- **Le contrôle négatif est exécuté** : 36/36 preuves acceptées rejetées après altération d'un
  octet, 1 020/1 020 mutations de `eq(2,2)` rejetées, non-trivialité vérifiée, corpus corrompu
  refusé.
- **La porte est rejouable** : `bash tools/porte-cic.sh` et les 21 tests.

La prochaine action de la ligne Panini est **J13.1** (la table des mesures), puis **J14.1**
(la passe et le tag).
