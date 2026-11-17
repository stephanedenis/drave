# N3.7 — les variantes d'implémentation sont un contrat

> **Ligne de roadmap** : N3 · **Date** : 2026-11-17 · **Verdict** : ✅ **N3.7 tenu** — deux
> implémentations de la **même fonction** sont **indifférentes** dans la tolérance déclarée par le
> manifeste (**4,768e-07** ≤ 1e-4) ; une implémentation d'une **autre fonction** sous la même
> signature **échoue** ce test (**5,790e-03** > 1e-4) — c'est le contrôle négatif qui rend le test
> non vide.
>
> **Dispositif** : [`tools/porte-n3-variante.sh`](../tools/porte-n3-variante.sh) · petit `drave-n0`
> (**132 720 paramètres**, `d_model` 32, 2 blocs, graine 7, mêmes poids) exporté **trois fois** avec
> `impl` = `defaut`, `bloque`, `flou` et le même contrat ; logits du dernier pas par
> `--drvm-pas-hex`.

## Ce qui est mesuré

| contrôle | résultat |
|---|---|
| `defaut` vs `bloque` — même fonction, somme tuilée sur 4 accumulateurs | **4,768e-07** ≤ 1e-4 → **indifférent** |
| `defaut` vs `flou` — seuil net du k-WTA → appartenance sigmoïde | **5,790e-03** > 1e-4 → **non indifférent** |
| coût, 2 048 octets, médiane de 7 passes | **~86 ms** pour les deux profils (**0,98–0,99×**, deux passes) |
| provenance | `--drvm-inspect` et la trace portent `impl=bloque`, `tol=1e-4` |
| moteur numpy | `defaut` et `bloque` **exécutés** (**2,831e-07**) ; `flou` **refusé** (nommé) |
| `impl` inconnue | refusée à l'écriture, donc absente du disque |

## Les deux choses que la porte sépare

1. **Substitution** — même fonction, autre algorithme : indifférence **dans le contrat**. C'est le
   théorème d'indifférence (`docs/theorie/modele-natif.md`) mesuré sur des logits, pas sur une
   intention.
2. **Routage** — autre fonction, même signature : la substitution est **interdite**, et le test doit
   le dire. `flou` est un candidat au **routage**, pas un remplaçant.

## Le contrôle négatif

- `flou` **doit** échouer l'indifférence : s'il passait, le test ne testerait rien ;
- une `impl` inconnue est refusée à l'écriture **et** à la lecture, par les deux lecteurs
  (`porte-n3-refus`) ;
- le moteur numpy **refuse** au lieu d'exécuter autre chose : sans ce refus, un manifeste `bloque`
  rendrait des logits qui ne sont ceux d'aucune implémentation déclarée.

## Ce qui pourrait le rendre faux

- **Une graine, un modèle, un pas** : la tolérance 4,768e-07 est celle de ce modèle ; elle grandit
  avec `d_model` et le nombre de blocs. Le contrat est **déclaré par modèle**, pas universel.
- **`bloque` n'est pas plus rapide ici** (0,98–0,99×) : le tuilage paie quand la matrice est grande, pas
  sur 32×32. La porte imprime le rapport, elle ne promet pas un gain.
- **Le coût inclut le démarrage du processus** (~5 ms) : sur 2 048 octets il pèse peu, mais ce n'est
  pas un banc de noyau.
- **`flou` est une différence *conçue***, pas une expérience de routage : « faut-il router vers
  `flou` ? » est la question de R0.5/R06, et leur réponse est négative pour un seuil global.

## Ce que ça change

Le format DRVM accepte `impl` (profil **public**) et `contrat {version, tolerance}` sur un bloc
`local_mixer` ; le nom entre dans le manifeste, donc dans le hash, donc dans la trace. Les deux
moteurs **refusent** ce qu'ils n'exécutent pas. La prochaine étape est le **routage**
(`graph.routes`), avec la leçon de R0.5 : un seuil global ne transfère pas, il faut une calibration
par document.

## Voir aussi

- [la porte](../tools/porte-n3-variante.sh) · [le format](../tools/drvm.py) ·
  [le moteur natif](../drave-core/src/native.rs) · [le modèle natif](../docs/theorie/modele-natif.md)
