# Dix exemples d'analyse, commentés

> **Ce que ce document est.** Dix exécutions **réelles** du produit, avec leur JSON commenté. Il
> complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
> *comment lire* ce qui sort. Les **cinq premiers blocs** ont été produits le **2026-11-06** sur
> la branche `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et
> sans réseau ; ils ont été **rejoués le 2026-11-16** sur le code courant — F1 **0,7902**,
> attachement **238/238 labels** (238/239 cibles), schéma **v2**. Le format v2 ajoute
> `version: 2`, `meta.attachement.candidats` en **objets** `{span, cible, source}`, un
> `meta.role` **normalisé** (huit valeurs) et, sur un syntagme qui chevauche un autre,
> `meta.partition`/`meta.alternative` ; v1 reste lue
> ([schéma v2](../../tools/schemas/drave-annotation-v2.json)).
>
> **Le rejeu du 2026-11-16.** **3 blocs sur 5** ont bougé, tous par la **normalisation des
> rôles** : `qualité` → `qualite`, `prédicat` → `predicat`, `groupe nominal` → `objet`.
> Le refus est identique champ pour champ ; `g001` l'est aussi pour les champs existants, et
> gagne en plus les **candidats objets** et un bloc de **durée**. Les candidats objets sont
> publiés dans `meta.attachement.candidats` (le champ historique `candidats` reste une liste de
> chaînes) ; `--duree` ajoute `cout.duree_s` (absent par défaut). Le **contrôle négatif** est
> [`tools/verifie_exemples.py`](../../tools/verifie_exemples.py) : il rejoue les blocs et compare
> le JSON **parsé**, pas le texte. Fiche :
> [`reports/rapport-exemples-v2.md`](../../reports/rapport-exemples-v2.md).
>
> **Les cinq blocs du 15/11.** Trois exécutions avec `--tagger` (§ 6) et deux avec `--reel`
> (§ 7), produites le **2026-11-15** avec la **clé DeepSeek** et un **cache disque neuf** : le
> coût affiché est donc réel (`réseau=1`, tokens non nuls). Le tagger ne change que le **POS** ;
> les syntagmes, rôles et attachements restent à l'heuristique. La base `--reel` est la **base
> honnête** : 452 phrases réelles (main + corpus), sans les 160 synthétiques.
>
> **Les chiffres de référence (15/11).** Gold **vivant 612** : F1 **0,7902**, POS **0,8625**,
> attachement **238/238 labels** (**238/239 cibles**, 0,9958), schéma **v2**. Gold **réel 452** :
> POS **0,8891**, F1 **0,7906**, attachement **183/184 labels** (0,9946). Les trois annotations
> `--tagger` sont en v2 (`schema: "drave.annotation"`, `version: 2`).
>
> **L'historique du rejeu.** Le rejeu du **14/11** avait corrigé **4 blocs sur 5** : ponctuation
> finale dans le POS (20 étiquettes), refus en **3**, POS anglais de `r241`, et `r035` —
> l'ancien échec — désormais **prédit**. Son récit et ses chiffres datés restent dans
> [`reports/rapport-exemples-rejoues.md`](../../reports/rapport-exemples-rejoues.md) ; le rejeu
> du 16/11 ci-dessus le remplace pour les rôles et les candidats.
>
> **Une commande, un JSON.** `python3 tools/drave.py analyser "…" --json` rend l'annotation
> complète (neuf niveaux). Pour la lire, ce document filtre avec `jq` ; le produit, lui, n'a pas
> besoin de `jq`. Avec `--tagger`, le JSON garde le même contrat v2 et le **coût** part sur
> `stderr` ; avec `--reel`, `evaluer --json` rend un **rapport de mesure**, pas une annotation.

## 0. Comment lire les JSON

- `debut` / `fin` : indices en **points de code Unicode**, 0-based, fin exclue : `[debut:fin)`.
  « Élodie » → `[0:6]` ; un emoji compte pour **un** point.
- `niveau` : `pos`, `syntagme`, `phrase` et `pragmatique` sont montrés ; `graphème`, `mot`,
  `morphème`, `discours` et `document` sont omis (ils existent dans le JSON complet).
- `confiance` : **déclarée**, pas calibrée. 0,3 pour un NOUN ouvert, 0,92 pour un DET. Avec
  `--tagger`, les POS neuronaux portent **0,60** : c'est le **seuil de la cascade**, pas une
  probabilité par token ; ils ont `source: "neuronal"`, `meta.modele: true` et **pas** de
  `meta.ouvert` (le tagger ne consulte pas le lexique). La ponctuation, restituée depuis
  l'heuristique, garde 0,95 et `meta.ouvert: false`.
- `meta.role` : un **vocabulaire fermé** de huit valeurs — `predicat`, `agent`, `objet`,
  `lieu`, `temps`, `qualite`, `possesseur`, `destinataire`. Les règles produisent des
  orthographes et des granularités différentes ; le JSON publie la forme canonique
  (`prédicat` → `predicat`, `qualité` → `qualite`, `groupe nominal`/`patient`/`complément` →
  `objet`). C'est une **normalisation**, pas un raffinement sémantique.
- `cout.duree_s` : **absent par défaut** ; `--duree` l'ajoute au JSON. C'est une mesure
  locale à l'horloge murale, en secondes : deux exécutions donnent deux valeurs. Le script de
  vérification contrôle sa **présence** et son **type**, jamais sa valeur.
- `TAGGER API` : la ligne de **coût** (`modèle`, `appels`, `réseau`, `cache`, `tokens`, `latence`).
  Elle va sur `stdout` avec `analyser --tagger` et sur `stderr` avec `--json` ; la **clé n'y est
  jamais**. Un cache chaud affiche `réseau=0 · cache=1 · tokens=0`.
- `--reel` : ce n'est pas une annotation, c'est une **évaluation**. Le JSON porte
  `gold.nom: "réel (hand + reel, sans synthétique)"`, `gold.phrases: 452`,
  `gold.cibles_attachement: 184` et `reel: null` (la base mesurée **est** déjà la base réelle).
- `meta.attachement` : `{segment, cible, candidats}` ; `cible` est une **chaîne**, et
  `candidats` (v2) est une liste d'objets `{span, cible, source}` — `span` donne la position
  exacte de la cible dans `texte`. Un candidat dont la cible n'est pas retrouvée est écarté.
- `meta.partition` : `{groupe, rang, membres, vue}` — présent sur un syntagme d'un groupe de
  chevauchement (v2) ; `rang: 1` est la vue préférée, pas une suppression.
- `meta.alternative` : la liste des autres segments du groupe (`type`, `debut`, `fin`, `source`,
  `union`, `relation`, `rang`, `role`, `attachement`, `retire` en vue filtrée) — v2.
- `candidats` : le champ **historique** de l'étiquette, des **chaînes d'affichage** (parfois
  « « qui dort » → voisine ») ; c'est la sortie lisible et le contrat v1. Le JSON v2 publie
  les mêmes candidats en objets dans `meta.attachement.candidats` (voir la notice § 3.2).
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
           partition:.meta.partition, alternative:.meta.alternative, candidats,
           candidats_objets:.meta.attachement.candidats}],
  phrase: [.etiquettes[] | select(.niveau=="phrase") | {type, valeur}],
  pragmatique: [.etiquettes[] | select(.niveau=="pragmatique") | {type, valeur}],
  unites_semantiques}'
```

