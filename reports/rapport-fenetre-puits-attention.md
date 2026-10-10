# Fenêtre d'attention × puits : jusqu'où la fenêtre est-elle gratuite ?

> Campagne : **cerveau complet** · expérience : fenêtre × puits
> Question : existe-t-il un couple (fenêtre, nombre de puits d'attention) qui **approche
> l'attention complète** en ne notant qu'une **fraction** des clés ? Les scores d'attention sont
> le poste dominant : la fenêtre les rend `O(W)` au lieu de `O(N)` — mais elle coûte en qualité,
> et la question est de savoir si le **drain** (les `n` premiers jetons, toujours notés) paie ce
> coût.
> Verdict : **oui, à condition que le drain GRANDISSE avec la séquence.**
> À 512 jetons, **fenêtre 128 + 64 puits** rend **13,3968** contre **13,1368** (**+2,0 %**) pour
> **192 clés sur 512** (**÷2,67**). À 2 048 jetons, **fenêtre 512 + 128 puits** coûte **+40,3 %**
> — mais **fenêtre 512 + 512 puits** rend **10,4046** contre **10,3703** (**+0,33 %**) pour
> **1 024 clés** (**÷2**), et **fenêtre 1 024 + 128 puits** rend même **10,3652**, très
> légèrement **mieux** que l'attention complète, pour **÷1,78**. Le drain n'est pas un petit
> supplément : c'est lui qui porte la qualité, et il doit suivre la séquence. **Zéro puits avec
> une fenêtre casse le modèle** (1297,54 contre 29,02 à fenêtre 32).
> Date réelle : **2026-10-10 10:18 HAE** (les journaux et commits de ce round ; `date` sur la
> machine, pas une horloge supposée).
> Protocole : `tools/carte-fenetre-puits.sh <limit>` — Qwen2.5-0.5B-Q8_0,
> `ids` = `/tmp/campagne24/ids_0.5B-Q8.txt`, `--ctx 512`, `--threads 8`, perplexité déterministe.

## 1. Pourquoi ce n'est pas une question de réglage, mais de mécanisme

`--attn-sinks N` **n'était pas un drapeau mort** (voir la fiche 50 de la campagne) : sous une
fenêtre, les `n` premiers jetons restent **notés** (`model.rs:7472`), et **zéro puits casse le
modèle** — 0 puits à fenêtre 32 : **1297,5437** contre **29,0206** à 4 puits (×45). Une attention
à fenêtre **sans drain** ne perd pas un peu de qualité : elle s'effondre. C'est ce qui rend la
question ci-dessus légitime — le drain est **porteur**, pas décoratif.

## 2. La carte, à 128 jetons (fenêtre 32 = un quart de la séquence)

| fenêtre \ puits | 0 | 8 | 16 | 24 | 32 |
|---|---|---|---|---|---|
| **16** | 23,8917 | 23,1946 | 20,7664 | 16,3487 | **16,2566** |
| **32** | 18,1141 | 16,9511 | 16,3812 | **15,4339** | 15,4499 |
| **64** | 16,1972 | 15,5128 | 15,3427 | 14,9614 | **14,8530** |

Référence **sans fenêtre : 14,6496**. Déjà visible : **un gros drain compense une petite
fenêtre** (16 de fenêtre + 32 puits = 16,2566 ≈ 64 de fenêtre + 0 puits = 16,1972).

## 3. La carte qui décide, à 512 jetons (le régime qui compte)

| fenêtre \ puits | 0 | 32 | 64 | clés notées / jeton | prix vs complet |
|---|---|---|---|---|---|
| **64** | 21,5801 | 16,2652 | 14,4247 | 128 | ÷4 |
| **128** | 17,2481 | 14,7484 | **13,3968** | 192 | **÷2,67** |
| **256** | 16,6749 | 14,6262 | 13,4778 | 320 | ÷1,6 |
| **aucune** | **13,1368** | — | — | 512 | — |

**Le résultat cherché est dans la case 128 × 64 : +2,0 % de perplexité pour ÷2,67 de clés
notées.** Et la fenêtre n'est pas seulement « moins chère » : avec le même drain de 64, la
fenêtre **128 bat la 256** (13,3968 contre 13,4778) — une non-monotonie de 0,6 % qu'il faut
**confirmer** (elle peut être du bruit de corpus sur 512 jetons ; elle est dans le bon sens).

## 4. La pente en N : le drain ne compense plus quand la séquence grandit

Les deux cartes ci-dessus sont à 128 et 512 jetons. La troisième, à **2 048 jetons** (`--ctx 2048`,
mêmes ids, même modèle), répond à la question qui décide de l'usage réel :

| fenêtre \ puits | 0 | 64 | 128 | clés / jeton | prix vs complet |
|---|---|---|---|---|---|
| **128** | 20,6093 | 17,6891 | 16,4784 | 256 | ÷8 |
| **256** | 18,4229 | 16,4944 | 15,5281 | 384 | ÷5,3 |
| **512** | 15,4711 | 15,0810 | **14,5531** | 640 | **÷3,2** |
| **aucune** | **10,3703** | — | — | 2 048 | — |

**La synthèse, à taux de clés comparable :**

| N | attention complète | meilleure case | clés | prix |
|---|---|---|---|---|
| 128 | 14,6496 | 64 + 24 puits | 88 (**69 %**) | **+2,1 %** |
| 512 | 13,1368 | 128 + 64 puits | 192 (**37,5 %**) | **+2,0 %** |
| 2 048 | 10,3703 | 512 + 128 puits | 640 (**31 %**) | **+40,3 %** |

**Le fait, et il est net : à 31 % des clés notées, on paie +2,0 % à 512 jetons et +40,3 % à
2 048.** Ce n'est donc pas le *nombre* de clés qui décide, c'est **ce qu'on ne voit plus** : à
2 048 jetons, une fenêtre de 512 laisse 1 536 jetons accessibles seulement par les 128 puits, et
les puits ne portent pas l'information — ils drainent l'attention, ils ne la remplacent pas.

**LA CONCLUSION CI-DESSUS ÉTAIT TROP FORTE, ET ELLE EST CORRIGÉE AU § 5.** Elle était **bornée par
la grille mesurée** : à 2 048 jetons, la grille ci-dessus ne montait qu'à **128 puits**. Dire
« le drain ne compense plus » à partir de là revient à conclure sur le drain en n'ayant essayé
que ses petites valeurs — la même erreur de méthode que mesurer l'inertie d'un drapeau là où
l'inertie est attendue (fiche 50). La grille étendue (§ 5) montre l'inverse.

## 5. La frontière à 2 048 jetons : c'est le DRAIN qui porte la qualité

La grille du § 4 plafonnait à 128 puits. Étendue jusqu'à **512 puits** (fenêtre 512 et 1 024),
mêmes conditions (`--ctx 2048`, mêmes ids) :

| fenêtre \ puits | 128 | 256 | 512 | clés / jeton | prix vs complet (10,3703) |
|---|---|---|---|---|---|
| **512** | 14,5531 | 12,6526 | **10,4046** | 1 024 | **+0,33 %** |
| **1 024** | **10,3652** | 10,3930 | 10,3699 | 1 152 | **−0,05 %** |

**Trois faits, et ils changent la conclusion :**

1. **le drain doit grandir avec la séquence.** À fenêtre 512, passer de 128 à 512 puits fait
   tomber la perplexité de **14,5531 à 10,4046** — c'est-à-dire de +40,3 % à **+0,33 %** ;
2. **on peut donc diviser par deux les clés notées à qualité quasi intacte** : (512 fenêtre,
   512 puits) = **1 024 clés sur 2 048** (+0,33 %) ; et (1 024, 128) = 1 152 clés pour **−0,05 %**
   (à l'intérieur du bruit, mais pas pire) ;
3. **le meilleur prix n'est pas la plus grande fenêtre** : à budget de clés voisin, (512, 512)
   coûte moins cher que (1 024, 128) pour une qualité comparable — **le drain est le levier le
   moins cher des deux**.

**Ce que ça veut dire pour le moteur** : une attention « fenêtre + préfixe » (les `n` premiers
jetons toujours notés) conserve la qualité à longue portée **à condition de garder un préfixe
substantiel** — de l'ordre de la fenêtre, pas de quelques jetons. C'est le mécanisme des
*attention sinks*, mais à l'échelle : quelques puits suffisent à drainer, il en faut beaucoup
plus pour **porter l'information du début de séquence**.

**À 4 096 jetons** (mêmes conditions, `--ctx 4096`), la référence d'attention complète vaut
**12,2177** :

| fenêtre \ puits | 512 | 1 024 | clés / jeton | prix vs complet |
|---|---|---|---|---|
| **512** | 12,8824 | 12,7884 | 1 024 / 1 536 | +5,4 % / +4,7 % |
| **1 024** | 12,4875 | **12,4466** | 1 536 / 2 048 | +2,2 % / **+1,9 %** |

La règle « préfixe ≈ fenêtre » **ne suffit plus** : elle donnait +0,33 % à 2 048, elle donne
**+5,4 %** à 4 096. Ce qui tient, en revanche, c'est **de garder la moitié des clés** : (1 024,
1 024) — la moitié récente en fenêtre, la moitié ancienne en préfixe — coûte **+1,9 %** à
4 096, et (512, 512) coûtait +0,33 % à 2 048 et +2,0 % à 512. **La frontière se déplace avec N,
et le prix croît avec N à fraction de clés constante.**

**Ce qui reste ouvert** : la **loi** de cette frontière (faut-il `N/2` clés à toute longueur, ou
la fraction utile diminue-t-elle ?), et le **gain de temps réel** — la carte rend désormais
aussi les secondes et les tok/s, parce que la fenêtre ne réduit que les scores d'attention, un
poste parmi d'autres (la FFN domine) : le gain de temps est toujours plus petit que le gain de
clés, et il se mesure.

## 6. Le prix RÉEL en temps : la fenêtre est un levier de CLÉS, pas de vitesse

La qualité ne suffit pas à décider : un levier qui divise les clés par quatre ne divise le temps
que si l'attention dominait. Mesure directe, même protocole, **débit** (`tok/s` de la passe
complète sur 4 096 jetons, une mesure par case, machine au repos) :

