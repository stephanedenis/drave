# Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais)

**Date** : 2026-10-19 18:34 UTC  
**Outil** : `tools/aligneur_litteraire.py` (CPU, bibliothèque standard, aucun modèle)  
**Verdict** : **VALIDE** — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).

## 1. La question

La mesure 59 a établi que le banc littéraire était **invalide** : trois découpages successifs (titres, grille proportionnelle, corps) donnaient 84, 60 puis 37 sections françaises contre 37 anglaises, et le chrF restait au niveau du hasard. Le problème n'était pas le modèle mais l'**appariement** : les segments comparés ne disaient pas la même chose. Ce sous-chantier construit donc un alignement **phrase à phrase** et, surtout, le **vérifie** avec des ancres indépendantes — sans quoi un alignement « plausible » ne serait qu'une hypothèse de plus.

## 2. Le dispositif

### 2.1 Les textes

| | français | anglais |
|---|---:|---:|
| fichier | `/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_fr.txt` | `/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_en.txt` |
| source | Project Gutenberg n° 800 (ebooksgratuits) | Project Gutenberg n° 103 (trad. Towle, 1873) |
| caractères des phrases | 408 378 | 357 175 |
| phrases | 4 275 | 3 526 |

Le rapport global de longueur est **0,875 caractère anglais par caractère français** ; c'est ce ratio qui sert de référence à l'appariement, il n'est pas ajusté par chapitre.

### 2.2 Découpage en chapitres — et le piège de la table des matières

Les deux textes ont **37 chapitres numérotés I à XXXVII**, mais les tables des matières utilisent la même forme que les en-têtes (`I TITRE` en français, `CHAPTER I. TITRE` en anglais). Un simple comptage de lignes donne donc **74 candidates par langue**, et c'est exactement l'erreur de la mesure 59 (84 sections françaises). Le filtre est ici **par la longueur** : pour chaque numéro, on garde la candidate dont le bloc suivant est le plus long (un chapitre fait des milliers de caractères, une entrée de table ~100).

| langue | lignes candidates | chapitres retenus | lignes écartées (table des matières) |
|---|---:|---:|---:|
| français | 74 | 37 | 37 |
| anglais | 74 | 37 | 37 |

Contrôle : les numéros retenus sont **contigus 1..37 dans les deux langues** et identiques ; l'appariement ne peut donc se faire qu'entre chapitres de même numéro.

### 2.3 Découpage en phrases

Découpage par règles, sensible aux abréviations (`M.`, `MM.`, `Mr.`, `Mrs.`, `Dr.`, `etc.`), aux initiales, aux guillemets (`« »`, `“ ”`) et aux dialogues français en `--`. On ne coupe pas devant une minuscule, ce qui préserve les incises du type « Quoi ! dit-il ». Les paragraphes sont d'abord déroulés (les textes Gutenberg sont coupés à 70 colonnes).

### 2.4 L'appariement

Programmation dynamique **Gale-Church** chapitre par chapitre, sur la longueur en caractères. Perles autorisées : 1:1, 1:2, 2:1, 1:0, 0:1, 2:2, 1:3, 3:1 ; coût `-2 log p(type) + z²/2`, avec `z = (L_en − ratio·L_fr) / sqrt(L_en + ratio²·L_fr)`. Les frontières de chapitre sont **verrouillées** : chaque chapitre commence et finit sur ses propres phrases. Le dictionnaire d'ancres n'entre **jamais** dans ce calcul.

### 2.5 Les ancres

