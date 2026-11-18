# Le 150 M : à lr 3e-4 le palier ne casse pas, à 1e-4 il casse vers 1 550 pas

> **Ligne de roadmap** : N (le palier 1) · **Date** : 2026-11-18 · **Verdict** : ✅ mesuré — sur le
> 142 M (`d=896`, 141 935 400 paramètres) au corpus v2, **lr 3e-4** plafonne à une PPL de validation
> de ~12,1-12,2 pendant 2 000 pas puis **monte** (12,4-12,6, pointes à 13,1) ; **lr 1e-4** descend
> doucement (12,5 → 11,9 à 1 000 pas) puis **casse** entre 1 500 et 2 000 pas : 11,56 → **7,60**.
> **lr 2e-4** casse aussi, un peu plus tard (11,69 à 1 500 → 7,98 à 2 000).
>
> **Dispositif** : `entrainer_native.py`, même corpus (`data/wiki_mix_v2/train.txt`), même val
> épinglé, `seq` 1 024, lot 8, AMP, graine 1 · trois courses de 2 000 pas (3e-4 arrêtée à 4 000) ·
> données [`sonde-lr-150m.json`](sonde-lr-150m.json).

## La table

| pas | lr 3e-4 | lr 1e-4 | lr 2e-4 |
|---:|---:|---:|---:|
| 1 | 185,50 | **185,50** | 129,89 |
| 500 | 12,18 | 12,09 | 12,14 |
| 1 000 | 12,07 | 11,88 | 11,88 |
| 1 500 | 12,15 | 11,56 | 11,69 |
| 1 600 | 12,20 | **11,18** | 10,72 |
| 1 800 | 12,23 | **9,05** | 8,88 |
| 2 000 | 12,21 | **7,60** | 7,98 |
| 4 000 | 12,66 | — | — |

## Lecture

1. **C'est une transition de phase, pas une pente** : entre 1 500 et 2 000 pas, la PPL du 1e-4
   tombe de 11,56 à 7,60 (facteur 1,5) — le modèle trouve la structure des octets d'un coup.
2. **Le lr décide de la transition** : à 3e-4 la même transition n'a pas lieu sur 4 000 pas ; le
   lr plus élevé maintient le modèle hors du bassin (la PPL dérive même à la hausse). Le 2e-4
   casse, mais plus tard et plus haut.
3. **Le 3e-4 ne se transpose pas du 73 M** : c'était la recette du 73 M (PPL 4,01 à 3 000 pas) ;
   à 142 M elle ne marche pas. La taille change le lr stable — c'est la leçon à porter au plan.
4. **La comparaison 1e-4 / 3e-4 est appariée** : la PPL au pas 1 est identique au chiffre près
   (185,496), donc même initialisation ; la 2e-4 a une autre initialisation (129,888) — elle
   confirme la transition, pas la comparaison exacte.

## Les contrôles

- **Même corpus, même val épinglé, mêmes fenêtres** (Van der Corput, compteur identique), même
  architecture, même graine : la seule variable est le lr.
- **La PPL de validation est le juge**, pas la perte d'entraînement (qui reste ~2,5 dans les trois
  cas : elle ne distingue pas les régimes).
- **La course 3e-4 a été arrêtée à 4 000 pas** sur ce constat, pas poursuivie « pour voir ».

## Ce qui pourrait le rendre faux

- **Une graine** : la transition pourrait être sensible à l'initialisation (la 2e-4, autre init,
  casse quand même — mais un troisième tirage serait plus solide).
- **La validation est le `val.txt` de v1** (résumés Wikipédia) quand le train est le plein texte
  dédupliqué : une partie de la chute peut être un changement de régime de domaine.
- **L'AMP** : le `GradScaler` est journalisé (échelle 65 536 au pas 1) mais son effet sur la
  transition n'est pas isolé — une course fp32 à 1e-4 le dira.

## Ce que ça change

La recette du palier 1 est **lr 1e-4** (les chaînes de la nuit ont été relancées à 17 h 24 avec
cette valeur, 11 tranches de 10 000 pas, banc après chacune). Le seuil de transition (~1 550 pas)
est un point de mesure à retrouver sur les deux corpus : c'est là que la comparaison v1/v2 devient
lisible.

## Voir aussi

- [les données](sonde-lr-150m.json) · [le corpus v2](rapport-corpus-v2.md) · [les deux val](rapport-natif-val-deux-decoupages.md) ·
  [le plan natif](../docs/pilotage/natif-plan.md)
