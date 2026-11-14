# Cinq exemples d'analyse, commentés

> **Ce que ce document est.** Cinq exécutions **réelles** du produit, avec leur JSON commenté. Il
> complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
> *comment lire* ce qui sort. Les sorties ont été produites le **2026-11-06** sur la branche
> `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et sans réseau ;
> elles ont été **rejouées le 2026-11-14** sur le code courant — F1 **0,7902**, attachement
> **238/238 labels** (238/239 cibles), schéma **v2**. Le format v2 ajoute `version: 2` et, sur un
> syntagme qui chevauche un autre, `meta.partition`/`meta.alternative` ; v1 reste lue
> ([schéma v2](../../tools/schemas/drave-annotation-v2.json)).
>
> **Le rejeu du 14/11.** **4 blocs sur 5** ont bougé : la ponctuation finale entre dans le POS
> (20 étiquettes et non 19), le refus sort en **3**, le POS anglais de `r241` s'améliore et
> `r035`, l'ancien échec connu, est désormais **prédit**. Seul le bloc `g011` est identique champ
> pour champ. Les écarts, le dispositif et le contrôle négatif sont dans
> [`reports/rapport-exemples-rejoues.md`](../../reports/rapport-exemples-rejoues.md).
>
> **Une commande, un JSON.** `python3 tools/drave.py analyser "…" --json` rend l'annotation
> complète (neuf niveaux). Pour la lire, ce document filtre avec `jq` ; le produit, lui, n'a pas
> besoin de `jq`.

## 0. Comment lire les JSON

- `debut` / `fin` : indices en **points de code Unicode**, 0-based, fin exclue : `[debut:fin)`.
  « Élodie » → `[0:6]` ; un emoji compte pour **un** point.
- `niveau` : `pos`, `syntagme`, `phrase` et `pragmatique` sont montrés ; `graphème`, `mot`,
  `morphème`, `discours` et `document` sont omis (ils existent dans le JSON complet).
- `confiance` : **déclarée**, pas calibrée. 0,3 pour un NOUN ouvert, 0,92 pour un DET.
- `meta.attachement` : `{segment, cible}` ; `cible` est une **chaîne**, pas un span.
- `meta.partition` : `{groupe, rang, membres, vue}` — présent sur un syntagme d'un groupe de
  chevauchement (v2) ; `rang: 1` est la vue préférée, pas une suppression.
- `meta.alternative` : la liste des autres segments du groupe (`type`, `debut`, `fin`, `source`,
  `union`, `relation`, `rang`, `role`, `attachement`, `retire` en vue filtrée) — v2.
- `candidats` : des **chaînes d'affichage** (parfois « « qui dort » → voisine »), pas des objets.
- `null` : pas d'attachement publié pour ce syntagme.
- `union: true` : seconde lecture qui chevauche un syntagme plus court. Dans la sortie lisible du
  CLI, elle apparaît comme un **doublon REL** ; pour une lecture unique, filtrer les segments qui
  en contiennent un autre (ou garder `union: null`).

Un filtre de lecture (à définir une fois dans le terminal ; les exemples ci-dessous adaptent
parfois la liste des niveaux) :

```bash
FILTRE='{langue, script, refus, fraction_semantique,
  pos: [.etiquettes[] | select(.niveau=="pos")
        | {valeur, type, debut, fin, confiance, ouvert:.meta.ouvert}],
  syntagmes: [.etiquettes[] | select(.niveau=="syntagme")
        | {valeur, type, debut, fin, confiance, role:.meta.role,
           cible:.meta.attachement.cible, union:.meta.union,
           partition:.meta.partition, alternative:.meta.alternative, candidats}],
  phrase: [.etiquettes[] | select(.niveau=="phrase") | {type, valeur}],
  pragmatique: [.etiquettes[] | select(.niveau=="pragmatique") | {type, valeur}],
  unites_semantiques}'
