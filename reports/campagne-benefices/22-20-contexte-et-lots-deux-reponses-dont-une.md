> Campagne : **campagne-benefices** · expérience **20**
> Titre : 20. Contexte et lots : deux réponses, dont une qui n'est pas celle qu'on croit
> Date réelle : **2026-10-09 00:06 HAE** (source : commit `f9ca016`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 20. Contexte et lots : deux réponses, dont une qui n'est pas celle qu'on croit

**Contexte long — le protocole mesurait le cache, pas la qualité.** L'étape fait
varier `--ctx` de 512 à 8 192 en gardant `--limit 256` : la perplexité est donc
**constante par construction** (17,4315), et ce qui varie est l'allocation du
cache KV. Résultat : **RSS 1 248-1 249 Mo pour tous les contextes**, cache KV en
32 bits. Autrement dit, à fenêtre courte, le contexte déclaré ne coûte rien — et
c'est la mesure d'aiguille (§ 9) qui porte la qualité à longue portée, pas
celle-ci. La campagne dit maintenant lequel des deux mesure quoi.

**Lots — ×1,4, et la perplexité ne bouge pas.** Qwen2.5-0.5B, 512 jetons :

| `--lot` | 1 | 2 | 4 | 8 | 16 | 32 | 64 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PPL | 13,1368 | 13,1359 | 13,1359 | 13,1359 | 13,1359 | 13,1359 | 13,1359 |
| tok/s | 16,8 | 18,4 | **23,2** | 23,2 | 21,5 | **23,7** | 13,1 |

**Le lot ne change pas le résultat** (perplexité identique au chiffre près dès le
lot 2) et il apporte **×1,4 de débit** (16,8 → 23,7), avec un plateau de 4 à 32 et
une chute à 64. C'est le même ordre que le ×1,58 du dépôt, mesuré ici sur un
modèle qui tient en RAM — donc **sans le disque**, ce qui est le point : le lot
paie même quand rien n'est lu du disque.

*(Les temps restent mesurés sous charge 66-81 : l'ordre de grandeur est là, la
décimale non.)*

---
