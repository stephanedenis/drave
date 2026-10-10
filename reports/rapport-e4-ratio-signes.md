# E4 (côté ENTRAÎNEMENT) — le ratio de signes cortical ne paie pas : 2,2729 → 2,3838 → 2,5188

> Campagne : **biologie** · expérience : contraindre le **ratio de signes** sans figer les magnitudes
> Question : la biologie cortex sépare excitation et inhibition (~80 % de neurones excitateurs,
> ~20 % inhibiteurs) et le principe de Dale veut qu'un neurone garde le même signe. Le dépôt avait
> mesuré la moitié **inférence** de E4 (les gains par couche : optimum intérieur du côté
> amplification, −11,5 %) et l'effet de **figer** les signes (E6, cher : 2,2662 contre 1,9020
> bits/octet). Ce qui manquait est le point milieu, et c'est celui que la biologie suggère :
> **contraindre le RATIO de signes, magnitudes libres**.
> Verdict : **l'hypothèse est réfutée, et proprement** — à protocole identique (mêmes graine,
> données, pas, modèle), l'équilibre **0,5** donne **2,2729 bits/octet**, le ratio cortical **0,8**
> donne **2,3838** (**+4,9 %**), et **0,9** donne **2,5188** (**+10,8 %**). La dégradation est
> **monotone** : plus on impose le déséquilibre biologique, plus le modèle est mauvais.
> Date réelle : **2026-10-10 19:51 HAE** (heure lue sur la machine).
> Protocole : `tools/entrainer_moteur.py --ratio-signes R` (nouveau), famille **route**,
> dim 192, 4 couches, 8 experts, k=2, seq 128, lot 32, 3 000 pas, lr 1e-3, graine 1,
> corpus `data/corpus_en.txt`, validation `data/corpus_en_val.txt`.

## 1. Les chiffres

| ratio de signes positifs | validation (bits/octet) | prix |
|---|---|---|
| **0,5** (équilibré) | **2,2729** | — |
| **0,8** (le ratio cortical) | **2,3838** | **+4,9 %** |
| **0,9** (déséquilibre extrême) | **2,5188** | **+10,8 %** |

Les ratios ont été **vérifiés à l'application** (« 0.80 demandé, 0.8000 obtenu sur 17 couches ») :
ce n'est pas une intention, c'est une mesure du poids réellement signé.

## 2. Ce que ça dit, et à quoi ça s'ajoute

**La séparation E/I n'est pas un levier de qualité** — en tout cas pas sous cette forme, à cette
échelle. Trois observations du dépôt disent maintenant la même chose par trois chemins :

| mesure | résultat |
|---|---|
| **inférence** (E4, `porte-gain.sh`) | l'optimum est du côté **amplification** (couche 0, gain 0,75 : −11,5 %) ; l'**inhibition dégrade** de façon monotone |
| **signes figés** (E6) | coûte cher : 2,2662 contre 1,9020 bits/octet |
| **ratio imposé** (cette fiche) | coûte : +4,9 % à 0,8, +10,8 % à 0,9 |

Autrement dit : **ce n'est pas le SIGNe qui porte la qualité, c'est la MAGNITUDE** (et, côté
inférence, le gain d'entrée). La biologie impose un ratio parce qu'elle a deux types de cellules et
des contraintes de transport axonal ; un tenseur dense n'a aucune de ces contraintes, et lui
imposer la conséquence **coûte**.

## 3. Ce que ça ne dit pas

- **une seule échelle** (7,58 M paramètres, dim 192) et **3 000 pas** : à plus grande échelle, un
  ratio imposé pourrait devenir *utile* (régularisation). C'est une hypothèse à tester, pas un
  résultat ;
- **un seul sens de contrainte** : on a imposé le ratio *des poids* ; la biologie l'impose *par
  neurone* (tous les axones d'un neurone ont le même signe). Un test par **ligne** et non par
  tenseur serait plus fidèle — et plus contraint, donc probablement plus coûteux ;
- **la stabilité** n'est pas mesurée : le ratio pourrait ne rien apporter en qualité *et* stabiliser
  l'entraînement (moins de divergence). La perte finale est le seul critère d'ici, et il est
  défavorable.

## 4. Protocole, pour rejouer

```bash
P=/home/stephane/gpu-env/bin/python
for R in 0.5 0.8 0.9; do
  CUDA_VISIBLE_DEVICES=0 $P tools/entrainer_moteur.py --famille route --dim 192 --couches 4 \
     --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 --lot 32 --pas 3000 --lr 1e-3 --graine 1 \
     --ratio-signes $R --sortie /tmp/e4/modele-$R.gguf
done
```

**Deux pièges de harnais attrapés** (le même jour, dans le même ajout) : un tenseur de signes créé
sur **CPU** alors que les poids sont sur **GPU** (erreur de device), et un `randperm` demandé sur
`cuda` avec un **générateur cpu** (« Expected a 'cuda' device type for generator »). Le générateur
reste sur CPU — c'est ce qui rend la graine reproductible quel que soit l'appareil — et la
permutation est **déplacée** ensuite.
