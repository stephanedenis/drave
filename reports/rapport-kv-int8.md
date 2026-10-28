# A7.10 — cache KV en int8 : 4× moins d'octets, erreur 1,5e-2

> **Objet.** A7.9 montrait que le cache KV f32 coûte **24 580 o/jeton** sur 24 couches
> (**96 Mio** pour 4 096 jetons). Ici on quantifie le cache en **int8 par canal** (256 canaux
> KV = 2 têtes × 2 × 64), avec une échelle partagée entre les jetons.

## Résultats (couche 12, 64 jetons)

| mesure | f32 | **int8 par canal** |
|---|---:|---:|
| octets | **65 548** | **17 420** |
| ratio | 1,00 | **0,266** |
| par jeton | 1 024 o | **272 o** |
| diff max | 0 | **0,0155** |
| diff moyenne | 0 | **0,0050** |
| 24 couches × 4 096 jetons | **96,0 Mio** | **25,5 Mio** |

## Lecture

- **4× moins d'octets** : 17 420 contre 65 548, et **25,5 Mio** contre **96,0 Mio** pour 4 096
  jetons sur 24 couches.
- L'erreur de reconstruction est **faible** (diff max **0,0155**, moyenne **0,005**) mais **non
  nulle** : ce n'est pas bit-à-bit.
- L'échelle **par canal** coûte **1 024 o** (256 f32) par requête, indépendante du nombre de jetons ;
  pour de très courtes séquences, le ratio se dégrade.
- La **fidélité du modèle** (argmax, PPL) n'est pas mesurée : c'est une mesure de **cache**, pas de
  logits.

## Verdict

**A7.10 est un compromis positif** : le cache KV int8 par canal divise le volume par **4** avec une
erreur de reconstruction **~1e-2**. Il reste à mesurer l'effet sur les **logits** et la **PPL** pour
savoir si le cache quantifié est utilisable en décodage.

## Limites

- **Cache synthétique**, pas un vrai décodage autoregressif.
- **Une couche** ; l'extrapolation à 24 suppose des couches identiques.
- **Fidélité modèle** non mesurée.
- L'échelle par canal est **symétrique** ; un outlier-aware pourrait faire mieux.

## Fichiers

- Code : [`tools/kv_int8.py`](../tools/kv_int8.py).
- Test : [`tools/cerveau/tests/test_kv_int8.py`](../tools/cerveau/tests/test_kv_int8.py).
- JSON : [`kv-int8.json`](kv-int8.json).
