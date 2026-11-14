# J11.2 — la mesure par langue : l'anglais devant, mais le gold n'est pas le même

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Tâche** : **J11.2** ·
> **Date** : 2026-11-14 · **Verdict** : ✅
> **Le chiffre.** `evaluer --par-langue` scinde la mesure du gold vivant 612 en **fr** et **en**
> sans changer le global (F1 **0,7902**, POS **0,8625**, attachement **238/239**). Le français
> fait **402 phrases / 2 031 tokens / 151 cibles** (POS **0,8159**, F1 **0,7475**, attachement
> **151/151**) ; l'anglais **210 phrases / 1 148 tokens / 88 cibles** (POS **0,9451**, F1
> **0,8656**, attachement **87/88**). L'anglais est devant, mais les deux golds **n'ont pas la
> même composition** : l'anglais est **100 % réel**, le français ajoute **160 synthétiques**.
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) (`evaluer --par-langue`, 0.1.0),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`test_produit.py`](../tools/tests/test_produit.py) (18 tests) ; gold vivant 612 phrases.
> **JSON** : [`evaluer-langue.json`](evaluer-langue.json).

## 1. Le détail fr/en

Le drapeau rejoue `evaluer_bloc` sur chaque sous-gold, avec le **même** bloc heuristique. Le
contrôle négatif est recalculé par langue : l'univers des cibles change avec la langue.

| langue | phrases | tokens | POS | fermé | ouvert | F1 syntagmes | tête F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **fr** | 402 | 2 031 | **0,8159** | 0,9092 | 0,7325 | **0,7475** | 0,8733 |
| **en** | 210 | 1 148 | **0,9451** | 0,9830 | 0,9054 | **0,8656** | 0,9527 |
| tout | 612 | 3 179 | 0,8625 | 0,9373 | 0,7918 | 0,7902 | 0,9029 |

| langue | cibles | labels | exact (rendement) | exact / spans | top-k | contrôle négatif |
|---|---:|---:|---:|---:|---:|---:|
| **fr** | 151 | 151 | **151/151 (1,0000)** | **1,0000** | 149/151 (0,9868) | 1,99 % |
| **en** | 88 | 87 | **87/88 (0,9886)** | **1,0000** | 87/88 (0,9886) | 2,27 % |
| tout | 239 | 238 | 238/239 (0,9958) | 1,0000 | 236/239 (0,9874) | 1,67 % |

**Ce que ça dit.** L'attachement n'est pas le trou : sur les spans prédits, il est **exact dans
les deux langues** (151/151 et 87/87). La seule cible sans span est **`g017`** côté anglais :
c'est la convention rejetée, pas une erreur d'attachement. Le français est **parfait en
couverture** (151/151) et l'anglais à **87/88** ; le top-k est à **0,9868 / 0,9886**.

**Ce que le détail ne dit pas.** Le français et l'anglais **ne sont pas comparables tels quels** :
la POS et le F1 mesurent des golds de tailles, de sources et de domaines différents. Les chiffres
par langue ne sont pas une note de « qualité linguistique » ; ils décrivent ce gold-ci.

## 2. Le confondant de composition

L'anglais du gold vivant est **entièrement réel** : 6 phrases `hand` + 204 `reel`. Le français
ajoute **160 phrases synthétiques** (lexique disjoint), qui sont les plus dures. La décomposition
par source le montre :

| source | langue | phrases | POS | F1 | attachement exact | couverture |
|---|---|---:|---:|---:|---:|---:|
| `hand` | fr | 14 | 0,8378 | 0,8889 | 1,0000 | 1,0000 |
| `hand` | en | 6 | 1,0000 | 0,9375 | 0,6667 | 0,6667 |
| `reel` | fr | 228 | 0,8410 | 0,7158 | 1,0000 | 1,0000 |
| `reel` | en | 204 | 0,9436 | 0,8638 | 1,0000 | 1,0000 |
| `synthetique` | fr | 160 | 0,7682 | 0,7888 | 1,0000 | 1,0000 |
| **`hand` + `reel`** | **fr** | **242** | **0,8408** | **0,7258** | **1,0000** | **1,0000** |
| **`hand` + `reel`** | **en** | **210** | **0,9451** | **0,8656** | **0,9886** | **0,9886** |

