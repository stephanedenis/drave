# L'interface de la RSN — cinq verbes, six paradigmes, la substitution

> **Ce que ce document est.** Le **contrat** qui rend la RSN **substituable** : cinq verbes qui
> couvrent tous les paradigmes (le noyau formel, le flou, le probabiliste, la provenance, le TMS,
> l'argumentation), un **transport JSON** qui ne dépend d'aucun cadre, et des **adaptateurs** qui
> branchent chaque paradigme **derrière** l'interface. La théorie : [`rsn-3-niveaux.md`](rsn-3-niveaux.md) ;
> les comparables : [`rapport-rsn-comparables.md`](../../reports/rapport-rsn-comparables.md) ; le code :
> [`tools/rsn_interface.py`](../../tools/rsn_interface.py).

## Le principe : les verbes, pas les modèles

Un **paradigme** (Lean, PSL, ProbLog, RDF-star, un TMS, Dung) est une **implémentation** de la même
chose : quelqu'un qui **affirme**, **interroge**, **promeut**, **explique** et **contextualise**.
Si l'interface expose ces **cinq verbes**, n'importe quel paradigme peut se brancher **derrière**
elle — et le moteur de pensée n'a jamais besoin de savoir lequel il utilise.

**La règle de substitution** : un bloc est substituable s'il **accepte les cinq verbes** et **rend
les mêmes structures** (les mêmes champs, pas les mêmes valeurs). Le test le vérifie : deux
implémentations différentes passent **le même** test de conformité.

## Les cinq verbes

| verbe | entrée | sortie | ce que ça garantit |
|---|---|---|---|
| **`assert`** | une affirmation (corps + contexte) | un identifiant stable (`sha256` du canonique) | l'ajout est **idempotent** : deux fois la même → le même id |
| **`query`** | un terme (ou un id) | `{statut, degre, preuve, contexte}` | le **tri-état** est toujours rendu : `prouve`, `refute`, `inconnu` |
| **`promote`** | un id + une preuve | le nouveau statut | **seule** entrée dans le noyau : sans preuve, `refuse` |
| **`explain`** | un id | `{justification, provenance}` | toute réponse est **traçable** jusqu'à sa source |
| **`context`** | un id | `{texte, span, version, langue}` | **le contexte source ne se perd jamais** |

**Deux verbes de service** (facultatifs, pour les paradigmes qui en ont besoin) :

| verbe | entrée | sortie | pour quel paradigme |
|---|---|---|---|
| **`compose`** | des règles + des faits | des affirmations dérivées (avec degrés) | le flou (PSL, Zadeh) |
| **`replay`** | une trace | le même état | le TMS, la reproductibilité |

## Le transport (le JSON, pas le cadre)

**Chaque verbe rend et accepte du JSON** — aucun objet du paradigme ne traverse l'interface :

```json
{
  "schema": "drave.rsn", "version": 1,
  "affirmation": {
    "id": "sha256:…",
    "corps": {"type": "predication", "role": "agent", "forme": "Le chat", "cible": "dort"},
    "contexte": {"texte": "Le chat dort.", "span": [0, 7], "langue": "fr", "version": "heuristique-1"},
    "statut": "hypothese", "degre": 0.62,
    "provenance": {"operateur": "heuristique.predication", "source": "analyser"}
  }
}
```

**Les champs sont le contrat** : `corps` (canonique, sans flottant), `contexte` (le source),
`statut` (le tri-état), `degre` (le [0,1], **jamais dans le noyau**), `provenance` (la
justification). Un paradigme qui ne sait pas remplir `degre` met `null` — et le déclare.

## Les six adaptateurs (le catalogue)

| adaptateur | paradigme | ce qu'il implémente | ce qu'il déclare ne pas faire |
|---|---|---|---|
| **`RSNFormel`** | Lean/Coq, Prolog, Ł3 | `query` (tri-état + preuve), `promote` (la dérivation) | le flou, la composition |
| **`RSNFlou`** | PSL, Zadeh | `query` (le degré), `compose` (les règles) | la preuve formelle |
| **`RSNProbabiliste`** | ProbLog, MLN | `query` (la probabilité), `compose` | le tri-état strict |
| **`RSNProvenance`** | RDF-star, PROV-O | `context`, `explain` (la provenance) | l'inférence |
| **`RSNTMS`** | Doyle, de Kleer | `assert`, `explain` (la justification), `replay` | le flou |
| **`RSNDung`** | Dung 1995 | `query` (l'acceptabilité), `promote` (l'extension) | les degrés |

**Deux adaptateurs peuvent se composer** : un `RSNFlou` + un `RSNProvenance` donnent une RSN
floue **traçable** — c'est la RSN que Drave veut, et elle se construit **par branchement**, pas par
réécriture.

## Le test de conformité (la substitutabilité, mesurée)

Un **seul** test, lancé sur **chaque** adaptateur :

1. `assert` deux fois la même affirmation → **le même id** ;
2. `query` une affirmation absente → **`inconnu`** (jamais `refute` par défaut) ;
3. `promote` **sans** preuve → **`refuse`** ;
4. `explain` → la provenance **complète** jusqu'à la source ;
5. `context` → le texte et le span **exacts**.

**Le critère** : un adaptateur qui passe les 5 tests est **substituable**. Le moteur de pensée ne
change pas d'une ligne quand on remplace l'un par l'autre.

## Ce que ça garantit, et ce que ça ne garantit pas

**Garantit** : la **modularité** (l'interface est stable, les paradigmes sont des blocs), la
**substitution** (le test de conformité), la **traçabilité** (`explain` et `context` sont
obligatoires), et la **non-régression** (les 5 tests sont dans `tools/tests/`).

**Ne garantit pas** : la **qualité** d'un paradigme (un adaptateur conforme peut être médiocre), la
**performance** (l'interface est un contrat, pas un optimiseur), et la **couverture** (les six
adaptateurs sont des **squelettes** : le `RSNFormel` et le `RSNFlou` sont les premiers à écrire).

## L'état et le chemin

| pièce | état |
|---|---|
| l'interface (les 5 verbes + le JSON) | **ce document** |
| le test de conformité | **à écrire** (le premier test de substitution) |
| `RSNFlou` (le degré, la composition) | **à écrire** — c'est la RSN utile pour Drave |
| `RSNProvenance` (le contexte, l'explain) | **à écrire** — il complète le flou |
| `RSNFormel` (le tri-état, la preuve) | **à écrire** — le noyau minimal |

**Le chemin** : écrire le test de conformité **d'abord** (il définit le contrat), puis le couple
**`RSNFlou` + `RSNProvenance`** (la RSN de Drave), puis `RSNFormel` (le noyau), et enfin les
adaptateurs « lourds » (PSL, ProbLog, Dung) **si** le besoin est mesuré.
