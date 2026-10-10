> Campagne : **toutes-langues** · expérience **61**
> Titre : 61. Le défaut est LOCALISÉ et QUANTIFIÉ : notre sortie porte douze fois moins d'énergie de CONTENU
> Date réelle : **2026-10-06 20:58 HAE** (source : commit `09b0218`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 61. Le défaut est LOCALISÉ et QUANTIFIÉ : notre sortie porte douze fois moins d'énergie de CONTENU

Après quatre causes écartées (§58 à §60), restait à localiser le défaut. Ni une
similarité cosinus ni une comparaison à une cible mouvante ne le pouvaient. Une
**décomposition de variance** le peut, et elle est exacte et additive.

Pour chaque entrée (langue `L`, contenu `k`), on prend sa moyenne `m_Lk` et on
décompose :

```
ν_L  = moyenne sur les contenus   -> effet LANGUE
μ_k  = moyenne sur les langues    -> effet CONTENU
P_lang = Σ_L n_L ‖ν_L − m̄‖²      énergie portée par la LANGUE
P_cont = Σ_k n_k ‖μ_k − m̄‖²      énergie portée par le CONTENU
```

### 61.1 Le résultat

| panel | | P_lang | **P_cont** | **rapport P_cont/P_lang** |
|---|---|---:|---:|---:|
| **TEST** (langues inconnues) | **NOTRE** | 232,0 | **338,7** | **1,46** |
| | professeur | 399,2 | **4 356,4** | **10,91** |
| **APPRENTISSAGE** (langues connues) | **NOTRE** | 1 834,7 | **493,9** | **0,27** |
| | professeur | 2 405,1 | **5 219,9** | **2,17** |

### 61.2 Ce que cela dit, et c'est net

**1. Le professeur porte 10,9 fois plus d'énergie de contenu que de langue** (test).
Notre sortie n'en porte que **1,46 fois**.

**2. Le défaut n'est PAS « trop de langue ».** Notre énergie de langue (232) est du même
ordre que celle du professeur (399). **C'est notre énergie de CONTENU qui est
dérisoire : 338,7 contre 4 356,4 — douze fois moins.**

**3. Le même écart existe sur les langues d'apprentissage** (493,9 contre 5 219,9, onze
fois moins), donc **ce n'est pas un défaut de transfert** : c'est un défaut de
reproduction, présent partout.

**4. Et cela explique — enfin — le §60.1.** Le rapport
`‖écart à la moyenne‖ / ‖moyenne‖` valait 0,291 chez nous contre 2,145 chez le
professeur : l'écart à la moyenne, c'est précisément la part qui porte le contenu. Le
rétrécissement du §60 et la décomposition du §61 mesurent **la même chose par deux
chemins indépendants**, et ils concordent.

**5. La cause de l'inversion contenu/langue est donc identifiée** : ce n'est pas un
excès de structure linguistique, c'est une **famine de structure de contenu**. Le
moindres carrés, forcé de choisir entre reproduire la masse commune (qui domine
l'énergie) et les écarts de contenu (petits devant elle), sous-produit massivement les
seconds.

### 61.3 Ce que cela rouvre, et ce que cela ferme

**Cela ferme** la piste du §59 d'une autre façon : ce n'est pas la *pondération* des
petites composantes qui manquait, c'est leur **amplitude** — elles ne sont pas
seulement sous-pondérées dans l'objectif, elles sont **sous-produites dans la sortie**.

**Cela rouvre** le §58 sous un jour favorable : le terme `−μ_cont·P_cont` **compense
exactement cette famine** — il demande à la sortie de porter plus d'énergie de contenu.
Ce n'était donc pas un artefact : c'était le bon remède appliqué par un moyen
non convexe.

**Et cela désigne un remède CONVEXE qui n'a pas été essayé** : amplifier la sortie
**le long de l'axe du contenu seulement** — et non globalement comme au §60.2, où
l'amplification uniforme augmentait les deux axes et ne rétablissait donc pas leur
rapport.

### 61.4 Pourquoi cette mesure est meilleure que les précédentes

`P_cont/P_lang` **ne dépend pas de quelles langues composent le panel** — seulement de
leur nombre et de leur diversité. Le §60.3 avait montré que la similarité du
professeur, elle, **changeait de signe** entre les langues d'apprentissage (−0,0152) et
celles de test (+0,0517), ce qui rendait la « cible » mouvante. La décomposition, elle,
donne 10,91 et 2,17 — deux valeurs différentes, mais **du même côté, et interprétables
directement** : le contenu domine la langue dans les deux cas.


---
