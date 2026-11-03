# Le dossier pilotage — carte et ordre de lecture

> **Ce que ce dossier est.** Le **pilotage** du projet : l'état courant, l'ordre des chantiers,
> le plan de travail multi-sessions, les relations entre chantiers, les contrats du backlog, les
> manques et les références de non-régression. **Ce n'est pas** la documentation de conception
> (celle-ci est dans `docs/theorie/`, `docs/implantation/`, `docs/methode/`) ni les résultats
> (`reports/`) ni le récit (`journal/`).
>
> **Machine** : une seule ; plusieurs sessions travaillent en parallèle sur le même arbre de
> travail. Les territoires et la surveillance sont dans [`plan-travail.md`](plan-travail.md) ; le
> registre des ressources machine (GPU, CPU, RAM, IO) et son protocole sont au **§ 10** du même
> plan, outillé par `tools/ressources.py`.

## L'ordre de lecture

| ordre | document | ce qu'il répond | quand le lire |
|---|---|---|---|
| 1 | [`en-cours.md`](en-cours.md) | que se passe-t-il **maintenant** ? | au début de chaque session |
| 2 | [`plan-travail.md`](plan-travail.md) | **qui** fait quoi, où, à quelle cadence ? | avant d'ouvrir une session |
| 3 | [`roadmap.md`](roadmap.md) | dans quel **ordre** et avec quel état ? | pour choisir la tâche |
| 4 | [`chantiers.md`](chantiers.md) | **pourquoi** les chantiers tiennent ensemble (relations, tensions, capacité) | une fois, pour la vue d'ensemble |
| 5 | [`programme-r.md`](programme-r.md) | le **lecteur** (R0–R5), ses phases et ses lois | pour une tâche du programme R |
| 6 | [`backlog/index.md`](backlog/index.md) | les **contrats** par fonctionnalité | pour coder une fonctionnalité |
| 7 | [`backlog/dependances.md`](backlog/dependances.md) | le **graphe** des dépendances du backlog | avant de déclarer une dépendance |

**Documents datés — ne pas charger par défaut** : [`manques.md`](manques.md) (registre des
manques, revu le 27/10), [`utilisation.md`](utilisation.md) (ce qui s'utilise, revu le 27/10),
[`references-non-regression.md`](references-non-regression.md) (les rouges tolérées).

## Les fichiers, et qui les écrit

| fichier | écrit par | contenu |
|---|---|---|
| `en-cours.md` | le **hub** (une session à la fois) | l'état court : synthèse, chantiers, sessions actives (onze champs), questions |
| `plan-travail.md` | le **hub** | les quatre sessions, les territoires, la cadence, la surveillance |
| `roadmap.md` | le **hub** | l'ordre des chantiers, les états, la prochaine action |
| `chantiers.md` | le **hub** | les relations, la vision à jour, la capacité |
| `programme-r.md` | le **hub** | la charte du programme R |
| `manques.md`, `utilisation.md` | le **hub** | les documents datés |
| `references-non-regression.md` | le **hub** | les portes rouges tolérées |
| `backlog/` | la session qui ouvre le chantier | une fiche par fonctionnalité |

Les sessions **proposent** leur section et leur fait ; le hub **intègre** et commite. Un fait
(`reports/`, `tools/`) ne se commit pas sans sa ligne d'état (hook `verifie_etat_a_jour.py`).

## Les outils du pilotage

| outil | rôle |
|---|---|
| `tools/sessions.py --status` / `--check` | les plans de session : mandats, heartbeats, **périmètres et réservations qui se recouvrent** |
| `tools/surveille_sessions.py` | les **fichiers en mouvement** (`git status`) par session, les orphelins, les conflits |
| `tools/verifie_etat_a_jour.py` | aucun fait commité sans état |
| `tools/revue_documentation.py` | classement, liens, compteurs, fraîcheur |
| `tools/ressources.py` | les ressources machine (GPU, CPU, RAM, IO) : réservations, file, usage réel |
| `tools/taille_documents.py` | les budgets de contexte (T0 ≤ 4 000) |
| `tools/verifie_journal.py` | les jours, les sessions, les liens |
| `tools/carte_chantiers.py` | la carte `docs/schemas/chantiers-vision.svg` |
| `tools/carte_decisions.py` | la carte de décision `docs/schemas/chantiers-decision.svg` |

## Les règles en trois lignes

1. **Un écrivain par fichier** ; l'état, la roadmap et les compteurs s'écrivent **une session à la
   fois** (le hub).
2. **Un fait = une fiche + un contrôle + un commit + une ligne d'état** ; les limites sont
   nommées.
3. **La machine est partagée** : réservations déclarées, fichiers en mouvement surveillés,
   portes lourdes sérialisées, `IA` à 34 Go — pas de nouveau gros modèle sans supprimer.
