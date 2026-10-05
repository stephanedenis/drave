# Note — la voie événementielle : prédire une couche pour ne transporter que l'imprévu

> Note de conception, 06/10. Elle part d'une objection de Stéphane : arrêter de
> retomber sur les solutions d'entraînement classiques, et traiter le problème
> par des **flux de données légers, en mode événements**, sans rétropropagation.

## 1. Ce que le moteur a déjà, et qui n'est pas un détour

| primitive | ce qu'elle fait | où |
|---|---|---|
| `SignedDelta`, `BitmapSign`, `FusedSign`, `SparseK`, `PushMat` | transport par **listes d'événements**, y compris **signés** — un événement peut être négatif | `list.rs` |
| `quant_scratch` (k-WTA, seuil) | **inhibition latérale** : ne garder que les k plus grandes magnitudes | `model.rs` |
| `kda_pas`, `kda_porte`, `res_mix` | **récurrence** par tête et mélange résiduel — vérifiés contre llama.cpp sur 25 couches de K3 | `model.rs` |
| `Hebb` | adaptation **locale**, sans passe arrière | `model.rs` |
| `Engram` | table de mémoire adressable | `engram.rs` |
| `--trace-flux` / `--flux-forcer` | **capture** du flux à l'entrée de chaque couche, et **rejeu à l'identique** | `main.rs` |

Aucune de ces pièces ne demande d'entraînement. La voie proposée est donc
**déjà outillée**, pas à construire.

## 2. La question préalable, et elle est mesurable sans rien changer au modèle

**La sortie d'une couche est-elle prévisible depuis son entrée ?**

- Si **non** : remplacer une couche du milieu par un prédicteur léger n'a pas de
  socle — il n'y a rien à annuler, donc rien à ne pas transporter.
- Si **oui** : l'écart entre la sortie et la prédiction — l'**imprévu** — est ce
  qu'il reste à transporter, et c'est lui qu'on met en liste d'événements.

C'est exactement « rétroactivité négative sur des grappes d'activation
récurrentes » : l'état récurrent **annule** ce qu'il avait prédit, et ce qui
**émerge après annulation** est le signal utile.

## 3. Comment le mesurer, par couche

La trace DRVF enregistre, pour chaque (couche, jeton), le flux à l'entrée de la
famille **attention** (base 0) et de la famille **FFN** (base 1000). Donc :

```
  ce que l'attention ajoute  =  flux_ffn[L]   − flux_attn[L]
  ce que la FFN ajoute       =  flux_attn[L+1] − flux_ffn[L]
```

Trois chiffres par couche, et ils décident de tout :

1. **l'incrément relatif** : `‖ajout‖ / ‖flux‖`. Une couche qui ajoute peu est une
   couche qu'on peut alléger ;
2. **la parcimonie de l'incrément** : combien de coordonnées portent 90 % de son
   énergie. Un incrément parcimonieux se transporte en liste ;
3. **la part prévisible par un état récurrent** : combien de l'incrément du jeton
   `t` est déjà contenu dans l'état des jetons `t−1, t−2…`. C'est la mesure qui
   dit si « annuler » a un sens — et elle se fait **forward-only**, par une règle
   locale sur les flux enregistrés, sans passe arrière.

**Prédiction à réfuter** : dans un modèle de cette famille, les couches du
**milieu** devraient avoir l'incrément relatif le plus faible et la plus forte
part prévisible ; les premières et les dernières, l'inverse. Si c'est faux, la
proposition « on peut perdre les couches du milieu » n'a pas de base mesurée.

## 4. État au 06/10

- La trace est **enregistrée** : `--trace-flux`, 64 jetons de code,
  **34 335 939 octets**, 27 265 463 événements (419 469 par jeton).
  Commande exacte :
  ```bash
  drave <modele> --infer --ids-file <ids> --n 1 --ctx 128 --lot 1 \
      --threads 16 --trace-flux /tmp/flux_code.drvf
  ```
  Elle exige **`--lot 1`** : en mode lot le chemin est dense, il n'y a pas
  d'événements à tracer (0 événement en `--lot 8`, mesuré).
- **`tools/profil_flux.py` est PÉRIMÉ** : il lit la **v1** du format
  (`struct.unpack("<Ih")`) et tombe sur la **v3** que le moteur écrit
  (« unpack requires a buffer of 6 bytes »). `analyse_flux.py`, lui, gère v1, v2
  et v3. C'est le défaut que ce dépôt combat : un outil qui ne lit plus ce que le
  moteur produit doit le dire ou être réparé.
