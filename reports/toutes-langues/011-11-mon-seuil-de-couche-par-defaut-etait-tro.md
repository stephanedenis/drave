> Campagne : **toutes-langues** · expérience **11**
> Titre : 11. Mon seuil de couche par défaut était TROP STRICT
> Date réelle : **2026-10-06 01:43 HAE** (source : commit `cf54f8b`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 11. Mon seuil de couche par défaut était TROP STRICT

Le critère de couche n'ouvrait **jamais** de couche sur le panel stratifié
(`communs` plafonnait à 28-38 %, sous le seuil de 50 %). Deux lectures possibles :
soit c'était correct — rien de partagé à composer à ce niveau — soit je me privais
de profondeur utile. Test en abaissant le seuil de **décision** :

| seuil-part | réseau | fid VAL | fid TEST | **écart à la constante** | invariance | pire paire |
|---|---|---:|---:|---:|---:|---:|
| **0,50** (défaut) | 52 neurones · **1 couche** | 0,7621 | 0,7438 | **+0,0223** | **0,9739** | **0,8929** |
| **0,25** | 80 neurones · **5 couches** [44, 10, 10, 11, 5] | **0,7681** | **0,7487** | **+0,0272** | 0,9649 | 0,8745 |

**Forcer la profondeur gagne en fidélité** : +0,0060 en validation, +0,0049 en test,
et l'écart à la constante monte de **+0,0223 à +0,0272, soit +22 %**. Le prix est
l'invariance : **−0,0090**, et la pire paire perd 0,0184.

### Ce que cela dit du seuil

**Le défaut de 0,50 était trop strict** — il laissait de la fidélité sur la table.
Mais ce n'est pas gratuit : c'est un déplacement le long de la courbe d'échange.

**Le taux obtenu est intéressant** : 0,0049 de fidélité pour 0,0090 d'invariance
abandonnée, soit **0,55 point par point** — à comparer aux **0,3856** de la loi
générale mesurée sur onze points de croissance. **Forcer la profondeur est donc un
moyen légèrement plus efficace que la moyenne d'acheter de la fidélité.**

### Et un bug trouvé au passage

En testant, j'ai découvert qu'abaisser `--seuil-commun` de 0,50 à 0,25 donnait un
résultat **bit-à-bit identique**. Cause : le déclencheur comparait `part_commune >
0.5`, une **constante en dur**, au lieu de la variable. Le drapeau ne changeait que
le pourcentage **affiché**, jamais la **décision**. Corrigé : la décision se règle
par `--seuil-part` (défaut 0,5, comportement inchangé), et `--seuil-commun` garde
son rôle propre — définir ce qu'est un neurone « concept commun ».

**Leçon** : quand un paramètre ne change rien, **suspecter le paramètre avant de
conclure sur le phénomène**.


---
