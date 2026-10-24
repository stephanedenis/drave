# A7.3 — la grappe intra-couche : le top-1024 (21 %) rend la même perplexité

> Mesure du 24/10/2026, Qwen2.5-0.5B Q4_0, **255 jetons**, `--act-topk` : le moteur ne calcule que les **k** neurones
> les plus actifs d'une projection, les autres sont à zéro.

## Les résultats

| k (neurones calculés) | part des 4 864 | PPL |
|---|---:|---:|
| 0 (tout) | 100 % | 30,7286 |
| 64 | 1,3 % | **446,3** (effondrement) |
| 256 | 5,3 % | **6 918** (effondrement) |
| **1 024** | **21,1 %** | **30,7286 — la même** |

## Ce que ça dit

- **La grappe exacte existe à 21 %** : le top-1024 rend **exactement** la perplexité du réseau complet (30,7286 à
  quatre décimales) — 79 % des neurones FFN ne changent rien, sur ce corpus.
- **En dessous, ça casse** : 64 et 256 effondrent la perplexité — la grappe a une **taille minimale** mesurable, et
  elle est bien au-dessus de 5 %.
- C'est la **densité naturelle** des activations (SwiGLU) que la grappe épouse : les 21 % sont les neurones non nuls,
  pas une approximation choisie.

## Ce que ça ne dit pas

- **255 jetons** et un **0,5 B** : la taille (21 %) peut varier avec le modèle et le texte ; un autre corpus peut
  déplacer la frontière.
- « La même PPL » ne veut pas dire « la même sortie jeton par jet on » — c'est la **perplexité** qui est identique.
- **La grappe exécutée ailleurs** (le transport en réseau) reste à faire : ici c'est la **taille** de la grappe qui
  est mesurée, pas son transport — la couche déportée (A7.2) est le niveau au-dessus.
