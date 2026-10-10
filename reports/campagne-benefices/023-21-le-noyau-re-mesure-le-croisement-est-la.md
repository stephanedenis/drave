> Campagne : **campagne-benefices** · expérience **21**
> Titre : 21. Le noyau, re-mesuré : le croisement est là, et il coûte à densité 1
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 21. Le noyau, re-mesuré : le croisement est là, et il coûte à densité 1

`drave <modèle>` sans autre argument refait la mesure fondatrice du projet sur le
binaire du jour — Qwen2.5-0.5B, 64 Mo lus, 20 threads, sous charge 44 :

| mesure | valeur |
|---|---|
| bande passante mémoire | **21,5 Go/s** |
| forme listes (push) | 15,88 bits/poids (int8 + listes de rangs) |
| forme dense (pull) | 8,00 bits/poids |
| push, 0 événement | 233 134 matvec/s (**0,004 ms**) · **×0,02** du dense |
| push, 43 560 événements | 40 027 matvec/s · ×0,10 |
| push, 430 359 événements | 10 474 matvec/s · ×0,36 |
| push, 1 076 785 événements | 4 498 matvec/s · ×0,86 |
| push, 2 152 648 événements | 2 473 matvec/s · **×1,54** |
| pull (dense), tous les cas | 3 830-3 875 matvec/s (0,26 ms) |

**Le croisement est entre 1,08 et 2,15 M d'événements**, et il est franc : à vide
les listes sont **50× plus rapides**, à pleine densité **1,5 à 3,2× plus lentes**
(le journal de l'étape retient ×3,19 sur la dernière ligne). Ce n'est pas une
contradiction avec le seuil de 22 % du dépôt : c'est la même courbe, vue en
événements au lieu de la fraction. **Et cela dit pourquoi le chemin dense reste le
défaut sur un modèle dense** : à 71 % de densité (§ 10 ter), on est du mauvais côté
du croisement, d'un facteur 2 à 3.

---
