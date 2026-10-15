# N5 — la mémoire de travail : le réseau ne l'APPREND pas, la structure la donne (+0,96 contre −2,77)

> Campagne : **cerveau** · expérience : N5 (« le modèle n'a aucune mémoire d'un signal injecté »),
> et la suite que la fiche du 13/10 appelait : **un entraînement**.
> Question : le réseau peut-il **apprendre** à retenir un scalaire injecté 8 pas plus tôt — ou
> faut-il une **structure** ? Et si structure il faut, laquelle est la plus efficiente ?
> Verdict : **la structure.** Entraîné huit époques (LoRA rang 8 sur les 24 couches, 4 séquences de
> 2 048 pas, objectif « retrouver `v[t−8]` »), le réseau **n'apprend pas** : R² **−1,091 → −2,773**
> (le contrôle à cibles mélangées est à **−2,855** : l'entraîné ne fait pas mieux que le hasard).
> Avec le **tampon** (`--entree-memoire 8`, le passé écrit dans un canal), le modèle **gelé** lit
> déjà `v[t−8]` à **+0,879** et l'entraînement le porte à **+0,964** — et le moteur, mesuré par
> l'outil de la campagne, rend **+0,766** (non linéaire) contre **−0,493** sans tampon. Le présent
> reste lisible partout (**+0,99**), le témoin avenir reste négatif : le protocole ne fuit pas.
> Date réelle : **2026-10-14 22 h 35-23 h 05 HAE** (heure lue sur la machine)
> Protocole : `tools/memoire_travail.py` (nouveau) — un jeton de base fixe, le signal
> `v[t] ~ U(−2,2)` posé sur le canal 0 de l'embarquement (`--entree signal:F --entree-canal 0
> --entree-gain 1 --recurent`), sonde **ridge** apprise sur la **première moitié** d'une séquence
> et mesurée sur la **seconde** (le protocole de `reports/rapport-c8-peripherie.md` § 2 bis).
> Vérification moteur : `drave --entree … --recurent [--entree-memoire 8]` puis
> `tools/peripherie_memoire.py` (l'outil de la campagne, inchangé).

## 1. Le plan 2×2, et il est net

| | **sans tampon** (le réseau doit retenir) | **avec tampon** (le passé est dans l'entrée) |
|---|---:|---:|
| **gelé** (sonde seule) | **−1,091** | **+0,879** |
| **entraîné** (LoRA + sonde) | **−2,773** | **+0,964** |
| contrôle : cibles mélangées | −2,855 | −0,887 |
| *référence : tampon lu directement (moteur)* | — | ***1,000*** (zéro paire) |

Ce que ça dit, et c'est la réponse à N5 :

* **sans structure, l'entraînement ne crée pas la mémoire** : la sonde entraînée tombe **sous** le
  niveau du hasard (−2,773 contre −2,855 pour les cibles mélangées), et le témoin « présent » reste
  à +0,993 — donc le modèle n'est pas cassé, il n'a simplement **rien** à lire du passé ;
* **avec la structure, le passé est lisible sans entraîner le réseau** (+0,879) : le tampon écrit
  `v[t−8]` dans un canal, et l'état le porte. L'entraînement **améliore la lecture** (+0,964) —
  c'est un apprentissage de *lecture*, pas de *mémoire* ;
* **le témoin avenir reste négatif dans les deux cas** (−2,549 et −1,725) : la sonde ne devine pas,
  elle lit ce qui est là ;
* **et le tampon lu directement vaut 1,000 pour zéro paire** (moteur) : aucune des deux variantes
  entraînées ne bat une structure gratuite.

## 2. Ce que le moteur confirme, et où il ne suit pas

Même signal (2 048 pas de bruit), mêmes canaux, l'outil de la campagne sur les états du moteur :

| cible | lecture | sans tampon | avec tampon (`--entree-memoire 8`) |
|---|---|---:|---:|
| `v[t]` (présent) | linéaire | +0,962 | +0,787 |
| `v[t]` (présent) | non linéaire | +0,988 | +0,935 |
| `v[t−8]` (mémoire) | linéaire | −2,879 | −0,338 |
| `v[t−8]` (mémoire) | **non linéaire** | **−0,493** | **+0,766** |
| `v[t+1]` (témoin) | non linéaire | −0,864 | −0,655 |

* **le désaccord est dit, pas caché** : sur le bras *avec tampon*, torch lit la mémoire à
  **+0,879 en linéaire** et le moteur à **−0,338 en linéaire / +0,766 en non linéaire**. Les deux
  disent la même **direction** (le passé devient lisible quand la structure est là), pas le même
  **degré**. La cause n'est pas instruite — deux différences connues : le jeton de base (0 dans le
  moteur, 220 ici) et la quantification Q8_0 du moteur. C'est écrit comme un écart à instruire,
  pas comme un accord ;
* **sur le bras *sans* tampon, les deux plateformes concordent** : mémoire illisible (−2,879 moteur,
  −1,091 torch) et présent lisible (+0,96-0,99 des deux côtés) — c'est le résultat qui porte la
  conclusion ;
* les chiffres publiés du 13/10 sont **reproduits** : présent +0,962/+0,988 (publié +0,982/+0,992),
  mémoire −2,879/−0,493 (publié −0,611/−0,681). Même régime, mêmes conclusions.

## 3. Ce que ça change pour le cerveau

* **la mémoire de travail est une STRUCTURE, pas un entraînement** : c'est le troisième résultat de
  ce dépôt qui va dans ce sens (la récurrence locale dégrade — « un écho, pas une mémoire » ; la
  récurrence linéaire de 64 canaux plafonne à +0,104 ; ici, l'entraînement du réseau échoue), et il
  est maintenant **mesuré contre un entraînement**, pas seulement contre une sonde ;
* **le mécanisme le plus efficient pour cette faculté reste le tampon** : R² 1,000, **zéro paire**,
  aucune époque d'entraînement, borné (`--memoire K`), et il refuse de déborder du modèle (code 2).
  Un LoRA entraîné pour lire ce tampon apporte **+0,085** de R² (0,879 → 0,964) au prix de 1,4 M de
  paramètres et de 8 époques : le rapport est défavorable, et c'est chiffré ;
* **ce qui reste vrai** : le réseau *peut* apprendre à **lire** une structure (0,879 → 0,964), donc
  la faculté « lire sa propre mémoire » existe ; c'est « être la mémoire » qui n'existe pas.

## 4. Ce que cette fiche ne dit pas

* **un seul k** (8 pas), **un seul canal** (0), **un seul budget** d'entraînement (8 époques,
  4 séquences de 2 048 pas) : un k plus court (1-2 pas) serait peut-être appris — c'est la courbe
  qui manque, et elle est facile ;
* **un seul rang de LoRA** (8) et une seule profondeur (les 24 couches) : la rétropropagation
  traverse tout le modèle ; un LoRA sur les dernières couches seulement n'est pas mesuré ;
* **l'écart torch/moteur du § 2 n'est pas instruit** : il est nommé avec ses deux différences
  connues, et il ne change pas la conclusion — mais il devrait être tranché avant de citer un
  chiffre au dixième ;
* **rien n'est mesuré en génération** : la faculté est mesurée comme une *lecture* (R² d'une sonde),
  pas comme un comportement ;
* **la mémoire de travail du modèle n'est pas testée sur une tâche** : le plan (§ C8) demande une
  **tâche fermée** (poursuite d'un signal) — elle est résolue par le tampon lu directement
  (R² 1,000, `reports/rapport-c8-peripherie.md` § 2 quinquies), pas par un réseau entraîné.
