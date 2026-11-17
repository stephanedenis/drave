# N3.9 — les deux moteurs rendent le même corps

> **Ligne de roadmap** : N3 · **Date** : 2026-11-17 · **Verdict** : ✅ **N3.9 tenu** — le moteur
> **Rust** et le moteur **numpy**, sur le même manifeste, rendent les mêmes logits dans la tolérance
> déclarée : **3,576e-07** (`defaut`) et **2,384e-07** (`bloque`), pour une tolérance de **1e-4**.
> Le comparateur **voit** une différence réelle (**5,790e-03** pour `flou`), les deux moteurs sont
> déterministes, et le numpy **refuse** ce qu'il n'exécute pas.
>
> **Dispositif** : [`tools/porte-n3-moteurs.sh`](../tools/porte-n3-moteurs.sh) · petit `drave-n0`
> (**132 720 paramètres**, `d_model` 32, 2 blocs, graine 7) exporté trois fois (`defaut`, `bloque`,
> `flou`) ; logits du dernier pas par `--drvm-pas-hex` (Rust, cache KV) contre `logits()` (numpy,
> passe complète).

## Ce qui est mesuré

| contrôle | résultat |
|---|---|
| Rust vs numpy, profil `defaut` | **2,980e-07** ≤ 1e-4 |
| Rust vs numpy, profil `bloque` | **3,576e-07** ≤ 1e-4 |
| Rust vs numpy, profil `court` | **2,980e-07** ≤ 1e-4 |
| contrôle du comparateur : Rust `defaut` vs `flou` | **5,790e-03** > 1e-4 (il voit) |
| déterminisme, deux exécutions | identiques des deux côtés |
| moteur numpy sur `flou` | **refusé** (nommé) |

## Ce que la porte établit

Le « même modèle » n'est pas une intention : les deux moteurs — un avec cache KV en Rust, l'autre en
passe complète numpy — donnent le même vecteur de logits à 3,0–3,6e-07, soit **~30 fois sous la
tolérance déclarée**. Une substitution mesurée sur un moteur vaut donc pour l'autre, dans le
contrat. Et la parité n'est plus un chiffre de session : elle est **gardée** à chaque passe.

## Ce qui pourrait le rendre faux

- **Un modèle, une graine, une position** : la comparaison porte sur les logits de la dernière
  position d'un prompt de 128 octets,
  `drave-n0` synthétique ; elle ne prouve pas la parité sur un modèle entraîné (N4 l'a mesurée
  séparément, 4/4 en greedy).
- **Deux chemins différents** : Rust calcule avec un cache KV, numpy refait la passe — l'accord est
  donc aussi un contrôle du cache, mais il ne teste pas les positions intermédiaires.
- **f32 et BLAS** : l'écart résiduel vient de l'ordre des sommes ; il grandirait avec `d_model` et la
  profondeur. La tolérance est celle du manifeste, pas une constante universelle.
- **Le comparateur ne juge que le corps, pas le coût** : deux moteurs d'accord ne disent rien du
  temps ni de la mémoire.

## Ce que ça change

La parité DRVM ↔ numpy cesse d'être un résultat de session : c'est une **porte**. Toute modification
du moteur natif ou de `drvm_infere.py` qui casserait le contrat la fait rougir. C'est la condition
pratique du théorème d'indifférence : sans deux moteurs d'accord, « le même modèle sur deux supports »
reste une déclaration.

## Voir aussi

- [la porte](../tools/porte-n3-moteurs.sh) · [le moteur Rust](../drave-core/src/native.rs) ·
  [le moteur numpy](../tools/drvm_infere.py) · [la parité N4](rapport-natif-numpy.md)
