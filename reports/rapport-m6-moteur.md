# B27 — un Stroop à réponse motrice reste sans conflit

> **Objet.** B26 montrait un conflit nul avec une simple acceptation. Ici la réponse est un **choix
> moteur unique** (gauche/droite) : le mot et l'encre peuvent désigner des actions différentes.

## Résultats (8 essais)

| mesure | valeur |
|---|---:|
| exact | **100 %** |
| congruent | **100 %** |
| incongruent | **100 %** |
| **conflit** | **0,00** |
| réponse | gauche/droite |

## Lecture

- La politique **suit le canal demandé** (mot ou encre) et ignore l'autre : elle est **exacte** dans
  les deux conditions.
- Le **conflit est nul** parce que la tâche est **triviale** : le cue dit explicitement quel canal
  lire, et les deux canaux sont **indépendants**.
- Ce n'est **pas** un Stroop : un vrai Stroop demande de **nommer l'encre** en **ignorant le mot**,
  avec une **réponse unique** et un **coût** quand les deux divergent. Ici, il n'y a **ni coût ni
  compétition**.

## Verdict

**B27 est négatif** : la réponse motrice ne crée pas de conflit si le cue désigne le canal. Il
faudrait **une seule consigne** (« lis l'encre ») et des essais **incongruents** où le mot est
**plus fort** que l'encre — ce que la politique actuelle ne modélise pas.

## Limites

- **8 essais**, politique **déterministe**, pas de modèle.
- Pas de **coût** ni de **temps de réaction**.
- Les canaux sont **indépendants** : aucune compétition.
- Un seul jeu de couleurs.

## Fichiers

- Code : [`tools/cerveau/gating_moteur.py`](../tools/cerveau/gating_moteur.py).
- Test : [`tools/cerveau/tests/test_gating_moteur.py`](../tools/cerveau/tests/test_gating_moteur.py).
- JSON : [`m6-moteur.json`](m6-moteur.json).
