# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 23/46 textes à chevauchement de syntagmes

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `56eb43af` (module `c1a08588`, `tools/drave.py` `59a06f3e`) ·
> **Date** : 2026-11-06 · **Verdict** : ⚠️ **la surface est fiable ; le contrat ne l'est pas encore.**
> **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
> [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json).
>
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) (CLI : `analyser`, `evaluer`, `rejouer`,
> `--version`) et [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) ;
> **50 phrases libres** écrites pour l'audit (textes dans le JSON) ; harnais local non committé
> dans `/tmp` ; machine **Xeon E5-2687W v3**, Python **3.13.16**.
>
> **Snapshot.** HEAD a bougé pendant l'audit (`6ef2a3f5` → `56eb43af`). Le module a reçu à
> **11 h 34** le correctif « non-str / surrogate » (`c1a08588`) ; le banc a tourné à **11 h 40**,
> après ce correctif, et `drave.py` n'a pas changé. Les chiffres portent sur ce couple de hash ;
> un audit futur doit repartir du hash, pas de la date.

**En une phrase.** Sur **50 phrases libres**, la CLI **ne plante pas**, ne rend **aucun JSON
invalide**, garde **tous ses spans dans le texte**, ne perd **aucune cible** et rejoue **50/50** ;
mais **4 refus n'ont pas de JSON** (stdout vide, code 1), **23/46 succès** portent des syntagmes
qui se chevauchent, **4/46** n'ont **aucun syntagme**, **302/1068 tokens** n'ont **pas de POS**,
**6/46** textes ont une frontière de phrase cassée, et le JSON n'a **ni `schema` ni `version`**.
C'est un bon analyseur de surface ; ce n'est pas encore un contrat de produit.

| question | mesure |
|---|---:|
| plantages (traceback, code inattendu) | **0/50** |
| JSON invalide | **0/46** |
| sorties vides sur succès | **0/46** |
| refus | **4/50** (code 1, stdout 0 octet) |
| spans hors texte / spans vides | **0/4501** / **0** |
| clés racine ou étiquette manquantes | **0/46** / **0/4501** |
| cibles absentes du texte | **0/284** |
| déterminisme (deux passages) | **50/50** |
| chevauchements de syntagmes | **23/46** textes, **107** paires |
| textes sans aucun syntagme | **4/46** |
| tokens sans POS | **302/1068** (257 ponctuation, 45 nombres) |
| temps CLI (50 phrases) | **136,8–226,6 ms**, médiane **152,7 ms** |
| temps interne (API) | **0,2–45,1 ms**, médiane **1,0 ms** |

## 1. Dispositif

- **Banc libre** : 50 phrases écrites à la main pour cet audit — **41 françaises** (dont
  **1 très longue**, f50 : 2 144 caractères, 4 paragraphes), **5 anglaises**, **4 refus**
  (vide, espaces, ponctuation, emoji). Les textes couvrent questions, impératives, négations,
  majuscules, chiffres, dates, URL, emails, chemins, caractères spéciaux, accents, emoji,
  abréviations, citations, ellipses, latin et un texte multi-paragraphes. **Aucune phrase ne
  vient du gold.**
- **Mesure** : `python3 tools/drave.py analyser TEXTE --json` en **subprocess** (comme un
  utilisateur), deux passages par texte, plus `analyser` lisible en parallèle. Validation de
  **20 invariants** : clés, spans, `valeur` vs tranche, chevauchements, cibles, POS, unités,
  fraction, types, sources, confiance, tri, doublons, déterminisme.
- **Temps** : horloge murale du processus CLI (démarrage Python compris) et `Heuristique().analyser`
  en direct (durée interne, hors démarrage). Les deux sont rapportés par phrase dans le JSON.
- **Contrôle négatif** : **9 mutations** injectées dans une annotation valide (span hors texte,
  chevauchement, cible absente, confiance 1,7, clé manquante, fraction fausse, valeur hors span,
  attachement retiré, niveau inconnu) ; **9/9 détectées** (§ 6).
- **Portée** : le **CLI** et l'heuristique par défaut. Le neuronal, `Parallele`, `Cascade` et les
  profils UDHR ne sont pas mesurés ici ; un audit parallèle (A24) couvre l'API du bloc.

**Reproduire les cas cités** (depuis la racine du dépôt) :

```bash
python3 tools/drave.py analyser "Élodie sourit."          # SYNTAGMES —
python3 tools/drave.py analyser "Le chat dort." --json    # 11 clés, 19 étiquettes
python3 tools/drave.py analyser "" --json; echo $?        # stdout vide, code 1
python3 tools/drave.py analyser "Le prix est 12.5 euros." # deux phrases
python3 tools/drave.py evaluer --json                     # 222/222, 0,9289, 0,5849
python3 tools/drave.py rejouer "Le chat dort."            # rejeu identique : oui
```

## 2. Les 50 phrases : ce qui tient, ce qui casse

### 2.1 Ce qui tient

- **0 plantage** : aucun traceback, aucun code de sortie hors `{0, 1}`, aucun `stderr` sur succès.
- **0 JSON invalide** : les 46 succès se parsent ; 11 clés racine et 11 clés par étiquette,
  toujours les mêmes ; étiquettes triées, **0 doublon exact**, **0 span vide**, **0 span hors
  texte**, `valeur == texte[debut:fin]` pour les niveaux de surface.
- **0 cible absente** : les 284 chaînes de `meta.attachement.cible` existent dans le texte.
- **50/50 déterminisme** : deux invocations rendent le même octet ; `rejouer` est cohérent.
- **Refus propre** : texte vide, espaces, ponctuation, emoji → code **1**, stdout **0 octet**,
  message sur `stderr`, aucun JSON partiel.