```

Puis : `python3 tools/drave.py analyser "…" --json | jq "$FILTRE"`.

## 1. Une déclarative simple — `g001`

**Entrée.** `Le chat dort.` (phrase `hand` du gold, `g001`).

**Commande (sortie lisible).**

```bash
python3 tools/drave.py analyser "Le chat dort."
```

**Sortie (réelle).**

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

**Commande (JSON).**

```bash
python3 tools/drave.py analyser "Le chat dort." --json \
  | jq '{langue, script, refus,
         pos: [.etiquettes[] | select(.niveau=="pos")
           | {valeur, type, debut, fin, confiance, ouvert:.meta.ouvert}],
         syntagmes: [.etiquettes[] | select(.niveau=="syntagme")
           | {valeur, type, debut, fin, confiance, role:.meta.role,
              cible:.meta.attachement.cible, union:.meta.union, candidats}],
         phrase: [.etiquettes[] | select(.niveau=="phrase") | {type, valeur}],
         pragmatique: [.etiquettes[] | select(.niveau=="pragmatique") | {type, valeur}]}'
```

**Sortie (réelle, extrait).**

```json
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "pos": [
    {
      "valeur": "Le",
      "type": "DET",
      "debut": 0,
      "fin": 2,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "chat",
      "type": "NOUN",
      "debut": 3,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "dort",
      "type": "VERB",
      "debut": 8,
      "fin": 12,
      "confiance": 0.72,
      "ouvert": true
    },
    {
      "valeur": ".",
      "type": "PONCT",
      "debut": 12,
      "fin": 13,
      "confiance": 0.95,
      "ouvert": false
    }
  ],
  "syntagmes": [
    {
      "valeur": "Le chat",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confiance": 0.55,
      "role": "agent",
      "cible": "dort",
      "union": null,
      "candidats": [
        "structure la plus proche",
        "dort"
      ]
    },
    {
      "valeur": "dort",
      "type": "GV",
      "debut": 8,
      "fin": 12,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "chat",
      "union": null,
      "candidats": [
        "structure la plus proche"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type",
      "valeur": "déclarative"
    }
  ],
  "pragmatique": [
    {
      "type": "acte",
      "valeur": "assertion"
    }
  ]
}
```

**Lecture.**

- `langue: fr`, `script: Latn`, `refus: ""` : le texte est accepté.
- Quatre POS : `Le/DET`, `chat/NOUN`, `dort/VERB` et `.`/`PONCT` (0,95). `chat` et `dort` sont
  **ouverts** (confiance 0,3 et 0,72) : le lexique ne les connaît pas comme classes fermées.
- Deux syntagmes : `GN « Le chat » [0:7] → dort` et `GV « dort » [8:12] → chat`. Le gold `g001`
  attend exactement ces deux spans et `assertion` ; c'est le cas de base réussi.
- L'extrait omet `fraction_semantique`, `unites_semantiques`, `trace` et `cout` (présents dans le
  JSON complet) ; la sortie lisible donne **2 unités**, soit **61,5 %** du texte.

**Ce qu'il faut en conclure.** Sur une phrase canonique, l'analyse est exacte, lisible et
complète. C'est le cas d'usage de base ; il ne dit rien de la couverture sur un texte difficile
(voir § 5).

## 2. Un attachement de REL — `g011`

**Entrée.** `Le livre que j'ai lu est intéressant.` (phrase `hand` du gold, `g011`).

**Commande.**

```bash
python3 tools/drave.py analyser "Le livre que j'ai lu est intéressant." --json \
  | jq '{langue, script, refus,
         syntagmes: [.etiquettes[] | select(.niveau=="syntagme")
           | {valeur, type, debut, fin, confiance, role:.meta.role,
              cible:.meta.attachement.cible, union:.meta.union, candidats}],
         phrase: [.etiquettes[] | select(.niveau=="phrase") | {type, valeur}],
         pragmatique: [.etiquettes[] | select(.niveau=="pragmatique") | {type, valeur}]}'
```

