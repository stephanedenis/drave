# N4 — le banc de génération du 100 M : la répétition tombe de 9 à 6, la composition ne vient pas

> **Ligne de roadmap** : **N4** (l'usage du natif) · **Date** : 2026-11-17 · **Verdict** : à
> réglages **appariés** (20 prompts, 64 octets, GPU), le 100 M **ne gagne pas** en mots valides
> (0,882 contre 0,884) mais **réduit la répétition** (6 contre 9) ; il gagne en top-40 (**+0,069**)
> et perd en top-20 (**−0,088**). Le contrôle aléatoire (0,366 / 0,337 / 0,329) **discrimine** le
> modèle du bruit.
>
> **Dispositif** : [`tools/banc_generation.py`](../tools/banc_generation.py) `--n 64 --device cuda` ·
> `work/n2ac/mix1024-60k.pt` (**34,3 M**) contre `work/n2ac/mix1024-100m.pt` (**100 M**) · les
> **20 prompts** fixes du banc · données `banc-generation-100m.json`,
> `banc-generation-34m-64o.json`, `banc-generation-alea-64o.json`.

## Les résultats (mêmes réglages, même banc)

| modèle | réglage | mots valides | distinct-2 | répétition | octets/s |
|---|---|---:|---:|---:|---:|
| **34 M** | greedy | **0,884** | 0,790 | **9** | 129,5 |
| **100 M** | greedy | **0,882** | 0,753 | **6** | 124,4 |
| 34 M | top-40 / 0,8 | 0,518 | 1,000 | 1 | 125,5 |
| 100 M | top-40 / 0,8 | **0,587** | 0,997 | 1 | 122,3 |
| 34 M | top-20 / 0,5 | **0,741** | 0,990 | 1 | 126,2 |
| 100 M | top-20 / 0,5 | 0,653 | 0,986 | 2 | 123,4 |
| **aléatoire 34 M** | greedy | **0,366** | 1,000 | 1 | 48,4 |
| aléatoire 34 M | top-40 | 0,337 | 1,000 | 1 | 50,7 |
| aléatoire 34 M | top-20 | 0,329 | 1,000 | 1 | 53,6 |

## Lecture

1. **Le vocabulaire est saturé dès 34 M** : 0,884 contre 0,882 en greedy — l'échelle ×3 n'achète
   rien sur les mots réels.
2. **La répétition baisse** (9 → 6) : le 100 M boucle moins, mais **boucle encore** — la composition
   n'est pas venue avec l'échelle.
3. **Le compromis se déplace** : top-40 gagne +0,069, top-20 perd −0,088. La distribution a changé,
   pas la capacité de composer.
4. **Le débit** (129 contre 124 octets/s) est un effet du **GPU** (`--device`), pas du modèle : sur
   CPU, les deux tournaient à ~36 octets/s.

## Les contrôles

- **Aléatoire (même architecture, poids au hasard)** : 0,366 / 0,337 / 0,329 — stable d'un réglage à
  l'autre, et loin du modèle (0,88). Le banc mesure bien le modèle, pas le format des prompts.
- **Appariement** : même liste de 20 prompts, même longueur (64 octets), même vocabulaire de
  50 000 formes, même carte — la seule variable est le modèle.
- **Cohérence avec la fiche du 34 M à 128 octets** (0,870 greedy, répétition **15**) : la boucle
  grandit avec la longueur (9 à 64 octets, 15 à 128), ce qui est attendu.

## Ce qui pourrait le rendre faux

- **20 prompts, 64 octets, une graine** : le banc est petit ; un autre jeu de prompts peut déplacer
  les chiffres.
- **Le contrôle aléatoire est celui du 34 M** : le 100 M aléatoire n'a pas été mesuré ici.
- **Les deux modèles ne diffèrent pas que par la taille** : données et étapes d'entraînement peuvent
  différer ; l'attribution au seul paramètre « échelle » n'est pas prouvée.
- **Les métriques sont lexicales** (mots valides, distinct-2, répétition) : elles ne disent rien de la
  grammaticalité ni du sens.

## Ce que ça change

Le palier **100 M n'est pas un changement de régime** : il réduit la boucle et déplace le compromis,
il ne fait pas composer. Le prochain levier est donc la **donnée et l'alignement**, pas la taille —
ce que le plan natif suppose déjà (« l'échelle achète le vocabulaire, pas la composition »), et ce
que le palier 300–600 M devra réfuter ou confirmer.

## Voir aussi

- [le banc](../tools/banc_generation.py) · [la fiche du 34 M](rapport-banc-generation.md) ·
  [le plan natif](../docs/pilotage/natif-plan.md) · les données : [100 M](banc-generation-100m.json),
  [34 M apparié](banc-generation-34m-64o.json), [aléatoire](banc-generation-alea-64o.json)
