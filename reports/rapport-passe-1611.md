# La passe complète du 16/11 (nuit exploitable) — 84 portes, 81 vertes, 3 rouges nommées

> **Ce que cette fiche est.** Le relevé de la **passe complète** lancée par la tâche Z2
> (`JOURNAUX=work/portes/passe-1611`, l'agent a dépassé son timeout après 70 min ; la passe a
> continué et **terminé**) : **84 portes**, **81 vertes**, **3 rouges** — et deux des trois sont
> **tolérées et connues**.
>
> **Le chiffre.** Registre : `work/portes/passe-1611/registre.txt`, lu par `awk '$2 != 0'` :
> - `porte-indice` (1) — la structurelle, antérieure (l'indice extérieur tombe à 482 jetons) ;
> - `porte-melange` (1) — la structurelle, antérieure (l'état de A ne rend pas le code de A) ;
> - `porte-sessions` (1) — le mandat du **hub** `1e7ef596`, périmé (le mien est rafraîchi).
>
> `porte-tableaux` a rougi **pendant** la passe (un document en cours d'écriture par un agent
> concurrent) et **repasse verte** en isolation (`bash tools/porte-tableaux.sh` → 1 857 fichiers,
> 4 852 liens, EXIT 0) : ce n'était pas une régression.
>
> **La lecture.** Les deux rouges structurelles sont dans
> [`references-non-regression.md`](../docs/pilotage/references-non-regression.md) ; la rouge
> `sessions` est un **état de session**, pas une porte de code. **Aucune nouvelle rouge.**

## Ce qui a changé depuis la passe du 14/11

- Le **tagger** (`--tagger`, `auto`), la **base réelle** (`--reel`), `--strict`, `--profils`,
  `--duree`, les **candidats objets**, les **rôles normalisés**, l'**empaquetage** (la roue), le
  **quickstart**, la **CI** — la passe les couvre (la porte produit 183/183, le banc, le bloc).
- Le temps : la passe a pris **~2 h** (les portes lourdes : poids-creux, préchargement, produit).

## Ce que cette fiche ne dit pas

- Elle ne mesure **pas** les rouges : elle les **lit** (la passe les a mesurées).
- Elle ne prouve pas l'absence de régression : les 81 vertes sont celles de la passe du 16/11.

## Fichiers

- `work/portes/passe-1611/registre.txt` — le registre (85 lignes).
- `work/portes/passe-1611/` — les journaux des portes.
