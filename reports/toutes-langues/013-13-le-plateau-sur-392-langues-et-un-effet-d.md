> Campagne : **toutes-langues** · expérience **13**
> Titre : 13. Le plateau sur 392 langues, et un effet de panel qui corrige une mesure antérieure
> Date réelle : **2026-10-06 03:17 HAE** (source : commit `e85847a`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 13. Le plateau sur 392 langues, et un effet de panel qui corrige une mesure antérieure

Mesure faite sur les **392 langues**, dernière position, couche 10 :

| | |
|---|---:|
| **50 % de l'énergie** | **40 canaux sur 896 (4 %)** |
| 90 % de l'énergie | 298 (33 %) |
| 99 % de l'énergie | 597 (67 %) |
| canaux actifs dans **au moins une** langue | **896 / 896** |
| **canaux actifs dans TOUTES les langues** | **48 / 896 (5 %)** |

### Ce qui tient, et ce qui s'effondre

**Ce qui tient** : la couche est **creuse** — 40 canaux sur 896 portent la moitié de
l'énergie. C'était déjà le chiffre mesuré sur l'ancien panel (34 canaux), il est
confirmé à 392 langues. La conclusion qualitative est solide.

**Ce qui s'effondre** : le « sous-ensemble partagé ». Sur 6 langues je mesurais
**678 canaux actifs dans toutes** ; sur **392 langues, il n'en reste que 48**.
Autrement dit **95 % des canaux ne sont pas universellement actifs** — ils
dépendent de la langue à la dernière position.

**C'était une borne supérieure optimiste.** Avec 6 langues, un canal n'avait que 6
occasions d'être absent ; avec 392, il en a 392. La mesure ne grandit pas avec le
panel, elle **se resserre**. Toute affirmation du type « ce canal est partagé par
toutes les langues » doit donc dire **sur combien de langues elle a été vérifiée** —
sinon elle ne veut rien dire.

### Et l'écart test/validation, à pleine échelle

Sur le panel complet de **41 langues de test couvrant les 22 écritures** :

| neurones | fid appr | fid VAL | **fid TEST** | invariance | pire paire |
|---:|---:|---:|---:|---:|---:|
| 33 | 0,7445 | 0,7494 | 0,7411 | 0,9865 | 0,9320 |
| 37 | 0,7453 | 0,7502 | **0,7428** | 0,9838 | 0,9192 |

**Rapport test/validation : 1,01** — contre **2,58** sur l'ancien panel uniquement
non latin. Le diagnostic de typologie est donc confirmé **à pleine échelle**, et
pas seulement sur le signal précoce.

`communs` reste à **+0,233** avec 14-15 % des neurones au-dessus du seuil de 0,35 :
le critère n'ouvre pas de couche, le réseau reste à **1 couche** — résultat qui, on
le sait maintenant, n'est pas optimal (l'optimum mesuré est 0,25, +22 % d'écart à
la constante).


---
