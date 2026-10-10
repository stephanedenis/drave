> Campagne : **campagne-benefices** · expérience **18**
> Titre : 18. Le résultat publié SURVIT au correctif d'échelle (sémantique multilingue)
> Date réelle : **2026-10-08 23:54 HAE** (source : commit `baeb2c6`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 18. Le résultat publié SURVIT au correctif d'échelle (sémantique multilingue)

La bande sémantique « 10–15 sur 24 couches » avait été mesurée avec un lecteur qui
**ignorait l'échelle par enregistrement** des traces DRVF. Le lecteur est corrigé ;
la question était : le résultat tient-il ? Caches **neufs** des deux côtés,
398 langues, article 1 contre article 2, pooling moyenne :

| couche | ancienne lecture | **échelle corrigée** |
|---|---:|---:|
| 0 | +0,0002 | **+0,0030** |
| 4 | +0,0156 | +0,0175 |
| 12 | — | +0,0354 |
| **13** | **+0,0344** | **+0,0395** |
| 14 | — | +0,0342 |
| 15 | — | +0,0326 |

**La bande 10–15 tient, et le pic reste à la couche 13** — légèrement plus marqué
après correction (+0,0395 contre +0,0344). Ce qui change : la couche 0 n'est plus
« exactement nulle » (+0,0030), ce qui est cohérent — l'échelle par enregistrement
n'est pas uniforme d'une couche à l'autre, et son omission écrasait
différentiellement les premières couches.

**C'est le premier résultat publié du dépôt qui soit revérifié après un correctif
de lecteur, et il survit.** La conclusion (une bande 10–15, un plateau, un effet
petit sur un fond anisotrope élevé) reste celle du `rapport-cycle-rapide.md`.

---
