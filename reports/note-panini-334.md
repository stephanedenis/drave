# Note pour Panini/NIPADA — le §334 : votre loi reproduite, votre β époque non, et pourquoi

> **Ce que cette note est.** Le **message prêt à envoyer** à l'équipe Panini/NIPADA (décision 4A
> du 14/11), avec la fiche technique en dessous. Elle porte sur **leur** résultat du §334
> (l'époque β +0,138 vs la filiation +0,049) et sur notre rejeu indépendant.
> **Ce qu'elle n'est pas** : une réfutation. C'est une **mesure de plus**, avec ses limites.

## 1. Le message (à envoyer tel quel)

> Bonjour,
>
> Nous avons rejoué votre §334 (655 paires, 374 avec date, les 44 signatures V14) avec nos outils
> et un contrôle supplémentaire : la **topologie** du graphe (la distance dans l'arbre), pour
> séparer ce que l'époque explique de ce que la filiation explique.
>
> **Ce qui se reproduit** : votre loi H0 tient (**R² = 0,909139** sur les 655 lignes ;
> **0,906307** sur les 488 paires uniques non auto). Le retrieval brut donne **61,4 %** de même
> tradition (hasard 22,4 %).
>
> **Ce qui ne se reproduit pas** : le coefficient d'époque **+0,138** de la v150 devient
> **−0,006** (non significatif) sur 374 paires ; l'époque seule explique **0,258** de la distance
> lexicale, mais n'ajoute que **0,0089** de R² **après** la topologie (p = 0,86).
>
> **Pourquoi, et c'est le point intéressant** : votre plan est **colinéaire** — les 180 paires de
> même tradition ont **28,7 ans** d'écart en moyenne (max 230), les 308 inter-traditions en ont
> **1 189** (136 à ≤ 100 ans). À **date fixe**, le contraste de filiation est fort dans la tranche
> axiale (**Δ = −0,166**, p = 0,0005), mais il **disparaît à surface contrôlée** (même langue
> source : Δ −0,135 contre un null de −0,129, p = 0,34). Votre avertissement n'est donc **ni
> confirmé ni réfuté** : dans ce corpus, **l'époque n'est pas séparable de la filiation**.
>
> **Ce que nous proposons** : un protocole commun sur un corpus **à date contrôlée** (paires
> contemporaines de traditions différentes, et paires de même tradition à dates décalées), avec
> les 14 atomes et nos mesures de retrieval — pour trancher ce que ce corpus ne peut pas trancher.
> Nos artefacts sont dans `reports/rapport-panini-334.md` et `panini-334.json`.
>
> — L'équipe Drave

## 2. Les chiffres, pour la réponse aux questions

| mesure | Panini (§334) | notre rejeu |
|---|---:|---:|
| loi H0 (R²) | publiée | **0,909139** (655 lignes) / **0,906307** (488 uniques) |
| β époque (v150) | **+0,138** | **−0,006** (374 paires, n.s.) |
| R² de l'époque seule | — | **0,258** |
| Δ R² de l'époque **après** topologie | — | **0,0089** (p = 0,86) |
| retrieval même tradition | — | **61,4 %** (hasard 22,4 %) |
| même tradition à ≤ 50 ans | — | **56,8 %** (hasard 22,8 %) |
| filiation après contrôles croisés | — | **50,0 %** (p = 0,0492 ; Holm 0,128) |
| époque après contrôles croisés | — | **53,8 %** (p = 0,373) |
| prédiction d'année intra-tradition | — | **R² = 0,042** (p = 0,0086 ; Holm 0,034) |

**Les trois contrôles négatifs** (détail dans la fiche) : la permutation des colonnes de la
signature tue le signal ; le nul de même langue source ramène le contraste à zéro ; la
collinéarité est mesurée (28,7 vs 1 189 ans).

## 3. Le protocole proposé (la suite commune)

1. **Un corpus à date contrôlée** : 20 paires contemporaines (± 10 ans) de traditions différentes,
   20 paires de même tradition à ± 200 ans, 20 paires de même langue source à dates décalées.
2. **Les mêmes 14 atomes** (leurs signatures) et **nos mesures** (retrieval,Glottolog, la
   topologie).
3. **Un pré-enregistrement** des hypothèses et des contrôles (la leçon de leur §150 et de notre
   audit).
4. **Le résultat attendu** : soit l'époque ajoute du R² **après** la topologie (leur avertissement
   tient), soit elle n'ajoute rien (la filiation explique tout) — dans les deux cas, **on le saura**.

## 4. Ce que cette note ne dit pas

- **Elle ne dit pas** que Panini a tort : elle dit que **leur corpus ne permet pas** de trancher.
- **Elle ne dit pas** que notre mesure est meilleure : elle dit qu'elle **ajoute un contrôle**.
- **Les 44 œuvres** sont un petit échantillon ; la tranche axiale est la plus informative.

## 5. Fichiers

- [`rapport-panini-334.md`](rapport-panini-334.md) — la fiche technique (655 paires, les contrôles).
- [`panini-334.json`](panini-334.json) — les données.
