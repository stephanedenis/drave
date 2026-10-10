> Campagne : **toutes-langues** · expérience **22**
> Titre : 22. CORRECTION : la « richesse » n'est pas dans le nombre de canaux actifs
> Date réelle : **2026-10-06 05:15 HAE** (source : commit `4e12ea6`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 22. CORRECTION : la « richesse » n'est pas dans le nombre de canaux actifs

Au tour précédent j'ai annoncé, sur un échantillon de huit traces, que Wikipedia
activait la couche « beaucoup plus densément » que l'UDHR — 810-864 canaux actifs
contre un minimum de 5. **C'était faux** : j'avais comparé un **minimum**
échantillonné à une **moyenne**.

Distribution complète, couche 10, sur 896 canaux :

| corpus | min | p10 | médiane | p90 | max | positions |
|---|---:|---:|---:|---:|---:|---:|
| UDHR (392 langues) | 60 | 850 | 862 | 873 | 889 | 20 803 |
| Wikipedia (en/fr) | 63 | 858 | **871** | 880 | 890 | 5 732 |
| Romeo (24 scènes) | 79 | 860 | **872** | 880 | 891 | 19 135 |

**La médiane va de 862 à 872 — 1 % d'écart.** Le minimum réel est de 60, pas 5. La
« richesse » d'un corpus ne se lit donc **pas** dans le nombre de canaux actifs.

### La vraie caractérisation, et les deux mesures ne se contredisent pas

**La couche 10 du professeur est DENSE EN SUPPORT et CREUSE EN ÉNERGIE :**

| | mesure |
|---|---|
| canaux non nuls | **862 sur 896 (96 %)** — dense |
| énergie portée par 50 % des canaux | **40 canaux (4 %)** — concentrée |

Ce ne sont pas deux mesures contradictoires, mais **deux questions différentes** :
*combien de canaux parlent* (presque tous) et *lesquels portent le signal* (une
poignée). J'avais laissé entendre qu'elles s'opposaient ; elles se complètent.

**Conséquence pour la sélection de canaux** : garder les 157 canaux énergétiques ne
revient pas à écarter du vide — 96 % des canaux sont non nuls. Cela revient à
écarter **du bruit de faible amplitude**, ce qui explique pourquoi la restriction
fonctionne aussi bien : on ne jette presque que du détail.


---
