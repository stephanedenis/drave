# Le chantier autonome — le méta-harnais

> **La question.** Peut-on laisser l'agent travailler **plusieurs jours** sans surveillance ? DSH
> en est-il capable seul, ou faut-il un **méta-harnais** ?
>
> **La réponse courte.** DSH fournit l'**agent** (les rounds, la session reprenable, la compaction,
> les sous-agents) ; il ne fournit **pas** la **couche de contrôle** d'un chantier long. Le
> méta-harnais est `tools/chantier/` : une **file de tâches**, un **superviseur** qui lance l'agent,
> **vérifie l'acceptation** et persiste l'état, et un **arrêt propre**. Il est en place et testé.

## 1. Ce que DSH donne — et ce qui manque

| DSH fournit | conséquence |
|---|---|
| les **rounds** (`max_goal_rounds`) et la continuation | l'agent ne s'arrête pas après un tour |
| la **session reprenable** (`--session-id`) | on peut reprendre une session interrompue |
| la **compaction** (le checkpoint) | le contexte ne déborde pas |
| les **sous-agents** et le **workflow** | on parallélise les analyses |
| le mode **`headless`** (une tâche, une réponse, sortie) | **scriptable** |

| ce qui manque pour plusieurs jours | le méta-harnais |
|---|---|
| une **file de tâches** persistante | `tools/chantier/plan.json` |
| une **acceptation indépendante** de l'agent | le superviseur exécute lui-même les tests |
| un **budget** (temps, lancements) | `--budget`, `--max-taches`, `etat.json` |
| la **reprise après crash** | l'état écrit après **chaque** étape |
| l'**escalade** (une tâche qui échoue) | `max_tentatives`, statut `bloque`, journal |
| un **journal d'audit** | `work/chantier/journal.log` |
| un **arrêt propre** | `work/chantier/STOP` |
| la **clé** du modèle | lue depuis `~/.config/drave/deepseek.key` |

**Le fait décisif, mesuré** : `dsh --profile headless` **exige** `DEEPSEEK_API_KEY` ; sans elle,
il rend `MISSING_CREDENTIAL`. Le superviseur lit la clé du fichier et la passe au processus fils —
c'est ce qui rend la boucle possible. (L'agent interactif, lui, a ses propres identifiants.)

## 2. L'architecture

```
plan.json          la file : chaque tâche a un mandat, une acceptation, un budget
     │
superviseur.py     boucle : prochaine tâche → dsh headless (clé) → acceptation → état → suivante
     │
etat.json          l'état persistant (statut, tentatives, durée, commit avant/après)
journal.log        l'audit horodaté de chaque lancement et de chaque vérification
STOP               l'arrêt propre (créé à la main ou par une règle)
```

**Les trois garanties** :

1. **Une tâche n'est « faite » que si son acceptation passe** — les commandes sont exécutées par le
   superviseur, pas par l'agent. Un agent qui se déclare satisfait ne suffit pas.
2. **Rien n'est perdu** : `etat.json` et `journal.log` sont écrits après chaque étape ; une relance
   reprend la première tâche non finie.
3. **On s'arrête proprement** : le STOP, le budget ou la file vide arrêtent la boucle ; l'agent
   n'est jamais tué au milieu d'un commit.

## 3. Ce que le superviseur **ne** fait pas

- Il **ne juge pas la qualité** au-delà de l'acceptation : une fiche vide qui passe le test
  « le fichier existe » passera. C'est pourquoi chaque acceptation combine un **fichier**, une
  **commande** et un **attendu** textuel.
- Il **ne corrige pas** l'agent : si la tâche échoue deux fois, elle est **bloquée** et le
  chantier continue avec la suivante (la file « jamais en attente »).
- Il **ne pousse pas** : les commits sont locaux ; un humain (ou une règle) pousse.
- Il **ne remplace pas** le pilote : `en-cours`, la roadmap et le journal restent tenus par l'agent
  principal, comme le veut la règle 10.

## 4. Les modes de panne, et la parade

| panne | symptôme | parade |
|---|---|---|
| **clé absente** | `MISSING_CREDENTIAL` | le superviseur lit `~/.config/drave/deepseek.key` ; sans clé, il s'arrête avec un message |
| **agent muet** | `code 124` (timeout) | `--timeout`, puis `bloque` après `max_tentatives` |
| **agent qui ne commite pas** | `commit_produit: false` | noté dans l'état ; l'acceptation exige la fiche |
| **session perdue** | `--session-id` inconnu | le superviseur relance **sans** `--session-id` (session neuve) |
| **contexte compacté** | l'agent oublie le fil | chaque mandat est **autonome** (il porte le contexte et les règles) |
| **autre session qui écrit** | worktree sale | le superviseur **n'exige pas** un worktree propre ; il note le HEAD et les fichiers modifiés |
| **régression** | l'acceptation passe, les portes non | chaque acceptation inclut `revue_documentation` et/ou `porte-bloc-linguistique` |

## 5. L'exploitation

```bash
# 1. vérifier l'état
python3 tools/chantier/superviseur.py etat

# 2. lancer la boucle (6 h d'agent max, 90 min par tâche, 2 tentatives)
python3 tools/chantier/superviseur.py boucle --budget 21600 --timeout 5400

# 3. surveiller
tail -f work/chantier/journal.log

# 4. arrêter proprement
python3 tools/chantier/superviseur.py stop      # ou : touch work/chantier/STOP

# 5. reprendre une tâche bloquée
python3 tools/chantier/superviseur.py reprendre J1.1
```

**Le lancement par cron** (une relance si le superviseur meurt) :

```cron
*/20 * * * * cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && \
  test -f work/chantier/STOP || python3 tools/chantier/superviseur.py boucle --budget 21600 \
  >> work/chantier/cron.log 2>&1
```

## 6. La leçon du 07/11

Le premier test réel (J0) a demandé **deux corrections** avant de passer : la clé (le mode
`headless` la réclame) et l'**absence de worktree propre** (le dépôt est multi-sessions). Un
méta-harnais se juge à ses **premiers échecs**, pas à sa conception : c'est pour cela que chaque
tâche a une acceptation exécutable et que l'état est écrit après chaque étape.
