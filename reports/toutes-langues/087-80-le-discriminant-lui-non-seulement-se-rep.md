> Campagne : **toutes-langues** · expérience **80**
> Titre : 80. Le discriminant, lui, NON SEULEMENT se réplique — il DÉPASSE le professeur
> Date réelle : **2026-10-07 08:33 HAE** (source : commit `3d76ede`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 80. Le discriminant, lui, NON SEULEMENT se réplique — il DÉPASSE le professeur

Le §79 venait de réfuter le mécanisme du §73 à 482 articles. Restait à tester l'autre :
le **discriminant** du §69. Réponse, sur les 1 446 entrées de test :

| | fid TEST | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| rang 0 (référence, centrage seul) | **0,4713** | 39,8 | 98,9 | 2,487 |
| **discriminant rang 2** | 0,4334 | 3,6 | 45,0 | **12,645** |
| discriminant rang 5 | 0,4420 | 12,5 | 56,2 | 4,502 |
| discriminant rang 20 | 0,4584 | 18,3 | 75,0 | 4,100 |
| **PROFESSEUR** | — | *387,9* | *4 655,4* | ***12,001*** |

### 80.1 Le résultat

**Rapport 12,645 contre 12,001 pour le professeur : 105 % de la cible.**

Et le contraste avec les 85 articles est instructif :

| | à 85 articles | à **482 articles** |
|---|---:|---:|
| professeur | 10,912 | **12,001** |
| discriminant rang 2 | 6,961 (**64 %**) | **12,645 (105 %)** |

**Le mécanisme ne se contente pas de tenir à grande échelle : il y gagne.** À 85 articles
il atteignait 64 % de la cible, à 482 il la dépasse de 5 %.

**Le coût en fidélité est de 0,038** (0,4713 → 0,4334) — du même ordre que celui mesuré à
85 articles (0,4703 → 0,4341, soit 0,036). **Le coût, lui, est stable.**

### 80.2 Ce que cela discrimine, et c'est le vrai apport de cette vérification

Les deux mécanismes testés à 482 articles se comportent **différemment** :

| mécanisme | à 85 articles | à 482 articles | verdict |
|---|---:|---:|---|
| **apprendre quoi lire** (§73) | 1,934 → **2,411** | 2,487 → **1,759** | **NE se réplique PAS** |
| **discriminant** (§69) | 1,934 → **6,961** (64 %) | 2,487 → **12,645** (105 %) | **SE RÉPLIQUE et s'améliore** |

**Le mécanisme qui survit est celui qui agit sur la LECTURE, pas celui qui agit sur les
caractéristiques.** C'est cohérent avec le §70 : la langue entre par l'entrée, et modifier
ce que lisent les neurones ne fait que redistribuer le problème. **Le discriminant, lui,
optimise directement la quantité qu'on mesure** — et cela se transfère, parce que c'est un
changement de directions dans l'espace de sortie, pas une reconstruction des
caractéristiques.

### 80.3 Le résultat final, et il est positif

**Sur le corpus Wikipedia complet — 482 articles × 6 langues, 1 446 entrées de test — une
analyse discriminante linéaire appliquée à la sortie du pont atteint un rapport
contenu/langue de 12,645 contre 12,001 pour le professeur, pour 0,038 de fidélité.**

C'est **en forme fermée**, **sans rétropropagation**, **déployable** (matrice fixe apprise
sur l'apprentissage), et **cela ne demande ni neurone supplémentaire ni couche
supplémentaire**.

**Ce que cela ne règle pas** : `P_cont` reste à 45,0 contre 4 655,4 pour le professeur —
**cent fois moins**. Le rapport est dépassé, l'énergie de contenu ne l'est pas. Et le §77
a établi que l'amplification qui les rapprocherait coûte la fidélité, de façon monotone.

### 80.4 La conclusion du rapport, corrigée une dernière fois

Le §79 terminait sur la réfutation du §73 et annonçait que « la cible » n'était pas
répliquée. **C'était vrai pour un mécanisme, pas pour l'autre.** Le rapport se termine donc
sur :

- **un mécanisme qui échoue à grande échelle** — apprendre quoi lire (§73, §79) ;
- **un mécanisme qui réussit et s'améliore** — le discriminant (§69, §80), à **105 % du
  rapport du professeur** ;
- **une frontière inchangée** — la structure s'obtient, l'énergie de contenu ne suit pas
  (§76, §77) ;
- **une question ouverte, seule** : quel mécanisme, sous les contraintes du projet, peut
  produire la transformation couche 0 → couche 8 et **porter l'énergie de contenu** du
  professeur ?


---

# CLÔTURE — l'objectif, exigence par exigence

> **AVERTISSEMENT.** Les §82 à §86, écrits après cette clôture, corrigent la cible qui y
> est citée (12,001 est un chiffre à trois langues romanes) et le sort du discriminant
> (105 % dans-panel, 31–55 % hors vivier). Voir l'avertissement placé au début du BILAN.
