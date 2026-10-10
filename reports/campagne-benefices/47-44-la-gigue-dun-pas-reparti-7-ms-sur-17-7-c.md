> Campagne : **campagne-benefices** · expérience **44**
> Titre : 44. La GIGUE d'un pas réparti : 7 ms sur 17,7 — ce qu'un ordonnanceur doit tolérer
> Date réelle : **2026-10-10 09:12 HAE** (source : commit `d09f78c`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 44. La GIGUE d'un pas réparti : 7 ms sur 17,7 — ce qu'un ordonnanceur doit tolérer

L'instrument étant étalonné (§43), il peut mesurer autre chose que ce qu'on lui a injecté. La
question qui décide de l'asynchronisme (C4) est : **de combien la durée d'un pas varie-t-elle ?**
Un ordonnanceur qui suppose des pas réguliers casse à la première irrégularité ; il faut donc la
chiffrer.

**Mesure** (12 couches locales, 12 distantes, 64 pas, traces des deux côtés fusionnées) :

| phase | médiane | p90 | max | min | n |
|---|---|---|---|---|---|
| aller (pilote → nœud) | 0,13 ms | 0,14 | 0,16 | 0,09 | 63 |
| retour (nœud → pilote) | 0,14 ms | 0,17 | 0,17 | 0,05 | 63 |
| **pas complet** (envoi → réception finale) | **17,67 ms** | 19,57 | **21,29** | **14,29** | 63 |

**Trois lectures, et la troisième est la plus utile :**

1. **le réseau local ne coûte rien** : 0,13 ms à l'aller, 0,14 au retour — le transport est
   négligeable devant le calcul, ce qui est cohérent avec la loi de latence de la campagne
   (3,4 ms par jeton et par ms de RTT) dès qu'on met un vrai RTT ;
2. **le pas complet vaut 17,67 ms en médiane**, dont l'essentiel est le calcul du nœud ;
3. **la gigue est de 7,00 ms** (max − min) sur cette même médiane de 17,67 ms, soit **40 %** — et
   le p90 (19,57) est à 2 ms au-dessus de la médiane. Autrement dit : **un ordonnanceur qui
   suppose des pas réguliers se trompe de 40 %**, et c'est exactement ce que C4 devra absorber.

**Et avec un VRAI RTT** (le proxy `tools/proxy_latence.py` ajoute 5 ms par message), la
condition laissée ouverte ci-dessus est levée :

| phase | sans RTT | **avec 5 ms/message** |
|---|---|---|
| aller (pilote → nœud) | 0,13 ms | **5,29 ms** (médiane) · p90 **10,38** · max 10,46 |
| pas complet | 17,67 ms | **30,24 ms** (médiane) · p90 38,98 · max 39,47 |
| **gigue du pas** | 7,00 ms (**40 %**) | **14,80 ms (**49 %**)** |

**Trois choses, dont une qui surprend :**

1. **l'instrument est de nouveau étalonné** : 5 ms injectés par message ⇒ 5,29 ms mesurés à
   l'aller (le reste est le transport) ;
2. **le p90 de l'aller vaut le DOUBLE de la médiane** (10,38 contre 5,29) : le proxy endort chaque
   message, et une trame qui traverse les deux sens paie deux fois — la distribution est
   **bimodale**, pas bruitée ;
3. **la gigue croît plus vite que la latence** : +71 % de latence médiane pour +111 % de gigue, et
   le taux passe de 40 % à **49 %**. Autrement dit : **un ordonnanceur asynchrone (C4) doit
   tolérer la moitié de la durée d'un pas en irrégularité** sur un lien à 5 ms — et cette
   proportion **empire** avec la distance, ce qui est l'inverse de l'intuition (« un lien plus
   lent est plus régulier »).

**Ce que la mesure ne dit toujours pas** : le proxy endort **par message**, il ne simule ni la
perte, ni la réorganisation, ni la congestion — un vrai réseau fait les trois. La gigue mesurée
est donc un **plancher** pour un lien de ce RTT.
