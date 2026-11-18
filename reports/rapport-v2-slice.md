# Le corpus dédupliqué en entraînement : +2,1 % de PPL à pas égal — mais le test est confondu

> **Ligne de roadmap** : N4 / D · **Date** : 2026-11-18 · **Verdict** : ⚠️ **négatif et confondu** — à
> pas égal (10 000 pas depuis r4, mêmes réglages), le **corpus v1** donne PPL **3,0098** et le
> **flux dédupliqué v2** (premier Go) **3,0723** (**+2,1 %**), top-40 0,895 contre 0,888. Mais le
> test ne mesure **pas** la déduplication : v1 n'a que **0,038 %** d'octets dupliqués à retirer, et
> la tranche v2 couvre **plus de source** que v1 (les deux corpus n'ont pas le même contenu).
>
> **Dispositif** : `entrainer_native.py`, init `work/n3/r4.pt`, 10 000 pas, lr 1e-4, AMP, seq 1 024,
> lot 8 · r5a sur `data/wiki_mix/propre/train.txt` (1,017 Go) · r5b sur
> `work/dedup/train-lignes.txt` tronqué au premier Go (1,073 Go) · même validation épinglée
> (`val.txt`) · banc [`checkpoint_bench.sh`](../bench/checkpoint_bench.sh).

## Les chiffres

| run | corpus | octets | PPL val | top-40 | top-20 |
|---|---|---:|---:|---:|---:|
| **r5a** | v1 (`train.txt`) | 1,017 Go | **3,0098** | **0,895** / 2 | **0,932** / 3 |
| **r5b** | v2 (1er Go dédupliqué) | 1,073 Go | 3,0723 | 0,888 / 2 | 0,889 / 2 |
| | | | **+2,1 %** | −0,007 | −0,043 |

## Pourquoi c'est confondu

1. **v1 n'a presque rien à dédupliquer** : `tools/dedup_lignes.py` sur `data/wiki_mix/propre/train.txt`
   retire **0,038 %** des octets (385 658 o) en 8,2 s. Les 8,042 % mesurés sont dans
   `data/corpus_wiki_fr_texte/train.txt` (7,50 Go), pas dans le corpus d'entraînement actuel.
2. **Les deux tranches ne couvrent pas la même source** : 1 Go de v2 = 1 Go du flux dédupliqué,
   donc environ **1,17 Go de source** v1 ; r5a n'a vu que 1,017 Go. Le contenu diffère, pas
   seulement la duplication.
3. **Conséquence** : le −2,1 % se lit « à pas égal, cette tranche-là est un peu moins bonne », pas
   « la déduplication coûte 2 % ». Un test propre demanderait **le même texte source**, dédupliqué
   et brut — impossible sur v1 (0,038 % de duplication), possible sur les 7,50 Go (8,042 %).

## Ce qui reste vrai

- **Le corpus v2 existe** (6,90 Go, `e3112a84…`, dans `work/`), il s'entraîne (r5b a convergé sans
  incident), et il est **8 % plus léger** à contenu source égal.
- **La déduplication n'aide pas le corpus actuel** : v1 est déjà propre ; le gain est pour le
  palier 1 (3-6 Go), où la matière viendra du corpus de 7,50 Go.
- **Le 5e tour de la courbe v1** (r5a, 53 000 pas) : PPL **3,0098** (−36 % depuis l'init), top-20
  **0,932** — le meilleur chiffre du banc, et l'échantillonnage repart après le plateau 33k-43k.

## Ce que ça change

La prochaine étape du palier 1 n'est pas « dédupliquer v1 » (il est propre) mais **construire le
corpus de 3-6 Go** à partir des 7,50 Go (dédupliqués à 8,042 %, épinglés) **et y ajouter de la
diversité** (livres FR du domaine public — l'écart de diversité, pas de volume). Le test
dédoublonnage-vrai se fera là, à contenu source égal.

## Voir aussi

- [la courbe](rapport-courbe-r1-r3.md) · [le dédup par ligne](rapport-dedup-lignes.md) ·
  [les données](rapport-donnees-inventaire.md) · [le plan natif](../docs/pilotage/natif-plan.md)
