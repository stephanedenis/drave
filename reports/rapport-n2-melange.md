# N2.ac — Le mélange des deux corpus : la largeur sans perdre le français

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : le modèle entraîné sur le
> **mélange** (186 Mo + 831 Mo = **1,02 Go**, 60 000 pas) vaut **3,4902** sur la validation
> française (fr-60k : 3,4365 ; big-60k : 3,5877), **6,0283** en littérature (**le meilleur**),
> **8,3352** en anglais (≈ big-60k 8,3173, bien mieux que fr-60k 9,5185) et **9,0525** sur
> wikitext2 (**le meilleur**). **La largeur sans perdre le français.**

## Le dispositif

- Corpus : `data/wiki_fr/propre/train.txt` (186 Mo) + `data/wiki_big/propre/train.txt` (831 Mo)
  concaténés = **1,02 Go** ; canal concaténé ; validation = celle de N2.z (la même pour les trois).
- Recette : 34,3 M, **60 000 pas** × 8 × 128, positions [0, 384], canal — identique à fr-60k et
  big-60k.
- Évaluation : val fr, val grand, littérature, anglais, wikitext2 (avec canal).

## Ce qui est mesuré

| modèle | val fr | val grand | littérature | anglais | wikitext2 |
|---|---:|---:|---:|---:|---:|
| **fr-60k** (186 Mo) | **3,4365** | 3,7237 | 6,0011 | 9,5185 | 10,7138 |
| **big-60k** (831 Mo) | 3,5877 | **3,3301** | 6,1381 | **8,3173** | 9,1609 |
| **mix-60k** (1,02 Go) | 3,4902 | 3,3565 | **6,0283** | 8,3352 | **9,0525** |

## Lecture

**Le mélange prend le meilleur des deux, ou presque** : il est **premier** en littérature et sur
wikitext2, **à 0,02** du meilleur en anglais, et **à 0,05** du meilleur en validation française —
là où le big perdait 0,15. Il **domine** le big en français (−0,10 en validation, −0,11 en
littérature) et **domine** le fr en largeur (−1,18 en anglais, −1,66 sur wikitext2).

**La concaténation suffit** : pas de pondération, pas de curriculum — les deux tranches de wiki se
complètent, et le modèle apprend les deux vocabulaires (le français proche et le monde).

**C'est le modèle de production pour R** : français quasi inchangé, largeur du grand corpus.

## Ce que ça change pour N2

- La **recette de production** devient : mélange des deux corpus (1,02 Go), 34,3 M, canal,
  60 000 pas → **3,49 / 6,03 / 8,34 / 9,05**.
- Le levier suivant est le **compute** : 200 000 pas sur le mélange (les 60 k paient déjà +0,1).
- La **fenêtre** (R1) reste la question ouverte ; le mélange ne la change pas (3,52 à 512).

## Ce qui pourrait le rendre faux

- **Une graine** ; l'écart de 0,05 en français est dans le bruit entre graines (±0,01 à ±0,05),
  mais les écarts de largeur (1,2 à 1,7) sont nets.
- **60 000 pas** : aucun des trois n'est convergé.
- **La validation fr favorise le fr** (proximité) ; les OOD favorisent le big — c'est pourquoi les
  trois mesures sont données.
- **La concaténation** met le français en premier (la première moitié du corpus) : un mélange
  entrelacé dirait peut-être autre chose.

## Fichiers

- Modèle : `work/n2w/mix-60k.pt` ; corpus : `data/wiki_mix/propre/` (1,02 Go) ; mesures :
  `work/n2w/eval-mix60-*.json`, `ood-mix60.json`.
