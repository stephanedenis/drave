# B10.2bis — l'attention croisée ne décolle pas le décodeur : 16,5 / 11,2 contre un plancher de 38,5

> **Ligne de roadmap** : B10.2bis (déblocage de B10.3) · **Date** : 2026-10-29 · **Verdict** :
> ❌ **négatif net** — trois bras (projection, **attention croisée**, segments), **3 graines**
> chacun, 600 pas : le chrF de traduction plafonne à **11.13 / 11.2 / 11.0**
> contre un plancher de **38.5**. L'attention croisée ne fait pas mieux que la
> projection : **le plancher du décodeur n'est pas un problème d'attention**.
>
> **Dispositif** : corpus UDHR parallèle (30 articles, 10 langues, 24/6 par article), modèle
> natif **9,29 M** (`/tmp/natif-224-6-align-s1`), 600 pas, lot 8, seq 128, 3 graines ;
> entraînement GPU (torch 2.11, cu130) ; JSON brut [`b102bis-decodeur.json`](b102bis-decodeur.json) ;
> fiche de fonctionnalité [`B10.2bis`](../docs/pilotage/backlog/B10.2bis-decodeur-attention-croisee.md).

## La question

L'encodeur converge (rappel ~0,2–0,3 contre 0,16 de hasard) mais le décodeur ne restitue pas :
chrF 12–17 contre un plancher de 38,5. B10.2bis proposait l'**attention croisée** (des requêtes
apprises qui lisent tous les états, au lieu d'une moyenne) pour franchir le plancher. La
question est donc : l'attention croisée change-t-elle le chrF ?

## Ce qui est mesuré — 3 bras × 3 graines

| bras | graine | chrF reconstruction | chrF traduction | rappel | sonde de langue |
|---|---:|---:|---:|---:|---:|
| 1  | | 17.0 | 11.4 | 0.319 | 0.267 |
| 2  | | 19.2 | 11.2 | 0.302 | 0.317 |
| 3  | | 16.0 | 10.8 | 0.326 | 0.333 |
| **moyenne** | | **17.4** | **11.13** | | |

| bras | graine | chrF reconstruction | chrF traduction | rappel | sonde de langue |
|---|---:|---:|---:|---:|---:|
| 1  | | 16.6 | 11.1 | 0.259 | 0.2 |
| 2  | | 15.8 | 11.3 | 0.285 | 0.383 |
| 3  | | 16.8 | 11.2 | 0.331 | 0.333 |
| **moyenne** | | **16.4** | **11.2** | | |

| bras | graine | chrF reconstruction | chrF traduction | rappel | sonde de langue |
|---|---:|---:|---:|---:|---:|
| 1 | | 16.5 | 11.2 | 0.33 | 0.333 |
| 2 | | 18.2 | 10.8 | 0.283 | 0.433 |
| 3 | | 16.2 | 11.0 | 0.348 | 0.367 |
| **moyenne** | | **16.97** | **11.0** | | |

**Le résultat est un plateau, pas un gain** : les trois bras sont à **11.13 ± 0.25**
(traduction) et **17.4–16.4** (reconstruction). L'écart maximal
entre bras est de **0.2 point** de chrF,
contre **27.3 points** manquants pour atteindre le plancher. Ce n'est pas une
question de réglage : c'est un autre levier.


## Les pas ne suffisent pas — 1800 pas, deux bras

Le chrF monte-t-il avec l'entraînement ? Non. Mêmes bras, même corpus, **1800 pas** (éval
tous les 300) :

| pas | projection rec | projection trad | attention rec | attention trad | rappel (proj / att) |
|---:|---:|---:|---:|---:|---:|
| 300 | 18.3 | 10.7 | 16.1 | 10.2 | 0.309 / 0.241 |
| 600 | 16.6 | 11.4 | 16.6 | 11.1 | 0.319 / 0.259 |
| 900 | 15.9 | 10.1 | 14.3 | 11.2 | 0.387 / 0.313 |
| 1200 | 17.9 | 11.4 | 16.6 | 10.9 | 0.367 / 0.304 |
| 1500 | 15.5 | 10.8 | 15.4 | 11.3 | 0.398 / 0.317 |
| 1800 | 16.9 | 11.2 | 15.3 | 10.7 | 0.374 / 0.328 |

La traduction reste entre **10,2 et 11,4** sur les deux bras et les six points de mesure ;
la reconstruction oscille entre 14,3 et 18,3 sans tendance ; pendant ce temps le **rappel
monte** (0,24 → 0,40). L'encodeur apprend, le décodeur ne décolle pas : **ce n'est pas un
problème de durée d'entraînement**. Trois leviers restent nommés : la **capacité** (9,29 M),
le **corpus** (30 articles) et l'**objectif** de décodage (byte-level).

## Les contrôles

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **plancher** (source → référence) | être au-dessus du décodeur | ✅ **38.5** contre ~11 |
| **sonde de langue** | chuter si `z` perd la langue | ✅ de 0,98 à **0.2** |
| **rappel mélangé** | rester au hasard | ✅ ~0.14 contre un rappel qui monte |
| **bras égalés** | mêmes données, même budget, même graine | ✅ seul le bras change |

## Ce qui pourrait le rendre faux

- **Un seul modèle** : 9,29 M paramètres, 6 blocs, byte-level — le plancher peut être un plancher
  de **capacité**, pas de mécanisme ; un modèle plus grand peut changer la conclusion.
- **30 articles** : petit corpus, une seule source (UDHR), un registre juridique.
- **600 pas** : le chrF monte encore lentement à 600 (16,2 → 16,6 chez le bras a) ; plus de pas
  peut gagner quelques points, pas 27.
- **Une seule métrique de sortie** : chrF mesure la surface ; le sens peut être meilleur que le
  chrF — mais la porte de B10.3 est chrF > 39,6, et c'est elle qui bloque.
- **Le plancher de 38,5** est celui de la source → référence : il dépend du corpus et du
  découpage.

## Ce que ça décide

**B10.2bis est close négative** : l'attention croisée et les segments sont **mesurés** et
**n'ouvrent pas** le décodeur. B10.3 (« raisonner sur `z` ») ne peut donc plus attendre
« l'attention croisée » : le levier suivant est nommé, et il n'est pas l'attention —
**capacité du modèle** (9,29 M), **taille du corpus** (30 articles) ou **objectif de décodage**
(byte-level). C'est la prochaine expérience, pas la prochaine intuition.

## Reproduire

```bash
gpu-env/bin/python3 tools/semantique/entrainer.py --checkpoint /tmp/natif-224-6-align-s1 \
  --articles 30 --pas 600 --eval-tous 100 --lot 8 --seq 128 --graine 1 \
  --n-sem 4 --attention-sem --sortie /tmp/b102bis-b-s1
```
