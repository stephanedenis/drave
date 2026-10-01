# Rapport — l'attention creuse perd-elle l'information ? (aiguille × `--attn-topk`)

**En une ligne** : à 4 096 clés, une attention qui ne garde que **256 clés (6 %)** 
retrouve l'information placée **au début** (profondeur 0,1) et **à la fin**
(0,9, mesuré ci-dessous), mais **pas au milieu** (0,5) — là où l'attention
complète la retrouve. CPU et GPU se comportent pareil, ce qui est aussi un contrôle
croisé des deux implémentations.

Outil : `tools/aiguille.py` (v2), auquel ce sprint a ajouté `--attn-topk` et
`--gpu-topk`. Modèle : Qwen2.5-0.5B-Instruct Q8_0, 24 jetons de réponse,
`--lot 256`, remplissage Wikitext-2 (fenêtres décalées), code planté
`AZUR-7391`.

## Le coût d'une sonde, d'abord

| modèle | contexte | secondes par sonde | cause |
|---|---|---|---|
| Qwen2.5-0.5B | 4 096 | ~250 | ~175 ms par jeton de prompt |
| Qwen2.5-1.5B | 4 096 | ~725 | idem |
| Qwen3-30B-A3B | 2 048 | ~670 | idem |

Ce coût n'est pas le modèle : `run_infer` traite le prompt **jeton par jeton**
(`for (pos, &t) in ids.iter()…`), alors que `forward_lot` existe et n'est appelé
que par la perplexité et le mode réparti. **`--infer` ignore `--lot`** — trouvé en
préparant cette grille, et mis au planning (c'est le levier qui rendra les grilles
longues abordables).

## La grille

| contexte | profondeur | attention complète | top-k 256 CPU | top-k 256 GPU |
|---|---|---|---|---|
| 4 096 | 0,1 | **oui** (256,5 s) | **oui** (238,5 s) | **oui** (243,1 s) |
| 4 096 | **0,5** | **oui** (246,5 s) | **NON** (242,0 s) | **NON** (267,6 s) |
| 4 096 | 0,9 | **oui** (249,9 s) | **oui** (236,4 s) | **oui** (248,3 s) |

Neuf sondes, même modèle, mêmes fenêtres de corpus : le seul point qui échoue est
le MILIEU, et il échoue des deux côtés (CPU et GPU).

## Ce que ça veut dire

1. **La profondeur médiane est le point dur**, et c'est exactement le phénomène
   « perdu au milieu » : la sélection top-k d'une requête, à 4 096 clés, retient
   les jetons récents (et les puits d'attention du début) ; une phrase plantée au
   milieu n'entre pas dans les 256 premières. L'attention complète, elle, la
   retrouve.
2. **Les deux implémentations se comportent pareil** (NON aux deux au milieu,
   oui aux deux au début) : le noyau fusionné et le chemin CPU ne divergent pas
   sur un comportement de qualité, pas seulement sur des chiffres.
3. **Le coût du pruning n'est donc pas uniforme** : il est nul là où l'information
   est au bord du contexte, et total au milieu. C'est une raison de plus pour
   l'**index** que le plan de la phase 1.1 rangeait « hors périmètre » : noter
   toutes les clés puis garder les k meilleures ne peut pas retrouver une
   information dont le score est moyen — il faut un mécanisme qui la *cherche*.

## Ce que ce rapport ne dit pas

* 8 192 et 16 384 : la grille n'a pas été mesurée dans ce box (≈25 min par sonde à
  8 192 avec le préremplissage jeton par jeton — les trois sondes de 8 192 ont été
  LANCÉES puis arrêtées pour laisser la place à la cérémonie de fin de box, elles
  sont reportées). Le sprint 4 branche le préremplissage par lots et reprend la
  grille là où elle s'arrête.
* plusieurs codes par sonde, plusieurs fenêtres de corpus : la mesure est
  binaire (trouvé / non trouvé), avec un seul code et une seule fenêtre par
  (contexte, profondeur). Un « NON » peut être un échec de génération ; le détail
  (« oui » dense au même endroit) protège de cette lecture, mais une répétition
  serait plus solide.
* l'effet d'un k plus grand (512, 1 024) : non mesuré. C'est la première
  expérience à faire ensuite — si k = 1 024 (25 % du contexte) retrouve le milieu,
  le problème est un réglage ; sinon c'est un mécanisme manquant.

## Reproduire

```bash
python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256
python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256 --attn-topk 256
python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256 --attn-topk 256 --gpu-topk
```
