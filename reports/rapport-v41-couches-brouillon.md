> Campagne : M5 — le brouillon est-il **dans le fichier** ? · expérience 01
> Question : le GGUF de V4.1 (et celui de K3) porte-t-il les **poids** d'une couche de brouillon, donc un décodage spéculatif **sans second modèle** ?
> Verdict : **OUI pour V4.1** — le fichier **déclare** 3 couches (`num_nextn_predict_layers = 3`, `dspark_target_layer_ids = [37, 38, 39]`) et **porte 75 tenseurs** pour ces trois couches (**41 263 M poids**) ; **NON pour K3** — 64 clés de métadonnées, **aucune** `mtp` / `nextn` / `dspark`, aucune config embarquée.
> Date réelle : 2026-10-12 08:57 HAE (heure lue sur la machine ; source : ce fichier, ajouté par le commit qui le porte)

# V4.1 — les couches du brouillon sont dans le fichier

**Pourquoi cette fiche.** `docs/strata-pour-drave.md` § 1 (S1) propose de rouvrir **M5** en changeant
son cahier des charges : le brouillon ne serait pas un second modèle, mais **une couche de la cible** —
comme Strata, dont la couche MTP est lue dans le même GGUF. Le premier pas ne demandait **aucune
modification du moteur** : il suffisait de lire les métadonnées et l'inventaire du fichier.

## Protocole, pour rejouer

```bash
M=/home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf
python3 tools/lire_meta_gguf.py "$M" deepseek41.config     # la config embarquée (JSON)
./drave-core/target/release/drave "$M" --tensors           # l'inventaire, en-têtes seuls
K=/home/stephane/Data13TB/stephane/modeles/gguf/Kimi-K3-UD-Q4_K_XL/Kimi-K3-UD-Q4_K_XL-00001-of-00032.gguf
python3 tools/lire_meta_gguf.py "$K"                        # toutes les clés
```

**Piège payé ici** : les clés `dspark_*` ne sont **pas** des clés de premier niveau — elles vivent
**dans la valeur** de `deepseek41.config` (le `config.json` d'origine, stocké comme chaîne). Chercher
`dspark` parmi les noms de clés ne rend **rien** et laisse croire à une absence. C'est la deuxième
fois que ce dépôt paie « un silence n'est une mesure que si l'on a vérifié » : ici, la vérification
est de **lire la valeur**, pas la liste des noms.

## Mesures

**V4.1** — `deepseek41`, **1 046 tenseurs**, **365,70 Go** de poids, en-têtes lus en **66,2 ms**
(`--tensors`) et **66,6 ms** (second appel). Config embarquée (`deepseek41.config`) :

| clé | valeur |
|---|---|
| `num_nextn_predict_layers` | **3** |
| `dspark_target_layer_ids` | **[37, 38, 39]** |
| `dspark_n_routed_experts` | 128 |
| `dspark_num_experts_per_tok` | **3** |
| `dspark_block_size` | 5 |
| `dspark_markov_rank` | 256 |
| `dspark_noise_token_id` | 128799 |

Présence dans le fichier — les trois couches existent, **25 tenseurs chacune** :

| couche | tenseurs | poids |
|---|---:|---:|
| `blk.37` | 25 | — |
| `blk.38` | 25 | — |
| `blk.39` | 25 | — |
| **total 37-39** | **75** | **41 263 M poids** |

Dernière couche du modèle : **`blk.39`** ; les 37 premières (`blk.0` … `blk.36`) portent la même
structure (`hc_attn_*`, `attn_q_a/q_b`, `attn_kv`, `indexer.*`, `ffn_*_exps` en IQ2_XXS, `ffn_*_shexp`
en Q8_0). Aucun tenseur de tête MTP à la DeepSeek-V3 (`eh_proj`, `enorm`, `hnorm`, `shared_head`) :
la mécanique `dspark` n'est **pas** la tête MTP classique.

**K3** — shard 1/32 : **64 clés distinctes**, toutes `general.*` ou `kimi-k3.*`
(`kimi-k3.block_count`, `kimi-k3.attention.*`, `kimi-k3.attn_res.block_size`…) ; **aucune** clé
`mtp` / `nextn` / `dspark`, et **aucune** clé `*.config` (il n'y a donc pas de JSON embarqué à
fouiller). Cela **confirme** `docs/roadmap-drave.md` axe 2 (« K3 n'a pas de couche MTP vérifiée ») :
ce n'était pas un silence, c'est une absence vérifiée sur les 64 clés.

## Verdict

**V4.1 porte son brouillon dans son propre fichier.** Le prérequis de M5 n'est donc pas « trouver ou
entraîner un petit modèle » : c'est **exécuter les couches 37-39** et mesurer leur taux d'acceptation.
K3, lui, reste sans brouillon — pour cette cible, M5 garde son cahier des charges d'origine
(brouillon externe : `eagle3-gpt-oss-120b-Q8_0.gguf` est sur le disque, 849 Mo).

## Ce que cette fiche ne dit pas (et qui reste à mesurer)

- **Que les couches 37-39 *servent* de brouillon** : la config les nomme comme cibles et
  `num_nextn_predict_layers = 3` les compte — c'est une **déduction des clés**, pas une exécution.
  Le moteur ne les a jamais fait tourner.
- **Leur coût en octets** : 41 263 M poids est la **somme des comptes de l'inventaire**, pas une
  mesure d'octets sur le disque (le fichier est en IQ2_XXS pour les experts, Q8_0/F16/F32 ailleurs).
- **Le taux d'acceptation** : c'est la seule mesure qui décide si M5 paie — et elle exige la porte
  (jetons gourmands **identiques** au chemin sans brouillon, puis acceptation par type de tâche).

## Suite

1. écrire la porte de M5 : invariants (sortie identique) **et** taux d'acceptation, vue **rouge**
   avec un brouillon volontairement désaligné ;
2. `docs/strata-pour-drave.md` § 1 (S1) et § 4 sont mis à jour avec ce verdict.
