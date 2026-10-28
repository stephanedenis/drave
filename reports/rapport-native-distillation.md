# N2.3 — distillation : PPL 3,297 contre 3,465

> **Objet.** Distiller `drave-n0` (11,47 M) depuis le professeur byte-level (23,76 M, PPL 2.355),
> avec la divergence KL sur les 256 octets et l'entropie croisée.

## Dispositif

- Professeur : `/tmp/route-teacher`, **23,76 M**, PPL **2.355**, gelé.
- Student : `drave-n0`, **11 469 192** paramètres, initialisé depuis `/tmp/drave-n0-pont.pt`.
- **2 000 pas**, lot 16, séquence 128, lr 2e-4, température 2, alpha 0,7 (KL) / 0,3 (CE).
- Corpus : `data/corpus_fr_train.txt` ; validation : derniers 5 %.
- **133 s** GPU.

## Résultats

| mesure | valeur |
|---|---:|
| PPL student avant | **3,465** |
| PPL student après | **3,297** |
| **gain** | **−4,85 %** |
| PPL professeur | **2.355** |
| gap student − professeur | **+0,942** |
| durée | 133 s |

## Lecture

- La distillation **améliore** le student de **4,85 %** sans changer son architecture.
- Le **gap** au professeur reste **+0,942** de PPL : le student de 11,47 M ne rattrape pas 23,76 M en
  2 000 pas.
- Le professeur partage le **vocabulaire octet** : aucun tokenizer, aucune perte d'alignement.
- Le student distillé est **exporté** en DRVM (`/tmp/drave-n0-distille.drvm`).

## Verdict

**N2.3 — première passe : atteint.** La distillation fonctionne et le gain est mesuré. La porte N2
(« PPL < 2,5 ») n'est **pas** atteinte : **3,297**.

## Limites

- **2 000 pas** seulement ; pas de curriculum.
- **Même corpus** ; pas de test externe.
- **Pas** de pertes locales, têtes précoces ou pensée dans la distillation : seule la tête principale
  est distillée.
- **Gain** mesuré sur 8 lots de validation, sans intervalle.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-distillation.json`](native-distillation.json).
