# N3.4d — la couverture N3 par brique est complète, la composition native reste conditionnelle

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ✅ **couverture par brique**
> — chaque opération native a une porte verte ou une condition nommée. ⛔ **composition native
> unique** avec placement : impossible sans un chemin distribué natif qui n’existe pas.
>
> **Dispositif** : synthèse des fiches et portes, aucun nouveau run ; données
> [`n3.4d-couverture.json`](n3.4d-couverture.json).

## La couverture

| brique | porte(s) | état |
|---|---|---|
| k-WTA / routes | N3.3a, N3.3b, N3.3c | ✅ |
| sortie précoce | N3.2b0, N3.2b1, N3.2b2 | ✅ / condition K/V |
| pont | N3.4b, `porte-pont` | ✅ |
| rejeu | `porte-trace` | ✅ |
| placement | `porte-topologie` (GGUF), N3.4c (natif) | ✅ / condition métadonnée |
| service | N3.2a | ✅ |
| composition | N3.4a | ✅ |

## La condition

Une **composition native unique** qui inclurait le placement demanderait un chemin distribué
natif : le service natif lit l’architecture, pas `execution.placement` (N3.4c). Ce n’est pas une
porte manquante, c’est une **architecture absente**, nommée.

## Le contrôle négatif

- **Aucune brique n’est supposée** : chacune a une porte (verte) ou une condition mesurée.
- **La composition N3.4a** est une exécution réelle, pas une liste de portes.
- **Le placement natif** est prouvé inerte par N3.4c, avec un contrôle pont nul qui, lui, change.

## Ce qui pourrait le rendre faux

- **Synthèse, pas une nouvelle mesure** : les chiffres sont dans les fiches liées.
- **Le placement natif** reste une métadonnée ; la couverture GGUF ne vaut pas pour le natif.
- **Une composition complète** reste impossible ; le dire est le résultat.

## Ce que ça change

N3 est **couvert par brique**. La composition native complète reste une **condition
d’architecture**, pas une ligne ouverte ordinaire. A8.0 reste à 14/33 ; A8.3 est opt-in ; R13.1
est une condition nommée.

## Fichiers

- `reports/n3.4d-couverture.json` — la couverture.
- `reports/rapport-n3.4d-couverture.md` — cette fiche.
