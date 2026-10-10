> Campagne : **toutes-langues** · expérience **32**
> Titre : 32. Le §29 est-il un artefact d'alignement ? NON — mesuré
> Date réelle : **2026-10-06 09:41 HAE** (source : commit `4de5b2f`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 32. Le §29 est-il un artefact d'alignement ? NON — mesuré

### 32.1 Le soupçon

L'UDHR est **un seul texte** traduit en 392 langues : à la position `t`, toutes les
langues disent la même chose. La couche 0 encode la position. Une lecture `e_t → y_t`
pourrait donc apprendre « à la position `t`, sors le vecteur typique de `t` » et
réussir **sans rien comprendre à la langue** — ce qui expliquerait tout le §29, où
l'entrée seule bat le réservoir (le réservoir, lui, ne lit pas la position
directement).

### 32.2 Le témoin qui le quantifie — aucun paramètre, aucun neurone

On prédit la ligne `t` d'une tranche de test par la **moyenne des lignes `t` des
tranches d'apprentissage**. C'est le meilleur prédicteur possible qui ne connaisse
**que la position**. Comparé à la constante (une seule ligne pour toutes les
positions), l'écart est exactement ce que la position apporte.

| corpus | position seule | constante | **ce que la position ajoute** |
|---|---:|---:|---:|
| **UDHR** (392 langues, texte ALIGNÉ) | 0,5690 | 0,5545 | **+0,0145** |
| **Wikipedia EN** (192/48 tranches, articles DIFFÉRENTS) | 0,3704 | 0,3602 | **+0,0101** |

**La position n'apporte que +0,0145 sur l'UDHR aligné, et +0,0101 sur Wikipedia non
aligné** — soit 0,0044 d'écart entre les deux. Or l'avantage de la lecture directe sur
le réservoir (§29) est de **+0,0564**.

**Conclusion : l'alignement de l'UDHR n'explique pas le §29.** La position seule est
loin de rendre compte de ce que la lecture directe extrait, et le corpus aligné
n'apporte presque rien de plus que le corpus non aligné. **Le §29 tient.**

### 32.3 Wikipedia : le pont y transfère mieux qu'on ne le craignait

Le pont a aussi été relancé sur Wikipedia (240 tranches EN, 240 FR, **articles
différents** — donc non parallèle). La régression `a_neur` l'avait tué ; corrigé, il
donne :

| | Romeo (parallèle, littéraire) | Wikipedia (non parallèle, encyclopédique) |
|---|---:|---:|
| fidélité sur A | 0,6660 | 0,5522 |
| **fidélité sur B (transférée)** | **0,5802** | **0,5226** |
| perte au transfert | −0,0858 | **−0,0296** |
| oracle sur B | 0,6207 | **0,5545** |
| écart à l'oracle | +0,0405 | **+0,0319** |
| invariance de sortie | 0,9540 | 0,9165 |

**La perte au transfert est presque trois fois plus faible sur Wikipedia** (−0,0296
contre −0,0858), et l'écart à l'oracle y est plus petit. Le corpus encyclopédique
transfère donc **mieux** que le corpus littéraire — ce qui va dans le sens de la
mission : un texte long et varié donne un pont plus général, pas moins.

L'invariance du professeur sur Wikipedia (0,3032) **ne veut rien dire** : le corpus
n'est pas apparié, et l'outil l'affiche lui-même en avertissement.


---
