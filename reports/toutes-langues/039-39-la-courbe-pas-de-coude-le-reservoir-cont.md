> Campagne : **toutes-langues** · expérience **39**
> Titre : 39. La courbe : pas de coude, le réservoir continue de payer
> Date réelle : **2026-10-06 12:17 HAE** (source : commit `d15c870`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 39. La courbe : pas de coude, le réservoir continue de payer

Le §34 avait mesuré une pente en deux points et demandé **la courbe**. La voici —
même vivier, 896 canaux, ride 0,03, fit sur 1/5 des lignes (§35.5, coût 0,0045) :

| neurones | A seul | A + entrée linéaire | apport sur `C_lin` | caractéristiques |
|---:|---:|---:|---:|---:|
| 40 | 0,5972 | 0,6609 (entrée quad.) | +0,0073 | 1 872 |
| **200** | 0,6218 | 0,6693 | **+0,0329** | 1 296 |
| **400** | 0,6333 | 0,6763 | **+0,0399** | 1 696 |
| **800** | **0,6421** | **0,6821** | **+0,0457** | 2 496 |

**Aucun coude.** L'apport du réservoir par-dessus l'entrée croît de façon monotone :
+0,0329 → +0,0399 → +0,0457 en doublant deux fois. Il est **sub-linéaire** (le
doublement rapporte de moins en moins : +0,0070 puis +0,0058) mais il ne plafonne
pas.

Et le point décisif reste vrai à chaque taille : **A800 + entrée (2 496
caractéristiques) fait 0,6821, contre 0,6536 pour `C_quad` (1 792 caractéristiques,
entrée seule quadratique)**. Le réservoir n'est pas un substitut à de la capacité
d'entrée : il porte une information que l'expansion instantanée de l'entrée ne
contient pas.

**Meilleur résultat de la session : fidélité TEST 0,6821, 800 neurones, 1 couche.**

### 39.1 Ce que cela dit de la croissance

La mission repose sur la **croissance** par corrélation, sans rétropropagation. Cette
courbe la valide : ajouter des neurones achète du transfert, régulièrement. Si l'on
veut +0,06, il faut de l'ordre de 2 000 à 3 000 neurones — c'est un budget, pas un
obstacle de principe.

### 39.2 Le point de méthode

La fidélité de `A200 + entrée` vaut 0,6738 avec **toutes** les lignes et 0,6693 avec
une sur cinq : le sous-échantillonnage coûte bien les 0,0045 annoncés, ni plus ni
moins. La prévision du §35.5 se vérifie donc sur un second cas.

---
