> Campagne : **toutes-langues** · expérience **95**
> Titre : 95. LA PORTÉE DU CONTEXTE : le voisin immédiat porte presque tout
> Date réelle : **2026-10-07 14:03 HAE** (source : commit `84160d1`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 95. LA PORTÉE DU CONTEXTE : le voisin immédiat porte presque tout

### 95.1 Le montage

Le §89 mesurait ce qu'une **fenêtre de trois jetons** ajoute. Il ne disait pas **à quelle
distance** le passé cesse de porter. Mêmes 300 traces, mêmes 164 775 positions ; on ajuste
un modèle `{jeton courant, jeton à la distance d}` pour `d = 1, 2, 4, 8, 16, 32`.

| couche | d=1 | d=2 | d=4 | d=8 | d=16 | d=32 | **jeton seul** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **3** | 0,5005 | 0,4507 | 0,4313 | 0,4238 | 0,4238 | 0,4242 | **0,4139** |
| **8** | 0,3040 | 0,2803 | 0,2633 | 0,2541 | 0,2524 | 0,2521 | **0,2424** |

Gain au-dessus du jeton seul :

| couche | d=1 | d=2 | d=4 | d=8 | d=16 | d=32 |
|---|---:|---:|---:|---:|---:|---:|
| 3 | **+0,0866** | +0,0368 | +0,0174 | +0,0099 | +0,0099 | +0,0103 |
| 8 | **+0,0616** | +0,0379 | +0,0209 | +0,0117 | +0,0100 | +0,0097 |

### 95.2 Le fait : le gain est divisé par deux à chaque doublement de distance

**Le jeton immédiatement précédent porte à lui seul les deux tiers du gain contextuel**
(+0,087 sur +0,108 pour la fenêtre de trois, à la couche 3). Ensuite chaque doublement de
distance **divise le gain par deux environ** : +0,037 à d=2, +0,017 à d=4, +0,010 à d=8 —
puis un **plancher** de +0,010 qui ne bouge plus jusqu'à d=32.

**Conséquence pour la conception, et elle est nette** : ce qui compte est **le voisinage
immédiat**. Un mécanisme récurrent dont l'état résume surtout les derniers jetons capte
l'essentiel de ce qu'une lecture linéaire peut tirer du contexte. **Chercher un contexte
long n'est pas la priorité** ; c'est le premier pas qui porte.

### 95.3 Réserves, et elles sont de taille

**1. Le plancher de +0,010 est peut-être un artefact de capacité.** Le modèle à deux blocs a
1 792 variables contre 896 pour le témoin, et un R² calculé sur les données d'ajustement est
toujours un peu gonflé par la capacité supplémentaire. Le §89.4 a déjà montré combien ce
gonflement peut être grand quand le rapport variables/points se dégrade. **Un plancher
constant en d est exactement la signature attendue d'un tel artefact.**

**2. Un jeton lointain isolé n'est pas le contexte.** Cette mesure dit qu'*un seul* jeton
pris à 32 positions n'ajoute presque rien. Elle ne dit **pas** que la totalité du préfixe
n'ajoute rien — une information répartie sur tout le contexte serait invisible ici.

**3. La colonne « jeton seul » du premier tableau a été corrigée après coup.** La première
version du bloc de portée accumulait `E(k)ᵀ Y(k+d)` — le jeton d'il y a `d` pas, et non le
jeton aligné sur la cible. Elle affichait **0,0054** là où la même quantité vaut **0,4139**.
Les colonnes `d = 1…32`, elles, étaient justes : le défaut ne portait que sur le témoin.
Les valeurs de la colonne « jeton seul » ci-dessus viennent du tableau principal du §89,
calculé sur les mêmes traces avec le bon alignement.
