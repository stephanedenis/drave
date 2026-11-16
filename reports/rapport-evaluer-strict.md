# V1 — `evaluer --strict` : les quatre modes locaux, la cascade à 86,25 % / 88,91 %, le plancher 0,70 qui mord

> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **V1** (la suite du bilan T6) ·
> **Date** : 2026-11-16 · **Verdict** : ✅ **la cascade locale passe le plancher 0,70 sur les
> deux golds** — POS **0,8625** sur 612, **0,8891** sur le réel 452 — et le **contrôle négatif**
> échoue comme il doit : une cascade dégradée tombe à **0,0000** et rend **code 1**. Le CLI
> affiche désormais les **quatre modes** (heuristique, neuronal, parallèle, cascade) et leur
> **delta** contre l'heuristique, sans réseau ni GPU.
>
> **Le chiffre, en une ligne.** `drave evaluer --strict` mesure **612** et **452** phrases,
> quatre modes, et sort en **0** : cascade POS **86,25 %** (612) et **88,91 %** (452), soit
> **+16,25** et **+18,91 points** au-dessus du plancher ; le neuronal local est **en dessous**
> de l'heuristique (**−10,85** et **−12,70 points**), et le parallèle comme la cascade sont
> **identiques à l'heuristique** (delta **0,00**).
>
> **Dispositif** : [`tools/tests/test_evaluer_strict.py`](../tools/tests/test_evaluer_strict.py)
> (5 tests) · [`reports/evaluer-strict.json`](evaluer-strict.json) · `tools/drave.py`
> (`--strict`, `_evaluer_strict`) · [`docs/produit/README.md`](../docs/produit/README.md) § 3.3.

## 1. Ce que le CLI ne faisait pas

Le banc de recherche [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) mesure
**quatre modes** — heuristique, `MockNeuronal`, `Parallele`, `Cascade` — et applique un
**plancher 0,70** au POS du gold réel (`verdict.pos_reel`). Le CLI, lui, ne mesurait que
l'heuristique : `drave evaluer` rendait POS, syntagmes, attachement et pragmatique, puis
**sortait 0 sans jamais tester la cascade**. Le mode `--strict` comble cet écart : il rejoue
le banc local dans le produit et transforme le plancher en **code de sortie**.

## 2. Le dispositif

- **Gold vivant 612** : `hand` 20 + `reel` 432 + `synthetique` 160 ; **3 179 tokens**.
- **Gold réel 452** : `hand` 20 + `reel` 432, sans les 160 synthétiques ; **2 480 tokens**.
- **Neuronal** : `bl.MockNeuronal` — le neuronal **de contrat**, déterministe, hors ligne,
  sans GPU (règle 11). Ce n'est **pas** un modèle de qualité.
- **Quatre modes** : `Heuristique()`, `MockNeuronal()`, `Parallele([h, n])`,
  `Cascade(h, n)` (seuil 0,6, politique de fusion par défaut).
- **Mesure** : `evaluer_bloc` du banc, sur le **même** gold et le **même** évaluateur ; POS
  exact (token), syntagmes F1, tête F1, acte, fraction, attachement. Le JSON porte le détail.
- **Plancher** : **0,70** sur l'**exactitude POS de la cascade**, séparément sur 612 et sur
  452. Si l'un des deux est sous le plancher, `evaluer --strict` sort en **code 1**.
- **Contrôle négatif** : une cascade dont le niveau POS est forcé à `X` (tout le reste est
  conservé) est mesurée dans la même passe ; elle doit tomber sous 0,70 et porter `code 1`.

## 3. Les quatre modes

### 3.1 Gold vivant 612

| mode | POS | ΔPOS | syntagmes F1 | ΔF1 | tête F1 | Δtête | acte | attachement exact |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **heuristique** | **0,8625** | — | **0,7902** | — | **0,9029** | — | 0,9967 | 0,9958 |
| neuronal (`MockNeuronal`) | 0,7540 | −10,85 pts | 0,7651 | −2,51 pts | 0,8807 | −2,22 pts | 0,9967 | 0,0000 |
| parallèle | 0,8625 | +0,00 pt | 0,7902 | +0,00 pt | 0,9029 | +0,00 pt | 0,9967 | 0,9958 |
| **cascade** | **0,8625** | **+0,00 pt** | **0,7902** | **+0,00 pt** | **0,9029** | **+0,00 pt** | 0,9967 | 0,9958 |

La cascade appelle le neuronal **612 fois sur 612 phrases** — mais la fusion par défaut donne
la priorité à l'heuristique sur les niveaux qu'elle couvre : la sortie est **celle de
l'heuristique**, au label près. Le `MockNeuronal` ne dégrade donc pas la cascade ; il ne
l'améliore pas non plus.

