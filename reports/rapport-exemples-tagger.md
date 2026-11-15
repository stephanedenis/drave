# D1 — les exemples `--tagger` et `--reel` : le coût affiché, la base honnête, cinq blocs rejoués

> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **D1** · **Date** : 2026-11-15 ·
> **Verdict** : ✅
> **Cinq blocs ajoutés** à [`docs/produit/exemples.md`](../docs/produit/exemples.md) : **3** avec
> `--tagger` (la clé, le réseau, le **coût affiché**) et **2** avec `--reel` (la **base
> honnête**). Les trois exemples `--tagger` réparent **2 tokens sur 17** (14/17 → 16/17) ;
> **3 appels**, **441 tokens**, **3,7 s**. Les deux `--reel` donnent **452 phrases**, POS
> **0,8891**, F1 **0,7906**, attachement **183/184 = 0,9946**. Le code courant n'a pas bougé :
> F1 **0,7902**, attachement **238/238 labels** (**238/239 cibles**, 0,9958), schéma **v2**.
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) 0.1.0, clé
> `~/.config/drave/deepseek.key`, cache disque neuf (`DEEPSEEK_CACHE`), `jq`. **Contrôle
> négatif** : doc mutée (`lu/VERB` → `lu/NOUN`) détectée **4/5**, schéma v2 qui refuse une
> version 3. **JSON** : [`rapport-exemples-tagger.json`](rapport-exemples-tagger.json).

## 1. Ce qui a été ajouté

| bloc | cas | commande | ce que la sortie montre | coût |
|---|---|---|---|---|
| § 6.1 | `g001` — « Le chat dort. » | `analyser "…" --tagger` | POS **identique** à l'heuristique ; `PONCT` présent | 1 appel · 130 tokens · 1,1 s |
| § 6.2 | `g011` — « Le livre que j'ai lu… » | `analyser "…" --tagger` | `lu` **NOUN → VERB** ; `que` reste PRON | 1 appel · 157 tokens · 1,5 s |
| § 6.3 | `r241` — « The day when we left… » | `analyser "…" --langue en --tagger` | `when` **CONJ → PRON** (le gold attend PRON) | 1 appel · 154 tokens · 1,1 s |
| § 7.1 | la base honnête | `evaluer --reel` | 452 phrases, POS 0,8891, F1 0,7906 | 0 appel |
| § 7.2 | le contrat JSON | `evaluer --reel --json \| jq …` | `gold.phrases: 452`, `reel: null`, 184 cibles | 0 appel |

Les sorties complètes, les commandes et les commentaires sont dans la doc : c'est elle que ces
blocs servent. Ici : le chiffre, le dispositif, le contrôle et les limites.

## 2. Les trois exemples `--tagger`

| bloc | tokens du gold | heuristique | `--tagger` | ce qui change |
|---|---:|---:|---:|---|
| `g001` | 3 | 3/3 | **3/3** | rien |
| `g011` | 7 | 5/7 | **6/7** | `lu` NOUN → VERB |
| `r241` | 7 | 6/7 | **7/7** | `when` CONJ → PRON |
| **total** | **17** | **14/17 = 82,35 %** | **16/17 = 94,12 %** | **+2 tokens** |

**Le chiffre.** Sur les **17 tokens du gold** de ces trois phrases, le tagger en répare **2** et
n'en casse aucun. Le gain visible est donc **+2/17**, soit **+11,76 points** — un chiffre
d'**exemple**, pas une mesure : les trois phrases ont été choisies, et elles surévaluent le gain
réel. Les chiffres publiés sur les golds complets sont **0,9575 contre 0,8625** sur **612**
(**+9,5 pts**) et **0,9500 contre 0,8891** sur le **réel 452** (**+6,1 pts**) ; le gain est
surtout porté par le synthétique ([`rapport-tagger-option.md`](rapport-tagger-option.md)).

