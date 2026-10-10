> Campagne : **toutes-langues** · expérience **14**
> Titre : 14. LE LIVRABLE DE LA PHASE 2 : le pont sur 301 langues
> Date réelle : **2026-10-06 03:18 HAE** (source : commit `2bdae7e`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 14. LE LIVRABLE DE LA PHASE 2 : le pont sur 301 langues

| | |
|---|---:|
| apprentissage / validation | **301 / 50 langues** |
| test | **41 langues · 22 écritures** |
| réseau | **40 neurones · 1 couche** |
| fidélité apprentissage | 0,7459 |
| fidélité VALIDATION | 0,7505 |
| **fidélité TEST** | **0,7430** (constante 0,7207) |
| **invariance TEST** | **0,9827** |
| **pire paire** | **0,9165** |
| oracle TEST | 0,7653 — écart **+0,0223** |
| oracle VALIDATION | 0,7563 — écart **+0,0058** |
| **écart à la constante** | **+0,0223** |

### Les trois choses qui tiennent, à pleine échelle

**1. L'écart test/validation est de 1,01** (0,7505 / 0,7430), contre **2,58** sur
l'ancien panel uniquement non latin. Le diagnostic de typologie est **confirmé sur
le panel complet**, et pas seulement sur le signal précoce.

**2. L'écart de transfert tombe à +0,0223** (oracle test), contre **+0,0693** sur
l'ancien panel — **3,1× plus petit**. Là encore, ce que je prenais pour un goulot
de méthode était largement un artefact de mesure.

**3. L'écart à la constante vaut +0,0223** — dans la plage de l'invariant des +0,020

> **ATTENTION — cette affirmation est CORRIGÉE au §16.** L'écart vaut +0,0223 ici
> mais **+0,0322** sur les 896 canaux : ce n'est pas une constante mais une
> **plage de +0,020 à +0,032**. Les sept périmètres qui donnaient +0,0197 ± 0,0009
> partageaient le **même panel de 46 langues**. Voir §16.
mesuré sur sept périmètres et deux architectures, puis sur le panel stratifié
partiel (+0,0223). Il traverse donc : changement de panel, de taille, de corpus.

### Le signal précoce était représentatif

| | signal précoce (20 langues) | **définitif (41 langues)** |
|---|---:|---:|
| fidélité TEST | 0,7438 | 0,7430 |
| fidélité VALIDATION | 0,7621 | 0,7505 |
| écart oracle TEST | +0,0292 | **+0,0223** |

Les chiffres convergent. **Prendre le signal tôt était donc justifié** : il a
corrigé une conclusion fausse plusieurs heures avant que le run complet ne la
confirme.


---
