# Dessin B (poids creux) — le levier reste à trouver : élaguer coûte toujours cher

> Campagne : **cerveau** · dessin : **B — modèle à poids creux** (`docs/modele-pour-drave.md` § 3 B)
> Question : le dessin B promet que la parcimonie des **poids** divise les paires. Il butait sur
> deux murs : **aucun instrument** ne mesurait l'occupation (manque **M9**), et **aucun modèle**
> n'encaissait l'élagage.
> Verdict : **un mur est tombé (l'instrument), l'autre tient.** Les chiffres du 11/10 annonçant un
> modèle « quasi insensible à l'élagage » (×1,09) sont **RÉTRACTÉS** : ils venaient d'un défaut du
> harnais qui laissait l'**attention non élaguée** pour les variantes reparamétrées. Mesuré
> proprement, le meilleur point du plan 2×2 d'E6 (**signes figés + magnitudes libres**) vaut
> **41,67** contre **49,43** au témoin dense à 25 % de poids gardés — soit **×1,19**, pas ×1,09, et
> les deux sont très loin de leur point de départ (7,30 et 7,34).
> Date réelle : **2026-10-11 03 h 05 HAE**.
> Mesures : [`rapport-e6-poids-lognormaux.md`](rapport-e6-poids-lognormaux.md) § 1 (le plan 2×2
> corrigé, avec la rétractation) · occupation : `tools/occupation_poids.py` ·
> invariants : `tools/porte-harnais-invariants.sh`.

## 1. Ce qui bloquait, et ce qui est débloqué

| mur | état avant | état après |
|---|---|---|
| **mesurer** la sparsité des poids | le compteur de paires du moteur additionne `n_in × n_out` : **2,3 M avant comme après** un élagage à 50 % de tous les tenseurs (`--flux`, `--flux-listes`, `--flux-blocs`, `--keep 0.5`) — manque **M9** | `tools/occupation_poids.py` lit l'**occupation** du fichier par genre (F32, F16, Q8_0, Q4_0) |
| **encaisser** l'élagage | le témoin dense est multiplié par **6,7** à 25 % gardés | la recette **signes figés** : **×1,09**, pour un coût nul avant élagage |

## 2. Le noyau creux : ce qu'il paie, et ce qu'il coûte

Le 11/10, la pièce qui manquait a été écrite : une forme **CSR par lignes** (`Creux`), construite au
chargement quand `DRAVE_POIDS_CREUX=1`, et utilisée dans les deux chemins de calcul. Trois mesures,
sur `models/Qwen2.5-0.5B-Q8_0.gguf` et un corpus tokenisé par le modèle :

| mesure | noyau dense | noyau creux | verdict |
|---|---:|---:|---|
| perplexité, modèle **intact** | 14,6496 | 14,6567 | **+0,05 %** : les deux noyaux s'accordent |
| perplexité, élagué à 25 % | 245 056 | 232 958 | −5 % : le creux est le **meilleur** des deux |
| **paires d'attention**, élagué à 25 % | 44,4 M | **11,1 M** | **÷4** — la sparsité est **payée** |
| paires totales, élagué à 25 % | 496,8 M | **226,4 M** | ÷2,2 (modèle dense) |
| **débit** de génération, élagué | **1400 tok/s** | 900 tok/s | **−36 %** : le creux est plus LENT |

**Et sur le modèle à EXPERTS du harnais** (25 % gardés, où les experts pèsent 1,8 M des 2,3 M de
paires) — c'est là que le noyau creux change d'échelle, une fois les experts branchés comme les
projections d'attention :

| mesure | noyau dense | noyau creux |
|---|---:|---:|
| perplexité | 4,5886 | **4,5886** (identique) |
| paires d'attention | 0,4 M | 0,1 M |
| **paires d'experts** | 1,8 M | **0,4 M** |
| **paires totales** | 2,3 M | **0,6 M** (**÷3,8**) |

**Ce que ça dit, sans arrondir.** Le noyau creux **paie** la sparsité : il lit 4 fois moins de poids
d'attention et le compteur de paires le voit. Mais il **ne va pas plus vite** — un parcours CSR
scalaire en `f32` perd contre un noyau dense **int8 vectorisé**, même en lisant quatre fois moins.
Autrement dit : **« moins de paires » n'est pas « plus rapide »** ; le coût en paires est un modèle,
la vitesse est une mesure, et les deux ne coïncident que si le noyau creux est lui aussi optimisé.

Les deux noyaux ne font d'ailleurs **pas la même arithmétique** : le dense quantifie les poids en
int8 (et les activations), le creux multiplie les poids **déquantifiés** en `f32`. Sur un modèle
sain l'écart est de 0,05 % ; sur un modèle détruit il atteint 5 % — et c'est le creux qui est le
plus **fidèle**, pas le plus rapide.

## 3. Ce que ça change pour le dessin B

- **le levier existe enfin, mesurable** : la sparsité des poids se paie en paires (÷4 sur
  l'attention) au lieu de s'annoncer ;
- **il ne paie pas encore en temps** : il faudrait un noyau creux **vectorisé** (SIMD, ou blocs
  creux de 32 alignés sur la quantification) — c'est un travail de noyau, pas de modèle ;
- **les experts sont branchés** : 1,8 M → 0,4 M de paires sur le modèle à experts (÷3,8 au total,
  qualité identique). C'est la première fois que le dessin B est **payé** sur tout le modèle ;
- **la vitesse reste contre nous** : −36 % malgré 3,8× moins de poids lus. Le prochain pas n'est pas
  un modèle, c'est un **noyau** : vectoriser le parcours creux (SIMD, ou blocs creux de 32 alignés
  sur la quantification) pour que le compte devienne du temps.

## 4. Ce que cette fiche ne dit PAS

- **la cause profonde est ouverte** : on ne sait pas pourquoi l'élagage coûte autant, ni pourquoi la
  loi log-normale l'aggrave ;
- **une seule échelle** (7,58 M paramètres), un corpus, une graine ;
- **l'occupation n'est pas le coût** : 26 % de non-nuls dans un fichier **dense** ne réduisent
  aucune lecture tant que le noyau lit la matrice entière ;
- **la recette n'est pas testée sur un vrai modèle** : ni Qwen, ni un modèle de campagne.