**Ce que le tagger change.** Lui seul remplace le **POS** ; les syntagmes, rôles, cibles et la
pragmatique restent à l'heuristique. Dans `g011`, `lu` redevient **VERB** (le gold l'attend) mais
`que` reste **PRON** (le gold attend `CONJ`) : le tagger ne répare pas tout. Dans `r241`, `when`
redevient **PRON** (le gold l'attend) alors que l'heuristique le donnait `CONJ`. La confiance des
POS neuronaux est **0,60** (le seuil de la cascade), `source` vaut `neuronal` et `meta.ouvert`
est **absent** : ce n'est pas une probabilité calibrée.

## 3. Le coût

| passage | appels | réseau | cache | tokens | latence |
|---|---:|---:|---:|---:|---:|
| `g001` | 1 | 1 | 0 | 130 | 1,1 s |
| `g011` | 1 | 1 | 0 | 157 | 1,5 s |
| `r241` | 1 | 1 | 0 | 154 | 1,1 s |
| **total** | **3** | **3** | **0** | **441** | **3,7 s** |

**Le prix.** Au prorata du chiffre publié (~**0,02 $** pour **612 phrases / 22 299 tokens** après
la suppression du tagger de syntagmes), **441 tokens** valent **~0,0004 $** : une **estimation**,
pas une facture. Le coût est dominé par l'**appel par phrase** ; le tagger de syntagmes, qui
coûtait un second appel sans contribuer, a été retiré (1 appel/phrase).

**Le cache.** Les trois sorties de la doc sont celles d'un **cache neuf** : c'est la seule façon
d'afficher un coût réel. Avec le cache du premier appel, la ligne devient
`réseau=0 · cache=1 · tokens=0 · latence=0.0 s` et l'annotation est **identique** : le cache
rejoue la réponse, il ne change pas le résultat.

## 4. Les deux exemples `--reel`

| lecture | phrases | tokens | cibles | POS | F1 | attachement |
|---|---:|---:|---:|---:|---:|---:|
| `evaluer --reel` (lisible) | 452 | 2 480 | 184 | **0,8891** | **0,7906** | **0,9946** |
| `evaluer --reel --json` (extrait) | 452 | 2 480 | 184 | 0,8891 | 0,7906 | 0,9946 |

**La base honnête.** Les **452** phrases sont `hand` + `reel` (20 + 432), **sans** les 160
synthétiques. Le POS réel (**88,91 %**) est **meilleur** que le global (**86,25 %**) : le
synthétique est plus difficile pour le POS et **tire la moyenne vers le bas**. La F1 est
quasi identique (**79,06** contre **79,02**) et l'attachement un peu plus bas (**99,46** contre
**99,58**, 183/184 contre 238/239). `reel: null` dans le JSON est **attendu** : `--reel` mesure
déjà la base réelle ; sans le drapeau, `reel` porte un objet calculé à côté du global. Le
contrôle négatif « cible exacte tirée au hasard » est à **0,00 %** : c'est le plancher.

## 5. La vérification contre le code courant

| invariant | valeur | où |
|---|---|---|
| F1 syntagmes (gold vivant 612) | **0,7902** (P 0,7860 / R 0,7944) | `evaluer --json` |
| attachement | **238/238 labels** · **238/239 cibles = 0,9958** | `evaluer --json` |
| POS (gold vivant) | **0,8625** (fermé 0,9373, ouvert 0,7918) | `evaluer --json` |
| POS (réel 452) | **0,8891** (fermé 0,9294, ouvert 0,8466) | `evaluer --reel` |
| F1 (réel 452) | **0,7906** (P 0,8128 / R 0,7695) | `evaluer --reel` |
| attachement (réel 452) | **183/184 = 0,9946** | `evaluer --reel` |
| schéma des annotations `--tagger` | **3/3 en v2** (`schema: drave.annotation`, `version: 2`) | les trois JSON |
| blocs ajoutés reproduits | **5/5** | comparateur de blocs |
| blocs existants (14/11) | **5/5** (non modifiés ; `g001`, `g011`, `r241`, refus, `r035` revérifiés) | [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md) |

