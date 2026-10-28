# C3.2e — les sous-familles des autres familles

> **Objet.** C3.2d avait expliqué l'indo-européen (14,7 %) par ses sous-familles. Ici on descend
> d'un niveau dans **atlantic-congo**, **austronesian**, **afro-asiatic** et **uralic**, avec le
> même module de recopie.

## Résultats (8 textes, contrôle 0 %)

| famille | sous-famille | langues | famille entière | sous-famille |
|---|---|---:|---:|---:|
| atlantic-congo | **benue-congo** | 45 | 94,0 % | **88,0 %** |
| austronesian | **est** | 12 | 61,0 % | **60,3 %** |
| afro-asiatic | **ouest** | 6 | 60,2 % | **53,5 %** |
| uralic | **côtier** | 5 | 46,7 % | **100,0 %** |

## Lecture

- L'**uralic** est le cas le plus net : la famille entière est à **46,7 %**, mais la sous-famille
  **côtière** atteint **100 %**. Le 46,7 % est un **effet de composition**, comme l'IE.
- L'**atlantic-congo** reste très haut (**88 %** pour benue-congo, 94 % pour la famille) : la
  sous-famille **n'ajoute pas**.
- L'**austronesian** est stable (60,3 % contre 61,0) : le découpage ne change pas la difficulté.
- L'**afro-asiatic** **baisse** (53,5 % contre 60,2) : la sous-famille **ouest** est plus difficile
  que la moyenne de la famille ; le découpage ne suffit pas à expliquer.
- Le **contrôle** est à **0 %** partout.

## Verdict

**C3.2e est positif pour l'uralic** : la sous-famille côtière **explique** la famille à 46,7 %.
Pour les trois autres, le découpage **ne change pas** la conclusion — la famille n'est pas un
mélange problématique, sauf pour l'afro-asiatic où la sous-famille ouest est **plus difficile**.

## Limites

- **4 sous-familles**, une par famille ; d'autres branches existent.
- **5 à 45 langues**, corpus courts ; évaluation à mi-corpus.
- **200 pas**, rang 8, un seul run.
- Le découpage glottolog au 2ᵉ niveau est **grossier** pour certaines familles.

## Fichiers

- Données : `data/udhr/familles/{ac_benue,austro_est,afro_ouest,uralic_coastal}.jsonl`.
- Outil : [`tools/lora_recopie.py`](../tools/lora_recopie.py).
- JSON : [`sous-familles-autres.json`](sous-familles-autres.json).