| configuration | perplexité | clés / jeton | **tok/s** | vs attention complète |
|---|---|---|---|---|
| attention complète | 12,2177 | 4 096 | **17,1** | — |
| fenêtre 512 + 512 puits | 12,8824 | 1 024 (**÷4**) | **19,1** | **+12 %** |
| fenêtre 512 + 1 024 puits | 12,7884 | 1 536 (÷2,67) | 17,3 | +1 % |
| fenêtre 1 024 + 512 puits | 12,4875 | 1 536 (÷2,67) | 17,4 | +2 % |
| fenêtre 1 024 + 1 024 puits | 12,4466 | 2 048 (÷2) | 16,0 | **−6 %** |

**Le fait, et il faut le dire ainsi : diviser les clés d'attention par quatre ne rend que
+12 % de débit**, et les configurations plus larges sont dans le bruit (l'une est même plus
lente). Ce n'est pas une surprise quand on regarde les postes : l'attention pèse **3,95 ms** sur
**33 ms** par jeton, la FFN en pèse 26 — et les puits ajoutent du travail dans le poste qu'on
réduit. **La fenêtre est donc un levier de PARCIMONIE (clés, paires, octets à transporter), pas
un levier de vitesse locale**, et c'est en réparti qu'elle compte : chaque clé non notée est une
paire non calculée sur le nœud et une activation non transportée.

