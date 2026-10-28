# Continuité — cycles longs, sous-agents, état unique

> **Objet.** Ce document règle **comment un travail continue** : la taille des cycles DSH, le recours
> aux sous-agents, et la discipline de [`docs/pilotage/en-cours.md`](../pilotage/en-cours.md). Il ne
> remplace ni le planning (roadmap) ni les résultats (reports) : il dit **qui écrit l'état, quand, et
> avec quoi on reprend**.
>
> **Règle d'or.** Un cycle n'est fini que lorsque le résultat est **mesuré, écrit, committé**, que
> `en-cours` porte **une ligne de plus** avec sa **prochaine action**, et que la roadmap est à jour.

## 1. Les cycles DSH

| réglage | valeur | pourquoi |
|---|---|---|
| `max_goal_rounds` | **1 000** (ou le maximum du harnais) | la limite est un **filet**, pas un objectif : on ne s'arrête pas à 20 ou 50 rounds |
| goal | **un par programme** (N, B, docs) | recréer un goal à chaque tâche casse la continuité et l'historique |
| reprise | `update_goal resume` | on reprend le **même** goal, on n'en ouvre pas un nouveau |
| fin de cycle | résultat + fiche + commit + `en-cours` + roadmap | jamais « le temps est écoulé » |

- **Un cycle = un sous-chantier**, pas un round de sous-agent. Il peut durer plusieurs heures et
  contenir plusieurs délégations.
- **On ne s'arrête pas sur un compteur.** Si la limite est atteinte avant un résultat : écrire
  `en-cours` + [`REPRISE`](../../REPRISE.md), committer, puis `update_goal resume`.
- **Un cycle bloqué** (corpus, compte, matériel) se **nomme** dans `en-cours` et l'on prend la
  **ligne suivante** de la roadmap — jamais une attente silencieuse.
- **Pas de nouveau goal pour un sous-chantier** : le goal porte le programme, le cycle porte le
  sous-chantier.

## 2. Les sous-agents

### Quand déléguer

- dès qu'il y a **deux tâches indépendantes** (mesure, audit, conversion, test, revue) : **2 à 4
  sous-agents en parallèle** ;
- pour une tâche **longue et isolée** (campagne, migration, vérification exhaustive) ;
- pour une **revue adverse** ou une **continuation** qui a besoin du contexte : `subagent_fork`.

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
2. **fichiers autorisés** — le sous-agent ne touche à rien d'autre ;
3. **livrable** : fichier, mesure, diff, rapport ;
4. **critères d'acceptation** et **contrôle négatif** ;
5. **condition d'arrêt** (temps, essais, succès) ;
6. **format de rapport** : les **10 lignes** ci-dessous ;
7. **interdits** : `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`, `AGENTS.md`, les
   fichiers d'un autre agent.

**Un seul écrivain par fichier.** Le principal garde la propriété de l'état, de la roadmap et des
directives ; le sous-agent est propriétaire de son périmètre.

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

Le principal **vérifie** (porte, lien, contrôle), **met à jour `en-cours`**, **commite** et
**marque la roadmap**. Un résultat de sous-agent n'est **pas fini** tant qu'il n'est pas intégré :
le sous-agent ne clôt pas la tâche, il la rend intégrale.

## 3. La discipline de `en-cours`

`docs/pilotage/en-cours.md` est **la seule source de l'état**. Le journal est de l'histoire, les
fiches sont des résultats, la roadmap est le plan : aucun ne remplace l'état.

| règle | détail |
|---|---|
| **budget** | **≤ 2 000 mots** ; au-delà, on coupe et on renvoie aux fiches |
| **cadence** | mise à jour **à chaque cycle**, et **avant chaque commit de clôture** |
| **une ligne par résultat** | le chiffre + le lien vers la fiche ; jamais le protocole |
| **prochaine action** | toujours nommée, avec son identifiant (N0.3b, N2.4…) |
| **sous-agents actifs** | tableau ou ligne : qui, quoi, état ; « aucun » est une information |
| **questions ouvertes** | **5 au plus**, chacune avec ce qui la débloque |
| **pas de logs** | pas de tableaux de mesures, pas de séries, pas de récit de round |
| **pas de doublon** | un résultat n'apparaît qu'une fois ; on supprime la ligne périmée |

**Lecture** : `AGENTS.md` + `en-cours` (**« Session en cours »** + **« Ce qui reste »**) + **un**
document de tâche. On ne lit ni le journal ni les rapports « pour suivre » : `en-cours` suffit.

**Écriture** : seul le **principal** écrit `en-cours`. Un sous-agent rend un **diff d'état** ; le
principal l'applique, avec le lien et la prochaine action.

**Dépassement** : si `en-cours` dépasse 2 000 mots, on **coupe** (résumé + lien) ou on déplace le
détail dans `reports/` ou la roadmap. On ne relève pas le budget.

## 4. La passation

À la fin d'un cycle, `en-cours` doit permettre à un agent qui n'a **rien vu** de reprendre :

- la **date** est celle du dernier commit ;
- **« Session en cours »** dit l'ID DSH, le goal, les sous-agents actifs et la reprise ;
- **« Ce qui reste »** nomme la **prochaine action** ;
- les **questions ouvertes** sont celles qui bloquent, pas celles qui sont déjà tranchées ;
- le **commit** et la **fiche** sont liés.

Un nouvel agent lit `AGENTS` + `en-cours` + **un** document de tâche, puis [`REPRISE`](../../REPRISE.md)
pour les pièges. Le journal ne se lit que si l'on a besoin du **récit** d'une journée précise.
Le journal est en **dossiers par jour** (`journal/AAAA-MM-JJ/`) ; chaque rapport de session
renvoie à son jour, à l'index des sessions et à `en-cours` (`python3 tools/verifie_journal.py`).

## 5. Reprendre un goal en pause

Un goal est **lié à sa session**. Ouvrir la session qui le porte, demander **directement**
« Reprends le goal en pause » : l'agent appelle `get_goal` (goal_id, revision) puis
`update_goal action="resume"`. Si la pause vient de `max_goal_rounds`, faire d'abord
`action="edit"` avec `max_goal_rounds=1000`. Relire `en-cours` avant de continuer.

## 6. Vérifier

```bash
python3 tools/verifie_en_cours.py   # structure, taille, sections, prochaine action
python3 tools/taille_documents.py   # budgets T0/T1
python3 tools/revue_documentation.py # liens, compteurs, fraîcheur
```

`verifie_en_cours.py` échoue si `en-cours` dépasse 2 000 mots, s'il manque une section, si une
section « Ce qui est en cours » dépasse 10 puces, si les questions ouvertes dépassent 5, ou si la
prochaine action n'est pas nommée.

> *Un état qu'on ne peut pas reprendre en deux minutes n'est pas un état : c'est un journal.*
