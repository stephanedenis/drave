# C4 — le prix d'un état en retard : **×633 pour UN pas**, et ce que ça impose à un ordonnanceur

> Campagne : **cerveau** · expérience : état d'une couche imposé avec k pas de retard
> Question : C4 demande l'**asynchronisme réel** — chaque région à son rythme, avec des horloges
> déclarées. Avant d'écrire un ordonnanceur, il faut savoir **ce que coûte un état qui arrive en
> retard**. Un pas ? Dix ? Rien ?
> Verdict : **un seul pas de retard multiplie la perplexité par 633** (14,6496 → 9 277,98 sur
> 128 jetons), deux pas par 4 087, et la dégradation sature vers ×10 000. **Un état n'est valide
> qu'à SA position** : ce n'est pas une question de précision, c'est une question d'identité.
> Conséquence pour C4 : l'asynchronisme ne peut pas vouloir dire « laisser un pas prendre du
> retard » — il peut seulement vouloir dire **réordonner À L'INTÉRIEUR d'un pas**, la position
> restant collée à l'état (c'est ce que le champ `pos` de l'en-tête transporte depuis le v6).
> Date réelle : **2026-10-10 17:18 HAE** (heure lue sur la machine).
> Protocole : `tools/c4_retard.sh` (une capture, six états décalés, six perplexités).

## 1. Les chiffres

| retard k | perplexité (128 jetons, couche 12) | prix |
|---|---|---|
| **0** (invariant : la coupe exacte) | **14,6496** | ×1 |
| **1** | **9 277,9771** | **×633** |
| 2 | 59 878,6885 | ×4 087 |
| 4 | 90 096,6419 | ×6 150 |
| 8 | 151 517,0001 | ×10 343 |
| 16 | 131 248,9897 | ×8 959 (saturation) |

**Trois lectures :**

1. **un pas de retard est déjà catastrophique** (×633) : l'état d'une position décrit *ce jeton-là*
   et son contexte ; le donner à la position suivante, c'est lui faire lire le monde d'avant ;
2. **la dégradation sature** (×10 000 vers 8-16 pas) : au-delà de quelques pas, l'état est
   simplement « faux », et la perplexité plafonne au niveau d'un modèle qui ne reçoit presque rien
   d'utile — le plateau est donc une information sur la *borne haute* du désastre, pas une
   amélioration ;
3. **la position n'est pas un détail d'implémentation, c'est une identité.** Le protocole transporte
   `pos` dans chaque trame (v6) et la réduction finale refuse un état d'une autre position — cette
   mesure dit **pourquoi**, et de combien.

## 1 bis. Périmé ou MANQUANT ? La politique d'un ordonnanceur est chiffrée

Un ordonnanceur asynchrone a trois choix quand un état n'est pas arrivé : **attendre**, **réutiliser
le dernier reçu** (donc un état d'une autre position), ou **continuer sans** (la position reste sans
état). Le prix des deux derniers est mesuré (128 jetons, couche 12 ; un état « manquant » est mis à
zéro, ce qui n'est pas neutre — c'est le plancher) :

| situation | perplexité | prix |
|---|---|---|
| modèle entier (référence) | 14,6496 | ×1 |
| **un état MANQUANT** (position 32 · 64 · 96) | 15,1529 · 15,5295 · 15,6291 | **×1,03 à ×1,07** |
| huit états manquants (un sur seize) | 52,7319 | ×3,6 |
| **un état PÉRIMÉ** (décalage d'un pas, sur toute la séquence) | 9 277,9771 | **×633** |
| tous les états manquants | 2 801 962,2714 | ×191 000 |

**La politique est donc tranchée par la mesure : on CONTINUE SANS, on ne réutilise JAMAIS.**
Réutiliser un état d'une autre position coûte ×633 ; le laisser manquant coûte ×1,05. Un
ordonnanceur qui « fait au mieux avec le dernier état reçu » se trompe de trois ordres de grandeur.

*(Le test « périmé » et le test « manquant » ne mesurent pas la même chose, et c'est voulu :
réutiliser, c'est **désaligner** toute la suite ; manquer, c'est perdre **une** position. Le second
est local, le premier est systémique.)*

**Un contrôle qui ne contrôlait rien**, attrapé en écrivant ce tableau : le premier « un état
manquant » portait sur la **dernière** position — or la perplexité note les N−1 premiers pas, et la
dernière position ne sert à rien. Le chiffre sortait **identique à la référence** (14,6496), ce qui
avait l'air d'un résultat et n'était qu'un trou hors champ. Corrigé en trouant des positions
**notées** (32, 64, 96), et c'est la même famille que le témoin périodique de la périphérie.

## 2. Ce que ça impose à l'ordonnanceur de C4 (et ce que ça n'interdit pas)

**Interdit** : un ordonnanceur qui « laisse un pas prendre du retard » en réutilisant le dernier
état reçu. Le prix est ×633 par pas, mesuré.

**Permis, et c'est là que l'asynchronisme a un sens** : réordonner **à l'intérieur** d'un pas —
les messages d'un même pas (état, `pre`, paires) peuvent arriver dans n'importe quel ordre, du
moment que chacun porte sa position et que la réduction attend **le bon** état. C'est déjà ce que
fait le protocole : le champ `pos` voyage, et un état d'une autre position est refusé plutôt que
mélangé en silence (même famille que les réglages qui voyagent depuis le v7 : **deux nœuds ne
doivent pas calculer deux choses différentes sous le même nom**).

**Ce qui reste ouvert pour C4** : le coût n'est mesuré que pour un état **décalé**. Un état
**périmé mais bien aligné** (recalculé après coup, ou fourni par une région en retard qui a
rattrapé) n'est pas la même chose — et c'est ce que ferait un vrai ordonnanceur asynchrone :
retarder le *calcul*, pas *l'appariement*. La borne de péremption à écrire est donc : « un état
est refusé s'il n'a pas la position attendue » — ce que la mesure chiffre à ×633.

## 3. Protocole, pour rejouer

```bash
tools/c4_retard.sh 128 12 "0 1 2 4 8 16"     # ~3 min
```

**Le contrôle qui valide le banc** : le retard 0 doit rendre **exactement** la perplexité du modèle
entier (14,6496 = 14,6496 ✓) — sans lui, les six chiffres mesureraient peut-être autre chose que le
retard.
