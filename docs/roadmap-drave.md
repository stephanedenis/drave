# Où Drave est à son meilleur — le roadmap, et pourquoi c'est cette niche-là

> Écrit après la mesure du 05/10. Chaque chiffre de ce document vient d'un relevé
> du dépôt ; ceux qui viennent d'ailleurs sont marqués.
>
> **MISE À JOUR DU 07/10 — LA PASSE K3 EST LIÉE AU DISQUE, ET RIEN D'AUTRE.**
> `reports/rapport-passe-k3-disque.md` mesure la passe complète : **1 587 s**,
> dont **206,58 Gio lus** à **133 Mio/s**, avec **`sda` (disque DUR de 10,9 To)
> occupé 87,6 % du temps** et le CPU à **21 %**. La vérification est exacte à
> 0,1 % : 206,58 Gio à 133 Mio/s = 1 589 s.
>
> Deux conséquences pour ce document :
> 1. **L'axe 1 est mal nommé.** Le regroupement des jetons par expert **est déjà
>    implémenté** (`MoeK3::avant_lot`, `kimi_k3.rs:787`) — le point qui le donnait
>    pour absent est périmé. Il ne paie pas à 4 jetons parce qu'il n'y a rien à
>    regrouper ; le levier n'est pas du code, c'est la **TAILLE DU LOT**.
> 2. **L'axe 3 change de statut.** Il n'est plus « le seul moyen de descendre
>    sous la minute » : c'est **le seul levier qui multiplie un débit de disque**.
>    À 87,6 % d'occupation, trois nœuds à un disque chacun valent ×3, mesurable.
>
> Et une hypothèse est **réfutée** : la « dispersion » (la tête qui se déplace).
> Le disque ne cherche pas, il débite — file de ~14 requêtes, 87,6 % d'occupation.
> En revanche il reste **~35 % de débit à récupérer par le MOTIF d'accès** : une
> copie séquentielle du même modèle tient 205 Mio/s, la passe en obtient 133.

## 1. La niche, définie par une mesure

| | lectures par jeton | vitesse | source |
|---|---:|---:|---|
| llama.cpp-k3 sur Kimi-K3 | **451 Go** (1,80 To pour 4 jetons, 5,2 balayages) | 42 min/jeton | `docs/verification-kimi-k3.md` |
| Drave sur le même fichier | **26 Go** d'experts (16 sur 896) | **7,4 min/jeton** | idem |

Ce n'est pas une victoire de vitesse, c'est une victoire d'**existence**. Et les
concurrents ne sont pas lents, ils ne **fonctionnent pas** :

- **llama.cpp** repaquette les poids en RAM par défaut : 104 Go résidents et
  6,9 Go de swap après **16 tenseurs sur 2 573**, sur une machine de 125 Go. Il
  ne finit pas (`REF_SANS_REPACK` est né de là) ;
- **Strata** exige que **tous** les experts tiennent en RAM (34-50 Go) : sa cible
  est la classe 100-350 Go. Ses propres chiffres le disent — quand il doit lire
  du SSD, il tombe à 7-8,5 tok/s ;
- **vLLM et consorts** sont GPU-résidents : hors sujet à 1,5 To ;
- **Ollama** *est* llama.cpp.

**La niche est donc : quand la RAM fait moins de ~15 % du modèle et que le poids
est sur disque.** Personne d'autre n'y fonctionne.

## 2. Les quatre axes, dans l'ordre où ils paient

### Axe 1 — Le LOT, pas le code (le socle) — RÉVISÉ LE 07/10

Mesuré depuis : la passe de 4 jetons lit **206,58 Gio**, dont **57,93 Gio (28 %)
de dense — lu UNE fois et partagé par les quatre jetons — et 148,65 Gio (72 %)
d'experts, relus pour CHAQUE jeton à chaque couche.** Les octets d'experts sont
proportionnels au nombre de jetons ; ceux du dense non.

- **le regroupement par expert EXISTE** (`MoeK3::avant_lot`). Il ne rapporte rien
  à 4 jetons (collisions rares sur ~581 experts), et c'est ce qui explique la
  phrase « réduire de 25 % les experts lus ne change rien » — pas que les octets
  cessent de compter ;
