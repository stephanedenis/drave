# A8.0 — `porte-flux` épingle ses PPL : 61,9920 / 60,8135

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **première porte
> épinglée** — `porte-flux` vérifie maintenant la **PPL absolue** de ses cinq modes, pas seulement
> l'écart entre deux nœuds. A8.0 reste **partielle** : 1 porte sur 33.
>
> **Dispositif** : `tools/porte-flux.sh`, Qwen2.5-0.5B Q8_0, 24 identifiants, 12 couches, ctx 64 ;
> références `61,9920` (modes 0/1/2) et `60,8135` (modes 3/4), tolérance **5e-4** ; données
> [`a80-porte-flux.json`](a80-porte-flux.json).

## La question

La porte vérifiait l’**écart** entre la référence locale et les deux nœuds, mais pas la **valeur**
de la référence : une régression globale de PPL passait. A8.0 demande d’épingler l’absolu.

## Ce qui est mesuré

| mode | PPL référence | PPL deux nœuds | écart | état |
|---|---:|---:|---:|---|
| 0 — f32 dense | **61,9920** | 61,9920 | 0,00e0 | ✅ |
| 1 — listes quantifiées | **61,9920** | 61,9920 | 0,00e0 | ✅ |
| 2 — listes par blocs | **61,9920** | 64,2535 | 3,65e-2 | ✅ |
| 3 — lot dense f32 | **60,8135** | 60,8135 | 0,00e0 | ✅ |
| 4 — lot en listes | **60,8135** | 60,5427 | 4,45e-3 | ✅ |

La porte **exit 0** avec le contrôle de référence actif. Les deux PPL de référence sont celles que
`historique-passes-portes.md` donnait déjà comme stables.

## Le contrôle négatif

La condition est numérique : `abs(ppl_ref - attendu) <= 5e-4 × attendu`. Avec la même expression,
une référence décalée de **10 %** (`61,9920` contre `68,1912`) est **refusée** — vérifié avant le
commit. Le contrôle porte sur la valeur, pas sur l’écart.

## Ce qui pourrait le rendre faux

- **Un seul modèle et une seule quantification** : les références sont liées à Qwen2.5-0.5B Q8_0.
- **Les modes avec perte** : la PPL à deux nœuds (64,2535 / 60,5427) n’est **pas** épinglée ; elle
  dépend du codec, et l’écart la borne. C’est volontaire.
- **Tolérance 5e-4** : elle attrape une dérive de 0,05 %, pas une dérive de 0,01 %.
- **Le gate n’a pas été rejoué sur une autre machine** : la PPL est déterministe sur ce build, pas
  nécessairement sur un autre.

## Ce que ça change

`porte-flux` est la **première** porte PPL épinglée ; A8.0 passe de **0/33** à **1/33**. La suivante
est `porte-pont` (références relatives **+2,81 % / +25,35 %** dans l’historique), puis les portes de
budget et de topologie. A8.3 reste **opt-in** tant que le lot n’est pas épinglé.

## Fichiers

- `tools/porte-flux.sh` — contrôle de référence PPL.
- `reports/a80-porte-flux.json` — les mesures.
- `reports/rapport-a80-porte-flux.md` — cette fiche.
