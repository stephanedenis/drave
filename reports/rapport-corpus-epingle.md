# N — le corpus d'entraînement est épinglé

> **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·
> **Verdict** : ✅ le corpus de `data/wiki_mix/propre` est **épinglé** — sha256 du train, du val et
> de leurs canaux, tailles, lignes, dates, empreinte du manifeste (`fae5bb73…`). Sans cette
> épingle, chaque perplexité est une rumeur : l'alerte du 16/11 a montré que le `ppl_val` 2,40
> annoncé **ne se reproduit pas** avec le `val.txt` actuel (17,3 à 22,6 selon le morceau lu).
>
> **Dispositif** : [`tools/epingle_corpus.py`](../tools/epingle_corpus.py) · le manifeste
> [`corpus-epingle.json`](corpus-epingle.json) · vérification `--verifie` (recalcule et compare).

## L'épingle

| fichier | sha256 | octets | lignes |
|---|---|---:|---:|
| `train.txt` | `0876b6089aaebb5d…` | 1 017 487 092 | 2 480 766 |
| `val.txt` | `fbddef918166f1d6…` | 10 330 112 | 24 498 |
| `train.canal` | `04efed3039f8398e…` | 1 017 487 092 | — (classes par octet) |
| `val.canal` | `f1abc5d1d63c3207…` | 10 330 112 | — |
| **manifeste** | `fae5bb7389c6c0a9…` | — | — |

Date des fichiers : **2026-11-02 12:25:22**. L'empreinte du manifeste est le sha256 du JSON
canonique des fichiers (sans les dates) : modifier une ligne du manifeste se voit.

## Le contrôle négatif

- **L'autotest** (`--autotest`) : un petit corpus est épinglé, **reconnu intact**, puis **un octet
  est changé** — et l'épingle le détecte (`5b1ce044…` ≠ `50632d79…`). Un vérificateur qui ne sait
  pas échouer ne vérifie rien.
- **`--verifie` sur le vrai corpus** : recalcule les quatre empreintes en 6,5 s et les compare au
  manifeste — c'est la commande à lancer avant toute campagne.

## Ce que ça ne prouve pas

- **L'identité, pas la propreté** : l'épingle certifie que le corpus est **le même**, pas qu'il est
  bon. Un corpus sale, épinglé, reste sale.
- **Pas de champ « version du nettoyage »** : la date, le mtime et le sha256 en tiennent lieu ; si
  le nettoyage change sans changer les octets, c'est le même corpus — et c'est correct.
- **Le manifeste peut mentir** s'il est édité à la main : c'est l'empreinte du manifeste qui le
  protège, et elle est committée.
- **Les 1 Go** : le pin couvre ce corpus-ci ; le palier 1 demande 3–6 Go — l'épingle devra être
  refaite (et datée) quand la donnée s'étendra.

## Ce que ça change

Le palier 1 du plan natif commence par « la donnée d'abord, et l'épingler » : c'est fait pour le
corpus actuel. Toute PPL désormais peut **nommer son corpus** (`fae5bb73…`) ; la « porte propre »
(0,29) et le prochain entraînement peuvent être comparés sans ambiguïté. Le prochain pas est
l'entraînement **plus long** sur ce corpus épinglé, avec le banc dès le premier checkpoint.

## Voir aussi

- [l'outil](../tools/epingle_corpus.py) · [le manifeste](corpus-epingle.json) ·
  [l'alerte de reproductibilité](rapport-native-reproductibilite.md) ·
  [le plan natif](../docs/pilotage/natif-plan.md)
