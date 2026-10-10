> Campagne : **toutes-langues** · expérience **58**
> Titre : 58. Réécrire l'objectif : la structure du professeur EST atteignable, mais l'objectif à deux curseurs est NON CONVEXE
> Date réelle : **2026-10-06 20:05 HAE** (source : commit `c3de2df`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 58. Réécrire l'objectif : la structure du professeur EST atteignable, mais l'objectif à deux curseurs est NON CONVEXE

### 58.1 L'objectif, et pourquoi il tient en forme fermée

Le §57 a montré que l'invariance seule ne suffit pas : elle s'obtient aussi bien en
rapprochant les langues **à contenu égal** qu'en effaçant tout. On ajoute donc un
**second** terme, et l'objectif devient :

```
‖XW − Y‖²  +  μ_lang·P_lang(W)  −  μ_cont·P_cont(W)
```

- `P_lang` = variance **inter-langue** de la sortie (à minimiser) ;
- `P_cont` = variance **inter-contenu** de la sortie (à maximiser) ;
- les deux valent `tr(WᵀCW)`, donc la solution reste en **forme fermée**.

Et la mesure qui compte n'est plus l'invariance seule, mais la **SÉPARATION** :

```
séparation = S_langue − S_domaine
```

`S_langue` : même contenu, langues différentes — à garder. `S_domaine` : même langue,
contenus différents — à distinguer. **Positive = la sortie rapproche les langues PLUS
qu'elle n'efface les contenus.** C'est la définition mesurable d'un pont qui
fonctionne, et elle manquait à tous les chiffres du rapport.

### 58.2 Sur l'UDHR, la métrique est dégénérée — et on le voit

| μ_lang | μ_cont | fid TEST | S_langue | S_domaine | **séparation** | cible du prof |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0,5692 | 0,8824 | 0,9907 | −0,1083 | |
| 0,3 | 0,3 | 0,5563 | 0,9378 | 0,9936 | −0,0558 | |
| 3 | 3 | 0,5516 | 0,9594 | 0,9953 | −0,0359 | |
| | | | | | **cible** | **−0,2482** |

**Les curseurs éloignent de la cible.** Mais l'UDHR est le mauvais corpus pour cette
mesure : ses dix « contenus différents » sont **le même texte** (§53), donc son
`S_domaine` ne mesure rien. C'est le corpus Wikipedia qu'il faut interroger.

### 58.3 Sur Wikipedia : la cible est ATTEINTE — et c'est le résultat important

| μ_lang | μ_cont | fid TEST | S_langue | S_domaine | **séparation** | vs professeur |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | **0,4747** | 0,9835 | 0,9866 | −0,0031 | −0,0548 |
| 0,1 | 0 | 0,4729 | 0,9871 | 0,9908 | −0,0037 | −0,0554 |
| 0 | 0,1 | 0,2341 | 0,8436 | 0,8340 | +0,0096 | −0,0421 |
| **0,1** | **0,1** | **0,3359** | 0,8479 | 0,7959 | **+0,0519** | **+0,0003** |
| 0,3 | 0,3 | 0,3474 | 0,9037 | 0,9158 | −0,0122 | −0,0639 |
| 1 | 1 | 0,2520 | 0,7636 | 0,9040 | −0,1404 | −0,1921 |
| | | | | | **cible** | **+0,0517** |

**À μ_lang = μ_cont = 0,1, notre sortie atteint une séparation de +0,0519 contre
+0,0517 pour le professeur** — l'écart est de 0,0003.

**C'est le résultat important, et il est positif :** la structure contenu/langue du
professeur **est atteignable par une lecture LINÉAIRE des mêmes caractéristiques**.
Les états du réservoir contiennent donc l'information ; c'est l'**objectif** des
moindres carrés qui ne l'extrait pas. Le problème n'est ni la taille du réseau, ni la
richesse des caractéristiques.

### 58.4 Mais l'objectif est NON CONVEXE, et les résultats le montrent

Le terme `−μ_cont·P_cont` étant **soustrait**, la matrice cesse d'être définie positive.
Le code le **signale** (garde ajouté) :

| μ_cont | λ_min de la matrice |
|---:|---:|
| 0,1 (Wikipedia) | −5,7e+03 |
| 0,3 | −7,7e+04 |
| 1,0 | −1,0e+06 |

**Et les résultats sont erratiques** : la séparation vaut +0,052 à μ=0,1, **−0,012 à
μ=0,3** et **−0,140 à μ=1**. Un objectif convexe donnerait une courbe monotone ; ici
la solution n'est pas un minimum mais un **point selle**, et le résultat dépend du
réglage de façon imprévisible.

**Le coût de fidélité est par ailleurs lourd** : 0,4747 → 0,3359, soit −0,139 pour
atteindre la séparation du professeur.

### 58.5 La conclusion, et elle est nette

1. **La cible est atteignable** — la structure contenu/langue du professeur est
   accessible par une lecture linéaire, donc les caractéristiques suffisent.
2. **L'objectif quadratique à deux curseurs n'est pas la bonne façon de l'atteindre** :
   il est non convexe, non monotone, et coûte 0,14 de fidélité.
3. **Ce qu'il faut, c'est une formulation sous CONTRAINTE** — par exemple maximiser la
   fidélité sous contrainte que la séparation atteigne un seuil. Cela reste en forme
   fermée si la contrainte est quadratique (multiplicateur de Lagrange), mais la
   mécanique est différente et n'a pas été essayée.

**Ce qui est établi et ne le sera plus :** le problème du pont n'est ni sa taille, ni
la richesse de ses caractéristiques, ni la quantité de langues. **C'est son
objectif.** Les trois premiers ont été testés et écartés ; celui-ci est mesuré et
localisé.


---
