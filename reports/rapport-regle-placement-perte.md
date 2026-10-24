# A8.3 — la règle place et perte choisit le KV comme la main

> Mesure du 24/10/2026, Qwen2.5-0.5B Q4_0, **255 jetons**, `--ppl`, `DRAVE_PERTE_MAX` (le budget de perte).

## Ce qui a été branché

`placement::kv_precision(couche, n_layer, budget_pct)` : l'**int8** si sa perte **mesurée** (A5.3 : **+2,28 %** sur les
premières couches, **+0,03 %** sur les dernières) tient dans le budget, le **f32** sinon. C'est
`DRAVE_KV_BITS_COUCHES="12-23:8"` **calculé au lieu d'être écrit** — la leçon de la tête (le 4 bits « qui tient »
coûte +10 % de PPL) appliquée au KV. **Deux tests** : les 24 couches (l'int8 passe sur 12-23 seulement), le budget
3 % (il passe partout), le budget 0 % (nulle part).

## Les résultats

| réglage | PPL |
|---|---:|
| f32 (la référence) | 30,7660 |
| **la règle place + perte (défaut, budget 1 %)** | **30,7286** |
| la main : `DRAVE_KV_BITS_COUCHES="12-23:8"` | **30,7286** |

- **La règle rend exactement le choix de la main** : même PPL à quatre décimales, mêmes couches en int8.
- Le coût mesuré est de **−0,12 %** (légèrement *mieux* que le f32) — **dans le bruit** des 255 jetons, à ne pas
  lire comme un gain : l'int8 tardif est **gratuit**, c'est tout ce que la mesure autorise à dire.
- **La leçon de la tête est appliquée** : la règle ne choisit pas « ce qui tient » (la place) mais « ce qui tient
  **dans le budget de perte** » — un 4 bits de tête (+10 %) serait refusé par le même budget.

## Ce que ça ne dit pas

- **255 jetons** : la PPL est bruitée (±0,1) ; l'égalité à quatre décimales entre la règle et la main est solide
  (c'est le même calcul), la différence avec le f32 ne l'est pas.
- **Le 0,5 B** : la frontière mesurée (12 couches sur 24) est celle de ce modèle ; un autre modèle peut la déplacer.
- **La place** n'est pas testée ici : c'est la **précision** que A8.3 branche ; la place (`choisir`, VRAM/RAM) est
  celle du KV depuis A2.6.
