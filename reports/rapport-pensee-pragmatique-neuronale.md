# B13 — la pragmatique neuronale : parfaite sur les 20 réelles (dev), sous le majoritaire sur les 160 synthétiques (test)

> **Ligne de roadmap** : **B13** (moteur de pensée) / **R0.7** (bloc linguistique) · **Date** : 2026-11-02 ·
> **Verdict** : ❌ **le tagger pragmatique 7B n'est pas qualifié** — sur les **160 synthétiques**
> (le test), l'acte est **0,6375** (heuristique **1,0**, **majoritaire 0,7556**), la négation
> **0,9625**, la modalité **0,9688**, le double sens **0,6062** (heuristique **0,8875**). Sur les
> **20 réelles** (le dev), il est **parfait** (1,0/1,0/0,95/0,9), mais c'est le dev : le prompt a
> été choisi sur elles. La cascade prend l'acte et le double sens du modèle et **dégrade** ; la
> **négation et la modalité** restent à l'heuristique (0,85 > 0,6). **L'heuristique garde la
> pragmatique.**
>
> **Dispositif** : [`qualifier_pragmatique.py`](../tools/tests/linguistique/qualifier_pragmatique.py) ;
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`NeuronalLLMPragmatique`) ; JSON
> [`pensee-gold-pragmatique.json`](pensee-gold-pragmatique.json).

## 1. Ce qui était mesuré

Le POS (cascade 0,9440), les syntagmes (tête 0,7606) et la cascade complète
(0,9415 / 0,7539 / acte 1,0) étaient qualifiés ; la pragmatique restait à l'heuristique
(acte **1,0**, négation **1,0**, modalité **0,9944**, double sens **0,8889**). Il fallait
mesurer un tagger neuronal de pragmatique — le dernier niveau du bloc.

## 2. Le dispositif

- **Tagger** : `NeuronalLLMPragmatique` — un prompt d'analyse pragmatique, une **grammaire
  GBNF** qui impose un objet `{acte, negation, modalite, double_sens}` (l'acte dans
  `assertion`/`question`/`exclamation`, trois booléens), un `llama-server` local en **CPU**.
- **Gold** : 180 phrases — **20 réelles** (14 fr, 6 en) et **160 synthétiques** (fr). Les 20
  réelles ont servi au choix du prompt (dev) ; les 160 synthétiques sont le **test**.
- **Trois lectures** : heuristique, neuronal seul, cascade `Cascade(heuristique, tagger)` —
  l'acte et le double sens passent au modèle (0,6 > 0,45), la négation et la modalité restent à
  l'heuristique (0,85 > 0,6).
- **Contrôles** : majoritaire (assertion, pas de négation/mod./double sens), hasard (acte
  uniforme, booléens à 0,5, graine 0), permutation des prédictions entre phrases.
- **Commande** :
  `python3 tools/tests/linguistique/qualifier_pragmatique.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-gold-pragmatique.json`.

## 3. Les résultats

| lecture | source | acte | négation | modalité | double sens |
|---|---|---:|---:|---:|---:|
| **heuristique** | 180 | **1,0000** | **1,0000** | **0,9944** | **0,8889** |
| neuronal | 180 | 0,6778 | 0,9667 | 0,9667 | 0,6389 |
| cascade | 180 | 0,6778 | 0,9944 | 0,9889 | 0,6389 |
| **heuristique** | 20 réelles | 1,0000 | 1,0000 | 0,9500 | 0,9000 |
| **neuronal** | 20 réelles | **1,0000** | **1,0000** | 0,9500 | 0,9000 |
| **neuronal** | 160 synth. | **0,6375** | 0,9625 | 0,9688 | **0,6062** |
| **cascade** | 160 synth. | 0,6375 | 0,9938 | 0,9938 | 0,6062 |

- **Le dev ment** : sur les 20 réelles, le modèle est **exactement** l'heuristique
  (1,0 / 1,0 / 0,95 / 0,9). Sur les 160 synthétiques, il tombe à **0,6375** d'acte, **0,6062**
  de double sens, et la négation/modalité à 0,9625/0,9688.
- **Sous le majoritaire** : l'acte du modèle (0,6778 sur 180, 0,6375 sur le test) est **sous**
  le contrôle majoritaire (0,7556) — toujours `assertion` fait mieux que le 7B. Le double sens
  (0,6389) est sous le majoritaire (0,9222) et sous l'heuristique (0,8889).
