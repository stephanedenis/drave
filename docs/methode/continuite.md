# Continuité — cycles longs, sous-agents, état unique

> **Objet.** Comment un travail continue : cycles DSH, sous-agents, discipline de
> [`en-cours`](../pilotage/en-cours.md). Ni planning ni résultats : **qui écrit l'état, quand, et avec quoi on reprend**.
>
> **Règle d'or.** Un cycle est fini quand le résultat est **mesuré, écrit, committé**, qu'`en-cours` porte sa
> **prochaine action**, et que la roadmap est à jour.

## 1. Les cycles DSH

| réglage | valeur | pourquoi |
|---|---|---|
| `max_goal_rounds` | **1 000** (ou le maximum du harnais) | la limite est un **filet**, pas un objectif : on ne s'arrête pas à 20 ou 50 rounds |
| goal | **un par programme** (N, B, docs) | recréer un goal à chaque tâche casse la continuité et l'historique |
| reprise | `update_goal resume` | on reprend le **même** goal, on n'en ouvre pas un nouveau |
| fin de cycle | résultat + fiche + commit + `en-cours` + roadmap | jamais « le temps est écoulé » |

- **Un cycle = un sous-chantier**, pas un round : plusieurs heures et délégations possibles.
- **On ne s'arrête pas sur un compteur** : si la limite tombe avant un résultat, écrire `en-cours` +
  [`REPRISE`](../../REPRISE.md), committer, puis `update_goal resume`.
- **Un cycle bloqué** se **nomme** et l'on prend la **ligne suivante**.

## 2. Les sous-agents

### Quand déléguer

- **deux tâches indépendantes** : **2 à 4** en parallèle ;
- une tâche **longue et isolée** ;
- une **revue adverse** ou une **continuation** : `subagent_fork`.

**On ne délègue pas** : une édition triviale d'une ligne, l'écriture de `en-cours`/`roadmap`/`AGENTS`,
la décision humaine, ou deux agents sur le **même fichier**.

### Comment

| outil | usage |
|---|---|
| `subagent` | tâche autonome, sans contexte de la conversation |
| `subagent_fork` | revue, continuation, analyse qui s'appuie sur la conversation |
| `workflow` | **fan-out** sur beaucoup d'items indépendants (audit, migration) |

**Contrat de prompt** (obligatoire) :

1. **objectif** en une phrase, et le résultat attendu ;
2. **fichiers autorisés** — rien d'autre ;
3. **livrable** : fichier, mesure, diff, rapport ;
4. **critères d'acceptation** et **contrôle négatif** ;
5. **condition d'arrêt** (temps, essais, succès) ;
6. **format de rapport** : les **10 lignes** ci-dessous ;
7. **interdits** : `en-cours`, `roadmap`, `AGENTS`, les fichiers d'un autre agent.

**Un seul écrivain par fichier** : la session qui clôt garde l'état, la roadmap et les directives ; le sous-agent
possède son périmètre.

### Le rapport d'un sous-agent (10 lignes)

1. **fait** — ce qui est terminé, avec le chiffre ;
2. **fichiers** — les chemins touchés ;
3. **mesure** — la commande et le résultat ;
4. **contrôle négatif** — ce qui aurait dû échouer ;
5. **ce qui pourrait le rendre faux** ;
6. **limites** — ce qui n'a pas été testé ;
7. **prochaine action** ;
8. **diff d'état** — la ligne exacte à mettre dans `en-cours` ;
9. **commit** — le hash, ou « aucun » ;
10. **blocage** — nommé, ou « aucun ».

Pas de logs bruts, pas de récit de tâtonnements, pas de tableau de mesures.

### L'intégration

La session **vérifie** (porte, lien, contrôle), **met à jour `en-cours`**, **commite** et
**marque la roadmap**. Un résultat de sous-agent n'est **pas fini** tant qu'il n'est pas intégré :
le sous-agent ne clôt pas la tâche, il la rend intégrale.

## 3. La discipline de `en-cours`

