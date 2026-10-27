# Le protocole sémantique natif — rejouer, converger, puis parler

> **Ce que ce document est.** Le protocole qui remplace l'enchaînement « surface → professeur → distillation »
> par un entraînement **auto-supervisé** du modèle natif : on **rejoue** le même sens dans plusieurs langues
> jusqu'à ce que l'embedding sémantique **converge**, on entraîne **simultanément** la sortie **sens → texte**,
> et on ne branche le **raisonnement** qu'après, sur un embedding **gelé**. Les résultats sont dans
> [`reports/rapport-semantique.md`](../reports/rapport-semantique.md) ; le code dans [`tools/semantique`](../tools/semantique/).

## Pourquoi ce protocole

Les étapes B5–B9 ont appris une chose : un modèle natif peut apprendre une **distribution de réponses** sans
apprendre le **sens**. La distillation par séquences, même avec 610 exemples et 31,63 M paramètres, donne un
écart relatif réel (4,40 %) mais **transitoire** : à 1 000 pas, le contrôle repasse, et à 30 langues l'effet se
dilue. Ce n'est pas un problème de données seulement : c'est un problème de **protocole**.

Le protocole sémantique change l'objectif :

1. **Le même sens, plusieurs surfaces.** Un article de l'UDHR existe dans 10, 20 ou 30 langues. Le modèle doit
   produire le **même `z`** pour toutes les versions, et **reconstruire** chaque version depuis `z`.
2. **Le sens est un goulot, pas une couche.** `z` est de dimension petite (128), normalisé ; le décodeur ne
   reçoit que `z` et la **langue cible**. La langue est dans le décodeur, jamais dans `z`.
3. **La convergence se mesure.** On n'arrête pas sur la perte : on arrête quand le **rappel parallèle** ne
   progresse plus, que la **sonde de langue** ne baisse plus, et que la **traduction** ne s'améliore plus.
4. **Le raisonnement attend.** Tant que `z` n'est pas stable, il n'y a rien à raisonner : un embedding qui
   change avec la langue ne porte pas le sens, il porte la surface.

## Les trois étages

```
surface L1 ──► encodeur ──► z ──► décodeur + langue L2 ──► surface L2
                  ▲                    ▲
                  │                    │
             même article          même z, autre langue
```

### Étage 1 — rejouer et converger

- **corpus** : UDHR, articles 1–30, langues parallèles ; découpage **par article** (train 1–24, val 25–30) ;
  jamais par phrase — une phrase d'un article de validation ne doit pas fuiter.
- **encodeur** : `route` lit les octets ; `z` est la moyenne des états cachés (mean pooling) projetée en 128
  dimensions et normalisée. Le mean pooling est le défaut : le dernier octet d'un article tronqué ne voit que
  sa fin, et deux articles différents se ressemblent (leçon du premier passage).
- **décodeur** : `z` devient `k = 4` préfixes doux + un **jeton de langue cible** ; le même `route` génère la
  surface cible. La langue est dans le décodeur, pas dans `z`.
- **pertes** :
  - **reconstruction** : `z` de la langue L → texte L ;
  - **traduction** : `z` de L → texte L' ;
  - **alignement** : `1 − cos(z_L, z_L')` pour le même article — **poids faible**, sinon collapse ;
  - **contrastive (InfoNCE)** : dans le lot, la paire parallèle doit être plus proche que les autres articles —
    c'est ce qui rend `z` **discriminant**, pas seulement aligné ;
  - **adversaire de langue** : un classifieur de langue sur `z` avec **gradient inversé** ; `z` doit rester
    neutre. La sonde de langue est le contrôle.
- **convergence** : arrêt quand le **rappel parallèle** plafonne (patience 3 évaluations), avec la sonde, le
  rappel mélangé et le chrF comme garde-fous. La perte seule ne suffit pas : elle peut baisser en collapse.

### Étage 2 — sens → texte

Le décodeur est déjà entraîné à l'étage 1. On mesure :

- **reconstruction** : `z` de L → L (la référence est le texte L) ;
- **traduction** : `z` de L → L' (la référence est la traduction humaine) ;
- **plancher** : `chrF(surface L, surface L')` — le même texte sans traduction ; sans lui, un chrF de 20 ne dit
  rien ;
- **écart** : traduction − reconstruction, par langue ; c'est l'écart que l'étage 2 devra réduire.

### Étage 3 — raisonner sur `z` gelé

On **gèle** l'encodeur et on branche un petit opérateur (linéaire, MLP, ou un bloc classique) sur `z` :

- **jeux** : prédire la légalité d'un coup, le résultat, ou la RSN d'une surface (B5/B6) ;
- **langue** : prédire une opération (négation, ordre, comparaison) sur des paires parallèles ;
- **contrôle** : le même opérateur sur les **surfaces** (sans `z`) doit faire moins bien, et l'opérateur sur
  `z` doit être **invariant** quand on change la langue d'entrée.

Tant que l'étage 1 n'est pas stable, l'étage 3 ne mesure que la surface : on ne le branche pas.

## Les acquis réutilisés (B5–B9)

