# A8.0 — `porte-topologie` épingle ses PPL : 17,4702 / 30,4363 / 42,5477

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **troisième porte
> épinglée** — `porte-topologie` vérifie les **PPL absolues** du modèle entier, du découpage
> historique, de la topologie et du relais. A8.0 reste **partielle** : 3 portes sur 33.
>
> **Dispositif** : `tools/porte-topologie.sh`, Qwen2.5-0.5B Q8_0, 2 couches locales, 255
> identifiants pour le découpage, 128 pour le relais ; références **17,4702 / 30,4363 / 42,5477**,
> tolérance **5e-4** ; données [`a80-porte-topologie.json`](a80-porte-topologie.json).

## Ce qui est mesuré

| cas | PPL | état |
|---|---:|---|
| modèle entier | **17,4702** | ✅ |
| découpage historique | **30,4363** | ✅ |
| découpage par topologie | **30,4363** | ✅ |
| relais 2 régions / 2 instances | **42,5477** | ✅ |
| relais 3 régions / 3 instances | **42,5477** | ✅ |

La porte **exit 0** ; les PPL sont épinglées et le relais ne change aucun chiffre.

## Le contrôle négatif

La condition est numérique : `abs(ppl - attendu) <= 5e-4 × attendu`. Un décalage de **10 %** des
trois références est **refusé** par la même expression (vérifié avant le commit). Le contrôle porte
sur la valeur, pas sur l’égalité entre bras.

## Ce qui pourrait le rendre faux

- **Un seul modèle et une seule quantification** : les PPL sont liées à Qwen2.5-0.5B Q8_0.
- **Deux limites différentes** : 255 identifiants pour le découpage, 128 pour le relais ; les
  références ne sont pas interchangeables.
- **Tolérance 5e-4** : attrape 0,05 %, pas 0,01 %.
- **Le relais est sauté** si le modèle à 24 couches ou les identifiants manquent ; l’épinglage du
  relais ne s’applique alors pas.

## Ce que ça change

A8.0 passe de **2/33** à **3/33** portes épinglées. Les trois portes qui mesurent la PPL sur le
chemin du placement (`flux`, `pont`, `topologie`) sont maintenant ancrées. La suivante est
`porte-budget` (PPL de deux nœuds) ou `porte-reparti-moteur` (0,0000 %).

## Fichiers

- `tools/porte-topologie.sh` — PPL de référence épinglées.
- `reports/a80-porte-topologie.json` — les mesures.
- `reports/rapport-a80-porte-topologie.md` — cette fiche.
