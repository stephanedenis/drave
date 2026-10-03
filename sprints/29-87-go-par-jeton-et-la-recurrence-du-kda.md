# Sprint 29 — 87 Go par jeton, et la récurrence du KDA

- **Début** : 10:50 · **Fin** : 11:40
- **Objectif** : le bloc 28 a installé la cible (Kimi-K3) et sa référence. Ce bloc
  devait répondre à une question que le plan posait sans la trancher : **ce qu'un
  jeton lit vraiment**, et ce que ça impose au placement. Il a répondu — et la
  réponse a corrigé un chiffre publié la veille.
- **Engagement de fin** : dépôt vert, machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. Un jeton de Kimi-K3 lit **87 Go** de poids, pas 35

L'outil de la veille (`analyse_octets_par_jeton.py`) comptait **les experts**, et
c'est ainsi que « 35 Go/jeton » est entré dans le plan et dans la spécification.
Le total, mesuré sur 25 couches (de 93) par `tools/budget_execution_locale.py` :

| | Go par jeton |
|---|---|
| **attention** (q/k/v/o, `ssm_*`, compresseur) — **dense** | **48,7** |
| experts routés (16 sur 896) | 24,7 |
| experts partagés (2) | 12,4 |
| tête de sortie + scores résiduels | 1,3 |
| **TOTAL** | **87,0** (5,8 % du modèle) |

**Deux surprises, et les deux changent les priorités** :

1. **L'attention pèse plus que les experts** (48,7 contre 24,7). Un dispositif qui
   ne traite que le MoE — grappes, cache d'experts, routage — laisse **56 % du
   trafic** de côté.
2. **62,3 Go sont « résidents possibles »** (attention + partagés + tête) et
   **24,7 Go sont routés**. Sur les 125 Go de cette machine, la partie dense
   **tient en RAM** — mais pas en même temps que V4.1-Flash (341 Go) et
   Kimi-K2.7 (284 Go) : ce qui vit en cache est désormais un **arbitrage**.

**Aucun placement ne rend 87 Go/jeton interactif** : disque dur 435 s, NVMe 43 s,
dense en RAM + experts sur NVMe 14,8 s, deux nœuds 8,6 s, RAM seule 4,4 s. La
conclusion est nette : **il faut de la réutilisation**, pas seulement du
placement. 16 experts sur 896 = 1,8 % par jeton ; c'est cette redondance qui
décide, et c'est le jalon M6.

### 2. Les outils disent maintenant ce qu'ils comptent

`tools/budget_execution_locale.py` (neuf) : total par jeton **et** ce que chaque
placement implique, avec les débits **mesurés sur cette machine** (disque dur
200 Mo/s, NVMe 2,0 Go/s, RAM 20 Go/s, PCIe 6,5 Go/s, NVLink 25,8 Go/s). Il valide
son propre calcul sur V4-Flash : experts 1,873 Go + partagé/dense 6,688 = **8,56
Go/jeton**, cohérent avec le compteur de paires du profileur (16,2 G paires).
`analyse_octets_par_jeton.py` garde son rôle (les experts) et **annonce
désormais** qu'il ne compte qu'eux. Les deux corrections sont propagées : plan,
spécification, rapport GPU (où V4-Flash passe de 2,669 à 8,56 Go/jeton).

### 3. Le KDA : la récurrence implémentée et vérifiée

`kda_pas` (Rust) est la transcription de `build_delta_net_autoregressive` :

```
s ← s · exp(g)                          décroissance, par canal de CLÉ
sk[j]  = Σ_i s[i][j]·k[i]               (sᵀ k)
s[i][j] += k[i]·β·(v[j] − sk[j])        mise à jour delta, produit extérieur
o[j]   = Σ_i s[i][j]·q[i]               (sᵀ q)
```

**4 tests**, dont un contre une **référence NumPy en f64** (état *et* sortie), un
sur l'état nul (le produit extérieur, valeurs calculées à la main) et un sur la
porte très négative (l'état est oublié). S'y ajoutent, du bloc précédent, l'activation
**SiTU** et l'**attention résiduelle** (`res_mix`) — soit **75 tests** au total.

Le chemin **par blocs** (`build_delta_net_chunking`, nécessaire au préremplissage)
viendra après : il devra donner **le même** résultat que le chemin autorégressif,
et c'est en soi un point de vérification que la référence porte aussi.

## Rétrospective — garder / changer / doute

**Garder.** L'outil écrit pour une question (« combien pèsent les experts ? ») a
été réutilisé pour une autre (« combien lit un jeton ? ») — et son nom ne le
disait pas. Le nouveau outil **imprime ce qu'il compte et ce qu'il ne compte
pas**, et la vérification croisée (paires du profileur contre octets du fichier)
tient en une ligne. Un chiffre doit porter son périmètre.

**Garder (2).** Le test contre une référence **indépendante** (NumPy en f64) pour
une récurrence : les trois tests structurels auraient pu passer avec une convention
transposée ; c'est la comparaison numérique qui a verrouillé `i` = clé / `j` =
valeur.

**Changer.** Trois chiffres de poids par jeton ont été publiés en deux jours
(2,669 · 35 · 87) parce que chacun mesurait un périmètre différent sans le dire.
La règle à écrire noir sur blanc : **tout chiffre de volume nomme son périmètre**
(experts ? dense ? total ?) et l'outil qui l'a produit.

**Changer (2).** Le plan affichait encore « le poste dominant est le MoE » comme
un acquis. Pour cette classe de modèles, l'attention Q8_0 **dépasse** les experts
MXFP4 en volume par jeton. Les priorités d'optimisation changent, et elles sont
maintenant écrites dans le plan (dense d'abord, routage ensuite).

**Doute.** Les 87 Go sont une **extrapolation** de 25 couches à 93, avec 6 couches
MLA et 19 KDA observées : le ratio est proche du 1:3 réel, mais l'extrapolation
linéaire reste une extrapolation. Elle sera refaite sur le fichier complet dès la
fin du téléchargement (~13h55), et le chiffre publié sera alors **mesuré**, pas
extrapolé — c'est la première chose à faire après le transfert.

**Doute (2).** La réutilisation des experts est *supposée* décisive sans avoir été
mesurée sur ce modèle. Elle pourrait être faible (si le routage est uniforme), et
alors aucun cache ne sauverait les 24,7 Go/jeton : la seule voie serait le
découpage sur plusieurs machines. Le jalon M6 tranchera, et il faut le faire
**avant** d'écrire un cache.
