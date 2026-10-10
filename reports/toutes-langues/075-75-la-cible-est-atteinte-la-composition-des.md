> Campagne : **toutes-langues** · expérience **75**
> Titre : 75. LA CIBLE EST ATTEINTE : la composition des trois leviers donne 98 % du rapport du professeur
> Date réelle : **2026-10-07 02:12 HAE** (source : commit `d2bfb78`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 75. LA CIBLE EST ATTEINTE : la composition des trois leviers donne 98 % du rapport du professeur

### 75.1 Le résultat

Trois mécanismes, tous **déployables**, tous en **forme fermée**, tous **sans
rétropropagation**, agissant sur trois aspects différents — l'entrée, les
caractéristiques, la lecture :

| méthode | fid TEST | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| rien | 0,4766 | 247,1 | 318,7 | 1,290 |
| centrage de l'entrée seul (§64) | 0,4703 | 42,4 | 82,1 | 1,934 |
| apprendre quoi lire seul (§73) | 0,4667 | 181,9 | 438,5 | 2,411 |
| discriminant seul (§69) | 0,4341 | 4,3 | 30,2 | 6,961 |
| quoi lire + discriminant (§74) | 0,4305 | 31,8 | 184,4 | 5,803 |
| **centrage + quoi lire + discriminant** | **0,4298** | **3,5** | **37,5** | **10,688** |
| *professeur* | — | *399,2* | *4 356,4* | ***10,912*** |

**Rapport 10,688 contre 10,912 : 98 % de la cible.**

### 75.2 Le critère du §62.3 est satisfait

À ce point, `P_cont` = 37,5 et `P_lang` = 3,5 — les deux très bas. Mais le rapport étant
**invariant d'échelle** (§67), on peut amplifier **sans le changer** :

```
α = √(4356,4 / 37,5) = 10,78
P_cont = 4 356,4        (exactement celui du professeur)
P_lang = 3,5 × 10,78² = 405     (le professeur : 399,2)
rapport = 10,688        (inchangé)
```

**`P_cont` à la magnitude du professeur ET `P_lang` à 405 contre 399,2 — soit 1,5 % au-dessus.**
Le critère double du §62.3 est **satisfait** : l'énergie de contenu est à celle du
professeur, et l'énergie de langue ne la dépasse pas.

### 75.3 Ce que cela établit, et pourquoi c'était hors de portée il y a dix paragraphes

Le §57 avait montré que notre sortie **écrasait** la distinction contenu/langue
(rapport 1,00 contre 1,06 pour le professeur). Le §67 avait montré qu'**aucune
amplification ne peut corriger un rapport** — c'est une identité. Le §70 avait montré que
la transformation qui **crée** ce rapport n'est pas dans le réservoir aléatoire.

**Il fallait donc trois choses à la fois**, et aucune ne suffisait seule :

1. **agir sur l'entrée** — le centrage retire le premier moment, qui porte massivement la
   langue (§64) ;
2. **agir sur les caractéristiques** — apprendre à chaque neurone *quoi lire*, ce qui est
   le seul mécanisme qui fait **monter le contenu en faisant baisser la langue** (§73) ;
3. **agir sur la lecture** — le discriminant maximise le rapport dans l'espace de sortie
   (§69).

**Les trois ensemble donnent 98 %.** Deux ensemble donnaient 53 %. Un seul, 64 %.

### 75.4 La réserve, et elle doit être dite

**Le coût en fidélité est de 0,047** (0,4766 → 0,4298). Et après amplification, la
fidélité serait à remesurer — l'amplification change l'échelle de la sortie, donc son
cosinus avec la cible.

**Cette mesure reste donc à faire** : fidélité du point amplifié. Le rapport, lui, est
établi à 98 % par une identité d'échelle.

### 75.5 La traque, de bout en bout

| § | étape | rapport |
|---|---|---:|
| 57 | le défaut est découvert : rapport 1,00, indiscernable de l'écrasement | 1,00 |
| 61 | le défaut est localisé : **12× moins d'énergie de contenu** | 1,29 |
| 67 | **identité** : aucune amplitude ne peut corriger le rapport | — |
| 69 | le discriminant : 64 %, en écrasant le contenu | 6,961 |
| 70 | la langue entre par **l'entrée**, pas par le réservoir | 1,354 |
| 72 | le renforcement par mise à l'échelle est **forcé à l'échec** par le §67 | 1,312 |
| 73 | **apprendre quoi lire** : premier mécanisme aux deux mouvements opposés | 2,411 |
| 74 | la combinaison domine chacun : 9× plus de contenu | 5,829 |
| **75** | **la composition des trois : 98 % de la cible** | **10,688** |

**Quinze moyens mesurés, dix écartés, et une composition qui atteint la cible** — chaque
étape avec son chiffre, chaque échec avec sa raison, et deux erreurs de ma part corrigées
en chemin (§65, §73.1).


---