- **La cascade dégrade** : elle prend l'acte et le double sens du modèle (0,6778 / 0,6389) et
  garde la négation/modalité de l'heuristique (0,9944 / 0,9889). Le POS et les syntagmes de la
  cascade restent ceux de l'heuristique ; la fraction sémantique 0,6381 ne bouge pas.
- **La syntaxe du test** : les synthétiques sont parfois peu naturelles (« nous compte avec
  il ») ; l'heuristique, elle, lit la ponctuation (`?`, `!`) et fait 1,0 sur l'acte.

## 4. Les contrôles

| contrôle | acte | négation | modalité | double sens |
|---|---:|---:|---:|---:|
| **majoritaire** | **0,7556** | 0,8722 | 0,8833 | 0,9222 |
| hasard (graine 0) | 0,3389 | 0,5389 | 0,5000 | 0,4556 |
| permutation | 0,4444 | 0,8222 | 0,8111 | 0,6611 |
| **heuristique** | **1,0000** | **1,0000** | **0,9944** | **0,8889** |
| **neuronal** | 0,6778 | 0,9667 | 0,9667 | 0,6389 |

- Le modèle est **au-dessus** du hasard et de la permutation, mais **sous le majoritaire** sur
  l'acte (0,6778 < 0,7556) et sur le double sens (0,6389 < 0,9222). Ce n'est pas un problème de
  contrat : **0 refus**, 180 appels, JSON/grammaire valides.
- L'heuristique est à 1,0 sur l'acte et la négation : le neuronal n'ajoute rien ; il retire.

## 5. Le coût

- **180 appels**, **0 refus**, latence CPU moyenne **3,836 s**, médiane **3,843 s** ; passe
  complète **702,3 s** (~11,7 min).
- Pas de mesure GPU : les deux Quadro RTX 5000 sont réservées à N2.

## 6. Ce qui pourrait rendre ce résultat faux

- **Le dev/test** : les 20 réelles ont servi au choix du prompt ; leur 1,0 est **optimiste**.
  Le test (160 synthétiques) est le chiffre ; il est mauvais. Un prompt few-shot avec des
  exemples synthétiques pourrait améliorer, mais il **verrait** le test.
- **La syntaxe des synthétiques** : elle est parfois artificielle ; le 7B décroche, l'heuristique
  (ponctuation) non. Le test est dur, mais c'est le gold.
- **Le prompt** : trois actes (le gold n'a pas `ordre`) ; le premier prompt avec `ordre` a été
  corrigé avant la mesure. La version mesurée est celle du JSON.
- **Le double sens** : les ambiguïtés « prêt à manger » sont manquées ; le modèle ne les voit
  pas. C'est le point dur, et il est nommé.
- **La cascade** : la négation/modalité du modèle (0,6) perdent contre l'heuristique (0,85) ;
  l'acte/double sens du modèle (0,6) gagnent contre 0,45 et **dégradent**. La politique de
  confiance n'est pas la bonne pour la pragmatique : il faudrait **exclure** le modèle, pas le
  brancher.
- **Une seule graine**, CPU, température 0, grammaire.

## 7. La suite

1. **L'heuristique garde la pragmatique** : acte 1,0, négation 1,0, modalité 0,9944, double sens
   0,8889. Le composite de production reste **POS + syntagmes** (`NeuronalLLMCompose`), sans
   pragmatique neuronale.
2. **Le double sens** : un classifieur dédié (pas le tagger général) ou un prompt few-shot
   d'ambiguïtés ; à mesurer séparément.
3. **Le gold 200+ phrases réelles** : le dev de 20 est trop petit ; c'est la prochaine mesure
   de la ligne L.
4. **La porte B13** : six rouges S à traiter (T111, T113–T115, T132–T133) ; hors de ce fait.
5. **La porte qui bouge** (DRVM) : la politique LLM sur `LABYRINTHE_PORTE_MINUTE`/`STO`.

## 8. Fichiers

- [`tools/tests/linguistique/qualifier_pragmatique.py`](../tools/tests/linguistique/qualifier_pragmatique.py) —
  le banc (trois lectures, contrôles, JSON).
- [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) — `NeuronalLLMPragmatique`,
  `grammaire_pragma`, `ACTES`.
- [`tools/tests/linguistique/test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py) —
  le test du tagger (16 tests au total).
- [`pensee-gold-pragmatique.json`](pensee-gold-pragmatique.json) — les chiffres, les seuils, les
  limites.
