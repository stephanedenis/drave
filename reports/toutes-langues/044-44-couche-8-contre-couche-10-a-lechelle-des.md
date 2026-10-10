> Campagne : **toutes-langues** · expérience **44**
> Titre : 44. Couche 8 contre couche 10 à l'échelle des 392 langues : 41 sur 41, zéro régression
> Date réelle : **2026-10-06 13:48 HAE** (source : commit `817ca1b`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 44. Couche 8 contre couche 10 à l'échelle des 392 langues : 41 sur 41, zéro régression

Le traçage de la couche 8 est terminé (§42) et l'analyse a tourné **avec exactement le
même code, le même périmètre et les mêmes quatre mesures** que la couche 10 — les
deux profils ont été recalculés dans la même exécution, précisément pour que la
comparaison soit légitime.

**Protocole complet** : 351 langues d'apprentissage (300 d'ajustement + 51 de
validation), 41 langues de test hors vivier, 896 canaux, 40 neurones, 1 couche,
80 caractéristiques, fit sur 300 langues, évaluation entière.

### 44.1 Le tableau

| | couche 10 | **couche 8** | écart |
|---|---:|---:|---:|
| fidélité **TEST** (hors vivier) | 0,5960 | **0,6424** | **+0,0464** |
| fidélité **VALIDATION** (même vivier) | 0,6206 | **0,6768** | +0,0562 |
| témoin constant sur TEST | 0,5678 | 0,6049 | +0,0371 |
| **apport propre TEST** | +0,0282 | **+0,0375** | **+0,0093** |
| apport propre VALIDATION | +0,0317 | +0,0328 | +0,0011 |
| oracle TEST | 0,6935 | **0,7427** | +0,0492 |
| **écart à l'oracle TEST** | **+0,0975** | **+0,1003** | +0,0028 |
| écart à l'oracle VALIDATION | +0,0112 | +0,0121 | +0,0009 |
| invariance du **professeur** | 0,6529 | **0,6836** | +0,0307 |
| invariance de **notre sortie** | 0,9565 | 0,9483 | −0,0082 |
| **pire paire** du professeur | 0,0478 | **0,0104** | |
| **pire paire** de notre sortie | 0,7371 | 0,6798 | −0,0573 |
| corrélation apport ↔ fragmentation | +0,7986 (R² 0,64) | +0,8175 (R² 0,67) | |
| corrélation oracle ↔ norme | −0,8368 | −0,8022 | |

### 44.2 Le résultat sans ambiguïté : 41 sur 41

Langue par langue, sur les 41 langues de test :

- **apport propre : 41 langues améliorées, 0 dégradée**, gain moyen **+0,0112** ;
- **oracle : 41 améliorées, 0 dégradée**, gain moyen **+0,0492**.

Ce n'est pas une moyenne qui monte en cachant des pertes : **aucune langue ne perd.**
C'est la mesure la plus nette de la session.

Et les langues les plus mal servies sont celles qui gagnent le plus :

| langue | apport L10 | apport L8 | effet | oracle L10 → L8 |
|---|---:|---:|---:|---|
| **amh** | +0,0535 | +0,0880 | **+0,0345** | 0,7538 → 0,7814 |
| **csw** | +0,0639 | +0,0980 | **+0,0342** | 0,7859 → 0,8333 |
| **dzo** | +0,0885 | +0,1219 | **+0,0334** | 0,7907 → 0,8108 |
| mya | +0,0769 | +0,1018 | +0,0250 | 0,7515 → 0,7661 |
| lao | +0,0379 | +0,0609 | +0,0230 | 0,7450 → 0,7782 |
| tha | +0,0208 | +0,0437 | +0,0229 | 0,6374 → 0,6840 |
| **heb** | +0,0014 | +0,0099 | **+0,0085** | 0,5916 → 0,6412 |
| … | | | | |
| **deu** | +0,0133 | +0,0146 | +0,0012 | 0,5388 → 0,5676 |
| **jpn** | +0,0216 | +0,0218 | **+0,0002** | 0,5747 → 0,5964 |
| **srp** | +0,0128 | +0,0140 | +0,0012 | 0,5615 → 0,6144 |

`heb` multiplie son apport par **7**, `csw` et `amh` gagnent +0,034. Les trois langues
que rien ne servait (`deu`, `jpn`, `srp`) gagnent peu — **elles restent le noyau dur.**

### 44.3 Ce que la couche 8 NE règle PAS : le transfert

**L'écart à l'oracle est inchangé : +0,0975 à la couche 10, +0,1003 à la couche 8.**
Dans le vivier, il reste à +0,012. Autrement dit :

> **le goulot de transfert identifié au §36 est structurel — il ne dépend pas de la
> couche visée.** Changer de cible améliore tout le monde uniformément, mais ne
> réduit pas d'un iota l'écart entre ce que nos caractéristiques permettent (oracle)
> et ce que notre lecture partagée en tire.

C'est un résultat négatif précis, et il oriente : la question n'est plus « quelle
couche », ni « combien de neurones », mais **« qu'est-ce qui, dans nos états, ne
transfère pas d'une langue à l'autre »**.

### 44.4 Deux réserves qui comptent

**1. Les deux tiers du gain brut sont le témoin, pas le pont.** La fidélité TEST gagne
+0,0464, mais le **témoin constant** gagne +0,0371 à lui seul (0,5678 → 0,6049) : la
couche 8 est simplement plus prévisible pour tout le monde. L'apport **propre** du
pont ne gagne que **+0,0093**. C'est réel, mais six fois plus petit que le chiffre
brut.

**2. La pire paire du professeur EMPIRE à la couche 8 : 0,0104 contre 0,0478.** Deux
langues dont les représentations de couche 8 sont quasi orthogonales, là où la couche
10 les rapprochait un peu. Notre sortie, elle, reste à 0,6798 — nous lissons toujours
beaucoup plus que notre cible (§41).

### 44.5 Le multi-échelle, confirmé à l'échelle 392

| | mono-échelle | multi-échelle | effet |
|---|---:|---:|---:|
| apport TEST (couche 8) | +0,0375 | **+0,0406** | +0,0031 |
| apport TEST (couche 10) | +0,0282 | +0,0307 | +0,0025 |
| corrélation effet ↔ fragmentation | | | −0,3094 |

Le gain est du même ordre qu'au §28 (+0,0025), la corrélation avec la fragmentation
reste **faible** (−0,31) : la prédiction d'origine n'est toujours pas confirmée.

### 44.6 Verdict

**La couche 8 est la bonne cible, et c'est maintenant établi à l'échelle des 392
langues, sur deux panneaux, avec 41 langues sur 41 qui s'améliorent et aucune qui
régresse.** Le gain propre est de +0,0093 à +0,0112 selon la mesure ; le gain d'oracle
de +0,0492.

Mais **la couche 8 ne réduit pas le goulot de transfert**, et c'est désormais la
question centrale.


---
