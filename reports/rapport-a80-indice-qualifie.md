# A8.0 — `porte-indice` : rouge structurelle qualifiée

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ⛔ **rouge confirmée** —
> l’indice **extérieur** tombe à **482** jetons de l’aiguille, le témoin à **459** : l’écart est
> nul ou négatif, rien n’est établi sur ce texte. La porte refuse au lieu de conclure.
>
> **Dispositif** : `tools/porte-indice.sh`, Qwen2.5-0.5B Q8_0, invites A/B (1470/1440 jetons,
> aiguille au jeton 669) ; données [`a80-indice-qualifie.json`](a80-indice-qualifie.json).

## Ce qui est mesuré

| élément | valeur |
|---|---|
| invites A / B | 1470 / 1440 jetons |
| aiguille | jeton **669** |
| écho interne | **64/64** (ne prouve rien) |
| indice extérieur | **482** jetons |
| témoin | **459** jetons |
| hasard | 370 jetons |

La porte **exit 1** : l’indice extérieur est au niveau du témoin ; l’écho interne parfait est un
piège (il retrouve ce qu’on lui donne).

## Le contrôle négatif

- **Indice interne** : 64/64, mais la porte exige un **indice extérieur**.
- **Indice extérieur** : 482, témoin 459 — écart nul/négatif.
- **Hasard** : 370 ; aucun des deux ne s’en détache.
- **La porte refuse** : pas de pin PPL, pas de conclusion.

## Ce qui pourrait le rendre faux

- **Un seul modèle**, un texte.
- **Mémoire par contenu, pas sémantique** : c’est la limite mesurée, pas un bug.
- **La porte n’est pas corrigée** : elle est qualifiée.
- **Aucun pin** : une rouge ne s’épingle pas.

## Ce que ça change

A8.0 garde **18 portes PPL épinglées**. Les rouges sont maintenant **qualifiées** : pannes
(corrigée), mélange (calibration), indice (extérieur au niveau du témoin).

## Fichiers

- `reports/a80-indice-qualifie.json` — les mesures.
- `reports/rapport-a80-indice-qualifie.md` — cette fiche.