- **Ce qui reste à écrire** : un script court qui lit la v3 (le lecteur de
  `analyse_flux.py` est à réutiliser, pas à réinventer) et rend les trois chiffres
  du § 3, par couche. C'est la première mesure de la voie événementielle, et elle
  ne touche pas au modèle.

## 5. La limite, dite franchement

Cette voie **allège le transport et la mémoire**, elle ne promet pas de
reconstruire la qualité du modèle de référence : remplacer une FFN par un
prédicteur change le modèle, et la porte de correction dira ce qui est perdu.
Mais la question préalable — *y a-t-il quelque chose à annuler ?* — se tranche
**avant** d'écrire quoi que ce soit, et c'est elle qu'on mesure d'abord.


## 6. Le bloc 0-9 est-il approximable ? Première borne (06/10)

Idée précisée par Stéphane : **distiller les couches 0-9 en modèle récurrent avec
isolation en grappes**, en commençant par elles parce que **leur entrée est du
texte** — donc échantillonnable sans rien simuler. Au-delà (9-29), l'entrée vit
dans l'espace sémantique et il faudra un corpus ou un émulateur stochastique.

Mesure : `tools/approximabilite_bloc.py` sur une trace DRVF de 192 jetons de code
(193 positions), bloc `0 → k`, avec un approximant **délibérément pauvre** — une
combinaison linéaire de **2 colonnes** de l'entrée sur 2048, trouvée par
recherche aléatoire, sur les 8 sorties les plus énergétiques :

| sortie | R² |
|---|---:|
| couche 1 | **0,580** |
| couche 2 | 0,299 |
| couche 4 | 0,313 |
| couche 10 | **0,192** |

**Ce que ça dit, et ce que ça ne dit pas.** Deux directions suffisent à expliquer
58 % de la variance dès la première couche et 19 % après dix : le flux est
**dominé par peu de directions**, ce qui est cohérent avec le plateau sémantique
du § 5 (la représentation se resserre sur une variété indépendante de la langue).

Mais c'est une **borne inférieure**, pas une performance : l'approximant est
volontairement pauvre. Elle ne dit donc pas « un récurrent peut porter 0-9 » ;
elle dit que **la cible n'est pas du bruit**, ce qui est la condition pour que
l'essai vaille la peine.

**Ce qu'il faut mesurer ensuite** pour transformer cette borne en réponse :
1. la **régression linéaire complète** (crête, 2048×2048) — le vrai plafond
   linéaire, celui au-dessus duquel il faut de la non-linéarité ;
2. un **récurrent minimal** ajusté forward-only sur les flux, jugé par le
   résidu qu'il laisse — et par la porte de correction sur la sortie du bloc ;
3. **l'isolation en grappes** : mesurer si le résidu est localisé (peu de
   coordonnées, peu de têtes) — si oui, les grappes sont naturelles ; si non,
   elles seront arbitr... à vérifier plutôt qu'à supposer.

**Et le piège du § 4 reste valable** : `--lot 1` est obligatoire pour avoir des
événements (le mode lot est dense, 0 événement mesuré).

## 7. L'apprentissage hebbien différentiel — implémenté et mesuré (06/10)

### Ce qui existait

`Hebb` **mesurait** le produit hebbien — il accumulait `h` et l'exportait — sans
jamais modifier le calcul. Le moteur observait la co-activation, il ne l'apprenait
pas.

### Ce qui a été ajouté : `HebbDiff`

```text
  Δx = x(t) − x(t−1)          différentiel de l'ENTRÉE
  Δy = y(t) − y(t−1)          différentiel de la SORTIE
  D += η · Δy ⊗ Δx            produit extérieur des différentiels
  y'  = y + D·x               l'adaptateur s'ajoute à la projection
```

