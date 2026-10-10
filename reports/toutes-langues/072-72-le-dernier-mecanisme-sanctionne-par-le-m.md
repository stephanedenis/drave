> Campagne : **toutes-langues** · expérience **72**
> Titre : 72. Le dernier mécanisme sanctionné par le mandat — renforcement/atrophie — échoue aussi
> Date réelle : **2026-10-07 00:36 HAE** (source : commit `3133a05`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 72. Le dernier mécanisme sanctionné par le mandat — renforcement/atrophie — échoue aussi

### 72.1 Pourquoi c'était le dernier recours

Les §57-§71 ont écarté, par neuf mesures, tous les moyens de **post-traiter** la sortie.
Le §70 a montré que la transformation qui **crée** la séparation contenu/langue entre la
couche 0 et la couche 8 (rapport 10,912 contre 1,698) n'est pas reproduite par un
réservoir à poids aléatoires gelés.

Restait **un** mécanisme, et il est explicitement sanctionné par le mandat :

> *« L'ajout d'une couche suppose donc une relecture du corpus pour réajuster les poids
> par renforcement/atrophie (pas de backprop). »*

C'est le seul ajustement de poids autorisé en dehors de la lecture, et il n'avait
**jamais** été testé sur l'axe contenu/langue.

### 72.2 Le mécanisme, tel qu'il est implémenté

`Pont.renforce` : on ajuste la lecture, on calcule le **résidu** `R = Y − (φ(X)·W + mt)`,
puis pour chaque neurone on mesure sa **capture** du résidu —
`cap = |corrélation entre sa trace et le résidu|`, normalisée dans `[0, 1]` — et on
multiplie ses poids par `f = 1 + η·(2·cap − 1)`. Renforcé s'il capte plus de la moitié
du résidu, atrophié sinon. **Aucune rétropropagation** : `f` ne dépend que d'une
corrélation locale.

Chaque passe est une **relecture du corpus**, exactement ce que le mandat décrit.

### 72.3 Le résultat : plateau immédiat

| passe | η | fid TEST | P_lang | P_cont | **RAPPORT** |
|---:|---:|---:|---:|---:|---:|
| **0** | — | 0,4766 | 247,1 | 318,7 | **1,290** |
| **1** | 0,10 | 0,4768 | 241,9 | 317,2 | **1,311** |
| **2** | 0,10 | 0,4769 | 241,7 | 317,0 | **1,312** |
| | | | | **cible** | **10,912** |

**+0,021 à la première passe, +0,001 à la seconde : le plateau est atteint
immédiatement.** Le gain relatif est de **+1,7 %** là où il faudrait **+746 %**.

La capture moyenne du résidu vaut ≈ 0,5, ce qui est attendu d'un réservoir aléatoire :
**aucun neurone ne capte le résidu mieux que le hasard**, donc aucun n'est franchement
renforcé ni atrophié, et le facteur `f` reste proche de 1.

### 72.4 Une réserve de méthode, et elle est importante

J'ai testé **la forme de renforcement implémentée dans le dépôt**, appliquée comme le
mandat la décrit. **D'autres formes existent** — un renforcement portant sur les poids
d'entrée `B` plutôt que sur l'échelle globale, un renforcement compétitif entre
neurones, une mesure de capture fondée sur autre chose que la corrélation maximale. Je
n'en ai testé qu'une, et **c'est la seule réserve qui reste** à cette conclusion.

Mais la forme testée est celle que le projet a écrite, et elle échoue d'un facteur 470.

### 72.5 Ce que la traque complète établit

| mécanisme autorisé | testé | résultat |
|---|---|---|
| réservoir aléatoire gelé | §29, §34, §70, §71 | **coûte** en fidélité **et** en structure |
| lecture en forme fermée | §58-§69 | borne à 6,96 de rapport en payant 0,12 à 0,23 |
| post-traitements linéaires | §58-§69 | neuf moyens, sept écartés |
| **renforcement/atrophie** | **§72** | **+1,7 % du chemin nécessaire** |

**Tous les mécanismes que le projet s'autorise ont été mesurés, et aucun ne produit la
transformation entre la couche 0 et la couche 8 du professeur.**

C'est la conclusion de la traque. Elle est négative, elle porte sur l'architecture, et
elle est établie par **douze paragraphes de mesures** dont chacune écarte une piste ou
localise un défaut. Ce qui manque n'est pas un réglage : c'est **le mécanisme qui
calcule**. Un réservoir aléatoire ne calcule pas huit couches d'attention ; une lecture
linéaire ne les improvise pas ; un renforcement local ne les découvre pas.

**La question que cela pose est précise et elle est pour la prochaine étape** : sous les
contraintes maintenues — un seul professeur, boîte noire, aucune rétropropagation —
**quel mécanisme, autre que le réservoir aléatoire gelé, peut produire cette
transformation ?**


---