**La méthode.** Un comparateur de session extrait les blocs ``` de la doc, rejoue les commandes
(`analyser --tagger`, `evaluer --reel`, `evaluer --reel --json`) et compare les **objets JSON**
ou les sorties lisibles, pas le texte brut. Pour les trois blocs `--tagger`, la ligne
`TAGGER API` est exclue de la comparaison : elle dépend du cache, pas de l'annotation. Le
rejeu est fait avec le cache du premier appel (aucun réseau), et les trois annotations sont
validées par `fastjsonschema` contre [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json)
(**3/3**). Le schéma v2 refuse une annotation dont `version` vaut 3 et une annotation sans
`refus` : le validateur ne dit pas seulement « oui ».

## 6. Contrôle négatif

| essai | résultat |
|---|---|
| doc réelle | **5/5** blocs reproduits |
| doc mutée : `lu/VERB` → `lu/NOUN` (bloc 6.2) | **4/5**, code 1 ; écart détecté `lu/NOUN` (doc) ≠ `lu/VERB` (CLI) |
| schéma v2, annotation réelle | **3/3** valides |
| schéma v2, `version: 3` | **refusé** (`version must be same as const 2`) |
| schéma v2, `refus` retiré | **refusé** (champ obligatoire absent) |
| cache chaud | `réseau=0 · cache=1 · tokens=0` ; annotation identique |

La mutation est un **drift d'un seul token** : si le comparateur recopiait la doc au lieu de
rejouer, il ne verrait rien. Il le voit. C'est le contrôle qui manque à un simple « ça a l'air
bon ».

## 7. Ce qui pourrait rendre ce rapport faux

1. **Le choix des exemples.** Trois phrases et **17 tokens** : `16/17` n'est pas une mesure. Le
   gain réel est **+6,1** sur le réel 452, pas **+11,76**.
2. **Le modèle et la date.** Les trois appels sont du **2026-11-15**, avec le modèle demandé
   `deepseek-chat` ; un changement de routage, de prompt ou de tarif déplace le coût et, à la
   marge, le POS.
3. **Le cache.** Un cache chaud rend `tokens=0` : le coût affiché n'est alors **pas** le coût de
   l'annotation. La doc le dit, mais une copie du bloc de coût sans cette phrase serait fausse.
4. **Le gold.** `g011` attend `que/CONJ` et `lu/VERB` ; `r241` attend `when/PRON`. Ce sont des
   **conventions** du gold : si elles changent, le compte 14/17 → 16/17 change sans que le code
   bouge.
5. **La base réelle.** Les 452 phrases ne sont **pas** un tirage aléatoire (20 `hand` + 432
   corpus) ; le « réel » reste un corpus annoté, avec ses conventions.
6. **Les deux exemples `--reel` ne sont pas indépendants.** Ils mesurent la **même** base : le
   second montre le contrat JSON, pas une seconde mesure.
7. **Le tagger est prompté en français.** Il étiquette l'anglais de `r241` correctement, mais la
   ventilation du gain par langue n'est pas faite ici ; ne pas conclure au gain anglais.

## 8. Fichiers

- [`docs/produit/exemples.md`](../docs/produit/exemples.md) — les **cinq nouveaux blocs** (§ 6 et
  § 7), l'en-tête « dix exemples », les deux bullets `TAGGER API`/`--reel` du § 0, et le § 8
  corrigé (le CLI expose le tagger API en option, pas un neuronal local).
- [`docs/produit/README.md`](../docs/produit/README.md) § 3.7 — recalé sur le code courant :
  20 étiquettes, `PONCT` restitué, **1 appel/phrase**, POS **0,9575** sur 612 (+9,5), **0,9500**
  sur le réel 452 (+6,1), **22 299 tokens** / **155 s** / **~0,02 $**.
- [`rapport-exemples-tagger.json`](rapport-exemples-tagger.json) — les sorties, les coûts, les
  mesures, la vérification et le contrôle négatif.
- [`rapport-tagger-option.md`](rapport-tagger-option.md) — le tagger, son coût de référence et
  ses 14 tests.
- [`rapport-base-reelle.md`](rapport-base-reelle.md) — la base honnête, 452 phrases.
- [`tools/drave.py`](../tools/drave.py) · [`bloc_linguistique.py`](../tools/bloc_linguistique.py) —
  le code rejoué.

**La suite.** La doc produit a maintenant un exemple par chemin : heuristique (5), tagger (3),
base réelle (2). La prochaine action du produit reste **trancher `g017`** (convention d'adverbe)
et étendre le gold réel.
