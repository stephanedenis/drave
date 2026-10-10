> Campagne : **campagne-benefices** · expérience **39**
> Titre : 39. Audit des drapeaux par CHEMIN : une méthode de criblage, et sa portée exacte
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 39. Audit des drapeaux par CHEMIN : une méthode de criblage, et sa portée exacte

Après avoir trouvé `--ffn-gain` non câblé dans le chemin réparti (§38), la question qui suit
est mécanique : **combien d'autres drapeaux ne sont câblés que dans certains chemins ?**

**La méthode** (criblage statique) : extraire de `main.rs` les bornes des trois fonctions
d'exécution (`run_infer`, `run_ppl`, `run_ppl_reparti`), puis comparer les ensembles
d'assignations `mdl.<champ> = …` de chacune.

| fonction | champs assignés en propre |
|---|---|
| `run_infer` | 30 |
| `run_ppl` | 16 |
| **`run_ppl_reparti`** | **3** |

**Et c'est là qu'il faut être précis sur ce que la méthode PROUVE.** Le criblage a annoncé 29
champs « absents des autres chemins » pour `run_infer`, dont `act_thresh`, `act_topk`,
`attn_topk`, `qk_topk`, `moe_topk`… Or ces champs **sont** câblés dans les autres chemins — par
le **helper** `appliquer_quantification(&mut mdl, &opt)`, que le criblage ne lit pas. Le
criblage a donc un **angle mort** : il ne voit que les assignations écrites *dans* la fonction.

**Ce qu'il a réellement établi** : le chemin réparti assigne 3 champs en propre, le helper en
couvre 7 de plus, et c'est **précisément ce qui restait hors des deux** qui contenait le défaut
trouvé — `ffn_gain`, ni dans le helper, ni dans la fonction. La méthode a donc **servi**, à
condition de ne pas confondre « absent du criblage » avec « non câblé ».

**Ce qui n'est PAS concluant, et il faut le dire** : les candidats restants
(`--attn-window`, `--attn-sinks`, `--swa-pattern`, `--patch`, `--hebb-*`, `--flux-forcer`,
`--trace-flux`) n'ont **pas** été départagés — la tentative de mesure en chemin réparti a rendu
des perplexités **vides** (extraction en échec), et une mesure vide ne prouve rien. Ils sont
donc **à instruire**, pas déclarés sains ni défectueux.

**LES CANDIDATS ONT ÉTÉ INSTRUITS — et la mesure vide d'abord était MON erreur.** Le tirage
de port du banc allait jusqu'à 65 949, **au-delà de 65 535** : le nœud ne pouvait pas se lier,
et le pilote refusait en le nommant (`INJOIGNABLE (invalid port value)`). Une mesure vide ne
prouvait rien, et elle ne venait pas des drapeaux.

Reprise avec un port valide (61 578) et `--options-strict` (pour qu'un drapeau inconnu soit
refusé au lieu d'être ignoré) :

| drapeau | perplexité en réparti | verdict |
|---|---|---|
| aucun (référence) | 180,5245 | — |
| `--act-topk 64` | 1 137 878,95 | **agit** |
| `--qk-topk 64` | 24 955,44 | **agit** |
| `--act-thresh 0,01` | 209,7804 | **agit** |
| **`--attn-window 16`** | 180,5245 | **SANS EFFET** |
| **`--attn-topk 64`** | 180,5245 | **SANS EFFET** |
| `--moe-topk 2` | 180,5245 | sans effet — **normal** (Qwen2.5-0.5B est DENSE, il n'a pas d'experts) |

**Deux vrais constats, et un faux :**

- `--moe-topk` est **normalement** sans effet sur un modèle dense — ce n'est pas un défaut ;
- `--attn-topk` **voyage pourtant dans la trame** (le champ `attn_topk` est dans `struct Act`,
  avec `qk_topk` et `moe_topk`) et agit en local : il est donc **câblé et transporté**, mais
  sans effet sur le résultat **dans cette configuration** — à instruire : le top-k d'attention
  ne change-t-il rien à 32 jetons de contexte (où l'attention est déjà triviale) ? C'est
  l'explication la plus probable, et elle se teste en allongeant le contexte ;
- **`--attn-window` : deux constats, et une tentative de correction REVERTÉE.** À contexte long
  (512 jetons), le drapeau **agit en local** (13,1368 → **21,5801**) et reste **SANS EFFET en
  réparti** (18,5520 des deux côtés) : il n'est câblé que dans `run_infer` et `run_ppl`, pas
  dans `run_ppl_reparti` — même famille que `--ffn-gain` (§38). Et il **ne voyage pas** dans la
  trame (`struct Act` ne porte ni `attn_window`, ni `swa_pattern`, ni `attn_sinks`).
  Le câblage a été tenté : il rend un **résultat VIDE** (aucune perplexité), cause **non
  diagnostiquée**. La correction a donc été **REVERTÉE** plutôt que laissée dans l'arbre : une
  régression silencieuse vaut moins qu'un manque écrit. Après revert, la référence répartie est
  de nouveau **18,5520** et les 122 tests passent.
  **INSTRUIT, ET RÉSOLU PAR UN REFUS.** Le câblage a été refait **en regardant la sortie
  complète** (c'était la commande écrite au round précédent) : le run ne rend plus un vide
  mais un résultat **FAUX ET SILENCIEUX** — et c'est bien pire. Le pilote applique la fenêtre à
  ses douze couches, le nœud garde la sienne, et les deux moitiés ne calculent plus le même
  modèle :

  | avec `--attn-window 64` câblé | perplexité |
  |---|---|
  | référence locale (12 couches du pilote) | **195,5685** |
  | découpage (12 + 12 couches) | **50,3829** |
  | écart de flux | **7,42e-1** |

  **La correction a donc été remplacée par un REFUS EXPLICITE** : en chemin réparti, si l'un
  des trois réglages est donné, le moteur **s'arrête en expliquant** (code 2, aucune perplexité).
  Un drapeau inerte est un défaut ; **un drapeau qui fait calculer deux modèles différents sous
  le même nom en est un pire** — et le pire cas du dépôt est le résultat faux qui a l'air d'un
  résultat. Ces réglages restent honorés en local (`--ppl`) et en inférence (`--infer`), où ils
  ont été mesurés (13,1368 → 21,5801).

  **Pour les honorer en réparti**, il faudra les ajouter à `struct Act` et à l'encodeur de
  trame (protocole v7), puis les appliquer côté nœud comme les autres réglages d'activation ;

- `--attn-topk` : **mon hypothèse est confirmée par la mesure** — sans effet à 32 jetons
  (180,5245), il **agit** à 512 (18,5520 → **18,4032**). Il n'y a donc **pas** de défaut là :
  à contexte court, l'attention est déjà triviale, et le drapeau ne peut rien changer.
