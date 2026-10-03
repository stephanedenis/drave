# Rapport — le préremplissage par experts : ce que le regroupement rapporte, mesuré

**Date** : bloc 31 · **Modèle** : Qwen3-30B-A3B-Instruct-2507-Q4_K_M (48 couches,
128 experts, 8 par jeton) · **Support** : NVMe (copie dédiée, le modèle d'origine
est sur le disque tournant) · 40 CPU, 16 fils · **Invite** : 192 jetons fixes,
identifiants produits une fois et réutilisés par toutes les configurations.

## Le mécanisme mesuré

`forward_lot` regroupe les jetons du lot par expert : la boucle est
`for e in 0..n_experts`, et chaque expert non vide reçoit **un** `gemm_dense_q4`
sur les `g` jetons qui l'ont choisi. Jeton par jeton, la même matrice est relue
autant de fois qu'elle a d'ayants droit.

## 1. Le temps

`tools/mesure-prefill-lot.sh`, 3 passes par point, médiane des 3 :

| lot | prompt_s | tok/s | CPU % | mur_s | gain |
|---|---|---|---|---|---|
| 1 | 33,23 | 5,77 | 995 | 60,5 | 1,00× |
| 2 | 24,51 | 7,83 | 889 | 51,1 | 1,36× |
| 4 | 23,29 | 8,27 | 864 | 50,3 | 1,43× |
| 8 | 23,17 | 8,27 | 854 | 50,6 | 1,43× |
| 16 | 22,45 | 8,53 | 851 | 49,3 | 1,48× |
| 32 | 21,91 | 8,77 | 839 | 48,9 | 1,52× |
| 64 | 21,27 | 9,03 | 831 | 48,2 | 1,56× |
| 192 | 21,00 | 9,20 | 827 | 47,8 | **1,58×** |

`mur_s` inclut le chargement du modèle (~27 s) : le gain porte bien sur
`prompt_s`, la seule colonne qui mesure le préremplissage.

## 2. Les octets

`tools/analyse_union_experts.py` lit la trace de routage réelle
(`DRAVE_TRACE_EXPERTS`, 48 couches × 194 jetons) et compte les matrices lues —
pas une estimation, un compte :

| bloc | lectures mode jeton | lectures mode groupe | gain | exp-éq/jeton |
|---|---|---|---|---|
| 1 | 74 496 | 74 496 | 1,00× | 8,000 |
| 2 | 74 496 | 56 904 | 1,31× | 6,111 |
| 4 | 74 496 | 43 427 | 1,72× | 4,664 |
| 8 | 74 496 | 32 847 | 2,27× | 3,527 |
| 16 | 74 496 | 23 946 | 3,11× | 2,572 |
| 32 | 74 496 | 16 446 | 4,53× | 1,766 |
| 64 | 74 496 | 10 526 | 7,08× | 1,130 |
| 192 | 74 496 | 4 804 | **15,51×** | 0,516 |

Borne (N → ∞) : 128 experts-équivalents par couche, soit 0,660 par jeton pour
cette invite — **12,1×** moins que le mode jeton. Le bloc de 192 fait donc mieux
que la borne par couche, parce que les jetons de génération qui suivent
complètent les couches.

