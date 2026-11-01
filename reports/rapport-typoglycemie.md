# La typoglycémie du modèle : il lit les lettres, pas les formes

> **Ligne de roadmap** : R (la lecture de surface) · **Date** : 2026-11-01 · **Verdict** : sur le
> texte de validation, le mélange de **l'intérieur des mots** multiplie la perplexité par **17,8**
> (3,0555 → 54,2655) et le mélange de **toutes les lettres** par **62,7** (191,4059). Le modèle
> actuel est un lecteur **de lettres**, pas un lecteur **de formes** — l'effet humain
> (« l'ordre des lettres du milieu ne compte pas ») n'est pas reproduit, et c'est une **mesure**,
> pas une intuition.

## Le dispositif

Trois variantes du **même** texte de validation (`data/corpus_propre/val.txt`, 180 223 octets),
mêmes octets, même longueur, même protocole (8 lots × 16 fenêtres × 128 octets, chunk-aware) :

| variante | ce qui change | PPL | ×propre |
|---|---|---:|---:|
| **propre** | rien | **3,0555** | 1,0 |
| **milieu** | l'intérieur de chaque mot (≥ 4 lettres) est mélangé, première et dernière gardées | **54,2655** | **17,8** |
| **tout** | toutes les lettres de chaque mot sont mélangées | **191,4059** | **62,7** |

Modèle : `A-propre-g1` (11,47 M, distillation sur le corpus propre), mélange déterministe
(`random.Random(0)`), script `work/n2i/typoglycemie.py`.

## Ce que ça dit

Le modèle humain de la typoglycémie repose sur **trois** choses que ce modèle n'a pas : un
**lexique** de dizaines de milliers de mots, une **prédiction top-down** forte (le contexte choisit
le mot), et une **reconnaissance de forme globale** (les lettres extérieures et la longueur
suffisent). Le modèle, lui, prédit l'octet suivant à partir de l'octet précédent : mélanger
l'intérieur d'un mot détruit exactement ce qu'il lit.

La différence **milieu / tout** (17,8 contre 62,7) montre que la première et la dernière lettre
portent encore un peu de signal (un facteur 3,5), mais rien qui ressemble à une lecture de mots.

## Ce que le test ne dit pas

- Il ne dit **pas** qu'un modèle de formes serait meilleur : il dit que **celui-ci** lit des
  lettres. Un encodeur de formes devrait être jugé sur **son** test de mélange, pas sur celui-ci.
- Le mélange détruit les n-grammes de lettres, qui sont **toute** l'entrée du modèle : le test
  mesure sa **dépendance**, pas une faiblesse « réparable » à architecture constante.
- Il ne dit rien de la **structure de page** (colonnes, tableaux) — c'est R4.4, et elle est
  mesurée séparément.

## Ce qui pourrait le rendre faux

- **Un seul modèle, une seule graine** : la PPL propre de cette graine (3,0555) diffère de la
  moyenne publiée (3,0904) ; l'ordre de grandeur (×17,8) est robuste, le chiffre exact ne l'est pas.
- **Le mélange est uniforme** : un mélange qui préserve les digrammes fréquents (« tion », « ent »)
  dirait autre chose — c'est le test suivant.
- **La tokenisation** : le modèle est en octets ; un modèle BPE aurait une autre sensibilité au
  mélange (les tokens changent), donc le chiffre n'est pas transposable.

## Le programme que ce test ouvre

1. **E2 — un encodeur de formes** : mots représentés par un pooling de n-grammes de caractères
   (forme globale, ordre interne libre), positions relatives, même budget de paramètres ; jugé sur
   la PPL **et** sur le mélange.
2. **E3 — la saccade** : une politique qui échantillonne des fenêtres de mots (perception active)
   au lieu de tout lire ; le moteur de pensée v0 (B13) est l'hôte naturel de cette politique —
   recherche tracée, budget, rejeu.
3. **Le test de mélange comme banc** : la typoglycémie devient une **métrique de robustesse** du
   projet, à côté de la PPL et de la longueur.

## Fichiers

- Script : `work/n2i/typoglycemie.py` (diagnostic, non committé dans `tools/`).
- Modèle : `work/n2h/A-propre-g1.pt` (11,47 M).
- Corpus : `data/corpus_propre/val.txt`.