**Sortie (réelle).**

```json
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "syntagmes": [
    {
      "valeur": "Le livre",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.55,
      "role": "agent",
      "cible": "intéressant",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ]
    },
    {
      "valeur": "que j'ai lu",
      "type": "REL",
      "debut": 9,
      "fin": 20,
      "confiance": 0.55,
      "role": "qualite",
      "cible": "livre",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ]
    },
    {
      "valeur": "que j'ai lu est intéressant",
      "type": "REL",
      "debut": 9,
      "fin": 36,
      "confiance": 0.3,
      "role": "qualité",
      "cible": "livre",
      "union": true,
      "candidats": [
        "REL",
        "livre",
        "intéressant"
      ]
    },
    {
      "valeur": "est intéressant",
      "type": "GV",
      "debut": 21,
      "fin": 36,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "livre",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "livre"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type",
      "valeur": "déclarative"
    }
  ],
  "pragmatique": [
    {
      "type": "acte",
      "valeur": "assertion"
    },
    {
      "type": "double_sens",
      "valeur": "candidat"
    }
  ]
}
```

**Lecture.**

- `REL « que j'ai lu » [9:20] → livre` : c'est l'attachement attendu par le gold
  (`cible: livre`). C'est le cas `g011` réussi.
- `REL « que j'ai lu est intéressant » [9:36] → livre` avec **`union: true`** : c'est la **seconde
  lecture d'union**, un **doublon REL** qui chevauche la première. La sortie lisible du CLI ne
  montre pas `union` : elle affiche deux REL, et il faut **ignorer la plus longue** pour une
  lecture unique (ou filtrer les segments qui en contiennent un autre). Ce n'est pas une erreur
  d'attachement : c'est une hypothèse concurrente publiée telle quelle.
- En **v2**, le JSON complet porte en plus `meta.partition` sur les trois segments du groupe 0
  (`membres: 3` ; rang 1 = REL longue, rang 2 = GV, rang 3 = REL courte) et `meta.alternative`
  avec les deux autres. Le filtre ci-dessus ne les sélectionne pas ; pour les voir, ajouter
  `partition:.meta.partition, alternative:.meta.alternative` (voir le `FILTRE` du § 0).
- `GN « Le livre » → intéressant` : le GN est rattaché au GV, pas à la REL. Le gold annote ce GN
  `patient`, le bloc `agent` : **les rôles ne sont pas mesurés** par le banc ; seul
  l'attachement l'est. Ne pas lire `role` comme une vérité.
- `lu` est tagué **NOUN**, pas VERB : la classe ouverte reste fragile (POS ouvert **0,7918**).
- `pragmatique` publie `double_sens: candidat` : « livre » est dans la liste des mots à double
  sens. C'est un **candidat**, pas une décision — le gold ne l'attend pas.

**Ce qu'il faut en conclure.** L'attachement est utile et vérifié sur ce cas, mais il vient avec
un **doublon d'union**, des rôles non évalués et un POS imparfait. Le champ à consommer est
`cible` (et `candidats`), pas `role` seul ; et `union: true` doit être filtré.

## 3. L'anglais et le marqueur ambigu — `r241`

**Entrée.** `The day when we left was beautiful.` (phrase `reel` du gold, `r241`).

**Commande.**

```bash
python3 tools/drave.py analyser "The day when we left was beautiful." --langue en --json \
  | jq '{langue, script, refus,
         pos: [.etiquettes[] | select(.niveau=="pos")
           | {valeur, type, debut, fin, confiance, ouvert:.meta.ouvert}],
         syntagmes: [.etiquettes[] | select(.niveau=="syntagme")
           | {valeur, type, debut, fin, confiance, role:.meta.role,
              cible:.meta.attachement.cible, union:.meta.union, candidats}]}'
```

**Sortie (réelle).**