**Lecture** : au lot 2 le gain d'octets (1,31×) et le gain de temps (1,36×)
coïncident — le chemin jeton était limité par les octets. Au-delà, le temps
décroche (1,58× pour 15,5× d'octets) : le calcul dense et l'ordonnancement
deviennent le mur.

## 3. Le chemin par lots n'est pas le chemin jeton, et il le dit maintenant

Routage : 7 838 des 9 312 lignes de trace diffèrent entre lot 1 et lot 192 (un
expert sur huit, au voisinage d'une égalité du routeur). Génération gloutonne,
huit jetons, même invite :

```
lot 1   : [67554, 512, 82497, 271, 14374, 220, 16, 13]
lot ≥ 2 : [67554, 512, 56698, 20538, 271, 2304, 44320, 56698]
```

lots 2, 4, 8, 32 et 192 donnent **la même** sortie : le chemin par lots est
cohérent avec lui-même, et diffère du chemin jeton à partir du 3e jeton.

Quantification (logits vidés à chaque position par `--ppl --logits-bin`) :

| mesure | lot 1 contre lot 8 |
|---|---|
| perplexité (191 jetons notés) | 19,172 contre 19,143 |
| argmax identique | 191/191 = **100 %** |
| Pearson | min 0,99719 · médiane 1,00000 |
| \|Δlogit\| | médian 1,29e-02 · max 1,27e+00 |

Ce n'est donc pas un autre modèle — c'est le même à 1e-2 près sur les logits —
mais une chaîne gloutonne amplifie la différence. Le moteur l'annonce désormais
au démarrage dès que `--lot > 1`, avec ces chiffres.

## 4. Deux compteurs qui ne comptaient pas

| compteur, par jeton | avant | après |
|---|---|---|
| experts, lot 1 | 1 811,9 M | 1 811,9 M |
| experts, lot 8 | **18,7 M** | **1 811,9 M** |
| attention, lot 1 | 902,6 M | 902,6 M |
| attention, lot 8 | **507,5 M** | **906,0 M** |
| total, lot 1 / lot 8 | 995 M / 530 M | 2 717,8 M / 2 721,1 M |

`gemm_dense_q4` ne tient pas de compteur (le pool ne connaît pas le modèle) : le
chemin par lots ne comptait que les jetons de génération. La sortie d'attention
`wo` était en plus le seul produit du chemin par lots à ne pas se compter, d'où
le 507,5 M contre 902,6 M pour un calcul identique. Les deux sont corrigés ;
la perplexité est inchangée au chiffre près (19,172 / 19,143 avant et après).

## 5. Ce que ça vaut sur Kimi-K3, et ce que ça ne vaut pas

Sur K3, le budget **mesuré** est de 86,787 Go/jeton : 25,830 pour les experts
routés (29,8 %) et 60,958 pour le partagé + l'attention + la tête (70,2 %). Le
regroupement par experts ne peut donc adresser **que 30 %** du trafic d'un
jeton — moins que sur Qwen3, où les experts sont 56 % des octets.

Le préremplissage, lui, amortit *tout* : le dense est lu une fois pour le lot
entier. À 1 000 jetons le coût par jeton tombe vers 0,09 Go au lieu de 86,8.
Mais le calcul ne s'amortit pas : ~210 GFLOP par jeton (98,3 pour les experts
routés, 112,2 pour le dense) contre 56,7 GFLOP/s mesurés sur ce moteur, soit
**~3,7 s/jeton** — estimation, à remplacer par une mesure quand le chemin
complet sera branché.

## Protocole, pour refaire

```bash
# 1. le temps
REPS=3 tools/mesure-prefill-lot.sh <modele.gguf> <ids-file> 1 2 4 8 16 32 64 192
# 2. les octets (la trace, puis le compte d'unions)
DRAVE_TRACE_EXPERTS=/tmp/tr.txt drave <modele> --infer --ids-file <ids> --n 2 --lot 1
python3 tools/analyse_union_experts.py /tmp/tr.txt --experts-par-jeton 8
# 3. la divergence du chemin par lots
drave <modele> --ppl <ids> --ctx 512 --limit 192 --lot 1 --logits-bin /tmp/lg1.bin
drave <modele> --ppl <ids> --ctx 512 --limit 192 --lot 8 --logits-bin /tmp/lg8.bin
```

**Rien d'autre ne doit tourner.** Un balayage mesuré pendant qu'un autre `drave`
tournait encore a donné 580 s au lot 2 au lieu de 24 s (×17) : deux pools de
16 fils sur 40 CPU se disputent les cœurs et la bande mémoire.
