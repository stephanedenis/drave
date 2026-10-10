> Campagne : **toutes-langues** · expérience **90**
> Titre : 90. LA RÉPLICATION DU §88.5 : le gain de fidélité tient, le gain de rapport s'inverse
> Date réelle : **2026-10-07 12:34 HAE** (source : commit `370ed3b`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 90. LA RÉPLICATION DU §88.5 : le gain de fidélité tient, le gain de rapport s'inverse

### 90.1 Pourquoi j'ai répliqué avant d'y croire

Le §88.5 annonçait que **centrer la cible sur chaque entrée** dominait la référence sur les
deux tableaux — fidélité *et* rapport — en restant convexe et en forme fermée. Le chiffre
était spectaculaire : rapport **1,877 contre 0,232**, soit ×8,1.

Mais il portait sur **47 articles d'apprentissage**. Or le §79 avait précisément établi
qu'un effet mesuré à 85 articles ne s'était pas répliqué à 482. La réserve était écrite dans
le §88.5 ; voici la réplication.

### 90.2 La réplication, sur 482 articles

Même outil, même protocole (120 neurones, quadratique, ride 0,03, graine 5), mais sur
`cache_vf_train.npz` → `cache_vf_test.npz` : **1 446 entrées d'apprentissage, 1 446 de test,
482 articles**, de/en/fr appris, es/it/pt mesuré.

| | fid TEST | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| professeur | — | 387,9 | 4 655,4 | **12,001** |
| A — référence | 0,4689 | 246,0 | 423,8 | **1,723** |
| B — cible centrée | **0,4751** | 168,8 | 236,3 | **1,400** |

Et les deux panels côte à côte :

| | fid A → B | **rapport A → B** |
|---|---|---|
| 47 articles, 6 langues (§88.5) | 0,4910 → 0,5002 (**+0,0092**) | 0,232 → 1,877 (**×8,1**) |
| **482 articles, 3+3 langues** | 0,4689 → 0,4751 (**+0,0062**) | 1,723 → 1,400 (**×0,81**) |

### 90.3 Le verdict, en deux lignes

**Le gain de FIDÉLITÉ se réplique.** +0,0092 puis +0,0062, même signe, même ordre de
grandeur. Rapporté à l'écart-type entre graines du §81 (**0,0013**), cela fait **5 à 7 fois
l'écart-type** : c'est un effet réel, et il est gratuit — centrer la cible est une
opération convexe en forme fermée qui **améliore la fidélité sans rien coûter**.

**Le gain de RAPPORT ne se réplique PAS — il s'inverse.** ×8,1 à 47 articles, ×0,81 à 482.
Un effet qui change de signe en changeant de panel n'est pas un mécanisme.

### 90.4 Pourquoi, et c'est cohérent avec le §88

B **abaisse les deux énergies** : `P_lang` 246,0 → 168,8 et `P_cont` 423,8 → 236,3. Il ne
« sépare » donc rien : il atténue tout, et **le rapport est le quotient de deux quantités
atténuées**. Selon le panel, le dénominateur baisse plus vite que le numérateur (rapport qui
monte, 47 articles) ou l'inverse (rapport qui baisse, 482 articles).

C'est exactement la leçon du §88 : **le rapport est un quotient, et un quotient de deux
choses qui changent ensemble ne dit pas laquelle a changé.** Le §88 avait montré que
l'échelle était gratuite ; le §90 montre que **l'atténuation l'est presque aussi**, et que
le rapport seul ne sait pas distinguer « séparer mieux » de « atténuer différemment ».

### 90.5 Ce qui reste, et ce que cela dit de la méthode

**Reste acquis** : un gain de fidélité de +0,006 à +0,009, gratuit, convexe, en forme
fermée, répliqué sur deux panels de tailles très différentes. C'est peu, mais c'est solide —
et c'est un levier à ajouter à la lecture de référence.

**Reste perdu** : le gain de rapport du §88.5, et avec lui la formulation « B domine A sur
les deux tableaux ». La bonne formulation est : **B paie moins cher en fidélité, et son
effet sur le rapport dépend du panel.**

**La leçon de méthode, et c'est la septième de la même famille.** Le §88.5 avait écrit sa
réserve (« B doit être répliqué avant d'être cru ») — et la réserve était la bonne. Ce qui
manquait n'était pas la prudence, c'était **le temps de la vérifier avant de publier le
chiffre dans un tableau**.

> **Une réserve écrite n'est pas une réserve tenue.** Si un chiffre mérite une réserve, il
> mérite d'être répliqué *avant* d'entrer dans un tableau de résultats — sinon le tableau le
> fait circuler sans elle.

---
