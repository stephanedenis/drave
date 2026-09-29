# Localité d'activation : ce que PowerInfer apporte, et ce qu'on en garde

> Étude demandée du dépôt [SJTU-IPADS/PowerInfer](https://github.com/SJTU-IPADS/PowerInfer)
> (miroir `Tiiny-AI/PowerInfer`), confrontée à nos propres mesures. Tout ce qui
> suit est mesuré sur cette machine ; les chiffres de PowerInfer viennent de leur
> README et de l'article SOSP 2024.

## 1. Leur idée

La distribution des activations d'un LLM suit une **loi de puissance** : une
petite partie des neurones est active presque toujours (« chauds »), le reste
dépend de l'entrée (« froids »). PowerInfer en tire un moteur hybride CPU/GPU
**à la granularité du neurone** : les chauds résident sur le GPU, les froids sont
calculés sur le CPU, ce qui réduit à la fois la VRAM nécessaire et le trafic
PCIe. S'y ajoutent un **prédicteur** (un petit MLP qui devine l'ensemble actif
pour précharger) et des **opérateurs creux conscients des neurones**. Leur modèle
TurboSparse (≈ 90 % de creux) est *entraîné* ainsi, précisément parce
qu'imposer la parcimonie à l'inférence coûte cher en qualité.

## 2. Ce que le moteur avait déjà

| leur mécanisme | notre équivalent | mesure |
|---|---|---|
| opérateurs creux par neurone | chemin par **listes d'événements** (`SparseVec`, push) | bascule push/pull mesurée à **22 % de densité** (`seuil_push = 0.22`) |
| parcimonie exploitable | `--act-topk`, `--act-thresh`, `--act-renorm` | courbe qualité/octets mesurée ; conclusion identique à la leur : la parcimonie imposée coûte, elle se gagne à l'entraînement |
| profil d'activation | capteur hebbien (`--hebbian`) | journalise les co-activations entrée→sortie d'une couche |
| déport GPU | matrices entières, seuil de rentabilité mesuré (8 Mo) | granularité **grossière** : pas de placement par neurone |

## 3. Ce qu'on a ajouté, et ce que ça dit

`--profil-neurones` (et `--neurones-sortie F` pour le classement) compte, pour
chaque neurone intermédiaire de chaque couche FFN, le **taux de tir** et la
**somme des magnitudes**. Un neurone est « tiré » quand son activation dépasse
5 % du maximum du vecteur : chez eux, zéro est exact (ReLU), chez nous le SiLU
n'a pas de zéro franc, il faut donc un seuil relatif — le critère « valeur
quantifiée non nulle » laissait passer 100 % des neurones à 16 bits
(mesuré : densité de 51 104 %).

Qwen2.5-0.5B, 512 jetons, wikitext :

| mesure | valeur |
|---|---|
| densité d'activation (seuil 5 % du max) | **17,9 %** des neurones par jeton (82 % ne font rien) |
| magnitude portée par les 1 / 10 / 50 % de neurones les plus lourds | 12,3 % / **33,1 %** / 74,2 % |
| neurones tirés **> 90 %** du temps | **0,08 %** |
| neurones tirés > 50 % du temps | 2,82 % |
| dispersion entre couches | 173 à 1 579 tirs par jeton (×9) ; part des 10 % les plus lourds : 16,7 à 51,1 % |

**Lecture** : la localité existe (82 % des neurones sont inactifs par jeton) mais
elle est **dynamique**, pas statique : l'ensemble *toujours* chaud est
minuscule (0,08 %). Un préchargement figé à la PowerInfer ne couvrirait donc
presque rien sur un modèle SiLU. C'est cohérent avec leur propre trajectoire :
leurs gains viennent des modèles **ReLU/TurboSparse**, entraînés pour avoir des
zéros francs.

## 4. Ce qu'on en garde, dans l'ordre

1. **Le placement par expert, pas par neurone** — c'est l'analogue MoE et notre
   vrai enjeu : gpt-oss active 4 experts sur 128 par couche et par jeton. Le
   profileur compte désormais les choix d'experts (`profil_experts`) ; si un
   petit noyau couvre l'essentiel des routages, un **cache d'experts chauds en
   VRAM** (32 Go sur les deux RTX 5000, pour un modèle de 62 Go) devient
   rentable, d'autant que le noyau MXFP4 « warp par ligne » tourne maintenant à
   42 Go/s avec un résultat **bit à bit identique** au CPU.
2. **Un cache à éviction plutôt qu'un préchargement figé** : puisque la
   localité est dynamique, garder en VRAM les experts les plus récemment
   utilisés capte ce que le profil statique rate.
3. **Prédicteur + préchargement** : utile seulement quand le « froid » n'est pas
   en RAM — notre cas « modèle > 125 Go » (plan 1 M), où l'activation doit être
   prévue pour lancer le transfert NVMe à temps.
4. **La leçon de qualité** : leur TurboSparse confirme notre mesure — la
   parcimonie s'entraîne ; nos drapeaux `--act-*` restent des outils de mesure.

## 5. Ce qu'on ne copie pas

- Le **préchargement statique** comme mécanisme principal : notre ensemble chaud
  stable est trop petit (0,08 %) pour payer la complexité.
- Leurs **noyaux** : ils exploitent la parcimonie ReLU exacte ; la nôtre est un
  seuil relatif, et notre moteur d'événements fait déjà ce travail côté CPU.
- La **granularité neurone côté GPU** : sur nos modèles, le gain attendu est
  faible devant le coût d'un cache par ligne ; l'expert est la bonne maille.
