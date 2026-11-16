# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-15** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
> existent, et la
> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le
> **prototype `--tagger auto`** (complété le **2026-11-15**, § 3.7) choisit l'API si une clé
> existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
> Le format
> est **version 2** (`schema: "drave.annotation"`,
> `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
> reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
> § 3.5 ont été relancées le 07/11 pour le format v2 ; les mesures chiffrées du § 2 datent du
> **06/11**, et l'`evaluer` du § 3.3 a été relancé le **16/11** (gold vivant 612, `--par-langue
> fr/en`, `--strict`) ; la fiche du mode strict est [`rapport-evaluer-strict.md`](../../reports/rapport-evaluer-strict.md).
> Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
> La **FAQ** (§ 8) est vérifiée à part le **2026-11-15** par
> [`tools/verifier_faq.py`](../../tools/verifier_faq.py) : **10/10** réponses.
>
> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
> candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.
>
> **Démarrage en 5 minutes** : le parcours pas à pas — clone, installation, les commandes,
> JSON, tagger optionnel et erreurs — est dans [`demarrage.md`](demarrage.md).

## Sommaire

- [1. À qui s'adresse le produit](#1-à-qui-sadresse-le-produit)
- [2. Ce que le produit fait](#2-ce-que-le-produit-fait)
- [3. Comment l'utiliser — cinq exemples réels](#3-comment-lutiliser--cinq-exemples-réels)
- [4. Ce que le produit ne fait pas encore](#4-ce-que-le-produit-ne-fait-pas-encore)
- [5. Performance](#5-performance)
- [6. Garanties](#6-garanties)
- [7. Le CLI livré — contrat et manques](#7-le-cli-livré--contrat-et-manques)
- [**8. FAQ — dix questions**](#8-faq--dix-questions)
- [9. Où aller ensuite](#9-où-aller-ensuite)

## 1. À qui s'adresse le produit

| vous êtes… | ce que vous obtenez | ce qu'il faut savoir |
|---|---|---|
| **linguiste, enseignant, curieux** | une analyse immédiate : POS, syntagmes, rôles, attachement, acte de parole | c'est une **annotation**, pas une traduction ni une correction |
| **développeur NLP** | un JSON déterministe, des spans, une confiance, des candidats | le format est **versionné** (schéma v2) ; v1 reste lue (§ 7) |
| **chercheur du dépôt** | le banc des fiches : gold 612, 239 cibles, rejeu | les règles sont dessinées sur ce gold : lire la **couverture**, pas seulement l'exactitude |

**Prérequis** : le dépôt, Python 3.10+ (testé en 3.13), **aucune dépendance externe**, aucun GPU,
aucun accès réseau **par défaut** (le tagger en option, lui, appelle l'API DeepSeek, § 3.7). Les
quatre gold sont versionnés dans `tools/tests/linguistique/` ; le corpus UDHR, lui, ne l'est pas
(voir § 4).

**Ce que ce n'est pas** : un produit grand public, un traducteur, un générateur, un correcteur,
un serveur. Le produit **lit** et **étiquette** ; il n'écrit pas de texte.

## 2. Ce que le produit fait

Une seule opération : `analyser(texte, langue)` → une **annotation**. Elle porte neuf niveaux ;
le produit en expose cinq, plus le coût et la trace. Le JSON est estampillé `schema`
(`"drave.annotation"`) et `version` (`2`) ; en v2, `meta.partition` et `meta.alternative`
documentent les syntagmes qui se chevauchent, `meta.attachement.candidats` publie les
candidats en **objets** `{span, cible, source}`, et `meta.role` appartient à un
**vocabulaire fermé** de huit rôles.

| ce que vous demandez | ce que vous obtenez | mesure du 15/11 |
|---|---|---|
| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; `drave profils` les expose, `--langue` reste un indice `fr`/`en`) |
| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger` |
| **syntagmes** | GN, GV, GP, REL, SUB, avec leur span | F1 **0,7902** ; tête **0,9029** (vivant 612) ; **0,7906** sur le réel 452 |
| **attachement** | par syntagme : `role`, `cible`, `candidats` (objets v2, chaînes d'affichage en lecture) | **238/239** exacts ; couverture **0,9958** ; exact sur span **1,0000** ; **2 139** candidats objets, **0** span faux |
| **pragmatique** | acte (assertion, question, exclamation), négation, modalité, double sens | acte **0,9967**, négation **0,9771**, modalité **0,9886**, double sens **0,9444** |
| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |
| **coût et trace** | octets, caractères, étiquettes, étapes | local, sans réseau |

**Ce que « attachement » veut dire.** Pour un syntagme, le bloc publie la **cible** à laquelle il
le rattache — le verbe pour un GN sujet ou un GP, l'antécédent pour une REL — et une liste de
**candidats**. C'est une lecture, avec sa confiance ; ce n'est pas un arbre syntaxique complet.

**Comment on le sait.** Le banc est le **gold 612** : 20 phrases `hand`, 432 réelles, 160
synthétiques ; **239 cibles** d'attachement ; **3 179 tokens**. Les règles ont été dessinées sur
ce gold : la mesure est **in-sample**, limitée par un split dev/test (153/153 et 69/69).

**Les contre-épreuves.** Le CLI imprime son propre plancher : **cible exacte tirée au hasard
1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat
aléatoire** dans les listes donne **42,14 %** de top-1 — et la **permutation des cibles**
**1,997/220 = 0,908 %** ; les deux donnent p = 0. Un chiffre sans sa contre-épreuve n'est pas un
résultat.

**Les trois bases.** Le **vivant 612** (POS 0,8625, F1 **0,7902**, attachement 238/239), le
**gelé 602** (0,7882, 234/239) et le **réel 452** (`--reel` : POS **0,8891**, F1 **0,7906**,
attachement 99,46 %). Les chiffres de la fiche v12 (0,6511/0,6482, 235/236) sont **datés** : ils
mesuraient le bloc avant la semaine du 07/11. Toujours lire la base avec le chiffre.

## 3. Comment l'utiliser — cinq exemples réels

Tout se lance **depuis la racine du dépôt**. Les commandes ci-dessous sont celles d'aujourd'hui ;
elles n'utilisent ni modèle, ni GPU, ni réseau. Les JSON complets et commentés sont dans
[`exemples.md`](exemples.md).

### 3.1 Analyser une phrase

```bash
python3 tools/drave.py analyser "Le chat dort."
```
```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
```

**Lecture.** La phrase est reconnue comme française, deux syntagmes sont posés, chacun avec sa
cible : le GN « Le chat » est rattaché à « dort », le GV « dort » à « chat ». Le gold `g001`
attend exactement ces deux spans et `assertion`. `POS` est la suite des mots ; `COUVERTURE` est
la **confiance maximale déclarée** par niveau, pas une précision.

### 3.2 Analyser en JSON et lire l'attachement

```bash
python3 tools/drave.py analyser "Le livre que j'ai lu est intéressant." --json \
  | jq -r '[.etiquettes[] | select(.niveau=="syntagme")
           | "\(.type) \(.valeur) → \(.meta.attachement.cible // "—")"] | join(" · ")'
```
```
GN Le livre → intéressant · REL que j'ai lu → livre · REL que j'ai lu est intéressant → livre · GV est intéressant → livre
```

**Lecture.** Un appel = **une annotation** ; les phrases sont des étiquettes de niveau `phrase`,
pas des objets séparés. La REL « que j'ai lu » est bien rattachée à « livre » (cas `g011` du
gold). Le JSON publie aussi une **seconde lecture d'union** (`meta.union: true`, span plus
large) : dans la sortie lisible, elle apparaît comme un **doublon REL** ; le JSON la marque
`union: true`, à filtrer pour une lecture unique (voir [`exemples.md`](exemples.md) § 2).

**Les candidats d'attachement, en objets (v2).** Le champ historique `candidats` reste une
liste de **chaînes d'affichage** ; le champ v2 `meta.attachement.candidats` donne les mêmes
candidats en objets `{span, cible, source}`, avec un span qui découpe exactement la cible :

```bash
python3 tools/drave.py analyser "Le chat dort." --json \
  | jq -r '.etiquettes[] | select(.niveau=="syntagme")
           | "\(.type) \(.valeur) role=\(.meta.role) → \(.meta.attachement.cible) · " +
             ([.meta.attachement.candidats[] | "\(.cible)[\(.span.debut):\(.span.fin)]"] | join(", "))'
```
```
GN Le chat role=agent → dort · dort[8:12]
GV dort role=predicat → chat · chat[3:7]
```

Un consommateur n'a plus à parser « « qui dort » → voisine » : il lit `cible` et `span`.
La **cible choisie** est toujours le premier objet ; un candidat dont la cible n'est pas
retrouvée dans le texte est écarté. Le détail et la mesure sont dans
[`rapport-contrat-json.md`](../../reports/rapport-contrat-json.md).

### 3.3 Mesurer sur le gold

```bash
python3 tools/drave.py evaluer
```
```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)
  tête      F1 90.29 %  (P 92.61 % / R 88.08 %)
  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture
ATTACHEMENT exact 99.58 % · couverture 99.58 % · exact sur span 100.00 % · top-k 98.74 %
  tête      couverture 100.00 % · top-k 99.16 %
PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %
FRACTION SÉMANTIQUE 54.76 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
```