```json
{
  "langue": "en",
  "script": "Latn",
  "refus": "",
  "pos": [
    {
      "valeur": "The",
      "type": "DET",
      "debut": 0,
      "fin": 3,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "day",
      "type": "NOUN",
      "debut": 4,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "when",
      "type": "CONJ",
      "debut": 8,
      "fin": 12,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "we",
      "type": "PRON",
      "debut": 13,
      "fin": 15,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "left",
      "type": "VERB",
      "debut": 16,
      "fin": 20,
      "confiance": 0.85,
      "ouvert": true
    },
    {
      "valeur": "was",
      "type": "AUX",
      "debut": 21,
      "fin": 24,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "beautiful",
      "type": "ADJ",
      "debut": 25,
      "fin": 34,
      "confiance": 0.68,
      "ouvert": true
    },
    {
      "valeur": ".",
      "type": "PONCT",
      "debut": 34,
      "fin": 35,
      "confiance": 0.95,
      "ouvert": false
    }
  ],
  "syntagmes": [
    {
      "valeur": "The day",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confiance": 0.35,
      "role": "groupe nominal",
      "cible": "beautiful",
      "union": null,
      "candidats": [
        "GN",
        "beautiful"
      ]
    },
    {
      "valeur": "when we left",
      "type": "REL",
      "debut": 8,
      "fin": 20,
      "confiance": 0.35,
      "role": "qualité",
      "cible": "day",
      "union": null,
      "candidats": [
        "REL",
        "day",
        "beautiful"
      ]
    },
    {
      "valeur": "was beautiful",
      "type": "GV",
      "debut": 21,
      "fin": 34,
      "confiance": 0.35,
      "role": "prédicat",
      "cible": null,
      "union": null,
      "candidats": [
        "GV"
      ]
    }
  ]
}
```

**Lecture.**

- `when` est tagué **CONJ** par le POS, mais il déclenche une **REL** `[8:20] « when we left »`
  → `day` : c'est la correction `AMBIGUES_REL` de la v12 (« when » après un GN = relative ;
  ailleurs, subordonnée). Sans elle, la REL était une SUB et le span était perdu.
- `left` est désormais **VERB** (0,85) et `was` **AUX** ; le POS anglais n'est pas parfait pour
  autant (POS global **0,8625**, ouvert **0,7918**). L'attachement juste et le POS imparfait
  continuent de coexister dans la même sortie.
- `beautiful` est **ADJ**, `The day` **GN**, `was beautiful` **GV** : la segmentation est
  complète. La ponctuation finale sort en **PONCT** depuis le correctif de ponctuation.
- L'attachement `REL → day` est celui du gold ; c'est le **87/87 labels** anglais (88 cibles ;
  `g017` est la seule cible sans span prédit).
- `GV « was beautiful »` a `cible: null` : le bloc ne publie pas d'attachement pour ce GV. `null`
  veut dire « pas de cible publiée », pas « pas de relation ».

**Ce qu'il faut en conclure.** Le produit n'est pas monolingue : il analyse l'anglais et publie
les mêmes champs. Mais une réussite d'attachement peut coexister avec des erreurs de POS ; les
deux mesures sont séparées (POS **0,8625** ; attachement **238/238 labels**, 238/239 cibles,
**0,9958**). Ne pas conclure « tout est bon » à partir d'une seule ligne.

## 4. Le refus — texte vide

**Entrée.** `""` (chaîne vide).

**Commande (CLI).**

```bash
python3 tools/drave.py analyser ""; echo "exit=$?"
```

**Sortie (réelle).**

```
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
exit=3
```

Sans `--json`, le CLI écrit sur `stderr` et sort **3**. Avec `--json`, il écrit l'annotation de
refus sur `stdout` (`schema: "drave.annotation"`, `version: 2`, `refus: "vide"`,
`etiquettes: []`) et sort toujours **3** : le contrat (code 3 + JSON) est implémenté. C'est l'API
(`bloc_linguistique.py`), derrière le CLI, qui porte le même état :

