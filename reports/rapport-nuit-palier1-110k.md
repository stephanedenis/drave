# La nuit du 20-21/11 : le palier 1 à 110 000 pas, et ce que les vals disent vraiment

> **Ligne de roadmap** : N · **Date** : 2026-11-20 → 21 · **Verdict** : *(en cours — les tranches
> 5 à 11 tournent ; le point de 110 000 pas tombe vers 8 h 50)*. Deux graines du corpus du palier 1
> (les résumés `frwiki_v14`, 3,69 Go, épinglé `469a6d78…`) reprises de 30 000 à 110 000 pas,
> jugées à chaque tranche sur wikitext2 et, au bout, sur trois autres vals.

## Les courbes (wikitext2 / PPL du val de v1)

| pas | p1 (graine 1) | p2 (graine 2) |
|---:|---|---|
| 30 000 | 7,7044 / 3,1486 | 7,2790 / 3,0874 |
| 40 000 | 7,3733 / 3,0761 | 7,1548 / 3,0232 |
| 50 000 | 7,1953 / 3,0229 | 7,0021 / 2,9860 |
| 60 000 | 7,1253 / 2,9924 | 7,0252 / 2,9611 |
| 70 000 | 7,1114 / 2,9664 | 6,9098 / 2,9322 |
| 80 000 | 7,0881 / 2,9550 | **6,8757** / 2,9245 |
| 90 000 | 6,9957 / 2,9479 | 6,9398 / 2,9272 |
| 100 000 | 7,0367 / 2,9409 | 7,0523 / 2,9282 |
| 110 000 | **7,0342** / 2,9360 | 7,0477 / 2,9289 |

**Les deux graines plafonnent vers 7,0** : p2 passe par un minimum à **80 000 pas (6,8757)** puis
remonte (7,05 à 110 000) ; p1 descend jusqu'à 6,9957 (90 000) et stagne (7,03). Sur le val de v1,
les PPL continuent de baisser (2,93-2,94) alors que wikitext2 ne baisse plus — le modèle se
spécialise, il ne généralise plus. C'est exactement le signe attendu du **rejeu des fenêtres**
(plus d'optimisation sur le même échantillon).

Comparaison au même pas : `wiki_big` à 110 000 pas = **6,8349**, et son minimum de parcours ~6,807
(90 000). Le palier 1 reste **derrière de ~2-3 %** — dans la bande de variance (4,7 %), mais sans
jamais passer devant.

## Les fenêtres, pas les époques — et le défaut trouvé cette nuit

Un pas = 8 192 octets (lot 8 × seq 1024), et **chaque tranche repartait le compteur de fenêtres à
zéro** : les onze tranches rejouent le **même échantillon de 80 000 fenêtres** (~82 Mo), pas 900 Mo
de données fraîches. Voir [`rapport-rejeu-des-fenetres.md`](rapport-rejeu-des-fenetres.md) — le
correctif `--compteur-suite` est écrit et validé, mais **pas** utilisé par les runs de la nuit (pour
rester comparable à `wiki_big`, qui a le même schéma).

Conséquence : les deux corpus voient **autant de fenêtres distinctes** (80 000), et la taille du
corpus ne change que leur **diversité**, pas la quantité consommée. Les « époques » ne se calculent
pas comme sur un parcours séquentiel.

## Ce que les vals mesurent (et ne mesurent pas)

1. **wikitext2 est anglais** : 5 lignes tirées au hasard ne se retrouvent **dans aucun** des deux
   corpus français (0/5 et 0/5). Les PPL de 6,8-9,5 mesurent donc du **transfert inter-langue**.
2. **Le val du registre propre est quatre fois plus bas** : `wiki_big` à 110 000 pas donne **2,71**
   sur son propre val tenu à l'écart, contre 6,83 sur wikitext2. Les deux chiffres ne disent pas la
   même chose — et c'est le second (anglais) qui a servi à classer les corpus toute la semaine.
3. **Les vals des corpus se contaminent** : 5 lignes du val de `wiki_big` → **1 sur 5** dans le
   train du palier 1 (~20 %) : les deux corpus viennent de la même base, avec des découpages
   différents. Un val « du registre » n'est propre que pour les modèles de son corpus.
4. **Le val littérature** (11 livres Wikisource, 8,76 Mo, `work/vals/litterature_val_1m.txt`) donne
   le val **français d'un autre registre** qui manquait.

## La matrice du matin — et le classement qui s'inverse selon le val

| modèle | entraîné sur | pas | wikitext2 (EN) | littérature (FR, autre) | val de son registre |
|---|---|---:|---:|---:|---:|
| nb11 | `wiki_big` (831 Mo) | 110k | **6,8349** | 4,0443 | **2,7227** (`wiki_big`) |
| v111 | mélange v1 (1 Go) | 110k | 6,8674 | 3,9872 | 2,7367 (`wiki_big`) |
| v211 | plein texte v2 (6,9 Go) | 110k | 7,0930 | **3,5752** | 3,2288 (`wiki_big`) |
| p111 | palier 1 (3,69 Go), g1 | 110k | 7,0342 | 4,1036 | **2,6929** (palier 1) |
| p211 | palier 1, g2 | 110k | 7,0477 | 4,1306 | **2,6796** (palier 1) |

**Trois lectures, et elles ne vont pas dans le même sens :**

1. **Dans son registre**, tout se vaut : les modèles de résumés rendent 2,68-2,74 sur un val de
   résumés tenu à l'écart — `wiki_big` (831 Mo) comme le palier 1 (3,69 Go). **4,4 fois plus de
   résumés n'achète rien** — cohérent avec le rejeu des fenêtres (mêmes 80 000 fenêtres) et avec la
   saturation d'un registre.
2. **Hors registre** (littérature française, jamais vue), le classement **s'inverse** : le **plein
   texte** gagne (**3,58**), le mélange suit (3,99), les résumés perdent (4,04-4,12). Entraîner sur
   des résumés apprend le registre encyclopédique ; entraîner sur le plein texte apprend une prose
   plus large — et c'est ce qui transfère à la littérature.
3. **En anglais** (wikitext2, transfert inter-langue), `wiki_big` et le mélange mènent (6,83-6,87) ;
   le palier 1 suit (7,04-7,05) ; le plein texte ferme (7,09).

**Nuance de contamination** : le val `wiki_big` est contaminé pour v211 (le plein texte couvre les
mêmes articles) et pour p1/p2 ; le val palier 1 est contaminé pour nb11/v111/v211. Le val
**littérature est propre pour tous** — c'est le seul classement hors registre sans réserve.

## Ce qui pourrait le rendre faux

- **Une graine par bras** (sauf le palier 1, deux graines) ; la variance mesurée est de 1,8 %
  d'écart-type et 4,7 % d'étendue à 30 000 pas — aucun écart inférieur n'est significatif.
- **Les vals changent de langue et de registre** : un classement sur l'anglais n'est pas un
  classement sur le français.
- **Le val littérature n'est pas tenu à l'écart** d'un entraînement (aucun modèle n'a vu
  Wikisource — vérifié par construction, mais à confirmer par une recherche d'empreintes).
- La contamination des vals de registre (~20 %) gonfle les chiffres des modèles de l'autre corpus.

## Voir aussi

- [le corpus du palier 1](rapport-corpus-palier1.md) · [la variance](rapport-variance-graines.md) ·
  [la sélection](rapport-selection-contenu.md) · [la nuit `wiki_big`](rapport-nuit-wikibig.md) ·
  [la diversité Wikisource](rapport-diversite-wikisource.md)