Puis : `python3 tools/drave.py analyser "…" --json | jq "$FILTRE"`.

`candidats` est la liste **historique** de chaînes ; `candidats_objets` est la même liste en
objets `{span, cible, source}` (v2), avec `texte[span.debut:span.fin] == cible`. `role` est
déjà normalisé par le produit. Les cinq blocs ci-dessous sélectionnent les deux formes pour que
l'écart entre le contrat v1 et le contrat v2 soit visible.

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
              cible:.meta.attachement.cible, union:.meta.union, candidats,
              candidats_objets:.meta.attachement.candidats}],
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
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 8,
            "fin": 12
          },
          "cible": "dort",
          "source": "heuristique"
        }
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
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 3,
            "fin": 7
          },
          "cible": "chat",
          "source": "heuristique"
        }
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

**La durée (optionnelle).** Sans `--duree`, `cout` ne porte pas d'horloge ; avec le drapeau,
`cout.duree_s` est ajouté. C'est une mesure **locale** : la valeur ci-dessous est celle du
rejeu, elle change à chaque exécution.

```bash
python3 tools/drave.py analyser "Le chat dort." --json --duree \
  | jq '{duree_s: .cout.duree_s, octets: .cout.octets}'
```

**Sortie (réelle).**

```json
{
  "duree_s": 0.00581,
  "octets": 13
}
```

