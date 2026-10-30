# B11.10c — `E4` lu comme requête de case : l’hybride passe à 4/4

> **Ligne de roadmap** : B11.10 · **Date** : 2026-10-29 · **Verdict** : ✅ **4/4 routées et
> 4/4 lues** — une case d’échecs nue (`E4`) avec le jeu explicite est lue comme une **requête**
> `{case: 36}`, pas comme un coup. Sans jeu, elle reste refusée. Le SAN, lui, exige toujours une
> position.
>
> **Dispositif** : `CodecEchecs` (case seule), `lit_avec_indice` ; porte
> `tools/porte-b1110-hybride.sh` ; données [`b1110c-case.json`](b1110c-case.json).

## Ce qui est mesuré

| phrase | jeu | lu ? | RSN |
|---|---|---|---|
| `A1 au morpion` | morpion | ✅ | case 0 |
| `d4 au go` | go | ✅ | point 288 |
| `b6-c5 aux dames` | dames | ✅ | chemin [8,13] |
| `E4 aux échecs` | échecs | ✅ | **requête case 36** |

- **Sans indice** : les quatre refusées.
- **`e2e4` / `2D`** : non touchés.
- **`E4` seule** : refusée, car ambiguë entre quatre jeux.

## Le contrôle négatif

- **`E4` sans jeu** : refus conservé.
- **`E4` avec jeu** : `ok=True`, nature `requete`, pas `coup`.
- **`e2e4`** : reste un coup UCI ; la case seule ne l’écrase pas.
- **`2D`** : reste une carte.

## Ce qui pourrait le rendre faux

- **Une case n’est pas un coup** : la RSN est une requête, pas une action ; un consommateur qui
  attend un coup doit la refuser.
- **Aucune position validée** : `E4` est une case valide, pas une légalité.
- **Quatre surfaces** ; le corpus 161 et le champ natif ne sont pas couverts.

## Ce que ça change

B11.10 est **4/4 routé et lu**. La correction B11.10a (3/4) est **résolue** par la lecture de
case ; B11.10b (indice strippé) reste le mécanisme. Le corpus large et le champ natif 69,3 %
restent des sujets distincts.

## Fichiers

- `tools/jeux/codecs/echecs.py` — case seule.
- `tools/jeux/hybride.py` — indice strippé.
- `tools/porte-b1110-hybride.sh` — la porte.
- `reports/b1110c-case.json` — les mesures.
- `reports/rapport-b1110c-case.md` — cette fiche.
