# Rapport — l'attention creuse perd-elle l'information ? (aiguille × `--attn-topk`)

**En une ligne** : à 4 096 clés, l'attention à **256 clés (6,25 %)** des 24 jetons
de DÉCODAGE retrouve l'information placée **au début** (profondeur 0,1) et **à la
fin** (0,9), mais **pas au milieu** (0,5) — là où l'attention complète la retrouve.
CPU et GPU se comportent pareil, ce qui est aussi un contrôle croisé des deux
implémentations.

⚠️ **Portée exacte de la mesure** : avec `--lot 256` (le réglage de cette grille),
le moteur **ignore `--attn-topk` au préremplissage** — il l'imprime lui-même
(« l'attention par lots est DENSE »). Le k = 256 ne s'applique donc qu'aux 24 jetons
générés (0,58 % des passes), ce qui est bien le moment où le modèle doit regarder
en arrière — mais la phrase « une attention qui ne garde que 256 clés » décrit le
DÉCODAGE, pas le passage entier. Une grille en `--lot 1` lèverait l'ambiguïté ; elle
est au planning (le message d'avertissement du moteur n'est pas lu par
`aiguille.py`, qui ne lit la sortie que si le moteur est muet : c'est un défaut de
l'outil, corrigé depuis).

Outil : `tools/aiguille.py` (v2), auquel ce sprint a ajouté `--attn-topk` et
`--gpu-topk`. Modèle : Qwen2.5-0.5B-Instruct Q8_0, 24 jetons de réponse,
`--lot 256`, remplissage Wikitext-2 (fenêtres décalées), code planté
`AZUR-7391`.

## Le coût d'une sonde, d'abord

| modèle | contexte | secondes par sonde |
|---|---|---|
| Qwen2.5-0.5B | 4 096 | ~250 |
| Qwen2.5-1.5B | 4 096 | ~725 |
| Qwen3-30B-A3B | 2 048 | ~670 |

⚠️ **Correction d'une affirmation fausse de la première version de ce rapport** :
j'y avais écrit que « `--infer` ignore `--lot` », en me fondant sur un `grep` limité
au corps de `run_infer` (qui ne contient qu'un `mdl.generate(...)`). Or
`Model::generate` (`model.rs:3911`) **utilise bien `forward_lot`** sur des tranches
de `self.lot` — le commentaire du code le dit mot pour mot. Le préremplissage par
lots est donc actif en inférence, et le chiffre « ~175 ms par jeton de prompt »
était faux lui aussi (4114 jetons à 175 ms feraient 720 s, alors que la sonde
entière, génération comprise, en prend 250).

**Leçon** : un `grep` qui s'arrête à la fonction qu'on regarde ne suit pas la
chaîne d'appels. La vérification se fait dans le code appelé, pas dans l'appelant.

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

* 8 192 et 16 384 : non mesurés dans ce box. Le taux mesuré du 0.5B est de 58 à
  62 ms par jeton de prompt (238,5 à 256,5 s pour 4 114 jetons), donc ≈9 min par
  sonde à 8 192 — et **seule** la sonde « 8 192 / 0,5 / complète » a été lancée,
  puis arrêtée 8 s plus tard (22:55:13) pour laisser la place à la cérémonie. Le
  sprint 4 reprend la grille là où elle s'arrête.
* plusieurs codes par sonde, plusieurs fenêtres de corpus : la mesure est
  binaire (trouvé / non trouvé), avec un seul code et une seule fenêtre par
  (contexte, profondeur). Un « NON » peut être un échec de génération ; le détail
  (« oui » dense au même endroit) protège de cette lecture, mais une répétition
  serait plus solide.
* l'effet d'un k plus grand (512, 1 024) : non mesuré. C'est la première
  expérience à faire ensuite — si k = 1 024 (25 % du contexte) retrouve le milieu,
  le problème est un réglage ; sinon c'est un mécanisme manquant.
* le préremplissage reste DENSE avec `--lot > 1` : la mesure porte sur le décodage.
  Une grille en `--lot 1` (où tout le passage est creux) est la vérification qui
  manque, et elle serait d'autant plus abordable que le préremplissage par lots est
  déjà branché.

## Reproduire

```bash
python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256
python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256 --attn-topk 256
python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256 --attn-topk 256 --gpu-topk
```
