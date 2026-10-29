# A8.0 — 0 porte sur 33 n'épingle une PPL

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ❌ **A8.0 n'est pas fait** —
> **33 portes** mesurent ou mentionnent une PPL, **7** la comparent, **0** la comparent à une
> **référence externe**. A8.3 ne peut donc pas passer par défaut : une régression de PPL ne serait
> pas vue.
>
> **Dispositif** : audit statique des `tools/porte-*.sh` ; les sept comparaisons ont été relues à la
> main ; données [`a80-portes-ppl.json`](a80-portes-ppl.json). **Ce n'est pas une mesure de PPL**,
> c'est l'audit de ce que les portes vérifient.

> **Mise à jour du 29/10** : `porte-flux` et `porte-pont` sont désormais **épinglées** (2/33) —
> voir [`rapport-a80-porte-flux.md`](rapport-a80-porte-flux.md) et
> [`rapport-a80-porte-pont.md`](rapport-a80-porte-pont.md). L'audit ci-dessous reste la photographie
> du point de départ (0/33).

## La question

A8.3 est branché en **opt-in** (`DRAVE_PERTE_MAX`) : la règle place + perte rend le même choix que
la main (30,7286 des deux côtés). Pour la passer **par défaut**, il faut d'abord **épingler les
portes qui mesurent une PPL** — sinon un défaut qui dégrade la perplexité passerait sans être vu.

## Ce qui est mesuré

| ce que la porte fait de la PPL | portes |
|---|---:|
| la **mentionne** (log, grep, affichage) | **33** |
| la **compare** dans le même run (identité, budget, dense/creux) | **7** |
| la compare à une **référence externe** | **0** |

Les sept comparaisons intra-run :

| porte | ce qu'elle compare | référence externe |
|---|---|---|
| `porte-adaptateur-sortie.sh` | adaptateur identité vs modèle d'origine | non |
| `porte-budget.sh` | deux exécutions avec budgets différents, **égalité** | non |
| `porte-horloge.sh` | exécution bornée vs non bornée | non |
| `porte-pannes.sh` | présence du résultat après panne | non |
| `porte-poids-creux.sh` | dense vs creux, écart relatif **5e-3** | non |
| `porte-profondeur-routee.sh` | présence de la PPL par profondeur | non |
| `porte-registre.sh` | deux exécutions, **égalité** | non |

**Conséquence.** Une régression **commune aux deux bras** d'une comparaison intra-run passe : si le
défaut dégrade la PPL de 1 %, les deux exécutions la dégradent ensemble et l'égalité tient. Les
portes vérifient la **cohérence**, pas la **valeur**.

## Les contrôles négatifs

- `porte-budget.sh` compare `PPL` et `PPL2` : les deux runs partagent le même défaut ; une
  régression globale est invisible.
- `porte-flux.sh` compare la référence locale et les deux nœuds ; aucun **absolu** n'est vérifié.
- `porte-poids-creux.sh` compare dense et creux à **5e-3** près ; c'est un écart **relatif**, pas un
  ancrage.
- `docs/pilotage/references-non-regression.md` ne porte **aucune** PPL de référence (les portes y
  sont listées par temps et par invariant, pas par perplexité).

## Ce que ça change

A8.0 reste **ouverte** ; A8.3 reste **opt-in**. Le premier pas est de épingler **une** porte stable,
pas les 33 :

- `porte-flux.sh` : les références connues sont **61,9920 / 60,8135** (`historique-passes-portes.md`) ;
- `porte-pont.sh` : **42,5477** sur le relais (archive A7.2) ;
- `porte-budget.sh` : l'égalité est déjà un contrôle ; lui ajouter une **valeur** de référence.

La tolérance doit être **par porte** et **par modèle/corpus** : une PPL n'est pas un invariant
universel.

## Ce qui pourrait le rendre faux

- **Audit statique** : aucune porte n'a été exécutée ; une porte peut épingler une valeur dans un
  fichier de référence non détecté par le motif.
- **Regex** : les sept comparaisons ont été relues, mais les 26 autres n'ont pas été inspectées
  ligne à ligne ; une comparaison indirecte pourrait exister.
- **Les valeurs de PPL dépendent du modèle, du corpus et de la quantification** ; une référence
  unique pour toutes les portes serait fausse.
- **Le test n'est pas une mesure** : il dit ce que les portes vérifient, pas si la PPL est bonne.

## Fichiers

- `reports/a80-portes-ppl.json` — l'inventaire des 33 portes.
- `reports/rapport-a80-portes-ppl.md` — cette fiche.
