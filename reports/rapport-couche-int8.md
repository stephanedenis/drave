# A7.7 — int8 sur le hidden : le volume baisse, la fidélité casse

> **Objet.** A7.6 transportait le hidden d'une couche en **f32** (4 105 o/jeton). Ici on le
> **quantifie en int8** avant l'envoi, avec deux granularités : **par tenseur** et **par jeton**.

## Résultats (couche 12, 3 invites)

| variante | ratio d'octets | argmax | diff max | KL |
|---|---:|---:|---:|---:|
| **int8 par tenseur** | **0,345** | **0,00** | **26,6** | **10,2** |
| **int8 par jeton** | **0,346** | **0,83–0,93** | **17,0** | **0,12–0,37** |
| f32 (A7.6) | 1,00 | **1,00** | **0,0** | **0,0** |
| bf16 (A7.6) | ~0,50 | **1,00** | **0,456** | non mesuré |

## Lecture

- **Int8 par tenseur est inutilisable** : une seule échelle pour 896 canaux ; les valeurs
  extrêmes écrasent les petites, l'argmax tombe à **0**.
- **Int8 par jeton** sauve l'argmax (**0,83–0,93**) et divise la KL par **~30**, mais **reste
  lossy** : diff max **17**, KL **0,12–0,37**.
- Le **volume** est **2,9×** plus faible (34,6 % du dense) ; c'est le gain recherché.
- **bf16** (A7.6) est **plus fidèle** (argmax 1,0, diff 0,456) pour **2× moins d'octets** que f32,
  mais **2× plus** que int8.

## Verdict

**A7.7 est négatif pour int8 nu** : le volume tombe à **34,6 %**, mais la fidélité n'est pas
au rendez-vous. Il faut **une échelle par canal** (ou un **outlier-aware**), pas une échelle par
jeton, avant de transporter un hidden.

## Limites

- **Une couche**, 3 invites, pas de PPL quantifiée.
- Le serveur **dequantifie** avant la couche ; le coût CPU de la quantization n'est pas compté.
- **f32** et **bf16** viennent d'A7.6, pas de la même passe.

## Fichiers

- Code : [`tools/couche_distante.py`](../tools/couche_distante.py) (`--quant` interne, `quant=True`).
- Fiche : [`rapport-couche-distante.md`](rapport-couche-distante.md).
- JSON : [`couche-int8.json`](couche-int8.json).
