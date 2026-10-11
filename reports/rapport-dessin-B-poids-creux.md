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

## 2. La mesure, corrigée

| poids gardés | témoin dense | signes figés (magnitudes libres) | log-normal (signes figés) | occupation |
|---|---:|---:|---:|---:|
| 100 % | 7,3429 | **7,3003** | 7,6168 | 89,2 % |
| 50 % | 7,5680 | **7,2241** | 7,8401 | 50,6 % |
| 25 % | 49,4291 | **41,6677** | 71,1531 | 26,0 % |

**Le facteur d'élagage reste brutal** : ×6,7 pour le témoin, ×5,7 pour le meilleur point du plan
(41,67 / 7,30). Le dessin B n'a donc **pas** trouvé, ce jour, de modèle qui encaisse l'élagage sans
douleur — il a trouvé un **instrument** qui dit la vérité sur l'occupation, et une **loi des poids
qui coûte** (la log-normale).

## 3. Ce que ça change pour le dessin B

- **l'instrument existe** : `tools/occupation_poids.py` lit l'occupation d'un GGUF par genre, et
  c'est lui qui a démasqué deux défauts du harnais (voir la rétractation, § 0 de la fiche E6) ;
- **le levier d'élagage reste à trouver** : ni la loi log-normale (elle coûte), ni la contrainte de
  signe seule (effet incohérent : ×1,19 dans un sens, ×0,83 dans l'autre) ne rendent l'élagage
  indolore ;
- **le couple avec le format creux reste à faire** : le gain de paires n'existe que si la
  représentation est creuse, et le compteur du moteur ne la voit pas (seconde moitié de **M9**).

## 4. Ce que cette fiche ne dit PAS

- **la cause profonde est ouverte** : on ne sait pas pourquoi l'élagage coûte autant, ni pourquoi la
  loi log-normale l'aggrave ;
- **une seule échelle** (7,58 M paramètres), un corpus, une graine ;
- **l'occupation n'est pas le coût** : 26 % de non-nuls dans un fichier **dense** ne réduisent
  aucune lecture tant que le noyau lit la matrice entière ;
- **la recette n'est pas testée sur un vrai modèle** : ni Qwen, ni un modèle de campagne.
