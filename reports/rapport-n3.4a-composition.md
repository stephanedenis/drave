# N3.4a — service, profondeur, routage et comptage composés sur les mêmes modèles

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ✅ **N3.4a tenu** — les
> briques déjà branchées (service N3.2a, profondeur N3.2b0, routage N3.3a, comptage N3.3c)
> tournent **ensemble** sur deux modèles de mêmes poids. Ce n’est pas encore la composition
> complète : le **seuil de confiance** (N3.2b) et le pont/placement n’y sont pas.
>
> **Dispositif** : `tools/porte-n3-composition.sh`, deux DRVM à 2 blocs (graine 7,
> 132 528 paramètres, `top_k=2` contre `top_k=1`), service `--drvm-serve`,
> `--drvm-sparsite` ; données [`n3.4a-composition.json`](n3.4a-composition.json).

## Ce qui est mesuré

| contrôle | résultat |
|---|---|
| `/sante` | **132 528** paramètres |
| A pleine × 2 | **identique** (15 octets) |
| A profondeur 1 × 2 | **identique** et **différent** de A |
| B (`top_k=1`) | **différent** de A |
| compteurs A | **6 appels · 12 experts · 96 canaux** |
| compteurs B | **6 appels · 6 experts · 48 canaux** |

Les quatre briques sont exercées dans le **même récit de mesure** : le service répond, la
profondeur change la génération, le routage change la génération, les compteurs comptent.

## Le contrôle négatif

- **A deux fois** : identique — pas de tirage.
- **Profondeur 1** : différente — la profondeur agit.
- **B** : différente — `top_k` agit.
- **Compteurs exacts** : `(6,12,96)` et `(6,6,48)` — le routage est compté, pas supposé.

## Ce qui pourrait le rendre faux

- **Profondeur fixe, pas de seuil** : N3.2b reste ouvert.
- **Pas de pont/placement** dans la même exécution : ce sont des portes séparées.
- **Modèle synthétique** : la composition est prouvée, pas la qualité.
- **Un prompt** ; une seule graine.

## Ce que ça change

N3.4a est **fait** : les briques branchées composent. N3 reste **partielle** :
N3.2b (seuil de confiance), puis l’entrée du pont/placement dans la composition.

## Fichiers

- `tools/porte-n3-composition.sh` — la porte.
- `reports/n3.4a-composition.json` — les mesures.
- `reports/rapport-n3.4a-composition.md` — cette fiche.