### 3.2 Gold réel 452

| mode | POS | ΔPOS | syntagmes F1 | ΔF1 | tête F1 | Δtête | acte | attachement exact |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **heuristique** | **0,8891** | — | **0,7906** | — | **0,8990** | — | 0,9956 | 0,9946 |
| neuronal (`MockNeuronal`) | 0,7621 | −12,70 pts | 0,7448 | −4,58 pts | 0,8697 | −2,93 pts | 0,9956 | 0,0000 |
| parallèle | 0,8891 | +0,00 pt | 0,7906 | +0,00 pt | 0,8990 | +0,00 pt | 0,9956 | 0,9946 |
| **cascade** | **0,8891** | **+0,00 pt** | **0,7906** | **+0,00 pt** | **0,8990** | **+0,00 pt** | 0,9956 | 0,9946 |

Les 452 appels neuronaux ne changent pas les labels : la cascade réelle est **l'heuristique
avec un appel neuronal dominé**. C'est le fait que le mode strict publie, pas un gain caché.

## 4. Le plancher et le code de sortie

| gold | cascade POS | plancher | marge | verdict |
|---|---:|---:|---:|---|
| **vivant 612** | **0,8625** | 0,70 | **+16,25 pts** | ✅ |
| **réel 452** | **0,8891** | 0,70 | **+18,91 pts** | ✅ |

La commande sort **0** parce que les deux mesures passent. Le plancher n'est pas un
affichage : c'est la condition du code de retour, et le test vérifie qu'un verdict faux rend
**1** (injection d'un rapport `ok: false`, sans réseau).

## 5. Le contrôle négatif

La même passe mesure une **cascade dégradée** : le niveau POS est forcé à `X`, les syntagmes,
l'attachement et la pragmatique restent ceux de la cascade. Résultat :

| contrôle | POS | plancher | passe | code |
|---|---:|---:|---|---:|
| cascade dégradée, réel 452 | **0,0000** | 0,70 | ❌ | **1** |

C'est le contrôle qui compte : le plancher **mord** quand la cascade est sous 0,70. Le rapport
JSON le porte (`controle_negatif.ok: true`, `code: 1`) ; le test
`test_negative_control_code_1` vérifie en plus que `cmd_evaluer` rend **1** quand le verdict
est faux. Le contrôle est **grossier** (POS constant), et c'est sa limite : il prouve que le
seuil est branché, pas qu'il détecte une dégradation subtile.

## 6. Ce qui pourrait rendre ce résultat faux

- **Le neuronal est un mock** : `MockNeuronal` réimplémente l'heuristique sous un autre nom.
  Il prouve le contrat et le câblage, **pas** la qualité d'un modèle. Le plancher 0,70 est
  passé par la cascade parce que la cascade **est** l'heuristique ici.
- **La fusion domine le neuronal** : les 612 et 452 appels sont réels, mais la politique par
  défaut garde les labels de l'heuristique. Un autre `priorite_par_niveau` changerait le
  résultat ; ce n'est pas mesuré ici.
- **Le plancher ne porte que sur le POS** : F1 0,7902 / 0,7906 et tête 0,9029 / 0,8990 sont
  publiés, pas gardés. Une cascade qui perdrait 20 points de F1 pourrait encore passer.
- **Le gold est le gold de mise au point** : les règles de l'heuristique ont été dessinées
  sur ces phrases ; le 452 est la base honnête, pas un test indépendant.
- **Une seule passe, un seul jeu de réglages** (seuil de cascade 0,6, politique par défaut).
  Aucune variance, aucun intervalle.
- **Le contrôle négatif est volontairement grossier** : forcer le POS à `X` fait 0,0000 ;
  une dégradation de 5 points serait plus difficile à distinguer du plancher.
- **`--strict` est local et exclusif** : `--gold`, `--tagger` et `--par-langue` sortent en
  **5** ; le mode ne mesure ni le gold gelé, ni l'API, ni le détail par langue.

## 7. Les fichiers

- [`tools/drave.py`](../tools/drave.py) — `--strict`, `_modes_quatre`, `_evaluer_strict`,
  `_verdict_strict`, `_formater_strict`, `PLANCHER_STRICT = 0.70`.
- [`tools/tests/test_evaluer_strict.py`](../tools/tests/test_evaluer_strict.py) — **5 tests** :
  quatre modes et plancher, sortie lisible, contrôle négatif code 1, options exclusives,
  aide. Ajouté à [`tools/porte-produit.sh`](../tools/porte-produit.sh).
- [`reports/evaluer-strict.json`](evaluer-strict.json) — le rapport complet (modes 612 et 452,
  deltas, verdict, contrôle négatif).
- [`docs/produit/README.md`](../docs/produit/README.md) § 3.3 — la notice du mode strict.