### 2.2 Ce qui casse (chiffré)

| anomalie | mesure | où / exemple |
|---|---:|---|
| syntagmes qui se chevauchent | **107 paires** dans **23/46** textes ; **85/360** étiquettes `meta.union` | f02 : `REL 22-42` et `REL 22-54` ; f50 : 50 paires |
| partition après filtre `meta.union` | **0 conflit** | le filtre marche, mais n'est pas dans le schéma |
| textes sans aucun syntagme | **4/46** | f13 (emoji), f18 (chiffres), f27 « Élodie sourit. », f37 (email/téléphone) |
| POS manquantes | **302/1068** tokens | 257/257 ponctuations, 45/45 nombres ; 0/766 mots |
| `POS —` | **1/46** | f18, `1234567890` |
| frontière de phrase cassée | **6/46** textes | URL (f12, f38, f50), email (f37, f50), chemin (f39), abréviation (f20) |
| fausses questions | **3** | `?page=2` dans une URL → phrase `interrogative` |
| phrases qui se chevauchent | **1** paire | f20 : `[0:59]` et `[2:59]` sur `M. Dupont…` |
| phrases commençant par un espace | **19/76** | f03, f20, f25, f26, f29, f50 (14) |
| documents tronqués à 60 caractères | **17/49** | f50 : 4 titres tronqués |
| faux titres de document | **2/49** | f18 (`1234567890`), f31 (`ÇA NE MARCHE PAS !!!`) |
| langue fausse | **1/41 fr** | f33 « Si tu viens… » → `it` |
| langue `und` | **5** | f13, f18 (chiffres), f27, f37, f48 (latin) |
| cibles en mot fermé | **18/284** | `pas` (7), `est` (4), `ce`/`Ce` (4), `hier`, `ici`, `Nous` |
| cibles ambiguës par chaîne | **56/284** | cible présente >1 fois ; 9 cibles d'un caractère (`M`, `c`, `f`) |
| syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/215** non-GV |
| rôles non normalisés | **106** `predicat` vs **39** `prédicat` ; **17** `qualite` vs **11** `qualité` | filtre client fragile |
| `valeur` non uniforme | **295/4501** | phrase = type, pragmatique = acte, document tronqué, 4 morphèmes normalisés |

**23 ou 28 ?** Les **107 paires de syntagmes** concernent **23 textes**. Si l'on compte aussi les
étiquettes de **même span** (`phrase` type/négation, `pragmatique` acte/double sens), **28 textes**
portent au moins un chevauchement — mais ce sont des annotations multi-label attendues, pas des
conflits de structure. Le chiffre à retenir pour un client qui construit un arbre est **23/46**.

**Le cas « Élodie sourit. »** — une phrase canonique, 13 étiquettes, 2 unités sémantiques, mais
**aucun syntagme** :

```
langue=und script=Latn source=heuristique · 13 étiquettes · unités sémantiques=2 (85.7% du texte)
POS  Élodie/NOUN sourit/NOUN
SYNTAGMES —
PRAGMATIQUE
  phrase [0:14] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
```

Un client qui demande « les syntagmes » reçoit une section vide sans savoir si c'est un échec,
une limite ou un texte sans structure. Même chose pour `1234567890` (`POS —`, `SYNTAGMES —`,
0 unité, fraction 0,0).

**Les frontières de phrase.** `12.5` donne deux phrases (`[0:15]` et `[15:23]`), `12.03.2024`
en donne trois, `alice@example.org` deux, `Visitez https://example.com/docs?page=2` trois dont
une **fausse question** (`com/docs?`). `M. Dupont…` rend deux phrases qui se chevauchent
(`[0:59]` et `[2:59]`). C'est le défaut le plus visible pour un utilisateur qui segmente.

### 2.3 Les 4 refus du banc

| id | texte | longueur | code | stdout | message |
|---|---|---:|---:|---:|---|
| f14 | `🚀` | 1 | 1 | 0 | `refus d'analyse : vide` |
| f15 | `` (vide) | 0 | 1 | 0 | `refus d'analyse : vide` |
| f16 | `   ` | 3 | 1 | 0 | `refus d'analyse : vide` |
| f17 | `...` | 3 | 1 | 0 | `refus d'analyse : vide` |

Le comportement est **documenté** (code 1, stdout vide) ; le problème est qu'il est **indistinguable
d'une erreur** et qu'aucun JSON n'est rendu. Pour un client `--json`, `json.loads("")` échoue ;
il doit parser `stderr` pour savoir s'il s'agit d'un refus. La raison `vide` est de plus **fausse**
pour l'emoji et la ponctuation : le texte n'est pas vide, il ne contient ni lettre ni chiffre.

### 2.4 Temps

| mesure | min | médiane | moyenne | p95 | max |
|---|---:|---:|---:|---:|---:|
| CLI, 50 phrases (ms) | **136,8** | **152,7** | **157,3** | **180,3** | **226,6** (f50) |
| interne API (ms) | **0,2** | **1,0** | **2,2** | **2,0** | **45,1** (f50) |
| JSON produit (octets) | 2 126 | 13 510 | 26 205 | 22 841 | **533 611** (f50) |

