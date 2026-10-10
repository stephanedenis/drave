> Campagne : **toutes-langues** · expérience **36**
> Titre : 36. Le protocole à DEUX PANNEAUX tranche : le goulot est le TRANSFERT, pas les caractéristiques
> Date réelle : **2026-10-06 11:36 HAE** (source : commit `8dfb6dc`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 36. Le protocole à DEUX PANNEAUX tranche : le goulot est le TRANSFERT, pas les caractéristiques

Le protocole exige l'oracle sur deux panneaux : le **TEST**, hors vivier (41 langues
jamais vues), et la **VALIDATION**, du même vivier que l'apprentissage. Un langage
d'apprentissage sur sept est mis de côté (51 langues), et la lecture est ajustée sur
les 300 restantes seulement. Mesuré, couche 10, 40 neurones, 1 couche, 80
caractéristiques, 896 canaux :

| | TEST (hors vivier) | VALIDATION (même vivier) |
|---|---:|---:|
| fidélité | 0,5960 | **0,6206** |
| témoin constant | 0,5678 | 0,5889 |
| **apport propre** | +0,0282 | **+0,0317** |
| oracle | 0,6935 | 0,6318 |
| **écart à l'oracle** | **+0,0975** | **+0,0112** |

### 36.1 Ce que cela dit, et c'est décisif

**Dans le vivier, notre lecture partagée est à 0,0112 de l'oracle** — c'est-à-dire
quasi optimale. Les caractéristiques suffisent, la lecture suffit, il n'y a rien à
gagner sur ces langues.

**Hors vivier, l'écart est 8,7× plus grand (+0,0975).** Un ajustement privé
rapporterait dix fois plus sur une langue jamais vue que sur une langue du vivier.

**Le goulot n'est donc ni la taille du réseau, ni la lecture, ni les
caractéristiques : c'est le TRANSFERT d'une langue à l'autre.**

### 36.2 Cela réconcilie trois résultats qui semblaient se contredire

- Le §27 trouvait que l'oracle **par langue** restait mauvais sur `deu`, `jpn`, `kor`,
  `heb` — donc « les caractéristiques ne portent pas ces langues ».
- Le §34 trouvait qu'un **gros** réservoir ajoutait +0,0374 par-dessus l'entrée —
  donc la capacité compte.
- Le §29 trouvait qu'à **40** neurones le réservoir n'ajoutait que +0,007.

Les trois tiennent ensemble si l'on sépare les panneaux : **dans le vivier tout va
bien ; c'est la généralisation à une langue nouvelle qui coûte.** Un plus gros
réservoir aide non pas parce que la lecture manque de place, mais parce que ses
caractéristiques **transfèrent mieux**.

### 36.3 La piste que cela désigne

Si le problème est le transfert, la question n'est plus « combien de neurones » mais
**« qu'est-ce qui, dans nos caractéristiques, est propre à la langue et ne transfère
pas ? »**. Le §27 en donne déjà le corrélat : l'apport transfère d'autant mieux que
le tokeniseur hache la langue (R² 0,67), et d'autant moins que sa représentation est
de forte norme.

C'est une question de **facteurs communs**, pas de taille. Et elle est mesurable :
il suffit de chercher la partie des états qui est commune aux langues du vivier, et
de la garder seule.

### 36.4 Note de méthode

La couche 10 a été **recalculée avec le même code** que la couche 8 (`/tmp/profil_l10.csv`),
précisément parce que le protocole a changé le vivier d'ajustement (300 au lieu de
351). Comparer un chiffre ancien à un chiffre nouveau aurait été une faute — c'est
exactement l'erreur de périmètre déjà commise plus tôt dans ce rapport.

L'effet du changement est faible mais réel : à périmètre identique, la fidélité TEST
passe de 0,5972 (351 langues d'ajustement) à 0,5960 (300). L'apport passe de +0,0294
à +0,0282.


---
