# N3.3a — le routage/k-WTA du natif est vivant

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ✅ **N3.3a tenu** — deux
> DRVM de **mêmes poids** et de routages différents (`top_k=2/kwta=0,5` contre
> `top_k=1/kwta=1,0`) donnent des générations **différentes** ; le même modèle deux fois donne
> la même. Le routage agit dans le moteur natif.
>
> **Dispositif** : `tools/porte-n3-routes.sh`, petit `drave-n0` synthétique (graine 7,
> 113 292 paramètres), `--drvm-generate` ; données [`n3.3a-routes.json`](n3.3a-routes.json).

## Ce qui est mesuré

| contrôle | résultat |
|---|---|
| A (`top_k=2`, `kwta=0,5`), deux fois | **identique** (27 octets) |
| A contre B (`top_k=1`, `kwta=1,0`) | **différent** |
| paramètres A / B | **113 292 / 113 292** (mêmes poids) |

Les deux modèles partagent la **même graine** et le même `state_dict` ; seule la configuration
de routage change. La différence de sortie est donc **causée par le routage**, pas par les poids.

## Le contrôle négatif

- **Même modèle deux fois** : identique — la génération n’est pas un tirage.
- **Config différente** : sortie différente — si `top_k`/`kwta` ne faisaient rien, la porte
  échouerait.
- **Mêmes paramètres** : le nombre de paramètres est identique, donc la différence ne vient pas
  d’une capacité différente.

## Ce qui pourrait le rendre faux

- **Modèle synthétique** : la porte prouve que le routage **agit**, pas qu’il est **juste**.
- **Une seule graine, un prompt** : la sensibilité peut varier.
- **`kwta` et `top_k` changent ensemble** : la porte ne sépare pas les deux effets.
- **Pas de mesure de sparsité** : N3.3b doit vérifier le nombre d’experts retenus.

## Ce que ça change

N3.3a est **fait**. N3 reste **partielle** : N3.3b (finesse de la sparsité/top-k), N3.2b
(sortie précoce en service), puis la porte de composition. La porte N3.2a (service) et N3.3a
(routage) sont vertes.

## Fichiers

- `tools/porte-n3-routes.sh` — la porte.
- `reports/n3.3a-routes.json` — les mesures.
- `reports/rapport-n3.3a-routes.md` — cette fiche.
