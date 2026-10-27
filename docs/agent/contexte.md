# Le contexte de l'IA — ce qu'on charge, et ce qu'on ne charge pas

> **Principe.** Le contexte est un **budget**, pas un espace gratuit. On charge le **minimum** qui
> permet de faire la tâche, et **jamais** « pour être complet ». Un document qui n'est pas nécessaire
> à la décision du moment est du bruit — et le bruit coûte plus cher que le manque.
>
> **Règle d'or.** `AGENTS.md` + `docs/en-cours.md` + **un** document de tâche. Tout le reste est
> **à la demande**, par section, jamais en entier.

## Les trois niveaux

| niveau | ce qu'on charge | budget | exemples |
|---|---|---:|---|
| **T0 — toujours** | les règles, l'état, **un** document de tâche | **≤ 4 000 mots** | `AGENTS.md` · `docs/en-cours.md` · `docs/agent/<tâche>.md` |
| **T1 — à la demande** | **un** concept, **une** section de roadmap, **un** verdict de fiche, **une** fiche de glossaire | **budget par document** (tableau ci-dessous) | `docs/vision.md` · `docs/synthese/0*.md` · `reports/<fiche>.md` (verdict + section) · `docs/glossaire/0*.md` |
| **T2 — jamais en entier** | l'histoire, les mesures brutes, les archives, les journaux | **0 mot par défaut** | `journal/` · `docs/archive/` · `reports/` (sauf verdict) · les documents datés |

## Le protocole de chargement

1. Lire [`AGENTS.md`](../../AGENTS.md) — les règles et le routage.
2. Lire [`docs/en-cours.md`](../en-cours.md) — l'état courant, pas l'historique.
3. Lire **un seul** document de tâche dans [`docs/agent/`](.) — celui de la tâche.
4. Si la tâche a besoin d'un **concept**, lire le chapitre de [`docs/synthese/`](../synthese/)
   ou la page de `docs/` qui le porte — **pas les deux**, et **pas** le glossaire entier.
5. Si la tâche a besoin d'un **résultat**, lire le **verdict** de la fiche (les 10 premières lignes)
   puis **une** section ; jamais la fiche entière si elle dépasse 300 lignes.
6. Si la tâche a besoin d'un **mot**, lire sa **fiche** (`docs/glossaire/entrees/<slug>.md`, 2-3 lignes) ; si elle n'existe pas, `grep` la famille — jamais les 11.
7. Si la tâche a besoin d'une **ligne de roadmap**, lire le **résumé exécutif** puis la section A ou B.

## Les budgets

| document | budget (mots) | usage |
|---|---:|---|
| `AGENTS.md` | 1 200 | **T0** — toujours |
| `docs/en-cours.md` | 2 000 | **T0** — toujours |
| `docs/agent/*.md` | 1 200 | **T0** — un seul |
| `docs/README.md` · `docs/carte.md` | 1 000 | **T1** — si l'on cherche un fichier |
| `docs/synthese/index.md` | 2 000 | **T1** — l'introduction |
| `docs/synthese/0*.md` | 2 000 | **T1** — un chapitre |
| `docs/roadmap.md` | 8 500 | **T1** — résumé + une section |
| `docs/glossaire.md` | 1 500 | **T1** — l'index des familles |
| `docs/glossaire/0*.md` | 5 000 | **T1** — `grep` le terme, jamais les 11 |
| `docs/glossaire/README.md` | 2 000 | **T1** — l'index des entrées |
| `docs/schemas/README.md` | 1 500 | **T1** — l'index des schémas |
| `docs/glossaire/entrees/*.md` | 150 | **T1** — une fiche, une carte |
| `reports/README.md` | 2 800 | **T1** — les fiches courantes seulement |
| `README.md` | 3 500 | **T1** — la vitrine publique |
| `REPRISE.md` | 2 000 | **T1** — la check-list de démarrage |
| `docs/utilisation.md` | 2 500 | **T1** — les commandes qui marchent |

Les documents **datés** (`contexte-long`, `numa-segregation`, `configuration-nvme-raid-amd`,
`convertisseur`, `manques`, `modularisation`) ont un **résumé** en tête et ne se chargent **jamais**
par défaut : on lit le résumé, puis la section utile.

Les **fiches de résultats** ne sont pas dans ce tableau : elles ne s'intègrent pas au contexte
automatique. On lit le **verdict** (les 10 premières lignes) et **une** section ; le reste est du
détail de protocole.

## Ce qui n'entre jamais

- `journal/` — le récit daté, y compris `journal/sessions/` : c'est de l'histoire, pas de l'état.
- `docs/archive/` — les plans et notes conservés pour l'histoire.
- `reports/` en entier — une fiche par question ; on cite la fiche, on ne l'avale pas.
- `docs/glossaire/` en entier — on charge la **fiche** du terme, ou on `grep` la famille.
- `reports/historique-passes-portes.md` — l'historique des passes, pas les repères courants.
- les documents datés — sauf si la tâche est **précisément** leur sujet.

## La cohésion d'un document

Un document chargeable doit :

1. avoir **un seul sujet** — un document = une question ;
2. porter un **titre** et un **résumé de 3 à 6 lignes** dans les 15 premières lignes ;
3. dire **quand le charger** (et quand ne pas le charger) ;
4. avoir des **sections** si plus de 200 lignes, et un **résumé** si plus de 500 ;
5. **renvoyer** au lieu de recopier : l'état à `en-cours.md`, les chiffres à `reports/`, le récit au
   `journal/` ;
6. ne pas mélanger **théorie**, **mesures** et **histoire** dans le même fichier.

Si un document dépasse son budget, on **coupe** : un résumé + un lien, ou un découpage en sections
avec un index. On ne « compense » pas par un contexte plus grand.

## Vérifier

```bash
python3 tools/taille_documents.py       # la taille, les budgets, les résumés manquants
python3 tools/revue_documentation.py    # les liens, les compteurs, la cohérence
bash tools/porte-tableaux.sh            # les tableaux et les liens
```

`tools/taille_documents.py` échoue si un document **T0/T1** dépasse son budget ou s'il manque son
résumé. Les fiches de `reports/` et le `journal/` sont **hors budget** : ils ne sont pas chargés
automatiquement.

> *Un contexte exemplaire n'est pas un contexte qui contient tout : c'est un contexte qui contient
> exactement ce qu'il faut, et qui sait où trouver le reste.*
