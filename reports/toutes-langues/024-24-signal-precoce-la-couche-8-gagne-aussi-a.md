> Campagne : **toutes-langues** · expérience **24**
> Titre : 24. Signal précoce : la couche 8 gagne aussi au niveau des UNITÉS
> Date réelle : **2026-10-06 07:39 HAE** (source : commit `b7fcce9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 24. Signal précoce : la couche 8 gagne aussi au niveau des UNITÉS

Mesure prise sur les 198 premières unités tracées (**17 langues complètes**, 10 unités
chacune), donc **avant** la fin du traçage. C'est la mesure la plus fine dont je
dispose : dix points appariés par langue au lieu d'un.

| | couche 10 | **couche 8** | gain |
|---|---:|---:|---:|
| **invariance moyenne** (10 unités) | 0,5977 | **0,6358** | **+0,0381** |
| pire paire (moyenne sur les unités) | 0,1383 | 0,1620 | +0,0237 |
| pire unité | 0,5616 | **0,6170** | +0,0554 |

**Deux confirmations indépendantes de la couche 8 :**

| mesure | corpus | gain de la couche 8 |
|---|---|---:|
| invariance segment par segment | Romeo (24 scènes) | +0,0512 |
| **invariance par unité** | **UDHR (17 langues × 10 unités)** | **+0,0381** |

Deux corpus, deux méthodes de mesure, même conclusion. Ce n'est plus une mesure
isolée.

### Et la « pire paire » devient enfin NOMMABLE

C'était l'objectif du traçage par unité. Au lieu d'un agrégat, on obtient des
couples précis :

| couche | pire unité | pire couple | valeur |
|---|---:|---|---:|
| 10 | 8 | **deu–dzo** | 0,0970 |
| 8 | 9 | **ces–dzo** | 0,0905 |

Le dzongkha (dzo) apparaît dans les deux — c'est la langue la plus éloignée du
panel sur ce corpus, ce qui est cohérent avec sa position (tibétain, isolat
morphologique) et donne enfin une **cible concrète** pour améliorer le pont.


---