**Lecture.** Sur le **gold réel seul**, l'anglais reste devant (POS **0,9451** contre **0,8408** ;
F1 **0,8656** contre **0,7258**). Le synthétique n'est donc **pas la seule cause** de l'écart.
Mais la composition reste un **confondant** : les deux corpus réels n'ont ni les mêmes phrases,
ni les mêmes domaines, ni la même densité de syntagmes. Le `hand` anglais ne fait que **6
phrases** : son 0,6667 d'attachement (2/3 cibles) est un échantillon, pas un effet de langue.

**Ce qu'il faudrait pour trancher.** Un gold **apparié par source et par longueur** (mêmes
proportions de `hand`, `reel`, synthétique dans les deux langues). Tant qu'il n'existe pas, la
bonne lecture est : « sur ce gold, l'anglais rend mieux », pas « l'anglais est plus facile ».

## 3. Contrôle négatif et non-régression

- **Plancher aléatoire.** Une cible exacte tirée au hasard dans les cibles de la langue donne
  **1,67 %** (239 cibles), **1,99 %** (151, fr) et **2,27 %** (88, en), graine 0. Le modèle est
  **très au-dessus** du plancher ; le plancher n'est pas une mesure de qualité.
- **Non-régression.** Le test compare `evaluer --json` et `evaluer --par-langue --json` : la clé
  `heuristique` est **identique**. Le drapeau **ajoute** un détail, il ne change pas la mesure.
- **Cohérence interne.** Le test vérifie que `par_langue[langue].attachement.{cibles,exact}`
  coïncide avec `heuristique.attachement.par_langue[langue]` du rapport global, et que la somme
  des phrases par langue fait bien **612**.
- **Suite.** `python3 tools/tests/test_produit.py` → **18 tests, OK** (dont 2 pour ce drapeau).

## 4. Ce qui pourrait rendre cette fiche fausse

- **mesure in-sample** : les règles ont été dessinées sur ce gold ; les chiffres par langue
  héritent de ce biais ;
- **composition des golds** : l'anglais est 100 % réel, le français a 160 synthétiques ; même
  sur le réel seul, les corpus diffèrent ;
- **petit échantillon anglais** : **88 cibles**, **6 phrases `hand`** ; les taux anglais sont
  fragiles, surtout `hand` ;
- **`g017`** : une cible anglaise sans span prédit ; le 0,9886 d'exact est un **rendement**
  (87/88), pas une erreur d'attachement (87/87 sur les spans) ;
- **la langue vient du gold**, pas d'une détection ; une phrase mal étiquetée changerait le
  sous-gold ;
- **le F1 par langue** compare des inventaires de segments différents : ce n'est pas un F1
  « toutes choses égales ».

## 5. La suite

1. **J11.3** — re-mesurer les 50 textes libres avec le code de la semaine.
2. **J11.4** — documenter le schéma v2 (rétro-compatibilité v1) dans `docs/produit/README.md`.
3. **Trancher `g017`** — la seule cible sans span.
4. **Un gold apparié par langue** si l'on veut une comparaison de langues, et non de golds.

## 6. Fichiers

- [`tools/drave.py`](../tools/drave.py) — `evaluer --par-langue` (texte et `--json`).
- [`tools/tests/test_produit.py`](../tools/tests/test_produit.py) — `TestParLangue`, 18 tests.
- [`evaluer-langue.json`](evaluer-langue.json) — les deux langues, les sources, les contrôles.
- [`docs/produit/README.md`](../docs/produit/README.md) — § 3.3 et § 7 (option documentée).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — la mesure par bloc.
