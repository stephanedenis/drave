> Campagne : **toutes-langues** · expérience **54**
> Titre : 54. Le garde-fou du §30 a attrapé une SECONDE occurrence du même bug
> Date réelle : **2026-10-06 18:22 HAE** (source : commit `8be5966`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 54. Le garde-fou du §30 a attrapé une SECONDE occurrence du même bug

### 54.1 Ce qui s'est passé

La croissance sous contrainte d'invariance (μ = 0,1) a parcouru **toute** la naissance
et **toute** l'attrition, puis a planté au moment du **diagnostic oracle** :

```
ValueError: généalogie désynchronisée : 6 constantes de temps pour 149 neurones.
```

**C'est le garde-fou ajouté au §30 qui a parlé**, et il a bien fait.

### 54.2 La cause : le même oubli, à un troisième endroit

En ajoutant la constante de temps par neurone (§28), j'avais propagé `a_neur` dans
`nait`, `recalcule` et `compacte` — **et écrit un commentaire expliquant qu'il fallait
la propager partout.** J'ai ensuite trouvé, et corrigé, un oubli dans
`pont_parallele.py` (§30.4). Voici le **troisième** :

**La sauvegarde et la restauration du « meilleur passage » de l'attrition.** Le code
met de côté `poids`, `X`, `couches` et `compte_neurones` pour pouvoir y revenir après
être descendu jusqu'à un neurone — **mais pas `a_neur`**. À la restauration, `poids`
repassait à 149 neurones en laissant `a_neur` à 6.

### 54.3 Ce que cela aurait donné SANS le garde-fou

Sans lui, `recalcule` aurait indexé `a_neur[j]` hors bornes — ou, si les listes
avaient eu la même longueur par hasard, il aurait **calculé des trajectoires avec la
mauvaise dynamique, en silence**, et le diagnostic oracle aurait été faux sans que
rien ne le signale.

C'est exactement le scénario que le garde-fou du §30 était censé empêcher, et c'est la
**deuxième fois** qu'il sert. Un contrôle bruyant posé une fois a payé deux fois.

### 54.4 Corrigé, et relancé

Trois endroits corrigés : les deux créations de `meilleur_passage` et la restauration.
La passe est relancée.

### 54.5 Ce que la passe interrompue avait déjà donné

Le journal contenait la naissance et l'attrition complètes ; seul le résumé final
manquait. Meilleur point mesuré, **149 neurones** :

| | μ = 0,1 | μ = 0 (même taille, interpolé) |
|---|---:|---:|
| fidélité apprentissage | 0,6466 | — |
| fidélité VALIDATION | 0,6311 | ~0,6317 |
| **fidélité TEST** | **0,6306** | ~0,6317 |
| **invariance** | **0,8954** | ~0,8703 |
| **pire paire** | **0,6433** | ~0,5817 |

**−0,0011 de fidélité pour +0,0251 d'invariance et +0,0616 de pire paire** — même
taux d'échange qu'au §51, sur un point de plus et une graine identique.


---
