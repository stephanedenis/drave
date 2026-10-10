> Campagne : **toutes-langues** · expérience **62**
> Titre : 62. Le remède est trouvé — mais il n'est pas déployable. Et un piège de méthode
> Date réelle : **2026-10-06 21:29 HAE** (source : commit `120d50c`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 62. Le remède est trouvé — mais il n'est pas déployable. Et un piège de méthode

### 62.1 L'énergie de contenu EST récupérable : la preuve

Le §61 a localisé le défaut : notre sortie porte **douze fois moins d'énergie de
contenu** que le professeur, à énergie de langue comparable. Restait à savoir si cette
énergie est **absente** de la représentation ou seulement **sous-produite**.

On amplifie donc la sortie **le long de l'axe du contenu seulement** — en ajoutant
`β·(μ_k − m̄)`, le décalage de contenu de l'entrée, à toutes ses lignes :

| β | fid TEST | P_lang | **P_cont** | **rapport** |
|---:|---:|---:|---:|---:|
| 0 | 0,4747 | 232,0 | 338,7 | 1,46 |
| **1,0** | **0,4749** | 232,0 | 1 354,8 | **5,84** |
| **3,0** | **0,4688** | 232,0 | **5 419,2** | **23,36** |
| 10 | 0,4129 | 232,0 | 40 983 | 176,6 |
| | | | **professeur 4 356** | **10,91** |

**À β = 3, notre énergie de contenu (5 419) dépasse celle du professeur (4 356) pour un
coût de fidélité de 0,006.** Et à β = 1 elle quadruple **sans aucun coût** (0,4749
contre 0,4747).

**Conclusion nette : l'énergie de contenu n'est pas absente, elle est sous-produite.**
Le moindres carrés la rétrécit d'un facteur ~3,6 en amplitude, et il suffit de la
remettre à l'échelle.

### 62.2 Mais la version déployable échoue — et proprement

Le remède ci-dessus utilise le **regroupement par contenu** (`μ_k`), information qui
n'existe pas pour un texte neuf. On teste donc la version calculable à l'inférence :
amplifier le **décalage de moyenne de chaque entrée**, sans toucher aux écarts entre
positions.

| γ | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 0 | 0,4747 | 232,0 | 338,7 | **1,460** |
| 1 | 0,4712 | 928,1 | 1 354,8 | **1,460** |
| 3 | 0,4502 | 3 712,2 | 5 419,2 | **1,460** |
| 5 | 0,4191 | 8 352,5 | 12 193,3 | **1,460** |

**Le rapport vaut exactement 1,460 à tout γ.** La moyenne d'une entrée contient **à la
fois** son décalage de langue et son décalage de contenu : les amplifier ensemble ne
change pas leur rapport. Seule une amplification **de l'axe contenu seul** fonctionne,
et elle exige de savoir quelles entrées partagent un contenu.

### 62.3 Le levier du §48 ne le remplace pas, et révèle un piège de méthode

On teste enfin si la pénalité inter-langue `μ_lang` du §48 rétablit le rapport, en
baissant `P_lang` :

| μ_lang | TEST P_lang | TEST P_cont | **rapport** | fid TEST |
|---:|---:|---:|---:|---:|
| **0** | **232,0** | **338,7** | **1,460** | **0,4747** |
| 0,03 | 218,3 | 283,9 | 1,300 | 0,4741 |
| 0,1 | 195,7 | 217,5 | 1,112 | 0,4729 |
| 0,3 | 158,7 | 144,4 | 0,910 | 0,4710 |
| | | | *professeur* **10,912** | |

**Le rapport BAISSE.** `μ_lang` comprime bien `P_lang` (232 → 159), mais comprime
`P_cont` **davantage encore** (339 → 144). Il ne rétablit pas le rapport, il écrase.

**Et c'est là le piège de méthode, qu'il faut dire :** sur le panneau
d'apprentissage, μ_lang = 0,3 donne un rapport de **3,139**, *supérieur* à celui du
professeur (2,170). On pourrait donc annoncer « nous dépassons le professeur ». C'est
faux : `P_lang` y vaut **51,3** — l'énergie de langue a été écrasée à presque rien, et
le rapport est gonflé par le dénominateur, pas par le numérateur.

**Le rapport `P_cont/P_lang` ne suffit donc pas comme critère.** Le bon critère est
double : **`P_cont` proche de celui du professeur ET `P_lang` qui ne le dépasse pas.**
C'est la leçon de ce paragraphe, et elle vaut pour toute la série §58-§62.

### 62.4 Où en est la question, après cinq paragraphes de traque

| piste | verdict |
|---|---|
| §58 — objectif à deux curseurs | atteint la cible, mais **non convexe** et non monotone |
| §59 — pondération (centrage, normalisation, blanchiment) | **écartée** — prémisse réfutée par le spectre |
| §60 — rétrécissement global | **réel (3,4×)**, mais l'amplifier uniformément n'inverse pas l'ordre |
| §61 — **décomposition de variance** | **défaut localisé** : 12× moins d'énergie de contenu |
| §62 — amplification ciblée | **fonctionne** (β=3 → la magnitude du professeur, coût 0,006) |
| §62 — version déployable | **échoue** : la moyenne par entrée mêle les deux axes |
| §62 — `μ_lang` | **échoue** : comprime les deux, fait baisser le rapport |

**Le problème est maintenant posé en une phrase :** *l'énergie de contenu est
sous-produite d'un facteur ~3,6, elle est récupérable par mise à l'échelle, mais la
mise à l'échelle exige d'isoler l'axe du contenu — et cet axe n'est pas identifiable
sur un texte neuf par les moyens essayés.*

C'est une question précise, avec un chiffre, un remède connu **et une raison
d'échec connue**. Ce n'était pas le cas il y a cinq paragraphes.


---