**Lecture.** `exact 99.58 %` est le **rendement** (238/239 cibles) ; `exact sur span 100.00 %` est
l'**exactitude** sur les 238 segments dont le span est prédit. La seule cible restante (`g017`)
n'a pas de segment au bon span : c'est un plafond de **couverture**, pas d'attachement.
`--gold` mesure le gold gelé 602 (F1 78,82 %, POS 86,25 %). La commande sort **0** : elle ne
teste pas la cascade ; c'est le rôle de `--strict`.

**Par langue.** `--par-langue` rejoue la **même** mesure sur les deux sous-golds et ajoute un
bloc `PAR LANGUE` (et une clé `par_langue` au JSON) : phrases, tokens, cibles, POS, syntagmes,
attachement, pragmatique et contrôle négatif **par langue**. Le contrôle négatif est recalculé
sur les cibles de la langue ; les chiffres globaux, eux, ne bougent pas.

```bash
python3 tools/drave.py evaluer --par-langue
```
```
PAR LANGUE
  en  210 phrases · 1148 tokens · 88 cibles d'attachement
      POS 94.51 % (fermé 98.30 %, ouvert 90.54 %) · SYNTAGMES F1 86.56 % (tête 95.27 %)
      ATTACHEMENT exact 98.86 % · couverture 98.86 % · top-k 98.86 % · PRAGMATIQUE acte 99.52 %
      CONTRÔLE NÉGATIF cible exacte tirée au hasard 2.27 % (graine 0, 88 cibles)
  fr  402 phrases · 2031 tokens · 151 cibles d'attachement
      POS 81.59 % (fermé 90.92 %, ouvert 73.25 %) · SYNTAGMES F1 74.75 % (tête 87.33 %)
      ATTACHEMENT exact 100.00 % · couverture 100.00 % · top-k 98.68 % · PRAGMATIQUE acte 99.75 %
      CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.99 % (graine 0, 151 cibles)
```

**Ce que le détail par langue dit — et ne dit pas.** L'anglais est **au-dessus** du français en
POS (94,51 % contre 81,59 %) et en syntagmes (F1 86,56 % contre 74,75 %) ; l'attachement est
**exact dans les deux langues** sur les spans prédits (87/87 et 151/151). Mais les deux golds ne
sont **pas de même composition** : l'anglais est fait de 210 phrases réelles (dont 6 `hand`),
le français ajoute **160 phrases synthétiques** au lexique disjoint. Le contrôle sur le seul
gold réel (`hand` + `reel`) donne encore l'anglais devant (POS 94,51 contre 84,08 ; F1 86,56
contre 72,58) : l'écart n'est donc pas *seulement* un effet du synthétique, mais il reste
**confondu avec la source**. Lire la langue avec la source, jamais l'une sans l'autre. La fiche
complète est [`rapport-evaluer-langue.md`](../../reports/rapport-evaluer-langue.md).

**Le mode strict — `--strict`.** Le banc de recherche mesure quatre modes et un plancher ; le CLI
le fait maintenant en une commande, **hors ligne** (`MockNeuronal`, pas de GPU, pas de clé) :

```bash
python3 tools/drave.py evaluer --strict
```
```
drave 0.1.0 — évaluation stricte (cascade locale, plancher 0.70)
gold vivant 612 phrases · 3179 tokens · gold réel 452 phrases · 2480 tokens

GOLD VIVANT 612
mode               POS        ΔPOS  SYNT. F1         ΔF1   TÊTE F1       ΔTÊTE
heuristique    86.25 %           —   79.02 %           —   90.29 %           —
neuronal       75.40 %  -10.85 pts   76.51 %   -2.51 pts   88.07 %   -2.22 pts
parallèle      86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts
cascade        86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts
cascade : 612 appels neuronaux sur 612 phrases

GOLD RÉEL 452
mode               POS        ΔPOS  SYNT. F1         ΔF1   TÊTE F1       ΔTÊTE
heuristique    88.91 %           —   79.06 %           —   89.90 %           —
neuronal       76.21 %  -12.70 pts   74.48 %   -4.58 pts   86.97 %   -2.93 pts
parallèle      88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts
cascade        88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts
cascade : 452 appels neuronaux sur 452 phrases

PLANCHER 0.70 — cascade POS 86.25 % (612) ✅ · 88.91 % (452) ✅ — code 0
CONTRÔLE NÉGATIF cascade dégradée (POS forcé à X) · POS 0.00 % < 0.70 ✅ (échec attendu, code 1)
```

**Ce qu'il fait.** Il mesure les **quatre modes** — heuristique, neuronal (`MockNeuronal`),
parallèle, cascade — sur le gold vivant **612** et sur le réel **452**, puis affiche le
**delta** de chaque mode contre l'heuristique (POS, F1, tête). Le **plancher 0,70** porte sur
l'**exactitude POS de la cascade** : si l'un des deux golds est sous 0,70, la commande sort en
**code 1**. Ici la cascade vaut **86,25 %** (612) et **88,91 %** (452) : **code 0**.

