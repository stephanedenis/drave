> Campagne : **toutes-langues** · expérience **88**
> Titre : 88. CORRECTION DU §87.3 : l'écart d'énergie n'est pas un défaut, c'est une échelle
> Date réelle : **2026-10-07 12:13 HAE** (source : commit `9d47dcc`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 88. CORRECTION DU §87.3 : l'écart d'énergie n'est pas un défaut, c'est une échelle

### 88.1 Ce que j'avais écrit, et pourquoi c'est faux

Le §87.3 concluait, en gras :

> *« Nous atteignons 136 % du RAPPORT avec 3,4 % de l'énergie de contenu et 2,5 % de
> l'énergie de langue. […] Il ne l'atteint pas — il atteint son quotient. »*

**C'est faux, et le §67 le disait déjà.** `P_lang` et `P_cont` sont l'un et l'autre
**quadratiques en l'amplitude**. Multiplier la sortie par une constante α multiplie les deux
énergies par α² — donc **laisse leur rapport exactement inchangé**, et laisse la fidélité
inchangée aussi, puisque c'est un cosinus par ligne.

**Une énergie absolue n'est donc pas une mesure : c'est une mesure À UNE ÉCHELLE PRÈS, et
cette échelle ne coûte rien.** Comparer nos deux énergies brutes à celles du professeur
revient à compter comme un défaut ce qui se corrige en multipliant par un nombre.

### 88.2 La mesure, et non l'argument

Le §87.3 était un raisonnement ; voici le chiffre. Même montage que le §87 (discriminant de
rang 2 appris sur les 47 articles d'apprentissage, mesuré sur les 24 articles de test), en
ramenant `P_cont` à celui du professeur :

| | P_lang | P_cont | RAPPORT | part du rapport | critère §62.3 |
|---|---:|---:|---:|---:|---|
| professeur | 2 410,7 | 2 605,5 | 1,081 | 100 % | — |
| notre pont, rang 2, brut | 60,5 | 89,2 | 1,474 | 136,4 % | — |
| **notre pont, rang 2, amplifié ×5,40** | **1 767,9** | **2 605,5** | **1,474** | **136,4 %** | **satisfait** (P_lang 73 %) |
| notre pont, rang 5, amplifié ×4,64 | 2 862,2 | 2 605,5 | 0,910 | 84,2 % | échoue (P_lang 119 %) |

**L'amplification ×5,40 porte `P_cont` à 2 605,5 — exactement celui du professeur — et laisse
le rapport à 1,474.** Les deux lignes du milieu sont le même résultat écrit à deux échelles.

### 88.3 Ce que le critère du §62.3 devient, une fois l'échelle retirée

Le §62.3 demande : *« `P_cont` proche du professeur ET `P_lang` qui ne le dépasse pas »*.
Après amplification, `P_cont` vaut 100 % par construction, et

    P_lang_amplifié = (P_lang / P_cont) × P_cont_professeur.

La condition « `P_lang` ≤ `P_lang` du professeur » s'écrit donc

    (P_lang / P_cont) × P_cont_prof ≤ P_lang_prof   ⟺   P_cont / P_lang ≥ P_cont_prof / P_lang_prof.

**Le critère du §62.3 est exactement « notre rapport ≥ celui du professeur » — ni plus, ni
moins.** Les deux énergies n'ajoutent rien au rapport. Toute la discussion d'énergie des
§62, §75 et §87 se réduit à une inégalité sur le rapport.

### 88.4 La cinquième fois, et la deuxième de ma main

Le §81.6, le §84.1 et le §86.5 avaient relevé quatre chiffres indexés sur un choix non
déclaré. En voici un cinquième — et il a une forme nouvelle, parce que **ce n'est pas un
chiffre mal mesuré, c'est un chiffre qui ne mesure rien** : une quantité définie à une
transformation près qui ne coûte rien.

> **Une quantité invariante par une transformation gratuite n'est pas une mesure.** Avant de
> comparer deux énergies, vérifier qu'on ne compare pas deux échelles.

La règle des §81.6, §84.1 et §86.5 s'allonge d'un cinquième terme : *nommer la graine, le
panel, le pooling, l'ajustement — et l'échelle.*

### 88.5 Un vrai résultat, trouvé en cherchant l'énergie : **centrer la cible est un gain gratuit**

La même expérience a testé quatre transformations de la cible, toutes **convexes et en forme
fermée**, sur le panel 6 langues (47 articles appris, 24 testés, 120 neurones, ride 0,03) :

| variante | fid TEST | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| professeur | — | 2 410,7 | 2 605,5 | **1,081** |
| A — référence (moindres carrés sur Y) | 0,4910 | 1 549,4 | 359,2 | **0,232** |
| **B — cible centrée** | **0,5002** | 107,8 | 202,3 | **1,877** |
| C — lignes normées | 0,4217 | 9,2 | 286,0 | **31,240** |
| D — blanchiment 0,25 | 0,4464 | 38,4 | 8,3 | 0,216 |
| D — blanchiment 0,50 | 0,4254 | 1,3 | 0,3 | 0,240 |

**B fait mieux sur les DEUX tableaux à la fois** : fidélité 0,5002 contre 0,4910 (+0,009) et
rapport 1,877 contre 0,232 (**×8,1**). Ce n'est pas un compromis, c'est une domination — et
elle est **convexe, en forme fermée, sans rétropropagation**, donc elle respecte le mandat.

**Pourquoi, et c'est l'hypothèse du §58 qui se vérifie.** La cible a une masse commune
énorme et une structure fine. En ajustant la cible **centrée sur chaque entrée**, la lecture
n'est plus payée pour reproduire le niveau moyen de l'entrée — niveau où vit largement la
langue. Elle se consacre aux écarts, qui portent le contenu. `P_lang` tombe de 1 549 à 108
tandis que `P_cont` ne tombe que de 359 à 202.

**Réserve, et elle est sérieuse** : ce chiffre est mesuré sur **47 articles d'apprentissage**,
soit un panel dix fois plus petit que celui du §79 — or le §79 a précisément montré qu'un
effet mesuré à 85 articles ne s'était pas répliqué à 482. **B doit être répliqué avant d'être
cru**, et la réplication est la prochaine mesure.

> **RÉPLIQUÉ AU §90, ET LE RÉSULTAT EST PARTAGÉ.** Sur 482 articles, le gain de **fidélité**
> tient (+0,0062 après +0,0092) ; le gain de **rapport** s'inverse (×0,81 après ×8,1).
> Le tableau ci-dessus ne doit donc pas être lu seul : **la ligne B y est un effet de petit
> panel pour ce qui est du rapport.**

---
