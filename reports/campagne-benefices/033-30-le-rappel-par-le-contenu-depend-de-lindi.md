> Campagne : **campagne-benefices** · expérience **30**
> Titre : 30. Le rappel par le contenu dépend de l'INDICE, pas de la mémoire (8 indices)
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 30. Le rappel par le contenu dépend de l'INDICE, pas de la mémoire (8 indices)

Le §29 avait montré que la chaîne mémoire → injection fonctionne, et que le goulot est le
RAPPEL. Restait à savoir **pourquoi** : la mémoire est-elle mauvaise, ou est-ce l'indice
choisi ? La question se répond par une distribution, pas par un point — d'où un
prélèvement de **huit positions** dans l'invite B (de la dernière à la 128ᵉ depuis la
fin), chacune servant d'indice extérieur au magasin de A (aiguille au jeton 740, hasard
448).

| indice (position dans B) | épisode rendu | distance à l'aiguille |
|---|---|---|
| 1594 (128ᵉ depuis la fin) | 1630 | 890 |
| 1658 (64ᵉ) | 393 | 347 |
| 1690 (32ᵉ) | 437 | 303 |
| 1706 (16ᵉ) | 393 | 347 |
| 1714 (8ᵉ) | 1743 | 1 003 |
| **1718 (4ᵉ)** | **690** | **50** |
| 1720 (2ᵉ) | 429 | 311 |
| 1721 (dernière) | 437 | 303 |

**Moyenne 444 · médiane 329 · meilleure 50 · pire 1 003 · hasard 448.**

**Ce que la distribution dit, et elle est plus instructive qu'un point :**

1. **un indice existe qui trouve l'aiguille** : la position 1718 (quatre jetons avant la
   fin) tombe à **50 jetons**, soit **9× mieux que le hasard** — c'est le voisinage
   immédiat, largement assez près pour que le préfixe de l'épisode contienne le fait ;
2. **mais un seul sur huit** : les sept autres sont à 303-1 003 jetons, c'est-à-dire au
   niveau du hasard (moyenne 444 contre 448). Le §24 ter ter qui annonçait « 3,3× mieux
   que le hasard » était donc un **tirage chanceux** parmi cette distribution — et sa
   fragilité (136 puis 378 selon un point d'interrogation) s'explique par la même cause ;
3. **la limite n'est donc pas la mémoire, c'est le choix de l'indice** — et ce choix ne se
   devine pas : il n'y a aucune raison de préférer la dernière position (303 jetons) à la
   quatrième depuis la fin (50 jetons).

**Suite — dix indices, et le résultat est plus tranchant que prévu.** Les six dernières
positions ont été prélevées une à une (la 4ᵉ était la gagnante) :

| position depuis la fin | jeton (déduit) | distance à l'aiguille |
|---|---|---|
| 1 | `:` | 303 |
| 2 | `Answer` | 311 |
| 3 | `.` | 533 |
| **4** | **`only`** | **50** |
| **5** | **`code`** | **1 006** |
| 6 | `the` | 1 005 |
| 8, 16, 32, 64, 128 | — | 1 003 · 347 · 303 · 347 · 890 |

Les six dernières positions, dans l'ordre : **303 · 311 · 533 · 50 · 1 006 · 1 005**.

**Deux jetons VOISINS — « code » et « only » — donnent 1 006 et 50 jetons.** Rien de
lexical n'explique cela : les deux états ont lu presque le même texte. Ce que ces deux
points disent, c'est que **le rappel n'est pas une fonction continue de l'indice** : la
clé est un k-WTA (les 64 plus grands canaux sur 16 384), donc une petite variation de
l'état fait **entrer et sortir des canaux**, et la clé saute. Il n'y a donc aucune pente à
suivre pour « s'approcher » du bon indice — c'est ce qui rend le choix de l'indice
impossible à deviner, et c'est un mécanisme, pas une fatalité.

**Ce que cela indique pour la suite, et ce n'est pas mesuré** : rendre la clé **stable** en
la formant sur une FENÊTRE de positions (union ou intersection des k-WTA voisins) au lieu
d'un seul jeton — ce qui lisserait l'hypersensibilité au prix de la précision ; ou
interroger avec plusieurs indices et garder le meilleur (mais le recouvrement ne les
départage pas : celui du gagnant, 25/64, n'est pas le plus élevé) ; ou **abandonner le
rappel sémantique** pour ce qu'il ne sait pas faire et faire entrer le contenu comme
jetons (RAG ordinaire).
