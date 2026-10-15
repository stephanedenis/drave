# Où dépenser le budget d'attention — uniforme ou sur la moitié des couches ? (second ordre)

> Campagne : **cerveau** · expérience : l'**allocation** du budget de clés, à budget **égal**.
> Question : quand on ne garde qu'une fraction des clés, vaut-il mieux **répartir** la réduction
> sur toutes les couches, ou **spécialiser** — fenêtre étroite sur la moitié des couches, attention
> complète sur l'autre moitié ? (Le dépôt a mesuré *combien* de clés garder, `N/2` ou `N/4` —
> `rapport-loi-frontiere-fenetre.md` — jamais **où**, et `--swa-pattern` permet exactement cela.)
> Verdict : **l'allocation est un levier de SECOND ordre, et son signe dépend du texte.**
> À clés **égales** (9 216 par couche en moyenne, ctx 512) : sur m32 l'alterné **bat** l'uniforme
> (9,6110 contre 9,6624, et même contre le **complet** 9,6503) ; sur m20 il **perd** (15,6744 contre
> 15,4227). L'écart entre les deux allocations (0,5 à 1 point) est du même ordre que la variabilité
> entre textes que ce dépôt mesure partout — alors que le **volume** de clés, lui, pèse bien plus
> (fenêtre 256 contre complète : +0,50 % sur m32 et **+3,85 %** sur m20).
> Date réelle : **2026-10-14 23 h 50-00 h 10 HAE** (heure lue sur la machine)
> Protocole : `drave --ppl <morceau> --limit 512 --ctx 512 --threads 8` · quatre configurations,
> **64 puits** dans toutes · morceaux m32 et m20 · clés = `fenêtre` sur toutes les couches, ou
> `fenêtre` sur les couches paires (motif 2) et **complètes** sur les impaires.

## 1. Les chiffres

| configuration | clés par couche (moyenne) | m32 | écart au complet | m20 | écart au complet |
|---|---:|---:|---:|---:|---:|
| **complet** (fenêtre 512) | 512 | 9,6503 | — | 15,4418 | — |
| **uniforme 384** | 384 | 9,6624 | +0,13 % | 15,4227 | −0,12 % |
| **alterné 256** (motif 2 : 256 sur 12 couches, 512 sur 12) | **384** | **9,6110** | **−0,41 %** | 15,6744 | +1,51 % |
| uniforme 256 | 256 | 9,6990 | +0,50 % | 16,0361 | +3,85 % |
| alterné 128 (motif 2) | 320 | 9,7651 | +1,19 % | 15,9440 | +3,25 % |

Ce que ça dit :

* **à clés égales, les deux allocations se disputent le point** : l'alterné gagne sur m32 de
  **0,53 %** (9,6110 contre 9,6624) et perd sur m20 de **1,63 %** (15,6744 contre 15,4227). Aucune
  des deux n'est « la bonne » — et c'est cohérent avec tout ce que ce dépôt mesure sur la fenêtre
  (la dispersion dépend du texte *et* de N) ;
* **le volume, lui, est un levier de premier ordre** : passer de 512 à 256 clés coûte **+0,50 %**
  sur m32 mais **+3,85 %** sur m20 — et c'est **le même ordre** que ce que la fiche de la loi de
  frontière annonçait (la moitié des clés : +0,4 à +3,0 % selon le texte) ;
* **surprise agréable, et elle est petite** : sur m32, l'alterné à 384 clés bat le **complet**
  (−0,41 %). Un modèle qui n'attend pas partout peut donc être *meilleur* — mais c'est **un texte**,
  et la fiche le dit comme tel ;
* **la conséquence pratique** : il n'y a pas de « bon endroit » universel où dépenser ; il y a un
  **budget** à tenir (la moitié des clés, ~1 % en moyenne) et une **liberté d'implémentation** sur
  la répartition. C'est la même conclusion que la fiche du 13/10 pour le partage fenêtre/puits
  (« un paramètre d'implémentation, pas de qualité »), étendue aux **couches**.

## 2. Ce que cette fiche ne dit pas

* **deux morceaux, une longueur** (512 jetons) : la fiche de la loi de frontière a montré que N
  change la donne ; ici, un seul N ;
* **un seul motif** (2 : une couche sur deux) et un seul jeu de puits (64) : les motifs 4 et 8, et
  le nombre de puits, ne sont pas balayés — or les puits portent le début de séquence, et leur
  nombre change la qualité (`rapport-fenetre-puits-attention.md`) ;
* **rien n'est mesuré en temps** : l'alterné ne coûte pas moins cher que l'uniforme à clés égales,
  mais les deux devraient coûter moins qu'une attention complète — ce n'est pas vérifié ici ;
* **rien sur le modèle entraîné** : ces mesures sont sur un modèle **gelé** ; un modèle entraîné
  *avec* le motif alterné (comme Gemma) n'est pas mesurable sans entraînement.
