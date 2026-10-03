# Granularité des listes et volume des flux entre unités — mesuré

> Fil repris le 03/10 (bloc 26) : « séparer les grappes et les couches en listes
> plus fines pour qu'elles puissent être sur des unités de traitement différentes,
> et surtout réduire le volume des flux d'activation potentiels entre unités.
> Plus de petits lots d'événements = plus de flexibilité pour l'optimisation en
> temps réel. »
>
> C'est l'axe 3 de `docs/vision.md` (« Distribuer, c'est router des listes »), dont
> les points ouverts étaient : la granularité, l'ordonnanceur de placement, et le
> flux de poids depuis le NVMe. Ce rapport mesure la granularité sur des
> **activations réelles** de V4-Flash (`DRAVE_DUMP_COUCHES`, 43 couches × 4
> positions ; tenseur `l_last` = le flux de coupure, 16 384 valeurs = 4 copies
> d'hyper-connexion × 4 096, soit **65 536 octets en f32**).

## 1. Ce que le flux pèse selon sa représentation (une liste pour tout le flux)

| seuil θ (fraction du max) | événements | DRVF v2 (écart u8 + i16) | % du dense f32 | « v3 » (échelle f16/32 + i8) | % dense | erreur L2 |
|---|---|---|---|---|---|---|
| 0,01 | 12 071 | 36 227 o | 55,3 % | 25 180 o | 38,4 % | **0,041** |
| 0,02 | 9 448 | 28 360 o | 43,3 % | 19 935 o | 30,4 % | 0,100 |
| 0,05 | 5 829 | 17 502 o | 26,7 % | 12 697 o | 19,4 % | 0,244 |
| 0,10 | 3 193 | 9 593 o | 14,6 % | 7 424 o | 11,3 % | 0,441 |

Le flux peut donc descendre à **un quart du dense** — au prix de 24 % d'erreur L2
sur l'activation. La question n'est pas « peut-on compresser » mais « quelle erreur
le modèle tolère », et elle se mesure (les modes de flux mesurés donnent 3,65e-2 et
4,45e-3 d'écart de perplexité, `tools/porte-flux.sh`).

## 2. Ce que la GRANULARITÉ coûte — à erreur ÉGALE

C'est le point qui tranche l'intuition. Pour chaque granularité G (nombre de listes
indépendantes dans le flux), on cherche le seuil qui donne l'erreur visée :

| G (listes) | valeurs/liste | err ≈ 0,05 | err ≈ 0,10 | err ≈ 0,20 |
|---|---|---|---|---|
| **1** | 16 384 | **55,3 %** | **43,3 %** | **26,7 %** |
| 4 (= les 4 copies hc) | 4 096 | 66,0 % | 61,8 % | 54,5 % |
| 16 | 1 024 | 65,7 % | 60,0 % | 52,3 % |
| 64 | 256 | 64,6 % | 58,3 % | 50,6 % |
| 512 | 32 | 73,9 % | 68,1 % | 57,5 % |

**À fidélité égale, une seule liste est la plus compacte** : découper en 512 listes
coûte 68 % du dense là où une seule en coûte 43 %. Deux raisons mesurables :
l'en-tête (14 octets par liste : 7 168 octets, soit 11 % du dense, pour 512 listes)
et la perte de l'**échelle globale** — un seuil relatif au max global filtre plus
durement qu'un seuil relatif au max de chaque tranche.

Un schéma à deux niveaux (jeter les tranches d'énergie négligeable, puis garder les
événements ≥ 5 % du max de chaque tranche gardée) ne renverse pas la conclusion :
à erreur comparable, G = 64 avec ε = 1e-2 donne 28,2 % du dense pour 0,31 d'erreur,
là où **une seule liste donne 26,7 % pour 0,24**.

## 3. Ce que la granularité apporte vraiment : le ROUTAGE, pas la compression

Les chiffres ci-dessus mesurent le volume **agrégé**. Ce qu'une liste fine change,
c'est *qui* reçoit quoi :

- une unité ne reçoit que les listes qui lui sont adressées — le débit d'un lien
  devient proportionnel à ce qu'il sert, pas au flux total ;
- une tranche d'énergie négligeable coûte **0 octet** (mesuré : à G = 64, ε = 1e-2,
  28,5 tranches sur 64 sont jetées, et le flux tombe à 28,2 % du dense) ;
- à seuil égal, une tranche fine a une **erreur plus faible** (0,244 à G = 1 contre
  0,030 à G = 512, au seuil 0,05) : on peut donc élaguer plus finement.

Autrement dit : **la granularité ne compresse pas, elle route.** Le gain est un
gain de *provisionnement* et de *localité* (chaque unité borne son entrée), pas un
gain d'octets — et il se paie en en-têtes.

## 4. Le fait qui commande le placement : les POIDS, pas les activations

Mesuré ce soir (`tools/analyse_octets_par_jeton.py`) :

| | par jeton |
|---|---|
| poids à lire (V4-Flash IQ1_M) | **2,669 Go** |
| poids à lire (V4.1 Q2) | **3,893 Go** |
| flux d'activation à une coupure (V4-Flash, `l_last`, f32) | **65 536 octets** |

**Quatre ordres de grandeur d'écart.** Un découpage entre unités paie donc, avant
tout, l'endroit où vivent les poids : un jeton a besoin de 2,7 Go de poids *par
pas*, et les transporter coûte 411 ms (PCIe 6,5 Go/s) à 107 ms (NVLink 25,8 Go/s)
par jeton, contre 65 Ko d'activation (2,5 µs sur le même lien). **Le placement doit
suivre les poids** ; les activations, même denses et dupliquées, sont abordables.

Corollaire pour l'idée de départ : « réduire le volume des flux d'activation
potentiels » est un bon critère de *dimensionnement par lien*, mais ce n'est pas là
que se joue le coût d'un découpage. Là où la granularité fine paie, c'est pour
**router le travail** (une liste = une unité de travail autonome) et pour **borner
la latence** — pas pour économiser des octets.

## 5. Ce qui reste à mesurer

1. **Le volume par expert routé** (pas par couche) : combien d'octets d'activation
   entrent et sortent d'un expert, et quelle est la dispersion par jeton. Cela
   demande un vidage par expert (inexistant aujourd'hui) — c'est la mesure qui
   dirait si la granularité « par grappe » bat la granularité « par couche » sur le
   *provisionnement*.
2. **La latence par liste** en fonction de sa taille : le seuil où une liste fine
   coûte plus en ordonnancement qu'elle ne rapporte en parallélisme.
3. **Le plafond de listes** : à 512 listes, les en-têtes pèsent 11 % du dense ; le
   point où ils dépassent le gain est mesurable et proche.
