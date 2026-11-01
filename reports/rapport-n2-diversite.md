# N2.h2 — La diversité française : un modèle de français plutôt qu'un modèle du dépôt

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : entraîné **moitié dépôt,
> moitié littérature**, le même élève passe de **16,70** à **3,85** sur de la littérature
> jamais vue (**÷ 4,33**) et de **57,58** à **25,68** en anglais (**÷ 2,24**),
> pour **+0,17** de PPL en domaine (**3,0904 → 3,2625**).

## La question

Sur le mètre propre, l'élève de N2 vaut **3,0904** en domaine mais **16,70** sur de la
littérature française jamais vue — un **spécialiste du dépôt**. La question : la **diversité
française** répare-t-elle cela, et à quel prix en domaine ? C'est la question que la ligne R
(« le lecteur ») posera de toute façon : un lecteur qui ne sait lire que le dépôt n'est pas un
lecteur.

## Le dispositif

Même recette que [`n2-propre`](rapport-n2-propre.md), même budget (20 000 pas × 16 × 128 = 41 Mo
vus, lr 1e-4 puis 3e-5, trois graines), à un seul changement près : le corpus d'entraînement est
**moitié dépôt, moitié littérature**, entrelacé chunk par chunk (6,14 Mo, 50/50 exact).

- dépôt : `data/corpus_propre/train.txt` (3,24 Mo, dédupliqué, 0 % de fuite) ;
- littérature : `data/corpus_litt_propre/train.txt` — 15,33 Mo de textes du domaine public
  (Verne, Carroll, etc.), dédupliqués eux aussi (0,07 % retiré), avec leur propre split ; on en
  échantillonne un chunk sur cinq pour équilibrer ;
- **professeur et base réentraînés sur le mélange** : sinon le professeur donnerait des cibles de
  littérature qu'il n'a jamais apprises — c'est exactement le confondant nommé de N2.d, où le
  corpus anglais était distillé par un professeur français.

Le test hors domaine est la **validation de la littérature**, tenue à l'écart par le même
découpage : aucune fenêtre n'apparaît dans l'entraînement (0 / 3 000 vérifiées).

## Ce qui est mesuré

| bras | graines | val | test | littérature | anglais | wikitext2 |
|---|---:|---:|---:|---:|---:|---:|
| **A — dépôt seul** | 3 | **3,0904** ±0,0048 | **3,1960** ±0,0100 | **16,7034** ±0,2706 | **57,5773** ±2,2054 | **56,8821** ±2,0231 |
| **D — moitié littérature** | 3 | **3,2625** ±0,0032 | **3,3221** ±0,0032 | **3,8546** ±0,0026 | **25,6755** ±0,4552 | **26,0589** ±0,3353 |

## Lecture

- **Le gain hors domaine est massif** : 16,70 → 3,85 sur de la littérature jamais vue,
  soit **÷ 4,33**. Le corpus était bien le levier, pas le budget.
- **Le coût en domaine est réel mais petit** : 3,0904 → 3,2625 (**+0,17**). Le modèle
  consacre la moitié de ses octets à autre chose, et le dépôt y perd un peu.
- **L'anglais suit** : 57,58 → 25,68 (**÷ 2,24**) alors que le modèle n'a **jamais**
  vu un octet d'anglais. La diversité de registre, dans une langue, transfère au niveau des
  octets.
- **Le test hors domaine est propre** : le gain n'est pas de la mémoire — la validation de
  littérature est tenue à l'écart par construction.

## Ce que ça change

Le modèle de N2 n'est plus évalué sur sa capacité à reproduire le dépôt mais sur sa capacité à
lire du français. Pour la ligne R, qui lira des documents quelconques, c'est la seule mesure qui
compte. Et la porte < 2,5, si elle doit rester la cible, se paie en diversité : à 3,2625 en
domaine, l'élève diversifié en est à 0,76.

## Ce qui pourrait le rendre faux

- **Le test de littérature est du même auteur** que l'entraînement (Verne pour l'essentiel) : le
  gain mesure l'adaptation à un **genre** et à une **langue**, pas à un auteur.
- **Le corpus de littérature est daté** (1900) : le gain en anglais ne dit rien d'un anglais
  moderne.
- **Le professeur mixte** est plus faible en domaine que le professeur dépôt : une partie du coût
  en domaine vient de lui, pas du corpus de l'élève.
- **Trois graines** : l'écart en domaine (+0,17) est petit ; l'intervalle le couvre peut-être.
- **Le ratio 50/50 est un choix** : ni balayé, ni optimisé ; un autre ratio déplacerait le
  compromis.

## Fichiers

- Code : [`tools/distiller_budget.py`](../tools/distiller_budget.py) ·
  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py).
- Corpus : `data/corpus_mixte_propre.txt`, `data/corpus_litt_propre/`, manifeste
  [`corpus-litt-propre.json`](corpus-litt-propre.json).
- Points de contrôle : `work/n2h/D-mixte-g{1,2,3}.pt`, archivés sur deux disques
  (`backups/n2h/2026-11-01/` et `IA/artefacts/n2h/2026-11-01/`).