81 groupes d'ancres (personnages, lieux, navires, institutions), avec leurs formes française et anglaise (`Londres`/`London`, `Inde`/`India`, `Tankadère`/`Tankadere`, `Banque d'Angleterre`/`Bank of England`…). La recherche est insensible à la casse et aux accents, mais **avec frontières de mot** — sans quoi `fixe` compterait pour `Fix`, `comparaison` pour `Paris` et `machine` pour `Chine`. Six ancres ambiguës en anglais (`fix`, `young`, `speedy`, `hitch`, `smith`, `proctor`) exigent une majuscule — et `reform` aussi, pour ne pas confondre le club avec le mot commun. **Alias** : le français dit « Sir Francis Cromarty » là où l'anglais abrège souvent en « Sir Francis » ; les deux formes sont un seul groupe (`cromarty`), sinon on compterait comme des échecs des différences de dénomination, pas d'alignement. Les ancres **distinctives** sont celles qui apparaissent dans au plus 6 chapitres : ce sont elles qui portent le contrôle fort.

## 3. Les chiffres

### 3.1 Structure

| | français | anglais |
|---|---:|---:|
| chapitres retenus | 37 | 37 |
| phrases | 4 275 | 3 526 |
| caractères des phrases | 408 378 | 357 175 |
| rapport global EN/FR | | 0,875 |

### 3.2 Appariement

**3 397 perles appariées** (les deux côtés non vides) sur 3 464 perles ; 2 570 sont des paires 1:1 strictes.

| type de perle | nombre |
|---|---:|
| 1:1 | 2 570 |
| 2:1 | 628 |
| 1:2 | 86 |
| 3:1 | 81 |
| 1:0 | 59 |
| 2:2 | 29 |
| 0:1 | 8 |
| 1:3 | 3 |

| couverture | français | anglais |
|---|---:|---:|
| phrases dans une perle appariée | 4 216 (98,6 %) | 3 518 (99,8 %) |
| phrases non appariées | 59 (1,4 %) | 8 (0,2 %) |

### 3.3 Rappel des ancres

Une **occurrence** est un couple (côté source d'une perle, ancre) — pour une perle 1:1, c'est bien un couple (phrase, ancre). Le rappel à distance *d* est la fraction des occurrences françaises dont l'ancre se retrouve dans la perle anglaise (d = 0) ou dans son voisinage ±*d*. C'est la mesure la plus directe : *si l'alignement est bon, le nom propre doit être là où le français le met*.

| mesure (sens FR → EN) | toutes ancres | ancres distinctives |
|---|---:|---:|
| occurrences | 2 686 | 587 |
| rappel à distance 0 | 81,1 % | 83,6 % |
| rappel ±1 | 90,2 % | 91,3 % |
| rappel ±2 | 92,7 % | 93,2 % |
| rappel ±5 | 95,6 % | 96,1 % |
| perles avec ancre | 1 781 | 500 |
| perles partageant une ancre (distance 0) | 84,7 % | 83,0 % |
| perles partageant une ancre (±2) | 94,8 % | 92,8 % |

Sens inverse (EN → FR), pour vérifier que le résultat ne dépend pas du côté de départ :

| mesure (sens EN → FR) | toutes ancres | ancres distinctives |
|---|---:|---:|
| occurrences | 2 554 | 567 |
| rappel à distance 0 | 85,3 % | 86,6 % |
| rappel ±2 | 94,9 % | 95,8 % |
| perles avec ancre | 1 687 | 475 |

**Où vont les ancres manquées ?** Sur 2 686 occurrences, 81,1 % sont dans la perle, 17,7 % sont **ailleurs dans le même chapitre** (déplacement local, réécriture) et 1,2 % sont **absentes du chapitre** (le traducteur a supprimé ou remplacé le nom). Sur les distinctives : 491/587 dans la perle, 92 ailleurs, 4 absentes. L'essentiel des manques est donc un **déplacement de quelques phrases**, pas une perte de chapitre — c'est ce que rattrape la tolérance ±2. Ce classement est un diagnostic *a posteriori*, pas un critère : le contrôle négatif, lui, ne pardonne rien.

Les huit ancres distinctives les plus fréquentes — le taux global n'est pas porté par une seule :

| ancre | occurrences | rappel 0 | rappel ±2 |
|---|---:|---:|---:|
| `cromarty` | 53 | 81,1 % | 90,6 % |
| `stuart` | 31 | 87,1 % | 90,3 % |
| `rangoon` | 31 | 61,3 % | 80,6 % |
| `carnatic` | 29 | 86,2 % | 96,6 % |
| `proctor` | 24 | 87,5 % | 91,7 % |
| `henrietta` | 24 | 87,5 % | 95,8 % |
| `omaha` | 21 | 95,2 % | 100,0 % |
| `tankadere` | 20 | 85,0 % | 100,0 % |

Le point faible est `rangoon` (61,3 % à distance 0) : le traducteur paraphrase parfois le nom du navire (« the steamer », « the first few days of the voyage ») là où le français l'écrit ; l'ancre manque alors à cet endroit, même si elle reparaît plus loin dans le chapitre. C'est une **limite de la traduction**, pas une preuve de mauvais alignement — et elle est comptée comme un échec, jamais retirée.

**Par chapitre** (≥ 5 occurrences distinctives) : le rappel à distance 0 va de 45,5 % (chapitre 9) à 100,0 % (chapitre 6). Les chapitres sous 70 % sont : 9 (45,5 %), 17 (57,1 %), 15 (65,0 %), 14 (65,5 %). Les effectifs par chapitre sont petits (5 à 53 occurrences) : ces variations sont du bruit d'échantillonnage autant que des différences de traduction.

Les chapitres 9 et 14-17 sont les plus bas pour cette raison : le traducteur y remplace des noms par des périphrases (« la rade d'Aden » → « the roadstead », « les îles Salcette » → « the islands in the bay »), et l'ancre disparaît sans que la phrase ait bougé.

**Phrases sans ancre** : 55,1 % des phrases françaises et 51,4 % des phrases anglaises ne contiennent aucun nom propre du dictionnaire ; 45,1 % des perles n'ont d'ancre ni d'un côté ni de l'autre. C'est la **zone aveugle** du contrôle : ces phrases ne sont validées que par la longueur et la position, pas par une ancre.

### 3.4 Contrôles négatifs

Tous les contrôles utilisent **le même aligneur, le même dictionnaire et la même mesure** ; seule la vérité de l'appariement change. Si les ancres se retrouvent autant dans un appariement faux, le taux réel ne prouve rien.

| contrôle (rappel ±2) | toutes ancres | distinctives | distinctives à distance 0 |
|---|---:|---:|---:|
| **alignement réel** | 92,7 % | 93,2 % | 83,6 % |
| chapitres permutés #1 | 26,3 % | 0,3 % | 0,2 % |
| chapitres permutés #2 | 23,9 % | 0,5 % | 0,3 % |
| chapitres permutés #3 | 25,8 % | 0,2 % | 0,0 % |
| chapitre voisin (i → i+1) | 31,8 % | 9,2 % | 2,4 % |
| phrases mélangées #1 | 43,9 % | 30,2 % | 9,8 % |
| phrases mélangées #2 | 42,8 % | 29,0 % | 7,8 % |
| phrases mélangées #3 | 43,7 % | 31,4 % | 8,6 % |

**Hasard pur, phrase contre phrase dans le même chapitre** : 38 400 tirages, **15,62 %** de rencontres d'ancres. C'est un plancher **phrase contre phrase** — conservateur, parce que les noms propres reviennent beaucoup dans un même chapitre — et non le plancher de la mesure par perle : le contrôle de référence reste la **permutation des chapitres** (0,3 %). L'alignement réel fait **83,65 %** à distance 0 et **93,19 %** à ±2 sur les ancres distinctives, soit **×5,4** et **×6,0** ce plancher.

### 3.5 Matrice chapitres × chapitres (contrôle structurel)

Indépendamment de l'alignement des phrases, on compare l'**ensemble des ancres** de chaque chapitre français à celui de chaque chapitre anglais (Jaccard pondérée par l'IDF). Si les chapitres se correspondent par leur contenu, la diagonale doit dominer.

| mesure | valeur |
|---|---:|
| diagonale classée n° 1 | **37/37** chapitres |
| diagonale dans le top 3 | **37/37** chapitres |
| similarité moyenne sur la diagonale | 0,917 |
| similarité moyenne hors diagonale | 0,107 |
| similarité minimale sur la diagonale | 0,743 |

### 3.6 Distribution des rapports de longueur

| mesure | par caractères | par mots |
|---|---:|---:|
| nombre de perles | 3 397 | 3 397 |
| médiane | 0,904 | 1,000 |
| quartiles Q1 – Q3 | 0,800 – 1,010 | 0,851 – 1,111 |
| 5 % – 95 % | 0,627 – 1,250 | 0,647 – 1,429 |
| minimum – maximum | 0,161 – 4,200 | 0,250 – 7,000 |
| part dans [0,75 ; 1,25] | 78,5 % | 77,5 % |
| part dans [0,80 ; 1,20] | 69,1 % | 68,1 % |
| part hors [0,5 ; 2,0] | 1,4 % | 1,4 % |

La médiane **par caractères** (0,904) est inférieure à 1 parce que l'anglais est plus court que le français ; celle **par mots** (1,000) est au niveau. C'est le **ratio global** qui sert de référence, pas 1. Les queues de distribution sont attendues : une perle 1:1 peut contenir une phrase-source très courte et une phrase-cible longue (ou l'inverse), surtout dans les dialogues.

## 4. Ce qui pourrait rendre le chiffre faux

1. **Les ancres sont des noms propres, et c'est précisément ce qu'un traducteur conserve.** Le taux élevé prouve la correspondance *structurelle* des phrases, pas la fidélité des mots communs. 55,1 % des phrases françaises n'ont aucune ancre : pour elles, seul l'appariement par longueur et position parle.
2. **La tolérance ±2 absorbe les différences de découpage.** Le taux à distance 0 (83,6 % sur les distinctives) est le chiffre honnête ; le ±2 (93,2 %) dit qu'une phrase voisine porte souvent le même nom. Un lecteur qui exige l'alignement exact doit regarder la première colonne.
3. **Le dictionnaire d'ancres est construit à la main, à partir des deux textes.** Il pourrait favoriser les noms à orthographe stable et sous-représenter les lieux que le traducteur a vraiment traduits (`Royaume-Uni` → `United Kingdom`, une seule occurrence anglaise, a été écarté). Il reste indépendant de l'alignement, mais pas indépendant du choix des textes.
4. **Le contrôle négatif « chapitres permutés » n'est pas un hasard parfait** : les chapitres voisins partagent des personnages, et l'anglais d'un chapitre peut contenir les mêmes noms qu'un autre. C'est pourquoi le contrôle **distinctif** (ancres de ≤ 6 chapitres) est mis en avant : il tombe à 0,3 %, contre 93,2 % pour l'alignement réel.
5. **La traduction anglaise (Towle, 1873) condense parfois.** Les perles 2:1 et 3:1 (nombreuses) sont légitimes — le français segmente davantage les dialogues — mais quelques-unes peuvent être des réécritures où le traducteur a fusionné deux phrases. L'alignement les met ensemble ; il ne dit pas laquelle des deux phrases françaises correspond le mieux.
6. **Un seul livre, un seul traducteur.** Le chiffre vaut pour ce couple de textes ; il ne prouve pas que l'outil alignerait *n'importe quel* roman. La méthode (chapitres → Gale-Church → ancres) est générale, mais les 37 chapitres et le dictionnaire sont propres à Verne.
7. **Les textes Gutenberg peuvent contenir des coquilles de transcription.** Une coquille dans un nom propre fait rater une ancre (elle est comptée comme un échec) ; elle ne crée pas de faux positif.
8. **Le contrôle de la matrice est un contrôle de contenu, pas de phrase.** Il établit que le chapitre *i* français et le chapitre *i* anglais parlent du même endroit ; il ne garantit pas que chaque phrase à l'intérieur est à sa place — c'est le rôle du rappel des ancres, avec sa zone aveugle.
9. **Quelques fragments non narratifs** (l'itinéraire chiffré du chapitre 3, les tableaux de distances) sont traités comme des phrases : leurs lignes se ressemblent et peuvent s'apparier entre elles de travers. Ils sont peu nombreux et sans effet sur le taux d'ancres, mais un utilisateur du banc doit les connaître.

## 5. Verdict et usage

**VALIDE** — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).

Critères explicitement vérifiés :

- ✓ **structure 37 / 37** : 37 chapitres FR et 37 EN, numéros identiques
- ✓ **matrice des chapitres (diagonale n° 1)** : 37 / 37 chapitres ont leur homologue en première position
- ✓ **rappel des ancres distinctives** : 93,2 % à ±2 (seuil 80,0 %)
- ✓ **contrôle négatif (chapitres permutés)** : 0,3 % à ±2 (seuil 10,0 %)
- ✓ **facteur au-dessus du hasard** : ×272,5 (seuil ×8)

**Usage.** Le fichier `data/alignement/verne_fr_en.json` contient les paires ; chaque paire porte `chapitre`, `i_fr`, `i_en` (indices 0-based du début de perle), `n_fr`, `n_en` (nombre de phrases de chaque côté) et les textes `fr`/`en` (concaténation de la perle). Les phrases non appariées sont dans `non_appariees`. C'est l'unité à utiliser pour un banc de traduction : comparer le `fr` d'une perle à son `en`, jamais une phrase isolée à une perle entière.

Reproduction :

```bash
CUDA_VISIBLE_DEVICES="" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py
```

*Graine des contrôles : 20260227 ; répétitions : chapitres permutés 3, phrases mélangées 3 ; durée du run : 23,9 s.*

