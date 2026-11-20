# S — La profondeur entre dans la banque : 324/369 candidats appariés, 95 à profondeur ≥ 3

> **Ligne de roadmap** : S · **Date** : 2026-11-20 · **Verdict** : la migration `/` v7 est faite
> **sans casser les 150 verdicts** — les identifiants des phrases et des candidats sont conservés,
> et la `profondeur` de l'analyseur v7 est ajoutée aux segments stockés. **324 des 369 candidats**
> (87,8 %) sont appariés ; 45 ne le sont pas (leur `lecture` a changé entre la génération du 02/11
> et l'analyseur v7) ; **95 candidats ont une profondeur maximale ≥ 3** (maximum 5).
>
> **Dispositif** : `tools/structures/regenerer_banque.py` (nouveau) — pour chaque phrase des deux
> fichiers (`phrases.json` + `phrases_generees.json`), l'analyseur courant, puis l'appariement des
> candidats par `lecture` et des segments par `debut`/`fin` ; `static/app.js` lit
> `profondeur ?? niveau` pour l'indentation. 57 tests du sous-module verts.

## Le tableau

| quoi | avant | après |
|---|---:|---:|
| candidats dans la banque | 369 | 369 |
| candidats avec `profondeur` | 0 | **324** (87,8 %) |
| candidats à profondeur max ≥ 3 | 0 | **95** |
| profondeur maximale | — | **5** |
| verdicts de la banque | 150 | 150 (inchangés) |

## Ce qui pourrait le rendre faux

- Les **45 non appariés** : leur `lecture` a changé (l'analyseur a évolué entre le 02/11 et
  aujourd'hui) ; leurs segments restent sans `profondeur` et l'indentation retombe sur `niveau`.
- L'appariement par `lecture` peut apparier un candidat à un autre de même lecture mais de
  structure différente — rare, mais possible.
- La profondeur mesure l'**arbre de l'analyseur**, pas une vérité syntaxique.

## Voir aussi

- [l'état de S](rapport-etat-s.md) · [l'analyseur](rapport-s-analyseur-roles.md) ·
  [les limites](rapport-s-limites-v6.md)
