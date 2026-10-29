# A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 %

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **deuxième porte
> épinglée** — `porte-pont` vérifie maintenant ses **PPL absolues** et les **deux côtés de la
> falaise**. A8.0 reste **partielle** : 2 portes sur 33.
>
> **Dispositif** : `tools/porte-pont.sh`, Qwen2.5-0.5B Q8_0, 48 identifiants, 12 couches, ctx 256 ;
> PPL de référence **113,0068** (dense) et **111,9225** (blocs), tolérance **5e-4** ; falaise
> **+2,81 %** à 448 fibres et **+25,35 %** à 392, tolérance **0,05 point** ; données
> [`a80-porte-pont.json`](a80-porte-pont.json).

## Ce qui est mesuré

| point | PPL | écart | état |
|---|---:|---:|---|
| dense sans pont | **113,0068** | — | ✅ |
| blocs sans pont (896) | **111,9225** | 0,000 % | ✅ |
| 672 fibres | 112,9891 | 0,953 % | ✅ |
| 448 fibres | 115,0632 | 2,806 % | ✅ |
| 224 fibres | 233,8589 | 108,947 % | ✅ |
| 112 fibres | 1153,3098 | 930,454 % | ✅ |

La falaise est verrouillée des deux côtés : **448 fibres +2,81 %**, **392 fibres +25,35 %**.
La porte **exit 0**, les contrôles de référence sont actifs.

## Le contrôle négatif

Les contrôles sont numériques : `abs(ppl - attendu) <= 5e-4 × attendu` et `abs(écart - attendu)
<= 0,05`. Avec la même expression, un décalage de **10 %** des quatre références est **refusé**
(vérifié avant le commit). Le contrôle porte sur la valeur, pas sur l’égalité entre bras.

## Ce qui pourrait le rendre faux

- **Un seul modèle et une seule quantification** : les PPL absolues sont liées à Qwen2.5-0.5B Q8_0
  et au corpus de 48 identifiants.
- **La falaise est un point mesuré**, pas une loi : 448/392 sont les bornes de la marche ; une
  autre architecture peut déplacer la marche.
- **Tolérance 5e-4 / 0,05 point** : attrape une dérive de 0,05 %, pas de 0,01 %.
- **Les modes avec perte** restent vérifiés par leur écart, pas par une PPL absolue.

## Ce que ça change

A8.0 passe de **1/33** à **2/33** portes épinglées. La suivante est `porte-budget` (PPL de deux
nœuds) ou `porte-topologie` (**42,5477** dans l’historique). A8.3 reste **opt-in** : deux portes ne
suffisent pas à couvrir les 33.

## Fichiers

- `tools/porte-pont.sh` — PPL de référence et falaise épinglées.
- `reports/a80-porte-pont.json` — les mesures.
- `reports/rapport-a80-porte-pont.md` — cette fiche.
