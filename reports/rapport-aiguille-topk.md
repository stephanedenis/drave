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

## Suite (sprint 4) : le k est un RÉGLAGE, pas une fatalité

⚠️ **Ce que cette grille est, et ce qu'elle n'est pas** — corrigé après la revue
adverse du sprint 4 (et re-corrigé au sprint 5, qui a refait la grille sur trois
textes) : les trois colonnes sont trois **répétitions de la MÊME invite**, pas trois
fenêtres de corpus. Le garde-fou d'`aiguille.py` comparait
l'offset à `len(corpus) - 400_000` alors que le corpus en fait **353 778** : la
remise à zéro se déclenchait donc toujours, et les trois sondes d'une série
utilisaient l'offset 0. Or le moteur est déterministe : **trois répétitions d'une
même invite ne mesurent rien de plus qu'une seule**. Ce qui reste établi, c'est la
CONVERGENCE entre le premier balayage (une sonde) et cette série ; la généralité
inter-fenêtres, elle, n'est pas mesurée. L'outil est corrigé (marge calculée sur la
taille réelle du corpus) et la grille est à refaire.

La grille, à 4 096 clés et profondeur 0,5 (le milieu), `--lot 256` :

| configuration | répétition 1 | répétition 2 | répétition 3 | verdict |
|---|---|---|---|---|
| attention complète | oui (383,6 s) | oui (326,5 s) | oui (251,5 s) | **3/3** |
| **k = 256** (6,25 %) | NON (244,7 s) | NON (237,8 s) | NON (237,0 s) | **0/3** |
| **k = 1 024** (25 %) | oui (239,6 s) | oui (253,2 s) | oui (244,1 s) | **3/3** |
| **k = 512** (12,5 %) | NON (240,5 s) | NON (238,1 s) | NON (237,8 s) | **0/3** |

(Les durées de la rangée « complète » ont été mesurées pendant qu'un autre balayage
tournait : elles ne sont pas comparables à celles des autres rangées. Les verdicts,
eux, ne dépendent pas de la charge.)