Le **démarrage** (`--version`, 10 passages) coûte **134–192 ms**, médiane **146 ms**. Pour une
phrase courte, **plus de 95 % du temps CLI est le démarrage**, pas l'analyse (0,8 ms pour f01).
`evaluer` coûte **530–543 ms** sur le gold vivant et **577–600 ms** avec `--gold` ; `rejouer`
**146–149 ms**. Les cinq textes les plus lents en CLI
sont f50 (226,6 ms), f02 (193,8), f05 (181,6), f35 (180,3), f44 (179,1) — l'ordre est surtout
du bruit de démarrage, sauf f50. En interne, les plus lents sont f50 (45,1 ms), f43 (7,9),
f20 (2,4), f06 (2,0), f38 (1,9). Le détail par phrase est dans le JSON
(`banc_50.resultats[].temps_cli_ms` et `temps_api_ms`).

**Passage à l'échelle** (même texte répété, mesure interne, après chauffe) :

| caractères | 1 000 | 2 000 | 5 000 | 10 000 | 20 000 | 50 000 |
|---|---:|---:|---:|---:|---:|---:|
| ms | 27,5 | 37,5 | 125,0 | **331,6** | 1 025,7 | **5 438,9** |
| étiquettes | 1 042 | 2 077 | 5 187 | 10 362 | 20 719 | 51 792 |
| JSON (Mo) | 0,23 | 0,46 | 1,13 | **2,26** | 4,59 | **11,52** |

Le coût est **superlinéaire** (×16,4 de temps pour ×5 de texte entre 10 k et 50 k) ; à 10 000
caractères, le CLI reste sous la seconde, mais le JSON fait **2,76 Mo** (indenté). Un document
de 50 000 caractères coûte **5,4 s** et **11,5 Mo** : il n'y a ni plafond ni mode compact.

## 3. Robustesse des entrées

### 3.1 Codes et arguments

| cas | code attendu | code observé | stdout | constat |
|---|---:|---:|---:|---|
| `--version`, `--aide` | 0 | **0** | oui | conforme |
| aucune commande, commande inconnue, texte manquant | 2 | **2** | 0 | conforme |
| `--langue de`, `--langue FR`, option inconnue | 2 | **2** | 0 | conforme (choix `fr\|en`) |
| texte commençant par `--` (`--bonjour`) | 0 | **2** | 0 | **anomalie** : pris pour une option |
| même texte avec `--` séparateur | 0 | **0** | oui | conforme |
| texte `-3 degrés` | 0 | **0** | oui | conforme (argparse accepte) |
| un mot (`Bonjour`), un caractère (`a`) | 0 | **0** | oui | conforme ; 7 et 8 étiquettes (0 et 1 syntagme) |
| caractères spéciaux (f40 : `@ # $ % & * ( ) [ ] { } < > ~ ^`, barre verticale et antislash) | 0 | **0** | oui | 76 étiquettes, 0 plantage ; la barre et l'antislash sont des tokens de ponctuation |
| texte vide / espace / tabs | 1 | **1** | **0** | conforme, refus |
| ponctuation seule / emoji / espace invisible | 1 | **1** | **0** | refus correct, **raison `vide` fausse** |
| `--json` avant le texte | 0 | **0** | oui | conforme |
| nouvelle ligne, tabulation, CRLF | 0 | **0** | oui | conforme |

Les codes **0 / 1 / 2** existent ; les codes **3 (refus distinct)** et **4 (dépendance absente)**
du contrat cible ne sont **pas implémentés** — le refus reste un code 1.

### 3.2 Encodages

