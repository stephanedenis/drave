> Campagne : **toutes-langues** · expérience **43**
> Titre : 43. Le goulot de la CROISSANCE : 28 s par neurone, ramené à 1,76 s
> Date réelle : **2026-10-06 13:39 HAE** (source : commit `f30b14b`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 43. Le goulot de la CROISSANCE : 28 s par neurone, ramené à 1,76 s

En lisant le code pour lancer l'entraînement complet, j'ai trouvé un coût que
personne n'avait nommé : **`nait` boucle `pour chaque langue : pour chaque pas`**,
soit **472 472 itérations d'interpréteur Python**. Chaque naissance coûtait donc
**28 secondes** — et le mode `--naissance libre` fait **une naissance par neurone**.

### 43.1 La vectorisation, et pourquoi elle est légitime

**Les langues sont indépendantes.** Seule la récurrence en `t` est séquentielle. On
regroupe donc les langues par longueurs voisines et on boucle sur `t`, toutes les
langues du bloc d'un coup. Le calcul est **le même** : c'est une vectorisation, pas un
changement d'algorithme.

### 43.2 Identité bit à bit — vérifiée, pas supposée

Comparaison avec l'ancienne boucle recopiée telle quelle, sur 25 langues réelles,
pour trois tailles de naissance et trois tailles de bloc :

| k \ bloc | 4 | 16 | 64 |
|---:|---:|---:|---:|
| 1 | **0,000e+00** | **0,000e+00** | **0,000e+00** |
| 7 | **0,000e+00** | **0,000e+00** | **0,000e+00** |
| 40 | **0,000e+00** | **0,000e+00** | **0,000e+00** |

**L'écart maximal est exactement zéro**, pas « petit ». La vectorisation ne change
rien aux trajectoires.

### 43.3 Le gain, sur le corpus complet

351 langues, 472 472 pas :

| langues par bloc | `nait(1)` |
|---:|---:|
| 8 | 2,58 s |
| 16 | 2,07 s |
| **32 (retenu)** | **1,76 s** |
| 64 | 1,67 s |

**×16 sur l'étape centrale de la croissance.** Le mode libre passait de 28 s à 1,76 s
par neurone : 300 neurones coûtaient 2 h 20 de naissances, ils en coûtent 9 minutes.

### 43.4 Ce que cela dit de la question « où va le temps »

C'était **la troisième réponse** à cette question, et chacune a désigné un endroit
différent :

1. le **fit de la lecture** (22 min par ajustement à 1 296 colonnes) — §35 ;
2. la **passe professeur** (4 h 17, faite deux fois par ma faute) — §35.3 et §42 ;
3. la **croissance** (28 s par neurone, ×16 par vectorisation) — ici.

Les trois sont indépendants, et aucun n'était visible sans instrumenter. La
simulation des neurones, soupçonnée la première, n'était le goulot dans aucun des
trois cas.


---