**Lecture.**

- `langue: fr`, `script: Latn`, `refus: ""` : le texte est accepté.
- Quatre POS : `Le/DET`, `chat/NOUN`, `dort/VERB` et `.`/`PONCT` (0,95). `chat` et `dort` sont
  **ouverts** (confiance 0,3 et 0,72) : le lexique ne les connaît pas comme classes fermées.
- Deux syntagmes : `GN « Le chat » [0:7] → dort` et `GV « dort » [8:12] → chat`. Le gold `g001`
  attend exactement ces deux spans et `assertion` ; c'est le cas de base réussi.
- Les rôles sont **normalisés** : `agent` et `predicat` (sans accent) appartiennent au
  vocabulaire fermé. Les `candidats_objets` donnent la position exacte de chaque cible —
  `dort[8:12]` pour le GN, `chat[3:7]` pour le GV — et le premier objet est la cible choisie.
  Le champ `candidats`, lui, reste la liste de chaînes du contrat v1.
- L'extrait omet `fraction_semantique`, `unites_semantiques`, `trace` et `cout` (présents dans le
  JSON complet) ; la sortie lisible donne **2 unités**, soit **61,5 %** du texte. La durée
  n'est publiée que sur demande (`--duree`, ci-dessus).

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
              cible:.meta.attachement.cible, union:.meta.union, candidats,
              candidats_objets:.meta.attachement.candidats}],
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
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 25,
            "fin": 36
          },
          "cible": "intéressant",
          "source": "heuristique"
        },
        {
          "span": {
            "debut": 0,
            "fin": 8
          },
          "cible": "Le livre",
          "source": "heuristique"
        },
        {
          "span": {
            "debut": 3,
            "fin": 8
          },
          "cible": "livre",
          "source": "heuristique"
        }
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
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 3,
            "fin": 8
          },
          "cible": "livre",
          "source": "heuristique"
        },
        {
          "span": {
            "debut": 0,
            "fin": 8
          },
          "cible": "Le livre",
          "source": "heuristique"
        },
        {
          "span": {
            "debut": 25,
            "fin": 36
          },
          "cible": "intéressant",
          "source": "heuristique"
        }
      ]
    },
    {
      "valeur": "que j'ai lu est intéressant",
      "type": "REL",
      "debut": 9,
      "fin": 36,
      "confiance": 0.3,
      "role": "qualite",
      "cible": "livre",
      "union": true,
      "candidats": [
        "REL",
        "livre",
        "intéressant"
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 3,
            "fin": 8
          },
          "cible": "livre",
          "source": "heuristique"
        },
        {
          "span": {
            "debut": 25,
            "fin": 36
          },
          "cible": "intéressant",
          "source": "heuristique"
        }
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
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 3,
            "fin": 8
          },
          "cible": "livre",
          "source": "heuristique"
        },
        {
          "span": {
            "debut": 0,
            "fin": 8
          },
          "cible": "Le livre",
          "source": "heuristique"
        }
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
- Les deux REL portent `role: qualite` : la forme accentuée `qualité` est **normalisée**, comme
  `prédicat` en `predicat`. Les `candidats_objets` publient `livre[3:8]` et
  `intéressant[25:36]` avec leur source, sans changer l'attachement.
- `GN « Le livre » → intéressant` : le GN est rattaché au GV, pas à la REL. Le gold annote ce GN
  `patient`, le bloc `agent` : **les rôles ne sont pas mesurés** par le banc ; seul
  l'attachement l'est. Ne pas lire `role` comme une vérité.
- `lu` est tagué **NOUN**, pas VERB : la classe ouverte reste fragile (POS ouvert **0,7918**).
- `pragmatique` publie `double_sens: candidat` : « livre » est dans la liste des mots à double
  sens. C'est un **candidat**, pas une décision — le gold ne l'attend pas.

