> Campagne : **campagne-benefices** · expérience **08**
> Titre : 8. Les tâches à SORTIE CONTRAINTE : une matrice qu'on ne lit pas
> Date réelle : **2026-10-08 22:03 HAE** (source : commit `6379e49`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 8. Les tâches à SORTIE CONTRAINTE : une matrice qu'on ne lit pas

La tête de sortie est **la plus grosse matrice du modèle** : vocabulaire × cachés.
Pour le 0,5 B, 151 936 × 896 = **136 M poids, soit 136 Mo lus par jeton** — un
cinquième du modèle entier pour une seule projection. Or une classification ou un
choix multiple n'a que quelques sorties valides : `--tete-restreinte` ne calcule
que celles-là.

Mesure entrelacée, 64 jetons générés, 0,5 B Q8_0, 8 fils :

| tête | tour 1 | tour 2 | moyenne |
|---|---:|---:|---:|
| complète (151 936 jetons) | 14,79 tok/s | 16,14 tok/s | 15,47 |
| **restreinte à 3 jetons** | **21,92** | **22,07** | **22,00** |

**×1,42 de débit**, et la tête restreinte est **stable** (21,92 / 22,07 là où la
complète varie de 14,79 à 16,14 — moins de travail, donc moins de sensibilité à
la charge).

**Le second bénéfice compte plus que le premier, et il ne se mesure pas en
tok/s** : la sortie **ne peut pas** être hors de l'ensemble autorisé. Dans l'essai,
le modèle a produit `neutral negative negative positive positive negative neutral
positive` — des réponses incohérentes (un 0,5 B ne sait pas juger un sentiment),
**mais jamais un mot hors des trois étiquettes**. Pour une tâche de production,
cela vaut plus que la vitesse : plus de post-traitement, plus de reprise, plus de
réponse invalide à rattraper.

C'est donc la **première famille de tâches où l'architecture de Drave gagne par
construction** plutôt que par ses circonstances (modèle plus gros que la RAM) —
et elle ne demande aucun modèle particulier.

Le batch 7 refait la mesure sur le 1,5 B et sur gpt-oss-120b, où le rapport
tête/corps est différent.

### 8 bis. La carte de latence : à partir de quand un réseau coûte plus que le calcul

Le découpage à deux nœuds est exact sur localhost (écart 0,00e0). Mais localhost
est un plancher optimiste : ce qui décide, sur un vrai réseau, n'est pas le débit
(0,25 Mbit/s de flux) mais **la latence par message**. `tools/proxy_latence.py`
est un relais TCP qui ajoute un délai réglable ; `tools/carte_latence.sh`
l'intercale entre le pilote et le nœud et refait la mesure pour chaque délai.
Modèle entraîné ici, 4 couches dont **2 locales** (donc deux frontières franchies
par jeton), 128 jetons :

| latence ajoutée par message | m5_d384 (44 M) | m6_d512 (79 M) | perplexité |
|---:|---:|---:|---|
| 0 ms (localhost) | ×5,32 | ×3,49 | **3,5140 / 3,6064** |
| +1 ms | ×6,31 | ×4,99 | identique |
| +2 ms | ×7,97 | ×11,47 | identique |
| +5 ms | ×12,96 | ×10,97 | identique |
| +10 ms | ×18,94 | ×17,71 | identique |
| +20 ms | ×37,54 | ×28,18 | identique |
| +50 ms | ×79,73 | ×56,11 | identique |

**La perplexité ne bouge PAS d'un chiffre à 50 ms de latence par message** : le
transport est exact quelle que soit la latence, et c'est la seule chose que le
découpage doit garantir.

**Le temps, lui, croît linéairement** — et la pente donne la règle :
**≈ 3,4 ms de plus par jeton pour chaque milliseconde d'aller-retour** (44 M) et
**3,3 ms** (79 M), soit ≈ 0,85 ms par jeton et par frontière et par ms de RTT.
*(Les valeurs individuelles portent le bruit de charge de la machine — un point
isolé de la colonne 79 M sort de la monotonie — mais les deux extrémités de chaque
série sont mesurées à quelques minutes d'intervalle, et c'est la pente entre elles
qui est retenue.)*
Le plancher localhost, lui, est de **×3,5 à ×5,3** : à ces tailles, un processus
unique gagne toujours.

**La règle qui en sort, et elle est utilisable** : répartir ne paie que si le
calcul local par jeton dépasse ≈ **3,4 ms × RTT**. Concrètement : sur un réseau
local à 0,2 ms, il faut un modèle plus lent que ~0,7 ms/jeton (soit ~1 400 tok/s) —
tout gagne ; sur un lien à 1 ms, il faut plus de 3,4 ms/jeton (moins de 300 tok/s),
et un 0,5 B à 34 ms/jeton est largement au-dessus ; sur un lien à 20 ms, il faut
plus de 68 ms/jeton, soit un modèle **plus lent que 15 tok/s** — c'est le cas d'un
14 B en Q4 sur cette machine (0,5 à 9 tok/s), et **pas** d'un 0,5 B.

---
