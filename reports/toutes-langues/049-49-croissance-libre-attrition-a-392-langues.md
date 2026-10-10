> Campagne : **toutes-langues** · expérience **49**
> Titre : 49. Croissance libre + attrition à 392 langues : le résultat complet
> Date réelle : **2026-10-06 16:41 HAE** (source : commit `a3abff2`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 49. Croissance libre + attrition à 392 langues : le résultat complet

Protocole entier, couche 10, `--part-langues 0.5`, ride 0,03, lecture quadratique,
réservoir multi-échelle, fit sur 1/20 des lignes, **300 langues d'ajustement /
51 de validation / 41 de test**, 896 canaux.

| | |
|---|---:|
| naissance libre | **191 neurones nés**, arrêt par patience |
| **meilleur réseau (selon la VALIDATION)** | **182 neurones · 1 couche** |
| fidélité apprentissage | 0,6501 |
| fidélité VALIDATION | 0,6339 |
| **fidélité TEST** (hors vivier) | **0,6340** |
| constante témoin sur TEST | 0,5762 |
| **apport propre** | **+0,0578** |
| **invariance inter-langue** | **0,8659** |
| **pire paire** | **0,5556** |

Comparé au profil à 40 neurones de la même famille de réglages (couche 10,
multi-échelle, ride 0,03) : fidélité TEST 0,5985 → **0,6340**, soit **+0,0355**.
La croissance et l'attrition apportent donc bien un gain réel.

### 49.1 L'attrition n'a rien retranché d'utile — et c'est un résultat

L'attrition est descendue de 191 à 9 neurones, **et la validation a baissé à chaque
pas** : 0,6339 · 0,6328 · 0,6308 · 0,6288 · 0,6275 · 0,6255 · 0,6243 · 0,6221 ·
0,6206 · 0,6202 · 0,6192 · 0,6158. Le meilleur passage est donc le réseau **né**, et
l'attrition le confirme au lieu de le réduire.

**Mais le TEST, lui, préférait un autre point** : à **144 neurones** le TEST vaut
0,6362 contre 0,6340 à 191. L'écart est faible (0,0022) et il dit quelque chose
d'important : **le critère de sélection (51 langues de validation) et la mesure
d'intérêt (41 langues de test) ne désignent pas le même réseau.** Sélectionner sur
la validation est honnête, mais ce n'est pas gratuit.

### 49.2 Un drapeau qui ne se déclenchait plus, et c'est ma faute

Le bloc **oracle** ne figure pas dans ce résultat. En corrigeant plus tôt le
`IndexError` d'`opt` sur les drapeaux sans valeur, j'ai fait retourner `""` à un
drapeau placé en dernière position — et `if opt("--oracle", "")` devient alors
**faux**. Le drapeau ne plantait plus, il ne faisait plus rien. Quatre drapeaux
étaient dans ce cas : `--oracle`, `--centre-entree`, `--biais`, `--normalise`.

**Un drapeau se teste par sa PRÉSENCE (`in sys.argv`), jamais par sa valeur.** Corrigé
aux quatre endroits. C'est la deuxième fois de la session qu'un drapeau se comporte
mal en silence — la première fois il « marchait par accident » en renvoyant l'option
suivante.

**Conséquence sur le protocole** : sans ce bloc, le diagnostic oracle sur les **deux
panneaux** manque à ce résultat. Il sera fourni par la passe suivante, qui tourne en
outre **sous contrainte d'invariance** (`--mu-inv 0,1`, §48).


---
