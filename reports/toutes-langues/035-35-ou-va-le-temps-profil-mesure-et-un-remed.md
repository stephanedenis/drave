> Campagne : **toutes-langues** · expérience **35**
> Titre : 35. Où va le temps — profil mesuré, et un remède gratuit
> Date réelle : **2026-10-06 11:25 HAE** (source : commit `8374ad4`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 35. Où va le temps — profil mesuré, et un remède gratuit

Question posée : le professeur ne devrait tourner qu'**une fois**, et l'apprentissage
par croissance devrait être quasi instantané sur cette machine. Où va le temps ?

### 35.1 Le pipeline, en quatre étapes, avec le coût MESURÉ de chacune

| étape | ce qu'elle fait | coût mesuré |
|---|---|---|
| **1. Passe professeur** (`drave --infer --trace-flux`) | fait tourner Qwen2.5-0.5B sur le texte et écrit la couche 0 et la couche cible à chaque position | **39,3 s par langue** → **392 langues = 4 h 17** |
| **2. Cache** (`cache_pont.py`) | lit les `.drvf` en `.npz` | 16 s |
| **3. Construction du réservoir** (`Pont.nait`) | boucle Python sur chaque pas de chaque langue (472 472 pas) | **24 µs/pas** → **0,4 min pour 40 neurones**, ~2 min pour 200, ~8 min pour 800 |
| **4. Trajectoires de test** (`recalcule`) | rejoue le réseau sur le test | ~5 s pour les 41 langues |
| **5. AJUSTEMENT DE LA LECTURE** (`ajuste`) | accumule la Gram `AᵀA` sur 472 472 lignes | **LE GOULOT — voir ci-dessous** |

**La construction du réservoir, que l'on soupçonnait, est l'étape la MOINS chère.**
0,4 minute pour 40 neurones sur 472 472 pas. C'est 24 µs par pas, dont l'essentiel
est de la surcharge d'interpréteur Python, pas du calcul.

### 35.2 Le vrai goulot : le fit de la lecture

La lecture est ajustée par moindres carrés ridgés. On accumule `AᵀA` où `A` a
`n_caractéristiques` colonnes et 472 472 lignes. Le coût est **O(lignes ×
caractéristiques²)**, et les caractéristiques valent `2 × neurones + 896` :

| neurones | caractéristiques | temps de fit mesuré |
|---:|---:|---:|
| 40 | 80 | quelques secondes |
| 200 | 1 296 | **~22 min** |
| 200 + entrée | 1 296 | ~22 min |
| 800 + entrée | 2 496 | **~80 min** |

C'est du calcul dense réel, pas de la surcharge. D'où la lenteur apparente : ce n'est
pas le modèle qui est lent, c'est **une régression sur un demi-million de lignes**.

### 35.3 Vous avez raison sur un point, et il a coûté 4 heures

**La passe professeur ne devrait avoir lieu qu'UNE fois.** Elle a eu lieu **deux
fois** : j'ai d'abord visé la couche 10, découvert que la couche 8 est le plateau
(§30), puis retracé les 392 langues. **4 h 17 perdues à cause de mon choix de cible.**

Et l'erreur est plus bête que ça : `--trace-couches` ne filtre que l'**écriture**. La
passe avant exécute les 24 couches de toute façon. Écrire 0, 4, 8, 10, 12 et 16 au
lieu de 0 et 10 n'aurait coûté **presque rien** et aurait rendu la question du
plateau réponseable sans aucune repasse. La convention actuelle écrit le minimum et
paie le maximum.

### 35.4 Votre intuition « millisecondes » : elle tient à moitié

**L'évaluation est rapide** : 41 langues de test, 76 812 pas, en ~5 s — soit 0,1 s
par langue. C'est la récurrence, séquentielle en `t`, à ~50 µs par pas. Pas des
millisecondes, mais pas lent non plus.

**Le fit, lui, ne peut pas être en millisecondes** : résoudre un système de 472 472
équations à 1 296 inconnues, sur 351 séquences, c'est ~1,7 TFLOP. À 1,2 TFLOP/s
effectif, cela fait 22 minutes. Le chiffre est cohérent avec le matériel.

### 35.5 Le remède gratuit, mesuré

Une régression sur 472 472 lignes est massivement sur-déterminée. J'ai mesuré ce que
coûte de n'en garder qu'une fraction (lecture linéaire sur l'entrée, 896 colonnes,
évaluation sur **tout** le test) :

| sous-échantillonnage | lignes | temps de fit | fidélité TEST |
|---|---:|---:|---:|
| 1/1 | 472 472 | 328,0 s | **0,6364** |
| 1/2 | 236 318 | 129,4 s | 0,6353 |
| **1/5** | **94 634** | **56,4 s** | **0,6319** |
| 1/10 | 47 395 | 29,5 s | 0,6265 |
| 1/20 | 23 790 | 14,9 s | 0,6161 |

**Garder une ligne sur cinq rend le fit 5,8× plus rapide et coûte 0,0045 de
fidélité** — 0,7 % en relatif. C'est le meilleur rapport temps/qualité disponible, et
il ne demande aucune approximation : c'est le même modèle, ajusté sur moins de
points.

*(Contrôle de cohérence : la valeur 1/1 vaut 0,6364, exactement le `C_lin` du §31.)*

### 35.6 Les remèdes, par ordre de gain

| remède | gain | coût |
|---|---|---|
| **Tracer TOUTES les couches utiles en UNE passe** | **4 h 17 économisées** | nul |
| **Sous-échantillonner le fit à 1/5** | **5,8×** | −0,0045 de fidélité |
| Gram en `float32` | ~2× | à mesurer |
| Mettre en cache les états du réservoir sur disque | exploration quasi gratuite | disque |
| Vectoriser le réservoir **sur les langues** (boucler sur `t`, pas sur les pas) | construction en secondes | réécriture |

Le dernier point mérite d'être dit clairement : la récurrence est séquentielle en `t`,
mais **les langues sont indépendantes**. La boucle actuelle est
`pour chaque langue : pour chaque pas`. L'inverse — `pour chaque pas : toutes les
langues d'un coup` — ferait passer 472 472 itérations Python à ~4 000, chacune sur un
tableau `(351, k)`. Ce n'est pas le goulot aujourd'hui, mais c'est un plancher de
24-275 µs par pas qu'on peut supprimer.


---
