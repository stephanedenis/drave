> Campagne : **toutes-langues** · expérience **63**
> Titre : 63. Cinquième remède écarté : le sous-espace du contenu appris ne se TRANSFÈRE pas
> Date réelle : **2026-10-06 21:41 HAE** (source : commit `7414653`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 63. Cinquième remède écarté : le sous-espace du contenu appris ne se TRANSFÈRE pas

### 63.1 L'idée, et elle était la bonne sur le papier

Le §62 avait trouvé le remède mais l'avait déclaré non déployable : amplifier l'axe du
contenu exige de savoir **quelles entrées partagent un contenu**. L'objection était
juste — mais elle ne vaut qu'à l'**inférence**. À l'**apprentissage**, ce regroupement
existe.

On apprend donc, **une fois pour toutes sur les données d'apprentissage** :
1. le **sous-espace du contenu** — l'espace engendré par les écarts `μ_k − m̄` ;
2. un **projecteur** `Π` sur ce sous-espace (85 directions, **100 % de l'énergie**
   captée).

Puis, à l'inférence, sur la sortie d'un texte neuf : `O + (γ−1)·Π·(O − m̄)`. `Π` est
une **matrice fixe** de 896×896 : aucun regroupement n'est demandé au texte neuf.

### 63.2 Le résultat : le rapport reste figé

| γ | rang | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|---:|
| 1,00 | 85 | **0,4747** | 232,0 | 338,7 | **1,460** |
| 1,50 | 85 | 0,4720 | 508,3 | 752,0 | 1,480 |
| 2,00 | 85 | 0,4664 | 895,0 | 1 330,6 | 1,487 |
| 5,00 | 85 | 0,4015 | 5 536,2 | 8 274,3 | 1,495 |
| | | | | **professeur 4 356** | **professeur 10,912** |

**Le rapport passe de 1,460 à 1,495 en multipliant γ par cinq.** Les deux axes montent
**ensemble**. Le sous-espace appris n'isole pas le contenu sur le panel de test.

### 63.3 Pourquoi — et c'est cohérent avec tout le reste

Le détail qui explique tout : **les articles du test sont LES MÊMES que ceux de
l'apprentissage.** Le partage a été fait par **langue** (de/en/fr apprises, es/it/pt en
test), pas par article — donc les contenus sont partagés. Le sous-espace du contenu
*devrait* se transférer.

**Il ne se transfère pas parce que les sorties des langues INCONNUES sont décalées.**
Le sous-espace du contenu est appris sur des moyennes calculées sur de/en/fr ; sur
es/it/pt ces moyennes sont ailleurs. C'est **le même décalage de transfert que le §36**
— l'écart à l'oracle hors vivier — qui revient, cette fois sous la forme d'un
sous-espace qui ne s'applique plus.

**Le remède ne peut donc pas être appris sur les langues connues et appliqué aux
inconnues.** Il doit être soit **par langue** (mais une langue inconnue n'a pas de
statistiques), soit **structurellement indépendant de la langue** — et c'est une
exigence beaucoup plus forte.

### 63.4 Une étiquette fausse dans ma propre sortie

La première version affichait `# professeur (TEST) : P_lang 232,0 · P_cont 338,7`.
**Ces chiffres sont ceux de NOTRE sortie**, pas du professeur. Je passais nos sorties à
la fonction de décomposition et j'étiquetais le résultat « professeur ». Corrigé : les
deux sont maintenant calculés et affichés côte à côte.

C'est la deuxième fois de la session qu'une sortie d'outil porte une étiquette fausse
(après le tableau trié recopié dans le mauvais ordre, §27.7). Un chiffre juste sous un
nom faux est plus dangereux qu'un chiffre faux : il passe la relecture.

### 63.5 La série complète, et ce qu'elle établit

| § | piste | verdict |
|---|---|---|
| 58 | objectif à deux curseurs | atteint la cible, mais **non convexe**, non monotone, cible instable |
| 59 | pondération (centrage, normalisation, blanchiment) | **écartée** — prémisse réfutée par le spectre |
| 60 | rétrécissement global | **réel (3,4×)**, mais l'amplifier uniformément ne change pas l'ordre |
| 61 | décomposition de variance | **défaut localisé** : 12× moins d'énergie de contenu |
| 62 | amplification ciblée | **fonctionne** (β=3 → la magnitude du professeur, coût 0,006) |
| 62 | version déployable (moyenne par entrée) | **échoue** — mêle les deux axes |
| 62 | `μ_lang` | **échoue** — comprime les deux |
| 63 | sous-espace du contenu appris | **échoue** — ne se transfère pas aux langues inconnues |

**Cinq remèdes écartés, chacun par une mesure, et un défaut localisé avec un chiffre.**
La question s'est resserrée à ceci : *l'énergie de contenu est sous-produite d'un
facteur ~3,6 et récupérable par mise à l'échelle, mais tout ce qui permet de l'isoler
dépend de la langue — donc ne passe pas aux langues inconnues.*


---
