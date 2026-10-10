> Campagne : **toutes-langues** · expérience **31**
> Titre : 31. Contrôle de capacité : l'entrée gagne-t-elle par NATURE ou par TAILLE ?
> Date réelle : **2026-10-06 09:28 HAE** (source : commit `b15a604`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 31. Contrôle de capacité : l'entrée gagne-t-elle par NATURE ou par TAILLE ?

Le §29 laissait une objection sérieuse : C (entrée seule, 1 792 caractéristiques) bat
A (40 neurones, 80 caractéristiques) — mais C a 22× plus de colonnes. Une partie de
l'écart peut être de la **capacité**, pas de la nature. Mesuré :

| | caractéristiques | fidélité TEST |
|---|---:|---:|
| témoin constant | 0 | 0,5678 |
| A40 · réservoir | 80 | 0,5972 |
| **A200 · réservoir (5× plus large)** | 400 | **0,6218** |
| **C_lin · entrée seule, LINÉAIRE** | 896 | **0,6364** |
| C_quad · entrée seule, quadratique | 1 792 | 0,6536 |
| B · A40 + entrée | 1 872 | 0,6609 |

Deux enseignements :

1. **La non-linéarité ne fait presque rien.** C_lin (896 colonnes) = 0,6364 contre
   C_quad (1 792 colonnes) = 0,6536. Doubler les colonnes par les carrés ne rapporte
   que +0,0172 : **l'essentiel de ce que porte l'entrée est accessible LINÉAIREMENT.**
2. **La capacité aide le réservoir, mais ne le rattrape pas.** 5× plus de neurones
   font passer A de 0,5972 à 0,6218 (+0,0246). Il reste 0,0146 sous C_lin, qui a
   2,2× plus de colonnes — donc à peu près à capacité comparable, le réservoir est
   toujours derrière.

**Verdict : la prédiction d'un avantage de NATURE est soutenue sans être tranchée.**
Le réservoir progresse avec la taille mais reste sous une lecture linéaire de
l'entrée.

### 31.1 Une mesure perdue, à refaire

La variante **A200 + entrée** — la plus intéressante, puisqu'elle dirait ce qu'un
gros réservoir ajoute quand on lui donne aussi l'accès direct — **n'a pas été
obtenue** : le processus a été tué avant la fin. Cause : je l'ai lancé avec
`nohup … &` **sans `setsid`**, et il n'a pas survécu à la sortie du shell. C'est la
deuxième fois dans cette session qu'un lancement sans `setsid`/`disown` coûte une
mesure ; la règle est désormais explicite. À relancer.


---
