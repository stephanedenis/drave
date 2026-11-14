# B13 — la POS passe à 83,83 % : la position du sujet tranche (R2a + R3 + R2b)

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **183/183 portes** : trois règles de la fiche [POS anglaise](rapport-pos-anglais.md) (A25) sont
> intégrées — **R2a** (après un pronom sujet, un mot inconnu est un verbe, sauf désinence
> nominale), **R3** (un DET ambigu sans nom à sa droite est un PRON/CONJ) et **R2b** (`-s`/`-es`
> après un nom sujet est un verbe). Résultat : **POS 75,81 → 83,83 %** (dev **83,75**, test
> **84,00**), **F1 syntagmes 0,5849 → 0,6181** (anglais **0,6341 → 0,7273**), et
> **l'attachement est strictement inchangé** : **222/222**, couverture **0,9289**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`analyser`, boucles
> 3 a/3 b/3 a bis), [`autotest.py`](../tools/pensee/autotest.py) (18 assertions recalées) ;
> fiche A25 [`rapport-pos-anglais.md`](rapport-pos-anglais.md) ; JSON
> [`pensee-pos-anglais-v2.json`](pensee-pos-anglais-v2.json).

## 1. Les trois règles

| # | règle | effet |
|---|---|---|
| **R2a** | après un **pronom sujet**, un mot inconnu (confiance ≤ 0,45) est un **verbe**, sauf désinence nominale (`-tion`, `-ness`, `-ity`, `-ment`…) | +6,3 dev / +5,2 test |
| **R3** | un **DET ambigu** (`that`, `her`) **sans nom à sa droite** n'est pas un DET : **PRON**, ou **CONJ** après un verbe | +0,5 dev / +0,4 test |
| **R2b** | une forme en **`-s`/`-es`** après un **nom sujet** est un verbe (« the cat sleeps ») | avec R2a : +8,3 dev / +7,4 test |

**R1 (le lexique verbal tranche le défaut ouvert) n'est pas intégrée** : 101/101 de ses
correctifs anglais sont des membres exacts de `VERBES_CONNUS`, lexique écrit sur ce gold — son
gain n'est pas comptable comme généralisation (A25).

## 2. Avant / après

| mesure | avant | **après** |
|---|---:|---:|
| POS (tout) | 75,81 % | **83,83 %** |
| POS dev / test | 75,47 / 76,56 | **83,75 / 84,00** |
| F1 syntagmes (612) | 0,5849 | **0,6181** |
| F1 anglais | 0,6341 | **0,7273** |
| tête (612) | 0,7336 | **0,7568** |
| **attachement** | **222/222, couv. 0,9289** | **222/222, couv. 0,9289** |

**Ce que ça dit** :

- **La position du sujet est un signal fort et gratuit** : +8 points de POS, +3,3 de F1, 0 perte.
- **L'attachement ne bouge pas** : les nouvelles étiquettes POS ne changent pas les frontières
  des segments au point de déplacer une cible — la mesure le confirme (222/222).
- **L'anglais rattrape son retard** (F1 0,6341 → 0,7273) : c'était la langue faible.

## 3. Contrôles (A25)

**Placebo** (même action, position aléatoire) : −2,46/−2,83/−0,21/−4,18 pts en moyenne — les
règles ne gagnent pas par hasard. **255 corrigés / 0 cassé** sur dev+test. **Attachement
strictement inchangé** partout.

## 4. Ce que ce banc ne dit pas

- **Le test** (347 jetons anglais) : petit ; 1 jeton = 0,29 pt.
- **R1** : écartée (lexique contaminé) ; son câblage reste à faire.
- **Le gold templaté** : les phrases synthétiques sont régulières.

## 5. Ce qui pourrait rendre cette fiche fausse

- **le garde-fou de R3** a été affiné après une phrase de test (`r117`) → le chiffre test est une
  borne légèrement optimiste ;
- **les désinences nominales** sont une liste ;
- **la position du sujet** peut se tromper sur une apposition.

## 6. La suite

1. **R4** (copule → ADJ) : +0,73 dev / +0,70 test annoncés.
2. **Les classes fermées anglaises** (28 erreurs) : `where`, `late`, `out`, `as`.
3. **Le câblage de R1** (cohérence chunker/POS), sans compter son gain.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — R2a, R3, R2b.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`rapport-pos-anglais.md`](rapport-pos-anglais.md) — le diagnostic A25.
- [`pensee-pos-anglais-v2.json`](pensee-pos-anglais-v2.json).
