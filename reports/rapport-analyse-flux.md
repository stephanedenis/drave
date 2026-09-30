# Analyse du flux, couche par couche

Première analyse **pure** : aucune exécution du moteur, seulement une trace relue
(`tools/analyse_flux.py`). Ce qu'elle apporte, et pourquoi ces questions-là ont
été posées plutôt que d'autres.

Modèle : Qwen2.5-0.5B Q8_0, contexte 256, 256 jetons, 24 couches, 896 cachés,
trace enregistrée avec `--abits 8 --act-thresh 0.05` (réglage de COÛT, pas de
qualité : la perplexité de cette configuration est de 2 445 — ce qui suit décrit
la forme du flux, pas la qualité du modèle).

## Densité : où le push paie, où le pull paie

Le croisement push/pull du projet est mesuré à **~10 % de densité**. Ce qui
manquait était la densité **par couche** — or elle varie du simple au triple :

| couche | densité | couche | densité |
|---|---|---|---|
| **9** | **20,1 %** | 6 | 40,5 % |
| 0 | 25,9 % | 5 | 45,6 % |
| 4 | 26,7 % | **1** | **56,3 %** |
| 3 | 28,8 % | 8 | 29,2 % |

Autrement dit : la décision « listes ou matrice dense » n'est pas une propriété du
modèle, c'est une propriété de la **couche**. Une architecture qui traite tout le
modèle de la même façon perd d'un côté ou de l'autre.

## Persistance : ce qui est toujours là

Neurones actifs dans au moins 90 % des jetons, par couche : **0,89 % à 1,90 %**
du vecteur. C'est peu, mais c'est ce qui doit rester résident quoi qu'on fasse —
et c'est cohérent avec la mesure d'activation du projet (0,08 % « chauds » plus
de 90 % du temps sur un autre modèle et un autre seuil).

## Concentration : combien porte quoi

Par couche, les **10 % de neurones les plus forts portent 26 % à 67 %** de la
magnitude, et le 1 % le plus fort en porte 5 % à 16 %. La couche 9 est la plus
concentrée (67 % pour 10 %), la couche 1 la moins (26 %) — et c'est aussi la plus
dense : les deux mesures vont dans le même sens, ce qui est rassurant sur la
cohérence de l'analyse.

## Recouvrement : une direction qui traverse la pile

Recouvrement des 50 neurones les plus forts entre couches **voisines** : de
**28 % à 86 %**. Les couches 5 à 8 se partagent 84-86 % de leurs neurones
dominants — une même direction y travaille — tandis que le passage 0 → 1 ne
partage que 28 %.

C'est le genre de fait qu'aucune perplexité ne montre, et qui décide de ce qu'on
précharge, de ce qu'on élague et de ce qu'on place sur quel composant.


## Modèle de coût par couche (dérivé, pas mesuré)

Le croisement push/pull mesuré du projet est à ~10 % de densité. Avec les densités
ci-dessus, la conséquence par couche est directe :

| couche (densité) | régime attendu | raison |
|---|---|---|
| 9 (20,1 %), 0 (25,9 %), 4 (26,7 %), 3 (28,8 %), 8 (29,2 %) | au-dessus du croisement | les listes coûtent moins que la matrice |
| 6 (40,5 %), 5 (45,6 %), 1 (56,3 %) | en dessous | la matrice dense est plus économique |

Ce tableau est une **projection**, pas une mesure : il dit où regarder pour la
phase 1.2 (« quantification et chemin choisis par la mesure »), et il donne le
critère du banc à écrire — comparer, pour chaque couche, le temps du chemin par
listes et celui du chemin dense. La trace fournit la densité ; le moteur fournit
les deux chemins ; il ne manque que la comparaison systématique.
