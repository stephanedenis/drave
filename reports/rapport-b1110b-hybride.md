# B11.10b — l’indice de jeu strippé route les quatre ambiguës

> **Ligne de roadmap** : B11.10 · **Date** : 2026-10-29 · **Verdict** : ✅ **hybride** — quand
> la phrase nomme le jeu, l’indice est **strippé** et la surface est lue avec le jeu explicite.
> **4/4 routées, 3/4 lues** : `E4` aux échecs exige une **position** pour un SAN.
>
> **Dispositif** : `tools/jeux/hybride.py`, `lit_avec_indice` ; porte
> `tools/porte-b1110-hybride.sh` ; données [`b1110b-hybride.json`](b1110b-hybride.json).

## Ce qui est mesuré

| phrase | jeu | lu ? | RSN / erreur |
|---|---|---|---|
| `A1 au morpion` | morpion | **oui** | case 0 |
| `d4 au go` | go | **oui** | point 288 |
| `b6-c5 aux dames` | dames | **oui** | chemin [8,13] |
| `E4 aux échecs` | échecs | **non** | position requise pour un SAN |

- **Sans indice** : les quatre sont refusées.
- **`e2e4` et `2D`** : non touchés.
- **Bilan** : 4/4 routées, **3/4 lues**.

## Le contrôle négatif

- **Sans indice** : refus conservé ; l’hybride n’invente pas un jeu.
- **`E4`** : routé mais refusé — un SAN se valide sur une position, pas sur une case nue.
- **`e2e4`/`2D`** : les contrôles du rapport B11.10 restent verts.
- **La porte peut échouer** : un jeu mal routé ou un `ok` inattendu la fait sortir en 1.

## Ce qui pourrait le rendre faux

- **Quatre phrases** ; pas le corpus 161.
- **Pas de champ natif** : le 69,3 % n’est pas reproduit.
- **`E4`** n’est pas une lecture incomplète : c’est une exigence sémantique.
- **L’indice est une règle de surface** ; une phrase qui nomme le jeu sans le vouloir serait routée.

## Ce que ça change

B11.10b est **fait** : l’hybride route 4/4 et lit 3/4. Pour `E4`, il faut une position (ou
accepter le refus) ; le corpus large et le champ natif restent.

## Fichiers

- `tools/jeux/hybride.py` — `lit_avec_indice`.
- `tools/porte-b1110-hybride.sh` — la porte.
- `reports/b1110b-hybride.json` — les mesures.
- `reports/rapport-b1110b-hybride.md` — cette fiche.
