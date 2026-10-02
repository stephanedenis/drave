# V4-Flash réparti sur deux nœuds — exact, et ce qu'il coûte

**En une ligne** : un modèle à **hyper-connexions** se découpe entre deux
processus et rend **exactement** la même perplexité (écart `0,00e0` en mode
dense), au prix de **4× le transport** — parce que son état résiduel voyage en
`hc` copies — et le mode **listes n'y gagne rien** : cet état est dense à
99,9 %.

## 1. Le résultat

Couche 20 sur 43 chez le pilote, 23 chez le pair, mêmes jetons des deux côtés :

| | perplexité | octets par flux (aller) | activité | temps |
|---|---|---|---|---|
| référence locale | **8 311,3347** | — | — | 4 377 ms/jeton |
| deux nœuds, dense | **8 311,3347** — écart **0,00e0** | 65 615 | 400 % (16 384 canaux) | 4 873 ms (1,11×) |
| deux nœuds, listes | 9,13e-2 d'écart | 65 544 | 399,6 % | 5 123 ms (1,16×) |

Le transport dense est **exact** (c'est le contrat : `0,00e0`), et il l'est
resté après l'extension du protocole aux `hc × cachés` canaux.

## 2. Ce qu'il a fallu étendre, et le bug que ça a révélé

1. **La validation de largeur** : le nœud moteur n'acceptait que `cachés`
   (4 096) canaux ; il accepte les deux largeurs, et c'est **son propre modèle**
   qui dit laquelle est légitime.
2. **Le décodage** : la charge se décode à la largeur du **modèle**, jamais à
   `f.n` — ce champ vaut le nombre de **canaux** en mode dense mais le nombre de
   **paires** en modes listes. Les confondre donnait un état de **16 362**
   valeurs au lieu de 16 384 (`Hc::melanger` sortait de la tranche) : la
   première version de ce correctif avait introduit cette confusion, et c'est le
   mode listes qui l'a montrée — le mode dense, lui, passait.
3. **La réduction des copies** : elle se fait **une seule fois**, sur le nœud qui
   possède la tête (`norme_finale`), et le point de coupure rend l'état **brut**.
   La réduire au point de coupure puis la ré-expandre à l'arrivée changeait le
   modèle : perplexité 8 311 → 34 159, écart **3,11** là où le transport est
   exact.

## 3. Le coût, et pourquoi le mode listes n'aide pas ici

L'état d'un modèle à hyper-connexions fait `hc × cachés` valeurs. À l'encodage
en listes, cela ne change **rien** : le taux d'activité mesuré est de **399,6 %**
(16 366 neurones actifs sur 16 384), c'est-à-dire que l'état est **entièrement
dense** — les quatre copies de l'état résiduel n'ont presque aucun zéro.

C'est une différence de nature avec les activations ordinaires, où le mode
listes divise le flux par 2,3 à seuil 0,01. Autrement dit :

> **là où le flux est dense, la liste ne compresse pas.** Le découpage d'un
> modèle à hyper-connexions coûte donc 4× le transport, en dense comme en
> listes — ce qui déplace l'arbitrage : mieux vaut couper **plus près du
> calcul**, ou après une couche dont la sortie est creuse.

## 4. Ce que ce n'est pas

- Ce n'est pas une validation du modèle : la perplexité locale (8 311) porte sur
  **4 jetons notés**, et la comparaison à llama.cpp pour le modèle entier donne
  678,09 contre 548,32 (voir `reports/rapport-v4-hca.md`).
- Ce n'est pas un débit : 1,11× le calcul local à deux processus sur la MÊME
  machine, avec un chargement de 86 Go de chaque côté. La mesure dit que le
  découpage **fonctionne**, pas qu'il accélère.
- Ce n'est pas la fin de P6 : restent le découpage en **fichiers de grappes**
  (`cluster-XX.gguf`) et la mesure du mode blocs sur un état creux.
