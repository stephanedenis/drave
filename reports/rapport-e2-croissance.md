# E2 — la croissance locale ne bat pas la structure tirée au hasard (2,3431 contre 2,3215)

> Campagne : **biologie** · expérience : croissance des connexions selon l'activité
> Question (le plan la pose ainsi) : « partir de 10 % de connexions, en **ajouter** selon
> l'activité — l'inné **plus** la croissance locale peuvent-ils remplacer l'apprentissage global
> des poids ? » Autrement dit : apprendre **où** sont les connexions vaut-il mieux que les tirer
> au hasard ?
> Verdict : **non, et de peu — mais dans le mauvais sens.** À protocole identique (mêmes graine,
> données, pas, modèle), la croissance locale par gradient donne **2,3431 bits/octet** là où un
> masque **statique** de **même densité finale** (25 %) donne **2,3215** : la croissance est
> **+0,9 % pire que le hasard**. Elle bat en revanche le point de départ (10 % statique : 2,3635),
> donc « ajouter des connexions aide » est vrai — c'est **choisir où** qui n'apporte rien.
> Date réelle : **2026-10-10 20:02 HAE** (heure lue sur la machine).
> Protocole : `tools/entrainer_moteur.py --masque … --croissance … --densite-cible 0.25`
> (nouveau), famille route, dim 192, 4 couches, 8 experts, seq 128, 3 000 pas, graine 1.

## 1. Les chiffres

| structure | densité | validation (bits/octet) |
|---|---|---|
| masque **statique 10 %** (le point de départ, E1) | 10 % | 2,3635 |
| **croissance** 10 % → 25 % (règle locale, +2 % des absentes / 250 pas) | 25 % | **2,3431** |
| masque **statique 25 %** (même densité finale, tiré au hasard) | 25 % | **2,3215** |

**Lecture** : la croissance apporte **+0,9 %** par rapport au départ (2,3635 → 2,3431) — elle
« marche » au sens où ajouter des câbles aide. Mais à densité égale, le **hasard** fait **mieux**
(2,3215). **Savoir OÙ ajouter ne paie pas**, à cette échelle et avec cette règle.

## 2. La règle testée, et pourquoi elle est locale

La croissance ajoute, à chaque étape, la fraction demandée des connexions **absentes** dont le
**|∂L/∂w| accumulé** est le plus grand, **couche par couche**. C'est une règle **locale** au sens
fort : pour une connexion interdite, le gradient reste calculable (produit de l'activation d'entrée
et du signal rétropropagé), il ne demande aucune information globale, et il dit exactement où
« ajouter un câble » ferait le plus baisser la perte **au premier ordre**. C'est le pendant
« croissance » du principe de Hebb, et c'est la règle la plus favorable qu'on puisse donner à
l'hypothèse.

**Le résultat est donc d'autant plus net** : même avec la règle la plus informative disponible
localement, la structure apprise ne dépasse pas la structure aléatoire.

## 3. Ce que ça dit, et comment ça s'ajoute aux autres mesures

| mesure du dépôt | résultat |
|---|---|
| **E1** (masque inné aléatoire) | un connectome aléatoire coûte **1 %** de perplexité et **divise les lectures par 4** |
| **E2** (cette fiche) | la croissance locale ne bat pas ce masque aléatoire à densité égale (+0,9 %) |
| **E3** (élagage développemental) | dense → élagage **appris** à 50 % : l'axe appris **paie** (÷2 lectures à qualité égale) |
| borne connue (biologie § 4) | les **401 856 monômes quadratiques** sont les seules directions neuves : la structure a un plafond |

**La synthèse, et elle est cohérente** : ce n'est pas la structure **ajoutée** qui porte la
qualité, c'est la structure **retirée avec discernement** (E3, l'élagage appris) — et le hasard
suffit pour la structure fixe (E1). La croissance par activité, telle que la biologie la décrit,
n'apporte rien **ici** : le gradient d'une connexion absente est un signal du **premier ordre**, et
la qualité d'un réseau vient d'interactions d'ordre supérieur.

## 4. Ce que ça ne dit pas

- **une seule échelle** (7,58 M paramètres) et **un seul calendrier de croissance** (+2 % des
  absentes toutes les 250 pas, plafond 25 %) : une croissance plus lente, ou jusqu'à une densité
  plus haute, pourrait changer la conclusion ;
- **la mesure est la perte de validation**, pas les paires par jeton : la croissance pourrait ne
  rien apporter en qualité **et** changer le coût d'exécution (c'est la densité qui le fixe, et
  elle est ici identique par construction) ;
- **l'inné n'est pas testé seul** : E1 l'a fait (÷4 lectures pour +1 %), et c'est le résultat qui
  compte pour l'architecture événementielle — E2 ne fait que dire que la **croissance** n'ajoute
  pas à cet inné.

## 5. Protocole, pour rejouer

```bash
P=/home/stephane/gpu-env/bin/python
C="--famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 \
   --lot 32 --pas 3000 --lr 1e-3 --graine 1"
CUDA_VISIBLE_DEVICES=0 $P tools/entrainer_moteur.py $C --masque 0.10 --sortie /tmp/e2/statique10.gguf
CUDA_VISIBLE_DEVICES=0 $P tools/entrainer_moteur.py $C --masque 0.25 --sortie /tmp/e2/statique25.gguf
CUDA_VISIBLE_DEVICES=0 $P tools/entrainer_moteur.py $C --masque 0.10 --croissance 0.02 \
   --croissance-tous 250 --densite-cible 0.25 --sortie /tmp/e2/croissance.gguf
```

**Le piège que la règle a failli avoir** : accumuler le gradient **après** avoir appliqué le masque
aurait accumulé **zéro** sur les connexions interdites — c'est-à-dire exactement celles que la
croissance doit départager. L'accumulation est donc faite **avant** l'application du masque, et
c'est écrit dans le code.
