# N3.2a — le service natif répond, et il est déterministe

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ✅ **N3.2a tenu** — le
> service `--drvm-serve` démarre sur un DRVM **reproductible**, `/sante` rend le bon nombre de
> paramètres, deux générations du même prompt sont identiques, un autre prompt diffère, et un
> chemin inconnu rend **404**. N3.2 (sortie précoce en service) reste ouvert.
>
> **Dispositif** : `tools/porte-n3-service.sh` ; petit `drave-n0` synthétique (graine 7,
> 1 bloc, 4 experts top-2, kwta 0,5, vocab 256, **113 292** paramètres) exporté en DRVM ;
> service Rust `--drvm-serve` ; données [`n3.2a-service.json`](n3.2a-service.json).

## Ce qui est mesuré

| contrôle | résultat |
|---|---|
| `/sante` | **113 292** paramètres, identiques au modèle |
| génération « abc » × 2 | **11 octets**, textes identiques |
| génération « zzz » | 11 octets, texte **différent** |
| `/inconnu` | **404** |

Le service est **vivant**, **déterministe** et **refuse** les chemins inconnus. Le modèle
synthétique est régénérable par la porte (graine fixe), donc la mesure ne dépend pas d’un
fichier `/tmp`.

## Le contrôle négatif

- **Même prompt deux fois** : identique — la génération n’est pas un tirage.
- **Autre prompt** : différent — le service lit bien l’entrée.
- **404** : un refus, pas une génération silencieuse.
- **`/sante`** : le nombre de paramètres est celui du modèle, pas une constante.

## Ce qui pourrait le rendre faux

- **Modèle synthétique** : la porte teste le **service**, pas la qualité du natif.
- **Pas de sortie précoce, de pont ni de rejeu** dans ce service : N3.2b et N3.3 restent.
- **Pas d’auth, pas de cache KV** : le service est minimal, comme le dit `serveur_natif.py`.
- **Un seul prompt** de chaque sorte ; la parité avec Python n’est pas mesurée ici.

## Ce que ça change

N3.2a est **fait** : le chemin de service natif existe, il est gardé. N3 reste **partielle** :
N3.2b (sortie précoce en service), N3.3 (porte `k-WTA/routes`), puis la porte de composition.

## Fichiers

- `tools/porte-n3-service.sh` — la porte.
- `reports/n3.2a-service.json` — les mesures.
- `reports/rapport-n3.2a-service.md` — cette fiche.
