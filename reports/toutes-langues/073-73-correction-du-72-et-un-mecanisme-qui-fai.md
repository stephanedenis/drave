> Campagne : **toutes-langues** · expérience **73**
> Titre : 73. CORRECTION du §72, et un mécanisme qui fait enfin les DEUX mouvements
> Date réelle : **2026-10-07 01:08 HAE** (source : commit `e7f3b95`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 73. CORRECTION du §72, et un mécanisme qui fait enfin les DEUX mouvements

### 73.1 La correction : la capture vaut 0,018, pas 0,5

Le §72 affirmait : *« La capture moyenne du résidu vaut ≈ 0,5, ce qui est attendu d'un
réservoir aléatoire : aucun neurone ne capte le résidu mieux que le hasard. »*

**Ce chiffre, je ne l'avais pas lu.** La ligne qui l'affiche arrivait après huit passes
que j'avais interrompues ; j'ai **déduit** 0,5 au lieu de le mesurer, et je l'ai écrit
comme un résultat.

**La mesure réelle est 0,018** — plus de vingt fois moins. Et cela **change
l'explication de l'échec du §72** :

```
f = 1 + η·(2·cap − 1)     avec cap = 0,018  ->  f = 1 − 0,964·η
```

**Tous les neurones sont atrophiés, presque également.** Or une atrophie uniforme est une
**mise à l'échelle globale** — et le §67 a établi qu'aucune mise à l'échelle ne peut
changer le rapport, c'est une identité. **Le plateau du §72 n'est donc pas une surprise :
il était mathématiquement forcé.** Le mécanisme ne pouvait pas marcher, non parce que le
renforcement est impuissant, mais parce que **sa forme implémentée produit une
transformation de degré 0**.

**C'est une correction qui renforce la conclusion au lieu de l'affaiblir** : le §72
n'écartait pas « le renforcement », il écartait « le renforcement **par mise à
l'échelle** » — ce qui laissait la réserve ouverte, et elle valait la peine d'être
explorée.

### 73.2 La réserve, explorée : apprendre QUOI LIRE

Mettre à l'échelle ne change pas **ce qu'un neurone lit**, seulement l'amplitude de ce
qu'il lit déjà. Si aucun neurone ne capte le résidu (0,018), c'est peut-être qu'aucun ne
lit la bonne direction de l'entrée.

On apprend donc à chaque neurone **la direction de l'entrée qui prédit le résidu**, par
corrélation seule :

```
G = Eᵀ·R          covariance croisée entrée / résidu
SVD(G) = U·S·Vᵀ   les colonnes de U sont les directions les plus prédictives
B_j ← U[:, j]     chaque neurone reçoit SA direction
```

**Aucune rétropropagation** : `G` est une corrélation entre l'entrée et le résidu, et
chaque neurone ne reçoit qu'une direction. C'est de la règle de Hebb appliquée à
l'entrée du réservoir.

### 73.3 Le résultat : le premier mécanisme qui fait les DEUX mouvements

| passe | capture | fid TEST | **P_lang** | **P_cont** | **RAPPORT** |
|---:|---:|---:|---:|---:|---:|
| 0 | 0,018 | 0,4766 | 247,1 | 318,7 | 1,290 |
| **1** | 0,017 | **0,4667** | **181,9** | **438,5** | **2,411** |
| 2 | 0,018 | 0,4681 | 208,4 | 484,8 | 2,326 |
| 3 | 0,018 | 0,4666 | 210,1 | 460,3 | 2,191 |
| | | | | **professeur** | **10,912** |

**Une seule passe fait passer le rapport de 1,290 à 2,411 — et surtout :**

- **`P_cont` MONTE** (318,7 → **438,5**),
- **`P_lang` BAISSE** (247,1 → **181,9**),
- pour **0,010** de fidélité.

**C'est le premier mécanisme de toute la traque dont les deux énergies vont dans des
directions OPPOSÉES.** Tous les autres — centrage (§64), sous-espace (§66), discriminant
(§69), blanchiment (§71), mise à l'échelle (§72) — faisaient baisser les deux, ou
faisaient monter les deux. **Aucun n'avait jamais fait monter le contenu en faisant
baisser la langue.**

Et cela se lit directement sur le critère du §62.3, le seul qui compte :

| méthode déployable | P_lang (< 399 ?) | **P_cont** | rapport |
|---|---:|---:|---:|
| rien | 247,1 ✓ | 318,7 | 1,290 |
| centrage + sous-espace (§66) | 22,9 ✓ | 70,2 | 3,064 |
| discriminant rang 2 (§69) | 4,3 ✓ | **30,2** | 6,961 |
| **apprendre quoi lire (§73)** | **181,9 ✓** | **438,5** | **2,411** |
| *professeur* | *399,2* | *4 356,4* | *10,912* |

**Le discriminant a le meilleur rapport, mais il écrase le contenu (30,2). « Apprendre
quoi lire » a un rapport plus modeste (2,411) mais porte **14 fois plus d'énergie de
contenu** (438,5), tout en restant sous l'énergie de langue du professeur.**

### 73.4 Ce que cela établit

**1. Le renforcement n'est pas impuissant — sa forme par mise à l'échelle l'était.** Le
§72 avait conclu trop largement ; le §73 le corrige en testant la forme qui agit sur
*quoi* lire plutôt que sur *combien*.

**2. Agir sur les directions d'entrée est le premier levier qui attaque le bon axe.**
`P_cont` monte et `P_lang` baisse simultanément — c'est exactement ce que la mission
demande, et c'était absent de tous les moyens précédents.

**3. Mais un seul passage suffit, puis le mécanisme sature** (2,411 → 2,326 → 2,191).
Il reste **4,5 fois** sous la cible. Le gain n'est pas cumulable — probablement parce
qu'après une passe, `U` change peu et le mécanisme se répète à l'identique.

**4. Et cela ouvre une piste qui n'existait pas il y a une heure** : si **apprendre quoi
lire** améliore le contenu *et* la langue, et si le **discriminant** optimise le rapport
en écrasant le contenu, les deux sont **complémentaires** — l'un agit sur les
caractéristiques, l'autre sur la lecture. **Leur combinaison n'a pas été essayée.**


---