| cas | résultat |
|---|---|
| UTF-8 valide (`Élodie sourit.`) | 0, JSON UTF-8 non échappé |
| **NFD** (`e` + accent combinant) | 0, mais tokens `e` / `́` / `lodie` ; **0 syntagme** ; POS `NOUN` pour `e` et `lodie` |
| BOM (`\ufeffLe chat dort.`) | 0 ; le BOM devient un token de **ponctuation** `[0:1]` |
| **octet UTF-8 invalide seul** (`\xff`) | 1, refus **`vide`** (pas `encodage`), stdout 0 |
| **octet invalide dans un mot** (`a\xffb`) | 1, **`UnicodeEncodeError` interne** à l'écriture du JSON, stdout 0 |
| stdout **ASCII** (`PYTHONIOENCODING=ascii`) | 1, **`UnicodeEncodeError` interne** (le tiret `—` de l'en-tête) |
| `LC_ALL=C` | 0, UTF-8 sort quand même (mode UTF-8 de Python 3.13) |

Deux **échecs internes** subsistent : l'UTF-8 invalide mêlé à des lettres et le stdout ASCII.
Aucun n'émet de traceback, mais le message est `drave: erreur : UnicodeEncodeError` — pas un
refus d'encodage explicite.

### 3.3 Les 10 000 caractères

| texte | code | temps CLI | étiquettes | JSON | constat |
|---|---:|---:|---:|---:|---|
| 10 000 car., phrases répétées | 0 | **590–765 ms** | 10 362 | **2 763 666 o** | spans valides, déterminisme |
| 10 000 car., `a` × 10 000 | 0 | **172 ms** | 7 | 42 482 o | un seul token |
| 10 000 car., ponctuation | 1 | **155 ms** | — | 0 | refus `vide` (raison fausse) |
| mode lisible, `a` × 10 000 | 0 | 153 ms | — | 10 457 o | **ligne de 10 010 caractères** |

Le texte de 10 000 caractères **ne plante pas** et garde tous ses spans ; le coût reste sous la
seconde. En revanche, la sortie lisible d'un token de 10 000 caractères n'est pas coupée
(`break_long_words=False`) et envahit le terminal.

### 3.4 Scripts non latins et entrées non-str

- **Russe, arabe, chinois** : code 0, script correct (`Cyrl`, `Arab`, `Hani`), langue `und`,
  **0 syntagme**, POS `NOUN` (russe) ou `MOT` (arabe, chinois). Surface seulement.
- **API non-str** (`None`, `3`, `[1,2]`, `b"abc"`) : `refus = "non_texte"`, 0 étiquette, pas de
  plantage — le correctif `c1a08588` tient. Le CLI, lui, ne peut recevoir que des chaînes.

## 4. Le contrat de sortie

### 4.1 Ce qui est toujours présent

Sur les **46 succès** :

- **11 clés racine** : `texte`, `langue`, `script`, `source`, `refus`, `etiquettes`,
  `unites_semantiques`, `fraction_semantique`, `trace`, `cout`, `contexte` — **46/46**.
- **11 clés par étiquette** : `niveau`, `type`, `valeur`, `debut`, `fin`, `source`, `confiance`,
  `candidats`, `langue`, `script`, `meta` — **4501/4501**.
- **Invariants tenus** : étiquettes triées (46/46), `0` doublon exact, `0` span vide, `0` span
  hors texte, `confiance ∈ [0,1]` (4501/4501), `source` dans l'enum, `niveau` dans les 9,
  `texte` inchangé, `stderr` vide, déterminisme 46/46.

### 4.2 Ce qui peut être vide

| élément | constat sur le banc |
|---|---|
| `etiquettes` | vide seulement sur refus (0/46 succès) |
| `unites_semantiques` / `fraction_semantique` | **f18** : 0 unité, fraction 0,0 ; max 0,8571 (f03) |
| syntagmes | **4/46** succès sans syntagme : f13, f18, f27, f37 |
| `pos` | **1/46** : f18 (chiffres) ; sinon 3 à 200 POS |
| `candidats` | **3470/4501** étiquettes : graphème, mot, phrase, document, POS fermées |
| `meta` | **3375/4501** : graphème, mot, phrase, pragmatique, discours, document, morphème |
| `contexte` | **46/46 vide** : le CLI n'a aucune option pour le fournir |
| `refus` | **46/46 vide** en succès ; `vide` sur refus ; `non_texte` côté API |
| `cout` | 3 clés en succès (`octets`, `caracteres`, `etiquettes`) ; 1 clé (`octets`) sur refus API |
| `trace` | 2 schémas en succès : `{langue...}` puis `{niveaux...}` ; 1 schéma `{refus...}` |

**Conséquence** : un client ne peut pas supposer que `meta`, `candidats`, `trace` ou `cout` ont
un schéma fixe ; il ne peut pas non plus supposer que `POS` ou `syntagmes` sont non vides.

### 4.3 Ce qui casserait un client

1. **Pas de version de format** : 0/46 annotations portent `schema`/`version` ; `--version` ne
   rend que `drave 0.1.0`. Impossible d'épingler un rejeu à un format.
2. **Refus sans JSON** : `--json` + texte vide/emoji/ponctuation → **stdout 0 octet**, code 1.
   Un pipeline `... --json | jq` casse ; le refus est confondu avec une erreur.
3. **Chevauchements** : 107 paires / 23 textes ; un arbre ou un index par offset casse. Filtrer
   `meta.union` donne **0 conflit**, mais ce n'est pas dans le schéma : le client doit lire la
   doc et filtrer lui-même, sans garantie de test.
4. **Cible sans offset** : 56/284 cibles apparaissent plusieurs fois ; 18 mots fermés ; 9 cibles
   d'un caractère. `texte.find(cible)` est ambigu ; il n'y a pas `cible_debut`/`cible_fin`.
5. **POS trouées** : 302/1068 tokens sans POS (toute la ponctuation, tous les nombres) ; un
   alignement token → POS a des trous ; `POS —` sur les chiffres.
6. **`valeur` non uniforme** : 295/4501 étiquettes ne portent pas la surface — `phrase` porte le
   type (`déclarative`), `pragmatique` l'acte, `document` une valeur tronquée à 60, `morphème`
   une forme normalisée. Un client qui slice `texte[debut:fin]` doit traiter chaque niveau.
7. **Frontières de phrase** : 6/46 textes coupés (URL, email, chemin, abréviation), 3 fausses
   questions, 1 paire de phrases chevauchantes. Les actes par phrase sont faux en conséquence.
8. **Structures vides** : 4/46 textes valides sans syntagme, dont « Élodie sourit. ». Le client
   ne distingue pas « rien trouvé » de « non supporté ».
9. **Enums instables** : `langue` peut être `it` (f33) ou `und` ; `Annotation.source` peut être
   `parallele`/`cascade` côté API ; `refus` a plusieurs sémantiques (`vide`, `non_texte`, erreurs
   neuronales).
10. **Taille et lot** : 2,76 Mo pour 10 000 caractères, 11,5 Mo pour 50 000 ; une invocation =
    un texte ; pas de JSONL, pas de `--fichier`, pas de stdin.

### 4.4 Le schéma minimal versionné (8 champs)

Le schéma **`drave.annotation` v1.0** garde **8 champs obligatoires** et laisse les autres en
extension optionnelle :

| # | champ | type | sens |
|---:|---|---|---|
| 1 | `schema` | `"drave.annotation"` | famille de format |
| 2 | `version` | `"1.0"` (MAJOR.MINOR) | version du format |
| 3 | `texte` | string | entrée, inchangée, pour interpréter les offsets |
| 4 | `langue` | string (`und` ou ISO 639) | langue détectée |
| 5 | `script` | string (`Zyyy` ou ISO 15924) | écriture |
| 6 | `refus` | string (`""` en succès) | refus explicite |
| 7 | `etiquettes` | array d'`Etiquette` (11 champs) | annotation |
| 8 | `unites_semantiques` | array de `{debut, fin}` | unités, triées et disjointes |

`fraction_semantique` est **dérivée** (somme des unités / `len(texte)`) : optionnelle.
`source`, `trace`, `cout`, `contexte` restent des extensions optionnelles. Un client **doit**
refuser un `version` MAJOR inconnu et **ignorer** les champs inconnus.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://drave.local/schema/annotation-1.0.json",
  "title": "drave.annotation v1.0",
  "type": "object",
  "required": ["schema", "version", "texte", "langue", "script", "refus",
               "etiquettes", "unites_semantiques"],
  "properties": {
    "schema": {"const": "drave.annotation"},
    "version": {"type": "string", "pattern": "^1\\.[0-9]+$"},
    "texte": {"type": "string"},
    "langue": {"type": "string", "pattern": "^(und|[a-z]{2,3})$"},
    "script": {"type": "string", "pattern": "^(Zyyy|[A-Z][a-z]{3})$"},
    "refus": {"type": "string"},
    "etiquettes": {"type": "array", "items": {"$ref": "#/$defs/etiquette"}},
    "unites_semantiques": {"type": "array", "items": {"$ref": "#/$defs/span"}}
  },
  "additionalProperties": true,
  "$defs": {
    "span": {
      "type": "object", "required": ["debut", "fin"],
      "properties": {"debut": {"type": "integer", "minimum": 0},
                     "fin": {"type": "integer", "minimum": 0}},
      "additionalProperties": false
    },
    "etiquette": {
      "type": "object",
      "required": ["niveau", "type", "valeur", "debut", "fin", "source",
                   "confiance", "candidats", "langue", "script", "meta"],
      "properties": {
        "niveau": {"enum": ["graphème", "morphème", "mot", "pos", "syntagme",
                            "phrase", "discours", "pragmatique", "document"]},
        "type": {"type": "string", "minLength": 1},
        "valeur": {"type": "string"},
        "debut": {"type": "integer", "minimum": 0},
        "fin": {"type": "integer", "minimum": 0},
        "source": {"enum": ["heuristique", "neuronal", "humain"]},
        "confiance": {"type": "number", "minimum": 0, "maximum": 1},
        "candidats": {"type": "array", "items": {"type": "string"}},
        "langue": {"type": "string"},
        "script": {"type": "string"},
        "meta": {"type": "object"}
      },
      "additionalProperties": true
    }
  }
}
```

**Politique de version.** MAJOR pour toute suppression, renommage ou changement de type/sémantique
d'un des 8 champs ; MINOR pour un champ optionnel, une valeur de `type` ou un code de `refus`.
`schema` et `version` sont présents **sur succès et sur refus** ; le refus est un code **3** avec
un JSON d'annotation vide (`etiquettes: []`), pas un stdout vide.

### 4.5 Le test de non-régression du schéma

Le test ci-dessous est **proposé** pour `tools/tests/test_schema_produit.py` (il n'est pas écrit
dans le dépôt : la mission n'autorise que deux fichiers neufs). Il a été **essayé à blanc** depuis
`/tmp` : `Ran 4 tests ... OK (skipped=1)` — les 4 tests du contrat actuel passent, la classe
`TestSchemaV1` est sautée tant que `schema` n'existe pas. Elle deviendra stricte dès P0-1 livré.

```python
"""test_schema_produit.py — le contrat de sortie de `drave analyser --json`.

Deux contrats cohabitent :

- **actuel** (drave 0.1.0) : 11 champs racine, 11 champs par étiquette, spans valides,
  déterminisme. Ce test passe sur le produit livré ; il gèle l'enveloppe et attrape une
  disparition de champ, un span hors texte ou une valeur qui n'est plus la surface.
- **cible v1** (`schema: "drave.annotation"`, `version: "1.0"`, 8 champs requis) : il est
  **sauté** tant que le champ `schema` n'existe pas, puis il devient strict. C'est le test
  de non-régression du schéma versionné : il échoue si `schema`/`version` disparaissent,
  si un des 8 champs manque, ou si le refus ne rend plus de JSON avec le code 3.

À placer dans `tools/tests/test_schema_produit.py`. Stdlib seulement, lancé par
`python3 tools/tests/test_schema_produit.py` ou `pytest`.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import unittest

RACINE = pathlib.Path(os.environ.get("DRAVE_RACINE")
                      or pathlib.Path(__file__).resolve().parents[2])
CLI = RACINE / "tools" / "drave.py"
SCHEMA = "drave.annotation"
VERSION = "1.0"

CHAMPS_ACTUELS = {"texte", "langue", "script", "source", "refus", "etiquettes",
                  "unites_semantiques", "fraction_semantique", "trace", "cout", "contexte"}
CHAMPS_V1 = {"schema", "version", "texte", "langue", "script", "refus",
             "etiquettes", "unites_semantiques"}
CHAMPS_ETIQUETTE = {"niveau", "type", "valeur", "debut", "fin", "source", "confiance",
                    "candidats", "langue", "script", "meta"}
NIVEAUX = {"graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
           "pragmatique", "document"}
SOURCES = {"heuristique", "neuronal", "humain"}
SURFACE = {"graphème", "mot", "pos", "syntagme"}  # morphème : valeur normalisée, document : tronquée
TEXTES = [
    "Le chat dort.",
    "The cat sleeps on the roof.",
    "Le livre que j'ai lu est intéressant.",
    "Bonjour. Salut.",
    "1234567890",
    "Élodie sourit.",
]


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE), capture_output=True, text=True, encoding="utf-8", timeout=120,
    )


def annoter(texte: str) -> tuple[subprocess.CompletedProcess[str], dict | None]:
    resultat = drave("analyser", texte, "--json")
    donnees = json.loads(resultat.stdout) if resultat.returncode == 0 else None
    return resultat, donnees


class TestContratActuel(unittest.TestCase):
    """Le contrat de drave 0.1.0 — doit rester vert tant que le schéma v1 n'est pas livré."""

    def test_enveloppe_et_etiquettes(self) -> None:
        for texte in TEXTES:
            with self.subTest(texte=texte):
                resultat, d = annoter(texte)
                self.assertEqual(resultat.returncode, 0, resultat.stderr)
                assert d is not None
                # Les 11 champs actuels restent obligatoires ; les 8 champs du schéma v1
                # peuvent s'ajouter sans casser ce test (transition P0-1).
                self.assertTrue(CHAMPS_ACTUELS <= set(d), sorted(CHAMPS_ACTUELS - set(d)))
                self.assertTrue(set(d) <= (CHAMPS_ACTUELS | CHAMPS_V1),
                                sorted(set(d) - (CHAMPS_ACTUELS | CHAMPS_V1)))
                self.assertEqual(d["texte"], texte)
                self.assertEqual(d["refus"], "")
                self.assertIsInstance(d["etiquettes"], list)
                self.assertGreater(len(d["etiquettes"]), 0)
                self.assertIsInstance(d["unites_semantiques"], list)
                tri = [(e["debut"], e["fin"], e["niveau"]) for e in d["etiquettes"]]
                self.assertEqual(tri, sorted(tri), "les étiquettes doivent être triées")
                for etiquette in d["etiquettes"]:
                    self.assertEqual(set(etiquette), CHAMPS_ETIQUETTE)
                    self.assertIn(etiquette["niveau"], NIVEAUX)
                    self.assertIn(etiquette["source"], SOURCES)
                    self.assertIsInstance(etiquette["type"], str)
                    self.assertTrue(etiquette["type"])
                    self.assertIsInstance(etiquette["valeur"], str)
                    self.assertIsInstance(etiquette["debut"], int)
                    self.assertIsInstance(etiquette["fin"], int)
                    self.assertTrue(0 <= etiquette["debut"] <= etiquette["fin"] <= len(texte))
                    self.assertTrue(0.0 <= etiquette["confiance"] <= 1.0)
                    self.assertIsInstance(etiquette["candidats"], list)
                    self.assertTrue(all(isinstance(c, str) for c in etiquette["candidats"]))
                    self.assertIsInstance(etiquette["meta"], dict)
                    if etiquette["niveau"] in SURFACE:
                        self.assertEqual(etiquette["valeur"],
                                         texte[etiquette["debut"]:etiquette["fin"]])

    def test_determinisme(self) -> None:
        for texte in TEXTES[:3]:
            with self.subTest(texte=texte):
                premier, _ = annoter(texte)
                second, _ = annoter(texte)
                self.assertEqual(premier.returncode, 0, premier.stderr)
                self.assertEqual(premier.stdout, second.stdout)

    def test_refus_actuel_ou_cible(self) -> None:
        """0.1.0 : refus = code 1, stdout vide. Cible : code 3 + JSON. Les deux passent.

        La classe TestSchemaV1 exige le code 3 ; ce test-ci ne gèle que le fait qu'un refus
        ne doit jamais être confondu avec un succès.
        """
        resultat = drave("analyser", "", "--json")
        if resultat.returncode == 3:
            d = json.loads(resultat.stdout)
            self.assertTrue(d["refus"])
            self.assertEqual(d["etiquettes"], [])
            self.assertEqual(d["unites_semantiques"], [])
        else:
            self.assertEqual(resultat.returncode, 1)
            self.assertEqual(resultat.stdout, "")
            self.assertIn("refus d'analyse", resultat.stderr)

    def test_codes_de_sortie(self) -> None:
        self.assertEqual(drave("--version").returncode, 0)
        self.assertEqual(drave().returncode, 2)
        self.assertEqual(drave("analyser", "Le chat dort.", "--langue", "de").returncode, 2)
        self.assertEqual(drave("analyser", "--", "--bonjour").returncode, 0)  # le `--` protège
        self.assertEqual(drave("analyser", "--bonjour").returncode, 2)       # sans lui, usage