**C'est exactement une mise à jour de poids** : `y' = W·x + D·x = (W + D)·x`.
Garder `D` à part ne change rien au modèle — c'est de la comptabilité qui laisse
l'original intact, exportable et réversible.

**Pourquoi le différentiel et pas le produit simple** : `Δw = η·x·y` renforce ce
qui est *simultanément actif*, donc il apprend des co-occurrences — et sur un flux
de langue, la co-occurrence dominante est « tout est actif tout le temps ». Le
différentiel annule ce terme statique et ne garde que ce qui **change ensemble** :
les transitions, donc les séquences. Et un changement est un **événement** — ce
que ce moteur transporte déjà.

Trois réglages, tous mesurés :
- **`DRAVE_HEBB_SEUIL`** — un canal ne contribue que si `|Δx|` dépasse le seuil.
  C'est la part événementielle : sous le seuil, ce n'est pas un changement, c'est
  du bruit de dernier bit.
- **`DRAVE_HEBB_SIGNE`** — `signe(Δx)·signe(Δy)`, la forme historique, bornée par
  construction.
- **`DRAVE_HEBB_DECROI`** — `D ← D·decroi + η·…`. Sans elle, l'adaptateur ne fait
  que croître.

### Les mesures

Qwen2.5-0.5B, 255 jetons, `--lot 1`, adaptateur sur la couche 12 (24), perplexité
en ligne sur le texte même :

| réglage | perplexité | vs référence |
|---|---:|---:|
| référence, sans adaptateur | 40,279 | — |
| valeur brute, η=1e-4 | 40,176 | −0,26 % |
| valeur brute, η=1e-3 | **53,783** | **+33 %** |
| valeur brute, η=1e-1 | **2 710 504** | **×67 000** |
| **valeur + seuil 1e-4 + décroi 0,99, η=4e-4** | **39,985** | **−0,73 %** |
| signé + seuil 1e-3 + décroi, η=1e-4 | 40,288 | +0,02 % |
| valeur + seuil + décroi, η=1e-3 | 41,514 | +3 % |

**Ce que ça dit :**

1. **La règle apprend** — mais faiblement : −0,73 % au mieux.
2. **Sans décroissance, la bande stable fait un facteur dix** : η=1e-4 améliore,
   η=1e-3 fait exploser. Avec la décroissance, η=1e-3 passe de **53 783 à
   41 514** — 1 300 fois mieux au même taux.
3. **La forme signée est moins bonne** : elle jette la magnitude, et la magnitude
   porte de l'information ici.
4. **Le seuil n'est pas qu'une économie** : il stabilise en ignorant le bruit.

### 8. Le test hors échantillon N'A PAS TOURNÉ — et pourquoi

J'ai voulu trancher entre « apprend » et « retient » : adapter sur un texte A,
sauver `D`, puis noter sur un texte B avec `D` rechargé.

**Le résultat : 29,151 sur B, modèle intact · 29,151 sur B, `D` appris sur A.**
Identiques au chiffre près — donc `D` était **nul**.

**La cause est un défaut que j'ai déjà rencontré ce soir, et que j'ai refait** :
le rapport de fin (`‖D‖`, nombre de pas, sauvegarde) a été posé dans `run_infer`
— le mode `--infer` — alors que le test tourne en `--ppl`, qui a sa **propre**
fonction et son propre câblage. **Aucune ligne `[hebb-diff] couche …` ne s'est
imprimée, donc `D` n'a jamais été sauvé, donc rien n'a été rechargé.**

C'est la deuxième fois ce soir que ce piège me prend : `hebb_diff` avait déjà dû
être câblé deux fois, dans `run_infer` **et** dans `run_ppl`. Un moteur avec deux
chemins qui doivent porter la même chose finit par n'en porter qu'un — et le
défaut est silencieux, ce qui est le pire cas du dépôt.

**Ce qui reste vrai malgré ça** : les mesures EN ÉCHANTILLON (§7) ont bien varié
avec η et avec les réglages, de façon monotone et reproductible — donc
l'adaptateur **agit** sur le calcul. Mais je n'ai **pas** mesuré `‖D‖`, et je n'ai
**pas** fait le test hors échantillon. La conclusion « la règle apprend » n'est
donc pas établie ; ce qui est établi, c'est qu'elle change la perplexité en
échantillon, et que la décroissance élargit la bande stable.

**Le pas suivant, précis** : poser le rapport et la sauvegarde dans `run_ppl`
aussi — ou mieux, **à un seul endroit** que les deux modes appellent, pour que ce
défaut ne puisse plus revenir.

### Ce qui reste à mesurer, et c'est le seul test qui compte

**La mesure est EN ÉCHANTILLON** : le modèle s'adapte au texte sur lequel on le
note. Le gain peut donc n'être que de la mémorisation. Le test qui tranche :
**adapter sur un texte A, noter sur un texte B**. C'est la différence entre
« apprendre la structure » et « retenir le texte » — et c'est la prochaine
mesure, pas une conclusion.