**Ce qu'il faut en conclure.** L'attachement est utile et vérifié sur ce cas, mais il vient avec
un **doublon d'union**, des rôles non évalués et un POS imparfait. Le champ à consommer est
`cible` (et `candidats_objets`), pas `role` seul ; et `union: true` doit être filtré.

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
              cible:.meta.attachement.cible, union:.meta.union, candidats,
              candidats_objets:.meta.attachement.candidats}]}'
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
      "role": "objet",
      "cible": "beautiful",
      "union": null,
      "candidats": [
        "GN",
        "beautiful"
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 25,
            "fin": 34
          },
          "cible": "beautiful",
          "source": "heuristique"
        }
      ]
    },
    {
      "valeur": "when we left",
      "type": "REL",
      "debut": 8,
      "fin": 20,
      "confiance": 0.35,
      "role": "qualite",
      "cible": "day",
      "union": null,
      "candidats": [
        "REL",
        "day",
        "beautiful"
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 4,
            "fin": 7
          },
          "cible": "day",
          "source": "heuristique"
        },
        {
          "span": {
            "debut": 25,
            "fin": 34
          },
          "cible": "beautiful",
          "source": "heuristique"
        }
      ]
    },
    {
      "valeur": "was beautiful",
      "type": "GV",
      "debut": 21,
      "fin": 34,
      "confiance": 0.35,
      "role": "predicat",
      "cible": null,
      "union": null,
      "candidats": [
        "GV"
      ],
      "candidats_objets": null
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
- Les rôles sont **normalisés** : `The day` est `objet` (le brut `groupe nominal` tombe sur
  `objet`), `when we left` `qualite`, `was beautiful` `predicat`. Les candidats objets donnent
  `beautiful[25:34]`, `day[4:7]` et la source heuristique ; le GV n'a pas de candidat publié.
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
              cible:.meta.attachement.cible, union:.meta.union, candidats,
              candidats_objets:.meta.attachement.candidats}],
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
      "role": "objet",
      "cible": "out",
      "union": null,
      "candidats": [
        "GN",
        "out"
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 21,
            "fin": 24
          },
          "cible": "out",
          "source": "heuristique"
        }
      ]
    },
    {
      "valeur": "she talks about",
      "type": "REL",
      "debut": 9,
      "fin": 24,
      "confiance": 0.35,
      "role": "qualite",
      "cible": "film",
      "union": null,
      "candidats": [
        "REL",
        "film",
        "out"
      ],
      "candidats_objets": [
        {
          "span": {
            "debut": 4,
            "fin": 8
          },
          "cible": "film",
          "source": "heuristique"
        },
        {
          "span": {
            "debut": 21,
            "fin": 24
          },
          "cible": "out",
          "source": "heuristique"
        }
      ]
    },
    {
      "valeur": "is out",
      "type": "GV",
      "debut": 25,
      "fin": 31,
      "confiance": 0.35,
      "role": "predicat",
      "cible": null,
      "union": null,
      "candidats": [
        "GV"
      ],
      "candidats_objets": null
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
- Rôles **normalisés** : `The film` est `objet` (brut `groupe nominal`), `she talks about`
  `qualite` (brut `qualité`), `is out` `predicat`. Les candidats objets publient `out[21:24]`
  pour le GN et `film[4:8]`, `out[21:24]` pour la REL ; le GV n'en publie aucun (`null`).
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

## 6. Le tagger en option — trois exécutions avec la clé

> **Le dispositif.** Les trois commandes ci-dessous ont été lancées le **2026-11-15** avec la clé
> lue dans `~/.config/drave/deepseek.key` et un **cache disque neuf** (`DEEPSEEK_CACHE` pointant
> vers un répertoire vide) : chaque ligne `TAGGER API` montre donc un **vrai appel réseau**
> (`réseau=1`, `cache=0`). Sans cette précaution, le cache du client rend
> `réseau=0 · cache=1 · tokens=0` et le coût affiché n'est plus celui du jour. La clé n'est
> jamais affichée. Le tagger ne remplace que le **POS** ; les syntagmes, rôles, cibles et la
> pragmatique restent ceux de l'heuristique.

### 6.1 `g001` — le cas neutre

**Entrée.** `Le chat dort.` (phrase `hand`, `g001`).

**Commande.**

```bash
python3 tools/drave.py analyser "Le chat dort." --tagger
```

**Sortie (réelle, cache neuf).**

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
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.1 s
```

**Lecture.** Le POS est **identique** à celui du § 1 : `Le/DET`, `chat/NOUN`, `dort/VERB` et
`./PONCT` ; les deux syntagmes et l'acte aussi. Le seul changement est l'en-tête
(`source=cascade`) et la ligne de coût. C'est le **cas neutre** : le tagger ne dégrade pas une
phrase que l'heuristique réussissait déjà, mais il coûte **1 appel et 130 tokens**. La
ponctuation est bien là (restituée depuis l'heuristique) : l'ancien défaut « `PONCT` perdu »
est corrigé.

### 6.2 `g011` — `lu` redevient un verbe

**Entrée.** `Le livre que j'ai lu est intéressant.` (phrase `hand`, `g011`).

**Commande.**

```bash
python3 tools/drave.py analyser "Le livre que j'ai lu est intéressant." --tagger
```

**Sortie (réelle, cache neuf).**

```
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 43 étiquettes · unités sémantiques=3 (48.6% du texte)
POS  Le/DET livre/NOUN que/PRON j'ai/PRON lu/VERB est/AUX intéressant/ADJ ./PONCT
SYNTAGMES
  GN   [0:8]    Le livre                     rôle=agent     → intéressant
  REL  [9:20]   que j'ai lu                  rôle=qualite   → livre
  REL  [9:36]   que j'ai lu est intéressant  rôle=qualite   → livre
  GV   [21:36]  est intéressant              rôle=predicat  → livre
PRAGMATIQUE
  phrase [0:37] déclarative · acte=assertion · négation=non · modalité=non · double sens=oui
COUVERTURE  (confiance max par niveau)  graphème=0.99 · morphème=0.32 · mot=0.98 · pos=0.95 ·
            syntagme=0.55 · phrase=0.85 · discours=0.55 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=157 · latence=1.5 s
```

**Lecture.** Le gold attend `lu/VERB` et `que/CONJ`. L'heuristique rend `lu/NOUN` (§ 2) ; le
tagger rend **`lu/VERB`** : la classe ouverte est réparée sur ce token. Mais `que` reste
**PRON** (le gold attend `CONJ`) : le tagger ne répare pas tout. Les syntagmes sont **identiques**
à ceux du § 2 : le tagger ne rend ni rôle ni cible, et le doublon d'union reste publié.

Le JSON garde le contrat v2 ; on peut le vérifier sur le token réparé et sur la ponctuation :

```bash
python3 tools/drave.py analyser "Le livre que j'ai lu est intéressant." --tagger --json \
  | jq '{schema, version, langue, script, refus,
         lu: [.etiquettes[] | select(.niveau=="pos" and .valeur=="lu")][0],
         ponct: [.etiquettes[] | select(.niveau=="pos" and .valeur==".")][0]}'
```

**Sortie (réelle, extrait).**

```json
{
  "schema": "drave.annotation",
  "version": 2,
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "lu": {
    "niveau": "pos",
    "type": "VERB",
    "valeur": "lu",
    "debut": 18,
    "fin": 20,
    "source": "neuronal",
    "confiance": 0.6,
    "candidats": [],
    "langue": "und",
    "script": "Latn",
    "meta": {
      "modele": true
    }
  },
  "ponct": {
    "niveau": "pos",
    "type": "PONCT",
    "valeur": ".",
    "debut": 36,
    "fin": 37,
    "source": "heuristique",
    "confiance": 0.95,
    "candidats": [],
    "langue": "fr",
    "script": "Latn",
    "meta": {
      "ouvert": false
    }
  }
}
```

**Lecture du JSON.** `schema: "drave.annotation"` et `version: 2` : le contrat est le même que
pour l'heuristique. `lu` porte `source: "neuronal"`, `confiance: 0.6` et `meta.modele: true` :
c'est le **seuil de la cascade**, pas une confiance calibrée, et `meta.ouvert` est **absent**
(le tagger ne consulte pas le lexique). `PONCT` porte `source: "heuristique"`, `0.95` et
`meta.ouvert: false` parce qu'il vient de l'heuristique. Le coût, lui, n'est **pas** dans ce
JSON : il part sur `stderr` avec `--json` (et sur `stdout` sans `--json`).

### 6.3 `r241` — `when` redevient un pronom

**Entrée.** `The day when we left was beautiful.` (phrase `reel`, `r241`).

**Commande.**

```bash
python3 tools/drave.py analyser "The day when we left was beautiful." --langue en --tagger
```

**Sortie (réelle, cache neuf).**

```
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=en script=Latn source=cascade · 38 étiquettes · unités sémantiques=3 (45.7% du texte)
POS  The/DET day/NOUN when/PRON we/PRON left/VERB was/AUX beautiful/ADJ ./PONCT
SYNTAGMES
  GN   [0:7]    The day        rôle=objet     → beautiful
  REL  [8:20]   when we left   rôle=qualite   → day
  GV   [21:34]  was beautiful  rôle=predicat  → —
PRAGMATIQUE
  phrase [0:35] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · morphème=0.32 · mot=0.98 · pos=0.95 ·
            syntagme=0.35 · phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=154 · latence=1.1 s
```

**Lecture.** Le gold attend `when/PRON` ; l'heuristique rend `when/CONJ` (§ 3), le tagger rend
**`when/PRON`** : le POS anglais est réparé sur ce token. `left/VERB`, `was/AUX`,
`beautiful/ADJ` et la ponctuation sont inchangés. L'attachement `REL → day` est celui de
l'heuristique : le tagger ne touche pas aux syntagmes. Le tagger est **prompté en français** et
étiquette ici l'anglais correctement ; ce n'est pas une preuve de qualité par langue (la
ventilation du tagger par langue n'est pas faite).

### 6.4 Ce que les trois exemples mesurent — et ne mesurent pas

| bloc | tokens du gold | heuristique | `--tagger` | ce qui change |
|---|---:|---:|---:|---|
| `g001` | 3 | 3/3 | **3/3** | rien |
| `g011` | 7 | 5/7 | **6/7** | `lu` NOUN → VERB |
| `r241` | 7 | 6/7 | **7/7** | `when` CONJ → PRON |
| **total** | **17** | **14/17 = 82,35 %** | **16/17 = 94,12 %** | **+2 tokens** |

**Lecture.** Le tagger **gagne 2 tokens** sur cet échantillon et n'en perd aucun. Mais **17
tokens ne sont pas une mesure** : c'est un choix d'exemples, et il surévalue le gain. Les
chiffres globaux, eux, sont dans [`rapport-tagger-option.md`](../../reports/rapport-tagger-option.md) :
POS **0,9575 contre 0,8625** sur le gold **612** (**+9,5 pts**), et **0,9500 contre 0,8891** sur
le **réel 452** (**+6,1 pts**). Le gain est porté par le synthétique ; le réel vaut +6,1, pas
+9,5.

**Le coût des trois exemples.** **3 appels**, **441 tokens** (130 + 157 + 154), **3,7 s** de
latence cumulée, `réseau=1` et `cache=0` à chaque fois. Au prorata du chiffre publié (~0,02 $
pour 612 phrases / 22 299 tokens), cela vaut **~0,0004 $** : une **estimation**, pas une facture.
Un cache chaud rejoue la même annotation avec `réseau=0 · cache=1 · tokens=0` ; c'est le
comportement attendu, pas une mesure de coût.

## 7. La base honnête — deux exécutions avec `--reel`

> **Le dispositif.** `--reel` ne change pas l'analyse : il **restreint l'évaluation** aux
> phrases `hand` + `reel` (**452**), sans les 160 synthétiques. Deux lectures : la sortie
> lisible, puis le JSON qui la porte. Aucune clé, aucun réseau.

### 7.1 `evaluer --reel` — la sortie lisible

**Commande.**

```bash
python3 tools/drave.py evaluer --reel
```

**Sortie (réelle).**

```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold réel (hand + reel, sans synthétique) · 452 phrases · 2480 tokens · 184 cibles d'attachement

POS         exactitude 88.91 %  (fermé 92.94 %, ouvert 84.66 %)
SYNTAGMES   F1 79.06 %  (P 81.28 % / R 76.95 %)
  tête      F1 89.90 %  (P 93.84 % / R 86.28 %)
  vue linéaire (partition filtrer) F1 79.53 %  · attachement 91.85 % de couverture
BASE RÉELLE — (déjà la base, ou gold gelé)
ATTACHEMENT exact 99.46 % · couverture 99.46 % · exact sur span 100.00 % · top-k 98.91 %
  tête      couverture 100.00 % · top-k 99.45 %
PRAGMATIQUE acte 99.56 % · négation 96.90 % · modalité 98.45 % · double sens 96.46 %
FRACTION SÉMANTIQUE 50.82 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 0.00 % (graine 0, 184 cibles)
```

**Lecture.** La base fait **452 phrases**, **2 480 tokens** et **184 cibles**. Le POS est
**88,91 %** (fermé 92,94, ouvert 84,66), la F1 **79,06 %** (P 81,28 / R 76,95), l'attachement
**99,46 %** (183/184 labels). `BASE RÉELLE — (déjà la base, ou gold gelé)` est la confirmation
que `--reel` mesure directement cette base ; sans `--reel`, la même ligne est **calculée et
publiée à côté** du global 612. Le contrôle négatif (cible exacte tirée au hasard) est à
**0,00 %** : c'est le plancher, pas une performance.

**Pourquoi « honnête ».** Le global 612 (hand + reel + **160 synthétiques**) donne POS
**86,25 %**, F1 **79,02 %**, attachement **99,58 %**. Le synthétique est **plus difficile** pour
le POS (mots hors lexique) : il **tire la moyenne vers le bas**, et le 86,25 sous-estime donc
la qualité réelle. La F1, elle, est quasi identique (79,06 contre 79,02). Publier le seul
global cache cet effet. Les 452 incluent les 20 phrases `hand` et 432 phrases de corpus : ce
n'est **pas un tirage aléatoire**.

### 7.2 `evaluer --reel --json` — le contrat de la mesure

**Commande.**

```bash
python3 tools/drave.py evaluer --reel --json \
  | jq '{version, gold, reel,
         pos: (.heuristique.pos | {exactitude, exactitude_ferme, exactitude_ouvert, tokens}),
         f1: (.heuristique.syntagme | {f1, precision, rappel}),
         attachement: (.heuristique.attachement | {cibles, labels, exact, exact_taux, couverture}),
         controle_negatif}'
```

**Sortie (réelle).**

```json
{
  "version": "0.1.0",
  "gold": {
    "nom": "réel (hand + reel, sans synthétique)",
    "gele": false,
    "phrases": 452,
    "tokens": 2480,
    "cibles_attachement": 184
  },
  "reel": null,
  "pos": {
    "exactitude": 0.8891,
    "exactitude_ferme": 0.9294,
    "exactitude_ouvert": 0.8466,
    "tokens": 2480
  },
  "f1": {
    "f1": 0.7906,
    "precision": 0.8128,
    "rappel": 0.7695
  },
  "attachement": {
    "cibles": 184,
    "labels": 183,
    "exact": 183,
    "exact_taux": 0.9946,
    "couverture": 0.9946
  },
  "controle_negatif": {
    "nom": "cible exacte tirée au hasard dans le gold",
    "graine": 0,
    "cibles": 184,
    "exact_taux": 0.0
  }
}
```

**Lecture.** `gold.nom` **nomme la base** mesurée, `gold.phrases: 452` et
`gold.cibles_attachement: 184` la bornent. `reel: null` est **attendu** : la base mesurée est
déjà la base réelle ; sans `--reel`, ce champ porte un objet (452 phrases, POS, F1,
attachement) calculé à côté du global. Les nombres sont **les mêmes** que dans la sortie
lisible : 0,8891, 0,7906, 0,9946. Attention : ce JSON est un **rapport d'évaluation**
(`version: "0.1.0"` est celle du CLI), pas une **annotation** : le schéma `drave.annotation`
v2 ne s'applique pas ici.

## 8. Ce que ces exemples ne montrent pas

1. **Pas de restitution, pas de traduction, pas de génération** : la sortie ne contient aucun
   texte produit ; seulement des étiquettes. Le produit ne réécrit pas la phrase.
2. **Pas de neuronal local** : le défaut reste `Heuristique` (CPU, hors ligne) ; `MockNeuronal`
   est un contrat, pas un tagger. Le CLI expose en **option** le tagger POS de l'**API DeepSeek**
   (`--tagger`, § 6), pas un modèle local : la cascade 7B locale (0,9415) n'est pas un chemin
   livré.
3. **Pas de couverture complète** : sur les **239 cibles d'attachement** du gold vivant, **238**
   ont un span prédit (**0,9958**) ; la seule qui manque est `g017` (`SUB [9:28]`). Sur la base
   réelle 452, **183/184** cibles ont un span (0,9946). `r035`, autrefois manqué, est désormais
   prédit (§ 5).
4. **Pas de lecture unique garantie** : le **doublon REL de l'union** (`union: true`) est publié ;
   il faut le filtrer si l'on veut un seul segment par span.
5. **Pas de valeurs raffinées** : les rôles sont **normalisés** dans un vocabulaire fermé de
   huit valeurs (`predicat` sans accent, `groupe nominal` → `objet`), pas raffinés. Le champ
   historique `candidats` reste une liste de chaînes ; les **objets** `{span, cible, source}`
   sont dans `meta.attachement.candidats` et le premier objet est la cible choisie. Le **format**
   est versionné (v2 ; v1 reste lue) et le schéma publie le vocabulaire des rôles. Avec
   `--tagger`, `confiance` vaut **0,60** (le seuil de la cascade), `source` vaut `neuronal` et
   `meta.ouvert` est **absent** : ne pas lire ces champs comme une probabilité.

Pour mesurer sur votre propre corpus, il faut le format du gold (mots + segments + pragma) : il
n'est pas publié comme schéma — c'est un des manques du CLI (notice § 7). Le schéma de
l'**annotation** du produit, lui, est publié : [`drave-annotation-v2.json`](../../tools/schemas/drave-annotation-v2.json).

## 9. Où aller ensuite

| si vous voulez… | allez à |
|---|---|
| **la notice d'usage** | [`README.md`](README.md) |
| **le schéma du JSON (v2, v1)** | [`drave-annotation-v2.json`](../../tools/schemas/drave-annotation-v2.json) · [`drave-annotation-v1.json`](../../tools/schemas/drave-annotation-v1.json) |
| **le contrat du bloc** | [`docs/implantation/bloc-linguistique.md`](../implantation/bloc-linguistique.md) |
| **le rejeu du 16/11 (rôles normalisés, candidats objets, durée)** | [`reports/rapport-exemples-v2.md`](../../reports/rapport-exemples-v2.md) |
| **le rejeu des cinq blocs du 14/11 (historique)** | [`reports/rapport-exemples-rejoues.md`](../../reports/rapport-exemples-rejoues.md) |
| **les trois exemples `--tagger` et les deux `--reel`** | [`reports/rapport-exemples-tagger.md`](../../reports/rapport-exemples-tagger.md) · [JSON](../../reports/rapport-exemples-tagger.json) |
| **le tagger, son coût et son contrôle négatif** | [`reports/rapport-tagger-option.md`](../../reports/rapport-tagger-option.md) |
| **la base honnête (`--reel`)** | [`reports/rapport-base-reelle.md`](../../reports/rapport-base-reelle.md) |
| **les chiffres courants** | [convention GV](../../reports/rapport-convention-gv.md) · [`s065`](../../reports/rapport-s065.md) · [`r035`](../../reports/rapport-r035.md) |
| **les 17 spans de la v12 (instantané)** | [`reports/rapport-pensee-v12.md`](../../reports/rapport-pensee-v12.md) |
| **l'audit et les contrôles** | [`reports/rapport-audit-v10.md`](../../reports/rapport-audit-v10.md) |
| **le gold réel** | `tools/tests/linguistique/gold_reel.json` |
