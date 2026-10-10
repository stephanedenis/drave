> Campagne : **toutes-langues** · expérience **37**
> Titre : 37. Le ride était dix fois trop fort — et l'écart de transfert n'est pas du sur-apprentissage
> Date réelle : **2026-10-06 11:58 HAE** (source : commit `1404bac`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 37. Le ride était dix fois trop fort — et l'écart de transfert n'est pas du sur-apprentissage

### 37.1 Balayage du ride, deux panneaux

Prédiction écrite avant la mesure : si la lecture sur-apprend le vivier, augmenter le
ride doit **réduire l'écart à l'oracle hors vivier**. Mesuré (40 neurones, 1 couche,
80 caractéristiques, 896 canaux, 300 langues d'ajustement / 51 de validation / 41 de
test) :

| ride | VALID fid | VALID écart | TEST fid | TEST écart |
|---:|---:|---:|---:|---:|
| 0,0003 | 0,6301 | +0,0191 | 0,6204 | +0,0468 |
| 0,001 | 0,6302 | +0,0190 | 0,6207 | +0,0465 |
| 0,003 | 0,6304 | +0,0187 | 0,6212 | +0,0458 |
| 0,01 | **0,6307** | +0,0177 | 0,6224 | +0,0440 |
| **0,03** | 0,6304 | +0,0159 | **0,6233** | +0,0409 |
| 0,1 | 0,6274 | +0,0133 | 0,6220 | +0,0364 |
| **0,3 (valeur du pont)** | 0,6206 | +0,0112 | 0,6159 | +0,0329 |
| 1,0 | 0,6106 | +0,0087 | 0,6044 | +0,0303 |
| 3,0 | 0,6022 | +0,0060 | 0,5930 | +0,0279 |
| 10 | 0,5964 | +0,0031 | 0,5842 | +0,0195 |
| 30 | 0,5940 | +0,0013 | 0,5804 | +0,0097 |

**L'écart diminue bien (+0,047 → +0,010), MAIS parce que les deux baissent** —
l'oracle chute plus vite que nous. **La prédiction est réfutée : le transfert manquant
n'est pas du sur-apprentissage de la lecture.**

### 37.2 Le gain gratuit : le ride de 0,3 est 10 à 30 fois trop fort

La fidélité TEST est **maximale à ride 0,03** (0,6233) et la validation à 0,01
(0,6307). À la valeur utilisée jusqu'ici (0,3) elles valent 0,6159 et 0,6206 :

| | ride 0,3 (actuel) | ride 0,03 | gain |
|---|---:|---:|---:|
| fidélité TEST | 0,6159 | **0,6233** | **+0,0074** |
| fidélité VALIDATION | 0,6206 | 0,6304 | +0,0098 |

C'est **+0,0074 gratuit**, sans un neurone de plus, sans apprentissage — le ride
n'avait jamais été balayé sur ce critère. En dessous de 0,01 la qualité retombe
(0,6204 à 0,0003) : l'optimum est un vrai maximum, pas un bord.

L'ancien 0,3 avait probablement été choisi sur un périmètre plus petit, et n'a jamais
été réexaminé. **Il faut le remplacer par 0,03.**

---
