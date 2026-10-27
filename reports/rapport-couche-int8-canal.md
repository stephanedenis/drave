# A7.8 — int8 par canal : l'argmax tient, le bit non

> **Objet.** A7.7 montrait qu'int8 **par tenseur** ou **par jeton** casse la fidélité. Ici on
> quantifie avec **une échelle par canal** (896 échelles f32 partagées entre les jetons), avant
> transport vers le serveur de couche.

## Résultats (couche 12, 3 invites)

| mesure | invite 0 | invite 1 | invite 2 |
|---|---:|---:|---:|
| ratio d'octets (quant/dense) | **0,394** | **0,360** | **0,376** |
| argmax | **1,00** | **1,00** | **1,00** |
| diff max logits | **0,486** | **1,717** | **0,929** |
| KL | **0,0015** | **0,0020** | **0,0006** |
| bits identiques | 0,0006 % | 0,0002 % | 0,0003 % |
| PPL locale → quantifiée | 55,943 → **54,860** | 7,478 → **7,356** | 1,787 → **1,763** |

## Lecture

- **L'argmax est identique** sur les trois invites : le classement des tokens ne change pas.
- Le **diff max** reste **0,5–1,7** et la **KL** est **~1e-3** : ce n'est **pas** bit-à-bit, mais
  c'est **beaucoup mieux** que l'int8 par jeton (KL 0,12–0,37).
- Le **volume** tombe à **36–39 %** du dense : **2,6× moins** d'octets, au prix des 896 échelles
  f32 (3 584 o par requête, indépendantes du nombre de jetons).
- Les **bits** ne sont pas identiques : int8 est **lossy**, même par canal.
- La **PPL ne se dégrade pas** sur ces trois invites (elle baisse même légèrement, 54,86 contre
  55,94) : le bruit de quantification ne change pas la décision. Ce n'est pas une preuve de
  fidélité ; c'est une absence de perte mesurable sur 3 textes.

## Verdict

**A7.8 est un compromis utilisable** : argmax **1,0**, KL **~1e-3**, volume **~37 %**. Ce n'est pas
la fidélité bit-à-bit d'A7.6 ; c'est un **transport compressé** qui garde la décision. Il faut
mesurer la **PPL** avant de l'adopter par défaut.

## Limites

- **Une couche**, 3 invites ; la PPL quantifiée est mesurée mais sur des textes courts.
- Les **échelles par canal** coûtent 3,6 ko par requête ; pour de très petites séquences, le ratio
  se dégrade.
- Le serveur **dequantifie** avant la couche ; le coût CPU n'est pas compté.
- La quantification est **symétrique** ; un outlier-aware (par bloc) pourrait faire mieux.

## Fichiers

- Code : [`tools/couche_distante.py`](../tools/couche_distante.py) (`quant=True`, échelle par canal).
- Fiche : [`rapport-couche-int8.md`](rapport-couche-int8.md) (le négatif par tenseur/jeton).
- JSON : [`couche-int8-canal.json`](couche-int8-canal.json).
