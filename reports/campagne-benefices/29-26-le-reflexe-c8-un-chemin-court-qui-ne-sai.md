> Campagne : **campagne-benefices** · expérience **26**
> Titre : 26. Le réflexe (C8) : un chemin court qui ne sait RIEN, et pourquoi
> Date réelle : **2026-10-09 23:39 HAE** (source : commit `f8ac10e`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 26. Le réflexe (C8) : un chemin court qui ne sait RIEN, et pourquoi

Un réflexe médullaire ne remonte pas au cortex : il répond par un chemin court. Dans
le moteur, ce chemin existe déjà — `--couches 0,L` tronque le modèle et
`--tete-partielle` applique la tête à la fin de la plage. La question mesurable n'est
donc pas « peut-on faire un réflexe ? » mais **« à partir de quelle profondeur un
réflexe tombe-t-il d'accord avec le modèle entier ? »**. Mesuré sur Qwen2.5-0.5B-Q8
(24 couches), 32 jetons réels, `--reflexe-essai` :

| couches | accord | accord top-5 | **cos(état tronqué, état final)** | ms/jeton | plus rapide |
|---|---|---|---|---|---|
| 1 | 0,0 % | 0,0 % | 0,044 | 4,5 | 18,5× |
| 2 | 3,1 % | 3,1 % | −0,009 | 7,0 | 11,9× |
| 4 | 0,0 % | 0,0 % | 0,013 | 16,7 | 4,9× |
| 8 | 0,0 % | 0,0 % | 0,058 | 32,3 | 2,6× |
| 12 | 0,0 % | 0,0 % | 0,083 | 49,6 | 1,7× |
| 16 | 0,0 % | 0,0 % | 0,145 | 61,7 | 1,3× |
| 20 | 6,2 % | 15,6 % | 0,320 | 79,8 | 1,0× |
| **24** | **100,0 %** | 100,0 % | **1,000** | 93,2 | — |

**Il n'y a pas de sortie précoce utilisable dans ce modèle** : jusqu'à 16 couches sur
24 (deux tiers de la profondeur), l'accord avec le modèle entier est de **0 %**, et il
ne décolle qu'à 24 — c'est-à-dire quand le réflexe *est* le modèle. Le gain de temps,
lui, est bien réel (une couche est 18,5× plus rapide) : l'échec n'est pas un artefact
de mesure.

**Et la cause est mesurée, pas supposée** : la **cosinus** entre l'état tronqué et
l'état final vaut 0,044 à une couche, **0,145 à seize** et 1,000 à vingt-quatre.
L'état intermédiaire est **presque orthogonal** à l'état final — la tête du modèle est
celle de sa dernière couche, et lit une direction que seules les dernières couches
produisent. Un réflexe court ne peut donc pas réutiliser cette tête : il lui faudrait
sa **propre** lecture entraînée (un petit module sur l'entrée), ce que le moteur ne
sait pas produire — et c'est un manque, pas un résultat.

**Conséquence pour la distribution** : le découpage en régions ne peut pas s'appuyer
sur une sortie anticipée d'une région pour aller plus vite. La seule sortie valide est
celle de la dernière couche, donc **le chemin est au moins aussi long que le
modèle** — ce que C1/C9 mesurent par ailleurs en latence et en fibres.

**Conditions** : un seul modèle (0,5 B, 24 couches), 32 jetons, sortie précoce **sans
tête dédiée**, accord mesuré sur le jeton de plus forte probabilité (la calibration de
la distribution tronquée n'est pas mesurée). Un modèle plus profond ou entraîné
autrement pourrait se comporter différemment : c'est une mesure, pas une loi.
