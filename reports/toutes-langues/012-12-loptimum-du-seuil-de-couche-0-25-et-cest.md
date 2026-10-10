> Campagne : **toutes-langues** · expérience **12**
> Titre : 12. L'optimum du seuil de couche : 0,25, et c'est un maximum INTÉRIEUR
> Date réelle : **2026-10-06 01:53 HAE** (source : commit `dad554e`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 12. L'optimum du seuil de couche : 0,25, et c'est un maximum INTÉRIEUR

Balayage complet, panel stratifié, tout le reste égal :

| seuil-part | réseau | fid VAL | fid TEST | **écart à la constante** | invariance | pire paire |
|---|---|---:|---:|---:|---:|---:|
| 0,50 | 52 neurones · **1 couche** | 0,7621 | 0,7438 | +0,0223 | **0,9739** | **0,8929** |
| **0,25** | 80 neurones · 5 couches [44, 10, 10, 11, 5] | **0,7681** | **0,7487** | **+0,0272** | 0,9649 | 0,8745 |
| 0,10 | 80 neurones · 5 couches [44, 8, 8, 16, 4] | 0,7662 | 0,7481 | +0,0266 | 0,9634 | 0,8562 |

**0,25 est un maximum intérieur.** Au-delà, forcer encore la profondeur détériore
**les trois colonnes à la fois** : la fidélité de test (−0,0006), l'écart à la
constante (−0,0006) **et** l'invariance (−0,0015). On paie donc plus pour obtenir
moins — le signe net d'un réglage passé.

**Ce n'est pas un déplacement gratuit le long de la courbe d'échange** : entre 0,25
et 0,10, l'invariance baisse *et* la fidélité baisse. La courbe d'échange ne suffit
donc pas à décrire ce réglage — au-delà de l'optimum, on perd sur les deux tableaux.

### Le réglage retenu

Le défaut reste **0,50** — je ne change pas un défaut en silence, et 0,50 maximise
l'**invariance** (0,9739) et la **pire paire** (0,8929). Mais **0,25 est désormais
mesuré comme l'optimum de fidélité** (+22 % d'écart à la constante), réglable en
une ligne.

**Le choix dépend de l'usage** : un pont destiné au raisonnement veut de la
fidélité (0,25) ; un pont destiné à servir de représentation interlingue veut de
l'invariance (0,50). Les deux sont maintenant chiffrés.


---
