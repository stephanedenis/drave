# Dessin B (poids creux) — le levier existe enfin : élaguer à 25 % coûte ×1,09, pas ×6,7

> Campagne : **cerveau** · dessin : **B — modèle à poids creux** (`docs/modele-pour-drave.md` § 3 B)
> Question : le dessin B promet que la parcimonie des **poids** divise les paires. Or il butait sur
> deux murs : **aucun instrument** ne mesurait l'occupation (manque **M9**), et **aucun modèle**
> n'encaissait l'élagage (le témoin dense est multiplié par 6,7 à 25 % de poids gardés). Les deux
> murs sont tombés le même jour.
> Verdict : **le levier est là — à condition de changer la PARAMÉTRISATION des poids, pas leur loi.**
> Un modèle entraîné avec des **signes figés** (`w = signe · |θ|`, principe de Dale) élagué à 25 %
> ne perd que **×1,09** de perplexité (7,3003 → 7,9467) là où le témoin dense perd **×6,7**
> (7,3429 → 49,4291) — et il ne coûte **rien** avant élagage. Résultat tenu sur **trois graines**.
> Date réelle : **2026-10-11 01 h 45 HAE** (heure lue sur la machine).
> Mesures : [`rapport-e6-poids-lognormaux.md`](rapport-e6-poids-lognormaux.md) (le plan 2×2) ·
> occupation : `tools/occupation_poids.py` · porte : `tools/porte-signes-figes.sh`.

## 1. Ce qui bloquait, et ce qui est débloqué

| mur | état avant | état après |
|---|---|---|
| **mesurer** la sparsité des poids | le compteur de paires du moteur additionne `n_in × n_out` : **2,3 M avant comme après** un élagage à 50 % de tous les tenseurs (`--flux`, `--flux-listes`, `--flux-blocs`, `--keep 0.5`) — manque **M9** | `tools/occupation_poids.py` lit l'**occupation** du fichier par genre (F32, F16, Q8_0, Q4_0) |
| **encaisser** l'élagage | le témoin dense est multiplié par **6,7** à 25 % gardés | la recette **signes figés** : **×1,09**, pour un coût nul avant élagage |

## 2. La mesure

Mêmes conditions partout (7,58 M paramètres, 3 000 pas, même graine, mêmes 28 tenseurs élagués,
même export, même texte), l'occupation **lue dans le fichier** :

| poids gardés | témoin dense | **signes figés** | occupation stockée (dense / signes figés) |
|---|---:|---:|---|
| 100 % | 7,3429 | **7,3003** | 89,2 % / 89,2 % |
| 50 % | 7,5680 (+3,1 %) | **7,3470** (+0,6 %) | 50,6 % / 53,5 % |
| 25 % | 49,4291 (**×6,7**) | **7,9467** (**×1,09**) | 26,0 % / 30,3 % |

**Trois graines à 25 % gardés** — le résultat n'est pas une graine chanceuse :

| graine | témoin dense | signes figés |
|---|---:|---:|
| 1 | 49,4291 | 7,9467 |
| 2 | 55,4520 | 7,9873 |
| 3 | 46,6111 | 8,2676 |

**Ce qu'un format creux lirait** (estimation : `occupation × paires noyau`, en supposant les
non-nuls répartis comme les activations vivantes — **hypothèse**) :

| modèle | paires noyau (moteur) | paires creuses estimées | ÷ |
|---|---:|---:|---:|
| signes figés, aucun élagage | 2,20 M | 1,99 M | ÷1,11 |
| **signes figés, 25 % gardés** | 2,20 M | **0,67 M** | **÷3,3** |

## 3. Ce que ça change pour le dessin B

- **le levier est un changement d'ENTRAÎNEMENT, pas de moteur** : trois lignes (`w = signe · |θ|`,
  signe tiré à la naissance et jamais modifié). Aucun drapeau du moteur, aucun format nouveau ;
- **le prix est nul** : à 100 % gardés, le modèle à signes figés rend **7,3003** contre **7,3429**
  au témoin. On n'échange pas de la qualité contre de la robustesse ;
- **le couple avec le format creux reste à faire** : le ÷3,3 est une **estimation**, et le compteur
  du moteur ne la vérifie pas (seconde moitié de **M9**). Ce qui est mesuré, c'est l'**occupation**
  du fichier — 30,3 % de non-nuls — et la **qualité**.

## 4. Ce que cette fiche ne dit PAS

- **la cause profonde est ouverte** : on sait que figer les signes rend l'élagage indolore, on ne
  sait pas **pourquoi**. L'hypothèse la plus simple — un signe figé interdit au gradient de
  « retourner » une connexion, donc l'élagage ne peut pas créer de poids de signe opposé — n'est
  pas testée ;
- **une seule échelle** (7,58 M paramètres) et un seul corpus pour la mesure principale ;
- **l'occupation n'est pas le coût** : 30,3 % de non-nuls dans un fichier **dense** ne réduisent
  aucune lecture tant que le noyau lit la matrice entière. Le gain n'existe que si la
  représentation est creuse — et cette représentation n'est pas encore mesurée de bout en bout ;
- **la recette n'est pas testée sur un vrai modèle** : ni Qwen, ni un modèle de campagne à
  plusieurs centaines de millions de paramètres.
