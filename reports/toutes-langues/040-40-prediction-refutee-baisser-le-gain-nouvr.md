> Campagne : **toutes-langues** · expérience **40**
> Titre : 40. Prédiction réfutée : baisser le gain n'ouvre PAS le régime gradué
> Date réelle : **2026-10-06 12:17 HAE** (source : commit `d15c870`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 40. Prédiction réfutée : baisser le gain n'ouvre PAS le régime gradué

Le §38.2 terminait sur une piste contre-intuitive : puisque le `tanh` est déjà saturé
à gain 1, **baisser** le gain devrait le faire sortir de saturation et donner à chaque
neurone une information graduée au lieu d'un signe. Mesuré :

| gain | saturation | événements 1e-4 | fidélité VALID | fidélité TEST |
|---:|---:|---:|---:|---:|
| 0,003 | 0,0 % | 99,4 % | 0,5985 | 0,5868 |
| 0,01 | 0,0 % | 99,8 % | 0,6112 | 0,6033 |
| 0,03 | 0,0 % | 99,9 % | 0,6217 | 0,6129 |
| 0,1 | 0,0 % | 100,0 % | 0,6281 | 0,6207 |
| 0,3 | 0,3 % | 100,0 % | 0,6301 | 0,6229 |
| **1,0 (valeur du pont)** | 0,6 % | 99,8 % | **0,6304** | **0,6233** |

**Réfutée, et nettement** : la fidélité **monte** de façon monotone avec le gain. Le
gain 1 est déjà au sommet de la plage utile, et sortir de saturation ne fait que
détruire l'information.

Autrement dit : **la saturation n'est pas un défaut, c'est le mécanisme.** Le `tanh`
saturé transforme l'entrée en signes ; la récurrence en fait une moyenne glissante de
signes ; c'est cette moyenne qui porte le contenu. Un neurone gradué, lui, ne
transmet presque rien.

**Troisième prédiction réfutée de la session** — après la pesée `1/norme²` (§27.3) et
le multi-échelle comme cause principale (§28). C'est le signe que les mesures ne sont
pas des rituels, et cela vaut d'être dit à égalité avec les résultats positifs.

### 40.1 Conséquence pour le passage aux impulsions

Le tableau ci-dessus est aussi la réponse à la question des événements. De 0,003 à 1,
le taux d'événements **ne descend jamais sous 99,4 %**. Il n'existe aucun réglage du
gain, dans cette dynamique, qui rende le calcul creux.

Le passage aux impulsions n'est donc **pas un réglage** : c'est un **changement de
dynamique** (seuil, émission, remise à zéro), et il faudra le mesurer comme tel — en
comparant une dynamique impulsionnelle à celle-ci, pas en espérant que celle-ci
devienne creuse.


---
