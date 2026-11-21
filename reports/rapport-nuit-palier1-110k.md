# La nuit du 20-21/11 : le palier 1 à 110 000 pas, et ce que les vals disent vraiment

> **Ligne de roadmap** : N · **Date** : 2026-11-20 → 21 · **Verdict** : *(en cours — les tranches
> 5 à 11 tournent ; le point de 110 000 pas tombe vers 8 h 50)*. Deux graines du corpus du palier 1
> (les résumés `frwiki_v14`, 3,69 Go, épinglé `469a6d78…`) reprises de 30 000 à 110 000 pas,
> jugées à chaque tranche sur wikitext2 et, au bout, sur trois autres vals.

## Les courbes (wikitext2)

| pas | palier 1, g1 (p1) | palier 1, g2 (p2) |
|---:|---|---|
| 30 000 | 7,7044 | 7,2790 |
| 40 000 | *(à remplir)* | 7,1548 |
| 50 000 | *(à remplir)* | *(à remplir)* |
| 60 000 | *(à remplir)* | *(à remplir)* |
| 70 000 | *(à remplir)* | *(à remplir)* |
| 80 000 | *(à remplir)* | *(à remplir)* |
| 90 000 | *(à remplir)* | *(à remplir)* |
| 100 000 | *(à remplir)* | *(à remplir)* |
| 110 000 | *(à remplir)* | *(à remplir)* |

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

## La matrice du matin

| modèle | entraîné sur | wikitext2 (anglais) | littérature (fr, autre) | val du registre |
|---|---|---:|---:|---:|
| nb11 | `wiki_big` 110k | 6,8349 | *(à remplir)* | 2,71 |
| v111 | mélange v1 110k | 6,8674 | *(à remplir)* | *(à remplir)* |
| v211 | plein texte v2 110k | 7,0930 | *(à remplir)* | *(à remplir)* |
| p111 | palier 1 110k, g1 | *(à remplir)* | *(à remplir)* | *(à remplir)* |
| p211 | palier 1 110k, g2 | *(à remplir)* | *(à remplir)* | *(à remplir)* |

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