class TestSchemaV1(unittest.TestCase):
    """Le schéma cible versionné — sauté tant que P0-1 n'est pas livré."""

    @classmethod
    def setUpClass(cls) -> None:
        resultat, d = annoter("Le chat dort.")
        if d is None or "schema" not in d:
            raise unittest.SkipTest("schéma v1 non livré : `schema` absent de l'annotation")

    def test_les_8_champs_et_la_version(self) -> None:
        for texte in TEXTES:
            with self.subTest(texte=texte):
                resultat, d = annoter(texte)
                self.assertEqual(resultat.returncode, 0, resultat.stderr)
                assert d is not None
                self.assertTrue(CHAMPS_V1 <= set(d), sorted(CHAMPS_V1 - set(d)))
                self.assertEqual(d["schema"], SCHEMA)
                self.assertRegex(d["version"], rf"^{re.escape(VERSION.split('.')[0])}\.\d+$")
                self.assertIsInstance(d["texte"], str)
                self.assertIsInstance(d["langue"], str)
                self.assertRegex(d["langue"], r"^(und|[a-z]{2,3})$")
                self.assertIsInstance(d["script"], str)
                self.assertIsInstance(d["refus"], str)
                self.assertIsInstance(d["etiquettes"], list)
                self.assertIsInstance(d["unites_semantiques"], list)

    def test_refus_code_3_et_json(self) -> None:
        """La cible : le refus rend un JSON d'annotation, avec un code distinct des erreurs."""
        resultat = drave("analyser", "", "--json")
        self.assertEqual(resultat.returncode, 3, resultat.stderr)
        d = json.loads(resultat.stdout)  # un JSON valide, pas un stdout vide
        self.assertTrue(CHAMPS_V1 <= set(d), sorted(CHAMPS_V1 - set(d)))
        self.assertTrue(d["refus"])
        self.assertEqual(d["etiquettes"], [])
        self.assertEqual(d["unites_semantiques"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

**Intégration** : ajouter `python3 tools/tests/test_schema_produit.py` à `tools/porte-produit.sh`
(après le smoke test) et faire échouer la porte si le code sort ≠ 0. Le test actuel gèle
les 11 champs de l'enveloppe et n'admet, en plus, que les 8 champs du schéma v1 ; le test v1
gèle les 8 champs, `schema`, `version` et le refus code 3.

## 5. Correctifs produit

Sauf mention, les lignes sont celles de [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py)
au commit `56eb43af` (module `c1a08588`). Les coûts sont des estimations d'ingénieur, pas des
mesures ; les risques disent ce qui peut bouger dans le gold.

### Bloquants

| # | correctif | preuve chiffrée | lignes | coût | risque |
|---|---|---|---|---|---|
| **P0-1** | **Versionner le format** : `schema` + `version` dans chaque annotation, `--version` les affiche | **0/46** annotations ; impossible d'épingler un rejeu | `drave.py` 50-52, 324 ; `bloc_linguistique.py` 116-127 | **2 h** | faible : champs additifs, test de schéma à ajouter |
| **P0-2** | **Refus en JSON + code 3** (le refus n'est plus une erreur) | **6 refus CLI** : stdout 0 octet, code 1 ; code 3 absent | `drave.py` 154-164, 265-272, 310-311 ; `bloc_linguistique.py` 1012-1017 | **2 h** | faible : JSON d'annotation sur stdout, code 3, docs/tests |
| **P0-3** | **Partition explicite des syntagmes** : `meta.alternative` + filtre `union` documenté (ou suppression mesurée) | **107 paires / 23 textes** ; 85 `union` ; 0 conflit après filtre | `bloc_linguistique.py` 1099-1156, 1179-1204, 1820-1849 | **0,5–1 j** | moyen : change F1/attachement ; préférer l'alternative étiquetée à la suppression |
| **P0-4** | **Frontières de phrase et tokénisation** : décimaux, URL, emails, chemins, abréviations | **6/46** textes coupés ; **3** fausses questions ; `12.5` → 2 phrases, `12.03.2024` → 3 | `bloc_linguistique.py` 549-565, 568-587 (550, 570, 579) | **0,5–1 j** | moyen : change le nombre de phrases et les actes ; tests dédiés |

### Importants

| # | correctif | preuve chiffrée | lignes | coût | risque |
|---|---|---|---|---|---|
| **P1-1** | **Cible d'attachement offsettée** (`cible_debut`/`cible_fin`) et désambiguïsée | **56/284** cibles apparaissent >1 fois ; **18** mots fermés ; **9** cibles de 1 caractère | `bloc_linguistique.py` 1145-1156, 1168-1176, 1195-1203 | **4 h** | faible : ajout dans `meta.attachement` |
| **P1-2** | **POS pour nombres et ponctuation** (`NUM`, `PONCT`) | **302/1068** tokens sans POS ; `POS —` sur les chiffres | `bloc_linguistique.py` 601-623, 1039-1049 | **2 h** | faible-moyen : vérifier l'exactitude gold |
| **P1-3** | **Langue** : éviter `fr → it`, documenter `und` | f33 → `it` ; 35/41 fr, 5/5 en, 5 `und` | `bloc_linguistique.py` 199-224, 273-296, 540-545 | **2 h** | faible : seuil et mots-outils |
| **P1-4** | **Au moins un syntagme sur une phrase simple** (GN + GV) | **4/46** succès sans syntagme, dont « Élodie sourit. » | `bloc_linguistique.py` 855-1000 (884-999) | **0,5 j** | moyen : touche le F1 gold |
| **P1-5** | **Encodage** : UTF-8 invalide, NFD, stdout non UTF-8 | 2 échecs internes ; NFD → 2 tokens ; ASCII → échec | `bloc_linguistique.py` 144, 549, 1003-1017 ; `drave.py` 382-384 | **2 h** | faible : refus `encodage`, NFC sans changer les offsets |
| **P1-6** | **Alternatives mortes `url`/`emoji`** | **0/1068** tokens `url`/`emoji` ; `https` → `mot`, emoji → `ponctuation` | `bloc_linguistique.py` 550 | **30 min** | faible : ordre des alternatives |
| **P1-7** | **Compacité et lot** : `--compact`, JSONL, `--fichier`/stdin | **2,76 Mo** pour 10 k ; **11,5 Mo** pour 50 k ; 1 texte par appel | `drave.py` 50-52, 329-341 | **0,5–1 j** | faible : option additive |
| **P1-8** | **`rejouer` une annotation sauvegardée** | on ne peut pas rejouer le JSON d'hier | `drave.py` 265-287, 357-368 | **4 h** | faible : `--annotation` + canonique |
| **P1-9** | **`candidats` structurés et `role` normalisé** | candidats = chaînes ; `predicat` 106 vs `prédicat` 39, `qualite` 17 vs `qualité` 11 | `bloc_linguistique.py` 1147-1156, 1177-1181, 1201-1209, 939-942 | **4 h** | faible : ajout d'objets `{span, cible}` |

### Confort

| # | correctif | preuve chiffrée | lignes | coût |
|---|---|---|---|---|
| **P2-1** | Document : valeur non tronquée et titre sûr | **17/49** valeurs à 60 car. ; 2 faux titres | `bloc_linguistique.py` 1222-1236 | **2 h** |
| **P2-2** | Sortie lisible : phrase et tokens longs | ligne de **10 010** car. ; `phrase [0:15] déclarative` affiche le type, pas le texte | `drave.py` 71-75, 86-148 | **2 h** |
| **P2-3** | `contexte` : l'exposer ou le retirer | **46/46** vide ; aucune option CLI | `bloc_linguistique.py` 1237-1239 ; `drave.py` 329-341 | **1 h** |
| **P2-4** | Figer `trace` et `cout` | `trace` 2 schémas ; `cout` 3 clés en succès, 1 sur refus | `bloc_linguistique.py` 1013-1021, 1246-1252 | **1 h** |
| **P2-5** | Graphème : couvrir les contrôles | newlines/tabs non étiquetés dans f50 | `bloc_linguistique.py` 1025-1037 | **15 min** |
| **P2-6** | Morphème : `valeur` = surface ou normalisée documentée | 4/104 : « Co » → `co` | `bloc_linguistique.py` 627-638, 1050-1053 | **30 min** |
| **P2-7** | `--version` : schéma et commit | `drave 0.1.0` seulement | `drave.py` 43, 324 | **30 min** |
| **P2-8** | Nettoyage `_verbe_dans` | deux boucles identiques | `bloc_linguistique.py` 770-787 | **15 min** |

**Total** : ≈ **12–20 h** de bloquants, **15–17 h** d'importants, **8 h** de confort, soit
**≈ 5–6 jours ingénieur** avec les tests et la doc. Les cinq prioritaires sont en § 8.

## 6. Contrôle négatif

Sur une annotation valide de « Le chat dort. » (0 chevauchement), **9 mutations** ont été
injectées et **9/9** ont été détectées par le validateur de l'audit :

| mutation | détectée par |
|---|---|
| span hors texte (`fin = len+1`) | `span_hors` |
| chevauchement de syntagme ajouté | `overlaps.syntagme` |
| cible absente (`zzz`) | `cibles_absentes` |
| confiance 1,7 | `types_inconnus` |
| clé `meta` retirée | `cles_label_ko` |
| `fraction_semantique = 0,99` | `fraction_ecart` |
| `valeur` hors span | `surface_ko` |
| attachement retiré | `sans_attachement` |
| `niveau = "foo"` | `types_inconnus` |

Ce contrôle ne dit rien de la **qualité sémantique** de la cible (une cible fermée comme `pas`
passe le test de présence) ; c'est précisément la limite P1-1.

## 7. Limites de l'audit

- **Pas de gold libre** : les 50 phrases n'ont pas de vérité sémantique ; on mesure la forme,
  les invariants et les cas limites, pas la justesse de l'analyse.
- **Banc écrit à la main** : 41 fr, 5 en, 4 refus ; il ne remplace pas un corpus aléatoire.
- **Une seule machine** (Xeon partagé) : les temps varient avec la charge ; les médianes sont
  plus fiables que les maxima. Les 590–765 ms du 10 k en sont un exemple.
- **Le module a changé pendant l'audit** (`c1a08588`, correctif non-str/surrogate) ; le banc est
  postérieur, mais un audit futur doit repartir du hash. `drave.py` n'a pas changé.
- **CLI seulement** : `Parallele`, `Cascade`, le neuronal et les profils UDHR ne sont pas mesurés.
- **Chevauchements** : les **107 paires** dépendent du banc ; l'audit A24 en compte **132** sur
  son propre banc. Les deux chiffres ne sont pas comparables ; le mécanisme, lui, est le même.
- **Coûts** : estimations d'ingénieur, pas des mesures.

## 8. Conclusion — les 5 correctifs prioritaires

1. **P0-1 — Versionner le format** (`schema`, `version`) : sans cela, aucun client ne peut
   épingler un rejeu ; 0/46 annotations, 2 h.
2. **P0-2 — Refus en JSON + code 3** : 6 refus CLI rendent un stdout vide et un code 1 confondu
   avec une erreur ; 2 h.
3. **P0-3 — Partition explicite des syntagmes** : 107 paires sur 23/46 textes ; le filtre
   `meta.union` donne 0 conflit mais n'est pas contractualisé ; 0,5–1 j.
4. **P0-4 — Frontières de phrase et tokénisation** : 6/46 textes cassés (URL, email, chemin,
   abréviation), 3 fausses questions ; 0,5–1 j.
5. **P1-1 — Cibles d'attachement offsettées** : 56/284 cibles ambiguës, 18 mots fermés, 0 offset ;
   4 h.

**Deux justes derrière** : **P1-2** (302/1068 tokens sans POS) et **P1-4** (4/46 textes sans
aucun syntagme, dont « Élodie sourit. »). Le produit est **utilisable en surface** aujourd'hui ;
il devient **intégrable** quand les cinq premiers points sont livrés, et **fiable pour un
utilisateur** quand P1-2 et P1-4 le sont aussi.

## Fichiers

- `reports/rapport-fiabilite-produit.md` — ce rapport.
- `reports/pensee-fiabilite-produit.json` — les 50 textes, les mesures par phrase, la robustesse,
  le contrat, le schéma JSON, le test complet et les correctifs.
- **Aucun fichier existant modifié ; aucun commit.** Les harnais sont dans `/tmp` et ne sont pas
  versionnés.
