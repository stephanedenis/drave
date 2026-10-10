> Campagne : **toutes-langues** · expérience **29**
> Titre : 29. Le réservoir ne sert presque à rien — et le vrai témoin n'était pas celui que je croyais
> Date réelle : **2026-10-06 08:55 HAE** (source : commit `e036749`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 29. Le réservoir ne sert presque à rien — et le vrai témoin n'était pas celui que je croyais

Depuis le début, l'apport du pont est mesuré **contre la constante témoin** (`mt`).
C'est un témoin trop faible : il ne dit pas si le pont apporte quelque chose qu'une
**lecture directe de l'entrée du professeur** n'apporterait pas déjà. Je l'ai
mesuré. C'est la remise en cause la plus sérieuse de ce rapport.

### 29.1 Les quatre variantes, même vivier, même périmètre

351 langues d'apprentissage · 41 de test · **896 canaux** · entrée centrée par langue
(calculable à l'inférence) · lecture `[X, X²]`.

| | caractéristiques | fidélité TEST | apport vs constante |
|---|---:|---:|---:|
| témoin constant | 0 | 0,5678 | — |
| **A · 40 neurones récurrents, 1 couche** | 80 | 0,5972 | +0,0294 |
| **C · l'entrée SEULE, ZÉRO neurone** | 1 792 | **0,6536** | **+0,0857** |
| B · réservoir **et** entrée | 1 872 | **0,6609** | +0,0931 |
| D · 2 couches de 20 (même budget) | 80 | 0,5979 | +0,0301 |

### 29.2 Ce que cela dit, sans détour

**Une lecture sans aucun neurone — une simple application quadratique de la couche 0
du professeur — bat le réservoir de 40 neurones de +0,0564.** Et lui ajouter le
réservoir par-dessus ne rapporte plus que **+0,0073**.

Autrement dit : **sur ce périmètre, 40 neurones récurrents valent +0,007. Le pont,
tel qu'il est construit, est pour l'essentiel une sonde sur l'entrée.**

### 29.3 Et les langues « non servies » étaient servies depuis le début

C'est le plus instructif. Les langues pour lesquelles le pont n'apportait rien
(§27) sont précisément celles que la lecture directe sert le mieux :

| langue | apport A (réservoir) | apport C (entrée seule) |
|---|---:|---:|
| **heb** | +0,0014 | **+0,0637** |
| **srp** | +0,0128 | **+0,1005** |
| **deu** | +0,0133 | **+0,1024** |
| **jpn** | +0,0216 | **+0,1224** |
| **kor** | +0,0192 | **+0,0823** |

**L'information n'était pas absente : elle était dans l'entrée, et le réservoir la
détruisait.** L'hypothèse du §27.5 — « les caractéristiques ne portent pas le
contenu de ces langues » — est donc **fausse** : elle confondait « les
caractéristiques du réservoir » avec « les caractéristiques disponibles ». La couche
0 du professeur les porte.

### 29.4 La profondeur n'achète rien

**D (2 couches de 20) = 0,5979** contre **A (1 couche de 40) = 0,5972** : +0,0007,
soit le bruit. À budget de neurones constant, composer une couche de plus n'apporte
rien de mesurable. C'est une réponse — négative — à la question centrale de la
mission, et elle est mesurée.

### 29.5 Ce qui reste debout, et ce qui tombe

**Tombe** : l'idée que l'apport mesuré contre la constante qualifie le réservoir.
Il faut désormais mesurer contre **C**, la lecture directe de l'entrée.

**Reste debout** : toute la mécanique d'attention, d'oracle et de profil par langue,
qui a précisément permis de trouver cela. Et le fait que B (réservoir **et** entrée)
soit le meilleur des cinq — +0,0073 au-dessus de C — donc que le réservoir n'est pas
*nul*, seulement très bon marché à remplacer.

**Reste à établir** : C a 1 792 caractéristiques contre 80 pour A. Une partie de
l'écart peut être de la **capacité**, pas de la nature. Le contrôle qui tranche est
une lecture **linéaire seule** sur l'entrée (896 caractéristiques) et un réservoir
**beaucoup plus large**. C'est la prochaine mesure, et elle est écrite ici avant
d'être faite.

### 29.6 Une réserve de méthode

Le témoin constant n'était pas *faux* — c'est bien lui qui apparaît dans le résultat
de tête (0,7430 contre 0,7207). Mais il était **trop faible pour être informatif** :
il laissait croire que l'écart mesurait le pont, alors qu'il mesurait surtout ce que
la couche 0 contient déjà. Le corriger change la lecture de tous les écarts
« +0,02 à +0,03 » rapportés depuis le début, sans en changer un seul chiffre.

Outil : `tools/leviers_pont.py`.


---
