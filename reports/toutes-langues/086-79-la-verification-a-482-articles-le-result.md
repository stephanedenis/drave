> Campagne : **toutes-langues** · expérience **79**
> Titre : 79. La vérification à 482 articles : le résultat du §73 NE SE RÉPLIQUE PAS
> Date réelle : **2026-10-07 08:01 HAE** (source : commit `91cef12`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 79. La vérification à 482 articles : le résultat du §73 NE SE RÉPLIQUE PAS

Le corpus Wikipedia apparié complet — **482 articles × 6 langues, 1 446 entrées
d'apprentissage et 1 446 de test** — permet de vérifier si les effets mesurés sur 85
articles tenaient à la taille du panel. Réponse, sur la composition des leviers :

| étape | fid TEST | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| à **85 articles** — base (centrage seul) | 0,4703 | 42,4 | 82,1 | 1,934 |
| à **85 articles** — + apprendre quoi lire | 0,4667 | 181,9 | 438,5 | **2,411** |
| à **482 articles** — base (centrage seul) | 0,4713 | 39,8 | 98,9 | **2,487** |
| à **482 articles** — + apprendre quoi lire | 0,4546 | **83,3** | 146,6 | **1,759** |
| *professeur à 482 articles* | — | *387,9* | *4 655,4* | ***12,001*** |

### 79.1 Le fait, sans détour

**À 85 articles, « apprendre quoi lire » faisait MONTER le rapport** (1,934 → 2,411),
en faisant monter `P_cont` (82 → 438) tout en faisant baisser `P_lang` (42 → 182).

**À 482 articles, il le fait BAISSER** (2,487 → 1,759) : `P_cont` monte (99 → 147) mais
`P_lang` monte **davantage** (40 → 83).

**L'effet du §73 ne se réplique pas.** Ce que j'avais présenté comme « le premier
mécanisme dont les deux énergies vont dans des directions opposées » était un **effet de
petit panel**.

### 79.2 Ce que cela change dans le rapport

**Le §73, le §74, le §75 et le §77 reposent sur des mesures à 85 articles.** Le §75
annonçait « la cible est atteinte, 98 % du rapport du professeur ». **Ce chiffre doit
être considéré comme non répliqué**, et la chaîne qui y menait — apprendre quoi lire →
combiner avec le discriminant → composer avec le centrage — repose sur un effet qui
disparaît quand le panel grandit d'un facteur 5,7.

**Ce qui tient à 482 articles :**
- la **ligne de base** (centrage seul) : rapport **2,487**, meilleure qu'à 85 articles
  (1,934) — les grands panels aident, comme le §34 l'avait montré ;
- la **cible du professeur** : **12,001** contre 10,912 — elle monte aussi, donc l'écart
  relatif à combler ne se réduit pas ;
- **toutes les mesures de la traque qui portaient sur des identités** — le §67
  (invariance d'échelle), le §61 (décomposition de variance), le §70 (caractéristiques
  emboîtées) — car une identité ne dépend pas de la taille du panel.

### 79.3 La leçon, et elle complète celle du bilan

Le bilan (§B.5) disait : *avant d'améliorer un mécanisme, mesurer ce qu'il apporte
au-dessus du plus bête des modèles qui pourrait le remplacer.*

Il faut y ajouter : **et le mesurer sur un panel assez grand pour que l'effet ne soit pas
un artefact de taille.** Les 85 articles du §73 venaient d'un corpus en cours de
traçage — c'était ce qui était disponible, mais ce n'était pas une raison pour publier
l'effet sans le marquer comme provisoire.

**Le rapport contient donc, à sa dernière page, la réfutation d'un de ses propres
résultats centraux.** C'est la bonne façon de finir : la mesure qui contredit est arrivée
parce que la chaîne pour l'obtenir avait été armée avant de connaître la réponse.


---