**Commande (API).**

```bash
python3 tools/bloc_linguistique.py --texte "" --json \
  | jq '{langue, script, refus, etiquettes: (.etiquettes|length)}'
```

**Sortie (réelle).**

```json
{
  "langue": "und",
  "script": "Zyyy",
  "refus": "vide",
  "etiquettes": 0
}
```

**Lecture.**

- `refus: "vide"` : le bloc **refuse** au lieu d'inventer une analyse.
- `langue: und`, `script: Zyyy` : rien à détecter.
- Zéro étiquette, zéro unité, fraction 0.
- **Le CLI sort 3** ; avec `--json`, il rend le même JSON de refus. Le contrat cible (code **3** +
  JSON sur `stdout`) est donc tenu (`tools/drave.py`).

**Ce qu'il faut en conclure.** Un pipeline doit traiter `refus` comme un état de première classe :
un texte vide ne produit pas une annotation vide « comme les autres ». Le CLI et l'API le disent
dans le JSON et le code de sortie ; c'est une garantie de non-invention, pas un bug.

## 5. L'échec autrefois connu — `r035`, désormais prédit

**Entrée.** `The film she talks about is out.` (phrase `reel` du gold, `r035`).

> **Ce bloc était l'échec connu de la doc.** Il ne l'est plus : la règle de **relative zéro**
> (J1.1) rétablit le span et la cible. La sortie ci-dessous est celle du 14/11 ; l'échec courant,
> lui, s'appelle `g017` (voir la fin de cette section).

**Le gold attend** (extrait de `tools/tests/linguistique/gold_reel.json`) :

```json
{
  "type": "REL",
  "texte": "she talks about",
  "debut": 9,
  "fin": 24,
  "cible": "film"
}
```

**Commande.**

```bash
python3 tools/drave.py analyser "The film she talks about is out." --json \
  | jq '{langue, script, refus,
         syntagmes: [.etiquettes[] | select(.niveau=="syntagme")
           | {valeur, type, debut, fin, confiance, role:.meta.role,
              cible:.meta.attachement.cible, union:.meta.union, candidats}],
         phrase: [.etiquettes[] | select(.niveau=="phrase") | {type, valeur}],
         pragmatique: [.etiquettes[] | select(.niveau=="pragmatique") | {type, valeur}]}'
```

**Sortie (réelle).**

```json
{
  "langue": "en",
  "script": "Latn",
  "refus": "",
  "syntagmes": [
    {
      "valeur": "The film",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.35,
      "role": "groupe nominal",
      "cible": "out",
      "union": null,
      "candidats": [
        "GN",
        "out"
      ]
    },
    {
      "valeur": "she talks about",
      "type": "REL",
      "debut": 9,
      "fin": 24,
      "confiance": 0.35,
      "role": "qualité",
      "cible": "film",
      "union": null,
      "candidats": [
        "REL",
        "film",
        "out"
      ]
    },
    {
      "valeur": "is out",
      "type": "GV",
      "debut": 25,
      "fin": 31,
      "confiance": 0.35,
      "role": "prédicat",
      "cible": null,
      "union": null,
      "candidats": [
        "GV"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type",
      "valeur": "déclarative"
    }
  ],
  "pragmatique": [
    {
      "type": "acte",
      "valeur": "assertion"
    }
  ]
}
```

**Lecture.**

- Le bloc prédit exactement les trois spans du gold : `GN « The film » [0:8]`, `REL « she talks
  about » [9:24] → film` et `GV « is out » [25:31]`. **La REL est là**, avec la cible attendue.
- La relative est **sans marqueur** (« the film **she talks about** » : le pronom relatif est
  absent). La règle **relative zéro** (`relative_zero`, J1.1) la retrouve : GN antécédent, pronom
  sujet, verbe, préposition orpheline. C'était l'un des « 17 spans inatteignables » de la v12 ;
  ce n'est plus le cas.
