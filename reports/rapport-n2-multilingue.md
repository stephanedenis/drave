# N2.k — Dix langues : la base multilingue paie **0,60 bit/octet** en français et en gagne **0,8 à 3,2** ailleurs

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : une seule base de 11,47 M
> entraînée sur **10 langues** (237 Mo) passe le français de **3,7633** à **5,6842** (+51 %,
> **+0,60 bit/octet**) et fait tomber l'anglais de 11,04 à **6,30**, l'allemand de 16,30 à
> **6,50**, le japonais de 53,84 à **5,74**, le chinois de 85,03 à **9,65**. À capacité constante,
> la diversité linguistique se paie en précision sur la langue la plus entraînée.

## La question

Le modèle est en **octets** : il n'a pas de vocabulaire par langue, donc le multilingue ne lui
coûte rien *a priori* en couverture. Mais à 11,47 M de paramètres, chaque langue prise en charge
se paie en capacité. La question : **que coûte la diversité au français, et que rapporte-t-elle
aux autres langues ?** Et ce coût est-il de la **dilution** ou simplement du **données** (le
corpus multilingue ne contient que 21 Mo de français, contre 186 Mo pour la base française) ?

## Le dispositif

- **10 langues** : fr, en, de, es, it, pt, ru, ar, ja, zh ; **11 000 articles par langue** extraits
  des bases sqlite (page_ids 200 000+ pour éviter tout recouvrement avec N2.j), **1 000 en
  validation** par langue.
- **Corpus** : 275,5 Mo bruts, entrelacés par chunks de 8 Ko pour que chaque langue soit partout ;
  déduplication (−4,4 %) → **237,0 Mo** d'entraînement ; **0 / 60** fenêtres de validation dans
  l'entraînement **par langue** (10 contrôles).
- **Base** : 11,47 M, 20 000 pas × 8 × 128 (20,5 Mo vus), lr 3e-4, graine 1 — recette N2.h.
- **Contrôles** : la base **française seule** (186 Mo, N2.j) et la base **française à données
  égales** (les 21 Mo de français du corpus multilingue, sans les autres langues) — c'est ce
  dernier qui sépare la dilution de l'effet de données.

## Ce qui est mesuré

| langue | FR seul (186 Mo) | FR seul (21 Mo) | 10 langues (237 Mo) | écart multi / FR 21 Mo |
|---|---:|---:|---:|---:|
| **fr** | 3,7633 | 3,6230 | 5,6842 | +57 % |
| **en** | 11,0366 | 10,9509 | 6,3024 | −42 % |
| **de** | 16,3009 | 17,5431 | 6,5047 | −63 % |
| **es** | 13,0054 | 13,3105 | 6,0866 | −54 % |
| **it** | 13,6259 | 13,8877 | 6,0605 | −56 % |
| **pt** | 15,2688 | 15,9746 | 6,8002 | −57 % |
| **ru** | 10,7419 | 8,3772 | 3,6809 | −56 % |
| **ar** | 13,0103 | 16,5414 | 3,6064 | −78 % |
| **ja** | 53,8382 | 43,5327 | 5,7423 | −87 % |
| **zh** | 85,0273 | 107,8443 | 9,6509 | −91 % |

## Lecture

En français, la base multilingue vaut **5,6842** contre **3,7633** pour la base 186 Mo et **3,6230** pour la base française **à données égales** (21 Mo) : **+57 %** par rapport à cette dernière, soit **+0.65 bit/octet**. La dilution est donc **réelle et forte**, et le volume de français n'y change rien — 21 Mo suffisent déjà à 3,62. Sur les neuf autres langues, la base multilingue divise la PPL par **1.8** en anglais, **2.5** en allemand, **9.4** en japonais et **8.8** en chinois. En bits par octet, le français paie **+0.65** quand l'anglais gagne **+0.81** et le chinois **+3.14**.

## Ce que ça change pour N2

Le multilingue coûte **0,65 bit/octet** en français et en rapporte **0,8 à 3,4** dans les neuf autres langues. À 11,47 M, dix langues est un partage serré : pour la porte N2, la base française seule reste la référence ; pour la ligne R (lire des documents dans dix langues), c'est un levier direct. La question ouverte est une **loi d'échelle** : à quel nombre de paramètres la dilution disparaît-elle ? Elle se mesure en refaisant tourner les trois bases à 21,65 M (N2.h5) — la capacité double, la question devient « combien de langues par million de paramètres ».

## Ce qui pourrait le rendre faux

- **20 000 pas = 20,5 Mo vus**, soit 7,5 % du corpus : aucune des deux bases n'est convergée ; les
  écarts disent la *vitesse d'apprentissage*, pas la limite asymptotique.
- **Une seule graine** ; les écarts sont grands, l'intervalle n'est pas mesuré.
- **La PPL par octet dépend de l'écriture** : le cyrillique et l'arabe prennent 2 octets par
  caractère, le CJK 3 ; les PPL ne sont pas comparables **entre** langues, seulement **entre
  modèles** pour une même langue.
- **Les validations diffèrent en difficulté** (articles courts, 1 000 par langue) : le français à
  3,76 et le russe à 3,68 ne disent pas que le russe est « mieux appris ».
- **Le texte est du wikitexte nettoyé** : titres de section collés, listes, formules — même
  remarque que N2.j.

## Fichiers

- Extraction : `work/n2k/extrait.py` ; corpus : `data/wiki_multi/`, manifeste
  [`corpus-multi-propre.json`](corpus-multi-propre.json).
- Évaluation : `work/n2k/evalue.py` ; JSON : `work/n2k/eval-wiki.json`, `eval-multi.json`.
- Points de contrôle : `work/n2k/base-multi.pt`, `base-fr21.pt` ; référence `work/n2j/base-wiki.pt`.
