# Deux nuits, deux expériences — la première garde son gain, la seconde n'ajoute presque rien

> Campagne : **cerveau** · expérience : le sommeil **répété** — la question du plan C7 que les
> fiches précédentes laissaient ouverte (« un rejeu répété ou séquentiel n'est pas mesuré »).
> Question : une **deuxième nuit** sur des textes **différents** efface-t-elle ce que la première a
> consolidé (**oubli catastrophique**), ou s'y ajoute-t-elle — et vaut-elle le même prix qu'une
> première nuit à volume égal ?
> Verdict : **ni oubli, ni gain.** La nuit 1 (5 morceaux, m0..m4) amène m32 de **7,1787 à 6,6151**
> (**−7,85 %**) et m20 de **18,4607 à 15,9408** (**−13,65 %**). La nuit 2 (5 morceaux **différents**,
> m10..m14), qui repart du modèle de la nuit 1, laisse m32 à **6,5950** (**−0,30 %** de plus) et m20
> à **16,0440** (**+0,65 %**, très légèrement pire). **Rien n'est oublié** — et **rien n'est gagné** :
> à volume égal, la deuxième nuit vaut **0,3 point** là où la première en valait **7,9**.
> Date réelle : **2026-10-15 00 h 10-00 h 40 HAE** (heure lue sur la machine)
> Protocole : `tools/n4_dessin_b.py --objectif plein` · nuit 1 : m0..m4, 8 époques, validation m29 ·
> nuit 2 : `--lora-depart` (le LoRA de la nuit 1 est **repris**), rejeu m10..m14, 8 époques ·
> l'époque se choisit sur la **même** validation (m29, hors des deux rejeux) · test m32 **et** m20,
> jamais rejoués ni validés · graine 0 · mesure du **modèle complet**.

## 1. Les chiffres

| | m32 | écart | m20 | écart |
|---|---:|---:|---:|---:|
| modèle de base | 7,1787 | — | 18,4607 | — |
| **après la nuit 1** (m0..m4, époque 2) | **6,6151** | **−7,85 %** | **15,9408** | **−13,65 %** |
| **après la nuit 2** (m10..m14, époque 1) | **6,5950** | −0,30 % *(sur la nuit 1)* | 16,0440 | +0,65 % *(sur la nuit 1)* |

Ce que ça dit :

* **pas d'oubli catastrophique, à cette échelle** : la nuit 2 ne ramène **pas** m32 vers 7,18 — elle
  le laisse à 6,60. Le LoRA de la nuit 1 n'est pas écrasé par cinq nouveaux morceaux, et c'est la
  première mesure de **continuité** du dépôt : deux expériences se succèdent **sans se détruire** ;
* **mais la nuit 2 n'apporte presque rien** : −0,30 % sur m32, **+0,65 %** sur m20 — du bruit. À
  volume égal (5 morceaux, 8 époques), la première nuit valait 7,9 points et la seconde 0,3. **Le
  rendement d'une nuit s'effondre dès la deuxième** ;
* **c'est cohérent avec la courbe du budget** (`rapport-sommeil-budget.md`) : 3 morceaux → −5,6 %,
  20 morceaux → −10,0 % — soit **−2,5 % par doublement**. Une deuxième nuit de 5 morceaux est le
  doublement suivant d'une première nuit de 5 : ~−1 point attendu, et on en mesure 0,3. La courbe
  explique l'ordre de grandeur, le reste est dans le bruit ;
* **ce que ça ne dit pas, et il faut le lire ainsi** : « la deuxième nuit ne sert à rien » **n'est
  pas** établi — ce qui est établi est que, **sur le même corpus**, cinq morceaux de plus après une
  première nuit n'ajoutent presque rien. Une deuxième nuit sur un **autre domaine** (ou sur des
  tâches, pas du texte) poserait une autre question — et c'est exactement là que l'oubli
  catastrophique se mesurerait.

## 2. Ce que ça change pour le protocole de sommeil

1. **une nuit bien choisie vaut mieux que deux nuits** — à volume total égal, la première porte
   presque tout le gain (7,9 sur 8,2 points mesurés) ;
2. **la continuité existe** : rien n'interdit d'enchaîner les nuits, et rien n'est perdu — mais rien
   n'est gagné non plus, sur le même corpus ;
3. **la question ouverte est nommée** : le jour où le rejeu portera sur un **domaine différent** (ou
   sur des épisodes, pas des textes), c'est le prix de l'ancien qui devient la question — et le
   protocole (`--lora-depart` + deux jeux de test) est désormais en place pour le mesurer.

## 3. Ce que cette fiche ne dit pas

* **deux nuits, une graine** : l'écart de la nuit 2 (−0,30 % / +0,65 %) est **du même ordre que le
  bruit de graine** mesuré sur ce bras (0,14 point, `rapport-sommeil-budget.md` § 1bis) — il ne
  faut donc pas lire « la nuit 2 dégrade m20 » : elle ne fait **rien** de mesurable ;
* **pas de remise à zéro de l'optimiseur** : la nuit 2 repart d'un Adam neuf (le `--lora-depart` ne
  transporte que les poids) ; un état d'optimiseur conservé pourrait donner un autre résultat, et
  ce n'est pas mesuré ;
* **même domaine, même corpus** : les deux nuits rejouent des morceaux du **même** texte
  (wikitext2) — c'est ce qui rend le « pas d'oubli » peu surprenant, et c'est dit ;
* **un seul volume** (5 + 5 morceaux) : la forme de la courbe « deuxième nuit » (2, 5, 10 morceaux)
  n'est pas faite.