- L'exactitude d'attachement est **238/238 labels = 1,0000**, mais elle reste **conditionnelle
  aux spans prédits** ; la couverture est **238/239 = 0,9958**. Les deux chiffres doivent être lus
  ensemble.
- Le seul span du gold encore manquant qui porte une cible est `g017` : `SUB [9:28] « that she
  would come »`, que le bloc étend à `[9:38]` en absorbant `yesterday`. C'est l'échec courant,
  et la règle qui le corrigerait a été **rejetée** (J6.1, test −0,0028).
- Le gold attend aussi `GN « The film » [0:8]` : le bloc le rend exactement. Le **span** doit
  être exact pour compter, et il l'est ici.

**Ce qu'il faut en conclure.** Le produit est **précis sur ce qu'il voit, silencieux sur ce qu'il
ne voit pas**. Un utilisateur qui a besoin d'une REL doit vérifier qu'elle est présente dans le
JSON (`type: "REL"`), pas seulement que l'attachement est bon. Et il ne doit pas lire `1,0000`
comme « 100 % du langage » : c'est 100 % des spans prédits, sur **99,58 %** des cibles. Le cas
`g017` montre que la couverture n'est pas encore complète.

## 6. Ce que ces exemples ne montrent pas

1. **Pas de restitution, pas de traduction, pas de génération** : la sortie ne contient aucun
   texte produit ; seulement des étiquettes. Le produit ne réécrit pas la phrase.
2. **Pas de neuronal** : tout vient de `Heuristique` (CPU) ; `MockNeuronal` est un contrat, pas un
   tagger, et le CLI ne l'expose pas. La cascade 7B (0,9415) n'est pas un chemin livré.
3. **Pas de couverture complète** : sur les **239 cibles d'attachement**, **238** ont un span
   prédit (**0,9958**) ; la seule qui manque est `g017` (`SUB [9:28]`). `r035`, autrefois manqué,
   est désormais prédit (§ 5).
4. **Pas de lecture unique garantie** : le **doublon REL de l'union** (`union: true`) est publié ;
   il faut le filtrer si l'on veut un seul segment par span.
5. **Pas de valeurs normalisées** : `candidats` sont des chaînes et `role` n'est pas normalisé
   (`predicat`/`prédicat`). Le **format** est versionné (v2 ; v1 reste lue), mais le vocabulaire
   des valeurs, lui, n'a pas de schéma.

Pour mesurer sur votre propre corpus, il faut le format du gold (mots + segments + pragma) : il
n'est pas publié comme schéma — c'est un des manques du CLI (notice § 7). Le schéma de
l'**annotation** du produit, lui, est publié : [`drave-annotation-v2.json`](../../tools/schemas/drave-annotation-v2.json).

## 7. Où aller ensuite

| si vous voulez… | allez à |
|---|---|
| **la notice d'usage** | [`README.md`](README.md) |
| **le schéma du JSON (v2, v1)** | [`drave-annotation-v2.json`](../../tools/schemas/drave-annotation-v2.json) · [`drave-annotation-v1.json`](../../tools/schemas/drave-annotation-v1.json) |
| **le contrat du bloc** | [`docs/implantation/bloc-linguistique.md`](../implantation/bloc-linguistique.md) |
| **le rejeu de ces cinq blocs** | [`reports/rapport-exemples-rejoues.md`](../../reports/rapport-exemples-rejoues.md) |
| **les chiffres courants** | [convention GV](../../reports/rapport-convention-gv.md) · [`s065`](../../reports/rapport-s065.md) · [`r035`](../../reports/rapport-r035.md) |
| **les 17 spans de la v12 (instantané)** | [`reports/rapport-pensee-v12.md`](../../reports/rapport-pensee-v12.md) |
| **l'audit et les contrôles** | [`reports/rapport-audit-v10.md`](../../reports/rapport-audit-v10.md) |
| **le gold réel** | `tools/tests/linguistique/gold_reel.json` |
