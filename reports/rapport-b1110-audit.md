# B11.10a — audit : 4/4 routées, 3/4 lues

> **Ligne de roadmap** : B11.10 · **Date** : 2026-10-29 · **Verdict** : ✅ **correction** — le
> rapport B11.10 annonçait **4/4 exacts avec le jeu explicite** ; c’est **4/4 routées** mais
> **3/4 lues**. `E4` aux échecs est bien routé, mais le codec exige une **position** pour un SAN
> et rend `ok=False`. `A1 au morpion` avec l’indice dans la phrase échoue aussi.
>
> **Dispositif** : `lit(surface, jeu=…)` et `lit(surface avec indice)` sur les quatre surfaces ;
> données [`b1110-audit.json`](b1110-audit.json).

## Ce qui est mesuré

| surface | jeu | `ok` | RSN / erreur |
|---|---|---|---|
| `A1` | morpion | **oui** | case 0, symbole nul |
| `E4` | échecs | **oui** (B11.10c) | requête case 36 |
| `d4` | go | **oui** | point 288, taille 19 |
| `b6-c5` | dames | **oui** | chemin [8, 13] |

Avec un indice dans la phrase : `d4 au go` et `b6-c5 aux dames` passent ; `E4 aux échecs` reste
`ok=False` ; `A1 au morpion` échoue parce que la phrase n’est pas strippée.

## Le contrôle négatif

- **Sans jeu** : les quatre surfaces sont refusées (ambiguïté nommée).
- **Avec jeu** : le routage est 4/4, la lecture 3/4.
- **`e2e4` / `2D`** : non touchés (contrôles du rapport B11.10).
- **Le 4/4 du rapport** était un **routage**, pas une lecture : la distinction est le résultat.

## Ce qui pourrait le rendre faux

- **Quatre surfaces** seulement ; pas le corpus 161.
- **Pas de champ natif** : le 69,3 % n’est pas reproduit ici.
- **`E4` sans position** n’est pas une lecture incomplète du codec : c’est une exigence
  sémantique (un SAN se valide sur une position).
- **`A1 au morpion`** est un cas de phrase, pas de codec.

## Ce que ça change

B11.10 est **mesurée mais corrigée** : 4/4 routées, 3/4 lues. L’hybride devra soit fournir une
position pour `E4`, soit stripper l’indice de jeu ; le champ natif 69,3 % reste un autre sujet.

## Fichiers

- `reports/b1110-audit.json` — les mesures.
- `reports/rapport-b1110-audit.md` — cette fiche.
