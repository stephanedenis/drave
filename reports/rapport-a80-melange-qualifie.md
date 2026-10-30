# A8.0 — `porte-melange` : la rouge est qualifiée, pas maquillée

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ⛔ **rouge structurelle
> confirmée** — le mélange d'états ne peut pas être mesuré sur ce montage : l'état de A ne rend
> pas le code de A dans une invite qui n'en contient aucun. La porte échoue au **contrôle de
> calibration**, pas sur un chiffre.
>
> **Dispositif** : `tools/porte-melange.sh`, Qwen2.5-0.5B Q8_0, trois invites A/B/C (1470,
> 1470, 1440 jetons), capture d'état à la position 1470 ; données
> [`a80-melange-qualifie.json`](a80-melange-qualifie.json).

## Ce qui est mesuré

| élément | valeur |
|---|---|
| jetons A / B | **1470 / 1470** |
| jetons C (A sans aiguille) | **1440** |
| capture | position **1470** d'une invite de 1471 |
| contrôle de calibration | **échec** : l'état de A ne rend pas le code de A |

La porte **exit 1** : le mélange ne pourrait rien dire, car le témoin de calibration ne porte
pas le contenu qu'il prétend.

## Le contrôle négatif

- **Trois invites** A (code ZQ), B (code KJ), C (aucun code) ; A et B de même longueur, C sans
  l'aiguille.
- **Calibration** : avant de mélanger, l'état de A doit rendre le code de A dans C — il ne le
  fait pas.
- **La porte refuse** au lieu de produire un chiffre non interprétable.

## Ce qui pourrait le rendre faux

- **Un seul modèle** ; le défaut est dans le **montage** (position/capture), pas dans le mélange.
- **La porte n'est pas corrigée** : la qualification ne dit pas que le mélange est mauvais, elle
  dit qu'il n'est **pas mesurable ici**.
- **Aucun pin PPL** : une rouge ne s'épingle pas.
- **Pas de diagnostic du cache/état** au-delà du contrôle.

## Ce que ça change

A8.0 garde **18 portes PPL épinglées** ; `porte-melange` reste **rouge structurelle qualifiée**.
`porte-indice` (895 s) reste la seconde rouge. Aucune des deux n'est maquillée en vert.

## Fichiers

- `reports/a80-melange-qualifie.json` — les mesures.
- `reports/rapport-a80-melange-qualifie.md` — cette fiche.
