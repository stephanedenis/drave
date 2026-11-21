# S — Les deux formes que l'analyseur manquait sont retrouvées : 14/16 → 16/16 sur le gold

> **Ligne de roadmap** : S · **Date** : 2026-11-20 (nuit) · **Verdict** : le trou documenté le 03/11
> — « les » (les suivît → *it*) et « l' » (l'ouvrit → *it*) — venait de la **classe** : ces formes
> sont des `DET`, et `referents()` ne regardait que les `PRON` et les possessifs. Une règle
> **étroite** les retrouve : un `les` / `l'` **suivi d'un verbe** est un pronom objet, pas un
> déterminant. Sur les **216 textes** de la banque (207 phrases + 9 paragraphes) : 405 → **409**
> référents, **4 ajouts, tous des clitiques** (« les suivît », « l'ouvrit », « l'était »,
> « l'attendaient ») ; **0 faux positif** dans l'échantillon. Sur le gold des a001-a003 :
> **14/16 → 16/16** formes couvertes. Les 57 tests du sous-module restent verts.

## La règle, et pourquoi elle est étroite

- **« l' »** : le jeton est analysé après l'élision — « l'ouvrit » est un seul mot dans le
  découpage, on regarde le reste (« ouvrit ») et il doit finir comme un verbe (ît / it / ait /
  aient / ut / urent / èrent / rent / ont) ;
- **« les »** : le jeton doit être exactement « les », et le mot suivant doit finir comme un verbe ;
- **jamais « le / la »** : trop de noms commencent par une forme verbale (« le lit »), et les
  formes non élidées n'étaient pas dans le trou ;
- **« l'opium » n'est pas un clitique** : c'est un seul jeton (DET + nom), exclu par construction ;
  « l'idée » ne finit pas comme un verbe.

## Ce qui pourrait le rendre faux

- Un nom en -it/-ait après « les » (« les récits » finit en -its, exclu ; « les habits » en -ts) :
  la terminaison protège, mais ce n'est pas une preuve — un relevé sur un corpus plus large le
  dirait.
- Le trou restant : les clitiques **non élidés** « le / la » (« le vit », « la regarda ») — non
  traités, volontairement.
- La mesure est faite sur la banque (216 textes), pas sur un corpus de référence : les 4 ajouts
  sont vérifiés à la main un par un, pas statistiquement.

## La suite

Relancer la **rétro-traduction** à la prochaine fenêtre remisée : les deux formes seront dans la
liste du prompt, et les paires a001/a002 devraient les voir (le gold les attend).

## Voir aussi

- [la rétro-traduction](rapport-s-retro-traduction.md) · [l'or de rôles](rapport-j4-seconds-cadres.md) ·
  [l'analyseur](rapport-s-analyseur-roles.md)
