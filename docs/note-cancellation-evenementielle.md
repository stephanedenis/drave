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