`docs/pilotage/en-cours.md` est **la seule source de l'état**. Le journal est de l'histoire, les
fiches sont des résultats, la roadmap est le plan : aucun ne remplace l'état.

| règle | détail |
|---|---|
| **budget** | **≤ 2 000 mots** ; au-delà, on **coupe** (résumé + lien) et on ne relève pas |
| **cadence** | mise à jour **à chaque cycle**, et **avant chaque commit de clôture** |
| **une ligne par résultat** | le chiffre + le lien vers la fiche ; jamais le protocole |
| **prochaine action** | toujours nommée, avec son identifiant (N0.3b, N2.4…) |
| **écriture** | toute session écrit `en-cours`, **une à la fois** ; aucun fait (`reports/`, roadmap, backlog) ne se commite sans sa ligne (hook `pre-commit`) |
| **sessions actives** | une sous-section par session : Id, rôle, action, autres sessions, prochaine action, bloquants, journal ; le rôle nomme le chantier |
| **plan** | `journal/sessions/<id>/plan.md` |
| **bloquants** | un bloquant par chantier A/B/N/R, même « aucun » |
| **questions ouvertes** | **5 au plus**, chacune avec ce qui la débloque |
| **pas de logs** | pas de tableaux de mesures, pas de séries, pas de récit de round |
| **pas de doublon** | un résultat n'apparaît qu'une fois ; on supprime la ligne périmée |

**Lecture** : `AGENTS.md` + `en-cours` (« Sessions en cours », « Les chantiers et leurs bloquants »,
« Ce qui reste ») + **un** document de tâche. On ne lit ni journal ni rapports « pour suivre ».

**Écriture** : toute session écrit `en-cours`, **une à la fois** ; aucun fait (`reports/`, roadmap,
backlog) ne se commite sans sa ligne — `tools/verifie_etat_a_jour.py` le refuse (hook) et
`porte-etat.sh` compare les commits. Git : `git status`, `git add` explicite, jamais `-A`/`commit -a`,
jamais `--amend` sur le commit d'un autre.

À la fin d'un cycle, `en-cours` doit permettre de reprendre sans contexte :

- la **date** est celle du dernier commit ;
- **« Sessions en cours »** : une sous-section par session active, avec ses sept champs (Id, rôle, action,
  autres sessions, prochaine action, bloquants, journal) ;
- **« Les chantiers et leurs bloquants »** : A/B/N/R, bloquant non vide ;
- **« Ce qui reste »** nomme la **prochaine action** ;
- les **questions ouvertes** sont celles qui bloquent, pas celles qui sont déjà tranchées ;
- le **commit** et la **fiche** sont liés.

**Sessions terminées** : archivées dans `journal/sessions/<id>/rapport.md`, elles **sortent** d'`en-cours` ;
les éléments finis du jour vont dans `journal/AAAA-MM-JJ/etat-transfere.md`.

Un nouvel agent lit `AGENTS` + `en-cours` + **un** document de tâche, puis [`REPRISE`](../../REPRISE.md).
Le journal ne se lit que pour le **récit** d'une journée ; chaque rapport de session renvoie à son jour,
à l'index des sessions et à `en-cours` (`python3 tools/verifie_journal.py`).

## 4. Arrimer l'écran à la session

`en-cours`, `journal/sessions/<id>/plan.md` et le premier item du TUI portent la même identité
(`Session <id> — rôle`). Le premier item suit le plan ; sinon la session est non déclarée ou le
plan périmé. `tools/sessions.py --check` compare plans et `en-cours` ; le TUI reste une convention.

## 5. Reprendre un goal en pause

`get_goal`, puis `update_goal action="resume"` ; si `max_goal_rounds` est atteint, `edit` d'abord.

## 6. Vérifier

`verifie_en_cours.py`, `verifie_etat_a_jour.py`, `sessions.py --check`, `taille_documents.py`,
`revue_documentation.py` ; le hook refuse un fait sans `en-cours`.

> *Un état qu'on ne peut pas reprendre en deux minutes n'est pas un état : c'est un journal.*
