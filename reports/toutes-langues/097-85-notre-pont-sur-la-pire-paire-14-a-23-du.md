> Campagne : **toutes-langues** · expérience **85**
> Titre : 85. NOTRE PONT SUR LA PIRE PAIRE : 14 à 23 % du professeur, et jusqu'à 62 % sur de–fr
> Date réelle : **2026-10-07 11:08 HAE** (source : commit `207ef67`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 85. NOTRE PONT SUR LA PIRE PAIRE : 14 à 23 % du professeur, et jusqu'à 62 % sur de–fr

Toutes les mesures du §82 portaient sur le professeur. Reste la question qui compte : **nous,
sur ces mêmes paires ?** `rapport_du_pont.py` mesure les deux sur le même panel, avec le
protocole de référence du dépôt (masque des canaux vivants ≥ 0,5, 120 neurones, lecture
quadratique, ride 0,03, graine 5).

### 85.1 Deux sens croisés, tous deux HORS VIVIER

| apprentissage | évaluation | fidélité TEST | notre rapport | professeur | **part** |
|---|---|---:|---:|---:|---:|
| de/en/fr | **es/it/pt** | 0,4780 | 1,676 | 12,001 | **14,0 %** |
| es/it/pt | **de/en/fr** | 0,4652 | 0,301 | 1,316 | **22,9 %** |
| de/en/fr | de/en/fr *(in-sample pour nous)* | 0,5067 | 0,193 | 1,316 | 14,6 % |

### 85.2 Paire par paire

| évaluation | paire | notre P_lang | notre P_cont | **notre rapport** | professeur | **part** |
|---|---|---:|---:|---:|---:|---:|
| es/it/pt | es–it | 225,8 | 439,3 | 1,945 | 12,936 | 15,0 % |
| es/it/pt | it–pt | 196,8 | 517,3 | 2,628 | 12,681 | 20,7 % |
| es/it/pt | es–pt | 136,6 | 533,1 | 3,901 | 54,428 | **7,2 %** |
| de/en/fr | **de–en (la pire)** | 1 197,5 | 457,8 | 0,382 | 1,494 | 25,6 % |
| de/en/fr | en–fr | 1 173,5 | 451,3 | 0,385 | 2,288 | 16,8 % |
| de/en/fr | de–fr | 271,7 | 402,4 | **1,481** | 2,386 | **62,1 %** |

### 85.3 Ce que ces chiffres disent, et ce qu'ils ne disent pas

**1. Notre rapport dépend du panel autant que celui du professeur.** 1,676 sur es/it/pt,
0,301 sur de/en/fr : facteur 5,6. Ce n'est donc pas un défaut du professeur, c'est une
propriété des paires de langues. **Toute affirmation sur ce rapport doit nommer sa paire.**

**2. La « part du professeur » est, elle, beaucoup plus stable : 14 à 23 %.** C'est la
formulation robuste. Elle dit la même chose sur les deux sens croisés, alors que les rapports
absolus, eux, varient d'un facteur 5,6.

**3. Nous sommes en retard sur les DEUX axes, pas seulement sur le contenu.** Sur de–en :
`P_cont` 457,8 contre 5 037,6 (**11×**) et `P_lang` 1 197,5 contre 3 372,6 (**2,8×**). Le
professeur sépare *davantage* l'allemand de l'anglais que nous. Le rapport, qui est un
quotient, masquait ce double retard.

**4. Notre pire paire est la même que la sienne (de–en), et notre meilleure aussi (de–fr
contre es–pt).** L'ordre des difficultés se transfère. C'est un point commun réel — et c'est
la première fois qu'une structure du professeur se retrouve chez nous **sur un classement**,
et non sur une valeur.

**5. La tentation à écarter.** Notre 1,676 sur es/it/pt est numériquement presque égal au
1,697 du professeur **sur 6 langues**. Il serait malhonnête d'en tirer quoi que ce soit :
deux panels différents. C'est exactement l'erreur que le §82 vient de corriger, et il serait
absurde de la refaire dans l'autre sens, à notre avantage.

### 85.4 Ce qui reste ouvert après cette mesure

La part de 14 à 23 % est mesurée **sur le protocole de référence, sans discrimination, sans
croissance, sans aucun des leviers des §73–§80**. Les §74–§80 avaient mesuré qu'un
discriminant appris portait le rapport à 105 % de la cible **sur le panel roman**. La
question ouverte, et elle est maintenant précise :

> **Le discriminant apprend sur un panel donné. Que vaut-il sur la pire paire — et
> transfère-t-il d'un panel à l'autre ?**

C'est la prochaine mesure, et elle est rendue possible par les outils de ce paragraphe.

---