| acquis | ce qu'il devient dans le protocole |
|---|---|
| **RSN-jeu** (B5/B6) | la cible de l'étage 3 : un `z` doit retrouver la RSN d'une surface, pas la surface |
| **71 langues** (B7) | le corpus de rejeu ; les libellés sont des faits, pas des tokens |
| **maîtres** (B8) | les principes sont une **entrée** du raisonnement, pas une force |
| **natif 31,63 M / 610** (B9) | le point de départ : capacité et données se paient ensemble |
| **fenêtre 500/750/1 000** (B9) | la convergence remplace la fenêtre : on s'arrête sur le rappel, pas sur le pas |
| **masque, plancher, permutation** (B9) | les contrôles : plancher chrF, rappel mélangé, sonde de langue |

## Les contrôles négatifs

- **rappel mélangé** : les articles sont permutés dans la langue cible ; le rappel doit tomber au hasard ;
- **sonde de langue** : un classifieur linéaire sur `z` ; si elle reste haute, `z` n'est pas neutre ;
- **plancher chrF** : la surface source contre la référence cible, sans traduction ;
- **collapse** : si `z` est constant, l'alignement est parfait et le rappel au hasard — c'est le premier piège,
  et il est arrivé au premier passage (alignement 0,98, rappel 0,18) ;
- **découpage par article** : aucune phrase de validation dans l'entraînement ;
- **split de langue** : entraîner sans une langue, la tester ; le `z` doit tenter de transférer, et l'échec est
  nommé.

## Ce qui rendrait le protocole faux

- le rappel reste au hasard alors que la reconstruction marche → `z` n'est pas un sens partagé ;
- la sonde de langue reste haute → `z` porte la langue ;
- la traduction ne dépasse pas le plancher → le décodeur n'utilise pas `z` ;
- la convergence n'arrive qu'en collapse → les contrôles le disent ;
- l'étage 3 sur `z` ne bat pas la surface → le sens n'est pas exploitable pour le raisonnement.

## La distribution du travail

Le protocole est **parallèle par construction** :

- **deux GPU** : un pour 10 langues, un pour 20 langues (ou deux variantes : mean/last, avec/sans adversaire) ;
- **batch 16, seq 384** : le GPU est à ~95 %, la mémoire à ~15 Go par carte ; le CPU ne fait qu'un fil par
  processus, ce qui est le bon ratio pour ce modèle ;
- **évaluation batchée** : les 12 générations de validation partent en un seul `generate`, pas en boucle ;
- **deux résultats** : le 10 langues et le 20 langues se comparent à protocole constant, pas à données
  différentes.

## Où vit le code

| module | rôle |
|---|---|
| [`tools/semantique/corpus.py`](../tools/semantique/corpus.py) | articles parallèles, découpage par article, octets |
| [`tools/semantique/modele.py`](../tools/semantique/modele.py) | encodeur `route`, tête `z`, préfixe, décodeur, adversaire |
| [`tools/semantique/entrainer.py`](../tools/semantique/entrainer.py) | pertes, convergence, rappel, sonde, chrF, JSON |
| [`tools/semantique/tests/`](../tools/semantique/tests/) | le corpus et le découpage |

## Le premier passage (26/10)

Le protocole a été exécuté sur **10 langues**, deux GPU NVLink, `route` 31,63 M. Deux résultats :

- **l'encodeur converge** : rappel parallèle **0,426** contre **0,167** de hasard, contrôle mélangé
  **0,172**, sonde de langue **0,100** (hasard 1/10) au pas 250 ;
- **le décodeur ne suit pas** : chrF reconstruction **12,7**, traduction **5,3–7,8**, plancher **39,6** ;
  le diagnostic multilingue est **sous le plancher** (diagonale 7,3, hors diagonale 6,3, plancher 12,6),
  avec une sensibilité à la source de **0,704**.

Les **ablations** confirment le diagnostic : `z` de 512 dims **dégrade** le rappel (0,278), un préfixe de
64 ne fait pas mieux que 16 (12,4 / 6,7), le décodeur **utilise** `z` (5,84 avec, 2,52 sans) mais `z` ne
porte que l'identité de l'article, et **8 unités linéaires moyennées** diluent le rappel (0,237). Le prochain
levier est donc une **attention de requêtes** sur les états (chaque unité lit des positions différentes), ou
une **attention croisée** du décodeur — pas un vecteur plus gros, un préfixe plus long ou une moyenne d'unités.

Le premier passage a corrigé trois choses dans le protocole : l'**all-gather détaché** (la contrastive ne
touchait pas `z`), les **gradients du décodeur** (ils écrasent l'encodeur : étages séparés), et les
**articles du lot global** (les mêmes articles sur les deux rangs annulaient la contrastive). Le décodeur
doit maintenant passer à une **attention croisée** ou à un entraînement plus long ; le raisonnement sur
`z` n'est **pas** branché. Détail : [`rapport-semantique.md`](../reports/rapport-semantique.md).

## Ce qui reste ouvert

- **la taille de `z`** : 128 est un choix de départ ; la courbe 32/64/128/256 dira où le sens sature ;
- **le nombre de préfixes** : 4 ; la courbe 1/2/4/8 ;
- **l'adversaire** : 0,5 ; trop fort, il détruit le sens ; trop faible, la langue reste ;
- **la convergence** : le rappel à 6 articles de validation est grossier ; il faudra 20–30 articles ;
- **le raisonnement** : l'étage 3 n'est pas encore branché ; c'est la prochaine mesure après la convergence.
