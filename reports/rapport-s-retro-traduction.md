# S — La rétro-traduction existe : 9/9 paragraphes traduits, 39 paires, l'alignement à raffiner

> **Ligne de roadmap** : S · **Date** : 2026-11-20 · **Verdict** : le **script existe** (l'état de S
> du 06/11 disait « 0 script, 0 mesure, 0/9 »), les **9 paragraphes** sont traduits, et la mesure
> brute donne **39 paires** / **18 accords de classe (46,2 %)**. Mais l'alignement des paires est
> **par position** (la n-ième anaphore française contre la n-ième forme anglaise de la source) :
> l'ordre n'est pas le même (a002 : « l' » → *it* est comparé à *she*). **Le 46,2 % mesure
> l'alignement, pas la traduction** — c'est un plancher, pas un verdict.
>
> **Dispositif** : `tools/structures/retro_traduction.py` (prompt : traduire littéralement + rendre
> les formes anglaises des anaphores en JSON), `deepseek-chat`, 9 appels, `reports/retro-traduction.json`.
> Le témoin `--sans-api` rend 0/9 (aucune traduction) — la mesure ne s'invente pas sans l'API.
>
> **Ce qui pourrait le rendre faux** : l'alignement (ci-dessus) ; la source anglaise contient des
> formes qui ne correspondent pas aux anaphores françaises (l'original et la traduction ne
> s'alignent pas mot à mot) ; le modèle peut traduire librement au lieu de littéralement.
>
> **Prochaine action** : l'alignement **par position** (la forme française et sa forme anglaise
> dans la même réponse), puis la comparaison au gold des a001-a003 (14/14) — une passe remisée.

## La v2 (anaphores numérotées) et l'analyse des a001-a003

Le prompt v2 donne à l'analyseur la liste **numérotée** de ses anaphores ; le modèle rend les formes
dans cet ordre. Sur les trois paragraphes du gold :

- **13 anaphores** rendues, **13 accords de classe** avec la source (a001 6/6, a002 2/2, a003 5/5) ;
- les **2 formes que l'analyseur manque** (« les » de a001, « l' » de a002) ne sont pas dans la
  liste du prompt : la rétro-traduction ne peut pas les valider — c'est le **même trou** que la
  fiche du 03/11 avait nommé (« les » → *it*, « l' » → *it*) ;
- les formes **réflexives** se perdent parfois (« elle se dit » → *she*, la source dit *herself*) :
  la classe tient (personne), la réflexivité non ;
- le taux brut du script (**37,1 %** en v2, 46,2 % en v1) est **faux comme mesure** : il apparie la
  n-ième anaphore à la n-ième forme de la source, et les deux listes n'ont pas la même longueur.
  La mesure juste est **par anaphore de l'analyseur, contre le gold** — 13/13.

## Ce que le premier passage montre déjà

- a001 : 6 accords sur 7 — les formes du gold (She, herself, she, it, herself, her) reviennent ;
- a002 : l'anaphore « l' » du français rend bien *it* (la boîte) — c'est l'**alignement** qui la
  compare à *she* de la source ;
- a003 : les formes reviennent (she, her…), l'accord de classe tient.

## Voir aussi

- [l'état de S](rapport-etat-s.md) · [la traduction contrôle le sens](rapport-s-traductions.md) ·
  [la migration de la banque](rapport-s-migration-profondeur.md)