**Conclusion corrigée, avec sa portée exacte** : à 4 096 clés, en `--lot 256` (où
`--attn-topk` ne s'applique qu'aux **24 jetons du décodage**, le préremplissage
restant dense — le moteur l'imprime), l'échec au milieu n'est PAS une impossibilité
structurelle du top-k : **0 à k = 256 (6,25 %), 0 à k = 512 (12,5 %), 3/3 à
k = 1 024 (25 %)**, référence complète à 3/3. Ce n'est pas « reproductible » au sens
de trois fenêtres — c'est **convergent** : le premier balayage (une sonde) donnait
déjà non à 512 et oui à 1 024. Le seuil est donc **entre 512 et 1 024 clés** (12,5 % et
25 % du contexte), et l'affirmation du sprint 3 (« sans index, l'attention creuse ne
peut pas remplacer l'attention complète à long contexte ») était **trop forte** :
elle vaut pour un k nettement inférieur au seuil.

La question qui compte pour la feuille de route n'est donc pas « index ou pas
index », mais **comment le k nécessaire évolue avec le contexte** : si le rapport
k/contexte reste de l'ordre du quart, l'élagage ne rapporte rien à 32 k ; s'il
décroît (l'information utile est de plus en plus concentrée), il devient payant.
C'est la mesure à faire ensuite, et le préremplissage déporté (§ ci-dessus) la rend
abordable.

Et un contrôle (UNE sonde) qui invalide une comparaison tentante : **en `--lot 1`,
l'attention COMPLÈTE échoue aussi au milieu** (251,0 s, « NON ») alors qu'elle
réussit en `--lot 256`. Le chemin par lots change le résultat lui-même (la revue
adverse du sprint 3 avait mesuré que `--lot 1` et `--lot 256` génèrent des
identifiants différents) : la comparaison « tout le passage creux » en `--lot 1`
n'est pas propre, et la seule comparaison valable est **à lot fixé**, entre
attention complète et attention creuse.

### Pourquoi `--lot 1` ≠ `--lot 256` : mesuré (et c'est minuscule)

Les deux chemins ne donnent pas la même continuation à température 0 — c'est ce qui
rendait le contrôle « tout le passage creux » ininterprétable. Les logits, eux,
disent l'écart réel (Qwen2.5-0.5B Q8_0, ctx 2 048, 511 jetons, mêmes identifiants) :

| | perplexité | écart moyen \|ΔNLL\| | accord top-1 |
|---|---|---|---|
| `--lot 1` | 13,1368 (moteur) / 13,1367 (comparateur) | — | — |
| `--lot 256` | 13,1359 | **0,0007** (médiane 0,0003, p90 0,0017, max 0,0068) | **511/511** |

Le désaccord entre les deux chemins est donc de **7e-4 nat par position en moyenne**
(max 6,8e-3, p90 1,7e-3), et le jeton choisi est le même PARTOUT : ce n'est pas un chemin faux, c'est une
amplification chaotique — un écart de 1e-3 sur un logit suffit à changer un jeton
greedy après quelques dizaines de pas, et une réponse qui doit contenir un code de
8 caractères ne pardonne pas un jeton.

Conséquence pour la méthode : **toute comparaison de qualité doit se faire à lot
fixé**, et les verdicts binaires (trouvé / non trouvé) doivent être lus comme des
révélateurs d'un écart minuscule, pas comme une propriété stable du modèle.

### La grille refaite sur TROIS TEXTES (sprint 5)

L'outil corrigé produit enfin trois fenêtres distinctes — les longueurs de prompt le
prouvent (4 114 / 4 433 / 4 126 jetons, contre 4 114 aux douze sondes du sprint 4 —
trois répétitions par configuration, toutes à l'offset 0). Mêmes
conditions : 4 096 clés, profondeur 0,5, `--lot 256`.

| configuration | fenêtre 1 | fenêtre 2 | fenêtre 3 | trouvé |
|---|---|---|---|---|
| attention complète | oui (266,2 s) | oui (280,2 s) | oui (251,1 s) | **3/3** |
| **k = 256** (6,25 %) | NON (240,3 s) | **oui** (302,2 s) | **oui** (241,4 s) | **1/3** |
| **k = 1 024** (25 %) | oui (238,9 s) | oui (275,6 s) | oui (265,7 s) | **3/3** |

**La conclusion change de nature** : à k = 256, l'échec n'est pas systématique mais
**probabiliste — 1 fenêtre sur 3**. L'attention complète retrouve l'information dans
les trois cas, k = 1 024 aussi ; k = 256 échoue sur un texte et réussit sur deux.
Autrement dit :

* l'échec du sprint 3 (« NON au milieu ») était **réel mais sur un seul texte** —
  il ne se généralise pas ;
* le « 0/3 » du sprint 4 mesurait trois fois ce même texte, pas trois textes ;
* la bonne formulation est un **taux**, pas un verdict binaire : sur trois fenêtres,
  dense 3/3, k = 256 **1/3**, k = 1 024 3/3.

Trois fenêtres restent un petit échantillon (l'intervalle de confiance d'un 1/3 sur
trois tirages va de 1 % à 90 %) : la mesure à faire est **neuf fenêtres**, ce qui
donne un taux utilisable. C'est l'objet du sprint 6.

### Le k nécessaire croît-il avec le contexte ? (deux points, à 8 192)

| contexte | dense | k = 1 024 | k = 2 048 |
|---|---|---|---|
| 4 096 (trois fenêtres) | **3/3** | **3/3** (25 % du contexte) | — |
| 8 192 (UNE fenêtre) | **oui** (1 002,0 s) | **oui** (764,7 s, 12,5 %) | **oui** (755,7 s, 25 %) |

⚠️ **Ce que ce tableau est, et ce qu'il n'est pas** : à 8 192, chaque ligne est UNE
sonde, sur UNE fenêtre (prompt 7 963 jetons), les trois avec les mêmes réglages
(`--lot 256`, sans `--gpu-kv`) et toutes trois portant l'avertissement « `--attn-topk`
IGNORÉ en mode lot » (le k ne s'applique donc qu'aux 24 jetons générés). **Aucun k
n'échoue à 8 192** : le seuil n'y est pas localisé, et « k = 1 024 suffit » est une
borne supérieure sur un point. Ce qui est établi : à 4 096 clés il fallait 1 024
(25 %), à 8 192 clés 1 024 suffit (12,5 %) — le k nécessaire croît donc **plus
lentement que le contexte** sur ces deux points, ce qui est la direction favorable
pour l'élagage à long contexte, sans être une courbe. Source : `/tmp/aiguille_s5.log`
§B ; contrôle dense : `/tmp/aig8192.log`.

## Ce que ce rapport ne dit pas

* **8 192 : le contrôle dense est mesuré** (sprint 4, une sonde : **trouvé**,
  1 002,0 s pour un prompt de 7 963 jetons) — la question « le k nécessaire
  croît-il avec le contexte ? » est donc mesurable à 8 192 ; 16 384 ne l'est pas.
* **8 192 : mesuré depuis** (dense, k = 1 024, k = 2 048 — une fenêtre chacun,
  section précédente). **16 384 n'est pas mesuré** : le taux du 0.5B est de 58 à
  62 ms par jeton de prompt, soit ≈20 min par sonde à 16 384.
* plusieurs codes par sonde, **plusieurs fenêtres de corpus** : la mesure est
  binaire (trouvé / non trouvé), avec un seul code et — la correction ci-dessus le
  montre — **une seule fenêtre par (contexte, profondeur)**. Un « NON » peut être un
  échec de génération ; le détail (« oui » dense au même endroit) protège de cette
  lecture, mais la généralité inter-fenêtres n'est pas mesurée.
* **un seul modèle** (Qwen2.5-0.5B) : rien ne dit que le seuil k/contexte soit le
  même sur un modèle plus grand.
* **k plus grand : mesuré depuis** (512 et 1 024, section « Suite ») — le seuil est
  entre 12,5 % et 25 % du contexte sur ce cas.
* le préremplissage reste DENSE avec `--lot > 1` : la mesure porte sur le décodage.
  Une grille en `--lot 1` (où tout le passage est creux) est la vérification qui
  manque, et elle serait d'autant plus abordable que le préremplissage par lots est
  déjà branché.

## Reproduire

```bash
# grille du sprint 3 (une sonde par point)
python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256
python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256 --attn-topk 256
python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5 --n 24 --lot 256 --attn-topk 256 --gpu-topk
# grille du sprint 4 (le k), une invocation par k : trois sondes à trois offsets
for k in 256 512 1024; do
  python3 tools/aiguille.py models/Qwen2.5-0.5B-Q8_0.gguf 4096 0.5,0.5,0.5 \
      --n 24 --lot 256 --attn-topk $k
done
```

Sources brutes : `/tmp/aiguille_topk2.log` (sprint 3), `/tmp/aiguille_k.log`
(premier balayage en k), `/tmp/aiguille_rep.log` (les trois répétitions).
