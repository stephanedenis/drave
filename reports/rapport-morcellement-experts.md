# Rapport — peut-on « morceler » un modèle ? L'élagage par fréquence, mesuré

**Question** (posée par Stéphane) : Drave permet d'optimiser un modèle couche par
couche selon les scénarios d'usage à l'entrée de chaque couche ; on pourrait donc
construire par distillation un MoE très malléable, « morcelé de façon optimale »,
qui garde les qualités des meilleurs modèles.

**Ce qui est testable sans entraîner** : la prémisse « une version morcelée garde
les qualités du modèle ». Si l'élagage par **fréquence mesurée** tient, l'idée
tient ; sinon, elle a besoin d'autre chose.

## Le protocole

Qwen3-30B-A3B (48 couches, **128 experts, 8 par jeton**), scénario **code** :
384 jetons du code source de ce dépôt (`kimi_k3.rs`, `list.rs`, `engine.rs`),
tokenisés par le tokenizer du modèle.

1. trace de routage réelle (`DRAVE_TRACE_EXPERTS`) : 18 432 lignes ;
2. par couche, on garde les K experts les plus appelés ;
3. `DRAVE_EXPERTS_GARDES=<liste>` masque les autres dans le routeur (`-inf` sur
   la sélection ; la renorme des poids se fait sur les seuls retenus) — c'est
   donc **un autre modèle**, et il se mesure comme tel.

## Le résultat

| experts gardés | masse de routage couverte | perplexité | coût |
|---|---:|---:|---:|
| **128** (original) | 100 % | **9,584** | — |
| 96 (75 %) | 99,6 % | 11,327 | **+18,2 %** |
| 64 (50 %) | 94,3 % | 12,515 | **+30,6 %** |
| 32 (25 %) | 74,2 % | 18,605 | **+94,1 %** |

## Ce que ça dit

**1. La fréquence n'est pas l'importance.** Retirer le quart le moins appelé des
experts coûte **18 % de perplexité** alors que ces experts ne portent que
**0,4 %** de la masse de routage. Un expert appelé une fois sur cent peut être le
seul à traiter un motif donné ; le retirer coûte précisément sur ces jetons.

**2. La relation masse → qualité est violemment non linéaire.** 99,6 % de masse
couverte → +18 % de perplexité. 74,2 % → +94 %. Optimiser la masse couverte est
donc le mauvais objectif.

**3. Le morcellement n'est pas absurde pour autant.** À 50 % d'experts gardés, le
coût est de +30 % de perplexité — et c'est l'ordre de grandeur des résultats
publiés : le « Coder » d'ISTA-DASLab garde 256 experts sur 512 et annonce 91,3 %
du SWE-bench. La différence n'est pas la quantité, c'est **le critère de choix** :
RCO alloue sur données de calibration, pas au comptage.

## Ce que Drave peut faire, et que les autres ne font pas

Le critère qui manque est l'**importance**, et elle se mesure sans gradient :
**par retrait** (leave-one-out) sur les flux RÉELS du scénario.

- `--trace-flux` capture l'entrée exacte de chaque couche pour un scénario, et
  `--flux-forcer` la **rejoue à l'identique**. La couche peut donc être évaluée
  seule, contre la distribution qui l'intéresse vraiment — pas contre un corpus
  générique.
- Pour chaque expert d'une couche : mesurer l'écart de sortie quand on le retire.
  C'est une mesure d'importance **sans rétropropagation**, sur des flux en cache,
  donc peu coûteuse par couche.
- La porte de correction (`compare_logits.py --porte`) est le juge : corrélation,
  top-1, perplexité, avec ses positions saturées exclues et le critère écrit
  comme un taux.

**C'est exactement « optimiser un modèle couche par couche en fonction des
scénarios d'utilisation à l'entrée d'une couche »** — et Drave en a les deux
moitiés : capturer le flux, et juger le résultat.

## La limite, dite franchement

Drave **sélectionne**, il ne **crée** pas. La distillation qui produirait un
nouveau modèle demande des passes arrière, donc un cadre d'entraînement, donc du
calcul GPU que cette machine n'a pas (2 × 16 Go en PCIe). Ce qui est à portée
ici : **choisir** quels experts garder avec un bon critère, et **prouver** ce que
le modèle morcelé perd. Le reste est un projet d'entraînement.

## Ce qu'il faut mesurer ensuite

1. l'importance par retrait sur les flux capturés, contre la fréquence — sur le
   même scénario code, et comparer les deux critères à budget égal d'experts ;
2. la même mesure sur K3 (896 experts par couche : l'élagage y a beaucoup plus de
   marge, et c'est là que le morcellement paierait) ;
3. un scénario **par couche** : la question posée est « à l'entrée d'une couche »,
   donc le profil peut différer d'une couche à l'autre — à vérifier plutôt qu'à
   supposer.