**Le contrôle négatif est dans la passe.** Une cascade dont le POS est forcé à `X` tombe à
**0,0000** et le rapport porte `code: 1` : le plancher mord. Le JSON (`--json`) ajoute
`strict`, `plancher`, `modes`, `delta`, `verdict` et `controle_negatif` ; le test
[`test_evaluer_strict.py`](../../tools/tests/test_evaluer_strict.py) vérifie aussi qu'un
verdict faux fait sortir `cmd_evaluer` en **1**. `--strict` est **exclusif** avec `--gold`
(le gold gelé), `--tagger` (l'API) et `--par-langue` : ces options sortent en **5** plutôt
que d'être ignorées. La fiche complète, avec les limites du mock, est
[`rapport-evaluer-strict.md`](../../reports/rapport-evaluer-strict.md).

### 3.3 quater Traiter un corpus

```bash
python3 tools/drave.py analyser --fichier corpus.txt --jsonl   # une ligne JSON par phrase
python3 tools/drave.py analyser --fichier corpus.txt --json    # le texte entier
```

`--fichier` lit un texte UTF-8 ; `--jsonl` rend une **ligne JSON par phrase** (le format des
traitements de corpus), chaque ligne portant le schéma **v2** complet (`version: 2`).

### 3.3 bis La vue des syntagmes qui se chevauchent — les champs du schéma v2

```bash
python3 tools/drave.py analyser "Le chat de la voisine qui dort sur le toit se réveille." --partition filtrer
```

Quatre vues (`--partition`) : `alternative` (défaut : les deux segments restent, `meta.alternative`
dit lequel est préféré — **aucune perte**), `filtrer` (vue linéaire : **F1 +0,047** mais **18
attachements en moins**), `filtrer_union` (variante économique, 91 paires résiduelles) et `brut`
(l'ancienne sortie). Le défaut est `alternative`.

**Deux champs additifs et optionnels.** Un segment qui appartient à un **groupe de chevauchement**
(au moins deux syntagmes dont les spans s'intersectent) porte `meta.partition` et
`meta.alternative` ; les autres n'en portent pas, et `meta` reste **ouvert** pour les clés
habituelles (`role`, `attachement`, `union`, `ouvert`, `contexte`). Les deux champs sont typés dans
le [schéma v2](../../tools/schemas/drave-annotation-v2.json), qui laisse `meta` ouvert mais
**ferme** chaque alternative (`additionalProperties: false`).

**`meta.partition` — la place du segment dans son groupe.**

| champ | type | contrainte | sens |
|---|---|---|---|
| `groupe` | entier | `≥ 0` | identifiant du groupe de chevauchement, stable dans l'annotation |
| `rang` | entier | `≥ 1` | rang du segment dans le groupe ; `1` = segment préféré (chunker `union`, puis le plus large, puis le plus sûr) |
| `membres` | entier | `≥ 2` | nombre de segments du groupe |
| `vue` | énumération | `alternative`, `filtrer_union`, `filtrer` | vue qui a produit l'annotation (`brut` n'écrit pas ces champs) |

**`meta.alternative` — les autres segments du groupe, vus depuis le porteur.**

| champ | type | contrainte | sens |
|---|---|---|---|
| `type` | énumération | `GN`, `GV`, `GP`, `REL`, `SUB` | type du segment alternatif |
| `debut`, `fin` | entiers | `0 ≤ debut < fin` | span en **points de code Unicode**, 0-based, `[debut:fin)` |
| `source` | énumération | `heuristique`, `neuronal`, `humain` | provenance du segment |
| `union` | booléen | — | le segment vient de l'union S/chunker |
| `relation` | énumération | `inclut`, `inclus`, `meme_span`, `croise` | relation **du point de vue du porteur** : `inclut` = le porteur contient l'alternative ; `inclus` = l'alternative contient le porteur ; `croise` = intersection partielle |
| `rang` | entier | `≥ 1` | rang de l'alternative dans le groupe |
| `retire` | booléen | optionnel | présent en vue `filtrer`/`filtrer_union` ; `true` = segment retiré de la sortie mais toujours lisible ici |
| `attachement` | objet | optionnel, `{segment, cible, candidats?}` | attachement recopié de l'alternative, avec ses candidats objets quand ils existent |
| `role` | chaîne | optionnelle, vocabulaire fermé | rôle normalisé recopié de l'alternative, quand il existe |

**`meta.attachement.candidats` — les candidats en objets (v2).**

| champ | type | contrainte | sens |
|---|---|---|---|
| `span` | objet | `{debut, fin}`, `0 ≤ debut < fin` | position de la cible dans `texte`, en points de code Unicode, fin exclue |
| `cible` | chaîne | non vide | surface du candidat ; `texte[debut:fin] == cible` |
| `source` | énumération | `heuristique`, `neuronal`, `humain` | provenance du candidat |

La cible choisie est le premier objet de la liste ; les `meta.alternative[].attachement`
recopient les mêmes objets. Le champ **historique** `candidats` de l'étiquette reste une
liste de chaînes : c'est la sortie lisible, et le contrat v1 ne connaît que lui.

```json
{
  "type": "REL", "debut": 22, "fin": 42, "valeur": "qui dort sur le toit",
  "meta": {
    "partition": {"groupe": 0, "rang": 2, "membres": 3, "vue": "alternative"},
    "alternative": [
      {"type": "REL", "debut": 22, "fin": 54, "source": "heuristique",
       "union": true, "relation": "inclus", "rang": 1,
       "attachement": {
         "segment": "qui dort sur le toit se réveille", "cible": "réveille",
         "candidats": [
           {"span": {"debut": 46, "fin": 54}, "cible": "réveille", "source": "heuristique"}
         ]},
       "role": "qualite"},
      {"type": "GV", "debut": 43, "fin": 54, "source": "heuristique",
       "union": false, "relation": "croise", "rang": 3,
       "attachement": {
         "segment": "se réveille", "cible": "voisine",
         "candidats": [
           {"span": {"debut": 14, "fin": 21}, "cible": "voisine", "source": "heuristique"}
         ]},
       "role": "predicat"}
    ]
  }
}
```

**Lecture.** Le porteur `REL [22:42]` est le **rang 2** d'un groupe de **3** segments ; ses deux
alternatives sont au rang 1 (la REL longue `[22:54]`, qui le **contient** : `inclus`) et au rang 3
(le GV `[43:54]`, qui le **croise**). Le champ `union` dit lesquelles viennent de l'union
S/chunker ; `vue` dit dans quelle vue le groupe a été écrit. En `filtrer`, le segment écarté
n'apparaît plus dans `etiquettes` mais reste décrit dans `meta.alternative` avec `retire: true` :
**la perte est documentée, pas silencieuse**. Le schéma vérifie la **forme** ; les invariants
sémantiques (réciprocité des relations, unicité des groupes, rangs permutés) sont couverts par les
tests du bloc, pas par le validateur JSON.

**La rétro-compatibilité v1.** Les **huit champs obligatoires** de la racine (`schema`, `version`,
`texte`, `langue`, `script`, `refus`, `etiquettes`, `unites_semantiques`) sont **les mêmes** en v1
et en v2 ; le bump n'ajoute que deux champs optionnels dans `meta`. Un client v1 qui ne lit pas
`meta` continue donc de lire l'annotation. En revanche, la **compatibilité octet pour octet** n'est
pas garantie : le passage à `version: 2` change le JSON et son `sha256` de rejeu.

| `version` de l'annotation | schéma choisi | résultat |
|---:|---|---|
| `1` | [`drave-annotation-v1.json`](../../tools/schemas/drave-annotation-v1.json) (inchangé) | lu et validé |
| `2` | [`drave-annotation-v2.json`](../../tools/schemas/drave-annotation-v2.json) | lu et validé |
| autre | — | refusé (version inconnue) |

`tools/verifier_schema_produit.py` lit `version` et choisit le schéma ; il compile les deux une
fois, puis valide les cas de base, les phrases du gold demandées et **un cas v1** de
rétro-compatibilité. Un **contrôle négatif** soumet ce cas v1 au schéma v2, qui doit le refuser.

```bash
python3 tools/verifier_schema_produit.py --json          # 5 cas v2 + 1 cas v1, versions_lues [1, 2]
python3 tools/verifier_schema_produit.py --gold 20       # + 20 phrases du gold (26 cas)
```

Au 14/11 : **6 cas, 0 échec**, `versions_lues: [1, 2]`, `v1_lue: true`, `v2_refuse_v1: true`,
validateur `fastjsonschema` ; avec `--gold 20`, **26 cas, 0 échec**. Le cas v1 est l'annotation
française ramenée à `version: 1` et privée de `meta.partition`/`meta.alternative`. Le détail de la
mesure est dans [`reports/rapport-schema-v2-doc.md`](../../reports/rapport-schema-v2-doc.md).

### 3.3 ter Le contexte (mémoire de discours)

```bash
python3 tools/drave.py analyser "Il dort." --contexte "Le chat est sur le toit."
```

Le champ `contexte` est porté dans le JSON ; il alimente la mémoire de discours (coréférence,
connecteurs) sans changer le texte analysé.

### 3.4 Rejouer et vérifier le déterminisme

```bash
python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
```
```
rejeu identique : oui
  texte      : 'Le chat de la voisine qui dort sur le toit se réveille.'
  langue     : fr
  étiquettes : 60
  JSON       : 13284 octets · sha256 31f3798beebe22f7…
```

**Lecture.** La commande analyse **deux fois**, compare le JSON **canonique** (clés triées,
durée exclue) et rend une empreinte sha256. Deux exécutions indépendantes rendent le même octet :
l'analyse est déterministe. C'est la garantie de base du rejeu.

### 3.5 Le refus, et la langue inconnue

```bash
python3 tools/drave.py analyser ""; echo "exit=$?"
```
```
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
exit=3
```

**Lecture.** Le refus est une **réponse** : le CLI écrit un **JSON d'annotation** sur `stdout`
(`refus: "vide"`, `schema: "drave.annotation"`, `version: 2`, `etiquettes: []`) et sort avec le
code **3**, distinct des autres erreurs (1) et de l'usage (5). Le message reste sur `stderr`. Un texte
vide n'est jamais une annotation « comme les autres ». Pour la langue, `und` est une réponse
honnête : « Élodie sourit. » rend `langue=und` (confiance 0,04 < seuil 0,12), même avec
`--langue fr` — l'indice n'est pas une contrainte. Et `--langue de` sort **5** : le CLI n'accepte
que `fr` et `en`.

### 3.6 Restituer la surface (v0)

```bash
python3 tools/drave.py restituer "Le chat dort."
```
```
restitution (annotation → surface)
source      : 'Le chat dort.'
surface     : 'Le chat dort.'
fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%
mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%
pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%
miroir      : 0.0000 (non exact) — minimum des fidélités binaires de la surface (graphème),
              des mots et des POS ; une sortie n'est fidèle que si elle reproduit exactement
              la source
contrôle négatif : mélange exacte 0.0000 (caractères 0.3077) · troncature exacte 0.0000
                   (caractères 0.9231)
```

**Lecture.** La commande **analyse** le texte, puis **reconstruit** la surface depuis le niveau
`graphème` de l'annotation — sans lire `Annotation.texte` — et la compare à la source. La
**surface est exacte** ; le **miroir strict** est le minimum des fidélités surface/mots/POS, et
il tombe ici parce que mots et POS séparent le point (`dort .`). `--json` publie le détail,
`--banc reports/pensee-fiabilite-produit.json` rejoue les **50 textes libres** : **46/46
surfaces exactes**, miroir strict **0,1087**, contrôle négatif **46/46**. C'est un **codec de
surface**, pas un décodeur neuronal : il ne prouve pas la fidélité sémantique. La fiche est
[`rapport-restitution-v0.md`](../../reports/rapport-restitution-v0.md).

`--canonique` ajoute la **forme canonique v1** (segments + rôles + cibles) : **46/46** contre
la source **canonisée**, mais le **miroir strict reste 0,1087** — la forme n'est pas la
surface, et elle tombe à **1/46** si on la compare à la source brute. Les **395 segments**
portent **395 rôles** et **315 cibles** (315 résolues, 313 dans un autre segment) ; la
stabilité structurelle est **18/46**. Fiche
[`rapport-restitution-v1.md`](../../reports/rapport-restitution-v1.md).

### 3.6 bis La base honnête — `--reel`

```bash
python3 tools/drave.py evaluer --reel
```

`--reel` mesure les **452 phrases réelles** (main + corpus), sans les 160 synthétiques : POS
**88,91 %**, F1 **79,06 %**, attachement **99,46 %**. Sans lui, `evaluer` publie la ligne
`BASE RÉELLE` à côté du global (612 phrases) — le chiffre global seul peut tromper.

### 3.8 bis Générer avec le natif — `generer` (expérimental)

```bash
python3 tools/drave.py generer --prompt "La France est un pays" --n 64
```

Charge un modèle natif (`drave-n0`, 34 M) et génère `--n` octets. Deux **moteurs** :
`--moteur numpy` lit le **DRVM** (sans torch, **4/4** de parité avec torch, ~0,6 s/octet) ;
`--moteur torch` lit le `.pt` (~0,15 s/octet). **Expérimental** : le
modèle produit des **collages** (les mots sont là, la phrase non — voir
[`rapport-banc-generation.md`](../../reports/rapport-banc-generation.md)) ; il exige **torch** et
un checkpoint dans `work/n2ac/` (hors dépôt). Sans torch : code **4**, message clair. Le chemin
par défaut du produit reste l'analyse heuristique (0 dépendance, hors ligne).

### 3.7 Le tagger en option — `--tagger`

```bash
python3 tools/drave.py analyser "Le chat dort." --tagger
python3 tools/drave.py analyser "Le chat dort." --tagger auto
python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
python3 tools/drave.py evaluer --tagger
```
```
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=0 · cache=1 · tokens=0 · latence=0.0 s
```

Ici le cache disque avait déjà la réponse ; un **premier** appel affiche `réseau=1`, 130 tokens
et 1,1 s (voir le coût ci-dessous, et les trois exemples réels de
[`exemples.md`](exemples.md) § 6).

**La clé.** Lue dans `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`, puis
`DEEPSEEK_API_KEY` (`DSH_KEY_FILE` / `DSH_API_KEY` en repli). Elle n'est **jamais** affichée :
ni dans le message, ni dans le JSON, ni dans le cache. **Sans clé**, la commande écrit un
message clair sur `stderr` et sort avec le code **4** ; rien n'est rendu sur `stdout`.

**Les cas d'erreur.** Mesurés par [`test_tagger_api.py`](../../tools/tests/test_tagger_api.py)
(transport factice, aucun socket) ; le tableau dit le comportement **du code courant**.

| cas | ce que fait le CLI | code | `stdout` | `stderr` / JSON |
|---|---|---:|---|---|
| **clé absente** | refuse de démarrer | **4** | vide | `drave: dépendance absente : clé DeepSeek absente …` |
| **clé invalide** (HTTP 401/403) | refuse de démarrer, **sans repli** | **4** | vide | `drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.` |
| **réseau coupé** (après 3 essais) | **replie** sur l'heuristique | **0** | annotation heuristique | `drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau : …` ; JSON `refus` non vide, POS `source=heuristique` |
| **refus du modèle** (non JSON, JSON incomplet) | **replie** sur l'heuristique | **0** | annotation heuristique | `drave: tagger : refus partiel : neuronal-pos: ValueError: …` ; JSON `refus` non vide, POS `source=heuristique` |

**Deux familles.** Une **clé absente** ou **refusée** est une dépendance manquante : le run ne
peut pas commencer, il sort **4**, rien sur `stdout`, et il ne publie pas un repli déguisé en
cascade. Un **réseau coupé** ou un **refus du modèle** est un refus **par phrase** : la cascade
garde le POS de l'heuristique, porte la cause dans `refus`, et le JSON reste valide ; le code
reste **0** parce que l'analyse, elle, est rendue. Sur `--jsonl`, le coût et
`N/M phrase(s) refusée(s)` vont sur `stderr` ; le JSONL partiel est publié. `evaluer --tagger`
suit la même règle : clé refusée → **4**, sans sortie ; refus par phrase → `refus: N`,
métriques égales à l'heuristique et `delta_pos: 0`, avec la ligne `REFUS` dans la sortie
lisible.

**Le mode `auto` — prototype.** `--tagger auto` choisit la voie au lieu de l'imposer : si
`_cle_tagger()` trouve une clé (fichier ou environnement), il construit la cascade API ; sinon
il ne construit même pas le client réseau et rend l'heuristique. Le **code de sortie ne change
pas** : **0** dans les deux cas, **3** pour un refus de texte, **jamais 4** — le 4 reste réservé
à `--tagger` **explicite**. `stderr` dit toujours **laquelle a servi**, sans nommer la clé :
`tagger auto · API (clé présente)`, `tagger auto · heuristique (clé absente)`, ou
`tagger auto · heuristique (repli : …)`. La ligne `TAGGER API` porte le coût quand l'API a été
tentée ; sans clé, il n'y a **aucun appel**, donc **aucune ligne de coût**.

| cas `--tagger auto` | ce que fait le CLI | code | `stdout` | `stderr` / JSON |
|---|---|---:|---|---|
| **clé présente** | cascade API (si le seuil 0,60 l'appelle) | **0** | `source=cascade`, POS `neuronal` | `TAGGER API · appels=1 · réseau=1 · tokens=130 …` puis `tagger auto · API (clé présente)` |
| **clé invalide** (401/403) | **replie**, ne sort pas 4 | **0** | `source=heuristique`, `refus` non vide | `tagger auto · heuristique (repli : clé refusée (HTTP 401))` ; `TAGGER API · appels=1 · réseau=0 · tokens=0` |
| **clé absente** | heuristique, **comme le défaut** | **0** | **identique au défaut octet pour octet** | `tagger auto · heuristique (clé absente)` ; aucun import réseau |
| **clé + réseau coupé** | 3 essais, puis **replie** | **0** | `source=heuristique`, `refus` non vide | `tagger auto · heuristique (repli : … réseau …)` ; `TAGGER API · appels=1 · réseau=0 · tokens=0` |
| **refus de texte** | aucun appel API | **3** | annotation de refus (`refus="vide"`) | `tagger auto · heuristique (clé présente ; refus du texte, aucun appel)` |

Le repli `auto` est **lisible dans le JSON** : `source=heuristique` et
`refus="tagger auto : … ; heuristique"`, alors que `--tagger` explicite garde
`source=cascade` et `refus="neuronal-pos: …"`. Le mode est **analyser** seulement dans ce
prototype ; `evaluer --tagger auto` rend un code **5** d'usage. Mesures réelles, cache neuf par
cas et contrôle négatif auto / explicite : [`rapport-tagger-auto.md`](../../reports/rapport-tagger-auto.md)
(30/30 tests). **La décision reste à l'humain** : le défaut ne bouge pas.

**En `--jsonl`**, une clé refusée peut laisser sur `stdout` les lignes déjà écrites avant le
code **4** (le premier texte sans appel neuronal ne déclenche pas le 401) ; le message et le
code restent les mêmes. Le tableau ci-dessus décrit `analyser` sur **un** texte.

**Ce que l'option change — et ce qu'elle ne change pas.** Le **POS** vient du tagger
(`source=cascade`, confiance déclarée **0,60**) ; les **syntagmes**, leurs **rôles**, leurs
**cibles d'attachement** et la **pragmatique** restent à l'heuristique. Le tagger ne reçoit que
les mots et les nombres : la **ponctuation** est **restituée depuis l'heuristique** (`PONCT`
reste dans la ligne `POS`, avec `0,95` ; le gold ne la compte pas). La cascade appelle le
neuronal quand un niveau passe sous **0,60** ; la fusion choisit la source **par niveau**, pas par
confiance.

**La mesure.** Sur les **20 phrases `hand`** du gold (105 tokens) : POS **88,57 % → 97,14 %**
(**+8,57 pts**), syntagmes et attachement **inchangés**. Sur le **gold 612** : **86,25 % →
95,75 %** (**+9,5 pts**) ; sur le **réel 452**, **88,91 % → 95,00 %** (**+6,1 pts**) — le
synthétique porte le reste du gain. Dispositif, coût et contrôle négatif :
[`rapport-tagger-option.md`](../../reports/rapport-tagger-option.md).

**Le coût.** **Un appel par phrase** (le tagger de syntagmes, qui était appelé sans contribuer,
a été retiré). La référence mesurée est la passe API de W2 sur **452 phrases** : **65 029
tokens** (55 572 d'entrée + 9 457 de sortie), **447 requêtes** et **443,8 s**. Le **cache**
(mémoire par texte + disque du client) rend la seconde analyse gratuite : `appels=20 ·
réseau=0 · cache=20 · tokens=0` sur les 20 phrases rejouées. Les **trois exemples** de
[`exemples.md`](exemples.md) § 6 totalisent **3 appels**, **441 tokens** et **3,7 s**.

**Le coût pour 1 000 phrases.** La passe API de W2 (452 phrases) donne **143 870 tokens**
(122 947 d'entrée + 20 923 de sortie), **989 requêtes** et **981,9 s** de réseau pour **1 000
phrases** de même longueur, soit **~0,031 $ hors pointe / ~0,062 $ en pointe** au tarif
`deepseek-flash` du 2026-11-13 ; le cache chaud rejoue à **0 réseau, 0 token** (~0,14 s). Le
chiffre est une **extrapolation** de W2, pas un run de 1 000 phrases ; `evaluer --tagger --json`
publie `tagger.cout_pour_1000_phrases`. Dispositif et limites :
[`rapport-tagger-defaut.md`](../../reports/rapport-tagger-defaut.md) § 3.6.

**`evaluer --tagger`.** La commande mesure **les deux** lectures et publie l'écart et le coût
(la ligne `TAGGER API DEEPSEEK` sur 20 phrases, exemple réel) :

```
TAGGER API DEEPSEEK (option --tagger)
  POS         exactitude 97.14 % (fermé 94.74 %, ouvert 100.00 %) · Δ +8.57 pts vs heuristique
  SYNTAGMES   F1 90.16 % (tête 97.39 %) — conservés à l'heuristique
  COÛT        appels 20 · réseau 0 · cache 20 · tokens 0 · modèle deepseek-chat
  modèle renvoyé : deepseek-flash
```

**Le défaut ne bouge pas.** Sans `--tagger`, la commande ne lit aucune clé, n'importe pas le
module réseau, n'ouvre aucune socket, sort **code 0** et rend exactement l'heuristique d'avant
(le test [`test_tagger_api.py`](../../tools/tests/test_tagger_api.py) le compare octet pour
octet ; le test W3 piège `socket.socket` et vérifie que `tools.llm.deepseek` n'est pas importé).
Le `--tagger` **explicite** est une **option**, pas un changement de produit : c'est la seule
porte qui peut sortir **4** (clé absente ou refusée). `--tagger auto` ne peut pas sortir 4 : il
replie sur l'heuristique, code **0**, et le dit. Dans les deux cas, le **défaut** sans option
reste l'heuristique hors ligne.

### 3.8 Les profils de langue — `drave profils`

```bash
python3 tools/drave.py profils --texte "Le chat dort."
python3 tools/drave.py profils --texte "Привет мир" --json
python3 tools/drave.py profils --fichier article.txt --json
python3 tools/drave.py analyser "Le chat dort." --profils
```
```
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue=fra script=Latn confiance=0.3333 source=lexique
langue      : fra (French)
script      : Latn
confiance   : 0.3333 (marge 0.0000, seuil 0.12)
source      : lexique
prior       : fra (mots-outils 0.3333)
candidats   : hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
```

**Lecture.** La commande charge l'artefact de **398 profils de trigrammes UDHR** (articles
0–14 ; article 15 tenu à l'écart) et rend la **langue probable**, le **script** et la
**confiance**. Le JSON (`--json`) porte `schema: "drave.profils"`, `langue` (la **décision**),
`langue_probable` (le premier profil), `nom`, `script`, `confiance`, `marge`, `source`,
`seuil`, `sous_seuil`, `refus`, `prior`, `candidats` et les métadonnées des profils. Sous le
seuil **0,12**, `langue` est **`und`** ; `langue_probable` et la confiance restent publiées.

**Deux chemins.** Sur un texte **long** (> 80 caractères), les 398 profils (`source: profils`).
Sur un texte **court**, les trigrammes se recouvrent : le **prior des mots-outils** des sept
langues du bloc peut trancher (`source: lexique`, `prior: {langue, score}`), et les
`candidats` restent les profils — le désaccord est visible. Un texte de moins de cinq mots qui passe par les profils est
pénalisé : un mot isolé rend `und`. `analyser --profils` emploie le même détecteur pour la
langue de l'annotation.

**Les codes.** `0` succès · `3` refus (vide ou sans lettre/chiffre) · `4` artefact de profils
absent · `5` usage (`TEXTE` et `--texte` ensemble, seuil hors `[0,1]`). Sans l'artefact,
`stdout` reste vide et le message nomme le fichier et les deux issues (roue complète, ou
constructeur).

**La mesure.** Sur les **20 langues stratifiées** de l'échantillon UDHR (5 familles × 4,
10 écritures), article 15 tenu à l'écart : **20/20** langues et **20/20** scripts ; sur les
articles 15–30 : **313/320 = 0,9781** (script **320/320**). L'autotest complet 398 langues
donne **433/447 = 0,9687** avec les profils bruts et **431/447 = 0,9642** par le chemin CLI.
Le texte ambigu bilingue rend **`und`** (0,0836 < 0,12) ; les profils permutés tombent à
**0/20** (0,0022 sur 447). Dispositif, JSON et limites :
[`rapport-profils.md`](../../reports/rapport-profils.md) et
[`profils.json`](../../reports/profils.json).

**Ce que ce n'est pas.** Une précision de déploiement : l'échantillon est **stratifié**, pas
aléatoire, l'UDHR est propre et parallèle, et la confiance n'est **pas calibrée**. Les langues
proches (mandarin/jinyu, anglais/scots) et le texte court hors des sept langues à mots-outils
restent les points faibles.

## 4. Ce que le produit ne fait pas encore

**1. Il ne génère pas de texte.** `restituer` reconstruit la **surface** depuis l'annotation
(codec), mais il n'y a **pas de génération** : pas de traduction, pas de réponse libre, pas de
paraphrase. Le produit rend des **étiquettes** et, avec `restituer`, la surface qu'elles
portent. Les résultats de traduction de la vitrine ([`README.md`](../../README.md)) sont une
recherche sur un modèle externe ; ils ne sont pas dans ce produit.

**1 bis. La restitution v2 lit les rôles, pas leur justesse.** `restituer --roles` rend un
cadre `agent / prédicat / lieu` lisible, mais la fidélité mesurée sur les 46 textes de la v0
est **19/46** cadres exacts (**16/46** non vides), **F1 0,5270** : la commande expose les
rôles de l'annotation, elle ne les corrige pas. La fiche
[`rapport-restitution-v2.md`](../../reports/rapport-restitution-v2.md) nomme le négatif.

**1 ter. Les rôles sont normalisés, pas raffinés.** Les valeurs publiées sont un
**vocabulaire fermé** — `predicat`, `agent`, `objet`, `lieu`, `temps`, `qualite`,
`possesseur`, `destinataire` — et non plus `prédicat`/`predicat` ou `qualité`/`qualite`.
La table des correspondances est dans
[`roles_vocabulaire.py`](../../tools/roles_vocabulaire.py) : `patient`, `complément`,
`contenu`, `theme` et `groupe nominal` tombent sur `objet` ; `attribut`, `maniere`,
`concession`, `hypothese`, `cause` et `consequence` sur `qualite`. C'est une
**normalisation**, pas une annotation plus fine : `objet` et `qualite` sont des catégories
larges, et le rapport [`rapport-contrat-json.md`](../../reports/rapport-contrat-json.md)
nomme ce que la table ne dit pas.

**2. Un span reste inatteignable.** Sur **239 cibles**, **238** sont attachées (couverture
**0,9958**) ; **1** ne l'est pas : `g017` (une convention du gold, déclarée inatteignable le
14/11 — la règle coûtait deux autres spans). Elles sont
**inatteignables sans corriger le gold ou le lexique** — quatre sont des cas réels nommés dans
l'audit v10 (`r035`, `r255`, `r264`, `g017`), les autres viennent du gold synthétique, dont le
lexique est disjoint. Conséquence : **238/239 (0,9958)** est l'exactitude **conditionnelle aux
spans prédits**, pas la couverture du langage. Lire les deux ensemble.

**Le doublon REL de l'union.** Deux REL peuvent se chevaucher : la plus longue porte
`meta.union: true`. C'est une **lecture concurrente** publiée par l'union, pas un second
attachement ; la sortie lisible la montre comme un **doublon REL**, et il faut la filtrer pour
une lecture unique (garder `union: null`, ou le segment qui en contient un autre).

**3. `cascade_pos` : le plancher, désormais mesuré par le CLI.** `evaluer --strict` applique le
**plancher 0,70** à la cascade locale (`MockNeuronal`) et sort en **1** sous le seuil. Sur le
gold vivant 612, la cascade rend **0,8625** ; sur le réel 452, **0,8891** — soit exactement
l'heuristique : la fusion par défaut garde ses labels, et le `MockNeuronal` est appelé sans
gagner. Ce n'est donc **pas un gain de POS** ; le produit par défaut reste l'heuristique.
`evaluer --tagger` mesure en plus la cascade **API** (**0,9575** sur 612, § 3.7), sans changer le
défaut. La cascade avec le vrai tagger 7B local a été mesurée à **0,9415** en POS sur 180
phrases, mais elle exige un serveur local 7B, que la règle 11 interdit aujourd'hui : ce n'est
pas un chemin livré. La fiche du mode strict est
[`rapport-evaluer-strict.md`](../../reports/rapport-evaluer-strict.md).

**4. Pas de neuronal local.** `MockNeuronal` est un **contrat** déterministe, pas un tagger de
qualité. Le vrai adaptateur local (`NeuronalLLM`, `NeuronalLLMPOS`) parle à un serveur local ; il
n'est ni requis ni utilisé par défaut. Le CLI expose en **option** le tagger de l'**API**
DeepSeek (§ 3.7), pas le 7B local.

**5. Les classes ouvertes sont fragiles.** POS fermé **0,9004**, ouvert **0,6234** : les mots
inconnus tombent souvent en NOUN. Exemple réel : dans « Le livre que j'ai lu… », `lu` est tagué
NOUN ; dans « The day when we left… », `left` est NOUN. Un lexique plus large améliorerait ces
cas, pas une règle.

**6. La langue n'est pas forcée.** `--langue` est un **indice**, limité à `fr` et `en` dans le
CLI ; sous le seuil de confiance, la sortie reste `und`. Il n'y a pas de `--langue-forcee`. Les
profils UDHR (398 langues, 0,9687) sont exposés par **`drave profils`** et **versionnés dans la
roue** (artefact de 802 110 octets) ; `data/` reste hors dépôt et le corpus XML source est
externe. Sans l'artefact, la commande sort en **4** et `analyser` se rabat sur les indices
internes.

**7. Pas de RSN, pas de DRVM, pas de serveur.** Le bloc a le contrat, la trace et le coût ; il
ne produit pas le corps de la RSN, n'est pas un port DRVM et n'expose pas d'API HTTP. La couche
sémantique est un **compteur d'unités**, pas une représentation.

**8. Pas de classement appris ; le gold réel 452 existe.** L'attachement est une **heuristique de
proximité** avec candidats ; il n'y a pas de modèle de classement. Le gold fait 612 phrases, dont
160 synthétiques ; les 452 phrases réelles (20 hand + 432 corpus) sont le gold de référence,
avec un split 402/H50 proposé.

**9. Pas de calibration des confiances.** `confiance` est **déclarée** (0,3 pour un NOUN ouvert,
0,92 pour un DET), pas mesurée comme une probabilité. Elle sert à trier, pas à seuiller une
décision automatique sans contrôle.

**10. Pas de texte arbitraire garanti.** Les mesures sont sur le gold ; les règles y ont été
dessinées. Sur un texte hors domaine, la couverture et la précision peuvent baisser sans que le
JSON change de forme — d'où le rejeu et le contrôle par un gold à soi. Le **format** est versionné
(v2 ; v1 reste lue), la **qualité linguistique** ne l'est pas.

## 5. Performance

| ce qui est mesuré | valeur | conditions |
|---|---|---|
| **612 phrases du gold** | **0,36 s** (mesure du 06/11) ; **0,45–0,55 s** (audit) ; **~0,6 s** (chiffre rond publié) | heuristique, un cœur, 3 179 tokens |
| **`drave evaluer`** | **0,55 s** au total | une lecture (heuristique), démarrage Python compris |
| **`drave analyser`** | **0,15 s** au total | une phrase, démarrage compris |
| **cache du chunker** | **×138,7** à 160 répétitions (9 817,7 → 70,8 ms) | banc de texte **répété**, chemin chunker |
| **cache, chemin par défaut** | ×5,8 à 20 répétitions, puis **×1,0** à 80 et 160 | S domine le coût |
| **cache, corpus réel** | **×1,2** | phrases réelles, 6,1 tokens/phrase |
| **sortie** | **identique** : 0 différence sur 612 phrases, tous champs | le cache ne change pas une mesure |

**Ce que le ×139 veut dire — et ne veut pas dire.** C'est la suppression du **O(n²)** du chunker
sur un texte **répété** : 1 + 2S appels ramenés à 1, verbes de GV mémoïsés par span. Sur du texte
réel, le gain est **×1,2** ; sur le chemin par défaut, **×1,0** à 80 et 160 répétitions. Annoncer
« ×139 plus rapide » sans la condition serait faux. Ce que le cache garantit, c'est que les
textes longs et répétés ne s'effondrent plus.

**Ce que le produit ne consomme pas** : pas de GPU, pas de modèle, pas de réseau, pas d'écriture
disque (hors le fichier de sortie). Le cache est **local à une analyse** et libéré à chaque
phrase. Les temps sont CPU, sur machine partagée ; ils varient avec la charge.

## 6. Garanties

| garantie | ce que ça veut dire | contrôle |
|---|---|---|
| **déterminisme** | même entrée → même JSON, octet pour octet | `drave rejouer` (§ 3.4) ; `tools/tests/test_produit.py` compare deux sorties |
| **hors réseau** | le chemin par défaut n'ouvre aucune socket | analyse `heuristique` seulement ; le tagger API exige `--tagger` et une clé |
| **refus explicite** | texte vide ou sans lettre/chiffre → `refus: "vide"`, 0 étiquette | bloc : JSON ; CLI : JSON sur `stdout` + code 3 |
| **pas d'invention** | chaque étiquette porte `source`, `confiance`, `candidats` ; `und` plutôt qu'une langue forcée | JSON ; `--langue` est un indice |
| **spans lisibles** | indices en **points de code Unicode**, 0-based, `[debut:fin)` | « Élodie » → `[0:6]` ; emoji = 1 point |
| **UTF-8** | le JSON est en UTF-8, non échappé ; la durée est **absente par défaut** et `--duree` l'ajoute | `--json` ; `test_produit.py` vérifie l'absence de `duree_s` sans le drapeau |
| **gold versionné** | les 4 gold sont dans le dépôt ; `evaluer` rejoue hors ligne | `tools/tests/linguistique/gold*.json` |
| **format versionné** | `schema: "drave.annotation"`, `version: 2` ; v1 reste lue | `tools/schemas/` ; `python3 tools/verifier_schema_produit.py --gold 20` |
| **porte produit** | version, JSON fr/en, rejeu, smoke test, autotest | `bash tools/porte-produit.sh` → ✅ |
| **intégration continue** | la porte et les tests du contrat rejoués sur **Python 3.10 et 3.13** à chaque `push` | [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) ; [ci.md](ci.md) |

**La porte produit, mesurée le 07/11** : `✅ porte produit verte` — `drave 0.1.0`, JSON valide et
étiqueté en `fr` et `en`, `sha256 f4b7822076a4203d` deux fois, **18 tests** de fumée, **8 tests**
de schéma (v2 + rétro-compatibilité v1), **4 tests** sur 50 textes libres, **11 tests** de
restitution, **183/183** portes d'autotest ; **12 contrôles**. Le smoke test est
`tools/tests/test_produit.py`.

**L'intégration continue** rejoue cette porte à chaque `push` : `.github/workflows/ci.yml` teste
`pip install -e .`, les trois tests du contrat et `porte-produit.sh` sur **Python 3.10 et 3.13**
(matrice, `fail-fast: false`). Le sous-module `tools/structures` ayant une URL locale, le
workflow restaure une **copie de secours** de `generateur.py` et du gold de l'analyseur depuis
[`.github/ci/structures/`](../../.github/ci/structures/) avant l'installation. La preuve locale,
faite sans `act`, est [`tools/verifier_ci.py`](../../tools/verifier_ci.py) : YAML chargé par
PyYAML, cinq étapes par version, et un test volontairement cassé qui sort en **1** et arrête la
séquence. Le mode d'emploi et les limites sont dans [`ci.md`](ci.md) ; les chiffres dans
[`reports/rapport-ci.md`](../../reports/rapport-ci.md).

**Codes de sortie.** Le CLI implémente **0 / 1 / 3 / 4 / 5** ; le contrat est écrit dans
`--aide` et vérifié par `tools/tests/test_produit.py` :

| code | sens | aujourd'hui |
|---:|---|---|
| **0** | succès : annotation rendue, évaluation rendue, rejeu identique, restitution rendue | `analyser`, `evaluer`, `rejouer`, `restituer` |
| **3** | refus d'analyse : une **réponse**, pas une erreur | `analyser ""` (JSON de refus sur `stdout`), `restituer ""`, `rejouer ""` |
| **4** | clé/dépendance absente : clé du tagger (absente **ou refusée**) en `--tagger` explicite, ou **fichier introuvable** | `--tagger` sans clé, clé refusée HTTP 401/403, `--fichier absent.txt` : message clair, rien sur `stdout`, pas de trace |
| **5** | usage invalide : argument, sous-commande, langue hors `fr`/`en`, `--fichier` sur un **répertoire** | `argparse` et les contrôles de cohérence du CLI |
| **1** | autre erreur : divergence de rejeu, tagger qui refuse une phrase sans POS, exception inattendue | cas résiduels, jamais un refus ni un usage |

**Les deux erreurs de `--fichier`.** Un chemin **inexistant** est une **dépendance absente**
(code **4**) : `drave: dépendance absente : fichier introuvable : 'absent.txt'`. Un
**répertoire** est un **usage invalide** (code **5**) : `drave: erreur d'usage : un répertoire
n'est pas un fichier : 'corpus/' (--fichier attend un fichier UTF-8)`. Dans les deux cas, rien
sur `stdout` et aucune trace Python. Un fichier présent mais illisible (permission) est aussi
une dépendance (4).

**Ce qui n'est pas garanti** : le chemin neuronal **local**, un texte hors domaine, la calibration
des confiances, la **compatibilité octet pour octet** entre versions (le bump v1 → v2 change le
JSON), et la qualité sur un lot de textes hétérogènes (une invocation = un texte). Le tagger API
est une option **best-effort** : sa justesse dépend du modèle du jour, et son cache peut rejouer
une ancienne réponse.

## 7. Le CLI livré — contrat et manques

Le point d'entrée existe : `tools/drave.py`, version **0.1.0**, sans dépendance externe.

```bash
python3 tools/drave.py --version
python3 tools/drave.py --aide
python3 tools/drave.py analyser "Le chat dort." [--langue fr|en] [--json] [--duree] [--tagger] \
    [--partition brut|alternative|filtrer_union|filtrer] [--contexte TEXTE] [--profils]
python3 tools/drave.py analyser --fichier corpus.txt [--jsonl|--json] [--duree] [--tagger]
python3 tools/drave.py profils --texte "Le chat dort." [--json] [--seuil 0.12]
python3 tools/drave.py profils --fichier page.txt [--json]
python3 tools/drave.py evaluer [--gold] [--json] [--par-langue] [--tagger]
python3 tools/drave.py rejouer "TEXTE" [--langue fr|en]
python3 tools/drave.py restituer "TEXTE" [--langue fr|en] [--json] [--fichier CHEMIN]
python3 tools/drave.py restituer "TEXTE" --roles
python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json [--json]
python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --roles
```

`--tagger` est la **seule** option qui sort du hors ligne : elle appelle l'API DeepSeek (clé et
réseau, § 3.7). Toutes les autres lignes ci-dessus restent CPU, déterministes et sans socket.

**Sorties réelles des commandes** (07/11 pour le format ; les valeurs d'`evaluer` sont celles
mesurées le 14/11) :

```
$ python3 tools/drave.py --version
drave 0.1.0

$ python3 tools/drave.py evaluer --gold
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold gelé (référence figée) · 602 phrases · 3141 tokens · 239 cibles d'attachement
...
SYNTAGMES   F1 78.82 %  (P 78.18 % / R 79.46 %)
  tête      F1 90.25 %  (P 92.34 % / R 88.26 %)
...
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)

$ python3 tools/drave.py rejouer "Le chat dort."
rejeu identique : oui
  texte      : 'Le chat dort.'
  langue     : fr
  étiquettes : 20
  JSON       : 4227 octets · sha256 f4b7822076a4203d…
```

**Options du CLI** :

| option | commande | sens |
|---|---|---|
| `--langue fr\|en` | `analyser`, `rejouer`, `restituer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 5 |
| `--json` | `analyser`, `evaluer`, `profils`, `restituer` | sortie machine UTF-8 |
| `--duree` | `analyser` | ajoute `cout.duree_s` au JSON (ou à chaque ligne de `--jsonl`) ; absent par défaut |
| `--tagger` | `analyser`, `evaluer` | POS par l'API DeepSeek (clé et réseau ; défaut : heuristique) ; `evaluer` mesure en plus la cascade et le Δ (§ 3.7) |
| `--jsonl` | `analyser` | une ligne JSON par phrase (avec `--fichier`) |
| `--fichier CHEMIN` | `analyser`, `profils`, `restituer` | lit un texte UTF-8 au lieu de l'argument |
| `--banc CHEMIN` | `restituer` | mesure un banc JSON de textes (les 50 textes libres) |
| `--canonique` | `restituer` | ajoute la forme canonique v1 (segments + rôles + cibles) et son miroir |
| `--roles` | `restituer` | ajoute la forme lisible des rôles (agent, prédicat, lieu) ; avec `--banc`, mesure leur fidélité à l'or |
| `--partition MODE` | `analyser`, `rejouer` | `alternative` (défaut), `filtrer_union`, `filtrer`, `brut` |
| `--contexte TEXTE` | `analyser`, `restituer` | mémoire de discours portée dans le JSON |
| `--profils` | `analyser` | détecte la langue par les 398 profils UDHR (texte long) et le prior court ; sans lui, le repli à sept langues |
| `--texte TEXTE` | `profils` | le texte à profiler (équivalent du TEXTE positionnel) ; avec `--seuil`, règle la décision `und` |
| `--gold` | `evaluer` | gold gelé 602 au lieu du vivant 612 |
| `--strict` | `evaluer` | quatre modes locaux sur 612 et 452, plancher 0,70 sur la cascade POS (échec = code 1) ; exclusif avec `--gold`, `--tagger`, `--par-langue` (§ 3.3) |
| `--par-langue` | `evaluer` | détail **fr/en** : POS, syntagmes, attachement et contrôle négatif par langue |
| `-V`, `--version` | global | `drave 0.1.0` |
| `-h`, `--aide` | global | l'aide, largeur fixe |

**Ce qui manque encore** (le contrat cible, non livré) :

| manque | conséquence |
|---|---|
| **l'entrée standard** | `--fichier` lit un fichier, mais pas de pipe (`cat corpus.txt \| drave analyser`) |
| **`--sortie`** | pas d'écriture directe d'un JSON ; il faut rediriger le shell |
| **`rejouer` sur un JSON sauvegardé** | `rejouer` prend un **texte**, pas une annotation ; on ne peut pas rejouer un fichier produit hier |
| **`--mode` / la cascade locale en analyse** | `evaluer --strict` **mesure** les quatre modes locaux ; `analyser` n'expose pas `--mode` : la cascade locale en production demande encore le code Python |
| **un répertoire** | `--fichier` lit un fichier ; pas de parcours de répertoire |
| **la publication** | `pip install -e .` et la commande `drave` existent ; **pas de wheel publiée** ni de paquet sur PyPI — l'installation pointe vers le dépôt |
| **le neuronal local** | la cascade 7B (0,9415) exige un serveur local interdit par la règle 11 ; le tagger **API** est en option, le 7B local n'est pas livré |
| **la restitution sémantique** | `restituer` est un **codec de surface** (graphème) ; il ne restitue pas le sens, ne traduit pas, ne génère pas |

**Ce qui est déjà tenu** : `--version`, `--aide`, les **cinq** sous-commandes, les **398
profils de langue** (`drave profils`, `analyser --profils`), le JSON
déterministe, le rejeu par empreinte, le **format versionné** (schéma v2, v1 lue),
`--fichier`/`--jsonl`, `--duree`, `--banc`, `--partition`, le **tagger API en option** (`--tagger`, code 4,
cache), le **mode strict** (`--strict`, quatre modes, plancher 0,70, code 1), la **restitution v0** (46/46 surfaces exactes,
miroir strict 0,1087), la **forme canonique v1** (`--canonique`, 46/46 canonique, strict
inchangé), les **candidats d'attachement en objets** `{span, cible, source}` et le
**vocabulaire fermé des rôles** (`predicat` sans accent ; 21 rôles bruts → 8, 0 hors
table sur le gold 612), la porte produit et le smoke test. Le reste est nommé ci-dessus,
sans être présenté comme acquis.

## 8. FAQ — dix questions

> **Vérifié le 2026-11-15** contre le code courant (`drave 0.1.0`) par
> [`tools/verifier_faq.py`](../../tools/verifier_faq.py) : **10/10** réponses passent et le
> **contrôle négatif** est détecté. Le détail des commandes, les sorties observées et ce qui
> pourrait rendre chaque réponse fausse sont dans
> [`reports/rapport-faq.md`](../../reports/rapport-faq.md) et
> [`reports/faq.json`](../../reports/faq.json). Si le code bouge, relancer
> `python3 tools/verifier_faq.py`.

### 8.1 Quelles langues le produit reconnaît-il ?

Le **bloc** détecte la langue et le script : ses profils UDHR couvrent **398 langues**
(**0,9687** sur l'autotest), et **`drave profils --texte` les expose** (langue probable,
script, confiance). `--langue` reste un **indice** limité à `fr`/`en` ; sans indice, `analyser`
rend la langue détectée — `de` pour « Der Hund schläft. », `es` pour « El perro duerme. » — ou
`und` quand la confiance passe sous le seuil (**0,12**) : « Élodie sourit. » rend `und`, **même
avec `--langue fr`**. `--langue de` sort **5** (usage invalide). L'artefact des 398 profils est
**versionné dans la roue** (802 110 octets) ; `data/` reste hors dépôt.

### 8.2 Est-ce que ça marche hors ligne ?

**Oui, par défaut.** `analyser`, `evaluer`, `profils`, `rejouer` et `restituer` tournent sur **CPU**, sans
modèle, sans GPU et **sans ouvrir de socket** ; le seul chemin réseau est l'option
`--tagger` (§ 3.7). Vérifié en interdisant `socket.socket` : l'analyse passe, et le module
`tools.llm.deepseek` n'est **même pas importé**. Sans `--tagger`, aucune clé n'est lue.

### 8.3 Combien ça coûte ?

Le défaut n'ouvre aucun appel : **0 $ d'API** (seul le CPU local est consommé). L'option
`--tagger` coûte **un appel par phrase** : **609 appels**, **22 299 tokens**, **155 s** et
**~0,02 $** pour les 612 phrases du gold ; le cache mémoire + disque rend la seconde analyse
gratuite (**0 réseau, 0 token**). Les trois exemples de [`exemples.md`](exemples.md) totalisent
**3 appels**, **441 tokens** et **3,7 s**. Le prix dépend du modèle du jour (`deepseek-chat`
demandé, `deepseek-flash` souvent renvoyé) et le cache peut rejouer une ancienne réponse.

### 8.4 Qu'est-ce que `--tagger` change ?

`--tagger` remplace le **POS** par celui de l'API DeepSeek ; les **syntagmes**, leurs
**rôles**, les **cibles d'attachement** et la **pragmatique** restent heuristiques, et la
**ponctuation** est restituée depuis l'heuristique. Sur le gold 612, le POS passe de
**86,25 % à 95,75 %** (**+9,5 pts**) ; sur le réel 452, de **88,91 % à 95,00 %** (**+6,1**).
La clé est lue dans `DEEPSEEK_KEY_FILE`, `~/.config/drave/deepseek.key`, puis
`DEEPSEEK_API_KEY` (repli `DSH_*`) ; sans clé **ou avec une clé refusée**, code **4**, rien sur
`stdout` (§ 3.7). C'est une option **best-effort** : sa justesse dépend du modèle, et le cache
peut servir une réponse ancienne.

### 8.5 Quel est le format de sortie, et est-il stable ?

Le JSON est estampillé `schema: "drave.annotation"` et `version: 2`. La v2 ajoute des champs
**optionnels** dans `meta` — `partition`, `alternative`, `attachement.candidats` — et
normalise `meta.role` en huit valeurs ; les **huit champs obligatoires** de la racine sont
ceux de la v1, et un client v1 qui ignore `meta` continue de lire. Le champ historique
`candidats` de l'étiquette reste une liste de chaînes. `tools/verifier_schema_produit.py`
lit les versions **1 et 2**, valide **6 cas** (dont un cas v1) et, avec `--gold 20`, **26
cas, 0 échec** ; il refuse en plus un rôle hors vocabulaire et un candidat qui redevient une
chaîne. La compatibilité **octet pour octet** entre versions n'est pas garantie : le bump
change le JSON et son `sha256`.

### 8.6 Que veut dire « attachement », et à quel point est-il fiable ?

Pour chaque syntagme, le produit publie un **rôle**, une **cible** d'attachement et des
**candidats** : « Le chat » → `dort`, la REL « que j'ai lu » → `livre`. Le JSON v2 donne les
candidats en **objets** `{span, cible, source}` (`meta.attachement.candidats`), et la sortie
lisible garde les chaînes d'affichage. Ce n'est **pas un
arbre syntaxique complet**. Sur le gold vivant 612, **238/239 cibles** sont attachées
(**0,9958**) ; sur les 238 segments dont le span est prédit, l'exactitude est **1,0000** ; le
top-k vaut **0,9874**. Le contrôle négatif du CLI — une cible exacte tirée au hasard — vaut
**1,67 %** ; l'audit v10 ajoute un **candidat aléatoire** dans les listes (**42,14 %** de top-1)
et une **permutation des cibles** (**0,908 %**). La mesure est **in-sample** : les règles ont
été dessinées sur ce gold, avec un split dev/test.

### 8.7 Pourquoi reste-t-il un span inatteignable ?

Oui, **un** : `g017` (« She said that she would come yesterday. »). Le gold attend la SUB
**[9:28]** « that she would come » ; le bloc prédit **[9:38]**, adverbe inclus. La **cible** est
déjà juste (`said`) — c'est le **span** qui manque, donc le seul label absent des 239. La règle
qui retire l'adverbe final corrige `g017` mais **casse `r264` et `r288`** : F1 **0,7902 →
0,7901** et couverture **0,9958 → 0,9916** ; elle a été **rejetée**. Lire **238/239** comme une
exactitude **conditionnelle aux spans prédits**, pas comme la couverture du langage ; sur la
base réelle 452, **183/184 (99,46 %)**. Détail : [`rapport-g017.md`](../../reports/rapport-g017.md).

### 8.8 Que peut-on restituer : la surface, la forme, les rôles ?

Trois vues, de la surface vers les rôles. `restituer` (défaut, **v0**) reconstruit la
**surface** depuis le niveau `graphème` : **46/46** surfaces exactes, mais le **miroir strict**
vaut **0,1087** (mots et POS séparent le point). `--canonique` (**v1**) ajoute la **forme
canonique** (segments + rôles + cibles) : **46/46** contre la source canonisée, strict inchangé.
`--roles` (**v2**) rend un cadre lisible **agent / prédicat / lieu** : **19/46** cadres exacts
(**16/46** non vides), **F1 0,5270**, **198/198** spans dans la source et **46/46** rendus
relus. La v2 **expose** les rôles de l'annotation ; elle ne les corrige pas. Aucune des trois
ne traduit ni ne génère.

### 8.9 Quelles limites faut-il connaître avant de s'en servir ?

**Pas de génération** (texte, traduction, correction, paraphrase), **pas de serveur HTTP**,
**pas de RSN/DRVM**, **pas de neuronal local** (le 7B exige un serveur interdit par la règle 11 ;
seul le tagger **API** est en option). **Pas de classement appris** de l'attachement, **pas de
calibration** des confiances (elles sont déclarées), **pas de `--langue-forcee`** et **pas de
garantie hors domaine** : les chiffres sont sur un gold où les règles ont été dessinées. Le CLI
n'a **pas** d'entrée standard, pas de `--sortie`, pas de parcours de répertoire, pas de rejeu
d'une annotation sauvegardée. Les candidats sont des objets `{span, cible, source}` et les
rôles un vocabulaire fermé de huit valeurs ; mais la normalisation ne raffine pas le rôle
(`objet` et `qualite` sont larges) et le span d'un candidat est sa première occurrence dans
le texte. Le format est versionné ; la **qualité linguistique** ne l'est pas.

### 8.10 Comment l'installer et le lancer ?

Trois chemins, le même CLI. **Depuis le dépôt, sans rien installer** : `python3 tools/drave.py …`
depuis la racine (Python **3.10+**, mesuré ici en 3.13), **aucune dépendance externe**, aucun GPU.
**En éditable** (pour développer) : `python3 -m pip install -e .` dans un venv, depuis la racine.
**Depuis la roue** (pour installer hors du dépôt) :

```bash
python3 -m pip wheel . --no-deps --no-build-isolation -w dist
# dist/drave-0.1.0-py3-none-any.whl

python3 -m venv /tmp/venv-drave-roue
/tmp/venv-drave-roue/bin/python -m pip install --no-index --no-deps \
  dist/drave-0.1.0-py3-none-any.whl
cd /tmp
/tmp/venv-drave-roue/bin/drave --version            # drave 0.1.0
/tmp/venv-drave-roue/bin/drave analyser "Le chat dort."
/tmp/venv-drave-roue/bin/drave evaluer --json
```

La roue **embarque les données de la mesure** : `tools/tests/linguistique/gold*.json` (les cinq
gold), le générateur S (`tools/structures/generateur.py`) et le client du tagger optionnel. Elle
ne dépend donc **pas du dépôt** : `analyser` et `evaluer` rendent depuis `/tmp` les **mêmes
sorties** que le chemin historique. `drave evaluer --gold` mesure le gold **gelé**
(`gold_gele.json`), livré lui aussi. Le corpus UDHR et les poids restent hors roue (`data/`,
`models/`), comme hors dépôt.

Le **contrôle négatif** : une roue **amputée** des `gold*.json` installe et analyse encore, mais
`drave evaluer` sort en **4**, `stdout` vide, avec un message qui nomme les fichiers manquants et
dit quoi faire (réinstaller la roue complète, ou mesurer depuis le dépôt). `--gold` ne remplace
pas un gold absent : il choisit le gelé. Détail, hashes et sorties :
[`reports/rapport-roue.md`](../../reports/rapport-roue.md) ; installation éditable et premier
contrôle négatif (sans aucun `drave`) : [`reports/rapport-empaquetage.md`](../../reports/rapport-empaquetage.md).

Sans installation, `drave` n'existe pas : `command not found` (code **127**), pas une trace
Python. Le chemin historique reste garanti : `python3 tools/drave.py --version` → `drave 0.1.0`.
Construire la roue demande `setuptools` (isolé par pip, donc réseau ou cache) et le sous-module
`tools/structures` ; la roue publiée n'est pas sur PyPI, elle se construit localement.

## 9. Où aller ensuite

| si vous voulez… | allez à |
|---|---|
| **installer et lancer en 5 minutes** | [`demarrage.md`](demarrage.md) |
| **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |
| **la FAQ du produit** (dix questions vérifiées) | [§ 8](#8-faq--dix-questions) · [`reports/rapport-faq.md`](../../reports/rapport-faq.md) · [`reports/faq.json`](../../reports/faq.json) |
| **le schéma du JSON** (v2 : `meta.partition`, `meta.alternative`) | [`tools/schemas/drave-annotation-v2.json`](../../tools/schemas/drave-annotation-v2.json) · [v1](../../tools/schemas/drave-annotation-v1.json) |
| **la fiche du schéma v2** | [`reports/rapport-schema-v2.md`](../../reports/rapport-schema-v2.md) |
| **le contrat du bloc** (9 niveaux, substitution, activation) | [`docs/implantation/bloc-linguistique.md`](../implantation/bloc-linguistique.md) |
| **les chiffres de l'attachement** (v12, instantané) | [`reports/rapport-pensee-v12.md`](../../reports/rapport-pensee-v12.md) · [`reports/pensee-v12.json`](../../reports/pensee-v12.json) |
| **l'audit des mesures** (contrôles, spans, bases) | [`reports/rapport-audit-v10.md`](../../reports/rapport-audit-v10.md) |
| **la mesure par langue** (fr/en, source contrôlée) | [`reports/rapport-evaluer-langue.md`](../../reports/rapport-evaluer-langue.md) |
| **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |
| **la cascade réelle** (0,9415, 7B, non livrée) | [`reports/rapport-pensee-gold-cascade.md`](../../reports/rapport-pensee-gold-cascade.md) |
| **le tagger en option** (mesure 20/612, coût, tests) | [`reports/rapport-tagger-option.md`](../../reports/rapport-tagger-option.md) · [`reports/pensee-tagger-option.json`](../../reports/pensee-tagger-option.json) |
| **l'intégration continue** (matrice 3.10/3.13, contrôle négatif) | [`ci.md`](ci.md) · [`reports/rapport-ci.md`](../../reports/rapport-ci.md) · [`reports/rapport-ci.json`](../../reports/rapport-ci.json) |
| **le plancher `cascade_pos`** et les repères des passes | [`docs/pilotage/references-non-regression.md`](../pilotage/references-non-regression.md) |
| **l'ancien constat « pas de produit »** (27/10) | [`docs/pilotage/utilisation.md`](../pilotage/utilisation.md) |
| **la théorie de la couche heuristique** | [`docs/theorie/pre-traitement-linguistique.md`](../theorie/pre-traitement-linguistique.md) |

**Un mot sur la méthode.** Le produit ne remplace pas la fiche : les chiffres vivent dans
`reports/`, avec leur dispositif, leur contrôle négatif et ce qui pourrait les rendre faux. Cette
notice dit seulement ce qu'un utilisateur peut en faire **aujourd'hui**, et ce qu'il ne peut pas
encore faire.
