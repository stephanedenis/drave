> Campagne : **toutes-langues** · expérience **86**
> Titre : 86. LE DISCRIMINANT TRANSFÈRE — mais il perd l'essentiel en changeant de panel
> Date réelle : **2026-10-07 11:31 HAE** (source : commit `8d76d1e`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 86. LE DISCRIMINANT TRANSFÈRE — mais il perd l'essentiel en changeant de panel

### 86.1 La question, posée au §85.4

Le §80 avait mesuré qu'un discriminant linéaire portait notre rapport à **105 % du
professeur**. Le §82 vient d'établir que ce résultat a été obtenu **et mesuré** sur le panel
roman es/it/pt. La question qui reste est donc :

> **Un projecteur appris à séparer l'espagnol, l'italien et le portugais sait-il séparer
> l'allemand de l'anglais ?**

Rien ne l'assurait. Le discriminant maximise `C_cont/C_lang`, et `C_lang` est estimé **sur
les langues du panel d'apprentissage** : si l'axe de langue qu'il apprend est « l'axe
roman », il peut être orthogonal à « l'axe germanique ».

### 86.2 Le protocole

Trois caches, un seul pont (appris sur de/en/fr dans les quatre cas), un discriminant appris
sur un panel puis appliqué à un autre. **Aucun réglage ne change entre les cas** — seul
l'échange des caches. Les cas 2 et 4 sont les seuls **hors vivier** : le discriminant y est
appris sur un panel et évalué sur l'autre. Les cas 1 et 3 sont les références **dans-panel**.

| cas | discriminant appris sur | mesuré sur | rang 0 (notre pont) | **rang 2** | professeur | **part** |
|---|---|---|---:|---:|---:|---:|
| **1** | es/it/pt | es/it/pt *(dans-panel)* | 1,676 | **38,443** | 12,001 | **320,3 %** |
| **2** | es/it/pt | **de/en/fr** *(transfert)* | 0,193 | **0,411** | 1,316 | **31,2 %** |
| **3** | de/en/fr | de/en/fr *(dans-panel)* | 0,193 | **2,783** | 1,316 | **211,5 %** |
| **4** | de/en/fr | **es/it/pt** *(transfert)* | 1,676 | **6,610** | 12,001 | **55,1 %** |

Le rang 2 est l'optimum dans les **quatre** cas — cohérent avec le §80 : `C_lang` est de rang
au plus `n_langues − 1` = 2.

### 86.3 Le fait : le transfert est RÉEL mais ASYMÉTRIQUE

**Le discriminant transfère.** Appris sur les langues germaniques et appliqué aux langues
romanes, il porte notre rapport de 1,676 à **6,610** — 55,1 % du professeur au lieu de
14,0 %. Ce n'est pas rien : un axe de langue appris sur un panel garde du sens sur un autre.

**Mais il perd l'essentiel.** Dans-panel il valait 211 à 320 % ; en transfert, 31 à 55 %. Le
facteur perdu est de **4 à 7**. Et il est **asymétrique** : germanique→roman (55,1 %) vaut
près du double de roman→germanique (31,2 %). Le sens facile est celui où l'on apprend sur
les langues **les plus éloignées** et où l'on applique aux plus proches — ce qui est
exactement ce que la théorie du §82.3 prédit, puisque c'est `P_lang` du panel
d'apprentissage qui règle l'axe appris.

### 86.4 La pire paire résiste, et le classement des difficultés ne survit pas

Cas 2, rang 2, paire par paire — et en regard la valeur du professeur :

| paire | rang 0 | **rang 2** | professeur | **part** |
|---|---:|---:|---:|---:|
| **de–en** (la pire du professeur) | 0,240 | **0,680** | 1,494 | **45,5 %** |
| en–fr | 0,310 | **0,360** | 2,288 | **15,7 %** |
| de–fr | 0,530 | **3,887** | 2,386 | **163,1 %** |

**Trois choses, dont la troisième est un recul.**

1. **Sur de–fr, le discriminant transféré DÉPASSE le professeur** (3,887 contre 2,386, soit
   163 %). Le mécanisme n'est donc pas intrinsèquement incapable de traiter des langues
   germaniques : il en traite une.

2. **Sur la pire paire (de–en), il reste à 45,5 %.** C'est mieux que les 16,1 % du rang 0
   (0,240 / 1,494), mais loin du compte.

3. **Le classement des difficultés ne survit PAS à la projection.** Au rang 0, notre pire
   paire est de–en — la même que celle du professeur. Au rang 2, notre pire paire devient
   **en–fr** (0,360 contre 0,680). Le §85.3 avait noté comme un point commun réel que
   *« l'ordre des difficultés se transfère »* : **ce n'est vrai qu'avant projection.** Le
   discriminant réorganise les axes, et il le fait d'une façon qui ne respecte plus la
   géométrie du professeur.

### 86.5 Ce que cela corrige dans le §80

Le §80 annonçait : *« le discriminant NON SEULEMENT se réplique — il DÉPASSE le professeur,
12,645 contre 12,001, pour 0,038 de fidélité »*, et le §B.2 rangeait ce résultat parmi
*« ce qui est acquis et qui le restera »*.

**Ce qui reste acquis** : le discriminant est en forme fermée, sans rétropropagation,
déployable comme matrice fixe, et il **fonctionne** — 320 % du professeur sur son panel.

**Ce qui doit être corrigé** : le mot « dépasse ». Un projecteur de rang 2 sur un panel de
3 langues dispose de 2 directions pour faire coïncider 3 moyennes de langue — il peut
presque les annuler **dans-panel**, et c'est ce qu'il fait. Le chiffre de 320 % mesure donc
autant la capacité du projecteur à s'ajuster au panel que sa capacité à séparer le contenu
de la langue. **Le seul chiffre qui vaut est hors vivier : 31 à 55 %.**

C'est la **quatrième** fois dans cette session qu'un chiffre se révèle indexé sur un choix
non déclaré (graine au §81, panel au §82, pooling au §84.1, ajustement au §86). La règle des
§81.6 et §84.1 se complète d'un quatrième terme :

> **Avant d'écrire un chiffre : nommer la graine, le panel, le pooling — et si le modèle a
> été ajusté sur les données qu'on mesure.**

### 86.6 La question ouverte, maintenant précise

Le §85.4 demandait si le discriminant transfère. Réponse : **oui, en perdant 4 à 7×**.

Ce qui n'est pas mesuré, et qui est la suite naturelle :

> **Un discriminant appris sur les QUINZE paires à la fois — plutôt que sur trois langues —
> transfère-t-il mieux ? Et si l'axe de langue est ce qui ne transfère pas, qu'obtient-on en
> apprenant les directions sur le contenu SEUL, langue tenue pour nuisance ?**

C'est la prochaine mesure. Les outils sont en place : `discriminant_transfert.py` prend trois
caches et fait varier le panel du discriminant indépendamment de celui du pont.

---
