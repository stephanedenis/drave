> Campagne : **toutes-langues** · expérience **34**
> Titre : 34. Correction du §29 : le réservoir n'était pas inutile, il était TROP PETIT
> Date réelle : **2026-10-06 10:40 HAE** (source : commit `c660fde`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 34. Correction du §29 : le réservoir n'était pas inutile, il était TROP PETIT

Le §29 concluait que « 40 neurones récurrents valent +0,007 : le pont est pour
l'essentiel une sonde sur l'entrée ». La mesure qui manquait — un réservoir large
avec accès à l'entrée — **renverse cette conclusion**.

### 34.1 Le tableau complet, même vivier, même périmètre

351 langues d'apprentissage · 41 de test · 896 canaux · entrée centrée par langue.

| configuration | caractéristiques | fidélité TEST | apport vs constante |
|---|---:|---:|---:|
| témoin constant | 0 | 0,5678 | — |
| A40 · réservoir | 80 | 0,5972 | +0,0294 |
| A200 · réservoir | 400 | 0,6218 | +0,0540 |
| C_lin · entrée seule, linéaire | 896 | 0,6364 | +0,0686 |
| C_quad · entrée seule, quadratique | 1 792 | 0,6536 | +0,0857 |
| A40 + entrée quadratique | 1 872 | 0,6609 | +0,0931 |
| **A200 + entrée LINÉAIRE** | **1 296** | **0,6738** | **+0,1059** |

### 34.2 Ce n'est pas de la capacité

**A200 + entrée (1 296 caractéristiques) bat C_quad (1 792) et A40 + entrée (1 872)
avec MOINS de colonnes.** L'objection du §31 — « l'entrée gagne peut-être par
capacité » — est donc levée dans l'autre sens : **les 400 états récurrents portent
une information que l'expansion quadratique instantanée de l'entrée ne contient
pas.**

La différence est qualitative et nommable : `C_quad` ne voit que le **jeton
courant** `e_t` et son carré. Le réservoir voit `e_t` **et l'histoire** de la
séquence, à travers sa récurrence. Ce qu'il ajoute, c'est de la **mémoire
non linéaire**.

### 34.3 L'apport marginal croît avec la taille — il ne plafonne pas

| | apport du réservoir par-dessus l'entrée |
|---|---:|
| 40 neurones (+ entrée quadratique) | +0,0073 |
| **200 neurones (+ entrée linéaire)** | **+0,0374** |

Multiplier la taille par 5 multiplie l'apport marginal par 5. **Ce n'est pas une
saturation, c'est une pente.** Le §29 avait mesuré un point et conclu une tendance —
c'était l'erreur.

### 34.4 Ce qui reste vrai du §29

Le §29 n'était pas faux, il était **incomplet** : à 40 neurones, sur ce périmètre,
le réservoir vaut effectivement +0,007. Ce qui tombe, c'est la généralisation que
j'en avais tirée. Et le §29.4 (la profondeur n'achète rien) n'est pas touché : D
(2 couches de 20) = 0,5979 contre A (1 couche de 40) = 0,5972.

### 34.5 La suite, écrite avant d'être faite

Si l'apport croît avec la taille, il faut **la courbe**, pas un point : 400, 800
neurones, avec la même entrée linéaire. Deux questions précises :

1. **Où est le coude ?** Si +0,037 à 200 devient +0,06 à 800, l'architecture est la
   bonne et le problème est un budget de neurones. Si l'apport plafonne vers 200,
   c'est la **forme** de la récurrence qu'il faut revoir.
2. **Le réservoir aléatoire gelé est-il le bon ?** Les poids `P` et `B` sont tirés
   au hasard et ne changent jamais — seul le readout est ajusté. C'est ce qui rend
   le pont si peu coûteux, et c'est peut-être ce qui le limite.


---
