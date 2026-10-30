# N3.4b — le pont natif agit dans la génération

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ✅ **N3.4b tenu** — deux
> DRVM de **mêmes poids** (graine 7, 428 504 paramètres, 4 blocs) ne diffèrent que par le pont :
> B a `bridge.weight` et `bridge.bias` mis à zéro (**4 160** poids). A est déterministe ; B rend
> une génération **différente**. Le pont est branché.
>
> **Dispositif** : `tools/porte-n3-pont.sh`, `--drvm-generate` ; données
> [`n3.4b-pont.json`](n3.4b-pont.json).

## Ce qui est mesuré

| contrôle | résultat |
|---|---|
| A deux fois | **identique** (35 octets) |
| A contre B (pont nul) | **différent** |
| poids du pont neutralisés | **4 160** |
| paramètres A / B | **428 504 / 428 504** |

Le pont du modèle natif est appliqué au milieu de la pile ; le neutraliser change la
génération. C’est la brique « pont » de N3 **dans le moteur**, pas le lien distribué de
`porte-pont` (Qwen).

## Le contrôle négatif

- **A deux fois** : identique — la génération n’est pas un tirage.
- **Pont nul** : sortie différente — le pont agit.
- **Mêmes paramètres** : la différence ne vient pas d’une capacité différente.

## Ce qui pourrait le rendre faux

- **Pont du modèle natif**, pas le lien réseau distribué : ce sont deux « ponts » différents.
- **Pas de placement** dans cette porte : N3.4c reste.
- **Modèle synthétique**, un prompt, une graine.
- **Le pont nul n’est pas une ablation de qualité** : il prouve l’activité, pas l’utilité.

## Ce que ça change

N3.4b est **fait**. La composition N3 couvre maintenant service, profondeur, routage, comptage
et **pont**. Le **placement** (N3.4c) et une composition complète restent.

## Fichiers

- `tools/porte-n3-pont.sh` — la porte.
- `reports/n3.4b-pont.json` — les mesures.
- `reports/rapport-n3.4b-pont.md` — cette fiche.
