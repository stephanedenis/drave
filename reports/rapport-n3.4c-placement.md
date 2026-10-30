# N3.4c — le placement natif est une métadonnée, pas un chemin distribué

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ⛔ **condition nommée** —
> deux DRVM de mêmes poids, l’un `placement=local`, l’autre `placement=remote`, donnent la
> **même génération** : le service natif lit l’architecture, pas le placement. Le contrôle
> (pont nul) change bien la sortie, donc la porte détecte un vrai changement.
>
> **Dispositif** : `tools/porte-n3-placement.sh`, modèle 4 blocs (graine 7, 428 504 paramètres),
> `exporter_drvm(..., placement=...)` ; données [`n3.4c-placement.json`](n3.4c-placement.json).

## Ce qui est mesuré

| contrôle | résultat |
|---|---|
| A (`local`) deux fois | **identique** (35 octets) |
| A contre B (`remote`) | **identique** |
| A contre C (pont nul) | **différent** |
| paramètres | **428 504** |

Le placement ne change **rien** ; le pont nul, lui, change la sortie. Le champ est donc une
**métadonnée inerte** dans le service natif.

## Le contrôle négatif

- **A deux fois** : identique — pas de tirage.
- **Local contre remote** : identique — le placement est inerte.
- **Pont nul** : différent — la porte détecte un vrai changement ; elle ne dit pas « tout est
  identique » par construction.

## Ce qui pourrait le rendre faux

- **Champ de manifeste**, pas une exécution distribuée : le test ne prouve pas l’absence de tout
  chemin, seulement que ce champ n’en active aucun.
- **Le placement distribué du moteur GGUF** est couvert par `porte-topologie` ; ce n’est pas le
  natif.
- **Modèle synthétique**, un prompt ; pas de réseau.

## Ce que ça change

N3.4c est **nommé** : le placement natif n’existe pas comme chemin d’exécution. La brique
« placement » est couverte pour le moteur GGUF (`porte-topologie`) ; une composition **native**
avec placement demanderait un chemin distribué qui n’existe pas. N3 reste **partielle** sur ce
point ; les autres briques sont couvertes.

## Fichiers

- `tools/native_model.py` — `exporter_drvm(..., placement=...)`.
- `tools/porte-n3-placement.sh` — la porte.
- `reports/n3.4c-placement.json` — les mesures.
- `reports/rapport-n3.4c-placement.md` — cette fiche.