**Ce qu'il faudrait pour en tirer du temps** : réduire aussi ce qui domine (la FFN), ou déporter
les scores — deux chantiers distincts, et aucun n'est la fenêtre.

## 7. Ce que ça ne dit pas (et qu'il faut mesurer)

- **la pente en N est mesurée jusqu'à 2 048** (§ 4 et § 5) : le drain **rachète** le prix quand
  il grandit avec la séquence. Reste **4 096 jetons** (mesure en cours) et la règle de
  dimensionnement à budget de clés fixé ;
- **le prix réel n'est pas dans le compteur de paires affiché** : à cette échelle il arrondit à
  `0,01 M`. Le prix est **analytique** (`fenêtre + puits` clés notées par jeton par couche),
  et c'est celui du tableau ;
- **le temps est maintenant mesuré** (§ 6) : ÷4 de clés = **+12 %** de débit, pas ×4 — l'attention
  est le second poste (3,95 ms sur 33 ms), la FFN domine ;
- **un modèle à fenêtre déclarée** (`swa_pattern` > 1, comme gpt-oss : une couche sur deux en
  attention complète) n'a pas été mesuré dans cette carte.

## 8. Protocole, pour rejouer

```bash
FENETRES="64 128 256" PUITS="0 32 64" tools/carte-fenetre-puits.sh 512
tools/carte-fenetre-puits.sh 128          # la carte complète par défaut
```

Le script imprime la référence sans fenêtre, puis une ligne par fenêtre — chaque case est une
perplexité mesurée par le moteur, aucun chiffre interpolé.
