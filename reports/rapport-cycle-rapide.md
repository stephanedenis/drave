# Le cycle rapide : l'article 1 de l'UDHR dans 399 langues

> 07/10. Réponse à une demande précise : *« peut-on refaire nos exercices sur un
> très petit modèle afin de faire des cycles de tests plus rapides entre les
> couches d'entrée et première couche sémantique ? »*
>
> La réponse est oui, mais **le modèle n'est pas le bon levier** — et c'est
> mesuré, pas supposé.

---

## 1. D'où venait la lenteur, chiffres en main

| poste | ce qui coûtait |
|---|---|
| traçage d'une entrée | **~16 s** sur Wikipedia (un article entier, `ctx 1024`, 9 couches) |
| taille d'une entrée | **~575 positions** (l'article entier, moyenné) |
| ajustement d'un pont | **5 à 10 min** sur 1 446 entrées × 575 positions, parce que la Grammaire `AᵀA` coûte `n·d²` avec `d = 1 792` |

Le coût d'un ajustement est en `n · d²` : **n** = nombre total de positions,
**d** = 2 × dimension cachée. Les deux termes sont attaquables, mais pas au même
prix :

- **diviser `d` par 1,5** (un modèle de 576 cachés au lieu de 896) gagne **×2,4** ;
- **diviser `n` par 20** (une phrase au lieu d'un article) gagne **×20**.

C'est le second qui décide, et il ne demande aucun modèle nouveau.

## 2. Le corpus : l'article 1, pas l'article entier

L'unité d'alignement la plus solide de l'UDHR n'est pas l'article — c'est
**l'article 1**, présent dans toutes les langues, qui dit exactement la même chose
partout, et qui tient en une phrase.

**Ce que `tools/extrait_article1.py` produit** (`udhr_xml/`, 456 fichiers) :

| propriété | valeur |
|---|---|
| fichiers XML | 456 |
| **codes `iso639-3` distincts** | **400** |
| écritures écrasées | **56** — deux fichiers de même code s'écrasent (`und` en porte cinq) |
| langues avec un article 1 exploitable | **399** |
| longueur médiane | **169 caractères** (min 40, max 609) |
| positions par trace | **33 à 176** selon la langue |

Le point à retenir : **456 fichiers ne font pas 456 langues.** Le script comptait
les écritures ; il compte maintenant les codes, et dit les écrasements.

**Un second article est extrait** (`--article 2`, 399 langues aussi, médiane
541 caractères) parce que sans lui, « sémantique » ne veut rien dire : voir §4.

## 3. Le mode de traçage : la vraie économie cachée

Le mode par défaut du moteur construit ses listes d'événements **au chargement** :
sur Qwen2.5-0.5B, **15,6 M d'événements pour ~6 s**, à chaque invocation. Le
calcul par jeton, lui, est identique :

| mode | ms/jeton (mesuré) | temps total d'une trace |
|---|---:|---:|
| défaut (événementiel) | 32,4 | **8,00 s** |
| **`--dense`** | 32,3 | **1,94 s** |

**Même calcul, 6 s de moins par invocation.** Sur 399 langues tracées une par
une, ces 6 secondes fixes font **40 minutes**.

**Mais changer de mode sans le mesurer rendrait le nouveau corpus incomparable à
tout ce que ce dépôt a tracé.** La calibration a donc été faite
(`tools/calibre_modes.py`, 8 langues, 4 écritures) :

| | valeur |
|---|---:|
| cosinus **moyen** entre les deux modes | **0,9964** |
| cosinus **minimum** | 0,9160 |
| 5ᵉ centile | 0,9924 |
| rapport des normes | **1,000** |

**Verdict** : les deux modes tracent la même direction à 0,4 % près en moyenne,
8 % au pire, et à la même amplitude. Un corpus tracé en dense est donc comparable
à un corpus tracé en événementiel — **à condition de le dire**, ce qui est fait
ici.

## 4. La mesure que ce corpus rend possible : la première couche sémantique

Un chiffre qui monte ne prouve rien. La similarité entre les représentations d'une
même phrase dans 399 langues monte avec la profondeur — mais elle monterait aussi
si la couche devenait simplement **anisotrope**, c'est-à-dire si tous les vecteurs
se ressemblaient sans rien savoir du sens.

D'où **deux articles**, et une différence :

    même(c)    = cos( art1 langue i , art1 langue j )      i ≠ j
    autre(c)   = cos( art1 langue i , art2 langue j )      i ≠ j
    SÉPARATION = même(c) − autre(c)

`autre(c)` est le **plancher d'anisotropie** : ce que la couche fait ressembler
sans rien savoir du sens. La couche où la séparation culmine est la **première
couche sémantique** — celle où le modèle a fini de traduire et commence à
raisonner. C'est la cible naturelle d'un pont.

`tools/premiere_couche_semantique.py` la mesure **avec les deux poolings**
(moyenne des positions et dernière position), parce que le §84 du rapport
`rapport-toutes-langues.md` a montré qu'ils ne racontent pas la même histoire —
1,769 contre 6,275 sur le même corpus. S'ils s'accordent ici, la conclusion sera
solide ; s'ils divergent, c'est le pooling qu'il faudra interroger avant la
couche.

## 5. Ce que le cycle coûte maintenant

| étape | avant | après |
|---|---:|---:|
| traçage d'une langue | ~16 s | **3,7 s** |
| traçage du corpus entier | 2 h 30 (300 traces) | **~25 min** (399 langues) |
| positions par entrée | ~575 | **~60** |
| lignes dans la Grammaire d'ajustement | 147 000 à 830 000 | **~24 000** |
| **ajustement d'un pont** | **5 à 10 min** | **~15 s** (projection) |

**Le traçage n'est pas 20× plus rapide — il est 4× plus rapide**, parce que le
chargement du modèle est un coût fixe qu'aucun corpus ne supprime. C'est
**l'ajustement** qui change d'échelle, et c'est lui qu'on répète.

## 6. Réserves

1. **Une phrase, c'est peu.** L'article 1 porte ~50 jetons ; les mesures de
   contenu par entrée y sont plus bruitées que sur un article entier. C'est le
   prix de la vitesse, et il se paie en répétant — 399 langues au lieu de 10.
2. **Le corpus dense n'est pas identique à l'ancien** (cos 0,9964). Toute
   comparaison entre un chiffre mesuré sur ce corpus et un chiffre mesuré sur les
   anciens doit porter cette réserve.
3. **`--dense` est un chemin différent**, pas seulement plus rapide : le moteur
   documente ailleurs un écart de +0,15 % de perplexité et une corrélation 0,9981
   contre la référence. La calibration ci-dessus le chiffre sur les traces.
4. **Le contexte est de 256 jetons** alors que l'article 2 atteint 1 705
   caractères : les plus longs sont tronqués. Le dire, et le vérifier le jour où
   une langue longue portera une conclusion.

---

## 7. Le premier résultat : la première couche sémantique est dans la bande 10–15

Mesuré sur **183 langues** (pooling moyenne) et **209 langues** (pooling dernière
position), 24 couches, l'article 2 étant encore en cours de traçage. Le corpus
grandit tout seul — le cache s'invalide quand de nouvelles traces arrivent, sinon
il servirait éternellement les langues du premier passage en annonçant le corpus
entier.

### 7.1 Pooling MOYENNE — 183 langues

| couche | même | artic≠ | **SÉPARATION** |
|---:|---:|---:|---:|
| 0 | 0,6410 | 0,6401 | +0,0009 |
| 1 | 0,6296 | 0,6091 | +0,0205 |
| 2–3 | 0,7490 · 0,7887 | 0,7423 · 0,7798 | +0,0067 · +0,0089 |
| **4** | 0,8572 | 0,8424 | **+0,0148** |
| 5–9 | — | — | +0,0112 à +0,0174 |
| 10 | 0,8441 | 0,8221 | +0,0221 |
| 11 | 0,7638 | 0,7383 | +0,0255 |
| 12 | 0,8323 | 0,8025 | +0,0298 |
| **13** | 0,8134 | 0,7812 | **+0,0322** ← pic |
| 14–15 | 0,8076 · 0,8077 | 0,7797 · 0,7805 | +0,0279 · +0,0272 |
| 16–21 | — | — | +0,0165 à +0,0216 |
| 22–23 | 0,6507 · 0,6357 | 0,6267 · 0,6163 | +0,0240 · +0,0194 |

### 7.2 Pooling DERNIÈRE POSITION — 209 langues

Pic à la **couche 10** (+0,0374), plateau de 10 à 15 (+0,0269 à +0,0354),
et un bombement net à la **couche 4** (+0,0295).

### 7.3 Les deux poolings s'accordent, et c'est ce qui compte

| | pic | plateau | bombement précoce |
|---|---|---|---|
| moyenne | **13** | 10–15 | couche 4 |
| dernière position | **10** | 10–15 | couche 4 |

Le §84 avait averti que les deux poolings peuvent raconter des histoires
différentes (1,769 contre 6,275 sur le corpus Wikipedia). **Ici ils racontent la
même** : une bande sémantique entre les couches **10 et 15** sur 24, soit
**42 % à 62 % de la profondeur**, avec un second bombement à la couche 4.

**Et cela corrobore une mesure indépendante.** `rapport-plateau-semantique.md`
situait la convergence inter-langue à **35–42 % de la profondeur** — mesurée sur
**10 langues et 4 écritures**. Ici, **183 à 209 langues** et deux poolings
donnent 42–62 %. Les deux mesures ont été faites avec des méthodes différentes,
sur des corpus différents, et elles se recouvrent.

**Conséquence pour la conception** : la cible d'un pont n'est pas « la couche 8 »
parce qu'on l'a choisie, c'est **la bande 10–15** parce qu'on l'a mesurée — et le
bombement de la couche 4 mérite sa propre mesure, parce qu'il pourrait être une
seconde étape sémantique (ou un artefact de la normalisation).

### 7.4 Réserves, et elles sont réelles

1. **Les effets sont PETITS** : +0,03 de cosinus sur un plancher d'anisotropie de
   0,75 à 0,87. Le signal sémantique est réel mais il est **dix fois plus petit
   que ce que les vecteurs se ressemblent sans rien savoir du sens**. Toute
   conclusion qui oublierait le plancher serait fausse.
2. **Deux articles, pas trente.** 30 articles alignés existent ; deux suffisent à
   établir le contraste, pas à le caractériser finement.
3. **Les longueurs diffèrent** (169 contre 541 caractères de médiane) — la
   symétrisation annule l'effet au premier ordre, elle ne le supprime pas.
4. **Le corpus grandit pendant qu'on le mesure** : 183 et 209 langues ici, 399
   sont attendues. Les chiffres seront repris quand il sera complet.

---

## 8. Le corpus complet : mêmes pics, et c'est une vraie vérification

Le corpus est passé de **183–209 langues** (§7) à **398 langues** — le traçage de
l'article 2 s'est terminé pendant la rédaction. Le §7 annonçait qu'il faudrait
reprendre les chiffres ; les voici, et ils **ne bougent pas**.

| | pic (183–209 langues) | **pic (398 langues)** |
|---|---|---|
| pooling moyenne | couche **13** (+0,0322) | couche **13** (+0,0344) |
| pooling dernière position | couche **10** (+0,0374) | couche **10** (+0,0397) |

**Les deux pics sont identiques, et les amplitudes à 7 % près.** Ce n'est pas une
vérification de complaisance : le corpus a **plus que doublé**, et 190 langues
nouvelles — dont des familles et des écritures entièrement neuves — n'ont pas
déplacé la conclusion d'une seule couche.

### 8.1 Les tableaux complets, 398 langues

**Pooling MOYENNE** — pic couche 13 (+0,0344 = 0,8308 − 0,7964) :

| couche | 0 | 1 | 4 | 8 | 10 | 11 | 12 | **13** | 14 | 15 | 16 | 23 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| séparation | +0,001 | +0,023 | +0,016 | +0,012 | +0,023 | +0,027 | +0,031 | **+0,034** | +0,030 | +0,029 | +0,023 | +0,021 |

**Pooling DERNIÈRE POSITION** — pic couche 10 (+0,0397 = 0,8025 − 0,7628) :

| couche | 0 | 1 | 4 | 8 | 9 | **10** | 11 | 12 | 13 | 14 | 15 | 23 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| séparation | +0,000 | +0,016 | +0,030 | +0,019 | +0,023 | **+0,040** | +0,028 | +0,036 | +0,038 | +0,035 | +0,031 | +0,024 |

### 8.2 Ce que la bande 10–15 dit, et ce qu'elle ne dit pas

**Elle dit** où la représentation cesse d'être une transcription de surface : la
couche 0 a une séparation de **+0,001** (nulle — le même texte dans deux langues
ne se ressemble pas plus que deux textes différents), la couche 13 a **+0,034**.
Et les couches **10 à 15** forment un plateau, pas un pic isolé.

**Elle ne dit pas** que la couche 13 est « la » couche à viser. Trois raisons :

1. **Le plateau est large** (10–15, soit six couches sur 24) : rien ne distingue
   fortement 12, 13 et 14, et le pic se déplace de 10 à 13 selon le pooling.
2. **Le bombement de la couche 4 est inexpliqué.** Il apparaît dans les deux
   poolings, sur les deux tailles de corpus (+0,0156 et +0,0299). Deux
   hypothèses : une première étape sémantique, ou un artefact de normalisation.
   La mesure qui trancherait : refaire le profil sur un modèle dont on sait
   qu'il n'a pas cette structure, ou corréler le bombement avec ce que la couche
   4 fait au même texte dans la MÊME langue.
3. **Le plancher d'anisotropie est haut** : 0,75 à 0,87 selon la couche et le
   pooling. Le signal sémantique fait **+0,03 sur un fond de 0,80** — il est
   réel, il est reproductible, et il est **petit**. C'est la première chose à
   dire de cette mesure.

### 8.3 Ce que le cycle rapide a coûté

| | |
|---|---:|
| traçage article 1 (399 langues × 24 couches) | **26 min** |
| traçage article 2 (399 langues × 24 couches) | **48 min** |
| **la mesure elle-même, cache chaud** | **quelques secondes** |
| taille du cache des vecteurs réduits | quelques Mo |

**Une heure et quart de capture, puis des itérations instantanées.** C'est cela,
le cycle rapide — et il n'a demandé aucun modèle plus petit.