- **le levier est donc la taille du lot.** À k=16 et n≈581, un lot de 64 jetons
  lirait ~1 174 Gio au lieu de 1 174/16 par jeton, soit **2,8× moins d'octets par
  jeton** ; un lot de 512 lirait le modèle entier une fois, **19× mieux**. Modèle
  et prédictions : `reports/rapport-passe-k3-disque.md` §7.1 ;
- **le noyau AVX2 Q8_0** reste valable, mais il ne touche que 4 % des octets.

Critère, révisé : la passe sous 10 min demande de lire **moins de 78 Gio** à
133 Mio/s, soit 2,6× moins qu'aujourd'hui. Le critère est un critère d'octets et
de disques, pas de code.

### Axe 2 — Le décodage spéculatif (le multiplicateur)

C'est le seul moyen de rendre le décodage **par lots** — donc de faire servir au
décodage ce que le regroupement par experts donne au préremplissage. Aujourd'hui
un jeton de décodage n'a pas de voisins, et la réutilisation mesurée (30,2 %
immédiate sur K3) ne peut pas être exploitée.

Prérequis : un modèle brouillon. K3 n'a pas de couche MTP vérifiée ; un petit
modèle de la même famille ferait l'affaire, à condition de mesurer le taux
d'acceptation — un brouillon qui n'est pas accepté coûte plus qu'il ne rapporte.

Critère : ≥ 2 jetons acceptés par passe sur du code.

### Axe 3 — La grappe (le seul moyen de descendre sous la minute)

Un nœud = une plage de couches, chacun ne lit que son shard. Le découpage tient
déjà : cinq modes sous porte, écarts nuls à 4,45e-3 (`tools/portes.sh`,
§ Découpage). À trois nœuds, 1 508 Go deviennent 500 Go chacun — et une passe de
25 min devient ~8 min.

C'est la carte propre de Drave sur cette classe : personne ne découpe un modèle
de 1,5 To pour le faire tenir sur des machines ordinaires.

### Axe 4 — La porte de correction comme produit

« Prouvez que votre moteur calcule bien le même modèle. » La méthodologie existe
(`tools/compare_logits.py --porte`, `tools/compare_etats.py`), et c'est elle qui
a trouvé les trois bugs de Kimi-K3 en deux heures après deux jours de relecture
qui n'avaient rien vu. Le critère est écrit comme un taux, pas comme un
extremum ; les positions saturées sont exclues et le disent.

## 3. Ce qu'il faut ARRÊTER — et c'est mesuré, pas supposé

| chantier | pourquoi non |
|---|---|
| courir après les tok/s sur les modèles qui tiennent en RAM | llama.cpp y est mûr, SIMD, avec des noyaux GPU. Drave n'y a aucun avantage |
| des noyaux GPU pour le MoE | les poids ne peuvent pas être en VRAM : 2,7-3,9 Go/jeton contre 32 Go disponibles |
| un cache d'experts en VRAM pour K3 | mesuré : plafond ×1,41, verdict ×1,09 (29,3 % du trafic seulement) |
| rendre le dense résident | la page cache ne le garde pas (deux passes : 1 516 430 puis 1 522 584 ms) et la copie anonyme swape (VmSwap 28,5 Go) |
| **chercher la « dispersion » des lectures** | **réfuté (07/10)** : le disque est occupé 87,6 % avec une file de ~14 requêtes — il débite, il ne cherche pas. Le temps est celui du VOLUME. Reste en revanche la pénalité de MOTIF : 133 Mio/s contre 205 en séquentiel |
| le découpage en clusters pour les modèles qui tiennent en RAM | aucun besoin ; c'est un outil pour la classe hors-RAM |

## 4. L'ordre, avec un critère mesurable par étape

| étape | gain | critère de réussite |
|---|---|---|
| regroupement par experts dans la couche | ×1,3 à ×1,6 sur les lectures d'experts | passe à 4 jetons sous 20 min |
| noyau AVX2 Q8_0 | −80 s sur l'attention | idem |
| décodage spéculatif | ×1,58 (mesuré en préremplissage) | 2 jetons acceptés par passe |
| grappe à 3 nœuds | ×3 | 2,5 min par passe complète |

## 5. Le positionnement, en une phrase

**Drave n'est pas un moteur rapide. C'est le seul moteur qui FINIT un modèle de
1,5 To sur une machine de 125 Go — et il le prouve contre la référence, logits en
main, top-1 identique.**
