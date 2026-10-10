> Campagne : **toutes-langues** · expérience **26**
> Titre : 26. Ce qui distingue les langues éloignées : une NORME plus grande
> Date réelle : **2026-10-06 07:44 HAE** (source : commit `37429ed`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 26. Ce qui distingue les langues éloignées : une NORME plus grande

Après avoir réfuté l'hypothèse de longueur (§25), j'ai profilé les 22 langues
complètes : norme de la représentation, canaux actifs, et cosinus au centroïde du
panel. Couche 10, trié par éloignement :

| langue | norme | actifs | cos au centroïde |
|---|---:|---:|---:|
| **csw** (cri des plaines) | **479** | 868 | **0,4419** |
| **dzo** (dzongkha) | **468** | 864 | **0,4651** |
| **amh** (amharique) | **537** | 867 | 0,6090 |
| fuf | 418 | 860 | 0,6818 |
| … | | | |
| acu | 283 | 844 | 0,8669 |
| haw | 282 | 846 | 0,8703 |
| **guc** | 289 | 845 | **0,8774** |

**Les langues les plus éloignées du centroïde ont systématiquement une norme plus
grande** : 468-537 pour les trois premières, ~282-289 pour les trois dernières. Le
nombre de canaux actifs, lui, est quasi identique partout (844-868) — ce n'est donc
**pas** un effet de densité.

### Et les trois plus éloignées partagent leur type d'écriture

**cri syllabique** (csw), **tibétain** (dzo), **éthiopien** (amh) — trois écritures
très éloignées du latin. Le quatrième (fuf, Pular) est à écriture latine et déjà
nettement plus proche (0,68).

**Ce n'est pas une preuve de mécanisme** — 22 langues, une corrélation — mais c'est
une piste nette : **plus l'écriture s'éloigne du latin, plus la représentation du
professeur est forte en magnitude et divergente en direction.**

### Pourquoi cela compte pour le pont

Si la cible est « forte » pour certaines langues, le pont doit apprendre à être
fort pour elles — ce qui **coûte le transfert**. Cela expliquerait pourquoi les
paires impliquant dzo résistent, et **donne un levier testable** : normaliser la
magnitude de la cible, langue par langue, avant d'ajuster la lecture.

**Réserve** : j'ai testé une normalisation voisine sur les états du RÉSERVOIR (§10.3)
et elle avait **échoué** en effondrant l'invariance. Mais il s'agissait des états
internes, pas de la cible du professeur. Les deux sont à ne pas confondre, et
l'expérience reste à faire.



---
