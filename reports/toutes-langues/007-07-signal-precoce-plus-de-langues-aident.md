> Campagne : **toutes-langues** · expérience **07**
> Titre : 7. Signal précoce : PLUS DE LANGUES AIDENT
> Date réelle : **2026-10-06 00:10 HAE** (source : commit `1a42f81`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 7. Signal précoce : PLUS DE LANGUES AIDENT

Mesure prise sur les 133 premières langues tracées, **avant** la fin du traçage —
pour ne pas attendre deux heures si la réponse était déjà lisible. Même validation
(12 langues), même test (9 langues), **seul le nombre de langues d'apprentissage
change**.

| | **30 langues** | **112 langues** | gain |
|---|---:|---:|---:|
| fidélité TEST | 0,7029 | **0,7105** | **+0,0076** |
| fidélité VALIDATION | 0,7450 | **0,7478** | +0,0028 |
| invariance TEST | 0,9787 | **0,9809** | +0,0022 |
| pire paire | 0,9267 | **0,9309** | +0,0042 |
| écart oracle TEST | +0,0347 | **+0,0299** | −0,0048 |
| écart oracle VALIDATION | +0,0240 | +0,0231 | −0,0009 |
| constante témoin | 0,6907 | 0,6955 | +0,0048 |
| **écart à la constante** | **+0,0122** | **+0,0150** | **+23 %** |

**Cela contredit ma mesure antérieure.** Sur la plage 20 → 30 → 36 langues, l'effet
était **nul**, et j'en avais conclu que le nombre de langues ne comptait pas. À
112 langues, l'avantage sur la constante progresse de **23 %**.

**L'effet existe donc, mais il n'apparaît qu'à plus grande échelle** : entre 20 et
36 langues il est sous le bruit, à 112 il devient visible.

**Réserve à ne pas oublier** : le test ne compte que **9 langues** à ce stade (41
quand tout sera tracé). Le gain de +0,0076 porte donc sur un panel mince, et c'est
l'**écart à la constante** — qui corrige la difficulté du panel — qu'il faut
regarder : **+0,0122 → +0,0150**.

Un détail structurel au passage : la naissance libre trouve ici **40 neurones en
1 SEULE couche** dans les deux cas, là où le panel à 46 langues donnait
[30, 8, 8, 8, 8, 8, 8, 2]. La hiérarchie dépend donc bien des données.


---
